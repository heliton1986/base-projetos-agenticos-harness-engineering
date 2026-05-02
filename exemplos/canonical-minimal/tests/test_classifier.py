from types import SimpleNamespace

import pytest

from src.agents.classifier_agent import ClassifierAgent
from src.contracts.issue_contract import IssueInput


class _FakeMessages:
    def __init__(self, content: str) -> None:
        self._content = content

    def create(self, **_: object) -> SimpleNamespace:
        return SimpleNamespace(content=[SimpleNamespace(text=self._content)])


class _FakeClient:
    def __init__(self, content: str) -> None:
        self.messages = _FakeMessages(content)


def test_classificar_com_fake_client():
    agent = ClassifierAgent.__new__(ClassifierAgent)
    agent._client = _FakeClient(
        'prefixo {"severidade":"alta","categoria":"bug","justificativa":"Erro reproduzivel com impacto claro no fluxo principal","confianca":"alta"} sufixo'
    )
    agent._model = "claude-sonnet-4-6"

    issue = IssueInput(texto="A pagina retorna erro 500 quando o usuario tenta salvar dados.")
    resultado = agent.classificar(issue)

    assert resultado.severidade == "alta"
    assert resultado.categoria == "bug"
    assert resultado.confianca == "alta"


def test_extrair_json_rejeita_saida_sem_objeto():
    with pytest.raises(ValueError):
        ClassifierAgent._extrair_json("sem json aqui")


def test_init_exige_api_key(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)

    with pytest.raises(EnvironmentError):
        ClassifierAgent()
