-- Pregunta de negocio: Como se comporta cada cohorte trimestral por grade?
-- Mora: Charged Off o Default, sobre prestamos terminados (ver src/creditflow/definitions.py)
WITH terminados AS (
    SELECT strftime(strptime(issue_d, '%b-%Y'), '%Y') || '-Q' ||
           CAST(quarter(strptime(issue_d, '%b-%Y')) AS VARCHAR) AS cohorte,
           grade,
           CASE WHEN loan_status IN ('Charged Off', 'Default') THEN 1 ELSE 0 END AS mora
    FROM loans
    WHERE loan_status IN ('Fully Paid', 'Charged Off', 'Default')
)
SELECT cohorte,
       round(100 * avg(mora) FILTER (WHERE grade = 'A'), 1) AS A,
       round(100 * avg(mora) FILTER (WHERE grade = 'B'), 1) AS B,
       round(100 * avg(mora) FILTER (WHERE grade = 'C'), 1) AS C,
       round(100 * avg(mora) FILTER (WHERE grade = 'D'), 1) AS D,
       round(100 * avg(mora) FILTER (WHERE grade = 'E'), 1) AS E
FROM terminados
GROUP BY cohorte
ORDER BY cohorte;
