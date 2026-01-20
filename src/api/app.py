from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sys
sys.path.append(".")  # Pour que Python trouve nos modules 'src'
from src.api.models import ChatRequest, ChatResponse, Source
from src.engine.loader import get_chat_engine
import uvicorn

# 1. Initialisation de l'application
app = FastAPI(
    title="MOKABOT API",
    description="API de support technique intelligent pour machines à café",
    version="1.0.0"
)

# 2. Configuration CORS (Sécurité)
# Cela permet au futur site web (qui sera sur un autre port) de parler à cette API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # En prod, on mettra l'URL du site MOKACO ici. Pour le dev, "*" accepte tout.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Chargement du Moteur IA au démarrage
# On le charge UNE SEULE FOIS ici pour ne pas recharger le modèle à chaque message (ce serait trop lent)
print(" Démarrage du serveur... Chargement de l'IA...")
chat_engine = get_chat_engine()
print(" IA chargée et prête.")

# Configuration des endpoints

@app.get("/")
def health_check():
    """Simple vérification que le serveur est en vie"""
    return {"status": "online", "service": "Mokaco AI"}

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    """
    Point d'entrée principal pour discuter avec le bot.
    Reçoit un message JSON, renvoie une réponse JSON avec sources.
    """
    try:
        # On interroge le moteur (qui gère déjà la mémoire et le reranking)
        response = chat_engine.chat(request.message)
        
        # On extrait les sources proprement pour le JSON
        sources_data = []
        for node in response.source_nodes:
            sources_data.append(Source(
                file_name=node.metadata.get("file_name", "Inconnu"),
                score=node.score if node.score else 0.0
            ))
            
        return ChatResponse(
            response=response.response,
            sources=sources_data
        )

    except Exception as e:
        # En cas de crash, on renvoie une erreur propre 500
        raise HTTPException(status_code=500, detail=str(e))
    
    """
    Potentiels reqyeuêtes futures à rajouter :
    POST   /api/chat              # Message principal
    GET    /api/chat/history      # Récupérer historique
    POST   /api/chat/feedback     # Évaluation satisfaction
    POST   /api/upload            # Upload fichiers (futures MAJ)
    GET    /api/suggestions       # Questions fréquentes
    POST   /api/appointment       # Prise RDV SAV
    """

# Cette partie permet de lancer le serveur directement via 'python src/api/app.py'
if __name__ == "__main__":
    uvicorn.run("src.api.app:app", host="0.0.0.0", port=8000, reload=True)