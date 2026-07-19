# Clase 157 — ABI, enlace y convenciones de llamada

> Parte **10 — Interoperabilidad y fronteras entre lenguajes** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

La clase anterior asumió que basta con "declarar la firma correcta" para que la FFI funcione. Bajo esa firma hay un contrato mucho más profundo y silencioso: la **ABI, Application Binary Interface**. Si la API es el acuerdo en el código fuente ("existe una función `doble` que toma un entero"), la ABI es el acuerdo en el **binario**: en qué registro va el primer argumento, cuántos bytes ocupa un `long`, cómo se alinean los campos de una estructura, quién limpia la pila al volver. El objetivo de esta clase es hacer visible ese contrato invisible y entender por qué su desajuste rompe la interoperabilidad de forma que ningún compilador puede advertir.

La ABI es a los binarios lo que un formato de codificación es a los datos. Kleppmann dedica el capítulo 4 de *Designing Data-Intensive Applications* a que emisor y receptor de un mensaje deben acordar la representación de bytes; la ABI es exactamente esa idea aplicada a las llamadas de función dentro de un proceso. Un binario de 32 bits y otro de 64 bits no pueden enlazarse por la misma razón por la que un lector que espera enteros de 4 bytes no puede leer un flujo escrito con enteros de 8: los bits están donde no se los espera. Entender la ABI es entender por qué "compila en mi máquina" no garantiza "enlaza con tu librería".

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. **Explicar** qué es la ABI y qué reglas cubre.
2. **Detectar** una incompatibilidad de ABI (anchura, alineación, convención).
3. **Distinguir** con precisión ABI de API.
4. **Relacionar** la estabilidad de ABI con la compatibilidad binaria de librerías.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | ABI | El contrato binario que hace posible enlazar |
| 2 | Convención de llamada | Registros, pila y quién limpia al volver |
| 3 | API vs. ABI | Contrato fuente frente a contrato binario |

## 📖 Definiciones y características

La **ABI** define cómo se representan los datos y cómo se llaman las funciones a nivel de máquina. Cubre cuatro cosas: el **tamaño y alineación** de cada tipo (¿`long` son 4 u 8 bytes?), la **convención de llamada** (¿los argumentos van en registros o en la pila?, ¿en qué orden?), el **name mangling** (cómo se codifica el nombre de la función en el binario) y el **layout de estructuras** (dónde cae cada campo, con qué relleno). Para que dos binarios se enlacen, deben coincidir en las cuatro. Basta que uno crea que `size_t` son 4 bytes y el otro 8 para que la pila se descuadre y el programa se corrompa.

La **convención de llamada** es la parte más subestimada. En x86-64 System V (Linux, macOS) los primeros seis enteros van en los registros `rdi, rsi, rdx, rcx, r8, r9`; en la ABI de Windows x64 van en `rcx, rdx, r8, r9` y el resto en la pila. Son reglas incompatibles: el mismo código fuente compilado para una y llamado con la otra lee argumentos basura. Por último, **API frente a ABI**: la API es el contrato en código fuente —lo que escribes y el compilador verifica—; la ABI es el contrato binario —lo que queda tras compilar. Puedes mantener la API idéntica y romper la ABI con solo cambiar el orden de dos campos de una estructura: el código que la incluye seguirá compilando, pero los binarios ya compilados contra la versión vieja fallarán.

- **ABI** — Application Binary Interface: representación de datos y protocolo de llamada a nivel binario. Clave: debe coincidir para enlazar.
- **Convención de llamada** — reglas de paso de argumentos, valor de retorno y limpieza de pila. Clave: parte central de la ABI, y varía por plataforma.
- **API vs. ABI** — la API es el contrato en el código fuente; la ABI, en el binario. Clave: son niveles distintos y se rompen por causas distintas.

## 🧩 Situación

Descargas una librería precompilada de 32 bits y tu aplicación es de 64 bits. El enlazador falla con un error críptico, o peor, enlaza y el programa se corrompe en tiempo de ejecución. Sus ABI no coinciden: los punteros miden distinto, los registros son otros, la pila se organiza diferente. No hay nada malo en tu código fuente —la API es perfecta—, el problema vive un nivel más abajo. Este es el drama cotidiano de quien distribuye software nativo: mantener la ABI estable es lo que permite actualizar una `.dll` o una `.so` sin recompilar todo lo que la usa. Para observar la esencia del problema sin montar dos toolchains, esta clase lo reduce a comparar dos "anchos de bits": si coinciden, los binarios son compatibles; si no, no.

