CREATE TABLE stock (
    stock_id NUMERIC NOT NULL,
    symbol TEXT NOT NULL,
    shares NUMERIC NOT NULL,
    FOREIGN KEY(stock_id) REFERENCES users(id)
)