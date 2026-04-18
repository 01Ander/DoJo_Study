# 🧪 B01 — Setup de Testing & Configuración

> **Propósito:** Documentar el flujo completo de configuración del entorno de testing para la misión B01.
> **Fecha de creación:** 2026-04-17

---

## 1. Crear y Activar el Entorno Virtual

```bash
# Navegar a la raíz de la misión
cd ~/Documents/DoJo/DoJo_Study/subjects/python/campaigns/PY-BASICO/missions/B01

# Crear el entorno virtual (si no existe)
python3 -m venv venv

# Activar el entorno virtual
source venv/bin/activate
```

**Verificación:** Deberías ver `(venv)` al inicio de tu prompt.

---

## 2. Instalar Dependencias de Testing

```bash
# Instalar pytest
pip install pytest

# Instalar mypy para type checking
pip install mypy

# (Opcional) Instalar pytest-cov para coverage reports
pip install pytest-cov
```

**Verificación:**
```bash
pytest --version
mypy --version
```

---

## 3. Crear `pyproject.toml` para Configuración de Pytest

Crea un archivo `pyproject.toml` en la raíz de la misión (`B01/`) con el siguiente contenido:

```toml
[tool.pytest.ini_options]
pythonpath = ["."]
testpaths = ["test"]
python_files = "test_*.py"
python_functions = "test_*"
addopts = "-v"

[tool.mypy]
python_version = "3.9"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
```

**¿Por qué `pythonpath = ["."]?**  
Esto le dice a pytest que resuelva los imports desde la raíz de la misión, permitiendo importar desde `src/` sin necesidad de manipular `sys.path`.

---

## 4. Estructura de Directorios Esperada

```
B01/
├── pyproject.toml          # ← Configuración de pytest y mypy
├── venv/                   # ← Entorno virtual
├── src/
│   └── etl.py              # ← Código de producción
├── test/
│   └── test_etl.py         # ← Tests unitarios
├── mock_data/
│   └── generate_mock_logs.py
├── requirements.md
├── Mini-RFC.md
└── journal.md
```

---

## 5. Comandos para Ejecutar Tests

```bash
# Asegúrate de estar en la raíz de B01 y con el venv activado
cd ~/Documents/DoJo/DoJo_Study/subjects/python/campaigns/PY-BASICO/missions/B01
source venv/bin/activate

# Correr todos los tests
pytest

# Correr tests con output detallado (verbose)
pytest -v

# Correr un test específico
pytest -v test/test_etl.py::test_normalize_date_yyyy_mm_dd_T_H_M_S

# Correr tests hasta el primer fallo (rápido para TDD)
pytest -x

# Correr tests con coverage report
pytest --cov=src --cov-report=term-missing

# Correr mypy para type checking
mypy src/
```

---

## 6. Flujo TDD Recomendado

```bash
# 1. Escribe un test fallido en test/test_etl.py
# 2. Ejecuta el test específico para ver el fallo
pytest -v test/test_etl.py::test_nombre_del_test

# 3. Implementa lo mínimo en src/etl.py para pasar el test
# 4. Ejecuta el test nuevamente para confirmar que pasa
pytest -v test/test_etl.py::test_nombre_del_test

# 5. Ejecuta todos los tests para verificar que no rompiste nada
pytest -v

# 6. Ejecuta mypy para verificar tipos
mypy src/

# 7. Commit
git add src/etl.py test/test_etl.py
git commit -m "feat: implement normalize_logs_date with TDD"
```

---

## 7. Errores Comunes y Soluciones

### `ModuleNotFoundError: No module named 'src'`
**Causa:** Falta `pyproject.toml` con `pythonpath = ["."]` o no estás en la raíz de la misión.

**Solución:**
1. Verifica que `pyproject.toml` existe en `B01/`
2. Verifica que estás ejecutando pytest desde `B01/`
3. Verifica que el venv está activado

### `SyntaxError` en los format strings de datetime
**Causa:** Usar `$` en lugar de `%` en los especificadores de formato.

**Incorrecto:**
```python
"%d-%m-%Y %H:%M:$S"  # ← $S es inválido
```

**Correcto:**
```python
"%d-%m-%Y %H:%M:%S"  # ← %S es válido
```

### El test no coincide con el formato documentado
**Causa:** El test usa un formato de fecha que la función no soporta.

**Solución:** Verifica que el formato del test coincida con:
- Lo que dice el docstring de la función
- Lo que exige el `requirements.md`

---

## 8. Checklist de Verificación Pre-Commit

- [ ] Todos los tests pasan (`pytest -v`)
- [ ] Mypy no reporta errores (`mypy src/`)
- [ ] El código sigue el DoD (tipado fuerte, docstrings en inglés)
- [ ] El journal.md está actualizado con el avance

---

## Referencias

- **Requirements.md:** Define los formatos de fecha y casos de test obligatorios
- **Mini-RFC.md:** Diseño de la arquitectura del pipeline ETL
- **Journal.md:** Bitácora de progreso y decisiones técnicas
