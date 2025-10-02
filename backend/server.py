from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
import uvicorn
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from dotenv import load_dotenv
from rag_pipeline import vectordb
from graph import ask_graph
from models import llm, embeddings_model
import logging
import time
import re
from functools import wraps
import uuid

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("MyAppLog")

class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        try:
            response = await call_next(request)
        except Exception as e:
            logger.error(f"Exception during request: {request.method} {request.url} : {e}")
            raise e
        end_time = time.time()
        latency = round((end_time - start_time) * 1000, 2)
        logger.info(f"Request: {request.method} {request.url.path} processed in {latency}ms with status code: {response.status_code}")
        return response

load_dotenv()

app = FastAPI(
    title="Claims Retrieval API",
    version="1.0.0",
    description="A simple RAG retrieval endpoint."
)

app.add_middleware(LoggingMiddleware)

@app.get("/")
def default():
    return { "response": "on"}

class UserQuery(BaseModel):
    query: str
    k: int

class Citation(BaseModel):
    doc: str
    snippet: str
    content: str

class Retrieval(BaseModel):
    k: int
    latency_ms: Optional[float]

class RetrievedResponse(BaseModel):
    answer: str = Field(description="Answer to the user query")
    citations: List[Citation] = Field(description="List of citations")
    grounding_score: Optional[float]
    retrieval: Retrieval = Field(description="k documents retreived and latency in milisecond")

@app.post("/ask", response_model=RetrievedResponse)
async def retrieval(user_query: UserQuery) -> RetrievedResponse:
    query = user_query.query
    
    start_time = time.perf_counter()
    # retrieved_results = await vectordb.asimilarity_search(query, k=user_query.k)
    retrieved_results = await vectordb.asimilarity_search_with_relevance_scores(query, k=user_query.k)
    print(retrieved_results)
    end_time = time.perf_counter()
    latency = round((end_time - start_time) * 1000, 2)

    # query_embedding = np.array(embeddings_model.embed_query(query)).reshape(1, -1)

    # cosine_similarity_scores = []
    # for doc in retrieved_results:
    #     doc_embedding = np.array(embeddings_model.embed_query(doc.page_content)).reshape(1, -1)
    #     cosine_similarity_scores.append(
    #         cosine_similarity(
    #             query_embedding,
    #             doc_embedding
    #         )[0][0]
    #     )

    # grounding_score = np.mean(cosine_similarity_scores) if cosine_similarity_scores else 0.0
    # print(grounding_score)
    grounding_score = round(float(np.mean([score for _, score in retrieved_results])), 2) if len(retrieved_results) > 0 else 0.0
    # print(grounding_score)

    # filtered_docs = [(doc, score) for doc, score in zip(retrieved_results, cosine_similarity_scores) if score >= 0.75]
    filtered_docs = [(doc, score) for doc, score in retrieved_results if score >= 0.60]

    if filtered_docs:
        context = "\n\n".join(f"Context: {doc.page_content}\nCitation: {doc.metadata['source']}" for doc, _ in filtered_docs)
    else:
        context = "No relevant context found in the knowledge base."

    prompt = (
        "You are an insurance claim information assistant. "
        "Use ONLY the provided context below to answer the user's question concisely and accurately. "
        "ONLY USE THE CONTEXT WHEN THE QUERY PERTAINS TO INSURANCE.\n\n"
        f"User Query: {query}\n\nContext:\n{context}"
    )

    response = llm.invoke(prompt)

    return RetrievedResponse(
        answer=response.content,
        citations=[
            Citation(
                doc=doc.metadata.get('source','N/A'), 
                snippet=" ".join(doc.page_content.split()[:8]) + "...",
                content=doc.page_content
            ) for doc, _ in filtered_docs
        ],
        grounding_score=grounding_score,
        retrieval=Retrieval(k=len(filtered_docs), latency_ms=latency)
    )

    # ---- Structured Output ----

    # llm_structured_output = llm.with_structured_output(RetrievedResponse, method="json_mode")
    
    # ---- Structured Output ----

class GraphQuery(BaseModel):
    query: str
    id: Optional[uuid.UUID] = None
    resume_data: Optional[str] = None

@app.post("/askgraph")
def invoke_graph(user_query: GraphQuery) -> Dict[str, Any]:
    response = ask_graph(user_query.query, user_query.id, user_query.resume_data)
    return response

def mask_aadhaar(text: str) -> str:
    def mask_match(match):
        digits = re.sub(r'\D', '', match.group())
        if len(digits) == 12:
            return f"XXXX-XXXX-{digits[-4:]}"
        return match.group()
    return re.sub(r'(?:\d[\s-]*){12}', mask_match, text)

def aadhaar_mask(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)

        if isinstance(result, str):
            return mask_aadhaar(result)
        
        if isinstance(result, dict):
            return {
                k: mask_aadhaar(v) if isinstance(v, str) else v
                for k, v in result.items()
            }
        return result
    return wrapper

class MaskDetails(BaseModel):
    details: str

@app.post("/mask")
@aadhaar_mask
def mask(user_details: MaskDetails) -> Dict[str, str]:
    return {"masked": user_details.details}

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)