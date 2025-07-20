# 3. Product Architecture

## 3.1 System Components
```
Math Genius Platform
├── mathgenius/              # Core mathematical library
│   ├── arithmetic/          # Basic operations
│   ├── algebra/             # Equation solving, polynomials
│   ├── geometry/            # Shapes, coordinates, spatial
│   ├── advanced/            # Calculus, linear algebra, statistics, symbolic
│   ├── core/                # Validation, errors
│   └── api/                 # Unified dispatcher
└── mgenius-mcp/             # MCP protocol server
    ├── server.py            # MCP server implementation
    ├── tools.py             # Tool discovery and registration
    ├── handlers.py          # Request handlers
    └── config.py            # Configuration management
```

## 3.2 Technology Stack
- **Language**: Python 3.12+
- **Core Dependencies**: NumPy, SciPy, SymPy, scikit-learn, matplotlib, pandas
- **MCP Framework**: FastMCP 2.10.5+
- **API Framework**: FastAPI, Pydantic
- **Testing**: pytest, pytest-asyncio, pytest-cov
- **Quality Tools**: black, flake8, mypy

## 3.3 Integration Patterns
- **Direct Import**: `from mathgenius.api import solve_equation`
- **MCP Protocol**: Tool calls via Model Context Protocol
- **Future REST API**: HTTP endpoints for web integration
- **Future GraphQL**: Query-based mathematical operations
