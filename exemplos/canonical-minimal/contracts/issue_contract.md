# Contratos de Dados — Issue Triage Agent

Fonte executavel correspondente: `src/contracts/issue_contract.py`

## IssueInput

Entrada do sistema. Fornecida pelo chamador.

```python
class IssueInput(BaseModel):
    texto: str                        # texto livre da issue (obrigatorio)
    titulo: str | None = None         # titulo opcional
    autor: str | None = None          # autor opcional
    repositorio: str | None = None    # repositorio opcional
```

Validacao: `texto` nao pode ser vazio ou menor que 10 caracteres.

## IssueClassification

Saida do `ClassifierAgent`. Validada pelo `ValidatorAgent`.

```python
class IssueClassification(BaseModel):
    severidade: Literal["critica", "alta", "media", "baixa"]
    categoria: Literal["bug", "feature", "performance", "seguranca", "documentacao", "duvida"]
    justificativa: str                # obrigatorio, minimo 20 caracteres
    confianca: Literal["alta", "media", "baixa"]
```

Regras de validacao (alem do Pydantic):
- `severidade == "critica"` → `categoria` deve ser `"bug"` ou `"seguranca"`
- `categoria == "duvida"` → `severidade` deve ser `"baixa"`
- `categoria == "feature"` → `severidade` nao pode ser `"critica"` ou `"alta"`
- `justificativa` com menos de 20 chars → invalido

## IssueReport

Saida final do sistema. Gerada pelo `ReporterAgent`.

```python
class IssueReport(BaseModel):
    input: IssueInput
    classificacao: IssueClassification
    timestamp_utc: str                # ISO 8601
    tentativas: int                   # quantas vezes ClassifierAgent rodou
    status: Literal["aprovado", "falhou"]
    erro: str | None = None           # preenchido se status == "falhou"
```

## Invariantes do sistema

1. `IssueReport.status == "aprovado"` implica `classificacao` passou validacao Pydantic + regras de negocio
2. `tentativas` nunca excede 3
3. Se `tentativas == 3` e classificacao ainda invalida → `status = "falhou"`, `erro` preenchido
