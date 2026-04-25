# spec/02-define.md — [NOME DO PROJETO]

## Objetivo deste documento

Transformar o brainstorm em requisitos verificaveis. Tudo aqui deve ser testavel ou validavel.

## Declaracao de escopo

### O que o sistema faz

[2-3 frases precisas sobre o que o sistema entrega]

### O que o sistema nao faz (fora de escopo)

- [exclusao 1]
- [exclusao 2]
- [exclusao 3]

## Usuarios e casos de uso

| Usuario | Caso de uso | Resultado esperado |
|---------|-------------|-------------------|
| [perfil] | [acao] | [resultado] |

## Requisitos funcionais

| ID | Requisito | Criterio de aceite |
|----|-----------|-------------------|
| RF-01 | [requisito] | [como validar] |
| RF-02 | [requisito] | [como validar] |

## Requisitos nao funcionais

| ID | Requisito | Criterio de aceite |
|----|-----------|-------------------|
| RNF-01 | [ex: audit_log imutavel] | [como validar] |
| RNF-02 | [ex: dados sensiveis mascarados] | [como validar] |

## Restricoes de negocio obrigatorias

Estas restricoes nao podem ser violadas em nenhuma circunstancia:

1. [restricao critica 1]
2. [restricao critica 2]

## Dados de entrada

| Fonte | Formato | Frequencia | Obrigatorio |
|-------|---------|------------|-------------|
| [fonte] | [CSV/JSON/API] | [diario/manual/...] | sim/nao |

## Dados de saida

| Saida | Formato | Destino | Descricao |
|-------|---------|---------|-----------|
| [saida] | [tipo] | [onde vai] | [descricao] |

## Dependencias externas

| Sistema | Tipo | Modo de acesso | Criticidade |
|---------|------|---------------|-------------|
| [sistema] | [API/DB/arquivo] | [leitura/escrita] | [critico/opcional] |

## Criterios de aceite do projeto

O projeto so e considerado funcional quando:

- [ ] [criterio 1]
- [ ] [criterio 2]
- [ ] [criterio 3]

## Perguntas resolvidas (do brainstorm)

| Pergunta | Decisao | Justificativa |
|----------|---------|--------------|
| [pergunta] | [decisao] | [por que] |

## Perguntas ainda em aberto

- [pergunta que ficou sem resposta]
