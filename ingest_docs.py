import os
from dotenv import load_dotenv
import pdfplumber
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema.document import Document

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# Pasta dos PDFs
docs_path = "./docs"

def extract_text_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

documents = []
for filename in os.listdir(docs_path):
    if filename.endswith(".pdf"):
        file_path = os.path.join(docs_path, filename)
        text = extract_text_from_pdf(file_path)
        documents.append(Document(page_content=text, metadata={"source": filename}))

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
docs_split = splitter.split_documents(documents)

embedding_model = OpenAIEmbeddings()
db = Chroma.from_documents(docs_split, embedding_model, persist_directory="./chroma_db")

db.persist()

print(f"Ingestão finalizada. {len(docs_split)} pedaços salvos no vetor.")
