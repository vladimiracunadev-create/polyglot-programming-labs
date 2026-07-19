# Clase 150 — Refactorización segura

> Parte **9 — Ingeniería de software políglota** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Fowler abre su libro *Refactoring* con una definición que conviene grabar palabra por palabra: refactorizar es **cambiar la estructura interna del código sin alterar su comportamiento observable**. Las dos mitades de esa frase son igual de importantes. "Cambiar la estructura interna" es la libertad: renombrar, extraer una función, reorganizar; "sin alterar el comportamiento observable" es la restricción sagrada: lo que el usuario y las pruebas ven debe quedar idéntico. Si cambias el comportamiento, no estás refactorizando —estás modificando el software—, y mezclar ambas cosas es la receta clásica del desastre, porque cuando algo se rompe no sabes si fue el cambio de estructura o el de conducta.

Lo que hace *segura* a la refactorización es la **red de pruebas**. Beck, en *Test-Driven Development: By Example*, describe el ritmo que Fowler adopta: un conjunto de pruebas verdes es una red bajo el trapecista; con ella puedes reestructurar con confianza, porque si un paso rompe el comportamiento, una prueba se pone roja al instante y te dice exactamente dónde. Sin pruebas, cada refactorización es un acto de fe. Con ellas, es rutina. Por eso Fowler insiste en **pasos pequeños**: cambios diminutos, cada uno seguido de correr las pruebas, de modo que si algo falla la causa esté en las últimas líneas que tocaste, no perdida entre cientos.

El programa de `casos.json` captura la esencia con un ejemplo mínimo: sustituir `n*2` por `n+n`. Son dos expresiones distintas —dos "estructuras"— que producen el mismo resultado —el mismo "comportamiento"—, y el programa lo *verifica* comparando ambas y confirmando la equivalencia. Es una refactorización de juguete, pero encierra el patrón entero: cambia la forma, comprueba que la conducta se preserva. Detrás de esa comprobación están los **malos olores** (code smells) que motivan refactorizar —código duplicado, funciones largas, nombres opacos— y los refactors clásicos que Fowler cataloga: *extract function*, *rename*, *inline*.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. **Definir** la refactorización como cambio de estructura que preserva el comportamiento observable, y distinguirla de un cambio funcional.
2. **Verificar** la equivalencia de dos formas de un cálculo con una prueba que actúa como red de seguridad.
3. **Explicar** por qué las pruebas verdes habilitan refactorizar en pasos pequeños y con confianza.
4. **Reconocer** malos olores comunes y nombrar los refactors clásicos que los curan (extract function, rename).

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Refactorización | Mejorar la estructura sin cambiar la conducta |
| 2 | Comportamiento observable | Lo que debe permanecer idéntico |
| 3 | Red de pruebas | Habilita el cambio seguro y en pasos pequeños |
| 4 | Malos olores y refactors clásicos | Cuándo y cómo reestructurar |

## 📖 Definiciones y características

- **Refactorización** — según Fowler, una transformación que reestructura el código sin cambiar su comportamiento observable, con el fin de hacerlo más fácil de entender y más barato de modificar. No añade funciones ni corrige bugs (eso es otra cosa): mejora la forma para que los cambios futuros duelan menos.
- **Comportamiento observable** — todo lo que el mundo exterior percibe: las salidas para unas entradas dadas, los efectos visibles. Es exactamente lo que las pruebas fijan y lo que una refactorización promete no tocar. En este ejercicio, `resultado=10` para `n=5` es el comportamiento; que se calcule con `n*2` o `n+n` es estructura.
- **Red de seguridad (safety net)** — el conjunto de pruebas que, al seguir en verde tras cada paso, garantiza que la conducta no cambió. Beck la considera el prerrequisito psicológico de la refactorización: convierte una operación arriesgada en un hábito cotidiano.
- **Malos olores (code smells)** — síntomas superficiales de problemas de diseño más hondos: duplicación, funciones demasiado largas, nombres crípticos, clases que hacen de todo. No son bugs, pero señalan dónde refactorizar. Los refactors clásicos son sus antídotos: *extract function* parte una función larga, *rename* pone nombres que revelan la intención, *inline* elimina indirecciones inútiles.

## 🧩 Situación

