import requests
from bs4 import BeautifulSoup

url = "https://books.toscrape.com"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

libros  = soup.find_all('article', class_='product_pod')

for libro in libros:
    titulo = libro.h3.a['title']
    precio = libro.find('p', class_='price_color').text
    print(f'Título: {titulo}, Precio: {precio}')