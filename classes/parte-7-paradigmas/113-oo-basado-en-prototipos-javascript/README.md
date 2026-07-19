# Clase 113 — OO basado en prototipos (JavaScript)

> Parte **7 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Casi todo lo que aprendiste sobre orientación a objetos —clases, jerarquías, instancias— asume un modelo que JavaScript **no tiene por debajo**. En la mayoría de lenguajes, una clase es un molde: un plano estático a partir del cual se fabrican objetos. JavaScript hereda otra tradición, la del lenguaje Self de los años 80: aquí no hay moldes, hay **objetos que heredan directamente de otros objetos**. Cuando pides una propiedad y el objeto no la tiene, el motor no consulta una clase sino que sube por una **cadena de prototipos** —un enlace vivo de objeto a objeto— hasta encontrarla o agotarse. El objetivo de esta clase es que veas ese mecanismo con claridad, porque explica comportamientos de JavaScript que desde la óptica de las clases parecen magia o accidentes.

La distinción es más que una curiosidad histórica. En el modelo de clases, la relación "de dónde saco mis métodos" se fija cuando se define la clase y no cambia. En el modelo de prototipos, esa relación es un **enlace en tiempo de ejecución** que puedes inspeccionar y modificar: dos objetos pueden compartir un prototipo, y un cambio en el prototipo se refleja al instante en todos los que delegan en él. Haverbeke, en el capítulo 6 de *Eloquent JavaScript*, construye la OO del lenguaje partiendo justo de aquí —objetos, métodos y prototipos— y solo al final presenta la palabra `class` como lo que realmente es: **azúcar sintáctico** sobre esa maquinaria de delegación.

El objetivo práctico es doble. Primero, que entiendas `this`: en JavaScript no es una referencia fija al objeto donde se definió el método, sino al objeto sobre el que se **invoca**, decidido en cada llamada. Segundo, que puedas contrastar con criterio los dos modelos de OO —clases vs. prototipos— que recorren toda esta parte del curso, y reconozcas que producen el mismo comportamiento observable (un objeto con estado que sabe calcular) por caminos conceptualmente distintos.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Crear un objeto con estado y método.
2. Explicar la herencia por prototipos.
3. Contrastar prototipos con clases.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Prototipos | Objetos que heredan de objetos |
| 2 | Método en objeto | Comportamiento ligado al valor |
| 3 | Clases vs. prototipos | Dos modelos de OO |

## 📖 Definiciones y características

- **Prototipo** — objeto del que otro hereda propiedades y métodos. Clave: cadena de prototipos en JS.
- **Objeto literal** — objeto creado directamente con sus campos y métodos. Clave: `{ v: n, doble() {...} }`.
- **this** — referencia al objeto sobre el que se llama el método. Clave: accede a su estado.

El corazón del modelo es la **delegación**, no la instanciación. Haverbeke (*Eloquent JavaScript*, cap. 6) lo describe así: cada objeto tiene un enlace interno a su prototipo, y cuando buscas una propiedad que el objeto no posee, el motor la busca en el prototipo, luego en el prototipo del prototipo, y así hasta `Object.prototype`, cuyo prototipo es `null`. Esa **cadena de prototipos** es una lista enlazada de objetos que se resuelve en cada acceso. La diferencia con las clases es sutil pero profunda: en un lenguaje de clases el objeto *copia* la estructura de su molde al nacer; en JavaScript el objeto *delega* en su prototipo en cada lectura, en vivo. Por eso puedes añadir un método a un prototipo después de crear los objetos y todos lo "ganan" de inmediato.

Este linaje viene del lenguaje **Self** (Ungar y Smith, Xerox PARC), que eliminó las clases para unificarlo todo en objetos que se clonan y delegan. Brendan Eich lo adoptó al diseñar JavaScript en 1995, y de ahí que el lenguaje careciera de `class` durante casi veinte años. La palabra `class` llegó con ES2015, pero —insiste Haverbeke— es **azúcar sintáctico**: `class Obj { doble() {...} }` sigue creando una función constructora y colgando `doble` de `Obj.prototype`. No hay un mecanismo nuevo debajo; hay una notación más cómoda sobre el mismo modelo de delegación.

La otra pieza esencial es **`this`**. En muchos lenguajes `this`/`self` es el objeto receptor y punto. En JavaScript, `this` se determina por la **forma de la llamada**: en `obj.doble()`, `this` es `obj`; pero si extraes el método (`const f = obj.doble; f()`), `this` se pierde y pasa a ser `undefined` (en modo estricto) o el objeto global. Esta atadura dinámica es la fuente de casi todos los tropiezos con prototipos, y entenderla es la mitad del valor de esta clase: `this` no dice "el objeto donde se escribió el método", sino "el objeto a la izquierda del punto en esta invocación".

