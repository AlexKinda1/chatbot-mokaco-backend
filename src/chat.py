import os
import logging
from ingest import load_documents_from_path, split_documents, initialize_embeddings, create_vector_store
from langchain_ollama import ChatOllama
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

PERSIST_DIRECTORY = "data/vector_db"
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


logging.info("Démarrage")

try:
    llm = ChatOllama(model="gemma3:4b", temperature=0.3)

    logging.info("Connecté au LLM Ollama (Mistral).")

except Exception as e:
    logging.error(f"Erreur de connexion à Ollama: {e}")





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
