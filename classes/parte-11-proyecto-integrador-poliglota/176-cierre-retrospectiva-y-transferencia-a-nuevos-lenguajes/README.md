# Clase 176 — Cierre: retrospectiva y transferencia a nuevos lenguajes

> Parte **11 — Proyecto integrador políglota** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Cerrar el programa: mirar hacia atrás las 176 clases y, sobre todo, mirar hacia adelante — hacia el
lenguaje que todavía no conoces. La tesis que abrió la clase 001 se cierra aquí, y conviene enunciarla otra
vez con las palabras que ahora ya significan algo: **aprender a programar no es aprender un lenguaje**. Un
lenguaje es una forma; los conceptos que esa forma expresa —vincular un nombre a un valor, decidir,
repetir, agrupar datos, aislar comportamiento tras una frontera, gestionar el fallo— son los mismos en los
diez lenguajes del núcleo, en las doce familias del Atlas y en el que se inventará el año que viene.

Que esa afirmación no sea un eslogan es lo que este programa ha intentado demostrar por medios verificables
y no retóricos. Cada una de las clases con código llevaba un `casos.json` y diez implementaciones que un
verificador ejecutaba de verdad, exigiendo la misma salida byte a byte. Esa maquinaria existía por una sola
razón: convertir "el concepto es el mismo" en un hecho comprobable en lugar de una promesa del profesor.
Cuando diez lenguajes con modelos de memoria, sistemas de tipos y paradigmas incompatibles producen la
misma línea de texto ante la misma entrada, lo que queda demostrado es que había algo debajo de los diez
que no dependía de ninguno. Ese algo —el algoritmo, el concepto, la idea— es lo que te llevas. La sintaxis
se olvida en meses; eso, no.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Hacer una retrospectiva honesta del proyecto: qué funcionó, qué costó más de lo previsto y qué harías distinto.
2. Enunciar y defender la tesis de la transferencia con ejemplos propios de las tres clases de diferencia.
3. Abordar un lenguaje desconocido situándolo en su familia del Atlas y aprendiendo solo sus deltas.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Retrospectiva | Registrar lo aprendido para no volver a pagarlo |
| 2 | Transferencia | Reconocer el mismo concepto bajo otra forma |
| 3 | Las tres diferencias | El marco que convierte lo desconocido en deltas |
| 4 | Siguiente lenguaje | Situarlo en su familia del Atlas y estudiar solo lo nuevo |

## 📖 Definiciones y características

La **retrospectiva** es la mirada estructurada hacia atrás al cerrar un trabajo: qué salió bien, qué costó
más de lo previsto y qué se hará distinto la próxima vez. Su valor no está en el desahogo sino en el
registro: una lección que no se escribe se vuelve a aprender pagándola otra vez. La **transferencia** es
aplicar a un contexto nuevo lo aprendido en otro, y es la tesis entera de este programa. El **aprendizaje
por familia** es el método concreto que la hace operativa: en lugar de estudiar un lenguaje nuevo desde
cero, se lo sitúa en su parentesco —de las doce familias del Atlas— y se aprenden únicamente sus
diferencias respecto a lo que ya conoces.

Ese método descansa en el marco que dimos en la clase 002 y que hemos usado en cada comparación desde
entonces: toda diferencia entre dos lenguajes es de una de tres clases. Las **sintácticas** —dónde van las
llaves, si el punto y coma es obligatorio, cómo se declara una función— son las que más ruido hacen al
principio y las que menos importan: se absorben en días con un editor y práctica. Las **semánticas** son
las peligrosas, porque el código compila y parece correcto mientras se comporta distinto: si un valor se
copia o se mueve, si `==` compara identidad o contenido, si un entero desborda en silencio o revienta, si
el error viaja como excepción o como valor de retorno. Y las **paradigmáticas** son las que exigen cambiar
de mentalidad —de recorrer con bucles a describir conjuntos como en SQL, de mutar estado a componer
funciones, de compartir memoria a pasar mensajes—; son las más lentas de adquirir y también las que más te
cambian como programador. La consecuencia práctica es una regla de estudio: dedica una tarde a la sintaxis
y todo el resto del tiempo a lo semántico y lo paradigmático, porque ahí está lo que de verdad no sabes.

