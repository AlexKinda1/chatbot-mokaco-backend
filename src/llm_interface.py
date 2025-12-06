from llama_index.llms.ibm import WatsonxLLM
import os

def define_llm():
    """Définit et retourne une instance de WatsonxLLM avec les paramètres appropriés."""
    ibm_api_key = os.getenv("IBM_API_KEY", "votre