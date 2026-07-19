# Clase 137 — Errores: de sintaxis, de tipos, de enlace y de ejecución

> Parte **8 — Cómo funcionan los lenguajes** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Un error no es solo un mensaje: es una **coordenada en el pipeline** que la clase 123 recorrió. Cada clase de error nace en una fase concreta —el lexer, el parser, el análisis semántico, el enlazador, el runtime— y saber en cuál nació determina dónde buscar, qué herramienta usar y, a menudo, si el problema es tuyo o del entorno. Esta clase organiza ese mapa con un programa que traduce un código numérico al nombre de la clase de error, y lo usa como excusa para responder la pregunta que de verdad importa: **cuánto tarda cada lenguaje en decirte que algo está mal**. Ese retraso no es un detalle de comodidad: es una de las decisiones de diseño más consecuentes que un lenguaje toma. Un error de tipos que Rust rechaza en compilación es el mismo error que Python descubre a las tres de la mañana en producción, en una rama poco frecuente. El *porqué* de estudiarlo es que Aho, Lam, Sethi y Ullman estructuran el «Dragon Book» exactamente sobre estas fases, y que leer un mensaje de error con criterio —saber que un `undefined reference` no lo produce el compilador sino el enlazador, y por tanto no se arregla tocando el código— es una de las habilidades que más tiempo ahorran a lo largo de una carrera.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Situar cada clase de error en la fase del pipeline que la detecta.
2. Explicar por qué un lenguaje dinámico solo puede detectar errores de tipo al ejecutar la línea que falla.
3. Diagnosticar un error de enlace distinguiendo el enlazado estático del dinámico.
4. Distinguir un error de ejecución **recuperable** de uno **irrecuperable**, y qué hace cada lenguaje con ellos.
5. Reconocer la categoría más peligrosa: el error **silencioso**, que no produce mensaje alguno.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Léxico y sintáctico | El código no llega a ser un programa: el parser se detiene |
| 2 | Semántico y de tipos | La forma es válida pero la operación no tiene sentido |
| 3 | De enlace | El símbolo no existe: ni el compilador ni el runtime, sino el enlazador |
| 4 | De ejecución | Solo el dato real revela el fallo: índice, división, nulo |
| 5 | Silenciosos | Los que no fallan: desbordamiento, conversión implícita, comparación laxa |

## 📖 Definiciones y características

Un **error léxico** ocurre cuando un carácter no puede formar parte de ningún token válido: una comilla sin cerrar, un `@` fuera de lugar. El *scanner* se detiene ahí. Un **error de sintaxis** es un paso más adelante: los tokens son legítimos pero su orden no encaja en la gramática —un paréntesis sin cerrar, un `if` sin condición—. Un detalle importante para leer estos mensajes: el parser señala el punto donde *descubrió* la inconsistencia, que casi nunca es donde tú la introdujiste. Un `{` sin cerrar en la línea 40 se reporta al final del archivo, porque hasta ahí todo era gramaticalmente posible. Por eso los compiladores modernos invierten tanto esfuerzo en **recuperación de errores**: intentan resincronizar tras el primer fallo para reportar varios de una pasada, en lugar de rendirse.

Un **error semántico o de tipos** aparece cuando la forma es válida pero el significado no: sumar una cadena y una lista, llamar a un método inexistente, pasar tres argumentos a una función de dos. Aquí está la divisoria más importante entre lenguajes. En un lenguaje **estáticamente tipado** —Java, C#, Go, Rust, C, TypeScript—, un comprobador de tipos recorre el AST antes de generar código y rechaza el programa entero: el error se detecta **sin ejecutar**, cubriendo todas las rutas, incluidas las que ninguna prueba visita. En un lenguaje **dinámicamente tipado** —Python, JavaScript, PHP—, los tipos viven en los valores y no en las expresiones, así que el error solo puede aparecer cuando la línea concreta se ejecuta con los datos concretos. La consecuencia práctica es asimétrica: un fallo de tipos en una rama de manejo de errores poco frecuente puede sobrevivir meses en producción en Python y es imposible en Rust.

