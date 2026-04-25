# Exemplos de Preenchimento do Prompt Mestre

## Objetivo

Este documento traz exemplos prontos de preenchimento do `PROMPT_MESTRE_INICIAL.md` para diferentes tipos de projeto agentico.

A ideia e ajudar a reduzir ambiguidade no momento de iniciar um novo projeto.

## Como usar

Voce pode:

- copiar um exemplo inteiro e adaptar
- misturar campos de exemplos diferentes
- usar os exemplos apenas como referencia para escrever o seu proprio contexto

## Exemplo 1 - Analise de Reviews para E-commerce

- Nome: `ReviewInsight`
- Objetivo: `Criar um sistema agentico que analisa reviews de clientes, identifica temas criticos e sugere acoes para melhorar satisfacao e retencao.`
- Dominio: `e-commerce`
- Usuario ou operacao alvo: `analistas de customer success e gestores de operacao`
- Stack preferida: `Python + FastAPI + PostgreSQL + Qdrant + React`
- Integracoes previstas: `PostgreSQL, Qdrant e importacao de CSV de reviews`
- Restricoes importantes: `responder em portugues, funcionar localmente com Docker e operar em modo somente leitura na base principal`
- Fora de escopo: `nao criar autenticacao, nao fazer deploy cloud e nao integrar com WhatsApp nesta fase`

## Exemplo 2 - Triagem de Tickets de Suporte

- Nome: `SupportTriageAI`
- Objetivo: `Construir um sistema multiagente para classificar tickets de suporte, priorizar urgencia e sugerir resposta inicial com base em contexto historico.`
- Dominio: `atendimento ao cliente`
- Usuario ou operacao alvo: `time de suporte nivel 1`
- Stack preferida: `Python + LangGraph + PostgreSQL + React`
- Integracoes previstas: `Zendesk API, PostgreSQL e Slack`
- Restricoes importantes: `nao responder automaticamente ao cliente sem validacao humana, manter logs de decisao e nao usar dados fora do tenant atual`
- Fora de escopo: `nao integrar voz, nao usar WhatsApp e nao fazer automacao full-autonomous na primeira versao`

## Exemplo 3 - Assistente Financeiro Operacional

- Nome: `FinanceOps Agent`
- Objetivo: `Criar um agente que consolida lancamentos financeiros, detecta inconsistencias e gera relatorio executivo para o time financeiro.`
- Dominio: `financas`
- Usuario ou operacao alvo: `analistas financeiros e controller`
- Stack preferida: `Python + FastAPI + PostgreSQL + Streamlit`
- Integracoes previstas: `ERP interno, planilhas CSV e banco PostgreSQL`
- Restricoes importantes: `nao alterar lancamentos automaticamente, manter trilha de auditoria e mascarar dados sensiveis`
- Fora de escopo: `nao executar pagamento, nao integrar banco externo e nao fazer previsao financeira por ML nesta fase`

## Exemplo 4 - Copiloto para Compliance

- Nome: `Compliance Radar`
- Objetivo: `Construir um sistema agentico que revisa documentos, identifica riscos de compliance e gera resumos com evidencias para revisao humana.`
- Dominio: `compliance`
- Usuario ou operacao alvo: `analistas de compliance e juridico interno`
- Stack preferida: `Python + FastAPI + Qdrant + PostgreSQL`
- Integracoes previstas: `PDFs locais, SharePoint exportado e banco vetorial`
- Restricoes importantes: `nao tomar decisao final automaticamente, citar evidencias e manter sigilo dos documentos processados`
- Fora de escopo: `nao integrar assinatura digital, nao emitir parecer juridico definitivo e nao automatizar aprovacao final`

## Exemplo 5 - Assistente de SDR / Vendas

