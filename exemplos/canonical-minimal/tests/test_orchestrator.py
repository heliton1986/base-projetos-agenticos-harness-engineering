from src.agents.orchestrator import OrchestratorAgent
from src.agents.reporter_agent import ReporterAgent
from src.agents.validator_agent import ValidatorAgent
from src.contracts.issue_contract import IssueClassification, IssueInput


class FakeClassifier:
    def __init__(self, respostas):
        self._respostas = list(respostas)
        self.contextos: list[str] = []

    def classificar(self, issue: IssueInput, contexto_erro: str = "") -> IssueClassification:
        self.contextos.append(contexto_erro)
        resposta = self._respostas.pop(0)
        if isinstance(resposta, Exception):
            raise resposta
        return resposta


def _build_orchestrator(fake_classifier: FakeClassifier) -> OrchestratorAgent:
    orchestrator = OrchestratorAgent.__new__(OrchestratorAgent)
    orchestrator._classifier = fake_classifier
    orchestrator._validator = ValidatorAgent()
    orchestrator._reporter = ReporterAgent()
    return orchestrator


def test_orchestrator_retenta_apos_regra_de_negocio_invalida():
    issue = IssueInput(texto="Usuarios perderam acesso ao sistema apos atualizacao recente.")
    fake = FakeClassifier(
        [
            IssueClassification(
                severidade="critica",
                categoria="feature",
                justificativa="Classificacao inicial inconsistente com a regra do dominio",
                confianca="media",
            ),
            IssueClassification(
                severidade="alta",
                categoria="bug",
                justificativa="Incidente afeta usuarios reais e exige resposta rapida",
                confianca="alta",
            ),
        ]
    )
    orchestrator = _build_orchestrator(fake)

    resultado = orchestrator.processar(issue)

    assert resultado.status == "aprovado"
    assert resultado.tentativas == 2
    assert 'severidade "critica" so permitida para categoria "bug" ou "seguranca"' in fake.contextos[1]
    assert 'categoria "feature" tem severidade maxima "media"' in fake.contextos[1]


def test_orchestrator_falha_apos_tres_erros():
    issue = IssueInput(texto="Nao consigo usar a funcionalidade principal desde ontem.")
    fake = FakeClassifier(
        [ValueError("json invalido"), ValueError("json invalido"), ValueError("json invalido")]
    )
    orchestrator = _build_orchestrator(fake)

    resultado = orchestrator.processar(issue)

    assert resultado.status == "falhou"
    assert resultado.tentativas == 3
    assert "json invalido" in resultado.erro
