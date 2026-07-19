# Clase 164 — Elegir el lenguaje correcto para cada componente

> Parte **10 — Interoperabilidad y fronteras entre lenguajes** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Esta parte empezó constatando que los sistemas reales son políglotas (155) y ha recorrido las fronteras que lo hacen posible: FFI, ABI, bindings, serialización, contratos, canales, Wasm, intérpretes embebidos. Toca cerrar con la decisión que todo eso habilita —**elegir el lenguaje correcto para cada componente**— y con la advertencia que la acompaña.

Porque la conclusión honesta no es "usa el mejor lenguaje para cada cosa". Es más incómoda: **cada frontera tiene un coste, y ese coste hay que ganárselo**. Las ocho clases anteriores han sido, vistas juntas, un catálogo de lo que cuesta mezclar lenguajes — tipos que hay que emparejar a mano, datos que hay que serializar y copiar, contratos que se rompen al desplegar por separado, dos toolchains, dos ecosistemas de dependencias, dos culturas de código. Newman lo formula sin rodeos en *Building Microservices*: la libertad tecnológica es una de las ventajas reales de dividir un sistema, y también una de las que con más facilidad se convierte en un lastre operativo. El objetivo de esta clase es aprender a hacer esa elección como ingeniería —con criterios explícitos y contando el coste de la frontera— y no como preferencia.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. **Asociar** un tipo de componente con el lenguaje que mejor encaja.
2. **Justificar** la elección por la tarea, el equipo y el coste de la frontera.
3. **Aplicar** el criterio a un sistema real con varios componentes.
4. **Reconocer** cuándo *no* introducir otro lenguaje, aunque técnicamente encaje mejor.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Elegir por componente | El mejor lenguaje para cada parte |
| 2 | Fortalezas | Qué destaca cada lenguaje |
| 3 | Sistema políglota | Varias elecciones coherentes |

## 📖 Definiciones y características

La **idoneidad** de un lenguaje para un componente casi nunca la decide la elegancia del lenguaje. La deciden, por este orden, cuatro cosas.

La **plataforma** manda y a veces no deja elegir. En el navegador se ejecuta JavaScript o algo que compile a JS o a Wasm: no hay debate. En iOS nativo, Swift; en Android, Kotlin. Dentro de PostgreSQL, SQL más algún lenguaje procedural del motor. Antes de comparar méritos conviene ver cuántas opciones quedan realmente sobre la mesa; a menudo son una o dos.

El **ecosistema** decide casi todo lo demás. La razón por la que el aprendizaje automático se hace en Python no es que Python sea rápido —no lo es—, sino que NumPy, PyTorch y el resto están ahí y llevan quince años puliéndose. Elegir un lenguaje sin las bibliotecas del dominio significa reescribirlas, y ese coste supera cualquier ventaja de sintaxis o rendimiento. La pregunta útil no es "¿qué lenguaje me gusta más?" sino "¿qué tendría que construir yo mismo en cada opción?".

Las **propiedades de ejecución** entran cuando hay restricciones duras. Latencia predecible sin pausas de recolección de basura y control fino de memoria apuntan a Rust, C o C++ — un motor de audio o un sistema de trading no toleran una pausa de GC de 50 ms. Alta concurrencia de E/S con código simple apunta a Go o a runtimes asíncronos. Arranque en frío rápido para funciones sin servidor descarta lo que arranca una JVM. Y conviene medir: la mayoría de los servicios están limitados por E/S y base de datos, no por CPU, y ahí la diferencia entre lenguajes es mucho menor de lo que sugiere un microbenchmark.

El **equipo** es el criterio que más se ignora y más incidentes causa. Un lenguaje que nadie del equipo domina no solo se escribe más despacio: se depura mal a las tres de la mañana, se revisa peor y crea un punto único de fallo humano cuando la única persona que lo entiende se va. Newman recomienda por eso limitar deliberadamente el número de lenguajes de una organización a un conjunto pequeño y explícito, en lugar de dejar que cada equipo elija libremente. La libertad tecnológica es real, pero se ejerce dentro de una lista corta.

