import sqlite3
from pathlib import Path


def column_exists(conn: sqlite3.Connection, table: str, column: str) -> bool:
    cur = conn.execute(f"PRAGMA table_info('{table}')")
    cols = [row[1] for row in cur.fetchall()]
    return column in cols


def migrate(db_path: Path = Path("cbt-test.db")):
    if not db_path.exists():
        print(f"Base de datos no encontrada: {db_path}")
        return

    conn = sqlite3.connect(str(db_path))
    try:
        conn.execute("PRAGMA foreign_keys=ON")
        if not column_exists(conn, "prepago", "estado"):
            print("Agregando columna 'estado' a tabla 'prepago'...")
            conn.execute("ALTER TABLE prepago ADD COLUMN estado TEXT DEFAULT 'pendiente'")
            conn.commit()
            print("Columna agregada.")
        else:
            print("Columna 'estado' ya existe en 'prepago'.")
    finally:
        conn.close()


if __name__ == "__main__":
    migrate()
    print("Migración de 'prepago.estado' finalizada.")
