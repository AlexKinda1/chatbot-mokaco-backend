from qdrant_client import QdrantClient
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.qdrant import QdrantVectorStore
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
    # C'est ici qu'on pourra plus tard configurer le "Reranking" ou la mémoire de conversation
    engine = index.as_query_engine(similarity_top_k=3) # On récupère les 3 meilleurs morceaux de texte
    
    return engine