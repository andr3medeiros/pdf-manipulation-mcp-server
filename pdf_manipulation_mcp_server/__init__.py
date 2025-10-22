"""
PDF Manipulation MCP Server

A study project implementing a Model Context Protocol (MCP) server 
that provides comprehensive PDF manipulation capabilities.
"""

from .pdf_server import mcp
from .server import main

__version__ = "0.1.0"
__author__ = "André da Silva Medeiros"
__email__ = "andr3medeiros@gmail.com"

__all__ = ["mcp", "main"]
