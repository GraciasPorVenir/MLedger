CREATE TABLE IF NOT EXISTS currencies(
  iso TEXT PRIMARY KEY CHECK ( length(iso) = 3 )
);

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
  currency TEXT NOT NULL REFERENCES currencies(iso),
  type INTEGER DEFAULT 0 CHECK ( type IN (0, 1) ),
  created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS payments(
  id INTEGER PRIMARY KEY,
  transaction_id INTEGER NOT NULL REFERENCES transactions(id) ON DELETE CASCADE,
  cents INTEGER NOT NULL CHECK( cents > 0),
  paid_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_transactions_metadata ON transactions(metadata_id);
CREATE INDEX idx_payments_transaction ON payments(transaction_id);
