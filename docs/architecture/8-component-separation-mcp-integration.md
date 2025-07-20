# 8. Component Separation: MCP Integration

## 8.1 Updated MCP Component Structure
```
mgenius-mcp/
├── __init__.py
├── server.py                  # MCP server implementation
├── search_tools.py            # NEW: search_tool and execute_tool implementations
├── handlers.py                # Updated MCP request handlers
├── config.py                  # MCP configuration
├── tests/                     # MCP-specific tests
├── pyproject.toml             # MCP package config
└── README.md                  # Updated MCP setup guide
```

## 8.2 Integration Pattern
```mermaid
graph TB
    MCP[MCP Client] -->|search_tool| MCPS[MCP Server - mgenius-mcp]
    MCP -->|execute_tool| MCPS
    MCPS -->|search| VS[Vector Search Engine]
    MCPS -->|execute| MGD[mathgenius.api.dispatcher]
    
    VS -->|query| CDB[ChromaDB Vector Store]
    MGD -->|calls| MG[mathgenius core library]
    
    subgraph "mgenius-mcp (root level)"
        MCPS
        ST[Search Tool Handler]
        ET[Execute Tool Handler]
    end
    
    subgraph "mathgenius (root level)"
        VS
        CDB
        MGD
        MG
        MGCore[Core Math Functions]
    end
```
