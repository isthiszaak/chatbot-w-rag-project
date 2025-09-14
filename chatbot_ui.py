import streamlit as st

from app.src import vector_store
from app.llm import llm_handler, qa_chain

# --- Configuração da Página Streamlit ---
st.set_page_config(
    page_title="RAG Chatbot Local",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Chatbot RAG com Documentos Locais")
st.caption("Faça perguntas sobre os documentos carregados no sistema.")

# --- Cache e Carregamento de Recursos ---

# @st.cache_resource é um decorador que armazena em cache o resultado da função.
# Isso garante que o LLM e o banco de dados vetorial sejam carregados apenas uma vez.
@st.cache_resource
def load_resources():
    """Carrega os recursos pesados (LLM e Vector Store) e os armazena em cache."""
    print("Executando load_resources: Carregando modelos e banco de dados...")
    db = vector_store.setup_vector_store()
    llm = llm_handler.load_llm()
    # Retornamos a "chain" pronta para uso, pois ela depende do db e do llm.
    chain = qa_chain.create_qa_chain(llm=llm, vector_store=db)
    return chain

# Carrega a cadeia RAG na inicialização da aplicação
try:
    chain = load_resources()
except Exception as e:
    st.error(f"Erro ao carregar os recursos: {e}")
    st.stop()


# --- Gerenciamento do Histórico de Chat ---

# st.session_state permite que o Streamlit mantenha o estado entre as re-execuções.
# Vamos usá-lo para armazenar o histórico do chat.
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Olá! Como posso ajudar com seus documentos hoje?"}]

# Exibe as mensagens do histórico
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Entrada do Usuário e Resposta do Chatbot ---

# st.chat_input cria um campo de entrada de texto fixo na parte inferior da tela.
if prompt := st.chat_input("Qual é a sua pergunta?"):
    # Adiciona a mensagem do usuário ao histórico e a exibe
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Gera e exibe a resposta do assistente
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Pensando...")
        try:
            # Chama a cadeia RAG para obter a resposta
            response = chain.invoke({"question": prompt})
            
            # Formata a resposta com o resultado e as fontes
            full_response = response['answer']
            
            source_docs = response.get('source_documents')
            if source_docs:
                full_response += "\n\n**Fontes:**"
                # Usamos um set para evitar fontes duplicadas
                unique_sources = set(doc.metadata.get('source', 'N/A') for doc in source_docs)
                for source in unique_sources:
                    full_response += f"\n- `{source}`"

            message_placeholder.markdown(full_response)
        except Exception as e:
            full_response = f"Ocorreu um erro: {e}"
            message_placeholder.error(full_response)

    # Adiciona a resposta completa do assistente ao histórico
    st.session_state.messages.append({"role": "assistant", "content": full_response})