Tienes una función central que un test cubre bien: para cada entrada conocida produce una salida conocida, y todas esas pruebas están verdes. Te das cuenta de que su implementación es innecesariamente enrevesada y quieres simplificarla. Aquí es donde la red de pruebas gana su sueldo: haces un cambio pequeño —por ejemplo, reemplazas una expresión por otra equivalente—, corres las pruebas y, si siguen verdes, sabes que el comportamiento observable no se movió. Repites en pasos diminutos hasta que la estructura queda limpia. El programa de esta clase modela ese ciclo en su forma más pura: calcula el resultado "viejo" (`n*2`) y el "nuevo" (`n+n`), comprueba que coinciden y lo declara `equivalente=true`. Es una refactorización con su propia prueba de equivalencia incorporada: la garantía de que cambiar la forma no cambió el fondo.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n`
- **Salida** (stdout): `equivalente=<true|false> resultado=<2n>`
- **Regla:** viejo = n*2 ; nuevo = n+n ; equivalente si coinciden

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `equivalente=true resultado=10` |
| `0` | `equivalente=true resultado=0` |
| `7` | `equivalente=true resultado=14` |

## 📐 Algoritmo (pseudocódigo neutral)

El algoritmo *es* una refactorización verificada: calcula ambas formas y comprueba que la conducta se preserva antes de dar el cambio por bueno.

```text
viejo <- n*2 ; nuevo <- n+n ; equivalente <- (viejo==nuevo) ; ESCRIBIR
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

La versión de Python pone a la vista el patrón entero de una refactorización verificada. `viejo` guarda la forma antigua (`n * 2`), `nuevo` la refactorizada (`n + n`), y `viejo == nuevo` es la prueba en línea que confirma la equivalencia. Fíjate en que el programa nunca *asume* que son iguales: lo comprueba, igual que un test comprueba que la conducta sigue intacta tras reestructurar. La salida imprime tanto el veredicto (`equivalente=true`) como el resultado observable (`resultado=10`), separando limpiamente "la estructura cambió" de "el comportamiento se preservó".

```python
import sys

n = int(sys.stdin.readline())
viejo = n * 2
nuevo = n + n
eq = "true" if viejo == nuevo else "false"
print(f"equivalente={eq} resultado={nuevo}")
```

Para `n=5`, `viejo` es 10 y `nuevo` es 10: iguales, así que `equivalente=true resultado=10`. Para `n=0`, ambos son 0. Para `n=7`, ambos 14. La equivalencia de `n*2` y `n+n` es cierta para todo entero, y por eso los tres casos dan `true`: la refactorización es siempre segura.

### Java · `java Main.java`

