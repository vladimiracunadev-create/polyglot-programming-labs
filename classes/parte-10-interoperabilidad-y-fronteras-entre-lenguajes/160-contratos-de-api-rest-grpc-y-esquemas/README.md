# Clase 160 — Contratos de API: REST, gRPC y esquemas

> Parte **10 — Interoperabilidad y fronteras entre lenguajes** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

La clase anterior resolvió *cómo* viajan los datos: serializados a un formato común. Falta lo otro: *qué* datos y *qué* operaciones. Un formato compartido no basta —saber que ambos lados hablan JSON no te dice si el servidor espera `user_id` o `usuario`, si `GET /users` devuelve una lista o un objeto paginado, ni qué ocurre si pides un recurso que no existe. Ese acuerdo es el **contrato de API**, y es la unidad real de interoperabilidad entre servicios escritos en lenguajes distintos.

Newman insiste en *Building Microservices* en que el contrato —no el código— es lo que un servicio expone al mundo. Todo lo demás (lenguaje, base de datos, framework, versión del runtime) es interno y debe poder cambiar sin avisar a nadie. El precio de esa libertad es que el contrato se vuelve **rígido**: en cuanto un tercero depende de él, ya no puedes cambiarlo a tu antojo. El objetivo de esta clase es entender qué hace que un contrato sea bueno —explícito, versionable, evolucionable— y por qué REST y gRPC responden a esa pregunta de forma opuesta: uno con convenciones sobre HTTP y documentación externa, el otro con un esquema formal que genera el código de ambos lados.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. **Construir** un endpoint a partir de método y recurso.
2. **Explicar** qué es un contrato de API y por qué desacopla a los equipos.
3. **Distinguir** REST de gRPC por sus compromisos de acoplamiento y rendimiento.
4. **Razonar** qué cambios de un contrato rompen a los clientes y cuáles no.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Contrato de API | El acuerdo entre servicios |
| 2 | REST | Recursos y métodos HTTP |
| 3 | gRPC | Contratos con esquema (Protobuf) |

## 📖 Definiciones y características

Un **contrato de API** es la promesa pública de un servicio: qué operaciones ofrece, qué datos acepta, qué datos devuelve y qué errores puede señalar. Su valor está en lo que *no* incluye. Si el contrato dice `GET /users` devuelve una lista de objetos con `id` y `nombre`, el servidor puede reescribirse de Ruby a Go, cambiar de PostgreSQL a DynamoDB y triplicar sus réplicas sin que ningún cliente se entere. Newman llama a esto *technology-agnostic interface*: la frontera es lo único compartido, y por eso debe ser lo único estable.

**REST** organiza ese contrato alrededor de **recursos** identificados por URL y **verbos** HTTP que actúan sobre ellos: `GET /users/42` lee, `PUT /users/42` reemplaza, `DELETE /users/42` borra. Su gran ventaja es que reutiliza una infraestructura que ya existe en todas partes —cachés, proxies, códigos de estado, autenticación— y que cualquier lenguaje con un cliente HTTP puede consumirla sin generar nada. Su gran debilidad es que el contrato vive fuera del código: en un documento OpenAPI, en un wiki, o en la cabeza de quien lo escribió. Nada obliga al servidor a cumplirlo.

**gRPC** invierte esa decisión. El contrato se escribe en un archivo `.proto` —el mismo esquema Protobuf de la clase 159— con los mensajes *y* los métodos declarados, y un generador produce las clases del cliente y las interfaces del servidor en cada lenguaje. Llamar a un servicio remoto se parece a llamar a un método local, con tipos comprobados por el compilador. Sobre HTTP/2 y con codificación binaria es notablemente más rápido y compacto que JSON sobre HTTP/1.1, y soporta *streaming* bidireccional. El coste es acoplamiento de herramientas: hace falta el generador, el binario no es legible con `curl`, y los navegadores no lo hablan directamente (de ahí gRPC-Web).

