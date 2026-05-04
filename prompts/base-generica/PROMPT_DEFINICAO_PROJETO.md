# Prompt Mestre Inicial

## Objetivo

Este arquivo serve como prompt mestre reutilizavel para iniciar um novo projeto agentico com base em Harness Engineering.

Ele deve ser usado como prompt de abertura e alinhamento, nao como pedido para implementar tudo de uma vez.

## Quando usar

Use este prompt quando quiser separar definicao de implementacao.

E o caminho preferencial quando:

- o dominio ainda precisa ser lapidado
- o projeto serve para validar a propria base
- o caso sera usado como referencia canonica
- ha recriacao controlada de um projeto anterior
- voce quer auditar a aderencia estrutural antes de deixar a execucao seguir sozinha

Resultado esperado:

- a LLM define primeiro
- a base e aprovada antes da primeira capacidade
- a implementacao segue depois, normalmente com `prompts/base-generica/PROMPTS_FASEADOS_BASE.md`

## Decisao obrigatoria de modo do projeto

Antes de qualquer implementacao, este prompt deve levar a LLM a classificar explicitamente o projeto em um dos modos abaixo:

- `operacional_simples`
- `validado_por_fases`
- `canonico_ou_referencia`

Regra derivada:

- `PROMPT_[PROJETO]_CANONICO.md` deve sempre ser criado
- `PROMPTS_[PROJETO]_POR_FASE.md` deve ser criado quando o projeto for `validado_por_fases` ou `canonico_ou_referencia`

Se houver duvida entre `operacional_simples` e `validado_por_fases`, preferir `validado_por_fases`.

## Como usar

Substitua os campos entre colchetes e envie para a LLM.

## Template

Leia a base de harness em:

- `[HARNESS_BASE_PATH]/FRAMEWORK_PRATICO_HARNESS_AGENTIC_SYSTEMS.md`
- `[HARNESS_BASE_PATH]/DOE_OPERACIONAL_PARA_HARNESS.md`
- `[HARNESS_BASE_PATH]/BOOTSTRAP_PROJETO_AGENTICO.md`
- `[HARNESS_BASE_PATH]/CHECKLIST_PARA_GERAR_AGENTS_MD.md`
- `[HARNESS_BASE_PATH]/KB_MINIMA_PARA_PROJETOS_AGENTICOS.md`
- `[HARNESS_BASE_PATH]/PADRAO_BUILDER_VALIDATOR_E_TASK_CONTRACTS.md`
- `[HARNESS_BASE_PATH]/09_TEMPLATES_PARA_BASE_HARNESS.md`
- `[HARNESS_BASE_PATH]/templates/TEMPLATE_PROGRESS.md`
- `[HARNESS_BASE_PATH]/templates/TEMPLATE_VALIDATION_STATUS.md`
- `[HARNESS_BASE_PATH]/10_ESTRATEGIA_DE_MODELOS_PARA_AGENTES.md`
- `[HARNESS_BASE_PATH]/11_PROTOCOLO_DE_EXECUCAO_AGENTICA.md`
- `[HARNESS_BASE_PATH]/12_ORQUESTRADOR_E_SUBAGENTES_PARA_FLUXOS_DE_EXECUCAO.md`
- `[HARNESS_BASE_PATH]/13_OBSERVABILIDADE_DE_MODELOS_E_AGENTES.md`
- `[HARNESS_BASE_PATH]/15_FASES_DE_IMPLEMENTACAO_EXECUTAVEIS.md`
- `[HARNESS_BASE_PATH]/17_POR_QUE_FASE_MANUAL_ANTES_DO_FRAMEWORK.md`
- `[HARNESS_BASE_PATH]/18_AUTONOMIA_AGENTICA_E_GUARDRAILS.md`

Se o projeto for multi-agent ou houver duvida sobre criacao de papeis, leia tambem:

- `[HARNESS_BASE_PATH]/14_EXPANSAO_DE_PAPEIS_AGENTICOS.md`

Se o projeto incluir UI, API com verificacao live ou observabilidade visual, leia tambem:

- `[HARNESS_BASE_PATH]/FRONTEND_OBSERVAVEL_PARA_AGENTES.md`

Como apoio complementar, quando precisar de camada opcional de examples, references ou visuals:

- `[HARNESS_BASE_PATH]/ESTRUTURA_OPCIONAL_KB_REFERENCES_VISUALS_EXAMPLES.md`

Quero iniciar um novo projeto agentico em:

`[CAMINHO_DO_PROJETO]`

Projeto:

- Nome: `[NOME_DO_PROJETO]`
- Modo do projeto: `[operacional_simples|validado_por_fases|canonico_ou_referencia]`
- Objetivo: `[OBJETIVO_DO_PROJETO]`
- Dominio: `[DOMINIO]`
- Usuario ou operacao alvo: `[USUARIO_OU_OPERACAO]`
- Stack preferida: `[STACK_PREFERIDA]`
- Integracoes previstas: `[INTEGRACOES]`
- Restricoes importantes: `[RESTRICOES]`
- Estrategia inicial de modelos por papel: `[MODELOS_POR_PAPEL]`
- Fora de escopo: `[FORA_DE_ESCOPO]`

Quero que voce siga a logica de harness e trabalhe em fases.

Importante:

- Nao implemente o sistema inteiro de uma vez
- Nao pule direto para codigo sem definir a base
- Nao improvise estrutura sem primeiro verificar a base de harness
- Nao gere tudo em modo one-shot
- Nao declare uma fase como pronta sem evidencias de validacao
- Ao propor multi-agent, deixe claro quando usar agente unico e quando usar subagentes especializados
- Ao propor subagentes, especifique papel, handoff, tools permitidas e output esperado
- Se o projeto for multi-agent, `implementation/` e obrigatorio — nao opcional. Agentes autonomos nao tem contexto de sessao; sem runbooks de fase explícitos, improvisam ordem e pulam validacoes
- Ao reportar execucao no chat, seguir padrao: checklist por etapa com agente + modelo LLM quando chamado + tabela para dados estruturados (ver `13_OBSERVABILIDADE_DE_MODELOS_E_AGENTES.md`)

Sua tarefa inicial neste momento e apenas a `Fase 1: Definicao`.

Responda no chat apenas com:

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
11. confirmar se `PROMPTS_[PROJETO]_POR_FASE.md` sera obrigatorio neste caso, com justificativa curta

Nao crie arquivos ainda, a menos que eu aprove a definicao.


Observacao opcional: se o projeto ja souber que usara modelos diferentes por papel, voce pode gerar tambem um `templates/TEMPLATE_MODEL_ROUTING.md` adaptado ao contexto do projeto.
