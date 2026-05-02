# Prompts por Fase

## Objetivo

Este arquivo organiza prompts curtos e reutilizaveis para criar projetos agenticos de forma disciplinada, seguindo `Harness Engineering`.

A ideia e evitar implementacao one-shot e trabalhar em etapas controladas.

## Nota de uso

Estes prompts sao usados em sequencia — cada fase pressupoe que os docs lidos na Fase 1 permanecem no contexto da sessao.

Se iniciar uma nova sessao em qualquer fase alem da 1, releia os docs da Fase 1 antes de continuar.

---

## Fase 1 - Definicao

Use este prompt para iniciar o projeto.

```text
Leia os seguintes documentos da base de harness em `[HARNESS_BASE_PATH]`:
- `01_FRAMEWORK_PRATICO_HARNESS_AGENTIC_SYSTEMS.md`
- `02_DOE_OPERACIONAL_PARA_HARNESS.md`
- `03_BOOTSTRAP_PROJETO_AGENTICO.md`
- `04_CHECKLIST_PARA_GERAR_AGENTS_MD.md`
- `05_KB_MINIMA_PARA_PROJETOS_AGENTICOS.md`
- `06_PADRAO_BUILDER_VALIDATOR_E_TASK_CONTRACTS.md`
- `09_TEMPLATES_PARA_BASE_HARNESS.md`
- `10_ESTRATEGIA_DE_MODELOS_PARA_AGENTES.md`
- `11_PROTOCOLO_DE_EXECUCAO_AGENTICA.md`
- `12_ORQUESTRADOR_E_SUBAGENTES_PARA_FLUXOS_DE_EXECUCAO.md`
- `13_OBSERVABILIDADE_DE_MODELOS_E_AGENTES.md`
- `15_FASES_DE_IMPLEMENTACAO_EXECUTAVEIS.md`
- `17_POR_QUE_FASE_MANUAL_ANTES_DO_FRAMEWORK.md`
- `18_AUTONOMIA_AGENTICA_E_GUARDRAILS.md`

Se o projeto for multi-agent ou houver duvida sobre criacao de papeis, leia tambem:
- `14_EXPANSAO_DE_PAPEIS_AGENTICOS.md`

Se o projeto incluir UI, API com verificacao live ou observabilidade visual, leia tambem:
- `07_FRONTEND_OBSERVAVEL_PARA_AGENTES.md`

Me ajude a definir um novo projeto agentico.

Quero construir: [OBJETIVO]
Dominio: [DOMINIO]
Usuario ou operacao alvo: [USUARIO]
Stack preferida: [STACK]
Integracoes previstas: [INTEGRACOES]
Restricoes importantes: [RESTRICOES]
Fora de escopo: [FORA_DE_ESCOPO]

Primeiro, nao implemente nada.

Extraia e proponha apenas:
- objetivo refinado
- escopo inicial
- stack sugerida
- integracoes principais
- restricoes concretas
- riscos iniciais
- classificacao do bootstrap mais adequado: recomendado ou completo
- estrutura inicial sugerida do projeto
- proposta inicial de spec/ para a fase atual
- contratos minimos de dados necessarios para a primeira capacidade
- se fizer sentido, proposta inicial de task contracts e gates de validacao
- recomendacao inicial: agente unico ou multi-agent, com justificativa
- estrategia inicial de modelos por papel, se aplicavel
- se multi-agent fizer sentido, sugira os primeiros subagentes, com papel e handoff esperado
```

## Fase 2 - Bootstrap

Use este prompt depois de aprovar a definicao.

```text
Com base na definicao aprovada, crie a estrutura inicial do projeto em `[CAMINHO_DO_PROJETO]` usando o pacote [RECOMENDADO/COMPLETO].

Gere primeiro:
- README.md
- directives/
- spec/
- implementation/
- execution/
- .env.example
- proposta inicial de AGENTS.md

Se o pacote escolhido exigir, inclua tambem:
- tests/
- progress/
- docs/
- contracts/
- evals/

Ao montar AGENTS.md, directives/ e spec/, deixe explicito:
- quando usar agente unico
- quando usar subagentes
- como deve ser o handoff entre agentes
- quais tools podem ser usadas por cada papel
- quais modelos fazem sentido para cada papel, se aplicavel
- quais validacoes minimas sao gates obrigatorios
- como `implementation/` deve refletir a fase atual — obrigatorio se o projeto for multi-agent (CrewAI, LangGraph com multiplos nos, handoff entre agentes); opcional apenas para projetos de agente unico com menos de 4 fases
- se a fase atual precisa de task contracts formais
- quais contratos minimos de dados precisam existir antes da primeira capacidade
- qual template da base foi usado para cada artefato obrigatorio criado

Nao implemente ainda o sistema inteiro. Foque no bootstrap correto do projeto.

Se a base ficar aprovada e os contratos minimos de dados estiverem claros, o proximo passo esperado e continuar automaticamente para a primeira capacidade incremental minima, sem pedir aprovacao adicional generica.

Se a base do projeto exigir padronizacao mais forte, voce pode tambem propor a criacao de templates reutilizaveis para README, AGENTS, spec, task contracts, progress e validacao.
```

