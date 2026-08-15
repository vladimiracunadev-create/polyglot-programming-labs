# 🐹 Go — 2009

> [⬅️ Atlas](README.md) · [🗂️ Todas las fichas](lenguajes.md) · [📚 Índice de clases](../classes/README.md)

Go se diseñó a partir de una queja concreta: **los programas grandes tardaban demasiado en compilar y
demasiado en entenderse**. Su respuesta fue radical y poco habitual — **quitar características** — y el
resultado es un lenguaje que se aprende en un fin de semana y que mueve buena parte de la
infraestructura de Internet.

> **🎯 Por qué está en este programa**
>
> **Go es uno de los diez lenguajes del núcleo** y, junto a [Rust](rust.md), el **representante de la
> familia de sistemas** ([Atlas](README.md#sistemas)).
>
> Aporta al programa el modelo de concurrencia que ningún otro del núcleo enseña: **CSP con
> gorrutinas y canales**
> ([clases 133 y 134](../classes/parte-8-como-funcionan-los-lenguajes/README.md)), la idea de Hoare de
> 1978 llevada a un lenguaje mayoritario. Y aporta una lección de diseño que el curso repite desde
> varios ángulos (clases 155 y 164): **un lenguaje pequeño es una decisión, y lo que prohíbe es lo que
> permite prometer**.

| | |
|---|---|
| **Año** | 2009; **1.0** en 2012, con **promesa de compatibilidad**; **1.18** con genéricos (2022) |
| **Autoría** | **Robert Griesemer, Rob Pike, Ken Thompson**, Google |
| **Familia** | Sistemas; herencia de C, Pascal/Oberon ([Wirth](pascal.md)) y de **CSP** (Hoare) |
| **Paradigma** | Imperativo y concurrente; composición en vez de herencia |
| **Tipado** | **Estático y fuerte**, con **interfaces estructurales** e inferencia local |
| **Memoria** | Recolección de basura de **latencia muy baja**, concurrente |
| **Ejecución** | Compilado a nativo, **estático por defecto**, con compilación rapidísima |
| **Estado** | 🟢 **Estándar de facto** en infraestructura, nube y herramientas de línea de comandos |

---

## 📜 Historia

La historia de Go empieza, según cuenta Rob Pike, **esperando a que compilara un binario de C++ en
Google**. Tardaba tanto que en esa espera empezó la conversación que llevó al lenguaje.

**Ken Thompson** —coautor de Unix y de [C](c.md)—, **Rob Pike** —de Plan 9 y de UTF-8— y **Robert
Griesemer** —de la máquina virtual de JavaScript V8 y discípulo de [Wirth](pascal.md)— diseñaron en
**2007** un lenguaje con tres objetivos explícitos:

1. **Compilar rapidísimo**, incluso proyectos enormes.
2. **Ser fácil de leer** por alguien que no lo escribió, en una empresa con miles de programadores.
3. **Hacer la concurrencia natural**, porque los servidores ya eran multinúcleo.

Y para conseguirlo **quitaron cosas**: sin herencia de clases, sin excepciones, sin genéricos —durante
trece años—, sin sobrecarga de operadores ni de funciones, sin macros, sin constructores, sin
aritmética de punteros.

**Go 1.0 (2012)** vino con una promesa que ha cumplido: **compatibilidad hacia atrás**. Código de 2012
compila hoy. Es la misma disciplina de [Tcl](tcl.md) y del mainframe (clase 154), y es una de las
razones de su adopción industrial.

**Go 1.18 (2022)** añadió **genéricos** tras una discusión pública de una década — y el resultado es
deliberadamente limitado, coherente con la filosofía.

## 🏭 Dónde vive hoy

- **Infraestructura de la nube**: **Docker, Kubernetes, Terraform, Prometheus, etcd, containerd**.
  Prácticamente toda la capa de orquestación moderna está escrita en Go (clase 174).
- **Servicios de red y API**: por el modelo de concurrencia y por el despliegue simple.
- **Herramientas de línea de comandos**: el binario estático sin dependencias es ideal (clase 167).
- **Bases de datos y almacenamiento**: CockroachDB, InfluxDB, Minio.
- **Y como sustituto de Python en tareas de administración** donde el rendimiento o el despliegue
  importan.

## 🧠 Lo que enseña: CSP, y por qué es distinto de los hilos

Go implementa **CSP —*Communicating Sequential Processes*, de Tony Hoare, 1978**— con dos primitivas:

```go
go trabajar(datos)              // una GORRUTINA: unos pocos KB, no un hilo del sistema
canal <- valor                   // enviar
valor := <-canal                  // recibir, bloqueando hasta que haya algo
```

**Y el lema del lenguaje resume la idea**:

> **"No te comuniques compartiendo memoria; comparte memoria comunicándote."**

Es lo contrario del modelo de hilos con cerrojos de [Java](java.md) y [C++](cpp.md) (clase 135): en
lugar de proteger un dato compartido, **el dato se pasa por un canal** y solo una gorrutina lo tiene a
la vez.

**Y las gorrutinas son ligeras de verdad**: arrancan con unos pocos kilobytes de pila que crece sola,
y el planificador de Go multiplexa **cientos de miles** sobre unos pocos hilos del sistema.

> **Y la honestidad exige decir el límite** (clase 136): **Go no impide las carreras de datos**. Los
> canales son la forma recomendada, no la obligatoria, y compartir un mapa entre gorrutinas sin
> sincronizar es un error que compila. Por eso existe `go test -race`, el detector de carreras, y por
> eso conviene usarlo siempre. [Rust](rust.md) resolvió el mismo problema por el otro camino: **hacerlo
> imposible en el sistema de tipos**.

Y el segundo concepto que Go enseña es **la interfaz estructural**:

```go
type Escritor interface { Write(p []byte) (int, error) }
```

**Cualquier tipo con ese método la cumple, sin declararlo** — como [TypeScript](typescript.md) y a
diferencia de [Java](java.md) (clase 112). Eso permite definir la interfaz **donde se consume**, no
donde se implementa, que es la inversión de dependencias hecha idioma.

## 🔄 Lo que se ha modernizado

- **Genéricos (1.18)** con restricciones por conjuntos de tipos — limitados a propósito.
- **Errores envueltos** con `%w`, `errors.Is` y `errors.As`: Go **no tiene excepciones** y devuelve
  errores como valores (clase 116), y esta capa da la información que faltaba.
- **Espacios de trabajo y módulos** con `go.sum`: fichero de bloqueo con sumas de comprobación
  (clase 143) y **suma de comprobación verificable en un registro público**, que es una defensa real
  de cadena de suministro (clase 153).
- **Optimización guiada por perfiles (PGO)** desde 1.21: compilar usando datos de ejecución real.
- **`log/slog`**: registro estructurado en la biblioteca estándar (clase 142).
- **Y una discusión abierta y sana** sobre `for` con variables por iteración, corregida en 1.22 tras
  años de ser la fuente número uno de errores del lenguaje.

## ⚙️ Cómo se ejecuta hoy

```bash
go run main.go < entrada.txt        # el comando de la clase 041
go build -o venta .                  # binario estático, sin dependencias

go vet ./... && gofmt -l .           # calidad: gofmt NO tiene opciones (clase 146)
go test -race ./...                   # pruebas con detector de carreras (clase 136)
```

> **`gofmt` merece la mención**: **no tiene opciones de configuración**. La comunidad renunció a la
> discusión de estilo eliminando la posibilidad de tenerla, y es probablemente la decisión de la
> clase 146 mejor ejecutada de cualquier ecosistema.

## 🧪 El programa de la clase 041 en Go

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
	reader := bufio.NewReader(os.Stdin)
	linea, _ := reader.ReadString('\n')
	campos := strings.Fields(linea)

	// Go: tipado estático explícito; conversión float64(cantidad) obligatoria.
	precioUnitario, _ := strconv.ParseFloat(campos[0], 64)
	cantidad, _ := strconv.Atoi(campos[1])
	descuento, _ := strconv.ParseFloat(campos[2], 64)

	subtotal := precioUnitario * float64(cantidad)
	total := subtotal * (1 - descuento)

	fmt.Printf("Total: %.2f\n", total)
}
```

**Lo que hay que ver.**

- **`float64(cantidad)` es obligatorio.** Go **no convierte números implícitamente**, ni siquiera de
  `int` a `float64`. Es más verboso y elimina una familia entera de sorpresas (clase 100) —lo
  contrario de [JavaScript](javascript.md) y [PHP](php.md)—.
- **El `_` que descarta el error aparece cuatro veces, y en código real no debería.** Go devuelve
  errores como valores y **obliga a mirarlos**; ignorarlos con `_` es una decisión explícita y visible,
  que es justamente la virtud del modelo (clase 116).
- **`strings.Fields`** parte por cualquier espacio en blanco, como `split ' '` de [Perl](perl.md).
- **No hay `try` ni `catch`**: si algo falla, se ve en la línea donde falla. Es la decisión más
  discutida del lenguaje y la más coherente con su filosofía de que **el flujo de control se lee**.

## 📚 Fuentes y bibliografía

- [go.dev](https://go.dev/doc/) — *A Tour of Go*, *Effective Go* y la referencia; de lo mejor
  documentado de esta lista.
- [El blog de Go](https://go.dev/blog/) — los artículos sobre concurrencia, errores y genéricos
  explican el porqué de cada decisión.
- **Alan Donovan, Brian Kernighan**, *The Go Programming Language*, Addison-Wesley — el "K&R de Go",
  escrito por uno de los autores del original.
- **Jon Bodner**, *Learning Go*, 2.ª ed., O'Reilly — actualizado a genéricos; enseña los idiomas del
  lenguaje, no solo la sintaxis.
- **Katherine Cox-Buday**, *Concurrency in Go*, O'Reilly — los patrones de canales y gorrutinas.

---

⏮️ [Volver al Atlas](README.md) · 🗂️ [Todas las fichas](lenguajes.md) ·
🔗 Relacionadas: [Rust](rust.md) · [C](c.md) · [Zig](zig.md) · [Erlang](erlang.md) ·
[Pascal](pascal.md)
