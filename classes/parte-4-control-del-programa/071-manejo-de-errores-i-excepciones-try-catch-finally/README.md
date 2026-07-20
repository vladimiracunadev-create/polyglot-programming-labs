# Clase 071 — Manejo de errores I: excepciones (try/catch/finally)

> Parte **4 — Control del programa** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Una excepción es una transferencia de control **no local**: cuando una operación falla, el flujo no continúa en la siguiente línea sino que salta hasta el manejador más cercano en la pila de llamadas, descartando por el camino todos los marcos intermedios que no sepan tratar el problema. Ese mecanismo —el *stack unwinding*, el desenrollado de la pila— es lo que distingue a las excepciones de cualquier otra construcción de control: un `if` decide entre dos caminos dentro de la misma función, mientras que un `throw` puede atravesar diez funciones de golpe hasta encontrar quien lo capture. Las excepciones existen porque el código que *detecta* un fallo rara vez es el que sabe *qué hacer* con él: una rutina de bajo nivel que abre un archivo sabe que no existe, pero solo la capa de aplicación sabe si eso significa abortar, reintentar o usar un valor por defecto.

En esta clase dividimos dos enteros y tratamos el caso `b = 0` para ver de cerca el aparato completo: el bloque `try` que envuelve la operación arriesgada, el `catch` que captura el tipo concreto de fallo, y el `finally` que se ejecuta pase lo que pase. El caso es deliberadamente pequeño pero revela una fractura profunda entre lenguajes: Java, C#, Python y PHP lanzan una excepción ante la división entera por cero; JavaScript no lanza nada y devuelve `Infinity`; Go, Rust y C carecen directamente de excepciones y obligan a comprobar antes. Veremos además el coste real de este mecanismo —construir una traza de pila no es gratis—, por qué usar excepciones como control de flujo ordinario es un antipatrón salvo en Python, y cómo cada lenguaje ha inventado su propia forma (`try-with-resources`, `using`, `with`) de garantizar la limpieza sin escribir `finally` a mano.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Capturar una excepción con try/catch.
2. Distinguir el flujo normal del de error.
3. Reconocer qué lenguajes lanzan y cuáles no.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Excepción | Un error que interrumpe el flujo |
| 2 | try/catch | Intentar y capturar el fallo |
| 3 | finally | Código que corre pase lo que pase |
| 4 | Lanzar vs. comprobar | No todos lanzan en /0 |

## 📖 Definiciones y características

- **Excepción** — objeto que representa un error y desvía el flujo. Clave: se captura con try/catch.
- **try** — bloque que puede fallar. Clave: envuelve la operación arriesgada.
- **catch** — bloque que maneja la excepción. Clave: el plan B ante el error.
- **finally** — bloque que se ejecuta siempre (haya error o no). Clave: liberar recursos.

Sebesta dedica en *Concepts of Programming Languages* un capítulo entero al manejo de excepciones, y su punto de partida es que se trata de una construcción de control tan legítima como el bucle o la selección, solo que con un alcance distinto: mientras `if` y `while` transfieren el control dentro de una función, la excepción lo transfiere *entre* funciones, hacia arriba en la pila. De ahí nacen las dos propiedades que la definen. La primera es la propagación: si el marco actual no tiene un manejador adecuado, la excepción sube al marco que lo llamó, y así sucesivamente hasta la raíz; si nadie la captura, el programa termina. La segunda es la selección por tipo: los manejadores se organizan en una jerarquía de clases (`ArithmeticException` bajo `RuntimeException` bajo `Exception` bajo `Throwable` en Java), y el criterio es capturar siempre **lo específico antes que lo general**, porque un `catch (Exception e)` colocado primero engulliría también los fallos que un manejador posterior sabía tratar mejor. El precio de esta potencia es la legibilidad: el código deja de leerse linealmente, porque cualquier línea del `try` puede ser el último punto de ejecución.

