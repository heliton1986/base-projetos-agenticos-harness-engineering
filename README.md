# Base para Projetos Agenticos com Harness Engineering

## Objetivo

Este diretório reúne uma base reutilizável para iniciar, estruturar e evoluir projetos agenticos com foco em `Harness Engineering`.

A baseline oficial desta base agora e o pacote `recomendado`.


A base foi organizada para ajudar em quatro frentes:

- pensar arquitetura de sistemas agenticos
- estruturar bootstrap de novos projetos
- orientar a criação de `AGENTS.md`, `README.md`, `spec/` e diretivas
- reduzir improvisação na criação de projetos com LLMs

## Pasta .claude/kb/

A pasta `.claude/kb/` contem padroes operacionais prontos para uso imediato — resumos densos derivados dos `.md` da base.

**Papel:** os `.md` explicam o porque e quando aplicar. A KB entrega o padrao pronto para copiar e usar agora.
**Regra:** os `.md` sao a fonte de verdade. Quando houver conflito, o `.md` prevalece.

| Dominio | Proposito |
|---------|-----------|
| `doe/` | Template DOE e checklist de conformidade |
| `builder-validator/` | Ciclo builder→validator→loop pronto por capacidade |
| `execution-protocol/` | Loop obrigatorio de execucao com tabela de decisao |
| `model-routing/` | Criterios e tabela de roteamento de modelos por agente |
| `agent-contracts/` | Template de contrato, audit_log e checklist por agente |
| `autonomy-guardrails/` | Guardrail vs constraint, Tool/Agent/Workflow, docstring-as-spec, loop de autocorrecao |

Cada dominio tem `index.md` (contexto) e `quick-reference.md` (padrao pronto para usar).

## Como ler esta base

Se for a primeira vez usando a base, a ordem recomendada é:

1. `01_FRAMEWORK_PRATICO_HARNESS_AGENTIC_SYSTEMS.md`
2. `02_DOE_OPERACIONAL_PARA_HARNESS.md`
3. `03_BOOTSTRAP_PROJETO_AGENTICO.md`
4. `04_CHECKLIST_PARA_GERAR_AGENTS_MD.md`
5. `prompts/PROMPT_MESTRE_INICIAL.md`
6. `prompts/PROMPTS_POR_FASE.md`

Depois, conforme a necessidade, use os documentos complementares.

## Nucleo da base

### 01_FRAMEWORK_PRATICO_HARNESS_AGENTIC_SYSTEMS.md

Define os principios gerais para construir sistemas agenticos com harness.

### 02_DOE_OPERACIONAL_PARA_HARNESS.md

Define o modelo operacional em `Diretivas`, `Orquestracao` e `Execucao`.

### 03_BOOTSTRAP_PROJETO_AGENTICO.md

Define como um novo projeto deve nascer e qual pacote estrutural usar: recomendado ou completo.

### 04_CHECKLIST_PARA_GERAR_AGENTS_MD.md

Ajuda a transformar a base em um `AGENTS.md` especifico de projeto. **Obrigatorio antes de gerar README e AGENTS.md.**

## Documentos obrigatorios em todo projeto com gates e capacidades

### 06_PADRAO_BUILDER_VALIDATOR_E_TASK_CONTRACTS.md

Formaliza contratos de tarefa, gates, builder, validator e loop de correcao. Sem isso, gates viram checklist estatico sem execucao real.

### 10_ESTRATEGIA_DE_MODELOS_PARA_AGENTES.md

Define como pensar selecao de modelos por papel, custo, latencia, risco e criticidade da validacao. Definir antes de implementar qualquer agente.

### 11_PROTOCOLO_DE_EXECUCAO_AGENTICA.md

Define como a LLM deve executar, corrigir, reexecutar, validar e reportar fluxos operacionais quando o usuario pedir um script ou fluxo do projeto.

