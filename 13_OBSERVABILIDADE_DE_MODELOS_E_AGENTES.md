# Observabilidade de Modelos e Agentes

## Objetivo

Este documento define como registrar e exibir informacoes sobre:

- qual agente executou
- qual modelo foi usado
- qual provider foi usado
- qual foi o status da execucao
- quando houve retry, validacao ou falha

Ele conecta tres preocupacoes da base:

- `10_ESTRATEGIA_DE_MODELOS_PARA_AGENTES.md`
- `07_FRONTEND_OBSERVAVEL_PARA_AGENTES.md`
- `11_PROTOCOLO_DE_EXECUCAO_AGENTICA.md`

## Principio central

Se o sistema usa papeis diferentes com modelos diferentes, isso deve ser observavel pelo menos em modo tecnico.

A observabilidade deve responder perguntas como:

- qual agente executou esta etapa?
- qual modelo foi usado?
- houve retry?
- a validacao passou?
- o sistema esta pronto para abrir API e frontend?

## O que registrar por agente

Para cada execucao agentica, registrar pelo menos:

- `agent_name`
- `agent_role`
- `provider`
- `model`
- `status`
- `started_at`
- `finished_at`
- `retry_count`
- `validation_status`, quando aplicavel
- `summary`, quando util

## Exemplo de estrutura

```json
{
  "agent_name": "Orchestrator",
  "agent_role": "orchestration",
  "provider": "openai",
  "model": "gpt-5-strong",
  "status": "completed",
  "started_at": "2026-04-24T18:00:00Z",
  "finished_at": "2026-04-24T18:00:03Z",
  "retry_count": 0,
  "validation_status": "approved"
}
```

## O que mostrar no chat

Em modo tecnico, a LLM pode mostrar:

- agente executado
- modelo usado
- provider, se relevante
- status da etapa
- erro encontrado
- retry realizado
- validacao aprovada ou nao

Em modo mais simples, pode resumir apenas:

- etapa
- status
- proximo passo

## O que mostrar no frontend

### Modo tecnico

Pode mostrar:

- nome do agente
- papel do agente
- modelo usado
- provider
- status
- retries
- validacao
- timestamps

### Modo usuario final

Deve mostrar menos detalhe por padrao, por exemplo:

- etapa atual
- agente em execucao
- concluido / executando / falhou / validando
- resultado final

A exibicao de modelo pode ser opcional ou restrita a uma area tecnica.

## Relacao com a estrategia de modelos

A observabilidade existe para tornar verificavel a politica definida em `10_ESTRATEGIA_DE_MODELOS_PARA_AGENTES.md`.

Se o projeto diz que:

- `Orchestrator` usa modelo robusto
- `ExecutionAgent` usa modelo medio
- `ReporterAgent` usa modelo economico

entao o runtime deve conseguir registrar e exibir isso.

## Relacao com o frontend observavel

O frontend observavel deve ser capaz de exibir pelo menos:

- agente atual
- status atual
- modelo usado, quando o modo tecnico estiver ativo
- validacao da etapa
- readiness para abrir API e frontend, quando fizer sentido

## Configuracao via ambiente

Uma configuracao tipica pode incluir:

```text
LLM_PROVIDER=openai
OPENAI_API_KEY=...
ORCHESTRATOR_MODEL=gpt-5-strong
EXECUTION_MODEL=gpt-5-medium
VALIDATOR_MODEL=gpt-5
REPORTER_MODEL=gpt-5-mini
FRONTEND_STATUS_MODEL=gpt-5-mini
```

## O que nao fazer

Evite:

- usar modelos por papel sem observabilidade minima
- mostrar detalhes tecnicos demais para usuarios finais sem necessidade
- ocultar retries e falhas em modo tecnico
- expor dados sensiveis junto com metadados de execucao

## Recomendacao pratica

### Sempre registrar internamente

- agente
- modelo
- status
- timestamps
- retries

### Mostrar no frontend tecnico

- agente
- modelo
- status
- validacao

### Mostrar no frontend usuario final

- etapa
- status
- resultado

## Conclusao

Se ha orquestrador e subagentes com modelos diferentes, a observabilidade dessa escolha nao deve ficar invisivel.

Em uma frase:

`Estratégia de modelos sem observabilidade vira suposicao; com observabilidade, vira sistema auditavel.`
