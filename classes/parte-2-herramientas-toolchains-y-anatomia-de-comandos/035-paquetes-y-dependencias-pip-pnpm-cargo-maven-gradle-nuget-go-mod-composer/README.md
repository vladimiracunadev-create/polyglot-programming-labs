# Clase 035 — Paquetes y dependencias: pip, pnpm, cargo, maven/gradle, nuget, go mod, composer

> Parte **2 — Herramientas, toolchains y anatomía de comandos** · ⏱️ Duración estimada: **75 min** · Nivel: **Fundamentos**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

Nadie escribe todo el software desde cero. Un proyecto moderno se apoya en decenas o cientos de bibliotecas de terceros: para parsear JSON, hablar HTTP, cifrar, dibujar. El objetivo de esta clase es que entiendas el mecanismo universal con el que cada lenguaje reutiliza ese código ajeno: un **gestor de paquetes** que descarga e instala dependencias, un archivo **manifiesto** donde declaras qué necesitas, y un **lockfile** que congela las versiones exactas para que tu proyecto sea reproducible en cualquier máquina. Cambian los nombres —pip, pnpm, cargo, composer— pero la trinidad manifiesto/lockfile/gestor es la misma en todos.

El concepto de reproducibilidad que introdujo *The Pragmatic Programmer* alcanza aquí su expresión más concreta. Un proyecto cuyas dependencias no están fijadas es una bomba de tiempo: funciona hoy y se rompe mañana cuando una biblioteca publique una versión nueva incompatible. El lockfile es la respuesta de ingeniería a ese problema, y entenderlo distingue al que sufre builds impredecibles del que los controla.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Explicar qué es una dependencia, un gestor de paquetes, un manifiesto y un lockfile.
2. Identificar el manifiesto y el lockfile de cada lenguaje del núcleo.
3. Añadir una dependencia con el comando del gestor de cada ecosistema.
4. Explicar por qué versionar el lockfile garantiza builds idénticos en todo el equipo.

## 🧩 Situación

Tu código funciona perfecto en tu máquina. Lo subes, tu compañero lo clona, instala las dependencias y falla con un error que tú nunca viste. La causa: tú tienes la versión 2.4 de una biblioteca y él, al instalar «la última», obtuvo la 2.5, que cambió un detalle. Ambos declarasteis «la versión 2.x», que es ambiguo. El lockfile resuelve exactamente esto: registra que se resolvió la 2.4.1 —el número exacto, hasta el parche— y, al haberlo versionado junto al código, tu compañero obtiene esa misma 2.4.1. El clásico «en mi máquina funciona» casi siempre nace de dependencias no fijadas, y la solución casi siempre es hacer commit del lockfile.

## 📖 Manifiesto, lockfile y gestor: la trinidad

El **manifiesto** es la lista de la compra: declara qué dependencias necesita tu proyecto y, normalmente, con qué rango de versiones aceptables. Es un archivo que tú editas y que expresa *intención*: `pyproject.toml` en Python, `package.json` en JS/TS, `Cargo.toml` en Rust, `go.mod` en Go, `composer.json` en PHP, el `.csproj` en C#, `pom.xml` o `build.gradle` en Java. Ahí escribes «quiero requests, versión 2.x o superior».

El **lockfile** es el recibo exacto de lo que se compró. Cuando el gestor resuelve tu manifiesto —eligiendo versiones concretas que satisfagan todos los rangos, incluidas las dependencias de tus dependencias— anota el resultado hasta el último dígito en un archivo que *no* editas a mano: `package-lock.json`/`pnpm-lock.yaml`, `Cargo.lock`, `poetry.lock`, `go.sum`, `composer.lock`. Este archivo es la clave de la reproducibilidad, y por eso la regla de oro es **versionar el lockfile junto al manifiesto**. El manifiesto dice qué quieres; el lockfile garantiza que todos obtengáis exactamente lo mismo.

