# Clase 031 — Anatomía de un comando: nombre, subcomando, flags, argumentos y esquema

> Parte **2 — Herramientas, toolchains y anatomía de comandos** · ⏱️ Duración estimada: **75 min** · Nivel: **Fundamentos**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

La línea de comandos asusta al principio porque parece un idioma secreto: cadenas crípticas de guiones, letras y rutas que la gente copia de foros sin entender. Pero no es un idioma secreto, es una gramática, y una muy regular. Todo comando —da igual si es `git`, `gcc`, `docker` o `dotnet`— se descompone en las mismas piezas: un **nombre** de programa, un **subcomando** opcional, unas **opciones** o *flags* que modifican el comportamiento y unos **argumentos** posicionales sobre los que actúa. El objetivo de esta clase es que interiorices ese esquema hasta el punto de poder *leer* un comando que nunca viste, *modificarlo* con seguridad y *componer* el tuyo propio, en lugar de pegar a ciegas.

Es, además, la herramienta transversal de toda la Parte 2: cada clase siguiente presenta comandos de un toolchain distinto, y todos obedecen esta misma gramática. Dominarla una vez es entender la estructura de miles de comandos que aún no conoces.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Descomponer cualquier comando en nombre, subcomando, flags y argumentos.
2. Distinguir flags cortas (`-v`), largas (`--verbose`), booleanas y con valor (`-o salida`).
3. Leer la línea de uso (*usage*) de la ayuda y deducir qué acepta un comando.
4. Reconocer las convenciones POSIX/GNU que comparten casi todas las herramientas.

## 🧩 Situación

Alguien copia `git commit -m "fix"` de un tutorial. Funciona. Al día siguiente quiere hacer commit de *todos* los archivos a la vez y no sabe cómo, porque nunca entendió qué era cada parte de aquel comando: para él era una fórmula mágica indivisible. Quien reconoce el esquema —programa `git`, subcomando `commit`, flag `-m` que lleva como valor el mensaje— ve de inmediato dónde encajaría un `-a` para incluir los cambios, o un `--amend` para corregir el commit anterior. La diferencia entre estos dos usuarios no es memoria: es haber entendido la gramática. *The Linux Command Line* de Shotts dedica sus primeros capítulos justamente a esto, porque es el cimiento sobre el que se construye toda fluidez en la terminal.

## 📖 La gramática de un comando

El esquema general se escribe así, y las convenciones de las páginas de manual lo formalizan: lo que va entre corchetes es opcional, y `...` indica que puede repetirse.

```text
programa [subcomando] [opciones] [argumentos]
```

El **nombre** es el ejecutable que el sistema busca en el `PATH` (lo veremos en la clase 040). El **subcomando** aparece en herramientas que agrupan muchas acciones bajo un mismo programa: `git commit`, `git push`, `docker run`, `dotnet build`, `cargo test`. No todas las herramientas los tienen —`gcc` o `ls` no— pero la tendencia moderna es agrupar funcionalidad en subcomandos, como hacen `git` o `go`.

Las **opciones** o *flags* modifican el comportamiento y siguen convenciones bien establecidas. Una flag *corta* es un guion y una letra (`-v`); una flag *larga* es dos guiones y una palabra (`--verbose`). Suelen ser sinónimos: `-v` y `--verbose` hacen lo mismo, la corta para teclear rápido y la larga para que un script se lea solo. Una flag puede ser *booleana* —está o no está, como un interruptor: `-l`, `--force`— o *llevar un valor*: `-o salida` o `--output=salida` dicen «la salida va a este archivo». Por convención GNU, las flags cortas booleanas se pueden agrupar: `ls -l -a -h` es lo mismo que `ls -lah`. Y `--` a secas marca «aquí terminan las opciones», útil cuando un argumento empieza por guion.

Los **argumentos posicionales** son los datos sobre los que el comando opera, y su significado depende de dónde están, no de un nombre: en `cp origen destino`, el primero es la fuente y el segundo el destino; intercambiarlos cambia todo. Esta distinción —opciones con nombre frente a argumentos por posición— es la que más confunde al principiante, que a veces pone un archivo donde iba una flag o viceversa.

La belleza del esquema es que la propia herramienta te lo revela. La línea de *usage* que imprime `--help` es exactamente esta gramática escrita para ese comando concreto. Aprender a leerla es aprender a usar cualquier herramienta sin tutorial: el manual, decía la tradición Unix, es la fuente de verdad.

## 🔬 Laboratorio guiado: diseccionar comandos reales

Toma el mismo esquema y obsérvalo repetirse en toolchains de distintos lenguajes. Aquí están anotados por partes:

```text
  git     commit   -m "mensaje inicial"
  └┬─┘    └──┬─┘   └────────┬────────┘
 nombre  subcomando   flag con valor

  gcc     main.c   -o main          # nombre + argumento (fuente) + flag con valor (salida)
  cargo   build    --release        # nombre + subcomando + flag booleana
  docker  run      -it   ubuntu bash  # flags agrupadas (-i -t) + argumentos posicionales
  dotnet  build    -c Release        # -c (--configuration) lleva el valor Release
```

