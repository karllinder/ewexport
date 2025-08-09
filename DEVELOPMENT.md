# Development Documentation

## Branch Strategy
- `main`: Stable releases only
- `sprint*`: Feature development branches
- Create new branch for each sprint/major feature
- Merge to main via pull request after testing

## Sprint Progress Tracking

### ✅ Sprint 1: Research & Planning
**Status**: Complete  
**Branch**: main  
**Date**: 2025-01-06  

Key Deliverables:
- Database structure research
- ProPresenter format analysis
- Architecture design
- Technology stack selection

### ✅ Sprint 2: MVP GUI Implementation  
**Status**: Complete  
**Branch**: main  
**Date**: 2025-01-06  

Implemented Features:
- Basic Tkinter GUI with song list
- SQLite database connection
- Auto-detection of EasyWorship path
- Song selection with checkboxes
- Select All/None functionality
- Real-time selection counter

### ✅ Sprint 3: RTF Parsing & Text Processing
**Status**: Complete  
**Branch**: main (merged from sprint3-rtf-parsing)  
**Completed**: 2025-01-06  
**PR**: #1

Implemented Features:
- ✅ RTF to plain text conversion with striprtf
- ✅ Swedish Unicode character handling (å, ä, ö)
- ✅ Section detection from RTF formatting
- ✅ Text cleaning and normalization
- ✅ Section label mapping (Swedish to English)
- ✅ Database integration with processed lyrics
- ✅ Comprehensive test suite (14 tests)
- ✅ Interactive demo and documentation

Technical Solutions:
- Custom Unicode escape handling: \u228?→ä, \u229?→å, \u246?→ö
- Advanced section detection with pattern matching
- RTF structure parsing (\par vs \line handling)
- Swedish character preservation throughout pipeline

### ✅ Sprint 4: ProPresenter Export
**Status**: Complete  
**Branch**: main (merged from sprint4-propresenter-export)  
**Completed**: 2025-01-07  
**PR**: #2  
**Releases**: v0.1.0, v0.1.1

Implemented Features:
- ✅ ProPresenter 6 XML generation with complete structure
- ✅ GUID generation for all elements (slides, groups, arrangements)
- ✅ RTF data encoding for text content
- ✅ WinFlow and WinFont data generation
- ✅ File naming sanitization for Windows compatibility
- ✅ Batch export with real-time progress tracking
- ✅ Multi-threaded export to prevent GUI freezing
- ✅ Comprehensive error handling and recovery
- ✅ Export results dialog with success/failure summary
- ✅ Cancel export functionality

Technical Achievements:
- Complete ProPresenter 6 XML document structure
- Proper slide grouping by sections
- Swedish character preservation in XML
- Base64 encoding for binary data
- Thread-safe progress callbacks
- Graceful failure handling per song

### 🔧 Bug Fixes: RV Slide Group Handling
**Status**: Complete  
**Branch**: main (merged from bugfix/rv-slide-group-handling)  
**Completed**: 2025-01-07  
**PR**: #3

Bug Fixes Implemented:
- ✅ RV Slide Group naming with section numbers (verse 1 → Verse 1)
- ✅ Configurable Swedish to English section mappings
- ✅ Extra line feed removal from slide content
- ✅ Created config/section_mappings.json for translation settings
- ✅ Updated SectionDetector for number preservation
- ✅ Fixed ProPresenter export content trimming

### ✅ Sprint 5: Search/Filter & Settings GUI
**Status**: Complete  
**Branch**: main (merged from sprint-5-search-filter)  
**Completed**: 2025-01-08  
**PR**: #4

Implemented Features:
- ✅ Real-time search filtering across title, author, copyright, CCLI fields
- ✅ Search history with last 10 searches (persistent storage)
- ✅ Result count display ("Showing X of Y songs")
- ✅ Clear search button for quick reset
- ✅ Comprehensive Settings GUI for section mappings
- ✅ Table/grid view for managing mappings
- ✅ Add/Edit/Delete mapping operations
- ✅ Real-time preview with test input
- ✅ Import/Export mapping configurations
- ✅ Reset to defaults functionality
- ✅ Menu bar integration (File, Edit, Help menus)
- ✅ About dialog
- ✅ Automatic selection clearing after export

Technical Achievements:
- Search history persistence in ~/.ewexport/search_history.json
- Modal settings dialog with tabbed interface
- Duplicate mapping validation
- Case-insensitive mapping with number preservation
- Double-click editing in mappings table
- Unsaved changes warning dialog

