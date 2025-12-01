# src/ingest.py

import os
import shutil
import pinecone
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext
from params import CHUNK_SIZE, CHUNK_OVERLAP, pinecone_api_key
from llama_index.vector_stores.pinecone import PineconeVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
import logging

logger = logging.getLogger(__name__)
# Configuration du logging
logger.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# --- FONCTIONS D'INGESTION DES FICHIERS ---
def load_documents_from_path(directory_path):# ajouter la variable doc_type si reference aux metadata

    logger.info(
        f"Chargement des documents depuis : {directory_path}"
    )
    
    try:
        reader = SimpleDirectoryReader(input_dir= directory_path)
        documents = reader.load_data()

        """for doc in documents:
        doc.metadata["doc_type"] = doc_type
        # On nettoie le nom du fichier pour le garder en référence
        doc.metadata["source"] = os.path.basename(doc.metadata["source"])"""

        logger.info(f"Nombre de documents chargés : {len(documents)}")
        return documents
    
    except Exception as e:
        logger.error(f"Erreur lors du chargement des documents : {e}")
        return []   
    
# --- FONCTIONS DE DECOUPAGE DES DOCUMENTS ---
def split_documents(documents):

    logger.info("Démarrage du découpage des documents")
        
    try:   
        text_splitter = SentenceSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
        nodes = text_splitter.get_nodes_from_documents([documents])

        logger.info(f"Nombre total de 'chunks' créés : {len(nodes)}")
        return nodes
    
    except Exception as e:
        logger.error(f"Erreur lors du découpage des documents : {e}")
        return []

# --- FONCTIONS DE CREATION DE LA BASE VECTORIELLE ---
def create_vector_database(nodes):
    
    logger.info("Création de la base de données vectorielle")
    
    try:
        pinecone.init(api_key=pinecone_api_key, environment="us-west1-gcp")
        pinecone.create_index(
            "mokaco_faqs", dimensiosn=384, metric="cosine", pod_type="p1"
        )
        
        logger.info("Index Pinecone crée avec succès.")
        
        pinecone_index = pinecone.Index("mokaco_faqs")
        vector_store = PineconeVectorStore(pinecone_index, HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2"))
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        index = VectorStoreIndex.from_documents(documents=nodes, storage_context=storage_context)
        
        logger.info("Base de données vectorielle créée avec succès.")
        return index

    except Exception as e:
        logger.error(f"Erreur lors de la création de la base de données vectorielle : {e}")
        return None