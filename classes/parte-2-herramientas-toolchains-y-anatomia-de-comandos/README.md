# Parte 2 — Herramientas, toolchains y anatomía de comandos

> [⏮️ Parte 1](../parte-1-atlas-y-genealogia-de-los-lenguajes/README.md) · [⬅️ Programa](../../README.md) · [📚 Índice](../README.md) · [⏭️ Parte 3](../parte-3-valores-tipos-y-variables/README.md)

**12 clases** · rango 029–040 · clases de **método** · nivel fundamentos · **~18 h** ([cronograma](../../docs/syllabus.md))

> 🧭 **Del archivo de texto al proceso que corre: el toolchain de cada lenguaje.**

---

## 🧭 De qué trata esta parte

El código fuente es un archivo de texto que no hace nada por sí mismo. Entre ese texto y un proceso vivo hay una cadena de herramientas —el **toolchain**— que casi nadie enseña y que todo el mundo necesita: instalar, ejecutar, compilar, gestionar dependencias, formatear, probar y empaquetar.

Esta parte es deliberadamente práctica y transversal: cubre los diez lenguajes del núcleo a la vez, mostrando que bajo diez vocabularios distintos hay unos pocos conceptos idénticos. `pip`, `cargo`, `pnpm`, Maven y Composer hacen lo mismo con nombres distintos; entender el patrón ahorra volver a aprender desde cero en cada lenguaje.

Es también la parte que hace ejecutable el resto del curso: aquí se instala y comprueba lo necesario para que el verificador de equivalencia pueda correr en tu máquina y no solo en CI.

## 🎒 Qué necesitas traer

Las Partes 0 y 1. Conviene tener acceso a una terminal y permisos para instalar software; sin ello, varias clases se quedan en lectura.

## 🎯 Qué sabrás hacer al terminar

Resultados comprobables: si no puedes hacerlos, la parte no está cerrada.

1. Nombrar cada eslabón entre tu archivo fuente y el proceso en ejecución.
2. Leer un comando desconocido descomponiéndolo en nombre, subcomando, flags y argumentos.
3. Instalar y convivir con varias versiones del mismo lenguaje en una máquina.
4. Ejecutar, construir, probar y empaquetar en cualquiera de los diez lenguajes del núcleo.
5. Diagnosticar el clásico «en mi máquina sí funciona» mirando PATH y variables de entorno.

## 🗺️ El recorrido, clase a clase

Las clases están agrupadas en bloques por la razón que las une. El orden es secuencial: cada una asume la anterior.

### 🔹 Qué hay entre tu texto y un proceso · clases 029–031

El toolchain, los cuatro modelos de ejecución y la gramática de un comando.

- **[029 · Qué es un toolchain: del código fuente al programa que corre](029-que-es-un-toolchain-del-codigo-fuente-al-programa-que-corre/README.md)** — Entre el archivo de texto que escribes y un proceso vivo consumiendo CPU hay una cadena de herramientas. Nombrar cada eslabón —preprocesador, compilador, enlazador, cargador, intérprete— es lo que convierte un error de build en un problema localizable.
- **[030 · Compilado vs. interpretado vs. transpilado vs. bytecode/VM](030-compilado-vs-interpretado-vs-transpilado-vs-bytecode-vm/README.md)** — «¿Es compilado o interpretado?» está casi siempre mal planteada: la realidad tiene cuatro respuestas —compilado a máquina, interpretado, transpilado y bytecode sobre VM— y muchos lenguajes usan varias a la vez. Aquí se corrige la dicotomía.
- **[031 · Anatomía de un comando: nombre, subcomando, flags, argumentos y esquema](031-anatomia-de-un-comando-nombre-subcomando-flags-argumentos-y-esquema/README.md)** — La línea de comandos parece un idioma secreto y es una gramática muy regular: nombre, subcomando, flags, argumentos. Aprender el esquema permite leer un comando que nunca viste en lugar de copiarlo de un foro sin entenderlo.

### 🔹 Instalar y ejecutar · clases 032–033

Gestión de versiones y el comando de ejecución de cada lenguaje del núcleo.

- **[032 · Instalación y gestión de versiones (pyenv, nvm, rustup, SDKMAN, phpenv)](032-instalacion-y-gestion-de-versiones-pyenv-nvm-rustup-sdkman-phpenv/README.md)** — El día en que dos proyectos exigen versiones distintas del mismo lenguaje en la misma máquina, instalar deja de ser trivial. `pyenv`, `nvm`, `rustup`, SDKMAN y `phpenv` resuelven el mismo problema con la misma idea; aquí se ve el patrón común.
- **[033 · Ejecutar: python, node, tsx, java, dotnet, go run, rustc, cc, php, sqlite3](033-ejecutar-python-node-tsx-java-dotnet-go-run-rustc-cc-php-sqlite3/README.md)** — El comando de ejecución de cada lenguaje del núcleo, comprendido y no memorizado: qué hace realmente `python`, `node`, `java`, `dotnet`, `go run`, `rustc`, `cc`, `php` y `sqlite3` con tu archivo antes de que aparezca la primera línea de salida.

### 🔹 Construir, depender y explorar · clases 034–036

Artefactos, gestores de paquetes y la consola interactiva como herramienta de estudio.

