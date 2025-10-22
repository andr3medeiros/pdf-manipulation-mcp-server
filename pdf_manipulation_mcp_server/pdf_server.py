#!/usr/bin/env python3
"""
PDF Manipulation MCP Server using FastMCP

A Model Context Protocol server that provides comprehensive PDF manipulation
capabilities using the official MCP FastMCP framework.
"""

import os
import tempfile
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any

import fitz  # PyMuPDF
from mcp.server.fastmcp import FastMCP

# Initialize the MCP server
mcp = FastMCP("pdf-manipulation")

# Utility functions
def generate_output_filename(input_path: str, suffix: str = "modified") -> str:
    """Generate a new filename with timestamp to avoid overwriting originals."""
    path = Path(input_path)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return str(path.parent / f"{path.stem}_{suffix}_{timestamp}{path.suffix}")

def validate_pdf_file(pdf_path: str) -> bool:
    """Validate that the file is a valid PDF."""
    try:
        doc = fitz.open(pdf_path)
        doc.close()
        return True
    except Exception:
        return False

def validate_page_number(doc: fitz.Document, page_num: int) -> bool:
    """Validate that the page number exists in the document."""
    return 0 <= page_num < len(doc)

# Text Operations
@mcp.tool()
async def pdf_add_text(
    pdf_path: str,
    page_number: int,
    text: str,
    x: float,
    y: float,
    font_size: int = 12,
    color: List[float] = None
) -> str:
    """Add text to a PDF at a specified position."""
    if color is None:
        color = [0, 0, 0]
    
    if not os.path.exists(pdf_path):
        return f"Error: PDF file not found: {pdf_path}"
    
    if not validate_pdf_file(pdf_path):
        return f"Error: Invalid PDF file: {pdf_path}"
    
    try:
        # Open PDF document
        doc = fitz.open(pdf_path)
        
        # Validate page number
        if not validate_page_number(doc, page_number):
            doc.close()
            return f"Error: Invalid page number {page_number}. Document has {len(doc)} pages."
        
        # Get the page
        page = doc[page_number]
        
        # Add text to the page
        page.insert_text(
            (x, y),
            text,
            fontsize=font_size,
            color=color
        )
        
        # Generate output filename
        output_path = generate_output_filename(pdf_path)
        
        # Save the modified PDF
        doc.save(output_path)
        doc.close()
        
        return f"Successfully added text to PDF. Output saved to: {output_path}"
        
    except Exception as e:
        return f"Error adding text to PDF: {str(e)}"

@mcp.tool()
async def pdf_replace_text(
    pdf_path: str,
    old_text: str,
    new_text: str,
    page_number: Optional[int] = None
) -> str:
    """Replace text in a PDF document."""
    if not os.path.exists(pdf_path):
        return f"Error: PDF file not found: {pdf_path}"
    
    if not validate_pdf_file(pdf_path):
        return f"Error: Invalid PDF file: {pdf_path}"
    
    try:
        # Open PDF document
        doc = fitz.open(pdf_path)
        
        # Determine pages to search
        pages_to_search = [page_number] if page_number is not None else range(len(doc))
        
        # Validate page number if specified
        if page_number is not None and not validate_page_number(doc, page_number):
            doc.close()
            return f"Error: Invalid page number {page_number}. Document has {len(doc)} pages."
        
        replacements_made = 0
        
        # Search and replace text
        for page_num in pages_to_search:
            page = doc[page_num]
            
            # Search for the text
            text_instances = page.search_for(old_text)
            
            if text_instances:
                # Use redaction to replace text
                for rect in text_instances:
                    # Add redaction annotation
                    redact = page.add_redact_annot(rect, fill=(1, 1, 1))  # White fill
                    page.apply_redactions()
                    
                    # Insert new text at the same position
                    page.insert_text(
                        (rect.x0, rect.y1),  # Position at bottom-left of original text
                        new_text,
                        fontsize=12
                    )
                    replacements_made += 1
        
        if replacements_made == 0:
            doc.close()
            return f"No instances of '{old_text}' found in the PDF."
        
        # Generate output filename
        output_path = generate_output_filename(pdf_path)
        
        # Save the modified PDF
        doc.save(output_path)
        doc.close()
        
        return f"Successfully replaced {replacements_made} instances of text. Output saved to: {output_path}"
        
    except Exception as e:
        return f"Error replacing text in PDF: {str(e)}"

