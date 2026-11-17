-- Reference orphan check query for Quest BI-01 (Libreria El Faro)
SELECT COUNT(*) AS orphan_sales_count
FROM fact_book_sales f
LEFT JOIN dim_store s ON f.store_id = s.store_id
WHERE s.store_id IS NULL;
