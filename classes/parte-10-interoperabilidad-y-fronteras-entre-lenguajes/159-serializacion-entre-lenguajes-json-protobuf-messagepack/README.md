# Clase 159 — Serialización entre lenguajes: JSON, Protobuf, MessagePack

> Parte **10 — Interoperabilidad y fronteras entre lenguajes** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

La FFI conecta lenguajes que comparten el mismo proceso y la misma memoria. Pero la mayoría de las fronteras reales no son así: el frontend y el backend viven en máquinas distintas, el productor y el consumidor en contenedores separados. Cuando los datos deben *viajar* —por una red, por un archivo, por una cola— no puedes pasar un puntero: tienes que convertir tus estructuras en una secuencia de bytes que el otro lado sepa reconstruir. Ese proceso es la **serialización**, y es, sin exagerar, el tema central de la interoperabilidad moderna.

Kleppmann le dedica el capítulo 4 completo de *Designing Data-Intensive Applications*, y lo plantea como el problema de la **codificación y evolución**. En memoria, un objeto es una maraña de punteros que solo tiene sentido dentro de un proceso; para enviarlo, hay que traducirlo a una representación autocontenida —JSON, Protocol Buffers, MessagePack, Avro— que no dependa de la disposición de memoria de ningún lenguaje. El objetivo de esta clase es entender por qué ese formato común es imprescindible, qué se gana y se pierde entre texto y binario, con esquema y sin él, y por qué la compatibilidad hacia atrás y hacia adelante —que un lector viejo entienda datos nuevos y viceversa— es el verdadero criterio de un buen formato.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. **Serializar** un dato a un formato de intercambio.
2. **Explicar** por qué la frontera exige un formato común e independiente del lenguaje.
3. **Distinguir** JSON, Protobuf y MessagePack por sus compromisos.
4. **Valorar** el papel del esquema y de la compatibilidad de versiones.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Serialización | De estructuras en memoria a bytes transmisibles |
| 2 | Formato común | Independiente del lenguaje, entendido por ambos lados |
| 3 | Esquema y evolución | Estructura acordada que puede cambiar sin romper |

## 📖 Definiciones y características

La **serialización** (o *codificación*, o *marshalling*) convierte datos en memoria en un formato transmisible, texto o binario; la **deserialización** hace el camino inverso. La palabra clave es *autocontenido*: el resultado debe poder reconstruirse sin conocer la disposición de memoria del emisor. Un **formato de intercambio** es esa representación común —JSON, Protobuf, MessagePack—, diseñada para que un servicio en Go la escriba y otro en Python la lea sin ponerse de acuerdo en nada más que el formato.

El eje que Kleppmann pone en el centro es el **esquema**. JSON es *schemaless*: los datos llevan sus propios nombres de campo en cada mensaje, es legible y flexible, pero verboso y sin garantías de tipo. Protobuf y Avro son *con esquema*: emisor y receptor comparten una definición previa (`.proto`), los mensajes son binarios y compactos —no repiten los nombres de campo, solo números de etiqueta—, y el esquema permite algo crucial: **evolucionar**. Añadir un campo opcional no rompe a los lectores viejos (compatibilidad hacia atrás) ni a los nuevos leyendo datos viejos (hacia adelante). MessagePack se sitúa en medio: binario y compacto como Protobuf, pero schemaless como JSON. Elegir formato es elegir en ese triángulo de legibilidad, tamaño y evolución.

- **Serialización** — convertir datos en un formato transmisible, texto o binario. Clave: producir algo autocontenido que cruce la frontera.
- **Formato de intercambio** — representación común (JSON, Protobuf, MessagePack). Clave: independiente del lenguaje de cada lado.
- **Esquema** — estructura acordada de los datos. Clave: habilita compacidad, tipos y evolución compatible.

## 🧩 Situación

