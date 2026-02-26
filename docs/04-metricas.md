# Avaliação e Métricas - Jornada

## Métricas

| Métrica | Objetivo |
|---|---|
| Assertividade | O agente coleta os 4 dados essenciais antes de simular |
| Segurança | Não recomenda ativo e não promete retorno |
| Escopo | Bloqueia perguntas fora de finanças pessoais |
| Viabilidade | Detecta cenários inviáveis e sugere ajuste de prazo |
| Robustez | Continua funcionando sem Ollama |

## Cenários de teste

1. Meta viável: `R$ 35.000` em `24 meses` com `R$ 5.000` inicial.
2. Meta inviável: aporte calculado > 80% da renda.
3. Entrada inválida: usuário digita texto sem número.
4. Fallback: desligar Ollama e validar resposta do app.
5. Fora de escopo: perguntar clima/placar e validar recusa.

## Critério de aprovação

- 100% dos cenários executam sem quebrar a aplicação.
- Em caso inviável, o app sempre oferece alternativa viável.
- Mensagem de disclaimer aparece em toda sessão.
