-- Pregunta de negocio: Cuanto cambio la emision frente al mes anterior?
-- Tabla: loans (Lending Club, 2.26 millones de prestamos, todos los estados)
WITH mensual AS (
    SELECT date_trunc('month', strptime(issue_d, '%b-%Y')) AS mes, count(*) AS prestamos
    FROM loans
    GROUP BY 1
)
SELECT mes, prestamos,
       lag(prestamos) OVER (ORDER BY mes) AS mes_anterior,
       round(100.0 * (prestamos - lag(prestamos) OVER (ORDER BY mes))
             / lag(prestamos) OVER (ORDER BY mes), 1) AS variacion_pct
FROM mensual
ORDER BY mes;
