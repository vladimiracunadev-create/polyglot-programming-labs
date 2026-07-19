# Clase 163 — Incrustar un lenguaje en otro (Lua, Python embebido)

> Parte **10 — Interoperabilidad y fronteras entre lenguajes** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Las clases anteriores cruzaron fronteras entre *iguales*: dos servicios que se llaman, dos procesos que se pasan bytes. Incrustar un lenguaje invierte la relación y la vuelve **jerárquica**: hay un anfitrión —el programa compilado, dueño del proceso, de la memoria y del bucle principal— y hay un intérprete que vive dentro de él y solo ejecuta cuando el anfitrión se lo pide. No son dos pares negociando: es un lenguaje ejecutando a otro.

La razón de hacerlo es casi siempre el **ciclo de cambio**. Un motor de videojuego en C++ tarda minutos en compilar; ajustar el equilibrio de un arma no debería costar una compilación. Un servidor de bases de datos no puede recompilarse para que un cliente añada su lógica. Un editor no puede prever todos los flujos de trabajo de sus usuarios. En los tres casos, la solución es la misma: dar al usuario un lenguaje interpretado, más lento pero editable en caliente y seguro de fallar. El objetivo de esta clase es entender cómo funciona esa frontera de verdad —qué expone el anfitrión, cómo se pasan los valores, qué pasa cuando el script falla o no termina— y por qué la elección del lenguaje embebido depende más del tamaño y del aislamiento que de la potencia.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. **Evaluar** un script embebido con datos que provee el anfitrión.
2. **Explicar** por qué se embebe un intérprete y qué se gana frente a recompilar.
3. **Reconocer** los casos canónicos (juegos, *plugins*, Redis, Nginx) y su patrón común.
4. **Identificar** los riesgos de la frontera: seguridad, memoria, errores y bucles infinitos.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Lenguaje embebido | Un intérprete dentro de la app |
| 2 | Anfitrión y script | Quién ejecuta a quién |
| 3 | Extensibilidad | Cambiar comportamiento sin recompilar |

## 📖 Definiciones y características

Un **lenguaje embebido** es un intérprete que se enlaza como una biblioteca dentro de otra aplicación, en lugar de correr como programa independiente. El caso arquetípico es Lua: su intérprete completo son unos pocos miles de líneas de C ANSI y unos cientos de kilobytes compilado, sin dependencias más allá de la biblioteca estándar de C. Ese tamaño no es una curiosidad — es la razón de su éxito. Un intérprete que quepa en el binario del anfitrión y arranque en microsegundos puede crearse y destruirse por cada petición; uno que pese decenas de megabytes y tarde en inicializar, no.

El **anfitrión** conserva el control absoluto. Crea un *estado* del intérprete (en Lua, un `lua_State`), decide qué funciones y datos registrar en él, y llama al script pasándole argumentos. Lo decisivo es lo que ocurre por omisión: **si el anfitrión no registra algo, el script no puede usarlo**. Un script Lua en un juego no puede abrir archivos si el anfitrión no expuso `io`; en Redis, un script no puede hacer red porque solo se le registraron las funciones de acceso a claves. La superficie de lo posible es una lista explícita, y eso convierte al intérprete embebido en un mecanismo de aislamiento además de en uno de extensibilidad.

La frontera funciona con **traducción de valores**, no con memoria compartida. Un número de C no es un número de Lua, y una tabla de Lua no es un `struct`. Lua resuelve esto con una **pila** en la que el anfitrión empuja los argumentos (`lua_pushnumber`), llama (`lua_pcall`) y saca el resultado (`lua_tonumber`). Es el mismo *marshalling* de la FFI y de Wasm, con la misma consecuencia: cruzar cuesta, y un script llamado un millón de veces por fotograma es un problema de rendimiento aunque su cuerpo sea trivial. También cuesta la **propiedad de la memoria**: el intérprete tiene su propio recolector de basura, ajeno al del anfitrión, y un puntero del anfitrión guardado en el script puede quedar colgando cuando el anfitrión lo libera.

Y está la parte que se descubre en producción: el script es **código ajeno que puede fallar**. Puede lanzar un error, puede devolver un tipo que no esperabas, y puede entrar en un bucle infinito. Un error sin capturar que cruce hacia el anfitrión lo tumba entero, y por eso las API de embebido ofrecen llamadas protegidas (`lua_pcall` frente a `lua_call`) que convierten el fallo del script en un valor de retorno. Los bucles infinitos son peores porque ninguna API los previene sola: hay que instalar un *hook* que cuente instrucciones y aborte, o ejecutar el script con un presupuesto. Nygard describe en *Release It!* justamente este patrón — un componente integrado sin límite de tiempo acaba consumiendo todos los hilos del anfitrión — y aplica igual a un script embebido que a una llamada remota.

