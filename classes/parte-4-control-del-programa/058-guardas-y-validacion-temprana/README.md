# Clase 058 — Guardas y validación temprana

> Parte **4 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Una función que primero se ocupa de todo lo que puede salir mal —entradas inválidas, casos límite, situaciones especiales— y sale de inmediato ante cada uno, deja el resto del cuerpo para una sola cosa: el trabajo real. Eso es una **guarda** (*guard clause*), y la técnica de anteponerlas se llama validación temprana. El problema que resuelve es concreto y viejo: sin guardas, cada comprobación envuelve al resto del código en un `else`, y tres o cuatro validaciones producen una escalera de anidamiento que se desplaza hacia la derecha hasta volverse ilegible. La guarda invierte esa forma: en lugar de anidar el camino feliz cada vez más adentro, lo saca a la superficie y descarta los desvíos uno a uno.

El concepto entronca directamente con la programación estructurada. Los **comandos guardados** (*guarded commands*) que Dijkstra formaliza en *Structured Programming* proponen justamente pensar el flujo como una lista de condiciones vigiladas, cada una con su acción; la guard clause moderna es la versión pragmática de esa idea. La intuición que se gana es que la validación no es ruido que estorba al algoritmo, sino su primera fase: establecer las precondiciones bajo las cuales el resto del código tiene derecho a suponer que sus datos son buenos. Un cuerpo de función que empieza con guardas se lee después "de corrido", sin tener que sostener mentalmente en qué rama anidada estamos.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Escribir guardas que validan y salen temprano.
2. Evitar el anidamiento profundo de if.
3. Ordenar las comprobaciones de más restrictiva a menos.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Validación temprana | Comprobar lo inválido primero |
| 2 | Guarda | Un if que corta el flujo pronto |
| 3 | Retorno temprano | Salir en cuanto se decide |
| 4 | Legibilidad | Menos anidamiento, más claridad |

## 📖 Definiciones y características

- **Guarda** — condición al inicio que corta el flujo si no se cumple. Clave: evita anidar.
- **Validación temprana** — rechazar entradas inválidas antes del cálculo. Clave: el camino feliz queda limpio.
- **Retorno temprano** — salir de la función en cuanto hay respuesta. Clave: menos ramas abiertas.
- **Camino feliz** — el flujo principal sin errores. Clave: se lee de corrido tras las guardas.

Estas cuatro nociones describen una misma disciplina desde ángulos distintos. La guarda es la construcción; la validación temprana es la estrategia de ponerlas al principio; el retorno temprano es el mecanismo con que cada guarda corta el flujo; y el camino feliz es el resultado: el trozo de código, ya al final, que solo se ejecuta cuando todo lo anterior pasó. La conexión con la teoría es directa. Los *guarded commands* de Dijkstra en *Structured Programming* modelan una decisión como un conjunto de guardas —condiciones booleanas— asociadas a acciones, y esa misma idea, llevada a la práctica, dice: comprueba las condiciones que invalidan el resto y despáchalas antes de continuar. Sebesta, al tratar la selección múltiple en *Concepts of Programming Languages*, observa que un `if/else` profundamente anidado y una secuencia de retornos tempranos son *equivalentes en control de flujo* pero no en carga cognitiva: el segundo mantiene baja la "profundidad" del código, que es una medida real de cuánto contexto debe sostener el lector. Aplanar el anidamiento no cambia lo que el programa hace; cambia lo que un humano puede verificar de un vistazo. Por eso en Go y Rust el early return al inicio de la función no es un truco, sino el estilo idiomático recomendado: se valida, se retorna, y el camino feliz queda al ras del margen izquierdo.

## 🧩 Situación

Piensa en la función que procesa el pago de un pedido: necesita un usuario autenticado, un carrito no vacío, un método de pago válido y stock disponible. Escrita sin guardas, cada requisito abre un `if` cuyo `else` envuelve todo lo siguiente, y el cobro real termina cuatro o cinco niveles de indentación adentro, rodeado de llaves que hay que emparejar mentalmente para saber a qué error corresponde cada rama. Un lector que llega a arreglar un bug en el cálculo del total debe primero descifrar bajo qué combinación de condiciones se ejecuta esa línea. Con guardas —`if (!usuario.autenticado) return Error.NO_AUTH;`, `if (carrito.vacio) return Error.CARRITO_VACIO;`, y así— cada fallo se despacha y se olvida, y el cobro queda al final, sin anidar, legible como una frase.

La diferencia no es solo estética: es de corrección. Cuando la validación está dispersa en `else` anidados, es fácil que una rama olvide cubrir un caso o que un cambio posterior mueva código dentro de la rama equivocada, y el sistema procese un pedido inválido. La validación temprana concentra todas las precondiciones en un bloque visible al inicio, donde saltan a la vista los huecos. Es la diferencia entre "creo que validamos el stock en algún sitio" y "las cuatro guardas están aquí, en orden, al principio".

## 🧮 Modelo

