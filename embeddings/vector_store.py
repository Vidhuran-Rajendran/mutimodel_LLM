import chromadb

class VectorStore:
    def __init__(self, path="./data/db", collection_name="docs"):
        self.client = chromadb.PersistentClient(path=path)
        self.collection = self.client.get_or_create_collection(name=collection_name)

    def add(self, ids, documents, embeddings, metadatas, batch_size = 500):
        total = len(ids)
        if total == 0:
            print("no documents to index")
            return
        
        for i in range(0, total, batch_size):
            batch_ids = ids[i:i+batch_size]
            batch_docs = documents[i:i+batch_size]
            batch_embeds = embeddings[i:i+batch_size]
            batch_meta = metadatas[i:i+batch_size]
            
            self.collection.add(
                ids=batch_ids,
                documents=batch_docs,
                embeddings=batch_embeds,
                metadatas=batch_meta
            )

    def query(self, query_embedding, top_k=5):
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        # Check if documents exist and are not None
        documents = results.get("documents")
        
        if documents and len(documents) > 0:
            return documents[0]  # ✅ Safely return the first list of docs
        
        return []