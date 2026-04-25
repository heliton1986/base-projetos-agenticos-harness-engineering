# Bootstrap de Projeto Agentico

## Objetivo

Este documento define como um novo projeto agentico deve nascer para aproveitar bem a base de `Harness Engineering`.

Ele existe para responder duas perguntas:

- qual estrutura minima um projeto precisa ter para funcionar bem com LLMs?
- qual estrutura e mais adequada quando queremos confiabilidade, reaproveitamento e evolucao saudavel?

## Recomendacao pratica

A recomendacao padrao desta base e:

- usar `pacote recomendado` como ponto de partida padrao
- usar `pacote completo` para projetos com maior risco, maior duracao ou maior criticidade

Em termos simples:

- `Recomendado` = ponto de partida ideal
- `Completo` = setup para maturidade operacional

## 1. Pacote recomendado

Use quando:

- o projeto vai continuar por mais de alguns dias
- existe mais de um fluxo importante
- ha integracoes externas
- ja existe a intencao de colocar agentes para trabalhar de forma estruturada

Este deve ser o ponto de partida padrao.

### Estrutura sugerida

```text
README.md
AGENTS.md
.env.example
directives/
spec/
implementation/
execution/
tests/
progress/
docs/
```

Antes da primeira capacidade real, o projeto recomendado deve registrar contratos minimos de dados em `directives/`, `spec/` ou `contracts/` para reduzir improvisacao sobre entradas e saidas.

### O que entra a mais

- `implementation/`
  - fases executaveis do projeto
  - guia a LLM por etapa
  - deve existir como camada obrigatoria no pacote recomendado e completo

- `tests/`
  - validacoes minimas automatizaveis
  - smoke tests, testes unitarios ou scripts de verificacao

- `progress/`
  - estado atual
  - backlog imediato
  - o que foi feito
  - o que falhou
  - proximos passos

- `docs/`
  - arquitetura
  - integracoes
  - modelos de dados
  - decisoes tecnicas relevantes

### Beneficios do pacote recomendado

- melhor continuidade entre sessoes
- melhor onboarding de novos agentes
- menor improvisacao
- maior clareza na validacao
- melhor base para crescer para multi-agent e harness mais forte

## 2. Pacote completo

Use quando:

- o projeto e importante para negocio
- ha multiplos agentes ou handoffs complexos
- ha risco tecnico relevante
- existe necessidade de auditabilidade
- o sistema tende a ir para producao

### Estrutura sugerida

```text
README.md
AGENTS.md
.env.example
directives/
spec/
implementation/
execution/
tests/
progress/
docs/
contracts/
evals/
observability/
scripts/bootstrap/
examples/
```

### O que entra a mais

- `contracts/`
  - contratos de tarefa
  - formatos de entrada e saida
  - acordos entre builder e validator

- `evals/`
  - suites de avaliacao
  - criterios qualitativos e quantitativos
  - cenarios de regressao

- `observability/`
  - traces
  - logs estruturados
  - configuracoes de monitoramento

- `scripts/bootstrap/`
  - scripts de setup
  - inicializacao de ambiente
  - seeds
  - checagens de precondicoes

- `examples/`
  - exemplos de input/output
  - consultas modelo
  - casos bons de referencia

### Beneficios do pacote completo

- maior previsibilidade
- maior reprodutibilidade
- maior rastreabilidade
- menor dependencia de memoria implicita
- melhor condicao para sistemas agenticos mais autonomos

## Escopo padrao de README.md

O `README.md` deve responder pelo menos:

- o que e o projeto
- qual problema resolve
- para quem
- qual stack usa
- como rodar localmente
- quais servicos e integracoes existem
- estrutura de diretorios
- principais restricoes do sistema
- onde estao as diretivas do dominio
- onde esta a especificacao do projeto
- como validar o projeto

### Estrutura recomendada

