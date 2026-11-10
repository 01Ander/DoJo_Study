-- Script de inicialización automática para el contenedor PostgreSQL (DoJo Study / FinCorp Global)
CREATE TABLE IF NOT EXISTS gold_transactions (
    transaction_id VARCHAR(64) NOT NULL,
    amount NUMERIC(12, 2) NOT NULL,
    status VARCHAR(32) NOT NULL,
    loaded_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

