# Clase 126 — AOT vs. JIT: costos y beneficios

> Parte **8 — Cómo funcionan los lenguajes** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

La clase 124 presentó el JIT; esta lo enfrenta cara a cara con la compilación **AOT** (*ahead-of-time*) para entender un compromiso de ingeniería que se paga en cada despliegue real. Con el cálculo trivial de `2^n`, aislamos la única variable que importa: *cuándo* se traduce el código a instrucciones de la CPU. En AOT (C, Rust, Go), toda la traducción ocurre antes de distribuir el programa: obtienes un binario que arranca al instante pero que no puede reoptimizarse con lo que ocurra en ejecución. En JIT (JVM, V8), el programa llega sin traducir del todo y el motor compila las partes *calientes* mientras corre, alcanzando o superando al AOT tras un periodo de *calentamiento*. El *porqué* es económico: la CLI que un usuario invoca mil veces al día necesita arranque instantáneo, así que AOT; el servidor que corre semanas puede permitirse calentar para exprimir el pico, así que JIT. No hay ganador absoluto —hay un eje *arranque contra pico sostenido* sobre el que cada proyecto elige su punto.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Calcular una potencia de dos por iteración o por operador de potencia.
2. Explicar la diferencia AOT/JIT en términos de *cuándo* y *con qué información* se compila.
3. Relacionar cada modelo con su perfil de arranque, memoria y rendimiento sostenido.
4. Justificar por qué existe GraalVM y qué compromiso resuelve.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | AOT | Toda la traducción por adelantado: arranque instantáneo, sin reoptimización |
| 2 | JIT | Compila lo caliente en ejecución, con los tipos reales observados |
| 3 | Arranque vs. pico | El compromiso central que decide qué modelo conviene a cada carga |

## 📖 Definiciones y características

La **compilación AOT** traduce el programa completo a código de máquina antes de que se ejecute una sola vez. El binario que produce `cc`, `rustc` o `go build` es autónomo: no lleva compilador dentro y no consume tiempo ni memoria en traducir durante la ejecución. Su fortaleza es el arranque —un `exec` y a correr— y su predecibilidad; su límite es que el compilador solo conoce lo que podía deducir estáticamente, sin ver los datos reales.

La **compilación JIT** difiere la traducción al momento de ejecución. El motor arranca interpretando y perfila el código; cuando una función supera un umbral de invocaciones —se vuelve *código caliente*—, la compila a máquina optimizándola con información que el AOT nunca tuvo: los tipos concretos, las ramas que de verdad se toman, los valores frecuentes. Ese *feedback* dinámico puede producir código más rápido que el AOT, pero cuesta: memoria para el compilador y las versiones compiladas, y un arranque más lento mientras se calienta.

El **código caliente** es la porción del programa que se ejecuta muchísimas veces —el bucle interno, la función del *hot path*—. Es donde el JIT concentra su inversión, porque optimizar código que se ejecuta una sola vez no compensa el coste de compilarlo. Esta asimetría explica por qué un microbenchmark mal hecho «castiga» injustamente al JIT: si no lo dejas calentar, mides solo su fase interpretada.

## 🧩 Situación

Publicas dos servicios equivalentes, uno en Go (AOT) y otro en Java (JIT), y observas algo desconcertante: bajo una prueba de carga breve, Go parece más rápido; bajo una prueba de horas, Java lo alcanza y a veces lo supera. Ninguno «miente»: mides puntos distintos del eje arranque-pico. El cálculo de `2^n`, idéntico en resultado (`resultado=8`), te deja separar el modelo de compilación del algoritmo y razonar sobre ese compromiso sin ruido.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n` (0 <= n <= 60)
- **Salida** (stdout): `resultado=<2^n>`
- **Regla:** 2 elevado a n

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3` | `resultado=8` |
| `0` | `resultado=1` |
| `5` | `resultado=32` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
multiplicar 2 por sí mismo n veces (o desplazar bits)
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys

n = int(sys.stdin.readline())
print(f"resultado={2 ** n}")
```

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
let r = 1;
for (let i = 0; i < n; i++) r *= 2;
console.log(`resultado=${r}`);
```

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
let r = 1;
for (let i = 0; i < n; i++) r *= 2;
console.log(`resultado=${r}`);
```

### Java · [`java/Main.java`](implementaciones/java/Main.java) · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        long r = 1;
        for (int i = 0; i < n; i++) r *= 2;
        System.out.println("resultado=" + r);
    }
}
```

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;

int n = int.Parse(Console.In.ReadToEnd().Trim());
long r = 1;
for (int i = 0; i < n; i++) r *= 2;
Console.WriteLine($"resultado={r}");
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
	n, _ := strconv.Atoi(strings.TrimSpace(line))
	var r int64 = 1
	for i := 0; i < n; i++ {
		r *= 2
	}
	fmt.Printf("resultado=%d\n", r)
}
```

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: u32 = s.trim().parse().unwrap();
    let r: i64 = 2i64.pow(n);
    println!("resultado={r}");
}
```

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    int n;
    if (scanf("%d", &n) != 1) return 1;
    long r = 1;
    for (int i = 0; i < n; i++) r *= 2;
    printf("resultado=%ld\n", r);
    return 0;
}
```

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL: potencia con un CTE recursivo (ilustrativo, n=3).
WITH RECURSIVE p(i, v) AS (VALUES (0, 1) UNION ALL SELECT i + 1, v * 2 FROM p WHERE i < 3)
SELECT printf('resultado=%d', v) AS resultado FROM p ORDER BY i DESC LIMIT 1;
```

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
$n = (int) trim(fgets(STDIN));
$r = 1;
for ($i = 0; $i < $n; $i++) {
    $r *= 2;
}
echo "resultado=$r\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🧪 Laboratorio: recorrido del código

