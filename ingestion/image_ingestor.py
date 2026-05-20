from ingestion.ocr_extractor import OCRService
from ingestion.cleaning import clean_text
from ingestion.chunking import chunk_text


def load_image(file_path):
    
    ocr = OCRService()
    raw_text = ocr.extract_text(file_path)
    
    cleaned_text = clean_text(raw_text)
    
    chunks = chunk_text(cleaned_text)
    
    return chunks