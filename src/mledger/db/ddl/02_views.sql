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
  p_latest.paid_at AS last_payment,
  t.created_at
FROM transactions t 
INNER JOIN metadata m ON t.metadata_id = m.id 
INNER JOIN categories c ON m.category_id = c.id
LEFT JOIN (
    SELECT transaction_id, MAX(paid_at) AS paid_at
    FROM payments
    GROUP BY transaction_id
) p_latest ON p_latest.transaction_id = t.id;
