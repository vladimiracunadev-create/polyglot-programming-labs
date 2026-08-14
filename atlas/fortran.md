# 🔬 Fortran — 1957

> [⬅️ Atlas](README.md) · [🧟 Lenguajes que siguen vivos](vivos.md) · [📚 Índice de clases](../classes/README.md)

**El lenguaje con el que se predice el clima.** El primer lenguaje de alto nivel de la historia sigue
siendo, casi setenta años después, el que ejecutan los supercomputadores más grandes del mundo. No
por inercia: por velocidad.

> **🎯 Por qué está en este programa**
>
> **Criterio de inclusión: Fortran se ejecuta hoy, y además sigue evolucionando** — el estándar
> vigente es de 2023, hay cuatro compiladores en desarrollo activo y un gestor de paquetes nuevo.
> No es un lenguaje que sobreviva: es uno que compite.
>
> Entra porque **deja a la vista un concepto que el núcleo esconde**: el **array como ciudadano de
> primera** y el coste real del **solapamiento de memoria (*aliasing*)**. Cuando en Python escribes
> `c = a + b` sobre arrays de NumPy y va rápido, es porque debajo hay código compilado con las
> garantías que Fortran da por defecto. Ver la versión de Fortran explica **por qué** NumPy existe
> y por qué C tuvo que inventar `restrict` para acercarse.

| | |
|---|---|
| **Año** | 1957 (primer compilador, IBM 704) |
| **Autoría** | **John Backus** y su equipo en IBM |
| **Familia** | Científica / cálculo numérico y de arrays |
| **Paradigma** | Imperativo y procedimental; modular desde F90, OO desde F2003 |
| **Tipado** | Estático y fuerte, con `implicit none` obligatorio en la práctica moderna |
| **Memoria** | Estática y de pila por defecto; `allocatable` gestionado por el compilador |
| **Ejecución** | Compilado a nativo, con optimización agresiva |
| **Estado** | 🟢 **Vivo y en evolución** — estándar 2023; no es solo legacy |

---

## 📜 Historia

En 1954 John Backus propuso a IBM algo que sonaba a herejía: un lenguaje en el que el programador
escribiera fórmulas matemáticas y **un traductor generara código máquina tan bueno como el escrito a
mano**. Era la parte difícil. Nadie dudaba de que se pudiera traducir; se dudaba de que el resultado
fuera aceptablemente rápido, porque en 1954 la programación era ensamblador y el ensamblador era
sagrado.

El equipo tardó tres años. **FORTRAN** (*FORmula TRANslating System*) se entregó en 1957 para el IBM
704 y, con él, el primer **compilador optimizador** de la historia: análisis de expresiones, asignación
de registros, optimización de bucles. Ese trabajo, más que el lenguaje, es la contribución que fundó
la disciplina de construcción de compiladores.

La evolución posterior marca dos épocas claramente distintas:

- **FORTRAN 66 y 77** — la era de las **columnas**. Herencia de la tarjeta perforada: columnas 1–5
  para etiquetas, columna 6 para continuación, 7–72 para la sentencia. Variables de seis caracteres,
  `GO TO` por todas partes, tipado implícito por la inicial del nombre (`I` a `N` eran enteros: de ahí
  el chiste de que "GOD is REAL, unless declared INTEGER"). Este es el Fortran de la mala fama.
- **Fortran 90 en adelante** — el rediseño. Formato libre, **módulos** con interfaces explícitas,
  **operaciones sobre arrays completos** (`c = a + b` suma dos matrices sin escribir un bucle),
  asignación dinámica, punteros, `implicit none` para desactivar el tipado implícito. **2003** trajo
  orientación a objetos e interoperabilidad estandarizada con C; **2008**, los *coarrays* para
  paralelismo en el propio lenguaje; **2018** y **2023** siguen añadiendo.

Nota tipográfica útil para leer literatura antigua: hasta el 77 se escribía **FORTRAN** en mayúsculas;
desde el 90, **Fortran**. La grafía te dice de qué época habla un texto.

## 🏭 Dónde sobrevive hoy

- **Modelos climáticos y meteorológicos**: WRF, CESM y los modelos operativos de los servicios
  meteorológicos nacionales.
- **Dinámica de fluidos computacional (CFD)**: aerodinámica, combustión, turbomaquinaria.
- **Física computacional**: estructura electrónica, física de plasmas, astrofísica, redes cristalinas.
- **Ingeniería estructural**: análisis por elementos finitos.
- **Álgebra lineal de alto rendimiento**: **BLAS** y **LAPACK**, las bibliotecas sobre las que se
  apoyan NumPy, SciPy, MATLAB, R y buena parte del aprendizaje automático, tienen su implementación
  de referencia en Fortran. Cuando haces una multiplicación de matrices en Python, hay Fortran
  compilado debajo.

## 🧠 Por qué no ha muerto

