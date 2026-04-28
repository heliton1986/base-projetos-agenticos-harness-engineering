# Spec 02 — Define: Issue Triage Agent

## Objetivo refinado

Classificar issues de software (texto livre) em severidade e categoria validas, com validacao de contrato e loop de correcao, gerando IssueReport auditavel.

## Escopo

**Incluido:**
- Receber `IssueInput` (texto + metadados opcionais)
- Classificar via `ClassifierAgent` (LLM)
- Validar via `ValidatorAgent` (Pydantic + regras de negocio)
- Loop de correcao: ate 3 tentativas
- Gerar `IssueReport` com status e trilha de tentativas

**Excluido (v1):**
- Persistencia em banco de dados
- Interface web ou API REST
- Integracoes externas (GitHub, Jira, Slack)

## Stack

| Camada | Escolha | Justificativa |
|--------|---------|--------------|
| LLM | claude-sonnet-4-6 (Anthropic) | Raciocinio sobre texto ambiguo |
| Validacao | Pydantic v2 | Schema + validadores customizados |
| Testes | pytest | Padrao do ecossistema Python |
| Persistencia | JSON em disco | Simplicidade canonica, sem dependencias |

## Restricoes

- Sem estado entre chamadas (stateless)
- ClassifierAgent nunca escreve em disco
- Maximo 3 tentativas de classificacao por issue
- Tempo de resposta: sem SLA na v1 (demonstracao)

## Riscos identificados

| Risco | Probabilidade | Mitigacao |
|-------|--------------|-----------|
| LLM retorna valor fora do contrato | Media | Pydantic + loop de correcao |
| Issue muito vaga para classificar | Alta | Campo `confianca: baixa` no contrato |
| API Anthropic indisponivel | Baixa | Erro explicito, sem fallback silencioso |

## Criterio de pronto (v1)

- `run_onboarding_flow.py` passa todos os gates
- 5 issues de exemplo classificadas corretamente
- Nenhum valor fora do contrato chegando ao IssueReport final
