#!/usr/bin/env python3
"""Initialize the vector database for the intelligent MCP server."""

import asyncio
import logging
import sys
import os

# Add the current directory to Python path to import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from math_mcp_server.search.vector_search import VectorSearchEngine
from math_mcp_server.config import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def initialize_vector_database():
    """Initialize the vector database with all mathematical tools."""
    logger.info("Starting vector database initialization...")
    
    try:
        # Create vector search engine
        search_engine = VectorSearchEngine()
        
        # Initialize and index all tools
        logger.info("Indexing mathematical tools...")
        await asyncio.get_event_loop().run_in_executor(
            None, search_engine.index_tools, True  # force_reindex=True
        )
        
        # Get statistics
        stats = search_engine.get_index_stats()
        logger.info("Vector database initialization completed!")
        logger.info(f"Statistics: {stats}")
        
        # Test search functionality
        logger.info("Testing search functionality...")
        test_results = search_engine.search("solve quadratic equation", limit=3)
        logger.info(f"Test search found {len(test_results)} results")
        
        for i, result in enumerate(test_results, 1):
            logger.info(f"  {i}. {result.tool_name} (similarity: {result.similarity_score:.3f})")
        
        return True
        
    except Exception as e:
        logger.error(f"Vector database initialization failed: {e}")
        return False


def main():
    """Main entry point."""
    logger.info(f"Initializing vector database at: {config.vector_db_path}")
    logger.info(f"Collection name: {config.vector_collection_name}")
    logger.info(f"Embedding model: {config.embedding_model}")
    
    # Run initialization
    success = asyncio.run(initialize_vector_database())
    
    if success:
        logger.info("✅ Vector database initialization successful!")
        logger.info("The intelligent MCP server is ready to use.")
    else:
        logger.error("❌ Vector database initialization failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
