# Claims Micro RAG Assistant 🏥

A production-ready Retrieval-Augmented Generation (RAG) system built for insurance policy and claims information retrieval. This application combines the power of LangChain, FAISS vector search, LangGraph agentic workflows, and Google Gemini AI to provide accurate, citation-backed answers to insurance-related queries.

## 🌟 Features

- **🔍 Semantic Search**: FAISS-powered vector database with cosine similarity for precise document retrieval
- **🤖 RAG Pipeline**: LangChain-based document processing with intelligent chunking and embedding
- **🔗 LangGraph Agent**: Agentic workflow with human-in-the-loop capabilities for gathering missing information
- **📊 Grounding & Citations**: Confidence scores and source citations for every answer
- **🔒 Privacy-First**: Automatic Aadhaar number masking for PII protection
- **📈 Evaluation Framework**: Built-in evaluation system to measure hit rate and precision@k
- **🏥 Health Monitoring**: Health check endpoints for production deployment
- **⚡ Performance Tracking**: Request logging with latency metrics

## 🏗️ Architecture

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────┐
│      FastAPI Server              │
│  ┌──────────┬──────────────┐   │
│  │  /ask    │  /askgraph   │   │
│  └──────────┴──────────────┘   │
└──────┬─────────────┬────────────┘
       │             │
       ▼             ▼
┌──────────────┐  ┌──────────────┐
│ RAG Pipeline │  │  LangGraph   │
│   + FAISS    │  │   Agent      │
└──────┬───────┘  └──────┬───────┘
       │                 │
       └────────┬────────┘
                ▼
        ┌───────────────┐
        │ Google Gemini │
        │   (LLM + EMB) │
        └───────────────┘
```

## 📁 Project Structure

```
.
├── server.py              # FastAPI application with REST endpoints
├── rag_pipeline.py        # Document loading, chunking, and vector DB
├── graph.py               # LangGraph agent with tool-calling
├── models.py              # LLM and embeddings model configuration
├── eval.py                # RAG evaluation framework
├── main.py                # Application entry point
├── test_app.py            # Unit tests
├── data/                  # Text documents for knowledge base
├── vdb/                   # FAISS vector database (generated)
└── .env                   # Environment variables
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Google Gemini API key

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/nishantguvvada/claim-micro-rag.git
   cd claim-micro-rag/backend
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**

   Create a `.env` file in the project root:

   ```env
   GEMINI_API_KEY=your_google_gemini_api_key_here
   ```

5. **Prepare your documents**

   Place your insurance policy documents (`.txt` files) in the `data/` directory.

6. **Build the vector database**

   Uncomment `store.create_index(chunks)` in rag_pipeline.py to create the index for the first time.

   ```bash
   python rag_pipeline.py
   ```

7. **Run the server**

   Uncomment `vectordb = VectorDB(embeddings_model=embeddings_model).load_index()` in rag_pipeline.py to load the created index.

   ```bash
   python main.py
   ```

   or

   ```bash
   uvicorn server:app --reload
   ```

   The API will be available at `http://localhost:8000`

## 📚 API Documentation

### 1. RAG Query Endpoint

**POST** `/ask`

Query the insurance knowledge base with semantic search and get AI-generated answers with citations.

**Request Body:**

```json
{
  "query": "What is the TAT for claim processing?",
  "k": 3
}
```

**Response:**

```json
{
  "answer": "The Turnaround Time (TAT) for claim processing is 7 business days from the date of submission...",
  "citations": [
    {
      "doc": "data/claims_faq.txt",
      "snippet": "Claim processing turnaround time is...",
      "content": "Full relevant document chunk text..."
    }
  ],
  "grounding_score": 0.85,
  "retrieval": {
    "k": 2,
    "latency_ms": 145.32
  }
}
```

**Key Features:**

- Relevance threshold filtering (0.60)
- Grounding score calculation
- Document snippets for quick scanning
- Performance metrics

### 2. LangGraph Agent Endpoint

**POST** `/askgraph`

- Interact with the agentic workflow that can retrieve documents or request additional information.
- The endpoint returns a response object along with a thread id. Use the thread id to maintain context across multiple interactions.
- Any request without the `id` field creates a new conversation thread.
- `resume_data` field must be used instead of `query` field when the interrupt object is received from the graph. The occurence of the interrupt object denotes that the graph requires more information from the user and has interrupted the flow for user inputs. User must provide the inputs through `resume_data` field to continue the interrupted state.

**Request Body:**

```json
{
  "query": "I want to file a claim",
  "id": null,
  "resume_data": null
}
```

**Response:**