# Image Operations
@mcp.tool()
async def pdf_add_image(
    pdf_path: str,
    page_number: int,
    image_path: str,
    x: float,
    y: float,
    width: float,
    height: float
) -> str:
    """Add an image to a PDF."""
    if not os.path.exists(pdf_path):
        return f"Error: PDF file not found: {pdf_path}"
    
    if not validate_pdf_file(pdf_path):
        return f"Error: Invalid PDF file: {pdf_path}"
    
    if not os.path.exists(image_path):
        return f"Error: Image file not found: {image_path}"
    
    try:
        # Open PDF document
        doc = fitz.open(pdf_path)
        
        # Validate page number
        if not validate_page_number(doc, page_number):
            doc.close()
            return f"Error: Invalid page number {page_number}. Document has {len(doc)} pages."
        
        # Get the page
        page = doc[page_number]
        
        # Create rectangle for image placement
        rect = fitz.Rect(x, y, x + width, y + height)
        
        # Add image to the page
        page.insert_image(rect, filename=image_path)
        
        # Generate output filename
        output_path = generate_output_filename(pdf_path)
        
        # Save the modified PDF
        doc.save(output_path)
        doc.close()
        
        return f"Successfully added image to PDF. Output saved to: {output_path}"
        
    except Exception as e:
        return f"Error adding image to PDF: {str(e)}"

@mcp.tool()
async def pdf_extract_images(
    pdf_path: str,
    output_dir: Optional[str] = None
) -> str:
    """Extract all images from a PDF."""
    if not os.path.exists(pdf_path):
        return f"Error: PDF file not found: {pdf_path}"
    
    if not validate_pdf_file(pdf_path):
        return f"Error: Invalid PDF file: {pdf_path}"
    
    try:
        # Open PDF document
        doc = fitz.open(pdf_path)
        
        # Determine output directory
        if not output_dir:
            pdf_file = Path(pdf_path)
            output_dir = str(pdf_file.parent / f"{pdf_file.stem}_images")
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        extracted_images = []
        
        # Extract images from each page
        for page_num in range(len(doc)):
            page = doc[page_num]
            image_list = page.get_images()
            
            for img_index, img in enumerate(image_list):
                # Get image data
                xref = img[0]
                pix = fitz.Pixmap(doc, xref)
                
                # Skip if image is too small or invalid
                if pix.n - pix.alpha < 4:  # GRAY or RGB
                    img_name = f"page_{page_num + 1}_img_{img_index + 1}.png"
                    img_path = os.path.join(output_dir, img_name)
                    pix.save(img_path)
                    extracted_images.append(img_path)
                
                pix = None  # Free memory
        
        doc.close()
        
        if not extracted_images:
            return "No images found in the PDF."
        
        return f"Successfully extracted {len(extracted_images)} images to: {output_dir}\nImages: {', '.join(extracted_images)}"
        
    except Exception as e:
        return f"Error extracting images from PDF: {str(e)}"

