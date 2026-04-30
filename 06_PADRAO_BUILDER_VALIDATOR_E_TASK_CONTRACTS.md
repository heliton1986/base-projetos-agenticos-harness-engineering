# Padrao Builder, Validator e Task Contracts

## Objetivo

Este documento formaliza uma parte central da visao de `Harness Engineering`: separar implementacao, validacao e aprovacao por meio de contratos de tarefa e gates explicitos.

Ele complementa a base existente, principalmente no lado de:

- confiabilidade operacional
- task contracts
- builder vs validator
- loop de correcao
- evidencias de validacao

## Problema que este padrao resolve

Um erro comum em sistemas agenticos e deixar o mesmo agente:

- implementar
- julgar a propria implementacao
- declarar que esta pronto

Esse modelo tende a gerar:

- vitoria prematura
- validacao superficial
- regressao acumulada
- entregas sem evidencia suficiente

A ideia deste padrao e reduzir esse risco.

## Estrutura conceitual

O padrao se apoia em tres papeis logicos.

### 1. Builder

Responsavel por:

- implementar
- ajustar
- produzir artefatos
- corrigir falhas apontadas

### 2. Validator

Responsavel por:

- verificar criterios acordados
- executar checks e sensores
- identificar gaps
- reprovar ou aprovar tecnicamente a entrega

### 3. Orchestrator

Responsavel por:

- decidir o que vai para construcao
- encaminhar para validacao
- decidir se volta para correcao
- aprovar encerramento da fase

## O que e um Task Contract

Um `task contract` e o acordo explicito sobre o que precisa ser entregue em uma tarefa ou fase.

Ele deve reduzir ambiguidade para:

- quem constrói
- quem valida
- quem aprova

## Estrutura minima de um Task Contract

Um contrato de tarefa deve responder pelo menos:

- qual o objetivo da tarefa
- qual o escopo
- o que esta fora de escopo
- quais arquivos ou componentes podem ser tocados
- quais outputs sao esperados
- quais validacoes sao obrigatorias
- quais evidencias precisam existir
- o que significa pronto

## Contrato acordado antes da execucao

Um erro comum: o Validator so descobre o que precisa testar depois que o Builder terminou.

O padrao correto: **Builder e Validator concordam no contrato antes de qualquer execucao**.

Sequencia correta:

1. Orchestrator define o task contract
2. Builder le o contrato e confirma o que vai entregar
3. Validator le o contrato e confirma o que vai checar
4. Builder executa
5. Validator verifica item a item do contrato acordado
6. Orchestrator decide aprovacao

Por que isso importa:

- Validator com lista acordada nao sugere coisas fora do escopo
- Builder nao declara pronto baseado em criterios diferentes dos que serao verificados
- Loop nao entra em ciclo infinito por desacordo sobre o que significa pronto

Sem acordo previo, o Validator tende a incluir novos requisitos durante a verificacao, forçando o Builder a implementar coisas nao planejadas. O sistema entra em loop.

## Template sugerido

```text
Task Contract

- Objetivo:
- Escopo:
- Fora de escopo:
- Artefatos afetados:
- Output esperado:
- Validacoes obrigatorias:
- Evidencias exigidas:
- Criterio de pronto:
```

## Exemplo resumido

```text
Task Contract

- Objetivo: implementar a primeira rota de consulta de pedidos
- Escopo: endpoint de leitura + validacao minima + teste basico
- Fora de escopo: autenticacao e dashboard
- Artefatos afetados: api/, tests/, docs/
- Output esperado: endpoint funcional e resposta estruturada
- Validacoes obrigatorias: teste de rota + lint + typecheck
- Evidencias exigidas: comando executado e resultado verde
- Criterio de pronto: endpoint funcionando e validacoes minimas aprovadas
```

## Gates de validacao

Um gate e um ponto explicito de aprovacao antes da proxima etapa.

Exemplos de gates:

- gate de bootstrap
- gate de implementacao da fase
- gate de validacao funcional
- gate de qualidade minima
- gate de entrega final

## Regra pratica

`Uma fase nao deve avancar se o gate atual nao estiver aprovado.`

## Evidencias de validacao

Validacao forte nao deve depender apenas de texto declarativo.

Sempre que possivel, a entrega deve apresentar evidencias como:

- testes passando
- lint sem erro
- typecheck sem erro
- evals minimos aprovados
- saida esperada gerada
- contrato atendido item a item

## Loop de correcao

O fluxo recomendado e:

1. Builder implementa
2. Validator verifica
3. Se falhar, registrar motivo
4. Builder corrige
5. Validator reavalia
6. Orchestrator decide aprovacao

## O que o Validator deve checar

O validator deve responder pelo menos:

- o escopo foi respeitado?
- a saida pedida existe?
- os gates obrigatorios passaram?
- houve quebra de restricoes?
- a tarefa foi realmente concluida ou apenas parcialmente adiantada?

## O que o Builder nao deve fazer

O builder nao deve:

- declarar pronto sem validacao
- expandir escopo por conta propria
- ignorar restricoes do task contract
- substituir evidencias por opiniao

## Relacao com outros artefatos da base

### README.md

- contextualiza o projeto
- nao substitui task contract

### directives/

