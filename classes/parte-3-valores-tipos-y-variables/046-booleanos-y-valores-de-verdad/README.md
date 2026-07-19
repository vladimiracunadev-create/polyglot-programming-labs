# Clase 046 — Booleanos y valores de verdad

> Parte **3 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

En 1854 George Boole demostró que la lógica podía tratarse como un álgebra: un cálculo con solo dos valores, verdadero y falso, y tres operaciones —conjunción, disyunción y negación— capaces de expresar cualquier razonamiento. Casi un siglo después, Claude Shannon vio que esos mismos dos valores describían los circuitos de conmutación, y con ello el booleano se convirtió en la piedra angular de toda la computación. El objetivo de esta clase es que domines ese núcleo mínimo —**AND** (ambos), **OR** (alguno) y **NOT** (negación)— no como tres funciones sueltas, sino como el lenguaje en el que se escribe *toda* decisión que tomará un programa.

Cada `if`, cada `while`, cada filtro de una consulta se reduce en el fondo a evaluar una expresión booleana. Por eso conviene verlos aislados, con su tabla de verdad completa, antes de que en la Parte 4 aparezcan enredados dentro de condiciones complejas. Aquí construimos un booleano a partir de una entrada numérica (0 o 1), aplicamos las tres operaciones y observamos algo revelador: los lenguajes **no se ponen de acuerdo en cómo escribir "verdadero"**. Python y C# imprimen `True` con mayúscula; JavaScript, Java o Go imprimen `true`; C ni siquiera tuvo un tipo booleano nativo hasta 1999. Esa disparidad obliga a **normalizar la salida**, y esa normalización es, en sí misma, una lección sobre cómo cada lenguaje modela la verdad.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Calcular AND, OR y NOT sobre valores booleanos.
2. Construir un booleano a partir de una entrada (0/1).
3. Normalizar la impresión de booleanos entre lenguajes.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | AND, OR, NOT | Las tres operaciones lógicas fundamentales |
| 2 | Representar la verdad | 0/1, true/false, según el lenguaje |
| 3 | Impresión de booleanos | true vs. True: hay que normalizar |
| 4 | Base de las condiciones | Todo if depende de un booleano |

## 📖 Definiciones y características

Un **booleano** es un tipo con exactamente dos habitantes: verdadero y falso. Desde la perspectiva de la teoría de tipos que expone Pierce, es el tipo suma más pequeño no trivial, y su valor típico nace de una comparación (`a > b`, `x == 0`) o de otra expresión booleana. Las tres operaciones fundamentales forman, junto a esos dos valores, un álgebra de Boole completa: **AND** (∧, conjunción) es verdadero solo cuando ambos operandos lo son; **OR** (∨, disyunción) es verdadero cuando al menos uno lo es; y **NOT** (¬, negación) invierte el valor. Con solo estas tres se puede construir cualquier función lógica imaginable —de hecho, con NAND o NOR una sola basta—, y de ahí su papel de cimiento.

Hay dos sutilezas que distinguen la teoría de la práctica en los lenguajes reales. La primera es la **evaluación en cortocircuito**: en `a && b`, si `a` ya es falso, el resultado es falso sin necesidad de mirar `b`, así que la mayoría de lenguajes ni siquiera lo evalúan; lo mismo con `a || b` cuando `a` es verdadero. Esto importa cuando `b` tiene efectos secundarios o podría fallar (por ejemplo, `p != null && p.valor > 0`). La segunda es la **veracidad** (*truthiness*): muchos lenguajes dinámicos permiten usar valores no booleanos donde se espera una condición —el `0`, la cadena vacía o `null` se consideran "falsos"—, una comodidad que Haverbeke advierte que puede sorprender en JavaScript. En esta clase evitamos esa ambigüedad convirtiendo explícitamente la entrada con `a != 0`, para obtener un booleano genuino antes de operar.

Los términos en breve:

- **Booleano** — tipo de dos valores (verdadero/falso); resultado natural de comparaciones y condiciones.
- **AND (∧)** — conjunción: verdadero solo si ambos operandos lo son.
- **OR (∨)** — disyunción: verdadero si al menos uno lo es.
- **NOT (¬)** — negación: invierte el valor de verdad.
- **Cortocircuito** — `&&` y `||` no evalúan el segundo operando si el primero ya decide el resultado.
- **Veracidad (truthiness)** — regla por la que valores no booleanos se interpretan como verdaderos o falsos.

## 🧩 Situación

"Si es fin de semana **Y** no llueve, salgo al parque." Esa frase cotidiana es ya una expresión booleana: dos condiciones (`es_finde`, `no_llueve`) unidas por un AND. Cambia el conector y cambia la política: "si es feriado **O** es fin de semana" abre más días; "si **NO** hay reunión" niega una condición. Toda regla de negocio, todo permiso de acceso, todo filtro se descompone en esta gramática de tres operadores, y por eso practicarla aislada —con la tabla de verdad delante— es la mejor inversión antes de encadenar condiciones reales.

