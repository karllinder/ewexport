# Changelog

All notable changes to the EasyWorship to ProPresenter Converter project will be documented in this file.

## [1.1.3] - 2025-01-13

### 🚀 Auto-Distribution System

This release introduces a comprehensive auto-distribution system with automated installation, update checking, and executable build pipeline.

### ✨ New Features

#### PowerShell Installation Script
- **Automated Setup**: Complete installation with Python detection and setup
- **GitHub Integration**: Downloads latest release from GitHub API
- **Desktop Shortcuts**: Automatic shortcut creation
- **Dependency Management**: Installs required packages (striprtf, packaging)
- **Flexible Options**: Custom installation paths and silent mode

#### Update Checking System
- **Check for Updates Menu**: New menu item in Help menu
- **Automatic Checks**: Configurable startup update checking
- **GitHub API Integration**: Version comparison against latest releases
- **User Preferences**: Persistent settings for update notifications
- **Direct Downloads**: Opens browser to latest release page

#### Executable Build System
- **PyInstaller Integration**: Single-file Windows executable creation (~12 MB)
- **Build Scripts**: `build.py` Python script and `build.bat` Windows wrapper
- **GitHub Actions**: Automated builds on version tags
- **Release Automation**: Automatic GitHub release creation with exe attachment

### 🔧 Technical Improvements

#### Build Infrastructure
- **GitHub Actions Workflow**: `.github/workflows/build-release.yml`
- **Automated Releases**: Trigger on version tags (v*)
- **Windows Builds**: Native Windows executable generation
- **Error Handling**: Improved build script permission handling

#### Documentation
- **INSTALL.md**: Comprehensive installation guide
- **Build Instructions**: Added to README.md
- **Security Guidance**: Safe installation practices
- **Troubleshooting**: Common issues and solutions

### 🐛 Bug Fixes
- **ConfigManager Compatibility**: Fixed `get_bool` method error in update checker
- **Build Permissions**: Better handling of file access during builds
- **Settings Persistence**: Proper method calls for configuration saving

### 📦 Dependencies
- Added `packaging>=23.0` for version comparison

---

## [1.1.2] - 2025-01-11

### 🎨 UI and Export Improvements

This patch release improves the Export Options dialog and fixes a critical bug where First/Last slides were not being added to the ProPresenter export.

### 🔧 Bug Fixes & Improvements

#### Export Options - First/Last Slides
- **Fixed:** First and Last slides were not being added to the ProPresenter XML export despite being configured
- **Fixed:** Blank slide creation was failing due to empty content handling
- **Improvement:** Renamed "Intro Slide" to "First Slide" for better clarity
- **Improvement:** Renamed "Blank Slide" to "Last Slide" for better clarity
- **Implementation:** Added proper configuration reading in ProPresenter exporter
- **Implementation:** Added support for custom group names for First/Last slides
- **Impact:** First and Last slides now work correctly and are properly exported to ProPresenter format

### 📝 Technical Details
- Modified `create_pro6_document` method to check for First/Last slide configuration
- Added `custom_name` parameter to `create_slide_group` method
- Improved handling of blank slides with empty content
- Added 'blank' section type to color and name mappings

---

## [1.1.1] - 2025-01-11

### 🐛 Bug Fix Release

This patch release addresses critical bugs reported by users and improves the overall user experience. All issues were identified through real-world usage and reported via GitHub Issues.

### 🔧 Bug Fixes

#### Issue #7: Export Failures and Duplicate Handling
- **Fixed:** Export failures for songs with IDs 2727, 2728, 2729
- **Fixed:** ValueError when handling duplicate files during batch export
- **Improvement:** Enhanced error handling to provide more descriptive error messages
- **Improvement:** Better logging for debugging export issues
- **Improvement:** Robust duplicate file detection using file path indexing
- **Impact:** Songs that previously failed to export now work correctly, duplicate handling is reliable

#### Issue #6: Database File Selection Dialog
- **Fixed:** File dialog now displays .db files when selecting EasyWorship database
- **Improvement:** Changed from directory-only selection to file selection dialog
- **Improvement:** Users can now see Songs.db and SongWords.db files to confirm correct folder
- **Improvement:** Added validation warning if required database files are missing
- **Impact:** Much easier for users to locate and select the correct database folder

#### Issue #8: Font Size Selection UX
- **Fixed:** Replaced difficult-to-use spinbox with dropdown combobox
- **Improvement:** Added common font sizes for quick selection (12, 18, 24, 36, 48, 60, 72, 84, 96, 120, 144, 168, 200)
- **Improvement:** Extended font size range from 12-120 to 12-200 for large projection displays
- **Improvement:** Allow custom font size entry with validation
- **Impact:** Significantly improved user experience when selecting font sizes

