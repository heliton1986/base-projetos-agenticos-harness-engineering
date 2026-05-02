"""
Gate 1 — Verificacao de ambiente do Issue Triage Agent.

Executa smoke tests sem chamar a API real.
Todos os gates devem passar antes de rodar o sistema.
"""
import importlib
import os
import sys
from pathlib import Path

# carrega .env se existir (sem dependencia de python-dotenv)
_env_path = Path(__file__).parent.parent / ".env"
if _env_path.exists():
    for line in _env_path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, _, value = line.partition("=")
            os.environ.setdefault(key.strip(), value.strip())

GATES = []


def gate(nome: str):
    def decorator(fn):
        GATES.append((nome, fn))
        return fn
    return decorator


@gate("ANTHROPIC_API_KEY presente")
def gate_api_key():
    key = os.environ.get("ANTHROPIC_API_KEY", "")
    assert key and key.startswith("sk-"), (
        "ANTHROPIC_API_KEY ausente ou formato invalido. "
        "Execute: export ANTHROPIC_API_KEY=sk-..."
    )


@gate("anthropic importavel")
def gate_anthropic():
    try:
        importlib.import_module("anthropic")
    except ImportError:
        raise AssertionError("anthropic nao instalado. Execute: pip install anthropic")


@gate("pydantic importavel")
def gate_pydantic():
    try:
        import pydantic
        major = int(pydantic.VERSION.split(".")[0])
        assert major >= 2, f"Pydantic v2+ necessario, encontrado: {pydantic.VERSION}"
    except ImportError:
        raise AssertionError("pydantic nao instalado. Execute: pip install pydantic")


@gate("IssueInput valida texto vazio")
def gate_issue_input_validacao():
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
    from src.contracts.issue_contract import IssueInput
    from pydantic import ValidationError

    try:
        IssueInput(texto="")
        raise AssertionError("Deveria ter rejeitado texto vazio")
    except ValidationError:
        pass


@gate("IssueClassification rejeita valores invalidos")
def gate_classification_contract():
    from src.contracts.issue_contract import IssueClassification
    from pydantic import ValidationError

    try:
        IssueClassification(
            severidade="urgente",  # invalido
            categoria="bug",
            justificativa="Texto longo o suficiente aqui",
            confianca="alta",
        )
        raise AssertionError("Deveria ter rejeitado severidade invalida")
    except ValidationError:
        pass


@gate("ValidatorAgent valida payload conhecido")
def gate_validator_agent():
    from src.agents.validator_agent import ValidatorAgent

    vr = ValidatorAgent().validar_payload(
        "IssueClassification",
        {
            "severidade": "alta",
            "categoria": "bug",
            "justificativa": "Erro reproduzivel em ambiente de producao com impacto claro",
            "confianca": "alta",
        },
    )
    assert vr.valido is True, f"ValidatorAgent retornou erro: {vr.erros}"


@gate("Regras de negocio: critica + feature rejeitada")
def gate_business_rules():
    from src.agents.orchestrator import validar_regras_negocio
    from src.contracts.issue_contract import IssueClassification

    invalido = IssueClassification(
        severidade="critica",
        categoria="feature",
        justificativa="Texto longo o suficiente aqui para teste",
        confianca="alta",
    )
    erros = validar_regras_negocio(invalido)
    assert len(erros) > 0, "Deveria ter detectado violacao de regra de negocio"


@gate("ReporterAgent gera IssueReport aprovado")
def gate_reporter():
    from src.contracts.issue_contract import IssueClassification, IssueInput
    from src.agents.reporter_agent import ReporterAgent

    issue = IssueInput(texto="Sistema fora do ar apos deploy, usuarios bloqueados")
    classificacao = IssueClassification(
        severidade="critica",
        categoria="bug",
        justificativa="Sistema completamente inoperante, usuarios nao conseguem acessar",
        confianca="alta",
    )
    reporter = ReporterAgent()
    relatorio = reporter.gerar_aprovado(issue, classificacao, tentativas=1)
    assert relatorio.status == "aprovado"
    assert relatorio.tentativas == 1
    assert relatorio.erro is None


def main():
    print("=" * 60)
    print("Issue Triage Agent — Onboarding Flow")
    print("=" * 60)

    aprovados = 0
    reprovados = 0

    for nome, fn in GATES:
        try:
            fn()
            print(f"  [PASS] {nome}")
            aprovados += 1
        except (AssertionError, Exception) as e:
            print(f"  [FAIL] {nome}")
            print(f"         {e}")
            reprovados += 1

    print("=" * 60)
    print(f"Resultado: {aprovados}/{len(GATES)} gates aprovados")

    if reprovados > 0:
        print(f"BLOQUEADO — {reprovados} gate(s) falharam")
        sys.exit(1)
    else:
        print("APROVADO — ambiente pronto para execucao")
        sys.exit(0)


if __name__ == "__main__":
    main()
