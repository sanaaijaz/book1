import asyncio
from typing import Optional, List
from datetime import datetime
import logging

from models.request_models import RAGQueryRequest, RAGQueryResponse, Source
from services.qdrant_service import QdrantService
from services.openai_service import OpenAIService
from services.neon_service import NeonService

logger = logging.getLogger(__name__)

class RAGAgent:
    """
    RAG Agent that handles retrieval and generation for the textbook chatbot.
    Supports both full-book queries and selected text context queries.
    """

    def __init__(self):
        self.qdrant_service = QdrantService()
        self.openai_service = OpenAIService()
        self.neon_service = NeonService()

    async def query(self, query: str, selected_text_context: Optional[str] = None) -> RAGQueryResponse:
        """
        Process a query using RAG approach.

        Args:
            query: The user's question
            selected_text_context: Optional text that the user has selected for context

        Returns:
            RAGQueryResponse with the answer and sources
        """
        try:
            # Determine query mode
            if selected_text_context:
                mode = "selected_text"
                # Use selected text as primary context
                context_chunks = await self._get_context_for_selected_text(selected_text_context, query)
            else:
                mode = "full_book"
                # Retrieve relevant chunks from the entire book
                context_chunks = await self._retrieve_relevant_chunks(query)

            # Generate response using OpenAI
            answer = await self.openai_service.generate_response(query, context_chunks)

            # Create source information
            sources = await self._create_sources(context_chunks)

            return RAGQueryResponse(
                answer=answer,
                sources=sources,
                query_time=datetime.now(),
                mode=mode
            )

        except Exception as e:
            logger.error(f"Error in RAG query: {str(e)}")
            raise

    async def _retrieve_relevant_chunks(self, query: str, top_k: int = 5) -> List[dict]:
        """
        Retrieve relevant text chunks from the vector database based on the query.

        Args:
            query: The user's question
            top_k: Number of top results to retrieve

        Returns:
            List of relevant text chunks with metadata
        """
        try:
            # Generate embeddings for the query
            query_embedding = await self.openai_service.get_embedding(query)

            # Search in Qdrant
            search_results = await self.qdrant_service.search(
                query_embedding,
                top_k=top_k
            )

            # Retrieve full content from Neon Postgres
            chunks = []
            for result in search_results:
                chunk_content = await self.neon_service.get_chunk_by_id(result['chunk_id'])
                if chunk_content:
                    chunks.append({
                        'id': result['chunk_id'],
                        'content': chunk_content['content'],
                        'metadata': result.get('metadata', {}),
                        'score': result.get('score', 0.0)
                    })

            return chunks

        except Exception as e:
            logger.error(f"Error retrieving relevant chunks: {str(e)}")
            raise

    async def _get_context_for_selected_text(self, selected_text: str, query: str, top_k: int = 3) -> List[dict]:
        """
        Get context based on user-selected text and the query.

        Args:
            selected_text: The text the user has selected
            query: The user's question about the selected text
            top_k: Number of additional context chunks to retrieve

        Returns:
            List of context chunks (including the selected text and related content)
        """
        try:
            # Start with the selected text as primary context
            context_chunks = [{
                'id': 'selected_text',
                'content': selected_text,
                'metadata': {'type': 'selected_text'},
                'score': 1.0
            }]

            # Generate embeddings for the combined context
            combined_context = f"Selected text: {selected_text}\nQuestion: {query}"
            query_embedding = await self.openai_service.get_embedding(combined_context)

            # Search for related content in Qdrant
            search_results = await self.qdrant_service.search(
                query_embedding,
                top_k=top_k
            )

            # Retrieve full content from Neon Postgres
            for result in search_results:
                chunk_content = await self.neon_service.get_chunk_by_id(result['chunk_id'])
                if chunk_content:
                    context_chunks.append({
                        'id': result['chunk_id'],
                        'content': chunk_content['content'],
                        'metadata': result.get('metadata', {}),
                        'score': result.get('score', 0.0)
                    })

            return context_chunks

        except Exception as e:
            logger.error(f"Error getting context for selected text: {str(e)}")
            raise

    async def _create_sources(self, context_chunks: List[dict]) -> List[Source]:
        """
        Create source information from context chunks.

        Args:
            context_chunks: List of context chunks with metadata

        Returns:
            List of Source objects
        """
        sources = []
        for chunk in context_chunks:
            metadata = chunk.get('metadata', {})
            sources.append(Source(
                chapter_id=metadata.get('chapter_id', 'unknown'),
                title=metadata.get('chapter_title', 'Unknown Chapter'),
                snippet=chunk['content'][:200] + "..." if len(chunk['content']) > 200 else chunk['content'],
                score=chunk.get('score')
            ))
        return sources