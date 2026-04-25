# Status da Base Harness

## Quando ler este documento

Ler antes de usar a base pela primeira vez e antes de criar qualquer projeto novo.
Responde: a base esta pronta para uso? O que e obrigatorio? O que ainda esta evoluindo?

## Objetivo

Registro sintetico do estado atual da base. Responde diretamente:

- o que ja esta maduro
- o que e obrigatorio vs complementar
- o que ainda pode evoluir

## Versao atual: v1.1

A base evoluiu de v1.0 para v1.1 com as seguintes adicoes:

- `AGENTS.md` proprio da base — contrato de comportamento da LLM ao usar a base
- `.claude/kb/` — 5 dominios de padroes prontos (doe, builder-validator, execution-protocol, model-routing, agent-contracts)
- 6 templates novos: `TEMPLATE_README.md`, `TEMPLATE_AGENTS.md`, `TEMPLATE_TASK_CONTRACT.md`, `TEMPLATE_SPEC_01/02/03`
- Reclassificacao de documentos: nucleo / obrigatorio / complementar
- `05_KB_MINIMA` promovido de complementar para obrigatorio
- `04_CHECKLIST` atualizado com checklist completo de artefatos por fase
- `README.md` atualizado com secao `.claude/kb/` e comportamento obrigatorio da LLM

## Diagnostico Geral

Base madura para uso real em projetos agenticos com multiplas sessoes, multiplos agentes e gates de validacao.

## O que esta maduro

### Nucleo conceitual

- framework (`01`)
- DOE (`02`)
- bootstrap (`03`)
- checklist com sequencia e templates obrigatorios (`04`)

### Padroes operacionais obrigatorios

- KB minima de projeto (`05`)
- builder/validator/loop de correcao (`06`)
- estrategia de modelos por agente (`10`)
- protocolo de execucao agentica (`11`)
- orquestrador e subagentes (`12`)
- observabilidade de modelos e agentes (`13`)
- fases de implementacao executaveis (`15`)

### Templates (todos obrigatorios, distintos por momento de uso)

| Momento | Templates |
|---------|-----------|
| Bootstrap | README, AGENTS, SPEC 01/02/03 |
| Antes de implementar | TASK_CONTRACT, FIRST_INCREMENTAL_CAPABILITY, IMPLEMENTATION_PHASE, DATA_CONTRACT |
| Antes de subir agentes | ONBOARDING_FLOW, MODEL_ROUTING |
| Durante sessoes | PROGRESS, VALIDATION_STATUS |

### KB operacional (.claude/kb/)

| Dominio | Conteudo |
|---------|---------|
| `doe/` | Template DOE e checklist de conformidade |
| `builder-validator/` | Ciclo builder→validator→loop por capacidade |
| `execution-protocol/` | Loop obrigatorio com tabela de decisao |
| `model-routing/` | Criterios e tabela de roteamento por agente |
| `agent-contracts/` | Template de contrato, audit_log e checklist |

### AGENTS.md da base

Contrato de comportamento da LLM ao usar a base. Define:
- sequencia de leitura obrigatoria ao criar projeto
- protocolo de execucao
- sequencia de criacao de projeto com templates
- regras que nunca podem ser violadas
- quando perguntar ao humano

## Classificacao atual dos documentos

### Nucleo

- `01_FRAMEWORK_PRATICO_HARNESS_AGENTIC_SYSTEMS.md`
- `02_DOE_OPERACIONAL_PARA_HARNESS.md`
- `03_BOOTSTRAP_PROJETO_AGENTICO.md`
- `04_CHECKLIST_PARA_GERAR_AGENTS_MD.md`
- `prompts/PROMPT_MESTRE_INICIAL.md`
- `prompts/PROMPTS_POR_FASE.md`

### Obrigatorio em todo projeto com gates e capacidades

- `05_KB_MINIMA_PARA_PROJETOS_AGENTICOS.md`
- `06_PADRAO_BUILDER_VALIDATOR_E_TASK_CONTRACTS.md`
- `10_ESTRATEGIA_DE_MODELOS_PARA_AGENTES.md`
- `11_PROTOCOLO_DE_EXECUCAO_AGENTICA.md`
- `12_ORQUESTRADOR_E_SUBAGENTES_PARA_FLUXOS_DE_EXECUCAO.md`
- `13_OBSERVABILIDADE_DE_MODELOS_E_AGENTES.md`
- `15_FASES_DE_IMPLEMENTACAO_EXECUTAVEIS.md`

### Complementar

- `07_FRONTEND_OBSERVAVEL_PARA_AGENTES.md`
- `08_ESTRUTURA_OPCIONAL_KB_REFERENCES_VISUALS_EXAMPLES.md`
- `09_TEMPLATES_PARA_BASE_HARNESS.md`
- `14_EXPANSAO_DE_PAPEIS_AGENTICOS.md`
- `prompts/EXEMPLOS_PREENCHIMENTO_PROMPT_MESTRE.md`

## Maturidade por dimensao

| Dimensao | Status |
|----------|--------|
| Conceitual | Alta |
| Operacional | Alta |
| Templates | Alta — 13 templates, todos com momento de uso definido |
| KB operacional | Alta — 5 dominios com index + quick-reference |
| Automacao | Media — gates e scripts existem, CI nao |
| Pronta para uso real | Sim |

## O que ainda pode evoluir

Sem bloquear v1.1:

- exemplos canonicos completos de projeto gerado com todos os templates
- convencoes de telemetria e custo por modelo
- KB adicional: `harness-patterns/` com padroes de projeto recorrentes
- `prompts/EXEMPLOS_PREENCHIMENTO_PROMPT_MESTRE.md` atualizado com exemplos usando templates

## Regra de atualizacao da base

Ao atualizar qualquer `.md`:
1. Atualizar a KB correspondente em `.claude/kb/`
2. Atualizar este `STATUS_DA_BASE_HARNESS.md`
3. Verificar se `04_CHECKLIST` e `AGENTS.md` precisam de ajuste

Em uma frase:

`A base v1.1 e suficientemente madura para iniciar projetos agenticos reais com estrutura, validacao, templates obrigatorios e padroes operacionais prontos para uso.`
