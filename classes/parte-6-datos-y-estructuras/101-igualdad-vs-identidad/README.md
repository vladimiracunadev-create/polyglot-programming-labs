# Clase 101 — Igualdad vs. identidad

> Parte **6 — Datos y estructuras** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Distinguir **igualdad** (mismo valor) de **identidad** (mismo objeto en memoria). Son dos preguntas diferentes que la sintaxis suele disfrazar con el mismo símbolo. «¿Estos dos billetes de veinte valen lo mismo?» es igualdad; «¿son el mismo billete?» es identidad. Con enteros y otros valores primitivos las dos preguntas dan siempre la misma respuesta —un `5` es indistinguible de otro `5`, no tiene sentido preguntar cuál de los dos es—, y por eso el ejercicio de hoy, que compara dos enteros, sale idéntico en los diez lenguajes. Con objetos la coincidencia se rompe: dos listas con el mismo contenido son iguales pero no idénticas, y decidir cuál de las dos preguntas quiere responder tu código es la diferencia entre un programa correcto y uno con un bug intermitente. La distinción viene de la clase 099: un tipo con **semántica de valor** casi no admite la pregunta de identidad; uno con **semántica de referencia** la exige. Bloch dedica a esto uno de los ítems más citados de *Effective Java* —el contrato de `equals` y `hashCode`—, porque la igualdad no es un detalle sintáctico sino una **relación de equivalencia** que el programador define y de la que dependen los mapas y los conjuntos de las clases 094 y 095.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Comparar por valor.
2. Explicar la diferencia entre igualdad e identidad.
3. Reconocer los operadores de cada lenguaje.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Igualdad | Mismo valor |
| 2 | Identidad | Mismo objeto en memoria |
| 3 | Operadores | ==, is, ===, equals |

## 📖 Definiciones y características

La **igualdad** es una afirmación sobre el *contenido*: dos valores son iguales si representan la misma información. Para que esa afirmación sea utilizable, debe comportarse como una **relación de equivalencia** en el sentido matemático: **reflexiva** (`a == a`), **simétrica** (si `a == b` entonces `b == a`) y **transitiva** (si `a == b` y `b == c`, entonces `a == c`). No es pedantería. Cormen y Sedgewick construyen sus estructuras de búsqueda sobre esa garantía: una tabla hash localiza una entrada calculando el hash de la clave y luego comparando por igualdad dentro del cubo, de modo que si tu `equals` no es simétrico o tu `hashCode` no es coherente con él, el mapa «pierde» entradas que sí insertaste. De ahí la regla que Bloch enuncia en *Effective Java*: **si redefines `equals`, debes redefinir `hashCode`**, porque dos objetos iguales están obligados a producir el mismo hash. El coste de comparar depende del tipo: para un entero es O(1) —una instrucción de la CPU—, para una cadena o una lista es O(n) en el peor caso, aunque en la práctica un cortocircuito por longitud distinta suele resolverlo antes.

La **identidad** es una afirmación sobre la *ubicación*: dos referencias son idénticas si apuntan al mismo objeto en memoria. Es siempre O(1), porque solo compara dos direcciones. La identidad implica la igualdad —el mismo objeto trivialmente vale lo mismo que él mismo—, pero no al revés. Su utilidad real es reducida y muy concreta: comprobar contra un centinela (`x is None` en Python), detectar aliasing antes de copiar, o cortocircuitar una comparación cara. Un ejemplo que confunde a casi todo el mundo la primera vez: CPython **internaliza** los enteros pequeños (de −5 a 256) y muchas cadenas literales, de modo que `a is b` puede dar `True` para dos `5` calculados por separado y `False` para dos `1000`; Ramalho lo explica en *Fluent Python* insistiendo en que esa optimización de la implementación nunca debe usarse como si fuera semántica del lenguaje.

