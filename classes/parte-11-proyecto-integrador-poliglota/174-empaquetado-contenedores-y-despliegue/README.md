# Clase 174 — Empaquetado, contenedores y despliegue

> Parte **11 — Proyecto integrador políglota** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Empaquetar el sistema y su entorno en un artefacto reproducible, y ponerlo a correr. Este es el momento en
que un proyecto políglota deja de ser un problema y pasa a ser una ventaja: diez componentes en diez
lenguajes significan diez toolchains, diez formas de instalar dependencias y diez maneras de romperse en
producción — a menos que todos se entreguen bajo el **mismo formato de paquete**. La operación de hoy es la
que cierra ese círculo: construir el nombre etiquetado de una imagen, `app:1.2.3`.

Parece un ejercicio de concatenación de cadenas, y lo es; pero esa cadena es el identificador que sostiene
toda la práctica moderna de despliegue. Una etiqueta une tres cosas en una sola palabra: **qué** código se
compiló, **con qué** entorno se empaquetó y **cuál** de todas las versiones está corriendo ahora mismo en
producción. Michael Nygard construye en *Release It!* un argumento que se resume así: los sistemas hay que
diseñarlos pensando en el día del despliegue y en el día del incidente, no solo en el día en que el código
funciona. La etiqueta es la herramienta central de ambos días — porque cuando algo se rompe a las tres de
la madrugada, la primera pregunta útil no es "¿qué hace este código?" sino "¿qué versión exacta está
corriendo y cuál era la anterior?".

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Construir el identificador etiquetado de una imagen a partir de su versión.
2. Explicar qué problema resuelve un contenedor y por qué es decisivo en un sistema políglota.
3. Relacionar imagen, versión y despliegue, y justificar por qué una etiqueta debe ser inmutable.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Contenedor | Programa + su entorno |
| 2 | Imagen etiquetada | app:version |
| 3 | Despliegue | Correr la imagen |

## 📖 Definiciones y características

Un **contenedor** es un proceso aislado que lleva consigo su entorno: su sistema de archivos, sus
bibliotecas, su intérprete o su tiempo de ejecución. No es una máquina virtual —comparte el kernel del
anfitrión y no arranca un sistema operativo completo—, sino un proceso normal al que el kernel le
restringe la vista mediante *namespaces* y *cgroups*. Una **imagen** es la plantilla inmutable de la que
nacen los contenedores: un conjunto de capas de sistema de archivos más un manifiesto que dice cómo
arrancar. El **despliegue** es el acto de poner una imagen concreta a correr en un entorno concreto.

La consecuencia práctica para un sistema políglota es enorme, y merece decirse con claridad. Sin
contenedores, desplegar tu sistema exige que el servidor tenga la versión correcta de Python, la de Node,
un JDK, el SDK de .NET, el compilador de Go, el de Rust y un `gcc` — y que ninguna de esas versiones entre
en conflicto con las que necesita otro sistema en la misma máquina. El contenedor convierte esa pesadilla
combinatoria en un problema resuelto: cada componente declara su entorno dentro de su propia imagen, y
hacia fuera todos exponen la misma interfaz de operación —arrancar, parar, leer logs, comprobar salud—.
Los diez lenguajes del núcleo se vuelven, desde el punto de vista del despliegue, indistinguibles. Newman
señala en *Building Microservices* que esa uniformidad operativa es lo que hace viable la libertad
tecnológica: sin ella, cada lenguaje nuevo que añades te cuesta una plataforma nueva que mantener.

La etiqueta merece un párrafo propio porque es donde más se falla. `app:1.2.3` debe ser **inmutable**: una
vez publicada, esa etiqueta apunta para siempre al mismo contenido. Si republicas `1.2.3` con un arreglo,
acabas de romper la propiedad que hacía útil el número, porque ya no hay forma de saber cuál de los dos
`1.2.3` está corriendo en cada máquina. El versionado semántico —mayor.menor.parche— añade significado
encima de la inmutabilidad: el mayor avisa de una ruptura de compatibilidad, el menor de una adición
retrocompatible, el parche de una corrección. Es exactamente el mismo contrato que estudiamos entre
componentes, aplicado ahora al artefacto entero.

## 🧩 Situación

Tu sistema políglota tiene cinco componentes y dos entornos, preproducción y producción. Sin empaquetado,
"desplegar" es un documento de veinte pasos que alguien ejecuta a mano y que falla de forma distinta cada
vez; el error clásico —"en mi máquina funciona"— es literalmente cierto, porque tu máquina tiene una
versión de la biblioteca que el servidor no tiene. Con imágenes etiquetadas, desplegar es una sola frase:
"pon a correr `api:2.1.5`". Y revertir, cuando algo sale mal, es la misma frase con el número anterior —una
operación de segundos en vez de una reconstrucción de emergencia—. Esa capacidad de volver atrás rápido es,
para Nygard, más valiosa que casi cualquier medida preventiva: no puedes evitar todos los fallos, pero sí
puedes hacer que salir de uno sea barato.

