# Clase 115 — Funcional II: composición, currying y aplicación parcial

> Parte **7 — Paradigmas** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

En la clase anterior aislaste dos ideas del estilo funcional: la inmutabilidad y la función pura. Aquí das el paso que las vuelve productivas. Una función pura es un ladrillo; la **composición** es el mortero que une ladrillos para levantar muros sin abrir cada uno. Van Roy y Haridi, en el modelo declarativo de *Concepts, Techniques, and Models of Computer Programming*, insisten en que la potencia de este estilo no está en las funciones sueltas sino en la libertad de combinarlas: si `f` y `g` son puras, `f ∘ g` también lo es, y esa clausura bajo composición es lo que permite razonar sobre programas grandes como si fueran expresiones algebraicas.

SICP dedica la sección 1.3 entera a los **procedimientos de orden superior**: procedimientos que reciben otros procedimientos como argumentos y que devuelven procedimientos como valor. Abelson y Sussman lo presentan como el mecanismo que nos deja subir un peldaño de abstracción: en vez de escribir `2*n+1` una y otra vez, nombramos `doblar` e `incrementar` y construimos con esos nombres. El **currying** —bautizado por Haskell Curry, aunque la idea es de Moses Schönfinkel— y la **aplicación parcial** son la otra cara de la misma moneda: transformar una función de varios argumentos en una cadena de funciones de uno, de modo que fijar el primer argumento ya produce una función nueva y especializada.

El objetivo concreto de hoy es modesto en tamaño pero central en concepto: componer `doblar` e `incrementar` en una única función `compuesta`, aplicarla a un entero leído de `stdin` y observar cómo cada lenguaje del núcleo expresa —o esquiva— la composición explícita. Verás que el orden importa (`incrementar ∘ doblar` no es `doblar ∘ incrementar`) y por qué el estilo funcional trata a las funciones como valores de primera clase.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Componer dos funciones.
2. Aplicar la composición a un valor.
3. Reconocer la aplicación parcial/currying.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Composición | f(g(x)): encadenar funciones |
| 2 | Funciones pequeñas | Construir a partir de piezas |
| 3 | Currying | Funciones que devuelven funciones |

## 📖 Definiciones y características

- **Composición de funciones** — combinar funciones: `(f ∘ g)(x) = f(g(x))`. Clave: construir con piezas.
- **Currying** — transformar una función de varios argumentos en una cadena de funciones de uno. Clave: aplicación parcial.
- **Aplicación parcial** — fijar algunos argumentos y obtener una función nueva. Clave: reutilización.

La composición `(f ∘ g)(x) = f(g(x))` tiene una propiedad que SICP explota sin descanso: es **asociativa** y tiene un elemento neutro (la función identidad). Eso significa que podemos encadenar tantas funciones como queramos sin preocuparnos por dónde ponemos los paréntesis, igual que sumamos números. Cuando Abelson y Sussman construyen abstracciones como `compose` en la sección 1.3, lo que persiguen es que el programador deje de pensar en *pasos* y empiece a pensar en *tuberías*: el dato entra por un extremo y sale transformado por el otro, y cada tramo de la tubería es una función pequeña, probada y reutilizable por separado.

El currying no es una curiosidad académica. Sebesta, en el capítulo 15 de *Concepts of Programming Languages*, lo describe como una consecuencia natural de tratar las funciones como valores: si una función `sumar(a, b)` es en realidad `sumar(a)(b)`, entonces `sumar(10)` ya es una función útil —"suma diez a lo que venga"— sin haber terminado de aplicar todos los argumentos. Esa es la **aplicación parcial**: congelar parte de la entrada y quedarnos con una función más especializada. En lenguajes como Haskell el currying es la forma por defecto de toda función; en los del núcleo de este curso hay que provocarlo con closures o con métodos de biblioteca, pero la intuición es idéntica: una función que aún espera argumentos sigue siendo un valor que podemos nombrar, pasar y componer.

Van Roy y Haridi remarcan que este poder expresivo no sale gratis en legibilidad: una tubería de cinco composiciones anónimas puede ser tan opaca como un bucle imperativo mal escrito. La disciplina consiste en nombrar los tramos intermedios cuando aportan significado y componer solo cuando la cadena se lee como una frase.

## 🧩 Situación

