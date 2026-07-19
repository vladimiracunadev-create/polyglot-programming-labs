# Clase 142 — Registro (logging) y observabilidad

> Parte **9 — Ingeniería de software políglota** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

El depurador de la clase anterior sirve mientras tienes el programa delante; en producción, con miles de peticiones concurrentes y sin poder pausar nada, tu única ventana al interior del sistema es lo que el propio programa haya dejado escrito. Ese rastro es el **registro (logging)**, y saber leerlo y producirlo es lo que separa "no sé qué pasó" de "aquí está la línea exacta". McConnell, en *Code Complete*, trata la instrumentación como parte del oficio, no como un añadido: un programa que no cuenta lo que hace es una caja negra imposible de operar.

La unidad básica es un log con dos ingredientes: un **nivel** que expresa su gravedad —DEBUG, INFO, WARN, ERROR— y unos **datos** que describen el evento. Nuestro ejercicio produce la línea mínima `log=[INFO] procesados=n`: un nivel y un dato. Parece poco, pero encierra la decisión clave del logging moderno —el **logging estructurado**—, donde cada registro es un conjunto de campos legibles por máquina (`procesados=5`) y no una frase suelta. Sobre esa base se construye la **observabilidad**: la capacidad de entender el estado interno de un sistema desde sus salidas, articulada en los tres pilares clásicos —logs, métricas y trazas— que permiten operar en producción sin adivinar.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. **Emitir** un registro con su nivel y sus datos en un formato estructurado.
2. **Distinguir** los niveles DEBUG, INFO, WARN y ERROR y elegir el correcto para cada evento.
3. **Explicar** la observabilidad y sus tres pilares (logs, métricas, trazas).
4. **Identificar** la biblioteca de logging idiomática de cada lenguaje del núcleo.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Logging estructurado | Registros con campos legibles por máquina, no frases sueltas, se pueden consultar |
| 2 | Niveles | DEBUG/INFO/WARN/ERROR permiten filtrar por gravedad y bajar el ruido |
| 3 | Observabilidad | Los tres pilares (logs, métricas, trazas) hacen operable un sistema en marcha |
| 4 | Bibliotecas por lenguaje | Cada ecosistema tiene su estándar (logging, SLF4J, slog, tracing…) |

## 📖 Definiciones y características

- **Log.** Mensaje que registra un evento del programa junto al momento y el contexto en que ocurrió. Es la caja negra del avión: cuando algo falla en producción, el log es lo que reconstruye la secuencia. McConnell insiste en que un buen log dice *qué* pasó y *con qué datos*, no solo "error aquí".
- **Nivel de log.** La gravedad del mensaje, en una escala convencional: **DEBUG** (detalle fino para desarrollo), **INFO** (hitos normales, como nuestro `procesados=5`), **WARN** (algo anómalo pero recuperable) y **ERROR** (fallo que exige atención). El nivel permite filtrar: en producción sueles emitir de INFO hacia arriba y activar DEBUG solo al investigar.
- **Logging estructurado.** En lugar de una frase (`"se procesaron 5 elementos"`), se emiten campos (`procesados=5`, o un JSON `{"procesados":5}`). La diferencia es enorme: los campos se filtran, agregan y grafican en herramientas como Grafana Loki o Elastic, mientras que el texto libre solo se puede leer a ojo.
- **Observabilidad.** La capacidad de inferir el estado interno de un sistema a partir de lo que emite, sin acceder a su interior. Se apoya en tres pilares complementarios: **logs** (eventos discretos), **métricas** (números agregados en el tiempo, como peticiones por segundo) y **trazas** (el viaje de una petición a través de varios servicios).

## 🧩 Situación

