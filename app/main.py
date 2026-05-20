from retrieval.search import HybridSearch
from ingestion.pdf_ingestor import load_pdf
from ingestion.excel_ingestor import load_excel
from tools.excel_tool import ExcelTool
from models.llm import generate
from app.agent import Agent

def main():
    print("Multimodal AI System (RAG Enabled)")

    vs = HybridSearch()

    # ✅ Load and index data (ONE TIME)
    filepath = r"data\raw\research_test_file.pdf"
    docs = load_pdf(filepath)
    vs.index(docs)
    print("Documents indexed!")

    excel_agent = None
    try:
        df = load_excel("data/raw/sample.xlsx")
        excel_agent = ExcelTool(df)

        print("Excel Agent Ready ✅")

        print("\nSuggested questions:")
        print(excel_agent.suggest_questions())

    except:
        print("No Excel file found")

    # MAIN LOOP STARTS HERE
    while True:
        query = input(">> ")

        if query.lower() == "exit":
            break

        # ROUTING
        if "excel" in query and excel_agent:
            response = excel_agent.smart_query(query, generate)

        elif "summary" in query and excel_agent:
            response = excel_agent.summary()

        else:
            results = vs.search(query)
            context = "\n".join(results[:3])

            response = generate(f"""
Answer using context:
{context}
Question: {query}
""")
        print("\nAnswer:\n", response)

if __name__ == "__main__":
    main()