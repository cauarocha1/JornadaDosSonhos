# Avaliacao e Metricas - Jornada

## Metricas tecnicas

| Metrica | Meta |
|---|---|
| Disponibilidade local | App sobe em `localhost:8501` |
| Conectividade Ollama | `/api/tags` responde com sucesso |
| Tempo de resposta | <= timeout configurado pelo usuario |
| Qualidade de saida | Sem caracteres quebrados e moeda legivel |

## Cenarios de teste sugeridos

1. Ollama online e modelo carregado.
2. Ollama offline (mensagem de erro orientada).
3. Modelo pesado com timeout curto e depois timeout alto.
4. Pergunta com varios valores monetarios para validar `R$`.
5. Pergunta longa para validar estabilidade do chat.

## Criterio de pronto

- App nao quebra em nenhuma chamada.
- Mensagens de erro sao acionaveis.
- Documentacao bate com o comportamento real.
