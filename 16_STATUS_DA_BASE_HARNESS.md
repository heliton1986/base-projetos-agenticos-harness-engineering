# Status da Base Harness

## Quando ler este documento

Ler antes de usar a base pela primeira vez e antes de criar qualquer projeto novo.
Responde: a base esta pronta para uso? O que e obrigatorio? O que ainda esta evoluindo?

## Objetivo

Registro sintetico do estado atual da base. Responde diretamente:

- o que ja esta maduro
- o que e obrigatorio vs complementar
- o que ainda pode evoluir

## Versao atual: v1.17.1

### Historico de evolucao significativa

**v1.1–v1.7:** estrutura inicial — AGENTS.md, KB (5 dominios), 13 templates, classificacao nucleo/obrigatorio/complementar, CI/coverage, parser LLM, ValidatorAgent, session DB, audit_log, testes offline.

**v1.8–v1.10:** adicao de padroes de orquestracao:
- `12_ORQUESTRADOR_E_SUBAGENTES.md` — 7 padroes + processos separados vs subagentes + loop autocorrecao com MAX_CICLOS
- `templates/TEMPLATE_LANGGRAPH.md` — create_react_agent + dual-store routing + docstring-as-spec
- `templates/TEMPLATE_CHAINLIT.md` — lifecycle hooks + astream_events + cl.Step transparency
- `.claude/kb/autonomy-guardrails/` — dominio KB com guardrail/constraint, checklist

**v1.11–v1.17:** adicao de fundamentos de autonomia e progressao:
- `17_POR_QUE_FASE_MANUAL_ANTES_DO_FRAMEWORK.md` — Software 1.0/2.0/3.0, fundamentacao progressao manual→framework
- `18_AUTONOMIA_AGENTICA_E_GUARDRAILS.md` — Convergence Formula, 3 principios SDD, JIT Context, "every continue is harness failure", Human Triad, docstring-as-spec, guardrail vs constraint, Tool/Agent/Workflow taxonomy
- `15_FASES_DE_IMPLEMENTACAO_EXECUTAVEIS.md` — `implementation/` obrigatorio para projetos multi-agent
- `11_` + `13_`: padrao narrativa no chat (checklist por etapa, agente+modelo, tabelas)
- Todos os prompts atualizados com refs a 11_/13_/15_/17_/18_
- Total: 21 templates obrigatorios

**v1.17.1:** endurecimento da camada `implementation/`:
- `15_FASES_DE_IMPLEMENTACAO_EXECUTAVEIS.md` agora explicita que titulo + 1 frase nao contam como fase executavel valida
- `templates/TEMPLATE_IMPLEMENTATION_PHASE.md` agora inclui regra de completude minima
- `AGENTS.md`, `README.md` e prompts passaram a tratar placeholder curto em `implementation/` como artefato incompleto

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
- por que fase manual antes do framework (`17`)
- autonomia agentica e guardrails (`18`)

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
- `17_POR_QUE_FASE_MANUAL_ANTES_DO_FRAMEWORK.md`
- `18_AUTONOMIA_AGENTICA_E_GUARDRAILS.md`

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
| Templates | Alta — 21 templates, todos com momento de uso definido |
| KB operacional | Alta — 6 dominios com index + quick-reference (inclui autonomy-guardrails) |
| Automacao | Alta — gates, scripts, CI/coverage 80% obrigatorio |
| Pronta para uso real | Sim |

## O que ainda pode evoluir

Aguardando validacao em D4 (Semana AI):

- `templates/TEMPLATE_CREWAI.md` — stack: crewai + crewai-tools + anthropic
- `templates/TEMPLATE_LANGFUSE.md` — langfuse>=2.50.0, trace→observe→optimize
- deepeval (`assert score > 0.85`) — avaliar se entra na base apos D4
- Context decay / Attention Budget — extrair apos Semana AI concluida

Sem data:

- exemplos canonicos completos de projeto gerado com todos os templates
- convencoes de telemetria e custo por modelo

## Regra de atualizacao da base

Ao atualizar qualquer `.md`:
1. Atualizar a KB correspondente em `.claude/kb/`
2. Atualizar este `STATUS_DA_BASE_HARNESS.md`
3. Verificar se `04_CHECKLIST` e `AGENTS.md` precisam de ajuste

Em uma frase:

`A base v1.17.1 cobre o ciclo completo: bootstrap, implementacao faseada, validacao deterministica, orquestracao multi-agent, autonomia com guardrails, e progressao manual→framework — pronta para projetos agenticos reais.`
