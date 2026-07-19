# Clase 162 — WebAssembly como objetivo común

> Parte **10 — Interoperabilidad y fronteras entre lenguajes** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

La clase 156 mostró el punto de encuentro clásico: la ABI de C, donde todos los lenguajes convergen para llamarse entre sí. Pero ese encuentro tiene un precio duro — es específico de cada arquitectura y sistema operativo, y no ofrece ninguna garantía de seguridad: al otro lado de la frontera, un puntero mal calculado corrompe todo el proceso. **WebAssembly** propone un punto de encuentro distinto: no una convención de llamada sobre el hardware real, sino una **máquina virtual abstracta** con su propio formato binario, a la que muchos lenguajes compilan y que se ejecuta en cualquier plataforma dentro de un aislamiento estricto.

El objetivo de esta clase es entender por qué esa segunda respuesta cambia las reglas. Wasm no es "otro formato de ejecutable": es un objetivo de compilación *portable* (el mismo binario corre en x86, ARM, navegador y servidor), *rápido* (cercano al nativo, con validación previa y compilación JIT o AOT) y *aislado por diseño* (un módulo no puede tocar nada que el anfitrión no le entregue explícitamente). Eso lo convierte en la primera frontera políglota donde ejecutar código ajeno no es un acto de fe.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. **Explicar** qué es WebAssembly y qué garantiza su modelo de ejecución.
2. **Reconocer** qué lenguajes compilan a Wasm y con qué facilidad.
3. **Ver** Wasm como objetivo común y compararlo con la ABI de C.
4. **Identificar** el coste real de la frontera: el paso de datos entre el anfitrión y el módulo.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | WebAssembly | Binario portable y rápido |
| 2 | Objetivo de compilación | Muchos lenguajes compilan a Wasm |
| 3 | Runtime | Navegador o fuera de él (WASI) |

## 📖 Definiciones y características

**WebAssembly** es el formato binario de una máquina virtual de pila con un conjunto de instrucciones deliberadamente pequeño: enteros y flotantes de 32 y 64 bits, aritmética, control estructurado (bloques, bucles, condicionales — no saltos arbitrarios) y acceso a una memoria lineal. Esa pobreza es intencionada. Al no tener saltos libres, el código puede **validarse completo antes de ejecutarse**: el runtime demuestra estáticamente que el módulo respeta los tipos y no salta fuera de su código. Un binario nativo no admite esa verificación; un módulo Wasm sí, y es lo que permite ejecutar código no confiable sin un proceso ni una máquina virtual completa alrededor.

La segunda pieza es la **memoria lineal**: un módulo ve un único array de bytes que crece en páginas de 64 KB, y todo puntero suyo es un desplazamiento dentro de él. Un acceso fuera de rango no toca la memoria del anfitrión — falla como una trampa controlada. De ahí el modelo de seguridad: un módulo **no puede hacer nada que el anfitrión no le haya pasado**. No hay llamadas al sistema implícitas, no hay sistema de archivos, no hay red. Solo las funciones que el anfitrión importa explícitamente en el módulo. Es una capacidad negativa muy potente: por defecto, un módulo Wasm es inofensivo.

**WASI** (WebAssembly System Interface) es la respuesta a lo que falta cuando Wasm sale del navegador. Define de forma estandarizada esas funciones importadas —abrir archivos, leer el reloj, abrir sockets— siguiendo un modelo de **capacidades**: el módulo no pide "abre `/etc/passwd`", recibe del anfitrión un descriptor de un directorio concreto y solo puede moverse dentro de él. Comparado con un proceso Unix, que hereda todos los permisos del usuario, la diferencia de superficie de ataque es enorme, y es lo que hace de Wasm una unidad de despliegue atractiva para *plugins*, funciones sin servidor y extensiones de terceros.

El punto que más sorprende al usarlo es la **frontera de datos**. Las funciones Wasm solo intercambian números: `i32`, `i64`, `f32`, `f64`. No hay tipo cadena, ni lista, ni objeto. Pasar un texto de JavaScript a un módulo Rust significa reservar espacio en la memoria lineal del módulo, copiar los bytes, pasar el desplazamiento y la longitud como dos enteros, y que el otro lado los reconstruya. Es el mismo problema de *marshalling* de la FFI clásica, solo que con un aislamiento que lo hace seguro. Herramientas como `wasm-bindgen` lo automatizan, pero la copia sigue ahí — y por eso Wasm compensa en cargas de cómputo intenso y pierde en llamadas triviales y frecuentes.

