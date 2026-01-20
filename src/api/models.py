from pydantic import BaseModel
from typing import List, Optional

# --- Ce que l'utilisateur envoie ---
class ChatRequest(BaseModel):
    message: str  # La question de l'utilisateur

# --- Ce que l'API renvoie ---

class Source(BaseModel):
    file_name: str
    score: float

class ChatResponse(BaseModel):
    response: str       # La réponse générée par Gemini
    sources: List[Source] # La liste des preuves (transparence)