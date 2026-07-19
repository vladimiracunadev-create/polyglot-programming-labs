# Clase 053 — Nulabilidad: null, nil, None, Option y valores ausentes

> Parte **3 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

La ausencia de valor parece trivial hasta que rompe un programa en producción. Cuando buscas un usuario que no existe, cuando un campo opcional viene vacío, cuando una operación puede fracasar sin lanzar excepción, necesitas representar "aquí no hay nada". La forma más difundida de hacerlo —la referencia nula: `null`, `nil`, `None`— es también la más traicionera. Tony Hoare, que la introdujo en ALGOL W en 1965, la llamó décadas después su *billion dollar mistake*: una referencia nula parece un valor más del tipo, pero al usarla revienta el programa, y el sistema de tipos no te avisó de nada.

Esta clase modela ese problema con el ejemplo mínimo —un entero donde `0` significa "ausente"— para contrastar las dos grandes respuestas. La imperativa clásica usa un valor especial (null/nil/None) o un centinela y confía en que el programador recuerde comprobarlo. La tipada envuelve la posible ausencia en un tipo suma: `Option<T>` en Rust, `Maybe a` en Haskell. Como explica Pierce en *Types and Programming Languages*, un tipo suma tiene dos constructores (`Some v` / `None`) y el compilador obliga a distinguir el caso presente del ausente antes de tocar el valor: la ausencia deja de ser una bomba de relojería y pasa a ser una rama del código que no puedes ignorar.

El objetivo, entonces, no es memorizar cómo se escribe "nada" en diez lenguajes, sino entender por qué esa diferencia importa: dónde se detecta el error —en compilación o en ejecución—, quién carga con la responsabilidad de comprobar (el tipo o el programador) y qué herramientas modernas —`?.`, `??`, `Optional`, nullable reference types— intentan devolverle a la ausencia la seguridad que el null le quitó.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Distinguir un valor presente de uno ausente.
2. Nombrar cómo cada lenguaje representa la ausencia.
3. Explicar por qué Option/None es más seguro que null.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Ausencia de valor | No todo dato existe siempre |
| 2 | null / nil / None | Nombres del 'nada' por lenguaje |
| 3 | Option / Maybe | Ausencia tipada y segura |
| 4 | El error del billón de dólares | Los NullPointerException |

## 📖 Definiciones y características

- **Nulabilidad** — posibilidad de que un valor esté ausente. Clave: fuente clásica de errores.
- **null / nil / None** — representación de 'sin valor'. Clave: cada lenguaje lo llama distinto.
- **Option / Maybe** — tipo que envuelve 'hay valor' o 'no hay' (Rust, Haskell). Clave: obliga a manejar la ausencia.
- **Valor centinela** — un valor normal usado para significar 'ausente' (aquí, 0). Clave: sencillo pero frágil.

Conviene separar tres ideas que el lenguaje coloquial mezcla. La **nulabilidad** es una propiedad del diseño: ¿este dato puede faltar? La **representación de la ausencia** es el mecanismo concreto para decir "falta" (`null`, `nil`, `None`, `NULL`). Y el **modelo de tipos** decide si esa ausencia vive dentro del tipo del valor (un `String` que puede ser null) o al lado de él (un `Option<String>`, que es un tipo distinto de `String`). Casi toda la seguridad —o su falta— sale de esta última decisión.

En la familia imperativa clásica null es un habitante universal: cualquier referencia puede valer null y el tipo no lo refleja. Java, C#, JavaScript y PHP comparten esa herencia, y Go la matiza con su `nil`, su convención de "valor cero" y el patrón `(valor, error)` que empuja —sin obligar— a mirar el error antes que el valor. El compilador te deja escribir `usuario.nombre` aunque `usuario` sea null; solo en ejecución aparece el `NullPointerException`. La familia tipada da el paso que faltaba y hace la ausencia visible en el tipo: `Option<T>` (Rust) y `Maybe a` (Haskell) son tipos suma con dos casos, y no puedes leer el valor sin abrir la caja con un `match`. Kotlin y TypeScript ofrecen una vía intermedia marcando la nulabilidad en el propio tipo (`String?`, `string | null`) con comprobaciones que convierten el desliz en error de compilación.

