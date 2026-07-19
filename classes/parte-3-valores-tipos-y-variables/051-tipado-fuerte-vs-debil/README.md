# Clase 051 — Tipado fuerte vs. débil

> Parte **3 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Si la clase anterior preguntaba *cuándo* se comprueban los tipos, esta pregunta *cuántas* conversiones inseguras tolera el lenguaje cuando una operación recibe tipos que no encajan. Ese es el eje **fuerte/débil**. Un lenguaje de tipado **fuerte** se niega a operar entre tipos incompatibles sin una conversión que tú pidas: ante `"5" + 5` prefiere detenerse antes que adivinar. Uno de tipado **débil** hace lo contrario: coacciona uno de los operandos para que la operación "cuadre", produzca lo que produzca. El resultado de esa política es el ejemplo canónico de la programación: el mismo `+` puede sumar `10` o concatenar `"55"` según qué coerciones inserte cada lenguaje.

Es importante presentar fuerte/débil como un **espectro, no un binario**. Sebesta define un lenguaje de tipado fuerte como aquel en el que los errores de tipo *siempre se detectan*, y admite que casi ningún lenguaje real es fuerte o débil de forma absoluta: lo que varía es *cuántas* coerciones potencialmente inseguras permite. C es estático pero relativamente débil, porque deja convertir punteros y enteros con laxitud; JavaScript es dinámico y notoriamente débil, con reglas de coerción que sorprenden hasta a expertos; Python es dinámico pero **fuerte**, porque rechaza `"5" + 5` con un error en lugar de inventarse un resultado. Precisamente porque fuerte/débil (qué se tolera) es ortogonal a estático/dinámico (cuándo se comprueba), esos tres lenguajes ocupan casillas distintas del mismo mapa.

El laboratorio aísla el fenómeno con la operación más sobrecargada que existe: el `+`. A partir de un entero `n`, calcula a la vez su **suma** consigo mismo (`n + n`, aritmética) y su **concatenación** textual (`str(n) + str(n)`, unir cadenas). Verlo lado a lado en diez lenguajes deja claro por qué en un lenguaje débil `"5" + 5` puede dar `"55"` sin avisar, y por qué en uno fuerte tienes que decir explícitamente `str(n)` para concatenar: la ambigüedad del símbolo `+` es exactamente donde la coerción débil siembra sus bugs más difíciles de rastrear.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Diferenciar suma numérica de concatenación de texto.
2. Explicar tipado fuerte vs. débil con `+`.
3. Producir ambos resultados de forma explícita.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Suma vs. concatenación | El mismo símbolo, dos operaciones |
| 2 | Tipado fuerte | No convierte tipos sin que lo pidas |
| 3 | Tipado débil | Convierte automáticamente (a veces sorprende) |
| 4 | El operador + | Sobrecargado en muchos lenguajes |

## 📖 Definiciones y características

- **Tipado fuerte** — no permite operar entre tipos incompatibles sin conversión (Python, Java). Clave: menos sorpresas.
- **Tipado débil** — convierte tipos automáticamente para operar (PHP, JS). Clave: `'5'+5` puede dar cosas raras.
- **Concatenación** — unir dos cadenas. Clave: en muchos lenguajes también con `+`.
- **Sobrecarga de operador** — un operador con distinto significado según los tipos. Clave: `+` suma o concatena.

La fuerza del tipado se mide por cuántas **coerciones inseguras** admite el lenguaje sin protestar. Un lenguaje fuerte trata la discordancia de tipos como un error a reportar; un lenguaje débil la trata como un problema a resolver por su cuenta, insertando una conversión implícita. La palabra "inseguras" es clave: nadie llama débil a un lenguaje por promover `int` a `double` (esa coerción es ensanchante e inofensiva). Lo que caracteriza al tipado débil es convertir entre tipos *conceptualmente distintos* —texto y número, número y booleano— para que una operación de otro modo ilegal produzca un valor. JavaScript es el ejemplo de manual: `"5" + 5` da `"55"` (coacciona el número a texto y concatena), pero `"5" - 5` da `0` (coacciona el texto a número y resta), porque `-` no está sobrecargado para cadenas. Esa incoherencia entre operadores es la firma del tipado débil.

