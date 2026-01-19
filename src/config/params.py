from dotenv import load_dotenv
import os

load_dotenv()

# --- CHEMINS DE DONNEES ---
RAW_DATA_PATH = "data/raw"
VECTOR_STORE_PATH = "data/vector_db"
PERSIST_DIRECTORY = "data/vector_db"

# --- MODELES LLM ---
OPEN_AI_LLM = ""  # À compléter si nécessaire
MIXTRAL_LLM = ""
IBM_LLM = ""
LLAMA_LLM = ""

#QDRANT URL
QDRANT_URL = os.getenv("QDRANT_URL")

#Paramètres de qdrant
QDRANT_COLLECTION_NAME = "mokaco_manuals"

# --- EMBEDDINGS ---
EMBEDDING_MODEL = "text-embedding-3-small"

# --- PARAMETRAGE DU CHUNKING ---
CHUNK_SIZE = 700
CHUNK_OVERLAP = 100

# --- PARAMETRAGE DU LLM ---
MAX_NEW_TOKENS = 250
MIN_NEW_TOKENS = 50
TEMPERATURE = 0.3
TOP_P = 0.9
TOP_K = 25
