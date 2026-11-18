-- Pregunta de negocio: Cuales son los segmentos mas riesgosos por estado?
-- Mora: Charged Off o Default, sobre prestamos terminados (ver src/creditflow/definitions.py)
WITH base AS (
    SELECT addr_state, grade,
           count(*) AS terminados,
           100 * avg(CASE WHEN loan_status IN ('Charged Off', 'Default') THEN 1 ELSE 0 END) AS morosidad_pct
    FROM loans
    WHERE loan_status IN ('Fully Paid', 'Charged Off', 'Default')
    GROUP BY addr_state, grade
    HAVING count(*) >= 100
),
ranked AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY addr_state ORDER BY morosidad_pct DESC) AS rn
    FROM base
)
SELECT addr_state, grade, terminados, round(morosidad_pct, 2) AS morosidad_pct, rn
FROM ranked
WHERE rn <= 3
ORDER BY addr_state, rn;
