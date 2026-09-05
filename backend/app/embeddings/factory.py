from app.embeddings.base import EmbeddingProvider
from app.embeddings.sentence_transformer import SentenceTransformerProvider
from app.embeddings.openai_embeddings import OpenAIEmbeddingProvider
from app.config import settings

def get_embedding_provider() -> EmbeddingProvider:
    provider_name = settings.EMBEDDING_PROVIDER.lower()
    
    if provider_name == "openai":
        return OpenAIEmbeddingProvider()
    else:
        # Default to local
        return SentenceTransformerProvider()
