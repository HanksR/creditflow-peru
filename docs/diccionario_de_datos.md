# Diccionario de datos - Lending Club

Tabla `loans`: **151 columnas** y 2 260 668 filas (un prestamo por fila). Se genera con `python scripts/build_data_dictionary.py`.

## Idea clave: que se conoce al momento de solicitar

De las 151 columnas, **112** se conocen cuando el cliente pide el prestamo y **39** se generan **despues** (pagos, cobranza, ayudas, liquidaciones, resultado).
Para predecir mora solo se pueden usar las primeras; usar las demas es **fuga de datos (data leakage)** y da modelos que parecen perfectos pero no sirven en produccion.

## Resumen por grupo

| Grupo | Columnas | Se conoce al solicitar |
|---|---:|---|
| 1. Identificacion | 4 | Si |
| 2. Condiciones del prestamo | 16 | Si |
| 3. Resultado del prestamo | 1 | No |
| 4. Perfil del cliente | 8 | Si |
| 5. Historial crediticio (buro) | 69 | Si |
| 6. Pagos y cobranza (despues del desembolso) | 15 | No |
| 7. Segundo solicitante / solicitud conjunta | 16 | Si |
| 8. Dificultad financiera (hardship) | 15 | No |
| 9. Liquidacion de deuda (settlement) | 7 | No |

## 1. Identificacion

| Columna | Tipo | % vacios | Ejemplo | Significado |
|---|---|---:|---|---|
| `id` | BIGINT | 0.0 | 68407277 | Identificador unico del prestamo |
| `member_id` | VARCHAR | 100.0 |  | Identificador del cliente (casi siempre vacio en este archivo) |
| `url` | VARCHAR | 0.0 | https://lendingclub.com/browse/loanDetai | Enlace a la pagina del prestamo en Lending Club |
| `policy_code` | DOUBLE | 0.0 | 1.0 | Politica de publicacion del prestamo (1 = publico, 2 = no publico) |

## 2. Condiciones del prestamo

| Columna | Tipo | % vacios | Ejemplo | Significado |
|---|---|---:|---|---|
| `loan_amnt` | DOUBLE | 0.0 | 3600.0 | Monto solicitado por el cliente (USD) |
| `funded_amnt` | DOUBLE | 0.0 | 3600.0 | Monto realmente financiado (USD) |
| `funded_amnt_inv` | DOUBLE | 0.0 | 3600.0 | Monto financiado por inversionistas (USD) |
| `term` | VARCHAR | 0.0 |  36 months | Plazo: ' 36 months' o ' 60 months' (viene con un espacio al inicio) |
| `int_rate` | DOUBLE | 0.0 | 13.99 | Tasa de interes anual (%) |
| `installment` | DOUBLE | 0.0 | 123.03 | Cuota mensual (USD) |
| `grade` | VARCHAR | 0.0 | C | Calificacion de riesgo asignada por Lending Club: A (menor riesgo) a G (mayor) |
| `sub_grade` | VARCHAR | 0.0 | C4 | Subcalificacion dentro del grade (A1 a G5) |
| `issue_d` | VARCHAR | 0.0 | Dec-2015 | Mes y anio de emision, como texto ('Dec-2015') |
| `pymnt_plan` | VARCHAR | 0.0 | n | Indica si el prestamo tiene plan de pagos especial (y/n) |
| `desc` | VARCHAR | 94.4 | We knew that using our credit cards to f | Descripcion libre del cliente (casi siempre vacia) |
| `purpose` | VARCHAR | 0.0 | debt_consolidation | Motivo del prestamo (consolidar deuda, tarjeta, casa, auto...) |
| `title` | VARCHAR | 1.0 | Debt consolidation | Titulo del prestamo escrito por el cliente |
| `initial_list_status` | VARCHAR | 0.0 | w | Estado inicial de publicacion del prestamo (w / f) |
| `application_type` | VARCHAR | 0.0 | Individual | Tipo de solicitud: Individual o Joint App (conjunta) |
| `disbursement_method` | VARCHAR | 0.0 | Cash | Como se entrego el dinero: Cash o DirectPay (pago directo a acreedores) |

## 3. Resultado del prestamo

| Columna | Tipo | % vacios | Ejemplo | Significado |
|---|---|---:|---|---|
| `loan_status` | VARCHAR | 0.0 | Fully Paid | Estado actual del prestamo (Fully Paid, Charged Off, Current...). Es la variable que queremos predecir |

## 4. Perfil del cliente

