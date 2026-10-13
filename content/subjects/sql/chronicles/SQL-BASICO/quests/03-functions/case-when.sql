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
    emp_name,
    projects_completed,
    COALESCE(satisfaction_score, 0.0) AS score,
    CASE
        WHEN projects_completed >= 10 AND satisfaction_score >= 8.0 THEN 'Top Performer'
        WHEN projects_completed >= 5 THEN 'Solid Performer'
        ELSE 'Needs Improvement'
    END AS performance_tier,
    CASE
        WHEN satisfaction_score IS NULL THEN 'Pending Eval'
        ELSE 'Evaluated'
    END AS review_status
FROM employee_evaluations;