import sqlite3

with sqlite3.connect('users.db') as conn:
    cursor = conn.cursor()

    query_create_table_users = """
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
    """
    query_create_table_roles = """
        CREATE TABLE IF NOT EXISTS roles (
            id INTEGER PRIMARY KEY,
            description varchar NOT NULL
        );
    """

    cursor.execute(query_create_table_roles)
    cursor.execute(query_create_table_users)
    cursor.execute("""
        INSERT INTO roles (id, description) VALUES (1, "default")
        ON CONFLICT(id) DO NOTHING;
    """)
    conn.commit()
    print('Tables created successfully.')