Sobre esos cuatro criterios se apoya la regla que resume la parte: **introducir otro lenguaje solo cuando el beneficio supere el coste de la nueva frontera**. Ese coste es concreto y medible — serializar y copiar datos, definir y versionar un contrato, dos toolchains y dos ficheros de dependencias, dos pipelines de CI, dos sistemas de vulnerabilidades que vigilar, y despliegues que ya no son atómicos. Reescribir en Rust un componente que consume el 2 % de la CPU es un mal negocio aunque Rust sea diez veces más rápido; hacerlo con el que consume el 60 % puede ser el mejor cambio del trimestre. La diferencia es aritmética, no ideológica.

- **Idoneidad** — cuánto encaja un lenguaje con una tarea. Clave: plataforma y ecosistema pesan más que la sintaxis o el rendimiento bruto.
- **Componente de sistemas** — cercano al hardware, con latencia acotada o memoria controlada. Clave: Rust y C encajan porque no hay pausas de GC.
- **Componente web/datos** — interfaz interactiva o consulta sobre datos. Clave: TypeScript por la plataforma, SQL porque el motor optimiza mejor que tu bucle.

## 🧩 Situación

Un sistema de análisis en tiempo real: el núcleo que procesa el flujo de eventos con latencia acotada se escribe en Rust; la API que lo expone, en Go, por su concurrencia sencilla y su despliegue como binario único; el panel de control, en TypeScript, porque corre en el navegador; los informes analíticos, en SQL, porque el motor optimiza la agregación mejor que cualquier bucle que escribas; y el entrenamiento de los modelos, en Python, por su ecosistema. Cinco lenguajes, cinco razones distintas y ninguna de ellas estética. Pero también cinco fronteras que mantener: un esquema Protobuf compartido, un contrato de API versionado, una cola entre el núcleo y la API, y dos pipelines de CI más. Elegir por componente es ingeniería justo cuando ese lado del balance se cuenta; deja de serlo cuando se ignora. Para aislar la decisión en su forma más pura, esta clase mapea un tipo de componente a un lenguaje recomendado.

## 🧮 Modelo

- **Entrada** (stdin): una palabra: `sistemas`, `web` o `datos`
- **Salida** (stdout): `lenguaje=<Rust|TypeScript|SQL>`
- **Regla:** sistemas→Rust, web→TypeScript, datos→SQL

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `sistemas` | `lenguaje=Rust` |
| `web` | `lenguaje=TypeScript` |
| `datos` | `lenguaje=SQL` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER tipo ; SEGUN tipo: recomendar lenguaje
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys

tipo = sys.stdin.readline().strip()
rec = {"sistemas": "Rust", "web": "TypeScript", "datos": "SQL"}
print(f"lenguaje={rec.get(tipo, 'Python')}")
```

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const tipo = readFileSync(0, "utf8").trim();
const rec = { sistemas: "Rust", web: "TypeScript", datos: "SQL" };
console.log(`lenguaje=${rec[tipo] ?? "Python"}`);
```

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const tipo: string = readFileSync(0, "utf8").trim();
const rec: Record<string, string> = { sistemas: "Rust", web: "TypeScript", datos: "SQL" };
console.log(`lenguaje=${rec[tipo] ?? "Python"}`);
```

### Java · [`java/Main.java`](implementaciones/java/Main.java) · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String tipo = br.readLine().trim();
        String r;
        switch (tipo) {
            case "sistemas": r = "Rust"; break;
            case "web": r = "TypeScript"; break;
            case "datos": r = "SQL"; break;
            default: r = "Python";
        }
        System.out.println("lenguaje=" + r);
    }
}
```

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;

