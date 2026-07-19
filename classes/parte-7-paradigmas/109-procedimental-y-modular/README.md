# Clase 109 — Procedimental y modular

> Parte **7 — Paradigmas** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

El **paradigma procedimental** es el imperativo que ha crecido y necesita orden. Cuando un programa deja de caber en la cabeza, la respuesta clásica es darle nombre a las partes: agrupar una secuencia de pasos bajo una etiqueta —un *procedimiento*— y a partir de ahí invocarla en lugar de repetirla. SICP construye toda su primera sección alrededor de esta idea con el nombre de *abstracción procedimental*: un procedimiento como `promedio` se convierte en una "caja negra" que el resto del código usa por su nombre y su contrato (dame una lista, te devuelvo su promedio) sin preocuparse de cómo lo calcula por dentro. Ese ocultamiento del *cómo* detrás de un *qué* es lo que permite construir programas grandes a partir de piezas comprensibles.

La palabra **modular** añade la dimensión de la organización a gran escala. David Parnas, en su artículo seminal de 1972 sobre criterios de descomposición en módulos, mostró que dividir un sistema no es solo cuestión de trocearlo en funciones, sino de decidir *qué información oculta cada módulo* del resto. Un buen módulo expone una interfaz estable y esconde sus decisiones internas, de modo que puedas cambiar la implementación sin tocar a quien lo usa. El procedimiento `promedio` de esta clase es el germen de esa idea: quien lo llama solo ve `promedio(nums)`, y si mañana cambiaras la fórmula interna, el `main` no se enteraría.

En esta clase practicarás el gesto fundacional del estilo: extraer un cálculo repetible —el promedio de una lista— a un procedimiento con nombre, y llamarlo desde el programa principal. Sebesta dedica su capítulo 9 a los subprogramas (parámetros, paso de argumentos, valores de retorno, ámbito), que es la maquinaria que hace posible esta abstracción en cada lenguaje del núcleo. El objetivo es que veas el imperativo, ya no como un `main` monolítico, sino como una conversación entre procedimientos.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Encapsular un cálculo en un procedimiento.
2. Llamarlo desde el programa principal.
3. Reconocer la modularidad procedimental.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Procedimiento | Bloque con nombre reutilizable |
| 2 | Modularidad | Dividir en unidades |
| 3 | Reutilización | Llamar en vez de repetir |

## 📖 Definiciones y características

- **Procedimental** — paradigma que organiza el código en procedimientos/funciones. Clave: imperativo modular.
- **Procedimiento** — unidad con nombre que realiza una tarea. Clave: se invoca cuando se necesita.
- **Modularidad** — dividir el problema en piezas manejables. Clave: cada una con una responsabilidad.

Lo que distingue al procedimental del imperativo desnudo de la clase anterior es la *abstracción por parametrización*. SICP 1.1 lo ilustra con el paso de escribir tres veces el mismo cálculo a escribir un procedimiento que recibe sus datos como parámetros: el nombre `promedio` y su parámetro `lista` capturan un patrón general y lo separan de los valores concretos. Una vez hecho ese corte, el `main` deja de saber cómo se calcula un promedio; solo sabe *que puede pedirlo*. Van Roy describe esto como la construcción de nuevas operaciones que enriquecen el vocabulario del programa: cada procedimiento con nombre es una palabra nueva que puedes usar en niveles superiores de abstracción.

La modularidad de Parnas lleva la idea más lejos: no se trata solo de tener funciones, sino de agruparlas de modo que cada módulo esconda una *decisión de diseño*. El criterio clave que Parnas propuso —contra la intuición de la época— no es dividir según los pasos del procesamiento, sino según lo que puede cambiar: un módulo debe encapsular aquello que quisieras poder modificar sin propagar cambios. En nuestro ejemplo mínimo, `promedio` oculta la decisión de usar división entera; si el requisito cambiara a promedio con decimales, tocarías un único lugar. Ese es el retorno de inversión de la modularidad, y la razón por la que Sebesta trata los subprogramas como uno de los mecanismos centrales de todo lenguaje.

Conviene fijar una distinción de vocabulario que Sebesta subraya: en sentido estricto, un *procedimiento* es un subprograma que actúa por sus efectos y no devuelve valor, mientras que una *función* devuelve un resultado. En la práctica actual la mayoría de los lenguajes del núcleo unifican ambos bajo "función", y aquí `promedio` es técnicamente una función porque retorna el promedio. El término "procedimental" nombra el *paradigma* —organizar el imperativo en unidades invocables con nombre—, no la ausencia de valor de retorno.

