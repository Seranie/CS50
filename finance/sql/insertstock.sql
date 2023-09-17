IF EXISTS (SELECT * FROM stock WHERE stock_id = ? AND symbol = ?)
BEGIN
    UPDATE stock SET shares = ? WHERE stock_id = ? AND symbol = ?
END
ELSE
BEGIN
    INSERT INTO stock (stock_id, symbol, shares) VALUES (?, ?, ?)
END
GO









SELECT *
    CASE
    WHEN
    EXISTS(
        SELECT * FROM stock WHERE stock_id = ? AND symbol = ?
    )
    THEN
        UPDATE stock (shares) VALUES (?) WHERE stock_id = ?, symbol = ?
    ELSE
        INSERT INTO stock (stock_id, symbol, shares) VALUES (?, ?, ?)
    END
FROM stock