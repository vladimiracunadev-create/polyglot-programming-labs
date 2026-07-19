# Clase 041 — Literales, valores, variables y constantes

> Parte **3 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — clase insignia con las 10 implementaciones del núcleo verificadas en CI.

---

## 🎯 Objetivo

Todo programa manipula valores, pero un valor puro —el número `27000`, la cadena `"hola"`— no tiene nombre ni domicilio: existe solo mientras alguien lo sostiene. Las cuatro nociones de esta clase son las herramientas con que un lenguaje sostiene, nombra y protege valores. Un **literal** es un valor escrito de forma directa en el texto del programa (`15000`, `"hola"`, `true`): el compilador o el intérprete lo reconoce por su sintaxis y fabrica el valor correspondiente. Un **valor** es ese dato ya materializado en memoria durante la ejecución, con un tipo que determina qué se puede hacer con él. Una **variable** es un nombre que se enlaza a un valor y que puede reenlazarse a otro más tarde; introduce estado que cambia en el tiempo. Una **constante** es un nombre cuyo enlace se promete inmutable, una intención que el lenguaje convierte —o no— en garantía.

El porqué de fondo es el **enlace (binding) entre un nombre y un valor**, que Sebesta y Scott ponen en el centro de su análisis de los lenguajes. Nombrar un valor es lo que permite reutilizarlo, razonar sobre él y comunicar intención; sin nombres, un programa sería una cascada ilegible de literales repetidos. Y la pregunta decisiva es *cuándo* y *con qué rigidez* se fija cada enlace —el **binding time** de Scott—: ¿el tipo se decide al compilar (Java, Rust, C) o al ejecutar (Python, PHP)? ¿el enlace nombre→valor puede cambiar (variable) o queda sellado (constante)? Esas dos preguntas, aplicadas a un cálculo tan simple como el total de una venta, separan a las diez familias del núcleo.

Comparar los lenguajes revela que el concepto es universal pero las decisiones de diseño son opuestas: Rust hace inmutable *por defecto* y obliga a pedir `mut` para lo contrario; Python trata los nombres como etiquetas que se pegan y despegan de objetos, sin declaración ni tipo escrito. Ver el mismo problema resuelto en ambos extremos —y en los siete que quedan en medio— enseña más sobre variables que cualquier definición aislada.

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

Detrás de estos términos hay una distinción que Sebesta trata con cuidado: la de **l-value** y **r-value**. Un nombre que aparece a la izquierda de una asignación se usa como *l-value* —designa un lugar donde guardar—, mientras que a la derecha se usa como *r-value* —designa el valor que se lee—. En `total = subtotal * (1 - descuento)`, `total` es l-value y todo lo de la derecha se evalúa como r-value. Un literal como `15000` solo puede ser r-value: no tiene lugar propio al que asignar, y por eso se puede escribir `x = 3` pero nunca `3 = x`.

La otra distinción, subrayada por Scott, es entre el **modelo de valores** y el **modelo de referencias**. En C o en un `int` de Java, la variable *es* la caja que contiene los bits del valor; asignar copia esos bits. En Python la variable es una **etiqueta** que se adhiere a un objeto que vive en otra parte —Ramalho insiste en que en Python "todo es objeto" y los nombres no son cajas sino post-its—; asignar mueve la etiqueta, no copia el objeto. Esta diferencia, invisible en un cálculo aritmético como el de esta clase, se vuelve central en cuanto aparecen listas y estructuras mutables.

Finalmente, **constante** significa cosas distintas según el lenguaje, y conviene no dejarse engañar por la palabra compartida. El `final` de Java y el `const` de C impiden reasignar el nombre y lo verifican en tiempo de compilación; el `PRECIO_UNITARIO` en mayúsculas de Python es solo una *convención* —nada en el intérprete impide reasignarlo, es un acuerdo entre programadores—. Rust va más lejos: `let` ya es inmutable, y una `const` de Rust debe ser evaluable en tiempo de compilación. La misma idea, tres niveles de garantía: convención, chequeo del compilador y valor conocido antes de ejecutar.

## 🧩 Situación

Una tienda calcula el total de una venta a partir de tres datos: el **precio unitario**, la **cantidad** y un **descuento** expresado como fracción entre 0 y 1. Elegimos este problema porque es el más pequeño en el que coexisten las cuatro nociones sin ruido: el descuento entra como literal (`0.10`), los tres datos se leen y se nombran, y el resultado exige una operación aritmética y un formateo con dos decimales. La regla `total = precio_unitario * cantidad * (1 - descuento)` obliga además a mezclar un entero (la cantidad) con reales (precio y descuento), lo que fuerza a cada lenguaje a mostrar su política de conversión: Go y Rust exigen convertir la cantidad a real de forma explícita (`float64(cantidad)`, `cantidad as f64`), mientras Python y PHP lo hacen en silencio. Los casos límite del contrato —cantidad `0` que da `0.00`, descuento `0` que no rebaja— confirman que el mismo código responde bien en los bordes.

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

