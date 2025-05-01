# Prompt Cost Calculator CLI

Uma ferramenta de linha de comando (CLI) simples para **estimar o custo de INPUT (prompt)** ao usar diferentes modelos de linguagem grandes (LLMs) de provedores como OpenAI, Anthropic e Google.

**Desenvolvido como um projeto open source pela [Nome da Sua Empresa - Aquim.ai] ([Link para Aquim.ai])** para ajudar a comunidade a entender melhor os custos associados aos prompts.

**IMPORTANTE:**
*   Esta ferramenta **estima APENAS o custo de INPUT**. Ela **NÃO** calcula o custo de OUTPUT (completion).
*   Ela **NÃO** faz chamadas reais às APIs dos LLMs.
*   Ela **NÃO** requer chaves de API.
*   A contagem de unidades (tokens/caracteres) para provedores **não-OpenAI** pode ser uma **ESTIMATIVA** baseada em métodos como contagem de caracteres, pois bibliotecas de tokenização oficiais podem não estar disponíveis publicamente ou serem fáceis de integrar. O custo real pode variar.
*   Os preços dos modelos são baseados em dados públicos no momento do desenvolvimento e **podem ficar desatualizados**. Verifique sempre a documentação oficial do provedor para os preços mais recentes.

## Instalação

Certifique-se de ter Python 3.8+ instalado.

1.  Clone este repositório (ou baixe o código).
2.  Navegue até a pasta do projeto no seu terminal.
3.  (Recomendado) Crie e ative um ambiente virtual:
    ```bash
    python -m venv venv
    # Linux/macOS: source venv/bin/activate
    # Windows: venv\Scripts\activate.bat
    ```
4.  Instale a ferramenta e suas dependências:
    ```bash
    pip install .
    ```
    Isso disponibilizará o comando `prompt-cost-calculator` no seu terminal (enquanto o ambiente virtual estiver ativo).

## Uso

O comando principal é `prompt-cost-calculator`.

### Calcular Custo de Input

Use o subcomando `calculate` com as opções necessárias:

```bash
prompt-cost-calculator calculate \
    --provider <nome_do_provedor> \
    --model <nome_do_modelo> \
    --prompt "<o texto do seu prompt aqui>"
```

**Exemplos:**

*   **OpenAI GPT-4 Turbo:**
    ```bash
    prompt-cost-calculator calculate --provider openai --model gpt-4-turbo --prompt "Explique o conceito de MLOps em 3 frases."
    ```

*   **Anthropic Claude 3 Haiku (Custo Estimado):**
    ```bash
    prompt-cost-calculator calculate --provider anthropic --model claude-3-haiku-20240307 --prompt "Qual a capital da França?"
    ```

*   **Google Gemini 1.0 Pro (Custo baseado em caracteres):**
    ```bash
    prompt-cost-calculator calculate --provider google --model gemini-1.0-pro --prompt "Escreva um poema curto sobre chuva."
    ```

### Listar Modelos Suportados

Para ver a lista de provedores e modelos configurados na ferramenta (e seus dados de preço/unidade):

```bash
prompt-cost-calculator list-models
```

### Ajuda

Para ver todas as opções e comandos disponíveis:

```bash
prompt-cost-calculator --help
prompt-cost-calculator calculate --help
```

## Modelos Suportados (Exemplos - Verifique `list-models`)

*   **OpenAI:** `gpt-4-turbo`, `gpt-3.5-turbo` (contagem via `tiktoken`)
*   **Anthropic:** `claude-3-opus-20240229`, `claude-3-sonnet-20240229`, `claude-3-haiku-20240307` (contagem ESTIMADA)
*   **Google:** `gemini-1.5-pro-latest`, `gemini-1.0-pro` (contagem baseada em caracteres, verificar precificação oficial)

*Consulte a saída de `prompt-cost-calculator list-models` para a lista mais atualizada dentro da ferramenta.*

## Limitações e Próximos Passos (Fase 2)

*   **Apenas Custo de Input:** Esta versão não calcula o custo de output.
*   **Estimativas:** Contagem para não-OpenAI é aproximada.
*   **Preços Estáticos:** Os preços precisam ser atualizados manualmente no código (`cost_calculator/models.py`).

A **Fase 2** planeja adicionar a capacidade de executar o prompt (requerendo chave de API) para calcular o custo de output e o custo total.

## Licença

Este projeto é licenciado sob a Licença MIT. Veja o arquivo `LICENSE` (você precisará criar um se não existir) para mais detalhes.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests no repositório [Link para o Repositório GitHub, se aplicável].