### 📝 Technical Improvements
- Enhanced error logging throughout the export pipeline
- Improved data consistency between database reads and exports
- Better handling of edge cases in RTF parsing
- More robust file system error handling

### ✅ Issues Resolved
- [#6](https://github.com/karllinder/ewexport/issues/6): Database file dialog improvements
- [#7](https://github.com/karllinder/ewexport/issues/7): Export failures and duplicate handling
- [#8](https://github.com/karllinder/ewexport/issues/8): Font size selection UX
- [#9](https://github.com/karllinder/ewexport/issues/9): Development coordination (meta-issue)

---

## [1.1.0] - 2025-08-10

### 🎉 Major Feature Update - Enhanced Export Options and Settings Management

This release focuses on improving the user experience with comprehensive export options, better settings management, and numerous bug fixes based on user feedback.

### ✨ New Features

#### Enhanced Export Options Dialog
- **Windows Font Integration**: Complete system font enumeration from all available Windows fonts
- **Master Formatting Control**: Single checkbox to enable/disable all custom formatting options
- **Extended Font Size Range**: Configurable font size from 12-200 (increased from 12-120)
- **Improved Dialog Layout**: Larger dialog (650x600) with better button visibility and organization
- **Font Family Selection**: Dropdown with all system fonts (excluding vertical fonts)

#### Advanced Line Breaking System
- **Natural Slide Breaks**: Empty lines in lyrics always create new slides, preserving song structure
- **Configurable Line Limits**: Set maximum lines per slide (default: 4)
- **Smart Auto-Breaking**: 
  - When enabled: Automatically splits slides exceeding line limit
  - When disabled: Preserves natural slides intact
- **Improved Text Processing**: Better handling of line breaks in RTF and WinFlow data

#### Complete Settings Persistence
- **First-Run Experience**: Guided setup for default export directory
- **Window State Management**: Save and restore window size, position, and maximized state
- **Column Width Persistence**: Remember song list column widths
- **Path Memory**: Automatically remember last database and export paths
- **Export Preferences**: Persistent folder structure and CCLI filename options

#### Enhanced Duplicate File Handling
- **Smart Detection**: Automatically detect existing files before export
- **Multiple Options**: Skip, Overwrite, Rename (auto), or Custom Name
- **Batch Operations**: "Apply to All" option for handling multiple duplicates
- **Custom Naming**: Manual filename entry with validation

#### Configuration Version Management
- **Schema Versioning**: Settings include version tracking (v1.1.0)
- **Automatic Migration**: Seamless upgrade from older configuration formats
- **Section Mappings Versioning**: Version handling for section_mappings.json
- **Backward Compatibility**: Maintains compatibility with existing settings

### 🔧 Improvements

#### User Interface
- **Larger Export Options Dialog**: Increased from 600x500 to 650x600
- **Better Button Layout**: Clear Save, Apply, and Cancel buttons with proper positioning
- **Tabbed Organization**: Formatting settings moved to dedicated tab
- **Enhanced Controls**: Master formatting toggle affects all related controls

#### Configuration Defaults
- **Font Size**: Default changed from 48 to 72 points for better visibility
- **Subfolder Creation**: Disabled by default to reduce clutter
- **Formatting**: Custom formatting disabled by default for simplicity

### 🐛 Major Bug Fixes

#### Critical Export Issues
- **Window Geometry Error**: Fixed `TclError: bad geometry specifier` on startup
- **Missing Methods**: Fixed `AttributeError: 'ProPresenter6Exporter' has no attribute 'create_presentation'`
- **XML Processing**: Fixed missing `prettify_xml` method with inline XML formatting
- **Settings Application**: Fixed font and line break settings not affecting exported files

#### User Interface Fixes
- **Column Width Saving**: Fixed error when closing application with column width persistence
- **Dialog Visibility**: Fixed Export Options dialog buttons not being visible
- **RTF Font Processing**: Corrected font size calculation (now properly uses half-points)

### 📝 Configuration Changes
- **Default Settings**: Updated default values for better user experience
- **New Settings**: Added `formatting_enabled` master control and `change_font` override
- **Version Tracking**: All configuration files now include version information

### 🔄 Technical Improvements
- **Windows Font Enumeration**: Using `tkinter.font.families()` for system font detection
- **Enhanced RTF Generation**: Dynamic font settings in RTF and WinFlow data
- **Better Error Handling**: Improved user feedback and error recovery
- **Configuration Management**: Robust settings migration and validation system

### 📋 Known Issues Identified
- Database file selection dialog doesn't show .db files (#6)
- Export failures for specific song IDs 2727, 2728, 2729 (#7) 
- Font size selection UX could be improved with dropdown (#8)

---

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
- Complete project documentation (CLAUDE.md)
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