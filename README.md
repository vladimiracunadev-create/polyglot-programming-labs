<div align="center">

# 🌐 Polyglot Programming Labs

## **176 clases · 12 partes · un concepto, 10 lenguajes, ~40 familias**

**El programa de programación comparada más completo en español — aprende el concepto una vez y reconócelo, compáralo y aplícalo en Python, JavaScript, TypeScript, Java, C#, Go, Rust, C, SQL y PHP, con un Atlas que te deja leer decenas de lenguajes más.**

[![CI](https://github.com/vladimiracunadev-create/polyglot-programming-labs/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/vladimiracunadev-create/polyglot-programming-labs/actions/workflows/ci.yml)
[![Labs](https://github.com/vladimiracunadev-create/polyglot-programming-labs/actions/workflows/labs.yml/badge.svg?branch=main)](https://github.com/vladimiracunadev-create/polyglot-programming-labs/actions/workflows/labs.yml)
[![Security](https://github.com/vladimiracunadev-create/polyglot-programming-labs/actions/workflows/security.yml/badge.svg?branch=main)](https://github.com/vladimiracunadev-create/polyglot-programming-labs/actions/workflows/security.yml)
[![Deploy Pages](https://github.com/vladimiracunadev-create/polyglot-programming-labs/actions/workflows/deploy-pages.yml/badge.svg?branch=main)](https://github.com/vladimiracunadev-create/polyglot-programming-labs/actions/workflows/deploy-pages.yml)

[![Clases](https://img.shields.io/badge/clases-176%20·%2012%20partes-7c5cff?style=for-the-badge)](classes/README.md)
[![Núcleo](https://img.shields.io/badge/núcleo-10%20lenguajes-2e8b57?style=for-the-badge)](languages.json)
[![Atlas](https://img.shields.io/badge/atlas-~40%20familias-orange?style=for-the-badge)](atlas/README.md)
[![Idioma](https://img.shields.io/badge/idioma-español-blue?style=for-the-badge)](README.md)
[![License](https://img.shields.io/badge/license-MIT-3fb950?style=for-the-badge)](LICENSE)

[📚 Índice completo de clases](classes/README.md) · [📕 Manual completo (PDF)](manual/MANUAL.pdf) · [🌐 Atlas de lenguajes](atlas/README.md) · [🧭 Rutas](rutas/README.md) · [📝 Autoevaluación](autoevaluaciones/README.md) · [🗺️ Roadmap](ROADMAP.md) · [🤝 Contribuir](CONTRIBUTING.md) · [🔐 Seguridad](SECURITY.md)

</div>

---

> 🧭 **Estado del programa.** Las **176 clases en 12 partes están construidas**. Las clases de código (Partes 3–11) traen sus **10 implementaciones del núcleo con el código a la vista y verificadas en CI** contra su `casos.json`; las de método (Partes 0–2) son las clases conceptuales de pensamiento, familias de lenguajes y toolchains.
>
> **Qué verifica una máquina y qué no**, para que sepas de qué te fías: el **[verificador de equivalencia](scripts/verificar_equivalencia.py)** ejecuta en CI las implementaciones de cada clase de código contra su `casos.json` y comprueba que **todas producen la misma salida**. El texto de las clases y el Atlas son material de lectura escrito a mano, apoyado en los libros de referencia: **no** se ejecutan en CI. Si el badge de CI está verde, garantiza que las implementaciones equivalentes lo son de verdad.

## 🎯 Qué es esto

Un currículo modular y **secuencial** que enseña **los conocimientos transferibles de la programación**: no diez cursos aislados, sino cada concepto (una variable, un bucle, una función, un tipo) mostrado una vez y luego **comparado** entre lenguajes. La pregunta que responde cada clase no es "¿cómo se escribe en X?", sino **"¿qué permanece y qué cambia —y por qué— al pasar de un lenguaje a otro?"**.

Cada clase es una carpeta con un `README.md` completo que incluye:

- 🎯 **Objetivo** y **resultados de aprendizaje verificables**.
- 🗺️ **Temas** con el porqué de cada uno · 📖 **Definiciones** de los términos.
- 🧮 **Modelo** (entradas/salidas/reglas) y 📐 **algoritmo en pseudocódigo neutral**.
- 🌐 **Implementaciones idiomáticas con el código a la vista** en los 10 lenguajes del núcleo.
- 🔬 **Comparación** (sintáctica · semántica · paradigmática) y 🧬 **el concepto en la familia**.
- ✅ **Prueba común** (`casos.json`) · 🧪 **reto de transferencia** · ⚠️ **errores comunes** · ❓ **FAQ**.
- 🔗 **Referencias** a los libros del área y de cada lenguaje.

## 📚 Pauta derivada de los mejores libros

El contenido no sale de una plantilla: cada parte sigue la literatura de referencia de su tema. Estos son los libros que sostienen el programa (las referencias apuntan a las obras; **no se reproduce su contenido**, la redacción es original).

| Área | Libros de referencia |
|---|---|
| **Pensamiento y algoritmos** | Polya — *How to Solve It* · Abelson/Sussman — *SICP* · Cormen et al. — *Introduction to Algorithms* · Hunt/Thomas — *The Pragmatic Programmer* |
| **Lenguajes y paradigmas** | Sebesta — *Concepts of Programming Languages* · Scott — *Programming Language Pragmatics* · Van Roy/Haridi — *Concepts, Techniques, and Models…* · Tate — *Seven Languages in Seven Weeks* |
| **Tipos y semántica** | Pierce — *Types and Programming Languages* · Dahl/Dijkstra/Hoare — *Structured Programming* |
| **Datos y estructuras** | Cormen et al. — *Introduction to Algorithms* · Sedgewick/Wayne — *Algorithms* |
| **Runtime y compilación** | Nystrom — *Crafting Interpreters* · Aho et al. — *Compilers* («Dragon Book») · Bryant/O'Hallaron — *Computer Systems: A Programmer's Perspective* |
| **Ingeniería de software** | McConnell — *Code Complete* · Martin — *Clean Code* · Fowler — *Refactoring* · Gamma et al. — *Design Patterns* (GoF) · Beck — *TDD by Example* |
| **Interoperabilidad y sistemas** | Kleppmann — *Designing Data-Intensive Applications* · Newman — *Building Microservices* · Tanenbaum — *Distributed Systems* · Nygard — *Release It!* |
| **Toolchains y entorno** | Shotts — *The Linux Command Line* · Kernighan/Pike — *The Unix Programming Environment* |
| **Por lenguaje (núcleo)** | Ramalho — *Fluent Python* · Bloch — *Effective Java* · Donovan/Kernighan — *The Go Programming Language* · Klabnik/Nichols — *The Rust Programming Language* · Kernighan/Ritchie — *K&R* · Haverbeke — *Eloquent JavaScript* · Cherny — *Programming TypeScript* · Skeet — *C# in Depth* · Date — *SQL and Relational Theory* · Lockhart — *Modern PHP* |

Cada clase cita, en su sección de 🔗 **Referencias**, los libros de su parte y el libro del lenguaje.

## 🧩 Núcleo y Atlas: dos capas

| Capa | Qué es | Lenguajes |
|---|---|---|
| **Núcleo** | Se implementa, se muestra a la vista y **se verifica en CI** | Python, JavaScript, TypeScript, Java, C#, Go, Rust, C, SQL, **PHP** |
| **Atlas** | Se **comprende por características** (historia, paradigma, toolchain, primos) | ~40 familias: Ruby, Kotlin, Haskell, Elixir, Lisp, Prolog, Bash, Zig, Lua… |

La idea: **aprende el representante, reconoce la familia entera.** Si dominas C, ya lees el 80 % de la sintaxis de Java, C#, JS, Go y PHP. El **[Atlas](atlas/README.md)** cubre esa amplitud sin multiplicar el mantenimiento.

## 🗂️ Las 12 partes

| # | Parte | Clases | Rango |
|---|---|---:|---|
| 0 | Pensamiento computacional y el método políglota | 14 | 001–014 |
| 1 | Atlas y genealogía de los lenguajes | 14 | 015–028 |
| 2 | Herramientas, toolchains y anatomía de comandos | 12 | 029–040 |
| 3 | Valores, tipos y variables | 16 | 041–056 |
| 4 | Control del programa | 16 | 057–072 |
| 5 | Funciones y modularidad | 16 | 073–088 |
| 6 | Datos y estructuras | 18 | 089–106 |
| 7 | Paradigmas | 16 | 107–122 |
| 8 | Cómo funcionan los lenguajes | 16 | 123–138 |
| 9 | Ingeniería de software políglota | 16 | 139–154 |
| 10 | Interoperabilidad y fronteras entre lenguajes | 10 | 155–164 |
| 11 | Proyecto integrador políglota | 12 | 165–176 |

➡️ **[Ver el índice completo de las 176 clases](classes/README.md)**

## 📕 Manual completo (todo el curso en un documento)

¿Prefieres el curso entero en un solo sitio, para leer de corrido o estudiar sin conexión? El **manual** consolida las **176 clases** en orden, con portada e índice enlazado, y **con el código de los 10 lenguajes a la vista**, que es lo que hace que valga la pena en papel: se comparan sin saltar entre archivos.

- 📥 **[Descargar el manual en PDF](manual/MANUAL.pdf)** — listo para imprimir o leer offline.

> Se genera con `python scripts/generar_manual.py` a partir de las clases, así que siempre refleja el contenido actual del repositorio. Para guías sueltas por clase: `python scripts/generar_material.py --parte 3` deja los PDF en `material/` (no se versionan).

## 🧬 Los primos: el mismo programa en toda la familia

Cada muestra de código del núcleo enlaza, justo debajo, a las versiones del **mismo programa** en los lenguajes primos de su familia. Si lees el bloque de Python, ves de inmediato cómo lo escribirían Ruby, Perl, Lua, Tcl o R:

```markdown
🧬 El mismo programa en la familia Scripting dinámico: Ruby · Perl · Lua · Tcl · R
```

Son **2722 programas** repartidos en las 7 familias del Atlas, y lo que da valor a cada página no es el código sino el párrafo *«Qué reconocer»* que la cierra: que `0` es verdadero en Lua y Clojure, que Lua hace herencia por `__index` —el mismo modelo de prototipos de JavaScript—, o que el *name mangling* de C++ no está estandarizado entre compiladores.

Ruby, Perl y Lua **se ejecutan en CI** contra el mismo `casos.json` que el núcleo ([workflow Labs](.github/workflows/labs.yml)); los otros 17 primos son material de lectura y así se declara en cada página.

## 🧪 El verificador de equivalencia

El diferenciador de este programa: cada clase de código define un `casos.json` (entradas y salidas comunes), y el verificador ejecuta **todas** las implementaciones alimentándolas por stdin para comprobar que **coinciden**. No es teoría: es equivalencia demostrada por máquina, en paralelo por lenguaje en CI.

```bash
python scripts/verificar_equivalencia.py 041            # una clase
python scripts/verificar_equivalencia.py --all          # todas las clases
python scripts/verificar_equivalencia.py --all --lang go  # solo un lenguaje
```

Los lenguajes cuyo toolchain no esté instalado se **omiten** e informan (degradación silenciosa); SQL, al ser declarativo, se marca como *ilustrativo*.

## 🧭 Portal

- 🧭 **[Rutas por perfil](rutas/README.md)** — "vengo de Python", "quiero sistemas (C/Rust)", "web (JS/TS)", "backend (Java/C#/Go)", "datos (SQL)".
- 🌐 **[Atlas de lenguajes](atlas/README.md)** — genealogía, historia, características y toolchain de cada familia.
- 📝 **[Autoevaluaciones](autoevaluaciones/README.md)** — una batería de preguntas por parte.
- 📖 **[Glosario](glosario/README.md)** — términos enlazados a la clase donde se explican.
- 🧪 **[Laboratorios](labs/README.md)** — la equivalencia demostrada: el verificador sobre las implementaciones.

🌐 Todo navegable en el **[sitio del curso](https://vladimiracunadev-create.github.io/polyglot-programming-labs/)** (GitHub Pages).

## 🗂️ Estructura del repositorio

```text
classes/
  _manifest.json          # fuente de verdad (176 clases)
  README.md               # índice completo
  parte-N-.../
    README.md             # README de la parte (con sus libros de referencia)
    NNN-.../
      README.md           # la clase, con el código a la vista
      concepto.md comparacion.md reto.md casos.json
      implementaciones/<lenguaje>/...
atlas/  rutas/  autoevaluaciones/  glosario/  labs/
scripts/  docs/  .github/workflows/
```

## 👩‍🏫 Para instructores

- 📅 **[Syllabus y cronograma](docs/syllabus.md)** — horas por parte, dependencias y un plan de ~41 semanas.
- 📊 **[Rúbrica de evaluación](docs/rubrica-evaluacion.md)** — cómo puntuar retos de transferencia, laboratorios y el proyecto integrador.
- 🎓 **[Examen final por perfil](docs/examen-final-por-perfil.md)** — teoría + transferencia verificada + explicación, para cada ruta.
- 🧱 **[Currículo](docs/CURRICULO.md)** · **[Metodología](docs/METODOLOGIA.md)** · **[Ampliar lenguajes](docs/EXTENDER.md)**.

## 🚀 Cómo estudiar

```text
problema → concepto → pseudocódigo → implementaciones → comparación → transferencia
```

1. **Sigue el orden.** La numeración es global y secuencial por diseño: cada clase asume la anterior. Empieza por la [Parte 0](classes/parte-0-pensamiento-computacional-y-el-metodo-poliglota/README.md), que fija el método de comparación.
2. **Lee las 10 implementaciones, no solo la de tu lenguaje.** El valor de cada clase está en el contraste: ahí se ve qué es esencial y qué es accidente de la sintaxis.
3. **Ejecuta el verificador.** Comprueba tú mismo que las implementaciones son equivalentes, y observa en qué se diferencian sus salidas cuando fuerzas un caso límite.
4. **Haz el reto de transferencia.** Portar el concepto a un lenguaje que no dominas es donde se fija el aprendizaje.
5. **Usa los libros de referencia** de cada parte para profundizar en lo que más te interese.

## Principios

- Comparar conceptos, no solo sintaxis.
- Anclar el contenido en los **libros de referencia** de cada área.
- Mantener el mismo problema, datos de prueba y resultado esperado en todos los lenguajes.
- Explicar diferencias reales sin declarar que todos los lenguajes son iguales.
- Distinguir siempre lo que verifica la máquina de lo que es material de lectura.
- Crecer por conceptos, no por cursos aislados.
- Usar `pnpm` en todo componente JavaScript/TypeScript que requiera paquetes.

## 🤝 Contribuir y seguridad

Lee la [guía de contribución](CONTRIBUTING.md) y la [política de seguridad](SECURITY.md). El repositorio escanea secretos con `gitleaks` y el tooling con `bandit` en cada push.

## Licencia

MIT. Consulta [LICENSE](LICENSE).