El **gestor de paquetes** es la herramienta que lee el manifiesto, descarga las bibliotecas desde un **repositorio central** (PyPI para Python, npm para JS, crates.io para Rust, Packagist para PHP, Maven Central para Java, NuGet para C#) y escribe el lockfile. Su verbo típico es `install` o `add`: `pip install`, `pnpm add`, `cargo add`. Una precaución que Shotts y la cultura Unix inculcan —desconfiar de lo que traes de fuera— cobra aquí especial peso: cada dependencia es código de terceros que ejecutarás con tus permisos, así que conviene fijar versiones, revisar el lockfile y no depender de `latest`, que es un blanco móvil.

## 🔬 Laboratorio guiado: declarar y bloquear dependencias

Compara cómo cada ecosistema añade una dependencia y qué archivos toca. El patrón se repite: un comando que actualiza el manifiesto y regenera el lockfile.

```bash
# Python (pip + pyproject.toml, o el clásico requirements.txt)
pip install requests                 # instala y puedes fijar en requirements.txt
pip freeze > requirements.txt        # congela las versiones exactas instaladas

# JavaScript / TypeScript (pnpm + package.json -> pnpm-lock.yaml)
pnpm add zod                         # añade al package.json y actualiza el lockfile
pnpm install                         # instala exactamente lo del lockfile

# Rust (cargo + Cargo.toml -> Cargo.lock)
cargo add serde                      # edita Cargo.toml y resuelve Cargo.lock
cargo build                          # descarga y compila las dependencias

# Go (go mod + go.mod -> go.sum)
go get github.com/google/uuid        # añade al go.mod y fija hashes en go.sum

# Java (Maven: pom.xml / Gradle: build.gradle)
mvn dependency:resolve               # resuelve lo declarado en pom.xml

# C# (.NET + .csproj)
dotnet add package Newtonsoft.Json   # añade al .csproj y restaura

# PHP (composer + composer.json -> composer.lock)
composer require guzzlehttp/guzzle   # añade y escribe composer.lock
```

Mapa de la trinidad por lenguaje, para tenerlo a mano:

```text
Lenguaje   Gestor       Manifiesto        Lockfile              Repositorio
--------   ----------   ---------------   -------------------   --------------
Python     pip          pyproject.toml    poetry.lock*          PyPI
JS / TS    pnpm         package.json      pnpm-lock.yaml        npm
Rust       cargo        Cargo.toml        Cargo.lock            crates.io
Go         go mod       go.mod            go.sum                proxy de módulos
Java       maven/gradle pom.xml           (gradle.lockfile)     Maven Central
C#         nuget        proyecto.csproj   packages.lock.json    NuGet
PHP        composer     composer.json     composer.lock         Packagist
```

*El lockfile de Python depende de la herramienta (poetry, pip-tools); con pip clásico se usa `requirements.txt` con versiones fijadas.

Verifica la reproducibilidad tú mismo: abre cualquier lockfile con un editor y localiza una dependencia. Verás su versión exacta y, a menudo, un hash criptográfico que garantiza que descargaste ese contenido y no otro suplantado.

## ✍️ Práctica

Abre un manifiesto real de cualquier proyecto que tengas a mano (`package.json`, `Cargo.toml` o `pyproject.toml`) y localiza la lista de dependencias con sus versiones. Fíjate en la sintaxis de los rangos: un `^2.4.0` o un `~1.2` no es lo mismo que `2.4.1` fijo. Luego busca el lockfile al lado (`pnpm-lock.yaml`, `Cargo.lock`…), ábrelo y encuentra esa misma dependencia: comprueba que aquí la versión es un número exacto, sin rangos. Si tienes un ecosistema instalado, crea un proyecto de prueba y añade una dependencia con su comando (`cargo add`, `pnpm add`, `composer require`): observa cómo el manifiesto gana una línea y el lockfile aparece o crece. Comprueba con `git status` que ambos archivos han cambiado y que ambos deberían ir al commit.

## ⚠️ Errores comunes

| Síntoma / mensaje | Causa y cómo arreglar |
|-------------------|-----------------------|
| «En mi máquina funciona» pero en la de otro no | Dependencias no fijadas. Versiona el lockfile para que todos resuelvan lo mismo |
| No commitear el lockfile | Cada máquina resuelve versiones distintas. Añádelo a git junto al manifiesto |
| Fijar dependencias a `*` o `latest` | Roturas por actualizaciones inesperadas. Acota rangos y confía en el lockfile |
| Editar el lockfile a mano | Es generado; se corrompe fácil. Cámbialo solo vía el gestor (`add`, `update`) |
| Versionar la carpeta de dependencias (`node_modules`, `target`) | Es pesada y regenerable. Ignórala; el lockfile basta para reconstruirla |

## ❓ Preguntas frecuentes

- **¿pnpm o npm?** Este curso usa pnpm en JS/TS por su eficiencia en disco y velocidad, pero el concepto —manifiesto `package.json` más lockfile— es idéntico. Lo que aprendes se transfiere a npm y yarn sin cambios.
- **¿Go no tiene lockfile?** Lo tiene repartido: `go.mod` declara y `go.sum` fija los hashes exactos de cada módulo, cumpliendo el papel de bloqueo e integridad. Juntos garantizan builds reproducibles.
- **¿Qué diferencia hay entre manifiesto y lockfile?** El manifiesto expresa intención con rangos (lo editas tú); el lockfile registra el resultado exacto de resolver esos rangos (lo genera el gestor). Uno dice «quiero 2.x», el otro «se instaló la 2.4.1».
- **¿Es seguro instalar cualquier paquete?** Cada dependencia es código que ejecutarás. Prefiere paquetes mantenidos, revisa el lockfile y desconfía de nombres sospechosamente parecidos a los populares (typosquatting). La confianza no es automática.

## 🔗 Referencias

- W. Shotts — *The Linux Command Line* (2ª ed., No Starch Press) — [gratis online](https://linuxcommand.org/tlcl.php).
- B. W. Kernighan y R. Pike — *The Unix Programming Environment* (Prentice Hall).
- A. Hunt y D. Thomas — *The Pragmatic Programmer* (2ª ed., Addison-Wesley), sobre control de versiones y reproducibilidad del entorno.

---

> [⏮️ Clase 034](../../parte-2-herramientas-toolchains-y-anatomia-de-comandos/034-compilar-y-construir-gcc-clang-cargo-go-build-javac-dotnet-build/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 036 ⏭️](../../parte-2-herramientas-toolchains-y-anatomia-de-comandos/036-repl-e-interpretes-interactivos-por-lenguaje/README.md)