El laboratorio recibe dos bits `a b` y produce `and`, `or` y `not_a`. Fíjate en el caso `1 0` de `casos.json`, cuyo esperado es `and=false or=true not_a=false`: con `a`=verdadero y `b`=falso, la conjunción es falsa (no ambos), la disyunción verdadera (al menos uno), y la negación de `a` es falsa. El caso `0 0` da `and=false or=false not_a=true`, el único donde `not_a` se vuelve verdadero. Reproducir estas tres filas exactas en diez lenguajes obliga a resolver el problema real: cada uno imprime la verdad con una grafía distinta, y hay que unificarla.

## 🧮 Modelo

- **Entrada** (stdin): una línea `a b` (cada uno 0 o 1)
- **Salida** (stdout): `and=<true|false> or=<true|false> not_a=<true|false>`
- **Regla:** and = a ∧ b ; or = a ∨ b ; not_a = ¬a (con a,b interpretados como booleanos)

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `1 0` | `and=false or=true not_a=false` |
| `1 1` | `and=true or=true not_a=false` |
| `0 0` | `and=false or=false not_a=true` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER a, b
ba <- (a != 0) ; bb <- (b != 0)
ESCRIBIR "and=" (ba Y bb) " or=" (ba O bb) " not_a=" (NO ba)
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

