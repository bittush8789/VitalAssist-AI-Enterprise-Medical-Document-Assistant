from fastapi import FastAPI, UploadFile, File, Depends
from workflows.langgraph_flow import medical_workflow
from ocr.pdf_parser import extract_text_from_pdf
from ocr.image_ocr import extract_text_from_image
import os

app = FastAPI(title="Medical AI API")

@app.get("/")
def read_root():
    return {"message": "Welcome to Enterprise Medical AI API"}

@app.post("/process-document")
async def process_document(file: UploadFile = File(...)):
    # Save file
    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    
    # Extract text
    if file.filename.endswith(".pdf"):
        text = extract_text_from_pdf(file_path)
    else:
        text = extract_text_from_image(file_path)
    
    # Run workflow
    inputs = {"text": text, "summary": "", "diagnosis": {}, "insurance": {}, "codes": {}, "metadata": {}}
    results = medical_workflow.invoke(inputs)
    
    return results
