import os
import logging
from langchain_ollama import ChatOllama
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

PERSIST_DIRECTORY = "data/vector_db"
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

def main():
    logging.info("Démarrage du chatbot Mokaco...")

    try:
        llm = ChatOllama(model="gemma3:4b", temperature=0.3)
        
        logging.info("Connecté au LLM Ollama (Mistral).")

    except Exception as e:
        logging.error(f"Erreur de connexion à Ollama. As-tu lancé 'ollama pull mistral' et Ollama est-il en cours d'exécution ? Erreur: {e}")
        return

    # --- 2. Initialiser le Modèle d'Embedding (Le "Vectoriseur" de question) ---
    logging.info(f"Chargement du modèle d'embedding: {EMBEDDING_MODEL_NAME}")

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME,
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': False}
    )

    # --- 3. Charger la Base Vectorielle (La "Bibliothèque") ---
    logging.info(f"Chargement de la base vectorielle depuis: {PERSIST_DIRECTORY}")
    if not os.path.exists(PERSIST_DIRECTORY):
        logging.error(f"Le dossier de la base vectorielle n'existe pas: {PERSIST_DIRECTORY}. As-tu lancé ingest.py d'abord ?")
        return
        
    vector_store = Chroma(
        persist_directory=PERSIST_DIRECTORY,
        embedding_function=embeddings
    )

    # --- 4. Initialiser le Retriever (Le "Chercheur") ---

    retriever = vector_store.as_retriever(search_kwargs={"k": 4})
    logging.info("Retriever initialisé (k=4 chunks).")

    # --- 5. Définition du Prompt Template (Les "Instructions" du Bot) ---
    
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

    # --- 6. Construction de la Chaîne RAG (Le "Pipeline") ---

    # Fonction pour formater le contexte (les chunks récupérés)
    def format_context(docs):
        # On combine le contenu des 4 chunks en un seul bloc de texte
        # On inclut aussi la source pour que le bot puisse la citer
        return "\n\n".join(f"Source: {doc.metadata.get('source', 'N/A')}\nContenu: {doc.page_content}" for doc in docs)

    # Voici le pipeline :
    rag_chain = (
        {"context": retriever | format_context, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    logging.info("Chaîne RAG construite avec succès.")

    # --- 7. Lancement de la boucle de chat ---
    print("\n--- Chatbot Mokaco v1.0 (local/Mistral) ---")
    print("Votre base de connaissances est chargée. Posez vos questions.")
    print("(Tapez 'quit' ou 'exit' pour quitter)")

    while True:
        try:
            # Obtenir la question de l'utilisateur
            query = input("\nVous: ")
            
            if query.lower() in ["quit", "exit", "quitter"]:
                logging.info("Arrêt du chatbot.")
                break
            
            if not query.strip():
                continue

            logging.info(f"Question reçue: {query}")
            
            # 1. Invoquer la chaîne RAG
            # La question (query) est envoyée à l'entrée de la chaîne
            print("MokaBot: (Réflexion en cours...)")
            answer = rag_chain.invoke(query)
            
            # 2. Afficher la réponse
            print(f"MokaBot: {answer}")

        except KeyboardInterrupt:
            logging.info("Arrêt forcé par l'utilisateur.")
            break
        except Exception as e:
            logging.error(f"Une erreur est survenue pendant le chat: {e}")
            print("MokaBot: Oups, j'ai rencontré une erreur interne. Veuillez réessayer dans quelques minutes.")

# Point d'entrée du script (rappel)
if __name__ == "__main__":
    main()

