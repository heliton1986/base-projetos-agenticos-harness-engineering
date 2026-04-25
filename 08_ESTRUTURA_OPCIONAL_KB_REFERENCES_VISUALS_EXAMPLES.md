# Estrutura Opcional: KB, References, Visuals e Examples

## Objetivo

Este documento propoe uma camada opcional de apoio para a base de projetos agenticos com `Harness Engineering`.

A ideia e enriquecer a base sem poluir o nucleo operacional.

O nucleo continua sendo:

- framework
- DOE
- bootstrap
- checklist
- prompts
- definicao de README, directives e spec

A camada opcional existe para apoiar:

- reaproveitamento de conhecimento
- onboarding
- exemplos concretos
- explicacoes visuais
- referencias tecnicas recorrentes

Observacao:

- a referencia principal para uma `kb/` enxuta e `KB_MINIMA_PARA_PROJETOS_AGENTICOS.md`

## Estrutura sugerida

```text
base-projetos-agenticos-harness-engineering/
  prompts/
  kb/
  references/
  visuals/
  examples/
```

## kb/

`kb/` significa `knowledge base`.

### Para que serve

Guardar conhecimento reutilizavel que a LLM ou o humano pode consultar repetidamente.

### O que pode entrar aqui

- explicacoes de frameworks
- padroes recorrentes
- componentes tecnicos usados com frequencia
- boas praticas da stack
- guias curtos por tecnologia

### Exemplos de arquivos

```text
kb/
  langgraph.md
  crewai.md
  fastapi.md
  qdrant.md
  postgres.md
  observability.md
  multi-agent-patterns.md
```

### Quando faz sentido

- quando voces repetem stack e componentes em varios projetos
- quando querem reduzir reexplicacao recorrente
- quando certos padroes ja estao consolidados

## references/

`references/` e a camada de material de consulta tecnica ou conceitual.

### Para que serve

Guardar material de apoio que fundamenta decisoes, mas que nao precisa entrar no fluxo operacional do dia a dia.

### O que pode entrar aqui

- artigos resumidos
- notas de comparacao entre ferramentas
- transcricoes de videos
- comparativos entre abordagens
- papers ou resumos de papers
- documentos que explicam porque certas escolhas fazem sentido

### Exemplos de arquivos

```text
references/
  video1-harness-summary.md
  video2-harness-summary.md
  crewai-vs-langgraph.md
  spec-driven-vs-harness.md
  token-budget-notes.md
```

### Diferenca para kb/

- `kb/` tende a ser mais operacional e reaproveitavel
- `references/` tende a ser mais conceitual, comparativo ou de fundamentacao

## visuals/

`visuals/` e a camada de apoio visual.

### Para que serve

Guardar material visual que ajuda a explicar arquitetura, runtime, handoff e organizacao dos sistemas agenticos.

### O que pode entrar aqui

- diagramas
- imagens
- excalidraw
- slides exportados
- capturas de tela exemplificando fluxos

### Exemplos de arquivos

```text
visuals/
  harness-runtime.excalidraw
  doe-architecture.excalidraw
  multi-agent-flow.png
  validation-gates.png
```

### Quando faz sentido

- quando a explicacao visual ajuda mais do que texto puro
- quando voces querem reaproveitar diagramas em novos projetos ou materiais

## examples/

`examples/` e a camada de exemplos concretos.

### Para que serve

Mostrar como a base se traduz em projetos ou artefatos reais.

### O que pode entrar aqui

- exemplos de README bem feitos
- exemplos de AGENTS.md
- exemplos de directives/
- exemplos de spec/
- mini projetos de referencia
- exemplos de bootstrap completo

### Exemplos de arquivos

```text
examples/
  readme-ecommerce-example.md
  agents-finance-example.md
  directives-support-example/
  spec-dataops-example/
  bootstrap-minimo-example/
```

### Quando faz sentido

- quando voces querem acelerar novos projetos
- quando desejam mostrar padroes de alta qualidade
- quando querem diminuir a variabilidade de output da LLM

## Como nao poluir o nucleo

A regra importante e:

- o nucleo deve continuar pequeno e operacional
- a camada opcional deve servir de apoio, nao de dependencia obrigatoria para tudo

Ou seja:

- `kb/`, `references/`, `visuals/` e `examples/` ajudam muito
- mas nao devem tornar a base pesada demais para usar

## Ordem de prioridade

Se fossem criar por etapas, eu faria assim:

1. `examples/`
2. `kb/`
3. `references/`
4. `visuals/`

### Por que essa ordem

- `examples/` gera valor pratico mais rapido
- `kb/` reduz reexplicacao recorrente
- `references/` fortalece a base conceitual
- `visuals/` ajudam bastante, mas sao mais complementares

## Recomendacao pratica

Se quiserem manter a base enxuta, comecem apenas com:

```text
examples/
kb/
```

E adicionem `references/` e `visuals/` depois, conforme a necessidade.

## Conclusao

Essas quatro pastas nao substituem o nucleo da base. Elas funcionam como camada opcional de apoio.

Em uma frase:

`kb/ ensina, references/ fundamenta, visuals/ explica visualmente e examples/ mostra como fazer na pratica.`
