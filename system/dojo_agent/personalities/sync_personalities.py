#!/usr/bin/env python3
"""sync_personalities.py — genera e instala personalidades portables para Hermes y OpenCode.

Fuente canónica (una sola verdad, tool-agnostic):
    system/dojo_agent/personalities/<name>.md

Artefactos generados en `dist/`:
    dist/opencode/agents/<name>.md   -> agente OpenCode (cuerpo = system prompt)
    dist/hermes/personalities.yaml   -> bloque de referencia para pegar bajo `agent:`

Instalación:
    python3 sync_personalities.py --install-opencode        # copia agentes a .opencode/agents/
    python3 sync_personalities.py --install-hermes          # edita ~/.hermes/config.yaml
                                                            # (solo reemplaza las entradas
                                                            #  `witch`/`wizard`, con backup)

La edición de Hermes es quirúrgica: localiza la entrada de cada personalidad por su
extensión real (escalares de varias líneas incluidos) y la sustituye, sin reescribir el
resto del archivo. Valida con PyYAML que nada más cambió.
"""

from __future__ import annotations

import argparse
import copy
import os
import shutil
import sys
import time
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("Se requiere PyYAML:  pip install pyyaml")

HERE = Path(__file__).resolve().parent
DIST = HERE / "dist"
SKIP = {"README.md"}
QUOTE_CHARS = "'\""


# --------------------------------------------------------------------------------------
# Carga de la fuente canónica
# --------------------------------------------------------------------------------------
def split_frontmatter(text: str) -> tuple[dict, str]:
    """Separa el frontmatter YAML del cuerpo (el system prompt)."""
    if not text.startswith("---"):
        raise ValueError("no empieza con '---'")
    end = text.find("\n---", 3)
    if end == -1:
        raise ValueError("frontmatter sin cerrar (falta '---')")
    meta = yaml.safe_load(text[3:end]) or {}
    body = text[end + 4:]
    return meta, body.lstrip("\n").rstrip() + "\n"


def load_personas() -> list[tuple[str, dict, str]]:
    personas: list[tuple[str, dict, str]] = []
    for path in sorted(HERE.glob("*.md")):
        if path.name in SKIP:
            continue
        meta, body = split_frontmatter(path.read_text(encoding="utf-8"))
        personas.append((str(meta.get("name") or path.stem), meta, body))
    return personas


def _install_block_scalar_style() -> None:
    """Escribe los prompts multilínea como bloques literales (`|`) y no con comillas."""

    def representer(dumper, data):
        style = "|" if "\n" in data else None
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style=style)

    yaml.add_representer(str, representer, Dumper=yaml.SafeDumper)


def _dump(obj: dict) -> str:
    _install_block_scalar_style()
    return yaml.safe_dump(
        obj, sort_keys=False, allow_unicode=True, default_flow_style=False, width=1000
    )


# --------------------------------------------------------------------------------------
# Generación de artefactos
# --------------------------------------------------------------------------------------
def write_hermes(personas) -> Path:
    doc = {"personalities": {}}
    for name, meta, body in personas:
        doc["personalities"][name] = {
            "description": str(meta.get("description", "")).strip(),
            "system_prompt": body,
        }
    dumped = _dump(doc)
    indented = "\n".join(("  " + line) if line.strip() else "" for line in dumped.splitlines())
    header = (
        "# ── DoJo Study · Personalidades (GENERADO — no editar a mano) ──\n"
        "# Referencia de lo que `--install-hermes` escribe en ~/.hermes/config.yaml.\n"
        "# Fuente canónica: system/dojo_agent/personalities/*.md\n"
    )
    out = DIST / "hermes" / "personalities.yaml"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(header + indented + "\n", encoding="utf-8")
    return out


def write_opencode(personas) -> list[Path]:
    paths: list[Path] = []
    for name, meta, body in personas:
        oc = meta.get("opencode") or {}
        front: dict = {"description": str(meta.get("description", "")).strip()}
        if oc.get("mode"):
            front["mode"] = oc["mode"]
        if oc.get("model"):
            front["model"] = oc["model"]
        if oc.get("color"):
            front["color"] = oc["color"]
        fm = _dump(front).strip()
        out = DIST / "opencode" / "agents" / f"{name}.md"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(f"---\n{fm}\n---\n\n{body}", encoding="utf-8")
        paths.append(out)
    return paths


# --------------------------------------------------------------------------------------
# Instalación en Hermes (edición quirúrgica del config.yaml)
# --------------------------------------------------------------------------------------
def repo_root() -> Path:
    """Raíz del repo (donde vive `.git`), para anclar `.opencode/` sin depender del cwd."""
    for parent in (HERE, *HERE.parents):
        if (parent / ".git").exists():
            return parent
    return Path.cwd()


def _hermes_config_path(explicit: str | None) -> Path:
    if explicit:
        return Path(explicit).expanduser()
    home = os.environ.get("HERMES_HOME") or (Path.home() / ".hermes")
    return Path(home) / "config.yaml"


