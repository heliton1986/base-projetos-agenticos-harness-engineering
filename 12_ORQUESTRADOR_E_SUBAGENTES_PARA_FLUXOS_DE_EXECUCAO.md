# Orquestrador e Subagentes para Fluxos de Execucao

## Objetivo

Este documento explicita como modelar fluxos de execucao agentica com:

- um `orquestrador`
- subagentes especializados
- handoffs claros
- estrategia de modelos por papel

Ele complementa o `11_PROTOCOLO_DE_EXECUCAO_AGENTICA.md`.

## Pergunta central

Quando o usuario pedir algo como:

- `@run_onboarding_flow.py`
- `rode a primeira capacidade`
- `execute, valide e corrija`

quem faz o que dentro do sistema agentico?

A resposta recomendada desta base e:

- um `Orchestrator` coordena o fluxo
- subagentes especializados executam partes delimitadas
- a selecao de modelo deve seguir o papel de cada agente

## O que a base ja dizia implicitamente

A base ja trazia, de forma distribuída:

- `DOE`: separacao entre decisao e execucao
- `Builder/Validator`: separacao entre fazer e validar
- `Model routing`: modelos diferentes por papel
- `Frontend observavel`: etapas e status visiveis
- `Protocolo de execucao`: executar, corrigir, reexecutar, validar e reportar

O que faltava era juntar tudo isso num padrao unico para fluxos executaveis.

## Arquitetura recomendada

### 1. Orchestrator

Responsavel por:

- interpretar o pedido do usuario
- decidir qual fluxo ou script executar
- escolher agente unico ou multi-agent
- decidir retry, correcao ou escalacao
- consolidar o estado atual
- reportar progresso no chat

Este e o melhor lugar para um modelo mais robusto.

### 2. ExecutionAgent

Responsavel por:

- rodar o script ou comando principal
- capturar stdout/stderr
- verificar arquivos gerados
- devolver resultado estruturado ao orquestrador

Esse papel tende a funcionar bem com modelo medio ou economico.

### 3. FixAgent

Responsavel por:

- corrigir erros locais de codigo, path ou configuracao simples
- ajustar scripts quebrados
- reduzir falhas de execucao de baixo risco

Esse papel tende a funcionar bem com modelo medio.

### 4. ValidatorAgent

Responsavel por:

- rodar validacoes e gates
- verificar se o fluxo passou
- apontar o que ainda esta pendente
- distinguir falha local de bloqueio real

Esse papel pode usar modelo medio ou robusto, dependendo da criticidade.

### 5. ReporterAgent

Responsavel por:

- transformar o estado do fluxo em mensagem clara para o usuario
- resumir o que executou, o que falhou e o que foi corrigido
- informar se API e frontend ja podem ser abertos

Esse papel tende a funcionar bem com modelo medio ou economico.

## Handoff recomendado

Cada handoff deve incluir:

- objetivo da subtarefa
- contexto suficiente
- restricoes importantes
- formato esperado do retorno
- gates relevantes

Exemplo:

- `Orchestrator -> ExecutionAgent`: rode `run_onboarding_flow.py` e devolva status estruturado
- `Orchestrator -> FixAgent`: houve erro local de import; corrija sem expandir escopo
- `Orchestrator -> ValidatorAgent`: confirme se os gates minimos passaram
- `Orchestrator -> ReporterAgent`: transforme o estado atual em update curto para o usuario

## Estrategia de modelos por papel

### Orchestrator

- modelo mais robusto

Porque:

- decide estrategia
- interpreta risco
- escolhe retry ou escalacao
- coordena subagentes

### ExecutionAgent

- modelo medio ou economico

Porque:

- a tarefa e mais operacional
- depende mais de comando, script e artefato do que de julgamento amplo

### FixAgent

- modelo medio

Porque:

- precisa raciocinio tecnico localizado
- normalmente trabalha em escopo menor

### ValidatorAgent

- modelo medio ou robusto

Porque:

- validacao estrutural pode ser media
- validacao semantica ou de maior risco pode exigir algo mais forte

### ReporterAgent

- modelo medio ou economico

Porque:

- resume e comunica
- normalmente nao precisa da maior capacidade de raciocinio do sistema

## 6 Padroes de Orquestracao

Sistemas agenticos reais nao sao apenas sequencias lineares. Escolha o padrao pelo tipo de problema.

### 1. Sequential

Agente A → Agente B → Agente C em ordem fixa.

Quando usar: passos com dependencia estrita de ordem, output de um e input do proximo.

Exemplo: ingestao → deteccao → relatorio (FinanceOps fase manual).

Limitacao: nenhuma decisao de roteamento — mais pipeline do que agente.

### 2. Parallel

Multiplos agentes executam simultaneamente, resultados consolidados ao final (fan-out / fan-in).

Quando usar: tarefas independentes que podem rodar ao mesmo tempo sem dependencia entre si.

Exemplo: agente SQL e agente semantico consultando stores diferentes ao mesmo tempo, orquestrador consolida.

### 3. Hierarchical

Agente manager delega para agentes especialistas. Manager decide quem executa o que.

Quando usar: problema complexo com subdivisao clara de domínios; manager precisa raciocinar sobre delegacao.

Exemplo: ShopAgent — manager recebe pedido, delega para agente de busca, agente de preco, agente de estoque.

### 4. Reactive

