from embeddings.embeddings_service import EmbeddingService
from embeddings.vector_store import VectorStore
from retrieval.bm25  import BM25Retriever
from retrieval.rrf import reciprocal_rank_fusion
from retrieval.reranker import Reranker

class HybridSearch:
    def __init__(self):
        self.embedder = EmbeddingService()
        self.store = VectorStore()
        self.reranker = Reranker()
        self.bm25 = BM25Retriever()   
        self.documents = []

    def index(self, documents):
        embeddings = self.embedder.encode(documents)

        ids = [str(i) for i in range(len(documents))]
        metadata = [{"source": "file"} for _ in documents]

        self.store.add(ids, documents, embeddings, metadata)
        self.bm25.fit(documents)

    def search(self, query):
        print("Step 1: vector done")
        query_embedding = self.embedder.encode(query)[0]
        vector_results = self.store.query(query_embedding)
        
        print("Step 2: bm25 done")
        bm25_results = self.bm25.search(query)
        fused_results = reciprocal_rank_fusion(bm25_results, vector_results)
        
        print("Step 3: fusion done")
        print("Step 4: reranker starting...")
        final_results = self.reranker.rerank(query=query, documents=fused_results[:10],top_k=5)
        print("Step 5: done")
        
        return final_results
