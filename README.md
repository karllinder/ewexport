# EasyWorship to ProPresenter Converter

A Windows desktop application that converts songs from EasyWorship 6.1 database format to ProPresenter 6 format with full support for Swedish and English text.

## 🎉 Current Version: v0.1.1

**Status**: ✅ **Working** - The converter successfully exports songs from EasyWorship to ProPresenter 6 format.

## Features

### Core Functionality
- ✅ Read songs from EasyWorship 6.1 SQLite databases (Songs.db & SongWords.db)
- ✅ Export to ProPresenter 6 XML format (.pro6)
- ✅ Full Swedish character support (å, ä, ö)
- ✅ Automatic section detection (Verse, Chorus, Bridge, etc.)
- ✅ RTF text parsing and formatting
- ✅ Batch export multiple songs with progress tracking
- ✅ CCLI metadata preservation

### User Interface
- ✅ Simple and intuitive GUI with song list
- ✅ Auto-detection of EasyWorship database path
- ✅ Song selection with checkboxes
- ✅ Select All/None functionality
- ✅ Real-time selection counter
- ✅ Export progress bar with status updates
- ✅ Detailed export results dialog

## Completed Sprints

### Sprint 1: Research & Planning ✅
- Database structure analysis
- ProPresenter format research
- Architecture design

### Sprint 2: MVP GUI ✅
- Basic Tkinter interface
- Database connection
- Song list display

### Sprint 3: RTF Processing ✅
- RTF to text conversion
- Swedish character handling
- Section detection

### Sprint 4: ProPresenter Export ✅
- Complete XML generation
- Batch export functionality
- Progress tracking
- Error handling

### Upcoming Features (Sprint 5)

- Search and filter functionality
- Preview converted text before export
- Settings persistence
- Duplicate file handling
- Advanced export options

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

3. Select songs from the list using checkboxes or use Select All/None buttons

4. Choose an export location (default: Desktop/ProPresenter_Export)

5. Click "Export Selected Songs" to generate ProPresenter 6 files

The exported .pro6 files will be saved to your chosen directory and can be imported directly into ProPresenter 6.

## Acknowledgments

- Based on research from [ew61-export](https://github.com/jamesinglis/ew61-export) PHP implementation
- Designed for local Windows desktop use

## License

*To be determined*