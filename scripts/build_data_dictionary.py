"""Genera el diccionario de datos de Lending Club (151 columnas).

Salidas:
    docs/diccionario_columnas.csv   (lo lee el notebook)
    docs/diccionario_de_datos.md    (lectura en GitHub)

Uso:  python scripts/build_data_dictionary.py

Las descripciones se basan en el diccionario publico de Lending Club y en el nombre
de cada campo. Las marcadas con (por confirmar) no tienen una definicion oficial segura.
"""

from pathlib import Path

import duckdb
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PARQUET = ROOT / "data" / "processed" / "lending_club.parquet"
OUT_CSV = ROOT / "docs" / "diccionario_columnas.csv"
OUT_MD = ROOT / "docs" / "diccionario_de_datos.md"

G1 = "1. Identificacion"
G2 = "2. Condiciones del prestamo"
G3 = "3. Resultado del prestamo"
G4 = "4. Perfil del cliente"
G5 = "5. Historial crediticio (buro)"
G6 = "6. Pagos y cobranza (despues del desembolso)"
G7 = "7. Segundo solicitante / solicitud conjunta"
G8 = "8. Dificultad financiera (hardship)"
G9 = "9. Liquidacion de deuda (settlement)"

S, N = "Si", "No"

# columna: (grupo, que significa, se conoce al solicitar?)
D = {
    # ---- 1. Identificacion
    "id": (G1, "Identificador unico del prestamo", S),
    "member_id": (G1, "Identificador del cliente (casi siempre vacio en este archivo)", S),
    "url": (G1, "Enlace a la pagina del prestamo en Lending Club", S),
    "policy_code": (G1, "Politica de publicacion del prestamo (1 = publico, 2 = no publico)", S),
    # ---- 2. Condiciones del prestamo
    "loan_amnt": (G2, "Monto solicitado por el cliente (USD)", S),
    "funded_amnt": (G2, "Monto realmente financiado (USD)", S),
    "funded_amnt_inv": (G2, "Monto financiado por inversionistas (USD)", S),
    "term": (G2, "Plazo: ' 36 months' o ' 60 months' (viene con un espacio al inicio)", S),
    "int_rate": (G2, "Tasa de interes anual (%)", S),
    "installment": (G2, "Cuota mensual (USD)", S),
    "grade": (
        G2,
        "Calificacion de riesgo asignada por Lending Club: A (menor riesgo) a G (mayor)",
        S,
    ),
    "sub_grade": (G2, "Subcalificacion dentro del grade (A1 a G5)", S),
    "issue_d": (G2, "Mes y anio de emision, como texto ('Dec-2015')", S),
    "purpose": (G2, "Motivo del prestamo (consolidar deuda, tarjeta, casa, auto...)", S),
    "title": (G2, "Titulo del prestamo escrito por el cliente", S),
    "desc": (G2, "Descripcion libre del cliente (casi siempre vacia)", S),
    "pymnt_plan": (G2, "Indica si el prestamo tiene plan de pagos especial (y/n)", N),
    "initial_list_status": (G2, "Estado inicial de publicacion del prestamo (w / f)", S),
    "application_type": (G2, "Tipo de solicitud: Individual o Joint App (conjunta)", S),
    "disbursement_method": (
        G2,
        "Como se entrego el dinero: Cash o DirectPay (pago directo a acreedores)",
        S,
    ),
    # ---- 3. Resultado
    "loan_status": (
        G3,
        "Estado actual del prestamo (Fully Paid, Charged Off, Current...). Es la variable que queremos predecir",
        N,
    ),
    # ---- 4. Perfil del cliente
    "emp_title": (G4, "Cargo o puesto de trabajo del cliente (texto libre)", S),
    "emp_length": (G4, "Anios de antiguedad laboral ('< 1 year' a '10+ years')", S),
    "home_ownership": (G4, "Vivienda: RENT (alquila), MORTGAGE (hipoteca), OWN (propia), OTHER", S),
    "annual_inc": (G4, "Ingreso anual declarado (USD)", S),
    "verification_status": (
        G4,
        "Si Lending Club verifico el ingreso: Verified, Source Verified, Not Verified",
        S,
    ),
    "zip_code": (G4, "Primeros 3 digitos del codigo postal ('123xx')", S),
    "addr_state": (G4, "Estado de residencia (EE. UU.)", S),
    "dti": (
        G4,
        "Relacion deuda/ingreso: pagos mensuales de deuda sobre ingreso mensual (%), sin contar la hipoteca",
        S,
    ),
    # ---- 5. Historial crediticio
    "delinq_2yrs": (G5, "Atrasos de 30+ dias en los ultimos 2 anios (cantidad)", S),
    "earliest_cr_line": (G5, "Fecha de apertura de su primera linea de credito (texto)", S),
    "fico_range_low": (G5, "Puntaje FICO al solicitar: limite inferior del rango", S),
    "fico_range_high": (G5, "Puntaje FICO al solicitar: limite superior del rango", S),
    "inq_last_6mths": (G5, "Consultas de credito en los ultimos 6 meses", S),
    "mths_since_last_delinq": (G5, "Meses desde el ultimo atraso (vacio = nunca tuvo)", S),
    "mths_since_last_record": (
        G5,
        "Meses desde el ultimo registro publico negativo (vacio = nunca)",
        S,
    ),
    "open_acc": (G5, "Lineas de credito abiertas", S),
    "pub_rec": (G5, "Registros publicos negativos (quiebras, juicios)", S),
    "revol_bal": (G5, "Saldo total de credito revolvente (tarjetas) en USD", S),
    "revol_util": (G5, "% usado de su limite de credito revolvente", S),
    "total_acc": (G5, "Total de lineas de credito que ha tenido (abiertas y cerradas)", S),
    "collections_12_mths_ex_med": (
        G5,
        "Cobranzas en los ultimos 12 meses, sin contar las medicas",
        S,
    ),
    "mths_since_last_major_derog": (
        G5,
        "Meses desde la ultima falta grave (90+ dias de atraso)",
        S,
    ),
    "acc_now_delinq": (G5, "Cuentas actualmente en mora", S),
    "tot_coll_amt": (G5, "Monto total que ha pasado por cobranza (USD)", S),
    "tot_cur_bal": (G5, "Saldo actual de todas sus cuentas (USD)", S),
    "open_acc_6m": (G5, "Cuentas abiertas en los ultimos 6 meses", S),
    "open_act_il": (G5, "Cuentas a plazos (installment) activas", S),
    "open_il_12m": (G5, "Cuentas a plazos abiertas en los ultimos 12 meses", S),
    "open_il_24m": (G5, "Cuentas a plazos abiertas en los ultimos 24 meses", S),
    "mths_since_rcnt_il": (G5, "Meses desde que abrio su cuenta a plazos mas reciente", S),
    "total_bal_il": (G5, "Saldo total de cuentas a plazos (USD)", S),
    "il_util": (G5, "Saldo sobre limite en cuentas a plazos (%)", S),
    "open_rv_12m": (G5, "Cuentas revolventes abiertas en los ultimos 12 meses", S),
    "open_rv_24m": (G5, "Cuentas revolventes abiertas en los ultimos 24 meses", S),
    "max_bal_bc": (G5, "Maximo saldo en una tarjeta bancaria (USD)", S),
    "all_util": (G5, "Uso total del credito disponible (%)", S),
    "total_rev_hi_lim": (G5, "Limite total de credito revolvente (USD)", S),
    "inq_fi": (G5, "Consultas de credito de tipo financiero personal", S),
    "total_cu_tl": (G5, "Numero de cuentas financieras 'finance trades' (por confirmar)", S),
    "inq_last_12m": (G5, "Consultas de credito en los ultimos 12 meses", S),
    "acc_open_past_24mths": (G5, "Cuentas abiertas en los ultimos 24 meses", S),
    "avg_cur_bal": (G5, "Saldo promedio por cuenta (USD)", S),
    "bc_open_to_buy": (G5, "Credito aun disponible en tarjetas bancarias (USD)", S),
    "bc_util": (G5, "Uso de sus tarjetas bancarias (% del limite)", S),
    "chargeoff_within_12_mths": (G5, "Deudas castigadas (charge-offs) en los ultimos 12 meses", S),
    "delinq_amnt": (G5, "Monto vencido de cuentas en mora (USD)", S),
    "mo_sin_old_il_acct": (G5, "Meses desde su cuenta a plazos mas antigua", S),
    "mo_sin_old_rev_tl_op": (G5, "Meses desde su cuenta revolvente mas antigua", S),
    "mo_sin_rcnt_rev_tl_op": (G5, "Meses desde su cuenta revolvente mas reciente", S),
    "mo_sin_rcnt_tl": (G5, "Meses desde su cuenta mas reciente (de cualquier tipo)", S),
    "mort_acc": (G5, "Numero de cuentas hipotecarias", S),
    "mths_since_recent_bc": (G5, "Meses desde su tarjeta bancaria mas reciente", S),
    "mths_since_recent_bc_dlq": (G5, "Meses desde el ultimo atraso en tarjeta bancaria", S),
    "mths_since_recent_inq": (G5, "Meses desde su consulta de credito mas reciente", S),
    "mths_since_recent_revol_delinq": (G5, "Meses desde el ultimo atraso en credito revolvente", S),
    "num_accts_ever_120_pd": (G5, "Cuentas que alguna vez tuvieron 120+ dias de atraso", S),
    "num_actv_bc_tl": (G5, "Tarjetas bancarias activas", S),
    "num_actv_rev_tl": (G5, "Cuentas revolventes activas", S),
    "num_bc_sats": (G5, "Tarjetas bancarias en buen estado (satisfactorias)", S),
    "num_bc_tl": (G5, "Total de tarjetas bancarias", S),
    "num_il_tl": (G5, "Total de cuentas a plazos", S),
    "num_op_rev_tl": (G5, "Cuentas revolventes abiertas", S),
    "num_rev_accts": (G5, "Total de cuentas revolventes", S),
    "num_rev_tl_bal_gt_0": (G5, "Cuentas revolventes con saldo mayor a 0", S),
    "num_sats": (G5, "Cuentas en buen estado (satisfactorias)", S),
    "num_tl_120dpd_2m": (
        G5,
        "Cuentas con 120+ dias de atraso en los ultimos 2 meses (por confirmar)",
        S,
    ),
    "num_tl_30dpd": (G5, "Cuentas con 30 dias de atraso ahora", S),
    "num_tl_90g_dpd_24m": (G5, "Cuentas con 90+ dias de atraso en los ultimos 24 meses", S),
    "num_tl_op_past_12m": (G5, "Cuentas abiertas en los ultimos 12 meses", S),
    "pct_tl_nvr_dlq": (G5, "% de cuentas que nunca tuvieron atraso", S),
    "percent_bc_gt_75": (G5, "% de tarjetas usadas por encima del 75 % de su limite", S),
    "pub_rec_bankruptcies": (G5, "Quiebras en registros publicos", S),
    "tax_liens": (G5, "Embargos por deudas de impuestos", S),
    "tot_hi_cred_lim": (G5, "Limite de credito total mas alto (USD)", S),
    "total_bal_ex_mort": (G5, "Saldo total sin contar hipotecas (USD)", S),
    "total_bc_limit": (G5, "Limite total en tarjetas bancarias (USD)", S),
    "total_il_high_credit_limit": (G5, "Limite total en cuentas a plazos (USD)", S),
    # ---- 6. Pagos y cobranza (despues del desembolso) -> fuga de datos si se usan para predecir
    "out_prncp": (G6, "Capital pendiente de pago (USD)", N),
    "out_prncp_inv": (G6, "Capital pendiente que corresponde a inversionistas (USD)", N),
    "total_pymnt": (G6, "Total pagado hasta hoy (USD)", N),
    "total_pymnt_inv": (G6, "Total pagado a inversionistas hasta hoy (USD)", N),
    "total_rec_prncp": (G6, "Capital recibido hasta hoy (USD)", N),
    "total_rec_int": (G6, "Intereses recibidos hasta hoy (USD)", N),
    "total_rec_late_fee": (G6, "Cargos por mora recibidos (USD)", N),
    "recoveries": (G6, "Dinero recuperado despues de dar el prestamo por perdido (USD)", N),
    "collection_recovery_fee": (G6, "Comision pagada por cobranza (USD)", N),
    "last_pymnt_d": (G6, "Fecha del ultimo pago (texto)", N),
    "last_pymnt_amnt": (G6, "Monto del ultimo pago (USD)", N),
    "next_pymnt_d": (G6, "Fecha del proximo pago programado (texto)", N),
    "last_credit_pull_d": (G6, "Ultima vez que se consulto su credito (texto)", N),
    "last_fico_range_high": (G6, "FICO mas reciente: limite superior", N),
    "last_fico_range_low": (G6, "FICO mas reciente: limite inferior", N),
    # ---- 7. Segundo solicitante
    "annual_inc_joint": (G7, "Ingreso anual combinado de los dos solicitantes (USD)", S),
    "dti_joint": (G7, "Relacion deuda/ingreso combinada (%)", S),
    "verification_status_joint": (G7, "Estado de verificacion del ingreso combinado", S),
    "revol_bal_joint": (G7, "Saldo revolvente combinado (USD)", S),
    "sec_app_fico_range_low": (G7, "FICO del segundo solicitante: inferior", S),
    "sec_app_fico_range_high": (G7, "FICO del segundo solicitante: superior", S),
    "sec_app_earliest_cr_line": (G7, "Primera linea de credito del segundo solicitante", S),
    "sec_app_inq_last_6mths": (G7, "Consultas de credito del segundo solicitante (6 meses)", S),
    "sec_app_mort_acc": (G7, "Cuentas hipotecarias del segundo solicitante", S),
    "sec_app_open_acc": (G7, "Lineas abiertas del segundo solicitante", S),
    "sec_app_revol_util": (G7, "Uso de credito revolvente del segundo solicitante (%)", S),
    "sec_app_open_act_il": (G7, "Cuentas a plazos activas del segundo solicitante", S),
    "sec_app_num_rev_accts": (G7, "Cuentas revolventes del segundo solicitante", S),
    "sec_app_chargeoff_within_12_mths": (
        G7,
        "Deudas castigadas del segundo solicitante (12 meses)",
        S,
    ),
    "sec_app_collections_12_mths_ex_med": (
        G7,
        "Cobranzas del segundo solicitante (12 meses, sin medicas)",
        S,
    ),
    "sec_app_mths_since_last_major_derog": (
        G7,
        "Meses desde la ultima falta grave del segundo solicitante",
        S,
    ),
    # ---- 8. Hardship
    "hardship_flag": (
        G8,
        "Indica si el prestamo entro a un programa de dificultad financiera (Y/N)",
        N,
    ),
    "hardship_type": (G8, "Tipo de programa de ayuda", N),
    "hardship_reason": (G8, "Motivo de la dificultad financiera", N),
    "hardship_status": (G8, "Estado del programa de ayuda", N),
    "deferral_term": (G8, "Meses de pago diferido", N),
    "hardship_amount": (G8, "Monto de la ayuda otorgada (USD)", N),
    "hardship_start_date": (G8, "Fecha de inicio de la ayuda", N),
    "hardship_end_date": (G8, "Fecha de fin de la ayuda", N),
    "payment_plan_start_date": (G8, "Inicio del plan de pagos de la ayuda", N),
    "hardship_length": (G8, "Duracion de la ayuda (meses)", N),
    "hardship_dpd": (G8, "Dias de atraso al iniciar la ayuda", N),
    "hardship_loan_status": (G8, "Estado del prestamo durante la ayuda", N),
    "orig_projected_additional_accrued_interest": (
        G8,
        "Interes adicional proyectado por la ayuda (USD)",
        N,
    ),
    "hardship_payoff_balance_amount": (G8, "Saldo a pagar para cerrar la ayuda (USD)", N),
    "hardship_last_payment_amount": (G8, "Ultimo pago durante la ayuda (USD)", N),
    # ---- 9. Settlement
    "debt_settlement_flag": (
        G9,
        "Indica si el cliente negocio liquidar la deuda por menos del total (Y/N)",
        N,
    ),
    "debt_settlement_flag_date": (G9, "Fecha en que se marco la liquidacion", N),
    "settlement_status": (G9, "Estado de la liquidacion", N),
    "settlement_date": (G9, "Fecha de la liquidacion", N),
    "settlement_amount": (G9, "Monto acordado de liquidacion (USD)", N),
    "settlement_percentage": (G9, "% de la deuda acordado en la liquidacion", N),
    "settlement_term": (G9, "Plazo de la liquidacion (meses)", N),
}


