# Clase 036 — REPL e intérpretes interactivos por lenguaje

> Parte **2 — Herramientas, toolchains y anatomía de comandos** · ⏱️ Duración estimada: **75 min** · Nivel: **Fundamentos**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

Hay una herramienta que convierte una duda en un experimento de tres segundos: el **REPL** (Read-Eval-Print Loop), una consola interactiva donde escribes una expresión, pulsas Enter y ves su resultado al instante, sin crear un archivo, sin compilar, sin ceremonia. El objetivo de esta clase es que incorpores el REPL a tu forma de trabajar: como laboratorio para explorar el comportamiento de un lenguaje, para verificar una hipótesis antes de escribirla en tu programa, y para aprender por experimentación directa. Casi todos los lenguajes del núcleo tienen uno, y saber abrirlo es saber tener un banco de pruebas siempre a mano.

El REPL encarna un valor que *The Unix Programming Environment* de Kernighan y Pike defiende sin descanso: la retroalimentación inmediata. Cuando el ciclo entre pensar algo y comprobarlo se reduce a segundos, aprendes y depuras a una velocidad que ningún ciclo de editar-compilar-ejecutar puede igualar. El REPL es esa inmediatez llevada al lenguaje mismo.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Explicar qué es un REPL y las cuatro fases de su bucle (leer, evaluar, imprimir, repetir).
2. Abrir el REPL de al menos dos lenguajes del núcleo y evaluar expresiones.
3. Distinguir cuándo el REPL es la herramienta adecuada y cuándo hace falta un archivo.
4. Reconocer qué lenguajes del núcleo no traen REPL nativo y qué alternativas existen.

## 🧩 Situación

Te asalta una duda clásica: ¿cuánto da `0.1 + 0.2` en JavaScript? Sabes que el punto flotante tiene rarezas, pero no recuerdas el detalle. Una opción es abrir tu editor, crear un archivo, escribir un `console.log`, guardarlo y ejecutarlo: un minuto de ceremonia para una pregunta trivial. La otra es teclear `node`, escribir `0.1 + 0.2` y leer al instante `0.30000000000000004`. El REPL convierte esa curiosidad en un experimento inmediato, y esa inmediatez cambia cómo aprendes: en lugar de suponer cómo se comporta un lenguaje, lo preguntas y te responde. Multiplica esto por las cien pequeñas dudas que tienes al día y entiendes por qué el REPL es una de las herramientas más infravaloradas.

## 📖 Leer, evaluar, imprimir, repetir

El nombre lo dice todo. El REPL **lee** lo que escribes, lo **evalúa** (calcula su valor o ejecuta su efecto), **imprime** el resultado y **repite**, esperando la siguiente entrada. La diferencia con ejecutar un archivo es que cada línea se procesa de inmediato y su resultado se muestra sin que pidas explícitamente imprimirlo: escribir `2 + 2` en el REPL muestra `4`, mientras que en un archivo tendrías que envolverlo en un `print`. Esa economía es lo que lo hace ideal para tantear.

El REPL mantiene una **sesión** con estado: las variables y definiciones que creas persisten mientras la consola está abierta. Puedes definir `x = 10`, luego `y = x * 2`, e ir construyendo sobre lo anterior como en una conversación. Ese estado acumulado es su fuerza para explorar de forma incremental, y también su límite: al cerrar el REPL, todo se pierde. Por eso el REPL complementa pero no reemplaza el código en archivos. Un programa real, que debe repetirse, versionarse y compartirse, vive en archivos; el REPL es el cuaderno de borrador donde pruebas ideas antes de pasarlas a limpio. Confundir ambos —escribir un programa entero en el REPL— es perder el trabajo al primer cierre.

No todos los lenguajes del núcleo traen REPL nativo, y eso mismo enseña algo sobre su naturaleza. Los interpretados y los de VM lo tienen casi por definición: Python (`python`), Node (`node`), PHP (`php -a`), C# (`dotnet fsi` para F#, o `csharprepl`). Los compilados a máquina, tradicionalmente, no: C y Go no incluyen un REPL de serie porque su modelo es compilar todo el programa. Rust tampoco trae uno oficial, aunque la comunidad ofrece `evcxr`. SQL, curiosamente, tiene la interactividad en su ADN: el cliente `sqlite3` o `psql` es un REPL de consultas donde cada sentencia se ejecuta y muestra resultados al instante.

## 🔬 Laboratorio guiado: abrir el REPL del núcleo

Abre el REPL de cada lenguaje que tengas y evalúa una expresión. La primera columna es el comando para entrar; dentro, escribes expresiones y las ves evaluarse:

