# KB Minima para Projetos Agenticos

## Objetivo

Este documento define uma camada minima de `kb/` para projetos agenticos que usam `Harness Engineering`.

A ideia nao e obrigar todo projeto a nascer com uma base de conhecimento grande.
A ideia e definir o menor conjunto de conhecimento persistente que tende a gerar valor real para humanos e LLMs.

## Regra curta

Se o projeto for muito curto ou puramente exploratorio, a `kb/` pode nao existir no dia 1.

Se o projeto tiver continuidade, multiplas sessoes, mais de uma integracao ou risco de reexplicacao recorrente, vale muito considerar uma `kb/` minima.

## O que e uma KB minima

Uma `kb/` minima e um pequeno conjunto de arquivos reutilizaveis que preserva contexto importante do projeto sem depender apenas de:

- memoria da conversa
- README generico
- prompts repetidos
- reexplicacoes manuais

## Estrutura recomendada

```text
kb/
  project-operating-model.md
  architecture.md
  stack.md
```

## 1. project-operating-model.md

### Papel

Guardar como o projeto opera no dia a dia.

### O que pode conter

- como o agente deve trabalhar
- regras de handoff
- principios de validacao
- limites de autonomia
- criterios gerais de pronto
- convencoes de memoria operacional
- quando usar agente unico ou multi-agent

### Pergunta que responde

`Como este projeto funciona operacionalmente?`

## 2. architecture.md

### Papel

Guardar a arquitetura viva do sistema.

### O que pode conter

- principais componentes
- fluxo entre agentes
- stores
- tools
- integracoes
- pontos de validacao
- papel de cada camada

### Pergunta que responde

`Como este sistema e organizado tecnicamente?`

## 3. stack.md

### Papel

Guardar as decisoes tecnicas e convencoes da stack principal.

### O que pode conter

- frameworks usados
- bibliotecas principais
- convencoes tecnicas
- boas praticas da stack
- padroes de implementacao recorrentes
- o que evitar

### Pergunta que responde

`Como esta stack deve ser usada neste projeto?`

## Quando a KB minima faz sentido

Ela faz sentido quando pelo menos uma destas condicoes aparece:

- o projeto vai durar mais de alguns dias
- ha multiplas sessoes com LLMs
- ha mais de uma integracao importante
- o agente esta repetindo erros ou reexplicacoes
- ha mais de um agente ou mais de um fluxo relevante
- existe chance de reaproveitar o conhecimento em projetos futuros

## Quando nao precisa no inicio

Pode nao precisar no dia 1 quando:

- o projeto e uma prova de conceito curtissima
- a arquitetura ainda esta indefinida
- nao ha stack consolidada ainda
- a meta e apenas validar uma ideia em poucas horas

## Relacao com outros arquivos

### README.md

- contextualiza o projeto em nivel geral
- nao substitui a KB minima

### directives/

- guarda regras operacionais de dominio
- complementa a KB minima

### spec/

- organiza a entrega por fase
- nao substitui a KB minima

### AGENTS.md

- diz como o agente deve agir no runtime do projeto
- pode se apoiar na KB minima

## Diferenca entre KB minima e directives/

- `kb/` guarda conhecimento mais estavel e reaproveitavel
- `directives/` guarda regras operacionais e de dominio mais diretamente ligadas aos fluxos

Resumo pratico:

- `kb/` ensina o projeto
- `directives/` orienta a operacao do projeto

## Diferenca entre KB minima e references/

- `kb/` deve ser mais operacional e reutilizavel
- `references/` pode guardar material mais conceitual, comparativo ou de fundamentacao

## Recomendacao pratica

Se houver duvida, use esta regra:

- projeto curto: sem `kb/` no inicio ou apenas um arquivo leve
- projeto com continuidade: criar `kb/` minima
- projeto serio: evoluir a `kb/` minima para uma camada mais rica

## Estrategia de evolucao

Uma boa estrategia e:

### Etapa 1

Criar apenas:

```text
kb/
  project-operating-model.md
```

### Etapa 2

Adicionar:

```text
kb/
  architecture.md
  stack.md
```

### Etapa 3

Se houver necessidade, evoluir para arquivos mais especificos, como:

```text
kb/
  integrations.md
  validation-patterns.md
  multi-agent-patterns.md
  observability.md
```

## Conclusao

Uma `kb/` minima nao deve ser tratada como burocracia. Ela deve ser tratada como amortecedor de contexto e reaproveitamento.

Em uma frase:

`Nem todo projeto precisa nascer com uma KB grande, mas quase todo projeto agentico com continuidade se beneficia de uma KB minima bem escolhida.`

## Como a KB minima reduz invencao

A `kb/` nao serve apenas para guardar contexto. Ela tambem serve para evitar que a LLM preencha lacunas sensiveis com suposicoes soltas.

Em projetos com dados de negocio, especialmente `financas`, vale usar a KB minima para registrar pelo menos:

- como representar inconsistencias
- como consolidar saidas
- quais campos sao sensiveis
- quais suposicoes padrao sao aceitaveis e quais exigem confirmacao
