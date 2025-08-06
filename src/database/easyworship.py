"""
EasyWorship database access layer
"""

import sqlite3
from pathlib import Path
from typing import List, Dict, Optional, Any

class EasyWorshipDatabase:
    def __init__(self, db_path: str):
        self.db_path = Path(db_path)
        self.songs_db = self.db_path / "Songs.db"
        self.words_db = self.db_path / "SongWords.db"
        
    def validate_database(self) -> bool:
        """Check if database files exist and are valid"""
        if not self.songs_db.exists():
            return False
        if not self.words_db.exists():
            return False
        
        try:
            conn = sqlite3.connect(self.songs_db)
            cursor = conn.execute("SELECT COUNT(*) FROM song")
            cursor.fetchone()
            conn.close()
            
            conn = sqlite3.connect(self.words_db)
            cursor = conn.execute("SELECT COUNT(*) FROM word")
            cursor.fetchone()
            conn.close()
            
            return True
        except Exception:
            return False
    
    def get_all_songs(self) -> List[Dict[str, Any]]:
        """Retrieve all songs with metadata"""
        conn = sqlite3.connect(self.songs_db)
        conn.row_factory = sqlite3.Row
        
        query = """
        SELECT 
            rowid,
            title,
            COALESCE(author, '') as author,
            COALESCE(copyright, '') as copyright,
            COALESCE(administrator, '') as administrator,
            COALESCE(reference_number, '') as reference_number,
            COALESCE(tags, '') as tags,
            COALESCE(description, '') as description
        FROM song
        ORDER BY title COLLATE NOCASE
        """
        
        cursor = conn.execute(query)
        songs = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return songs
    
    def get_song_lyrics(self, song_rowid: int) -> Optional[str]:
        """Get RTF lyrics for a specific song"""
        conn = sqlite3.connect(self.words_db)
        
        query = """
        SELECT words 
        FROM word
        WHERE song_id = ?
        """
        
        cursor = conn.execute(query, (song_rowid,))
        result = cursor.fetchone()
        conn.close()
        
        return result[0] if result else None
    
    def get_song_count(self) -> int:
        """Get total number of songs in database"""
        try:
            conn = sqlite3.connect(self.songs_db)
            cursor = conn.execute("SELECT COUNT(*) FROM song")
            count = cursor.fetchone()[0]
            conn.close()
            return count
        except Exception:
            return 0