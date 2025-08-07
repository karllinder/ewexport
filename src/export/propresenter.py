"""
ProPresenter 6 XML export functionality - Corrected format
Based on propresenter-parser documentation
"""

import xml.etree.ElementTree as ET
import xml.dom.minidom
import uuid
import re
import base64
from pathlib import Path
from typing import List, Dict, Optional, Any, Tuple
from datetime import datetime

class ProPresenter6Exporter:
    """Handles export to ProPresenter 6 (.pro6) format with correct XML structure"""
    
    def __init__(self):
        self.slide_width = 1920
        self.slide_height = 1080
        self.default_font_size = 60
        self.text_padding = 20
        
    def sanitize_filename(self, filename: str) -> str:
        """Sanitize filename for Windows file system"""
        # Remove or replace invalid characters
        invalid_chars = r'[<>:"/\\|?*]'
        filename = re.sub(invalid_chars, '_', filename)
        
        # Remove leading/trailing spaces and dots
        filename = filename.strip(' .')
        
        # Limit length to reasonable size
        if len(filename) > 200:
            filename = filename[:200]
        
        # Ensure filename is not empty
        if not filename:
            filename = "Untitled_Song"
            
        return filename
    
    def generate_guid(self) -> str:
        """Generate a GUID for ProPresenter elements"""
        return str(uuid.uuid4()).upper()
    
    def encode_base64(self, text: str) -> str:
        """Encode text to base64 for ProPresenter fields"""
        return base64.b64encode(text.encode('utf-8')).decode('ascii')
    
    def create_rtf_data(self, content: str) -> str:
        """Create RTF data for text content and encode to base64"""
        # Escape special RTF characters
        content = content.replace('\\', '\\\\')
        content = content.replace('{', '\\{')
        content = content.replace('}', '\\}')
        
        # Convert line breaks to RTF paragraphs  
        lines = content.split('\n')
        rtf_lines = []
        
        # Build RTF content with proper formatting
        rtf_header = (
            r'{\rtf1\prortf1\ansi\ansicpg1252\uc1\htmautsp\deff2'
            r'{\fonttbl{\f0\fcharset0 Times New Roman;}{\f2\fcharset0 Georgia;}{\f3\fcharset0 Arial;}{\f4\fcharset0 Impact;}}'
            r'{\colortbl;\red0\green0\blue0;\red255\green255\blue255;}'
            r'\loch\hich\dbch\pard\slleading0\plain\ltrpar\itap0'
            r'{\lang1033\fs120\f3\cf1 \cf1\qc'
        )
        
        for i, line in enumerate(lines):
            if i > 0:
                rtf_lines.append(r'\par}')
            rtf_lines.append(r'{\fs149\f4 {\cf2\ltrch ' + line + r'}\li0\sa0\sb0\fi0\qc')
        
        # Close the RTF structure without adding extra paragraph break
        rtf_content = rtf_header + ''.join(rtf_lines) + r'}}}' 
        
        # Encode to base64
        return base64.b64encode(rtf_content.encode('utf-8')).decode('ascii')
    
    def create_winflow_data(self, content: str) -> str:
        """Create Windows Flow document data and encode to base64"""
        lines = content.split('\n')
        paragraphs = []
        
        for line in lines:
            # Escape XML special characters
            line = line.replace('&', '&amp;')
            line = line.replace('<', '&lt;')
            line = line.replace('>', '&gt;')
            line = line.replace('"', '&quot;')
            line = line.replace("'", '&apos;')
            
            paragraph = (
                f'<Paragraph Margin="0,0,0,0" TextAlignment="Center" FontFamily="Arial" FontSize="60">'
                f'<Run FontFamily="Impact" FontStretch="Condensed" FontSize="75" Foreground="#FFFFFFFF" '
                f'Block.TextAlignment="Center">{line}</Run></Paragraph>'
            )
            paragraphs.append(paragraph)
        
        winflow = (
            '<FlowDocument TextAlignment="Center" PagePadding="5,0,5,0" AllowDrop="True" '
            'xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation">'
            + ''.join(paragraphs) +
            '</FlowDocument>'
        )
        
        return base64.b64encode(winflow.encode('utf-8')).decode('ascii')
    
    def create_winfont_data(self) -> str:
        """Create Windows font data and encode to base64"""
        winfont = (
            '<?xml version="1.0" encoding="utf-16"?>'
            '<RVFont xmlns:i="http://www.w3.org/2001/XMLSchema-instance" '
            'xmlns="http://schemas.datacontract.org/2004/07/ProPresenter.Common">'
            '<Kerning>0</Kerning><LineSpacing>0</LineSpacing>'
            '<OutlineColor xmlns:d2p1="http://schemas.datacontract.org/2004/07/System.Windows.Media">'
            '<d2p1:A>255</d2p1:A><d2p1:B>0</d2p1:B><d2p1:G>0</d2p1:G><d2p1:R>0</d2p1:R>'
            '<d2p1:ScA>1</d2p1:ScA><d2p1:ScB>0</d2p1:ScB><d2p1:ScG>0</d2p1:ScG><d2p1:ScR>0</d2p1:ScR>'
            '</OutlineColor><OutlineWidth>0</OutlineWidth><Variants>Normal</Variants></RVFont>'
        )
        
        # Note: ProPresenter expects UTF-16 encoding for this field
        return base64.b64encode(winfont.encode('utf-16')).decode('ascii')
    
    def get_group_color(self, section_type: str) -> str:
        """Get the color for a slide group based on section type"""
        colors = {
            'verse': '0 0 1 1',        # Blue
            'chorus': '1 0.39 0.39 1',  # Red-ish
            'bridge': '0 0.5 1 1',      # Light blue
            'pre-chorus': '0.5 0 1 1',  # Purple
            'intro': '0.5 0.5 0.5 1',   # Gray
            'outro': '0.5 0.5 0.5 1',   # Gray
            'ending': '0.5 0.5 0.5 1',  # Gray
            'tag': '1 0.5 0 1',         # Orange
            'interlude': '0 1 0.5 1'    # Green
        }
        return colors.get(section_type.lower(), '0 0 0 1')
    
    def format_section_name(self, section_type: str) -> str:
        """Format section name for ProPresenter display"""
        # Section detector now returns properly formatted names like "Verse 1", "Chorus", etc.
        # If it already contains a space and number, use as-is
        if ' ' in section_type and section_type.split()[-1].isdigit():
            return section_type
        
        # Otherwise, apply legacy mapping for backwards compatibility
        section_map = {
            'verse': 'Verse',
            'chorus': 'Chorus', 
            'refrain': 'Chorus',
            'bridge': 'Bridge',
            'pre-chorus': 'Pre-Chorus',
            'intro': 'Intro',
            'outro': 'Outro',
            'ending': 'Outro',
            'tag': 'Tag',
            'interlude': 'Interlude'
        }
        
        return section_map.get(section_type.lower(), section_type.title())
    
    def split_content_into_slides(self, content: str) -> List[str]:
        """Split content into individual slides"""
        slides = []
        lines = content.split('\n')
        current_slide = []
        
        for line in lines:
            line = line.strip()
            if not line:
                # Empty line - potential slide break
                if current_slide:
                    slides.append('\n'.join(current_slide))
                    current_slide = []
            else:
                current_slide.append(line)
        
        # Add final slide if content remains
        if current_slide:
            slides.append('\n'.join(current_slide))
        
        # If no natural breaks, treat as single slide
        if not slides and content.strip():
            slides = [content.strip()]
            
        return slides
    
    def create_pro6_document(self, song_data: Dict[str, Any], sections: List[Dict[str, str]]) -> ET.Element:
        """Create the root ProPresenter 6 XML document with correct structure"""
        
        # Root element with proper attributes
        root = ET.Element('RVPresentationDocument')
        root.set('height', str(self.slide_height))
        root.set('width', str(self.slide_width))
        root.set('docType', '0')
        root.set('versionNumber', '600')
        root.set('usedCount', '0')
        root.set('backgroundColor', '0 0 0 1')
        root.set('drawingBackgroundColor', 'false')
        root.set('CCLIDisplay', 'true' if song_data.get('reference_number') else 'false')
        root.set('lastDateUsed', datetime.now().strftime('%Y-%m-%dT%H:%M:%S+00:00'))
        root.set('selectedArrangementID', '')
        root.set('category', 'Song')
        root.set('resourcesDirectory', '')
        root.set('notes', '')
        
        # CCLI metadata
        root.set('CCLIAuthor', song_data.get('author', ''))
        root.set('CCLIArtistCredits', song_data.get('author', ''))
        root.set('CCLISongTitle', song_data.get('title', 'Untitled'))
        root.set('CCLIPublisher', song_data.get('administrator', ''))
        root.set('CCLICopyrightYear', '')
        root.set('CCLISongNumber', song_data.get('reference_number', ''))
        root.set('chordChartPath', '')
        root.set('os', '1')
        root.set('buildNumber', '6016')
        
        # Timeline
        timeline = ET.SubElement(root, 'RVTimeline')
        timeline.set('timeOffset', '0')
        timeline.set('duration', '0')
        timeline.set('selectedMediaTrackIndex', '-1')
        timeline.set('loop', 'false')
        timeline.set('rvXMLIvarName', 'timeline')
        
        # Time cues array
        time_cues = ET.SubElement(timeline, 'array')
        time_cues.set('rvXMLIvarName', 'timeCues')
        
        # Media tracks array
        media_tracks = ET.SubElement(timeline, 'array')
        media_tracks.set('rvXMLIvarName', 'mediaTracks')
        
        # Groups array for slide groups
        groups_array = ET.SubElement(root, 'array')
        groups_array.set('rvXMLIvarName', 'groups')
        
        # Create slide groups for each section
        for section in sections:
            if not section.get('content', '').strip():
                continue
                
            group = self.create_slide_group(section)
            groups_array.append(group)
        
        # Arrangements array (empty for now)
        arrangements = ET.SubElement(root, 'array')
        arrangements.set('rvXMLIvarName', 'arrangements')
        
        return root
    
    def create_slide_group(self, section: Dict[str, str]) -> ET.Element:
        """Create a slide group with proper ProPresenter 6 structure"""
        
        section_type = section.get('type', 'verse')
        group_name = self.format_section_name(section_type)
        
        group = ET.Element('RVSlideGrouping')
        group.set('name', group_name)
        group.set('color', self.get_group_color(section_type))
        group.set('uuid', self.generate_guid())
        
        # Slides array
        slides_array = ET.SubElement(group, 'array')
        slides_array.set('rvXMLIvarName', 'slides')
        
        # Split content into individual slides
        content = section.get('content', '').strip()
        if not content:
            return group
            
        slides = self.split_content_into_slides(content)
        
        for slide_content in slides:
            slide = self.create_slide(slide_content)
            slides_array.append(slide)
        
        return group
    
    def create_slide(self, content: str) -> ET.Element:
        """Create an individual slide with ProPresenter 6 structure"""
        
        slide = ET.Element('RVDisplaySlide')
        slide.set('backgroundColor', '0 0 0 0')
        slide.set('highlightColor', '')
        slide.set('drawingBackgroundColor', 'false')
        slide.set('enabled', 'true')
        slide.set('hotKey', '')
        slide.set('label', '')
        slide.set('notes', '')
        slide.set('UUID', self.generate_guid())
        slide.set('chordChartPath', '')
        
        # Cues array (empty)
        cues = ET.SubElement(slide, 'array')
        cues.set('rvXMLIvarName', 'cues')
        
        # Display elements array
        display_elements = ET.SubElement(slide, 'array')
        display_elements.set('rvXMLIvarName', 'displayElements')
        
        # Create text element
        text_element = self.create_text_element(content)
        display_elements.append(text_element)
        
        return slide
    
    def create_text_element(self, content: str) -> ET.Element:
        """Create a text element with proper encoding and structure"""
        
        element = ET.Element('RVTextElement')
        element.set('displayName', 'Default')
        element.set('UUID', self.generate_guid())
        element.set('typeID', '0')
        element.set('displayDelay', '0')
        element.set('locked', 'false')
        element.set('persistent', '0')
        element.set('fromTemplate', 'false')
        element.set('opacity', '1')
        element.set('source', '')
        element.set('bezelRadius', '0')
        element.set('rotation', '0')
        element.set('drawingFill', 'false')
        element.set('drawingShadow', 'false')
        element.set('drawingStroke', 'false')
        element.set('fillColor', '1 1 1 1')
        element.set('adjustsHeightToFit', 'false')
        element.set('verticalAlignment', '0')
        element.set('revealType', '0')
        
        # Position - ProPresenter uses special format: {x y z width height}
        position = ET.SubElement(element, 'RVRect3D')
        position.set('rvXMLIvarName', 'position')
        # Calculate position with padding
        x = self.text_padding
        y = self.text_padding
        width = self.slide_width - (self.text_padding * 2)
        height = self.slide_height - (self.text_padding * 2)
        position.text = f'{{{x} {y} 0 {width} {height}}}'
        
        # Shadow
        shadow = ET.SubElement(element, 'shadow')
        shadow.set('rvXMLIvarName', 'shadow')
        shadow.text = '10|0 0 0 1|{4.94974746830583, -4.94974746830583}'
        
        # Stroke dictionary
        stroke_dict = ET.SubElement(element, 'dictionary')
        stroke_dict.set('rvXMLIvarName', 'stroke')
        
        stroke_color = ET.SubElement(stroke_dict, 'NSColor')
        stroke_color.set('rvXMLDictionaryKey', 'RVShapeElementStrokeColorKey')
        stroke_color.text = '0 0 0 1'
        
        stroke_width = ET.SubElement(stroke_dict, 'NSNumber')
        stroke_width.set('rvXMLDictionaryKey', 'RVShapeElementStrokeWidthKey')
        stroke_width.set('hint', 'double')
        stroke_width.text = '0'
        
        # Plain text (base64 encoded)
        plain_text = ET.SubElement(element, 'NSString')
        plain_text.set('rvXMLIvarName', 'PlainText')
        # Ensure content is properly trimmed and convert line endings
        trimmed_content = content.strip()
        clean_content = trimmed_content.replace('\r\n', '\n').replace('\n', '\r\n')
        plain_text.text = self.encode_base64(clean_content)
        
        # RTF data (base64 encoded)
        rtf_data = ET.SubElement(element, 'NSString')
        rtf_data.set('rvXMLIvarName', 'RTFData')
        rtf_data.text = self.create_rtf_data(trimmed_content)
        
        # WinFlow data (base64 encoded)
        winflow_data = ET.SubElement(element, 'NSString')
        winflow_data.set('rvXMLIvarName', 'WinFlowData')
        winflow_data.text = self.create_winflow_data(trimmed_content)
        
        # WinFont data (base64 encoded)
        winfont_data = ET.SubElement(element, 'NSString')
        winfont_data.set('rvXMLIvarName', 'WinFontData')
        winfont_data.text = self.create_winfont_data()
        
        return element
        
    def ensure_proper_array_tags(self, element):
        """Ensure empty array elements have proper opening/closing tags by adding empty text"""
        for array_elem in element.iter('array'):
            if array_elem.text is None and len(list(array_elem)) == 0:
                # Add empty text to prevent self-closing
                array_elem.text = ''
    
    def fix_self_closing_tags(self, xml_string: str) -> str:
        """Fix self-closing array tags to have proper opening/closing tags"""
        # Replace self-closing array tags with proper opening/closing tags
        import re
        
        # Pattern to match self-closing array tags
        pattern = r'<array([^>]*?)rvXMLIvarName="([^"]*?)"([^>]*?)/>'
        
        # Replace with opening and closing tags
        def replace_func(match):
            attrs_before = match.group(1)
            var_name = match.group(2)
            attrs_after = match.group(3)
            return f'<array{attrs_before}rvXMLIvarName="{var_name}"{attrs_after}></array>'
        
        return re.sub(pattern, replace_func, xml_string)
    
    def export_song(self, song_data: Dict[str, Any], sections: List[Dict[str, str]], 
                   output_path: Path) -> Tuple[bool, str]:
        """Export a single song to ProPresenter 6 format"""
        
        try:
            # Create XML document
            root = self.create_pro6_document(song_data, sections)
            
            # Ensure empty arrays have proper tags
            self.ensure_proper_array_tags(root)
            
            # Create filename
            title = song_data.get('title', 'Untitled')
            clean_title = self.sanitize_filename(title)
            filename = f"{clean_title}.pro6"
            full_path = output_path / filename
            
            # Ensure output directory exists
            output_path.mkdir(parents=True, exist_ok=True)
            
            # Convert to string with proper formatting
            xml_str = ET.tostring(root, encoding='unicode')
            
            # Fix self-closing array tags before pretty printing
            xml_str = self.fix_self_closing_tags(xml_str)
            
            # Pretty print using minidom
            dom = xml.dom.minidom.parseString(xml_str)
            pretty_xml = dom.toprettyxml(indent="  ", encoding='utf-8')
            
            # Decode from bytes to string for final processing
            if isinstance(pretty_xml, bytes):
                pretty_xml = pretty_xml.decode('utf-8')
            
            # Apply fix again after pretty printing (in case minidom creates new self-closing tags)
            pretty_xml = self.fix_self_closing_tags(pretty_xml)
            
            # Write to file
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(pretty_xml)
            
            return True, str(full_path)
            
        except Exception as e:
            error_msg = f"Failed to export '{song_data.get('title', 'Unknown')}': {str(e)}"
            return False, error_msg
    
    def export_songs_batch(self, songs_with_sections: List[Tuple[Dict[str, Any], List[Dict[str, str]]]], 
                          output_path: Path, progress_callback=None) -> Tuple[List[str], List[str]]:
        """Export multiple songs with progress tracking"""
        
        successful_exports = []
        failed_exports = []
        total_songs = len(songs_with_sections)
        
        for i, (song_data, sections) in enumerate(songs_with_sections):
            try:
                # Update progress
                if progress_callback:
                    progress_callback(i, total_songs, song_data.get('title', 'Unknown'))
                
                # Export song
                success, result = self.export_song(song_data, sections, output_path)
                
                if success:
                    successful_exports.append(result)
                else:
                    failed_exports.append(result)
                    
            except Exception as e:
                error_msg = f"Unexpected error exporting '{song_data.get('title', 'Unknown')}': {str(e)}"
                failed_exports.append(error_msg)
        
        # Final progress update
        if progress_callback:
            progress_callback(total_songs, total_songs, "Export complete")
        
        return successful_exports, failed_exports


def create_sample_pro6():
    """Create a sample .pro6 file for testing"""
    exporter = ProPresenter6Exporter()
    
    sample_song = {
        'title': 'Amazing Grace',
        'author': 'John Newton',
        'copyright': 'Public Domain',
        'administrator': '',
        'reference_number': '12345'
    }
    
    sample_sections = [
        {
            'type': 'verse',
            'content': 'Amazing grace how sweet the sound\nThat saved a wretch like me\n\nI once was lost but now am found\nWas blind but now I see'
        },
        {
            'type': 'verse', 
            'content': 'Twas grace that taught my heart to fear\nAnd grace my fears relieved\n\nHow precious did that grace appear\nThe hour I first believed'
        },
        {
            'type': 'chorus',
            'content': 'My chains are gone, I\'ve been set free\nMy God, my Savior has ransomed me\n\nAnd like a flood His mercy reigns\nUnending love, amazing grace'
        }
    ]
    
    success, result = exporter.export_song(sample_song, sample_sections, Path("./"))
    print(f"Sample export: {success} - {result}")


if __name__ == "__main__":
    create_sample_pro6()