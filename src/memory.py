from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
import logging
from ingest import load_documents_from_path, split_documents, initialize_embeddings, create_vector_store
    
    
def qa():
    #Chargement des documents    
    documents=load_documents_from_path(mettre le bon path)
    logging.info("Documents chargés.")

    #Splitting des documents
    chunks=split_documents(documents)
    logging.info("Documents découpés en chunks.")

    #Initialisation des embeddings
    embeddings_model = initialize_embeddings()
    
    #Créer la base vectorielle
    create_vector_store(all_chunks, embeddings_model)
    
    logging.info("--- INGESTION TERMINÉE ---")
    
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