def build() -> pd.DataFrame:
    con = duckdb.connect()
    con.execute(f"CREATE VIEW loans AS SELECT * FROM read_parquet('{PARQUET.as_posix()}')")
    cols = con.execute("DESCRIBE loans").df()[["column_name", "column_type"]]

    faltan = set(cols.column_name) - set(D)
    sobran = set(D) - set(cols.column_name)
    assert not faltan and not sobran, f"Sin describir: {sorted(faltan)} | Sobran: {sorted(sobran)}"

    # 1) % de vacios sobre TODAS las filas: una sola pasada (count(col) cuenta no nulos)
    total = con.execute("SELECT count(*) FROM loans").fetchone()[0]
    nonnull = con.execute(
        "SELECT " + ", ".join(f'count("{c}")' for c in cols.column_name) + " FROM loans"
    ).fetchone()

    # 2) valores distintos sobre una muestra de 200 000 filas (aproximado, barato)
    con.execute(
        "CREATE TEMP TABLE muestra AS SELECT * FROM loans USING SAMPLE 200000 ROWS (reservoir, 42)"
    )
    distintos = con.execute(
        "SELECT " + ", ".join(f'count(DISTINCT "{c}")' for c in cols.column_name) + " FROM muestra"
    ).fetchone()

    out = []
    for i, r in enumerate(cols.itertuples()):
        grupo, desc, antes = D[r.column_name]
        # 3) ejemplo: primer valor no nulo (la consulta se detiene en cuanto lo encuentra)
        ej = con.execute(
            f'SELECT "{r.column_name}" FROM loans WHERE "{r.column_name}" IS NOT NULL LIMIT 1'
        ).fetchone()
        out.append(
            {
                "orden": i + 1,
                "columna": r.column_name,
                "grupo": grupo,
                "tipo": r.column_type,
                "se_conoce_al_solicitar": antes,
                "pct_vacios": round(100 * (1 - nonnull[i] / total), 1),
                "valores_distintos_muestra": distintos[i],
                "ejemplo": "" if ej is None else str(ej[0])[:40],
                "descripcion": desc,
            }
        )
    return pd.DataFrame(out)


