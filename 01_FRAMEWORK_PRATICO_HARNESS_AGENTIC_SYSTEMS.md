# Framework Pratico: Harness Engineering para Sistemas Agenticos

## Objetivo

Este documento sintetiza o melhor dos dois videos analisados sobre `Harness Engineering` e transforma esses conceitos em um framework pratico para construir sistemas agenticos reais.

A ideia central e combinar:

- o lado de `runtime, handoff e orquestracao`
- com o lado de `confiabilidade, validacao e autocorrecao`

## A sintese dos dois videos

Se eu resumisse o melhor dos dois videos em uma frase:

`Um sistema agentico bom nao depende apenas de um modelo inteligente; ele depende de um ambiente operacional que saiba orientar, dividir, observar, validar e corrigir o trabalho do agente.`

### O que o Video 1 traz de mais valioso

- `Spec-Driven Development`
- memoria operacional
- sensores externos
- separacao entre implementador e validador
- loop de correcoes
- foco em confiabilidade

### O que o Video 2 traz de mais valioso

- `runtime` do harness
- loop de `tool_use` e `tool_result`
- `Task tool` como mecanismo de handoff
- subagentes com contexto isolado
- `tool scoping`
- gerenciamento de `token budget`
- progresso visivel no front

## O framework recomendado

## 1. Comece por especificacao

Antes de qualquer agente rodar, defina:

- objetivo
- escopo
- restricoes
- output esperado
- arquivos ou sistemas que podem ser alterados
- criterios de pronto
- validacoes obrigatorias

Sem isso, o agente tende a improvisar.

## 2. Tenha um agente orquestrador

O sistema deve ter um `orchestrator` principal que:

- recebe o pedido do usuario
- interpreta a intencao
- quebra o problema em etapas
- decide quais subagentes invocar
- consolida a resposta final

Esse agente nao deveria tentar fazer tudo sozinho.

## 3. Use subagentes especializados

Cada subagente deve ter:

- papel claro
- objetivo restrito
- prompt autocontido
- ferramentas limitadas
- output esperado

Isso reduz confusao e melhora a previsibilidade.

## 4. Faça handoff por contrato

Quando um agente chamar outro, o handoff deve carregar:

- contexto suficiente
- objetivo da tarefa
- criterios de sucesso
- formato do retorno

O prompt do subagente deve ser `self-contained`.

## 5. Isole o contexto

O parent nao deve carregar todo o contexto de todos os filhos.

Idealmente:

- o subagente roda com contexto proprio
- faz seus `tool_calls` internamente
- retorna apenas a sintese ou artefato final

Isso economiza tokens e evita poluicao de contexto.

## 6. Limite as tools por agente

Cada agente deve receber apenas o conjunto minimo de ferramentas que precisa.

Exemplo:

- `SQLAgent`: SQL e leitura de schema
- `SemanticAgent`: busca vetorial
- `ApiAgent`: chamadas HTTP ou MCP externo
- `ValidatorAgent`: testes, lint, typecheck, evals

Isso e uma forma de `defesa em profundidade`.

## 7. Separe quem constrói de quem valida

Uma das melhores ideias do primeiro video é nao deixar o mesmo agente:

- implementar
- se autoavaliar
- declarar a tarefa como pronta

O fluxo ideal tem pelo menos:

- `Builder`
- `Validator`
- `Orchestrator`

O `Builder` produz.
O `Validator` verifica.
O `Orchestrator` decide aprovar ou pedir correcao.

## 8. Use sensores externos

O julgamento do sistema nao pode depender apenas do texto do agente.

Sensores uteis:

- testes unitarios
- testes de integracao
- lint
- typecheck
- evals de qualidade
- traces
- verificadores de contrato

Em harness forte, "parece bom" nao é suficiente.

## 9. Tenha loop de correcao

O sistema deve funcionar como um ciclo:

1. planejar
2. executar
3. validar
4. falhou -> corrigir
5. validar novamente
6. aprovar

Esse loop é o coracao do sistema confiavel.

## 10. Guarde memoria operacional

Crie artefatos persistentes com:

- estado atual
- backlog imediato
- o que foi concluido
- o que falhou
- decisoes arquiteturais
- proximos passos

Sem isso, cada nova sessao recomeça do zero.

## 11. Mostre progresso no front

Um sistema agentico real ganha muito quando o usuario consegue ver:

- etapa atual
- subagentes em execucao
- tarefas concluidas
- tarefas aguardando
- artefatos intermediarios
- falhas e retries

Isso melhora:

- confianca
- depuracao
- UX
- capacidade de auditoria

## Arquitetura recomendada

