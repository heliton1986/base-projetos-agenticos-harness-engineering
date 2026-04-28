# Template: KB Minima do Projeto

## Objetivo

Contexto denso para novas sessoes. Evita reler `directives/` completo e preencher lacunas com suposicoes.
Criar antes de implementar qualquer agente. Atualizar ao fim de cada fase.

## Estrutura obrigatoria

```
kb/
├── index.md    — estado atual, proximos passos, fontes de verdade
├── domain.md   — agentes, modelos, stack, escopo, fluxo de execucao
└── rules.md    — regras de negocio + contratos por agente
```

## kb/index.md

```markdown
# KB — [Nome do Projeto]

Contexto denso para novas sessoes. Ler antes de qualquer acao no projeto.

## Quando ler cada arquivo

| Arquivo | Ler quando |
|---------|-----------|
| `domain.md` | Inicio de sessao — contexto do sistema, agentes, stack, escopo |
| `rules.md` | Antes de implementar/modificar qualquer agente ou regra de negocio |

## Estado do projeto

- **Versao:** [versao atual]
- **Data:** [YYYY-MM-DD]
- **Gates:** [status dos gates]
- **Testes:** [N/N passando]

## Proximos passos

1. [proximo passo prioritario]
2. [segundo passo]

## Fontes de verdade

- Regras de negocio: `directives/business-rules.md`
- Contratos de saida: `directives/output-contracts.md`
- Roteamento de modelos: `model_routing.yaml`
- Estado atual: `progress/PROGRESS.md`
```

## kb/domain.md

```markdown
# Dominio — [Nome do Projeto]

## O que o sistema faz

[descricao concisa em 2-3 linhas]

## O que NAO faz (v[N])

- [limitacao 1]
- [limitacao 2]

## Agentes e modelos

| Agente | LLM | Modelo | Papel |
|--------|-----|--------|-------|
| OrchestratorAgent | nao | — | Coordena fluxo, sem logica de negocio |
| [AgenteX] | [sim/nao] | [modelo ou —] | [papel] |

## Stack

- [linguagem, frameworks, versoes]
- [banco de dados]
- [providers externos]

## Arquitetura de sessao DB

[como a sessao e gerenciada — runner abre, passa para fases, nunca delega ao orquestrador]

## Mascaramento (se aplicavel)

[regras de mascaramento antes de enviar ao LLM]

## Fluxo de execucao

```
Fase 1 — [Nome]   → Gate: [criterios]
Fase 2 — [Nome]   → [Agente] → ValidatorAgent gate → audit_log
...
```
```

## kb/rules.md

```markdown
# Regras e Contratos — [Nome do Projeto]

## Regras de [dominio 1]

| Regra | Descricao | Tipo inconsistencia |
|-------|-----------|-------------------|
| R01 | [regra] | `[tipo]` |

## Regras de [dominio 2]

| Regra | Descricao | Tipo | Severidade |
|-------|-----------|------|-----------|
| R0N | [regra] | `[tipo]` | [critica/alta/media/baixa] |

## Contratos por agente

### [AgenteX] → [ContratoSaida]
```
campo1: tipo
campo2: tipo
...
```

## Regras de contrato

- [regra 1]
- [regra 2]
```

## Regras de manutencao

- Atualizar `kb/index.md` ao fim de cada fase (estado, proximos passos)
- Atualizar `kb/rules.md` ao adicionar ou modificar regra de negocio ou contrato
- Atualizar `kb/domain.md` ao adicionar agente ou mudar arquitetura
- KB e resumo denso — nao duplicar conteudo de `directives/`. Se conflito: `directives/` prevalece

## Quando criar

Antes de implementar qualquer agente — idealmente logo apos gerar `model_routing.yaml`.

## Referencia

`05_KB_MINIMA_PARA_PROJETOS_AGENTICOS.md` — contexto completo sobre quando e como usar kb/ em projetos agenticos.
