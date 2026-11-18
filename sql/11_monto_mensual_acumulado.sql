-- Pregunta de negocio: Como crecio la cartera mes a mes?
-- Tabla: loans (Lending Club, 2.26 millones de prestamos, todos los estados)
WITH mensual AS (
    SELECT date_trunc('month', strptime(issue_d, '%b-%Y')) AS mes,
           sum(loan_amnt) AS monto
    FROM loans
    GROUP BY 1
)
SELECT mes, monto, sum(monto) OVER (ORDER BY mes) AS acumulado
FROM mensual
ORDER BY mes;
