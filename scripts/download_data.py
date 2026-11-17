"""Descarga el dataset Lending Club (CC0) a data/raw/ y lo convierte a Parquet.

Uso:
    python scripts/download_data.py              # descarga (si falta) y convierte
    python scripts/download_data.py --delete-csv # ademas borra el CSV (ahorra 1.7 GB)

Los datos NO se suben a GitHub (ver .gitignore). Este script permite recrearlos
en minutos, asi que se pueden borrar sin perder nada.
"""
import argparse
import sys
import urllib.request
from pathlib import Path

import duckdb

URL = ("https://huggingface.co/datasets/codesignal/lending-club-loan-accepted/"
       "resolve/main/accepted_2007_to_2018Q4.csv")
ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "data" / "raw" / "accepted_2007_to_2018Q4.csv"
PARQUET = ROOT / "data" / "processed" / "lending_club.parquet"


def download() -> None:
    if CSV.exists():
        print(f"CSV ya existe: {CSV}")
        return
    CSV.parent.mkdir(parents=True, exist_ok=True)
    print(f"Descargando (~1.7 GB) a {CSV} ...")
    with urllib.request.urlopen(URL) as r, open(CSV, "wb") as f:
        total = int(r.headers.get("Content-Length", 0))
        done = 0
        while chunk := r.read(1 << 20):
            f.write(chunk)
            done += len(chunk)
            if total:
                print(f"\r  {done / total:6.1%}", end="", flush=True)
    print("\nDescarga lista.")


def to_parquet() -> None:
    PARQUET.parent.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect()
    # sample_size=-1 lee todo el archivo para inferir tipos; ignore_errors salta
    # las filas de pie de pagina que trae el CSV original.
    # El CSV trae 33 filas de pie de pagina (id no numerico, sin loan_status):
    # se excluyen y id pasa a BIGINT.
    con.execute(f"""
        COPY (
            SELECT * REPLACE (CAST(id AS BIGINT) AS id)
            FROM read_csv('{CSV.as_posix()}',
                          header=true, sample_size=-1, ignore_errors=true)
            WHERE TRY_CAST(id AS BIGINT) IS NOT NULL
        ) TO '{PARQUET.as_posix()}' (FORMAT parquet, COMPRESSION zstd)
    """)
    n = con.execute(f"SELECT count(*) FROM read_parquet('{PARQUET.as_posix()}')").fetchone()[0]
    print(f"Parquet listo: {PARQUET}  ({PARQUET.stat().st_size / 1e6:,.0f} MB, {n:,} filas)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--delete-csv", action="store_true",
                    help="borra el CSV (1.7 GB) tras convertir a Parquet")
    args = ap.parse_args()
    download()
    to_parquet()
    if args.delete_csv:
        CSV.unlink()
        print(f"CSV borrado: {CSV}")
    sys.exit(0)
