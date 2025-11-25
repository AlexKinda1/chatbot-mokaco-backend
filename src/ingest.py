# src/ingest.py

import os
import shutil
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# --- CONFIGURATION DES CHEMINS ---

RAW_DATA_PATH = "data/raw"
MANUALS_PATH = os.path.join(RAW_DATA_PATH, "manuals")
FAQ_PATH = os.path.join(RAW_DATA_PATH, "faq")

# Chemin vers la base de données vectorielle (là où Chroma va stocker les données)
PERSIST_DIRECTORY = "data/vector_db"


# --- CONFIGURATION DU MODÈLE D'EMBEDDING ---

EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200


def load_documents_from_path(directory_path, doc_type):

    logging.info(
        f"Chargement des documents depuis : {directory_path} (Type: {doc_type})")

    loader = PyPDFDirectoryLoader(directory_path)
    documents = loader.load()

    for doc in documents:
        doc.metadata["doc_type"] = doc_type
        # On nettoie le nom du fichier pour le garder en référence
        doc.metadata["source"] = os.path.basename(doc.metadata["source"])

    logging.info(f"Nombre de documents chargés : {len(documents)}")
    return documents


def split_documents(documents):

    logging.info("Démarrage du découpage des documents...")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len
    )

    chunks = text_splitter.split_documents(documents)

    logging.info(f"Nombre total de 'chunks' créés : {len(chunks)}")

    return chunks


def initialize_embeddings():

    logging.info(
        f"Initialisation du modèle d'embedding : {EMBEDDING_MODEL_NAME}")

    model_kwargs = {'device': 'cpu'}
    # Tester plus tard avec True
    encode_kwargs = {'normalize_embeddings': False}

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )
    return embeddings




def create_vector_store(chunks, embeddings):
    # Pré-nettoyage : Supprime l'ancienne base si elle existe
    if os.path.exists(PERSIST_DIRECTORY):
        logging.warning(
            f"Suppression de l'ancienne base de données : {PERSIST_DIRECTORY}")
        shutil.rmtree(PERSIST_DIRECTORY)


    logging.info(
        f"Création de la nouvelle base vectorielle à : {PERSIST_DIRECTORY}")

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=PERSIST_DIRECTORY
    )

    logging.info(
        "Base de données vectorielle créée et persistée avec succès !")
    return vector_store
