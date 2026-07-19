# Clase 075 — Argumentos nombrados y de palabra clave

> Parte **5 — Funciones y modularidad** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Aprender a pasar los argumentos diciendo **a qué parámetro corresponde cada uno**, en lugar de confiar en el orden en que van escritos. En la clase 073 vimos que en una llamada posicional «el orden es el significado»: `restar(a, b)` no es `restar(b, a)`. El argumento nombrado rompe esa dependencia. Escribir `punto(x=3, y=4)` deja explícito que el `3` es la abscisa y el `4` la ordenada, y de paso permite reordenarlos —`punto(y=4, x=3)` significa lo mismo—. Lo que se gana no es potencia de cálculo sino claridad en el punto exacto donde más se necesita: la línea que invoca la función, que es la que un futuro lector encuentra sin ver la firma.

El motivo profundo es de legibilidad, y Robert Martin lo pone en el centro de *Clean Code* (cap. 3, «Functions»): los argumentos que más confunden son los que no dicen nada por sí mismos en la llamada. Su ejemplo clásico es el argumento booleano suelto —`render(true)`, ¿qué es `true`?— que obliga a saltar a la definición para descifrarlo. El argumento nombrado ataca ese problema de raíz: `crear(ancho=800, alto=600)` no necesita comentario ni memoria; la llamada se documenta a sí misma. Cuando una función tiene varios parámetros del mismo tipo —dos enteros, dos cadenas—, nombrarlos es la diferencia entre una llamada que se lee y una que se adivina.

Como en la clase anterior, el reparto entre lenguajes es desigual y conviene tenerlo claro desde el principio. Python y C# los soportan de forma nativa; PHP los añadió en su versión 8; Kotlin, Ruby y Swift los tienen. Pero Java, Go, C y Rust **no** ofrecen argumentos nombrados en la firma, y cada uno recurre a un sustituto: Java se queda con el orden posicional, Go y Rust usan structs con campos nombrados, y en JavaScript el idioma equivalente —tan extendido que se siente nativo— es pasar un único objeto de opciones cuyas claves hacen las veces de nombres.

## 🧩 Situación

Imagina una función que crea una ventana: `crear(800, 600, true, false)`. En la llamada, esos cuatro valores son un jeroglífico. ¿Es `800` el ancho o el alto? ¿Qué activa el primer `true`? Quien lee esta línea en una revisión de código no tiene forma de saberlo sin abrir la definición, y ahí es donde se cuelan los bugs: alguien escribe `crear(600, 800, ...)` con las dimensiones invertidas y el programa compila tan feliz porque ambos son enteros. Con argumentos nombrados la misma llamada se vuelve `crear(ancho=800, alto=600, visible=true, modal=false)` y el jeroglífico desaparece: cada valor lleva pegada su intención. Es la clase de claridad que no cuesta nada en tiempo de ejecución y ahorra horas de depuración. En esta clase practicamos la versión mínima de esa idea, construyendo `punto(x=a, y=b)`, dos parámetros del mismo tipo donde nombrar es exactamente lo que evita confundir la abscisa con la ordenada.

## 🧮 Modelo