El **operador `+` sobrecargado** es el escenario perfecto para exhibir esto. En un lenguaje fuerte como Python, `+` significa "suma" entre números y "concatena" entre cadenas, pero se niega a mezclarlos: `"5" + 5` lanza `TypeError`, obligándote a decidir con `int("5") + 5` o `"5" + str(5)`. Esa negativa es una *característica*, no una limitación: te fuerza a declarar tu intención, y así el código dice la verdad sobre lo que hace. En un lenguaje débil el mismo `+` "hace algo" siempre, y ese *algo* depende de reglas de precedencia de coerción que hay que memorizar. SQL toma una tercera vía elegante: usa símbolos **distintos** —`+` solo para números y `||` para concatenar— eliminando de raíz la ambigüedad.

Conviene fijar la relación con los otros ejes para no arrastrar confusiones. Fuerte/débil (esta clase) es *cuántas conversiones inseguras se permiten*; estático/dinámico (clase 050) es *cuándo se comprueban los tipos*; y la conversión explícita frente a la coerción implícita (clase 049) es *quién ordena el cambio de tipo*. La coerción implícita es precisamente el mecanismo con el que el tipado débil realiza sus conversiones automáticas: por eso ambos conceptos se citan juntos, aunque uno describe un mecanismo y el otro, la política del lenguaje respecto a ese mecanismo.

## 🧩 Situación

Un caso real: un endpoint recibe dos valores de un formulario, `precio` y `descuento`, y calcula `precio - descuento`. Ambos llegan como texto. En JavaScript débil, `"20" - "5"` da `15` (coacciona ambos a número y resta), y parece que todo funciona… hasta que alguien suma en lugar de restar: `"20" + "5"` da `"205"`, no `25`, porque `+` con una cadena concatena. El mismo par de valores, el mismo lenguaje, dos operadores, y un bug silencioso de facturación que ninguna excepción delata. Esa asimetría —`+` concatena pero `-` resta— es la marca inconfundible del tipado débil, y su peligro es que no falla ruidosamente: produce un valor *plausible pero equivocado*.

En un lenguaje fuerte la misma situación se detiene antes: Python respondería con un `TypeError` a `"20" + 5`, empujándote a convertir explícitamente y, de paso, a decidir de forma consciente si querías sumar o concatenar. El laboratorio hace esa decisión visible calculando, a partir de un mismo entero `n`, tanto `n + n` (aritmética) como la concatenación de sus representaciones textuales, para que la diferencia entre "sumar" y "unir" quede escrita en el código y no oculta en una regla de coerción.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n`
- **Salida** (stdout): `suma=<n+n> texto=<n concatenado consigo mismo>`
- **Regla:** suma = n + n ; texto = str(n) ++ str(n)

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `suma=10 texto=55` |
| `3` | `suma=6 texto=33` |
| `12` | `suma=24 texto=1212` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER n
ESCRIBIR "suma=" (n+n) " texto=" (TEXTO(n) ++ TEXTO(n))
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

n = int(sys.stdin.readline())
print(f"suma={n + n} texto={str(n) + str(n)}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`suma=${n + n} texto=${String(n) + String(n)}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`suma=${n + n} texto=${String(n) + String(n)}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        String t = Integer.toString(n) + Integer.toString(n);
        System.out.printf("suma=%d texto=%s%n", n + n, t);
    }
}
```

### C# · `dotnet run`

```csharp
using System;

int n = int.Parse(Console.In.ReadToEnd().Trim());
Console.WriteLine($"suma={n + n} texto={n.ToString() + n.ToString()}");
```

### Go · `go run main.go`

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
	s := strconv.Itoa(n)
	fmt.Printf("suma=%d texto=%s%s\n", n+n, s, s)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    println!("suma={} texto={}{}", n + n, n, n);
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    printf("suma=%ld texto=%ld%ld\n", n + n, n, n);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL concatena con || (no con +).
WITH nums(n) AS (VALUES (5), (3), (12))
SELECT printf('suma=%d texto=%s', n + n, n || n) AS resultado
FROM nums;
```

### PHP · `php main.php`

```php
<?php
$n = (int) trim(fgets(STDIN));
printf("suma=%d texto=%s\n", $n + $n, (string) $n . (string) $n);
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔎 Recorrido guiado por el código

Sigamos el caso `stdin` = `5`, cuyo esperado es `suma=10 texto=55`. La gracia está en que `10` y `55` salen del **mismo número** por dos caminos: uno aritmético y otro textual. Ver cómo cada lenguaje escribe esos dos caminos revela si es fuerte o débil.

