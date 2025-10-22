# Installation Guide

This guide shows you different ways to install the PDF Manipulation MCP Server.

## Quick Install (Recommended)

### Run Directly with UV (Like npx)

The fastest way to run the server without any installation:

```bash
uv run pdf-manipulation-mcp-server
```

This downloads and runs the package directly, just like `npx` for Node.js packages.

### Install with pip

The traditional way to install the server:

```bash
pip install pdf-manipulation-mcp-server
```

After installation, you can run the server with:

```bash
pdf-mcp-server
```

### Install with UV

If you prefer UV (which is often faster than pip):

**Install in project:**
```bash
uv add pdf-manipulation-mcp-server
```

**Install globally:**
```bash
uv tool install pdf-manipulation-mcp-server
```

After installation, you can run the server with:

```bash
pdf-mcp-server
```

## Alternative Installation Methods

### From GitHub (Latest Version)

If you want the latest development version:

**Run directly with UV (like npx):**
```bash
uv run git+https://github.com/yourusername/pdf-manipulation-mcp-server.git
```

**Install with pip:**
```bash
pip install git+https://github.com/yourusername/pdf-manipulation-mcp-server.git
```

**Install with UV:**
```bash
uv add git+https://github.com/yourusername/pdf-manipulation-mcp-server.git
```


## Configuration

After installation, configure your MCP client (like Cursor IDE) to use the server:

### For Cursor IDE

Add this to your Cursor settings:

```json
{
  "mcp.servers": {
    "pdf-manipulation": {
      "command": "pdf-mcp-server"
    }
  }
}
```

### For Other MCP Clients

The server runs as a standard MCP server and can be configured with any MCP-compatible client.

## Verification

To verify the installation works:

1. Run the server: `pdf-mcp-server`
2. You should see output indicating the server is running
3. Test with your MCP client

## Troubleshooting

### Common Issues

1. **Command not found**: Make sure the package was installed correctly
   ```bash
   # For pip
   pip show pdf-manipulation-mcp-server
   
   # For UV
   uv pip show pdf-manipulation-mcp-server
   ```

2. **Permission errors**: On some systems, you might need to use user installation
   ```bash
   # For pip
   pip install --user pdf-manipulation-mcp-server
   
   # For UV (usually not needed as UV handles this better)
   uv add pdf-manipulation-mcp-server
   ```

3. **Python version**: Make sure you have Python 3.10 or higher
   ```bash
   python --version
   # UV will automatically install the correct Python version if needed
   ```

4. **UV not found**: Install UV first
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

### Getting Help

If you encounter issues:

1. Check the [main README](README.md) for detailed documentation
2. Look at the [troubleshooting section](README.md#troubleshooting)
3. Open an issue on GitHub

## Uninstalling

To remove the package:

**Using pip:**
```bash
pip uninstall pdf-manipulation-mcp-server
```

**Using UV:**
```bash
uv remove pdf-manipulation-mcp-server
```
