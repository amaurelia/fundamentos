# Ejercicios

Esta carpeta contiene los ejercicios propuestos para practicar descuentos y promociones.

---

## Ejercicio 1 — Ropa (`ropa.py`)

![Moda](img/moda.jpg)

Usted debe crear un programa de tienda de ropa. Los productos disponibles y sus precios son:

| Producto   | Precio    |
|------------|-----------|
| Falda      | $10.000   |
| Blusa      | $5.500    |
| Pantalón   | $5.000    |
| Chaqueta   | $14.000   |

El programa debe permitir comprar varias unidades de cada prenda. Al finalizar la compra, se debe solicitar un **código de descuento**. Los códigos válidos son:

| Código           | Descuento |
|------------------|-----------|
| PRIMAVERAVERANO  | 15%       |
| FUNDAMENTOS      | 20%       |
| ALAMODA          | 25%       |

Si el código ingresado no es válido, no se aplica descuento. Al final se debe mostrar el **valor total con el descuento aplicado**.

---

## Ejercicio 2 — Cine (`cine.py`)

![Cine](img/cine.jpg)

Usted debe crear un programa de compra de entradas de cine. Los tipos de entrada disponibles son:

| Tipo de entrada | Precio  |
|-----------------|---------|
| Estreno         | $6.000  |
| Normal          | $4.500  |

El programa debe permitir comprar varias entradas de un tipo específico ( Estreno | Normal ). El descuento se aplica automáticamente según la cantidad **total** de entradas compradas:

| Cantidad de entradas | Descuento |
|----------------------|-----------|
| 1 entrada            | Sin descuento |
| 2 a 3 entradas       | 10%       |
| 4 o más entradas     | 20%       |

Al final se debe mostrar el **valor total con el descuento aplicado**.

---

## Ejercicio 3 — Cursos (`cursos.py`)

![Cursos](img/cursos.jpg)

Usted debe crear un programa de compra de cursos académicos. Los cursos disponibles y sus precios son:

| Curso          | Precio     |
|----------------|------------|
| Liderazgo      | $200.000   |
| Programación   | $230.000   |
| Cyberseguridad | $270.000   |

El alumno debe seleccionar un curso e ingresar su nota. Según la nota obtenida, se aplica automáticamente un descuento en el precio del curso:

| Nota            | Descuento     |
|-----------------|---------------|
| Menor a 5.0     | Sin descuento |
| Entre 5.0 y 5.9 | 10%           |
| Entre 6.0 y 6.5 | 15%           |
| 6.6 en adelante | 20%           |

Al final se debe mostrar el **valor total a pagar con el descuento aplicado**.

---

## Ejercicio 4 — Impuestos (`impuestos.py`)

![Impuestos](img/impuestos.jpg)

Todos los años usted debe pagar impuestos por su propiedad. El programa debe solicitar:

- Valor de la propiedad (en UF)
- Metros cuadrados
- ¿Tiene piscina?
- ¿Tiene árboles frutales?

El porcentaje a pagar se calcula sumando los siguientes tramos:

| Condición | Porcentaje adicional |
|---|---|
| Propiedad vale **menos de 4.000 UF** | 2% |
| Propiedad vale **más de 4.000 UF** | 3% |
| Superficie **mayor a 100 m²** | +1% |
| Tiene **piscina** | +0.5% |
| Tiene **árboles frutales** | +0.5% |

Al final se debe mostrar el **porcentaje total** a pagar y el **costo anual** de los impuestos.

---

## Ejercicio 5 — Anticuchos (`anticuchos.py`)

![Anticuchos](img/anticuchos.jpg)

¡Ha llegado el 18 y es momento de celebrar! El combo incluye 2 anticuchos y un terremoto, con un precio base de **$15.000**. Sin embargo, hay descuento según el rol del comprador:

| Rol | Descuento |
|---|---|
| Estudiante de informática | 5% |
| Profesor | 95% |
| Otro | Sin descuento |

Ingresa si eres **estudiante / profesor / otro** y calcula el precio a pagar.

---

## Ejercicio 6 — Centro Pokémon (`centro_pokemon.py`)

![Centro Pokémon](img/centro_pokemon.jpg)

Debido a problemas presupuestarios, los centros Pokémon ahora cobran **800 yenes** por cada atención. Sin embargo, hay descuento según el nivel del Pokémon:

| Nivel del Pokémon | Descuento |
|---|---|
| Nivel 1 a 4 | Sin descuento |
| Nivel 5 a 15 | 5% |
| Nivel 16 a 30 | 7% |
| Nivel 31 a 50 | 10% |
| Sobre nivel 50 | 15% |

Ingresa el nivel del Pokémon y calcula el costo de la atención.

---

## Ejercicio 7 — Fotografías (`fotografias.py`)

![Fotografías](img/fotografias.jpg)

Peter Parker es un fotógrafo malpagado. Su jefe le paga solo **$5.000 por cada foto de Spider-Man**, pero accede a aumentarle el pago si trae suficientes fotos esta semana:

| Fotos entregadas | Aumento |
|---|---|
| Menos de 5 fotos | Sin aumento |
| 5 a 10 fotos | +1% por foto |
| Más de 10 fotos | +2% por foto |

Ingresa el número de fotos tomadas esta semana y calcula el total que le deben pagar.


