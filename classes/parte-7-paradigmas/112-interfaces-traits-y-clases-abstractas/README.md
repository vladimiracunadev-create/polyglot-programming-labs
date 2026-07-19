# Clase 112 — Interfaces, traits y clases abstractas

> Parte **7 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Una interfaz es la respuesta de la programación a una pregunta muy antigua: **¿cómo desacoplo lo que un cliente necesita de cómo alguien decide dárselo?** La clase anterior mostró que el polimorfismo permite un nombre y muchos comportamientos; esta clase da el paso siguiente y hace explícito el **contrato**. Cuando declaras que `Forma` tiene un método `area()`, estás firmando una promesa: cualquier tipo que se declare `Forma` sabrá calcular su área, y cualquier código que reciba una `Forma` puede pedirla sin saber si es un cuadrado, un rectángulo o un círculo que aún no existe. Sebesta (cap. 12) presenta los **tipos abstractos** como el instrumento con el que un lenguaje separa la *especificación* de una operación de su *implementación*, y las interfaces son la forma más pura de esa separación: contrato sin una sola línea de código.

El objetivo es que aprendas a **programar contra la interfaz, no contra la implementación**. Es fácil escribir código que dependa de `Cuadrado` directamente; lo valioso es escribir código que dependa solo de `Forma` y siga funcionando cuando mañana aparezca un `Triangulo`. Ese hábito es el que sostiene los sistemas grandes: reduce el acoplamiento, hace las piezas sustituibles y convierte "añadir una figura" en escribir un tipo nuevo en lugar de editar el existente. Es, en la práctica, el principio abierto/cerrado —abierto a extensión, cerrado a modificación— hecho concreto.

Un segundo objetivo es distinguir tres herramientas que la gente confunde: **interfaz**, **trait** y **clase abstracta**. Las tres definen contratos, pero difieren en cuánto pueden aportar además del contrato. Una interfaz clásica es contrato puro; un trait de Rust (o una interfaz moderna de Java/Kotlin) puede traer métodos con implementación por defecto; una clase abstracta puede además guardar estado compartido. Elegir bien entre ellas —y respetar el **principio de sustitución de Liskov**, que exige que un subtipo pueda usarse en todo lugar donde se espera el supertipo sin romper el comportamiento— es lo que separa un diseño que envejece bien de uno que se agrieta.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Definir un contrato (interfaz) y varias implementaciones.
2. Programar contra la interfaz, no la implementación.
3. Distinguir interfaz de clase abstracta.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Interfaz/trait | Un contrato sin implementación |
| 2 | Implementar | Cumplir el contrato |
| 3 | Programar contra la interfaz | Desacoplar del tipo concreto |

## 📖 Definiciones y características

- **Interfaz** — conjunto de métodos que un tipo promete implementar. Clave: contrato sin código.
- **Trait** — el equivalente en Rust; puede llevar métodos por defecto. Clave: composición de comportamiento.
- **Clase abstracta** — clase incompleta que otras extienden. Clave: contrato + estado parcial.

La idea que une a las tres es la que Sebesta (cap. 12) llama **separar la especificación de la implementación**. Un tipo abstracto describe *qué* puede hacerse con un objeto —qué mensajes entiende— sin comprometerse con *cómo* lo hace. El cliente programa contra esa descripción y queda inmune a los cambios internos de cada implementación. Aquí está la raíz de la ocultación de información de Parnas: cuanto menos sepa el cliente del tipo concreto, más libremente puede evolucionar ese tipo. La interfaz es la frontera que hace posible ese olvido deliberado.

El criterio formal que gobierna cuándo un tipo puede cumplir un contrato es el **principio de sustitución de Liskov (LSP)**: si `S` es subtipo de `T`, todo programa correcto que use `T` debe seguir siendo correcto al recibir un `S`. No basta con que `Cuadrado` tenga un método `area()`; debe comportarse como una `Forma` de verdad, sin exigir más ni prometer menos que el contrato. Violar Liskov —el ejemplo clásico es hacer `Cuadrado` subtipo de `Rectangulo` y descubrir que "cambiar el ancho" ya no significa lo mismo— produce código que compila pero rompe suposiciones del cliente. Por eso el contrato no es solo una lista de firmas: es también un conjunto de expectativas de comportamiento.

