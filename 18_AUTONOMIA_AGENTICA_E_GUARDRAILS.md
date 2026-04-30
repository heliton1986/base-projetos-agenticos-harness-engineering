# Autonomia Agentica e Guardrails

## Objetivo

Este documento formaliza dois conceitos criticos que distinguem um sistema agentico real de um pipeline com LLM embutida:

1. A diferenca entre **guardrail** e **constraint**
2. A diferenca entre **feed forward** e **feedback** como mecanismos de controle

Esses conceitos fundamentam a decisao de quando um orquestrador e de verdade um agente ou apenas um script sequencial.

## Fonte

- `VIDEO1_HARNESS.md` — conceito de feed forward vs feedback (controle de sistemas)
- Semana AI Data Engineer 2026, Dia 3 — distinção guardrail vs constraint; agente decide fluxo

---

## Guardrail vs Constraint

### Constraint

Uma constraint e uma rota pre-determinada no codigo.

Exemplos:

```python
def executar(self, csv_path):
    lancamentos = self.ingestion.processar(csv_path)
    inconsistencias = self.detector.detectar(lancamentos)
    relatorio = self.reporter.gerar(lancamentos, inconsistencias)
    return relatorio
```

O fluxo nunca muda. A LLM executa dentro de cada etapa, mas nao decide a sequencia.

Isso e um **pipeline com LLM embutida**, nao um agente.

### Guardrail

Um guardrail e uma fronteira de seguranca. O agente opera livremente dentro dela.

Exemplos de guardrail:
- "nao acesse banco de producao sem aprovacao humana"
- "nao apague arquivos fora do diretorio de trabalho"
- "responda apenas sobre dados do periodo solicitado"

O agente decide o caminho. O guardrail define onde nao pode ir.

### Regra central

`Guardrail limita o espaco de acao. Constraint elimina a decisao.`

Se todo o fluxo for constraint, remova o agente e use um script. O resultado sera o mesmo com menos custo e complexidade.

---

## Quando o sistema e um agente de verdade

Um agente de verdade decide:

- **qual ferramenta chamar** — nao apenas como usar uma ferramenta pre-escolhida
- **qual sequencia seguir** — baseado no output intermediario, nao em ordem hardcoded
- **se tenta outra abordagem** — quando o resultado nao foi satisfatorio
- **quando escalar para humano** — baseado em condicoes do contexto

### Exemplos de decisao real do orquestrador

```
# Constraint — nao e agente
if fase >= 3:
    inconsistencias = detector.detectar(lancamentos)

# Guardrail + decisao real — e agente
resultado = detector.detectar(lancamentos)
if resultado.confianca < 0.7:
    # agente decide tentar com prompt diferente
    resultado = detector.detectar(lancamentos, modo="conservador")
if resultado.total_inconsistencias == 0:
    # agente decide se vale re-analisar ou aceitar
    decisao = orquestrador.avaliar_ausencia_de_inconsistencias(lancamentos)
```

---

## Feed Forward vs Feedback

Esses dois conceitos vem da engenharia de controle e sao a base do harness.

### Feed Forward

Orientacao preventiva. Acontece **antes** da execucao.

Objetivo: aumentar a chance de dar certo antes de rodar.

No harness:
- `AGENTS.md` — instrucoes de comportamento
- `spec` — objetivo, escopo, criterios de pronto
- `task contract` — acordo entre builder e validator
- `kb/` — padroes e restricoes do dominio
- `diretivas` — regras de negocio

Feed forward diz **o que fazer** e **como fazer**.

Analogia: a rota que o GPS traca antes de voce sair.

### Feedback

Observacao e correcao **depois** da execucao.

Objetivo: detectar desvio e corrigir em tempo real.

No harness:
- testes unitarios e de integracao
- linters e type checkers
- `ValidatorAgent`
- gates de conformidade (Pydantic, contratos)
- `audit_log`
- CI/CD

Feedback diz **se foi feito certo**.

Analogia: o GPS que detecta que voce saiu da rota e recalcula.

### Por que os dois sao necessarios

`Apenas feed forward: o agente sabe o que fazer, mas nao sabe se errou.`

`Apenas feedback: o agente corrige erros, mas sem direcao clara vai improvisar.`

O harness usa os dois. Sem feedback, spec-driven nao escala para sistemas completos.

---

## Pipeline com LLM vs Agente — diagnostico pratico

Use esta tabela para classificar um sistema:

| Pergunta | Pipeline com LLM | Agente real |
|---|---|---|
| Quem decide a sequencia de etapas? | Codigo Python | LLM |
| O fluxo muda baseado no output intermediario? | Nao | Sim |
| A LLM pode decidir nao chamar uma ferramenta? | Nao | Sim |
| Ha retentativa baseada em avaliacao propria? | Hardcoded (MAX_RETRIES) | Condicional por contexto |
| O agente pode escalar para humano por iniciativa? | Nao | Sim |

Um sistema pode ser parcialmente agentico — parte do fluxo e pipeline, parte tem decisao real. Isso e valido. O problema e chamar de agente um sistema que e inteiramente pipeline.

---

## Implicacao para projetos Harness Engineering

### Fase manual (pre-framework)

Pipelines sao aceitaveis e recomendados na fase manual. Objetivo e validar contratos, sensores e outputs antes de adicionar autonomia.

### Com framework (CrewAI, LangGraph, etc.)

O `OrchestratorAgent` deve ganhar decisao real sobre o fluxo:

- receber output de cada agente
- avaliar qualidade do resultado
- decidir proximo passo baseado nessa avaliacao
- nao apenas chamar o proximo agente da lista

### Anti-padrao a evitar

```python
# Anti-padrao: constraint disfarçada de orquestrador
class OrchestratorAgent:
    def executar(self, path):
        a = self.agent_a.processar(path)   # sempre
        b = self.agent_b.processar(a)      # sempre
        c = self.agent_c.gerar(a, b)       # sempre
        return c
```

```python
# Padrao correto: orquestrador com decisao real
class OrchestratorAgent:
    def executar(self, path):
        a = self.agent_a.processar(path)
        if not a.valido or a.confianca < threshold:
            return self._escalar(a)        # decisao
        b = self.agent_b.processar(a)
        if b.total == 0:
            b = self.agent_b.processar(a, modo="ampliado")  # decisao
        return self.agent_c.gerar(a, b)
```

---

## Relacao com outros documentos

- `02_DOE_OPERACIONAL_PARA_HARNESS.md` — camada O (Orquestracao) e onde a decisao real do agente vive
- `06_PADRAO_BUILDER_VALIDATOR_E_TASK_CONTRACTS.md` — contrato acordado antes da execucao
- `12_ORQUESTRADOR_E_SUBAGENTES_PARA_FLUXOS_DE_EXECUCAO.md` — arquitetura do loop de execucao
- `17_POR_QUE_FASE_MANUAL_ANTES_DO_FRAMEWORK.md` — por que pipeline e correto na fase manual
