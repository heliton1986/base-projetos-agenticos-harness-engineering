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
7. `.claude/kb/autonomy-guardrails/quick-reference.md`
8. `04_CHECKLIST_PARA_GERAR_AGENTS_MD.md` — seguir checklist item a item
9. `05_KB_MINIMA_PARA_PROJETOS_AGENTICOS.md` — kb-first como memoria operacional reutilizavel
10. `06_PADRAO_BUILDER_VALIDATOR_E_TASK_CONTRACTS.md` — gates reais, contratos e loop de correcao
11. `09_TEMPLATES_PARA_BASE_HARNESS.md` — nenhum artefato nasce sem template correspondente
12. `10_ESTRATEGIA_DE_MODELOS_PARA_AGENTES.md` — definir antes de implementar qualquer agente
13. `11_PROTOCOLO_DE_EXECUCAO_AGENTICA.md` — execucao, correcao, reexecucao e validacao
14. `12_ORQUESTRADOR_E_SUBAGENTES_PARA_FLUXOS_DE_EXECUCAO.md` — handoff entre papeis
15. `13_OBSERVABILIDADE_DE_MODELOS_E_AGENTES.md` — agente, modelo, status, retries, validacao
16. `15_FASES_DE_IMPLEMENTACAO_EXECUTAVEIS.md` — ordem de entrega incremental verificavel
17. `17_POR_QUE_FASE_MANUAL_ANTES_DO_FRAMEWORK.md` — quando usar framework vs implementacao manual
18. `18_AUTONOMIA_AGENTICA_E_GUARDRAILS.md` — guardrails, JIT context, docstring-as-spec, convergence formula
19. `prompts/base-generica/PROMPT_DEFINICAO_PROJETO.md`

Obrigatorio por contexto ao criar projeto novo:

- `14_EXPANSAO_DE_PAPEIS_AGENTICOS.md` — quando o projeto for multi-agent ou houver duvida sobre criar novos papeis
- `07_FRONTEND_OBSERVAVEL_PARA_AGENTES.md` — quando houver UI, API com verificacao live ou necessidade de observabilidade visual

Complementar:

- `08_ESTRUTURA_OPCIONAL_KB_REFERENCES_VISUALS_EXAMPLES.md` — camada opcional de apoio, exemplos, references e visuals
- `prompts/projetos/TEMPLATE_PROMPT_PROJETO_CANONICO.md` — usar para criar o prompt canonico obrigatorio do projeto
- `prompts/projetos/TEMPLATE_PROMPTS_PROJETO_POR_FASE.md` — usar quando o projeto entrar em validacao controlada ou execucao faseada

### Ao evoluir projeto existente

1. Este `AGENTS.md`
2. `kb/[ferramenta]/quick-reference.md` relevante para a tarefa — kb-first, context7 como fallback
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

Depois de cada tool call individual, publicar tambem um micro-resultado imediato no chat antes da proxima acao:
- o que acabou de acontecer
- se passou, falhou ou ficou pendente
- qual sera o proximo passo local
- quais arquivos foram lidos ou explorados, quando a interface ou harness resumir, colapsar ou ocultar essa atividade
- quais comandos realmente rodaram, quando a interface ou harness resumir, colapsar ou ocultar essa atividade
- se houve varias leituras ou comandos relevantes, nao esperar acumular um lote grande: relatar logo apos cada acao observavel relevante sempre que possivel

Objetivo: reduzir espera silenciosa e manter o usuario vendo progresso quase em tempo real.

Quando um prompt disser `entregue`, `mostre`, `resuma` ou equivalente:
- a saida final deve aparecer no chat em bloco estruturado
- nao depender do output cru do Bash para o usuario entender o estado
- comandos podem ser usados nos bastidores, mas o resultado consumivel deve ser textual e organizado na conversa

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
- Nunca acumular varias acoes silenciosamente para resumir so no fim — cada tool call deve ter retorno curto antes da proxima
- Nunca depender de resumos genericos da interface ou do harness como unica pista visual — o chat deve nomear explicitamente os arquivos lidos e os comandos executados
- Quando houver sequencia de leituras/comandos relevantes, preferir granularidade quase item a item: 1 acao observavel relevante -> 1 retorno curto no chat
- Sempre imprimir tabela de resultado depois de cada fase (nao so APROVADO/FALHOU)
- **Coluna "Modelo" obrigatoria para todo agente que usa LLM** — nunca omitir. Agente deterministico: coluna omitida ou `— (deterministico)`. Agente LLM: modelo exato (ex: `claude-sonnet-4-6`). Isso vale para fases normais e para verificacao live de UI/API.
- Se falhou: informar erro exato antes de corrigir
- Se bloqueio real: parar e explicar o que precisa de intervencao humana
- Output do Bash fica colapsado na UI — tabela no chat e a unica visibilidade completa para o usuario
- Sempre preferir bloco estruturado no chat a despejar saida bruta de terminal

Exemplo de micro-resultado bom:

```text
[Gate 2 — Revalidacao executavel] rodei `python execution/run_onboarding_flow.py`, `pytest tests/ -v --tb=short` e `python tools/validate_harness_project.py .`.
Li `AGENTS.md`, `README.md`, `progress/PROGRESS.md` e `progress/VALIDATION_STATUS.md`.
Resultado: onboarding e pytest passaram; o validador encontrou 1 falha em `progress/`.
Proximo passo: corrigir os dois arquivos de `progress/` e reexecutar o validador.
```

Exemplo de granularidade ideal:

