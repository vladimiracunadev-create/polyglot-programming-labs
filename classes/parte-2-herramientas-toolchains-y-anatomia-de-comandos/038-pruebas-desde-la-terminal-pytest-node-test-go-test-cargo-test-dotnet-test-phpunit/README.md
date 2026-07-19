# Clase 038 — Pruebas desde la terminal: pytest, node --test, go test, cargo test, dotnet test, phpunit

> Parte **2 — Herramientas, toolchains y anatomía de comandos** · ⏱️ Duración estimada: **75 min** · Nivel: **Fundamentos**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

Una prueba automatizada es código que verifica otro código: le da entradas conocidas, comprueba que la salida es la esperada y te dice, en verde o rojo, si algo se rompió. El objetivo de esta clase es que sepas ejecutar pruebas desde la línea de comandos en cada lenguaje del núcleo, porque ese es el gesto que sostiene todo el desarrollo profesional y, en particular, el verificador de equivalencia de este curso. No vas a aprender aquí a diseñar suites exhaustivas —eso es la Parte 9—, sino a entender qué es una prueba, cómo se ejecuta con un comando y por qué el ciclo rojo/verde es el latido de cualquier proyecto sano.

La idea conecta con dos raíces. Kernighan y Pike, en la tradición Unix, ya trataban los programas como componentes que se comprueban automáticamente encadenando herramientas. Y *The Pragmatic Programmer* eleva las pruebas a principio: el código sin pruebas es código en el que no puedes confiar para cambiarlo, porque no sabrías si lo rompiste. Las pruebas son lo que convierte un cambio de un salto de fe en una comprobación.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Explicar qué es una prueba automatizada, una aserción y el estado verde/rojo de una suite.
2. Ejecutar las pruebas de cada lenguaje del núcleo con su runner desde la terminal.
3. Interpretar la salida de un runner: cuántas pasaron, cuál falló y por qué.
4. Relacionar las pruebas con el verificador de equivalencia y con casos.json del curso.

## 🧩 Situación

Cambias una función que creías aislada y te vas a dormir con la duda de si rompiste algo en otra parte del sistema. Sin pruebas, la única forma de saberlo es ejecutar el programa a mano por todos sus caminos, algo lento y que nadie hace de verdad. Con pruebas, tecleas `pytest` y en segundos sabes si las doscientas comprobaciones siguen en verde o si una se puso roja señalando exactamente qué comportamiento cambió. Ese cambio —de la incertidumbre a la certeza en un comando— es la razón por la que las pruebas no son un lujo sino infraestructura. El verificador de equivalencia de este curso es, en el fondo, exactamente esto: una prueba que comprueba que las diez implementaciones producen la misma salida.

## 📖 Aserción, runner y rojo/verde

En el corazón de toda prueba está la **aserción**: una afirmación que el código comprueba y que debe ser verdadera. `assert suma(2, 3) == 5` dice «espero que sumar 2 y 3 dé 5». Si lo es, la prueba pasa; si no, falla y el runner te muestra qué esperabas y qué obtuviste. Una prueba es un conjunto de aserciones alrededor de un comportamiento concreto, con un nombre que describe qué verifica. La disciplina de nombrar bien las pruebas es la misma legibilidad de la Parte 0 aplicada aquí: `test_suma_de_negativos` te dice al fallar exactamente qué se rompió.

El **runner** es la herramienta que descubre las pruebas en tu proyecto, las ejecuta todas y reporta el resultado. Su virtud es que un solo comando corre cientos de comprobaciones: `pytest` busca los archivos y funciones de prueba por convención y las ejecuta; `go test ./...` recorre todos los paquetes; `cargo test` corre las pruebas del crate. No tienes que llamar a cada prueba a mano —el runner las encuentra— y ese descubrimiento automático es lo que hace viable tener miles de pruebas.

El resultado se expresa en el binomio **verde/rojo**. Verde: todo pasó, el código se comporta como se espera. Rojo: al menos una aserción falló, y el runner señala cuál, con el valor esperado y el obtenido para que localices el problema. Este estado es lo que un sistema de **integración continua** (CI) automatiza: en cada cambio subido, corre la suite; si se pone en rojo, bloquea la fusión. Así, ningún cambio que rompa una prueba llega al código principal. El ciclo rojo/verde no es solo tuyo mientras programas: es el guardián automático del proyecto entero.

## 🔬 Laboratorio guiado: correr pruebas en cada lenguaje

El comando de pruebas del núcleo, uno por ecosistema. Casi todos descubren las pruebas por convención y basta invocarlos:

```bash
pytest                        # Python: descubre test_*.py y funciones test_*
node --test                   # JavaScript: runner nativo desde Node 18
go test ./...                 # Go: prueba todos los paquetes del módulo
cargo test                    # Rust: compila y corre las pruebas del proyecto
dotnet test                   # C#: descubre y ejecuta el proyecto de pruebas
./vendor/bin/phpunit          # PHP: PHPUnit sobre el directorio de tests
```

