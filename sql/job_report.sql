SELECT
    job_number,
    SUM(hours_worked) AS total_hours
FROM
    job_register.employee_time
WHERE
    work_date >= :start_date
    AND work_date <= :end_date
    AND job_number = ANY(:job_numbers)
GROUP BY
    job_number
ORDER BY
    total_hours DESC;