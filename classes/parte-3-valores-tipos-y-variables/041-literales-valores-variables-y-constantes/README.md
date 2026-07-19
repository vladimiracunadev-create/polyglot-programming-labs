# Clase 041 — Literales, valores, variables y constantes

> Parte **3 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — clase insignia con las 10 implementaciones del núcleo verificadas en CI.

---

## 🎯 Objetivo

Entender los cuatro ladrillos con los que empieza todo programa: el **literal** (un valor escrito directamente en el código, como `15000`), el **valor** (el dato en memoria), la **variable** (un nombre que apunta a un valor y puede cambiar) y la **constante** (un nombre cuyo valor no debe cambiar). Verás que el concepto es idéntico en los 10 lenguajes del núcleo, pero **cómo se declara, si lleva tipo, si es mutable y cómo se formatea** cambia de una familia a otra.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. **Distinguir** literal, valor, variable y constante con ejemplos propios.
2. **Declarar** una constante y una variable en cada lenguaje del núcleo.
3. **Explicar** por qué en Rust todo es inmutable por defecto y en Python/PHP no.
4. **Implementar** el mismo cálculo de venta en los 10 lenguajes con salida idéntica.
5. **Reconocer** el mismo concepto en primos de otras familias (Ruby, Kotlin, Haskell).

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Literal vs. valor | Separa lo escrito en el código del dato en memoria |
| 2 | Variable | Es el nombre que permite reutilizar y cambiar un valor |
| 3 | Constante | Comunica intención: "esto no cambia" |
| 4 | Declaración e inicialización | Cada lenguaje exige (o infiere) el tipo de forma distinta |
| 5 | Mutabilidad por defecto | Rust/const vs. Python/PHP: decisiones de diseño opuestas |
| 6 | Formato de salida | La cultura/locale y el formateo decimal difieren entre runtimes |

## 📖 Definiciones y características

- **Literal** — valor escrito directamente en el código fuente (`15000`, `"hola"`, `true`). Clave: no tiene nombre.
- **Valor** — el dato concreto que existe en memoria durante la ejecución. Clave: es lo que se calcula y compara.
- **Variable** — nombre asociado a un valor que puede reasignarse. Clave: introduce estado que cambia en el tiempo.
- **Constante** — nombre asociado a un valor que no debe reasignarse. Clave: intención + seguridad.
- **Declaración** — acto de introducir un nombre en un ámbito. Clave: en lenguajes estáticos fija el tipo.
- **Inicialización** — dar el primer valor a una variable. Clave: usar una variable sin inicializar es un error clásico.
- **Mutabilidad** — si un enlace nombre→valor puede cambiar. Clave: Rust la niega por defecto; Python la permite siempre.

## 🧩 Situación

Una tienda calcula el total de una venta a partir de tres datos: el **precio unitario**, la **cantidad** y un **descuento** (0 a 1). Es el problema mínimo donde aparecen literales, variables y constantes, y una operación aritmética.

## 🧮 Modelo

- **Entrada** (stdin, una línea): `precio_unitario cantidad descuento`
- **Salida** (stdout): `Total: <total con 2 decimales>`
- **Regla:** `total = precio_unitario * cantidad * (1 - descuento)`
- **Casos límite:** cantidad `0` ⇒ total `0.00`; descuento `0` ⇒ sin rebaja.

Especificación y verificación en [`casos.json`](casos.json).

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER precio_unitario, cantidad, descuento
subtotal <- precio_unitario * cantidad
total    <- subtotal * (1 - descuento)
ESCRIBIR "Total: " + FORMATEAR(total, 2 decimales)
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`. Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

# Literales y constantes: los valores se leen y se nombran.
precio_str, cantidad_str, descuento_str = sys.stdin.readline().split()

PRECIO_UNITARIO = float(precio_str)   # tipo dinámico, inferido en tiempo de ejecución
CANTIDAD = int(cantidad_str)
DESCUENTO = float(descuento_str)

subtotal = PRECIO_UNITARIO * CANTIDAD
total = subtotal * (1 - DESCUENTO)

print(f"Total: {total:.2f}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

// Números en JS: un solo tipo `number` (doble de 64 bits) para todo.
const [precio, cantidad, descuento] = readFileSync(0, "utf8")
  .trim()
  .split(/\s+/)
  .map(Number);

const subtotal = precio * cantidad;
const total = subtotal * (1 - descuento);

console.log(`Total: ${total.toFixed(2)}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

// TypeScript añade tipos estáticos sobre JavaScript: se comprueban al compilar.
const [precio, cantidad, descuento]: number[] = readFileSync(0, "utf8")
  .trim()
  .split(/\s+/)
  .map(Number);

const subtotal: number = precio * cantidad;
const total: number = subtotal * (1 - descuento);

