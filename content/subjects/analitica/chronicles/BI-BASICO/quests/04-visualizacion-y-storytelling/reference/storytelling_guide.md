# Reference Storytelling Guide — Quest BI-04 (Librería El Faro)

## 3 Quantified Findings (Q1 2026 vs Q1 2025)
1. **Total Q1 2026 revenue reached $480,000 COP**, representing a **+77.78% YoY growth** compared to Q1 2025 ($270,000 COP).
2. **CENTRO store drives 58.33% ($280,000 COP) of 2026 revenue**, growing +33.33% YoY over Q1 2025 ($210,000 COP).
3. **Bogotá concentrates 85.42% ($410,000 COP) of 2026 sales** with an average ticket of **$136,667 COP**, whereas Medellín (`SUR`) accounts for 14.58% ($70,000 COP) with a single order.

## 1 Actionable Recommendation
- **Replicate CENTRO's multi-unit bundle strategy in SUR (Medellín) during Q2 2026**, targeting an increase from 1 unit/order to 2+ units/order to raise Medellín's revenue share above 20%.

## 5-Minute Defense Script Structure
- **0:00–1:00:** Business question (Q1 2026 growth & store contribution) and fact grain (`1 row per completed sale_id`).
- **1:00–2:00:** Star Schema (`1:N` single-direction filters from `dim_store` and `dim_date`) and SQL reconciliation parity.
- **2:00–4:00:** Walk through the 3 quantified findings live using `year` and `city` slicers.
- **4:00–5:00:** Present the Q2 recommendation and state dataset limits (small sample window 2025–2026).