def to_markdown(df: pd.DataFrame) -> str:
    n_sol = (df.se_conoce_al_solicitar == "Si").sum()
    L = [
        "# Diccionario de datos - Lending Club",
        "",
        f"Tabla `loans`: **{len(df)} columnas** y 2 260 668 filas (un prestamo por fila). "
        "Se genera con `python scripts/build_data_dictionary.py`.",
        "",
        "## Idea clave: que se conoce al momento de solicitar",
        "",
        f"De las {len(df)} columnas, **{n_sol}** se conocen cuando el cliente pide el prestamo y "
        f"**{len(df) - n_sol}** se generan **despues** (pagos, cobranza, ayudas, liquidaciones, resultado).",
        "Para predecir mora solo se pueden usar las primeras; usar las demas es **fuga de datos "
        "(data leakage)** y da modelos que parecen perfectos pero no sirven en produccion.",
        "",
        "## Resumen por grupo",
        "",
        "| Grupo | Columnas | Se conoce al solicitar |",
        "|---|---:|---|",
    ]
    for g, sub in df.groupby("grupo"):
        L.append(f"| {g} | {len(sub)} | {sub.se_conoce_al_solicitar.iloc[0]} |")
    L.append("")
    for g, sub in df.groupby("grupo"):
        L += [
            f"## {g}",
            "",
            "| Columna | Tipo | % vacios | Ejemplo | Significado |",
            "|---|---|---:|---|---|",
        ]
        for r in sub.itertuples():
            ej = r.ejemplo.replace("|", "/")
            L.append(f"| `{r.columna}` | {r.tipo} | {r.pct_vacios} | {ej} | {r.descripcion} |")
        L.append("")
    return "\n".join(L)


if __name__ == "__main__":
    df = build()
    OUT_CSV.parent.mkdir(exist_ok=True)
    df.to_csv(OUT_CSV, index=False, encoding="utf-8")
    OUT_MD.write_text(to_markdown(df), encoding="utf-8")
    print(f"{len(df)} columnas -> {OUT_CSV.name} y {OUT_MD.name}")
