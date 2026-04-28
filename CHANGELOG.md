# Changelog

Formato: [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/)
Versionamento: [Semantic Versioning](https://semver.org/lang/pt-BR/)

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
