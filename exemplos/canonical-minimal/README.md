# Issue Triage Agent

## Visao Geral

Recebe texto de issue (bug report, feature request, duvida), classifica severidade e categoria, e gera relatorio estruturado. Construido com `Harness Engineering`: OrchestratorAgent + ClassifierAgent + ValidatorAgent + ReporterAgent.

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
        +---> [ValidatorAgent]    (valida contratos Pydantic entre etapas)
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
| Validacao | Pydantic + pytest + coverage |
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

Contratos documentais: `contracts/issue_contract.md`. Contratos executaveis: `src/contracts/issue_contract.py`. Gates: `spec/03-design.md`.

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
pip install -r requirements.txt

# Configurar API key
export ANTHROPIC_API_KEY=sk-...

# Rodar onboarding (verifica ambiente)
python execution/run_onboarding_flow.py

# Rodar testes offline
pytest tests/ -v --tb=short

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
│   └── issue_contract.md        # contrato documental de entrada/saida
├── implementation/
│   └── 01-bootstrap-issue-triage.md  # runbook minimo da fase atual
├── progress/
│   ├── PROGRESS.md              # memoria operacional
│   └── VALIDATION_STATUS.md     # ultimo estado de validacao
├── tests/
│   ├── test_classifier.py       # parser e classificacao com fake client
│   ├── test_orchestrator.py     # retries e gates deterministas
│   ├── test_reporter.py         # geracao de relatorio
│   └── test_validator.py        # contratos validos e invalidos
├── src/agents/
│   ├── orchestrator.py          # coordenador de fluxo
│   ├── classifier_agent.py      # classifica via LLM
│   ├── validator_agent.py       # valida contratos Pydantic
│   └── reporter_agent.py        # gera relatorio
├── src/contracts/
│   └── issue_contract.py        # contratos executaveis em runtime
├── execution/
│   └── run_onboarding_flow.py   # smoke tests do ambiente
├── .github/workflows/tests.yml  # CI offline com coverage
├── .coveragerc                  # coverage minima sobre src/
├── requirements.txt             # dependencias do exemplo
└── model_routing.yaml           # estrategia de modelos por agente
```

## Observacoes de alinhamento com a base

- Este exemplo agora segue a regra de `implementation/` obrigatorio em projetos multi-agent.
- Os contratos foram separados em dois papeis: `.md` documental e `.py` executavel.
- Os testes rodam offline: sem API real, sem LLM real, sem servicos externos.
- CI e coverage estao preparados antes de qualquer futura migracao para framework.
