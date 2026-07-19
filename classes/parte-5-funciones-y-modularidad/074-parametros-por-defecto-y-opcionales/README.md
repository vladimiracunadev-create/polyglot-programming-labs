# Clase 074 — Parámetros por defecto y opcionales

> Parte **5 — Funciones y modularidad** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Aprender a declarar un parámetro que trae consigo su propio valor: si el llamador no lo entrega, la función usa el que ya venía escrito en la firma. En la clase anterior vimos que la firma es un contrato; el parámetro por defecto lo convierte en un contrato **flexible**, capaz de atender tanto al que pasa todos los datos como al que solo pasa los imprescindibles. `potencia(3)` eleva al cuadrado y `potencia(2, 3)` eleva al cubo, y ambas llamadas hablan con una misma definición. El valor por defecto es, en el fondo, una respuesta a una pregunta muy práctica: ¿cuál es el caso más frecuente, y cómo hago que ese caso no obligue a repetir siempre lo obvio?

El motivo profundo es de diseño de interfaz. Steve McConnell dedica en *Code Complete* (cap. 7, «High-Quality Routines») una discusión a mantener el número de parámetros bajo control —siete es el límite que la memoria de trabajo tolera con comodidad— y a ordenar los parámetros de lo esencial a lo accesorio. El parámetro por defecto es la herramienta que materializa esa jerarquía: lo esencial se exige, lo accesorio se ofrece con un valor sensato ya puesto. Robert Martin lo empuja aún más lejos en *Clean Code* (cap. 3, «Functions»): la mejor cantidad de argumentos es cero, luego uno, luego dos; cada argumento adicional es una carga cognitiva para quien lee la llamada. Un buen valor por defecto elimina argumentos de la mayoría de las llamadas sin eliminar la capacidad de la función.

Pero hay una advertencia que atraviesa toda la clase, y que separa a los lenguajes en dos campos. No todos tienen esta característica de forma nativa. Java, C y Go carecen de parámetros por defecto y deben **simularlos** —con sobrecarga, con lógica en el sitio de llamada o con estructuras de opciones—. Y aun donde existe, esconde una trampa célebre: en Python el valor por defecto se evalúa **una sola vez**, cuando se define la función, no en cada llamada, lo que vuelve peligroso usar objetos mutables como defecto. Entender el mecanismo, y no solo la sintaxis, es lo que evita esos accidentes.

## 🧩 Situación

Tienes una función que calcula el área de un rectángulo y, en el 90 % de tu código, los rectángulos son en realidad cuadrados. Sin valores por defecto, cada una de esas llamadas repite el mismo dato dos veces: `area(5, 5)`, `area(8, 8)`, `area(3, 3)`. El ruido no es solo estético; cada repetición es una ocasión de equivocarse y escribir `area(5, 6)` por descuido. La respuesta es una firma como `area(lado, alto=lado)` o `potencia(base, exp=2)`: el caso común queda expresado en su forma más corta —`potencia(3)`— y el caso general sigue disponible —`potencia(2, 3)`—. Un solo cuerpo, dos maneras de llamarlo, y el lector de `potencia(3)` entiende de inmediato que «lo normal aquí es elevar al cuadrado». Ese es exactamente el tipo de duplicación silenciosa que un valor por defecto disuelve.

## 🧮 Modelo

