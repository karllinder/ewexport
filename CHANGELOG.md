# Changelog

All notable changes to the EasyWorship to ProPresenter Converter project will be documented in this file.

## [1.2.5] - 2026-08-17

### 🐛 Bug Fix - Remove Local Config Folder Creation

This release completely removes the creation of local "config" folders and ensures all configuration files are stored in %APPDATA%\EWExport.

### 🔧 Bug Fix

#### Local Config Folder Creation
- **Fixed:** Application was creating unwanted "config" folder in working directory
- **Fixed:** section_mappings.json file being created in current directory
- **Root Cause:** Multiple hardcoded references to local "./config" paths
- **Solution:** All config files now saved to %APPDATA%\EWExport exclusively
- **Impact:** No more spurious config folders created in user's working directory

### 📝 Technical Details
- Removed all hardcoded references to local "config" folder paths
- Updated `config.py` to use APPDATA for section_mappings.json
- Updated `settings_window.py` to save to APPDATA directory
- Updated `section_detector.py` to load from APPDATA directory
- Updated `main.py` to create default section mappings in APPDATA
- Simplified config creation logic - no more development vs packaged app detection

### ✅ Config File Locations (All in %APPDATA%\EWExport)
- **settings.json**: Application settings
- **section_mappings.json**: Swedish to English section mappings
- **logs/**: Log files directory

### 🙏 Credits
- Karl Linder - Development and testing

## [1.2.4] - 2026-08-17

### 🐛 Bug Fix - First Slide Export Option

This release fixes the First Slide export option that was not working in Export Options.

### 🔧 Bug Fix

#### First Slide Export Option
- **Fixed:** First Slide option in Export Options was not working
- **Root Cause:** Code was only adding intro slides if they had text content, but users want to add blank first slides
- **Solution:** Allow intro slides to be added even when text is empty (for title slides or blank slides)
- **Impact:** First Slide option now works correctly and adds intro slides as intended

### 📝 Technical Details
- Removed text content requirement for intro slide creation
- Updated `create_slide_group` method to handle intro slides like blank slides
- Allow empty content for both 'intro' and 'blank' slide types
- First slides can now be used as title slides or blank intro slides

### ✅ Confirmed Working
- **First Slide**: Now creates intro slides even with empty text
- **Last Slide**: Continues to work as expected
- **Font Changes**: Continue to work as expected

### 🙏 Credits
- Karl Linder - Development and testing

## [1.2.3] - 2026-08-17

### 🐛 Bug Fix - Database Auto-Loading

This release fixes the database auto-loading issue that was still present in v1.2.2.

### 🔧 Bug Fix

#### Database Auto-Loading (Final Fix)
- **Fixed:** Database still required manual "Load Songs" button press on startup
- **Root Cause:** `load_saved_paths()` method was setting the database path but not calling `load_songs()`
- **Solution:** Created new `auto_load_database()` method that properly handles both saved paths and auto-detection
- **Impact:** Database now auto-loads correctly on startup without requiring manual button press

### 📝 Technical Details
- Replaced separate `auto_detect_easyworship()` and `load_saved_paths()` calls with unified `auto_load_database()` method
- Prioritizes saved database path over auto-detection
- Ensures `load_songs()` is called when valid database is found
- Prevents duplicate loading calls

### 🙏 Credits
- Karl Linder - Development and testing

## [1.2.2] - 2026-08-17

### 🐛 Bug Fixes - Database Loading and Version Display

This release fixes several regression issues introduced in v1.2.1.

### 🔧 Bug Fixes

#### Database Auto-Loading
- **Fixed:** Database no longer auto-loads on startup after encoding fix
- **Root Cause:** SQLite connection method needed string conversion for Path objects
- **Solution:** Ensure proper Path to string conversion in `_get_connection` method
- **Impact:** Database now auto-loads correctly when EasyWorship path is detected

#### Version Display
- **Fixed:** Application showing version 1.2.0 instead of current version
- **Root Cause:** Multiple hardcoded version strings not updated consistently
- **Solution:** Updated all version references throughout the codebase
- **Impact:** Version now displays correctly as 1.2.2 in About dialog and update checker

#### Config Folder Creation
- **Fixed:** Unwanted "config" folder created in working directory
- **Root Cause:** Settings window creating config folder without checking if it's needed
- **Solution:** Only create config folder in development mode, use bundled config in packaged app
- **Impact:** No more spurious config folders in user's working directory

### 📝 Technical Details
- Fixed Path object handling in SQLite connections
- Updated version strings in setup.py, update_checker.py, main_window.py, version_info.py, and build.py
- Improved config folder creation logic to respect packaged app structure
- Added proper logging for config handling issues

### 🙏 Credits
- Karl Linder - Development and testing

## [1.2.1] - 2026-08-17

### 🐛 Critical Bug Fix - Cross-Platform Encoding

This release fixes a critical encoding issue that caused Swedish characters (å, ä, ö) to display incorrectly on macOS when working with EasyWorship databases created on Windows.

### 🔧 Bug Fixes

#### Issue #16: Swedish Character Encoding on macOS
- **Fixed:** Swedish characters displaying as corrupted/scrambled text on macOS
- **Root Cause:** SQLite connections were not handling Windows-1252 encoding correctly on non-Windows platforms
- **Solution:** Added intelligent encoding detection and conversion in database layer
- **Implementation:** New `_get_connection` method with platform-specific text factory
- **Impact:** Swedish characters now display correctly across all platforms (Windows, macOS, Linux)

### 📝 Technical Details
- Added platform detection to handle encoding differences
- SQLite connections now use custom text factory on non-Windows platforms
- Graceful fallback chain: UTF-8 → Windows-1252 → UTF-8 with replacement
- No changes required to RTF parser or ProPresenter export (already UTF-8 compliant)

### ✅ Issues Resolved
- [#16](https://github.com/karllinder/ewexport/issues/16): Swedish characters displaying incorrectly on macOS

### 🙏 Credits
- Karl Linder - Development and testing

## [1.2.0] - 2025-01-14

### 🚀 Manual Release System & Build Improvements

This release introduces a comprehensive manual build and release system to eliminate antivirus false positives and provides better control over the distribution process.

### ✨ New Features

#### Manual Build and Release System
- **Local Build Process**: New `build_and_release.py` script for complete build automation
- **Upload Tool**: `upload_release.py` for uploading to existing GitHub releases
- **GitHub Actions Update**: Now creates draft releases only, no more problematic automated builds
- **SHA256 Verification**: Automatic hash calculation and verification for file integrity
- **Release Documentation**: Comprehensive `RELEASE_PROCESS.md` with step-by-step instructions

#### Antivirus Compatibility Improvements
- **Trusted Environment Builds**: Local builds from development machines significantly reduce false positives
- **Optimized Build Configuration**: Enhanced `build_clean.py` with better antivirus mitigation
- **Security Documentation**: Updated ANTIVIRUS.md with latest guidance
- **File Verification**: SHA256 hashes included in all releases for integrity verification

### 🔧 Technical Improvements

#### Build System
- **Clean Build Environment**: Automated cleanup of build artifacts
- **Dependency Optimization**: Better module exclusion for smaller, cleaner executables
- **Version Consistency**: Automatic version detection from setup.py
- **Error Handling**: Comprehensive error reporting and recovery procedures

#### Release Process
- **Draft Release Creation**: GitHub Actions creates draft releases with proper release notes
- **Manual Upload Workflow**: Streamlined process for uploading locally-built executables
- **Release Notes Automation**: Automatic extraction from CHANGELOG.md
- **Security Information**: Automatic inclusion of antivirus guidance in release descriptions

### 📚 Documentation
- **RELEASE_PROCESS.md**: Complete guide for maintainers
- **Build Scripts**: Comprehensive comments and error handling
- **Troubleshooting**: Solutions for common build and release issues
- **Security Guidelines**: Best practices for avoiding false positives

### 🛡️ Security & Reliability
- **Local Build Verification**: Multiple verification steps before release
- **Hash-Based Integrity**: SHA256 verification for all distributed files
- **Trusted Build Environment**: Builds from known, secure development machines
- **Emergency Procedures**: Documented processes for handling security issues

### 💡 Benefits
- **Reduced False Positives**: Local builds have significantly lower antivirus detection rates
- **Better Quality Control**: Manual oversight of each release
- **Faster Release Process**: No waiting for GitHub Actions to build
- **Improved User Trust**: SHA256 hashes and clear security documentation

## [1.1.6] - 2025-01-14

### 🛡️ Antivirus False Positive Mitigation

This release focuses on reducing false positive detections from antivirus software.

### ✨ Improvements
- **Clean Build Process**: Optimized PyInstaller configuration to reduce AV false positives
- **No UPX Compression**: Disabled UPX compression which often triggers antivirus warnings
- **Reduced Module Inclusion**: Excluded unnecessary Python modules to create cleaner executable
- **Windows Metadata**: Added proper version information and manifest
- **Documentation**: Added comprehensive ANTIVIRUS.md guide for users and IT administrators

### 📚 Documentation
- Added ANTIVIRUS.md with detailed information about false positives
- Instructions for whitelisting and verification
- Enterprise deployment guidelines
- Alternative solutions for persistent AV issues

### 🔧 Technical Changes
- Created `ewexport_clean.spec` with optimized PyInstaller settings
- Updated `build_clean.py` with antivirus-friendly build process
- Excluded cryptographic and network modules not needed for operation
- Added SHA256 hash verification support

## [1.1.5] - 2025-01-14

### 🐛 Bug Fixes
- **Remove Non-Functional Subfolder Export Option** (#13): Removed the broken subfolder export feature from Export Options dialog as it was not implemented in the export logic and added unnecessary complexity

### 🔧 Technical Improvements
- Simplified Export Options dialog by removing unused UI elements
- Cleaned up configuration settings by removing subfolder-related options
- Reduced code complexity and potential confusion for users

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