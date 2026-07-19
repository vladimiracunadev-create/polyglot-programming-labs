# Clase 037 — Formateadores y linters: black, prettier, gofmt, rustfmt, clang-format, php-cs-fixer

> Parte **2 — Herramientas, toolchains y anatomía de comandos** · ⏱️ Duración estimada: **75 min** · Nivel: **Fundamentos**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

Conocer dos herramientas que elevan la calidad sin esfuerzo manual: el formateador, que reescribe el código con un estilo consistente, y el linter, que detecta problemas y malas prácticas. Automatizan la legibilidad e idiomática que estudiaste en la Parte 0, y evitan discusiones de estilo en los equipos.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Distinguir formateador de linter.
2. Nombrar el formateador de cada lenguaje del núcleo.
3. Explicar por qué automatizar el estilo mejora el trabajo en equipo.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Formateador | Reescribe el código con un estilo único |
| 2 | Linter | Detecta errores probables y malas prácticas |
| 3 | Herramientas por lenguaje | black, prettier, gofmt, rustfmt, clippy… |
| 4 | Integración | En el editor y en el CI |

## 📖 Definiciones y características

- **Formateador** — herramienta que reescribe el código con un estilo consistente (black, gofmt). Clave: elimina las discusiones de formato.
- **Linter** — analiza el código en busca de errores probables y anti-patrones (clippy, ESLint). Clave: previene bugs antes de ejecutar.
- **Estilo consistente** — que todo el código luzca igual sin importar quién lo escribió. Clave: facilita leer y revisar.
- **gofmt** — formateador oficial de Go; no admite configuración. Clave: un solo estilo para toda la comunidad Go.

## 🧩 Situación

En una revisión de código, medio equipo discute si usar 2 o 4 espacios. Con un formateador (gofmt, black) la pregunta desaparece: la herramienta decide y todos aceptan. La energía se dedica a la lógica, no al formato.

## 🔎 Ejemplo

Formateador y linter por lenguaje:

```text
Python   black (formato)      + ruff/flake8 (lint)
JS/TS    prettier             + eslint
Go       gofmt                + go vet
Rust     rustfmt              + clippy
C/C++    clang-format
PHP      php-cs-fixer
```

## ✍️ Práctica

Si tienes uno instalado, pasa un formateador por un archivo desordenado y observa el 'antes y después'. ¿Qué reglas aplicó?

## ⚠️ Errores comunes

- **Formatear a mano** → causa: perder tiempo y ser inconsistente → solución: delegar el formato al formateador, integrado en el editor
- **Ignorar los avisos del linter** → causa: dejar pasar bugs latentes → solución: tratar los avisos como pistas y resolverlos o justificarlos

## ❓ Preguntas frecuentes

- **¿Formateador y linter son lo mismo?** No: el formateador cambia el aspecto; el linter señala problemas de fondo. Se usan juntos.
- **¿gofmt se puede configurar?** No, a propósito: Go impone un único estilo para toda la comunidad.

## 🔗 Referencias

- W. Shotts — *The Linux Command Line* (2ª ed., No Starch Press) — [gratis online](https://linuxcommand.org/tlcl.php).
- B. W. Kernighan y R. Pike — *The Unix Programming Environment* (Prentice Hall).
- A. Hunt y D. Thomas — *The Pragmatic Programmer* (2ª ed., Addison-Wesley).

---

> [⏮️ Clase 036](../../parte-2-herramientas-toolchains-y-anatomia-de-comandos/036-repl-e-interpretes-interactivos-por-lenguaje/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 038 ⏭️](../../parte-2-herramientas-toolchains-y-anatomia-de-comandos/038-pruebas-desde-la-terminal-pytest-node-test-go-test-cargo-test-dotnet-test-phpunit/README.md)
