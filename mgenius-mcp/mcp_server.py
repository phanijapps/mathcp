#!/usr/bin/env python3
"""
MCP Server for Math Genius - Compatible with Claude Desktop
"""

import asyncio
import json
import logging
import sys
from typing import Any, Dict, List, Optional
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))
sys.path.insert(0, str(current_dir.parent))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/tmp/mcp_server.log'),
        logging.StreamHandler(sys.stderr)
    ]
)
logger = logging.getLogger(__name__)

class MCPServer:
    """Simple MCP server implementation for Claude Desktop."""
    
    def __init__(self):
        self.tools = {}
        self.setup_tools()
    
    def setup_tools(self):
        """Setup available mathematical tools."""
        try:
            # Import mathgenius functions
            import mathgenius.api.dispatcher as dispatcher
            
            # Define available tools
            self.tools = {
                "add": {
                    "name": "add",
                    "description": "Add two numbers",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "a": {"type": "number", "description": "First number"},
                            "b": {"type": "number", "description": "Second number"}
                        },
                        "required": ["a", "b"]
                    },
                    "function": dispatcher.add
                },
                "subtract": {
                    "name": "subtract",
                    "description": "Subtract two numbers",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "a": {"type": "number", "description": "First number"},
                            "b": {"type": "number", "description": "Second number"}
                        },
                        "required": ["a", "b"]
                    },
                    "function": dispatcher.subtract
                },
                "multiply": {
                    "name": "multiply",
                    "description": "Multiply two numbers",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "a": {"type": "number", "description": "First number"},
                            "b": {"type": "number", "description": "Second number"}
                        },
                        "required": ["a", "b"]
                    },
                    "function": dispatcher.multiply
                },
                "divide": {
                    "name": "divide",
                    "description": "Divide two numbers",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "a": {"type": "number", "description": "Dividend"},
                            "b": {"type": "number", "description": "Divisor"}
                        },
                        "required": ["a", "b"]
                    },
                    "function": dispatcher.divide
                },
                "sin": {
                    "name": "sin",
                    "description": "Calculate sine of a number (in radians)",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "x": {"type": "number", "description": "Angle in radians"}
                        },
                        "required": ["x"]
                    },
                    "function": dispatcher.sin
                },
                "cos": {
                    "name": "cos",
                    "description": "Calculate cosine of a number (in radians)",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "x": {"type": "number", "description": "Angle in radians"}
                        },
                        "required": ["x"]
                    },
                    "function": dispatcher.cos
                },
                "circle_area": {
                    "name": "circle_area",
                    "description": "Calculate the area of a circle",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "radius": {"type": "number", "description": "Circle radius", "minimum": 0}
                        },
                        "required": ["radius"]
                    },
                    "function": dispatcher.circle_area
                },
                "rectangle_area": {
                    "name": "rectangle_area",
                    "description": "Calculate the area of a rectangle",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "length": {"type": "number", "description": "Length of rectangle", "minimum": 0},
                            "width": {"type": "number", "description": "Width of rectangle", "minimum": 0}
                        },
                        "required": ["length", "width"]
                    },
                    "function": dispatcher.rectangle_area
                },
                "solve_quadratic": {
                    "name": "solve_quadratic",
                    "description": "Solve quadratic equation ax² + bx + c = 0",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "a": {"type": "number", "description": "Coefficient of x²"},
                            "b": {"type": "number", "description": "Coefficient of x"},
                            "c": {"type": "number", "description": "Constant term"}
                        },
                        "required": ["a", "b", "c"]
                    },
                    "function": dispatcher.solve_quadratic
                },
                "distance_2d": {
                    "name": "distance_2d",
                    "description": "Calculate distance between two 2D points",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "x1": {"type": "number", "description": "X coordinate of first point"},
                            "y1": {"type": "number", "description": "Y coordinate of first point"},
                            "x2": {"type": "number", "description": "X coordinate of second point"},
                            "y2": {"type": "number", "description": "Y coordinate of second point"}
                        },
                        "required": ["x1", "y1", "x2", "y2"]
                    },
                    "function": dispatcher.distance_2d
                },
                "mean": {
                    "name": "mean",
                    "description": "Calculate the arithmetic mean of a list of numbers",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "data": {"type": "array", "items": {"type": "number"}, "description": "List of numbers"}
                        },
                        "required": ["data"]
                    },
                    "function": dispatcher.mean
                }
            }
            
            logger.info(f"✅ Loaded {len(self.tools)} mathematical tools")
            
        except ImportError as e:
            logger.error(f"❌ Failed to import mathgenius: {e}")
            # Fallback tools with simple implementations
            self.tools = {
                "add": {
                    "name": "add",
                    "description": "Add two numbers",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "a": {"type": "number", "description": "First number"},
                            "b": {"type": "number", "description": "Second number"}
                        },
                        "required": ["a", "b"]
                    },
                    "function": lambda a, b: a + b
                }
            }
    
    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP request."""
        try:
            method = request.get("method")
            params = request.get("params", {})
            
            if method == "tools/list":
                # Return list of available tools
                tools = []
                for tool_name, tool_info in self.tools.items():
                    tools.append({
                        "name": tool_info["name"],
                        "description": tool_info["description"],
                        "inputSchema": tool_info["inputSchema"]
                    })
                
                return {
                    "tools": tools
                }
            
            elif method == "tools/call":
                # Call a specific tool
                tool_name = params.get("name")
                arguments = params.get("arguments", {})
                
                if tool_name not in self.tools:
                    return {
                        "error": {
                            "code": -32601,
                            "message": f"Tool '{tool_name}' not found"
                        }
                    }
                
                tool = self.tools[tool_name]
                try:
                    # Call the function
                    if callable(tool["function"]):
                        result = tool["function"](**arguments)
                    else:
                        result = tool["function"]
                    
                    return {
                        "content": [
                            {
                                "type": "text",
                                "text": f"Result: {result}"
                            }
                        ]
                    }
                    
                except Exception as e:
                    logger.error(f"Error calling tool {tool_name}: {e}")
                    return {
                        "error": {
                            "code": -32603,
                            "message": f"Error executing tool: {str(e)}"
                        }
                    }
            
            else:
                return {
                    "error": {
                        "code": -32601,
                        "message": f"Method '{method}' not found"
                    }
                }
        
        except Exception as e:
            logger.error(f"Error handling request: {e}")
            return {
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                }
            }
    
    async def run(self):
        """Run the MCP server."""
        logger.info("🧮 Math Genius MCP Server Starting...")
        logger.info("=" * 50)
        logger.info(f"Available tools: {list(self.tools.keys())}")
        
        try:
            while True:
                # Read JSON-RPC request from stdin
                line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
                if not line:
                    break
                
                try:
                    request = json.loads(line.strip())
                    logger.info(f"Received request: {request.get('method', 'unknown')}")
                    
                    response = await self.handle_request(request)
                    
                    # Add request ID to response
                    if "id" in request:
                        response["id"] = request["id"]
                    
                    # Send response
                    print(json.dumps(response), flush=True)
                    
                except json.JSONDecodeError as e:
                    logger.error(f"Invalid JSON: {e}")
                    error_response = {
                        "error": {
                            "code": -32700,
                            "message": "Parse error"
                        }
                    }
                    print(json.dumps(error_response), flush=True)
                
        except KeyboardInterrupt:
            logger.info("🛑 Server stopped by user")
        except Exception as e:
            logger.error(f"❌ Server error: {e}")
            raise

def main():
    """Main entry point."""
    server = MCPServer()
    asyncio.run(server.run())

if __name__ == "__main__":
    main()