- **Lenguaje embebido** — intérprete enlazado como biblioteca dentro de una aplicación anfitriona (Lua, Python, JS). Clave: cambiar comportamiento sin recompilar ni reiniciar.
- **Anfitrión** — la aplicación que hospeda el intérprete y le registra funciones y datos. Clave: lo que no expone, el script no puede tocar.
- **Script embebido** — código interpretado que corre dentro del proceso del anfitrión. Clave: extiende la app, pero puede fallar y hay que contenerlo.

## 🧩 Situación

En un juego, la física y el renderizado son C++ compilado; el comportamiento de cada enemigo es un script Lua. Un diseñador ajusta el daño de un arma, guarda el archivo, el motor recarga el script y el cambio se ve sin compilar ni reiniciar la partida. El mismo patrón aparece en sitios que no parecen relacionados: Redis ejecuta scripts Lua para hacer atómicas varias operaciones sobre claves; Nginx enruta peticiones con Lua a través de OpenResty; Blender y GIMP exponen Python para automatizar; VS Code ejecuta las extensiones en JavaScript sobre el V8 que ya trae Electron. En todos, la estructura es idéntica: el anfitrión entrega los datos, el script decide, el anfitrión recibe el resultado. Para aislar esa esencia, aquí el anfitrión entrega dos números al script embebido, el script los suma y devuelve el resultado.

## 🧮 Modelo

- **Entrada** (stdin): una línea `a b` (los datos que el anfitrión pasa al script)
- **Salida** (stdout): `resultado=<a+b>` (lo que el script calcula)
- **Regla:** el script embebido evalúa a + b

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3 4` | `resultado=7` |
| `10 5` | `resultado=15` |
| `0 0` | `resultado=0` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
anfitrión pasa a, b ; el script suma ; devuelve el resultado
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys

a, b = map(int, sys.stdin.readline().split())
script = "a + b"  # el script embebido
resultado = eval(script, {}, {"a": a, "b": b})
print(f"resultado={resultado}")
```

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const [a, b] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
// El anfitrion evalua el script embebido con los datos.
const resultado = a + b;
console.log(`resultado=${resultado}`);
```

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const [a, b] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const resultado: number = a + b;
console.log(`resultado=${resultado}`);
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
        int a = Integer.parseInt(p[0]), b = Integer.parseInt(p[1]);
        System.out.println("resultado=" + (a + b));
    }
}
```

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
int a = int.Parse(p[0]), b = int.Parse(p[1]);
Console.WriteLine($"resultado={a + b}");
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
	f := strings.Fields(line)
	a, _ := strconv.Atoi(f[0])
	b, _ := strconv.Atoi(f[1])
	fmt.Printf("resultado=%d\n", a+b)
}
```

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let v: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    println!("resultado={}", v[0] + v[1]);
}
```

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long a, b;
    if (scanf("%ld %ld", &a, &b) != 2) return 1;
    printf("resultado=%ld\n", a + b);
    return 0;
}
```

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL se embebe en apps via librerias cliente; aqui, la suma.
WITH t(a, b) AS (VALUES (3, 4))
SELECT printf('resultado=%d', a + b) AS resultado FROM t;
```

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
[$a, $b] = array_map('intval', preg_split('/\s+/', trim(fgets(STDIN))));
echo "resultado=" . ($a + $b) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔎 Recorrido del código (laboratorio)

El caso `3 4` debe producir `resultado=7`. El anfitrión lee dos números de su entrada, se los entrega al script y publica lo que el script devuelve. La suma es lo de menos; lo que importa es la coreografía de los tres pasos.

En **Python** el ejemplo es literal, no simulado: `script = "a + b"` es una cadena de código, y `eval(script, {}, {"a": a, "b": b})` la ejecuta. Los dos diccionarios son la parte instructiva. El segundo es el entorno local con los datos que el anfitrión entrega — el equivalente a empujar argumentos en la pila de Lua. El primero, `{}`, es el entorno global vacío: un intento de restringir lo que el script ve. Y aquí conviene ser claro, porque es un error clásico: **eso no es un sandbox**. Python inserta `__builtins__` automáticamente si no se lo impides, y aunque lo hagas, desde un objeto cualquiera se puede navegar la jerarquía de clases hasta alcanzar cosas peligrosas. Aislar Python de verdad requiere otro proceso, un intérprete restringido o un módulo Wasm — el mecanismo de la clase 162. Como demostración del patrón, `eval` es perfecto; como diseño para código de terceros, es una vulnerabilidad.