## 🧩 Situación

Imagina una hoja de cálculo de calificaciones donde, en cinco lugares distintos, alguien copió y pegó la misma retahíla para promediar una columna de notas. El día que descubren un error en ese cálculo —o que hay que redondear distinto— tienen que corregir los cinco sitios y rezar por no olvidar ninguno. La solución procedimental es evidente en retrospectiva: define `promedio(lista)` una sola vez y llámala cinco veces. El error se arregla en un punto; la intención ("aquí calculamos un promedio") queda dicha con una palabra en lugar de reconstruirse leyendo un bucle.

Aquí reproducimos ese salto con el problema mínimo que lo hace visible: leer una línea de enteros y emitir `promedio=<división entera de la suma entre la cantidad>`. El contrato de [`casos.json`](casos.json) fija tres casos (`2 4 6 → promedio=4`, `10 → promedio=10`, `3 5 → promedio=4`; nota que `8/2=4` por división entera). En vez de resolverlo todo dentro del `main`, extraemos el cálculo a un procedimiento `promedio` y dejamos que el programa principal se ocupe solo de leer la entrada y de imprimir. Esa separación de responsabilidades —una unidad calcula, otra orquesta— es el estilo procedimental en su forma más pequeña.

## 🧮 Modelo

- **Entrada** (stdin): una línea con enteros separados por espacio
- **Salida** (stdout): `promedio=<suma dividida entre la cantidad, entera>`
- **Regla:** promedio = suma / cantidad (división entera)

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `2 4 6` | `promedio=4` |
| `10` | `promedio=10` |
| `3 5` | `promedio=4` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
PROCEDIMIENTO promedio(lista): DEVOLVER suma(lista)/|lista|
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys


def promedio(lista):
    return sum(lista) // len(lista)


nums = [int(x) for x in sys.stdin.read().split()]
print(f"promedio={promedio(nums)}")
```

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

function promedio(lista) {
  const suma = lista.reduce((a, b) => a + b, 0);
  return Math.trunc(suma / lista.length);
}

const nums = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`promedio=${promedio(nums)}`);
```

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

function promedio(lista: number[]): number {
  const suma = lista.reduce((a, b) => a + b, 0);
  return Math.trunc(suma / lista.length);
}

const nums: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`promedio=${promedio(nums)}`);
```

### Java · [`java/Main.java`](implementaciones/java/Main.java) · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    static long promedio(int[] a) {
        long suma = 0;
        for (int x : a) suma += x;
        return suma / a.length;
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        int[] nums = new int[p.length];
        for (int i = 0; i < p.length; i++) nums[i] = Integer.parseInt(p[i]);
        System.out.println("promedio=" + promedio(nums));
    }
}
```

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;
using System.Linq;

long Promedio(int[] a) => a.Sum(x => (long) x) / a.Length;

int[] nums = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries)
    .Select(int.Parse).ToArray();
Console.WriteLine($"promedio={Promedio(nums)}");
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

func promedio(a []int) int {
	suma := 0
	for _, x := range a {
		suma += x
	}
	return suma / len(a)
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	var nums []int
	for _, s := range strings.Fields(line) {
		n, _ := strconv.Atoi(s)
		nums = append(nums, n)
	}
	fmt.Printf("promedio=%d\n", promedio(nums))
}
```

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn promedio(a: &[i64]) -> i64 {
    let suma: i64 = a.iter().sum();
    suma / a.len() as i64
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let nums: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    println!("promedio={}", promedio(&nums));
}
```

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long v[1024];
    int n = 0;
    while (scanf("%ld", &v[n]) == 1) n++;
    long suma = 0;
    for (int i = 0; i < n; i++) suma += v[i];
    printf("promedio=%ld\n", suma / n);
    return 0;
}
```

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL: AVG con división entera.
WITH nums(x) AS (VALUES (2), (4), (6))
SELECT printf('promedio=%d', sum(x) / count(*)) AS resultado FROM nums;
```

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
function promedio($a) {
    return intdiv(array_sum($a), count($a));
}

$nums = array_map('intval', preg_split('/\s+/', trim(fgets(STDIN))));
echo "promedio=" . promedio($nums) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🧪 Laboratorio guiado — recorrido del código