Java expresa el mismo patrón con un matiz importante que Bloch trata en *Effective Java*: la elección del tipo numérico. Aquí `n` es `long`, de 64 bits, lo que da margen frente al desbordamiento en `n * 2`. En una refactorización real esto no es trivial: si `viejo` y `nuevo` desbordaran de formas distintas dejarían de ser equivalentes, y una prueba con valores extremos lo cazaría. La declaración doble `long viejo = n * 2, nuevo = n + n;` mantiene ambas formas lado a lado, invitando a compararlas.

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        long n = Long.parseLong(br.readLine().trim());
        long viejo = n * 2, nuevo = n + n;
        System.out.println("equivalente=" + (viejo == nuevo ? "true" : "false") + " resultado=" + nuevo);
    }
}
```

### SQL · `sqlite3 :memory: < main.sql`

SQL ofrece el paralelo más revelador de la clase, porque la refactorización que preserva el resultado es *el pan de cada día* de un motor de bases de datos: el optimizador reescribe tu consulta en otra equivalente y más rápida sin que el conjunto de filas devuelto cambie. Aquí la equivalencia `n * 2 = n + n` se evalúa dentro de un `CASE` sobre una fila, y el resultado observable se proyecta con `printf`. Date, en *SQL and Relational Theory*, dedica buena parte del libro precisamente a cuándo dos expresiones relacionales son equivalentes —el fundamento teórico de toda optimización—, que es la misma pregunta que se hace un refactorizador: ¿estas dos formas producen lo mismo?

```sql
-- SQL: dos expresiones equivalentes.
WITH nums(n) AS (VALUES (5))
SELECT printf('equivalente=%s resultado=%d', CASE WHEN n * 2 = n + n THEN 'true' ELSE 'false' END, n + n) AS resultado FROM nums;
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
const viejo = n * 2, nuevo = n + n;
console.log(`equivalente=${viejo === nuevo ? "true" : "false"} resultado=${nuevo}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
const viejo = n * 2, nuevo = n + n;
console.log(`equivalente=${viejo === nuevo ? "true" : "false"} resultado=${nuevo}`);
```

### C# · `dotnet run`

```csharp
using System;

long n = long.Parse(Console.In.ReadToEnd().Trim());
long viejo = n * 2, nuevo = n + n;
Console.WriteLine($"equivalente={(viejo == nuevo ? "true" : "false")} resultado={nuevo}");
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
	n, _ := strconv.ParseInt(strings.TrimSpace(line), 10, 64)
	viejo, nuevo := n*2, n+n
	res := "false"
	if viejo == nuevo {
		res = "true"
	}
	fmt.Printf("equivalente=%s resultado=%d\n", res, nuevo)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let (viejo, nuevo) = (n * 2, n + n);
    let eq = if viejo == nuevo { "true" } else { "false" };
    println!("equivalente={eq} resultado={nuevo}");
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    long viejo = n * 2, nuevo = n + n;
    printf("equivalente=%s resultado=%ld\n", viejo == nuevo ? "true" : "false", nuevo);
    return 0;
}
```

### PHP · `php main.php`

```php
<?php
$n = (int) trim(fgets(STDIN));
$viejo = $n * 2;
$nuevo = $n + $n;
echo "equivalente=" . ($viejo === $nuevo ? "true" : "false") . " resultado=$nuevo\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

Refactorizar de verdad se apoya en herramientas, y aquí los ecosistemas divergen: qué framework de pruebas te da la red de seguridad y qué refactorizaciones automatiza el tooling cambia de un lenguaje a otro.

| Lenguaje | Red de pruebas | Refactor asistido por |
|---|---|---|
| Python | pytest / unittest | PyCharm, VS Code + Pylance |
| JavaScript/TS | Jest / Vitest | servicio de lenguaje TS, WebStorm |
| Java | JUnit | IntelliJ IDEA (rename/extract muy maduros) |
| C# | xUnit / NUnit | Visual Studio, Rider |
| Go | `go test` | gopls (`gorename`, extract) |
| Rust | `cargo test` | rust-analyzer |
| C | CTest / a mano | clangd (más limitado) |
| SQL | asserts en scripts | optimizador (reescritura equivalente) |
| PHP | PHPUnit | PhpStorm |

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `==` vs `===` (JS/PHP), tuplas (Rust) o pares (Go) para las dos formas. |
| Semántica | La refactorización preserva el resultado observable; el programa lo verifica. |
| Paradigmática | SQL vive de reescrituras equivalentes: el optimizador refactoriza tu consulta. |

## 🧬 El concepto en la familia

La refactorización respaldada por análisis y pruebas es ubicua. Todos los IDE serios ofrecen refactorizaciones automáticas —renombrar un símbolo en todo el proyecto, extraer una función, cambiar una firma— y lo hacen de forma segura porque comprenden el árbol sintáctico y, en muchos casos, corren las pruebas por ti. Rename es tan cotidiano que casi olvidamos que es un refactor de Fowler; extract function estructura funciones largas en piezas con nombre. Y, como muestra SQL, el mismo principio —transformar la forma preservando el resultado— es el corazón de los compiladores optimizadores y de los motores de consulta.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 150
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Refactorizar sin pruebas** → causa: rompes el comportamiento sin enterarte → solución: asegura la red de pruebas *antes* de tocar la estructura.
- **Cambiar comportamiento "de paso"** → causa: eso no es refactorizar, es modificar, y confunde el diagnóstico si algo falla → solución: separa la refactorización del cambio funcional en commits distintos.
- **Pasos demasiado grandes** → causa: si algo se rompe, no sabes qué lo causó → solución: pasos pequeños, corriendo las pruebas tras cada uno.

## ❓ Preguntas frecuentes

- **¿Refactorizar cambia el comportamiento?** No: por definición lo preserva. Si el comportamiento cambia, es otra actividad (añadir función, corregir bug), no refactorización.
- **¿Cuándo refactorizar?** Continuamente, en pasos pequeños, con las pruebas en verde. Fowler recomienda la "regla del campamento": deja el código un poco mejor de como lo encontraste.
- **¿Y si no hay pruebas?** Entonces el primer paso es escribirlas (pruebas de caracterización que fijen el comportamiento actual); solo después es seguro refactorizar.

## 🔗 Referencias

**Libros de la parte:**

- S. McConnell — *Code Complete* (2ª ed., Microsoft Press).
- A. Hunt y D. Thomas — *The Pragmatic Programmer* (2ª ed., Addison-Wesley).
- M. Fowler — *Refactoring* (2ª ed., Addison-Wesley).
- E. Gamma, R. Helm, R. Johnson y J. Vlissides — *Design Patterns* (Addison-Wesley; «GoF»).
- K. Beck — *Test-Driven Development: By Example* (Addison-Wesley).

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

> [⏮️ Clase 149](../../parte-9-ingenieria-de-software-poliglota/149-diseno-y-arquitectura-comparada/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 151 ⏭️](../../parte-9-ingenieria-de-software-poliglota/151-patrones-de-diseno-comparados-entre-lenguajes/README.md)
