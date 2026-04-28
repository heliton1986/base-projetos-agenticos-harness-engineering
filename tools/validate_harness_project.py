"""
Validador de conformidade Harness Engineering.

Uso:
    python tools/validate_harness_project.py <caminho-do-projeto>

Verifica se um projeto derivado da base segue as convencoes Harness Engineering.
Retorna exit code 0 se aprovado, 1 se houver falhas criticas.
"""
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable


@dataclass
class CheckResult:
    nome: str
    passou: bool
    mensagem: str
    critico: bool = True


@dataclass
class ValidacaoReport:
    projeto: str
    resultados: list[CheckResult] = field(default_factory=list)

    @property
    def aprovados(self) -> int:
        return sum(1 for r in self.resultados if r.passou)

    @property
    def reprovados(self) -> int:
        return sum(1 for r in self.resultados if not r.passou)

    @property
    def falhas_criticas(self) -> int:
        return sum(1 for r in self.resultados if not r.passou and r.critico)

    @property
    def total(self) -> int:
        return len(self.resultados)


CHECKS: list[tuple[str, bool, Callable[[Path], tuple[bool, str]]]] = []


def check(nome: str, critico: bool = True):
    def decorator(fn: Callable[[Path], tuple[bool, str]]):
        CHECKS.append((nome, critico, fn))
        return fn
    return decorator


# ── Estrutura obrigatoria ──────────────────────────────────────────────────────

@check("README.md existe")
def check_readme(root: Path) -> tuple[bool, str]:
    if (root / "README.md").exists():
        return True, "ok"
    return False, "README.md ausente"


@check("AGENTS.md existe")
def check_agents(root: Path) -> tuple[bool, str]:
    if (root / "AGENTS.md").exists():
        return True, "ok"
    return False, "AGENTS.md ausente — contrato de comportamento da LLM nao definido"


@check("directives/ existe e nao esta vazia")
def check_directives(root: Path) -> tuple[bool, str]:
    d = root / "directives"
    if not d.exists():
        return False, "directives/ ausente — diretivas do dominio nao definidas"
    arquivos = list(d.glob("*.md"))
    if not arquivos:
        return False, "directives/ existe mas esta vazia (sem .md)"
    return True, f"{len(arquivos)} arquivo(s)"


@check("spec/ existe com 01, 02, 03")
def check_spec(root: Path) -> tuple[bool, str]:
    s = root / "spec"
    if not s.exists():
        return False, "spec/ ausente"
    faltando = []
    for prefixo in ("01", "02", "03"):
        if not any(s.glob(f"{prefixo}*.md")):
            faltando.append(prefixo)
    if faltando:
        return False, f"spec/ falta: {', '.join(faltando)}-*.md"
    return True, "01, 02, 03 presentes"


@check("contracts/ existe e nao esta vazia")
def check_contracts(root: Path) -> tuple[bool, str]:
    c = root / "contracts"
    if not c.exists():
        return False, "contracts/ ausente — contratos de entrada/saida nao definidos"
    arquivos = list(c.glob("*.md"))
    if not arquivos:
        return False, "contracts/ existe mas esta vazia (sem .md)"
    return True, f"{len(arquivos)} arquivo(s)"


@check("execution/run_onboarding_flow.py existe")
def check_onboarding(root: Path) -> tuple[bool, str]:
    p = root / "execution" / "run_onboarding_flow.py"
    if p.exists():
        return True, "ok"
    return False, "execution/run_onboarding_flow.py ausente — sem smoke tests de ambiente"


@check("model_routing.yaml existe", critico=False)
def check_model_routing(root: Path) -> tuple[bool, str]:
    if (root / "model_routing.yaml").exists():
        return True, "ok"
    return False, "model_routing.yaml ausente — estrategia de modelos nao documentada"


@check(".env.example existe", critico=False)
def check_env_example(root: Path) -> tuple[bool, str]:
    if (root / ".env.example").exists():
        return True, "ok"
    return False, ".env.example ausente — variaveis de ambiente nao documentadas"


# ── Conteudo AGENTS.md ─────────────────────────────────────────────────────────

SECOES_AGENTS_OBRIGATORIAS = [
    ("Modelo Operacional", r"modelo operacional|DOE|Diretivas.*Orquestracao|doe"),
    ("Agentes e responsabilidades", r"agentes e responsabilidades|responsabilidades"),
    ("Regras que nunca", r"regras que nunca|nunca podem ser violadas"),
    ("Protocolo de execucao", r"protocolo de execucao"),
    ("Gates de aprovacao", r"gates de aprovacao|gate"),
]


