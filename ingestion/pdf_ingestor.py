import pdfplumber
from ingestion.chunking import chunk_text
from ingestion.cleaning import clean_text
#from ingestion.ocr_extractor import OCRService

def load_pdf(file_path):
    full_text = ""
    #ocr = OCRService()
    
    with pdfplumber.open(file_path) as pdf:
        for i ,page in enumerate(pdf.pages):
            text = page.extract_text()
            # if not text:
            #     print(f"ocr used for page {i+1}")
            #     img = page.to_image(resolution=300).original
            #     image_path = f"data/temp/temp_page_{i+1}.png"
            #     img.save(image_path)
                
            if text:
                full_text += f"\n[Page {i+1}]\n"
                full_text += text
            
            if not full_text.strip():
                print("⚠️ No text found in PDF (likely scanned)")

    
    cleaned_text = clean_text(full_text)
    chunks = chunk_text(cleaned_text)
    
    return chunks
    
        