- **Igualdad (`==`, `equals`, `Equals`, `eq`)** — comparación por contenido. Debe ser reflexiva, simétrica y transitiva, y mantenerse coherente con la función hash. En Rust la formaliza el rasgo `PartialEq`; el prefijo *Partial* delata que los flotantes no son plenamente reflexivos, porque `NaN != NaN` por mandato del estándar IEEE 754.
- **Identidad (`is` en Python, `ReferenceEquals` en C#, `==` sobre objetos en Java, `equal?` en Ruby)** — comparación de direcciones. O(1) siempre; solo tiene sentido con tipos de referencia.
- **`equals` frente a `==` en Java** — `==` sobre dos variables de tipo objeto compara *referencias*; `equals` compara *contenido*. Es la trampa más famosa del lenguaje y la razón por la que `s1 == s2` con dos cadenas de igual texto puede dar `false`.

## 🧩 Situación

El caso clásico ocurre en Java con cadenas. Escribe `String a = "hola"; String b = "hola";` y `a == b` da `true`, porque el compilador coloca ambos literales en el *pool* de cadenas y las dos variables acaban apuntando al mismo objeto. Cambia una línea a `String b = new String("hola")` —o construye el texto leyéndolo de la entrada, como hace cualquier programa real— y de pronto `a == b` da `false` mientras `a.equals(b)` sigue dando `true`. El programa funcionaba con datos literales de prueba y falla con datos de producción: un bug que se esconde justamente donde nadie lo busca. JavaScript ofrece la trampa complementaria: `==` aplica **coerción de tipos** —`0 == "0"` es `true`, `null == undefined` es `true`— y `===` compara sin convertir, motivo por el que Haverbeke recomienda en *Eloquent JavaScript* usar `===` por defecto. Ojo con el falso amigo: el `===` de JavaScript **no** es identidad, es igualdad estricta sin conversión; comparar dos arreglos distintos con `===` da `false` no porque compare direcciones a propósito, sino porque los objetos de JavaScript se comparan por referencia y no existe operador nativo de igualdad estructural. El ejercicio de hoy compara dos enteros a propósito: sobre primitivos, todas estas distinciones se colapsan en una sola respuesta, y eso deja ver con nitidez dónde empiezan realmente los problemas.

## 🧮 Modelo

- **Entrada** (stdin): una línea `a b` (dos enteros)
- **Salida** (stdout): `iguales=<true|false>`
- **Regla:** iguales = (a == b)

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5 5` | `iguales=true` |
| `3 7` | `iguales=false` |
| `0 0` | `iguales=true` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER a, b ; ESCRIBIR iguales=(a==b)
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys

a, b = map(int, sys.stdin.readline().split())
print(f"iguales={'true' if a == b else 'false'}")
```

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const [a, b] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`iguales=${a === b ? "true" : "false"}`);
```

🧬 **El mismo programa en la familia JavaScript / web:** [Dart · ActionScript](primos.md#javascript-web)

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const [a, b]: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`iguales=${a === b ? "true" : "false"}`);
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
        System.out.println("iguales=" + (a == b ? "true" : "false"));
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
Console.WriteLine($"iguales={(a == b ? "true" : "false")}");
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
	res := "false"
	if a == b {
		res = "true"
	}
	fmt.Printf("iguales=%s\n", res)
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
    let res = if v[0] == v[1] { "true" } else { "false" };
    println!("iguales={res}");
}
```

🧬 **El mismo programa en la familia Sistemas:** [Zig · Nim · D](primos.md#sistemas)

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long a, b;
    if (scanf("%ld %ld", &a, &b) != 2) return 1;
    printf("iguales=%s\n", a == b ? "true" : "false");
    return 0;
}
```

🧬 **El mismo programa en la familia C / llaves:** [C++ · Objective-C](primos.md#c-llaves)

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL: compara valores con =.
WITH pares(a, b) AS (VALUES (5, 5), (3, 7), (0, 0))
SELECT printf('iguales=%s', CASE WHEN a = b THEN 'true' ELSE 'false' END) AS resultado FROM pares;
```

