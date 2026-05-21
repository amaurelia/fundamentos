# Ejercicios

Esta carpeta contiene los ejercicios propuestos para practicar los contenidos del ramo.

---

## Ejercicio 1 — Avistamientos (`avistamientos.py`)

![Avistamientos](img/avistamientos.jpg)

Nina, Luke, Iris y Gary aseguran haber visto objetos en el cielo. Debes crear un programa que tenga un menú con las siguientes opciones:

1. **Registrar** — Registrar el testimonio del evento de uno de los 4 testigos.
2. **Ver** — Mostrar los testimonios de todos los testigos que hayan registrado algo.
3. **Buscar** — Buscar si hay alguna descripción que hable sobre **"luces"** en el cielo.
4. **Salir** — Salir del programa.

> **Pista:** usa un diccionario con los 4 nombres como claves y los testimonios como valores. Para buscar, recorre los valores con un `for` y usa el operador `in` para verificar si `"luces"` aparece en el texto.

---

## Ejercicio 2 — Banco (`banco.py`)

![Banco](img/banco.jpg)

Usted debe crear un programa de menú bancario que tenga las siguientes opciones para una cuenta nueva con saldo cero:

1. **Depositar** — Depositar dinero a la cuenta.
2. **Retirar** — Retirar dinero de la cuenta, si es que tienes saldo para hacerlo.
3. **Consultar saldo** — Consultar el saldo actual.
4. **Salir** — Salir del programa.

> **Pista:** guarda el saldo en una variable `saldo = 0`. Para retirar, primero comprueba que `monto <= saldo` antes de descontar. Usa `float()` para permitir montos con decimales.

---

## Ejercicio 3 — Combo (`combo.py`)

![Combo](img/combo.jpg)

Usted debe crear un programa que permita registrar un combo de comidas. Los productos disponibles y sus precios son:

| Producto     | Precio   |
|--------------|----------|
| Completo     | $5.000   |
| Papas fritas | $2.000   |
| Bebida       | $1.500   |
| Helado       | $1.000   |
| Empanadas    | $3.000   |
| Nuggets      | $2.500   |

El menú debe tener las siguientes opciones:

1. **Agregar producto** — Seleccionar y agregar un producto al combo.
2. **Ver productos** — Mostrar los productos que han sido registrados.
3. **Ver precio total** — Calcular y mostrar el precio total del combo.
4. **Salir** — Salir del programa.

> **Pista:** guarda los productos y su precio en un diccionario. Usa una lista `combo = []` para acumular lo seleccionado. El total se puede calcular con `sum()` recorriendo la lista.

---

## Ejercicio 4 — Promedio (`promedio.py`)

![Promedio](img/promedio.jpg)

Usted debe crear un programa estudiantil que permita registrar notas y calcular el promedio. El menú debe tener las siguientes opciones:

1. **Registrar nota** — Ingresar una nueva nota al registro.
2. **Ver promedio** — Calcular y mostrar el promedio de todas las notas ingresadas.
3. **Ver cantidad** — Mostrar la cantidad de notas que han sido ingresadas.
4. **Salir** — Salir del programa.

> **Pista:** usa una lista `notas = []` y agrégale cada nota con `.append()`. El promedio es `sum(notas) / len(notas)`. Antes de calcularlo, verifica que la lista no esté vacía.

---

## Ejercicio 5 — Auto (`auto.py`)

![Auto](img/auto.jpg)

Usted tiene un auto nuevo (0 km) y debe llevar un registro de sus viajes. En cada viaje debe ingresar los kilómetros recorridos y la bencina consumida. El programa acumula los datos y calcula el consumo. El menú debe tener las siguientes opciones:

1. **Registrar viaje** — Ingresar los kilómetros recorridos y la bencina consumida en el viaje.
2. **Ver consumo** — Mostrar el consumo promedio de bencina (litros por cada 100 km).
3. **Ver kilometraje** — Mostrar el total de kilómetros recorridos.
4. **Salir** — Salir del programa.

> **Pista:** acumula `km_total` y `bencina_total` sumando en cada viaje. El consumo en litros/100 km se calcula como `(bencina_total / km_total) * 100`. Usa `float()` para los valores ingresados.

---

## Ejercicio 6 — Cantante (`cantante.py`)

![Cantante](img/cantante.jpg)

Hay un concurso entre 3 legendarios cantantes: **Michael Jackson**, **Madonna** y **David Bowie**. Usted debe crear un programa que permita votar por uno de ellos y llevar el conteo. El menú debe tener las siguientes opciones:

