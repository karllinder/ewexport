# EasyWorship to ProPresenter Converter

A Windows desktop application that converts songs from EasyWorship 6.1 database format to ProPresenter 6 format with full support for Swedish and English text.

## 🎉 Current Version: v1.0.0

**Status**: ✅ **Production Ready** - The converter successfully exports songs from EasyWorship to ProPresenter 6 format with advanced features.

## Features

### Core Functionality
- ✅ Read songs from EasyWorship 6.1 SQLite databases (Songs.db & SongWords.db)
- ✅ Export to ProPresenter 6 XML format (.pro6)
- ✅ Full Swedish character support (å, ä, ö)
- ✅ Automatic section detection (Verse, Chorus, Bridge, etc.)
- ✅ Configurable Swedish to English section name mapping
- ✅ RTF text parsing with Unicode support
- ✅ Batch export multiple songs with progress tracking
- ✅ CCLI metadata preservation
- ✅ Multi-threaded export to maintain UI responsiveness

### User Interface
- ✅ Modern GUI with menu bar (File, Edit, Help)
- ✅ Auto-detection of EasyWorship database path
- ✅ Real-time search filtering across all song fields
- ✅ Search history with last 10 searches
- ✅ Song selection with checkboxes
- ✅ Select All/None functionality
- ✅ Real-time selection and result counters
- ✅ Export progress bar with per-song status
- ✅ Detailed export results dialog
- ✅ Automatic selection clearing after export

### Advanced Features
- ✅ **Settings GUI for Section Mappings**
  - Table view of all mappings
  - Add, edit, delete mappings
  - Real-time preview and testing
  - Import/export configurations
  - Reset to defaults option
- ✅ **Search & Filter System**
  - Live search as you type
  - Search across title, author, copyright, CCLI
  - Persistent search history
  - Clear search button
  - Result count display

## Development Progress

### ✅ Completed Features
- **Sprint 1**: Research & Planning - Database structure analysis, format research
- **Sprint 2**: MVP GUI - Basic interface, database connection, song display
- **Sprint 3**: RTF Processing - Unicode handling, section detection, text cleaning
- **Sprint 4**: ProPresenter Export - XML generation, batch export, progress tracking
- **Sprint 5**: Search & Settings - Real-time filtering, section mapping GUI, menu system

### 🚀 Upcoming Features (Sprint 6)
- Complete settings persistence (window state, paths, preferences)
- Export options dialog (folder structure, CCLI options)
- Duplicate file handling with user choices
- Preview functionality before export
- Edit text before export option

### 🔮 Future Enhancements
- Bible verse detection and special handling
- Multi-language support (German, French, Spanish)
- Export statistics and reporting
- Advanced search with regex support
- Batch operations by tags or date range

## Technology Stack

- Python 3.x
- Tkinter (GUI)
- SQLite3 (Database access)
- XML generation for ProPresenter format

## Requirements

- Windows 11 (primary target)
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
python src/main.py
```

2. The application will auto-detect your EasyWorship database location, or you can browse to select it manually

3. Use the search bar to filter songs or browse the full list

4. Select songs from the list using checkboxes or use Select All/None buttons

5. Configure section mappings via Edit → Section Mappings (optional)

6. Choose an export location (default: Desktop/ProPresenter_Export)

7. Click "Export Selected Songs" to generate ProPresenter 6 files

The exported .pro6 files will be saved to your chosen directory and can be imported directly into ProPresenter 6.

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

## Acknowledgments

- Based on research from [ew61-export](https://github.com/jamesinglis/ew61-export) PHP implementation
- Designed for local Windows desktop use

## License

*To be determined*