# Clase 148 — Entrega y despliegue

> Parte **9 — Ingeniería de software políglota** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Si la CI (clase 147) contesta "¿es correcto este cambio?", esta clase contesta la pregunta siguiente: "¿cómo lo llevamos a manos de los usuarios sin miedo?". Aquí conviene separar dos palabras que se confunden a diario. La **entrega** (delivery) es tener siempre un artefacto probado, versionado y *listo para desplegar*; el **despliegue** (deployment) es el acto concreto de ponerlo en producción. Puedes tener entrega continua —cada commit verde produce un artefacto publicable— y aun así decidir cuándo desplegarlo con un botón humano. El despliegue continuo va un paso más allá y automatiza también ese último salto. Hunt y Thomas resumen el principio subyacente en *The Pragmatic Programmer*: automatiza todo lo repetible, porque lo que se hace a mano se hace mal, tarde y de formas distintas cada vez.

El hilo conductor de la clase es la **trazabilidad**: saber exactamente qué código corre en producción. La herramienta más básica para ello es la **etiqueta de versión** (`v1.2.3`), una marca inmutable en el historial que ancla un artefacto a un punto preciso del código. El programa de `casos.json` reduce toda la ceremonia a su gesto mínimo —tomar una versión `mayor.menor.parche` y prefijarla con `v` para producir `desplegado=v1.2.3`—, pero detrás de ese prefijo está la diferencia entre poder decir "en producción corre exactamente el commit etiquetado `v1.2.3`" y encogerse de hombros cuando algo falla.

Entender esto te prepara para razonar sobre lo que de verdad importa en producción: entornos separados, estrategias que reducen el riesgo del cambio, contenedores que hacen el artefacto reproducible, y —sobre todo— la capacidad de volver atrás (rollback) cuando una versión resulta mala.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. **Distinguir** entrega (tener listo) de despliegue (poner en producción) y explicar por qué la separación importa.
2. **Etiquetar** una versión de forma trazable y justificar la convención `mayor.menor.parche`.
3. **Comparar** estrategias de despliegue (blue-green, canary, rolling) según su riesgo y su coste de rollback.
4. **Reconocer** el papel de los artefactos versionados, los entornos (dev/staging/prod) y los contenedores en un despliegue seguro.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Entrega vs. despliegue | Listo para publicar ≠ publicado |
| 2 | Artefacto y etiqueta de versión | Trazabilidad: qué corre en prod |
| 3 | Entornos dev/staging/prod | Probar antes de exponer a usuarios |
| 4 | Estrategias y rollback | Cambiar con red y poder volver atrás |

## 📖 Definiciones y características

- **Entrega continua (continuous delivery)** — la disciplina de mantener el software *siempre* en un estado desplegable: cada cambio que pasa la CI genera un artefacto versionado y validado, de modo que desplegar sea una decisión de negocio, no una odisea técnica. La clave es que el "no lo puedo desplegar hoy porque está a medias" deja de existir.
- **Despliegue (deployment)** — el acto de instalar y activar una versión concreta en un entorno. Puede ser manual (alguien aprueba y lanza) o automático (despliegue continuo). Distinguirlo de la entrega evita la confusión más común del área.
- **Artefacto versionado** — el paquete inmutable que se despliega (un binario, una imagen de contenedor, un `.jar`, una rueda de Python), identificado por una versión. Inmutable es la palabra clave: el mismo artefacto que pasó staging es el que llega a prod, bit a bit.
- **Etiqueta (tag)** — la marca `v1.2.3` en el historial de Git que fija un artefacto a un commit exacto. Sigue el versionado semántico: `mayor` para cambios incompatibles, `menor` para funciones nuevas compatibles, `parche` para correcciones. Es la ancla de la trazabilidad.
- **Entornos** — copias del sistema con propósitos distintos: `dev` para desarrollar, `staging` para ensayar en condiciones casi reales, `prod` para los usuarios. El cambio avanza por ellos como por esclusas, ganando confianza antes de tocar a nadie.
- **Estrategias de despliegue** — **blue-green** mantiene dos entornos idénticos y conmuta el tráfico de golpe (rollback = volver a conmutar); **canary** dirige primero una fracción del tráfico a la versión nueva y la amplía si se comporta; **rolling** reemplaza instancias poco a poco. **Contenedores** (Docker) empaquetan el artefacto con su entorno para que corra igual en todas partes, y el **rollback** es la capacidad de restaurar rápido la versión anterior conocida-buena.