# Annotations
@mcp.tool()
async def pdf_add_annotation(
    pdf_path: str,
    page_number: int,
    annotation_type: str,
    x: float,
    y: float,
    width: float,
    height: float,
    content: str
) -> str:
    """Add an annotation to a PDF."""
    if not os.path.exists(pdf_path):
        return f"Error: PDF file not found: {pdf_path}"
    
    if not validate_pdf_file(pdf_path):
        return f"Error: Invalid PDF file: {pdf_path}"
    
    try:
        # Open PDF document
        doc = fitz.open(pdf_path)
        
        # Validate page number
        if not validate_page_number(doc, page_number):
            doc.close()
            return f"Error: Invalid page number {page_number}. Document has {len(doc)} pages."
        
        # Get the page
        page = doc[page_number]
        
        # Create rectangle for annotation
        rect = fitz.Rect(x, y, x + width, y + height)
        
        # Add annotation based on type
        if annotation_type == "text":
            annot = page.add_text_annot(rect, content)
        elif annotation_type == "highlight":
            annot = page.add_highlight_annot(rect)
            annot.set_info(content=content)
        elif annotation_type == "underline":
            annot = page.add_underline_annot(rect)
            annot.set_info(content=content)
        elif annotation_type == "strikeout":
            annot = page.add_strikeout_annot(rect)
            annot.set_info(content=content)
        else:
            doc.close()
            return f"Error: Invalid annotation type: {annotation_type}"
        
        # Update annotation appearance
        annot.update()
        
        # Generate output filename
        output_path = generate_output_filename(pdf_path)
        
        # Save the modified PDF
        doc.save(output_path)
        doc.close()
        
        return f"Successfully added {annotation_type} annotation to PDF. Output saved to: {output_path}"
        
    except Exception as e:
        return f"Error adding annotation to PDF: {str(e)}"

# Form Fields
@mcp.tool()
async def pdf_add_form_field(
    pdf_path: str,
    page_number: int,
    field_type: str,
    field_name: str,
    x: float,
    y: float,
    width: float,
    height: float,
    options: List[str] = None
) -> str:
    """Add a form field to a PDF."""
    if options is None:
        options = []
    
    if not os.path.exists(pdf_path):
        return f"Error: PDF file not found: {pdf_path}"
    
    if not validate_pdf_file(pdf_path):
        return f"Error: Invalid PDF file: {pdf_path}"
    
    try:
        # Open PDF document
        doc = fitz.open(pdf_path)
        
        # Validate page number
        if not validate_page_number(doc, page_number):
            doc.close()
            return f"Error: Invalid page number {page_number}. Document has {len(doc)} pages."
        
        # Get the page
        page = doc[page_number]
        
        # Create rectangle for form field
        rect = fitz.Rect(x, y, x + width, y + height)
        
        # Add form field based on type
        if field_type == "text":
            widget = page.add_textfield(rect, field_name)
        elif field_type == "checkbox":
            widget = page.add_checkbox(rect, field_name)
        elif field_type == "radio":
            widget = page.add_radio_button(rect, field_name)
        elif field_type == "combobox":
            widget = page.add_combobox(rect, field_name, options)
        else:
            doc.close()
            return f"Error: Invalid field type: {field_type}"
        
        # Update widget appearance
        widget.update()
        
        # Generate output filename
        output_path = generate_output_filename(pdf_path)
        
        # Save the modified PDF
        doc.save(output_path)
        doc.close()
        
        return f"Successfully added {field_type} form field '{field_name}' to PDF. Output saved to: {output_path}"
        
    except Exception as e:
        return f"Error adding form field to PDF: {str(e)}"

@mcp.tool()
async def pdf_fill_form(
    pdf_path: str,
    field_values: Dict[str, Any]
) -> str:
    """Fill form fields in a PDF with values."""
    if not os.path.exists(pdf_path):
        return f"Error: PDF file not found: {pdf_path}"
    
    if not validate_pdf_file(pdf_path):
        return f"Error: Invalid PDF file: {pdf_path}"
    
    try:
        # Open PDF document
        doc = fitz.open(pdf_path)
        
        filled_fields = 0
        
        # Fill form fields
        for page_num in range(len(doc)):
            page = doc[page_num]
            widgets = page.widgets()
            
            for widget in widgets:
                field_name = widget.field_name
                if field_name in field_values:
                    value = field_values[field_name]
                    
                    # Set field value based on widget type
                    if widget.field_type == fitz.PDF_WIDGET_TYPE_TEXT:
                        widget.field_value = str(value)
                    elif widget.field_type == fitz.PDF_WIDGET_TYPE_CHECKBOX:
                        widget.field_value = bool(value)
                    elif widget.field_type == fitz.PDF_WIDGET_TYPE_RADIOBUTTON:
                        widget.field_value = str(value)
                    elif widget.field_type == fitz.PDF_WIDGET_TYPE_COMBOBOX:
                        widget.field_value = str(value)
                    
                    widget.update()
                    filled_fields += 1
        
        if filled_fields == 0:
            doc.close()
            return "No matching form fields found to fill."
        
        # Generate output filename
        output_path = generate_output_filename(pdf_path)
        
        # Save the modified PDF
        doc.save(output_path)
        doc.close()
        
        return f"Successfully filled {filled_fields} form fields. Output saved to: {output_path}"
        
    except Exception as e:
        return f"Error filling form fields: {str(e)}"

