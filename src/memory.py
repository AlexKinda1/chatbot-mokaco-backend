from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from ingest import load_documents_from_path, split_documents, initialize_embeddings, create_vector_store



    logging.info("--- DÉMARRAGE DU SCRIPT D'INGESTION ---")
    
    # 1. Charger les manuels
    manual_docs = load_documents_from_path(MANUALS_PATH, doc_type="manual")
    
    # 2. Charger la FAQ
    faq_docs = load_documents_from_path(FAQ_PATH, doc_type="faq")
    
    all_documents = manual_docs + faq_docs
    if not all_documents:
        logging.error("Aucun document trouvé. Vérifiez vos dossiers /data/raw/manuals et /data/raw/faq.")
        return

    # 3. Découper tous les documents
    all_chunks = split_documents(all_documents)
    
    # 4. Initialiser le modèle d'embedding (cela peut prendre du temps la 1ère fois)
    embeddings_model = initialize_embeddings()
    
    # 5. Créer la base vectorielle
    create_vector_store(all_chunks, embeddings_model)
    
    logging.info("--- SCRIPT D'INGESTION TERMINÉ ---")


def qa():
    #Chargement des documents    
    documents=load_documents_from_path(mettre le bon path)
    logging.info("Documents chargés.")

    #Splitting des documents
    chunks=split_documents(documents)
    logging.info("Documents découpés en chunks.")

    #Initialisation des embeddings
    
    
    
    history=[]
    
    memory=ConversationBufferMemory(memory_key="chat_history", return_messages=False)
    
    qa=ConversationalRetrievalChain.from_llm(
                                           llm=llm_model,
                                           retriever=docsearch.as_retriever(),
                                           chain_type="stuff",
                                           memory=memory,
                                           get_chat_history=lambda h :h,
                                           return_source_documents=False)
    
    
    while True:

        query = input("Question:")

        if query.lower in ["quit", "exit"]:
             print("Answer: Goodbye")
             break
        
        result=qa({"question": query}, {"chat_history": history})

        history.append((query, result["answer"]))

        print("Answer:", result["answer"])
        
qa()