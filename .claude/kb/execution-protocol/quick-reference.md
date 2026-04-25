# Protocolo de Execucao — Quick Reference

## Loop obrigatorio

```
1. Executar o fluxo
2. Capturar saida e erros
3. Erro local e baixo risco? → corrigir → voltar para 1
4. Rodar validacao associada
5. Reportar no chat:
     - o que executou
     - o que falhou
     - o que corrigiu
     - estado atual (aprovado / bloqueado)
6. Parar apenas quando: gate aprovado OU bloqueio real
```

## Disparadores (quando aplicar o loop)

- `python execution/run_onboarding_flow.py`
- `pytest tests/...`
- "rode o gate N"
- "execute o fluxo"
- "valide e corrija"
- qualquer script em `execution/`

## Correcao automatica permitida

| Tipo de erro | Pode corrigir? |
|-------------|---------------|
| Import quebrado | Sim |
| Path incorreto | Sim |
| Artefato faltando por scaffold | Sim |
| Erro de validacao estrutural simples | Sim |
| Ambiguidade de regra de negocio | Nao — perguntar |
| Credencial ausente | Nao — perguntar |
| Risco de escrita em fonte sensivel | Nao — perguntar |
| Conflito de escopo | Nao — perguntar |

## Como reportar no chat

```
Executando: [comando]
Resultado: [sucesso/erro]
Correcao aplicada: [o que foi corrigido, se aplicavel]
Reexecutando: [sim/nao]
Estado atual: [gate aprovado / bloqueado por: X]
```

## Criterio de parada

**Parar com sucesso:** fluxo executou + validacao passou + gate aprovado

**Parar com bloqueio:** proximo passo exige decisao humana — descrever objetivamente o que precisa ser decidido
