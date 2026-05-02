# Protocolo de Execucao Agentica

## Objetivo

Este documento define como a LLM deve se comportar quando o usuario pedir a execucao de um fluxo operacional do projeto, por exemplo:

- `@run_onboarding_flow.py`
- `rode o onboarding`
- `execute a primeira capacidade`
- `rode a validacao`

A ideia nao e apenas ter scripts.
A ideia e definir o comportamento esperado da LLM em torno desses scripts.

## Principio central

Quando houver um fluxo executavel e validavel, a LLM deve agir como um operador assistido do sistema.

Isso significa:

1. executar o fluxo pedido
2. observar resultado e erros
3. tentar corrigir problemas locais e de baixo risco
4. reexecutar
5. validar
6. reportar progresso no chat
7. parar apenas quando:
   - o fluxo estiver aprovado
   - ou houver bloqueio real

## Disparadores

Quando o usuario pedir algo como:

- `@run_onboarding_flow.py`
- `rode o sistema`
- `execute o fluxo inicial`
- `rode a primeira capacidade`
- `valide e corrija`

A LLM deve interpretar isso como um pedido de execucao agentica e nao apenas como uma sugestao de comando.

## Loop do Agente: Perception → Reasoning → Action → Memory

Um agente real nao executa um script — percebe, raciocina, age e lembra, em loop. Cada iteracao refina a resposta com base no que foi armazenado.

| Fase | O que acontece |
|------|---------------|
| **Perception** | Recebe input e interpreta intencao — qual pergunta, qual contexto, qual objetivo |
| **Reasoning** | Analisa e decide o proximo passo — qual tool, qual fonte, qual estrategia |
| **Action** | Executa a decisao — SQL (exato/estruturado) ou busca semantica (Qdrant/vetor) |
| **Memory** | Armazena contexto para proximas decisoes — o que foi aprendido nesta iteracao alimenta a proxima |

Memory ativa e o que diferencia agente de script: o resultado de cada iteracao alimenta a proxima decisao.

## Loop ReAct

Este protocolo implementa o padrao **ReAct** (Reasoning + Acting), fundamento academico de agentes que intercalam raciocinio e acao.

As quatro fases do loop:

1. **Think** — raciocinar antes de agir; entender o estado atual, identificar o proximo passo
2. **Act** — executar a acao escolhida (script, tool call, correcao)
3. **Observe** — integrar o resultado; o que mudou, o que falhou, o que passou
4. **Iterate** — decidir: aprovado, corrigir e repetir, ou escalar

Cada decisao deve ser registrada (audit_log) para auditabilidade.

O loop termina quando: gate aprovado, ou bloqueio real que exige decisao humana.

Fonte: Yao et al. — ReAct: Synergizing Reasoning and Acting in Language Models (2022). arxiv.org/abs/2210.03629

Mapeamento entre os dois loops:

| Loop do Agente | ReAct |
|----------------|-------|
| Perception | Observe (entrada inicial) |
| Reasoning | Think |
| Action | Act |
| Memory | Observe + armazenamento persistente |

## Loop esperado

O fluxo padrao deve ser:

1. executar o comando ou script principal
2. capturar saida relevante
3. verificar se houve erro
4. se o erro for local, corrigivel e de baixo risco:
   - corrigir
   - reexecutar
5. rodar validacao associada
6. registrar status
7. informar no chat:
   - o que foi executado
   - o que falhou
   - o que foi corrigido
   - o estado atual

## O que pode ser corrigido automaticamente

A LLM pode tentar corrigir automaticamente quando o problema for:

- import quebrado
- path incorreto
- referencia de arquivo faltando por erro de scaffold
- ajuste de script local
- erro simples de validacao estrutural
- artefato esperado nao gerado por problema local de codigo

## O que nao deve ser corrigido silenciosamente

A LLM nao deve seguir automaticamente quando houver:

- ambiguidade de alto risco
- regra financeira ou regulatoria indefinida
- necessidade de credenciais nao fornecidas
- dependencia externa indisponivel que muda a arquitetura
- risco de escrita indevida em fonte sensivel
- conflito real de escopo

Nesses casos, deve parar e perguntar objetivamente.

## Criterio de parada

A LLM deve parar quando ocorrer uma destas condicoes:

### 1. Sucesso

- o fluxo principal executou
- a validacao passou
- os gates minimos foram aprovados

### 2. Bloqueio real

- a proxima correcao exigiria decisao humana
- a falha depende de credenciais ou acesso externo
- ha risco sensivel demais para assumir

## Como reportar no chat

Ao operar um fluxo, narrar cada etapa com o seguinte padrao:

```
✓ Etapa 1 — NomeAgente: o que fez + resultado quantificado
✓ Etapa 2 — NomeAgente → modelo-llm: input → output
✗ Etapa 3 — NomeAgente: falhou — detalhe do erro
■ Gate final — ValidatorAgent: PASSED/FAILED em Xs
```

Regras:
- `✓` etapa concluida com sucesso
- `✗` etapa com falha — detalhar o erro e o que foi corrigido
- `■` gate ou resultado final

Quando chamada LLM ocorreu, sempre mostrar agente + modelo:

```
✓ DetectorAgent → claude-sonnet-4-6: 3 candidatos → 1 inconsistencia
```

Para dados estruturados (coverage, status por agente, erros encontrados): usar tabela markdown, nao lista.

Nunca omitir: nome do agente, modelo LLM usado, quantidade processada, status final.

## Relacao com o onboarding

Quando existir um `run_onboarding_flow.py`, a expectativa padrao e:

1. executar esse script primeiro
2. usar o resultado dele como ponto de verdade do onboarding
3. se ele falhar por erro local, tentar corrigir
4. se ele aprovar os gates, informar que API e frontend podem ser abertos

## Relacao com a base

Este protocolo complementa:

- `03_BOOTSTRAP_PROJETO_AGENTICO.md`
- `06_PADRAO_BUILDER_VALIDATOR_E_TASK_CONTRACTS.md`
- `09_TEMPLATES_PARA_BASE_HARNESS.md`
- `templates/TEMPLATE_ONBOARDING_FLOW.md`
- `prompts/PROMPTS_POR_FASE.md`
- `12_ORQUESTRADOR_E_SUBAGENTES_PARA_FLUXOS_DE_EXECUCAO.md`
- `13_OBSERVABILIDADE_DE_MODELOS_E_AGENTES.md`

## Regra de ouro

Quando o usuario pedir execucao, a LLM nao deve apenas dizer quais comandos existem.

Ela deve, quando possivel:

- executar
- observar
- corrigir
- reexecutar
- validar
- reportar

Em uma frase:

`Scripts sao o motor; este protocolo define como a LLM deve dirigir.`
