import duckdb

from creditflow.definitions import BANDERA_MORA, FILTRO_TERMINADOS


def _con_con_datos():
    con = duckdb.connect()
    con.execute(
        "CREATE TABLE loans AS SELECT * FROM "
        "(VALUES ('Fully Paid'), ('Charged Off'), ('Default'), ('Current')) t(loan_status)"
    )
    return con


def test_bandera_mora():
    con = _con_con_datos()
    filas = con.execute(f"SELECT loan_status, {BANDERA_MORA} FROM loans").fetchall()
    assert dict(filas) == {"Fully Paid": 0, "Charged Off": 1, "Default": 1, "Current": 0}


def test_filtro_excluye_current():
    con = _con_con_datos()
    n = con.execute(f"SELECT count(*) FROM loans WHERE {FILTRO_TERMINADOS}").fetchone()[0]
    assert n == 3
