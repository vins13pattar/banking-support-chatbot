"""Knowledge service for retrieving FAQ and policy documents."""

from sqlalchemy import select
from sqlmodel import Session

from src.database import engine
from src.models.knowledge_document import KnowledgeDocument


def search_knowledge_base(query: str, category: str | None = None) -> list[dict[str, str]]:
    """Search the knowledge base for relevant documents.
    
    In a real app, this would use vector search (e.g. pgvector or pinecone).
    For this prototype, we'll do a simple ILIKE search.
    """
    with Session(engine) as session:
        statement = select(KnowledgeDocument).where(KnowledgeDocument.active == True)
        
        if category:
            statement = statement.where(KnowledgeDocument.category == category)
            
        # Basic keyword search on title or content
        keywords = query.split()
        for kw in keywords:
            if len(kw) > 3:  # skip small words
                statement = statement.where(
                    (KnowledgeDocument.title.ilike(f"%{kw}%")) |
                    (KnowledgeDocument.content.ilike(f"%{kw}%"))
                )
                
        # If no keywords matched, or query was empty, return some top documents
        statement = statement.limit(5)
        
        results = session.exec(statement).all()
        
        # If still no results and we had keywords, do a broader search
        if not results and keywords:
            broad_stmt = select(KnowledgeDocument).where(KnowledgeDocument.active == True)
            if category:
                broad_stmt = broad_stmt.where(KnowledgeDocument.category == category)
            # Match any word
            for kw in keywords:
                if len(kw) > 3:
                     broad_stmt = broad_stmt.where(
                        (KnowledgeDocument.title.ilike(f"%{kw}%")) |
                        (KnowledgeDocument.content.ilike(f"%{kw}%"))
                    )
                     break # just need one match
            broad_stmt = broad_stmt.limit(3)
            results = session.exec(broad_stmt).all()

        return [
            {
                "title": doc.title,
                "category": doc.category,
                "content": doc.content,
            }
            for doc in results
        ]


def get_policy_document(title: str) -> dict[str, str] | None:
    """Get a specific policy document by exact or partial title."""
    with Session(engine) as session:
        statement = select(KnowledgeDocument).where(
            KnowledgeDocument.title.ilike(f"%{title}%"),
            KnowledgeDocument.active == True
        ).limit(1)
        
        doc = session.exec(statement).first()
        if doc:
            return {
                "title": doc.title,
                "category": doc.category,
                "content": doc.content,
            }
    return None
