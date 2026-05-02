import json
import os

from ..contracts.issue_contract import IssueClassification, IssueInput


PROMPT_TEMPLATE = """\
Voce e um agente de triagem de issues de software.

Classifique a issue abaixo seguindo EXATAMENTE estas regras:

SEVERIDADES VALIDAS: critica, alta, media, baixa
CATEGORIAS VALIDAS: bug, feature, performance, seguranca, documentacao, duvida

REGRAS:
- severidade "critica" apenas para categoria "bug" ou "seguranca"
- categoria "duvida" tem severidade maxima "baixa"
- categoria "feature" tem severidade maxima "media"
- justificativa obrigatoria (minimo 20 caracteres)
- confianca: "alta" se texto claro, "media" se ambiguo, "baixa" se muito vago

ISSUE:
{texto}

{contexto_erro}

Retorne APENAS JSON valido no formato:
{{
  "severidade": "...",
  "categoria": "...",
  "justificativa": "...",
  "confianca": "..."
}}"""


class ClassifierAgent:
    def __init__(self) -> None:
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise EnvironmentError("ANTHROPIC_API_KEY nao definida")
        try:
            import anthropic
        except ImportError as exc:
            raise ImportError("anthropic nao instalado. Execute: pip install anthropic") from exc

        self._client = anthropic.Anthropic(api_key=api_key)
        self._model = "claude-sonnet-4-6"

    @staticmethod
    def _extrair_json(conteudo: str) -> dict:
        inicio = conteudo.find("{")
        fim = conteudo.rfind("}") + 1
        if inicio == -1 or fim == 0:
            raise ValueError(f"LLM nao retornou JSON valido: {conteudo[:200]}")

        try:
            return json.loads(conteudo[inicio:fim])
        except json.JSONDecodeError as exc:
            raise ValueError(f"JSON invalido retornado pelo LLM: {conteudo[:200]}") from exc

    def classificar(self, issue: IssueInput, contexto_erro: str = "") -> IssueClassification:
        prompt = PROMPT_TEMPLATE.format(
            texto=issue.texto,
            contexto_erro=f"ERRO DA TENTATIVA ANTERIOR (corrija):\n{contexto_erro}" if contexto_erro else "",
        )

        resposta = self._client.messages.create(
            model=self._model,
            max_tokens=512,
            messages=[{"role": "user", "content": prompt}],
        )

        conteudo = resposta.content[0].text.strip()
        dados = self._extrair_json(conteudo)
        return IssueClassification(**dados)