Uma arquitetura minima de `Harness Engineering` para sistemas agenticos poderia ser:

### Camada 1: Entrada e orquestracao

- `User Request`
- `OrchestratorAgent`
- parser de intencao
- planner
- dispatcher de subagentes

### Camada 2: Especializacao

- `ResearchAgent`
- `ExecutionAgent`
- `AnalysisAgent`
- `SynthesisAgent`
- `ValidatorAgent`

### Camada 3: Runtime do harness

- registry de tools
- controle de contexto
- `task handoff`
- memoria operacional
- sensores
- retry loop

### Camada 4: Observabilidade

- traces
- logs
- evals
- status das tarefas
- dashboard ou interface visual

## Exemplo real

## Caso: Assistente de operacoes para e-commerce

Pergunta do usuario:

`Quais problemas mais afetam clientes premium do Sudeste e o que devemos fazer nas proximas 2 semanas?`

### Como o sistema funcionaria

#### 1. OrchestratorAgent

Responsabilidades:

- interpreta a pergunta
- detecta que e uma pergunta hibrida
- cria plano de execucao

Plano:

- buscar dados estruturados de receita, segmento e regiao
- buscar reclamacoes semanticas
- cruzar os dois
- gerar recomendacoes
- validar a resposta

#### 2. SQLAgent

Responsabilidades:

- consultar `Postgres`
- responder:
  - clientes premium do Sudeste
  - faturamento
  - volume de pedidos
  - ticket medio

Output:

- tabela ou JSON estruturado com numeros exatos

#### 3. SemanticAgent

Responsabilidades:

- consultar `Qdrant`
- encontrar temas recorrentes nas reclamacoes
- identificar sentimento dominante

Output:

- resumo de temas
- exemplos de evidencias
- frequencia relativa

#### 4. SynthesisAgent

Responsabilidades:

- combinar dados do SQL com semantica
- produzir uma resposta executiva
- montar um plano de acao

Output:

- resumo executivo
- 3 principais problemas
- acoes recomendadas para 2 semanas

#### 5. ValidatorAgent

Responsabilidades:

- verificar se a resposta:
  - usou os dois stores quando necessario
  - contem evidencias
  - contem numeros concretos
  - nao contradiz os dados
  - passa os evals minimos

Se falhar:

- devolve para correcao

#### 6. Frontend

O front pode mostrar:

- `01 entender pedido`
- `02 buscar dados SQL`
- `03 buscar evidencias semanticas`
- `04 sintetizar resposta`
- `05 validar`
- `06 corrigir, se necessario`
- `07 entregar resultado`

Esse padrao bate muito com as imagens do `Harness de Receitas`.

## Exemplo de papéis e tools

### OrchestratorAgent

- tools:
  - `Task`
  - `progress_store`
  - `result_aggregator`

### SQLAgent

- tools:
  - `execute_sql`

### SemanticAgent

- tools:
  - `semantic_search`

### SynthesisAgent

- tools:
  - nenhuma ou apenas leitura de artefatos

### ValidatorAgent

- tools:
  - `run_tests`
  - `run_evals`
  - `check_contract`

## Checklist de implementacao

## Base minima

- definir o papel do `OrchestratorAgent`
- definir subagentes especializados
- documentar handoffs
- criar prompts autocontidos
- limitar tools por agente

## Confiabilidade

- criar contratos de tarefa
- criar checklist de validacao
- separar `builder` e `validator`
- adicionar retry loop
- registrar falhas por rodada

## Contexto e memoria

- definir o que sobe para o contexto do parent
- salvar progresso em arquivo ou store
- guardar decisoes importantes
- manter backlog imediato

## UX e observabilidade

- expor status por subagente
- mostrar etapa atual
- registrar traces
- guardar resultados intermediarios
- mostrar motivo de falha e reexecucao

## O erro mais comum a evitar

O erro mais comum e tentar fazer tudo com:

- um unico agente
- contexto enorme
- todas as tools liberadas
- sem validacao independente
- sem memoria de progresso

Isso ate pode funcionar em demo curta, mas degrada muito rapido em fluxos reais.

## Formula curta para projeto real

Uma formula pratica seria:

`Spec -> Orchestrator -> Subagents especializados -> Tool scoping -> Sensores externos -> Validator -> Retry loop -> UI de progresso`

## Conclusao

O melhor dos dois videos, usado junto, aponta para este principio:

`Sistemas agenticos reais nao devem ser tratados como um prompt grande, mas como um sistema operacional de colaboracao entre agentes, tools, contexto, validacao e memoria.`

Em uma frase:

`O Video 2 ensina como os agentes trabalham. O Video 1 ensina como fazer esse trabalho ser confiavel.`
