"""
Main GUI window for EasyWorship to ProPresenter converter
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import os
import threading
from typing import List, Optional
from src.database.easyworship import EasyWorshipDatabase
from src.export.propresenter import ProPresenter6Exporter

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("EasyWorship to ProPresenter Converter")
        self.root.geometry("900x700")
        
        self.db_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.selected_songs = set()
        self.songs_data = []
        self.db = None
        self.exporter = ProPresenter6Exporter()
        self.export_in_progress = False
        
        self.setup_ui()
        self.auto_detect_easyworship()
        self.set_default_output_path()
        
    def setup_ui(self):
        """Build the main GUI interface"""
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Database selection frame
        db_frame = ttk.LabelFrame(main_frame, text="EasyWorship Database", padding="10")
        db_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        db_frame.columnconfigure(1, weight=1)
        
        ttk.Label(db_frame, text="Database Path:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        path_entry = ttk.Entry(db_frame, textvariable=self.db_path, width=50)
        path_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        
        browse_btn = ttk.Button(db_frame, text="Browse...", command=self.browse_database)
        browse_btn.grid(row=0, column=2, padx=(5, 0))
        
        load_btn = ttk.Button(db_frame, text="Load Songs", command=self.load_songs)
        load_btn.grid(row=0, column=3, padx=(5, 0))
        
        # Song count label
        self.status_label = ttk.Label(db_frame, text="No database loaded")
        self.status_label.grid(row=1, column=0, columnspan=4, sticky=tk.W, pady=(5, 0))
        
        # Song list frame
        list_frame = ttk.LabelFrame(main_frame, text="Songs", padding="10")
        list_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(1, weight=1)
        
        # Selection buttons
        button_frame = ttk.Frame(list_frame)
        button_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        ttk.Button(button_frame, text="Select All", command=self.select_all).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Select None", command=self.select_none).pack(side=tk.LEFT, padx=(0, 5))
        
        self.selected_count_label = ttk.Label(button_frame, text="0 songs selected")
        self.selected_count_label.pack(side=tk.LEFT, padx=(20, 0))
        
        # Create Treeview for song list
        columns = ('title', 'author', 'copyright', 'ccli')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='tree headings', selectmode='extended')
        self.tree.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure columns
        self.tree.heading('#0', text='✓', anchor=tk.W)
        self.tree.column('#0', width=30, stretch=False)
        
        self.tree.heading('title', text='Title')
        self.tree.column('title', width=300)
        
        self.tree.heading('author', text='Author')
        self.tree.column('author', width=200)
        
        self.tree.heading('copyright', text='Copyright')
        self.tree.column('copyright', width=200)
        
        self.tree.heading('ccli', text='CCLI/Ref')
        self.tree.column('ccli', width=100)
        
        # Add scrollbars
        vsb = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        vsb.grid(row=1, column=1, sticky=(tk.N, tk.S))
        self.tree.configure(yscrollcommand=vsb.set)
        
        hsb = ttk.Scrollbar(list_frame, orient="horizontal", command=self.tree.xview)
        hsb.grid(row=2, column=0, sticky=(tk.W, tk.E))
        self.tree.configure(xscrollcommand=hsb.set)
        
        # Bind click event for checkbox toggle
        self.tree.bind('<ButtonRelease-1>', self.on_item_click)
        
        # Export frame
        export_frame = ttk.LabelFrame(main_frame, text="Export Options", padding="10")
        export_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        export_frame.columnconfigure(1, weight=1)
        
        # Output path selection
        ttk.Label(export_frame, text="Output Path:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        output_entry = ttk.Entry(export_frame, textvariable=self.output_path, width=50)
        output_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        
        browse_output_btn = ttk.Button(export_frame, text="Browse...", command=self.browse_output_path)
        browse_output_btn.grid(row=0, column=2, padx=(5, 0))
        
        # Progress section
        progress_frame = ttk.Frame(export_frame)
        progress_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        progress_frame.columnconfigure(0, weight=1)
        
        # Progress bar
        self.progress = ttk.Progressbar(progress_frame, mode='determinate')
        self.progress.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Progress label
        self.progress_label = ttk.Label(progress_frame, text="Ready to export")
        self.progress_label.grid(row=1, column=0, sticky=tk.W)
        
        # Export button
        button_frame = ttk.Frame(export_frame)
        button_frame.grid(row=2, column=0, columnspan=3, pady=(10, 0))
        
        self.export_btn = ttk.Button(button_frame, text="Export Selected Songs", 
                                     command=self.start_export, state='disabled')
        self.export_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.cancel_btn = ttk.Button(button_frame, text="Cancel Export", 
                                     command=self.cancel_export, state='disabled')
        self.cancel_btn.pack(side=tk.LEFT)
        
    def auto_detect_easyworship(self):
        """Try to auto-detect EasyWorship database path"""
        # Common EasyWorship installation paths
        possible_paths = [
            Path(os.environ.get('PROGRAMDATA', 'C:\\ProgramData')) / 'Softouch' / 'Easyworship' / 'Default' / 'Databases' / 'Data',
            Path(os.environ.get('USERPROFILE', '')) / 'Documents' / 'EasyWorship' / 'Default' / 'Databases' / 'Data',
            Path('C:\\Users\\Public\\Documents\\Softouch\\Easyworship\\Default\\Databases\\Data'),
            Path('C:\\Claud\\ewtest\\orginaldb'),  # Test path from CLAUDE.md
        ]
        
        for path in possible_paths:
            if path.exists() and (path / 'Songs.db').exists():
                self.db_path.set(str(path))
                self.load_songs()
                break
    
    def browse_database(self):
        """Browse for EasyWorship database folder"""
        folder = filedialog.askdirectory(
            title="Select EasyWorship Database Folder",
            initialdir=self.db_path.get() if self.db_path.get() else os.path.expanduser("~")
        )
        
        if folder:
            self.db_path.set(folder)
            self.load_songs()
    
    def load_songs(self):
        """Load songs from the selected database"""
        db_path = self.db_path.get()
        if not db_path:
            messagebox.showwarning("No Path", "Please select a database folder first.")
            return
        
        try:
            self.db = EasyWorshipDatabase(db_path)
            
            if not self.db.validate_database():
                messagebox.showerror("Invalid Database", 
                                   "The selected folder does not contain valid EasyWorship database files.")
                return
            
            # Clear existing items
            for item in self.tree.get_children():
                self.tree.delete(item)
            self.selected_songs.clear()
            
            # Load songs
            self.songs_data = self.db.get_all_songs()
            song_count = len(self.songs_data)
            
            # Populate tree
            for song in self.songs_data:
                item_id = self.tree.insert('', 'end', 
                                          text='☐',
                                          values=(
                                              song['title'],
                                              song['author'] or '-',
                                              song['copyright'] or '-',
                                              song['reference_number'] or '-'
                                          ),
                                          tags=(song['rowid'],))
            
            self.status_label.config(text=f"Loaded {song_count} songs from database")
            self.export_btn.config(state='normal' if song_count > 0 else 'disabled')
            self.update_selected_count()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load database: {str(e)}")
    
    def on_item_click(self, event):
        """Handle click on tree item to toggle selection"""
        region = self.tree.identify_region(event.x, event.y)
        
        if region == "tree":
            item = self.tree.identify_row(event.y)
            if item:
                self.toggle_item_selection(item)
    
    def toggle_item_selection(self, item):
        """Toggle selection state of an item"""
        tags = self.tree.item(item, 'tags')
        if tags and len(tags) > 0:
            song_id = int(tags[0])  # Ensure it's an integer
            
            if song_id in self.selected_songs:
                self.selected_songs.remove(song_id)
                self.tree.item(item, text='☐')
            else:
                self.selected_songs.add(song_id)
                self.tree.item(item, text='☑')
        
        self.update_selected_count()
    
    def select_all(self):
        """Select all songs"""
        for item in self.tree.get_children():
            tags = self.tree.item(item, 'tags')
            if tags and len(tags) > 0:
                song_id = int(tags[0])  # Ensure it's an integer
                self.selected_songs.add(song_id)
                self.tree.item(item, text='☑')
        
        self.update_selected_count()
    
    def select_none(self):
        """Deselect all songs"""
        self.selected_songs.clear()
        for item in self.tree.get_children():
            self.tree.item(item, text='☐')
        
        self.update_selected_count()
    
    def update_selected_count(self):
        """Update the selected songs count label"""
        count = len(self.selected_songs)
        self.selected_count_label.config(text=f"{count} song{'s' if count != 1 else ''} selected")
    
    def set_default_output_path(self):
        """Set default output path"""
        desktop = Path.home() / "Desktop"
        default_path = desktop / "ProPresenter_Export"
        self.output_path.set(str(default_path))
    
    def browse_output_path(self):
        """Browse for output directory"""
        folder = filedialog.askdirectory(
            title="Select Export Directory",
            initialdir=self.output_path.get() if self.output_path.get() else str(Path.home())
        )
        
        if folder:
            self.output_path.set(folder)
    
    def start_export(self):
        """Start the export process in a separate thread"""
        if not self.selected_songs:
            messagebox.showinfo("No Selection", "Please select at least one song to export.")
            return
        
        if not self.output_path.get():
            messagebox.showwarning("No Output Path", "Please select an output directory.")
            return
        
        # Confirm export
        count = len(self.selected_songs)
        if not messagebox.askyesno("Confirm Export", 
                                  f"Export {count} selected song{'s' if count != 1 else ''} to ProPresenter 6 format?"):
            return
        
        # Start export in background thread
        self.export_in_progress = True
        self.export_btn.config(state='disabled')
        self.cancel_btn.config(state='normal')
        self.progress.config(mode='determinate', value=0)
        self.progress_label.config(text="Preparing export...")
        
        self.export_thread = threading.Thread(target=self.export_worker, daemon=True)
        self.export_thread.start()
    
    def export_worker(self):
        """Background worker for export process"""
        try:
            # Collect selected songs with processed lyrics
            songs_to_export = []
            selected_song_ids = list(self.selected_songs)
            
            for song_data in self.songs_data:
                if song_data['rowid'] in selected_song_ids:
                    # Get processed lyrics with sections
                    processed = self.db.get_song_with_processed_lyrics(song_data['rowid'])
                    
                    if processed and processed.get('sections'):
                        sections = processed['sections']
                        songs_to_export.append((song_data, sections))
                    else:
                        # Handle songs without lyrics gracefully
                        empty_sections = [{'type': 'verse', 'content': 'No lyrics available'}]
                        songs_to_export.append((song_data, empty_sections))
            
            # Export songs
            output_dir = Path(self.output_path.get())
            successful, failed = self.exporter.export_songs_batch(
                songs_to_export, 
                output_dir, 
                progress_callback=self.update_export_progress
            )
            
            # Update UI in main thread
            self.root.after(0, self.export_complete, successful, failed)
            
        except Exception as e:
            error_msg = f"Export failed with error: {str(e)}"
            self.root.after(0, self.export_error, error_msg)
    
    def update_export_progress(self, current: int, total: int, song_title: str):
        """Update progress bar and label (called from background thread)"""
        def update_ui():
            if total > 0:
                progress_percent = (current / total) * 100
                self.progress.config(value=progress_percent)
            
            if current < total:
                self.progress_label.config(text=f"Exporting: {song_title} ({current + 1}/{total})")
            else:
                self.progress_label.config(text="Export complete")
        
        self.root.after(0, update_ui)
    
    def export_complete(self, successful: List[str], failed: List[str]):
        """Handle export completion"""
        self.export_in_progress = False
        self.export_btn.config(state='normal')
        self.cancel_btn.config(state='disabled')
        self.progress.config(value=100)
        
        # Show results
        success_count = len(successful)
        fail_count = len(failed)
        
        if fail_count == 0:
            message = f"Successfully exported {success_count} song{'s' if success_count != 1 else ''}!\n\n"
            message += f"Files saved to: {self.output_path.get()}"
            messagebox.showinfo("Export Complete", message)
        else:
            message = f"Export completed with some issues:\n\n"
            message += f"Successfully exported: {success_count} songs\n"
            message += f"Failed to export: {fail_count} songs\n\n"
            
            if failed:
                message += "Failed exports:\n"
                for error in failed[:5]:  # Show first 5 errors
                    message += f"• {error}\n"
                if len(failed) > 5:
                    message += f"... and {len(failed) - 5} more errors"
            
            messagebox.showwarning("Export Completed with Errors", message)
        
        self.progress_label.config(text="Ready to export")
    
    def export_error(self, error_message: str):
        """Handle export error"""
        self.export_in_progress = False
        self.export_btn.config(state='normal')
        self.cancel_btn.config(state='disabled')
        self.progress.config(value=0)
        self.progress_label.config(text="Export failed")
        
        messagebox.showerror("Export Error", error_message)
    
    def cancel_export(self):
        """Cancel the export process"""
        if self.export_in_progress:
            # Note: This is a simple cancellation - doesn't actually stop the thread
            # For a more robust solution, we'd need to implement proper thread cancellation
            self.export_in_progress = False
            self.export_btn.config(state='normal')
            self.cancel_btn.config(state='disabled')
            self.progress.config(value=0)
            self.progress_label.config(text="Export cancelled")
            messagebox.showinfo("Export Cancelled", "Export operation was cancelled.")
    
    def run(self):
        self.root.mainloop()