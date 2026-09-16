CREATE TABLE sales_agents (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    region TEXT NOT NULL
);

CREATE TABLE agent_deals (
    id INTEGER PRIMARY KEY,
    agent_id INTEGER,
    deal_amount REAL NOT NULL,
    FOREIGN KEY (agent_id) REFERENCES sales_agents(id)
);

INSERT INTO sales_agents VALUES (1, 'Carlos', 'LATAM'), (2, 'Diana', 'LATAM'), (3, 'Eric', 'EMEA');
INSERT INTO agent_deals VALUES (10, 1, 5000.0), (11, 1, 3000.0), (12, 2, 9000.0), (13, 3, 4000.0);

WITH AgentTotals AS (
    SELECT
        agent_id,
        SUM(deal_amount) AS total_sales
    FROM agent_deals
    GROUP BY agent_id
),
AverageSales AS (
    SELECT AVG(total_sales) AS total_avg_sales
    FROM AgentTotals
)
SELECT
    a.name,
    at.total_sales,
    avs.total_avg_sales
FROM sales_agents AS a
CROSS JOIN AverageSales AS avs
INNER JOIN AgentTotals AS at ON a.id = at.agent_id
WHERE at.total_sales > avs.total_avg_sales;