La salida de un runner sigue un patrón común: un resumen de cuántas pasaron y cuántas fallaron, y el detalle de las fallidas. Así se lee un rojo en pytest:

```text
FAILED test_ventas.py::test_total_con_descuento - assert 26100.0 == 27000.0
=================== 1 failed, 12 passed in 0.08s ===================
```

Esa línea te dice todo: falló una prueba, su nombre indica qué comportamiento (total con descuento), y la aserción muestra que esperaba `27000.0` pero obtuvo `26100.0` —probablemente aplicaste el descuento dos veces—. Doce pruebas siguieron en verde, así que el resto del sistema está intacto.

Filtra y observa con flags útiles que comparten casi todos los runners:

```bash
pytest -k descuento           # solo las pruebas cuyo nombre contiene 'descuento'
pytest -v                     # modo verboso: lista cada prueba y su resultado
go test -run TestTotal ./...  # solo la prueba que coincide con el patrón
cargo test suma               # solo las pruebas que contienen 'suma'
```

Y comprueba la conexión con el curso: el verificador de equivalencia es una prueba especializada que alimenta cada caso de `casos.json` a cada implementación y compara la salida:

```bash
python scripts/verificar_equivalencia.py 041   # verde si las 10 dan la misma salida
python scripts/verificar_equivalencia.py --all  # toda la colección
```

## ✍️ Práctica

Ejecuta el verificador de equivalencia sobre la clase 041 con `python scripts/verificar_equivalencia.py 041` y lee su salida con atención: identifica qué lenguajes verificó, cuáles omitió por falta de toolchain y qué significa el «verde» de cada implementación. Reconoce que, en el fondo, está haciendo lo mismo que `pytest`: comparar una salida real con una esperada. Si tienes un runner instalado, crea una función sencilla (una suma, por ejemplo) y una prueba con una aserción correcta; córrela y observa el verde. Después rompe la función a propósito —haz que sume mal— y vuelve a correr: estudia el rojo, y fíjate en cómo el runner te dice exactamente qué esperaba y qué obtuvo. Ese mensaje es el que te ahorrará horas cuando el fallo sea real.

## ⚠️ Errores comunes

| Síntoma / mensaje | Causa y cómo arreglar |
|-------------------|-----------------------|
| Verificar solo a mano ejecutando el programa | Lento y no repetible. Escribe pruebas que corran con un comando |
| No correr las pruebas antes de subir cambios | Rompes el CI y a tus compañeros. Ejecuta la suite en local antes del push |
| `No tests ran` / el runner no encuentra nada | Los archivos o funciones no siguen la convención de nombres. Revisa `test_*` / `*_test.go` |
| Pruebas que dependen del orden o de estado global | Se rompen de forma intermitente. Cada prueba debe ser independiente y repetible |
| Una prueba en rojo que se ignora «porque el programa funciona» | El rojo señala una discrepancia real. Corrígela o entiende por qué falla |

## ❓ Preguntas frecuentes

- **¿Cuántas pruebas necesito?** Al menos una por comportamiento importante y una por cada caso límite (vacío, cero, negativo). La calidad y la cobertura de los casos difíciles importan más que el número total.
- **¿`casos.json` es una prueba?** Sí, en esencia: define entradas y salidas esperadas, y el verificador las comprueba igual que un runner comprueba aserciones. Es la prueba que garantiza la equivalencia entre lenguajes.
- **¿Qué diferencia hay entre una prueba y ejecutar el programa?** Ejecutar el programa te muestra qué hace *una vez* con *unos* datos, y lo juzgas a ojo. Una prueba fija la entrada y la salida esperada y las compara automáticamente, cuantas veces haga falta, sin intervención.
- **¿Por qué el CI corre las pruebas si yo ya las corrí?** Para garantizarlo objetivamente en un entorno limpio, independiente de tu máquina. Es la red de seguridad que atrapa el «se me olvidó correrlas».

## 🔗 Referencias

- W. Shotts — *The Linux Command Line* (2ª ed., No Starch Press) — [gratis online](https://linuxcommand.org/tlcl.php).
- B. W. Kernighan y R. Pike — *The Unix Programming Environment* (Prentice Hall), sobre comprobar programas de forma automatizada.
- A. Hunt y D. Thomas — *The Pragmatic Programmer* (2ª ed., Addison-Wesley), sobre pruebas como red de seguridad para el cambio.

---

> [⏮️ Clase 037](../../parte-2-herramientas-toolchains-y-anatomia-de-comandos/037-formateadores-y-linters-black-prettier-gofmt-rustfmt-clang-format-php-cs-fixer/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 039 ⏭️](../../parte-2-herramientas-toolchains-y-anatomia-de-comandos/039-empaquetado-y-distribucion-wheels-jars-binarios-contenedores/README.md)
