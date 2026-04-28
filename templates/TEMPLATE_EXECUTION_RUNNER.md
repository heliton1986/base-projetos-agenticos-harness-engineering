# Template: Execution Runner Narrativo

## Objetivo

Este template define o padrao para runners de execucao com saida narrativa em tempo real.

Todo projeto derivado da base deve ter um runner que:
- imprime cada fase e gate conforme executa (nao ao final)
- usa timestamps
- distingue APROVADO / FALHOU / BLOQUEADO
- retorna exit code correto (0 = aprovado, 1 = falha critica, 2 = bloqueio real)

## Quando usar

Substitui ou complementa `run_onboarding_flow.py` quando o projeto tem multiplas fases
alem do bootstrap. Use para qualquer fluxo executavel end-to-end.

## Estrutura do arquivo

```
execution/
├── run_onboarding_flow.py   # Gate 1 apenas — ambiente
└── run_flow.py              # Todas as fases — runner narrativo completo
```

## Template base

```python
"""
[NOME_DO_PROJETO] — Execution Runner

Executa todas as fases do projeto com saida narrativa em tempo real.
Uso: python execution/run_flow.py [--fase NUMERO]

Exit codes:
  0 — todas as fases aprovadas
  1 — falha critica (gate nao passou)
  2 — bloqueio real (requer intervencao humana)
"""
import sys
import time
from datetime import datetime
from pathlib import Path

# carrega .env se existir
_env_path = Path(__file__).parent.parent / ".env"
if _env_path.exists():
    for line in _env_path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            import os
            key, _, value = line.partition("=")
            os.environ.setdefault(key.strip(), value.strip())

SEPARADOR = "═" * 56


def log(nivel: str, mensagem: str, duracao: float | None = None) -> None:
    """Imprime linha narrativa em tempo real."""
    ts = datetime.now().strftime("%H:%M:%S")
    dur = f"  ({duracao:.1f}s)" if duracao is not None else ""
    print(f"[{ts}] {nivel:<30} {mensagem}{dur}", flush=True)


def cabecalho(titulo: str) -> None:
    print(f"\n{SEPARADOR}", flush=True)
    print(f"  {titulo}", flush=True)
    print(f"{SEPARADOR}\n", flush=True)


def rodape(fases_ok: int, fases_total: int) -> None:
    print(f"\n{SEPARADOR}", flush=True)
    print(f"  Resultado: {fases_ok}/{fases_total} fases aprovadas", flush=True)
    status = "SISTEMA PRONTO" if fases_ok == fases_total else "SISTEMA BLOQUEADO"
    print(f"  {status}", flush=True)
    print(f"{SEPARADOR}\n", flush=True)


class RunnerNarrativo:
    def __init__(self, nome_projeto: str):
        self.nome = nome_projeto
        self.fases_ok = 0
        self.fases_total = 0

    def fase(self, numero: int, nome: str):
        """Context manager para uma fase."""
        return _FaseContext(self, numero, nome)

    def gate(self, nome: str):
        """Context manager para um gate dentro de uma fase."""
        return _GateContext(nome)


class _FaseContext:
    def __init__(self, runner: RunnerNarrativo, numero: int, nome: str):
        self.runner = runner
        self.label = f"[Fase {numero} — {nome}]"
        self._inicio = 0.0

    def __enter__(self):
        self.runner.fases_total += 1
        self._inicio = time.monotonic()
        log(self.label, "iniciando...")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        dur = time.monotonic() - self._inicio
        if exc_type is None:
            self.runner.fases_ok += 1
            log(self.label, "CONCLUIDA ✓", dur)
        elif exc_type is BlockingError:
            log(self.label, f"BLOQUEADO — {exc_val}")
            return False
        else:
            log(self.label, f"FALHOU — {exc_val}", dur)
            return False
        return True


class _GateContext:
    def __init__(self, nome: str):
        self.label = f"  [Gate — {nome}]"
        self._inicio = 0.0

    def __enter__(self):
        self._inicio = time.monotonic()
        log(self.label, "verificando...", )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        dur = time.monotonic() - self._inicio
        if exc_type is None:
            log(self.label, "APROVADO ✓", dur)
        else:
            log(self.label, f"FALHOU — {exc_val}", dur)
            return False
        return True


class BlockingError(Exception):
    """Bloqueio real — requer intervencao humana."""


# ── Fases do projeto (preencher por projeto) ──────────────────────────────────

def fase_1_bootstrap(runner: RunnerNarrativo) -> None:
    with runner.fase(1, "Bootstrap"):
        with _GateContext("Ambiente"):
            # importar e verificar dependencias
            # ex: import anthropic, pydantic
            pass

        with _GateContext("Conexao DB"):
            # verificar conexao com banco
            pass

        with _GateContext("Schema"):
            # verificar tabelas necessarias
            pass


def _validar_contrato(session, run_id, instancia, nome_agente: str) -> None:
    """Gate de validacao entre fases — revalida contrato Pydantic antes de passar ao proximo agente."""
    from src.agents.validator_agent import ValidatorAgent
    from src.db.audit import registrar
    vr = ValidatorAgent().validar_instancia(instancia)
    registrar(session, run_id, "ValidatorAgent", f"validacao_{type(instancia).__name__}",
              "ok" if vr.valido else "falhou", {"erros": vr.erros})
    if not vr.valido:
        raise RuntimeError(f"Contrato {vr.contrato_validado} invalido apos {nome_agente}: {vr.erros}")


def fase_2_primeira_capacidade(runner: RunnerNarrativo, session) -> None:
    with runner.fase(2, "[NOME_DA_CAPACIDADE]"):
        log("  [OrchestratorAgent]", "iniciando fluxo...")

        with _GateContext("[GATE_DA_FASE]"):
            # executar primeira capacidade incremental
            # acionar agentes
            # registrar em audit_log via: registrar(session, run_id, agente, acao, status, detalhe)
            pass

        # Gate obrigatorio apos cada agente — para o fluxo se contrato invalido
        with _GateContext("Validacao Contrato"):
            _validar_contrato(session, resultado.run_id, resultado, "[NOME_AGENTE]")

        log("  [ReporterAgent]", "gerando relatorio...")


# ── Entry point ────────────────────────────────────────────────────────────────

def main() -> None:
    runner = RunnerNarrativo("[NOME_DO_PROJETO]")
    cabecalho(f"{runner.nome} — Execution Runner")

    try:
        fase_1_bootstrap(runner)

        # Sessao unica para todas as fases com DB — garante audit_log por run
        # Regra: run_flow.py abre a sessao e passa para cada fase.
        # Nunca delegar abertura de sessao ao OrchestratorAgent ou agentes individuais.
        from src.db.connection import get_session
        with get_session() as session:
            fase_2_primeira_capacidade(runner, session)
            # adicionar fases conforme o projeto evolui
    except BlockingError as e:
        print(f"\n  BLOQUEIO REAL: {e}", flush=True)
        print("  Intervencao humana necessaria antes de continuar.", flush=True)
        sys.exit(2)
    except Exception as e:
        print(f"\n  ERRO NAO TRATADO: {e}", flush=True)
        sys.exit(1)
    finally:
        rodape(runner.fases_ok, runner.fases_total)

    sys.exit(0 if runner.fases_ok == runner.fases_total else 1)


if __name__ == "__main__":
    main()
```

