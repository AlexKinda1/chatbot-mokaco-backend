import sys
sys.path.append(".") # On ajoute le dossier courant au chemin pour que Python trouve nos modules 'src'

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext
from llama_index.core.node_parser import SentenceSplitter
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from src.config.params import QDRANT_URL, RAW_DATA_PATH
import os
from src.config.configuration import configure_settings
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Appel de la fonction de configuration au démarrage
configure_settings()

def run_ingestion(data_dir: str = RAW_DATA_PATH, db_path: str = QDRANT_URL):
    
    print(f"Démarrage de l'ingestion depuis {data_dir}...")

    # 1. Lecture des documents
    try:
        reader = SimpleDirectoryReader(data_dir) 
        documents = reader.load_data()
        logger.info(f" {len(documents)} documents sources chargés.")
    except Exception as e:
        logger.error(f"Erreur lors du chargement des documents : {e}")

    # 2. Configuration du Chunking (Ingénierie des caractéristiques)
    try:
        text_splitter = SentenceSplitter(
            chunk_size=512,    # Taille idéale pour text-embedding-004
            chunk_overlap=50 # Marge de sécurité pour ne pas couper les phrases
        )
    except Exception as e:
        logger.error(f"Erreur lors de la configuration du text_splitter : {e}")

    # 3. Connexion Qdrant et création du Vector Store
    try:
        if not QDRANT_URL:
            logger.error("QDRANT_URL est inexistant. Définir l'URL dans variable d'environnement '.env'.")
            return None
        client = QdrantClient(url=db_path)
        vector_store = QdrantVectorStore(client=client, collection_name="mokaco_manuals")
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
    except Exception as e:
        logger.info("Erreur lors de la configuration de qdrant: {e}")

    # 4. Indexation avec Transformation
    try:
        index = VectorStoreIndex.from_documents(
            documents,
            storage_context=storage_context,
            transformations=[text_splitter], # On applique le splitter ici
            show_progress=True
        )
        logger.info(" Ingestion terminée. Les données sont découpées et vectorisées.")
        return index
    except Exception as e:
        logger.error(f"Erreur lors de l'indexation des documents : {e}")
        return None

    