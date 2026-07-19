# Clase 106 — Otros formatos y persistencia: CSV, YAML, binarios, bases de datos

> Parte **6 — Datos y estructuras** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Cerrar la parte con **persistencia y formatos tabulares**. Un programa que no persiste sus datos los pierde al terminar; persistir es elegir una representación externa, y esa elección determina quién podrá leerlos, cuánto ocuparán y qué se podrá cambiar después sin romper nada. CSV —valores separados por comas— es el extremo más simple del abanico: una fila por registro, un delimitador entre campos y nada más. Esa simplicidad es a la vez su virtud y su trampa. La virtud es que lo lee todo el mundo, desde una hoja de cálculo hasta un `awk` de tres líneas, y que ocupa lo mínimo para datos tabulares. La trampa es que **CSV no es un formato, es una familia de formatos parecidos**: no hay un estándar obligatorio (el RFC 4180 llegó tarde y describe la práctica más que imponerla), el delimitador cambia según la región, la codificación de caracteres no viaja con el archivo y el escapado de comillas es fuente inagotable de datos corruptos. Esta clase serializa una fila y cuenta sus campos —el núcleo del formato— y desde ahí sitúa CSV frente a JSON, YAML, los formatos binarios y las bases de datos, que es la decisión real que tomarás en un proyecto.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Serializar valores a una línea CSV.
2. Contar los campos.
3. Reconocer CSV frente a JSON.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | CSV | Valores separados por comas |
| 2 | Campo | Cada valor de la fila |
| 3 | Persistencia | Guardar datos en formato de texto |

## 📖 Definiciones y características

CSV es un formato **plano y sin tipos**. Cada línea es un registro, cada registro es una lista de campos separados por un delimitador, y todos los campos son texto: no hay forma de saber, mirando el archivo, si `007` es el número siete o un identificador con ceros a la izquierda, ni si `2024-03-01` es una fecha o una cadena. Esa ausencia de tipos es la causa de un desastre famoso: las hojas de cálculo convierten automáticamente ciertos identificadores en fechas, hasta el punto de que el comité de nomenclatura genética humana tuvo que **renombrar varios genes** en 2020 porque Excel los reinterpretaba al abrir el CSV. Es el ejemplo perfecto de que la conversión de tipos, cuando no está en el formato, la acaba inventando quien lo lee.

El delimitador es el segundo punto débil. La coma es lo habitual en la convención anglosajona, pero en las regiones que usan la coma como separador decimal —España, Francia, Alemania, buena parte de Latinoamérica— Excel exporta con **punto y coma**, así que dos archivos con la extensión `.csv` pueden ser incompatibles. El TSV, con tabuladores, evita el problema en muchos casos precisamente porque un tabulador rara vez aparece dentro de un dato.

El tercer punto, y el más difícil de resolver bien a mano, es el **escapado**. ¿Qué pasa si un campo contiene el propio delimitador? El convenio del RFC 4180 es encerrar el campo entre comillas dobles y duplicar las comillas internas: el texto `Acuña, Vladimir` se escribe `"Acuña, Vladimir"` y el texto `dijo "hola"` se escribe `"dijo ""hola"""`. Un campo entrecomillado puede además contener saltos de línea, lo que significa que **una fila lógica no equivale a una línea del archivo**. Esa sola frase invalida el enfoque intuitivo de leer el archivo línea a línea y partir por comas, y es la razón por la que todos los lenguajes ofrecen un módulo CSV con una máquina de estados de verdad.

- **CSV (comma-separated values)** — formato tabular de texto: una fila por registro, campos separados por un delimitador. Sin tipos, sin esquema y sin codificación declarada. Descrito —que no impuesto— por el RFC 4180.
- **Campo** — cada valor de una fila. Se separa por el delimitador y se entrecomilla cuando contiene el delimitador, comillas o saltos de línea.
- **Cabecera** — primera fila opcional con los nombres de columna. Convierte el archivo en algo interpretable, pero no es obligatoria y nada indica en el archivo si está presente.
- **Persistencia** — conservar datos más allá de la vida del proceso. El abanico va del archivo de texto plano (simple, portable, sin garantías) a la base de datos (con esquema, índices, consultas y transacciones ACID), pasando por los formatos binarios y columnares.

