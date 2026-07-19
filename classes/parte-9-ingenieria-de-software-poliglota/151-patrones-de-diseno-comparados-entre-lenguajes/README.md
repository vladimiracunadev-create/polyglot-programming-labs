# Clase 151 — Patrones de diseño comparados entre lenguajes

> Parte **9 — Ingeniería de software políglota** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

En 1994, cuatro autores —Gamma, Helm, Johnson y Vlissides, la «Banda de los Cuatro» o *GoF*— publicaron *Design Patterns*, un catálogo de veintitrés soluciones recurrentes a problemas de diseño orientado a objetos. Su tesis no era inventar trucos nuevos, sino **darle nombre** a estructuras que los buenos diseñadores ya reinventaban una y otra vez. Un patrón es, en sus palabras, «una solución a un problema en un contexto»: nombre, problema, solución y consecuencias. El valor no está solo en la técnica, sino en el **vocabulario compartido**: decir «aquí uso una Estrategia» comunica en dos palabras una intención de diseño que de otro modo requeriría un párrafo.

Esta clase se centra en el patrón **Estrategia** (*Strategy*), quizá el más puro del catálogo. Su intención, según GoF, es «definir una familia de algoritmos, encapsular cada uno y hacerlos intercambiables». El programa de juguete —elegir entre suma, resta o producto por el nombre de la operación— es un Estrategia en miniatura: la operación es el algoritmo variable, y el nombre selecciona cuál se aplica. La razón de ingeniería es honda: cuando un comportamiento tiene varias variantes, meterlas todas en un `if/else` gigante hace que cada nueva variante obligue a tocar y arriesgar el mismo bloque. Estrategia extrae cada algoritmo a su propia unidad y deja que el código cliente elija sin conocer los detalles. Fowler, en *Refactoring*, describe exactamente esta transición como «Replace Conditional with Polymorphism»: el condicional disperso se convierte en un despacho limpio.

Lo revelador de recorrer diez lenguajes es que **el mismo patrón cambia de forma** según lo que cada lenguaje considera idiomático. En Java o C# la Estrategia clásica es una interfaz con implementaciones; en Python, JavaScript o Go, donde las funciones son valores de primera clase, una Estrategia es simplemente una función guardada en una variable o un mapa; en Rust puede ser un `trait` o un `match`; en C#, un `delegate`. El patrón es una idea; su encarnación es lengua.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. **Explicar** la intención del patrón Estrategia y en qué se diferencia de un condicional disperso.
2. **Reconocer** cómo cambia de forma el mismo patrón según el lenguaje: interfaces, funciones de primera clase, traits o delegados.
3. **Implementar** un despacho por nombre que seleccione un algoritmo en ejecución.
4. **Justificar** cuándo un patrón aporta y cuándo es sobreingeniería.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Patrón de diseño (GoF) | Solución con nombre a un problema recurrente; vocabulario común |
| 2 | Estrategia | Algoritmos intercambiables tras una interfaz común |
| 3 | Selección en ejecución | Elegir el comportamiento al vuelo, sin condicionales rígidos |
| 4 | Forma idiomática por lenguaje | Interfaces, funciones-valor, traits o delegados |

## 📖 Definiciones y características

Un **patrón de diseño** no es una biblioteca ni un fragmento copiable: es un esquema de solución. GoF lo estructura en cuatro partes —nombre, problema, solución y consecuencias— precisamente porque las *consecuencias* (qué gana y qué cuesta) son tan importantes como la técnica. Aplicar un patrón siempre tiene un precio en indirección; el juicio de ingeniería consiste en saber si ese precio compensa. Hunt y Thomas advierten en *The Pragmatic Programmer* contra el «programador cargo-cult» que aplica patrones por moda: un patrón mal usado añade complejidad sin resolver nada.

El **patrón Estrategia** encapsula cada algoritmo de una familia tras una interfaz común y deja que el cliente los intercambie sin cambiar. El síntoma que cura es el condicional que crece: cada vez que aparece una variante nueva, en lugar de añadir una rama a un `switch` que ya nadie entiende, se añade una estrategia. El **despacho** es el mecanismo que traduce un valor —aquí, el nombre de la operación— en la elección de qué código ejecutar. En los lenguajes con funciones de primera clase, ese despacho suele ser una tabla (un diccionario o mapa) que asocia nombres a funciones; en los orientados a objetos clásicos, un polimorfismo sobre una jerarquía.

