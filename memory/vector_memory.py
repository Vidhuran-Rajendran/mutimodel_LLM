from embeddings.embeddings_service import EmbeddingService
from embeddings.vector_store import VectorStore

class VectorMemory:

    def __init__(self):
        self.embedder = EmbeddingService()
        self.store = VectorStore(collection_name="memory")

    def add(self, text):

        embedding = self.embedder.encode(text)[0]

        self.store.add(
            ids=[str(hash(text))],
            documents=[text],
            embeddings=[embedding],
            metadatas=[{"type": "memory"}]
        )

    def search(self, query):

        query_embedding = self.embedder.encode(query)[0]

        results = self.store.query(query_embedding)

        return results