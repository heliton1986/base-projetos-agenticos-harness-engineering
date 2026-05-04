# Template - Prompts por Fase de Projeto

## Objetivo

Este template gera a trilha faseada obrigatoria de um projeto concreto derivado da base quando houver teste controlado, validacao faseada ou uso como caso de referencia.

## Estrutura recomendada

```text
# Prompts por Fase - [NOME_DO_PROJETO]

## Objetivo

Esta sequencia adapta `prompts/base-generica/PROMPT_DEFINICAO_PROJETO.md` e `prompts/base-generica/PROMPTS_FASEADOS_BASE.md` especificamente para o `[nome-do-projeto]`.

## Ordem de uso

1. usar `prompts/projetos/[nome-do-projeto]/PROMPT_[PROJETO]_CANONICO.md` para a Fase 1
2. aprovar a definicao
3. seguir os prompts abaixo em ordem
4. nao pular fase sem gate aprovado

## Fase 1 - Definicao
[...]

## Fase 2 - Bootstrap
[...]

## Fase 3 - Validacao da Base
[...]
```

## Regras

- este arquivo governa a validacao e a evolucao faseada do projeto
- e obrigatorio quando o projeto servir para teste da base ou validacao controlada
- deve deixar claro quando o fluxo sai dos prompts e entra em `implementation/*.md`
- nao deve ser confundido com os runbooks internos de `implementation/`