- **[034 · Compilar y construir: gcc/clang, cargo, go build, javac, dotnet build](034-compilar-y-construir-gcc-clang-cargo-go-build-javac-dotnet-build/README.md)** — Ejecutar y **construir** se confunden con facilidad y sirven a momentos distintos: ejecutar es correrlo ahora; construir es producir un **artefacto** —binario, jar, wheel— que sobrevive a la sesión y viaja a otra máquina.
- **[035 · Paquetes y dependencias: pip, pnpm, cargo, maven/gradle, nuget, go mod, composer](035-paquetes-y-dependencias-pip-pnpm-cargo-maven-gradle-nuget-go-mod-composer/README.md)** — Nadie escribe todo el software desde cero. Aquí se ve el mecanismo universal detrás de `pip`, `pnpm`, `cargo`, Maven/Gradle, NuGet, `go mod` y Composer: manifiesto, resolución, lockfile y caché — el mismo esquema con siete vocabularios.
- **[036 · REPL e intérpretes interactivos por lenguaje](036-repl-e-interpretes-interactivos-por-lenguaje/README.md)** — El **REPL** convierte una duda en un experimento de tres segundos: escribir una expresión, pulsar Enter y ver el resultado sin crear archivo ni compilar. Es la herramienta de aprendizaje más infrautilizada de todas.

### 🔹 Calidad, empaquetado y entorno · clases 037–040

Formateadores, linters, pruebas desde terminal, distribución y PATH.

- **[037 · Formateadores y linters: black, prettier, gofmt, rustfmt, clang-format, php-cs-fixer](037-formateadores-y-linters-black-prettier-gofmt-rustfmt-clang-format-php-cs-fixer/README.md)** — El **formateador** elimina la discusión sobre la forma reescribiendo el código a una convención; el **linter** detecta construcciones sospechosas antes de ejecutarlas. Automatizan justo la legibilidad que la clase 010 defendió a mano.
- **[038 · Pruebas desde la terminal: pytest, node --test, go test, cargo test, dotnet test, phpunit](038-pruebas-desde-la-terminal-pytest-node-test-go-test-cargo-test-dotnet-test-phpunit/README.md)** — Ejecutar pruebas desde la terminal en cada lenguaje: `pytest`, `node --test`, `go test`, `cargo test`, `dotnet test`, PHPUnit. Cambia el comando; no cambia la idea de dar entradas conocidas y afirmar la salida esperada.
- **[039 · Empaquetado y distribución: wheels, jars, binarios, contenedores](039-empaquetado-y-distribucion-wheels-jars-binarios-contenedores/README.md)** — Un programa que funciona en tu máquina todavía no es un producto. El **empaquetado** —wheels, jars, binarios, contenedores— es el paso entre «compila aquí» y «otra persona lo ejecuta allá», y decide buena parte del éxito de un proyecto.
- **[040 · Variables de entorno, rutas y el PATH en Windows y Unix](040-variables-de-entorno-rutas-y-el-path-en-windows-y-unix/README.md)** — Cuando escribes `python` y pulsas Enter, el sistema no sabe dónde está Python: lo busca recorriendo el **PATH**. Entender esa lista, y las variables de entorno en general, explica la mitad de los «en mi máquina sí funciona».

## ⚠️ Los malentendidos que esta parte corrige

| Se suele creer | Lo que ocurre en realidad |
|---|---|
| «Python es interpretado y Java compilado.» | Ambos compilan a bytecode y lo ejecutan sobre una VM. La dicotomía compilado/interpretado tiene cuatro respuestas, no dos. |
| «Ejecutar y compilar son lo mismo con otro comando.» | Ejecutar es correrlo ahora; construir produce un artefacto que sobrevive a la sesión y viaja a otra máquina. |
| «El lockfile es un archivo generado que se puede borrar.» | Es la diferencia entre una build reproducible y una que depende del día en que se ejecute. |

## 🧪 Cómo estudiar esta parte

1. **Lee la clase entera antes de opinar.** Son clases de razonamiento: el valor está en el argumento completo, no en la definición suelta.
2. **Contesta la pregunta que abre cada clase** con tus palabras antes de seguir a la siguiente. Si no puedes, vuelve al párrafo del objetivo.
3. **Aplícalo a un problema tuyo.** Estas clases no se verifican con una máquina; se verifican usándolas sobre código real que ya escribiste.
4. **Anota los términos nuevos.** Aparecen otra vez, con código delante, a partir de la Parte 3 — y están todos en el [glosario](../../glosario/README.md).

## 📚 Fuentes de referencia de esta parte

Cada clase cita estos libros en su sección de referencias. No se reproduce su contenido: la redacción es original.

- W. Shotts — *The Linux Command Line* (2ª ed., No Starch Press) — [gratis online](https://linuxcommand.org/tlcl.php).
- B. W. Kernighan y R. Pike — *The Unix Programming Environment* (Prentice Hall).
- A. Hunt y D. Thomas — *The Pragmatic Programmer* (2ª ed., Addison-Wesley).

## 🔗 Qué abre esta parte

Con las herramientas instaladas y entendidas, la Parte 3 empieza el código: la primera clase con diez implementaciones verificadas.

---

> [⏮️ Parte 1](../parte-1-atlas-y-genealogia-de-los-lenguajes/README.md) · [⬅️ Programa](../../README.md) · [📚 Índice](../README.md) · [⏭️ Parte 3](../parte-3-valores-tipos-y-variables/README.md)
