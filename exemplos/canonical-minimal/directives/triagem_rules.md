# Diretivas de Triagem — Issue Triage Agent

## Severidades validas

| Valor | Criterio |
|-------|---------|
| `critica` | Sistema fora do ar, perda de dados, bloqueio total de usuarios |
| `alta` | Funcionalidade principal quebrada, sem workaround |
| `media` | Funcionalidade degradada, workaround existe |
| `baixa` | Melhoria, cosmético, documentacao |

Regra: se ambiguo entre dois niveis, usar o mais alto.

## Categorias validas

| Valor | Criterio |
|-------|---------|
| `bug` | Comportamento incorreto vs especificacao |
| `feature` | Nova funcionalidade solicitada |
| `performance` | Lentidao, timeout, uso excessivo de recursos |
| `seguranca` | Vulnerabilidade, exposicao de dados, autenticacao |
| `documentacao` | Erro ou ausencia em docs, READMEs, comentarios |
| `duvida` | Pergunta sobre uso, nao e problema tecnico |

Regra: uma issue pode ter apenas UMA categoria principal.

## Regras de classificacao

1. Severidade `critica` so pode ser atribuida a categorias `bug` ou `seguranca`
2. Categoria `duvida` tem severidade maxima `baixa`
3. Categoria `feature` tem severidade maxima `media`
4. Justificativa e obrigatoria — sem excecao
5. Se o texto da issue for vago demais para classificar com confianca, retornar `confianca: baixa` no output

## O que ClassifierAgent NAO pode fazer

- Inventar severidades ou categorias fora das listas acima
- Atribuir `critica` a `feature` ou `documentacao`
- Retornar classificacao sem justificativa
- Assumir contexto que nao esta no texto da issue
