# Estrategia de Modelos para Agentes

## Objetivo

Este documento define uma estrategia pratica para escolher modelos diferentes dentro de um sistema agentico.

A ideia central e simples:

`Nem todo agente precisa do mesmo modelo.`

Em sistemas com `Harness Engineering`, a escolha de modelo deve levar em conta:

- papel do agente
- custo
- qualidade
- latencia
- tamanho de contexto
- risco da tarefa
- criticidade da validacao

## Principio geral

Usar o mesmo modelo para todos os agentes pode ser simples, mas raramente e a estrategia mais eficiente.

A abordagem mais madura e:

- usar modelos mais robustos onde a qualidade da decisao importa mais
- usar modelos mais economicos onde a tarefa e mais estreita, repetitiva ou delimitada
- preservar espaco para fallback e controle de custo

## Pergunta-chave

A pergunta correta nao e:

`Qual e o melhor modelo?`

A pergunta correta e:

`Qual e o modelo adequado para este papel dentro deste sistema?`

## Papeis tipicos

### Orchestrator

Papel:

- entende o pedido
- decide a estrategia
- escolhe entre agente unico e multi-agent
- faz handoff entre agentes
- consolida o fluxo geral

### Planner

Papel:

- decompoe o problema
- propõe fases
- define ordem de execucao
- organiza a estrategia da fase

### ResearchAgent

Papel:

- busca informacao
- pesquisa contexto
- explora bases e documentos
- consolida achados relevantes

### ExecutionAgent

Papel:

- executa tarefas delimitadas
- roda tools
- chama scripts
- produz artefatos operacionais

### Validator

Papel:

- verifica criterios
- executa checks
- avalia se a tarefa pode ser aprovada
- identifica gaps e falhas

### Reporter

Papel:

- sintetiza resultados
- transforma achados em resposta final
- organiza comunicacao para humano ou sistema

### Frontend-facing agent

Papel:

- traduz status para a UI
- monta mensagens intermediarias
- apresenta progresso e resultado final ao usuario

## Estrategia por papel

A estrategia abaixo nao e uma regra absoluta, mas um padrao muito razoavel.

### Orchestrator

Recomendacao:

- modelo mais robusto

Por que:

- decide arquitetura de execucao
- lida com ambiguidades
- escolhe handoffs
- precisa de maior capacidade de julgamento

### Planner

Recomendacao:

- modelo robusto ou medio

Por que:

- precisa decompor bem
- mas pode custar menos que o orchestrator em alguns cenarios

### ResearchAgent

Recomendacao:

- modelo medio

Por que:

- opera com escopo mais delimitado
- geralmente ganha mais com bom contexto e boas tools do que com o modelo mais caro possivel

### ExecutionAgent

Recomendacao:

- modelo barato ou medio

Por que:

- a tarefa tende a ser mais operacional
- o valor esta na execucao deterministica, nao em grande sofisticacao de linguagem

### Validator

Recomendacao:

- modelo medio ou robusto, conforme criticidade

Por que:

- validacao simples pode usar modelo medio
- validacao critica, semantica ou de alto risco pode justificar modelo mais forte

### Reporter

Recomendacao:

- modelo medio

Por que:

- precisa boa comunicacao e sintese
- mas normalmente nao exige o mesmo custo do orchestrator

### Frontend-facing agent

Recomendacao:

- modelo medio ou barato

Por que:

- muitas vezes vai resumir progresso e montar mensagens de interface
- nao precisa ser o agente mais forte do sistema na maioria dos casos

### Fallback

Recomendacao:

- modelo mais barato para tarefas simples, repetitivas ou de baixa criticidade

Por que:

- reduz custo
- preserva capacidade dos modelos mais fortes para momentos de maior valor

## Criterios de escolha

Ao escolher o modelo de cada papel, considere pelo menos:

### 1. Qualidade necessaria

- quanto erro esse papel pode tolerar?
- esse agente decide ou apenas executa?

### 2. Custo

- esse papel roda poucas vezes ou muitas vezes?
- esse agente esta em um loop frequente?

### 3. Latencia

- o usuario espera resposta imediata?
- esse passo esta no caminho critico da experiencia?

