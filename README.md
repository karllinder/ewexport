# EasyWorship to ProPresenter Converter

A Windows desktop application that converts songs from EasyWorship 6.1 database format to ProPresenter format with a simple graphical user interface.

## Features

- Read songs from EasyWorship 6.1 SQLite databases
- Simple GUI for song selection
- Export to ProPresenter 6 XML format (.pro6)
- Batch export multiple songs
- RTF text processing and formatting

## Status

🚧 **Under Development** - Sprint 2 Complete (MVP GUI Implementation)

### Completed Features (Sprint 2)
- ✅ Basic Tkinter GUI with song list
- ✅ SQLite database connection
- ✅ Auto-detection of EasyWorship database path
- ✅ Display songs with metadata (Title, Author, Copyright, CCLI)
- ✅ Song selection with checkboxes
- ✅ Select All/None functionality
- ✅ Real-time selection counter

### Upcoming Features

- **Sprint 3**: RTF parsing and ProPresenter export
- **Sprint 4**: Advanced options and batch operations
- **Sprint 5**: Search, filtering, and settings persistence

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

## Usage

1. Run the application:
```bash
python run.py
```

2. The application will auto-detect your EasyWorship database location, or you can browse to select it manually

3. Select songs from the list using checkboxes or use Select All/None buttons

4. Click "Export Selected Songs" (full export functionality coming in Sprint 3)

## Acknowledgments

- Based on research from [ew61-export](https://github.com/jamesinglis/ew61-export) PHP implementation
- Designed for local Windows desktop use

## License

*To be determined*