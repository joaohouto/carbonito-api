import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.schema.document import Document
import re

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

file_path = "docs/lei_15042.txt"
persist_directory = "chroma_db"

embedding_model = OpenAIEmbeddings()

with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

# Regex pra separar os artigos
pattern = r"(Art\.\s?\d+º?.*?)(?=Art\.\s?\d+º|\Z)"  # pega de 'Art. 1º' até o próximo ou fim
articles = re.findall(pattern, text, flags=re.DOTALL)

# Cria os Documentos com metadados
docs = []
for artigo_texto in articles:
    match = re.match(r"(Art\.\s?\d+º)", artigo_texto)
    artigo_id = match.group(1) if match else "Artigo Desconhecido"
    doc = Document(
        page_content=artigo_texto.strip(),
        metadata={"source_type": "norma", "file_name": "lei_15042.txt", "artigo": artigo_id}
    )
    docs.append(doc)

print(f"{len(docs)} artigos encontrados.")

splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
split_docs = splitter.split_documents(docs)

# Vetorização
db = Chroma.from_documents(split_docs, embedding_model, persist_directory=persist_directory)
db.persist()

print(f"Ingestão da lei concluída: {len(split_docs)} pedaços vetorizados.")
