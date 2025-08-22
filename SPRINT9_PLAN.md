# Sprint 9: Multi-Language Support Implementation Plan

## Overview
This sprint adds comprehensive multi-language support for section name mappings, allowing users to work with songs in German, French, Spanish, Norwegian, Danish, and other languages. Users can select both source (FROM) languages and target (TO) language for export, with integration into the existing section mappings editor.

## Key Design Decisions

### 1. Language Detection Strategy
**Decision: User-Selected Language Configuration**
- Users manually select which language(s) are present in their database
- No auto-detection (too complex and error-prone)
- Language selection is mandatory before export can proceed

**Rationale:**
- Churches typically know what languages are in their database
- Auto-detection would be unreliable with mixed languages
- Manual selection provides predictable, consistent results

### 2. Target (TO) Language Selection
**Decision: Configurable Export Target Language**
- Users can select target language for export (default: English)
- When non-English target selected, users must manually configure mappings
- Integrates with existing section mappings editor

**Rationale:**
- Some churches may want to export to languages other than English
- Manual mapping ensures accuracy for non-standard targets
- Leverages existing mapping editor functionality

### 3. Settings Architecture

#### A. Embedded Default Mappings
Since we distribute a single EXE file, default language mappings will be embedded in the code:

```python
DEFAULT_LANGUAGE_MAPPINGS = {
    "swedish": {
        "vers": "Verse",
        "refräng": "Chorus",
        "brygga": "Bridge",
        "förrefräng": "Pre-Chorus"
    },
    "german": {
        "strophe": "Verse",
        "vers": "Verse",
        "refrain": "Chorus",
        "brücke": "Bridge",
        "vorrefrain": "Pre-Chorus"
    },
    "french": {
        "couplet": "Verse",
        "refrain": "Chorus",
        "pont": "Bridge",
        "pré-refrain": "Pre-Chorus"
    },
    "spanish": {
        "verso": "Verse",
        "estrofa": "Verse",
        "coro": "Chorus",
        "puente": "Bridge",
        "pre-coro": "Pre-Chorus"
    },
    "norwegian": {
        "vers": "Verse",
        "refreng": "Chorus",
        "bro": "Bridge",
        "mellomspill": "Bridge"
    },
    "danish": {
        "vers": "Verse",
        "omkvæd": "Chorus",
        "bro": "Bridge"
    }
}

# Target language section names (for non-English targets)
TARGET_LANGUAGE_SECTIONS = {
    "english": ["Verse", "Chorus", "Bridge", "Pre-Chorus", "Intro", "Outro", "Tag"],
    "german": ["Strophe", "Refrain", "Brücke", "Vorrefrain", "Intro", "Outro", "Tag"],
    "french": ["Couplet", "Refrain", "Pont", "Pré-refrain", "Intro", "Outro", "Tag"],
    "spanish": ["Verso", "Coro", "Puente", "Pre-coro", "Intro", "Outro", "Tag"]
}
```

#### B. Settings File Structure (v2.0.0)
```json
{
  "version": "2.0.0",
  "language_settings": {
    "source_languages": ["swedish", "english"],
    "target_language": "english",
    "auto_populate_mappings": true
  },
  "section_mappings": {
    "active_mappings": {}  // Populated from source languages or manual entry
  },
  "export_settings": {
    // Existing export settings...
  }
}
```

### 3. Version Migration Strategy

#### Current Version: 1.2.0 → Target Version: 2.0.0

**Migration Path:**
1. Detect old version (1.2.0 or missing version field)
2. Preserve existing mappings in section_mappings
3. Set Swedish as source language (backward compatibility)
4. Set English as target language (default)
5. Create new structure with language_settings
6. Backup old settings before migration

