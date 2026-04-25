# spec/03-design.md — [NOME DO PROJETO]

## Objetivo deste documento

Definir a arquitetura tecnica do sistema antes de qualquer implementacao.
Decisoes aqui guiam o bootstrap e as fases de implementacao.

## Arquitetura geral

```
[Componente de entrada — ex: Streamlit / API / CLI]
      |
      v
[OrchestratorAgent]
      |
      +---> [SubagenteA]      → [responsabilidade]
      +---> [SubagenteB]      → [responsabilidade]
      +---> [SubagenteC]      → [responsabilidade]
      |
      v
[Camada de persistencia — ex: PostgreSQL / arquivos]
```

## Agentes e responsabilidades

| Agente | Responsabilidade | Entrada | Saida | Usa LLM? |
|--------|-----------------|---------|-------|---------|
| OrchestratorAgent | Coordena fluxo | [tipo] | [tipo] | nao |
| [SubagenteA] | [responsabilidade] | [tipo] | [TipoResponse] | sim/nao |
| AuditAgent | Trilha de auditoria | [tipo] | audit_id | nao |

## Modelo de dados

### Tabelas principais

| Tabela | Proposito | Campos chave |
|--------|-----------|-------------|
| [tabela] | [para que serve] | [campos] |

### Schema simplificado

```sql
-- [descricao da tabela principal]
CREATE TABLE [nome] (
    id UUID PRIMARY KEY,
    [campo] [tipo],
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

## Stack tecnica

| Camada | Tecnologia | Justificativa |
|--------|-----------|--------------|
| Frontend | [ex: Streamlit] | [razao] |
| API | [ex: FastAPI] | [razao] |
| LLM | [ex: Claude claude-sonnet-4-6] | [razao] |
| Banco | [ex: PostgreSQL] | [razao] |

## Estrategia de modelos por agente

| Agente | Modelo | Justificativa |
|--------|--------|--------------|
| [agente com LLM] | [modelo] | [por que LLM aqui] |
| Demais | Sem LLM | Logica deterministica |

Ref: `base/10_ESTRATEGIA_DE_MODELOS_PARA_AGENTES.md`

## Fluxo principal (happy path)

1. [passo 1 — ex: usuario faz upload de CSV]
2. [passo 2 — ex: IngestAgent normaliza e valida]
3. [passo 3 — ex: ConsolidationAgent agrega]
4. [passo 4 — ex: ReportAgent gera relatorio via LLM]
5. [passo 5 — ex: resultado exibido no frontend]

## Tratamento de erros

| Cenario | Comportamento esperado |
|---------|----------------------|
| [erro 1] | [o que acontece] |
| [erro 2] | [o que acontece] |

## Politica de mascaramento de dados

Defina quais dados sao sensiveis e como sao tratados antes de qualquer LLM:

- [campo sensivel 1]: [como mascarar]
- [campo sensivel 2]: [como mascarar]

## Observabilidade

Cada operacao registra em `audit_log`:
- `agent`, `operation`, `status`, `duration_ms`
- `input_summary`, `output_summary` — sem dados sensiveis
- `error_message` quando aplicavel

## Decisoes de design

| Decisao | Alternativa considerada | Razao da escolha |
|---------|------------------------|-----------------|
| [decisao] | [alternativa] | [justificativa] |

## Restricoes tecnicas

- [restricao 1 — ex: nenhum agente escreve na fonte de dados original]
- [restricao 2]

## Fases de implementacao previstas

| Fase | Objetivo | Gate |
|------|---------|------|
| 1 | [bootstrap + infraestrutura] | Gate 1 |
| 2 | [primeira capacidade] | Gate 2 |
| 3 | [capacidade seguinte] | Gate 3 |
