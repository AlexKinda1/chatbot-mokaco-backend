<!-- Copilot / AI agent instructions for chatbot-mokaco-backend -->
# Copilot instructions — chatbot-mokaco-backend

Purpose: give an AI coding agent the minimal, concrete knowledge to be productive in this repo.

1) Big picture
- This repo is a small backend for a domain-specific assistant called "MokaBot". It ingests PDFs, creates embeddings, stores them in a Chroma vector DB (`data/vector_db`) and uses a conversational retrieval pattern to answer user questions.
- Major components:
  - `src/ingest.py` — PDF loading, text splitting, embedding initialization, and creation/persistence of the Chroma vector store. This is the canonical ingestion flow.
  - `src/chat.py` — prompt template, LLM client initialization (uses `ChatOllama` if available), and constants like `PERSIST_DIRECTORY` and `EMBEDDING_MODEL_NAME`.
  - `src/memory.py` — intended QA loop using LangChain's `ConversationalRetrievalChain` and `ConversationBufferMemory`. The file currently contains placeholders/undefined names and is not runnable as-is; use `ingest.py` as the source of truth for ingestion logic.
  - `src/params.py` — global parameters and model settings. Many values are placeholders and need to be completed before production use.

2) Key files & examples
- Ingestion flow example (see `src/ingest.py`):
  - Input PDFs directory: `data/raw/manuals` and `data/raw/faq`
  - Embedding model: `sentence-transformers/all-MiniLM-L6-v2` (set in `ingest.py` and `chat.py`)
  - Persisted vector DB: `data/vector_db` (Chroma). `create_vector_store()` removes the old directory before writing a new one.

- Prompt/template: the assistant prompt is defined in `src/chat.py` and repeated in `src/params.py`. Prompts are in French and enforce strict rules (answer from context only, tell user to contact support if not found, cite document source when possible).

3) How to run locally (minimal reproducible steps)
- Create and activate a Python venv, then install dependencies:
  - `python -m venv .venv; .\\.venv\\Scripts\\Activate.ps1; pip install -r requirements.txt`
- Ingest PDFs (from repo root):
  - `python src\\ingest.py`
  - Note: `ingest.py` will look in `data/raw/manuals` and `data/raw/faq` — ensure PDFs are placed there.
- Run a quick interactive QA (there is no reliable `main.py` entrypoint yet):
  - Either adapt `src/chat.py` to create a `ConversationalRetrievalChain` using the persisted Chroma DB, or fix `src/memory.py` placeholders and run `python src\\memory.py`.

4) Project-specific conventions & important gotchas
- Language: prompts, logs and templates are written in French — keep this in mind for prompt edits.
- Paths: the code uses relative paths like `data/raw` and `data/vector_db`. Tests and CI (if added) should run from the repo root.
- Chroma usage: ingestion deletes the `PERSIST_DIRECTORY` before creating a new DB. Do not run ingestion unless you intend to rebuild the vector store.
- Embeddings: `HuggingFaceEmbeddings` is instantiated with `model_kwargs={'device':'cpu'}`; heavy models may need GPU and corresponding `model_kwargs` changes.
- LLM integration: `chat.py` attempts to use `ChatOllama(model="gemma3:4b")`. Verify local LLM availability; fallback handling is currently minimal.

5) Code health signals to look for
- `src/main.py` has syntax errors / broken structure — don't treat it as a runnable entrypoint.
- `src/memory.py` contains pseudo-code and literal placeholders (e.g., `mettre le bon path`, `all_chunks`, `llm_model`, `docsearch` are undefined). Prefer `ingest.py` for ingest logic and `chat.py` for prompt/LLM conventions.
- `src/params.py` contains incomplete constants (empty assignments). Update `params.py` only after confirming desired LLM and hyperparameters.

6) Typical small tasks an agent might perform first
- Wire a working CLI: add a simple `if __name__ == "__main__":` in `src/ingest.py` and `src/chat.py` to expose ingest and a test chat flow.
- Replace placeholders in `src/memory.py` with concrete imports/variables or remove the file until implemented.
- Add simple run scripts or a short README with the exact venv + install + run commands.

7) Tests & CI
- There are no tests in the repo. Keep changes small, and test ingestion locally by placing a few small PDFs in `data/raw/manuals` and running `python src\\ingest.py` to confirm `data/vector_db` is created.

8) When editing — style and safety
- Maintain the French prompt wording and message rules.
- Keep changes minimal and focused: prefer fixing root causes (e.g., undefined names) rather than superficial patches.

If anything here is unclear or you want this file to emphasize a different aspect (CI, security, or specific coding standards), tell me which areas to expand and I'll iterate.
