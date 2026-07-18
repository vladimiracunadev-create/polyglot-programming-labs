<div align="center">

# 🌐 Polyglot Programming Labs

## **176 clases · 12 partes · un concepto, diez lenguajes, ~40 familias**

**El programa de programación comparada en español: aprende el concepto una vez y reconócelo, compáralo y aplícalo en Python, JavaScript, TypeScript, Java, C#, Go, Rust, C, SQL y PHP — con el Atlas de familias que te deja leer decenas de lenguajes más.**

[![CI](https://github.com/vladimiracunadev-create/polyglot-programming-labs/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/vladimiracunadev-create/polyglot-programming-labs/actions/workflows/ci.yml)
[![Deploy Pages](https://github.com/vladimiracunadev-create/polyglot-programming-labs/actions/workflows/deploy-pages.yml/badge.svg?branch=main)](https://github.com/vladimiracunadev-create/polyglot-programming-labs/actions/workflows/deploy-pages.yml)

[![Clases](https://img.shields.io/badge/clases-176%20·%2012%20partes-7c5cff?style=for-the-badge)](classes/README.md)
[![Núcleo](https://img.shields.io/badge/núcleo-10%20lenguajes-2e8b57?style=for-the-badge)](languages.json)
[![Atlas](https://img.shields.io/badge/atlas-~40%20familias-orange?style=for-the-badge)](atlas/README.md)
[![Idioma](https://img.shields.io/badge/idioma-español-blue?style=for-the-badge)](README.md)
[![License](https://img.shields.io/badge/license-MIT-3fb950?style=for-the-badge)](LICENSE)

[🌐 Sitio del curso](https://vladimiracunadev-create.github.io/polyglot-programming-labs/) · [📚 Clases](classes/README.md) · [🌐 Atlas](atlas/README.md) · [🧭 Rutas](rutas/README.md) · [📝 Autoevaluación](autoevaluaciones/README.md) · [📖 Glosario](glosario/README.md) · [🗺️ Roadmap](ROADMAP.md)

</div>

---

> 🧭 **Estado del programa.** **Programa completo: las 176 clases en 12 partes están construidas** — de pensamiento computacional, el Atlas de familias y los toolchains a valores, control, funciones, datos, paradigmas, runtime, ingeniería, interoperabilidad y un proyecto integrador políglota. Cada clase de código trae sus **10 implementaciones del núcleo verificadas en CI** contra su `casos.json`; las partes 0, 1 y 2 son clases de método (pensar y comparar). Las Partes 0–2 no llevan implementaciones (son conceptuales); las Partes 3–11 sí.
>
> **Qué verifica una máquina y qué no**, para que sepas de qué te fías: el **[verificador de equivalencia](scripts/verificar_equivalencia.py)** ejecuta en CI las implementaciones de cada clase construida contra su `casos.json` y comprueba que **todas producen la misma salida**. El texto de las clases y el Atlas son material de lectura escrito a mano: **no** se ejecutan en CI. Si el badge de CI está verde, lo que garantiza es que las implementaciones equivalentes lo son de verdad.

## 🎯 Qué es esto

Un currículo modular y **secuencial** que enseña **los conocimientos transferibles de la programación**: no diez cursos aislados, sino cada concepto (una variable, un bucle, una función, un tipo) mostrado una vez y luego **comparado** entre lenguajes. La pregunta que responde cada clase no es "¿cómo se escribe en X?", sino **"¿qué permanece y qué cambia — y por qué — al pasar de un lenguaje a otro?"**.

Cada clase es una carpeta con un `README.md` que incluye:

- 🎯 **Objetivo** y **resultados de aprendizaje verificables**.
- 🗺️ **Temas** con el porqué de cada uno · 📖 **Definiciones**.
- 🧮 **Modelo** (entradas/salidas/reglas) y 📐 **algoritmo en pseudocódigo neutral**.
- 🌐 **Implementaciones idiomáticas** en el núcleo de 10 lenguajes.
- 🔬 **Comparación** (sintáctica · semántica · paradigmática) y 🧬 **el concepto en la familia**.
- ✅ **Prueba común** (`casos.json`) · 🧪 **reto de transferencia** · ⚠️ **errores comunes** · ❓ **FAQ**.

## 🧩 Núcleo y Atlas: dos capas

| Capa | Qué es | Lenguajes |
|---|---|---|
| **Núcleo** | Se implementa y **se verifica en CI** | Python, JavaScript, TypeScript, Java, C#, Go, Rust, C, SQL, **PHP** |
| **Atlas** | Se **comprende por características** (historia, paradigma, toolchain, primos) | ~40 familias: Ruby, Kotlin, Haskell, Elixir, Lisp, Prolog, Bash, Zig, Lua… |

La idea: **aprende el representante, reconoce la familia entera.** Si dominas C, ya lees el 80 % de la sintaxis de Java, C#, JS, Go y PHP. El **[Atlas](atlas/README.md)** cubre esa amplitud sin multiplicar el mantenimiento.

## 🧪 El verificador de equivalencia

El diferenciador de este programa: cada clase define un `casos.json` (entradas y salidas comunes), y el verificador ejecuta **todas** las implementaciones alimentándolas por stdin para comprobar que **coinciden**. No es teoría: es equivalencia demostrada por máquina.

```bash
python scripts/verificar_equivalencia.py 041      # una clase
python scripts/verificar_equivalencia.py --all     # todas las construidas
```

Los lenguajes cuyo toolchain no esté instalado se **omiten** e informan (degradación silenciosa); SQL, al ser declarativo, se marca como *ilustrativo*.

## 🧭 Portal

- 🧭 **[Rutas por perfil](rutas/README.md)** — "vengo de Python", "quiero sistemas (C/Rust)", "web (JS/TS)", "backend (Java/C#/Go)", "datos (SQL)".
- 🌐 **[Atlas de lenguajes](atlas/README.md)** — genealogía, historia, características y toolchain de cada familia.
- 📝 **[Autoevaluaciones](autoevaluaciones/README.md)** — una batería por parte.
- 📖 **[Glosario](glosario/README.md)** — términos enlazados a la clase donde se explican.

## 🗂️ Estructura del repositorio

```text
classes/
  _manifest.json          # fuente de verdad (176 clases)
  README.md               # índice completo
  parte-N-.../
    README.md             # README de la parte
    NNN-.../
      README.md           # la clase
      concepto.md comparacion.md reto.md casos.json
      implementaciones/<lenguaje>/...
atlas/        rutas/        autoevaluaciones/     glosario/
scripts/      docs/         .github/workflows/
```

## 📖 Cómo estudiar

```text
problema → concepto → pseudocódigo → implementaciones → comparación → transferencia
```

Empieza por la [Parte 0](classes/parte-0-pensamiento-computacional-y-el-metodo-poliglota/README.md) y sigue el orden: la numeración es global y cada clase asume la anterior. Consulta el [currículo](docs/CURRICULO.md), la [metodología](docs/METODOLOGIA.md) y la [guía para ampliar lenguajes](docs/EXTENDER.md).

## Principios

- Comparar conceptos, no solo sintaxis.
- Mantener el mismo problema, datos de prueba y resultado esperado en todos los lenguajes.
- Explicar diferencias reales sin declarar que todos los lenguajes son iguales.
- Distinguir siempre lo que verifica la máquina de lo que es material de lectura.
- Crecer por conceptos, no por cursos aislados.
- Usar `pnpm` en todo componente JavaScript/TypeScript que requiera paquetes.

## Licencia

MIT. Consulta [LICENSE](LICENSE).
