import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

persist_directory = "chroma_db"

embedding_model = OpenAIEmbeddings()

# Função para carregar e adicionar metadados
def load_and_tag(file_path, source_type):
    docs = []
    if file_path.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
        docs = loader.load()
    elif file_path.endswith(".txt"):
        loader = TextLoader(file_path, encoding="utf-8")
        docs = loader.load()
    else:
        print(f"Formato não suportado: {file_path}")
        return []

    for doc in docs:
        doc.metadata["source_type"] = source_type
        doc.metadata["file_name"] = os.path.basename(file_path)
    return docs

all_docs = []

# Leis
all_docs.extend(load_and_tag("docs/lei_15042.txt", "norma"))

# FAQ
all_docs.extend(load_and_tag("docs/faq_alunos.txt", "faq"))

# Artigos
artigos_dir = "docs/artigos/"
for filename in os.listdir(artigos_dir):
    file_path = os.path.join(artigos_dir, filename)
    if filename.endswith(".pdf"):
        all_docs.extend(load_and_tag(file_path, "artigo"))

# Splitter configurado (1000 tokens com 150 de overlap)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
split_docs = text_splitter.split_documents(all_docs)

# Vetorização no ChromaDB
db = Chroma.from_documents(split_docs, embedding_model, persist_directory=persist_directory)
db.persist()

print(f"Ingestão concluída. {len(split_docs)} pedaços vetorizados.")
