-- Pregunta de negocio: Cuanto dinero se presta en cada calificacion de riesgo (grade)?
-- Tabla: loans (Lending Club, 2.26 millones de prestamos, todos los estados)
SELECT grade,
       count(*)                  AS prestamos,
       sum(loan_amnt)            AS monto_total,
       round(avg(loan_amnt), 0)  AS monto_promedio
FROM loans
GROUP BY grade
ORDER BY grade;
