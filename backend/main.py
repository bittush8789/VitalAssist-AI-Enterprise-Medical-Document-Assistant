from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
import shutil

app = FastAPI(title="VitalAssist AI API", version="1.0.0")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount frontend
app.mount("/static", StaticFiles(directory="../frontend"), name="static")

@app.get("/")
def serve_frontend():
    return FileResponse("../frontend/index.html")

# Create required directories
os.makedirs("uploads", exist_ok=True)
os.makedirs("embeddings", exist_ok=True)

class QueryRequest(BaseModel):
    query: str

class TextRequest(BaseModel):
    text: str

@app.post("/api/upload")
async def upload_document(file: UploadFile = File(...)):
    """Uploads a document (PDF/Image) for processing."""
    try:
        file_path = os.path.join("uploads", file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Here we would normally trigger OCR and RAG ingestion
        return {"status": "success", "filename": file.filename, "message": "File uploaded successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/extract-text")
async def extract_text(request: TextRequest):
    """Placeholder for OCR extraction"""
    return {"text": "Simulated OCR Text from: " + request.text[:20]}

@app.post("/api/chat")
async def chat(request: QueryRequest):
    """Placeholder for RAG chatbot"""
    return {"response": f"AI response for: {request.query}", "sources": []}

@app.post("/api/extract-diagnosis")
async def extract_diagnosis(request: TextRequest):
    """Placeholder for Diagnosis Agent"""
    return {"diagnosis": ["Hypertension"], "medications": ["Lisinopril"]}

@app.post("/api/generate-summary")
async def generate_summary(request: TextRequest):
    """Placeholder for Summary Agent"""
    return {"summary": "Patient presented with elevated blood pressure..."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
