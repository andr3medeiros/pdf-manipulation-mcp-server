# PDF Manipulation MCP Server

A study project implementing a Model Context Protocol (MCP) server that provides comprehensive PDF manipulation capabilities using the official MCP FastMCP framework. This project focuses on direct PDF editing and manipulation features for learning and experimentation purposes.

**Quick Start:** Run directly with `uv run pdf-manipulation-mcp-server` (like npx for Node.js packages)

## Features

- **Text Operations**: Add, replace, and manipulate text in PDFs
- **Image Operations**: Add images and extract images from PDFs
- **Annotations**: Add various types of annotations (text, highlight, underline, etc.)
- **Form Fields**: Add and fill form fields
- **Page Manipulation**: Merge, split, rotate, delete, and crop pages
- **Auto-Crop**: Automatically detect and crop content boundaries
- **Page Combination**: Combine multiple pages into single pages with various layouts
- **Metadata**: Get and set PDF metadata

## Quick Start

### Prerequisites

- Python 3.10+ 
- pip (comes with Python)

> **📖 For detailed installation instructions, see [INSTALL.md](INSTALL.md)**

### Installation

**Option 1: Run Directly with UV (Like npx)**

```bash
# Run without installation (fastest)
uv run pdf-manipulation-mcp-server
```

**Option 2: Install from PyPI**

```bash
# Install the package
pip install pdf-manipulation-mcp-server

# Run the server
pdf-mcp-server
```

**Option 3: Install from GitHub**

```bash
# Install directly from GitHub
pip install git+https://github.com/yourusername/pdf-manipulation-mcp-server.git

# Run the server
pdf-mcp-server
```

**Option 4: Clone and Install Locally**

```bash
# Clone the repository
git clone https://github.com/yourusername/pdf-manipulation-mcp-server.git
cd pdf-manipulation-mcp-server

# Install in development mode
pip install -e .

# Run the server
pdf-mcp-server
```

**Option 5: Using UV (Development)**

```bash
# Clone the repository
git clone https://github.com/yourusername/pdf-manipulation-mcp-server.git
cd pdf-manipulation-mcp-server

# Install dependencies with UV
uv pip install mcp pymupdf

# Test the server
uv run pytest tests/ -v

# Run the server
uv run python server.py
```

## Available Tools (15 Total)

### Text Operations
- **`pdf_add_text`** - Add text to a PDF at specified position
- **`pdf_replace_text`** - Replace text in a PDF document

### Image Operations
- **`pdf_add_image`** - Add an image to a PDF
- **`pdf_extract_images`** - Extract all images from a PDF

### Annotations
- **`pdf_add_annotation`** - Add annotations to a PDF (text, highlight, underline, strikeout)

### Form Fields
- **`pdf_add_form_field`** - Add form fields to a PDF (text, checkbox, radio, combobox)
- **`pdf_fill_form`** - Fill form fields in a PDF with values

### Page Manipulation
- **`pdf_merge_files`** - Merge multiple PDF files into one
- **`pdf_combine_pages_to_single`** - Combine multiple pages from a PDF into a single page
- **`pdf_split`** - Split a PDF into individual pages or page ranges
- **`pdf_rotate_page`** - Rotate a page in a PDF (90, 180, 270 degrees)
- **`pdf_delete_page`** - Delete a page from a PDF
- **`pdf_crop_page`** - Crop a page in a PDF with coordinate support
- **`pdf_auto_crop_page`** - Automatically crop pages by detecting content boundaries

### Metadata
- **`pdf_get_info`** - Get metadata and information about a PDF
- **`pdf_set_metadata`** - Set metadata for a PDF

## How to Configure with Cursor IDE

### Step 1: Install the Server

Follow the installation steps above to set up the MCP server.

### Step 2: Configure Cursor IDE

Add this configuration to your Cursor settings:

```
**Option A: Using an MCP config and uvx:**
````json
{
  "mcpServers": {
    "pdf-manipulation": {
      "command": "uvx",
      "args": ["--from", "pdf-manipulation-mcp-server", "pdf-mcp-server"]
    }
  }
}
```
**Option B: Using MCP Config File**

Create `~/.cursor/mcp_config.json`:

