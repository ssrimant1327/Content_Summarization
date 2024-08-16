from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import io
from PyPDF2 import PdfReader
import docx
from transformers import pipeline

app = FastAPI()

@app.post("/uploadfile/")
async def create_summary(file: UploadFile = File(...)):
    # Read the file
    contents = await file.read()

    # Determine file type and extract text
    if file.filename.endswith('.pdf'):
        reader = PdfReader(io.BytesIO(contents))
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    elif file.filename.endswith('.docx'):
        doc = docx.Document(io.BytesIO(contents))
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
    else:
        text = contents.decode("utf-8")

    # Generate the summary
    summary = generate_summary(text)

    return JSONResponse(content={"summary": summary})

def generate_summary(text):
    summarizer = pipeline("summarization")
    summary = summarizer(text, max_length=150, min_length=30, do_sample=False)
    return summary[0]['summary_text']

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
