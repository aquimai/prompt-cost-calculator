# tests/test_core.py

import pytest
from cost_calculator.core import calculate_input_cost
from cost_calculator.models import get_model_info, get_supported_models

# Test cases: model_name, text, expected_tokens, expected_cost, expected_unit
# Os custos esperados agora serão calculados dinamicamente dentro do teste
# para usar os valores de input_cost_per_token do JSON.
TEST_DATA_INPUT = [
    # Cenário OpenAI GPT-3.5 Turbo (usando tiktoken)
    ("gpt-3.5-turbo", "Olá mundo!" * 10, 40), # 4 tokens por "Olá mundo!", 10x
    # Cenário Anthropic Claude 3 Haiku (usando aproximação tiktoken cl100k_base)
    # Nota: A contagem exata pode variar ligeiramente vs contador oficial Anthropic
    ("claude-3-haiku-20240307", "This is a test sentence." * 5, 26), # 5.2 tokens por sentença, 5x
    # Cenário Google Gemini (usando contagem de caracteres)
    ("gemini-1.5-pro", "Testando 123.", 13), # 13 caracteres
    # Teste com texto vazio
    ("gpt-4o", "", 0),
    # Teste com modelo não suportado diretamente pelo get_model_info (deve falhar)
    # ("modelo-inexistente", "abc", None), # Adicionado um teste específico para isso
]

@pytest.mark.parametrize("model_name, text, expected_tokens", TEST_DATA_INPUT)
def test_calculate_input_cost(model_name, text, expected_tokens):
    """Testa o cálculo do custo de entrada para diferentes modelos e textos."""
    model_info = get_model_info(model_name)
    assert model_info is not None, f"Informações para o modelo {model_name} não encontradas."

    # Calcula o custo esperado dinamicamente
    expected_cost = expected_tokens * model_info.get("input_cost_per_token", 0.0)
    expected_unit = "token" if model_info.get("tokenizer") != "google_char_based" else "char"

    cost, tokens, unit = calculate_input_cost(model_name=model_name, prompt=text)

    assert tokens == expected_tokens, f"Falha para {model_name}: Contagem de tokens esperada {expected_tokens}, obtida {tokens}"
    # Usar isclose para comparar floats
    assert pytest.approx(cost) == expected_cost, f"Falha para {model_name}: Custo esperado {expected_cost}, obtido {cost}"
    assert unit == expected_unit, f"Falha para {model_name}: Unidade esperada {expected_unit}, obtida {unit}"

def test_calculate_cost_unsupported_model():
    """Testa o cálculo de custo para um modelo não suportado."""
    with pytest.raises(ValueError, match="Modelo 'modelo-inexistente' não encontrado"): # Verifica a mensagem de erro
        calculate_input_cost(model_name="modelo-inexistente", prompt="teste")

def test_get_supported_models():
    """Testa se a função get_supported_models retorna uma lista de strings."""
    models = get_supported_models()
    assert isinstance(models, list)
    assert all(isinstance(model, str) for model in models)

    # Verifica se alguns modelos esperados estão na lista (após carregamento)
    assert "gpt-4o" in models
    assert "claude-3-5-sonnet-20240620" in models # Ajuste o nome se necessário
    assert "gemini/gemini-1.5-pro-latest" in models
