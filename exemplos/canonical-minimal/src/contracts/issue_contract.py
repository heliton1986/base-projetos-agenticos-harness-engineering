from typing import Literal, Optional

from pydantic import BaseModel, field_validator, model_validator


class IssueInput(BaseModel):
    texto: str
    titulo: Optional[str] = None
    autor: Optional[str] = None
    repositorio: Optional[str] = None

    @field_validator("texto")
    @classmethod
    def texto_nao_vazio(cls, valor: str) -> str:
        if len(valor.strip()) < 10:
            raise ValueError("texto deve ter ao menos 10 caracteres")
        return valor


class IssueClassification(BaseModel):
    severidade: Literal["critica", "alta", "media", "baixa"]
    categoria: Literal["bug", "feature", "performance", "seguranca", "documentacao", "duvida"]
    justificativa: str
    confianca: Literal["alta", "media", "baixa"]

    @field_validator("justificativa")
    @classmethod
    def justificativa_minima(cls, valor: str) -> str:
        if len(valor.strip()) < 20:
            raise ValueError("justificativa deve ter ao menos 20 caracteres")
        return valor


class IssueReport(BaseModel):
    input: IssueInput
    classificacao: Optional[IssueClassification]
    timestamp_utc: str
    tentativas: int
    status: Literal["aprovado", "falhou"]
    erro: Optional[str] = None

    @field_validator("tentativas")
    @classmethod
    def tentativas_positivas(cls, valor: int) -> int:
        if valor < 1:
            raise ValueError("tentativas deve ser maior ou igual a 1")
        return valor

    @model_validator(mode="after")
    def status_consistente(self) -> "IssueReport":
        if self.status == "aprovado" and self.classificacao is None:
            raise ValueError("IssueReport aprovado exige classificacao")
        if self.status == "falhou" and not self.erro:
            raise ValueError("IssueReport falhou exige erro preenchido")
        return self