string tipo = Console.In.ReadToEnd().Trim();
string r = tipo switch {
    "sistemas" => "Rust",
    "web" => "TypeScript",
    "datos" => "SQL",
    _ => "Python",
};
Console.WriteLine($"lenguaje={r}");
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
	tipo := strings.TrimSpace(line)
	rec := map[string]string{"sistemas": "Rust", "web": "TypeScript", "datos": "SQL"}
	r, ok := rec[tipo]
	if !ok {
		r = "Python"
	}
	fmt.Printf("lenguaje=%s\n", r)
}
```

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let tipo = s.trim();
    let r = match tipo {
        "sistemas" => "Rust",
        "web" => "TypeScript",
        "datos" => "SQL",
        _ => "Python",
    };
    println!("lenguaje={r}");
}
```

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char tipo[32];
    if (scanf("%31s", tipo) != 1) return 1;
    const char *r;
    if (strcmp(tipo, "sistemas") == 0) r = "Rust";
    else if (strcmp(tipo, "web") == 0) r = "TypeScript";
    else if (strcmp(tipo, "datos") == 0) r = "SQL";
    else r = "Python";
    printf("lenguaje=%s\n", r);
    return 0;
}
```

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL recomienda con CASE.
WITH t(tipo) AS (VALUES ('sistemas'))
SELECT printf('lenguaje=%s', CASE tipo WHEN 'sistemas' THEN 'Rust' WHEN 'web' THEN 'TypeScript' WHEN 'datos' THEN 'SQL' ELSE 'Python' END) AS resultado FROM t;
```

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
$tipo = trim(fgets(STDIN));
$rec = ["sistemas" => "Rust", "web" => "TypeScript", "datos" => "SQL"];
echo "lenguaje=" . ($rec[$tipo] ?? "Python") . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔎 Recorrido del código (laboratorio)

El caso `sistemas` debe producir `lenguaje=Rust`. Es un mapeo de una clave a un valor con un caso por defecto, y resulta un cierre feliz de la parte porque las diez implementaciones exhiben, cada una, la forma en que su lenguaje piensa la decisión.

En **Python**, `rec.get(tipo, 'Python')` fusiona la búsqueda y el valor por defecto en una sola expresión: el diccionario es la estructura de datos por defecto del lenguaje y `get` con segundo argumento es el modismo esperado. En **JavaScript y TypeScript**, `rec[tipo] ?? "Python"` hace lo mismo con el operador de coalescencia nula — y nota que se usa `??` y no `||`, distinción semántica real: `||` también sustituiría una cadena vacía o un `0`, mientras que `??` solo actúa ante `null` o `undefined`.

En **Go**, `r, ok := rec[tipo]` devuelve **dos** valores. Go no tiene valor por defecto en el acceso al mapa ni operador de coalescencia; te obliga a mirar el booleano `ok` y escribir el `if` explícito. Es el estilo del lenguaje llevado a un caso mínimo: pocas abstracciones, la ausencia se maneja a la vista. En **Rust**, el `match` sobre `&str` es una expresión, y el brazo `_ => "Python"` no es opcional — el compilador exige exhaustividad. Comparado con Go, la decisión no puede olvidarse; comparado con Python, no hay diccionario que construir en tiempo de ejecución.

En **Java** aparece el `switch` clásico con `break` en cada caso, y en **C#** el `switch` como expresión con `=>` y `_`. Los dos lenguajes son primos cercanos y la diferencia se ve nítida: C# ha incorporado el emparejamiento de patrones como expresión y Java lo ha hecho después. En **C**, `strcmp(tipo, "sistemas") == 0` recuerda que no hay comparación de cadenas con `==`: hay que llamar a una función y comparar contra cero, porque en C una cadena es un puntero. Y en **SQL**, `CASE tipo WHEN ... THEN ... ELSE ... END` es la forma declarativa: no hay flujo de control, hay una expresión que produce un valor por fila.

