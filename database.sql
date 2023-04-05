CREATE TABLE IF NOT EXISTS urls (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    created_at DATE
);

CREATE TABLE IF NOT EXISTS url_checks (
    url_id BIGINT REFERENCES urls(id),
    id SERIAL PRIMARY KEY,
    status_code smallint,
    h1 VARCHAR(255),
    title VARCHAR(255),
    description VARCHAR(255),
    created_at DATE
);