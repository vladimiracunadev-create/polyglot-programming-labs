# Clase 095 — Mapas / diccionarios / tablas hash

> Parte **6 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Comprender el **mapa** —diccionario, tabla hash, según el lenguaje— como la estructura que asocia **claves con valores** y que, junto con el arreglo, sostiene buena parte de la programación real. Si el conjunto de la clase anterior era una tabla hash que solo guarda claves, el mapa es la tabla hash completa: a cada clave le cuelga un valor. Lo esencial es cómo se logra el acceso rápido. Como formaliza Cormen en el capítulo 11 de *Introduction to Algorithms*, una **función hash** transforma la clave en el índice de un cubo, de modo que leer, insertar o actualizar `mapa[clave]` cuesta **O(1) promedio**, no O(n): no hay que buscar la clave recorriendo, se calcula directamente dónde vive. Sedgewick dedica a esta idea el corazón de sus *symbol tables* en *Algorithms*. El uso más común, y el de hoy, es el **mapa de frecuencias**: recorrer una secuencia usando cada elemento como clave y llevando en el valor cuántas veces ha aparecido. Es el patrón que subyace a contar palabras, votos o visitas, y muestra el mapa en su forma más pura: clave → cuenta.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Construir un mapa de frecuencias.
2. Consultar el valor de una clave.
3. Reconocer el acceso por clave en O(1).

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Mapa/diccionario | Clave → valor |
| 2 | Frecuencias | Contar apariciones |
| 3 | Acceso por clave | Búsqueda rápida |

## 📖 Definiciones y características

Un **mapa** es una colección de pares **clave→valor** donde cada clave es única y sirve para localizar su valor. Su implementación dominante es la **tabla hash**, y entender esa tabla explica todas sus propiedades. Cormen la describe así (cap. 11): una función hash mapea cada clave a un índice de una tabla de cubos; cuando dos claves distintas caen en el mismo cubo se produce una **colisión**, que se resuelve por **encadenamiento** (cada cubo guarda una lista de las entradas que colisionan) o por **direccionamiento abierto** (se busca otro cubo libre siguiendo una secuencia de sondeo). Con un buen reparto, el acceso, la inserción y el borrado son **O(1) promedio**; en el peor caso —todas las claves colisionando— caen a O(n). El equilibrio lo gobierna el **factor de carga** (entradas ÷ cubos): cuando sube demasiado, la tabla hace **rehashing** —reserva más cubos y recoloca todo—, una operación O(n) puntual que mantiene barato el coste amortizado.

La segunda cara del mapa es el **orden**, y aquí los lenguajes discrepan de forma notable. El `dict` de Python conserva el **orden de inserción** desde la versión 3.7 (Ramalho lo documenta en *Fluent Python*); el `HashMap` de Java y el `Dictionary` de C# no garantizan ningún orden; y Go va más lejos: itera sus mapas en **orden deliberadamente aleatorio** para que nadie escriba código que dependa de un orden accidental (Donovan y Kernighan lo advierten en *The Go Programming Language*). Las claves, por último, deben ser **hashables**: números y cadenas siempre valen; objetos mutables, en general, no.

