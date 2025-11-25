"""
Tests for EasyWorship database access layer.

Tests database validation, song retrieval, lyrics fetching, and data processing
with in-memory SQLite databases to avoid file system dependencies.
"""

import unittest
import sqlite3
import sys
import os
import tempfile
import shutil
from pathlib import Path

# Add src to path for testing
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from database.easyworship import EasyWorshipDatabase


class TestDatabaseValidation(unittest.TestCase):
    """Test database validation functionality."""

    def setUp(self):
        """Create temporary database directory for each test."""
        self.temp_dir = tempfile.mkdtemp()
        self.db = EasyWorshipDatabase(self.temp_dir)

    def tearDown(self):
        """Clean up temporary directory after each test."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_validate_missing_songs_db(self):
        """Test validation fails when Songs.db is missing."""
        # Create only SongWords.db
        words_db = Path(self.temp_dir) / "SongWords.db"
        conn = sqlite3.connect(str(words_db))
        conn.execute("CREATE TABLE word (song_id INTEGER, words TEXT)")
        conn.close()

        self.assertFalse(self.db.validate_database())

    def test_validate_missing_words_db(self):
        """Test validation fails when SongWords.db is missing."""
        # Create only Songs.db
        songs_db = Path(self.temp_dir) / "Songs.db"
        conn = sqlite3.connect(str(songs_db))
        conn.execute("CREATE TABLE song (rowid INTEGER PRIMARY KEY, title TEXT)")
        conn.close()

        self.assertFalse(self.db.validate_database())

    def test_validate_both_databases_present(self):
        """Test validation passes when both databases exist with correct tables."""
        # Create Songs.db
        songs_db = Path(self.temp_dir) / "Songs.db"
        conn = sqlite3.connect(str(songs_db))
        conn.execute("""CREATE TABLE song (
            rowid INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT,
            copyright TEXT,
            administrator TEXT,
            reference_number TEXT,
            tags TEXT,
            description TEXT
        )""")
        conn.close()

        # Create SongWords.db
        words_db = Path(self.temp_dir) / "SongWords.db"
        conn = sqlite3.connect(str(words_db))
        conn.execute("CREATE TABLE word (rowid INTEGER PRIMARY KEY, song_id INTEGER, words TEXT)")
        conn.close()

        self.assertTrue(self.db.validate_database())

    def test_validate_invalid_songs_schema(self):
        """Test validation fails with invalid Songs.db schema."""
        # Create Songs.db without required song table
        songs_db = Path(self.temp_dir) / "Songs.db"
        conn = sqlite3.connect(str(songs_db))
        conn.execute("CREATE TABLE other_table (id INTEGER)")
        conn.close()

        # Create valid SongWords.db
        words_db = Path(self.temp_dir) / "SongWords.db"
        conn = sqlite3.connect(str(words_db))
        conn.execute("CREATE TABLE word (song_id INTEGER, words TEXT)")
        conn.close()

        self.assertFalse(self.db.validate_database())


class TestSongRetrieval(unittest.TestCase):
    """Test song retrieval functionality."""

    def setUp(self):
        """Create temporary databases with test data."""
        self.temp_dir = tempfile.mkdtemp()
        self._create_test_databases()
        self.db = EasyWorshipDatabase(self.temp_dir)

    def tearDown(self):
        """Clean up temporary directory."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _create_test_databases(self):
        """Create test databases with sample song data."""
        # Create Songs.db
        songs_db = Path(self.temp_dir) / "Songs.db"
        conn = sqlite3.connect(str(songs_db))
        conn.execute("""CREATE TABLE song (
            rowid INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT,
            copyright TEXT,
            administrator TEXT,
            reference_number TEXT,
            tags TEXT,
            description TEXT
        )""")

        # Insert test songs
        test_songs = [
            ("Amazing Grace", "John Newton", "Public Domain", None, "12345", "hymn", "Classic hymn"),
            ("Abba Fader", None, None, None, None, "worship", None),
            ("Alfa och Omega", "Unknown", "2020 Test", "Publisher", "67890", "swedish,worship", "Swedish song"),
        ]
        conn.executemany(
            "INSERT INTO song (title, author, copyright, administrator, reference_number, tags, description) VALUES (?, ?, ?, ?, ?, ?, ?)",
            test_songs
        )
        conn.commit()
        conn.close()

        # Create SongWords.db
        words_db = Path(self.temp_dir) / "SongWords.db"
        conn = sqlite3.connect(str(words_db))
        conn.execute("CREATE TABLE word (rowid INTEGER PRIMARY KEY, song_id INTEGER, words TEXT)")

        # Insert test lyrics (RTF format)
        test_lyrics = [
            (1, r"{\rtf1\ansi verse\par Amazing grace how sweet the sound\par}"),
            (2, r"{\rtf1\ansi vers\par Abba F\u229?der\par L\u228?t mig f\u229? se vem Du \u228?r\par}"),
            (3, r"{\rtf1\ansi verse 1\par Alfa och Omega\par \par chorus\par Du \u228?r min Gud\par}"),
        ]
        conn.executemany(
            "INSERT INTO word (song_id, words) VALUES (?, ?)",
            test_lyrics
        )
        conn.commit()
        conn.close()

    def test_get_all_songs(self):
        """Test retrieving all songs from database."""
        songs = self.db.get_all_songs()

        self.assertEqual(len(songs), 3)

        # Songs should be ordered by title (case insensitive)
        titles = [s['title'] for s in songs]
        self.assertEqual(titles, ["Abba Fader", "Alfa och Omega", "Amazing Grace"])

    def test_get_all_songs_with_empty_fields(self):
        """Test that empty fields are returned as empty strings."""
        songs = self.db.get_all_songs()

        # Find "Abba Fader" which has NULL fields
        abba = next(s for s in songs if s['title'] == "Abba Fader")

        self.assertEqual(abba['author'], '')
        self.assertEqual(abba['copyright'], '')
        self.assertEqual(abba['administrator'], '')
        self.assertEqual(abba['reference_number'], '')

    def test_get_all_songs_with_metadata(self):
        """Test that metadata fields are properly retrieved."""
        songs = self.db.get_all_songs()

        # Find "Amazing Grace" which has full metadata
        amazing = next(s for s in songs if s['title'] == "Amazing Grace")

        self.assertEqual(amazing['author'], 'John Newton')
        self.assertEqual(amazing['copyright'], 'Public Domain')
        self.assertEqual(amazing['reference_number'], '12345')
        self.assertEqual(amazing['tags'], 'hymn')

    def test_get_song_lyrics(self):
        """Test retrieving lyrics for a specific song."""
        lyrics = self.db.get_song_lyrics(1)

        self.assertIsNotNone(lyrics)
        self.assertIn('Amazing grace', lyrics)

    def test_get_song_lyrics_nonexistent(self):
        """Test retrieving lyrics for non-existent song returns None."""
        lyrics = self.db.get_song_lyrics(999)

        self.assertIsNone(lyrics)

    def test_get_song_count(self):
        """Test getting total song count."""
        count = self.db.get_song_count()

        self.assertEqual(count, 3)