```text
# Nome do Projeto
## Visao Geral
## Objetivo
## Usuario ou Operacao Alvo
## Arquitetura Resumida
## Stack
## Como Rodar
## Estrutura do Projeto
## Integracoes e Dependencias
## Restricoes Importantes
## Diretivas de Dominio
## Especificacao do Projeto
## Validacao
```

## Escopo padrao de AGENTS.md

O `AGENTS.md` deve dizer como o agente trabalha dentro deste projeto especifico.

Deve cobrir:

- missao do agente
- o que ele pode e nao pode fazer
- modelo operacional
- ferramentas permitidas
- politica de subagentes
- politica de validacao
- memoria e artefatos
- politica de erro e escalacao

### Estrutura recomendada

```text
# Missao do Agente
# Modelo Operacional
# Ferramentas e Escopo
# Subagentes
# Validacao
# Memoria e Artefatos
# Politica de Erro
```

## Escopo padrao de directives/

O diretorio `directives/` guarda conhecimento operacional do dominio.

Exemplos de arquivos:

```text
directives/
  domain.md
  business-rules.md
  integrations.md
  output-contracts.md
  edge-cases.md
```

### O que deve ir em directives/

- regras de negocio
- contratos de entrada e saida
- politicas de uso de API
- edge cases conhecidos
- formatos esperados
- limitacoes do dominio
- regras de seguranca e consistencia

## Escopo padrao de spec/

O diretorio `spec/` guarda a especificacao do projeto e a decomposicao do trabalho.

Estrutura sugerida:

```text
spec/
  01-brainstorm.md
  02-define.md
  03-design.md
  04-build.md
  05-validate.md
```

### O que cada arquivo representa

- `01-brainstorm.md`
  - exploracao inicial de abordagens
  - alternativas e trade-offs

- `02-define.md`
  - requisitos
  - escopo
  - criterios de aceitacao

- `03-design.md`
  - arquitetura
  - componentes
  - fluxo entre agentes e tools

- `04-build.md`
  - plano de implementacao
  - ordem das entregas
  - ownership tecnico

- `05-validate.md`
  - estrategia de validacao
  - gates
  - checks e criterios de aprovacao

## Onde colocar restricoes concretas

### No README.md

Coloque restricoes de alto nivel, como:

- sistema deve responder em portugues
- integracao X e somente leitura
- nao apagar dados do cliente
- fluxo precisa funcionar com ambiente local

### Em directives/

Coloque restricoes operacionais e de dominio, como:

- limites de API
- ordem correta de chamadas
- campos obrigatorios
- formatos aceitos
- edge cases
- regras de calculo

### Em AGENTS.md

Coloque restricoes de comportamento do agente, como:

- quando pedir ajuda ao usuario
- quando nao alterar arquivos
- quando rodar validacoes
- como tratar erro

### Em spec/

Coloque restricoes de escopo e entrega, como:

- o que entra e o que nao entra na fase atual
- requisitos obrigatorios
- criterios de aceitacao
- gates de aprovacao

## Ordem recomendada de bootstrap

Ao iniciar um projeto novo, a sequencia recomendada e:

1. criar `README.md`
2. criar `directives/` com o dominio essencial
3. criar `spec/` com a estrutura inicial de definicao e design
4. criar `execution/` para o que for deterministico
5. gerar `AGENTS.md` usando a base harness
6. adicionar validacao minima em `tests/`
7. adicionar `progress/` se o projeto for continuar
8. evoluir para pacote completo se o projeto ganhar importancia

## KB minima opcional

Se o projeto tiver continuidade, multiplas sessoes ou risco de reexplicacao recorrente, considere adicionar tambem:

```text
kb/
  project-operating-model.md
  architecture.md
  stack.md
```

Referencia complementar:

- `KB_MINIMA_PARA_PROJETOS_AGENTICOS.md`

Essa camada e opcional no bootstrap inicial, mas tende a ajudar bastante em projetos que nao sao apenas experimentos curtos.

## Decisao padrao

Se houver duvida entre `minimo`, `recomendado` e `completo`, use esta regra:

