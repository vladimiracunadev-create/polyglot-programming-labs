# Clase 139 — Pruebas unitarias por lenguaje

> Parte **9 — Ingeniería de software políglota** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Una **prueba unitaria** es código que ejerce otro código y afirma —mediante una aserción— que el resultado observado coincide con el esperado. Suena modesto, pero es la pieza que sostiene todo lo demás: sin una red de pruebas que se ejecuta en segundos, cada cambio es una apuesta y el miedo a tocar el código se convierte en deuda. Kent Beck, en *Test-Driven Development: By Example*, invierte el orden habitual: primero se escribe la prueba que falla (rojo), después el código mínimo que la hace pasar (verde) y por último se refactoriza con la prueba como red de seguridad. Ese ciclo *red-green-refactor* no es una ceremonia; es una forma de dejar que el diseño emerja de ejemplos concretos en lugar de especulación.

El problema de juguete de esta clase —comprobar que `a + b == esperado`— es deliberadamente trivial para que el foco esté en el *mecanismo* de la aserción, no en la lógica bajo prueba. Steve McConnell, en *Code Complete*, insiste en que la calidad no se "añade" al final: se construye con prácticas que hacen visible cada defecto lo antes posible, y la prueba automática es la más barata de todas. Aquí verás que el mismo acto —afirmar una igualdad y declararla `pasa` o `falla`— existe en los diez lenguajes del núcleo, cada uno con su *runner*: pytest, JUnit, Jest/vitest, cargo test, go test, dotnet test o PHPUnit. Comprender ese denominador común te permite moverte entre ecosistemas sin reaprender la idea, solo la herramienta.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. **Escribir** una aserción que compare un valor observado con el esperado y decida el veredicto.
2. **Distinguir** con precisión una prueba que pasa (verde) de una que falla (rojo) y explicar qué comunica cada estado.
3. **Identificar** el *runner* y la convención de aserción de cada lenguaje del núcleo (pytest, JUnit, cargo test…).
4. **Justificar** por qué una unidad se prueba de forma aislada, repetible y sin depender del orden de ejecución.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Prueba unitaria | Es el bloque mínimo de la red de seguridad; corre en milisegundos y aísla el fallo |
| 2 | Aserción | Convierte una expectativa implícita en una comprobación explícita y automatizable |
| 3 | Pasa/falla (verde/rojo) | El veredicto binario guía el ciclo TDD y el semáforo de la CI |
| 4 | Runner por lenguaje | Cada ecosistema descubre y ejecuta las pruebas con su propia herramienta |

## 📖 Definiciones y características

- **Prueba unitaria.** Código que ejerce una unidad de comportamiento —normalmente una función— de forma aislada y automática, y afirma un resultado. Beck subraya tres propiedades que la hacen valiosa: es *repetible* (mismo resultado en cada ejecución), *rápida* (para poder correrla constantemente) y *autónoma* (no depende de otras pruebas ni de un orden concreto). Una prueba lenta o frágil se ignora, y una prueba ignorada no protege nada.
- **Aserción.** El corazón de la prueba: una comprobación que declara "esto debe cumplirse". Si se cumple, la prueba sigue; si no, la marca en rojo y detiene el flujo. Nuestra línea `test={'pasa' if a + b == esperado else 'falla'}` es una aserción desnuda, sin *framework*: expone la mecánica que herramientas como `assert` (Python), `assertEquals` (JUnit) o `expect().toBe()` (Jest) envuelven con mejores mensajes de error.
- **Runner.** La herramienta que descubre las pruebas, las ejecuta y reporta el resultado agregado. Un solo comando —`pytest`, `cargo test`, `go test ./...`— recorre todo el conjunto. Su valor está en el *reporte*: qué falló, con qué valor esperado frente al obtenido, y en qué línea.

## 🧩 Situación

Trabajas en una biblioteca de facturación y alguien "optimiza" la función de sumatoria de un pedido. Compila, se despliega, y tres días después contabilidad reporta totales de un céntimo de menos por redondeo. Con una sola prueba unitaria —`sumar(3, 4)` debe dar `7`, y un caso límite con decimales— ese error se habría iluminado en rojo en el instante del cambio, antes de salir del portátil. Esa es la promesa de McConnell: mover el descubrimiento del defecto lo más cerca posible de su introducción, donde arreglarlo cuesta minutos y no incidentes.

## 🧮 Modelo

