# Clase 089 — Arreglos de tamaño fijo

> Parte **6 — Datos y estructuras** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Comprender el **arreglo de tamaño fijo** no como «una lista cualquiera», sino como la estructura de datos primitiva de la que descienden casi todas las demás. Un arreglo es un bloque **contiguo** de memoria dividido en celdas idénticas; conocer su longitud por anticipado permite reservar ese bloque de una sola vez y, sobre todo, calcular la dirección de cualquier elemento con una multiplicación y una suma: `dirección(arr[i]) = base + i × tamaño`. De esa aritmética nace la propiedad que define al arreglo y que ninguna otra estructura ofrece tan barata: **acceso aleatorio en tiempo constante, O(1)**, dé igual que pidas el elemento 0 o el 999. Cormen lo formaliza en el modelo RAM (CLRS, cap. 10) y Sedgewick lo llama la ventaja del «acceso indexado». En esta clase verás esa misma física encarnada en diez lenguajes que difieren en la escritura pero comparten la memoria.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Declarar y recorrer un arreglo fijo.
2. Acumular suma y máximo.
3. Reconocer el acceso por índice.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Arreglo fijo | Tamaño conocido, memoria contigua |
| 2 | Índice | Acceso por posición (base 0) |
| 3 | Recorrido | Visitar cada posición |

## 📖 Definiciones y características

- **Arreglo (array)** — secuencia de elementos del mismo tipo colocados uno tras otro en memoria. Su rasgo esencial no es «guardar varias cosas», sino *cómo* las guarda: contiguas y del mismo tamaño, lo que hace posible el acceso O(1) por índice. Recorrerlo entero cuesta O(n).
- **Tamaño fijo** — la longitud se fija al crear el arreglo y no cambia. A cambio de perder flexibilidad, ganas previsibilidad: el compilador sabe exactamente cuánta memoria reservar y a menudo puede colocarlo en la pila, sin llamadas al asignador dinámico.
- **Índice** — desplazamiento entero desde el inicio, empezando en 0. `arr[0]` es el primer elemento porque está a *cero* celdas del comienzo; `arr[i]` está a `i` celdas. La base 0 no es un capricho: es la traducción directa de la aritmética de direcciones.

## 🧩 Situación

Piensa en tres sensores de temperatura, los doce meses de un año o los siete días de la semana: cantidades que **no van a cambiar** durante la ejecución. Cuando el tamaño se conoce de antemano, el arreglo fijo es la opción más eficiente que existe: no reserva memoria de más «por si crece», no paga el coste de reubicarse y su disposición contigua es amable con la caché del procesador (los elementos vecinos viajan juntos a la caché, lo que acelera los recorridos). El problema de hoy es deliberadamente mínimo —tres enteros, su suma y su máximo— para que la atención caiga sobre la estructura, no sobre el algoritmo: un solo recorrido lineal que toca cada celda una vez.

## 🧮 Modelo

- **Entrada** (stdin): una línea `a b c` (tres enteros)
- **Salida** (stdout): `suma=<a+b+c> max=<el mayor>`
- **Regla:** suma y máximo de los tres elementos

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3 1 4` | `suma=8 max=4` |
| `10 5 2` | `suma=17 max=10` |
| `1 1 1` | `suma=3 max=1` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER arr[3]
suma <- Σ arr ; max <- MAX(arr)
ESCRIBIR suma, max
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys

a, b, c = map(int, sys.stdin.readline().split())
arr = [a, b, c]
print(f"suma={sum(arr)} max={max(arr)}")
```

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const arr = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`suma=${arr.reduce((a, b) => a + b, 0)} max=${Math.max(...arr)}`);
```

🧬 **El mismo programa en la familia JavaScript / web:** [Dart · ActionScript](primos.md#javascript-web)

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const arr: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`suma=${arr.reduce((a, b) => a + b, 0)} max=${Math.max(...arr)}`);
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
        int[] arr = new int[3];
        for (int i = 0; i < 3; i++) arr[i] = Integer.parseInt(p[i]);
        int suma = 0, max = arr[0];
        for (int x : arr) {
            suma += x;
            if (x > max) max = x;
        }
        System.out.println("suma=" + suma + " max=" + max);
    }
}
```

