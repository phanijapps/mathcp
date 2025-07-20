# 4. Key Design Decisions

## 4.1 Original Architecture
- **Python 3.12**: Leverage latest language features, type hints, and async where needed
- **Modular Packages**: Each math domain is a self-contained module, importable independently
- **Unified API Layer**: All functions exposed via a single, consistent API (e.g., `math_genius.api`)
- **Input Validation**: Centralized in `core/validation.py` for all modules
- **Error Handling**: Custom exceptions in `core/errors.py`
- **Extensibility**: New math domains can be added as new modules with minimal friction

## 4.2 New Search-Based Architecture
- **Vector Search**: ChromaDB with SQLite backend for tool discovery via semantic similarity
- **Tool Documentation**: Automated generation of searchable tool descriptions and examples
- **Smart MCP Interface**: Only 2 MCP tools (`search_tool`, `execute_tool`) instead of 100+
- **Embedding Service**: Generate semantic embeddings for tool descriptions and user queries
- **Tool Metadata System**: Rich metadata extraction from function signatures and docstrings
