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

    def query(self, embedding, top_k=5):
        return self.collection.query(
            query_embeddings=[embedding],
            n_results=top_k
        )