## 🧩 Situación

Trabajas en la pasarela de cobro de una tienda. Al principio solo aceptabas tarjeta, así que el método de cobro era un bloque directo. Luego llegó la transferencia, después el monedero, después el pago contra reembolso. Con cada forma nueva, aquel `if tipo == "tarjeta" ... elif ...` se volvió un monstruo que había que releer entero y volver a probar en cada release. Refactorizas a Estrategia: cada forma de cobro es un objeto (o una función) con la misma firma `cobrar(monto)`, y un registro asocia el nombre del método a su estrategia. Añadir «cripto» ya no toca el código existente: registras una estrategia nueva. El ejercicio de esta clase —elegir suma, resta o producto por nombre— es esa misma mecánica reducida a lo mínimo.

## 🧮 Modelo

- **Entrada** (stdin): una línea `estrategia a b` (estrategia ∈ {suma, resta, producto})
- **Salida** (stdout): `resultado=<a estrategia b>`
- **Regla:** aplicar la estrategia elegida a a y b

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `suma 3 4` | `resultado=7` |
| `resta 10 3` | `resultado=7` |
| `producto 5 6` | `resultado=30` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER estrategia, a, b ; seleccionar operación ; aplicar
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

En Python la Estrategia toma su forma más ligera: un diccionario. Ramalho, en *Fluent Python*, dedica un capítulo entero a mostrar que, en un lenguaje con funciones de primera clase, el patrón Estrategia «clásico» de GoF —una interfaz y una clase por algoritmo— se disuelve en un simple mapa de nombres a valores. Aquí no hay ni siquiera funciones: el diccionario `ops` guarda el *resultado ya calculado* de cada operación sobre `a` y `b`, y `ops[estrategia]` selecciona el que corresponde al nombre leído. La línea `estrategia, a, b = ...split()` desempaqueta las tres palabras de la entrada; luego `a` y `b` pasan a enteros, y la indexación `ops[estrategia]` es el despacho.

```python
import sys

estrategia, a, b = sys.stdin.readline().split()
a, b = int(a), int(b)
ops = {"suma": a + b, "resta": a - b, "producto": a * b}
print(f"resultado={ops[estrategia]}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const [estrategia, a, b] = readFileSync(0, "utf8").trim().split(/\s+/);
const x = Number(a), y = Number(b);
const ops = { suma: x + y, resta: x - y, producto: x * y };
console.log(`resultado=${ops[estrategia]}`);
```

### TypeScript · `pnpm exec tsx main.ts`

La versión de TypeScript es idéntica en espíritu, pero fíjate en la anotación `Record<string, number>` sobre `ops`. Cherny, en *Programming TypeScript*, insiste en que el tipo documenta el contrato de la tabla de estrategias: las claves son cadenas y los valores números. En una Estrategia real con funciones, ese tipo sería algo como `Record<string, (a: number, b: number) => number>`, y el compilador garantizaría que toda estrategia registrada respete la firma.

```typescript
import { readFileSync } from "node:fs";

const [estrategia, a, b] = readFileSync(0, "utf8").trim().split(/\s+/);
const x = Number(a), y = Number(b);
const ops: Record<string, number> = { suma: x + y, resta: x - y, producto: x * y };
console.log(`resultado=${ops[estrategia]}`);
```

### Java · `java Main.java`

