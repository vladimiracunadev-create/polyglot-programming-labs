# Clase 085 — Funciones de primera clase y como valores

> Parte **5 — Funciones y modularidad** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Dejar de ver la función como una construcción especial del lenguaje y empezar a verla como lo que en muchos lenguajes realmente es: **un valor más**. Decir que las funciones son de **primera clase (first-class)** significa que gozan de los mismos derechos que un número o una cadena: se pueden guardar en una variable, meter en una lista, pasar como argumento a otra función y devolver como resultado. Ese estatus, aparentemente modesto, es el que hace posibles `map`, `filter`, `reduce`, los callbacks, los manejadores de eventos, las tablas de despacho y buena parte de los patrones de diseño clásicos, que dejan de necesitar una jerarquía de clases cuando puedes simplemente pasar la operación como dato.

La idea nuclear la desarrollan Abelson y Sussman en *Structure and Interpretation of Computer Programs* §1.3, dedicada a las **funciones de orden superior** (higher-order procedures): procedimientos que reciben otros procedimientos como argumentos o los devuelven. Su tesis es que limitar qué se puede nombrar y pasar limita el poder expresivo de un lenguaje; conceder a las funciones el estatus de primera clase elimina esa restricción y permite capturar patrones generales —«aplicar una operación a cada elemento», «combinar mediante una operación»— como abstracciones reutilizables. La operación deja de estar cableada en el código y pasa a ser un parámetro.

Luciano Ramalho lo resume en *Fluent Python* con la frase que da nombre al fenómeno: en Python las funciones son *objetos* de primera clase, instancias que se pueden crear en tiempo de ejecución, asignar, almacenar en estructuras y pasar como argumento. El objetivo profundo de la clase es interiorizar que `aplicar(suma, 3, 4)` no es magia: `suma` es un valor que viaja hasta `aplicar`, y dentro se invoca. Reconocer ese mecanismo —y ver cómo cada lenguaje lo modela, desde el puntero a función de C hasta el delegado de C#— es la llave de casi todo el estilo funcional que viene después.

## 🧩 Situación

Escribes una función que recorre una lista de pedidos y aplica un cálculo a cada uno: hoy es «sumar impuesto», mañana «aplicar descuento», la semana que viene «convertir divisa». Sin funciones de primera clase, escribirías tres funciones de recorrido casi idénticas que solo difieren en la línea del medio, o meterías un `switch` gigante con un código por operación. Con funciones como valores, escribes *un solo* recorrido, `procesar(operacion, pedidos)`, y le pasas la operación que toque como argumento. El patrón de iteración se escribe una vez; la operación se decide en el sitio de la llamada. Ese es el dolor que resuelve el estatus de primera clase: no tener que duplicar la estructura de control cada vez que cambia la operación que va dentro.

## 🧮 Modelo

- **Entrada** (stdin): una línea `a b` (dos enteros)
- **Salida** (stdout): `suma=<a+b> producto=<a*b>`
- **Regla:** aplicar(f, a, b) = f(a, b); con f = suma y f = producto

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3 4` | `suma=7 producto=12` |
| `5 5` | `suma=10 producto=25` |
| `0 9` | `suma=9 producto=0` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
FUNCION aplicar(f, a, b): DEVOLVER f(a, b)
ESCRIBIR "suma=" aplicar(suma,a,b) " producto=" aplicar(producto,a,b)
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys


def suma(a, b):
    return a + b


def producto(a, b):
    return a * b


def aplicar(f, a, b):
    return f(a, b)


a, b = map(int, sys.stdin.readline().split())
print(f"suma={aplicar(suma, a, b)} producto={aplicar(producto, a, b)}")
```

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const suma = (a, b) => a + b;
const producto = (a, b) => a * b;
const aplicar = (f, a, b) => f(a, b);

const [a, b] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`suma=${aplicar(suma, a, b)} producto=${aplicar(producto, a, b)}`);
```

🧬 **El mismo programa en la familia JavaScript / web:** [Dart · ActionScript](primos.md#javascript-web)

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

type Op = (a: number, b: number) => number;
const suma: Op = (a, b) => a + b;
const producto: Op = (a, b) => a * b;
const aplicar = (f: Op, a: number, b: number): number => f(a, b);

const [a, b]: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`suma=${aplicar(suma, a, b)} producto=${aplicar(producto, a, b)}`);
```

