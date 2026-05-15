import chromadb

class VectorStore:
    def __init__(self, path="./data/db", collection_name="docs"):
        self.client = chromadb.PersistentClient(path=path)
        self.collection = self.client.get_or_create_collection(name=collection_name)

    def add(self, ids, documents, embeddings, metadatas):
        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
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