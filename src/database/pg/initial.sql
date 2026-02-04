CREATE TABLE IF NOT EXISTS roles (
    id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    description varchar NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    "name" varchar NOT NULL,
    email varchar NOT NULL UNIQUE,
    "password" varchar NOT NULL,
    role_id INTEGER NOT NULL,
    created_at date NOT NULL,
    updated_at date NULL,
    FOREIGN KEY (role_id) REFERENCES roles(id)
);

INSERT INTO roles (description) VALUES ('default') ON CONFLICT(id) DO NOTHING;