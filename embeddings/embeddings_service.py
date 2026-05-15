from sentence_transformers import SentenceTransformer

class EmbeddingService:
    def __init__(self):
        self.model = SentenceTransformer("models/bge_model")
        
    def encode(self, texts):
        if isinstance(texts, str):
            texts = [texts]
        return self.model.encode(texts).tolist()

# import ollama

# class EmbeddingService:
#     def encode(self, texts):
#         if isinstance(texts, str):
#             texts = [texts]

#         embeddings = []

#         for text in texts:
#             response = ollama.embeddings(
#                 model="qwen2.5",
#                 prompt=text
#             )
#             embeddings.append(response["embedding"])

#         return embeddings
