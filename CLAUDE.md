# EasyWorship to ProPresenter Converter - Project Documentation

## Project Overview
A Windows 11 desktop application to convert songs from EasyWorship 6.1 database format to ProPresenter 6 format with a modern GUI interface. Primary focus is on Swedish and English language support.

**Current Status**: Production Release v1.1.1 (2025-01-11)
- ✅ Full EasyWorship 6.1 database support
- ✅ Complete ProPresenter 6 export pipeline
- ✅ Advanced export options and settings management
- ✅ Swedish character support and section mapping
- ✅ Real-time search, filtering, and batch operations

## Research Findings

### 1. EasyWorship 6.1 Database Structure

#### Database Files
- **Songs.db**: SQLite database containing song metadata
  - Location: `C:\Claud\ewtest\orginaldb`
  - File: `Songs.db`
  - Main table: `song`
  
- **SongWords.db**: SQLite database containing lyrics
  - Location: Same directory as Songs.db
  - File: `SongWords.db`
  - Main table: `word`
  - Links to Songs.db via foreign key

#### Database Schema Details

##### Songs.db - `song` table
```sql
CREATE TABLE "song" (
    "rowid" integer NOT NULL UNIQUE PRIMARY KEY AUTOINCREMENT,
    "song_item_uid" text UNIQUE,
    "song_rev_uid" text,
    "song_uid" text,
    "title" text NOT NULL COLLATE UTF8_U_CI,
    "author" text COLLATE UTF8_U_CI,
    "copyright" text COLLATE UTF8_U_CI,
    "administrator" text COLLATE UTF8_U_CI,
    "description" text,
    "tags" text COLLATE UTF8_U_CI,
    "reference_number" text COLLATE UTF8_U_CI,
    "vendor_id" integer,
    "presentation_id" integer,
    "layout_revision" integer DEFAULT 1,
    "revision" integer DEFAULT 1
);
```

Key fields for export:
- `rowid`: Primary key, used to link to lyrics
- `title`: Song title
- `author`: Composer/songwriter
- `copyright`: Copyright notice
- `administrator`: Rights administrator (often publishing company)
- `reference_number`: CCLI or other reference number
- `tags`: Categories/keywords for filtering
- `description`: Additional notes

##### SongWords.db - `word` table
```sql
CREATE TABLE "word" (
    "rowid" integer NOT NULL UNIQUE PRIMARY KEY,
    "song_id" integer,  -- Foreign key to song.rowid
    "words" rtf,        -- RTF formatted lyrics
    "slide_uids" text,
    "slide_layout_revisions" int64a,
    "slide_revisions" int64a
);
```

Key fields for export:
- `song_id`: Links to `song.rowid` in Songs.db
- `words`: RTF formatted lyrics (requires parsing)
- Other fields can be ignored for ProPresenter export

#### Real-World Database Observations
Based on actual data analysis:
- **Metadata Often Empty**: Many songs have only titles, with empty author/copyright/CCLI fields
- **Content Types**: 
  - Swedish worship songs (e.g., "Abba Fader", "Alfa och Omega")
  - English worship songs (e.g., "Above all", "A Move Of God")
  - Bible verses (e.g., "1 Mos 1:26-27" - Genesis references)
  - Song variations (e.g., "Above all" and "Above all 2")
- **No CCLI Data**: reference_number field typically empty (churches may not track this)
- **UID Format**: Uses PCI- prefix for unique identifiers
- **Special Characters**: Titles contain Swedish characters (å, ä, ö) and hyphens

#### Technical Challenges
- Custom UTF8_U_CI collation sequence
- RTF formatted text requiring extensive parsing
- Unicode and special character handling (Swedish characters: å, ä, ö)
- Connection to multiple SQLite databases simultaneously
- Section detection from RTF formatting
- Handling empty metadata fields gracefully

### 2. ProPresenter File Formats

#### ProPresenter 6 (.pro6)
- XML-based format, human-readable
- Structure includes:
  - RVPresentationDocument root element
  - RVDisplaySlide elements for each slide
  - RVTextElement for text content
  - Support for slide groups (verses, chorus, etc.) - English labels only
  - Hotkey assignments for quick navigation
  - Default slide dimensions (typically 1920x1080)
  - Font sizing calculations
  - Line break handling (auto vs manual)
  - Slide transition settings (default: 0.5s dissolve)

#### ProPresenter 7 (.pro)
- Binary format using Google Protocol Buffers
- Not directly human-readable
- More complex to generate programmatically
- Requires protobuf definitions or reverse engineering

