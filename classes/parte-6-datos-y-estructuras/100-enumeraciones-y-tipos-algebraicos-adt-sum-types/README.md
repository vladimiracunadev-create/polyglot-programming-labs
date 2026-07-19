# Clase 100 — Enumeraciones y tipos algebraicos (ADT / sum types)

> Parte **6 — Datos y estructuras** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Distinguir dos ideas que a menudo se confunden bajo la palabra «enum». La primera es la **enumeración simple**: un conjunto cerrado de valores con nombre —`Lunes`, `Martes`…, o `Rojo`, `Verde`, `Azul`— que sustituye a las constantes enteras «mágicas» por símbolos legibles y con tipo. La segunda, mucho más potente, es el **tipo suma** o **tipo algebraico de datos (ADT)**: un valor que es **una de varias alternativas, y cada alternativa puede llevar datos distintos**. `Forma = Cuadrado(lado) | Rectangulo(ancho, alto)` no es solo una etiqueta: cada variante transporta su propia carga. Donde el registro de la clase 099 es un tipo **producto** (tiene el campo A **y** el campo B), el tipo suma es su dual: es la variante A **o** la variante B. Sobre ese valor, la construcción `match` (o `switch` de patrones) decide qué variante tienes, extrae sus datos y calcula. El objetivo profundo es entender por qué esta forma, heredada de la familia ML (Haskell, OCaml, F#) y adoptada por Rust y Swift, es la manera **segura** de modelar «esto o lo otro»: el compilador verifica la **exhaustividad** y hace imposible olvidar un caso.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Modelar alternativas con un tipo suma.
2. Decidir por variante con match/switch.
3. Reconocer la exhaustividad del tipo algebraico.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Tipo suma (ADT) | Una de varias alternativas |
| 2 | Variante | Cada caso con sus datos |
| 3 | Match por variante | Decidir según la forma |

## 📖 Definiciones y características

- **Enumeración (enum)** — tipo cuyos valores forman un conjunto **cerrado y finito** de constantes con nombre. En su forma simple es una etiqueta sin datos: `enum Dia { Lunes, Martes, ... }`. Aporta seguridad de tipos (no puedes pasar un `Dia` donde se espera un `Color`) y legibilidad frente a los enteros mágicos. Java y C# la enriquecen: el `enum` de Java es una clase completa con métodos, y Bloch (*Effective Java*, ítem «Use enums instead of int constants») la defiende como sustituto seguro de las constantes enteras.
- **Tipo suma / ADT** — valor que es **una** de varias alternativas, y cada alternativa puede llevar **datos propios y distintos**: `Cuadrado(i64)` lleva un lado, `Rectangulo(i64, i64)` lleva ancho y alto. Se llama «suma» porque el número de valores posibles del tipo es la **suma** de los de cada variante, frente al tipo **producto** (el registro), donde se **multiplican**. De ahí «algebraico»: los tipos se combinan con sumas y productos como en el álgebra. Klabnik y Nichols (*The Rust Programming Language*, cap. 6) presentan el `enum` de Rust exactamente así, como el tipo que «puede ser una de un conjunto posible de valores».
- **Variante (variant / constructor)** — cada alternativa del tipo suma, con su nombre y su carga de datos. Construir un valor es elegir una variante y darle sus datos, `Forma::Cuadrado(5)`; leerlo es descomponerlo con `match`.
- **Match y exhaustividad** — la construcción que inspecciona un valor suma, decide qué variante es y extrae sus datos en el mismo gesto (*pattern matching*). Su virtud decisiva es la **exhaustividad**: el compilador exige cubrir **todas** las variantes o dará error. Si mañana añades una variante `Circulo`, el compilador te señala cada `match` que quedó incompleto —el olvido se vuelve imposible—. Es también la base de `Option`/`Result`, la alternativa de la familia ML a `null`: en vez de un puntero nulo que revienta en tiempo de ejecución, un valor que es `Some(x)` **o** `None` y que el `match` te obliga a considerar.

## 🧩 Situación

Un pago es en efectivo, con tarjeta o por transferencia; y cada forma necesita datos distintos: la tarjeta guarda los últimos cuatro dígitos, la transferencia un IBAN, el efectivo nada. Sin tipos suma, la tentación es un `struct` con todos los campos posibles —la mayoría nulos según el caso— y una etiqueta de tipo que hay que recordar consultar; tarde o temprano alguien lee el IBAN de un pago en efectivo y el programa falla. El tipo suma modela esto con precisión: cada variante lleva **exactamente** los datos que le corresponden, ni uno más, y el `match` obliga a tratarlas todas. Cuando el negocio añade un cuarto medio de pago, el compilador recorre el programa y te señala cada lugar que olvidaste actualizar. El problema de hoy es una versión mínima de esa idea —una figura que es un cuadrado (con su lado) o un rectángulo (con ancho y alto), y hay que calcular el área— para que veas el patrón construir/match sin distracciones.

## 🧮 Modelo

- **Entrada** (stdin): una línea: `cuadrado <lado>` o `rectangulo <ancho> <alto>`
- **Salida** (stdout): `area=<área calculada>`
- **Regla:** cuadrado→lado²; rectangulo→ancho·alto

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `cuadrado 5` | `area=25` |
| `rectangulo 3 4` | `area=12` |
| `cuadrado 7` | `area=49` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER tipo y datos ; COINCIDIR tipo: cuadrado->l*l ; rectangulo->a*b
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys

t = sys.stdin.readline().split()
if t[0] == "cuadrado":
    area = int(t[1]) ** 2
else:  # rectangulo
    area = int(t[1]) * int(t[2])
print(f"area={area}")
```

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const t = readFileSync(0, "utf8").trim().split(/\s+/);
let area;
if (t[0] === "cuadrado") area = Number(t[1]) ** 2;
else area = Number(t[1]) * Number(t[2]);
console.log(`area=${area}`);
```

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const t: string[] = readFileSync(0, "utf8").trim().split(/\s+/);
let area: number;
if (t[0] === "cuadrado") area = Number(t[1]) ** 2;
else area = Number(t[1]) * Number(t[2]);
console.log(`area=${area}`);
```

### Java · [`java/Main.java`](implementaciones/java/Main.java) · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] t = br.readLine().trim().split("\\s+");
        long area;
        if (t[0].equals("cuadrado")) {
            long l = Long.parseLong(t[1]);
            area = l * l;
        } else {
            area = Long.parseLong(t[1]) * Long.parseLong(t[2]);
        }
        System.out.println("area=" + area);
    }
}
```

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;

string[] t = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
long area = t[0] switch {
    "cuadrado" => long.Parse(t[1]) * long.Parse(t[1]),
    _ => long.Parse(t[1]) * long.Parse(t[2]),
};
Console.WriteLine($"area={area}");
```

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
	t := strings.Fields(line)
	var area int64
	if t[0] == "cuadrado" {
		l, _ := strconv.ParseInt(t[1], 10, 64)
		area = l * l
	} else {
		a, _ := strconv.ParseInt(t[1], 10, 64)
		b, _ := strconv.ParseInt(t[2], 10, 64)
		area = a * b
	}
	fmt.Printf("area=%d\n", area)
}
```

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

enum Forma {
    Cuadrado(i64),
    Rectangulo(i64, i64),
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let t: Vec<&str> = s.split_whitespace().collect();
    let forma = if t[0] == "cuadrado" {
        Forma::Cuadrado(t[1].parse().unwrap())
    } else {
        Forma::Rectangulo(t[1].parse().unwrap(), t[2].parse().unwrap())
    };
    let area = match forma {
        Forma::Cuadrado(l) => l * l,
        Forma::Rectangulo(a, b) => a * b,
    };
    println!("area={area}");
}
```

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char tipo[32];
    if (scanf("%31s", tipo) != 1) return 1;
    long area;
    if (strcmp(tipo, "cuadrado") == 0) {
        long l;
        if (scanf("%ld", &l) != 1) return 1;
        area = l * l;
    } else {
        long a, b;
        if (scanf("%ld %ld", &a, &b) != 2) return 1;
        area = a * b;
    }
    printf("area=%ld\n", area);
    return 0;
}
```

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL: una columna 'tipo' + CASE modela las variantes.
WITH formas(tipo, a, b) AS (VALUES ('cuadrado', 5, 0))
SELECT printf('area=%d', CASE WHEN tipo = 'cuadrado' THEN a * a ELSE a * b END) AS resultado
FROM formas;
```

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
$t = preg_split('/\s+/', trim(fgets(STDIN)));
if ($t[0] === "cuadrado") {
    $area = (int) $t[1] * (int) $t[1];
} else {
    $area = (int) $t[1] * (int) $t[2];
}
echo "area=$area\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🧪 Laboratorio guiado: del código a la salida

Sigamos el caso `cuadrado 5`, que debe producir `area=25`, y de paso `rectangulo 3 4` → `area=12`. Los diez programas leen una etiqueta y sus datos, deciden la variante y calculan; conviene contrastar el que **tiene** tipo suma de verdad con los que lo **simulan**.

En **Rust**, el `enum Forma { Cuadrado(i64), Rectangulo(i64, i64) }` es un tipo suma nativo. El programa primero **construye** el valor: si la etiqueta es `"cuadrado"`, crea `Forma::Cuadrado(5)`; si no, `Forma::Rectangulo(...)`. Luego el `match forma { Forma::Cuadrado(l) => l * l, Forma::Rectangulo(a, b) => a * b }` **descompone**: reconoce la variante, liga `l` al 5 que iba dentro y devuelve 25. Lo esencial es lo que no se ve: si borraras el brazo `Rectangulo`, el programa **no compilaría** —el compilador exige cubrir todas las variantes—. Esa es la exhaustividad de la que habla Klabnik y Nichols.

En **C#**, no hay enum con datos, pero el `switch` de expresión con patrones se le acerca: `t[0] switch { "cuadrado" => p*p, _ => a*b }` sobre la etiqueta de texto. El brazo `_` es el comodín; produce 25 para `cuadrado 5`. La diferencia con Rust es que la exhaustividad aquí es sobre cadenas, no sobre variantes de un tipo cerrado: el compilador no puede saber qué etiquetas son válidas.

En **C**, no hay ni enum con datos ni match: el programa usa `strcmp(tipo, "cuadrado")` y un `if/else`, leyendo con `scanf` solo los números que la rama necesita (uno para el cuadrado, dos para el rectángulo). Es la simulación más cruda del tipo suma: la «etiqueta» es una cadena y la «exhaustividad» depende enteramente de que el programador no olvide una rama —no hay red de seguridad—. Go hace lo mismo con `iota` para enums simples, pero tampoco tiene sum types reales.

Los tres imprimen `area=25` para `cuadrado 5`; el verificador comprueba que las diez implementaciones coinciden carácter a carácter con lo que dicta `casos.json`.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `enum` con datos (Rust), sealed/record (Java/C#), etiqueta + campos (Go/C). |
| Semántica | Rust/Haskell garantizan exhaustividad; C usa una etiqueta manual. |
| Paradigmática | SQL usa una columna 'tipo' + CASE. |

La brecha real entre los diez lenguajes es **quién tiene tipos suma de verdad**. Rust los tiene nativos y con exhaustividad comprobada; Java moderna los aproxima con `sealed interface` + records y `switch` de patrones que también exige exhaustividad; C# con `record` y `switch` de patrones se acerca. En el otro extremo, **Go** solo ofrece `iota` para numerar constantes —un enum pobre, sin datos por variante y sin exhaustividad—, y la comunidad simula los sum types con interfaces y *type switches*. **C** no tiene nada: se usa un `enum` de etiquetas junto a un `union` y un `switch` que el compilador no obliga a completar. **TypeScript** ocupa un lugar curioso: sus *union types* discriminados (`{tipo: "cuadrado", lado: number} | {tipo: "rectangulo", ...}`) con un `switch` sobre el discriminante sí dan exhaustividad si activas `strict`, acercándose a la familia ML sin salir del ecosistema JavaScript. Cherny (*Programming TypeScript*) dedica un capítulo a esta técnica. **Python** cubre el hueco con `enum.Enum` para el caso simple y `match` estructural (3.10+) para descomponer, aunque sin comprobación de exhaustividad en tiempo de compilación. Hay además un eje de **coste**: el `match` es esencialmente un salto según la etiqueta, O(número de variantes) en el peor caso pero típicamente O(1) por *jump table*, tan barato como el `if/else` que sustituye.

## 🧬 El concepto en la familia

El tipo suma nace en la familia ML y de ahí irradia. En **Haskell**, `data Forma = Cuadrado Int | Rectangulo Int Int` es la definición canónica, y el compilador avisa (`-Wincomplete-patterns`) si un `case` no cubre todas las variantes. **OCaml** y **F#** tienen la misma construcción bajo el nombre de *variant types*. **Swift** copió el `enum` con datos asociados casi tal cual de Rust (o ambos de ML), y lo usa hasta para `Optional`. **Kotlin** lo emula con `sealed class`, y **Scala** con `sealed trait` + `case class`. El hilo común es doble: el conjunto de variantes es **cerrado** (nadie puede añadir una desde fuera, al revés que con la herencia abierta), y el compilador usa ese cierre para garantizar la exhaustividad. Reconocer que `Option`/`Maybe`, `Result`/`Either` y tu propio `Forma` son todos el mismo patrón —un valor que es «una de N cosas, cada una con sus datos»— es la idea que unifica media biblioteca estándar de los lenguajes modernos.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 100
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Olvidar una variante** → causa: un `match`/`switch` que no cubre todos los casos → solución: en Rust, Haskell o Java sellada el compilador lo impide; en lenguajes sin exhaustividad, activa las advertencias del compilador y evita el comodín `_`/`default` que silencia el olvido justo cuando añades una variante nueva.
- **Abusar del comodín `_`** → causa: un brazo `_ => ...` que traga cualquier variante futura y anula la comprobación de exhaustividad → solución: enumerar las variantes explícitamente cuando quieras que el compilador te avise al añadir una; reserva `_` solo para casos genuinamente «todos los demás».
- **Leer los datos de la variante equivocada** → causa: acceder a un campo que solo existe en otra variante (el IBAN de un pago en efectivo) → solución: extraer los datos **dentro** del brazo del `match`, donde el patrón garantiza qué campos existen; nunca antes de saber qué variante tienes.
- **Confundir enum simple con tipo suma** → causa: esperar que el `iota` de Go o un `enum` de C lleven datos por variante → solución: para datos por variante necesitas un ADT real (Rust, Swift, Java sellada) o simularlo con interfaces/uniones; el enum a secas es solo un conjunto de etiquetas.

## ❓ Preguntas frecuentes

- **¿Tipo suma o herencia?** Ambos modelan «una de varias cosas», pero con garantías opuestas. El tipo suma es **cerrado**: las variantes se conocen todas en un sitio y el compilador comprueba la exhaustividad, ideal cuando el conjunto de casos es estable y quieres seguridad. La herencia es **abierta**: cualquiera puede añadir una subclase después, ideal cuando esperas extensiones y prefieres el polimorfismo. Elige según cuál de las dos libertades necesitas.
- **¿Por qué 'algebraico'?** Porque los tipos se componen con las mismas operaciones que los números: el **producto** (registro: campo A y campo B; sus valores se multiplican) y la **suma** (variantes: A o B; sus valores se suman). De ahí «tipo algebraico de datos». La analogía llega lejos: el tipo con cero valores es como el 0 y el tipo con un solo valor (unit) es como el 1.
- **¿Qué relación tiene con `null`?** El tipo suma es la cura de `null`. En vez de un puntero que puede ser nulo y reventar sin aviso, la familia ML usa `Option<T>` = `Some(T) | None`: el `match` te **obliga** a manejar el caso vacío, y el «error del billón de dólares» —el `NullPointerException`— desaparece por construcción.
- **¿Y el rendimiento?** Un valor de tipo suma ocupa lo que su variante más grande más una pequeña etiqueta (el *tag*); el `match` sobre él suele compilarse a una tabla de saltos, tan rápido como un `switch` sobre enteros. No hay penalización por la seguridad que aporta.

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

> [⏮️ Clase 099](../../parte-6-datos-y-estructuras/099-registros-structs-y-clases/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 101 ⏭️](../../parte-6-datos-y-estructuras/101-igualdad-vs-identidad/README.md)
