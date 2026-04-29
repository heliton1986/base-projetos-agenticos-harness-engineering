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

## Parser de output LLM — padrao obrigatorio

Quando agente parseia texto LLM com campo tipado:

```python
import re

uuid_pattern = re.compile(
    r"([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})\|([^|]+)\|(.+)",
    re.IGNORECASE,
)
TIPOS_VALIDOS = {"tipo_a", "tipo_b", "tipo_generico"}  # adaptar ao dominio

for linha in texto.strip().splitlines():
    match = uuid_pattern.search(linha)          # search, nao match
    if match:
        lid = match.group(1)
        tipo = match.group(2).strip()
        descricao = match.group(3).strip().strip("*`")
        tipo_norm = re.sub(r"[^a-zA-Z0-9_]", "_", tipo).strip("_")
        tipo_limpo = tipo_norm if tipo_norm in TIPOS_VALIDOS else "tipo_generico"
```

Regras: ancora no ID estruturado, `search()` ignora prefixo markdown, strip `*\`` no descricao, fallback obrigatorio para tipo invalido.

## Checklist de conformidade

- [ ] Cada capacidade tem gate definido em `spec/05-validate.md`
- [ ] Gate tem comando pytest executavel
- [ ] Criterios sao verificaveis (nao subjetivos)
- [ ] audit_log e criterio obrigatorio em todo gate
- [ ] LLM executa loop completo sem esperar confirmacao a cada passo intermediario
