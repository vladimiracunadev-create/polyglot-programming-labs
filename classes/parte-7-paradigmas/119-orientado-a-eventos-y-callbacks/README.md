# Clase 119 — Orientado a eventos y callbacks

> Parte **7 — Paradigmas** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

En los paradigmas que ya viste, tu código manda: llama a una función, recibe el valor, sigue a la línea siguiente. El paradigma **orientado a eventos** invierte esa relación. Tu programa deja de ser el guionista que dicta cada paso y se convierte en un conjunto de reacciones: declaras "cuando ocurra X, ejecuta Y", entregas ese fragmento al sistema y esperas. Es la famosa *inversión de control* que se resume en el eslogan de Hollywood: "no nos llames, nosotros te llamamos". El objetivo de esta clase es que sientas ese giro en la mano, no como una definición abstracta sino como una forma distinta de estructurar el flujo.

El motor de todo esto es un **bucle de eventos** (aquí, simplificado, un simple `for` que emite `1..n`) y una **función de callback** que tú registras una sola vez y que el emisor invoca por cada suceso. Ese callback no lo llamas tú en ningún punto del programa principal; lo entregas y desapareces. Sebesta, en su capítulo sobre manejo de eventos (*event handling*), describe este patrón como la manera natural de programar interfaces gráficas y sistemas dirigidos por entrada externa: el programa no sabe *cuándo* llegará el próximo evento, solo *qué hacer* cuando llegue.

Importa porque casi todo el software que interactúa con el mundo —una GUI, un servidor HTTP, un sensor, un navegador— está construido así. Dominar el patrón evento→callback es el primer peldaño hacia lo reactivo (clase 120) y lo asíncrono (clase 122), que son refinamientos de esta misma idea de reaccionar en vez de dictar.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Registrar un callback.
2. Emitir eventos que lo invocan.
3. Reconocer la inversión de control.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Evento | Algo que ocurre |
| 2 | Callback/manejador | Función que reacciona |
| 3 | Inversión de control | El sistema llama a tu código |

## 📖 Definiciones y características

- **Evento** — suceso al que el programa reacciona (clic, mensaje, dato). Clave: dispara callbacks.
- **Callback** — función registrada para ejecutarse cuando ocurre el evento. Clave: no la llamas tú.
- **Inversión de control** — el sistema invoca tu código, no al revés. Clave: base de la GUI y del servidor.

La pieza teórica central es la **inversión de control**. En el modelo procedural clásico —el que Abelson y Sussman desarrollan en los primeros capítulos de *SICP*— el control fluye desde tu programa hacia las funciones que llamas: tú eres el sujeto activo. El estilo de eventos da la vuelta a esa flecha. Registras un procedimiento y cedes el mando; a partir de ahí es el entorno quien decide el momento de la invocación. El callback es, en el fondo, una función de primera clase: un valor que se pasa como argumento y se guarda para invocarlo después. Sin esa capacidad —tratar funciones como datos— el paradigma de eventos sería impracticable, y por eso florece en lenguajes con clausuras (Python, JavaScript, Go) donde el callback puede además capturar su entorno.

Sebesta enmarca el manejo de eventos como una categoría propia de flujo de control, distinta de la secuencia, la selección y la iteración. Su característica definitoria es la *asincronía lógica*: el productor del evento y el consumidor están desacoplados en el tiempo. El emisor no sabe qué hará el callback y el callback no sabe cuándo lo llamarán; solo comparten un contrato (la firma del manejador). Este desacoplamiento es lo que permite que un mismo botón tenga cero, uno o muchos oyentes registrados, y que se añadan o quiten sin tocar el emisor.

Conviene distinguir *evento* de *callback*. El evento es el hecho —"llegó el dato número 3"—; el callback es la respuesta —"guárdalo en la lista". Un mismo evento puede disparar varios callbacks, y un mismo callback puede atender varios tipos de evento. En nuestro laboratorio la relación es la más simple posible (un emisor, un manejador), pero esa asimetría uno-a-muchos es la que da al patrón su potencia en sistemas reales.

## 🧩 Situación

Imagina el panel de administración de una tienda en línea. No hay un guion que diga "primero el usuario hará clic aquí, luego escribirá allá". El usuario puede pulsar cualquier botón, arrastrar cualquier fila, cerrar la pestaña en cualquier momento. El código no puede predecir el orden. Lo que hace, en cambio, es registrar manejadores: "cuando se pulse *Guardar*, valida y persiste"; "cuando llegue un mensaje del servidor, refresca la tabla". Cada manejador es un callback dormido que el bucle de eventos del navegador despierta en el instante exacto en que su suceso ocurre.

