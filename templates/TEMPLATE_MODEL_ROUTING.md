# Template - Model Routing

## Objetivo

Definir como o projeto configura modelos por papel agentico de forma explicita e auditavel.

## Provider

- `LLM_PROVIDER=[provider]`

## Mapeamento por papel

```text
ORCHESTRATOR_MODEL=[modelo_robusto]
PLANNER_MODEL=[modelo_medio_ou_robusto]
EXECUTION_MODEL=[modelo_medio]
VALIDATOR_MODEL=[modelo_medio_ou_robusto]
REPORTER_MODEL=[modelo_economico_ou_medio]
FRONTEND_STATUS_MODEL=[modelo_economico_ou_medio]
```

## Exemplo generico

```text
ORCHESTRATOR_MODEL=robust-model
PLANNER_MODEL=medium-or-robust-model
EXECUTION_MODEL=medium-model
VALIDATOR_MODEL=medium-or-robust-model
REPORTER_MODEL=economical-or-medium-model
FRONTEND_STATUS_MODEL=economical-model
```

## Exemplo concreto opcional

```text
LLM_PROVIDER=openai
ORCHESTRATOR_MODEL=gpt-5
PLANNER_MODEL=gpt-5-mini
EXECUTION_MODEL=gpt-5-mini
VALIDATOR_MODEL=gpt-5
REPORTER_MODEL=gpt-5-mini
FRONTEND_STATUS_MODEL=gpt-5-mini
```

## Regras

- `robusto` para papeis de decisao e maior risco
- `medio` para papeis tecnicos delimitados
- `economico` para papeis de status, resumo simples e tarefas repetitivas

## O que registrar no runtime

Para cada etapa, registrar pelo menos:

- papel do agente
- provider usado
- modelo usado
- status
- retry_count