## 🧮 Modelo

- **Entrada** (stdin): una línea con una versión `mayor.menor.parche`
- **Salida** (stdout): `imagen=app:<versión>`
- **Regla:** construir el nombre de imagen app:version

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `1.2.3` | `imagen=app:1.2.3` |
| `0.9.0` | `imagen=app:0.9.0` |
| `2.1.5` | `imagen=app:2.1.5` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER version ; ESCRIBIR 'imagen=app:' + version
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys

version = sys.stdin.readline().strip()
print(f"imagen=app:{version}")
```

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const version = readFileSync(0, "utf8").trim();
console.log(`imagen=app:${version}`);
```

🧬 **El mismo programa en la familia JavaScript / web:** [Dart · ActionScript](primos.md#javascript-web)

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const version: string = readFileSync(0, "utf8").trim();
console.log(`imagen=app:${version}`);
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
        String version = br.readLine().trim();
        System.out.println("imagen=app:" + version);
    }
}
```

🧬 **El mismo programa en la familia JVM:** [Kotlin · Scala · Groovy · Clojure](primos.md#jvm)

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;

string version = Console.In.ReadToEnd().Trim();
Console.WriteLine($"imagen=app:{version}");
```

🧬 **El mismo programa en la familia .NET:** [F# · VB.NET](primos.md#dotnet)

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
	version := strings.TrimSpace(line)
	fmt.Printf("imagen=app:%s\n", version)
}
```

🧬 **El mismo programa en la familia Sistemas:** [Zig · Nim · D](primos.md#sistemas)

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let version = s.trim();
    println!("imagen=app:{version}");
}
```

🧬 **El mismo programa en la familia Sistemas:** [Zig · Nim · D](primos.md#sistemas)

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    char version[64];
    if (scanf("%63s", version) != 1) return 1;
    printf("imagen=app:%s\n", version);
    return 0;
}
```

🧬 **El mismo programa en la familia C / llaves:** [C++ · Objective-C](primos.md#c-llaves)

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL concatena el nombre de la imagen.
WITH t(v) AS (VALUES ('1.2.3'))
SELECT 'imagen=app:' || v AS resultado FROM t;
```

