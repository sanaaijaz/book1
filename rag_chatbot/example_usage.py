"""
Example usage of the RAG Chatbot
"""
import asyncio
import sys
import os
from dotenv import load_dotenv

# Add the project root to the path so we can import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

async def example_usage():
    """
    Example of how to use the RAG chatbot
    """
    print("RAG Chatbot Example Usage")
    print("=" * 40)

    # Import the RAG Agent
    from agents.rag_agent import RAGAgent
    from models.request_models import RAGQueryRequest

    # Initialize the RAG Agent
    rag_agent = RAGAgent()

    print("\nExample 1: Full-book query")
    print("-" * 25)
    query_request = RAGQueryRequest(
        query="Explain the concept of ROS 2 nodes and how they communicate",
        selected_text_context=None
    )

    # Note: This would require actual services to be configured
    # For demonstration purposes only
    print(f"Query: {query_request.query}")
    print("Mode: Full-book search")
    print("This would search the entire textbook for relevant information")

    print("\nExample 2: Selected text query")
    print("-" * 25)
    selected_text = "ROS 2 nodes communicate with each other through topics, services, and actions. Topics provide a publish-subscribe communication pattern where nodes can publish messages to topics and subscribe to receive messages from topics."

    query_request_2 = RAGQueryRequest(
        query="What does this mean?",
        selected_text_context=selected_text
    )

    print(f"Selected text: {query_request_2.selected_text_context}")
    print(f"Query: {query_request_2.query}")
    print("Mode: Selected text context")
    print("This would focus on the selected text with additional context from related content")

    print("\nExample 3: API request format")
    print("-" * 25)
    print("To use the API directly, send a POST request to /rag/query:")
    print()
    print("curl -X POST 'http://localhost:8000/rag/query' \\")
    print("  -H 'Content-Type: application/json' \\")
    print("  -d '{")
    print('    "query": "Explain how ROS 2 nodes communicate",')
    print('    "selected_text_context": null')
    print("  }'")

    print("\nThe RAG agent would:")
    print("1. Process the query and determine the mode (full-book vs selected text)")
    print("2. Retrieve relevant text chunks from the vector database (Qdrant)")
    print("3. Fetch full content from the document store (Neon Postgres)")
    print("4. Generate a response using OpenAI API with the context")
    print("5. Return the answer with source attribution")

if __name__ == "__main__":
    asyncio.run(example_usage())