Sigamos el caso `2 4 6 → promedio=4` de [`casos.json`](casos.json) para ver cómo la abstracción procedimental separa el *qué* del *cómo*.

En **Python**, el archivo se lee ahora en dos niveles. Arriba, la definición `def promedio(lista): return sum(lista) // len(lista)` crea la abstracción: recibe una lista, la pliega a su suma con `sum`, la divide entre su longitud con `len` y usa `//` (división entera) para devolver el resultado. Con `[2, 4, 6]`: `sum` da 12, `len` da 3, y `12 // 3` es 4. Abajo, el programa principal es apenas `nums = [int(x) for x in sys.stdin.read().split()]` seguido de `print(f"promedio={promedio(nums)}")`. Observa el reparto de responsabilidades que esto crea: el `main` no sabe *cómo* se promedia —no aparece ninguna suma ni división en esas dos líneas—, solo sabe *que puede pedir* un promedio invocando el nombre. Eso es exactamente la caja negra de SICP 1.1: el procedimiento oculta su mecanismo tras su nombre y su contrato.

**C** encarna el estilo procedimental en su tierra natal, y aquí muestra una variante interesante. El `main` lee los números en un arreglo `v` (`while (scanf("%ld", &v[n]) == 1) n++;`) y luego calcula el promedio *en línea*, con su propio bucle de suma y una división `suma / n`. Es un recordatorio honesto de que la modularidad es una *decisión*, no una obligación del lenguaje: C podría extraer una función `long promedio(long *v, int n)` igual que hace **Java** con su método `static long promedio(int[] a)`. Java sí lo separa: define el procedimiento como método estático que recorre el arreglo acumulando en un `long` y retorna `suma / a.length`, y el `main` se limita a parsear la entrada y llamarlo. Con `2 4 6`, el método suma 12, divide entre 3 y devuelve 4; `System.out.println("promedio=" + promedio(nums))` imprime `promedio=4`.

Los demás lenguajes muestran el mismo procedimiento con sus acentos: **JavaScript** y **TypeScript** lo escriben con `reduce` para la suma y `Math.trunc(suma / lista.length)` para truncar hacia cero; **C#** lo comprime en una expresión flecha `long Promedio(int[] a) => a.Sum(x => (long) x) / a.Length;`; **Go** define `func promedio(a []int) int`; **Rust** define `fn promedio(a: &[i64]) -> i64` recibiendo un *slice* prestado; **PHP** usa `intdiv(array_sum($a), count($a))`. En todos, el patrón es idéntico: un procedimiento con nombre que recibe la lista y devuelve el promedio, invocado desde un `main` delgado. **SQL** vuelve a ser el caso declarativo: `sum(x) / count(*)` sobre una tabla de valores, donde la "modularidad" no es un procedimiento del usuario sino las funciones de agregación del motor —por eso su bloque incrusta los datos y el verificador lo marca *ilustrativo*—. Ejecuta `python scripts/verificar_equivalencia.py 109` para comprobar que todas producen las salidas de `casos.json`.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Cada lenguaje define el procedimiento a su manera. |
| Semántica | El procedimiento agrupa pasos imperativos bajo un nombre. |
| Paradigmática | SQL usa AVG (declarativo). |

Más allá de la sintaxis, la diferencia sustantiva está en *cómo se pasan los datos al procedimiento*, un tema que Sebesta trata a fondo en el capítulo 9. Rust es el más explícito: `promedio(a: &[i64])` recibe una *referencia prestada* al slice, sin copiar ni tomar posesión, lo que el compilador verifica con su sistema de propiedad. C pasa un puntero y una longitud por separado (`long *v, int n`), dejando en manos del programador la coherencia entre ambos —fuente clásica de errores—. Java, C# y Go pasan referencias a arreglos gestionados por el recolector de basura, así que el procedimiento puede recorrerlos sin preocuparse por la memoria. Otra diferencia real es la semántica de la división entera: Python usa `//` (redondeo hacia menos infinito), JavaScript y TypeScript necesitan `Math.trunc` porque `/` produce un flotante, C# y PHP usan división entera y `intdiv` respectivamente, y Go/Rust dividen enteros truncando hacia cero por defecto. Para valores positivos como los de `casos.json` todas coinciden, pero con negativos `//` y `trunc` divergirían: la equivalencia observada no garantiza equivalencia en todos los dominios.

## 🧬 El concepto en la familia

