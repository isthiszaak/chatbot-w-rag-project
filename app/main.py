from .src import vector_store
from .llm import llm_handler, qa_chain

def run():
    """
    Initializes the RAG components and starts an interactive command-line session.
    """

    # 1. Fluxo de execução do Vector Store (execução única por início de aplicação)
    print("Loading vector store...")
    db = vector_store.setup_vector_store()

    # 2. Instanciando o modelo LLM
    print("Loading LLM...")
    llm = llm_handler.load_llm()

    # 3. Instanciando chain de acesso ao Vector Store
    print("Creating QA chain...")
    chain = qa_chain.create_qa_chain(llm=llm, vector_store=db)

    print("\n--- RAG Chatbot is Ready (Terminal Mode) ---")
    print("Type 'exit' or 'quit' to end the session.")
    
    # Este loop agora está DENTRO da função, com acesso a 'chain'
    while True:
        # 1. A entrada do usuário é CAPTURADA na variável 'query'
        query = input("\nAsk a question: ")

        # 2. A mesma variável 'query' é usada para a condição de saída
        if query.lower() in ["exit", "quit"]:
            print("Exiting session.")
            break
        
        if not query.strip():
            continue

        try:
            print("Thinking...")
            # 3. A MESMA variável 'query' é usada para invocar o chatbot
            response = chain.invoke({"query": query})
            
            print("\n--- Answer ---")
            # print("Full response: ", response)
            print(response['result'])
            
            print("\n--- Sources ---")
            unique_sources = set(doc.metadata.get('source', 'N/A') for doc in response['source_documents'])
            for source in unique_sources:
                print(f"- {source}")

        except Exception as e:
            print(f"An error occurred: {e}")

# Este bloco executa a função que contém TODA a nossa lógica
if __name__ == "__main__":
    run()