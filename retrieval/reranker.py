from sentence_transformers import CrossEncoder
import torch
class Reranker:
    def __init__(self):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = CrossEncoder(r"E:\training\mutimodel_LLM\models\bge_reranker_model", device=device)
        
    def rerank(self,query, documents, top_k =5):
        #step:1 create query, doc pair
        
        documents = [str(doc) for doc in documents]
        pairs = [[query, doc] for doc in documents]

            
        #setp:2 model predicts relevance scores
        scores = self.model.predict(pairs)
        
        #step:3 combine docs with scores
        doc_scores_pairs = list(zip(documents,scores))
        
        #step:4 sort by scores
        ranked = sorted(doc_scores_pairs, key = lambda x: x[1],reverse = True)
        
        #step:5 return only top_k documents
        return [doc for doc, _ in ranked[:top_k]]
        
        