- **Mapa** — colección de pares clave→valor respaldada por una tabla hash (Python `dict`, Java `HashMap`, C# `Dictionary`, Go `map`, Rust `HashMap`); acceso por clave en O(1) promedio.
- **Clave** — identificador único de cada entrada; se pasa por la función hash para localizar el cubo. Insertar con una clave existente sobrescribe su valor.
- **Frecuencia** — número de apariciones de un elemento; el uso canónico del mapa consiste en usar el elemento como clave y su cuenta como valor.

## 🧩 Situación

Contar cuántas veces aparece cada palabra en un texto, cuántos votos recibió cada candidato, cuántas visitas tuvo cada página, qué usuario hizo cada acción: son todas variantes del mismo problema —asociar cada cosa con un dato y actualizarlo sobre la marcha— y todas piden un mapa. Resolverlas con listas paralelas o búsquedas lineales convierte cada actualización en un recorrido O(n); el mapa las hace en O(1) promedio, calculando directamente dónde está la entrada de esa clave. El caso de hoy es la forma esencial de ese patrón: construir un mapa de frecuencias de una lista de enteros y consultar cuántas veces aparece el primero. Verás que el mapa hace dos trabajos a la vez —almacenar y contar— y que el modismo `mapa[clave] = mapa.get(clave, 0) + 1` (o su equivalente en cada lenguaje) captura la esencia de «leer el valor actual, incrementarlo y volver a escribirlo».

## 🧮 Modelo

- **Entrada** (stdin): una línea con enteros separados por espacio
- **Salida** (stdout): `cuenta=<veces que aparece el primer elemento>`
- **Regla:** cuenta = frecuencia[lista[0]]

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3 1 3 3` | `cuenta=3` |
| `5 5` | `cuenta=2` |
| `7 1 2` | `cuenta=1` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER lista ; construir mapa de frecuencias ; ESCRIBIR frecuencia del primero
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

nums = [int(x) for x in sys.stdin.read().split()]
freq = {}
for x in nums:
    freq[x] = freq.get(x, 0) + 1
print(f"cuenta={freq[nums[0]]}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const nums = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const freq = new Map();
for (const x of nums) freq.set(x, (freq.get(x) || 0) + 1);
console.log(`cuenta=${freq.get(nums[0])}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const nums: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const freq = new Map<number, number>();
for (const x of nums) freq.set(x, (freq.get(x) || 0) + 1);
console.log(`cuenta=${freq.get(nums[0])}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.HashMap;
import java.util.Map;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        Map<Integer, Integer> freq = new HashMap<>();
        for (String s : p) {
            int x = Integer.parseInt(s);
            freq.merge(x, 1, Integer::sum);
        }
        System.out.println("cuenta=" + freq.get(Integer.parseInt(p[0])));
    }
}
```

### C# · `dotnet run`

```csharp
using System;
using System.Collections.Generic;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
var freq = new Dictionary<int, int>();
foreach (string s in p) {
    int x = int.Parse(s);
    freq[x] = freq.GetValueOrDefault(x, 0) + 1;
}
Console.WriteLine($"cuenta={freq[int.Parse(p[0])]}");
```

### Go · `go run main.go`

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
	fields := strings.Fields(line)
	freq := make(map[int]int)
	var nums []int
	for _, s := range fields {
		n, _ := strconv.Atoi(s)
		nums = append(nums, n)
		freq[n]++
	}
	fmt.Printf("cuenta=%d\n", freq[nums[0]])
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::collections::HashMap;
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let nums: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    let mut freq: HashMap<i64, i64> = HashMap::new();
    for &x in &nums {
        *freq.entry(x).or_insert(0) += 1;
    }
    println!("cuenta={}", freq[&nums[0]]);
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long v[1024];
    int n = 0;
    while (scanf("%ld", &v[n]) == 1) n++;
    int cuenta = 0;
    for (int i = 0; i < n; i++) {
        if (v[i] == v[0]) cuenta++;
    }
    printf("cuenta=%d\n", cuenta);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: GROUP BY para frecuencias.
WITH nums(x) AS (VALUES (3), (1), (3), (3))
SELECT printf('cuenta=%d', count(*)) AS resultado
FROM nums WHERE x = (SELECT x FROM nums LIMIT 1);
```

### PHP · `php main.php`

```php
<?php
$nums = array_map('intval', preg_split('/\s+/', trim(fgets(STDIN))));
$freq = array_count_values($nums);
echo "cuenta=" . $freq[$nums[0]] . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🧪 Laboratorio guiado: del código a la salida

Sigamos el caso `3 1 3 3`, que debe producir `cuenta=3`. El primer elemento es `3`, y aparece tres veces; el mapa de frecuencias debe reflejarlo y luego consultarse por esa clave.

En **Python**, el corazón es `freq[x] = freq.get(x, 0) + 1`. `freq.get(x, 0)` lee el valor actual de la clave `x`, devolviendo `0` si aún no existe —el truco que evita el error de clave inexistente—. Recorriendo `3 1 3 3`: el `3` pasa de ausente a 1; el `1` a 1; el segundo `3` de 1 a 2; el tercer `3` de 2 a 3. El mapa queda `{3: 3, 1: 1}`. Después, `freq[nums[0]]` consulta la clave `nums[0] = 3` y devuelve 3. Cada acceso a `freq[...]` es una operación hash O(1) promedio.

En **Java**, el mismo conteo se escribe con `freq.merge(x, 1, Integer::sum)`, un método que Bloch destaca en *Effective Java* por eliminar el rodeo del «leer, comprobar nulo, escribir»: si la clave `x` no existe, la inserta con valor 1; si existe, combina el valor viejo con 1 usando `Integer::sum`. Para `3 1 3 3` el resultado es idéntico: la clave `3` termina en 3. Luego `freq.get(Integer.parseInt(p[0]))` recupera la cuenta del primer token. El `HashMap` no promete orden de iteración, pero eso aquí da igual: solo consultamos una clave concreta.

En **C**, no hay mapa nativo, y el código lo sortea con astucia: como el problema solo pide la frecuencia del **primer** elemento, no construye ninguna tabla; recorre el arreglo `v[]` contando cuántos elementos son iguales a `v[0]`. Para `3 1 3 3` cuenta las tres apariciones de `3` y emite `cuenta=3`. Es correcto para esta pregunta puntual, pero no generaliza: contar la frecuencia de *cada* clave a la vez exigiría construir una tabla hash a mano o recorrer en O(n²). Ese contraste es justo lo que el mapa nativo regala en los demás lenguajes.

Los tres imprimen `cuenta=3`; el verificador comprueba que las diez implementaciones coinciden carácter a carácter con lo que dicta `casos.json`.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `dict` (Python), `{}`/Map (JS), `HashMap` (Java/Rust), `Dictionary` (C#). |
| Semántica | El mapa no garantiza orden de claves; C lo simula con arreglos. |
| Paradigmática | SQL agrupa con GROUP BY. |

La diferencia más visible es el **modismo de incremento con valor por defecto**, porque leer una clave ausente es el error clásico con mapas y cada lenguaje lo previene a su manera: Python usa `freq.get(x, 0) + 1`, C# `GetValueOrDefault(x, 0) + 1`, Java el elegante `merge(x, 1, Integer::sum)`, Rust `*freq.entry(x).or_insert(0) += 1` (que devuelve una referencia mutable a la entrada, creándola si falta), Go se apoya en que el valor cero de un `int` ausente es `0`, de modo que `freq[n]++` simplemente funciona, y PHP tiene la función de biblioteca `array_count_values`. La segunda diferencia honda es el **orden de iteración**: el `dict` de Python conserva orden de inserción desde 3.7, Go lo aleatoriza a propósito, y Java/C# no lo garantizan; por eso este ejercicio consulta una clave concreta en vez de recorrer, y así el resultado no depende del orden. El tercer eje es **quién trae mapa nativo**: todos menos C lo tienen de serie; en C hay que construir la tabla hash o, como aquí, resolver el caso puntual con un recorrido. Finalmente, el **array asociativo de PHP** difumina la frontera entre lista y mapa: es a la vez secuencia indexada y diccionario, algo que Lockhart señala en *Modern PHP* como rasgo distintivo del lenguaje.

## 🧬 El concepto en la familia

El mapa es tan central que casi ningún lenguaje prescinde de él, y sus nombres delatan su implementación: *HashMap*, *Dictionary*, *hash*, *associative array*, *table*. La familia se divide en dos ramas por el orden. La rama **hash** —`HashMap`, `dict`, `Dictionary`, `map` de Go, `HashMap` de Rust— da O(1) promedio sin orden garantizado. La rama **ordenada** —`TreeMap` en Java, `SortedDictionary` en C#, `BTreeMap` en Rust, `std::map` en C++— mantiene las claves ordenadas a cambio de O(log n) por operación, respaldada por un árbol balanceado en lugar de una tabla hash. En Ruby, `Hash.new(0)` crea un mapa cuyo valor por defecto es 0, ideal para contar sin comprobar existencia; en Go, `map[int]int` es el modismo directo para frecuencias. Reconocer que «mapa» significa por defecto «tabla hash sin orden», y que existe la variante ordenada de árbol cuando se necesita recorrer por clave en orden, es la decisión de diseño que más se repite en la práctica.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 095
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Leer una clave inexistente sin defecto** → causa: error o valor nulo → solución: inicializar con 0 o comprobar la existencia
- **Asumir orden de inserción** → causa: no siempre garantizado → solución: usar mapas ordenados si lo necesitas

## ❓ Preguntas frecuentes

- **¿Mapa o lista de pares?** Mapa para búsqueda rápida por clave; lista de pares si el orden importa.
- **¿Las claves pueden ser cualquier cosa?** Suelen requerir ser hashables/comparables; números y cadenas siempre valen.

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

> [⏮️ Clase 094](../../parte-6-datos-y-estructuras/094-conjuntos-sets-y-unicidad/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 096 ⏭️](../../parte-6-datos-y-estructuras/096-pilas-y-colas/README.md)