## 🧩 Situación

Estás depurando código JavaScript real y te topas con algo desconcertante: un método que funciona perfecto cuando lo llamas como `obj.doble()` de pronto da `NaN` o lanza un error cuando lo pasas como *callback* a `setTimeout` o a un `.map`. Nada en el cuerpo del método cambió; lo que cambió es **quién es `this`** en el momento de la invocación. Sin el modelo de prototipos y su regla de `this`, ese comportamiento es inexplicable y se "arregla" a golpe de superstición. Con el modelo claro, es predecible: `this` se ata en la llamada, no en la definición.

En esta clase reduces ese fenómeno a su forma mínima. Un objeto guarda un `valor` y expone un método `doble()` que devuelve `this.valor * 2`. Los tres casos —`5 → resultado=10`, `0 → resultado=0`, `7 → resultado=14`— son deliberadamente simples para que la atención esté en el mecanismo, no en la aritmética: cómo un objeto literal lleva su propio comportamiento y cómo `this` conecta el método con el estado del objeto sobre el que se invoca.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n`
- **Salida** (stdout): `resultado=<2n>`
- **Regla:** objeto.doble() = valor·2

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `resultado=10` |
| `0` | `resultado=0` |
| `7` | `resultado=14` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
obj <- { valor: n, doble() { DEVOLVER valor*2 } } ; ESCRIBIR obj.doble()
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

n = int(sys.stdin.readline())
obj = {"valor": n}
def doble(o):
    return o["valor"] * 2
print(f"resultado={doble(obj)}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
// Objeto literal con método (modelo de prototipos).
const obj = {
  valor: n,
  doble() {
    return this.valor * 2;
  },
};
console.log(`resultado=${obj.doble()}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
const obj = {
  valor: n,
  doble(): number {
    return this.valor * 2;
  },
};
console.log(`resultado=${obj.doble()}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    static class Obj {
        int valor;
        Obj(int v) { valor = v; }
        int doble() { return valor * 2; }
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        System.out.println("resultado=" + new Obj(n).doble());
    }
}
```

### C# · `dotnet run`

```csharp
using System;

int n = int.Parse(Console.In.ReadToEnd().Trim());
var obj = new Obj(n);
Console.WriteLine($"resultado={obj.Doble()}");

class Obj {
    int valor;
    public Obj(int v) { valor = v; }
    public int Doble() => valor * 2;
}
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

type Obj struct{ valor int }

func (o Obj) doble() int { return o.valor * 2 }

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	n, _ := strconv.Atoi(strings.TrimSpace(line))
	o := Obj{valor: n}
	fmt.Printf("resultado=%d\n", o.doble())
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

struct Obj {
    valor: i64,
}

impl Obj {
    fn doble(&self) -> i64 {
        self.valor * 2
    }
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let o = Obj { valor: n };
    println!("resultado={}", o.doble());
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

struct Obj {
    long valor;
};

long doble(struct Obj *o) {
    return o->valor * 2;
}

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    struct Obj o = {n};
    printf("resultado=%ld\n", doble(&o));
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL no tiene objetos; el cálculo va en la consulta.
WITH nums(n) AS (VALUES (5), (0), (7))
SELECT printf('resultado=%d', n * 2) AS resultado FROM nums;
```

### PHP · `php main.php`

```php
<?php
$n = (int) trim(fgets(STDIN));
$obj = new class($n) {
    public function __construct(public int $valor) {}
    public function doble(): int { return $this->valor * 2; }
};
echo "resultado=" . $obj->doble() . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🧪 Laboratorio guiado — recorrido del código

Sigamos el caso `5 → resultado=10` de [`casos.json`](casos.json), junto a `0 → resultado=0` y `7 → resultado=14`. El verificador entrega el entero por `stdin` y espera exactamente `resultado=<2n>`.

El protagonista es **JavaScript**, y su implementación es la única que expresa el paradigma en su forma nativa. Tras leer `n`, crea un **objeto literal** con estado y método a la vez:

```javascript
const obj = { valor: n, doble() { return this.valor * 2; } };
console.log(`resultado=${obj.doble()}`);
```

Aquí no hay clase, no hay `new`, no hay molde: se construye directamente el objeto que se necesita. La sintaxis `doble() { ... }` es la forma abreviada de definir un método dentro del literal. Cuando se ejecuta `obj.doble()`, ocurren dos cosas que son el núcleo de la clase. Primero, el motor busca la propiedad `doble` en `obj`; la encuentra allí mismo (si no estuviera, subiría por la cadena de prototipos hasta `Object.prototype`). Segundo, y crucial, la **forma de la llamada** —`obj.doble()`, con `obj` a la izquierda del punto— fija `this = obj` durante la ejecución del método. Por eso `this.valor` vale `5` y `this.valor * 2` da `10`, produciendo `resultado=10`. Con `n = 0` el mismo método devuelve `0`; con `n = 7`, `14`. El comportamiento no está en ninguna clase: viaja pegado al objeto.

**Python** resuelve el mismo caso, pero delata que su modelo es otro. En lugar de un objeto con método, usa un diccionario para el estado y una **función libre** para el comportamiento:

```python
obj = {"valor": n}
def doble(o):
    return o["valor"] * 2
```

No hay `this` implícito: el objeto se pasa explícitamente como parámetro `o`, y `doble(obj)` devuelve `obj["valor"] * 2`. Es una elección honesta —Python tiene clases perfectas para esto— que pone el contraste sobre la mesa: donde JavaScript liga método y estado en un mismo literal con `this` dinámico, la versión Python separa datos (diccionario) de operación (función) y hace explícito lo que JS resuelve por la cadena de prototipos. El resultado impreso, `resultado=10`, es idéntico.

El resto del núcleo usa el modelo de **clases/structs** para reproducir la misma salida: **Java** define una clase `Obj` con campo `valor` y método `doble()`; **Rust** un `struct Obj` con un `impl` que expone `doble(&self)`; **Go** un `struct` con un método de valor. En todos ellos el "receptor" (`this`, `self`, `&self`, `o`) está atado al tipo desde la definición, no negociado en cada llamada como en JavaScript. Ese es exactamente el punto pedagógico: la misma operación `valor * 2` sobre un objeto llega a `resultado=10` por dos rutas conceptuales —delegación en prototipos vs. instanciación de clases—. El **SQL**, como en las clases hermanas, es *ilustrativo*: no tiene objetos, así que calcula `n * 2` directamente en el `SELECT` sobre una tabla de valores. Ver esa gama, de la delegación pura de JS al `SELECT` sin objetos, es lo que hace concreto qué significa "OO basada en prototipos".

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Objeto literal con método (JS) vs. clase (otros). |
| Semántica | JS hereda por prototipos; los demás por clases. |
| Paradigmática | SQL no tiene objetos. |

La diferencia real no es sintáctica sino **cuándo y cómo se resuelve el enlace entre objeto y comportamiento**. En Java, Go, Rust o C#, ese enlace queda fijado por el tipo en tiempo de compilación: un `Obj` siempre toma su `doble()` de la definición de `Obj`, y no hay forma de que un objeto individual cambie de método en caliente. En JavaScript el enlace se resuelve en cada acceso subiendo por la cadena de prototipos, que es mutable: puedes reasignar el prototipo de un objeto o añadir métodos a un prototipo compartido y afectar retroactivamente a todos sus delegados. Esa flexibilidad es potente y peligrosa a partes iguales —de ahí que "modificar prototipos ajenos" (*monkey patching*) sea un antipatrón conocido.

La segunda diferencia es el tratamiento de **`this`/`self`**. Python lo hace explícito (`self` es el primer parámetro, sin ambigüedad); Rust lo tipa cuidadosamente (`&self`, `&mut self`, `self`); Java y C# lo tienen implícito pero siempre atado al receptor. JavaScript es el único del núcleo donde `this` depende de la *forma* de la invocación y puede perderse al pasar el método como valor. Por eso conviven en JS las funciones flecha (que capturan el `this` léxico) y `.bind()` (que lo fija): son parches idiomáticos a una atadura dinámica que los demás lenguajes simplemente no tienen.

## 🧬 El concepto en la familia

El modelo de prototipos es minoritario pero influyente. **Self** lo inventó al eliminar las clases; **Lua** lo ofrece mediante *metatables* y el metamétodo `__index`, que implementa la misma búsqueda por delegación con otra notación; **JavaScript** lo llevó a la ubicuidad de la web. Frente a ellos, la gran mayoría —Java, C#, Python, Ruby, C++, Go (con structs), Rust (con impls)— usa el modelo de clases o de tipos con métodos, donde el comportamiento se ata al tipo, no al objeto individual. La lección de esta clase es que ambos modelos entregan lo mismo a ojos del usuario —objetos con estado que responden a mensajes— y que la `class` de JavaScript es un puente deliberado: una fachada familiar sobre la delegación de prototipos, no un cambio de motor.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 113
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Perder el `this` en JS** → causa: extraer el método de su objeto (`const f = obj.doble; f()`) o pasarlo como *callback* a `map`, `setTimeout` o un manejador de evento, con lo que `this` deja de ser `obj` → solución: preservar el receptor con `obj.doble.bind(obj)`, envolver en una arrow (`() => obj.doble()`), o usar una arrow como método cuando quieras el `this` léxico.
- **Creer que JS no es OO** → causa: buscar clases "de verdad" y no encontrarlas antes de ES2015 → solución: entender que la OO de JS es por prototipos y delegación; es plenamente OO, solo que con otro modelo que el de clases.
- **Pensar que `class` cambió el modelo** → causa: asumir que `class` introdujo herencia "real" como en Java → solución: recordar que `class` es azúcar; `Obj.prototype` sigue ahí y `extends` sigue encadenando prototipos. Depurar mirando la cadena real, no la fachada.
- **Mutar `Object.prototype` o prototipos ajenos** → causa: añadir métodos a prototipos globales para "comodidad", afectando a todos los objetos y a librerías de terceros (*monkey patching*) → solución: no tocar prototipos que no son tuyos; extiende con funciones propias o composición.

## ❓ Preguntas frecuentes

- **¿Prototipos o clases en JS?** Las dos cosas son la misma: `class` es azúcar sintáctico sobre prototipos. Al escribir una clase, sus métodos acaban en `Prototipo.prototype` y la herencia con `extends` encadena prototipos. Elige la sintaxis que aclare tu intención, pero sabe que por debajo siempre hay delegación.
- **¿Qué lenguajes usan prototipos?** JavaScript, Self (el pionero) y Lua (vía *metatables*). La inmensa mayoría —Java, C#, Python, Ruby, C++, Go, Rust— usa el modelo de clases o de tipos con métodos.
- **¿Por qué `this` a veces es `undefined`?** Porque en JavaScript `this` lo fija la forma de la llamada, no la definición del método. Si el método viaja separado de su objeto, pierde el receptor; en modo estricto eso deja `this` como `undefined` y `this.valor` falla. Es el motivo de existir de `bind` y de las funciones flecha.
- **¿La delegación por prototipos cuesta rendimiento?** Cada acceso puede recorrer la cadena, pero los motores modernos (V8) optimizan con *inline caches* y "formas" ocultas de objeto, de modo que en la práctica es rápido. El coste real aparece con cadenas muy largas o mutaciones frecuentes de la forma del objeto.

## 🔗 Referencias

**Libros de la parte:**

- P. Van Roy y S. Haridi — *Concepts, Techniques, and Models of Computer Programming* (MIT Press).
- H. Abelson y G. J. Sussman — *Structure and Interpretation of Computer Programs* (2ª ed., MIT Press).
- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson).

**Libros de los lenguajes del núcleo:**

- L. Ramalho — *Fluent Python* (2ª ed., O'Reilly).
- M. Haverbeke — *Eloquent JavaScript* (3ª ed.) — [gratis online](https://eloquentjavascript.net/). Cap. 6 (objetos, métodos, prototipos y `class` como azúcar).
- B. Cherny — *Programming TypeScript* (O'Reilly).
- J. Bloch — *Effective Java* (3ª ed., Addison-Wesley).
- J. Skeet — *C# in Depth* (4ª ed., Manning).
- A. Donovan y B. Kernighan — *The Go Programming Language* (Addison-Wesley).
- S. Klabnik y C. Nichols — *The Rust Programming Language* — [gratis online](https://doc.rust-lang.org/book/).
- B. Kernighan y D. Ritchie — *The C Programming Language* (2ª ed., Prentice Hall).
- C. J. Date — *SQL and Relational Theory* (3ª ed., O'Reilly).
- J. Lockhart — *Modern PHP* (O'Reilly).
- D. Ungar y R. B. Smith — *Self: The Power of Simplicity* (OOPSLA 1987). Origen del modelo de prototipos.

---

> [⏮️ Clase 112](../../parte-7-paradigmas/112-interfaces-traits-y-clases-abstractas/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 114 ⏭️](../../parte-7-paradigmas/114-funcional-i-inmutabilidad-y-funciones-puras/README.md)
