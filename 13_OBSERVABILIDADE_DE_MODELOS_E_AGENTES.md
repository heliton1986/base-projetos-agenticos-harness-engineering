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

### Formato padrao — checklist por etapa

Toda execucao agentica deve ser narrada no chat com o seguinte padrao:

```
✓ Etapa 1 — NomeAgente: o que fez + resultado quantificado
✓ Etapa 2 — NomeAgente → modelo-llm: input → output
■ Gate final — ValidatorAgent (Pydantic): PASSED/FAILED em Xs
```

Regras:
- `✓` etapa concluida com sucesso
- `■` gate ou resultado final
- `✗` etapa com falha — detalhar o erro
- entre etapas, publicar micro-updates curtos logo apos cada tool call para mostrar progresso continuo
- quando a interface ou harness resumir, colapsar ou ocultar a atividade, o micro-update no chat deve expandir isso com os nomes reais dos arquivos e comandos
- quando a interface mostrar varias leituras/comandos em sequencia, sincronizar o chat com granularidade parecida, evitando esperar um resumo em lote

### Quando LLM foi usada

Mostrar agente + modelo + fluxo de dados:

```
✓ DetectorAgent → claude-sonnet-4-6: 3 candidatos → 1 inconsistencia semantica
```

Nunca omitir o modelo quando uma chamada LLM foi feita.

### Dados estruturados — usar tabela

Coverage, status por agente, inconsistencias encontradas: sempre em tabela markdown, nao lista de texto.

| Agente | Cobertura | Status |
|--------|-----------|--------|
| detector_agent | 100% | PASSED |
| ingestion_agent | 100% | PASSED |

### Incluir sempre

- Nome do agente que executou
- Modelo LLM usado quando houve chamada (ex: `claude-sonnet-4-6`)
- Quantidade de itens processados
- Inconsistencias/erros com tipo e detalhe
- Status final e tempo de execucao quando relevante

**Por que:** output do Bash fica colapsado na UI do Claude Code. O usuario ve apenas o chat — a narrativa deve ser informativa o suficiente para nao precisar expandir o terminal.

### Regra extra para micro-updates

Um micro-update bom nao diz apenas "li 4 arquivos" ou "rodei 3 comandos".
Ele diz exatamente quais foram:

```text
Li `AGENTS.md`, `README.md`, `progress/PROGRESS.md` e `progress/VALIDATION_STATUS.md`.
Rodei `python execution/run_onboarding_flow.py`, `pytest tests/ -v --tb=short` e `python tools/validate_harness_project.py .`.
```

Isso evita que a observabilidade dependa de o usuario expandir blocos colapsados da UI.

Melhor ainda quando o fluxo exigir rastreabilidade fina:

```text
Li `AGENTS.md`. Resultado: regra de execucao confirmada. Proximo passo: abrir `progress/PROGRESS.md`.
Li `progress/PROGRESS.md`. Resultado: identifiquei a fase pendente. Proximo passo: rodar `pytest tests/ -v --tb=short`.
Rodei `pytest tests/ -v --tb=short`. Resultado: 12 testes passaram. Proximo passo: abrir `progress/VALIDATION_STATUS.md`.
```

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
