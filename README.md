# UMatter Backend

FastAPI backend with PostgreSQL and pgvector for vector database operations.

## Tech Stack

- **Framework**: FastAPI
- **ORM**: SQLModel (SQLAlchemy + Pydantic)
- **Database**: PostgreSQL with pgvector extension
- **Authentication**: JWT with passlib & python-jose
- **Deployment**: Render

## Project Structure

```
app/
├── api/              # API routes
├── core/             # Core functionality (security, logging)
├── db/               # Database session & initialization
├── models/           # SQLModel database models
├── schemas/          # Pydantic schemas (API contracts)
├── services/         # Business logic
└── main.py           # FastAPI app
```

## Setup

### 1. Clone and Setup Virtual Environment

```bash
python -m venv .
source bin/activate  # On Windows: .\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env with your database credentials
```

### 4. Setup PostgreSQL with pgvector

```bash
# Install PostgreSQL and pgvector extension
# macOS (Homebrew):
brew install postgresql pgvector

# Start PostgreSQL
brew services start postgresql

# Create database
createdb umatter_db
```

### 5. Initialize Database

```bash
# Run migrations (after setting up Alembic)
alembic upgrade head

# Or let the app create tables on startup
```

### 6. Run Development Server

```bash
uvicorn app.main:app --reload --port 8000
```

Visit:
- API Docs: http://localhost:8000/api/v1/docs
- Health Check: http://localhost:8000/api/v1/health

## Database Migrations with Alembic

```bash
# Initialize Alembic (already done)
alembic init migrations

# Create a new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

## Vector Database Usage

The project includes pgvector for similarity search. Example usage:

```python
from app.services.vector_service import VectorService

# Create embeddings table
await vector_service.create_embedding_table("documents", vector_dimension=1536)

# Insert embedding
await vector_service.insert_embedding(
    "documents",
    content="Your text content",
    embedding=[0.1, 0.2, ...],  # Your embedding vector
    metadata={"source": "doc1"}
)

# Search similar items
results = await vector_service.similarity_search(
    "documents",
    query_embedding=[0.1, 0.2, ...],
    limit=5
)
```

## Deploy to Render

1. Push code to GitHub
2. Connect repository to Render
3. Render will use `render.yaml` for configuration
4. Environment variables will be automatically set
5. Database will be provisioned with pgvector enabled

## API Development

### Add New Endpoint

1. Create model in `app/models/`
2. Create schema in `app/schemas/`
3. Create service in `app/services/`
4. Create router in `app/api/v1/`
5. Include router in `app/api/v1/router.py`

## Testing

```bash
pytest
pytest --cov=app tests/
```

## Code Quality

```bash
# Format code
black app/

# Lint
ruff app/

# Type checking
mypy app/
```