## 🧮 Modelo

- **Entrada** (stdin): una línea `a b` (ancho de bits de cada componente)
- **Salida** (stdout): `abi=<compatible|incompatible>`
- **Regla:** compatible si los anchos coinciden

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `64 64` | `abi=compatible` |
| `64 32` | `abi=incompatible` |
| `32 32` | `abi=compatible` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER a, b ; compatible <- (a == b)
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys

a, b = map(int, sys.stdin.readline().split())
print(f"abi={'compatible' if a == b else 'incompatible'}")
```

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const [a, b] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`abi=${a === b ? "compatible" : "incompatible"}`);
```

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const [a, b] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`abi=${a === b ? "compatible" : "incompatible"}`);
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
        int a = Integer.parseInt(p[0]), b = Integer.parseInt(p[1]);
        System.out.println("abi=" + (a == b ? "compatible" : "incompatible"));
    }
}
```

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
int a = int.Parse(p[0]), b = int.Parse(p[1]);
Console.WriteLine($"abi={(a == b ? "compatible" : "incompatible")}");
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
	res := "incompatible"
	if a == b {
		res = "compatible"
	}
	fmt.Printf("abi=%s\n", res)
}
```

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let v: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    let res = if v[0] == v[1] { "compatible" } else { "incompatible" };
    println!("abi={res}");
}
```

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long a, b;
    if (scanf("%ld %ld", &a, &b) != 2) return 1;
    printf("abi=%s\n", a == b ? "compatible" : "incompatible");
    return 0;
}
```

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL compara los anchos.
WITH t(a, b) AS (VALUES (64, 64))
SELECT printf('abi=%s', CASE WHEN a = b THEN 'compatible' ELSE 'incompatible' END) AS resultado FROM t;
```

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
[$a, $b] = array_map('intval', preg_split('/\s+/', trim(fgets(STDIN))));
echo "abi=" . ($a === $b ? "compatible" : "incompatible") . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔎 Recorrido del código (laboratorio)

El caso `64 32` debe producir `abi=incompatible`, y `32 32` debe dar `abi=compatible`. La entrada son dos anchos de bits; la regla es igualdad. El problema es deliberadamente un espejo de la vida real: dos binarios son compatibles si comparten anchura.

En **Python**, `a, b = map(int, sys.stdin.readline().split())` desempaqueta la línea en dos enteros de una sola expresión, y el operador ternario `'compatible' if a == b else 'incompatible'` decide dentro de la `f-string`. Es la forma idiomática pythónica: legible, sin ramas explícitas. Sobre `64 32`, `a == b` es `False` y sale `abi=incompatible`.

En **C**, la comparación es la misma pero el detalle es jugoso porque *esta clase trata precisamente de C*. `long a, b;` declara dos enteros cuyo tamaño **depende de la ABI**: 8 bytes en Linux de 64 bits, 4 en Windows aunque sea de 64. `scanf("%ld %ld", &a, &b)` los lee y el ternario `a == b ? "compatible" : "incompatible"` decide. Que el propio tipo `long` cambie de tamaño según la plataforma es la lección incrustada en el código: el lenguaje que sirve de puente universal es también el que más expone las diferencias de ABI.

En **Rust**, se parsea a `Vec<i64>` con `map(|x| x.parse().unwrap()).collect()` y se compara `v[0] == v[1]`. Rust fija `i64` a 64 bits *en toda plataforma*, a diferencia del `long` de C: esa decisión de diseño elimina una clase entera de bugs de ABI, y es una de las razones por las que Rust resulta cómodo para escribir bindings. Las tres implementaciones imprimen lo mismo, pero solo comparándolas se ve que "un entero" no significa lo mismo en todos los lenguajes: justo el corazón del problema de ABI.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Un `==` entre enteros y un ternario: trivial en todos. |
| Semántica | El tamaño real del entero varía: `long` de C depende de plataforma; `i64` de Rust y `long` de Java son fijos. Ahí nacen los desajustes de ABI. |
| Paradigmática | SQL compara valores con `CASE`, ajeno a cualquier noción de binario o registro. |

Lo que el problema abstrae —comparar dos números— esconde el tema verdadero: **por qué dos números que "son iguales" en el fuente pueden diferir en el binario**. Los lenguajes gestionados (Java, C#, Go) definen tamaños fijos por especificación y compilan a un bytecode o a un binario con ABI conocida, así que rara vez sufren estos choques entre sí. El drama vive en la frontera nativa: C, C++ y Rust producen código máquina directo, y ahí la ABI de la plataforma manda. El name mangling agrava la cosa: C exporta `doble` tal cual, pero C++ codifica el nombre con tipos (`_Z5doblel`), por eso todo binding declara `extern "C"` para desactivar el mangling y recuperar un símbolo estable. La ABI es, en el fondo, el formato de codificación de Kleppmann llevado al plano de la memoria y los registros.

## 🧬 El concepto en la familia

Cada plataforma define su ABI: x86-64 System V rige en Linux y macOS, la ABI de Windows x64 en Windows, y ARM64 tiene la suya (AAPCS). Un binario debe respetar la de su plataforma para enlazar. Los ecosistemas gestionados añaden una capa por encima: la JVM define su propio *bytecode* estable, y .NET su CIL, de modo que Java, Kotlin y Scala comparten ABI de VM aunque el hardware cambie. Esa es la jugada de fondo: subir el punto de encuentro por encima del hardware para que la heterogeneidad de la que habla Tanenbaum deje de doler.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 157
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Mezclar binarios de distinta arquitectura** → causa: enlazar una librería de 32 bits con un ejecutable de 64 → solución: compilar todo el conjunto para la misma ABI y verificarlo (`file`, `objdump`).
- **Confundir API con ABI** → causa: creer que si el código fuente compila, los binarios ya compilados seguirán funcionando → solución: recordar que reordenar un campo o cambiar un tipo mantiene la API y rompe la ABI.
- **Olvidar `extern "C"` al exportar desde C++/Rust** → causa: el name mangling produce un símbolo que el otro lado no encuentra → solución: envolver las funciones exportadas en `extern "C"`.
- **Asumir que `long`/`int` miden lo mismo en todas partes** → causa: `long` son 8 bytes en Linux y 4 en Windows → solución: usar tipos de anchura fija (`int64_t`, `i64`) en la frontera.

## ❓ Preguntas frecuentes

- **¿API o ABI?** La API es el contrato en el código fuente y la verifica el compilador; la ABI es el contrato binario y la verifica el enlazador y el runtime. Un cambio de ABI rompe binarios ya compilados aunque el fuente siga válido.
- **¿Por qué importa la ABI si uso lenguajes gestionados?** Entre lenguajes de la misma VM (Java/Kotlin) casi no la ves, porque la VM la estabiliza. Importa en cuanto tocas la frontera nativa: FFI, plugins compilados, librerías del sistema.
- **¿Qué es una ABI "estable"?** Una que no cambia entre versiones de una librería, de modo que puedes reemplazar la `.so`/`.dll` sin recompilar los programas que la usan. Es un compromiso caro que asumen las librerías del sistema (glibc, la Win32 API).

## 🔗 Referencias

**Libros de la parte:**

- M. Kleppmann — *Designing Data-Intensive Applications* (O'Reilly). Cap. 4: formatos de codificación y compatibilidad hacia atrás/adelante, análogo directo de la estabilidad de ABI.
- S. Newman — *Building Microservices* (2ª ed., O'Reilly). Sobre versionar contratos sin romper a los consumidores.
- A. Tanenbaum y M. van Steen — *Distributed Systems* (3ª ed.). Cap. 4: heterogeneidad de representación de datos entre plataformas.

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

> [⏮️ Clase 156](../../parte-10-interoperabilidad-y-fronteras-entre-lenguajes/156-la-ffi-foreign-function-interface-llamar-a-c-desde-todos/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 158 ⏭️](../../parte-10-interoperabilidad-y-fronteras-entre-lenguajes/158-enlaces-bindings-y-wrappers/README.md)
