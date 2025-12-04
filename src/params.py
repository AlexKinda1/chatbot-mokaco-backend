import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- CHEMINS DE DONNEES ---
RAW_DATA_PATH = "data/raw"
MANUALS_PATH = os.path.join(RAW_DATA_PATH, "manuals")
FAQ_PATH = os.path.join(RAW_DATA_PATH, "faq")
VECTOR_STORE_PATH = "data/vector_db"
PERSIST_DIRECTORY = "data/vector_db"

# --- MODELES LLM ---
OPEN_AI_LLM = ""  # À compléter si nécessaire
MIXTRAL_LLM = ""
IBM_LLM = ""
LLAMA_LLM = ""

# --- EMBEDDINGS ---
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# --- PINECONE ---
PINECONE_INDEX_NAME = "mokaco_faqs"
pinecone_api_key = os.getenv("PINECONE_API_KEY", "pcsk_K34dn_JadARxwXqsKvMQy6CBKa2sneVkqZoS6xasE2Fd9vYPbCSqdBXg9GuHVpwJDji4y")  # ⚠️ À déplacer dans .env

# --- PARAMETRAGE DU CHUNKING ---
CHUNK_SIZE = 700
CHUNK_OVERLAP = 100

# --- PARAMETRAGE DU LLM ---
MAX_NEW_TOKENS = 250
MIN_NEW_TOKENS = 50
TEMPERATURE = 0.3
TOP_P = 0.9
TOP_K = 25

# --- PROMPT TEMPLATE ---
template = """
Tu es "MokaBot", un assistant technique expert pour les machines à café Mokaco. 
Tu es amical, précis et professionnel.
    
Réponds à la question de l'utilisateur en te basant UNIQUEMENT sur le contexte suivant :
    
--- CONTEXTE ---
{context}
---
    
Question de l'utilisateur : {question}
    
Règles strictes :
1. Si le contexte ne contient pas la réponse, dis poliment : "Je suis désolé, je n'ai pas trouvé d'information précise sur ce sujet. Veuillez contacter l'assistance client"
2. Ne réponds PAS à des questions hors sujet (météo, histoire, etc.). Si la question n'a rien à voir avec Mokaco ou les machines à café, réponds : "Je suis spécialisé dans l'assistance pour les produits Mokaco. Je ne peux pas répondre à cette question."
3. Cite tes sources si possible, en mentionnant le nom du document (ex: "d'après le manuel machine_A.pdf").
    
Réponse :
"""