Diez formas de la misma decisión. Esa es, en miniatura, la tesis del curso entero: el concepto —mapear una clave a un valor con respaldo por defecto— es idéntico, y lo que cambia es cuánto te obliga cada lenguaje a hacer explícito.

## 🔬 Comparación

| Lenguaje | Dónde encaja mejor y por qué |
|---|---|
| Python | Datos, ciencia, ML y automatización: gana por ecosistema, no por velocidad. Cuando importa el rendimiento, delega en C. |
| JavaScript | El navegador, por obligación de plataforma; con Node, servicios ligeros y herramientas de front. |
| TypeScript | Front-end y BFF de cierto tamaño: los tipos reducen el coste de coordinar equipos y detectan rupturas de contrato al compilar. |
| Java | Sistemas empresariales grandes y longevos: madurez, herramientas de observabilidad y una reserva de talento enorme. |
| C# | Ecosistema Microsoft, back-ends web y juegos con Unity; muy similar a Java en el perfil de decisión. |
| Go | Servicios de red y CLIs: concurrencia sencilla, compilación rápida y un binario estático fácil de desplegar. |
| Rust | Núcleos de rendimiento, sistemas y componentes sin pausas de GC; también un buen objetivo de Wasm. |
| C | Sistemas operativos, embebidos y el papel de la clase 156: la ABI donde todos los lenguajes se encuentran. |
| SQL | Consulta y agregación de datos: el motor optimiza mejor que un bucle escrito a mano sobre las filas. |
| PHP | Web con CMS y aplicaciones consolidadas; el PHP moderno con tipado es muy distinto del de su mala fama. |

La diferencia paradigmática merece un comentario. SQL no está en esa lista como "un lenguaje más": es **declarativo**, y por eso permite que el motor reordene, indexe y paralelice sin que tú lo pidas. Una agregación de un millón de filas hecha en SQL suele ganar por goleada a la misma agregación hecha trayendo las filas al servicio y recorriéndolas — no porque SQL sea rápido, sino porque los datos no viajan y el planificador sabe más que tú sobre la distribución de la tabla. Esa es una diferencia paradigmática con consecuencias medibles, no una cuestión de gusto. El mismo razonamiento explica por qué elegir bien el lenguaje del componente de datos suele rendir más que optimizar el resto del sistema.

## 🧬 El concepto en la familia

La elección por componente es la tesis del programa. Los diez lenguajes del núcleo no son una lista arbitraria: cubren los terrenos donde hoy se toman las decisiones reales, y cada uno gana en el suyo por razones distintas —plataforma en el caso de JavaScript, ecosistema en el de Python, ejecución en el de Rust, paradigma en el de SQL, madurez organizativa en el de Java—. El Atlas amplía el mapa con las familias que no están en el núcleo pero que aparecen cuando el terreno cambia: Erlang y Elixir en sistemas que deben tolerar fallos y actualizarse en caliente; Haskell y OCaml donde el sistema de tipos debe descartar estados imposibles; R en estadística; Kotlin y Swift en móvil; Zig como alternativa a C. Y el patrón que se repite por encima de todos ellos es el que Newman y Kleppmann describen desde ángulos distintos: los sistemas grandes no eligen *un* lenguaje, eligen *fronteras*, y el lenguaje de cada lado se decide después. Aprender a ver esas fronteras —qué las cruza, qué cuesta, qué se rompe cuando cambian— es lo que esta parte ha intentado enseñar, y lo que la Parte 11 pone a prueba construyendo un sistema políglota completo.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 164
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Elegir por moda o por currículo** → causa: se adopta un lenguaje por interés personal y la organización carga con el mantenimiento durante años → solución: escribir la justificación en un registro de decisión (ADR) con los criterios de plataforma, ecosistema, ejecución y equipo.
- **Ignorar el coste de la frontera** → causa: se compara el rendimiento de dos lenguajes sin contar la serialización, el contrato, el despliegue extra y el CI adicional → solución: sumar el coste operativo a la comparación; muchas ganancias de CPU se las come la frontera.
- **Optimizar el componente equivocado** → causa: reescribir en Rust un módulo que consume el 2 % del tiempo → solución: medir dónde está el gasto real antes de decidir, y reescribir solo lo que domina el perfil.
- **Un solo lenguaje para todo, pase lo que pase** → causa: forzar la uniformidad lleva a reimplementar en el lenguaje corporativo lo que ya existe maduro en otro → solución: aceptar la excepción cuando el ecosistema o la plataforma no dejan alternativa.
- **Un lenguaje distinto por cada servicio** → causa: la libertad sin límite fragmenta el conocimiento, multiplica las cadenas de herramientas y hace imposible mover gente entre equipos → solución: una lista corta y explícita de lenguajes aprobados, con proceso para ampliarla.
- **Olvidar que la elección es a diez años** → causa: se decide pensando en escribirlo, no en mantenerlo, contratar para él y actualizar sus dependencias → solución: valorar madurez, tamaño de la comunidad y compromiso de compatibilidad, no solo la experiencia de desarrollo inicial.

