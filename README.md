## Document Management and RAG-based Q&A API

A FastAPI application for managing documents and answering questions using Retrieval-Augmented Generation (RAG).

## Setup Instructions

### Prerequisites
- Python 3.10 or higher
- PostgreSQL database

### Installation

1. Clone the repository
```bash
git clone https://github.com/pranavnamburi/auro-backend-assignment.git
cd auro-backend-assignment
```

2. Create a virtual environment
```bash
python -m venv venv
```

3. Activate the virtual environment
```bash
# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

4. Install the required packages
```bash
pip install -r requirements.txt
```

5. Create a `.env` file in the root directory with the following variables:
```
DATABASE_URL=postgresql://username:password@localhost/dbname
OPENAI_API_KEY=your_openai_api_key
```

6. Run the application
```bash
uvicorn app.main:app --reload
```

7. Access the API documentation at `http://localhost:8000/docs`

## Project Description

This project is a RESTful API that combines document management with question-answering capabilities using the RAG (Retrieval-Augmented Generation) architecture. It allows users to upload documents, which are then processed, chunked, and embedded. Users can then ask questions about these documents, and the system will retrieve relevant information and generate accurate answers.

### Features

- User management system
- Document uploading and management
- Automatic document processing and embedding
- Question answering based on document content
- Asynchronous background processing for document handling

### API Endpoints

#### User Endpoints
- `POST /users/`: Create a new user
- `GET /users/`: List all users
- `GET /users/{user_id}`: Get user details

#### Document Endpoints
- `POST /documents/`: Upload a new document
- `GET /documents/`: List all documents
- `GET /documents/{document_id}`: Get document details
- `DELETE /documents/{document_id}`: Delete a document
- `POST /documents/select`: Select specific documents for querying

#### Question-Answering Endpoints
- `POST /qa/`: Ask a question about uploaded documents

### Architecture

The application follows a modular architecture:

1. **API Layer**: FastAPI routes that handle HTTP requests
2. **Service Layer**: Business logic for document processing, embedding generation, and question answering
3. **Database Layer**: SQLAlchemy models and database interaction
4. **External Services**: Integration with OpenAI for embeddings and LLM capabilities

### Components

#### Document Processing Pipeline
Documents are processed through these steps:
1. Document is uploaded and stored in the database
2. Background task splits the document into chunks
3. Each chunk is embedded using OpenAI's embedding model
4. Chunk and embedding data are stored for later retrieval

#### Question Answering Pipeline
When a question is asked:
1. Question is embedded using the same embedding model
2. System retrieves the most relevant document chunks through similarity search
3. Retrieved chunks are used as context for the LLM to generate an answer
4. Answer is returned along with source information

### Technologies Used

- **FastAPI**: Web framework for building APIs
- **SQLAlchemy**: ORM for database interactions
- **LangChain**: Framework for LLM application development
- **OpenAI API**: For generating embeddings and answers
- **PostgreSQL**: Database for storing documents and metadata

### Configuration

Configuration options in `app/config.py`:
- `EMBEDDING_MODEL`: The OpenAI model used for embeddings (default: "text-embedding-3-small")
- `LLM_MODEL`: The OpenAI model used for answering questions (default: "gpt-3.5-turbo")
- `TOP_K_RETRIEVAL`: Number of chunks to retrieve for each question (default: 5)

