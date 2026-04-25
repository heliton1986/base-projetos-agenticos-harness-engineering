# Checklist para Gerar AGENTS.md

## Objetivo

Este documento serve como guia para gerar um `AGENTS.md` a partir da base conceitual de `Harness Engineering`.

Ele existe para responder uma pergunta simples:

`Quando um novo projeto começar, o que a LLM precisa ler e decidir para produzir um AGENTS.md realmente util?`

## Quando usar este checklist

Use este checklist quando:

- um novo projeto agentico for iniciado
- for necessario adaptar o harness para um dominio especifico
- for preciso transformar a base conceitual em instrucoes operacionais de projeto

Nao use este documento como substituto do `AGENTS.md` final.

## Arquivos que a LLM deve ler antes de gerar o AGENTS.md

A LLM deve ler, no minimo:

- `FRAMEWORK_PRATICO_HARNESS_AGENTIC_SYSTEMS.md`
- `DOE_OPERACIONAL_PARA_HARNESS.md`
- documentos de dominio do projeto
- arquitetura ou README do projeto
- constraints tecnicas do repositorio
- contratos, diretivas ou SOPs relevantes

Se existir, tambem deve ler:

- exemplos anteriores de `AGENTS.md`
- convencoes de pastas e scripts
- policy de validacao
- requirements de observabilidade

## O que a LLM deve extrair desses arquivos

Antes de escrever o `AGENTS.md`, a LLM deve identificar:

- qual e o objetivo do projeto
- qual problema o agente resolve
- qual o tipo de sistema agentico envolvido
- quais sao os limites de atuacao do agente
- quais ferramentas o agente pode usar
- quais entregaveis o projeto produz
- quais contratos minimos de dados precisam existir
- quais validacoes sao obrigatorias
- quais ambigudades podem ser assumidas com registro e quais exigem pergunta ao humano
- quais artefatos sao temporarios e quais sao permanentes
- quando usar subagentes
- quando escalar para validacao ou feedback humano

## O que deve variar por projeto

Estas partes do `AGENTS.md` devem ser adaptadas ao projeto concreto:

- objetivo do agente
- dominio de negocio
- stack tecnica
- tools permitidas
- comandos de execucao e validacao
- organizacao de diretorios
- restricoes de seguranca
- criterios de pronto
- policy de erro e retry
- regras de deploy ou publicacao

## O que pode permanecer fixo da base Harness

Estas partes tendem a permanecer parecidas entre projetos:

- separacao entre `Diretivas`, `Orquestracao` e `Execucao`
- principio de verificar ferramentas antes de criar novas
- principio de empurrar repeticao para execucao deterministica
- uso criterioso de subagentes
- necessidade de validacao externa
- preservacao de memoria operacional
- distincao entre entregaveis e intermediarios
- aprendizado continuo por atualizacao de diretivas

## Estrutura recomendada para o futuro AGENTS.md

A LLM deve tentar gerar um `AGENTS.md` com secoes curtas e operacionais, por exemplo:

### 1. Missao do agente

- o que o agente faz
- o que ele nao faz
- qual resultado ele deve maximizar

### 2. Modelo operacional

- funcionamento em `Diretivas`, `Orquestracao` e `Execucao`
- regra geral de tomada de decisao

### 3. Ferramentas e escopo

- tools permitidas
- tools proibidas ou restritas
- quando usar cada uma

### 4. Subagentes

- quando chamar
- que tipo de tarefa delegar
- formato de handoff

### 5. Validacao

- quais checks sao obrigatorios
- o que significa pronto
- quando pedir correcao

### 6. Memoria e artefatos

- onde registrar progresso
- como tratar temporarios
- como tratar entregaveis finais

### 7. Politica de erro

- como reagir quando algo quebra
- quando reexecutar
- quando escalar para humano

## Perguntas que a LLM deve responder antes de concluir o AGENTS.md

Antes de finalizar o arquivo, a LLM deve responder internamente:

- este agente esta acoplado ao dominio real do projeto?
- as tools listadas sao de fato as certas?
- os comandos de validacao fazem sentido para essa stack?
- as regras de erro estao claras?
- os limites de autonomia estao explicitos?
- o documento esta operacional ou esta abstrato demais?

## Sinais de um AGENTS.md ruim

