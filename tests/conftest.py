"""
Pytest configuration and shared fixtures for PDF Manipulation MCP Server tests.
"""

import os
import tempfile
from pathlib import Path

import fitz
import pytest
import pytest_asyncio

from pdf_manipulation_mcp_server.pdf_server import mcp


@pytest.fixture
def mcp_server():
    """Provide the MCP server instance for testing."""
    return mcp


@pytest.fixture
def test_pdf_path(tmp_path):
    """Create a test PDF file and return its path."""
    # Create a test PDF with some content
    doc = fitz.open()
    page = doc.new_page()
    
    # Add some text content
    page.insert_text((100, 100), "Test PDF for MCP Server")
    page.insert_text((100, 150), "This is a test document for FastMCP")
    page.insert_text((100, 200), "Testing PDF manipulation capabilities")
    page.insert_text((100, 250), "Added by FastMCP Server")
    
    # Save to temporary file
    pdf_path = tmp_path / "test_document.pdf"
    doc.save(str(pdf_path))
    doc.close()
    
    return str(pdf_path)


@pytest.fixture
def test_pdf_with_margins(tmp_path):
    """Create a test PDF with large margins to test auto-crop functionality."""
    doc = fitz.open()
    page = doc.new_page()
    
    # Add content in a small area (simulating large margins)
    page.insert_text((200, 200), "Content in center")
    page.insert_text((200, 250), "With large margins around")
    page.insert_text((200, 300), "This should be auto-cropped")
    
    # Save to temporary file
    pdf_path = tmp_path / "test_document_with_margins.pdf"
    doc.save(str(pdf_path))
    doc.close()
    
    return str(pdf_path)


@pytest.fixture
def test_pdf_multiple_pages(tmp_path):
    """Create a test PDF with multiple pages."""
    doc = fitz.open()
    
    # Page 1
    page1 = doc.new_page()
    page1.insert_text((100, 100), "Page 1 Content")
    
    # Page 2
    page2 = doc.new_page()
    page2.insert_text((100, 100), "Page 2 Content")
    
    # Page 3
    page3 = doc.new_page()
    page3.insert_text((100, 100), "Page 3 Content")
    
    # Save to temporary file
    pdf_path = tmp_path / "test_document_multiple.pdf"
    doc.save(str(pdf_path))
    doc.close()
    
    return str(pdf_path)


@pytest.fixture
def test_pdf_with_images(tmp_path):
    """Create a test PDF with images for testing image-related functions."""
    doc = fitz.open()
    page = doc.new_page()
    
    # Add text
    page.insert_text((100, 100), "PDF with images")
    
    # Create a simple rectangle as a placeholder for an image
    rect = fitz.Rect(100, 150, 200, 200)
    page.draw_rect(rect, color=(0, 0, 1), width=2)
    page.insert_text((110, 180), "Image Placeholder")
    
    # Save to temporary file
    pdf_path = tmp_path / "test_document_with_images.pdf"
    doc.save(str(pdf_path))
    doc.close()
    
    return str(pdf_path)


@pytest.fixture
def cleanup_test_files():
    """Cleanup function for any additional test files created during tests."""
    created_files = []
    
    def _track_file(file_path):
        created_files.append(file_path)
        return file_path
    
    yield _track_file
    
    # Cleanup after test
    for file_path in created_files:
        if os.path.exists(file_path):
            os.remove(file_path)