# Page Manipulation
@mcp.tool()
async def pdf_merge_files(
    pdf_paths: List[str],
    output_path: Optional[str] = None
) -> str:
    """Merge multiple PDF files into one combined PDF."""
    # Validate all PDF files
    for pdf_path in pdf_paths:
        if not os.path.exists(pdf_path):
            return f"Error: PDF file not found: {pdf_path}"
        if not validate_pdf_file(pdf_path):
            return f"Error: Invalid PDF file: {pdf_path}"
    
    try:
        # Create new document for merging
        merged_doc = fitz.open()
        
        # Merge all PDFs
        for pdf_path in pdf_paths:
            doc = fitz.open(pdf_path)
            merged_doc.insert_pdf(doc)
            doc.close()
        
        # Determine output path
        if not output_path:
            output_path = generate_output_filename(pdf_paths[0], "merged")
        
        # Save merged PDF
        merged_doc.save(output_path)
        merged_doc.close()
        
        return f"Successfully merged {len(pdf_paths)} PDFs. Output saved to: {output_path}"
        
    except Exception as e:
        return f"Error merging PDFs: {str(e)}"

@mcp.tool()
async def pdf_combine_pages_to_single(
    pdf_path: str,
    page_numbers: Optional[List[int]] = None,
    layout: str = "vertical",
    output_path: Optional[str] = None
) -> str:
    """Combine multiple pages from a PDF into a single page with specified layout."""
    if not os.path.exists(pdf_path):
        return f"Error: PDF file not found: {pdf_path}"
    
    if not validate_pdf_file(pdf_path):
        return f"Error: Invalid PDF file: {pdf_path}"
    
    if layout not in ["vertical", "horizontal", "grid"]:
        return f"Error: Invalid layout. Must be 'vertical', 'horizontal', or 'grid'."
    
    try:
        # Open PDF document
        doc = fitz.open(pdf_path)
        
        # Determine pages to combine
        if page_numbers is None:
            pages_to_combine = list(range(len(doc)))
        else:
            # Validate page numbers
            for page_num in page_numbers:
                if not validate_page_number(doc, page_num):
                    doc.close()
                    return f"Error: Invalid page number {page_num}. Document has {len(doc)} pages."
            pages_to_combine = page_numbers
        
        if len(pages_to_combine) < 2:
            doc.close()
            return "Error: Need at least 2 pages to combine."
        
        # Get dimensions of all pages
        page_rects = [doc[page_num].rect for page_num in pages_to_combine]
        page_widths = [rect.width for rect in page_rects]
        page_heights = [rect.height for rect in page_rects]
        
        # Calculate new page dimensions based on layout
        if layout == "vertical":
            new_width = max(page_widths)
            new_height = sum(page_heights)
        elif layout == "horizontal":
            new_width = sum(page_widths)
            new_height = max(page_heights)
        else:  # grid layout
            import math
            num_pages = len(pages_to_combine)
            cols = math.ceil(math.sqrt(num_pages))
            rows = math.ceil(num_pages / cols)
            new_width = max(page_widths) * cols
            new_height = max(page_heights) * rows
        
        # Create new document with single page
        new_doc = fitz.open()
        new_page = new_doc.new_page(width=new_width, height=new_height)
        
        # Place pages according to layout
        if layout == "vertical":
            y_offset = 0
            for page_num in pages_to_combine:
                page_rect = fitz.Rect(0, y_offset, page_rects[pages_to_combine.index(page_num)].width, 
                                    y_offset + page_rects[pages_to_combine.index(page_num)].height)
                new_page.show_pdf_page(page_rect, doc, page_num)
                y_offset += page_rects[pages_to_combine.index(page_num)].height
                
        elif layout == "horizontal":
            x_offset = 0
            for page_num in pages_to_combine:
                page_rect = fitz.Rect(x_offset, 0, x_offset + page_rects[pages_to_combine.index(page_num)].width,
                                    page_rects[pages_to_combine.index(page_num)].height)
                new_page.show_pdf_page(page_rect, doc, page_num)
                x_offset += page_rects[pages_to_combine.index(page_num)].width
                
        else:  # grid layout
            for i, page_num in enumerate(pages_to_combine):
                row = i // cols
                col = i % cols
                x = col * max(page_widths)
                y = row * max(page_heights)
                page_rect = fitz.Rect(x, y, x + page_rects[i].width, y + page_rects[i].height)
                new_page.show_pdf_page(page_rect, doc, page_num)
        
        # Generate output filename
        if not output_path:
            output_path = generate_output_filename(pdf_path, "combined")
        
        # Save the combined PDF
        new_doc.save(output_path)
        new_doc.close()
        doc.close()
        
        return f"Successfully combined {len(pages_to_combine)} pages using {layout} layout. Output saved to: {output_path}"
        
    except Exception as e:
        return f"Error combining pages: {str(e)}"

