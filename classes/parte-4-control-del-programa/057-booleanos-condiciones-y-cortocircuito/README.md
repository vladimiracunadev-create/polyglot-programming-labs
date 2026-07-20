# Clase 057 — Booleanos, condiciones y cortocircuito

> Parte **4 — Control del programa** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Todo programa que decide algo necesita antes fabricar un valor de verdad: reducir una situación del mundo —un número, un usuario, un saldo— a un simple *sí* o *no* sobre el que ramificar. Los operadores de comparación (`>`, `==`, `<`) son la máquina que produce esos booleanos, y los operadores lógicos (`and`/`&&`, `or`/`||`) los combinan para expresar condiciones compuestas. Sin este vocabulario, la programación estructurada no tendría sobre qué apoyar sus decisiones: el `if`, el `while` y el `for` toman todos su rumbo de una expresión booleana.

El objetivo de fondo de esta clase es el **cortocircuito** (*short-circuit evaluation*): en `a && b`, si `a` ya es falso, `b` ni siquiera se evalúa, porque el resultado ya está decidido. Esto no es un detalle de rendimiento sino una herramienta de corrección. Convierte el orden de las condiciones en algo semántico: `usuario != null && usuario.activo` es correcto, y `usuario.activo && usuario != null` revienta. Entender por qué esa asimetría existe —y en qué lenguajes se puede confiar en ella— es lo que separa escribir condiciones que funcionan por casualidad de escribirlas sabiendo que no pueden fallar.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Producir booleanos a partir de comparaciones.
2. Combinar condiciones con AND/OR.
3. Explicar el cortocircuito y por qué importa.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Comparaciones | Producen valores de verdad |
| 2 | Operadores lógicos | AND, OR y su cortocircuito |
| 3 | Cortocircuito | No evalúa lo que no hace falta |
| 4 | Normalizar booleanos | true/false consistente entre lenguajes |

## 📖 Definiciones y características

- **Condición** — expresión que da verdadero o falso. Clave: gobierna las decisiones.
- **Cortocircuito** — en `a && b`, si `a` es falso no se evalúa `b`. Clave: evita trabajo y errores.
- **Operador relacional** — compara valores (>, <, ==). Clave: produce booleanos.
- **Predicado** — condición sobre un valor (es positivo, es par). Clave: bloque de la lógica.

Estas piezas encajan en un mismo edificio conceptual. Un operador relacional produce el átomo —un booleano—; un predicado es ese átomo nombrado y con sentido (`es_par`, `es_mayor_de_edad`); los operadores lógicos componen predicados en condiciones más ricas; y el cortocircuito gobierna *cuándo* cada trozo llega a ejecutarse. Como argumentan Dahl, Dijkstra y Hoare en *Structured Programming*, la potencia de la programación estructurada nace de reducir el flujo de control a un puñado de construcciones bien entendidas, y todas ellas —selección e iteración— se gobiernan con expresiones booleanas: el booleano es el pegamento entre los datos y las decisiones. Sebesta, en el capítulo de control de flujo de *Concepts of Programming Languages*, dedica atención explícita a la evaluación en cortocircuito precisamente porque no es un mero optimizador: cambia qué código corre, y por tanto qué efectos secundarios ocurren. Un detalle histórico ilumina lo abstracto que es todo esto: C no tuvo un tipo booleano hasta C99 (`<stdbool.h>`); antes, la verdad era simplemente un entero donde cero significaba falso y cualquier otra cosa, verdadero. Que un concepto tan central pudiera vivir tanto tiempo sin tipo propio muestra que el booleano es antes una *idea* sobre el control del programa que un dato entre otros.

## 🧩 Situación

Imagina el endpoint de login de un servicio: recibe una sesión y debe decidir si el usuario tiene permiso. El chequeo natural es `if (sesion != null && sesion.usuario.activo && sesion.usuario.tienePermiso("leer"))`. Ese `&&` cortocircuitado no es adorno: es la única razón por la que la línea no lanza una `NullPointerException` cuando la sesión ha expirado y llega nula. La primera condición actúa de guardia de las siguientes, y el lenguaje garantiza que si falla, el resto no se toca. Invertir el orden —poner `sesion.usuario.activo` primero— convierte una comprobación defensiva en un crash en producción a las tres de la madrugada.

