# Clase 102 — Copia superficial vs. profunda; referencia vs. valor

> Parte **6 — Datos y estructuras** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Distinguir **copia** de **referencia compartida**, y **copia superficial** de **profunda**. Son dos preguntas encadenadas. La primera es si `b = a` duplica el dato o solo le da un segundo nombre: en casi todos los lenguajes modernos, asignar una colección **comparte** la referencia, de modo que modificar `b` modifica `a`, y muchos programadores descubren esa regla a base de un bug. La segunda pregunta aparece en cuanto decides copiar de verdad: una copia **superficial** duplica el contenedor externo pero deja que los elementos internos sigan apuntando a los mismos objetos, mientras que una copia **profunda** desciende recursivamente hasta duplicarlo todo. La diferencia entre ambas no es filosófica sino de coste y de riesgo: la superficial es O(n) sobre los n elementos del primer nivel; la profunda es O(tamaño total del grafo de objetos) y debe además detectar ciclos si los hay. Esta clase es la continuación directa de la 099 —semántica de valor frente a semántica de referencia— y la contracara de la 101: allí preguntábamos si dos cosas son el mismo objeto, aquí decidimos si queremos que lo sean.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Copiar una colección.
2. Comprobar que el original no cambia.
3. Distinguir copia superficial de profunda.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Copia vs. referencia | Duplicar o compartir |
| 2 | Copia superficial | Copia el primer nivel |
| 3 | Copia profunda | Copia todo recursivamente |

## 📖 Definiciones y características

Para entender esta clase conviene tener presente el modelo de memoria. Una variable que contiene una colección casi nunca contiene la colección: contiene una **referencia**, un puntero a un bloque del heap donde viven los elementos. Asignar `b = a` copia esa referencia —ocho bytes, O(1)— y deja dos nombres apuntando al mismo bloque. A esa situación se la llama **aliasing**, y es la fuente del bug más frecuente de esta parte del curso: una función recibe una lista, la ordena «para su uso interno» y devuelve al llamante una lista reordenada que él no pidió. Como advierte Bloch en *Effective Java*, cuando un objeto guarda una referencia a una colección que le pasaron desde fuera, su encapsulación está rota: quien se la pasó puede seguir mutándola por debajo. La solución que él recomienda son las **copias defensivas** al entrar y al salir.

Copiar de verdad ofrece dos niveles. La **copia superficial** reserva un contenedor nuevo y copia los n elementos del primer nivel tal cual: coste O(n), y si esos elementos son referencias, la copia y el original acaban compartiendo los mismos objetos internos. La **copia profunda** recorre recursivamente toda la estructura duplicando cada nivel: coste proporcional al número total de nodos y aristas del grafo de objetos, con el problema añadido de los **ciclos** —si `a` contiene a `b` y `b` contiene a `a`, una copia profunda ingenua entra en recursión infinita, y por eso `copy.deepcopy` de Python lleva un registro de los objetos ya visitados—.

La pregunta decisiva, y la que casi nadie se hace a tiempo, es **si el nivel que compartes es mutable**. Una copia superficial de una lista de enteros, de cadenas inmutables o de tuplas es indistinguible de una profunda, porque nada de lo compartido puede cambiar. Esa observación explica por qué en el ejercicio de hoy —una lista de enteros— basta con la copia superficial, y por qué la programación funcional, con sus datos inmutables, hace desaparecer todo el problema: si nada muta, compartir es gratis y seguro.

- **Referencia compartida (aliasing)** — dos nombres para el mismo dato en el heap. Se crea en O(1) al asignar o al pasar un argumento. Mutar por un nombre se ve por el otro.
- **Copia superficial (shallow copy)** — contenedor nuevo, mismos elementos. `list(x)` o `x[:]` en Python, `[...x]` en JavaScript, `Arrays.copyOf` en Java, `clone()` en C#, `copy()` en Go, `to_vec()` en Rust. Coste O(n).
- **Copia profunda (deep copy)** — duplica recursivamente toda la estructura. `copy.deepcopy` en Python, `structuredClone` en JavaScript, `clone()` de un `Vec<Vec<T>>` en Rust (que es profunda por construcción, porque `Vec` posee sus elementos). Coste proporcional al grafo entero.
- **Copia defensiva** — copiar en la frontera de un módulo, al recibir y al devolver colecciones, para que nadie mute tu estado interno por accidente. Es la contramedida estándar al aliasing accidental.

