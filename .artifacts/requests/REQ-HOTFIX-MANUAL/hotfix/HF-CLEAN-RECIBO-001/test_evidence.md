# Test Evidence - HF-CLEAN-RECIBO-001

## Test Run Results
Command: `poetry run pytest tests/test_recibo.py -v`

**Result: PASS**

### Output
```
=========================== test session starts ===========================
platform linux -- Python 3.11.14, pytest-8.3.5, pluggy-1.6.0 -- /home/irisso/proyectos/facturacion/.venv/bin/python
cachedir: .pytest_cache
rootdir: /home/irisso/proyectos/facturacion
configfile: pyproject.toml
plugins: cov-5.0.0, mock-3.15.1, Faker-37.3.0, asyncio-1.3.0, anyio-4.9.0
asyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collected 2 items                                                         

tests/test_recibo.py::test_create_recibo_basic PASSED               [ 50%]
tests/test_recibo.py::test_create_recibo_with_imputation PASSED     [100%]

===================== 2 passed, 45 warnings in 0.05s ======================
```
