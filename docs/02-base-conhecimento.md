# Base de Conhecimento - Jornada dos Sonhos

## Arquivos utilizados

| Arquivo | Tipo | Uso no app |
|---|---|---|
| `data/perfil_investidor.json` | JSON | Perfil financeiro e preferencia de risco |
| `data/transacoes.csv` | CSV | Historico de entradas/saidas para contexto |
| `data/historico_atendimento.csv` | CSV | Conversas anteriores de exemplo |
| `data/produtos_financeiros.json` | JSON | Referencias educativas e categorias |
| `data/jornada_contexto.json` | JSON | Contexto complementar local |

## Como o contexto e montado

1. O app le os arquivos de `data/`.
2. Converte JSON para texto estruturado.
3. Anexa CSV bruto como bloco de contexto.
4. Envia tudo junto com o historico recente do chat ao modelo.

## Boas praticas

- Manter arquivos pequenos e coerentes com o dominio.
- Evitar dados pessoais reais.
- Versionar mudancas de contexto junto com o codigo.