El **error de enlace** es el que más confusión genera porque no lo produce ni el compilador ni el programa: lo produce el **enlazador**, una herramienta distinta que se ejecuta entre ambos. Bryant & O'Hallaron le dedican un capítulo entero en *CS:APP*, y con razón. El compilador de C traduce cada `.c` a un `.o` que contiene código máquina más una tabla de símbolos: los que define y los que **necesita pero no tiene**. El enlazador junta todos los `.o` y las bibliotecas, resuelve cada símbolo pendiente y produce el ejecutable. Si nadie define `sqrt`, el resultado es el clásico `undefined reference to 'sqrt'` —que no se arregla tocando el código sino añadiendo `-lm`—. Y hay una segunda variante, más traicionera: el **enlace dinámico**, que resuelve símbolos al **cargar** el programa. Ahí el fallo llega en el arranque (`error while loading shared libraries`) o incluso más tarde con `dlopen`. Todo el ecosistema de la JVM y de .NET tiene su equivalente: `NoClassDefFoundError` y `MethodNotFoundException` son errores de enlace tardío, y el «infierno de dependencias» de casi cualquier gestor de paquetes es este mismo problema con otro nombre.

El **error de ejecución** solo se manifiesta con datos reales: división por cero, índice fuera de rango, desreferencia de nulo, memoria agotada, fichero inexistente. Ningún análisis estático razonable puede descartarlos todos —el problema es indecidible en general— pero los lenguajes difieren muchísimo en **cuáles** consiguen eliminar por diseño. Rust elimina la desreferencia de nulo obligando a usar `Option<T>`; Kotlin y Swift, con tipos anulables explícitos; Go y Java, no. Y hay una segunda distinción crucial: la de errores **recuperables** frente a **irrecuperables**. Un fichero que no existe es una condición esperada del dominio y se modela como valor de retorno (`Result` en Rust, `error` en Go) o excepción capturable; un índice fuera de rango es un bug del programador y provoca un pánico o un aborto. Confundir ambas categorías —capturar todo indiscriminadamente— convierte bugs en comportamientos silenciosamente incorrectos.

Y queda la categoría más peligrosa, la que ningún nombre de la lista cubre: el **error silencioso**. El desbordamiento de un entero en C, que es comportamiento indefinido y no avisa; la conversión implícita de `"10" + 5` en JavaScript, que da `"105"`; una comparación laxa con `==` en PHP; una división entera donde esperabas decimales. Nada falla, y el resultado es incorrecto. Estos errores no aparecen en ninguna fase porque el lenguaje los considera legales, y son la razón por la que existen los avisos del compilador (`-Wall -Wextra`), los sanitizadores y los linters. Cuanto más permisivo es un lenguaje al convertir tipos, más de estos errores acumula.

## 🧩 Situación

Un despliegue falla y el mensaje es `undefined symbol: PyInit__ssl`. Sin el mapa de fases, la reacción típica es revisar el código de la aplicación, que no tiene nada que ver. Con el mapa, el diagnóstico es inmediato: la palabra «symbol» sitúa el fallo en el **enlazador dinámico**, en el momento de cargar una biblioteca compartida, así que el problema está en el entorno —una versión de OpenSSL que no coincide con la que se usó al compilar—, no en una línea de Python. Cinco minutos en lugar de dos horas. Ese es el valor concreto de saber qué fase produce cada mensaje, y por eso la traducción de código a categoría de error que implementa esta clase es, en el fondo, un ejercicio de clasificación diagnóstica.

## 🧮 Modelo

- **Entrada** (stdin): un entero `codigo` (1 a 4)
- **Salida** (stdout): `error=<sintaxis|tipos|enlace|ejecucion>`
- **Regla:** 1→sintaxis, 2→tipos, 3→enlace, 4→ejecucion

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `1` | `error=sintaxis` |
| `3` | `error=enlace` |
| `4` | `error=ejecucion` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER codigo ; SEGUN codigo: 1..4 -> nombre del error
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys

codigo = int(sys.stdin.readline())
nombres = {1: "sintaxis", 2: "tipos", 3: "enlace", 4: "ejecucion"}
print(f"error={nombres.get(codigo, 'desconocido')}")
```

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const codigo = parseInt(readFileSync(0, "utf8").trim(), 10);
const nombres = { 1: "sintaxis", 2: "tipos", 3: "enlace", 4: "ejecucion" };
console.log(`error=${nombres[codigo] ?? "desconocido"}`);
```

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const codigo: number = parseInt(readFileSync(0, "utf8").trim(), 10);
const nombres: Record<number, string> = { 1: "sintaxis", 2: "tipos", 3: "enlace", 4: "ejecucion" };
console.log(`error=${nombres[codigo] ?? "desconocido"}`);
```

### Java · [`java/Main.java`](implementaciones/java/Main.java) · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int codigo = Integer.parseInt(br.readLine().trim());
        String e;
        switch (codigo) {
            case 1: e = "sintaxis"; break;
            case 2: e = "tipos"; break;
            case 3: e = "enlace"; break;
            case 4: e = "ejecucion"; break;
            default: e = "desconocido";
        }
        System.out.println("error=" + e);
    }
}
```

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;

