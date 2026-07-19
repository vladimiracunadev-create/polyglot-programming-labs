# Clase 077 — Múltiples retornos y desestructuración

> Parte **5 — Funciones y modularidad** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Aprender a que una función entregue **más de un valor de una vez** y a repartir esos valores en variables al recibirlos. La firma de la clase 073 prometía «un valor sale»; muchas operaciones, sin embargo, producen naturalmente dos resultados hermanos que carece de sentido separar. Dividir da un cociente **y** un resto. Buscar un elemento da si se encontró **y** dónde. Parsear un texto da el valor **y** si tuvo éxito. `divmod(17, 5)` devuelve el `3` y el `2` juntos, en una sola llamada, y al otro lado `q, r = divmod(17, 5)` los reparte en dos nombres. Ese ida y vuelta —agrupar al devolver, desagrupar al recibir— es el corazón de la clase.

El motivo profundo es de abstracción de datos, y Abelson y Sussman lo colocan en el centro de *Structure and Interpretation of Computer Programs* (§2.1): construir **valores compuestos** —agrupar varias piezas en un objeto que se maneja como una sola unidad— eleva el nivel al que diseñamos, porque permite tratar «cociente y resto» como una cosa que se pasa, se devuelve y se nombra de golpe. La tupla es la encarnación mínima de esa idea: un grupo ordenado de valores sin la ceremonia de declarar una clase. Robert Martin, en *Clean Code*, añade el reverso ético: devolver dos resultados por el canal legítimo del retorno es más honesto que la alternativa clásica de modificar un argumento de salida por referencia, un efecto lateral que oculta la mitad de lo que la función hace.

El reparto entre lenguajes vuelve a ser instructivo. Go hizo del retorno múltiple una seña de identidad —`(valor, error)` es su idioma para el manejo de errores— y Python devuelve una tupla que se desempaqueta sola. Rust usa tuplas `(a, b)`; JavaScript y TypeScript devuelven un arreglo o un objeto y lo desestructuran con `[a, b]` o `{a, b}`. En el otro campo, Java y C solo pueden devolver **un** valor: Java lo resuelve empaquetando los resultados en un objeto o `record`, y C recurre a la técnica antigua de devolver uno y escribir el otro a través de un puntero de salida. Reconocer en qué campo está tu lenguaje decide si el multi-retorno es una frase natural o un patrón que hay que montar a mano.

## 🧩 Situación

Escribes la lógica de un reloj que convierte segundos totales en minutos y segundos restantes: 125 segundos son 2 minutos y 5 segundos. La operación produce inevitablemente dos números atados entre sí. Sin multi-retorno, tus salidas son todas incómodas: llamas a la función dos veces —una para los minutos y otra para los segundos, repitiendo el cálculo—, o inventas una clase `TiempoDividido` solo para transportar dos enteros que nunca volverás a usar, o —peor— haces que la función escriba uno de los resultados en una variable que le pasas por referencia, escondiendo la mitad de su trabajo. El multi-retorno ofrece la salida limpia: `minutos, segundos = dividir_tiempo(125)`, un cálculo, dos valores, dos nombres. En esta clase practicamos el arquetipo de esa operación, `divmod(a, b)`, que devuelve cociente y resto a la vez —`3` y `2` para `17 5`— y se desestructura en `q, r` sin intermediarios.

## 🧮 Modelo

- **Entrada** (stdin): una línea `a b` (enteros positivos, b != 0)
- **Salida** (stdout): `cociente=<a/b> resto=<a%b>`
- **Regla:** (cociente, resto) = (a/b, a%b)

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `17 5` | `cociente=3 resto=2` |
| `10 2` | `cociente=5 resto=0` |
| `7 3` | `cociente=2 resto=1` |

## 📖 Definiciones y características

