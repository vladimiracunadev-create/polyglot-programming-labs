# Clase 033 — Ejecutar: python, node, tsx, java, dotnet, go run, rustc, cc, php, sqlite3

> Parte **2 — Herramientas, toolchains y anatomía de comandos** · ⏱️ Duración estimada: **75 min** · Nivel: **Fundamentos**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

Toda la Parte 2 gira alrededor de una operación que parece obvia y que cambia de forma en cada lenguaje: *ejecutar* un programa. El objetivo de esta clase es que tengas, comprendido y no solo memorizado, el comando de ejecución de cada lenguaje del núcleo, y que entiendas por qué unos son de un solo paso y otros de dos. Esta no es una lista de recetas: es el mapa que usarás en cada clase de código del curso, donde cada implementación viene acompañada de su comando de ejecución. Si sabes *por qué* `python main.py` no deja un binario pero `rustc main.rs` sí, dejarás de sorprenderte y empezarás a predecir.

La razón por la que los comandos difieren es exactamente el modelo de ejecución de la clase 030. Ejecutar un interpretado es «dale el fuente al intérprete»; ejecutar un compilado es «tradúcelo primero y luego corre el resultado». El comando refleja fielmente la cadena de herramientas de cada lenguaje, así que aprender los comandos es, en el fondo, repasar el toolchain de cada uno desde la práctica.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Ejecutar un «hola mundo» en cada lenguaje del núcleo con su comando propio.
2. Explicar por qué unos comandos ejecutan en un paso y otros requieren compilar primero.
3. Relacionar cada comando de ejecución con el modelo del lenguaje (interpretado, compilado, VM, motor).
4. Distinguir los comandos que dejan un artefacto reutilizable de los que no.

## 🧩 Situación

Al abrir la clase 041 —la primera de código— te encuentras diez implementaciones del mismo problema, cada una con su comando de ejecución al pie. Si esos comandos te resultan opacos, el estudio se convierte en una búsqueda constante en internet: cada lenguaje interrumpe tu concentración. Si en cambio los tienes claros, ejecutar cualquier implementación es un reflejo y puedes concentrarte en lo que importa, que es comparar cómo cada lenguaje resuelve el problema. Esta clase existe para que esa fricción desaparezca: es la tabla de referencia que convierte «¿cómo se corría esto?» en un gesto automático.

## 📖 Un paso, dos pasos y el caso del motor

Los lenguajes **interpretados** se ejecutan en un solo gesto: le entregas el archivo fuente al intérprete y este lo corre. `python main.py`, `node main.mjs`, `php main.php`. No queda ningún artefacto: cierras y solo tienes tu fuente. Es el ciclo más rápido para iterar, coherente con la filosofía de herramientas ligeras que describen Kernighan y Pike, donde escribir y probar están a un teclazo de distancia.

Los lenguajes **compilados a máquina** se dividen en dos estilos. Rust y C son de *dos pasos* explícitos: primero compilas (`rustc main.rs -o main`, `cc main.c -o main`) y eso produce un binario; luego lo ejecutas (`./main`). El binario es un artefacto reutilizable: puedes correrlo mil veces sin recompilar, e incluso copiarlo a otra máquina compatible. Go ofrece un atajo de *un paso* para desarrollo, `go run main.go`, que compila a un binario temporal, lo ejecuta y lo descarta; cuando quieras el binario permanente usarás `go build` (clase 034). Ese contraste —`go run` para probar, `go build` para conservar— resume la diferencia entre ejecutar y construir.

Los lenguajes sobre **máquina virtual** tienen su propia forma. Java tradicionalmente compila con `javac` y ejecuta con `java`, pero desde Java 11 puede correr un único archivo fuente directamente: `java Main.java` lo compila en memoria y lo ejecuta, muy cómodo para ejemplos. C# con .NET usa `dotnet run`, que restaura dependencias, compila y ejecuta el proyecto en un solo comando. TypeScript no se ejecuta por sí mismo: o lo transpilas y corres el JS resultante, o usas un ejecutor como `tsx`/`ts-node` que hace ambas cosas al vuelo (`tsx main.ts`).

SQL es el forastero: no se «ejecuta» como los demás porque es declarativo. Se lo entregas a un **motor** de base de datos que lo interpreta y devuelve resultados. En el curso, ese motor es SQLite: `sqlite3 :memory: < main.sql` crea una base de datos temporal en memoria y le alimenta el archivo por la entrada estándar, usando el operador `<` de redirección que Shotts explica como uno de los pilares del shell.

## 🔬 Laboratorio guiado: ejecutar el núcleo entero

Esta es la tabla de ejecución que reaparece en cada clase de código. Cada línea es un comando real y comprobado:

