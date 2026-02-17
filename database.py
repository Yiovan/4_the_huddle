import psycopg2

try:
    conexion = psycopg2.connect(
    host="localhost",
    database="books",
    user="postgres",        # usuario por defecto
    password="5860464",
    port="5432"
)
    print("✅ conexión exitosa!")
    conexion.close()

except psycopg2.OperationalError as e:
    print(f"❌ error de conexión: {e}")