Bloch advierte en *Effective Java* con especial insistencia sobre dos abusos. El primero es usar excepciones para el control de flujo ordinario —terminar un bucle lanzando y capturando— porque oscurece la intención, impide optimizaciones de la JVM y esconde bugs reales bajo el mismo mecanismo; su regla es que las excepciones son para condiciones excepcionales. El segundo es el `catch` vacío: capturar y descartar en silencio convierte un fallo diagnosticable en un comportamiento erróneo sin rastro, y si de verdad se quiere ignorar algo, hay que dejar constancia explícita del motivo. Java es además el único lenguaje mayoritario con **excepciones comprobadas** (*checked*), que el compilador obliga a capturar o a declarar en la firma; C# rechazó esa idea de forma deliberada, y Anders Hejlsberg argumentó públicamente que escalan mal por dos razones: el versionado (añadir una excepción a una función rompe a todos sus llamadores) y el acoplamiento que impone a cada firma de la cadena de llamadas. Casi ningún lenguaje posterior las ha adoptado. Sobre el coste, conviene saber que lo caro no es el `try` —que en implementaciones modernas es de coste cero cuando no se lanza nada— sino construir el objeto de excepción con su traza de pila; por eso lanzar dentro de un bucle caliente es un antipatrón, con la notable excepción de Python, donde el propio protocolo de iteración termina lanzando `StopIteration` y el estilo EAFP (*easier to ask forgiveness than permission*) hace del `try` una herramienta cotidiana.

## 🧩 Situación

El manejo de excepciones es la columna vertebral de la fiabilidad en cualquier sistema que hable con el mundo exterior: un servidor HTTP que consulta una base de datos, un proceso que lee archivos, un cliente que llama a una API. Todos esos límites fallan de forma rutinaria —la conexión se cae, el disco se llena, el JSON viene mal formado— y la pregunta de ingeniería no es si fallarán, sino dónde se colocará el manejador. La respuesta típica en una aplicación bien construida es que los fallos suben sin tratarse hasta una frontera concreta (el manejador de una petición, el bucle principal de un *worker*), donde se convierten en una respuesta de error, se registran con su traza y se decide si reintentar. Cada `catch` colocado prematuramente en una capa intermedia es una decisión de arquitectura, y casi siempre una decisión de tragarse información que la capa superior necesitaba.

Dividir entre cero es la versión mínima de ese patrón, y por eso importa. En Java, C#, Python y PHP la división entera por cero lanza una excepción; capturarla evita que el proceso termine abruptamente con un volcado ilegible. El coste de no hacerlo bien se mide en incidentes reales: un `catch` demasiado amplio que oculta un `NullPointerException` de un bug distinto convierte una hora de depuración en tres días; un recurso liberado solo en el camino feliz —sin `finally`— produce fugas de descriptores de archivo o de conexiones que agotan el *pool* y tumban el servicio bajo carga, un fallo que solo se manifiesta en producción y nunca en las pruebas. La mantenibilidad también sufre: cuando el manejo de errores está disperso en decenas de `catch` ad hoc, cambiar la política de errores de un sistema deja de ser una modificación local y se convierte en una auditoría del código entero.

## 🧮 Modelo

- **Entrada** (stdin): una línea `a b` (dos enteros)
- **Salida** (stdout): `resultado=<a/b entera>` o `error=division por cero` si b es 0
- **Regla:** si b != 0 → a/b (entera); si b == 0 → mensaje de error

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `10 2` | `resultado=5` |
| `7 0` | `error=division por cero` |
| `9 3` | `resultado=3` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER a, b
INTENTAR: r <- a/b ; ESCRIBIR "resultado=" r
CAPTURAR division_por_cero: ESCRIBIR "error=division por cero"
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys

a, b = map(int, sys.stdin.readline().split())
try:
    r = a // b
    print(f"resultado={r}")
except ZeroDivisionError:
    print("error=division por cero")
