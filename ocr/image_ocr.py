from paddleocr import PaddleOCR
import os

# Initialize PaddleOCR
# Use lang='en' for English medical documents
ocr_engine = PaddleOCR(use_angle_cls=True, lang='en')

def extract_text_from_image(image_path):
    try:
        result = ocr_engine.ocr(image_path, cls=True)
        text = ""
        for idx in range(len(result)):
            res = result[idx]
            for line in res:
                text += line[1][0] + " "
        return text.strip()
    except Exception as e:
        return f"OCR Error: {str(e)}"
