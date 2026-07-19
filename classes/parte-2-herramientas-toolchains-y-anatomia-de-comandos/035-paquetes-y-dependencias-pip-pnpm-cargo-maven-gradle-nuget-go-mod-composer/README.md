# Clase 035 — Paquetes y dependencias: pip, pnpm, cargo, maven/gradle, nuget, go mod, composer

> Parte **2 — Herramientas, toolchains y anatomía de comandos** · ⏱️ Duración estimada: **75 min** · Nivel: **Fundamentos**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

Entender cómo cada lenguaje reutiliza código de terceros mediante un gestor de paquetes y un archivo de manifiesto que declara las dependencias. Nadie escribe todo desde cero: pip, pnpm, cargo, composer y sus primos descargan, versionan y bloquean librerías para que tu proyecto sea reproducible.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Explicar qué es una dependencia y un gestor de paquetes.
2. Identificar el manifiesto y el lockfile de cada lenguaje del núcleo.
3. Entender por qué el lockfile garantiza builds reproducibles.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Dependencias | Código de terceros que tu proyecto reutiliza |
| 2 | Manifiesto | Declara qué dependencias y qué versiones |
| 3 | Lockfile | Fija las versiones exactas para reproducibilidad |
| 4 | Repositorios de paquetes | PyPI, npm, crates.io, Packagist… |

## 📖 Definiciones y características

- **Gestor de paquetes** — herramienta que descarga e instala dependencias (pip, cargo, composer). Clave: automatiza reutilizar código ajeno.
- **Manifiesto** — archivo que declara las dependencias (pyproject.toml, package.json, Cargo.toml). Clave: la lista de lo que el proyecto necesita.
- **Lockfile** — archivo con las versiones exactas resueltas (package-lock.json, Cargo.lock). Clave: mismo resultado en toda máquina.
- **Repositorio de paquetes** — servidor central de librerías (PyPI, npm, crates.io). Clave: de donde se descargan las dependencias.

## 🧩 Situación

Funciona en tu máquina pero falla en la del compañero: instalasteis versiones distintas de una librería. El lockfile resuelve exactamente esto, congelando las versiones para que ambos obtengáis lo mismo.

## 🔎 Ejemplo

Manifiesto y gestor por lenguaje:

```text
Python   pip / pyproject.toml      (repos: PyPI)
JS/TS    pnpm / package.json       (repos: npm)
Rust     cargo / Cargo.toml        (repos: crates.io)
Java     gradle o maven / pom.xml  (repos: Maven Central)
C#       nuget / .csproj           (repos: NuGet)
Go       go mod / go.mod           (repos: proxy de módulos)
PHP      composer / composer.json  (repos: Packagist)
```

## ✍️ Práctica

Abre un manifiesto (package.json, Cargo.toml o pyproject.toml) de cualquier proyecto. Localiza la lista de dependencias y su versión. ¿Hay un lockfile al lado?

## ⚠️ Errores comunes

- **No commitear el lockfile** → causa: builds distintos en cada máquina → solución: versionar el lockfile junto al manifiesto
- **Fijar versiones a '*' o 'latest'** → causa: roturas por actualizaciones inesperadas → solución: acotar rangos de versión y confiar en el lockfile

## ❓ Preguntas frecuentes

- **¿pnpm o npm?** Este curso usa pnpm en JS/TS por su eficiencia; el concepto (manifiesto + lockfile) es idéntico.
- **¿Go no tiene lockfile?** Usa go.mod y go.sum (este último fija los hashes exactos, cumpliendo el rol de lock).

## 🔗 Referencias

- W. Shotts — *The Linux Command Line* (2ª ed., No Starch Press) — [gratis online](https://linuxcommand.org/tlcl.php).
- B. W. Kernighan y R. Pike — *The Unix Programming Environment* (Prentice Hall).
- A. Hunt y D. Thomas — *The Pragmatic Programmer* (2ª ed., Addison-Wesley).

---

> [⏮️ Clase 034](../../parte-2-herramientas-toolchains-y-anatomia-de-comandos/034-compilar-y-construir-gcc-clang-cargo-go-build-javac-dotnet-build/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 036 ⏭️](../../parte-2-herramientas-toolchains-y-anatomia-de-comandos/036-repl-e-interpretes-interactivos-por-lenguaje/README.md)
