# Template - Task Contract

## Nome da Tarefa

`[NOME_DA_TAREFA]`

## Agente Responsavel

`[NomeDoAgente]` — `src/agents/[nome].py`

## Objetivo

Descreva o que esta tarefa deve produzir. Uma frase clara de resultado esperado.

## Pre-condicoes

O que precisa estar pronto antes desta tarefa poder executar:

- [ ] [pre-condicao 1]
- [ ] [pre-condicao 2]

## Entrada

| campo | tipo | obrigatorio | descricao |
|-------|------|-------------|-----------|
| `[campo]` | `[tipo]` | sim/nao | `[descricao]` |

## Saida Esperada

| campo | tipo | descricao |
|-------|------|-----------|
| `[campo]` | `[tipo]` | `[descricao]` |

## Contrato de Dados

- Fonte dos dados: `[origem]`
- Formato: `[CSV|JSON|PostgreSQL|API]`
- Dados sensiveis: `[sim/nao]` — se sim, mascarar antes de qualquer LLM

## Gate de Aprovacao

A tarefa so e considerada aprovada quando:

- [ ] [criterio 1]
- [ ] [criterio 2]
- [ ] Entrada em `audit_log` criada com status correto

## Politica de Ambiguidade

- Ambiguidade de baixo risco: assumir de forma conservadora, registrar decisao em `directives/` ou `spec/`
- Ambiguidade de alto risco ou regulatoria: parar e perguntar objetivamente

## Politica de Correcao

- Erro local e reversivel: corrigir e reexecutar automaticamente
- Erro que afeta dados ou contratos: parar e reportar antes de agir

## Audit Log Obrigatorio

Campos minimos a registrar:

- `agent`: nome do agente
- `operation`: nome da operacao
- `status`: success | partial | error
- `input_summary`: resumo sem dados sensiveis
- `output_summary`: resumo do resultado
- `duration_ms`: tempo de execucao

## Restricoes

- [restricao 1 — ex: nao alterar dados na fonte]
- [restricao 2 — ex: nao enviar dados nao mascarados ao LLM]

## Dependencias

- Depende de: `[tarefa ou agente anterior]`
- Alimenta: `[tarefa ou agente seguinte]`
