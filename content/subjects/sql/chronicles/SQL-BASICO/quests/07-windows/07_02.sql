CREATE TABLE staging_web_clicks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    page_url TEXT NOT NULL,
    click_timestamp TEXT NOT NULL
);

-- Inserción de eventos duplicados por reconexión de red
INSERT INTO staging_web_clicks (user_id, page_url, click_timestamp) VALUES
(42, '/checkout', '2026-07-31 10:00:00'),
(42, '/checkout', '2026-07-31 10:00:01'), -- Duplicado mas reciente
(88, '/home',     '2026-07-31 10:05:00'),
(42, '/checkout', '2026-07-31 09:59:59'), -- Registro mas antiguo
(88, '/home',     '2026-07-31 10:05:05'); -- Duplicado mas reciente

WITH RankedClicks AS (
    SELECT
        id,
        user_id,
        page_url,
        click_timestamp,
        ROW_NUMBER() OVER(
            PARTITION BY user_id,  page_url
            ORDER BY click_timestamp DESC
        ) AS dedup_rank
    FROM staging_web_clicks
)
SELECT id, user_id, page_url, click_timestamp
FROM RankedClicks
WHERE dedup_rank = 1;