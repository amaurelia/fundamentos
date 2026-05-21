# Ejercicios

Esta carpeta contiene los ejercicios propuestos para practicar el manejo de excepciones con `try`, `except`, `else` y `finally`.

---

## Ejercicio 1 — Mayor de edad (`mayor_de_edad.py`)

![Mayor de edad](img/mayor_de_edad.jpg)

El programa debe verificar si el usuario es mayor de edad según la edad que ingrese. Sin embargo, el usuario podría escribir texto en lugar de un número, lo que provocaría un error en tiempo de ejecución. Tu tarea es manejar ese error correctamente usando `try/except`.

El programa debe pedir:

| Dato | Tipo   | Descripción          |
|------|--------|----------------------|
| Edad | Entero | La edad del usuario  |

Las reglas son las siguientes:

| Condición           | Resultado                        |
|---------------------|----------------------------------|
| Edad 18 o más       | Eres mayor de edad               |
| Edad menor a 18     | Eres menor de edad               |
| Se ingresa un texto | Se debe mostrar un mensaje de error sin que el programa se caiga |

> **Pista:** usa `int()` dentro de un bloque `try` para convertir el dato ingresado. Si falla, captura la excepción `ValueError`.

---

## Ejercicio 2 — Clase de pociones (`pociones.py`)

![Clase de pociones](img/pociones.jpg)

Eres aprendiz en Hogwarts y el Profesor Snape te ha pedido que prepares los ingredientes para la clase de Pociones. Debes crear un programa en Python que solicite los siguientes datos mágicos:

| Dato | Tipo | Restricción |
|------|------|-------------|
| Cantidad de garras de dragón | Entero | Debe ser **más de 5** |
| Número de plumas de fénix | Entero | **Máximo 3** |
| Código mágico del grimorio | Texto | Debe terminar en un dígito del `0` al `9` o la letra `X` (ej: `Gretox`, `Grim48439`) |

El programa debe validar cada dato ingresado y manejar excepciones, ya que los magos pueden equivocarse al escribir. Si algún dato no cumple las reglas, el programa debe mostrar un mensaje de error y volver a pedirlo hasta que sea correcto.

> **Pista:** usa un ciclo `while True` con `try/except` para cada dato. Para el código del grimorio, revisa el último carácter del string con `.upper()` y verifica si es un dígito con `.isdigit()` o si es `'X'`.

---

## Ejercicio 3 — Jurassic Park (`jurassicpark.py`)

![Jurassic Park](img/jurrasicpark.jpg)

Eres guardia en Jurassic Park y tu misión es llevar el control de los dinosaurios y sus recintos. Debes crear un programa en Python que solicite los siguientes datos:

| Dato | Tipo | Restricción |
|------|------|-------------|
| Número de Velociraptors | Entero | Entre **5 y 20** |
| Número de T-Rex | Entero | **Máximo 2** |
| Número de Triceratops | Entero | **Mínimo 3** |
| Nombre del recinto | Texto | Debe incluir la palabra `"Sector"` |
| Tipo de alimento | Texto | Debe incluir la palabra `"carne"` o `"plantas"` |

El programa debe validar cada dato ingresado y manejar excepciones, ya que los cuidadores pueden equivocarse al escribir. Si algún dato no cumple las reglas, el programa debe mostrar un mensaje de error y volver a pedirlo hasta que sea correcto.

> **Pista:** para los textos usa `.lower()` al comparar (así `"Carne"` y `"carne"` son equivalentes) y verifica con el operador `in`.

---

## Ejercicio 4 — Ponle nombre a tu archivo (`python.py`)

![Nombre de archivo](img/python.jpg)

Acabas de escribir un código de Python y ahora debes guardar el archivo. El nombre debe cumplir con las siguientes características:

| Regla | Descripción |
|-------|-------------|
| Extensión | Debe terminar en `.py` |
| Caracteres | Solo letras (sin `ñ` ni tildes) y números, sin espacios |
| Longitud | Menos de **20 caracteres** en total |

El programa debe validar cada dato ingresado y manejar excepciones, ya que los desarrolladores pueden equivocarse al escribir. Si algún dato no cumple las reglas, el programa debe mostrar un mensaje de error y volver a pedirlo hasta que sea correcto.

> **Pista:** usa `.endswith(".py")` para verificar la extensión. Para los caracteres válidos puedes usar el módulo `re` con el patrón `r'^[a-zA-Z0-9]+\.py$'` o recorrer el string verificando cada carácter.

---

## Ejercicio 5 — Ficha de paciente (`hospital.py`)

![Hospital](img/hospital.jpg)

Eres programador en un hospital y tu tarea es registrar la ficha de un paciente. El programa debe solicitar los siguientes datos:

| Dato | Tipo | Restricción |
|------|------|-------------|
| Nombre | Texto | Debe tener **menos de 10 letras** |
| Edad | Entero | Debe ser **menor a 120** años |
| Peso | Decimal | Debe ser un número válido (mayor a 0) |
| RUT | Texto | Debe terminar en un dígito del `0` al `9` o la letra `K` |

El programa debe validar cada dato ingresado y manejar excepciones, ya que los pacientes pueden cometer errores al escribir. Si algún dato no cumple las reglas, el programa debe mostrar un mensaje de error y volver a pedir el dato hasta que sea correcto.

> **Pista:** para el peso usa `float()` dentro de un `try`. Para el RUT verifica el último carácter con `.upper()` y comprueba si es dígito con `.isdigit()` o si es `'K'`.

---

## Ejercicio 6 — Pizzería (`pizzeria.py`)

![Pizzería](img/pizzeria.jpg)

Eres cajero en una pizzería y debes tomar el pedido de un cliente. El programa debe solicitar los siguientes datos:

| Dato | Tipo | Restricción |
|------|------|-------------|
| Tamaño de la pizza | Texto | Debe ser `"pequeña"`, `"mediana"` o `"grande"` |
| Cantidad de pizzas | Entero | Entre **1 y 10** |
| Número de teléfono | Texto | Exactamente **9 dígitos numéricos** |
| Hora de entrega | Entero | Entre **10 y 22** |

El programa debe validar cada dato ingresado y manejar excepciones, ya que los clientes pueden equivocarse al escribir. Si algún dato no cumple las reglas, el programa debe mostrar un mensaje de error y volver a pedirlo hasta que sea correcto.

> **Pista:** para verificar que el teléfono tiene solo dígitos usa `.isdigit()` y `len()`. Para el tamaño compara con una lista de opciones válidas usando el operador `in`.

---

## Ejercicio 7 — Registro de jugador de fútbol (`futbol.py`)

![Fútbol](img/futbol.jpg)

Eres el secretario técnico de un equipo de fútbol y debes registrar la ficha de un jugador. El programa debe solicitar los siguientes datos:

| Dato | Tipo | Restricción |
|------|------|-------------|
| Nombre | Texto | Solo letras, **máximo 20 caracteres** |
| Número de camiseta | Entero | Entre **1 y 99** |
| Posición | Texto | Debe ser `"portero"`, `"defensa"`, `"centrocampista"` o `"delantero"` |
| Goles anotados | Entero | **0 o más** |

El programa debe validar cada dato ingresado y manejar excepciones, ya que los encargados pueden equivocarse al escribir. Si algún dato no cumple las reglas, el programa debe mostrar un mensaje de error y volver a pedirlo hasta que sea correcto.

> **Pista:** para el nombre usa `.replace(" ", "").isalpha()` para verificar que solo contiene letras. Para la posición compara con una lista de opciones válidas usando `in` y `.lower()`.
