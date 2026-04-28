# AGENTS.md — Base para Projetos Agenticos com Harness Engineering

## Papel deste arquivo

Define como a LLM deve se comportar ao trabalhar com esta base — seja criando um projeto novo, evoluindo um existente, ou atualizando artefatos da propria base.

Ler antes de qualquer acao.

## Identidade desta base

- **Tipo:** Base reutilizavel para projetos agenticos com Harness Engineering
- **Objetivo:** Reduzir improvisacao, aumentar consistencia e rastreabilidade em projetos agenticos com LLMs
- **Modelo operacional:** DOE (Diretivas + Orquestracao + Execucao)

## O que a LLM deve ler antes de agir

### Ao criar projeto novo

Obrigatorio, nesta ordem:

1. Este `AGENTS.md`
2. `.claude/kb/doe/quick-reference.md`
3. `.claude/kb/execution-protocol/quick-reference.md`
4. `.claude/kb/builder-validator/quick-reference.md`
5. `.claude/kb/model-routing/quick-reference.md`
6. `.claude/kb/agent-contracts/quick-reference.md`
7. `04_CHECKLIST_PARA_GERAR_AGENTS_MD.md` — seguir checklist item a item
8. `prompts/PROMPT_MESTRE_INICIAL.md`

### Ao evoluir projeto existente

1. Este `AGENTS.md`
2. KB relevante para o dominio da tarefa
3. `progress/PROGRESS.md` do projeto
4. Arquivos diretamente afetados pela tarefa

### Ao atualizar artefatos desta base

1. Este `AGENTS.md`
2. O `.md` que sera atualizado
3. A KB correspondente — atualizar junto se o `.md` mudar

## Protocolo de execucao (obrigatorio)

Sempre que houver fluxo executavel (script, pytest, gate, onboarding):

```
1. Executar
2. Capturar saida e erros
3. Erro local e baixo risco → corrigir → reexecutar
4. Validar
5. Reportar no chat: o que executou, falhou, corrigiu, estado atual
6. Parar apenas quando: gate aprovado OU bloqueio real
```

Nao pedir confirmacao a cada passo intermediario. Pedir apenas em bloqueio real.

**Bloqueio real:** ambiguidade de regra de negocio, credencial ausente, risco de escrita indevida, conflito de escopo.

## Protocolo narrativo no chat (obrigatorio)

Quando executar qualquer fase, gate ou agente — anunciar em texto no chat antes e depois de cada tool call.

Formato obrigatorio:

```
[Fase X — Nome]        iniciando...
[Gate X — Nome]        verificando...
*(executa tool)*
[Gate X — Nome]        APROVADO ✓
[AgenteX]              descricao do que fez
[Fase X — Nome]        CONCLUIDA ✓
```

Regras:
- Nunca executar tool call silenciosamente — sempre anunciar antes
- Sempre confirmar resultado depois (APROVADO / FALHOU / BLOQUEADO)
- Se falhou: informar o erro antes de corrigir
- Se bloqueio real: parar e explicar o que precisa de intervencao humana

Este protocolo garante visibilidade identica no chat e no terminal.
Ref: `templates/TEMPLATE_EXECUTION_RUNNER.md`

## Criacao de projeto novo — sequencia obrigatoria

```
1. Ler nucleo da base (01, 02, 03, 04) + KBs
2. Usar TEMPLATE_README.md → gerar README.md
3. Usar TEMPLATE_AGENTS.md → gerar AGENTS.md
4. Usar TEMPLATE_SPEC_01/02/03 → gerar spec/
5. Criar directives/ com domain.md e business-rules.md
6. Usar TEMPLATE_FIRST_INCREMENTAL_CAPABILITY.md → definir menor entrega
7. Usar TEMPLATE_TASK_CONTRACT.md → contrato por agente
8. Usar TEMPLATE_MODEL_ROUTING.md → modelo por agente antes de codar
9. Usar TEMPLATE_IMPLEMENTATION_PHASE.md → fase 1
10. Usar TEMPLATE_ONBOARDING_FLOW.md → execution/run_onboarding_flow.py
11. Implementar fase 1
12. Rodar Gate 1 — loop ate aprovado
13. So avancar para fase 2 com Gate 1 aprovado
```

Nunca pular etapas. Nunca gerar artefato sem o template correspondente.

**Velocidade de execucao:** executar cada fase completa sem pedir confirmacao a cada arquivo. A interacao com o humano acontece entre fases, nao entre arquivos. Perguntar apenas em bloqueio real.

## Regras que nunca podem ser violadas

1. **Nunca gerar artefato sem template** — README, AGENTS.md, spec, contratos: sempre a partir do template
2. **Nunca implementar tudo de uma vez** — primeira capacidade deve ser a menor entrega verificavel
3. **Nunca avancar sem gate aprovado** — gate e criterio de parada, nao sugestao
4. **Os `.md` da base sao fonte de verdade** — se KB e `.md` conflitarem, prevalece o `.md`
5. **Atualizar KB ao atualizar `.md`** — as duas fontes devem permanecer consistentes

## Estrutura da base

```
.md (01-15)           fonte de verdade — por que e quando aplicar cada padrao
templates/            moldes obrigatorios — como gerar cada artefato
.claude/kb/           padroes prontos — como aplicar agora sem reler tudo
prompts/              prompts reutilizaveis por fase
```

## Eixo interativo vs programatico

Esta base opera em dois eixos. A LLM deve saber em qual esta atuando.

**Interativo:** humano + LLM via interface (Claude Pro, Claude Code). Tarefas: editar base, ajustar prompts, revisar contratos, aprovar decisoes. Modelo: o disponivel para o humano via subscription.

**Programatico:** codigo chamando API sem intervencao humana. Tarefas: agentes executando fluxos, classificando, validando, reportando. Modelo: definido por papel em `model_routing.yaml`, otimizado por custo e criticidade.

Regra: nunca assumir que um agente e programatico sem que isso esteja documentado em `AGENTS.md` do projeto e em `model_routing.yaml`.

Ref: `10_ESTRATEGIA_DE_MODELOS_PARA_AGENTES.md` — secao "Eixo interativo vs programatico".

## Quando perguntar ao humano

- Ambiguidade de regra de negocio ou regulatoria
- Credencial ou acesso externo ausente
- Risco de escrita indevida em fonte sensivel
- Conflito de escopo entre capacidades
- Decisao que afeta arquitetura de forma irreversivel

Em todos os outros casos: agir, corrigir se necessario, reportar resultado.
