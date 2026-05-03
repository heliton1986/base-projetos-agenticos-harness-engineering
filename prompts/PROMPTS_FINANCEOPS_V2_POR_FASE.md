# Prompts por Fase - FinanceOps v2

## Objetivo

Esta sequencia adapta `PROMPT_MESTRE_INICIAL.md` e `PROMPTS_POR_FASE.md` especificamente para o `financeops-v2`.

Ela existe para evitar recriacao one-shot e para conduzir o projeto como validacao real da base atual.

## Ordem de uso

1. usar `PROMPT_FINANCEOPS_V2_CANONICO.md` para a Fase 1
2. aprovar a definicao
3. seguir os prompts abaixo em ordem
4. nao pular fase sem gate aprovado

---

## Fase 1 - Definicao

Use diretamente:

- `prompts/PROMPT_FINANCEOPS_V2_CANONICO.md`

Resultado esperado:

- objetivo refinado
- escopo inicial
- estrutura proposta
- estrategia de agentes
- separacao entre `contracts/*.md` e `src/contracts/*.py`
- divergencias esperadas em relacao ao `projeto-teste-financeops-agent`

---

## Fase 2 - Bootstrap

Use este prompt depois de aprovar a definicao.

```text
Com base na definicao aprovada, crie o bootstrap inicial do projeto em:

`/var/home/heliton/Documents/Projetos/harness-engineering/financeops-v2`

Gere primeiro, usando estritamente os templates da base:

- README.md
- AGENTS.md
- directives/
- spec/
- contracts/
- src/contracts/
- implementation/
- execution/
- tests/
- progress/
- .env.example
- model_routing.yaml
- requirements.txt

Regras especificas deste bootstrap:

- usar `contracts/*.md` para task contracts, contratos documentais e invariantes de fase/capacidade
- usar `src/contracts/*.py` para contratos executaveis tipados usados em runtime
- como o projeto e multi-agent, `implementation/` e obrigatorio desde o bootstrap
- cada arquivo em `implementation/` deve seguir o template de fase; titulo + 1 frase nao bastam
- criar `progress/PROGRESS.md` e `progress/VALIDATION_STATUS.md` ja na primeira entrega
- preparar o projeto para testes offline antes de qualquer migracao futura para framework

No bootstrap, deixe explicito:

- papel de `OrchestratorAgent`, `IngestionAgent`, `DetectorAgent`, `ValidatorAgent`, `ReporterAgent`
- handoff esperado entre os agentes
- quais agentes usam LLM e quais sao determinísticos
- quais contratos minimos precisam existir antes da primeira capacidade
- quais gates serao obrigatorios entre fases
- qual template da base foi usado para cada artefato criado

Nao implemente ainda o sistema inteiro.
Foque no bootstrap estrutural correto.

Ao final, responda no chat com um bloco estruturado contendo:

- resumo do que foi criado
- estrutura de pastas
- contratos minimos propostos
- fases registradas em `implementation/`
- status do bootstrap: `aprovado` ou `requer ajuste`
```

---

## Fase 3 - Validacao da Base

Use este prompt depois do bootstrap.

```text
Revise o bootstrap criado em:

`/var/home/heliton/Documents/Projetos/harness-engineering/financeops-v2`

Analise se a base ja esta apta para comecar implementacao incremental com boa disciplina de harness.

Verifique:

- clareza do README.md
- qualidade do AGENTS.md
- qualidade das directives/
- qualidade da spec/
- clareza de `implementation/`
- se `implementation/` contem runbooks completos ou apenas placeholders
- separacao correta entre `contracts/*.md` e `src/contracts/*.py`
- clareza de handoff entre agentes
- estrategia de modelos em `model_routing.yaml`
- existencia de `progress/`
- adequacao dos testes planejados para rodar offline
- criterios de pronto por fase
- divergencias explicitadas em relacao ao `projeto-teste-financeops-agent`

Use o validador da base como parte da revisao, se ja fizer sentido.

Nao implemente ainda.

Entregue:

- o que esta aprovado
- o que esta faltando
- lacunas importantes
- status final da base: `aprovada` ou `reprovada`
- se aprovada, sinalize explicitamente que a proxima fase deve continuar para a primeira capacidade incremental minima
```

---

## Fase 4 - Primeira Capacidade Incremental Minima

Use este prompt apenas com a base aprovada.

```text
Agora implemente apenas a primeira capacidade incremental minima do `financeops-v2`.

Capacidade alvo desta fase:

- ingestao de CSV financeiro local
- normalizacao dos lancamentos
- validacao contratual do resultado da ingestao
- relatorio minimo de ingestao aprovado/rejeitado

Respeite:

- README.md
- AGENTS.md
- directives/
- spec/
- implementation/
- contracts/
- src/contracts/

Regras:

- nao implemente deteccao semantica por LLM ainda
- nao implemente API ou UI ainda
- nao conectar PostgreSQL real nesta fase
- tudo precisa rodar offline
- `ValidatorAgent` deve validar a saida do `IngestionAgent` antes do proximo passo
- criar ou ajustar testes offline para a capacidade implementada
- registrar progresso em `progress/`

Ao final, responda no chat com um bloco estruturado contendo:

- o que foi implementado
- quais contratos foram criados ou refinados
- como validar com `pytest`
- resultado dos gates
- o que ainda nao foi feito
- proxima capacidade recomendada
```

---

## Fase 5 - Deteccao Deterministica

Use este prompt depois da Fase 4 aprovada.

```text
Agora implemente apenas a proxima capacidade prioritaria do `financeops-v2`:

- deteccao deterministica de inconsistencias financeiras

Escopo desta fase:

- duplicata suspeita
- valor alto suspeito
- descricao suspeita
- regras de negocio fixas documentadas em `directives/`
- validacao contratual pelo `ValidatorAgent`
- testes offline cobrindo apenas regras fixas

Ainda nao implemente:

- analise semantica por LLM
- FastAPI
- Streamlit
- persistencia real em PostgreSQL

Ao final, responda no chat com um bloco estruturado contendo:

- mostre quais regras foram implementadas
- quais contratos de deteccao foram criados ou ajustados
- como os testes validam a fase
- se a fase foi aprovada ou precisa de correcao
- atualize `progress/PROGRESS.md` e `progress/VALIDATION_STATUS.md`
```

---

## Fase 6 - Deteccao Semantica Controlada por LLM

Use este prompt apenas depois da fase deterministica aprovada.

```text
Agora expanda o `DetectorAgent` com analise semantica controlada por LLM apenas para os casos que sobraram apos as regras fixas.

Regras obrigatorias:

- mascarar dados sensiveis antes do envio ao modelo
- manter regras fixas como primeira camada obrigatoria
- registrar modelo usado no fluxo e no resultado
- separar claramente saida deterministica de saida inferida por LLM
- `ValidatorAgent` continua validando a saida final
- criar fallback para quando o LLM falhar ou retornar output invalido
- testes unitarios continuam offline e devem cobrir apenas regras fixas e parser deterministico

Nao implemente ainda:

- API FastAPI
- Streamlit
- persistencia real completa

Ao final, responda no chat com um bloco estruturado contendo:

- explique como o LLM entra no fluxo
- quais guardrails foram adicionados
- quais contratos foram atualizados
- quais testes continuam offline
- qual e o status da fase
```

---

## Fase 7 - Relatorio Executivo

Use este prompt quando a deteccao estiver aprovada.

```text
Implemente agora a capacidade de relatorio executivo do `financeops-v2`.

Escopo:

- `ReporterAgent` consolida totais
- sumariza inconsistencias por tipo e severidade
- gera status final do processamento
- produz saida estruturada pronta para futura API/UI
- `ValidatorAgent` valida o relatorio final

Regras:

- nao adicionar UI ainda, a menos que isso ja esteja aprovado
- relatorio deve ser deterministico
- contratos de saida devem existir em `src/contracts/*.py`
- o contrato documental correspondente deve existir em `contracts/*.md`
- testes offline devem cobrir o relatorio final

Ao final, responda no chat com um bloco estruturado contendo:

- mostrar o schema do relatorio final
- mostrar como validar
- mostrar se a fase foi aprovada
- registrar evidencias em `progress/`
```

---

## Fase 8 - FastAPI e Streamlit com Verificacao Live

Use este prompt apenas quando o fluxo central estiver pronto.

```text
Agora exponha o fluxo aprovado do `financeops-v2` via:

- FastAPI para processamento HTTP
- Streamlit para interface operacional

Regras obrigatorias:

- usar os templates da base para FastAPI e Streamlit
- manter o mesmo fluxo de contratos e gates do core do sistema
- nao duplicar regra de negocio na camada web
- subir os servicos localmente
- executar verificacao live obrigatoria com golden path real
- registrar no chat e em `progress/`:
  - porta usada
  - rota ou tela validada
  - resultado observado
  - modelo chamado, se houver LLM no fluxo

So declare esta fase como concluida se:

- os testes offline continuarem passando
- a verificacao live for executada sem erro
- houver evidencia textual clara da verificacao live
```

---

## Regra pratica para esta sequencia

- Fase 1 define
- Fase 2 estrutura
- Fase 3 aprova a base
- Fases 4 a 7 constroem o core por camadas
- Fase 8 expoe o core por API/UI com verificacao live

Nao inverter esta ordem.
