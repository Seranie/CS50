CREATE TABLE transactions (
    transaction_id INTEGER NOT NULL,
    symbol TEXT NOT NULL,
    shares INTEGER NOT NULL,
    sharePrice INTEGER NOT NULL,
    totalPrice INTEGER NOT NULL,
    transactionTime DATETIME NOT NULL,
    FOREIGN KEY(transaction_id) REFERENCES users(id)
);