### 4. Tamanho de contexto

- esse agente precisa de contexto muito grande?
- esse papel se beneficia de janela longa?

### 5. Risco da tarefa

- uma decisao errada aqui pode gerar dano relevante?
- esse agente atua em partes sensiveis do sistema?

### 6. Criticidade da validacao

- a aprovacao dessa fase exige julgamento fino?
- a validacao e apenas estrutural ou tambem semantica?

## Padroes de composicao

### Padrao 1 - Orchestrator forte, executores economicos

Exemplo:

- `Orchestrator` -> forte
- `ResearchAgent` -> medio
- `ExecutionAgent` -> barato
- `Reporter` -> medio

Quando faz sentido:

- projetos com boa divisao de responsabilidades
- tasks especializadas com contexto delimitado

### Padrao 2 - Orchestrator forte, validator forte

Exemplo:

- `Orchestrator` -> forte
- `ExecutionAgent` -> medio
- `Validator` -> forte

Quando faz sentido:

- projeto de maior risco
- validacao com peso semantico alto
- gates de aprovacao mais exigentes

### Padrao 3 - Modelo medio quase para tudo

Exemplo:

- `Planner` -> medio
- `ResearchAgent` -> medio
- `ExecutionAgent` -> medio
- `Reporter` -> medio

Quando faz sentido:

- projeto simples
- budget limitado
- escopo pequeno

## Anti-padroes

### 1. Usar modelo caro para tudo

Problema:

- custo desnecessario
- pouco ganho em tarefas estreitas
- desperdicio de budget

### 2. Usar modelo barato no orchestrator sem criterio

Problema:

- pior decomposicao
- handoffs mais fracos
- maior risco de estrategia ruim

### 3. Usar o mesmo modelo em todo papel por conveniencia

Problema:

- perde a oportunidade de otimizar custo e desempenho por papel

### 4. Ignorar contexto e token budget

Problema:

- custo sobe sem necessidade
- fluxo degrada
- agentes carregam contexto demais

### 5. Validacao critica com modelo fraco sem compensacao

Problema:

- gates perdem credibilidade
- aumenta o risco de aprovacao inadequada

## Regra pratica de escolha

Se houver duvida, use algo assim como ponto de partida:

- `Orchestrator` -> robusto
- `Planner` -> robusto ou medio
- `ResearchAgent` -> medio
- `ExecutionAgent` -> barato ou medio
- `Validator` -> medio ou robusto, conforme criticidade
- `Reporter` -> medio
- `Frontend-facing agent` -> medio ou barato

Depois ajuste com base em:

- custo real
- latencia observada
- qualidade de resposta
- taxa de erro

## Relacao com a base de Harness

Este documento complementa especialmente:

- `01_FRAMEWORK_PRATICO_HARNESS_AGENTIC_SYSTEMS.md`
- `02_DOE_OPERACIONAL_PARA_HARNESS.md`
- `06_PADRAO_BUILDER_VALIDATOR_E_TASK_CONTRACTS.md`
- `07_FRONTEND_OBSERVAVEL_PARA_AGENTES.md`

E tambem pode influenciar:

- `AGENTS.md` do projeto
- `spec/03-design.md`
- `spec/04-build.md`
- `directives/` de orquestracao

## Onde isso deve aparecer em um projeto

### Em AGENTS.md

- politica de uso de modelos por papel
- criterios para agente unico vs multi-agent

### Em spec/

- decisao arquitetural de distribuicao dos agentes
- modelo escolhido por papel

### Em directives/

- regras de custo, latencia ou fallback quando necessario

## Conclusao

Escolher modelos por papel e uma parte importante de maturidade em sistemas agenticos.

Em uma frase:

`Orquestradores decidem, executores operam, validadores protegem o sistema; a estrategia de modelo deve refletir essa diferenca de responsabilidade.`


## Observabilidade da estrategia

A estrategia de modelos por papel so fica realmente confiavel quando o runtime consegue registrar e exibir:

- qual agente usou qual modelo
- qual provider foi usado
- status da etapa
- retries
- validacao associada

Para isso, consulte tambem `13_OBSERVABILIDADE_DE_MODELOS_E_AGENTES.md`.
