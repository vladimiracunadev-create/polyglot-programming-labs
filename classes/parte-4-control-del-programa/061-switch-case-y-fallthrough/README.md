# Clase 061 — switch, case y fallthrough

> Parte **4 — Control del programa** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

El `switch` nace de una necesidad muy concreta: cuando un programa debe elegir entre muchos valores exactos de una misma variable, una escalera de `if / else if / else if` se vuelve ilegible y, sobre todo, esconde la intención. El `switch` declara de un vistazo "estoy despachando según el valor de esta única expresión", y con ello el lector entiende el patrón sin reconstruirlo condición por condición. Detrás hay incluso una razón de máquina: un `switch` sobre valores densos permite al compilador generar una *tabla de saltos* (jump table), donde el valor se convierte en un índice y el salto es de coste constante, no una cadena de comparaciones.

Pero esa misma construcción arrastra una de las herencias más peligrosas de C: el `fallthrough`, la caída de un `case` al siguiente cuando falta un `break`. En esta clase traducimos un día (1..7) a su nombre y usamos ese problema mínimo para ver una divisoria profunda entre lenguajes: quiénes heredaron la caída implícita, quiénes la prohibieron y quiénes la sustituyeron por construcciones sin ese filo. El porqué de fondo es que un mecanismo de selección debe ser legible y a prueba de olvidos, no una trampa que castiga el descuido.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Seleccionar por valor exacto con switch/case.
2. Usar el caso por defecto.
3. Explicar el fallthrough y cómo lo maneja cada lenguaje.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | switch/case | Elegir por valor exacto |
| 2 | default | El caso por defecto |
| 3 | Fallthrough | Caída de un caso al siguiente (C/Java) |
| 4 | Alternativas | match/when sin caída |

## 📖 Definiciones y características

- **switch** — estructura que elige una rama según el valor exacto. Clave: para muchos valores concretos.
- **case** — una de las ramas del switch. Clave: coincide con un valor.
- **fallthrough** — en C/Java, un case sigue al siguiente si falta `break`. Clave: fuente de bugs.
- **default** — rama que se ejecuta si ningún case coincide. Clave: cubre lo inesperado.

Sebesta, en *Concepts of Programming Languages* (cap. sobre estructuras de control), clasifica el `switch` dentro de las *sentencias de selección múltiple* y muestra que el diseño oscila entre dos decisiones opuestas: si al terminar un `case` el control cae al siguiente por defecto o si sale del bloque. C tomó la primera opción —hija de que un `case` es, en el fondo, apenas una etiqueta a la que se salta— y con ello ganó flexibilidad (agrupar varios valores en una acción) al precio de un error casi imposible de ver a simple vista. La lección de fondo es la que Dahl, Dijkstra y Hoare defienden en *Structured Programming*: una construcción de control vale por su transparencia, por cuánto ayuda a razonar sobre lo que el programa hace sin ejecutarlo mentalmente. Un `switch` que "sigue de largo" en silencio traiciona esa transparencia.

Por eso los lenguajes posteriores reabrieron la decisión. Go conserva la palabra `switch` pero invierte el defecto: rompe automáticamente al final de cada `case` y exige un `fallthrough` explícito si de verdad quieres la caída. C# prohíbe la caída implícita y no compila si un `case` no termina en `break`, `return` o `goto`. Java, atado por compatibilidad, mantuvo el `switch` de dos puntos con caída, pero en Java 14 (JEP 361) añadió el `switch` de flechas `->`, donde cada rama es autónoma y no cae jamás. Rust fue más lejos y ni siquiera tiene `switch`: lo reemplaza por `match`. Todas estas variantes son la misma idea —despachar por valor— corrigiendo el mismo defecto histórico.

## 🧩 Situación

Traducir un código a un nombre —un día de la semana, un mes, un estado de un pedido, un código HTTP a su mensaje— es el trabajo más cotidiano del `switch`. Piensa en el enrutador de una máquina de estados: un byte de comando llega por la red y hay que despachar hacia la acción correcta. Es exactamente el patrón de esta clase, donde el entero `d` gobierna qué nombre de día se produce.

El drama de ingeniería aparece cuando ese `switch` crece y alguien, al añadir un nuevo `case` en medio, olvida el `break`. En C o en el Java clásico el programa sigue compilando sin una sola advertencia, pero en tiempo de ejecución un pedido "pagado" cae a la rama "reembolsado" y ejecuta lógica que no le corresponde. El bug no está en la línea que se ejecutó de más, sino en la ausencia silenciosa de una línea. Ese es el porqué de fondo de la clase: mecanismos aparentemente triviales de selección concentran una clase entera de errores caros, y la forma en que cada lenguaje resuelve —o no— el `fallthrough` revela su filosofía sobre cuánto debe protegerte el compilador de tus propios descuidos.

