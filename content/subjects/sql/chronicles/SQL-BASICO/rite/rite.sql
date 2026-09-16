-- fase 1

CREATE TABLE authors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    country TEXT NOT NULL
);

CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    isbn INTEGER NOT NULL UNIQUE,
    title TEXT NOT NULL,
    publication_year INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

CREATE TABLE book_authors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    author_id INTEGER NOT NULL,
    book_id INTEGER NOT NULL,
    FOREIGN KEY (author_id) REFERENCES authors(id),
    FOREIGN KEY (book_id) REFERENCES books(id),
    UNIQUE(author_id, book_id)
);

CREATE TABLE members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    join_date TEXT NOT NULL,
    status TEXT DEFAULT 'Active'
);

CREATE TABLE loans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER NOT NULL,
    member_id INTEGER NOT NULL,
    loan_date TEXT NOT NULL,
    due_date TEXT NOT NULL,
    return_date TEXT,
    fine_amount REAL DEFAULT 0.0,
    FOREIGN KEY (book_id) REFERENCES books(id),
    FOREIGN KEY (member_id) REFERENCES members(id)
);

-- fase 2

INSERT INTO categories (name)
VALUES ('Fiction'), ('Non-Fiction'), ('Science'), ('History'), ('Technology');

INSERT INTO authors (full_name, country) VALUES
('Isabel Allende', 'Chile'),
('Gabriel Garcia Marquez', 'Colombia'),
('Ursula K. Le Guin', 'United States'),
('Haruki Murakami', 'Japan'),
('Chinua Achebe', 'Nigeria'),
('Margaret Atwood', 'Canada'),
('Isaac Asimov', 'United States'),
('Alain Mabanckou', 'Congo');

INSERT INTO books (isbn, title, publication_year, category_id) VALUES
(9780553382563, 'The House of the Spirits', 1982, 1),
(9780060883287, 'One Hundred Years of Solitude', 1967, 1),
(9780547773746, 'The Left Hand of Darkness', 1969, 1),
(9780375718946, 'Kafka on the Shore', 2002, 1),
(9780385474542, 'Things Fall Apart', 1958, 1),
(9780385491027, 'Sapiens', 2011, 3),
(9780141989671, 'A Brief History of Time' ,1988 , 3),
(9780465026562, 'Guns Germs and Steel', 1997, 4),
(9780061120084, 'A Short History of Nearly Everything', 2003, 4),
(9780131103627, 'The Art of Computer Programming', 1968, 5),
(9780596007126, 'Head First Design Patterns', 2004, 5),
(9780451524935, 'The Handmaid s Tale', 1985, 1);

INSERT INTO book_authors (author_id, book_id) VALUES
(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 12), (7, 10), (7, 11), (2, 6), (3, 7), (4, 8), (1, 9), (8, 1), (8, 2), (8, 12);

INSERT INTO members (full_name, email, join_date) VALUES
('Carlos Mendoza', 'carlos.mendoza@email.com', '2025-03-15'),
('Ana Lopez', 'ana.lopez@email.com', '2025-06-01'),
('Roger Smith', 'roger.smith@email.com', '2025-09-20'),
('Maria Torre', 'maria.torres@email.com', '2026-01-10'),
('Luis Fernandez', 'luis.fernandez@email.com', '2025-11-05'),
('Sofia Rivera', 'sofia.rivera@email.com', '2026-02-14'),
('Pedro Ramirez', 'pedro.ramirez@email.com', '2024-12-01'),
('Elena Garcia', 'elena.garcia@email.com', '2026-04-22'),
('James Wright', 'james.wright@email.com', '2025-07-30'),
('Clara Jimenez', 'clara.jimenez@email.com', '2026-06-15');

PRAGMA foreign_keys = ON;
INSERT INTO loans (book_id, member_id, loan_date, due_date, return_date, fine_amount) VALUES
(1, 3, '2026-07-01', '2026-07-30', '2026-07-28', 0.0),
(2, 5, '2026-07-05', '2026-08-04', NULL, 0.0),
(3, 1, '2026-07-10', '2026-08-09', '2026-08-07', 0.0),
(4, 7, '2026-07-15', '2026-08-14', NULL, 0.0),
(5, 2, '2026-07-20', '2026-08-19', '2026-08-18', 0.0),
(6, 4, '2026-06-01', '2026-07-01', '2026-06-28', 0.0),
(7, 6, '2026-06-10', '2026-07-10', NULL, 0.0),
(8, 8, '2026-06-20', '2026-07-20', '2026-07-15', 0.0),
(9, 9, '2026-05-01', '2026-05-31', NULL, 2.50),
(10, 10, '2026-05-10', '2026-06-09', NULL, 3.00),
(11, 1, '2026-05-20', '2026-06-19', NULL, 1.75),
(12, 3, '2026-04-15', '2026-05-15', '2026-05-10', 0.0),
(1, 7, '2026-04-20', '2026-05-20', '2026-05-18', 0.0),
(4, 10, '2026-03-01', '2026-03-31', NULL, 5.00),
(6, 5, '2026-07-25', '2026-08-24', NULL, 0.0);