C y Pascal son los estandartes históricos del estilo procedimental: lenguajes en los que el programa *es* un conjunto de procedimientos que se llaman entre sí, sin clases ni objetos de por medio. C, además, popularizó la separación entre la *declaración* de un procedimiento (su firma, en un archivo de cabecera) y su *definición* (su cuerpo), que es la forma más pura del ocultamiento de información de Parnas: quien usa el módulo ve solo la interfaz. El resto de los lenguajes del núcleo heredaron y ampliaron esta capacidad: Go la ofrece con funciones y paquetes; Java y C# la envuelven dentro de clases (un método estático es, a efectos prácticos, un procedimiento modular); Python, JavaScript y PHP permiten funciones libres de primer nivel. Incluso los lenguajes que asociamos con otros paradigmas siguen apoyándose en la abstracción procedimental como su capa base: por debajo de todo objeto o toda expresión funcional hay procedimientos con nombre. Por eso el estilo procedimental no es una etapa "superada", sino el andamiaje sobre el que se construyen los demás.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 109
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Dividir sin controlar la cantidad 0** → causa: llamar a `promedio` con una lista vacía, lo que provoca una división por cero (en C, comportamiento indefinido o *crash*; en Python, `ZeroDivisionError`) → remedio: aunque `casos.json` garantiza al menos un elemento, un procedimiento robusto documenta su precondición ("la lista no puede estar vacía") o la valida al entrar; la abstracción incluye definir qué entradas acepta.
- **Meter todo en el `main`** → causa: resolver el problema en línea por prisa, sin extraer el cálculo, de modo que el código se vuelve un bloque monolítico difícil de reutilizar y probar → remedio: aplica el criterio de Parnas y pregunta "¿qué parte de esto querría cambiar o reutilizar por separado?"; ahí está el corte natural para un procedimiento con nombre.
- **Procedimiento con demasiadas responsabilidades** → causa: una función que además de calcular también lee la entrada e imprime, mezclando lógica y entrada/salida → remedio: separa el cálculo puro (`promedio`) de la orquestación (leer y escribir en el `main`); un procedimiento que solo transforma datos es más fácil de probar aisladamente que uno que también toca el mundo exterior.

## ❓ Preguntas frecuentes

- **¿Cuál es la diferencia entre procedimiento y función?** En la terminología clásica que recoge Sebesta, un procedimiento se ejecuta por sus *efectos* (modifica estado, imprime) y no devuelve valor, mientras que una función *devuelve un resultado* y, en el ideal, no tiene efectos secundarios. Aquí `promedio` es técnicamente una función porque retorna un número. "Procedimental" nombra el paradigma —organizar el imperativo en unidades invocables—, no la distinción concreta procedimiento/función.
- **¿El estilo procedimental está anticuado?** No: es la capa base sobre la que descansan la orientación a objetos y la programación funcional. Un método es un procedimiento adjunto a un objeto; una función pura es un procedimiento sin efectos. Los lenguajes más modernos del núcleo (Go, Rust) reivindican explícitamente la claridad procedimental. Lo que ha cambiado no es su vigencia, sino que ahora convive con otras formas de organizar el código.
- **¿En qué se diferencia la modularidad de Parnas de simplemente "usar funciones"?** Tener funciones es una condición necesaria pero no suficiente. La aportación de Parnas es el *criterio* de descomposición: no dividas según los pasos del algoritmo, sino según las decisiones de diseño que quieres poder cambiar sin propagar el cambio. Un buen módulo oculta una decisión (aquí, cómo se calcula el promedio) detrás de una interfaz estable.

## 🔗 Referencias

**Libros de la parte:**

- P. Van Roy y S. Haridi — *Concepts, Techniques, and Models of Computer Programming* (MIT Press). La construcción de abstracciones y el enriquecimiento del vocabulario del programa.
- H. Abelson y G. J. Sussman — *Structure and Interpretation of Computer Programs* (2ª ed., MIT Press). Secciones 1.1 y 1.2: abstracción procedimental y evolución de procesos.
- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson). Capítulo 9: subprogramas, paso de parámetros, ámbito y valores de retorno.
- D. L. Parnas — "On the Criteria to Be Used in Decomposing Systems into Modules" (*Communications of the ACM*, 1972), sobre el ocultamiento de información.

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

> [⏮️ Clase 108](../../parte-7-paradigmas/108-imperativo-y-estructurado/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 110 ⏭️](../../parte-7-paradigmas/110-orientado-a-objetos-clases-objetos-y-estado/README.md)
