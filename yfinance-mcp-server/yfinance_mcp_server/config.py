"""Configuration module for yfinance MCP server."""

import os
from typing import Dict, Any

# Default configuration
DEFAULT_CONFIG = {
    "server": {
        "name": "yfinance-mcp-server",
        "version": "0.1.0",
        "description": "Comprehensive yfinance MCP server for stock analysis"
    },
    "yfinance": {
        "cache_dir": os.path.expanduser("~/.cache/yfinance-mcp"),
        "timeout": 30,
        "retry_attempts": 3,
        "retry_delay": 1.0
    },
    "cache": {
        "enabled": True,
        "ttl": 3600,  # 1 hour
        "max_size": 1000
    },
    "news": {
        "max_articles": 50,
        "days_back": 7
    },
    "indicators": {
        "default_period": 14,
        "default_window": 20
    }
}

def get_config() -> Dict[str, Any]:
    """Get configuration with environment variable overrides."""
    config = DEFAULT_CONFIG.copy()
    
    # Override with environment variables
    if os.getenv("YFINANCE_CACHE_DIR"):
        config["yfinance"]["cache_dir"] = os.getenv("YFINANCE_CACHE_DIR")
    
    if os.getenv("YFINANCE_TIMEOUT"):
        config["yfinance"]["timeout"] = int(os.getenv("YFINANCE_TIMEOUT"))
    
    if os.getenv("NEWS_MAX_ARTICLES"):
        config["news"]["max_articles"] = int(os.getenv("NEWS_MAX_ARTICLES"))
    
    return config
