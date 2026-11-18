"""Ejecuta un archivo .sql de la carpeta sql/ y muestra el resultado."""

import sys
from pathlib import Path

from creditflow.definitions import PARQUET, conectar


def main(ruta):
    sql = Path(ruta).read_text(encoding="utf-8")
    print(conectar(PARQUET).execute(sql).df().to_string(index=False))


if __name__ == "__main__":
    main(sys.argv[1])
