# TEMPLATE_CHAINLIT.md — Interface Conversacional para Agentes

## Quando usar

Quando o projeto precisa de interface conversacional para usuario final — chat com agente, streaming token a token, transparencia de tool calls.

**Nao usar:** dashboards/relatorios/upload batch (usar Streamlit), endpoints HTTP para integracao (usar FastAPI).

**Diferenca de Streamlit:** Chainlit = voz do agente, interface conversacional com streaming e tool steps visiveis. Streamlit = dados, metricas, download de relatorios.

## Stack

```
chainlit>=2.0.0    # framework de chat UI — sem React, sem frontend separado
```

## Estrutura de arquivos

```
src/
  tools.py          # @tool functions (ver TEMPLATE_LANGGRAPH.md)
  agent.py          # create_react_agent com streaming=True
  chainlit_app.py   # interface — 3 hooks, ~40 linhas
chainlit.md         # mensagem de boas-vindas (markdown)
.chainlit/
  config.toml       # configuracao do servidor
```

## `src/chainlit_app.py` — padrao base

```python
import chainlit as cl
from src.agent import create_agent

WELCOME_MESSAGE = """**[NomeAgente] conectado!**

[Descrever as fontes de dados disponiveis e exemplos de perguntas]

Exemplos:
- "[exemplo de pergunta estruturada]"
- "[exemplo de pergunta semantica]"
- "[exemplo de pergunta hibrida]"
"""

TOOL_DISPLAY_NAMES = {
    "execute_sql": "[Nome legivel da tool SQL]",
    "semantic_search": "[Nome legivel da tool semantica]",
}


@cl.on_chat_start
async def start():
    agent = create_agent(streaming=True)
    cl.user_session.set("agent", agent)
    await cl.Message(content=WELCOME_MESSAGE).send()


@cl.on_message
async def main(message: cl.Message):
    agent = cl.user_session.get("agent")
    msg = cl.Message(content="")
    tool_steps: dict[str, cl.Step] = {}

    async for event in agent.astream_events(
        {"messages": [{"role": "user", "content": message.content}]},
        version="v2",
    ):
        kind = event["event"]

        if kind == "on_chat_model_stream":
            chunk = event["data"]["chunk"]
            if hasattr(chunk, "content") and isinstance(chunk.content, str) and chunk.content:
                await msg.stream_token(chunk.content)

        elif kind == "on_tool_start":
            tool_name = event["name"]
            display_name = TOOL_DISPLAY_NAMES.get(tool_name, tool_name)
            step = cl.Step(name=display_name, type="tool")
            await step.__aenter__()
            step.input = str(event["data"].get("input", ""))
            tool_steps[event["run_id"]] = step

        elif kind == "on_tool_end":
            step = tool_steps.pop(event["run_id"], None)
            if step:
                output = str(event["data"].get("output", ""))
                step.output = output[:1000]
                await step.__aexit__(None, None, None)

    await msg.send()
```

## Lifecycle hooks

| Hook | Quando dispara | Uso |
|---|---|---|
| `@cl.on_chat_start` | Nova sessao de chat | Criar agente, setar user_session, enviar boas-vindas |
| `@cl.on_message` | Mensagem do usuario | Invocar agente com streaming |
| `@cl.on_stop` | Usuario interrompe | Cancelar streams pendentes |

## Conceitos-chave

### Streaming (`astream_events version="v2"`)

Eventos relevantes:

| Evento | O que e |
|---|---|
| `on_chat_model_stream` | Token LLM — chamar `msg.stream_token(token)` |
| `on_tool_start` | Agente comecou a chamar tool — abrir `cl.Step` |
| `on_tool_end` | Tool terminou — fechar `cl.Step` com output |

### Tool Steps (transparencia)

```python
step = cl.Step(name="Nome Visivel", type="tool")
await step.__aenter__()
step.input = str(input_data)
# ... tool executa ...
step.output = resultado[:1000]  # limitar output longo
await step.__aexit__(None, None, None)
```

Usuario ve cada tool call expandivel no chat — "o agente pensou assim antes de responder".

### Session isolation

```python
cl.user_session.set("agent", agent)   # salvar na sessao
agent = cl.user_session.get("agent")  # recuperar na sessao
```

Cada usuario tem agente isolado — sem estado compartilhado entre sessoes.

## Rodar

```bash
chainlit run src/chainlit_app.py -w   # -w = hot-reload
```

UI disponivel em `http://localhost:8000`.

## `requirements.txt` — adicionar

```
chainlit>=2.0.0
```

## `.coveragerc` — excluir chainlit_app.py

```ini
[run]
omit =
    src/db/*
    src/chainlit_app.py
```

**Por que excluir:** `chainlit_app.py` e entrypoint Chainlit — requer runtime do servidor, nao testavel com pytest. Toda logica de negocio fica em `tools.py` e `agent.py` (testados offline).

## Regras

- `chainlit_app.py` = apenas hooks Chainlit + chamada ao agente. Sem logica de negocio.
- Sempre usar `astream_events(version="v2")` — versao v1 descontinuada
- `cl.Step` por tool call — usuario deve ver o que o agente fez, nao so a resposta final
- `cl.user_session` para isolamento entre usuarios — nunca variaveis globais mutaveis
- Output de tool truncado em 1000 chars no step — output completo vai pro agente, nao para o display
- `agent = create_agent(streaming=True)` — criar com streaming habilitado no `on_chat_start`
