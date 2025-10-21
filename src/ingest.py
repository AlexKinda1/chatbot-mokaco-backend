# src/ingest.py

import os
import shutil
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- CONFIGURATION DES CHEMINS ---
# Chemin vers les données brutes
RAW_DATA_PATH = "data/raw"
MANUALS_PATH = os.path.join(RAW_DATA_PATH, "manuals")
FAQ_PATH = os.path.join(RAW_DATA_PATH, "faq")

# Chemin vers la base de données vectorielle (là où Chroma va stocker les données)
PERSIST_DIRECTORY = "data/vector_db"

# --- CONFIGURATION DU MODÈLE D'EMBEDDING ---
# On choisit un modèle d'embedding performant et multilingue (au cas où)
# "all-MiniLM-L6-v2" est rapide et léger.
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# --- CONFIGURATION DU DÉCOUPEUR DE TEXTE ---
# Ces valeurs sont cruciales pour le RAG.
# chunk_size: La taille maximale de nos morceaux de texte (en caractères).
# chunk_overlap: Le nombre de caractères de chevauchement entre deux morceaux
#                pour ne pas perdre le contexte lors de la coupe.
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

def load_documents_from_path(directory_path, doc_type):
    """
    Charge tous les PDF d'un dossier et ajoute un "type" dans les métadonnées.
    """
    logging.info(f"Chargement des documents depuis : {directory_path} (Type: {doc_type})")
    # PyPDFDirectoryLoader charge tous les PDF d'un coup
    loader = PyPDFDirectoryLoader(directory_path)
    documents = loader.load()
    
    # C'est une étape CLÉ : nous "tagguons" chaque document
    # avec sa source (manual vs faq).
    # Cela permettra au bot de filtrer ses recherches.
    for doc in documents:
        doc.metadata["doc_type"] = doc_type
        # On nettoie le nom du fichier pour le garder en référence
        doc.metadata["source"] = os.path.basename(doc.metadata["source"])
        
    logging.info(f"Nombre de documents chargés : {len(documents)}")
    return documents

def split_documents(documents):
    """
    Découpe les documents chargés en petits "chunks".
    """
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
    """
    Initialise le modèle d'embedding depuis HuggingFace.
    """
    logging.info(f"Initialisation du modèle d'embedding : {EMBEDDING_MODEL_NAME}")
    # On spécifie 'cpu' car l'embedding n'a pas besoin d'un gros GPU
    model_kwargs = {'device': 'cpu'}
    encode_kwargs = {'normalize_embeddings': False}
    
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )
    return embeddings

def create_vector_store(chunks, embeddings):
    """
    Crée et persiste la base de données vectorielle ChromaDB.
    """
    
    # Pré-nettoyage : Supprime l'ancienne base si elle existe
    if os.path.exists(PERSIST_DIRECTORY):
        logging.warning(f"Suppression de l'ancienne base de données : {PERSIST_DIRECTORY}")
        shutil.rmtree(PERSIST_DIRECTORY)
        
    logging.info(f"Création de la nouvelle base vectorielle à : {PERSIST_DIRECTORY}")
    
    # Crée la base de données à partir des chunks et du modèle d'embedding
    # 'persist_directory' lui dit où sauvegarder les fichiers sur le disque.
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=PERSIST_DIRECTORY
    )
    
    logging.info("Base de données vectorielle créée et persistée avec succès !")
    return vector_store

def main():
    """
    Fonction principale pour orchestrer l'ingestion.
    """
    logging.info("--- DÉMARRAGE DU SCRIPT D'INGESTION MOKACO ---")
    
    # 1. Charger les manuels
    manual_docs = load_documents_from_path(MANUALS_PATH, doc_type="manual")
    
    # 2. Charger la FAQ
    faq_docs = load_documents_from_path(FAQ_PATH, doc_type="faq")
    
    all_documents = manual_docs + faq_docs
    if not all_documents:
        logging.error("Aucun document trouvé. Vérifiez vos dossiers /data/raw/manuals et /data/raw/faq.")
        return

    # 3. Découper tous les documents
    all_chunks = split_documents(all_documents)
    
    # 4. Initialiser le modèle d'embedding (cela peut prendre du temps la 1ère fois)
    embeddings_model = initialize_embeddings()
    
    # 5. Créer la base vectorielle
    create_vector_store(all_chunks, embeddings_model)
    
    logging.info("--- SCRIPT D'INGESTION TERMINÉ ---")

if __name__ == "__main__":
    main()