Aparte queda el `NULL` de SQL, que **no es** el null de los imperativos. Como insiste C. J. Date, SQL usa lógica trivaluada: una comparación con NULL no da verdadero ni falso sino *unknown*, `NULL = NULL` es unknown, y por eso se prueba con `IS NULL`. Es un marcador de "dato desconocido o inaplicable", no una referencia rota; confundir ambos conceptos es fuente constante de errores al saltar entre la base de datos y el código de aplicación.

## 🧩 Situación

Imagina un `buscarUsuario(id)` que consulta la base de datos. Si el id no existe, ¿qué devuelve? Si devuelve null, el error no aparece aquí: aparece tres capas más arriba, cuando alguien escribe `usuario.getNombre()` sin sospechar que puede faltar. El null viaja silencioso a través de las fronteras del código y estalla lejos de su origen, donde ya no hay contexto para diagnosticarlo. Ese desfase entre *dónde se produce* la ausencia y *dónde explota* es lo que la hace tan cara.

Modelar la ausencia con un tipo explícito cambia el momento del error: `buscarUsuario` devuelve `Option<Usuario>` y quien lo llama no puede acceder al nombre sin antes decidir qué hacer con el caso vacío. El fallo deja de ser un error en ejecución y se convierte en una pregunta que el compilador te obliga a responder en el sitio. Nuestro ejercicio comprime esa historia a su núcleo: un entero donde `0` es "ausente", para que el mecanismo —comparar, ramificar, imprimir "ausente" o el valor— quede a la vista sin el ruido de una base de datos real.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n` (0 significa ausente)
- **Salida** (stdout): `valor=<n>` si hay valor, o `valor=ausente` si n es 0
- **Regla:** si n == 0 → 'ausente'; si no → n

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `valor=5` |
| `0` | `valor=ausente` |
| `42` | `valor=42` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER n
SI n == 0: ESCRIBIR "valor=ausente"
SINO: ESCRIBIR "valor=" n
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

n = int(sys.stdin.readline())
print("valor=ausente" if n == 0 else f"valor={n}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(n === 0 ? "valor=ausente" : `valor=${n}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(n === 0 ? "valor=ausente" : `valor=${n}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        System.out.println(n == 0 ? "valor=ausente" : "valor=" + n);
    }
}
```

### C# · `dotnet run`

```csharp
using System;

int n = int.Parse(Console.In.ReadToEnd().Trim());
Console.WriteLine(n == 0 ? "valor=ausente" : $"valor={n}");
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
	n, _ := strconv.Atoi(strings.TrimSpace(line))
	if n == 0 {
		fmt.Println("valor=ausente")
	} else {
		fmt.Printf("valor=%d\n", n)
	}
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let valor: Option<i64> = if n == 0 { None } else { Some(n) };
    match valor {
        None => println!("valor=ausente"),
        Some(v) => println!("valor={v}"),
    }
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    if (n == 0) {
        printf("valor=ausente\n");
    } else {
        printf("valor=%ld\n", n);
    }
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL tiene NULL nativo; aquí 0 modela la ausencia con CASE WHEN.
WITH nums(n) AS (VALUES (5), (0), (42))
SELECT CASE WHEN n = 0 THEN 'valor=ausente' ELSE printf('valor=%d', n) END AS resultado
FROM nums;
```

### PHP · `php main.php`

```php
<?php
$n = (int) trim(fgets(STDIN));
echo $n === 0 ? "valor=ausente\n" : "valor=$n\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔎 Recorrido guiado por el código

Las diez implementaciones resuelven el mismo contrato —leer `n`, decidir presente/ausente— pero cada una revela cómo su lenguaje piensa la ausencia. Sigamos el dato desde stdin hasta stdout en tres de ellas.

En **Python** el cuerpo es una sola expresión. `n = int(sys.stdin.readline())` convierte la línea leída en entero, y el ternario `"valor=ausente" if n == 0 else f"valor={n}"` elige la cadena. Con el caso `0` de `casos.json`, `n == 0` es verdadero y se imprime exactamente `valor=ausente`; con el caso `5`, la f-string interpola el número y produce `valor=5`. Aquí la ausencia no está tipada: Python tiene su propio `None`, pero el ejercicio usa el centinela `0`, y nada impide que un `0` legítimo se confunda con "ausente" —justo la fragilidad que la clase quiere que veas.

**Rust** hace lo contrario: modela la ausencia de forma explícita aunque el enunciado no lo exija. Tras parsear `n`, construye `let valor: Option<i64> = if n == 0 { None } else { Some(n) };`. Ahora `valor` no es un número, es una caja que puede estar vacía. Para imprimir hay que abrirla con `match valor { None => ..., Some(v) => ... }`, y el compilador rechazaría el programa si olvidaras una de las dos ramas. Con la entrada `0` se toma la rama `None` y sale `valor=ausente`; con `42`, la rama `Some(v)` liga `v = 42` y sale `valor=42`. Es el mismo resultado que Python, pero la seguridad la garantiza el tipo, no la disciplina del programador —la idea de tipo suma de Pierce llevada a la práctica.

**SQL** habla otro idioma. No lee stdin: su `WITH nums(n) AS (VALUES (5), (0), (42))` fabrica una tabla con los tres casos y el `CASE WHEN n = 0 THEN 'valor=ausente' ELSE printf('valor=%d', n) END` los resuelve todos de una vez, fila por fila. Nótese que aquí `0` se compara con `=` normal porque es un valor real; si en vez de 0 usáramos el `NULL` nativo de SQL, `n = NULL` daría *unknown* y nunca entraría en esa rama —habría que escribir `n IS NULL`. Por eso el verificador marca esta implementación como *ilustrativa*: produce las mismas líneas (`valor=ausente`, `valor=42`) pero sobre un modelo declarativo, no leyendo del flujo de entrada.

## 🔬 Comparación

La diferencia de fondo no está en cómo se escribe la decisión, sino en *quién responde por la ausencia*: el programador que recuerda comprobar, o el sistema de tipos que no te deja olvidar. Esa línea separa el null clásico del `Option` tipado y atraviesa las tres capas de la tabla.

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Todos deciden con un ternario o un `if`; Rust añade encima un `match` de dos ramas obligatorias sobre el `Option`. |
| Semántica | Rust envuelve la ausencia en `Option<T>` (comprobación en compilación); Java, C#, JS, PHP y Go la dejan como null/nil comprobable en ejecución; C usa el centinela numérico crudo. |
| Paradigmática | SQL trata la ausencia con `NULL` nativo y lógica trivaluada (`IS NULL`), distinta del null imperativo; su `CASE WHEN` opera sobre filas, no sobre un flujo. |
| Momento del fallo | Con Option/nullable-types, olvidar el caso vacío es error de compilación; con null clásico es un `NullPointerException`/*nil dereference* en ejecución, lejos del origen. |

## 🧬 El concepto en la familia

En Rust idiomático la ausencia vive en `Option<i64>` y se abre con `match`, `if let` o combinadores como `map` y `unwrap_or`. En Haskell el equivalente es `Maybe Int` (`Just x` / `Nothing`), y toda una maquinaria de funtores permite encadenar cálculos que podrían fallar sin escribir un solo `if`. Kotlin, primo de la JVM, marca la nulabilidad en el tipo (`Int?` frente a `Int`) y ofrece los operadores de navegación segura `?.` y de coalescencia `?:` (Elvis). Swift usa `Optional<T>` con azúcar `T?` y `if let`. En el lado imperativo, Java añadió `Optional<T>` como valor de retorno —Bloch recomienda usarlo para eso, nunca para campos ni parámetros—, C# introdujo los *nullable reference types* (`string?`) que reviven en compilación el problema que el CLR toleraba, y TypeScript hace lo propio con `strictNullChecks` y las uniones `T | null`. Todos convergen en la misma moraleja: la ausencia se maneja mejor cuando es visible en el tipo.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 053
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Usar un valor ausente como si existiera** → causa: desreferenciar null → efecto: `NullPointerException` (Java), `TypeError: null is not an object` (JS), *nil pointer dereference* (Go) → solución: comprobar la ausencia antes de usar el valor, o modelarla con `Option`.
- **Elegir un centinela que es un dato válido** → causa: usar `0`, `-1` o `""` para decir "ausente" cuando pueden ser datos legítimos → solución: preferir un tipo Option explícito cuando el lenguaje lo ofrece.
- **Confundir el `NULL` de SQL con el null imperativo** → causa: esperar que `columna = NULL` filtre las filas vacías → efecto: no devuelve ninguna fila, porque la comparación da *unknown* → solución: usar `IS NULL` / `IS NOT NULL`.
- **Confundir `null` y `undefined` en JavaScript** → causa: son dos ausencias distintas (`null` asignado a propósito, `undefined` "nunca definido") → solución: comparar con `===` y usar `??`, que solo cae en el valor por defecto ante `null`/`undefined`, no ante `0` o `""`.
- **Silenciar la ausencia con `unwrap()` en Rust** → causa: abrir un `Option`/`Result` sin manejar `None` → efecto: `panic` en ejecución, tirando la seguridad del tipo → solución: `match`, `if let` o `unwrap_or` con un valor por defecto.

## ❓ Preguntas frecuentes

- **¿Por qué null es peligroso?** Se cuela sin avisar —cualquier referencia puede valer null y el tipo no lo refleja— y estalla al usarlo, lejos de donde se originó. Los tipos Option obligan a manejarlo en el sitio.
- **¿Qué lenguajes del núcleo tienen Option?** Rust (`Option`). Los demás usan null/nil; Kotlin (primo JVM) y TypeScript marcan la nulabilidad en el tipo, y Java ofrece `Optional<T>` como valor de retorno.
- **¿`None` de Python es como `Option`?** No. `None` es un valor centinela más (un singleton del tipo `NoneType`); nada obliga a comprobarlo. `Option` es un tipo distinto que el compilador exige abrir. Por eso en Python se prueba con `is None`, no con `== None`.
- **¿Y el "billion dollar mistake"?** Es como Tony Hoare llamó a haber introducido la referencia nula en ALGOL W en 1965: parecía cómoda, pero ha costado incontables fallos y horas de depuración. La alternativa —hacer la ausencia parte del tipo— ya existía, y es lo que rescatan Option/Maybe.
- **¿Un centinela como 0 es siempre malo?** No siempre, pero es frágil: funciona solo si el valor elegido nunca puede ser un dato legítimo. En cuanto `0` sea una edad, un saldo o un id válido, el centinela miente; entonces conviene el tipo explícito.

## 🔗 Referencias

**Libros de la parte:**

- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson), cap. tipos y variables (referencias y punteros; problema del dangling/null).
- B. C. Pierce — *Types and Programming Languages* (MIT Press), tipos suma / variantes (Option como forma segura de modelar la ausencia).
- M. L. Scott — *Programming Language Pragmatics* (4ª ed., Morgan Kaufmann), modelo de referencias y valores.

**Libros de los lenguajes del núcleo:**

- L. Ramalho — *Fluent Python* (2ª ed., O'Reilly) (`None`, `is` vs `==`).
- M. Haverbeke — *Eloquent JavaScript* (3ª ed.) — [gratis online](https://eloquentjavascript.net/) (`null` vs `undefined`, `??`).
- B. Cherny — *Programming TypeScript* (O'Reilly) (`strictNullChecks`, uniones con `null`).
- J. Bloch — *Effective Java* (3ª ed., Addison-Wesley) (evita null; usa `Optional` con criterio).
- J. Skeet — *C# in Depth* (4ª ed., Manning) (nullable reference types, `?`).
- A. Donovan y B. Kernighan — *The Go Programming Language* (Addison-Wesley) (`nil`, valores cero, `(valor, error)`).
- S. Klabnik y C. Nichols — *The Rust Programming Language* — [gratis online](https://doc.rust-lang.org/book/) (`Option<T>`, `match`).
- B. Kernighan y D. Ritchie — *The C Programming Language* (2ª ed., Prentice Hall) (punteros nulos).
- C. J. Date — *SQL and Relational Theory* (3ª ed., O'Reilly) (`NULL` y lógica trivaluada).
- J. Lockhart — *Modern PHP* (O'Reilly) (`null`, `??`).

---

> [⏮️ Clase 052](../../parte-3-valores-tipos-y-variables/052-inferencia-de-tipos/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 054 ⏭️](../../parte-3-valores-tipos-y-variables/054-mutabilidad-e-inmutabilidad/README.md)
