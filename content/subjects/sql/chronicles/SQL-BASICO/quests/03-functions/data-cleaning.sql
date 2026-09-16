CREATE TABLE raw_customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    raw_first_name TEXT,
    raw_last_name TEXT,
    signup_date TEXT,
    phone_number TEXT
);

INSERT INTO raw_customers (raw_first_name, raw_last_name, signup_date, phone_number) VALUES
('  pedro ', 'GARCIA ', '2025-03-10', '555-1234'),
('MARIA', ' lopes', '2024-11-01', NULL),
('john', 'DOE', '2026-01-15', '555-9999');

SELECT
    UPPER(TRIM(raw_first_name)) || ' ' || UPPER(TRIM(raw_last_name)),
    COALESCE(phone_number, 'No registrado') AS cleaned_phone,
    STRFTIME('%Y', signup_date) AS signup_year
FROM raw_customers
