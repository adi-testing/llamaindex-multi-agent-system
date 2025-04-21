import logging
from pathlib import Path
from typing import List, Dict, Any, Optional

from llama_index.core import (
    VectorStoreIndex,
    StorageContext,
    Document,
    load_index_from_storage
)
from llama_index.core.embeddings import BaseEmbedding
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.tools import QueryEngineTool
from llama_index.core.tools import ToolMetadata
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.settings import Settings

from config import KB_PERSIST_DIR, EMBEDDING_MODEL
from data.sample_documents import AI_DOCUMENTS

logger = logging.getLogger(__name__)

class KnowledgeBase:
    """Class to manage the vector knowledge base."""
    
    def __init__(self, persist_dir: Optional[Path] = None):
        """Initialize the knowledge base."""
        self.persist_dir = persist_dir or KB_PERSIST_DIR
        self.index = None
        self.embedding_model = self._get_embedding_model()
        Settings.embed_model = self.embedding_model
        
    def _get_embedding_model(self) -> BaseEmbedding:
        """Get the embedding model based on the configuration."""
        if EMBEDDING_MODEL.startswith("local:"):
            # Use a local embedding model
            model_name = EMBEDDING_MODEL.split("local:")[1]
            logger.info(f"Using local embedding model: {model_name}")
            return HuggingFaceEmbedding(model_name=model_name)
            """ elif EMBEDDING_MODEL.startswith("openai:"):
            logger.info(f"Using OpenAI embedding model: {EMBEDDING_MODEL}")
            return OpenAIEmbedding(model=EMBEDDING_MODEL) """
        else:
            raise ValueError(f"Unsupported embedding model: {EMBEDDING_MODEL}")
        
    def create_documents(self) -> List[Document]:
        """Create document objects from sample data."""
        documents = []
        for doc_info in AI_DOCUMENTS:
            doc = Document(
                text=doc_info["content"],
                metadata={"title": doc_info["title"]}
            )
            documents.append(doc)
        
        return documents
        
    def initialize(self, force_reload: bool = False) -> VectorStoreIndex:
        """Initialize or load the vector index."""
        if not force_reload and self.persist_dir.exists():
            try:
                logger.info(f"Loading existing index from {self.persist_dir}")
                # Load the index if it exists
                storage_context = StorageContext.from_defaults(
                    persist_dir=str(self.persist_dir)
                )
                self.index = load_index_from_storage(storage_context)
            except Exception as e:
                logger.warning(f"Failed to load index: {e}. Creating new index.")
                self._create_new_index()
        else:
            self._create_new_index()
            
        return self.index
    
    def _create_new_index(self):
        """Create a new vector index from documents."""
        logger.info("Creating new vector index")
        documents = self.create_documents()
        
        # Create a new storage context
        storage_context = StorageContext.from_defaults()
        
        # Build the index with the specified embedding model
        self.index = VectorStoreIndex.from_documents(
            documents=documents,
            storage_context=storage_context,
            embedding_model=self.embedding_model,  # Use the configured embedding model
        )
        
        # Persist the index
        self.index.storage_context.persist(persist_dir=str(self.persist_dir))
        logger.info(f"Index created and saved to {self.persist_dir}")
    
    def get_query_engine(self):
        """Get a query engine from the index."""
        if self.index is None:
            self.initialize()
        
        return self.index.as_query_engine()
    
    def get_query_engine_tool(self):
        """Create a QueryEngineTool from the knowledge base."""
        query_engine = self.get_query_engine()
        
        query_engine_tool = QueryEngineTool(
            query_engine=query_engine,
            metadata=ToolMetadata(
                name="ai_knowledge_base",
                description="Provides information about AI concepts and technologies. Use this when you need information about AI frameworks, techniques, or terminology."
            )
        )
        
        return query_engine_tool