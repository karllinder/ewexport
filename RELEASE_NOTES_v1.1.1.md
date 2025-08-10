# Release Notes - Version 1.1.1

**Release Date:** January 11, 2025

## Overview
This patch release addresses critical bugs reported by users and improves the overall user experience. All issues were identified through real-world usage and reported via GitHub Issues.

## Bug Fixes

### Issue #7: Export Failures and Duplicate Handling
- **Fixed:** Export failures for songs with IDs 2727, 2728, 2729
- **Fixed:** ValueError when handling duplicate files during batch export
- **Improvement:** Enhanced error handling to provide more descriptive error messages
- **Improvement:** Better logging for debugging export issues
- **Improvement:** Robust duplicate file detection using file path indexing
- **Impact:** Songs that previously failed to export now work correctly, duplicate handling is reliable

### Issue #6: Database File Selection Dialog
- **Fixed:** File dialog now displays .db files when selecting EasyWorship database
- **Improvement:** Changed from directory-only selection to file selection dialog
- **Improvement:** Users can now see Songs.db and SongWords.db files to confirm correct folder
- **Improvement:** Added validation warning if required database files are missing
- **Impact:** Much easier for users to locate and select the correct database folder

### Issue #8: Font Size Selection UX
- **Fixed:** Replaced difficult-to-use spinbox with dropdown combobox
- **Improvement:** Added common font sizes for quick selection (12, 18, 24, 36, 48, 60, 72, 84, 96, 120, 144, 168, 200)
- **Improvement:** Extended font size range from 12-120 to 12-200 for large projection displays
- **Improvement:** Allow custom font size entry with validation
- **Impact:** Significantly improved user experience when selecting font sizes

## Technical Improvements
- Enhanced error logging throughout the export pipeline
- Improved data consistency between database reads and exports
- Better handling of edge cases in RTF parsing
- More robust file system error handling

## Known Issues
- No new issues identified in this release

## Upgrade Notes
This is a backward-compatible patch release. No configuration changes required.

## Testing
All fixes have been tested with:
- Sample EasyWorship 6.1 databases
- Swedish and English songs
- Various font sizes and export configurations
- Songs with special characters and empty metadata

## Contributors
- Karl Linder (Project Owner)
- Claude AI Assistant (Development Support)

## Issues Resolved
- Issue #6: Database file dialog improvements
- Issue #7: Export failures and duplicate handling
- Issue #8: Font size selection UX
- Issue #9: Development coordination (meta-issue)

## Acknowledgments
Thanks to all users who reported issues and provided feedback to help improve the application.