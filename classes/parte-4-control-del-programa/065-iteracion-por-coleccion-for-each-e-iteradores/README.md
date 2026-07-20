# Clase 065 — Iteración por colección: for-each e iteradores

> Parte **4 — Control del programa** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

El `for-each` es el bucle que dice "para cada elemento de esto, haz aquello", y nada más. A diferencia del `for` clásico, no habla de posiciones ni de contadores: no hay un `i` que inicializar, ni un `i < n` que comprobar, ni un `i++` que recordar. Esa desaparición del índice no es cosmética. El índice es una variable intermedia que el programa no necesita —lo que necesita son los valores— y que abre la puerta a tres errores clásicos que el `for-each` elimina de raíz: salirse del rango, avanzar de más y confundir el índice con el elemento. Por eso el `for-each` es hoy la forma idiomática de recorrer colecciones en prácticamente todos los lenguajes modernos, y por eso muchos de ellos ni siquiera exponen otra manera de recorrer un diccionario, un conjunto o un flujo.

Detrás de esa sintaxis limpia hay un mecanismo real: el **protocolo de iteración**. El `for-each` no sabe nada de listas, arreglos ni árboles; lo único que sabe es pedirle a un objeto un *iterador* y luego pedirle a ese iterador el siguiente elemento hasta que se agote. Ese contrato —`__iter__`/`__next__` en Python, `Symbol.iterator` en JavaScript, `Iterable`/`Iterator` en Java, `IEnumerable`/`IEnumerator` en C#, `IntoIterator`/`Iterator` en Rust— es lo que permite que el mismo `for` recorra una lista en memoria, las claves de un mapa, las líneas de un archivo o los mensajes de un canal. En esta clase sumamos una lista de enteros de longitud desconocida para ver ese protocolo desde dentro: qué objeto se pide, quién decide cuándo parar, si el elemento que recibes es el original o una copia, y qué pasa —a veces catastróficamente— si modificas la colección mientras la estás recorriendo.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Recorrer una colección con for-each.
2. Acumular un resultado sobre todos los elementos.
3. Leer una lista de longitud variable.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | for-each | Para cada elemento, sin índice |
| 2 | Colección | Una secuencia de valores |
| 3 | Acumulación | Sumar recorriendo |
| 4 | Longitud variable | No se sabe cuántos hay de antemano |

## 📖 Definiciones y características

- **for-each** — bucle que recorre cada elemento de una colección. Clave: sin índice manual.
- **Colección** — estructura que agrupa varios valores (lista, arreglo). Clave: se recorre en orden.
- **Iterar** — visitar cada elemento una vez. Clave: base del procesamiento de datos.
- **Acumulación** — reunir un resultado (suma) recorriendo. Clave: patrón universal.
- **Protocolo de iteración** — el contrato que un objeto cumple para ser recorrible. Clave: iterable produce iterador; iterador entrega el siguiente o señala el fin.

Sebesta, en el capítulo de estructuras de control de *Concepts of Programming Languages*, clasifica el `for-each` entre los *bucles controlados por iterador* y los distingue tanto de los controlados por contador como de los controlados lógicamente: aquí no hay condición booleana ni variable de conteo, sino un objeto que va entregando elementos hasta declararse agotado. El detalle importante es cómo se señala ese agotamiento, porque cada lenguaje eligió un mecanismo distinto para lo mismo. Python levanta la excepción `StopIteration` desde `__next__`, y el `for` la captura en silencio; Ramalho insiste en *Fluent Python* en que un *iterable* (el que tiene `__iter__`) y un *iterador* (el que tiene `__next__` y además se devuelve a sí mismo desde `__iter__`) son cosas distintas, y que confundirlas es el origen de la mitad de los bugs con generadores. JavaScript devuelve desde `next()` un objeto `{value, done}` y el iterable se identifica por tener un método bajo la clave `Symbol.iterator`. Java usa `hasNext()` antes de `next()`, y Bloch recuerda en *Effective Java* que el `for` mejorado (`for (String s : p)`) es puro azúcar sintáctico: sobre un `Iterable` el compilador genera un `Iterator`, y sobre un arreglo genera un índice oculto. C# hace lo mismo con `IEnumerable`/`IEnumerator`, salvo que —como detalla Skeet en *C# in Depth*— el `foreach` no exige realmente implementar la interfaz: le basta con que el tipo ofrezca un método `GetEnumerator` con la forma adecuada, un caso deliberado de *duck typing* estructural dentro de un lenguaje nominalmente tipado.

