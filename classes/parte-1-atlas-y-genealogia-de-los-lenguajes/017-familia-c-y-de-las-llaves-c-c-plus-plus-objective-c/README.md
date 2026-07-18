# Clase 017 — Familia C y de las llaves: C, C++, Objective-C

> Parte **1 — Atlas y genealogía de los lenguajes** · ⏱️ Duración estimada: **75 min** · Nivel: **Fundamentos**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

Conocer la familia más influyente en la sintaxis actual: C y sus descendientes directos. C (1972) definió las llaves `{}`, el `;`, los tipos y la cercanía a la memoria que hoy reconoces en Java, C#, JavaScript, Go y muchos más. Aprender a leer C es aprender a leer media programación.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Reconocer los rasgos de C que heredaron docenas de lenguajes.
2. Distinguir C de C++ (OO + plantillas) y Objective-C (mensajes al estilo Smalltalk).
3. Explicar por qué 'saber C' facilita leer casi cualquier lenguaje de llaves.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | C: el ancestro | Llaves, punteros, memoria manual, tipos primitivos |
| 2 | C++: C con objetos | Clases, plantillas y RAII sobre la base de C |
| 3 | Objective-C: C con mensajes | OO al estilo Smalltalk; base de macOS/iOS clásico |
| 4 | La herencia sintáctica | Por qué Java, C#, JS y Go 'se parecen a C' |

## 📖 Definiciones y características

- **C** — lenguaje de 1972 (Dennis Ritchie, Bell Labs) para sistemas. Clave: control total de la memoria; en el núcleo del curso.
- **C++** — extensión de C (1985, Bjarne Stroustrup) con OO, plantillas y RAII. Clave: potencia y complejidad; primo directo.
- **Objective-C** — C + mensajería estilo Smalltalk (1984, Brad Cox). Clave: lenguaje histórico de Apple, hoy sustituido por Swift.
- **Sintaxis de llaves** — bloques delimitados por `{}` y sentencias con `;`. Clave: la marca de la familia, heredada por decenas de lenguajes.

## 🧩 Situación

Alguien que solo sabe JavaScript abre por primera vez código en C y, para su sorpresa, entiende los bucles, los `if`, las llaves y las funciones. No es casualidad: JavaScript heredó esa sintaxis de C a través de Java.

## 🔎 Ejemplo

El mismo bucle revela el parentesco de la familia de llaves:

```text
C:     for (int i = 0; i < 3; i++) { printf("%d", i); }
C++:   for (int i = 0; i < 3; i++) { std::cout << i; }
Java:  for (int i = 0; i < 3; i++) { System.out.print(i); }
JS:    for (let i = 0; i < 3; i++) { console.log(i); }
```

## ✍️ Práctica

Toma un `for` en un lenguaje que conozcas y reescríbelo en C mentalmente. ¿Qué cambia (semántica) más allá de la escritura (sintaxis)?

## ⚠️ Errores comunes

- **Creer que C++ es 'solo C con clases'** → causa: subestimar su complejidad (plantillas, RAII, sobrecarga) → solución: tratarlo como un lenguaje propio, no como C decorado
- **Asumir que llaves iguales = comportamiento igual** → causa: confundir sintaxis con semántica → solución: verificar la gestión de memoria y tipos de cada miembro

## ❓ Preguntas frecuentes

- **¿Por qué C sigue vivo tras 50 años?** Es la base de sistemas operativos, drivers y del runtime de casi todo. Rápido y portable.
- **¿Objective-C está muerto?** En desuso frente a Swift, pero aún corre en mucho software de Apple existente.

## 🔗 Referencias

- Documentación de referencia de cada lenguaje del núcleo.

---

> [⏮️ Clase 016](../../parte-1-atlas-y-genealogia-de-los-lenguajes/016-como-nace-y-evoluciona-un-lenguaje-estandares-versiones-y-ecosistemas/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 018 ⏭️](../../parte-1-atlas-y-genealogia-de-los-lenguajes/018-familia-scripting-dinamico-python-ruby-perl-php-lua/README.md)
