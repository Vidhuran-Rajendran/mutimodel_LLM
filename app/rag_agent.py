from models.llm import generate

class RAGAgent:
    
    def __init__(self, rag_system):
        self.rag = rag_system
        
    def run(self, query):
        
        docs = self.rag.search(query)
        context = "\n".join(docs[:3])
        
        prompt = f"""
        Answer using context
        {context}
        
        Question:
        {query}
        """
        return generate(prompt)