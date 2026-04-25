# Prompt Mestre Inicial

## Objetivo

Este arquivo serve como prompt mestre reutilizavel para iniciar um novo projeto agentico com base em Harness Engineering.

Ele deve ser usado como prompt de abertura e alinhamento, nao como pedido para implementar tudo de uma vez.

## Como usar

Substitua os campos entre colchetes e envie para a LLM.

## Template

Leia a base de harness em:

- `/var/home/heliton/Documents/Projetos/harness-engineering/base-projetos-agenticos-harness-engineering/FRAMEWORK_PRATICO_HARNESS_AGENTIC_SYSTEMS.md`
- `/var/home/heliton/Documents/Projetos/harness-engineering/base-projetos-agenticos-harness-engineering/DOE_OPERACIONAL_PARA_HARNESS.md`
- `/var/home/heliton/Documents/Projetos/harness-engineering/base-projetos-agenticos-harness-engineering/BOOTSTRAP_PROJETO_AGENTICO.md`
- `/var/home/heliton/Documents/Projetos/harness-engineering/base-projetos-agenticos-harness-engineering/CHECKLIST_PARA_GERAR_AGENTS_MD.md`

Se fizer sentido enriquecer a base com camadas opcionais de apoio, consulte tambem:

- `/var/home/heliton/Documents/Projetos/harness-engineering/base-projetos-agenticos-harness-engineering/ESTRUTURA_OPCIONAL_KB_REFERENCES_VISUALS_EXAMPLES.md`
- `/var/home/heliton/Documents/Projetos/harness-engineering/base-projetos-agenticos-harness-engineering/KB_MINIMA_PARA_PROJETOS_AGENTICOS.md`
- `/var/home/heliton/Documents/Projetos/harness-engineering/base-projetos-agenticos-harness-engineering/PADRAO_BUILDER_VALIDATOR_E_TASK_CONTRACTS.md`
- `/var/home/heliton/Documents/Projetos/harness-engineering/base-projetos-agenticos-harness-engineering/FRONTEND_OBSERVAVEL_PARA_AGENTES.md`
- `/var/home/heliton/Documents/Projetos/harness-engineering/base-projetos-agenticos-harness-engineering/templates/TEMPLATE_PROGRESS.md`
- `/var/home/heliton/Documents/Projetos/harness-engineering/base-projetos-agenticos-harness-engineering/templates/TEMPLATE_VALIDATION_STATUS.md`
- `/var/home/heliton/Documents/Projetos/harness-engineering/base-projetos-agenticos-harness-engineering/10_ESTRATEGIA_DE_MODELOS_PARA_AGENTES.md`
- `/var/home/heliton/Documents/Projetos/harness-engineering/base-projetos-agenticos-harness-engineering/11_PROTOCOLO_DE_EXECUCAO_AGENTICA.md`
- `/var/home/heliton/Documents/Projetos/harness-engineering/base-projetos-agenticos-harness-engineering/12_ORQUESTRADOR_E_SUBAGENTES_PARA_FLUXOS_DE_EXECUCAO.md`
- `/var/home/heliton/Documents/Projetos/harness-engineering/base-projetos-agenticos-harness-engineering/13_OBSERVABILIDADE_DE_MODELOS_E_AGENTES.md`

Quero iniciar um novo projeto agentico em:

`[CAMINHO_DO_PROJETO]`

Projeto:

- Nome: `[NOME_DO_PROJETO]`
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

Nao crie arquivos ainda, a menos que eu aprove a definicao.


Observacao opcional: se o projeto ja souber que usara modelos diferentes por papel, voce pode gerar tambem um `templates/TEMPLATE_MODEL_ROUTING.md` adaptado ao contexto do projeto.
