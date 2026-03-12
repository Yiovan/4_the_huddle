# 📚 CUARTO CHALLENGE

Este directorio contiene un notebook de Python que:

1. crea las tablas necesarias en un servidor **MySQL** local,
2. descarga con hilos los libros de [books.toscrape.com](https://books.toscrape.com),
3. inserta los datos en la base de datos (categorías, libros y autores ficticios),
4. ejecuta varias consultas SQL de ejemplo para practicar.

---

## 🧠 Conceptos básicos

### ¿Qué es una base de datos?

Una base de datos es un sistema organizado para almacenar, gestionar y proteger grandes volúmenes de información estructurada.  
- **Relacionales**: datos en tablas con filas y columnas; ideales para transacciones.  
- **No relacionales**: modelos de documentos, clave‑valor, grafos, etc.; se usan cuando la estructura es menos rígida.

En este proyecto usamos MySQL, una base de datos relacional. 

### ¿Qué es el scraping?

Scraping o “web scraping” es la técnica de extraer información de páginas web.  
1. Se envía una petición HTTP al servidor.  
2. El servidor devuelve HTML.  
3. El programa parsea ese HTML (por ejemplo con `BeautifulSoup`) y busca etiquetas específicas.  
4. Se extrae el texto o atributos deseados y, opcionalmente, se guarda en CSV, JSON, base de datos, etc.

---

## 🧩 Explicación del código

El notebook `script.ipynb` está dividido en pasos claros:

1. **Instalar dependencias**: `requests`, `beautifulsoup4`, `mysql‑connector‑python`.
2. **Conectar a MySQL**: se crea la base de datos `libros_scraper` y las tablas `categorias`, `autores`, `libros` y la intermedia `libros_autores`.
3. **Funciones de scraping**:
   - `obtener_categorias()` recorre el menú de la web y devuelve nombres y URLs.
   - `obtener_libros_de_pagina(soup)` extrae título, precio, calificación, disponibilidad, URL y asigna 1‑2 autores ficticios a cada libro.
   - `scrapear_categoria(categoria)` itera páginas de una categoría usando hilos (`ThreadPoolExecutor`).
4. **Inserción en la base de datos**: la función `obtener_o_crear_id` evita duplicados. Se insertan categorías, libros y se registra la relación N‑M con autores.
5. **Consultas de ejemplo**: varios bloques `cursor.execute(...)` que muestran, por ejemplo, cuántos libros tiene cada categoría, libros de 5 estrellas, precio promedio, libros por autor, etc.

También se documentan en el README los métodos del cursor:

```py
cursor = un mensajero entre tu código y la base de datos

cursor.execute("SELECT * FROM libros")
cursor.executemany("INSERT INTO libros VALUES (%s, %s)", [("Dune", 25), ("1984", 15)])

cursor.fetchone()    # un solo registro  → (1, "Dune", 25)
cursor.fetchall()    # todos             → [(1, ...), (2, ...), ...]
cursor.fetchmany(3)  # los primeros N    → [(1, ...), (2, ...), (3, ...)]
cursor.rowcount       # cuántas filas afectó la última consulta
cursor.lastrowid      # id del último registro insertado
cursor.description    # nombres de las columnas
cursor.column_names   # igual pero más limpio → ("id", "titulo", "precio")
conexion.commit()    # confirma los cambios — sin esto no se guardan
conexion.rollback()  # deshace los cambios si algo salió mal

cursor.close()
conexion.close()
```

…y un ejemplo de manejo de errores con `try/except/finally`.

---

## 📁 Estructura del directorio

- `script.ipynb` – notebook principal.
- `libros_db` – (no versionado) base de datos local.
- `scrapping.md` – notas personales sobre scraping.
- `.gitignore` – ignora la DB local, `scrapping.md` y otros ficheros temporales.

---

Puedes clonar este repositorio y ejecutar el notebook en VS Code o Jupyter; no olvides configurar tus credenciales de MySQL antes de ejecutar las celdas.