## 🧩 Situación

Un equipo exporta a CSV el listado de clientes para pasárselo a otro departamento. Funciona durante meses, hasta el día en que un cliente se llama «Muñoz, S.L.». La coma dentro del nombre parte el campo en dos, esa fila pasa a tener una columna de más, y la importación falla o —mucho peor— desplaza los datos una posición y los guarda mal sin que nadie se entere. El segundo capítulo llega con los acentos: el archivo se generó en UTF-8, Excel lo abre asumiendo la codificación local de Windows y «Muñoz» aparece como «MuÃ±oz», porque CSV no lleva dentro ninguna indicación de su propia codificación. El tercero llega cuando alguien exporta desde una hoja de cálculo configurada en español y el archivo sale delimitado por punto y coma, ilegible para el script que esperaba comas.

Los tres incidentes tienen la misma raíz: CSV traslada al lector decisiones que el formato no registra —qué delimitador, qué codificación, qué tipos, si hay cabecera—, y cada extremo las adivina. JSON no sufre ninguno de los tres porque fija comillas, escapes y UTF-8 en su propia definición. La lección práctica no es abandonar CSV, que sigue siendo insuperable para datos tabulares grandes y simples, sino usar la biblioteca del lenguaje en vez de partir cadenas a mano y acordar explícitamente delimitador y codificación con quien recibe el archivo. El ejercicio de hoy trabaja con enteros, donde nada de esto muerde, para aislar el mecanismo: unir los valores con comas y contar cuántos hay.

## 🧮 Modelo

- **Entrada** (stdin): una línea con enteros separados por espacio
- **Salida** (stdout): `csv=<valores separados por coma> campos=<cantidad>`
- **Regla:** csv = unir con coma ; campos = cantidad de valores

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `1 2 3` | `csv=1,2,3 campos=3` |
| `5` | `csv=5 campos=1` |
| `10 20` | `csv=10,20 campos=2` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER lista ; csv <- unir con , ; campos <- longitud
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys

nums = sys.stdin.read().split()
csv = ",".join(nums)
print(f"csv={csv} campos={len(nums)}")
```

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const nums = readFileSync(0, "utf8").trim().split(/\s+/);
console.log(`csv=${nums.join(",")} campos=${nums.length}`);
```

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const nums: string[] = readFileSync(0, "utf8").trim().split(/\s+/);
console.log(`csv=${nums.join(",")} campos=${nums.length}`);
```

### Java · [`java/Main.java`](implementaciones/java/Main.java) · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] nums = br.readLine().trim().split("\\s+");
        System.out.println("csv=" + String.join(",", nums) + " campos=" + nums.length);
    }
}
```

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;

string[] nums = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
Console.WriteLine($"csv={string.Join(",", nums)} campos={nums.Length}");
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
	nums := strings.Fields(line)
	fmt.Printf("csv=%s campos=%d\n", strings.Join(nums, ","), len(nums))
}
```

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let nums: Vec<&str> = s.split_whitespace().collect();
    println!("csv={} campos={}", nums.join(","), nums.len());
}
```

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    char tok[64];
    int campos = 0;
    printf("csv=");
    while (scanf("%63s", tok) == 1) {
        if (campos > 0) printf(",");
        printf("%s", tok);
        campos++;
    }
    printf(" campos=%d\n", campos);
    return 0;
}
```

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL: group_concat produce una fila CSV.
WITH nums(x) AS (VALUES (1), (2), (3))
SELECT 'csv=' || group_concat(x, ',') || printf(' campos=%d', count(*)) AS resultado FROM nums;
```

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
$nums = preg_split('/\s+/', trim(fgets(STDIN)));
echo "csv=" . implode(",", $nums) . " campos=" . count($nums) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🧪 Laboratorio guiado: del código a la salida

Sigamos el caso `1 2 3`, que debe producir `csv=1,2,3 campos=3`, y el caso `5`, que debe producir `csv=5 campos=1`. Los dos casos juntos comprueban la propiedad esencial del `join`: para n elementos hay exactamente n − 1 separadores, y con un solo elemento no hay ninguno.

