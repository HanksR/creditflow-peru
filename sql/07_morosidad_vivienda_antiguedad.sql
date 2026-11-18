-- Pregunta de negocio: Importan el tipo de vivienda y la antiguedad laboral?
-- Mora: Charged Off o Default, sobre prestamos terminados (ver src/creditflow/definitions.py)
WITH terminados AS (
    SELECT home_ownership, emp_length,
           CASE WHEN loan_status IN ('Charged Off', 'Default') THEN 1 ELSE 0 END AS mora
    FROM loans
    WHERE loan_status IN ('Fully Paid', 'Charged Off', 'Default')
)
SELECT home_ownership, emp_length, count(*) AS terminados, round(100 * avg(mora), 2) AS morosidad_pct
FROM terminados
WHERE home_ownership IN ('RENT', 'MORTGAGE', 'OWN')
GROUP BY home_ownership, emp_length
ORDER BY home_ownership, emp_length;