| Columna | Tipo | % vacios | Ejemplo | Significado |
|---|---|---:|---|---|
| `emp_title` | VARCHAR | 7.4 | leadman | Cargo o puesto de trabajo del cliente (texto libre) |
| `emp_length` | VARCHAR | 6.5 | 10+ years | Anios de antiguedad laboral ('< 1 year' a '10+ years') |
| `home_ownership` | VARCHAR | 0.0 | MORTGAGE | Vivienda: RENT (alquila), MORTGAGE (hipoteca), OWN (propia), OTHER |
| `annual_inc` | DOUBLE | 0.0 | 55000.0 | Ingreso anual declarado (USD) |
| `verification_status` | VARCHAR | 0.0 | Not Verified | Si Lending Club verifico el ingreso: Verified, Source Verified, Not Verified |
| `zip_code` | VARCHAR | 0.0 | 190xx | Primeros 3 digitos del codigo postal ('123xx') |
| `addr_state` | VARCHAR | 0.0 | PA | Estado de residencia (EE. UU.) |
| `dti` | DOUBLE | 0.1 | 5.91 | Relacion deuda/ingreso: pagos mensuales de deuda sobre ingreso mensual (%), sin contar la hipoteca |

## 5. Historial crediticio (buro)

| Columna | Tipo | % vacios | Ejemplo | Significado |
|---|---|---:|---|---|
| `delinq_2yrs` | DOUBLE | 0.0 | 0.0 | Atrasos de 30+ dias en los ultimos 2 anios (cantidad) |
| `earliest_cr_line` | VARCHAR | 0.0 | Aug-2003 | Fecha de apertura de su primera linea de credito (texto) |
| `fico_range_low` | DOUBLE | 0.0 | 675.0 | Puntaje FICO al solicitar: limite inferior del rango |
| `fico_range_high` | DOUBLE | 0.0 | 679.0 | Puntaje FICO al solicitar: limite superior del rango |
| `inq_last_6mths` | DOUBLE | 0.0 | 1.0 | Consultas de credito en los ultimos 6 meses |
| `mths_since_last_delinq` | DOUBLE | 51.2 | 30.0 | Meses desde el ultimo atraso (vacio = nunca tuvo) |
| `mths_since_last_record` | DOUBLE | 84.1 | 106.0 | Meses desde el ultimo registro publico negativo (vacio = nunca) |
| `open_acc` | DOUBLE | 0.0 | 7.0 | Lineas de credito abiertas |
| `pub_rec` | DOUBLE | 0.0 | 0.0 | Registros publicos negativos (quiebras, juicios) |
| `revol_bal` | DOUBLE | 0.0 | 2765.0 | Saldo total de credito revolvente (tarjetas) en USD |
| `revol_util` | DOUBLE | 0.1 | 29.7 | % usado de su limite de credito revolvente |
| `total_acc` | DOUBLE | 0.0 | 13.0 | Total de lineas de credito que ha tenido (abiertas y cerradas) |
| `collections_12_mths_ex_med` | DOUBLE | 0.0 | 0.0 | Cobranzas en los ultimos 12 meses, sin contar las medicas |
| `mths_since_last_major_derog` | DOUBLE | 74.3 | 30.0 | Meses desde la ultima falta grave (90+ dias de atraso) |
| `acc_now_delinq` | DOUBLE | 0.0 | 0.0 | Cuentas actualmente en mora |
| `tot_coll_amt` | DOUBLE | 3.1 | 722.0 | Monto total que ha pasado por cobranza (USD) |
| `tot_cur_bal` | DOUBLE | 3.1 | 144904.0 | Saldo actual de todas sus cuentas (USD) |
| `open_acc_6m` | DOUBLE | 38.3 | 2.0 | Cuentas abiertas en los ultimos 6 meses |
| `open_act_il` | DOUBLE | 38.3 | 2.0 | Cuentas a plazos (installment) activas |
| `open_il_12m` | DOUBLE | 38.3 | 0.0 | Cuentas a plazos abiertas en los ultimos 12 meses |
| `open_il_24m` | DOUBLE | 38.3 | 1.0 | Cuentas a plazos abiertas en los ultimos 24 meses |
| `mths_since_rcnt_il` | DOUBLE | 40.3 | 21.0 | Meses desde que abrio su cuenta a plazos mas reciente |
| `total_bal_il` | DOUBLE | 38.3 | 4981.0 | Saldo total de cuentas a plazos (USD) |
| `il_util` | DOUBLE | 47.3 | 36.0 | Saldo sobre limite en cuentas a plazos (%) |
| `open_rv_12m` | DOUBLE | 38.3 | 3.0 | Cuentas revolventes abiertas en los ultimos 12 meses |
| `open_rv_24m` | DOUBLE | 38.3 | 3.0 | Cuentas revolventes abiertas en los ultimos 24 meses |
| `max_bal_bc` | DOUBLE | 38.3 | 722.0 | Maximo saldo en una tarjeta bancaria (USD) |
| `all_util` | DOUBLE | 38.3 | 34.0 | Uso total del credito disponible (%) |
| `total_rev_hi_lim` | DOUBLE | 3.1 | 9300.0 | Limite total de credito revolvente (USD) |
| `inq_fi` | DOUBLE | 38.3 | 3.0 | Consultas de credito de tipo financiero personal |
| `total_cu_tl` | DOUBLE | 38.3 | 1.0 | Numero de cuentas financieras 'finance trades' (por confirmar) |
| `inq_last_12m` | DOUBLE | 38.3 | 4.0 | Consultas de credito en los ultimos 12 meses |
| `acc_open_past_24mths` | DOUBLE | 2.2 | 4.0 | Cuentas abiertas en los ultimos 24 meses |
| `avg_cur_bal` | DOUBLE | 3.1 | 20701.0 | Saldo promedio por cuenta (USD) |
| `bc_open_to_buy` | DOUBLE | 3.3 | 1506.0 | Credito aun disponible en tarjetas bancarias (USD) |
| `bc_util` | DOUBLE | 3.4 | 37.2 | Uso de sus tarjetas bancarias (% del limite) |
| `chargeoff_within_12_mths` | DOUBLE | 0.0 | 0.0 | Deudas castigadas (charge-offs) en los ultimos 12 meses |
| `delinq_amnt` | DOUBLE | 0.0 | 0.0 | Monto vencido de cuentas en mora (USD) |
| `mo_sin_old_il_acct` | DOUBLE | 6.2 | 148.0 | Meses desde su cuenta a plazos mas antigua |
| `mo_sin_old_rev_tl_op` | DOUBLE | 3.1 | 128.0 | Meses desde su cuenta revolvente mas antigua |
| `mo_sin_rcnt_rev_tl_op` | DOUBLE | 3.1 | 3.0 | Meses desde su cuenta revolvente mas reciente |
| `mo_sin_rcnt_tl` | DOUBLE | 3.1 | 3.0 | Meses desde su cuenta mas reciente (de cualquier tipo) |
| `mort_acc` | DOUBLE | 2.2 | 1.0 | Numero de cuentas hipotecarias |
| `mths_since_recent_bc` | DOUBLE | 3.2 | 4.0 | Meses desde su tarjeta bancaria mas reciente |
| `mths_since_recent_bc_dlq` | DOUBLE | 77.0 | 69.0 | Meses desde el ultimo atraso en tarjeta bancaria |
| `mths_since_recent_inq` | DOUBLE | 13.1 | 4.0 | Meses desde su consulta de credito mas reciente |
| `mths_since_recent_revol_delinq` | DOUBLE | 67.3 | 69.0 | Meses desde el ultimo atraso en credito revolvente |
| `num_accts_ever_120_pd` | DOUBLE | 3.1 | 2.0 | Cuentas que alguna vez tuvieron 120+ dias de atraso |
| `num_actv_bc_tl` | DOUBLE | 3.1 | 2.0 | Tarjetas bancarias activas |
| `num_actv_rev_tl` | DOUBLE | 3.1 | 4.0 | Cuentas revolventes activas |
| `num_bc_sats` | DOUBLE | 2.6 | 2.0 | Tarjetas bancarias en buen estado (satisfactorias) |
| `num_bc_tl` | DOUBLE | 3.1 | 5.0 | Total de tarjetas bancarias |
| `num_il_tl` | DOUBLE | 3.1 | 3.0 | Total de cuentas a plazos |
| `num_op_rev_tl` | DOUBLE | 3.1 | 4.0 | Cuentas revolventes abiertas |
| `num_rev_accts` | DOUBLE | 3.1 | 9.0 | Total de cuentas revolventes |
| `num_rev_tl_bal_gt_0` | DOUBLE | 3.1 | 4.0 | Cuentas revolventes con saldo mayor a 0 |
| `num_sats` | DOUBLE | 2.6 | 7.0 | Cuentas en buen estado (satisfactorias) |
| `num_tl_120dpd_2m` | DOUBLE | 6.8 | 0.0 | Cuentas con 120+ dias de atraso en los ultimos 2 meses (por confirmar) |
| `num_tl_30dpd` | DOUBLE | 3.1 | 0.0 | Cuentas con 30 dias de atraso ahora |
| `num_tl_90g_dpd_24m` | DOUBLE | 3.1 | 0.0 | Cuentas con 90+ dias de atraso en los ultimos 24 meses |
| `num_tl_op_past_12m` | DOUBLE | 3.1 | 3.0 | Cuentas abiertas en los ultimos 12 meses |
| `pct_tl_nvr_dlq` | DOUBLE | 3.1 | 76.9 | % de cuentas que nunca tuvieron atraso |
| `percent_bc_gt_75` | DOUBLE | 3.3 | 0.0 | % de tarjetas usadas por encima del 75 % de su limite |
| `pub_rec_bankruptcies` | DOUBLE | 0.1 | 0.0 | Quiebras en registros publicos |
| `tax_liens` | DOUBLE | 0.0 | 0.0 | Embargos por deudas de impuestos |
| `tot_hi_cred_lim` | DOUBLE | 3.1 | 178050.0 | Limite de credito total mas alto (USD) |
| `total_bal_ex_mort` | DOUBLE | 2.2 | 7746.0 | Saldo total sin contar hipotecas (USD) |
| `total_bc_limit` | DOUBLE | 2.2 | 2400.0 | Limite total en tarjetas bancarias (USD) |
| `total_il_high_credit_limit` | DOUBLE | 3.1 | 13734.0 | Limite total en cuentas a plazos (USD) |

