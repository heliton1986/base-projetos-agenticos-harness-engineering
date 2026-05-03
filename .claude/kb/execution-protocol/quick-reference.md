# Protocolo de Execucao — Quick Reference

## Loop do Agente: Perception → Reasoning → Action → Memory

| Fase | O que acontece |
|------|---------------|
| **Perception** | Recebe input, interpreta intencao |
| **Reasoning** | Decide proximo passo — qual tool, qual fonte |
| **Action** | Executa — SQL (exato) ou Qdrant (semantico) |
| **Memory** | Armazena contexto; alimenta proxima iteracao |

Memory ativa diferencia agente de script: resultado de cada iteracao entra na proxima decisao.

Mapeamento com ReAct: Perception≈Observe(entrada), Reasoning≈Think, Action≈Act, Memory≈Observe+armazenamento.

## Padrao ReAct (base do loop)

Loop fundamentado em **ReAct** (Reasoning + Acting — Yao et al. 2022):

| Fase | O que fazer |
|---|---|
| **Think** | Raciocinar antes de agir — entender estado atual, identificar proximo passo |
| **Act** | Executar a acao escolhida (script, correcao, tool call) |
| **Observe** | Integrar resultado — o que mudou, o que falhou, o que passou |
| **Iterate** | Decidir: aprovado / corrigir e repetir / escalar |

Cada decisao deve ser registrada no audit_log para auditabilidade.

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

## Granularidade dos micro-updates

- Nao esperar juntar tudo no fim do gate quando houver varias acoes observaveis relevantes.
- Preferir o padrao: `1 leitura/comando relevante -> 1 retorno curto no chat`.
- Se a interface resumir `Explored ...` ou `Ran ...`, expandir isso no chat com os nomes reais dos arquivos e comandos.

Exemplo:

```text
Li `AGENTS.md`. Resultado: confirmei o protocolo. Proximo passo: abrir `README.md`.
Li `README.md`. Resultado: localizei o script de onboarding. Proximo passo: rodar `python execution/run_onboarding_flow.py`.
Rodei `python execution/run_onboarding_flow.py`. Resultado: passou. Proximo passo: rodar `pytest tests/ -v --tb=short`.
```

## Criterio de parada

**Parar com sucesso:** fluxo executou + validacao passou + gate aprovado

**Parar com bloqueio:** proximo passo exige decisao humana — descrever objetivamente o que precisa ser decidido