## Fase 3 - Validacao da Base

Use este prompt depois do bootstrap.

```text
Revise a estrutura criada do projeto em `[CAMINHO_DO_PROJETO]` e me diga se ela ja esta apta para comecar implementacao agentica com boa base de harness.

Analise:
- clareza do README.md
- qualidade das directives/
- qualidade da spec/
- adequacao do AGENTS.md
- separacao entre diretivas, especificacao e execucao
- validacao minima existente
- criterios de pronto por fase
- clareza sobre agente unico vs subagentes
- clareza de handoff entre agentes
- clareza sobre task contracts e gates de aprovacao
- clareza dos contratos minimos de dados
- politica de ambiguidade: o que pode ser assumido com registro e o que exige pergunta
- lacunas importantes

Aponte objetivamente o que falta para o projeto estar pronto para a primeira implementacao incremental.
Nao implemente ainda, a menos que a base esteja claramente aprovada.
Se a base estiver aprovada, deixe isso explicito e sinalize que a fase seguinte deve continuar automaticamente para a primeira capacidade incremental minima.
Nao avance para a proxima fase sem deixar claro se a base esta aprovada ou reprovada.
```

## Fase 4 - Primeira Implementacao Incremental

Use este prompt apenas depois de validar a base.

```text
Agora implemente apenas a primeira capacidade do sistema, respeitando:
- README.md
- AGENTS.md
- directives/
- spec/
- execution/

Importante:
- nao tente construir tudo de uma vez
- trabalhe em uma unica capacidade pequena e validavel
- reuse ferramentas existentes antes de criar novas
- adicione validacao minima quando aplicavel
- registre o que foi feito e o que falta
- se fizer sentido, use um template de progress para manter continuidade
- mantenha a implementacao coerente com a spec da fase atual
- use contratos de dados, directives, spec e kb para evitar suposicoes fora do escopo
- se faltar detalhe de baixo risco, assuma de forma conservadora e registre
- se faltar detalhe de alto risco, sensivel ou regulatorio, pare e pergunte objetivamente
- se a capacidade exigir orquestracao, explicite se sera com agente unico ou com subagentes
- se usar subagentes, deixe claro papel, handoff, tools e output de cada um
- explicite como a capacidade sera validada e quem valida

Ao final, responda no chat com um bloco estruturado contendo:
- o que foi implementado
- como validar
- o que ainda nao foi feito
- qual deve ser a proxima capacidade
- se a capacidade foi aprovada ou se ainda precisa de correcao antes de seguir
- se fizer sentido, registre a aprovacao usando um template de validation status
- quais suposicoes foram feitas e onde foram registradas
- se a capacidade ja estiver operacional, crie tambem um fluxo unico de onboarding para primeira execucao
```

## Fase 5 - Expansao Controlada

Use este prompt para continuar o projeto sem perder disciplina.

```text
Com base no estado atual do projeto em `[CAMINHO_DO_PROJETO]`, implemente apenas a proxima capacidade prioritaria.

Antes de escrever codigo:
- revise README.md
- revise AGENTS.md
- revise directives/
- revise spec/
- revise progresso atual

Siga o metodo de harness:
- nao expandir escopo sem necessidade
- nao quebrar a arquitetura existente
- validar antes de declarar pronto
- atualizar memoria operacional quando houver aprendizado importante
- escolher conscientemente entre agente unico e multi-agent
- se houver handoff entre agentes, mante-lo autocontido e auditavel
- se a capacidade exigir validação forte, use task contracts e gates explicitos

Nao avance para a proxima capacidade sem declarar explicitamente se a capacidade atual passou nos gates minimos de validacao.
```

## Regra de ouro

Se houver duvida sobre o que fazer, use esta ordem:

1. definir
2. estruturar
3. validar a base
4. implementar incrementalmente
5. validar novamente

Nao inverter esta ordem.

## Enfases de Harness

- validar antes de avancar
- escolher conscientemente entre agente unico e multi-agent
- tornar handoffs explicitos, autocontidos e auditaveis
- nao declarar pronto sem evidencia de validacao

## Politica de Continuidade

Depois que a base estiver aprovada, a expectativa padrao desta base e:

- continuar automaticamente para a primeira capacidade incremental minima
- usar `templates/TEMPLATE_FIRST_INCREMENTAL_CAPABILITY.md` quando fizer sentido
- usar `templates/TEMPLATE_DATA_CONTRACT.md` quando o dominio depender de estrutura de dados mais explicita
- usar `templates/TEMPLATE_ONBOARDING_FLOW.md` quando a primeira capacidade ja puder ser executada de ponta a ponta
- seguir `11_PROTOCOLO_DE_EXECUCAO_AGENTICA.md` quando o usuario pedir a execucao de um fluxo ou script
- perguntar ao humano apenas quando houver ambiguidade de alto risco ou alto impacto
