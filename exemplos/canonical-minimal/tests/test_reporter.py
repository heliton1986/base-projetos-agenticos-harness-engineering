from src.agents.reporter_agent import ReporterAgent
from src.contracts.issue_contract import IssueClassification, IssueInput


def test_reporter_gera_aprovado():
    reporter = ReporterAgent()
    issue = IssueInput(texto="Servico indisponivel e impactando login de usuarios.")
    classificacao = IssueClassification(
        severidade="critica",
        categoria="bug",
        justificativa="Servico indisponivel afeta login e interrompe o uso do sistema",
        confianca="alta",
    )

    relatorio = reporter.gerar_aprovado(issue, classificacao, tentativas=1)

    assert relatorio.status == "aprovado"
    assert relatorio.classificacao == classificacao
    assert relatorio.erro is None


def test_reporter_gera_falhou():
    reporter = ReporterAgent()
    issue = IssueInput(texto="Texto suficiente para acionar um caso de erro controlado.")

    relatorio = reporter.gerar_falhou(issue, tentativas=3, erro="ultimo erro")

    assert relatorio.status == "falhou"
    assert relatorio.classificacao is None
    assert relatorio.erro == "ultimo erro"