Java muestra el otro extremo del espectro. Sin funciones de primera clase hasta Java 8, la Estrategia canónica de GoF nació aquí: una interfaz `Operacion` con un método `aplicar(a, b)` y una clase por variante. La implementación mínima de abajo usa un `switch` sobre el nombre —el despacho hecho a mano— porque el problema de juguete no justifica tres clases. Bloch, en *Effective Java*, recomienda para estos casos las estrategias como *function objects* o, desde Java 8, referencias a método y lambdas guardadas en un `Map<String, BinaryOperator<Long>>`. El `switch` explícito es la forma honesta cuando las variantes son fijas y triviales.

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] t = br.readLine().trim().split("\\s+");
        long a = Long.parseLong(t[1]), b = Long.parseLong(t[2]);
        long r;
        switch (t[0]) {
            case "suma": r = a + b; break;
            case "resta": r = a - b; break;
            default: r = a * b;
        }
        System.out.println("resultado=" + r);
    }
}
```

### C# · `dotnet run`

C# ofrece un tercer camino nativo: el **delegado**. Un `delegate` es un tipo que representa una función, y `Func<long, long, long>` es exactamente la firma de una estrategia binaria. Aquí, en cambio, la implementación usa una expresión `switch` moderna (`t[0] switch { ... }`), que Skeet en *C# in Depth* describe como el reemplazo idiomático del condicional: concisa, exhaustiva y sin `break`. En un diseño de producción registrarías `Func` en un diccionario y el patrón Estrategia se vería como una tabla de delegados.

```csharp
using System;

string[] t = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
long a = long.Parse(t[1]), b = long.Parse(t[2]);
long r = t[0] switch { "suma" => a + b, "resta" => a - b, _ => a * b };
Console.WriteLine($"resultado={r}");
```

### Go · `go run main.go`

Go no tiene clases ni herencia, pero sí funciones de primera clase, así que vuelve a la forma-mapa de Python. Donovan y Kernighan muestran en *The Go Programming Language* que una `map[string]func(int, int) int` es la Estrategia idiomática en Go; aquí el mapa guarda directamente los resultados. La indexación `ops[t[0]]` es el despacho.

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
	t := strings.Fields(line)
	a, _ := strconv.Atoi(t[1])
	b, _ := strconv.Atoi(t[2])
	ops := map[string]int{"suma": a + b, "resta": a - b, "producto": a * b}
	fmt.Printf("resultado=%d\n", ops[t[0]])
}
```

### Rust · `rustc main.rs -o main && ./main`

Rust brinda el contraste conceptual más rico. La Estrategia idiomática se expresa con un **trait** (un contrato de comportamiento) e implementaciones que se pasan como `Box<dyn Operacion>` o como genéricos monomorfizados. Pero aquí Klabnik y Nichols nos recordarían que el `match` exhaustivo es a menudo más claro: el compilador verifica que cubras todos los casos, y el patrón `_ => a * b` captura el resto. El `match` sobre `t[0]` es despacho estático; el trait sería despacho dinámico. Ambos son Estrategia.

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let t: Vec<&str> = s.split_whitespace().collect();
    let a: i64 = t[1].parse().unwrap();
    let b: i64 = t[2].parse().unwrap();
    let r = match t[0] {
        "suma" => a + b,
        "resta" => a - b,
        _ => a * b,
    };
    println!("resultado={r}");
}
```

### C · `cc main.c -o main && ./main`

C no tiene mapas ni traits, pero sí **punteros a función**, que son la Estrategia de más bajo nivel: una tabla de `long (*)(long, long)` indexada por nombre. La implementación mínima usa `strcmp` encadenados —el despacho más elemental— porque para tres casos fijos no hace falta más. Kernighan y Ritchie muestran en *The C Programming Language* que los punteros a función son precisamente lo que permite pasar comportamiento como dato en un lenguaje sin objetos.

```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char e[32];
    long a, b;
    if (scanf("%31s %ld %ld", e, &a, &b) != 3) return 1;
    long r;
    if (strcmp(e, "suma") == 0) r = a + b;
    else if (strcmp(e, "resta") == 0) r = a - b;
    else r = a * b;
    printf("resultado=%ld\n", r);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: selecciona la estrategia con CASE.