Dos ideas atraviesan ambos. La primera es la **idempotencia**: `GET` y `PUT` pueden repetirse sin efecto adicional, `POST` no. En una red que pierde respuestas —Tanenbaum dedica buena parte de *Distributed Systems* a este punto— reintentar es inevitable, y solo las operaciones idempotentes toleran el reintento sin duplicar datos. La segunda es la **evolución compatible**: añadir un campo opcional o un endpoint nuevo no rompe a nadie; renombrar un campo, cambiar su tipo, hacer obligatorio uno opcional o borrar un endpoint sí. Esa asimetría, no la elección de REST o gRPC, es lo que determina si tu API envejece bien.

- **Contrato de API** — acuerdo de qué operaciones y datos expone un servicio. Clave: frontera estable entre componentes que permite cambiar todo lo demás.
- **REST** — estilo basado en recursos y métodos HTTP (GET, POST, PUT). Clave: simple y universal, pero el contrato vive fuera del código.
- **gRPC** — framework de RPC con contratos definidos en Protobuf. Clave: eficiente y tipado, con el contrato como fuente que genera el código.

## 🧩 Situación

El frontend en TypeScript habla con un backend en Go: `GET /users` pide los usuarios. Ninguno de los dos equipos lee el código del otro; lo único que comparten es el contrato. Mientras `GET /users` siga devolviendo lo prometido, el backend puede migrar de framework y el frontend de bundler sin coordinarse. El día que alguien renombra `nombre` a `name` "porque queda mejor", el frontend muestra `undefined` en producción — y ese incidente, no un documento de arquitectura, es lo que enseña que el contrato es rígido. Para aislar la esencia —que un endpoint es la combinación de una operación y un recurso— esta clase construye la forma canónica `GET /users` a partir de sus dos piezas.

## 🧮 Modelo

- **Entrada** (stdin): una línea `metodo recurso`
- **Salida** (stdout): `contrato=<METODO> /<recurso>`
- **Regla:** combinar método y recurso en un endpoint

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `GET users` | `contrato=GET /users` |
| `POST items` | `contrato=POST /items` |
| `PUT data` | `contrato=PUT /data` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER metodo, recurso ; ESCRIBIR metodo + ' /' + recurso
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys

