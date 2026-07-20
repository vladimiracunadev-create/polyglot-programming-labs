# Clase 141 — Depuradores: gdb, lldb, pdb y los de IDE

> Parte **9 — Ingeniería de software políglota** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Un **depurador** es el instrumento que congela un programa en marcha y te deja mirar dentro: pausar en una línea, inspeccionar cada variable, avanzar una instrucción a la vez y ver cómo el estado se transforma. Hunt y Thomas, en *The Pragmatic Programmer*, dedican todo un apartado a la depuración y su primera regla es psicológica antes que técnica: *"fix the problem, not the blame"*. Depurar no es adivinar ni cambiar líneas al azar hasta que "funcione"; es un método científico en miniatura —observar el síntoma, formular una hipótesis, comprobarla observando el estado real, y no dar nada por sentado, empezando por tus propias suposiciones.

El ejercicio de esta clase materializa esa observación. En lugar de acumular una suma en silencio y emitir solo el total, emitimos la **traza** de estados intermedios: para `n = 3`, la salida `1-3-6` es el valor del acumulador después de cada paso, exactamente lo que verías en el panel de variables de un depurador mientras pulsas *step* una y otra vez. Convertir el estado invisible en una secuencia observable es la esencia de la depuración; aquí lo hacemos con `print`, y en el mundo real lo harás con gdb, lldb, pdb, delve, `node --inspect` o el depurador integrado de tu IDE, que son los nombres que da cada runtime a la misma idea.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. **Producir** una traza de estados intermedios que revele la evolución de una variable paso a paso.
2. **Explicar** qué hacen *breakpoint*, *step* y *watch*, y cuándo usar cada uno.
3. **Nombrar** el depurador propio de cada runtime (gdb, lldb, pdb, delve, JDB, los de VS/Rider).
4. **Aplicar** un método sistemático de depuración en vez de cambiar código al azar.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Traza de estado | Hacer visible la variable que evoluciona es el 80 % del diagnóstico |
| 2 | Paso a paso (step) | Avanzar una instrucción y ver el cambio exacto elimina la conjetura |
| 3 | Punto de ruptura (breakpoint) | Pausar justo donde importa, sin recompilar ni ensuciar con prints |
| 4 | Expresión vigilada (watch) | Ver cómo cambia un valor concreto a lo largo de la ejecución |

## 📖 Definiciones y características

- **Depurador.** Programa que controla la ejecución de otro: lo pausa, lee su memoria y sus variables, y lo reanuda bajo tus órdenes. Los nativos como gdb y lldb operan sobre binarios compilados (C, C++, Rust) con símbolos de depuración; pdb interpreta Python en su propio bucle; delve entiende el runtime de Go; `node --inspect` expone un protocolo al que se conecta Chrome DevTools o VS Code. Todos comparten el mismo repertorio de acciones.
- **Traza.** La secuencia de estados por los que pasa el programa. Cuando un resultado sorprende, la traza es lo que delata *dónde* se desvió de lo esperado. Nuestra `1-3-6` es una traza fabricada a mano; un depurador la genera sobre la marcha sin tocar el código.
- **Paso a paso (step).** Avanzar de forma controlada: *step over* ejecuta la línea sin entrar en las funciones que llama, *step into* baja al interior de la llamada, *step out* termina la función actual y vuelve a quien la invocó. Elegir bien entre ellos es lo que evita ahogarse en detalles irrelevantes.
- **Punto de ruptura y watch.** Un *breakpoint* pausa la ejecución al llegar a una línea (o cuando se cumple una condición, como `i == 100`); un *watch* es una expresión que el depurador reevalúa en cada pausa, o incluso un *watchpoint* que detiene el programa en cuanto una variable cambia de valor.

## 🧩 Situación

Una función de sumatoria devuelve un total que "está mal por poco" y nadie sabe por qué. En vez de sembrar `print` por todo el archivo y recompilar cinco veces, pones un *breakpoint* dentro del bucle, defines un *watch* sobre el acumulador y avanzas paso a paso. En el tercer paso ves que el acumulador salta de `3` a `6` cuando esperabas `1-3-6`… pero en la iteración siguiente no se reinicia y arrastra el valor: ahí está el defecto, visible en un segundo. La traza `1-3-6` de esta clase es esa misma película del acumulador, congelada en texto.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n` (n >= 1)
- **Salida** (stdout): `traza=<sumas acumuladas 1..n unidas por ->`
- **Regla:** traza[i] = 1 + 2 + ... + i

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3` | `traza=1-3-6` |
| `1` | `traza=1` |
| `4` | `traza=1-3-6-10` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
acc <- 0 ; PARA i de 1 a n: acc <- acc+i ; emitir acc
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/). Todos comparten la misma anatomía —una variable `acc` que arranca en cero, un bucle de `1` a `n`, y la captura del estado en cada vuelta—, que es justo lo que inspeccionarías con un depurador. Lee el bucle imaginando un *breakpoint* en la línea del `acc += i`.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys

