# Clase 154 — Mantenibilidad, documentación y deuda técnica

> Parte **9 — Ingeniería de software políglota** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

El software no se escribe una vez: se lee, se modifica y se reescribe durante años. McConnell recuerda en *Code Complete* que el código se lee muchas más veces de las que se escribe, y que por tanto **optimizar para el lector** —para el mantenedor futuro, que a menudo eres tú mismo dentro de seis meses— es la decisión económica correcta. La **mantenibilidad** es esa propiedad: cuán fácil resulta entender un sistema y cambiarlo sin romperlo. No es un lujo estético; es lo que determina el coste de cada funcionalidad futura.

Para hablar de por qué la mantenibilidad se degrada, Ward Cunningham acuñó en 1992 una de las metáforas más influyentes de la ingeniería de software: la **deuda técnica**. Igual que un préstamo financiero, tomar un atajo en el diseño te permite ir más rápido *hoy*, pero genera *intereses*: cada cambio posterior sobre ese código apresurado cuesta un poco más. La metáfora es precisa en un punto que se suele olvidar: Cunningham no dijo que la deuda fuera mala. Un préstamo consciente, contraído para entregar a tiempo y devuelto pronto mediante refactorización, es una herramienta legítima. Lo ruinoso es la deuda que nadie reconoce ni paga, cuyos intereses se acumulan hasta que el sistema se vuelve inmodificable. Hunt y Thomas dan a este proceso el nombre de **entropía del software** o *software rot* —«podredumbre»—: sin mantenimiento activo, el orden de un sistema decae hacia el caos, ventana rota tras ventana rota.

El ejercicio de esta clase es deliberadamente humilde —contar los módulos de un sistema— pero apunta a una idea real: la mantenibilidad se puede *medir*. El número de módulos, las líneas por función, la complejidad ciclomática o la duplicación son métricas que herramientas como SonarQube calculan para poner cifras a la deuda. Y la documentación —docstrings, Javadoc, rustdoc— es la otra mitad de la ecuación: código que explica su *porqué* baja la barrera para mantenerlo.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. **Definir** mantenibilidad y explicar por qué el código se optimiza para el lector.
2. **Explicar** la metáfora de la deuda técnica de Cunningham y distinguir deuda deliberada de deuda negligente.
3. **Relacionar** una métrica estructural simple (conteo de módulos) con la idea de complejidad medible.
4. **Nombrar** el sistema de documentación idiomático de cada lenguaje y qué documenta bien (el porqué, no el qué).

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Mantenibilidad | Determina el coste de todo cambio futuro |
| 2 | Deuda técnica | La metáfora de Cunningham: atajos con intereses |
| 3 | Entropía del software | Sin mantenimiento, el orden decae (Hunt y Thomas) |
| 4 | Documentación por lenguaje | El porqué, no el qué; docstrings, Javadoc, rustdoc… |

## 📖 Definiciones y características

La **mantenibilidad** es la facilidad con que el código se comprende, se cambia y se extiende sin introducir defectos. McConnell la desglosa en cualidades concretas —legibilidad, bajo acoplamiento, alta cohesión, nombres reveladores— porque son ellas, y no la elegancia superficial, las que abaratan el mantenimiento. Un nombre honesto de variable ahorra más horas a lo largo de la vida de un proyecto que cualquier truco ingenioso.

La **deuda técnica** es el coste futuro implícito de una solución rápida elegida hoy. La fuerza de la metáfora de Cunningham está en el *interés*: la deuda no es el atajo en sí, sino el sobrecosto que ese atajo impone a cada trabajo posterior sobre la misma zona. Fowler, ampliando la idea, la clasifica en un cuadrante (deliberada o inadvertida, prudente o imprudente): «no tuvimos tiempo de diseñarlo bien, lo arreglamos la semana que viene» es deuda prudente y deliberada; «¿qué es una capa?» es imprudente e inadvertida, la peor. El antídoto que propone toda la literatura de la parte es la **refactorización** continua: pagar la deuda en dosis pequeñas mientras trabajas, no en una gran reescritura que nunca llega.

La **documentación** explica lo que el código no puede decir por sí mismo: el *porqué*. McConnell y los pragmáticos coinciden en que documentar el *qué* —parafrasear lo que la línea siguiente ya dice— es ruido que envejece mal; documentar el *porqué* —qué decisión se tomó y contra qué alternativa— es información que el código nunca contiene. Cada lenguaje tiene su vehículo idiomático para esto, integrado con herramientas que generan referencia navegable a partir del propio fuente.

## 🧩 Situación