```bash
python                 # Python; dentro: >>> 0.1 + 0.2   luego  exit()  o Ctrl-D
node                   # Node;   dentro: > 0.1 + 0.2      luego  .exit  o Ctrl-D
php -a                 # PHP interactivo; dentro: echo 2 ** 10;
sqlite3 :memory:       # SQL: motor interactivo; dentro: SELECT 2 + 2;   luego .quit
irb                    # Ruby (primo del núcleo): irb> 2 + 2
ghci                   # Haskell (primo): ghci> 2 + 2
```

Dentro de una sesión de Python, observa el estado que persiste y cómo cada expresión se muestra sin `print`:

```python
>>> x = 10
>>> y = x * 2
>>> y
20
>>> 0.1 + 0.2
0.30000000000000004
>>> import math; math.sqrt(2)
1.4142135623730951
```

Para los lenguajes sin REPL nativo, la alternativa idiomática es un archivo mínimo de un solo uso, o un ejecutor al vuelo:

```bash
# Go no tiene REPL: se usa un archivo desechable o el Go Playground (web)
echo 'package main; import "fmt"; func main(){ fmt.Println(2+2) }' > t.go && go run t.go

# Rust: 'evcxr' (instalable) da un REPL no oficial; si no, un archivo con cargo
# C: sin REPL; se compila un archivo pequeño para cada prueba
```

El contraste es revelador: en Python o Node preguntas y respondes en la misma línea; en Go o C, incluso una prueba trivial pasa por el ciclo de compilar. Esa fricción no es un defecto, es el reflejo de un modelo de ejecución distinto (clase 030).

## ✍️ Práctica

Abre el REPL de Python o Node y realiza tres experimentos que respondan dudas reales. Por ejemplo: evalúa `0.1 + 0.2` y observa la imprecisión del punto flotante; mezcla tipos (`"3" + 4` en Node frente a `"3" + str(4)` en Python) y compara qué hace cada lenguaje con la coerción; define un par de variables y comprueba que persisten entre líneas. Después, si tienes Go o C instalados, intenta responder una de esas mismas dudas en ellos y siente la diferencia: no hay REPL, así que debes crear un archivo, compilarlo y ejecutarlo. Anota cuál de las dos experiencias te dejó iterar más rápido y por qué. Termina cerrando el REPL correctamente (`exit()`, `.exit` o Ctrl-D) para memorizar cómo se sale.

## ⚠️ Errores comunes

| Síntoma / mensaje | Causa y cómo arreglar |
|-------------------|-----------------------|
| Escribir un programa entero en el REPL | Se pierde al cerrar. Usa el REPL para explorar; los programas van en archivos |
| No saber salir del REPL | Cada uno tiene su comando. Prueba `exit()`, `.exit`, `.quit` o Ctrl-D |
| Buscar el REPL de Go o C | No lo traen de serie. Usa un archivo desechable o un playground online |
| Confundir el resultado mostrado con algo impreso | El REPL muestra el valor de la expresión automáticamente; en un archivo necesitarías `print` |
| Pegar un bloque largo y que falle a medias | La indentación o el estado se enredan. Para bloques largos, mejor un archivo |

## ❓ Preguntas frecuentes

- **¿El REPL sirve para depurar?** Para probar fragmentos aislados y verificar hipótesis, es excelente. Para depurar un programa en marcha con su estado real, se usa un depurador. Son herramientas complementarias.
- **¿Por qué C no tiene REPL?** Porque su modelo es compilar el programa completo a código máquina; no hay un intérprete residente que evalúe expresiones sueltas. Existen experimentos (como Cling para C++), pero no es lo habitual.
- **¿Las variables del REPL se guardan al cerrar?** No: la sesión es efímera. Si quieres conservar el trabajo, cópialo a un archivo. Algunos REPL permiten guardar el historial, pero no es un sustituto de un programa.
- **¿El cliente de SQLite es un REPL?** Sí, en esencia: lee una sentencia, la ejecuta contra la base de datos, imprime el resultado y espera la siguiente. La interactividad es natural en las bases de datos.

## 🔗 Referencias

- W. Shotts — *The Linux Command Line* (2ª ed., No Starch Press) — [gratis online](https://linuxcommand.org/tlcl.php).
- B. W. Kernighan y R. Pike — *The Unix Programming Environment* (Prentice Hall), sobre la retroalimentación inmediata y las herramientas interactivas.
- A. Hunt y D. Thomas — *The Pragmatic Programmer* (2ª ed., Addison-Wesley), sobre experimentar para aprender un lenguaje.

---

> [⏮️ Clase 035](../../parte-2-herramientas-toolchains-y-anatomia-de-comandos/035-paquetes-y-dependencias-pip-pnpm-cargo-maven-gradle-nuget-go-mod-composer/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 037 ⏭️](../../parte-2-herramientas-toolchains-y-anatomia-de-comandos/037-formateadores-y-linters-black-prettier-gofmt-rustfmt-clang-format-php-cs-fixer/README.md)
