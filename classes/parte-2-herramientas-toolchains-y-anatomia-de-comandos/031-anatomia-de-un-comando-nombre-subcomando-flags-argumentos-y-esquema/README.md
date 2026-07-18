# Clase 031 — Anatomía de un comando: nombre, subcomando, flags, argumentos y esquema

> Parte **2 — Herramientas, toolchains y anatomía de comandos** · ⏱️ Duración estimada: **75 min** · Nivel: **Fundamentos**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

Dominar la estructura universal de un comando de terminal para dejar de copiarlos a ciegas. Todo comando sigue el mismo esquema: nombre, subcomando opcional, opciones (flags) y argumentos. Entenderlo te permite leer, modificar y componer cualquier comando de cualquier toolchain.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Descomponer un comando en nombre, subcomando, flags y argumentos.
2. Distinguir flags cortas (-v), largas (--verbose) y con valor (-o salida).
3. Leer la línea de uso ('usage') de la ayuda de un comando.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | El esquema general | nombre [subcomando] [flags] [argumentos] |
| 2 | Flags/opciones | Cortas, largas, booleanas y con valor |
| 3 | Argumentos posicionales | Los datos sobre los que actúa el comando |
| 4 | La ayuda como esquema | --help revela la estructura exacta |

## 📖 Definiciones y características

- **Comando** — instrucción para el sistema o una herramienta, escrita en la terminal. Clave: sigue un esquema regular.
- **Subcomando** — acción específica dentro de una herramienta (git commit, dotnet build). Clave: agrupa funciones bajo un mismo programa.
- **Flag/opción** — modificador que cambia el comportamiento (-v, --output). Clave: puede ser booleana o llevar un valor.
- **Argumento posicional** — dato cuyo significado depende de su posición. Clave: distinto de las opciones con nombre.

## 🧩 Situación

Alguien copia `git commit -m "fix"` sin entenderlo y luego no sabe adaptarlo. Quien reconoce el esquema —programa `git`, subcomando `commit`, flag `-m` con valor— puede construir sus propios comandos con confianza.

## 🔎 Ejemplo

El mismo esquema en varias herramientas:

```text
  git      commit     -m "mensaje"        (sin argumento posicional)
  \_/      \____/     \_______________/
 nombre  subcomando   flag con valor

  cc       main.c     -o main            (compilar C)
  docker   run        -it   ubuntu bash
  dotnet   build      -c Release
```

## ✍️ Práctica

Toma `rustc main.rs -o main` y etiqueta cada parte (nombre, argumento, flag, valor). Luego busca `git --help` y localiza el 'usage'.

## ⚠️ Errores comunes

- **Copiar comandos sin entender sus partes** → causa: no poder adaptarlos → solución: descomponer siempre en nombre/subcomando/flags/argumentos
- **Confundir un argumento con una flag** → causa: errores de sintaxis del comando → solución: recordar que las flags empiezan por - o --

## ❓ Preguntas frecuentes

- **¿Por qué unas flags llevan un guion y otras dos?** Convención: un guion para la forma corta (-v), dos para la larga (--verbose).
- **¿Cómo sé qué acepta un comando?** Con `comando --help` o `man comando`: muestran el esquema y todas las opciones.

## 🔗 Referencias

- Documentación de referencia de cada lenguaje del núcleo.

---

> [⏮️ Clase 030](../../parte-2-herramientas-toolchains-y-anatomia-de-comandos/030-compilado-vs-interpretado-vs-transpilado-vs-bytecode-vm/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 032 ⏭️](../../parte-2-herramientas-toolchains-y-anatomia-de-comandos/032-instalacion-y-gestion-de-versiones-pyenv-nvm-rustup-sdkman-phpenv/README.md)