- **Entrada** (stdin): una línea `a b` (dos enteros: x, y)
- **Salida** (stdout): `punto(x=<a>, y=<b>)`
- **Regla:** punto(x=a, y=b)

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3 4` | `punto(x=3, y=4)` |
| `0 -2` | `punto(x=0, y=-2)` |
| `5 5` | `punto(x=5, y=5)` |

## 📖 Definiciones y características

- **Argumento nombrado (de palabra clave)** — el que se pasa indicando explícitamente el parámetro al que va destinado, como `y=4`. La llamada deja de ser una secuencia posicional para volverse un conjunto de asociaciones nombre-valor. Su virtud es doble: legibilidad en la llamada y libertad de orden.
- **Argumento posicional** — el que se entrega por su lugar en la lista, sin nombre, y cuyo significado depende enteramente de en qué posición cae. Es el modo por defecto en todos los lenguajes; el nombrado es una capa opcional encima.
- **Palabra clave (keyword)** — el propio nombre del parámetro usado en la llamada. En Python es la base de un mecanismo más amplio: `**kwargs` recoge en un diccionario todos los argumentos nombrados que no correspondan a un parámetro declarado, permitiendo funciones que aceptan opciones arbitrarias.
- **Legibilidad de la llamada** — la propiedad de entender qué hace una invocación sin necesidad de consultar la firma de la función. Es el criterio que Martin persigue en *Clean Code*: el código se lee muchas más veces de las que se escribe, y el argumento nombrado paga ese peaje una sola vez, al escribirlo.
- **Objeto de opciones** — el sustituto idiomático en lenguajes sin argumentos nombrados, sobre todo JavaScript: se pasa un único objeto `{ x: a, y: b }` y sus claves cumplen el papel de los nombres. Go y Rust hacen lo análogo con structs de campos nombrados.

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER a, b
ESCRIBIR punto(x=a, y=b)
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys


def punto(x, y):
    return f"punto(x={x}, y={y})"


a, b = map(int, sys.stdin.readline().split())
print(punto(x=a, y=b))
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

// JS simula argumentos nombrados con un objeto.
function punto({ x, y }) {
  return `punto(x=${x}, y=${y})`;
}

const [a, b] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(punto({ x: a, y: b }));
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

function punto({ x, y }: { x: number; y: number }): string {
  return `punto(x=${x}, y=${y})`;
}

const [a, b]: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(punto({ x: a, y: b }));
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    // Java no tiene argumentos nombrados: se pasan por posición.
    static String punto(int x, int y) {
        return "punto(x=" + x + ", y=" + y + ")";
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        System.out.println(punto(Integer.parseInt(p[0]), Integer.parseInt(p[1])));
    }
}
```

### C# · `dotnet run`

```csharp
using System;

string Punto(int x, int y) => $"punto(x={x}, y={y})";

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
Console.WriteLine(Punto(x: int.Parse(p[0]), y: int.Parse(p[1])));
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

// Go no tiene argumentos nombrados: se usan structs con campos nombrados.
type Punto struct {
	X, Y int
}

func (p Punto) String() string {
	return fmt.Sprintf("punto(x=%d, y=%d)", p.X, p.Y)
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	f := strings.Fields(line)
	a, _ := strconv.Atoi(f[0])
	b, _ := strconv.Atoi(f[1])
	fmt.Println(Punto{X: a, Y: b})
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn punto(x: i64, y: i64) -> String {
    format!("punto(x={x}, y={y})")
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let v: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    println!("{}", punto(v[0], v[1]));
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long a, b;
    if (scanf("%ld %ld", &a, &b) != 2) return 1;
    /* C no tiene argumentos nombrados: posicionales. */
    printf("punto(x=%ld, y=%ld)\n", a, b);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL nombra columnas, análogo a nombrar argumentos.
WITH puntos(x, y) AS (VALUES (3, 4), (0, -2), (5, 5))
SELECT printf('punto(x=%d, y=%d)', x, y) AS resultado FROM puntos;
```

### PHP · `php main.php`

