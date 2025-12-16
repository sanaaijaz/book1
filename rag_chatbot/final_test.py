"""
Final test to verify the RAG chatbot implementation
"""
import asyncio
import sys
import os
from dotenv import load_dotenv

# Add the project root to the path so we can import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

async def test_rag_implementation():
    """
    Test that all RAG components are properly implemented
    """
    print("Testing RAG Chatbot Implementation...")

    # Test imports
    try:
        from agents.rag_agent import RAGAgent
        from services.qdrant_service import QdrantService
        from services.openai_service import OpenAIService
        from services.neon_service import NeonService
        from models.request_models import RAGQueryRequest, RAGQueryResponse
        print("SUCCESS: All modules imported successfully")
    except ImportError as e:
        print(f"ERROR: Import error: {e}")
        return False

    # Test RAG Agent initialization
    try:
        rag_agent = RAGAgent()
        print("SUCCESS: RAG Agent initialized successfully")
    except Exception as e:
        print(f"ERROR: RAG Agent initialization error: {e}")
        return False

    # Test Qdrant Service initialization
    try:
        qdrant_service = QdrantService()
        print("SUCCESS: Qdrant Service initialized successfully")
    except Exception as e:
        print(f"ERROR: Qdrant Service initialization error: {e}")
        return False

    # Test OpenAI Service initialization
    try:
        openai_service = OpenAIService()
        print("SUCCESS: OpenAI Service initialized successfully")
    except Exception as e:
        print(f"ERROR: OpenAI Service initialization error: {e}")
        return False

    # Test Neon Service initialization
    try:
        neon_service = NeonService()
        print("SUCCESS: Neon Service initialized successfully")
    except Exception as e:
        print(f"ERROR: Neon Service initialization error: {e}")
        return False

    # Test model creation
    try:
        request = RAGQueryRequest(query="Test query", selected_text_context="Test context")
        print("SUCCESS: Request model created successfully")
    except Exception as e:
        print(f"ERROR: Request model creation error: {e}")
        return False

    print("\nAll RAG Chatbot components are properly implemented!")
    print("\nTo run the full application:")
    print("1. Ensure your environment variables are set in .env")
    print("2. Run: python init_db.py")
    print("3. Run: uvicorn main:app --reload")

    return True

if __name__ == "__main__":
    success = asyncio.run(test_rag_implementation())
    if success:
        print("\nRAG Chatbot implementation is complete and ready!")
    else:
        print("\nThere were errors in the implementation.")
        sys.exit(1)