```json
{
  "mcpServers": {
    "pdf-manipulation": {
      "command": "uv",
      "args": ["run", "python", "server.py"],
      "cwd": "/path/to/pdf-manipulation-mcp-server"
    }
  }
}

**Option C: Using Cursor Settings UI**
1. Open Cursor Settings (`Cmd+,` on Mac, `Ctrl+,` on Windows/Linux)
2. Search for "MCP" in settings
3. Add this configuration:

```json
{
  "mcp.servers": {
    "pdf-manipulation": {
      "command": "uv",
      "args": ["run", "python", "server.py"],
      "cwd": "/path/to/pdf-manipulation-mcp-server"
    }
  }
}
```

### Step 3: Restart Cursor IDE

After adding the configuration, restart Cursor IDE to load the MCP server.

### Step 4: Test the Integration

1. Open a new chat in Cursor
2. Try these commands:
   - "Convert this PDF to Markdown"
   - "Add text to a PDF"
   - "Extract images from a PDF"
   - "Merge multiple PDFs"

## Usage Examples

### Basic PDF Auto-Crop Workflow

```python
# Automatically crop PDF pages to remove margins
result = await pdf_auto_crop_page(
    pdf_path="document.pdf",
    padding=10.0
)

# Crop specific page with coordinates
result = await pdf_crop_page(
    pdf_path="document.pdf",
    page_number=0,
    x0=50, y0=50, x1=400, y1=300,
    coordinate_mode="bbox"
)
```

### Adding Text to PDF

```python
result = await pdf_add_text(
    pdf_path="document.pdf",
    page_number=0,
    text="New text content",
    x=100,
    y=100,
    font_size=14,
    color=[1, 0, 0]  # Red color
)
```

### Working with Images

```python
# Add image to PDF
result = await pdf_add_image(
    pdf_path="document.pdf",
    page_number=0,
    image_path="image.png",
    x=100,
    y=200,
    width=200,
    height=150
)

# Extract all images from PDF
result = await pdf_extract_images(
    pdf_path="document.pdf",
    output_dir="extracted_images"
)
```

### Page Manipulation

```python
# Merge multiple PDFs
result = await pdf_merge_files(
    pdf_paths=["doc1.pdf", "doc2.pdf", "doc3.pdf"]
)

# Combine pages from a single PDF
result = await pdf_combine_pages_to_single(
    pdf_path="document.pdf",
    page_numbers=[0, 1, 2],
    layout="vertical"
)

# Split PDF into individual pages
result = await pdf_split(
    pdf_path="document.pdf",
    output_dir="split_pages"
)

# Rotate a page
result = await pdf_rotate_page(
    pdf_path="document.pdf",
    page_number=0,
    rotation=90
)
```

## Development

### Project Structure

```
pdf-manipulation-mcp-server/
├── pdf_server.py          # Main MCP server implementation
├── server.py              # Entry point for UV
├── test_mcp_server.py     # Test script
├── pyproject.toml         # Project configuration
├── install.sh             # Installation script (Mac/Linux)
├── install.bat            # Installation script (Windows)
└── README.md              # This file
```

### Running Tests

```bash
# Test the MCP server
uv run python test_mcp_server.py

# Run the server
uv run python server.py
```

### Dependencies

- **`mcp`** - Official MCP SDK for Python
- **`pymupdf`** - Core PDF manipulation library
- **`pytest`** - Testing framework (dev dependency)
- **`pytest-asyncio`** - Async testing support (dev dependency)

## File Safety

All operations create new files with timestamps to avoid overwriting originals. Output files follow the pattern: `{original_name}_{operation}_{timestamp}.pdf`

## Error Handling

The server includes comprehensive error handling:
- Validates PDF files before operations
- Checks page numbers and coordinates
- Provides clear error messages
- Handles missing files gracefully
- Catches and reports PyMuPDF exceptions

## Troubleshooting

### Common Issues

1. **"No tools" in Cursor settings**: This is normal! Tools appear in the chat interface, not in settings.

2. **UV not found**: Install UV first:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. **Python version error**: UV will automatically install Python 3.11+ if needed.

4. **Dependencies not found**: Make sure you're using UV:
   ```bash
   uv pip install mcp pymupdf
   ```

### Debug Mode

To run the server in debug mode:

```bash
uv run python server.py --debug
```

## Contributing

This is a study project, but contributions are welcome! If you'd like to contribute:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with `uv run pytest tests/ -v`
5. Submit a pull request

## Study Project Notes

This project was created as a learning exercise to explore:
- Model Context Protocol (MCP) server development
- PDF manipulation using PyMuPDF
- FastMCP framework implementation
- Automated testing with pytest
- Content detection and cropping algorithms

## License

This project is open source and available under the MIT License.

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Review the test output: `uv run python test_mcp_server.py`
3. Check Cursor logs for MCP errors
4. Open an issue on GitHub