# Clase 173 — Pruebas end-to-end del sistema completo

> Parte **11 — Proyecto integrador políglota** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Ejercitar el sistema **completo**, de la entrada a la salida, como lo haría un usuario real: eso es una
prueba **end-to-end**. Hasta ahora cada clase de esta parte construyó una pieza y confió en que su contrato
se cumpliera. Hoy comprobamos lo único que ninguna prueba de componente puede comprobar: que las piezas,
juntas, producen el resultado que el usuario espera. La operación es deliberadamente mínima —dadas dos
entradas y un valor esperado, decir si el sistema acierta—, porque el fondo de una prueba e2e es siempre
ese: **comparar lo observado con lo prometido**.

La razón de que exista esta categoría de prueba es que los sistemas fallan en las costuras. Cada componente
puede pasar sus pruebas unitarias al 100 % y el sistema seguir roto, porque la API devuelve céntimos y la
web asume euros, o porque el script nocturno escribe una fecha en un formato que la base de datos
interpreta al revés. Sam Newman lo formula sin rodeos en *Building Microservices*: cuanto más se descompone
un sistema, más se desplaza el riesgo desde el interior de las piezas hacia el espacio entre ellas. La
prueba e2e es la única que mira ese espacio entero de una vez — y también, por eso mismo, la más lenta,
la más frágil y la que más caro sale mantener.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Escribir una prueba end-to-end que compare el resultado observado con el esperado.
2. Distinguir prueba unitaria, de integración y e2e por lo que cada una puede y no puede detectar.
3. Justificar la forma de la pirámide de pruebas en términos de coste, velocidad y confianza.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | End-to-end | El sistema completo |
| 2 | Flujo de usuario | De la entrada a la salida |
| 3 | Pirámide de pruebas | Muchas unitarias, pocas e2e |

## 📖 Definiciones y características

Una **prueba end-to-end** verifica el sistema completo desde la perspectiva de quien lo usa: entra por la
misma puerta que el usuario, atraviesa todos los componentes reales —sin sustituir ninguno por un doble— y
comprueba la salida final. Un **flujo** es el recorrido concreto de una acción a través de ese sistema
("registrarse", "hacer un pedido", "cerrar el mes"); es la unidad que una prueba e2e ejercita, y por eso
sus casos se escriben en el lenguaje del negocio y no en el de las funciones. La **pirámide de pruebas** es
la forma que debe tener la suite completa: una base ancha de pruebas unitarias rápidas, una franja media de
integración y una punta estrecha de e2e.

Conviene entender por qué la pirámide tiene esa forma y no otra, porque no es una convención estética. Cada
escalón hacia arriba multiplica dos cosas a la vez: la **confianza** que da un test que pasa y el **coste**
de tenerlo. Una prueba unitaria corre en milisegundos, señala con precisión la función culpable y casi
nunca falla por motivos ajenos; pero no puede detectar un desajuste de contrato entre dos servicios. Una
e2e sí lo detecta, y a cambio tarda minutos, depende de red, datos y relojes, y cuando falla te dice
"algo del sistema está mal" sin decirte qué. Ese último punto es el decisivo: una prueba que falla de
forma intermitente —lo que se llama un test *flaky*— no solo no ayuda, sino que **destruye** la utilidad de
toda la suite, porque el equipo aprende a ignorar los fallos en rojo. Hunt y Thomas insisten en *The
Pragmatic Programmer* en que una prueba vale por la decisión que te permite tomar sin pensarlo dos veces;
una suite en la que nadie confía no permite tomar ninguna.

## 🧩 Situación

Tu equipo despliega y en producción los totales salen mal por un céntimo. Las pruebas unitarias del backend
pasan: la función de cálculo es correcta. Las del frontend pasan: formatea bien lo que recibe. El error
está en el medio —el backend devuelve un decimal en coma flotante y el frontend redondea antes de sumar el
IVA—, y ninguna prueba de componente podía verlo, porque cada una probaba su lado del contrato asumiendo
que el otro se comportaba como esperaba. Una sola prueba e2e que introduzca un pedido real y compare el
total final con el esperado detecta ese fallo en el primer intento. Ese es exactamente el hueco que llena
esta categoría: no comprueba que las piezas sean correctas, comprueba que **encajan**.

## 🧮 Modelo

