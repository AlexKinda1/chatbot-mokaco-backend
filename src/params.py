import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctimes)s')


# Chemin vers les données brutes
RAW_DATA_PATH = "data/raw"
MANUALS_PATH = os.path.join(RAW_DATA_PATH, "manuals")
FAQ_PATH = os.path.join(RAW_DATA_PATH, "faq")

#Base de donnée vectorielle
PERSIST_DIRECTORY = "data/vector_db"

#Modelès de LLM
OPEN_AI_LLM= 
MIXTRAL_LLM=
IBM_LLM=
LLAMA_LLM= 

#Paramétrage
MAX_NEW_TOKENS= 250
TEMPERATURE=0.3
TOP_P=
TOP_K=
CHUNK_SIZE=50
CHUNK_OVERSIZE=

#Autres parametres