- **Entrada** (stdin): una línea `a b esperado`
- **Salida** (stdout): `test=<pasa|falla>`
- **Regla:** pasa si a + b == esperado

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3 4 7` | `test=pasa` |
| `2 2 5` | `test=falla` |
| `10 5 15` | `test=pasa` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER a, b, esperado ; SI a+b == esperado: pasa SINO falla
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/). Cada programa es a la vez el *sujeto* y la *aserción*: lee `a b esperado`, calcula la suma y emite el veredicto. En un proyecto real separarías la función bajo prueba del código que la prueba, pero aquí los fundimos para que veas la comparación esencial sin el andamiaje del *framework*.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys

a, b, esperado = map(int, sys.stdin.readline().split())
print(f"test={'pasa' if a + b == esperado else 'falla'}")
```

Léelo despacio, porque condensa toda la clase en dos líneas. `sys.stdin.readline().split()` parte la línea `3 4 7` en tres cadenas; `map(int, …)` las convierte a enteros y el desempaquetado los ata a `a`, `b` y `esperado`. La segunda línea es la aserción: la expresión condicional `'pasa' if a + b == esperado else 'falla'` evalúa exactamente el mismo predicado que escribirías dentro de un `assert a + b == esperado` de pytest. La diferencia es que pytest, al fallar, te mostraría el valor real y el esperado con su *introspección de aserciones*; aquí lo reducimos a la palabra `pasa` o `falla` para que el verificador del curso pueda compararla carácter a carácter. Con la entrada `2 2 5` la suma da `4`, no `5`, y la salida es `test=falla`: una prueba en rojo, tal como Beck quiere verla antes de escribir el arreglo.

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const [a, b, esperado] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`test=${a + b === esperado ? "pasa" : "falla"}`);
```

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const [a, b, esperado] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`test=${a + b === esperado ? "pasa" : "falla"}`);
```

### Java · [`java/Main.java`](implementaciones/java/Main.java) · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        int a = Integer.parseInt(p[0]), b = Integer.parseInt(p[1]), esperado = Integer.parseInt(p[2]);
        System.out.println("test=" + (a + b == esperado ? "pasa" : "falla"));
    }
}
```

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;

int[] p = Array.ConvertAll(Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries), int.Parse);
Console.WriteLine($"test={(p[0] + p[1] == p[2] ? "pasa" : "falla")}");
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
	a, _ := strconv.Atoi(f[0])
	b, _ := strconv.Atoi(f[1])
	esperado, _ := strconv.Atoi(f[2])
	res := "falla"
	if a+b == esperado {
		res = "pasa"
	}
	fmt.Printf("test=%s\n", res)
}
```

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let v: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    let res = if v[0] + v[1] == v[2] { "pasa" } else { "falla" };
    println!("test={res}");
}
```

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long a, b, esperado;
    if (scanf("%ld %ld %ld", &a, &b, &esperado) != 3) return 1;
    printf("test=%s\n", a + b == esperado ? "pasa" : "falla");
    return 0;
}
```

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL: una consulta de comprobación.
WITH t(a, b, esperado) AS (VALUES (3, 4, 7))
SELECT printf('test=%s', CASE WHEN a + b = esperado THEN 'pasa' ELSE 'falla' END) AS resultado FROM t;
```

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
[$a, $b, $esperado] = array_map('intval', preg_split('/\s+/', trim(fgets(STDIN))));
echo "test=" . ($a + $b === $esperado ? "pasa" : "falla") . "\n";
```

Compara ahora tres contrastes reveladores. En **Rust**, `v[0] + v[1] == v[2]` opera sobre `i64` con desbordamiento comprobado en modo *debug*: si la suma se saliera del rango, el programa entraría en pánico en lugar de dar un resultado silenciosamente erróneo —una forma de aserción que el propio lenguaje impone, en la línea de lo que Klabnik y Nichols describen sobre la seguridad de Rust. En **C**, `scanf("%ld %ld %ld", …)` puede fallar si la entrada no trae tres números, y por eso el `if (… != 3) return 1;` es su propia mini-aserción de contrato: sin frameworks, la disciplina de comprobar el valor de retorno es lo que separa un programa robusto de uno que corrompe memoria, tal como enseñan Kernighan y Ritchie. En **SQL**, en cambio, no hay `stdin` ni bucle: la comprobación es una `CASE WHEN a + b = esperado` sobre una tabla de casos, la forma declarativa de expresar la misma verdad. El veredicto textual —`test=pasa`— es idéntico en los tres; lo que cambia es cómo cada lenguaje llega a él.

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

