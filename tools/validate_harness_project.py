"""
Validador de conformidade Harness Engineering.

Uso:
    python tools/validate_harness_project.py <caminho-do-projeto>

Verifica se um projeto derivado da base segue as convencoes Harness Engineering.
Retorna exit code 0 se aprovado, 1 se houver falhas criticas.
"""
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


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""


def _agent_files(root: Path) -> list[Path]:
    agents_dir = root / "src" / "agents"
    if not agents_dir.exists():
        return []
    return [
        p for p in agents_dir.glob("*.py")
        if p.name != "__init__.py"
    ]


def _is_multi_agent(root: Path) -> tuple[bool, str]:
    agent_files = _agent_files(root)
    if len(agent_files) > 1:
        return True, f"{len(agent_files)} agentes em src/agents/"

    agents_md = _read_text(root / "AGENTS.md").lower()
    gatilhos = (
        "multi-agent",
        "multi agent",
        "subagentes",
        "subagente",
        "mais de um agente",
    )
    if any(g in agents_md for g in gatilhos):
        return True, "AGENTS.md indica multi-agent/subagentes"

    return False, "agente unico ou sem sinal claro de multi-agent"


def _has_ui_api_capability(root: Path) -> tuple[bool, str]:
    sinais = [
        root / "execution" / "run_api.py",
        root / "execution" / "run_ui.py",
        root / "src" / "api",
        root / "src" / "ui",
    ]
    encontrados = [p for p in sinais if p.exists()]
    if encontrados:
        return True, ", ".join(str(p.relative_to(root)) for p in encontrados)

    texto = " ".join(
        _read_text(root / rel)
        for rel in ("README.md", "AGENTS.md")
        if (root / rel).exists()
    ).lower()
    for termo in ("fastapi", "streamlit", "chainlit"):
        if termo in texto:
            return True, f"menciona {termo} em README/AGENTS"

    return False, "sem capacidade UI/API detectada"


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


@check("contracts/ existe e contem contratos")
def check_contracts(root: Path) -> tuple[bool, str]:
    candidatos = [root / "contracts", root / "src" / "contracts"]
    existentes = [c for c in candidatos if c.exists()]
    if not existentes:
        return False, "contracts/ ausente — contratos de entrada/saida nao definidos"

    artefatos: list[Path] = []
    for pasta in existentes:
        artefatos.extend(
            p for p in pasta.glob("*")
            if p.is_file() and p.suffix in {".md", ".py"} and p.name != "__init__.py"
        )

    if not artefatos:
        return False, "contracts/ existe mas nao contem contratos em .md ou .py"

    formatos = sorted({p.suffix for p in artefatos})
    return True, f"{len(artefatos)} contrato(s) em {', '.join(formatos)}"


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


@check("implementation/ obrigatorio em projetos multi-agent")
def check_implementation(root: Path) -> tuple[bool, str]:
    multi_agent, motivo = _is_multi_agent(root)
    if not multi_agent:
        return True, f"nao se aplica — {motivo}"

    impl = root / "implementation"
    if not impl.exists():
        return False, f"implementation/ ausente — projeto multi-agent detectado ({motivo})"

    arquivos = list(impl.glob("*.md"))
    if not arquivos:
        return False, "implementation/ existe mas esta vazia (sem runbooks .md)"

    return True, f"{len(arquivos)} runbook(s) em implementation/"


@check("progress/ tem memoria operacional minima", critico=False)
def check_progress(root: Path) -> tuple[bool, str]:
    progress_dir = root / "progress"
    if not progress_dir.exists():
        return False, "progress/ ausente — memoria operacional da execucao nao registrada"

    faltando = [
        nome for nome in ("PROGRESS.md", "VALIDATION_STATUS.md")
        if not (progress_dir / nome).exists()
    ]
    if faltando:
        return False, f"progress/ falta: {', '.join(faltando)}"

    return True, "PROGRESS.md e VALIDATION_STATUS.md presentes"


@check("tests/ offline existem")
def check_tests(root: Path) -> tuple[bool, str]:
    tests_dir = root / "tests"
    if not tests_dir.exists():
        return False, "tests/ ausente — base atual exige testes offline"

    suites = [
        p for p in tests_dir.rglob("test_*.py")
        if "__pycache__" not in p.parts
    ]
    if not suites:
        return False, "tests/ existe mas nao contem suites test_*.py"

    return True, f"{len(suites)} suite(s) offline encontrada(s)"


@check("CI e coverage configurados", critico=False)
def check_ci(root: Path) -> tuple[bool, str]:
    workflow = root / ".github" / "workflows" / "tests.yml"
    coveragerc = root / ".coveragerc"

    faltando = []
    if not workflow.exists():
        faltando.append(".github/workflows/tests.yml")
    if not coveragerc.exists():
        faltando.append(".coveragerc")

    if faltando:
        return False, f"faltando: {', '.join(faltando)}"

    return True, "workflow de testes e .coveragerc presentes"


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


@check("AGENTS.md cobre regras modernas da base")
def check_agents_modern_rules(root: Path) -> tuple[bool, str]:
    agents = root / "AGENTS.md"
    if not agents.exists():
        return False, "AGENTS.md ausente"

    conteudo = _read_text(agents).lower()
    faltando = []

    if "validatoragent" not in conteudo:
        faltando.append("ValidatorAgent")
    if not re.search(r"testes offline|pytest", conteudo):
        faltando.append("testes offline")
    if not re.search(r"\bci\b|coverage|github actions", conteudo):
        faltando.append("CI/coverage")

    multi_agent, _ = _is_multi_agent(root)
    if multi_agent and "implementation/" not in conteudo:
        faltando.append("implementation/ para multi-agent")

    if faltando:
        return False, f"AGENTS.md nao cobre: {', '.join(faltando)}"

    return True, "ValidatorAgent, testes offline, CI e regras multi-agent presentes"


@check("Projetos com UI/API registram verificacao live", critico=False)
def check_live_verification(root: Path) -> tuple[bool, str]:
    tem_ui_api, motivo = _has_ui_api_capability(root)
    if not tem_ui_api:
        return True, f"nao se aplica — {motivo}"

    fontes = [
        root / "AGENTS.md",
        root / "README.md",
        root / "progress" / "PROGRESS.md",
        root / "progress" / "VALIDATION_STATUS.md",
    ]
    conteudo = "\n".join(_read_text(p).lower() for p in fontes if p.exists())

    padroes = (
        r"verificacao live",
        r"golden path",
        r"localhost:\d+",
        r"/health",
    )
    if any(re.search(p, conteudo) for p in padroes):
        return True, f"evidencia de verificacao live encontrada — {motivo}"

    return False, f"capacidade UI/API detectada ({motivo}) sem evidencia textual de verificacao live"


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
