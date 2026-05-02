"""
Ponto de entrada principal. Executa classificacao de issue de exemplo.
"""
from pydantic import ValidationError

from ..contracts.issue_contract import IssueClassification, IssueInput, IssueReport
from .classifier_agent import ClassifierAgent
from .reporter_agent import ReporterAgent
from .validator_agent import ValidatorAgent

MAX_TENTATIVAS = 3

REGRAS_NEGOCIO = [
    (
        lambda c: c.severidade == "critica" and c.categoria not in ("bug", "seguranca"),
        'severidade "critica" so permitida para categoria "bug" ou "seguranca"',
    ),
    (
        lambda c: c.categoria == "duvida" and c.severidade != "baixa",
        'categoria "duvida" tem severidade maxima "baixa"',
    ),
    (
        lambda c: c.categoria == "feature" and c.severidade in ("critica", "alta"),
        'categoria "feature" tem severidade maxima "media"',
    ),
]


def validar_regras_negocio(classificacao: IssueClassification) -> list[str]:
    erros = []
    for regra, mensagem in REGRAS_NEGOCIO:
        if regra(classificacao):
            erros.append(mensagem)
    return erros


class OrchestratorAgent:
    def __init__(self) -> None:
        self._classifier = ClassifierAgent()
        self._validator = ValidatorAgent()
        self._reporter = ReporterAgent()

    def processar(self, issue: IssueInput) -> IssueReport:
        tentativas = 0
        contexto_erro = ""

        while tentativas < MAX_TENTATIVAS:
            tentativas += 1
            try:
                classificacao = self._classifier.classificar(issue, contexto_erro)
                vr_classificacao = self._validator.validar_instancia(classificacao)
                if not vr_classificacao.valido:
                    contexto_erro = "; ".join(vr_classificacao.erros)
                    continue

                erros = validar_regras_negocio(classificacao)
                if erros:
                    contexto_erro = "; ".join(erros)
                    continue

                relatorio = self._reporter.gerar_aprovado(issue, classificacao, tentativas)
                vr_relatorio = self._validator.validar_instancia(relatorio)
                if not vr_relatorio.valido:
                    contexto_erro = "; ".join(vr_relatorio.erros)
                    continue

                return relatorio
            except (ValidationError, ValueError, Exception) as e:
                contexto_erro = str(e)

        return self._reporter.gerar_falhou(
            issue,
            tentativas,
            f"Classificacao invalida apos {MAX_TENTATIVAS} tentativas. Ultimo erro: {contexto_erro}",
        )


if __name__ == "__main__":
    import json

    exemplos = [
        IssueInput(
            texto="O sistema nao inicializa apos o ultimo deploy. Usuarios nao conseguem fazer login.",
            titulo="Sistema fora do ar",
        ),
        IssueInput(
            texto="Seria legal ter um modo escuro na interface.",
            titulo="Feature request: dark mode",
        ),
        IssueInput(
            texto="Como faço para resetar minha senha?",
        ),
    ]

    orquestrador = OrchestratorAgent()

    for exemplo in exemplos:
        print(f"\n--- Issue: {exemplo.titulo or exemplo.texto[:50]} ---")
        relatorio = orquestrador.processar(exemplo)
        print(json.dumps(relatorio.model_dump(), indent=2, ensure_ascii=False))
