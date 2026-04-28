# Issue Triage Agent

## Visao Geral

Recebe texto de issue (bug report, feature request, duvida), classifica severidade e categoria, e gera relatorio estruturado. Construido com `Harness Engineering`: OrchestratorAgent + ClassifierAgent + ReporterAgent + validacao independente.

## Objetivo

Automatizar triagem inicial de issues para reduzir tempo de roteamento manual. Entrada: texto livre. Saida: classificacao validada + relatorio.

## Usuario ou Operacao Alvo

- Equipes de engenharia com volume alto de issues
- Operacoes de suporte que precisam priorizar filas

## Arquitetura Resumida

```
Texto da issue (entrada)
        |
        v
[OrchestratorAgent]
        |
        +---> [ClassifierAgent]   (classifica severidade e categoria via LLM)
        |
        +---> [ValidatorAgent]    (valida contrato de saida do ClassifierAgent)
        |
        +---> [ReporterAgent]     (gera relatorio estruturado)
        |
        v
[Saida: IssueReport]
```

**Regra central:** ClassifierAgent nunca escreve direto no banco — apenas retorna classificacao para o Orchestrator.

## Stack

| Camada | Tecnologia |
|--------|-----------|
| LLM | Claude claude-sonnet-4-6 (via API Anthropic) |
| Agentes | Python puro (sem framework) |
| Validacao | Pydantic + pytest |
| Persistencia | Arquivo JSON (simplicidade canonica) |

## Modelo Operacional DOE

- **Diretivas** (`directives/`): categorias validas, severidades, regras de classificacao
- **Orquestracao** (`src/agents/orchestrator.py`): coordena fluxo, nao classifica
- **Execucao** (`src/agents/`): ClassifierAgent e ReporterAgent com responsabilidades isoladas

Ref: `[HARNESS_BASE_PATH]/02_DOE_OPERACIONAL_PARA_HARNESS.md`

## Padrao Builder / Validator / Loop de Correcao

```
ClassifierAgent  → constroi IssueClassification
ValidatorAgent   → valida contra IssueClassificationContract
Loop             → se falhar: retentar com contexto de erro
Gate             → aprovado quando severidade + categoria validas
```

Contratos: `contracts/issue_contract.md`. Gates: `spec/03-design.md`.

## Estrategia de Modelos por Agente

| Agente | Modelo | Justificativa |
|--------|--------|--------------|
| ClassifierAgent | claude-sonnet-4-6 | Raciocinio sobre texto ambiguo |
| OrchestratorAgent | Sem LLM | Logica deterministica de fluxo |
| ValidatorAgent | Sem LLM | Validacao de schema (Pydantic) |
| ReporterAgent | Sem LLM | Formatacao deterministica |

Ref: `[HARNESS_BASE_PATH]/10_ESTRATEGIA_DE_MODELOS_PARA_AGENTES.md`

## Como rodar

```bash
# Instalar dependencias
pip install anthropic pydantic pytest

# Configurar API key
export ANTHROPIC_API_KEY=sk-...

# Rodar onboarding (verifica ambiente)
python execution/run_onboarding_flow.py

# Rodar classificacao de exemplo
python src/agents/orchestrator.py
```

## Estrutura de arquivos

```
canonical-minimal/
├── README.md                    # este arquivo
├── AGENTS.md                    # contrato de comportamento da LLM
├── directives/
│   └── triagem_rules.md         # categorias, severidades, regras
├── spec/
│   ├── 01-brainstorm.md         # exploracao inicial
│   ├── 02-define.md             # escopo definido
│   └── 03-design.md             # arquitetura + gates
├── contracts/
│   └── issue_contract.md        # contrato de entrada/saida
├── src/agents/
│   ├── orchestrator.py          # coordenador de fluxo
│   ├── classifier_agent.py      # classifica via LLM
│   └── reporter_agent.py        # gera relatorio
├── execution/
│   └── run_onboarding_flow.py   # smoke tests do ambiente
└── model_routing.yaml           # estrategia de modelos por agente
```
