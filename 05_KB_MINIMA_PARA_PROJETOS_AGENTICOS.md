# KB Minima para Projetos Agenticos

## Objetivo

Define quando e como usar uma camada `kb/` em projetos agenticos com Harness Engineering.

## Dois usos distintos de kb/

### 1. kb/ como biblioteca de ferramentas

Guarda referencia de uso de frameworks e ferramentas externas usadas no projeto.

Exemplos: `kb/crewai/`, `kb/langfuse/`, `kb/chainlit/`, `kb/pydantic/`

Cada dominio tem `index.md` (contexto) e `quick-reference.md` (padrao pronto para usar).

**Quando faz sentido:** projeto que adota frameworks complexos (CrewAI, LangChain, LangFuse). A LLM consulta a kb/ para aplicar padroes do framework sem buscar docs externos a cada sessao.

**Alternativa:** MCP context7 (`mcp__context7__*`) busca documentacao atualizada de qualquer biblioteca on demand — dispensa kb/ estatica de ferramentas quando context7 esta disponivel.

### 2. kb/ como contexto de projeto

Guarda resumo denso do estado, dominio e regras do projeto especifico.

Exemplos: `kb/index.md`, `kb/domain.md`, `kb/rules.md`

**Quando faz sentido:** projeto com `directives/` grande demais para reler inteiro a cada sessao, ou com muitas regras de negocio e contratos que mudam com frequencia.

**Quando nao precisa:** projeto com `directives/` pequeno e bem estruturado. Nesse caso, a LLM le `directives/` diretamente e kb/ seria redundante.

## Regra pratica para projetos Harness

| Situacao | kb/ necessaria? |
|----------|----------------|
| `directives/` pequeno (< 3 arquivos simples) | nao — ler directives/ diretamente |
| `directives/` grande ou regras complexas | sim — kb/ de contexto com index, domain, rules |
| Projeto usa CrewAI, LangFuse, Chainlit | sim — kb/ de ferramentas por framework |
| context7 MCP disponivel | kb/ de ferramentas dispensavel |

## Estrutura quando kb/ fizer sentido

```text
kb/
  [framework]/
    index.md           — contexto e quando usar
    quick-reference.md — padrao pronto para copiar
```

Ou, para contexto de projeto:

```text
kb/
  index.md    — estado atual, proximos passos, fontes de verdade
  domain.md   — agentes, modelos, stack, escopo
  rules.md    — regras de negocio + contratos por agente
```

## Relacao com directives/

- `directives/` e a fonte de verdade — regras completas com contexto e motivacao
- `kb/` e o atalho operacional — o que aplicar agora sem reler tudo

Se conflitarem: `directives/` prevalece. Atualizar kb/ para refletir.

## Conclusao

`kb/` e opcional e contextual — nao e obrigatoria no pacote recomendado. Adicionar quando `directives/` for insuficiente para novas sessoes ou quando o projeto adotar frameworks que justifiquem referencia persistente.
