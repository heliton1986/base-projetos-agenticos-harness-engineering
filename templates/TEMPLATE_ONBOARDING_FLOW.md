# Template - Onboarding Flow

## Objetivo

Fornecer um unico comando de primeira execucao para o projeto.

## Comportamento Esperado

O fluxo de onboarding deve:

1. executar a primeira capacidade incremental
2. rodar a validacao inicial
3. atualizar o status em `progress/` e/ou `runtime/`
4. informar claramente se o sistema esta pronto para abrir API e frontend

## Nome Sugerido

- `execution/run_onboarding_flow.py`

## Saidas Esperadas

- artefatos da primeira capacidade gerados
- resultado da validacao inicial
- status de onboarding persistido
- mensagem final clara para o usuario

## Politica de Status

O fluxo deve deixar explicito:

- `ready_for_api`: `true` ou `false`
- `ready_for_frontend`: `true` ou `false`
- gates aprovados
- gates pendentes
- proximo passo sugerido


## Comportamento esperado da LLM

Quando o usuario pedir este fluxo, a expectativa e que a LLM:

- execute o script
- observe a saida
- tente corrigir erros locais de baixo risco
- reexecute
- rode a validacao
- informe no chat se o sistema esta pronto ou nao
