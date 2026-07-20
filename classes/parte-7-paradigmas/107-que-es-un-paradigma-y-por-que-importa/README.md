# Clase 107 — Qué es un paradigma y por qué importa

> Parte **7 — Paradigmas** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Un **paradigma de programación** no es un lenguaje ni una sintaxis: es un marco mental, una manera de descomponer un problema y decidir qué cuenta como una "pieza" legítima de la solución. Van Roy y Haridi abren *Concepts, Techniques, and Models of Computer Programming* justamente con esta idea: un lenguaje se entiende mejor como la encarnación de uno o varios *modelos de cómputo*, y cada modelo trae consigo un vocabulario propio (estado y asignación, funciones y valores, relaciones y restricciones). Cambiar de paradigma no es cambiar de teclado; es cambiar la pregunta que uno se hace frente al problema. El imperativo pregunta "¿qué pasos, en qué orden, transforman el estado hasta la respuesta?"; el funcional pregunta "¿qué valor es la respuesta, expresado como composición de funciones?"; el declarativo pregunta "¿qué relación describe la respuesta, dejando el cómo a la máquina?".

El objetivo de esta clase es que interiorices que el mismo problema admite varias formas correctas, y que la elección de forma tiene consecuencias reales sobre legibilidad, verificabilidad y coste. Tomamos el ejemplo más humilde posible —sumar los enteros de 1 a n— precisamente porque su trivialidad deja al desnudo la diferencia de *estilo*. Sebesta, en el capítulo 1 de *Concepts of Programming Languages*, ofrece los criterios con los que se juzga un lenguaje (legibilidad, escribibilidad, confiabilidad); esos mismos criterios se aplican a la elección de paradigma dentro de un lenguaje multiparadigma.

Al terminar deberías poder mirar un fragmento de código y nombrar el paradigma que encarna, y a la inversa: dado un problema, anticipar qué estilo lo expresará con menos fricción. Esa doble lectura es la competencia central de todo el resto de la Parte 7.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Definir qué es un paradigma.
2. Reconocer que un problema admite varios enfoques.
3. Situar los paradigmas del curso.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Paradigma | Forma de estructurar la solución |
| 2 | Multiparadigma | Un lenguaje puede ofrecer varios |
| 3 | Mismo problema, varios enfoques | Imperativo, funcional, declarativo |

## 📖 Definiciones y características

