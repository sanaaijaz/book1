import asyncio
import openai
from typing import List, Dict, Any
import logging
import os
from dotenv import load_dotenv
import tiktoken

load_dotenv()

logger = logging.getLogger(__name__)

class OpenAIService:
    """
    Service class for interacting with OpenAI API.
    Handles embedding generation and response generation.
    """

    def __init__(self):
        # Set OpenAI API key
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
        self.embedding_model = os.getenv("EMBEDDING_MODEL", "text-embedding-ada-002")
        self.max_tokens = int(os.getenv("MAX_TOKENS", 2048))
        self.temperature = float(os.getenv("TEMPERATURE", 0.7))

        # Initialize tokenizer for token counting
        self.tokenizer = tiktoken.encoding_for_model(self.model)

    async def get_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for the given text.

        Args:
            text: The text to generate embedding for

        Returns:
            List of floats representing the embedding
        """
        try:
            # Truncate text if too long (OpenAI has a limit)
            max_chars = 8192  # Conservative limit to avoid token issues
            if len(text) > max_chars:
                text = text[:max_chars]
                logger.warning(f"Text truncated to {max_chars} characters for embedding")

            response = await openai.embeddings.acreate(
                input=text,
                model=self.embedding_model
            )

            embedding = response.data[0].embedding
            logger.debug(f"Generated embedding with {len(embedding)} dimensions")
            return embedding

        except Exception as e:
            logger.error(f"Error generating embedding: {str(e)}")
            raise

    async def generate_response(self, query: str, context_chunks: List[Dict[str, Any]]) -> str:
        """
        Generate a response based on the query and context chunks.

        Args:
            query: The user's question
            context_chunks: List of context chunks with content and metadata

        Returns:
            Generated response string
        """
        try:
            # Combine context chunks into a single context string
            context_parts = []
            for chunk in context_chunks:
                content = chunk['content']
                # Limit the content to avoid token limits
                max_chunk_tokens = 300  # Approximate token count
                if len(content) > max_chunk_tokens * 4:  # Rough estimate: 1 token ~ 4 chars
                    content = content[:max_chunk_tokens * 4] + "..."
                context_parts.append(content)

            combined_context = "\n\n".join(context_parts)

            # Create the prompt for the LLM
            prompt = self._create_rag_prompt(query, combined_context)

            # Count tokens to ensure we're within limits
            token_count = len(self.tokenizer.encode(prompt))
            if token_count > self.max_tokens * 0.8:  # Use 80% of max tokens to be safe
                # Truncate context to fit
                available_tokens = int(self.max_tokens * 0.8) - len(self.tokenizer.encode(self._create_rag_prompt(query, "")))
                if available_tokens > 0:
                    combined_context = combined_context[:available_tokens * 3]  # Rough estimate
                    prompt = self._create_rag_prompt(query, combined_context)

            # Call OpenAI API
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an AI assistant for a Physical AI & Humanoid Robotics textbook. Answer questions based on the provided context. If the context doesn't contain enough information, say so."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens // 2  # Use half for response
            )

            answer = response.choices[0].message.content.strip()
            logger.debug(f"Generated response with {len(answer)} characters")
            return answer

        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            raise

    def _create_rag_prompt(self, query: str, context: str) -> str:
        """
        Create the prompt for RAG response generation.

        Args:
            query: The user's question
            context: The retrieved context

        Returns:
            Formatted prompt string
        """
        prompt = f"""
        Context information:
        {context}

        Question: {query}

        Please provide a detailed answer based on the context information. If the context doesn't contain sufficient information to answer the question, please state that clearly. Be concise but comprehensive in your response, and reference specific concepts from the context when possible.
        """
        return prompt.strip()

    async def batch_get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts in batch.

        Args:
            texts: List of texts to generate embeddings for

        Returns:
            List of embeddings (each embedding is a list of floats)
        """
        try:
            # Process in chunks to avoid API limits
            chunk_size = 20  # Conservative limit
            all_embeddings = []

            for i in range(0, len(texts), chunk_size):
                chunk = texts[i:i + chunk_size]

                # Truncate long texts
                truncated_chunk = []
                for text in chunk:
                    max_chars = 8192
                    if len(text) > max_chars:
                        text = text[:max_chars]
                    truncated_chunk.append(text)

                response = await openai.embeddings.acreate(
                    input=truncated_chunk,
                    model=self.embedding_model
                )

                chunk_embeddings = [item.embedding for item in response.data]
                all_embeddings.extend(chunk_embeddings)

            logger.debug(f"Generated {len(all_embeddings)} embeddings in batch")
            return all_embeddings

        except Exception as e:
            logger.error(f"Error in batch embedding generation: {str(e)}")
            raise

    async def validate_api_key(self) -> bool:
        """
        Validate the OpenAI API key by making a simple test call.

        Returns:
            True if API key is valid, False otherwise
        """
        try:
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[{"role": "user", "content": "Test"}],
                max_tokens=5
            )
            return True
        except Exception as e:
            logger.error(f"API key validation failed: {str(e)}")
            return False