```json
{
  "response": {
    "messages": [...]
  },
  "thread_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Key Features:**

- **Human-in-the-loop**: Agent can interrupt to request missing information
- **Conversation memory**: Maintain context across multiple interactions using thread id
- **Tool calling**: Automatic retrieval and information gathering

### 3. PII Masking Endpoint

**POST** `/mask`

Mask Aadhaar numbers in text for privacy compliance.

**Request Body:**

```json
{
  "details": "My Aadhaar number is 123412341234"
}
```

**Response:**

```json
{
  "masked": "My Aadhaar number is XXXX-XXXX-1234"
}
```

### 4. Health Check

**GET** `/healthz`

Monitor system health and dependencies.

**Response:**

```json
{
  "status": "ok",
  "dependencies": {
    "vectordb": "ok",
    "llm": "ok"
  }
}
```

## 🧪 Testing

### Run Unit Tests

```bash
pytest test_app.py -v
```

## ✅ Project Checklist

---

### 📁 1. Ingest & Index

- [x] Create `data/` directory with the required text files:

  - [x] `policy_101.txt`
  - [x] `policy_201.txt`
  - [x] `kyc_rules.txt`
  - [x] `fraud_signals.txt`
  - [x] `faq_claims.txt`
  - [x] `hospitals.txt`

- [x] Load and chunk documents sensibly (200–400 chars with overlap)
- [x] Embed documents using a **local embedding model** (e.g., `sentence-transformers/all-MiniLM-L6-v2`)
- [x] Store embeddings in a **local vector database** (e.g., FAISS)
- [x] Document and expose a retrieval endpoint that returns top-k search results

---

### 🤖 2. Answering API

- [x] Implement `POST /ask` endpoint
- [x] Request body: `{ "query": "...", "k": 3 }`
- [x] Pipeline: Retrieve top-k → Compose answer → Return citations
- [x] Response JSON contains:

  - [x] `answer` – concise answer based only on retrieved context
  - [x] `citations` – list with `doc` and `snippet`
  - [x] `retrieval` – includes `k` and `latency_ms`

- [x] At least one citation must appear for simple queries (e.g., TAT, room rent, network hospitals)

---

### 💬 3. Conversational AI Agent

- [x] Build a conversational agent (Semantic Kernel or similar)
- [x] Retain and persist **chat history** for contextual conversations
- [x] Implement **memory** to maintain context across turns
- [x] Add **prompt engineering** for more natural, accurate responses
- [x] Agent should:

  - [x] Ask clarifying questions when input is incomplete
  - [x] Format responses according to instructions

---

### 📊 4. Mini Evaluation

- [x] Create `eval.py` to:

  - [x] Run each query from `eval.jsonl` through `/ask` or pipeline directly
  - [x] Compute:

    - [x] `precision@k` (does any retrieved doc contain `ans_contains`?)
    - [x] `hit rate` (≥1 match)

  - [x] Print a tiny report: `n=5 | hit_rate=0.8 | precision@3=0.73`

- [x] Add a small evaluation set (`eval.jsonl`) with 5 sample queries

---

### 🔐 5. Basic Redaction Utility (Bonus)

- [x] Implement `mask_aadhaar(text)` to replace 12-digit numbers with `XXXX-XXXX-####`
- [x] Demonstrate usage with a `/mask` endpoint
- [ ] (Optional) Explore out-of-the-box filtering features (e.g., Azure AI Content Filters)

---

### 📦 6. Packaging & Quality

- [x] Run the service with a single command:

  ```bash
  uvicorn app:app --reload
  ```

- [x] Provide a clear and complete `README.md`:

  - [x] Project setup instructions
  - [x] How to run the application

- [x] Write **unit tests** (`pytest`):

  - [x] Test `mask_aadhaar`
  - [x] Test retrieval returns ≥ 1 citation for a known question

- [ ] (Optional) Add a `Dockerfile` for containerization

---

### ✅ Acceptance Criteria

- [x] `/ask` returns coherent answers with citations
- [x] `eval.py` runs successfully and prints metrics
- [x] Repository contains:

  - [x] `app.py` (or `main.py`)
  - [x] `eval.py`
  - [x] `data/` directory
  - [x] `README.md`
  - [x] `test_app.py`

- [x] Project runs locally in a fresh virtual environment without paid keys

---

### 🌟 Stretch Goals (Optional)

- [x] Add grounding score (average cosine similarity)
- [ ] Implement a simple re-ranker (e.g., BM25) and show metric improvement
- [ ] Add a streaming endpoint (Server-Sent Events)
- [x] Implement `/healthz` endpoint and lightweight logging middleware

---
