CREATE TRIGGER IF NOT EXISTS trg_clean_deps 
AFTER DELETE ON transactions 
BEGIN
    DELETE FROM metadata 
    WHERE id = OLD.metadata_id 
      AND NOT EXISTS (SELECT 1 FROM transactions WHERE metadata_id = OLD.metadata_id);

    DELETE FROM categories WHERE NOT EXISTS (SELECT 1 FROM metadata WHERE category_id = categories.id);
END;