```php
<?php
function punto($x, $y) {
    return "punto(x=$x, y=$y)";
}

[$a, $b] = preg_split('/\s+/', trim(fgets(STDIN)));
// PHP 8 admite argumentos nombrados.
echo punto(x: (int) $a, y: (int) $b) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Ejemplo trabajado — del stdin a la salida

Sigamos el primer caso de `casos.json` (`stdin = "3 4"`, `esperado = "punto(x=3, y=4)"`) a través de tres lenguajes que resuelven de forma muy distinta el problema de «etiquetar» cada valor.

**Python (nombrado nativo).** La línea `a, b = map(int, sys.stdin.readline().split())` lee `"3 4"`, lo parte en `["3", "4"]`, lo convierte a enteros y desempaqueta `a=3`, `b=4`. Entonces la llamada `punto(x=a, y=b)` es la clave de la clase: no pasa `a` y `b` por posición, sino nombrando los parámetros de destino. El intérprete empareja `x` con el valor de `a` (que es `3`) y `y` con el de `b` (que es `4`), ejecuta el f-string `f"punto(x={x}, y={y})"` y produce `punto(x=3, y=4)`. Como el emparejamiento es por nombre, `punto(y=b, x=a)` daría exactamente el mismo resultado: el orden en la llamada ya no manda.

**Go (struct con campos nombrados).** Go no tiene argumentos nombrados, y su sustituto es de otra naturaleza: en vez de nombrar en la llamada a una función, se define un tipo `Punto struct { X, Y int }` y se construye con un literal cuyos campos sí llevan nombre. Tras parsear `a=3, b=4`, la línea `fmt.Println(Punto{X: a, Y: b})` crea el valor con `X: 3` y `Y: 4`. El método `String()` definido sobre `Punto` es lo que `fmt.Println` invoca en silencio para obtener el texto `punto(x=3, y=4)`. La claridad se logra, pero se ha desplazado del sitio de llamada al literal de struct: son los campos `X:` e `Y:`, no unos parámetros, los que llevan el nombre.

**JavaScript (objeto de opciones).** JavaScript tampoco tiene argumentos nombrados, pero su idioma es tan común que casi no se nota: la función se declara como `function punto({ x, y })`, desestructurando un objeto en el propio parámetro. Tras leer `a=3, b=4`, la llamada `punto({ x: a, y: b })` pasa un único objeto `{ x: 3, y: 4 }`; la desestructuración `{ x, y }` extrae sus claves en variables locales y el template string produce `punto(x=3, y=4)`. Como las claves del objeto no dependen del orden, `punto({ y: b, x: a })` sería equivalente —el objeto emula justamente la libertad de orden que Python obtiene con nombres reales—.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Nombre directo en la llamada —`punto(x=a, y=b)` (Python), `Punto(x: ..., y: ...)` (C#), `punto(x: ..., y: ...)` (PHP 8)— frente a posicional puro (Java, C, Rust) o literal de struct/objeto (Go, JS). |
| Semántica | Con nombres, el orden de los argumentos es libre y el emparejamiento es por identidad; sin ellos, la posición **es** el significado y equivocar el orden compila sin queja cuando los tipos coinciden. |
| Semántica | Python distingue además el paso de una struct/objeto (un solo valor con campos) del paso por palabra clave (varios argumentos etiquetados); Go y JS solo tienen la primera vía, y por eso «nombran el dato», no «nombran el argumento». |
| Paradigmática | Rust no tiene argumentos nombrados; el idioma es un struct con campos nombrados, a menudo construido con el patrón builder cuando hay muchas opciones. |
| Paradigmática | SQL nombra columnas por naturaleza: `SELECT ... x, y` etiqueta cada dato de la fila, un paralelo declarativo de nombrar argumentos. |

La síntesis vuelve a *Clean Code*: el valor del argumento nombrado no está en la máquina —al procesador le da igual— sino en el ser humano que lee la llamada meses después. Que Python lo consiga con palabras clave reales y JavaScript con un objeto de opciones es, para ese lector, casi lo mismo: en ambos casos cada valor llega con su etiqueta puesta. La diferencia práctica aparece cuando hay muchos parámetros opcionales del mismo tipo; ahí el lenguaje que obliga a posición pura (Java, C) es el que más se beneficiaría de nombres y el que, careciendo de ellos, empuja hacia objetos y structs contenedores.

## 🧬 El concepto en la familia

En **Ruby** los argumentos de palabra clave son de primera clase: `def punto(x:, y:)` los declara y `punto(x: a, y: b)` los pasa, con orden libre y hasta obligatorios si se quiere. **Kotlin** permite `punto(x = a, y = b)` y combina los nombres con los defectos de la clase 074 para saltarse argumentos intermedios sin ambigüedad. **Swift** lleva las etiquetas al extremo: por defecto **exige** el nombre en la llamada —`punto(x: a, y: b)`— salvo que el diseñador lo suprima con `_`, de modo que la legibilidad es la norma y no la excepción. **Scala** también los soporta y, como Kotlin, los mezcla con parámetros por defecto. Saber si un lenguaje trae nombres nativos, los exige o te obliga a un objeto contenedor te dice cuánta ceremonia necesitarás para que una llamada con muchos parámetros siga siendo legible.

## ⚠️ Errores comunes

- **Confiar en el orden con parámetros parecidos** → causa: llamar `punto(b, a)` con la abscisa y la ordenada invertidas; como ambas son enteras, compila y a veces «funciona» por casualidad con datos simétricos como `5 5` → solución: usa argumentos nombrados donde el lenguaje los ofrezca, o structs/objetos con campos nombrados donde no.
- **Asumir nombres en Java, Go, C o Rust** → causa: escribir `punto(x: 3, y: 4)` esperando que el compilador los acepte, cuando esos lenguajes no los tienen en la firma → solución: pasa por posición (Java, C), o modela los datos con una struct/record de campos nombrados (Go, Rust).
- **Mezclar posicionales y nombrados en mal orden** → causa: en Python o C#, poner un argumento posicional después de uno nombrado —`punto(x=3, 4)`— provoca un error de sintaxis → solución: primero todos los posicionales, luego todos los nombrados.
- **Repetir un argumento por nombre y por posición** → causa: `punto(3, x=5)` asigna `x` dos veces y el intérprete lo rechaza → solución: pasa cada parámetro una sola vez, o por posición o por nombre, nunca ambas.

## ❓ Preguntas frecuentes

- **¿Qué lenguajes tienen argumentos nombrados nativos?** Python, C#, PHP 8+, Kotlin, Ruby, Swift y Scala. Java, Go, C y Rust no los tienen en la firma; se recurre a structs, objetos o al orden posicional.
- **¿Y si el lenguaje no los tiene?** Se usa el sustituto idiomático: en JavaScript un objeto de opciones `{ x, y }`, en Go y Rust una struct con campos nombrados, en Java a menudo un patrón builder cuando hay muchos parámetros.
- **¿Los argumentos nombrados cambian el rendimiento?** No en la práctica: son una comodidad de la llamada que el compilador o intérprete resuelve al emparejar; el código resultante es equivalente al posicional.
- **¿Qué es `**kwargs` en Python?** Es un parámetro que recoge en un diccionario todos los argumentos nombrados que no correspondan a un parámetro declarado; sirve para funciones que aceptan un conjunto abierto de opciones, no solo para nombrar las ya previstas.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 075
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## 🔗 Referencias

**Libros de la parte:**

- H. Abelson y G. J. Sussman — *Structure and Interpretation of Computer Programs* (2ª ed., MIT Press), §1.1 sobre nombres y abstracción.
- R. C. Martin — *Clean Code* (Prentice Hall), cap. 3 «Functions», sobre la legibilidad de la llamada y los argumentos «bandera».
- S. McConnell — *Code Complete* (2ª ed., Microsoft Press), cap. 7 «High-Quality Routines».

**Libros de los lenguajes del núcleo:**

- L. Ramalho — *Fluent Python* (2ª ed., O'Reilly), cap. 7 sobre argumentos de palabra clave y `**kwargs`.
- M. Haverbeke — *Eloquent JavaScript* (3ª ed.) — [gratis online](https://eloquentjavascript.net/).
- B. Cherny — *Programming TypeScript* (O'Reilly).
- J. Bloch — *Effective Java* (3ª ed., Addison-Wesley), sobre el patrón builder ante muchos parámetros.
- J. Skeet — *C# in Depth* (4ª ed., Manning).
- A. Donovan y B. Kernighan — *The Go Programming Language* (Addison-Wesley).
- S. Klabnik y C. Nichols — *The Rust Programming Language* — [gratis online](https://doc.rust-lang.org/book/).
- B. Kernighan y D. Ritchie — *The C Programming Language* (2ª ed., Prentice Hall).
- C. J. Date — *SQL and Relational Theory* (3ª ed., O'Reilly).
- J. Lockhart — *Modern PHP* (O'Reilly).

---

> [⏮️ Clase 074](../../parte-5-funciones-y-modularidad/074-parametros-por-defecto-y-opcionales/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 076 ⏭️](../../parte-5-funciones-y-modularidad/076-parametros-variadicos/README.md)
