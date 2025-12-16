import asyncio
from typing import List, Dict, Any, Optional
from qdrant_client import AsyncQdrantClient
from qdrant_client.http import models
import logging
import os
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class QdrantService:
    """
    Service class for interacting with Qdrant vector database.
    Handles embedding storage, retrieval, and similarity search.
    """

    def __init__(self):
        # Initialize Qdrant client
        self.client = AsyncQdrantClient(
            url=os.getenv("QDRANT_URL"),
            api_key=os.getenv("QDRANT_API_KEY"),
            prefer_grpc=True
        )
        self.collection_name = os.getenv("QDRANT_COLLECTION_NAME", "textbook_embeddings")
        self.vector_size = int(os.getenv("EMBEDDING_DIMENSION", 1536))  # Default for OpenAI embeddings

    async def initialize_collection(self):
        """
        Initialize the Qdrant collection with appropriate configuration.
        """
        try:
            # Check if collection exists
            collections = await self.client.get_collections()
            collection_exists = any(col.name == self.collection_name for col in collections.collections)

            if not collection_exists:
                # Create collection
                await self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=models.VectorParams(
                        size=self.vector_size,
                        distance=models.Distance.COSINE
                    ),
                    optimizers_config=models.OptimizersConfigDiff(
                        indexing_threshold=20000
                    )
                )
                logger.info(f"Created Qdrant collection: {self.collection_name}")
            else:
                logger.info(f"Qdrant collection {self.collection_name} already exists")
        except Exception as e:
            logger.error(f"Error initializing Qdrant collection: {str(e)}")
            raise

    async def store_embedding(self, chunk_id: str, embedding: List[float], metadata: Dict[str, Any]):
        """
        Store a text chunk embedding in Qdrant.

        Args:
            chunk_id: Unique identifier for the text chunk
            embedding: The embedding vector
            metadata: Metadata associated with the chunk
        """
        try:
            await self.client.upsert(
                collection_name=self.collection_name,
                points=[
                    models.PointStruct(
                        id=chunk_id,
                        vector=embedding,
                        payload={
                            "text_chunk_id": chunk_id,
                            "metadata": metadata
                        }
                    )
                ]
            )
            logger.debug(f"Stored embedding for chunk: {chunk_id}")
        except Exception as e:
            logger.error(f"Error storing embedding: {str(e)}")
            raise

    async def search(self, query_embedding: List[float], top_k: int = 5, filters: Optional[Dict] = None) -> List[Dict[str, Any]]:
        """
        Search for similar embeddings in the database.

        Args:
            query_embedding: The embedding to search for
            top_k: Number of top results to return
            filters: Optional filters to apply to the search

        Returns:
            List of search results with chunk_id, score, and metadata
        """
        try:
            # Prepare filters if provided
            search_filter = None
            if filters:
                must_conditions = []
                for key, value in filters.items():
                    must_conditions.append(
                        models.FieldCondition(
                            key=f"metadata.{key}",
                            match=models.MatchValue(value=value)
                        )
                    )
                if must_conditions:
                    search_filter = models.Filter(must=must_conditions)

            # Perform search
            search_results = await self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=top_k,
                query_filter=search_filter,
                with_payload=True
            )

            # Format results
            results = []
            for result in search_results:
                results.append({
                    'chunk_id': result.payload.get('text_chunk_id'),
                    'score': result.score,
                    'metadata': result.payload.get('metadata', {})
                })

            logger.debug(f"Search returned {len(results)} results")
            return results

        except Exception as e:
            logger.error(f"Error searching embeddings: {str(e)}")
            raise

    async def batch_store_embeddings(self, chunks: List[Dict[str, Any]]):
        """
        Store multiple embeddings in batch for efficiency.

        Args:
            chunks: List of dictionaries containing chunk_id, embedding, and metadata
        """
        try:
            points = []
            for chunk in chunks:
                points.append(
                    models.PointStruct(
                        id=chunk['chunk_id'],
                        vector=chunk['embedding'],
                        payload={
                            "text_chunk_id": chunk['chunk_id'],
                            "metadata": chunk['metadata']
                        }
                    )
                )

            await self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            logger.info(f"Batch stored {len(chunks)} embeddings")
        except Exception as e:
            logger.error(f"Error in batch storing embeddings: {str(e)}")
            raise

    async def delete_embedding(self, chunk_id: str):
        """
        Delete an embedding from the database.

        Args:
            chunk_id: The ID of the chunk to delete
        """
        try:
            await self.client.delete(
                collection_name=self.collection_name,
                points_selector=models.PointIdsList(
                    points=[chunk_id]
                )
            )
            logger.debug(f"Deleted embedding for chunk: {chunk_id}")
        except Exception as e:
            logger.error(f"Error deleting embedding: {str(e)}")
            raise

    async def get_embedding_by_id(self, chunk_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve an embedding by its ID.

        Args:
            chunk_id: The ID of the chunk to retrieve

        Returns:
            Dictionary containing the embedding and metadata, or None if not found
        """
        try:
            records = await self.client.retrieve(
                collection_name=self.collection_name,
                ids=[chunk_id],
                with_vectors=True
            )

            if records and len(records) > 0:
                record = records[0]
                return {
                    'id': record.id,
                    'vector': record.vector,
                    'payload': record.payload
                }
            return None

        except Exception as e:
            logger.error(f"Error retrieving embedding by ID: {str(e)}")
            raise