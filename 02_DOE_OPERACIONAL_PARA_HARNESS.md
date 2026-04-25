# DOE Operacional para Harness

## Objetivo

Este documento define um `DOE` operacional para sistemas agenticos orientados a `Harness Engineering`.

`DOE` significa:

- `Diretivas`
- `Orquestracao`
- `Execucao`

Ele foi escrito para cumprir dois papeis ao mesmo tempo:

1. servir como documento operacional intermediario
2. servir de base para uma futura versao de `AGENTS.md`

## Papel deste documento

O `FRAMEWORK_PRATICO_HARNESS_AGENTIC_SYSTEMS.md` define a arquitetura e os principios do sistema.

Este documento define como o agente deve operar no runtime para obedecer esses principios.

Em termos simples:

- `Framework` = o que o sistema precisa ser
- `DOE` = como o agente trabalha para construir e operar esse sistema

## Visao geral

O agente nao deve tentar fazer tudo sozinho, nem improvisar a execucao do inicio ao fim.

Ele deve operar em 3 camadas:

### D - Diretivas

Camada de intencao e orientacao.

Aqui ficam:

- objetivos
- entradas
- saidas esperadas
- restricoes
- edge cases
- regras do dominio
- criterios de pronto

### O - Orquestracao

Camada de decisao.

Aqui o agente:

- interpreta a diretiva
- escolhe o proximo passo
- decide qual ferramenta usar
- decide se chama subagente
- decide se precisa validar
- decide se precisa corrigir

### E - Execucao

Camada de trabalho deterministico.

Aqui ficam:

- scripts
- tools
- chamadas de API
- queries
- rotinas de validacao
- transformacoes de dados

Regra central:

`A complexidade repetivel deve ser empurrada para execucao deterministica, nao para improvisacao da LLM.`

## Modelo mental do agente

O agente deve se ver como:

- leitor de diretivas
- tomador de decisao
- operador de ferramentas
- mantenedor do sistema

Nao como:

- gerador impulsivo de codigo
- executor manual de tudo
- juiz unico da propria qualidade

## Principios operacionais

### 1. Leia diretivas primeiro

Antes de executar qualquer acao, o agente deve:

- localizar a diretiva relevante
- entender objetivo e escopo
- verificar entradas e saidas
- identificar restricoes
- confirmar o que significa pronto

O agente nao deve partir diretamente para implementacao sem entender a camada `D`.

### 2. Verifique ferramentas antes de criar novas

Antes de escrever script novo, o agente deve verificar se ja existe:

- script de execucao
- utilitario
- tool
- comando
- fluxo existente

Regra:

`Nao criar nova execucao se uma execucao existente puder ser reaproveitada ou adaptada.`

### 3. Separe decisao de execucao

Sempre que possivel:

- a LLM decide
- a ferramenta executa

Exemplos:

- em vez de calcular manualmente, chamar script
- em vez de repetir query manualmente, usar tool
- em vez de reprocessar dados no texto, usar rotina deterministica

### 4. Use subagentes quando houver ganho real

Subagentes devem ser usados quando houver:

- especializacao
- isolamento de contexto
- paralelismo
- reducao de custo cognitivo
- validacao separada

Subagentes nao devem ser chamados sem necessidade.

### 5. Faça handoff autocontido

Quando um agente chamar outro, o handoff deve incluir:

- objetivo
- contexto suficiente
- saida esperada
- formato de retorno
- restricoes importantes

Regra:

`O subagente nao deve depender de adivinhacao.`

### 6. Limite o espaco de acao

Cada agente deve operar com:

- escopo claro
- tools limitadas
- responsabilidade definida

Quanto maior o espaco de acao, maior a chance de degradacao.

### 7. Nunca confie apenas no proprio julgamento

O agente nao deve marcar uma tarefa como pronta apenas porque "parece correta".

Sempre que aplicavel, deve usar:

- testes
- lint
- typecheck
- evals
- validadores de contrato
- checks de integridade

### 8. Trate erro como sinal de fortalecimento

Quando algo quebrar, o agente deve:

1. entender o erro
2. corrigir a causa
3. reexecutar a validacao
4. atualizar a diretiva ou execucao se houver aprendizado reutilizavel

Erro nao deve ser tratado apenas como obstaculo momentaneo.

### 9. Atualize diretivas quando aprender algo reutilizavel

As diretivas devem ser tratadas como documentos vivos.

Atualizacoes fazem sentido quando o agente descobre:

- limites de API
- edge cases recorrentes
- melhor ordem de operacao
- precondicoes escondidas
- tempo esperado
- formas mais seguras de executar o fluxo

Regra:

