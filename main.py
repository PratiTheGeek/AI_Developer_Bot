from fastapi import FastAPI
from dotenv import load_dotenv
from llama_index.core import  StorageContext, load_index_from_storage
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
import os
from llama_index.llms.openrouter import OpenRouter
from sentence_transformers import SentenceTransformer


#import for free embadding model
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings


load_dotenv()
os.environ['API_KEY'] = os.getenv("API_KEY")
API_KEY = os.getenv("API_KEY")

app = FastAPI()


# Use free embedding model
Settings.embed_model = HuggingFaceEmbedding(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    cache_folder="./models"
)
llm = OpenRouter(
    api_key=API_KEY,
    model="gpt-3.5-turbo", 
)
Settings.llm = llm


#load precomputed index for storage
storage_context = StorageContext.from_defaults(persist_dir="./storage")
index = load_index_from_storage(storage_context)
query_engine = index.as_query_engine()



@app.get("/")
async def root():
    return {"message": "developer docuemntation chatbot is running"}

@app.get("/query/")
async def query_docs(question: str):
    response = index.as_query_engine().query(question)
    return {"response": str(response)}


'''llama index internally uses Seting.llm module an din taht nmodule llm is openai so, I have modified that and have used openrouter's api key '''

# https://madhuriiiii.app.n8n.cloud/webhook-test/chatbot
# https://973f9bb4ac03.ngrok-free.app -> http://localhost:80
# client ID : 9461424273923.9450997235703
# client secret : 436d7f8b26abe013dd0ae866f81dff76
# signing secret: 350ea4d5966e35f889edb658c4ae01a0
# verification token: MgcyEEjaT9WJMDDnIdLo58Gw
# app id: A09D8VB6XLP