Imagina el pipeline de ingesta de un sistema de facturación. Cada importe que entra debe pasar por una serie de transformaciones: normalizar la moneda, aplicar el impuesto, redondear a dos decimales, formatear para el recibo. La tentación imperativa es escribir un método de cuarenta líneas que haga las cuatro cosas seguidas. El problema aparece a los seis meses, cuando el fisco cambia el redondeo: hay que localizar el fragmento exacto dentro del método, tocarlo con cuidado de no romper lo demás y volver a probar el bloque entero.

El enfoque funcional descompone ese método en cuatro funciones puras independientes y las **compone** en una tubería `formatear ∘ redondear ∘ aplicarImpuesto ∘ normalizar`. Cambiar el redondeo es sustituir un solo tramo; el resto de la tubería no se entera. En esta clase reducimos ese pipeline a su mínima expresión reconocible —`incrementar ∘ doblar`, es decir `2n+1`— para que el mecanismo quede a la vista sin ruido de dominio. En vez de escribir `x*2+1` a mano, componemos dos piezas nombradas y aplicamos la tubería resultante al número que llega por `stdin`.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n`
- **Salida** (stdout): `resultado=<2n+1>` (doblar y luego incrementar)
- **Regla:** resultado = incrementar(doblar(n)) = 2n + 1

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `resultado=11` |
| `0` | `resultado=1` |
| `3` | `resultado=7` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
doblar(x)=2x ; inc(x)=x+1 ; compuesta = inc ∘ doblar ; ESCRIBIR compuesta(n)
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys


def doblar(x):
    return x * 2


def incrementar(x):
    return x + 1


n = int(sys.stdin.readline())
print(f"resultado={incrementar(doblar(n))}")
```

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const doblar = (x) => x * 2;
const incrementar = (x) => x + 1;
const compuesta = (x) => incrementar(doblar(x));

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`resultado=${compuesta(n)}`);
```

🧬 **El mismo programa en la familia JavaScript / web:** [Dart · ActionScript](primos.md#javascript-web)

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const doblar = (x: number): number => x * 2;
const incrementar = (x: number): number => x + 1;
const compuesta = (x: number): number => incrementar(doblar(x));

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`resultado=${compuesta(n)}`);
```

🧬 **El mismo programa en la familia JavaScript / web:** [Dart · ActionScript](primos.md#javascript-web)

### Java · [`java/Main.java`](implementaciones/java/Main.java) · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.function.IntUnaryOperator;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        IntUnaryOperator doblar = x -> x * 2;
        IntUnaryOperator incrementar = x -> x + 1;
        IntUnaryOperator compuesta = doblar.andThen(incrementar);
        System.out.println("resultado=" + compuesta.applyAsInt(n));
    }
}
```

🧬 **El mismo programa en la familia JVM:** [Kotlin · Scala · Groovy · Clojure](primos.md#jvm)

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;

int n = int.Parse(Console.In.ReadToEnd().Trim());
Func<int, int> doblar = x => x * 2;
Func<int, int> incrementar = x => x + 1;
Func<int, int> compuesta = x => incrementar(doblar(x));
Console.WriteLine($"resultado={compuesta(n)}");
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

func doblar(x int) int      { return x * 2 }
func incrementar(x int) int { return x + 1 }

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	n, _ := strconv.Atoi(strings.TrimSpace(line))
	fmt.Printf("resultado=%d\n", incrementar(doblar(n)))
}
```

