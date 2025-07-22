# Intelligent MCP Server

An intelligent Model Context Protocol (MCP) server that provides semantic search and execution of 85+ mathematical functions through just 2 smart tools: `search_tool` and `execute_tool`.

## Features

- **🔍 Semantic Search**: Find mathematical tools using natural language queries
- **⚡ Intelligent Execution**: Execute mathematical functions with parameter validation
- **🧠 Vector Search**: ChromaDB-powered semantic similarity search
- **📊 85+ Mathematical Functions**: Complete coverage of arithmetic, algebra, geometry, calculus, statistics, and more
- **🚀 High Performance**: Sub-100ms search responses, configurable execution timeouts
- **🛡️ Robust Error Handling**: Comprehensive validation and error recovery
- **📝 Rich Documentation**: Auto-generated tool documentation with examples

## Architecture

Instead of exposing 85+ individual MCP tools, this server provides an intelligent interface with just 2 tools:

### Core Tools

1. **`search_tool`** - Search for mathematical tools using natural language
   - Semantic similarity search using sentence transformers
   - Category filtering and result ranking
   - Rich metadata including examples and mathematical context

2. **`execute_tool`** - Execute mathematical tools with parameters
   - Parameter validation and type conversion
   - Timeout protection and error handling
   - Detailed execution results and metadata

3. **`server_info`** - Get server information and statistics

## Quick Start

### Installation

```bash
# Clone and install
git clone <repository-url>
cd intelligent-mcp-server
pip install -e .

# Or install dependencies manually
pip install -r requirements.txt
```

### MCP Client Configuration

Add this configuration to your MCP client (e.g., Claude Desktop `config.json`):

```json
{
  "mcpServers": {
    "intelligent-math-genius": {
      "command": "python",
      "args": [
        "-m", "intelligent_mcp_server.server"
      ],
      "cwd": "/path/to/intelligent-mcp-server",
      "env": {
        "MCP_INTELLIGENT_MODE": "true",
        "MCP_SEARCH_INDEX_STARTUP": "true",
        "MCP_LOG_LEVEL": "INFO"
      }
    }
  }
}
```

**For Claude Desktop specifically:**
1. Open Claude Desktop
2. Go to Settings → Developer → Edit Config
3. Copy the configuration from `claude_desktop_config.json` (included in this repository)
4. Update the paths in the config to match your installation
5. Restart Claude Desktop
6. The intelligent math tools will be available with just 2 tools: `search_tool` and `execute_tool`

**Quick Setup:**
```bash
# Copy the example config
cp claude_desktop_config.json ~/.config/claude-desktop/config.json
# Edit paths to match your installation
nano ~/.config/claude-desktop/config.json
```

**Alternative direct execution:**
```json
{
  "mcpServers": {
    "intelligent-math-genius": {
      "command": "/path/to/python",
      "args": ["/path/to/intelligent-mcp-server/intelligent_mcp_server/server.py"],
      "env": {
        "PYTHONPATH": "/path/to/mathgenius:/path/to/intelligent-mcp-server"
      }
    }
  }
}
```

### Usage

```bash
# Run the server standalone
intelligent-mcp-server

# Or run directly
python -m intelligent_mcp_server.server

# With custom configuration
MCP_INTELLIGENT_MODE=true MCP_LOG_LEVEL=DEBUG python -m intelligent_mcp_server.server
```

### Environment Configuration

```bash
# Optional environment variables
export MCP_INTELLIGENT_MODE=true           # Enable intelligent interface (default)
export MCP_SEARCH_INDEX_STARTUP=true       # Build search index at startup (default)
export MCP_EMBEDDING_MODEL=all-MiniLM-L6-v2  # Sentence transformer model
export MCP_EXECUTION_TIMEOUT=30.0          # Tool execution timeout in seconds
export MCP_LOG_LEVEL=INFO                  # Logging level
```

## Example Workflows

### 1. Search and Execute Pattern

```python
# Search for triangle area calculation
search_results = await search_tool(
    query="calculate area of triangle",
    limit=3
)

# Results show triangle_area tool with parameters: base, height
execution_result = await execute_tool(
    tool_name="triangle_area",
    parameters={"base": 10, "height": 6}
)
# Result: 30.0
```

### 2. Category-based Discovery

```python
# Find all geometry tools
geometry_tools = await search_tool(
    query="geometry",
    category="geometry",
    limit=10
)

# Execute a specific geometry function
result = await execute_tool(
    tool_name="circle_area",
    parameters={"radius": 5}
)
# Result: 78.54 (π × 5²)
```

### 3. Complex Mathematical Operations

```python
# Search for matrix operations
matrix_tools = await search_tool(
    query="multiply matrices",
    limit=5
)

# Execute matrix multiplication
result = await execute_tool(
    tool_name="matrix_multiply",
    parameters={
        "matrix1": [[1, 2], [3, 4]],
        "matrix2": [[5, 6], [7, 8]]
    }
)
# Result: [[19, 22], [43, 50]]
```

## Mathematical Categories

The server provides tools across 8 mathematical domains:

