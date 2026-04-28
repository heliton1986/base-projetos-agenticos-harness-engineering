# AGENTS.md — Issue Triage Agent

## Papel deste arquivo

Este arquivo define como a LLM deve se comportar ao trabalhar neste projeto.
Leia antes de qualquer implementacao, execucao ou modificacao.

## Identidade do sistema

- **Nome:** Issue Triage Agent
- **Tipo:** Sistema agentico com 3 subagentes especializados
- **Dominio:** Triagem e classificacao de issues de software
- **Stack:** Python + Anthropic API + Pydantic

## Modelo Operacional (DOE)

Este projeto segue `Diretivas + Orquestracao + Execucao`:

- **Diretivas** em `directives/` — categorias e severidades validas, nunca improvisar fora delas
- **Orquestracao** em `src/agents/orchestrator.py` — coordena fluxo, nao classifica
- **Execucao** em `src/agents/` — cada agente tem responsabilidade isolada e contrato tipado

## Agentes e responsabilidades

| Agente | Arquivo | Responsabilidade | Usa LLM? |
|--------|---------|-----------------|---------|
| OrchestratorAgent | `src/agents/orchestrator.py` | Coordena fluxo, roteia, agrega resultado | nao |
| ClassifierAgent | `src/agents/classifier_agent.py` | Classifica severidade e categoria via LLM | sim |
| ValidatorAgent | interno ao orchestrator | Valida IssueClassification contra contrato | nao |
| ReporterAgent | `src/agents/reporter_agent.py` | Formata IssueReport final | nao |

## Contratos de entrada e saida

- Entrada do sistema: `IssueInput` (texto livre + metadados opcionais)
- Saida do ClassifierAgent: `IssueClassification` (severidade + categoria + justificativa)
- Saida final: `IssueReport` (classificacao + metadados + timestamp)
- Contratos completos: `contracts/issue_contract.md`

## Regras que nunca podem ser violadas

1. ClassifierAgent retorna apenas `IssueClassification` — nunca escreve em disco ou banco
2. OrchestratorAgent nunca chama LLM diretamente — delega ao ClassifierAgent
3. Severidades validas: apenas `critica`, `alta`, `media`, `baixa` — sem valores fora da lista
4. Categorias validas: apenas as definidas em `directives/triagem_rules.md`
5. Se ClassifierAgent falhar 3 vezes consecutivas, fluxo para com erro explicito

## Protocolo de execucao

```
1. Receber IssueInput
2. OrchestratorAgent aciona ClassifierAgent
3. ClassifierAgent classifica via LLM
4. ValidatorAgent valida IssueClassification contra contrato
5. Se invalido: retentar ate 3x com contexto do erro
6. Se valido: ReporterAgent gera IssueReport
7. Retornar IssueReport
8. Parar apenas quando gate aprovado OU 3 falhas consecutivas
```

## Gates de aprovacao

Gate 1 — Ambiente: `run_onboarding_flow.py` passa sem erros
Gate 2 — Classificacao: `IssueClassification` valida (Pydantic sem erros)
Gate 3 — Report: `IssueReport` gerado com todos os campos obrigatorios

Ver criterios completos: `spec/03-design.md`.

## Eixo interativo vs programatico

- **Interativo (voce + Claude Pro):** editar directives, ajustar prompts do ClassifierAgent, revisar contratos
- **Programatico (codigo Python):** OrchestratorAgent, ClassifierAgent, ValidatorAgent, ReporterAgent — chamados por codigo, nao por humano

Nao misturar: humano nao intervem no fluxo programatico pos-gate-1.
