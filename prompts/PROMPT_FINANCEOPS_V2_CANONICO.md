# Prompt Canonico - FinanceOps v2

## Objetivo

Prompt pronto para iniciar o `financeops-v2` com `PROMPT_MESTRE_INICIAL`, ja alinhado com:

- separacao entre `contracts/*.md` e `src/contracts/*.py`
- `implementation/` obrigatorio por ser multi-agent
- testes offline antes de framework
- conflito historico entre base atual e `projeto-teste-financeops-agent`

## Como usar

Copie o bloco abaixo e envie como prompt inicial na sessao que vai criar o projeto.

```text
Leia a base de harness em:

- `/var/home/heliton/Documents/Projetos/harness-engineering/base-projetos-agenticos-harness-engineering/01_FRAMEWORK_PRATICO_HARNESS_AGENTIC_SYSTEMS.md`
- `/var/home/heliton/Documents/Projetos/harness-engineering/base-projetos-agenticos-harness-engineering/02_DOE_OPERACIONAL_PARA_HARNESS.md`
- `/var/home/heliton/Documents/Projetos/harness-engineering/base-projetos-agenticos-harness-engineering/03_BOOTSTRAP_PROJETO_AGENTICO.md`
- `/var/home/heliton/Documents/Projetos/harness-engineering/base-projetos-agenticos-harness-engineering/04_CHECKLIST_PARA_GERAR_AGENTS_MD.md`
- `/var/home/heliton/Documents/Projetos/harness-engineering/base-projetos-agenticos-harness-engineering/05_KB_MINIMA_PARA_PROJETOS_AGENTICOS.md`
- `/var/home/heliton/Documents/Projetos/harness-engineering/base-projetos-agenticos-harness-engineering/06_PADRAO_BUILDER_VALIDATOR_E_TASK_CONTRACTS.md`
- `/var/home/heliton/Documents/Projetos/harness-engineering/base-projetos-agenticos-harness-engineering/07_FRONTEND_OBSERVAVEL_PARA_AGENTES.md`
- `/var/home/heliton/Documents/Projetos/harness-engineering/base-projetos-agenticos-harness-engineering/09_TEMPLATES_PARA_BASE_HARNESS.md`
- `/var/home/heliton/Documents/Projetos/harness-engineering/base-projetos-agenticos-harness-engineering/10_ESTRATEGIA_DE_MODELOS_PARA_AGENTES.md`
- `/var/home/heliton/Documents/Projetos/harness-engineering/base-projetos-agenticos-harness-engineering/11_PROTOCOLO_DE_EXECUCAO_AGENTICA.md`
- `/var/home/heliton/Documents/Projetos/harness-engineering/base-projetos-agenticos-harness-engineering/12_ORQUESTRADOR_E_SUBAGENTES_PARA_FLUXOS_DE_EXECUCAO.md`
- `/var/home/heliton/Documents/Projetos/harness-engineering/base-projetos-agenticos-harness-engineering/13_OBSERVABILIDADE_DE_MODELOS_E_AGENTES.md`
- `/var/home/heliton/Documents/Projetos/harness-engineering/base-projetos-agenticos-harness-engineering/14_EXPANSAO_DE_PAPEIS_AGENTICOS.md`
- `/var/home/heliton/Documents/Projetos/harness-engineering/base-projetos-agenticos-harness-engineering/15_FASES_DE_IMPLEMENTACAO_EXECUTAVEIS.md`
- `/var/home/heliton/Documents/Projetos/harness-engineering/base-projetos-agenticos-harness-engineering/17_POR_QUE_FASE_MANUAL_ANTES_DO_FRAMEWORK.md`
- `/var/home/heliton/Documents/Projetos/harness-engineering/base-projetos-agenticos-harness-engineering/18_AUTONOMIA_AGENTICA_E_GUARDRAILS.md`
- `/var/home/heliton/Documents/Projetos/harness-engineering/base-projetos-agenticos-harness-engineering/templates/TEMPLATE_PROGRESS.md`
- `/var/home/heliton/Documents/Projetos/harness-engineering/base-projetos-agenticos-harness-engineering/templates/TEMPLATE_VALIDATION_STATUS.md`

Quero iniciar um novo projeto agentico em:

`/var/home/heliton/Documents/Projetos/harness-engineering/financeops-v2`

Projeto:

- Nome: `FinanceOps v2`
- Objetivo: `Recriar o FinanceOps Agent como projeto canonico derivado da base atual, capaz de consolidar lancamentos financeiros, detectar inconsistencias com regras fixas + LLM e gerar relatorio executivo com trilha de auditoria e validacao contratual entre fases.`
- Dominio: `financas`
- Usuario ou operacao alvo: `analistas financeiros, controller e operacao de auditoria interna`
- Stack preferida: `Python + FastAPI + PostgreSQL + Streamlit`
- Integracoes previstas: `ERP interno, planilhas CSV e banco PostgreSQL`
- Restricoes importantes: `nao alterar lancamentos automaticamente, manter audit_log imutavel, mascarar dados sensiveis antes de qualquer envio ao LLM, operar com validacao contratual entre fases, exigir testes offline sem DB e sem LLM real, e priorizar aderencia estrita a base atual em vez de reproduzir exatamente o projeto FinanceOps anterior`
- Estrategia inicial de modelos por papel: `OrchestratorAgent: sem LLM se possivel; IngestionAgent: sem LLM; DetectorAgent: modelo robusto para analise semantica; ValidatorAgent: sem LLM; ReporterAgent: sem LLM; verificacoes auxiliares: modelo economico apenas se realmente necessario`
- Fora de escopo: `nao executar pagamento, nao integrar banco externo, nao fazer previsao financeira por ML, nao migrar para CrewAI ou LangGraph nesta primeira versao e nao priorizar compatibilidade retroativa com o projeto teste antigo quando isso conflitar com a base atual`

Contexto adicional obrigatorio:

- Existe um projeto historico de referencia em `/var/home/heliton/Documents/Projetos/harness-engineering/projeto-teste-financeops-agent`
- Esse projeto historico deve ser usado como referencia de dominio e de aprendizado, nao como fonte de verdade estrutural
- Quando houver conflito entre a base atual e o projeto historico, priorize a base atual e liste o conflito explicitamente
- Convencao de contratos obrigatoria neste novo projeto:
  - `contracts/*.md` para task contracts, contratos documentais e invariantes de fase/capacidade
  - `src/contracts/*.py` para contratos executaveis tipados usados em runtime e validados pelo `ValidatorAgent`

Quero que voce siga a logica de harness e trabalhe em fases.

Importante:

- Nao implemente o sistema inteiro de uma vez
- Nao pule direto para codigo sem definir a base
- Nao improvise estrutura sem primeiro verificar a base de harness
- Nao gere tudo em modo one-shot
- Nao declare uma fase como pronta sem evidencias de validacao
- Ao propor multi-agent, deixe claro quando usar agente unico e quando usar subagentes especializados
- Ao propor subagentes, especifique papel, handoff, tools permitidas e output esperado
- Como este projeto e uma recriacao controlada de um projeto teste anterior, priorize a base atual quando houver conflito com a implementacao antiga
- Liste explicitamente quaisquer conflitos identificados entre a base atual e o FinanceOps anterior
- Se o projeto for multi-agent, `implementation/` e obrigatorio — nao opcional
- Ao reportar execucao no chat, seguir padrao: checklist por etapa com agente + modelo LLM quando chamado + tabela para dados estruturados
- A Fase 1 ja deve indicar explicitamente como os contratos serao separados entre `contracts/` e `src/contracts/`

Sua tarefa inicial neste momento e apenas a `Fase 1: Definicao`.

Entregue apenas:

1. objetivo refinado do projeto
2. escopo inicial
3. stack sugerida
4. integracoes principais
5. restricoes concretas
6. riscos iniciais
7. classificacao do bootstrap mais adequado: `minimo`, `recomendado` ou `completo`
8. proposta da estrutura inicial do projeto
9. proposta inicial de `spec/` com os arquivos base da fase atual
10. recomendacao inicial: agente unico ou multi-agent, com justificativa
11. estrategia inicial de separacao entre `contracts/*.md` e `src/contracts/*.py`
12. lista explicita de divergencias esperadas entre `financeops-v2` e o `projeto-teste-financeops-agent` antigo

Nao crie arquivos ainda, a menos que eu aprove a definicao.
```
