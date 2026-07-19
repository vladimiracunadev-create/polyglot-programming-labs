# Clase 032 — Instalación y gestión de versiones (pyenv, nvm, rustup, SDKMAN, phpenv)

> Parte **2 — Herramientas, toolchains y anatomía de comandos** · ⏱️ Duración estimada: **75 min** · Nivel: **Fundamentos**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

Instalar un lenguaje parece trivial —bajas un instalador y listo— hasta el día en que dos proyectos exigen versiones distintas del mismo lenguaje en la misma máquina. Uno necesita Node 16 porque una dependencia no soporta más; otro exige Node 22 por una característica nueva. Instalar globalmente uno rompe el otro, y empieza el sufrimiento de desinstalar y reinstalar. El objetivo de esta clase es que aprendas a instalar cada lenguaje del núcleo con su **gestor de versiones** —pyenv, nvm, rustup, SDKMAN, phpenv— y que sepas fijar qué versión usa cada proyecto de forma aislada y reproducible, de modo que varias versiones convivan sin chocar.

Esto conecta con un principio central de *The Pragmatic Programmer*: la reproducibilidad. Un proyecto que «funciona» solo con la versión exacta que tú tienes instalada por casualidad es frágil. Declarar la versión, y que la herramienta la respete automáticamente, convierte «funciona en mi máquina» en «funciona en cualquier máquina que lea la declaración».

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Instalar un lenguaje del núcleo con su gestor de versiones recomendado.
2. Fijar la versión global y la versión por proyecto, y explicar la diferencia.
3. Reconocer el archivo de declaración de versión de cada ecosistema (`.python-version`, `.nvmrc`, etc.).
4. Explicar por qué un gestor de versiones evita conflictos y editar el `PATH` a mano no.

## 🧩 Situación

Heredas un proyecto de hace tres años. Lo clonas, ejecutas la instalación de dependencias y falla con errores incomprensibles. El problema no es tu código: el proyecto se escribió para Python 3.8 y tú tienes 3.12, donde algo cambió. Sin gestor de versiones, tu única salida es desinstalar tu Python y poner el 3.8, rompiendo de paso todos tus otros proyectos. Con pyenv, la solución es una línea: `pyenv install 3.8.18` y `pyenv local 3.8.18` dentro de la carpeta del proyecto. Ahora esa carpeta usa 3.8 y el resto de tu sistema sigue con 3.12, sin conflicto. Ese es exactamente el problema que los gestores de versiones existen para resolver, y por qué son de las primeras herramientas que instala un profesional.

## 📖 Qué hace realmente un gestor de versiones

Un gestor de versiones instala múltiples versiones de un lenguaje en carpetas separadas y coloca un *shim* —un pequeño intermediario— al frente de tu `PATH`. Cuando escribes `python`, el sistema encuentra primero ese shim, que decide en el momento qué versión real invocar según el contexto: la declarada en la carpeta actual, o la global si no hay ninguna. Por eso editar el `PATH` a mano es tan frágil y un gestor no: el gestor centraliza esa decisión en un solo lugar y la cambia sin que tú toques nada.

La distinción clave es entre **versión global** y **versión por proyecto**. La global es la que usas por defecto en cualquier carpeta sin configuración especial. La versión por proyecto se declara con un archivo pequeño que vive *junto al código* y se versiona con él: `pyenv` lee `.python-version`, `nvm` lee `.nvmrc`, `rustup` lee `rust-toolchain.toml`, `SDKMAN` lee `.sdkmanrc`. Ese archivo es la parte que hace reproducible el entorno: quien clona el proyecto obtiene, automáticamente, la versión correcta. Es la misma idea que un manifiesto de dependencias (clase 035), aplicada al lenguaje mismo.

Cada ecosistema tiene su gestor de referencia, con vocabulario propio pero la misma lógica. `rustup` es peculiar porque es el instalador *oficial* de Rust y gestiona no solo versiones sino *toolchains* completas (stable, beta, nightly) y componentes (clippy, rustfmt). `SDKMAN` cubre todo el ecosistema JVM: no solo distintos JDK, sino también Gradle, Maven o Kotlin. Go y C son las excepciones notables: Go se instala normalmente desde su web o el gestor del sistema (aunque desde la versión 1.21 el propio `go` puede descargar la toolchain que declara el `go.mod`), y C depende del compilador del sistema (gcc/clang vía el gestor de paquetes del SO), sin un gestor de versiones al estilo pyenv.

## 🔬 Laboratorio guiado: instalar y fijar versiones

Cada gestor sigue el mismo ritmo: instalar una versión, elegir la global, fijar la del proyecto. Compara los comandos lado a lado:

