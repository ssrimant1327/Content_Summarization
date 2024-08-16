from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse, HTMLResponse
import io
from PyPDF2 import PdfReader
import docx
from transformers import pipeline

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <html>
        <head>
            <title>Medical Report Summarizer</title>
        </head>
        <body>
            <h1>Welcome to the Medical Report Summarizer API</h1>
            <p>Use the form below to upload a medical report and receive a summary.</p>
            <form action="/uploadfile/" method="post" enctype="multipart/form-data">
                <input type="file" name="file" accept=".txt,.pdf,.docx">
                <br><br>
                <input type="submit" value="Upload and Summarize">
            </form>
        </body>
    </html>
    """

@app.post("/uploadfile/")
async def create_summary(file: UploadFile = File(...)):
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

    # Generate summary
    summary = generate_summary(text)

    return JSONResponse(content={"summary": summary})

def generate_summary(text):
    summarizer = pipeline("summarization")

    # Split the text into smaller chunks
    max_chunk_length = 1024
    chunks = [text[i:i + max_chunk_length] for i in range(0, len(text), max_chunk_length)]

    # Summarize each chunk individually
    summaries = []
    for chunk in chunks:
        summary = summarizer(chunk, max_length=150, min_length=30, do_sample=False)
        summaries.append(summary[0]['summary_text'])

    # Combine all summaries into one
    final_summary = " ".join(summaries)
    return final_summary

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
