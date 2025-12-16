# RAG Chatbot for Physical AI & Humanoid Robotics Textbook

This is a Retrieval-Augmented Generation (RAG) chatbot designed for the Physical AI & Humanoid Robotics textbook project. It enables students to ask questions about the textbook content and receive AI-generated responses based on the book's content.

## Features

- **Full-book queries**: Ask questions about the entire textbook content
- **Selected text queries**: Ask questions specifically about selected text passages
- **Source attribution**: Responses include references to the relevant chapters
- **FastAPI backend**: Built with FastAPI for high performance
- **Qdrant vector database**: For efficient similarity search
- **OpenAI integration**: For high-quality response generation
- **Neon Postgres**: For storing content and metadata

## Architecture

```
User Query
    ↓
FastAPI Server
    ↓
RAG Agent
    ├── Query Processing
    ├── Context Retrieval (Qdrant)
    └── Response Generation (OpenAI)
    ↓
Response with Sources
```

## API Endpoints

### POST `/rag/query`

Query the RAG system with a natural language question.

**Request Body:**
```json
{
  "query": "string",
  "selected_text_context": "string | null"
}
```

**Response:**
```json
{
  "answer": "string",
  "sources": [
    {
      "chapter_id": "string",
      "title": "string",
      "snippet": "string",
      "score": "number | null"
    }
  ],
  "query_time": "datetime",
  "mode": "full_book | selected_text"
}
```

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   Copy `.env.example` to `.env` and fill in your credentials:
   ```bash
   cp .env.example .env
   # Edit .env with your actual values
   ```

3. **Initialize services:**
   ```bash
   python init_db.py
   ```

4. **Run the server:**
   ```bash
   uvicorn main:app --reload
   ```

## Environment Variables

- `QDRANT_URL`: Your Qdrant instance URL
- `QDRANT_API_KEY`: Your Qdrant API key
- `QDRANT_COLLECTION_NAME`: Name of the collection to use (default: "textbook_embeddings")
- `OPENAI_API_KEY`: Your OpenAI API key
- `OPENAI_MODEL`: Model to use for responses (default: "gpt-3.5-turbo")
- `EMBEDDING_MODEL`: Model to use for embeddings (default: "text-embedding-ada-002")
- `NEON_HOST`: Neon Postgres host
- `NEON_DATABASE`: Database name
- `NEON_USERNAME`: Database username
- `NEON_PASSWORD`: Database password
- `NEON_PORT`: Database port (default: 5432)
- `HOST`: Host to run the server on (default: "0.0.0.0")
- `PORT`: Port to run the server on (default: 8000)

## Project Structure

```
rag_chatbot/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── init_db.py             # Database initialization script
├── agents/
│   └── rag_agent.py       # Main RAG agent implementation
├── api/                   # API routes (if needed)
├── models/
│   └── request_models.py  # Pydantic models for requests/responses
├── services/
│   ├── qdrant_service.py  # Qdrant vector database service
│   ├── openai_service.py  # OpenAI API service
│   └── neon_service.py    # Neon Postgres service
├── utils/
│   └── text_chunker.py    # Text chunking utilities
├── config/
│   └── settings.py        # Configuration management
└── data/
    ├── embeddings/        # Stored embeddings
    └── documents/         # Raw documents
```

## Usage

Once the server is running, you can make requests to the `/rag/query` endpoint:

```bash
curl -X POST "http://localhost:8000/rag/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Explain how ROS 2 nodes communicate with each other",
    "selected_text_context": null
  }'
```

For queries about selected text:

```bash
curl -X POST "http://localhost:8000/rag/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What does this mean?",
    "selected_text_context": "ROS 2 nodes communicate through topics, services, and actions..."
  }'
```

## Development

To run the application in development mode:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The application will automatically reload when you make changes to the code.

## Testing

TODO: Add testing framework and example tests