from models.llm import generate
from app.rag_agent import RAGAgent
from utils.monitor import Monitor
from app.planner import Planner
from memory.chat_memory import ChatMemory
from evaluation.evaluator import Evaluator
from evaluation.logger import Logger
import asyncio
from config import SYSTEM_PROMPT
from memory.vector_memory import VectorMemory

class Agent:
    def __init__(self, rag_system, excel_tool=None,pdf_table_tool=None):
        self.rag_agent = RAGAgent(rag_system)
        self.excel = excel_tool
        self.pdf_table = pdf_table_tool
        
        self.planner = Planner()
        self.memory = ChatMemory()
        
        self.evaluator = Evaluator()
        self.logger = Logger()
        
        self.vector_memory = VectorMemory()
        self.monitor = Monitor()

    
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
                self.rag_agent.run, task
            )

        return "Unknown tool"
        
    # ✅ Multi-step execution
    async def run(self, query):
        self.monitor.logs = []
        
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
        
        t = self.monitor.start("Planner")
        plan = self.planner.create_plan(enriched_query)
        self.monitor.end(t)


        # fallback if planner fails
        if not plan:
            plan = [("EXCEL", query)]

        print("FINAL PLAN:", plan)

        tasks = []

        # Step 3: execute steps
        for tool,task in plan:
            tasks.append(self.execute_tool(tool,task))

        t = self.monitor.start("Tool Execution")
        results_raw = await asyncio.gather(*tasks)
        self.monitor.end(t)

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

        t = self.monitor.start("Final LLM")
        final_answer = generate(final_prompt)
        # retry if weak
        for _ in range(2):
            if len(final_answer.strip()) < 30:
                fix_prompt = f"""
                Improve this answer:
                {final_answer}
                Question:
                {query}"""
                final_answer = generate(fix_prompt)
        self.monitor.end(t)

        # ✅ Step 5: store memory
        self.memory.add(query, final_answer)
        
        evaluation = self.evaluator.evaluate(query=query, context=str(results), answer=final_answer)
        
        print("\nEVALUATION:")
        print("Relevance:", evaluation["relevance"])
        print("Faithfulness:", evaluation["faithfulness"])
        print("Correctness:", evaluation["correctness"])

        avg = (
            evaluation["relevance"] +
            evaluation["faithfulness"] +
            evaluation["correctness"]
        ) / 3

        if avg < 5:
            print("[WARNING] Low quality answer")

        # ✅ Step 6: log the interaction
        self.logger.log({
            "query": query,
            "final_answer": final_answer,
            "results": results,
            "evaluation": evaluation
        })
        
        self.memory.add(query, final_answer)
        self.vector_memory.add(f"User: {query} | Answer: {final_answer}")
        self.monitor.report()
        return final_answer
