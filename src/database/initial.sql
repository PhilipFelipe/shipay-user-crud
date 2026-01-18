CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        "name" varchar NOT NULL,
        email varchar NOT NULL UNIQUE,
        "password" varchar NOT NULL,
        role_id INTEGER NOT NULL,
        created_at date NOT NULL,
        updated_at date NULL,
        FOREIGN KEY (role_id) REFERENCES roles(id)
);

CREATE TABLE IF NOT EXISTS roles (
    id INTEGER PRIMARY KEY,
    description varchar NOT NULL
);

INSERT INTO roles (id, description) VALUES (1, "default")
ON CONFLICT(id) DO NOTHING;