1. **Votar** — Registrar un voto para uno de los tres cantantes.
2. **Ver resultados** — Mostrar la cantidad de votos que tiene cada cantante.
3. **Ver ganador** — Mostrar qué cantante lleva la delantera.
4. **Salir** — Salir del programa.

> **Pista:** guarda los votos en un diccionario `votos = {"Michael Jackson": 0, "Madonna": 0, "David Bowie": 0}`. Para encontrar al ganador usa `max(votos, key=votos.get)`.

---

## Ejercicio 7 — Libros (`libros.py`)

![Libros](img/libros.jpg)

Usted debe crear un programa que permita llevar un registro de hasta 3 libros. De cada libro se debe ingresar su título, autor y año de publicación. El menú debe tener las siguientes opciones:

1. **Registrar libro** — Ingresar el título, autor y año de un nuevo libro (máximo 3).
2. **Ver libros** — Mostrar todos los libros registrados con su información.
3. **Buscar libro** — Buscar un libro por su título.
4. **Salir** — Salir del programa.

> **Pista:** guarda cada libro como un diccionario `{"titulo": ..., "autor": ..., "año": ...}` dentro de una lista. Para buscar, recorre la lista y usa `in` con `.lower()` para comparar sin importar mayúsculas.

---

## Ejercicio 8 — Hotel (`hotel.py`)

![Hotel](img/hotel.jpg)

Usted es el recepcionista de un pequeño hotel que tiene **3 habitaciones** (todas disponibles al inicio). Debe crear un programa con un menú que permita gestionar las reservas. El menú debe tener las siguientes opciones:

1. **Tomar habitación** — Registrar el nombre de la persona que toma una habitación disponible.
2. **Habitaciones disponibles** — Mostrar cuántas habitaciones están disponibles.
3. **Ver huéspedes** — Mostrar el nombre de todas las personas que tienen habitaciones tomadas.
4. **Devolver habitación** — El huésped ingresa su nombre y libera su habitación.
5. **Salir** — Salir del programa.

> **Nota:** Si no hay habitaciones disponibles, el programa debe comunicar que el hotel está lleno y no permitir nuevas reservas. Para devolver una habitación, el usuario ingresa su nombre y el programa la libera.

---

## Ejercicio 9 — Estacionamiento (`estacionamiento.py`)

![Estacionamiento](img/estacionamiento.jpg)

Usted administra un estacionamiento con **5 plazas** (todas desocupadas al inicio). Debe crear un programa con menú que permita gestionar los autos. El menú debe tener las siguientes opciones:

1. **Ingresar auto** — Registrar la patente y hora de ingreso (entero, formato 0–24). No se puede ingresar si no hay plazas libres.
2. **Ver autos estacionados** — Mostrar las patentes de los autos registrados y su hora de ingreso.
3. **Registrar salida** — Ingresar la patente del auto que sale y la hora de salida. Libera la plaza e indica cuánto debe pagar (**$500 por hora**).
4. **Cantidad de autos** — Mostrar cuántos autos hay estacionados actualmente.
5. **Salir** — Salir del programa.

> **Pista:** guarda cada plaza como un diccionario `{"patente": ..., "hora_ingreso": ...}` dentro de una lista de 5 elementos (`None` = libre). Para calcular el cobro usa `(hora_salida - hora_ingreso) * 500`.

---

## Ejercicio 10 — Imperio Galáctico (`imperio_galactico.py`)

![Imperio Galáctico](img/imperio_galactico.jpg)

Estás postulando para enrolarte en el Imperio Galáctico como piloto élite de cazas **TIE Fighter**. Debes crear un programa con menú que gestione las postulaciones. Cada postulante debe ingresar su nombre, edad, especie (del universo Star Wars) y si es o no sensible a la Fuerza.

El menú debe tener las siguientes opciones:

1. **Ingresar nuevo postulante** — Solicitar y validar los datos del postulante.
2. **Mostrar todos los postulantes** — Listar todos los postulantes registrados.
3. **Mostrar postulantes calificados** — Mostrar solo quienes cumplen los requisitos.
4. **Porcentaje de calificados** — Mostrar qué porcentaje del total está calificado.
5. **Salir** — Salir del programa.

Un postulante está **calificado** si cumple **todas** estas condiciones:

| Condición | Requisito |
|-----------|-----------|
| Edad | Menor a **25 años** |
| Especie | **Humano** |
| Sensible a la Fuerza | **Sí** |

> **Pista:** guarda cada postulante como un diccionario con claves `nombre`, `edad`, `especie` y `sensible`, y agrégalo a una lista. Para filtrar calificados usa una comprensión de lista con una función auxiliar `es_calificado(p)`.