## 🧩 Situación

El escenario es siempre el mismo y ocurre en todos los lenguajes de referencia. Una función `procesar(datos)` recibe una lista, hace `datos.sort()` porque le viene bien trabajar ordenada, y devuelve su resultado. El llamante, que no leyó el código, sigue usando su lista y la encuentra reordenada. No hubo error de compilación, no hubo excepción, no hay línea culpable: hubo aliasing. La variante con estructuras anidadas es peor porque sobrevive a la primera corrección. Alguien detecta el problema y escribe `copia = list(datos)`; el bug desaparece para listas de números y reaparece intacto para listas de listas, porque la copia superficial duplicó el contenedor pero las sublistas siguen siendo las mismas. El ejercicio de hoy usa deliberadamente la versión más simple —copiar una lista de enteros, cambiar el último elemento de la copia a 99 e imprimir ambas— para que la comprobación sea inequívoca: si el original sale intacto, la copia fue real; si sale con un 99 al final, lo que hiciste fue compartir.

## 🧮 Modelo

- **Entrada** (stdin): una línea con enteros separados por espacio
- **Salida** (stdout): `original=<lista> copia=<lista con el último cambiado a 99>` (unidos por -)
- **Regla:** copiar; copia[último] = 99; original intacto

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `1 2 3` | `original=1-2-3 copia=1-2-99` |
| `5 5` | `original=5-5 copia=5-99` |
| `7` | `original=7 copia=99` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER lista ; copia <- COPIA(lista) ; copia[fin] <- 99 ; ESCRIBIR original y copia
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys

nums = [int(x) for x in sys.stdin.read().split()]
copia = list(nums)  # copia superficial (aquí basta, son enteros)
copia[-1] = 99
print(f"original={'-'.join(map(str, nums))} copia={'-'.join(map(str, copia))}")
```

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const nums = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const copia = [...nums];
copia[copia.length - 1] = 99;
console.log(`original=${nums.join("-")} copia=${copia.join("-")}`);
```

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const nums: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const copia: number[] = [...nums];
copia[copia.length - 1] = 99;
console.log(`original=${nums.join("-")} copia=${copia.join("-")}`);
```

### Java · [`java/Main.java`](implementaciones/java/Main.java) · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Arrays;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        int[] nums = new int[p.length];
        for (int i = 0; i < p.length; i++) nums[i] = Integer.parseInt(p[i]);
        int[] copia = Arrays.copyOf(nums, nums.length);
        copia[copia.length - 1] = 99;
        System.out.println("original=" + join(nums) + " copia=" + join(copia));
    }

    static String join(int[] a) {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < a.length; i++) {
            if (i > 0) sb.append("-");
            sb.append(a[i]);
        }
        return sb.toString();
    }
}
```

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;
using System.Linq;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
int[] nums = p.Select(int.Parse).ToArray();
int[] copia = (int[]) nums.Clone();
copia[copia.Length - 1] = 99;
Console.WriteLine($"original={string.Join("-", nums)} copia={string.Join("-", copia)}");
```

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
	nums := make([]int, len(f))
	for i, s := range f {
		nums[i], _ = strconv.Atoi(s)
	}
	copia := make([]int, len(nums))
	copy(copia, nums)
	copia[len(copia)-1] = 99
	fmt.Printf("original=%s copia=%s\n", join(nums), join(copia))
}

func join(a []int) string {
	parts := make([]string, len(a))
	for i, n := range a {
		parts[i] = strconv.Itoa(n)
	}
	return strings.Join(parts, "-")
}
```

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn join(a: &[i64]) -> String {
    a.iter().map(|x| x.to_string()).collect::<Vec<_>>().join("-")
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let nums: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    let mut copia = nums.clone();
    let n = copia.len();
    copia[n - 1] = 99;
    println!("original={} copia={}", join(&nums), join(&copia));
}
```

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long v[1024];
    int n = 0;
    while (scanf("%ld", &v[n]) == 1) n++;
    long copia[1024];
    for (int i = 0; i < n; i++) copia[i] = v[i];
    copia[n - 1] = 99;
    printf("original=");
    for (int i = 0; i < n; i++) { if (i) printf("-"); printf("%ld", v[i]); }
    printf(" copia=");
    for (int i = 0; i < n; i++) { if (i) printf("-"); printf("%ld", copia[i]); }
    printf("\n");
    return 0;
}
```

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL: los conjuntos no comparten referencias mutables; se ilustra el cambio.
WITH nums(pos, x) AS (VALUES (1, 1), (2, 2), (3, 3))
SELECT 'original=' || (SELECT group_concat(x, '-') FROM (SELECT x FROM nums ORDER BY pos))
     || ' copia=' || (SELECT group_concat(CASE WHEN pos = (SELECT max(pos) FROM nums) THEN 99 ELSE x END, '-')
                       FROM (SELECT pos, x FROM nums ORDER BY pos)) AS resultado;