class TestSongProcessing(unittest.TestCase):
    """Test song processing with RTF parsing and section detection."""

    def setUp(self):
        """Create temporary databases with test data."""
        self.temp_dir = tempfile.mkdtemp()
        self._create_test_databases()
        self.db = EasyWorshipDatabase(self.temp_dir)

    def tearDown(self):
        """Clean up temporary directory."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _create_test_databases(self):
        """Create test databases with Swedish song data."""
        # Create Songs.db
        songs_db = Path(self.temp_dir) / "Songs.db"
        conn = sqlite3.connect(str(songs_db))
        conn.execute("""CREATE TABLE song (
            rowid INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT,
            copyright TEXT,
            administrator TEXT,
            reference_number TEXT,
            tags TEXT,
            description TEXT
        )""")

        conn.execute(
            "INSERT INTO song (title, author) VALUES (?, ?)",
            ("Test Swedish Song", "Test Author")
        )
        conn.execute(
            "INSERT INTO song (title) VALUES (?)",
            ("Empty Song",)
        )
        conn.commit()
        conn.close()

        # Create SongWords.db
        words_db = Path(self.temp_dir) / "SongWords.db"
        conn = sqlite3.connect(str(words_db))
        conn.execute("CREATE TABLE word (rowid INTEGER PRIMARY KEY, song_id INTEGER, words TEXT)")

        # Swedish song with sections
        swedish_rtf = r"""{\rtf1\ansi\deff0 {\fonttbl {\f0 Times New Roman;}}
        verse\par
        Djupt inne i hj\u228?rtat\par
        det finns en eld\par
        \par
        chorus\par
        Abba F\u229?der\par
        L\u228?t mig se\par}"""

        conn.execute("INSERT INTO word (song_id, words) VALUES (?, ?)", (1, swedish_rtf))
        # Song 2 has no lyrics
        conn.commit()
        conn.close()

    def test_get_song_with_processed_lyrics(self):
        """Test retrieving a song with fully processed lyrics."""
        song = self.db.get_song_with_processed_lyrics(1)

        self.assertIsNotNone(song)
        self.assertEqual(song['title'], "Test Swedish Song")
        self.assertTrue(song['has_sections'])
        self.assertGreater(len(song['sections']), 0)

    def test_get_song_with_no_lyrics(self):
        """Test retrieving a song that has no lyrics."""
        song = self.db.get_song_with_processed_lyrics(2)

        self.assertIsNotNone(song)
        self.assertEqual(song['title'], "Empty Song")
        self.assertFalse(song['has_sections'])
        self.assertEqual(song['sections'], [])
        self.assertEqual(song['processed_text'], '')

    def test_get_song_nonexistent(self):
        """Test retrieving a non-existent song returns None."""
        song = self.db.get_song_with_processed_lyrics(999)

        self.assertIsNone(song)

    def test_swedish_character_preservation(self):
        """Test that Swedish characters are preserved in processed lyrics."""
        song = self.db.get_song_with_processed_lyrics(1)

        self.assertIsNotNone(song)
        processed = song['processed_text']

        # Check Swedish characters are present (using Unicode escapes)
        # \u00e4 = a with umlaut, \u00e5 = a with ring
        self.assertIn('hj\u00e4rtat', processed)  # hjärtat
        self.assertIn('F\u00e5der', processed)    # Fåder
        self.assertIn('L\u00e4t', processed)      # Lät


class TestSectionMappingsReload(unittest.TestCase):
    """Test section mappings reload functionality."""

    def setUp(self):
        """Create temporary database."""
        self.temp_dir = tempfile.mkdtemp()
        self._create_minimal_databases()
        self.db = EasyWorshipDatabase(self.temp_dir)

    def tearDown(self):
        """Clean up temporary directory."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _create_minimal_databases(self):
        """Create minimal test databases."""
        # Create Songs.db
        songs_db = Path(self.temp_dir) / "Songs.db"
        conn = sqlite3.connect(str(songs_db))
        conn.execute("""CREATE TABLE song (
            rowid INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT,
            copyright TEXT,
            administrator TEXT,
            reference_number TEXT,
            tags TEXT,
            description TEXT
        )""")
        conn.close()

        # Create SongWords.db
        words_db = Path(self.temp_dir) / "SongWords.db"
        conn = sqlite3.connect(str(words_db))
        conn.execute("CREATE TABLE word (song_id INTEGER, words TEXT)")
        conn.close()

    def test_reload_section_mappings(self):
        """Test that reload_section_mappings clears the detector cache."""
        # Set a detector first
        self.db.section_detector = "dummy_detector"

        # Reload mappings
        self.db.reload_section_mappings()

        # Detector should be cleared
        self.assertIsNone(self.db.section_detector)