- **Paradigma** — estilo de estructurar programas (imperativo, OO, funcional, declarativo). Clave: cambia cómo se piensa.
- **Multiparadigma** — lenguaje que soporta varios estilos (Python, C#, Rust). Clave: eliges por problema.
- **Enfoque** — la estrategia elegida para resolver. Clave: distintos paradigmas, distinta forma.

La palabra "paradigma" aplicada a la programación popularizada por Robert Floyd en su conferencia Turing de 1978, y sistematizada después por autores como Van Roy, designa algo más profundo que un estilo: es un conjunto coherente de conceptos que determina qué construcciones existen y cómo se combinan. Van Roy sostiene que un buen programador no piensa en "el lenguaje X", sino en el modelo de cómputo que ese lenguaje soporta, y que la mayoría de los lenguajes modernos son *multiparadigma* porque combinan varios modelos en uno. Por eso Python, C# o Rust dejan escribir el mismo problema con un bucle o con `sum`/`reduce`: no cambian de lenguaje, cambian de modelo dentro del lenguaje.

SICP lo muestra desde su primera sección (1.1): distingue con cuidado entre el *procedimiento* que escribimos y el *proceso* que ese procedimiento genera al ejecutarse. Un procedimiento recursivo puede generar un proceso iterativo, y un bucle puede generar el mismo proceso que una recursión de cola. Esta distinción es la raíz de todo el mapa de paradigmas: la forma del texto (el estilo) y la forma de la evolución en el tiempo (el proceso) son ejes independientes. Sumar 1..n es un caso de prueba ideal porque el proceso subyacente es el mismo —recorrer o plegar los números— mientras que la forma varía radicalmente entre un `for`, un `sum(range(...))` y la fórmula cerrada `n(n+1)/2`.

Sebesta añade la dimensión económica: los criterios de evaluación de lenguajes (legibilidad frente a escribibilidad, coste de aprendizaje, confiabilidad) explican por qué ningún paradigma "gana" en abstracto. El declarativo suele ganar en legibilidad de la intención; el imperativo, en control fino del rendimiento. Elegir paradigma es elegir qué criterio priorizas para ese problema concreto.

## 🧩 Situación

Imagina que llegas a un equipo donde tres personas resolvieron la misma tarea de reporting —sumar los importes de una lista— en tres estilos distintos: una escribió un bucle `for` que acumula, otra encadenó `reduce`, y la tercera dejó que la base de datos lo hiciera con `SELECT sum(...)`. Ninguna está equivocada; las tres producen el mismo número. Pero cuando el equipo discute cuál mantener, descubren que en realidad discuten de paradigmas, no de sabor personal. El bucle explicita cada paso y es fácil de instrumentar con logs; el `reduce` comunica la intención "plegar en un total" sin ruido de índices; la consulta delega el cómo al motor y escala a millones de filas sin cambiar una letra.

Aquí replicamos ese escenario con el problema más pequeño que lo hace visible: leer un entero `n` y emitir `suma=1+2+...+n`. El resultado esperado está fijado en [`casos.json`](casos.json) (`5 → suma=15`, `3 → suma=6`, `1 → suma=1`), idéntico para las diez implementaciones. Lo que cambia entre ellas no es la respuesta: es la forma de pensarla. Esa invariancia del resultado frente a la variación de la forma es exactamente lo que define un paradigma.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n` (n >= 1)
- **Salida** (stdout): `suma=<1+2+...+n>`
- **Regla:** suma = 1 + 2 + ... + n

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `suma=15` |
| `3` | `suma=6` |
| `1` | `suma=1` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER n ; sumar 1..n ; ESCRIBIR suma
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys

n = int(sys.stdin.readline())
suma = sum(range(1, n + 1))
print(f"suma={suma}")
```

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
let suma = 0;
for (let i = 1; i <= n; i++) suma += i;
console.log(`suma=${suma}`);
```

🧬 **El mismo programa en la familia JavaScript / web:** [Dart · ActionScript](primos.md#javascript-web)

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
let suma = 0;
for (let i = 1; i <= n; i++) suma += i;
console.log(`suma=${suma}`);
```

🧬 **El mismo programa en la familia JavaScript / web:** [Dart · ActionScript](primos.md#javascript-web)

### Java · [`java/Main.java`](implementaciones/java/Main.java) · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        long suma = 0;
        for (int i = 1; i <= n; i++) suma += i;
        System.out.println("suma=" + suma);
    }
}
```

🧬 **El mismo programa en la familia JVM:** [Kotlin · Scala · Groovy · Clojure](primos.md#jvm)

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;

int n = int.Parse(Console.In.ReadToEnd().Trim());
long suma = 0;
for (int i = 1; i <= n; i++) suma += i;
Console.WriteLine($"suma={suma}");
```

