import sqlite3
import os

def initialize_database():
    db_path = "miniatures.db"
    schema_path = "schema.sql"  # Ruta al archivo schema.sql

    # Verificar si la base de datos ya existe
    if not os.path.exists(db_path):
        try:
            # Crear la conexión a la base de datos
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Leer el contenido del archivo schema.sql
            if os.path.exists(schema_path):
                with open(schema_path, "r", encoding="utf-8") as schema_file:
                    schema_sql = schema_file.read()

                # Ejecutar las sentencias SQL del esquema
                cursor.executescript(schema_sql)
                print("Database initialized with the provided schema.")
            else:
                print(f"The file {schema_path} not found. The database could not be initialized.")

            # Confirmar los cambios
            conn.commit()
        except Exception as e:
            print(f"Error initializing database: {e}")
        finally:
            # Cerrar la conexión
            conn.close()
    else:
        print("The database already exists. No action was taken.")

if __name__ == "__main__":
    initialize_database()