### 12_ORQUESTRADOR_E_SUBAGENTES_PARA_FLUXOS_DE_EXECUCAO.md

Explicita como distribuir a execucao agentica entre orquestrador e subagentes, e como isso se conecta a handoff e estrategia de modelos.

### 13_OBSERVABILIDADE_DE_MODELOS_E_AGENTES.md

Define como registrar e exibir agente, modelo, provider, status, retries e validacao no chat e no frontend.

### 15_FASES_DE_IMPLEMENTACAO_EXECUTAVEIS.md

Explica como usar fases executaveis para guiar a LLM por etapas de implementacao incrementais e verificaveis.

### 17_POR_QUE_FASE_MANUAL_ANTES_DO_FRAMEWORK.md

Fundamenta a progressao obrigatoria: dominio + contratos + testes + CI → framework. Explica por que pipeline manual nao e desperdicio — e a base que o framework pressupoe. Inclui as tres eras de controle (Software 1.0/2.0/3.0) e por que controle por especificacao escala onde autoria e configuracao nao escalam.

### 18_AUTONOMIA_AGENTICA_E_GUARDRAILS.md

Formaliza: guardrail vs constraint, Tool vs Agent vs Workflow, feed forward vs feedback, docstring como spec do agente, Convergence Formula (∞ paths × gates = 1 outcome), 3 principios SDD (Context=Constraint, Test Loop=Convergencia, Gates=Fronteira Rigida), Just-in-Time Context, "every continue is a harness failure", Human Triad (triagem + observabilidade + metaprogramacao). Ler antes de qualquer decisao de arquitetura agentica.

## Documentos complementares

### 05_KB_MINIMA_PARA_PROJETOS_AGENTICOS.md

Explica quando e como usar uma `kb/` minima em projetos agenticos.

### 07_FRONTEND_OBSERVAVEL_PARA_AGENTES.md

Formaliza a ideia de mostrar agentes, subagentes, validacao e progresso no frontend.

### 08_ESTRUTURA_OPCIONAL_KB_REFERENCES_VISUALS_EXAMPLES.md

Explica a camada opcional de apoio com `kb/`, `references/`, `visuals/` e `examples/`.

### 09_TEMPLATES_PARA_BASE_HARNESS.md

Explica por que faz sentido criar templates para artefatos recorrentes.

### 14_EXPANSAO_DE_PAPEIS_AGENTICOS.md

Explica como criar novos tipos de agentes na base sem perder clareza, handoff, validacao e estrategia de modelos.

## Pasta prompts/

A pasta `prompts/` reúne os prompts reutilizáveis para usar a base.

### PROMPT_MESTRE_INICIAL.md

Prompt de **definicao** — para apos Fase 1 e aguarda aprovacao antes de criar arquivos. Indicado para projetos com dominio a explorar.

### PROMPT_NOVO_PROJETO.md

Prompt de **execucao autonoma** — cria o projeto completo do zero sem aprovacao fase a fase, com gates embutidos e obrigatorios. Indicado para projetos com brief claro e dominio conhecido.

### PROMPTS_POR_FASE.md

Prompts **modulares** — um por fase (definicao, bootstrap, validacao, implementacao, expansao). Usar quando quiser controle granular aprovando fase por fase.

### EXEMPLOS_PREENCHIMENTO_PROMPT_MESTRE.md

Exemplos prontos de preenchimento dos campos dos prompts acima. Usar como referencia — nunca enviar como prompt diretamente.

**Ordem de uso:**
- Dominio incerto: `PROMPT_MESTRE_INICIAL.md` → `PROMPTS_POR_FASE.md`
- Brief claro: `PROMPT_NOVO_PROJETO.md` direto
- Referencia de preenchimento: `EXEMPLOS_PREENCHIMENTO_PROMPT_MESTRE.md` (consulta, nao prompt)

## Pasta exemplos/

A pasta `exemplos/` contem projetos canonicos completos — demonstracoes end-to-end da base aplicada.

