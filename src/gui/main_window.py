"""
Main GUI window for EasyWorship to ProPresenter converter
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import os
from typing import List, Optional
from src.database.easyworship import EasyWorshipDatabase

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("EasyWorship to ProPresenter Converter")
        self.root.geometry("900x700")
        
        self.db_path = tk.StringVar()
        self.selected_songs = set()
        self.songs_data = []
        self.db = None
        
        self.setup_ui()
        self.auto_detect_easyworship()
        
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
        export_frame = ttk.Frame(main_frame)
        export_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E))
        
        # Progress bar
        self.progress = ttk.Progressbar(export_frame, mode='indeterminate')
        self.progress.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        export_frame.columnconfigure(0, weight=1)
        
        # Export button
        self.export_btn = ttk.Button(export_frame, text="Export Selected Songs", 
                                     command=self.export_songs, state='disabled')
        self.export_btn.grid(row=1, column=0, pady=(5, 0))
        
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
            song_id = tags[0]
            
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
                song_id = tags[0]
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
    
    def export_songs(self):
        """Export selected songs (stub for now)"""
        if not self.selected_songs:
            messagebox.showinfo("No Selection", "Please select at least one song to export.")
            return
        
        # For now, just show a message
        messagebox.showinfo("Export", 
                          f"Export functionality will be implemented in Sprint 3.\n"
                          f"Selected {len(self.selected_songs)} songs for export.")
    
    def run(self):
        self.root.mainloop()