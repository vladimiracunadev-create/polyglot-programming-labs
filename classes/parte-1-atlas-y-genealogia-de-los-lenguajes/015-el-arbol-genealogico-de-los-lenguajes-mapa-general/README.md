# Clase 015 — El árbol genealógico de los lenguajes: mapa general

> Parte **1 — Atlas y genealogía de los lenguajes** · ⏱️ Duración estimada: **75 min** · Nivel: **Fundamentos**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

Ver el mapa completo de las familias de lenguajes y sus antepasados comunes para dejar de percibir la programación como una lista inabarcable de tecnologías rivales y empezar a verla como lo que es: un puñado de linajes que descienden de unos pocos experimentos de finales de los años cincuenta. Casi todo lo que se programa hoy hereda de tres troncos: **Fortran** (1957, cálculo numérico), **Lisp** (1958, simbólico y funcional) y **ALGOL** (1958-60, del que brota la programación estructurada y, a través de C, casi toda la sintaxis de llaves).

Esto importa porque la genealogía es un atajo de aprendizaje. Sebesta abre su *Concepts of Programming Languages* argumentando que estudiar la evolución de los lenguajes no es erudición decorativa: entender de dónde viene un rasgo permite predecir cómo se comporta, reconocerlo en un lenguaje nuevo y juzgar por qué su diseñador lo eligió. El árbol convierte "decenas de lenguajes" en "cinco o seis familias con variaciones", y ese cambio de escala es la diferencia entre abrumarse y orientarse.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Ubicar los tres troncos históricos (Fortran, Lisp, ALGOL) y qué aportó cada uno.
2. Situar cada lenguaje del núcleo en su rama del árbol.
3. Distinguir **herencia** (pertenecer a una familia) de **influencia** (tomar un rasgo prestado sin serlo).
4. Explicar por qué conocer un representante de cada familia acelera aprender a sus miembros.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Los tres troncos | Fortran, Lisp y ALGOL originan casi todo lo demás |
| 2 | Ramas principales | Llaves, dinámicos, funcionales, declarativos, lógicos |
| 3 | Herencia de rasgos | Sintaxis, tipos y paradigma se transmiten de los ancestros |
| 4 | Influencias y cruces | El árbol tiene puentes, no solo ramas puras |
| 5 | Representante y primos | Un lenguaje del núcleo por rama abre la puerta a las demás |

## 📖 Definiciones y características

La historia empieza en 1957, cuando el equipo de **John Backus** en IBM entrega **Fortran** (FORmula TRANslator), el primer lenguaje de alto nivel con un compilador que producía código competitivo con el ensamblador escrito a mano. Fortran demostró que se podía abstraer la máquina sin renunciar al rendimiento, y con ello inauguró toda la computación numérica. Apenas un año después, en el MIT, **John McCarthy** diseña **Lisp** (LISt Processor) para la inteligencia artificial: introduce funciones de primera clase, recursión, recolección de basura y la idea de que el programa es una estructura de datos. Y en 1958-60, un comité internacional publica **ALGOL 60**, que aporta bloques anidados, alcance léxico, la gramática BNF para describir sintaxis y el propio concepto de programación estructurada. Sebesta dedica su capítulo 2, "Evolution of the Major Programming Languages", precisamente a esta secuencia, y su famoso diagrama de parentesco es el mapa que aquí resumimos.

De ALGOL desciende la rama más poblada. **Martin Richards** deriva BCPL (1966), de ahí sale B, y en 1972 **Dennis Ritchie** crea **C** en los Bell Labs para reescribir Unix. C fija las llaves `{}`, el punto y coma, los tipos primitivos y la aritmética de punteros. Su sintaxis resultó tan cómoda que fue copiada, con variaciones semánticas profundas, por C++ (1985), Java (1995), C# (2000), JavaScript (1995), PHP, Go y Rust. Por eso decimos que "leer C es leer media programación": la piel es compartida aunque el esqueleto —gestión de memoria, tipos, modelo de objetos— cambie por completo entre primos.

Las otras ramas nacen de necesidades distintas. La **funcional tipada** arranca con **ML** (Robin Milner, 1973) y su inferencia de tipos Hindley-Milner, y llega a OCaml, Haskell y F#; su influencia se cuela en Rust y Kotlin. La **lógica y declarativa** brota de **Prolog** (Colmerauer y Kowalski, 1972), donde se describen hechos y reglas en vez de pasos, y es prima lejana de SQL. Y los **dinámicos** —Python, Ruby, Perl, PHP— combinan la expresividad de Lisp con sintaxis cómoda para escribir rápido. Van Roy y Haridi, en *Concepts, Techniques, and Models*, insisten en que estas ramas no son tribus enemigas sino **modelos de computación** que un mismo programador debería poder combinar; el árbol genealógico es la puerta de entrada a esa mirada.

