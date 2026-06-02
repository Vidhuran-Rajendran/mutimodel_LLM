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
        answer = generate(prompt)

        for _ in range(2):
            if "not in context" in answer.lower() or len(answer.strip()) < 20:
                fix_prompt = f"""
                The previous answer was weak.
                Context:
                {context}
                Question:
                {query}
                Improve the answer.
                """
                answer = generate(fix_prompt)
        return answer
                        
            