Y hay un cierre que conviene dejar dicho con honestidad, porque un curso que solo celebra sus tesis no
sirve de mucho. La transferencia es real, pero no es gratuita ni instantánea: reconocer un concepto en un
lenguaje nuevo te da la mitad del camino, y la otra mitad —el idiomatismo, las bibliotecas, las trampas
que la comunidad ya conoce, el porqué de sus convenciones— solo se compra con horas de escribir código en
él. Lo que has ganado en estas 176 clases no es la capacidad de saltarte esa segunda mitad, sino la de
llegar a ella el primer día en vez del sexto mes.

## 🧩 Situación

Es tu primer día en un equipo y el sistema está escrito en Elixir, un lenguaje que no has tocado nunca.
La versión de ti que empezó este programa habría buscado un curso de veinte horas y habría empezado por el
"hola mundo". La versión de ti que termina esta clase hace otra cosa: abre el Atlas, lo sitúa en la familia
**concurrente / actor**, y con eso ya sabe lo esencial antes de leer una línea —que el estado no se
comparte sino que vive dentro de procesos ligeros que se comunican por mensajes, que el fallo se gestiona
dejando morir el proceso y reiniciándolo en vez de atrapar excepciones, que la inmutabilidad no es una
recomendación sino la regla—. Después mira los deltas: la sintaxis viene de Ruby, el modelo de ejecución de
Erlang, el emparejamiento de patrones lo comparte con Rust y con las familias funcionales tipadas. En dos
días estás leyendo el código del equipo con criterio. No porque sepas Elixir, sino porque sabes **dónde
mirar** — y eso es exactamente lo que este programa te ha entrenado a hacer.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n` (número de lecciones que te llevas)
- **Salida** (stdout): `lecciones=<n> transferible=si`
- **Regla:** informar las lecciones y confirmar la transferibilidad

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `lecciones=5 transferible=si` |
| `12` | `lecciones=12 transferible=si` |
| `1` | `lecciones=1 transferible=si` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER n ; ESCRIBIR lecciones=n transferible=si
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys

n = int(sys.stdin.readline())
print(f"lecciones={n} transferible=si")
```

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`lecciones=${n} transferible=si`);
```

🧬 **El mismo programa en la familia JavaScript / web:** [Dart · ActionScript](primos.md#javascript-web)

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`lecciones=${n} transferible=si`);
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
        int n = Integer.parseInt(br.readLine().trim());
        System.out.println("lecciones=" + n + " transferible=si");
    }
}
```

🧬 **El mismo programa en la familia JVM:** [Kotlin · Scala · Groovy · Clojure](primos.md#jvm)

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;

int n = int.Parse(Console.In.ReadToEnd().Trim());
Console.WriteLine($"lecciones={n} transferible=si");
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
	n, _ := strconv.Atoi(strings.TrimSpace(line))
	fmt.Printf("lecciones=%d transferible=si\n", n)
}
```

🧬 **El mismo programa en la familia Sistemas:** [Zig · Nim · D](primos.md#sistemas)

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    println!("lecciones={n} transferible=si");
}
```

🧬 **El mismo programa en la familia Sistemas:** [Zig · Nim · D](primos.md#sistemas)

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    printf("lecciones=%ld transferible=si\n", n);
    return 0;
}
```

🧬 **El mismo programa en la familia C / llaves:** [C++ · Objective-C](primos.md#c-llaves)

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL, la ultima vez: la misma idea, otra forma.
WITH t(n) AS (VALUES (5))
SELECT printf('lecciones=%d transferible=si', n) AS resultado FROM t;
```

