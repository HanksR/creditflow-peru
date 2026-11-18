.PHONY: help setup data notebook lint format test hooks clean-data
help:
	@echo make setup      - instala dependencias y activa pre-commit
	@echo make data       - descarga y convierte los datos a Parquet
	@echo make notebook   - abre Jupyter Lab
	@echo make lint       - revisa el codigo con ruff
	@echo make format     - formatea el codigo con ruff
	@echo make test       - corre las pruebas
	@echo make hooks      - corre pre-commit en todos los archivos
	@echo make clean-data - borra los datos procesados
setup:
	poetry install
	poetry run pre-commit install
data:
	poetry run python scripts/download_data.py --delete-csv
notebook:
	poetry run jupyter lab
lint:
	poetry run ruff check .
format:
	poetry run ruff format .
test:
	poetry run pytest
hooks:
	poetry run pre-commit run --all-files
clean-data:
	poetry run python -c "import shutil; shutil.rmtree('data/processed', ignore_errors=True)"