def _indent_of(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def _find_block(lines: list[str], key: str = "personalities:") -> tuple[int, int]:
    """Devuelve (indent_del_key, primer_hijo, fin_del_bloque)."""
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped == key or stripped.startswith(key + " ") or stripped.startswith(key + "\t"):
            indent = _indent_of(line)
            end = len(lines)
            for j in range(i + 1, len(lines)):
                s = lines[j]
                if s.strip() == "" or s.lstrip().startswith("#"):
                    continue
                if _indent_of(s) <= indent:
                    end = j
                    break
            return indent, i + 1, end
    raise ValueError(f"no encontré el bloque `{key}` en el config")


def _entry_span(lines: list[str], start: int, indent: int, name: str) -> tuple[int, int]:
    """Extensión [start, end) de la entrada `name:` (soporta escalares multilínea)."""
    after = lines[start][indent + len(name) + 1:]
    stripped = after.strip()

    if stripped == "" or stripped[0] in "|>":
        j = start + 1
        while j < len(lines):
            s = lines[j]
            if s.strip() == "":
                j += 1
                continue
            if _indent_of(s) > indent:
                j += 1
            else:
                break
        while j - 1 > start and lines[j - 1].strip() == "":
            j -= 1
        return start, j

    if stripped[0] in QUOTE_CHARS:
        quote = stripped[0]
        text = after
        k = text.index(quote) + 1
        line_no = start
        while True:
            if k < len(text):
                if text[k] == quote:
                    if k + 1 < len(text) and text[k + 1] == quote:
                        k += 2
                        continue
                    return start, line_no + 1
                k += 1
            else:
                line_no += 1
                if line_no >= len(lines):
                    raise ValueError(f"escalar sin cerrar en la entrada {name!r}")
                text += "\n" + lines[line_no]
                k += 1

    return start, start + 1


def _render_entry(name: str, meta: dict, body: str, indent: int) -> list[str]:
    doc = {name: {"description": str(meta.get("description", "")).strip(), "system_prompt": body}}
    dumped = _dump(doc)
    return [(" " * indent + line).rstrip() if line.strip() else "" for line in dumped.splitlines()]


def install_hermes(personas, config_path: Path) -> None:
    if not config_path.exists():
        sys.exit(f"No existe el config de Hermes: {config_path}")

    original_text = config_path.read_text(encoding="utf-8")
    original = yaml.safe_load(original_text)
    if not isinstance(original, dict):
        sys.exit("El config de Hermes no parsea como mapping; aborto.")

    lines = original_text.split("\n")
    for name, meta, body in personas:
        indent, first, end = _find_block(lines)
        child_indent = indent + 2
        target = " " * child_indent + name + ":"
        found = None
        for j in range(first, end):
            if lines[j].startswith(target):
                found = j
                break
        block = _render_entry(name, meta, body, child_indent)
        if found is None:
            insert_at = end
            while insert_at - 1 >= first and lines[insert_at - 1].strip() == "":
                insert_at -= 1
            lines[insert_at:insert_at] = block
        else:
            start_j, end_j = _entry_span(lines, found, child_indent, name)
            lines[start_j:end_j] = block
        print(f"  · agent.personalities.{name}: {'insertada' if found is None else 'reemplazada'}")

    new_text = "\n".join(lines)
    parsed = yaml.safe_load(new_text)
    if not isinstance(parsed, dict):
        sys.exit("El resultado no parsea como YAML; aborto (config intacto).")

    # Validación semántica: solo deben cambiar las claves target.
    expected = copy.deepcopy(original)
    for name, meta, body in personas:
        got = parsed["agent"]["personalities"][name]
        assert isinstance(got, dict), f"{name}: no quedó como mapping"
        assert got.get("description") == str(meta.get("description", "")).strip()
        assert str(got.get("system_prompt", "")).rstrip("\n") == body.rstrip("\n")
        expected["agent"]["personalities"][name] = got
    assert expected == parsed, "cambios inesperados fuera de las claves objetivo"

    backup = config_path.with_suffix(f".yaml.bak-{time.strftime('%Y%m%d-%H%M%S')}")
    shutil.copy2(config_path, backup)
    config_path.write_text(new_text, encoding="utf-8")
    print(f"[ok] Hermes   -> {config_path}  (backup: {backup.name})")


def install_opencode(dest: Path, agents: list[Path]) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    for path in agents:
        shutil.copy2(path, dest / path.name)
    print(f"[ok] OpenCode -> {dest}/  ({len(agents)} agentes)")


# --------------------------------------------------------------------------------------
def main() -> None:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--install-hermes", action="store_true",
                    help="edita ~/.hermes/config.yaml (reemplaza las entradas de cada personalidad)")
    ap.add_argument("--hermes-config", metavar="PATH", default=None,
                    help="ruta alternativa del config.yaml de Hermes")
    ap.add_argument("--install-opencode", metavar="DIR", nargs="?", const="__default__",
                    default=None,
                    help="copia los agentes a DIR (por defecto: <raíz-del-repo>/.opencode/agents)")
    args = ap.parse_args()

    personas = load_personas()
    if not personas:
        sys.exit(f"No hay personalidades canónicas en {HERE}")

    hermes = write_hermes(personas)
    agents = write_opencode(personas)

    names = ", ".join(name for name, _, _ in personas)
    print(f"[ok] {len(personas)} personalidades: {names}")
    print(f"[ok] dist     -> {hermes.relative_to(HERE)}, dist/opencode/agents/")

    if args.install_hermes:
        install_hermes(personas, _hermes_config_path(args.hermes_config))
    if args.install_opencode:
        dest = args.install_opencode
        if dest == "__default__":
            dest = str(repo_root() / ".opencode" / "agents")
        install_opencode(Path(dest), agents)


if __name__ == "__main__":
    main()
