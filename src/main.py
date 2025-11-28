#!/usr/bin/env python3
"""
EasyWorship to ProPresenter Converter
Main entry point
"""

import sys
import os
import logging
from pathlib import Path

# Add parent directory to path for imports
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from src.version import SECTION_MAPPINGS_SCHEMA_VERSION
from src.utils.config import get_app_data_dir


def initialize_application():
    """Initialize application directories and configuration"""
    # Determine if running as frozen executable or script
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        application_path = os.path.dirname(sys.executable)
    else:
        # Running as script
        application_path = os.path.dirname(os.path.abspath(__file__))

    # Get app data directory using centralized cross-platform function
    app_data_dir = get_app_data_dir()

    # Create logs directory
    logs_dir = app_data_dir / 'logs'
    logs_dir.mkdir(exist_ok=True)

    # Setup basic logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(logs_dir / 'ewexport.log'),
            logging.StreamHandler()
        ]
    )

    logger = logging.getLogger(__name__)
    logger.info(f"Application initialized. Running from: {application_path}")
    logger.info(f"Configuration directory: {app_data_dir}")

    # Ensure default section mappings exist in app data directory
    section_mappings_file = app_data_dir / 'section_mappings.json'
    if not section_mappings_file.exists():
        import json
        # Complete mappings for both English and Swedish source labels
        # Note: File is written with UTF-8 encoding for cross-platform compatibility
        default_mappings = {
            "version": SECTION_MAPPINGS_SCHEMA_VERSION,
            "section_mappings": {
                # Swedish source labels
                "vers": "Verse",
                "refräng": "Chorus",
                "brygga": "Bridge",
                "förrefräng": "Pre-Chorus",
                "slut": "Outro",
                # English source labels
                "verse": "Verse",
                "chorus": "Chorus",
                "bridge": "Bridge",
                "pre-chorus": "Pre-Chorus",
                "prechorus": "Pre-Chorus",
                "intro": "Intro",
                "outro": "Outro",
                "tag": "Tag",
                "ending": "Ending"
            },
            "number_mapping_rules": {
                "preserve_numbers": True,
                "start_from_one": True,
                "format": "{section_name} {number}"
            },
            "gui_settings": {
                "editable_via_gui": True,
                "description": "Section name mappings from Swedish/English to English for ProPresenter export"
            },
            "notes": [
                "This file maps Swedish and English section names to English equivalents",
                "Numbers are preserved: 'vers 1' becomes 'Verse 1'",
                "Case-insensitive matching is applied",
                "These mappings can be edited from Edit -> Section Mappings in the GUI"
            ]
        }
        with open(section_mappings_file, 'w', encoding='utf-8') as f:
            json.dump(default_mappings, f, indent=2, ensure_ascii=False)
        logger.info("Created default section_mappings.json in app data directory")

from src.gui.main_window import MainWindow

def main():
    # Initialize application environment
    initialize_application()
    
    # Start the GUI
    app = MainWindow()
    app.run()

if __name__ == "__main__":
    main()