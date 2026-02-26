# Base de Conhecimento - Jornada dos Sonhos

## Dados utilizados

| Arquivo | Formato | Uso no Jornada |
|---|---|---|
| `perfil_investidor.json` | JSON | Define renda, perfil e objetivos para personalizar conversa e viabilidade |
| `transacoes.csv` | CSV | Mostra padrão de gastos e registro de aportes para metas |
| `historico_atendimento.csv` | CSV | Dá continuidade ao acompanhamento da jornada |
| `produtos_financeiros.json` | JSON | Armazena cenários e regras educativas da simulação |
| `jornada_contexto.json` | JSON | Persistência de estado por `id_usuario` entre sessões |

## Estratégia de integração

1. O app carrega `perfil_investidor.json` no início para sugerir renda padrão.
2. O fluxo conversacional salva cada avanço em `jornada_contexto.json`.
3. Os cenários (0,5% e 0,8% ao mês) e a regra de viabilidade ficam em `produtos_financeiros.json` como base explicativa.
4. `transacoes.csv` e `historico_atendimento.csv` sustentam demonstração e narrativa de evolução da meta.

## Exemplo de contexto resumido

```text
CLIENTE:
- Nome: Camila Rocha
- Renda mensal: R$ 7.200,00
- Objetivo principal: Intercambio em Dublin em 24 meses

META ATUAL:
- Sonho: Intercambio em Dublin
- Valor-meta: R$ 42.000,00
- Prazo: 24 meses
- Valor inicial: R$ 6.000,00

ACOMPANHAMENTO:
- Ultima interacao: recalibracao para incluir passagens e seguro
- Status: plano concluido com simulacao de dois cenarios

REGRAS DE SIMULACAO:
- Cenario conservador: 0,5% a.m.
- Cenario moderado: 0,8% a.m.
- Alerta de viabilidade: aporte > 80% da renda
```

## Boas práticas aplicadas

- Separação entre dados de perfil, histórico e contexto de sessão.
- Persistência incremental por usuário para retomada proativa.
- Cenários tratados como hipótese educativa, sem promessa de retorno.
