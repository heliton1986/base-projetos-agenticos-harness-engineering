# Frontend Observavel para Agentes

## Objetivo

Este documento define um padrao para tornar sistemas agenticos observaveis no frontend.

A inspiracao principal vem da ideia de mostrar ao usuario, no proprio front, o andamento dos agentes e subagentes sem expor ruido tecnico desnecessario.

## Por que isso importa

Em sistemas agenticos, o usuario muitas vezes nao quer apenas a resposta final.

Ele tambem precisa de:

- confianca
- previsibilidade
- sensacao de progresso
- visibilidade do que esta acontecendo
- capacidade de entender por que algo ainda nao terminou

Um frontend observavel ajuda a transformar um sistema agentico de "caixa preta" em um fluxo inteligivel.

## O que significa frontend observavel

Significa que a interface consegue expor, de forma controlada:

- qual etapa esta em execucao
- quais agentes ou subagentes estao trabalhando
- o que ja foi concluido
- o que esta aguardando
- se houve falha ou correcao
- quando o sistema esta validando
- quando o resultado final esta pronto

## O que mostrar no frontend

### Minimo viavel

- status geral da execucao
- etapa atual
- percentual ou contagem de progresso
- resultado final

### Recomendado

- lista de etapas
- status por etapa
- agente ou subagente responsavel
- mensagens curtas de progresso
- erros resumidos
- indicacao de validacao

### Mais avancado

- artefatos intermediarios relevantes
- retries
- handoffs entre agentes
- resumo do que cada agente produziu
- modo tecnico vs modo executivo

## Estados minimos recomendados

Os estados mais uteis para uma UI agentica sao:

- `aguardando`
- `executando`
- `concluido`
- `falhou`
- `em correcao`
- `validando`
- `validado`

Esses estados ja cobrem boa parte dos fluxos reais.

## Componentes visuais recomendados

### 1. Barra ou lista de etapas

Exibe:

- nome da etapa
- ordem
- status
- progresso atual

Exemplos:

- entender pedido
- buscar dados
- analisar
- sintetizar
- validar
- entregar

### 2. Painel de subagentes

Exibe:

- nome do subagente
- papel
- status atual
- output resumido

Exemplo:

- `SQLAgent` -> concluido
- `SemanticAgent` -> executando
- `ValidatorAgent` -> aguardando

### 3. Bloco de resultado parcial

Mostra resultados intermediarios que ajudam sem gerar excesso de ruido.

Exemplos:

- quantidade de registros encontrados
- tema dominante nas reclamacoes
- score de validacao
- resumo parcial de achados

### 4. Bloco de validacao

Mostra se o sistema:

- esta validando
- passou nos checks minimos
- falhou em algum gate
- entrou em correcao

## O que nao mostrar por padrao

Nem todo detalhe interno precisa aparecer na interface.

Evite mostrar por padrao:

- prompts completos internos
- todos os tool calls crus
- stack traces longos para usuario final
- logs verbosos
- ruido tecnico sem valor de explicacao

A regra e:

`mostrar o suficiente para gerar confianca e entendimento, mas nao tanto a ponto de virar ruido.`

## Modos de visualizacao

Uma boa estrategia e pensar em tres modos possiveis.

### 1. Modo usuario final

Mostrar:

- progresso resumido
- etapa atual
- resultado final
- erros simples e amigaveis

### 2. Modo executivo

Mostrar:

- fluxo resumido
- tempo total
- confianca da resposta
- validacao final
- resumo de agentes envolvidos

### 3. Modo tecnico

Mostrar:

- subagentes
- handoffs
- validacoes
- retries
- outputs intermediarios relevantes
- detalhes de execucao

## Handoff no frontend

Quando houver handoff entre agentes, a UI pode mostrar isso como transicao de etapa.

Exemplos:

- `Orchestrator -> SQLAgent`
- `SQLAgent -> SynthesisAgent`
- `SynthesisAgent -> ValidatorAgent`

Mas isso deve ser exibido de forma legivel e resumida.

## Validacao no frontend

Uma das partes mais importantes do frontend observavel e tornar a validacao visivel.

Exemplos do que mostrar:

- `Validando resposta...`
- `Checks minimos aprovados`
- `Falha de validacao: resposta sem evidencia suficiente`
- `Em correcao antes de prosseguir`

Isso ajuda a alinhar UI com a logica de harness forte.

## Quando isso faz mais sentido

Esse padrao faz mais sentido quando:

- o fluxo leva mais que poucos segundos
- ha varias etapas
- ha subagentes
- existe validacao intermediaria
- o sistema faz analise ou execucao em cadeia
- o usuario ganha confianca ao ver o progresso

## Quando pode ser exagero

Pode ser exagero quando:

- a tarefa e simples demais
- a resposta e quase imediata
- nao ha beneficios reais em expor etapas
- a UI ficaria mais confusa do que util

Nesses casos, uma UI mais simples pode ser melhor.

## Estrutura de tela sugerida

Uma estrutura simples e forte pode ser:

```text
[ Entrada do usuario ]
[ Resumo do pedido ]

[ Painel principal ]
- status geral
- etapa atual
- mensagens resumidas

[ Barra lateral ou painel secundario ]
- lista de subagentes
- status por subagente
- outputs resumidos

[ Bloco de validacao ]
- validando / aprovado / falhou

[ Resultado final ]
- resposta consolidada
```

## Relacao com Harness Engineering

Frontend observavel nao e apenas UX bonita.

Ele tambem ajuda a materializar no produto algumas ideias centrais de harness:

- progresso por fase
- gates de validacao
- orquestracao entre agentes
- retries e correcoes
- separacao entre execucao e aprovacao

## Recomendacao pratica

Se o sistema for multi-agent ou tiver fluxo mais longo, vale considerar pelo menos:

- status geral
- etapas
- validacao
- subagentes principais

Isso ja entrega muito valor.

## Conclusao

Frontend observavel e a traducao visual de um sistema agentico bem orquestrado.

Em uma frase:

`Se o harness organiza o trabalho dos agentes por dentro, o frontend observavel torna esse trabalho compreensivel por fora.`


## Modelos e agentes no frontend

Quando o sistema usar orquestrador e subagentes com modelos diferentes, o frontend tecnico pode exibir tambem:

- agente atual
- papel do agente
- modelo usado
- provider, quando relevante
- status da etapa
- retries
- validacao

Em modo usuario final, esses detalhes podem ser reduzidos para nao poluir a interface.