**1. El compilador puede asumir que no hay solapamiento (*aliasing*).** Es la razón técnica de fondo.
En C, si una función recibe dos punteros, el compilador debe asumir que podrían apuntar a la misma
memoria, y eso le impide reordenar y vectorizar libremente. El estándar de Fortran **prohíbe** que
dos argumentos de un procedimiento se solapen, así que el compilador optimiza sin esa duda. C tuvo
que inventar la palabra clave `restrict` en C99 para recuperar, a mano y bajo responsabilidad del
programador, lo que Fortran tiene por defecto.

**2. Los arrays son ciudadanos de primera.** Un array de Fortran conoce su forma, sus límites (que no
tienen por qué empezar en 0) y puede rebanarse (`a(2:5, :)`) o operarse entero. Existen `matmul`,
`dot_product`, `sum`, `maxval` y las operaciones elementales en el propio lenguaje, no en una
biblioteca. Además, el almacenamiento es **por columnas** (*column-major*), al revés que C — un
detalle que hay que tener presente al interoperar.

**3. Medio siglo de bibliotecas numéricas validadas.** La estabilidad numérica de un solver no se
comprueba leyéndolo: se comprueba con décadas de uso en problemas reales. Reescribir LAPACK no es
un ejercicio de traducción.

**4. El paralelismo está en el ecosistema.** OpenMP, MPI y los *coarrays* del estándar cubren desde
el multinúcleo hasta el clúster, y los compiladores de NVIDIA y AMD ofrecen descarga a GPU desde
directivas. La comunidad HPC no se ha movido porque no ha tenido un motivo de rendimiento para
hacerlo.

## 🔄 Lo que se ha modernizado

Fortran es, de toda esta lista, el caso más claro de lenguaje que **no sobrevive sino que compite**:

- **`do concurrent`** (2008, ampliado en 2018): un bucle en el que el programador **garantiza** que
  las iteraciones son independientes. Los compiladores de NVIDIA e Intel lo usan para **descargarlo
  automáticamente a la GPU** sin una sola directiva ni línea de CUDA. Es paralelismo expresado en el
  propio lenguaje.
- **Coarrays** (2008): paralelismo distribuido en la sintaxis. `a[3]` significa "la copia de `a` en la
  imagen 3", con memoria distribuida gestionada por el compilador en lugar de por llamadas a MPI.
- **Interoperabilidad estandarizada con C** (`iso_c_binding`, 2003), que es lo que permite que NumPy,
  SciPy y R llamen a rutinas Fortran de forma portable y bien definida.
- **Submódulos** (2008): separar la interfaz de la implementación para no recompilar el mundo entero
  al tocar una función. Un problema de ingeniería moderno, resuelto en el estándar.
- **`fpm`**, el gestor de paquetes y sistema de construcción, que por fin da a Fortran un flujo
  equivalente a `cargo` o `npm`.
- **Compiladores nuevos**: **LLVM Flang** entró en el proyecto LLVM, y **`nvfortran`** y el
  **`flang`** de AMD dan acceso directo a GPU. Nadie invierte en escribir compiladores nuevos para un
  lenguaje muerto.
- **Estándar 2023** vigente, con más de sesenta años de compatibilidad hacia atrás: código de 1977
  sigue compilando junto a código con GPU.

## ⚙️ Cómo se ejecuta hoy

```bash
# GNU Fortran, parte de GCC
sudo apt-get install -y gfortran

gfortran -O2 total.f90 -o total
echo "15000 2 0.10" | ./total
# Total: 27000.00
```

**Compiladores en uso.** `gfortran` (GCC, libre y el más extendido), **Intel `ifx`** (oneAPI, el
referente en x86 para HPC), **LLVM Flang**, **NVIDIA `nvfortran`** (con descarga a GPU) y **AMD
`flang`**. Las extensiones importan: `.f` o `.for` implica **formato fijo** de columnas; `.f90` y
posteriores implican **formato libre**. Confundirlas produce errores de sintaxis desconcertantes.

