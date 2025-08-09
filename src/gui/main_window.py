"""
Main GUI window for EasyWorship to ProPresenter converter
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import os
import threading
import json
import logging
from typing import List, Optional, Dict, Any
from collections import deque
from src.database.easyworship import EasyWorshipDatabase
from src.export.propresenter import ProPresenter6Exporter
from src.gui.settings_window import SettingsWindow

logger = logging.getLogger(__name__)

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("EasyWorship to ProPresenter Converter")
        self.root.geometry("900x700")
        
        self.db_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.search_var = tk.StringVar()
        self.selected_songs = set()
        self.songs_data = []
        self.filtered_songs = []  # Songs currently shown after filtering
        self.all_songs = []  # All songs from database
        self.search_history = deque(maxlen=10)  # Last 10 searches
        self.db = None
        self.exporter = ProPresenter6Exporter()
        self.export_in_progress = False
        
        # Load search history from settings
        self.load_search_history()
        
        self.setup_ui()
        self.auto_detect_easyworship()
        self.set_default_output_path()
        
        # Bind search variable to update function
        self.search_var.trace('w', self.on_search_changed)
        
    def setup_ui(self):
        """Build the main GUI interface"""
        # Create menu bar
        self.create_menu_bar()
        
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
        list_frame.rowconfigure(2, weight=1)  # Changed to row 2 for tree
        
        # Search frame
        search_frame = ttk.Frame(list_frame)
        search_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        search_frame.columnconfigure(1, weight=1)
        
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=(0, 5))
        
        # Search combobox with history
        self.search_combo = ttk.Combobox(search_frame, textvariable=self.search_var, width=30)
        self.search_combo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.search_combo.bind('<Return>', self.add_to_search_history)
        
        # Clear search button
        ttk.Button(search_frame, text="Clear", command=self.clear_search).pack(side=tk.LEFT, padx=(0, 10))
        
        # Result count label
        self.result_count_label = ttk.Label(search_frame, text="")
        self.result_count_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # Selection buttons
        button_frame = ttk.Frame(list_frame)
        button_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        ttk.Button(button_frame, text="Select All", command=self.select_all).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Select None", command=self.select_none).pack(side=tk.LEFT, padx=(0, 5))
        
        self.selected_count_label = ttk.Label(button_frame, text="0 songs selected")
        self.selected_count_label.pack(side=tk.LEFT, padx=(20, 0))
        
        # Create Treeview for song list
        columns = ('title', 'author', 'copyright', 'ccli')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='tree headings', selectmode='extended')
        self.tree.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))  # Changed to row 2
        
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
        vsb.grid(row=2, column=1, sticky=(tk.N, tk.S))  # Changed to row 2
        self.tree.configure(yscrollcommand=vsb.set)
        
        hsb = ttk.Scrollbar(list_frame, orient="horizontal", command=self.tree.xview)
        hsb.grid(row=3, column=0, sticky=(tk.W, tk.E))  # Changed to row 3
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
        
    def create_menu_bar(self):
        """Create the application menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Load Database...", command=self.browse_database)
        file_menu.add_command(label="Set Export Directory...", command=self.browse_output_path)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Select All", command=self.select_all)
        edit_menu.add_command(label="Select None", command=self.select_none)
        edit_menu.add_separator()
        edit_menu.add_command(label="Section Mappings...", command=self.open_settings)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
    
    def open_settings(self):
        """Open the settings window for section mappings"""
        settings = SettingsWindow(parent_window=self)
        self.root.wait_window(settings.window)
        
        # Reload section mappings if they changed
        if hasattr(self, 'db') and self.db:
            self.db.reload_section_mappings()
    
    def reload_section_mappings(self):
        """Reload section mappings after settings change"""
        if hasattr(self, 'db') and self.db:
            self.db.reload_section_mappings()
    
    def show_about(self):
        """Show about dialog"""
        about_text = """EasyWorship to ProPresenter Converter
        
Version: 1.0.0
Released: January 2025
        
Converts songs from EasyWorship 6.1 database format 
to ProPresenter 6 format with Swedish language support.

Features:
• Real-time search and filtering
• Configurable section mappings
• Batch export with progress tracking
• Full Swedish character support
        
© 2025 - Created with Python and Tkinter
GitHub: https://github.com/karllinder/ewexport"""
        
        messagebox.showinfo("About", about_text)
    
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
            self.all_songs = self.db.get_all_songs()
            self.songs_data = self.all_songs.copy()
            self.filtered_songs = self.all_songs.copy()
            song_count = len(self.all_songs)
            
            # Apply current search filter if any
            if self.search_var.get():
                self.apply_search_filter()
            else:
                self.display_songs(self.filtered_songs)
            
            self.status_label.config(text=f"Loaded {song_count} songs from database")
            self.export_btn.config(state='normal' if song_count > 0 else 'disabled')
            self.update_selected_count()
            self.update_result_count()
            
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
            
            # Use all_songs instead of songs_data to ensure we export all selected songs
            for song_data in self.all_songs:
                if song_data['rowid'] in selected_song_ids:
                    # Get processed lyrics with sections
                    processed = self.db.get_song_with_processed_lyrics(song_data['rowid'])
                    
                    if processed and processed.get('sections'):
                        sections = processed['sections']
                        songs_to_export.append((song_data, sections))
                    else:
                        # Songs without any parseable content - add with empty section
                        # This will be caught by the exporter's validation
                        empty_sections = []
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
            
            # Clear selection after successful export
            self.select_none()
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
            
            # Clear selection even if some exports failed
            self.select_none()
        
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
    
    def on_search_changed(self, *args):
        """Handle search text changes for real-time filtering"""
        self.apply_search_filter()
    
    def apply_search_filter(self):
        """Apply search filter to song list"""
        search_text = self.search_var.get().lower().strip()
        
        if not search_text:
            # No search, show all songs
            self.filtered_songs = self.all_songs.copy()
        else:
            # Filter songs based on search text
            self.filtered_songs = []
            for song in self.all_songs:
                # Search in title, author, copyright, and CCLI number
                if (search_text in (song['title'] or '').lower() or
                    search_text in (song['author'] or '').lower() or
                    search_text in (song['copyright'] or '').lower() or
                    search_text in (song['reference_number'] or '').lower()):
                    self.filtered_songs.append(song)
        
        # Update display
        self.display_songs(self.filtered_songs)
        self.update_result_count()
    
    def display_songs(self, songs: List[Dict[str, Any]]):
        """Display the given list of songs in the tree view"""
        # Remember which songs were selected
        previously_selected = self.selected_songs.copy()
        
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add filtered songs
        for song in songs:
            song_id = song['rowid']
            is_selected = song_id in previously_selected
            
            item_id = self.tree.insert('', 'end', 
                                      text='☑' if is_selected else '☐',
                                      values=(
                                          song['title'],
                                          song['author'] or '-',
                                          song['copyright'] or '-',
                                          song['reference_number'] or '-'
                                      ),
                                      tags=(song_id,))
    
    def update_result_count(self):
        """Update the result count label"""
        total = len(self.all_songs)
        shown = len(self.filtered_songs)
        
        if self.search_var.get():
            self.result_count_label.config(text=f"Showing {shown} of {total} songs")
        else:
            self.result_count_label.config(text=f"Total: {total} songs")
    
    def clear_search(self):
        """Clear the search field and show all songs"""
        self.search_var.set('')
        self.apply_search_filter()
    
    def add_to_search_history(self, event=None):
        """Add current search to history when Enter is pressed"""
        search_text = self.search_var.get().strip()
        if search_text and search_text not in self.search_history:
            self.search_history.append(search_text)
            self.update_search_combo_values()
            self.save_search_history()
    
    def update_search_combo_values(self):
        """Update the combobox dropdown with search history"""
        self.search_combo['values'] = list(self.search_history)
    
    def load_search_history(self):
        """Load search history from settings file"""
        settings_dir = Path.home() / '.ewexport'
        settings_file = settings_dir / 'search_history.json'
        
        if settings_file.exists():
            try:
                with open(settings_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    history = data.get('search_history', [])
                    for item in history[-10:]:  # Keep last 10
                        self.search_history.append(item)
            except Exception:
                pass  # Ignore errors loading history
    
    def save_search_history(self):
        """Save search history to settings file"""
        settings_dir = Path.home() / '.ewexport'
        settings_dir.mkdir(exist_ok=True)
        settings_file = settings_dir / 'search_history.json'
        
        try:
            with open(settings_file, 'w', encoding='utf-8') as f:
                json.dump({'search_history': list(self.search_history)}, f, indent=2)
        except Exception:
            pass  # Ignore errors saving history
    
    def run(self):
        # Set initial search history dropdown values
        self.update_search_combo_values()
        self.root.mainloop()