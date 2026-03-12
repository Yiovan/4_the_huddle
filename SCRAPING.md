# 🕷️ Web Scraping — Cómo funciona en este proyecto

## ¿Qué es Web Scraping?

Web scraping es la técnica de **extraer datos de páginas web de forma automática**. En lugar de copiar información manualmente, un programa visita la página, lee su HTML y extrae lo que necesitas.

### Flujo general del scraping

```
Tu código Python  ──►  Petición HTTP (requests.get)  ──►  Servidor web
                                                              │
                  ◄── HTML de respuesta ──────────────────────┘
                       │
                       ▼
               BeautifulSoup analiza el HTML
                       │
                       ▼
              Extraes los datos que necesitas
                       │
                       ▼
           Guardas en base de datos, CSV, JSON, etc.
```

---

## Librerías utilizadas

| Librería | ¿Para qué sirve? |
|---|---|
| `requests` | Enviar peticiones HTTP y recibir el HTML de la página |
| `beautifulsoup4` | Analizar (parsear) el HTML y buscar etiquetas específicas |
| `concurrent.futures` | Ejecutar scraping en paralelo usando hilos (más rápido) |

---

## Paso a paso: qué hace el código

### 1. Enviar la petición HTTP

```python
url = "https://books.toscrape.com"
respuesta = requests.get(url)
```

- `requests.get(url)` envía una petición **GET** al servidor, como si abrieras la página en tu navegador.
- El servidor devuelve el HTML completo de la página.
- `respuesta.status_code` te dice si fue exitosa (`200 = OK`).

### 2. Analizar el HTML con BeautifulSoup

```python
soup = BeautifulSoup(respuesta.text, "html.parser")
```

- `respuesta.text` contiene el HTML crudo (texto plano).
- `BeautifulSoup` lo convierte en un **árbol de objetos** que puedes recorrer fácilmente.
- `"html.parser"` es el analizador que usa Python por defecto para interpretar el HTML.

### 3. Buscar los elementos que necesitas

```python
libros = soup.find_all("article", class_="product_pod")
```

- `find_all()` busca **todas** las etiquetas `<article>` que tengan la clase CSS `product_pod`.
- Cada `<article class="product_pod">` en la página representa **un libro**.
- El resultado es una lista de elementos HTML, uno por cada libro.

### 4. Extraer los datos de cada libro

```python
for libro in libros:
    titulo       = libro.h3.a["title"]
    precio_texto = libro.find("p", class_="price_color").text
    precio       = float(precio_texto.replace("£", "").replace("Â", "").strip())
    calificacion = libro.select_one("p.star-rating")["class"][1]
    disponible   = libro.select_one("p.availability").text.strip()
    url_libro    = libro.select_one("h3 > a")["href"]
```

| Dato | Cómo lo extrae | Qué hace |
|---|---|---|
| **Título** | `libro.h3.a["title"]` | Navega al `<h3>`, luego al `<a>` y lee el atributo `title` |
| **Precio** | `libro.find("p", class_="price_color").text` | Busca el `<p>` con clase `price_color` y lee su texto |
| **Calificación** | `libro.select_one("p.star-rating")["class"][1]` | Lee la segunda clase CSS (`One`, `Two`, ... `Five`) |
| **Disponibilidad** | `libro.select_one("p.availability").text.strip()` | Lee el texto del `<p>` de disponibilidad |
| **URL** | `libro.select_one("h3 > a")["href"]` | Lee el atributo `href` del enlace |

### 5. Obtener todas las categorías

```python
for enlace in soup.select("ul.nav-list > li > ul > li > a"):
    categorias.append({
        "nombre": enlace.text.strip(),
        "url":    URL_BASE + "/" + enlace["href"]
    })
```

- Usa un **selector CSS** (`select()`) para encontrar los enlaces dentro del menú lateral de categorías.
- Para cada categoría guarda su nombre y URL completa.

### 6. Navegar múltiples páginas (paginación)

```python
while True:
    respuesta = requests.get(url_actual, timeout=10)
    soup      = BeautifulSoup(respuesta.text, "html.parser")
    libros_totales.extend(obtener_libros_de_pagina(soup))

    siguiente = soup.select_one("li.next > a")
    if siguiente:
        url_actual = base + "/" + siguiente["href"]
        time.sleep(0.2)  # pausa para no saturar el servidor
    else:
        break
```

- Muchas categorías tienen varias páginas de libros.
- El código busca el botón **"next"** (`li.next > a`).
- Si existe, construye la URL de la siguiente página y sigue scrapeando.
- Si no existe, significa que ya recorrió todas las páginas → sale del bucle.
- `time.sleep(0.2)` añade una pausa de cortesía para no sobrecargar el servidor.

### 7. Scraping en paralelo con hilos (threading)

```python
MAX_HILOS = 5

with ThreadPoolExecutor(max_workers=MAX_HILOS) as ejecutor:
    futuros = {
        ejecutor.submit(scrapear_categoria, cat): cat["nombre"]
        for cat in obtener_categorias()
    }
    for futuro in as_completed(futuros):
        resultado = futuro.result()
```

- Sin hilos: scrapea categoría por categoría → **muy lento**.
- Con hilos: scrapea **5 categorías a la vez** en paralelo → **mucho más rápido** (~20 segundos las 50 categorías).
- `ThreadPoolExecutor` crea un "pool" de hilos que ejecutan la función `scrapear_categoria` simultáneamente.
- `as_completed()` te devuelve los resultados a medida que cada hilo termina.

---

## Resultado final

El scraping de **books.toscrape.com** extrae:

| Dato | Ejemplo |
|---|---|
| 📂 Categorías | Travel, Fiction, Mystery, etc. (50 categorías) |
| 📖 Libros | 1000 libros con título, precio, calificación, disponibilidad y URL |
| ✍️ Autores | Ficticios (la web no tiene autores reales), asignados aleatoriamente para practicar SQL |

---

## Métodos clave de BeautifulSoup

| Método | ¿Qué hace? | Ejemplo |
|---|---|---|
| `find()` | Busca **el primer** elemento que coincida | `soup.find("p", class_="price_color")` |
| `find_all()` | Busca **todos** los elementos que coincidan | `soup.find_all("article", class_="product_pod")` |
| `select()` | Busca usando **selectores CSS** (como en CSS) | `soup.select("ul.nav-list > li > a")` |
| `select_one()` | Como `select()` pero devuelve solo **el primero** | `soup.select_one("li.next > a")` |
| `.text` | Obtiene el **texto** dentro de una etiqueta | `elemento.text` → `"£25.99"` |
| `["atributo"]` | Obtiene un **atributo** HTML | `enlace["href"]` → `"/catalogue/..."` |
| `.strip()` | Elimina espacios en blanco al inicio y al final | `"  In stock  ".strip()` → `"In stock"` |

---

## Buenas prácticas aplicadas

- ✅ **`time.sleep()`** entre peticiones para no saturar el servidor
- ✅ **`timeout=10`** para que las peticiones no se queden colgadas infinitamente
- ✅ **`try/except`** para manejar errores sin que el programa se detenga
- ✅ **Hilos** para acelerar el proceso sin complicar el código
- ✅ **Placeholders `%s`** para insertar datos de forma segura en la base de datos (previene inyección SQL)
