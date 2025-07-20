"""Tests for search functionality."""

import pytest
import asyncio
from unittest.mock import Mock, patch

from intelligent_mcp_server.search.tool_indexer import ToolIndexer, ToolMetadata
from intelligent_mcp_server.search.embeddings import EmbeddingService
from intelligent_mcp_server.search.vector_search import VectorSearchEngine


class TestToolIndexer:
    """Test the tool indexer functionality."""
    
    def test_indexer_initialization(self):
        """Test that indexer initializes correctly."""
        indexer = ToolIndexer()
        assert indexer.tools == {}
        assert len(indexer._function_categories) > 0
    
    def test_function_categories_mapping(self):
        """Test that function categories are properly mapped."""
        indexer = ToolIndexer()
        categories = indexer._function_categories
        
        # Test some known mappings
        assert categories.get("add") == "arithmetic"
        assert categories.get("triangle_area") == "geometry"
        assert categories.get("sin") == "trigonometry"
        assert categories.get("matrix_multiply") == "linear_algebra"
    
    @patch('intelligent_mcp_server.search.tool_indexer.math_dispatcher')
    def test_index_all_tools(self, mock_dispatcher):
        """Test indexing all tools."""
        # Mock dispatcher
        mock_dispatcher.__all__ = ["add", "triangle_area"]
        
        # Mock functions
        mock_add = Mock()
        mock_add.__name__ = "add"
        mock_triangle = Mock() 
        mock_triangle.__name__ = "triangle_area"
        
        mock_dispatcher.add = mock_add
        mock_dispatcher.triangle_area = mock_triangle
        
        # Test indexing
        indexer = ToolIndexer()
        with patch('inspect.signature'), patch('inspect.getdoc'):
            result = indexer.index_all_tools()
        
        assert len(result) == 2
        assert "add" in result
        assert "triangle_area" in result


class TestEmbeddingService:
    """Test the embedding service."""
    
    @patch('intelligent_mcp_server.search.embeddings.SentenceTransformer')
    def test_embedding_service_initialization(self, mock_transformer):
        """Test embedding service initialization."""
        service = EmbeddingService()
        assert service.model_name == "all-MiniLM-L6-v2"  # Default model
        assert service._model is None  # Lazy loading
    
    @patch('intelligent_mcp_server.search.embeddings.SentenceTransformer')
    def test_encode_text(self, mock_transformer):
        """Test text encoding."""
        # Mock transformer
        mock_model = Mock()
        mock_model.encode.return_value = [[0.1, 0.2, 0.3]]
        mock_transformer.return_value = mock_model
        
        service = EmbeddingService()
        result = service.encode_text("test text")
        
        assert result.tolist() == [0.1, 0.2, 0.3]
        mock_model.encode.assert_called_once()
    
    def test_clean_text(self):
        """Test text cleaning functionality."""
        service = EmbeddingService()
        
        # Test basic cleaning
        cleaned = service._clean_text("  test  text  ")
        assert cleaned == "test text"
        
        # Test empty text
        cleaned = service._clean_text("")
        assert cleaned == ""
        
        # Test long text truncation
        long_text = "word " * 200  # Very long text
        cleaned = service._clean_text(long_text)
        assert len(cleaned) <= 512


class TestVectorSearchEngine:
    """Test the vector search engine."""
    
    @patch('intelligent_mcp_server.search.vector_search.chromadb')
    def test_search_engine_initialization(self, mock_chromadb):
        """Test search engine initialization."""
        engine = VectorSearchEngine()
        assert engine._client is None
        assert engine._collection is None
        assert not engine._is_indexed
    
    @pytest.mark.asyncio
    @patch('intelligent_mcp_server.search.vector_search.chromadb')
    async def test_initialize_chromadb(self, mock_chromadb):
        """Test ChromaDB initialization."""
        # Mock ChromaDB client and collection
        mock_client = Mock()
        mock_collection = Mock()
        mock_client.get_or_create_collection.return_value = mock_collection
        mock_chromadb.PersistentClient.return_value = mock_client
        
        engine = VectorSearchEngine()
        engine._initialize_chromadb()
        
        assert engine._client is not None
        assert engine._collection is not None
    
    def test_get_available_categories(self):
        """Test getting available categories."""
        engine = VectorSearchEngine()
        
        # Mock indexed tools
        engine._indexed_tools = {
            "add": ToolMetadata(
                name="add", primary_description="Add numbers", category="arithmetic",
                alternative_names=[], purpose="", use_cases=[], mathematical_context="",
                real_world_applications=[], parameters={}, basic_examples=[],
                practical_examples=[], keywords=[], common_phrases=[],
                error_scenarios=[], function_obj=None
            ),
            "sin": ToolMetadata(
                name="sin", primary_description="Sine function", category="trigonometry", 
                alternative_names=[], purpose="", use_cases=[], mathematical_context="",
                real_world_applications=[], parameters={}, basic_examples=[],
                practical_examples=[], keywords=[], common_phrases=[],
                error_scenarios=[], function_obj=None
            )
        }
        engine._is_indexed = True
        
        categories = engine.get_available_categories()
        assert "arithmetic" in categories
        assert "trigonometry" in categories
        assert len(categories) == 2


@pytest.mark.integration
class TestSearchIntegration:
    """Integration tests for search functionality."""
    
    @pytest.mark.asyncio
    async def test_search_workflow(self):
        """Test complete search workflow (requires actual dependencies)."""
        try:
            # This test requires actual mathgenius module
            import mathgenius.api.dispatcher
            
            # Create search engine
            engine = VectorSearchEngine()
            
            # Index tools (this will take some time in real scenario)
            # engine.index_tools()
            
            # For now, just test that the engine can be created
            assert engine is not None
            
        except ImportError:
            pytest.skip("mathgenius module not available for integration test")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