@mcp.tool()
async def pdf_split(
    pdf_path: str,
    output_dir: Optional[str] = None,
    page_ranges: Optional[List[Dict[str, int]]] = None
) -> str:
    """Split a PDF into individual pages or page ranges."""
    if not os.path.exists(pdf_path):
        return f"Error: PDF file not found: {pdf_path}"
    
    if not validate_pdf_file(pdf_path):
        return f"Error: Invalid PDF file: {pdf_path}"
    
    try:
        # Open PDF document
        doc = fitz.open(pdf_path)
        
        # Determine output directory
        if not output_dir:
            pdf_file = Path(pdf_path)
            output_dir = str(pdf_file.parent / f"{pdf_file.stem}_split")
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        split_files = []
        
        if page_ranges:
            # Split by page ranges
            for i, page_range in enumerate(page_ranges):
                start_page = page_range["start"]
                end_page = page_range["end"]
                
                # Validate page range
                if start_page < 0 or end_page >= len(doc) or start_page > end_page:
                    doc.close()
                    return f"Error: Invalid page range {start_page}-{end_page}"
                
                # Create new document for this range
                new_doc = fitz.open()
                new_doc.insert_pdf(doc, from_page=start_page, to_page=end_page)
                
                # Save split PDF
                output_file = os.path.join(output_dir, f"pages_{start_page + 1}_to_{end_page + 1}.pdf")
                new_doc.save(output_file)
                new_doc.close()
                split_files.append(output_file)
        else:
            # Split into individual pages
            for page_num in range(len(doc)):
                new_doc = fitz.open()
                new_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)
                
                output_file = os.path.join(output_dir, f"page_{page_num + 1}.pdf")
                new_doc.save(output_file)
                new_doc.close()
                split_files.append(output_file)
        
        doc.close()
        
        return f"Successfully split PDF into {len(split_files)} files. Output directory: {output_dir}"
        
    except Exception as e:
        return f"Error splitting PDF: {str(e)}"

