# Clase 111 — Herencia, composición y polimorfismo

> Parte **7 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

El problema que resuelve la orientación a objetos no es "modelar el mundo con clases": es **eliminar los condicionales que preguntan de qué tipo es un valor**. Cuando tienes un `perro`, un `gato` y una `vaca`, la solución ingenua es un `if tipo == "perro" ... elif tipo == "gato" ...` que se repite en cada punto donde alguien necesita el sonido. El polimorfismo de subtipo invierte esa carga: en lugar de que quien llama decida, es el objeto quien conoce su propia respuesta. Escribes `animal.sonido()` una sola vez y el sistema, en tiempo de ejecución, encuentra la implementación correcta según el tipo real del objeto. Sebesta, en el capítulo 12 de *Concepts of Programming Languages*, llama a esto **enlace dinámico** (dynamic binding) y lo presenta como el rasgo que distingue la verdadera OO de un simple empaquetado de datos con funciones.

En esta clase practicarás las tres piezas que sostienen ese mecanismo y que conviene no confundir. La **herencia** deja que un tipo reutilice y especialice a otro (relación *es-un*). La **composición** construye un objeto a partir de otros que posee (relación *tiene-un*). Y el **polimorfismo** es lo que hace que un mismo nombre de método —`sonido`— produzca comportamientos distintos sin que el código cliente cambie. Las tres se estudian juntas porque los principiantes tienden a resolver con herencia problemas que la composición modela mejor, y porque el polimorfismo funciona igual de bien lo hayas obtenido por herencia, por interfaz o por *duck typing*.

El objetivo profundo es que salgas capaz de razonar sobre la pregunta que atraviesa toda esta parte del curso: **¿cuándo heredar y cuándo componer?** Van Roy y Haridi dedican el capítulo 7 de CTM a mostrar que la herencia es "una de las características más útiles pero también más peligrosas" del modelo con estado, porque acopla la subclase a los detalles internos de la superclase. Guardar esa tensión en mente —potencia frente a fragilidad— es lo que separa a quien usa objetos de quien los diseña.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Reconocer el polimorfismo (mismo método, distinto comportamiento).
2. Distinguir herencia de composición.
3. Despachar según el tipo real.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Herencia | Un tipo deriva de otro |
| 2 | Polimorfismo | Mismo método, comportamiento distinto |
| 3 | Composición | Construir con partes, alternativa a heredar |

## 📖 Definiciones y características

- **Herencia** — un tipo hereda estado/comportamiento de otro. Clave: reutiliza y especializa.
- **Polimorfismo** — el mismo método se comporta distinto según el tipo real. Clave: `animal.sonido()`.
- **Composición** — construir un objeto a partir de otros (tiene-un) en vez de heredar (es-un). Clave: más flexible.

El polimorfismo que aquí ejercitas es el **polimorfismo de subtipo** o de inclusión, uno de los cuatro que distingue la literatura (junto al paramétrico —los genéricos—, la sobrecarga *ad hoc* y la coerción). Su motor es el **despacho dinámico**: la decisión de qué código ejecutar no se toma al compilar sino al ejecutar, mirando el tipo real del objeto. Sebesta (cap. 12) lo explica con la mecánica de la *vtable* en lenguajes como C++ y Java: cada objeto polimórfico lleva un puntero a una tabla de métodos, y la llamada `animal.sonido()` es en realidad "busca en la tabla de este objeto la entrada `sonido` y salta ahí". Por eso el mismo texto fuente produce salidas distintas: el enlace se resuelve contra el objeto, no contra la variable.

Herencia y polimorfismo suelen aparecer juntos, pero **no son lo mismo**, y esta clase lo hace visible. En Python y JavaScript los tres animales ni siquiera comparten una superclase: cada clase define `sonido()` por su cuenta y el polimorfismo emerge por *duck typing* —"si responde a `sonido()`, sirve"—. En Java, C# o Rust el polimorfismo viaja sobre un contrato explícito (`interface Animal`, `trait Animal`). Ambos caminos llegan al mismo comportamiento; lo que cambia es cuánta comprobación hace el compilador antes de confiar en ti.

