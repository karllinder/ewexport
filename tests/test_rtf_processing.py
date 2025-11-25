"""
Tests for RTF processing modules.

Tests RTF parsing, section detection, and text cleaning with Swedish characters
and EasyWorship-specific RTF formatting.
"""

import unittest
import sys
import os
from pathlib import Path

# Add src to path for testing
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from processing import parse_rtf, detect_sections, clean_text
from processing.rtf_parser import EasyWorshipRTFParser
from processing.section_detector import SectionDetector, AdvancedSectionDetector
from processing.text_cleaner import TextCleaner, SongTextCleaner


class TestRTFParser(unittest.TestCase):
    """Test RTF parsing functionality."""
    
    def setUp(self):
        self.parser = EasyWorshipRTFParser()
    
    def test_swedish_unicode_parsing(self):
        """Test parsing of Swedish Unicode characters."""
        rtf_content = r"""{{\rtf1\ansi\deff0 {\fonttbl {\f0 Times New Roman;}}
        Djupt inne i hj\u228?rtat\par
        det finns en eld som aldrig sl\u246?cknar\par
        \par
        Abba F\u229?der\par
        L\u180?t mig f\u229? se vem Du \u228?r}"""
        
        result = self.parser.parse(rtf_content)
        
        self.assertIsNotNone(result)
        self.assertTrue(result['has_content'])
        self.assertIn('hjärtat', result['plain_text'])
        self.assertIn('slöcknar', result['plain_text'])
        self.assertIn('Fåder', result['plain_text'])
        self.assertIn('få', result['plain_text'])
        self.assertIn('är', result['plain_text'])
    
    def test_section_markers_preserved(self):
        """Test that section markers are properly preserved."""
        rtf_content = r"""{{\rtf1\ansi\deff0 {\fonttbl {\f0 Times New Roman;}}
        verse\par
        This is verse content\par
        \par
        chorus\par
        This is chorus content\par}"""
        
        result = self.parser.parse(rtf_content)
        
        self.assertIsNotNone(result)
        self.assertIn('verse', result['plain_text'])
        self.assertIn('chorus', result['plain_text'])
        self.assertIn('This is verse content', result['plain_text'])
        self.assertIn('This is chorus content', result['plain_text'])
    
    def test_empty_content(self):
        """Test handling of empty or None RTF content."""
        self.assertIsNone(self.parser.parse(None))
        self.assertIsNone(self.parser.parse(""))
        self.assertIsNone(self.parser.parse("   "))
    
    def test_malformed_rtf_fallback(self):
        """Test fallback parsing for malformed RTF."""
        malformed_rtf = "This is not RTF but contains \\u228? Swedish chars"
        
        result = self.parser.parse(malformed_rtf)
        
        self.assertIsNotNone(result)
        self.assertIn('ä', result['plain_text'])


class TestSectionDetector(unittest.TestCase):
    """Test section detection functionality."""
    
    def setUp(self):
        self.detector = SectionDetector()
        self.advanced_detector = AdvancedSectionDetector()
    
    def test_basic_section_detection(self):
        """Test detection of basic song sections."""
        text = """verse
This is the first verse
With some content

chorus
This is the chorus
That repeats

verse
This is the second verse
More content here"""

        result = self.detector.detect_sections(text)

        self.assertTrue(result['has_sections'])
        self.assertEqual(len(result['sections']), 3)

        sections = result['sections']
        # Section types are mapped to capitalized English names
        self.assertEqual(sections[0]['type'], 'Verse')
        self.assertEqual(sections[1]['type'], 'Chorus')
        self.assertEqual(sections[2]['type'], 'Verse')

        self.assertIn('first verse', sections[0]['content'])
        self.assertIn('chorus', sections[1]['content'].lower())
        self.assertIn('second verse', sections[2]['content'])
    
    def test_numbered_sections(self):
        """Test detection of numbered sections like 'verse 1'."""
        text = """verse 1
First verse content

chorus
Chorus content

verse 2
Second verse content"""

        result = self.detector.detect_sections(text)

        self.assertTrue(result['has_sections'])
        self.assertEqual(len(result['sections']), 3)

        # Numbered sections include the number in the type (e.g., 'Verse 1')
        sections = result['sections']
        self.assertEqual(sections[0]['type'], 'Verse 1')
        self.assertEqual(sections[1]['type'], 'Chorus')
        self.assertEqual(sections[2]['type'], 'Verse 2')
    
    def test_swedish_section_mapping(self):
        """Test mapping of Swedish section names to English."""
        text = """vers
Swedish verse content

refräng
Swedish chorus content"""

        result = self.detector.detect_sections(text)

        self.assertTrue(result['has_sections'])
        sections = result['sections']

        # Swedish section names are mapped to capitalized English equivalents
        self.assertEqual(sections[0]['type'], 'Verse')
        self.assertEqual(sections[1]['type'], 'Chorus')
    
    def test_no_sections_fallback(self):
        """Test fallback when no sections are detected."""
        text = """This is just plain text
Without any section markers
But it should still be processed"""
        
        result = self.detector.detect_sections(text)
        
        self.assertFalse(result['has_sections'])
        self.assertEqual(len(result['sections']), 1)
        self.assertEqual(result['sections'][0]['type'], 'verse')
        self.assertIn('plain text', result['sections'][0]['content'])
    
    def test_advanced_pattern_detection(self):
        """Test advanced pattern detection for repeated content."""
        text = """This is verse one
With unique content

This repeats twice
And appears again

This is verse two
With different content

This repeats twice
And appears again"""
        
        result = self.advanced_detector.detect_sections(text)
        
        # Should detect the repeated content as chorus
        if result['has_sections']:
            chorus_sections = [s for s in result['sections'] if s['type'] == 'chorus']
            self.assertTrue(len(chorus_sections) >= 1)


