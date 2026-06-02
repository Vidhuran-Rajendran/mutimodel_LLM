from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from app.agent import Agent
from retrieval.search import HybridSearch
from tools.excel_agent import ExcelAgent
from ingestion.pdf_ingestor import load_pdf
from ingestion.pdf_table_extractor import extract_pdf_tables
from ingestion.excel_ingestor import load_excel
import pandas as pd
from models.llm import generate_stream
app = FastAPI()

rag = HybridSearch()

docs = load_pdf(r"data\raw\research_test_file.pdf")
rag.index(docs)

excel_agent = None
try:
    df = load_excel(r"data\raw\used_cars_data.xlsx")
    excel_agent = ExcelAgent(df)
except:
    print("no Excel Loaded")
    
pdf_table_agent = None
try:
    tables = extract_pdf_tables(r"data\raw\research_test_file.pdf")
    if tables:
        combined_pdf_df = pd.concat(tables, ignore_index=True)
        pdf_table_agent = ExcelAgent(combined_pdf_df)
except:
    print("no PDF tables extracted")
    
agent = Agent(rag_system=rag, excel_tool=excel_agent, pdf_table_tool=pdf_table_agent)

class Query(BaseModel):
    query: str

@app.post('/ask')
async def ask(q: Query):
    #answer = await agent.run(q.query)
    
    #return {"query": q.query, "answer": answer}

    async def stream():
        # ✅ run agent (still normal)
        answer = await agent.run(q.query)
        # ✅ stream final answer
        for token in generate_stream(answer):
            yield token
    return StreamingResponse(stream(), media_type="text/plain")