- Nome: `SalesCopilot`
- Objetivo: `Criar um sistema que analisa leads, prioriza contatos e sugere abordagem comercial com base em historico e perfil do cliente.`
- Dominio: `vendas`
- Usuario ou operacao alvo: `SDRs e gestores comerciais`
- Stack preferida: `Next.js + Supabase + OpenAI API`
- Integracoes previstas: `HubSpot, Supabase e Gmail API`
- Restricoes importantes: `nao enviar emails automaticamente na primeira fase, manter linguagem profissional e registrar a justificativa de cada priorizacao`
- Fora de escopo: `nao integrar WhatsApp, nao automatizar follow-up completo e nao fazer enriquecimento pago de leads`

## Exemplo 6 - DataOps Agent para Qualidade de Pipelines

- Nome: `DataQualityOps`
- Objetivo: `Criar um sistema agentico para monitorar pipelines de dados, detectar falhas, sugerir causa raiz e propor acoes corretivas.`
- Dominio: `DataOps`
- Usuario ou operacao alvo: `engenheiros de dados e equipe de operacoes`
- Stack preferida: `Python + FastAPI + PostgreSQL + Grafana`
- Integracoes previstas: `Airflow, PostgreSQL, logs de pipeline e Slack`
- Restricoes importantes: `nao reexecutar jobs em producao sem aprovacao, manter historico de incidentes e operar com leitura por padrao`
- Fora de escopo: `nao alterar DAGs automaticamente, nao fazer rollback automatico e nao administrar infraestrutura cloud nesta fase`

## Exemplo 7 - Assistente Educacional para Trilhas de Estudo

- Nome: `StudyPath AI`
- Objetivo: `Construir um agente que cria trilhas de estudo personalizadas, acompanha progresso e recomenda proximos passos com base no perfil do aluno.`
- Dominio: `educacao`
- Usuario ou operacao alvo: `alunos e mentores`
- Stack preferida: `Next.js + Supabase + Python`
- Integracoes previstas: `Supabase, arquivos PDF e banco vetorial`
- Restricoes importantes: `responder em portugues, adaptar nivel de linguagem ao perfil do aluno e nunca afirmar aprendizado sem evidencia de progresso`
- Fora de escopo: `nao emitir certificado, nao integrar pagamento e nao substituir o mentor humano`

## Exemplo 8 - Assistente para Contratos e Documentos

- Nome: `ContractLens`
- Objetivo: `Criar um sistema que resume contratos, destaca clausulas sensiveis e sugere pontos de revisao para o time juridico.`
- Dominio: `juridico`
- Usuario ou operacao alvo: `advogados internos e analistas juridicos`
- Stack preferida: `Python + FastAPI + Qdrant + PostgreSQL`
- Integracoes previstas: `PDFs, DOCX e repositorio interno de documentos`
- Restricoes importantes: `nao substituir parecer juridico humano, sempre citar evidencias textuais e tratar documentos como confidenciais`
- Fora de escopo: `nao assinar contratos, nao enviar documentos para terceiros e nao gerar parecer final autonomo`

## Exemplo 9 - Agente de Observabilidade para APIs

- Nome: `APIGuard Agent`
- Objetivo: `Construir um sistema agentico que monitora comportamento de APIs, identifica anomalias e gera diagnosticos acionaveis para engenharia.`
- Dominio: `engenharia de software`
- Usuario ou operacao alvo: `times de plataforma e backend`
- Stack preferida: `Python + FastAPI + Prometheus + PostgreSQL`
- Integracoes previstas: `logs, traces, Prometheus, Grafana e Slack`
- Restricoes importantes: `nao executar mudancas em producao automaticamente, operar com dados observacionais e justificar cada alerta com evidencias`
- Fora de escopo: `nao fazer auto-remediation em producao, nao alterar configuracoes de infraestrutura e nao paginar on-call automaticamente na primeira fase`

## Exemplo 10 - Agente de Conteudo e Calendario Editorial

