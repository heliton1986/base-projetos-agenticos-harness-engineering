# Template: Testes Automatizados

## Objetivo

Todo projeto derivado deve ter testes que rodam offline — sem DB, sem LLM, sem API externa.
Cobertura minima: regras fixas de cada agente + contratos Pydantic.

## Estrutura obrigatoria

```
tests/
├── __init__.py
├── fixtures/
│   └── [nome]_fixture.csv       # dados de entrada para testes de ingestao
├── test_ingestion.py            # testa IngestionAgent
├── test_detector.py             # testa regras fixas do DetectorAgent (sem LLM)
└── test_validator.py            # testa ValidatorAgent com contratos validos e invalidos
```

## Regras

1. **Sem LLM nos testes** — DetectorAgent tem regras fixas (duplicata, valor, descricao) e analise LLM. Testar apenas as regras fixas via metodos internos (`_detectar_duplicatas`, etc.). Analise LLM nao e testavel em unit test.
2. **Sem DB nos testes** — IngestionAgent e DetectorAgent nao dependem de DB. Usar `tmp_path` do pytest para CSV temporario.
3. **Fixture CSV realista** — incluir pelo menos: 1 duplicata, 1 lancamento com campo ausente, 1 valor suspeito, 1 descricao suspeita.
4. **Testar rejeicoes com CSV misto** — CSV com 1 linha valida + 1 invalida. Nao usar CSV so com linhas invalidas (levanta RuntimeError antes de checar inconsistencias_ingestao).

## Padroes por suite

### test_ingestion.py

```python
FIXTURE = str(Path(__file__).parent / "fixtures" / "[nome]_fixture.csv")
LINHA_VALIDA = "2026-01-01,Descricao valida,100.00,Categoria,CentroCusto,csv"

def test_ingestao_fixture_basica():
    resultado = IngestionAgent().processar(FIXTURE)
    assert resultado.total_lancamentos > 0

def test_ingestao_rejeita_campo_ausente(tmp_path):
    csv = tmp_path / "t.csv"
    csv.write_text(f"header\n{LINHA_VALIDA}\nlinha_com_campo_ausente\n")
    resultado = IngestionAgent().processar(str(csv))
    assert len(resultado.inconsistencias_ingestao) == 1
    assert "campo" in resultado.inconsistencias_ingestao[0].motivo

def test_ingestao_arquivo_inexistente():
    with pytest.raises(FileNotFoundError):
        IngestionAgent().processar("/nao/existe.csv")
```

### test_detector.py

```python
# Instanciar sem __init__ para nao precisar de ANTHROPIC_API_KEY
agent = DetectorAgent.__new__(DetectorAgent)

def test_detecta_duplicata():
    resultado = agent._detectar_duplicatas([l1, l2_identico])
    assert len(resultado) == 2
    assert resultado[0].tipo == "duplicata_suspeita"

def test_detecta_valor_alto():
    resultado = agent._detectar_valores_suspeitos([lancamento_alto])
    assert resultado[0].tipo == "valor_alto_suspeito"

def test_mascaramento_valor():
    from src.agents.detector_agent import _mascarar_valor
    assert _mascarar_valor(Decimal("500")) == "< 1k"
```

### test_validator.py

```python
def test_valida_contrato_valido():
    instancia = [instancia Pydantic valida]
    vr = ValidatorAgent().validar_instancia(instancia)
    assert vr.valido is True

def test_valida_dict_invalido():
    vr = ValidatorAgent().validar_lancamentos({})
    assert vr.valido is False
    assert len(vr.erros) > 0
```

## Rodar

```bash
pytest tests/ -v          # todos os testes
pytest tests/ -v --tb=short  # output resumido em falha
```

Deve passar em < 5s offline. Se demorar mais: algum teste esta fazendo chamada externa.

## Quando adicionar testes

- Ao implementar qualquer agente novo: adicionar suite correspondente
- Ao corrigir bug em regra fixa: adicionar teste que reproduz o bug antes de corrigir
- Antes de evoluir para CrewAI/framework: garantir 100% das regras fixas cobertas
