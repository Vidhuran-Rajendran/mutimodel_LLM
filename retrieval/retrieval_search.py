from embeddings.embeddings_service import EmbeddingService
from embeddings.vector_store import VectorStore

class VectorSearch:
    def __init__(self):
        self.embedder = EmbeddingService()
        self.store = VectorStore()

    def index(self, documents):
        embeddings = self.embedder.encode(documents)

        ids = [str(i) for i in range(len(documents))]
        metadata = [{"source": "file"} for _ in documents]

        self.store.add(ids, documents, embeddings, metadata)

    def search(self, query):
        query_embedding = self.embedder.encode(query)[0]
        results = self.store.query(query_embedding)

        return results
