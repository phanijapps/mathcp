"""Vector search engine using ChromaDB for semantic similarity search."""

import logging
import os
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
import chromadb
from chromadb.config import Settings

from .embeddings import EmbeddingService
from .tool_indexer import ToolIndexer, ToolMetadata
from ..config import config


logger = logging.getLogger(__name__)


@dataclass
class SearchResult:
    """Result from a vector search query."""
    
    tool_name: str
    tool_metadata: ToolMetadata
    similarity_score: float
    distance: float
    rank: int


class VectorSearchEngine:
    """Vector search engine for mathematical tools using ChromaDB."""
    
    def __init__(self, embedding_service: Optional[EmbeddingService] = None):
        """Initialize the vector search engine.
        
        Args:
            embedding_service: Service for generating embeddings. 
                             Creates new instance if None.
        """
        self.embedding_service = embedding_service or EmbeddingService()
        self.tool_indexer = ToolIndexer()
        
        # ChromaDB client and collection
        self._client: Optional[chromadb.Client] = None
        self._collection: Optional[chromadb.Collection] = None
        
        # Indexed tools
        self._indexed_tools: Dict[str, ToolMetadata] = {}
        self._is_indexed = False
        
    def _initialize_chromadb(self) -> None:
        """Initialize ChromaDB client and collection."""
        try:
            # Ensure data directory exists
            os.makedirs(config.vector_db_path, exist_ok=True)
            
            # Initialize ChromaDB client with persistent storage
            self._client = chromadb.PersistentClient(
                path=config.vector_db_path,
                settings=Settings(
                    anonymized_telemetry=False,
                    allow_reset=True
                )
            )
            
            # Get or create collection
            self._collection = self._client.get_or_create_collection(
                name=config.vector_collection_name,
                metadata={"description": "Mathematical tool embeddings for semantic search"}
            )
            
            logger.info(f"ChromaDB initialized at {config.vector_db_path}")
            logger.info(f"Collection '{config.vector_collection_name}' ready")
            
        except Exception as e:
            logger.error(f"Failed to initialize ChromaDB: {e}")
            raise
    
    def index_tools(self, force_reindex: bool = False) -> None:
        """Index all mathematical tools for vector search.
        
        Args:
            force_reindex: If True, clear existing index and rebuild
        """
        if self._is_indexed and not force_reindex:
            logger.info("Tools already indexed, skipping indexing")
            return
            
        logger.info("Starting tool indexing for vector search...")
        
        try:
            # Initialize ChromaDB if needed
            if self._client is None:
                self._initialize_chromadb()
            
            # Clear existing collection if force reindex
            if force_reindex:
                logger.info("Force reindex requested, clearing existing collection")
                self._client.delete_collection(config.vector_collection_name)
                self._collection = self._client.create_collection(
                    name=config.vector_collection_name,
                    metadata={"description": "Mathematical tool embeddings for semantic search"}
                )
            
            # Check if collection already has data
            existing_count = self._collection.count()
            if existing_count > 0 and not force_reindex:
                logger.info(f"Collection already contains {existing_count} tools, loading existing index")
                self._load_existing_index()
                return
            
            # Index tools from mathgenius
            self._indexed_tools = self.tool_indexer.index_all_tools()
            
            # Prepare data for ChromaDB
            tool_names = list(self._indexed_tools.keys())
            searchable_texts = [
                self.tool_indexer.get_all_searchable_content(tool_name)
                for tool_name in tool_names
            ]
            
            # Generate embeddings
            logger.info(f"Generating embeddings for {len(tool_names)} tools...")
            embeddings = self.embedding_service.encode_batch(searchable_texts)
            
            # Prepare metadata for ChromaDB
            metadatas = []
            for tool_name in tool_names:
                metadata = self._indexed_tools[tool_name]
                chroma_metadata = {
                    "name": metadata.name,
                    "category": metadata.category,
                    "description": metadata.primary_description,
                    "purpose": metadata.purpose,
                    "mathematical_context": metadata.mathematical_context,
                    "keywords": ",".join(metadata.keywords[:10]),  # Limit for ChromaDB
                    "alternative_names": ",".join(metadata.alternative_names[:5])
                }
                metadatas.append(chroma_metadata)
            
            # Add to ChromaDB collection
            self._collection.add(
                embeddings=embeddings.tolist(),
                documents=searchable_texts,
                metadatas=metadatas,
                ids=tool_names
            )
            
            self._is_indexed = True
            logger.info(f"Successfully indexed {len(tool_names)} tools in vector database")
            
        except Exception as e:
            logger.error(f"Failed to index tools: {e}")
            raise
    
    def _load_existing_index(self) -> None:
        """Load existing tool index from ChromaDB."""
        try:
            # Get all items from collection
            results = self._collection.get(include=['metadatas'])
            
            if not results['ids']:
                logger.warning("Collection is empty, will need to reindex")
                return
            
            # Rebuild tool index
            self._indexed_tools = self.tool_indexer.index_all_tools()
            self._is_indexed = True
            
            logger.info(f"Loaded existing index with {len(results['ids'])} tools")
            
        except Exception as e:
            logger.error(f"Failed to load existing index: {e}")
            raise
    
    def search(
        self, 
        query: str, 
        limit: Optional[int] = None,
        category_filter: Optional[str] = None,
        min_similarity: float = 0.0
    ) -> List[SearchResult]:
        """Search for mathematical tools using semantic similarity.
        
        Args:
            query: Natural language search query
            limit: Maximum number of results to return
            category_filter: Filter results by tool category
            min_similarity: Minimum similarity score (0.0-1.0)
            
        Returns:
            List of search results ordered by similarity
        """
        if not self._is_indexed:
            logger.warning("Tools not indexed yet, indexing now...")
            self.index_tools()
        
        # Set default limit
        if limit is None:
            limit = config.search_limit_default
        limit = min(limit, config.search_limit_max)
        
        try:
            logger.debug(f"Searching for: '{query}' (limit={limit})")
            
            # Generate query embedding
            query_embedding = self.embedding_service.encode_text(query)
            
            # Prepare where filter for category
            where_filter = None
            if category_filter:
                where_filter = {"category": {"$eq": category_filter}}
            
            # Perform vector search
            results = self._collection.query(
                query_embeddings=[query_embedding.tolist()],
                n_results=limit * 2,  # Get more results to filter by similarity
                where=where_filter,
                include=['metadatas', 'distances', 'documents']
            )
            
            # Process results
            search_results = []
            
            if results['ids'] and results['ids'][0]:  # Check if we have results
                for i, (tool_id, distance, metadata) in enumerate(zip(
                    results['ids'][0],
                    results['distances'][0], 
                    results['metadatas'][0]
                )):
                    # Convert distance to similarity score
                    # ChromaDB uses L2 distance, convert to similarity (0-1)
                    similarity_score = max(0.0, 1.0 - (distance / 2.0))
                    
                    # Filter by minimum similarity
                    if similarity_score < min_similarity:
                        continue
                    
                    # Get full tool metadata
                    if tool_id in self._indexed_tools:
                        tool_metadata = self._indexed_tools[tool_id]
                        
                        search_result = SearchResult(
                            tool_name=tool_id,
                            tool_metadata=tool_metadata,
                            similarity_score=similarity_score,
                            distance=distance,
                            rank=i + 1
                        )
                        search_results.append(search_result)
                    
                    # Stop when we have enough results
                    if len(search_results) >= limit:
                        break
            
            logger.debug(f"Found {len(search_results)} results for query: '{query}'")
            return search_results
            
        except Exception as e:
            logger.error(f"Search failed for query '{query}': {e}")
            raise
    
    def search_by_category(self, category: str, limit: Optional[int] = None) -> List[SearchResult]:
        """Get all tools in a specific category.
        
        Args:
            category: Tool category to search for
            limit: Maximum number of results
            
        Returns:
            List of tools in the category
        """
        if not self._is_indexed:
            self.index_tools()
            
        limit = limit or config.search_limit_default
        
        try:
            # Query by category metadata
            results = self._collection.query(
                query_embeddings=[[0.0] * self.embedding_service.embedding_dimension],
                where={"category": {"$eq": category}},
                n_results=limit,
                include=['metadatas']
            )
            
            search_results = []
            if results['ids'] and results['ids'][0]:
                for i, tool_id in enumerate(results['ids'][0]):
                    if tool_id in self._indexed_tools:
                        tool_metadata = self._indexed_tools[tool_id]
                        
                        search_result = SearchResult(
                            tool_name=tool_id,
                            tool_metadata=tool_metadata,
                            similarity_score=1.0,  # Perfect match for category
                            distance=0.0,
                            rank=i + 1
                        )
                        search_results.append(search_result)
            
            return search_results
            
        except Exception as e:
            logger.error(f"Category search failed for '{category}': {e}")
            raise
    
    def get_tool_by_name(self, tool_name: str) -> Optional[ToolMetadata]:
        """Get tool metadata by exact name.
        
        Args:
            tool_name: Exact tool name
            
        Returns:
            Tool metadata if found, None otherwise
        """
        if not self._is_indexed:
            self.index_tools()
            
        return self._indexed_tools.get(tool_name)
    
    def get_available_categories(self) -> List[str]:
        """Get list of available tool categories.
        
        Returns:
            List of unique categories
        """
        if not self._is_indexed:
            self.index_tools()
            
        categories = set()
        for tool_metadata in self._indexed_tools.values():
            categories.add(tool_metadata.category)
            
        return sorted(list(categories))
    
    def get_index_stats(self) -> Dict[str, Any]:
        """Get statistics about the current index.
        
        Returns:
            Dictionary with index statistics
        """
        stats = {
            "is_indexed": self._is_indexed,
            "total_tools": len(self._indexed_tools),
            "categories": len(self.get_available_categories()) if self._is_indexed else 0,
            "chromadb_count": self._collection.count() if self._collection else 0,
            "embedding_model": self.embedding_service.model_name,
            "embedding_dimension": self.embedding_service.embedding_dimension if self._is_indexed else None
        }
        
        if self._is_indexed:
            # Category breakdown
            category_counts = {}
            for tool_metadata in self._indexed_tools.values():
                category = tool_metadata.category
                category_counts[category] = category_counts.get(category, 0) + 1
            stats["category_breakdown"] = category_counts
        
        return stats
    
    def reset_index(self) -> None:
        """Reset the entire search index."""
        try:
            if self._client and self._collection:
                self._client.delete_collection(config.vector_collection_name)
                logger.info("Search index reset successfully")
            
            self._collection = None
            self._indexed_tools = {}
            self._is_indexed = False
            
        except Exception as e:
            logger.error(f"Failed to reset index: {e}")
            raise
