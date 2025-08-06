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

### 📋 Sprint 4: ProPresenter Export (Planned)
**Status**: Not Started  

Planned Features:
- ProPresenter 6 XML generation
- GUID generation for slides
- File naming sanitization
- Export progress tracking
- Error handling and recovery

### 📋 Sprint 5: Advanced Features (Planned)
**Status**: Not Started  

Planned Features:
- Search and filtering
- Export options dialog
- Settings persistence
- Bible verse detection
- Duplicate file handling

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
- None reported yet

### Resolved Issues
- Import path issues in main.py (Sprint 2)

## Performance Metrics

### Target Performance
- Load 1000 songs: < 2 seconds
- Search response: < 100ms
- Export 100 songs: < 30 seconds
- Memory usage: < 200MB

### Current Performance
- To be measured after Sprint 3

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