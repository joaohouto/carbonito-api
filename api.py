import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from fastapi.middleware.cors import CORSMiddleware # Adicione esta linha

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# Carregar .env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# Inicializar FastAPI e Limiter
app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://carbonito.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Conectar no ChromaDB
embedding_model = OpenAIEmbeddings()
db = Chroma(persist_directory="./chroma_db", embedding_function=embedding_model)

# Configurar LLM
llm = ChatOpenAI(model_name="gpt-4o", temperature=0)

# Prompt template
prompt_template = """
Você é o **Carbonito**, um especialista em legislação ambiental, mercado de carbono e agronegócio brasileiro, com foco no Pantanal.

Utilize **as informações dos documentos abaixo** para responder, de forma **clara, objetiva e acessível**, a qualquer pergunta.

Se houver informações provenientes de documentos classificados como "norma", priorize-os na resposta.

---

**Base de dados personalizada:**

{context}

---

**Pergunta:** {question}

**Resposta:**
"""


prompt = PromptTemplate(
    template=prompt_template,
    input_variables=["context", "question"]
)

# QA chain
qa = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=db.as_retriever(),
    chain_type="stuff",
    chain_type_kwargs={"prompt": prompt}
)

# Modelo da requisição
class Question(BaseModel):
    question: str

# Rota com limite de 5 requisições por minuto por IP
@app.post("/query")
@limiter.limit("5/minute")
def query_api(question: Question, request: Request):
    response = qa.run(question.question)
    return {"answer": response}
