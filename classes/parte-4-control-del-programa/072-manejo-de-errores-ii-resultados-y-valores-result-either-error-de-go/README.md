# Clase 072 — Manejo de errores II: resultados y valores (Result/Either/error de Go)

> Parte **4 — Control del programa** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

La clase anterior trató el error como un canal aparte: algo que se lanza, que viaja por la pila y que se captura lejos del punto donde ocurrió. Esta clase invierte la idea por completo. Si una función puede fallar, que lo diga en su tipo de retorno y que devuelva el fallo como cualquier otro dato: `Result<T, E>` en Rust, `Either e a` en Haskell, el par `(valor, error)` en Go, `Option<T>` cuando basta con distinguir "hay valor" de "no hay". El error deja de ser un salto de control y pasa a ser un valor ordinario que se inspecciona, se transforma y se propaga con las mismas herramientas que cualquier otro valor del lenguaje. La consecuencia es que la posibilidad de fallo se vuelve **visible en la firma**: leyendo `func dividir(a, b int) (int, error)` ya sabes que esta operación puede no funcionar, sin abrir la implementación ni leer documentación.

En esta clase dividimos dos enteros devolviendo un resultado en lugar de lanzar, y comparamos cómo cada lenguaje representa esa dualidad éxito/fallo: con un tipo suma real (Rust, Haskell), con una convención de tupla (Go, Python, C#), con un tipo unión discriminado (TypeScript), con `Optional` (Java), con un diccionario (PHP) o con el clásico código de retorno más puntero de salida (C). Veremos las herramientas que hacen este estilo llevadero —el operador `?` de Rust, que propaga el error en un solo carácter— y la propiedad decisiva que lo sostiene: el atributo `#[must_use]` que hace que el compilador de Rust avise si ignoras un `Result`. Y veremos también su fallo característico, el espejo del `catch` vacío de la clase anterior: el error simplemente olvidado. El debate de fondo —excepciones frente a valores— no tiene un ganador universal, pero sí una tendencia clara: Rust, Go, Swift y Kotlin, los lenguajes de diseño más reciente, se han inclinado por lo explícito.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Representar el error como un valor de retorno.
2. Manejar el resultado con match o comprobación.
3. Comparar excepciones con valores de error.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Errores como valores | El error es un dato, no un salto |
| 2 | Result / Either | Éxito o fallo tipado |
| 3 | El par (valor, error) de Go | Convención idiomática |
| 4 | Manejo explícito | No se puede ignorar por accidente |

## 📖 Definiciones y características

- **Result/Either** — tipo que contiene un valor de éxito o uno de error (Rust, Haskell). Clave: obliga a manejar ambos.
- **Valor de error** — devolver el error como dato en lugar de lanzarlo. Clave: flujo explícito.
- **Convención de Go** — devolver `(valor, error)` y comprobar `if err != nil`. Clave: errores visibles.
- **Manejo explícito** — el compilador o el estilo obligan a tratar el error. Clave: menos fallos silenciosos.

En Go, `error` no es una construcción del lenguaje sino una interfaz ordinaria de la biblioteca estándar, con un único método que devuelve un texto; cualquier tipo que lo implemente sirve como error, y `nil` significa "sin error". Donovan y Kernighan defienden en *The Go Programming Language* que este diseño es una elección consciente y no una carencia: al obligar a escribir `if err != nil` justo después de cada llamada, el manejo del fallo queda **en el punto exacto donde ocurre**, a la vista del lector, en lugar de en un manejador remoto varios marcos más arriba. El precio, que ellos mismos reconocen, es la verbosidad: una función que hace cinco llamadas falibles tendrá cinco bloques de comprobación. Rust ataca el mismo problema desde el sistema de tipos. Como explican Klabnik y Nichols en *The Rust Programming Language*, `Result<T, E>` y `Option<T>` no son magia del compilador sino enumeraciones corrientes con dos variantes (`Ok`/`Err`, `Some`/`None`); lo que las hace poderosas es que para extraer el valor hay que pasar por un `match` que el compilador exige exhaustivo — no puedes leer el éxito sin haber escrito qué ocurre en el fallo. El operador `?` resuelve la verbosidad: colocado tras una expresión que devuelve `Result`, extrae el valor si es `Ok` y hace `return` del error si es `Err`, condensando en un carácter lo que en Go ocupa tres líneas. Y `unwrap`/`expect`, que sacan el valor asumiendo el éxito, son atajos legítimos en pruebas y prototipos pero bombas de relojería en producción: convierten el error en un `panic` que aborta el proceso.

La propiedad decisiva de este enfoque, sin embargo, es más sutil que la sintaxis. `Result` en Rust está marcado con el atributo `#[must_use]`, lo que significa que si llamas a una función falible y descartas su retorno, el compilador **te avisa**. Ese detalle es el que convierte una convención en una garantía: el sistema de tipos te obliga a considerar el fallo. La idea viene de la tradición ML y funcional, donde Haskell modela el fallo con `Maybe a` (hay valor o no lo hay) y `Either e a` (éxito a la derecha, error a la izquierda), y compone cadenas de operaciones falibles mediante la mónada de error, de modo que el primer fallo cortocircuita el resto sin escribir una sola comprobación. Los lenguajes que llegaron después han tomado prestado el concepto con distinto grado de fidelidad: Java añadió `Optional` en la versión 8, sobre el que Bloch advierte en *Effective Java* que está pensado para el retorno de métodos y no debe usarse en campos, en parámetros ni en colecciones, porque añade una indirección y una asignación sin resolver nada que un `null` comprobado no resolviera igual. C# ofrece los tipos anulables y el patrón `bool TryX(out T)` —`int.TryParse` es el ejemplo canónico— que separa el "¿funcionó?" del valor obtenido. TypeScript no tiene soporte del lenguaje, pero sus **tipos unión discriminados** (`{ ok: true, value } \| { ok: false, error }`) consiguen lo mismo: el estrechamiento de tipos impide leer `value` sin haber comprobado antes la discriminante, un patrón que Cherny desarrolla en *Programming TypeScript*.

## 🧩 Situación

Este estilo domina hoy la programación de sistemas y de servicios. En Go, cualquier operación de red, de archivo o de codificación devuelve un `error` junto al valor, y el código de producción de un servidor real es en buena medida una secuencia de llamadas seguidas de `if err != nil`, cada una decidiendo si envolver el error con contexto (`fmt.Errorf("leyendo config: %w", err)`) y devolverlo hacia arriba, o si tratarlo ahí mismo. En Rust ocurre lo equivalente con `?` encadenado hasta una función que decide la política. Y fuera de esos dos lenguajes el patrón reaparece constantemente: los clientes HTTP de TypeScript que devuelven un objeto discriminado en lugar de lanzar, las funciones de C# que exponen un `TryGet`, los repositorios de Java que devuelven `Optional<Usuario>` en lugar de `null`.

Lo que está en juego es concreto y medible. El fallo característico de este enfoque no es el manejo desordenado sino el **error olvidado**: en Go, escribir `res, _ := dividir(a, b)` descarta el error de forma perfectamente legal y silenciosa, y por eso existe `errcheck`, un linter que se ejecuta en CI precisamente para cazar esos descartes. En C el problema es histórico y mucho más grave: ignorar el valor de retorno de `malloc` y usar un puntero nulo, o ignorar cuántos bytes devolvió realmente `read` y asumir que se leyó el buffer completo, son dos de las fuentes clásicas de vulnerabilidades de memoria documentadas durante décadas — el mecanismo estaba ahí, pero nada obligaba a mirarlo. De ahí que la aportación de Rust con `#[must_use]` sea tan relevante en términos de coste: convierte una clase entera de bugs de producción en un aviso en tiempo de compilación. En cuanto a mantenibilidad, la ventaja es que la firma documenta el contrato de fallo, así que refactorizar no requiere adivinar qué puede lanzar una función; la desventaja es la que anticipaban Donovan y Kernighan, y es real: el ruido de las comprobaciones puede llegar a enterrar la lógica de negocio si no se agrupa con cuidado.

## 🧮 Modelo

- **Entrada** (stdin): una línea `a b` (dos enteros)
- **Salida** (stdout): `ok=<a/b entera>` o `err=division` si b es 0
- **Regla:** si b != 0 → Ok(a/b); si b == 0 → Err(division)

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `10 2` | `ok=5` |
| `7 0` | `err=division` |
| `8 4` | `ok=2` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER a, b
res <- dividir(a,b)  // devuelve Ok(v) o Err
SEGUN res: Ok(v)->"ok="v ; Err->"err=division"
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys


def dividir(a, b):
    if b == 0:
        return (None, "division")
    return (a // b, None)


a, b = map(int, sys.stdin.readline().split())
valor, err = dividir(a, b)
if err is not None:
    print(f"err={err}")
else:
    print(f"ok={valor}")
```

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

function dividir(a, b) {
  if (b === 0) return { err: "division" };
  return { ok: Math.trunc(a / b) };
}

const [a, b] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const r = dividir(a, b);
console.log(r.err ? `err=${r.err}` : `ok=${r.ok}`);
```

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

type Res = { ok: number } | { err: string };

function dividir(a: number, b: number): Res {
  if (b === 0) return { err: "division" };
  return { ok: Math.trunc(a / b) };
}

const [a, b]: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const r = dividir(a, b);
console.log("err" in r ? `err=${r.err}` : `ok=${r.ok}`);
```

### Java · [`java/Main.java`](implementaciones/java/Main.java) · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Optional;

public class Main {
    static Optional<Integer> dividir(int a, int b) {
        return b == 0 ? Optional.empty() : Optional.of(a / b);
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        int a = Integer.parseInt(p[0]);
        int b = Integer.parseInt(p[1]);
        Optional<Integer> r = dividir(a, b);
        System.out.println(r.isPresent() ? "ok=" + r.get() : "err=division");
    }
}
```

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;

(int? ok, string err) Dividir(int a, int b) =>
    b == 0 ? (null, "division") : (a / b, null);

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
int a = int.Parse(p[0]);
int b = int.Parse(p[1]);
var (ok, err) = Dividir(a, b);
Console.WriteLine(err != null ? $"err={err}" : $"ok={ok}");
```

### Go · [`go/main.go`](implementaciones/go/main.go) · `go run main.go`

```go
package main

import (
	"bufio"
	"errors"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func dividir(a, b int) (int, error) {
	if b == 0 {
		return 0, errors.New("division")
	}
	return a / b, nil
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	f := strings.Fields(line)
	a, _ := strconv.Atoi(f[0])
	b, _ := strconv.Atoi(f[1])
	res, err := dividir(a, b)
	if err != nil {
		fmt.Printf("err=%s\n", err)
	} else {
		fmt.Printf("ok=%d\n", res)
	}
}
```

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn dividir(a: i64, b: i64) -> Result<i64, String> {
    if b == 0 {
        Err("division".to_string())
    } else {
        Ok(a / b)
    }
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let v: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    match dividir(v[0], v[1]) {
        Ok(r) => println!("ok={r}"),
        Err(e) => println!("err={e}"),
    }
}
```

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

/* C: se usa un valor de retorno para señalar el error (0 = ok, 1 = error). */
int dividir(long a, long b, long *out) {
    if (b == 0) return 1;
    *out = a / b;
    return 0;
}

int main(void) {
    long a, b, r;
    if (scanf("%ld %ld", &a, &b) != 2) return 1;
    if (dividir(a, b, &r) != 0) {
        printf("err=division\n");
    } else {
        printf("ok=%ld\n", r);
    }
    return 0;
}
```

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL: sin tipo de error; se distingue el caso con CASE WHEN.
WITH pares(a, b) AS (VALUES (10, 2), (7, 0), (8, 4))
SELECT CASE WHEN b = 0 THEN 'err=division'
            ELSE printf('ok=%d', a / b) END AS resultado
FROM pares;
```

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
function dividir($a, $b) {
    if ($b === 0) {
        return ["err" => "division"];
    }
    return ["ok" => intdiv($a, $b)];
}

[$a, $b] = preg_split('/\s+/', trim(fgets(STDIN)));
$r = dividir((int) $a, (int) $b);
echo isset($r["err"]) ? "err={$r['err']}\n" : "ok={$r['ok']}\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔎 Recorrido del código: de la entrada a la salida

Sigamos el caso `7 0` de `casos.json`, cuya salida esperada es `err=division`. En **Python**, la función `dividir(a, b)` implementa la convención de Go a mano: devuelve una tupla de dos elementos donde uno de los dos siempre es `None`. Con `a = 7` y `b = 0`, la primera línea del cuerpo, `if b == 0:`, se cumple y devuelve `(None, "division")` — nótese que la división `a // b` **nunca se evalúa**, así que el `ZeroDivisionError` de la clase anterior no llega a existir. En el cuerpo principal, `valor, err = dividir(a, b)` desempaqueta la tupla dejando `valor = None` y `err = "division"`. La comprobación `if err is not None:` es verdadera y se imprime `err=division`. Con el caso `10 2` el recorrido es el complementario: la función devuelve `(5, None)`, la comprobación falla y se ejecuta la rama `else` con `ok=5`. La convención funciona, pero es puramente disciplinaria: nada en Python impide escribir `valor, _ = dividir(a, b)` y quedarse con un `None` silencioso.

**Go** hace exactamente lo mismo, pero con la firma como contrato. `func dividir(a, b int) (int, error)` declara en el tipo de retorno que esta operación puede fallar. Con `b = 0`, la rama `return 0, errors.New("division")` construye un valor de error y lo devuelve junto a un `0` que es solo relleno — el llamador no debe mirarlo. En `main`, tras leer y convertir la línea, `res, err := dividir(a, b)` recibe ambos, y el idiomático `if err != nil` resulta verdadero, imprimiendo `err=%s` con el texto `division` que produce el método `Error()` de la interfaz. Aquí está la diferencia con Python: `err` es de tipo `error`, una interfaz declarada en la firma, y ningún lector puede llamar a `dividir` sin ver que devuelve dos cosas. Lo que Go no impide es el descarte deliberado — de hecho el propio programa lo usa dos veces en `strconv.Atoi(f[0])`, ignorando con `_` los errores de conversión, algo aceptable en un ejercicio con entrada controlada y peligroso en código real.

**Rust** cierra el contraste llevando la idea al sistema de tipos. La firma `fn dividir(a: i64, b: i64) -> Result<i64, String>` no devuelve dos valores sino **uno solo** que es de uno de dos tipos: con `b = 0` se construye `Err("division".to_string())`, y en el caso contrario `Ok(a / b)`. La diferencia crucial aparece en `main`: no hay un valor de éxito accesible junto a un error opcional, sino un `Result` que debe abrirse con `match dividir(v[0], v[1])`. La rama `Err(e) => println!("err={e}")` es la que se ejecuta con `7 0`, y `e` solo existe dentro de esa rama. La rama `Ok(r)` es inalcanzable en este caso, y `r` solo existe dentro de la suya. No es posible leer el valor de éxito sin haber pasado por una comprobación, y si el `match` omitiera cualquiera de las dos ramas el programa no compilaría. Las tres versiones producen el mismo `err=division`, pero Python lo consigue por convención, Go por firma explícita y Rust por imposición del compilador.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `Result`/`match` (Rust) vs. `(v, err)` (Go) vs. if/else (otros). |
| Semántica | Rust/Go obligan a manejar el error; ignorarlo es visible o imposible. |
| Paradigmática | SQL usa CASE WHEN, sin tipo de error. |

Agrupados por *cómo* representan la dualidad éxito/fallo, los diez lenguajes se reparten en cuatro familias claras. La primera tiene un **tipo suma auténtico**: solo **Rust**, con `Result<i64, String>`, donde el éxito y el error son variantes de un mismo valor que el `match` exhaustivo obliga a distinguir, y donde `#[must_use]` hace que descartarlo genere un aviso del compilador. La segunda usa una **tupla o par por convención**: **Go** con su `(int, error)` canónico —el único de los diez donde esto es el idioma oficial del lenguaje, sancionado por la biblioteca estándar entera—, **Python** imitándolo con `(valor, err)` y `None` como marca de ausencia, y **C#** con la tupla con nombres `(int? ok, string err)`, que aprovecha los tipos anulables y es primo directo del patrón `bool TryParse(string, out int)` que Skeet documenta en *C# in Depth*. La tercera representa el resultado con un **objeto de forma variable**: **JavaScript** devuelve `{ err: "division" }` o `{ ok: n }` y decide con un simple `r.err ?`, sin ninguna red de seguridad; **TypeScript** eleva exactamente el mismo objeto a un tipo unión discriminado, `type Res = { ok: number } \| { err: string }`, y el `"err" in r` del código no es un truco sino un *type guard* que hace que el compilador estreche el tipo y prohíba leer `r.ok` en la rama equivocada; **PHP** hace lo propio con un array asociativo y `isset`, sin verificación estática; y **Java** utiliza `Optional<Integer>`, que distingue presencia de ausencia pero —limitación importante— no transporta el *motivo* del fallo, por lo que la cadena `"error=division"` tiene que escribirse en el llamador. La cuarta familia es la de los que carecen del concepto: **C** recurre al patrón histórico de `int dividir(long a, long b, long *out)`, donde el retorno es un código de estado (`0` correcto, `1` error) y el resultado real sale por un puntero — el mecanismo más frágil de todos, porque nada obliga a mirar el código devuelto; y **SQL**, declarativo, no tiene tipo de error en absoluto y discrimina el caso dentro de la propia expresión con `CASE WHEN b = 0`. El eje que ordena a los diez es siempre el mismo: cuánta ayuda te da el lenguaje para que no olvides el fallo, desde ninguna (C, JS, PHP) hasta un error de compilación (Rust).

## 🧬 El concepto en la familia

La familia de C inventó la versión primitiva de esta idea y se quedó en ella: el código de retorno entero más un puntero de salida, con `errno` como canal auxiliar. Es el patrón que documentan Kernighan y Ritchie, y su debilidad —nada obliga a comprobar el retorno— explica una parte considerable de la historia de vulnerabilidades en C. Sus descendientes orientados a objetos (C++, Java, C#) se pasaron a las excepciones y solo han vuelto parcialmente sobre sus pasos: `Optional` en Java 8, los tipos anulables y `TryX(out T)` en C#, `std::optional` y `std::expected` en C++ moderno. La familia del scripting dinámico no tiene el concepto integrado y lo simula con estructuras de datos: tuplas en Python, objetos literales en JavaScript, arrays asociativos en PHP — funciona, pero sin ninguna comprobación que respalde la convención. La familia ML y funcional es el origen intelectual del enfoque: Haskell distingue `Maybe a` para la simple ausencia de `Either e a` para el fallo con causa, y su instancia de mónada permite encadenar operaciones falibles donde el primer `Left` cortocircuita todo lo demás; Scala envuelve el cómputo en `Try[T]` (`Success`/`Failure`), que actúa de puente entre el mundo de las excepciones de la JVM y el de los valores; F# usa `Result<'T,'TError>` con el mismo espíritu. Go y Rust son los herederos modernos de esa tradición, cada uno a su manera: Go con la simplicidad radical de una interfaz y una convención, Rust con el rigor de un tipo suma que el compilador vigila mediante exhaustividad y `#[must_use]`. Fuera del núcleo, Swift combina ambos mundos con `throws` y `try` sobre un modelo de valores, y Kotlin ofrece `Result<T>` junto a sus clases selladas. Los lenguajes declarativos como SQL quedan al margen: no hay tipo de error porque no hay función que devolver, solo expresiones que deben producir un valor para cada fila.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 072
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Ignorar el error devuelto** → causa: es el fallo característico de este enfoque, el espejo del `catch` vacío; en Go basta `res, _ := dividir(a, b)` para descartar el error de forma legal y silenciosa y seguir con un valor de relleno; en C, ignorar el retorno de `malloc` o el número de bytes de `read` es una fuente clásica y documentada de vulnerabilidades → solución: comprobar siempre el error antes de tocar el valor, y automatizarlo: `errcheck` en CI para Go, y en Rust apoyarse en el aviso de `#[must_use]` que el compilador emite al descartar un `Result`, elevándolo a error con `#![deny(unused_must_use)]`.
- **Abusar de `unwrap` y `expect` en producción** → causa: ambos extraen el valor asumiendo el éxito y convierten cualquier `Err` o `None` en un `panic` que aborta el proceso; son cómodos en un prototipo —de hecho aparecen en las implementaciones de esta clase al leer stdin— pero en un servicio real un `unwrap` es una caída garantizada ante la primera entrada inesperada → solución: reservarlos para invariantes verdaderamente imposibles y documentar el porqué con `expect("mensaje que explica por qué no puede fallar")`; en el resto, propagar con `?` o decidir con `match`.
- **Devolver un valor de éxito válido junto al error** → causa: en la convención de tupla nada impide devolver `(42, errors.New("fallo"))`, y un llamador descuidado puede usar el `42`; el contrato implícito de Go es que cuando `err != nil` el otro valor carece de significado, pero es una convención, no una regla del lenguaje → solución: devolver siempre el valor cero (`0`, `nil`, `""`) acompañando al error, tal como hace `return 0, errors.New("division")` en la implementación de esta clase, y no leer nunca el valor sin haber comprobado el error primero.
- **Perder el contexto al propagar** → causa: devolver el error tal cual a través de cinco capas produce un mensaje final como `division` que no dice en qué operación ni sobre qué datos ocurrió, y depurarlo obliga a adivinar → solución: envolver el error añadiendo contexto en cada frontera significativa —`fmt.Errorf("procesando fila %d: %w", i, err)` en Go, que conserva el original y permite recuperarlo con `errors.Is`/`errors.As`, o el ecosistema `anyhow`/`thiserror` en Rust— sin llegar al extremo de envolver en cada línea.
- **Mezclar excepciones y valores sin criterio** → causa: una base de código donde unas funciones lanzan y otras devuelven resultados obliga a cada llamador a recordar cuál es cuál, y el error acaba escapándose por la vía que nadie vigilaba → solución: fijar una política por proyecto (por ejemplo, valores para errores de dominio previsibles y excepciones solo en la frontera de infraestructura) y convertir explícitamente en los límites entre ambos mundos.

## ❓ Preguntas frecuentes

- **¿`Result` o excepciones?** El debate real es un intercambio, no una jerarquía. Las excepciones mantienen limpio el camino feliz pero ocultan el flujo de error: nada en la firma te dice qué puede lanzar. Los resultados hacen el fallo explícito y verificable, pero contaminan cada firma y cada llamada de la cadena con la posibilidad de error. La regla práctica es usar valores para lo previsible y frecuente (una entrada inválida, un recurso ausente) y excepciones para lo que rompe un invariante. Es significativo que los lenguajes de diseño más reciente —Rust, Go, Swift, Kotlin con `Result`— se hayan inclinado por lo explícito.
- **¿Por qué Go no tiene excepciones?** Es una decisión de diseño, no una omisión. Donovan y Kernighan argumentan que escribir `if err != nil` justo después de la llamada mantiene el manejo del fallo a la vista, en el punto donde el programador tiene todo el contexto, en lugar de en un manejador remoto que quizá no sepa qué falló. Go sí tiene `panic`/`recover`, pero reservados para lo irrecuperable. El coste reconocido es la verbosidad, y es la crítica más repetida al lenguaje.
- **¿Qué hace exactamente el operador `?` de Rust?** Puesto tras una expresión de tipo `Result`, si el valor es `Ok(v)` lo desenvuelve y la ejecución sigue con `v`; si es `Err(e)`, hace `return Err(e)` de la función actual inmediatamente, convirtiendo el tipo de error si hace falta. Condensa en un carácter el bloque de comprobación completo, lo que permite escribir cadenas de operaciones falibles con la misma fluidez del camino feliz pero conservando la propagación explícita. Solo funciona en funciones que devuelven `Result` u `Option`.
- **¿Puedo tener esto en TypeScript, que no lo trae?** Sí, y es el patrón recomendado: define un tipo unión discriminado como `{ ok: true, value: T } \| { ok: false, error: E }` (o el `{ ok: number } \| { err: string }` de esta clase) y comprueba la discriminante con `if ("err" in r)` o `if (r.ok)`. El estrechamiento de tipos del compilador hace el resto: en la rama de éxito solo existe `value`, en la de fallo solo `error`, y leer el campo equivocado es un error de compilación. Se obtiene casi toda la garantía de `Result` sin soporte del lenguaje — lo que falta es el equivalente a `#[must_use]`, así que nada impide ignorar el objeto entero.

## 🔗 Referencias

**Libros de la parte:**

- O.-J. Dahl, E. W. Dijkstra y C. A. R. Hoare — *Structured Programming* (Academic Press). Su insistencia en que el flujo de control sea localmente comprensible es el mejor argumento a favor de este estilo: un error devuelto se maneja donde se lee, sin saltos que atraviesen la pila.
- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson), cap. sobre control de flujo y manejo de excepciones. Sitúa el modelo de errores como valores frente al de excepciones y muestra por qué la decisión afecta a las firmas, a la composición y al versionado de las bibliotecas.

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

> [⏮️ Clase 071](../../parte-4-control-del-programa/071-manejo-de-errores-i-excepciones-try-catch-finally/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 073 ⏭️](../../parte-5-funciones-y-modularidad/073-firma-parametros-argumentos-y-retorno/README.md)
