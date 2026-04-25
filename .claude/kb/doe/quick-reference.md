# DOE — Quick Reference

## Estrutura obrigatoria em todo projeto

```
directives/           ← D: Diretivas
  domain.md           regras do dominio de negocio
  business-rules.md   regras operacionais
  integrations.md     politicas de integracao
  output-contracts.md formatos exatos de saida
  edge-cases.md       casos extremos conhecidos

src/agents/
  orchestrator.py     ← O: Orquestracao — coordena, nao executa logica
  [subagente].py      ← E: Execucao — responsabilidade isolada por agente
```

## Regras de cada camada

**Diretivas**
- LLM nao improvisa fora do que esta em `directives/`
- Toda ambiguidade de dominio vai para `directives/` antes de implementar
- Sao lidas antes de qualquer implementacao

**Orquestracao**
- Coordena fluxo entre subagentes
- Nao executa logica de negocio diretamente
- Recebe input → roteia → agrega resultado → retorna

**Execucao**
- Cada subagente tem UMA responsabilidade
- Recebe contrato tipado de entrada
- Retorna contrato tipado de saida
- Registra em audit_log obrigatoriamente

## Checklist de conformidade DOE

- [ ] `directives/` criado com pelo menos domain.md e business-rules.md
- [ ] OrchestratorAgent nao tem logica de negocio
- [ ] Cada subagente tem contrato de entrada e saida definido em `contracts/`
- [ ] Nenhum subagente chama outro diretamente (passa pelo orquestrador)
- [ ] Toda operacao registra em audit_log