En **JavaScript** el comentario `// El anfitrion evalua el script embebido con los datos.` marca dónde estaría la llamada real. Node ofrece el módulo `vm` para ejecutar código en un contexto separado, y navegadores y aplicaciones Electron incrustan V8 con la misma estructura. Vale la pena notar la asimetría con Python: en el mundo JS, el anfitrión suele *ser* el motor del lenguaje, así que la frontera entre anfitrión y script es más difusa — y, por lo mismo, más fácil de cruzar sin querer.

En **C** la simulación es la más honesta respecto a lo real, precisamente porque C es el anfitrión clásico. `scanf("%ld %ld", &a, &b)` y `printf` rodean a `a + b`; en la versión real, ese `a + b` se sustituiría por empujar `a` y `b` a la pila de Lua, invocar `lua_pcall`, comprobar si devolvió error y recoger el número resultante. La secuencia leer → empujar → llamar protegido → recoger es exactamente la que aparece en el código de cualquier motor de juego.

En **Rust**, `v[0] + v[1]` sobre un vector parseado esconde una tensión interesante: incrustar un intérprete en Rust obliga a decidir quién posee la memoria de los valores que cruzan. Las crates de la comunidad (`mlua`, `rlua`, `rhai`) resuelven esto con tipos que atan la vida del valor a la del estado del intérprete, de modo que el compilador impide guardar una referencia al script más allá de su validez — el mismo problema de propiedad de la clase 156, aquí resuelto por el sistema de tipos en lugar de por disciplina.

## 🔬 Comparación

| Lenguaje | Su papel en el patrón anfitrión/script |
|---|---|
| C | El anfitrión canónico: la API de Lua (`lua_State`, `lua_pcall`) está pensada para C. |
| C# | Anfitrión con `Microsoft.ClearScript` (V8), IronPython o `Roslyn` para compilar y ejecutar C# en caliente. |
| Java | Anfitrión con `ScriptEngine` (JSR-223) y GraalVM Polyglot, que ejecuta JS, Python y Ruby en el mismo proceso. |
| Rust | Anfitrión con `mlua`/`rlua` (Lua), `rhai` (script propio) o `deno_core` (V8); la propiedad de valores la vigila el compilador. |
| Go | Anfitrión con `gopher-lua` (Lua puro en Go) o `go-lua`; también `cgo` hacia el Lua original. |
| Python | Puede ser ambos: se embebe en C con `Python.h` (Blender, GIMP) y a la vez embebe scripts con `eval`/`exec`. |
| JavaScript | Motor embebible por excelencia (V8, QuickJS, JavaScriptCore); Electron y VS Code viven de ello. |
| TypeScript | No se embebe directamente: se transpila a JS y lo ejecuta el motor. |
| PHP | Raramente anfitrión; sí ejecuta código con `eval`, con los mismos riesgos que en Python. |
| SQL | Es el caso inverso: se embebe *en* las apps como lenguaje de consulta, y a su vez los motores embeben Lua (Redis) o PL/Python. |

Bajo la variedad sintáctica hay dos decisiones semánticas repetidas. La primera es el **aislamiento del estado**: si el intérprete es barato de crear (Lua, QuickJS), el anfitrión puede darle un estado nuevo a cada script y evitar que uno contamine a otro; si es caro (CPython, la JVM), se comparte un estado y hay que limpiar entre ejecuciones. La segunda es **quién posee la memoria**: dos recolectores de basura conviviendo en un proceso, ninguno consciente del otro, es una fuente clásica de fugas y punteros colgantes; por eso las bibliotecas modernas envuelven los valores en tipos que atan la vida del dato a la del intérprete. GraalVM merece mención aparte porque persigue algo más ambicioso: ejecutar varios lenguajes sobre un mismo runtime con objetos compartidos de verdad, sin traducción en la frontera. Es la promesa de eliminar el coste del *marshalling*, aunque a cambio de atarse a una implementación concreta.

## 🧬 El concepto en la familia

