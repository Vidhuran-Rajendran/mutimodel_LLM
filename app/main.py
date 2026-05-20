from retrieval.search import HybridSearch
from ingestion.pdf_ingestor import load_pdf
from ingestion.excel_ingestor import load_excel
from tools.excel_agent import ExcelAgent
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
        df = load_excel(r"data\raw\used_cars_data.xlsx")
        excel_agent = ExcelAgent(df)

        print("Excel Agent Ready ✅")

        print("\nSuggested questions:")
        print(excel_agent.suggest_questions())

    except Exception as e:
        print(f"Error loading Excel file: {e}")

    # MAIN LOOP STARTS HERE
    agent = Agent(vs, excel_agent)
    while True:
        query = input(">> ")

        if query.lower() == "exit":
            break

        response = agent.run(query)
        print("\nAnswer:\n", response)

if __name__ == "__main__":
    main()