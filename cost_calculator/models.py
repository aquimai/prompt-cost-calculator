"""
Define a estrutura de dados para armazenar informações sobre
provedores, modelos e seus custos de INPUT.

IMPORTANTE:
- Os preços são EXEMPLOS e podem estar desatualizados. Pesquise os preços atuais!
- A contagem de unidades para não-OpenAI é uma ESTIMATIVA.
- 'unit': 'token' para OpenAI, 'char' ou 'token_estimated' para outros.
- 'input_price_per_million_units': Preço por 1 MILHÃO de unidades (tokens/chars) de input em USD.
(Usar por milhão facilita lidar com números pequenos).
"""

import json
import os
from typing import Dict, Any, List, Tuple, Optional
import logging

# Configuração do logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Variável global para armazenar os dados carregados
MODEL_DATA: Dict[str, Any] = {}

def _infer_tokenizer(provider: Optional[str], model_name: str) -> Optional[str]:
    """Tenta inferir o nome do tokenizer com base no provedor LiteLLM."""
    if not provider:
        logger.warning(f"Provedor não especificado para o modelo {model_name}, não é possível inferir o tokenizer.")
        return None

    provider_lower = provider.lower()
    # Mapeamento simplificado (pode precisar de ajustes/expansão)
    if provider_lower in ["openai", "azure"]:
        # Tiktoken é geralmente usado para OpenAI/Azure
        # A inferência exata pode depender do modelo específico dentro do tiktoken
        # Usando um fallback genérico por enquanto
        return "tiktoken" # Ou tentar mapear model_name para tiktoken encoding? "gpt-4" é um bom default.
    elif provider_lower == "anthropic":
        return "anthropic_approx_tiktoken"
    # Adicionado 'vertex_ai-language-models' para cobrir o caso do JSON
    elif provider_lower in ["google", "vertex_ai", "vertex_ai-language-models"]:
        # Gemini usa contagem de caracteres como fallback comum
        # TODO: Verificar se o modelo específico usa 'google_generativeai' ou 'google_char_based'
        return "google_char_based"
    elif provider_lower == "mistral":
        # Placeholder - Adicionar lógica se/quando o contador Mistral for implementado
        # return "mistral_bpe_tokenizer"
        logger.warning(f"Contador para Mistral não implementado, usando fallback tiktoken para {model_name}.")
        return "tiktoken" # Fallback temporário
    elif provider_lower == "cohere":
        # Placeholder - Adicionar lógica se/quando o contador Cohere for implementado
        # return "cohere_tokenizer"
        logger.warning(f"Contador para Cohere não implementado, usando fallback tiktoken para {model_name}.")
        return "tiktoken" # Fallback temporário
    elif provider_lower == "groq":
        # Groq usa modelos de outros, a inferência pode ser complexa
        # Ex: llama usa tiktoken, mixtral usa mistral_bpe
        # Simplificando para tiktoken por enquanto
        logger.warning(f"Inferência de tokenizer para Groq simplificada para tiktoken para {model_name}.")
        return "tiktoken"
    # Adicionar outros provedores conforme necessário
    else:
        logger.warning(f"Provedor desconhecido '{provider}' para o modelo {model_name}. Usando fallback tiktoken.")
        return "tiktoken" # Fallback genérico

def _load_model_data() -> Dict[str, Any]:
    """Carrega os dados dos modelos do arquivo JSON."""
    # Constrói o caminho para o arquivo model_data.json relativo a este arquivo
    dir_path = os.path.dirname(os.path.realpath(__file__))
    json_path = os.path.join(dir_path, "model_data.json")

    try:
        with open(json_path, "r") as f:
            data = json.load(f)
            # Remove a entrada 'sample_spec' se existir
            data.pop("sample_spec", None)
            logger.info(f"Dados de {len(data)} modelos carregados de {json_path}")
            return data
    except FileNotFoundError:
        logger.error(f"Erro: Arquivo {json_path} não encontrado.")
        return {}
    except json.JSONDecodeError as e:
        logger.error(f"Erro ao decodificar JSON de {json_path}: {e}")
        return {}
    except Exception as e:
        logger.error(f"Erro inesperado ao carregar {json_path}: {e}")
        return {}

def get_model_info(model_name: str) -> Optional[Dict[str, Any]]:
    """Retorna informações sobre um modelo específico."""
    if not MODEL_DATA:
        logger.error("Dados de modelo não carregados. Verifique o arquivo model_data.json.")
        return None

    model_info = MODEL_DATA.get(model_name)

    if not model_info:
        logger.error(f"Modelo '{model_name}' não encontrado em model_data.json.")
        return None

    # Extrai e adapta os dados necessários
    # Custos por token são usados diretamente
    provider = model_info.get("litellm_provider")
    tokenizer_name = _infer_tokenizer(provider, model_name)

    # Retorna um dicionário com as chaves esperadas pelo resto da aplicação
    # (ou que serão esperadas após refatoração)
    adapted_info = {
        "input_cost_per_token": model_info.get("input_cost_per_token", 0.0),
        "output_cost_per_token": model_info.get("output_cost_per_token", 0.0),
        "max_input_tokens": model_info.get("max_input_tokens"),
        "max_output_tokens": model_info.get("max_output_tokens"),
        "litellm_provider": provider,
        "mode": model_info.get("mode"),
        "tokenizer": tokenizer_name, # Tokenizer inferido
        # Adicionar outros campos relevantes do JSON se necessário
        # "supports_vision": model_info.get("supports_vision", False),
        # "supports_function_calling": model_info.get("supports_function_calling", False),
    }

    # Adiciona o 'tiktoken_model' se o tokenizer for tiktoken, necessário pelo TiktokenCounter
    # Usa o próprio model_name como referência para tiktoken, pode precisar de ajuste
    if tokenizer_name == "tiktoken":
        adapted_info["tiktoken_model"] = model_name

    return adapted_info

def get_supported_models() -> List[str]:
    """Retorna uma lista dos nomes dos modelos suportados."""
    if not MODEL_DATA:
        logger.warning("Nenhum dado de modelo carregado.")
        return []
    # Retorna as chaves do dicionário (nomes dos modelos)
    return list(MODEL_DATA.keys())

# Carrega os dados do modelo na inicialização do módulo
MODEL_DATA = _load_model_data()