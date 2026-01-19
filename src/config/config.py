import os
import logging
from dotenv import load_dotenv
from llama_index.core import Settings
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding 
from llama_index.llms.google_genai import GoogleGenAI
from config.params import TEMPERATURE

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

print("Configuration des modèles Gemini")

# 1. Charger les variables d'environnement une bonne fois pour toutes
load_dotenv()

def configure_settings():
    """
    Configure les modèles globaux (LLM et Embeddings) pour toute l'application.
    """
    # Vérification de sécurité
    if not os.getenv("GOOGLE_API_KEY"):
        raise ValueError("GOOGLE_API_KEY est manquante dans le fichier .env")
    
    #Configuration du modèle LLM (Le Générateur de texte)
    try:
        Settings.llm = GoogleGenAI(
        model_name="models/gemini-2.5-flash",
        temperature=TEMPERATURE # Faible température pour la précision technique
    )
    except Exception as e:
        logger.error(f"Impossible de charger le LLM Gemini: {e}")   
        

    # Configuration du modèle d'embedding (Le Traducteur sémantique)BENEBO?OBEN
    try:
        Settings.embed_model = GoogleGenAIEmbedding(
        model_name="models/text-embedding-004"
    )
    except Exception as e:
        logger.error(f"Impossible de charger l'embedding Gemini: {e}")
        
    print("Gemini 2.5 Flash + Embedding 004 chargé avec succès")