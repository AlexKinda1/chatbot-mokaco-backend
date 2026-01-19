import sys
# On ajoute le dossier courant au chemin pour que Python trouve nos modules 'src'
sys.path.append(".") 
import logging
from src.ingestion.pipeline import run_ingestion
from src.engine.loader import get_query_engine

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def main():
    print("=== MOKACO AI CLI ===")
    """""" 
    """"
    try:
       run_ingestion()
       logger.info("Ingestion terminée avec succès.")
    except Exception as e:
       logger.error(f"Erreur lors de l'ingestion : {e}")
    """
        
    try:
        engine = get_query_engine()
        logger.info("Moteur de requête prêt.")
    except Exception as e:
        logger.error(f"Erreur lors du chargement du moteur de requête : {e}")
               
    while True:
        user_input = input("\nToi : ")
        if user_input.lower() in ["exit", "quit"]:
            break
            
        # Génération de la réponse
        response = engine.query(user_input)
        print(f"MOKACO : {response}")

if __name__ == "__main__":
    main()