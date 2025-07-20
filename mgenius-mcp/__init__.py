"""MCP server package for Math Genius mathematical tools."""

__version__ = "0.1.0"
__author__ = "Math Genius Team"
__email__ = "dev@mathgenius.com"
__description__ = "MCP (Model Context Protocol) server for Math Genius mathematical tools"

from .server import MCPServer
from .config import MCPConfig

__all__ = ["MCPServer", "MCPConfig"]