- **Arithmetic**: Basic operations (add, subtract, multiply, divide, power, modulo)
- **Algebra**: Equation solving, expression manipulation
- **Geometry**: Area, volume, perimeter calculations for shapes
- **Trigonometry**: Trigonometric functions and conversions
- **Coordinates**: 2D/3D point operations, distance calculations
- **Vectors**: Vector operations and transformations
- **Calculus**: Derivatives, integrals, limits, series
- **Linear Algebra**: Matrix operations, decompositions, systems
- **Statistics**: Descriptive statistics, distributions, hypothesis testing
- **Symbolic Mathematics**: Expression parsing, symbolic computation

## Search Capabilities

The search engine understands natural language queries like:

- "calculate area of triangle" → `triangle_area`
- "find distance between points" → `distance_2d`, `distance_3d`
- "matrix multiplication" → `matrix_multiply`
- "solve quadratic equation" → `solve_quadratic`
- "statistical average" → `mean`, `median`
- "derivative of function" → `differentiate`, `symbolic_differentiate`

## Configuration

### Server Settings

```python
# In config.py or via environment variables
server_name = "intelligent-math-genius"
intelligent_mode = True  # Use intelligent interface
search_index_startup = True  # Build index at startup
embedding_model = "all-MiniLM-L6-v2"  # Sentence transformer model
execution_timeout = 30.0  # Seconds
```

### Search Settings

```python
search_limit_default = 5    # Default search results
search_limit_max = 20       # Maximum search results
vector_db_path = "./data/vector_db"  # ChromaDB storage
```

## Performance

- **Search Response Time**: < 100ms for typical queries
- **Indexing Time**: ~30 seconds for 85+ tools at startup
- **Memory Usage**: ~500MB including embedding model
- **Embedding Model**: 384-dimensional vectors (all-MiniLM-L6-v2)

## Development

### Project Structure

```
intelligent-mcp-server/
├── intelligent_mcp_server/
│   ├── __init__.py           # Package initialization
│   ├── server.py             # Main MCP server
│   ├── config.py             # Configuration management
│   ├── search/               # Search functionality
│   │   ├── tool_indexer.py   # Tool documentation indexer
│   │   ├── vector_search.py  # ChromaDB vector search engine
│   │   └── embeddings.py     # Sentence transformer service
│   └── execute/              # Execution functionality
│       └── tool_executor.py  # Tool execution with validation
├── tests/                    # Test suite
├── pyproject.toml           # Project configuration
└── README.md               # This file
```

### Running Tests

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=intelligent_mcp_server --cov-report=html
```

### Adding New Mathematical Functions

1. Add functions to the `mathgenius` library
2. Update `tool_indexer.py` category mapping
3. Add validation rules in `tool_executor.py` if needed
4. Rebuild search index: `force_reindex=True`

## Dependencies

### Core Dependencies
- `fastmcp>=0.2.0` - MCP server framework
- `chromadb>=0.4.0` - Vector database
- `sentence-transformers>=2.2.2` - Text embeddings
- `mathgenius>=0.2.0` - Mathematical functions library
- `pydantic>=2.5.0` - Data validation
- `numpy>=1.24.0` - Numerical computing

### Mathematical Libraries
- `scipy>=1.11.0` - Scientific computing
- `sympy>=1.12` - Symbolic mathematics
- `pandas>=2.0.0` - Data analysis
- `matplotlib>=3.7.0` - Plotting (for some functions)

## Migration from Legacy MCP Servers

This intelligent server replaces traditional MCP servers that expose individual tools:

### Before (Legacy)
```python
# 85+ individual MCP tools
triangle_area_tool()
circle_area_tool()
matrix_multiply_tool()
# ... 82+ more tools
```

### After (Intelligent)
```python
# Just 2 intelligent tools
search_tool("calculate triangle area")  # Discovery
execute_tool("triangle_area", {...})    # Execution
```

### Benefits
- **Simplified Discovery**: Natural language search vs. browsing 85+ tools
- **Reduced Cognitive Load**: 2 tools vs. 85+ tool names to remember
- **Better Discoverability**: Semantic search finds relevant tools
- **Consistent Interface**: Same pattern for all mathematical operations
- **Enhanced Documentation**: Rich metadata and examples for each tool

## Troubleshooting

### Common Issues

1. **Slow Startup**: Search indexing takes ~30 seconds on first run
   - Set `MCP_SEARCH_INDEX_STARTUP=false` to disable startup indexing
   - Index will be built on first search request instead

2. **Memory Usage**: Embedding model uses ~400MB RAM
   - Use smaller model: `MCP_EMBEDDING_MODEL=all-MiniLM-L12-v2`
   - Or disable search index: run in legacy mode

3. **Search Not Finding Tools**: 
   - Check search query phrasing
   - Try different mathematical terms
   - Use category filter to narrow results

4. **Execution Timeouts**:
   - Increase timeout: `MCP_EXECUTION_TIMEOUT=60.0`
   - Check parameter validation errors
   - Monitor server logs for details

### Logging

```bash
# Enable debug logging
export MCP_LOG_LEVEL=DEBUG

# Check server logs
tail -f server.log
```

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## Roadmap

- [ ] Add more mathematical function categories
- [ ] Implement caching for frequent searches
- [ ] Add batch execution capabilities
- [ ] Support for custom embedding models
- [ ] Integration with external math libraries
- [ ] Performance optimization for large-scale deployments
