from ingestion.cleaning import clean_text
from ingestion.chunking import chunk_text

def load_text_file(file_path):
    with open(file_path,"r", encoding="utf-8") as f:
        text = f.read()
    text = clean_text(text)
    chunks = chunk_text(text)
    
    return chunks