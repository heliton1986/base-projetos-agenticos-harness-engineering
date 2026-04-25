# Template - Data Contract

## Nome do Contrato

`[NOME_DO_CONTRATO]`

## Fonte

- tipo: `[CSV|ERP|PostgreSQL|API|outro]`
- origem: `[origem]`
- modo de acesso: `[somente leitura|export controlado|outro]`

## Campos Esperados

| campo | tipo | obrigatorio | descricao |
|---|---|---|---|
| `[campo]` | `[tipo]` | `[sim|nao]` | `[descricao]` |

## Chaves de Rastreabilidade

- `[campo 1]`
- `[campo 2]`

## Regras de Qualidade

- `[regra 1]`
- `[regra 2]`
- `[regra 3]`

## Representacao de Inconsistencia

Defina como representar:

- tipo de inconsistencia
- severidade
- origem afetada
- evidencia
- recomendacao de revisao

## Politica de Mascaramento

Defina:

- campos sensiveis
- forma de mascaramento
- onde o dado pode aparecer mascarado
- onde o dado nao deve aparecer

## Saida Consolidada Esperada

Defina o formato minimo do consolidado final.
