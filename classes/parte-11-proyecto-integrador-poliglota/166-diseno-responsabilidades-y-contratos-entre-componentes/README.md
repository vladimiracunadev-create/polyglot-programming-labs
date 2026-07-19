# Clase 166 — Diseño: responsabilidades y contratos entre componentes

> Parte **11 — Proyecto integrador políglota** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Con el inventario en la mano (clase 165), el siguiente acto de diseño es definir **cómo se hablan** las
piezas: sus **responsabilidades** y los **contratos** en sus fronteras. Un contrato es la promesa que un
componente le hace a los demás sobre qué datos ofrece y en qué formato. Dos componentes encajan si —y solo
si— respetan el mismo contrato en la costura que los une. Esta clase reduce esa idea a su núcleo
comprobable: dados los valores de contrato de dos lados, decidir si son `compatible` o `incompatible`.

La razón por la que esto importa es la razón por la que existen los microservicios. Newman dedica capítulos
enteros a los contratos porque son lo que permite que un equipo cambie su servicio sin coordinar una
reunión con los otros diez equipos. Si el backend y el frontend comparten un contrato explícito, cada uno
evoluciona a su ritmo mientras la promesa se mantenga. El día que alguien cambia el contrato sin avisar,
la integración se rompe en producción —no en el compilador—, que es el peor lugar donde puede romperse.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Comprobar si dos lados de una frontera son compatibles comparando sus contratos.
2. Explicar por qué un contrato explícito **desacopla** a los componentes y les deja evolucionar.
3. Reconocer las fronteras de un sistema y saber que ahí es donde hay que poner las pruebas.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Contrato | La promesa que gobierna la frontera |
| 2 | Compatibilidad | Emisor y receptor esperan lo mismo |
| 3 | Responsabilidad | Lo que un componente hace define lo que expone |

## 📖 Definiciones y características

Un **contrato de frontera** es el acuerdo de datos y formato entre dos componentes; su valor, dice Newman,
es que hace posible el cambio independiente: mientras la promesa se cumpla, cada lado es libre por dentro.
La **compatibilidad** es la propiedad de que emisor y receptor entienden lo mismo por lo mismo; sin ella la
integración falla, y falla tarde. La **responsabilidad** es la tarea única de un componente y es lo que
determina qué expone: un servicio que "posee" los precios es el único que puede prometer cómo se ven.

Nygard, en *Release It!*, mira el mismo objeto desde el otro lado y lo llama **punto de integración**: cada
frontera es a la vez una promesa y un riesgo, el lugar por donde un sistema estable se contagia de la
inestabilidad del vecino. Por eso el contrato no es burocracia: es la unidad de diseño que decide si tu
sistema se puede mantener. Comprobar la compatibilidad —lo que hace el código de esta clase— es la versión
mínima de lo que la industria llama *contract testing* (Pact): verificar la frontera sin arrancar todo el
sistema.

## 🧩 Situación

El backend produce un formato —digamos, un JSON con un campo `total`— y el frontend lo consume esperando
ese mismo campo. Mientras ambos coincidan, encajan. Un día el backend renombra `total` a `amount` "porque
queda más limpio"; compila, pasa sus tests unitarios, se despliega… y el frontend deja de mostrar el
precio. Nada se cayó: simplemente el contrato se rompió en silencio. La comparación de contratos de esta
clase (`compatible` si los dos lados coinciden) es la forma más pequeña de atrapar ese fallo **antes** de
que llegue al usuario, y es el motivo por el que las pruebas de contrato viven en la frontera y no dentro
de cada servicio.

## 🧮 Modelo

- **Entrada** (stdin): una línea `a b` (los valores de contrato de cada componente)
- **Salida** (stdout): `contrato=<compatible|incompatible>`
- **Regla:** compatible si a == b

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5 5` | `contrato=compatible` |
| `5 6` | `contrato=incompatible` |
| `0 0` | `contrato=compatible` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER a, b ; compatible <- (a == b)
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys

a, b = sys.stdin.readline().split()
print(f"contrato={'compatible' if a == b else 'incompatible'}")
```

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const [a, b] = readFileSync(0, "utf8").trim().split(/\s+/);
console.log(`contrato=${a === b ? "compatible" : "incompatible"}`);
```

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const [a, b] = readFileSync(0, "utf8").trim().split(/\s+/);
console.log(`contrato=${a === b ? "compatible" : "incompatible"}`);
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
        System.out.println("contrato=" + (p[0].equals(p[1]) ? "compatible" : "incompatible"));
    }
}
```

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
Console.WriteLine($"contrato={(p[0] == p[1] ? "compatible" : "incompatible")}");
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
	f := strings.Fields(line)
	res := "incompatible"
	if f[0] == f[1] {
		res = "compatible"
	}
	fmt.Printf("contrato=%s\n", res)
}
```

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let v: Vec<&str> = s.split_whitespace().collect();
    let res = if v[0] == v[1] { "compatible" } else { "incompatible" };
    println!("contrato={res}");
}
```

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char a[64], b[64];
    if (scanf("%63s %63s", a, b) != 2) return 1;
    printf("contrato=%s\n", strcmp(a, b) == 0 ? "compatible" : "incompatible");
    return 0;
}
```

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL compara los valores de contrato.
WITH t(a, b) AS (VALUES (5, 5))
SELECT printf('contrato=%s', CASE WHEN a = b THEN 'compatible' ELSE 'incompatible' END) AS resultado FROM t;
```

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
[$a, $b] = preg_split('/\s+/', trim(fgets(STDIN)));
echo "contrato=" . ($a === $b ? "compatible" : "incompatible") . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🧪 Recorrido del código

