import requests
from bs4 import BeautifulSoup
import mysql.connector

# Conexión a MySQL
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="5860464",
    database="libros_prueba"
)

cursor = conexion.cursor()

url = "https://books.toscrape.com/"
respuesta = requests.get(url)

if respuesta.status_code == 200:
    soup = BeautifulSoup(respuesta.text, "html.parser")
    libros = soup.find_all("article", class_="product_pod")

    for libro in libros:
        titulo = libro.h3.a["title"]
        precio_texto = libro.find("p", class_="price_color").text
        
        # Quitar símbolo £ y convertir a float
        precio = float(precio_texto.replace("e", ""))

        sql = "INSERT INTO libros (titulo, precio) VALUES (%s, %s)"
        valores = (titulo, precio)

        cursor.execute(sql, valores)

    conexion.commit()
    print("Datos insertados correctamente")

cursor.close()
conexion.close()