"""Knowledge service for retrieving FAQ and policy documents."""

from sqlalchemy import select, or_
from sqlmodel import Session

from src.database import engine
from src.models.knowledge_document import KnowledgeDocument

# Common stop words to skip during keyword search
_STOP_WORDS = frozenset({
    "a", "an", "the", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "shall",
    "should", "may", "might", "must", "can", "could", "to", "of", "in",
    "for", "on", "with", "at", "by", "from", "as", "into", "about",
    "like", "through", "after", "before", "between", "out", "above",
    "below", "up", "down", "and", "but", "or", "not", "no", "nor",
    "so", "yet", "both", "each", "few", "more", "most", "other", "some",
    "such", "than", "too", "very", "just", "also", "how", "what", "when",
    "where", "which", "who", "whom", "why", "this", "that", "these",
    "those", "i", "me", "my", "we", "our", "you", "your", "he", "him",
    "his", "she", "her", "it", "its", "they", "them", "their",
})


def search_knowledge_base(query: str, category: str | None = None) -> list[dict[str, str]]:
    """Search the knowledge base for relevant documents.
    
    In a real app, this would use vector search (e.g. pgvector or pinecone).
    For this prototype, we do a simple ILIKE search with OR logic.
    """
    with Session(engine) as session:
        statement = select(KnowledgeDocument).where(KnowledgeDocument.active == True)
        
        if category:
            statement = statement.where(KnowledgeDocument.category == category)
            
        # Extract meaningful keywords (skip short words and stop words)
        keywords = [
            kw for kw in query.lower().split()
            if len(kw) > 2 and kw not in _STOP_WORDS
        ]
        
        if keywords:
            # Use OR logic: match any keyword in title or content
            keyword_conditions = []
            for kw in keywords:
                keyword_conditions.append(KnowledgeDocument.title.ilike(f"%{kw}%"))
                keyword_conditions.append(KnowledgeDocument.content.ilike(f"%{kw}%"))
            statement = statement.where(or_(*keyword_conditions))
                
        statement = statement.limit(5)
        results = session.exec(statement).all()

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
