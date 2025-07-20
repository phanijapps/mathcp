# 3. High-Level Component Diagram

```
math_genius/
├── core/                # Core utilities, validation, error handling
├── arithmetic/          # Basic arithmetic operations
├── algebra/             # Algebraic functions (solve, factor, simplify)
├── geometry/            # Geometric calculations
├── trigonometry/        # Trigonometric functions
├── calculus/            # Calculus operations
├── linear_algebra/      # Matrix, vector, eigenvalue ops
├── statistics/          # Stats, probability, distributions
├── symbolic/            # Symbolic computation (using SymPy)
├── api/                 # Unified API layer (internal, for future REST/MCP)
├── search/              # NEW: Vector search and tool discovery
│   ├── __init__.py
│   ├── tool_indexer.py      # Tool documentation indexer
│   ├── vector_search.py     # ChromaDB-based vector search
│   ├── tool_metadata.py     # Tool metadata extraction
│   └── embeddings.py        # Text embedding generation
├── tests/               # Comprehensive test suite
└── docs/                # Usage, API reference, examples
```
