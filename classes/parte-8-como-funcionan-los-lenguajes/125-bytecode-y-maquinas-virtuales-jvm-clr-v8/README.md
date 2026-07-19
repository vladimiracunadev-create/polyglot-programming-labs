# Clase 125 — Bytecode y máquinas virtuales (JVM, CLR, V8)

> Parte **8 — Cómo funcionan los lenguajes** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Cuando `javac` compila tu clase, no produce código de máquina sino **bytecode**: una lista de instrucciones muy simples para una **máquina virtual (VM)** imaginaria. La JVM, el CLR de .NET y V8 ejecutan ese bytecode, y la mayoría lo hace sobre una *pila de operandos*. Esta clase abre esa caja negra evaluando una expresión en **notación polaca inversa (RPN)** —`3 4 +`— porque RPN *es*, literalmente, cómo piensa una VM de pila: apila los operandos, y cuando llega un operador, los desapila, opera y apila el resultado. El *porqué* es doble. Primero, entender el bytecode explica la portabilidad («compila una vez, corre en cualquier sistema»): el bytecode no depende de la CPU, solo de la VM. Segundo, entender la máquina de pila explica por qué las instrucciones no necesitan nombrar registros —el operando implícito es «el tope de la pila»—, lo que las hace compactas y fáciles de generar. Nystrom construye exactamente esta VM de pila en la Parte III de *Crafting Interpreters*, con sus `OP_CONSTANT`, `OP_ADD` y un puntero de pila.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Evaluar una expresión RPN empujando y sacando valores de una pila.
2. Relacionar la RPN con el ciclo *fetch–decode–execute* de una VM de pila.
3. Explicar qué es el bytecode y por qué da portabilidad entre sistemas operativos.
4. Distinguir una máquina de *pila* de una máquina de *registros* y nombrar ejemplos de cada una.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Máquina de pila | El operando implícito es el tope; instrucciones sin registros |
| 2 | RPN | El orden operandos-luego-operador imita el bytecode de pila |
| 3 | Bytecode | Código intermedio portable que la VM interpreta o compila con JIT |

## 📖 Definiciones y características

El **bytecode** es un código intermedio: más bajo que el fuente, más alto que el código de máquina. `javac` genera un `.class` lleno de opcodes de un byte (de ahí el nombre) como `iload`, `iadd`, `invokevirtual`. Ese archivo no sabe nada de x86 ni de ARM; solo de la JVM. Esa indirección es la que cumple la promesa de Java, «*write once, run anywhere*»: basta con que exista una JVM para tu plataforma. El CLR de .NET hace lo mismo con su *IL* (*Intermediate Language*), y CPython con sus opcodes en `.pyc`.

Una **máquina virtual de pila** ejecuta ese bytecode manteniendo una pila de operandos. La instrucción `push 3` deja un 3 en la cima; `push 4`, un 4 encima; `add` desapila los dos, los suma y apila el 7. Ninguna instrucción menciona dónde están los datos —siempre operan sobre el tope—, y por eso el bytecode de pila es tan denso y tan sencillo de generar desde un AST: recorres el árbol en postorden y emites una instrucción por nodo. La alternativa, una *máquina de registros* (como Lua 5 o Dalvik de Android), nombra explícitamente sus operandos y produce menos instrucciones pero más grandes.

La **notación polaca inversa (RPN)** escribe el operador *después* de sus operandos: `3 4 +` en vez de `3 + 4`. No necesita paréntesis ni reglas de precedencia, y se evalúa en una sola pasada con una pila. Esta correspondencia no es casualidad: la RPN es la forma textual del recorrido postorden de un árbol de expresión, el mismo recorrido que un compilador usa para emitir bytecode de pila.

## 🧩 Situación

Un colega afirma que «Java es más portable que C». Sin el concepto de bytecode, la frase es un eslogan. Con él, es un mecanismo concreto: el binario de C está clavado a una arquitectura de CPU, mientras que el `.class` de Java habla el idioma de una máquina abstracta que cada plataforma implementa. Reproducir la evaluación de `3 4 +` con una pila —empujar, empujar, desapilar dos, operar, empujar— te deja tocar con las manos el ciclo que la JVM repite millones de veces por segundo, y entender por qué las instrucciones de bytecode son tan minúsculas.

## 🧮 Modelo

