"""
Ponto de entrada principal. Executa classificacao de issue de exemplo.
"""
from pydantic import ValidationError

from .classifier_agent import ClassifierAgent, IssueClassification, IssueInput
from .reporter_agent import IssueReport, ReporterAgent

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
        self._reporter = ReporterAgent()

    def processar(self, issue: IssueInput) -> IssueReport:
        tentativas = 0
        contexto_erro = ""

        while tentativas < MAX_TENTATIVAS:
            tentativas += 1
            try:
                classificacao = self._classifier.classificar(issue, contexto_erro)
                erros = validar_regras_negocio(classificacao)
                if erros:
                    contexto_erro = "; ".join(erros)
                    continue
                return self._reporter.gerar_aprovado(issue, classificacao, tentativas)
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