@mcp.tool()
async def pdf_rotate_page(
    pdf_path: str,
    page_number: int,
    rotation: int
) -> str:
    """Rotate a page in a PDF."""
    if not os.path.exists(pdf_path):
        return f"Error: PDF file not found: {pdf_path}"
    
    if not validate_pdf_file(pdf_path):
        return f"Error: Invalid PDF file: {pdf_path}"
    
    if rotation not in [90, 180, 270]:
        return f"Error: Invalid rotation angle. Must be 90, 180, or 270 degrees."
    
    try:
        # Open PDF document
        doc = fitz.open(pdf_path)
        
        # Validate page number
        if not validate_page_number(doc, page_number):
            doc.close()
            return f"Error: Invalid page number {page_number}. Document has {len(doc)} pages."
        
        # Get the page and rotate it
        page = doc[page_number]
        page.set_rotation(rotation)
        
        # Generate output filename
        output_path = generate_output_filename(pdf_path)
        
        # Save the modified PDF
        doc.save(output_path)
        doc.close()
        
        return f"Successfully rotated page {page_number + 1} by {rotation} degrees. Output saved to: {output_path}"
        
    except Exception as e:
        return f"Error rotating page: {str(e)}"

@mcp.tool()
async def pdf_delete_page(
    pdf_path: str,
    page_number: int
) -> str:
    """Delete a page from a PDF."""
    if not os.path.exists(pdf_path):
        return f"Error: PDF file not found: {pdf_path}"
    
    if not validate_pdf_file(pdf_path):
        return f"Error: Invalid PDF file: {pdf_path}"
    
    try:
        # Open PDF document
        doc = fitz.open(pdf_path)
        
        # Validate page number
        if not validate_page_number(doc, page_number):
            doc.close()
            return f"Error: Invalid page number {page_number}. Document has {len(doc)} pages."
        
        # Delete the page
        doc.delete_page(page_number)
        
        # Generate output filename
        output_path = generate_output_filename(pdf_path)
        
        # Save the modified PDF
        doc.save(output_path)
        doc.close()
        
        return f"Successfully deleted page {page_number + 1}. Output saved to: {output_path}"
        
    except Exception as e:
        return f"Error deleting page: {str(e)}"

@mcp.tool()
async def pdf_crop_page(
    pdf_path: str,
    page_number: int,
    x0: float,
    y0: float,
    x1: float,
    y1: float,
    coordinate_mode: str = "bbox"
) -> str:
    """Crop a page in a PDF."""
    if not os.path.exists(pdf_path):
        return f"Error: PDF file not found: {pdf_path}"
    
    if not validate_pdf_file(pdf_path):
        return f"Error: Invalid PDF file: {pdf_path}"
    
    if coordinate_mode not in ["bbox", "rect"]:
        return f"Error: Invalid coordinate_mode. Must be 'bbox' or 'rect'."
    
    try:
        # Open PDF document
        doc = fitz.open(pdf_path)
        
        # Validate page number
        if not validate_page_number(doc, page_number):
            doc.close()
            return f"Error: Invalid page number {page_number}. Document has {len(doc)} pages."
        
        # Get the page
        page = doc[page_number]
        
        # Convert coordinates based on mode
        if coordinate_mode == "rect":
            # Convert from x, y, width, height to x0, y0, x1, y1
            # Note: PDF coordinates have origin at bottom-left, so we need to adjust
            page_rect = page.rect
            actual_x0 = x0
            actual_y0 = page_rect.height - (y0 + y1)  # Convert from top-left to bottom-left origin
            actual_x1 = x0 + x1
            actual_y1 = page_rect.height - y0
        else:  # bbox mode
            actual_x0, actual_y0, actual_x1, actual_y1 = x0, y0, x1, y1
        
        # Validate crop coordinates
        page_rect = page.rect
        if (actual_x0 < 0 or actual_y0 < 0 or 
            actual_x1 > page_rect.width or actual_y1 > page_rect.height or
            actual_x0 >= actual_x1 or actual_y0 >= actual_y1):
            doc.close()
            return f"Error: Invalid crop coordinates. Page dimensions: {page_rect.width:.1f} x {page_rect.height:.1f}"
        
        # Set the crop box
        crop_rect = fitz.Rect(actual_x0, actual_y0, actual_x1, actual_y1)
        page.set_cropbox(crop_rect)
        
        # Generate output filename
        output_path = generate_output_filename(pdf_path)
        
        # Save the modified PDF
        doc.save(output_path)
        doc.close()
        
        return f"Successfully cropped page {page_number + 1}. Output saved to: {output_path}"
        
    except Exception as e:
        return f"Error cropping page: {str(e)}"