Son las tres de la madrugada y el servicio de pedidos ha empezado a tardar. No puedes conectar un depurador —pausarías a miles de usuarios—, así que abres el panel de logs. Filtras por nivel WARN y aparece una línea repetida: `[WARN] cola_reintentos procesados=0`. En segundos sabes que los reintentos no avanzan, algo que un mensaje de texto plano habría enterrado en el ruido. Un registro estructurado como `[INFO] procesados=5` es exactamente lo que hace posible esa consulta: campos, no prosa.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n` (elementos procesados)
- **Salida** (stdout): `log=[INFO] procesados=<n>`
- **Regla:** emitir un registro de nivel INFO con el conteo

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `log=[INFO] procesados=5` |
| `0` | `log=[INFO] procesados=0` |
| `3` | `log=[INFO] procesados=3` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER n ; ESCRIBIR log de nivel INFO con procesados=n
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/). Para que la salida sea verificable byte a byte, aquí construimos el log a mano con un `print`, en vez de invocar la biblioteca de logging real de cada lenguaje; pero la forma del mensaje —nivel entre corchetes y un campo `clave=valor`— imita deliberadamente lo que esas bibliotecas producen.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys

n = int(sys.stdin.readline())
print(f"log=[INFO] procesados={n}")
```

La línea `f"log=[INFO] procesados={n}"` es un log estructurado en miniatura: `[INFO]` es el nivel y `procesados={n}` es un campo con clave y valor. En un servicio real no lo escribirías así, sino con el módulo estándar `logging`: `logging.info("procesados=%d", n)`, que además añadiría el *timestamp*, el nombre del módulo y respetaría el nivel configurado —si el umbral fuera WARNING, este INFO ni se emitiría—. Esa es la ventaja de una biblioteca frente al `print`: el mismo código de aplicación produce más o menos detalle según la configuración del entorno, sin tocar la lógica. Ramalho, en *Fluent Python*, recomienda `logging` sobre `print` justo por eso: separa *qué* quieres registrar de *cuánto* se registra en cada despliegue.

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`log=[INFO] procesados=${n}`);
```

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`log=[INFO] procesados=${n}`);
```

### Java · [`java/Main.java`](implementaciones/java/Main.java) · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        System.out.println("log=[INFO] procesados=" + n);
    }
}
```

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;

int n = int.Parse(Console.In.ReadToEnd().Trim());
Console.WriteLine($"log=[INFO] procesados={n}");
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
	n, _ := strconv.Atoi(strings.TrimSpace(line))
	fmt.Printf("log=[INFO] procesados=%d\n", n)
}
```

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    println!("log=[INFO] procesados={n}");
}
```

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    printf("log=[INFO] procesados=%ld\n", n);
    return 0;
}
```

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL: registro con una tabla/consulta de auditoría.
WITH t(n) AS (VALUES (5))
SELECT printf('log=[INFO] procesados=%d', n) AS resultado FROM t;
```

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
$n = (int) trim(fgets(STDIN));
echo "log=[INFO] procesados=$n\n";
```

En un sistema real, cada uno de estos programas delegaría el registro en la biblioteca canónica de su ecosistema, y el contraste es instructivo. **Java** rara vez usa `System.out.println` para logs: emplea la fachada **SLF4J** con una implementación como **Logback** por debajo, de modo que el código depende de una interfaz y la configuración decide el destino y el formato —una aplicación directa del principio de programar contra abstracciones que defiende Bloch. **Go** incorpora desde la versión 1.21 el paquete **`log/slog`** en la biblioteca estándar, con logging estructurado nativo (`slog.Info("procesado", "n", n)`), superando al viejo `log` de solo texto. **Rust** favorece la fachada **`tracing`** (o `log`), que unifica logs y trazas de spans en un mismo modelo, muy alineado con la observabilidad moderna. **JavaScript** va de `console.log` en desarrollo a bibliotecas como **pino** o **winston** en producción, que serializan a JSON de alto rendimiento. Distintas casas, la misma idea: nivel, campos estructurados y un destino configurable.

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

El concepto de niveles es universal; lo que cambia es la biblioteca estándar de cada ecosistema y si el logging estructurado viene de fábrica.