## 🔎 Recorrido guiado por el código

Sigamos el primer caso de [`casos.json`](casos.json): la entrada `15000 2 0.10` debe producir exactamente `Total: 27000.00`. Veremos cómo tres lenguajes de familias opuestas llegan a esa misma línea.

En **Python**, `sys.stdin.readline().split()` lee `"15000 2 0.10"` y lo parte en la lista `["15000", "2", "0.10"]`, que la desestructuración reparte en `precio_str`, `cantidad_str`, `descuento_str`. Aquí las tres siguen siendo *cadenas*: el literal de entrada aún no es un número. La conversión ocurre en las tres líneas siguientes, `float(precio_str)`, `int(cantidad_str)`, `float(descuento_str)`, donde nacen los valores numéricos y quedan enlazados a nombres en MAYÚSCULAS. Esas mayúsculas no crean constantes reales —Python permitiría reasignar `PRECIO_UNITARIO`—; son la *convención* que documenta la intención. El cálculo `PRECIO_UNITARIO * CANTIDAD` mezcla un `float` con un `int` y Python promueve el resultado a `float` sin avisar: `15000.0 * 2 = 30000.0`. Luego `30000.0 * (1 - 0.10) = 30000.0 * 0.9 = 27000.0`. La magia final está en `f"Total: {total:.2f}"`: el mini-lenguaje de formato `:.2f` fuerza dos decimales, convirtiendo `27000.0` en el texto `27000.00` que el contrato exige.

En **C**, la historia del tipo es lo opuesto: los nombres se declaran *antes* de tener valor. `double precio_unitario, descuento; long cantidad;` reserva las cajas con su tipo fijo, y solo después `scanf("%lf %ld %lf", ...)` las llena leyendo el texto de entrada. Los especificadores `%lf` (double) y `%ld` (long) le dicen a `scanf` cómo interpretar cada campo; el `if (... != 3)` comprueba que se leyeron los tres valores. Nótese la conversión *explícita* `(double)cantidad` en `precio_unitario * (double)cantidad`: C no promueve tan libremente como Python, y el autor deja escrito que la cantidad entera debe leerse como real para no truncar. Con `1.0 - descuento` (el `1.0` es literal real, no entero) se evita hacer aritmética entera. El `printf("Total: %.2f\n", total)` cierra con el mismo `%.2f` de dos decimales, produciendo `Total: 27000.00`.

En **Rust** se ve el tercer temperamento: inmutabilidad por defecto y tipos anotados. `let precio_unitario: f64 = campos[0].parse().unwrap();` declara, anota el tipo `f64` y enlaza en una sola expresión; sin `mut`, ese enlace queda sellado. El `parse()` deduce a qué tipo convertir gracias a la anotación (`: f64`, `: i64`), y `unwrap()` aborta si el texto no fuese un número válido. Como Rust tampoco mezcla enteros y reales sin permiso, la conversión es visible: `cantidad as f64` en `precio_unitario * cantidad as f64`. La interpolación `println!("Total: {total:.2}")` usa `{total:.2}` —la sintaxis de Rust para dos decimales— y emite `Total: 27000.00`. Compara los tres: Python convierte tarde y en silencio, C declara el tipo antes del valor, Rust lo anota junto al valor y lo congela. Tres caminos, una salida idéntica.

## 🔬 Comparación

El mismo cálculo revela que "declarar una variable" no significa lo mismo en cada familia. Lo que en Python es pegar una etiqueta a un objeto, en C es reservar una caja de bits de tamaño fijo, y en Rust es firmar un contrato de tipo e inmutabilidad. Estas diferencias no son cosmética: gobiernan qué errores atrapa el compilador, cuándo, y qué libertades tiene el programador.

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| **Sintáctica** | `PRECIO = 15000` (Python) vs. `const precio = 15000;` (JS) vs. `final double precio = 15000;` (Java) vs. `let precio: f64 = ...` (Rust). |
| **Semántica** | Python/PHP infieren en ejecución y permiten reasignar; Java/C#/Go/Rust/C fijan el tipo al compilar; Rust exige `mut` para mutar; C usa tamaños fijos definidos por la implementación. |
| **Representación** | Python guarda una referencia a un objeto `float`; C y Rust guardan los 8 bytes del `double`/`f64` en la propia variable (modelo de valores vs. referencias). |
| **Conversión** | Python y PHP promueven `int`→`float` de forma implícita; Go (`float64(cantidad)`), Rust (`cantidad as f64`) y C (`(double)cantidad`) la exigen escrita. |
| **Formato/locale** | Java, C# y C fuerzan `Locale.US`/`InvariantCulture`/`%.2f` para evitar la coma decimal de locales europeos; el punto como separador es parte del contrato. |
| **Paradigmática** | SQL no tiene "variable que se asigna": describe el resultado con una consulta sobre una tabla de valores, no una secuencia de pasos. |

