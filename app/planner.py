from models.llm import generate

class Planner:

    def create_plan(self, query):

        prompt = f"""
Break the query into steps.

Tools:
- EXCEL → spreadsheet dataset
- PDF_TABLE → tables extracted from PDFs
- RAG → document text retrieval

Examples:

Q: average car price
Step 1: EXCEL: average car price

Q: average employee salary from pdf
Step 1: PDF_TABLE: average employee salary

Q: summarize report
Step 1: RAG: summarize report

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