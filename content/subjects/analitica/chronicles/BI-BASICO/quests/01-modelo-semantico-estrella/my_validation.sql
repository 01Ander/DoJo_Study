-- Operator workspace for Quest BI-01 (Libreria El Faro)
-- Complete the orphan check query to verify zero missing store_id keys in fact_book_sales.
SELECT COUNT(*) AS orphan_sales_count
FROM fact_book_sales f
-- TODO: LEFT JOIN dim_store s ON ...
-- TODO: WHERE ... IS NULL;