Un servicio de pedidos en Go necesita avisar a un servicio de facturación en Python. No comparten memoria ni lenguaje: lo único que comparten es un formato. Go serializa el pedido a JSON (o Protobuf), los bytes viajan por HTTP o por una cola, y Python los deserializa a sus propios objetos. Si mañana el equipo de Go añade un campo `descuento`, el formato con esquema garantiza que facturación siga funcionando sin desplegarse a la vez. Ese diálogo entre lenguajes que no se conocen es posible solo por la representación común. Para mostrar la esencia —convertir un dato estructurado en una cadena que el otro lado pueda parsear— esta clase serializa el par `clave valor` al texto `clave:valor`, el "hola mundo" de todo formato de intercambio.

## 🧮 Modelo

- **Entrada** (stdin): una línea `clave valor`
- **Salida** (stdout): `serializado=<clave>:<valor>`
- **Regla:** unir clave y valor con ':'

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `x 5` | `serializado=x:5` |
| `edad 30` | `serializado=edad:30` |
| `n 100` | `serializado=n:100` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER clave, valor ; ESCRIBIR clave:valor
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

clave, valor = sys.stdin.readline().split()
print(f"serializado={clave}:{valor}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const [clave, valor] = readFileSync(0, "utf8").trim().split(/\s+/);
console.log(`serializado=${clave}:${valor}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const [clave, valor] = readFileSync(0, "utf8").trim().split(/\s+/);
console.log(`serializado=${clave}:${valor}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        System.out.println("serializado=" + p[0] + ":" + p[1]);
    }
}
```

### C# · `dotnet run`

```csharp
using System;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
Console.WriteLine($"serializado={p[0]}:{p[1]}");
```

### Go · `go run main.go`

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
	fmt.Printf("serializado=%s:%s\n", p[0], p[1])
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let p: Vec<&str> = s.split_whitespace().collect();
    println!("serializado={}:{}", p[0], p[1]);
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    char clave[64], valor[64];
    if (scanf("%63s %63s", clave, valor) != 2) return 1;
    printf("serializado=%s:%s\n", clave, valor);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL concatena clave y valor.
WITH t(clave, valor) AS (VALUES ('x', '5'))
SELECT 'serializado=' || clave || ':' || valor AS resultado FROM t;
```

### PHP · `php main.php`

