# 5. New MCP Interface Design

## 5.1 Simplified MCP Tools
Instead of exposing 100+ individual tools, the new architecture exposes only 2 intelligent tools:

### `search_tool`
```python
async def search_tool(query: str, limit: int = 5) -> List[ToolSearchResult]:
    """
    Search for mathematical tools based on description using vector similarity.
    
    Args:
        query: Natural language description of what you want to do
        limit: Maximum number of tools to return (default: 5)
    
    Returns:
        List of matching tools with relevance scores
    """
```

### `execute_tool`
```python
async def execute_tool(tool_name: str, parameters: Dict[str, Any]) -> ToolExecutionResult:
    """
    Execute a specific mathematical tool with given parameters.
    
    Args:
        tool_name: Name of the tool to execute (from search results)
        parameters: Dictionary of parameters for the tool
        
    Returns:
        Result of the mathematical computation
    """
```

## 5.2 Tool Search Results Structure
```python
@dataclass
class ToolSearchResult:
    name: str                    # Tool name for execution
    description: str             # Human-readable description
    category: str               # Math domain category
    similarity_score: float     # Relevance score (0-1)
    parameters: Dict[str, Any]  # Parameter schema
    examples: List[Dict]        # Usage examples
```
