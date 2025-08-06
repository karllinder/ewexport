# -*- coding: utf-8 -*-
"""
Text Cleaner Module for EasyWorship Export

This module provides text cleaning and normalization utilities for
post-processing parsed RTF content and preparing it for export.
"""

import re
import logging
from typing import Optional, List, Dict

logger = logging.getLogger(__name__)


class TextCleaner:
    """
    Text cleaning and normalization utilities.
    
    Handles:
    - Whitespace normalization
    - Special character cleaning
    - Line break formatting
    - Text structure preservation
    """
    
    # Characters that should be removed or replaced
    UNWANTED_CHARS = {
        '\x00': '',  # Null character
        '\x0b': '\n',  # Vertical tab
        '\x0c': '\n',  # Form feed
        '\xa0': ' ',  # Non-breaking space
        '\u2028': '\n',  # Line separator
        '\u2029': '\n\n',  # Paragraph separator
    }
    
    # RTF artifacts that might remain after parsing
    RTF_ARTIFACTS = [
        r'\\[a-z]+\d*',  # RTF control words
        r'\{[^\}]*\}',  # Remaining RTF groups
        r'\\\'[0-9a-f]{2}',  # Hex encoded characters
    ]
    
    def __init__(self):
        """Initialize the text cleaner."""
        self.stats = {}
    
    def clean(self, text: str) -> str:
        """
        Perform complete text cleaning.
        
        Args:
            text: Raw text to clean
            
        Returns:
            Cleaned and normalized text
        """
        if not text:
            return ''
        
        original_length = len(text)
        
        # Remove RTF artifacts
        text = self._remove_rtf_artifacts(text)
        
        # Replace unwanted characters
        text = self._replace_unwanted_chars(text)
        
        # Normalize whitespace
        text = self._normalize_whitespace(text)
        
        # Fix line breaks
        text = self._fix_line_breaks(text)
        
        # Clean up special punctuation
        text = self._clean_punctuation(text)
        
        # Final trim
        text = text.strip()
        
        # Track cleaning stats
        self.stats = {
            'original_length': original_length,
            'cleaned_length': len(text),
            'characters_removed': original_length - len(text)
        }
        
        return text
    
    def _remove_rtf_artifacts(self, text: str) -> str:
        """
        Remove any remaining RTF formatting codes.
        
        Args:
            text: Text potentially containing RTF artifacts
            
        Returns:
            Text with RTF artifacts removed
        """
        for pattern in self.RTF_ARTIFACTS:
            text = re.sub(pattern, '', text)
        
        # Remove escaped braces
        text = text.replace('\\{', '{').replace('\\}', '}')
        
        # Remove double backslashes
        text = text.replace('\\\\', '\\')
        
        return text
    
    def _replace_unwanted_chars(self, text: str) -> str:
        """
        Replace or remove unwanted special characters.
        
        Args:
            text: Text with potential unwanted characters
            
        Returns:
            Text with unwanted characters replaced
        """
        for char, replacement in self.UNWANTED_CHARS.items():
            text = text.replace(char, replacement)
        
        # Remove control characters (except newline and tab)
        text = ''.join(char for char in text if ord(char) >= 32 or char in '\n\t')
        
        return text
    
    def _normalize_whitespace(self, text: str) -> str:
        """
        Normalize whitespace throughout the text.
        
        Args:
            text: Text with potentially irregular whitespace
            
        Returns:
            Text with normalized whitespace
        """
        # Replace tabs with spaces
        text = text.replace('\t', '  ')
        
        # Replace multiple spaces with single space
        text = re.sub(r' {2,}', ' ', text)
        
        return text
    
    def _fix_line_breaks(self, text: str) -> str:
        """
        Fix and normalize line breaks.
        
        Args:
            text: Text with potentially irregular line breaks
            
        Returns:
            Text with normalized line breaks
        """
        # Normalize different line ending styles
        text = text.replace('\r\n', '\n')
        text = text.replace('\r', '\n')
        
        # Remove excessive blank lines (more than 2 consecutive)
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        # Remove trailing whitespace from each line
        lines = text.split('\n')
        lines = [line.rstrip() for line in lines]
        text = '\n'.join(lines)
        
        return text
    
    def _clean_punctuation(self, text: str) -> str:
        """
        Clean up special punctuation and quotes.
        
        Args:
            text: Text with potentially problematic punctuation
            
        Returns:
            Text with cleaned punctuation
        """
        # Unicode replacements for special characters
        replacements = {
            '\u201c': '"',  # Left double quotation mark
            '\u201d': '"',  # Right double quotation mark
            '\u2018': "'",  # Left single quotation mark
            '\u2019': "'",  # Right single quotation mark
            '\u2013': '-',  # En dash
            '\u2014': '-',  # Em dash
            '\u2026': '...',  # Ellipsis
        }
        
        for old, new in replacements.items():
            text = text.replace(old, new)
        
        return text
    
    def get_stats(self) -> Dict:
        """Get statistics from the last cleaning operation."""
        return self.stats


