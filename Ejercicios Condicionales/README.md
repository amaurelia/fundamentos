# Ejercicios

Esta carpeta contiene los ejercicios propuestos para practicar el uso de condicionales.

---

## Ejercicio 1 — El videojuego divertido (`requerimientos.py`)

![Requerimientos](img/requerimientos.jpg)

Tienes un juego muy entretenido, pero no siempre funciona bien en todos los computadores. El programa debe solicitar las características del equipo y determinar cómo se comporta el juego.

El programa debe pedir:

| Dato              | Tipo    | Descripción                     |
|-------------------|---------|---------------------------------|
| RAM disponible    | Entero  | Cantidad de GB de memoria RAM   |
| Tarjeta de video  | True/False | Si el computador tiene tarjeta de video dedicada |

Según las características del computador, el juego se comporta así:

| Tarjeta de video | RAM disponible | Resultado              |
|------------------|----------------|------------------------|
| Sin tarjeta      | Cualquier RAM  | El juego no funciona   |
| Con tarjeta      | Menor a 2 GB   | Funciona a **30 FPS**  |
| Con tarjeta      | 2 GB o más     | Funciona a **60 FPS**  |

---

## Ejercicio 2 — El helado de tu amigo (`helado.py`)

![Helado](img/helado.jpg)

A tu amigo le encanta el helado, pero solo disfruta ciertas combinaciones de sabor y salsa. El programa debe pedir las preferencias y determinar si la combinación resultará rica o no.

El programa debe pedir:

| Dato           | Opciones disponibles            |
|----------------|---------------------------------|
| Sabor de helado | vainilla, chocolate, mixto     |
| Salsa          | manjar, chocolate, frutilla     |

Dependiendo de la combinación elegida, el resultado será:

| Condición                                | Resultado   |
|------------------------------------------|-------------|
| Sabor vainilla con salsa frutilla        | Desabrido   |
| Sabor chocolate (con cualquier salsa)    | Sabroso     |
| Sabor mixto con salsa manjar o frutilla  | Sabroso     |
| Cualquier otra combinación               | Normal      |

---

## Ejercicio 3 — La batalla contra el rey del mal (`heroe.py`)

![Héroe](img/heroe.jpg)

Debes combatir al rey del mal, pero tu destino depende del nivel que tengas y del equipo que lleves. El programa debe evaluar tus posibilidades de victoria.

El programa debe pedir:

| Dato                 | Tipo       | Descripción                                  |
|----------------------|------------|----------------------------------------------|
| Armadura del destino | True/False | Si el héroe lleva la armadura del destino    |
| Espada infinita      | True/False | Si el héroe lleva la espada infinita         |
| Nivel                | Entero     | Nivel actual del héroe                       |

El resultado de tu probabilidad de vencer será:

| Condición                                                          | Probabilidad de vencer |
|--------------------------------------------------------------------|------------------------|
| Nivel menor a 40                                                   | Sin oportunidad        |
| Nivel entre 40 y 79, con espada infinita                          | 20%                    |
| Nivel 80 o más, con espada infinita, sin armadura del destino     | 40%                    |
| Nivel 80 o más, con espada infinita y armadura del destino        | 60%                    |
| Cualquier otro caso                                                | 1%                     |

---

## Ejercicio 4 — Postulando a la beca (`beca.py`)

![Beca](img/beca.jpg)

Estás postulando a una beca universitaria. Tus posibilidades dependen de tus notas de programación y de inglés. El programa debe evaluar si puedes postular y cuál es tu probabilidad de obtenerla.

El programa debe pedir:

| Dato                | Tipo   | Descripción                           |
|---------------------|--------|---------------------------------------|
| Nota de programación | Float  | Tu nota en programación (escala 1–7) |
| Nota de inglés      | Float  | Tu nota en inglés (escala 1–7)       |

Las reglas son las siguientes:

| Condición                                        | Resultado                        |
|--------------------------------------------------|----------------------------------|
| Nota de programación o inglés menor a 4.0        | No puedes postular               |
| Nota de programación > 6.0 y nota de inglés > 6.0 | Puedes postular — **40% de probabilidad** |
| Nota de programación > 4.0 y nota de inglés > 6.0 | Puedes postular — **20% de probabilidad** |
| Cualquier otro caso aprobado                     | Puedes postular — sin ventaja especial |

---

## Ejercicio 5 — FONASA (`fonasa.py`)

![FONASA](img/fonasa.jpg)

Dependiendo de tu tramo de FONASA y tu edad, tendrás un porcentaje de descuento en tus atenciones médicas. El programa debe calcular el descuento que te corresponde.

El programa debe pedir:

| Dato   | Tipo   | Descripción                            |
|--------|--------|----------------------------------------|
| Tramo  | Letra  | Tu tramo FONASA: A, B, C o D          |
| Edad   | Entero | Tu edad en años                        |

El descuento se determina según las siguientes reglas:

| Condición                            | Descuento |
|--------------------------------------|-----------|
| Tramo D (cualquier edad)             | 20%       |
| Tramo C y edad 18 años o más         | 15%       |
| Tramo C y edad menor a 18 años       | 18%       |
| Tramo A o B y edad menor a 65 años   | 25%       |
| Tramo A o B y edad 65 años o más     | 40%       |

---

## Ejercicio 6 — El dilema del prisionero (`prisionero.py`)

![Prisionero](img/prisionero.jpg)

Dos personas han sido detenidas como sospechosas de robar un banco. Las autoridades las interrogan por separado y cada una debe tomar una decisión sin saber qué elegirá la otra: **declararse inocente** o **delatar al otro**.

La condena de cada una dependerá de la combinación de declaraciones:

| Persona 1        | Persona 2        | Resultado                                              |
|------------------|------------------|--------------------------------------------------------|
| Inocente         | Inocente         | Ambas reciben **1 año** de prisión por receptación    |
| Delata a la 2    | Inocente         | Persona 1 queda **libre**, persona 2 recibe **10 años** |
| Inocente         | Delata a la 1    | Persona 2 queda **libre**, persona 1 recibe **10 años** |
| Delata a la 2    | Delata a la 1    | Ambas reciben **10 años** de prisión                  |

El programa debe pedir la declaración de cada persona (inocente / culpable) y mostrar la condena correspondiente para cada una.