## 🧮 Modelo

- **Entrada** (stdin): un entero `d` (día)
- **Salida** (stdout): `dia=<nombre>` o `dia=invalido`
- **Regla:** 1→lunes … 7→domingo; otro→invalido

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `1` | `dia=lunes` |
| `6` | `dia=sabado` |
| `8` | `dia=invalido` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER d
SEGUN d: 1..7 -> nombre ; otro -> invalido
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys

d = int(sys.stdin.readline())
nombres = {1: "lunes", 2: "martes", 3: "miercoles", 4: "jueves",
           5: "viernes", 6: "sabado", 7: "domingo"}
print(f"dia={nombres.get(d, 'invalido')}")
```

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const d = parseInt(readFileSync(0, "utf8").trim(), 10);
let dia;
switch (d) {
  case 1: dia = "lunes"; break;
  case 2: dia = "martes"; break;
  case 3: dia = "miercoles"; break;
  case 4: dia = "jueves"; break;
  case 5: dia = "viernes"; break;
  case 6: dia = "sabado"; break;
  case 7: dia = "domingo"; break;
  default: dia = "invalido";
}
console.log(`dia=${dia}`);
```

🧬 **El mismo programa en la familia JavaScript / web:** [Dart · ActionScript](primos.md#javascript-web)

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const d: number = parseInt(readFileSync(0, "utf8").trim(), 10);
let dia: string;
switch (d) {
  case 1: dia = "lunes"; break;
  case 2: dia = "martes"; break;
  case 3: dia = "miercoles"; break;
  case 4: dia = "jueves"; break;
  case 5: dia = "viernes"; break;
  case 6: dia = "sabado"; break;
  case 7: dia = "domingo"; break;
  default: dia = "invalido";
}
console.log(`dia=${dia}`);
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
        int d = Integer.parseInt(br.readLine().trim());
        String dia;
        switch (d) {
            case 1: dia = "lunes"; break;
            case 2: dia = "martes"; break;
            case 3: dia = "miercoles"; break;
            case 4: dia = "jueves"; break;
            case 5: dia = "viernes"; break;
            case 6: dia = "sabado"; break;
            case 7: dia = "domingo"; break;
            default: dia = "invalido";
        }
        System.out.println("dia=" + dia);
    }
}
```

🧬 **El mismo programa en la familia JVM:** [Kotlin · Scala · Groovy · Clojure](primos.md#jvm)

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;

int d = int.Parse(Console.In.ReadToEnd().Trim());
string dia = d switch {
    1 => "lunes",
    2 => "martes",
    3 => "miercoles",
    4 => "jueves",
    5 => "viernes",
    6 => "sabado",
    7 => "domingo",
    _ => "invalido",
};
Console.WriteLine($"dia={dia}");
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
	d, _ := strconv.Atoi(strings.TrimSpace(line))
	var dia string
	switch d {
	case 1:
		dia = "lunes"
	case 2:
		dia = "martes"
	case 3:
		dia = "miercoles"
	case 4:
		dia = "jueves"
	case 5:
		dia = "viernes"
	case 6:
		dia = "sabado"
	case 7:
		dia = "domingo"
	default:
		dia = "invalido"
	}
	fmt.Printf("dia=%s\n", dia)
}
```

🧬 **El mismo programa en la familia Sistemas:** [Zig · Nim · D](primos.md#sistemas)

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let d: i64 = s.trim().parse().unwrap();
    let dia = match d {
        1 => "lunes",
        2 => "martes",
        3 => "miercoles",
        4 => "jueves",
        5 => "viernes",
        6 => "sabado",
        7 => "domingo",
        _ => "invalido",
    };
    println!("dia={dia}");
}
```

🧬 **El mismo programa en la familia Sistemas:** [Zig · Nim · D](primos.md#sistemas)

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long d;
    if (scanf("%ld", &d) != 1) return 1;
    const char *dia;
    switch (d) {
        case 1: dia = "lunes"; break;
        case 2: dia = "martes"; break;
        case 3: dia = "miercoles"; break;
        case 4: dia = "jueves"; break;
        case 5: dia = "viernes"; break;
        case 6: dia = "sabado"; break;
        case 7: dia = "domingo"; break;
        default: dia = "invalido";
    }
    printf("dia=%s\n", dia);
    return 0;
}
```

