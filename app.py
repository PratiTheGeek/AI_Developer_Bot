import os
from dotenv import load_dotenv
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex , StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb
from sentence_transformers import SentenceTransformer



#  Import for local embedding
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings
model = SentenceTransformer()
#  Set a free HuggingFace embedding model
Settings.embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2", cache_folder="./models")

load_dotenv()
os.environ['API_KEY'] = os.getenv("API_KEY")


#load document using simple directory reader
documents = SimpleDirectoryReader('./documentation').load_data()

#initializing chromadb
chroma_client = chromadb.PersistentClient(path = './storage') #this will create persistent chroadb instance that will store at given path


#load a chroma collection
collection_name = "doc_collection"

try:
    chroma_collection = chroma_client.get_collection(collection_name)
except Exception:
    chroma_collection = chroma_client.create_collection(collection_name)

#wrap chromadb as vectorestore
vector_store = ChromaVectorStore(chroma_collection)

#create vectore index
# index = Vectore_storeIndex.from_documents(documents, vectore_store = vector_store)
index = VectorStoreIndex.from_documents(documents, vector_store=vector_store)


#save storage contex for later use
index.storage_context.persist('./storage')

print("Documents index successfully")



# activate env:  conda activate chatbot
# uvicorn main:app --reload