En **Python**, `",".join(nums)` es el modismo canónico y merece una observación: se invoca sobre el **separador**, no sobre la lista, algo que sorprende a quien viene de otros lenguajes pero que tiene su lógica —el separador es quien sabe unir, y así el método sirve para cualquier iterable—. Nota también que el código no convierte los tokens a enteros: `sys.stdin.read().split()` devuelve cadenas y `join` exige cadenas, así que la conversión sería un rodeo innecesario. `len(nums)` cuenta los elementos de la lista, no los caracteres del texto: contar sobre la cadena `1,2,3` daría cinco, no tres. El recorrido completo es O(n), y `join` además reserva de una vez el búfer del tamaño total, evitando el clásico bucle de concatenación que sería O(n²) en lenguajes con cadenas inmutables.

En **Go**, `strings.Join(nums, ",")` invierte el orden de los argumentos respecto a Python —colección primero, separador después— y `len(nums)` sobre un slice devuelve su número de elementos. Aquí la elección de `strings.Fields(line)` es deliberada: parte por cualquier bloque de espacios y descarta los vacíos, a diferencia de `strings.Split(line, " ")`, que con dos espacios seguidos produciría un campo vacío. La biblioteca estándar de Go trae además `encoding/csv`, con `Writer` y `Reader` que resuelven correctamente el entrecomillado; en un caso real ese sería el camino.

En **C**, no hay `join` ni hay lista: el código emite el CSV **mientras lee**. `while (scanf("%63s", tok) == 1)` va tomando tokens, y la línea `if (campos > 0) printf(",");` implementa a mano la regla de «coma antes de cada elemento salvo el primero», que es exactamente lo que un `join` encapsula. El contador `campos` se incrementa en cada vuelta y se imprime al final. Es una solución en **streaming**: no guarda nada, así que funcionaría con un millón de campos en memoria constante. Y el `%63s` no es un adorno: limita la lectura a 63 caracteres más el terminador para no desbordar `tok[64]`, la precaución que Kernighan y Ritchie repiten en *The C Programming Language* cada vez que aparece un búfer de tamaño fijo.

En **SQL**, `group_concat(x, ',')` es una **función de agregación**: no recorre nada, colapsa un conjunto de filas en un único valor de texto, igual que `count(*)` las colapsa en un número. Es el mismo resultado desde el otro extremo del pensamiento —declarativo en vez de imperativo—, y refleja lo que ocurre de verdad al exportar: en la práctica no construirías el CSV a mano sino con `.mode csv` de SQLite o `COPY ... TO ... WITH CSV` de PostgreSQL, comandos que aplican el entrecomillado correcto.

Los diez imprimen `csv=1,2,3 campos=3`; el verificador comprueba que la salida coincide carácter a carácter con lo que dicta `casos.json`.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `','.join(...)` (Python), `.join(',')` (JS), bucle (C). |
| Semántica | CSV real necesita escapar comas y comillas; aquí los datos son simples. |
| Paradigmática | SQL exporta/importa CSV con comandos del motor. |

La diferencia sintáctica visible es **sobre qué se invoca el `join` y en qué orden van los argumentos**: Python lo pone en el separador (`",".join(xs)`), JavaScript, TypeScript, Rust y PHP en la colección (`xs.join(",")`, `implode(",", $xs)`), Java lo ofrece como método estático (`String.join(",", xs)`) y Go como función de paquete (`strings.Join(xs, ",")`). C no lo tiene y hay que escribir el bucle con la condición del primer elemento. Detrás de todos hay la misma consideración de rendimiento: concatenar en un bucle con `s = s + x` cuesta O(n²) en los lenguajes de cadenas inmutables, porque cada paso copia toda la cadena acumulada; por eso Java tiene `StringBuilder`, Go tiene `strings.Builder` y todos ofrecen un `join` que reserva el búfer una sola vez.

