"""
Language Manager for multi-language section mappings
Handles source language detection and target language mapping
"""

import logging
from typing import Dict, List, Optional, Set

logger = logging.getLogger(__name__)

class LanguageManager:
    """Manages language mappings for section names"""
    
    # Default mappings from various source languages to English
    DEFAULT_SOURCE_MAPPINGS = {
        "swedish": {
            "vers": "Verse",
            "refräng": "Chorus",
            "refrang": "Chorus",  # Alternative spelling
            "brygga": "Bridge",
            "bro": "Bridge",  # Alternative
            "förrefräng": "Pre-Chorus",
            "forrefrang": "Pre-Chorus",  # Alternative spelling
            "stick": "Bridge",
            "outro": "Outro",
            "slut": "Outro",
            "intro": "Intro",
            "tag": "Tag",
            "ending": "Ending"
        },
        "german": {
            "strophe": "Verse",
            "vers": "Verse",
            "refrain": "Chorus",
            "brücke": "Bridge",
            "brucke": "Bridge",  # Without umlaut
            "vorrefrain": "Pre-Chorus",
            "intro": "Intro",
            "outro": "Outro",
            "schluss": "Ending",
            "tag": "Tag"
        },
        "french": {
            "couplet": "Verse",
            "refrain": "Chorus",
            "pont": "Bridge",
            "pré-refrain": "Pre-Chorus",
            "pre-refrain": "Pre-Chorus",
            "prérefrain": "Pre-Chorus",
            "intro": "Intro",
            "outro": "Outro",
            "final": "Ending",
            "tag": "Tag"
        },
        "spanish": {
            "verso": "Verse",
            "estrofa": "Verse",
            "coro": "Chorus",
            "estribillo": "Chorus",
            "puente": "Bridge",
            "pre-coro": "Pre-Chorus",
            "precoro": "Pre-Chorus",
            "intro": "Intro",
            "outro": "Outro",
            "final": "Ending",
            "tag": "Tag"
        },
        "norwegian": {
            "vers": "Verse",
            "refreng": "Chorus",
            "bro": "Bridge",
            "bru": "Bridge",
            "mellomspill": "Bridge",
            "intro": "Intro",
            "outro": "Outro",
            "slutt": "Ending",
            "tag": "Tag"
        },
        "danish": {
            "vers": "Verse",
            "omkvæd": "Chorus",
            "omkvaed": "Chorus",  # Alternative spelling
            "bro": "Bridge",
            "mellemspil": "Bridge",
            "intro": "Intro",
            "outro": "Outro",
            "slutning": "Ending",
            "tag": "Tag"
        },
        "english": {
            "verse": "Verse",
            "chorus": "Chorus",
            "bridge": "Bridge",
            "pre-chorus": "Pre-Chorus",
            "prechorus": "Pre-Chorus",
            "intro": "Intro",
            "outro": "Outro",
            "ending": "Ending",
            "tag": "Tag",
            "interlude": "Interlude",
            "vamp": "Vamp"
        }
    }
    
    # Target language section names (for non-English targets)
    TARGET_LANGUAGE_SECTIONS = {
        "english": ["Verse", "Chorus", "Bridge", "Pre-Chorus", "Intro", "Outro", "Tag", "Ending", "Interlude"],
        "german": ["Strophe", "Refrain", "Brücke", "Vorrefrain", "Intro", "Outro", "Tag", "Schluss"],
        "french": ["Couplet", "Refrain", "Pont", "Pré-refrain", "Intro", "Outro", "Tag", "Final"],
        "spanish": ["Verso", "Coro", "Puente", "Pre-coro", "Intro", "Outro", "Tag", "Final"],
        "swedish": ["Vers", "Refräng", "Brygga", "Förrefräng", "Intro", "Outro", "Tag", "Slut"],
        "norwegian": ["Vers", "Refreng", "Bro", "Intro", "Outro", "Tag", "Slutt"],
        "danish": ["Vers", "Omkvæd", "Bro", "Intro", "Outro", "Tag", "Slutning"]
    }
    
    def __init__(self):
        """Initialize the language manager"""
        self.source_languages: List[str] = []
        self.target_language: str = "english"
        self.active_mappings: Dict[str, str] = {}
        
    def set_source_languages(self, languages: List[str]) -> None:
        """
        Set the source languages to use for mapping
        
        Args:
            languages: List of language codes (e.g., ["swedish", "english"])
        """
        self.source_languages = [lang.lower() for lang in languages if lang.lower() in self.DEFAULT_SOURCE_MAPPINGS]
        logger.info(f"Set source languages: {self.source_languages}")
        
    def set_target_language(self, language: str) -> None:
        """
        Set the target language for export
        
        Args:
            language: Target language code (e.g., "english", "german")
        """
        if language.lower() in self.TARGET_LANGUAGE_SECTIONS:
            self.target_language = language.lower()
            logger.info(f"Set target language: {self.target_language}")
        else:
            logger.warning(f"Unknown target language: {language}, defaulting to English")
            self.target_language = "english"
            
    def get_available_source_languages(self) -> List[str]:
        """Get list of available source languages"""
        return list(self.DEFAULT_SOURCE_MAPPINGS.keys())
        
    def get_available_target_languages(self) -> List[str]:
        """Get list of available target languages"""
        return list(self.TARGET_LANGUAGE_SECTIONS.keys())
        
    def get_target_section_names(self) -> List[str]:
        """Get section names for the current target language"""
        return self.TARGET_LANGUAGE_SECTIONS.get(self.target_language, [])
        
    def auto_populate_mappings(self) -> Dict[str, str]:
        """
        Auto-populate mappings based on selected source languages
        Only works when target is English
        
        Returns:
            Dictionary of source term -> target term mappings
        """
        if self.target_language != "english":
            logger.info("Auto-populate only works for English target language")
            return {}
            
        mappings = {}
        
        # Merge mappings from all selected source languages
        for lang in self.source_languages:
            if lang in self.DEFAULT_SOURCE_MAPPINGS:
                lang_mappings = self.DEFAULT_SOURCE_MAPPINGS[lang]
                for source_term, english_term in lang_mappings.items():
                    # Use lowercase for consistent lookup
                    source_key = source_term.lower()
                    if source_key not in mappings:
                        mappings[source_key] = english_term
                        
        self.active_mappings = mappings
        logger.info(f"Auto-populated {len(mappings)} mappings")
        return mappings
        
    def set_manual_mappings(self, mappings: Dict[str, str]) -> None:
        """
        Set manual mappings (for non-English targets or custom overrides)
        
        Args:
            mappings: Dictionary of source term -> target term mappings
        """
        self.active_mappings = {k.lower(): v for k, v in mappings.items()}
        logger.info(f"Set {len(self.active_mappings)} manual mappings")
        
    def get_mapping(self, source_term: str) -> Optional[str]:
        """
        Get the target term for a source term
        
        Args:
            source_term: The source section name
            
        Returns:
            The mapped target term, or None if not found
        """
        return self.active_mappings.get(source_term.lower())
        
    def get_all_source_terms(self) -> Set[str]:
        """
        Get all unique source terms from selected languages
        
        Returns:
            Set of all source terms
        """
        terms = set()
        for lang in self.source_languages:
            if lang in self.DEFAULT_SOURCE_MAPPINGS:
                terms.update(self.DEFAULT_SOURCE_MAPPINGS[lang].keys())
        return terms
        
    def validate_mappings(self) -> List[str]:
        """
        Validate current mappings and return any issues
        
        Returns:
            List of validation issues (empty if all valid)
        """
        issues = []
        
        if not self.source_languages:
            issues.append("No source languages selected")
            
        if not self.target_language:
            issues.append("No target language selected")
            
        if self.target_language != "english" and not self.active_mappings:
            issues.append("Non-English target requires manual mappings")
            
        # Check for unmapped source terms (only for selected languages)
        source_terms = self.get_all_source_terms()
        mapped_terms = set(self.active_mappings.keys())
        unmapped = source_terms - mapped_terms
        
        if unmapped and self.target_language == "english":
            logger.warning(f"Unmapped source terms: {unmapped}")
            
        return issues
        
    def export_config(self) -> Dict:
        """
        Export configuration for saving to settings
        
        Returns:
            Dictionary with language configuration
        """
        return {
            "source_languages": self.source_languages,
            "target_language": self.target_language,
            "active_mappings": self.active_mappings
        }
        
    def import_config(self, config: Dict) -> None:
        """
        Import configuration from settings
        
        Args:
            config: Dictionary with language configuration
        """
        self.source_languages = config.get("source_languages", [])
        self.target_language = config.get("target_language", "english")
        self.active_mappings = config.get("active_mappings", {})
        logger.info("Imported language configuration")