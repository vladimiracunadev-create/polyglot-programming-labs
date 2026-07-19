# Clase 087 — Visibilidad, encapsulación y contratos (public/private)

> Parte **5 — Funciones y modularidad** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Entender la encapsulación no como una regla de etiqueta («no toques los campos ajenos») sino como el mecanismo que hace confiable a un objeto. Un tipo encapsulado guarda su estado interno tras una pared —lo declara **privado**— y ofrece hacia fuera solo un puñado de operaciones con significado —el contrato **público**—. La consecuencia es poderosa: si el único modo de tocar el saldo es a través de `depositar` y `retirar`, entonces esos dos métodos son los únicos lugares donde el saldo puede volverse inválido, y basta escribirlos bien una vez para que el resto del programa no pueda romper nunca la regla `saldo >= 0`. La pared no está para ocultar por ocultar: está para reducir a un puñado de puntos los sitios donde algo puede salir mal.

La idea nace de David Parnas y su ocultamiento de información, y McConnell la desarrolla en *Code Complete* (cap. 6, «Working Classes»): una clase bien diseñada expone una interfaz que es una abstracción coherente y esconde tras ella todo lo que podría cambiar. Joshua Bloch la eleva a consejo de cabecera en *Effective Java* con el ítem «Minimize the accessibility of classes and members»: haz cada declaración tan inaccesible como el programa permita. La razón es de acoplamiento —cuanto menos expones, menos código ajeno depende de tus detalles internos, y más libre eres de cambiarlos—.

Esta clase practica el gesto fundacional: una `Cuenta` con un saldo privado y un método `depositar` que lo modifica de forma controlada. Verás que los diez lenguajes tienen opiniones muy distintas sobre cómo se dibuja esa pared: algunos la hacen cumplir con el compilador (Java, Rust, C#), otros la dejan a la palabra dada (Python, con su convención del guion bajo), y uno —Go— decide la visibilidad por algo tan simple como la mayúscula inicial del nombre.

## 🧩 Situación

Piensa en una cuenta bancaria representada con un campo `saldo` público, accesible desde cualquier parte del programa. Todo funciona hasta que, en algún módulo remoto escrito meses después, alguien hace `cuenta.saldo -= comision` sin comprobar nada, y una cuenta con dos euros queda en menos ocho. La regla del negocio —«el saldo nunca es negativo»— existía en la cabeza del programador original, pero no en el código: nada la protegía. Encapsular convierte esa regla en algo que la máquina custodia. Si `saldo` es privado y solo `retirar` puede disminuirlo, entonces `retirar` es el único guardián que debe comprobar `if (monto <= saldo)`, y ningún módulo lejano puede saltárselo porque, sencillamente, no alcanza el campo. La invariante deja de ser una promesa verbal y pasa a ser una propiedad estructural del programa. Aquí ensayamos la base de esa idea: dos depósitos de `n` sobre un saldo que empieza en cero y solo se toca por métodos.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n` (monto de cada depósito)
- **Salida** (stdout): `saldo=<2n>` (tras depositar n dos veces)
- **Regla:** cuenta.depositar(n) dos veces; saldo = 2n

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `50` | `saldo=100` |
| `0` | `saldo=0` |
| `30` | `saldo=60` |

## 📖 Definiciones y características

- **Encapsulación** — agrupar los datos y las operaciones que los manejan en una sola unidad, y ocultar los datos tras las operaciones. No es meramente «poner variables dentro de una clase»: es garantizar que el estado solo se toca por caminos que respetan sus reglas. McConnell la describe como el rasgo que distingue una clase de un simple montón de variables globales con nombres bonitos.

- **Privado** — accesible solo desde dentro del propio tipo. Es la cara oculta: lo que puedes cambiar mañana sin avisar a nadie porque nadie de fuera depende de ello. Cuanto más grande sea la parte privada respecto a la pública, más margen tienes para evolucionar el código.

- **Público** — la parte visible, el contrato que otros usan y del que dependen. Todo lo público es una promesa que te obliga: mientras alguien lo use, no puedes cambiarlo a la ligera. Por eso Bloch aconseja minimizarlo —cada miembro público es una atadura futura—.

- **Contrato** — el conjunto de operaciones públicas y lo que prometen hacer. `depositar(n)` promete «aumentar el saldo en n»; quien la llama no necesita —ni debe— saber cómo está guardado el saldo por dentro. El contrato es estable; la implementación es libre.

- **Invariante** — una regla que el objeto cumple siempre, entre operación y operación (por ejemplo, `saldo >= 0`). La encapsulación es lo que la protege: si todas las mutaciones pasan por métodos que respetan la invariante, esta no puede romperse desde fuera.

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER n
cuenta <- nueva Cuenta()
cuenta.depositar(n) ; cuenta.depositar(n)
ESCRIBIR "saldo=" cuenta.saldo()
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys


class Cuenta:
    def __init__(self):
        self._saldo = 0  # privado por convención

    def depositar(self, monto):
        self._saldo += monto

    def saldo(self):
        return self._saldo


n = int(sys.stdin.readline())
c = Cuenta()
c.depositar(n)
c.depositar(n)
print(f"saldo={c.saldo()}")
```

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

class Cuenta {
  #saldo = 0; // campo privado real
  depositar(monto) {
    this.#saldo += monto;
  }
  saldo() {
    return this.#saldo;
  }
}

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
const c = new Cuenta();
c.depositar(n);
c.depositar(n);
console.log(`saldo=${c.saldo()}`);
```

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

class Cuenta {
  private saldoInterno = 0;
  depositar(monto: number): void {
    this.saldoInterno += monto;
  }
  saldo(): number {
    return this.saldoInterno;
  }
}

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
const c = new Cuenta();
c.depositar(n);
c.depositar(n);
console.log(`saldo=${c.saldo()}`);
```

### Java · [`java/Main.java`](implementaciones/java/Main.java) · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    static class Cuenta {
        private long saldo = 0;

        void depositar(long monto) {
            saldo += monto;
        }

        long saldo() {
            return saldo;
        }
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        long n = Long.parseLong(br.readLine().trim());
        Cuenta c = new Cuenta();
        c.depositar(n);
        c.depositar(n);
        System.out.println("saldo=" + c.saldo());
    }
}
```

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;

// Las sentencias top-level van antes de la declaración del tipo.
long n = long.Parse(Console.In.ReadToEnd().Trim());
var c = new Cuenta();
c.Depositar(n);
c.Depositar(n);
Console.WriteLine($"saldo={c.Saldo()}");

class Cuenta {
    private long saldo = 0;
    public void Depositar(long monto) => saldo += monto;
    public long Saldo() => saldo;
}
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

// saldo en minúscula: privado del paquete.
type cuenta struct {
	saldo int64
}

func (c *cuenta) depositar(monto int64) {
	c.saldo += monto
}

func (c *cuenta) obtenerSaldo() int64 {
	return c.saldo
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	n, _ := strconv.ParseInt(strings.TrimSpace(line), 10, 64)
	c := &cuenta{}
	c.depositar(n)
	c.depositar(n)
	fmt.Printf("saldo=%d\n", c.obtenerSaldo())
}
```

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