## 6. Pagos y cobranza (despues del desembolso)

| Columna | Tipo | % vacios | Ejemplo | Significado |
|---|---|---:|---|---|
| `out_prncp` | DOUBLE | 0.0 | 0.0 | Capital pendiente de pago (USD) |
| `out_prncp_inv` | DOUBLE | 0.0 | 0.0 | Capital pendiente que corresponde a inversionistas (USD) |
| `total_pymnt` | DOUBLE | 0.0 | 4421.723916800001 | Total pagado hasta hoy (USD) |
| `total_pymnt_inv` | DOUBLE | 0.0 | 4421.72 | Total pagado a inversionistas hasta hoy (USD) |
| `total_rec_prncp` | DOUBLE | 0.0 | 3600.0 | Capital recibido hasta hoy (USD) |
| `total_rec_int` | DOUBLE | 0.0 | 821.72 | Intereses recibidos hasta hoy (USD) |
| `total_rec_late_fee` | DOUBLE | 0.0 | 0.0 | Cargos por mora recibidos (USD) |
| `recoveries` | DOUBLE | 0.0 | 0.0 | Dinero recuperado despues de dar el prestamo por perdido (USD) |
| `collection_recovery_fee` | DOUBLE | 0.0 | 0.0 | Comision pagada por cobranza (USD) |
| `last_pymnt_d` | VARCHAR | 0.1 | Jan-2019 | Fecha del ultimo pago (texto) |
| `last_pymnt_amnt` | DOUBLE | 0.0 | 122.67 | Monto del ultimo pago (USD) |
| `next_pymnt_d` | VARCHAR | 59.5 | Apr-2019 | Fecha del proximo pago programado (texto) |
| `last_credit_pull_d` | VARCHAR | 0.0 | Mar-2019 | Ultima vez que se consulto su credito (texto) |
| `last_fico_range_high` | DOUBLE | 0.0 | 564.0 | FICO mas reciente: limite superior |
| `last_fico_range_low` | DOUBLE | 0.0 | 560.0 | FICO mas reciente: limite inferior |