- define regras operacionais do dominio
- nao substitui criterios de aceite da tarefa

### spec/

- organiza a fase e o plano
- e o melhor lugar para desdobrar task contracts de fase

### AGENTS.md

- define como os agentes operam
- pode incorporar o padrao builder/validator como politica do projeto

### FRONTEND_OBSERVAVEL_PARA_AGENTES.md

- pode exibir visualmente:
  - em execucao
  - validando
  - falhou
  - em correcao
  - validado

## Onde esse padrao pode aparecer no projeto

### Em spec/

Exemplo:

```text
spec/
  04-build.md
  05-validate.md
```

### Em contracts/

Exemplo:

```text
contracts/
  feature-01.md
  feature-02.md
```

### Em AGENTS.md

Como regra operacional de fluxo.

## Quando usar a versao minima deste padrao

Mesmo em projeto pequeno, faz sentido pelo menos ter:

- objetivo da tarefa
- escopo
- validacoes obrigatorias
- criterio de pronto

## Quando usar a versao forte

Use com mais rigor quando:

- ha multiplos agentes
- ha handoffs complexos
- ha risco de regressao
- o projeto vai durar varias sessoes
- a entrega precisa de auditabilidade

## Conclusao

Este padrao transforma a validacao de algo implicito em algo estrutural.

Em uma frase:

`Builder constrói, Validator verifica, Orchestrator aprova; o task contract impede que o sistema avance no escuro.`

## Parser de Output LLM — padrao robusto

### Problema

LLMs retornam texto livre. Mesmo com instrucao de formato (`ID|tipo|descricao`), o modelo pode envolver os valores em markdown (`**UUID**`, `` `tipo` ``) ou adicionar texto antes/apos a linha. Parser baseado em `split("|")` ou linha exata quebra nesses casos.

### Solucao validada (FinanceOps v2)

**Contrato de prompt:** pedir formato `UUID|tipo|descricao_curta` — sem markdown, sem json, sem wrapper.

```python
prompt = (
    "...contexto...\n"
    "Responda apenas se tiver confianca alta. Formato: ID|tipo|descricao_curta\n\n"
    f"{linhas_dos_lancamentos}"
)
```

**Parser com regex UUID como ancora:**

```python
import re

uuid_pattern = re.compile(
    r"([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})\|([^|]+)\|(.+)",
    re.IGNORECASE,
)

for linha in texto.strip().splitlines():
    match = uuid_pattern.search(linha)  # search, nao match — ignora prefixo na linha
    if match:
        lid = match.group(1)
        tipo = match.group(2).strip()
        descricao = match.group(3).strip().strip("*`")  # remove markdown residual
```

Usar `search()` em vez de `match()` — captura UUID mesmo se houver texto antes na linha (ex: `- **uuid|tipo|desc**`).

**Contrato Literal com fallback:**

```python
TIPOS_VALIDOS = {
    "duplicata_suspeita", "campo_ausente", "formato_invalido",
    "valor_alto_suspeito", "valor_irrisorio_suspeito",
    "descricao_suspeita", "centro_custo_desconhecido", "inconsistencia_semantica",
}

tipo_normalizado = re.sub(r"[^a-zA-Z0-9_]", "_", tipo).strip("_")
tipo_limpo = tipo_normalizado if tipo_normalizado in TIPOS_VALIDOS else "inconsistencia_semantica"
```

Regra: normalizar caracteres estranhos primeiro (`re.sub`), depois checar contra `TIPOS_VALIDOS`. Tipo desconhecido → tipo generico (`inconsistencia_semantica`). Nunca rejeitar linha por tipo invalido — perda silenciosa de dados.

### Quando aplicar

- Qualquer agente que parseia output textual de LLM com campo tipado
- Output tem formato `chave|tipo|descricao` ou similar
- Tipo deve mapear para `Literal` Python ou enum do contrato Pydantic

### Regras

1. Ancora no campo mais estruturado (UUID, ID numerico) — nao no inicio da linha
2. `search()` > `match()` — robusto a prefixos markdown
3. Strip markdown (`` ` ``, `*`) no campo descricao
4. Normalizar tipo antes de validar contra set
5. Fallback obrigatorio — nunca deixar tipo invalido propagar nem descartar linha

## Referencias

Os padroes descritos aqui sao agnósticos de modelo e provedor. As fontes abaixo os nomearam e documentaram na literatura de sistemas agenticos.

- **Anthropic — Building effective agents** (2024): descreve o padrao `evaluator-optimizer` — um agente gera output, outro avalia e retroalimenta o loop de correcao. Equivalente direto ao Builder/Validator deste documento.
  Disponivel em: https://www.anthropic.com/research/building-effective-agents

- **Yao et al. — ReAct: Synergizing Reasoning and Acting in Language Models** (2022): fundamento academico de agentes que intercalam raciocinio e acao. A ideia de loop explicito (agir → observar → corrigir) sustenta o padrao de loop de correcao descrito aqui.
  Disponivel em: https://arxiv.org/abs/2210.03629

- **Chase — Cognitive Architectures for Language Agents** (2023): taxonomia de arquiteturas agênticas incluindo padroes de reflexao e autocorrecao alinhados ao loop Builder/Validator.
  Disponivel em: https://arxiv.org/abs/2309.02427