struct Cuenta {
    saldo: i64, // privado fuera del módulo
}

impl Cuenta {
    fn nueva() -> Self {
        Cuenta { saldo: 0 }
    }
    fn depositar(&mut self, monto: i64) {
        self.saldo += monto;
    }
    fn saldo(&self) -> i64 {
        self.saldo
    }
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let mut c = Cuenta::nueva();
    c.depositar(n);
    c.depositar(n);
    println!("saldo={}", c.saldo());
}
```

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

/* C no tiene 'private'; se usa una struct y funciones por convención. */
struct Cuenta {
    long saldo;
};

void depositar(struct Cuenta *c, long monto) {
    c->saldo += monto;
}

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    struct Cuenta c = {0};
    depositar(&c, n);
    depositar(&c, n);
    printf("saldo=%ld\n", c.saldo);
    return 0;
}
```

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL encapsula con vistas/permisos; aquí el cálculo va en la consulta.
WITH montos(n) AS (VALUES (50), (0), (30))
SELECT printf('saldo=%d', n * 2) AS resultado FROM montos;
```

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
class Cuenta {
    private $saldo = 0;

    public function depositar($monto) {
        $this->saldo += $monto;
    }

    public function saldo() {
        return $this->saldo;
    }
}

$n = (int) trim(fgets(STDIN));
$c = new Cuenta();
$c->depositar($n);
$c->depositar($n);
echo "saldo=" . $c->saldo() . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Ejemplo trabajado — del stdin a la salida

Sigamos el primer caso de `casos.json` (`stdin = "50"`, `esperado = "saldo=100"`) por tres lenguajes que dibujan la pared de la privacidad de tres formas distintas.

**Python.** La clase `Cuenta` guarda su estado en `self._saldo`, y el guion bajo inicial es la convención de Python para «esto es privado». Pero es solo eso, una convención: nada en el lenguaje impide que un módulo externo escriba `c._saldo = -999`. La comunidad respeta el guion bajo del mismo modo que se respeta una señal de «no pasar». El recorrido del caso: `n = int(sys.stdin.readline())` lee `"50\n"` y produce `n=50`; `c.depositar(n)` ejecuta `self._saldo += 50` dejando el saldo en `50`; la segunda llamada lo lleva a `100`; `c.saldo()` devuelve ese `100` y `print` emite `saldo=100`. Ramalho, en *Fluent Python*, matiza que el doble guion bajo (`__saldo`) activa además el *name mangling*, que dificulta —no prohíbe— el acceso externo.

**Java.** Aquí la pared es de hormigón: `private long saldo` significa que el compilador rechazará cualquier acceso a `saldo` desde fuera de `Cuenta`. Con `n=50`, la primera `c.depositar(n)` deja `saldo` en `50`, la segunda en `100`, y `c.saldo()` lo devuelve para imprimir `saldo=100`. Si alguien escribiera `c.saldo = -999` en otra clase, el programa **no compilaría**. Esta es la diferencia clave con Python: en Java la invariante no depende de la buena voluntad de los demás programadores, sino de una garantía que la máquina hace cumplir antes de ejecutar. Es exactamente lo que Bloch recomienda al minimizar la accesibilidad.

**Go.** Go no tiene las palabras `public` ni `private`: la visibilidad se decide por la **mayúscula inicial** del identificador. El campo `saldo` empieza en minúscula, así que es privado del paquete; si se llamara `Saldo`, sería exportado. Con `n=50`, `c.depositar(n)` suma `50` dos veces sobre el campo del struct `cuenta`, y `c.obtenerSaldo()` devuelve `100` para que `fmt.Printf("saldo=%d\n", ...)` imprima `saldo=100`. Nótese que la frontera de privacidad en Go es el **paquete**, no el tipo: dentro del mismo paquete, cualquier función alcanza `saldo`; la pared solo se levanta ante código de otros paquetes. Los tres llegan a `saldo=100`, pero custodian la invariante con tres rigores distintos: la palabra dada (Python), el compilador por tipo (Java) y el compilador por paquete y mayúscula (Go).

## 🔬 Comparación

| Lenguaje | Cómo marca lo privado | ¿Lo hace cumplir? |
|---|---|---|
| Python | Convención `_saldo`; `__saldo` activa *name mangling* | No, es acuerdo social |
| JavaScript | Campos con `#saldo` (privados reales de clase) | Sí, error en tiempo de ejecución |
| TypeScript | `private saldoInterno` (chequeo del compilador) | En compilación; en runtime es accesible |
| Java | `private` / `protected` / `public` / *package-private* | Sí, el compilador lo verifica |
| C# | `private` / `protected` / `internal` / `public` | Sí, el compilador lo verifica |
| Go | Mayúscula inicial = exportado; minúscula = privado del paquete | Sí, por paquete |
| Rust | Privado por defecto; `pub` expone; frontera es el módulo | Sí, el compilador lo verifica |
| C | No existe `private`; struct con campos accesibles, convención | No, disciplina del programador |
| SQL | Vistas y permisos (`GRANT`) restringen el acceso a datos | Sí, el motor lo aplica |
| PHP | `private` / `protected` / `public` en la clase | Sí, error en tiempo de ejecución |

