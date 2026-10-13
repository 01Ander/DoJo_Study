#!/usr/bin/env python3
"""Runner agnóstico de SQL para DoJo Study.

Ejecuta scripts .sql en bases efímeras (SQLite in-memory) para verificar
sintaxis, delimitadores y terminadores de sentencia. Garantiza el cierre
binario del Gate de Ejecución (§5.3 del Dictamen Final Consolidado).
"""

import argparse
import sqlite3
import sys
from pathlib import Path


def test_sql_file(file_path: Path) -> bool:
    """Ejecuta un archivo .sql en una base de datos efímera en memoria."""
    try:
        sql_content = file_path.read_text(encoding="utf-8")
        conn = sqlite3.connect(":memory:")
        try:
            conn.executescript(sql_content)
        finally:
            conn.close()
        print(f"✅ PASS: {file_path}")
        return True
    except sqlite3.Error as e:
        print(f"❌ FAIL: {file_path} -> SQLite Error: {e}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"❌ FAIL: {file_path} -> Error: {e}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(description="Runner agnóstico de SQL en memoria")
    parser.add_argument("paths", nargs="+", help="Archivos .sql o directorios a escanear")
    args = parser.parse_args()

    sql_files = []
    for p_str in args.paths:
        p = Path(p_str)
        if p.is_file() and p.suffix == ".sql":
            sql_files.append(p)
        elif p.is_dir():
            sql_files.extend(sorted(p.glob("**/*.sql")))

    if not sql_files:
        print("⚠️ No se encontraron archivos .sql para evaluar.")
        sys.exit(0)

    failed = 0
    for f in sql_files:
        if not test_sql_file(f):
            failed += 1

    print(f"\n--- Resumen: {len(sql_files) - failed} pasaron, {failed} fallaron ---")
    if failed > 0:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
