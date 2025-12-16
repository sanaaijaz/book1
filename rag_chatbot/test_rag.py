"""
Simple test script to verify the RAG chatbot components are properly structured.
"""
import asyncio
import sys
import os
from dotenv import load_dotenv

# Add the project root to the path so we can import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

async def test_rag_components():
    """
    Test that all RAG components can be imported and initialized without errors.
    """
    print("Testing RAG Chatbot Components...")

    # Test imports
    try:
        from agents.rag_agent import RAGAgent
        from services.qdrant_service import QdrantService
        from services.openai_service import OpenAIService
        from services.neon_service import NeonService
        from models.request_models import RAGQueryRequest, RAGQueryResponse
        print("✅ All modules imported successfully")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

    # Test RAG Agent initialization
    try:
        rag_agent = RAGAgent()
        print("✅ RAG Agent initialized successfully")
    except Exception as e:
        print(f"❌ RAG Agent initialization error: {e}")
        return False

    # Test Qdrant Service initialization
    try:
        qdrant_service = QdrantService()
        print("✅ Qdrant Service initialized successfully")
    except Exception as e:
        print(f"❌ Qdrant Service initialization error: {e}")
        return False

    # Test OpenAI Service initialization
    try:
        openai_service = OpenAIService()
        print("✅ OpenAI Service initialized successfully")
    except Exception as e:
        print(f"❌ OpenAI Service initialization error: {e}")
        return False

    # Test Neon Service initialization
    try:
        neon_service = NeonService()
        print("✅ Neon Service initialized successfully")
    except Exception as e:
        print(f"❌ Neon Service initialization error: {e}")
        return False

    # Test model creation
    try:
        request = RAGQueryRequest(query="Test query", selected_text_context="Test context")
        print("✅ Request model created successfully")
    except Exception as e:
        print(f"❌ Request model creation error: {e}")
        return False

    print("\n🎉 All RAG Chatbot components are properly structured!")
    print("\nTo run the full application:")
    print("1. Ensure your environment variables are set in .env")
    print("2. Run: python init_db.py")
    print("3. Run: uvicorn main:app --reload")

    return True

if __name__ == "__main__":
    success = asyncio.run(test_rag_components())
    if not success:
        sys.exit(1)