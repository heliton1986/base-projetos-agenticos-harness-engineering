# TEMPLATE_STREAMLIT.md — UI Web para Projetos Agenticos

## Quando usar

Quando o projeto precisa de interface visual para usuário não-técnico: upload de arquivos, visualização de resultados, download de relatórios.

**Não usar:** projetos puramente API/batch, quando usuário é técnico e usa CLI, quando já existe FastAPI com frontend separado.

## Estrutura

```
src/ui/
  __init__.py
  app.py           # Streamlit app (entrypoint, excluir do coverage)
  formatters.py    # helpers de display testados offline
execution/
  run_ui.py        # streamlit run entrypoint
tests/
  test_ui_formatters.py  # testes offline para formatters
```

## `src/ui/formatters.py` — padrão base

Extrair toda lógica de formatação/transformação para `formatters.py`. Manter `app.py` com apenas código Streamlit.

```python
from decimal import Decimal
from contracts.relatorio_contract import RelatorioExecutivo

SEVERIDADE_COR = {
    "critica": "🔴", "alta": "🟠", "media": "🟡", "baixa": "🟢",
}

STATUS_LABEL = {
    "pronto": "✅ Pronto para fechamento",
    "requer_revisao": "⚠️ Requer revisão",
    "bloqueado": "🚫 Bloqueado",
}

def formatar_status(status: str) -> str:
    return STATUS_LABEL.get(status, status)

def formatar_valor(valor: Decimal) -> str:
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def relatorio_para_json(relatorio: RelatorioExecutivo) -> str:
    return relatorio.model_dump_json(indent=2)
```

## `src/ui/app.py` — estrutura padrão

```python
import sys, os, tempfile
from pathlib import Path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import pandas as pd
from src.agents.orchestrator import OrchestratorAgent
from src.ui.formatters import formatar_status, formatar_valor, relatorio_para_json

st.set_page_config(page_title="[Projeto] Agent", layout="wide")
st.title("[Projeto] Agent")

uploaded = st.file_uploader("Selecione o arquivo CSV", type=["csv"])

if uploaded is not None:
    with st.spinner("Processando..."):
        conteudo = uploaded.read()
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
            tmp.write(conteudo)
            tmp_path = tmp.name
        try:
            relatorio = OrchestratorAgent().executar(tmp_path)
        except RuntimeError as e:
            st.error(f"Erro: {e}")
            st.stop()
        finally:
            Path(tmp_path).unlink(missing_ok=True)

    st.success(formatar_status(relatorio.status_sistema))
    # métricas, tabelas, download...
    st.download_button("⬇️ Baixar JSON", relatorio_para_json(relatorio),
                       file_name=f"relatorio_{relatorio.run_id}.json", mime="application/json")
```

## `execution/run_ui.py`

```python
import sys, os, subprocess
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if __name__ == "__main__":
    ui_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src", "ui", "app.py")
    subprocess.run(["streamlit", "run", ui_path], check=True)
```

## `requirements.txt` — adicionar

```
streamlit>=1.35.0
pandas>=2.0.0
```

## Testes offline — padrão

Testar `formatters.py` — nunca importar `streamlit` nos testes.

```python
def test_formatar_status_pronto():
    assert "Pronto" in formatar_status("pronto")

def test_formatar_valor():
    resultado = formatar_valor(Decimal("5000.50"))
    assert "5.000,50" in resultado

def test_relatorio_para_json():
    json_str = relatorio_para_json(relatorio_mock)
    assert "run_id" in json_str
```

## `.coveragerc` — excluir app.py

```ini
[run]
omit =
    src/db/*
    src/ui/app.py
```

**Por que excluir:** `app.py` é entrypoint Streamlit — requer runtime Streamlit, não testável com pytest. Toda lógica de negócio fica em `formatters.py` (testado 100%).

## Regras

- `app.py` = apenas código Streamlit (st.*) + chamada ao OrchestratorAgent
- `formatters.py` = toda lógica de display/transformação — deve ter 100% coverage
- Nunca importar `streamlit` em `formatters.py`
- Arquivo temporário sempre deletado no `finally`
- `st.stop()` para interromper fluxo em erro
