"""
ProPresenter 6 XML export functionality - Corrected format
Based on propresenter-parser documentation
"""

import xml.etree.ElementTree as ET
import uuid
import re
from pathlib import Path
from typing import List, Dict, Optional, Any, Tuple
from datetime import datetime

class ProPresenter6Exporter:
    """Handles export to ProPresenter 6 (.pro6) format with correct XML structure"""
    
    def __init__(self):
        self.slide_width = 1920
        self.slide_height = 1080
        self.default_font_size = 60
        self.default_font_name = 'Arial'
        
    def sanitize_filename(self, filename: str) -> str:
        """Sanitize filename for Windows file system"""
        invalid_chars = r'[<>:"/\\|?*]'
        filename = re.sub(invalid_chars, '_', filename)
        filename = filename.strip(' .')
        if len(filename) > 200:
            filename = filename[:200]
        if not filename:
            filename = "Untitled_Song"
        return filename
    
    def generate_uuid(self) -> str:
        """Generate a UUID for ProPresenter elements"""
        return str(uuid.uuid4()).upper()
    
    def create_pro6_document(self, song_data: Dict[str, Any], sections: List[Dict[str, str]]) -> ET.Element:
        """Create the root ProPresenter 6 XML document with correct structure"""
        
        # Root element with all required attributes
        root = ET.Element('RVPresentationDocument', {
            'height': str(self.slide_height),
            'width': str(self.slide_width),
            'versionNumber': '600',
            'docType': '0',
            'creatorCode': '1349676880',
            'lastDateUsed': datetime.now().strftime('%Y-%m-%dT%H:%M:%S+00:00'),
            'usedCount': '0',
            'category': 'Song',
            'resourcesDirectory': '',
            'backgroundColor': '0 0 0 1',
            'drawingBackgroundColor': '0',
            'notes': song_data.get('description', ''),
            'artist': song_data.get('author', ''),
            'author': song_data.get('author', ''),
            'album': '',
            'CCLIDisplay': '1' if song_data.get('reference_number') else '0',
            'CCLIArtistCredits': song_data.get('author', ''),
            'CCLIPublisher': song_data.get('administrator', ''),
            'CCLICopyright': song_data.get('copyright', ''),
            'CCLISongTitle': song_data['title'],
            'CCLIAuthor': song_data.get('author', ''),
            'CCLISongNumber': song_data.get('reference_number', ''),
            'CCLILicenseNumber': ''
        })
        
        # Timeline (required but can be empty)
        timeline = ET.SubElement(root, 'timeline', {
            'timeOffSet': '0',
            'selectedMediaTrackIndex': '0',
            'unitOfMeasure': '60',
            'duration': '0',
            'loop': '0'
        })
        ET.SubElement(timeline, 'timeCues')
        
        # Groups container
        groups = ET.SubElement(root, 'groups')
        
        # Create slide groups for each section
        for i, section in enumerate(sections):
            group = self.create_slide_group(section, i)
            groups.append(group)
        
        # Arrangements (optional but good to include)
        arrangements = ET.SubElement(root, 'arrangements')
        arrangement = self.create_default_arrangement(sections)
        arrangements.append(arrangement)
        
        return root
    
    def create_slide_group(self, section: Dict[str, str], index: int) -> ET.Element:
        """Create a slide group (verse, chorus, etc.) with proper structure"""
        
        group_name = self.format_section_name(section['type'])
        group_uuid = self.generate_uuid()
        
        group = ET.Element('RVSlideGrouping', {
            'name': group_name,
            'uuid': group_uuid,
            'color': '0 0 0 0',
            'serialNumber': str(index)
        })
        
        # Split content into slides 
        content = section['content'].strip()
        if not content:
            content = 'No lyrics available'
            
        slides = self.split_content_into_slides(content)
        
        for slide_index, slide_content in enumerate(slides):
            slide = self.create_slide(slide_content, index * 100 + slide_index)
            group.append(slide)
        
        return group
    
    def format_section_name(self, section_type: str) -> str:
        """Format section name for ProPresenter display"""
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
        """Split content into individual slides based on line breaks"""
        # For now, treat each section as a single slide
        # This can be enhanced later to split on double line breaks
        return [content] if content.strip() else ['']
    
    def create_slide(self, content: str, serial_number: int) -> ET.Element:
        """Create an individual slide with proper structure"""
        
        slide_uuid = self.generate_uuid()
        
        slide = ET.Element('RVDisplaySlide', {
            'backgroundColor': '0 0 0 0',
            'enabled': '1',
            'highlightColor': '0 0 0 0',
            'hotKey': '',
            'label': '',
            'notes': '',
            'slideType': '1',
            'sort_index': str(serial_number),
            'UUID': slide_uuid,
            'drawingBackgroundColor': '0',
            'chordChartPath': '',
            'serialNumber': str(serial_number)
        })
        
        # Cues (required but can be empty)
        ET.SubElement(slide, 'cues')
        
        # Display elements
        display_elements = ET.SubElement(slide, 'displayElements')
        
        # Text element
        text_element = self.create_text_element(content)
        display_elements.append(text_element)
        
        return slide
    
    def create_text_element(self, content: str) -> ET.Element:
        """Create a text element with proper RTF, FlowData, and FontData"""
        
        element_uuid = self.generate_uuid()
        
        element = ET.Element('RVTextElement', {
            'displayDelay': '0',
            'displayName': 'Default',
            'locked': '0',
            'persistent': '0',
            'typeID': '0',
            'fromTemplate': '0',
            'bezelRadius': '0',
            'drawingFill': '0',
            'drawingShadow': '1',
            'drawingStroke': '0',
            'fillColor': '0 0 0 0',
            'rotation': '0',
            'source': '',
            'adjustsHeightToFit': '0',
            'verticalAlignment': '0',
            'opacity': '1',
            'UUID': element_uuid
        })
        
        # Position (full slide)
        position = ET.SubElement(element, 'position', {
            'x': '20',
            'y': '20', 
            'z': '0'
        })
        
        # Size (with padding)
        size = ET.SubElement(element, 'size', {
            'width': str(self.slide_width - 40),  # 20px padding each side
            'height': str(self.slide_height - 40)
        })
        
        # Shadow
        shadow = ET.SubElement(element, 'shadow', {
            'shadowColor': '0 0 0 1',
            'shadowOffset': '0 0',
            'shadowBlurRadius': '5'
        })
        
        # Store content for RTF generation
        self.add_text_content(element, content)
        
        return element
    
    def add_text_content(self, element: ET.Element, content: str):
        """Add text content as RTF, FlowData, and FontData"""
        
        # Clean content for RTF
        rtf_content = self.escape_rtf_content(content)
        
        # RTF Data
        rtf_data = self.create_rtf_data(rtf_content)
        element.set('RTFData', rtf_data)
        
        # Add FlowData (Windows Flow Document) - must be escaped XML text
        flow_data = self.create_flow_data(content)
        flow_element = ET.SubElement(element, 'FlowData')
        flow_element.text = flow_data
        
        # Add FontData
        font_data = self.create_font_data()
        font_element = ET.SubElement(element, 'FontData') 
        font_element.text = font_data
    
    def escape_rtf_content(self, content: str) -> str:
        """Escape special RTF characters"""
        content = content.replace('\\', '\\\\')
        content = content.replace('{', '\\{')
        content = content.replace('}', '\\}')
        return content
    
    def create_rtf_data(self, content: str) -> str:
        """Create proper RTF data format"""
        # Convert line breaks
        rtf_lines = []
        for line in content.split('\n'):
            if line.strip():
                rtf_lines.append(f'{{\\cf2\\ltrch {line}}}\\li0\\sa0\\sb0\\fi0\\qc\\par')
        
        rtf_content = '\\r\\n'.join(rtf_lines)
        
        rtf_data = (
            f'{{\\rtf1\\prortf1\\ansi\\ansicpg1252\\uc1\\htmautsp\\deff2'
            f'{{\\fonttbl{{\\f0\\fcharset0 Times New Roman;}}{{\\f2\\fcharset0 Georgia;}}{{\\f3\\fcharset0 Arial;}}{{\\f4\\fcharset0 {self.default_font_name};}}}}' 
            f'{{\\colortbl;\\red0\\green0\\blue0;\\red255\\green255\\blue255;}}'
            f'\\loch\\hich\\dbch\\pard\\slleading0\\plain\\ltrpar\\itap0'
            f'{{\\lang1033\\fs{self.default_font_size * 2}\\f3\\cf1 \\cf1\\qc'
            f'{{\\fs{self.default_font_size * 2}\\f4 {rtf_content}}}\\r\\n}}'
        )
        
        return rtf_data
    
    def create_flow_data(self, content: str) -> str:
        """Create Windows FlowDocument data as escaped XML"""
        # First escape the text content that will go inside the XML
        text_content = content.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')
        
        # Create paragraphs for each line
        paragraphs = []
        for line in text_content.split('\n'):
            if line.strip():
                paragraphs.append(
                    f'<Paragraph Margin="0,0,0,0" TextAlignment="Center" FontFamily="{self.default_font_name}" FontSize="{self.default_font_size}">'
                    f'<Run FontFamily="{self.default_font_name}" FontSize="{self.default_font_size}" Foreground="#FFFFFFFF" Block.TextAlignment="Center">'
                    f'{line.strip()}</Run></Paragraph>'
                )
        
        # Create the FlowDocument XML
        flow_xml = (
            f'<FlowDocument TextAlignment="Center" PagePadding="5,0,5,0" AllowDrop="True" '
            f'xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation">'
            f'{"".join(paragraphs)}</FlowDocument>'
        )
        
        # Now escape the entire XML for storage in the text content
        escaped_flow_data = (
            flow_xml.replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;')
        )
        
        return escaped_flow_data
    
    def create_font_data(self) -> str:
        """Create font data XML"""
        font_data = (
            '<?xml version="1.0" encoding="utf-16"?>'
            '<RVFont xmlns:i="http://www.w3.org/2001/XMLSchema-instance" '
            'xmlns="http://schemas.datacontract.org/2004/07/ProPresenter.Common">'
            '<Kerning>0</Kerning><LineSpacing>0</LineSpacing>'
            '<OutlineColor xmlns:d2p1="http://schemas.datacontract.org/2004/07/System.Windows.Media">'
            '<d2p1:A>255</d2p1:A><d2p1:B>0</d2p1:B><d2p1:G>0</d2p1:G><d2p1:R>0</d2p1:R>'
            '<d2p1:ScA>1</d2p1:ScA><d2p1:ScB>0</d2p1:ScB><d2p1:ScG>0</d2p1:ScG><d2p1:ScR>0</d2p1:ScR>'
            '</OutlineColor><OutlineWidth>0</OutlineWidth><Variants>Normal</Variants></RVFont>'
        )
        return font_data
    
    def create_default_arrangement(self, sections: List[Dict[str, str]]) -> ET.Element:
        """Create a default arrangement that includes all sections"""
        
        arrangement_uuid = self.generate_uuid()
        
        arrangement = ET.Element('RVSlideGrouping', {
            'name': 'Default',
            'uuid': arrangement_uuid,
            'color': '0 0 0 0', 
            'serialNumber': '0'
        })
        
        # Add references to all sections in order
        for i, section in enumerate(sections):
            group_ref = ET.SubElement(arrangement, 'groupIDs', {
                'containerClass': 'NSMutableArray'
            })
            group_ref.text = self.generate_uuid()  # This should match the group UUIDs
        
        return arrangement
    
    def export_song(self, song_data: Dict[str, Any], sections: List[Dict[str, str]], 
                   output_path: Path) -> Tuple[bool, str]:
        """Export a single song to ProPresenter 6 format"""
        
        try:
            # Create XML document  
            root = self.create_pro6_document(song_data, sections)
            
            # Create filename
            title = song_data['title']
            clean_title = self.sanitize_filename(title)
            filename = f"{clean_title}.pro6"
            full_path = output_path / filename
            
            # Ensure output directory exists
            output_path.mkdir(parents=True, exist_ok=True)
            
            # Create XML tree and write to file
            tree = ET.ElementTree(root)
            
            # Write with proper XML declaration
            with open(full_path, 'wb') as f:
                f.write(b'<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n')
                tree.write(f, encoding='utf-8', xml_declaration=False)
            
            return True, str(full_path)
            
        except Exception as e:
            error_msg = f"Failed to export '{song_data['title']}': {str(e)}"
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
                    progress_callback(i, total_songs, song_data['title'])
                
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


def create_sample_pro6_v2():
    """Create a sample .pro6 file for testing with correct format"""
    exporter = ProPresenter6Exporter()
    
    sample_song = {
        'title': 'Amazing Grace (Corrected Format)',
        'author': 'John Newton',
        'copyright': 'Public Domain',
        'administrator': '',
        'reference_number': '12345'
    }
    
    sample_sections = [
        {
            'type': 'verse',
            'content': 'Amazing grace how sweet the sound\nThat saved a wretch like me\nI once was lost but now am found\nWas blind but now I see'
        },
        {
            'type': 'verse', 
            'content': 'Twas grace that taught my heart to fear\nAnd grace my fears relieved\nHow precious did that grace appear\nThe hour I first believed'
        }
    ]
    
    success, result = exporter.export_song(sample_song, sample_sections, Path("./"))
    print(f"Corrected format sample export: {success} - {result}")


if __name__ == "__main__":
    create_sample_pro6_v2()