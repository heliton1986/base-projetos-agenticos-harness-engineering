# Por Que a Fase Manual Vem Antes do Framework

## Contexto

Esta base usa uma progressão deliberada: domínio + contratos + testes → CI → framework (CrewAI, LangChain, etc).

A pergunta natural é: faz sentido fazer tudo isso manualmente antes de usar multi-agent? Não seria mais rápido ir direto para o framework?

A resposta é não. Este documento explica o porquê.

---

## A progressão do semana-ai era didática, não arquitetural

O semana-ai (referência usada na construção desta base) estruturou 4 dias como níveis de autonomia crescente:

```
Dia 1 → "EU FAÇO, IA AJUDA"        (copiloto)
Dia 2 → "IA BUSCA, EU PERGUNTO"    (contexto)
Dia 3 → "IA DECIDE, EU VALIDO"     (agente único)
Dia 4 → "IA CONSTRÓI, IA EXECUTA"  (multi-agent)
```

O objetivo era ensinar cada camada antes de adicionar a próxima. É uma ramp didática para alunos entenderem autonomia progressiva. Não é uma recomendação de arquitetura de produção.

---

## As três eras de controle de software

O contexto para entender por que a fase manual importa começa com como o controle sobre software evoluiu:

| Era | Mecanismo de controle | Produtividade | Como se garante qualidade |
|-----|----------------------|---------------|--------------------------|
| **Software 1.0** | Autoria — 100% hand-written | ~100 linhas/dia | Testes manuais |
| **Software 2.0** | Configuração — config over code | ~500 linhas/dia | Testes automatizados |
| **Software 3.0** | Especificação — specs + guardrails | 5.000+ linhas/dia | Verificação de outcomes |

O escopo do controle expandiu. O mecanismo mudou.

"Control freaks aren't losing control. They're scaling it."

Na era do Software 3.0, controlar qualidade não significa revisar cada linha de código gerado. Significa definir a especificação com precisão suficiente para que qualquer código que passe nos gates seja correto. A fase manual constrói exatamente isso: os contratos, gates e verificadores que tornam a verificação de outcomes possível.

Fonte: Semana AI Data Engineer 2026, Dia 3 — slide "Three Eras of Control"

---

## A fase manual é necessária, não desperdício

A fase manual constrói o que o framework pressupõe que você já sabe:

| O que se faz manualmente | Por que é necessário antes do framework |
|--------------------------|----------------------------------------|
| Contratos Pydantic por agente | Framework não valida tipos — você precisa saber o que validar antes de saber onde colocar |
| ValidatorAgent como gate | Sem entender onde o fluxo pode quebrar, você não sabe onde colocar o callback de validação |
| Testes offline por agente | Framework adiciona camada por cima — os agentes precisam ser corretos antes |
| Regras fixas separadas do LLM | Sem isso, você não sabe o que é determinístico e o que é probabilístico no domínio |
| Parser LLM robusto | Descoberto e corrigido na fase manual — dentro do framework é muito mais difícil de isolar |

O semana-ai comprimiu os dias 1-3 como base didática. A fase manual desta base constrói o equivalente, com muito mais rigor de produção embaixo.

---

## O que o semana-ai dia 4 não tem que esta base já tem

O ShopAgent do dia 4 é uma demo educacional. Comparação direta:

| | Semana-AI Dia 4 | Esta base (FinanceOps como referência) |
|--|----------------|----------------------------------------|
| Contratos validados entre agentes | Não | Sim (Pydantic + ValidatorAgent) |
| audit_log por operação | Não | Sim |
| Testes offline por agente | Não | Sim |
| CI/coverage mínimo | Não | Sim (80%+, GitHub Actions) |
| Fallback em caso de falha LLM | Não explícito | Sim (retry + tipo genérico) |

O framework (CrewAI + Chainlit) entra em cima de uma base validada. O semana-ai entra em cima de uma demo sem rede de segurança. Para entrega a clientes, essa diferença é crítica.

---

## A marcha dos noves na prática

VIDEO2 (Harness Engineering) cita 0,9^10 = 35% de chance de sucesso em um fluxo de 10 etapas onde cada etapa tem 90% de confiabilidade.

A fase manual é a forma de empurrar cada etapa de 90% para próximo de 99%:

- Agente testado offline = menos variável probabilística
- Contrato Pydantic = output previsível = próximo agente recebe dado confiável
- CI = nenhuma regressão silenciosa ao migrar para framework

Sem a fase manual, você aplica CrewAI em cima de agentes não validados. O framework gerencia o handoff, mas não valida o que está sendo passado. Cada etapa continua em 90% — e o produto do fluxo continua em 35%.

---

## A ordem correta para produção e entrega a clientes

```
Domínio + regras + contratos → testes → CI → framework
```

Não o contrário.

O semana-ai fez o contrário porque o objetivo era ensino, não entrega. Para ensino, mostrar o framework logo é motivador — o aluno vê o resultado visual rápido. Para produção, o framework sem fundamento é risco operacional.

---

## Quando adicionar o framework

O framework (CrewAI, LangChain, etc) entra quando:

1. Agentes individuais têm testes passando
2. Contratos Pydantic definidos e validados
3. ValidatorAgent como gate funcionando
4. CI verde no repositório
5. Você conhece cada ponto de falha possível no fluxo

Cumpridos esses critérios, o framework acrescenta observabilidade, handoff limpo e interface visual — sem adicionar risco novo.

---

## Referências

- VIDEO1_HARNESS.md — conceito de feed forward + feedback (sensores)
- VIDEO2_HARNESS.md — DOE, marcha dos noves, subagentes com contextos separados
- semana-ai/presentation/d4-multi-agent.html — progressão de autonomia e motivação para multi-agent
- 06_PADRAO_BUILDER_VALIDATOR_E_TASK_CONTRACTS.md — padrão Builder/Validator que sustenta a fase manual
