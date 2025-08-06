#!/usr/bin/env python3
"""
Test the GUI export process without the GUI
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pathlib import Path
from src.database.easyworship import EasyWorshipDatabase
from src.export.propresenter import ProPresenterExporter

def test_gui_export_process():
    print("=== GUI Export Process Test ===")
    
    # Try to connect to a database like the GUI would
    possible_db_paths = [
        Path('C:\\Claud\\ewtest\\orginaldb'),
        Path('C:\\Users\\Public\\Documents\\Softouch\\EasyWorship\\Default\\Databases\\Data'),
        Path('C:\\ProgramData\\Softouch\\EasyWorship\\Default\\Databases\\Data')
    ]
    
    db = None
    db_path = None
    
    for path in possible_db_paths:
        if path.exists() and (path / 'Songs.db').exists():
            print(f"Found database at: {path}")
            db_path = path
            try:
                db = EasyWorshipDatabase(str(path))
                if db.validate_database():
                    print(f"Database validation successful")
                    break
                else:
                    print(f"Database validation failed")
            except Exception as e:
                print(f"Error connecting to database: {e}")
    
    if not db:
        print("No valid database found. Creating mock data for testing...")
        # Create a minimal test that doesn't require database
        test_gui_export_without_db()
        return
    
    try:
        # Get songs like the GUI would
        songs_data = db.get_all_songs()
        print(f"Loaded {len(songs_data)} songs from database")
        
        if not songs_data:
            print("No songs found in database")
            return
            
        # Simulate selecting first few songs
        selected_songs = {song['rowid'] for song in songs_data[:3]}  # Select first 3 songs
        print(f"Simulating selection of songs: {selected_songs}")
        
        # Simulate the GUI export worker process
        songs_to_export = []
        for song_data in songs_data:
            if song_data['rowid'] in selected_songs:
                print(f"Processing song: {song_data['title']} (ID: {song_data['rowid']})")
                
                # Get processed lyrics with sections
                processed = db.get_song_with_processed_lyrics(song_data['rowid'])
                print(f"Processed result: {type(processed)}")
                
                if processed and processed.get('sections'):
                    sections = processed['sections']
                    print(f"Found {len(sections)} sections")
                    for i, section in enumerate(sections, 1):
                        print(f"  Section {i}: {section['type']} - {len(section['content'])} chars")
                    songs_to_export.append((song_data, sections))
                else:
                    print(f"No sections found, using fallback")
                    empty_sections = [{'type': 'verse', 'content': 'No lyrics available'}]
                    songs_to_export.append((song_data, empty_sections))
        
        print(f"Total songs to export: {len(songs_to_export)}")
        
        # Test export
        output_dir = Path.home() / "Desktop" / "ProPresenter_Export_Test"
        print(f"Output directory: {output_dir}")
        
        exporter = ProPresenterExporter()
        
        def progress_callback(current, total, title):
            print(f"Progress: {current + 1}/{total} - {title}")
        
        successful, failed = exporter.export_songs_batch(
            songs_to_export, 
            output_dir, 
            progress_callback=progress_callback
        )
        
        print(f"Export completed:")
        print(f"  Successful: {len(successful)}")
        print(f"  Failed: {len(failed)}")
        
        if successful:
            print("Successfully exported files:")
            for file_path in successful:
                file_obj = Path(file_path)
                print(f"  - {file_path} (exists: {file_obj.exists()}, size: {file_obj.stat().st_size if file_obj.exists() else 'N/A'})")
        
        if failed:
            print("Failed exports:")
            for error in failed:
                print(f"  - {error}")
                
    except Exception as e:
        print(f"Error during test: {e}")
        import traceback
        traceback.print_exc()

def test_gui_export_without_db():
    """Test export process without requiring a database"""
    print("\n=== Mock Database Export Test ===")
    
    # Create mock song data
    mock_songs = [
        {
            'rowid': 1,
            'title': 'Mock Song 1',
            'author': 'Test Author',
            'copyright': 'Test Copyright',
            'administrator': '',
            'reference_number': '123',
            'tags': '',
            'description': ''
        },
        {
            'rowid': 2, 
            'title': 'Mock Song 2',
            'author': 'Another Author',
            'copyright': '',
            'administrator': '',
            'reference_number': '',
            'tags': 'test',
            'description': 'Test song'
        }
    ]
    
    # Mock sections
    mock_sections = [
        [
            {'type': 'verse', 'content': 'First verse content\nSecond line of first verse'},
            {'type': 'chorus', 'content': 'Chorus content\nSecond line of chorus'}
        ],
        [
            {'type': 'verse', 'content': 'Different verse\nAnother line'},
            {'type': 'bridge', 'content': 'Bridge section\nBridge line two'}
        ]
    ]
    
    # Simulate the export process
    songs_to_export = list(zip(mock_songs, mock_sections))
    output_dir = Path.home() / "Desktop" / "ProPresenter_Mock_Export"
    
    print(f"Mock songs to export: {len(songs_to_export)}")
    print(f"Output directory: {output_dir}")
    
    exporter = ProPresenterExporter()
    
    def progress_callback(current, total, title):
        print(f"Progress: {current + 1}/{total} - {title}")
    
    successful, failed = exporter.export_songs_batch(
        songs_to_export,
        output_dir,
        progress_callback=progress_callback
    )
    
    print(f"Mock export completed:")
    print(f"  Successful: {len(successful)}")
    print(f"  Failed: {len(failed)}")
    
    if successful:
        print("Successfully exported files:")
        for file_path in successful:
            file_obj = Path(file_path)
            exists = file_obj.exists()
            size = file_obj.stat().st_size if exists else 0
            print(f"  - {file_path}")
            print(f"    Exists: {exists}, Size: {size} bytes")
            
            if exists:
                # Verify it's valid XML
                try:
                    with open(file_obj, 'r', encoding='utf-8') as f:
                        content = f.read()
                    print(f"    XML starts with: {content[:100]}...")
                    print(f"    Contains ProPresenter: {'RVPresentationDocument' in content}")
                except Exception as e:
                    print(f"    Error reading file: {e}")
    
    if failed:
        print("Failed exports:")
        for error in failed:
            print(f"  - {error}")

if __name__ == "__main__":
    test_gui_export_process()