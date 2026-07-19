# Clase 099 — Registros, structs y clases

> Parte **6 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Comprender el **registro** (struct, clase, record, según el lenguaje) como la estructura que agrupa campos **heterogéneos** accedidos por **nombre**, y no por posición. Es el complemento exacto de la tupla de la clase 091: donde la tupla dice «el elemento 0 y el elemento 1», el registro dice «`persona.nombre` y `persona.edad`». Ese cambio de índice a nombre no es cosmético: convierte una posición anónima —fácil de confundir— en un campo con significado que el compilador y el lector reconocen. Bajo la sintaxis late una decisión de la que depende casi todo el comportamiento del programa: si el tipo tiene **semántica de valor** (se copia al asignarlo o pasarlo, como un `struct` de C, Go o Rust) o **semántica de referencia** (se comparte, como una clase de Java, C# o Python). En memoria, los campos de un registro viven **contiguos**, uno tras otro, lo que lo hace amable con la caché igual que el arreglo de la clase 089. En esta clase modelas la misma `Persona` en diez lenguajes para ver cómo cada uno resuelve las dos preguntas que definen un registro: cómo se nombra y cómo se copia.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Definir un tipo con campos nombrados.
2. Crear una instancia y acceder a sus campos.
3. Distinguir struct de clase donde aplique.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Registro/struct | Campos nombrados juntos |
| 2 | Instancia | Un valor del tipo |
| 3 | Acceso a campos | `.nombre`, `.edad` |

## 📖 Definiciones y características

- **Registro (record / struct)** — tipo compuesto que agrupa un número fijo de campos, cada uno con su propio nombre y su propio tipo. A diferencia del arreglo (elementos homogéneos accedidos por índice) y de la tupla (heterogéneos pero accedidos por posición), el registro combina lo mejor de ambos: campos heterogéneos accedidos por nombre. Es lo que la teoría de tipos llama un **tipo producto**: el conjunto de sus valores posibles es el producto cartesiano de los valores de cada campo, `nombre × edad`. Donovan y Kernighan (*The Go Programming Language*, cap. 4) presentan el `struct` justamente así, como el agregado nombrado por excelencia. Crear, leer o escribir un campo es O(1): el compilador conoce el desplazamiento de cada campo dentro del bloque en tiempo de compilación.
- **Campo (field / member)** — cada dato con nombre dentro del registro, con su propio tipo. Se accede con la notación de punto, `persona.edad`. En memoria, los campos se disponen **contiguos** en el orden declarado (a veces con relleno de *alineamiento* entre ellos), lo que permite que el registro entero viaje junto a la caché y que el acceso a un campo sea una simple suma `base + desplazamiento`.
- **Instancia (instance / value)** — un valor concreto del tipo, `Persona("Ada", 36)`. La gran división: si el tipo tiene **semántica de valor**, asignar o pasar la instancia la **copia** entera (dos variables independientes); si tiene **semántica de referencia**, ambas variables apuntan al **mismo** objeto y mutar una afecta a la otra. Esta distinción —struct vs. clase— es el eje que separa a C, Go, Rust y los `struct` de C# de las clases de Java, C# y Python, y prepara el terreno para la identidad (clase 101) y la copia (clase 102).

## 🧩 Situación

Imagina una función que recibe `nombre`, `edad`, `email` y `saldo` como cuatro parámetros sueltos. Tarde o temprano alguien invierte dos de ellos, o actualiza `edad` en un sitio y olvida el otro, y los datos que deberían viajar juntos se desincronizan. El registro cura ese mal de raíz: junta los campos relacionados en un solo tipo con nombre —`Persona`— que se pasa como una sola cosa, se valida como una sola cosa y no puede separarse por accidente. Ganamos también **legibilidad** (`p.edad` dice mucho más que `args[1]`) y **evolución**: añadir un campo no obliga a reescribir cada firma de función. El problema de hoy es deliberadamente pequeño —leer un nombre y una edad, construir una `Persona` e imprimirla— para que la atención caiga sobre lo que de verdad importa: cómo cada lenguaje declara el tipo, nombra los campos y decide si la instancia se copia o se comparte.

## 🧮 Modelo

- **Entrada** (stdin): una línea `nombre edad` (una palabra y un entero)
- **Salida** (stdout): `Persona(nombre=<nombre>, edad=<edad>)`
- **Regla:** registro con campos nombre y edad

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `Ada 36` | `Persona(nombre=Ada, edad=36)` |
| `Bo 5` | `Persona(nombre=Bo, edad=5)` |
| `Cy 99` | `Persona(nombre=Cy, edad=99)` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER nombre, edad ; crear Persona ; ESCRIBIR formateado
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys
from dataclasses import dataclass


@dataclass
class Persona:
    nombre: str
    edad: int


t = sys.stdin.readline().split()
p = Persona(t[0], int(t[1]))
print(f"Persona(nombre={p.nombre}, edad={p.edad})")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const t = readFileSync(0, "utf8").trim().split(/\s+/);
const persona = { nombre: t[0], edad: parseInt(t[1], 10) };
console.log(`Persona(nombre=${persona.nombre}, edad=${persona.edad})`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

interface Persona {
  nombre: string;
  edad: number;
}

const t: string[] = readFileSync(0, "utf8").trim().split(/\s+/);
const p: Persona = { nombre: t[0], edad: parseInt(t[1], 10) };
console.log(`Persona(nombre=${p.nombre}, edad=${p.edad})`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    record Persona(String nombre, int edad) {}

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] t = br.readLine().trim().split("\\s+");
        Persona p = new Persona(t[0], Integer.parseInt(t[1]));
        System.out.println("Persona(nombre=" + p.nombre() + ", edad=" + p.edad() + ")");
    }
}
```

### C# · `dotnet run`

```csharp
using System;