class TestTextCleaner(unittest.TestCase):
    """Test text cleaning functionality."""
    
    def setUp(self):
        self.cleaner = TextCleaner()
        self.song_cleaner = SongTextCleaner()
    
    def test_whitespace_normalization(self):
        """Test normalization of various whitespace issues."""
        text = "Line  with   multiple    spaces\n\n\n\nToo many blank lines\t\tTabs here"
        
        cleaned = self.cleaner.clean(text)
        
        # Should normalize multiple spaces to single spaces within lines
        lines = cleaned.split('\n')
        for line in lines:
            self.assertNotIn('  ', line, f"Line contains multiple spaces: {repr(line)}")
        # Should reduce excessive blank lines
        self.assertNotIn('\n\n\n', cleaned)
        # Should convert tabs to spaces
        self.assertNotIn('\t', cleaned)
    
    def test_rtf_artifact_removal(self):
        """Test removal of remaining RTF artifacts."""
        text = "Text with \\rtf1 artifacts and {\\f0 font codes}"
        
        cleaned = self.cleaner.clean(text)
        
        self.assertNotIn('\\rtf1', cleaned)
        self.assertNotIn('{\\f0', cleaned)
        self.assertNotIn('}', cleaned)
    
    def test_special_character_replacement(self):
        """Test replacement of special characters."""
        # Using Unicode escapes to avoid syntax issues
        text = "Smart \u201Cquotes\u201D and \u2018apostrophes\u2019 and\u2014dashes"
        
        cleaned = self.cleaner.clean(text)
        
        # Should convert to regular quotes and dashes
        self.assertIn('"quotes"', cleaned)
        self.assertIn("'apostrophes'", cleaned)
        self.assertIn('-dashes', cleaned)
    
    def test_song_specific_cleaning(self):
        """Test song-specific text cleaning features."""
        text = """line one(x2)
        Line Two  [C]  [G7]  with chords
        line three [2x]"""
        
        # Test with chord removal
        chord_cleaner = SongTextCleaner(remove_chords=True)
        cleaned = chord_cleaner.clean(text)
        
        # Should remove repetition markers
        self.assertNotIn('(x2)', cleaned)
        self.assertNotIn('[2x]', cleaned)
        
        # Should remove chords if enabled
        self.assertNotIn('[C]', cleaned)
        self.assertNotIn('[G7]', cleaned)
        
        # Should capitalize first letters
        lines = cleaned.split('\n')
        for line in lines:
            if line.strip():
                self.assertTrue(line.strip()[0].isupper())


class TestIntegratedWorkflow(unittest.TestCase):
    """Test the complete RTF processing workflow."""
    
    def test_complete_swedish_song_processing(self):
        """Test complete processing of a Swedish song with sections."""
        rtf_content = r"""{{\rtf1\ansi\deff0 {\fonttbl {\f0 Times New Roman;}}
        verse\par
        Djupt inne i hj\u228?rtat\par
        det finns en eld som aldrig sl\u246?cknar\par
        \par
        chorus\par
        Abba F\u229?der\par
        L\u180?t mig f\u229? se vem Du \u228?r\par
        \par
        verse\par
        Anden fl\u246?dar genom mitt sinne\par
        och fyller mitt hj\u228?rta med k\u228?rlek}"""
        
        # Step 1: Parse RTF
        parsed = parse_rtf(rtf_content)
        self.assertIsNotNone(parsed)
        self.assertTrue(parsed['has_content'])
        
        # Step 2: Clean text
        cleaned = clean_text(parsed['plain_text'], for_song=True)
        
        # Step 3: Detect sections
        sections = detect_sections(cleaned)
        
        # Verify complete workflow
        self.assertTrue(sections['has_sections'])
        self.assertEqual(len(sections['sections']), 3)
        
        # Verify Swedish characters are preserved
        full_text = sections['plain_text']
        self.assertIn('hjärtat', full_text)
        self.assertIn('slöcknar', full_text)
        self.assertIn('Fåder', full_text)
        self.assertIn('få', full_text)
        self.assertIn('är', full_text)
        self.assertIn('flödar', full_text)
        self.assertIn('kärlek', full_text)
        
        # Verify section structure (types are capitalized English names)
        verse_sections = [s for s in sections['sections'] if s['type'] == 'Verse']
        chorus_sections = [s for s in sections['sections'] if s['type'] == 'Chorus']

        self.assertEqual(len(verse_sections), 2)
        self.assertEqual(len(chorus_sections), 1)


if __name__ == '__main__':
    # Set up basic logging for tests
    import logging
    logging.basicConfig(level=logging.DEBUG)
    
    unittest.main()