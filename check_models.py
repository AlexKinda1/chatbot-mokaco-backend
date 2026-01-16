import os
import json
import logging
import urllib.request
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("GOOGLE_API_KEY pas défini dans les variables d'environnement.")
    exit()
    
url = f"https://generativelanguage.googleapis.com/v1beta2/models?key={api_key}" 

try:
    logger.info("Récupération des modèles depuis l'API Google Generative AI...")
    with urllib.request.urlopen(url) as response:
        data = response.read().decode()
        logger.info("Modèles disponibles depuis l'API Google Generative AI :")
        logger.info(data)
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode())
        logger.info("Modèles disponibles depuis l'API Google Generative AI :")
    
    if 'models' in data:
        for model in data['models']:
            # On ne veut que les modèles qui génèrent du texte (generateContent)
            if "generateContent" in model.get("supportedGenerationMethods", []):
                name = model['name']
                print(f" {name}")
                
                # On cherche celui qu'on veut
                if "gemini-1.5-flash" in name:
                    found_flash = True
    else:
        print(" Bizarre, l'API a répondu mais pas de liste 'models'.")
        print(data)

    print("="*50)
    
except Exception as e:
    print(f"\nERREUR GRAVE : Impossible de contacter Google.")
    print(f"Détail : {e}")
    print("\nCela peut être dû à :")
    print("1. Une mauvaise clé API.")
    print("2. Un blocage géographique (France/Europe).")