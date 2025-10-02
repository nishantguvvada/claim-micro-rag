from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv()

embeddings_model = GoogleGenerativeAIEmbeddings(
    model="models/text-embedding-004",
    google_api_key=os.getenv("GEMINI_API_KEY")
)

llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash', api_key=os.getenv('GEMINI_API_KEY'))