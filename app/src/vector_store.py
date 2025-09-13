import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter

from .. import config

# Função para gerar embeddings a partir de modelo HuggingFace
def get_embedding():
    return HuggingFaceEmbeddings(model_name=config.EMBEDDING_MODEL_NAME)

def setup_vector_store():
    """
    Função de criação, checagem e obtenção do Vector Store, a partir de um diretório contendo arquivos.
    """

    # Instancia do modelo de embedding do HuggingFace
    embedding_function = get_embedding() 

    # Checkagem da existência do diretório de vector store já construído
    
    # Se existir:
    if os.path.exists(config.PERSIST_PATH):
        print(f"Vector Store já existe em {config.PERSIST_PATH}. Carregando ...")
        return Chroma(persist_directory=config.PERSIST_PATH, embedding_function=embedding_function)

    # Se não existir
    else:
        print("Criando novo Vector Store ...")

        # 1 - Criação do loader para carregar arquivos
        loader = DirectoryLoader(
            path=config.DOCUMENTS_PATH,
            glob="**/*", # Todos os arquivos
            show_progress=True,
            loader_cls=PyPDFLoader 
            )

        documents = loader.load()

        if not documents:
            print(f"Nenhum documento encontrado no caminho {config.DOCUMENTS_PATH}")

        # 2 - Criação de um spliter (para criar chunks)
        txt_splitter = RecursiveCharacterTextSplitter(
                chunk_size=500,
                chunk_overlap=20,
                length_function=len,
                is_separator_regex=False,        
                )
        
        chunks = txt_splitter.split_documents(documents) # Criação de chunks

        # 3 - Criação dos Embeddings e Vector Store
        print(f"Iniciando a criação de embeddings para {len(chunks)} chucks")
    
        vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=embedding_function, 
            persist_directory=config.PERSIST_PATH,
        )

        print(f"Vector Store criado e armazenado em {config.PERSIST_PATH}")

        return vector_store