```

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const [a, b] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
try {
  if (b === 0) throw new Error("div");
  console.log(`resultado=${Math.trunc(a / b)}`);
} catch {
  console.log("error=division por cero");
}
```

🧬 **El mismo programa en la familia JavaScript / web:** [Dart · ActionScript](primos.md#javascript-web)

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const [a, b]: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
try {
  if (b === 0) throw new Error("div");
  console.log(`resultado=${Math.trunc(a / b)}`);
} catch {
  console.log("error=division por cero");
}
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
        int a = Integer.parseInt(p[0]);
        int b = Integer.parseInt(p[1]);
        try {
            int r = a / b;
            System.out.println("resultado=" + r);
        } catch (ArithmeticException e) {
            System.out.println("error=division por cero");
        }
    }
}
```

🧬 **El mismo programa en la familia JVM:** [Kotlin · Scala · Groovy · Clojure](primos.md#jvm)

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
int a = int.Parse(p[0]);
int b = int.Parse(p[1]);
try {
    int r = a / b;
    Console.WriteLine($"resultado={r}");
} catch (DivideByZeroException) {
    Console.WriteLine("error=division por cero");
}
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
	a, _ := strconv.Atoi(f[0])
	b, _ := strconv.Atoi(f[1])
	// Go no usa excepciones: comprueba antes de dividir.
	if b == 0 {
		fmt.Println("error=division por cero")
	} else {
		fmt.Printf("resultado=%d\n", a/b)
	}
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
    let (a, b) = (v[0], v[1]);
    // Rust no usa excepciones: checked_div devuelve Option.
    match a.checked_div(b) {
        Some(r) => println!("resultado={r}"),
        None => println!("error=division por cero"),
    }
}
```

🧬 **El mismo programa en la familia Sistemas:** [Zig · Nim · D](primos.md#sistemas)

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long a, b;
    if (scanf("%ld %ld", &a, &b) != 2) return 1;
    /* C no tiene excepciones: comprobar antes de dividir. */
    if (b == 0) {
        printf("error=division por cero\n");
    } else {
        printf("resultado=%ld\n", a / b);
    }
    return 0;
}
```

🧬 **El mismo programa en la familia C / llaves:** [C++ · Objective-C](primos.md#c-llaves)

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL: evita el error comprobando el divisor con CASE WHEN.
WITH pares(a, b) AS (VALUES (10, 2), (7, 0), (9, 3))
SELECT CASE WHEN b = 0 THEN 'error=division por cero'
            ELSE printf('resultado=%d', a / b) END AS resultado
FROM pares;
```

