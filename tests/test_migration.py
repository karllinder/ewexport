"""
Tests for settings migration functionality
"""

import unittest
import json
import tempfile
import shutil
from pathlib import Path
import sys

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from utils.config import ConfigManager


class TestSettingsMigration(unittest.TestCase):
    """Test cases for settings migration"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create temporary directory for test settings
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)
        
        # Create test ConfigManager with temp directory
        self.config = ConfigManager()
        self.config.app_data_dir = self.temp_path
        self.config.settings_file = self.temp_path / "settings.json"
        
    def tearDown(self):
        """Clean up test fixtures"""
        # Remove temporary directory
        shutil.rmtree(self.temp_dir)
        
    def test_migrate_from_1_0_0(self):
        """Test migration from v1.0.0 to v2.0.0"""
        # Create old v1.0.0 settings
        old_settings = {
            'version': '1.0.0',
            'paths': {
                'last_easyworship_path': 'C:/test/db',
                'last_export_path': 'C:/test/export'
            },
            'export': {
                'output_directory': 'C:/test/output'
            }
        }
        
        # Write old settings to file
        with open(self.config.settings_file, 'w') as f:
            json.dump(old_settings, f)
        
        # Load settings (should trigger migration)
        self.config.load_settings()
        
        # Check version was updated
        self.assertEqual(self.config.settings['version'], '2.0.0')
        
        # Check language settings were added
        self.assertIn('language_settings', self.config.settings)
        self.assertEqual(self.config.settings['language_settings']['target_language'], 'english')
        self.assertEqual(self.config.settings['language_settings']['source_languages'], ['swedish', 'english'])
        
        # Check old settings were preserved
        self.assertEqual(self.config.settings['paths']['last_easyworship_path'], 'C:/test/db')
        self.assertEqual(self.config.settings['export']['output_directory'], 'C:/test/output')
        
    def test_migrate_from_1_2_0(self):
        """Test migration from v1.2.0 to v2.0.0"""
        # Create v1.2.0 settings
        old_settings = {
            'version': '1.2.0',
            'app': {
                'first_run': False
            },
            'paths': {
                'last_easyworship_path': 'D:/easyworship',
                'recent_databases': ['D:/db1', 'D:/db2']
            },
            'export': {
                'output_directory': 'D:/export',
                'include_ccli_in_filename': True,
                'font': {
                    'family': 'Calibri',
                    'size': 48
                }
            },
            'song_list': {
                'column_widths': {
                    'title': 350,
                    'author': 250
                }
            }
        }
        
        # Write old settings to file
        with open(self.config.settings_file, 'w') as f:
            json.dump(old_settings, f)
        
        # Load settings (should trigger migration)
        self.config.load_settings()
        
        # Check version was updated
        self.assertEqual(self.config.settings['version'], '2.0.0')
        
        # Check language settings were added
        self.assertIn('language_settings', self.config.settings)
        self.assertEqual(self.config.settings['language_settings']['source_languages'], ['swedish', 'english'])
        
        # Check old settings were preserved
        self.assertEqual(self.config.settings['app']['first_run'], False)
        self.assertEqual(self.config.settings['export']['font']['family'], 'Calibri')
        self.assertEqual(self.config.settings['export']['font']['size'], 48)
        self.assertEqual(self.config.settings['song_list']['column_widths']['title'], 350)
        
    def test_migrate_no_version(self):
        """Test migration from settings without version field"""
        # Create settings without version
        old_settings = {
            'paths': {
                'last_easyworship_path': 'E:/db'
            }
        }
        
        # Write old settings to file
        with open(self.config.settings_file, 'w') as f:
            json.dump(old_settings, f)
        
        # Load settings (should trigger migration)
        self.config.load_settings()
        
        # Check version was added
        self.assertEqual(self.config.settings['version'], '2.0.0')
        
        # Check language settings were added
        self.assertIn('language_settings', self.config.settings)
        
        # Check old settings were preserved
        self.assertEqual(self.config.settings['paths']['last_easyworship_path'], 'E:/db')
        
    def test_backup_creation(self):
        """Test that backup is created during migration"""
        # Create old settings
        old_settings = {
            'version': '1.0.0',
            'test_data': 'important_value'
        }
        
        # Write old settings to file
        with open(self.config.settings_file, 'w') as f:
            json.dump(old_settings, f)
        
        # Load settings (should trigger migration and backup)
        self.config.load_settings()
        
        # Check that backup file was created
        backup_files = list(self.temp_path.glob("settings_backup_*.json"))
        self.assertTrue(len(backup_files) > 0, "No backup file created")
        
        # Check backup content
        with open(backup_files[0], 'r') as f:
            backup_data = json.load(f)
        
        self.assertEqual(backup_data['version'], '1.0.0')
        self.assertEqual(backup_data['test_data'], 'important_value')
        
    def test_no_migration_for_current_version(self):
        """Test that no migration happens for current version"""
        # Create current version settings
        current_settings = {
            'version': '2.0.0',
            'language_settings': {
                'source_languages': ['german'],
                'target_language': 'french'
            }
        }
        
        # Write settings to file
        with open(self.config.settings_file, 'w') as f:
            json.dump(current_settings, f)
        
        # Load settings (should NOT trigger migration)
        self.config.load_settings()
        
        # Check no backup was created
        backup_files = list(self.temp_path.glob("settings_backup_*.json"))
        self.assertEqual(len(backup_files), 0, "Backup created when not needed")
        
        # Check settings unchanged
        self.assertEqual(self.config.settings['language_settings']['source_languages'], ['german'])
        self.assertEqual(self.config.settings['language_settings']['target_language'], 'french')
        
    def test_corrupted_settings_fallback(self):
        """Test fallback to defaults for corrupted settings"""
        # Write corrupted JSON
        with open(self.config.settings_file, 'w') as f:
            f.write("{corrupted json data}")
        
        # Load settings (should fall back to defaults)
        self.config.load_settings()
        
        # Check defaults were used
        self.assertEqual(self.config.settings['version'], '2.0.0')
        self.assertIn('language_settings', self.config.settings)
        self.assertEqual(self.config.settings['language_settings']['target_language'], 'english')
        
    def test_get_set_language_settings(self):
        """Test getting and setting language settings"""
        # Set language settings
        new_lang_settings = {
            'source_languages': ['german', 'french'],
            'target_language': 'spanish',
            'auto_populate_mappings': False
        }
        
        self.config.set_language_settings(new_lang_settings)
        
        # Get language settings
        retrieved = self.config.get_language_settings()
        
        self.assertEqual(retrieved['source_languages'], ['german', 'french'])
        self.assertEqual(retrieved['target_language'], 'spanish')
        self.assertEqual(retrieved['auto_populate_mappings'], False)
        
    def test_progressive_migration(self):
        """Test progressive migration through multiple versions"""
        # Create very old settings (v1.0.0)
        old_settings = {
            'version': '1.0.0',
            'paths': {
                'last_easyworship_path': 'F:/data'
            }
        }
        
        # Write old settings to file
        with open(self.config.settings_file, 'w') as f:
            json.dump(old_settings, f)
        
        # Load settings (should migrate through 1.0.0 -> 1.1.0 -> 2.0.0)
        self.config.load_settings()
        
        # Check final version
        self.assertEqual(self.config.settings['version'], '2.0.0')
        
        # Check all migrations were applied
        self.assertIn('export', self.config.settings)  # Added in 1.1.0
        self.assertIn('duplicate_handling', self.config.settings)  # Added in 1.1.0
        self.assertIn('language_settings', self.config.settings)  # Added in 2.0.0
        
        # Check original data preserved
        self.assertEqual(self.config.settings['paths']['last_easyworship_path'], 'F:/data')


if __name__ == '__main__':
    unittest.main()