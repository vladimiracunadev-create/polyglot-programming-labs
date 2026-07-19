# Clase 017 — Familia C y de las llaves: C, C++, Objective-C

> Parte **1 — Atlas y genealogía de los lenguajes** · ⏱️ Duración estimada: **75 min** · Nivel: **Fundamentos**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

Conocer la familia más influyente en la sintaxis de la programación actual: **C** y sus descendientes directos. Cuando en 1972 Dennis Ritchie escribió C en los Bell Labs para reimplementar el sistema operativo Unix, fijó una forma de escribir —llaves `{}` para delimitar bloques, `;` para terminar sentencias, paréntesis para las condiciones, tipos declarados antes del nombre— que resultó tan práctica que fue adoptada, con variaciones semánticas enormes, por Java, C#, JavaScript, Go, PHP y Rust. Aprender a leer C es, literalmente, aprender a leer media programación.

Esto importa porque la familia de llaves es el "idioma común" de la industria. Sebesta, en su capítulo sobre la evolución de los lenguajes, describe cómo la línea BCPL → B → C → C++ transporta rasgos que hoy das por sentados sin saber que nacieron ahí. Reconocer ese aire de familia te da una ventaja concreta: al abrir por primera vez un lenguaje que nunca estudiaste, si ves llaves y `;` ya entiendes el 70% de su estructura antes de leer una sola línea de su documentación.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Reconocer los rasgos de C que heredaron docenas de lenguajes posteriores.
2. Distinguir C de C++ (OO, plantillas, RAII) y de Objective-C (mensajes al estilo Smalltalk).
3. Separar la herencia **sintáctica** (la piel compartida) de la **semántica** (cómo cada primo gestiona memoria y tipos).
4. Explicar por qué "saber C" facilita leer casi cualquier lenguaje de llaves.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | C: el ancestro | Llaves, punteros, memoria manual, tipos primitivos |
| 2 | C++: C con objetos | Clases, plantillas y RAII sobre la base de C |
| 3 | Objective-C: C con mensajes | OO al estilo Smalltalk; base del macOS/iOS clásico |
| 4 | La herencia sintáctica | Por qué Java, C#, JS y Go "se parecen a C" |
| 5 | Sintaxis vs. semántica | La misma piel oculta esqueletos muy distintos |

## 📖 Definiciones y características

**C** (Dennis Ritchie, 1972) fue diseñado con un objetivo brutalmente concreto: reescribir Unix en algo más portable que el ensamblador sin perder control ni velocidad. De ahí sus rasgos definitorios: acceso directo a la memoria mediante punteros, gestión manual (`malloc`/`free`), tipos primitivos que se corresponden con lo que entiende la CPU, y una biblioteca estándar mínima. C es pequeño, rápido y peligroso: te da todo el poder de la máquina y ninguna red de seguridad. Su libro canónico, *The C Programming Language* de Kernighan y Ritchie —el célebre "K&R"—, es uno de los textos técnicos más influyentes jamás escritos y sigue siendo la referencia del núcleo del curso. Cincuenta años después, C sostiene los kernels de Linux, Windows y macOS, los drivers, y los runtimes de casi todos los demás lenguajes.

**C++** (Bjarne Stroustrup, 1985; originalmente "C with Classes") extiende C con programación orientada a objetos, plantillas (programación genérica), sobrecarga de operadores y, sobre todo, **RAII** (Resource Acquisition Is Initialization): la idea de que un recurso —memoria, un archivo, un candado— se libera automáticamente cuando su objeto sale de ámbito, mediante el destructor. RAII es el ancestro conceptual de los `defer`, `using` y `with` de otros lenguajes. El error clásico es verlo como "C con clases decorado": C++ es un lenguaje propio, mucho más grande y complejo, donde las plantillas y la resolución de sobrecargas exigen un modelo mental que C no requiere. **Objective-C** (Brad Cox, 1984) tomó otro camino: mantuvo C intacto y le añadió por encima el sistema de mensajería dinámica de Smalltalk (`[objeto mensaje:argumento]`). Fue el lenguaje de NeXT y luego de todo el ecosistema de Apple hasta que Swift lo relevó a partir de 2014; hoy sobrevive en enormes bases de código existentes.

La lección central de esta familia es distinguir **herencia sintáctica** de **herencia semántica**. Java, C#, JavaScript, Go y PHP heredaron la piel de C —las llaves, el `for` de tres partes, los `if`— pero cambiaron el esqueleto: unos añadieron recolección de basura, otros máquinas virtuales, otros tipado dinámico. Sebesta insiste en que confundir ambos niveles es el origen de bugs sutiles al portar código: el `for (int i=0; i<n; i++)` se ve idéntico en seis lenguajes, pero lo que ocurre con los desbordamientos, la aritmética de enteros o el paso de argumentos puede ser radicalmente distinto. La piel te dice a qué familia pertenece un lenguaje; solo el esqueleto te dice cómo se comportará.

