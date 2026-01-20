from dotenv import load_dotenv
import os

load_dotenv()

# --- CHEMINS DE DONNEES ---
RAW_DATA_PATH = "data/raw"
VECTOR_STORE_PATH = "data/vector_db"
PERSIST_DIRECTORY = "data/vector_db"

# --- MODELES LLM ---
OPEN_AI_LLM = ""  # À compléter si nécessaire
GEMINI_LLM = "models/gemini-2.5-flash"

# --- EMBEDDINGS ---
GEMINI_EMBEDDING = "models/text-embedding-004"

# RERANKING MODEL
SBERT_RERANKING_MODEL = "BAAI/bge-reranker-v2-m3"
TOP_N_RERANK = 5 # Nombre de passages à reclasser

#QDRANT 
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_COLLECTION_NAME = "mokaco_manuals"


# --- PARAMETRAGE DU CHUNKING ---
CHUNK_SIZE = 700
CHUNK_OVERLAP = 100

# PARAMETRES DU CHAT ENGINE
MAX_NEW_TOKENS = 250 
MIN_NEW_TOKENS = 50
TEMPERATURE = 0.3
TOP_P = 0.9
SIMILARITY_TOP_K = 10
CHAT_MODE = "condense_plus_context"

# GESTION DE LA MEMOIRE
MEMORY_TOKEN_LIMIT = 70000
CHAT_HISTORY_TOKEN_RATIO = 0.7
MEMORY_TOKEN_FLUSH_SIZE = 3000
