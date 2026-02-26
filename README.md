# Jornada dos Sonhos

App Streamlit de assistente financeiro com base de conhecimento local e Ollama.

## Visao geral

- Interface de chat em Streamlit.
- Contexto construído com arquivos em `data/`.
- Prompt de sistema carregado de `docs/03-prompts.md`.
- Conexao com Ollama em `http://localhost:11434/api/generate` (ou `127.0.0.1` como fallback).
- Pos-processamento de texto para reduzir caracteres estranhos e normalizar `R$`.

## Estrutura

```text
JornadaDosSonhos/
  src/
    app.py
    README.md
  data/
    perfil_investidor.json
    produtos_financeiros.json
    jornada_contexto.json
    transacoes.csv
    historico_atendimento.csv
  docs/
    01-documentacao-agente.md
    02-base-conhecimento.md
    03-prompts.md
    04-metricas.md
    05-pitch.md
    06-riscos-e-controles.md
```

## Requisitos

- Python 3.11+
- `streamlit`
- `requests`
- Ollama (obrigatorio)

## Como executar

1. Instale dependencias:

```bash
pip install streamlit requests
```

2. Inicie o Ollama:

```bash
ollama pull gpt-oss
ollama serve
```

3. Rode o app:

```bash
streamlit run src/app.py
```

4. Acesse `http://localhost:8501`.

## Configuracao no app

Na barra lateral:
- `URL API`: endpoint do Ollama.
- `Modelo`: modelo usado na geracao (ex.: `gpt-oss`).
- `Timeout de leitura (s)`: aumenta tolerancia para modelos pesados.

## Observacoes

- Sem Ollama ativo, o agente nao responde.
- O projeto usa dados locais de exemplo e nao deve ser tratado como recomendacao financeira.