El mismo `2^n` toma dos formas que iluminan el eje AOT/JIT: un bucle explícito y un operador de potencia.

En **C**, `for (int i = 0; i < n; i++) r *= 2;` es un bucle que `cc` compila a un puñado de instrucciones de máquina *antes* de que exista la entrada. Con optimización activada, un compilador AOT puede incluso reconocer el patrón y sustituir la multiplicación repetida por un desplazamiento de bits (`1 << n`), porque tiene tiempo de sobra para analizar. Ese análisis ocurre una vez, en tu máquina de compilación, y el usuario recibe el resultado ya cocinado: cero coste en ejecución.

En **Java**, el mismo `for (int i = 0; i < n; i++) r *= 2;` llega a la JVM como bytecode. En la primera ejecución se interpreta; si este bucle se ejecutara en un servicio millones de veces, HotSpot lo detectaría como caliente y lo recompilaría a máquina, quizá desenrollándolo o vectorizándolo con datos de perfil. Para nuestro caso de una sola pasada con `n ≤ 60`, el JIT nunca se activa: pagamos arranque de JVM sin cosechar su pico. Es la cara amarga del compromiso cuando la carga es corta.

En **Rust**, `2i64.pow(n)` delega en una función de la biblioteca estándar ya compilada AOT dentro del binario. Como Rust es AOT igual que C, no hay calentamiento ni interpretación: el binario contiene `pow` en código de máquina y lo invoca directo. El contraste entre `2i64.pow(n)` (Rust/AOT) y el mismo cálculo sobre la JVM resume la clase: idéntico resultado, distinto momento de traducción y, por tanto, distinto perfil de arranque frente a pico.

## 🔬 Comparación

| Rasgo | Cómo se reparte entre los 10 lenguajes |
|---|---|
| Momento de traducción | Antes de distribuir: C, Rust, Go. En ejecución: Java, C#, JS (JIT). |
| Arranque | Inmediato en AOT; con carga de VM y calentamiento en JIT. |
| Reoptimización con datos reales | Imposible en AOT (ya compilado); es la ventaja central del JIT. |
| Memoria en ejecución | Menor en AOT; mayor en JIT (aloja compilador + código generado). |
| SQL | El motor planifica y ejecuta la consulta; el CTE recursivo calcula la potencia de forma ilustrativa. |

## 🧬 El concepto en la familia

El eje AOT/JIT no parte los lenguajes en dos bandos limpios. Go, Rust y C son AOT puros. La JVM y V8 son JIT. Pero GraalVM compila Java AOT a *imagen nativa* para arrancar en milisegundos —sacrificando el pico del JIT— justo para escenarios *serverless* donde el arranque manda; y .NET ofrece *ReadyToRun* y AOT nativo por la misma razón. Incluso el kernel de Python explora compilación especializada. La conclusión de fondo, alineada con *Crafting Interpreters*, es que «cuándo compilar» es una perilla de diseño, no una propiedad inmutable del lenguaje.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 126
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Comparar AOT y JIT sin dejar calentar** → causa: un microbenchmark corto mide la fase interpretada del JIT y lo pinta artificialmente lento → solución: ejecutar miles de iteraciones antes de cronometrar, o medir el régimen sostenido.
- **Desbordar el entero con `n` grande** → causa: `2^64` no cabe en un entero de 64 bits → solución: el contrato limita `n ≤ 60`, donde el resultado cabe en `long`/`i64`.
- **Inicializar el acumulador en 0** → causa: un producto que parte de 0 siempre da 0 → solución: el elemento neutro de la multiplicación es 1, así que `r` empieza en 1.

## ❓ Preguntas frecuentes

- **¿AOT o JIT es mejor?** Ninguno en abstracto. AOT gana en arranque, binarios pequeños y previsibilidad; JIT gana en régimen sostenido gracias a la optimización guiada por perfil. Elige según la vida útil del proceso.
- **¿Se pueden combinar?** Sí: GraalVM *native-image* y .NET AOT compilan anticipadamente plataformas que nacieron JIT, y muchos motores usan compilación por niveles (interpretar → JIT rápido → JIT optimizado).
- **¿Por qué el JIT puede superar al AOT?** Porque optimiza con información dinámica —tipos reales, ramas frecuentes— que un compilador anticipado no puede conocer.

## 🔗 Referencias

**Libros de la parte:**

- R. Nystrom — *Crafting Interpreters* (Genever Benning) — [gratis online](https://craftinginterpreters.com/).
- A. Aho, M. Lam, R. Sethi y J. Ullman — *Compilers: Principles, Techniques, and Tools* (2ª ed., Pearson; «Dragon Book»).
- R. Bryant y D. O'Hallaron — *Computer Systems: A Programmer's Perspective* (3ª ed., Pearson).

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

> [⏮️ Clase 125](../../parte-8-como-funcionan-los-lenguajes/125-bytecode-y-maquinas-virtuales-jvm-clr-v8/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 127 ⏭️](../../parte-8-como-funcionan-los-lenguajes/127-la-pila-stack-y-el-marco-de-llamada/README.md)
