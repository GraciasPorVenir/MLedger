INSERT OR IGNORE INTO categories (id, name) VALUES 
(1, 'Salario'),
(2, 'Comida'),
(3, 'Transporte'),
(4, 'Servicios'),
(5, 'Entretenimiento');

INSERT OR IGNORE INTO metadata (id, category_id, frequency, reason) VALUES 
(1, 1, 1, 'Sueldo mensual fijo'),
(2, 2, 2, 'Supermercado semanal'),
(3, 3, 3, 'Viajes en transporte público'),
(4, 4, 1, 'Servicios de luz e internet'),
(5, 5, 0, 'Cine y salidas de fin de semana');

INSERT OR IGNORE INTO transactions (id, metadata_id, cents, currency, is_income, installments, created_at) VALUES 
(1, 1, 350000, 'USD', 1, 1, '2026-10-01 09:00:00'),
(2, 2, 8500, 'USD', 0, 1, '2026-10-02 14:30:00'),
(3, 3, 450, 'USD', 0, 1, '2026-10-03 08:15:00'),
(4, 4, 12000, 'USD', 0, 1, '2026-10-05 10:00:00'),
(5, 5, 3500, 'USD', 0, 1, '2026-10-06 20:00:00');

INSERT OR IGNORE INTO payments (transaction_id, cents, paid_at) VALUES 
(1, 350000, '2026-10-01 09:05:00'),
(2, 8500, '2026-10-02 14:35:00'),
(3, 450, '2026-10-03 08:20:00'),
(4, 12000, '2026-10-05 10:05:00'),
(5, 3500, '2026-10-06 20:05:00');
