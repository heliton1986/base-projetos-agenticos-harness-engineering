# Spec 03 — Design: Issue Triage Agent

## Arquitetura

```
IssueInput (texto livre)
        |
        v
[OrchestratorAgent]          # sem LLM, logica deterministica
        |
        v
[ClassifierAgent]            # LLM: claude-sonnet-4-6
        |
        v
[ValidatorAgent]             # Pydantic + regras de negocio
        |
    valido? ---nao---> loop (max 3x, contexto do erro incluido)
        |
       sim
        |
        v
[ReporterAgent]              # sem LLM, formatacao deterministica
        |
        v
IssueReport (saida final)
```

## Fluxo detalhado

```
1. OrchestratorAgent recebe IssueInput
2. Aciona ClassifierAgent com texto da issue
3. ClassifierAgent monta prompt com:
   - texto da issue
   - categorias validas (de directives/triagem_rules.md)
   - severidades validas
   - instrucao de saida JSON estruturada
4. LLM retorna JSON → parse para IssueClassification
5. ValidatorAgent valida:
   a. Schema Pydantic
   b. Regras de negocio (ex: critica → bug|seguranca)
6. Se invalido E tentativas < 3:
   - Acionar ClassifierAgent novamente com contexto do erro
   - Voltar ao passo 4
7. Se invalido E tentativas == 3:
   - Retornar IssueReport com status="falhou"
8. Se valido:
   - ReporterAgent gera IssueReport com status="aprovado"
9. Retornar IssueReport
```

## Prompt do ClassifierAgent

```
Voce e um agente de triagem de issues de software.

Classifique a issue abaixo seguindo EXATAMENTE estas regras:

SEVERIDADES VALIDAS: critica, alta, media, baixa
CATEGORIAS VALIDAS: bug, feature, performance, seguranca, documentacao, duvida

REGRAS:
- severidade "critica" apenas para categoria "bug" ou "seguranca"
- categoria "duvida" tem severidade maxima "baixa"
- categoria "feature" tem severidade maxima "media"
- justificativa obrigatoria (minimo 20 caracteres)
- confianca: "alta" se texto claro, "media" se ambiguo, "baixa" se muito vago

ISSUE:
{texto_da_issue}

{contexto_de_erro_se_reprocessando}

Retorne APENAS JSON valido no formato:
{
  "severidade": "...",
  "categoria": "...",
  "justificativa": "...",
  "confianca": "..."
}
```

## Gates de aprovacao

| Gate | Criterio | Verificado por |
|------|---------|---------------|
| Gate 1 — Ambiente | API key presente, anthropic importavel, pydantic importavel | `run_onboarding_flow.py` |
| Gate 2 — Classificacao | `IssueClassification` valida (schema + regras de negocio) | `ValidatorAgent` |
| Gate 3 — Report | `IssueReport` com todos os campos, status correto | `ReporterAgent` + assert |

## Modelos por agente

Ver `model_routing.yaml`.

## Decisoes de design

| Decisao | Alternativa rejeitada | Razao |
|---------|----------------------|-------|
| JSON em disco como persistencia | PostgreSQL | Sem dependencias externas no canonico |
| Python puro sem framework | LangChain | Transparencia total do fluxo |
| Loop de correcao max 3x | Sem limite | Evitar loop infinito em producao |
| Prompt com contexto de erro | Prompt identico no retry | Aumenta chance de correcao no reprocessamento |
