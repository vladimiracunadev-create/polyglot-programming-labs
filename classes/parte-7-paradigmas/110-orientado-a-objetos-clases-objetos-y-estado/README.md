# Clase 110 — Orientado a objetos: clases, objetos y estado

> Parte **7 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

La **orientación a objetos** responde a una pregunta que las clases anteriores dejaron abierta: si el estado mutable es tan poderoso como peligroso, ¿cómo lo domesticamos? La respuesta del paradigma OO es *encapsular*: en lugar de dejar el estado suelto en variables que cualquiera puede tocar, se agrupa junto con las operaciones que tienen derecho a modificarlo, formando una unidad —el objeto— que protege sus datos y solo se deja manipular a través de sus métodos. Van Roy dedica el capítulo 6 de *Concepts, Techniques, and Models* a este *estado explícito* y a la *abstracción de datos*, y define el objeto con precisión: es la agrupación de un estado interno con un conjunto de operaciones que lo consultan y lo transforman. El contador de esta clase es esa definición reducida a su mínima expresión: un dato (`cuenta`) y una operación (`incrementar`) que viven juntos.

El concepto tiene una raíz honda en SICP 3.1, donde Abelson y Sussman muestran que un objeto no es más que estado local con asignación: una variable que persiste entre invocaciones y a la que solo se accede mediante procedimientos que la capturan en su ámbito. Cuando escribes `c = Contador()` y luego llamas `c.incrementar()` tres veces, el objeto `c` *recuerda* su cuenta entre llamadas —empezó en 0 y ahora vale 3—. Esa memoria persistente es la misma que da poder al modelo imperativo, pero aquí está ordenada: cada objeto tiene su propio estado, aislado del de los demás. Dos contadores no se pisan porque cada uno lleva su cuenta.

En esta clase practicarás la tríada fundacional de la OO —clase, objeto y estado— construyendo un contador que se incrementa n veces. Sebesta (capítulos 11 y 12, soporte para la abstracción de datos y la orientación a objetos) es la referencia sistemática de cómo cada lenguaje del núcleo materializa clases, instancias y métodos, incluidos los que —como Go y Rust— logran lo esencial de la OO sin la palabra `class`. El objetivo es que veas el objeto no como una moda sintáctica, sino como la unión disciplinada de datos y comportamiento.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Definir una clase con estado y métodos.
2. Crear un objeto y cambiar su estado.
3. Reconocer la unión de datos y comportamiento.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Clase y objeto | Molde e instancia |
| 2 | Estado | Datos del objeto |
| 3 | Método | Comportamiento que actúa sobre el estado |

## 📖 Definiciones y características

- **Objeto** — instancia que agrupa estado y comportamiento. Clave: datos + métodos juntos.
- **Clase** — molde que define objetos. Clave: describe estado y métodos.
- **Método** — función asociada a un objeto que opera sobre su estado. Clave: `contador.incrementar()`.

La distinción entre **clase** y **objeto** es la primera que hay que interiorizar, y Sebesta la formula con claridad: la clase es una descripción, un molde que declara qué estado tendrán los objetos y qué métodos podrán ejecutar; el objeto es una *instancia* concreta creada a partir de ese molde, con su propia copia del estado. La clase `Contador` no cuenta nada; es la instancia `c = Contador()` la que tiene una `cuenta` real que evoluciona. De un mismo molde puedes fabricar muchos objetos independientes, cada uno con su historia. Esta separación es lo que permite razonar sobre el comportamiento (en la clase) por separado de los datos concretos (en cada objeto).

El corazón conceptual, según Van Roy, es la *abstracción de datos*: el objeto expone qué se puede hacer con él —su interfaz de métodos— y oculta cómo lo hace por dentro. Quien usa el contador llama `incrementar()` sin saber ni necesitar saber que por dentro hay un `cuenta += 1`. Esto conecta directamente con la modularidad de la clase anterior, pero da un paso más: mientras el procedimiento agrupaba comportamiento, el objeto agrupa comportamiento *y* el estado sobre el que ese comportamiento actúa. SICP 3.1 lo describe como la transición del estilo en el que los datos y los procedimientos están separados al estilo en el que se empaquetan juntos, con el estado protegido dentro del ámbito del objeto.

