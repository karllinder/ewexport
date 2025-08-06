# -*- coding: utf-8 -*-
"""
RTF Processing Demo

This script demonstrates how to use the RTF processing modules
to parse EasyWorship RTF content, detect sections, and clean text.
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from processing import parse_rtf, detect_sections, clean_text
from database.easyworship import EasyWorshipDatabase

def demo_rtf_processing():
    """Demonstrate RTF processing with Swedish content."""
    
    print("=" * 60)
    print("EasyWorship RTF Processing Demo")
    print("=" * 60)
    
    # Sample RTF content with Swedish characters
    sample_rtf = r"""{{\rtf1\ansi\deff0 {\fonttbl {\f0 Times New Roman;}}
verse\par
Djupt inne i hj\u228?rtat\par
det finns en eld som aldrig sl\u246?cknar\par
\par
chorus\par
Abba F\u229?der\par
L\u180?t mig f\u229? se vem Du \u228?r\par
Visa mig din h\u228?rlighet\par
\par
verse\par
Anden fl\u246?dar genom mitt sinne\par
och fyller mitt hj\u228?rta med k\u228?rlek\par
N\u229?r jag s\u229?nger ditt heliga namn}"""
    
    print("\n1. Original RTF Content:")
    print("-" * 30)
    print(sample_rtf[:200] + "..." if len(sample_rtf) > 200 else sample_rtf)
    
    # Step 1: Parse RTF
    print("\n2. Parsing RTF Content...")
    print("-" * 30)
    parsed_rtf = parse_rtf(sample_rtf)
    
    if parsed_rtf:
        print(f"[OK] Successfully parsed RTF")
        print(f"[OK] Has content: {parsed_rtf['has_content']}")
        print(f"[OK] Number of lines: {len(parsed_rtf['lines'])}")
        print("\nParsed text:")
        print(parsed_rtf['plain_text'])
    else:
        print("[ERROR] Failed to parse RTF")
        return
    
    # Step 2: Clean text
    print("\n3. Cleaning Text...")
    print("-" * 30)
    cleaned_text = clean_text(parsed_rtf['plain_text'], for_song=True)
    print(f"[OK] Text cleaned")
    print("Cleaned text:")
    print(cleaned_text)
    
    # Step 3: Detect sections
    print("\n4. Detecting Sections...")
    print("-" * 30)
    section_data = detect_sections(cleaned_text)
    
    print(f"[OK] Sections detected: {section_data['has_sections']}")
    print(f"[OK] Number of sections: {len(section_data['sections'])}")
    
    for i, section in enumerate(section_data['sections'], 1):
        print(f"\nSection {i} - Type: {section['type'].upper()}")
        print("-" * 20)
        print(section['content'])
    
    # Step 4: Demonstrate with advanced detection
    print("\n5. Advanced Section Detection...")
    print("-" * 30)
    
    # Sample text without explicit markers
    text_without_markers = """Vi sjunger lovsånger till dig
Herre du är vår räddning
Du är vår tillflykt

Vi sjunger lovsånger till dig
Herre du är vår räddning
Du är vår tillflykt

Ditt namn är högt över alla namn
Inget kan jämföras med dig
Du är kung över alla kungar

Vi sjunger lovsånger till dig
Herre du är vår räddning
Du är vår tillflykt"""
    
    advanced_sections = detect_sections(text_without_markers, advanced=True)
    print(f"[OK] Advanced detection found {len(advanced_sections['sections'])} sections")
    
    for i, section in enumerate(advanced_sections['sections'], 1):
        print(f"\nAdvanced Section {i} - Type: {section['type'].upper()}")
        print("-" * 25)
        print(section['content'][:100] + "..." if len(section['content']) > 100 else section['content'])


def demo_database_integration():
    """Demonstrate database integration (if database files exist)."""
    
    print("\n" + "=" * 60)
    print("Database Integration Demo")
    print("=" * 60)
    
    # Look for EasyWorship database in common locations
    common_paths = [
        Path("C:/Users/Public/Documents/Softouch/EasyWorship 6/Databases/Data"),
        Path("C:/Users/Public/Documents/Softouch/EasyWorship/Databases/Data"),
        Path.cwd() / "test_data"  # Local test data if available
    ]
    
    db_path = None
    for path in common_paths:
        if path.exists() and (path / "Songs.db").exists() and (path / "SongWords.db").exists():
            db_path = path
            break
    
    if not db_path:
        print("[INFO] No EasyWorship database found in common locations")
        print("  Expected locations:")
        for path in common_paths:
            print(f"    - {path}")
        print("\n  To test database integration, ensure Songs.db and SongWords.db exist")
        return
    
    print(f"[OK] Found EasyWorship database at: {db_path}")
    
    try:
        db = EasyWorshipDatabase(str(db_path))
        
        if not db.validate_database():
            print("[ERROR] Database validation failed")
            return
        
        print("[OK] Database validation successful")
        
        # Get song count
        song_count = db.get_song_count()
        print(f"[OK] Total songs in database: {song_count}")
        
        if song_count > 0:
            # Get first few songs
            songs = db.get_all_songs()[:3]  # Just first 3 for demo
            
            for i, song in enumerate(songs, 1):
                print(f"\nSong {i}: {song['title']}")
                print(f"  Author: {song['author'] or 'Unknown'}")
                print(f"  Copyright: {song['copyright'] or 'N/A'}")
                
                # Get processed lyrics for first song only
                if i == 1:
                    processed = db.get_song_with_processed_lyrics(song['rowid'])
                    if processed and processed.get('sections'):
                        print(f"  Sections: {len(processed['sections'])}")
                        for section in processed['sections'][:2]:  # Show first 2 sections
                            content_preview = section['content'][:50].replace('\n', ' ')
                            print(f"    - {section['type']}: {content_preview}...")
                    else:
                        print("  No lyrics or sections found")
        
    except Exception as e:
        print(f"[ERROR] Database error: {e}")


if __name__ == "__main__":
    demo_rtf_processing()
    demo_database_integration()
    
    print("\n" + "=" * 60)
    print("Demo Complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("- The RTF processing modules are ready for integration")
    print("- Use parse_rtf() to convert RTF to plain text") 
    print("- Use detect_sections() to identify song structure")
    print("- Use clean_text() to normalize and clean text")
    print("- Use EasyWorshipDatabase.get_song_with_processed_lyrics() for complete processing")