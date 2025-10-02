from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List
from langchain_community.vectorstores import FAISS, DistanceStrategy
from models import embeddings_model
from dotenv import load_dotenv

load_dotenv()

class DocumentLoader:

    def __init__(self, chunk_size=350, chunk_overlap=90):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def load(self, path):
        loader = DirectoryLoader(
            path, 
            glob="*.txt", 
            loader_cls=TextLoader, 
            use_multithreading=True,
            loader_kwargs={'encoding': 'utf-8'}
        )

        return loader.load()
    
    def split(self, docs: List[Document]) -> List[Document]:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )

        return text_splitter.split_documents(docs)

class VectorDB:

    def __init__(self, embeddings_model):
        self.embeddings_model = embeddings_model

    def create_index(self, docs: List[Document]):
        vectordb = FAISS.from_documents(
            documents=docs, 
            embedding=self.embeddings_model,
            normalize_L2=True,
            distance_strategy=DistanceStrategy.COSINE
        )

        vectordb.save_local("./vdb")

        print("Vector DB built!")

    def load_index(self) -> FAISS:
        return FAISS.load_local("./vdb", self.embeddings_model, allow_dangerous_deserialization=True)

vectordb = VectorDB(embeddings_model=embeddings_model).load_index()

if __name__ == "__main__":
    loader = DocumentLoader()
    docs = loader.load(path="data")
    chunks = loader.split(docs=docs)
    print(f"Split documents into {len(chunks)} chunks.")
    print(chunks)

    store = VectorDB(embeddings_model=embeddings_model)
    # store.create_index(chunks)
    vectordb = store.load_index()

    docs = vectordb.similarity_search_with_relevance_scores("what are the kyc rules?", k=3, score_threshold=0.80)
    print(docs)