La distinción entre interfaz y clase abstracta se reduce a **qué puede aportar cada una además del contrato**. La interfaz clásica (Java histórico, Go) es contrato puro: solo firmas, sin estado ni código. La clase abstracta puede llevar estado compartido y métodos ya implementados, a costa de imponer herencia —y en lenguajes de herencia simple, gastar el único "espacio de padre" disponible—. En medio está el **trait** de Rust (y las interfaces modernas de Java 8+ o Kotlin), que permite métodos por defecto: comparten comportamiento sin arrastrar estado, lo que Sebesta y la comunidad de Rust presentan como una vía para la reutilización sin los problemas de la herencia múltiple de estado. Elegir entre ellas es elegir cuánto compromiso quieres imponer a quien implemente.

## 🧩 Situación

Piensa en el motor de un editor de gráficos vectoriales. Debe medir el área de cada figura del lienzo para ordenarlas, cobrar por superficie o decidir cuál está encima. El editor no quiere un `if` gigante que pregunte "¿es cuadrado?, ¿es rectángulo?, ¿es elipse?" cada vez que necesita un área: eso lo condenaría a modificarse con cada figura nueva. En su lugar define un contrato —`Forma` con `area()`— y trabaja siempre contra él. Recibe una lista de `Forma`, llama `figura.area()` sobre cada una y suma.

El día que el equipo añade un triángulo, no toca el motor: escribe una clase `Triangulo` que implementa `Forma` y el sistema la acepta sin cambios. Esa es la promesa que verifican los tres casos de esta clase —`cuadrado 5 → area=25`, `rectangulo 3 4 → area=12`, `cuadrado 6 → area=36`—: dos implementaciones distintas del mismo contrato, usadas por un código que jamás pregunta el tipo concreto.

## 🧮 Modelo

- **Entrada** (stdin): una línea: `cuadrado <lado>` o `rectangulo <ancho> <alto>`
- **Salida** (stdout): `area=<área>`
- **Regla:** cada figura implementa area() a su manera

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `cuadrado 5` | `area=25` |
| `rectangulo 3 4` | `area=12` |
| `cuadrado 6` | `area=36` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER figura ; f: Forma ; ESCRIBIR f.area()
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys


class Cuadrado:
    def __init__(self, l):
        self.l = l
    def area(self):
        return self.l * self.l


class Rectangulo:
    def __init__(self, a, b):
        self.a, self.b = a, b
    def area(self):
        return self.a * self.b


t = sys.stdin.readline().split()
f = Cuadrado(int(t[1])) if t[0] == "cuadrado" else Rectangulo(int(t[1]), int(t[2]))
print(f"area={f.area()}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

class Cuadrado { constructor(l) { this.l = l; } area() { return this.l * this.l; } }
class Rectangulo { constructor(a, b) { this.a = a; this.b = b; } area() { return this.a * this.b; } }

const t = readFileSync(0, "utf8").trim().split(/\s+/);
const f = t[0] === "cuadrado" ? new Cuadrado(Number(t[1])) : new Rectangulo(Number(t[1]), Number(t[2]));
console.log(`area=${f.area()}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

interface Forma { area(): number; }
class Cuadrado implements Forma { constructor(private l: number) {} area() { return this.l * this.l; } }
class Rectangulo implements Forma { constructor(private a: number, private b: number) {} area() { return this.a * this.b; } }

const t: string[] = readFileSync(0, "utf8").trim().split(/\s+/);
const f: Forma = t[0] === "cuadrado" ? new Cuadrado(Number(t[1])) : new Rectangulo(Number(t[1]), Number(t[2]));
console.log(`area=${f.area()}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    interface Forma { long area(); }
    static class Cuadrado implements Forma {
        long l; Cuadrado(long l) { this.l = l; }
        public long area() { return l * l; }
    }
    static class Rectangulo implements Forma {
        long a, b; Rectangulo(long a, long b) { this.a = a; this.b = b; }
        public long area() { return a * b; }
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] t = br.readLine().trim().split("\\s+");
        Forma f = t[0].equals("cuadrado")
                ? new Cuadrado(Long.parseLong(t[1]))
                : new Rectangulo(Long.parseLong(t[1]), Long.parseLong(t[2]));
        System.out.println("area=" + f.area());
    }
}
```

### C# · `dotnet run`

```csharp
using System;

string[] t = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
IForma f = t[0] == "cuadrado"
    ? new Cuadrado(long.Parse(t[1]))
    : new Rectangulo(long.Parse(t[1]), long.Parse(t[2]));
Console.WriteLine($"area={f.Area()}");