- **WebAssembly** — formato binario portable, validable y eficiente, objetivo de compilación de varios lenguajes. Clave: se verifica antes de ejecutarse y corre aislado.
- **Objetivo (target)** — el formato al que compila un lenguaje. Clave: Rust, C/C++, Go y C# pueden apuntar a Wasm sin cambiar el código fuente.
- **WASI** — interfaz de sistema para Wasm fuera del navegador, basada en capacidades. Clave: el módulo solo accede a lo que el anfitrión le concede.

## 🧩 Situación

Un motor de cálculo escrito en Rust —caro de reescribir y demasiado lento en JavaScript— se compila a Wasm y se carga desde la página junto al código JS, que le pasa los datos y recibe el resultado. El mismo `.wasm`, sin recompilar, corre en un runtime del servidor como Wasmtime para el procesamiento por lotes. Y una plataforma que acepta *plugins* de terceros los ejecuta como módulos Wasm precisamente porque un plugin malicioso no puede leer el disco ni abrir conexiones si el anfitrión no se lo concede. Para aislar la idea de "función exportada por un módulo que el anfitrión invoca con números y de la que recibe un número", esta clase calcula el cuadrado de un entero: una función con un `i64` de entrada y un `i64` de salida, la forma exacta que cruza la frontera Wasm sin ningún *marshalling*.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n`
- **Salida** (stdout): `resultado=<n²>`
- **Regla:** calcular n al cuadrado (como en un módulo Wasm)

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `resultado=25` |
| `0` | `resultado=0` |
| `7` | `resultado=49` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER n ; ESCRIBIR n*n
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys

n = int(sys.stdin.readline())
print(f"resultado={n * n}")
```

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`resultado=${n * n}`);
```

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`resultado=${n * n}`);
```