Esa unión tiene una consecuencia práctica enorme: los objetos modelan *identidad* y *tiempo*. Un objeto no es su valor actual, sino una entidad que mantiene su identidad aunque su estado cambie —el contador sigue siendo "el mismo contador" tras incrementarse—. Por eso la OO encaja tan bien con el mundo real, donde las cosas persisten mientras cambian, y por eso Van Roy la sitúa dentro del modelo con estado explícito: es la forma más estructurada de administrar el estado mutable que el imperativo introdujo.

## 🧩 Situación

Un carrito de compra que acumula productos, una cuenta bancaria cuyo saldo sube y baja, un contador de visitas: todos son entidades que *tienen estado y evolucionan con el tiempo*. Modelarlos con variables sueltas y funciones separadas funciona en lo pequeño, pero se vuelve frágil en cuanto hay muchos: nada impide que una parte lejana del código altere el saldo sin pasar por las reglas del negocio. La OO propone empaquetar cada entidad como un objeto que custodia su propio estado y solo lo deja cambiar a través de sus métodos. El objeto recuerda su estado entre llamadas, y esa memoria queda protegida dentro de él.

Aquí destilamos esa idea al ejemplo mínimo que la contiene entera: un contador que empieza en 0 y se incrementa n veces. El contrato de [`casos.json`](casos.json) fija tres casos (`5 → cuenta=5`, `0 → cuenta=0`, `3 → cuenta=3`; nótese que con `n=0` el contador nunca se incrementa y conserva su estado inicial). Definimos una clase `Contador` con un dato `cuenta` y un método `incrementar`, creamos una instancia, la incrementamos n veces y leemos su estado final. Es OO en una cáscara de nuez: estado encapsulado más comportamiento que lo modifica.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n` (número de incrementos)
- **Salida** (stdout): `cuenta=<n>`
- **Regla:** contador incrementado n veces desde 0

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `cuenta=5` |
| `0` | `cuenta=0` |
| `3` | `cuenta=3` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
c <- Contador() ; REPETIR n veces: c.incrementar() ; ESCRIBIR c.cuenta
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys


class Contador:
    def __init__(self):
        self.cuenta = 0

    def incrementar(self):
        self.cuenta += 1


n = int(sys.stdin.readline())
c = Contador()
for _ in range(n):
    c.incrementar()
print(f"cuenta={c.cuenta}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

class Contador {
  constructor() {
    this.cuenta = 0;
  }
  incrementar() {
    this.cuenta++;
  }
}

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
const c = new Contador();
for (let i = 0; i < n; i++) c.incrementar();
console.log(`cuenta=${c.cuenta}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

