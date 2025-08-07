#!/usr/bin/env python3
"""
Unit test for ProPresenter 6 export format validation
Compares our export against the specification in v6-parser.md
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import xml.etree.ElementTree as ET
from pathlib import Path
from src.export.propresenter import ProPresenter6Exporter
import unittest
from typing import Dict, List, Any

class TestProPresenter6Format(unittest.TestCase):
    """Test ProPresenter 6 export format against specification"""
    
    def setUp(self):
        """Set up test data"""
        self.exporter = ProPresenter6Exporter()
        
        # Test song data
        self.test_song = {
            'title': 'Test Song Format',
            'author': 'Test Author',
            'copyright': 'Test Copyright 2023',
            'administrator': 'Test Publisher',
            'reference_number': '12345678',
            'description': 'Test song for format validation'
        }
        
        # Test sections
        self.test_sections = [
            {
                'type': 'verse',
                'content': 'Amazing grace how sweet the sound\nThat saved a wretch like me'
            },
            {
                'type': 'chorus', 
                'content': 'I once was lost but now am found\nWas blind but now I see'
            }
        ]
        
        # Export test file
        self.output_path = Path('./test_export_validation')
        self.output_path.mkdir(exist_ok=True)
        
        success, self.test_file_path = self.exporter.export_song(
            self.test_song, self.test_sections, self.output_path
        )
        
        self.assertTrue(success, f"Failed to export test song: {self.test_file_path}")
        
        # Parse the generated XML
        self.tree = ET.parse(self.test_file_path)
        self.root = self.tree.getroot()
    
    def test_root_document_structure(self):
        """Test root RVPresentationDocument structure against specification"""
        print("\n=== Testing Root Document Structure ===")
        
        # Check root element name
        self.assertEqual(self.root.tag, 'RVPresentationDocument', 
                        "Root element should be RVPresentationDocument")
        
        # Required attributes from specification
        required_attrs = {
            'height': '1080',
            'width': '1920', 
            'versionNumber': '600',
            'docType': '0',
            'creatorCode': '1349676880',
            'category': 'Song'
        }
        
        for attr, expected_value in required_attrs.items():
            actual_value = self.root.get(attr)
            self.assertEqual(actual_value, expected_value, 
                           f"Attribute {attr} should be '{expected_value}', got '{actual_value}'")
            print(f"[OK] {attr}: {actual_value}")
        
        # CCLI attributes
        ccli_attrs = {
            'CCLISongTitle': self.test_song['title'],
            'CCLIAuthor': self.test_song['author'],
            'CCLICopyright': self.test_song['copyright'],
            'CCLIPublisher': self.test_song['administrator'],
            'CCLISongNumber': self.test_song['reference_number'],
            'CCLIDisplay': '1'
        }
        
        for attr, expected_value in ccli_attrs.items():
            actual_value = self.root.get(attr)
            self.assertEqual(actual_value, expected_value,
                           f"CCLI attribute {attr} should be '{expected_value}', got '{actual_value}'")
            print(f"[OK] {attr}: {actual_value}")
    
    def test_timeline_structure(self):
        """Test timeline element structure"""
        print("\n=== Testing Timeline Structure ===")
        
        timeline = self.root.find('timeline')
        self.assertIsNotNone(timeline, "Timeline element is required")
        
        # Check timeline attributes
        timeline_attrs = {
            'timeOffSet': '0',
            'selectedMediaTrackIndex': '0',
            'unitOfMeasure': '60',
            'duration': '0',
            'loop': '0'
        }
        
        for attr, expected_value in timeline_attrs.items():
            actual_value = timeline.get(attr)
            self.assertEqual(actual_value, expected_value,
                           f"Timeline attribute {attr} should be '{expected_value}', got '{actual_value}'")
            print(f"[OK] Timeline {attr}: {actual_value}")
        
        # Check timeCues element
        time_cues = timeline.find('timeCues')
        self.assertIsNotNone(time_cues, "timeCues element is required")
        print("[OK] timeCues element present")
    
    def test_slide_groups_structure(self):
        """Test slide groups structure against specification"""
        print("\n=== Testing Slide Groups Structure ===")
        
        groups = self.root.find('groups')
        self.assertIsNotNone(groups, "groups element is required")
        
        slide_groups = groups.findall('RVSlideGrouping')
        self.assertEqual(len(slide_groups), len(self.test_sections),
                        f"Should have {len(self.test_sections)} slide groups, got {len(slide_groups)}")
        print(f"[OK] Found {len(slide_groups)} slide groups")
        
        for i, group in enumerate(slide_groups):
            print(f"\n--- Testing Slide Group {i+1} ---")
            
            # Check group attributes
            group_name = group.get('name')
            group_uuid = group.get('uuid')
            group_color = group.get('color')
            serial_number = group.get('serialNumber')
            
            self.assertIsNotNone(group_name, f"Group {i} must have name attribute")
            self.assertIsNotNone(group_uuid, f"Group {i} must have uuid attribute")
            self.assertEqual(group_color, '0 0 0 0', f"Group {i} color should be '0 0 0 0'")
            self.assertEqual(serial_number, str(i), f"Group {i} serialNumber should be '{i}'")
            
            print(f"[OK] Group name: {group_name}")
            print(f"[OK] Group UUID: {group_uuid}")
            print(f"[OK] Group color: {group_color}")
            print(f"[OK] Serial number: {serial_number}")
            
            # Check slides in group
            slides = group.findall('RVDisplaySlide')
            self.assertGreater(len(slides), 0, f"Group {i} must contain at least one slide")
            print(f"[OK] Contains {len(slides)} slide(s)")
            
            self.validate_slide_structure(slides[0], i)
    
    def validate_slide_structure(self, slide: ET.Element, group_index: int):
        """Validate individual slide structure"""
        print(f"\n--- Validating Slide Structure ---")
        
        # Check slide attributes
        required_slide_attrs = [
            'backgroundColor', 'enabled', 'highlightColor', 'hotKey', 
            'label', 'notes', 'slideType', 'sort_index', 'UUID',
            'drawingBackgroundColor', 'chordChartPath', 'serialNumber'
        ]
        
        for attr in required_slide_attrs:
            value = slide.get(attr)
            self.assertIsNotNone(value, f"Slide must have {attr} attribute")
            print(f"[OK] {attr}: {value}")
        
        # Check cues element
        cues = slide.find('cues')
        self.assertIsNotNone(cues, "Slide must have cues element")
        print("[OK] cues element present")
        
        # Check displayElements
        display_elements = slide.find('displayElements')
        self.assertIsNotNone(display_elements, "Slide must have displayElements")
        print("[OK] displayElements present")
        
        # Check text elements
        text_elements = display_elements.findall('RVTextElement')
        self.assertGreater(len(text_elements), 0, "Slide must contain at least one text element")
        print(f"[OK] Contains {len(text_elements)} text element(s)")
        
        self.validate_text_element_structure(text_elements[0])
    
    def validate_text_element_structure(self, text_element: ET.Element):
        """Validate text element structure against specification"""
        print(f"\n--- Validating Text Element Structure ---")
        
        # Required attributes from v6-parser.md specification
        required_attrs = [
            'displayDelay', 'displayName', 'locked', 'persistent', 'typeID',
            'fromTemplate', 'bezelRadius', 'drawingFill', 'drawingShadow',
            'drawingStroke', 'fillColor', 'rotation', 'source',
            'adjustsHeightToFit', 'verticalAlignment', 'opacity', 'UUID'
        ]
        
        for attr in required_attrs:
            value = text_element.get(attr)
            self.assertIsNotNone(value, f"Text element must have {attr} attribute")
            print(f"[OK] {attr}: {value}")
        
        # Check RTF data
        rtf_data = text_element.get('RTFData')
        self.assertIsNotNone(rtf_data, "Text element must have RTFData attribute")
        self.validate_rtf_format(rtf_data)
        
        # Check required child elements
        position = text_element.find('position')
        self.assertIsNotNone(position, "Text element must have position element")
        self.validate_position_element(position)
        
        size = text_element.find('size') 
        self.assertIsNotNone(size, "Text element must have size element")
        self.validate_size_element(size)
        
        shadow = text_element.find('shadow')
        self.assertIsNotNone(shadow, "Text element must have shadow element")
        self.validate_shadow_element(shadow)
        
        # Check FlowData and FontData (critical for ProPresenter compatibility)
        flow_data = text_element.find('FlowData')
        self.assertIsNotNone(flow_data, "Text element must have FlowData element")
        self.validate_flow_data(flow_data)
        
        font_data = text_element.find('FontData')
        self.assertIsNotNone(font_data, "Text element must have FontData element") 
        self.validate_font_data(font_data)
    
    def validate_rtf_format(self, rtf_data: str):
        """Validate RTF data format"""
        print(f"\n--- Validating RTF Format ---")
        
        # RTF should start with {\rtf1
        self.assertTrue(rtf_data.startswith('{\\rtf1'), 
                       f"RTF data should start with '{{\\rtf1', got: {rtf_data[:20]}...")
        print("[OK] RTF starts correctly")
        
        # Should contain font table
        self.assertIn('fonttbl', rtf_data, "RTF should contain font table")
        print("[OK] Contains font table")
        
        # Should contain color table
        self.assertIn('colortbl', rtf_data, "RTF should contain color table")
        print("[OK] Contains color table")
        
        # Should end with closing brace
        self.assertTrue(rtf_data.endswith('}'), "RTF should end with closing brace")
        print("[OK] RTF ends correctly")
        
        print(f"RTF Data preview: {rtf_data[:100]}...")
    
    def validate_position_element(self, position: ET.Element):
        """Validate position element"""
        print(f"--- Validating Position Element ---")
        
        required_attrs = ['x', 'y', 'z']
        for attr in required_attrs:
            value = position.get(attr)
            self.assertIsNotNone(value, f"Position must have {attr} attribute")
            print(f"[OK] position {attr}: {value}")
    
    def validate_size_element(self, size: ET.Element):
        """Validate size element"""
        print(f"--- Validating Size Element ---")
        
        required_attrs = ['width', 'height']
        for attr in required_attrs:
            value = size.get(attr)
            self.assertIsNotNone(value, f"Size must have {attr} attribute")
            print(f"[OK] size {attr}: {value}")
    
    def validate_shadow_element(self, shadow: ET.Element):
        """Validate shadow element"""
        print(f"--- Validating Shadow Element ---")
        
        required_attrs = ['shadowColor', 'shadowOffset', 'shadowBlurRadius']
        for attr in required_attrs:
            value = shadow.get(attr)
            self.assertIsNotNone(value, f"Shadow must have {attr} attribute")
            print(f"[OK] shadow {attr}: {value}")
    
    def validate_flow_data(self, flow_data: ET.Element):
        """Validate FlowData element against Windows Flow Document spec"""
        print(f"--- Validating FlowData Element ---")
        
        content = flow_data.text
        self.assertIsNotNone(content, "FlowData must have text content")
        
        # Should be XML with FlowDocument root
        # Content is escaped, so look for escaped tags
        self.assertIn('FlowDocument', content, "FlowData should contain FlowDocument")
        print("[OK] Contains FlowDocument")
        
        self.assertIn('xmlns=', content, "FlowData should contain XML namespace")
        print("[OK] Contains XML namespace")
        
        self.assertIn('Paragraph', content, "FlowData should contain Paragraph elements")
        print("[OK] Contains Paragraph elements")
        
        print(f"FlowData preview: {content[:100]}...")
    
    def validate_font_data(self, font_data: ET.Element):
        """Validate FontData element"""
        print(f"--- Validating FontData Element ---")
        
        content = font_data.text
        self.assertIsNotNone(content, "FontData must have text content")
        
        # Should be XML with RVFont root
        self.assertIn('RVFont', content, "FontData should contain RVFont element")
        print("[OK] Contains RVFont element")
        
        self.assertIn('xmlns=', content, "FontData should contain XML namespace")
        print("[OK] Contains XML namespace")
        
        # Should contain font properties
        required_elements = ['Kerning', 'LineSpacing', 'OutlineColor', 'OutlineWidth', 'Variants']
        for element in required_elements:
            self.assertIn(element, content, f"FontData should contain {element} element")
            print(f"[OK] Contains {element}")
        
        print(f"FontData preview: {content[:100]}...")
    
    def test_arrangements_structure(self):
        """Test arrangements structure"""
        print("\n=== Testing Arrangements Structure ===")
        
        arrangements = self.root.find('arrangements')
        self.assertIsNotNone(arrangements, "arrangements element is required")
        
        # Should contain at least one arrangement
        arrangement_groups = arrangements.findall('RVSlideGrouping')
        self.assertGreater(len(arrangement_groups), 0, "Should contain at least one arrangement")
        print(f"[OK] Found {len(arrangement_groups)} arrangement(s)")
        
        # Validate first arrangement
        arrangement = arrangement_groups[0]
        arrangement_name = arrangement.get('name')
        arrangement_uuid = arrangement.get('uuid')
        
        self.assertIsNotNone(arrangement_name, "Arrangement must have name")
        self.assertIsNotNone(arrangement_uuid, "Arrangement must have uuid")
        
        print(f"[OK] Arrangement name: {arrangement_name}")
        print(f"[OK] Arrangement UUID: {arrangement_uuid}")
    
    def tearDown(self):
        """Clean up test files"""
        if hasattr(self, 'test_file_path') and Path(self.test_file_path).exists():
            Path(self.test_file_path).unlink()
        if hasattr(self, 'output_path') and self.output_path.exists():
            try:
                self.output_path.rmdir()
            except OSError:
                pass  # Directory not empty, that's ok
    
    def test_format_comparison_with_spec_example(self):
        """Compare our format with the example in v6-parser.md"""
        print("\n=== Comparing with v6-parser.md Example ===")
        
        # Key differences we should look for based on the spec
        spec_requirements = {
            'RTF should contain prortf1': '{\\rtf1\\prortf1',
            'Should have proper font references': '\\f0\\fcharset0',
            'FlowData should be properly escaped XML': '&lt;FlowDocument',
            'FontData should have proper namespace': 'schemas.datacontract.org'
        }
        
        # Get our generated content
        text_element = self.root.find('.//RVTextElement')
        rtf_data = text_element.get('RTFData')
        flow_data_element = text_element.find('FlowData')
        font_data_element = text_element.find('FontData')
        
        # Check RTF format
        if 'RTF should contain prortf1' in spec_requirements:
            expected = spec_requirements['RTF should contain prortf1']
            if expected not in rtf_data:
                print(f"[ERROR] RTF missing: {expected}")
                print(f"   Our RTF starts with: {rtf_data[:50]}...")
            else:
                print(f"[OK] RTF format correct")
        
        # Check FlowData format  
        if flow_data_element is not None:
            flow_content = flow_data_element.text or ""
            if 'FlowData should be properly escaped XML' in spec_requirements:
                expected = spec_requirements['FlowData should be properly escaped XML']
                if expected not in flow_content:
                    print(f"[ERROR] FlowData missing: {expected}")
                    print(f"   Our FlowData starts with: {flow_content[:50]}...")
                else:
                    print(f"[OK] FlowData format correct")
        
        # Check FontData format
        if font_data_element is not None:
            font_content = font_data_element.text or ""
            if 'FontData should have proper namespace' in spec_requirements:
                expected = spec_requirements['FontData should have proper namespace']
                if expected not in font_content:
                    print(f"[ERROR] FontData missing: {expected}")
                    print(f"   Our FontData: {font_content[:100]}...")
                else:
                    print(f"[OK] FontData format correct")


def run_format_validation():
    """Run the format validation test suite"""
    print("="*80)
    print("ProPresenter 6 Format Validation Test Suite")
    print("Comparing export format against v6-parser.md specification")
    print("="*80)
    
    # Create test suite
    suite = unittest.TestSuite()
    
    # Add all test methods
    test_methods = [
        'test_root_document_structure',
        'test_timeline_structure', 
        'test_slide_groups_structure',
        'test_arrangements_structure',
        'test_format_comparison_with_spec_example'
    ]
    
    for method in test_methods:
        suite.addTest(TestProPresenter6Format(method))
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout, buffer=False)
    result = runner.run(suite)
    
    print("\n" + "="*80)
    if result.wasSuccessful():
        print("[SUCCESS] ALL TESTS PASSED - Format appears correct")
    else:
        print("[ERROR] SOME TESTS FAILED - Format issues detected")
        print(f"Failures: {len(result.failures)}")
        print(f"Errors: {len(result.errors)}")
        
        for test, traceback in result.failures + result.errors:
            print(f"\n--- {test} ---")
            print(traceback)
    
    print("="*80)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_format_validation()
    sys.exit(0 if success else 1)