```text
Li `AGENTS.md`. Resultado: alinhei o protocolo narrativo que preciso seguir. Proximo passo: abrir `11_PROTOCOLO_DE_EXECUCAO_AGENTICA.md`.
Li `11_PROTOCOLO_DE_EXECUCAO_AGENTICA.md`. Resultado: encontrei a secao de micro-updates. Proximo passo: editar a regra.
Rodei `pytest tests/ -v --tb=short`. Resultado: passou. Proximo passo: validar o projeto com `python tools/validate_harness_project.py .`.
```

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

### CI + Coverage (obrigatorio antes de migrar para framework)

Todo projeto derivado deve ter CI configurado antes de qualquer migração para framework (CrewAI, LangChain, etc).

Regras:
- `.github/workflows/tests.yml` — roda `pytest` a cada push/PR, bloqueia merge se falhar
- `.coveragerc` — excluir `src/db/` (requer DB real, nao testavel offline)
- Coverage minimo: **80%** sobre `src/` excluindo `src/db/`
- Adicionar `pytest>=8.0.0` e `pytest-cov>=5.0.0` ao `requirements.txt`
- `.coverage`, `htmlcov/`, `.pytest_cache/` no `.gitignore`

Por que antes do framework: refatoracao de agentes pode quebrar regras de negocio fixas silenciosamente. CI detecta regressao no push.

Ref: `templates/TEMPLATE_CI.md`

### Parser de output LLM (obrigatorio quando agente parseia texto do LLM)

Quando agente parseia output textual de LLM com campo tipado, usar padrao robusto:

- Prompt pede formato `ID|tipo|descricao_curta` — sem markdown, sem JSON
- Parser usa regex com UUID/ID como ancora: `re.compile(r"(uuid-pattern)\|([^|]+)\|(.+)")`
- Usar `search()`, nao `match()` — captura mesmo com prefixo markdown na linha
- Strip markdown residual no campo descricao: `.strip("*\`")`
- Normalizar tipo antes de validar: `re.sub(r"[^a-zA-Z0-9_]", "_", tipo).strip("_")`
- Fallback obrigatorio: tipo invalido → tipo generico (ex: `inconsistencia_semantica`). Nunca descartar linha nem propagar tipo invalido.

Ref: `06_PADRAO_BUILDER_VALIDATOR_E_TASK_CONTRACTS.md` — secao "Parser de Output LLM"

### Templates opcionais por capacidade

Usar apenas quando o projeto requer a capacidade. Nao adicionar por padrao.

| Capacidade | Quando usar | Template |
|-----------|-------------|----------|
| API REST (FastAPI) | expor processamento via HTTP, upload de arquivos, integracao com outros sistemas | `templates/TEMPLATE_FASTAPI.md` |
| UI Web (Streamlit) | interface visual para usuario nao-tecnico, upload + visualizacao + download | `templates/TEMPLATE_STREAMLIT.md` |
| Chat UI (Chainlit) | interface conversacional para usuario final, streaming token a token, tool steps visiveis | `templates/TEMPLATE_CHAINLIT.md` |
| Agente ReAct (LangGraph) | agente com decisao autonoma de ferramentas, dual-store routing, loop ReAct | `templates/TEMPLATE_LANGGRAPH.md` |
| Observabilidade LLM (LangFuse) | rastrear chamadas LLM em producao, custo, latencia, qualidade | futuro |
| Framework multi-agent (CrewAI) | multiplos agentes com papeis distintos, handoff sequencial/paralelo | futuro |

Regra: adicionar capacidade apenas quando requisito esta definido — nao por antecipacao.

### Oferta de proximo passo ao final de cada entrega (obrigatorio)

Ao concluir qualquer fase, gate ou entrega verificavel, oferecer proximo passo concreto antes de encerrar.

Regras:
- Nunca oferecer opcao generica ("quer continuar?") — sempre nomear o que sera feito e onde rodara
- Oferecer no maximo 3 opcoes relevantes para o estado atual do projeto
- Se houver componente subivel (FastAPI, Streamlit, Chainlit), oferecer explicitamente com porta e rota

Formato:
```
Proximo passo:
A) [acao concreta] — [o que o usuario vera/testara]
B) [acao concreta] — [o que o usuario vera/testara]
C) Encerrar aqui

Qual escolhe?
```

Exemplos validos:
- "Quer subir o FastAPI no localhost:8000 para testar o endpoint POST /processar com um CSV real?"
- "Quer abrir o Streamlit no localhost:8501 para visualizar as inconsistencias detectadas?"
- "Proximo: implementar Fase 4 (RelatorioAgent) ou encerrar aqui?"

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
6. **`implementation/` obrigatorio em projetos multi-agent** — todo projeto com mais de um agente deve ter diretorio `implementation/` com plano de implementacao por agente antes de codar. Ref: `15_FASES_DE_IMPLEMENTACAO_EXECUTAVEIS.md`
7. **Arquivo de fase em `implementation/` nao pode ser placeholder** — titulo + 1 frase nao contam como runbook valido. Cada fase deve seguir o `TEMPLATE_IMPLEMENTATION_PHASE.md` com pre-condicoes, arquivos a ler, passos, validacoes, criterio de aprovacao, artefatos esperados e proxima fase.
8. **Nunca declarar fase com UI/API concluida sem verificacao live** — apos implementar FastAPI, Streamlit ou Chainlit: subir o servico, verificar golden path manualmente (upload real, resposta esperada, sem erro na UI). pytest offline nao substitui verificacao live. Ref: templates `TEMPLATE_FASTAPI.md`, `TEMPLATE_STREAMLIT.md`, `TEMPLATE_CHAINLIT.md`

## Estrutura da base

```
.md (01-18)           fonte de verdade — por que e quando aplicar cada padrao
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