interface IForma { long Area(); }
class Cuadrado : IForma { long l; public Cuadrado(long l) { this.l = l; } public long Area() => l * l; }
class Rectangulo : IForma { long a, b; public Rectangulo(long a, long b) { this.a = a; this.b = b; } public long Area() => a * b; }
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

type Forma interface {
	area() int64
}

type Cuadrado struct{ l int64 }
type Rectangulo struct{ a, b int64 }

func (c Cuadrado) area() int64   { return c.l * c.l }
func (r Rectangulo) area() int64 { return r.a * r.b }

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	t := strings.Fields(line)
	var f Forma
	if t[0] == "cuadrado" {
		l, _ := strconv.ParseInt(t[1], 10, 64)
		f = Cuadrado{l}
	} else {
		a, _ := strconv.ParseInt(t[1], 10, 64)
		b, _ := strconv.ParseInt(t[2], 10, 64)
		f = Rectangulo{a, b}
	}
	fmt.Printf("area=%d\n", f.area())
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

trait Forma {
    fn area(&self) -> i64;
}

struct Cuadrado(i64);
struct Rectangulo(i64, i64);

impl Forma for Cuadrado { fn area(&self) -> i64 { self.0 * self.0 } }
impl Forma for Rectangulo { fn area(&self) -> i64 { self.0 * self.1 } }

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let t: Vec<&str> = s.split_whitespace().collect();
    let f: Box<dyn Forma> = if t[0] == "cuadrado" {
        Box::new(Cuadrado(t[1].parse().unwrap()))
    } else {
        Box::new(Rectangulo(t[1].parse().unwrap(), t[2].parse().unwrap()))
    };
    println!("area={}", f.area());
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char tipo[32];
    if (scanf("%31s", tipo) != 1) return 1;
    long area;
    if (strcmp(tipo, "cuadrado") == 0) {
        long l; if (scanf("%ld", &l) != 1) return 1; area = l * l;
    } else {
        long a, b; if (scanf("%ld %ld", &a, &b) != 2) return 1; area = a * b;
    }
    printf("area=%ld\n", area);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: sin interfaces; se usa CASE.
WITH formas(tipo, a, b) AS (VALUES ('cuadrado', 5, 0))
SELECT printf('area=%d', CASE WHEN tipo = 'cuadrado' THEN a * a ELSE a * b END) AS resultado FROM formas;
```

### PHP · `php main.php`

```php
<?php
interface Forma { public function area(): int; }
class Cuadrado implements Forma {
    public function __construct(private int $l) {}
    public function area(): int { return $this->l * $this->l; }
}
class Rectangulo implements Forma {
    public function __construct(private int $a, private int $b) {}
    public function area(): int { return $this->a * $this->b; }
}

$t = preg_split('/\s+/', trim(fgets(STDIN)));
$f = $t[0] === "cuadrado" ? new Cuadrado((int) $t[1]) : new Rectangulo((int) $t[1], (int) $t[2]);
echo "area=" . $f->area() . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🧪 Laboratorio guiado — recorrido del código

Tomemos el primer caso de [`casos.json`](casos.json): la entrada `cuadrado 5` que debe imprimir `area=25`. El archivo declara además `rectangulo 3 4 → area=12` y `cuadrado 6 → area=36`. El verificador pasa cada `stdin` y compara con el `esperado`. Fíjate en que el *cliente* —la línea que decide qué figura crear y le pide el área— es el mismo para cuadrado y rectángulo: ahí vive la abstracción.

En **Python**, `Cuadrado` y `Rectangulo` son clases con un método `area()` cada una. La línea que resuelve todo es `f = Cuadrado(int(t[1])) if t[0] == "cuadrado" else Rectangulo(int(t[1]), int(t[2]))`: según la primera palabra construye una figura u otra, pero la asigna a la misma variable `f`. Luego `print(f"area={f.area()}")` no vuelve a preguntar el tipo; confía en que `f`, sea lo que sea, sabe calcular su área. Para `cuadrado 5` construye `Cuadrado(5)`, cuyo `area()` devuelve `5 * 5 = 25`, y sale `area=25`. Python no exige declarar una interfaz `Forma`: le basta con que ambas respondan a `area()` (*duck typing*). La abstracción existe en la disciplina del programador, no en una firma.

