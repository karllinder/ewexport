# -*- coding: utf-8 -*-
"""
RTF Parser Module for EasyWorship Export

This module handles parsing RTF content from EasyWorship's SongWords.db database,
with special handling for Swedish Unicode characters and EasyWorship-specific formatting.
"""

import re
import logging
from typing import Optional, Dict, Any
from striprtf.striprtf import rtf_to_text

logger = logging.getLogger(__name__)


class EasyWorshipRTFParser:
    r"""
    Parser for EasyWorship RTF content with Swedish language support.
    
    Handles:
    - Unicode escape sequences for Swedish characters (å, ä, ö)
    - RTF structure conversion (\par, \line)
    - Text cleaning and normalization
    """
    
    # Unicode mappings for Swedish characters found in EasyWorship RTF
    UNICODE_MAPPINGS = {
        228: 'ä',  # Swedish letter ä
        229: 'å',  # Swedish letter å  
        246: 'ö',  # Swedish letter ö
        180: '´',  # Accent mark
        # Additional common Unicode escapes
        8217: "'",  # Right single quotation mark
        8220: '"',  # Left double quotation mark
        8221: '"',  # Right double quotation mark
        8211: '–',  # En dash
        8212: '—',  # Em dash
    }
    
    def __init__(self):
        """Initialize the RTF parser."""
        self.last_error = None
        
    def parse(self, rtf_content: str) -> Optional[Dict[str, Any]]:
        """
        Parse RTF content and return structured data.
        
        Args:
            rtf_content: RTF formatted string from EasyWorship database
            
        Returns:
            Dictionary with:
                - plain_text: Complete plain text version
                - lines: List of text lines preserving structure
                - has_content: Boolean indicating if content exists
            Returns None if parsing fails or content is empty
        """
        if not rtf_content or not rtf_content.strip():
            logger.debug("Empty RTF content provided")
            return None
            
        try:
            # First, use striprtf for basic RTF parsing
            plain_text = self._basic_rtf_parse(rtf_content)
            
            # Post-process for EasyWorship-specific Unicode patterns
            plain_text = self._fix_unicode_characters(plain_text)
            
            # Clean up the text
            plain_text = self._clean_text(plain_text)
            
            # Split into lines while preserving structure
            lines = self._extract_lines(plain_text)
            
            # Check if we have actual content
            has_content = bool(plain_text.strip())
            
            result = {
                'plain_text': plain_text,
                'lines': lines,
                'has_content': has_content
            }
            
            logger.debug(f"Successfully parsed RTF with {len(lines)} lines")
            return result
            
        except Exception as e:
            self.last_error = str(e)
            logger.error(f"RTF parsing failed: {e}")
            return None
    
    def _basic_rtf_parse(self, rtf_content: str) -> str:
        """
        Perform basic RTF to text conversion using striprtf.
        
        Args:
            rtf_content: RTF formatted string
            
        Returns:
            Plain text with basic RTF codes removed
        """
        try:
            # Use striprtf for initial conversion
            text = rtf_to_text(rtf_content)
            return text
        except Exception as e:
            logger.warning(f"striprtf failed, attempting manual parse: {e}")
            # Fallback to manual parsing if striprtf fails
            return self._manual_rtf_parse(rtf_content)
    
    def _manual_rtf_parse(self, rtf_content: str) -> str:
        """
        Manual RTF parsing as fallback when striprtf fails.
        
        Args:
            rtf_content: RTF formatted string
            
        Returns:
            Plain text with RTF codes removed
        """
        text = rtf_content
        
        # Remove RTF header and footer
        text = re.sub(r'^{\\rtf[^}]*}', '', text)
        text = re.sub(r'}$', '', text)
        
        # Convert \par to newlines (new slide/paragraph)
        text = text.replace(r'\par', '\n')
        
        # Convert \line to newlines (line break within slide)
        text = text.replace(r'\line', '\n')
        
        # Remove font table
        text = re.sub(r'{\\fonttbl[^}]*}', '', text)
        
        # Remove color table
        text = re.sub(r'{\\colortbl[^}]*}', '', text)
        
        # Remove other RTF groups
        text = re.sub(r'{\\[^}]*}', '', text)
        
        # Remove RTF control words (but keep their content)
        text = re.sub(r'\\[a-z]+[-]?\d*\s?', '', text)
        
        # Remove remaining curly braces
        text = text.replace('{', '').replace('}', '')
        
        # Handle escaped characters
        text = text.replace('\\{', '{').replace('\\}', '}')
        text = text.replace('\\\\', '\\')
        
        return text
    
    def _fix_unicode_characters(self, text: str) -> str:
        """
        Fix EasyWorship-specific Unicode escape sequences.
        
        Handles both positive and negative Unicode values and
        special handling for Swedish characters.
        
        Args:
            text: Text with potential Unicode escape sequences
            
        Returns:
            Text with Unicode characters properly decoded
        """
        # Handle standard Unicode escapes (both positive and negative)
        def unicode_replace(match):
            """Replace Unicode escape sequences with actual characters."""
            code = int(match.group(1))
            
            # Check if we have a specific mapping for this code
            if code in self.UNICODE_MAPPINGS:
                return self.UNICODE_MAPPINGS[code]
            
            # Handle negative values (two's complement for 16-bit)
            if code < 0:
                code = 65536 + code
            try:
                return chr(code)
            except (ValueError, OverflowError):
                logger.warning(f"Cannot decode Unicode value: {code}")
                return match.group(0)  # Return original if can't decode
        
        # Match \uNNNN? or \uNNNN where NNNN can be negative
        text = re.sub(r'\\u(-?\d+)\??', unicode_replace, text)
        
        return text
    
    def _clean_text(self, text: str) -> str:
        """
        Clean up text after RTF parsing.
        
        Args:
            text: Raw parsed text
            
        Returns:
            Cleaned text with normalized whitespace and structure
        """
        # Remove any remaining RTF artifacts
        text = re.sub(r'\\[a-z]+\d*', '', text)
        
        # Normalize line endings
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        
        # Remove excessive blank lines (more than 2 consecutive)
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        # Remove trailing whitespace from each line
        lines = text.split('\n')
        lines = [line.rstrip() for line in lines]
        text = '\n'.join(lines)
        
        # Remove leading/trailing whitespace from entire text
        text = text.strip()
        
        return text
    
    def _extract_lines(self, text: str) -> list:
        """
        Extract lines from text while preserving structure.
        
        Args:
            text: Plain text content
            
        Returns:
            List of non-empty lines
        """
        lines = text.split('\n')
        # Keep empty lines as they may indicate slide breaks
        # but remove lines that are only whitespace
        return [line.rstrip() for line in lines]
    
    def get_last_error(self) -> Optional[str]:
        """Get the last error message if any."""
        return self.last_error


def parse_rtf(rtf_content: str) -> Optional[Dict[str, Any]]:
    """
    Convenience function to parse RTF content.
    
    Args:
        rtf_content: RTF formatted string
        
    Returns:
        Parsed content dictionary or None if parsing fails
    """
    parser = EasyWorshipRTFParser()
    return parser.parse(rtf_content)