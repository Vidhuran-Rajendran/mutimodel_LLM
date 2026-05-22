import pandas as pd
from app.agent import Agent
from models.llm import generate
from tools.excel_agent import ExcelAgent
from retrieval.search import HybridSearch
from ingestion.pdf_ingestor import load_pdf
import ingestion.excel_ingestor as excel_loader
from ingestion.pdf_table_extractor import extract_pdf_tables

def main():
    print("Multimodal AI System (RAG Enabled)")

    vs = HybridSearch()

    # ✅ Load and index data (ONE TIME)
    filepath = r"data\raw\research_test_file.pdf"
    docs = load_pdf(filepath)
    vs.index(docs)
    
    pdf_tables = extract_pdf_tables(filepath)
    pdf_table_agent = None
    if pdf_tables:
        combined_pdf_df = pd.concat(pdf_tables, ignore_index=True)
        pdf_table_agent = ExcelAgent(combined_pdf_df)
        print("PDF Table Agent Ready ✅")
    print("Documents indexed!")

    excel_agent = None
    
    try:
        df = excel_loader.load_excel(r"data\raw\used_cars_data.xlsx")
        print(type(df))
        excel_agent = ExcelAgent(df)

        print("Excel Agent Ready ✅")
        print("\nSuggested questions:")
        
        print(excel_agent.suggest_questions())

    except Exception as e:
        print(f"Error loading Excel file: {e}")

    # MAIN LOOP STARTS HERE
    agent = Agent(rag_system=vs,excel_tool= excel_agent,pdf_table_tool = pdf_table_agent)
    while True:
        query = input(">> ")

        if query.lower() == "exit":
            break

        response = agent.run(query)
        print("\nAnswer:\n", response)

if __name__ == "__main__":
    main()