🧬 **El mismo programa en la familia Lógica y declarativa:** [Prolog · Datalog](primos.md#logica-declarativa)

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
[$a, $b] = preg_split('/\s+/', trim(fgets(STDIN)));
echo "iguales=" . ((int) $a === (int) $b ? "true" : "false") . "\n";
```

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🧪 Laboratorio guiado: del código a la salida

Sigamos el caso `5 5`, que debe producir `iguales=true`, y el caso `3 7`, que debe producir `iguales=false`.

En **Python**, `a, b = map(int, sys.stdin.readline().split())` convierte los dos tokens en enteros y `a == b` compara sus valores. Con `5 5` la comparación da `True` y la expresión condicional produce la cadena `true`. Merece la pena detenerse aquí: si el código hubiera escrito `a is b`, con `5 5` también habría dado `True` —porque CPython reutiliza el objeto del entero 5—, pero con una entrada como `1000 1000` habría dado `False`, y el programa fallaría solo para números grandes. Ese es el bug de identidad en estado puro: pasa los tests pequeños y revienta con datos reales.

En **Java**, `int a = Integer.parseInt(p[0])` produce un **primitivo**, no un objeto, y sobre primitivos `==` compara valores sin ambigüedad: `a == b` es correcto aquí. Pero si el código usara `Integer` en lugar de `int`, la comparación pasaría a ser de referencias y volvería la trampa del *autoboxing*: la caché de `Integer` cubre de −128 a 127, de modo que `Integer.valueOf(5) == Integer.valueOf(5)` da `true` y `Integer.valueOf(1000) == Integer.valueOf(1000)` da `false`. Bloch usa exactamente este ejemplo en *Effective Java* para desaconsejar los tipos envoltorio cuando basta con un primitivo.

En **PHP**, la implementación escribe `(int) $a === (int) $b`. Las dos partes importan. Los casts a `int` son necesarios porque `preg_split` devuelve *cadenas*, y `===` en PHP exige que coincidan valor **y** tipo: sin los casts, `"5" === "5"` sería cierto por casualidad pero `" 5" === "5"` no, y comparar la cadena `"5"` con el entero `5` daría `false`. El operador laxo `==` de PHP hace conversiones tan liberales que en versiones anteriores a PHP 8 llegaba a considerar iguales una cadena no numérica y el número cero; Lockhart insiste en *Modern PHP* en preferir siempre la comparación estricta.

En **SQL** la lógica cambia de forma: `CASE WHEN a = b THEN 'true' ELSE 'false' END` compara valores, pero SQL tiene un tercer resultado posible que no existe en los demás lenguajes. Si `a` o `b` fueran `NULL`, la expresión `a = b` no daría ni verdadero ni falso, sino **desconocido**, y el `CASE` caería por el `ELSE`. Por eso SQL necesita `IS NULL` e `IS NOT DISTINCT FROM`: son los operadores que sí responden sí o no con nulos de por medio. Date dedica en *SQL and Relational Theory* una crítica extensa a esta lógica de tres valores.

Los diez imprimen `iguales=true` para `5 5`; el verificador comprueba que la salida coincide carácter a carácter con lo que dicta `casos.json`.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `==` en todos para valor; identidad con `is` (Python), `===` (JS), `equals`/`==` (Java). |
| Semántica | Con primitivos, igualdad e identidad coinciden; con objetos no. |
| Paradigmática | SQL compara valores con `=`; NULL requiere `IS`. |

El primer eje de diferencia es **cuántos operadores de comparación tiene el lenguaje y qué significa cada uno**, y aquí el mismo símbolo engaña. En Python, `==` es igualdad estructural (delegada al método `__eq__`) e `is` es identidad; son dos operadores para dos preguntas, un diseño limpio. En JavaScript hay también dos, pero parten el espacio por otro sitio: `==` es igualdad **con coerción** y `===` es igualdad **estricta**; ninguno de los dos es identidad, aunque sobre objetos `===` acabe comportándose como tal porque los objetos se comparan por referencia. En Java hay un operador y un método: `==` es valor sobre primitivos e identidad sobre objetos —la misma sintaxis con dos semánticas según el tipo, lo que la vuelve traicionera— y `equals` es contenido. C# se parece a Java pero permite **sobrecargar** `==`, cosa que `string` y los `record` hacen para comparar por valor, y reserva `ReferenceEquals` para preguntar por identidad de forma inequívoca; Skeet analiza esa maraña de `==`, `Equals`, `IEquatable<T>` y `ReferenceEquals` en *C# in Depth*.

El segundo eje es **quién define la igualdad de los tipos propios**. Rust lo hace explícito con rasgos: `PartialEq` habilita `==` y se suele derivar con `#[derive(PartialEq)]`, mientras que `Eq` promete además reflexividad total, algo que `f64` no puede prometer por culpa de `NaN`. Go compara structs con `==` campo a campo de forma automática siempre que todos los campos sean comparables, pero **prohíbe en tiempo de compilación** comparar slices, mapas o funciones: en vez de dar un resultado sorprendente, Go se niega a compilar, decisión que Donovan y Kernighan defienden en *The Go Programming Language* como preferible a una respuesta ambigua. En C no existe nada de esto: `==` sobre dos structs no compila, y comparar dos cadenas con `==` compila pero compara **punteros**, no texto —hay que usar `strcmp`—, uno de los errores más antiguos y persistentes del lenguaje.

El tercer eje es la **lógica de tres valores de SQL**. En los nueve lenguajes imperativos, `a == b` devuelve verdadero o falso. En SQL devuelve verdadero, falso o desconocido, y `NULL = NULL` es desconocido, no verdadero. Es una diferencia paradigmática de fondo: `NULL` en SQL no representa un valor sino la *ausencia* de valor, y no se puede afirmar que dos ausencias coincidan.

## 🧬 El concepto en la familia

Casi todos los lenguajes acaban ofreciendo dos comparaciones, y la manera de nombrarlas revela cuál consideran la primaria. Ruby es el más explícito: `==` es valor, `equal?` es identidad (y `eql?` añade estrictez de tipo para el uso en hashes). Python nombra la identidad con la palabra clave `is`, y su `==` delega en `__eq__`, que cualquier clase puede redefinir. Java, C# y C++ hacen de la identidad el comportamiento *por defecto* de `==` sobre objetos y dejan la igualdad estructural a un método (`equals`) o a una sobrecarga explícita del operador. La rama funcional invierte la prioridad: en Haskell, OCaml, Elixir o Clojure los valores son inmutables, la igualdad estructural es la comparación natural, y la identidad se vuelve casi irrelevante —si nada muta, saber si dos valores son «el mismo objeto» no cambia el comportamiento de ningún programa—. Ese es el patrón general que conviene llevarse: **cuanta más inmutabilidad ofrece un lenguaje, menos importa la identidad**. Swift lo dibuja con nitidez, con `==` para valor y el operador aparte `===` reservado a la identidad de instancias de clase, que son sus únicos tipos de referencia. Y Kotlin lo invierte respecto a Java, la plataforma que comparte: `==` llama a `equals` y `===` compara referencias, corrigiendo deliberadamente la trampa heredada.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 101
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Usar `==` sobre objetos en Java** → causa: `==` compara referencias, y el código pasa los tests porque los literales comparten el *pool* de cadenas, pero falla en cuanto los datos llegan de la entrada o de la red → solución: usar `equals` siempre que quieras comparar contenido, y reservar `==` para primitivos y para comprobar `null`.
- **Redefinir `equals` y olvidar `hashCode`** → causa: dos objetos iguales acaban con hashes distintos, caen en cubos distintos y el `HashMap` o el `HashSet` deja de encontrar lo que insertaste; el bug no aparece hasta que usas el objeto como clave → solución: redefinir ambos a la vez a partir de los mismos campos, o dejar que el lenguaje los genere (`record` de Java, `#[derive(PartialEq, Hash)]` de Rust, `@dataclass` de Python).
- **Confiar en la identidad de enteros o cadenas pequeñas** → causa: `a is b` en Python o `Integer == Integer` en Java dan `true` para valores pequeños por internalización o caché, y `false` para los grandes; el programa funciona con los datos de prueba y falla con los reales → solución: usar `==` o `equals` para comparar valores, y reservar `is` únicamente para centinelas como `None`.
- **Usar `==` en JavaScript y sufrir la coerción** → causa: `0 == "0"`, `0 == false` y `"" == 0` son todos `true`, y `null == undefined` también → solución: usar `===` por defecto; si necesitas convertir tipos, hazlo de forma explícita antes de comparar.
- **Comparar reales con `==`** → causa: `0.1 + 0.2` no da exactamente `0.3` en aritmética IEEE 754, y `NaN != NaN` por definición → solución: comparar con una tolerancia (`abs(a - b) < epsilon`) y usar la función específica del lenguaje para detectar `NaN`; en este ejercicio los datos son enteros y el problema no aparece.
- **Comparar cadenas con `==` en C** → causa: compara las direcciones de los dos punteros, no el texto → solución: `strcmp(a, b) == 0`.

## ❓ Preguntas frecuentes

- **¿`==` compara valor o referencia?** Depende del lenguaje y del tipo. Con primitivos siempre compara valor. Con objetos: valor en Python, PHP (`===`), Ruby y Rust; referencia en Java y C++ salvo sobrecarga; en C# depende de si el tipo sobrecarga el operador (`string` y los `record` sí lo hacen; una clase corriente no). No hay atajo: es un dato que hay que saber de cada lenguaje que uses.
- **¿Qué es `is` en Python?** Pregunta si dos nombres apuntan al mismo objeto, comparando sus direcciones. Su uso legítimo es contra centinelas únicos: `if x is None`. Para cualquier otra cosa, `==`.
- **¿Por qué mi `HashSet` tiene duplicados aparentes?** Porque tu tipo no define bien la igualdad, o define `equals` sin `hashCode`. El conjunto localiza el cubo por hash y solo compara por igualdad dentro de él: si dos objetos iguales hashean distinto, nunca llegan a compararse y ambos se guardan. Es la razón práctica de la regla de Bloch.
- **¿Cuándo necesito de verdad la identidad?** En pocos casos concretos: comprobar centinelas, detectar aliasing antes de copiar una estructura, cortocircuitar una comparación cara (`if (this == other) return true;` al principio de un `equals`), o gestionar recursos donde importa cuál instancia concreta tienes —una conexión, un archivo abierto—.
- **¿Y la igualdad de estructuras anidadas?** La comparación estructural es recursiva y su coste es O(tamaño total), no O(1). En Python `==` sobre listas anidadas compara elemento a elemento en profundidad; en Java `Arrays.equals` es superficial y hay que usar `Arrays.deepEquals`; en Go los slices directamente no se pueden comparar y hay que recorrerlos o usar `reflect.DeepEqual`. Es el mismo eje superficial-frente-a-profundo que trata la clase siguiente para la copia.

## 🔗 Referencias

**Libros de la parte:**

- T. Cormen, C. Leiserson, R. Rivest y C. Stein — *Introduction to Algorithms* (4ª ed., MIT Press).
- R. Sedgewick y K. Wayne — *Algorithms* (4ª ed., Addison-Wesley).

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

> [⏮️ Clase 100](../../parte-6-datos-y-estructuras/100-enumeraciones-y-tipos-algebraicos-adt-sum-types/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 102 ⏭️](../../parte-6-datos-y-estructuras/102-copia-superficial-vs-profunda-referencia-vs-valor/README.md)
