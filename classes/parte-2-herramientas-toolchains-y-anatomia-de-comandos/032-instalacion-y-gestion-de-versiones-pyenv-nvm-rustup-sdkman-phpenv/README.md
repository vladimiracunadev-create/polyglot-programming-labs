# Clase 032 — Instalación y gestión de versiones (pyenv, nvm, rustup, SDKMAN, phpenv)

> Parte **2 — Herramientas, toolchains y anatomía de comandos** · ⏱️ Duración estimada: **75 min** · Nivel: **Fundamentos**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

Aprender a instalar cada lenguaje y, sobre todo, a manejar varias versiones en la misma máquina. Distintos proyectos necesitan distintas versiones; los gestores de versiones (pyenv, nvm, rustup, SDKMAN) permiten cambiar entre ellas sin conflictos. Es la base para no 'romper' tu entorno.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Instalar un lenguaje del núcleo con su gestor recomendado.
2. Cambiar entre versiones por proyecto.
3. Explicar por qué un gestor de versiones evita conflictos.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | El problema de las versiones | Proyectos que exigen versiones distintas |
| 2 | Gestores por lenguaje | pyenv, nvm, rustup, SDKMAN, phpenv |
| 3 | Versión global vs. por proyecto | Fijar la versión donde corresponde |
| 4 | Entornos aislados | Que un proyecto no afecte a otro |

## 📖 Definiciones y características

- **Gestor de versiones** — herramienta que instala y alterna versiones de un lenguaje (pyenv, nvm). Clave: varias versiones conviven sin chocar.
- **Versión por proyecto** — fijar qué versión usa una carpeta concreta (.python-version, .nvmrc). Clave: reproducibilidad entre máquinas.
- **rustup** — instalador y gestor oficial de Rust (toolchains, componentes). Clave: estándar de facto de la comunidad Rust.
- **SDKMAN** — gestor de versiones para el ecosistema JVM (Java, Kotlin, Gradle). Clave: cambia de JDK con un comando.

## 🧩 Situación

Un proyecto viejo necesita Node 16 y uno nuevo Node 22. Sin gestor, instalar uno rompe el otro. Con nvm, `nvm use 16` y `nvm use 22` conviven sin drama. Ese es el problema que resuelven los gestores.

## 🔎 Ejemplo

Cada ecosistema tiene su gestor:

```text
Python:  pyenv install 3.12.4   ; pyenv local 3.12.4
Node:    nvm install 22        ; nvm use 22
Rust:    rustup default stable
Java:    sdk install java 21-tem
PHP:     phpenv install 8.3
```

## ✍️ Práctica

Comprueba qué versión de un lenguaje tienes instalada (`python --version`, `node --version`). Averigua cómo fijarías una versión distinta solo para un proyecto.

## ⚠️ Errores comunes

- **Instalar una sola versión global para todo** → causa: romper proyectos que exigen otra → solución: usar un gestor y fijar la versión por proyecto
- **Editar el PATH a mano sin control** → causa: entorno frágil e irreproducible → solución: dejar que el gestor de versiones administre las rutas

## ❓ Preguntas frecuentes

- **¿Necesito un gestor si solo tengo un proyecto?** Aún así ayuda: cuando llegue el segundo proyecto, ya estarás preparado.
- **¿Docker no resuelve esto?** También aísla versiones, a otro nivel (todo el sistema). Se complementan.

## 🔗 Referencias

- W. Shotts — *The Linux Command Line* (2ª ed., No Starch Press) — [gratis online](https://linuxcommand.org/tlcl.php).
- B. W. Kernighan y R. Pike — *The Unix Programming Environment* (Prentice Hall).
- A. Hunt y D. Thomas — *The Pragmatic Programmer* (2ª ed., Addison-Wesley).

---

> [⏮️ Clase 031](../../parte-2-herramientas-toolchains-y-anatomia-de-comandos/031-anatomia-de-un-comando-nombre-subcomando-flags-argumentos-y-esquema/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 033 ⏭️](../../parte-2-herramientas-toolchains-y-anatomia-de-comandos/033-ejecutar-python-node-tsx-java-dotnet-go-run-rustc-cc-php-sqlite3/README.md)
