import sqlite3
import hashlib

DB_NAME = "usuarios.db"


usuarios = {
    "Javier Bahamondes": "clave123",
    "Amancay Sanhueza": "clave456",
    "Jose Daniel Hidalgo": "clave7890"
    
}

def hash_password(password):
    """Convierte una contraseña en su hash SHA-256 (hexadecimal)."""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def crear_base_datos():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
        )
    """)

    for nombre, password in usuarios.items():
        hash_pw = hash_password(password)
        try:
            cursor.execute(
                "INSERT INTO usuarios (nombre, password_hash) VALUES (?, ?)",
                (nombre, hash_pw)
            )
            print(f"Usuario '{nombre}' creado con hash: {hash_pw}")
        except sqlite3.IntegrityError:
            print(f"Usuario '{nombre}' ya existe, se omite.")

    conn.commit()
    conn.close()
    print(f"\nBase de datos '{DB_NAME}' lista.")

if __name__ == "__main__":
    crear_base_datos()