Aquí también asoma el principio de diseño que da nombre a la clase: **"favorecer la composición sobre la herencia"**, formulado por la Banda de los Cuatro (GoF) y respaldado por CTM (cap. 7). La herencia crea un acoplamiento fuerte y estático entre subclase y superclase; si la base cambia sus invariantes internas, las subclases pueden romperse sin haberse tocado —el célebre "problema de la clase base frágil"—. La composición delega en objetos que se poseen y se pueden sustituir, y por eso escala mejor cuando el sistema crece. La regla práctica: hereda solo cuando exista un *es-un* real, estable y sustituible; en cualquier otro caso, compón.

## 🧩 Situación

Imagina el módulo de sonido de un pequeño simulador de granja. Llega un mensaje del mundo del juego —"el jugador tocó a este animal"— y hay que reproducir su sonido. Sin polimorfismo, ese punto del código tendría que preguntar el tipo con una cadena de `if`, y lo peor es que esa misma cadena reaparecería en cada lugar donde otro subsistema (el registro de eventos, la interfaz, el logro "escucha las tres especies") necesite el sonido. Cada especie nueva obligaría a tocar todos esos sitios, y olvidar uno es un error silencioso.

Con polimorfismo, cada animal es un objeto que sabe sonar. El resto del programa trabaja contra la idea abstracta "un animal", invoca `animal.sonido()` y confía en que el despacho dinámico elija `guau`, `miau` o `muu`. Añadir una oveja es crear un tipo más, no editar diez condicionales. Eso es exactamente lo que verifican los tres casos de esta clase: mismo mensaje, tres respuestas correctas según el tipo real.

## 🧮 Modelo

- **Entrada** (stdin): una palabra: `perro`, `gato` o `vaca`
- **Salida** (stdout): `sonido=<guau|miau|muu>`
- **Regla:** cada tipo devuelve su propio sonido

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `perro` | `sonido=guau` |
| `gato` | `sonido=miau` |
| `vaca` | `sonido=muu` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER tipo ; crear animal ; ESCRIBIR animal.sonido()
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys


class Perro:
    def sonido(self):
        return "guau"


class Gato:
    def sonido(self):
        return "miau"


class Vaca:
    def sonido(self):
        return "muu"


tipo = sys.stdin.readline().strip()
animales = {"perro": Perro(), "gato": Gato(), "vaca": Vaca()}
print(f"sonido={animales[tipo].sonido()}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

class Perro { sonido() { return "guau"; } }
class Gato { sonido() { return "miau"; } }
class Vaca { sonido() { return "muu"; } }

const tipo = readFileSync(0, "utf8").trim();
const animales = { perro: new Perro(), gato: new Gato(), vaca: new Vaca() };
console.log(`sonido=${animales[tipo].sonido()}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

interface Animal { sonido(): string; }
class Perro implements Animal { sonido() { return "guau"; } }
class Gato implements Animal { sonido() { return "miau"; } }
class Vaca implements Animal { sonido() { return "muu"; } }

const tipo: string = readFileSync(0, "utf8").trim();
const animales: Record<string, Animal> = { perro: new Perro(), gato: new Gato(), vaca: new Vaca() };
console.log(`sonido=${animales[tipo].sonido()}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    interface Animal { String sonido(); }
    static class Perro implements Animal { public String sonido() { return "guau"; } }
    static class Gato implements Animal { public String sonido() { return "miau"; } }
    static class Vaca implements Animal { public String sonido() { return "muu"; } }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String tipo = br.readLine().trim();
        Animal a;
        switch (tipo) {
            case "perro": a = new Perro(); break;
            case "gato": a = new Gato(); break;
            default: a = new Vaca();
        }
        System.out.println("sonido=" + a.sonido());
    }
}
```

### C# · `dotnet run`

```csharp
using System;

string tipo = Console.In.ReadToEnd().Trim();
IAnimal a = tipo switch {
    "perro" => new Perro(),
    "gato" => new Gato(),
    _ => new Vaca(),
};
Console.WriteLine($"sonido={a.Sonido()}");

interface IAnimal { string Sonido(); }
class Perro : IAnimal { public string Sonido() => "guau"; }
class Gato : IAnimal { public string Sonido() => "miau"; }
class Vaca : IAnimal { public string Sonido() => "muu"; }
```

### Go · `go run main.go`

```go
package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

type Animal interface {
	sonido() string
}

