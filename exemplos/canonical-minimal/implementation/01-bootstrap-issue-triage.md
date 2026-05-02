# Fase 1 - Bootstrap de Triagem de Issues

Baseado em: `templates/TEMPLATE_IMPLEMENTATION_PHASE.md`

## Objetivo

Entregar o menor fluxo multi-agent verificavel do projeto: receber `IssueInput`, classificar com LLM, validar contrato, aplicar regras de negocio e gerar `IssueReport`.

## Pre-condicoes

- `spec/01-brainstorm.md`, `spec/02-define.md` e `spec/03-design.md` revisados
- `directives/triagem_rules.md` definido
- `model_routing.yaml` presente

## Arquivos que devem ser lidos antes

- `AGENTS.md`
- `directives/triagem_rules.md`
- `contracts/issue_contract.md`
- `src/contracts/issue_contract.py`
- `src/agents/orchestrator.py`

## Passos de Execucao

1. Validar contratos executaveis em `src/contracts/issue_contract.py`
2. Implementar agentes `ClassifierAgent`, `ValidatorAgent` e `ReporterAgent`
3. Encadear tudo em `OrchestratorAgent` com loop de ate 3 tentativas
4. Criar onboarding flow para smoke tests de ambiente
5. Adicionar testes offline e CI antes de qualquer migracao para framework

## Validacoes Obrigatorias

- `python execution/run_onboarding_flow.py`
- `pytest tests/ -v --tb=short`
- `pytest tests/ -v --tb=short --cov=src --cov-report=term --cov-fail-under=80`

## Politica de Correcao

- se houver erro local e de baixo risco, corrigir e reexecutar
- se houver ambiguidade de regra de negocio, parar e revisar `directives/triagem_rules.md`
- nao avancar para a proxima fase sem os gates minimos aprovados

## Criterio de Aprovacao

A fase so pode ser considerada concluida quando:

- `ValidatorAgent` bloquear contratos invalidos
- fluxo aprovado gerar `IssueReport` valido
- testes offline e coverage minima passarem

## Artefatos Esperados

- `src/contracts/issue_contract.py`
- `src/agents/validator_agent.py`
- `tests/`
- `.github/workflows/tests.yml`

## Proxima Fase Sugerida

`Fase 2 - API ou UI observavel, se houver requisito real`
