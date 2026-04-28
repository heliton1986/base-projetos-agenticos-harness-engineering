from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel
from typing import Literal

from .classifier_agent import IssueClassification, IssueInput


class IssueReport(BaseModel):
    input: IssueInput
    classificacao: Optional[IssueClassification]
    timestamp_utc: str
    tentativas: int
    status: Literal["aprovado", "falhou"]
    erro: Optional[str] = None


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
