CREATE TABLE Users (
    username VARCHAR(50) PRIMARY KEY,
    password VARCHAR(50),
    session_id INTEGER,
    token VARCHAR(50)
);