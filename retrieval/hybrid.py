def reciprocal_rank_fusion(bm25_docs, vector_docs, k=60):
    scores = {}

    for i, doc in enumerate(bm25_docs):
        scores[doc] = scores.get(doc, 0) + 1 / (i + k)

    for i, doc in enumerate(vector_docs):
        scores[doc] = scores.get(doc, 0) + 1 / (i + k)

    return sorted(scores.items(), key=lambda x: x[1], reverse=True)