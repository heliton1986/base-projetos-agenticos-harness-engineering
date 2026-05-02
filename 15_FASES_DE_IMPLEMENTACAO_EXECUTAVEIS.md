# Fases de Implementacao Executaveis

## Objetivo

Este documento define uma camada opcional para organizar a execucao do projeto em fases operacionais guiadas por arquivos.

A ideia e transformar cada fase importante de implementacao em um guia executavel para a LLM, com:

- objetivo da fase
- pre-condicoes
- arquivos a consultar
- passos de execucao
- validacoes obrigatorias
- criterio de aprovacao
- proximo passo

## Por que essa camada existe

A base ja tem:

- `spec/` para estruturar as fases de implementacao
- `contracts/` para gates e acordos verificaveis
- `progress/` para acompanhar o estado atual
- `execution/` para trabalho deterministico
- `prompts/` para disciplinar a LLM

Mesmo assim, em projetos maiores, pode ser util ter uma camada adicional de guias de fase com foco em execucao sequencial.

## Principio central

Essas fases nao substituem:

- `spec/`
- `contracts/`
- `progress/`
- `execution/`

Elas funcionam como:

- runbooks de implementacao
- guias operacionais por etapa
- gatilhos claros para a LLM executar, validar, corrigir e seguir

## Estrutura recomendada

A recomendacao desta base e usar algo como:

```text
implementation/
  phase-01-bootstrap.md
  phase-02-first-incremental-capability.md
  phase-03-validation-and-observability.md
```

## Exemplo de fases iniciais

### phase-01-bootstrap.md

Responsavel por:

- montar estrutura do projeto
- criar README, AGENTS, directives, spec, execution
- registrar contratos minimos de dados quando necessario
- validar se a base esta pronta para a primeira capacidade

### phase-02-first-incremental-capability.md

Responsavel por:

- implementar a menor capacidade util de dominio
- usar contratos de dados, directives e spec para evitar improviso
- produzir artefatos reais e validaveis
- gerar status inicial da fase

### phase-03-validation-and-observability.md

Responsavel por:

- fortalecer gates
- registrar status e readiness
- expor observabilidade no frontend e/ou runtime
- preparar o sistema para fases seguintes com mais seguranca

## Como a LLM deve usar essas fases

Quando existir um diretório `implementation/`, a LLM deve:

1. identificar qual fase esta ativa
2. ler o arquivo da fase atual
3. executar a fase conforme os passos definidos
4. aplicar o `11_PROTOCOLO_DE_EXECUCAO_AGENTICA.md`
5. validar e corrigir se necessario
6. so seguir para a proxima fase se a fase atual estiver aprovada

## O que cada fase deve conter

Uma boa fase executavel deve declarar pelo menos:

- nome da fase
- objetivo
- pre-condicoes
- arquivos que precisam ser lidos antes
- passos de execucao
- validacoes obrigatorias
- politica de correcao
- criterio de aprovacao
- proxima fase sugerida

### Gate adicional para fases com UI ou API

Se a fase entrega FastAPI, Streamlit ou Chainlit, o criterio de aprovacao deve incluir verificacao live — nao apenas pytest:

| Componente | Verificacao minima |
|-----------|-------------------|
| FastAPI | `GET /health` retorna 200 + golden path com CSV real sem erro 422/500 |
| Streamlit | upload real + resultado renderiza + download funciona |
| Chainlit | pergunta real + streaming visivel + `cl.Step` de tool aparece |

pytest offline valida logica. Verificacao live valida stack completo. Os dois sao obrigatorios.

## Relacao com spec/

A diferenca principal e:

- `spec/` descreve a implementacao em nivel mais estrutural e de produto
- `implementation/` descreve a execucao da fase como workflow pratico para a LLM

Resumo:

- `spec/` diz o que a fase significa
- `implementation/` diz como percorrer a fase na pratica

## Quando e obrigatorio

`implementation/` e **obrigatorio** em projetos multi-agente (CrewAI, LangGraph com multiplos nos, qualquer sistema com handoff entre agentes).

Razao: agentes autonomos nao tem contexto de sessao — eles executam o que encontram nos arquivos. Sem runbooks de fase explícitos, o agente improvisa ordem, pula validacoes e nao sabe onde parar. O `implementation/` e o harness da execucao entre fases.

Sinais de que e obrigatorio:
- dois ou mais agentes com papeis distintos (Analyst, Researcher, Reporter)
- handoff de contrato entre agentes
- fases que so podem comecar apos a anterior estar aprovada
- execucao autonoma sem engenheiro presente em cada passo

## Quando e opcional

Apenas em projetos com agente unico e poucas fases onde:

- o engenheiro esta presente em todas as fases
- `spec/` + `progress/` + `execution/` cobrem os checkpoints
- o numero de fases e pequeno (menos de 4)

## Conclusao

`implementation/` e uma camada opcional de orquestracao por fase.

Em uma frase:

`spec define a fase; implementation ajuda a LLM a percorrer a fase.`