## ❓ Preguntas frecuentes

- **¿Y si el equipo solo sabe un lenguaje?** Es un criterio legítimo y a menudo el decisivo. Un sistema mediocre que el equipo entiende y arregla a las tres de la mañana vale más que uno elegante que solo una persona sabe depurar. Introducir un lenguaje nuevo es también un plan de formación y de contratación.
- **¿No es más simple un solo lenguaje?** Operativamente sí, y esa simplicidad tiene un valor real que se subestima: una cadena de herramientas, un CI, un formato de dependencias, gente que rota entre equipos. Lo políglota gana cuando algún componente tiene una restricción que el lenguaje único no cubre — plataforma, ecosistema o latencia.
- **¿Cuántos lenguajes son demasiados?** No hay número mágico, pero sí una señal clara: cuando nadie puede revisar el código de otro equipo, o cuando actualizar una dependencia de seguridad requiere cinco procedimientos distintos, ya son demasiados.
- **¿Cómo justifico una elección ante el equipo?** Por escrito y con criterios comparables: qué restricciones impone la plataforma, qué habría que construir a mano en cada opción, qué exige la ejecución, quién lo va a mantener y qué cuesta la frontera nueva. Si la respuesta no cambia con el lenguaje, elige el que ya usáis.
- **¿Se puede migrar un componente después?** Sí, y es el mejor argumento a favor de fronteras bien diseñadas: si el contrato es estable, reescribir un servicio en otro lenguaje es invisible para sus clientes. Esa es la libertad real que Newman atribuye a los microservicios, y solo existe si el contrato se cuidó desde el principio.

## 🔗 Referencias

**Libros de la parte:**

- M. Kleppmann — *Designing Data-Intensive Applications* (O'Reilly). Elegir la herramienta según la carga de trabajo, y componer sistemas con piezas heterogéneas.
- S. Newman — *Building Microservices* (2ª ed., O'Reilly). Heterogeneidad tecnológica como beneficio y como coste; límites deliberados a la libertad de elección.
- A. Tanenbaum y M. van Steen — *Distributed Systems* (3ª ed.). Arquitecturas de sistemas y separación en componentes con interfaces estables.
- M. Nygard — *Release It!* (2ª ed., Pragmatic Bookshelf). Consecuencias operativas de cada frontera nueva en producción.

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

> [⏮️ Clase 163](../../parte-10-interoperabilidad-y-fronteras-entre-lenguajes/163-incrustar-un-lenguaje-en-otro-lua-python-embebido/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 165 ⏭️](../../parte-11-proyecto-integrador-poliglota/165-el-proyecto-un-sistema-con-componentes-en-varios-lenguajes/README.md)