@mcp.tool()
async def pdf_auto_crop_page(
    pdf_path: str,
    page_number: Optional[int] = None,
    padding: float = 10.0
) -> str:
    """Automatically crop a PDF page to remove blank margins by detecting content boundaries."""
    if not os.path.exists(pdf_path):
        return f"Error: PDF file not found: {pdf_path}"
    
    if not validate_pdf_file(pdf_path):
        return f"Error: Invalid PDF file: {pdf_path}"
    
    try:
        # Open PDF document
        doc = fitz.open(pdf_path)
        
        # Determine pages to process
        if page_number is not None:
            if not validate_page_number(doc, page_number):
                doc.close()
                return f"Error: Invalid page number {page_number}. Document has {len(doc)} pages."
            pages_to_process = [page_number]
        else:
            pages_to_process = list(range(len(doc)))
        
        cropped_pages = 0
        
        for page_num in pages_to_process:
            page = doc[page_num]
            
            # Get text at word level for tighter bounds
            words = page.get_text("words")
            text_rects = [word[:4] for word in words if len(word) >= 4]
            
            # Get image rectangles  
            images = page.get_images()
            image_rects = [img[:4] for img in images if len(img) >= 4]
            
            # Get drawing objects (lines, shapes, paths) - NO external dependencies
            drawing_rects = []
            try:
                drawings = page.get_drawings()
                for drawing in drawings:
                    if 'rect' in drawing:
                        drawing_rects.append(drawing['rect'])
            except Exception:
                pass
            
            # Combine all rectangles
            all_rects = text_rects + image_rects + drawing_rects
            
            # Filter out invalid rectangles (outside page bounds or with invalid coordinates)
            page_rect = page.rect
            valid_rects = []
            for rect in all_rects:
                if len(rect) >= 4:
                    try:
                        r = fitz.Rect(rect[:4])
                        # Check if rectangle is valid and within reasonable bounds
                        if (r.is_valid and 
                            r.x0 >= 0 and r.y0 >= 0 and 
                            r.x1 <= page_rect.width and r.y1 <= page_rect.height and
                            r.width > 0 and r.height > 0):
                            valid_rects.append(rect[:4])
                    except Exception:
                        continue
            
            all_rects = valid_rects
            
            
            if all_rects:
                # Calculate union of all content rectangles
                content_rect = fitz.Rect(all_rects[0])
                for rect in all_rects[1:]:
                    content_rect |= fitz.Rect(rect)
                
                # More conservative padding strategy to preserve section flow
                # Use asymmetric padding: less aggressive on sides, more generous on top/bottom
                page_rect = page.rect
                
                # Calculate how much we can crop while preserving document flow
                # Only crop if there's significant margin (at least 2 points on each side)
                margin_threshold = 2.0
                
                # Check if margins are significant enough to warrant cropping
                left_margin = content_rect.x0
                right_margin = page_rect.width - content_rect.x1
                top_margin = content_rect.y0
                bottom_margin = page_rect.height - content_rect.y1
                
                # Only crop if margins are substantial
                if (left_margin > margin_threshold or right_margin > margin_threshold or 
                    top_margin > margin_threshold or bottom_margin > margin_threshold):
                    
                    # Conservative padding: preserve more space for better flow
                    conservative_padding = max(padding, 20.0)  # At least 20 points padding
                    
                    # Asymmetric padding: less on sides, more on top/bottom for better section flow
                    content_rect = content_rect + [
                        -min(conservative_padding * 0.5, left_margin * 0.8),   # left: 50% of padding or 80% of margin
                        -min(conservative_padding, bottom_margin * 0.8),       # bottom: full padding or 80% of margin
                        min(conservative_padding * 0.5, right_margin * 0.8),   # right: 50% of padding or 80% of margin
                        min(conservative_padding, top_margin * 0.8)            # top: full padding or 80% of margin
                    ]
                    
                    # Ensure the crop box is within page bounds
                    content_rect.intersect(page_rect)
                    
                    # Apply crop if there's any reduction in size
                    if (content_rect.width < page_rect.width or 
                        content_rect.height < page_rect.height):
                        page.set_cropbox(content_rect)
                        cropped_pages += 1
            else:
                # No content found, skip this page
                continue
        
        if cropped_pages == 0:
            doc.close()
            return "No content found to crop on any pages."
        
        # Generate output filename
        output_path = generate_output_filename(pdf_path, "auto_cropped")
        
        # Save the modified PDF
        doc.save(output_path)
        doc.close()
        
        page_info = f"page {page_number + 1}" if page_number is not None else f"{cropped_pages} pages"
        return f"Successfully auto-cropped {page_info}. Output saved to: {output_path}"
        
    except Exception as e:
        return f"Error auto-cropping PDF: {str(e)}"

