# TEMPLATE_CI.md — CI + Coverage para Projetos Agenticos

## Quando usar

Antes de qualquer migração para framework (CrewAI, LangChain, etc). CI é a rede de segurança que garante que regras de negócio fixas não quebram durante refatoração.

## Arquivos a criar

### `.github/workflows/tests.yml`

```yaml
name: Tests

on:
  push:
    branches: ["**"]
  pull_request:
    branches: ["**"]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run tests with coverage
        run: pytest tests/ -v --tb=short --cov=src --cov-report=term --cov-fail-under=80
```

### `.coveragerc`

```ini
[run]
omit =
    src/db/*

[report]
omit =
    src/db/*
```

**Por que excluir `src/db/`:** módulos de conexão e models requerem DB real — não testáveis offline. Coverage deve refletir apenas código testável.

### `.gitignore` — adicionar

```
.coverage
htmlcov/
.pytest_cache/
```

### `requirements.txt` — adicionar

```
pytest>=8.0.0
pytest-cov>=5.0.0
```

## Regras

- Coverage mínimo: **80%** sobre `src/` excluindo `src/db/`
- Todo teste deve rodar offline: sem DB, sem LLM, sem API externa
- Para agentes que exigem API key no `__init__`: instanciar com `Agente.__new__(Agente)` nos testes
- Para agentes com dependências externas: usar `unittest.mock.patch`
- CI bloqueia merge automaticamente se coverage cair abaixo do mínimo

## Estrutura de testes esperada

```
tests/
  fixtures/           # CSVs e dados de teste
  test_ingestion.py   # IngestionAgent — fixture + CSV temporário (tmp_path)
  test_detector.py    # DetectorAgent — regras fixas via métodos internos, sem LLM
  test_validator.py   # ValidatorAgent — contratos válidos e inválidos
  test_reporter.py    # ReporterAgent — geração de relatório sem DB
  test_orchestrator.py # OrchestratorAgent — fluxo completo com mocks
```

## Gate de aprovação

```
pytest tests/ -v --tb=short --cov=src --cov-report=term --cov-fail-under=80
```

Resultado esperado: `X passed`, `Required test coverage of 80% reached`.

Ref: `templates/TEMPLATE_TESTS.md`
