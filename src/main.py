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

def initialize_application():
    """Initialize application directories and configuration"""
    # Determine if running as frozen executable or script
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        application_path = os.path.dirname(sys.executable)
    else:
        # Running as script
        application_path = os.path.dirname(os.path.abspath(__file__))
    
    # Ensure required directories exist
    app_data_dir = Path(os.environ.get('APPDATA', Path.home() / 'AppData' / 'Roaming')) / 'EWExport'
    app_data_dir.mkdir(parents=True, exist_ok=True)
    
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
    
    # Ensure default section mappings exist in APPDATA
    section_mappings_file = app_data_dir / 'section_mappings.json'
    if not section_mappings_file.exists():
        import json
        default_mappings = {
            "version": "1.2.4",
            "section_mappings": {
                "vers": "Verse",
                "refräng": "Chorus",
                "refrÃ¤ng": "Chorus",
                "brygga": "Bridge",
                "stick": "Bridge",
                "pre-chorus": "Pre-Chorus",
                "förrefräng": "Pre-Chorus",
                "fÃ¶rrefrÃ¤ng": "Pre-Chorus",
                "outro": "Outro",
                "slut": "Outro"
            },
            "number_mapping_rules": {
                "preserve_numbers": True,
                "format": "{section_name} {number}"
            }
        }
        with open(section_mappings_file, 'w', encoding='utf-8') as f:
            json.dump(default_mappings, f, indent=2, ensure_ascii=False)
        logger.info("Created default section_mappings.json in APPDATA")

from src.gui.main_window import MainWindow

def main():
    # Initialize application environment
    initialize_application()
    
    # Start the GUI
    app = MainWindow()
    app.run()

if __name__ == "__main__":
    main()