# creditflow-peru

Sistema de scoring crediticio de punta a punta, construido en 15 semanas: SQL, dbt, pipelines de ML,
MLflow, Airflow, API (FastAPI), Docker, PySpark, streaming, CI/CD y despliegue en AWS, Google Cloud y Azure.

> Estado: Semana 1 (SQL analitico sobre datos de credito).

## Datos

Dataset: [Lending Club](https://huggingface.co/datasets/codesignal/lending-club-loan-accepted) (CC0),
2.26 millones de prestamos. **Los datos no se guardan en este repositorio.**

```bash
poetry install      # crea el entorno e instala las versiones exactas de poetry.lock
make data           # descarga, convierte a Parquet (~270 MB) y borra el CSV
```

## Estructura

```
notebooks/   análisis y modelado
src/         código del pipeline (a partir de la Semana 4)
scripts/     utilidades (descarga de datos)
docs/        guía de cada semana
```

## Liberar espacio en disco

Los datos y el entorno se pueden borrar sin perder nada (se recrean con los comandos de arriba):

```bash
rmdir /s /q data\processed .venv
```
