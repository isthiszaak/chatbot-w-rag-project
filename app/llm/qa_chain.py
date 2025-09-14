from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory

from .prompts import prompt_template

# Carregando prompt completo, incluindo informações de contexto, solicitação do usuário e etc
llm_prompt = PromptTemplate(template=prompt_template, input_variables=["question","chat_history","context"])

def create_qa_chain(llm, vector_store):
    """
    Crie e retorna uma RetrievalQA chain
    """
    # Instanciando a memória da conversa
    memory = ConversationBufferMemory(memory_key="chat_history",return_messages=True)

    # O retriever é uma interface entre o LLM e o vector store
    retriever = vector_store.as_retriever(search_kwargs={"k": 2})

    # chain = LLM + retriever + prompt
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        chain_type="stuff", 
        retriever=retriever,
        memory=memory,
        return_source_documents=False, # Opcional
        combine_docs_chain_kwargs ={"prompt": llm_prompt},
        verbose=False
    )
    return qa_chain