- **Entrada** (stdin): un entero `edad`
- **Salida** (stdout): `invalido` si edad<0, `menor` si edad<18, `adulto` en otro caso
- **Regla:** guardas: edad<0 → invalido; edad<18 → menor; si no → adulto

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `-5` | `invalido` |
| `10` | `menor` |
| `20` | `adulto` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER edad
SI edad < 0: ESCRIBIR "invalido" ; FIN
SI edad < 18: ESCRIBIR "menor" ; FIN
ESCRIBIR "adulto"
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

edad = int(sys.stdin.readline())
if edad < 0:
    print("invalido")
elif edad < 18:
    print("menor")
else:
    print("adulto")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const edad = parseInt(readFileSync(0, "utf8").trim(), 10);
if (edad < 0) console.log("invalido");
else if (edad < 18) console.log("menor");
else console.log("adulto");
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const edad: number = parseInt(readFileSync(0, "utf8").trim(), 10);
if (edad < 0) console.log("invalido");
else if (edad < 18) console.log("menor");
else console.log("adulto");
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int edad = Integer.parseInt(br.readLine().trim());
        if (edad < 0) {
            System.out.println("invalido");
        } else if (edad < 18) {
            System.out.println("menor");
        } else {
            System.out.println("adulto");
        }
    }
}
```

### C# · `dotnet run`

```csharp
using System;

int edad = int.Parse(Console.In.ReadToEnd().Trim());
if (edad < 0)
    Console.WriteLine("invalido");
else if (edad < 18)
    Console.WriteLine("menor");
else
    Console.WriteLine("adulto");
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
	edad, _ := strconv.Atoi(strings.TrimSpace(line))
	if edad < 0 {
		fmt.Println("invalido")
		return
	}
	if edad < 18 {
		fmt.Println("menor")
		return
	}
	fmt.Println("adulto")
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let edad: i64 = s.trim().parse().unwrap();
    if edad < 0 {
        println!("invalido");
    } else if edad < 18 {
        println!("menor");
    } else {
        println!("adulto");
    }
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long edad;
    if (scanf("%ld", &edad) != 1) return 1;
    if (edad < 0) {
        printf("invalido\n");
    } else if (edad < 18) {
        printf("menor\n");
    } else {
        printf("adulto\n");
    }
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: clasificación con CASE WHEN en orden.
WITH edades(edad) AS (VALUES (-5), (10), (20))
SELECT CASE WHEN edad < 0 THEN 'invalido'
            WHEN edad < 18 THEN 'menor'
            ELSE 'adulto' END AS resultado
FROM edades;
```

### PHP · `php main.php`

```php
<?php
$edad = (int) trim(fgets(STDIN));
if ($edad < 0) {
    echo "invalido\n";
} elseif ($edad < 18) {
    echo "menor\n";
} else {
    echo "adulto\n";
}
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔎 Recorrido del código: de la entrada a la salida

Comparar **Python** y **Go** en esta clase es especialmente instructivo, porque expresan la misma lógica con dos formas distintas de la misma idea. Sigamos `edad = 10`. En Python, tras `int(sys.stdin.readline())` se evalúa `if edad < 0`: `10 < 0` es falso, se salta; luego `elif edad < 18`: `10 < 18` es verdadero, imprime `"menor"` y el `if/elif/else` termina sin tocar la rama `else`. Con `edad = -5`, la primera guarda `edad < 0` se cumple y produce `"invalido"` de inmediato; con `edad = 20`, ambas comprobaciones fallan y cae al `else` → `"adulto"`. Las tres salidas coinciden con `casos.json`. Aquí Python usa un `if/elif/else` clásico: una sola sentencia de selección múltiple con salida por `print`.

Go escribe exactamente la misma clasificación, pero como **guardas con retorno temprano**: `if edad < 0 { fmt.Println("invalido"); return }`, luego `if edad < 18 { fmt.Println("menor"); return }`, y finalmente `fmt.Println("adulto")` sin `else`. Con `edad = 10`, la primera guarda no se cumple, la segunda sí: imprime `"menor"` y el `return` corta la función antes de llegar al `adulto` del final. Esta es la forma canónica de la guard clause: cada condición especial se despacha y se sale, de modo que la línea del camino feliz (`"adulto"`) vive al margen izquierdo, sin anidar. Nota que el resultado es idéntico al de Python precisamente porque un `if/elif/else` y una secuencia de guardas con `return` son *equivalentes en control de flujo*; lo que cambia es la forma. Go además **obliga** las llaves `{ }` incluso en un cuerpo de una línea, lo que hace visualmente inconfundible dónde empieza y termina cada guarda. Un tercer contraste es **SQL**, que no tiene retorno ni función: colapsa las tres guardas en un único `CASE WHEN edad < 0 ... WHEN edad < 18 ... ELSE 'adulto' END`, evaluado en orden sobre cada fila. El orden de los `WHEN` reproduce el orden de las guardas: si intercambiaras las dos primeras condiciones, un `-5` se clasificaría mal en los tres lenguajes por igual.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `if ...: return` (Python) vs. `if (...) { return; }` (C/Java). |
| Semántica | El orden de las guardas define la clasificación; cambiarlo cambia el resultado. |
| Paradigmática | SQL encadena condiciones con CASE WHEN en orden. |