🧬 **El mismo programa en la familia Lógica y declarativa:** [Prolog · Datalog](primos.md#logica-declarativa)

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
$n = (int) trim(fgets(STDIN));
echo "lecciones=$n transferible=si\n";
```

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🧪 Recorrido del código

Por última vez, el contrato ([`casos.json`](casos.json)) es mínimo a propósito: entra `5`, sale
`lecciones=5 transferible=si`. Leer un entero y componer una frase — la misma operación elemental que
hicimos en la clase 001, cuando aún no sabíamos qué significaba. Mírala ahora y verás en ella todo el
programa condensado.

Empieza por lo que hay debajo de las diez implementaciones: una entrada de texto que hay que **interpretar**
como número. Python lo hace con `int()`, Java con `Integer.parseInt`, Go con `strconv.Atoi`, Rust con
`.parse()` guiado por la anotación `let n: i64`, C con `scanf("%ld", &n)`, PHP con una conversión `(int)`.
Diez formas de la misma idea —convertir una secuencia de caracteres en un valor numérico—, y bajo esa idea,
todo lo que estudiamos: la representación de los enteros y su desbordamiento, la diferencia entre tipado
estático y dinámico, la política de errores de cada lenguaje, el modelo de memoria que decide si esa cadena
se copia, se presta o se mueve. Ninguna de esas cosas se ve en la línea, y todas están ahí.

Luego está la composición de la frase, con la interpolación de Python, Rust, C#, JS/TS y PHP frente al
formateo por especificadores de Go y C, la concatenación de Java y el `printf` declarativo de SQL. Y está,
por última vez, la nota al pie de siempre: SQL no lee de stdin, porque su modelo no es un flujo de
caracteres sino un conjunto de filas. Esa excepción, que ha aparecido en decenas de clases, es el
recordatorio más útil del programa: la equivalencia de los conceptos no significa que todos los lenguajes
sean intercambiables. Significa que puedes reconocer la misma idea vestida de formas radicalmente
distintas — y elegir, con criterio, cuál de esas formas conviene a cada problema.

## 🔬 Comparación

Una última tabla, y esta resume el programa entero más que la clase.

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | La misma frase en diez escrituras: interpolación, `+`, `%d`, `printf`. Es la capa que más asusta al principio y la que se aprende en una tarde. |
| Semántica | Bajo una operación idéntica siguen latiendo el tipado, el desbordamiento, la política de errores y el modelo de memoria: lo que hace que el mismo código se comporte distinto. |
| Paradigmática | Nueve lenguajes leen un flujo y nueve imprimen; SQL declara un resultado sobre un conjunto. La frontera imperativo/declarativo, visible hasta en el programa más trivial. |

Si te quedas con una sola idea de las 176 clases, que sea esta: **la tabla de arriba es el método**. Ante
cualquier lenguaje nuevo, cualquier fragmento de código ajeno, cualquier decisión técnica que no entiendas,
las tres preguntas son siempre las mismas. ¿Esto se escribe distinto pero significa lo mismo? ¿Significa
algo distinto aunque se escriba igual? ¿O me está pidiendo pensar el problema de otra manera? La primera
pregunta se responde con la documentación, la segunda con experimentos, y la tercera con tiempo. Saber cuál
de las tres tienes delante es la competencia que separa a quien traduce código de quien lo escribe.

## 🧬 El concepto en la familia

Aquí termina el recorrido, así que conviene dejar el mapa desplegado. El Atlas organiza el paisaje en doce
familias: la de **C y las llaves**, el **scripting dinámico**, la **JVM**, **.NET**, **JavaScript y la
web**, la **funcional tipada** heredera de ML, **Lisp**, la **lógica y declarativa**, la **concurrente y de
actores**, la de **sistemas**, la de **arrays y computación científica**, y los **históricos**. Los diez
lenguajes del núcleo que has implementado y verificado cubren cinco o seis de ellas: sabes leer un lenguaje
de llaves, uno dinámico, uno de la JVM, uno de .NET, uno de sistemas con gestión manual o por propiedad de
la memoria, y uno declarativo. Las familias que te faltan no son territorio hostil: son deltas conocidos
sobre lo que ya dominas.

El procedimiento para abordar cualquiera de ellas es el mismo que has ensayado clase tras clase. Primero,
sitúa el lenguaje en su familia y averigua de quién heredó qué. Segundo, responde cinco preguntas que
resuelven el 80 % del comportamiento: cómo se declara y vincula un valor, si el tipado es estático o
dinámico y cuánto infiere, cómo se gestiona la memoria, cómo viaja un error y cómo se modulariza y se
importa código. Tercero, escribe en él un programa que ya sepas escribir en otro lenguaje —el mismo
`casos.json` sirve— y compara tu versión con la de alguien experto para descubrir en qué no eres idiomático
todavía. Cuarto, lee su libro canónico: los diez que aparecen abajo son las puertas de entrada a sus
familias, y para el lenguaje que elijas casi siempre existe uno equivalente. Ese es el ciclo que este
programa te deja, y funciona igual con el undécimo lenguaje que con el trigésimo.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 176
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Creer que hay que empezar de cero con cada lenguaje** → causa: se confunde la sintaxis desconocida con desconocimiento del concepto, y se repite un curso de introducción que ya no hace falta → solución: identificar la familia, dar por sabido lo transferible y estudiar únicamente los deltas semánticos y paradigmáticos.
- **Creer lo contrario: que basta con traducir la sintaxis** → causa: el exceso de confianza del error anterior, invertido; se escribe Python con llaves y se llama a eso saber Go → solución: buscar deliberadamente las diferencias semánticas (memoria, errores, tipos) y escribir idiomático, aunque cueste más al principio.
- **Coleccionar lenguajes en vez de profundizar en alguno** → causa: la transferencia hace fácil el primer contacto y adictiva la novedad → solución: alternar amplitud y profundidad; llevar al menos un lenguaje hasta el nivel en que conoces sus trampas, porque esa profundidad es la que da criterio para juzgar a los demás.
- **Detener el aprendizaje aquí** → causa: se toma el final del programa por el final del recorrido → solución: aplicar el método a un lenguaje nuevo cada cierto tiempo; lo que has aprendido no es un temario cerrado sino una forma de abordar lo que venga.

## ❓ Preguntas frecuentes

- **¿Y ahora qué?** Elige del Atlas una familia que no hayas tocado —la funcional tipada, Lisp o la de actores son las que más te cambiarán la cabeza— y aborda un lenguaje suyo con el ciclo de esta clase: familia, cinco preguntas, un programa que ya sabes escribir, y su libro canónico. Comprobarás la transferencia en el primer fin de semana.
- **¿Se acabó el aprendizaje?** El programa sí; el método no. Su valor está justamente en que no caduca: los lenguajes que domines dentro de diez años probablemente aún no existen, y los abordarás con estas mismas tres preguntas.
- **¿Qué leo después?** Los libros que han sostenido este curso siguen valiendo por sí solos. Para seguir comparando lenguajes, Sebesta (*Concepts of Programming Languages*) y Van Roy y Haridi (*Concepts, Techniques, and Models of Computer Programming*). Para entender qué hay debajo, Nystrom (*Crafting Interpreters*), que es gratuito y se lee construyendo. Para el oficio, Hunt y Thomas (*The Pragmatic Programmer*) y, si vas hacia sistemas distribuidos, Newman y Nygard. Y para cada lenguaje nuevo, su libro de referencia: la lista de abajo es el modelo de lo que hay que buscar.
- **¿Cuánto de esto se me va a olvidar?** La sintaxis, casi toda, y no importa: se recupera en minutos con la documentación. Lo que no se olvida es lo que has entrenado: saber qué preguntar, dónde mirar y cómo distinguir una diferencia superficial de una que te va a costar un incidente en producción.

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

> [⏮️ Clase 175](../../parte-11-proyecto-integrador-poliglota/175-documentacion-y-defensa-de-las-decisiones-de-lenguaje/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md)
