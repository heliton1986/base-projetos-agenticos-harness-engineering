# Builder / Validator — Quick Reference

## Ciclo por capacidade

```
Builder    → implementa o artefato (agente, script, endpoint)
     ↓
Validator  → executa teste/validacao contra contrato esperado
     ↓
Passou?
  Sim → Gate aprovado → avancar para proxima capacidade
  Nao → corrigir (se erro local e baixo risco) → reexecutar Builder
     ↓
Bloqueio real → parar e reportar ao humano
```

## O que e erro local e baixo risco (corrigir automaticamente)

- import quebrado
- path incorreto
- artefato faltando por erro de scaffold
- ajuste de script local
- erro simples de validacao estrutural

## O que e bloqueio real (parar e perguntar)

- ambiguidade de regra de negocio ou regulatoria
- credencial ausente
- risco de escrita indevida em fonte sensivel
- conflito de escopo entre capacidades

## Estrutura de gate por capacidade

```
spec/05-validate.md
  Gate N — [Nome da Capacidade]
    Comando: pytest tests/smoke/test_[capacidade].py -v
    Criterios:
      - [ ] [criterio 1 verificavel]
      - [ ] [criterio 2 verificavel]
      - [ ] Entrada em audit_log criada
```

## Checklist de conformidade

- [ ] Cada capacidade tem gate definido em `spec/05-validate.md`
- [ ] Gate tem comando pytest executavel
- [ ] Criterios sao verificaveis (nao subjetivos)
- [ ] audit_log e criterio obrigatorio em todo gate
- [ ] LLM executa loop completo sem esperar confirmacao a cada passo intermediario