El mismo patrón decide corrección en consultas: `if (i < arr.length && arr[i] == objetivo)` recorre un arreglo sin desbordarse, porque la comprobación de rango protege al acceso indexado. Aquí el cortocircuito no ahorra tiempo apreciable; ahorra un fallo. Y hay un giro importante que casi nadie anticipa: en SQL esta intuición se resquebraja, porque el motor puede reordenar los predicados de un `WHERE` a su antojo y porque un `NULL` introduce un tercer valor de verdad, `UNKNOWN`, que no se comporta como `false`. Lo que en Java es una garantía, en SQL es solo una expectativa.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n`
- **Salida** (stdout): `positivo=<true|false> par=<true|false> ambos=<true|false>`
- **Regla:** positivo = n>0 ; par = n%2==0 ; ambos = positivo && par

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `4` | `positivo=true par=true ambos=true` |
| `-3` | `positivo=false par=false ambos=false` |
| `7` | `positivo=true par=false ambos=false` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER n
ESCRIBIR positivo=(n>0), par=(n%2==0), ambos=((n>0) Y (n%2==0))
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys

n = int(sys.stdin.readline())
tf = lambda x: "true" if x else "false"
pos = n > 0
par = n % 2 == 0
print(f"positivo={tf(pos)} par={tf(par)} ambos={tf(pos and par)}")
```

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
const tf = (x) => (x ? "true" : "false");
const pos = n > 0;
const par = n % 2 === 0;
console.log(`positivo=${tf(pos)} par=${tf(par)} ambos=${tf(pos && par)}`);
```

🧬 **El mismo programa en la familia JavaScript / web:** [Dart · ActionScript](primos.md#javascript-web)

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
const tf = (x: boolean): string => (x ? "true" : "false");
const pos: boolean = n > 0;
const par: boolean = n % 2 === 0;
console.log(`positivo=${tf(pos)} par=${tf(par)} ambos=${tf(pos && par)}`);
```

🧬 **El mismo programa en la familia JavaScript / web:** [Dart · ActionScript](primos.md#javascript-web)

### Java · [`java/Main.java`](implementaciones/java/Main.java) · `java Main.java`

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
        int n = Integer.parseInt(br.readLine().trim());
        boolean pos = n > 0;
        boolean par = n % 2 == 0;
        System.out.printf("positivo=%s par=%s ambos=%s%n", tf(pos), tf(par), tf(pos && par));
    }
}
```

🧬 **El mismo programa en la familia JVM:** [Kotlin · Scala · Groovy · Clojure](primos.md#jvm)

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;

int n = int.Parse(Console.In.ReadToEnd().Trim());
string Tf(bool x) => x ? "true" : "false";
bool pos = n > 0;
bool par = n % 2 == 0;
Console.WriteLine($"positivo={Tf(pos)} par={Tf(par)} ambos={Tf(pos && par)}");
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

func tf(x bool) string {
	if x {
		return "true"
	}
	return "false"
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	n, _ := strconv.Atoi(strings.TrimSpace(line))
	pos := n > 0
	par := n%2 == 0
	fmt.Printf("positivo=%s par=%s ambos=%s\n", tf(pos), tf(par), tf(pos && par))
}
```

🧬 **El mismo programa en la familia Sistemas:** [Zig · Nim · D](primos.md#sistemas)

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn tf(x: bool) -> &'static str {
    if x { "true" } else { "false" }
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let pos = n > 0;
    let par = n % 2 == 0;
    println!("positivo={} par={} ambos={}", tf(pos), tf(par), tf(pos && par));
}
```

🧬 **El mismo programa en la familia Sistemas:** [Zig · Nim · D](primos.md#sistemas)

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

static const char *tf(int x) {
    return x ? "true" : "false";
}

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    int pos = n > 0;
    int par = n % 2 == 0;
    printf("positivo=%s par=%s ambos=%s\n", tf(pos), tf(par), tf(pos && par));
    return 0;
}
```

