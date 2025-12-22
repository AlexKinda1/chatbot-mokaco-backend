# src/ingest.py
import pinecone
import logging
import os
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext
from params import CHUNK_SIZE, CHUNK_OVERLAP, pinecone_api_key, EMBEDDING_MODEL, PINECONE_INDEX_NAME
from llama_index.vector_stores.pinecone import PineconeVectorStore
from langchain_huggingface import HuggingFaceEmbeddings

# Configuration du logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialiser l'embedder une seule fois (global)
embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

#FONCTIONS D'INGESTION DES FICHIERS 
def load_documents_from_path(directory_path):
    """Charge les documents PDF/txt depuis le répertoire spécifié."""
    logger.info(f"Chargement des documents depuis : {directory_path}")
    
    try:
        if not os.path.exists(directory_path):
            logger.warning(f"Répertoire introuvable : {directory_path}")
            return []
        
        reader = SimpleDirectoryReader(input_dir=directory_path)
        documents = reader.load_data()
        logger.info(f"Nombre de documents chargés : {len(documents)}")
        return documents
    
    except Exception as e:
        logger.error(f"Erreur lors du chargement des documents : {e}")
        return []   
    
# FONCTIONS DE DECOUPAGE DES DOCUMENTS 
def split_documents(documents):
    """Découpe les documents en chunks de taille configurable."""
    logger.info("Démarrage du découpage des documents")
        
    try:
        
        text_splitter = SentenceSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
        # Corriger : documents est déjà une liste, ne pas l'envelopper à nouveau
        nodes = text_splitter.get_nodes_from_documents(documents)
        
        logger.info(f"Nombre total de 'chunks' créés : {len(nodes)}")
        return nodes
    
    except Exception as e:
        logger.error(f"Erreur lors du découpage des documents : {e}")
        return []

# FONCTIONS DE CREATION DE LA BASE VECTORIELLE AVEC PINECONE 
def create_vector_database(nodes):
    """Crée ou réutilise un index Pinecone et upsert les nodes."""
    
    logger.info("Création/initialisation de la base de données vectorielle Pinecone")
    
    try:
        # Vérifier que les paramètres requis sont présents
        if not pinecone_api_key:
            raise ValueError("pinecone_api_key est vide ou non configuré")
        if not nodes:
            logger.warning("Aucun node à indexer")
            return None
        
        # Initialiser Pinecone
        pinecone.init(api_key=pinecone_api_key, environment="us-west1-gcp")
        logger.info("Pinecone initialisé.")
        
        # Vérifier et créer l'index seulement s'il n'existe pas
        index_name = PINECONE_INDEX_NAME or "mokaco_faqs"
        existing_indexes = pinecone.list_indexes()
        
        if index_name not in existing_indexes:
            logger.info(f"Création de l'index Pinecone '{index_name}' (dimensions=384, metric=cosine)...")
            pinecone.create_index(
                index_name, 
                dimension=384,  # doit correspondre à EMBEDDING_MODEL (all-MiniLM-L6-v2 → 384)
                metric="cosine",  # meilleur pour embeddings texte
                pod_type="p1"
            )
            logger.info(f"Index '{index_name}' créé avec succès.")
        else:
            logger.info(f"Index '{index_name}' existe déjà, réutilisation.")
        
        # Initialiser le client et le vector store
        pinecone_index = pinecone.Index(index_name)
        vector_store = PineconeVectorStore(pinecone_index, embeddings)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        
        # Indexation des documents
        logger.info(f"Indexation de {len(nodes)} nodes...")
        index = VectorStoreIndex.from_documents(documents=nodes, storage_context=storage_context)
        
        logger.info("Base de données vectorielle créée et persistée avec succès.")
        return index

    except ValueError as e:
        logger.error(f"Erreur de configuration : {e}")
        return None
    
    except pinecone.exceptions.PineconeException as e:
        logger.error(f"Erreur Pinecone  lors de la creationnde la base de donnée vectorielle : {e}")
        return None
    
    except Exception as e:
        logger.error(f"Erreur lors de la création de la base de données vectorielle : {e}")
        return None

def ingest_pipeline(directory_path):
    logger.info("Début de l'ingestion")
    #Chagement des documents
    documents = load_documents_from_path(directory_path)
    if not documents:
        logger.error("Aucun doucument chargé, fin de l'ingestion.")
        return None
    
    #Découpage des documents
    nodes = split_documents(documents)
    if not nodes:
        logger.error("Aucun chunk créé, fin de l'ingestion.")
        return None
    
    #Création de la base vectorielle
    index = create_vector_database(nodes)
    if not index:
        logger.error("Échec de la création de la base vectorielle, fin de l'ingestion.")
        return None
    
    logger.info("Ingestion terminée avec succès.")
    return index

if __name__ == "__main__":
    import sys
    from pathlib import Path

    direc_path = sys.argv[1] if len(sys.argv) > 1 else "data/raw"

    if Path(direc_path).exists():
        ingest_pipeline(direc_path)
    else:
        logger.error(f"Répertoire spécifié introuvable : {direc_path}")
        sys.exit(1)