from qdrant_client import QdrantClient
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.postprocessor.sbert_rerank import SentenceTransformerRerank
from src.config.configuration import configure_settings
import os
import logging
import sys
# On ajoute le dossier courant au chemin pour que Python trouve nos modules 'src'
sys.path.append(".") 
from src.config.params import QDRANT_URL

# Configuration du logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# On ajoute le dossier courant au chemin pour que Python trouve nos modules 'src'
sys.path.append(".") 

configure_settings()

def get_query_engine(db_path: str = QDRANT_URL):
    """
    Charge l'index existant et retourne un moteur de requête prêt à l'emploi.
    """
    # 1. Connexion à la DB existante
    
    client = QdrantClient(url=db_path)
    vector_store = QdrantVectorStore(client=client, collection_name="mokaco_manuals")

    # 2. Chargement de l'index sans re-calculer les embeddings 
    index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
    
    if not index:
        logger.error("L'index n'a pas pu être chargé depuis Qdrant ou est vide.")

    # 3. Création du moteur de chat
    try:
        rerank_postprocessor = SentenceTransformerRerank(
            model="BAAI/bge-reranker-v2-m3", #Modèle de Reranking SBERT optimisé pour les embeddings BGE
            top_n=5  # Nombre de passages à reclasser
        )
        #index.set_postprocessor(rerank_postprocessor)
        logger.info("Post-processeur de re-ranking SBERT configuré avec succès.")
    except Exception as e:
        logger.error(f"Erreur lors de la configuration du post-processeur de re-ranking : {e}")
        
    engine = index.as_query_engine(
        similarity_top_k=10, 
        node_postprocessors=[rerank_postprocessor]
        #system_prompt=MOKACO_SYSTEM_PROMPT
    )
    
    return engine