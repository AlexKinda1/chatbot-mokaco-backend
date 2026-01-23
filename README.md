# MOKABOT API

MOKABOT est un backend d'chatbot de support technique intelligent pour les machines à café MOKACO. Il utilise un modèle de langage (LLM) de pointe et une base de données vectorielle pour fournir des réponses rapides et précises aux questions des utilisateurs en se basant sur la documentation technique des machines.

## Fonctionnalités

*   **API d'interrogation**: Une API simple à utiliser pour interroger le chatbot.
*   **Ingestion de données**: Un pipeline pour traiter les documents (manuels, guides, etc.) et les stocker dans une base de données vectorielle.
*   **Interface en ligne de commande (CLI)**: Une interface pour interagir avec le chatbot directement depuis le terminal.
*   **Extensible**: Le projet est conçu pour être facilement extensible avec de nouvelles fonctionnalités (par exemple, historique des conversations, évaluation des réponses).
*   **Basé sur les technologies de pointe**: Utilise les modèles Gemini de Google, `llama-index` et Qdrant.

## Architecture

Le projet est basé sur une architecture RAG (Retrieval-Augmented Generation).

1.  **Ingestion de données**: Les documents sont chargés, découpés en morceaux (chunks) et transformés en vecteurs (embeddings) à l'aide d'un modèle d'embedding. Ces vecteurs sont ensuite stockés dans la base de données vectorielle Qdrant.
2.  **Interrogation**: Lorsqu'un utilisateur pose une question, celle-ci est également transformée en vecteur.
3.  **Recherche**: Le système recherche dans Qdrant les morceaux de documents les plus pertinents pour la question de l'utilisateur.
4.  **Génération**: Les morceaux de documents pertinents et la question de l'utilisateur sont envoyés au modèle de langage (LLM), qui génère une réponse en langage naturel.

## Démarrage rapide

### Prérequis

*   Python 3.9+
*   Docker
*   Une clé d'API Google (stockée dans une variable d'environnement `GOOGLE_API_KEY` dans un fichier `.env`)

### Installation

1.  **Clonez le projet :**
    ```bash
    git clone https://github.com/votre-utilisateur/chatbot-mokaco-backend.git
    cd chatbot-mokaco-backend
    ```

2.  **Créez un environnement virtuel et installez les dépendances :**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Sur Windows: .venv\Scripts\activate
    pip install -r requirements.txt
    ```

3.  **Créez un fichier `.env` à la racine du projet et ajoutez votre clé d'API Google :**
    ```
    GOOGLE_API_KEY="VOTRE_CLE_API_GOOGLE"
    ```

4.  **Lancez le service Qdrant avec Docker Compose :**
    ```bash
    docker-compose up -d
    ```

### Utilisation

#### 1. Ingestion des données

1.  Ajoutez vos documents (PDF, etc.) dans le dossier `data/raw`.
2.  Lancez le pipeline d'ingestion :
    ```bash
    python -m src.ingestion.pipeline
    ```
    Cela va traiter les documents, générer les embeddings et les stocker dans Qdrant.

#### 2. Lancement de l'API

Pour démarrer le serveur API :
```bash
uvicorn src.api.app:app --reload
```
Le serveur sera accessible à l'adresse `http://localhost:8000`. Vous pouvez consulter la documentation de l'API (générée par Swagger) à l'adresse `http://localhost:8000/docs`.

Pour envoyer une requête, vous pouvez utiliser `curl` ou tout autre client HTTP :
```bash
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "Comment détartrer ma machine ?"}'
```

#### 3. Utilisation de l'interface en ligne de commande (CLI)

Pour discuter avec le chatbot depuis votre terminal :
```bash
python -m src.cli.main
```

## Structure du projet

```
.
├── docker-compose.yml      # Configuration du service Qdrant
├── requirements.txt        # Dépendances Python
├── src/
│   ├── api/                # Code de l'API FastAPI
│   │   ├── app.py          # Point d'entrée de l'API
│   │   └── models.py       # Modèles de données Pydantic
│   ├── cli/                # Code de l'interface en ligne de commande
│   │   └── main.py         # Point d'entrée de la CLI
│   ├── config/             # Modules de configuration
│   │   ├── configuration.py # Configuration des modèles
│   │   ├── params.py       # Paramètres du projet
│   │   └── prompts.py      # Prompts pour le LLM
│   ├── engine/             # Cœur du moteur du chatbot
│   │   └── loader.py       # Chargement du moteur de chat
│   └── ingestion/          # Scripts pour l'ingestion des données
│       ├── load_data.py    # (Optionnel) Chargement de données spécifiques
│       └── pipeline.py     # Pipeline d'ingestion principal
├── data/
│   └── raw/                # Dossier pour les documents bruts
└── qdrant_data/            # Données de la base de données vectorielle Qdrant
```
