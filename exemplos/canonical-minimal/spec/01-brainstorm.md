# Spec 01 — Brainstorm: Issue Triage Agent

## Problema

Equipes recebem issues em texto livre. Triagem manual e lenta e inconsistente. Queremos classificacao automatica e auditavel.

## Ideias exploradas

### Abordagem A: LLM classifica tudo em one-shot
- Prompt unico recebe issue e retorna JSON com severidade + categoria
- Simples de implementar
- Risco: sem validacao, LLM pode inventar valores fora do contrato

### Abordagem B: Pipeline com contrato validado (escolhida)
- ClassifierAgent retorna `IssueClassification` tipada (Pydantic)
- ValidatorAgent verifica regras de negocio alem do schema
- Loop de correcao se invalido
- Rastreavel: sabemos quantas tentativas, qual erro

### Abordagem C: Ensemble de modelos votando
- Dois modelos classificam independentemente, resultado por maioria
- Mais robusto, mais caro
- Fora de escopo para versao minima

## Decisao

Abordagem B. Custo baixo, contrato claro, auditavel, extensivel.

## Escopo minimo (v1)

- Recebe texto de issue
- Classifica severidade (4 niveis) e categoria (6 tipos)
- Valida contra contrato
- Retorna IssueReport

## Fora de escopo (v1)

- Interface web
- Banco de dados persistente
- Integracao com GitHub/Jira
- Notificacoes
- Multi-tenant
