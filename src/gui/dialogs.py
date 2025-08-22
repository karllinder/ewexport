"""
Dialog windows for user interactions
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path
from typing import Optional, List, Tuple
import os

class DuplicateFileDialog:
    """Dialog for handling duplicate files during export"""
    
    ACTIONS = {
        'skip': 'Skip this file',
        'overwrite': 'Overwrite existing file',
        'rename': 'Rename with number suffix',
        'rename_custom': 'Choose custom name'
    }
    
    def __init__(self, parent, file_path: Path, remaining_count: int = 0):
        """
        Initialize duplicate file dialog
        
        Args:
            parent: Parent window
            file_path: Path to the duplicate file
            remaining_count: Number of remaining duplicates
        """
        self.result = None
        self.apply_to_all = False
        
        # Create dialog
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Duplicate File Found")
        self.dialog.geometry("500x300")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center on parent
        parent.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - 250
        y = parent.winfo_y() + (parent.winfo_height() // 2) - 150
        self.dialog.geometry(f"+{x}+{y}")
        
        # Build UI
        self._build_ui(file_path, remaining_count)
        
        # Focus
        self.dialog.focus_set()
    
    def _build_ui(self, file_path: Path, remaining_count: int):
        """Build the dialog UI"""
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.dialog.columnconfigure(0, weight=1)
        self.dialog.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # Message
        msg = f"The file already exists:\n\n{file_path.name}\n\nWhat would you like to do?"
        ttk.Label(main_frame, text=msg, wraplength=450).grid(row=0, column=0, pady=(0, 20))
        
        # Action selection
        self.action_var = tk.StringVar(value='skip')
        
        actions_frame = ttk.LabelFrame(main_frame, text="Choose Action", padding="10")
        actions_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        for action, label in self.ACTIONS.items():
            ttk.Radiobutton(actions_frame, text=label, variable=self.action_var, 
                          value=action).pack(anchor=tk.W, pady=2)
        
        # Apply to all checkbox (if there are more duplicates)
        if remaining_count > 0:
            self.apply_all_var = tk.BooleanVar(value=False)
            msg = f"Apply this action to all {remaining_count + 1} duplicate files"
            ttk.Checkbutton(main_frame, text=msg, 
                          variable=self.apply_all_var).grid(row=2, column=0, pady=10)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, pady=(10, 0))
        
        ttk.Button(button_frame, text="OK", command=self._ok_clicked, 
                  width=10).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self._cancel_clicked, 
                  width=10).pack(side=tk.LEFT)
        
        # Bind Enter and Escape
        self.dialog.bind('<Return>', lambda e: self._ok_clicked())
        self.dialog.bind('<Escape>', lambda e: self._cancel_clicked())
    
    def _ok_clicked(self):
        """Handle OK button click"""
        action = self.action_var.get()
        
        if action == 'rename_custom':
            # Show custom name dialog
            custom_name = self._get_custom_name()
            if custom_name:
                self.result = ('rename_custom', custom_name)
            else:
                return  # User cancelled custom name
        else:
            self.result = (action, None)
        
        # Check if apply to all
        if hasattr(self, 'apply_all_var'):
            self.apply_to_all = self.apply_all_var.get()
        
        self.dialog.destroy()
    
    def _cancel_clicked(self):
        """Handle Cancel button click"""
        self.result = ('cancel', None)
        self.dialog.destroy()
    
    def _get_custom_name(self) -> Optional[str]:
        """Get custom filename from user"""
        dialog = tk.Toplevel(self.dialog)
        dialog.title("Enter Custom Name")
        dialog.geometry("400x120")
        dialog.transient(self.dialog)
        dialog.grab_set()
        
        # Center on parent
        self.dialog.update_idletasks()
        x = self.dialog.winfo_x() + 50
        y = self.dialog.winfo_y() + 50
        dialog.geometry(f"+{x}+{y}")
        
        # Create form
        frame = ttk.Frame(dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Enter new filename (without extension):").pack(anchor=tk.W)
        
        name_var = tk.StringVar()
        entry = ttk.Entry(frame, textvariable=name_var, width=40)
        entry.pack(fill=tk.X, pady=(5, 10))
        entry.focus_set()
        
        result = {'name': None}
        
        def ok_clicked():
            name = name_var.get().strip()
            if name:
                # Sanitize filename
                invalid_chars = r'<>:"/\|?*'
                for char in invalid_chars:
                    name = name.replace(char, '_')
                result['name'] = name
                dialog.destroy()
        
        def cancel_clicked():
            dialog.destroy()
        
        # Buttons
        button_frame = ttk.Frame(frame)
        button_frame.pack()
        
        ttk.Button(button_frame, text="OK", command=ok_clicked).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=cancel_clicked).pack(side=tk.LEFT)
        
        # Bindings
        entry.bind('<Return>', lambda e: ok_clicked())
        dialog.bind('<Escape>', lambda e: cancel_clicked())
        
        # Wait for dialog
        dialog.wait_window()
        
        return result['name']


class ExportOptionsDialog:
    """Dialog for configuring export options"""
    
    def __init__(self, parent, config_manager):
        """
        Initialize export options dialog
        
        Args:
            parent: Parent window
            config_manager: Configuration manager instance
        """
        self.config = config_manager
        self.result = None
        
        # Create dialog
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Export Options")
        self.dialog.geometry("650x600")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center on parent
        parent.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - 325
        y = parent.winfo_y() + (parent.winfo_height() // 2) - 300
        self.dialog.geometry(f"+{x}+{y}")
        
        # Build UI
        self._build_ui()
        
        # Load current settings
        self._load_settings()
        
        # Focus
        self.dialog.focus_set()
    
    def _build_ui(self):
        """Build the dialog UI"""
        # Create notebook for tabs
        notebook = ttk.Notebook(self.dialog, padding="5")
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 5))
        
        # General tab
        general_frame = ttk.Frame(notebook)
        notebook.add(general_frame, text="General")
        self._build_general_tab(general_frame)
        
        # Formatting tab
        format_frame = ttk.Frame(notebook)
        notebook.add(format_frame, text="Formatting")
        self._build_format_tab(format_frame)
        
        # Slides tab
        slides_frame = ttk.Frame(notebook)
        notebook.add(slides_frame, text="Slides")
        self._build_slides_tab(slides_frame)
        
        # Bottom buttons
        button_frame = ttk.Frame(self.dialog)
        button_frame.pack(side=tk.BOTTOM, pady=10)
        
        ttk.Button(button_frame, text="Save", command=self._save_clicked, 
                  width=10).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Apply", command=self._apply_clicked, 
                  width=10).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self._cancel_clicked, 
                  width=10).pack(side=tk.LEFT, padx=5)
        
        # Handle window close button
        self.dialog.protocol("WM_DELETE_WINDOW", self._on_closing)
    
    def _build_general_tab(self, parent):
        """Build the general options tab"""
        frame = ttk.Frame(parent, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Output directory
        dir_frame = ttk.LabelFrame(frame, text="Output Directory", padding="10")
        dir_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.output_dir_var = tk.StringVar()
        dir_entry = ttk.Entry(dir_frame, textvariable=self.output_dir_var, width=50)
        dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Button(dir_frame, text="Browse...", 
                  command=self._browse_output_dir).pack(side=tk.LEFT, padx=(5, 0))
        
        # File naming
        naming_frame = ttk.LabelFrame(frame, text="File Naming", padding="10")
        naming_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.include_ccli_var = tk.BooleanVar()
        ttk.Checkbutton(naming_frame, text="Include CCLI number in filename", 
                       variable=self.include_ccli_var).pack(anchor=tk.W, pady=2)
        
        self.include_author_var = tk.BooleanVar()
        ttk.Checkbutton(naming_frame, text="Include author in filename", 
                       variable=self.include_author_var).pack(anchor=tk.W, pady=2)
        
        # Duplicate handling
        dup_frame = ttk.LabelFrame(frame, text="Duplicate Files", padding="10")
        dup_frame.pack(fill=tk.X)
        
        self.overwrite_var = tk.BooleanVar()
        ttk.Checkbutton(dup_frame, text="Overwrite existing files without asking", 
                       variable=self.overwrite_var).pack(anchor=tk.W, pady=2)
    
    def _build_format_tab(self, parent):
        """Build the formatting options tab"""
        frame = ttk.Frame(parent, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Master formatting control
        master_frame = ttk.LabelFrame(frame, text="Formatting Control", padding="10")
        master_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.formatting_enabled_var = tk.BooleanVar()
        formatting_check = ttk.Checkbutton(master_frame, text="Enable custom formatting", 
                                          variable=self.formatting_enabled_var,
                                          command=self._toggle_formatting_options)
        formatting_check.pack(anchor=tk.W, pady=2)
        ttk.Label(master_frame, text="When disabled, uses default ProPresenter formatting",
                 font=('TkDefaultFont', 8)).pack(anchor=tk.W, padx=(20, 0))
        
        # Font settings
        self.font_frame = ttk.LabelFrame(frame, text="Font Settings", padding="10")
        self.font_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Font family with Windows fonts
        ttk.Label(self.font_frame, text="Font:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.font_family_var = tk.StringVar()
        
        # Get all available Windows fonts
        available_fonts = self._get_available_fonts()
        self.font_combo = ttk.Combobox(self.font_frame, textvariable=self.font_family_var, 
                                       values=available_fonts, 
                                       width=30)
        self.font_combo.grid(row=0, column=1, sticky=tk.W, padx=(5, 0), pady=2)
        
        # Font size with dropdown and custom entry (Issue #8 fix)
        ttk.Label(self.font_frame, text="Size:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.font_size_var = tk.StringVar()  # Changed to StringVar for combobox
        
        # Common font sizes for quick selection
        common_sizes = ['12', '18', '24', '30', '36', '48', '60', '72', '84', '96', '120', '144', '168', '200']
        self.size_combo = ttk.Combobox(self.font_frame, textvariable=self.font_size_var, 
                                       values=common_sizes, width=8, state='normal')
        self.size_combo.grid(row=1, column=1, sticky=tk.W, padx=(5, 0), pady=2)
        
        # Add validation for custom entries (12-200 range)
        def validate_font_size(event=None):
            try:
                size = int(self.font_size_var.get())
                if size < 12:
                    self.font_size_var.set('12')
                elif size > 200:
                    self.font_size_var.set('200')
            except ValueError:
                # If not a valid number, reset to default
                self.font_size_var.set('72')
        
        self.size_combo.bind('<FocusOut>', validate_font_size)
        self.size_combo.bind('<Return>', validate_font_size)
        
        # Change font checkbox
        self.change_font_var = tk.BooleanVar()
        self.change_font_check = ttk.Checkbutton(self.font_frame, 
                                                 text="Override song font with selected font", 
                                                 variable=self.change_font_var)
        self.change_font_check.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=(5, 0))
        
        # Text processing options
        self.text_opts_frame = ttk.LabelFrame(frame, text="Text Processing", padding="10")
        self.text_opts_frame.pack(fill=tk.X)
        
        self.auto_break_lines_var = tk.BooleanVar()
        self.auto_break_check = ttk.Checkbutton(self.text_opts_frame, 
                                               text="Automatically break long lines", 
                                               variable=self.auto_break_lines_var)
        self.auto_break_check.pack(anchor=tk.W, pady=2)
        
        ttk.Label(self.text_opts_frame, text="Maximum lines per slide:").pack(anchor=tk.W, pady=(5, 2))
        self.max_lines_var = tk.IntVar()
        self.max_lines_spin = ttk.Spinbox(self.text_opts_frame, from_=1, to=10, 
                                         textvariable=self.max_lines_var, width=10)
        self.max_lines_spin.pack(anchor=tk.W)
    
    def _build_slides_tab(self, parent):
        """Build the slides options tab"""
        frame = ttk.Frame(parent, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Intro slide
        intro_frame = ttk.LabelFrame(frame, text="First Slide", padding="10")
        intro_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.add_intro_var = tk.BooleanVar()
        intro_check = ttk.Checkbutton(intro_frame, text="Add intro slide as first slide", 
                                     variable=self.add_intro_var, 
                                     command=self._toggle_intro_options)
        intro_check.pack(anchor=tk.W, pady=2)
        
        ttk.Label(intro_frame, text="Intro slide text:").pack(anchor=tk.W, pady=(5, 2))
        self.intro_text_var = tk.StringVar()
        self.intro_text_entry = ttk.Entry(intro_frame, textvariable=self.intro_text_var, 
                                         width=40, state='disabled')
        self.intro_text_entry.pack(anchor=tk.W)
        
        ttk.Label(intro_frame, text="Group name:").pack(anchor=tk.W, pady=(5, 2))
        self.intro_group_var = tk.StringVar()
        self.intro_group_entry = ttk.Entry(intro_frame, textvariable=self.intro_group_var, 
                                          width=20, state='disabled')
        self.intro_group_entry.pack(anchor=tk.W)
        
        # Blank slide
        blank_frame = ttk.LabelFrame(frame, text="Last Slide", padding="10")
        blank_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.add_blank_var = tk.BooleanVar()
        blank_check = ttk.Checkbutton(blank_frame, text="Add blank slide as last slide", 
                                     variable=self.add_blank_var, 
                                     command=self._toggle_blank_options)
        blank_check.pack(anchor=tk.W, pady=2)
        
        ttk.Label(blank_frame, text="Group name:").pack(anchor=tk.W, pady=(5, 2))
        self.blank_group_var = tk.StringVar()
        self.blank_group_entry = ttk.Entry(blank_frame, textvariable=self.blank_group_var, 
                                          width=20, state='disabled')
        self.blank_group_entry.pack(anchor=tk.W)
    
    def _get_available_fonts(self):
        """Get list of available fonts on Windows"""
        try:
            import tkinter.font as tkfont
            # Get all font families available in the system
            fonts = list(tkfont.families())
            # Filter out fonts that start with @ (vertical fonts in Windows)
            fonts = [f for f in fonts if not f.startswith('@')]
            # Sort alphabetically
            fonts.sort()
            return fonts
        except Exception:
            # Fallback to common fonts if can't get system fonts
            return ['Arial', 'Helvetica', 'Times New Roman', 'Calibri', 
                   'Verdana', 'Tahoma', 'Georgia', 'Impact', 'Comic Sans MS']
    
    def _toggle_formatting_options(self):
        """Enable/disable formatting options based on master control"""
        state = 'normal' if self.formatting_enabled_var.get() else 'disabled'
        
        # Toggle font frame widgets
        for child in self.font_frame.winfo_children():
            if isinstance(child, (ttk.Entry, ttk.Combobox, ttk.Checkbutton)):
                child.config(state=state)
        
        # Toggle text options frame widgets
        for child in self.text_opts_frame.winfo_children():
            if isinstance(child, (ttk.Entry, ttk.Spinbox, ttk.Checkbutton, ttk.Combobox)):
                child.config(state=state)
    
    def _toggle_intro_options(self):
        """Enable/disable intro slide options"""
        state = 'normal' if self.add_intro_var.get() else 'disabled'
        self.intro_text_entry.config(state=state)
        self.intro_group_entry.config(state=state)
    
    def _toggle_blank_options(self):
        """Enable/disable blank slide options"""
        state = 'normal' if self.add_blank_var.get() else 'disabled'
        self.blank_group_entry.config(state=state)
    
    def _browse_output_dir(self):
        """Browse for output directory"""
        current = self.output_dir_var.get() or str(Path.home())
        
        directory = filedialog.askdirectory(
            title="Select Output Directory",
            initialdir=current
        )
        
        if directory:
            self.output_dir_var.set(directory)
    
    def _load_settings(self):
        """Load current settings from config"""
        # General
        output_dir = self.config.get('export.output_directory')
        if output_dir:
            self.output_dir_var.set(output_dir)
        
        self.include_ccli_var.set(self.config.get('export.include_ccli_in_filename', False))
        self.include_author_var.set(self.config.get('export.include_author_in_filename', False))
        self.overwrite_var.set(self.config.get('export.overwrite_existing', False))
        
        # Formatting
        self.formatting_enabled_var.set(self.config.get('export.formatting_enabled', False))
        self.font_family_var.set(self.config.get('export.font.family', 'Arial'))
        self.font_size_var.set(str(self.config.get('export.font.size', 72)))
        self.change_font_var.set(self.config.get('export.change_font', False))
        self.auto_break_lines_var.set(self.config.get('export.slides.auto_break_long_lines', True))
        
        # Slides
        self.add_intro_var.set(self.config.get('export.slides.add_intro_slide', False))
        self.intro_text_var.set(self.config.get('export.slides.intro_slide_text', ''))
        self.intro_group_var.set(self.config.get('export.slides.intro_slide_group', 'Intro'))
        self.add_blank_var.set(self.config.get('export.slides.add_blank_slide', False))
        self.blank_group_var.set(self.config.get('export.slides.blank_slide_group', 'Blank'))
        self.max_lines_var.set(self.config.get('export.slides.max_lines_per_slide', 4))
        
        # Update UI states
        self._toggle_formatting_options()
        self._toggle_intro_options()
        self._toggle_blank_options()
    
    def _save_settings(self):
        """Save settings to config"""
        # General
        output_dir = self.output_dir_var.get()
        if output_dir:
            self.config.set('export.output_directory', output_dir, save=False)
        
        self.config.set('export.include_ccli_in_filename', self.include_ccli_var.get(), save=False)
        self.config.set('export.include_author_in_filename', self.include_author_var.get(), save=False)
        self.config.set('export.overwrite_existing', self.overwrite_var.get(), save=False)
        
        # Formatting
        self.config.set('export.formatting_enabled', self.formatting_enabled_var.get(), save=False)
        self.config.set('export.font.family', self.font_family_var.get(), save=False)
        # Convert font size string to int for config
        try:
            font_size = int(self.font_size_var.get())
        except ValueError:
            font_size = 72  # Default if invalid
        self.config.set('export.font.size', font_size, save=False)
        self.config.set('export.change_font', self.change_font_var.get(), save=False)
        self.config.set('export.slides.auto_break_long_lines', self.auto_break_lines_var.get(), save=False)
        
        # Slides
        self.config.set('export.slides.add_intro_slide', self.add_intro_var.get(), save=False)
        self.config.set('export.slides.intro_slide_text', self.intro_text_var.get(), save=False)
        self.config.set('export.slides.intro_slide_group', self.intro_group_var.get(), save=False)
        self.config.set('export.slides.add_blank_slide', self.add_blank_var.get(), save=False)
        self.config.set('export.slides.blank_slide_group', self.blank_group_var.get(), save=False)
        self.config.set('export.slides.max_lines_per_slide', self.max_lines_var.get(), save=False)
        
        # Save all settings
        self.config.save_settings()
    
    def _save_clicked(self):
        """Handle Save button click - save and close"""
        self._save_settings()
        self.result = 'saved'
        messagebox.showinfo("Settings Saved", "Export settings have been saved successfully.", 
                          parent=self.dialog)
        self.dialog.destroy()
    
    def _apply_clicked(self):
        """Handle Apply button click - save without closing"""
        self._save_settings()
        messagebox.showinfo("Settings Applied", "Export settings have been applied.", 
                          parent=self.dialog)
    
    def _cancel_clicked(self):
        """Handle Cancel button click - close without saving"""
        response = messagebox.askyesno("Confirm Cancel", 
                                      "Are you sure you want to cancel?\nAny unsaved changes will be lost.", 
                                      parent=self.dialog)
        if response:
            self.result = 'cancelled'
            self.dialog.destroy()
    
    def _on_closing(self):
        """Handle window close button"""
        response = messagebox.askyesnocancel("Save Changes", 
                                            "Do you want to save your changes before closing?", 
                                            parent=self.dialog)
        if response is True:  # Yes - save and close
            self._save_settings()
            self.result = 'saved'
            self.dialog.destroy()
        elif response is False:  # No - close without saving
            self.result = 'cancelled'
            self.dialog.destroy()


def show_section_mappings_dialog(parent, config_manager, language_manager=None):
    """
    Show the section mappings dialog
    This is a placeholder that will integrate with the existing SettingsWindow
    
    Args:
        parent: Parent window
        config_manager: ConfigManager instance  
        language_manager: LanguageManager instance (for target language context)
    """
    try:
        # Import here to avoid circular imports
        from src.gui.settings_window import SettingsWindow
        
        # Create settings window for section mappings
        settings_window = SettingsWindow(parent)
        
        # If we have a language manager with non-English target, 
        # we could customize the editor here in the future
        if language_manager and language_manager.target_language != 'english':
            # Future enhancement: customize for target language
            pass
            
        # Settings window handles its own modal behavior
        return True
        
    except Exception as e:
        from tkinter import messagebox
        messagebox.showerror("Error", f"Failed to open section mappings editor: {e}")
        return False