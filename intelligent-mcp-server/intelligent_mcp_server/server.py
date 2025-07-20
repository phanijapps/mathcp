"""Main MCP server implementation using FastMCP."""

import logging
import asyncio
from typing import Dict, Any, List, Optional
from dataclasses import asdict

from fastmcp import FastMCP
from pydantic import BaseModel, Field

from .config import config
from .search.vector_search import VectorSearchEngine, SearchResult
from .search.tool_indexer import ToolMetadata
from .execute.tool_executor import ToolExecutor, ExecutionResult


# Configure logging to stderr to avoid BrokenPipeError with MCP
import sys
logging.basicConfig(
    level=getattr(logging, config.log_level.upper()),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr  # Use stderr instead of stdout for MCP compatibility
)
logger = logging.getLogger(__name__)


# Pydantic models for MCP tool schemas
class SearchToolInput(BaseModel):
    """Input schema for search_tool."""
    query: str = Field(description="Natural language search query for mathematical tools")
    limit: Optional[int] = Field(
        default=None, 
        description=f"Maximum number of results (1-{config.search_limit_max})"
    )
    category: Optional[str] = Field(
        default=None,
        description="Filter results by category (arithmetic, geometry, calculus, etc.)"
    )


class ToolSearchResult(BaseModel):
    """Search result for a mathematical tool."""
    tool_name: str = Field(description="Name of the mathematical tool")
    description: str = Field(description="Brief description of what the tool does")
    category: str = Field(description="Mathematical category (arithmetic, geometry, etc.)")
    similarity_score: float = Field(description="Semantic similarity score (0.0-1.0)")
    parameters: Dict[str, Any] = Field(description="Tool parameters and their types")
    examples: List[str] = Field(description="Usage examples")
    mathematical_context: str = Field(description="Mathematical context and formulas")


class ExecuteToolInput(BaseModel):
    """Input schema for execute_tool."""
    tool_name: str = Field(description="Name of the mathematical tool to execute")
    parameters: Dict[str, Any] = Field(
        description="Parameters to pass to the tool"
    )


class ToolExecutionResult(BaseModel):
    """Result from tool execution."""
    success: bool = Field(description="Whether execution was successful")
    result: Any = Field(description="Computation result (if successful)")
    tool_name: str = Field(description="Name of the executed tool")
    execution_time: float = Field(description="Execution time in seconds")
    error_message: Optional[str] = Field(description="Error message (if failed)")
    metadata: Optional[Dict[str, Any]] = Field(description="Additional execution metadata")