- **Retorno múltiple** — la capacidad de una función de devolver varios valores en una sola llamada, sin envolverlos en un objeto que el llamador tenga que abrir. Es nativo en Go, Python y Rust; en Go es además el pilar de su convención `(resultado, error)`.
- **Tupla** — un grupo ordenado y a menudo inmutable de valores, posiblemente de tipos distintos, tratado como una sola unidad. Es el vehículo habitual del multi-retorno y la realización más simple del «valor compuesto» de SICP: agrupa sin obligar a nombrar ni a declarar una clase.
- **Desestructuración (destructuring)** — la operación de recibir una tupla, arreglo u objeto y repartir sus componentes en variables separadas en un solo paso: `q, r = divmod(a, b)`. Es la contraparte del empaquetado; sin ella, el multi-retorno obligaría a extraer cada campo por índice a mano.
- **Struct / objeto de salida** — la alternativa de los lenguajes sin multi-retorno nativo: se define un tipo que agrupa los resultados con nombre —el `record DivRes` de Java— y se devuelve esa única instancia. Aporta nombres a los valores a cambio de declarar un tipo.
- **Parámetro de salida (out param)** — la técnica de C: devolver un valor por `return` y entregar los demás escribiéndolos en direcciones de memoria que el llamador pasa por puntero. Funciona, pero Martin lo señala en *Clean Code* como menos claro, porque parte del resultado viaja de forma oculta a través de los argumentos.

## 📐 Algoritmo (pseudocódigo neutral)

```text
FUNCION divmod(a,b): DEVOLVER (a/b, a%b)
LEER a,b ; (q,r) <- divmod(a,b) ; ESCRIBIR q, r
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys


def divmod2(a, b):
    return a // b, a % b


a, b = map(int, sys.stdin.readline().split())
q, r = divmod2(a, b)
print(f"cociente={q} resto={r}")
```

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

function divmod(a, b) {
  return [Math.trunc(a / b), a % b];
}

const [a, b] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const [q, r] = divmod(a, b);
console.log(`cociente=${q} resto=${r}`);
```

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

function divmod(a: number, b: number): [number, number] {
  return [Math.trunc(a / b), a % b];
}

const [a, b]: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const [q, r]: [number, number] = divmod(a, b);
console.log(`cociente=${q} resto=${r}`);
```

### Java · [`java/Main.java`](implementaciones/java/Main.java) · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    // Java devuelve un objeto (record) para varios valores.
    record DivRes(int cociente, int resto) {}

    static DivRes divmod(int a, int b) {
        return new DivRes(a / b, a % b);
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        DivRes d = divmod(Integer.parseInt(p[0]), Integer.parseInt(p[1]));
        System.out.println("cociente=" + d.cociente() + " resto=" + d.resto());
    }
}
```

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;

(int, int) Divmod(int a, int b) => (a / b, a % b);

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
var (q, r) = Divmod(int.Parse(p[0]), int.Parse(p[1]));
Console.WriteLine($"cociente={q} resto={r}");
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

func divmod(a, b int) (int, int) {
	return a / b, a % b
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	f := strings.Fields(line)
	a, _ := strconv.Atoi(f[0])
	b, _ := strconv.Atoi(f[1])
	q, r := divmod(a, b)
	fmt.Printf("cociente=%d resto=%d\n", q, r)
}
```

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn divmod(a: i64, b: i64) -> (i64, i64) {
    (a / b, a % b)
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let v: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    let (q, r) = divmod(v[0], v[1]);
    println!("cociente={q} resto={r}");
}
```

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

/* C devuelve un valor; el segundo va por puntero. */
long divmod(long a, long b, long *resto) {
    *resto = a % b;
    return a / b;
}

int main(void) {
    long a, b, r;
    if (scanf("%ld %ld", &a, &b) != 2) return 1;
    long q = divmod(a, b, &r);
    printf("cociente=%ld resto=%ld\n", q, r);
    return 0;
}
```

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL: varias columnas por fila son un multi-retorno natural.
WITH pares(a, b) AS (VALUES (17, 5), (10, 2), (7, 3))
SELECT printf('cociente=%d resto=%d', a / b, a % b) AS resultado FROM pares;
```

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
function divmod($a, $b) {
    return [intdiv($a, $b), $a % $b];
}

[$a, $b] = preg_split('/\s+/', trim(fgets(STDIN)));
[$q, $r] = divmod((int) $a, (int) $b);
echo "cociente=$q resto=$r\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Ejemplo trabajado — del stdin a la salida

Sigamos el primer caso de `casos.json` (`stdin = "17 5"`, `esperado = "cociente=3 resto=2"`) por cuatro lenguajes que reparten los dos resultados de maneras que revelan sus filosofías: tupla desempaquetada, multi-retorno nativo, objeto contenedor y puntero de salida.

**Python (tupla implícita + desempaquetado).** Tras leer `a=17, b=5`, la función `divmod2` ejecuta `return a // b, a % b`. La coma es lo esencial: `17 // 5` da `3`, `17 % 5` da `2`, y la coma construye la tupla `(3, 2)` sin que aparezca ningún paréntesis explícito. En el sitio de llamada, `q, r = divmod2(a, b)` desestructura esa tupla, asignando `q=3` y `r=2` en un solo paso. El f-string produce `cociente=3 resto=2`. Todo el mecanismo —agrupar con una coma, repartir con una coma— es tan ligero que casi no se ve, y esa es precisamente la virtud del valor compuesto que describe SICP.

