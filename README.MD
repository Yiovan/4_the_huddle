# Explicacion de algunos procedimientos de codigo


### que es sql ?
 es un lenguaje de base de datos relacionales

### que es una base de datos?
es un sistema organizado para almacenar, gestionar y proteger grandes volumnenes de informacion estructuradas


- Relacionales = almacenan datos en tablas con filas y columnas, ideales para datos estructurados como transacciones 
- No Relacionales = incluyen modelos de documentos, clave-valor, graficos o columnas anchas, en simples palabras son 



```
cursor =  un mensajero entre tu codigo  y python 
```



```python 
cursor.execute("SELECT * FROM libros")                    # una consulta
cursor.executemany("INSERT INTO libros VALUES (%s, %s)",  # muchas a la vez
    [("Dune", 25), ("1984", 15)])
```


```
cursor.fetchone()    # un solo registro  → (1, "Dune", 25)
cursor.fetchall()    # todos             → [(1, ...), (2, ...), ...]
cursor.fetchmany(3)  # los primeros N    → [(1, ...), (2, ...), (3, ...)]
cursor.rowcount       # cuántas filas afectó la última consulta
cursor.lastrowid      # id del último registro insertado
cursor.description    # nombres de las columnas
cursor.column_names   # igual pero más limpio → ("id", "titulo", "precio")
conexion.commit()    # confirma los cambios — sin esto no se guardan
conexion.rollback()  # deshace los cambios si algo salió mal
```

Y para cerrar 
```
cursor.close()
conexion.close() 
```



```python 
try: 
    cursor.execute("INSERT INTO libros (titulo, precio) VALUES (%s, %s)",
                   ("Dune", 25)) #ejecuta una query, en este caso un insert
    conexion.commit()
    print(f"✅ Insertado con id: {cursor.lastrowid}")

except Exception as e:
    conexion.rollback()   # algo falló, deshace todo
    print(f"❌ Error: {e}")

finally:
    cursor.close()
    conexion.close()
```

```python
cursor.execute("INSERT INTO libros (titulo, precio) VALUES (%s, %s)",
                   ("Dune", 25))                 
```

cursor execute tiene una s con % que se llama placeholder, un espacio reservado donde python mete el valor real antes de enviar la consulta a mysql