class TestEmptyDatabase(unittest.TestCase):
    """Test handling of empty databases."""

    def setUp(self):
        """Create temporary empty databases."""
        self.temp_dir = tempfile.mkdtemp()

        # Create empty Songs.db
        songs_db = Path(self.temp_dir) / "Songs.db"
        conn = sqlite3.connect(str(songs_db))
        conn.execute("""CREATE TABLE song (
            rowid INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT,
            copyright TEXT,
            administrator TEXT,
            reference_number TEXT,
            tags TEXT,
            description TEXT
        )""")
        conn.close()

        # Create empty SongWords.db
        words_db = Path(self.temp_dir) / "SongWords.db"
        conn = sqlite3.connect(str(words_db))
        conn.execute("CREATE TABLE word (song_id INTEGER, words TEXT)")
        conn.close()

        self.db = EasyWorshipDatabase(self.temp_dir)

    def tearDown(self):
        """Clean up temporary directory."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_get_all_songs_empty(self):
        """Test retrieving songs from empty database returns empty list."""
        songs = self.db.get_all_songs()

        self.assertEqual(songs, [])

    def test_get_song_count_empty(self):
        """Test song count is zero for empty database."""
        count = self.db.get_song_count()

        self.assertEqual(count, 0)

    def test_get_all_songs_with_processed_lyrics_empty(self):
        """Test processed lyrics retrieval on empty database."""
        songs = self.db.get_all_songs_with_processed_lyrics()

        self.assertEqual(songs, [])


if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.DEBUG)

    unittest.main()