🧬 **El mismo programa en la familia C / llaves:** [C++ · Objective-C](primos.md#c-llaves)

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL: selección por valor con CASE WHEN.
WITH dias(d) AS (VALUES (1), (6), (8))
SELECT printf('dia=%s',
       CASE d WHEN 1 THEN 'lunes' WHEN 2 THEN 'martes' WHEN 3 THEN 'miercoles'
              WHEN 4 THEN 'jueves' WHEN 5 THEN 'viernes' WHEN 6 THEN 'sabado'
              WHEN 7 THEN 'domingo' ELSE 'invalido' END) AS resultado
FROM dias;
```

🧬 **El mismo programa en la familia Lógica y declarativa:** [Prolog · Datalog](primos.md#logica-declarativa)

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
$d = (int) trim(fgets(STDIN));
switch ($d) {
    case 1: $dia = "lunes"; break;
    case 2: $dia = "martes"; break;
    case 3: $dia = "miercoles"; break;
    case 4: $dia = "jueves"; break;
    case 5: $dia = "viernes"; break;
    case 6: $dia = "sabado"; break;
    case 7: $dia = "domingo"; break;
    default: $dia = "invalido";
}
echo "dia=$dia\n";
```

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔎 Recorrido del código: de la entrada a la salida

Sigamos el caso `6` de `casos.json`, cuya salida esperada es `dia=sabado`. En la versión de **Python** la línea `d = int(sys.stdin.readline())` lee la cadena `"6\n"`, la convierte al entero `6`, y aquí el código evita el `switch` por completo: construye un diccionario `nombres` que mapea cada número a su nombre y hace `nombres.get(d, 'invalido')`. Con `d=6`, `get` encuentra la clave y devuelve `"sabado"`; la interpolación produce `dia=sabado`. Es revelador que la solución más idiomática en Python no sea una selección múltiple sino una tabla de consulta: el propio despacho por valor se reifica en una estructura de datos. Con el caso `8`, la clave no existe, `get` devuelve su segundo argumento `'invalido'`, y sale `dia=invalido` sin ninguna rama especial.

Contrastémoslo con **C**, que sí ejerce el `switch` en su forma más cruda. Tras `scanf("%ld", &d)` con la entrada `6`, el control entra al `switch (d)` y salta directamente a `case 6:`, que asigna `dia = "sabado"` y ejecuta `break`. Ese `break` es la pieza crítica: sin él, el flujo caería a `case 7:` y `dia` acabaría valiendo `"domingo"`, produciendo una salida errónea que el compilador jamás señalaría. Cada rama del código C repite meticulosamente su `break` precisamente para blindarse contra esa caída. El `default` recoge el caso `8`: como ningún `case` coincide, asigna `"invalido"`.

La tercera mirada es **Go**, que usa `switch` pero con la semántica invertida. Con `d=6` salta a `case 6:`, asigna `dia = "sabado"` y sale automáticamente al terminar la rama —no hay `break` a la vista porque Go rompe por defecto. Si el autor hubiera querido la caída, tendría que haberla pedido con la palabra `fallthrough`. Las tres rutas —tabla de Python, `break` explícito de C, ruptura automática de Go— transforman el mismo `6` en el mismo `dia=sabado`, pero cada una encarna una respuesta distinta al peligro del `fallthrough`.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `switch` con `break` (C/Java/JS) vs. `match` (Rust) vs. `when` (Kotlin). |
| Semántica | C/Java caen sin `break`; Go, Rust y el switch de Python (match) no caen. |
| Paradigmática | SQL usa CASE WHEN valor. |

Puestos los diez lenguajes uno junto a otro, se dibuja un espectro claro de seguridad. En un extremo, **C** exige un `break` manual en cada rama y no advierte de nada si falta: es la caída implícita en estado puro. **JavaScript**, **TypeScript** y **PHP** heredaron literalmente esa sintaxis y ese peligro, aunque los linters modernos suelen marcar el olvido. **Java** ocupa una posición intermedia: su `switch` clásico cae, pero desde Java 14 dispone de la forma con flechas que no lo hace. **Go** conserva la palabra pero rompe por defecto y pide `fallthrough` explícito, invirtiendo el riesgo. **C#** directamente prohíbe la caída implícita y rechaza compilar un `case` que no cierre su flujo. En el extremo más seguro, **Rust** no tiene `switch` y obliga a usar `match`, mientras que **Python** —sin `switch` hasta la 3.10— aquí resuelve con un diccionario. **SQL**, declarativo, expresa la misma decisión con `CASE ... WHEN valor`, sin concepto alguno de caída. La misma tarea, diez actitudes distintas frente al mismo defecto histórico.

## 🧬 El concepto en la familia

En la familia de los descendientes de C —C, C++, Java, JavaScript, PHP— el `switch` con caída implícita es la norma, un rasgo hereditario que arrastra su mismo riesgo. La familia de los lenguajes funcionales y modernos (Rust, Scala, F#, y en buena medida Kotlin con su `when` y Swift con su `switch` sin caída) sustituyó el mecanismo por coincidencia de patrones, donde cada rama es autónoma por diseño. En Ruby, `case d; when 1 then 'lunes'` no cae nunca; en Kotlin, `when (d) { 1 -> ... }` tampoco. La tendencia histórica es inequívoca: los lenguajes nuevos abandonan el `fallthrough` por defecto porque la experiencia acumulada mostró que su coste en errores supera con creces su ocasional comodidad.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 061
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Olvidar `break` en C/Java clásico** → causa: al terminar un `case`, el flujo cae al siguiente y ejecuta código ajeno sin ningún aviso del compilador → solución: cerrar cada `case` con `break` (o `return`), o migrar al `switch` de flechas de Java 14+, que no cae.
- **No incluir `default`** → causa: si el valor no coincide con ningún `case`, la variable de salida queda sin asignar y produce salida vacía, basura o un fallo en tiempo de ejecución → solución: incluir siempre una rama `default` que cubra "todo lo demás", como el `dia=invalido` de esta clase.
- **Agrupar valores por accidente** → causa: querer que solo un `case` actúe pero dejar sin `break` uno anterior, encadenando acciones no buscadas → solución: si de verdad quieres agrupar varios valores en una acción, hazlo explícito apilando etiquetas `case` (o usando `fallthrough` en Go) para que la intención se lea.
- **Comparar tipos que el `switch` no soporta** → causa: en C el `switch` solo admite enteros; usar cadenas o reales no compila → solución: en lenguajes sin `switch` sobre cadenas, mapear con un diccionario o usar `if`/`else` sobre igualdad.

## ❓ Preguntas frecuentes

- **¿Por qué existe el fallthrough si causa tantos errores?** Es una consecuencia del modelo original de C, donde un `case` no es más que una etiqueta de salto dentro de un bloque; una vez dentro, la ejecución continúa hasta un `break`. Ocasionalmente es útil para agrupar varios valores en una misma acción, pero la experiencia mostró que el olvido accidental cuesta más que esa comodidad, y por eso los lenguajes nuevos lo invirtieron o eliminaron.
- **¿Go tiene fallthrough?** No por defecto: cada `case` rompe automáticamente al terminar. Si necesitas la caída explícita, existe la palabra reservada `fallthrough`, que debes escribir tú. Go volvió el peligro en una decisión consciente y visible.
- **¿Qué es el "Duff's device"?** Es una técnica histórica de C que aprovecha justamente el `fallthrough` para intercalar un `switch` con un bucle y desenrollar copias de memoria. Es una curiosidad brillante y a la vez la mejor prueba de lo permisivo que es el modelo de C: solo funciona porque la caída entre `case` está permitida.
- **¿Por qué Python usa un diccionario aquí en vez de `switch`?** Python no tuvo ninguna sentencia `switch` hasta el `match` de la 3.10, y para el despacho por valor exacto la solución idiomática siempre fue un diccionario `{valor: resultado}` con `.get(clave, defecto)`, que es a la vez tabla de consulta y caso por defecto.

## 🔗 Referencias

**Libros de la parte:**

- O.-J. Dahl, E. W. Dijkstra y C. A. R. Hoare — *Structured Programming* (Academic Press). La *Notes on Structured Programming* de Dijkstra argumenta por qué una construcción de control debe ser legible sin ejecutarla mentalmente: el criterio con el que aquí juzgamos el `fallthrough`.
- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson), cap. sobre estructuras de control, sección de *sentencias de selección múltiple*, que compara los diseños de `switch` con y sin caída implícita.

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

> [⏮️ Clase 060](../../parte-4-control-del-programa/060-expresiones-condicionales-ternario-e-if-como-expresion/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 062 ⏭️](../../parte-4-control-del-programa/062-coincidencia-de-patrones-match-when/README.md)
