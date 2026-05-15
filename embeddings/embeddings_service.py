from sentence_transformers import SentenceTransformer

class EmbeddingService:
    def __init__(self):
        self.model = SentenceTransformer("BAAI/beg-large-en")
        
        def encode(self, texts):
            if isinstance(texts, str):
                texts = [texts]
            return self.model.encode(texts).tolist()