Heredas un servicio de facturación de cuarenta módulos sin apenas documentación. Cada cambio te obliga a leer medio sistema para no romper algo invisible; una corrección de una hora se convierte en tres días de arqueología. Eso es deuda técnica cobrando intereses. Empiezas a pagarla como recomienda Fowler: cada vez que tocas un módulo, le añades un docstring que explica su propósito y las decisiones no obvias, y extraes las funciones enredadas. No reescribes todo de golpe —eso sería suicida—, sino que mejoras lo que tocas. En paralelo, mides: un informe de SonarQube cuantifica la complejidad y la duplicación, y le da al equipo argumentos para pedir tiempo de refactorización. El ejercicio de esta clase —contar los módulos como métrica de estructura— es el germen de esa medición.

## 🧮 Modelo

- **Entrada** (stdin): una línea con nombres de módulos (palabras separadas por espacio)
- **Salida** (stdout): `complejidad=<número de módulos>`
- **Regla:** contar los módulos

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `a b c` | `complejidad=3` |
| `x` | `complejidad=1` |
| `a b c d e` | `complejidad=5` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER módulos ; ESCRIBIR cantidad
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

La versión de Python es casi un aforismo: `sys.stdin.read().split()` parte la entrada en palabras y `len(...)` las cuenta. Su virtud es la que esta clase predica —legibilidad—: cualquiera la entiende de un vistazo, y esa transparencia *es* mantenibilidad. En un módulo real, aquí colocarías un **docstring**: la cadena entre triples comillas justo bajo la definición de una función o módulo, que herramientas como Sphinx o `pydoc` convierten en documentación navegable, y que `help()` muestra en el intérprete. Ramalho insiste en *Fluent Python* en que el docstring documenta el contrato, no la implementación: qué recibe, qué devuelve y por qué, no cómo lo hace línea a línea.

```python
import sys

mods = sys.stdin.read().split()
print(f"complejidad={len(mods)}")
```

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const mods = readFileSync(0, "utf8").trim().split(/\s+/);
console.log(`complejidad=${mods.length}`);
```

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

En el ecosistema JavaScript/TypeScript la documentación idiomática es **JSDoc/TSDoc**: comentarios `/** ... */` con etiquetas `@param` y `@returns` sobre cada función. En TypeScript hay una sinergia notable que Cherny destaca en *Programming TypeScript*: el propio sistema de tipos ya documenta las firmas —`mods: string[]` dice más que un párrafo—, así que el comentario queda libre para explicar el *porqué*. La anotación de tipo no es solo verificación: es documentación que el compilador garantiza que no miente.

```typescript
import { readFileSync } from "node:fs";

const mods: string[] = readFileSync(0, "utf8").trim().split(/\s+/);
console.log(`complejidad=${mods.length}`);
```

### Java · [`java/Main.java`](implementaciones/java/Main.java) · `java Main.java`

Java popularizó la documentación generada a partir del código con **Javadoc**: comentarios `/** ... */` con `@param`, `@return` y `@throws` que la herramienta `javadoc` convierte en el HTML de referencia que todo programador Java ha consultado. Bloch, en *Effective Java*, hace de esto un ítem propio: «escribe comentarios de documentación para todos los elementos de API expuestos», porque una API sin Javadoc es, en la práctica, una API que nadie puede usar con confianza. La disciplina de documentar la frontera pública es parte de lo que hace mantenible un sistema Java grande.

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] mods = br.readLine().trim().split("\\s+");
        System.out.println("complejidad=" + mods.length);
    }
}
```

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;

string[] mods = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
Console.WriteLine($"complejidad={mods.Length}");
```

### Go · [`go/main.go`](implementaciones/go/main.go) · `go run main.go`

Go convierte la documentación en un acto casi gratuito: **godoc** no usa etiquetas especiales, sino los comentarios normales escritos justo encima de cada declaración. La convención cultural, que Donovan y Kernighan describen en *The Go Programming Language*, es que un comentario de documentación empiece con el nombre de lo que documenta —«Fields divide la cadena…»— y sea una frase completa. Esa sencillez deliberada baja tanto la barrera que documentar se vuelve el camino por defecto, no una tarea aparte.

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
	mods := strings.Fields(line)
	fmt.Printf("complejidad=%d\n", len(mods))
}
```

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

