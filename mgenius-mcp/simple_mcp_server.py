#!/usr/bin/env python3
"""
Simple FastMCP server for Math Genius - exposes all mathematical tools via dispatcher
"""

import asyncio
import sys
import inspect
from pathlib import Path
from typing import Any, Dict, List, Union

# Add math-genius to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from fastmcp import FastMCP
    from pydantic import BaseModel, Field
except ImportError:
    print("Please install fastmcp and pydantic: pip install fastmcp pydantic")
    sys.exit(1)

# Import all mathgenius functions
import mathgenius.api.dispatcher as dispatcher

class MathGeniusServer:
    """FastMCP server for Math Genius mathematical tools."""
    
    def __init__(self):
        self.app = FastMCP("math-genius", "1.0.0")
        self.tools_registered = 0
        
    def discover_tools(self) -> List[Dict[str, Any]]:
        """Discover all available tools from mathgenius dispatcher."""
        tools = []
        
        # Get all functions from dispatcher
        for name in dir(dispatcher):
            if not name.startswith('_'):
                func = getattr(dispatcher, name)
                if callable(func):
                    tools.append({
                        'name': name,
                        'function': func,
                        'description': self._get_function_description(func),
                        'parameters': self._get_function_parameters(func)
                    })
        
        return tools
    
    def _get_function_description(self, func) -> str:
        """Get function description from docstring."""
        if func.__doc__:
            # Get first line of docstring
            return func.__doc__.split('\n')[0].strip()
        else:
            # Generate description from function name
            name = func.__name__
            return f"Mathematical operation: {name.replace('_', ' ')}"
    
    def _get_function_parameters(self, func) -> Dict[str, Any]:
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
            # Fallback for functions we can't inspect
            return {"value": {"type": "number", "description": "Input value", "required": True}}
    
    def register_tools(self):
        """Register all discovered tools with FastMCP."""
        tools = self.discover_tools()
        
        for tool_info in tools:
            try:
                # Create dynamic Pydantic model for parameters
                param_fields = {}
                annotations = {}
                
                for param_name, param_info in tool_info['parameters'].items():
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
                    f"{tool_info['name']}_params", 
                    (BaseModel,), 
                    {
                        '__annotations__': annotations,
                        **param_fields
                    }
                )
                
                # Create a closure to capture tool_info
                def create_handler(tool_info):
                    async def tool_handler(params: ParamModel):
                        """Dynamic tool handler."""
                        try:
                            # Convert params to dict
                            kwargs = params.model_dump()
                            
                            # Call the mathgenius function
                            result = tool_info['function'](**kwargs)
                            
                            return {
                                "result": result,
                                "success": True,
                                "tool": tool_info['name']
                            }
                        
                        except Exception as e:
                            return {
                                "error": str(e),
                                "success": False,
                                "tool": tool_info['name']
                            }
                    return tool_handler
                
                # Register the tool
                handler = create_handler(tool_info)
                self.app.tool(name=tool_info['name'], description=tool_info['description'])(handler)
                
                self.tools_registered += 1
                
            except Exception as e:
                print(f"Warning: Could not register tool {tool_info['name']}: {e}")
                continue
        
        print(f"✅ Registered {self.tools_registered} mathematical tools")
    
    async def run(self):
        """Run the FastMCP server."""
        print("🧮 Math Genius FastMCP Server")
        print("=" * 40)
        
        # Register all tools
        self.register_tools()
        
        print(f"🚀 Starting server with {self.tools_registered} tools...")
        print("📡 Server ready for Claude Desktop connection")
        
        # Run the server
        await self.app.run(host="127.0.0.1", port=8000)

def main():
    """Main entry point."""
    server = MathGeniusServer()
    
    try:
        import nest_asyncio
        nest_asyncio.apply()
        asyncio.run(server.run())
    except ImportError:
        try:
            asyncio.run(server.run())
        except RuntimeError as e:
            if "already running" in str(e):
                print("⚠️  Asyncio already running - using existing loop")
                loop = asyncio.get_event_loop()
                loop.run_until_complete(server.run())
            else:
                raise
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
