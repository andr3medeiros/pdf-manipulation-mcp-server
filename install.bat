@echo off
REM PDF Manipulation MCP Server Installation Script with UV (Windows)

echo 🚀 Installing PDF Manipulation MCP Server with UV
echo ==================================================

REM Get the current directory
set SCRIPT_DIR=%~dp0
echo 📁 Project directory: %SCRIPT_DIR%

REM Check if UV is available
uv --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Error: UV not found. Please install UV first:
    echo    https://docs.astral.sh/uv/getting-started/installation/
    pause
    exit /b 1
)

echo ✅ Found UV: 
uv --version

REM Check Python version
echo 🐍 Checking Python version...
uv python list | findstr "3.10 3.11 3.12" >nul
if %errorlevel% neq 0 (
    echo 📦 Installing Python 3.11 with UV...
    uv python install 3.11
)

REM Install dependencies with UV
echo 📦 Installing dependencies with UV...
uv pip install mcp pymupdf pymupdf4llm markdown-pdf

if %errorlevel% equ 0 (
    echo ✅ Dependencies installed successfully
) else (
    echo ❌ Error installing dependencies
    pause
    exit /b 1
)

REM Test the server
echo 🧪 Testing the MCP server...
uv run python test_mcp_server.py

if %errorlevel% equ 0 (
    echo ✅ Server test passed
) else (
    echo ❌ Server test failed
    pause
    exit /b 1
)

echo.
echo 🎉 Installation completed successfully!
echo.
echo 📋 Available tools:
echo   - pdf_to_markdown: Convert PDF to Markdown
echo   - markdown_to_pdf: Convert Markdown to PDF
echo   - pdf_add_text: Add text to PDF
echo   - pdf_replace_text: Replace text in PDF
echo   - pdf_add_image: Add images to PDF
echo   - pdf_extract_images: Extract images from PDF
echo   - pdf_add_annotation: Add annotations to PDF
echo   - pdf_add_form_field: Add form fields to PDF
echo   - pdf_fill_form: Fill form fields
echo   - pdf_merge_pages: Merge multiple PDFs
echo   - pdf_split: Split PDF into pages
echo   - pdf_rotate_page: Rotate pages
echo   - pdf_delete_page: Delete pages
echo   - pdf_get_info: Get PDF information
echo   - pdf_set_metadata: Set PDF metadata
echo.
echo 🔧 To run the server:
echo    uv run python server.py
echo.
echo 📚 Cursor IDE Setup:
echo    1. Open Cursor IDE
echo    2. Go to Settings (Ctrl + ,)
echo    3. Search for 'MCP' or go to Extensions ^> MCP
echo    4. Add this server configuration:
echo.
echo    {
echo      "mcpServers": {
echo        "pdf-manipulation": {
echo          "command": "uv",
echo          "args": ["run", "python", "server.py"],
echo          "cwd": "%SCRIPT_DIR%"
echo        }
echo      }
echo    }
echo.
echo    5. Save the configuration and restart Cursor
echo    6. The PDF manipulation tools will appear in the MCP tools panel
echo.
echo 📖 For detailed setup instructions, see README.md

pause
