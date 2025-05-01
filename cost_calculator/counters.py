import tiktoken
from abc import ABC, abstractmethod

class BaseCounter(ABC):
    @abstractmethod
    def count_units(self, text: str) -> int:
        """Conta as unidades (tokens, caracteres, etc.) no texto."""
        pass


class TiktokenCounter(BaseCounter):
    """Contador de tokens para modelos compatíveis com tiktoken (ex: OpenAI GPTs)."""
    def __init__(self, model_name: str):
        try:
            self.encoding = tiktoken.encoding_for_model(model_name)
        except KeyError:
            # Fallback para um encoding comum se o modelo exato não for encontrado
            print(f"Aviso: Encoding exato para '{model_name}' não encontrado no tiktoken. Usando 'cl100k_base'. A contagem pode ser ligeiramente imprecisa.")
            self.encoding = tiktoken.get_encoding("cl100k_base")

    def count_units(self, text: str) -> int:
        """Conta os tokens usando o encoding do tiktoken."""
        return len(self.encoding.encode(text))


# Renomeado e modificado para usar tiktoken cl100k_base como aproximação para Fase 1
class AnthropicTiktokenApproxCounter(BaseCounter):
    """Contador APROXIMADO para modelos Anthropic Claude (Fase 1) usando cl100k_base do tiktoken."""
    def __init__(self):
        # A codificação cl100k_base é uma boa aproximação para modelos Claude.
        # Esta é uma ESTIMATIVA para a Fase 1.
        self.encoding = tiktoken.get_encoding("cl100k_base")
        # Opcional: Adicionar aviso se desejar
        # print("Aviso: Usando tiktoken 'cl100k_base' como APROXIMAÇÃO para contagem de tokens Anthropic.")

    def count_units(self, text: str) -> int:
        """Conta os tokens usando cl100k_base como aproximação para Anthropic."""
        return len(self.encoding.encode(text))


class GoogleCharCounter(BaseCounter):
    """Contador de caracteres para modelos Google (Fase 1 - ESTIMATIVA)."""
    def count_units(self, text: str) -> int:
        """Conta caracteres como estimativa para Google na Fase 1."""
        # Nota: Verificar documentação do Google se a contagem de caracteres
        # é a melhor estimativa para os modelos desejados na Fase 1.
        return len(text)


def get_counter(
    tokenizer_name: str,
    tiktoken_model_ref: str | None = None,
) -> BaseCounter:
    """
    Retorna a instância do contador apropriado com base no nome (Fase 1).

    Contadores suportados na Fase 1:
    - 'tiktoken': Para modelos OpenAI (requer tiktoken_model_ref).
    - 'anthropic_approx_tiktoken': Aproximação para Anthropic usando tiktoken.
    - 'google_char_based': Contagem de caracteres como estimativa para Google.

    Args:
        tokenizer_name (str): O nome do tokenizador/contador a ser usado.
        tiktoken_model_ref (str | None): Nome do modelo tiktoken (obrigatório se tokenizer_name='tiktoken').

    Returns:
        BaseCounter: Uma instância da classe de contador apropriada.

    Raises:
        ValueError: Se um contador desconhecido for solicitado ou se os parâmetros necessários estiverem faltando.
    """
    if tokenizer_name == "tiktoken":
        if not tiktoken_model_ref:
            raise ValueError("Referência de modelo tiktoken ('tiktoken_model_ref') necessária para o contador tiktoken.")
        return TiktokenCounter(model_name=tiktoken_model_ref)
    elif tokenizer_name == "anthropic_approx_tiktoken":
        return AnthropicTiktokenApproxCounter()
    elif tokenizer_name == "google_char_based":
        return GoogleCharCounter()
    # Removido bloco elif para 'google_vertex_token'
    else:
        # Lista explícita de contadores suportados na mensagem de erro
        supported = ["tiktoken", "anthropic_approx_tiktoken", "google_char_based"]
        raise ValueError(f"Tipo de contador desconhecido: '{tokenizer_name}'. Suportados na Fase 1: {supported}")