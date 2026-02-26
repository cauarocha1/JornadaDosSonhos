# Riscos e Controles - Jornada dos Sonhos

## Matriz de risco resumida

| ID | Risco | Impacto | Mitigacao |
|---|---|---|---|
| R1 | Ollama indisponivel | Alto | Checagem de saude e mensagem orientada |
| R2 | Timeout em modelo pesado | Medio | Timeout configuravel na UI |
| R3 | Texto com caracteres corrompidos | Medio | Normalizacao no pos-processamento |
| R4 | Resposta com formato monetario ruim | Medio | Regra de prompt + limpeza de saida |
| R5 | Conteudo fora de escopo financeiro | Medio | Regras no prompt de sistema |

## Controles implementados

- Health check em `/api/tags`.
- Fallback `localhost` -> `127.0.0.1`.
- Timeout de leitura ajustavel (`60` a `600` segundos).
- Limpeza de caracteres invisiveis e espacos anormais.
- Normalizacao basica de `R$` nas respostas.

## Melhorias futuras

1. Testes automatizados para `normalize_ai_text`.
2. Telemetria local opcional de latencia por resposta.
3. Validacao semantica de respostas com regras de seguranca.
