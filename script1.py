import requests
from bs4 import BeautifulSoup

url = "https://quotes.toscrape.com"
response = requests.get(url)


print(f'response.status_code: {response.status_code}')
soup = BeautifulSoup(response.text, 'html.parser') 

titulos = soup.find_all('h1')
for titulo in titulos:
    print(titulo.text)