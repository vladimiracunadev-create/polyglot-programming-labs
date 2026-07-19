# Clase 165 — El proyecto: un sistema con componentes en varios lenguajes

> Parte **11 — Proyecto integrador políglota** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Arrancar el **proyecto integrador** y, con él, la última idea del programa: un sistema real
casi nunca es un único programa monolítico, sino una **federación de componentes** que colaboran, cada
uno escrito en el lenguaje que mejor resuelve su parte. Antes de escribir una línea, un ingeniero hace
lo que Sam Newman llama el trabajo más importante y más olvidado: **decidir dónde están las costuras**.
Esta primera clase se limita a ese acto fundacional: **inventariar** las piezas del sistema, ponerles
nombre y contarlas.

Parece trivial —"contar palabras"— pero el ejercicio esconde la tesis de toda la Parte 11. En
*Building Microservices*, Newman insiste en que la descomposición de un sistema en servicios no se hace
por tecnología (un servicio "de Java", otro "de SQL") sino por **capacidad de negocio**: cada componente
posee una responsabilidad y expone una frontera. Contar e identificar los componentes es el paso cero de
esa descomposición. Si no sabes cuántas piezas tienes ni cómo se llaman, no puedes razonar sobre cómo
encajan, ni desplegarlas por separado, ni sustituir una sin tocar las demás.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Inventariar los componentes de un sistema y darles un nombre estable.
2. Explicar por qué un sistema es más que la suma de sus partes: son las **fronteras** las que lo definen.
3. Entender el inventario como el primer artefacto de diseño, previo a cualquier código.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Sistema | El todo integrado, no un solo binario |
| 2 | Componente | Cada pieza con su responsabilidad y su lenguaje |
| 3 | Inventario | La lista de piezas: primer acto del diseño |

## 📖 Definiciones y características

Un **sistema integrador** es un producto compuesto por varios componentes que colaboran para cumplir un
objetivo; su virtud es que cada pieza puede escribirse en el lenguaje idóneo y evolucionar a su ritmo. Un
**componente** es una unidad con **una** responsabilidad —Hunt y Thomas, en *The Pragmatic Programmer*,
lo llaman *ortogonalidad*: cambiar una pieza no debería sacudir a las otras—. El **inventario** es la lista
explícita de esas piezas; es humilde pero decisivo, porque un componente que no aparece en el inventario
es un componente que nadie despliega, nadie prueba y nadie mantiene.

La lección de fondo, que recorre toda esta parte, es que la complejidad de un sistema no vive dentro de
cada componente sino **entre** ellos. Newman lo resume así: los servicios son fáciles; la integración es
difícil. Por eso empezamos nombrando y contando: el inventario convierte una idea difusa ("una app") en
una estructura sobre la que se puede diseñar, versionar y defender cada decisión.

## 🧩 Situación

Imagina que te encargan "una plataforma de ventas". Suena a un proyecto; en realidad son cuatro o cinco
sistemas que hablan entre sí: una **CLI** para los operadores, una **API** que contiene la lógica, una
**web** que consume esa API, una **capa de datos** que persiste todo y unos **scripts** que automatizan
tareas nocturnas. Si arrancas escribiendo código sin este inventario, terminas con un ovillo donde la
web consulta la base de datos directamente, la CLI reimplementa la lógica de la API y nadie sabe qué pieza
es dueña de qué. El inventario —contar los componentes y nombrarlos— es la vacuna contra ese ovillo: fija
el alcance, revela las fronteras y te dice, pieza por pieza, qué lenguaje pedirá cada una en las clases
siguientes.

## 🧮 Modelo

- **Entrada** (stdin): una línea con nombres de componentes (palabras)
- **Salida** (stdout): `componentes=<N> nombres=<unidos por ->`
- **Regla:** contar y listar los componentes

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `cli api web` | `componentes=3 nombres=cli-api-web` |
| `app` | `componentes=1 nombres=app` |
| `web api datos cache` | `componentes=4 nombres=web-api-datos-cache` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER componentes ; ESCRIBIR conteo y nombres unidos
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

c = sys.stdin.read().split()
print(f"componentes={len(c)} nombres={'-'.join(c)}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const c = readFileSync(0, "utf8").trim().split(/\s+/);
console.log(`componentes=${c.length} nombres=${c.join("-")}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const c: string[] = readFileSync(0, "utf8").trim().split(/\s+/);
console.log(`componentes=${c.length} nombres=${c.join("-")}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] c = br.readLine().trim().split("\\s+");
        System.out.println("componentes=" + c.length + " nombres=" + String.join("-", c));
    }
}
```

### C# · `dotnet run`

```csharp
using System;

string[] c = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
Console.WriteLine($"componentes={c.Length} nombres={string.Join("-", c)}");
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

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	c := strings.Fields(line)
	fmt.Printf("componentes=%d nombres=%s\n", len(c), strings.Join(c, "-"))
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let c: Vec<&str> = s.split_whitespace().collect();
    println!("componentes={} nombres={}", c.len(), c.join("-"));
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char t[64];
    char buf[4096];
    buf[0] = '\0';
    int n = 0;
    while (scanf("%63s", t) == 1) {
        if (n > 0) strcat(buf, "-");
        strcat(buf, t);
        n++;
    }
    printf("componentes=%d nombres=%s\n", n, buf);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL cuenta y une los componentes.
WITH c(nombre) AS (VALUES ('cli'), ('api'), ('web'))
SELECT printf('componentes=%d nombres=%s', count(*), group_concat(nombre, '-')) AS resultado FROM c;
```

### PHP · `php main.php`

```php
<?php
$c = preg_split('/\s+/', trim(fgets(STDIN)));
echo "componentes=" . count($c) . " nombres=" . implode("-", $c) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🧪 Recorrido del código