**Migration Code Structure:**
```python
def migrate_settings(old_settings):
    """Migrate settings from 1.2.0 to 2.0.0"""
    if old_settings.get('version', '1.0.0') < '2.0.0':
        # Backup old settings
        backup_settings(old_settings)
        
        # Create new structure
        new_settings = {
            'version': '2.0.0',
            'language_settings': {
                'source_languages': ['swedish', 'english'],
                'target_language': 'english',
                'auto_populate_mappings': True
            }
        }
        
        # Preserve old mappings
        if 'section_mappings' in old_settings:
            new_settings['section_mappings'] = old_settings['section_mappings']
        
        # Preserve other settings
        for key in ['export_settings', 'window_geometry']:
            if key in old_settings:
                new_settings[key] = old_settings[key]
        
        return new_settings
    return old_settings
```

## Implementation Plan

### Phase 1: Core Infrastructure (Day 1-2)
1. **Update ConfigManager**
   - Add version migration system
   - Implement settings backup mechanism
   - Add language mappings loader

2. **Create Language Module**
   - `src/processing/language_manager.py`
   - Embedded default mappings for FROM languages
   - Target language section names
   - Auto-populate mappings based on selected languages

### Phase 2: UI Implementation (Day 2-3)
1. **Language Selection Dialog**
   - New menu item: Edit → Language Settings
   - Source languages: Multi-select checkbox list
   - Target language: Dropdown (English, German, French, Spanish)
   - Auto-populate button to fill mappings

2. **Enhanced Section Mappings Editor**
   - Show target language section names when non-English selected
   - Allow manual mapping when target is not English
   - Clear indication of source → target mapping

3. **First-Run Experience**
   - Detect if no language selected
   - Force language selection before export
   - Clear instructions for source and target selection

### Phase 3: Migration & Testing (Day 3-4)
1. **Migration Testing**
   - Create test cases for 1.2.0 → 2.0.0
   - Test with missing version field
   - Test with corrupted settings
   - Verify backup creation

2. **Language Testing**
   - Test each source language mapping
   - Test multi-language source selection
   - Test different target languages
   - Test manual mapping for non-English targets
   - Test edge cases (empty mappings, conflicts)

### Phase 4: Documentation & Polish (Day 4-5)
1. **Update Documentation**
   - Update CLAUDE.md with new architecture
   - Create user guide for language selection
   - Document migration process

2. **Error Handling**
   - Clear error messages for migration failures
   - Helpful tooltips in language dialog
   - Validation of custom mappings

## Test Cases

### 1. Settings Migration Tests
```python
class TestSettingsMigration:
    def test_migrate_from_1_2_0(self):
        """Test migration from v1.2.0 to v2.0.0"""
        old_settings = {
            'version': '1.2.0',
            'section_mappings': {'vers': 'Verse'},
            'export_settings': {'output_dir': 'C:/test'}
        }
        new_settings = migrate_settings(old_settings)
        assert new_settings['version'] == '2.0.0'
        assert 'swedish' in new_settings['language_settings']['source_languages']
        assert new_settings['language_settings']['target_language'] == 'english'
        assert new_settings['section_mappings']['vers'] == 'Verse'
    
    def test_migrate_no_version(self):
        """Test migration from settings without version"""
        old_settings = {'section_mappings': {'vers': 'Verse'}}
        new_settings = migrate_settings(old_settings)
        assert new_settings['version'] == '2.0.0'
    
    def test_backup_creation(self):
        """Test that backup is created during migration"""
        # Test backup file creation
        # Test backup content matches original
        pass
    
    def test_failed_migration_rollback(self):
        """Test rollback on migration failure"""
        # Test that original settings are preserved on error
        pass
```

### 2. Language Selection Tests
```python
class TestLanguageSelection:
    def test_single_source_language(self):
        """Test selection of single source language"""
        pass
    
    def test_multiple_source_languages(self):
        """Test merging of multiple source language mappings"""
        pass
    
    def test_target_language_english(self):
        """Test default English target language"""
        pass
    
    def test_target_language_non_english(self):
        """Test non-English target requires manual mapping"""
        pass
    
    def test_no_language_blocks_export(self):
        """Test that export is blocked without language selection"""
        pass
```

## UI Mockup

