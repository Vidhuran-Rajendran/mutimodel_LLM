from rank_bm25 import BM25Okapi
import re

class BM25Retriever:
    def __init__(self):
        self.bm25 = None
        self.docs = []

    def fit(self, documents):
        self.docs = documents
        tokenized = [doc.split() for doc in documents]
        self.bm25 = BM25Okapi(tokenized)

    def search(self, query, top_k=5):

        
        if self.bm25 is None:
            return []
        query_tokens = query.split()
        #query_tokens = re.findall(r'\b\w+\b', query.lower())
        scores = self.bm25.get_scores(query_tokens)
        ranked = sorted(
            zip(self.docs, scores),
            key=lambda x: x[1],
            reverse=True
        )
        return [doc for doc, _ in ranked[:top_k]]



    