El contrato ([`casos.json`](casos.json)) es una comparación de igualdad: la entrada `5 5` es `compatible`,
`5 6` es `incompatible`. Trivial en apariencia, pero el "cómo se compara" esconde una de las diferencias
semánticas más traicioneras entre lenguajes.

En **Python** la lógica es una línea: `a, b = sys.stdin.readline().split()` desempaqueta los dos tokens y
`'compatible' if a == b else 'incompatible'` decide. Aquí `a` y `b` son cadenas, y en Python `==` compara
**valor**: `"5" == "5"` es verdadero. La *f-string* imprime el resultado. Nada sorprende.

**Java** cuenta la misma historia pero con una trampa clásica que esta clase esquiva a propósito:

```java
String[] p = br.readLine().trim().split("\\s+");
System.out.println("contrato=" + (p[0].equals(p[1]) ? "compatible" : "incompatible"));
```

Fíjate en `p[0].equals(p[1])` y **no** `p[0] == p[1]`. En Java `==` sobre objetos compara **referencias**
(si son el mismo objeto en memoria), no contenido; para comparar el texto hay que usar `equals`. Un
principiante que "traduce" el `a == b` de Python a Java carácter por carácter obtiene un programa que a
veces acierta (por el *string interning*) y a veces falla —el peor tipo de bug—. Bloch, en *Effective
Java*, dedica un ítem entero a esto: no es una diferencia sintáctica, es semántica.

**C** no tiene ni siquiera un operador de igualdad para texto: usa `strcmp(a, b) == 0`, porque una cadena
es un puntero y `a == b` compararía direcciones. **Go** y **Rust**, en cambio, sí definen `==` sobre sus
cadenas como comparación de valor (`f[0] == f[1]`, `v[0] == v[1]`), acercándose a la intuición de Python.
**SQL** lo dice de la forma más limpia: `CASE WHEN a = b THEN 'compatible' ELSE 'incompatible' END`, una
expresión declarativa sobre una tabla. Diez formas de preguntar "¿son iguales?", y tres respuestas
distintas a la pregunta más profunda: **¿iguales en qué sentido?**

## 🔬 Comparación

El contrato de esta clase es una igualdad, y la igualdad es donde los lenguajes esconden sus decisiones más
finas. La tabla lo condensa; el texto lo justifica.

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `==` (Python/Go/Rust/JS), `.equals` (Java), `strcmp` (C), `=` (SQL): el mismo predicado, distinta escritura. |
| Semántica | En Java y C, `==` sobre cadenas compara **identidad/puntero**, no contenido: hay que usar `equals`/`strcmp`. En Python, Go, Rust y PHP (`===`) compara valor. |
| Paradigmática | Los imperativos ejecutan una comparación; SQL **declara** la compatibilidad como una columna calculada con `CASE`. |

La moraleja conecta con la tesis del curso: portar un contrato de un lenguaje a otro cambiando solo la
sintaxis es exactamente el error que Newman advierte a escala de sistema —cambiar la frontera sin entender
su semántica—. La igualdad de cadenas es ese mismo peligro a escala de una línea.

## 🧬 El concepto en la familia

Los *tests de contrato* (Pact, Spring Cloud Contract) verifican que servicios independientes respetan su
frontera sin necesidad de levantarlos todos juntos. Son la generalización de lo que hace este programa:
comparar lo que un lado promete con lo que el otro espera. En lenguajes con tipos, el propio compilador es
un verificador de contratos internos; entre servicios, el contrato se hace explícito y se prueba aparte.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 166
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Cambiar el contrato sin versionar** → causa: rompes al consumidor sin enterarte → solución: versiona la frontera y mantén compatibilidad hacia atrás mientras haya clientes viejos.
- **Fronteras implícitas** → causa: cada lado "supone" el formato y los supuestos divergen → solución: documenta el contrato explícitamente y pruébalo.
- **Confundir igualdad de valor con igualdad de referencia** → causa: `==` sobre objetos/cadenas en Java o C compara identidad → solución: usa `equals`/`strcmp` para comparar contenido.

## ❓ Preguntas frecuentes

- **¿Cómo verificar contratos?** Con pruebas de contrato entre consumidor y proveedor (Pact): el consumidor declara qué espera y el proveedor comprueba que lo cumple, sin levantar todo el sistema.
- **¿Contrato o integración total?** El contrato permite probar cada lado por separado: es más barato, más rápido y localiza mejor el fallo que una prueba end-to-end (clase 173).
- **¿Y si necesito cambiar el contrato?** Evoluciónalo de forma compatible (añade campos, no los quites), versiónalo y da un periodo de gracia a los consumidores antes de retirar lo viejo.

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

> [⏮️ Clase 165](../../parte-11-proyecto-integrador-poliglota/165-el-proyecto-un-sistema-con-componentes-en-varios-lenguajes/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 167 ⏭️](../../parte-11-proyecto-integrador-poliglota/167-componente-cli-lenguaje-de-sistemas/README.md)