Rust lleva la documentación un paso más allá con **rustdoc**: los comentarios `///` se escriben en Markdown y, extraordinariamente, los ejemplos de código que incluyas se **compilan y ejecutan como tests** (`cargo test` los corre). Esto cierra la brecha clásica entre documentación y realidad: en Rust, un ejemplo documentado que deja de funcionar rompe la compilación de pruebas, así que la documentación no puede envejecer en silencio. Klabnik y Nichols muestran en *The Rust Programming Language* que esta integración —docs que son tests— es una de las mejores defensas contra la entropía documental que aquejan a otros ecosistemas.

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n = s.split_whitespace().count();
    println!("complejidad={n}");
}
```

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    char tok[256];
    int c = 0;
    while (scanf("%255s", tok) == 1) c++;
    printf("complejidad=%d\n", c);
    return 0;
}
```

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL: cuenta las filas (módulos).
WITH mods(nombre) AS (VALUES ('a'), ('b'), ('c'))
SELECT printf('complejidad=%d', count(*)) AS resultado FROM mods;
```

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
$mods = preg_split('/\s+/', trim(fgets(STDIN)));
echo "complejidad=" . count($mods) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Lenguaje | Documentación idiomática | Rasgo distintivo |
|---|---|---|
| Python | docstrings + Sphinx/pydoc | `help()` los muestra en vivo |
| JavaScript/TS | JSDoc/TSDoc (`/** */`) | los tipos de TS ya documentan las firmas |
| Java | Javadoc (`javadoc`) | referencia HTML estándar de la plataforma |
| C# | comentarios XML (`///`) + DocFX | integrados con IntelliSense |
| Go | godoc / pkg.go.dev | comentarios normales; convención de frase completa |
| Rust | rustdoc (`///`, Markdown) | los ejemplos se compilan y prueban |
| C | sin estándar; Doxygen de facto | documentación externa manual |
| SQL | comentarios `--`; sin generador estándar | el esquema documenta parte del dominio |
| PHP | PHPDoc (`/** */`) | base del autocompletado de los IDE |

Más allá de la documentación, la mantenibilidad se mide con herramientas transversales: **linters y formateadores** (ruff/black en Python, ESLint/Prettier en JS, gofmt en Go, rustfmt y Clippy en Rust, Checkstyle en Java) que imponen consistencia, y analizadores como **SonarQube** que cuantifican complejidad ciclomática, duplicación y «code smells» para poner cifras a la deuda técnica.

## 🧬 El concepto en la familia

La deuda técnica y la mantenibilidad se gestionan hoy con instrumentación automática. **SonarQube** y los linters miden complejidad ciclomática (cuántos caminos de ejecución tiene una función), duplicación de código y cobertura de pruebas, y muchos equipos fijan «puertas de calidad» que bloquean un *merge* si la deuda crece. En la cultura de equipo, la metáfora de la **ventana rota** de Hunt y Thomas —un desperfecto sin arreglar invita a más desperfectos— justifica la política de «no dejes el código peor de como lo encontraste» (la regla del *boy scout* de Robert Martin). Y la documentación viva —diagramas de arquitectura, ADRs (registros de decisiones de arquitectura), READMEs actualizados— combate la entropía a escala de proyecto, no solo de función. El hilo conductor es el de McConnell: la mantenibilidad no se hereda, se sostiene con disciplina continua.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 154
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Ignorar la deuda técnica** → causa: los intereses se acumulan hasta volver el código inmodificable → solución: pagarla en dosis pequeñas y continuas mientras trabajas (Fowler: refactorización constante)
- **Documentar el qué en vez del porqué** → causa: comentarios que parafrasean el código y envejecen mal → solución: explicar las decisiones y las alternativas descartadas, no repetir la línea siguiente
- **Reescritura total en vez de refactorización** → causa: la gran reescritura casi nunca se termina → solución: mejora lo que tocas (regla del boy scout)
- **Confundir toda deuda con algo malo** → causa: parálisis o culpa → solución: distinguir deuda prudente y deliberada de la negligente (cuadrante de Fowler); lo malo es no pagarla

## ❓ Preguntas frecuentes

- **¿La deuda técnica es siempre mala?** No. Cunningham la propuso como herramienta legítima: un préstamo consciente para entregar a tiempo, devuelto pronto. Lo dañino es la deuda que nadie reconoce ni paga.
- **¿Qué debo documentar?** El porqué de las decisiones, los supuestos y las alternativas descartadas. El qué suele leerse en el propio código; si necesita comentario, quizá el código debería ser más claro.
- **¿Cómo mido la mantenibilidad?** Con métricas como complejidad ciclomática, duplicación y cobertura (SonarQube, linters), y con la práctica: cuánto cuesta hacer un cambio típico.
- **¿Sirve de algo un docstring en un script de tres líneas?** En un script trivial, poco; en una API que otros usarán, es imprescindible (Bloch). La documentación es proporcional a la frontera pública.

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

> [⏮️ Clase 153](../../parte-9-ingenieria-de-software-poliglota/153-seguridad-entradas-memoria-y-dependencias/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 155 ⏭️](../../parte-10-interoperabilidad-y-fronteras-entre-lenguajes/155-por-que-los-sistemas-reales-son-poliglotas/README.md)