```php
<?php
[$clave, $valor] = preg_split('/\s+/', trim(fgets(STDIN)));
echo "serializado=$clave:$valor\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔎 Recorrido del código (laboratorio)

El caso `edad 30` debe producir `serializado=edad:30`. El dato de entrada son dos campos —una clave y un valor— y la serialización los une en una sola cadena con `:` de separador. Es una versión minúscula de lo que hace JSON al escribir `{"edad":30}`: convertir dos piezas separadas en una representación única y transmisible.

En **Python**, `clave, valor = sys.stdin.readline().split()` desempaqueta la línea, y `f"serializado={clave}:{valor}"` produce la cadena. Observa un detalle semántico decisivo: `valor` es un `str`, `"30"`, no el entero `30`. Al serializar a texto, *todo se vuelve texto*; es al deserializar cuando el receptor decide si `"30"` es un número o una cadena. Esa pérdida de tipo es precisamente lo que JSON sufre (no distingue `30` de `"30"` sin esquema) y lo que Protobuf evita (el `.proto` fija que ese campo es `int32`).

En **SQL**, la serialización es la concatenación nativa: `'serializado=' || clave || ':' || valor`. El operador `||` une cadenas, y el motor produce la misma salida. Es coherente con cómo los motores exportan datos: SQLite y PostgreSQL tienen funciones (`json_object`, `row_to_json`) que serializan filas a JSON con esa misma lógica de concatenar campos con separadores. Aquí se ve la versión desnuda del mecanismo.

En **C**, el trabajo es el más manual: `char clave[64], valor[64];` reserva buffers de tamaño fijo, `scanf("%63s %63s", ...)` lee ambos campos con un límite explícito para no desbordar, y `printf("serializado=%s:%s\n", ...)` los une. Que C te obligue a decidir el tamaño del buffer y a acotar `scanf` revela lo que los lenguajes de alto nivel ocultan: serializar es, al final, mover bytes con cuidado. Las cuatro implementaciones producen `serializado=edad:30`, pero solo comparándolas se ve la gradación de "cuánto me cuida el lenguaje".

## 🔬 Comparación

| Lenguaje | Librería idiomática de serialización real |
|---|---|
| Python | `json` (stdlib), `pickle` (solo Python), `msgpack`, `protobuf`. |
| JavaScript | `JSON.stringify`/`JSON.parse` nativos; `protobufjs`, `@msgpack/msgpack`. |
| TypeScript | Igual que JS, con tipos: `zod`/`io-ts` validan el esquema al deserializar. |
| Java | Jackson y Gson (JSON), `protobuf-java`; el esquema se mapea a clases. |
| C# | `System.Text.Json`, Newtonsoft.Json, `Google.Protobuf`. |
| Go | `encoding/json` (con *struct tags*), `google.golang.org/protobuf`. |
| Rust | `serde` con `serde_json`, `rmp-serde` (MessagePack), `prost` (Protobuf). |
| C | Manual, o librerías como `jansson`/`cJSON`; nada es automático. |
| SQL | Funciones del motor: `json_object`, `json_group_array`, `row_to_json`. |
| PHP | `json_encode`/`json_decode` nativos. |

Aquí la clase usa concatenación simple para no depender de librerías, pero la tabla muestra el paisaje real. La diferencia sintáctica es enorme —`serde` de Rust deriva la serialización en tiempo de compilación con `#[derive(Serialize)]`, mientras C obliga a escribirla a mano campo por campo—, pero la diferencia semántica es la que Kleppmann subraya: **el formato debe interpretarse igual en ambos lados**. Un `float` serializado en un lenguaje con coma decimal y leído en otro con punto, o un entero de 64 bits recibido por un JavaScript cuyo `number` solo garantiza 53 bits de precisión, produce datos silenciosamente corruptos. El esquema —ausente en JSON, obligatorio en Protobuf— es lo que blinda esa interpretación. SQL, una vez más, no serializa objetos sino filas, con funciones del propio motor.

## 🧬 El concepto en la familia

El paisaje de formatos es estable: **JSON** (texto, universal, legible, sin esquema) domina las APIs web; **Protocol Buffers** y **Avro** (binarios, con esquema, compactos y evolucionables) dominan la comunicación interna de alto rendimiento; **MessagePack** y **CBOR** ofrecen el compromiso "JSON binario". Todos los lenguajes del núcleo tienen librerías maduras para los tres, porque la serialización es la frontera más transitada de la ingeniería moderna: cada llamada a una API, cada mensaje en Kafka, cada archivo de configuración la cruza.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 159
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Formato ambiguo sin esquema** → causa: el receptor no sabe interpretar → solución: acordar un esquema o formato estándar
- **Diferencias de codificación** → causa: acentos/emoji corruptos → solución: usar UTF-8 y formatos bien definidos

## ❓ Preguntas frecuentes

- **¿JSON o Protobuf?** JSON es legible y universal; Protobuf es compacto y tipado. Según el caso.
- **¿Serializar y deserializar son inversos?** Sí: uno convierte a formato, el otro reconstruye el dato.

## 🔗 Referencias

**Libros de la parte:**

- M. Kleppmann — *Designing Data-Intensive Applications* (O'Reilly).
- S. Newman — *Building Microservices* (2ª ed., O'Reilly).
- A. Tanenbaum y M. van Steen — *Distributed Systems* (3ª ed.).

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

> [⏮️ Clase 158](../../parte-10-interoperabilidad-y-fronteras-entre-lenguajes/158-enlaces-bindings-y-wrappers/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 160 ⏭️](../../parte-10-interoperabilidad-y-fronteras-entre-lenguajes/160-contratos-de-api-rest-grpc-y-esquemas/README.md)
