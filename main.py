# main.py

import click
import json # Usaremos para listar modelos de forma bonita
from cost_calculator.core import calculate_input_cost
from cost_calculator.models import get_supported_models

# Cria um grupo de comandos principal
@click.group()
def cli():
    """
    Calculadora de Custo de Prompt CLI (Fase 1: Estimativa de Input)

    Estima o custo de INPUT para prompts em diferentes LLMs.
    NÃO faz chamadas de API reais e NÃO calcula custo de output.
    """
    pass

# Comando para calcular o custo
@cli.command()
@click.option('--provider', required=True, type=click.Choice(list(get_supported_models().keys()), case_sensitive=False), help='Provedor do LLM (ex: openai, anthropic, google).')
@click.option('--model', required=True, type=str, help='Nome exato do modelo (ex: gpt-4-turbo, claude-3-haiku-20240307).')
@click.option('--prompt', required=True, type=str, help='O texto do prompt a ser avaliado.')
def calculate(provider: str, model: str, prompt: str):
    """Calcula o custo estimado de INPUT para o prompt fornecido."""
    provider = provider.lower() # Garante minúsculas para consistência
    try:
        unit_count, cost, unit_type = calculate_input_cost(provider, model, prompt)

        click.echo("\n--- Estimativa de Custo de Input ---")
        click.echo(f"Provedor: {provider}")
        click.echo(f"Modelo: {model}")
        click.echo(f"Unidades ({unit_type}): {unit_count}")
        # Formata o custo para exibir em USD com várias casas decimais
        click.echo(f"Custo Estimado (Input): ${cost:.6f} USD")
        click.echo("----------------------------------")
        if "estimated" in unit_type or provider != "openai":
             click.secho("AVISO: A contagem de unidades para este provedor/modelo pode ser uma ESTIMATIVA.", fg='yellow')
             click.secho("O custo real baseado na tokenização oficial do provedor pode variar.", fg='yellow')


    except ValueError as e:
        click.secho(f"Erro de Validação: {e}", fg='red')
    except RuntimeError as e:
        click.secho(f"Erro Inesperado: {e}", fg='red')
    except Exception as e:
        click.secho(f"Erro desconhecido: {e}", fg='red')

# Comando para listar modelos suportados
@cli.command(name="list-models")
def list_models():
    """Lista todos os provedores e modelos suportados pela ferramenta."""
    models = get_supported_models()
    click.echo("\n--- Modelos Suportados (Fase 1: Custo de Input) ---")
    # Usa json.dumps para uma formatação bonita do dicionário
    click.echo(json.dumps(models, indent=2))
    click.echo("--------------------------------------------------")
    click.secho("Lembrete: Preços são exemplos e podem estar desatualizados.", fg='cyan')
    click.secho("Contagem de unidades para não-OpenAI pode ser estimada.", fg='cyan')


# Ponto de entrada principal para executar a CLI
if __name__ == '__main__':
    cli()