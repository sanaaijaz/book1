"""
Initialization script for the RAG Chatbot.
Sets up the database tables and initializes services.
"""
import asyncio
import sys
import os
from dotenv import load_dotenv

# Add the project root to the path so we can import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.qdrant_service import QdrantService
from services.neon_service import NeonService

async def initialize_services():
    """
    Initialize all required services for the RAG chatbot.
    """
    print("Starting RAG Chatbot initialization...")

    # Load environment variables
    load_dotenv()
    print("Environment variables loaded")

    # Initialize Qdrant service
    print("Initializing Qdrant service...")
    qdrant_service = QdrantService()
    await qdrant_service.initialize_collection()
    print("Qdrant service initialized")

    # Initialize Neon service
    print("Initializing Neon Postgres service...")
    neon_service = NeonService()
    await neon_service.initialize_connection()
    print("Neon Postgres service initialized")

    print("All services initialized successfully!")
    print("RAG Chatbot is ready for use.")

    # Close connections
    await neon_service.close_connection()

if __name__ == "__main__":
    asyncio.run(initialize_services())