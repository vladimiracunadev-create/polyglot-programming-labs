# Clase 172 — Persistencia y almacenamiento

> Parte **11 — Proyecto integrador políglota** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Construir la **persistencia**: guardar un dato para poder recuperarlo cuando el proceso que lo escribió
ya no exista. En la clase 170 el componente de datos *consultaba*; hoy nos ocupamos del otro lado del
mismo componente, el que decide **dónde y cómo vive el estado**. La operación que lo caracteriza es la más
elemental de todas: escribir un par clave/valor y confirmar que quedó guardado.

Vale la pena detenerse en por qué esta operación tan pobre merece una clase entera del proyecto
integrador. Todo lo demás de un sistema —la CLI, la API, la web, los scripts— es **sin estado** o puede
volverse sin estado: si un proceso muere, arrancas otro y nadie se entera. El almacenamiento es la única
pieza donde eso no vale, porque es la que recuerda. Michael Nygard, en *Release It!*, construye buena
parte de su argumento sobre esta asimetría: los sistemas fallan siempre, y lo que distingue a uno robusto
de uno frágil es qué queda escrito y en qué estado queda cuando el fallo ocurre a mitad de una operación.
Persistir no es "llamar a `save()`": es aceptar un contrato sobre qué se pierde en el peor momento posible.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Guardar un par clave/valor y confirmar el resultado de la escritura.
2. Explicar la diferencia entre *guardar en memoria* y *persistir con durabilidad*.
3. Elegir entre un almacén clave-valor y uno relacional según el patrón de acceso del componente.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Persistencia | Sobrevivir al reinicio |
| 2 | Clave/valor | Almacén simple |
| 3 | Almacenamiento | Dónde viven los datos |

## 📖 Definiciones y características

La **persistencia** es la propiedad de un dato que sobrevive al proceso que lo creó: sigue ahí después de
un reinicio, un despliegue o una caída. Un **almacén clave-valor** es la forma más simple de conseguirla:
una asociación entre una clave única y un valor opaco, con dos operaciones —`put` y `get`— y ninguna
consulta compleja; Redis, etcd o un fichero indexado son sus representantes típicos. La **durabilidad** es
la garantía concreta de que una escritura confirmada no se perderá, y es la palabra que hay que exigir con
precisión: "confirmada" puede significar "aceptada en un buffer de memoria" o "sincronizada al disco físico
con `fsync`", y entre ambas hay ventanas de milisegundos en las que una caída te borra datos que el sistema
ya te dijo que tenía.

Esa distinción es el fondo de la clase. En el código de hoy, `almacen[clave] = valor` es un diccionario en
memoria: se comporta *exactamente* como un almacén persistente mientras el proceso vive, y pierde todo en
cuanto termina. Ese parecido engañoso es precisamente lo que hace peligrosa la persistencia mal entendida,
porque un mapa en memoria y una base de datos exponen casi la misma interfaz. La diferencia no está en la
API sino en las garantías detrás de ella, y esas garantías nunca son gratis: cada nivel extra de
durabilidad cuesta latencia. Hunt y Thomas, en *The Pragmatic Programmer*, insisten en que el estado
compartido y mutable es la fuente de la mayoría de los problemas difíciles; el almacenamiento es el lugar
donde ese estado se concentra a propósito, y por eso Newman recomienda en *Building Microservices* que cada
componente sea **dueño exclusivo** de su almacén y no lo comparta jamás por debajo de la mesa: un almacén
compartido es un acoplamiento invisible que ninguna API documenta.

## 🧩 Situación

Tu API mantiene sesiones de usuario en un diccionario en memoria. Funciona perfectamente en desarrollo y
en la demo. Entonces escalas a dos instancias detrás de un balanceador y la mitad de los usuarios pierde la
sesión en cada petición, porque la instancia B no tiene el mapa de la instancia A. Lo arreglas con una
instancia sola… hasta que un despliegue reinicia el proceso a las once de la mañana y todo el mundo queda
desconectado. El bug no está en el código: está en haber confundido *guardar* con *persistir*. Mover ese
mapa a un almacén clave-valor externo —Redis, o una tabla— no cambia una línea de la lógica, pero cambia
quién es dueño del estado y cuánto sobrevive. Esa es la decisión que esta clase pone sobre la mesa.

## 🧮 Modelo

- **Entrada** (stdin): una línea `clave valor`
- **Salida** (stdout): `guardado=<clave>=<valor>`
- **Regla:** almacenar el par y confirmar

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `x 5` | `guardado=x=5` |
| `nombre ada` | `guardado=nombre=ada` |
| `n 100` | `guardado=n=100` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER clave, valor ; guardar ; confirmar clave=valor
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys

clave, valor = sys.stdin.readline().split()
almacen = {}
almacen[clave] = valor
print(f"guardado={clave}={almacen[clave]}")
```

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const [clave, valor] = readFileSync(0, "utf8").trim().split(/\s+/);
const almacen = new Map();
almacen.set(clave, valor);
console.log(`guardado=${clave}=${almacen.get(clave)}`);
```