La sintaxis de la aserción es lo de menos; lo que de verdad distingue a cada ecosistema es su *runner*, cómo descubre las pruebas y cómo las ejecuta.

| Lenguaje | Runner habitual | Cómo se invoca | Aserción idiomática |
|---|---|---|---|
| Python | pytest / unittest | `pytest` | `assert a + b == esperado` |
| JavaScript | Jest / vitest | `npx jest` · `npx vitest` | `expect(x).toBe(y)` |
| TypeScript | vitest / Jest | `npx vitest` | `expect(x).toBe(y)` |
| Java | JUnit 5 | `mvn test` · `gradle test` | `assertEquals(y, x)` |
| C# | xUnit / NUnit | `dotnet test` | `Assert.Equal(y, x)` |
| Go | testing (estándar) | `go test ./...` | `if got != want { t.Errorf(...) }` |
| Rust | test (integrado) | `cargo test` | `assert_eq!(x, y)` |
| C | Unity / Criterion | según *build* | `TEST_ASSERT_EQUAL(y, x)` |
| SQL | pgTAP / assert manual | según motor | `CASE WHEN … THEN 'ok'` |
| PHP | PHPUnit | `./vendor/bin/phpunit` | `$this->assertSame(y, x)` |

Nota los dos extremos culturales. Go y Rust traen el *runner* dentro del propio lenguaje: no instalas nada, `go test` y `cargo test` descubren las funciones de prueba por convención (`func TestXxx` y `#[test]`) y las corren. En el otro lado, Java, C# o PHP delegan en herramientas externas (JUnit, xUnit, PHPUnit) que se integran con el gestor de dependencias. Esa decisión de diseño —¿pruebas de primera clase en el lenguaje o biblioteca aparte?— condiciona cuánta fricción hay para empezar a probar, y explica por qué en Go probar es el camino de menor resistencia.

## 🧬 El concepto en la familia

pytest, JUnit, xUnit, cargo test, `go test` o PHPUnit son dialectos de la misma idea que formalizó la familia *xUnit* de Kent Beck: un *test case* que prepara (arrange), ejerce (act) y afirma (assert). Cambia el nombre del método de aserción y la forma de descubrir las pruebas, pero el ciclo rojo-verde-refactor es idéntico en todas partes; por eso quien lo interioriza en un lenguaje lo transporta a los demás casi sin coste.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 139
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **No probar los casos límite.** El happy path pasa siempre; los defectos viven en los extremos. Incluye el cero, el conjunto vacío, los negativos y el desbordamiento. Beck sugiere escribir primero la prueba del caso que te preocupa.
- **Pruebas frágiles.** Si una prueba falla cuando renombras una variable interna o reordenas el código sin cambiar el comportamiento, está acoplada a la implementación. Prueba el *qué* observable (la salida), no el *cómo* interno.
- **Aserciones sin mensaje.** `assert x` sin contexto te dice que algo falló, no qué. Los buenos frameworks muestran esperado-vs-obtenido; aprovéchalo y evita la aserción muda.
- **Pruebas que dependen entre sí.** Si la prueba B necesita que A haya corrido antes, el conjunto es un castillo de naipes. Cada prueba debe montar y desmontar su propio estado.

## ❓ Preguntas frecuentes

- **¿Cuántas pruebas escribo?** Al menos una por comportamiento distinto y una por cada caso límite que te quite el sueño. La métrica no es el número, sino la confianza para cambiar el código sin miedo.
- **¿`casos.json` es una prueba?** Sí, es una prueba de caja negra: fija una entrada y la salida esperada, y el verificador compara la real con la esperada. Es equivalente a una tabla de casos parametrizados de pytest o JUnit.
- **¿TDD obliga a escribir la prueba antes?** El método de Beck sí (rojo primero), y esa disciplina mejora el diseño porque te obliga a pensar en la interfaz antes que en la implementación. Pero incluso probar después es infinitamente mejor que no probar.

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

> [⏮️ Clase 138](../../parte-8-como-funcionan-los-lenguajes/138-depuracion-como-se-diagnostica-en-cada-runtime/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 140 ⏭️](../../parte-9-ingenieria-de-software-poliglota/140-pruebas-de-integracion-y-el-verificador-de-equivalencia/README.md)