En **Python**, `n = int(sys.stdin.readline())` convierte el texto `"5"` en el entero `5`. La línea `print(f"suma={n + n} texto={str(n) + str(n)}")` contiene las dos operaciones clave, y ambas usan `+`, pero sobre tipos distintos. En `{n + n}`, los dos operandos son enteros, así que `+` **suma**: `5 + 5 = 10`. En `{str(n) + str(n)}`, cada `str(n)` produce la cadena `"5"`, y ahora `+` entre dos cadenas **concatena**: `"5" + "5" = "55"`. La diferencia entera es que escribimos `str(n)` de forma explícita. Si intentáramos `n + str(n)` —mezclar entero y texto— Python lanzaría `TypeError`, porque es **fuerte** y no coacciona entre esos tipos. Junto todo da la salida literal `suma=10 texto=55`; con `n = 12`, `n + n` es `24` y `str(12) + str(12)` es `"1212"`, de ahí `suma=24 texto=1212`.

El contraste más agudo lo da **SQL**, que ni siquiera comparte el símbolo: `printf('suma=%d texto=%s', n + n, n || n)`. Aquí `n + n` es la suma numérica, pero la concatenación usa el operador **`||`**, no `+`. SQL elimina la ambigüedad en la sintaxis: `+` jamás concatena, así que `5 + 5` solo puede ser `10` y `5 || 5` solo puede ser `"55"`. No hay coerción sorprendente posible porque cada operación tiene su propio símbolo. **Go** toma una vía parecida en espíritu: como es fuerte, no reutiliza `+` para mezclar tipos; primero produce el texto con `s := strconv.Itoa(n)` y luego concatena esas cadenas en el formato `%s%s`, nunca sumando texto con número.