- `exemplos/canonical-minimal/` — Issue Triage Agent: projeto minimo com README, AGENTS.md, directives, spec, contracts, src/agents, execution/run_onboarding_flow.py, model_routing.yaml. Referencia de como um projeto derivado deve ser estruturado.

## Pasta tools/

A pasta `tools/` contem ferramentas de suporte a gestao da base e dos projetos derivados.

- `tools/validate_harness_project.py` — validador automatico de conformidade Harness Engineering. Verifica 11 criterios (estrutura, conteudo, portabilidade). Uso: `python tools/validate_harness_project.py <caminho-do-projeto>`

## Pasta templates/

A pasta `templates/` guarda moldes obrigatorios para reduzir variabilidade na geracao dos artefatos.
**Todos os 21 templates sao obrigatorios** — a diferenca e o momento de uso e a capacidade requerida pelo projeto, nao a opcionalidade.
Use o template correspondente antes de gerar cada artefato. Nunca gerar do zero sem template.

### Antes de qualquer codigo (bootstrap)

- `TEMPLATE_README.md` — estrutura completa do README com DOE, protocolo, gates e regras
- `TEMPLATE_AGENTS.md` — contrato de comportamento da LLM no projeto
- `TEMPLATE_SPEC_01_BRAINSTORM.md` — captura de ideias e hipoteses antes do design
- `TEMPLATE_SPEC_02_DEFINE.md` — requisitos verificaveis e criterios de aceite
- `TEMPLATE_SPEC_03_DESIGN.md` — arquitetura, stack, modelo de dados e decisoes de design

### Antes de implementar cada capacidade

- `TEMPLATE_TASK_CONTRACT.md` — contrato de tarefa por agente (entrada, saida, gate, audit)
- `TEMPLATE_FIRST_INCREMENTAL_CAPABILITY.md` — definicao da menor capacidade util e verificavel
- `TEMPLATE_IMPLEMENTATION_PHASE.md` — estrutura de fase com pre-condicoes, passos e gate
- `TEMPLATE_DATA_CONTRACT.md` — contrato de dados (campos, mascaramento, saida consolidada)

### Antes de subir qualquer agente

- `TEMPLATE_ONBOARDING_FLOW.md` — script de onboarding com validacao de conexoes e smoke tests
- `TEMPLATE_MODEL_ROUTING.md` — roteamento de modelos por agente e operacao

### Durante e entre sessoes

- `TEMPLATE_PROGRESS.md` — estado atual, o que foi feito, bloqueios, proximo passo
- `TEMPLATE_VALIDATION_STATUS.md` — status dos gates por fase
- `TEMPLATE_EXECUTION_RUNNER.md` — runner narrativo com saida em tempo real por fase e gate
- `TEMPLATE_TESTS.md` — padrao de testes offline (sem DB, sem LLM) por tipo de agente
- `TEMPLATE_KB.md` — estrutura de kb/ por ferramenta com index e quick-reference

### Por capacidade (usar quando o projeto requer)

- `TEMPLATE_CI.md` — GitHub Actions com pytest + coverage minimo 80% (obrigatorio antes de migrar para framework)
- `TEMPLATE_FASTAPI.md` — API REST com upload de arquivo, health check, error handling
- `TEMPLATE_STREAMLIT.md` — UI web para upload, visualizacao e download de relatorios
- `TEMPLATE_LANGGRAPH.md` — agente ReAct com decisao autonoma de tools, dual-store routing, docstring-as-spec
- `TEMPLATE_CHAINLIT.md` — interface conversacional com streaming token a token e tool steps visiveis

## O que e nucleo e o que e opcional

### Nucleo