La síntesis la ofrece Bloch en *Effective Java*: minimizar la accesibilidad es minimizar el acoplamiento, y con ello maximizar la libertad de cambiar el interior. Los lenguajes se ordenan en un espectro de rigor. En un extremo, Python y C confían en la convención —eficaces mientras el equipo la respete—. En el otro, Java, C#, Rust y Go la hacen cumplir con el compilador, cada uno con su frontera: Java y C# por tipo, Rust por módulo, Go por paquete. En medio, TypeScript ofrece una privacidad que existe para el compilador pero se evapora en el JavaScript emitido, mientras que los `#campos` de JavaScript sí son inviolables en ejecución. Elegir bien lo privado, dice McConnell, es tan importante como elegir bien lo público: la pared no protege a la máquina, protege al humano de sí mismo dentro de seis meses.

## 🧬 El concepto en la familia

En **Ruby** los atributos de instancia son privados por naturaleza —solo el objeto los ve— y se exponen deliberadamente con `attr_reader`, `attr_writer` o métodos escritos a mano; la privacidad es el punto de partida, no una anotación. En **Go**, como vimos, no hay palabras clave: la visibilidad es una propiedad ortográfica del identificador y su alcance es el paquete entero, un diseño deliberadamente minimalista. En **Swift** hay una escala fina de niveles —`private`, `fileprivate`, `internal`, `public`, `open`— que gradúa cuánto sale la visibilidad más allá del propio tipo, el archivo o el módulo. Reconocer dónde pone cada familia la frontera —tipo, archivo, módulo, paquete— permite predecir qué se puede tocar desde dónde sin leer el manual.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 087
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Exponer el estado directamente** → causa: declarar el saldo público «para que sea cómodo», con lo que cualquier módulo puede corromperlo y la invariante deja de existir → solución: hacerlo privado y ofrecer operaciones con significado que la respeten (`depositar`, `retirar`).
- **Getters y setters para todo sin criterio** → causa: generar automáticamente `getSaldo`/`setSaldo` para cada campo, lo que reabre la pared que la privacidad cerraba: un `setSaldo(-999)` es tan dañino como el campo público → solución: exponer operaciones de negocio, no acceso crudo al estado; un setter que rompe la invariante es un error, no encapsulación.
- **Confundir la frontera de privacidad entre lenguajes** → causa: asumir que «privado» siempre significa «solo este tipo», cuando en Go significa «este paquete» y en Rust «este módulo» → solución: recordar en cada lenguaje cuál es la unidad que la pared protege.
- **Creer que la privacidad de TypeScript existe en tiempo de ejecución** → causa: confiar en `private` para proteger datos frente a código JavaScript que consume el módulo compilado → solución: usar campos `#privados` reales cuando la protección deba sobrevivir a la compilación.