🧬 **El mismo programa en la familia .NET:** [F# · VB.NET](primos.md#dotnet)

### Go · [`go/main.go`](implementaciones/go/main.go) · `go run main.go`

```go
package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	n, _ := strconv.Atoi(strings.TrimSpace(line))
	suma := 0
	for i := 1; i <= n; i++ {
		suma += i
	}
	fmt.Printf("suma=%d\n", suma)
}
```

🧬 **El mismo programa en la familia Sistemas:** [Zig · Nim · D](primos.md#sistemas)

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let suma: i64 = (1..=n).sum();
    println!("suma={suma}");
}
```

🧬 **El mismo programa en la familia Sistemas:** [Zig · Nim · D](primos.md#sistemas)

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    long suma = 0;
    for (long i = 1; i <= n; i++) suma += i;
    printf("suma=%ld\n", suma);
    return 0;
}
```

🧬 **El mismo programa en la familia C / llaves:** [C++ · Objective-C](primos.md#c-llaves)

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL (declarativo): suma con CTE recursivo (ilustrativo, n=5).
WITH RECURSIVE r(i) AS (VALUES (1) UNION ALL SELECT i + 1 FROM r WHERE i < 5)
SELECT printf('suma=%d', sum(i)) AS resultado FROM r;
```

🧬 **El mismo programa en la familia Lógica y declarativa:** [Prolog · Datalog](primos.md#logica-declarativa)

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
$n = (int) trim(fgets(STDIN));
$suma = 0;
for ($i = 1; $i <= $n; $i++) {
    $suma += $i;
}
echo "suma=$suma\n";
```

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🧪 Laboratorio guiado — recorrido del código

Sigamos el caso `5 → suma=15` de [`casos.json`](casos.json) a través de tres implementaciones que encarnan tres paradigmas, para *ver* que la diferencia no está en el resultado sino en la forma de razonar.

Empieza por **Python**, que aquí adopta el estilo funcional-declarativo. La línea `n = int(sys.stdin.readline())` lee el `5` de stdin y lo convierte en entero. La línea siguiente es la clave: `suma = sum(range(1, n + 1))`. No hay bucle a la vista, no hay variable que se actualice paso a paso. `range(1, 6)` describe la secuencia perezosa `1,2,3,4,5` (el `n + 1` es porque `range` excluye el extremo superior) y `sum` la *pliega* a un único valor, `15`. Estás describiendo *qué es* la suma —el pliegue de un rango— no *cómo* recorrerla. Es la lectura de SICP 1.1: expresas el resultado como composición de dos funciones, `sum ∘ range`. `print(f"suma={suma}")` emite `suma=15`, la salida exacta que exige el contrato.

Contrasta ahora con **Go**, que la escribe en estilo imperativo puro. Tras leer la línea y parsearla con `strconv.Atoi`, aparece el corazón del paradigma imperativo: `suma := 0` inicializa un *estado mutable* (el acumulador), y `for i := 1; i <= n; i++ { suma += i }` lo transforma paso a paso. En la primera vuelta `suma` pasa de 0 a 1; luego a 3, 6, 10 y 15. La respuesta no se *describe*: se *construye* mediante una secuencia de asignaciones sobre una celda de memoria que cambia en el tiempo. Esta es precisamente la esencia del modelo con estado que SICP analiza en 3.1: la variable `suma` tiene una identidad que persiste entre iteraciones y cuyo valor depende de la historia de asignaciones. `fmt.Printf("suma=%d\n", suma)` cierra con `suma=15`. JavaScript, TypeScript, Java, C#, C y PHP en esta clase siguen el mismo molde imperativo del bucle acumulador.

Finalmente, **SQL** encarna el paradigma declarativo llevado al extremo. El bloque usa un CTE recursivo, `WITH RECURSIVE r(i) AS (VALUES (1) UNION ALL SELECT i + 1 FROM r WHERE i < 5)`, que *genera* la relación de filas `1..5`, y `SELECT sum(i) ... FROM r` la agrega. Aquí no lees de stdin ni recorres nada tú: describes la relación que quieres y el motor decide el orden de evaluación. Por eso la nota bajo el código lo marca como *ilustrativo* —el `n=5` está incrustado en la consulta en lugar de leerse— y el verificador lo trata aparte. Es el mismo `15`, alcanzado sin un solo paso escrito por ti: la diferencia paradigmática hecha código. Ejecuta `python scripts/verificar_equivalencia.py 107` y comprobarás que las tres formas convergen en las salidas de `casos.json`, que es la demostración práctica de la tesis de la clase: el paradigma decide la forma, no el resultado.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Bucle, `reduce` o fórmula según el estilo. |
| Semántica | Todos dan el mismo resultado; cambia la estructura. |
| Paradigmática | Imperativo describe pasos; declarativo describe el resultado. |

Bajo la superficie las diferencias son más profundas que "un `for` frente a un `sum`". Python y Rust ofrecen el pliegue como parte natural del lenguaje (`sum(range(...))`, `(1..=n).sum()`), de modo que el estilo declarativo es idiomático y de primera clase; en C, en cambio, no existe un `sum` de biblioteca sobre rangos y el bucle imperativo es la única forma razonable, lo que hace que el lenguaje *empuje* hacia un paradigma. Java y C# se sitúan en medio: podrían usar `IntStream.rangeClosed(1,n).sum()` o LINQ, pero el código de esta clase eligió el bucle para mantener el contraste visible. Otra diferencia real es la de tipos y desbordamiento: Java, C# y C acumulan en `long`/`int` con aritmética de tamaño fijo (un `n` grande desbordaría silenciosamente en C), mientras que Python usa enteros de precisión arbitraria y nunca desborda, y SQLite decide el tipo dinámicamente. El mismo `suma=15` esconde, por tanto, modelos numéricos distintos: la equivalencia de salida no implica equivalencia de semántica interna.

## 🧬 El concepto en la familia

Casi todos los lenguajes del núcleo son *multiparadigma*, y esto no es un accidente histórico sino una tendencia de diseño que Van Roy documenta: los lenguajes maduros absorben conceptos de varios modelos porque ningún modelo único cubre bien todos los problemas. Python nació imperativo pero incorporó comprensiones, `map`/`filter`/`reduce` y clases; C# creció desde la OO imperativa hasta incluir LINQ (consultas declarativas) y funciones de primera clase; Rust combina control imperativo de memoria con iteradores funcionales y pattern matching. Los extremos del núcleo son ilustrativos: C es deliberadamente estrecho —imperativo y procedimental, sin cierre funcional idiomático ni consultas— y SQL es deliberadamente estrecho en el otro sentido —declarativo relacional, sin bucles ni estado mutable de usuario—. Entre esos dos polos, la mayoría de los lenguajes te dejan elegir el paradigma frase a frase, y la madurez profesional consiste en elegir bien.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 107
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Creer que hay un solo modo correcto** → causa: haber aprendido un único estilo y asumir que es *el* estilo, no *un* estilo → remedio: reescribe deliberadamente un mismo problema en dos paradigmas (el bucle y el `sum`/`reduce` de esta clase) hasta que ambos te resulten naturales; la fluidez de traducción es la señal de que dejaste de encasillarte.
- **Confundir paradigma con lenguaje** → causa: identificar "Java = OO" o "C = imperativo" como si el lenguaje fijara un único modelo → remedio: recuerda que Java tiene streams funcionales y C puede simular objetos con structs y punteros a función; el paradigma es un estilo que *eliges dentro* del lenguaje, no una etiqueta fija del lenguaje.
- **Juzgar un paradigma por un problema de juguete** → causa: concluir que "el declarativo es más corto" a partir de `sum(1..n)` → remedio: evalúa cada estilo con los criterios de Sebesta (legibilidad, escribibilidad, confiabilidad, rendimiento) sobre problemas de tamaño real, donde las diferencias de mantenimiento y escala se vuelven decisivas.

## ❓ Preguntas frecuentes

- **¿Cuál paradigma es mejor?** Ninguno en abstracto. Van Roy insiste en que cada modelo de cómputo resuelve bien cierta clase de problemas: el imperativo brilla donde importa el control fino del estado y el rendimiento; el funcional donde importa la componibilidad y el razonamiento sin efectos; el declarativo donde importa expresar el *qué* y delegar el *cómo* a un motor optimizado. "Mejor" solo tiene sentido relativo a un problema y a los criterios que priorizas.
- **¿Un lenguaje equivale a un paradigma?** Casi nunca. La inmensa mayoría de los lenguajes del núcleo son multiparadigma; C y SQL son las excepciones deliberadamente estrechas. Aun así, cada lenguaje tiene un paradigma "por defecto" que hace más cómodo —su *grano*— y escribir a contracorriente de ese grano suele salir caro.
- **¿La forma imperativa y la declarativa dan siempre el mismo resultado?** Dan el mismo resultado *observable* cuando resuelven la misma especificación, como demuestra `casos.json`, pero pueden diferir en propiedades no funcionales: uso de memoria, comportamiento ante desbordamiento, orden de evaluación y facilidad de paralelizar. La equivalencia de salida no es equivalencia total.

## 🔗 Referencias

**Libros de la parte:**

- P. Van Roy y S. Haridi — *Concepts, Techniques, and Models of Computer Programming* (MIT Press). Introducción y el "mapa de paradigmas": los modelos de cómputo como clave para entender los lenguajes.
- H. Abelson y G. J. Sussman — *Structure and Interpretation of Computer Programs* (2ª ed., MIT Press). Sección 1.1 (procedimientos y procesos) para la distinción entre la forma del texto y la forma del proceso.
- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson). Capítulo 1: criterios de evaluación de lenguajes (legibilidad, escribibilidad, confiabilidad).

**Libros de los lenguajes del núcleo:**

- L. Ramalho — *Fluent Python* (2ª ed., O'Reilly).
- M. Haverbeke — *Eloquent JavaScript* (3ª ed.) — [gratis online](https://eloquentjavascript.net/).
- B. Cherny — *Programming TypeScript* (O'Reilly).
- J. Bloch — *Effective Java* (3ª ed., Addison-Wesley).
- J. Skeet — *C# in Depth* (4ª ed., Manning).
- A. Donovan y B. Kernighan — *The Go Programming Language* (Addison-Wesley).
- S. Klabnik y C. Nichols — *The Rust Programming Language* — [gratis online](https://doc.rust-lang.org/book/).
- B. Kernighan y D. Ritchie — *The C Programming Language* (2ª ed., Prentice Hall).
- C. J. Date — *SQL and Relational Theory* (3ª ed., O'Reilly).
- J. Lockhart — *Modern PHP* (O'Reilly).

---

> [⏮️ Clase 106](../../parte-6-datos-y-estructuras/106-otros-formatos-y-persistencia-csv-yaml-binarios-bases-de-datos/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 108 ⏭️](../../parte-7-paradigmas/108-imperativo-y-estructurado/README.md)
