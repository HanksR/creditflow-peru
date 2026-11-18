-- Pregunta de negocio: En que estados se concentra el negocio?
-- Tabla: loans (Lending Club, 2.26 millones de prestamos, todos los estados)
SELECT addr_state,
       sum(loan_amnt) AS monto_total,
       RANK() OVER (ORDER BY sum(loan_amnt) DESC) AS ranking
FROM loans
GROUP BY addr_state
ORDER BY ranking
LIMIT 10;