Um `AGENTS.md` provavelmente esta ruim quando:

- esta generico demais
- nao menciona a stack real
- nao deixa claro o que o agente pode tocar
- nao diz como validar o resultado
- nao diferencia artefatos temporarios de finais
- nao diz quando usar subagentes
- parece apenas um manifesto conceitual

## Sinais de um AGENTS.md bom

Um `AGENTS.md` provavelmente esta bom quando:

- e curto, claro e prescritivo
- conversa com a arquitetura real do projeto
- deixa claro o fluxo de trabalho do agente
- limita o espaco de acao de forma inteligente
- define validacao minima obrigatoria
- pode ser usado em runtime sem ambiguidade excessiva

## Fluxo recomendado de geracao

1. Ler os documentos obrigatorios da base (nucleo + obrigatorios)
2. Ler `.claude/kb/` — quick-references de doe, builder-validator, execution-protocol, model-routing, agent-contracts
3. Ler o contexto do projeto
4. Extrair restricoes e objetivos
5. Definir o modelo operacional DOE do agente
6. Definir tools, subagentes, estrategia de modelos e validacoes
7. **Usar `TEMPLATE_AGENTS.md` como base** — nao gerar do zero
8. Revisar se o documento esta especifico o suficiente
9. Ajustar para o dominio do projeto

## Checklist de artefatos antes de qualquer implementacao

Antes de escrever qualquer codigo, verificar:

### Bootstrap (obrigatorio no dia 1)
- [ ] `README.md` gerado a partir de `TEMPLATE_README.md`
- [ ] `AGENTS.md` gerado a partir de `TEMPLATE_AGENTS.md`
- [ ] `spec/01-brainstorm.md` gerado a partir de `TEMPLATE_SPEC_01_BRAINSTORM.md`
- [ ] `spec/02-define.md` gerado a partir de `TEMPLATE_SPEC_02_DEFINE.md`
- [ ] `spec/03-design.md` gerado a partir de `TEMPLATE_SPEC_03_DESIGN.md`
- [ ] `.env.example` criado com todas as variaveis necessarias
- [ ] `directives/` criado com domain.md e business-rules.md no minimo

### Antes de implementar primeira capacidade
- [ ] `TEMPLATE_FIRST_INCREMENTAL_CAPABILITY.md` preenchido — menor entrega verificavel definida
- [ ] `TEMPLATE_TASK_CONTRACT.md` preenchido por agente
- [ ] `TEMPLATE_IMPLEMENTATION_PHASE.md` preenchido para fase 1
- [ ] `TEMPLATE_DATA_CONTRACT.md` preenchido se ha dados sensiveis ou multiplas fontes
- [ ] `TEMPLATE_MODEL_ROUTING.md` preenchido — modelo definido por agente antes de codar
- [ ] `spec/05-validate.md` criado com Gate 1 definido

### Antes de subir qualquer agente
- [ ] `TEMPLATE_ONBOARDING_FLOW.md` preenchido
- [ ] `execution/run_onboarding_flow.py` criado
- [ ] Gate 1 passa sem erro

### Durante e entre sessoes
- [ ] `TEMPLATE_PROGRESS.md` atualizado a cada sessao
- [ ] `TEMPLATE_VALIDATION_STATUS.md` atualizado por gate aprovado

## Checklist de qualidade do AGENTS.md gerado

- [ ] Usa `TEMPLATE_AGENTS.md` como estrutura base
- [ ] Menciona modelo operacional DOE explicito
- [ ] Lista agentes com responsabilidade, entrada, saida e uso de LLM
- [ ] Define protocolo de execucao (loop obrigatorio)
- [ ] Lista restricoes que nunca podem ser violadas
- [ ] Define gates de aprovacao com comandos executaveis
- [ ] Define estrategia de modelos por agente
- [ ] Lista arquivos criticos a ler antes de modificar codigo
- [ ] E especifico para o dominio — nao generico

## Conclusao

Este checklist existe para evitar dois erros comuns:

- gerar um `AGENTS.md` abstrato demais para ser util
- gerar um `AGENTS.md` especifico demais sem base conceitual consistente

Em uma frase:

`O AGENTS.md deve nascer do encontro entre a base Harness e a realidade concreta do projeto — sempre a partir do template, nunca do zero.`