Nuestro laboratorio destila esa dinámica a su núcleo verificable: un emisor genera eventos numerados `1, 2, …, n` y un único callback los recolecta en el orden en que llegan. No hay red ni interfaz, pero la estructura es idéntica a la del panel real: se registra el manejador *antes* de que empiecen a llegar los eventos, y es el emisor —no tu línea de código— quien decide cuándo se ejecuta.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n` (número de eventos, n >= 1)
- **Salida** (stdout): `eventos=<1-2-...-n>` (orden en que llegaron)
- **Regla:** por cada i en 1..n, emitir evento i; el callback lo recolecta

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3` | `eventos=1-2-3` |
| `1` | `eventos=1` |
| `4` | `eventos=1-2-3-4` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
registrar callback ; PARA i de 1 a n: emitir(i) ; ESCRIBIR recolectados
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys

recolectados = []


def al_evento(i):
    recolectados.append(i)


n = int(sys.stdin.readline())
for i in range(1, n + 1):
    al_evento(i)
print("eventos=" + "-".join(str(x) for x in recolectados))
```

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const recolectados = [];
const alEvento = (i) => recolectados.push(i);

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
for (let i = 1; i <= n; i++) alEvento(i);
console.log(`eventos=${recolectados.join("-")}`);
```

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const recolectados: number[] = [];
const alEvento = (i: number): void => {
  recolectados.push(i);
};

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
for (let i = 1; i <= n; i++) alEvento(i);
console.log(`eventos=${recolectados.join("-")}`);
```

### Java · [`java/Main.java`](implementaciones/java/Main.java) · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;
import java.util.function.IntConsumer;
import java.util.stream.Collectors;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        List<Integer> recolectados = new ArrayList<>();
        IntConsumer alEvento = recolectados::add;
        for (int i = 1; i <= n; i++) alEvento.accept(i);
        System.out.println("eventos=" + recolectados.stream().map(String::valueOf).collect(Collectors.joining("-")));
    }
}
```

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;
using System.Collections.Generic;

int n = int.Parse(Console.In.ReadToEnd().Trim());
var recolectados = new List<int>();
Action<int> alEvento = i => recolectados.Add(i);
for (int i = 1; i <= n; i++) alEvento(i);
Console.WriteLine($"eventos={string.Join("-", recolectados)}");
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
	var recolectados []string
	alEvento := func(i int) {
		recolectados = append(recolectados, strconv.Itoa(i))
	}
	for i := 1; i <= n; i++ {
		alEvento(i)
	}
	fmt.Printf("eventos=%s\n", strings.Join(recolectados, "-"))
}
```

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn al_evento(recolectados: &mut Vec<String>, i: i64) {
    recolectados.push(i.to_string());
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let mut recolectados: Vec<String> = Vec::new();
    for i in 1..=n {
        al_evento(&mut recolectados, i);
    }
    println!("eventos={}", recolectados.join("-"));
}
```

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    printf("eventos=");
    for (long i = 1; i <= n; i++) {
        if (i > 1) printf("-");
        printf("%ld", i);
    }
    printf("\n");
    return 0;
}
```

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL no tiene eventos; se genera la secuencia con un CTE (ilustrativo, n=3).
WITH RECURSIVE e(i) AS (VALUES (1) UNION ALL SELECT i + 1 FROM e WHERE i < 3)
SELECT 'eventos=' || group_concat(i, '-') AS resultado FROM e;
```

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
$recolectados = [];
$alEvento = function ($i) use (&$recolectados) {
    $recolectados[] = $i;
};

$n = (int) trim(fgets(STDIN));
for ($i = 1; $i <= $n; $i++) {
    $alEvento($i);
}
echo "eventos=" . implode("-", $recolectados) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🧪 Laboratorio guiado — recorrido del código

Sigamos el camino de un dato desde stdin hasta la línea impresa, usando el primer caso de [`casos.json`](casos.json): entrada `3`, salida esperada `eventos=1-2-3`.

Empecemos por **Python**. La lista `recolectados = []` es el estado que sobrevive entre invocaciones del callback. La función `al_evento(i)` es el manejador: no hace más que `recolectados.append(i)`. Fíjate en que se *define* pero no se *llama* en su declaración; queda registrada, dormida, esperando. Después leemos `n = int(sys.stdin.readline())`, que con la entrada `3` deja `n = 3`. El bucle `for i in range(1, n + 1)` es nuestro emisor minúsculo: hace el papel del bucle de eventos, disparando `al_evento(1)`, `al_evento(2)`, `al_evento(3)`. Cada disparo empuja el número a la lista, de modo que `recolectados` termina siendo `[1, 2, 3]`. La última línea une esos valores con guiones y antepone el prefijo: `"eventos=" + "-".join(...)` produce exactamente `eventos=1-2-3`. Cambia la entrada a `1` y el bucle solo emite una vez: sale `eventos=1`, el segundo caso del `casos.json`; con `4`, cuatro emisiones dan `eventos=1-2-3-4`, el tercero.

