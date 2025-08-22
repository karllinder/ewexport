# EasyWorship to ProPresenter Converter

A Windows desktop application that converts songs from EasyWorship 6.1 database format to ProPresenter 6 format with full support for Swedish and English text.

## 🎉 Current Version: v1.2.5

The converter successfully exports songs from EasyWorship to ProPresenter 6 format with advanced formatting controls and customization options.

## Features

### Core Functionality
- ✅ Read songs from EasyWorship 6.1 SQLite databases (Songs.db & SongWords.db)
- ✅ Export to ProPresenter 6 XML format (.pro6)
- ✅ Full Swedish character support (å, ä, ö)
- ✅ Automatic section detection (Verse, Chorus, Bridge, etc.)
- ✅ Configurable Swedish to English section name mapping
- ✅ RTF text parsing with Unicode support
- ✅ Real-time search filtering across all song fields
- ✅ Custom font selection from all Windows system fonts
- ✅ Configurable slide formatting and line breaks
- ✅ Duplicate file detection and handling
- ✅ Complete settings persistence

### Using Section Mappings

Access the Section Mappings settings from the Edit menu to:
- Customize how Swedish section names are translated to English
- Add new language mappings
- Import/export mapping configurations
- Test translations with the preview feature

### Export Options

Access Export Options from the Edit menu to configure:
- **Font Settings**: Choose from all available Windows fonts and set custom font size
- **Line Breaking**: Control how lyrics are split across slides
- **File Naming**: Include CCLI number or author in filenames
- **Duplicate Handling**: Choose to skip, overwrite, or rename duplicates

#### Line Breaking and Slide Formatting

The "Automatically break long lines" setting controls how content is divided into slides:

**How it works:**
1. **Natural Slide Breaks**: Empty lines in the lyrics always create new slides
2. **Maximum Lines Per Slide**: Set how many lines appear on each slide (default: 4)

**When "Automatically break long lines" is ON:**
- Slides with more lines than the maximum are automatically split
- Example: An 8-line verse with max=4 creates 2 slides (4 lines each)

**When "Automatically break long lines" is OFF:**
- Natural slides are kept intact regardless of line count
- Only empty lines create new slides
- Example: An 8-line verse stays as 1 slide with all 8 lines

### Search Features

The search bar allows you to:
- Filter songs by title, author, copyright, or CCLI number
- View search history (last 10 searches)
- See filtered results count
- Clear search with one click


## Development Progress

### 🚀 Latest Updates (v1.1.2)
- ✅ Complete settings persistence (window state, paths, preferences)
- ✅ Enhanced Export Options dialog with font and formatting controls
- ✅ Duplicate file detection with user-friendly handling
- ✅ Windows system font integration
- ✅ Configurable line breaking and slide formatting
- ✅ Improved first-run experience

### 🔧 Upcoming Features
- Preview functionality before export
- Edit text before export option


### 🔮 Future Enhancements
- Multi-language support (German, French, Spanish)
- Advanced search
- Edit text before export option

## Technology Stack

- Python 3.x
- Tkinter (GUI)
- SQLite3 (Database access)
- XML generation for ProPresenter format

## Requirements

- Windows 10 or 11
- EasyWorship 6.1 database files
- That's it! (The executable includes everything else)

## Installation

### Option 1: Download Executable (Easiest - No Installation Required!)
1. Go to [Releases](https://github.com/karllinder/ewexport/releases/latest)
2. Download `ewexport.exe` 
3. Run it from anywhere - it's completely standalone!

The executable includes Python and all dependencies. Nothing else needed!

**Note**: Some antivirus software may flag the executable as a false positive. This is common with PyInstaller apps. If you encounter this:
1. Verify the SHA256 hash from the release page
2. Add an exception for ewexport.exe in your antivirus
3. Report it as a false positive to your antivirus vendor

### Option 2: Automated Installation
See [INSTALL.md](INSTALL.md) for detailed installation instructions including automated setup script.

### Option 3: Run from Source
1. Clone the repository:
```bash
git clone https://github.com/karllinder/ewexport.git
cd ewexport
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Quick Start

### Running from Source

1. Run the application:
```bash
python run.py
```

2. The application will auto-detect your EasyWorship database location, or you can browse to select it manually

3. Use the search bar to filter songs or browse the full list

4. Select songs from the list using checkboxes or use Select All/None buttons

5. Configure section mappings via Edit → Section Mappings (optional)

6. Choose an export location (default: Desktop/ProPresenter_Export)

7. Click "Export Selected Songs" to generate ProPresenter 6 files

The exported .pro6 files will be saved to your chosen directory and can be imported directly into ProPresenter 6.



## Acknowledgments

- Based on research from [ew61-export](https://github.com/jamesinglis/ew61-export) PHP implementation


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### MIT License Summary

This software is provided free of charge with the following permissions:
- ✅ Commercial use
- ✅ Modification
- ✅ Distribution
- ✅ Private use

The only requirements are:
- Include the original copyright notice
- Include the license text

The software is provided "as is", without warranty of any kind.

## Building from Source

### Creating the Executable

#### Quick Build (Windows)
Simply run:
```batch
build.bat
```

#### Manual Build
```bash
# Install PyInstaller
pip install pyinstaller

# Run build script
python build_scripts/build.py
```

The executable will be created in the `dist` folder.

### Automated Releases

This project uses GitHub Actions for automated builds. When you push a version tag, it automatically:
1. Builds the Windows executable
2. Creates a GitHub release
3. Uploads the executable as a release asset

To create a new release:
```bash
git tag v1.1.3
git push origin v1.1.3
```

## Support

Report issues at: [GitHub Issues](https://github.com/karllinder/ewexport/issues)