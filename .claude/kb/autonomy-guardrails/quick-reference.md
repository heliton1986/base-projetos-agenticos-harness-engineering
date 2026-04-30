# Autonomia Agentica — Quick Reference

## Guardrail vs Constraint

| Conceito | Definicao | Efeito |
|---|---|---|
| **Guardrail** | Fronteira de seguranca — agente opera livremente dentro | Preserva decisao do agente |
| **Constraint** | Rota pre-determinada no codigo | Elimina decisao do agente |

Regra: `Guardrail limita o espaco de acao. Constraint elimina a decisao.`

Se todo fluxo for constraint → remova o agente, use um script. Mesmo resultado, menos custo.

## Diagnostico: pipeline ou agente?

| Pergunta | Pipeline com LLM | Agente real |
|---|---|---|
| Quem decide a sequencia? | Codigo Python | LLM |
| Fluxo muda pelo output intermediario? | Nao | Sim |
| LLM pode nao chamar uma ferramenta? | Nao | Sim |
| Retentativa e condicional por contexto? | Nao (MAX_RETRIES fixo) | Sim |
| Agente escala para humano por iniciativa? | Nao | Sim |

## Anti-padrao vs padrao correto

```python
# Anti-padrao: constraint disfarçada de orquestrador
def executar(self, path):
    a = self.agent_a.processar(path)   # sempre
    b = self.agent_b.processar(a)      # sempre
    return self.agent_c.gerar(a, b)    # sempre

# Padrao correto: orquestrador com decisao real
def executar(self, path):
    a = self.agent_a.processar(path)
    if not a.valido or a.confianca < threshold:
        return self._escalar(a)                          # decisao
    b = self.agent_b.processar(a)
    if b.total == 0:
        b = self.agent_b.processar(a, modo="ampliado")  # decisao
    return self.agent_c.gerar(a, b)
```

## Non-determinism reframe

`Geracao nao-deterministica x verificacao deterministica = resultado determinístico`

Nao controle como a LLM gera — controle se o resultado passa nos gates.

| Nao controlar | Controlar |
|---|---|
| Como a LLM formula o codigo | Se o teste passa |
| Qual sequencia de tokens | Se o contrato Pydantic valida |
| Estilo de implementacao | Se o CI aprova |

## 7 Padroes de Orquestracao

| Padrao | Quando usar | Exemplo |
|---|---|---|
| **Sequential** | Dependencia estrita de ordem | ingestao → deteccao → relatorio |
| **Parallel** | Tarefas independentes simultaneas | SQL + vetor ao mesmo tempo |
| **Hierarchical** | Manager delega para especialistas | ShopAgent com subagentes por dominio |
| **Reactive** | Resposta a eventos em tempo real | Monitoramento com alertas |
| **Adaptive** | Aprende com historico de runs | Ajuste de threshold por feedback |
| **Hybrid** | Combinacao de padroes por fase | Producao complexa |
| **Consensus** ⚠️ | Alto risco + gate deterministico insuficiente | 3 agentes votam em classificacao critica |

Consensus — nao usar por padrao: N× custo, falsa seguranca se prompt identico. Substituir por ValidatorAgent + pytest/Pydantic na maioria dos casos.

## Fase manual vs framework

| Fase | Padrao aceito | Objetivo |
|---|---|---|
| Manual (pre-framework) | Pipeline com LLM — constraint OK | Validar contratos e outputs |
| Com framework (CrewAI) | Orquestrador com decisao real | Autonomia de fluxo baseada em output |

## Checklist antes de chamar de agente

- [ ] OrchestratorAgent avalia output antes de chamar proximo agente
- [ ] Ha pelo menos uma decisao condicional baseada em resultado intermediario
- [ ] LLM pode escolher nao executar uma etapa
- [ ] Ha caminho de escalacao para humano por iniciativa do agente