🧬 **El mismo programa en la familia C / llaves:** [C++ · Objective-C](primos.md#c-llaves)

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL: condiciones con AND dentro de CASE WHEN.
WITH nums(n) AS (VALUES (4), (-3), (7))
SELECT printf('positivo=%s par=%s ambos=%s',
       CASE WHEN n > 0 THEN 'true' ELSE 'false' END,
       CASE WHEN n % 2 = 0 THEN 'true' ELSE 'false' END,
       CASE WHEN n > 0 AND n % 2 = 0 THEN 'true' ELSE 'false' END) AS resultado
FROM nums;
```

🧬 **El mismo programa en la familia Lógica y declarativa:** [Prolog · Datalog](primos.md#logica-declarativa)

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
$n = (int) trim(fgets(STDIN));
$tf = fn($x) => $x ? "true" : "false";
$pos = $n > 0;
$par = $n % 2 === 0;
printf("positivo=%s par=%s ambos=%s\n", $tf($pos), $tf($par), $tf($pos && $par));
```

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔎 Recorrido del código: de la entrada a la salida

Sigamos el caso `n = 4` a través de la implementación de **Python**. La primera línea, `int(sys.stdin.readline())`, lee la línea de texto `"4\n"` y la convierte en el entero `4`. Luego `pos = n > 0` evalúa `4 > 0`, que es `True`, y `par = n % 2 == 0` evalúa `4 % 2 == 0`, es decir `0 == 0`, también `True`. La clave está en el `f-string` final: `tf(pos and par)`. Aquí `pos and par` es `True and True`. Como `pos` es verdadero, Python *no* puede decidir todavía el `and`, así que evalúa el segundo operando `par`, que es `True`, y devuelve ese último operando. El ayudante `tf` lo mapea a la cadena `"true"`, y la salida es `positivo=true par=true ambos=true`, exactamente lo que `casos.json` espera. Con `n = -3`, en cambio, `pos` es `False`; el `and` cortocircuita y ni mira `par`, devolviendo directamente `False` → `ambos=false`. Y con `n = 7`, `pos=True` pero `par=False` (`7 % 2` es `1`), así que `ambos=false`.

El contraste más ilustrativo es **SQL**, porque es el único que no ramifica imperativamente. En vez de leer `n` de stdin, define una tabla en línea con `WITH nums(n) AS (VALUES (4), (-3), (7))` y procesa las tres filas de golpe. Donde Python usa un ayudante `tf` y el operador `and`, SQL necesita tres `CASE WHEN ... THEN 'true' ELSE 'false' END` separados, porque un booleano no es directamente un texto imprimible: hay que traducirlo explícitamente. El `ambos` se calcula con `CASE WHEN n > 0 AND n % 2 = 0 THEN ...`, y para `n = -3` produce `'false'` igual que Python, pero por una razón distinta —evalúa la expresión relacional completa como parte de un predicado declarativo, sin garantía documentada del orden de cortocircuito—. Un tercer punto de vista es **C**: como no hay tipo `bool` en el código (`int pos = n > 0;`), la verdad viaja como los enteros `1` y `0`, y `tf(int x)` decide con `x ? "true" : "false"`. Tres modelos del mismo booleano —operando en Python, celda de texto en SQL, entero en C— convergen en la misma tabla de `casos.json`.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `and` (Python) vs. `&&` (C/Java/JS/Go/Rust/PHP). |
| Semántica | Todos cortocircuitan `&&`/`and`; C# imprime True/False (normalizar). |
| Paradigmática | SQL usa AND en la expresión y CASE WHEN para el texto. |

Las diferencias van más hondo que la sintaxis. En Python y JavaScript, `and`/`or` (y `&&`/`||`) devuelven **uno de los operandos**, no un booleano normalizado: `0 or 5` vale `5` y `"a" && "b"` vale `"b"`, un idiom que se explota para valores por defecto. Java, C# y —crucialmente— Go y Rust rechazan esa laxitud: exigen que el operando de una condición sea de tipo booleano estricto, sin *truthiness*, de modo que `if (n)` con `n` entero no compila. C ocupa el extremo opuesto: sin `bool` nativo antes de C99, cualquier entero no nulo es verdadero. TypeScript añade sobre JavaScript un análisis estático que estrecha tipos tras una comprobación (`if (x != null)` hace que el compilador trate `x` como no nulo debajo). Y SQL rompe la lógica binaria por completo: opera con lógica **ternaria**, donde `NULL` produce `UNKNOWN`, así que `NULL = NULL` no es `true` y un `WHERE` puede descartar filas que ingenuamente creerías incluidas.

## 🧬 El concepto en la familia

En la familia orientada a objetos con raíz en Smalltalk, Ruby escribe `n > 0 && n.even?` y trata la verdad como objetos (`true`/`false` son instancias singleton). En la familia funcional pura, Haskell define `(&&)` de forma que `n > 0 && even n` cortocircuita porque la evaluación perezosa del lenguaje no fuerza el segundo argumento salvo que haga falta: aquí el cortocircuito no es un caso especial del operador, sino una consecuencia natural del *lazy evaluation*. Lisp lo expresa con `(and ...)` como forma especial que devuelve el último valor no nulo, herencia directa del idiom que Python y JS heredaron después. En la familia lógica, Prolog invierte la perspectiva: la conjunción `,` no combina booleanos sino *objetivos* a satisfacer, y el backtracking reintenta alternativas en vez de simplemente cortocircuitar. Mismo símbolo lógico, ontologías muy distintas de qué es "verdad".

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 057
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Ordenar mal las condiciones protegidas** → causa: poner el acceso peligroso (`p.activo`) antes de la guarda (`p != null`), de modo que el cortocircuito ya no protege → solución: colocar siempre primero la condición que hace seguro al resto.
- **Confundir `&` con `&&`** → causa: `&` es un operador *bit a bit* que evalúa ambos lados sin cortocircuitar; usarlo en una condición lógica pierde la protección y puede dar resultados numéricos inesperados → solución: usar `&&`/`and` para lógica y reservar `&` para manipulación de bits.
- **Imprimir `True`/`False` en C#** → causa: `bool.ToString()` produce mayúscula inicial por defecto, rompiendo la igualdad exacta con `casos.json` → solución: normalizar con un ayudante `Tf(bool) => x ? "true" : "false"`.
- **Suponer cortocircuito donde no lo hay** → causa: creer que un `WHERE` de SQL o un lenguaje con evaluación estricta respetan el orden izquierda-a-derecha → solución: en SQL, envolver el acceso peligroso en un `CASE` explícito en vez de confiar en el orden de los predicados.
- **Depender de *truthiness* que el lenguaje no ofrece** → causa: escribir `if (n)` con `n` entero portando código de Python/JS a Go o Rust → solución: comparar explícitamente (`if n != 0`), como exigen los lenguajes de tipado estricto.

## ❓ Preguntas frecuentes

- **¿`&` y `&&` son iguales?** No: `&` es bit a bit y evalúa ambos lados siempre; `&&` es lógico y cortocircuita. En una condición casi siempre quieres `&&`.
- **¿El cortocircuito cambia el resultado?** No cambia el valor lógico final, pero sí cambia *qué se ejecuta*: si el segundo operando tiene efectos secundarios (una llamada, una escritura) o puede fallar (un acceso nulo), el cortocircuito decide si eso ocurre.
- **¿Por qué `0 or 5` da `5` en Python y no `True`?** Porque `and`/`or` en Python devuelven uno de los operandos, no un booleano: `or` devuelve el primero verdadero (o el último si todos son falsos). Es el idiom clásico de valor por defecto.
- **¿Puedo fiarme del orden de los predicados en SQL?** No: el optimizador puede reordenarlos, y `NULL` introduce lógica ternaria. Si un predicado protege a otro, hazlo explícito con `CASE` en lugar de confiar en el cortocircuito.

## 🔗 Referencias

Para esta clase, lee en Sebesta el apartado de *short-circuit evaluation* dentro del capítulo de expresiones y control de flujo, y contrástalo con la discusión de operadores relacionales y booleanos; en *Structured Programming* apóyate en el ensayo de Dijkstra sobre cómo la selección se apoya en condiciones bien formadas.

**Libros de la parte:**

- O.-J. Dahl, E. W. Dijkstra y C. A. R. Hoare — *Structured Programming* (Academic Press).
- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson), cap. control de flujo.

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

> [⏮️ Clase 056](../../parte-3-valores-tipos-y-variables/056-entrada-y-salida-basica-leer-y-escribir/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 058 ⏭️](../../parte-4-control-del-programa/058-guardas-y-validacion-temprana/README.md)
