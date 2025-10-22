import os
import shutil
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import logging

RAW_DATA_PATH = "data/raw"

MANUALS_PATH = os.path.join(RAW_DATA_PATH, "manuals")
FAQ_PATH = os.path.join(RAW_DATA_PATH, "faq")

EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2" 

CHUNK_SIZE=1000
CHUNK_OVERLAP=200

 # Tester avec PyMuPDFLoader et UnstructuredIO

def load_documents_from_path(directory_path, doc_type):
    logging.info(f"Chargement des documents depuis : {directory_path} (Type: {doc_type})")
    # PyPDFDirectoryLoader charge tous les PDF d'un coup
    loader = PyPDFDirectoryLoader(directory_path)

    documents = loader.load()

    for doc in documents:
        doc.metadata["doc_type"] = doc_type
        # On nettoie le nom du fichier pour le garder en référence
        doc.metadata["source"] = os.path.basename(doc.metadata["source"])
        
    logging.info(f"Nombre de documents chargés : {len(documents)}")
    print(f"Documents chargés : {len(documents)}")
    return documents

def split_document(documents):
    logging.info("Démarrage du découpage des documents...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    chunks = splitter.split_documents(documents)
    print(f"Nombre total de 'chunks' créés : {len(chunks)}")
    return chunks

manual_docs = load_documents_from_path(MANUALS_PATH, doc_type="manual")

chunks_manual_docs=split_document(manual_docs)
print(chunks_manual_docs[:2])
    
    # 2. Charger la FAQ
#faq_docs = load_documents_from_path(FAQ_PATH, doc_type="faq")