# cost_calculator/core.py

from .models import get_model_info
from .counters import get_counter

# Função principal para calcular o custo de entrada
def calculate_input_cost(model_name: str, prompt: str) -> tuple[float, int, str]:
    """
    Calcula o custo estimado e as unidades (tokens/caracteres) para um prompt de entrada,
    dado o nome do modelo.

    Args:
        model_name (str): O nome do modelo (e.g., 'gpt-4o', 'claude-3-haiku-20240307').
        prompt (str): O texto do prompt de entrada.

    Returns:
        tuple[float, int, str]: Uma tupla contendo o custo estimado (float),
                                o número de unidades contadas (int),
                                e o tipo de unidade ('token' ou 'char').

    Raises:
        ValueError: Se o modelo não for encontrado ou não for suportado.
    """
    # Obtém informações do modelo usando a função atualizada
    model_info = get_model_info(model_name)
    if not model_info:
        # get_model_info já loga o erro, apenas levantamos a exceção
        raise ValueError(f"Modelo '{model_name}' não encontrado ou informações inválidas.")

    # Extrai informações necessárias
    tokenizer_name = model_info.get("tokenizer")
    input_cost_per_unit = model_info.get("input_cost_per_token", 0.0) # Usar custo por token como padrão
    unit_type = "token" # Assume token por padrão
    tiktoken_model_ref = model_info.get("tiktoken_model") # Necessário para TiktokenCounter

    # Ajusta se for baseado em caracteres
    if tokenizer_name == "google_char_based":
        unit_type = "char"

    # Obtém o contador apropriado
    try:
        counter = get_counter(tokenizer_name=tokenizer_name, tiktoken_model_ref=tiktoken_model_ref)
    except ValueError as e:
        raise ValueError(f"Erro ao obter contador para {model_name} (tokenizer: {tokenizer_name}): {e}")

    # Conta as unidades
    units = counter.count_units(prompt)

    # Calcula o custo
    cost = units * input_cost_per_unit

    return cost, units, unit_type

# TODO: Implementar calculate_output_cost quando necessário.
# def calculate_output_cost(model_name: str, completion: str) -> tuple[float, int, str]:
#     ...