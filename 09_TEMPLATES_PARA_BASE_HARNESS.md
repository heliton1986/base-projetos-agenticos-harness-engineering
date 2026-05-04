# Templates para a Base Harness

## Objetivo

Este documento explica a camada de `templates/` na base de projetos agenticos com Harness Engineering.

Templates nao substituem prompts nem bootstrap. Funcionam como moldes obrigatorios para reduzir ambiguidade e variabilidade na geracao de artefatos importantes.

## Regra curta

- `prompts/` dizem o que gerar e em que fase
- `templates/` dizem qual estrutura o arquivo final deve seguir
- **Nunca gerar artefato do zero — sempre usar o template correspondente**

## Por que templates sao obrigatorios

Sem templates, a LLM inventa o formato de cada artefato a cada projeto. Isso gera:

- README sem secoes criticas (DOE, protocolo, gates)
- AGENTS.md generico sem contrato de comportamento real
- spec sem criterios verificaveis
- contratos sem campos de audit obrigatorios

Com templates, o formato e consistente entre projetos e a LLM nao precisa decidir estrutura — so preencher conteudo especifico do dominio.

## Todos os templates existentes

### Antes de qualquer codigo (bootstrap)

| Template | Gera | Obrigatorio |
|----------|------|-------------|
| `TEMPLATE_README.md` | `README.md` do projeto | Sim — dia 1 |
| `TEMPLATE_AGENTS.md` | `AGENTS.md` do projeto | Sim — dia 1 |
| `TEMPLATE_SPEC_01_BRAINSTORM.md` | `spec/01-brainstorm.md` | Sim — dia 1 |
| `TEMPLATE_SPEC_02_DEFINE.md` | `spec/02-define.md` | Sim — dia 1 |
| `TEMPLATE_SPEC_03_DESIGN.md` | `spec/03-design.md` | Sim — dia 1 |

### Antes de implementar cada capacidade

| Template | Gera | Obrigatorio |
|----------|------|-------------|
| `TEMPLATE_TASK_CONTRACT.md` | `contracts/[capacidade].md` | Sim — por agente |
| `TEMPLATE_FIRST_INCREMENTAL_CAPABILITY.md` | definicao da menor entrega | Sim — antes de codar |
| `TEMPLATE_IMPLEMENTATION_PHASE.md` | `implementation/phase-N.md` | Sim — por fase |
| `TEMPLATE_DATA_CONTRACT.md` | contrato de dados | Sim — se ha dados sensiveis |

### Antes de subir qualquer agente

| Template | Gera | Obrigatorio |
|----------|------|-------------|
| `TEMPLATE_ONBOARDING_FLOW.md` | `execution/run_onboarding_flow.py` | Sim |
| `TEMPLATE_MODEL_ROUTING.md` | tabela de modelos por agente | Sim — antes de codar |

### Durante e entre sessoes

| Template | Gera | Obrigatorio |
|----------|------|-------------|
| `TEMPLATE_PROGRESS.md` | `progress/PROGRESS.md` | Sim — atualizar por sessao |
| `TEMPLATE_VALIDATION_STATUS.md` | status dos gates | Sim — atualizar por gate |

## Estrutura atual da pasta templates/

```
templates/
  TEMPLATE_README.md
  TEMPLATE_AGENTS.md
  TEMPLATE_TASK_CONTRACT.md
  TEMPLATE_SPEC_01_BRAINSTORM.md
  TEMPLATE_SPEC_02_DEFINE.md
  TEMPLATE_SPEC_03_DESIGN.md
  TEMPLATE_PROGRESS.md
  TEMPLATE_VALIDATION_STATUS.md
  TEMPLATE_FIRST_INCREMENTAL_CAPABILITY.md
  TEMPLATE_DATA_CONTRACT.md
  TEMPLATE_ONBOARDING_FLOW.md
  TEMPLATE_MODEL_ROUTING.md
  TEMPLATE_IMPLEMENTATION_PHASE.md
```

## Relacao com outros artefatos da base

- `04_CHECKLIST_PARA_GERAR_AGENTS_MD.md` — lista qual template usar em cada etapa do checklist
- `prompts/base-generica/PROMPTS_FASEADOS_BASE.md` — define quando acionar cada template por fase
- `.claude/kb/` — padroes prontos que complementam os templates com quick-references

## Conclusao

Templates sao obrigatorios — nao opcionais. A diferenca e o momento de uso, nao a opcionalidade.

Em uma frase:

`Prompts dizem quando e como gerar; templates dizem qual formato seguir — e nenhum artefato deve nascer sem o seu template.`

## Como templates evitam invencao fora do escopo

Templates forcam definicao explicita de:

- entradas e saidas por agente
- contratos de dados com campos de mascaramento
- gates com criterios verificaveis
- politica de ambiguidade
- audit_log obrigatorio

Sem isso, a LLM preenche lacunas com suposicoes — que e exatamente o que a base existe para evitar.
