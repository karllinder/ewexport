"""
ProPresenter 6 XML export functionality
"""

import xml.etree.ElementTree as ET
import uuid
import re
from pathlib import Path
from typing import List, Dict, Optional, Any, Tuple
from datetime import datetime

class ProPresenterExporter:
    """Handles export to ProPresenter 6 (.pro6) format"""
    
    def __init__(self):
        self.slide_width = 1920
        self.slide_height = 1080
        self.default_font_size = 60
        self.line_spacing = 1.2
        
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
    
    def create_pro6_document(self, song_data: Dict[str, Any], sections: List[Dict[str, str]]) -> ET.Element:
        """Create the root ProPresenter 6 XML document"""
        
        # Root element
        root = ET.Element('RVPresentationDocument', {
            'height': str(self.slide_height),
            'width': str(self.slide_width),
            'versionNumber': '600',
            'docType': '0',
            'creatorCode': '1349676880',
            'lastDateUsed': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'usedCount': '0',
            'category': 'Song',
            'resourcesDirectory': '',
            'backgroundColor': '0 0 0 1',
            'drawingBackgroundColor': '0',
            'notes': '',
            'artist': song_data.get('author', ''),
            'author': song_data.get('author', ''),
            'album': '',
            'CCLIDisplay': '1' if song_data.get('reference_number') else '0',
            'CCLIArtistCredits': '',
            'CCLIPublisher': song_data.get('administrator', ''),
            'CCLICopyright': song_data.get('copyright', ''),
            'CCLISongTitle': song_data['title'],
            'CCLIAuthor': song_data.get('author', ''),
            'CCLISongNumber': song_data.get('reference_number', ''),
            'CCLILicenseNumber': ''
        })
        
        # Timeline
        timeline = ET.SubElement(root, 'timeline', {
            'timeOffSet': '0',
            'selectedMediaTrackIndex': '0',
            'unitOfMeasure': '60',
            'duration': '0',
            'loop': '0'
        })
        
        # Media tracks
        media_tracks = ET.SubElement(timeline, 'timeCues')
        
        # Slide groups container
        groups = ET.SubElement(root, 'groups')
        
        # Arrangements
        arrangements = ET.SubElement(root, 'arrangements')
        
        # Create slides for each section
        slide_index = 0
        for section in sections:
            group_name = self.format_section_name(section['type'])
            group = self.create_slide_group(group_name, section, slide_index)
            groups.append(group)
            
            # Count slides in this section
            section_content = section['content'].strip()
            if section_content:
                section_slides = self.split_content_into_slides(section_content)
                slide_index += len(section_slides)
        
        return root
    
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
    
    def create_slide_group(self, group_name: str, section: Dict[str, str], start_index: int) -> ET.Element:
        """Create a slide group for a song section"""
        
        group = ET.Element('RVSlideGrouping', {
            'name': group_name,
            'uuid': self.generate_guid(),
            'color': '0 0 0 0',
            'serialNumber': str(start_index)
        })
        
        # Split section content into individual slides
        content = section['content'].strip()
        if not content:
            return group
            
        slides = self.split_content_into_slides(content)
        
        for i, slide_content in enumerate(slides):
            slide = self.create_slide(slide_content, start_index + i)
            group.append(slide)
        
        return group
    
    def split_content_into_slides(self, content: str) -> List[str]:
        """Split content into individual slides"""
        # Split on double line breaks or explicit slide markers
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
    
    def create_slide(self, content: str, index: int) -> ET.Element:
        """Create an individual slide element"""
        
        slide = ET.Element('RVDisplaySlide', {
            'backgroundColor': '0 0 0 0',
            'enabled': '1',
            'highlightColor': '0 0 0 0',
            'hotKey': '',
            'label': '',
            'notes': '',
            'slideType': '1',
            'sort_index': str(index),
            'UUID': self.generate_guid(),
            'drawingBackgroundColor': '0',
            'chordChartPath': '',
            'serialNumber': str(index)
        })
        
        # Create cues
        cues = ET.SubElement(slide, 'cues')
        
        # Create display elements
        display_elements = ET.SubElement(slide, 'displayElements')
        
        # Create text element
        text_element = self.create_text_element(content)
        display_elements.append(text_element)
        
        return slide
    
    def create_text_element(self, content: str) -> ET.Element:
        """Create a text element for slide content"""
        
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
            'RTFData': self.create_rtf_data(content),
            'serialNumber': '0',
            'opacity': '1'
        })
        
        # Position and size
        ET.SubElement(element, 'position', {
            'x': '0',
            'y': '0',
            'z': '0'
        })
        
        ET.SubElement(element, 'size', {
            'width': str(self.slide_width),
            'height': str(self.slide_height)
        })
        
        # Shadow properties
        shadow = ET.SubElement(element, 'shadow', {
            'shadowColor': '0 0 0 1',
            'shadowOffset': '0 0',
            'shadowBlurRadius': '5'
        })
        
        return element
    
    def create_rtf_data(self, content: str) -> str:
        """Create RTF data for text content"""
        # Escape special RTF characters
        content = content.replace('\\', '\\\\')
        content = content.replace('{', '\\{')
        content = content.replace('}', '\\}')
        
        # Convert line breaks to RTF
        content = content.replace('\n', '\\line\n')
        
        # Basic RTF with centered text and default font
        rtf_content = (
            r'{\rtf1\ansi\deff0 '
            r'{\fonttbl {\f0 Arial;}} '
            r'{\colortbl ;\red255\green255\blue255;} '
            f'\\f0\\fs{self.default_font_size * 2}\\cf1\\qc '  # *2 because RTF font size is in half-points
            f'{content}'
            r'}'
        )
        
        return rtf_content
    
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
            ET.indent(tree, space="  ", level=0)  # Pretty formatting
            
            with open(full_path, 'wb') as f:
                tree.write(f, encoding='utf-8', xml_declaration=True)
            
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


def create_sample_pro6():
    """Create a sample .pro6 file for testing"""
    exporter = ProPresenterExporter()
    
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
            'content': 'Amazing grace how sweet the sound\nThat saved a wretch like me\nI once was lost but now am found\nWas blind but now I see'
        },
        {
            'type': 'verse', 
            'content': 'Twas grace that taught my heart to fear\nAnd grace my fears relieved\nHow precious did that grace appear\nThe hour I first believed'
        }
    ]
    
    success, result = exporter.export_song(sample_song, sample_sections, Path("./"))
    print(f"Sample export: {success} - {result}")


if __name__ == "__main__":
    create_sample_pro6()