SELECT
    UPPER(TRIM(full_name)) AS member_name,
    LOWER(email),
    CASE
        WHEN CAST(JULIANDAY('now') - JULIANDAY(join_date) AS INTEGER) > 365.0 THEN 'Senior Member'
        ELSE 'Standard Member'
    END AS MemberTitle
FROM members
ORDER BY join_date;

-- fase 3
-- report 1

SELECT
    b.title AS book_title,
    a.full_name AS author_name,
    m.full_name AS member_name,
    l.loan_date,
    CAST(JULIANDAY('now') - JULIANDAY(l.loan_date) AS INTEGER) AS loan_total_days
FROM loans AS l
INNER JOIN books AS b ON l.book_id = b.id
INNER JOIN book_authors AS ba ON l.book_id = ba.book_id
INNER JOIN authors AS a ON ba.author_id = a.id
INNER JOIN members AS m ON l.member_id = m.id
WHERE l.return_date IS NULL;

--report 2

SELECT
    c.name AS category_name,
    COUNT(*) AS loans_categories_count,
    ROUND(AVG(CAST(JULIANDAY('now') - JULIANDAY(l.loan_date) AS INTEGER)), 2) AS total_avg_loan_days
FROM loans AS l
INNER JOIN books AS b ON l.book_id = b.id
INNER JOIN categories AS c ON b.category_id = c.id
GROUP BY c.name
HAVING COUNT(*) > 2
ORDER BY loans_categories_count DESC;

-- fase 4

--report 3

WITH UniqueLoans AS (
    SELECT
        id,
        book_id,
        member_id,
        loan_date,
        ROW_NUMBER() OVER(
            PARTITION BY book_id, member_id, loan_date
            ORDER BY id DESC
        ) AS dedup_rank
    FROM loans
)
SELECT id, book_id, member_id, loan_date
FROM UniqueLoans
WHERE dedup_rank = 1;

--report 4

SELECT
    b.title,
    b.category_id,
    c.name,
    COUNT(l.id) AS total_loans,
    DENSE_RANK() OVER(PARTITION BY b.category_id ORDER BY COUNT(l.id) DESC) AS rank_category,
    COUNT(l.id) - LAG(COUNT(l.id), 1) OVER(PARTITION BY b.category_id ORDER BY COUNT(l.id) DESC) AS loans_different
FROM loans AS l
INNER JOIN books AS b ON l.book_id = b.id
INNER JOIN categories AS c ON b.category_id = c.id
GROUP BY b.id, b.title, b.category_id, c.name
ORDER BY c. name, total_loans DESC;

-- fase 5

CREATE VIEW IF NOT EXISTS v_active_fines AS
SELECT
    m.id AS member_id,
    m.full_name,
    SUM(COALESCE(l.fine_amount, 0.0)) AS total_amount
FROM loans AS l
INNER JOIN members AS m ON l.member_id = m.id
WHERE l.fine_amount > 0.0
GROUP BY m.id, m.full_name;

SELECT * FROM v_active_fines;

CREATE INDEX idx_member_status ON loans(member_id);

EXPLAIN QUERY PLAN
SELECT * FROM loans WHERE member_id = 5;

BEGIN TRANSACTION;

INSERT INTO loans (book_id, member_id, loan_date, due_date, return_date, fine_amount)
VALUES (2, 4, '2026-09-08', '2026-10-07', NULL, 0.0);

UPDATE members SET status = 'Active' WHERE id = 4;

COMMIT;

-- Validation Space * Not finale script

PRAGMA foreign_keys = ON;
INSERT INTO loans (book_id, member_id, loan_date, due_date, return_date)
VALUES (5, 10, '2026-08-01 09:00', '2026-08-30 09:00', '2026-08-30 09:00');

DROP TABLE IF EXISTS loans;


--

