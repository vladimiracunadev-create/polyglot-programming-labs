# Clase 124 — Compilador, intérprete y JIT

> Parte **8 — Cómo funcionan los lenguajes** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

La clase 123 mostró que todo lenguaje tokeniza y parsea; esta responde a la pregunta que abría allí: *¿qué se hace con el AST después?* Hay tres respuestas, y son el corazón de por qué un mismo programa —contar los dígitos de un número— rinde distinto en C, en Python y en JavaScript. Un **compilador** traduce todo el código a instrucciones de máquina *antes* de que el programa corra; un **intérprete** recorre la representación interna y actúa sobre ella *mientras* corre; y un **JIT** (*just-in-time*) empieza interpretando pero, al detectar código que se ejecuta muchas veces, lo compila a máquina *durante* la ejecución. El *porqué* de distinguirlos es práctico: explica por qué un binario de C arranca en microsegundos y un proceso de la JVM tarda en «calentar», por qué un error de tipos detiene a `rustc` pero no a Python hasta que la línea se ejecuta, y por qué los tres modelos coexisten hoy en el mismo runtime. Nystrom dedica la segunda mitad de *Crafting Interpreters* justamente a este salto: de un intérprete de árbol (*tree-walk*) a una VM con compilación a bytecode.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Contar los dígitos de un entero midiendo su representación textual.
2. Distinguir compilación AOT, interpretación y JIT por *cuándo* traducen a código de máquina.
3. Relacionar cada modelo con su perfil de rendimiento (arranque, régimen, memoria).
4. Explicar por qué el modelo de ejecución no altera el resultado, solo el camino hacia él.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Compilador (AOT) | Traduce todo antes de ejecutar; errores y coste de traducción por adelantado |
| 2 | Intérprete | Ejecuta la representación interna al vuelo; arranque inmediato, régimen más lento |
| 3 | JIT | Compila lo «caliente» durante la ejecución; combina arranque rápido y régimen veloz |

## 📖 Definiciones y características

Un **compilador anticipado (AOT, *ahead-of-time*)** hace todo el trabajo de traducción antes de que exista el primer dato de entrada. `cc main.c -o main` produce un binario de instrucciones de la CPU; cuando lo ejecutas, no queda rastro del texto fuente. Como todo el programa pasó por el front-end y el back-end del Dragon Book, el compilador tuvo la oportunidad de rechazar errores de tipo y de optimizar globalmente. El precio es que cualquier cambio exige recompilar, y el arranque incluye cargar y enlazar un binario ya listo.

Un **intérprete** conserva la representación interna del programa (bytecode o AST) y la recorre paso a paso en tiempo de ejecución. CPython compila tu `.py` a bytecode `.pyc` y luego un bucle de evaluación —la *VM* de Python— ejecuta esas instrucciones una a una. La ventaja es la flexibilidad y el arranque inmediato: no hay fase de espera. El coste es el sobrecoste de *interpretar* cada instrucción cada vez que se ejecuta, incluso dentro de un bucle apretado.

Un **compilador JIT** es la síntesis. El motor V8 de JavaScript y la HotSpot de la JVM empiezan interpretando (o compilando de forma rápida y tosca), miden qué funciones y bucles son *hot* —se repiten mucho— y solo entonces invierten en compilarlos a código de máquina optimizado, con información que un compilador AOT no tiene: los tipos reales que se vieron en ejecución. Por eso un servicio Java «calienta»: los primeros segundos van interpretados y luego aceleran. El JIT paga un coste de compilación en tiempo de ejecución a cambio de un régimen casi tan rápido como el AOT.

## 🧩 Situación

Te dicen que «Python es lento y C es rápido» y lo aceptas sin matiz. Pero cuando escribes un script que se ejecuta una vez y termina, el arranque instantáneo del intérprete gana; cuando escribes un servicio que corre horas, el JIT de la JVM alcanza a C tras el calentamiento; y cuando el programa es un binario que debe arrancar en un microcontrolador, solo el AOT sirve. Contar dígitos —una operación que da el mismo `digitos=5` en los tres modelos— es el laboratorio perfecto: aísla el *modelo de ejecución* de la *lógica*, y deja ver que la diferencia no está en el resultado sino en el viaje.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n` (n >= 0)
- **Salida** (stdout): `digitos=<cantidad de dígitos>`
- **Regla:** contar los dígitos de n (0 tiene 1)

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `12345` | `digitos=5` |
| `7` | `digitos=1` |
| `100` | `digitos=3` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
contar dígitos dividiendo por 10 hasta 0 (o longitud del texto)
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys

n = int(sys.stdin.readline())
print(f"digitos={len(str(n))}")
```

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const n = readFileSync(0, "utf8").trim();
console.log(`digitos=${n.length}`);
```

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const n: string = readFileSync(0, "utf8").trim();
console.log(`digitos=${n.length}`);
```

### Java · [`java/Main.java`](implementaciones/java/Main.java) · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String n = br.readLine().trim();
        System.out.println("digitos=" + n.length());
    }
}
```

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;

string n = Console.In.ReadToEnd().Trim();
Console.WriteLine($"digitos={n.Length}");
```