- Nome: `ContentOps AI`
- Objetivo: `Criar um sistema agentico que organiza ideias de conteudo, prioriza temas e gera propostas de calendario editorial.`
- Dominio: `marketing de conteudo`
- Usuario ou operacao alvo: `time de conteudo e operacao de marketing`
- Stack preferida: `Next.js + Supabase + Python`
- Integracoes previstas: `Google Sheets, Notion e banco local`
- Restricoes importantes: `nao publicar automaticamente, manter coerencia com a linha editorial e registrar racional das prioridades sugeridas`
- Fora de escopo: `nao integrar redes sociais diretamente, nao gerar criativos finais e nao fazer automacao de aprovacao`

## Regra pratica

Se voce ficar em duvida sobre como preencher, use esta ordem:

1. escreva primeiro o objetivo real do sistema
2. depois o dominio
3. depois quem usa ou opera
4. depois a stack e integracoes
5. por fim, seja rigoroso em restricoes e fora de escopo

## Conclusao

Quanto mais claro esse preenchimento inicial, menor a chance de a LLM improvisar arquitetura, stack ou escopo de forma errada.

Em uma frase:

`O preenchimento do prompt mestre define a qualidade da primeira leitura que a LLM fara do projeto.`

## Como esse preenchimento influencia a spec/

O preenchimento do prompt mestre nao define apenas o README ou o bootstrap. Ele tambem orienta a primeira versao de `spec/`.

Em termos praticos:

- `Objetivo` influencia `02-define.md`
- `Dominio` influencia `directives/` e tambem os requisitos e edge cases da `spec/`
- `Usuario ou operacao alvo` influencia os criterios de aceitacao e o formato de saida
- `Stack preferida` influencia `03-design.md`
- `Integracoes previstas` influencia `03-design.md` e `04-build.md`
- `Restricoes importantes` influencia `02-define.md` e `05-validate.md`
- `Fora de escopo` ajuda a limitar `02-define.md` e evitar expansao indevida do `04-build.md`

Leitura pratica:

- `01-brainstorm.md` recebe alternativas e trade-offs
- `02-define.md` recebe objetivo, escopo, restricoes e criterios
- `03-design.md` recebe arquitetura, integracoes e componentes
- `04-build.md` recebe a primeira capacidade prioritaria a implementar
- `05-validate.md` recebe os gates e checks da fase

Em uma frase:

`Quanto melhor o preenchimento inicial, mais limpa e mais util tende a nascer a spec/ do projeto.`


## Como preencher estrategia inicial de modelos por papel

Use esta secao para indicar, desde o inicio, como o sistema deve distribuir custo, qualidade e latencia entre os papeis do fluxo agentico.

### Forma generica recomendada

```text
- Estrategia inicial de modelos por papel:
  - Orchestrator: modelo robusto
  - Planner: modelo medio ou robusto
  - ExecutionAgent: modelo medio
  - Validator: modelo medio ou robusto
  - Reporter: modelo economico ou medio
```

### Forma concreta opcional

Use nomes de modelos reais apenas como exemplo ou quando o projeto ja souber qual provider usara.

```text
- Estrategia inicial de modelos por papel:
  - Orchestrator: Claude Opus
  - ExecutionAgent: Claude Haiku
  - Validator: GPT-5
  - Reporter: GPT-5-mini
```

## Exemplo adicional

```text
- Nome: `FinanceOps Agent`
- Objetivo: `Criar um agente que consolida lancamentos financeiros, detecta inconsistencias e gera relatorio executivo para o time financeiro.`
- Dominio: `financas`
- Usuario ou operacao alvo: `analistas financeiros e controller`
- Stack preferida: `Python + FastAPI + PostgreSQL + Streamlit`
- Integracoes previstas: `ERP interno, planilhas CSV e banco PostgreSQL`
- Restricoes importantes: `nao alterar lancamentos automaticamente, manter trilha de auditoria e mascarar dados sensiveis`
- Estrategia inicial de modelos por papel:
  - Orchestrator: modelo robusto
  - ExecutionAgent: modelo medio
  - Validator: modelo medio ou robusto
  - Reporter: modelo economico ou medio
- Fora de escopo: `nao executar pagamento, nao integrar banco externo e nao fazer previsao financeira por ML nesta fase`
```
