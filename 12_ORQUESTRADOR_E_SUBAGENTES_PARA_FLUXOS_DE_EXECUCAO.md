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

## Processos Separados vs Subagentes no Mesmo Processo

Esta e uma das distincoes mais importantes do harness — e a que mais projetos ignoram.

### Subagente no mesmo processo

O orquestrador chama um subagente como funcao ou tool call dentro do mesmo contexto.

```python
# mesmo processo — contexto compartilhado
resultado = builder_agent.executar(tarefa)
validacao = validator_agent.validar(resultado)
```

O validator tem acesso ao contexto do builder — pode ser "contaminado" pelo raciocinio anterior.

### Agentes em processos separados

Orquestrador inicia cada agente em processo independente, com contexto proprio.

```
Orchestrator (Processo 1)
  ↓ lanca
Builder    (Processo 2 — contexto isolado — missao: implementar)
  ↓ retorna artefato
Orchestrator
  ↓ lanca
Validator  (Processo 3 — contexto isolado — missao: validar)
  ↓ retorna veredicto
Orchestrator decide: aprovar ou corrigir
```

**Por que processos separados importam:**
- Builder com missao de implementar vai implementar — mesmo que precise deletar codigo
- Validator com missao de validar vai validar — sem ser influenciado por como o builder raciocinou
- Sem contexto compartilhado, o validator nao pode ser "convencido" pelo builder
- Claude Code (vazamento de codigo, 2025) ja se instrumenta para esse padrao — Builder e Validator em janelas separadas

**Quando usar:**
- Fluxos criticos onde validacao independente e obrigatoria
- Sistemas com loop de autocorrecao que precisam de veredicto limpo
- Qualquer contexto onde "agente julga o proprio trabalho" e um risco inaceitavel

**Quando subagente no mesmo processo e suficiente:**
- Tarefas de baixo risco onde validacao e estrutural (Pydantic)
- Fase manual do harness — pipeline sequencial sem autonomia de fluxo
- Prototipo ou fase inicial onde custo de processos separados nao se justifica

Fonte: VIDEO1_HARNESS.md — "Em outro processo, tem o processo orquestrador que inicia um para implementar e inicia outro para validar. Nao e um sub agent."

---

## Loop de Autocorrecao Orquestrado

O loop de autocorrecao e o coracao de um sistema agentico confiavel. Sem ele, o fluxo para no primeiro erro.

### Estrutura do loop

```
1. Orchestrator define tarefa + criterios de pronto
2. Builder executa
3. Validator verifica contra criterios
4. SE passou → Orchestrator aprova e avanca
5. SE falhou → Orchestrator aciona FixAgent com erro especifico
6. FixAgent corrige escopo limitado
7. Voltar para passo 2 (reexecutar)
8. Limite de ciclos (ex: 3) → escalar para humano se nao convergir
```

### Regras do loop

- **Validator nao corrige** — apenas veredicto binario (passou / nao passou) + motivo
- **FixAgent nao valida** — apenas corrige o erro apontado, sem expandir escopo
- **Orchestrator decide** — retry, correcao ou escalacao para humano
- **Limite de ciclos obrigatorio** — loop infinito e falha silenciosa

### Implementacao minima

```python
MAX_CICLOS = 3

for ciclo in range(MAX_CICLOS):
    resultado = builder.executar(tarefa)
    validacao = validator.verificar(resultado, criterios)
    if validacao.passou:
        return resultado
    if ciclo < MAX_CICLOS - 1:
        fix_agent.corrigir(validacao.erro, escopo=tarefa.escopo)
    else:
        raise RuntimeError(f"Nao convergiu em {MAX_CICLOS} ciclos: {validacao.erro}")
```

### Relacao com sensores externos

O Validator nao deve julgar por texto — deve rodar sensores:

```
pytest → passou/falhou (binario)
Pydantic → valido/invalido (binario)
linter → 0 erros / N erros (numerico)
```

"Parece bom" nao e criterio. Sensor externo retorna 0 ou 1 — isso e o gate.

Fonte: VIDEO1_HARNESS.md — "O que forca nao e a instrucao. O que forca sao os sensores — coisas externas, linters, test runners — porque o agente nao deve ser quem julga."

---

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