## 7. Segundo solicitante / solicitud conjunta

| Columna | Tipo | % vacios | Ejemplo | Significado |
|---|---|---:|---|---|
| `annual_inc_joint` | DOUBLE | 94.7 | 71000.0 | Ingreso anual combinado de los dos solicitantes (USD) |
| `dti_joint` | DOUBLE | 94.7 | 13.85 | Relacion deuda/ingreso combinada (%) |
| `verification_status_joint` | VARCHAR | 94.9 | Not Verified | Estado de verificacion del ingreso combinado |
| `revol_bal_joint` | DOUBLE | 95.2 | 7101.0 | Saldo revolvente combinado (USD) |
| `sec_app_fico_range_low` | DOUBLE | 95.2 | 610.0 | FICO del segundo solicitante: inferior |
| `sec_app_fico_range_high` | DOUBLE | 95.2 | 614.0 | FICO del segundo solicitante: superior |
| `sec_app_earliest_cr_line` | VARCHAR | 95.2 | Feb-2005 | Primera linea de credito del segundo solicitante |
| `sec_app_inq_last_6mths` | DOUBLE | 95.2 | 3.0 | Consultas de credito del segundo solicitante (6 meses) |
| `sec_app_mort_acc` | DOUBLE | 95.2 | 1.0 | Cuentas hipotecarias del segundo solicitante |
| `sec_app_open_acc` | DOUBLE | 95.2 | 14.0 | Lineas abiertas del segundo solicitante |
| `sec_app_revol_util` | DOUBLE | 95.3 | 80.0 | Uso de credito revolvente del segundo solicitante (%) |
| `sec_app_open_act_il` | DOUBLE | 95.2 | 11.0 | Cuentas a plazos activas del segundo solicitante |
| `sec_app_num_rev_accts` | DOUBLE | 95.2 | 8.0 | Cuentas revolventes del segundo solicitante |
| `sec_app_chargeoff_within_12_mths` | DOUBLE | 95.2 | 0.0 | Deudas castigadas del segundo solicitante (12 meses) |
| `sec_app_collections_12_mths_ex_med` | DOUBLE | 95.2 | 2.0 | Cobranzas del segundo solicitante (12 meses, sin medicas) |
| `sec_app_mths_since_last_major_derog` | DOUBLE | 98.4 | 37.0 | Meses desde la ultima falta grave del segundo solicitante |