- **Tronco** — lenguaje raíz del que desciende una familia (Fortran, Lisp, ALGOL). Clave: fija rasgos que perduran décadas.
- **Familia** — grupo de lenguajes con ancestro y rasgos comunes. Clave: dominar un representante facilita leer a los demás.
- **Herencia vs. influencia** — heredar es pertenecer a la familia; influir es tomar un rasgo suelto (Rust hereda de C la sintaxis, pero recibe la *influencia* de ML en sus tipos). Clave: el árbol tiene cruces.
- **Programación estructurada** — aporte de ALGOL: bloques, alcance y control de flujo sin `goto`. Clave: base de casi todo lo imperativo posterior.

## 🧩 Situación

Un principiante abre una oferta de empleo y ve "requerido: Java; deseable: Kotlin, Go o TypeScript" y siente que le piden cuatro carreras distintas. Un veterano lee lo mismo y ve una sola: Java y Kotlin son la rama JVM, TypeScript y Go descienden de la sintaxis de C, y con reconocer los tres bucles `for` sabe que el 80% del código le resultará legible desde el primer día. La diferencia entre el pánico y la calma no es talento: es tener el árbol en la cabeza. Ese mapa es lo que esta parte del curso instala.

## 🔎 Ejemplo

Árbol simplificado con el año de nacimiento aproximado y el rasgo que cada tronco legó:

```text
Fortran (1957) ── cálculo numérico ──── Fortran, MATLAB, R, Julia
Lisp    (1958) ── simbólico/funcional ─ Scheme, Racket, Clojure  (influye en ML)
ALGOL   (1960) ── estructurado ──┬── C (1972) ── C++, Java, C#, JS, Go, Rust
                                 ├── Pascal (1970) ── Delphi
                                 └── (influye en casi todo lo imperativo)
ML      (1973) ── funcional tipado ──── OCaml, Haskell, F#  (influye en Rust)
Prolog  (1972) ── lógico ──────────────  Datalog  (primo de SQL)
```

Fíjate en los `(influye en…)`: no son ramas, son puentes. Rust cuelga de C por su sintaxis y su cercanía a la máquina, pero su `enum`, su `match` y su `Option` vienen de ML. Un lenguaje real casi nunca pertenece a una sola caja; entender el árbol es entender también sus cruces.

## ✍️ Práctica

Dibuja tu propio árbol solo con los 10 lenguajes del núcleo (Python, JavaScript, TypeScript, Java, C#, Go, Rust, C, SQL, PHP). Agrúpalos por tronco: ¿cuáles comparten la sintaxis de llaves de C? ¿Cuál corre sobre una máquina virtual? ¿Cuál no encaja en ninguna rama imperativa (pista: SQL)? Marca con una flecha discontinua al menos una **influencia** entre ramas.

## ⚠️ Errores comunes

- **Tratar cada lenguaje como algo aislado y nuevo** → causa: no ver la familia → solución: identificar el ancestro y estudiar primero los rasgos heredados.
- **Confundir parecido sintáctico con parentesco real** → causa: creer que "se escribe igual" implica "se comporta igual" → solución: separar la piel (sintaxis) del esqueleto (semántica).
- **Creer que el árbol son ramas puras sin cruces** → causa: ignorar las influencias → solución: recordar que Rust toma de C y de ML a la vez, y que casi todo lenguaje moderno es un híbrido.

## ❓ Preguntas frecuentes

- **¿Hay un árbol "oficial"?** No único, pero las relaciones históricas están muy documentadas; el diagrama del capítulo 2 de Sebesta es la referencia habitual y coincide entre fuentes.
- **¿Dónde va SQL?** Fuera del tronco imperativo: es declarativo, primo lejano de la rama lógica (Prolog). Describe qué datos quieres, no cómo obtenerlos.
- **¿Por qué importan lenguajes que no voy a escribir?** Porque sus ideas viajaron a los que sí escribes: la recolección de basura viene de Lisp, la inferencia de tipos de ML, los bloques de ALGOL.

## 🔗 Referencias

- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson), cap. 2 "Evolution of the Major Programming Languages".
- M. L. Scott — *Programming Language Pragmatics* (4ª ed., Morgan Kaufmann), cap. 1 "Introduction".
- B. A. Tate — *Seven Languages in Seven Weeks* (Pragmatic Bookshelf), introducción.
- P. Van Roy y S. Haridi — *Concepts, Techniques, and Models of Computer Programming* (MIT Press), cap. 1.

---

> [⏮️ Clase 014](../../parte-0-pensamiento-computacional-y-el-metodo-poliglota/014-como-elegir-lenguaje-para-un-problema/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 016 ⏭️](../../parte-1-atlas-y-genealogia-de-los-lenguajes/016-como-nace-y-evoluciona-un-lenguaje-estandares-versiones-y-ecosistemas/README.md)