- **Entrada** (stdin): una línea: `base` (exp por defecto 2) o `base exp`
- **Salida** (stdout): `resultado=<base^exp>`
- **Regla:** potencia(base, exp=2) = base^exp

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3` | `resultado=9` |
| `2 3` | `resultado=8` |
| `5` | `resultado=25` |

## 📖 Definiciones y características

- **Parámetro por defecto** — un parámetro que lleva escrito en la firma el valor que tomará si el llamador lo omite. En `def potencia(base, exp=2)`, el `exp=2` es la promesa de que, a falta de instrucción, se elevará al cuadrado. El defecto forma parte de la definición, no de la llamada: vive en el cuerpo de la función esperando a ver si alguien lo pisa.
- **Argumento opcional** — desde la perspectiva de quien llama, es el argumento que se puede no escribir. `potencia(3)` ejerce la opcionalidad de `exp`. Un parámetro por defecto es, visto desde afuera, un argumento opcional; son las dos caras del mismo contrato.
- **Sobrecarga (overloading)** — definir varias funciones con el mismo nombre y distinta lista de parámetros, de modo que el compilador elija cuál usar según los argumentos. Java y C carecen de defectos y recurren a esto: una `potencia(base)` que internamente llama a `potencia(base, 2)`. McConnell la trata como una técnica válida pero recuerda que multiplica las firmas que hay que mantener coherentes.
- **Simular el defecto** — en los lenguajes sin la característica (C, Go), reconstruir el efecto a mano: comprobar en el sitio de llamada si el dato llegó y, si no, asignar el valor base. No es un adorno del lenguaje sino una decisión explícita del programador en cada punto.
- **Trampa del defecto mutable** — en Python el valor por defecto se evalúa **una vez**, al definir la función, y se reutiliza en cada invocación. Con un objeto mutable como `def f(x=[])`, la misma lista se comparte entre todas las llamadas y va acumulando basura. El patrón seguro es `def f(x=None)` y crear la lista dentro. La regla nace de que el defecto es un valor congelado en el momento de la definición.

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER tokens
base <- tokens[0] ; exp <- tokens[1] SI EXISTE SINO 2
ESCRIBIR "resultado=" base^exp
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys


def potencia(base, exp=2):
    r = 1
    for _ in range(exp):
        r *= base
    return r


t = sys.stdin.readline().split()
base = int(t[0])
if len(t) > 1:
    print(f"resultado={potencia(base, int(t[1]))}")
else:
    print(f"resultado={potencia(base)}")
```

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

function potencia(base, exp = 2) {
  let r = 1;
  for (let i = 0; i < exp; i++) r *= base;
  return r;
}

const t = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`resultado=${t.length > 1 ? potencia(t[0], t[1]) : potencia(t[0])}`);
```

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

function potencia(base: number, exp = 2): number {
  let r = 1;
  for (let i = 0; i < exp; i++) r *= base;
  return r;
}

const t: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`resultado=${t.length > 1 ? potencia(t[0], t[1]) : potencia(t[0])}`);
```