Agentes respondem a eventos em tempo real, nao a pedidos explícitos.

Quando usar: monitoramento continuo, alertas, triggers baseados em condicoes externas.

Exemplo: agente que observa pipeline de dados e dispara acao quando anomalia e detectada.

### 5. Adaptive

Agentes aprendem com feedback e ajustam comportamento ao longo do tempo.

Quando usar: sistemas com ciclo de melhoria continua, onde runs anteriores informam runs futuros.

Exemplo: agente que ajusta threshold de deteccao baseado em taxa de falso positivo historica.

### 6. Hybrid

Combinacao de padroes por fase ou contexto.

Quando usar: sistemas de producao complexos onde nenhum padrao unico serve para todas as etapas.

Exemplo: hierarchical para decisao de rota + parallel para coleta de dados + sequential para geracao de relatorio.

### 7. Consensus (uso condicional)

Multiplos agentes independentes avaliam o mesmo problema e votam — a resposta com maior concordancia vence.

Quando usar: classificacao de alto risco (medico, legal, financeiro) onde single agent tem confianca insuficiente; reducao de alucinacao em outputs criticos; tarefas ambiguas onde concordancia entre agentes e um gate de qualidade.

Exemplo: 3 agentes avaliam se uma transacao e fraude — maioria vence. Cada agente usa prompt diferente para evitar correlacao de erro.

**Atencao — nao usar por padrao:**
- Custo: N × mais chamadas LLM
- Falsa seguranca se prompt identico — 3 agentes erram igual
- Substituivel por ValidatorAgent + gate determinístico (pytest/Pydantic) na maioria dos casos

Use Consensus apenas quando gate determinístico nao for suficiente para o nivel de risco.

### Guia rapido de selecao

| Cenario | Padrao |
|---|---|
| Passos com dependencia estrita | Sequential |
| Tarefas independentes simultaneas | Parallel |
| Problema com subdivisao de domínios | Hierarchical |
| Monitoramento e alertas | Reactive |
| Melhoria continua com historico | Adaptive |
| Sistema completo de producao | Hybrid |
| Alto risco + gate determinístico insuficiente | Consensus |

Fonte: Semana AI Data Engineer 2026, Dias 3-4 — Orchestration Patterns

## Quando usar agente unico

Use agente unico quando:

- o fluxo for simples
- o numero de passos for pequeno
- nao houver grande risco de retry complexo
- a validacao for direta

## Quando usar orquestrador com subagentes

Use orquestrador com subagentes quando:

- houver execucao, correcao e validacao como fases distintas
- o fluxo tiver retries relevantes
- a observabilidade for importante
- o custo/contexto de um agente unico ficar ruim
- quiser separar responsabilidade entre operar, corrigir, validar e reportar

## Fluxo operacional recomendado

1. `Orchestrator` recebe o pedido do usuario
2. decide qual fluxo executar
3. aciona `ExecutionAgent`
4. se houver erro local corrigivel, aciona `FixAgent`
5. reexecuta
6. aciona `ValidatorAgent`
7. aciona `ReporterAgent`
8. comunica se o sistema esta pronto ou bloqueado

## Relacao com o onboarding

Quando existir um `run_onboarding_flow.py`, uma boa arquitetura e:

- `Orchestrator`: decide e acompanha
- `ExecutionAgent`: roda o onboarding
- `FixAgent`: corrige erro local, se houver
- `ValidatorAgent`: verifica os gates
- `ReporterAgent`: informa no chat e/ou frontend

## Anti-padroes

Evite:

- usar um unico agente para tudo sem necessidade
- usar modelo caro para todos os papeis
- deixar o mesmo agente executar e julgar tudo
- usar subagentes sem handoff claro
- abrir API/frontend sem validar gates minimos

## Conclusao

Sim, a base ja apontava para esse desenho.

Mas agora isso fica formalizado de maneira explicita:

- `11` define como executar agenticamente
- `12` define como distribuir esse trabalho entre orquestrador e subagentes
- `10` define como escolher modelos por papel

Em uma frase:

`O protocolo diz o que fazer; este documento diz quem faz o que.`

## Referencias

Os padroes descritos aqui sao agnósticos de modelo e provedor. As fontes abaixo nomearam e documentaram o padrao orchestrator-workers na literatura.

- **Anthropic — Building effective agents** (2024): nomeia explicitamente o padrao `orchestrator-workers` — "Orchestrators direct agents to use tools or undertake tasks with the intention of completing some broader goal. Workers follow orchestrator directions." Equivalente direto ao modelo descrito neste documento.
  Disponivel em: https://www.anthropic.com/research/building-effective-agents

- **OpenAI — A practical guide to building agents** (2025): descreve arquitetura multi-agent com orquestrador central coordenando subagentes especializados, incluindo handoffs e estrategia de modelo por papel.
  Disponivel em: https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf

- **Yao et al. — ReAct** (2022): base academica do loop executar → observar → corrigir que sustenta o fluxo operacional do ExecutionAgent e FixAgent neste documento.
  Disponivel em: https://arxiv.org/abs/2210.03629


## Observabilidade

Quando esta arquitetura estiver ativa, vale registrar e exibir por agente:

- nome do agente
- papel
- modelo usado
- provider
- status
- retries
- validacao

Para isso, consulte tambem `13_OBSERVABILIDADE_DE_MODELOS_E_AGENTES.md`.