# Metadata
@mcp.tool()
async def pdf_get_info(pdf_path: str) -> str:
    """Get metadata and information about a PDF."""
    if not os.path.exists(pdf_path):
        return f"Error: PDF file not found: {pdf_path}"
    
    if not validate_pdf_file(pdf_path):
        return f"Error: Invalid PDF file: {pdf_path}"
    
    try:
        # Open PDF document
        doc = fitz.open(pdf_path)
        
        # Get basic information
        page_count = len(doc)
        file_size = os.path.getsize(pdf_path)
        
        # Get metadata
        metadata = doc.metadata
        
        # Get page dimensions (first page)
        first_page = doc[0]
        page_rect = first_page.rect
        page_width = page_rect.width
        page_height = page_rect.height
        
        # Close document
        doc.close()
        
        # Format information
        info_text = f"""PDF Information for: {pdf_path}

Basic Information:
- Page count: {page_count}
- File size: {file_size:,} bytes
- Page dimensions: {page_width:.1f} x {page_height:.1f} points

Metadata:
- Title: {metadata.get('title', 'N/A')}
- Author: {metadata.get('author', 'N/A')}
- Subject: {metadata.get('subject', 'N/A')}
- Creator: {metadata.get('creator', 'N/A')}
- Producer: {metadata.get('producer', 'N/A')}
- Creation date: {metadata.get('creationDate', 'N/A')}
- Modification date: {metadata.get('modDate', 'N/A')}
- Keywords: {metadata.get('keywords', 'N/A')}
- Format: {metadata.get('format', 'N/A')}
- Encryption: {metadata.get('encryption', 'N/A')}"""
        
        return info_text
        
    except Exception as e:
        return f"Error getting PDF info: {str(e)}"

@mcp.tool()
async def pdf_set_metadata(
    pdf_path: str,
    metadata: Dict[str, str]
) -> str:
    """Set metadata for a PDF."""
    if not os.path.exists(pdf_path):
        return f"Error: PDF file not found: {pdf_path}"
    
    if not validate_pdf_file(pdf_path):
        return f"Error: Invalid PDF file: {pdf_path}"
    
    try:
        # Open PDF document
        doc = fitz.open(pdf_path)
        
        # Set metadata fields
        updated_fields = []
        for field, value in metadata.items():
            if value:  # Only set non-empty values
                doc.set_metadata({field: str(value)})
                updated_fields.append(f"{field}: {value}")
        
        # Generate output filename
        output_path = generate_output_filename(pdf_path)
        
        # Save the modified PDF
        doc.save(output_path)
        doc.close()
        
        if updated_fields:
            return f"Successfully updated metadata. Output saved to: {output_path}\nUpdated fields:\n" + "\n".join(updated_fields)
        else:
            return "No metadata fields to update."
        
    except Exception as e:
        return f"Error setting PDF metadata: {str(e)}"