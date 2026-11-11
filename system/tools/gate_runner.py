#!/usr/bin/env python3
"""gate_runner.py — Verificador determinista del Carril B (Protocolo de Generación, docs/09).

Ejecuta las comprobaciones mecánicas de los 5 gates del
`system/docs/09-generation-protocol.md` y emite PASS/FAIL/WARN con evidencia.

No modifica archivos. No sustituye la auditoría semántica del agente `dojo-gate`:
cierra el bucle de ejecución (regla 1 del Dictamen) y las comprobaciones
estructurales que un LLM no debería estar "leyendo".

Uso:
    python3 system/tools/gate_runner.py --list
    python3 system/tools/gate_runner.py --chronicle PY-POO
    python3 system/tools/gate_runner.py --chronicle CLOUD-AWS --gate 4
    python3 system/tools/gate_runner.py --all --json
    python3 system/tools/gate_runner.py --chronicle PY-POO --no-exec   # solo estructura

Exit code: 0 si no hay FAIL; 1 si hay al menos un FAIL.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import asdict, dataclass, field
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SQL_RUNNER = REPO / "system" / "tools" / "sql_runner.py"
GATE_NAMES = {
    1: "Scope (humano)",
    2: "Lore (IA)",
    3: "Lore↔Grimoire (IA)",
    4: "Quests↔Lore (IA)",
    5: "Final Integral (humano)",
}
SKIP_DIRS = {"__pycache__", ".pytest_cache", ".mypy_cache", ".venv", "venv", "node_modules"}


# --------------------------------------------------------------------------------------
# Modelo de reporte
# --------------------------------------------------------------------------------------
@dataclass
class Check:
    gate: int
    level: str  # PASS | FAIL | WARN | SKIP
    code: str
    message: str
    path: str = ""
    detail: str = ""


@dataclass
class Report:
    chronicle: Path
    checks: list[Check] = field(default_factory=list)

    def add(self, gate: int, level: str, code: str, message: str,
            path: Path | str | None = None, detail: str = "") -> None:
        rel = ""
        if path:
            p = Path(path)
            try:
                rel = str(p.resolve().relative_to(REPO))
            except ValueError:
                rel = str(p)
        self.checks.append(Check(gate, level, code, message, rel, detail))

    def summary(self) -> dict:
        out = {"pass": 0, "fail": 0, "warn": 0, "skip": 0}
        for c in self.checks:
            out[c.level.lower()] = out.get(c.level.lower(), 0) + 1
        return out

    def result(self) -> str:
        return "FAIL" if any(c.level == "FAIL" for c in self.checks) else "PASS"


# --------------------------------------------------------------------------------------
# Utilidades
# --------------------------------------------------------------------------------------
def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(REPO))
    except ValueError:
        return str(path)


def count_code_blocks(text: str) -> int:
    return len(re.findall(r"^```", text, re.M)) // 2


def has_heading(text: str, pattern: str) -> bool:
    return bool(re.search(r"(?im)^#{1,6}\s+.*(?:" + pattern + ")", text))


def find_venv(chronicle: Path) -> Path | None:
    candidates = [chronicle / ".venv", chronicle / "rite" / ".venv"]
    quests = chronicle / "quests"
    if quests.is_dir():
        candidates.extend(sorted(quests.glob("*/.venv")))
    for venv in candidates:
        py = venv / "bin" / "python"
        if py.exists():
            return py
    return None


def run(cmd: list[str], cwd: Path, timeout: int = 180,
        extra_env: dict[str, str] | None = None) -> tuple[int, str]:
    env = None
    if extra_env:
        env = os.environ.copy()
        env.update(extra_env)
    try:
        proc = subprocess.run(
            cmd, cwd=str(cwd), capture_output=True, text=True, timeout=timeout, env=env
        )
        out = (proc.stdout or "") + (proc.stderr or "")
        return proc.returncode, out.strip()
    except subprocess.TimeoutExpired:
        return 124, f"timeout tras {timeout}s: {' '.join(cmd)}"
    except OSError as exc:
        return 127, f"no se pudo ejecutar {' '.join(cmd)}: {exc}"


def quest_dirs(chronicle: Path) -> list[Path]:
    q = chronicle / "quests"
    if not q.is_dir():
        return []
    return sorted(d for d in q.iterdir() if d.is_dir() and d.name not in SKIP_DIRS)


def lore_files(chronicle: Path) -> list[Path]:
    lo = chronicle / "lore"
    if not lo.is_dir():
        return []
    return sorted(p for p in lo.glob("*.md") if p.name not in SKIP_DIRS)


def sql_files(chronicle: Path) -> list[Path]:
    return sorted(
        p for p in chronicle.rglob("*.sql") if not any(part in SKIP_DIRS for part in p.parts)
    )


def py_files(chronicle: Path) -> list[Path]:
    return sorted(
        p for p in chronicle.rglob("*.py") if not any(part in SKIP_DIRS for part in p.parts)
    )


# --------------------------------------------------------------------------------------
# GATE 1 — Scope (estructural; lo semántico lo cierra el agente)
# --------------------------------------------------------------------------------------
def gate1(rep: Report, ch: Path) -> None:
    md = ch / "chronicle.md"
    if not md.exists():
        rep.add(1, "FAIL", "G1-CHRONICLE", "falta chronicle.md", ch)
        return
    text = read(md)
    rep.add(1, "PASS", "G1-CHRONICLE", "chronicle.md presente", md)
    if not re.search(r"(?m)^#\s+\S", text):
        rep.add(1, "FAIL", "G1-H1", "chronicle.md sin título H1", md)

    caps = len(re.findall(r"(?i)\bcap\s*\d", text))
    if caps == 0:
        rep.add(1, "WARN", "G1-CHAPTERS", "no se detectan capítulos ('Cap NN')", md)
    else:
        rep.add(1, "PASS", "G1-CHAPTERS", f"{caps} referencias a capítulos detectadas", md)

    for needle, code, label in [
        ("domain shifting", "G1-DOMAIN", "Domain Shifting"),
        ("rite", "G1-RITE", "sección del Rite"),
        ("prerequisit", "G1-PREREQ", "prerequisites"),
        ("prerrequisit", "G1-PREREQ", "prerrequisitos"),
    ]:
        if needle in text.lower():
            rep.add(1, "PASS", code, f"declara {label}", md)

    if "domain shifting" not in text.lower():
        rep.add(1, "WARN", "G1-DOMAIN", "no declara el dominio de Domain Shifting", md)
    if "rite" not in text.lower():
        rep.add(1, "FAIL", "G1-RITE", "no declara la sección del Rite", md)

    # Señales de competencias (el mapeo exacto es semántico).
    if not re.search(r"(?im)^#{2,3}\s+.*(competencia|syllabus|objetivo)", text):
        rep.add(1, "WARN", "G1-COMP", "sin sección explícita de competencias/syllabus", md)


# --------------------------------------------------------------------------------------
# GATE 2 — Lore
# --------------------------------------------------------------------------------------
def gate2(rep: Report, ch: Path) -> None:
    lore = lore_files(ch)
    if not lore:
        rep.add(2, "FAIL", "G2-LORE", "falta lore/ o está vacío", ch / "lore")
        return
    rep.add(2, "PASS", "G2-LORE", f"{len(lore)} capítulos de lore", ch / "lore")

    for f in lore:
        text = read(f)
        if not has_heading(text, r""):
            rep.add(2, "WARN", "G2-HEADINGS", f"{f.name}: sin encabezados", f)
        if "objetivo de negocio" not in text.lower():
            rep.add(2, "WARN", "G2-BIZ", f"{f.name}: sin '🎯 Objetivo de Negocio'", f)
        if not has_heading(text, r"testing|pruebas|pytest|c[oó]mo probar|test"):
            rep.add(2, "FAIL", "G2-TESTING",
                    f"{f.name}: falta sección de 'Conexión con Testing' (docs/09 PASO 4.8)", f)
        if count_code_blocks(text) == 0:
            rep.add(2, "WARN", "G2-CODE", f"{f.name}: sin bloques de código", f)

    gen = REPO / "content" / "_generation" / ch.name
    for name, code in [("matriz-trazabilidad.md", "G2-MATRIZ"), ("roadmap.md", "G2-ROADMAP")]:
        p = gen / name
        if p.exists():
            rep.add(2, "PASS", code, f"{name} presente", p)
        else:
            rep.add(2, "WARN", code,
                    f"falta content/_generation/{ch.name}/{name} (estado de generación no trazado)", gen)


# --------------------------------------------------------------------------------------
# GATE 3 — Lore↔Grimoire
# --------------------------------------------------------------------------------------
def gate3(rep: Report, ch: Path) -> None:
    g = ch / "grimoire.md"
    if not g.exists():
        rep.add(3, "FAIL", "G3-GRIMOIRE", "falta grimoire.md", ch)
        return
    text = read(g)
    rep.add(3, "PASS", "G3-GRIMOIRE", "grimoire.md presente", g)

    lore = lore_files(ch)
    questions = len(re.findall(r"(?m)^.*\?.*$", text))
    expected = 2 * len(lore)
    if lore and questions < expected:
        rep.add(3, "WARN", "G3-QUESTIONS",
                f"{questions} preguntas para {len(lore)} capítulos (esperado ≥{expected})", g)
    else:
        rep.add(3, "PASS", "G3-QUESTIONS", f"{questions} preguntas detectadas", g)

    if "auditoría del dm" not in text.lower() and "auditoria del dm" not in text.lower():
        rep.add(3, "WARN", "G3-DM", "sin sección 'Auditoría del DM'", g)
    if "friction log" not in text.lower():
        rep.add(3, "WARN", "G3-FRICTION", "sin 'Friction Log'", g)


# --------------------------------------------------------------------------------------
# GATE 4 — Quests↔Lore
# --------------------------------------------------------------------------------------
def _is_skeleton(text: str) -> bool:
    return bool(re.search(r"(?m)^\s*(pass|\.\.\.|raise NotImplementedError)\s*(#.*)?$", text)
                or "TODO" in text)


def _imports(text: str, module: str) -> bool:
    return bool(re.search(rf"(?m)^\s*(from|import)\s+{re.escape(module)}\b", text))


def run_against_reference(q: Path, python: Path, tests: list[str],
                          timeout: int = 180) -> tuple[int, str]:
    """Ejecuta tests del quest contra reference/solution.py en una copia temporal.

    Evita depender de que el Operador haya resuelto my_solution.py y evita tocar
    el repositorio: copia el quest, sustituye my_solution.py por la referencia y
    corre pytest allí.
    """
    rs = q / "reference" / "solution.py"
    if not rs.exists():
        return 127, "falta reference/solution.py"
    tmp = Path(tempfile.mkdtemp(prefix="dojo-gate-"))
    try:
        dest = tmp / q.name
        shutil.copytree(q, dest, ignore=shutil.ignore_patterns(*SKIP_DIRS))
        shutil.copyfile(dest / "reference" / "solution.py", dest / "my_solution.py")
        cmd = [str(python), "-m", "pytest", "-q", "-p", "no:cacheprovider"] + tests
        return run(cmd, cwd=dest, timeout=timeout,
                   extra_env={"PYTHONDONTWRITEBYTECODE": "1"})
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def gate4(rep: Report, ch: Path, python: Path, execute: bool) -> None:
    quests = quest_dirs(ch)
    if not quests:
        rep.add(4, "FAIL", "G4-QUESTS", "falta quests/ o está vacío", ch / "quests")
        return
    rep.add(4, "PASS", "G4-QUESTS", f"{len(quests)} quests detectadas", ch / "quests")

    lore = lore_files(ch)
    if lore and len(quests) != len(lore):
        rep.add(4, "WARN", "G4-COUNT",
                f"{len(quests)} quests vs {len(lore)} capítulos de lore", ch / "quests")

    for q in quests:
        required = [
            ("quest.md", "enunciado"),
            ("my_solution.py", "espacio del Operador"),
            ("reference/solution.py", "solución de referencia"),
            ("reference/reference_test.py", "test de referencia"),
        ]
        missing = [name for name, _ in required if not (q / name).exists()]
        if missing:
            rep.add(4, "FAIL", "G4-LAYOUT",
                    f"{q.name}: falta {', '.join(missing)} (contrato docs/09 PASO 6)", q)

        # Test del Operador
        op_tests = sorted(q.glob("test_*.py"))
        if not op_tests:
            rep.add(4, "FAIL", "G4-OPTEST", f"{q.name}: falta test_*.py del Operador", q)
        elif not any(_imports(read(t), "my_solution") for t in op_tests):
            rep.add(4, "FAIL", "G4-OPTEST-IMPORT",
                    f"{q.name}: el test del Operador no importa my_solution", q)

        # Evaluador: tras Ola 1.2 (Dictamen §1.2) debe apuntar al artefacto del Operador,
        # no a solution.py. Importar `solution` es el defecto que la auditoría detectó.
        rt = q / "reference" / "reference_test.py"
        ref_ok = False
        if rt.exists():
            rtxt = read(rt)
            if _imports(rtxt, "my_solution"):
                ref_ok = True
                rep.add(4, "PASS", "G4-REFTEST-IMPORT",
                        f"{q.name}: evaluador apunta a my_solution (Ola 1.2)", rt)
            elif _imports(rtxt, "solution"):
                rep.add(4, "FAIL", "G4-REFTEST-IMPORT",
                        f"{q.name}: evaluador importa solution; no evalúa el artefacto del Operador", rt)
            else:
                rep.add(4, "WARN", "G4-REFTEST-IMPORT",
                        f"{q.name}: evaluador sin import reconocible", rt)

        # Reference no debe ser un esqueleto
        rs = q / "reference" / "solution.py"
        if rs.exists() and _is_skeleton(read(rs)):
            rep.add(4, "FAIL", "G4-REFSKEL",
                    f"{q.name}: reference/solution.py parece esqueleto (pass/…/TODO)", rs)

        # El espacio del Operador sí debe ser un esqueleto (scaffolding real)
        ms = q / "my_solution.py"
        if ms.exists():
            if _is_skeleton(read(ms)):
                rep.add(4, "PASS", "G4-SKELETON",
                        f"{q.name}: my_solution.py es un esqueleto", ms)
            else:
                rep.add(4, "WARN", "G4-SKELETON",
                        f"{q.name}: my_solution.py no parece esqueleto (¿ya resuelto?)", ms)

        # Sintaxis Python (compile() no escribe .pyc: el gate no modifica el repo)
        for py in sorted(q.rglob("*.py")):
            if any(part in SKIP_DIRS for part in py.parts):
                continue
            code, out = run(
                [str(python), "-c",
                 "import sys; compile(open(sys.argv[1], encoding='utf-8').read(), sys.argv[1], 'exec')",
                 str(py)],
                cwd=REPO, timeout=60,
                extra_env={"PYTHONDONTWRITEBYTECODE": "1"},
            )
            if code != 0:
                # my_solution.py es trabajo del Operador: no bloquea la generación.
                level = "WARN" if py.name == "my_solution.py" else "FAIL"
                code_name = "G4-SYNTAX-OP" if level == "WARN" else "G4-SYNTAX"
                rep.add(4, level, code_name, f"{rel(py)}: no compila", py, out[-500:])

        if not execute:
            continue

        # Si el Operador ya resolvió, se ejecuta en sitio. Si no, se valida el
        # evaluador contra reference/solution.py en una copia temporal.
        ms = q / "my_solution.py"
        solved = ms.exists() and not _is_skeleton(read(ms))
        has_ref = (q / "reference" / "solution.py").exists()
        eval_test = "reference/reference_test.py" if (rt.exists() and ref_ok) else None
        op_names = [t.name for t in op_tests]

        if solved:
            if eval_test:
                code, out = run([str(python), "-m", "pytest", "-q", "-p", "no:cacheprovider",
                                 eval_test],
                                cwd=q, extra_env={"PYTHONDONTWRITEBYTECODE": "1"})
                if code == 0:
                    rep.add(4, "PASS", "G4-REFTEST-RUN",
                            f"{q.name}: evaluador en verde", rt)
                else:
                    rep.add(4, "FAIL", "G4-REFTEST-RUN",
                            f"{q.name}: evaluador falla (exit {code})", rt, out[-1500:])
            if op_names:
                code, out = run([str(python), "-m", "pytest", "-q", "-p", "no:cacheprovider"]
                                + op_names,
                                cwd=q, extra_env={"PYTHONDONTWRITEBYTECODE": "1"})
                if code == 0:
                    rep.add(4, "PASS", "G4-OPTEST-RUN",
                            f"{q.name}: test del Operador en verde", q)
                else:
                    # El artefacto del Operador no es contenido generado: si falla,
                    # se reporta como discrepancia, no como fallo del gate.
                    rep.add(4, "WARN", "G4-OPTEST-RUN",
                            f"{q.name}: test del Operador falla (exit {code}); "
                            f"discrepa del evaluador o my_solution.py está incompleto", q, out[-1500:])
        elif has_ref and (eval_test or op_names):
            tests = ([eval_test] if eval_test else []) + op_names
            code, out = run_against_reference(q, python, tests)
            if code == 0:
                rep.add(4, "PASS", "G4-REFCHECK",
                        f"{q.name}: evaluador y tests validados contra reference/solution.py", q)
            else:
                rep.add(4, "FAIL", "G4-REFCHECK",
                        f"{q.name}: evaluador/tests fallan contra reference/solution.py "
                        f"(exit {code})", q, out[-1500:])
        else:
            rep.add(4, "SKIP", "G4-REFCHECK",
                    f"{q.name}: sin my_solution resuelto ni reference/solution.py", q)


# --------------------------------------------------------------------------------------
# GATE 5 — Final Integral
# --------------------------------------------------------------------------------------
def gate5(rep: Report, ch: Path, python: Path, execute: bool, mypy: bool) -> None:
    core = {
        "chronicle.md": ch / "chronicle.md",
        "grimoire.md": ch / "grimoire.md",
        "lore/": ch / "lore",
        "quests/": ch / "quests",
        "rite/requirements.md": ch / "rite" / "requirements.md",
        "rite/journal.md": ch / "rite" / "journal.md",
    }
    for label, path in core.items():
        if path.exists():
            rep.add(5, "PASS", "G5-CORE", f"{label} presente", path)
        else:
            rep.add(5, "FAIL", "G5-CORE", f"falta {label}", path)

    req = ch / "rite" / "requirements.md"
    if req.exists():
        text = read(req)
        phases = len(re.findall(r"(?im)^#{2,4}\s+.*\bfase\b", text))
        if phases == 0:
            rep.add(5, "FAIL", "G5-PHASES", "rite/requirements.md sin fases desbloqueables", req)
        else:
            rep.add(5, "PASS", "G5-PHASES", f"{phases} fases detectadas", req)
        if not re.search(r"(?im)^#{2,4}\s+.*(criterio|aprobaci)", text):
            rep.add(5, "WARN", "G5-CRITERIA",
                    "rite/requirements.md sin sección de criterios de aprobación", req)

    # El Rite no debe traer solución/tests pre-hechos (docs/09 PASO 7).
    for bad in ("solution.py", "test_rite.py"):
        p = ch / "rite" / bad
        if p.exists():
            rep.add(5, "FAIL", "G5-RITE-ARTIFACT",
                    f"rite/{bad} no debe existir en la generación (es trabajo del Operador)", p)

    rite = ch / "rite"
    if rite.is_dir():
        extras = sorted(
            p.name for p in rite.iterdir()
            if p.name not in {"requirements.md", "journal.md"} and p.name not in SKIP_DIRS
        )
        if extras:
            shown = ", ".join(extras[:6]) + ("…" if len(extras) > 6 else "")
            rep.add(5, "WARN", "G5-RITE-EXTRA",
                    f"rite/ contiene artefactos post-generación: {shown}", rite)

    # Coherencia del índice: enlaces relativos y capítulos huérfanos.
    md = ch / "chronicle.md"
    if md.exists():
        text = read(md)
        links = []
        for raw in re.findall(r"\]\(([^)]+)\)", text):
            link = raw.split("#", 1)[0].strip()
            if not link or link.startswith(("http://", "https://", "mailto:", "#")):
                continue
            links.append((raw, md.parent / link))
        broken = [(raw, p) for raw, p in links if not p.exists()]
        if broken:
            for raw, _ in broken[:10]:
                rep.add(5, "FAIL", "G5-LINK", f"enlace roto en chronicle.md: {raw}", md)
        elif links:
            rep.add(5, "PASS", "G5-LINK", f"{len(links)} enlaces relativos válidos", md)
        orphans = [
            f.name for f in lore_files(ch)
            if f.name not in text and f.stem not in text
        ]
        if orphans:
            shown = ", ".join(orphans[:6]) + ("…" if len(orphans) > 6 else "")
            rep.add(5, "WARN", "G5-ORPHAN",
                    f"capítulos de lore no referenciados en chronicle.md: {shown}",
                    ch / "lore")

    if not execute:
        return

    # Todos los evaluadores en verde (Ola 1.2: apuntan a my_solution)
    for q in quest_dirs(ch):
        rt = q / "reference" / "reference_test.py"
        if not rt.exists():
            continue
        rtxt = read(rt)
        if _imports(rtxt, "solution"):
            rep.add(5, "FAIL", "G5-REFTEST-SCOPE",
                    f"{q.name}: evaluador importa solution; no evalúa al Operador", rt)
        elif _imports(rtxt, "my_solution"):
            ms = q / "my_solution.py"
            has_ref = (q / "reference" / "solution.py").exists()
            if ms.exists() and not _is_skeleton(read(ms)):
                code, out = run([str(python), "-m", "pytest", "-q", "-p", "no:cacheprovider",
                                 "reference/reference_test.py"],
                                cwd=q, extra_env={"PYTHONDONTWRITEBYTECODE": "1"})
                label = "evaluador en verde"
            elif has_ref:
                code, out = run_against_reference(q, python, ["reference/reference_test.py"])
                label = "evaluador validado contra reference/solution.py"
            else:
                rep.add(5, "SKIP", "G5-REFTEST",
                        f"{q.name}: sin my_solution resuelto ni reference/solution.py", ms)
                continue
            if code == 0:
                rep.add(5, "PASS", "G5-REFTEST", f"{q.name}: {label}", rt)
            else:
                rep.add(5, "FAIL", "G5-REFTEST",
                        f"{q.name}: {label} — falla (exit {code})", rt, out[-1500:])

    # SQL
    sqls = sql_files(ch)
    if sqls:
        code, out = run([sys.executable, str(SQL_RUNNER)] + [str(p) for p in sqls],
                        cwd=REPO, timeout=300,
                        extra_env={"PYTHONDONTWRITEBYTECODE": "1"})
        if code == 0:
            rep.add(5, "PASS", "G5-SQL", f"{len(sqls)} archivos .sql en verde", ch)
        else:
            rep.add(5, "FAIL", "G5-SQL", f"{len(sqls)} archivos .sql con fallos", ch, out[-2000:])

    # mypy (opcional; solo si está instalado en el venv)
    if mypy:
        targets = [str(p) for p in py_files(ch)]
        if targets:
            code, out = run([str(python), "-m", "mypy", "--ignore-missing-imports"] + targets,
                            cwd=REPO, timeout=300)
            if code == 0:
                rep.add(5, "PASS", "G5-MYPY", "mypy en verde", ch)
            else:
                rep.add(5, "WARN", "G5-MYPY", "mypy reporta hallazgos", ch, out[-2000:])


# --------------------------------------------------------------------------------------
# Descubrimiento y CLI
# --------------------------------------------------------------------------------------
def discover() -> list[Path]:
    root = REPO / "content" / "subjects"
    found = []
    for md in root.rglob("chronicle.md"):
        if any(part in SKIP_DIRS for part in md.parts):
            continue
        ch = md.parent
        if (ch / "lore").is_dir() or (ch / "quests").is_dir() or (ch / "rite").is_dir():
            found.append(ch)
    return sorted(set(found))


def resolve(target: str) -> Path:
    p = Path(target).expanduser()
    if p.is_dir() and (p / "chronicle.md").exists():
        return p.resolve()
    matches = [c for c in discover() if c.name.lower() == target.strip().lower()]
    if len(matches) == 1:
        return matches[0]
    if not matches:
        raise SystemExit(f"No encontré la chronicle {target!r}. Usa --list.")
    raise SystemExit(f"Nombre ambiguo {target!r}: {', '.join(str(m) for m in matches)}")


def render(rep: Report, gate_filter: int | None) -> str:
    lines = []
    lines.append("═" * 78)
    lines.append(f" GATE RUNNER — {rep.chronicle.name}")
    lines.append("═" * 78)
    if gate_filter is None:
        lines.append(" ⚠️  MODO DIAGNÓSTICO: 5 gates en una pasada.")
        lines.append("    No es un veredicto secuencial del protocolo. Usa --gate N.")
    gates = sorted({c.gate for c in rep.checks})
    for g in gates:
        if gate_filter and g != gate_filter:
            continue
        lines.append("")
        lines.append(f"── GATE {g}: {GATE_NAMES.get(g, '')} " + "─" * 30)
        for c in [x for x in rep.checks if x.gate == g]:
            icon = {"PASS": "✅", "FAIL": "❌", "WARN": "⚠️ ", "SKIP": "⏭️ "}[c.level]
            loc = f"  [{c.path}]" if c.path else ""
            lines.append(f"{icon} {c.level:<4} {c.code:<22} {c.message}{loc}")
            if c.detail:
                for dl in c.detail.splitlines()[-6:]:
                    lines.append(f"          │ {dl}")
    s = rep.summary()
    lines.append("")
    lines.append("─" * 78)
    lines.append(f" Resumen: {s['pass']} PASS · {s['fail']} FAIL · {s['warn']} WARN · {s['skip']} SKIP")
    lines.append(f" Resultado: {rep.result()}")
    lines.append("─" * 78)
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Verificador determinista de los gates del protocolo de generación (docs/09).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--chronicle", "-c", metavar="CODE|PATH",
                    help="chronicle a auditar (código o ruta)")
    ap.add_argument("--all", action="store_true", help="audita todas las chronicles")
    ap.add_argument("--gate", "-g", type=int, choices=[1, 2, 3, 4, 5],
                    help="ejecuta solo un gate (modo protocolo); si se omite, "
                         "modo diagnóstico de los 5")
    ap.add_argument("--json", action="store_true", help="salida JSON")
    ap.add_argument("--list", action="store_true", help="lista chronicles disponibles")
    ap.add_argument("--no-exec", action="store_true",
                    help="omite la ejecución de pytest/SQL (solo comprobaciones estructurales)")
    ap.add_argument("--mypy", action="store_true", help="incluye mypy en GATE 5")
    args = ap.parse_args()

    if args.list:
        for c in discover():
            print(c.name, "→", rel(c))
        return

    if not args.chronicle and not args.all:
        ap.error("indica --chronicle CODE o --all")

    targets = discover() if args.all else [resolve(args.chronicle)]

    reports = []
    results = []
    for ch in targets:
        rep = Report(chronicle=ch)
        python = find_venv(ch) or Path(sys.executable)
        run_gate = args.gate

        if run_gate in (None, 1):
            gate1(rep, ch)
        if run_gate in (None, 2):
            gate2(rep, ch)
        if run_gate in (None, 3):
            gate3(rep, ch)
        if run_gate in (None, 4):
            gate4(rep, ch, python, execute=not args.no_exec)
        if run_gate in (None, 5):
            gate5(rep, ch, python, execute=not args.no_exec, mypy=args.mypy)

        results.append(rep)
        if args.json:
            reports.append({
                "chronicle": ch.name,
                "path": rel(ch),
                "gate": run_gate or "all",
                "mode": "gate" if run_gate else "diagnostic",
                "result": rep.result(),
                "summary": rep.summary(),
                "checks": [asdict(c) for c in rep.checks],
            })
        else:
            print(render(rep, run_gate))

    if args.json:
        print(json.dumps(reports, ensure_ascii=False, indent=2))

    failed = any(rep.result() == "FAIL" for rep in results)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
