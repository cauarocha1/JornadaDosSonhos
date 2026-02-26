# Documentação do Agente - Jornada

## Caso de uso

### Problema
Pessoas têm sonhos concretos, mas não sabem converter objetivos em um plano financeiro viável.

### Solução
A `Jornada` conduz uma conversa em etapas para transformar o sonho em meta com prazo, simula aporte mensal e sinaliza inviabilidade com alternativas.

### Público-alvo
Usuários iniciantes e intermediários que querem planejar metas como viagem, intercâmbio, casamento, carro ou entrada de imóvel.

## Persona e tom

- Nome: `Jornada`
- Personalidade: empática, pragmática e honesta.
- Tom: simples e didático, sem jargão desnecessário.

## Regras de segurança

- Não recomendar ativo financeiro específico.
- Não prometer retorno garantido.
- Explicar que os cenários são hipotéticos.
- Ajustar expectativas quando o plano estiver agressivo para a renda.

## Arquitetura

```mermaid
flowchart TD
    A[Usuário] --> B[Streamlit]
    B --> C[Orquestrador conversacional]
    C --> D[Motor matemático PMT]
    C --> E[Contexto persistente JSON]
    C --> F[Ollama opcional]
    D --> G[Resposta final com cenários]
    E --> G
    F --> G
```

## Limitações declaradas

- Não substitui assessor financeiro certificado.
- Não usa dados bancários sensíveis.
- Não prevê taxa real futura, apenas simula cenários.
