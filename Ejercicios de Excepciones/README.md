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
