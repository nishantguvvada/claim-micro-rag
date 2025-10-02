from server import mask_aadhaar
from rag_pipeline import vectordb

def test_mask_aadhaar():
    text = "My Aadhaar is 123412341234 and my PAN is ABCDE1234F."
    masked = mask_aadhaar(text)
    assert masked == "My Aadhaar is XXXX-XXXX-1234 and my PAN is ABCDE1234F."

def test_one_citation():
    query = "What is the TAT for claim processing?"
    k = 3
    retrieved_results = vectordb.similarity_search_with_relevance_scores(query, k)
    filtered_docs = [doc for doc, score in retrieved_results if score >= 0.60]
    assert len(filtered_docs) >= 1