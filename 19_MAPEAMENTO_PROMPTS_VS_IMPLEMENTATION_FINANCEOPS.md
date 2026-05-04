# Niveis entre Prompts da Base, Prompts de Projeto e `implementation/`

## Objetivo

Explicar a diferenca entre tres niveis que usam a palavra "fase", mas nao operam no mesmo plano:

- prompts da base generica
- prompts do projeto concreto
- runbooks de execucao interna em `implementation/`

Este documento existe para evitar leitura enganosa de equivalencia direta entre macrofases da base e fases internas do projeto.

## Niveis

| Nivel | Arquivos | Papel |
|------|----------|-------|
| Base generica | `prompts/base-generica/PROMPT_DEFINICAO_PROJETO.md`, `prompts/base-generica/PROMPT_EXECUCAO_AUTONOMA_PROJETO.md`, `prompts/base-generica/PROMPTS_FASEADOS_BASE.md` | Definem a metodologia geral de criacao e evolucao de qualquer projeto derivado |
| Projeto | `prompts/projetos/[projeto]/PROMPT_[PROJETO]_CANONICO.md`, `prompts/projetos/[projeto]/PROMPTS_[PROJETO]_POR_FASE.md` | Traduzem a base generica para um caso concreto e governam a validacao faseada daquele projeto |
| Execucao interna | `implementation/*.md` dentro do projeto | Descrevem como implementar e validar as capacidades reais do produto depois que a base do projeto ja foi definida e aprovada |

## Quando usar cada nivel

### Base generica

Use os prompts da base quando o objetivo ainda for:

- iniciar um projeto novo
- organizar a jornada geral de definicao, bootstrap, validacao e expansao
- aplicar o modelo Harness de forma independente do dominio

### Projeto

Use prompts do projeto quando:

- o projeto tiver contexto proprio, restricoes especificas ou legado relevante
- houver necessidade de teste controlado ou validacao faseada
- o projeto for servir como caso canonico da base

Regra atual da base:

- todo projeto derivado deve ter um `PROMPT_[PROJETO]_CANONICO.md`
- se o projeto passar por teste, validacao controlada ou execucao faseada, deve ter tambem `PROMPTS_[PROJETO]_POR_FASE.md`

### Execucao interna

Use `implementation/*.md` apenas depois que:

- a definicao do projeto estiver aprovada
- o bootstrap estrutural estiver pronto
- a base do projeto tiver sido validada

`implementation/` nao substitui os prompts. Ele entra depois, como harness operacional das capacidades reais.

## O que nao mapear 1:1

Nao assumir que:

- uma fase em `prompts/base-generica/PROMPTS_FASEADOS_BASE.md` corresponde diretamente a uma fase em `implementation/`
- a Fase 4 do projeto sempre vira exatamente um unico arquivo de `implementation/`
- a Fase 5 da base generica equivale linearmente a todas as fases internas seguintes do projeto

Exemplo no `financeops-v2`:

- a Fase 4 do prompt especializado inaugura a entrada no core incremental
- dentro do projeto, esse core se desdobra em ingestao, deteccao deterministica, deteccao semantica, relatorio e API/UI

Ou seja: o prompt do projeto governa a jornada do experimento; `implementation/` governa a execucao interna do produto.

## Fluxo correto de leitura

1. Ler `prompts/base-generica/PROMPT_DEFINICAO_PROJETO.md` ou `prompts/base-generica/PROMPT_EXECUCAO_AUTONOMA_PROJETO.md`
2. Criar ou usar `prompts/projetos/[projeto]/PROMPT_[PROJETO]_CANONICO.md`
3. Seguir `prompts/projetos/[projeto]/PROMPTS_[PROJETO]_POR_FASE.md` quando houver validacao faseada
4. So depois do bootstrap aprovado e da base validada, entrar em `implementation/*.md`

## Resumo

Em uma frase:

`prompts da base definem a metodologia, prompts do projeto definem a trilha concreta, e implementation define a execucao operacional das capacidades do produto`