string[] t = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
var p = new Persona(t[0], int.Parse(t[1]));
Console.WriteLine($"Persona(nombre={p.Nombre}, edad={p.Edad})");

record Persona(string Nombre, int Edad);
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

type Persona struct {
	Nombre string
	Edad   int
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	t := strings.Fields(line)
	edad, _ := strconv.Atoi(t[1])
	p := Persona{Nombre: t[0], Edad: edad}
	fmt.Printf("Persona(nombre=%s, edad=%d)\n", p.Nombre, p.Edad)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

struct Persona {
    nombre: String,
    edad: i64,
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let t: Vec<&str> = s.split_whitespace().collect();
    let p = Persona {
        nombre: t[0].to_string(),
        edad: t[1].parse().unwrap(),
    };
    println!("Persona(nombre={}, edad={})", p.nombre, p.edad);
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

struct Persona {
    char nombre[64];
    long edad;
};

int main(void) {
    struct Persona p;
    if (scanf("%63s %ld", p.nombre, &p.edad) != 2) return 1;
    printf("Persona(nombre=%s, edad=%ld)\n", p.nombre, p.edad);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: una fila de una tabla es un registro.
WITH personas(nombre, edad) AS (VALUES ('Ada', 36))
SELECT printf('Persona(nombre=%s, edad=%d)', nombre, edad) AS resultado FROM personas;
```

### PHP · `php main.php`

```php
<?php
class Persona {
    public function __construct(public string $nombre, public int $edad) {}
}

$t = preg_split('/\s+/', trim(fgets(STDIN)));
$p = new Persona($t[0], (int) $t[1]);
echo "Persona(nombre={$p->nombre}, edad={$p->edad})\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🧪 Laboratorio guiado: del código a la salida

Sigamos el caso `Ada 36`, que debe producir `Persona(nombre=Ada, edad=36)`. Los diez programas leen dos palabras, construyen un registro y lo formatean; conviene mirar tres que revelan modelos distintos de declaración y de memoria.

En **Python**, el decorador `@dataclass` sobre `class Persona` con las anotaciones `nombre: str` y `edad: int` genera automáticamente el `__init__`, de modo que `Persona(t[0], int(t[1]))` guarda `"Ada"` y `36` como atributos. Aquí `p` es una **referencia** a un objeto en el heap: si hicieras `q = p`, ambos nombres apuntarían al mismo objeto. El f-string lee `p.nombre` y `p.edad` por nombre y arma la línea. Ramalho (*Fluent Python*, cap. sobre *data class builders*) muestra que `@dataclass` es azúcar que evita escribir el constructor y el `__repr__` a mano.

En **Go**, `type Persona struct { Nombre string; Edad int }` declara un tipo con semántica de **valor**: `p := Persona{Nombre: t[0], Edad: edad}` crea el registro en la pila y, si lo asignaras a otra variable, se copiaría campo a campo. Los nombres de campo van en mayúscula por la regla de exportación de Go, no por capricho. `fmt.Printf` los formatea por nombre para producir exactamente `Persona(nombre=Ada, edad=36)`.

En **Java**, `record Persona(String nombre, int edad) {}` es la forma moderna (Java 16+): en una línea el compilador genera el constructor, los accesores `nombre()` y `edad()`, y `equals`/`hashCode`/`toString` coherentes. `new Persona(t[0], ...)` crea el objeto en el heap —semántica de **referencia**, como toda clase de Java—; los accesores devuelven los campos que la salida ensambla. Bloch (*Effective Java*) recomienda los records precisamente para estos «portadores de datos inmutables».

Los tres imprimen `Persona(nombre=Ada, edad=36)`; el verificador comprueba que las diez implementaciones coinciden carácter a carácter con lo que dicta `casos.json`.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `class`/`@dataclass` (Python), `record` (Java), `struct` (Go/Rust/C), objeto (JS). |
| Semántica | Struct suele ser por valor; clase por referencia (Java/C#). |
| Paradigmática | SQL: una fila de una tabla es un registro. |

La diferencia más honda entre los diez no es sintáctica sino de **semántica de copia**. En C, Go, Rust y los `struct` de C#, un registro es un valor: asignarlo o pasarlo a una función lo **copia** entero, y las dos variables quedan independientes. En Java, Python, JavaScript y las `class` de C#, la instancia vive en el heap y la variable es una **referencia**: asignarla comparte el mismo objeto. Esto explica por qué C# ofrece ambas herramientas —`record class` (referencia) y `record struct` (valor)— y obliga al programador a elegir. Hay además un eje de **cuánto trabajo te ahorra el lenguaje**: el `record` de Java, la `@dataclass` de Python y el `record` de C# generan constructor, comparación e impresión gratis; en C debes declarar cada campo del `struct` y formatearlo a mano, sin accesores ni `toString`. Y un eje de **disposición en memoria**: en C, Go y Rust los campos ocupan bytes contiguos con posible relleno de alineamiento, un detalle que importa para el rendimiento y la interoperabilidad; en Python un objeto es un diccionario de atributos, mucho más flexible pero más pesado.

## 🧬 El concepto en la familia

El registro es tan fundamental que cada familia le da su propia forma, y los nombres engañan. En Kotlin, `data class Persona(val nombre: String, val edad: Int)` genera igualdad y copia como el record de Java. En C++, `struct` y `class` son casi idénticos —solo cambia la visibilidad por defecto— y ambos tienen semántica de valor, al revés que en C#, donde `struct` es valor y `class` es referencia. En Swift, la distinción `struct` (valor) vs. `class` (referencia) es el eje central del lenguaje. En Rust, un `struct` es valor y solo se copia implícitamente si implementa `Copy`; si no, se *mueve*. Reconocer, en cada lenguaje que toques, si tu registro se copia o se comparte es la mitad de entender su comportamiento: de ahí salen tanto los bugs de aliasing (clase 102) como las sorpresas de identidad (clase 101).

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 099
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Usar variables sueltas en vez de agrupar** → causa: campos que deberían viajar juntos se pasan por separado y se desincronizan → solución: agruparlos en un registro con nombre que se valide y viaje como una unidad.
- **Confundir struct (valor) con clase (referencia)** → causa: en Go, C o Rust asignas un struct esperando compartirlo y en realidad copiaste; en Java o Python asignas un objeto esperando copiarlo y en realidad lo compartiste → solución: saber de memoria si el tipo del lenguaje es por valor o por referencia (ver la comparación de arriba).
- **Mutar un campo de un struct copiado creyendo que cambia el original** → causa: en un lenguaje de valor, la función recibió una copia; tus cambios se pierden al volver → solución: devolver el struct modificado, o usar un puntero/referencia explícito (`*Persona` en Go, `&mut` en Rust) si de verdad quieres mutar el original.
- **Acceder a los campos por posición cuando ya son un registro** → causa: tratar `Persona` como si fuera una tupla y confiar en el orden → solución: acceder siempre por nombre (`p.edad`); ese es justamente el valor que aporta el registro sobre la tupla.

## ❓ Preguntas frecuentes

- **¿Struct o clase?** Como regla, `struct` (valor) para agregados pequeños e inmutables de datos —un punto, una fecha, un color—; `class` (referencia) cuando el objeto tiene identidad propia, comportamiento rico o es grande y no quieres copiarlo en cada paso. En lenguajes que solo tienen uno de los dos (Java: todo clase; Go: todo struct) la pregunta desaparece y usas lo que hay.
- **¿Registro inmutable?** A menudo conviene: un `record` de Java, un `record` de C#, una `@dataclass(frozen=True)` de Python o un `struct` de Rust que no expones como `mut`. Los datos inmutables se comparten sin miedo, se comparan por valor con seguridad y eliminan una clase entera de bugs de aliasing (clase 102).
- **¿Por qué el registro es un «tipo producto»?** Porque el conjunto de sus valores posibles es el producto cartesiano de los de cada campo: una `Persona` con nombre entre N posibles y edad entre M posibles admite N × M valores. Es el dual del **tipo suma** de la clase siguiente, donde las alternativas se *suman* en vez de multiplicarse.
- **¿Cuál es la diferencia con una tupla?** Una tupla accede por posición (`t[0]`, `t[1]`) y no nombra sus componentes; un registro accede por nombre (`p.nombre`, `p.edad`). El registro es más legible y resistente al cambio; la tupla, más breve para datos anónimos y de vida corta.

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

> [⏮️ Clase 098](../../parte-6-datos-y-estructuras/098-grafos/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 100 ⏭️](../../parte-6-datos-y-estructuras/100-enumeraciones-y-tipos-algebraicos-adt-sum-types/README.md)
