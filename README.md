# EasyWorship to ProPresenter Converter

A Windows desktop application that converts songs from EasyWorship 6.1 database format to ProPresenter 6 format with full support for Swedish and English text.

## 🎉 Current Version: v1.0.0

The converter successfully exports songs from EasyWorship to ProPresenter 6 format with advanced features.

## Features

### Core Functionality
- ✅ Read songs from EasyWorship 6.1 SQLite databases (Songs.db & SongWords.db)
- ✅ Export to ProPresenter 6 XML format (.pro6)
- ✅ Full Swedish character support (å, ä, ö)
- ✅ Automatic section detection (Verse, Chorus, Bridge, etc.)
- ✅ Configurable Swedish to English section name mapping
- ✅ RTF text parsing with Unicode support
- ✅ Real-time search filtering across all song fields

### Using Section Mappings

Access the Section Mappings settings from the Edit menu to:
- Customize how Swedish section names are translated to English
- Add new language mappings
- Import/export mapping configurations
- Test translations with the preview feature

### Search Features

The search bar allows you to:
- Filter songs by title, author, copyright, or CCLI number
- View search history (last 10 searches)
- See filtered results count
- Clear search with one click


## Development Progress

### 🚀 Upcoming Features (Sprint 6)
- Complete settings persistence (window state, paths, preferences)
- Duplicate file handling with user choices
- Preview functionality before export


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

- Windows 11 
- Python 3.8 or higher
- EasyWorship 6.1 database files

## Installation

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
python srun.py
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