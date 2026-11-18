-- Pregunta de negocio: Como sube la morosidad con la calificacion de riesgo?
-- Mora: Charged Off o Default, sobre prestamos terminados (ver src/creditflow/definitions.py)
WITH terminados AS (
    SELECT grade,
           CASE WHEN loan_status IN ('Charged Off', 'Default') THEN 1 ELSE 0 END AS mora
    FROM loans
    WHERE loan_status IN ('Fully Paid', 'Charged Off', 'Default')
)
SELECT grade, count(*) AS terminados, round(100 * avg(mora), 2) AS morosidad_pct
FROM terminados
GROUP BY grade
ORDER BY grade;
