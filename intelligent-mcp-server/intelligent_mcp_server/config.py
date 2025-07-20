"""Configuration management for Intelligent MCP Server."""

import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class ServerConfig(BaseSettings):
    """Configuration settings for the intelligent MCP server."""
    
    # Server settings
    server_name: str = Field(
        default="intelligent-math-genius",
        description="Name of the MCP server"
    )
    
    server_version: str = Field(
        default="1.0.0",
        description="Version of the MCP server"
    ) 
    
    # Intelligent mode settings
    intelligent_mode: bool = Field(
        default=True,
        description="Enable intelligent interface (search + execute tools only)"
    )
    
    legacy_support: bool = Field(
        default=False,
        description="Enable legacy mode with individual tool registration"
    )
    
    # Search engine settings
    search_index_startup: bool = Field(
        default=True,
        description="Build search index at server startup"
    )
    
    embedding_model: str = Field(
        default="all-MiniLM-L6-v2",
        description="Sentence transformer model for embeddings"
    )
    
    search_limit_default: int = Field(
        default=5,
        description="Default number of search results to return"
    )
    
    search_limit_max: int = Field(
        default=20,
        description="Maximum number of search results allowed"
    )
    
    # Vector database settings
    vector_db_path: str = Field(
        default=os.path.expanduser("~/.cache/intelligent-mcp-server/vector_db"),
        description="Path to ChromaDB storage directory"
    )
    
    vector_collection_name: str = Field(
        default="math_tools",
        description="Name of the ChromaDB collection"
    )
    
    # Execution settings
    execution_timeout: float = Field(
        default=30.0,
        description="Timeout for tool execution in seconds"
    )
    
    # Performance monitoring
    performance_monitoring: bool = Field(
        default=True,
        description="Enable performance monitoring and analytics"
    )
    
    # Logging
    log_level: str = Field(
        default="INFO",
        description="Logging level (DEBUG, INFO, WARNING, ERROR)"
    )
    
    log_execution_requests: bool = Field(
        default=True,
        description="Log tool execution requests and results"
    )
    
    model_config = {
        "env_prefix": "MCP_",
        "case_sensitive": False
    }
        

def get_config() -> ServerConfig:
    """Get server configuration with environment variable overrides."""
    return ServerConfig()


# Global config instance
config = get_config()