@check("AGENTS.md tem secoes obrigatorias")
def check_agents_sections(root: Path) -> tuple[bool, str]:
    agents = root / "AGENTS.md"
    if not agents.exists():
        return False, "AGENTS.md ausente (verificado em check anterior)"
    conteudo = agents.read_text(encoding="utf-8").lower()
    faltando = []
    for nome, padrao in SECOES_AGENTS_OBRIGATORIAS:
        if not re.search(padrao, conteudo, re.IGNORECASE):
            faltando.append(nome)
    if faltando:
        return False, f"AGENTS.md falta secoes: {', '.join(faltando)}"
    return True, f"{len(SECOES_AGENTS_OBRIGATORIAS)} secoes presentes"


# ── Portabilidade ──────────────────────────────────────────────────────────────

PADROES_HARDCODED = [
    r"/home/\w+/",
    r"/Users/\w+/",
    r"/var/home/\w+/",
    r"C:\\Users\\",
]


@check("Sem caminhos hardcoded em .md e .yaml")
def check_no_hardcoded_paths(root: Path) -> tuple[bool, str]:
    violacoes = []
    for ext in ("*.md", "*.yaml", "*.yml", "*.py"):
        for arquivo in root.rglob(ext):
            if ".git" in arquivo.parts:
                continue
            try:
                conteudo = arquivo.read_text(encoding="utf-8")
            except Exception:
                continue
            for padrao in PADROES_HARDCODED:
                if re.search(padrao, conteudo):
                    violacoes.append(str(arquivo.relative_to(root)))
                    break
    if violacoes:
        return False, f"Caminhos hardcoded em: {', '.join(violacoes[:5])}"
    return True, "nenhum caminho hardcoded encontrado"


# ── DOE no README ──────────────────────────────────────────────────────────────

@check("README.md referencia modelo DOE", critico=False)
def check_readme_doe(root: Path) -> tuple[bool, str]:
    readme = root / "README.md"
    if not readme.exists():
        return False, "README.md ausente"
    conteudo = readme.read_text(encoding="utf-8")
    if re.search(r"DOE|Diretivas.*Orquestracao|modelo operacional", conteudo, re.IGNORECASE):
        return True, "ok"
    return False, "README.md nao menciona modelo DOE — considere adicionar secao 'Modelo Operacional DOE'"


# ── Runner ─────────────────────────────────────────────────────────────────────

def validar(caminho_projeto: str) -> ValidacaoReport:
    root = Path(caminho_projeto).resolve()
    report = ValidacaoReport(projeto=str(root))

    if not root.exists():
        print(f"ERRO: caminho nao existe: {root}")
        sys.exit(2)

    for nome, critico, fn in CHECKS:
        try:
            passou, mensagem = fn(root)
        except Exception as e:
            passou = False
            mensagem = f"excecao ao verificar: {e}"
        report.resultados.append(CheckResult(nome=nome, passou=passou, mensagem=mensagem, critico=critico))

    return report


def imprimir_report(report: ValidacaoReport) -> None:
    print("=" * 65)
    print(f"Harness Engineering — Validador de Conformidade")
    print(f"Projeto: {report.projeto}")
    print("=" * 65)

    for r in report.resultados:
        icone = "[PASS]" if r.passou else ("[FAIL]" if r.critico else "[WARN]")
        print(f"  {icone} {r.nome}")
        if not r.passou:
            print(f"         {r.mensagem}")

    print("=" * 65)
    avisos = sum(1 for r in report.resultados if not r.passou and not r.critico)
    print(f"Resultado: {report.aprovados}/{report.total} checks aprovados  |  "
          f"{report.falhas_criticas} falha(s) critica(s)  |  {avisos} aviso(s)")

    if report.falhas_criticas == 0 and avisos == 0:
        print("APROVADO — projeto em conformidade com Harness Engineering")
    elif report.falhas_criticas == 0:
        print("APROVADO COM AVISOS — conformidade basica ok, revisar avisos")
    else:
        print("REPROVADO — corrigir falhas criticas antes de continuar")


def main() -> None:
    if len(sys.argv) < 2:
        print(f"Uso: python {sys.argv[0]} <caminho-do-projeto>")
        print(f"Exemplo: python tools/validate_harness_project.py exemplos/canonical-minimal")
        sys.exit(2)

    report = validar(sys.argv[1])
    imprimir_report(report)
    sys.exit(0 if report.falhas_criticas == 0 else 1)


if __name__ == "__main__":
    main()