### Language Settings Dialog
```
┌─ Language Settings ─────────────────────────────────┐
│                                                      │
│  SOURCE Languages (in your database):               │
│                                                      │
│  ☑ Swedish (vers, refräng, brygga)                 │
│  ☑ English (verse, chorus, bridge)                 │
│  ☐ German (strophe, refrain, brücke)               │
│  ☐ French (couplet, refrain, pont)                 │
│  ☐ Spanish (verso, coro, puente)                   │
│  ☐ Norwegian (vers, refreng, bro)                  │
│  ☐ Danish (vers, omkvæd, bro)                      │
│                                                      │
│  TARGET Language (export to):                       │
│  [English            ▼]                              │
│                                                      │
│  [Auto-populate Mappings]                           │
│                                                      │
│  Note: When target is not English, use the          │
│  Section Mappings editor to configure mappings.     │
│                                                      │
│  [Open Section Mappings Editor]  [OK]  [Cancel]     │
└──────────────────────────────────────────────────────┘
```

### Enhanced Section Mappings Editor (when target ≠ English)
```
┌─ Section Mappings ──────────────────────────────────┐
│                                                      │
│  Target Language: German                            │
│                                                      │
│  Source Term    →    Target Term                    │
│  ──────────────────────────────────────────────────  │
│  vers           →    [Strophe        ▼]             │
│  refräng        →    [Refrain        ▼]             │
│  brygga         →    [Brücke         ▼]             │
│  verse          →    [Strophe        ▼]             │
│  chorus         →    [Refrain        ▼]             │
│  bridge         →    [Brücke         ▼]             │
│                                                      │
│  Available German sections:                         │
│  Strophe, Refrain, Brücke, Vorrefrain,             │
│  Intro, Outro, Tag                                  │
│                                                      │
│  [Save]  [Cancel]                                   │
└──────────────────────────────────────────────────────┘
```

## Risk Mitigation

### Risk 1: Migration Failure
**Mitigation:**
- Always create backup before migration
- Provide manual recovery instructions
- Include settings reset option

### Risk 2: Language Conflicts
**Mitigation:**
- Use existing section mappings editor
- Clear indication of source vs target
- Manual control for non-English targets

### Risk 3: Performance Impact
**Mitigation:**
- Cache merged mappings
- Only recalculate on settings change
- Optimize mapping lookup

## Success Criteria

1. **Backward Compatibility**
   - Existing users' settings migrate seamlessly
   - No data loss during migration
   - Swedish mappings continue to work

2. **Multi-Language Support**
   - All 6 source languages fully supported
   - Multiple target language options
   - Integration with existing mapping editor
   - Manual mapping for non-English targets

3. **Robustness**
   - Settings migration has comprehensive tests
   - Clear error messages and recovery paths
   - Version tracking prevents future issues

4. **User Experience**
   - Intuitive language selection
   - Clear documentation
   - Helpful error messages

## Timeline

- **Day 1-2**: Core infrastructure and language manager
- **Day 2-3**: UI implementation and integration
- **Day 3-4**: Migration system and testing
- **Day 4-5**: Documentation and final polish
- **Day 5**: Final testing and PR submission

## Files to Modify

1. **New Files:**
   - `src/processing/language_manager.py`
   - `src/gui/language_dialog.py`
   - `tests/test_migration.py`
   - `tests/test_language_manager.py`

2. **Modified Files:**
   - `src/utils/config.py` - Add migration system
   - `src/gui/main_window.py` - Add language menu item
   - `src/processing/section_detector.py` - Use language manager
   - `CLAUDE.md` - Document new features
   - `setup.py` - Bump version to 1.3.0

## Open Questions (Resolved)

1. **Q: How to detect language?**
   **A: User selection only, no auto-detection**

2. **Q: How to handle settings versioning?**
   **A: Semantic versioning with migration functions**

3. **Q: Where to store default mappings?**
   **A: Embedded in code for single EXE distribution**

4. **Q: How to handle custom mappings?**
   **A: Use existing section mappings editor, no new custom system**

5. **Q: How to handle non-English target languages?**
   **A: Manual mapping through section editor with language-specific options**

## Next Steps

1. Review and approve this plan
2. Create feature branch and start implementation
3. Regular testing during development
4. User testing before merge to main