🧬 **El mismo programa en la familia Sistemas:** [Zig · Nim · D](primos.md#sistemas)

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn doblar(x: i64) -> i64 {
    x * 2
}

fn incrementar(x: i64) -> i64 {
    x + 1
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    println!("resultado={}", incrementar(doblar(n)));
}
```

🧬 **El mismo programa en la familia Sistemas:** [Zig · Nim · D](primos.md#sistemas)

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

long doblar(long x) { return x * 2; }
long incrementar(long x) { return x + 1; }

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    printf("resultado=%ld\n", incrementar(doblar(n)));
    return 0;
}
```

🧬 **El mismo programa en la familia C / llaves:** [C++ · Objective-C](primos.md#c-llaves)

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL: se anidan las expresiones/funciones.
WITH nums(n) AS (VALUES (5), (0), (3))
SELECT printf('resultado=%d', (n * 2) + 1) AS resultado FROM nums;
```

🧬 **El mismo programa en la familia Lógica y declarativa:** [Prolog · Datalog](primos.md#logica-declarativa)

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
$doblar = fn($x) => $x * 2;
$incrementar = fn($x) => $x + 1;
$compuesta = fn($x) => $incrementar($doblar($x));

$n = (int) trim(fgets(STDIN));
echo "resultado=" . $compuesta($n) . "\n";
```

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🧪 Laboratorio guiado — recorrido del código

Sigue el dato desde `stdin` hasta la línea impresa y comprueba, caso por caso, que cada implementación reproduce lo que declara [`casos.json`](casos.json): para `stdin` `5` se espera `resultado=11`, para `0` se espera `resultado=1` y para `3`, `resultado=7`. Todos salen de la misma fórmula `2n+1`, pero cada lenguaje construye la composición de un modo distinto.

**Python — composición por anidamiento.** El archivo define `doblar(x)` que devuelve `x * 2` e `incrementar(x)` que devuelve `x + 1`. La línea clave es `print(f"resultado={incrementar(doblar(n))}")`. Léela de dentro hacia afuera, que es como se evalúa: para `n = 5`, primero `doblar(5)` produce `10`, y ese `10` alimenta `incrementar`, que da `11`. La composición aquí es puro **anidamiento de llamadas**: `f(g(x))` escrito literalmente. No hay operador de composición porque Python no lo trae de serie; el orden se lee de derecha a izquierda en el texto, pero de dentro hacia afuera en la ejecución. Para `n = 0`, `doblar(0)` es `0` e `incrementar(0)` es `1`; para `n = 3`, `6` seguido de `7`. Los tres casos de `casos.json` cuadran.

**Java — composición explícita con `andThen`.** Aquí el código no anida llamadas: construye una función nueva. Declara `doblar` e `incrementar` como `IntUnaryOperator` (funciones que van de `int` a `int`) y luego escribe `IntUnaryOperator compuesta = doblar.andThen(incrementar);`. Esta es la línea que merece atención. `andThen` es la composición *hacia adelante*: `doblar.andThen(incrementar)` significa "aplica `doblar` y **luego** pasa el resultado a `incrementar`", exactamente `incrementar ∘ doblar`. Fíjate en que `compuesta` es un valor —una función guardada en una variable— antes de aplicarse a nada; solo cuando se ejecuta `compuesta.applyAsInt(n)` entra `n = 5` y sale `11`. Ese `andThen` de la biblioteca `java.util.function` es la prueba de que Java trata las funciones como objetos de primera clase. Si hubiéramos escrito `incrementar.andThen(doblar)` obtendríamos `2(n+1)`, es decir `12` para `n = 5`: el orden es semántico, no cosmético.

**SQL — la nota ilustrativa.** El bloque marcado como ilustrativo no compone funciones nombradas; anida las **expresiones** directamente: `(n * 2) + 1`. Recorre la tabla `nums(n)` con los valores `5`, `0` y `3` —los mismos `stdin` de `casos.json`— y para cada fila calcula `printf('resultado=%d', (n * 2) + 1)`, produciendo `resultado=11`, `resultado=1` y `resultado=7`. Es la composición reducida a su esencia aritmética: sin funciones de primera clase, la anidación de expresiones ya *es* composición, solo que resuelta por el motor en una sola pasada. Por eso el verificador la trata aparte: no lee `stdin`, sino que lleva los casos incrustados en el `VALUES`.

Contrasta las tres formas: Python compone en el punto de uso, Java compone *antes* de usar y guarda la tubería como valor reutilizable, y SQL disuelve la composición en la expresión. Las tres llegan al mismo `2n+1`, que es justo lo que verifica `casos.json`.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Composición explícita `inc(doblar(n))` o con operador de composición. |
| Semántica | El orden importa: doblar primero, luego incrementar. |
| Paradigmática | SQL anida funciones/expresiones. |

La diferencia real entre los lenguajes no está en si pueden componer —todos pueden— sino en si la composición es un **valor ciudadano** o solo una forma de escribir llamadas. Java y C# exponen la composición como operación de biblioteca: `andThen`/`compose` en Java, la delegación `Func<int,int>` en C#, que permiten guardar la tubería en una variable, pasarla a otro método o meterla en una lista de transformaciones. Go y C, en el otro extremo, no tienen operador ni método de composición idiomático, así que anidan las llamadas `incrementar(doblar(n))` como Python; en Go podrías construir una closure `func(x int) int { return incrementar(doblar(x)) }`, pero el lenguaje no te empuja a ello.

Hay un matiz de dirección que confunde a menudo. El operador matemático `∘` y el `compose` de muchas bibliotecas van de *derecha a izquierda* (`f.compose(g)` es `f(g(x))`), mientras que `andThen`/pipe van de *izquierda a derecha* (`g.andThen(f)` es también `f(g(x))` pero se lee en orden de ejecución). El resultado numérico es el mismo, pero elegir mal el método invierte el orden y `casos.json` deja de cuadrar: `resultado=12` en lugar de `11` para la entrada `5`. Por eso conviene leer siempre la firma: no basta con que compile, hay que saber qué función se aplica primero.

## 🧬 El concepto en la familia

En Haskell la composición es un operador de primera clase: `(inc . doblar) n` usa el punto `.`, que es literalmente `∘`, y como toda función está currificada por defecto, `inc . doblar` es una función nueva sin necesidad de nombrar el argumento (estilo *point-free*). En F# y Elm el operador `>>` compone hacia adelante y `<<` hacia atrás. En los lenguajes del núcleo el patrón sobrevive aunque cambie de vestido: los `Streams` de Java, los métodos encadenados de LINQ en C#, las tuberías de iteradores en Rust (`.map().map()`) son todas composiciones de transformaciones. El hilo conductor, que SICP formula en 1.3, es que una función que devuelve o recibe funciones es la unidad mínima de abstracción reutilizable, y la composición es su operación natural.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 115
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Invertir el orden de composición** → causa: confundir `andThen` con `compose`, o leer `f ∘ g` como "primero f". El resultado cambia: `incrementar ∘ doblar` da `2n+1`, pero `doblar ∘ incrementar` da `2(n+1)`. → remedio: fija el contrato (`doblar` va primero) y verifica un caso a mano; para `n=5` la salida correcta es `11`, no `12`.
- **Componer funciones incompatibles** → causa: la salida de una no es del tipo que la otra espera (componer una función que devuelve texto con otra que espera un número). → remedio: comprueba que el tipo de retorno de `g` coincide con el parámetro de `f`; en Java/Rust el compilador lo detecta, en Python o JS el error aparece en ejecución, así que lee la cadena como una tubería y confirma que cada junta encaja.
- **Crear la composición dentro del bucle en vez de fuera** → causa: reconstruir la función compuesta en cada iteración desperdicia trabajo. → remedio: la composición es un valor; constrúyela una vez (como hace Java con `compuesta`) y reutilízala.

## ❓ Preguntas frecuentes

- **¿Componer o anidar llamadas es lo mismo?** Producen el mismo resultado, pero conceptualmente difieren: anidar `f(g(x))` aplica y descarta; componer construye una función `f ∘ g` que existe como valor antes de aplicarse. Cuando necesitas *pasar* la tubería a otra parte del programa, la composición explícita gana; cuando solo la usas una vez en el sitio, anidar es más directo.
- **¿Para qué sirve el currying en la práctica?** Para fabricar funciones especializadas fijando parte de la entrada. Una función `descuento(porcentaje, precio)` currificada te deja crear `descuento(0.1)` —"aplica el 10 %"— y reutilizarla sobre miles de precios sin repetir el porcentaje. Es la aplicación parcial que Sebesta describe en el capítulo 15: congelar argumentos para obtener piezas más pequeñas y componibles.
- **¿Por qué SICP insiste tanto en las funciones de orden superior?** Porque son el salto de abstracción que separa "escribir cada cálculo" de "escribir el patrón del cálculo". Componer, pasar y devolver funciones permite capturar patrones (una tubería, un `map`, un `reduce`) una sola vez y aplicarlos en muchos contextos, que es la idea central de la sección 1.3.

## 🔗 Referencias

**Libros de la parte:**

- P. Van Roy y S. Haridi — *Concepts, Techniques, and Models of Computer Programming* (MIT Press) — modelo declarativo y clausura bajo composición.
- H. Abelson y G. J. Sussman — *Structure and Interpretation of Computer Programs* (2ª ed., MIT Press) — sección 1.3, procedimientos de orden superior como argumentos y valores.
- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson) — cap. 15, currying y aplicación parcial en lenguajes funcionales.

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

> [⏮️ Clase 114](../../parte-7-paradigmas/114-funcional-i-inmutabilidad-y-funciones-puras/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 116 ⏭️](../../parte-7-paradigmas/116-funcional-iii-functores-monadas-y-efectos-vision-practica/README.md)
