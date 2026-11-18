-- Pregunta de negocio: Cuantos prestamos hay en cada estado?
-- Tabla: loans (Lending Club, 2.26 millones de prestamos, todos los estados)
SELECT loan_status, count(*) AS n
FROM loans
GROUP BY loan_status
ORDER BY n DESC;
