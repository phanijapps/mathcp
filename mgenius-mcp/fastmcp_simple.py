#!/usr/bin/env python3
"""
Simple FastMCP server for Math Genius - exposes all mathematical tools via dispatcher
"""

import sys
import inspect
from pathlib import Path
from typing import Any, Dict, List, Union


# Add math-genius to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from fastmcp import FastMCP
    from pydantic import BaseModel, Field
    from fastmcp.client.transports import SSETransport
    import uvicorn
except ImportError:
    print("Please install fastmcp and pydantic: pip install fastmcp pydantic")
    sys.exit(1)

# Import all mathgenius functions
import mathgenius.api.dispatcher as dispatcher

# Create the FastMCP app
app = FastMCP("math-genius", "1.0.0")

def get_function_description(func) -> str:
    """Get function description from docstring."""
    if func.__doc__:
        return func.__doc__.split('\n')[0].strip()
    else:
        name = func.__name__
        return f"Mathematical operation: {name.replace('_', ' ')}"

def get_function_parameters(func) -> Dict[str, Any]:
    """Extract parameters from function signature."""
    try:
        sig = inspect.signature(func)
        parameters = {}
        
        for param_name, param in sig.parameters.items():
            param_info = {
                "type": "number",
                "description": f"Parameter {param_name}"
            }
            
            # Check if parameter has default value
            if param.default != inspect.Parameter.empty:
                param_info["default"] = param.default
            else:
                param_info["required"] = True
            
            # Special handling for known parameter types
            if param_name in ['data', 'values', 'points']:
                param_info["type"] = "array"
                param_info["items"] = {"type": "number"}
            elif param_name in ['expression', 'equation', 'symbol']:
                param_info["type"] = "string"
            elif param_name in ['matrix', 'vector']:
                param_info["type"] = "array"
                param_info["items"] = {"type": "array", "items": {"type": "number"}}
            
            parameters[param_name] = param_info
        
        return parameters
        
    except Exception as e:
        return {"value": {"type": "number", "description": "Input value", "required": True}}

# Register all tools
tools_registered = 0

for name in dir(dispatcher):
    if not name.startswith('_'):
        func = getattr(dispatcher, name)
        if callable(func):
            try:
                description = get_function_description(func)
                parameters = get_function_parameters(func)
                
                # Create dynamic Pydantic model for parameters
                param_fields = {}
                annotations = {}
                
                for param_name, param_info in parameters.items():
                    if param_info.get('type') == 'array':
                        param_type = List[Union[float, int, List[float]]]
                    elif param_info.get('type') == 'string':
                        param_type = str
                    else:
                        param_type = Union[float, int]
                    
                    annotations[param_name] = param_type
                    param_fields[param_name] = Field(description=param_info['description'])
                
                # Create the Pydantic model with proper annotations
                ParamModel = type(
                    f"{name}_params", 
                    (BaseModel,), 
                    {
                        '__annotations__': annotations,
                        **param_fields
                    }
                )
                
                # Create tool handler function
                def create_handler(func_name, func_obj):
                    async def tool_handler(params: ParamModel):
                        """Dynamic tool handler."""
                        try:
                            kwargs = params.model_dump()
                            result = func_obj(**kwargs)
                            return {
                                "result": result,
                                "success": True,
                                "tool": func_name
                            }
                        except Exception as e:
                            return {
                                "error": str(e),
                                "success": False,
                                "tool": func_name
                            }
                    return tool_handler
                
                # Register the tool
                handler = create_handler(name, func)
                app.tool(name=name, description=description)(handler)
                
                tools_registered += 1
                
            except Exception as e:
                print(f"Warning: Could not register tool {name}: {e}")
                continue

print(f"🧮 Math Genius FastMCP Server - {tools_registered} tools registered")

if __name__ == "__main__":
    print("🚀 Starting server...")
    print("📡 Running FastMCP with SSE on http://127.0.0.1:8000")
    
    # Run with SSE transport using asyncio
    app.run()