int codigo = int.Parse(Console.In.ReadToEnd().Trim());
string e = codigo switch {
    1 => "sintaxis",
    2 => "tipos",
    3 => "enlace",
    4 => "ejecucion",
    _ => "desconocido",
};
Console.WriteLine($"error={e}");
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
	codigo, _ := strconv.Atoi(strings.TrimSpace(line))
	var e string
	switch codigo {
	case 1:
		e = "sintaxis"
	case 2:
		e = "tipos"
	case 3:
		e = "enlace"
	case 4:
		e = "ejecucion"
	default:
		e = "desconocido"
	}
	fmt.Printf("error=%s\n", e)
}
```

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let codigo: i64 = s.trim().parse().unwrap();
    let e = match codigo {
        1 => "sintaxis",
        2 => "tipos",
        3 => "enlace",
        4 => "ejecucion",
        _ => "desconocido",
    };
    println!("error={e}");
}
```

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    int codigo;
    if (scanf("%d", &codigo) != 1) return 1;
    const char *e;
    switch (codigo) {
        case 1: e = "sintaxis"; break;
        case 2: e = "tipos"; break;
        case 3: e = "enlace"; break;
        case 4: e = "ejecucion"; break;
        default: e = "desconocido";
    }
    printf("error=%s\n", e);
    return 0;
}
```

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL: selección por código con CASE.
WITH c(codigo) AS (VALUES (1))
SELECT printf('error=%s', CASE codigo WHEN 1 THEN 'sintaxis' WHEN 2 THEN 'tipos' WHEN 3 THEN 'enlace' WHEN 4 THEN 'ejecucion' ELSE 'desconocido' END) AS resultado
FROM c;
```

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
$codigo = (int) trim(fgets(STDIN));
$nombres = [1 => "sintaxis", 2 => "tipos", 3 => "enlace", 4 => "ejecucion"];
echo "error=" . ($nombres[$codigo] ?? "desconocido") . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🧪 Laboratorio: recorrido del código

El programa es una tabla de códigos a nombres, y precisamente por su trivialidad sirve para ver qué error cometería cada lenguaje si te equivocaras, y **cuándo** te lo diría.

En **Python**, `nombres.get(codigo, 'desconocido')` maneja el código desconocido con un valor por defecto. Si en su lugar se hubiera escrito `nombres[codigo]`, un código `7` provocaría un `KeyError` en ejecución —clase 4—. Y si `codigo` fuera una cadena en lugar de un entero, el diccionario no encontraría la clave y devolvería `'desconocido'` **silenciosamente**, porque `1` y `"1"` son claves distintas: un error de la quinta categoría, el que no avisa. Nada de esto se detecta antes de ejecutar, porque en Python el tipo vive en el valor.

En **TypeScript**, el tipo `Record<number, string>` es la declaración explícita que permite al compilador comprobar los accesos antes de ejecutar. Aquí aparece un matiz importante y muy propio de TypeScript: sus tipos son **erasables**, se comprueban al compilar y desaparecen del JavaScript generado. Con `noUncheckedIndexedAccess` activado, el compilador obligaría a tratar el resultado como posiblemente `undefined` —convirtiendo en error de tipos lo que sin esa opción sería un error de ejecución o, peor, un `undefined` propagado en silencio—. Es un ejemplo limpio de cómo la configuración del comprobador mueve errores de una fase a otra.

En **Java**, el `switch` con `String e;` y un `default` obligatorio ilustra el análisis semántico del compilador: `javac` verifica la **asignación definitiva** —que `e` tenga valor en todas las rutas antes de usarse— y rechaza el programa si falta el `default`. No es un error de sintaxis (la gramática está bien) sino semántico, detectado sin ejecutar nada. En **C#**, la expresión `switch` moderna va más lejos y avisa si el conjunto de casos no es exhaustivo.

En **C**, el `switch` con `char *e` y `break` en cada rama esconde la trampa clásica del lenguaje: omitir un `break` no es un error de ninguna clase —es sintaxis válida y semántica intencionada, el *fallthrough*— y produce un resultado incorrecto en silencio. Solo `-Wimplicit-fallthrough` lo convierte en aviso. Ese es exactamente el patrón que motivó que Go exija `fallthrough` explícito y que Rust use `match` exhaustivo.

