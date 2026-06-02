from models.llm import generate

class Planner:

    def create_plan(self, query):

        
        prompt = f"""
You are a planning agent.

Break the query into steps.

Tools:
- EXCEL → structured data analysis
- PDF_TABLE → table data from PDF
- RAG → document-based reasoning

Rules:
- Use minimal steps
- Use correct tool
- Do NOT repeat steps

Return format:
Step 1: TOOL: task

Query:
{query}
"""

        response = generate(prompt)
        print("PLAN RAW:", response)

        return self.parse_plan(response)

    def parse_plan(self, text):

        steps = []

        for line in text.split("\n"):
            if "Step" in line:
                parts = line.split(":")

                if len(parts) >= 3:
                    tool = parts[1].strip().upper()
                    task = parts[2].strip()

                    steps.append((tool, task))

        return steps