🧬 **El mismo programa en la familia JavaScript / web:** [Dart · ActionScript](primos.md#javascript-web)

### Java · [`java/Main.java`](implementaciones/java/Main.java) · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.function.IntBinaryOperator;

public class Main {
    static int aplicar(IntBinaryOperator f, int a, int b) {
        return f.applyAsInt(a, b);
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        int a = Integer.parseInt(p[0]);
        int b = Integer.parseInt(p[1]);
        IntBinaryOperator suma = (x, y) -> x + y;
        IntBinaryOperator producto = (x, y) -> x * y;
        System.out.println("suma=" + aplicar(suma, a, b) + " producto=" + aplicar(producto, a, b));
    }
}
```

🧬 **El mismo programa en la familia JVM:** [Kotlin · Scala · Groovy · Clojure](primos.md#jvm)

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;

int Aplicar(Func<int, int, int> f, int a, int b) => f(a, b);

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
int a = int.Parse(p[0]);
int b = int.Parse(p[1]);
Func<int, int, int> suma = (x, y) => x + y;
Func<int, int, int> producto = (x, y) => x * y;
Console.WriteLine($"suma={Aplicar(suma, a, b)} producto={Aplicar(producto, a, b)}");
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

func suma(a, b int) int     { return a + b }
func producto(a, b int) int { return a * b }

func aplicar(f func(int, int) int, a, b int) int {
	return f(a, b)
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	fields := strings.Fields(line)
	a, _ := strconv.Atoi(fields[0])
	b, _ := strconv.Atoi(fields[1])
	fmt.Printf("suma=%d producto=%d\n", aplicar(suma, a, b), aplicar(producto, a, b))
}
```

🧬 **El mismo programa en la familia Sistemas:** [Zig · Nim · D](primos.md#sistemas)

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn suma(a: i64, b: i64) -> i64 {
    a + b
}

fn producto(a: i64, b: i64) -> i64 {
    a * b
}

fn aplicar(f: fn(i64, i64) -> i64, a: i64, b: i64) -> i64 {
    f(a, b)
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let v: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    println!("suma={} producto={}", aplicar(suma, v[0], v[1]), aplicar(producto, v[0], v[1]));
}
```

🧬 **El mismo programa en la familia Sistemas:** [Zig · Nim · D](primos.md#sistemas)

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

long suma(long a, long b) { return a + b; }
long producto(long a, long b) { return a * b; }

long aplicar(long (*f)(long, long), long a, long b) {
    return f(a, b);
}

int main(void) {
    long a, b;
    if (scanf("%ld %ld", &a, &b) != 2) return 1;
    printf("suma=%ld producto=%ld\n", aplicar(suma, a, b), aplicar(producto, a, b));
    return 0;
}
```

🧬 **El mismo programa en la familia C / llaves:** [C++ · Objective-C](primos.md#c-llaves)

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL usa operadores/funciones incorporadas, no funciones como valor.
WITH pares(a, b) AS (VALUES (3, 4), (5, 5), (0, 9))
SELECT printf('suma=%d producto=%d', a + b, a * b) AS resultado FROM pares;
```

🧬 **El mismo programa en la familia Lógica y declarativa:** [Prolog · Datalog](primos.md#logica-declarativa)

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
$suma = fn($a, $b) => $a + $b;
$producto = fn($a, $b) => $a * $b;
function aplicar($f, $a, $b) {
    return $f($a, $b);
}

[$a, $b] = preg_split('/\s+/', trim(fgets(STDIN)));
$a = (int) $a;
$b = (int) $b;
echo "suma=" . aplicar($suma, $a, $b) . " producto=" . aplicar($producto, $a, $b) . "\n";
```

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Ejemplo trabajado — del stdin a la salida

Sigamos el primer caso de `casos.json` (`stdin = "3 4"`, `esperado = "suma=7 producto=12"`) por Python, C y Java, tres formas de responder a la pregunta «¿cómo viaja una función hasta `aplicar`?».

**Python — la función es un objeto.** Tras `a, b = map(int, ...)` tenemos `a=3, b=4`. La clave está en `aplicar(suma, a, b)`: aquí `suma` **sin paréntesis** no es una llamada, es el objeto-función en sí, que se pasa como argumento. Dentro, `aplicar` recibe ese objeto en su parámetro `f` y ejecuta `f(a, b)`, que ahora sí invoca: `suma(3, 4) = 7`. La segunda llamada pasa `producto`, y `f(3, 4)` calcula `12`. El f-string imprime `suma=7 producto=12`. Como explica Ramalho, `suma` es una instancia de primera clase: podrías meterla en una lista `[suma, producto]` y recorrerla, porque no tiene nada de especial frente a otros valores. La distinción crítica es `suma` (el valor) frente a `suma(a, b)` (el resultado de invocarlo); confundirlas es el error número uno del tema.

**C — puntero a función.** C no tiene objetos-función, pero sí su forma de primera clase: el **puntero a función**. La firma de `aplicar` lo declara con la sintaxis característica `long (*f)(long, long)` —«`f` es un puntero a una función que toma dos `long` y devuelve `long`»—. Al llamar `aplicar(suma, a, b)`, el nombre `suma` se convierte automáticamente en la dirección de la función, que se pasa por `f`; dentro, `f(a, b)` la invoca a través del puntero y da `7`. Con `producto`, `12`. Salida: `suma=7 producto=12`. Es el mismo mecanismo conceptual que en Python —pasar la operación como dato— pero expuesto al nivel de la máquina: lo que viaja es una dirección de memoria de código, no un objeto con métodos.

**Java — interfaz funcional.** Java no permite pasar «un método suelto» como valor: todo tiene que ser un objeto. Su solución son las **interfaces funcionales**, interfaces con un único método abstracto que una lambda puede satisfacer. Aquí `IntBinaryOperator` es esa interfaz (su método es `applyAsInt(int, int)`), y `IntBinaryOperator suma = (x, y) -> x + y;` crea un objeto que la implementa. `aplicar` lo recibe como `f` y lo usa con `f.applyAsInt(a, b)`, que para `3, 4` da `7`; con `producto`, `12`. El resultado impreso es idéntico, `suma=7 producto=12`, pero el andamiaje revela la filosofía de Java: la función-como-valor se modela como un objeto que cumple un contrato de un solo método. Los tres lenguajes llevan la operación hasta `aplicar`; solo cambian el envoltorio —objeto, dirección de código o instancia de interfaz—.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Se pasa el nombre desnudo `suma` (Python, JS, Go, Rust, C, PHP) o una lambda a una interfaz (Java `IntBinaryOperator`, C# `Func<>`). C exige la sintaxis de puntero `long (*f)(long, long)`. |
| Semántica | Python, JS, Ruby y PHP tratan la función como un **objeto** de primera clase, creable y almacenable en tiempo de ejecución. C usa un **puntero a función** (sin entorno). Rust distingue el *puntero* `fn(...)` de los *traits* `Fn`/`FnMut`/`FnOnce` para cierres. |
| Semántica | Java y C# no pasan «métodos sueltos»: envuelven la función en una interfaz funcional (`IntBinaryOperator`) o un delegado (`Func<>`); la lambda es azúcar sobre ese objeto. Go pasa valores de función con tipo `func(int, int) int` directamente. |
| Paradigmática | SQL no trata las funciones como valores que se pasan: usa operadores y funciones incorporadas dentro de la consulta; el `a + b` y `a * b` de la CTE cumplen el papel sin pasar `f`. |

La síntesis está en *SICP* §1.3: conceder a las funciones el estatus de primera clase es lo que permite capturar patrones de cómputo como abstracciones. La diferencia entre los diez lenguajes no es *si* pueden pasar operaciones —casi todos pueden, de una forma u otra— sino *qué* viaja por el cable: un objeto (Python), una dirección de código (C), una instancia de interfaz (Java), un delegado (C#) o un valor de función tipado (Go, Rust). Reconocer el envoltorio de cada familia es lo que te deja leer código funcional en un lenguaje que nunca has visto.

## 🧬 El concepto en la familia

En **Ruby**, los métodos no son objetos de primera clase por defecto, pero se obtiene su versión pasable con `method(:suma)`, o se usan `Proc`/bloques y `lambda`, que sí lo son. En **Haskell**, pasar funciones es lo más natural del lenguaje: no hay ninguna ceremonia, y la aplicación parcial hace que `map (+1)` sea idiomático. En **Kotlin**, las funciones son de primera clase y existe la referencia a función con `::suma`, además de lambdas con tipo `(Int, Int) -> Int`. En **Swift**, las funciones son valores tipados y las clausuras se pasan a diario como argumento final (*trailing closure*). El patrón a reconocer en cualquier lenguaje nuevo: ¿se pasa el nombre desnudo, se necesita un operador de referencia (`::`, `method(...)`), o hay que envolverlo en una interfaz/delegado?

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 085
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Llamar la función en vez de pasarla** → causa: escribir `aplicar(suma(a, b), ...)` en lugar de `aplicar(suma, ...)`; lo primero invoca `suma` y pasa el *número* resultante, no la función → solución: pasa el nombre **sin paréntesis**; los paréntesis significan «invócala ahora».
- **Firmas incompatibles con lo que espera la de orden superior** → causa: pasar una función cuya forma no encaja con la que `aplicar` invocará (número o tipo de parámetros distinto) → solución: verifica que la función pasada cumple exactamente el tipo esperado (`IntBinaryOperator`, `fn(i64, i64) -> i64`, `long (*)(long, long)`).
- **En C, olvidar que el nombre decae a puntero** → causa: intentar `&aplicar` o dudar de si hace falta `&suma`; el nombre de una función ya decae a su dirección → solución: pasa `suma` a secas; `&suma` también funciona, pero el nombre desnudo es suficiente e idiomático.
- **Esperar que Java pase un método suelto** → causa: intentar pasar `suma` como si fuera un valor cuando es un método → solución: usa una interfaz funcional (`IntBinaryOperator`, `Function<>`) con una lambda o una referencia a método (`Math::max`), que es como Java modela la función-como-valor.

## ❓ Preguntas frecuentes

- **¿Los callbacks son esto?** Sí: un callback es exactamente una función de primera clase que pasas a otra parte del programa para que la ejecute más tarde —al llegar un evento, al completarse una operación asíncrona—. El mecanismo que estudias aquí es la base de toda la programación orientada a eventos.
- **¿C tiene funciones de primera clase?** Parcialmente. Con punteros a función puedes guardarlas en variables, pasarlas y devolverlas, así que cumplen buena parte del criterio; lo que les falta es **capturar entorno** (no hay cierres), por lo que el estado hay que pasarlo aparte, como se vio en la clase de cierres.
- **¿Qué diferencia hay entre función de primera clase y de orden superior?** «Primera clase» describe el estatus de la función *como valor* (se puede pasar, guardar, devolver); «orden superior» describe una función que *recibe o devuelve* otras funciones. `aplicar` es de orden superior precisamente porque las funciones son de primera clase.
- **¿Por qué Java y C# necesitan tanto andamiaje (interfaces, delegados)?** Porque son lenguajes donde, históricamente, todo valor pasable era un objeto; modelan la función-como-valor como un objeto que implementa un contrato de un método (`IntBinaryOperator`) o como un tipo delegado (`Func<>`). Las lambdas son azúcar sintáctico sobre ese objeto.

## 🔗 Referencias

**Libros de la parte:**

- H. Abelson y G. J. Sussman — *Structure and Interpretation of Computer Programs* (2ª ed., MIT Press), §1.3 «Formulating Abstractions with Higher-Order Procedures».
- R. C. Martin — *Clean Code* (Prentice Hall), cap. 3 «Functions».
- S. McConnell — *Code Complete* (2ª ed., Microsoft Press), cap. 7 «High-Quality Routines».

**Libros de los lenguajes del núcleo:**

- L. Ramalho — *Fluent Python* (2ª ed., O'Reilly), cap. 7 «Funciones como objetos de primera clase».
- M. Haverbeke — *Eloquent JavaScript* (3ª ed.), cap. 5 «Higher-Order Functions» — [gratis online](https://eloquentjavascript.net/).
- B. Cherny — *Programming TypeScript* (O'Reilly).
- J. Bloch — *Effective Java* (3ª ed., Addison-Wesley) (ítems sobre lambdas e interfaces funcionales).
- J. Skeet — *C# in Depth* (4ª ed., Manning) (delegados y `Func<>`).
- A. Donovan y B. Kernighan — *The Go Programming Language* (Addison-Wesley), §5.5 sobre valores de función.
- S. Klabnik y C. Nichols — *The Rust Programming Language* — [gratis online](https://doc.rust-lang.org/book/).
- B. Kernighan y D. Ritchie — *The C Programming Language* (2ª ed., Prentice Hall) (punteros a función, §5.11).
- C. J. Date — *SQL and Relational Theory* (3ª ed., O'Reilly).
- J. Lockhart — *Modern PHP* (O'Reilly).

---

> [⏮️ Clase 084](../../parte-5-funciones-y-modularidad/084-funciones-puras-y-efectos-secundarios/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 086 ⏭️](../../parte-5-funciones-y-modularidad/086-modulos-paquetes-y-espacios-de-nombres/README.md)
