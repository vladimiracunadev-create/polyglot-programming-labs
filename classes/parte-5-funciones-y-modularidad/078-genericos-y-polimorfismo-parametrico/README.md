# Clase 078 — Genéricos y polimorfismo paramétrico

> Parte **5 — Funciones y modularidad** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Escribir una función **una sola vez** y que sirva para muchos tipos sin perder la comprobación del compilador. La función `mayor(a, b)` que devuelve el mayor de dos valores no debería reescribirse para enteros, luego para reales, luego para texto: la lógica —«compara y devuelve el más grande»— es idéntica; lo único que cambia es el tipo de lo que entra. El **polimorfismo paramétrico** es el mecanismo que captura exactamente esa idea: parametrizar el código por un *tipo* como se parametriza por un valor. Donde una función normal deja un hueco para un número (`a`), una función genérica deja además un hueco para un tipo (`T`), y ese hueco se rellena en el momento de la llamada.

Robert Sebesta, en *Concepts of Programming Languages*, distingue el polimorfismo *ad hoc* (la sobrecarga, donde cada tipo tiene su propia implementación) del polimorfismo *paramétrico*, donde **un solo cuerpo de código** opera sobre un rango de tipos gracias a un parámetro de tipo. La diferencia es profunda: en la sobrecarga escribes N funciones que casualmente comparten nombre; en el paramétrico escribes una función que el compilador especializa. Benjamin Pierce lo lleva al terreno teórico en *Types and Programming Languages*: una función genuinamente paramétrica no puede *inspeccionar* el tipo que recibe —solo puede hacer con él lo que su firma promete—, y de esa restricción nace la *parametricidad*, la propiedad de que el comportamiento es uniforme para todos los tipos.

El objetivo hondo de la clase es ver que «una función para todos los tipos» no significa «renunciar a los tipos». Al contrario: en los lenguajes estáticos, `mayor<T>` sigue exigiendo que `T` sea **comparable**, y esa restricción se verifica antes de ejecutar. Genéricos bien hechos son reutilización *con* seguridad, no *a costa* de ella.

## 🧩 Situación

Imagina una biblioteca de utilidades donde alguien necesitó el máximo de dos enteros y escribió `maxInt`. Meses después, otro necesitó el de dos `double` y copió la función cambiando el tipo: nació `maxDouble`. Luego llegó `maxString`, `maxLong`, `maxFloat`... Un día se descubre que todas tenían el mismo error sutil en el caso de empate, y hay que corregirlo en seis sitios idénticos. Esa duplicación es la que Robert Martin llama deuda en *Clean Code*: el mismo cambio repetido en muchos lugares es un imán de bugs. El polimorfismo paramétrico borra el problema de raíz: `mayor<T: Comparable>(a, b)` se escribe **una vez**, sirve para todo tipo que sepa compararse, y el compilador rechaza en el sitio de la llamada cualquier tipo que no cumpla el contrato. Una corrección, un cuerpo, cero copias.

## 🧮 Modelo

- **Entrada** (stdin): una línea `a b` (dos enteros)
- **Salida** (stdout): `max=<el mayor>`
- **Regla:** max<T>(a, b) = a si a>b, si no b

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3 7` | `max=7` |
| `9 2` | `max=9` |
| `5 5` | `max=5` |

## 📖 Definiciones y características

- **Genérico** — una función o un tipo parametrizado por otro tipo, como `mayor<T>`. La `T` es una variable de tipo: un hueco que el llamador rellena. Lo esencial es que da reutilización **sin** perder la comprobación estática; el compilador sigue sabiendo, en cada llamada concreta, qué es `T`.
- **Polimorfismo paramétrico** — la capacidad de que un mismo cuerpo de código opere sobre muchos tipos. Sebesta lo contrapone al polimorfismo de subtipos (herencia): allí la variedad viene de la jerarquía de clases; aquí viene de dejar el tipo abierto como parámetro. No hay `if es_entero... else si es_texto`; hay un único camino que funciona para todos.
- **Restricción de tipo (constraint / bound)** — la condición que debe cumplir `T` para que el cuerpo tenga sentido. Comparar con `>` exige que `T` sea *comparable*; por eso Java escribe `T extends Comparable<T>`, C# escribe `where T : IComparable<T>`, Rust `T: PartialOrd` y Go `T cmp.Ordered`. Sin restricción, el compilador no dejaría usar `>`, porque no todo tipo sabe compararse.
- **Inferencia de tipo genérico** — el compilador deduce `T` a partir de los argumentos, así que rara vez hay que escribirlo. Al llamar `mayor(3, 7)`, `T` se resuelve a entero solo; no hace falta `mayor<int>(3, 7)`.
- **Borrado de tipos (type erasure) vs. reificación** — dos formas de implementar los genéricos. Java los **borra**: en tiempo de ejecución no queda rastro de `T` (todo es `Object` bajo el capó), lo que Joshua Bloch explica en *Effective Java* al advertir sobre arreglos genéricos. C# los **reifica**: la información de `T` sobrevive en runtime y puedes preguntarla. Rust hace **monomorfización**: genera una copia especializada del código por cada tipo usado, como si hubieras escrito `maxInt` y `maxDouble` a mano, pero sin la duplicación en el fuente.

## 📐 Algoritmo (pseudocódigo neutral)

```text
FUNCION max<T comparable>(a,b): DEVOLVER a SI a>b SINO b
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys


