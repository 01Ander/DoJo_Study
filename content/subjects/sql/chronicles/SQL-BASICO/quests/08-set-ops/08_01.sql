CREATE TABLE temp_online_leads (
    full_name TEXT,
    email TEXT
);

CREATE TABLE temp_event_leads (
    full_name TEXT,
    email TEXT
);

CREATE TABLE master_contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    clean_name TEXT NOT NULL,
    clean_email TEXT NOT NULL UNIQUE,
    source TEXT NOT NULL
);

INSERT INTO temp_online_leads VALUES ('  carlos ruiz ', 'CARLOS@test.com');
INSERT INTO temp_event_leads VALUES ('diana Gomez', 'diana@test.com');

SELECT full_name, email FROM temp_online_leads
UNION ALL
SELECT full_name, email FROM temp_event_leads;

INSERT INTO master_contacts (clean_name, clean_email, source)
SELECT
    UPPER(TRIM(full_name)),
    LOWER(TRIM(email)),
    'ONLINE'
FROM temp_online_leads;

INSERT INTO master_contacts (clean_name, clean_email, source)
SELECT
    UPPER(TRIM(full_name)),
    LOWER(TRIM(email)),
    'EVENT'
FROM temp_event_leads;