metodo, recurso = sys.stdin.readline().split()
print(f"contrato={metodo} /{recurso}")
```

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const [metodo, recurso] = readFileSync(0, "utf8").trim().split(/\s+/);
console.log(`contrato=${metodo} /${recurso}`);
```

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const [metodo, recurso] = readFileSync(0, "utf8").trim().split(/\s+/);
console.log(`contrato=${metodo} /${recurso}`);
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
        System.out.println("contrato=" + p[0] + " /" + p[1]);
    }
}
```

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
Console.WriteLine($"contrato={p[0]} /{p[1]}");
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
	p := strings.Fields(line)
	fmt.Printf("contrato=%s /%s\n", p[0], p[1])
}
```

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let p: Vec<&str> = s.split_whitespace().collect();
    println!("contrato={} /{}", p[0], p[1]);
}
```

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    char metodo[16], recurso[64];
    if (scanf("%15s %63s", metodo, recurso) != 2) return 1;
    printf("contrato=%s /%s\n", metodo, recurso);
    return 0;
}
```

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL construye el endpoint por concatenacion.
WITH t(metodo, recurso) AS (VALUES ('GET', 'users'))
SELECT 'contrato=' || metodo || ' /' || recurso AS resultado FROM t;
```

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
[$metodo, $recurso] = preg_split('/\s+/', trim(fgets(STDIN)));
echo "contrato=$metodo /$recurso\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔎 Recorrido del código (laboratorio)

El caso `GET users` debe producir `contrato=GET /users`. Dos piezas sueltas —un verbo y un nombre de recurso— se combinan en la forma canónica que identifica una operación. Es exactamente lo que hace un enrutador HTTP al registrar una ruta: asocia el par (método, ruta) con un manejador.

En **Python**, `metodo, recurso = sys.stdin.readline().split()` desempaqueta las dos piezas y la f-string las une con `" /"`. Nota que el método se copia tal cual: si llegara `get` en minúsculas, la salida sería `contrato=get /users`. Los frameworks reales normalizan el verbo a mayúsculas porque HTTP los define sensibles a mayúsculas y `get` no es un método válido — un ejemplo diminuto de que un contrato no es solo la forma, también las reglas de validación que nadie escribió.

En **C**, `char metodo[16], recurso[64];` fija de antemano cuánto puede medir cada pieza, y `scanf("%15s %63s", ...)` las acota. Esa decisión —16 bytes para el verbo, 64 para el recurso— es un contrato en miniatura: si el cliente envía una ruta más larga, C la trunca en silencio. Los servidores HTTP reales tienen el mismo límite (una URL máxima de 8 KB es habitual) y devuelven `414 URI Too Long`. La diferencia entre truncar y rechazar es justo lo que un buen contrato debe especificar.

En **SQL**, `'contrato=' || metodo || ' /' || recurso` hace la misma concatenación de forma declarativa. Es el recordatorio de que una base de datos también publica un contrato: el nombre y tipo de las columnas de una vista. Renombrar una columna de una vista rompe a sus consumidores igual que renombrar un campo JSON, y por eso los equipos maduros tratan las vistas como API pública y las tablas como detalle interno.

## 🔬 Comparación

| Lenguaje | Cómo se define y consume un contrato de API |
|---|---|
| Python | FastAPI genera OpenAPI desde los *type hints*; `grpcio` para gRPC; `requests`/`httpx` como cliente. |
| JavaScript | Express/Fastify definen rutas a mano; `fetch` como cliente; `@grpc/grpc-js` para gRPC. |
| TypeScript | El contrato se puede tipar de extremo a extremo (tRPC, `openapi-typescript`): el compilador detecta la ruptura. |
| Java | Spring Boot con anotaciones (`@GetMapping`); JAX-RS; `protoc` genera *stubs* gRPC. |
| C# | ASP.NET Core Minimal APIs y controladores; `Grpc.AspNetCore` genera servidor y cliente. |
| Go | `net/http` con `ServeMux` en la stdlib; gRPC es ciudadano de primera (Google lo creó ahí). |
| Rust | `axum`/`actix-web` con extractores tipados; `tonic` para gRPC sobre `prost`. |
| C | Sin framework estándar: `libmicrohttpd` o similares; el contrato se escribe y se respeta a mano. |
| SQL | No expone HTTP: su contrato son vistas, funciones y procedimientos almacenados. |
| PHP | Laravel/Symfony enrutan por convención; PSR-7/PSR-15 estandarizan petición y respuesta. |

La diferencia sintáctica —`@GetMapping("/users")` frente a `mux.HandleFunc("GET /users", ...)`— es superficial. La semántica importante es **dónde vive la verdad del contrato**. En los lenguajes de tipado estático con generación de código (Java, C#, Go, Rust con gRPC; TypeScript con tRPC) el contrato está *en el compilador*: si el servidor cambia un campo, el cliente deja de compilar antes de desplegarse. En los dinámicos con REST y JSON, el contrato está en un documento, y la ruptura solo aparece en tiempo de ejecución, en producción, como un `undefined`. Newman propone cerrar ese hueco con **pruebas de contrato dirigidas por el consumidor** (Pact y similares): cada cliente declara qué espera, y el CI del servidor falla si deja de cumplirlo. Es la forma de recuperar en un sistema políglota la garantía que un compilador da dentro de un solo proceso.

## 🧬 El concepto en la familia

Los tres estilos dominantes resuelven el mismo problema con prioridades distintas. **REST sobre HTTP+JSON** gana en alcance: lo consume cualquier cosa con un cliente HTTP, se depura con `curl` y aprovecha cachés y proxies existentes; es el estándar de facto de las APIs públicas. **gRPC** gana en eficiencia y en seguridad de tipos, y por eso domina la comunicación *interna* entre servicios donde ambos extremos los controla la misma organización. **GraphQL** ataca un tercer problema —que el cliente pida exactamente los campos que necesita, evitando el *over-fetching* de REST— a costa de un servidor más complejo y de un cacheo más difícil. Y por debajo de todos sigue el patrón que Tanenbaum describe desde los años ochenta: la **RPC**, la ilusión de que llamar a algo remoto se parece a llamar a algo local. Una ilusión útil, pero que nunca es completa: lo remoto puede tardar, fallar a medias o no responder jamás, y ninguna sintaxis lo esconde.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 160
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Cambiar el contrato sin versionar** → causa: renombrar un campo o hacer obligatorio uno opcional rompe a todo cliente desplegado → solución: solo añadir de forma opcional; para cambios incompatibles, exponer `/v2` y mantener `/v1` hasta que nadie lo use.
- **Suponer que cliente y servidor se despliegan a la vez** → causa: en un sistema políglota conviven versiones distintas durante horas o meses → solución: diseñar para compatibilidad hacia atrás *y* hacia adelante, como en el capítulo 4 de Kleppmann.
- **Reintentar operaciones no idempotentes** → causa: una respuesta perdida hace que el cliente repita un `POST` y se cree el pedido dos veces → solución: usar verbos idempotentes o una clave de idempotencia que el servidor deduplique.
- **Filtrar el modelo interno en el contrato** → causa: serializar la entidad de la base de datos tal cual expone columnas privadas y ata el esquema interno a la API → solución: definir un DTO explícito de la frontera, separado del modelo de dominio.
- **Ignorar el contrato de errores** → causa: el cliente solo maneja el camino feliz y trata un `503` como si fueran datos válidos → solución: especificar los códigos y el formato de error, y manejarlos como parte de la API.

## ❓ Preguntas frecuentes

- **¿REST o gRPC?** REST para APIs públicas, heterogéneas o consumidas por navegadores: gana en alcance y depurabilidad. gRPC para tráfico interno de alto volumen entre servicios que controlas: gana en latencia, tamaño y comprobación de tipos. Muchos sistemas usan los dos, con gRPC dentro y una fachada REST hacia fuera.
- **¿Qué es un endpoint?** Un punto de acceso: el par (método, ruta) que identifica una operación. `GET /users` y `POST /users` comparten ruta pero son endpoints distintos porque la operación es distinta.
- **¿Versionar en la URL o en la cabecera?** `/v1/users` es explícito y trivial de enrutar y cachear; versionar por cabecera (`Accept: application/vnd.api.v1+json`) es más purista pero más fácil de olvidar. Lo importante no es cuál, sino tener alguno antes de necesitarlo.
- **¿Un esquema hace innecesarias las pruebas?** No. El esquema garantiza la *forma* (que el campo existe y es un entero), no el *significado* (que ese entero sea el importe en céntimos y no en euros). Las pruebas de contrato cubren lo segundo.
- **¿Puedo borrar un campo que "nadie usa"?** Solo si puedes demostrarlo con telemetría. En una API pública casi nunca puedes: la vía segura es marcarlo obsoleto, medir su uso, avisar y borrarlo mucho después.

## 🔗 Referencias

**Libros de la parte:**

- M. Kleppmann — *Designing Data-Intensive Applications* (O'Reilly). Cap. 4: modos de flujo de datos —bases de datos, servicios, mensajes— y compatibilidad hacia atrás y adelante.
- S. Newman — *Building Microservices* (2ª ed., O'Reilly). Interfaces tecnológicamente agnósticas, versionado y pruebas de contrato dirigidas por el consumidor.
- A. Tanenbaum y M. van Steen — *Distributed Systems* (3ª ed.). Cap. 4: RPC, semánticas de invocación y por qué lo remoto nunca es como lo local.

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

> [⏮️ Clase 159](../../parte-10-interoperabilidad-y-fronteras-entre-lenguajes/159-serializacion-entre-lenguajes-json-protobuf-messagepack/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 161 ⏭️](../../parte-10-interoperabilidad-y-fronteras-entre-lenguajes/161-procesos-y-comunicacion-stdin-stdout-sockets-colas/README.md)
