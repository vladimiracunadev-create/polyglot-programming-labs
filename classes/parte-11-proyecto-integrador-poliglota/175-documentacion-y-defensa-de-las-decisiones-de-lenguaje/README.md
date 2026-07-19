# Clase 175 — Documentación y defensa de las decisiones de lenguaje

> Parte **11 — Proyecto integrador políglota** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Escribir la parte del proyecto que no se ejecuta y que, sin embargo, decide si el sistema sobrevive: la
**defensa razonada de las decisiones de lenguaje**. Un sistema políglota con cinco lenguajes es o bien una
obra de ingeniería —cada elección justificada por lo que ese componente necesita— o bien una colección de
caprichos acumulados por rotación de personal. Desde fuera, el código se ve exactamente igual en los dos
casos. Lo único que los distingue es la existencia de un documento que explique **por qué**.

Esa es la asimetría que hace tan valiosa esta clase. El código responde perfectamente a la pregunta *qué
hace el sistema*: es su descripción más precisa y siempre está actualizada, porque es la que se ejecuta.
Pero el código no puede responder *por qué es así y no de otra forma*, ni *qué alternativas se descartaron*,
ni *bajo qué supuestos la decisión sigue siendo válida*. Esa información existe solo en la cabeza de quien
decidió, y se evapora con el primer cambio de equipo. Hunt y Thomas, en *The Pragmatic Programmer*,
argumentan que la documentación debe vivir pegada al código y tratarse con la misma disciplina que él;
Newman añade en *Building Microservices* que en un sistema descompuesto lo que hay que documentar por
encima de todo son las **fronteras y sus razones**, porque nadie las ve leyendo un solo repositorio.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Medir la cobertura de la documentación por las decisiones registradas, no por su extensión.
2. Explicar por qué el *porqué* es lo único que el código no puede documentar por sí mismo.
3. Escribir un registro de decisión de arquitectura (ADR) que justifique la elección de un lenguaje.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Documentación | Explicar el porqué |
| 2 | Defensa de decisiones | Justificar cada lenguaje |
| 3 | Secciones | Cobertura del documento |

## 📖 Definiciones y características

La **documentación** de un sistema es su explicación escrita, y su valor está concentrado en la parte que
el código no puede dar: el contexto, las alternativas descartadas y las consecuencias aceptadas. La
**defensa de decisiones** es el género concreto que nos ocupa hoy: un argumento revisable —y por tanto
refutable— sobre por qué este componente está escrito en este lenguaje. Un **ADR** (*Architecture Decision
Record*) es su formato canónico: un documento breve, numerado e inmutable, con cuatro apartados —contexto,
decisión, alternativas consideradas y consecuencias— que se escribe cuando la decisión se toma y no se
edita después: si la decisión cambia, se escribe un ADR nuevo que anula al anterior. La **cobertura** mide
cuántas de las decisiones estructurales del sistema tienen su registro.

Que el registro sea inmutable es el detalle que más gente pasa por alto y el que más rendimiento da. Un
documento que se reescribe cada vez que cambia la realidad acaba describiendo solo el presente, y el
presente ya lo describe el código. Lo que no se puede reconstruir de ninguna otra forma es la **secuencia**:
qué sabíamos cuando elegimos Go para el servicio de ingesta, qué descartamos, qué esperábamos ganar. Con
esa secuencia, un ingeniero que llega dos años después puede hacer la única pregunta que importa —"¿siguen
siendo ciertos los supuestos?"— y decidir con fundamento si mantener o cambiar. Sin ella solo le quedan dos
malas opciones: respetar la decisión por superstición, o rehacerla desde cero por desconocimiento. La
segunda es la que produce reescrituras que repiten, una a una, los errores que la decisión original ya
había evitado.

