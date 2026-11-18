-- Pregunta de negocio: En que estados se paga peor? (mas de 5000 terminados)
-- Mora: Charged Off o Default, sobre prestamos terminados (ver src/creditflow/definitions.py)
WITH terminados AS (
    SELECT addr_state,
           CASE WHEN loan_status IN ('Charged Off', 'Default') THEN 1 ELSE 0 END AS mora
    FROM loans
    WHERE loan_status IN ('Fully Paid', 'Charged Off', 'Default')
)
SELECT addr_state, count(*) AS terminados, round(100 * avg(mora), 2) AS morosidad_pct
FROM terminados
GROUP BY addr_state
HAVING count(*) > 5000
ORDER BY morosidad_pct DESC;
