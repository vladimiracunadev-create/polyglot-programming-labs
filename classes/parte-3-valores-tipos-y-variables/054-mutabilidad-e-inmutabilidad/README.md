# Clase 054 — Mutabilidad e inmutabilidad

> Parte **3 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Detrás de una pregunta aparentemente doméstica —¿cómo construyo la cadena `1-2-3-...-n`?— se esconde una de las decisiones más profundas del diseño de un lenguaje: ¿un valor puede cambiar una vez creado, o toda "modificación" produce un valor nuevo? Esta clase construye una secuencia numérica con el patrón *acumulador* para hacer palpable esa diferencia. Un acumulador que crece con `append` muta una estructura en su sitio; una lista que se junta al final con `join` trata cada pieza como inmutable y arma el resultado de una vez. Producen la misma salida, pero cuentan con dos filosofías distintas debajo.

La distinción importa por dos razones muy concretas. La primera es de **rendimiento**: en lenguajes donde las cadenas son inmutables (Java, C#, Python, JS), concatenar con `+` dentro de un bucle recrea toda la cadena en cada vuelta, un coste cuadrático O(n²) que colapsa con miles de elementos. Por eso existen los *builders* mutables —`StringBuilder`, `strings.Builder`— que reservan un búfer y escriben encima sin recopiar. La segunda es de **seguridad**: un valor inmutable se puede compartir entre hilos, usar como clave de un mapa o pasar a una función sin miedo a que alguien lo altere a tus espaldas. Como argumenta Bloch en *Effective Java*, los objetos inmutables son intrínsecamente seguros para hilos y más fáciles de razonar; su regla es minimizar la mutabilidad.

El eje que recorre la clase es quién decide, y por defecto qué. Rust invierte la costumbre: las variables son inmutables salvo que escribas `mut`. Java y C tienen `final`/`const` como opción explícita. Python distingue objetos mutables (listas) de inmutables (tuplas, cadenas). Y por debajo late la diferencia entre **valor y referencia** —modificar un objeto compartido a través de un alias afecta a todos los que lo referencian—, el fenómeno del *aliasing* que Scott analiza como el corazón de por qué la mutabilidad es a la vez potente y peligrosa.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Construir un resultado acumulando en un bucle.
2. Reconocer estructuras mutables (builder, lista).
3. Explicar el coste de concatenar cadenas inmutables.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Acumulador | Una variable que crece en cada vuelta |
| 2 | Mutable vs. inmutable | Modificar en sitio o crear nuevo |
| 3 | StringBuilder | Construir texto eficientemente |
| 4 | Coste de la inmutabilidad | Concatenar cadenas puede recrear todo |

## 📖 Definiciones y características

- **Mutabilidad** — capacidad de cambiar un valor in situ. Clave: eficiente para construir por partes.
- **Inmutabilidad** — el valor no cambia; toda 'modificación' crea uno nuevo. Clave: más seguro, a veces más caro.
- **Acumulador** — variable que reúne el resultado a lo largo de un bucle. Clave: patrón universal.
- **Builder** — estructura mutable para construir cadenas/colecciones (StringBuilder). Clave: evita recrear en cada paso.

La pareja **mutable / inmutable** describe qué le pasa a un valor cuando quieres "cambiarlo". Un valor mutable se modifica *in situ*: la misma celda de memoria pasa a contener otra cosa y todas las referencias a ella ven el cambio. Un valor inmutable no admite eso; cualquier "modificación" fabrica un valor nuevo y deja el original intacto. Esta no es una propiedad de la variable sino del objeto: en Python `x = 5; x = 6` no muta el 5 (los enteros son inmutables), simplemente reapunta el nombre `x` a otro objeto. Distinguir *reasignar el nombre* de *mutar el objeto* es la fuente de la mitad de las confusiones sobre este tema.

El **acumulador** es el patrón que hace visible la elección. En cada vuelta del bucle añades una pieza al resultado parcial. Si el acumulador es un *builder* mutable (`StringBuilder` en Java/C#, `strings.Builder` en Go), `append` escribe sobre un búfer que crece de forma amortizada y el coste total es lineal. Si en cambio acumulas concatenando cadenas inmutables con `+`, cada paso copia todo lo anterior y el coste se dispara a O(n²). Las variantes idiomáticas de Python y Rust esquivan el dilema de otra forma: juntan las piezas en una lista y llaman a `join`/`collect` una sola vez al final, de modo que la cadena grande se construye una vez.

La inmutabilidad, además, se paga y se cobra en distintas monedas. Cuesta más copias, pero regala seguridad: un valor que nadie puede alterar se comparte sin defensa, se hashea sin sorpresas y se razona sin rastrear quién lo tocó. Por eso las cadenas suelen ser inmutables incluso en lenguajes imperativos, y por eso `final` (Java), `const` (C) o la ausencia de `mut` (Rust) son afirmaciones de intención tanto para el compilador como para el lector.

## 🧩 Situación

Supón un informe que arma una tabla de 10.000 filas concatenando texto con `+=` dentro de un bucle. En un lenguaje de cadenas inmutables, la vuelta número 10.000 copia las 9.999 filas anteriores solo para añadir una más; el programa que "debería" tardar un instante se arrastra durante segundos. El síntoma es clásico y engañoso: funciona perfecto con datos de prueba pequeños y se degrada en producción. La cura es un builder mutable que escribe sobre un búfer, o acumular en una lista y unir al final.

Construir `1-2-...-n` es la versión mínima de ese problema. Es lo bastante pequeño para leerlo de un vistazo y lo bastante representativo para exhibir las dos estrategias —mutar un builder frente a juntar y unir— en los diez lenguajes. Y trae una trampa de borde propia del patrón: el separador va *entre* elementos, no antes del primero, así que el caso `n=1` debe dar `sec=1` sin guion sobrante.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n` (n >= 1)
- **Salida** (stdout): `sec=1-2-...-n` (números de 1 a n separados por guiones)
- **Regla:** sec = unir([1..n], separador='-')

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3` | `sec=1-2-3` |
| `1` | `sec=1` |
| `5` | `sec=1-2-3-4-5` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER n
acc <- vacío
PARA i de 1 a n: añadir i a acc
ESCRIBIR "sec=" UNIR(acc, "-")
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

n = int(sys.stdin.readline())
print("sec=" + "-".join(str(i) for i in range(1, n + 1)))
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
const parts = [];
for (let i = 1; i <= n; i++) parts.push(i);
console.log(`sec=${parts.join("-")}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
const parts: number[] = [];
for (let i = 1; i <= n; i++) parts.push(i);
console.log(`sec=${parts.join("-")}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        StringBuilder sb = new StringBuilder();
        for (int i = 1; i <= n; i++) {
            if (i > 1) sb.append("-");
            sb.append(i);
        }
        System.out.println("sec=" + sb);
    }
}
```

### C# · `dotnet run`

```csharp
using System;
using System.Text;

int n = int.Parse(Console.In.ReadToEnd().Trim());
var sb = new StringBuilder();
for (int i = 1; i <= n; i++) {
    if (i > 1) sb.Append("-");
    sb.Append(i);
}
Console.WriteLine($"sec={sb}");
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

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	n, _ := strconv.Atoi(strings.TrimSpace(line))
	var sb strings.Builder
	for i := 1; i <= n; i++ {
		if i > 1 {
			sb.WriteString("-")
		}
		sb.WriteString(strconv.Itoa(i))
	}
	fmt.Printf("sec=%s\n", sb.String())
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let parts: Vec<String> = (1..=n).map(|i| i.to_string()).collect();
    println!("sec={}", parts.join("-"));
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    printf("sec=");
    for (long i = 1; i <= n; i++) {
        if (i > 1) printf("-");
        printf("%ld", i);
    }
    printf("\n");
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL construye la secuencia con un CTE recursivo y group_concat (ilustrativo, n=5).
WITH RECURSIVE seq(i) AS (
    VALUES (1)
    UNION ALL SELECT i + 1 FROM seq WHERE i < 5
)
SELECT 'sec=' || group_concat(i, '-') AS resultado FROM seq;
```

### PHP · `php main.php`

```php
<?php
$n = (int) trim(fgets(STDIN));
$parts = [];
for ($i = 1; $i <= $n; $i++) {
    $parts[] = $i;
}
echo "sec=" . implode("-", $parts) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔎 Recorrido guiado por el código

Los diez programas leen `n` y emiten `sec=` seguido de los números de 1 a n unidos por guiones, pero se reparten en dos campos: los que **mutan** un builder y los que **juntan** una lista al final. Verlo en tres lenguajes fija la diferencia.

**Python** representa la vía inmutable-al-final. `"-".join(str(i) for i in range(1, n + 1))` genera cada número como cadena, los recoge y los une en una sola operación; `join` inserta el separador *entre* elementos, nunca al borde, así que el caso `n=1` de `casos.json` produce `sec=1` sin guiones sobrantes y el caso `n=3` produce `sec=1-2-3`. No hay acumulador mutable a la vista: la construcción cara ocurre una vez.

**Java** muestra el builder mutable explícito. Crea `StringBuilder sb = new StringBuilder();` y en el bucle hace `if (i > 1) sb.append("-"); sb.append(i);`. Cada `append` escribe sobre el búfer interno sin recrear la cadena, y el guard `i > 1` es el que evita el separador inicial —la traducción imperativa de lo que `join` hace por ti—. Al final `"sec=" + sb` convierte el builder a `String` una sola vez. Con `n=1` el `if` nunca se cumple y sale `sec=1`; con `n=5`, `sec=1-2-3-4-5`. Go sigue el mismo molde con `strings.Builder` y `WriteString`, evitando así la trampa de concatenar con `+` dentro del bucle.

**SQL** no itera: declara. Un CTE recursivo `WITH RECURSIVE seq(i) AS (VALUES (1) UNION ALL SELECT i + 1 FROM seq WHERE i < 5)` fabrica las filas 1..5 y `group_concat(i, '-')` las pega con guiones en un solo agregado. No hay ni mutación ni bucle explícito: el motor genera las filas y las combina. Por eso la implementación está fijada a `n=5` y el verificador la marca como *ilustrativa*; produce `sec=1-2-3-4-5`, la misma línea que los demás, pero por una vía declarativa.

## 🔬 Comparación

Aunque la salida es idéntica, el reparto revela dos escuelas: mutar un acumulador reservado (los builders) o tratar cada pieza como inmutable y combinarlas una sola vez (los `join`/`collect`). La primera domina donde las cadenas son inmutables y concatenar en bucle sería cuadrático; la segunda expresa lo mismo de forma más declarativa.

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `'-'.join(...)` (Python), `StringBuilder`/`strings.Builder` con `append` (Java/C#/Go), `(1..=n).map(...).collect()` + `join` (Rust). |
| Semántica | Java/C#/Go mutan un builder en cada vuelta; Python/Rust construyen una lista inmutable y la unen al final; ambas evitan el O(n²) de concatenar con `+`. |
| Paradigmática | SQL usa `group_concat` sobre filas de un CTE recursivo, sin bucle ni acumulador explícito. |
| Manejo del separador | Los builders necesitan un guard `if (i > 1)` para no poner guion inicial; `join`/`group_concat` lo insertan solo entre elementos por diseño. |

## 🧬 El concepto en la familia

En Ruby lo idiomático es `(1..n).to_a.join('-')`, mismo espíritu que Python. En Haskell, `intercalate "-" (map show [1..n])` es puramente inmutable: no hay estado que mutar, solo transformación de listas. En C++ el equivalente al builder es `std::ostringstream`, que acumula en un búfer sin recrear la cadena. Más allá de la sintaxis, la familia se ordena por su postura ante la mutabilidad por defecto: Rust la prohíbe salvo `mut` y persigue el aliasing mutable con su sistema de *ownership* y *borrowing*; los lenguajes funcionales (Haskell, Clojure) hacen de la inmutabilidad la norma y ofrecen estructuras persistentes que comparten memoria entre versiones; los imperativos clásicos son mutables por defecto y ofrecen la inmutabilidad como disciplina opcional (`final`, `const`, `readonly`, objetos inmutables al estilo *Effective Java*).

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 054
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Concatenar con `+` en un bucle grande** → causa: recrear toda la cadena en cada vuelta (O(n²)) → efecto: lentitud que solo aparece con muchos datos → solución: usar un builder mutable o juntar una lista y unir al final.
- **Olvidar el caso `n=1`** → causa: añadir el separador antes de comprobar si es el primer elemento → efecto: un guion sobrante (`sec=-1`) → solución: guard `if (i > 1)` o delegar en `join`, que no pone bordes.
- **Creer que reasignar una variable "muta" el valor** → causa: confundir el nombre con el objeto; en Python `s = s + "x"` crea una cadena nueva y el original no cambia → solución: distinguir reasignar de mutar (una lista con `list.append` sí muta in situ).
- **Compartir una estructura mutable sin querer (aliasing)** → causa: dos referencias al mismo objeto mutable; modificar una afecta a la otra → solución: copiar antes de compartir, o usar tipos inmutables/`final`.
- **Intentar mutar una cadena de Python/Java** → causa: son inmutables, no existe `str[i] = 'x'` → solución: construir una nueva con las piezas deseadas o usar un tipo mutable (`bytearray`, `StringBuilder`).

## ❓ Preguntas frecuentes

- **¿Siempre es mejor mutar?** No. Para construir por partes, un builder mutable es eficiente; para compartir datos entre hilos o usarlos como clave, la inmutabilidad es más segura. La regla de Bloch: minimiza la mutabilidad, hazla mutable solo cuando haya una razón.
- **¿Por qué las cadenas suelen ser inmutables?** Por seguridad y eficiencia: una cadena que nadie puede alterar se comparte sin copiar, se hashea de forma estable (clave de mapa) y evita errores por modificación a distancia.
- **¿`join` es más rápido que `StringBuilder`?** Son dos caras de la misma optimización: ambos evitan el O(n²) de `+` en bucle. `join`/`collect` recogen y unen una vez; el builder escribe sobre un búfer amortizado. La diferencia es de estilo, no de orden de complejidad.
- **¿Qué hace `final`/`const` exactamente?** Marcan que una referencia (o variable) no se reasigna. Ojo: en Java `final List` impide reapuntar la variable, pero la lista sigue siendo mutable por dentro. Inmutabilidad de la referencia no es inmutabilidad del objeto.
- **¿Por qué Rust es inmutable por defecto?** Para que el caso seguro sea el que menos escribes: si quieres mutar, lo declaras con `mut` y lo haces visible. Combinado con *ownership*, esto elimina en compilación toda una clase de errores de aliasing mutable.

## 🔗 Referencias

**Libros de la parte:**

- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson), asignación y variables (l-values, r-values).
- B. C. Pierce — *Types and Programming Languages* (MIT Press), referencias y estado mutable.
- M. L. Scott — *Programming Language Pragmatics* (4ª ed., Morgan Kaufmann), modelo de referencias y aliasing.

**Libros de los lenguajes del núcleo:**

- L. Ramalho — *Fluent Python* (2ª ed., O'Reilly) (inmutabilidad de tuplas y cadenas; mutable vs. inmutable).
- M. Haverbeke — *Eloquent JavaScript* (3ª ed.) — [gratis online](https://eloquentjavascript.net/) (`const`, objetos mutables).
- B. Cherny — *Programming TypeScript* (O'Reilly) (`readonly`, tipos inmutables).
- J. Bloch — *Effective Java* (3ª ed., Addison-Wesley) (minimizar la mutabilidad; clases inmutables; `StringBuilder`).
- J. Skeet — *C# in Depth* (4ª ed., Manning) (`readonly`, tipos inmutables).
- A. Donovan y B. Kernighan — *The Go Programming Language* (Addison-Wesley) (`strings.Builder`).
- S. Klabnik y C. Nichols — *The Rust Programming Language* — [gratis online](https://doc.rust-lang.org/book/) (inmutable por defecto, `mut`, ownership).
- B. Kernighan y D. Ritchie — *The C Programming Language* (2ª ed., Prentice Hall) (`const`).
- C. J. Date — *SQL and Relational Theory* (3ª ed., O'Reilly) (CTE recursivo, agregación).
- J. Lockhart — *Modern PHP* (O'Reilly) (arrays y cadenas).

---

> [⏮️ Clase 053](../../parte-3-valores-tipos-y-variables/053-nulabilidad-null-nil-none-option-y-valores-ausentes/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 055 ⏭️](../../parte-3-valores-tipos-y-variables/055-operadores-y-expresiones-aritmeticos-logicos-de-comparacion-y-bit-a-bit/README.md)