🧬 **El mismo programa en la familia JVM:** [Kotlin · Scala · Groovy · Clojure](primos.md#jvm)

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;
using System.Linq;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
int[] arr = p.Take(3).Select(int.Parse).ToArray();
Console.WriteLine($"suma={arr.Sum()} max={arr.Max()}");
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
	f := strings.Fields(line)
	var arr [3]int
	for i := 0; i < 3; i++ {
		arr[i], _ = strconv.Atoi(f[i])
	}
	suma, max := 0, arr[0]
	for _, x := range arr {
		suma += x
		if x > max {
			max = x
		}
	}
	fmt.Printf("suma=%d max=%d\n", suma, max)
}
```

🧬 **El mismo programa en la familia Sistemas:** [Zig · Nim · D](primos.md#sistemas)

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let v: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    let arr: [i64; 3] = [v[0], v[1], v[2]];
    let suma: i64 = arr.iter().sum();
    let max = *arr.iter().max().unwrap();
    println!("suma={suma} max={max}");
}
```

🧬 **El mismo programa en la familia Sistemas:** [Zig · Nim · D](primos.md#sistemas)

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long arr[3];
    if (scanf("%ld %ld %ld", &arr[0], &arr[1], &arr[2]) != 3) return 1;
    long suma = 0, max = arr[0];
    for (int i = 0; i < 3; i++) {
        suma += arr[i];
        if (arr[i] > max) max = arr[i];
    }
    printf("suma=%ld max=%ld\n", suma, max);
    return 0;
}
```

🧬 **El mismo programa en la familia C / llaves:** [C++ · Objective-C](primos.md#c-llaves)

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL: agrega sobre filas, no índices.
WITH arr(x) AS (VALUES (3), (1), (4))
SELECT printf('suma=%d max=%d', sum(x), max(x)) AS resultado FROM arr;
```