## Campos a substituir

| Placeholder | O que colocar |
|-------------|--------------|
| `[NOME_DO_PROJETO]` | nome do projeto (ex: FinanceOps Agent) |
| `[NOME_DA_CAPACIDADE]` | nome da fase 2 (ex: Consolidacao de Lancamentos) |
| `[GATE_DA_FASE]` | nome do gate (ex: Lancamentos Consolidados) |

## Padrao de saida esperado

```
════════════════════════════════════════════════════════
  FinanceOps Agent — Execution Runner
════════════════════════════════════════════════════════

[10:23:41] [Fase 1 — Bootstrap]          iniciando...
[10:23:41]   [Gate — Ambiente]           verificando...
[10:23:41]   [Gate — Ambiente]           APROVADO ✓  (0.1s)
[10:23:41]   [Gate — Conexao DB]         verificando...
[10:23:42]   [Gate — Conexao DB]         APROVADO ✓  (0.8s)
[10:23:42] [Fase 1 — Bootstrap]          CONCLUIDA ✓  (0.9s)

[10:23:42] [Fase 2 — Consolidacao]       iniciando...
[10:23:42]   [OrchestratorAgent]         iniciando fluxo...
[10:23:42]   [Gate — Lancamentos]        verificando...
[10:23:44]   [Gate — Lancamentos]        APROVADO ✓  (2.1s)
[10:23:44]   [ReporterAgent]             gerando relatorio...
[10:23:44] [Fase 2 — Consolidacao]       CONCLUIDA ✓  (2.2s)

════════════════════════════════════════════════════════
  Resultado: 2/2 fases aprovadas
  SISTEMA PRONTO
════════════════════════════════════════════════════════
```

## Regra de BlockingError

Use `raise BlockingError("motivo")` quando:
- credencial ausente ou invalida
- ambiguidade de regra de negocio
- risco de escrita indevida
- conflito de escopo

Nunca use `BlockingError` para erros tecnicos recuperaveis — esses vao para o loop de correcao.

## Integracao com o chat (LLM)

Quando a LLM executar este runner, seguir o protocolo completo de `AGENTS.md`:

**Antes da tool call** — contextualizar o que vai executar:
```
[Fase 3 — Deteccao] iniciando DetectorAgent.
Regras fixas primeiro, depois LLM (claude-sonnet-4-6) com valores mascarados.
```

**Depois da tool call** — reportar resultado detalhado:
```
Fase 3 CONCLUIDA. DetectorAgent (claude-sonnet-4-6):
- 9 lancamentos analisados
- 2 inconsistencias: duplicata_suspeita [critica] + descricao_suspeita [media]
Proximo: Fase 4 — ReporterAgent gera RelatorioExecutivo.
```

**Atualizacao de progress/** — automatica ao fim de cada fase, sem pedir confirmacao.
Formato de data: `YYYY-MM-DD HH:MM`.

Ver instrucao completa em `AGENTS.md` — secao "Protocolo narrativo no chat".
