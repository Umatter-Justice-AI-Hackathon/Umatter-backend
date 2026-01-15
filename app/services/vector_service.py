from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from pgvector.sqlalchemy import Vector


class VectorService:
    """Service for vector database operations using pgvector."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_embedding_table(
        self,
        table_name: str,
        vector_dimension: int = 1536  # OpenAI ada-002 dimension
    ):
        """Create a table with vector column for embeddings."""
        query = text(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id SERIAL PRIMARY KEY,
                content TEXT,
                embedding vector({vector_dimension}),
                metadata JSONB,
                created_at TIMESTAMP DEFAULT NOW()
            )
        """)
        await self.session.execute(query)
        await self.session.commit()

        # Create index for faster similarity search
        index_query = text(f"""
            CREATE INDEX IF NOT EXISTS {table_name}_embedding_idx
            ON {table_name}
            USING ivfflat (embedding vector_cosine_ops)
            WITH (lists = 100)
        """)
        await self.session.execute(index_query)
        await self.session.commit()

    async def insert_embedding(
        self,
        table_name: str,
        content: str,
        embedding: List[float],
        metadata: Optional[dict] = None
    ):
        """Insert content with its embedding."""
        query = text(f"""
            INSERT INTO {table_name} (content, embedding, metadata)
            VALUES (:content, :embedding, :metadata)
            RETURNING id
        """)
        result = await self.session.execute(
            query,
            {
                "content": content,
                "embedding": embedding,
                "metadata": metadata or {}
            }
        )
        await self.session.commit()
        return result.scalar_one()

    async def similarity_search(
        self,
        table_name: str,
        query_embedding: List[float],
        limit: int = 5,
        threshold: float = 0.7
    ) -> List[dict]:
        """Perform cosine similarity search."""
        query = text(f"""
            SELECT
                id,
                content,
                metadata,
                1 - (embedding <=> :query_embedding) as similarity
            FROM {table_name}
            WHERE 1 - (embedding <=> :query_embedding) > :threshold
            ORDER BY embedding <=> :query_embedding
            LIMIT :limit
        """)
        result = await self.session.execute(
            query,
            {
                "query_embedding": query_embedding,
                "threshold": threshold,
                "limit": limit
            }
        )

        return [
            {
                "id": row.id,
                "content": row.content,
                "metadata": row.metadata,
                "similarity": float(row.similarity)
            }
            for row in result.fetchall()
        ]