- **Entrada** (stdin): una línea `a b op` (dos enteros y un operador +, -, *)
- **Salida** (stdout): `resultado=<a op b>`
- **Regla:** apilar a y b; aplicar op; el tope es el resultado

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3 4 +` | `resultado=7` |
| `5 6 *` | `resultado=30` |
| `10 2 -` | `resultado=8` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
PARA cada token: SI número, apilar; SI operador, desapilar 2, aplicar, apilar
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

a, b, op = sys.stdin.readline().split()
pila = [int(a), int(b)]
y = pila.pop()
x = pila.pop()
r = x + y if op == "+" else x - y if op == "-" else x * y
print(f"resultado={r}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const [a, b, op] = readFileSync(0, "utf8").trim().split(/\s+/);
const pila = [Number(a), Number(b)];
const y = pila.pop(), x = pila.pop();
const r = op === "+" ? x + y : op === "-" ? x - y : x * y;
console.log(`resultado=${r}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const [a, b, op] = readFileSync(0, "utf8").trim().split(/\s+/);
const pila: number[] = [Number(a), Number(b)];
const y = pila.pop()!, x = pila.pop()!;
const r = op === "+" ? x + y : op === "-" ? x - y : x * y;
console.log(`resultado=${r}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayDeque;
import java.util.Deque;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] t = br.readLine().trim().split("\\s+");
        Deque<Long> pila = new ArrayDeque<>();
        pila.push(Long.parseLong(t[0]));
        pila.push(Long.parseLong(t[1]));
        long y = pila.pop(), x = pila.pop();
        long r = t[2].equals("+") ? x + y : t[2].equals("-") ? x - y : x * y;
        System.out.println("resultado=" + r);
    }
}
```

### C# · `dotnet run`

```csharp
using System;
using System.Collections.Generic;

string[] t = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
var pila = new Stack<long>();
pila.Push(long.Parse(t[0]));
pila.Push(long.Parse(t[1]));
long y = pila.Pop(), x = pila.Pop();
long r = t[2] switch { "+" => x + y, "-" => x - y, _ => x * y };
Console.WriteLine($"resultado={r}");
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
	t := strings.Fields(line)
	x, _ := strconv.Atoi(t[0])
	y, _ := strconv.Atoi(t[1])
	var r int
	switch t[2] {
	case "+":
		r = x + y
	case "-":
		r = x - y
	default:
		r = x * y
	}
	fmt.Printf("resultado=%d\n", r)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let t: Vec<&str> = s.split_whitespace().collect();
    let mut pila: Vec<i64> = vec![t[0].parse().unwrap(), t[1].parse().unwrap()];
    let y = pila.pop().unwrap();
    let x = pila.pop().unwrap();
    let r = match t[2] {
        "+" => x + y,
        "-" => x - y,
        _ => x * y,
    };
    println!("resultado={r}");
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long x, y;
    char op;
    if (scanf("%ld %ld %c", &x, &y, &op) != 3) return 1;
    long r = op == '+' ? x + y : op == '-' ? x - y : x * y;
    printf("resultado=%ld\n", r);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: sin pila explícita; evalúa la expresión.
WITH e(x, y, op) AS (VALUES (3, 4, '+'))
SELECT printf('resultado=%d', CASE op WHEN '+' THEN x + y WHEN '-' THEN x - y ELSE x * y END) AS resultado
FROM e;
```

### PHP · `php main.php`

```php
<?php
[$a, $b, $op] = preg_split('/\s+/', trim(fgets(STDIN)));
$pila = [(int) $a, (int) $b];
$y = array_pop($pila);
$x = array_pop($pila);
$r = $op === "+" ? $x + $y : ($op === "-" ? $x - $y : $x * $y);
echo "resultado=$r\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🧪 Laboratorio: recorrido del código

Sigue `3 4 +` (esperado `resultado=7`) y verás la máquina de pila explícita en unos lenguajes e implícita en otros.

En **Python**, `pila = [int(a), int(b)]` es la pila con los dos operandos ya empujados; una lista donde `append`/`pop` operan por el final. Las dos líneas `y = pila.pop()` y `x = pila.pop()` desapilan en el orden en que la VM lo haría: primero sale el operando de la cima (`y`, el segundo que se empujó), luego `x`. Ese orden importa muchísimo para operaciones no conmutativas: en `10 2 -` el resultado debe ser `10 - 2 = 8`, no `2 - 10`. Al desapilar `y=2` y `x=10` y calcular `x - y`, la implementación respeta la semántica de la RPN. El resultado se apilaría de nuevo en una VM real; aquí se imprime directo.

En **Java**, la máquina de pila es literal: `Deque<Long> pila = new ArrayDeque<>()` y las llamadas `pila.push(...)` / `pila.pop()` son casi el bytecode que la propia JVM ejecutaría para `x + y`. De hecho, si desensamblaras este método con `javap -c`, verías instrucciones `ladd`, `lsub` y `lmul` operando sobre la pila de operandos interna del *frame* —la misma idea que el código modela a mano. Java está, en cierto modo, simulando en objetos lo que su runtime hace en el metal virtual.

En **C**, no hay pila de operandos: `scanf("%ld %ld %c", &x, &y, &op)` lee los tres campos a variables y el ternario calcula directo. C compila a una *máquina de registros real* (la CPU), así que su compilador nunca construyó una pila de operandos de bytecode; asignó `x` e `y` a registros y emitió una instrucción `add`/`sub`/`imul`. El contraste es exacto: la implementación en C revela por qué un lenguaje compilado a máquina no necesita la indirección de la VM de pila, y por qué la JVM sí la usa para ser portable.

## 🔬 Comparación

| Rasgo | Cómo aparece entre los 10 lenguajes |
|---|---|
| Modelo de máquina | Pila de bytecode: Java (JVM), C# (CLR), Python (VM). Registros de CPU: C, Rust, Go tras compilar. |
| Pila explícita en el código | Sí en Python, JS, TS, Java, C#, Rust, PHP (lista/deque); no en C ni Go (variables directas). |
| Orden de desapilado | Todos respetan «la cima es el segundo operando» para que `-` y `/` no se inviertan. |
| Portabilidad del artefacto | `.class`/IL corren en cualquier VM; el binario de C/Rust está atado a la arquitectura. |
| SQL | Sin pila: el motor evalúa la expresión con `CASE`; se marca ilustrativa. |

## 🧬 El concepto en la familia

La JVM y el CLR son las máquinas de pila más conocidas, y CPython comparte el modelo (`dis.dis()` te muestra sus opcodes de pila). Pero no es la única opción: la VM de Lua y la Dalvik de Android son *máquinas de registros*, que emiten menos instrucciones a cambio de instrucciones más grandes. V8, en JavaScript, empieza con un intérprete de bytecode de pila (*Ignition*) y luego compila lo caliente con JIT. Reconocer el patrón «apilar operandos, aplicar operador» te permite leer un volcado de bytecode de casi cualquier lenguaje gestionado y seguir *Crafting Interpreters* cuando construye su propia VM.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 125
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Desapilar en el orden equivocado** → causa: para operaciones no conmutativas (`-`, `/`), invertir los operandos da otro resultado → solución: recordar que el *primero* que sale de la pila es el *segundo* operando; calcular `x - y` con `x` desapilado en segundo lugar.
- **Confundir bytecode con código de máquina** → causa: creer que un `.class` ya son instrucciones de CPU → solución: el bytecode lo ejecuta una VM (o lo recompila su JIT); no lo entiende el procesador directamente.
- **Operar con la pila vacía** → causa: una expresión RPN mal formada deja menos operandos de los que el operador necesita → solución: en una VM real esto es un error de verificación del bytecode; aquí se asume entrada bien formada.

## ❓ Preguntas frecuentes

- **¿Por qué una VM de pila y no de registros?** Porque las instrucciones de pila no nombran operandos (van al tope), son compactas y trivialmente fáciles de generar desde un AST. Es un compromiso de simplicidad y portabilidad sobre densidad.
- **¿La RPN se usa de verdad?** Sí: las calculadoras HP, el lenguaje PostScript, Forth y el bytecode interno de muchas VM se basan en ella.
- **¿Puedo ver el bytecode de un lenguaje?** Sí: `javap -c` (Java), `ildasm` (.NET), `dis.dis()` (Python) o `node --print-bytecode` (V8) te muestran los opcodes reales.

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

> [⏮️ Clase 124](../../parte-8-como-funcionan-los-lenguajes/124-compilador-interprete-y-jit/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 126 ⏭️](../../parte-8-como-funcionan-los-lenguajes/126-aot-vs-jit-costos-y-beneficios/README.md)
