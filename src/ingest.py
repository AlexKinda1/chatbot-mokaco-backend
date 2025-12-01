# src/ingest.py

import os
import shutil
import pinecone
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext
from ingest import CHUNK_SIZE, CHUNK_OVERLAP, PERSIST_DIRECTORY, EMBEDDING_MODEL_NAME
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
        """if os.path.exists(PERSIST_DIRECTORY):
            logger.warning(
                f"Suppression de l'ancienne base de données : {PERSIST_DIRECTORY}"
            )
            shutil.rmtree(PERSIST_DIRECTORY)

        vector_store = VectorStoreIndex.from_documents(
            documents=nodes,
            show_progress=False,
            embed_model=embeddings,
            persist_dir=PERSIST_DIRECTORY
        )"""
        
        

        vector_store.persist()
        logger.info("Base de données vectorielle créée et persistée avec succès !")
        return vector_store
    
    except Exception as e:
        logger.error(f"Erreur lors de la création de la base de données vectorielle : {e}")
        return None




def initialize_embeddings():

    logging.info(f"Initialisation du modèle d'embedding : {EMBEDDING_MODEL_NAME}")

    model_kwargs = {"device": "cpu"}
    # Tester plus tard avec True
    encode_kwargs = {"normalize_embeddings": False}

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs,
    )
    return embeddings


def create_vector_store(chunks, embeddings):
    # Pré-nettoyage : Supprime l'ancienne base si elle existe
    if os.path.exists(PERSIST_DIRECTORY):
        logging.warning(
            f"Suppression de l'ancienne base de données : {PERSIST_DIRECTORY}"
        )
        shutil.rmtree(PERSIST_DIRECTORY)

    logging.info(f"Création de la nouvelle base vectorielle à : {PERSIST_DIRECTORY}")

    vector_store = Chroma.from_documents(
        documents=chunks, embedding=embeddings, persist_directory=PERSIST_DIRECTORY
    )

    logging.info("Base de données vectorielle créée et persistée avec succès !")
    return vector_store