🧬 **El mismo programa en la familia Lógica y declarativa:** [Prolog · Datalog](primos.md#logica-declarativa)

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
[$a, $b, $c] = preg_split('/\s+/', trim(fgets(STDIN)));
$arr = [(int) $a, (int) $b, (int) $c];
echo "suma=" . array_sum($arr) . " max=" . max($arr) . "\n";
```

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🧪 Laboratorio guiado: del código a la salida

Sigamos el caso `3 1 4`, que debe producir `suma=8 max=4`. Las diez implementaciones ejecutan el mismo recorrido lineal; conviene mirar tres que revelan modelos de memoria distintos.

En **Python**, `map(int, ...split())` convierte la línea en tres enteros y `arr = [a, b, c]` crea una lista (Python no tiene arreglos fijos nativos: usa listas dinámicas). Las funciones `sum(arr)` y `max(arr)` recorren la secuencia por dentro, cada una en O(n): suman 3+1+4=8 y comparan hasta quedarse con 4. La salida se arma con un f-string.

En **Go**, `var arr [3]int` es un arreglo de verdad de tamaño fijo: el `3` es parte del tipo y el arreglo vive en la pila. El bucle `for _, x := range arr` acumula `suma` y actualiza `max`, inicializado en `arr[0]`. Aquí se ve el patrón clásico del máximo: empezar con el primer elemento como candidato y quedarse con cualquiera mayor —nunca con un valor «neutro» como 0, que fallaría si todos fueran negativos.

En **C**, `long arr[3]` reserva 24 bytes contiguos y `scanf` los llena. El bucle accede con `arr[i]`, que el compilador traduce a `base + i × 8`: la aritmética de direcciones desnuda. Es el mismo algoritmo que en Python, pero sin ninguna capa entre tu código y la memoria.

Los tres imprimen `suma=8 max=4`; el verificador comprueba que las diez implementaciones coinciden carácter a carácter con lo que dicta `casos.json`.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `[a, b, c]` (Python/JS), `int[]` (Java/C#), `[i64; 3]` (Rust), `long[3]` (C). |
| Semántica | En C el tamaño es parte del tipo; en Python/JS el arreglo es dinámico. |
| Paradigmática | SQL agrega sobre filas, no índices. |

La diferencia semántica más honda es **quién comprueba los límites**. En C, `arr[5]` sobre un arreglo de 3 no da error: lee memoria ajena (comportamiento indefinido). En Java, C#, Go, Rust y Python la lectura fuera de rango lanza una excepción o *panic* en tiempo de ejecución, a cambio de una comprobación en cada acceso. Y hay un eje de **valor vs. referencia**: en C, Rust, Go y C# un arreglo fijo se copia al asignarlo o pasarlo (en Rust, `[i64; 3]` implementa `Copy`); en Java, `int[]` es una referencia y se comparte. Python, JavaScript y PHP ni siquiera tienen arreglos fijos: sus «arreglos» son colecciones dinámicas que crecen —el tema de la clase siguiente.

## 🧬 El concepto en la familia

En Go, `[3]int` es un arreglo fijo pero `[]int` es un *slice* dinámico: parecen iguales pero uno es valor y el otro una vista con longitud y capacidad. En C++, `std::array<int, 3>` es el fijo con seguridad de tipos, frente al `int[3]` heredado de C. En Rust, `[i64; 3]` es fijo y vive en la pila, mientras `Vec<i64>` vive en el heap. Reconocer este par fijo/dinámico en cada lenguaje es media batalla ganada: casi todos ofrecen ambos y el nombre a veces engaña.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 089
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Salirse del índice (off-by-one)** → recorrer `0..=n` en vez de `0..n-1`, o confiar en un tamaño equivocado → recorre solo `[0, n)`; en C esto es especialmente peligroso porque no hay red de seguridad y el fallo puede pasar inadvertido.
- **Inicializar el máximo en 0** → si todos los elementos fueran negativos, el resultado sería 0, que no está en el arreglo → inicializa `max` con `arr[0]`, el primer elemento real, como hacen todas las implementaciones.
- **Confundir fijo con dinámico** → esperar que un arreglo fijo crezca con `append` → si el tamaño varía, usa lista/vector (clase 090).

## ❓ Preguntas frecuentes

- **¿Por qué el índice empieza en 0?** Porque es un desplazamiento desde el inicio: el primer elemento está a distancia cero. `arr[i]` significa literalmente «la celda a `i` posiciones de la base». Lenguajes como Fortran o Lua rompen esta convención y empiezan en 1, lo que obliga a restar 1 al hacer aritmética de direcciones.
- **¿Por qué el acceso es O(1) pero la búsqueda es O(n)?** Acceder a una posición conocida es una cuenta directa; *encontrar* un valor sin saber dónde está obliga a mirar celda por celda. El arreglo es rapidísimo para «dame el elemento i» y mediocre para «¿está el valor v?».
- **¿Arreglo o lista?** Arreglo fijo si el tamaño es constante y te importan la eficiencia y la localidad de memoria; lista/vector si el tamaño cambia (siguiente clase).

## 🔗 Referencias

**Libros de la parte:**

- T. Cormen, C. Leiserson, R. Rivest y C. Stein — *Introduction to Algorithms* (4ª ed., MIT Press).
- R. Sedgewick y K. Wayne — *Algorithms* (4ª ed., Addison-Wesley).

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

> [⏮️ Clase 088](../../parte-5-funciones-y-modularidad/088-importar-exportar-y-organizar-un-proyecto/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 090 ⏭️](../../parte-6-datos-y-estructuras/090-listas-vectores-y-arreglos-dinamicos/README.md)
