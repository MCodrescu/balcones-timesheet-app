SELECT
    employee_name,
    job_number,
    SUM(hours_worked) AS total_hours
FROM
    job_register.employee_time
LEFT JOIN
    job_register.employees 
    USING (employee_id)
WHERE
    work_date >= :start_date
    AND work_date <= :end_date
    AND employee_id = :employee_id
GROUP BY
    employee_name, job_number
ORDER BY
    total_hours DESC;