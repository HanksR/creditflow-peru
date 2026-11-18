# creditflow-peru

Sistema de scoring crediticio de punta a punta, construido en 15 semanas: dbt, pipelines de ML,
MLflow, Airflow, API (FastAPI), Docker, PySpark, streaming, CI/CD y despliegue en AWS,
Google Cloud y Azure.

> Estado: **Semana 1 completada** (estructura del repositorio, herramientas y definición de mora).
> Siguiente: Semana 2 (Docker y PostgreSQL). El análisis exploratorio (EDA) llegará en un notebook.

## Problema de negocio

Un banco o una fintech debe decidir a quién prestar. Si predice bien quién no pagará, reduce pérdidas
sin rechazar a buenos clientes. Este repositorio construye ese sistema por etapas; la Semana 1 deja los
datos entendidos y la definición de mora escrita en código y protegida por pruebas.

## Datos

[Lending Club](https://huggingface.co/datasets/codesignal/lending-club-loan-accepted) (licencia CC0):
2.26 millones de préstamos y 151 columnas. **Los datos no se guardan en este repositorio.**

```bash
poetry install      # crea el entorno e instala las versiones exactas de poetry.lock
make data           # descarga, convierte a Parquet (~270 MB) y borra el CSV
make test
```

## Definición de mora

- **Mora** = el préstamo terminó como `Charged Off` o `Default`.
- Se mide solo sobre préstamos **terminados** (`Fully Paid`, `Charged Off`, `Default`).
- Se excluyen `Current`, `Late` e `In Grace Period` (aún no sabemos cómo terminan) y 2 749 préstamos
  antiguos marcados `Does not meet the credit policy`.
- La definición vive en `src/creditflow/definitions.py` y está protegida por pruebas.

## Calidad de datos

- `member_id` está 100 % vacía.
- 112 columnas se conocen al solicitar el préstamo y 39 son posteriores: usarlas para predecir
  sería *data leakage* (se trata en la Semana 4).

## Decisiones técnicas

- **DuckDB + Parquet:** el CSV de 1.7 GB pasa a 269 MB y se consulta sin cargar una base de datos.
- **Poetry:** `poetry.lock` fija las versiones exactas; cualquiera reproduce el entorno.
- **pre-commit + ruff:** formatea el código y bloquea archivos grandes y claves antes de cada commit.
- **Datos fuera de Git:** un script los descarga y convierte; se pueden borrar y recrear.

## Rendimiento

Leer 3 columnas de las 151 tarda 0.05 s frente a 1.94 s leyéndolas todas (mejor de 3 lecturas sobre
los préstamos de grade A). Parquet es columnar: solo lee las columnas que necesita.

## Estructura

```
src/creditflow/   definición de mora y conexión a los datos
tests/            pruebas de la definición de mora
scripts/          descarga de datos y generación del diccionario de datos
docs/             diccionario de datos (151 columnas)
```

## Hoja de ruta

Semana 2 Docker y PostgreSQL · 3 dbt y modelo en estrella · 4 pipeline de ML y MLflow ·
5 Airflow y calidad de datos · 6 monitoreo y SHAP · 7 API y Streamlit · 8 PySpark ·
9 streaming y lakehouse · 10 CI/CD · 11 AWS · 12 SageMaker y Terraform · 13 Google Cloud ·
14 Azure · 15 portafolio.

## Liberar espacio en disco

Los datos y el entorno se pueden borrar sin perder nada (se recrean con los comandos de arriba):

```bash
rmdir /s /q data\processed .venv
```
