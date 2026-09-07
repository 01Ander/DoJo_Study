CREATE TABLE enrolled_2025 (
    student_id INTEGER PRIMARY KEY,
    student_name TEXT
);

CREATE TABLE enrolled_2026 (
    student_id INTEGER PRIMARY KEY,
    student_name TEXT
);

INSERT INTO enrolled_2025 VALUES (1, 'Alice'), (2, 'Bob'), (3, 'Charlie');
INSERT INTO enrolled_2026 VALUES (2, 'Bob'), (4, 'David');

SELECT student_id, student_name FROM enrolled_2025
EXCEPT
SELECT student_id, student_name FROM enrolled_2026;

WITH AllStudents AS (
    SELECT student_id, student_name FROM enrolled_2025
    UNION
    SELECT student_id, student_name FROM enrolled_2026
)
SELECT
    student_id,
    student_name,
    ROW_NUMBER() OVER(ORDER BY student_name ASC) AS global_list_num
FROM AllStudents;