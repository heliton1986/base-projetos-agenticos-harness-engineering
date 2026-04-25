# Model Routing — Quick Reference

## Regra principal

**LLM apenas onde linguagem natural agrega valor.**
Logica financeira, validacao, agregacao, roteamento = deterministica, sem LLM.

## Criterios de decisao

| Pergunta | LLM | Sem LLM |
|----------|-----|---------|
| Precisa gerar texto narrativo? | Sim | — |
| Precisa interpretar linguagem ambigua? | Sim | — |
| E logica calculavel deterministicamente? | — | Sim |
| E validacao de schema ou tipo? | — | Sim |
| E agregacao ou query de dados? | — | Sim |
| E roteamento de fluxo? | — | Sim |

## Template de tabela por projeto

```markdown
| Agente | Modelo | Justificativa |
|--------|--------|--------------|
| ReportAgent | claude-sonnet-4-6 | Sintese narrativa executiva |
| OrchestratorAgent | claude-sonnet-4-6 | Interpretacao de intencao do usuario |
| IngestAgent | Sem LLM | Validacao e normalizacao deterministica |
| ConsolidationAgent | Sem LLM | Agregacao SQL deterministica |
| InconsistencyAgent | Sem LLM | Regras de deteccao deterministicas |
| AuditAgent | Sem LLM | INSERT imutavel — zero ambiguidade |
```

## Modelos disponiveis (Anthropic)

| Modelo | Uso recomendado |
|--------|----------------|
| claude-opus-4-7 | Tarefas complexas de raciocinio, arquitetura |
| claude-sonnet-4-6 | Balanco custo/qualidade — padrao para producao |
| claude-haiku-4-5 | Tarefas simples, alta frequencia, baixo custo |

## Checklist antes de implementar agente com LLM

- [ ] Justificativa documentada de por que LLM e necessario aqui
- [ ] Dados sensiveis mascarados antes do prompt
- [ ] Modelo definido em `.env` (nao hardcoded)
- [ ] max_tokens configurado por env var
- [ ] Fallback definido se LLM falhar
