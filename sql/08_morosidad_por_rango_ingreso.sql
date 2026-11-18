-- Pregunta de negocio: Pagan mejor los que ganan mas?
-- Mora: Charged Off o Default, sobre prestamos terminados (ver src/creditflow/definitions.py)
WITH terminados AS (
    SELECT CASE WHEN annual_inc < 30000  THEN '1) <30k'
                WHEN annual_inc < 60000  THEN '2) 30-60k'
                WHEN annual_inc < 100000 THEN '3) 60-100k'
                ELSE                          '4) 100k+' END AS rango_ingreso,
           CASE WHEN loan_status IN ('Charged Off', 'Default') THEN 1 ELSE 0 END AS mora
    FROM loans
    WHERE loan_status IN ('Fully Paid', 'Charged Off', 'Default')
      AND annual_inc IS NOT NULL
)
SELECT rango_ingreso, count(*) AS terminados, round(100 * avg(mora), 2) AS morosidad_pct
FROM terminados
GROUP BY rango_ingreso
ORDER BY rango_ingreso;