- **C** — lenguaje de 1972 (Ritchie, Bell Labs) para sistemas. Clave: control total de la memoria; está en el núcleo del curso.
- **C++** — extensión de C (1985, Stroustrup) con OO, plantillas y RAII. Clave: potencia y complejidad; un lenguaje propio, no C decorado.
- **Objective-C** — C + mensajería estilo Smalltalk (1984, Cox). Clave: lenguaje histórico de Apple, hoy relevado por Swift.
- **Sintaxis de llaves** — bloques con `{}` y sentencias con `;`. Clave: la marca de la familia, heredada por decenas de lenguajes con semánticas muy distintas.

## 🧩 Situación

Una desarrolladora que solo ha escrito JavaScript abre por primera vez un archivo `.c` de un proyecto de código abierto para arreglar un bug menor. Espera perderse, y en cambio reconoce los bucles, los `if`, las llaves, las funciones y hasta la forma de los comentarios. No es suerte: JavaScript heredó esa sintaxis de C a través de Java, en 1995, cuando Netscape quiso que su lenguaje "se pareciera a Java" para atraer programadores. Lo que la sorprende de verdad no es la piel familiar, sino el esqueleto: los punteros, el `malloc` y la ausencia de recolector de basura. Ahí está, exactamente, la frontera entre lo sintáctico y lo semántico.

## 🔎 Ejemplo

El mismo bucle revela el parentesco de la familia de llaves. La forma es casi idéntica; lo que imprime cada uno depende de su biblioteca:

```text
C:     for (int i = 0; i < 3; i++) { printf("%d", i); }
C++:   for (int i = 0; i < 3; i++) { std::cout << i; }
Java:  for (int i = 0; i < 3; i++) { System.out.print(i); }
JS:    for (let i = 0; i < 3; i++) { console.log(i); }
Go:    for i := 0; i < 3; i++ { fmt.Print(i) }
```

Cuatro de los cinco comparten hasta el `for (…; …; …)` de tres partes que C inventó (Go solo elimina los paréntesis exteriores). El **delta** semántico está oculto: en C ese `i` es un entero de máquina que puede desbordar en silencio; en JavaScript es un número de coma flotante de 64 bits; en Java es un `int` de 32 bits con desbordamiento definido. Misma escritura, tres realidades distintas bajo la superficie.

## ✍️ Práctica

Toma un bucle `for` de un lenguaje que conozcas y reescríbelo mentalmente en C. Luego responde por escrito: ¿qué parte del cambio es puramente **sintáctica** (cómo se escribe) y qué parte sería **semántica** (qué ocurre con el tipo del contador, el desbordamiento o la gestión de memoria)? Si tu lenguaje de origen tiene recolector de basura y C no, ¿qué responsabilidad nueva aparece?

## ⚠️ Errores comunes

- **Creer que C++ es "solo C con clases"** → causa: subestimar plantillas, RAII y sobrecarga → solución: tratarlo como un lenguaje propio con su propio modelo mental.
- **Asumir que "llaves iguales" implica "comportamiento igual"** → causa: confundir sintaxis con semántica → solución: verificar siempre la gestión de memoria, los tipos y el paso de argumentos de cada miembro.
- **Escribir C con mentalidad de lenguaje con GC** → causa: olvidar liberar memoria → solución: parear cada `malloc` con su `free` y razonar sobre la propiedad de cada puntero.

## ❓ Preguntas frecuentes

- **¿Por qué C sigue vivo tras más de 50 años?** Porque es la base de los sistemas operativos, los drivers y el runtime de casi todo. Es pequeño, rápido, portable y su modelo de máquina es predecible.
- **¿Objective-C está muerto?** Está en desuso frente a Swift para proyectos nuevos, pero corre en enormes bases de código existentes de Apple que siguen manteniéndose.
- **¿Aprender C hoy sirve para algo si voy a programar en la web?** Sí: entender punteros, pila y memoria te hace mejor en cualquier lenguaje, y la sintaxis de C es la puerta a la mitad del árbol genealógico.

## 🔗 Referencias

- B. Kernighan y D. Ritchie — *The C Programming Language* (2ª ed., Prentice Hall).
- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson), cap. 2 (linaje BCPL → B → C → C++).
- M. L. Scott — *Programming Language Pragmatics* (4ª ed., Morgan Kaufmann).
- B. A. Tate — *Seven Languages in Seven Weeks* (Pragmatic Bookshelf).

---

> [⏮️ Clase 016](../../parte-1-atlas-y-genealogia-de-los-lenguajes/016-como-nace-y-evoluciona-un-lenguaje-estandares-versiones-y-ecosistemas/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 018 ⏭️](../../parte-1-atlas-y-genealogia-de-los-lenguajes/018-familia-scripting-dinamico-python-ruby-perl-php-lua/README.md)
