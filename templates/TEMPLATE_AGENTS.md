# AGENTS.md — [NOME DO PROJETO]

## Papel deste arquivo

Este arquivo define como a LLM deve se comportar ao trabalhar neste projeto.
Deve ser lido antes de qualquer implementacao, execucao ou modificacao de codigo.

## Identidade do sistema

- **Nome:** [NOME DO PROJETO]
- **Tipo:** Sistema agentico com [N] subagentes especializados
- **Dominio:** [dominio de negocio]
- **Stack:** [tecnologias principais]

## Modelo Operacional (DOE)

Este projeto segue o modelo `Diretivas + Orquestracao + Execucao`:

- **Diretivas** estao em `directives/` — nunca improvisar fora dessas fronteiras
- **Orquestracao** esta em `src/agents/orchestrator.py`
- **Execucao** esta em `src/agents/` — cada agente tem responsabilidade isolada

## Agentes e responsabilidades

| Agente | Arquivo | Responsabilidade | Usa LLM? |
|--------|---------|-----------------|---------|
| OrchestratorAgent | `src/agents/orchestrator.py` | Coordena fluxo, roteia para subagentes | [sim/nao] |
| [SubagenteA] | `src/agents/[nome].py` | [responsabilidade] | [sim/nao] |
| [SubagenteB] | `src/agents/[nome].py` | [responsabilidade] | [sim/nao] |
| AuditAgent | `src/agents/audit_agent.py` | Registra toda operacao — imutavel | nao |

## Contratos de entrada e saida

Cada agente recebe e retorna tipos definidos em `src/db/models.py`.
Nunca alterar a assinatura de um agente sem atualizar o contrato correspondente em `contracts/`.

## Regras que nunca podem ser violadas

1. [Regra critica 1 — ex: nao alterar dados na fonte]
2. [Regra critica 2 — ex: audit_log e imutavel, apenas INSERT]
3. [Regra critica 3 — ex: dados sensiveis mascarados antes do LLM]

## Protocolo de execucao

Quando um fluxo executavel for acionado:

```
1. Executar
2. Capturar saida e erros
3. Se erro local e baixo risco → corrigir → reexecutar
4. Validar
5. Reportar no chat
6. Parar apenas quando gate aprovado OU bloqueio real
```

Bloqueio real: ambiguidade de regra de negocio, credencial ausente, risco de escrita indevida.

## Gates de aprovacao

Ver `spec/05-validate.md` para criterios completos por gate.

| Gate | Comando | O que valida |
|------|---------|-------------|
| Gate 1 | `python execution/run_onboarding_flow.py` | Infraestrutura e conexoes |
| Gate 2 | `pytest tests/smoke/test_[capacidade].py` | [capacidade] |

## Estrategia de modelos

| Agente | Modelo | Justificativa |
|--------|--------|--------------|
| [Agente LLM] | [modelo] | [razao] |
| Demais | Sem LLM | Logica deterministica — sem custo de LLM |

## Arquivos criticos — ler antes de modificar

- `directives/domain.md` — regras do dominio
- `directives/business-rules.md` — regras de negocio
- `directives/output-contracts.md` — formatos de saida
- `contracts/` — contratos de dados por capacidade
- `spec/05-validate.md` — gates de aprovacao

## Como a LLM deve agir ao receber uma tarefa

1. Ler este arquivo e os arquivos criticos relevantes
2. Verificar se a tarefa esta dentro das diretivas
3. Identificar qual agente e fase corresponde
4. Executar seguindo o protocolo de execucao
5. Reportar resultado com evidencias
6. Nao avancar sem gate aprovado
