# Claude Desktop Setup for Intelligent Math Genius MCP Server

## Overview
This document provides the complete setup instructions for integrating the Intelligent Math Genius MCP server with Claude Desktop.

## Issues Fixed

### 1. FastMCP Lifespan Context Manager
- **Problem**: `'FastMCP' object has no attribute 'on_startup'` and `'async_generator' object is not callable`
- **Solution**: Fixed the lifespan function to use proper `@asynccontextmanager` decorator with `app` parameter

### 2. Logging Configuration
- **Problem**: BrokenPipeError when server logged to stdout
- **Solution**: Redirected all logging to stderr using `stream=sys.stderr`

### 3. Dependency Resolution
- **Problem**: `uv run` couldn't find local `mathgenius` package
- **Solution**: Use existing virtual environment directly instead of `uv run`

## Final Configuration

### Claude Desktop Config
Add this to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "intelligent-math-genius": {
      "command": "/Users/phani.jammulamadaka/math-genius/.venv/bin/python",
      "args": [
        "-m",
        "intelligent_mcp_server.server"
      ],
      "cwd": "/Users/phani.jammulamadaka/math-genius/intelligent-mcp-server",
      "env": {
        "PYTHONPATH": "/Users/phani.jammulamadaka/math-genius:/Users/phani.jammulamadaka/math-genius/intelligent-mcp-server"
      }
    }
  }
}
```

## Prerequisites

1. **Virtual Environment**: Ensure the virtual environment is set up and activated:
   ```bash
   cd /Users/phani.jammulamadaka/math-genius
   python -m venv .venv
   source .venv/bin/activate
   ```

2. **Install Dependencies**: Install both packages in editable mode:
   ```bash
   # Install mathgenius package first
   cd mathgenius
   uv pip install -e .
   
   # Install intelligent-mcp-server package (this will also install all dependencies)
   cd ../intelligent-mcp-server
   uv pip install -e .
   ```

**IMPORTANT**: Both packages must be installed in editable mode in the same virtual environment for Claude Desktop to find them.

## Available Tools

The server provides 3 MCP tools:

1. **search_tool**: Search for mathematical tools using natural language queries
2. **execute_tool**: Execute mathematical tools with specified parameters
3. **server_info**: Get information about the server configuration and capabilities

## Verification

To verify the setup works:

```bash
cd /Users/phani.jammulamadaka/math-genius/intelligent-mcp-server
PYTHONPATH="/Users/phani.jammulamadaka/math-genius:/Users/phani.jammulamadaka/math-genius/intelligent-mcp-server" \
/Users/phani.jammulamadaka/math-genius/.venv/bin/python -c "
from intelligent_mcp_server.server import IntelligentMCPServer
server = IntelligentMCPServer()
print('✅ Server ready for Claude Desktop')
"
```

## Troubleshooting

### If you see "spawn uv ENOENT"
- The configuration now uses the virtual environment Python directly, avoiding this issue

### If you see "mathgenius was not found"
- Ensure mathgenius is installed in editable mode: `cd mathgenius && uv pip install -e .`

### If you see "BrokenPipeError"
- This has been fixed by redirecting logging to stderr

### If tools don't appear in Claude
- Restart Claude Desktop after updating the configuration
- Check the Claude Desktop logs for any connection errors

## Success Indicators

When working correctly, you should see in Claude Desktop logs:
- "Server started and connected successfully"
- "Message from client: initialize"
- No error messages about broken pipes or missing dependencies

The server will be available in Claude Desktop and you can use natural language to search for and execute mathematical operations.