El contrato de la clase (ver [`casos.json`](casos.json)) es mínimo: recibe una línea de nombres separados
por espacios y responde `componentes=<N> nombres=<unidos por ->`. Con la entrada `cli api web` la salida
esperada es `componentes=3 nombres=cli-api-web`. Sigamos cómo cada lenguaje llega a esa misma línea, porque
las diferencias revelan cómo piensa cada familia.

En **Python** todo cabe en dos gestos. `sys.stdin.read().split()` lee toda la entrada y la parte por
cualquier espacio en una lista `['cli', 'api', 'web']`; `split()` sin argumentos ya colapsa espacios
múltiples y descarta los extremos, así que no hace falta limpiar nada. Luego `len(c)` da el conteo y
`'-'.join(c)` teje los nombres. La *f-string* interpola ambos: es el estilo idiomático que Ramalho celebra
en *Fluent Python* —dejar que las estructuras de datos de alto nivel hagan el trabajo—.

**Go** cuenta la misma historia con más andamiaje explícito, fiel a su filosofía de no ocultar nada:

```go
line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
c := strings.Fields(line)
fmt.Printf("componentes=%d nombres=%s\n", len(c), strings.Join(c, "-"))
```

`strings.Fields` es el gemelo de `split()` de Python: parte por espacios y descarta los vacíos. Pero fíjate
en el `_`: Go te obliga a mirar de frente el error de lectura y a decidir, aquí, ignorarlo. Donovan y
Kernighan describen esa verbosidad como una virtud: el código dice exactamente lo que hace.

**C** no tiene ni listas ni `join`; hay que construir la salida a mano. El `while (scanf("%63s", t) == 1)`
lee token a token, y en cada vuelta antepone un guion (`if (n > 0) strcat(buf, "-")`) antes de concatenar.
Es el mismo algoritmo, pero al nivel del byte: se ve el coste que las abstracciones de Python y Go te
ahorran. **SQL**, por su parte, no lee de stdin; expresa la idea de forma declarativa con
`count(*)` y `group_concat(nombre, '-')` sobre una tabla de valores, y por eso el verificador la marca como
*ilustrativa*. Los cinco caminos convergen en el mismo texto: eso es la equivalencia que este programa
demuestra por máquina, no de palabra.

## 🔬 Comparación

Contar e imprimir parece idéntico en todas partes, pero el detalle de cómo se separa la entrada distingue
a las familias. La tabla resume las tres clases de diferencia; el texto las explica.

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `split()` (Python), `Fields` (Go), `preg_split` (PHP), `strcat` en bucle (C): la misma partición, diez escrituras. |
| Semántica | Python y JS obtienen una lista/array vivo; C manipula un buffer de bytes de tamaño fijo (de ahí el `%63s` que evita el desbordamiento). |
| Paradigmática | Los nueve imperativos recorren tokens; SQL **declara** el resultado con `count` y `group_concat` sobre un conjunto. |

La diferencia semántica más real es la del manejo de memoria y errores: en Python o JavaScript un array
crece solo; en C decides el tamaño del buffer y cargas con las consecuencias; en Go el error de E/S es un
valor que no puedes fingir que no existe. Son tres modelos de responsabilidad para el mismo problema
trivial —y esa es justamente la razón por la que un sistema real elige un lenguaje distinto por componente—.

## 🧬 El concepto en la familia

Todo sistema real es, en el fondo, un inventario de componentes con responsabilidades y lenguajes propios.
Newman lo llama descomposición por capacidades; en el mundo Unix es la vieja idea de "programas que hacen
una cosa bien" y se componen por tuberías. Reconocer esa estructura —contar las piezas antes de construir—
es lo que separa un diseño de una acumulación de código.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 165
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Componentes sin responsabilidad clara** → causa: dos piezas hacen lo mismo o comparten estado → solución: una responsabilidad por componente, verificable con la pregunta "¿quién es dueño de este dato?".
- **Olvidar un componente** → causa: el script de despliegue no lo contempla y la integración queda a medias → solución: inventariar todas las piezas, incluidas las invisibles (jobs, migraciones, colas).
- **Descomponer por tecnología en vez de por capacidad** → causa: acabas con un "servicio de base de datos" que todos tocan → solución: dividir por lo que hace el negocio, como propone Newman, no por el lenguaje.

## ❓ Preguntas frecuentes

- **¿Cuántos componentes?** Los que el problema justifique; ni de más ni de menos. Cada frontera que añades tiene un coste de integración (red, contratos, despliegue), así que se paga por tenerla.
- **¿Por dónde empezar?** Por el inventario y luego por los contratos entre componentes (clase 166): primero qué piezas hay, después cómo se hablan.
- **¿Un componente = un lenguaje?** No forzosamente, pero el enfoque políglota permite que cada uno use el suyo. Lo que los une no es el lenguaje sino el contrato en su frontera.

## 🔗 Referencias

**Libros de la parte:**

- S. Newman — *Building Microservices* (2ª ed., O'Reilly).
- M. Nygard — *Release It!* (2ª ed., Pragmatic Bookshelf).
- A. Hunt y D. Thomas — *The Pragmatic Programmer* (2ª ed., Addison-Wesley).

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

> [⏮️ Clase 164](../../parte-10-interoperabilidad-y-fronteras-entre-lenguajes/164-elegir-el-lenguaje-correcto-para-cada-componente/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 166 ⏭️](../../parte-11-proyecto-integrador-poliglota/166-diseno-responsabilidades-y-contratos-entre-componentes/README.md)