class Contador {
  cuenta = 0;
  incrementar(): void {
    this.cuenta++;
  }
}

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
const c = new Contador();
for (let i = 0; i < n; i++) c.incrementar();
console.log(`cuenta=${c.cuenta}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    static class Contador {
        int cuenta = 0;
        void incrementar() { cuenta++; }
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        Contador c = new Contador();
        for (int i = 0; i < n; i++) c.incrementar();
        System.out.println("cuenta=" + c.cuenta);
    }
}
```

### C# · `dotnet run`

```csharp
using System;

int n = int.Parse(Console.In.ReadToEnd().Trim());
var c = new Contador();
for (int i = 0; i < n; i++) c.Incrementar();
Console.WriteLine($"cuenta={c.Cuenta}");

class Contador {
    public int Cuenta { get; private set; }
    public void Incrementar() => Cuenta++;
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

type Contador struct {
	cuenta int
}

func (c *Contador) incrementar() {
	c.cuenta++
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	n, _ := strconv.Atoi(strings.TrimSpace(line))
	c := &Contador{}
	for i := 0; i < n; i++ {
		c.incrementar()
	}
	fmt.Printf("cuenta=%d\n", c.cuenta)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

struct Contador {
    cuenta: i64,
}

impl Contador {
    fn nuevo() -> Self {
        Contador { cuenta: 0 }
    }
    fn incrementar(&mut self) {
        self.cuenta += 1;
    }
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let mut c = Contador::nuevo();
    for _ in 0..n {
        c.incrementar();
    }
    println!("cuenta={}", c.cuenta);
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

struct Contador {
    long cuenta;
};

void incrementar(struct Contador *c) {
    c->cuenta++;
}

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    struct Contador c = {0};
    for (long i = 0; i < n; i++) incrementar(&c);
    printf("cuenta=%ld\n", c.cuenta);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL no tiene objetos con estado; el contador es el propio valor.
WITH nums(n) AS (VALUES (5), (0), (3))
SELECT printf('cuenta=%d', n) AS resultado FROM nums;
```

### PHP · `php main.php`

```php
<?php
class Contador {
    public int $cuenta = 0;
    public function incrementar() {
        $this->cuenta++;
    }
}

$n = (int) trim(fgets(STDIN));
$c = new Contador();
for ($i = 0; $i < $n; $i++) {
    $c->incrementar();
}
echo "cuenta={$c->cuenta}\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🧪 Laboratorio guiado — recorrido del código

Sigamos el caso `3 → cuenta=3` de [`casos.json`](casos.json) para ver nacer un objeto, cambiar su estado y consultarlo.

En **Python**, el bloque `class Contador:` es el molde. Su método `__init__` es el *constructor*: cuando escribes `c = Contador()`, Python crea una instancia y ejecuta `self.cuenta = 0`, dando a *ese* objeto su estado inicial. `self` es la referencia al objeto concreto, y `self.cuenta` es su atributo, el estado encapsulado. El método `incrementar` hace `self.cuenta += 1`: opera sobre el estado del objeto que lo recibe. La parte principal lee `n = int(sys.stdin.readline())` (aquí, 3), crea `c = Contador()` con `cuenta` en 0, y el bucle `for _ in range(n): c.incrementar()` llama al método tres veces. La clave del paradigma está aquí: entre una llamada y la siguiente, `c` *recuerda* su cuenta —tras la primera vale 1, tras la segunda 2, tras la tercera 3—. Ese recuerdo persistente es el estado local con asignación de SICP 3.1. Finalmente `print(f"cuenta={c.cuenta}")` consulta el estado final y emite `cuenta=3`.

**Rust** ofrece el contraste más instructivo, porque logra lo mismo *sin la palabra `class`*. Define `struct Contador { cuenta: i64 }` —solo el estado— y luego un bloque `impl Contador` que le adjunta comportamiento: `fn nuevo() -> Self` es una función asociada que cumple el papel del constructor (`Contador { cuenta: 0 }`), e `fn incrementar(&mut self)` es un método que recibe una *referencia mutable* al objeto, `&mut self`, sin la cual el compilador no permitiría modificar `self.cuenta`. Esa exigencia explícita de mutabilidad es pura filosofía Rust: mutar estado es un acto que debe declararse. En `main`, `let mut c = Contador::nuevo()` crea la instancia (mutable, de nuevo explícito) y `for _ in 0..n { c.incrementar(); }` la incrementa. Con `n=3`, `c.cuenta` recorre 0→1→2→3, y `println!("cuenta={}", c.cuenta)` imprime `cuenta=3`. La lección es que "objeto" no es sintaxis de `class`, sino la unión de estado (`struct`) y comportamiento (`impl`) sobre una identidad que persiste.

Los demás lenguajes reparten estas mismas piezas a su manera. **Java** anida una `static class Contador` con campo `int cuenta` y método `void incrementar()`, instanciada con `new`; **C#** usa una propiedad con *setter privado* (`public int Cuenta { get; private set; }`), que encapsula el estado impidiendo que se modifique desde fuera salvo por el método `Incrementar`; **JavaScript** y **TypeScript** usan `class ... { constructor() ... }` con `this.cuenta`; **Go** replica el patrón de Rust con `type Contador struct` y un método sobre puntero `func (c *Contador) incrementar()` —el puntero es necesario para que el incremento afecte al objeto real y no a una copia—; **PHP** declara `class Contador` con `public int $cuenta` y `$this->cuenta++`. **C** llega hasta donde puede sin OO nativa: una `struct Contador` y una función libre `void incrementar(struct Contador *c)` que recibe la dirección del objeto; es la OO "a mano", exactamente como Van Roy explica que el objeto se reduce a estado más operaciones. **SQL** es el forastero: no tiene objetos con estado, así que su bloque simplemente proyecta el valor `n` —por eso incrusta los datos y el verificador lo marca *ilustrativo*—. Ejecuta `python scripts/verificar_equivalencia.py 110` para confirmar que todas convergen en las salidas de `casos.json`.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `class` (Python/Java/C#/PHP), `struct`+métodos (Go/Rust), objeto (JS). |
| Semántica | El objeto conserva su estado entre llamadas a métodos. |
| Paradigmática | SQL no tiene objetos con estado; opera sobre datos. |

La diferencia semántica más profunda entre los lenguajes es *cómo un método accede al objeto sobre el que actúa*. Python y PHP lo reciben como parámetro explícito (`self`, `$this`); Java, C# y JavaScript lo hacen implícito. Go y Rust exigen decidir si el método recibe el objeto por valor (una copia) o por referencia: aquí ambos usan puntero/`&mut self` porque incrementar una copia no cambiaría el original —un error clásico y sutil si se olvida—. Rust va más allá y hace del control de mutabilidad parte del tipo: `&mut self` frente a `&self` distingue en la firma si el método puede o no alterar el estado, algo que ningún otro lenguaje del núcleo verifica en tiempo de compilación. En el eje del encapsulamiento, C# es el más estricto de este ejemplo con su *setter* privado, que impide modificar `Cuenta` salvo por el método; Python y JavaScript, en cambio, dejan `cuenta` accesible desde fuera, confiando en la convención más que en el compilador. Y en el extremo, C demuestra que la OO es un *estilo*, no una característica: con `struct` y funciones que reciben un puntero se obtiene estado encapsulado y comportamiento asociado, aunque el lenguaje no tenga la palabra `class`.

## 🧬 El concepto en la familia

La orientación a objetos se materializa en un abanico sorprendentemente amplio de formas dentro del núcleo. En un extremo están los lenguajes "objeto-primero" como Java y C#, donde casi todo vive dentro de una clase y el `new` es el gesto cotidiano; Ruby (fuera del núcleo pero canónico) lleva esto al límite haciendo que *todo* sea un objeto, incluso los números. En el medio, Python, JavaScript, TypeScript y PHP ofrecen clases pero no las imponen: puedes mezclar objetos con funciones libres según convenga. En el otro extremo, Go y Rust prescinden de la palabra `class` por completo y reconstruyen la OO desde piezas más básicas: un `struct` que agrupa el estado y métodos adjuntos (`impl` en Rust, receptores en Go) que aportan el comportamiento. Esto confirma la tesis de Van Roy de que el objeto es un *concepto* —estado explícito más operaciones— y no una palabra clave: donde no hay `class`, un `struct` con métodos cumple exactamente el mismo papel. Incluso C, sin ningún soporte, permite emular objetos con `struct` y funciones que reciben un puntero, que es históricamente como se programaba "orientado a objetos" antes de que los lenguajes lo integraran. El paradigma, más que una característica, es una manera de organizar estado y comportamiento que cada lenguaje ofrece con más o menos ceremonia.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 110
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Estado compartido sin control** → causa: objetos que se pisan → solución: encapsular el estado en cada objeto
- **Confundir clase con objeto** → causa: molde vs. instancia → solución: la clase define; el objeto existe

## ❓ Preguntas frecuentes

- **¿Todo debe ser objeto?** No: la OO es una herramienta; a veces una función basta.
- **¿Go tiene clases?** No, pero structs con métodos ofrecen lo esencial de la OO.

## 🔗 Referencias

**Libros de la parte:**

- P. Van Roy y S. Haridi — *Concepts, Techniques, and Models of Computer Programming* (MIT Press).
- H. Abelson y G. J. Sussman — *Structure and Interpretation of Computer Programs* (2ª ed., MIT Press).
- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson).

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

> [⏮️ Clase 109](../../parte-7-paradigmas/109-procedimental-y-modular/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 111 ⏭️](../../parte-7-paradigmas/111-herencia-composicion-y-polimorfismo/README.md)
