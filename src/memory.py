docsearch = vector
def qa():
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