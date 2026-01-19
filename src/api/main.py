import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# LlamaIndex
from llama_index.core import VectorStoreIndex, Settings, StorageContext
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

# Google (Version Moderne)
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from llama_index.llms.google_genai import GoogleGenAI

# 1. Initialisation
load_dotenv()
app = FastAPI(title="MOKACO Chatbot API", description="API pour le chatbot RAG")

# Modèle de données pour la requête (ce que le frontend envoie)
class ChatRequest(BaseModel):
    question: str

# Variable globale pour stocker le moteur de recherche
query_engine = None

@app.on_event("startup")
async def startup_event():
    """Cette fonction s'exécute une seule fois au démarrage du serveur"""
    global query_engine
    print("🚀 Démarrage du serveur... Chargement du cerveau IA...")
    
    try:
        # A. Configurer les modèles (Comme dans simple_search.py)
        Settings.embed_model = GoogleGenAIEmbedding(model="models/text-embedding-004")
        
        # On ajoute un "system_prompt" pour forcer le français
        Settings.llm = GoogleGenAI(
            model="models/gemini-2.5-flash", # Ou gemini-2.5-flash selon ce qui marche pour toi
            system_prompt="Tu es un assistant expert pour les machines à café MOKACO. Tu réponds toujours en FRANÇAIS. Sois courtois, précis et utilise le contexte fourni pour répondre."
        )

        # B. Connexion Qdrant
        client = QdrantClient(url=os.getenv("QDRANT_URL"))
        vector_store = QdrantVectorStore(client=client, collection_name="mokaco_manuals")
        
        # C. Chargement de l'index
        index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
        
        # D. Création du moteur
        query_engine = index.as_query_engine(similarity_top_k=3)
        print("✅ API Prête à répondre !")
        
    except Exception as e:
        print(f"❌ Erreur critique au démarrage : {e}")

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    """L'endpoint que le site web va appeler"""
    if not query_engine:
        raise HTTPException(status_code=503, detail="Le moteur IA n'est pas prêt.")
    
    try:
        print(f"📩 Question reçue : {request.question}")
        response = query_engine.query(request.question)
        
        # On prépare la réponse propre
        return {
            "response": str(response),
            "sources": [node.text[:200] + "..." for node in response.source_nodes]
        }
    except Exception as e:
        print(f"❌ Erreur pendant la réponse : {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"status": "MOKABOT is running", "doc": "Go to /docs to test"}