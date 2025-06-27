# 🌿 Carbonito API

[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

API open source de chatbot especialista em **Mercado de Carbono**, **Pantanal** e **legislação ambiental brasileira**. Este projeto foi desenvolvido no curso de **Direito da UEMS — Unidade de Aquidauana** para o **Pantanal Tech 2025**.

Veja ao vivo em https://carbonito.vercel.app/

A API utiliza a técnica de **Retrieval-Augmented Generation (RAG)** para gerar respostas baseadas em documentos oficiais, leis e pesquisas regionais.

## 📦 Tecnologias

- **Python**
- **FastAPI**
- **LangChain**
- **ChromaDB**
- **OpenAI API**
- **slowapi** (Rate Limiting)

## 🚀 Como funciona esse trem?

O **Retrieval-Augmented Generation (RAG)** é uma abordagem que combina busca de informações em bases de dados vetorizadas com modelos de linguagem generativa.

No nosso caso:

1. Os documentos sobre mercado de carbono, legislação ambiental e Pantanal são transformados em vetores (embeddings) e armazenados no ChromaDB. Dê uma olhada no `ingest_docs.py`.
2. Quando o usuário faz uma pergunta, a API:
   - Busca os vetores mais próximos da pergunta (informações relevantes).
   - Passa esse contexto junto com a pergunta para o GPT-4o via API da OpenAI.
   - O modelo gera a resposta considerando o conteúdo buscado.

Isso garante respostas mais seguras, baseadas em documentos reais e locais.

## 🛠️ Setup do Projeto

### 📋 Pré-requisitos:

- Python `>=3.11`
- API Key da [OpenAI](https://platform.openai.com/api-keys)

### 1. Clone o projeto:

```bash
git clone https://github.com/joaohouto/carbonito-api.git
cd carbonito-api

```

### 2. Instale as dependências:

```bash
pip install -r requirements.txt
```

### 3. Configure o `.env`:

Crie um arquivo `.env` na raiz do projeto:

```ini
OPENAI_API_KEY=YOUR_OPENAI_API_KEY
```

### 4. Faça a ingestão dos documentos:

Coloque seus PDFs e arquivos na pasta `docs/` e rode:

```bash
python ingest_docs.py
```

Isso vai criar a base vetorizada no diretório `chroma_db/`.

### 5. Execute a API:

```bash
uvicorn api:app --reload
```

A API estará acessível em: `http://localhost:8000`. Nesse ponto, você pode rodar um `curl` para testar api no seu terminal.

```
curl -X POST http://localhost:8000/query -H "Content-Type: application/json" -d '{"question":"Quais as vantagens do crédito de carbono para produtores no Pantanal?"}'
```

## 🐍 Desenvolvido por

Alunos do curso de Direito - UEMS/Aquidauana para o Pantanal Tech 2025.
Idealizado por [@joaohouto](https://joaocouto.com) com apoio da galera do curso.