## 🧩 Situación

Tu equipo acaba de fusionar un cambio que pasó toda la CI. El pipeline de CD construye una imagen de contenedor, la etiqueta como `v1.2.3` y la publica en el registro: eso es la *entrega*, el artefacto ya existe y es trazable. Un ingeniero de guardia decide desplegar por canary: el 5 % del tráfico va a `v1.2.3` mientras el resto sigue en `v1.2.2`. Los tableros muestran latencia y errores estables durante quince minutos, así que se amplía al 50 % y luego al 100 %. Si en cualquier momento los errores se hubieran disparado, el rollback habría sido inmediato —redirigir el tráfico de vuelta a `v1.2.2`, la última versión conocida-buena— porque la etiqueta permite saber exactamente a qué volver. Ese pequeño `desplegado=v1.2.3` que produce el programa de esta clase es, literalmente, el eslabón que hace posible toda esa maniobra.

## 🧮 Modelo

- **Entrada** (stdin): una línea con una versión `mayor.menor.parche`
- **Salida** (stdout): `desplegado=v<versión>`
- **Regla:** prefijar la versión con 'v'

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `1.2.3` | `desplegado=v1.2.3` |
| `0.9.0` | `desplegado=v0.9.0` |
| `2.1.5` | `desplegado=v2.1.5` |

## 📐 Algoritmo (pseudocódigo neutral)

El gesto es mínimo pero cargado de sentido: tomar la versión y anteponerle la marca que la vuelve una etiqueta reconocible.

```text
LEER version ; ESCRIBIR 'desplegado=v' + version
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

El problema es, en el fondo, una concatenación con formato, y ahí Python brilla con las f-strings. `sys.stdin.readline().strip()` lee la única línea y le quita el salto final; la f-string `f"desplegado=v{version}"` inserta la versión ya limpia justo después del prefijo `v`. Ramalho, en *Fluent Python*, presenta las f-strings como la forma preferente de interpolar en Python moderno por ser legibles y eficientes: el texto plantilla y los valores conviven a la vista, sin `+` ni `%` que estorben.

```python
import sys

version = sys.stdin.readline().strip()
print(f"desplegado=v{version}")
```

Para `1.2.3`, `version` vale `"1.2.3"` y la salida es `desplegado=v1.2.3`. El `strip()` es la parte silenciosamente importante: sin él, el `\n` de stdin viajaría dentro de la etiqueta y rompería la comparación con `casos.json`.

### Java · `java Main.java`

Java contrasta por su ceremonia: no hay lectura de una línea "de una", sino el trío `BufferedReader` + `InputStreamReader` + `System.in`, la escalera clásica de la E/S de la plataforma. La concatenación usa el operador `+` sobre `String`, que Bloch analiza en *Effective Java*: es cómodo para unir dos piezas como aquí, aunque desaconseje encadenar muchas en bucle por el coste. `br.readLine().trim()` cumple el mismo papel que el `strip()` de Python.

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String version = br.readLine().trim();
        System.out.println("desplegado=v" + version);
    }
}
```

### SQL · `sqlite3 :memory: < main.sql`

SQL hace explícito el otro rostro de la misma operación: la concatenación como cómputo declarativo. El operador estándar `||` une el literal `'desplegado=v'` con la columna `v` de una tabla de una sola fila. No hay "leer una línea"; hay una relación con un valor y una proyección que lo transforma. Date, en *SQL and Relational Theory*, recuerda que en el modelo relacional todo es evaluación de expresiones sobre relaciones, y algo tan mundano como añadir un prefijo se piensa como un `SELECT` que proyecta una nueva columna.