class SongTextCleaner(TextCleaner):
    """
    Specialized text cleaner for song lyrics.
    
    Includes additional processing specific to song content:
    - Chord removal options
    - Repetition markers
    - Song-specific formatting
    """
    
    def __init__(self, remove_chords: bool = False):
        """
        Initialize the song text cleaner.
        
        Args:
            remove_chords: Whether to remove chord notations
        """
        super().__init__()
        self.remove_chords = remove_chords
    
    def clean(self, text: str) -> str:
        """
        Clean song text with song-specific processing.
        
        Args:
            text: Raw song text
            
        Returns:
            Cleaned song text
        """
        # Perform base cleaning
        text = super().clean(text)
        
        # Remove chord notations if requested
        if self.remove_chords:
            text = self._remove_chord_notations(text)
        
        # Clean repetition markers
        text = self._clean_repetition_markers(text)
        
        # Fix song-specific formatting
        text = self._fix_song_formatting(text)
        
        return text
    
    def _remove_chord_notations(self, text: str) -> str:
        """
        Remove chord notations from song text.
        
        Args:
            text: Song text potentially containing chords
            
        Returns:
            Text with chord notations removed
        """
        # Common chord patterns: [C], (C), C:, etc.
        # Match chords like C, G7, Am, F#m, Bb, etc.
        chord_pattern = r'\[?[A-G][#b]?(?:maj|min|m|dim|aug|sus|add)?[0-9]*\]?'
        
        # Remove chords in brackets
        text = re.sub(r'\[' + chord_pattern + r'\]', '', text)
        
        # Remove chords in parentheses
        text = re.sub(r'\(' + chord_pattern + r'\)', '', text)
        
        # Remove standalone chords at start of lines
        text = re.sub(r'^' + chord_pattern + r'\s+', '', text, flags=re.MULTILINE)
        
        return text
    
    def _clean_repetition_markers(self, text: str) -> str:
        """
        Clean up repetition markers in song text.
        
        Args:
            text: Song text with repetition markers
            
        Returns:
            Text with cleaned repetition markers
        """
        # Common repetition patterns
        patterns = [
            r'\(x\d+\)',  # (x2), (x3), etc.
            r'\(\d+x\)',  # (2x), (3x), etc.
            r'\[x\d+\]',  # [x2], [x3], etc.
            r'\[\d+x\]',  # [2x], [3x], etc.
            r'x\d+$',  # x2, x3 at end of line
        ]
        
        for pattern in patterns:
            text = re.sub(pattern, '', text, flags=re.MULTILINE | re.IGNORECASE)
        
        return text
    
    def _fix_song_formatting(self, text: str) -> str:
        """
        Fix song-specific formatting issues.
        
        Args:
            text: Song text
            
        Returns:
            Text with improved song formatting
        """
        # Ensure proper spacing after punctuation
        text = re.sub(r'([.!?])([A-ZÅÄÖa-zåäö])', r'\1 \2', text)
        
        # Fix spacing around parentheses
        text = re.sub(r'\(\s+', '(', text)
        text = re.sub(r'\s+\)', ')', text)
        
        # Capitalize first letter of each line (common in songs)
        lines = text.split('\n')
        capitalized_lines = []
        for line in lines:
            if line.strip():  # Only process non-empty lines
                stripped = line.strip()
                if stripped[0].islower():
                    # Find the position of the first character and capitalize it
                    first_char_pos = len(line) - len(line.lstrip())
                    line = line[:first_char_pos] + line[first_char_pos].upper() + line[first_char_pos+1:]
            capitalized_lines.append(line)
        
        return '\n'.join(capitalized_lines)


def clean_text(text: str, for_song: bool = True, remove_chords: bool = False) -> str:
    """
    Convenience function to clean text.
    
    Args:
        text: Text to clean
        for_song: Whether to use song-specific cleaning
        remove_chords: Whether to remove chord notations (only if for_song=True)
        
    Returns:
        Cleaned text
    """
    if for_song:
        cleaner = SongTextCleaner(remove_chords=remove_chords)
    else:
        cleaner = TextCleaner()
    
    return cleaner.clean(text)