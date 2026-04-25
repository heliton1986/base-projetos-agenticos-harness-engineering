# Padrao Builder, Validator e Task Contracts

## Objetivo

Este documento formaliza uma parte central da visao de `Harness Engineering`: separar implementacao, validacao e aprovacao por meio de contratos de tarefa e gates explicitos.

Ele complementa a base existente, principalmente no lado de:

- confiabilidade operacional
- task contracts
- builder vs validator
- loop de correcao
- evidencias de validacao

## Problema que este padrao resolve

Um erro comum em sistemas agenticos e deixar o mesmo agente:

- implementar
- julgar a propria implementacao
- declarar que esta pronto

Esse modelo tende a gerar:

- vitoria prematura
- validacao superficial
- regressao acumulada
- entregas sem evidencia suficiente

A ideia deste padrao e reduzir esse risco.

## Estrutura conceitual

O padrao se apoia em tres papeis logicos.

### 1. Builder

Responsavel por:

- implementar
- ajustar
- produzir artefatos
- corrigir falhas apontadas

### 2. Validator

Responsavel por:

- verificar criterios acordados
- executar checks e sensores
- identificar gaps
- reprovar ou aprovar tecnicamente a entrega

### 3. Orchestrator

Responsavel por:

- decidir o que vai para construcao
- encaminhar para validacao
- decidir se volta para correcao
- aprovar encerramento da fase

## O que e um Task Contract

Um `task contract` e o acordo explicito sobre o que precisa ser entregue em uma tarefa ou fase.

Ele deve reduzir ambiguidade para:

- quem constrói
- quem valida
- quem aprova

## Estrutura minima de um Task Contract

Um contrato de tarefa deve responder pelo menos:

- qual o objetivo da tarefa
- qual o escopo
- o que esta fora de escopo
- quais arquivos ou componentes podem ser tocados
- quais outputs sao esperados
- quais validacoes sao obrigatorias
- quais evidencias precisam existir
- o que significa pronto

## Template sugerido

```text
Task Contract

- Objetivo:
- Escopo:
- Fora de escopo:
- Artefatos afetados:
- Output esperado:
- Validacoes obrigatorias:
- Evidencias exigidas:
- Criterio de pronto:
```

## Exemplo resumido

```text
Task Contract

- Objetivo: implementar a primeira rota de consulta de pedidos
- Escopo: endpoint de leitura + validacao minima + teste basico
- Fora de escopo: autenticacao e dashboard
- Artefatos afetados: api/, tests/, docs/
- Output esperado: endpoint funcional e resposta estruturada
- Validacoes obrigatorias: teste de rota + lint + typecheck
- Evidencias exigidas: comando executado e resultado verde
- Criterio de pronto: endpoint funcionando e validacoes minimas aprovadas
```

## Gates de validacao

Um gate e um ponto explicito de aprovacao antes da proxima etapa.

Exemplos de gates:

- gate de bootstrap
- gate de implementacao da fase
- gate de validacao funcional
- gate de qualidade minima
- gate de entrega final

## Regra pratica

`Uma fase nao deve avancar se o gate atual nao estiver aprovado.`

## Evidencias de validacao

Validacao forte nao deve depender apenas de texto declarativo.

Sempre que possivel, a entrega deve apresentar evidencias como:

- testes passando
- lint sem erro
- typecheck sem erro
- evals minimos aprovados
- saida esperada gerada
- contrato atendido item a item

## Loop de correcao

O fluxo recomendado e:

1. Builder implementa
2. Validator verifica
3. Se falhar, registrar motivo
4. Builder corrige
5. Validator reavalia
6. Orchestrator decide aprovacao

## O que o Validator deve checar

O validator deve responder pelo menos:

- o escopo foi respeitado?
- a saida pedida existe?
- os gates obrigatorios passaram?
- houve quebra de restricoes?
- a tarefa foi realmente concluida ou apenas parcialmente adiantada?

## O que o Builder nao deve fazer

O builder nao deve:

- declarar pronto sem validacao
- expandir escopo por conta propria
- ignorar restricoes do task contract
- substituir evidencias por opiniao

## Relacao com outros artefatos da base

### README.md

- contextualiza o projeto
- nao substitui task contract

### directives/

- define regras operacionais do dominio
- nao substitui criterios de aceite da tarefa

### spec/

- organiza a fase e o plano
- e o melhor lugar para desdobrar task contracts de fase

### AGENTS.md

- define como os agentes operam
- pode incorporar o padrao builder/validator como politica do projeto

### FRONTEND_OBSERVAVEL_PARA_AGENTES.md

- pode exibir visualmente:
  - em execucao
  - validando
  - falhou
  - em correcao
  - validado

## Onde esse padrao pode aparecer no projeto

### Em spec/

Exemplo:

```text
spec/
  04-build.md
  05-validate.md
```

### Em contracts/

Exemplo:

```text
contracts/
  feature-01.md
  feature-02.md
```

### Em AGENTS.md

Como regra operacional de fluxo.

## Quando usar a versao minima deste padrao

Mesmo em projeto pequeno, faz sentido pelo menos ter:

- objetivo da tarefa
- escopo
- validacoes obrigatorias
- criterio de pronto

## Quando usar a versao forte

Use com mais rigor quando:

- ha multiplos agentes
- ha handoffs complexos
- ha risco de regressao
- o projeto vai durar varias sessoes
- a entrega precisa de auditabilidade

## Conclusao

Este padrao transforma a validacao de algo implicito em algo estrutural.

Em uma frase:

`Builder constrói, Validator verifica, Orchestrator aprova; o task contract impede que o sistema avance no escuro.`
