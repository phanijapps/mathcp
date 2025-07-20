"""FastMCP server implementation for Math Genius mathematical tools."""

import asyncio
import logging
import signal
import sys
from typing import Dict, Any, Optional, List
from contextlib import asynccontextmanager

try:
    from fastmcp import FastMCP
    from fastmcp.tools import Tool
    from fastmcp.server import MCPServer as BaseMCPServer
    from fastmcp.exceptions import MCPError
except ImportError:
    # Fallback for development - we'll implement a minimal FastMCP interface
    class FastMCP:
        def __init__(self, name: str, version: str):
            self.name = name
            self.version = version
            self.tools = {}
        
        def add_tool(self, tool):
            self.tools[tool.name] = tool
        
        async def run(self, host: str = "localhost", port: int = 8000):
            print(f"Mock MCP server running on {host}:{port}")
            await asyncio.sleep(1)
    
    class Tool:
        def __init__(self, name: str, description: str, parameters: Dict[str, Any]):
            self.name = name
            self.description = description
            self.parameters = parameters
    
    class MCPError(Exception):
        pass

from .config import MCPConfig
from .tools import ToolRegistry, ToolCategory
from .handlers import MCPHandlerRegistry, MCPRequestRouter
from .schema_validation import SchemaGenerator, SchemaValidator
from .error_handling import ErrorHandler, ResponseFormatter, PerformanceMonitor

logger = logging.getLogger(__name__)


class MCPServer:
    """MCP server for Math Genius mathematical tools."""
    
    def __init__(self, config: Optional[MCPConfig] = None):
        """Initialize MCP server with configuration."""
        self.config = config or MCPConfig.from_env()
        self.config.setup_logging()
        
        self.app = FastMCP(
            name=self.config.server_name,
            version=self.config.server_version
        )
        
        # Initialize components
        self.handler_registry = MCPHandlerRegistry()
        self.schema_generator = SchemaGenerator()
        self.schema_validator = SchemaValidator()
        self.error_handler = ErrorHandler(self.config.max_computation_time)
        self.response_formatter = ResponseFormatter(self.config.precision)
        self.performance_monitor = PerformanceMonitor(self.config.max_computation_time)
        self.router = MCPRequestRouter(self.handler_registry)
        
        self._is_running = False
        self._shutdown_event = asyncio.Event()
        
        # Setup signal handlers
        self._setup_signal_handlers()
        
        logger.info(f"MCP Server initialized: {self.config}")
    
    def _setup_signal_handlers(self) -> None:
        """Setup signal handlers for graceful shutdown."""
        def signal_handler(signum, frame):
            logger.info(f"Received signal {signum}, initiating shutdown...")
            self._shutdown_event.set()
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    async def initialize(self) -> None:
        """Initialize the MCP server and register tools."""
        logger.info("Initializing MCP server...")
        
        # This will be implemented in Task 2: Tool Discovery & Registration
        await self._register_tools()
        
        logger.info("MCP server initialized successfully")
    
    async def _register_tools(self) -> None:
        """Register mathematical tools with MCP server."""
        logger.info("Registering mathematical tools...")
        
        # Get enabled categories from config
        enabled_categories = []
        if self.config.enable_arithmetic:
            enabled_categories.append(ToolCategory.ARITHMETIC)
        if self.config.enable_algebra:
            enabled_categories.append(ToolCategory.ALGEBRA)
        if self.config.enable_geometry:
            enabled_categories.append(ToolCategory.GEOMETRY)
        if self.config.enable_trigonometry:
            enabled_categories.append(ToolCategory.TRIGONOMETRY)
        if self.config.enable_calculus:
            enabled_categories.append(ToolCategory.CALCULUS)
        if self.config.enable_linear_algebra:
            enabled_categories.append(ToolCategory.LINEAR_ALGEBRA)
        if self.config.enable_statistics:
            enabled_categories.append(ToolCategory.STATISTICS)
        if self.config.enable_symbolic:
            enabled_categories.append(ToolCategory.SYMBOLIC)
        
        # Register handlers
        handler_count = self.handler_registry.register_all_handlers(enabled_categories)
        
        # Generate and register schemas
        discovered_tools = self.handler_registry.tool_registry.discovery.discovered_tools
        for tool_name, metadata in discovered_tools.items():
            schema = self.schema_generator.generate_schema(tool_name, metadata.function)
            self.schema_validator.register_schema(tool_name, schema)
        
        # Set validator in handler registry
        self.handler_registry.set_validator(self.schema_validator)
        
        logger.info(f"Successfully registered {handler_count} mathematical tools")
    
    async def start(self) -> None:
        """Start the MCP server."""
        logger.info(f"Starting MCP server on {self.config.host}:{self.config.port}")
        
        try:
            await self.initialize()
            self._is_running = True
            
            # Start the server
            server_task = asyncio.create_task(
                self.app.run(host=self.config.host, port=self.config.port)
            )
            
            # Wait for shutdown signal
            await self._shutdown_event.wait()
            
            logger.info("Shutting down MCP server...")
            self._is_running = False
            
            # Cancel server task
            server_task.cancel()
            
            try:
                await server_task
            except asyncio.CancelledError:
                pass
            
        except Exception as e:
            logger.error(f"Error starting MCP server: {e}")
            raise
    
    async def stop(self) -> None:
        """Stop the MCP server."""
        logger.info("Stopping MCP server...")
        self._shutdown_event.set()
    
    @property
    def is_running(self) -> bool:
        """Check if server is running."""
        return self._is_running
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check and return server status."""
        return {
            "status": "healthy" if self._is_running else "stopped",
            "server_name": self.config.server_name,
            "server_version": self.config.server_version,
            "protocol_version": self.config.protocol_version,
            "enabled_tools": self.config.get_enabled_tools(),
            "total_tools": len(self.handler_registry.handlers) if hasattr(self.handler_registry, 'handlers') else 0,
            "performance_metrics": self.performance_monitor.get_performance_report(),
            "routing_stats": self.router.get_routing_statistics()
        }
    
    def get_tool_info(self) -> List[Dict[str, Any]]:
        """Get information about registered tools."""
        return self.handler_registry.get_tool_info()


@asynccontextmanager
async def create_mcp_server(config: Optional[MCPConfig] = None):
    """Context manager for creating and managing MCP server."""
    server = MCPServer(config)
    
    try:
        yield server
    finally:
        if server.is_running:
            await server.stop()


async def main() -> None:
    """Main entry point for MCP server."""
    config = MCPConfig.from_env()
    
    logger.info("Starting Math Genius MCP Server...")
    
    try:
        async with create_mcp_server(config) as server:
            await server.start()
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt, shutting down...")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)
    
    logger.info("Math Genius MCP Server stopped")


if __name__ == "__main__":
    asyncio.run(main())
