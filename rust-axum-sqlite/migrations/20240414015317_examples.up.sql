CREATE TABLE examples (
    id SERIAL PRIMARY KEY,
    example TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX unique_examples ON examples (example);