from models.llm import generate
from app.planner import Planner
from memory.chat_memory import ChatMemory
from evaluation.evaluator import Evaluator
from evaluation.logger import Logger
import asyncio
from config import SYSTEM_PROMPT
from memory.vector_memory import VectorMemory

class Agent:
    def __init__(self, rag_system, excel_tool=None,pdf_table_tool=None):
        self.rag = rag_system
        self.excel = excel_tool
        self.pdf_table = pdf_table_tool
        
        self.planner = Planner()
        self.memory = ChatMemory()
        
        self.evaluator = Evaluator()
        self.logger = Logger()
        
        self.vector_memory = VectorMemory()

    
    async def execute_tool(self, tool, task):

        if tool == "EXCEL" and self.excel:
            return await asyncio.to_thread(
                self.excel.smart_query, task, generate
            )

        elif tool == "PDF_TABLE" and self.pdf_table:
            return await asyncio.to_thread(
                self.pdf_table.smart_query, task, generate
            )

        elif tool == "RAG":
            return await asyncio.to_thread(
                self.rag.search, task
            )

        return "Unknown tool"
        
    # ✅ Multi-step execution
    async def run(self, query):
        
        # step 1: get past conversation
        history = self.memory.get()
        
        #convert memory to text
        past_context = ""
        for item in history:
            past_context += f"user: {item['user']}\nAssistant: {item['response']}\n"
        
        memory_context = self.vector_memory.search(query)
        memory_text = "\n".join(memory_context[:3])
        enriched_query = f"""
        Conversation so far:
        {past_context}

        Relevant past memory:
        {memory_text}

        Current question:
        {query}
        """        
        # Step 2: get plan from planner
        plan = self.planner.create_plan(enriched_query)

        # fallback if planner fails
        if not plan:
            plan = [("EXCEL", query)]

        print("FINAL PLAN:", plan)

        tasks = []

        # Step 3: execute steps
        for tool,task in plan:
            tasks.append(self.execute_tool(tool,task))

        results_raw = await asyncio.gather(*tasks)
        
        results = []
        for i , res in enumerate(results_raw):
            print(f"STEP {i+1} RESULT:", res)
            results.append(f"Step {i+1}:\n{res}")
            
        # Step 4: final answer (keep Claude style)
        final_prompt = f"""
        
        {SYSTEM_PROMPT}
Conversation:
{past_context}

Results:
{results}

User question:
{query}


Instructions:
- Use ONLY the context
- Be accurate and structured
- Avoid unnecessary text

Give final answer:
"""

        final_answer = generate(final_prompt)

        # ✅ Step 5: store memory
        self.memory.add(query, final_answer)
        
        evaluation = self.evaluator.evaluate(query=query, context=str(results), answer=final_answer)
        print("\nEVALUATION:\n", evaluation)


        # ✅ Step 6: log the interaction
        self.logger.log({
            "query": query,
            "final_answer": final_answer,
            "results": results
        })
        
        self.memory.add(query, final_answer)
        self.vector_memory.add(f"User: {query} | Answer: {final_answer}")
        return final_answer
