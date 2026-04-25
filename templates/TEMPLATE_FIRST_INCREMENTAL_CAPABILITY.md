# Template - First Incremental Capability

## Nome da Capacidade

`[NOME_DA_CAPACIDADE]`

## Objetivo

Descreva a menor capacidade util, validavel e coerente com a fase atual do projeto.

## Entradas

- `[fonte 1]`
- `[fonte 2]`
- `[fonte 3]`

## Contratos de Dados Necessarios

Antes de implementar, confirme onde estao documentados:

- formato exato dos CSVs
- schema esperado do ERP ou export equivalente
- formato do consolidado
- representacao de inconsistencia
- politica de mascaramento de dados sensiveis

## Scripts Esperados

- `normalize_[dominio]_inputs.py`
- `consolidate_[dominio].py`
- `detect_[dominio]_inconsistencies.py`
- `build_[dominio]_summary.py`
- `run_first_capability.py`

## Saidas Esperadas

- arquivo consolidado
- arquivo de inconsistencias
- resumo executivo inicial
- evidencias minimas de validacao

## Gates Minimos

- nao expandir escopo
- preservar rastreabilidade
- respeitar contratos de dados
- respeitar mascaramento
- passar nas validacoes minimas da fase

## Politica de Ambiguidade

Se faltar detalhe de baixo risco, assumir de forma conservadora e registrar em `spec/`, `contracts/`, `directives/` ou `kb/`.

Se faltar detalhe de alto risco, sensivel ou regulatorio, parar e pedir esclarecimento objetivo.
