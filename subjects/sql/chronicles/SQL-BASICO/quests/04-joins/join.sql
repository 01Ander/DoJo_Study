CREATE TABLE departments (
    id INTEGER PRIMARY KEY,
    dept_name TEXT NOT NULL
);

CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    full_name TEXT NOT NULL,
    dept_id INTEGER,
    FOREIGN KEY (dept_id) REFERENCES departments(id)
);

CREATE TABLE laptop_assignments (
    id INTEGER PRIMARY KEY,
    emp_id INTEGER NOT NULL,
    serial_number TEXT NOT NULL,
    FOREIGN KEY (emp_id) REFERENCES employees(id)
);

INSERT INTO departments VALUES (1, 'Engineering'), (2, 'Sales'), (3, 'HR');
INSERT INTO employees VALUES (101, 'Alice', 1), (102, 'Bob', 1), (103, 'Charlie', 2), (104, 'Diana', NULL);
INSERT INTO laptop_assignments VALUES (1, 101, 'SN-APPLE-001'), (2, 103, 'SN-DELL-999');

SELECT
    e.full_name AS employee_name,
    d.dept_name
FROM employees AS e
INNER JOIN departments AS d ON e.dept_id = d.id;

SELECT
    e.full_name,
    COALESCE(d.dept_name, 'Unassigned') AS dept_name,
    COALESCE(l.serial_number, 'No Laptop') AS serial_number
FROM employees AS e
LEFT JOIN departments AS d ON e.dept_id = d.id
LEFT JOIN laptop_assignments AS l ON e.id = l.emp_id