# 9. Technology Stack

## 9.1 Core Dependencies
- **ChromaDB**: Vector database for tool search with SQLite backend
- **sentence-transformers**: Generate semantic embeddings for tool descriptions
- **NumPy/SciPy**: Mathematical computations (existing)
- **SymPy**: Symbolic mathematics (existing)

## 9.2 New Dependencies
```toml
[tool.poetry.dependencies]
chromadb = "^0.4.0"           # Vector database
sentence-transformers = "^2.2.2"  # Text embeddings
sqlite3 = "*"                 # Included with Python
```
