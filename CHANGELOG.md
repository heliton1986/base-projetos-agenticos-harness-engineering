# Changelog

Formato: [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/)
Versionamento: [Semantic Versioning](https://semver.org/lang/pt-BR/)

---

## [1.17.1] - 2026-05-03

### Corrigido

- `15_FASES_DE_IMPLEMENTACAO_EXECUTAVEIS.md` — deixou explicito que arquivo em `implementation/` com apenas titulo + 1 frase nao cumpre o papel de fase executavel
- `templates/TEMPLATE_IMPLEMENTATION_PHASE.md` — adicionada regra de completude minima para runbooks de fase
- `AGENTS.md`, `README.md`, `prompts/base-generica/PROMPT_EXECUCAO_AUTONOMA_PROJETO.md`, `prompts/base-generica/PROMPTS_FASEADOS_BASE.md` e `prompts/projetos/financeops-v2/PROMPTS_FINANCEOPS_V2_POR_FASE.md` — placeholder curto em `implementation/` passa a ser tratado como artefato incompleto

### Adicionado

- `19_MAPEAMENTO_PROMPTS_VS_IMPLEMENTATION_FINANCEOPS.md` — leitura por niveis entre prompts da base, prompts de projeto e `implementation/*.md`

---

## [1.7.0] - 2026-04-30

### Adicionado

- `18_AUTONOMIA_AGENTICA_E_GUARDRAILS.md` — distinção guardrail vs constraint, feed forward vs feedback, pipeline com LLM vs agente real, anti-padrão do orquestrador como script sequencial
- `## Contrato acordado antes da execucao` em `06_PADRAO_BUILDER_VALIDATOR_E_TASK_CONTRACTS.md` — builder e validator concordam no contrato antes de executar; sequencia correta e por que previne loop infinito

### Origem

- VIDEO1_HARNESS.md — feed forward vs feedback (controle de sistemas)
- Semana AI Data Engineer 2026, Dia 3 — guardrail vs constraint; agente decide fluxo

---

## [1.3.0] - 2026-04-28

### Adicionado

- `templates/TEMPLATE_EXECUTION_RUNNER.md` — padrão de runner narrativo com saída em tempo real por fase e gate
- `## Protocolo narrativo no chat` em `AGENTS.md` — LLM anuncia cada fase/gate/agente antes e depois de tool calls

---

## [1.2.0] - 2026-04-28

### Adicionado

- `exemplos/canonical-minimal/` — projeto canônico completo (Issue Triage Agent) com README, AGENTS.md, directives, spec, contracts, src/agents, execution/run_onboarding_flow.py, model_routing.yaml
- `tools/validate_harness_project.py` — validador automático de conformidade Harness Engineering (11 checks, PASS/FAIL/WARN, exit code)
- `## Referencias` em docs 06, 10, 12, 14 — âncoras bibliográficas (Anthropic, OpenAI, ReAct, Chase) com nota de neutralidade de provedor
- `## Eixo interativo vs programatico` em `10_ESTRATEGIA_DE_MODELOS_PARA_AGENTES.md` e `AGENTS.md`
- `.env.example` no canonical-minimal

### Corrigido

- Caminhos hardcoded `/var/home/heliton/...` em `prompts/base-generica/PROMPT_DEFINICAO_PROJETO.md` e `prompts/base-generica/PROMPTS_FASEADOS_BASE.md` → substituídos por `[HARNESS_BASE_PATH]`

---

## [1.1.0] - 2026-04-26

### Adicionado

- 16 documentos de base (01–16)
- 13 templates cobrindo todas as fases do projeto agentico
- 5 domínios KB em `.claude/kb/` (doe, builder-validator, execution-protocol, model-routing, agent-contracts)
- `AGENTS.md` — contrato de comportamento da LLM para esta base
- `prompts/base-generica/` — PROMPT_DEFINICAO_PROJETO.md e PROMPTS_FASEADOS_BASE.md
- `README.md` da base

---

## Guia de versoes

| Tipo de mudanca | Incremento |
|----------------|-----------|
| Novo doc, template, exemplo, ferramenta | MINOR (1.x.0) |
| Correcao, ajuste, complemento em doc existente | PATCH (1.1.x) |
| Mudanca arquitetural que afeta contratos com projetos derivados | MAJOR (x.0.0) |
