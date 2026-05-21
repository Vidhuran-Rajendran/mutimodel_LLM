from models.llm import generate
from app.planner import Planner


class Agent:
    def __init__(self, rag_system, excel_tool=None):
        self.rag = rag_system
        self.excel = excel_tool
        self.planner = Planner()

    # ✅ Multi-step execution
    def run(self, query):

        # Step 1: get plan from planner
        plan = self.planner.create_plan(query)

        # fallback if planner fails
        if not plan:
            plan = [("EXCEL", query)]

        print("FINAL PLAN:", plan)

        results = []

        # Step 2: execute steps
        for i, (tool, task) in enumerate(plan, 1):

            print(f"Executing Step {i}: {tool} → {task}")

            if tool == "EXCEL" and self.excel:
                result = self.excel.smart_query(task, generate)

            elif tool == "RAG":
                docs = self.rag.search(task)
                result = "\n".join(docs[:3])

            else:
                result = "Unknown tool"

            print(f"STEP {i} RESULT:", result)

            results.append(f"Step {i} Result:\n{result}")

        # Step 3: final answer (keep Claude style)
        final_prompt = f"""
Use these step results to answer the question:

{results}

Question:
{query}
"""

        final_answer = generate(final_prompt)

        return final_answer