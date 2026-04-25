# [NOME DO PROJETO]

## Visao Geral

Descreva o que o sistema faz em 2-3 frases. Inclua: o problema que resolve, quem usa, e o resultado principal.

Construido com `Harness Engineering`: [papeis dos agentes] + validacao independente + trilha de auditoria.

## Objetivo

Descreva o objetivo operacional central. O que o sistema automatiza ou resolve?

## Usuario ou Operacao Alvo

- [Perfil 1]
- [Perfil 2]

## Arquitetura Resumida

```
[Componente de entrada]
      |
      v
[OrchestratorAgent]
      |
      +---> [SubagenteA]   ([responsabilidade])
      +---> [SubagenteB]   ([responsabilidade])
      +---> [SubagenteC]   ([responsabilidade])
      |
      v
[Camada de persistencia]
```

**Regra central:** [regra principal do dominio — o que nunca pode acontecer automaticamente]

## Stack

| Camada | Tecnologia |
|--------|-----------|
| Frontend | [ex: Streamlit] |
| API | [ex: FastAPI] |
| LLM | [ex: Claude claude-sonnet-4-6] |
| Agentes | [ex: LangChain] |
| Banco de dados | [ex: PostgreSQL] |
| Validacao | pytest + contratos de dados |

## Modelo Operacional DOE

- **Diretivas** (`directives/`): regras do dominio, restricoes, politicas, contratos de saida, casos extremos.
- **Orquestracao** (`src/agents/orchestrator.py`): coordena subagentes, define fluxo, nao executa logica de negocio.
- **Execucao** (`src/agents/`): cada subagente executa uma responsabilidade isolada com contrato tipado.

Ref: `base/02_DOE_OPERACIONAL_PARA_HARNESS.md`

## Padrao Builder / Validator / Loop de Correcao

```
Builder    → constroi o artefato
Validator  → valida contra o contrato esperado
Loop       → se falhar: corrigir → reexecutar → revalidar
Gate       → aprovado quando todos os criterios passam
```

Contratos: `contracts/`. Gates: `spec/05-validate.md`.

Ref: `base/06_PADRAO_BUILDER_VALIDATOR_E_TASK_CONTRACTS.md`

## Estrategia de Modelos por Agente

| Agente | Modelo | Justificativa |
|--------|--------|--------------|
| [Agente que usa LLM] | [modelo] | [por que LLM aqui] |
| [Demais agentes] | Sem LLM | Logica deterministica |

Ref: `base/10_ESTRATEGIA_DE_MODELOS_PARA_AGENTES.md`

## Orquestrador e Subagentes

```
[OrchestratorAgent]
  → [SubagenteA]  (contrato: [TipoResponse])
  → [SubagenteB]  (contrato: [TipoResponse])
  → [SubagenteC]  (contrato: [TipoResponse])
```

Ref: `base/12_ORQUESTRADOR_E_SUBAGENTES_PARA_FLUXOS_DE_EXECUCAO.md`

## Observabilidade

Cada operacao registra em `audit_log`: agente, operacao, status, duration_ms, input_summary, output_summary, error_message.

Ref: `base/13_OBSERVABILIDADE_DE_MODELOS_E_AGENTES.md`

## Fases de Implementacao

| Fase | Arquivo | Objetivo |
|------|---------|---------|
| 1 | `implementation/phase-01-bootstrap.md` | [objetivo] |
| 2 | `implementation/phase-02-[nome].md` | [objetivo] |
| 3 | `implementation/phase-03-[nome].md` | [objetivo] |

Ref: `base/15_FASES_DE_IMPLEMENTACAO_EXECUTAVEIS.md`

## Como Rodar

```bash
cp .env.example .env
# Editar .env com credenciais
pip install -r requirements.txt
python execution/run_onboarding_flow.py
```

## Estrutura do Projeto

```
README.md
AGENTS.md
.env.example
requirements.txt
directives/
spec/
implementation/
execution/
contracts/
src/
tests/
progress/
docs/
```

## Restricoes Importantes

1. **[Restricao 1]:** [descricao]
2. **[Restricao 2]:** [descricao]

## Diretivas de Dominio

Ver `directives/` — especialmente:
- `directives/domain.md`
- `directives/business-rules.md`
- `directives/output-contracts.md`

## Validacao

```bash
python execution/run_onboarding_flow.py
pytest tests/ -v --tb=short
python execution/validate_connections.py
```

Gates: ver `spec/05-validate.md`

## Protocolo de Execucao Agentica

Quando um fluxo executavel for acionado, a LLM opera como operador assistido:

```
1. Executar o fluxo
2. Capturar saida e erros
3. Se erro local e baixo risco → corrigir → reexecutar
4. Rodar validacao
5. Reportar: o que executou, falhou, corrigiu, estado atual
6. Parar apenas quando: gate aprovado OU bloqueio real
```

Ref: `base/11_PROTOCOLO_DE_EXECUCAO_AGENTICA.md`

## Regra de Ouro

Nao implementar tudo de uma vez. Sequencia obrigatoria:

1. Definir (spec + diretivas)
2. Estruturar (bootstrap)
3. Validar a base (Gate 1)
4. Implementar incrementalmente
5. Validar cada capacidade antes de avancar
