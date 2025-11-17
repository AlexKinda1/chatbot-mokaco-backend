import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctimes)s')


# Chemin vers les données brutes
RAW_DATA_PATH = "data/raw"

MANUALS_PATH = os.path.join(RAW_DATA_PATH, "manuals")

FAQ_PATH = os.path.join(RAW_DATA_PATH, "faq")

VECTOR_STORE_PATH = "data/vector_db"

# Base de donnée vectorielle
PERSIST_DIRECTORY = "data/vector_db"

# Modelès de LLM
OPEN_AI_LLM =
MIXTRAL_LLM =
IBM_LLM =
LLAMA_LLM =

# Paramétrage
MAX_NEW_TOKENS = 250
TEMPERATURE = 0.3
TOP_P =
TOP_K =
CHUNK_SIZE = 50
CHUNK_OVERSIZE =


def define_template(model):

    template = """
    Tu es "MokaBot", un assistant technique expert pour les machines à café Mokaco. 
    Tu es amical, précis et professionnel.
    
    Réponds à la question de l'utilisateur en te basant UNIQUEMENT sur le contexte suivant :
    
    --- CONTEXTE ---
    {context}
    ---
    
    Question de l'utilisateur : {question}
    
    Règles strictes :
    1. Si le contexte ne contient pas la réponse, dis poliment : "Je suis désolé, je n'ai pas trouvé d'information précise sur ce sujet. Veuillez contacter l'assistance client"
    2. Ne réponds PAS à des questions hors sujet (météo, histoire, etc.). Si la question n'a rien à voir avec Mokaco ou les machines à café, réponds : "Je suis spécialisé dans l'assistance pour les produits Mokaco. Je ne peux pas répondre à cette question."
    3. Cite tes sources si possible, en mentionnant le nom du document (ex: "d'après le manuel machine_A.pdf").
    
    Réponse :
    """

    prompt = ChatPromptTemplate.from_template(template)

    logging.info("Template de prompt défini.")