Conviene además nombrar el criterio con el que se defiende un lenguaje, porque no es el gusto. Una
justificación sólida se apoya en lo que el componente exige: latencia y control de memoria (y entonces
Rust, C o Go tienen argumentos), riqueza de ecosistema para un dominio (Python en datos, TypeScript en el
navegador), garantías del compilador en una base grande y de larga vida (Java, C#), o expresividad
declarativa sobre conjuntos (SQL). Y se apoya, sobre todo, en un factor que no aparece en ninguna tabla
comparativa: qué lenguajes puede **mantener** el equipo que tienes. Un lenguaje técnicamente superior que
solo una persona domina es una decisión peor que uno mediocre que todos leen.

## 🧩 Situación

Llega un ingeniero nuevo al proyecto y encuentra el servicio de ingesta en Go, la API en TypeScript, el
motor de cálculo en Rust y las consultas en SQL. Su primera reacción es razonable: "esto es un
desastre, unifiquémoslo todo en un lenguaje". Si no hay documentación, no tiene forma de saber que Rust
está ahí porque el cálculo tardaba nueve minutos y ahora tarda veinte segundos, ni que la API es
TypeScript porque comparte los tipos del contrato con el frontend y eso eliminó una clase entera de bugs.
Con cuatro ADR de media página cada uno, esa misma conversación cambia de naturaleza: deja de ser una
opinión contra otra y pasa a ser una revisión de supuestos. Documentar no es burocracia; es lo que
convierte una discusión de gustos en una decisión de ingeniería.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n` (número de secciones documentadas)
- **Salida** (stdout): `documentado=<n> secciones`
- **Regla:** informar el número de secciones

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `documentado=5 secciones` |
| `1` | `documentado=1 secciones` |
| `8` | `documentado=8 secciones` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER n ; ESCRIBIR documentado=n secciones
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys

n = int(sys.stdin.readline())
print(f"documentado={n} secciones")
```

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`documentado=${n} secciones`);
```

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`documentado=${n} secciones`);
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
        System.out.println("documentado=" + n + " secciones");
    }
}
```

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;

int n = int.Parse(Console.In.ReadToEnd().Trim());
Console.WriteLine($"documentado={n} secciones");
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
	fmt.Printf("documentado=%d secciones\n", n)
}
```

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    println!("documentado={n} secciones");
}
```

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    printf("documentado=%ld secciones\n", n);
    return 0;
}
```

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL se documenta con comentarios; aqui, el conteo.
WITH t(n) AS (VALUES (5))
SELECT printf('documentado=%d secciones', n) AS resultado FROM t;
```

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
$n = (int) trim(fgets(STDIN));
echo "documentado=$n secciones\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🧪 Recorrido del código

El contrato ([`casos.json`](casos.json)) lee un entero y responde `documentado=<n> secciones`. Es la
implementación más escueta de la parte, y la elección no es casual: sirve para señalar que la
documentación se **cuenta** por decisiones registradas, no por páginas escritas. Cinco ADR de media página
cubren más sistema que cincuenta folios de descripción que repiten lo que el código ya dice.

La operación técnica es leer un número y formatearlo, y aun ahí hay algo que mirar: cada lenguaje decide
qué hacer cuando la entrada **no** es un número. **Python** lanza `ValueError` con `int()`; **Java** lanza
`NumberFormatException`; **C#** lanza `FormatException` con `int.Parse`; **Rust** devuelve un `Result` que
aquí se abre con `.unwrap()` y aborta si vino mal. Los cuatro fallan ruidosamente. En cambio **Go**
descarta el error con `n, _ := strconv.Atoi(...)` y sigue con `n = 0`, **PHP** convierte con `(int)` sin
protestar, y **JavaScript** devuelve `NaN` desde `parseInt` — un valor que se propaga silenciosamente por
todo el cálculo posterior. Ese contraste entre fallar pronto y seguir con un valor dudoso es una diferencia
semántica pura, y es exactamente el tipo de decisión que un ADR debería recoger cuando eliges el lenguaje
de un componente que valida entradas ajenas.

El detalle idiomático que cierra el recorrido está en cómo cada lenguaje mezcla texto y número.
**Python** interpola con `f"documentado={n} secciones"`, **Rust** con `println!("documentado={n} secciones")`
usando la captura directa de la variable en la plantilla, **Go** y **C** con especificadores `%d`/`%ld`, y
**SQL** con `printf` sobre una tabla de un solo caso. La misma frase, cinco maneras de componerla.

## 🔬 Comparación