```sql
-- SQL: concatena el prefijo con ||.
WITH t(v) AS (VALUES ('1.2.3'))
SELECT 'desplegado=v' || v AS resultado FROM t;
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const version = readFileSync(0, "utf8").trim();
console.log(`desplegado=v${version}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const version: string = readFileSync(0, "utf8").trim();
console.log(`desplegado=v${version}`);
```

### C# · `dotnet run`

```csharp
using System;

string version = Console.In.ReadToEnd().Trim();
Console.WriteLine($"desplegado=v{version}");
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
	version := strings.TrimSpace(line)
	fmt.Printf("desplegado=v%s\n", version)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let version = s.trim();
    println!("desplegado=v{version}");
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    char version[64];
    if (scanf("%63s", version) != 1) return 1;
    printf("desplegado=v%s\n", version);
    return 0;
}
```

### PHP · `php main.php`

```php
<?php
$version = trim(fgets(STDIN));
echo "desplegado=v$version\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

El ejercicio es una concatenación en todos, pero el *artefacto* que cada ecosistema publica al desplegar difiere de raíz, y con él la herramienta de versionado y el registro donde acaba.

| Lenguaje | Artefacto típico | Se publica en |
|---|---|---|
| Python | rueda `.whl` / imagen | PyPI, registro de contenedores |
| JavaScript/TS | paquete npm / bundle | npm registry, CDN |
| Java | `.jar` / `.war` | Maven Central, Nexus/Artifactory |
| C# | paquete NuGet / binario | NuGet, registro |
| Go | binario estático | release de GitHub, imagen |
| Rust | crate / binario | crates.io, imagen |
| C | binario / biblioteca | paquete del SO |
| SQL | scripts de migración | control de versiones |
| PHP | paquete Composer | Packagist |

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Concatenación con f-string, `+`, `\|\|` o interpolación. |
| Semántica | La etiqueta identifica de forma única la versión desplegada. |
| Paradigmática | SQL concatena con `\|\|` sobre una relación, no sobre una línea leída. |

## 🧬 El concepto en la familia

La entrega y el despliegue versionados no son idea de una herramienta concreta: los `git tag` y las *releases* de GitHub anclan artefactos a commits; los registros de contenedores guardan imágenes por etiqueta; herramientas de CD como Argo CD o Spinnaker orquestan blue-green y canary sobre Kubernetes; y en móvil, las tiendas gestionan despliegues escalonados por porcentaje de usuarios. En todas, dos constantes se repiten: la versión inmutable como fuente de verdad y el rollback como derecho irrenunciable.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 148
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Desplegar sin etiquetar** → causa: no poder saber qué código corre en producción → solución: etiquetar cada release con versión semántica.
- **Desplegar sin pasar el CI** → causa: llevar código roto a los usuarios → solución: desplegar solo artefactos que estén verdes.
- **No preparar el rollback** → causa: ante un fallo, no hay a dónde volver rápido → solución: conservar la versión anterior conocida-buena y ensayar el rollback.

## ❓ Preguntas frecuentes

- **¿Entrega o despliegue continuo?** La entrega continua deja el software *listo* para desplegar en cualquier momento; el despliegue continuo lo publica automáticamente sin intervención humana.
- **¿Por qué el prefijo 'v'?** Es la convención dominante para distinguir a simple vista una etiqueta de versión (`v1.2.3`) de otras etiquetas del historial.
- **¿Blue-green o canary?** Blue-green cambia todo de golpe (rollback instantáneo, pero coste de mantener dos entornos); canary expone la versión nueva de forma gradual y detecta problemas con impacto acotado. Se eligen según el riesgo tolerable.

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

> [⏮️ Clase 147](../../parte-9-ingenieria-de-software-poliglota/147-integracion-continua-ci-multi-lenguaje/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 149 ⏭️](../../parte-9-ingenieria-de-software-poliglota/149-diseno-y-arquitectura-comparada/README.md)