La otra mitad del asunto es qué te entrega el bucle: el elemento o una copia suya. En **Go**, `for _, x := range xs` asigna a `x` una *copia* del elemento en cada vuelta; modificar `x` no toca el slice, y para mutar hay que escribir `xs[i]`. Donovan y Kernighan advierten además de otra decisión deliberada de Go: el `range` sobre un mapa recorre las claves en orden **aleatorio a propósito**, precisamente para que ningún programa llegue a depender de un orden que la implementación no garantiza. En **Rust** el asunto se vuelve parte del sistema de tipos: `for x in &v` toma prestada la colección y entrega referencias (`&T`), `for x in &mut v` entrega referencias mutables, y `for x in v` **consume** el vector —lo mueve— de modo que después ya no puedes usarlo; los tres casos corresponden a `iter()`, `iter_mut()` e `into_iter()`, y Klabnik y Nichols los presentan como uno de los primeros lugares donde la propiedad deja de ser teoría. En **PHP**, `foreach ($nums as $x)` también itera sobre una copia del valor, y `foreach ($nums as &$x)` sobre una referencia —con la trampa célebre, que Lockhart señala en *Modern PHP*, de que `$x` sigue viva tras el bucle y estropea el siguiente `foreach` si no se hace `unset($x)`. **C**, por su parte, no tiene protocolo alguno: Kernighan y Ritchie enseñan el recorrido con índice o con puntero (`for (p = a; p < a + n; p++)`), y todo lo que un iterador esconde queda a la vista y a cargo del programador.

## 🧩 Situación

Sumar una lista de precios, contar elementos, buscar un máximo, procesar las filas de un CSV, recorrer las cabeceras de una petición HTTP: casi todo el trabajo real de un programa empieza recorriendo una colección. El `for-each` importa porque expresa exactamente esa intención —"para cada elemento"— sin el ruido del índice, y porque desacopla el código de la estructura concreta que hay debajo. Si mañana esa lista pasa a ser un conjunto, un mapa ordenado o un flujo perezoso que lee de disco, el bucle no cambia: cambia el iterable. Esa indiferencia respecto de la estructura es lo que hace que el `for-each` sea también la puerta de entrada a las tuberías de datos (`map`, `filter`, `reduce`) y a los flujos que veremos en la clase siguiente.

El coste de no usarlo se paga en errores y en mantenimiento. El recorrido con índice concentra el clásico *off-by-one* (`<=` donde tocaba `<`), el acceso fuera de rango —que en C es directamente comportamiento indefinido y en Java o C# una excepción en producción— y el recorrido de dos colecciones con el índice equivocado. En rendimiento, la intuición popular de que "indexar es más rápido" suele ser falsa: en Java, C# o Rust el `for-each` permite al compilador o al JIT probar que el recorrido no se sale del arreglo y eliminar la comprobación de límites de cada vuelta, algo que con un índice arbitrario no siempre puede demostrar. Y está el fallo más traicionero de todos: mutar la colección mientras se la recorre. Python responde con `RuntimeError: dictionary changed size during iteration`, Java con `ConcurrentModificationException` gracias al diseño *fail-fast* de sus colecciones, C# con `InvalidOperationException`, y C++ simplemente invalida los iteradores y te deja leyendo memoria liberada. Rust es el único del grupo que convierte ese error en un fallo de compilación: el *borrow checker* no admite un préstamo mutable mientras exista el préstamo compartido que el bucle mantiene vivo, así que el programa jamás llega a ejecutarse mal.

