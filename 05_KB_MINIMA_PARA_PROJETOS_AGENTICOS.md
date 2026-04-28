# KB Minima para Projetos Agenticos

## Objetivo

Define a `kb/` minima obrigatoria para projetos agenticos com Harness Engineering.

Nao e burocracia. E amortecedor de contexto: sem kb/, cada sessao nova a LLM rele `directives/` do zero e preenche lacunas com suposicoes.

## Regra curta

Todo projeto com continuidade (mais de uma sessao, mais de um agente, fases sequenciais) deve ter `kb/` criada antes de implementar qualquer agente.

Excecao: prova de conceito curtissima (poucas horas, sem continuidade prevista).

## Estrutura obrigatoria

```text
kb/
  index.md    — estado atual, proximos passos, fontes de verdade
  domain.md   — agentes, modelos, stack, escopo, fluxo de execucao
  rules.md    — regras de negocio + contratos por agente
```

Usar `TEMPLATE_KB.md` para gerar os tres arquivos. Nunca gerar do zero.

## 1. index.md

### Papel

Orientacao rapida para novas sessoes — onde o projeto esta e o que fazer a seguir.

### O que contem

- versao atual e data
- status dos gates e testes
- proximos passos priorizados
- ponteiros para fontes de verdade (`directives/`, `model_routing.yaml`, `progress/`)

### Pergunta que responde

`Qual o estado atual do projeto e o que fazer agora?`

## 2. domain.md

### Papel

Contexto tecnico e de dominio denso — o que o sistema faz, como e organizado, quem usa LLM.

### O que contem

- o que o sistema faz e o que NAO faz (escopo da versao atual)
- tabela de agentes: nome, usa LLM, modelo, papel
- stack: linguagem, frameworks, banco, providers externos
- arquitetura de sessao DB (quem abre, quem passa, quem nao gerencia)
- regras de mascaramento antes do LLM (se aplicavel)
- fluxo de execucao por fase

### Pergunta que responde

`Como este sistema e organizado e como executa?`

## 3. rules.md

### Papel

Regras de negocio e contratos em formato consultavel — para nao ter que reler `directives/` completo.

### O que contem

- tabelas de regras por dominio (ingestao, deteccao, auditoria, relatorio)
- contratos de saida por agente (campos, tipos)
- regras de contrato (invalido = fase nao avanca, sem dict puro entre agentes)

### Pergunta que responde

`Quais regras governam o sistema e quais contratos cada agente produz?`

## Diferenca entre kb/ e directives/

- `directives/` e a fonte de verdade — explicacao completa com contexto e motivacao
- `kb/` e o resumo executavel — o que aplicar agora sem reler tudo

Se conflitarem: `directives/` prevalece. kb/ deve ser atualizada para refletir.

## Quando atualizar

- `index.md` — ao fim de cada fase (estado, proximos passos)
- `rules.md` — ao adicionar ou modificar regra de negocio ou contrato
- `domain.md` — ao adicionar agente ou mudar arquitetura

## Estrategia de evolucao

Comecar com os 3 arquivos obrigatorios. Se necessario, adicionar:

```text
kb/
  integrations.md       — detalhes de integrações externas
  validation-patterns.md — padrões de validação recorrentes
  observability.md      — como rastrear agentes, modelos, status
```

## Relacao com outros arquivos

| Arquivo | Papel | Substitui kb/? |
|---------|-------|---------------|
| `README.md` | Visao geral do projeto | nao |
| `directives/` | Regras operacionais completas — fonte de verdade | nao |
| `spec/` | Entrega por fase, requisitos verificaveis | nao |
| `AGENTS.md` | Comportamento da LLM no runtime | nao |
| `progress/PROGRESS.md` | Estado atual detalhado | nao — index.md aponta para ele |

## Como a kb/ reduz invencao

Sem kb/, a LLM preenche lacunas com suposicoes sobre:

- qual modelo usar por agente
- quais campos sao obrigatorios nos contratos
- o que ja foi implementado e aprovado
- quais regras de negocio existem

Com kb/ bem mantida, essas informacoes estao disponiveis em 3 arquivos densos sem reler o projeto inteiro.

## Conclusao

`kb/` nao e documentacao extra. E o contexto minimo que garante que sessoes futuras comecem do mesmo ponto que a sessao anterior terminou.