La segunda diferencia es **cuánto CSV real trae la biblioteca estándar**. Python incluye el módulo `csv` con `reader`, `writer` y `DictReader`, y hasta un detector automático de dialecto (`Sniffer`). Go trae `encoding/csv`. Java y C# lo dejan a bibliotecas externas (OpenCSV, CsvHelper), lo que lleva a muchos programadores a improvisar un `split(",")` que funciona hasta que aparece la primera coma dentro de un campo. Rust tiene el crate `csv`, integrado con `serde` para leer directamente a structs tipados. PHP ofrece `fgetcsv` y `fputcsv` desde hace décadas. La regla práctica es unánime en todos: para **escribir** datos que controlas, un `join` basta; para **leer** CSV ajeno, la biblioteca no es opcional, porque el análisis correcto exige una máquina de estados que gestione comillas, comillas duplicadas y saltos de línea dentro de un campo.

El tercer eje es **paradigmático**. En los nueve lenguajes imperativos el CSV se produce recorriendo una colección; en SQL se produce agregando un conjunto, y la importación y exportación son responsabilidad del motor (`COPY` en PostgreSQL, `.import` en SQLite, `LOAD DATA INFILE` en MySQL), que además valida los tipos contra el esquema de la tabla al cargar. Es un contraste que sitúa la clase entera: Date insiste en *SQL and Relational Theory* en que el valor del modelo relacional está en el esquema y las restricciones, justo aquello de lo que CSV carece por completo.

## 🧬 El concepto en la familia

La forma de unir campos es casi idéntica en todas partes —`arr.join(',')` en Ruby, `intercalate ","` en Haskell, `Enum.join` en Elixir, `joinToString` en Kotlin—, y casi todos los lenguajes disponen además de una biblioteca CSV que hace el trabajo sucio. Lo interesante de esta clase no es el `join`, sino el lugar que CSV ocupa en el abanico de la persistencia, que conviene tener ordenado. **CSV** es plano, sin tipos y sin esquema: imbatible para tablas grandes y homogéneas, pésimo para datos anidados. **JSON** (clase 105) añade tipos básicos y anidamiento a cambio de repetir los nombres de campo en cada registro, lo que lo hace bastante más voluminoso. **YAML** es un superconjunto de JSON pensado para que lo escriban humanos: admite comentarios y usa indentación en vez de llaves, razón por la que domina la configuración (Docker Compose, Kubernetes, GitHub Actions) y también por la que da sustos —su regla histórica de convertir `no` en booleano falso obligó a YAML 1.2 a cambiar el comportamiento, y sigue viva en muchos analizadores—. **TOML** buscó la legibilidad de YAML sin sus ambigüedades y por eso lo adoptaron Rust y Python para sus manifiestos. Los **formatos binarios** —Protocol Buffers, Avro, MessagePack— renuncian a la legibilidad a cambio de tamaño y velocidad. **Parquet** y **ORC**, columnares, son el sucesor natural de CSV en analítica: guardan los datos por columna en lugar de por fila, lo que permite leer solo las columnas necesarias y comprimir mucho mejor los valores repetidos. Y en el otro extremo está la **base de datos**, que no es un formato sino un sistema: aporta esquema, índices, consultas y transacciones ACID, y es lo que debes elegir en cuanto necesites consultar, actualizar o acceder concurrentemente en vez de simplemente volcar. La escalera va de menos a más garantías, y cada peldaño se paga en complejidad; la decisión de ingeniería consiste en subir solo hasta donde el problema lo exija.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 106
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **No escapar comas dentro de un campo** → causa: un valor como `Muñoz, S.L.` parte la fila en un campo de más, y la importación falla o —peor— desplaza silenciosamente todas las columnas siguientes → solución: entrecomillar el campo (`"Muñoz, S.L."`) y duplicar las comillas internas; en la práctica, dejar que lo haga la biblioteca CSV del lenguaje.
- **Analizar CSV con `split(",")`** → causa: ignora el entrecomillado, los campos con comas y los saltos de línea dentro de un campo; funciona con los datos de prueba y se rompe con los reales → solución: usar el módulo CSV (`csv` en Python, `encoding/csv` en Go, `fgetcsv` en PHP, el crate `csv` en Rust), que implementa la máquina de estados correcta.
- **Confundir campos con caracteres** → causa: contar sobre la cadena `1,2,3` en vez de sobre la colección devuelve 5 → solución: contar los elementos antes de unirlos; para n campos hay siempre n − 1 delimitadores.
- **Dar por hecha la codificación** → causa: el archivo se escribe en UTF-8 y el lector asume la codificación local (o al revés), y los acentos salen como mojibake; CSV no declara su codificación en ninguna parte → solución: acordarla explícitamente con quien recibe el archivo, escribir siempre UTF-8 y valorar el BOM si el destino es Excel en Windows.
- **Dar por hecho el delimitador** → causa: una hoja de cálculo configurada en español exporta con punto y coma, y el script que espera comas ve una única columna → solución: no adivinar; especificar el delimitador al leer, o negociarlo (el TSV con tabuladores evita buena parte del problema).
- **Perder los tipos al pasar por CSV** → causa: todo es texto, así que `007` se convierte en `7`, un identificador numérico largo pierde precisión y ciertos códigos se transforman en fechas al abrirlos en una hoja de cálculo → solución: no usar CSV como formato de intercambio con tipos sensibles, o transportar esos campos como texto entrecomillado y documentarlo.
- **Usar CSV cuando el problema pide una base de datos** → causa: se acaba reimplementando a mano la búsqueda, la actualización y el acceso concurrente, y sin transacciones un fallo a media escritura deja el archivo corrupto → solución: en cuanto haya consultas, actualizaciones o varios escritores, subir un peldaño (SQLite basta y no exige servidor).