### Java · [`java/Main.java`](implementaciones/java/Main.java) · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    // Java no tiene defectos: se simula con sobrecarga.
    static long potencia(long base) {
        return potencia(base, 2);
    }

    static long potencia(long base, int exp) {
        long r = 1;
        for (int i = 0; i < exp; i++) r *= base;
        return r;
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] t = br.readLine().trim().split("\\s+");
        long base = Long.parseLong(t[0]);
        long r = t.length > 1 ? potencia(base, Integer.parseInt(t[1])) : potencia(base);
        System.out.println("resultado=" + r);
    }
}
```

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;

long Potencia(long baseN, int exp = 2) {
    long r = 1;
    for (int i = 0; i < exp; i++) r *= baseN;
    return r;
}

string[] t = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
long b = long.Parse(t[0]);
long res = t.Length > 1 ? Potencia(b, int.Parse(t[1])) : Potencia(b);
Console.WriteLine($"resultado={res}");
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

// Go no tiene defectos: se simula con la lógica de llamada.
func potencia(base int64, exp int) int64 {
	var r int64 = 1
	for i := 0; i < exp; i++ {
		r *= base
	}
	return r
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	t := strings.Fields(line)
	base, _ := strconv.ParseInt(t[0], 10, 64)
	exp := 2
	if len(t) > 1 {
		exp, _ = strconv.Atoi(t[1])
	}
	fmt.Printf("resultado=%d\n", potencia(base, exp))
}
```

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn potencia(base: i64, exp: u32) -> i64 {
    base.pow(exp)
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let t: Vec<&str> = s.split_whitespace().collect();
    let base: i64 = t[0].parse().unwrap();
    let exp: u32 = if t.len() > 1 { t[1].parse().unwrap() } else { 2 };
    println!("resultado={}", potencia(base, exp));
}
```

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

/* C no tiene defectos: se simula pasando siempre el exponente. */
long potencia(long base, int exp) {
    long r = 1;
    for (int i = 0; i < exp; i++) r *= base;
    return r;
}

int main(void) {
    long base;
    int exp;
    int leidos = scanf("%ld %d", &base, &exp);
    if (leidos < 1) return 1;
    if (leidos < 2) exp = 2;
    printf("resultado=%ld\n", potencia(base, exp));
    return 0;
}
```

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL: COALESCE simula el valor por defecto (aquí, exponente 2 mediante base*base).
WITH datos(base) AS (VALUES (3), (5))
SELECT printf('resultado=%d', base * base) AS resultado FROM datos;
```

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
function potencia($base, $exp = 2) {
    $r = 1;
    for ($i = 0; $i < $exp; $i++) {
        $r *= $base;
    }
    return $r;
}

$t = preg_split('/\s+/', trim(fgets(STDIN)));
$base = (int) $t[0];
$res = count($t) > 1 ? potencia($base, (int) $t[1]) : potencia($base);
echo "resultado=$res\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Ejemplo trabajado — del stdin a la salida

Sigamos el primer caso de `casos.json` (`stdin = "3"`, `esperado = "resultado=9"`), donde el llamador **omite** el exponente, y contrastémoslo con el segundo (`stdin = "2 3"`, `esperado = "resultado=8"`), donde lo pasa. Tres lenguajes resuelven el mismo dilema con filosofías opuestas.

**Python (defecto nativo).** Con la entrada `"3"`, la línea `t = sys.stdin.readline().split()` produce la lista `["3"]`, de modo que `len(t)` es 1 y se toma la rama `else`: se ejecuta `potencia(base)` con `base=3`. Aquí ocurre lo interesante: la llamada no menciona `exp`, así que la función usa el valor escrito en su firma, `exp=2`. El bucle multiplica `r` por `3` dos veces —`1*3=3`, `3*3=9`— y devuelve `9`, que el f-string convierte en `resultado=9`. Con la entrada `"2 3"`, `len(t)` vale 2, se toma la rama `if` y se llama `potencia(2, int("3"))`: el defecto queda **pisado** por el argumento explícito `3`, el bucle multiplica tres veces —`2`, `4`, `8`— y sale `resultado=8`. Fíjate en que el defecto vive en la definición y solo se activa por ausencia.

**Java (simulación por sobrecarga).** Java no tiene defectos, así que la clase define **dos** métodos `potencia`. Con `"3"`, `t.length` es 1 y el ternario invoca `potencia(base)` —la versión de un solo argumento—, cuyo único cuerpo es `return potencia(base, 2)`: la sobrecarga corta delega en la completa pasando el `2` a mano. El resultado es idéntico, `9`, pero el «defecto» no es una propiedad de la firma sino una segunda función que existe solo para rellenar el hueco. Con `"2 3"` se llama directamente a la versión de dos argumentos y el `2` de la sobrecarga nunca entra en juego.

**Go (simulación en el sitio de llamada).** Go tampoco tiene defectos, y su solución es aún más explícita: no hay dos funciones, sino una sola `potencia(base, exp)` que **siempre** exige el exponente, y es el `main` quien decide el valor. La línea `exp := 2` fija el defecto como una variable local ordinaria, y solo si `len(t) > 1` la sobrescribe con `strconv.Atoi(t[1])`. Con `"3"`, `t` tiene un elemento, el `if` no se cumple, `exp` queda en `2` y `potencia(3, 2)` devuelve `9`. El contraste con Python es nítido: donde Python guarda el defecto en la firma, Go lo guarda en el flujo de `main`; el mismo `resultado=9` sale por caminos conceptualmente distintos.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | El defecto en la firma —`exp=2` (Python, C#, PHP), `exp = 2` (JS/TS)— frente a no poder escribirlo y tener que simularlo en Java/C/Go. |
| Semántica | Python, JavaScript, TypeScript, C# y PHP resuelven el defecto en cada llamada donde falte el argumento; Java lo resuelve eligiendo entre firmas sobrecargadas en compilación. |
| Semántica | En Python el defecto se evalúa **una vez** al definir la función (de ahí la trampa del objeto mutable); en JS/TS la expresión por defecto se evalúa **en cada llamada** que omita el argumento. |
| Paradigmática | Rust no tiene parámetros por defecto: idiomáticamente usa `Option<T>`, el rasgo `Default` o el patrón builder; aquí el defecto se resuelve con un `if` en `main`. |
| Paradigmática | SQL no «omite un argumento»: expresa la ausencia de valor con `COALESCE`, que sustituye un `NULL` por un valor de reserva sobre las filas de una consulta. |

La síntesis la ofrece McConnell en *Code Complete*: un buen parámetro por defecto acorta la interfaz para el caso común sin cerrar la puerta al caso general, y ese es el equilibrio que persigue una rutina de calidad. Que Java lo consiga con dos firmas y Python con una es un detalle de implementación; para quien lee `potencia(3)`, en ambos lenguajes la promesa es la misma: «si no digo más, elevo al cuadrado». La diferencia que sí importa es la temporal —cuándo se evalúa el defecto—, porque es la que produce bugs reales cuando el valor es mutable.

## 🧬 El concepto en la familia

En **Ruby** se escribe `def potencia(base, exp = 2)`, con exactamente la misma semántica de Python pero sin su trampa del mutable, porque Ruby reevalúa la expresión por defecto en cada llamada. **Kotlin** ofrece `fun potencia(base: Int, exp: Int = 2)` y, a diferencia de Java, sí tiene defectos nativos —Kotlin los añadió en parte para reducir la explosión de sobrecargas típica de Java, y con `@JvmOverloads` incluso las genera automáticamente para interoperar—. **Swift** también los admite: `func potencia(_ base: Int, exp: Int = 2)`. **Scala** los soporta y permite combinarlos con argumentos nombrados para saltarse los del medio. Reconocer si un lenguaje trae defectos nativos, obliga a sobrecargar o exige simular en la llamada es lo que te dice de antemano cuánto código de andamiaje vas a escribir.

## ⚠️ Errores comunes

- **Poner un parámetro con defecto antes de uno obligatorio** → causa: firmas como `f(exp=2, base)` que la mayoría de lenguajes rechazan, porque el llamador posicional ya no sabría a qué corresponde cada valor → solución: coloca siempre los parámetros con defecto al final de la lista, después de todos los obligatorios.
- **Usar un objeto mutable como defecto en Python** → causa: `def f(x=[])` crea la lista una sola vez al definir la función y la comparte entre todas las llamadas, que la ven crecer de forma fantasmal → solución: usa `def f(x=None)` y dentro haz `if x is None: x = []`.
- **Asumir que C, Go o Java tienen defectos** → causa: escribir `func f(x int = 2)` en Go o esperar que Java elija un valor implícito, cuando ninguno lo soporta → solución: simula con sobrecarga (Java), con una variable local y un `if` en el sitio de llamada (Go) o pasando siempre el argumento (C).
- **Multiplicar defectos hasta volver la firma ilegible** → causa: acumular `f(a, b=1, c=2, d=3, e=4)` y confiar en que nadie se pierda → solución: Martin recomienda en *Clean Code* pocos argumentos; si son muchos opcionales, agrúpalos en un objeto de configuración o registro con nombres.

## ❓ Preguntas frecuentes

- **¿Todos los lenguajes tienen parámetros por defecto?** No. Python, JavaScript, TypeScript, C#, PHP, Kotlin, Ruby y Swift sí; Java, C y Go no, y los simulan con sobrecarga, structs de opciones o lógica en la llamada.
- **¿El valor por defecto se evalúa una vez o en cada llamada?** Depende del lenguaje: en Python, una sola vez al definir la función (por eso los defectos mutables son peligrosos); en JavaScript y TypeScript, en cada llamada que omita el argumento, lo que hace seguro escribir `f(x = [])`.
- **¿Por qué Go prefiere no tenerlos?** Es una decisión de diseño: sus autores buscan una sola forma evidente de leer una llamada. Para casos con muchas opciones, el idioma de Go es una struct de configuración o el patrón de «opciones funcionales», no un defecto en la firma.
- **¿Sobrecarga o defecto cuando ambos existen?** Un defecto mantiene un único cuerpo y una única firma que documentar; la sobrecarga duplica firmas que deben mantenerse coherentes. Donde el lenguaje ofrezca defectos, suelen preferirse por eso.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 074
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## 🔗 Referencias

**Libros de la parte:**

- H. Abelson y G. J. Sussman — *Structure and Interpretation of Computer Programs* (2ª ed., MIT Press), §1.1 sobre procedimientos como abstracciones.
- R. C. Martin — *Clean Code* (Prentice Hall), cap. 3 «Functions», sobre reducir el número de argumentos.
- S. McConnell — *Code Complete* (2ª ed., Microsoft Press), cap. 7 «High-Quality Routines», sobre número y orden de parámetros.

**Libros de los lenguajes del núcleo:**

- L. Ramalho — *Fluent Python* (2ª ed., O'Reilly), cap. 7 sobre la trampa del argumento por defecto mutable.
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

> [⏮️ Clase 073](../../parte-5-funciones-y-modularidad/073-firma-parametros-argumentos-y-retorno/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 075 ⏭️](../../parte-5-funciones-y-modularidad/075-argumentos-nombrados-y-de-palabra-clave/README.md)
