-- Pregunta de negocio: Cuales son los 3 prestamos mas grandes de cada estado?
-- Tabla: loans (Lending Club, 2.26 millones de prestamos, todos los estados)
WITH ranked AS (
    SELECT addr_state, id, loan_amnt,
           ROW_NUMBER() OVER (PARTITION BY addr_state ORDER BY loan_amnt DESC, id) AS rn
    FROM loans
    WHERE addr_state IS NOT NULL
)
SELECT addr_state, id, loan_amnt, rn
FROM ranked
WHERE rn <= 3
ORDER BY addr_state, rn;