```bash
# Python con pyenv
pyenv install 3.12.4        # descarga y compila esa versión
pyenv global 3.12.4         # versión por defecto del sistema
pyenv local 3.8.18          # crea .python-version en esta carpeta -> solo aquí usa 3.8.18
python --version            # verifica qué versión resuelve el shim
```

```bash
# Node con nvm
nvm install 22              # instala Node 22
nvm install 16              # y también Node 16
nvm use 16                  # cambia la sesión actual a 16
nvm alias default 22        # 22 como global por defecto
node --version              # comprueba
```

```bash
# Rust con rustup
rustup default stable       # toolchain estable como global
rustup toolchain install nightly   # añade la nightly
rustup override set nightly # esta carpeta usa nightly
rustc --version
```

```bash
# Java / JVM con SDKMAN
sdk install java 21-tem     # instala Temurin JDK 21
sdk install java 17-tem     # y el 17
sdk use java 17.0.11-tem    # cambia la sesión actual
java -version
```

```bash
# PHP con phpenv
phpenv install 8.3.6
phpenv global 8.3.6
phpenv local 8.2.19         # .php-version en esta carpeta
php --version
```

El patrón es idéntico en los cinco: `install` trae una versión, `global`/`default` la fija para todo, `local`/`use`/`override` la fija para la carpeta o la sesión. Aprendido el ritmo en uno, los demás son variaciones del mismo tema. Verifica siempre con `--version`, que es el comando universal para preguntar «¿qué versión estoy usando de verdad?».

## ✍️ Práctica

Averigua qué versión de un lenguaje del núcleo tienes ahora mismo con `--version` (por ejemplo `python --version`, `node --version`). Después instala su gestor de versiones recomendado si no lo tienes y usa el laboratorio de arriba para instalar una *segunda* versión distinta. Crea una carpeta de prueba, entra en ella y fija ahí la versión antigua con el comando `local`/`override`: comprueba con `--version` que dentro de la carpeta se usa una versión y fuera otra. Abre el archivo de declaración que se creó (`.python-version`, `.nvmrc`…) y verifica que es texto plano con el número de versión: ese es el archivo que harías commit para que tu equipo use la misma versión que tú.

## ⚠️ Errores comunes

| Síntoma / mensaje | Causa y cómo arreglar |
|-------------------|-----------------------|
| Un proyecto viejo falla con errores raros de sintaxis o API | Versión del lenguaje incorrecta. Fija la que exige el proyecto con `local`/`override` |
| Instalar una versión global rompe otro proyecto | No usar un gestor. Instala por versión y declara la de cada proyecto |
| `command not found` tras instalar el gestor | Falta inicializarlo en el shell. Añade la línea de `init` a tu `.bashrc`/`.zshrc` y reabre la terminal |
| Editar el `PATH` a mano para cambiar de versión | Frágil e irreproducible. Deja que el gestor administre las rutas vía shims |
| El equipo usa versiones distintas sin saberlo | Falta versionar el archivo de declaración. Haz commit de `.nvmrc`/`.python-version` |

## ❓ Preguntas frecuentes

- **¿Necesito un gestor si solo tengo un proyecto?** Aún así conviene: el día que llegue el segundo proyecto o clones código ajeno, ya estarás preparado y no tendrás que migrar tu instalación global.
- **¿Docker no resuelve esto?** También aísla versiones, pero a otro nivel (todo el sistema operativo del contenedor). Se complementan: el gestor para desarrollar cómodo en local, el contenedor para desplegar. La clase 039 lo retoma.
- **¿Por qué Go y C no tienen un pyenv?** Go gestiona su propia toolchain desde el `go.mod` y suele instalarse una sola versión; C depende del compilador del sistema. Su cultura no gira en torno a alternar versiones del lenguaje como en Python o Node.
- **¿El gestor descarga binarios o compila?** Depende: `nvm` y `SDKMAN` bajan binarios; `pyenv` suele compilar desde el fuente (por eso tarda más y necesita herramientas de compilación instaladas).

## 🔗 Referencias

- W. Shotts — *The Linux Command Line* (2ª ed., No Starch Press), sobre el entorno y el `PATH` — [gratis online](https://linuxcommand.org/tlcl.php).
- B. W. Kernighan y R. Pike — *The Unix Programming Environment* (Prentice Hall).
- A. Hunt y D. Thomas — *The Pragmatic Programmer* (2ª ed., Addison-Wesley), sobre reproducibilidad y entornos de trabajo.

---

> [⏮️ Clase 031](../../parte-2-herramientas-toolchains-y-anatomia-de-comandos/031-anatomia-de-un-comando-nombre-subcomando-flags-argumentos-y-esquema/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 033 ⏭️](../../parte-2-herramientas-toolchains-y-anatomia-de-comandos/033-ejecutar-python-node-tsx-java-dotnet-go-run-rustc-cc-php-sqlite3/README.md)
