#!/usr/bin/env python3
"""
Test the complete export pipeline
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pathlib import Path
from src.export.propresenter import ProPresenterExporter
from src.processing.rtf_parser import parse_rtf
from src.processing.section_detector import detect_sections
from src.processing.text_cleaner import clean_text

def test_complete_pipeline():
    """Test the complete export pipeline with Swedish content"""
    
    print("=" * 60)
    print("EasyWorship to ProPresenter Export Pipeline Test")
    print("=" * 60)
    
    # Sample RTF content with Swedish characters
    rtf_content = r"""{{\rtf1\ansi\deff0 {\fonttbl {\f0 Times New Roman;}}
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
N\u228?r jag s\u229?nger ditt heliga namn\par
}"""
    
    # Sample song data
    song_data = {
        'rowid': 1,
        'title': 'Abba Fader',
        'author': 'Swedish Hymn Writer',
        'copyright': '© 2023 Swedish Church',
        'administrator': 'Svenska Kyrkan',
        'reference_number': '12345',
        'tags': 'worship, swedish',
        'description': 'Swedish worship song'
    }
    
    print("1. Testing RTF Parsing...")
    print("-" * 30)
    
    # Parse RTF
    rtf_result = parse_rtf(rtf_content)
    print(f"[OK] RTF parsed successfully")
    
    if rtf_result and 'plain_text' in rtf_result:
        plain_text = rtf_result['plain_text']
        print(f"  Swedish characters preserved: {'hjärtat' in plain_text and 'Fåder' in plain_text}")
        print(f"  Content length: {len(plain_text)} characters")
    else:
        print("[ERROR] Failed to extract plain text from RTF result")
        return
    
    print("\n2. Testing Text Cleaning...")
    print("-" * 30)
    
    # Clean text
    cleaned_text = clean_text(plain_text)
    print(f"[OK] Text cleaned successfully")
    print(f"  First line capitalized: {cleaned_text.startswith('Verse')}")
    
    print("\n3. Testing Section Detection...")
    print("-" * 30)
    
    # Detect sections
    section_result = detect_sections(cleaned_text)
    print(f"[OK] Sections detected")
    print(f"  Type: {type(section_result)}")
    print(f"  Keys: {list(section_result.keys()) if isinstance(section_result, dict) else 'Not a dict'}")
    
    # Extract sections list from result
    if isinstance(section_result, dict) and 'sections' in section_result:
        sections = section_result['sections']
        print(f"  Number of sections: {len(sections)}")
        
        for i, section in enumerate(sections, 1):
            if isinstance(section, dict):
                print(f"  Section {i}: {section['type'].upper()}")
                content_preview = section['content'][:50].replace('\n', ' ')
                print(f"    Content: {content_preview}...")
            else:
                print(f"  Section {i}: {section}")
    else:
        print("[ERROR] Could not extract sections from result")
        return
    
    print("\n4. Testing ProPresenter Export...")
    print("-" * 30)
    
    # Export to ProPresenter
    exporter = ProPresenterExporter()
    output_path = Path("./test_export")
    
    success, result = exporter.export_song(song_data, sections, output_path)
    
    if success:
        print(f"[OK] Export successful")
        print(f"  File created: {result}")
        
        # Verify file exists and has content
        if Path(result).exists():
            file_size = Path(result).stat().st_size
            print(f"  File size: {file_size} bytes")
            
            # Read and check XML structure
            with open(result, 'r', encoding='utf-8') as f:
                xml_content = f.read()
                
            print(f"  XML structure checks:")
            print(f"    - Contains RVPresentationDocument: {'RVPresentationDocument' in xml_content}")
            print(f"    - Contains song title: {song_data['title'] in xml_content}")
            print(f"    - Contains CCLI info: {'CCLISongNumber' in xml_content}")
            print(f"    - Contains slide groups: {'RVSlideGrouping' in xml_content}")
            print(f"    - Contains text elements: {'RVTextElement' in xml_content}")
            
        else:
            print(f"[ERROR] File was not created")
            
    else:
        print(f"[ERROR] Export failed: {result}")
    
    print("\n5. Testing Batch Export...")
    print("-" * 30)
    
    # Test batch export with multiple songs
    songs_batch = [
        (song_data, sections),
        ({
            'rowid': 2,
            'title': 'Test Song 2',
            'author': 'Test Author',
            'copyright': '',
            'administrator': '',
            'reference_number': '',
            'tags': '',
            'description': ''
        }, [{'type': 'verse', 'content': 'Simple test verse\nWith two lines'}])
    ]
    
    def progress_callback(current, total, title):
        print(f"    Progress: {current + 1}/{total} - {title}")
    
    successful, failed = exporter.export_songs_batch(songs_batch, output_path, progress_callback)
    
    print(f"[OK] Batch export completed")
    print(f"  Successful: {len(successful)} songs")
    print(f"  Failed: {len(failed)} songs")
    
    if successful:
        print(f"  Successfully exported files:")
        for file_path in successful:
            print(f"    - {file_path}")
    
    if failed:
        print(f"  Failed exports:")
        for error in failed:
            print(f"    - {error}")
    
    print("\n" + "=" * 60)
    print("Pipeline Test Complete!")
    
    # Cleanup test files
    import shutil
    if output_path.exists():
        shutil.rmtree(output_path)
        print("Test files cleaned up.")
    
    print("=" * 60)

def test_filename_sanitization():
    """Test filename sanitization"""
    print("\nTesting Filename Sanitization:")
    print("-" * 30)
    
    exporter = ProPresenterExporter()
    
    test_cases = [
        ("Normal Song Title", "Normal Song Title"),
        ("Song with / slash", "Song with _ slash"),
        ("Song: with colon", "Song_ with colon"),
        ("Song with <brackets>", "Song with _brackets_"),
        ("Song with \"quotes\"", "Song with _quotes_"),
        ("Song with |pipe|", "Song with _pipe_"),
        ("Song with *asterisk*", "Song with _asterisk_"),
        ("Song with ?question?", "Song with _question_"),
        ("", "Untitled_Song"),
        ("..." + "x" * 200, "..." + "x" * 197),  # Long filename
    ]
    
    for original, expected in test_cases:
        sanitized = exporter.sanitize_filename(original)
        status = "[OK]" if sanitized == expected else "[ERROR]"
        print(f"  {status} '{original[:30]}...' -> '{sanitized[:30]}...'")

if __name__ == "__main__":
    test_complete_pipeline()
    test_filename_sanitization()