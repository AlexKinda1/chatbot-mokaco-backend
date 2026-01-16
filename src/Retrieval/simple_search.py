import os
import sys
from dotenv import load_dotenv
import logging
from llama_index.core import VectorStoreIndex, StorageContext, Settings
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

# Importations Google
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from llama_index.llms.google_genai import GoogleGenAI

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)
# 1. Charger les secrets
load_dotenv()

def run_search():

    # 2. Configuration (Indispensable pour que ça marche)
    try:
        # A. L'Embedding (DOIT être le même que pour l'ingestion)
        Settings.embed_model = GoogleGenAIEmbedding(model="models/text-embedding-004")
        
        logger.info("Chargement du modèle Gemini...")
        Settings.llm = GoogleGenAI(model="models/gemini-2.5-flash")
        
    except Exception as e:
        logger.error(f"Erreur Config: {e}")
        return

    # 3. Connexion à la mémoire existante (Qdrant)
    logger.info("Connexion à la mémoire Qdrant...")
    client = QdrantClient(url=os.getenv("QDRANT_URL"))
    vector_store = QdrantVectorStore(client=client, collection_name="mokaco_manuals")
    
    # On charge l'index SANS ré-ingérer les documents (on utilise ce qui existe déjà)
    index = VectorStoreIndex.from_vector_store(vector_store=vector_store)

    # 4. Le Moteur de Recherche (Query Engine)
    # similarity_top_k=3 signifie "Trouve-moi les 3 meilleurs passages du manuel"
    query_engine = index.as_query_engine(similarity_top_k=3)

    # 5. Pose ta question ici !
    # Change cette phrase pour tester ton propre manuel
    question = "Comment détartrer la machine ?" 
    
    print(f"❓ Question : {question}")
    print("🔎 Recherche dans les manuels et réflexion...")
    
    try:
        response = query_engine.query(question)
        
        print("\n" + "="*30)
        print(" RÉPONSE DU CHATBOT :")
        print("="*30)
        print(response)
        print("="*30 + "\n")
        
        # Afficher les sources utilisées (Preuve qu'il ne ment pas)
        print(" Sources utilisées :")
        for node in response.source_nodes:
            print(f"- [Score: {node.score:.2f}] {node.text[:100]}...") # Affiche les 100 premiers caractères
            
    except Exception as e:
        print(f" Erreur lors de la génération de la réponse : {e}")

if __name__ == "__main__":
    run_search()