### Java · [`java/Main.java`](implementaciones/java/Main.java) · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        long n = Long.parseLong(br.readLine().trim());
        System.out.println("resultado=" + (n * n));
    }
}
```

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;

long n = long.Parse(Console.In.ReadToEnd().Trim());
Console.WriteLine($"resultado={n * n}");
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
	n, _ := strconv.ParseInt(strings.TrimSpace(line), 10, 64)
	fmt.Printf("resultado=%d\n", n*n)
}
```

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    println!("resultado={}", n * n);
}
```

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    printf("resultado=%ld\n", n * n);
    return 0;
}
```

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL calcula el cuadrado.
WITH nums(n) AS (VALUES (5), (0), (7))
SELECT printf('resultado=%d', n * n) AS resultado FROM nums;
```

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
$n = (int) trim(fgets(STDIN));
echo "resultado=" . ($n * $n) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔎 Recorrido del código (laboratorio)

El caso `5` debe producir `resultado=25`. La operación es trivial a propósito: lo interesante no es el cuadrado, sino que esta función tiene exactamente la forma que Wasm sabe exportar sin ayuda —un entero entra, un entero sale— y que cada lenguaje llega a ella por un camino distinto.

En **Rust**, `let n: i64 = s.trim().parse().unwrap();` y `n * n` es el caso ideal: `cargo build --target wasm32-unknown-unknown` compila este mismo código a un módulo, sin runtime que embarcar y sin recolector de basura. Por eso Rust es el lenguaje con mejor relación tamaño/rendimiento sobre Wasm: lo que hay en el `.wasm` es el código y poco más. Fíjate en el `i64`: coincide con uno de los cuatro tipos numéricos que Wasm entiende de forma nativa, así que atraviesa la frontera sin conversión alguna.

En **C**, `scanf("%ld", &n)` y `printf(...)` no son código puro de cálculo: son llamadas al sistema. Compilado con Emscripten o `clang --target=wasm32-wasi`, ese `scanf` no puede ejecutarse solo — necesita que el anfitrión importe una función de lectura, que es precisamente lo que WASI estandariza. Aquí se ve dónde está la frontera real de Wasm: `n * n` es puro y portable, la E/S es la parte que exige negociar capacidades con el exterior.

En **JavaScript**, `parseInt(...)` y `n * n` recuerdan por qué Wasm existe: el `number` de JS es un flotante de doble precisión, con solo 53 bits de mantisa. Para `5` da igual, pero con enteros grandes el resultado empieza a perder precisión en silencio, mientras que el `i64` de Rust o el `long` de C son exactos. Cuando el anfitrión es JavaScript y el módulo trabaja con `i64`, la frontera obliga a usar `BigInt` — un caso concreto y muy real de incompatibilidad de tipos entre los dos lados.

En **SQL**, el cuadrado se calcula dentro del motor y el contraste es el esperado. Pero conviene saber que la separación se está difuminando: SQLite compilado a Wasm corre hoy dentro del navegador, y varios motores permiten cargar extensiones como módulos Wasm en lugar de bibliotecas nativas, justamente para no ceder el proceso entero a código de terceros.

## 🔬 Comparación

| Lenguaje | Situación respecto a WebAssembly |
|---|---|
| Rust | El mejor soportado: `wasm32-unknown-unknown` y `wasm32-wasip1` de serie, `wasm-bindgen` para el puente con JS, binarios pequeños. |
| C | Emscripten (con emulación de POSIX) o `clang --target=wasm32-wasi`; fue el caso de uso original de Wasm. |
| C# | Blazor WebAssembly ejecuta .NET en el navegador; con AOT compila a Wasm, si no interpreta IL sobre un runtime en Wasm. |
| Go | `GOOS=js GOARCH=wasm` y `GOOS=wasip1`; funciona bien, pero el runtime y el GC engordan el binario. |
| TypeScript | No compila a Wasm; AssemblyScript es un subconjunto parecido a TS que sí lo hace. |
| JavaScript | Es el **anfitrión**, no el invitado: carga módulos con `WebAssembly.instantiate` y les pasa datos. |
| Python | No compila a Wasm; se *porta el intérprete* (Pyodide, CPython sobre WASI) y se ejecuta Python dentro del módulo. |
| Java | Proyectos experimentales (TeaVM, CheerpJ); la JVM ya era su propia máquina virtual portable. |
| PHP | Existe un port del intérprete a Wasm; es un caso de nicho, no una práctica habitual. |
| SQL | No es un lenguaje compilable: lo que se lleva a Wasm es el motor, como SQLite Wasm en el navegador. |

El patrón que revela la tabla es la división en dos grupos. Los lenguajes **compilados y sin recolector de basura** —Rust, C, C++, Zig— compilan a Wasm de forma natural y producen módulos pequeños: su modelo de memoria encaja directamente con la memoria lineal. Los lenguajes **con runtime propio** —Python, Java, PHP, y .NET en modo interpretado— no compilan *a* Wasm; lo que se compila es su intérprete, y el módulo resultante pesa megabytes porque lleva la máquina virtual dentro. Es la diferencia entre traducir un texto y enviar al traductor con él. La comparación con la clase 156 cierra el argumento: la ABI de C da rendimiento máximo y cero aislamiento, y depende de la plataforma; Wasm cuesta algo de rendimiento y una copia en la frontera, pero da portabilidad real y aislamiento verificable. Cuál conviene depende de si el código del otro lado es tuyo o de un desconocido.

## 🧬 El concepto en la familia

La idea del **objetivo intermedio común** es vieja y recurrente: el bytecode de la JVM permitió que Kotlin, Scala y Clojure compartieran ecosistema; el CIL de .NET hizo lo mismo con C#, F# y VB; LLVM IR es el objetivo intermedio de Rust, Swift, Clang y decenas más. Wasm se distingue en tres puntos. No está atado a un proveedor —es un estándar del W3C con múltiples implementaciones independientes—. Está diseñado desde el principio para **ejecutar código no confiable**, cosa que ni la JVM ni LLVM se plantearon. Y es deliberadamente **agnóstico de lenguaje**: no asume recolector de basura, ni modelo de objetos, ni excepciones. El precio de esa neutralidad es que las estructuras ricas no cruzan solas la frontera, y por eso el trabajo actual del estándar —el *Component Model* y WIT, junto a propuestas como GC y *reference types*— apunta justo ahí: describir interfaces con cadenas, listas y registros para que dos módulos de lenguajes distintos se entiendan sin escribir el *marshalling* a mano. Es, literalmente, el problema de esta parte del curso resuelto una capa más abajo.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 162
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Esperar acceso directo al sistema desde un módulo** → causa: Wasm no tiene llamadas al sistema; solo puede usar lo que el anfitrión importe → solución: pasar las capacidades explícitamente, o usar WASI fuera del navegador.
- **Cruzar la frontera en un bucle caliente** → causa: cada llamada anfitrión↔módulo tiene coste, y pasar cadenas o arrays implica copiar en la memoria lineal → solución: mover lotes grandes de datos y hacer el trabajo dentro del módulo, no ida y vuelta por elemento.
- **Llevar un lenguaje con runtime propio sin medir el tamaño** → causa: compilar Python o Go a Wasm arrastra intérprete y GC, y el módulo pesa megabytes → solución: para el navegador, elegir un lenguaje sin GC (Rust, C) o aceptar y presupuestar la descarga.
- **Suponer que Wasm es siempre más rápido que JavaScript** → causa: los motores JS optimizan muy bien el código monomórfico, y la frontera añade coste → solución: medir; Wasm gana en cómputo numérico sostenido, no en lógica ligera con muchas llamadas.
- **Creer que el aislamiento cubre la lógica** → causa: el sandbox impide salir de la memoria, pero no que un módulo agote CPU o memoria en un bucle infinito → solución: imponer límites de combustible, de memoria y de tiempo en el runtime del anfitrión.
- **Pasar enteros de 64 bits a JavaScript sin más** → causa: el `number` de JS solo garantiza 53 bits de precisión → solución: usar `BigInt` en la frontera o dividir el valor en dos `i32`.

## ❓ Preguntas frecuentes

- **¿Wasm reemplaza a JavaScript?** No. Wasm no accede al DOM ni a las APIs del navegador por sí mismo; necesita a JavaScript como anfitrión. Lo complementa donde JS es débil: cómputo numérico sostenido, código portado de C/C++ y bibliotecas que ya existían en otro lenguaje.
- **¿Wasm solo en el navegador?** No, y el lado servidor es hoy su crecimiento más interesante: con WASI sirve para *plugins*, funciones sin servidor con arranque en milisegundos y extensiones de bases de datos o *proxies* (Envoy usa filtros Wasm).
- **¿Por qué Wasm y no la ABI de C, si ya funcionaba?** Porque la ABI de C no es portable entre plataformas y no ofrece aislamiento. Wasm da un único binario para todas las arquitecturas y ejecuta código ajeno sin poner en riesgo el proceso anfitrión. Se paga en rendimiento y en copias.
- **¿Necesito saber Wasm para usarlo?** Casi nunca. Es un objetivo de compilación: escribes Rust o C y una bandera del compilador produce el `.wasm`. Conocer su modelo importa cuando hay que depurar el rendimiento de la frontera o recortar el tamaño.
- **¿Qué tipos pueden cruzar la frontera?** De forma nativa, solo números (`i32`, `i64`, `f32`, `f64`). Todo lo demás —cadenas, structs, listas— se codifica como bytes en la memoria lineal y se pasa como puntero y longitud. Es lo que el *Component Model* pretende estandarizar.

## 🔗 Referencias

**Libros de la parte:**

- M. Kleppmann — *Designing Data-Intensive Applications* (O'Reilly). Cap. 4: por qué un formato común e independiente del lenguaje es la clave de la interoperabilidad.
- S. Newman — *Building Microservices* (2ª ed., O'Reilly). Wasm como unidad de despliegue aislada y como vía para *plugins* de terceros.
- A. Tanenbaum y M. van Steen — *Distributed Systems* (3ª ed.). Virtualización, código móvil y ejecución de código no confiable.

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

> [⏮️ Clase 161](../../parte-10-interoperabilidad-y-fronteras-entre-lenguajes/161-procesos-y-comunicacion-stdin-stdout-sockets-colas/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 163 ⏭️](../../parte-10-interoperabilidad-y-fronteras-entre-lenguajes/163-incrustar-un-lenguaje-en-otro-lua-python-embebido/README.md)
