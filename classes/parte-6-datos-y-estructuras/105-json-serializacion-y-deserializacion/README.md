# Clase 105 — JSON: serialización y deserialización

> Parte **6 — Datos y estructuras** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Trabajar con **JSON**: el formato universal de intercambio de datos. Todo lo visto en esta parte —arreglos, mapas, registros— vive dentro del proceso: son punteros, cabeceras y bloques de memoria que dejan de existir cuando el programa termina. **Serializar** es traducir esas estructuras a una secuencia de bytes que sobrevive al proceso y viaja entre máquinas; **deserializar** es reconstruirlas al otro lado. JSON se impuso como el idioma común de esa traducción por una razón que conviene entender: su modelo de datos —objetos, arreglos, cadenas, números, booleanos y nulo— es el **mínimo común denominador** de casi todos los lenguajes, de modo que un servidor en Go y un cliente en JavaScript pueden entenderse sin acordar nada más que el formato. Esa universalidad se paga con imprecisión: JSON no distingue enteros de reales, no tiene fechas, no tiene binarios y no describe su propio esquema. Kleppmann analiza este compromiso en *Designing Data-Intensive Applications* al comparar JSON con formatos con esquema como Avro o Protocol Buffers. En esta clase construyes a mano el objeto `{"nombre": "Ada", "edad": 36}` en diez lenguajes, precisamente para fijar el formato exacto antes de delegarlo en una biblioteca.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Serializar datos a JSON.
2. Respetar el formato (comillas, dos puntos).
3. Reconocer JSON como formato de intercambio.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | JSON | Formato de intercambio de datos |
| 2 | Serializar | De datos a texto JSON |
| 3 | Deserializar | De texto JSON a datos |

## 📖 Definiciones y características

La gramática de JSON es minúscula y se puede enunciar entera en un párrafo, lo que explica buena parte de su éxito. Un **valor** JSON es una de seis cosas: un **objeto** (`{}` con pares `"clave": valor` separados por comas, y la clave siempre entre comillas dobles), un **arreglo** (`[]` con valores separados por comas), una **cadena** (comillas dobles obligatorias, con `\"`, `\\`, `\n` y `\uXXXX` como escapes), un **número** (en notación decimal opcionalmente con exponente, sin comillas y sin distinción entre entero y real), un **booleano** (`true` o `false` en minúsculas) o **`null`**. No hay comentarios, no hay coma final permitida y no hay comillas simples. Esa rigidez es intencionada: cuanto más pequeña es la gramática, menos margen hay para que dos implementaciones la interpreten de forma distinta.

Serializar y deserializar son operaciones **O(n)** sobre el tamaño del texto, pero no son simétricas en riesgo. Serializar es un recorrido de la estructura escribiendo tokens; el único cuidado real es **escapar** correctamente las cadenas y detectar ciclos, porque un objeto que se contiene a sí mismo haría que el recorrido no termine. Deserializar es análisis sintáctico de entrada externa, y ahí toda la entrada es hostil: puede estar mal formada, puede tener campos que no esperas, puede faltar el que sí esperas, y puede ser lo bastante grande o profunda como para agotar la memoria o la pila. La primera regla práctica de la serialización es que serializar puedes hacerlo con confianza y deserializar nunca.

- **JSON (JavaScript Object Notation)** — formato de texto para datos estructurados, definido por Douglas Crockford y estandarizado como RFC 8259 y ECMA-404. Su modelo se limita a objeto, arreglo, cadena, número, booleano y nulo. Es **autodescriptivo** (los nombres de campo viajan con los datos) y **sin esquema**, lo que lo hace flexible y verboso a la vez.
- **Serializar (marshalling, encoding)** — convertir estructuras en memoria a texto JSON. O(n). Los puntos de cuidado son el escapado de las cadenas y las referencias circulares.
- **Deserializar (unmarshalling, parsing)** — reconstruir estructuras desde el texto. O(n), pero con validación obligatoria: la entrada es externa y por tanto no confiable. Limitar el tamaño y la profundidad de anidamiento es parte del trabajo.
- **Esquema** — la descripción de qué campos y tipos se esperan. JSON no lo lleva incorporado; se añade aparte (JSON Schema, tipos de TypeScript, `struct` con etiquetas en Go, clases anotadas en Java). Formatos como Protocol Buffers o Avro lo exigen por adelantado y, a cambio, producen mensajes mucho más compactos y detectan las incompatibilidades antes.

