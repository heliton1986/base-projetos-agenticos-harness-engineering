# AGENTS.md — Issue Triage Agent

## Papel deste arquivo

Este arquivo define como a LLM deve se comportar ao trabalhar neste projeto.
Leia antes de qualquer implementacao, execucao ou modificacao.

## Identidade do sistema

- **Nome:** Issue Triage Agent
- **Tipo:** Sistema agentico com 4 agentes especializados
- **Dominio:** Triagem e classificacao de issues de software
- **Stack:** Python + Anthropic API + Pydantic + pytest

## Modelo Operacional (DOE)

Este projeto segue `Diretivas + Orquestracao + Execucao`:

- **Diretivas** em `directives/` — categorias e severidades validas, nunca improvisar fora delas
- **Orquestracao** em `src/agents/orchestrator.py` — coordena fluxo, aplica loop de correcao e gates
- **Execucao** em `src/agents/` — cada agente tem responsabilidade isolada
- **Contratos executaveis** em `src/contracts/` — schemas Pydantic usados em runtime
- **Contratos documentais** em `contracts/` — invariantes e significado de cada payload

## Agentes e responsabilidades

| Agente | Arquivo | Responsabilidade | Usa LLM? |
|--------|---------|-----------------|---------|
| OrchestratorAgent | `src/agents/orchestrator.py` | Coordena fluxo, retenta quando ha contrato ou regra invalida | nao |
| ClassifierAgent | `src/agents/classifier_agent.py` | Classifica severidade e categoria via LLM | sim |
| ValidatorAgent | `src/agents/validator_agent.py` | Valida contratos Pydantic de classificacao e relatorio | nao |
| ReporterAgent | `src/agents/reporter_agent.py` | Formata `IssueReport` final | nao |

## Contratos de entrada e saida

- Entrada do sistema: `IssueInput`
- Saida do ClassifierAgent: `IssueClassification`
- Saida final: `IssueReport`
- Contratos executaveis: `src/contracts/issue_contract.py`
- Contratos documentais: `contracts/issue_contract.md`

## Regras que nunca podem ser violadas

1. ClassifierAgent retorna apenas `IssueClassification` — nunca escreve em disco, banco ou fila externa
2. OrchestratorAgent nunca chama LLM diretamente — delega ao ClassifierAgent
3. Todo output de agente passa por `ValidatorAgent` antes de seguir para a proxima etapa
4. Severidades validas: apenas `critica`, `alta`, `media`, `baixa`
5. Categorias validas: apenas as definidas em `directives/triagem_rules.md`
6. `implementation/` e obrigatorio neste projeto por ser multi-agent; leia o runbook ativo antes de refatorar fluxo
7. Testes devem rodar offline — sem API real, sem LLM real, sem servicos externos
8. CI + coverage sao obrigatorios antes de qualquer migracao para framework

## Protocolo de execucao

```
1. Receber IssueInput
2. OrchestratorAgent aciona ClassifierAgent
3. ValidatorAgent valida IssueClassification
4. OrchestratorAgent aplica regras de negocio deterministicas
5. ReporterAgent gera IssueReport
6. ValidatorAgent valida IssueReport
7. Retornar IssueReport aprovado ou falhou
8. Parar apenas quando gate aprovado OU 3 falhas consecutivas
```

## Gates de aprovacao

| Gate | Comando | O que valida |
|------|---------|-------------|
| Gate 1 | `python execution/run_onboarding_flow.py` | Ambiente basico e contratos |
| Gate 2 | `pytest tests/ -v --tb=short` | Testes offline sem LLM real |
| Gate 3 | `pytest tests/ -v --tb=short --cov=src --cov-report=term --cov-fail-under=80` | Coverage minima e regressao |

Ver criterios completos: `spec/03-design.md`.

## Arquivos criticos — ler antes de modificar

- `implementation/01-bootstrap-issue-triage.md` — plano minimo do fluxo atual
- `directives/triagem_rules.md` — categorias, severidades e restricoes
- `contracts/issue_contract.md` — significado documental dos contratos
- `src/contracts/issue_contract.py` — schema executavel em runtime
- `progress/PROGRESS.md` — memoria operacional
- `progress/VALIDATION_STATUS.md` — ultimo estado de validacao

## Eixo interativo vs programatico

- **Interativo:** editar diretivas, revisar prompts, ajustar contratos e arquitetura
- **Programatico:** `OrchestratorAgent`, `ClassifierAgent`, `ValidatorAgent` e `ReporterAgent`

Nao misturar: humano nao intervem no fluxo programatico depois que os gates basicos estao aprovados.
