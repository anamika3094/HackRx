from fastapi import FastAPI, Request
from pydantic import BaseModel
import requests
import fitz  # PyMuPDF
from sentence_transformers import SentenceTransformer
from fastapi import Header, HTTPException
import faiss
import subprocess
import tempfile
import numpy as np

app = FastAPI()

model = SentenceTransformer('all-MiniLM-L6-v2')  # Free transformer
index = None
chunks = []

class QueryRequest(BaseModel):
    documents: str
    questions: list

def download_pdf(url):
    response = requests.get(url)
    print(f"[DEBUG] Downloaded {len(response.content)} bytes from {url}")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(response.content)
        return tmp_file.name

def extract_text(pdf_path):
    doc = fitz.open(pdf_path)
    return [page.get_text() for page in doc]

def prepare_embeddings(text_pages):
    global chunks, index
    chunks = []
    for page in text_pages:
        for para in page.split("\n\n"):
            if len(para.strip()) > 40:
                chunks.append(para.strip())
    if not chunks:
        raise ValueError("No valid text chunks extracted from PDF.")
    embeddings = model.encode(chunks, convert_to_numpy=True)
    if isinstance(embeddings, list):
        embeddings = np.array(embeddings)
    if embeddings.ndim == 1:
        embeddings = embeddings.reshape(1, -1)
    print("Embeddings shape:", embeddings.shape)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

def query_ollama_mistral(prompt):
    proc = subprocess.Popen(
        ['ollama', 'run', 'mistral'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding='utf-8'  # <-- This ensures Unicode handling
    )
    out, err = proc.communicate(prompt)
    if err:
        print('[OLLAMA STDERR]', err)
    return out.strip()

def get_top_chunks(question):
    question_emb = model.encode([question], convert_to_numpy=True)
    if question_emb.ndim == 1:
        question_emb = question_emb.reshape(1, -1)
    D, I = index.search(question_emb, k=3)
    return [chunks[i] for i in I[0] if i != -1 and i < len(chunks)]

@app.post("/hackrx/run")
async def run_query(data: QueryRequest, authorization: str = Header(...)):
    expected_token = "6890cfc475e4b61cf6b049684a7c7fa65ebb88696d672f1a9ce7d86f901bdbb8"
    if authorization != expected_token:
        raise HTTPException(status_code=401, detail="Unauthorized")


    try:
        print("[INFO] Downloading PDF...")
        pdf_path = download_pdf(data.documents)
        print(f"[INFO] Saved to: {pdf_path}")

        print("[INFO] Extracting text...")
        pages = extract_text(pdf_path)
        print(f"[INFO] Total pages: {len(pages)}")

        print("[INFO] Preparing embeddings...")
        prepare_embeddings(pages)
        print(f"[INFO] Chunks created: {len(chunks)}")

        answers = []
        for q in data.questions:
            top_chunks = get_top_chunks(q)
            prompt = f"""You are an expert insurance assistant. Use the following context to answer the question clearly.

Context:
{top_chunks[0]}
{top_chunks[1] if len(top_chunks)>1 else ''}
{top_chunks[2] if len(top_chunks)>2 else ''}

Question:
{q}

Answer:"""
            print(f"[PROMPT]: {prompt}")
            response = query_ollama_mistral(prompt)
            answers.append(response)

        return {"answers": answers}

    except Exception as e:
        print(f"[ERROR] {e}")
        raise HTTPException(status_code=500, detail=str(e))