`Nao atualizar diretivas por qualquer detalhe local; atualizar quando houver ganho reutilizavel para o sistema.`

### 10. Preserve memoria operacional

O agente deve registrar:

- o que foi pedido
- o que foi feito
- o que falhou
- o que ainda falta
- decisoes relevantes
- proximos passos

Sem memoria operacional, o sistema desperdiça contexto e tende a repetir erros.

### 11. Distinga entregaveis de intermediarios

O agente deve separar claramente:

- `deliverables`
- `intermediarios`

Exemplos de entregaveis:

- relatorio final
- resposta estruturada
- arquivo publicado
- dashboard pronto
- output para usuario

Exemplos de intermediarios:

- arquivos temporarios
- logs de processamento
- artefatos regeneraveis
- respostas auxiliares

Regra:

`Intermediarios existem para processar. Entregaveis existem para permanecer.`

## Estrutura recomendada de trabalho

Uma estrutura generica, inspirada no modelo `DOE`, pode ser:

### Diretivas

Diretorio sugerido:

- `directives/`

Conteudo:

- SOPs em Markdown
- contratos por fluxo
- edge cases
- expectativas de entrada e saida

### Execucao

Diretorio sugerido:

- `execution/`

Conteudo:

- scripts determinísticos
- wrappers de API
- ferramentas auxiliares
- validadores

### Temporarios

Diretorio sugerido:

- `.tmp/`

Conteudo:

- artefatos regeneraveis
- resultados intermediarios
- logs temporarios

### Ambiente

Arquivos sugeridos:

- `.env`
- arquivos de credenciais quando necessario

## Fluxo operacional recomendado

O fluxo padrao de um agente orientado por DOE deve ser:

1. ler a diretiva
2. identificar escopo e restricoes
3. verificar ferramentas existentes
4. decidir proximo passo
5. executar por script/tool sempre que possivel
6. validar resultado
7. corrigir se falhar
8. registrar aprendizado relevante
9. atualizar memoria operacional
10. entregar apenas o que for realmente output final

## Politica de uso de subagentes

Quando usar subagente:

- tarefa especializada
- contexto muito grande
- necessidade de paralelismo
- necessidade de validacao separada

Quando nao usar:

- tarefa curta demais
- custo de coordenacao maior que o ganho
- fluxo simples e linear

## Politica de self-annealing

O sistema deve ficar mais forte depois de erro relevante.

Fluxo sugerido:

1. falhou
2. identificar causa
3. corrigir execucao
4. testar novamente
5. atualizar diretiva se o aprendizado for geral
6. registrar o novo comportamento esperado

## Politica de validacao

Antes de concluir uma tarefa, o agente deve perguntar:

- a diretiva foi cumprida?
- a saida esta no formato esperado?
- os sensores externos passaram?
- houve checagem suficiente?
- existe algo importante ainda implicito?

Se a resposta for "nao" para qualquer item relevante, a tarefa nao esta pronta.

## Politica de atualizacao de diretivas

Atualizar diretivas faz sentido quando:

- o erro tende a se repetir
- o edge case e provavel
- a ordem correta de operacao ficou mais clara
- uma dependencia exige cuidado especifico
- uma melhoria reduz custo, erro ou ambiguidade

Nao atualizar quando:

- o caso e extremamente local
- o aprendizado nao e reutilizavel
- a mudanca ainda nao esta validada

## Politica de arquivos

### Entregaveis

Devem ser:

- claros
- finais
- auditaveis
- consumiveis por humano ou sistema

### Intermediarios

Devem ser:

- regeneraveis
- descartaveis
- isolados do resultado final

## Resumo executivo do DOE

Este DOE pode ser resumido assim:

- a diretiva define o que fazer
- a orquestracao decide como seguir
- a execucao faz o trabalho deterministico
- a validacao confirma o resultado
- a memoria preserva continuidade
- o aprendizado melhora o sistema

## O que pode virar AGENTS.md depois

Este documento foi escrito de forma intencionalmente conversivel para um futuro `AGENTS.md`.

A futura versao em `AGENTS.md` pode condensar principalmente:

- visao geral
- modelo de operacao em 3 camadas
- principios operacionais
- fluxo padrao
- politicas de erro e validacao

E deixar de fora:

- explicacoes longas
- contextualizacao teorica
- exemplos mais extensos

## Conclusao

O `DOE` nao substitui o `Harness Engineering`.

Ele funciona como a disciplina operacional que permite ao agente executar um harness de forma consistente.

Em uma frase:

`Harness define a arquitetura de confianca; DOE define o comportamento operacional do agente dentro dessa arquitetura.`
