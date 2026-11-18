-- Pregunta de negocio: Donde cae cada cliente en ingreso dentro de su grade?
-- Tabla: loans (Lending Club, 2.26 millones de prestamos, todos los estados)
SELECT id, grade, annual_inc,
       round(percent_rank() OVER (PARTITION BY grade ORDER BY annual_inc), 3) AS percentil_en_grade
FROM loans
WHERE annual_inc IS NOT NULL
ORDER BY id
LIMIT 10;
