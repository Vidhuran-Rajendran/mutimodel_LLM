from models.llm import generate
from app.planner import Planner
from memory.chat_memory import ChatMemory

class Agent:
    def __init__(self, rag_system, excel_tool=None,pdf_table_tool=None):
        self.rag = rag_system
        self.excel = excel_tool
        self.pdf_table = pdf_table_tool
        
        self.planner = Planner()
        self.memory = ChatMemory()

    # ✅ Multi-step execution
    def run(self, query):
        
        # step 1: get past conversation
        history = self.memory.get()
        
        #convert memory to text
        past_context = ""
        for item in history:
            past_context += f"user: {item['user']}\nAssistant: {item['response']}\n"
        
        enriched_query = f""" 
        Converation so far: {past_context}
        Current question: {query}
        """
        

        # Step 2: get plan from planner
        plan = self.planner.create_plan(enriched_query)

        # fallback if planner fails
        if not plan:
            plan = [("EXCEL", query)]

        print("FINAL PLAN:", plan)

        results = []

        # Step 3: execute steps
        for i, (tool, task) in enumerate(plan, 1):

            print(f"Executing Step {i}: {tool} → {task}")

            if tool == "EXCEL" and self.excel:
                result = self.excel.smart_query(task, generate)                
                
            elif tool == "PDF_TABLE" and self.pdf_table:
                result = self.pdf_table.smart_query(task,generate)

            elif tool == "RAG":
                docs = self.rag.search(task)
                result = "\n".join(docs[:3])

            else:
                result = "Unknown tool"

            print(f"STEP {i} RESULT:", result)

            results.append(f"Step {i} Result:\n{result}")

        # Step 4: final answer (keep Claude style)
        final_prompt = f"""
Conversation:
{past_context}

Results:
{results}

User question:
{query}

Give final answer:
"""

        final_answer = generate(final_prompt)

        # ✅ Step 5: store memory
        self.memory.add(query, final_answer)

        return final_answer