Los lenguajes de la familia débil, **JavaScript**/**TypeScript** y **PHP**, son justamente los que *podrían* confundir suma y concatenación con `+`, y por eso el código es deliberadamente explícito. En JS, `${n + n}` suma porque ambos son números, y para el texto se fuerza `String(n) + String(n)` en vez de confiar en la coerción; en PHP, `$n + $n` suma y `(string) $n . (string) $n` concatena con el operador `.` (PHP separa concatenación con `.` de suma con `+`, aunque su *type juggling* coacciona en muchos otros contextos). La lección del recorrido es que, fuertes o débiles, todas las implementaciones **escriben explícitamente** la conversión a texto para concatenar —precisamente la disciplina que evita el bug de `"5" + 5`— y por eso todas convergen en `suma=10 texto=55`.

## 🔬 Comparación

El eje que ordena esta tabla es *cuánta coerción insegura tolera cada lenguaje*. En un extremo, los muy fuertes (Python, Java, Rust, Haskell) rechazan mezclar texto y número con `+` y exigen una conversión nombrada; SQL va más lejos y ni siquiera comparte el símbolo. En el otro, los débiles (JS, PHP) coaccionan según reglas por operador que hay que memorizar. Fíjate en que este eje es independiente del de la clase 050: Python es dinámico *y* fuerte, C es estático *y* relativamente débil.

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `str(n)+str(n)` (Python), `Integer.toString(n)+...` (Java), `String(n)+String(n)` (JS/TS), `(string)$n . (string)$n` (PHP), `n \|\| n` (SQL). |
| Semántica (fuerza) | Python/Java/Rust (fuertes) exigen convertir a texto para concatenar; JS/PHP (débiles) coaccionan solos en muchos contextos. |
| Semántica (símbolo) | `+` está sobrecargado (suma o concatena) en casi todos; SQL lo evita usando `+` para números y `\|\|` para texto, y PHP separa suma (`+`) de concatenación (`.`). |
| Paradigmática | El eje fuerte/débil es un **espectro**: JS deja pasar más coerciones inseguras que C, y C más que Go o Rust, que casi no permiten ninguna. |

## 🧬 El concepto en la familia

En Ruby (dinámico y fuerte) se escribe `n.to_s + n.to_s`; como Python, `"5" + 5` es un error. En JavaScript (débil) el truco `n + '' + n` concatena aprovechando que sumar cualquier cosa a una cadena vacía coacciona a texto —un idiom que funciona *porque* el lenguaje es débil, y que en Python no compilaría—. Haskell, en el extremo fuerte del espectro, obliga a `show n ++ show n`: no solo separa números de cadenas, sino que usa un operador de concatenación distinto (`++`) y jamás inserta una coerción implícita. Recorrer la familia de más débil (JS, PHP) a más fuerte (Haskell, Rust) deja ver que "fuerte" y "débil" no son etiquetas de sí/no sino posiciones en un continuo definido por cuántas conversiones peligrosas cede el lenguaje.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 051
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Esperar que `n + n` concatene (o al revés)** → causa: confundir suma con concatenación bajo el mismo `+` → solución: convierte a texto explícitamente (`str(n)`) para concatenar, y deja `+` numérico solo para números.
- **Confiar en la coerción débil** → causa: en JS `"20" + 5` da `"205"` y `"20" - 5` da `15`, resultados plausibles pero erróneos → solución: convierte de forma explícita para que la intención quede escrita y el bug no pueda esconderse.
- **Usar `==` en un lenguaje débil** → causa: JavaScript coacciona en la comparación laxa (`0 == "0"` es `true`, `"" == 0` es `true`) → solución: usa comparación estricta `===`, que no coacciona los tipos.
- **Asumir que "fuerte" implica "estático"** → causa: mezclar los dos ejes → solución: recuerda que Python es dinámico y fuerte a la vez; la fuerza es qué se tolera, no cuándo se comprueba.

## ❓ Preguntas frecuentes

- **¿Por qué `"5" + 5` es `"55"` en JS?** Por tipado débil: ante una cadena y un número, `+` prioriza la concatenación y coacciona el número a texto. Con `-`, en cambio, coacciona el texto a número, porque `-` no está sobrecargado para cadenas.
- **¿Python es fuerte o débil?** Fuerte. `"5" + 5` lanza `TypeError`; debes convertir explícitamente con `int("5") + 5` o `"5" + str(5)`. Ser dinámico no lo hace débil.
- **¿Fuerte/débil es lo mismo que seguro/inseguro?** No exactamente, pero se relacionan: un tipado más fuerte reporta más discordancias de tipo como errores, y Pierce vincula esa detección con la *seguridad de tipos* (progreso y preservación). Menos coerciones ciegas suelen significar menos comportamientos indefinidos.
- **¿Por qué se dice que es un espectro?** Porque no hay una frontera nítida: casi todos los lenguajes permiten *alguna* coerción (la promoción `int`→`double`) y ninguno las permite *todas*. Se ordenan por cuántas conversiones inseguras admiten, de JS (muchas) a Rust (casi ninguna).

## 🔗 Referencias

**Libros de la parte:**

- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson), cap. 6 (tipado fuerte/débil como espectro y coerción).
- B. C. Pierce — *Types and Programming Languages* (MIT Press), cap. 8 (seguridad de tipos: progreso y preservación).
- M. L. Scott — *Programming Language Pragmatics* (4ª ed., Morgan Kaufmann), cap. 7 (coerción y comprobación de tipos).

**Libros de los lenguajes del núcleo:**

- L. Ramalho — *Fluent Python* (2ª ed., O'Reilly), sobre *duck typing* y tipado dinámico fuerte.
- M. Haverbeke — *Eloquent JavaScript* (3ª ed.), cap. 1 (coerción, `==` vs. `===`) — [gratis online](https://eloquentjavascript.net/).
- B. Cherny — *Programming TypeScript* (O'Reilly).
- J. Bloch — *Effective Java* (3ª ed., Addison-Wesley).
- J. Skeet — *C# in Depth* (4ª ed., Manning).
- A. Donovan y B. Kernighan — *The Go Programming Language* (Addison-Wesley).
- S. Klabnik y C. Nichols — *The Rust Programming Language* — [gratis online](https://doc.rust-lang.org/book/).
- B. Kernighan y D. Ritchie — *The C Programming Language* (2ª ed., Prentice Hall).
- C. J. Date — *SQL and Relational Theory* (3ª ed., O'Reilly), sobre operadores y tipos.
- J. Lockhart — *Modern PHP* (O'Reilly), sobre *type juggling* y coerción.

---

> [⏮️ Clase 050](../../parte-3-valores-tipos-y-variables/050-tipado-estatico-vs-dinamico/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 052 ⏭️](../../parte-3-valores-tipos-y-variables/052-inferencia-de-tipos/README.md)
