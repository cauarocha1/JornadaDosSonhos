# Riscos e Controles - Jornada dos Sonhos

## Objetivo

Mapear riscos de produto, técnicos e de uso indevido, com ações preventivas para reduzir a chance de falha na demo e no uso real.

## Matriz de riscos

| ID | Risco | Impacto | Probabilidade | Controle preventivo | Plano de contingência |
|---|---|---|---|---|---|
| R1 | Alucinação na estimativa de custo | Alto | Médio | Estimativa inicial por faixas pré-definidas por categoria de sonho | Exibir faixa genérica e pedir validação manual do usuário |
| R2 | Usuário entender simulação como recomendação | Alto | Médio | Aviso fixo de uso educativo + prompt com restrição explícita | Reforçar disclaimer em cada resultado final |
| R3 | Meta inviável para renda do usuário | Alto | Alto | Regra de viabilidade (>80% da renda gera alerta) | Sugerir prazo alternativo com orçamento alvo de 35% da renda |
| R4 | Entrada inválida (texto sem números) | Médio | Alto | Parsing com validação de moeda e prazo por etapa | Reperguntar com exemplo de formato aceito |
| R5 | Queda do Ollama/API local | Médio | Médio | LLM opcional e desacoplado da matemática | Responder com texto determinístico sem interromper o fluxo |
| R6 | Perda de contexto entre sessões | Médio | Médio | Persistência em `data/jornada_contexto.json` por `id_usuario` | Reconstruir conversa a partir do contexto salvo |
| R7 | Corrupção do arquivo JSON | Médio | Baixo | Leitura com fallback seguro e escrita atômica simplificada | Reinicializar contexto do usuário mantendo app funcional |
| R8 | Prazo extremo gerando simulação irreal | Médio | Baixo | Limite de prazo de 720 meses | Solicitar novo prazo dentro do limite |
| R9 | Dependência de taxa fixa desatualizada | Médio | Médio | Rotular taxas como cenários hipotéticos | Permitir ajuste de taxa em futura versão |
| R10 | Exposição de dados sensíveis no prompt | Alto | Baixo | Uso mínimo de contexto pessoal e sem dados bancários sensíveis | Remover campos sensíveis e anonimizar IDs |

## Controles implementados no código

- Fluxo por etapas (`descoberta`, `valor_meta`, `prazo`, `valor_inicial`, `renda`, `concluido`).
- Cálculo financeiro independente do LLM.
- `fallback` automático quando a chamada ao Ollama falha.
- Persistência de estado por usuário com timestamp.
- Mensagem de ajuste quando o plano fica agressivo para o orçamento.

## Riscos futuros previstos

1. Mudanças macroeconômicas podem invalidar premissas de taxa.
2. Estimativas de sonhos podem variar por cidade e sazonalidade.
3. Usuário pode informar renda incorreta e distorcer viabilidade.

## Próximas melhorias para reduzir risco residual

1. Adicionar campo de cidade/país para estimativas geográficas.
2. Criar testes automatizados para fórmula de PMT e parsing.
3. Versionar contextos por data para auditoria das simulações.
4. Incluir score de confiança nas estimativas de custo.
