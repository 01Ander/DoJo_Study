CREATE TABLE company_hierarchy (
    emp_id INTEGER PRIMARY KEY,
    emp_name TEXT NOT NULL,
    job_title TEXT NOT NULL,
    manager_id INTEGER,
    FOREIGN KEY (manager_id) REFERENCES company_hierarchy(emp_id)
);

INSERT INTO company_hierarchy VALUES
(1, 'CEO Elizabeth', 'Executive', NULL),
(2, 'VP Mark', 'Executive', 1),
(3, 'Lead Dev Sarah', 'Engineering', 2),
(4, 'Junior Dev Tom', 'Engineering', 3),
(5, 'Sales Rep Kevin', 'Sales', 2);

SELECT
    e.emp_name AS employee,
    e.job_title,
    COALESCE(b.emp_name, 'Top Management') AS manager
FROM company_hierarchy AS e
LEFT JOIN company_hierarchy AS b ON e.manager_id = b.emp_id
WHERE e.job_title IN ('Engineering') OR e.emp_name = 'VP Mark';