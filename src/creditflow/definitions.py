"""Definiciones de negocio compartidas por consultas SQL, notebooks y pipelines."""

from pathlib import Path

import duckdb

RAIZ = Path(__file__).resolve().parents[2]
PARQUET = RAIZ / "data" / "processed" / "lending_club.parquet"

# Un prestamo esta "terminado" cuando ya sabemos como acabo. 'Current' y 'Late' aun no.
ESTADOS_TERMINADOS = ("Fully Paid", "Charged Off", "Default")
# Morosidad = el prestamo termino mal.
ESTADOS_MORA = ("Charged Off", "Default")


def _lista_sql(valores):
    return ", ".join(f"'{v}'" for v in valores)


FILTRO_TERMINADOS = f"loan_status IN ({_lista_sql(ESTADOS_TERMINADOS)})"
BANDERA_MORA = f"CASE WHEN loan_status IN ({_lista_sql(ESTADOS_MORA)}) THEN 1 ELSE 0 END"


def conectar(parquet=PARQUET):
    """Abre DuckDB en memoria y expone el Parquet como la vista `loans`."""
    con = duckdb.connect()
    con.execute(f"CREATE VIEW loans AS SELECT * FROM read_parquet('{Path(parquet).as_posix()}')")
    return con