**Gestión de paquetes.** Históricamente no había ninguna: se copiaban los fuentes. Hoy existe
[**fpm**](https://fpm.fortran-lang.org/) (*Fortran Package Manager*), que da a Fortran algo parecido
a `cargo` o `npm`.

## 🧪 El programa de la clase 041 en Fortran

```fortran
program total_venta
   implicit none
   real(kind=8) :: precio, cantidad, descuento, total
   character(len=32) :: buffer

   read(*, *) precio, cantidad, descuento
   total = precio * cantidad * (1.0d0 - descuento)

   write(buffer, '(F20.2)') total
   write(*, '(A)') 'Total: ' // trim(adjustl(buffer))
end program total_venta
```

**Recorrido, línea a línea.**

- `implicit none` es la primera línea de cualquier Fortran moderno serio. Sin ella, una variable no
  declarada **no es un error**: el compilador le asigna un tipo según su inicial, herencia directa de
  1957. Un `total` mal tecleado como `totl` se convertiría en un real nuevo con valor basura, en
  silencio. `implicit none` apaga esa herencia y convierte el descuido en error de compilación.
- `real(kind=8)` pide un real de 8 bytes (doble precisión). El `kind` es un número entero que
  identifica la representación; escribir `kind=8` funciona en los compiladores habituales, pero la
  forma **portable** es `use iso_fortran_env, only: real64` y declarar `real(real64)`. Es la clase de
  detalle que separa el código que compila aquí del que compila en cualquier sitio.
- `read(*, *)` es lectura **dirigida por lista**: el primer `*` es la unidad (entrada estándar), el
  segundo el formato (libre). Lee tantos valores como variables haya, separados por espacios o comas,
  atravesando saltos de línea si hace falta. Es notablemente cómodo comparado con el `scanf` de C.
- `1.0d0` es un literal de **doble precisión**. Escribir `1.0` a secas sería precisión simple, y en
  una expresión con dobles introduciría una conversión innecesaria. La `d` es la marca; en código
  moderno se prefiere `1.0_real64`.
- `//` es el operador de **concatenación de cadenas**, no un comentario ni una división. Los
  comentarios en Fortran libre empiezan por `!`.
- El truco del `buffer`: se escribe el número **a una cadena** con formato `F20.2` (ancho 20, dos
  decimales), y luego `adjustl` lo empuja a la izquierda y `trim` corta los espacios sobrantes. Se
  podría escribir `F0.2` para pedir "el ancho mínimo", pero su comportamiento con el cero varía entre
  compiladores; el rodeo por el buffer es el que da la misma salida en todos.
- Las cadenas de Fortran tienen **longitud fija**: `character(len=32)` reserva 32 caracteres y los
  rellena con espacios. No hay cadena dinámica sin `allocatable`. De ahí que `trim` aparezca tanto.

## 🔍 Qué reconocer si vienes de otro lenguaje

| Si conoces… | En Fortran es… |
|---|---|
| `import` / `#include` | `use modulo` — con interfaz comprobada por el compilador |
| `def f(x)` con retorno | `function f(x) result(y)` |
| `void f(x)` | `subroutine f(x)` |
| `a[0]` | `a(1)` — paréntesis, y el índice **empieza en 1** por defecto |
| `for i in range(n)` | `do i = 1, n ... end do` |
| `c = a + b` sobre listas | `c = a + b` sobre arrays completos — nativo, sin bucle |
| `numpy.dot(a, b)` | `matmul(a, b)` |
| `restrict` de C | El comportamiento por defecto |
| `f"{x:.2f}"` | `write(buf, '(F20.2)') x` |

## ⚠️ Errores comunes al leerlo

- **Índices desde 1.** Y no siempre: `real :: a(0:9)` o `a(-5:5)` son legales. El array lleva sus
  límites consigo, así que no puedes asumirlos.
- **Column-major.** `a(i, j)` guarda contiguos los que varían en `i`. Recorrer una matriz con el
  bucle exterior en `i` destruye la localidad de caché. En C es exactamente al revés, y ese es el
  error clásico al portar código entre ambos.
- **Confundir formato fijo y libre.** Si un `.f` moderno "no compila por sintaxis", casi siempre es
  que el compilador lo está leyendo como formato fijo y descartando todo más allá de la columna 72.
- **`implicit none` ausente en código antiguo.** Al leerlo, no des por hecho que una variable está
  declarada: puede existir solo por su inicial.
- **Paso por referencia por defecto.** Un argumento modificado dentro de una subrutina cambia fuera.
  El Fortran moderno lo documenta con `intent(in)`, `intent(out)` o `intent(inout)`, y usarlos es
  obligatorio en cualquier código mantenible.

## 📚 Fuentes y bibliografía

- [fortran-lang.org](https://fortran-lang.org/) — el portal actual de la comunidad, con tutoriales,
  el gestor de paquetes `fpm` y el índice de bibliotecas.
- [Documentación de GNU Fortran](https://gcc.gnu.org/onlinedocs/gfortran/) — referencia del
  compilador libre.
- [Intel Fortran Compiler](https://www.intel.com/content/www/us/en/developer/tools/oneapi/fortran-compiler.html)
  — el compilador de referencia en HPC sobre x86.
- **Michael Metcalf, John Reid, Malcolm Cohen**, *Modern Fortran Explained*, Oxford University Press
  — la obra de referencia; Reid y Cohen han estado en el comité del estándar, así que explica el
  porqué de cada decisión.
- **Milan Curcic**, *Modern Fortran*, Manning, 2020 — enfoque práctico y actual, orientado a quien
  llega desde Python o C.
- **Ronald Hanson, Tim Hopkins**, *Numerical Computing with Modern Fortran*, SIAM — el puente entre el
  lenguaje y el cálculo numérico serio.

---

⏮️ [Volver al Atlas](README.md) · 🧟 [Los lenguajes que siguen vivos](vivos.md) ·
🔗 Relacionadas: [Ada](ada.md) · [C](c.md) · [Assembler](assembler.md)
