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
2. `kb/index.md` do projeto — estado atual, proximos passos, fontes de verdade
3. `kb/domain.md` do projeto — agentes, modelos, stack, fluxo
4. `kb/rules.md` do projeto — regras de negocio e contratos por agente
5. `progress/PROGRESS.md` do projeto
6. Arquivos diretamente afetados pela tarefa

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

### Antes da tool call (contexto do que vai fazer)

Explicar em 1-2 linhas:
- o que a fase/gate vai executar
- qual agente sera acionado e com qual modelo (se LLM)
- o que se espera como resultado

Exemplo:
```
[Fase 3 — Deteccao] iniciando DetectorAgent.
Regras fixas primeiro (duplicata, valor alto, descricao suspeita), depois LLM (claude-sonnet-4-6)
para analise semantica dos candidatos restantes, com valores mascarados por faixa.
```

### Formato durante execucao

```
[Fase X — Nome]        iniciando...
[Gate X — Nome]        verificando...
*(executa tool)*
[Gate X — Nome]        APROVADO ✓
[AgenteX]              descricao do que fez
[Fase X — Nome]        CONCLUIDA ✓
```

### Depois da tool call (resultado por fase — obrigatorio)

Apos cada fase, imprimir no chat tabela ou bloco com:
- modelo usado (se LLM foi acionado)
- quantidade de itens processados
- resultado concreto por agente: tipo/severidade de inconsistencias, status, totais
- qualquer detalhe que aparece no terminal mas fica colapsado na UI

Formato sugerido (adaptar ao dominio do projeto):

```
[Fase 2 — Ingestao] CONCLUIDA ✓
| Agente         | Resultado                          |
|----------------|------------------------------------|
| IngestionAgent | 9 lancamentos normalizados, 1 erro |

[Fase 3 — Deteccao] CONCLUIDA ✓
| Agente        | Modelo              | Resultado                                        |
|---------------|---------------------|--------------------------------------------------|
| DetectorAgent | claude-sonnet-4-6   | 2 inconsistencias: duplicata_suspeita [critica], descricao_suspeita [media] |

[Fase 4 — Relatorio] CONCLUIDA ✓
| Agente        | Status         | Total lancamentos | Total inconsistencias |
|---------------|----------------|-------------------|-----------------------|
| ReporterAgent | requer_revisao | 9                 | 2                     |
```

### Regras

- Nunca executar tool call silenciosamente — sempre anunciar antes com contexto
- Sempre imprimir tabela de resultado depois de cada fase (nao so APROVADO/FALHOU)
- Se falhou: informar erro exato antes de corrigir
- Se bloqueio real: parar e explicar o que precisa de intervencao humana
- Output do Bash fica colapsado na UI — tabela no chat e a unica visibilidade completa para o usuario

### ValidatorAgent como gate entre fases (obrigatorio)

Todo projeto derivado deve ter um `ValidatorAgent` que revalida o contrato de saida de cada agente antes de passar ao proximo.

Padrao obrigatorio apos cada agente no `run_flow.py`:

```python
def _validar_contrato(session, run_id, instancia, nome_agente: str) -> None:
    from src.agents.validator_agent import ValidatorAgent
    from src.db.audit import registrar
    vr = ValidatorAgent().validar_instancia(instancia)
    registrar(session, run_id, "ValidatorAgent", f"validacao_{type(instancia).__name__}",
              "ok" if vr.valido else "falhou", {"erros": vr.erros})
    if not vr.valido:
        raise RuntimeError(f"Contrato {vr.contrato_validado} invalido apos {nome_agente}: {vr.erros}")
```

Regras:
- Gate `Validacao Contrato` aparece no terminal apos cada gate de agente
- Contrato invalido para o fluxo imediatamente — nao propaga dado corrompido
- Toda validacao registrada no `audit_log` com status `ok` ou `falhou`
- `ValidatorAgent` nao usa LLM — validacao Pydantic deterministica

### Testes automatizados (obrigatorio)

Todo projeto derivado deve ter testes offline — sem DB, sem LLM, sem API externa.

Regras:
- `tests/test_ingestion.py` — testa IngestionAgent com fixture e CSV temporario (`tmp_path`)
- `tests/test_detector.py` — testa regras fixas via metodos internos, sem chamar LLM. Instanciar com `DetectorAgent.__new__(DetectorAgent)` para evitar `__init__` que exige API key
- `tests/test_validator.py` — testa contratos validos e invalidos
- CSV com 1 linha valida + 1 invalida para testar rejeicoes (CSV so com invalidas levanta RuntimeError)
- Deve rodar em < 5s: `pytest tests/ -v`

Ref: `templates/TEMPLATE_TESTS.md`

### Atualizacao de progress/ ao final de cada fase

Faz parte da fase — nao e passo separado, nao requer confirmacao.
Ao concluir qualquer fase ou gate: atualizar `progress/PROGRESS.md` e `progress/VALIDATION_STATUS.md` automaticamente.
Formato de data obrigatorio: `YYYY-MM-DD HH:MM`.

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
8a. Usar TEMPLATE_KB.md → criar kb/ (index, domain, rules) antes de implementar qualquer agente
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
