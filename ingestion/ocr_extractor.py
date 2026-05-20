from paddleocr import PaddleOCR

class OCRService:
    def __init__(self):
        self.ocr = PaddleOCR(use_angle_cls = True, lang='en',
                             det_model_dir = r"E:\training\mutimodel_LLM\models\paddle_models\en_PP-OCRv3_det_infer",
                             rec_model_dir = r"E:\training\mutimodel_LLM\models\paddle_models\en_PP-OCRv3_rec_infer")
        
    def extract_text(self, image_path):
        result = self.ocr.ocr(image_path, cls=True)
        
        extracted_text = ""
        
        for line in result:
            for word in line:
                text = word[1][0]
                extracted_text += text + " "
            
        return extracted_text.strip()