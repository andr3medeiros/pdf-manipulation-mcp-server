#!/usr/bin/env python3
"""
PDF Manipulation MCP Server Entry Point

This is the main entry point for the PDF Manipulation MCP Server.
Run with: uv run python server.py
"""

import asyncio
from .pdf_server import mcp

def main():
    """Main function to run the MCP server."""
    mcp.run()

if __name__ == "__main__":
    main()