**TypeScript** hace visible ese contrato que Python deja implícito. Declara `interface Forma { area(): number; }` y ambas clases lo firman con `implements Forma`. La variable se anota `const f: Forma = ...`, de modo que el compilador solo permite llamar métodos que `Forma` promete. Si un día `Cuadrado` olvidara `area()`, el error saltaría al compilar, no al ejecutar `cuadrado 5`. El resultado en ejecución es idéntico —`this.l * this.l` con `l=5` da `25`—, pero el contrato está ahora verificado por la máquina. Esta es la diferencia central que Sebesta subraya: el tipo abstracto convertido en garantía estática.

**Go** aporta el matiz más interesante. Define `type Forma interface { area() int64 }`, pero `Cuadrado` y `Rectangulo` **nunca dicen** que implementan `Forma`: simplemente tienen un método `area() int64`, y con eso Go los considera `Forma` automáticamente. Es tipado **estructural**. En `main`, la variable `var f Forma` recibe `Cuadrado{l}` o `Rectangulo{a, b}` según la entrada, y `f.area()` despacha al método correcto. Para `rectangulo 3 4`, construye `Rectangulo{3, 4}` y `area()` devuelve `3 * 4 = 12`. El contrato se cumple sin ceremonia; el compilador lo verifica igual, pero la relación tipo-interfaz es implícita.

