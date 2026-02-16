SELECT
    job_number,
    employee_name,
    SUM(hours_worked) AS total_hours
FROM
    job_register.employee_time
LEFT JOIN
    job_register.employees 
    USING (employee_id)
WHERE
    work_date >= :start_date
    AND work_date <= :end_date
    AND job_number = ANY(:job_numbers)
GROUP BY
    job_number, employee_name
ORDER BY
    total_hours DESC;