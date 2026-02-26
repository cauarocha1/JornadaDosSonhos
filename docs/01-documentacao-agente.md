# Documentacao do Agente - Jornada

## Objetivo

Responder perguntas de planejamento financeiro em linguagem simples, usando os dados locais do projeto como contexto.

## Comportamento esperado

- Linguagem clara e direta em portugues do Brasil.
- Sem recomendacao de ativo especifico.
- Sem promessa de retorno garantido.
- Quando faltar dado, pedir contexto adicional do usuario.

## Arquitetura atual

- Frontend: Streamlit (`src/app.py`).
- Motor de resposta: Ollama via `/api/generate`.
- Contexto: arquivos em `data/` incorporados no prompt.
- Prompt base: `docs/03-prompts.md`.
- Pos-processamento: limpeza de caracteres e normalizacao de valores com `R$`.

## Limites

- Nao substitui assessoria profissional.
- Qualidade depende do modelo local instalado no Ollama.
- Dados de exemplo podem nao representar situacoes reais.
