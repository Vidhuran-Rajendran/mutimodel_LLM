from embeddings.embeddings_service import EmbeddingService
from embeddings.vector_store import VectorStore
from retrieval.bm25  import BM25Retriever
from retrieval.hybrid import reciprocal_rank_fusion

class HybridSearch:
    def __init__(self):
        self.embedder = EmbeddingService()
        self.store = VectorStore()
        self.bm25 = BM25Retriever()   
        self.documents = []

    def index(self, documents):
        embeddings = self.embedder.encode(documents)

        ids = [str(i) for i in range(len(documents))]
        metadata = [{"source": "file"} for _ in documents]

        self.store.add(ids, documents, embeddings, metadata)
        self.bm25.fit(documents)

    def search(self, query):
        query_embedding = self.embedder.encode(query)[0]
        vector_results = self.store.query(query_embedding)
        
        bm25_results = self.bm25.search(query)
        final_result = reciprocal_rank_fusion(bm25_results, vector_results)

        return final_result[:5]