def mayor(a, b):
    return a if a > b else b


a, b = map(int, sys.stdin.readline().split())
print(f"max={mayor(a, b)}")
```

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

// JS es dinámico: la función ya sirve para cualquier tipo comparable.
function mayor(a, b) {
  return a > b ? a : b;
}

const [a, b] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`max=${mayor(a, b)}`);
```

🧬 **El mismo programa en la familia JavaScript / web:** [Dart · ActionScript](primos.md#javascript-web)

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

function mayor<T>(a: T, b: T): T {
  return a > b ? a : b;
}

const [a, b]: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`max=${mayor(a, b)}`);
```

🧬 **El mismo programa en la familia JavaScript / web:** [Dart · ActionScript](primos.md#javascript-web)

### Java · [`java/Main.java`](implementaciones/java/Main.java) · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    static <T extends Comparable<T>> T mayor(T a, T b) {
        return a.compareTo(b) > 0 ? a : b;
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        int a = Integer.parseInt(p[0]);
        int b = Integer.parseInt(p[1]);
        System.out.println("max=" + mayor(a, b));
    }
}
```

🧬 **El mismo programa en la familia JVM:** [Kotlin · Scala · Groovy · Clojure](primos.md#jvm)

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;

T Mayor<T>(T a, T b) where T : IComparable<T> => a.CompareTo(b) > 0 ? a : b;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
int a = int.Parse(p[0]);
int b = int.Parse(p[1]);
Console.WriteLine($"max={Mayor(a, b)}");
```

🧬 **El mismo programa en la familia .NET:** [F# · VB.NET](primos.md#dotnet)

### Go · [`go/main.go`](implementaciones/go/main.go) · `go run main.go`

```go
package main

import (
	"bufio"
	"cmp"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func mayor[T cmp.Ordered](a, b T) T {
	if a > b {
		return a
	}
	return b
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	f := strings.Fields(line)
	a, _ := strconv.Atoi(f[0])
	b, _ := strconv.Atoi(f[1])
	fmt.Printf("max=%d\n", mayor(a, b))
}
```

🧬 **El mismo programa en la familia Sistemas:** [Zig · Nim · D](primos.md#sistemas)

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn mayor<T: PartialOrd>(a: T, b: T) -> T {
    if a > b { a } else { b }
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let v: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    println!("max={}", mayor(v[0], v[1]));
}
```

🧬 **El mismo programa en la familia Sistemas:** [Zig · Nim · D](primos.md#sistemas)

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

/* C no tiene genéricos: se escribe una función por tipo (o macros). */
long mayor(long a, long b) {
    return a > b ? a : b;
}

int main(void) {
    long a, b;
    if (scanf("%ld %ld", &a, &b) != 2) return 1;
    printf("max=%ld\n", mayor(a, b));
    return 0;
}
```

🧬 **El mismo programa en la familia C / llaves:** [C++ · Objective-C](primos.md#c-llaves)

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL: max() es polimórfico incorporado.
WITH pares(a, b) AS (VALUES (3, 7), (9, 2), (5, 5))
SELECT printf('max=%d', max(a, b)) AS resultado FROM pares;
```

🧬 **El mismo programa en la familia Lógica y declarativa:** [Prolog · Datalog](primos.md#logica-declarativa)

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
// PHP es dinámico: la función sirve para cualquier tipo comparable.
function mayor($a, $b) {
    return $a > $b ? $a : $b;
}

[$a, $b] = preg_split('/\s+/', trim(fgets(STDIN)));
echo "max=" . mayor((int) $a, (int) $b) . "\n";
```

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Ejemplo trabajado — del stdin a la salida

Sigamos el primer caso de `casos.json` (`stdin = "3 7"`, `esperado = "max=7"`) por tres lenguajes que resuelven la genericidad con filosofías opuestas.

**Python.** No hay parámetro de tipo por ningún lado: `def mayor(a, b)` acepta lo que sea. La línea `a, b = map(int, sys.stdin.readline().split())` produce `a=3`, `b=7`, y `mayor(3, 7)` evalúa `3 if 3 > 7 else 7`. Como `3 > 7` es falso, devuelve `7`, y `print(f"max={7}")` emite `max=7`. Python es genérico «gratis» por *duck typing*: la función corre con cualquier cosa que soporte `>`. Pero esa libertad no es polimorfismo paramétrico *verificado*: si le pasaras un entero y un texto, `mayor(3, "7")` no fallaría al definir la función, sino que reventaría en tiempo de ejecución con un `TypeError`. El contrato «T debe ser comparable» existe solo como esperanza, no como comprobación.

**Java.** Aquí `T` es explícito: la firma `<T extends Comparable<T>> T mayor(T a, T b)` declara el parámetro de tipo *y* su restricción. El cuerpo no usa `>` (los objetos de Java no lo soportan) sino `a.compareTo(b) > 0`, que es justo lo que la restricción `Comparable<T>` garantiza que existe. Con `a=3`, `b=7`, la llamada `mayor(a, b)` infiere `T = Integer` (los `int` se autoboxean), evalúa `Integer.valueOf(3).compareTo(7)` que da negativo, y devuelve `7`. El detalle histórico clave: por el **borrado de tipos** (*type erasure*), en el bytecode compilado `T` ya no existe —la función opera sobre `Comparable` y hace un cast a `Object`—, de modo que en tiempo de ejecución Java no sabe que aquello «era un genérico de Integer». Bloch dedica varios ítems de *Effective Java* a las consecuencias de este borrado.

**Go.** Los genéricos llegaron a Go en la versión 1.18, y aquí se ven en `func mayor[T cmp.Ordered](a, b T) T`. La restricción `cmp.Ordered` es una *constraint* de la biblioteca estándar que agrupa todos los tipos ordenables (enteros, reales, cadenas), y precisamente por eso el cuerpo **sí** puede usar `if a > b` directamente. Con `a=3`, `b=7`, `T` se infiere como `int`, `3 > 7` es falso, la función devuelve `7`, y `fmt.Printf("max=%d\n", 7)` imprime `max=7`. El tercer caso, `5 5`, es la prueba del empate: `5 > 5` es falso, así que devuelve el segundo `5` —igual en los tres lenguajes—, produciendo `max=5`. Tres caminos hacia la misma salida: uno sin tipos (Python), uno con tipos borrados en runtime (Java), uno con tipos y restricción explícita (Go).

## 🔬 Comparación

| Lenguaje | Cómo expresa la genericidad |
|---|---|
| Python | Sin parámetro de tipo; genérico por *duck typing*, verificado solo en ejecución. |
| JavaScript | Igual que Python: dinámico, sin genéricos; la función sirve para todo lo comparable. |
| TypeScript | `<T>` real en el fuente, pero **borrado** al compilar a JS: no queda tipo en runtime. |
| Java | `<T extends Comparable<T>>`; genéricos con **type erasure**, sin info de tipo en runtime. |
| C# | `<T> where T : IComparable<T>`; genéricos **reificados**, `T` disponible en tiempo de ejecución. |
| Go | `[T cmp.Ordered]`; parámetros de tipo y *constraints* desde Go 1.18. |
| Rust | `<T: PartialOrd>`; *trait bounds* y **monomorfización** (una copia por tipo usado). |
| C | No tiene genéricos reales: una función por tipo, macros, `void*` o `_Generic` de C11. |
| SQL | `max()` es una función polimórfica incorporada; no defines el genérico, ya viene dado. |
| PHP | Dinámico como Python/JS; sin parámetros de tipo, comparación resuelta en ejecución. |

La síntesis la ilumina la distinción de Sebesta: los estáticos (Java, C#, Go, Rust, TS) comprueban la restricción de `T` *antes* de ejecutar, aunque luego difieran en si el tipo sobrevive a runtime (borrado en Java/TS, reificado en C#, monomorfizado en Rust); los dinámicos (Python, JS, PHP) ofrecen la misma reutilización pero pagan la comprobación en tiempo de ejecución. Y C, en el otro extremo, recuerda que el polimorfismo paramétrico es un lujo del sistema de tipos: sin él, la única salida honesta es escribir una función por tipo. Pierce diría que solo los primeros garantizan *parametricidad* real: que el comportamiento es demostrablemente uniforme para todos los tipos que cumplen el contrato.

## 🧬 El concepto en la familia

En **Kotlin** la firma sería `fun <T : Comparable<T>> mayor(a: T, b: T)`, casi calcada a Java pero sin el `extends`. En **Haskell**, el sistema de tipos hace la restricción explícita y elegante: `mayor :: Ord a => a -> a -> a`, donde `Ord a =>` es literalmente «para todo `a` que pertenezca a la clase de los ordenables»; es la misma idea que `T: PartialOrd` de Rust o `cmp.Ordered` de Go. **Swift** usa `func mayor<T: Comparable>(_ a: T, _ b: T) -> T`, con la restricción tras los dos puntos como Rust. Reconocer el patrón —dónde va la variable de tipo, cómo se escribe su restricción— permite leer una firma genérica en cualquier lenguaje de la familia en segundos.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 078
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Usar `Object` en vez de genéricos (estilo Java pre-2004)** → causa: antes de los genéricos se guardaba todo como `Object` y se hacía cast al sacarlo, perdiendo la seguridad de tipos y arriesgando un `ClassCastException` en runtime → solución: parametrizar con `<T extends Comparable<T>>` y dejar que el compilador impida el error.
- **Olvidar la restricción del tipo** → causa: escribir `mayor<T>` y usar `a > b` en un lenguaje donde no todo `T` es comparable; el compilador rechaza el `>` porque no puede garantizar que exista → solución: acotar con `Comparable`, `IComparable`, `PartialOrd` o `cmp.Ordered` según el lenguaje.
- **Creer que Java conoce `T` en runtime** → causa: intentar `if (a instanceof T)` o crear `new T[]`, que el *type erasure* prohíbe porque `T` ya no existe tras compilar → solución: pasar un `Class<T>` explícito si de verdad necesitas el tipo en ejecución, o usar C# si necesitas reificación.
- **Comparar objetos con `>` en vez de `compareTo`** → causa: en Java/C# los tipos de referencia no admiten `>`; el operador solo vale para primitivos → solución: usar `a.compareTo(b) > 0`, que es lo que la restricción `Comparable` garantiza.

## ❓ Preguntas frecuentes

- **¿Genéricos o sobrecarga?** Los genéricos evitan duplicar cuando la lógica es idéntica y solo cambia el tipo; la sobrecarga sirve cuando el comportamiento debe ser *distinto* por tipo. `mayor` es un caso claro de genérico: la comparación es la misma para todos.
- **¿Python tiene genéricos?** Su tipado dinámico ya es «genérico» en la práctica: cualquier función acepta cualquier tipo. Para las herramientas de análisis estático existen `TypeVar` y la sintaxis `def mayor[T](a: T, b: T)` (Python 3.12+), pero esas anotaciones no cambian la ejecución: no hay comprobación en tiempo de corrida.
- **¿Qué es la monomorfización de Rust?** Que el compilador genera una versión especializada del código por cada tipo concreto con el que llamas la función. `mayor(3, 7)` produce una copia para `i64`; `mayor(1.0, 2.0)` produciría otra para `f64`. El resultado es tan rápido como si las hubieras escrito a mano, sin coste de despacho en runtime.
- **¿Por qué C# reifica y Java borra?** Es una decisión de diseño de plataforma: la JVM introdujo genéricos manteniendo compatibilidad con bytecode antiguo, y el borrado fue el precio; el CLR de .NET añadió soporte de genéricos al propio runtime, así que `T` sobrevive y puedes inspeccionarlo con reflexión.

## 🔗 Referencias

**Libros de la parte:**

- R. W. Sebesta — *Concepts of Programming Languages* (11ª ed., Pearson), cap. 9 «Subprograms» y §9.9 sobre polimorfismo paramétrico.
- B. C. Pierce — *Types and Programming Languages* (MIT Press), cap. 23 «Universal Types» (polimorfismo paramétrico y parametricidad).
- R. C. Martin — *Clean Code* (Prentice Hall), cap. 3 «Functions».

**Libros de los lenguajes del núcleo:**

- L. Ramalho — *Fluent Python* (2ª ed., O'Reilly), cap. sobre *type hints* y `TypeVar`.
- M. Haverbeke — *Eloquent JavaScript* (3ª ed.) — [gratis online](https://eloquentjavascript.net/).
- B. Cherny — *Programming TypeScript* (O'Reilly), cap. 6 «Advanced Types» (genéricos).
- J. Bloch — *Effective Java* (3ª ed., Addison-Wesley), ítems 26-31 «Generics».
- J. Skeet — *C# in Depth* (4ª ed., Manning), cap. sobre genéricos y reificación.
- A. Donovan y B. Kernighan — *The Go Programming Language* (Addison-Wesley); genéricos añadidos en Go 1.18.
- S. Klabnik y C. Nichols — *The Rust Programming Language* — [gratis online](https://doc.rust-lang.org/book/), cap. 10 «Generic Types, Traits, and Lifetimes».
- B. Kernighan y D. Ritchie — *The C Programming Language* (2ª ed., Prentice Hall).
- C. J. Date — *SQL and Relational Theory* (3ª ed., O'Reilly).
- J. Lockhart — *Modern PHP* (O'Reilly).

---

> [⏮️ Clase 077](../../parte-5-funciones-y-modularidad/077-multiples-retornos-y-desestructuracion/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 079 ⏭️](../../parte-5-funciones-y-modularidad/079-paso-por-valor/README.md)
