"""Text embedding service for semantic search."""

import logging
from typing import List, Optional
import numpy as np
from sentence_transformers import SentenceTransformer

from ..config import config


logger = logging.getLogger(__name__)


class EmbeddingService:
    """Service for generating text embeddings using sentence transformers."""
    
    def __init__(self, model_name: Optional[str] = None):
        """Initialize the embedding service.
        
        Args:
            model_name: Name of the sentence transformer model to use.
                       Defaults to config.embedding_model.
        """
        self.model_name = model_name or config.embedding_model
        self._model: Optional[SentenceTransformer] = None
        self._embedding_dimension: Optional[int] = None
        
    def _load_model(self) -> None:
        """Load the sentence transformer model."""
        if self._model is None:
            logger.info(f"Loading embedding model: {self.model_name}")
            try:
                self._model = SentenceTransformer(self.model_name)
                # Get embedding dimension
                test_embedding = self._model.encode(["test"])
                self._embedding_dimension = test_embedding.shape[1]
                logger.info(f"Model loaded successfully. Embedding dimension: {self._embedding_dimension}")
            except Exception as e:
                logger.error(f"Failed to load embedding model {self.model_name}: {e}")
                raise
    
    @property
    def embedding_dimension(self) -> int:
        """Get the embedding dimension."""
        if self._embedding_dimension is None:
            self._load_model()
        return self._embedding_dimension
    
    def encode_text(self, text: str) -> np.ndarray:
        """Encode a single text string into an embedding vector.
        
        Args:
            text: Text to encode
            
        Returns:
            Embedding vector as numpy array
        """
        if self._model is None:
            self._load_model()
            
        try:
            # Clean and prepare text
            cleaned_text = self._clean_text(text)
            
            # Generate embedding
            embedding = self._model.encode([cleaned_text])
            return embedding[0]  # Return single embedding vector
            
        except Exception as e:
            logger.error(f"Failed to encode text: {e}")
            logger.debug(f"Failed text: {text[:100]}...")
            raise
    
    def encode_batch(self, texts: List[str]) -> np.ndarray:
        """Encode multiple texts into embedding vectors.
        
        Args:
            texts: List of texts to encode
            
        Returns:
            Array of embedding vectors
        """
        if self._model is None:
            self._load_model()
            
        try:
            # Clean and prepare texts
            cleaned_texts = [self._clean_text(text) for text in texts]
            
            # Generate embeddings in batch
            embeddings = self._model.encode(cleaned_texts)
            return embeddings
            
        except Exception as e:
            logger.error(f"Failed to encode batch of {len(texts)} texts: {e}")
            raise
    
    def compute_similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """Compute cosine similarity between two embeddings.
        
        Args:
            embedding1: First embedding vector
            embedding2: Second embedding vector
            
        Returns:
            Cosine similarity score (0-1, higher is more similar)
        """
        try:
            # Compute cosine similarity
            dot_product = np.dot(embedding1, embedding2)
            norm1 = np.linalg.norm(embedding1)
            norm2 = np.linalg.norm(embedding2)
            
            if norm1 == 0 or norm2 == 0:
                return 0.0
                
            similarity = dot_product / (norm1 * norm2)
            
            # Ensure similarity is in [0, 1] range
            # Cosine similarity is in [-1, 1], so we normalize to [0, 1]
            normalized_similarity = (similarity + 1) / 2
            
            return float(normalized_similarity)
            
        except Exception as e:
            logger.error(f"Failed to compute similarity: {e}")
            return 0.0
    
    def _clean_text(self, text: str) -> str:
        """Clean and prepare text for embedding generation.
        
        Args:
            text: Raw text to clean
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
            
        # Basic text cleaning
        cleaned = text.strip()
        
        # Remove excessive whitespace
        cleaned = " ".join(cleaned.split())
        
        # Truncate very long texts to avoid model limits
        max_length = 512  # Most sentence transformers have 512 token limit
        if len(cleaned) > max_length:
            cleaned = cleaned[:max_length].rsplit(' ', 1)[0]  # Don't cut words in half
            logger.debug(f"Truncated text to {len(cleaned)} characters")
        
        return cleaned
    
    def get_model_info(self) -> dict:
        """Get information about the loaded model.
        
        Returns:
            Dictionary with model information
        """
        if self._model is None:
            self._load_model()
            
        return {
            "model_name": self.model_name,
            "embedding_dimension": self.embedding_dimension,
            "max_sequence_length": getattr(self._model, 'max_seq_length', 'unknown'),
            "device": str(self._model.device) if hasattr(self._model, 'device') else 'unknown'
        }
