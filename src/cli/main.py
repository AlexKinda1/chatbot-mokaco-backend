import sys
# On ajoute le dossier courant au chemin pour que Python trouve nos modules 'src'
sys.path.append(".") 
import logging
from src.ingestion.pipeline import run_ingestion
from src.engine.loader import get_chat_engine

# Configuration du logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Fonction utilitaire pour formater les sources
def format_sources(response):
    text = "\n Sources consultées :\n"
    for node in response.source_nodes:
        file_name = node.metadata.get('file_name', 'Inconnu')
        score = node.score if node.score else 0.0
        text += f"- {file_name} (Pertinence : {score:.2f})\n"
    return text


def main():
    print("=== MOKACO AI CLI ===")
    
    # Attention: Si l'ingestion doit être relancée, décommentez ce bloc
    # Bloc d'ingestion des données
    """"
    try:
       run_ingestion()
       logger.info("Ingestion terminée avec succès.")
    except Exception as e:
       logger.error(f"Erreur lors de l'ingestion : {e}")
    """
        
    # Chargement du moteur de chat
    try:
        chat_engine = get_chat_engine()
        logger.info("Moteur de chat prêt.")
    except Exception as e:
        logger.error(f"Erreur lors du chargement du moteur de chat : {e}")
        
    # Boucle principale d'interaction           
    while True:
        user_input = input("\nToi : ")
        if user_input.lower() in ["exit", "quit"]:
            break
            
        # Génération de la réponse 
        response = chat_engine.chat(user_input)
        
        print(f"\nMOKACO : {response.response}")
        print(format_sources(response))

if __name__ == "__main__":
    main()