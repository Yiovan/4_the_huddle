CREATE TABLE libros (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    titulo VARCHAR(500),
    precio NUMERIC(10, 2),   -- guarda 51.77
    categoria VARCHAR(100)
);


-- primero la categoría
CREATE TABLE categorias (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR(100) UNIQUE
);

-- luego el libro referencia a categoría
CREATE TABLE libros (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    titulo VARCHAR(500),
    precio NUMERIC(10, 2),
    categoria_id INT REFERENCES categorias(id)  -- ← llave foránea
);


-- ## Cómo queda la data
-- ```
-- categorias          libros
-- ──────────          ──────────────────────────────
-- id │ nombre         id │ titulo    │ precio │ categoria_id
-- ───┼────────        ───┼───────────┼────────┼─────────────
-- 1  │ Mystery        1  │ Book A    │ 51.77  │ 1
-- 2  │ Poetry         2  │ Book B    │ 23.99  │ 1
--                     3  │ Book C    │ 15.00  │ 2