- `01_FRAMEWORK_PRATICO_HARNESS_AGENTIC_SYSTEMS.md`
- `02_DOE_OPERACIONAL_PARA_HARNESS.md`
- `03_BOOTSTRAP_PROJETO_AGENTICO.md`
- `04_CHECKLIST_PARA_GERAR_AGENTS_MD.md` — obrigatorio antes de gerar README e AGENTS.md
- `prompts/PROMPT_MESTRE_INICIAL.md`
- `prompts/PROMPTS_POR_FASE.md`

### Obrigatorio em todo projeto com gates e capacidades

- `05_KB_MINIMA_PARA_PROJETOS_AGENTICOS.md` — sem isso a LLM repete reexplicacoes a cada sessao e preenche lacunas com suposicoes
- `06_PADRAO_BUILDER_VALIDATOR_E_TASK_CONTRACTS.md` — sem isso gates viram checklist estatico sem execucao real
- `10_ESTRATEGIA_DE_MODELOS_PARA_AGENTES.md` — definir antes de implementar qualquer agente
- `11_PROTOCOLO_DE_EXECUCAO_AGENTICA.md` — comportamento da LLM ao operar fluxos
- `12_ORQUESTRADOR_E_SUBAGENTES_PARA_FLUXOS_DE_EXECUCAO.md` — handoff entre agentes e distribuicao de execucao
- `13_OBSERVABILIDADE_DE_MODELOS_E_AGENTES.md` — rastreabilidade de agente, modelo, status e retries
- `15_FASES_DE_IMPLEMENTACAO_EXECUTAVEIS.md` — guia incremental de entrega por fases verificaveis
- `17_POR_QUE_FASE_MANUAL_ANTES_DO_FRAMEWORK.md` — progressao obrigatoria dominio+contratos+CI antes do framework
- `18_AUTONOMIA_AGENTICA_E_GUARDRAILS.md` — guardrail vs constraint, Tool/Agent/Workflow, loop autocorrecao, docstring-as-spec

### Padroes obrigatorios de execucao (derivados de projetos reais)

- **ValidatorAgent como gate entre fases** — revalida contrato Pydantic de saida de cada agente antes de passar ao proximo. Padrao em `AGENTS.md` e `TEMPLATE_EXECUTION_RUNNER.md`
- **Sessao DB unica no runner** — `run_flow.py` abre sessao e passa para todas as fases. Nunca delegar ao OrchestratorAgent
- **audit_log por agente** — cada agente registra acao, status e detalhe ao final da sua execucao
- **Testes offline obrigatorios** — sem DB, sem LLM, rodam em < 5s. Padrao em `TEMPLATE_TESTS.md`
- **CI + coverage minimo 80%** — GitHub Actions rodando pytest a cada push, bloqueando merge se falhar. Obrigatorio antes de qualquer migracao para framework. Padrao em `TEMPLATE_CI.md`

### Complementar

- `07_FRONTEND_OBSERVAVEL_PARA_AGENTES.md`
- `08_ESTRUTURA_OPCIONAL_KB_REFERENCES_VISUALS_EXAMPLES.md`
- `09_TEMPLATES_PARA_BASE_HARNESS.md`
- `14_EXPANSAO_DE_PAPEIS_AGENTICOS.md`

## Como usar para iniciar um projeto novo

Fluxo recomendado:

1. ler o nucleo da base
2. usar o `PROMPT_MESTRE_INICIAL.md`
3. definir o projeto sem implementar de imediato
4. usar os `PROMPTS_POR_FASE.md`
5. bootstrapar o projeto com `README.md`, `directives/`, `spec/`, `implementation/`, `execution/`, `AGENTS.md`
6. **usar `04_CHECKLIST_PARA_GERAR_AGENTS_MD.md` para validar que README e AGENTS.md cobrem todos os contratos antes de implementar** — sem esse passo, artefatos ficam incompletos
7. **definir estrategia de modelos por agente antes de implementar** (`10_ESTRATEGIA_DE_MODELOS_PARA_AGENTES.md`) — evita colocar LLM onde logica deterministica basta
8. validar a base antes de implementar a primeira capacidade
9. quando a primeira capacidade existir, expor um comando unico de onboarding para primeira execucao