```

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
$nums = array_map('intval', preg_split('/\s+/', trim(fgets(STDIN))));
$copia = $nums; // PHP copia los arreglos por valor
$copia[count($copia) - 1] = 99;
echo "original=" . implode("-", $nums) . " copia=" . implode("-", $copia) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🧪 Laboratorio guiado: del código a la salida

Sigamos el caso `1 2 3`, que debe producir `original=1-2-3 copia=1-2-99`. La salida está diseñada para delatar el fallo: si en lugar de copiar hubiésemos compartido, el original saldría también como `1-2-99`.

En **Python**, la línea clave es `copia = list(nums)`. `list(...)` construye una lista nueva y va colocando en ella los elementos de `nums` uno a uno: contenedor distinto, mismos elementos. El comentario del código lo dice sin rodeos —es una copia superficial, y aquí basta— porque los elementos son enteros inmutables y compartirlos no tiene consecuencias. Después, `copia[-1] = 99` sustituye el último elemento **de la lista nueva**; `nums` no se entera. Si la línea hubiera sido `copia = nums`, ambos nombres apuntarían al mismo objeto y la salida sería `original=1-2-99 copia=1-2-99`, un fallo que el verificador detectaría de inmediato. Y si los elementos fueran a su vez listas, `list(nums)` seguiría sin bastar: habría que recurrir a `copy.deepcopy`.

En **Go**, la copia es explícita en dos pasos: `copia := make([]int, len(nums))` reserva un arreglo subyacente nuevo del tamaño justo, y `copy(copia, nums)` transfiere los elementos. Aquí la disciplina no es opcional. Un slice de Go es una cabecera de tres campos —puntero al arreglo, longitud y capacidad— de modo que `copia := nums` copia esa cabecera pero deja el mismo arreglo debajo, y escribir en `copia[0]` se vería en `nums[0]`. Donovan y Kernighan lo subrayan en *The Go Programming Language*: el slice es una *vista* sobre un arreglo, no el arreglo. La función incorporada `copy` existe justamente para cuando quieres el dato y no la vista.

En **Rust**, `let mut copia = nums.clone();` es la única forma que el lenguaje permite. La asignación `let copia = nums;` no compartiría la lista: **movería** la propiedad, y el compilador rechazaría cualquier uso posterior de `nums`. Ese es el mecanismo que Klabnik y Nichols explican en *The Rust Programming Language* como núcleo del lenguaje: cada valor tiene un dueño único, y compartir mutabilidad es un error de compilación, no un bug en tiempo de ejecución. Vale la pena notar que `clone()` sobre un `Vec<Vec<i64>>` sería **profunda** sin que haya que pedirlo, porque en Rust un `Vec` posee sus elementos en vez de referenciarlos: la distinción superficial/profunda casi se desvanece cuando el sistema de tipos codifica la propiedad.

En **PHP**, el comentario del código señala una rareza que conviene conocer: `$copia = $nums;` **copia** el arreglo, no lo comparte. PHP aplica a los arreglos una semántica de valor con *copy-on-write* —internamente comparte los datos hasta que alguien escribe, y solo entonces duplica—, así que la copia es barata y el comportamiento observable es el de un valor independiente. Es la excepción entre los diez: en Python, JavaScript, Java o Go, esa misma línea habría compartido. Los objetos de PHP, en cambio, sí se manejan por referencia, y para ellos hace falta `clone`; Lockhart avisa en *Modern PHP* de esa asimetría entre arreglos y objetos.

Los diez imprimen `original=1-2-3 copia=1-2-99`; el verificador comprueba que la salida coincide carácter a carácter con lo que dicta `casos.json`.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `list(x)`/`x[:]` (Python), `[...x]` (JS), `clone()` (Rust/Java). |
| Semántica | Sin copiar, `b=a` comparte; hay que copiar explícitamente. |
| Paradigmática | SQL trabaja con conjuntos; no comparte referencias mutables. |

El eje que de verdad separa a los diez es **qué hace la asignación por defecto**, y no hay una respuesta única. En Python, JavaScript, TypeScript y Java, `b = a` sobre una colección **comparte**: copia la referencia y deja dos nombres sobre el mismo objeto. En C, copiar un arreglo exige un bucle o `memcpy`, porque el nombre del arreglo decae a puntero y `b = a` ni siquiera compila como copia. En Go, el `[]int` comparte el arreglo subyacente aunque la cabecera del slice se copie, mientras que un arreglo de tamaño fijo `[3]int` **sí** se copia entero al asignarlo: dos tipos parecidos con semánticas opuestas dentro del mismo lenguaje. En Rust, la asignación **mueve** la propiedad y el compilador impide usar el origen después, salvo que el tipo implemente `Copy` (como los enteros). Y PHP copia los arreglos por valor con *copy-on-write*. Cinco comportamientos distintos para la misma línea de código: no existe una intuición transferible, hay que saber el modelo de cada lenguaje.

El segundo eje es **cuánta ayuda ofrece la biblioteca para copiar en profundidad**. Python tiene `copy.copy` y `copy.deepcopy` en el módulo estándar, con detección de ciclos incluida. JavaScript tardó años en tener algo equivalente y hoy ofrece `structuredClone`, que copia grafos con ciclos pero se niega ante funciones y nodos del DOM; antes de él, el modismo `JSON.parse(JSON.stringify(x))` era habitual y también silenciosamente incorrecto, porque pierde `undefined`, convierte las fechas en cadenas y estalla con referencias circulares. Java no tiene copia profunda genérica: `Cloneable` y `clone()` son, en palabras del propio Bloch en *Effective Java*, un mecanismo defectuoso que conviene evitar en favor de un constructor de copia o un método de fábrica escrito a mano. C# ofrece `MemberwiseClone` para lo superficial y deja lo profundo al programador o a la serialización. En Rust y Go no hace falta un mecanismo especial porque los tipos que poseen sus datos ya los duplican al clonarse.

El tercer eje es **cómo el lenguaje evita el problema de raíz**. Rust lo hace con propiedad y préstamos verificados en compilación; los lenguajes funcionales, con inmutabilidad —si nada muta, compartir nunca se nota—; y SQL, por su modelo relacional: una consulta produce un conjunto de filas nuevo, sin punteros compartidos que alguien pueda mutar a espaldas de otro. Es la diferencia paradigmática de fondo: los demás lenguajes te dan la herramienta para copiar y confían en tu disciplina; estos tres hacen que el error no se pueda cometer.

## 🧬 El concepto en la familia

Los nombres del vocabulario de copia son bastante estables entre familias, pero su profundidad varía. En Ruby, `dup` y `clone` son ambos superficiales —`clone` conserva además el estado de congelado— y para lo profundo hay que recorrer a mano. En C++ el asunto está en el corazón del lenguaje: el **constructor de copia** y el operador de asignación definen qué significa copiar tu tipo, y la «regla de tres» (hoy de cinco) obliga a escribirlos coherentemente si tu clase gestiona memoria; el clásico error de la copia superficial de un puntero acaba en doble liberación al destruirse ambos objetos. Swift resuelve la misma tensión con *copy-on-write*, como PHP: sus arreglos y diccionarios se comportan como valores independientes, pero comparten el almacenamiento hasta que alguien escribe, de modo que pagas la copia solo cuando de verdad haces falta. Y la familia funcional —Haskell, Clojure, Elixir, Erlang— elimina la pregunta con **estructuras persistentes**: al «modificar» una lista o un mapa se obtiene una versión nueva que comparte con la anterior toda la parte no tocada, así que la copia es O(log n) o incluso O(1) y siempre es segura, porque nada de lo compartido puede cambiar. Ese es el patrón que conviene retener: la copia solo es un problema donde hay mutación, y cada familia lo ataca por un lado distinto —copiando con disciplina, copiando de forma perezosa, o no mutando nunca—.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 102
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Creer que asignar copia** → causa: en la mayoría de los lenguajes `b = a` sobre una colección solo duplica la referencia, y las dos variables acaban siendo el mismo objeto → solución: copiar explícitamente (`list(x)`, `[...x]`, `Arrays.copyOf`, `copy()`, `clone()`) siempre que necesites independencia, y saber de memoria qué hace la asignación en el lenguaje que estés usando.
- **Copia superficial con datos anidados** → causa: duplicaste el contenedor externo pero los elementos internos siguen siendo los mismos objetos; el bug desaparece en las pruebas con listas planas y reaparece con listas de listas → solución: copia profunda (`copy.deepcopy`, `structuredClone`) cuando haya anidamiento mutable, o hacer inmutables los niveles internos.
- **Mutar un parámetro sin avisar** → causa: la función ordena, vacía o reordena la colección que recibió, y el llamante encuentra su dato cambiado sin haberlo pedido → solución: copiar al entrar si vas a mutar, o documentar con claridad que la función muta su argumento; en Rust el propio `&mut` de la firma ya lo declara.
- **Guardar una referencia recibida como estado interno** → causa: el constructor asigna `this.lista = listaRecibida`, y quien la pasó puede seguir mutándola desde fuera, rompiendo los invariantes del objeto → solución: copia defensiva en el constructor y en el getter, o exponer una vista inmutable (`List.copyOf`, `Collections.unmodifiableList`).
- **Usar `JSON.parse(JSON.stringify(x))` como copia profunda en JavaScript** → causa: pierde los campos `undefined` y las funciones, convierte las fechas en cadenas, no soporta `Map`/`Set` y lanza excepción con referencias circulares → solución: `structuredClone(x)`, o una copia escrita a mano para los tipos implicados.
- **Copiar en profundidad cuando no hace falta** → causa: el error contrario, y también cuesta: una copia profunda de una estructura grande en cada llamada convierte una operación O(1) en O(n) y llena el heap de basura → solución: si el contenido es inmutable, compartirlo es correcto y gratis.

## ❓ Preguntas frecuentes

- **¿Copia superficial o profunda?** La pregunta útil no es cuántos niveles tiene la estructura, sino si el nivel que vas a compartir es **mutable**. Una lista de enteros, cadenas o tuplas puede copiarse superficialmente sin riesgo alguno. Una lista de listas, de diccionarios o de objetos mutables exige copia profunda si de verdad quieres independencia.
- **¿Los primitivos se comparten?** No: los enteros, reales y booleanos se copian al asignarse, porque el valor cabe en la propia variable. Las colecciones y los objetos se manejan por referencia en la mayoría de los lenguajes. Las excepciones importan: los `struct` de C, Go, Rust y C# se copian enteros al asignarse, y los arreglos de PHP también.
- **¿Cuánto cuesta cada copia?** La compartición es O(1) —copias un puntero—. La copia superficial es O(n) sobre los elementos del primer nivel. La copia profunda es proporcional al número total de nodos del grafo de objetos, y necesita además llevar registro de los ya visitados para no caer en bucle infinito con referencias circulares.
- **¿Cómo evito el problema del todo?** Haciendo inmutables tus datos. Si nadie puede mutar la estructura, compartirla es seguro y ya no hay nada que copiar: es la razón por la que la programación funcional casi no habla de copias, y por la que en Java conviene devolver `List.copyOf(...)` en vez de la lista interna.
- **¿Rust también tiene este problema?** No en tiempo de ejecución. Su sistema de propiedad lo convierte en un error de compilación: la asignación mueve el valor, `clone()` copia de forma explícita y visible, y el verificador de préstamos impide tener a la vez una referencia mutable y otra cualquiera al mismo dato. El precio es aprender esas reglas; el beneficio es que la clase entera de bugs de aliasing desaparece.

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

> [⏮️ Clase 101](../../parte-6-datos-y-estructuras/101-igualdad-vs-identidad/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 103 ⏭️](../../parte-6-datos-y-estructuras/103-propiedad-y-ciclo-de-vida-de-los-datos/README.md)
