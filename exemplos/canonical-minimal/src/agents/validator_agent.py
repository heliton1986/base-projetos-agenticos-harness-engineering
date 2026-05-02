from typing import Any

from pydantic import BaseModel, ValidationError

from ..contracts.issue_contract import IssueClassification, IssueInput, IssueReport


CONTRACTS: dict[str, type[BaseModel]] = {
    "IssueInput": IssueInput,
    "IssueClassification": IssueClassification,
    "IssueReport": IssueReport,
}


class ValidationResult(BaseModel):
    valido: bool
    contrato_validado: str
    erros: list[str] = []


class ValidatorAgent:
    def validar_payload(self, contrato_validado: str, payload: Any) -> ValidationResult:
        contrato = CONTRACTS.get(contrato_validado)
        if contrato is None:
            return ValidationResult(
                valido=False,
                contrato_validado=contrato_validado,
                erros=[f"contrato desconhecido: {contrato_validado}"],
            )

        try:
            contrato.model_validate(payload)
            return ValidationResult(valido=True, contrato_validado=contrato_validado)
        except ValidationError as exc:
            return ValidationResult(
                valido=False,
                contrato_validado=contrato_validado,
                erros=[erro["msg"] for erro in exc.errors()],
            )

    def validar_instancia(self, instancia: Any) -> ValidationResult:
        for nome_contrato, contrato in CONTRACTS.items():
            if isinstance(instancia, contrato):
                return self.validar_payload(nome_contrato, instancia.model_dump())

        return ValidationResult(
            valido=False,
            contrato_validado=type(instancia).__name__,
            erros=["tipo de instancia nao suportado pelo ValidatorAgent"],
        )
