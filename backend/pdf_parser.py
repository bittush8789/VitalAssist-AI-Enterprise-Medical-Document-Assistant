import fitz  # PyMuPDF
import pdfplumber

def extract_text_from_pdf(pdf_path):
    text = ""
    # Method 1: PyMuPDF (Fast)
    try:
        doc = fitz.open(pdf_path)
        for page in doc:
            text += page.get_text()
        doc.close()
    except Exception as e:
        print(f"PyMuPDF error: {e}")

    # Method 2: pdfplumber (Good for tables)
    if not text.strip():
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
        except Exception as e:
            print(f"pdfplumber error: {e}")
            
    return text
