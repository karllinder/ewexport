# Release Notes

## Version 1.1.0 (2025-01-10)

### 🎉 New Features

#### Export Options Dialog
- **Custom Font Selection**: Choose from all available Windows system fonts
- **Font Size Control**: Set custom font size (default: 72)
- **Master Formatting Control**: Enable/disable all custom formatting with one checkbox
- **Line Breaking Configuration**: Control how lyrics are split across slides

#### Enhanced Settings Management
- **Complete Settings Persistence**: Window geometry, column widths, and all preferences are saved
- **Version-Aware Configuration**: Settings include version tracking for future migrations
- **First-Run Experience**: Guided setup for default export directory on first launch

#### Duplicate File Handling
- **Smart Detection**: Automatically detects existing files before export
- **User-Friendly Options**: Skip, Overwrite, Rename, or use Custom Name
- **Batch Operations**: "Apply to All" option for handling multiple duplicates
- **Confirmation Dialogs**: Prevents accidental data loss

### 🔧 Improvements

#### Line Breaking and Slide Formatting
The "Automatically break long lines" feature now works correctly:

- **Natural Slide Breaks**: Empty lines in lyrics always create new slides, preserving song structure
- **Maximum Lines Per Slide**: Configurable limit (default: 4 lines per slide)
- **Smart Breaking**: 
  - When ON: Automatically splits slides that exceed the maximum line count
  - When OFF: Preserves natural slides intact, only empty lines create breaks
- **Example**: An 8-line verse with max=4 lines:
  - Auto-break ON: Creates 2 slides (4 lines each)
  - Auto-break OFF: Keeps as 1 slide (all 8 lines)

#### User Interface
- **Larger Export Options Dialog**: Increased from 600x500 to 650x600 for better visibility
- **Improved Button Layout**: Clear Save, Apply, and Cancel buttons with proper positioning
- **Better Organization**: Formatting settings moved to dedicated tab
- **Windows Font Integration**: Dropdown shows all available system fonts (excluding vertical fonts)

### 🐛 Bug Fixes
- Fixed window geometry error on startup (`TclError: bad geometry specifier`)
- Fixed missing `create_presentation` method error during export
- Fixed missing `prettify_xml` method error
- Fixed column width saving error when closing application
- Fixed font and line break settings not being applied to exported files
- Fixed RTF font size calculation (now properly uses half-points)

### 📝 Configuration Changes
- Default font size changed from 48 to 72
- "Create subfolder for export" now disabled by default
- Added `formatting_enabled` master control setting
- Added `change_font` setting for font override control

### 🔄 Technical Improvements
- Proper XML formatting with inline processing
- Enhanced RTF data generation with configurable fonts
- Improved WinFlow data with dynamic font settings
- Better error handling and user feedback

## Version 1.0.0 (2025-01-08)

### Initial Release
- Core functionality for converting EasyWorship 6.1 songs to ProPresenter 6 format
- Swedish to English section mapping
- Song selection and search functionality
- Basic export capabilities