-- Pregunta de negocio: Como evoluciono la morosidad por anio de emision?
-- Mora: Charged Off o Default, sobre prestamos terminados (ver src/creditflow/definitions.py)
WITH terminados AS (
    SELECT year(strptime(issue_d, '%b-%Y')) AS anio,
           CASE WHEN loan_status IN ('Charged Off', 'Default') THEN 1 ELSE 0 END AS mora
    FROM loans
    WHERE loan_status IN ('Fully Paid', 'Charged Off', 'Default')
)
SELECT anio, count(*) AS terminados, round(100 * avg(mora), 2) AS morosidad_pct
FROM terminados
GROUP BY anio
ORDER BY anio;