class IntelligentMCPServer:
    """Intelligent MCP Server with search and execute capabilities."""
    
    def __init__(self):
        """Initialize the intelligent MCP server."""
        from contextlib import asynccontextmanager
        
        # Create lifespan context manager for startup/shutdown
        @asynccontextmanager
        async def lifespan(app):
            logger.info(f"Starting {config.server_name} v{config.server_version}")
            logger.info(f"Intelligent mode: {config.intelligent_mode}")
            logger.info(f"Legacy support: {config.legacy_support}")
            
            try:
                # Initialize components
                await self._initialize_search_engine()
                await self._initialize_tool_executor()
                logger.info("Server startup completed successfully")
                yield
            except Exception as e:
                logger.error(f"Server startup failed: {e}")
                raise
            finally:
                logger.info("Server shutdown")
        
        self.app = FastMCP(name=config.server_name, lifespan=lifespan)
        self.search_engine: Optional[VectorSearchEngine] = None
        self.tool_executor: Optional[ToolExecutor] = None
        self._setup_tools()
        
    def _setup_tools(self) -> None:
        """Setup MCP tools for search and execute functionality."""
        
        @self.app.tool(description="Search for mathematical tools using natural language queries")
        async def search_tool(query: str, limit: Optional[int] = None, category: Optional[str] = None) -> List[ToolSearchResult]:
            """Search for mathematical tools using semantic similarity.
            
            Args:
                query: Natural language description of what you want to calculate
                limit: Maximum number of results to return (default: 5, max: 20)
                category: Filter by mathematical category (optional)
                
            Returns:
                List of relevant mathematical tools with descriptions and usage info
            """
            logger.info(f"Search request: query='{query}', limit={limit}, category={category}")
            
            try:
                if self.search_engine is None:
                    await self._initialize_search_engine()
                
                # Validate and set limit
                if limit is None:
                    limit = config.search_limit_default
                limit = min(max(1, limit), config.search_limit_max)
                
                # Perform search
                search_results = self.search_engine.search(
                    query=query,
                    limit=limit,
                    category_filter=category
                )
                
                # Convert to response format
                response_results = []
                for result in search_results:
                    tool_result = ToolSearchResult(
                        tool_name=result.tool_name,
                        description=result.tool_metadata.primary_description,
                        category=result.tool_metadata.category,
                        similarity_score=result.similarity_score,
                        parameters=result.tool_metadata.parameters,
                        examples=result.tool_metadata.basic_examples[:3],  # Limit examples
                        mathematical_context=result.tool_metadata.mathematical_context
                    )
                    response_results.append(tool_result)
                
                logger.info(f"Search completed: found {len(response_results)} results")
                return response_results
                
            except Exception as e:
                logger.error(f"Search failed: {e}")
                raise Exception(f"Search failed: {str(e)}")
        
        @self.app.tool(description="Execute a mathematical tool with specified parameters")
        async def execute_tool(tool_name: str, parameters: Dict[str, Any]) -> ToolExecutionResult:
            """Execute a mathematical tool with given parameters.
            
            Args:
                tool_name: Name of the mathematical tool (from search results)
                parameters: Dictionary of parameter names and values
                
            Returns:
                Execution result with computed value or error information
            """
            logger.info(f"Execute request: tool='{tool_name}', params={parameters}")
            
            try:
                if self.tool_executor is None:
                    await self._initialize_tool_executor()
                
                # Execute the tool
                execution_result = await self.tool_executor.execute_tool(
                    tool_name=tool_name,
                    parameters=parameters
                )
                
                # Convert to response format
                response = ToolExecutionResult(
                    success=execution_result.success,
                    result=execution_result.result,
                    tool_name=execution_result.tool_name,
                    execution_time=execution_result.execution_time,
                    error_message=execution_result.error_message,
                    metadata=execution_result.metadata
                )
                
                if execution_result.success:
                    logger.info(f"Execution successful: {tool_name} -> {execution_result.result}")
                else:
                    logger.warning(f"Execution failed: {tool_name} -> {execution_result.error_message}")
                
                return response
                
            except Exception as e:
                logger.error(f"Execute failed: {e}")
                raise Exception(f"Execute failed: {str(e)}")
        
        # Add server info tool
        @self.app.tool(description="Get information about the intelligent MCP server")
        async def server_info() -> Dict[str, Any]:
            """Get information about the server configuration and capabilities.
            
            Returns:
                Server information including available categories and statistics
            """
            try:
                if self.search_engine is None:
                    await self._initialize_search_engine()
                if self.tool_executor is None:
                    await self._initialize_tool_executor()
                
                # Get index statistics
                index_stats = self.search_engine.get_index_stats()
                available_categories = self.search_engine.get_available_categories()
                
                info = {
                    "server_name": config.server_name,
                    "server_version": config.server_version,
                    "intelligent_mode": config.intelligent_mode,
                    "total_tools": self.tool_executor.get_tool_count(),
                    "available_categories": available_categories,
                    "search_engine_stats": index_stats,
                    "configuration": {
                        "embedding_model": config.embedding_model,
                        "search_limit_default": config.search_limit_default,
                        "search_limit_max": config.search_limit_max,
                        "execution_timeout": config.execution_timeout
                    }
                }
                
                return info
                
            except Exception as e:
                logger.error(f"Server info failed: {e}")
                raise Exception(f"Server info failed: {str(e)}")
    
    async def _initialize_search_engine(self) -> None:
        """Initialize the search engine with indexing."""
        if self.search_engine is None:
            logger.info("Initializing search engine...")
            self.search_engine = VectorSearchEngine()
            
            if config.search_index_startup:
                logger.info("Building search index at startup...")
                await asyncio.get_event_loop().run_in_executor(
                    None, self.search_engine.index_tools
                )
                logger.info("Search index ready")
    
    async def _initialize_tool_executor(self) -> None:
        """Initialize the tool executor."""
        if self.tool_executor is None:
            logger.info("Initializing tool executor...")
            self.tool_executor = ToolExecutor()
            logger.info(f"Tool executor ready with {self.tool_executor.get_tool_count()} tools")
    
    async def startup(self) -> None:
        """Server startup initialization."""
        logger.info(f"Starting {config.server_name} v{config.server_version}")
        logger.info(f"Intelligent mode: {config.intelligent_mode}")
        logger.info(f"Legacy support: {config.legacy_support}")
        
        try:
            # Initialize components
            await self._initialize_search_engine()
            await self._initialize_tool_executor()
            
            logger.info("Server startup completed successfully")
            
        except Exception as e:
            logger.error(f"Server startup failed: {e}")
            raise
    
    def run(self, transport: str = "stdio") -> None:
        """Run the MCP server.
        
        Args:
            transport: Transport method ("stdio" or specify port for TCP)
        """
        logger.info(f"Running server with transport: {transport}")
        
        # Run the server
        if transport == "stdio":
            self.app.run()
        else:
            # Assume TCP transport with port
            try:
                port = int(transport)
                self.app.run_tcp(port=port)
            except ValueError:
                logger.error(f"Invalid transport: {transport}")
                raise ValueError(f"Invalid transport specification: {transport}")


def main() -> None:
    """Main entry point for the intelligent MCP server."""
    try:
        server = IntelligentMCPServer()
        server.run()
    except KeyboardInterrupt:
        logger.info("Server shutdown requested")
    except Exception as e:
        logger.error(f"Server failed: {e}")
        raise


# Create server instance for import
server = IntelligentMCPServer()
app = server.app

if __name__ == "__main__":
    main()