Formatear un número dentro de una frase parece idéntico en todas partes; las diferencias aparecen en los
bordes, que es donde siempre viven.

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Interpolación (Python, JS/TS, C#, Rust, PHP), concatenación con `+` (Java), `Printf` con `%d` (Go, C), `printf` de SQLite (SQL). |
| Semántica | Ante una entrada no numérica, Python, Java, C# y Rust fallan de inmediato; Go ignora el error y usa el cero, PHP convierte a cero en silencio y JS produce `NaN`. El mismo programa, tres políticas de error distintas. |
| Paradigmática | Los imperativos leen un valor y lo formatean; SQL proyecta una columna calculada sobre una tabla — y su documentación natural no son comentarios sino el **esquema**: nombres de tablas, columnas y restricciones que describen el modelo. |

Hay un paralelismo que vale la pena hacer explícito. Los lenguajes con tipos estáticos y explícitos —Java,
C#, Rust, TypeScript— documentan una parte del *porqué* dentro del propio código: una firma que dice
`Result<Pedido, ErrorValidacion>` está declarando qué puede salir mal sin necesidad de un párrafo. Los
dinámicos —Python, JavaScript, PHP— trasladan esa carga a la documentación externa y a las convenciones.
No es que unos necesiten documentar y otros no: es que el límite entre lo que el código puede afirmar por
sí solo y lo que hay que escribir aparte **se mueve** según el lenguaje. Saber dónde está ese límite en
cada uno es parte de la competencia políglota.

## 🧬 El concepto en la familia

Cada ecosistema tiene su forma de documentación pegada al código: *docstrings* y Sphinx en Python, Javadoc
en la JVM, comentarios XML y DocFX en .NET, `godoc` —que en Go es tan central que la comunidad escribe los
comentarios pensando en cómo se leerán renderizados—, `rustdoc` con ejemplos que además se **ejecutan**
como pruebas, JSDoc y TypeDoc en JavaScript y TypeScript, phpDocumentor en PHP, y comentarios de esquema en
SQL. La documentación ejecutable de Rust es el caso límite interesante: un ejemplo en la documentación que
deja de compilar rompe la construcción, lo que ataca de raíz el problema de la documentación obsoleta. Por
encima de todos ellos está la capa que no pertenece a ningún lenguaje —README, ADR, diagramas— y que es la
única que puede hablar del sistema completo. En un proyecto políglota esa capa neutral no es opcional:
es el único lugar donde el sistema existe entero.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 175
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Documentar el qué en vez del porqué** → causa: se parafrasea el código en prosa (`// incrementa i`), que es la única parte que el lector ya podía obtener solo → solución: escribir lo que el código no puede decir: la razón, la alternativa descartada y el supuesto que sostiene la decisión.
- **Documentación desactualizada** → causa: vive en un wiki aparte que nadie toca al cambiar el código, y engaña más que la ausencia total → solución: mantenerla en el repositorio, revisarla en el mismo *pull request* que el cambio y, cuando el lenguaje lo permita, hacerla ejecutable (ejemplos que se compilan o se prueban).
- **Registrar solo las decisiones que salieron bien** → causa: se documenta como si fuera publicidad del proyecto → solución: un ADR debe incluir las consecuencias negativas aceptadas; si no las tiene, es que no se analizó la decisión, se justificó a posteriori.
- **Justificar un lenguaje por gusto o por moda** → causa: "es lo que quería probar" disfrazado de argumento técnico → solución: anclar la elección en un requisito verificable del componente (latencia, ecosistema, garantías del compilador) y en la capacidad real de mantenimiento del equipo.

## ❓ Preguntas frecuentes

- **¿Qué documentar?** Lo que se pierde si se va la persona que lo sabe: las fronteras entre componentes y sus contratos, las decisiones estructurales con su razón, los supuestos operativos y los procedimientos de recuperación ante fallos. El detalle de implementación se lee en el código y se documenta solo cuando es sorprendente.
- **¿Qué es un ADR?** Un documento corto y numerado que registra una decisión de arquitectura con su contexto, las alternativas consideradas y las consecuencias aceptadas. Se escribe en el momento de decidir, vive junto al código y no se edita: si la decisión cambia, un ADR posterior anula al anterior y la cadena queda como historia consultable.
- **¿Cómo defiendo un sistema políglota ante quien quiere unificarlo?** Con el argumento de coste, no de preferencia. Cada lenguaje añadido cuesta toolchain, CI, contratación y contexto mental; ese coste hay que pagarlo con un beneficio concreto y medible en el componente que lo justifica. Si puedes nombrar ese beneficio para cada lenguaje, tienes un sistema políglota; si no puedes, tienes uno accidental y quien quiere unificarlo tiene razón.

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

> [⏮️ Clase 174](../../parte-11-proyecto-integrador-poliglota/174-empaquetado-contenedores-y-despliegue/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 176 ⏭️](../../parte-11-proyecto-integrador-poliglota/176-cierre-retrospectiva-y-transferencia-a-nuevos-lenguajes/README.md)