- **Entrada** (stdin): una línea `a b esperado`
- **Salida** (stdout): `e2e=<pasa|falla>`
- **Regla:** pasa si el sistema (a + b) da el esperado

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3 4 7` | `e2e=pasa` |
| `2 2 5` | `e2e=falla` |
| `10 5 15` | `e2e=pasa` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER a, b, esperado ; SI a+b == esperado: pasa SINO falla
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys

a, b, esperado = map(int, sys.stdin.readline().split())
print(f"e2e={'pasa' if a + b == esperado else 'falla'}")
```

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const [a, b, esperado] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`e2e=${a + b === esperado ? "pasa" : "falla"}`);
```

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const [a, b, esperado] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`e2e=${a + b === esperado ? "pasa" : "falla"}`);
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
        int a = Integer.parseInt(p[0]), b = Integer.parseInt(p[1]), e = Integer.parseInt(p[2]);
        System.out.println("e2e=" + (a + b == e ? "pasa" : "falla"));
    }
}
```

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;

int[] p = Array.ConvertAll(Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries), int.Parse);
Console.WriteLine($"e2e={(p[0] + p[1] == p[2] ? "pasa" : "falla")}");
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
	e, _ := strconv.Atoi(f[2])
	res := "falla"
	if a+b == e {
		res = "pasa"
	}
	fmt.Printf("e2e=%s\n", res)
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
    println!("e2e={res}");
}
```

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long a, b, e;
    if (scanf("%ld %ld %ld", &a, &b, &e) != 3) return 1;
    printf("e2e=%s\n", a + b == e ? "pasa" : "falla");
    return 0;
}
```

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL prueba con una consulta de comprobacion.
WITH t(a, b, esperado) AS (VALUES (3, 4, 7))
SELECT printf('e2e=%s', CASE WHEN a + b = esperado THEN 'pasa' ELSE 'falla' END) AS resultado FROM t;
```

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
[$a, $b, $e] = array_map('intval', preg_split('/\s+/', trim(fgets(STDIN))));
echo "e2e=" . ($a + $b === $e ? "pasa" : "falla") . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🧪 Recorrido del código

El contrato ([`casos.json`](casos.json)) recibe `a b esperado` y responde `e2e=pasa` o `e2e=falla`: el
sistema bajo prueba es la suma `a + b`, y el tercer número es la promesa contra la que se contrasta. Esa
estructura —**ejecutar, observar, comparar con lo esperado**— es la de cualquier aserción, desde un
`assert` de una línea hasta una suite de Playwright que pilota un navegador. Fíjate en que el caso
`2 2 5` produce `e2e=falla` y aun así el programa termina con éxito: distinguir "el test falló" de "el
ejecutor de tests se rompió" es una de las diferencias que un arnés de pruebas real debe respetar.

Los diez lenguajes convergen en la misma línea de decisión, pero la escriben con formas que revelan su
familia. **Python**, **JavaScript**, **TypeScript**, **Java**, **C#**, **Rust** y **PHP** usan una
expresión condicional que *devuelve un valor*:

```python
print(f"e2e={'pasa' if a + b == esperado else 'falla'}")
```

La comparación y la elección del texto ocurren dentro de la misma expresión. **Go** no tiene operador
ternario —una omisión deliberada de sus diseñadores, que Donovan y Kernighan explican como preferencia por
un único camino legible— y obliga a una sentencia con una variable previa:

```go
res := "falla"
if a+b == e {
    res = "pasa"
}
```

Inicializar en `"falla"` y ascender a `"pasa"` solo si la condición se cumple es, además, el orden correcto
para un test: el veredicto por defecto es el negativo, y el éxito hay que ganárselo. **C** aprovecha su
ternario para pasarlo directamente a `printf`, y **SQL** usa `CASE WHEN … THEN … ELSE … END`, que es la
misma idea en forma de expresión declarativa aplicada a una tabla de casos: exactamente como se escriben
las pruebas basadas en datos, donde los casos son filas y no líneas de código.

## 🔬 Comparación

Comparar un resultado con un valor esperado es trivial; lo interesante es qué forma le da cada familia a
esa decisión y qué dice esa forma sobre el lenguaje.

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Ternario `?:` (JS/TS/Java/C#/C/PHP), expresión condicional (Python), `if` como expresión (Rust), `if` como sentencia (Go), `CASE WHEN` (SQL). |
| Semántica | En Python, JS y PHP la comparación puede convertir tipos si no se cuida (`===` frente a `==`); en Java, C#, Go y Rust el compilador impide comparar tipos incompatibles antes de ejecutar nada. |
| Paradigmática | Los imperativos ejecutan el flujo y luego comprueban; SQL expresa la comprobación **sobre un conjunto de casos** — una fila por caso de prueba, que es el modelo de las pruebas parametrizadas. |

Hay una lección de fondo que este ejercicio hace visible sin decirlo: la prueba está escrita en el mismo
lenguaje que el componente. En un sistema políglota real eso deja de ser posible, porque ningún lenguaje
puede probar el flujo completo desde dentro. Por eso las pruebas e2e viven **fuera** de los componentes —en
un script, un contenedor o una herramienta dedicada— y hablan con el sistema por sus fronteras públicas:
HTTP, stdin/stdout, la interfaz gráfica. El verificador de este propio programa, que corre las diez
implementaciones contra `casos.json` y compara salidas, es precisamente eso: un arnés e2e políglota.

## 🧬 El concepto en la familia

Toda familia de lenguajes tiene su capa de pruebas —`pytest` y `unittest` en Python, JUnit en la JVM, xUnit
y NUnit en .NET, `go test` integrado en el propio toolchain de Go, `cargo test` en Rust, Jest y Vitest en
JavaScript, PHPUnit en PHP— y todas implementan la misma tríada: preparar, ejecutar, afirmar. Para el
escalón e2e el reparto es distinto, porque la herramienta ya no depende del lenguaje del componente sino
del **canal** por el que se entra al sistema: Playwright, Cypress y Selenium pilotan un navegador real;
`curl`, Postman o k6 golpean una API por HTTP; un simple script de shell ejercita una CLI. Reconocer que
todas son la misma idea aplicada a puertas distintas es lo que te permite montar una suite e2e en un
sistema cuyos lenguajes no dominas todavía.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 173
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Suite invertida: casi todo e2e** → causa: parece que cubren más, así que se escriben primero → solución: seguir la pirámide; cada fallo detectado por una e2e debería convertirse además en una prueba unitaria que lo señale con precisión la próxima vez.
- **e2e sin datos controlados** → causa: la prueba depende del estado que dejó la ejecución anterior o de la fecha del día, y falla los lunes → solución: fijar los datos de partida, reiniciar el estado entre ejecuciones y controlar el reloj y las fuentes de aleatoriedad.
- **Tolerar tests intermitentes** → causa: un fallo esporádico se relanza en vez de investigarse, y el equipo aprende a ignorar el rojo → solución: tratar cada *flaky* como un bug de prioridad alta; casi siempre esconde una condición de carrera real del sistema, no de la prueba.
- **Esperas fijas en vez de esperas por condición** → causa: `sleep 2` funciona en tu portátil y falla en CI, que va más lento → solución: esperar a que ocurra el suceso (el elemento aparece, la respuesta llega) con un límite de tiempo, nunca una duración a ojo.

## ❓ Preguntas frecuentes

- **¿e2e o unitaria?** No son alternativas, responden preguntas distintas. La unitaria pregunta "¿esta función es correcta?" y te lo dice en milisegundos señalando la línea; la e2e pregunta "¿el sistema entero cumple lo que promete al usuario?" y no puede responderlo ninguna otra. Necesitas muchas de las primeras y unas pocas de las segundas, bien elegidas.
- **¿Por qué son costosas?** Porque arrastran todo: arrancar servicios, esperar red y disco, preparar y limpiar datos. Y porque su coste no es solo el tiempo de ejecución sino el de mantenimiento: cualquier cambio en cualquier componente puede romperlas, y su diagnóstico es lento porque el fallo no señala culpable.
- **¿Cuántas e2e hacen falta?** Las que cubran los flujos que, si se rompen, harían inaceptable el despliegue: normalmente el registro, el flujo de compra, el inicio de sesión. Nygard lo enmarca en *Release It!* como una decisión de riesgo, no de cobertura: pruebas el camino cuyo fallo te costaría dinero o reputación, no todos los caminos posibles.

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

> [⏮️ Clase 172](../../parte-11-proyecto-integrador-poliglota/172-persistencia-y-almacenamiento/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 174 ⏭️](../../parte-11-proyecto-integrador-poliglota/174-empaquetado-contenedores-y-despliegue/README.md)
