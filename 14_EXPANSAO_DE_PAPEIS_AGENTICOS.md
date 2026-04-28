# Expansao de Papeis Agenticos

## Objetivo

Explicar como criar novos tipos de agentes na base sem perder clareza, handoff, validacao e estrategia de modelos.

## Principio central

A base nao trabalha com um catalogo fechado de agentes.

Ela trabalha com:

- papeis tipicos
- responsabilidades claras
- handoffs explicitos
- modelos por papel
- observabilidade por papel

## Papeis tipicos da base

A base ja usa com frequencia:

- `Orchestrator`
- `Planner`
- `ExecutionAgent`
- `Validator`
- `Reporter`
- `FrontendStatusAgent`
- `IngestionAgent`
- `ReconciliationAgent`
- `FixAgent`

## Quando criar um novo papel

Crie um novo papel quando houver:

- responsabilidade claramente distinta
- ganho real de isolamento de contexto
- necessidade de validacao separada
- necessidade de handoff mais auditavel
- beneficio claro de custo, latencia ou especializacao

## Quando nao criar um novo papel

Nao crie um novo papel apenas porque:

- parece elegante ter mais agentes
- o mesmo agente ainda consegue operar com clareza
- nao ha diferenca real de responsabilidade

## Perguntas para decidir

Antes de criar um novo agente, responda:

- qual problema ele resolve que outro papel nao resolve bem?
- qual seria o handoff de entrada e saida?
- esse papel precisa de modelo diferente?
- esse papel precisa de validacao propria?
- ele reduz ou aumenta a complexidade do sistema?

## Estrutura minima para um novo papel

Ao adicionar um novo agente, documente pelo menos:

- nome do papel
- objetivo
- escopo
- handoff de entrada
- handoff de saida
- ferramentas permitidas
- estrategia de modelo
- validacao minima
- o que deve ser observavel no chat/frontend

## Exemplo 1 - AuditAgent

Use quando:

- o projeto precisa reforcar trilha de auditoria
- o dominio e sensivel

Documente:

- entrada: artefatos gerados pela etapa anterior
- saida: resumo de auditoria e conformidade
- modelo: medio ou robusto

## Exemplo 2 - ResearchAgent

Use quando:

- o sistema precisa buscar contexto externo ou interno
- a tarefa de pesquisa e diferente da tarefa de execucao

Documente:

- entrada: pergunta de pesquisa
- saida: achados estruturados
- modelo: medio

## Exemplo 3 - ComplianceAgent

Use quando:

- ha regras regulatórias ou politicas de conformidade mais especificas

Documente:

- entrada: artefato ou decisao a revisar
- saida: parecer de conformidade
- modelo: robusto quando o risco for alto

## Relacao com modelos

Sempre que um novo papel for criado, vale responder:

- ele e `robusto`, `medio` ou `economico`?
- precisa de modelo proprio ou pode reutilizar o de outro papel?

Consulte tambem:

- `10_ESTRATEGIA_DE_MODELOS_PARA_AGENTES.md`
- `13_OBSERVABILIDADE_DE_MODELOS_E_AGENTES.md`
- `templates/TEMPLATE_MODEL_ROUTING.md`

## Relacao com observabilidade

Todo novo papel deve poder aparecer, quando fizer sentido, em:

- chat tecnico
- frontend observavel tecnico
- logs e status do runtime

## Conclusao

A base nao limita o numero de agentes.
Ela limita a criacao irresponsavel de papeis sem necessidade.

Em uma frase:

`Novos agentes sao bem-vindos quando trazem especializacao real, e nao apenas ornamentacao arquitetural.`

## Referencias

Os padroes descritos aqui sao agnósticos de modelo e provedor. As fontes abaixo sustentam os criterios de criacao e especializacao de papeis agenticos.

- **Anthropic — Building effective agents** (2024): discute quando usar agente unico vs multi-agent, e os criterios de especializacao de subagentes por responsabilidade. Base direta para as perguntas de decisao deste documento.
  Disponivel em: https://www.anthropic.com/research/building-effective-agents

- **Anthropic — Model Context Protocol** (2024): define como agentes com ferramentas (tool use) devem ser especificados, com escopo, inputs e outputs claros — alinhado ao checklist de estrutura minima para novo papel descrito aqui.
  Disponivel em: https://modelcontextprotocol.io/introduction

- **Chase — Cognitive Architectures for Language Agents** (2023): taxonomia de papeis agenticos (planner, executor, critic, memory) com criterios de quando separar responsabilidades em agentes distintos.
  Disponivel em: https://arxiv.org/abs/2309.02427
