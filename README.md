#Medical Report Summarizer API

This project provides an API that accepts medical reports in various formats (TXT, PDF, DOCX) and returns a summarized version of the report using NLP techniques. The application is built using FastAPI and leverages Hugging Face's transformers for text summarization.

## Features

- *Upload Medical Reports*: Supports .txt, .pdf, and .docx file formats.
- *Text Summarization*: Summarizes the text content of the uploaded medical reports.
- *Chunking for Large Texts*: Handles large text inputs by processing them in chunks to avoid token limit issues.
- *Simple Web Interface*: Provides an HTML form for file uploads, allowing users to easily interact with the API.

## Installation

### Prerequisites

- Python 3.7+
- pip (Python package installer)

### Step 1: Clone the Repository

```bash
git clone https://github.com/ssrimant/Content_Summarization.git
cd Content_Summarization
pip install -r requirements.txt
uvicorn main:app --reload


### The application will be available at http://127.0.0.1:8000/.

Usage

Web Interface
Navigate to http://127.0.0.1:8000/ in your web browser.
Upload a medical report in .txt, .pdf, or .docx format.
Click "Upload and Summarize" to receive a summarized version of the report.
API Endpoint


Technical Details

Summarization Model
The summarization functionality is powered by Hugging Face's distilbart-cnn-12-6 model. The text is processed in chunks to handle large documents, ensuring the summarizer works within token limits.

File Handling
PDF: Extracted using PyPDF2.
DOCX: Extracted using python-docx.
TXT: Read directly as text.
Chunking
To avoid issues with long documents, the text is divided into chunks with a maximum length of 1024 tokens. Each chunk is summarized individually, and the final summary is a concatenation of all chunk summaries.