## 🧩 Situación

Las APIs web hablan JSON, y con eso se dice casi todo: un servidor en Go serializa una `struct`, la envía por HTTP, y un cliente en JavaScript la recibe como objeto sin que ninguno de los dos sepa nada del otro. Pero la situación interesante no es el camino feliz, sino lo que falla. Dos ejemplos que se ven a diario. El primero es el de los **números grandes**: JSON no distingue enteros de reales, y `JSON.parse` de JavaScript los convierte todos a `double` de 64 bits, cuya mantisa solo garantiza enteros exactos hasta 2^53; un identificador de Twitter o de Discord, que supera ese límite, llega al navegador con los últimos dígitos alterados. La solución de la industria fue enviar esos identificadores como **cadenas**. El segundo es el de las **fechas**: JSON no tiene tipo fecha, así que se transmiten como texto ISO 8601, y cada extremo debe acordar el formato y la zona horaria por su cuenta, porque el formato no lo impone. En ambos casos el problema no está en el código sino en el modelo de datos del formato, y por eso conviene conocerlo. El ejercicio de hoy construye a mano el objeto para que el formato quede grabado —comillas dobles en las claves y en la cadena, ninguna comilla en el número—, aunque en producción esa construcción manual sea exactamente lo que no debes hacer.

## 🧮 Modelo

- **Entrada** (stdin): una línea `nombre edad` (una palabra y un entero)
- **Salida** (stdout): `{"nombre": "<nombre>", "edad": <edad>}`
- **Regla:** objeto JSON con las claves nombre y edad

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `Ada 36` | `{"nombre": "Ada", "edad": 36}` |
| `Bo 5` | `{"nombre": "Bo", "edad": 5}` |
| `Cy 99` | `{"nombre": "Cy", "edad": 99}` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER nombre, edad ; construir objeto ; serializar a JSON
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys

t = sys.stdin.readline().split()
nombre, edad = t[0], int(t[1])
print(f'{{"nombre": "{nombre}", "edad": {edad}}}')
```

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const t = readFileSync(0, "utf8").trim().split(/\s+/);
const nombre = t[0];
const edad = parseInt(t[1], 10);
console.log(`{"nombre": "${nombre}", "edad": ${edad}}`);
```