🧬 **El mismo programa en la familia JavaScript / web:** [Dart · ActionScript](primos.md#javascript-web)

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const [clave, valor] = readFileSync(0, "utf8").trim().split(/\s+/);
const almacen = new Map<string, string>();
almacen.set(clave, valor);
console.log(`guardado=${clave}=${almacen.get(clave)}`);
```

🧬 **El mismo programa en la familia JavaScript / web:** [Dart · ActionScript](primos.md#javascript-web)

### Java · [`java/Main.java`](implementaciones/java/Main.java) · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.HashMap;
import java.util.Map;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        Map<String, String> almacen = new HashMap<>();
        almacen.put(p[0], p[1]);
        System.out.println("guardado=" + p[0] + "=" + almacen.get(p[0]));
    }
}
```

🧬 **El mismo programa en la familia JVM:** [Kotlin · Scala · Groovy · Clojure](primos.md#jvm)

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;
using System.Collections.Generic;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
var almacen = new Dictionary<string, string>();
almacen[p[0]] = p[1];
Console.WriteLine($"guardado={p[0]}={almacen[p[0]]}");
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
	p := strings.Fields(line)
	almacen := map[string]string{}
	almacen[p[0]] = p[1]
	fmt.Printf("guardado=%s=%s\n", p[0], almacen[p[0]])
}
```

🧬 **El mismo programa en la familia Sistemas:** [Zig · Nim · D](primos.md#sistemas)

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::collections::HashMap;
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let p: Vec<&str> = s.split_whitespace().collect();
    let mut almacen: HashMap<&str, &str> = HashMap::new();
    almacen.insert(p[0], p[1]);
    println!("guardado={}={}", p[0], almacen[p[0]]);
}
```

🧬 **El mismo programa en la familia Sistemas:** [Zig · Nim · D](primos.md#sistemas)

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    char clave[64], valor[64];
    if (scanf("%63s %63s", clave, valor) != 2) return 1;
    printf("guardado=%s=%s\n", clave, valor);
    return 0;
}
```

🧬 **El mismo programa en la familia C / llaves:** [C++ · Objective-C](primos.md#c-llaves)

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL persiste en tablas; aqui, el par guardado.
WITH t(clave, valor) AS (VALUES ('x', '5'))
SELECT 'guardado=' || clave || '=' || valor AS resultado FROM t;
```

🧬 **El mismo programa en la familia Lógica y declarativa:** [Prolog · Datalog](primos.md#logica-declarativa)

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
[$clave, $valor] = preg_split('/\s+/', trim(fgets(STDIN)));
$almacen = [];
$almacen[$clave] = $valor;
echo "guardado=$clave={$almacen[$clave]}\n";
```

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🧪 Recorrido del código

El contrato ([`casos.json`](casos.json)) pide leer `clave valor` y responder `guardado=<clave>=<valor>`.
Todas las implementaciones hacen algo aparentemente redundante: guardan el par en un mapa y **luego leen de
ese mapa** para imprimirlo. Podrían imprimir directamente lo leído de la entrada, y el resultado sería el
mismo. La redundancia es deliberada: modela el ciclo real de un almacén —escribir y releer para confirmar—
en lugar de asumir que la escritura funcionó.

**Python** lo escribe en su forma más desnuda: `almacen = {}` crea el `dict`, `almacen[clave] = valor`
inserta y `almacen[clave]` recupera. Ramalho dedica en *Fluent Python* buena parte del libro a este tipo,
porque el `dict` no es una estructura más del lenguaje sino su cimiento: los atributos de los objetos, los
espacios de nombres y los módulos son diccionarios por debajo. **Java** y **C#** obligan a nombrar los tipos
de clave y valor (`Map<String, String>`, `Dictionary<string, string>`): el compilador te impide guardar una
cosa y leer otra, una garantía que Bloch defiende en *Effective Java* como la primera línea de defensa.
**JavaScript** y **TypeScript** usan `Map` en lugar de un objeto plano —la elección idiomática cuando las
claves son datos y no nombres fijos—, con `set`/`get` explícitos.

**Rust** revela una tensión que los demás esconden:

```rust
let mut almacen: HashMap<&str, &str> = HashMap::new();
almacen.insert(p[0], p[1]);
```

El mapa no guarda cadenas: guarda **referencias** (`&str`) a la cadena `s` que sigue viva en la pila. El
compilador verifica que el almacén no sobreviva a los datos que apunta —exactamente la clase de error que
en C provoca una lectura de memoria liberada—. Es el modelo de propiedad de Klabnik y Nichols aplicado a un
almacén: la duración de lo guardado es parte del tipo. **C**, coherente con su nivel, ni siquiera construye
un mapa: no hay uno en la biblioteca estándar, así que imprime directamente los dos buffers. Y **SQL**
recuerda de qué va realmente la persistencia: su unidad no es un mapa efímero sino una **fila** en una
tabla, que es lo que de verdad sobrevive al reinicio.

## 🔬 Comparación

Guardar un par parece la operación más neutra del mundo, pero cada lenguaje expresa una idea distinta sobre
quién es dueño de lo guardado y cuánto dura.

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `dict` (Python), `Map` (JS/TS), `HashMap` (Java/Rust), `Dictionary` (C#), `map[string]string` (Go), array asociativo (PHP): el mismo mapa con seis escrituras. |
| Semántica | Java, C# y Rust fijan los tipos de clave y valor en tiempo de compilación; Python, JS, Go y PHP admiten valores heterogéneos o los convierten. Rust, además, ata la **vida** de lo guardado a la del dato original. |
| Paradigmática | Los nueve imperativos mutan una estructura en memoria; SQL **inserta una fila** en una relación duradera y consulta el conjunto — el único de los diez cuyo modelo es realmente persistente. |

La diferencia que importa fuera del ejercicio es otra, y ningún lenguaje la resuelve por ti: **ninguno de
estos diez mapas persiste nada**. Todos viven en el proceso y mueren con él. La persistencia real no es una
construcción del lenguaje sino una decisión de arquitectura —un fichero con `fsync`, una base de datos, un
servicio externo— y por eso SQL ocupa aquí un lugar aparte: es el único cuya semántica nativa ya habla de
datos que sobreviven a quien los escribió.

## 🧬 El concepto en la familia

La idea de "asociar una clave a un valor" es tan universal que cada familia le da su nombre: `dict` en
Python, *hash* en Ruby y Perl, `Map` en Java y JavaScript, tabla asociativa en Lua, *hash table* en C++.
Todas comparten el mismo modelo de acceso en tiempo casi constante. Lo que cambia al pasar de la memoria al
disco es la familia de almacenes: los **clave-valor** (Redis, etcd, DynamoDB) conservan esa interfaz mínima
a cambio de no ofrecer consultas ricas; los **relacionales** (PostgreSQL, SQLite, MySQL) piden un esquema y
devuelven a cambio consultas arbitrarias, integridad referencial y transacciones; los **sistemas de
archivos** son el sustrato bajo todos ellos. Reconocer que un `HashMap` y Redis son el mismo concepto en dos
escalas de duración es, literalmente, la transferencia que este programa entrena.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 172
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Confundir un mapa en memoria con persistencia** → causa: la interfaz es idéntica (`get`/`set`), así que el código parece correcto hasta el primer reinicio o la segunda instancia → solución: preguntarse siempre "si mato el proceso ahora, ¿esto sigue existiendo?" y externalizar el estado que deba sobrevivir.
- **Dar por confirmada una escritura que solo llegó a un buffer** → causa: la escritura se acepta en memoria del proceso o del sistema operativo y una caída la borra → solución: exigir la garantía explícita (`fsync`, confirmación transaccional, réplica confirmada) para los datos que no puedes perder, y aceptar su coste en latencia.
- **Claves sin convención** → causa: dos componentes escriben `usuario:1` y `user_1` para lo mismo, o dos significados colisionan en la misma clave → solución: definir un esquema de claves con prefijo de dominio y versión (`sesion:v1:<id>`) y documentarlo como parte del contrato.
- **Compartir el almacén entre componentes** → causa: es más rápido que exponer una API, pero crea un acoplamiento que ningún contrato registra → solución: un dueño por almacén, como propone Newman; los demás acceden por la frontera pública.

## ❓ Preguntas frecuentes

- **¿Clave-valor o relacional?** Depende de cómo vas a *leer*, no de cómo vas a escribir. Si siempre accedes por una clave conocida (sesiones, caché, configuración), un clave-valor te da latencia mínima y un modelo trivial. Si necesitas filtrar, agrupar, unir tablas o garantizar integridad entre entidades, quieres un relacional: lo que pagas en esquema lo recuperas en poder de consulta.
- **¿Persistir en disco o en memoria?** Es la disyuntiva latencia/durabilidad. La memoria es órdenes de magnitud más rápida pero volátil, así que sirve para lo reconstruible (caché, resultados intermedios). El disco es el que puede prometer que el dato sigue ahí tras un corte de luz. Muchos sistemas combinan ambos: escriben primero a un registro secuencial en disco y mantienen el índice en memoria.
- **¿Por qué el código lee del mapa lo que acaba de escribir?** Para modelar el ciclo escribir-y-confirmar. En un almacén real esa relectura es lo que distingue "envié la orden" de "el almacén acepta la orden como suya"; asumir el éxito sin confirmarlo es el origen clásico de la pérdida silenciosa de datos que describe Nygard en *Release It!*.

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

> [⏮️ Clase 171](../../parte-11-proyecto-integrador-poliglota/171-componente-de-automatizacion-scripting/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 173 ⏭️](../../parte-11-proyecto-integrador-poliglota/173-pruebas-end-to-end-del-sistema-completo/README.md)