console.log(`Total: ${total.toFixed(2)}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Locale;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");

        // Tipado estático nominal: cada valor declara su tipo.
        final double precioUnitario = Double.parseDouble(p[0]);
        final int cantidad = Integer.parseInt(p[1]);
        final double descuento = Double.parseDouble(p[2]);

        double subtotal = precioUnitario * cantidad;
        double total = subtotal * (1 - descuento);

        System.out.printf(Locale.US, "Total: %.2f%n", total);
    }
}
```

### C# · `dotnet run`

```csharp
using System;
using System.Globalization;

// C# sobre el CLR: tipado estático con cultura invariante para el formato.
string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);

double precioUnitario = double.Parse(p[0], CultureInfo.InvariantCulture);
int cantidad = int.Parse(p[1], CultureInfo.InvariantCulture);
double descuento = double.Parse(p[2], CultureInfo.InvariantCulture);

double subtotal = precioUnitario * cantidad;
double total = subtotal * (1 - descuento);

Console.WriteLine("Total: " + total.ToString("F2", CultureInfo.InvariantCulture));
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
	reader := bufio.NewReader(os.Stdin)
	linea, _ := reader.ReadString('\n')
	campos := strings.Fields(linea)

	// Go: tipado estático explícito; conversión float64(cantidad) obligatoria.
	precioUnitario, _ := strconv.ParseFloat(campos[0], 64)
	cantidad, _ := strconv.Atoi(campos[1])
	descuento, _ := strconv.ParseFloat(campos[2], 64)

	subtotal := precioUnitario * float64(cantidad)
	total := subtotal * (1 - descuento)

	fmt.Printf("Total: %.2f\n", total)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut entrada = String::new();
    std::io::stdin().read_to_string(&mut entrada).unwrap();
    let campos: Vec<&str> = entrada.split_whitespace().collect();

    // Rust: inmutable por defecto (`let`), tipos explícitos, conversión con `as`.
    let precio_unitario: f64 = campos[0].parse().unwrap();
    let cantidad: i64 = campos[1].parse().unwrap();
    let descuento: f64 = campos[2].parse().unwrap();

    let subtotal = precio_unitario * cantidad as f64;
    let total = subtotal * (1.0 - descuento);

    println!("Total: {total:.2}");
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    double precio_unitario, descuento;
    long cantidad;

    /* C: tipos primitivos de tamaño fijo; scanf convierte el texto de entrada. */
    if (scanf("%lf %ld %lf", &precio_unitario, &cantidad, &descuento) != 3) {
        return 1;
    }

    double subtotal = precio_unitario * (double)cantidad;
    double total = subtotal * (1.0 - descuento);

    printf("Total: %.2f\n", total);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL es declarativo: no lee stdin como los lenguajes imperativos. En vez de
-- una variable que se asigna, se describe el cálculo sobre una tabla de valores.
-- Esta consulta demuestra la misma fórmula para los tres casos de casos.json.
WITH ventas(precio_unitario, cantidad, descuento) AS (
    VALUES (15000.0, 2, 0.10),
           (999.9, 3, 0.0),
           (5000.0, 0, 0.20)
)
SELECT printf('Total: %.2f', precio_unitario * cantidad * (1 - descuento)) AS resultado
FROM ventas;
```

### PHP · `php main.php`

```php
<?php
// PHP: dinámico y débilmente tipado; las variables llevan el prefijo $.
$linea = trim(fgets(STDIN));
[$precio, $cantidad, $descuento] = preg_split('/\s+/', $linea);

$precioUnitario = (float) $precio;
$cantidadInt = (int) $cantidad;
$descuentoFloat = (float) $descuento;

$subtotal = $precioUnitario * $cantidadInt;
$total = $subtotal * (1 - $descuentoFloat);

printf("Total: %.2f\n", $total);
```

> SQL es declarativo: no lee de stdin como los demás. Su implementación muestra la misma fórmula
> sobre una tabla de casos, y por eso el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| **Sintáctica** | `PRECIO = 15000` (Python) vs. `const precio = 15000;` (JS) vs. `final double precio = 15000;` (Java). |
| **Semántica** | Python/PHP infieren y permiten reasignar; Java/C#/Go/Rust/C fijan tipo; Rust exige `mut` para mutar; C usa tamaños fijos. |
| **Paradigmática** | SQL no tiene "variable que se asigna": describe el resultado, no los pasos. |

## 🧬 El concepto en la familia

- **Familia scripting dinámico** (Ruby, Perl, Lua): como Python/PHP, sin declarar tipo. Ruby: `precio = 15000`, constante por convención con mayúscula (`PRECIO`).
- **Familia JVM** (Kotlin): `val precio = 15000.0` (inmutable) vs. `var` (mutable) — inferencia como en Rust.
- **Familia funcional** (Haskell): `precio = 15000` es una **definición inmutable**, no una asignación; no existe "variable que cambia".
- **Familia C/llaves** (C++): `const double precio = 15000;` — igual que C con `const`.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 041
```

El verificador alimenta cada caso por stdin, compara la salida y omite los lenguajes cuyo
toolchain no esté instalado (degradación silenciosa).

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md): añade un **impuesto** del 19 % después del descuento y resuélvelo en **Kotlin** (no explicado paso a paso), apoyándote en la implementación de Java.

## ⚠️ Errores comunes

- **Formato con coma decimal** (síntoma: `Total: 27000,00`) → causa: locale del sistema → solución: forzar cultura invariante (`Locale.US`, `CultureInfo.InvariantCulture`).
- **Porcentaje entero** (síntoma: descuento ignorado) → causa: `1 - descuento` calculado en enteros → solución: usar tipo real.
- **Usar variable sin inicializar** (C) → causa: valor basura → solución: inicializar siempre.

## ❓ Preguntas frecuentes

- **¿Por qué Rust obliga a `mut`?** Para que la mutación sea una decisión visible, no un accidente.
- **¿PHP es débilmente tipado?** Sí: convierte entre tipos automáticamente; por eso el `(float)`/`(int)` explícito documenta la intención.

## 🔗 Referencias

**Libros de la parte:**

- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson), cap. tipos y variables.
- B. C. Pierce — *Types and Programming Languages* (MIT Press).
- M. L. Scott — *Programming Language Pragmatics* (4ª ed., Morgan Kaufmann).

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

> [⏮️ Clase 040](../../parte-2-herramientas-toolchains-y-anatomia-de-comandos/040-variables-de-entorno-rutas-y-el-path-en-windows-y-unix/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 042 ⏭️](../../parte-3-valores-tipos-y-variables/042-declaracion-asignacion-e-inicializacion/README.md)
