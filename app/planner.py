from models.llm import generate

class Planner:

    def create_plan(self, query):

        prompt = f"""
Break the user query into steps.

Tools available:
- EXCEL → dataset operations
- RAG → document retrieval

Return STRICTLY:

Step 1: <TOOL>: <task>
Step 2: <TOOL>: <task>

Examples:

Q: average price
Step 1: EXCEL: average price

Q: max price and explain
Step 1: EXCEL: find max price
Step 2: RAG: explain pricing trends

Now:

Q: {query}
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