🧬 **El mismo programa en la familia JavaScript / web:** [Dart · ActionScript](primos.md#javascript-web)

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const t: string[] = readFileSync(0, "utf8").trim().split(/\s+/);
const nombre: string = t[0];
const edad: number = parseInt(t[1], 10);
console.log(`{"nombre": "${nombre}", "edad": ${edad}}`);
```

🧬 **El mismo programa en la familia JavaScript / web:** [Dart · ActionScript](primos.md#javascript-web)

### Java · [`java/Main.java`](implementaciones/java/Main.java) · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] t = br.readLine().trim().split("\\s+");
        String nombre = t[0];
        int edad = Integer.parseInt(t[1]);
        System.out.println("{\"nombre\": \"" + nombre + "\", \"edad\": " + edad + "}");
    }
}
```

🧬 **El mismo programa en la familia JVM:** [Kotlin · Scala · Groovy · Clojure](primos.md#jvm)

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;

string[] t = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
string nombre = t[0];
int edad = int.Parse(t[1]);
Console.WriteLine($"{{\"nombre\": \"{nombre}\", \"edad\": {edad}}}");
```

🧬 **El mismo programa en la familia .NET:** [F# · VB.NET](primos.md#dotnet)

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
	t := strings.Fields(line)
	nombre := t[0]
	edad, _ := strconv.Atoi(t[1])
	fmt.Printf("{\"nombre\": \"%s\", \"edad\": %d}\n", nombre, edad)
}
```

🧬 **El mismo programa en la familia Sistemas:** [Zig · Nim · D](primos.md#sistemas)

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let t: Vec<&str> = s.split_whitespace().collect();
    let nombre = t[0];
    let edad: i64 = t[1].parse().unwrap();
    println!("{{\"nombre\": \"{nombre}\", \"edad\": {edad}}}");
}
```

🧬 **El mismo programa en la familia Sistemas:** [Zig · Nim · D](primos.md#sistemas)

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    char nombre[64];
    long edad;
    if (scanf("%63s %ld", nombre, &edad) != 2) return 1;
    printf("{\"nombre\": \"%s\", \"edad\": %ld}\n", nombre, edad);
    return 0;
}
```

🧬 **El mismo programa en la familia C / llaves:** [C++ · Objective-C](primos.md#c-llaves)

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL: construye JSON con printf (o json_object en motores con la extensión).
WITH personas(nombre, edad) AS (VALUES ('Ada', 36))
SELECT printf('{"nombre": "%s", "edad": %d}', nombre, edad) AS resultado FROM personas;
```

🧬 **El mismo programa en la familia Lógica y declarativa:** [Prolog · Datalog](primos.md#logica-declarativa)

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
$t = preg_split('/\s+/', trim(fgets(STDIN)));
$nombre = $t[0];
$edad = (int) $t[1];
echo "{\"nombre\": \"$nombre\", \"edad\": $edad}\n";
```

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🧪 Laboratorio guiado: del código a la salida

Sigamos el caso `Ada 36`, que debe producir exactamente `{"nombre": "Ada", "edad": 36}`. Fíjate en los cuatro detalles que el verificador comprueba carácter a carácter: llaves, comillas dobles alrededor de las claves y del valor de texto, ausencia de comillas alrededor del número, y un espacio después de cada dos puntos y de la coma.

En **Python**, la línea `print(f'{{"nombre": "{nombre}", "edad": {edad}}}')` esconde una peculiaridad de las f-strings: `{{` y `}}` son la forma de escribir una llave literal, porque la llave simple abre una interpolación. Por eso el código usa comillas simples para delimitar la cadena de Python y reserva las dobles para el JSON: así no hace falta escapar nada más. `nombre` entra entre comillas porque es texto; `edad`, que se convirtió con `int(t[1])`, entra desnudo porque es número. En un programa real esta línea sería `json.dumps({"nombre": nombre, "edad": edad})`, que además escaparía correctamente un nombre que contuviera comillas o acentos.

En **Java** y **C#**, lo que domina la línea es el **escapado de las comillas dobles**, que en ambos lenguajes se escribe `\"`. La concatenación de Java, `"{\"nombre\": \"" + nombre + "\", \"edad\": " + edad + "}"`, es tan ilegible que sirve de argumento por sí sola a favor de las bibliotecas: cualquier lector tiene que contar comillas para verificarla. C# lo sufre igual dentro de su cadena interpolada y añade el problema de Python: como `{` abre la interpolación, hay que duplicarla a `{{` para obtener una llave literal. Java 15 introdujo los bloques de texto (`"""`) precisamente para que este tipo de literal deje de necesitar escapes.

En **Rust**, `println!("{{\"nombre\": \"{nombre}\", \"edad\": {edad}}}")` acumula las dos convenciones a la vez: `{{` y `}}` para las llaves literales del macro de formato, y `\"` para las comillas de la cadena. Además exhibe la captura de identificadores por nombre —`{nombre}` toma directamente la variable del ámbito, sin pasarla como argumento—, disponible desde Rust 2021. Nota que `edad` se declaró como `i64` y se imprime sin comillas: el tipo del lenguaje decide la forma del JSON.

En **SQL**, `printf('{"nombre": "%s", "edad": %d}', nombre, edad)` deja ver el mecanismo desnudo: `%s` es texto y va entre comillas escritas a mano, `%d` es entero y va sin ellas. Es exactamente lo que hacen los demás, solo que sin ocultarlo. En producción usarías `json_object('nombre', nombre, 'edad', edad)`, la función que SQLite y PostgreSQL ofrecen para construir JSON con el escapado ya resuelto —y que además nunca produciría un JSON inválido a partir de un nombre con comillas—.

Los diez imprimen `{"nombre": "Ada", "edad": 36}`; el verificador comprueba que la salida coincide carácter a carácter con lo que dicta `casos.json`.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Librerías `json` (Python), `JSON.stringify` (JS), pero el formato es idéntico. |
| Semántica | Las cadenas van entre comillas dobles; los números sin comillas. |
| Paradigmática | SQL genera JSON con funciones `json_object` (aquí, con printf). |

La primera diferencia no está en el formato —que es literalmente el mismo en todas partes; ese es el sentido de JSON— sino en **cómo cada lenguaje salva la distancia entre su sistema de tipos y el de JSON**. Los lenguajes dinámicos casi no tienen distancia que salvar: JavaScript trae `JSON.stringify` y `JSON.parse` en el propio lenguaje, y Python mapea `dict` a objeto, `list` a arreglo y `None` a `null` de forma directa con el módulo `json`. Los lenguajes estáticos necesitan un puente explícito. Go usa **etiquetas de struct** —`json:"nombre"`— que la biblioteca `encoding/json` lee por reflexión para saber cómo se llama cada campo en el texto. Rust usa `serde` con `#[derive(Serialize, Deserialize)]`, que genera el código de conversión **en tiempo de compilación**: sin reflexión y sin coste en ejecución. Java y C# recurren a bibliotecas con anotaciones (Jackson, `System.Text.Json`) que resuelven el mapeo por reflexión o, en el caso moderno de .NET, mediante generadores de código. En C no hay nada de esto en la biblioteca estándar y hay que enlazar una biblioteca externa o escribir el analizador a mano.

La segunda diferencia, y la que produce bugs reales de interoperabilidad, es **cómo trata cada lenguaje los números**. JSON solo tiene «número», sin especificar precisión. JavaScript lo interpreta siempre como `double`, y por eso pierde precisión más allá de 2^53. Python distingue `int` de `float` al parsear y admite enteros de precisión arbitraria, así que lee sin problema un número que JavaScript ya habría estropeado. Go, al deserializar en un `interface{}`, convierte todo número a `float64` salvo que se use `json.Number`. Java con Jackson decide el tipo según el campo destino. Resultado: el mismo documento JSON puede producir valores distintos en dos lenguajes, y ese es el motivo por el que los identificadores grandes se transmiten como cadenas.

El tercer eje es **el tratamiento de la ausencia**. Go escribe el valor cero (`0`, `""`) para los campos no establecidos salvo que se marquen `omitempty`, de modo que no distingue «cero» de «no había dato». Rust modela la ausencia con `Option<T>`, que serializa a `null` y que obliga al programador a decidir qué hacer cuando falta. Java tiene `null` para todo y `Optional`, que Jackson necesita un módulo aparte para manejar. TypeScript declara la opcionalidad en el tipo (`edad?: number`), pero esa comprobación desaparece en ejecución: Cherny insiste en *Programming TypeScript* en que el JSON entrante debe validarse en tiempo de ejecución, porque el compilador no puede garantizar la forma de un dato que llega de la red.

## 🧬 El concepto en la familia

Prácticamente todo lenguaje vivo trae JSON de serie o mediante una biblioteca canónica: `to_json` en Ruby, `json_encode` en PHP, `Data.Aeson` en Haskell, `Jason` en Elixir, `kotlinx.serialization` en Kotlin, `Codable` en Swift. El formato no cambia; lo que cambia es dónde se decide el mapeo. Hay tres escuelas. La **dinámica** convierte a estructuras genéricas —diccionarios y listas— y deja la validación al programador: rápida de escribir, frágil ante datos inesperados. La **reflexiva** —Jackson, `encoding/json`, `System.Text.Json`— inspecciona el tipo destino en tiempo de ejecución para rellenarlo; cómoda, con algo de coste y sorpresas cuando el tipo no encaja. La **generativa** —`serde` en Rust, `Codable` en Swift, `kotlinx.serialization`— produce el código de conversión al compilar: sin reflexión, sin coste añadido y con los errores de forma detectados antes de ejecutar. Conviene, por último, situar JSON entre sus parientes. **XML** es su antecesor: más verboso, pero con esquemas y espacios de nombres maduros. **YAML** (clase 106) es un superconjunto pensado para que lo escriban humanos. **Protocol Buffers**, **Avro** y **MessagePack** son binarios y con esquema: mucho más compactos y rápidos, a costa de no ser legibles y de exigir que ambos extremos compartan la definición. La elección, como resume Kleppmann, se reduce a un compromiso entre legibilidad y flexibilidad por un lado, y tamaño, velocidad y garantías de evolución del esquema por otro.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 105
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Comillas simples en JSON** → causa: la gramática exige comillas dobles tanto en las claves como en las cadenas, y `{'a': 1}` es JSON inválido aunque sea un `dict` de Python perfectamente válido → solución: usar siempre comillas dobles, y no confundir la representación de un diccionario impresa por el lenguaje con JSON de verdad.
- **Poner comillas a los números** → causa: `"edad": "36"` convierte el número en cadena y el otro extremo recibirá texto donde esperaba un entero → solución: los números, booleanos y `null` van sin comillas; solo las cadenas las llevan.
- **Concatenar JSON a mano con datos de usuario** → causa: un nombre que contenga una comilla doble, una barra invertida o un salto de línea rompe el documento y produce JSON inválido, además de abrir la puerta a inyección → solución: usar siempre la biblioteca (`json.dumps`, `JSON.stringify`, `json_object`), que escapa correctamente; el código de esta clase construye el texto a mano solo con fines didácticos y con datos controlados.
- **Confiar en la precisión de los números grandes** → causa: JavaScript convierte todo número JSON a `double` y pierde exactitud pasado 2^53, así que un identificador de 19 dígitos llega alterado → solución: transmitir los identificadores grandes como cadenas, o usar `BigInt` con un analizador que lo soporte.
- **Deserializar sin validar** → causa: el JSON entrante es entrada externa; puede faltarle un campo, traer un tipo inesperado, venir anidado a miles de niveles o pesar cientos de megas, y un `JSON.parse` optimista se lo traga todo → solución: validar contra un esquema o unos tipos comprobados en ejecución (JSON Schema, Zod, `serde` con tipos concretos), y limitar el tamaño y la profundidad.
- **Depender del orden de las claves** → causa: el estándar define los objetos JSON como colecciones **desordenadas** de pares, y ni el orden ni el espaciado están garantizados entre implementaciones → solución: no comparar documentos JSON como cadenas ni firmarlos byte a byte; compararlos ya parseados, o usar una forma canónica acordada.
- **Esperar fechas o binarios nativos** → causa: JSON no tiene ninguno de los dos tipos → solución: acordar una convención explícita, normalmente ISO 8601 en UTC para las fechas y Base64 para los binarios, y documentarla; ninguna de las dos la impone el formato.

## ❓ Preguntas frecuentes

- **¿Construir JSON a mano o con biblioteca?** Con biblioteca, siempre, en cuanto los datos no los controles tú. La biblioteca escapa las comillas, las barras y los caracteres de control, decide bien la representación de los números y no produce jamás un documento inválido. Aquí se construye a mano únicamente para que el formato exacto quede visible.
- **¿JSON solo para web?** No. Es también el formato dominante de configuración (`package.json`, `tsconfig.json`, `composer.json`), de registros estructurados —una línea JSON por evento, el patrón habitual de los sistemas de logs modernos— y de almacenamiento en bases documentales como MongoDB o en columnas `jsonb` de PostgreSQL, que además permiten indexarlo y consultarlo.
- **¿Por qué no usar XML?** Se puede, y sigue vigente donde hacen falta esquemas estrictos, espacios de nombres o firma digital. JSON ganó en la web por ser mucho menos verboso, mapear casi uno a uno con las estructuras de los lenguajes y no necesitar un analizador aparte en JavaScript.
- **¿Y si necesito más velocidad o menos tamaño?** Ahí entran los formatos binarios con esquema: Protocol Buffers, Avro, MessagePack, CBOR. Prescinden de los nombres de campo en el mensaje —van en el esquema, no en los datos— y por eso ocupan una fracción y se analizan mucho más rápido. El precio es que dejan de ser legibles y que ambos extremos deben compartir la definición del esquema y gestionar su evolución.
- **¿Qué pasa con los comentarios?** JSON no los admite, deliberadamente: Crockford los eliminó para que nadie los usara como canal de directivas de análisis. Como la configuración sí los necesita, surgieron dialectos como JSONC y JSON5, y por eso los archivos `tsconfig.json` admiten comentarios pese a no ser JSON estricto. Los analizadores estándar los rechazan.
- **¿Puedo serializar cualquier objeto?** No. JSON solo representa los seis tipos de su modelo. Las funciones, las clases con comportamiento, los manejadores de archivos y las referencias circulares no tienen representación, y una estructura cíclica hace que la serialización ingenua no termine —`JSON.stringify` lanza una excepción al detectarla—. Lo que se serializa son datos, no objetos con identidad ni conducta.

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

> [⏮️ Clase 104](../../parte-6-datos-y-estructuras/104-archivos-leer-y-escribir-texto-y-binario/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 106 ⏭️](../../parte-6-datos-y-estructuras/106-otros-formatos-y-persistencia-csv-yaml-binarios-bases-de-datos/README.md)