## Estrutura esperada de um novo projeto

Como ponto de partida, a base recomenda o pacote `recomendado`, com pelo menos:

```text
README.md
AGENTS.md
.env.example
directives/
spec/
implementation/
execution/
tests/
progress/
docs/
```

Dependendo do caso, o projeto pode crescer para incluir:

```text
contracts/
evals/
observability/
kb/
templates/
examples/
```

## Regra de ouro

Nao usar a base para pedir um sistema inteiro de uma vez.

A base foi desenhada para funcionar melhor com a sequencia:

1. definir
2. estruturar
3. validar a base
4. implementar incrementalmente
5. validar de novo

## Comportamento obrigatorio da LLM ao executar fluxos

Este item nao e opcional. Sempre que houver um fluxo executavel no projeto (`run_onboarding_flow.py`, `pytest`, gate, script de validacao), a LLM deve operar como operador assistido — nao apenas sugerir comandos.

Loop obrigatorio:

```
1. Executar o fluxo
2. Capturar saida e erros
3. Se erro for local e baixo risco → corrigir → reexecutar
4. Rodar validacao associada
5. Reportar no chat: o que executou, o que falhou, o que corrigiu, estado atual
6. Parar apenas quando: gate aprovado OU bloqueio real
```

Bloqueio real = ambiguidade de regra de negocio, credencial ausente, risco de escrita indevida, conflito de escopo. Nesses casos: parar e perguntar objetivamente.

Detalhe completo: `11_PROTOCOLO_DE_EXECUCAO_AGENTICA.md`

### Protocolo narrativo no chat (obrigatorio)

Output do Bash fica colapsado na UI — tabela no chat e a unica visibilidade completa para o usuario.

**Antes de cada tool call:** anunciar em 1-2 linhas o que vai executar, qual agente, qual modelo (se LLM), o que se espera.

**Depois de cada fase:** imprimir tabela no chat com modelo usado, itens processados, resultado por agente:

```
[Fase 3 — Deteccao] CONCLUIDA ✓
| Agente        | Modelo            | Resultado                                                   |
|---------------|-------------------|-------------------------------------------------------------|
| DetectorAgent | claude-sonnet-4-6 | 2 inconsistencias: duplicata_suspeita [critica], descricao_suspeita [media] |

[Fase 4 — Relatorio] CONCLUIDA ✓
| Agente        | Status         | Total lancamentos | Total inconsistencias |
|---------------|----------------|-------------------|-----------------------|
| ReporterAgent | requer_revisao | 9                 | 2                     |
```

Regra: nunca executar tool call silenciosamente. Sempre tabela de resultado depois de cada fase — nao so APROVADO/FALHOU.

Padrao completo com formato de fase/gate: `AGENTS.md` — secao "Protocolo narrativo no chat".

## Estado atual da base

Ver `16_STATUS_DA_BASE_HARNESS.md` para avaliacao sintetica do que esta maduro, o que e obrigatorio vs complementar, e o que ainda pode evoluir.

## Conclusao

Esta base existe para transformar projetos agenticos em algo menos improvisado, mais rastreável e mais consistente.

Em uma frase:

`O objetivo desta base nao e apenas ajudar a construir agentes, mas ajudar a construir projetos agenticos com estrutura, validacao e continuidade.`

## Como a base evita invencao fora do escopo

A base foi ajustada para que a LLM nao dependa apenas de improviso na hora de implementar a primeira capacidade real.

A regra geral agora e:

- definir primeiro contratos minimos de dados
- usar `directives/`, `spec/`, `contracts/` e `kb/` para reduzir ambiguidade
- continuar automaticamente para a primeira capacidade incremental quando a base estiver aprovada
- quando houver fluxo executavel, executar, corrigir, revalidar e reportar
- perguntar ao humano apenas quando a ambiguidade for de alto risco
