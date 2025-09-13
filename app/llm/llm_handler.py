from langchain_community.llms import LlamaCpp
from ..utils import config

def load_llm():
    """
    Carrega o modelo LlamaCpp do caminho especificado
    """
    llm = LlamaCpp(
        model_path=config.MODELS_PATH,
        temperature=config.LLM_TEMPERATURE,
        n_ctx=config.LLM_CTX,
        n_gpu_layers=0, # Set to 0 to run on CPU. Change if you have a compatible GPU.
        verbose=False,
    )
    return llm