#!/usr/bin/env python3
"""
Check export status and help diagnose issues
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pathlib import Path
import glob

def check_export_status():
    print("=== Export Status Checker ===")
    print()
    
    # Check common export locations
    possible_locations = [
        Path.home() / "Desktop" / "ProPresenter_Export",
        Path.home() / "Desktop" / "ProPresenter_Export_Test", 
        Path.home() / "Desktop" / "ProPresenter_Mock_Export",
        Path.home() / "Downloads",
        Path.home() / "Documents",
        Path("./"),  # Current directory
        Path("./debug_export_test"),
        Path("./test_export")
    ]
    
    print("Checking for .pro6 files in common locations:")
    print("-" * 50)
    
    found_files = []
    
    for location in possible_locations:
        if location.exists():
            pro6_files = list(location.glob("*.pro6"))
            if pro6_files:
                print(f"[FOUND] {len(pro6_files)} .pro6 files in: {location}")
                for file in pro6_files:
                    size = file.stat().st_size
                    modified = file.stat().st_mtime
                    import datetime
                    mod_time = datetime.datetime.fromtimestamp(modified).strftime('%Y-%m-%d %H:%M:%S')
                    print(f"  - {file.name} ({size} bytes, modified: {mod_time})")
                    found_files.extend(pro6_files)
            else:
                print(f"  No .pro6 files in: {location}")
        else:
            print(f"  Directory doesn't exist: {location}")
    
    print()
    print(f"Total .pro6 files found: {len(found_files)}")
    
    if found_files:
        print()
        print("Recent .pro6 files (last 5):")
        print("-" * 30)
        # Sort by modification time, newest first
        recent_files = sorted(found_files, key=lambda x: x.stat().st_mtime, reverse=True)[:5]
        for file in recent_files:
            size = file.stat().st_size
            modified = file.stat().st_mtime
            mod_time = datetime.datetime.fromtimestamp(modified).strftime('%Y-%m-%d %H:%M:%S')
            print(f"  {file} ({size} bytes, {mod_time})")
    
    print()
    print("=== Diagnostic Information ===")
    print(f"Current working directory: {Path.cwd()}")
    print(f"User home directory: {Path.home()}")
    print(f"Desktop path: {Path.home() / 'Desktop'}")
    print(f"Desktop exists: {(Path.home() / 'Desktop').exists()}")
    
    # Check if Desktop/ProPresenter_Export exists
    default_export = Path.home() / "Desktop" / "ProPresenter_Export"
    print(f"Default export directory: {default_export}")
    print(f"Default export dir exists: {default_export.exists()}")
    
    if default_export.exists():
        all_files = list(default_export.glob("*"))
        print(f"Files in default export directory: {len(all_files)}")
        for file in all_files[:10]:  # Show first 10 files
            print(f"  - {file.name}")
        if len(all_files) > 10:
            print(f"  ... and {len(all_files) - 10} more files")
    
    print()
    print("=== Troubleshooting Tips ===")
    print("1. Make sure you have selected songs (checked the boxes) in the GUI")
    print("2. Check the 'Output Path' field in the GUI - files are saved there")
    print("3. Look for .pro6 files in the locations listed above")
    print("4. If the export says 'successful' but you can't find files, try:")
    print("   - Check if the output directory has write permissions")
    print("   - Try changing the output path to your Desktop")
    print("   - Run the application as administrator if needed")
    
    return found_files

if __name__ == "__main__":
    import datetime
    check_export_status()