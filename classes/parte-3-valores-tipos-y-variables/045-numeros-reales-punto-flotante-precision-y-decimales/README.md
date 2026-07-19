# Clase 045 — Números reales: punto flotante, precisión y decimales

> Parte **3 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Un número real matemático como 0.1 tiene infinitos vecinos infinitamente cercanos; una computadora, en cambio, solo dispone de una cantidad finita de bits para representarlo. El estándar **IEEE 754** —el que usan sin excepción los diez lenguajes de esta clase— resuelve esa imposibilidad guardando cada real como una fracción binaria de la forma *signo × mantisa × 2^exponente*, de manera análoga a la notación científica pero en base 2. El objetivo de esta clase es que dejes de pensar en `double` como "un número con decimales" y empieces a verlo como lo que realmente es: **la aproximación más cercana** que el hardware puede ofrecer dentro de una rejilla de valores representables.

De ahí se sigue la consecuencia central: 0.1 no cabe exactamente en base 2, igual que 1/3 no cabe exactamente en base 10. Su representación binaria es periódica y debe truncarse, así que `0.1 + 0.2` produce `0.30000000000000004`. No es un fallo del lenguaje ni de tu máquina; es el **error de representación**, inevitable y reproducible en cualquier procesador conforme a IEEE 754. Como explican Sebesta y Scott, este es el precio de tener un tipo de tamaño fijo (64 bits) capaz de cubrir un rango gigantesco de magnitudes: se sacrifica exactitud decimal a cambio de eficiencia y uniformidad.

Por eso el laboratorio no imprime el real "crudo", sino que lo **formatea a un número fijo de decimales** y fuerza el punto como separador decimal. Aprenderás que el formateo hace dos cosas a la vez —redondear el valor aproximado y neutralizar la cultura del sistema (que en español suele usar coma)— y por qué esa combinación es la única forma robusta de mostrar cantidades a un humano.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Operar con reales (suma y producto).
2. Formatear un real con un número fijo de decimales.
3. Explicar por qué el punto flotante es aproximado.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Punto flotante | Representación aproximada de los reales |
| 2 | Formateo con decimales | Mostrar 2 decimales de forma consistente |
| 3 | Cultura/locale | Punto vs. coma decimal según el sistema |
| 4 | Redondeo | El formateo redondea; cuidado con los empates |

## 📖 Definiciones y características

Un valor de **punto flotante** de doble precisión (el `double` de casi todos estos lenguajes, el único `number` de JavaScript) ocupa 64 bits repartidos en tres campos: 1 bit de signo, 11 de exponente y 52 de mantisa (fracción). Con esa mantisa se obtienen unos 15-17 dígitos decimales significativos, y con el exponente un rango que va desde ~10⁻³⁰⁸ hasta ~10³⁰⁸. La clave conceptual, siguiendo a Scott en *Programming Language Pragmatics*, es que los valores representables **no están distribuidos de manera uniforme**: cerca del cero hay muchos, muy juntos; para magnitudes grandes hay pocos, muy separados. Entre dos representables consecutivos existe un hueco, y cualquier real que caiga en ese hueco se redondea al más cercano.

La **precisión** es, entonces, el tamaño de ese hueco relativo al valor: es limitada y, sobre todo, es *relativa*, no absoluta. Por eso sumar un número muy pequeño a uno muy grande puede no cambiar nada (el pequeño desaparece en el redondeo), y por eso comparar dos reales con `==` es frágil. El estándar reserva además valores especiales que conviene reconocer: `Inf` (infinito, resultado de desbordar el rango o dividir por cero) y `NaN` (*Not a Number*, resultado de operaciones indefinidas como 0/0), este último con la propiedad desconcertante de no ser igual ni a sí mismo.