## ❓ Preguntas frecuentes

- **¿CSV o JSON?** CSV para tablas planas, homogéneas y grandes: pesa mucho menos porque no repite los nombres de columna en cada fila, y se procesa en streaming sin cargarlo entero. JSON para datos anidados, heterogéneos o con tipos que importan. Si el dato es una tabla, CSV; si es un árbol, JSON.
- **¿CSV siempre usa comas?** No, aunque el nombre lo diga. El punto y coma es habitual en las regiones que usan la coma decimal, y el tabulador (TSV) es común en bioinformática y en volcados de bases de datos justo porque casi nunca aparece dentro de un dato. El delimitador es una convención entre las dos partes, no una propiedad del formato.
- **¿Existe un estándar de CSV?** El RFC 4180 (2005) describe la práctica dominante —comas, `CRLF` entre filas, entrecomillado con comillas dobles duplicadas— pero llegó décadas después del uso real y no obliga a nadie. Por eso conviven tantos dialectos y por eso el módulo `csv` de Python incluye un detector automático.
- **¿Y YAML, cuándo?** Para configuración escrita y leída por personas, porque admite comentarios y su indentación se lee bien. No lo uses para intercambio de datos entre máquinas: su gramática es enormemente más compleja que la de JSON, sus analizadores han tenido vulnerabilidades serias por deserializar objetos arbitrarios, y su conversión implícita de tipos —`no` como booleano, `1.0` como número, versiones como `1.10` que pierden el cero— produce sorpresas que JSON simplemente no tiene.
- **¿Cuándo pasar a una base de datos?** En cuanto necesites **consultar** en vez de leerlo todo, **actualizar** partes en vez de reescribir el archivo entero, garantizar **integridad** con restricciones y tipos, o permitir varios lectores y escritores a la vez. El salto no tiene por qué ser grande: SQLite es un solo archivo, sin servidor ni administración, y ya te da esquema, índices y transacciones ACID.
- **¿Y los formatos columnares como Parquet?** Son la elección natural cuando el CSV se hace grande y las consultas son analíticas. Al guardar los datos por columna en vez de por fila, permiten leer solo las columnas que interesan y comprimen muchísimo mejor los valores repetidos; un CSV de gigabytes suele encoger un orden de magnitud y consultarse varias veces más rápido.

## 🔗 Referencias

**Libros de la parte:**

- T. Cormen, C. Leiserson, R. Rivest y C. Stein — *Introduction to Algorithms* (4ª ed., MIT Press).
- R. Sedgewick y K. Wayne — *Algorithms* (4ª ed., Addison-Wesley).

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

> [⏮️ Clase 105](../../parte-6-datos-y-estructuras/105-json-serializacion-y-deserializacion/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 107 ⏭️](../../parte-7-paradigmas/107-que-es-un-paradigma-y-por-que-importa/README.md)