## ❓ Preguntas frecuentes

- **¿Python encapsula de verdad?** No lo impone: `_saldo` es una convención y `__saldo` solo dificulta el acceso con *name mangling*. Pero la comunidad respeta la señal con tanta firmeza que, en la práctica, funciona como una pared. Es privacidad por acuerdo, no por candado.
- **¿Encapsular es solo poner getters y setters?** No, y creerlo es el malentendido más extendido. Encapsular es exponer operaciones con significado que mantienen los invariantes; un objeto rodeado de getters y setters que dan acceso crudo a cada campo no está encapsulado, solo disfrazado.
- **¿Por qué Bloch dice que minimice la accesibilidad?** Porque cada miembro público es una promesa que te ata: mientras alguien dependa de él, no lo puedes cambiar. Cuanto menos expongas, menos código ajeno se apoya en tus detalles y más libre eres de reescribir el interior.
- **¿La encapsulación tiene coste en rendimiento?** En los lenguajes compilados, prácticamente ninguno: los accesos a través de métodos suelen quedar en línea (*inlined*). El coste es de escritura —hay que definir los métodos—, y se recupera con creces en mantenimiento.

## 🔗 Referencias

**Libros de la parte:**

- S. McConnell — *Code Complete* (2ª ed., Microsoft Press), cap. 6 «Working Classes» (encapsulación e interfaces de clase).
- J. Bloch — *Effective Java* (3ª ed., Addison-Wesley), ítem «Minimize the accessibility of classes and members».
- D. Parnas — «On the Criteria To Be Used in Decomposing Systems into Modules» (CACM, 1972), origen del ocultamiento de información, citado por McConnell.

**Libros de los lenguajes del núcleo:**

- L. Ramalho — *Fluent Python* (2ª ed., O'Reilly), cap. sobre atributos privados y *name mangling*.
- M. Haverbeke — *Eloquent JavaScript* (3ª ed.), cap. «Objects» — [gratis online](https://eloquentjavascript.net/).
- B. Cherny — *Programming TypeScript* (O'Reilly), cap. sobre clases y modificadores de acceso.
- A. Donovan y B. Kernighan — *The Go Programming Language* (Addison-Wesley), §6 sobre métodos y visibilidad exportada.
- J. Skeet — *C# in Depth* (4ª ed., Manning).
- S. Klabnik y C. Nichols — *The Rust Programming Language*, cap. 7 sobre `pub` y visibilidad — [gratis online](https://doc.rust-lang.org/book/).
- B. Kernighan y D. Ritchie — *The C Programming Language* (2ª ed., Prentice Hall).
- C. J. Date — *SQL and Relational Theory* (3ª ed., O'Reilly).
- J. Lockhart — *Modern PHP* (O'Reilly).

---

> [⏮️ Clase 086](../../parte-5-funciones-y-modularidad/086-modulos-paquetes-y-espacios-de-nombres/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 088 ⏭️](../../parte-5-funciones-y-modularidad/088-importar-exportar-y-organizar-un-proyecto/README.md)