- se e experimento curto, `minimo`
- se e projeto real com chance de continuidade, `recomendado`
- se e projeto serio, com integracoes, risco ou multi-agent, `completo`

### Regra pratica final

Por padrao:

`Nao comece no minimo. Comece no recomendado.`

## Templates como camada opcional

Conforme a base amadurece, faz sentido considerar tambem uma pasta `templates/` para padronizar artefatos como `README.md`, `AGENTS.md`, `spec/` e `task contracts`.

Referencia complementar:

- `TEMPLATES_PARA_BASE_HARNESS.md`

Essa camada nao precisa ser obrigatoria no inicio, mas tende a reduzir variabilidade em projetos recorrentes.

## Templates uteis para progresso e validacao

Se o projeto exigir mais disciplina operacional, faz sentido considerar tambem templates como:

- `templates/TEMPLATE_PROGRESS.md`
- `templates/TEMPLATE_VALIDATION_STATUS.md`

Esses templates ajudam a tornar memoria operacional e gates de validacao mais concretos.

## Referencias complementares de maturidade

Conforme o projeto ganhar complexidade, estas referencias podem ajudar bastante:

- `KB_MINIMA_PARA_PROJETOS_AGENTICOS.md`
- `FRONTEND_OBSERVAVEL_PARA_AGENTES.md`
- `PADRAO_BUILDER_VALIDATOR_E_TASK_CONTRACTS.md`

Esses documentos complementam a base sem serem obrigatorios para todo bootstrap inicial.

## Conclusao

A base de harness funciona melhor quando o projeto nasce com estrutura suficiente para:

- orientar a LLM
- limitar improvisacao
- preservar memoria
- validar resultados
- crescer sem perder consistencia

Em uma frase:

`O pacote minimo faz o projeto nascer; o pacote recomendado faz o projeto durar; o pacote completo faz o projeto escalar com confianca.`

## Reduzindo ambiguidade antes da primeira capacidade

Para evitar que a LLM invente estruturas fora do escopo, a base recomenda documentar explicitamente, antes da primeira implementacao incremental:

- formato exato dos CSVs ou exports equivalentes
- schema esperado das fontes principais
- formato do consolidado
- representacao de inconsistencia
- politica de mascaramento de dados sensiveis

Essas definicoes devem viver preferencialmente em:

- `directives/` quando forem regras operacionais do dominio
- `spec/` quando fizerem parte da entrega da fase
- `contracts/` quando precisarem virar acordo verificavel
- `kb/` quando forem conhecimento mais estavel e reaproveitavel

## Continuidade automatica apos aprovacao da base

Quando a base estiver aprovada e os contratos minimos de dados estiverem definidos, o proximo passo padrao nao deve ser perguntar genericamente o que fazer.

O proximo passo padrao deve ser:

1. implementar automaticamente a primeira capacidade incremental minima
2. assumir detalhes de baixo risco de forma conservadora
3. registrar essas suposicoes nos artefatos corretos
4. perguntar ao humano apenas quando houver ambiguidade de alto risco, sensivel ou regulatorio

## implementation/ como camada obrigatoria

A partir desta versao da base, `implementation/` deve existir em todo projeto tratado como `recomendado` ou `completo`.

A funcao dessa camada e:

- explicitar a fase ativa
- guiar a LLM na execucao por etapa
- reforcar validacao antes de avancar
- reduzir ambiguidade sobre o proximo passo

Estrutura inicial sugerida:

```text
implementation/
  phase-01-bootstrap.md
  phase-02-first-incremental-capability.md
  phase-03-validation-and-observability.md
```

## Comando unico de primeira execucao

Quando o projeto ja tiver a primeira capacidade incremental implementada, a base recomenda expor um unico comando de onboarding, por exemplo:

```bash
python execution/run_onboarding_flow.py
```

Esse fluxo deve:

- executar a primeira capacidade
- rodar a validacao
- atualizar status
- informar se o sistema esta pronto para abrir API e frontend