## 8. Dificultad financiera (hardship)

| Columna | Tipo | % vacios | Ejemplo | Significado |
|---|---|---:|---|---|
| `hardship_flag` | VARCHAR | 0.0 | N | Indica si el prestamo entro a un programa de dificultad financiera (Y/N) |
| `hardship_type` | VARCHAR | 99.5 | INTEREST ONLY-3 MONTHS DEFERRAL | Tipo de programa de ayuda |
| `hardship_reason` | VARCHAR | 99.5 | NATURAL_DISASTER | Motivo de la dificultad financiera |
| `hardship_status` | VARCHAR | 99.5 | BROKEN | Estado del programa de ayuda |
| `deferral_term` | DOUBLE | 99.5 | 3.0 | Meses de pago diferido |
| `hardship_amount` | DOUBLE | 99.5 | 47.01 | Monto de la ayuda otorgada (USD) |
| `hardship_start_date` | VARCHAR | 99.5 | Sep-2017 | Fecha de inicio de la ayuda |
| `hardship_end_date` | VARCHAR | 99.5 | Dec-2017 | Fecha de fin de la ayuda |
| `payment_plan_start_date` | VARCHAR | 99.5 | Oct-2017 | Inicio del plan de pagos de la ayuda |
| `hardship_length` | DOUBLE | 99.5 | 3.0 | Duracion de la ayuda (meses) |
| `hardship_dpd` | DOUBLE | 99.5 | 26.0 | Dias de atraso al iniciar la ayuda |
| `hardship_loan_status` | VARCHAR | 99.5 | Late (16-30 days) | Estado del prestamo durante la ayuda |
| `orig_projected_additional_accrued_interest` | DOUBLE | 99.6 | 442.41 | Interes adicional proyectado por la ayuda (USD) |
| `hardship_payoff_balance_amount` | DOUBLE | 99.5 | 3058.14 | Saldo a pagar para cerrar la ayuda (USD) |
| `hardship_last_payment_amount` | DOUBLE | 99.5 | 61.23 | Ultimo pago durante la ayuda (USD) |

## 9. Liquidacion de deuda (settlement)

| Columna | Tipo | % vacios | Ejemplo | Significado |
|---|---|---:|---|---|
| `debt_settlement_flag` | VARCHAR | 0.0 | N | Indica si el cliente negocio liquidar la deuda por menos del total (Y/N) |
| `debt_settlement_flag_date` | VARCHAR | 98.5 | Nov-2017 | Fecha en que se marco la liquidacion |
| `settlement_status` | VARCHAR | 98.5 | COMPLETE | Estado de la liquidacion |
| `settlement_date` | VARCHAR | 98.5 | Sep-2017 | Fecha de la liquidacion |
| `settlement_amount` | DOUBLE | 98.5 | 9915.0 | Monto acordado de liquidacion (USD) |
| `settlement_percentage` | DOUBLE | 98.5 | 55.0 | % de la deuda acordado en la liquidacion |
| `settlement_term` | DOUBLE | 98.5 | 1.0 | Plazo de la liquidacion (meses) |
