# TEMPLATE_LANGGRAPH.md — Agente ReAct com LangGraph + Anthropic

## Quando usar

Quando o projeto precisa de um agente com decisao autonoma de ferramentas — ele recebe uma pergunta e decide qual tool chamar, em qual ordem, e se precisa combinar resultados.

**Nao usar:** fluxos deterministicos (usar pipeline Python puro), multiplos agentes com papeis distintos (usar CrewAI), interface sem chat (usar Streamlit).

**Diferenca de Streamlit:** Chainlit = interface conversacional com agente. Streamlit = dashboards/dados/relatorios. Escolher pelo tipo de interacao do usuario.

## Stack

```
langchain-anthropic>=0.3.0   # ChatAnthropic com tool binding nativo
langchain-core>=0.3.0        # BaseTool, @tool decorator, Runnables
langgraph>=0.2.0             # create_react_agent — loop ReAct autonomo
```

## Estrutura de arquivos

```
src/
  tools.py          # @tool functions — poderes do agente
  agent.py          # create_react_agent — cerebro do agente
  chainlit_app.py   # interface conversacional (ver TEMPLATE_CHAINLIT.md)
```

Tres arquivos, responsabilidade unica cada um. Tools nao conhecem o agente. Agente nao conhece Chainlit.

## `src/tools.py` — padrao base

```python
from langchain_core.tools import tool

@tool
def execute_sql(query: str) -> str:
    """Use para perguntas sobre numeros, totais, faturamento, pedidos e ticket medio.
    Exemplos: 'qual o faturamento do mes?', 'quantos pedidos foram feitos?'
    Escreva queries SELECT validas para o schema do banco."""
    # implementacao...
    return resultado

@tool
def semantic_search(question: str) -> str:
    """Use para perguntas sobre opiniao, sentimento, reclamacoes e contexto qualitativo.
    Exemplos: 'o que os clientes reclamam?', 'qual o sentimento sobre o produto X?'"""
    # implementacao...
    return resultado
```

### Regra critica: docstring e a spec do agente

O agente le a docstring de cada tool para decidir QUANDO usa-la. Docstring ruim → decisao ruim.

```python
# Ruim — descreve implementacao, nao criterio de uso
@tool
def execute_sql(query: str) -> str:
    """Executa query SQL no banco de dados."""

# Correto — responde: "em que situacao o agente deve escolher esta tool?"
@tool
def execute_sql(query: str) -> str:
    """Use para perguntas sobre numeros, totais, faturamento, pedidos e ticket medio."""
```

Escreva a docstring respondendo: "Em que situacao o agente deve escolher esta tool?"

## `src/agent.py` — padrao base

```python
from langchain_anthropic import ChatAnthropic
from langgraph.prebuilt import create_react_agent
from src.tools import execute_sql, semantic_search

SYSTEM_PROMPT = """Voce e o [NomeAgente]. Voce tem acesso a ferramentas e deve decidir qual usar.

## [Fonte A] — Dados Exatos
Use execute_sql para perguntas sobre numeros, totais e dados estruturados.

## [Fonte B] — Significado
Use semantic_search para perguntas sobre opinioes e sentimentos.

## Regras de Roteamento
1. Numeros, totais, contagens → execute_sql
2. Opinioes, sentimentos, temas → semantic_search
3. Perguntas hibridas → use AMBAS as ferramentas
4. Sempre responda em Portugues
"""

TOOLS = [execute_sql, semantic_search]


def create_agent(*, streaming: bool = False):
    llm = ChatAnthropic(
        model="claude-sonnet-4-6",
        temperature=0,
        streaming=streaming,
    )
    return create_react_agent(
        model=llm,
        tools=TOOLS,
        prompt=SYSTEM_PROMPT,
    )
```

### Dual-store routing — padrao D3

Quando o agente precisa decidir entre fonte estruturada (SQL) e fonte semantica (vetorial):

1. Duas tools com docstrings claras sobre quando usar cada uma
2. System prompt com regras de roteamento explicitas
3. Agente decide por intencao da pergunta, nao por logica hardcoded
4. Perguntas hibridas → agente chama as duas e combina

```
Pergunta: "faturamento dos clientes que reclamam de entrega"
→ agente chama semantic_search("reclamacoes entrega") → extrai IDs
→ agente chama execute_sql("SELECT ... WHERE customer_id IN (...)") → faturamento
→ combina e responde
```

### Arvore de decisao formal

```
Pergunta do Usuario
  → Classificacao em Linguagem Natural
    → Dados Exatos?  → execute_sql     (SELECT/AVG/COUNT — Postgres/SQL)
    → Hibrido?       → ambas as tools  (Semantica + SQL na mesma query)
    → Significado?   → semantic_search (Embeddings/similarity — Qdrant/vetores)
```

"O routing e o coracao da inteligencia do agente. Classificacao em linguagem natural decide o caminho antes de qualquer execucao."

A inteligencia do sistema esta na qualidade do routing, nao na complexidade das tools.

Fonte: Semana AI Data Engineer 2026, Dia 3 — slide "Como o Agente Decide"

## `requirements.txt` — adicionar

```
langchain-anthropic>=0.3.0
langchain-core>=0.3.0
langgraph>=0.2.0
python-dotenv>=1.0.0
```

Se usar Postgres:
```
psycopg2-binary>=2.9.0
```

Se usar Qdrant + LlamaIndex:
```
llama-index-core>=0.12.0
llama-index-vector-stores-qdrant>=0.4.0
llama-index-embeddings-fastembed>=0.3.0
fastembed>=0.4.0
llama-index-llms-anthropic>=0.6.0
qdrant-client>=1.12.0
```

## Testes offline — padrao

Testar tools sem chamar servicos externos. Mockar conexoes.

```python
from unittest.mock import patch, MagicMock
from src.tools import execute_sql

def test_execute_sql_retorna_colunas():
    mock_cursor = MagicMock()
    mock_cursor.description = [("estado",), ("total",)]
    mock_cursor.fetchall.return_value = [("SP", 10000), ("RJ", 5000)]
    mock_conn = MagicMock()
    mock_conn.cursor.return_value.__enter__ = lambda s: mock_cursor
    mock_conn.cursor.return_value.__exit__ = MagicMock(return_value=False)

    with patch("src.tools._get_postgres_connection", return_value=mock_conn):
        result = execute_sql.invoke({"query": "SELECT estado, total FROM orders"})
    assert "estado" in result
    assert "SP" in result
```

## Regras

- `tools.py` — sem conhecimento do agente ou da UI
- `agent.py` — sem conhecimento da UI; exporta apenas `create_agent()`
- `create_react_agent` gerencia o loop ReAct — nao implementar loop manualmente
- `temperature=0` para consistencia de roteamento
- Docstring de cada tool responde "quando usar", nao "o que faz"
- Dual-store: nunca hardcodar qual store usar — deixar o agente decidir por intencao
