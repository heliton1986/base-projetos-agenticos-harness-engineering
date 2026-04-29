# TEMPLATE_FASTAPI.md — API REST para Projetos Agenticos

## Quando usar

Quando o projeto precisa expor processamento via HTTP: upload de arquivos, integração com outros sistemas, consumo por frontend externo.

**Não usar:** projetos puramente internos, scripts batch, automações sem interface HTTP.

## Estrutura

```
src/api/
  __init__.py
  main.py          # FastAPI app + endpoints
execution/
  run_api.py       # uvicorn entrypoint
tests/
  test_api.py      # TestClient + mock dos agentes
```

## `src/api/main.py` — padrão base

```python
import tempfile
from pathlib import Path

from fastapi import FastAPI, HTTPException, UploadFile, File

from contracts.relatorio_contract import RelatorioExecutivo
from src.agents.orchestrator import OrchestratorAgent

app = FastAPI(title="[Projeto] Agent API", version="1.0.0")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/processar", response_model=RelatorioExecutivo)
async def processar(file: UploadFile = File(...)):
    if not file.filename or not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Arquivo deve ser CSV (.csv)")

    conteudo = await file.read()
    if not conteudo:
        raise HTTPException(status_code=400, detail="Arquivo CSV vazio")

    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
        tmp.write(conteudo)
        tmp_path = tmp.name

    try:
        agente = OrchestratorAgent()
        relatorio = agente.executar(tmp_path)
        return relatorio
    except RuntimeError as e:
        raise HTTPException(status_code=422, detail=str(e))
    finally:
        Path(tmp_path).unlink(missing_ok=True)
```

## `execution/run_api.py`

```python
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dotenv import load_dotenv
load_dotenv()
import uvicorn

if __name__ == "__main__":
    uvicorn.run("src.api.main:app", host="0.0.0.0", port=8000, reload=True)
```

## `requirements.txt` — adicionar

```
fastapi>=0.111.0
uvicorn[standard]>=0.30.0
python-multipart>=0.0.9
httpx>=0.27.0
```

## Testes offline — padrão

```python
import os
from unittest.mock import patch
import pytest
from fastapi.testclient import TestClient

@pytest.fixture
def client():
    with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"}):
        from src.api.main import app
        return TestClient(app)

def test_health(client):
    assert client.get("/health").status_code == 200

def test_processar_csv_valido(client):
    with patch("src.api.main.OrchestratorAgent") as mock:
        mock.return_value.executar.return_value = _relatorio_mock()
        response = client.post(
            "/processar",
            files={"file": ("lancamentos.csv", CSV_VALIDO, "text/csv")},
        )
    assert response.status_code == 200

def test_rejeita_nao_csv(client):
    response = client.post(
        "/processar",
        files={"file": ("dados.xlsx", b"x", "application/octet-stream")},
    )
    assert response.status_code == 400

def test_erro_runtime_vira_422(client):
    with patch("src.api.main.OrchestratorAgent") as mock:
        mock.return_value.executar.side_effect = RuntimeError("CSV invalido")
        response = client.post(
            "/processar",
            files={"file": ("x.csv", b"data", "text/csv")},
        )
    assert response.status_code == 422
```

## Regras

- `GET /health` obrigatório — usado por CI e monitoramento
- Erros de negócio (`RuntimeError` dos agentes) → HTTP 422
- Erros de validação de input → HTTP 400
- Arquivo temporário sempre deletado no `finally`
- `OrchestratorAgent` mockado nos testes — nunca chamar LLM/DB em teste

## `.coveragerc` — não precisa excluir

`src/api/main.py` é testável com `TestClient` — não excluir do coverage.