## 🧬 El concepto en la familia

- **Familia scripting dinámico** (Ruby, Perl, Lua): como Python/PHP, sin declarar tipo. En Ruby `precio = 15000` es una variable, y una constante se marca con inicial mayúscula (`PRECIO`); a diferencia de Python, Ruby *sí* avisa con un warning si reasignas una constante, un punto intermedio entre la convención y la garantía.
- **Familia JVM** (Kotlin): `val precio = 15000.0` es un enlace inmutable y `var` uno mutable —la misma dicotomía `let`/`let mut` de Rust—, con inferencia de tipo desde el literal. Kotlin distingue además `val` (inmutable en tiempo de ejecución) de `const val` (constante de compilación).
- **Familia funcional** (Haskell): `precio = 15000` es una **definición**, no una asignación; el nombre queda ligado a un valor para siempre y no existe la noción de "variable que cambia". Toda la mutación se modela como transformación de valores nuevos.
- **Familia C/llaves** (C++): `const double precio = 15000;` funciona como en C, pero C++ añade `constexpr` para exigir que el valor se calcule en compilación —el equivalente conceptual de la `const` de Rust.

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

- **Formato con coma decimal** (síntoma: `Total: 27000,00`) → causa: el locale del sistema usa coma como separador decimal → solución: forzar cultura invariante (`Locale.US`, `CultureInfo.InvariantCulture`, `%.2f` de C).
- **Porcentaje entero** (síntoma: el descuento se ignora y el total no baja) → causa: escribir `1 - descuento` cuando `descuento` es entero hace aritmética entera y `1 - 0` da `1` → solución: leer el descuento como tipo real (`float`, `f64`, `double`).
- **Truncar la cantidad** (síntoma: totales redondeados de más) → causa: dividir o multiplicar enteros y reales sin convertir en lenguajes que no promueven solos → solución: convertir de forma explícita (`float64(cantidad)`, `cantidad as f64`, `(double)cantidad`).
- **Usar una variable sin inicializar** (C) → causa: declarar `double total;` y leerla antes de asignarle valor deja bits basura → solución: inicializar en la declaración o justo después de `scanf`.
- **Confundir constante de convención con garantía** → causa: creer que `PRECIO_UNITARIO` en Python es inmutable → solución: recordar que la mayúscula es solo un acuerdo; si necesitas inmutabilidad real, usa `Final` (typing) o un lenguaje que la imponga.

## ❓ Preguntas frecuentes

- **¿Por qué Rust obliga a `mut`?** Para que la mutación sea una decisión visible, no un accidente. Klabnik y Nichols explican que la inmutabilidad por defecto ayuda al compilador a razonar sobre el código y evita bugs de aliasing; si quieres mutar, lo declaras y el lector lo ve.
- **¿PHP es débilmente tipado?** Sí: convierte entre tipos automáticamente en muchas operaciones; por eso el `(float)`/`(int)` explícito de la implementación documenta la intención y evita sorpresas al mezclar cadenas y números.
- **¿Un literal tiene tipo?** Sí, aunque no lleve nombre: `15000` es un literal entero, `15000.0` uno real y `"hola"` uno de cadena. El tipo del literal decide cómo se interpreta y con qué otros valores puede operar sin conversión.
- **¿Qué diferencia hay entre valor y variable?** El valor es el dato (el `27000.0` en memoria); la variable es el nombre que lo sostiene. Un mismo valor puede estar enlazado a varios nombres, y un nombre puede reenlazarse a valores distintos a lo largo del tiempo.
- **¿Cuándo se fija el tipo de una variable?** Depende del *binding time* del lenguaje: en Java, C, Go y Rust al compilar; en Python y PHP al ejecutar, cuando el nombre recibe su primer objeto.

## 🔗 Referencias

**Libros de la parte:**

- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson), cap. de nombres, enlaces y ámbito (binding, l-value/r-value, tiempo de vida).
- B. C. Pierce — *Types and Programming Languages* (MIT Press), introducción (los tipos como disciplina que descarta programas mal formados).
- M. L. Scott — *Programming Language Pragmatics* (4ª ed., Morgan Kaufmann), cap. de binding time y modelo de valores vs. referencias.

**Libros de los lenguajes del núcleo:**

- L. Ramalho — *Fluent Python* (2ª ed., O'Reilly), cap. sobre el modelo de objetos y los nombres como etiquetas.
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