## 🧮 Modelo

- **Entrada** (stdin): una línea con enteros separados por espacio
- **Salida** (stdout): `suma=<suma de todos>`
- **Regla:** suma = Σ elementos

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3 1 4` | `suma=8` |
| `10 20 30` | `suma=60` |
| `5` | `suma=5` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER lista
suma <- 0
PARA CADA x EN lista: suma <- suma + x
ESCRIBIR "suma=" suma
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys

nums = [int(x) for x in sys.stdin.read().split()]
suma = 0
for x in nums:
    suma += x
print(f"suma={suma}")
```

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const nums = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
let suma = 0;
for (const x of nums) {
  suma += x;
}
console.log(`suma=${suma}`);
```

🧬 **El mismo programa en la familia JavaScript / web:** [Dart · ActionScript](primos.md#javascript-web)

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const nums: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
let suma = 0;
for (const x of nums) {
  suma += x;
}
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
        String[] p = br.readLine().trim().split("\\s+");
        long suma = 0;
        for (String s : p) {
            suma += Integer.parseInt(s);
        }
        System.out.println("suma=" + suma);
    }
}
```

🧬 **El mismo programa en la familia JVM:** [Kotlin · Scala · Groovy · Clojure](primos.md#jvm)

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
long suma = 0;
foreach (string s in p) {
    suma += int.Parse(s);
}
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
	data, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	suma := 0
	for _, s := range strings.Fields(data) {
		n, _ := strconv.Atoi(s)
		suma += n
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
    let nums: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    let mut suma = 0i64;
    for x in &nums {
        suma += x;
    }
    println!("suma={suma}");
}
```

🧬 **El mismo programa en la familia Sistemas:** [Zig · Nim · D](primos.md#sistemas)

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long suma = 0, x;
    while (scanf("%ld", &x) == 1) {
        suma += x;
    }
    printf("suma=%ld\n", suma);
    return 0;
}
```

🧬 **El mismo programa en la familia C / llaves:** [C++ · Objective-C](primos.md#c-llaves)

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL: SUM() agrega sobre las filas, sin bucle.
WITH nums(x) AS (VALUES (3), (1), (4))
SELECT printf('suma=%d', sum(x)) AS resultado FROM nums;
```

🧬 **El mismo programa en la familia Lógica y declarativa:** [Prolog · Datalog](primos.md#logica-declarativa)

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
$nums = preg_split('/\s+/', trim(fgets(STDIN)));
$suma = 0;
foreach ($nums as $x) {
    $suma += (int) $x;
}
echo "suma=$suma\n";
```

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔎 Recorrido del código: de la entrada a la salida

Sigamos el caso `3 1 4` de `casos.json`, cuya salida esperada es `suma=8`. En **Python**, `sys.stdin.read()` devuelve la cadena `"3 1 4\n"`; `.split()` la parte en `["3", "1", "4"]` y la comprensión `[int(x) for x in ...]` construye la lista `[3, 1, 4]`. Con `suma = 0` inicializado, entra el `for x in nums:`. Aquí ocurre lo que la sintaxis oculta: el `for` llama internamente a `iter(nums)`, que a su vez invoca `nums.__iter__()` y obtiene un objeto `list_iterator`. En la primera vuelta el bucle llama a `__next__()` sobre ese iterador y recibe `3`, así que `suma += x` deja `suma = 3`; la segunda llamada devuelve `1` y `suma = 4`; la tercera devuelve `4` y `suma = 8`. La cuarta llamada a `__next__()` no devuelve nada: levanta `StopIteration`, excepción que el `for` captura y traduce en "sal del bucle" sin que el programador la vea nunca. Se imprime `suma=8`. La lista original nunca se toca, y `x` es una referencia al mismo objeto entero que vive en la lista.

En **C** el mismo caso se resuelve sin colección ninguna, y ese es justamente el contraste: `while (scanf("%ld", &x) == 1)` no recorre nada, lee. Cada llamada a `scanf` consume el siguiente número del flujo de entrada saltando los espacios en blanco y devuelve `1` si logró convertir un valor. Con `3 1 4` en stdin, la primera llamada deja `x = 3` y devuelve `1`, así que `suma += x` da `3`; la segunda deja `x = 1` y `suma` pasa a `4`; la tercera deja `x = 4` y `suma` llega a `8`. La cuarta llamada topa con el fin de archivo, devuelve `EOF` (distinto de `1`), la condición falla y el bucle termina. `printf("suma=%ld\n", suma)` imprime `suma=8`. Kernighan y Ritchie enseñan exactamente este idioma —el valor de retorno de la función de lectura como condición del bucle— porque en C no existe un iterable que consultar: la "colección" es el propio flujo, y el papel del `StopIteration` de Python lo cumple aquí un valor centinela.

En **Rust** el recorrido es idéntico en resultado pero explícito en propiedad. `read_to_string` deja `"3 1 4\n"` en `s`; `s.split_whitespace()` produce un iterador perezoso de rodajas de texto, `.map(|x| x.parse().unwrap())` lo envuelve en otro iterador que convertirá cada rodaja a `i64`, y `.collect()` es quien realmente consume la cadena y materializa el `Vec<i64>` con `[3, 1, 4]` —hasta ese punto no se había parseado un solo número. Después, `for x in &nums` es la clave: el `&` significa que el bucle toma *prestado* el vector en lugar de consumirlo, de modo que `x` tiene tipo `&i64` y `nums` sigue siendo utilizable tras el bucle. `suma += x` acumula `3`, luego `4`, luego `8`, y `println!("suma={suma}")` cierra. Si se hubiera escrito `for x in nums` sin el `&`, el vector se habría movido dentro del bucle y cualquier uso posterior de `nums` sería un error de compilación: la misma línea, un `&` de diferencia, y dos semánticas de propiedad distintas.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `for x in lista` (Python) vs. `for (int x : arr)` (Java) vs. `for x in &v` (Rust). |
| Semántica | Todos recorren sin índice; C aún usa índice o puntero. |
| Paradigmática | SQL suma con `SUM()` sobre filas, sin bucle explícito. |

Agrupando los diez lenguajes por la decisión de diseño que gobierna el recorrido, aparecen cuatro bloques. El primero es el de los **lenguajes con protocolo de iteración basado en objetos**: **Python** (`__iter__`/`__next__` con `StopIteration`), **JavaScript** y **TypeScript** (`Symbol.iterator` devolviendo un objeto con `next()` que produce `{value, done}`), **Java** (`Iterable`/`Iterator` con `hasNext()`/`next()`, y el `for` mejorado como azúcar sobre él) y **C#** (`IEnumerable`/`IEnumerator`, con la particularidad de que `foreach` se conforma con un `GetEnumerator` de la forma correcta, sin exigir la interfaz). En los cuatro, un tipo propio se vuelve recorrible con solo cumplir el contrato. El segundo bloque lo forman **Go** y **Rust**, que resuelven la iteración sin objetos-interfaz clásicos: Go integra `range` en el lenguaje con reglas fijas por tipo —slice, mapa, cadena, canal—, entrega copias del valor y aleatoriza a propósito el orden de los mapas; Rust la construye sobre el trait `Iterator` y su compañero `IntoIterator`, y hace de `iter()`, `iter_mut()` e `into_iter()` tres formas distintas de recorrer con tres semánticas distintas de propiedad. El tercer bloque es el de la iteración por **acceso posicional**: **C**, sin ningún protocolo, recorre con índice o con puntero, o —como en la implementación de esta clase— consume directamente el flujo; y **PHP**, aunque tiene `foreach`, arrastra la distinción entre iterar por copia (`as $x`) y por referencia (`as &$x`) con sus efectos residuales. El cuarto es **SQL**, que sencillamente no itera: `SUM(x)` es una agregación sobre un conjunto de filas y el orden de recorrido es asunto del motor, no del programador. La misma frase —"para cada elemento"— se resuelve así con un contrato de objetos, con una construcción del lenguaje, con aritmética de punteros o con una declaración de intención, según lo que cada lenguaje considere que debe estar a la vista.

## 🧬 El concepto en la familia

En la familia de C, el `for-each` llegó tarde y como añadido: C nunca lo tuvo, y C++ (con `for (auto& x : v)`), Java 5 (`for (T x : c)`), C# (`foreach`) y PHP lo incorporaron sobre estructuras previas, lo que explica que en todas ellas conviva con el `for` clásico y que sigan expuestas las viejas trampas de invalidación de iteradores. La familia del scripting dinámico —Python, Ruby, PHP, JavaScript— hizo del recorrido por elementos el modo *natural* y del índice la excepción: Ruby ni siquiera necesita palabra clave, porque `lista.each { |x| ... }` es un método que recibe un bloque, y el módulo `Enumerable` construye sobre él toda la biblioteca de transformaciones. La familia ML y funcional va un paso más allá y prescinde del bucle: en Haskell o en OCaml no se recorre, se pliega (`foldr`, `List.fold_left`), y la iteración explícita se considera un detalle de implementación de operaciones más expresivas. Go y Rust representan dos rediseños modernos y opuestos: Go metió `range` dentro del lenguaje para tener una sola forma simple y predecible, con reglas especiales por tipo pero sin abstracción extensible; Rust hizo lo contrario y puso todo en un trait, de modo que `Iterator` es a la vez el mecanismo del `for` y el fundamento de una biblioteca entera de adaptadores encadenables. Los declarativos, con SQL a la cabeza, niegan el problema: como argumenta Date en *SQL and Relational Theory*, una relación es un conjunto y un conjunto no tiene orden, así que pedirle a SQL que "recorra" es pedirle algo ajeno a su modelo.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 065
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Modificar la colección mientras se la recorre** → causa: añadir o borrar elementos invalida el estado interno del iterador, que sigue apuntando a una estructura que ya cambió; Python lanza `RuntimeError: dictionary changed size during iteration`, Java `ConcurrentModificationException` por su diseño *fail-fast*, C# `InvalidOperationException`, y C++ deja iteradores colgando que leen memoria liberada → solución: recorrer una copia (`for x in list(d)`, `foreach (var x in lista.ToList())`), acumular los cambios aparte y aplicarlos al terminar, o usar el `remove()` del propio iterador cuando el lenguaje lo ofrece.
- **Creer que el elemento del bucle es el original y mutarlo** → causa: en Go `for _, x := range xs` entrega una **copia** del elemento, y en PHP `foreach ($nums as $x)` también; asignar a `x` no cambia nada en la colección y el bug pasa desapercibido porque no hay error → solución: en Go escribir en `xs[i]` usando el índice del `range`; en PHP usar `foreach ($nums as &$x)` y hacer `unset($x)` al salir para que la referencia no contamine el siguiente bucle.
- **Depender del orden de iteración de un mapa** → causa: el orden de recorrido de las claves no está garantizado en general, y Go lo aleatoriza **deliberadamente** en cada ejecución para impedir que un programa se apoye en él; el resultado son pruebas que pasan en tu máquina y fallan en CI → solución: si el orden importa, extraer las claves y ordenarlas explícitamente antes de recorrer.
- **Usar índice cuando solo necesitas el valor** → causa: el `for` con contador añade tres oportunidades de error (inicialización, límite, avance) que el `for-each` no tiene, y en C o C++ un índice fuera de rango es comportamiento indefinido, no una excepción → solución: reservar el índice para cuando la posición forma parte del problema, y usar entonces las construcciones que dan ambas cosas: `enumerate()` en Python, `entries()` en JavaScript, `for i, x := range xs` en Go, `.iter().enumerate()` en Rust.
- **Olvidar inicializar el acumulador** → causa: si `suma` arranca en un valor distinto de `0` —el elemento neutro de la suma—, el resultado sale desplazado desde la primera vuelta y con listas vacías devuelve basura en lugar de `0` → solución: inicializar siempre con el neutro de la operación (`0` para sumar, `1` para multiplicar) y comprobar el caso de la colección vacía.

## ❓ Preguntas frecuentes

- **¿`for-each` o `for` con índice?** Usa `for-each` siempre que solo necesites el valor, que es la mayoría de las veces: es más corto, más difícil de equivocar y funciona igual sobre listas, conjuntos, mapas o flujos. Reserva el índice para cuando la posición es parte del problema (comparar `x[i]` con `x[i+1]`, escribir en el elemento, recorrer dos colecciones en paralelo). Casi todos los lenguajes ofrecen un punto intermedio —`enumerate`, `entries`, `range` con dos variables— que te da posición y valor sin volver al contador manual.
- **¿El `for-each` es más lento que indexar?** Normalmente no, y a menudo es más rápido. En Java, C# o Rust el compilador o el JIT pueden demostrar que el recorrido no se sale del arreglo y eliminar la comprobación de límites que un acceso indexado arbitrario obliga a hacer en cada vuelta. La complejidad es O(n) en ambos casos; lo que cambia es el trabajo constante por elemento, y ahí el iterador suele ganar por tener más información disponible para el optimizador.
- **¿Qué diferencia hay entre `for x in &v` y `for x in v` en Rust?** Con `&v` el bucle toma prestado el vector y entrega referencias (`&T`); `v` sigue siendo tuyo y utilizable después. Sin el `&`, `v` se **mueve** dentro del bucle mediante `into_iter()`, entrega los valores por propiedad y cualquier uso posterior de `v` es un error de compilación. Existe además `&mut v`, que entrega `&mut T` y permite modificar los elementos en su sitio.
- **¿Por qué Rust no tiene el problema de modificar la colección mientras la recorre?** Porque el bucle mantiene vivo un préstamo de la colección durante todo el recorrido, y el *borrow checker* no permite crear un préstamo mutable mientras exista uno compartido. Intentar hacer `v.push(...)` dentro de un `for x in &v` no compila. Es la única prestación del grupo que convierte en error de compilación lo que en Python, Java, C# o C++ es un fallo en tiempo de ejecución —o, peor, memoria corrupta.
- **¿Cómo leo una lista de tamaño desconocido?** Leyendo toda la entrada y separándola por espacios en blanco, como hacen aquí Python (`sys.stdin.read().split()`), Go (`strings.Fields`) o Rust (`split_whitespace`). La alternativa, visible en la implementación de C, es no construir colección alguna y consumir el flujo elemento a elemento mientras la lectura tenga éxito: memoria constante en lugar de proporcional a la entrada.

## 🔗 Referencias

**Libros de la parte:**

- O.-J. Dahl, E. W. Dijkstra y C. A. R. Hoare — *Structured Programming* (Academic Press). Su defensa de las construcciones que abstraen el recorrido —frente al salto y al manejo manual de posiciones— es el antecedente directo del `for-each` como estructura de control.
- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson), cap. control de flujo, sección de *bucles controlados por iterador*, que separa este bucle de los controlados por contador y por condición y compara los protocolos de iteración de los distintos lenguajes.

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

> [⏮️ Clase 064](../../parte-4-control-del-programa/064-iteracion-por-rango-for-clasico-y-for-range/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 066 ⏭️](../../parte-4-control-del-programa/066-iteradores-y-generadores-perezosos-lazy/README.md)
