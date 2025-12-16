import asyncio
import asyncpg
from typing import Dict, Any, Optional, List
import logging
import os
from dotenv import load_dotenv
import json

load_dotenv()

logger = logging.getLogger(__name__)

class NeonService:
    """
    Service class for interacting with Neon Postgres database.
    Handles storage and retrieval of textbook content and metadata.
    """

    def __init__(self):
        self.host = os.getenv("NEON_HOST")
        self.database = os.getenv("NEON_DATABASE")
        self.username = os.getenv("NEON_USERNAME")
        self.password = os.getenv("NEON_PASSWORD")
        self.port = os.getenv("NEON_PORT", "5432")
        self.pool = None

    async def initialize_connection(self):
        """
        Initialize the connection pool to Neon Postgres.
        """
        try:
            self.pool = await asyncpg.create_pool(
                host=self.host,
                database=self.database,
                user=self.username,
                password=self.password,
                port=self.port,
                min_size=1,
                max_size=10,
                command_timeout=60
            )
            logger.info("Connected to Neon Postgres successfully")

            # Create tables if they don't exist
            await self._create_tables()
        except Exception as e:
            logger.error(f"Error connecting to Neon Postgres: {str(e)}")
            raise

    async def _create_tables(self):
        """
        Create necessary tables if they don't exist.
        """
        try:
            async with self.pool.acquire() as connection:
                # Create chapters table
                await connection.execute("""
                    CREATE TABLE IF NOT EXISTS chapters (
                        id UUID PRIMARY KEY,
                        title VARCHAR(255) NOT NULL,
                        content TEXT NOT NULL,
                        module_id UUID REFERENCES modules(id),
                        original_language VARCHAR(10) DEFAULT 'en'
                    )
                """)

                # Create users table
                await connection.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id UUID PRIMARY KEY,
                        email VARCHAR(255) UNIQUE NOT NULL,
                        username VARCHAR(255),
                        betterauth_id VARCHAR(255) UNIQUE NOT NULL,
                        background_info JSONB
                    )
                """)

                # Create personalizations table
                await connection.execute("""
                    CREATE TABLE IF NOT EXISTS personalizations (
                        id UUID PRIMARY KEY,
                        user_id UUID REFERENCES users(id),
                        chapter_id UUID REFERENCES chapters(id),
                        personalized_content TEXT NOT NULL,
                        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE (user_id, chapter_id)
                    )
                """)

                # Create textbook_content table for storing text chunks
                await connection.execute("""
                    CREATE TABLE IF NOT EXISTS textbook_content (
                        chunk_id UUID PRIMARY KEY,
                        chapter_id UUID REFERENCES chapters(id),
                        content TEXT NOT NULL,
                        embedding_id VARCHAR(255), -- Reference to Qdrant point ID
                        metadata JSONB,
                        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                    )
                """)

                logger.info("Database tables created/verified successfully")
        except Exception as e:
            logger.error(f"Error creating tables: {str(e)}")
            raise

    async def get_chunk_by_id(self, chunk_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a text chunk by its ID.

        Args:
            chunk_id: The ID of the chunk to retrieve

        Returns:
            Dictionary containing the chunk content and metadata, or None if not found
        """
        try:
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow(
                    "SELECT content, metadata, chapter_id FROM textbook_content WHERE chunk_id = $1",
                    chunk_id
                )

                if row:
                    return {
                        'content': row['content'],
                        'metadata': row['metadata'],
                        'chapter_id': row['chapter_id']
                    }
                return None
        except Exception as e:
            logger.error(f"Error retrieving chunk by ID: {str(e)}")
            raise

    async def get_chunks_by_chapter(self, chapter_id: str) -> List[Dict[str, Any]]:
        """
        Retrieve all chunks for a specific chapter.

        Args:
            chapter_id: The ID of the chapter

        Returns:
            List of chunk dictionaries
        """
        try:
            async with self.pool.acquire() as connection:
                rows = await connection.fetch(
                    "SELECT chunk_id, content, metadata FROM textbook_content WHERE chapter_id = $1",
                    chapter_id
                )

                chunks = []
                for row in rows:
                    chunks.append({
                        'chunk_id': row['chunk_id'],
                        'content': row['content'],
                        'metadata': row['metadata']
                    })

                return chunks
        except Exception as e:
            logger.error(f"Error retrieving chunks by chapter: {str(e)}")
            raise

    async def store_chunk(self, chunk_id: str, chapter_id: str, content: str, metadata: Dict[str, Any]) -> bool:
        """
        Store a text chunk in the database.

        Args:
            chunk_id: Unique identifier for the chunk
            chapter_id: ID of the chapter this chunk belongs to
            content: The text content
            metadata: Additional metadata as a dictionary

        Returns:
            True if successful, False otherwise
        """
        try:
            async with self.pool.acquire() as connection:
                await connection.execute(
                    """
                    INSERT INTO textbook_content (chunk_id, chapter_id, content, metadata)
                    VALUES ($1, $2, $3, $4)
                    ON CONFLICT (chunk_id)
                    DO UPDATE SET content = EXCLUDED.content, metadata = EXCLUDED.metadata
                    """,
                    chunk_id, chapter_id, content, json.dumps(metadata)
                )
                logger.debug(f"Stored chunk: {chunk_id}")
                return True
        except Exception as e:
            logger.error(f"Error storing chunk: {str(e)}")
            return False

    async def batch_store_chunks(self, chunks: List[Dict[str, Any]]) -> bool:
        """
        Store multiple chunks in batch.

        Args:
            chunks: List of dictionaries containing chunk data

        Returns:
            True if successful, False otherwise
        """
        try:
            async with self.pool.acquire() as connection:
                # Prepare data for batch insert
                chunk_ids = [chunk['chunk_id'] for chunk in chunks]
                chapter_ids = [chunk['chapter_id'] for chunk in chunks]
                contents = [chunk['content'] for chunk in chunks]
                metadatas = [json.dumps(chunk['metadata']) for chunk in chunks]

                # Use COPY for efficient batch insert
                await connection.copy_records_to_table(
                    'textbook_content',
                    records=list(zip(chunk_ids, chapter_ids, contents, metadatas)),
                    columns=['chunk_id', 'chapter_id', 'content', 'metadata']
                )

                logger.info(f"Batch stored {len(chunks)} chunks")
                return True
        except Exception as e:
            logger.error(f"Error in batch storing chunks: {str(e)}")
            return False

    async def get_chapter_by_id(self, chapter_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a chapter by its ID.

        Args:
            chapter_id: The ID of the chapter to retrieve

        Returns:
            Dictionary containing the chapter content and metadata, or None if not found
        """
        try:
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow(
                    "SELECT id, title, content, module_id, original_language FROM chapters WHERE id = $1",
                    chapter_id
                )

                if row:
                    return {
                        'id': row['id'],
                        'title': row['title'],
                        'content': row['content'],
                        'module_id': row['module_id'],
                        'original_language': row['original_language']
                    }
                return None
        except Exception as e:
            logger.error(f"Error retrieving chapter by ID: {str(e)}")
            raise

    async def get_all_chapters(self) -> List[Dict[str, Any]]:
        """
        Retrieve all chapters.

        Returns:
            List of chapter dictionaries
        """
        try:
            async with self.pool.acquire() as connection:
                rows = await connection.fetch(
                    "SELECT id, title, content, module_id, original_language FROM chapters"
                )

                chapters = []
                for row in rows:
                    chapters.append({
                        'id': row['id'],
                        'title': row['title'],
                        'content': row['content'],
                        'module_id': row['module_id'],
                        'original_language': row['original_language']
                    })

                return chapters
        except Exception as e:
            logger.error(f"Error retrieving all chapters: {str(e)}")
            raise

    async def close_connection(self):
        """
        Close the connection pool.
        """
        if self.pool:
            await self.pool.close()
            logger.info("Neon Postgres connection pool closed")