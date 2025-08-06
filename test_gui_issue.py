#!/usr/bin/env python3
"""
Test GUI data handling issue
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pathlib import Path
from src.database.easyworship import EasyWorshipDatabase

def test_gui_data_issue():
    print("=== GUI Data Issue Test ===")
    
    # Try to connect to the database like GUI does
    db_paths = [
        Path('C:\\Claud\\ewtest\\orginaldb'),
        Path('C:\\Users\\Public\\Documents\\Softouch\\EasyWorship\\Default\\Databases\\Data'),
    ]
    
    db = None
    for db_path in db_paths:
        if db_path.exists() and (db_path / 'Songs.db').exists():
            print(f"Found database at: {db_path}")
            try:
                db = EasyWorshipDatabase(str(db_path))
                if db.validate_database():
                    print("Database validation successful")
                    break
            except Exception as e:
                print(f"Error with database: {e}")
    
    if not db:
        print("No database found!")
        return
    
    # Test the data loading like GUI does
    try:
        print("\n1. Loading all songs like GUI...")
        songs_data = db.get_all_songs()
        print(f"Loaded {len(songs_data)} songs")
        
        if songs_data:
            first_song = songs_data[0]
            print(f"First song: {first_song['title']} (ID: {first_song['rowid']})")
            print(f"First song keys: {list(first_song.keys())}")
            
            # Test processed lyrics like GUI does
            print(f"\n2. Testing processed lyrics for first song...")
            try:
                processed = db.get_song_with_processed_lyrics(first_song['rowid'])
                print(f"Processed type: {type(processed)}")
                
                if processed:
                    print(f"Processed keys: {list(processed.keys()) if isinstance(processed, dict) else 'Not a dict'}")
                    
                    if isinstance(processed, dict) and 'sections' in processed:
                        sections = processed['sections']
                        print(f"Sections type: {type(sections)}")
                        print(f"Number of sections: {len(sections) if sections else 0}")
                        
                        if sections:
                            print(f"First section: {sections[0]}")
                    else:
                        print("No 'sections' key in processed result")
                else:
                    print("Processed result is None or empty")
                    
            except Exception as e:
                print(f"Error getting processed lyrics: {e}")
                import traceback
                traceback.print_exc()
        
        # Test with a specific song that has lyrics
        print(f"\n3. Testing with song that should have lyrics...")
        target_song = None
        for song in songs_data[:10]:  # Check first 10
            if 'reason' in song['title'].lower() or '000' in song['title']:  # Find "10 000 reasons"
                target_song = song
                break
        
        if target_song:
            print(f"Testing song: {target_song['title']} (ID: {target_song['rowid']})")
            try:
                processed = db.get_song_with_processed_lyrics(target_song['rowid'])
                print(f"Processed result: {type(processed)}")
                
                if processed and isinstance(processed, dict) and 'sections' in processed:
                    sections = processed['sections']
                    print(f"Found {len(sections)} sections")
                    for i, section in enumerate(sections[:3], 1):  # Show first 3
                        print(f"  Section {i}: {section['type']} - {len(section['content'])} chars")
                        print(f"    Preview: {section['content'][:50]}...")
                else:
                    print("No valid sections found")
            except Exception as e:
                print(f"Error processing target song: {e}")
                import traceback
                traceback.print_exc()
        
    except Exception as e:
        print(f"Error during test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_gui_data_issue()