CREATE TABLE employee_evaluations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    emp_name TEXT NOT NULL,
    projects_completed INTEGER NOT NULL,
    satisfaction_score REAL -- 0.0 a 10.0
);

INSERT INTO employee_evaluations (emp_name, projects_completed, satisfaction_score) VALUES
('Carlos V', 12, 9.5),
('Ana G', 4, 7.0),
('Luis M', 0, NULL),
('Elena P', 8, 8.2),
('Sofia R', 15, 6.5);


SELECT
    id,
    emp_name,
    projects_completed,
    CASE
        WHEN projects_completed >= 10 THEN 