a, b = map(int, sys.stdin.readline().split())
ba, bb = a != 0, b != 0
tf = lambda x: "true" if x else "false"
print(f"and={tf(ba and bb)} or={tf(ba or bb)} not_a={tf(not ba)}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const [ai, bi] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const a = ai !== 0;
const b = bi !== 0;
const tf = (x) => (x ? "true" : "false");
console.log(`and=${tf(a && b)} or=${tf(a || b)} not_a=${tf(!a)}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const [ai, bi]: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const a: boolean = ai !== 0;
const b: boolean = bi !== 0;
const tf = (x: boolean): string => (x ? "true" : "false");
console.log(`and=${tf(a && b)} or=${tf(a || b)} not_a=${tf(!a)}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    static String tf(boolean x) {
        return x ? "true" : "false";
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        boolean a = Integer.parseInt(p[0]) != 0;
        boolean b = Integer.parseInt(p[1]) != 0;
        System.out.printf("and=%s or=%s not_a=%s%n", tf(a && b), tf(a || b), tf(!a));
    }
}
```

### C# · `dotnet run`

```csharp
using System;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
bool a = int.Parse(p[0]) != 0;
bool b = int.Parse(p[1]) != 0;
string Tf(bool x) => x ? "true" : "false";
Console.WriteLine($"and={Tf(a && b)} or={Tf(a || b)} not_a={Tf(!a)}");
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

func tf(x bool) string {
	if x {
		return "true"
	}
	return "false"
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	f := strings.Fields(line)
	ai, _ := strconv.Atoi(f[0])
	bi, _ := strconv.Atoi(f[1])
	a, b := ai != 0, bi != 0
	fmt.Printf("and=%s or=%s not_a=%s\n", tf(a && b), tf(a || b), tf(!a))
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn tf(x: bool) -> &'static str {
    if x { "true" } else { "false" }
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let v: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    let (a, b) = (v[0] != 0, v[1] != 0);
    println!("and={} or={} not_a={}", tf(a && b), tf(a || b), tf(!a));
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

static const char *tf(int x) {
    return x ? "true" : "false";
}

int main(void) {
    int a, b;
    if (scanf("%d %d", &a, &b) != 2) return 1;
    a = a != 0;
    b = b != 0;
    printf("and=%s or=%s not_a=%s\n", tf(a && b), tf(a || b), tf(!a));
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL no tiene tipo booleano nativo: se expresa con CASE WHEN.
WITH pares(a, b) AS (VALUES (1, 0), (1, 1), (0, 0))
SELECT printf('and=%s or=%s not_a=%s',
       CASE WHEN a <> 0 AND b <> 0 THEN 'true' ELSE 'false' END,
       CASE WHEN a <> 0 OR b <> 0 THEN 'true' ELSE 'false' END,
       CASE WHEN NOT (a <> 0) THEN 'true' ELSE 'false' END) AS resultado
FROM pares;
```

### PHP · `php main.php`

```php
<?php
[$a, $b] = preg_split('/\s+/', trim(fgets(STDIN)));
$a = ((int) $a) !== 0;
$b = ((int) $b) !== 0;
$tf = fn($x) => $x ? "true" : "false";
printf("and=%s or=%s not_a=%s\n", $tf($a && $b), $tf($a || $b), $tf(!$a));
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔎 Recorrido guiado por el código

Sigamos el caso testigo `1 0`, cuya salida esperada en `casos.json` es `and=false or=true not_a=false`, para ver cómo cada lenguaje llega exactamente ahí.

En **Python**, tras leer los dos enteros, la línea `ba, bb = a != 0, b != 0` es el paso conceptual clave: **convierte números en booleanos genuinos**. Con `a`=1 y `b`=0 obtenemos `ba=True`, `bb=False`. Podríamos habernos saltado esta conversión —Python trata cualquier entero no nulo como verdadero por *truthiness*—, pero hacerla explícita evita ambigüedades y deja claro que operamos sobre verdad, no sobre cantidad. Luego `ba and bb` da `False`, `ba or bb` da `True`, y `not ba` da `False`. El detalle de presentación vive en `` tf = lambda x: "true" if x else "false" ``: sin este ayudante, Python imprimiría `False` con mayúscula y rompería el contrato. La f-string final produce el texto exacto `and=false or=true not_a=false`.

**JavaScript** sigue la misma coreografía con otra sintaxis: `const a = ai !== 0` construye el booleano, y luego `a && b`, `a || b`, `!a` aplican las tres operaciones. Aquí `&&` y `||` son los operadores *lógicos con cortocircuito* —muy distintos de `&` y `|`, que operarían bit a bit sobre los números—. El mismo ayudante `` tf = (x) => (x ? "true" : "false") `` normaliza la salida, aunque en JavaScript sea menos necesario porque su `true`/`false` ya van en minúscula por defecto.

El contraste iluminador es **C#**, porque expone por qué la normalización no es opcional. Si escribiéramos `Console.WriteLine(a && b)` directamente, C# imprimiría `False` con F mayúscula (el resultado de `bool.ToString()`), y el verificador lo rechazaría frente al esperado `false`. Por eso existe `string Tf(bool x) => x ? "true" : "false"`: fuerza la grafía en minúscula que el contrato exige. Python comparte exactamente este problema (`True`/`False`), mientras que Java, Go, Rust, PHP y JavaScript ya usan minúsculas y solo emplean `tf` por consistencia.

El caso más didáctico es **C**, que enseña el origen histórico de todo esto. C no tuvo tipo booleano hasta C99; aquí `int a, b;` guarda enteros, y `a = a != 0;` **reduce cualquier valor a 0 o 1** aprovechando que en C el resultado de una comparación es un `int`. Sus operadores `&&`, `||`, `!` devuelven también `int` (0 o 1), no un `bool`. El ayudante `` static const char *tf(int x) `` recibe ese entero y devuelve la cadena adecuada. Es la implementación más "descarnada": muestra que, por debajo, un booleano siempre fue un número disfrazado.

Por su parte **SQL** no tiene tipo booleano nativo en SQLite, así que traduce cada operación a un `CASE WHEN … THEN 'true' ELSE 'false' END` sobre la tabla de casos declarada con `VALUES (1,0), (1,1), (0,0)`. Es la misma tabla de verdad, expresada de forma declarativa fila por fila; el verificador la marca como ilustrativa porque no lee de stdin.

## 🔬 Comparación

La lógica es universal —las tres tablas de verdad son idénticas en todo lenguaje—, pero cada uno decide tres cosas por su cuenta: **cómo se escriben los operadores**, **cómo se imprime la verdad** y **si existe siquiera un tipo booleano de primera clase**. Ahí es donde surgen las divergencias que la tabla resume.

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Palabras vs. símbolos: `and`/`or`/`not` (Python) frente a `&&`/`\|\|`/`!` (C, Java, JS, Go, Rust, PHP). El significado es el mismo; solo cambia la grafía del operador. |
| Semántica | Grafía de la verdad: C# y Python imprimen `True`/`False` con mayúscula por defecto; JS, Java, Go, Rust y PHP usan minúscula. C carece de tipo `bool` hasta C99 y opera con `int` (0/1). Todos deben normalizarse a `true`/`false` con el ayudante `tf`. |
| Paradigmática | SQL (SQLite) no tiene booleano nativo: expresa cada operación con `CASE WHEN a<>0 AND b<>0 THEN 'true' ELSE 'false' END` sobre una tabla declarada con `VALUES`. |

Merece una fila propia una distinción que causa errores reales: **operadores lógicos vs. de bits**. `&&`/`||` son lógicos y cortocircuitan; `&`/`|` son *bitwise* y evalúan siempre ambos lados operando bit a bit. Sobre valores 0/1 pueden dar el mismo resultado numérico y ocultar el error, pero su semántica difiere: con `&` no hay cortocircuito, así que un `p != null & p.valor > 0` sí intentaría leer `p.valor` aunque `p` sea nulo. La familia entera comparte esta trampa.

## 🧬 El concepto en la familia

En Ruby, `a && b`, con `true`/`false` en minúscula por defecto (y solo `nil` y `false` cuentan como falsos). En Haskell son `&&`, `||`, `not`, con el tipo `Bool` explícito y valores `True`/`False`, sin ninguna veracidad implícita: una condición *debe* ser un `Bool`. Swift también exige un `Bool` estricto en sus `if`. El patrón general: cuanto más estático y tipado es el lenguaje, menos tolera usar un número donde se espera una verdad, y más pura resulta el álgebra de Boole que subyace a todo.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 046
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Imprimir `True`/`False`** → causa: dejar que C# o Python usen su formato por defecto → solución: normalizar a minúsculas con un ayudante `tf` que mapee el booleano a la cadena `"true"`/`"false"`.
- **Confundir cortocircuito con bit a bit** → causa: usar `&`/`|` en vez de `&&`/`||` → solución: usar los operadores lógicos; los de bits no cortocircuitan y evalúan efectos secundarios que no querías.
- **Depender de la veracidad implícita** → causa: escribir `if (x)` con `x` numérico o cadena y asumir que "no vacío = verdadero" en todo lenguaje → solución: convertir explícitamente (`x != 0`) para no llevarte sorpresas al portar el código.
- **Negar mal una condición compuesta** → causa: escribir `!(a && b)` como `!a && !b` → solución: aplicar De Morgan correctamente: `!(a && b)` equivale a `!a || !b`.

## ❓ Preguntas frecuentes

- **¿`&&` y `&` son lo mismo?** No: `&&` es lógico con cortocircuito y trabaja sobre valores de verdad; `&` es bit a bit y evalúa siempre ambos operandos. Para booleanos, usa `&&`.
- **¿Qué es el cortocircuito?** En `a && b`, si `a` es falso no se evalúa `b` (el resultado ya está decidido); en `a || b`, si `a` es verdadero tampoco. Importa cuando `b` tiene efectos secundarios o puede fallar.
- **¿Por qué unos lenguajes escriben `True` y otros `true`?** Es una decisión de diseño de su método de conversión a texto: Python y C# capitalizan; la mayoría del resto no. No hay una razón lógica, solo convención, y por eso hay que normalizar.
- **¿Qué son las leyes de De Morgan?** Dos equivalencias que todo programador usa: `!(a && b) == !a || !b` y `!(a || b) == !a && !b`. Permiten simplificar condiciones negadas sin cambiar su significado.

## 🔗 Referencias

**Libros de la parte:**

- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson), cap. tipos de datos (tipo booleano) y expresiones (operadores relacionales y booleanos, cortocircuito).
- B. C. Pierce — *Types and Programming Languages* (MIT Press), el tipo `Bool` y el condicional en el cálculo lambda tipado.
- M. L. Scott — *Programming Language Pragmatics* (4ª ed., Morgan Kaufmann), evaluación en cortocircuito de operadores booleanos.

**Libros de los lenguajes del núcleo:**

- L. Ramalho — *Fluent Python* (2ª ed., O'Reilly), objetos verdaderos y falsos (`bool` y `__bool__`).
- M. Haverbeke — *Eloquent JavaScript* (3ª ed.) — valores truthy/falsy y operadores lógicos — [gratis online](https://eloquentjavascript.net/).
- B. Cherny — *Programming TypeScript* (O'Reilly), tipo `boolean` y estrechamiento por condiciones.
- J. Bloch — *Effective Java* (3ª ed., Addison-Wesley), preferir tipos primitivos como `boolean`.
- J. Skeet — *C# in Depth* (4ª ed., Manning), `bool` y booleanos anulables.
- A. Donovan y B. Kernighan — *The Go Programming Language* (Addison-Wesley), tipo `bool` y operadores lógicos.
- S. Klabnik y C. Nichols — *The Rust Programming Language* — tipo `bool` — [gratis online](https://doc.rust-lang.org/book/).
- B. Kernighan y D. Ritchie — *The C Programming Language* (2ª ed., Prentice Hall), expresiones relacionales y lógicas (sin tipo bool nativo).
- C. J. Date — *SQL and Relational Theory* (3ª ed., O'Reilly), lógica de tres valores y predicados.
- J. Lockhart — *Modern PHP* (O'Reilly), tipos escalares y conversión a booleano.

---

> [⏮️ Clase 045](../../parte-3-valores-tipos-y-variables/045-numeros-reales-punto-flotante-precision-y-decimales/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 047 ⏭️](../../parte-3-valores-tipos-y-variables/047-caracteres-texto-y-unicode/README.md)
