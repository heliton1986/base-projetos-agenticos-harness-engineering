# Template - Prompt Canonico de Projeto

## Objetivo

Este template gera o prompt canonico obrigatorio de um projeto derivado da base.

Uso esperado:

- sempre criar um prompt canonico do projeto
- usar esse arquivo como camada entre a base generica e o projeto concreto
- apontar para o prompt por fase do projeto quando a definicao inicial estiver aprovada

## Estrutura recomendada

```text
# Prompt Canonico - [NOME_DO_PROJETO]

## Objetivo

Prompt pronto para iniciar o `[nome-do-projeto]` com `prompts/base-generica/PROMPT_DEFINICAO_PROJETO.md`, ja alinhado com:

- [restricao ou decisao 1]
- [restricao ou decisao 2]
- [restricao ou decisao 3]

## Como usar

Copie o bloco abaixo e envie como prompt inicial na sessao que vai criar o projeto.

Depois da Fase 1 aprovada, continue com:

- `prompts/projetos/[nome-do-projeto]/PROMPTS_[PROJETO]_POR_FASE.md`

```text
[prompt concreto de definicao do projeto]
```
```

## Regras

- este arquivo e obrigatorio em todo projeto derivado iniciado com a base
- deve traduzir a base generica para o contexto concreto do projeto
- deve explicitar conflitos com legados, restricoes e estrutura esperada
- nao substituir `implementation/`; ele governa o inicio e a definicao do projeto
