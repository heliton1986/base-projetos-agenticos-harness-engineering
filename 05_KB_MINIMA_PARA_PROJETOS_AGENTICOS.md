# KB Minima para Projetos Agenticos

## Objetivo

Define quando e como usar `kb/` em projetos agenticos com Harness Engineering.

## Modelo: kb-first → context7 fallback

Leitura de arquivo local e mais rapida e barata que chamada MCP. Padrao:

1. Consultar `kb/[ferramenta]/quick-reference.md` primeiro
2. Se kb/ nao cobre ou pode estar desatualizada → context7 MCP on demand
3. Se context7 retornar padrao diferente do kb/ → atualizar kb/

## O que kb/ guarda

**Padroes validados e especificos do projeto** — como *este* projeto usa cada ferramenta.

Nao e copia de documentacao generica. E o padrao que ja foi testado, esta em uso, e vale registrar para novas sessoes.

## Estrutura por ferramenta

```text
kb/
  [ferramenta]/
    index.md           — contexto: tabelas, arquivos relevantes, regras do projeto
    quick-reference.md — snippets prontos para copiar e usar agora
```

Usar `TEMPLATE_KB.md` para gerar cada dominio. Nunca gerar do zero.

## Quando criar kb/ de uma ferramenta

Criar quando o projeto usa a ferramenta de forma recorrente e ha padroes especificos que valem registrar. Exemplos:

- ORM com schema proprio → kb/supabase/ ou kb/sqlalchemy/
- Contratos Pydantic recorrentes → kb/pydantic/
- SDK LLM com configuracoes fixas → kb/anthropic/ ou kb/openai/
- Framework de agentes → kb/crewai/, kb/langchain/
- Observabilidade → kb/langfuse/
- Interface de chat → kb/chainlit/

## Quando NAO criar

- Ferramenta usada uma vez de forma generica → consultar context7 diretamente
- Padrao ja coberto por `directives/` → nao duplicar
- Biblioteca utilitaria simples (ex: `python-dotenv`) → nao precisa de kb/

## Relacao com directives/

- `directives/` guarda **regras de negocio e dominio** — o que o sistema deve fazer
- `kb/` guarda **padroes de ferramentas** — como o sistema implementa usando cada ferramenta

Nao substituem um ao outro. Nao duplicar conteudo entre eles.

## Freshness

kb/ estatica pode ficar desatualizada. Verificar com context7 quando:
- biblioteca lancar versao major
- padrao do projeto mudar
- context7 retornar API diferente do que esta no quick-reference.md

## Conclusao

`kb/` reduz custo por sessao (leitura local vs MCP call) e garante que padroes validados do projeto estao acessiveis sem reler todo o codigo. Opcional para ferramentas simples, recomendada para frameworks complexos usados repetidamente.