Partial Settings Persistence Implemented:
- ✅ Search history (last 10 searches)
- ✅ Section mappings configuration
- ⏳ Last EasyWorship database path (not yet)
- ⏳ Last export directory (not yet)
- ⏳ Window size/position (not yet)
- ⏳ Column widths (not yet)

### 📋 Sprint 6: Settings Persistence & Export Options
**Status**: Planning  

1. **Complete Settings Persistence**:
   - Last EasyWorship database path
   - Last export directory
   - Window size and position
   - Column widths in song list
   - Export preferences (folder structure, CCLI info options)
   - Select output directory on first run and then save it, no hardcoded default path.

2. **Export Options**:
   - Output directory selection with browse
   - Text formatting preferences.
   - Select output font in settings.
   - Enable blank page with group name "Into" as first slide, and "Blank" as last. Options in settings.

3. **Duplicate File Handling**:
   - Detect existing files before export
   - Dialog with options: Skip/Overwrite/Rename/Apply to All

4. **Preview Functionality**:
   - Preview converted text before export
   - Show detected sections with labels
   - Display section mapping results
   - Edit text before export option

Future Sprint 7 Features:
- Bible verse detection and special handling
- Multi-language section mappings (German, French, Spanish)
- Export statistics and reporting
- Batch operations (export by tag, date range)
- Advanced search filters (regex, date modified)

## Testing Approach

### Unit Tests
- RTF parser with various encodings
- Section detection accuracy
- Swedish character handling
- XML validation

### Integration Tests  
- Database to export pipeline
- Large database handling
- Edge cases (empty fields, special chars)

### Manual Testing
- Test with real EasyWorship databases
- Verify ProPresenter import
- Swedish church song libraries

## Known Issues & Bugs

### Current Issues
- ProPresenter 6 format validation tests fail (not affecting functionality)
- Some advanced ProPresenter 6 features not implemented (timeline, arrangements)

### Resolved Issues
- Import path issues in main.py (Sprint 2)
- RTF parsing with Swedish characters (Sprint 3)
- GUI freezing during export (Sprint 4)
- Song ID type mismatch in export (Sprint 4)

## Performance Metrics

### Target Performance
- Load 1000 songs: < 2 seconds
- Search response: < 100ms
- Export 100 songs: < 30 seconds
- Memory usage: < 200MB

### Current Performance
- Load 1000 songs: ~1.5 seconds ✅
- Export 100 songs: ~15-20 seconds ✅
- Memory usage: < 150MB ✅
- GUI remains responsive during export ✅

## Dependencies

### Core Dependencies
- Python 3.8+
- tkinter (built-in)
- sqlite3 (built-in)
- striprtf (1.6+)

### Development Dependencies
- PyInstaller (5.0+)
- pytest (for testing)

## Code Standards

### Python Style
- Follow PEP 8
- Type hints where beneficial
- Docstrings for public methods
- No inline comments unless necessary

### Git Commits
- Clear, descriptive messages
- Reference sprint/issue numbers
- Include Co-Authored-By for AI assistance

### File Organization
```
src/
├── gui/          # UI components
├── database/     # Data access layer
├── processing/   # RTF and text processing
├── export/       # ProPresenter generation
└── utils/        # Shared utilities
```

## Release Process

1. Complete sprint features on feature branch
2. Run all tests
3. Update version in setup.py
4. Update README and CHANGELOG
5. Create pull request to main
6. Tag release after merge
7. Build executable with PyInstaller

## Architecture Decisions

### Why Tkinter?
- Built into Python (no extra deps)
- Simple for basic GUI needs
- Native Windows appearance
- Fast enough for our needs

### Why SQLite directly?
- EasyWorship uses SQLite natively
- No ORM overhead needed
- Simple schema, direct queries sufficient

### Why XML for ProPresenter 6?
- Human-readable format
- Easier than protobuf (PP7)
- Well-supported by Python stdlib

## RTF Processing Strategy

### Approach for Sprint 3
1. Use striprtf library for basic conversion
2. Custom handling for Swedish Unicode escapes
3. Detect sections by text patterns
4. Preserve line breaks for slide boundaries

### Section Detection Logic
- Look for keywords: verse, chorus, bridge, etc.
- Keywords appear on their own line
- Already in English in Swedish databases
- Map to ProPresenter group labels

## Contact & Support

Project: https://github.com/karllinder/ewexport  
Issues: https://github.com/karllinder/ewexport/issues