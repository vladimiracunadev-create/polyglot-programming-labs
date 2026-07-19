# Clase 111 — Herencia, composición y polimorfismo

> Parte **7 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Practicar **herencia, composición y polimorfismo**: distintos tipos que comparten una interfaz común (`sonido`) y responden cada uno a su manera. Llamar al mismo método da resultados distintos según el tipo real.

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

## 🧩 Situación

Perro, gato y vaca son animales, pero cada uno suena distinto. El polimorfismo permite tratarlos igual (`animal.sonido()`) y obtener la respuesta correcta según el tipo.

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

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Herencia/interfaces (Java/C#), traits (Rust), interfaces (Go), duck typing (Python/JS). |
| Semántica | El despacho es dinámico: se decide en ejecución por el tipo real. |
| Paradigmática | SQL usa CASE; no hay despacho polimórfico. |

## 🧬 El concepto en la familia

En Ruby el polimorfismo es por duck typing. En Kotlin, interfaces y clases selladas.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 111
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Abusar de la herencia profunda** → causa: jerarquías frágiles → solución: preferir composición cuando encaje
- **Olvidar un tipo** → causa: caso sin manejar → solución: cubrir todos o usar un default

## ❓ Preguntas frecuentes

- **¿Herencia o composición?** Composición por defecto; herencia cuando hay un 'es-un' real y estable.
- **¿Qué es duck typing?** Si suena como pato, es pato: importa el método, no el tipo declarado.

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

> [⏮️ Clase 110](../../parte-7-paradigmas/110-orientado-a-objetos-clases-objetos-y-estado/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 112 ⏭️](../../parte-7-paradigmas/112-interfaces-traits-y-clases-abstractas/README.md)
