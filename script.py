import requests
import psycopg2
from bs4 import BeautifulSoup


try:
    conexion = psycopg2.connect(host ='localhost', database= 'books', user= 'postgres', password='5860464', port = 5432 )
    cursor = conexion.cursor()

    url = 'https://books.toscrape.com/'
    respuesta = requests.get(url)
    respuesta.encoding = "utf-8"
    soup = BeautifulSoup(respuesta.text, 'html.parser')
        
    libros = soup.find_all ('article', class_ ='product_pod' )
    categorias = soup.find("ul", class_="nav nav-list").find("ul").find_all("li")
    print(
        '1. Libros \n' +
        '2. costos\n' +
        '3. categorias'
    )
    like = int(input('que categoria quisiera ver\n?'))


    if like ==1:
        for libro in libros:
            titulo = libro.h3.a['title']
            print(f'{titulo}')
            
    elif like == 2:
        for libro in libros:
            titulo = libro.h3.a['title']
            costo = libro.find('p' ,class_ = "price_color").text
    elif like == 3:
        for categoria in categorias:
            nombre = categoria.find('a').text.strip()
            print(f'{nombre}')
    elif like == 4:
        for categoria in categorias:  
            nombre = categoria.find('a').text.strip()
            cursor.excecute('INSERT INTO categorias (nombre) VALUES ($s) ON CONFLICT (nombre) DO NOTHING', (nombre,))
        
        for libro in libros:
            titulo = libro.h3.a['tittle']
            precio = libro.find('p', class_ = 'price_color')
    conexion.close()
except psycopg2.OperationalError as e:
    print(f'error de conexion')

# for categoria in categorias:
#     for precio in precios:
#         for libro in libros:
            
            
#             trama = categoria.find("a").text.strip()
#             costo = precio.find('p', class_='price_color').text
#             titulo = libro.h3.a['title']
            
            
#             if like == 1:
#                 print(f'{titulo}')
#             elif like == 2: 
#                 print(f'Precio de {titulo}: {costo}')
#             elif like == 3:
#                 print(f'{trama}') 
#             # print(f'Nombre: {titulo} - costo: {costo}')
#             # print(f'')
