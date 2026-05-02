from src.agents.validator_agent import ValidatorAgent
from src.contracts.issue_contract import IssueClassification, IssueInput, IssueReport


def test_validator_valida_instancia_valida():
    vr = ValidatorAgent().validar_instancia(
        IssueClassification(
            severidade="alta",
            categoria="bug",
            justificativa="Falha reproduzivel com impacto claro e justificativa suficiente",
            confianca="alta",
        )
    )

    assert vr.valido is True
    assert vr.contrato_validado == "IssueClassification"
    assert vr.erros == []


def test_validator_rejeita_payload_invalido():
    vr = ValidatorAgent().validar_payload(
        "IssueClassification",
        {
            "severidade": "urgente",
            "categoria": "bug",
            "justificativa": "curta",
            "confianca": "alta",
        },
    )

    assert vr.valido is False
    assert vr.contrato_validado == "IssueClassification"
    assert len(vr.erros) >= 1


def test_issue_report_exige_erro_quando_falha():
    vr = ValidatorAgent().validar_payload(
        "IssueReport",
        {
            "input": IssueInput(texto="Mensagem suficientemente longa para passar no contrato").model_dump(),
            "classificacao": None,
            "timestamp_utc": "2026-05-02T17:43:00+00:00",
            "tentativas": 3,
            "status": "falhou",
            "erro": None,
        },
    )

    assert vr.valido is False
