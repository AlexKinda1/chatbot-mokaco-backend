from qdrant_client import QdrantClient
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.postprocessor.sbert_rerank import SentenceTransformerRerank
from llama_index.core.llms import ChatMessage
from llama_index.core.memory import Memory

import sys
# On ajoute le dossier courant au chemin pour que Python trouve nos modules 'src'
sys.path.append(".") 

from src.config.configuration import configure_settings
import os
import logging 
from src.config.params import QDRANT_URL, QDRANT_COLLECTION_NAME, SBERT_RERANKING_MODEL, TOP_N_RERANK, MEMORY_TOKEN_LIMIT, CHAT_HISTORY_TOKEN_RATIO, MEMORY_TOKEN_FLUSH_SIZE, SIMILARITY_TOP_K, CHAT_MODE
from src.config.prompts import PROMPT_TEMPLATE

# Configuration du logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# On ajoute le dossier courant au chemin pour que Python trouve nos modules 'src'
sys.path.append(".") 

configure_settings()

def get_chat_engine(db_path: str = QDRANT_URL):
    """
    Charge l'index existant et retourne un moteur de requête prêt à l'emploi.
    """
    # 1. Connexion à la DB existante
    
    client = QdrantClient(url=db_path)
    vector_store = QdrantVectorStore(client=client, collection_name=QDRANT_COLLECTION_NAME)

    # 2. Chargement de l'index sans re-calculer les embeddings 
    index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
    
    if not index:
        logger.error("L'index n'a pas pu être chargé depuis Qdrant ou est vide.")

    # 3. Création du moteur de chat
    try:
        rerank_postprocessor = SentenceTransformerRerank(
            model=SBERT_RERANKING_MODEL, #Modèle de Reranking SBERT optimisé pour les embeddings BGE
            top_n=TOP_N_RERANK  # Nombre de passages à reclasser
        )
        #index.set_postprocessor(rerank_postprocessor)
        logger.info("Post-processeur de re-ranking SBERT configuré avec succès.")
    except Exception as e:
        logger.error(f"Erreur lors de la configuration du post-processeur de re-ranking : {e}")
        
    #Configuration de la memoire de conversation
    memory = Memory.from_defaults(
        session_id="my_session",
        token_limit=MEMORY_TOKEN_LIMIT,
        chat_history_token_ratio=CHAT_HISTORY_TOKEN_RATIO,
        token_flush_size=MEMORY_TOKEN_FLUSH_SIZE
    )
    
    logger.info("Mémoire de conversation configurée avec succès.")
        
    chat_engine = index.as_chat_engine(
        chat_mode=CHAT_MODE, # Mode intelligent : reformule la question
        memory=memory,
        #system_prompt=MOKACO_SYSTEM_PROMPT,
        similarity_top_k=SIMILARITY_TOP_K,
        node_postprocessors=[rerank_postprocessor], # On garde notre super Reranker
        verbose=True # Affiche dans la console comment il reformule la question (utile pour debug)       
    )

    #Pensez au context_prompt ou au system_prompt plus tard
    """context_prompt=(
        "You are a chatbot, able to have normal interactions, as well as talk"
        " about an essay discussing Paul Grahams life."
        "Here are the relevant documents for the context:\n"
        "{context_str}"
        "\nInstruction: Use the previous chat history, or the context above, to interact and help the user."
    )"""

    return chat_engine