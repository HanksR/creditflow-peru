-- Pregunta de negocio: Cuanto cambia la tasa de interes entre 36 y 60 meses?
-- Tabla: loans (Lending Club, 2.26 millones de prestamos, todos los estados)
SELECT trim(term) AS plazo, round(avg(int_rate), 2) AS tasa_promedio, count(*) AS n
FROM loans
GROUP BY 1
ORDER BY 1;