```bash
python main.py                    # Python: interpreta el fuente, sin artefacto
node main.mjs                     # JavaScript: V8 lo corre (JIT), sin artefacto
pnpm exec tsx main.ts             # TypeScript: transpila y ejecuta al vuelo
java Main.java                    # Java: compila en memoria y ejecuta (JDK 11+)
dotnet run                        # C#: restaura, compila y ejecuta el proyecto
go run main.go                    # Go: compila a binario temporal y lo corre
rustc main.rs -o main && ./main   # Rust: DOS pasos, deja el binario 'main'
cc main.c -o main && ./main       # C: DOS pasos, deja el binario 'main'
php main.php                      # PHP: el motor Zend lo ejecuta
sqlite3 :memory: < main.sql       # SQL: el motor SQLite ejecuta la consulta
```

Observa el patrón con lupa. Las líneas con `&&` son las de dos pasos: `&&` encadena de modo que el segundo comando solo corre si el primero tuvo éxito (si la compilación falla, no intenta ejecutar). Tras esas dos líneas queda un archivo `main` en tu carpeta; tras `python main.py` no queda nada nuevo. Ese es el criterio observable para distinguir compilado de interpretado desde la terminal:

```bash
ls                    # antes de ejecutar
rustc main.rs -o main
ls                    # ahora aparece 'main' -> compilado deja artefacto
python main.py
ls                    # nada nuevo -> interpretado no deja artefacto
```

## ✍️ Práctica

Escribe un «hola mundo» en dos lenguajes que tengas instalados, uno interpretado y uno compilado (por ejemplo Python y C, o Node y Go). Ejecuta ambos y, con `ls` antes y después, comprueba cuál dejó un archivo binario y cuál no. Con el compilado, ejecuta el binario resultante *directamente* (`./main`) sin volver a compilar, y verifica que corre igual: acabas de comprobar que el artefacto es reutilizable. Si tienes Java, prueba las dos formas —`java Main.java` de un tirón frente a `javac` seguido de `java Main`— y observa que la primera no deja `.class` visible y la segunda sí. Anota, para cada lenguaje que uses, si su comando de ejecución es de uno o dos pasos y por qué.

## ⚠️ Errores comunes

| Síntoma / mensaje | Causa y cómo arreglar |
|-------------------|-----------------------|
| Buscar un binario tras `python main.py` | Esperar comportamiento de compilado. Los interpretados no generan ejecutable |
| Compilar en Rust/C y que «no pase nada» | Olvidaste el segundo paso. Ejecuta `./main` o encadena con `&& ./main` |
| `./main: command not found` estando el archivo | Falta el `./`: el directorio actual no está en el `PATH` por seguridad (clase 040) |
| `Permission denied` al correr el binario | Falta permiso de ejecución. `chmod +x main` en Unix |
| `dotnet run` no encuentra un proyecto | Debes estar en la carpeta con el `.csproj`. `dotnet run` opera sobre el proyecto, no un archivo suelto |

## ❓ Preguntas frecuentes

- **¿`java Main.java` no necesita compilar?** Sí compila, pero en memoria y de forma transparente: desde Java 11 el lanzador acepta un único archivo fuente, lo compila al vuelo y lo ejecuta sin dejar el `.class`. Para varios archivos vuelves a `javac` + `java`.
- **¿Por qué `go run` y no `go build`?** `go run` compila a un binario temporal, lo ejecuta y lo borra: ideal para probar. `go build` conserva el binario para distribuirlo. Son dos intenciones distintas.
- **¿Qué hace el `<` en `sqlite3 :memory: < main.sql`?** Es redirección de entrada del shell: alimenta el contenido de `main.sql` a `sqlite3` como si lo hubieras tecleado. `:memory:` indica una base de datos temporal en RAM.
- **¿Por qué necesito `./` para correr mi binario?** Porque, por seguridad, el directorio actual no está en el `PATH`. `./main` dice explícitamente «el `main` de aquí». La clase 040 lo detalla.

## 🔗 Referencias

- W. Shotts — *The Linux Command Line* (2ª ed., No Starch Press), sobre redirección (`<`, `>`) y ejecución de programas — [gratis online](https://linuxcommand.org/tlcl.php).
- B. W. Kernighan y R. Pike — *The Unix Programming Environment* (Prentice Hall).
- A. Hunt y D. Thomas — *The Pragmatic Programmer* (2ª ed., Addison-Wesley).

---

> [⏮️ Clase 032](../../parte-2-herramientas-toolchains-y-anatomia-de-comandos/032-instalacion-y-gestion-de-versiones-pyenv-nvm-rustup-sdkman-phpenv/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 034 ⏭️](../../parte-2-herramientas-toolchains-y-anatomia-de-comandos/034-compilar-y-construir-gcc-clang-cargo-go-build-javac-dotnet-build/README.md)
