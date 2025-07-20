"""Configuration management for MCP server."""

import logging
import os
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class MCPConfig(BaseModel):
    """Configuration for MCP server."""
    
    # Server Configuration
    host: str = Field(default="localhost", description="Server host address")
    port: int = Field(default=8000, description="Server port")
    debug: bool = Field(default=False, description="Enable debug mode")
    
    # MCP Protocol Configuration
    protocol_version: str = Field(default="1.0", description="MCP protocol version")
    server_name: str = Field(default="mgenius-mcp", description="MCP server name")
    server_version: str = Field(default="0.1.0", description="MCP server version")
    
    # Mathematical Computation Configuration
    max_computation_time: int = Field(default=30, description="Maximum computation time in seconds")
    precision: int = Field(default=15, description="Default precision for floating point operations")
    
    # Tool Configuration
    enable_arithmetic: bool = Field(default=True, description="Enable arithmetic tools")
    enable_algebra: bool = Field(default=True, description="Enable algebra tools")
    enable_geometry: bool = Field(default=True, description="Enable geometry tools")
    enable_trigonometry: bool = Field(default=True, description="Enable trigonometry tools")
    enable_calculus: bool = Field(default=True, description="Enable calculus tools")
    enable_linear_algebra: bool = Field(default=True, description="Enable linear algebra tools")
    enable_statistics: bool = Field(default=True, description="Enable statistics tools")
    enable_symbolic: bool = Field(default=True, description="Enable symbolic mathematics tools")
    
    # Logging Configuration
    log_level: str = Field(default="INFO", description="Logging level")
    log_format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Log format string"
    )
    
    # Performance Configuration
    max_concurrent_requests: int = Field(default=100, description="Maximum concurrent requests")
    request_timeout: int = Field(default=60, description="Request timeout in seconds")
    
    @classmethod
    def from_env(cls) -> "MCPConfig":
        """Create configuration from environment variables."""
        config_dict = {}
        
        # Server Configuration
        if host := os.getenv("MCP_HOST"):
            config_dict["host"] = host
        if port := os.getenv("MCP_PORT"):
            config_dict["port"] = int(port)
        if debug := os.getenv("MCP_DEBUG"):
            config_dict["debug"] = debug.lower() in ("true", "1", "yes", "on")
        
        # Protocol Configuration
        if protocol_version := os.getenv("MCP_PROTOCOL_VERSION"):
            config_dict["protocol_version"] = protocol_version
        if server_name := os.getenv("MCP_SERVER_NAME"):
            config_dict["server_name"] = server_name
        if server_version := os.getenv("MCP_SERVER_VERSION"):
            config_dict["server_version"] = server_version
        
        # Mathematical Configuration
        if max_computation_time := os.getenv("MCP_MAX_COMPUTATION_TIME"):
            config_dict["max_computation_time"] = int(max_computation_time)
        if precision := os.getenv("MCP_PRECISION"):
            config_dict["precision"] = int(precision)
        
        # Tool Configuration
        tool_flags = [
            "enable_arithmetic", "enable_algebra", "enable_geometry",
            "enable_trigonometry", "enable_calculus", "enable_linear_algebra",
            "enable_statistics", "enable_symbolic"
        ]
        for flag in tool_flags:
            env_var = f"MCP_{flag.upper()}"
            if value := os.getenv(env_var):
                config_dict[flag] = value.lower() in ("true", "1", "yes", "on")
        
        # Logging Configuration
        if log_level := os.getenv("MCP_LOG_LEVEL"):
            config_dict["log_level"] = log_level.upper()
        if log_format := os.getenv("MCP_LOG_FORMAT"):
            config_dict["log_format"] = log_format
        
        # Performance Configuration
        if max_concurrent_requests := os.getenv("MCP_MAX_CONCURRENT_REQUESTS"):
            config_dict["max_concurrent_requests"] = int(max_concurrent_requests)
        if request_timeout := os.getenv("MCP_REQUEST_TIMEOUT"):
            config_dict["request_timeout"] = int(request_timeout)
        
        return cls(**config_dict)
    
    def setup_logging(self) -> None:
        """Setup logging configuration."""
        logging.basicConfig(
            level=getattr(logging, self.log_level),
            format=self.log_format,
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler("mcp-server.log")
            ]
        )
    
    def get_enabled_tools(self) -> Dict[str, bool]:
        """Get dictionary of enabled tool categories."""
        return {
            "arithmetic": self.enable_arithmetic,
            "algebra": self.enable_algebra,
            "geometry": self.enable_geometry,
            "trigonometry": self.enable_trigonometry,
            "calculus": self.enable_calculus,
            "linear_algebra": self.enable_linear_algebra,
            "statistics": self.enable_statistics,
            "symbolic": self.enable_symbolic
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return self.model_dump()
    
    def __str__(self) -> str:
        """String representation of configuration."""
        return f"MCPConfig(host={self.host}, port={self.port}, debug={self.debug})"
