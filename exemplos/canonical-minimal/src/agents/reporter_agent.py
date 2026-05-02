from datetime import datetime, timezone

from ..contracts.issue_contract import IssueClassification, IssueInput, IssueReport


class ReporterAgent:
    def gerar_aprovado(
        self,
        issue: IssueInput,
        classificacao: IssueClassification,
        tentativas: int,
    ) -> IssueReport:
        return IssueReport(
            input=issue,
            classificacao=classificacao,
            timestamp_utc=datetime.now(timezone.utc).isoformat(),
            tentativas=tentativas,
            status="aprovado",
        )

    def gerar_falhou(
        self,
        issue: IssueInput,
        tentativas: int,
        erro: str,
    ) -> IssueReport:
        return IssueReport(
            input=issue,
            classificacao=None,
            timestamp_utc=datetime.now(timezone.utc).isoformat(),
            tentativas=tentativas,
            status="falhou",
            erro=erro,
        )