WITH t(e, a, b) AS (VALUES ('suma', 3, 4))
SELECT printf('resultado=%d', CASE e WHEN 'suma' THEN a + b WHEN 'resta' THEN a - b ELSE a * b END) AS resultado FROM t;
```

### PHP · `php main.php`

```php
<?php
[$e, $a, $b] = preg_split('/\s+/', trim(fgets(STDIN)));
$a = (int) $a;
$b = (int) $b;
$ops = ["suma" => $a + $b, "resta" => $a - $b, "producto" => $a * $b];
echo "resultado=" . $ops[$e] . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Estrategia idiomática | Interfaz/clases (Java clásico); mapa de funciones (Python, JS, Go, PHP); trait o `match` (Rust); delegado o `switch` de expresión (C#); punteros a función (C); `CASE` (SQL) |
| Funciones como valores | Python, JS, TS, Go, C#, Rust, PHP las tienen; en Java llegaron con lambdas (8+); en C son punteros a función |
| Verificación del despacho | Rust y C# fuerzan `match`/`switch` exhaustivos; Java y C dejan el `default` a tu criterio; los mapas fallan en clave ausente |
| Herramienta de patrones | Java/C# empujan a la Estrategia OO clásica; los lenguajes funcionales la reducen a una tabla |

En un diseño real, la diferencia decisiva no es la sintaxis sino qué tan barato es añadir una estrategia. Un mapa de funciones permite registrar variantes en tiempo de ejecución (incluso desde plugins); una jerarquía de clases las fija en compilación. Ninguna es «mejor»: la primera favorece la extensibilidad dinámica, la segunda el control estático.

## 🧬 El concepto en la familia

Estrategia es solo uno de los veintitrés patrones GoF. Sus parientes cercanos comparten el gesto de encapsular variación: **Observer** (notificar a interesados sin acoplarlos), **Factory Method** (delegar la creación de objetos a subclases), **Singleton** (garantizar una única instancia), **Command** (encapsular una acción como objeto), **Template Method** (fijar el esqueleto de un algoritmo y dejar huecos). En marcos modernos los patrones a menudo desaparecen a la vista: la inyección de dependencias es Estrategia industrializada, y un middleware HTTP es Cadena de Responsabilidad. Reconocerlos bajo distintos nombres es lo que da fluidez para moverse entre lenguajes y frameworks.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 151
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Condicionales gigantes en vez de estrategias** → causa: cada variante nueva obliga a tocar y reprobar el mismo bloque → solución: encapsular cada algoritmo tras una interfaz o función común (Fowler: *Replace Conditional with Polymorphism*)
- **Sobre-aplicar patrones** → causa: complejidad e indirección sin beneficio → solución: usar el patrón solo cuando la variación existe de verdad (Hunt y Thomas: no seas cargo-cult)
- **Clave de despacho ausente** → causa: nombre no registrado → solución: valida la entrada o define un caso por defecto explícito
- **Confundir el patrón con su forma en un lenguaje** → causa: creer que Estrategia «es» una interfaz Java → solución: reconocer que un mapa de funciones también lo es

## ❓ Preguntas frecuentes

- **¿Estrategia o if/else?** Estrategia cuando los algoritmos cambian, crecen o se registran dinámicamente; if/else para casos simples y fijos que nunca crecerán.
- **¿Los patrones son obligatorios?** No: son herramientas y vocabulario. GoF describe consecuencias, no mandamientos; aplícalos cuando resuelven un problema real.
- **¿Por qué el mismo patrón se ve tan distinto en Java y en Python?** Porque depende de si el lenguaje tiene funciones de primera clase. Donde una función es un valor, la Estrategia colapsa en un mapa; donde no, se recurre a interfaces y clases.

## 🔗 Referencias

**Libros de la parte:**

- S. McConnell — *Code Complete* (2ª ed., Microsoft Press).
- A. Hunt y D. Thomas — *The Pragmatic Programmer* (2ª ed., Addison-Wesley).
- M. Fowler — *Refactoring* (2ª ed., Addison-Wesley).
- E. Gamma, R. Helm, R. Johnson y J. Vlissides — *Design Patterns* (Addison-Wesley; «GoF»).
- K. Beck — *Test-Driven Development: By Example* (Addison-Wesley).

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

> [⏮️ Clase 150](../../parte-9-ingenieria-de-software-poliglota/150-refactorizacion-segura/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 152 ⏭️](../../parte-9-ingenieria-de-software-poliglota/152-rendimiento-y-perfilado-profiling/README.md)