En **Rust**, el `match` sobre el código se comprueba por **exhaustividad**: si faltara un brazo que cubra los valores restantes, el compilador rechaza el programa. Es la traslación más agresiva de la escala: un error que en C es silencioso y en Java es semántico, en Rust es imposible de escribir. En **Go**, el idioma sería un `switch` con `default`, y el compilador añadiría su propia peculiaridad —variables o importaciones no usadas son **errores**, no avisos—, una decisión deliberada para que la basura no se acumule. En **PHP**, `$nombres[$codigo] ?? "desconocido"` usa el operador de coalescencia nula precisamente para evitar el aviso de índice indefinido, que históricamente era un *warning* que muchos ignoraban. En **SQL**, el `CASE ... ELSE` cubre el caso restante; sin `ELSE`, el resultado sería `NULL` —otro error silencioso, y de los que más quebraderos dan en informes—.

## 🔬 Comparación

| Rasgo | Cómo se manifiesta entre los 10 lenguajes |
|---|---|
| Errores de tipo | En compilación (Java, C#, Go, Rust, C, TypeScript); en ejecución, al alcanzar la línea (Python, JavaScript, PHP); al preparar la consulta (SQL). |
| Rigor del comprobador | Muy alto: exhaustividad, propiedad, *lifetimes* (Rust); alto (Java, C#, Go); permisivo con conversiones (C); configurable (TypeScript, según `strict`). |
| Error de enlace | Enlazador estático y dinámico (C, Rust, Go con cgo); carga de clases (`NoClassDefFoundError` en Java, ensamblados en C#); resolución de módulos en ejecución (Python `ImportError`, JS `ERR_MODULE_NOT_FOUND`). |
| Fallo por nulo | Imposible en el subconjunto seguro (Rust, con `Option<T>`); `NullPointerException` frecuente (Java, C#); `nil pointer dereference` (Go); `undefined is not a function` (JS); segfault (C). |
| Errores recuperables | `Result<T, E>` como valor (Rust); `error` como segundo retorno (Go); excepciones comprobadas y no comprobadas (Java); excepciones (Python, C#, PHP, JS); código de retorno y `errno` (C). |
| Irrecuperables | `panic!` (Rust), `panic` (Go), `Error` de la JVM, abortos y comportamiento indefinido (C). |
| Errores silenciosos frecuentes | Desbordamiento entero y conversiones implícitas (C); coerción de tipos con `+` y `==` (JS, PHP); división entera (varios); `NULL` propagado (SQL). |

## 🧬 El concepto en la familia

La familia C compila a código máquina y pasa por un enlazador real, así que exhibe las cuatro fases en su forma más pura y separable: `cc -c` produce objetos, `ld` los une, y cada uno falla con su propio vocabulario. Las familias JVM y .NET desplazan el enlace a la carga: el compilador solo verifica que las firmas existan en el *classpath* de compilación, y la resolución real ocurre al arrancar, lo que hace posible el clásico caso de compilar contra una versión de una biblioteca y ejecutar contra otra —el error llega en producción y no en la compilación—. La familia de scripting dinámico concentra casi todo en ejecución: importar un módulo, resolver un método y comprobar un tipo son operaciones que ocurren mientras el programa corre, con la flexibilidad enorme que eso da y el coste de que solo lo ejecutado esté verificado; de ahí que la respuesta cultural de esas comunidades hayan sido las suites de pruebas exhaustivas y, más recientemente, los comprobadores de tipos graduales (`mypy`, `TypeScript`, tipos en PHP 8). La familia funcional tipada —Haskell, OCaml, F#— lleva al extremo la idea contraria: cuanto más expresivo el sistema de tipos, más errores dejan de existir como categoría de ejecución, hasta el punto del lema «si compila, funciona», que es una exageración útil. Rust ocupa la posición más ambiciosa del espectro para un lenguaje de sistemas, moviendo a compilación no solo los tipos sino también la gestión de memoria y la seguridad entre hilos. Y SQL es un caso aparte que conviene recordar: sus errores se dividen entre la preparación de la sentencia (sintaxis, columnas inexistentes) y la ejecución (violaciones de restricciones, interbloqueos), con `NULL` como fuente inagotable de resultados incorrectos que nunca producen un mensaje.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 137
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Buscar el error de sintaxis donde el compilador lo señala** → causa: el parser reporta dónde *descubrió* la inconsistencia, no dónde la introdujiste → solución: ante un error al final del archivo, buscar hacia atrás la llave, el paréntesis o la comilla sin cerrar. Un formateador automático (`gofmt`, `prettier`, `rustfmt`) suele localizarlo de inmediato porque la indentación se descuadra.
- **Perseguir un `undefined reference` en el código fuente** → causa: es un error del **enlazador**, no del compilador: el símbolo se declaró pero nadie lo define → solución: comprobar que la biblioteca está enlazada (`-lm`, `-lpthread`), que el orden de los `-l` es correcto en GCC, y que la arquitectura coincide.
- **Corregir solo el primer error del compilador y recompilar** → causa: los errores en cascada tras el primero suelen ser artefactos de la recuperación del parser → solución: al revés de lo que parece, corregir el **primero** y recompilar es lo correcto; lo que no lo es es intentar corregir los cincuenta a la vez, porque cuarenta y ocho desaparecerán solos.
- **Capturar excepciones genéricas** → causa: `except Exception`, `catch (Exception e)` o `catch {}` engullen tanto los errores esperados del dominio como los bugs del programador → solución: capturar tipos concretos y dejar propagar lo inesperado. Un `catch` vacío convierte un fallo ruidoso en un fallo silencioso, que siempre es peor.
- **Ignorar los avisos del compilador** → causa: tratarlos como ruido → solución: los avisos son la única defensa contra la categoría silenciosa. Activar `-Wall -Wextra` en C, `strict` en TypeScript, `-Xlint` en Java, y tratar los avisos como errores en CI.
- **Ignorar el valor de retorno de error** → causa: en Go, `resultado, _ := funcion()` descarta el error; en C, no comprobar el retorno de `malloc` o `scanf` → solución: manejar el error o propagarlo explícitamente. El `_` de Go debe ser una decisión consciente y rara, no un reflejo.
- **Confundir el error con su causa raíz** → causa: `NullPointerException` en la línea 200 cuando el nulo se produjo en la 40 → solución: leer la traza completa desde el fondo (la excepción original, no la envuelta) y buscar el punto donde el valor se creó, no donde se usó.

## ❓ Preguntas frecuentes

- **¿Cuándo salen los errores de tipos?** En los lenguajes estáticos, antes de ejecutar y para **todas** las rutas del programa, incluidas las que ninguna prueba cubre. En los dinámicos, cuando esa línea concreta se ejecuta con esos datos concretos; una rama de manejo de errores que se alcanza una vez al mes puede llevar un error de tipos meses en producción.
- **¿Qué es exactamente un error de enlace?** El enlazador junta los objetos y las bibliotecas y resuelve cada símbolo que un módulo usa pero no define. Si nadie lo define, falla. En el enlace **estático** eso ocurre al construir el ejecutable; en el **dinámico**, al cargarlo o incluso más tarde. Los `NoClassDefFoundError` de Java y los conflictos de versiones de cualquier gestor de paquetes son la misma clase de problema, con la resolución diferida.
- **¿Es mejor un lenguaje que detecta más errores en compilación?** Detecta más errores *de esas categorías*, y ese es un beneficio real y medible. Pero no es gratis: exige más anotaciones, compila más lento y rechaza programas correctos que el comprobador no logra demostrar seguros. El equilibrio depende del sistema: para un script de una tarde, la comprobación estática estorba; para un sistema de pagos con diez años de vida, es una inversión evidente.
- **¿Y los errores lógicos?** Son la quinta categoría y ninguna fase los detecta: el programa hace exactamente lo que escribiste y lo que escribiste está mal. Ninguna herramienta puede saber que querías `<` donde pusiste `<=`. Contra esto solo hay pruebas, revisión y tipos que hagan imposible el estado inválido —modelar un identificador de usuario como `UserId` y no como `String`, por ejemplo—.
- **¿Por qué distinguir errores recuperables de irrecuperables?** Porque llaman a respuestas opuestas. Un fichero ausente es una condición esperable del mundo: se modela como valor (`Result`, `error`) y se maneja. Un índice fuera de rango es un bug: la respuesta correcta es fallar ruidosamente y arreglar el código, no capturarlo y continuar con un estado que ya no entiendes. Rust y Go separan ambas cosas explícitamente en el lenguaje; en las familias con excepciones, la separación es una convención que hay que sostener a mano.

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

> [⏮️ Clase 136](../../parte-8-como-funcionan-los-lenguajes/136-el-modelo-de-memoria-y-las-condiciones-de-carrera/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 138 ⏭️](../../parte-8-como-funcionan-los-lenguajes/138-depuracion-como-se-diagnostica-en-cada-runtime/README.md)