🧬 **El mismo programa en la familia Lógica y declarativa:** [Prolog · Datalog](primos.md#logica-declarativa)

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
$version = trim(fgets(STDIN));
echo "imagen=app:$version\n";
```

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🧪 Recorrido del código

El contrato ([`casos.json`](casos.json)) es el más simple de la parte: entra `1.2.3`, sale
`imagen=app:1.2.3`. Toda la clase cabe en dos gestos —recortar los espacios de la entrada y pegar la
versión detrás del nombre—, y por eso sirve tan bien para ver cómo cada familia construye texto.

El primer gesto es el que esconde el detalle importante. La entrada llega con un salto de línea al final, y
si no lo quitas obtienes `imagen=app:1.2.3\n` con el retorno **dentro** de la etiqueta, lo que en un
registro de imágenes real es un nombre inválido. Cada lenguaje tiene su recorte: `strip()` en Python,
`.trim()` en JavaScript, TypeScript, Java y C#, `strings.TrimSpace` en Go, `.trim()` en Rust y `trim()` en
PHP. **C** lo consigue sin querer: `scanf("%63s", version)` lee un *token* delimitado por espacios en
blanco, así que el salto de línea nunca entra en el buffer — y el `63` es la defensa explícita contra el
desbordamiento que en los demás lenguajes está implícita en el tipo cadena.

El segundo gesto separa dos escuelas de composición de texto. La **interpolación** —`f"imagen=app:{version}"`
en Python, las plantillas con acento grave en JS y TS, `$"..."` en C#, `println!("imagen=app:{version}")` en
Rust y las comillas dobles de PHP— coloca el valor dentro de una plantilla legible. La **concatenación**
explícita de Java (`"imagen=app:" + version`) y el **formateo por especificadores** de Go y C
(`Printf("imagen=app:%s\n", version)`) separan plantilla y datos. Y **SQL** usa su propio operador,
`'imagen=app:' || v`, heredado del estándar relacional: dos barras verticales que en casi ningún otro
lenguaje del núcleo significan lo mismo, ya que allí son el "o" lógico. Es un buen recordatorio de que el
mismo símbolo puede tener significados incompatibles entre familias.

## 🔬 Comparación

Pegar dos cadenas es la operación más elemental que existe, y aun así los diez lenguajes revelan aquí sus
preferencias sobre legibilidad, seguridad de tipos y coste.

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Interpolación (Python, JS/TS, C#, Rust, PHP), suma de cadenas (Java), formateo con `%s` (Go, C), operador `\|\|` (SQL): la misma concatenación en cinco escrituras. |
| Semántica | En Java, C# y Go el `+`/`Printf` sobre cadenas crea un objeto nuevo porque las cadenas son inmutables; en C manipulas un buffer de tamaño fijo y respondes tú del desbordamiento; en Rust el `&str` prestado y el `String` propio son tipos distintos. |
| Paradigmática | Los nueve imperativos construyen una cadena paso a paso; SQL **proyecta una columna** calculada sobre una tabla: el resultado no es una variable sino un conjunto de filas. |

Hay una lectura de este ejercicio que va más allá de las cadenas. El nombre `app:1.2.3` es un **contrato
textual** entre quien construye y quien despliega: una convención frágil, sin tipos, que un espacio de más
o un salto de línea rompen. Los sistemas reales lo refuerzan añadiendo por debajo un identificador
criptográfico del contenido —el *digest* `sha256:…`— que no depende de ninguna convención de nombres. La
etiqueta es para las personas; el digest, para las máquinas. Convertir un acuerdo humano frágil en una
identidad verificable es un patrón que reaparece en todas las fronteras que hemos estudiado en esta parte.

## 🧬 El concepto en la familia

Antes de los contenedores, cada familia de lenguajes tenía su propio formato de entrega, y todavía los
usa por dentro: un `.jar` o `.war` en la JVM, un ensamblado y un `.nupkg` en .NET, una *wheel* en Python,
un paquete npm en JavaScript, un *crate* en Rust, un binario estático en Go, un `.phar` o un repositorio
Composer en PHP. Todos resuelven el mismo problema —agrupar código y metadatos en una unidad instalable—
pero cada uno solo sirve dentro de su ecosistema. El contenedor OCI es la generalización que los engloba a
todos: en lugar de empaquetar código para un tiempo de ejecución, empaqueta el tiempo de ejecución
también. Docker construye y corre esas imágenes; Kubernetes las programa, las escala y las reemplaza en un
clúster; los registros (Docker Hub, GHCR, ECR) las almacenan y versionan. Reconocer que un `.jar` y una
imagen OCI son el mismo concepto en dos niveles de alcance es lo que te permite razonar sobre el despliegue
de un lenguaje que aún no conoces.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 174
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Desplegar `:latest`** → causa: la etiqueta es móvil, así que dos máquinas pueden estar corriendo contenidos distintos bajo el mismo nombre y nadie puede saber cuál → solución: etiquetar con la versión concreta y, para lo crítico, fijar el *digest* del contenido.
- **Reutilizar una etiqueta ya publicada** → causa: se corrige un fallo y se vuelve a publicar `1.2.3` para no "gastar" un número → solución: tratar las etiquetas como inmutables y publicar `1.2.4`; los números son gratis, la trazabilidad no.
- **Imágenes enormes** → causa: se parte de una imagen base con un sistema operativo completo y se dejan dentro el compilador y las dependencias de construcción → solución: usar bases mínimas y construcción por etapas (*multi-stage*), copiando a la imagen final solo el artefacto ejecutable; menos superficie es también menos superficie de ataque.
- **Meter la configuración dentro de la imagen** → causa: la misma imagen deja de servir para preproducción y producción, y acabas construyendo una por entorno → solución: una sola imagen por versión, parametrizada por variables de entorno y secretos inyectados al arrancar.

## ❓ Preguntas frecuentes

- **¿Contenedor o máquina virtual?** Un contenedor es un proceso del anfitrión con la vista restringida por el kernel: arranca en milisegundos y pesa lo que pesa tu aplicación más sus bibliotecas. Una máquina virtual emula hardware y ejecuta un kernel propio: arranca en decenas de segundos y aísla mucho más. Si necesitas separar cargas que no confían entre sí, la VM da una frontera más fuerte; para empaquetar y desplegar tus propios componentes, el contenedor es la herramienta adecuada.
- **¿Por qué etiquetar?** Porque sin etiqueta no hay dos preguntas que puedas responder durante un incidente: qué está corriendo ahora y a qué se puede volver. La etiqueta convierte el despliegue en una operación reversible, y la reversibilidad es lo que permite desplegar a menudo sin miedo.
- **¿Un contenedor por componente o uno para todo?** Uno por componente. Meter varios procesos en la misma imagen los obliga a escalar, reiniciarse y fallar juntos, que es justo lo que la descomposición en componentes pretendía evitar. La regla práctica: si dos piezas necesitan versionarse o escalarse por separado, van en imágenes separadas.

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

> [⏮️ Clase 173](../../parte-11-proyecto-integrador-poliglota/173-pruebas-end-to-end-del-sistema-completo/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 175 ⏭️](../../parte-11-proyecto-integrador-poliglota/175-documentacion-y-defensa-de-las-decisiones-de-lenguaje/README.md)
