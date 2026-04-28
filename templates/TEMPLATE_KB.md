# Template: KB de Ferramentas

## Objetivo

kb/ guarda padroes validados de uso de ferramentas e frameworks no projeto.
Modelo: kb-first → context7 fallback. Leitura local e mais rapida e barata que chamada MCP.

## Estrutura obrigatoria por ferramenta

```
kb/
  [ferramenta]/
    index.md           — contexto: como ESTE projeto usa a ferramenta, arquivos relevantes, regras
    quick-reference.md — padrao pronto para copiar: snippets, configuracoes, variaveis de ambiente
```

## index.md — estrutura

```markdown
# [Ferramenta] — [Nome do Projeto]

## Como este projeto usa [Ferramenta]

[descricao em 2-3 linhas — especifico do projeto, nao documentacao generica]

## [Tabelas / Modelos / Contratos / Agentes] (conforme relevante)

| Item | Arquivo | Papel |
|------|---------|-------|
| ... | ... | ... |

## Arquivos relevantes

- `caminho/arquivo.py` — descricao

## Regras de uso

- [regra especifica deste projeto]
- [limitacao ou padrao obrigatorio]
```

## quick-reference.md — estrutura

```markdown
# [Ferramenta] — Quick Reference

## [Caso de uso 1]

```python
# snippet pronto para usar
```

## [Caso de uso 2]

```python
# snippet pronto para usar
```

## Variaveis de ambiente

```
VAR=valor
```
```

## Quando criar kb/ de uma ferramenta

Criar quando o projeto usa a ferramenta de forma recorrente e ha padroes especificos do projeto que valem registrar. Nao copiar documentacao generica — apenas o que e especifico deste projeto.

Se a ferramenta e usada de forma basica e generica: consultar context7 on demand.

## Freshness

kb/ estatica pode ficar desatualizada quando a biblioteca lanca nova versao.
Verificar com context7 se houver mudancas relevantes na API usada.
Atualizar quick-reference.md quando o padrao do projeto mudar.

## Referencia

`05_KB_MINIMA_PARA_PROJETOS_AGENTICOS.md`
