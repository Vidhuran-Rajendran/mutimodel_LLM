from models.llm import generate

class Agent:
    def __init__(self,rag_system, excel_tool=None):
        self.rag = rag_system
        self.excel = excel_tool
        
    def choose_tool(self,query):
        """Asking LLm to decide"""
        prompt = f"""
You are an intelligent router.

Choose the best tool for the query.

Available tools:
1. RAG → for general knowledge / documents
2. EXCEL → for data analysis (numbers, averages, tables)

Rules:
- If query involves numbers, averages, totals → EXCEL
- Otherwise → RAG

Query:
{query}

Return ONLY one word: RAG or EXCEL
"""
        decision = generate(prompt).strip().upper()
        
        return decision
    
    def run(self, query):
        tool = self.choose_tool(query)
        
        if tool == "RAG":
            results = self.rag.search(query)
            print(f"[Agent] Selected tool: {tool}")
            
            if tool == "EXCEL" and self.excel:
                return self.excel.smart_query(query, generate)
            
            results = self.rag.search(query)
            
            context = "\n".join(results[:3])
            response = generate(f"""
            Answer based on context:
            Context:{context}
            Question:{query}""")
            
            return response