Los tres casos convergen en la salida que exige `casos.json`: `area=25`, `area=12`, `area=36`. Lo revelador es que el código cliente —la línea que pide `.area()`— es indiferente al tipo concreto en todas las implementaciones nominales (Java, C#, TS, PHP), estructurales (Go) o basadas en traits (Rust, con `Box<dyn Forma>`). El **SQL** es de nuevo la excepción declarada: no hay interfaz ni objeto, solo un `CASE WHEN tipo = 'cuadrado' THEN a * a ELSE a * b END` sobre una fila; el verificador lo marca como *ilustrativo* porque produce el número correcto sin ningún contrato. Contrastar ambos extremos deja claro qué compra la interfaz: no un resultado distinto, sino un cliente que no cambia cuando cambian las implementaciones.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `interface` (Java/C#/Go/TS/PHP), `trait` (Rust), duck typing (Python/JS). |
| Semántica | El contrato desacopla el uso del tipo concreto. |
| Paradigmática | SQL usa CASE; no hay interfaces. |

La diferencia que más pesa en la práctica es **nominal frente a estructural**. En Java, C#, TypeScript y PHP un tipo es `Forma` solo si lo declara con `implements`: la relación es explícita y buscable. En Go un tipo es `Forma` por el mero hecho de tener los métodos correctos, sin declararlo. La ventaja del modelo estructural es que puedes hacer que tipos ajenos —de una librería que no controlas— satisfagan tus interfaces sin tocarlos; la desventaja es que la intención queda menos visible y una coincidencia accidental de firmas puede satisfacer un contrato sin querer. Python y JavaScript llevan esto al extremo del *duck typing* sin verificación alguna: el "contrato" solo existe mientras el objeto responda al método en ejecución.

La segunda diferencia es **qué puede aportar el contrato además de las firmas**. El `trait` de Rust admite métodos por defecto, así que un contrato puede traer comportamiento reutilizable sin imponer herencia de estado; Java 8+ lo imita con métodos `default` en interfaces. Las clases abstractas de C++, Java o C# van más lejos y comparten estado, pero cuestan el único cupo de herencia en lenguajes de herencia simple. Go, deliberadamente, no ofrece ni herencia ni clases abstractas: fuerza a componer mediante *embedding* e interfaces pequeñas. Esa austeridad es una postura de diseño, no una carencia: empuja hacia interfaces mínimas y enfocadas, justo lo que recomienda el principio de segregación de interfaces.

## 🧬 El concepto en la familia

En Kotlin las interfaces admiten métodos por defecto y propiedades abstractas, difuminando la vieja frontera con las clases abstractas. En C++ el equivalente son las clases con métodos virtuales puros (`= 0`), y la herencia múltiple obliga a lidiar con el "problema del diamante" que Java evitó prohibiéndola para el estado. Scala populariza los *traits* como unidades de composición apilable (linearización). Swift construye buena parte de su biblioteca estándar sobre *protocols* con extensiones por defecto —"programación orientada a protocolos"—. Haskell resuelve el mismo problema sin objetos, mediante *type classes*. Todos responden a la misma necesidad que aquí ejercitas: nombrar un contrato y programar contra él, para que las implementaciones puedan cambiar sin arrastrar a sus clientes.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 112
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Depender de la implementación concreta** → causa: declarar variables y parámetros con el tipo `Cuadrado` en lugar de `Forma`, de modo que el código se acopla al detalle y hay que editarlo con cada figura nueva → solución: programar contra la interfaz; anota siempre el tipo más abstracto que te sirva.
- **Interfaz demasiado grande** → causa: meter en un solo contrato todo lo que "podría" hacer una figura (dibujar, serializar, medir, animar), obligando a cada implementación a rellenar métodos que no le importan → solución: interfaces pequeñas y enfocadas (segregación de interfaces); es más fácil componer dos contratos chicos que descomponer uno enorme.
- **Violar Liskov al forzar una jerarquía** → causa: hacer `Cuadrado` subtipo de `Rectangulo` porque "un cuadrado es un rectángulo", y descubrir que `setAncho` rompe la invariante del cuadrado → solución: no dejes que la intuición del lenguaje natural dicte los subtipos; comprueba que el subtipo se comporte de verdad como el supertipo en todo contexto.
- **Confundir tener el método con cumplir el contrato** → causa: en lenguajes estructurales o con *duck typing*, un tipo satisface la interfaz por coincidencia de firmas aunque su semántica sea otra → solución: documenta las expectativas de comportamiento del contrato, no solo las firmas, y en lenguajes nominales usa `implements` para declarar la intención explícitamente.

## ❓ Preguntas frecuentes

- **¿Interfaz o clase abstracta?** Interfaz cuando solo necesitas un contrato puro y quieres que un tipo pueda cumplir varios a la vez; clase abstracta cuando además hay estado o código común que todas las subclases comparten. En herencia simple, recuerda que la clase abstracta consume tu único "padre", mientras que puedes implementar muchas interfaces.
- **¿Go tiene interfaces?** Sí, y se satisfacen de forma implícita (tipado estructural): un tipo cumple una interfaz por tener sus métodos, sin declararlo. Esto permite que tipos que no controlas satisfagan tus contratos, y empuja a definir interfaces pequeñas justo donde se consumen.
- **¿Qué gana un trait de Rust frente a una interfaz clásica?** Puede traer métodos por defecto, así que comparte comportamiento sin imponer herencia de estado, y el compilador verifica su cumplimiento. Es la vía de Rust para reutilizar código evitando los problemas de la herencia múltiple.
- **¿Por qué "programar contra la interfaz" si igual funciona con la clase concreta?** Porque el objetivo no es que funcione hoy, sino que siga funcionando cuando aparezca una implementación nueva. Depender del contrato hace el cambio local (una clase más) en vez de global (editar cada cliente). Es el principio abierto/cerrado en acción.

## 🔗 Referencias

**Libros de la parte:**

- P. Van Roy y S. Haridi — *Concepts, Techniques, and Models of Computer Programming* (MIT Press).
- H. Abelson y G. J. Sussman — *Structure and Interpretation of Computer Programs* (2ª ed., MIT Press).
- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson). Cap. 12 (tipos abstractos, clases abstractas, separación contrato/implementación).
- B. Liskov y J. Guttag — *Program Development in Java: Abstraction, Specification, and Object-Oriented Design* (Addison-Wesley). Origen del principio de sustitución.

**Libros de los lenguajes del núcleo:**

- L. Ramalho — *Fluent Python* (2ª ed., O'Reilly).
- M. Haverbeke — *Eloquent JavaScript* (3ª ed.) — [gratis online](https://eloquentjavascript.net/).
- B. Cherny — *Programming TypeScript* (O'Reilly).
- J. Bloch — *Effective Java* (3ª ed., Addison-Wesley). Ítem 20: "prefiere interfaces a clases abstractas".
- J. Skeet — *C# in Depth* (4ª ed., Manning).
- A. Donovan y B. Kernighan — *The Go Programming Language* (Addison-Wesley).
- S. Klabnik y C. Nichols — *The Rust Programming Language* — [gratis online](https://doc.rust-lang.org/book/).
- B. Kernighan y D. Ritchie — *The C Programming Language* (2ª ed., Prentice Hall).
- C. J. Date — *SQL and Relational Theory* (3ª ed., O'Reilly).
- J. Lockhart — *Modern PHP* (O'Reilly).

---

> [⏮️ Clase 111](../../parte-7-paradigmas/111-herencia-composicion-y-polimorfismo/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 113 ⏭️](../../parte-7-paradigmas/113-oo-basado-en-prototipos-javascript/README.md)