n = int(sys.stdin.readline())
acc = 0
pasos = []
for i in range(1, n + 1):
    acc += i
    pasos.append(acc)
print("traza=" + "-".join(str(x) for x in pasos))
```

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

Esta versión hace explícito lo que un depurador te enseñaría implícitamente. Si abrieras este archivo con pdb (`python -m pdb main.py`), pondrías un *breakpoint* en `acc += i` con `break 7`, correrías con `continue` y en cada pausa consultarías el valor con `p acc`: verías `1`, luego `3`, luego `6`, la misma secuencia que `pasos` va acumulando. La lista `pasos` es, literalmente, el registro de lo que un *watch* sobre `acc` mostraría en cada iteración; y el `"-".join(...)` final solo la aplana a la cadena que el contrato exige. Depurar así, con la variable a la vista en cada paso, es lo que Hunt y Thomas llaman no dar nada por supuesto: en lugar de creer que `acc` vale lo que crees, lo compruebas.

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
let acc = 0;
const pasos = [];
for (let i = 1; i <= n; i++) {
  acc += i;
  pasos.push(acc);
}
console.log(`traza=${pasos.join("-")}`);
```

🧬 **El mismo programa en la familia JavaScript / web:** [Dart · ActionScript](primos.md#javascript-web)

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
let acc = 0;
const pasos: number[] = [];
for (let i = 1; i <= n; i++) {
  acc += i;
  pasos.push(acc);
}
console.log(`traza=${pasos.join("-")}`);
```

🧬 **El mismo programa en la familia JavaScript / web:** [Dart · ActionScript](primos.md#javascript-web)

### Java · [`java/Main.java`](implementaciones/java/Main.java) · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        long acc = 0;
        StringBuilder sb = new StringBuilder();
        for (int i = 1; i <= n; i++) {
            acc += i;
            if (i > 1) sb.append("-");
            sb.append(acc);
        }
        System.out.println("traza=" + sb);
    }
}
```

🧬 **El mismo programa en la familia JVM:** [Kotlin · Scala · Groovy · Clojure](primos.md#jvm)

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;
using System.Text;

int n = int.Parse(Console.In.ReadToEnd().Trim());
long acc = 0;
var sb = new StringBuilder();
for (int i = 1; i <= n; i++) {
    acc += i;
    if (i > 1) sb.Append("-");
    sb.Append(acc);
}
Console.WriteLine($"traza={sb}");
```

🧬 **El mismo programa en la familia .NET:** [F# · VB.NET](primos.md#dotnet)

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
	acc := 0
	var pasos []string
	for i := 1; i <= n; i++ {
		acc += i
		pasos = append(pasos, strconv.Itoa(acc))
	}
	fmt.Printf("traza=%s\n", strings.Join(pasos, "-"))
}
```

🧬 **El mismo programa en la familia Sistemas:** [Zig · Nim · D](primos.md#sistemas)

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let mut acc = 0i64;
    let mut pasos: Vec<String> = Vec::new();
    for i in 1..=n {
        acc += i;
        pasos.push(acc.to_string());
    }
    println!("traza={}", pasos.join("-"));
}
```

🧬 **El mismo programa en la familia Sistemas:** [Zig · Nim · D](primos.md#sistemas)

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    long acc = 0;
    printf("traza=");
    for (long i = 1; i <= n; i++) {
        acc += i;
        if (i > 1) printf("-");
        printf("%ld", acc);
    }
    printf("\n");
    return 0;
}
```

🧬 **El mismo programa en la familia C / llaves:** [C++ · Objective-C](primos.md#c-llaves)

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL: sumas acumuladas con función de ventana (ilustrativo, n=3).
WITH RECURSIVE r(i) AS (VALUES (1) UNION ALL SELECT i + 1 FROM r WHERE i < 3)
SELECT 'traza=' || group_concat(s, '-') AS resultado
FROM (SELECT sum(i) OVER (ORDER BY i) AS s FROM r);
```

🧬 **El mismo programa en la familia Lógica y declarativa:** [Prolog · Datalog](primos.md#logica-declarativa)

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
$n = (int) trim(fgets(STDIN));
$acc = 0;
$pasos = [];
for ($i = 1; $i <= $n; $i++) {
    $acc += $i;
    $pasos[] = $acc;
}
echo "traza=" . implode("-", $pasos) . "\n";
```

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

El contraste entre runtimes es aquí más que sintáctico: determina *qué depurador* usas. La versión en **C** compila a un binario nativo, así que la depurarías con gdb o lldb tras compilar con símbolos (`cc -g main.c`); pondrías `break main.c:8`, avanzarías con `next` e inspeccionarías con `print acc`. La de **Go** usa acumulador `int` y se depura con **delve** (`dlv debug`), que entiende las goroutines y el runtime del lenguaje mejor que gdb. La de **Java** corre en la JVM: se depura con JDB o, en la práctica, con el depurador de IntelliJ o VS Code hablando por JDWP; nota que usa `long acc` porque Bloch, en *Effective Java*, recuerda vigilar el desbordamiento de `int` en sumatorias. **C#** se depura con el motor de Visual Studio o Rider. Un solo algoritmo, cinco instrumentos distintos, pero el gesto —pausar, mirar `acc`, avanzar— es idéntico en todos.

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

Cada runtime tiene su depurador de referencia, y conocer el nombre y el comando de entrada ahorra horas.

| Lenguaje | Depurador de referencia | Cómo se lanza | Comando de paso típico |
|---|---|---|---|
| Python | pdb / debugpy | `python -m pdb main.py` | `n` (next), `s` (step), `p acc` |
| JavaScript | Inspector de V8 | `node --inspect-brk main.mjs` | *step over* / `watch` en DevTools |
| TypeScript | Inspector de V8 (con *source maps*) | `node --inspect` sobre el JS emitido | igual que JS, mapeado al `.ts` |
| Java | JDB / depurador de IDE (JDWP) | `jdb` · IntelliJ · VS Code | `step`, `stepi`, `print` |
| C# | Depurador de VS / Rider / `vsdbg` | F5 en Visual Studio · Rider | *Step Into*, ventana *Watch* |
| Go | delve | `dlv debug` | `next`, `step`, `print acc` |
| Rust | gdb / lldb (con `rust-gdb`) | `rust-gdb ./main` | `next`, `step`, `print acc` |
| C | gdb / lldb | `gdb ./main` (compilar con `-g`) | `next`, `step`, `print acc` |
| SQL | `EXPLAIN` / logs del motor | según motor | inspección del plan, no paso a paso |
| PHP | Xdebug | cliente DBGp (VS Code, PhpStorm) | *step over*, *step into* |

Dos cosas saltan a la vista. Primero, los binarios nativos (C, Rust) comparten gdb/lldb, mientras que los lenguajes con runtime propio traen su instrumento especializado —delve para Go, Xdebug para PHP, pdb para Python— porque conocen las estructuras internas que un depurador genérico ignora. Segundo, SQL rompe el molde: no se "avanza paso a paso" por una consulta declarativa; su equivalente a depurar es leer el *plan de ejecución* con `EXPLAIN`, que revela cómo el motor decidió resolverla.

## 🧬 El concepto en la familia

Todos estos instrumentos —gdb, lldb, pdb, delve, el Inspector de V8, JDB, los depuradores de Visual Studio y Rider, Xdebug— son variantes de una misma abstracción: un proceso controlador que suspende, examina y reanuda otro proceso. Los IDE (VS Code, IntelliJ, Rider) suelen ser una capa gráfica sobre uno de estos motores, hablando protocolos como DAP o JDWP. Aprende el modelo mental una vez —breakpoint, step, watch, call stack— y solo cambiarás de teclado, no de idea, al saltar de lenguaje.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 141
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Depurar cambiando código al azar.** Modificar líneas "a ver si así funciona" sin una hipótesis es lo contrario de depurar. Observa el estado real, formula una hipótesis y compruébala, como aconsejan Hunt y Thomas.
- **Compilar sin símbolos de depuración.** Sin `-g` en C/Rust, gdb no puede mostrarte nombres de variables ni líneas de código fuente, solo direcciones. Compila en modo *debug* antes de depurar.
- **Abusar del `print` y dejarlo.** Los `print` de depuración son legítimos, pero un breakpoint no ensucia el código ni exige recompilar, y no se te olvidará quitarlo antes del *commit*.
- **No reiniciar el estado entre casos.** Un acumulador que no vuelve a cero, una variable global que arrastra valor: el defecto clásico que la traza paso a paso delata de inmediato.

## ❓ Preguntas frecuentes

- **¿`print` o depurador?** Ambos tienen su lugar. El `print` es rápido para una sospecha puntual; el depurador brilla cuando no sabes dónde mirar, porque avanzas paso a paso e inspeccionas cualquier variable sin recompilar ni tocar el código.
- **¿Qué es exactamente un watch?** Una expresión que el depurador reevalúa en cada pausa (por ejemplo `acc * 2`), o un *watchpoint* que detiene el programa en cuanto una variable cambia de valor, útil para cazar quién la modifica.
- **¿Puedo depurar en producción?** Rara vez con un depurador que pausa el proceso —congelaría el servicio—. Para eso está la observabilidad (logs, métricas, trazas) de la clase siguiente; el depurador es la herramienta del desarrollo.

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

> [⏮️ Clase 140](../../parte-9-ingenieria-de-software-poliglota/140-pruebas-de-integracion-y-el-verificador-de-equivalencia/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 142 ⏭️](../../parte-9-ingenieria-de-software-poliglota/142-registro-logging-y-observabilidad/README.md)
