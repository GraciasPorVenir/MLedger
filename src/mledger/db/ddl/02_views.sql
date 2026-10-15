CREATE VIEW IF NOT EXISTS vw_transactions AS 
SELECT 
  t.id,
  t.metadata_id,
  m.category_id,
  t.is_income,
  t.cents,
  t.currency,
  t.installments,
  m.frequency,
  m.reason,
  c.name AS category,
  t.created_at
FROM transactions t 
INNER JOIN metadata m ON t.metadata_id = m.id 
INNER JOIN categories c ON m.category_id = c.id;
