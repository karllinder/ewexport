# Changelog

All notable changes to the EasyWorship to ProPresenter Converter project will be documented in this file.

## [1.0.0] - 2025-08-09

### 🎉 First Production Release

This is the first stable production release of the EasyWorship to ProPresenter Converter, featuring a complete solution for converting worship songs from EasyWorship 6.1 to ProPresenter 6 format.

### ✨ Features

#### Core Functionality
- Full EasyWorship 6.1 database support (Songs.db & SongWords.db)
- ProPresenter 6 XML format generation
- RTF text parsing with Swedish character support (å, ä, ö)
- Automatic section detection (Verse, Chorus, Bridge, etc.)
- Batch export with multi-threading
- CCLI metadata preservation

#### User Interface
- Modern GUI with menu system (File, Edit, Help)
- Auto-detection of EasyWorship database path
- Real-time search and filtering
- Search history (last 10 searches)
- Song selection with checkboxes
- Export progress tracking
- Detailed export results dialog

#### Advanced Features
- **Settings GUI for Section Mappings**
  - Table view for managing Swedish to English translations
  - Add, edit, delete mappings
  - Real-time preview and testing
  - Import/export configurations
  - Reset to defaults option

- **Search & Filter System**
  - Live filtering across all song fields
  - Persistent search history
  - Result count display
  - Clear search functionality

#### Error Handling
- Clear error messages for empty/corrupt songs
- Proper handling of invalid filenames
- Graceful handling of songs with newline characters in titles
- Detailed export failure reporting

### 🐛 Bug Fixes
- Fixed errno 22 issues with invalid filenames
- Resolved newline characters in song titles
- Improved empty/blank song handling
- Fixed RTF parsing warnings for empty content
- Corrected section number formatting (e.g., "Verse 1")

### 📚 Documentation
- Comprehensive README with features and usage
- Development documentation (DEVELOPMENT.md)
- Project documentation (CLAUDE.md)
- Code comments and docstrings

### 🔧 Technical Details
- Python 3.8+ with Tkinter GUI
- SQLite database access
- striprtf library for RTF parsing
- XML generation for ProPresenter format
- Multi-threaded export processing
- Settings persistence in JSON format

---

## [0.1.1] - 2025-08

### Fixed
- RV Slide Group naming with section numbers
- Extra line feed removal from slide content
- Configurable section mappings

### Added
- config/section_mappings.json for translation settings

---

## [0.1.0] - 2025-08

### Added
- Initial beta release
- Basic ProPresenter 6 export functionality
- RTF parsing with Swedish character support
- Basic GUI with song list
- Database connection and song display