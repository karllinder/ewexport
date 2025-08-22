"""
Language Settings Dialog for multi-language section mapping configuration
"""

import tkinter as tk
from tkinter import ttk, messagebox
import logging
from typing import Dict, List, Optional
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from processing.language_manager import LanguageManager

logger = logging.getLogger(__name__)


class LanguageDialog:
    """Dialog for configuring language settings"""
    
    def __init__(self, parent, config_manager, current_settings: Optional[Dict] = None):
        """
        Initialize language settings dialog
        
        Args:
            parent: Parent window
            config_manager: ConfigManager instance
            current_settings: Current language settings (optional)
        """
        self.parent = parent
        self.config_manager = config_manager
        self.language_manager = LanguageManager()
        self.result = None
        
        # Current settings or defaults
        if current_settings:
            self.language_manager.import_config(current_settings)
        else:
            # Use defaults
            self.language_manager.set_source_languages(['swedish', 'english'])
            self.language_manager.set_target_language('english')
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Language Settings")
        self.dialog.geometry("600x500")
        self.dialog.resizable(False, False)
        
        # Make modal
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center on parent
        self._center_dialog()
        
        # Create UI
        self._create_widgets()
        
        # Handle close
        self.dialog.protocol("WM_DELETE_WINDOW", self._on_cancel)
        
    def _center_dialog(self):
        """Center dialog on parent window"""
        self.dialog.update_idletasks()
        
        # Get parent position and size
        parent_x = self.parent.winfo_rootx()
        parent_y = self.parent.winfo_rooty()
        parent_w = self.parent.winfo_width()
        parent_h = self.parent.winfo_height()
        
        # Calculate position
        x = parent_x + (parent_w // 2) - (600 // 2)
        y = parent_y + (parent_h // 2) - (500 // 2)
        
        self.dialog.geometry(f"600x500+{x}+{y}")
        
    def _create_widgets(self):
        """Create dialog widgets"""
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Configure grid
        self.dialog.grid_rowconfigure(0, weight=1)
        self.dialog.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(2, weight=1)  # Make source languages area expandable
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Multi-Language Settings", 
                               font=('TkDefaultFont', 12, 'bold'))
        title_label.grid(row=0, column=0, sticky="w", pady=(0, 20))
        
        # Source languages section
        self._create_source_section(main_frame, row=1)
        
        # Target language section  
        self._create_target_section(main_frame, row=3)
        
        # Buttons
        self._create_buttons(main_frame, row=5)
        
    def _create_source_section(self, parent, row):
        """Create source languages selection section"""
        # Source languages label
        source_label = ttk.Label(parent, text="SOURCE Languages (in your database):",
                                font=('TkDefaultFont', 10, 'bold'))
        source_label.grid(row=row, column=0, sticky="w", pady=(0, 10))
        
        # Source languages frame with scrollbar
        source_frame = ttk.Frame(parent)
        source_frame.grid(row=row+1, column=0, sticky="ew", pady=(0, 20))
        source_frame.grid_columnconfigure(0, weight=1)
        
        # Create checkboxes for source languages
        self.source_vars = {}
        available_sources = self.language_manager.get_available_source_languages()
        current_sources = self.language_manager.source_languages
        
        # Language descriptions
        lang_descriptions = {
            'swedish': 'Swedish (vers, refräng, brygga, förrefräng)',
            'english': 'English (verse, chorus, bridge, pre-chorus)', 
            'german': 'German (strophe, refrain, brücke, vorrefrain)',
            'french': 'French (couplet, refrain, pont, pré-refrain)',
            'spanish': 'Spanish (verso, coro, puente, pre-coro)',
            'norwegian': 'Norwegian (vers, refreng, bro)',
            'danish': 'Danish (vers, omkvæd, bro)'
        }
        
        for i, lang in enumerate(available_sources):
            var = tk.BooleanVar()
            var.set(lang in current_sources)
            self.source_vars[lang] = var
            
            description = lang_descriptions.get(lang, lang.title())
            checkbox = ttk.Checkbutton(source_frame, text=description, variable=var)
            checkbox.grid(row=i, column=0, sticky="w", pady=2)
            
    def _create_target_section(self, parent, row):
        """Create target language selection section"""
        target_frame = ttk.Frame(parent)
        target_frame.grid(row=row, column=0, sticky="ew", pady=(0, 20))
        target_frame.grid_columnconfigure(1, weight=1)
        
        # Target language label
        target_label = ttk.Label(target_frame, text="TARGET Language (export to):",
                                font=('TkDefaultFont', 10, 'bold'))
        target_label.grid(row=0, column=0, sticky="w", pady=(0, 10), columnspan=2)
        
        # Target language dropdown
        self.target_var = tk.StringVar()
        self.target_var.set(self.language_manager.target_language)
        
        available_targets = self.language_manager.get_available_target_languages()
        target_combo = ttk.Combobox(target_frame, textvariable=self.target_var,
                                   values=available_targets, state="readonly", width=20)
        target_combo.grid(row=1, column=0, sticky="w")
        target_combo.bind('<<ComboboxSelected>>', self._on_target_changed)
        
        # Load default mappings button
        self.auto_button = ttk.Button(target_frame, text="Load Default Mappings",
                                     command=self._load_default_mappings)
        self.auto_button.grid(row=1, column=1, sticky="w", padx=(20, 0))
        
        # Note about non-English targets
        note_text = ("Note: When target is not English, use the\n"
                    "Section Mappings editor to configure mappings manually.")
        note_label = ttk.Label(target_frame, text=note_text, 
                              foreground="gray", font=('TkDefaultFont', 8))
        note_label.grid(row=2, column=0, columnspan=2, sticky="w", pady=(10, 0))
        
        # Button to open section mappings editor
        self.mappings_button = ttk.Button(target_frame, text="Open Section Mappings Editor",
                                         command=self._open_mappings_editor)
        self.mappings_button.grid(row=3, column=0, sticky="w", pady=(10, 0))
        
        # Update button states based on current target
        self._update_target_ui()
        
    def _create_buttons(self, parent, row):
        """Create OK/Cancel buttons"""
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=row, column=0, sticky="ew", pady=(20, 0))
        
        # Right-align buttons
        button_frame.grid_columnconfigure(0, weight=1)
        
        cancel_button = ttk.Button(button_frame, text="Cancel", command=self._on_cancel)
        cancel_button.grid(row=0, column=1, padx=(0, 10))
        
        ok_button = ttk.Button(button_frame, text="OK", command=self._on_ok)
        ok_button.grid(row=0, column=2)
        
    def _on_target_changed(self, event=None):
        """Handle target language change"""
        self._update_target_ui()
        
    def _update_target_ui(self):
        """Update UI based on target language selection"""
        target = self.target_var.get()
        is_english = target == 'english'
        
        # Enable/disable load default mappings button
        if is_english:
            self.auto_button.config(state='normal')
        else:
            self.auto_button.config(state='disabled')
            
    def _load_default_mappings(self):
        """Load default mappings for English target"""
        try:
            # Get selected source languages
            selected_sources = [lang for lang, var in self.source_vars.items() if var.get()]
            
            if not selected_sources:
                messagebox.showwarning("No Languages Selected", 
                                     "Please select at least one source language first.")
                return
                
            # Check if mappings already exist
            existing_mappings = self._get_existing_mappings()
            if existing_mappings:
                result = messagebox.askyesno("Existing Mappings Found",
                                           f"Found {len(existing_mappings)} existing section mappings.\n\n"
                                           "Loading default mappings will overwrite these existing mappings.\n\n"
                                           "Do you want to continue?")
                if not result:
                    return
                
            # Update language manager
            self.language_manager.set_source_languages(selected_sources)
            self.language_manager.set_target_language('english')
            
            # Load default mappings
            mappings = self.language_manager.auto_populate_mappings()
            
            if mappings:
                messagebox.showinfo("Default Mappings Loaded", 
                                  f"Loaded {len(mappings)} default section mappings for selected languages.\n\n"
                                  f"Languages: {', '.join(selected_sources)}")
            else:
                messagebox.showinfo("No Mappings", 
                                  "No default mappings could be loaded.")
                                  
        except Exception as e:
            logger.error(f"Error loading default mappings: {e}")
            messagebox.showerror("Error", f"Failed to load default mappings: {e}")
    
    def _get_existing_mappings(self):
        """Get existing section mappings from config"""
        try:
            if not self.config_manager:
                return {}
                
            # Check current language manager mappings
            current_mappings = getattr(self.language_manager, 'active_mappings', {})
            if current_mappings:
                return current_mappings
                
            # Check config file for existing section mappings
            import json
            from pathlib import Path
            import os
            
            # Get section mappings file path
            app_data = os.environ.get('APPDATA', Path.home() / 'AppData' / 'Roaming')
            app_dir = Path(app_data) / 'EWExport'
            mappings_file = app_dir / "section_mappings.json"
            
            if mappings_file.exists():
                with open(mappings_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get('section_mappings', {})
                    
            return {}
            
        except Exception as e:
            logger.error(f"Error getting existing mappings: {e}")
            return {}
            
    def _open_mappings_editor(self):
        """Open the section mappings editor"""
        try:
            # Import here to avoid circular imports
            from src.gui.dialogs import show_section_mappings_dialog
            
            # Get current settings
            selected_sources = [lang for lang, var in self.source_vars.items() if var.get()]
            target = self.target_var.get()
            
            if not selected_sources:
                messagebox.showwarning("No Languages Selected",
                                     "Please select at least one source language first.")
                return
                
            # Update language manager
            self.language_manager.set_source_languages(selected_sources) 
            self.language_manager.set_target_language(target)
            
            # Show mappings editor
            show_section_mappings_dialog(self.dialog, self.config_manager, 
                                       self.language_manager)
            
        except Exception as e:
            logger.error(f"Error opening mappings editor: {e}")
            messagebox.showerror("Error", f"Failed to open mappings editor: {e}")
            
    def _validate_settings(self) -> bool:
        """Validate current settings"""
        # Get selected source languages
        selected_sources = [lang for lang, var in self.source_vars.items() if var.get()]
        
        if not selected_sources:
            messagebox.showerror("Invalid Settings", 
                               "Please select at least one source language.")
            return False
            
        target = self.target_var.get()
        if not target:
            messagebox.showerror("Invalid Settings", 
                               "Please select a target language.")
            return False
            
        # Update language manager for validation
        self.language_manager.set_source_languages(selected_sources)
        self.language_manager.set_target_language(target)
        
        # Validate
        issues = self.language_manager.validate_mappings()
        if issues:
            # For non-English targets without mappings, just warn
            if target != 'english' and 'Non-English target requires manual mappings' in issues:
                result = messagebox.askyesno("Manual Mappings Required",
                                           f"Target language '{target}' requires manual mappings.\n\n"
                                           "You can configure these in the Section Mappings editor.\n"
                                           "Continue anyway?")
                return result
            else:
                messagebox.showerror("Validation Failed", "\n".join(issues))
                return False
                
        return True
        
    def _on_ok(self):
        """Handle OK button click"""
        if not self._validate_settings():
            return
            
        # Get final settings
        selected_sources = [lang for lang, var in self.source_vars.items() if var.get()]
        target = self.target_var.get()
        
        # Update language manager
        self.language_manager.set_source_languages(selected_sources)
        self.language_manager.set_target_language(target)
        
        # Load default mappings for English targets
        if target == 'english':
            self.language_manager.auto_populate_mappings()
            
        # Export result
        self.result = self.language_manager.export_config()
        
        logger.info(f"Language settings configured: {len(selected_sources)} sources, target: {target}")
        self.dialog.destroy()
        
    def _on_cancel(self):
        """Handle Cancel button click"""
        self.result = None
        self.dialog.destroy()
        
    def show(self) -> Optional[Dict]:
        """
        Show dialog and return result
        
        Returns:
            Language configuration dict or None if cancelled
        """
        self.dialog.wait_window()
        return self.result


def show_language_settings_dialog(parent, config_manager, current_settings=None):
    """
    Show language settings dialog
    
    Args:
        parent: Parent window
        config_manager: ConfigManager instance
        current_settings: Current language settings (optional)
        
    Returns:
        Language configuration dict or None if cancelled
    """
    dialog = LanguageDialog(parent, config_manager, current_settings)
    return dialog.show()


if __name__ == '__main__':
    # Test the dialog standalone
    root = tk.Tk()
    root.title("Test Language Dialog")
    root.geometry("300x200")
    
    def test_dialog():
        result = show_language_settings_dialog(root, None)
        print(f"Result: {result}")
    
    ttk.Button(root, text="Open Language Dialog", command=test_dialog).pack(pady=50)
    root.mainloop()