**Go (retorno múltiple nativo).** La firma `func divmod(a, b int) (int, int)` declara dos tipos de retorno entre paréntesis, algo imposible en Java o C. El cuerpo `return a / b, a % b` devuelve `3` y `2` como dos valores independientes, no como una tupla que haya que abrir. La línea `q, r := divmod(a, b)` los recibe directamente en dos variables. Aquí se ve por qué Go convirtió esto en su idioma para errores: la misma sintaxis que devuelve `cociente, resto` devuelve en la biblioteca estándar `valor, error`, y el llamador siempre recibe ambos por el canal limpio del retorno.

**Java (objeto contenedor).** Java solo puede devolver un valor, así que declara un `record DivRes(int cociente, int resto)` —un tipo inmutable con dos campos nombrados— y `divmod` devuelve `new DivRes(a / b, a % b)`, es decir, una sola instancia que encierra el `3` y el `2`. No hay desestructuración: en `main` se recuperan uno a uno con los accesores `d.cociente()` y `d.resto()`. Java gana nombres para los resultados —imposible confundir cuál es cuál— a cambio de declarar un tipo y renunciar al reparto en una línea.

**C (parámetro de salida por puntero).** C también devuelve un solo valor, y su solución es la más antigua: `long divmod(long a, long b, long *resto)` devuelve el cociente por `return` y escribe el resto en la dirección que recibe. En `main`, la variable `r` se declara vacía y se pasa su dirección con `&r`; dentro de la función, `*resto = a % b` deposita el `2` en la memoria de `r`, mientras `return a / b` entrega el `3`. Tras la llamada, `q` vale `3` y `r` vale `2`. Funciona y produce `cociente=3 resto=2`, pero ilustra justo lo que Martin critica: la mitad del resultado viaja escondida a través de un argumento, no del retorno visible.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Multi-retorno directo con reparto —`q, r = ...` (Python, Go, Rust, C#), `[q, r] = ...` (JS/TS, PHP)— frente a objeto contenedor (Java) o puntero de salida (C). |
| Semántica | Go devuelve varios valores **independientes**; Python, Rust, C# y JS/TS devuelven **una** estructura (tupla o arreglo) que la desestructuración abre; Java devuelve **un** objeto cuyos campos se leen con accesores. |
| Semántica | En C parte del resultado sale por el retorno y parte por un argumento que se muta vía puntero, un efecto lateral que los demás lenguajes evitan al usar el canal del retorno. |
| Paradigmática | La tupla es anónima (posición) mientras que la struct/`record` da nombre a cada valor: tupla para pocos valores efímeros, struct cuando el significado merece un nombre estable. |
| Paradigmática | SQL entrega varias columnas por fila de forma nativa: un `SELECT` que produce `cociente` y `resto` es un multi-retorno declarativo sin desestructuración explícita. |

La síntesis reúne a los dos autores de la parte. Abelson y Sussman explican **por qué** el multi-retorno importa: agrupar valores en una unidad compuesta sube el nivel de abstracción, y la tupla es su forma más barata. Martin explica **cómo** hacerlo bien: preferir el canal honesto del retorno al truco del argumento de salida. Entre esos dos polos se ordenan los diez lenguajes: los que tienen tupla o multi-retorno nativo (Python, Go, Rust, C#) expresan la idea en una línea; los que no (Java, C) la reconstruyen con un objeto o un puntero, pagando en verbosidad o en claridad lo que les falta de sintaxis.

## 🧬 El concepto en la familia

En **Ruby**, `return q, r` empaqueta automáticamente una tupla-arreglo que el llamador desestructura con `q, r = ...`, casi calcado de Python. **Kotlin** no tiene tuplas de longitud arbitraria pero ofrece `Pair` y `Triple`, y para más valores o nombres significativos empuja hacia una `data class` con desestructuración por `componentN()`: `val (q, r) = divmod(a, b)`. **Swift** sí tiene tuplas nativas y hasta permite nombrar sus componentes —`func divmod() -> (cociente: Int, resto: Int)`—, uniendo la ligereza de la tupla con la claridad de los nombres. **Scala** también trae tuplas de primera clase (`(Int, Int)`) con desestructuración en `val (q, r) = ...`. La familia se ordena por una pregunta: ¿la tupla es un ciudadano de pleno derecho (Python, Rust, Swift, Scala) o hay que sustituirla por un `Pair`/`data class` (Kotlin) o un objeto (Java)?

## ⚠️ Errores comunes

- **Devolver un objeto solo para dos valores efímeros** → causa: declarar una clase contenedora en lenguajes que ya tienen tuplas, añadiendo ceremonia sin ganar nada → solución: usa el multi-retorno o la tupla nativa cuando exista; reserva la struct/`record` para cuando los valores merezcan nombres estables y reutilizables.
- **Equivocar el orden en la desestructuración** → causa: escribir `r, q = divmod(a, b)` y asignar el cociente al resto porque el reparto es puramente posicional → solución: respeta el orden en que la función devuelve los valores; si el orden es fácil de confundir, considera una struct con nombres.
- **Olvidar tomar el segundo valor en lenguajes que lo exigen** → causa: en Go, ignorar el `error` de un retorno `(valor, error)` o dejar una variable sin usar → solución: recibe todos los valores y descarta explícitamente con `_` los que de verdad no necesites.
- **Pasar mal el puntero de salida en C** → causa: pasar la variable por valor en vez de su dirección, o desreferenciar un puntero no inicializado, corrompiendo memoria → solución: pasa `&variable` y asegúrate de que apunta a memoria válida antes de escribir en `*resto`.

## ❓ Preguntas frecuentes

- **¿Tupla o struct?** Tupla para pocos valores anónimos y efímeros, donde la posición basta; struct o `record` cuando cada valor merece un nombre y el tipo se va a reutilizar. Es un intercambio entre ligereza y claridad.
- **¿Java tiene multi-retorno?** No de forma nativa: solo devuelve un valor. Se empaquetan los resultados en un objeto o `record` con campos nombrados y se leen con accesores.
- **¿Por qué Go usa multi-retorno para los errores?** Porque le permite devolver `(valor, error)` por el mismo canal limpio del retorno, sin excepciones ni argumentos ocultos; el llamador recibe siempre el resultado y su posible fallo juntos.
- **¿La desestructuración funciona con cualquier retorno?** Funciona sobre estructuras posicionales o con claves: tuplas y arreglos por posición (`[q, r]`), objetos por nombre (`{a, b}`). Un objeto de Java que solo expone accesores no se desestructura: sus campos se leen uno a uno.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 077
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## 🔗 Referencias

**Libros de la parte:**

- H. Abelson y G. J. Sussman — *Structure and Interpretation of Computer Programs* (2ª ed., MIT Press), §2.1 sobre valores compuestos y abstracción de datos.
- R. C. Martin — *Clean Code* (Prentice Hall), cap. 3 «Functions», sobre evitar argumentos de salida.
- S. McConnell — *Code Complete* (2ª ed., Microsoft Press), cap. 7 «High-Quality Routines».

**Libros de los lenguajes del núcleo:**

- L. Ramalho — *Fluent Python* (2ª ed., O'Reilly), cap. 2 sobre tuplas y desempaquetado.
- M. Haverbeke — *Eloquent JavaScript* (3ª ed.) — [gratis online](https://eloquentjavascript.net/).
- B. Cherny — *Programming TypeScript* (O'Reilly), sobre tipos tupla.
- J. Bloch — *Effective Java* (3ª ed., Addison-Wesley).
- J. Skeet — *C# in Depth* (4ª ed., Manning), sobre tuplas de valor.
- A. Donovan y B. Kernighan — *The Go Programming Language* (Addison-Wesley), sobre retorno múltiple y la convención `(valor, error)`.
- S. Klabnik y C. Nichols — *The Rust Programming Language* — [gratis online](https://doc.rust-lang.org/book/).
- B. Kernighan y D. Ritchie — *The C Programming Language* (2ª ed., Prentice Hall), sobre punteros como argumentos de salida.
- C. J. Date — *SQL and Relational Theory* (3ª ed., O'Reilly).
- J. Lockhart — *Modern PHP* (O'Reilly).

---

> [⏮️ Clase 076](../../parte-5-funciones-y-modularidad/076-parametros-variadicos/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 078 ⏭️](../../parte-5-funciones-y-modularidad/078-genericos-y-polimorfismo-parametrico/README.md)
