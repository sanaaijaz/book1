"""
Simple test to verify the basic imports work
"""
import sys
import os

# Add the project root to the path so we can import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from models.request_models import RAGQueryRequest, RAGQueryResponse
    print("Request models imported successfully")
except Exception as e:
    print(f"Error importing request models: {e}")

try:
    from agents.rag_agent import RAGAgent
    print("RAG Agent imported successfully")
except Exception as e:
    print(f"Error importing RAG Agent: {e}")

try:
    from services.qdrant_service import QdrantService
    print("Qdrant Service imported successfully")
except Exception as e:
    print(f"Error importing Qdrant Service: {e}")

try:
    from services.openai_service import OpenAIService
    print("OpenAI Service imported successfully")
except Exception as e:
    print(f"Error importing OpenAI Service: {e}")

try:
    from services.neon_service import NeonService
    print("Neon Service imported successfully")
except Exception as e:
    print(f"Error importing Neon Service: {e}")

print("All imports completed!")