El detalle pedagógico está en la *dirección de la llamada*. En un programa lineal escribirías `recolectados.append(i)` dentro del bucle y no habría callback. Aquí, en cambio, el trabajo real vive en `al_evento`, una función independiente que el emisor invoca. Esa indirección es artificial en un ejemplo tan pequeño, pero es justo la que en un sistema real te permite cambiar *qué* se hace ante cada evento sin tocar *quién* lo emite.

En **JavaScript** el patrón se ve aún más nítido porque el callback es un valor guardado en una constante: `const alEvento = (i) => recolectados.push(i);`. Esa flecha es una función de primera clase almacenada en `alEvento`, exactamente el objeto que en un navegador pasarías a `addEventListener`. Tras leer `n` con `parseInt(readFileSync(0, "utf8").trim(), 10)` —que ante la entrada `3` da `3`—, el bucle `for (let i = 1; i <= n; i++) alEvento(i)` recorre el papel de emisor y llama al manejador una vez por número. `recolectados.push(i)` va acumulando, y `recolectados.join("-")` reconstruye `1-2-3`. La plantilla `` `eventos=${...}` `` imprime `eventos=1-2-3`, idéntico al Python y a lo que exige `casos.json`.

Observa que ambos lenguajes separan tres momentos que en el mundo real ocurren en tiempos muy distintos: **registrar** el callback (definir `al_evento` / `alEvento`), **emitir** los eventos (el bucle) y **consumir** el resultado acumulado (la impresión final). En una interfaz gráfica el registro sucede al arrancar, las emisiones a lo largo de minutos de interacción, y el consumo cuando el usuario pide "guardar". Nuestro laboratorio los comprime en milisegundos, pero conserva el orden y el desacoplamiento que definen el paradigma. Si registraras el callback *después* del bucle, no recolectaría nada: por eso "registrar antes de emitir" no es un capricho, es la ley del patrón.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Callback como función pasada (Python/JS/Go), delegate (C#), interfaz (Java). |
| Semántica | El emisor invoca el callback; el flujo no es lineal. |
| Paradigmática | SQL no tiene eventos; procesa datos. |

La diferencia más real entre los lenguajes no es sintáctica sino de *qué es un callback*. En Python, JavaScript, Go, C# y PHP el manejador es simplemente una función o una clausura que se pasa como valor; en JavaScript incluso la almacenamos en `const alEvento`. Java, en cambio, no tuvo funciones de primera clase hasta las expresiones lambda de Java 8: por eso el código usa `IntConsumer alEvento = recolectados::add`, una *interfaz funcional* con un método único que la lambda implementa. Bajo el azúcar sintáctico, cada llamada al callback en Java es en realidad una invocación de método sobre un objeto anónimo. C# ocupa un terreno intermedio con sus *delegates* (`Action<int>`), que son tipos de función con nombre propio en el sistema de tipos.

La otra diferencia es la captura de estado. En PHP la clausura debe pedir explícitamente el estado externo por referencia con `use (&$recolectados)`, mientras que en Python, JavaScript o Go la clausura captura el entorno de forma automática. SQL queda fuera del paradigma: no hay noción de "evento" ni de callback, por lo que su implementación solo *ilustra* el resultado generando la secuencia con un CTE recursivo, y el verificador la marca como tal.

## 🧬 El concepto en la familia

JavaScript es el hogar natural de este estilo: el `addEventListener` del navegador y el `EventEmitter` de Node.js son bucles de eventos con registro de callbacks tal cual los describimos. Pero la idea es transversal. En Java, el patrón Observer del *Gang of Four* y los listeners de Swing/AWT son el mismo mecanismo con ropaje de interfaces; en C#, los `event` y `delegate` lo elevan a construcción del lenguaje; en Go, un canal con una goroutine que lo escucha cumple el papel de emisor-oyente. El denominador común, en todos, es la inversión de control que Sebesta identifica: tu código no pregunta "¿ya pasó algo?", sino que declara "cuando pase, haz esto".

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 119
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Callback con efectos secundarios ocultos** → causa: el manejador muta estado global que otros callbacks también tocan, y el orden de invocación deja de ser evidente; depurar se vuelve rastrear "quién modificó qué y cuándo" → solución: mantén el callback pequeño y enfocado; si necesita estado, pásalo explícitamente o encapsúlalo, como hace nuestro `recolectados` en un único lugar.
- **Olvidar registrar el manejador (o registrarlo tarde)** → causa: si el `for` emite antes de que exista `al_evento`, o si en un sistema real suscribes el listener después de que el evento ya pasó, la reacción simplemente no ocurre y no hay error visible → solución: registrar siempre *antes* de emitir; en frameworks, suscríbete en la fase de inicialización.
- **Callback hell (anidamiento profundo)** → causa: encadenar callbacks dentro de callbacks para secuenciar operaciones produce la "pirámide de la muerte", ilegible e imposible de manejar errores → solución: aplanar con funciones con nombre, o migrar a promesas/async-await (clase 122), que linealizan la secuencia.
- **Fugas por no dar de baja el oyente** → causa: registrar callbacks sin removerlos nunca mantiene vivas referencias y consume memoria en apps de larga vida → solución: emparejar cada suscripción con su cancelación (`removeEventListener`, cerrar el canal, etc.).

## ❓ Preguntas frecuentes

- **¿Callback o async/await?** Son dos capas de la misma idea. El callback es el mecanismo primitivo: registras una función que el sistema invocará. `async/await` (clase 122) es azúcar construido *encima* de esa maquinaria para escribir secuencias asíncronas como si fueran lineales, evitando el *callback hell*. Cuando solo reaccionas a un evento suelto, un callback es lo natural; cuando encadenas varios pasos dependientes, `async/await` lee mucho mejor.
- **¿Qué es exactamente la inversión de control?** Es invertir quién tiene el mando del flujo. En el estilo tradicional tu `main` llama a las bibliotecas; en el estilo de eventos entregas tu función a un framework o bucle de eventos y es él quien te llama cuando corresponde. De ahí el lema "no nos llames, te llamamos". Todo framework de UI y todo servidor se apoya en este giro.
- **¿Puedo tener varios callbacks para el mismo evento?** Sí, y es una de las ventajas del patrón. El emisor mantiene una lista de oyentes y los invoca a todos; se pueden añadir o quitar sin que el emisor cambie. Nuestro laboratorio usa uno solo por simplicidad, pero la relación uno-a-muchos es la que hace escalable el modelo.
- **¿El orden de los eventos está garantizado?** En un emisor secuencial como nuestro `for`, sí: `1`, luego `2`, luego `3`. En sistemas reales con múltiples fuentes asíncronas el orden puede variar, y ahí es donde el paradigma reactivo (clase 120) aporta operadores para ordenar y combinar flujos.

## 🔗 Referencias

**Libros de la parte:**

- P. Van Roy y S. Haridi — *Concepts, Techniques, and Models of Computer Programming* (MIT Press). Cap. 5: concurrencia por paso de mensajes y el modelo de puertos/agentes, base conceptual del emisor-receptor.
- H. Abelson y G. J. Sussman — *Structure and Interpretation of Computer Programs* (2ª ed., MIT Press). Cap. 1–2: procedimientos como valores de primera clase, el requisito que hace posible pasar callbacks.
- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson). Capítulo sobre manejo de eventos (*event handling*): la inversión de control como categoría de flujo.

**Libros de los lenguajes del núcleo:**

- L. Ramalho — *Fluent Python* (2ª ed., O'Reilly).
- M. Haverbeke — *Eloquent JavaScript* (3ª ed.) — [gratis online](https://eloquentjavascript.net/). Cap. "Handling Events".
- B. Cherny — *Programming TypeScript* (O'Reilly).
- J. Bloch — *Effective Java* (3ª ed., Addison-Wesley).
- J. Skeet — *C# in Depth* (4ª ed., Manning).
- A. Donovan y B. Kernighan — *The Go Programming Language* (Addison-Wesley).
- S. Klabnik y C. Nichols — *The Rust Programming Language* — [gratis online](https://doc.rust-lang.org/book/).
- B. Kernighan y D. Ritchie — *The C Programming Language* (2ª ed., Prentice Hall).
- C. J. Date — *SQL and Relational Theory* (3ª ed., O'Reilly).
- J. Lockhart — *Modern PHP* (O'Reilly).

---

> [⏮️ Clase 118](../../parte-7-paradigmas/118-logico-reglas-hechos-y-unificacion-prolog/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 120 ⏭️](../../parte-7-paradigmas/120-reactivo-y-flujos-de-datos-streams/README.md)