| Lenguaje | Biblioteca de referencia | ¿Estructurado nativo? | Llamada idiomática |
|---|---|---|---|
| Python | `logging` (estándar) | Parcial (vía `extra`/handlers) | `logging.info("procesados=%d", n)` |
| JavaScript | pino / winston (`console` en dev) | Sí (JSON) | `logger.info({ procesados: n })` |
| TypeScript | pino / winston | Sí (JSON) | `logger.info({ procesados: n })` |
| Java | SLF4J + Logback / Log4j 2 | Sí (con encoders) | `log.info("procesados={}", n)` |
| C# | `Microsoft.Extensions.Logging` / Serilog | Sí | `logger.LogInformation("procesados={N}", n)` |
| Go | `log/slog` (estándar, 1.21+) | Sí | `slog.Info("proc", "n", n)` |
| Rust | `tracing` / `log` | Sí | `info!(procesados = n)` |
| C | syslog / bibliotecas propias | No | `syslog(LOG_INFO, "...")` |
| SQL | tablas de auditoría / logs del motor | según motor | `INSERT INTO auditoria …` |
| PHP | Monolog (estándar de facto, PSR-3) | Sí | `$log->info('proc', ['n' => $n])` |

Dos observaciones útiles. La primera: los lenguajes modernos convergen hacia el logging *estructurado* de serie —`slog` en Go, `tracing` en Rust, la abstracción `ILogger` en .NET—, reconociendo que un log que una máquina puede consultar vale mucho más que uno que solo un humano puede leer. La segunda: PHP estandarizó su ecosistema con **PSR-3**, una interfaz común que Monolog y otros implementan, de modo que cambiar de biblioteca no rompe el código de aplicación; es la misma idea de fachada que Java resolvió con SLF4J.

## 🧬 El concepto en la familia

SLF4J/Logback y Log4j 2 (Java), `logging` (Python), Serilog y `Microsoft.Extensions.Logging` (.NET), `slog` y zap (Go), `tracing` (Rust), Monolog (PHP), pino y winston (Node): todos son variaciones del mismo modelo —un evento con nivel, mensaje y campos, dirigido a uno o varios destinos configurables—. Por encima de ellos, la observabilidad los integra con métricas y trazas distribuidas mediante estándares como OpenTelemetry, que unifica cómo los servicios exportan estas tres señales.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 142
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Loggear demasiado.** Un torrente de mensajes en el nivel equivocado ahoga la señal en ruido y encarece el almacenamiento. Usa DEBUG para el detalle y súbelo a INFO o WARN solo cuando el evento importe de verdad.
- **Loggear datos sensibles.** Contraseñas, tokens, números de tarjeta o datos personales en un log son una fuga de seguridad y a menudo una infracción legal. Redacta o excluye esos campos antes de registrar.
- **Texto libre en vez de campos.** `"procesé 5 pedidos del usuario 12"` es imposible de consultar; `procesados=5 usuario=12` se filtra y agrega. Prefiere siempre el formato estructurado.
- **Confiar en `print` en producción.** `print`/`console.log` no tienen niveles ni destino configurable y suelen ir a `stdout` sin control. Usa la biblioteca de logging del lenguaje, que separa qué registras de cuánto se emite.

## ❓ Preguntas frecuentes

- **¿Log o depurador?** El depurador es para el desarrollo, cuando tienes el programa delante y puedes pausarlo; el log es para producción, donde solo cuentas con lo que el sistema dejó escrito. Son complementarios, no alternativos.
- **¿Qué es la observabilidad?** La capacidad de entender un sistema en marcha desde sus salidas, apoyada en tres pilares: logs (eventos), métricas (números en el tiempo) y trazas (el recorrido de una petición entre servicios).
- **¿Por qué logging estructurado y no frases?** Porque los campos (`procesados=5`) se filtran, agregan y grafican en las herramientas de observabilidad, mientras que el texto libre solo se lee a ojo. Estructurar el log es lo que lo convierte en dato consultable.

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

> [⏮️ Clase 141](../../parte-9-ingenieria-de-software-poliglota/141-depuradores-gdb-lldb-pdb-y-los-de-ide/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 143 ⏭️](../../parte-9-ingenieria-de-software-poliglota/143-dependencias-versiones-y-lockfiles/README.md)