El paisaje se ordena por tamaño y por propósito. **Lua** domina donde el intérprete debe ser diminuto y arrancar instantáneamente: juegos, Redis, Nginx/OpenResty, Wireshark. **Python** domina donde el script necesita un ecosistema rico y el anfitrión es una herramienta de escritorio: Blender, GIMP, QGIS, la mayoría de aplicaciones científicas. **JavaScript** domina el mundo de las extensiones de aplicaciones modernas porque el motor V8 ya estaba en el proceso. **SQL** aparece en todos lados como lenguaje embebido de consulta. Y los motores de reglas de negocio (Drools, Rhai, CEL) resuelven el mismo problema con lenguajes deliberadamente limitados, sin bucles ni E/S, donde la terminación está garantizada por construcción. La tendencia actual apunta a sustituir el intérprete embebido por un módulo **WebAssembly**: mismo beneficio —extensibilidad sin recompilar— con un aislamiento verificable y sin obligar al usuario a un único lenguaje de scripting. Es la clase 162 reapareciendo como respuesta a los problemas de esta.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 163
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Exponer demasiado al script** → causa: registrar la biblioteca estándar completa da al script acceso a archivos, red y procesos → solución: registrar solo las funciones necesarias; partir de una lista blanca vacía, nunca de restar a lo que ya está.
- **Confiar en un sandbox improvisado** → causa: `eval(script, {}, ...)` con globales vacíos *no* aísla Python; se puede escapar navegando la jerarquía de objetos → solución: si el código es de terceros, usar otro proceso con límites del sistema operativo, o un módulo Wasm.
- **No validar lo que devuelve el script** → causa: el anfitrión asume un número y recibe `nil`, una cadena o una tabla enorme → solución: comprobar tipo y rango en la frontera, como con cualquier entrada externa.
- **Dejar que un error del script tumbe al anfitrión** → causa: usar una llamada no protegida y propagar la excepción al proceso principal → solución: invocar siempre en modo protegido (`lua_pcall` y equivalentes) y tratar el fallo como un valor.
- **No limitar el tiempo ni la memoria** → causa: un `while true` en un script cuelga el hilo del anfitrión indefinidamente → solución: instalar un *hook* que cuente instrucciones y aborte, o ejecutar con un presupuesto y un *timeout*, como aconseja Nygard.
- **Cruzar la frontera en el bucle caliente** → causa: llamar al script por cada entidad y por cada fotograma multiplica el coste de empujar y recoger valores → solución: llamar una vez con un lote, o mantener en el anfitrión lo que se ejecuta muy a menudo.
- **Ignorar la interacción entre los dos recolectores de basura** → causa: guardar en el script un puntero a memoria del anfitrión, que este libera después → solución: envolver los objetos del anfitrión en tipos con vida controlada y no guardar referencias crudas.

## ❓ Preguntas frecuentes

- **¿Por qué embeber un lenguaje?** Para separar lo que cambia despacio (motor, rendimiento, compilado) de lo que cambia a diario (reglas, contenido, personalización). Permite que quien ajusta el comportamiento —diseñador, administrador, usuario avanzado— no dependa del ciclo de compilación ni sepa C++.
- **¿Lua o Python?** Lua si el intérprete debe ser diminuto, arrancar en microsegundos y crearse por petición: juegos, servidores, dispositivos. Python si el script necesita bibliotecas reales y quien lo escribe ya sabe Python: herramientas de escritorio, ciencia, automatización. El tamaño y el arranque deciden más que la potencia del lenguaje.
- **¿Es más lento que compilar la lógica?** Sí, entre uno y dos órdenes de magnitud según el caso, y además cada cruce de frontera cuesta. Se acepta porque la lógica scripteada suele ser una fracción mínima del tiempo total: el 95 % del trabajo sigue en el código compilado del anfitrión.
- **¿Puedo recargar scripts sin reiniciar?** Ese es el atractivo principal, y funciona si el script es sin estado o si el anfitrión sabe reconstruir el estado tras recargar. Cuando el script guarda estado propio, la recarga se complica y hay que decidir explícitamente qué se conserva.
- **¿Y si prefiero no atarme a un lenguaje de scripting?** Esa es la propuesta de WebAssembly como capa de extensión: el usuario escribe el *plugin* en Rust, Go o C, y el anfitrión ejecuta el módulo con un aislamiento verificable y límites de recursos. Es más trabajo de integración y menos inmediato de editar, pero mucho más seguro con código de terceros.

## 🔗 Referencias

**Libros de la parte:**

- M. Kleppmann — *Designing Data-Intensive Applications* (O'Reilly). Cap. 4: traducción de valores entre representaciones y coste de la frontera.
- S. Newman — *Building Microservices* (2ª ed., O'Reilly). Extensibilidad y aislamiento de código de terceros dentro de un componente.
- A. Tanenbaum y M. van Steen — *Distributed Systems* (3ª ed.). Código móvil, agentes y ejecución de lógica ajena en el propio proceso.
- M. Nygard — *Release It!* (2ª ed., Pragmatic Bookshelf). *Timeouts* y límites de recursos: contener un componente integrado que no termina.

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

> [⏮️ Clase 162](../../parte-10-interoperabilidad-y-fronteras-entre-lenguajes/162-webassembly-como-objetivo-comun/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 164 ⏭️](../../parte-10-interoperabilidad-y-fronteras-entre-lenguajes/164-elegir-el-lenguaje-correcto-para-cada-componente/README.md)