🧬 **El mismo programa en la familia Lógica y declarativa:** [Prolog · Datalog](primos.md#logica-declarativa)

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
[$a, $b] = preg_split('/\s+/', trim(fgets(STDIN)));
$a = (int) $a;
$b = (int) $b;
try {
    $r = intdiv($a, $b);
    echo "resultado=$r\n";
} catch (DivisionByZeroError $e) {
    echo "error=division por cero\n";
}
```

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔎 Recorrido del código: de la entrada a la salida

Sigamos el caso `7 0` de `casos.json`, cuya salida esperada es `error=division por cero`. En **Python**, la línea `a, b = map(int, sys.stdin.readline().split())` deja `a = 7` y `b = 0`. Entra el bloque `try:` y se evalúa `r = a // b`. Aquí ocurre lo interesante: el operador `//` no devuelve nada, sino que el intérprete construye un objeto `ZeroDivisionError` y transfiere el control fuera de la línea. La asignación a `r` nunca se completa y —punto clave— la línea siguiente, `print(f"resultado={r}")`, **no se ejecuta**: el resto del `try` se abandona por completo. El intérprete busca entonces un manejador que acepte ese tipo, encuentra `except ZeroDivisionError:` y ejecuta su cuerpo, imprimiendo `error=division por cero`. Con el caso `10 2` el recorrido es el contrario: `a // b` da `5`, se asigna a `r`, se imprime `resultado=5` y el bloque `except` se salta entero, porque un manejador solo corre si hubo excepción.

En **Go** el mismo caso recorre un camino radicalmente distinto, porque Go no tiene excepciones y el código lo dice explícitamente en su comentario. Tras leer la línea con `bufio.NewReader(os.Stdin).ReadString('\n')` y trocearla con `strings.Fields`, `strconv.Atoi` convierte `f[0]` en `7` y `f[1]` en `0`. Entonces llega `if b == 0 {` — una comprobación *previa*, no un manejador posterior. Como `b` vale cero, se imprime `error=division por cero` y la división `a/b` **nunca llega a ejecutarse**. Esto no es un detalle estilístico: si el `if` faltara, `a/b` con `b = 0` provocaría un `panic` en tiempo de ejecución que abortaría el proceso, porque en Go la división entera por cero no es un valor legítimo sino un error irrecuperable. El programador previene, no captura.

**Rust** ofrece el tercer contraste, y es el más sutil de los tres. Tras leer la entrada y construir el vector con `s.split_whitespace().map(|x| x.parse().unwrap()).collect()`, quedan `a = 7` y `b = 0`. La división se hace con `a.checked_div(b)`, que en lugar de operar a ciegas devuelve un `Option<i64>`: `Some(r)` si la división es válida, `None` si el divisor es cero o si hubiera desbordamiento. El `match` que sigue no es un manejador de excepciones sino una selección sobre un valor ordinario: la rama `None => println!("error=division por cero")` es la que se ejecuta. La diferencia conceptual es que aquí el fallo *no es un salto*, es un dato que el compilador obliga a considerar, porque un `match` sobre `Option` que olvide la rama `None` sencillamente no compila. Las tres versiones transforman el mismo `7 0` en el mismo texto, pero Python descubre el fallo lanzando, Go lo previene comprobando y Rust lo codifica en el tipo del resultado — que es justo el hilo que retoma la clase siguiente.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `try/except` (Python), `try/catch` (Java/C#/JS/PHP). |
| Semántica | Java/C#/Python/PHP lanzan en /0 entero; JS da Infinity (hay que comprobar); Go/Rust no usan excepciones. |
| Paradigmática | SQL evita el error con CASE WHEN b=0. |

Los diez lenguajes del núcleo se ordenan con nitidez según una sola pregunta: ¿qué hace el lenguaje cuando una operación no puede completarse? Un primer grupo lanza y ofrece el aparato completo de captura. **Python** usa `try/except/finally` y su `ZeroDivisionError` forma parte de una jerarquía que cuelga de `BaseException`; su cultura EAFP hace del `try` algo cotidiano, no excepcional. **Java** lanza `ArithmeticException` en la división entera por cero (aunque `1.0/0` en coma flotante da `Infinity`, siguiendo IEEE 754) y es el único del grupo con excepciones comprobadas. **C#** lanza `DivideByZeroException` y ofrece `try/catch/finally` casi idéntico al de Java, pero sin *checked exceptions* por la decisión explícita de Hejlsberg. **PHP** se sumó tarde y bien: desde PHP 7 existe la interfaz `Throwable` con dos ramas, `Exception` para los errores de aplicación y `Error` para los del motor —y `DivisionByZeroError`, que captura la implementación de esta clase, pertenece a la segunda—, un cambio que Lockhart señala en *Modern PHP* como parte de la modernización del lenguaje. Un segundo grupo tiene la sintaxis pero no el disparo: **JavaScript** y **TypeScript** disponen de `try/catch/finally` (con el `catch` sin parámetro desde ES2019, que es justo el que usan las implementaciones), pero `7 / 0` no lanza nada — devuelve `Infinity` según IEEE 754, y por eso ambos códigos tienen que escribir a mano `if (b === 0) throw new Error("div")`. El tercer grupo renuncia al mecanismo: **Go** tiene `panic`/`recover` y **Rust** tiene `panic!` y `catch_unwind`, pero ambos los reservan para lo irrecuperable —un índice fuera de rango, un invariante roto— y esperan que los errores previsibles viajen como valores; **C**, en el extremo, no tiene nada: solo `errno`, códigos de retorno y el par `setjmp`/`longjmp`, que permite un salto no local pero sin destruir objetos ni ejecutar limpieza, con todo el peligro que eso implica. Y **SQL**, declarativo, ni lanza ni comprueba: resuelve el caso con un `CASE WHEN b = 0` dentro de la propia expresión.

## 🧬 El concepto en la familia

La familia de C se dividió en dos ante esta cuestión. C, el tronco, no tiene excepciones en absoluto y las simula con códigos de retorno, la variable global `errno` que documentan Kernighan y Ritchie, y en casos extremos `setjmp`/`longjmp`. Sus descendientes con objetos —C++, Java, C#— sí las adoptaron, y con ellas nació el modelo canónico `try/catch/finally` que hoy reconoce cualquier programador; Java le añadió las excepciones comprobadas y C# las descartó, y ese es probablemente el desacuerdo de diseño más citado entre lenguajes hermanos. La familia del scripting dinámico las abrazó sin reservas: Python (`try/except/else/finally`), Ruby (`begin/rescue/ensure`), PHP desde su versión 7 y JavaScript comparten la idea de que casi cualquier error es una excepción, y Python llega a construir sobre ella su protocolo de iteración con `StopIteration`. La familia ML y funcional prefiere otra vía: Haskell representa el fallo en el tipo con `Either e a` y `Maybe a` y lo compone con la mónada de error, Scala envuelve el cómputo arriesgado en `Try[T]` con sus casos `Success` y `Failure` —un puente explícito entre excepciones y valores—, y F# usa `Result<'T,'TError>`; en todos ellos la excepción existe pero se considera el recurso de última instancia. Go y Rust, los dos lenguajes de sistemas modernos, se apartaron deliberadamente del modelo: `panic`/`recover` y `panic!` están ahí para lo irrecuperable, no para el flujo normal. Y los lenguajes declarativos como SQL no tienen el concepto en el sentido habitual: el fallo se evita en la expresión (`CASE WHEN`, `NULLIF`) o se maneja fuera, en el cliente que ejecuta la consulta.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 071
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Capturar todo con un `catch` vacío** → causa: un `except Exception: pass` o un `catch (Exception e) {}` atrapa también los fallos que no esperabas —un error de programación, un fallo de memoria— y los borra sin dejar rastro, convirtiendo un problema diagnosticable en un comportamiento erróneo sin causa visible → solución: capturar el tipo más específico posible (`ZeroDivisionError`, no `Exception`), y si de verdad hay que ignorar algo, registrarlo o dejar un comentario que explique por qué es seguro hacerlo, tal como recomienda Bloch.
- **Capturar lo general antes que lo específico** → causa: colocar `catch (Exception e)` delante de `catch (ArithmeticException e)` hace que el primero se lleve todas las excepciones y el segundo quede muerto; en Java ni siquiera compila, pero en lenguajes más laxos pasa desapercibido → solución: ordenar los manejadores de la subclase más concreta a la superclase más amplia, y recordar que el primero que coincide gana.
- **Poner un `return` dentro de `finally`** → causa: `finally` se ejecuta siempre, incluso mientras una excepción está propagándose; si su cuerpo hace `return` (o lanza otra excepción), esa salida **sustituye** a la excepción en curso y el fallo original desaparece por completo, dejando al llamador con un valor aparentemente normal → solución: usar `finally` solo para limpiar, nunca para devolver valores ni alterar el resultado; mejor aún, delegar la limpieza en `try-with-resources` (Java), `using` (C#) o `with` (Python), que liberan el recurso automáticamente sin `finally` manual.
- **Usar excepciones como control de flujo en un bucle caliente** → causa: lanzar y capturar en cada vuelta obliga a construir un objeto de excepción con su traza de pila completa, que es la parte cara del mecanismo; el resultado son órdenes de magnitud de diferencia frente a un simple `if` → solución: reservar las excepciones para condiciones realmente excepcionales y comprobar por adelantado lo que se puede comprobar; la salvedad es Python, donde el propio lenguaje usa `StopIteration` internamente y el estilo EAFP está aceptado.
- **Asumir que dividir por cero siempre lanza** → causa: en JavaScript y TypeScript `7 / 0` devuelve `Infinity` (IEEE 754) y `0 / 0` devuelve `NaN`, sin excepción alguna; en Go y Rust el comportamiento es un `panic` o un valor comprobado, no algo capturable con `catch` → solución: conocer la semántica aritmética del lenguaje concreto y comprobar el divisor explícitamente donde el lenguaje no colabora, exactamente como hacen las implementaciones de JS, TS, Go y C de esta clase.

## ❓ Preguntas frecuentes

- **¿Excepciones o valores de error?** Las excepciones mantienen limpio el camino feliz —el código de éxito se lee de corrido y el manejo queda aparte— pero ocultan por dónde puede escaparse el flujo. Los valores de error hacen lo contrario: explícito y visible, a costa de contaminar cada firma y cada llamada. La heurística práctica es usar excepciones para lo verdaderamente excepcional (fallos que no forman parte del contrato normal de la función) y valores para los errores esperables y frecuentes, como una entrada inválida. La clase siguiente desarrolla el otro lado del debate.
- **¿Para qué sirve exactamente `finally`?** Para código que debe ejecutarse haya o no fallo: cerrar un archivo, devolver una conexión al *pool*, soltar un cerrojo. Su garantía es que corre tanto si el `try` termina normalmente, como si lanza, como si hace `return` en medio. Ese es precisamente el motivo de que un `return` dentro del propio `finally` sea peligroso: se ejecuta también mientras una excepción sube, y la anula.
- **¿Qué son las excepciones comprobadas y por qué casi nadie las copió?** En Java, ciertas excepciones deben capturarse o declararse con `throws` en la firma, y el compilador lo verifica. La intención era hacer visible el contrato de fallo de cada método. En la práctica generan dos problemas: añadir una excepción a una función rompe la compilación de todos sus llamadores (mal versionado) y la firma acaba acoplada a detalles de implementación de capas inferiores. Hejlsberg citó ambas razones al explicar por qué C# no las incluyó, y ningún lenguaje mayoritario posterior las ha adoptado.
- **¿Es caro lanzar una excepción?** El `try` en sí es prácticamente gratuito cuando no se lanza nada: las implementaciones modernas usan tablas que solo se consultan si hay un fallo. Lo caro es crear el objeto de excepción, porque capturar la traza de pila implica recorrer los marcos activos. Por eso una excepción por segundo es irrelevante y un millón por segundo dentro de un bucle es un problema medible de rendimiento.

## 🔗 Referencias

**Libros de la parte:**

- O.-J. Dahl, E. W. Dijkstra y C. A. R. Hoare — *Structured Programming* (Academic Press). Su defensa del flujo de control disciplinado es el trasfondo contra el que se mide la excepción: un salto no local que rompe la lectura lineal y que por eso conviene acotar a fronteras bien definidas.
- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson), cap. sobre manejo de excepciones. Sistematiza el mecanismo —propagación por la pila, selección del manejador por tipo, jerarquías— y compara cómo lo resolvieron Ada, C++, Java, C# y Python.

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

> [⏮️ Clase 070](../../parte-4-control-del-programa/070-control-de-flujo-break-continue-return-goto/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 072 ⏭️](../../parte-4-control-del-programa/072-manejo-de-errores-ii-resultados-y-valores-result-either-error-de-go/README.md)
