# Prompt Novo Projeto — Execucao Autonoma

## Objetivo

Prompt de entrada para criacao de projeto agentico completo com execucao autonoma.

Diferente de `PROMPT_MESTRE_INICIAL.md` (que para apos definicao e aguarda aprovacao), este prompt executa o projeto inteiro de forma autonoma — do brief aos testes passando — parando apenas em bloqueios reais.

## Quando usar

Use quando quiser que a LLM crie o projeto do zero sem aprovacao a cada fase.
Indicado para projetos com brief claro e dominio ja conhecido.

## Como usar

Cole o texto abaixo como prompt, substituindo os campos marcados com `[...]`.

---

## Template

```
Leia antes de qualquer acao:
- [BASE_PATH]/AGENTS.md
- [BASE_PATH]/06_PADRAO_BUILDER_VALIDATOR_E_TASK_CONTRACTS.md
- [BASE_PATH]/10_ESTRATEGIA_DE_MODELOS_PARA_AGENTES.md
- [BASE_PATH]/templates/TEMPLATE_AGENTS.md
- [BASE_PATH]/templates/TEMPLATE_TASK_CONTRACT.md
- [BASE_PATH]/templates/TEMPLATE_TESTS.md
- [BASE_PATH]/templates/TEMPLATE_CI.md

O projeto sera criado em: [CAMINHO_DO_PROJETO]

Brief do projeto:

- Nome: [NOME]
- Objetivo: [OBJETIVO]
- Dominio: [DOMINIO]
- Usuario ou operacao alvo: [USUARIO_ALVO]
- Stack preferida: [STACK]
- Integracoes previstas: [INTEGRACOES]
- Restricoes importantes: [RESTRICOES]
- Fora de escopo: [FORA_DE_ESCOPO]

---

## Modo de operacao: AUTONOMO

Execute o projeto completo sem pedir aprovacao a cada fase.

Pare apenas em:
- credencial ou variavel de ambiente ausente que bloqueie execucao
- ambiguidade de regra de negocio ou regulatoria que impacta o contrato de dados
- risco de escrita indevida em fonte sensivel

Em todos os outros casos: aja, corrija se necessario, reporte resultado.

---

## Etapa 0 — Q&A Inicial (obrigatoria)

Antes de gerar qualquer arquivo, faca no maximo 5 perguntas.

Criterios para perguntar:
- a resposta impacta diretamente o contrato Pydantic ou regra de negocio
- a informacao nao pode ser inferida com segurança do brief
- a ambiguidade geraria retrabalho de estrutura, nao so de detalhe

Nao perguntar sobre:
- preferencias esteticas
- nomes de arquivo
- detalhes de implementacao que podem ser decididos depois
- qualquer coisa ja respondida no brief

Formato:
[Q&A Inicial]
Antes de gerar, X perguntas sobre pontos que impactam os contratos:

1. [pergunta direta e especifica]
2. [pergunta direta e especifica]
...

Aguardando respostas para continuar.

---

## Etapa 1 — Estrutura

Gerar: README.md, AGENTS.md, spec/, directives/domain.md, directives/business-rules.md, .env.example, progress/PROGRESS.md, progress/VALIDATION_STATUS.md

Usar templates da base para cada artefato.

Narrar antes de executar:
[Fase 1 — Estrutura] iniciando: README, AGENTS.md, spec/, directives/

Apos gerar, executar Gate 1.

### Gate 1 — Estrutura

Verificar:
- todos os arquivos foram criados
- AGENTS.md tem: protocolo de execucao, ValidatorAgent, testes offline, CI
- directives/business-rules.md tem pelo menos 3 regras de negocio do dominio
- spec/ tem pelo menos: 01-overview, 02-agents, 03-contracts, 04-phases, 05-validate

Se falhar: corrigir e reverificar. Nao avancar com gate reprovado.

Reportar no chat:
[Gate 1 — Estrutura] APROVADO ✓
| Artefato                     | Status  |
|------------------------------|---------|
| README.md                    | criado  |
| AGENTS.md                    | criado  |
| spec/ (N arquivos)           | criado  |
| directives/domain.md         | criado  |
| directives/business-rules.md | criado  |
| .env.example                 | criado  |
| progress/PROGRESS.md         | criado  |

---

## Etapa 2 — Contratos Pydantic

Gerar: src/contracts/ com um modelo por entidade do dominio.

Regras:
- Input do primeiro agente
- Output de cada agente intermediario
- Output final (relatorio ou resultado)
- Tipos com Literal onde ha valores fixos — nunca str livre para campo tipado
- Campos obrigatorios sem default quando a ausencia e erro de negocio

Narrar antes:
[Fase 2 — Contratos] definindo Pydantic: [lista dos contratos]

### Gate 2 — Contratos

Verificar:
- python -c "from src.contracts import *" sem erro
- cada contrato tem pelo menos 1 validacao alem de tipo (Literal, validator, min_length, etc)
- nenhum campo tipado usa str puro onde deveria ser Literal ou enum

Reportar no chat:
[Gate 2 — Contratos] APROVADO ✓
| Contrato   | Campos principais | Validacao chave |
|------------|-------------------|-----------------|
| [nome]     | [campos]          | [regra]         |

---

## Etapa 3 — Agentes

Implementar em src/agents/:
- IngestionAgent (ou equivalente de entrada) — sem LLM
- Agente de dominio (logica de negocio: regras fixas primeiro, LLM apenas para o que regra fixa nao cobre)
- ReporterAgent (ou equivalente de saida) — sem LLM se possivel
- ValidatorAgent — validacao Pydantic deterministica, sem LLM
- run_flow.py em src/ — orquestra os agentes em sequencia com _validar_contrato() entre cada um

Regras dos agentes:
- Regras fixas sempre antes do LLM — o que pode ser detectado deterministicamente nao vai para o LLM
- LLM apenas para analise semantica ou classificacao subjetiva
- Parser de output LLM: regex com ancora no campo mais estruturado (UUID, ID), search() nao match(), strip markdown, Literal fallback obrigatorio
- Modelo por papel: definir em model_routing.yaml antes de codar

Narrar antes:
[Fase 3 — Agentes] implementando: [lista dos agentes com responsabilidade e LLM sim/nao]

### Gate 3 — Agentes

Verificar:
- python -c "from src.agents import *" sem erro
- run_flow.py executa sem excecao com fixture minima (CSV mock ou equivalente)
- ValidatorAgent rejeita corretamente instancia invalida (testar inline)
- audit_log recebe entrada para cada agente executado

Reportar no chat:
[Gate 3 — Agentes] APROVADO ✓
| Agente         | Responsabilidade        | LLM?              |
|----------------|-------------------------|-------------------|
| [nome]         | [o que faz]             | [Sim/Nao/modelo]  |

---

## Etapa 4 — Testes

Gerar tests/ com testes offline: sem LLM real, sem DB real, sem API externa.

Regras:
- test_ingestion: fixture com arquivo temporario (tmp_path), testa normalizacao
- test_[dominio]: testa regras fixas via metodos internos, instanciar agente com __new__ para evitar __init__ que exige API key
- test_validator: testa contrato valido e invalido, verifica que invalido levanta excecao
- test_reporter: testa geracao de relatorio com fixture de inconsistencias

Narrar antes:
[Fase 4 — Testes] gerando testes offline para: [lista das suites]

### Gate 4 — Testes

Executar:
pytest tests/ -v --cov=src --cov-report=term

Criterios de aprovacao:
- 100% dos testes passando
- coverage >= 80% em src/ (excluindo src/db/ se existir)
- tempo de execucao < 10s (testes offline devem ser rapidos)

Se falhar:
- mostrar erro exato no chat
- corrigir
- reexecutar
- nunca avancar com teste falhando

Reportar no chat:
[Gate 4 — Testes] APROVADO ✓
| Suite           | Testes | Status |
|-----------------|--------|--------|
| test_ingestion  | N      | PASS   |
| test_[dominio]  | N      | PASS   |
| test_validator  | N      | PASS   |
| test_reporter   | N      | PASS   |
N/N testes · coverage X% · tempo Xs

---

## Etapa 5 — CI

Gerar:
- .github/workflows/tests.yml — roda pytest a cada push e PR, bloqueia merge se falhar
- .coveragerc — exclui src/db/ (requer DB real), define source = src
- adicionar pytest>=8.0.0 e pytest-cov>=5.0.0 ao requirements.txt se ainda nao existirem
- .gitignore — incluir .coverage, htmlcov/, .pytest_cache/

Usar TEMPLATE_CI.md da base.

Narrar antes:
[Fase 5 — CI] configurando GitHub Actions + .coveragerc

### Gate 5 — CI

Verificar:
- .github/workflows/tests.yml e YAML valido (python -c "import yaml; yaml.safe_load(open('.github/workflows/tests.yml'))")
- coverage minimo configurado no workflow
- .coveragerc presente e excluindo diretorios corretos
- .gitignore atualizado

Reportar no chat:
[Gate 5 — CI] APROVADO ✓
| Artefato                       | Regra configurada           |
|--------------------------------|-----------------------------|
| .github/workflows/tests.yml    | pytest a cada push/PR       |
| .coveragerc                    | source=src, exclui src/db/  |
| .gitignore                     | .coverage, htmlcov/         |

---

## Encerramento

Atualizar progress/PROGRESS.md e progress/VALIDATION_STATUS.md com estado final.

Reportar no chat tabela de estado final:

[NOME_DO_PROJETO] PRONTO ✓
| Componente    | Status     | Detalhe                      |
|---------------|------------|------------------------------|
| Estrutura     | APROVADO   | README, AGENTS.md, spec/     |
| Contratos     | APROVADO   | N contratos Pydantic         |
| Agentes       | APROVADO   | N agentes implementados      |
| Testes        | APROVADO   | N/N · coverage X%            |
| CI            | APROVADO   | GitHub Actions configurado   |

Em seguida, oferecer proximos passos com base no que foi construido.
Nao oferecer opcao generica — cada opcao deve nomear o que sera feito e onde rodara.

Exemplo de formato:
Proximos passos:
A) FastAPI   — endpoint POST /[rota] para testar [operacao] no localhost:8000
B) Streamlit — upload [input] + visualizar [output] + download [formato]
C) CrewAI    — especializar [AgenteX] e [AgenteY] como workers com handoff via task_callback
D) Encerrar — projeto pronto para evoluir

Aguardar escolha do usuario antes de continuar.
```

---

## Diferenca em relacao ao PROMPT_MESTRE_INICIAL.md

| | PROMPT_MESTRE_INICIAL | PROMPT_NOVO_PROJETO |
|--|----------------------|---------------------|
| Para apos definicao | Sim — aguarda aprovacao | Nao — executa tudo |
| Gates por fase | Sugeridos | Embutidos e obrigatorios |
| Interacao humana | Entre todas as fases | Apenas em bloqueio real |
| Q&A inicial | Nao | Sim — max 5 perguntas |
| Oferta de proximo passo | Nao | Sim — opcoes concretas ao final |
| Indicado para | Projetos novos com dominio a explorar | Projetos com brief claro e dominio conhecido |
