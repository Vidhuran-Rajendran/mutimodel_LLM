def reciprocal_rank_fusion(bm25_docs, vector_docs, k=60):
    scores = {}

    for rank, doc in enumerate(bm25_docs):
        scores[doc] = scores.get(doc, 0) + 1 / (rank + k)

    for rank, doc in enumerate(vector_docs):
        scores[doc] = scores.get(doc, 0) + 1 / (rank + k)
        
    sorted_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    return [doc for doc, _ in sorted_docs]