El **formateo** con N decimales convierte el real interno en texto legible aplicando un redondeo —normalmente *redondeo al par más cercano*, el modo por defecto de IEEE 754, que en los empates elige el dígito par para no sesgar sumas largas—. Y la **cultura invariante** (`Locale.US` en Java, `InvariantCulture` en C#) fija el punto como separador decimal con independencia del idioma del sistema operativo, evitando que en una máquina configurada en español el `4.00` se convierta en `4,00` y rompa la comparación con la salida esperada.

En términos de términos clave:

- **Punto flotante** — real codificado como signo × mantisa × 2^exponente (IEEE 754 binario64).
- **Error de representación** — diferencia entre el real deseado y el representable más cercano; origen de `0.1 + 0.2 != 0.3`.
- **Precisión relativa** — ~15-17 dígitos significativos; el hueco entre representables crece con la magnitud.
- **Formateo** — conversión a texto con N decimales, que además redondea el valor aproximado.
- **Cultura invariante** — política de formato que impone el punto decimal sin importar el locale.

## 🧩 Situación

Imagina un carrito de compra que suma 0.10 + 0.20 y compara el total con 0.30 para decidir si aplica un descuento. La comparación falla, el descuento no se aplica, y el usuario reporta un "bug" que no existe en ningún `if` que escribiste: existe en los bits. Este es el escenario que aquí reproducimos en miniatura. El caso `0.1 0.2` de `casos.json` espera exactamente `suma=0.30 producto=0.02`, y solo lo obtenemos porque el formateo a dos decimales redondea `0.30000000000000004` de vuelta a `0.30` antes de mostrarlo.

Este mismo mecanismo es la razón histórica por la que en aplicaciones financieras se desaconseja usar `float`/`double` para dinero (Bloch lo señala en *Effective Java*): los errores de representación se acumulan en sumas largas y producen centavos fantasma. La respuesta profesional es un tipo decimal exacto (`decimal` en C#, `BigDecimal` en Java, `Decimal` de Python) o trabajar en la unidad mínima (centavos como enteros). El laboratorio muestra la alternativa más simple y universal: **fijar los decimales al presentar** y forzar la cultura, para que el mismo programa dé la misma salida en una máquina en inglés y en una en español.

## 🧮 Modelo

- **Entrada** (stdin): una línea `a b` (dos reales)
- **Salida** (stdout): `suma=<a+b con 2 decimales> producto=<a*b con 2 decimales>`
- **Regla:** suma = a + b ; producto = a * b (ambos a 2 decimales)

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `1.5 2.5` | `suma=4.00 producto=3.75` |
| `0.1 0.2` | `suma=0.30 producto=0.02` |
| `10 3` | `suma=13.00 producto=30.00` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER a, b
ESCRIBIR "suma=" FORMATEAR(a+b,2) " producto=" FORMATEAR(a*b,2)
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

a, b = map(float, sys.stdin.readline().split())
print(f"suma={a + b:.2f} producto={a * b:.2f}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const [a, b] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`suma=${(a + b).toFixed(2)} producto=${(a * b).toFixed(2)}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const [a, b]: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`suma=${(a + b).toFixed(2)} producto=${(a * b).toFixed(2)}`);
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
        double a = Double.parseDouble(p[0]);
        double b = Double.parseDouble(p[1]);
        System.out.printf(Locale.US, "suma=%.2f producto=%.2f%n", a + b, a * b);
    }
}
```

### C# · `dotnet run`

```csharp
using System;
using System.Globalization;

var inv = CultureInfo.InvariantCulture;
string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
double a = double.Parse(p[0], inv);
double b = double.Parse(p[1], inv);
Console.WriteLine($"suma={(a + b).ToString("F2", inv)} producto={(a * b).ToString("F2", inv)}");
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
	f := strings.Fields(line)
	a, _ := strconv.ParseFloat(f[0], 64)
	b, _ := strconv.ParseFloat(f[1], 64)
	fmt.Printf("suma=%.2f producto=%.2f\n", a+b, a*b)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let v: Vec<f64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    println!("suma={:.2} producto={:.2}", v[0] + v[1], v[0] * v[1]);
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    double a, b;
    if (scanf("%lf %lf", &a, &b) != 2) return 1;
    printf("suma=%.2f producto=%.2f\n", a + b, a * b);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL formatea reales con printf dentro de la consulta.
WITH pares(a, b) AS (VALUES (1.5, 2.5), (0.1, 0.2), (10, 3))
SELECT printf('suma=%.2f producto=%.2f', a + b, a * b) AS resultado
FROM pares;
```

### PHP · `php main.php`

```php
<?php
[$a, $b] = preg_split('/\s+/', trim(fgets(STDIN)));
$a = (float) $a;
$b = (float) $b;
printf("suma=%.2f producto=%.2f\n", $a + $b, $a * $b);
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔎 Recorrido guiado por el código

Sigamos el camino que recorre una línea de entrada hasta convertirse en la salida exacta que exige `casos.json`, tomando como caso testigo el más revelador: `0.1 0.2`, cuyo esperado es `suma=0.30 producto=0.02`.

En **Python**, la primera línea `a, b = map(float, sys.stdin.readline().split())` hace tres cosas encadenadas: `readline()` trae la línea `"0.1 0.2\n"`, `split()` la parte en la lista `["0.1", "0.2"]`, y `map(float, …)` convierte cada trozo en un `double` de 64 bits. Aquí ocurre el error de representación silencioso: ni 0.1 ni 0.2 caben exactos en binario, así que `a` y `b` ya guardan aproximaciones. La segunda línea es donde vive toda la lección: dentro de la f-string, `` `{a + b:.2f}` `` no imprime el valor crudo `0.30000000000000004`, sino que el especificador `:.2f` **redondea a dos decimales** y produce el texto `0.30`. El producto `a * b` vale internamente algo como `0.020000000000000004`, y `:.2f` lo colapsa a `0.02`. Por eso la salida es `suma=0.30 producto=0.02` y no las colas binarias. Con el caso `1.5 2.5`, que sí son exactos en binario, la mecánica es idéntica y da `suma=4.00 producto=3.75`.

En **JavaScript**, `readFileSync(0, "utf8")` lee todo el stdin (el descriptor `0`), `.trim().split(/\s+/)` lo separa por espacios y `.map(Number)` convierte a los únicos números que JS conoce: `double` IEEE 754. El formateo cambia de nombre pero no de idea: `(a + b).toFixed(2)` devuelve **una cadena** —no un número— con exactamente dos decimales, `"0.30"`. Es importante notar que `toFixed` ya redondea; devolver una cadena es intencional, porque un número no puede "recordar" que quiere mostrarse con dos decimales.

El contraste más instructivo es **Java**, porque hace explícito lo que Python y JS ocultan. La línea `System.out.printf(Locale.US, "suma=%.2f producto=%.2f%n", a + b, a * b)` pasa `Locale.US` como primer argumento *a propósito*: sin él, en una JVM configurada en español el especificador `%.2f` imprimiría `0,30` con coma, y el verificador lo marcaría como fallo frente al esperado `0.30`. C# hace lo mismo con `InvariantCulture` en `(a + b).ToString("F2", inv)`. Esta es la diferencia semántica clave entre lenguajes: unos (Python, C, Go) usan el punto por defecto en `%.2f`; otros (Java, C#) son sensibles al locale y obligan a fijarlo.

Finalmente **C** revela el nivel más bajo: `scanf("%lf %lf", &a, &b)` lee dos `double` (`%lf` = *long float*), y la condición `!= 2` verifica que ambos se parsearon antes de continuar. Su `printf("suma=%.2f producto=%.2f\n", …)` usa el mismo especificador `%.2f` que Python heredó de C —no es casualidad: casi toda la familia tomó prestada la sintaxis `printf` de Kernighan y Ritchie—. En C el punto decimal depende del `locale` del programa, que por defecto es la "C locale" neutra, así que aquí también sale `0.30`.

## 🔬 Comparación

Todos estos lenguajes comparten el mismo `double` de 64 bits y, por tanto, los mismos errores de representación: en eso son idénticos. Divergen en dos ejes prácticos: **cómo se nombra el redondeo al formatear** y **si el resultado respeta o no la cultura del sistema**. La tabla resume esas diferencias en las tres clases habituales.

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | El redondeo a 2 decimales se escribe distinto: `%.2f` (Python/C/Go/Java/PHP heredado de `printf`), `toFixed(2)` (JS/TS, y devuelve cadena), `ToString("F2")` (C#), `{:.2}` (Rust con `format!`). |
| Semántica | Punto vs. coma: Python, C, Go y Rust usan el punto por defecto; Java y C# son sensibles al locale y exigen fijar `Locale.US` / `InvariantCulture` para no imprimir `0,30`. El modo de redondeo por defecto es "al par más cercano" en toda la familia. |
| Paradigmática | SQL no lee stdin: `printf('%.2f producto=%.2f', a+b, a*b)` opera fila a fila sobre una tabla de casos declarada con `VALUES`, y el verificador la marca como ilustrativa. |

Un matiz de tamaño que conviene recordar: en C y Java coexisten `float` (32 bits, ~7 dígitos) y `double` (64 bits, ~15-17). El laboratorio usa siempre doble precisión, que es lo que Python (`float`), JavaScript (`number`) y Rust (`f64` por inferencia) ofrecen por defecto. Usar `float` de 32 bits para estos mismos casos habría ampliado el error de representación, aunque el formateo a 2 decimales lo seguiría ocultando.

## 🧬 El concepto en la familia

En Ruby: `format('%.2f', x)`. En Haskell: `printf "%.2f" x` (de `Text.Printf`). En Swift, `String(format: "%.2f", x)`. El patrón se repite porque el problema es el mismo en toda la familia: al compartir IEEE 754, comparten el error de representación, y todos lo resuelven en la capa de presentación con un redondeo a decimales fijos. Lo único que cambia de un lenguaje a otro es el nombre de la función de formato y si arrastra o no la cultura del sistema.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 045
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Ver `4,00` en vez de `4.00`** → causa: la JVM o el runtime .NET heredan un locale con coma decimal → solución: forzar cultura invariante (`Locale.US` en Java, `InvariantCulture` en C#); Python, C y Go no sufren esto porque `%.2f` usa el punto por defecto.
- **Comparar reales con `==`** → causa: esperar igualdad exacta entre valores que sufrieron redondeo → solución: comparar `abs(a - b) < epsilon` con una tolerancia, o formatear ambos a N decimales y comparar las cadenas.
- **Acumular céntimos fantasma en dinero** → causa: sumar muchos `double` (cada suma redondea) → solución: un tipo decimal exacto (`BigDecimal`, `decimal`, `Decimal`) o trabajar en enteros de la unidad mínima.
- **Confiar en que `toFixed`/`%.2f` "arregla" el número** → causa: creer que redondear para mostrar corrige el valor interno → solución: entender que solo cambia la *presentación*; el `double` sigue siendo aproximado para cálculos posteriores.

## ❓ Preguntas frecuentes

- **¿Por qué 0.1+0.2 no es 0.3?** Porque 0.1 y 0.2 son fracciones periódicas en base 2 (como 1/3 lo es en base 10) y deben truncarse a 52 bits de mantisa; los errores de ambas se suman y el resultado cae en un representable ligeramente mayor: `0.30000000000000004`.
- **¿Cómo manejo dinero entonces?** Con decimales fijos y formateo solo para *mostrar*, y para *calcular* usando un tipo decimal exacto (`decimal`/`BigDecimal`/`Decimal`) o enteros de centavos. Nunca sumes grandes cantidades de `double` esperando exactitud contable.
- **¿Qué son `NaN` e `Inf`?** Valores especiales de IEEE 754: `Inf` aparece al desbordar el rango o dividir por cero; `NaN` al hacer operaciones indefinidas como 0/0 o `sqrt(-1)`. `NaN` no es igual ni a sí mismo, así que `x != x` es la forma clásica de detectarlo.
- **¿Todos los lenguajes dan el mismo resultado erróneo?** Sí, y eso es una garantía, no un accidente: al implementar todos IEEE 754 binario64, `0.1 + 0.2` produce idénticos bits en Python, Java, Go o Rust, lo que hace el comportamiento reproducible entre plataformas.

## 🔗 Referencias

**Libros de la parte:**

- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson), cap. tipos de datos primitivos (tipos numéricos de punto flotante).
- B. C. Pierce — *Types and Programming Languages* (MIT Press), tipos base y su semántica.
- M. L. Scott — *Programming Language Pragmatics* (4ª ed., Morgan Kaufmann), representación en memoria y valores de punto flotante.

**Libros de los lenguajes del núcleo:**

- L. Ramalho — *Fluent Python* (2ª ed., O'Reilly), cap. de números (`float` vs. `Decimal`, precisión).
- M. Haverbeke — *Eloquent JavaScript* (3ª ed.) — un único tipo `Number` IEEE 754 — [gratis online](https://eloquentjavascript.net/).
- B. Cherny — *Programming TypeScript* (O'Reilly), tipo `number`.
- J. Bloch — *Effective Java* (3ª ed., Addison-Wesley), evitar `float`/`double` cuando se necesitan respuestas exactas (dinero).
- J. Skeet — *C# in Depth* (4ª ed., Manning), `double` vs. `decimal` y formato con cultura.
- A. Donovan y B. Kernighan — *The Go Programming Language* (Addison-Wesley), tipos de punto flotante `float32`/`float64`.
- S. Klabnik y C. Nichols — *The Rust Programming Language* — tipos `f32`/`f64` — [gratis online](https://doc.rust-lang.org/book/).
- B. Kernighan y D. Ritchie — *The C Programming Language* (2ª ed., Prentice Hall), tipos `float`/`double` y `printf` con `%f`.
- C. J. Date — *SQL and Relational Theory* (3ª ed., O'Reilly), tipos y dominios.
- J. Lockhart — *Modern PHP* (O'Reilly), tipos escalares.

---

> [⏮️ Clase 044](../../parte-3-valores-tipos-y-variables/044-enteros-tamano-signo-desbordamiento-y-bases/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 046 ⏭️](../../parte-3-valores-tipos-y-variables/046-booleanos-y-valores-de-verdad/README.md)
