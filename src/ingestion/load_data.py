import os
import sys 
import logging
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, Settings
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding 
from llama_index.llms.google_genai import GoogleGenAI
from qdrant_client import QdrantClient
from config.params import EMBEDDING_MODEL, RAW_DATA_PATH 

# Configuration du logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

#Chargement des secrets
load_dotenv()

if not os.getenv("GOOGLE_API_KEY"):
    logger.error("GOOGLE_API_KEY est inexistant. Définir la clé dans variable d'environnement.")
    sys.exit(1)

#Ingestion des documents
def ingest_docs():
    try: 
        #Chargement et configuration des modèles d'embeddding et llm")
        Settings.embed_model = GoogleGenAIEmbedding(model="models/text-embedding-004")
        logger.info("Modèle d'embedding chargé")
              
        Settings.llm = GoogleGenAI(model="models/gemini-2.5-flash")
        logger.info("Modèle LLM chargé")

        # 2. Lecture des documents depuis le répertoire 'data/raw'
        input_dir = RAW_DATA_PATH
        
        if not os.path.exists(input_dir):
            logger.error(f"le dossier {input_dir}n'existe pas.")
            return 
        
        logger.info(f"Lecture des documents depuis le répertoire : {input_dir}")
        reader = SimpleDirectoryReader(input_dir)
        documents = reader.load_data()
        logger.info(f"{len(documents)} documents chargés.")
        
        # 3. Connexion à Qdrant
        qdranturl = os.getenv("QDRANT_URL")
        if not qdranturl:
            logger.error("QDRANT_URL est inexistant. Définir l'URL dans variable d'environnement '.env'.")
            return
        
        logger.info("Connexion à Qdrant...")
        
        try:
            client = QdrantClient(url=qdranturl)
        except Exception as e:
            logger.error(f"Erreur lors de la connexion à Qdrant : {e}")
            return
        logger.info("Connexion à Qdrant réussie.")
        
        # 4. Création du vector store dans Qdrant
        vector_store = QdrantVectorStore(client=client, collection_name="mokaco_manuals") # Nom de la collection Qdrant
        
        storage_context = StorageContext.from_defaults(vector_store=vector_store) # Utilisation du vector store Qdrant pour le stockage des vecteurs
        
        #5. Indexation des documents
        logger.info("Creation de l'index et  vectorisation") 
        try:
            index = VectorStoreIndex.from_documents(
                documents,
                storage_context=storage_context
            )
            logger.info("Index créé avec succès.")
        except Exception as e:
            logger.error(f"Erreur lors de la création de l'index : {e}")
            return
        
        logger.info("Indexation et vectorisation terminées.")
        print("Données ingérées et indexées avec succès dans Qdrant.")
    except Exception as e:
        logger.error(f"Erreur lors de l'ingestion des documents : {e}")
        
#Utiliser le Query Engine pour interroger l'index ?        

if __name__ == "__main__":
    ingest_docs()