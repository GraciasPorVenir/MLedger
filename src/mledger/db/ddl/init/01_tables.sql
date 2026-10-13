CREATE TABLE IF NOT EXISTS categories(
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS metadata(
  id INTEGER PRIMARY KEY,
  category_id INTEGER NOT NULL REFERENCES categories(id),
  frequency INTEGER DEFAULT 0 CHECK ( frequency BETWEEN 0 AND 5 ),
  reason TEXT
);

CREATE TABLE IF NOT EXISTS transactions(
  id INTEGER PRIMARY KEY,
  metadata_id INTEGER NOT NULL REFERENCES metadata(id),
  cents INTEGER NOT NULL CHECK ( cents > 0 ),
  currency TEXT NOT NULL CHECK( length(currency) = 3 ),
  type INTEGER DEFAULT 0 CHECK ( type IN (0, 1) ),
  created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS payments(
  transaction_id INTEGER NOT NULL REFERENCES transactions(id) ON DELETE CASCADE,
  cents INTEGER NOT NULL CHECK( cents > 0),
  paid_at TEXT DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY(transaction_id, cents, paid_at)
);

CREATE INDEX IF NOT EXISTS idx_transactions_metadata ON transactions(metadata_id);
CREATE INDEX IF NOT EXISTS idx_payments_transaction ON payments(transaction_id);
CREATE INDEX IF NOT EXISTS idx_metadata_category ON metadata(category_id);