Ahora compara la *misma idea* —«compila este archivo y llama al resultado `app`»— entre lenguajes, para ver que la gramática es universal aunque cambien los nombres:

```bash
gcc   main.c   -o app          # C:    -o = output
rustc main.rs  -o app          # Rust: mismo -o
go    build    -o app main.go  # Go:   subcomando build + -o + argumento posicional
javac Main.java                # Java: sin -o; el nombre de salida lo dicta la clase
tsc   main.ts  --outFile app.js  # TS: flag larga con valor
```

Y practica leer la ayuda, que es donde vive el esquema autoritativo. Casi todo comando responde a `--help`, y muchos tienen página de manual:

```bash
git commit --help      # muestra el USAGE: git commit [<options>] [--] <pathspec>...
gcc --help             # lista las opciones de gcc
ls --help              # en la cabecera: "Usage: ls [OPTION]... [FILE]..."
man ls                 # el manual completo (q para salir); [OPTION]... = repetible
tar --help | head -20  # combina ayuda con otra herramienta vía tubería
```

Fíjate en cómo se lee `Usage: ls [OPTION]... [FILE]...`: el nombre es `ls`, acepta cero o más opciones y cero o más archivos, ambos repetibles. Esa sola línea te dice cómo se usa `ls` sin necesidad de ningún tutorial. La disciplina de leer el *usage* antes de copiar es, según Shotts, lo que separa al que sufre la terminal del que la maneja.

## ✍️ Práctica

Etiqueta cada parte de `rustc main.rs -o main`: nombre (`rustc`), argumento posicional (`main.rs`), flag con valor (`-o` con valor `main`). Después ejecuta `git --help` y localiza en su salida la línea de *usage*; identifica qué es opcional (corchetes) y qué es repetible (`...`). A continuación, toma un comando que uses por costumbre sin entenderlo del todo —por ejemplo `docker run -it ubuntu bash`— y descomponlo entero: ¿qué son `-i` y `-t`, por qué están juntos, cuál es la imagen y cuál el comando a ejecutar dentro? Verifica tus hipótesis con `docker run --help`. Termina inventando una variante propia: cambia una flag y predice qué hará antes de ejecutarla.

## ⚠️ Errores comunes

| Síntoma / mensaje | Causa y cómo arreglar |
|-------------------|-----------------------|
| Copiar un comando y no saber adaptarlo | No se reconoció el esquema. Descompón siempre en nombre/subcomando/flags/argumentos |
| Poner un argumento donde iba una flag | Confundir posición con opción. Recuerda: las flags empiezan por `-` o `--` |
| `unknown option` con una flag correcta | Flag larga escrita con un guion (`-verbose`) o corta con dos. Un guion = corta, dos = larga |
| Un valor con espacios se parte en varios argumentos | Falta comillas: usa `-m "mensaje con espacios"` |
| Un argumento que empieza por `-` se toma por flag | Usa `--` para cerrar las opciones: `rm -- -archivo-raro` |

## ❓ Preguntas frecuentes

- **¿Por qué unas flags llevan un guion y otras dos?** Convención POSIX/GNU: un guion para la forma corta de una letra (`-v`), dos para la forma larga y legible (`--verbose`). Suelen ser equivalentes; la larga se prefiere en scripts por claridad.
- **¿Cómo sé qué opciones acepta un comando?** Con `comando --help` para un resumen o `man comando` para el manual completo. Ambos muestran la línea de *usage*, que es el esquema exacto de ese comando.
- **¿Puedo juntar varias flags cortas?** Sí, si son booleanas: `ls -l -a` es igual que `ls -la`. No se pueden agrupar las que llevan valor.
- **¿El orden de las flags importa?** Casi nunca entre sí, pero los argumentos posicionales sí dependen del orden. `cp a b` no es lo mismo que `cp b a`.

## 🔗 Referencias

- W. Shotts — *The Linux Command Line* (2ª ed., No Starch Press), caps. iniciales sobre el shell y la ayuda — [gratis online](https://linuxcommand.org/tlcl.php).
- B. W. Kernighan y R. Pike — *The Unix Programming Environment* (Prentice Hall), sobre la filosofía de herramientas de línea de comandos.
- A. Hunt y D. Thomas — *The Pragmatic Programmer* (2ª ed., Addison-Wesley), sobre dominar un shell.

---

> [⏮️ Clase 030](../../parte-2-herramientas-toolchains-y-anatomia-de-comandos/030-compilado-vs-interpretado-vs-transpilado-vs-bytecode-vm/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 032 ⏭️](../../parte-2-herramientas-toolchains-y-anatomia-de-comandos/032-instalacion-y-gestion-de-versiones-pyenv-nvm-rustup-sdkman-phpenv/README.md)