Bajo la superficie, los diez lenguajes divergen en cuánto favorecen el estilo de guarda. Go lo eleva casi a norma cultural: su ausencia deliberada de excepciones para el flujo ordinario hace que el `if err != nil { return err }` sea el patrón dominante de todo el lenguaje, y el compilador **obliga** las llaves, eliminando el problema del `else` colgante. Rust empuja en la misma dirección pero con más herramientas: además del early return, ofrece `?` para propagar errores y `let ... else { return }` para validar-y-desestructurar en un gesto. Python, JavaScript y PHP permiten el `return` temprano sin ceremonia, aunque su tradición mezcla ambos estilos. Java y C# admiten guardas, pero cargan con el debate histórico del "único punto de salida" heredado de la era estructurada estricta, hoy mayormente abandonado. C las usa con `return` directo, sin excepciones que compliquen el flujo. SQL, declarativo, no tiene "salida temprana" en absoluto: su equivalente es el orden de los `WHEN` en un `CASE`, evaluado perezosamente de arriba abajo pero sin abandonar nunca la evaluación de la fila.

## 🧬 El concepto en la familia

En la familia de scripting dinámico, Ruby ofrece el elegante modificador postfijo `return 'invalido' if edad < 0`, que lee casi como inglés y hace la guarda aún más compacta. En la familia de sistemas, Go y Rust han convertido el early return en el estilo por defecto para el manejo de errores, hasta el punto de que su ausencia de excepciones para el flujo normal *fuerza* el patrón de guarda. En la familia funcional, la idea toma otra forma: en vez de "salir temprano" —que presupone sentencias y efectos—, Haskell o los `match`/`case` con patrones expresan lo mismo despachando primero los casos base de una función definida por ecuaciones, y las *guard clauses* de Haskell (`| edad < 0 = "invalido"`) son literalmente eso, guardas, heredando el término de Dijkstra. La disciplina es universal; solo cambia si la encarnas con `return` imperativo o con ramas de una expresión.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 058
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Anidar en vez de usar guardas** → causa: envolver cada validación en un `else`, produciendo una escalera que se hunde hacia la derecha → solución: sacar los casos especiales como guardas con retorno temprano al inicio, dejando el camino feliz al margen.
- **Ordenar mal las guardas** → causa: comprobar una condición general antes que una más específica, de modo que un valor cae en la rama equivocada (p. ej. probar `edad < 18` antes que `edad < 0`, clasificando un `-5` como `menor`) → solución: ir de la condición más restrictiva o excluyente a la más general.
- **Olvidar el `return` en la guarda** → causa: escribir la condición pero no cortar el flujo, de modo que la ejecución sigue y también entra al camino feliz → solución: asegurar que cada guarda termina en `return` (o `break`/`continue`/`throw`) y no solo imprime.
- **Meter lógica en las guardas** → causa: mezclar cálculo real dentro de las cláusulas de validación, difuminando la frontera entre "validar" y "hacer" → solución: mantener las guardas como comprobaciones baratas y de salida rápida; el trabajo va después, en el camino feliz.

## ❓ Preguntas frecuentes

- **¿Guarda o if/else anidado?** La guarda suele ser más legible: aplana el código, elimina la indentación creciente y deja el camino feliz claro al final. El anidado solo gana cuando las condiciones no son independientes y realmente representan sub-decisiones.
- **¿Varios `return` no violan la regla del "único punto de salida"?** Esa regla era una convención de la era estructurada estricta, útil cuando había que liberar recursos manualmente. Con guardas y gestión automática de recursos, múltiples returns tempranos hacen el flujo *más* claro, no menos.
- **¿Dónde ubico las guardas?** Al principio de la función, antes de cualquier cálculo, ordenadas de la validación más barata o más excluyente a la más costosa. Así el código nunca hace trabajo que luego una guarda descartaría.
- **¿Esto sirve también en bucles?** Sí: el equivalente de la guarda dentro de un bucle es `continue` para saltar iteraciones inválidas temprano, aplanando el cuerpo del bucle igual que el `return` aplana la función.

## 🔗 Referencias

Para esta clase, ve en *Structured Programming* al material de Dijkstra sobre *guarded commands* y la disciplina de la selección; en Sebesta, apóyate en el tratamiento de sentencias de selección y en su discusión sobre profundidad de anidamiento y legibilidad dentro del capítulo de control de flujo.

**Libros de la parte:**

- O.-J. Dahl, E. W. Dijkstra y C. A. R. Hoare — *Structured Programming* (Academic Press).
- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson), cap. control de flujo.

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

> [⏮️ Clase 057](../../parte-4-control-del-programa/057-booleanos-condiciones-y-cortocircuito/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 059 ⏭️](../../parte-4-control-del-programa/059-if-else-y-anidamiento/README.md)