type Perro struct{}
type Gato struct{}
type Vaca struct{}

func (Perro) sonido() string { return "guau" }
func (Gato) sonido() string  { return "miau" }
func (Vaca) sonido() string  { return "muu" }

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	tipo := strings.TrimSpace(line)
	var a Animal
	switch tipo {
	case "perro":
		a = Perro{}
	case "gato":
		a = Gato{}
	default:
		a = Vaca{}
	}
	fmt.Printf("sonido=%s\n", a.sonido())
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

trait Animal {
    fn sonido(&self) -> &'static str;
}

struct Perro;
struct Gato;
struct Vaca;

impl Animal for Perro { fn sonido(&self) -> &'static str { "guau" } }
impl Animal for Gato { fn sonido(&self) -> &'static str { "miau" } }
impl Animal for Vaca { fn sonido(&self) -> &'static str { "muu" } }

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let tipo = s.trim();
    let a: Box<dyn Animal> = match tipo {
        "perro" => Box::new(Perro),
        "gato" => Box::new(Gato),
        _ => Box::new(Vaca),
    };
    println!("sonido={}", a.sonido());
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char tipo[32];
    if (scanf("%31s", tipo) != 1) return 1;
    const char *sonido;
    if (strcmp(tipo, "perro") == 0) sonido = "guau";
    else if (strcmp(tipo, "gato") == 0) sonido = "miau";
    else sonido = "muu";
    printf("sonido=%s\n", sonido);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: sin despacho polimórfico; se usa CASE.
WITH animales(tipo) AS (VALUES ('perro'))
SELECT printf('sonido=%s', CASE tipo WHEN 'perro' THEN 'guau' WHEN 'gato' THEN 'miau' ELSE 'muu' END) AS resultado
FROM animales;
```

### PHP · `php main.php`

```php
<?php
interface Animal { public function sonido(): string; }
class Perro implements Animal { public function sonido(): string { return "guau"; } }
class Gato implements Animal { public function sonido(): string { return "miau"; } }
class Vaca implements Animal { public function sonido(): string { return "muu"; } }

$tipo = trim(fgets(STDIN));
$animales = ["perro" => new Perro(), "gato" => new Gato(), "vaca" => new Vaca()];
echo "sonido=" . $animales[$tipo]->sonido() . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🧪 Laboratorio guiado — recorrido del código

Sigamos el camino de un caso concreto de [`casos.json`](casos.json): la entrada `perro` que debe producir `sonido=guau`. El archivo declara tres casos —`perro→sonido=guau`, `gato→sonido=miau`, `vaca→sonido=muu`— y el verificador alimenta cada `stdin` a las diez implementaciones esperando exactamente ese `esperado`.

Empecemos por **Python**. El programa define tres clases independientes, cada una con su método `sonido()`. La línea clave es el diccionario `animales = {"perro": Perro(), "gato": Gato(), "vaca": Vaca()}`: no es una jerarquía, es un mapa de nombre a **instancia ya construida**. Cuando entra `perro`, `animales[tipo]` devuelve el objeto `Perro()` y `.sonido()` se resuelve en tiempo de ejecución sobre ese objeto concreto. Python ni siquiera exige que las tres clases compartan una base: le basta con que respondan a `sonido()`. Eso es *duck typing* puro, y por eso el `f"sonido={...}"` imprime `sonido=guau` sin un solo `if` sobre el tipo. Fíjate en que la tabla del diccionario reemplaza a la cadena de condicionales: el polimorfismo está en el objeto, no en la ramificación.

**Java** muestra el mismo comportamiento con el contrato explícito. Aquí sí hay una `interface Animal { String sonido(); }` y `Perro`, `Gato`, `Vaca` la implementan con `implements Animal`. La variable se declara `Animal a` —el tipo estático es la interfaz— pero el `switch` sobre `tipo` le asigna una instancia concreta (`new Perro()` para `perro`). Cuando se ejecuta `a.sonido()`, la JVM consulta el tipo **dinámico** del objeto, no el estático de la variable, y salta a `Perro.sonido()`. Ese es el enlace dinámico que describe Sebesta: la misma línea `a.sonido()` produciría `miau` si `a` apuntara a un `Gato`. El `default` del `switch` cubre `vaca` y garantiza que ningún caso quede sin manejar.

**Rust** ilustra el mismo concepto sin herencia de clases: usa un `trait Animal` y tres structs vacíos que lo implementan. La firma reveladora es `let a: Box<dyn Animal> = match tipo { ... }`. El `dyn Animal` es un **objeto-trait**: un puntero gordo que lleva, además del dato, una tabla de métodos (la vtable). Cuando entra `perro`, el `match` mete un `Box::new(Perro)` en `a`, y `a.sonido()` hace un salto indirecto a través de esa tabla hasta la implementación de `Perro`. Rust exige el `Box` porque necesita un tamaño conocido en la pila para algo cuyo tipo real solo se sabe en ejecución; es la misma vtable de Java, hecha explícita.

Los tres —y las diez— convergen en la salida que pide el `esperado` de `casos.json`. Para `perro`, todas imprimen `sonido=guau`; para `gato`, `sonido=miau`; para `vaca`, `sonido=muu`. Lo instructivo es cómo cada lenguaje llega ahí: Python y JavaScript por *duck typing* con un diccionario/objeto de instancias, Java/C#/PHP por interfaz nominal con un `switch`, Go por interfaz estructural, Rust por objeto-trait. El **SQL** es la excepción declarada: no hay despacho de objetos, solo un `CASE tipo WHEN 'perro' THEN 'guau' ...` sobre una fila; el verificador lo marca como *ilustrativo* precisamente porque reproduce la salida sin usar polimorfismo. Ver los dos extremos —despacho dinámico real vs. un condicional— es lo que hace tangible qué aporta el paradigma.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Herencia/interfaces (Java/C#), traits (Rust), interfaces (Go), duck typing (Python/JS). |
| Semántica | El despacho es dinámico: se decide en ejecución por el tipo real. |
| Paradigmática | SQL usa CASE; no hay despacho polimórfico. |

La diferencia real más profunda es **cuándo se comprueba el contrato**. Python y JavaScript no lo comprueban nunca hasta que la llamada ocurre: si pasas un objeto que no tiene `sonido()`, el error salta en ejecución. Java, C#, Rust y TypeScript exigen que el tipo declare o implemente el contrato en tiempo de compilación, así que un animal sin `sonido()` ni siquiera compila. Go ocupa un lugar intermedio muy citado: su tipado es **estructural**, no nominal —un tipo satisface `Animal` por el mero hecho de tener el método `sonido() string`, sin escribir `implements` en ninguna parte—. Es interfaz con la comodidad del *duck typing* pero verificada por el compilador.

La segunda diferencia es **cómo se representa el objeto polimórfico en memoria**. Rust obliga a `Box<dyn Animal>` y C++ pediría un puntero o referencia a la base: el polimorfismo cuesta una indirección explícita a través de la vtable. Java y C# ocultan esa indirección porque todo objeto vive tras una referencia. Esto no es cosmético: en Rust puedes elegir entre despacho dinámico (`dyn`) y despacho estático (genéricos monomorfizados, sin vtable ni coste en ejecución), una decisión de rendimiento que los demás lenguajes del núcleo no ponen tan a la vista.

## 🧬 El concepto en la familia

El polimorfismo de subtipo es casi universal, pero cada familia lo consigue por un camino distinto. En Ruby y Smalltalk es *duck typing* llevado al extremo: todo es un mensaje enviado a un objeto, y el receptor decide. En Kotlin conviven interfaces y **clases selladas** (`sealed`), que permiten un `when` exhaustivo verificado por el compilador —lo mejor del despacho y del casamiento de patrones—. En C++ el polimorfismo dinámico exige métodos `virtual` y punteros/referencias a la base, mientras que las plantillas dan polimorfismo estático sin coste. En Haskell no hay subtipos: el rol lo cumplen las *type classes*, un despacho resuelto por el compilador según el tipo. Ver que todos persiguen el mismo objetivo —"un nombre, muchos comportamientos"— con mecanismos tan distintos es la lección transversal de esta parte del curso.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 111
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Abusar de la herencia profunda** → causa: modelar como *es-un* algo que solo comparte código, creando jerarquías de cuatro o cinco niveles donde un cambio en la raíz rompe hojas lejanas (la "clase base frágil" de CTM cap. 7) → solución: preferir composición y delegación; hereda solo cuando el subtipo es sustituible por el supertipo sin sorpresas.
- **Olvidar un tipo** → causa: un `switch`/`match` sin rama para algún valor deja un caso sin manejar y produce salida vacía o una excepción → solución: cubrir todos los casos explícitamente o dar un `default` sensato; en lenguajes con exhaustividad (Rust, Kotlin `sealed`) deja que el compilador te obligue.
- **Confundir el tipo estático con el dinámico** → causa: creer que `Animal a` ejecutará "el método de Animal" cuando en realidad ejecuta el del objeto real → solución: recordar que el despacho es dinámico; el tipo de la variable solo dice qué métodos puedes llamar, no cuál se ejecuta.
- **Heredar solo para reutilizar código** → causa: usar la superclase como un cajón de utilidades, arrastrando estado y métodos que el hijo no necesita → solución: si solo quieres reusar, compón o extrae una función; la herencia es para *sustituibilidad*, no para ahorrar líneas.

## ❓ Preguntas frecuentes

- **¿Herencia o composición?** Composición por defecto; herencia solo cuando exista un *es-un* real, estable y sustituible (principio de Liskov). GoF lo resume en "favorece la composición sobre la herencia" y CTM cap. 7 explica por qué: la herencia acopla al hijo con los detalles internos del padre, y ese acoplamiento es difícil de deshacer cuando el sistema evoluciona.
- **¿Qué es duck typing?** "Si camina como pato y grazna como pato, es un pato": lo que importa es que el objeto responda al método `sonido()`, no que declare pertenecer a un tipo. Python y JavaScript lo usan por defecto; el precio es que un objeto sin ese método falla en ejecución, no al compilar.
- **¿El polimorfismo necesita herencia?** No. En esta clase Python y JS lo logran sin superclase común, y Go lo logra con interfaces satisfechas de forma implícita. La herencia es *una* manera de compartir un contrato, no la única.
- **¿Por qué Rust me obliga a escribir `Box<dyn Animal>`?** Porque un valor cuyo tipo real solo se conoce en ejecución no tiene tamaño fijo en la pila. El `Box` lo pone en el heap tras un puntero de tamaño conocido y adjunta la vtable para el despacho dinámico. Es la misma indirección que Java y C# hacen por ti de forma invisible.

## 🔗 Referencias

**Libros de la parte:**

- P. Van Roy y S. Haridi — *Concepts, Techniques, and Models of Computer Programming* (MIT Press). Cap. 7 (herencia y sus riesgos; "prefiere composición").
- H. Abelson y G. J. Sussman — *Structure and Interpretation of Computer Programs* (2ª ed., MIT Press).
- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson). Cap. 12 (soporte para OO, herencia, enlace dinámico y polimorfismo).
- E. Gamma, R. Helm, R. Johnson y J. Vlissides (GoF) — *Design Patterns* (Addison-Wesley). Principio "favorecer la composición sobre la herencia".

**Libros de los lenguajes del núcleo:**

- L. Ramalho — *Fluent Python* (2ª ed., O'Reilly).
- M. Haverbeke — *Eloquent JavaScript* (3ª ed.) — [gratis online](https://eloquentjavascript.net/).
- B. Cherny — *Programming TypeScript* (O'Reilly).
- J. Bloch — *Effective Java* (3ª ed., Addison-Wesley). Ítem 18: "prefiere composición a herencia".
- J. Skeet — *C# in Depth* (4ª ed., Manning).
- A. Donovan y B. Kernighan — *The Go Programming Language* (Addison-Wesley).
- S. Klabnik y C. Nichols — *The Rust Programming Language* — [gratis online](https://doc.rust-lang.org/book/).
- B. Kernighan y D. Ritchie — *The C Programming Language* (2ª ed., Prentice Hall).
- C. J. Date — *SQL and Relational Theory* (3ª ed., O'Reilly).
- J. Lockhart — *Modern PHP* (O'Reilly).

---

> [⏮️ Clase 110](../../parte-7-paradigmas/110-orientado-a-objetos-clases-objetos-y-estado/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 112 ⏭️](../../parte-7-paradigmas/112-interfaces-traits-y-clases-abstractas/README.md)
