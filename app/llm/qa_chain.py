from langchain.chains import RetrievalQA

def create_qa_chain(llm, vector_store):
    """
    Crie e retorna uma RetrievalQA chain
    """
    # O retriever é uma interface entre o LLM e o vector store
    retriever = vector_store.as_retriever(search_kwargs={"k": 2})

    # chain = LLM + retriever
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff", 
        retriever=retriever,
        return_source_documents=True # Opcional
    )
    return qa_chain