**Decision**: Target ProPresenter 6 format due to simpler XML structure

#### ProPresenter 6 Export Requirements
- File naming restrictions (avoid special characters: /, \, :, *, ?, ", <, >, |)
- Standard font in XML output
- English-only section labels (Verse, Chorus, Bridge, etc.)

#### Field Mapping: EasyWorship to ProPresenter
- `song.title` → ProPresenter `CCLISongTitle`
- `song.author` → ProPresenter `CCLIAuthor` (if present)
- `song.copyright` → ProPresenter `CCLICopyright` (if present)
- `song.reference_number` → ProPresenter `CCLISongNumber` (if present)
- `song.administrator` → ProPresenter `CCLIPublisher` (if present)
- `word.words` (after RTF parsing) → ProPresenter slide content

**Note**: Many fields may be empty - ProPresenter XML should only include populated fields

### 3. Song Structure Handling

#### Section Detection
- **Source**: Sections are marked as plain text labels in the RTF content
- **Format**: Section names appear on their own line before the section content
- **Language**: Section markers are already in English (verse, chorus, bridge, etc.) even in Swedish songs!
- **Common Section Markers Found**:
  - verse
  - chorus
  - bridge
  - pre-chorus
  - outro
  - tag
- **Detection Method**: Parse RTF, identify lines that match section keywords
- **No Sections**: Songs without section markers should be treated as one continuous text

#### RTF Format Details
Based on actual data analysis:
- **Unicode Encoding**: Swedish characters use Unicode escape sequences
  - `\u228?` = ä
  - `\u229?` = å
  - `\u246?` = ö
  - `\u180?` = ´ (accent)
- **Line Breaks**: 
  - `\par` = paragraph/new slide
  - `\line` = line break within slide
- **Section Format**: Section labels appear as plain text on separate lines
- **Font Information**: Multiple fonts may be specified (`\f0`, `\f1`)

Example RTF structure:
```
verse
Djupt inne i hjärtat
det finns en eld
som aldrig slocknar

chorus
Abba Fader
Låt mig få se vem Du är
```

### 4. Existing PHP Solution Analysis

The ew61-export PHP solution provides:
- **RTF Parser**: Comprehensive character-by-character RTF parsing
- **Text Processing**: Handles Unicode, special characters, formatting
- **Database Access**: PDO SQLite connections
- **ProPresenter Generation**: XML template-based approach
- **Batch Processing**: Exports entire song libraries

Key functions to replicate:
- RTF to plain text conversion
- Unicode character handling (especially Swedish characters)
- Section detection (Verse, Chorus, Bridge)
- Section label translation (Swedish to English)
- XML generation with proper GUIDs

## Technology Stack: Python + Tkinter

### Why Python + Tkinter
**Pros:**
- Python has excellent SQLite support built-in
- Tkinter provides simple, native-looking GUI on Windows
- Easy RTF parsing with libraries like `striprtf`
- XML generation with `xml.etree.ElementTree`
- Single executable with PyInstaller
- Good Unicode support for Swedish characters

**Cons:**
- Requires Python installation or bundling
- GUI might look dated compared to modern frameworks

### Architecture Design

```
┌─────────────────────────────────────────────┐
│              GUI Layer (Tkinter)            │
│  - Database file selector                   │
│  - Song list display (with search)          │
│  - Export options                           │
│  - Progress indicator                       │
│  - Duplicate handling dialogs               │
└─────────────────────────────────────────────┘
                      │
┌─────────────────────────────────────────────┐
│            Business Logic Layer             │
│  - Song selection management                │
│  - Export orchestration                     │
│  - Configuration management                 │
│  - Duplicate detection                      │
└─────────────────────────────────────────────┘
                      │
┌─────────────────────────────────────────────┐
│             Data Access Layer               │
│  - SQLite database connections              │
│  - Song retrieval                           │
│  - RTF text extraction                      │
│  - Database validation                      │
└─────────────────────────────────────────────┘
                      │
┌─────────────────────────────────────────────┐
│           Processing Layer                  │
│  - RTF to text conversion                   │
│  - Text formatting and cleaning             │
│  - Section detection                        │
│  - Swedish to English label translation     │
└─────────────────────────────────────────────┘
                      │
┌─────────────────────────────────────────────┐
│            Export Layer                     │
│  - ProPresenter 6 XML generation            │
│  - File writing                             │
│  - Progress reporting                       │
│  - Error logging                            │
└─────────────────────────────────────────────┘
```

### Key Python Libraries
- **tkinter**: Built-in GUI framework
- **sqlite3**: Built-in SQLite support
- **striprtf**: RTF to text conversion (handles Unicode escapes)
- **xml.etree.ElementTree**: XML generation
- **pathlib**: File path handling
- **uuid**: GUID generation for ProPresenter
- **re**: Regular expressions for Bible verse detection
- **PyInstaller**: Create standalone executable
- **configparser**: Settings persistence
- **json**: Configuration file handling for section mappings

## Section Mappings Configuration

### Current Implementation (v1.2.0)
- **File**: `config/section_mappings.json`
- **Purpose**: Configurable Swedish to English section name translation
- **Structure**:
  ```json
  {
    "version": "1.1.0",
    "section_mappings": {
      "vers": "Verse",
      "refräng": "Chorus", 
      "brygga": "Bridge",
      "förrefräng": "Pre-Chorus"
    },
    "number_mapping_rules": {
      "preserve_numbers": true,
      "format": "{section_name} {number}"
    }
  }
  ```

### Sprint 9 Multi-Language Implementation (v2.0.0)
- **Embedded Default Mappings**: Languages hardcoded in EXE
- **User Language Selection**: Manual selection required
- **Settings Migration**: Automatic v1.2.0 → v2.0.0 migration with backup
- **Supported Languages**: Swedish, German, French, Spanish, Norwegian, Danish


## Development Status

### ✅ Completed Features (v1.1.0)
All core functionality has been implemented and tested:

#### Core Application Features
- **Database Integration**: Full EasyWorship 6.1 support (Songs.db & SongWords.db)
- **GUI Interface**: Modern Tkinter interface with menu system, search, and filtering
- **RTF Processing**: Complete RTF parsing with Swedish Unicode character support
- **Section Detection**: Automatic section detection and Swedish to English mapping
- **ProPresenter Export**: Full ProPresenter 6 XML generation with proper structure
- **Batch Operations**: Multi-threaded export with progress tracking and error handling

#### Advanced Features (v1.1.0)
- **Export Options Dialog**: Comprehensive formatting and output controls
- **Settings Persistence**: Complete application state management
- **Duplicate Handling**: Smart file conflict resolution with multiple options  
- **Version Management**: Configuration versioning and automatic migration
- **Windows Integration**: System font enumeration and proper file handling

### Sprint 6 Features ✅ COMPLETED (v1.1.0 - 2025-08-10)
1. **Complete Settings Persistence** ✅:
   - Last EasyWorship database path
   - Last export directory
   - Window size and position
   - Column widths in song list
   - Export preferences (folder structure, CCLI info options)
   - Select output directory on first run and then save it, no hardcoded default path.

2. **Export Options** ✅:
   - Output directory selection with browse
   - Enhanced Export Options dialog with Windows font loading
   - Master formatting control (enable/disable all custom formatting)
   - Font family selection from all available Windows fonts
   - Font size control (12-200, default: 72)
   - Line breaking configuration with natural slide breaks
   - Slide formatting options (intro/blank slides)
   - Enable blank page with group name "Intro" as first slide, and "Blank" as last

3. **Duplicate File Handling** ✅:
   - Detect existing files before export
   - Dialog with options: Skip/Overwrite/Rename/Apply to All
   - Custom rename functionality
   - "Apply to all" batch operations

4. **Version Management** ✅:
   - Section mappings version handling and migration
   - Settings schema versioning
   - Configuration backward compatibility

5. **Bug Fixes and Improvements** ✅:
   - Fixed window geometry startup errors
   - Fixed export method errors (create_presentation, prettify_xml)
   - Improved line breaking functionality
   - Enhanced error handling and user feedback
   - Better dialog sizing and button visibility


### Sprint 7 Features ✅ COMPLETED (v1.1.1 - 2025-08-11)
1. **Issue Fixes**:
   - ✅ Fixed database file dialog to show .db files (#6)
   - ✅ Fixed export failures and ValueError in duplicate handling (#7)
   - ✅ Improved font size selection with dropdown and extended range (#8)
   - ✅ Development coordination and issue resolution (#9)


### Sprint 8 Autodist
1. **Distribution Improvements**:
   - Auto-update checks
   - Installer creation, simpler installation
   - Better installation instructions for beginners
   - Enhanced About dialog with correct version information

### Sprint 9 More Language
2. **Multi-Language Section Support**:
   - German section mappings (vers → Verse, refrain → Chorus)
   - French section mappings (couplet → Verse, refrain → Chorus) 
   - Spanish section mappings (verso → Verse, coro → Chorus)
   - Norwegian/Danish section mappings
   - Auto-detection of source language in RTF content
   - Language-specific section detection patterns
   - Configurable language priority settings


### Future Enhancements
1. **Preview Functionality**:
   - Preview converted text before export
   - Show detected sections with labels
   - Display section mapping results
   - Edit text before export option 


## Issue Tracking

### GitHub Issues for Production Problems
Starting with v1.1.0, we use **GitHub Issues** to track problems that occur outside normal development cycles:

- **User-Reported Bugs**: Issues discovered during actual usage in production environments
- **Feature Requests**: Enhancement requests from real-world usage
- **Compatibility Issues**: Problems with different EasyWorship versions or ProPresenter imports
- **Performance Issues**: Real-world performance problems with large databases

**Current Open Issues**:
- None - All Sprint 7 issues have been successfully resolved

**Recently Closed Issues (v1.1.1)**:
- [#6](https://github.com/karllinder/ewexport/issues/6): ✅ Database file dialog doesn't show .db files
- [#7](https://github.com/karllinder/ewexport/issues/7): ✅ Export failures and ValueError in duplicate handling fixed
- [#8](https://github.com/karllinder/ewexport/issues/8): ✅ Font size selection UX improvements
- [#9](https://github.com/karllinder/ewexport/issues/9): ✅ Development coordination for Opus 4.1

**Issue Guidelines**:
- Issues should be **specific and reproducible**
- Include EasyWorship database version and song count
- Provide steps to reproduce the problem
- Include error messages and relevant logs
- Label appropriately: `bug`, `enhancement`, `user-feedback`


## Typical User Journey
1. User opens app
2. App auto-detects default EasyWorship path (or user browses)
3. App validates database files exist
4. Shows total song count and any warnings
5. User can search/filter/select songs
6. User chooses export location (default: Desktop/ProPresenter_Export)
7. User configures export options:
   - Folder structure preferences
   - CCLI info in filename
   - Section label language mapping
8. Clicks export with progress display
9. If duplicates found, user chooses action
10. Summary report shows successful/failed exports

## Performance Targets
- Load 1000 songs in < 2 seconds
- Search response < 100ms
- Export 100 songs in < 30 seconds
- Memory usage < 200MB for typical library
- UI remains responsive during export

## Version Compatibility
- **EasyWorship**: 6.1+ (database structure assumed consistent)
- **ProPresenter**: 6.x (primary target)
- **Windows**: 11 (primary), 10 (should work)
- **Python**: 3.8+ for development

## Testing Strategy

### Unit Tests
- RTF parsing with Swedish characters
- Section detection algorithms
- Swedish to English mapping
- XML generation validity

### Integration Tests
- Database access with various sizes
- Complete export pipeline
- Settings persistence

### Edge Cases to Test
- Empty database
- Database with 1 song
- Database with 10,000+ songs
- Songs with only title (no author/copyright) - **Very common case**
- Bible verse entries (e.g., "1 Mos 1:26-27")
- Multiple versions of same song (e.g., "Above all", "Above all 2")
- Song titles with hyphens and special formatting
- RTF with complex formatting
- Special characters in titles (/, \, :, *, ?, ", <, >, |)
- Very long song titles (>255 characters)
- Swedish characters throughout (å, ä, ö)
- Mixed language songs
- Songs without clear sections
- Corrupted RTF content (graceful handling)
- Empty metadata fields (no author, copyright, CCLI)

### Manual Testing
- Validation with sample EasyWorship databases
- ProPresenter 6 import verification
- Swedish church song libraries

## File Structure
```
ewexport/
├── .gitignore
├── README.md
├── requirements.txt
├── setup.py
├── config/
│   ├── default_settings.ini
│   └── section_mappings.json    # Swedish to English mappings
├── src/
│   ├── __init__.py
│   ├── main.py                  # Entry point
│   ├── gui/
│   │   ├── __init__.py
│   │   ├── main_window.py       # Tkinter GUI
│   │   └── dialogs.py           # Duplicate handling dialogs
│   ├── database/
│   │   ├── __init__.py
│   │   └── easyworship.py       # Database access
│   ├── processing/
│   │   ├── __init__.py
│   │   ├── rtf_parser.py        # RTF to text
│   │   ├── text_cleaner.py      # Text processing
│   │   └── section_detector.py  # Section identification
│   ├── export/
│   │   ├── __init__.py
│   │   └── propresenter.py      # ProPresenter generation
│   └── utils/
│       ├── __init__.py
│       ├── config.py            # Settings management
│       └── logger.py            # Logging setup
├── tests/
│   ├── test_rtf_parser.py
│   ├── test_section_detector.py
│   └── test_export.py
├── logs/
│   └── .gitkeep
└── build/
    └── .gitkeep
```

## Logging Strategy
- Log file location: `%APPDATA%/EWExport/logs/`
- Include: timestamp, action, success/failure, song details
- Rotation: Keep last 7 days
- Debug mode: Verbose RTF parsing details
- Error reports: Stack traces for debugging
- Export summary: List of successful and failed songs

## Distribution Strategy
- **PyInstaller**: Single exe file (no installation needed)
- **No code signing initially** (add later if needed for SmartScreen)
- **Manual updates** (check GitHub releases page)
- **Portable version** (no installation, settings in app folder)

## Technical Challenges Resolved
The following challenges have been successfully addressed in v1.1.0:

1. ✅ **RTF parsing complexity with Swedish characters** - Complete Unicode support
2. ✅ **Section detection from RTF formatting** - Advanced pattern matching implemented
3. ✅ **Swedish to English section mapping accuracy** - Configurable mapping system
4. ✅ **Maintaining formatting consistency** - Master formatting control system
5. ✅ **GUID generation for ProPresenter** - Proper UUID generation for all elements
6. ✅ **Handling large song libraries efficiently** - Multi-threaded processing with progress tracking
7. ✅ **Database working state validation** - Comprehensive validation and error handling

## Current Technical Debt
- UI could benefit from more modern styling (consider future migration to tkinter.ttk themes)
- Test coverage could be expanded for edge cases
- Documentation could include more user screenshots and examples

## Performance Metrics

### Target Performance
- Load 1000 songs: < 2 seconds
- Search response: < 100ms
- Export 100 songs: < 30 seconds
- Memory usage: < 200MB
- UI remains responsive during export

### Current Performance (v1.1.0)
- Load 1000 songs: ~1.5 seconds ✅
- Export 100 songs: ~15-20 seconds ✅
- Memory usage: < 150MB ✅
- GUI remains responsive during export ✅
- Search response: < 50ms ✅

## Settings Versioning & Migration

### Version History
- **v1.0.0**: Initial settings structure (no version field)
- **v1.2.0**: Added version field, Swedish mappings only
- **v2.0.0**: Multi-language support with migration system

### Migration Strategy
1. **Automatic Detection**: Check version field on startup
2. **Backup Creation**: Save `settings_backup_{timestamp}.json` before migration
3. **Progressive Migration**: Support path from any version to current
4. **Rollback Capability**: Restore from backup if migration fails
5. **Test Coverage**: Comprehensive test cases for each migration path

### Migration Test Cases
```python
# Required test scenarios:
- Migrate from no version → v2.0.0
- Migrate from v1.2.0 → v2.0.0  
- Handle corrupted settings file
- Verify backup creation
- Test rollback on failure
- Preserve user customizations
- Validate migrated data structure
```

## Dependencies

### Core Dependencies
- Python 3.8+
- tkinter (built-in)
- sqlite3 (built-in)
- striprtf (1.6+)

### Development Dependencies
- PyInstaller (5.0+) - For building executables
- pytest - For automated testing

## Success Criteria ✅ ACHIEVED
All original success criteria have been met in v1.1.0:

- ✅ Successfully read EasyWorship 6.1+ databases
- ✅ Display songs with Swedish characters correctly
- ✅ Accurate section detection and translation
- ✅ Export selected songs to ProPresenter 6 format
- ✅ Generated files open correctly in ProPresenter
- ✅ Section labels appear in English in ProPresenter
- ✅ Application runs smoothly on Windows 11
- ✅ Handle typical Swedish church song library (500-2000 songs)
- ✅ **Additional achievements**: Advanced export options, settings persistence, duplicate handling

## Current Focus (v1.1.0+)
The application is now in **production use**. Current focus areas:

1. **Issue Resolution**: Address user-reported problems via GitHub Issues
2. **User Experience**: Implement UX improvements based on real-world usage
3. **Stability**: Continue improving error handling and edge case coverage
4. **Performance**: Optimize for larger databases (5000+ songs)
5. **Documentation**: Maintain up-to-date user guides and troubleshooting

## Database Access Implementation Example

```python
import sqlite3
import re
from pathlib import Path
from striprtf.striprtf import rtf_to_text

class EasyWorshipDatabase:
    def __init__(self, db_path):
        self.db_path = Path(db_path)
        self.songs_db = self.db_path / "Songs.db"
        self.words_db = self.db_path / "SongWords.db"
        
        # Section markers to detect (already in English in EasyWorship!)
        self.section_markers = [
            'verse', 'chorus', 'bridge', 'pre-chorus', 
            'outro', 'tag', 'intro', 'ending'
        ]
    
    def get_all_songs(self):
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
        songs = cursor.fetchall()
        conn.close()
        
        return songs
    
    def get_song_lyrics(self, song_rowid):
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
    
    def parse_rtf_lyrics(self, rtf_content):
        """Convert RTF to text and detect sections"""
        if not rtf_content:
            return None
            
        # Convert RTF to plain text
        plain_text = rtf_to_text(rtf_content)
        
        # Split into lines
        lines = plain_text.split('\n')
        
        sections = []
        current_section = None
        current_content = []
        
        for line in lines:
            line_lower = line.strip().lower()
            
            # Check if this line is a section marker
            if line_lower in self.section_markers:
                # Save previous section if exists
                if current_section:
                    sections.append({
                        'type': current_section,
                        'content': '\n'.join(current_content).strip()
                    })
                
                # Start new section
                current_section = line_lower
                current_content = []
            else:
                # Add line to current section
                if line.strip():  # Skip empty lines
                    current_content.append(line)
        
        # Save last section
        if current_section:
            sections.append({
                'type': current_section,
                'content': '\n'.join(current_content).strip()
            })
        elif current_content:
            # No sections found, treat as single block
            sections.append({
                'type': 'verse',  # Default to verse
                'content': '\n'.join(current_content).strip()
            })
        
        return sections
    
    def get_songs_with_lyrics(self):
        """Get all songs with parsed lyrics"""
        songs = self.get_all_songs()
        
        for song in songs:
            song_dict = dict(song)
            rtf_lyrics = self.get_song_lyrics(song['rowid'])
            
            # Parse RTF and detect sections
            song_dict['sections'] = self.parse_rtf_lyrics(rtf_lyrics)
            
            # Handle display values for empty fields
            song_dict['display_author'] = song_dict['author'] or '-'
            song_dict['display_copyright'] = song_dict['copyright'] or '-'
            song_dict['display_ccli'] = song_dict['reference_number'] or '-'
            
            yield song_dict
```

## Production Notes (v1.1.0)
- **Target Environment**: Windows 10/11 with EasyWorship 6.1+ and ProPresenter 6.x
- **Primary Users**: Swedish churches with multilingual song libraries
- **Database Requirements**: Working SQLite databases (Songs.db & SongWords.db)
- **Export Format**: ProPresenter 6 XML format (human-readable, well-supported)
- **Font Handling**: Full Windows system font support with configurable sizing (12-200pt)
- **Performance Tested**: Libraries up to 2000+ songs with responsive UI
- **Character Support**: Complete Swedish Unicode support (å, ä, ö) throughout pipeline

## Development Process

### Branch Strategy
- `main`: Stable releases only
- `sprint*`: Feature development branches
- Create new branch for each sprint/major feature
- Merge to main via pull request after testing

### Release Process
1. Complete sprint features on feature branch
2. Run all tests
3. Update version in setup.py
4. Update README and CHANGELOG
5. Create pull request to main
6. Tag release after merge
7. Build executable with PyInstaller

### Code Standards
#### Python Style
- Follow PEP 8
- Type hints where beneficial
- Docstrings for public methods
- No inline comments unless necessary

#### Git Commits
- Clear, descriptive messages
- Reference sprint/issue numbers
- Include Co-Authored-By for AI assistance

### Testing Approach
#### Unit Tests
- RTF parser with various encodings
- Section detection accuracy
- Swedish character handling
- XML validation

#### Integration Tests
- Database to export pipeline
- Large database handling
- Edge cases (empty fields, special chars)

#### Manual Testing
- Test with real EasyWorship databases
- Verify ProPresenter import
- Swedish church song libraries

## Maintenance and Support
- **Issue Tracking**: GitHub Issues for production problems and feature requests
- **Version Control**: Git with tagged releases and proper branching strategy  
- **Documentation**: Maintained in CLAUDE.md (comprehensive technical documentation)
- **Testing**: Manual testing with real EasyWorship databases, automated tests for core functions
- **Distribution**: GitHub Releases with pre-built executables