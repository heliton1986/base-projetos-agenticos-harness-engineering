import json
import os
from typing import Optional

import anthropic
from pydantic import BaseModel, field_validator
from typing import Literal


class IssueInput(BaseModel):
    texto: str
    titulo: Optional[str] = None
    autor: Optional[str] = None
    repositorio: Optional[str] = None

    @field_validator("texto")
    @classmethod
    def texto_nao_vazio(cls, v: str) -> str:
        if len(v.strip()) < 10:
            raise ValueError("texto deve ter ao menos 10 caracteres")
        return v


class IssueClassification(BaseModel):
    severidade: Literal["critica", "alta", "media", "baixa"]
    categoria: Literal["bug", "feature", "performance", "seguranca", "documentacao", "duvida"]
    justificativa: str
    confianca: Literal["alta", "media", "baixa"]

    @field_validator("justificativa")
    @classmethod
    def justificativa_minima(cls, v: str) -> str:
        if len(v.strip()) < 20:
            raise ValueError("justificativa deve ter ao menos 20 caracteres")
        return v


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
        self._client = anthropic.Anthropic(api_key=api_key)
        self._model = "claude-sonnet-4-6"

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

        # extrai JSON mesmo se vier com texto ao redor
        inicio = conteudo.find("{")
        fim = conteudo.rfind("}") + 1
        if inicio == -1 or fim == 0:
            raise ValueError(f"LLM nao retornou JSON valido: {conteudo[:200]}")

        dados = json.loads(conteudo[inicio:fim])
        return IssueClassification(**dados)
