"""
Tests for the LanguageManager module
"""

import unittest
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from processing.language_manager import LanguageManager


class TestLanguageManager(unittest.TestCase):
    """Test cases for LanguageManager"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.manager = LanguageManager()
        
    def test_available_languages(self):
        """Test getting available languages"""
        source_langs = self.manager.get_available_source_languages()
        self.assertIn("swedish", source_langs)
        self.assertIn("german", source_langs)
        self.assertIn("english", source_langs)
        
        target_langs = self.manager.get_available_target_languages()
        self.assertIn("english", target_langs)
        self.assertIn("german", target_langs)
        
    def test_set_source_languages(self):
        """Test setting source languages"""
        self.manager.set_source_languages(["swedish", "english"])
        self.assertEqual(self.manager.source_languages, ["swedish", "english"])
        
        # Test with invalid language (should be filtered)
        self.manager.set_source_languages(["swedish", "klingon"])
        self.assertEqual(self.manager.source_languages, ["swedish"])
        
    def test_set_target_language(self):
        """Test setting target language"""
        self.manager.set_target_language("german")
        self.assertEqual(self.manager.target_language, "german")
        
        # Test with invalid language (should default to English)
        self.manager.set_target_language("klingon")
        self.assertEqual(self.manager.target_language, "english")
        
    def test_auto_populate_english_target(self):
        """Test auto-populate with English target"""
        self.manager.set_source_languages(["swedish", "german"])
        self.manager.set_target_language("english")
        
        mappings = self.manager.auto_populate_mappings()
        
        # Check Swedish mappings
        self.assertEqual(mappings.get("vers"), "Verse")
        self.assertEqual(mappings.get("refräng"), "Chorus")
        
        # Check German mappings
        self.assertEqual(mappings.get("strophe"), "Verse")
        self.assertEqual(mappings.get("refrain"), "Chorus")
        
    def test_auto_populate_non_english_target(self):
        """Test auto-populate with non-English target (should return empty)"""
        self.manager.set_source_languages(["swedish"])
        self.manager.set_target_language("german")
        
        mappings = self.manager.auto_populate_mappings()
        self.assertEqual(mappings, {})
        
    def test_manual_mappings(self):
        """Test setting manual mappings"""
        self.manager.set_target_language("german")
        
        manual_mappings = {
            "vers": "Strophe",
            "refräng": "Refrain",
            "bridge": "Brücke"
        }
        
        self.manager.set_manual_mappings(manual_mappings)
        
        # Check mappings (should be case-insensitive)
        self.assertEqual(self.manager.get_mapping("vers"), "Strophe")
        self.assertEqual(self.manager.get_mapping("VERS"), "Strophe")
        self.assertEqual(self.manager.get_mapping("refräng"), "Refrain")
        
    def test_get_target_section_names(self):
        """Test getting section names for target language"""
        self.manager.set_target_language("german")
        sections = self.manager.get_target_section_names()
        
        self.assertIn("Strophe", sections)
        self.assertIn("Refrain", sections)
        self.assertIn("Brücke", sections)
        
    def test_get_all_source_terms(self):
        """Test getting all source terms from selected languages"""
        self.manager.set_source_languages(["swedish", "english"])
        
        terms = self.manager.get_all_source_terms()
        
        # Check Swedish terms
        self.assertIn("vers", terms)
        self.assertIn("refräng", terms)
        
        # Check English terms
        self.assertIn("verse", terms)
        self.assertIn("chorus", terms)
        
    def test_validation(self):
        """Test validation of mappings"""
        # No source languages
        issues = self.manager.validate_mappings()
        self.assertIn("No source languages selected", issues)
        
        # Non-English target without mappings
        self.manager.set_source_languages(["swedish"])
        self.manager.set_target_language("german")
        issues = self.manager.validate_mappings()
        self.assertIn("Non-English target requires manual mappings", issues)
        
        # Valid configuration
        self.manager.set_target_language("english")
        self.manager.auto_populate_mappings()
        issues = self.manager.validate_mappings()
        self.assertEqual(len(issues), 0)
        
    def test_export_import_config(self):
        """Test exporting and importing configuration"""
        # Set up configuration
        self.manager.set_source_languages(["swedish", "german"])
        self.manager.set_target_language("english")
        self.manager.auto_populate_mappings()
        
        # Export
        config = self.manager.export_config()
        
        self.assertEqual(config["source_languages"], ["swedish", "german"])
        self.assertEqual(config["target_language"], "english")
        self.assertIn("vers", config["active_mappings"])
        
        # Import into new manager
        new_manager = LanguageManager()
        new_manager.import_config(config)
        
        self.assertEqual(new_manager.source_languages, ["swedish", "german"])
        self.assertEqual(new_manager.target_language, "english")
        self.assertEqual(new_manager.get_mapping("vers"), "Verse")
        
    def test_case_insensitive_mapping(self):
        """Test that mappings are case-insensitive"""
        self.manager.set_source_languages(["swedish"])
        self.manager.set_target_language("english")
        self.manager.auto_populate_mappings()
        
        # All these should return the same result
        self.assertEqual(self.manager.get_mapping("vers"), "Verse")
        self.assertEqual(self.manager.get_mapping("Vers"), "Verse")
        self.assertEqual(self.manager.get_mapping("VERS"), "Verse")
        
    def test_alternative_spellings(self):
        """Test that alternative spellings are handled"""
        self.manager.set_source_languages(["swedish", "danish"])
        self.manager.set_target_language("english")
        self.manager.auto_populate_mappings()
        
        # Swedish alternatives
        self.assertEqual(self.manager.get_mapping("refrang"), "Chorus")  # Without umlaut
        self.assertEqual(self.manager.get_mapping("forrefrang"), "Pre-Chorus")  # Without umlaut
        
        # Danish alternatives
        self.assertEqual(self.manager.get_mapping("omkvaed"), "Chorus")  # Without special char


if __name__ == '__main__':
    unittest.main()