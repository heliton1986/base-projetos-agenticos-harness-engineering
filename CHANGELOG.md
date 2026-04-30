# Changelog

Formato: [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/)
Versionamento: [Semantic Versioning](https://semver.org/lang/pt-BR/)

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

- Caminhos hardcoded `/var/home/heliton/...` em `prompts/PROMPT_MESTRE_INICIAL.md` e `prompts/PROMPTS_POR_FASE.md` → substituídos por `[HARNESS_BASE_PATH]`

---

## [1.1.0] - 2026-04-26

### Adicionado

- 16 documentos de base (01–16)
- 13 templates cobrindo todas as fases do projeto agentico
- 5 domínios KB em `.claude/kb/` (doe, builder-validator, execution-protocol, model-routing, agent-contracts)
- `AGENTS.md` — contrato de comportamento da LLM para esta base
- `prompts/` — PROMPT_MESTRE_INICIAL.md e PROMPTS_POR_FASE.md
- `README.md` da base

---

## Guia de versoes

| Tipo de mudanca | Incremento |
|----------------|-----------|
| Novo doc, template, exemplo, ferramenta | MINOR (1.x.0) |
| Correcao, ajuste, complemento em doc existente | PATCH (1.1.x) |
| Mudanca arquitetural que afeta contratos com projetos derivados | MAJOR (x.0.0) |
