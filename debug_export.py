#!/usr/bin/env python3
"""
Debug the export functionality
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pathlib import Path
from src.export.propresenter import ProPresenterExporter
import tempfile

def debug_export():
    print("=== Export Debug Test ===")
    
    # Create a simple test song
    test_song = {
        'rowid': 1,
        'title': 'Debug Test Song',
        'author': 'Test Author',
        'copyright': 'Test Copyright',
        'administrator': '',
        'reference_number': '12345',
        'tags': '',
        'description': ''
    }
    
    test_sections = [
        {'type': 'verse', 'content': 'Test verse content\nSecond line of verse'},
        {'type': 'chorus', 'content': 'Test chorus content\nSecond line of chorus'}
    ]
    
    # Test with different output paths
    test_paths = [
        Path.home() / "Desktop" / "ProPresenter_Export",  # Default path
        Path("./debug_export_test"),  # Local path
        Path(tempfile.gettempdir()) / "ewexport_test"  # Temp directory
    ]
    
    exporter = ProPresenterExporter()
    
    for i, output_path in enumerate(test_paths, 1):
        print(f"\n--- Test {i}: {output_path} ---")
        
        try:
            # Check if directory exists/can be created
            print(f"Output path exists: {output_path.exists()}")
            print(f"Parent directory exists: {output_path.parent.exists()}")
            
            # Try to create directory
            print(f"Creating output directory...")
            output_path.mkdir(parents=True, exist_ok=True)
            print(f"Directory created successfully: {output_path.exists()}")
            
            # Test export
            print(f"Attempting export...")
            success, result = exporter.export_song(test_song, test_sections, output_path)
            
            print(f"Export success: {success}")
            print(f"Export result: {result}")
            
            if success:
                # Check if file actually exists
                expected_file = Path(result)
                print(f"Expected file path: {expected_file}")
                print(f"File exists: {expected_file.exists()}")
                
                if expected_file.exists():
                    file_size = expected_file.stat().st_size
                    print(f"File size: {file_size} bytes")
                    
                    # Try to read the file
                    try:
                        with open(expected_file, 'r', encoding='utf-8') as f:
                            content = f.read()[:200]
                        print(f"File content preview: {content}...")
                        print(f"SUCCESS: File created and readable")
                    except Exception as e:
                        print(f"ERROR reading file: {e}")
                else:
                    print(f"ERROR: File does not exist despite success report")
                    
                    # List directory contents
                    try:
                        files = list(output_path.glob("*"))
                        print(f"Files in output directory: {files}")
                    except Exception as e:
                        print(f"Error listing directory: {e}")
            else:
                print(f"ERROR: Export failed - {result}")
                
        except Exception as e:
            print(f"ERROR: Exception during test - {e}")
            import traceback
            traceback.print_exc()
    
    print("\n=== Debug Complete ===")

if __name__ == "__main__":
    debug_export()