### Go · [`go/main.go`](implementaciones/go/main.go) · `go run main.go`

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
	n := strings.TrimSpace(line)
	fmt.Printf("digitos=%d\n", len(n))
}
```

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n = s.trim();
    println!("digitos={}", n.len());
}
```

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char n[64];
    if (scanf("%63s", n) != 1) return 1;
    printf("digitos=%d\n", (int) strlen(n));
    return 0;
}
```

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL: length sobre el texto del número.
WITH nums(n) AS (VALUES ('12345'))
SELECT printf('digitos=%d', length(n)) AS resultado FROM nums;
```

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
$n = trim(fgets(STDIN));
echo "digitos=" . strlen($n) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🧪 Laboratorio: recorrido del código

El truco compartido por casi todas las implementaciones es contar dígitos *sin aritmética*: leer el número como texto y medir su longitud. Es una decisión reveladora, porque hace que el trabajo real —contar caracteres— sea idéntico y deja el modelo de ejecución como única variable.

En **Python**, `n = int(sys.stdin.readline())` convierte la entrada a entero y `len(str(n))` la vuelve a texto para medirla. Cada una de esas operaciones se ejecuta interpretando bytecode: CPython ya compiló el `.py` a instrucciones internas, y su bucle de evaluación las recorre. Si el programa estuviera dentro de un bucle de un millón de iteraciones, ese sobrecoste de interpretar `LOAD_NAME`, `CALL_FUNCTION`, etc., se pagaría un millón de veces. Aquí, con una sola línea de entrada, es imperceptible.

En **C**, `scanf("%63s", n)` lee el número como cadena y `strlen(n)` cuenta sus caracteres. Pero lo decisivo es que `strlen` y el `printf` ya son código de máquina antes de arrancar: `cc` los tradujo, el enlazador los unió con la libc, y el binario resultante no interpreta nada. Por eso el arranque es un `exec` del sistema operativo y la ejecución, instrucciones directas de la CPU. No hay «calentamiento» ni bucle de evaluación: es el modelo AOT en estado puro.

En **JavaScript**, `readFileSync(0, "utf8").trim()` y `n.length` corren sobre V8, un JIT. En la primera ejecución V8 interpreta con su intérprete *Ignition*; si esta función se llamara millones de veces, el compilador *TurboFan* la recompilaría a máquina especializando el tipo de `n` como cadena. Para un programa de una sola pasada como este, el JIT nunca llega a activarse: pagas el arranque del intérprete y no cosechas la aceleración. Ese es el matiz que la frase «JS usa JIT» esconde: el JIT ayuda al código *repetido*, no al de una sola vez.

## 🔬 Comparación

| Rasgo del runtime | Cómo se reparte entre los 10 lenguajes |
|---|---|
| Traducción a máquina | Antes de ejecutar: C, Rust, Go. Durante: Java, C#, JS (JIT). Nunca del todo: Python, PHP interpretan bytecode. |
| Arranque | Instantáneo en intérpretes; con carga de binario en AOT; con «calentamiento» en JIT de larga vida (JVM). |
| Detección de errores de tipo | En compilación (C, Rust, Go, Java, C#); en ejecución al llegar la línea (Python, JS, PHP). |
| Régimen sostenido | AOT y JIT maduro son comparables; el intérprete puro paga sobrecoste por instrucción. |
| SQL | No encaja en el eje: el motor de la BD planifica y ejecuta la consulta; `length` opera sobre el texto. |

## 🧬 El concepto en la familia

Las etiquetas se difuminan en cuanto miras de cerca. Python «interpretado» compila a bytecode; Java «compilado» ejecuta bytecode que la JVM vuelve a compilar con JIT; JavaScript «interpretado» corre sobre uno de los JIT más sofisticados del mundo. GraalVM incluso compila Java AOT a binario nativo para arrancar rápido, sacrificando el calentamiento del JIT. La lección de *Crafting Interpreters* aplica aquí: intérprete y compilador no son especies opuestas sino puntos de un continuo definido por *cuándo* traduces y *cuánto* optimizas con la información disponible en ese momento.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 124
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Creer que «interpretado» y «compilado» se excluyen** → causa: pensar en dos cajones estancos → solución: casi todo lenguaje moderno compila a *algo* (bytecode) y luego lo interpreta o lo re-compila con JIT.
- **Esperar el pico de rendimiento del JIT en un script corto** → causa: el JIT solo invierte en compilar lo que se repite → solución: para medir de verdad un runtime JIT, hay que dejarlo «calentar» con muchas iteraciones antes de cronometrar.
- **Contar el `0` como cero dígitos** → causa: el enfoque aritmético (dividir por 10) no entra al bucle con `n=0` → solución: la implementación mide la longitud del texto, donde `"0"` ya tiene un carácter; el caso límite queda cubierto.

## ❓ Preguntas frecuentes

- **¿Cuál es más rápido?** Depende del régimen. En arranque gana el intérprete; en ejecución sostenida, AOT y JIT maduro empatan; en un cálculo largo de una sola pasada, el AOT suele liderar.
- **¿Python compila?** Sí, a bytecode (`.pyc`); lo que interpreta es ese bytecode, no el texto fuente. Por eso es más justo llamarlo «compilado a bytecode, ejecutado por una VM».
- **¿Qué es «calentar» la JVM?** Es la fase inicial en que el código va interpretado mientras el JIT reúne estadísticas; al superar los umbrales, recompila las funciones calientes a máquina y el rendimiento sube de golpe.

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

> [⏮️ Clase 123](../../parte-8-como-funcionan-los-lenguajes/123-del-codigo-a-la-ejecucion-fases-de-compilacion/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 125 ⏭️](../../parte-8-como-funcionan-los-lenguajes/125-bytecode-y-maquinas-virtuales-jvm-clr-v8/README.md)
