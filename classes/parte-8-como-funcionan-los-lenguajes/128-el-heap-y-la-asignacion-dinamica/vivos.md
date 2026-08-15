# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 128

> [⬅️ Volver a la clase 128](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Construir una lista de `n` elementos que no existía al compilar. Aquí hay una fecha que ordena la
página: **PL/I tuvo `allocate`, punteros y estructuras basadas en 1964**, ocho años antes que C. Y hay
un contraste que define a dos comunidades enteras: **Fortran prefiere `allocatable` a los punteros
porque no puede tener alias**, y **Ada permite acotar el montón de cada tipo y prohibirlo entero con
una directiva**.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es la **memoria cuyo tamaño y vida se deciden en ejecución**, y estos lenguajes lo
> enseñan porque cubren desde "no la uses" hasta "aquí está toda la maquinaria". **En COBOL y RPG casi
> no se usa**: la memoria se reserva al arrancar y el sistema la administra. **En Ada está acotada y se
> puede prohibir** por norma de certificación. **En Fortran hay dos mecanismos** —`allocatable` y
> `pointer`— y la guía es clara sobre cuál usar.
>
> Y todos comparten el problema del cierre: **el montón es flexible y su coste no es una suma al puntero
> de pila** — hay que buscar hueco, y hay que devolverlo.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: un entero `n` (n >= 1) → stdout: `lista=<n-(n-1)-...-1>`
- **Regla:** `lista dinámica con los valores de n a 1`

| stdin | esperado |
|---|---|
| `3` | `lista=3-2-1` |
| `1` | `lista=1` |
| `5` | `lista=5-4-3-2-1` |

> **Qué está verificado en esta página.** Los lenguajes de la sección 🟢 se **ejecutan en CI**
> contra este mismo `casos.json`, igual que las diez implementaciones del núcleo
> ([workflow Labs](../../../labs/README.md)). Los de la sección 🟡 **no pueden** cumplir este
> contrato sin falsear el lenguaje, y se explica por qué. Los de la sección ⚪ sí podrían, pero
> su cadena de herramientas no está en los *runners*: son correctos, sin sello de máquina.

---

## 🟢 Se ejecutan en CI

### COBOL

[Ficha completa](../../../atlas/cobol.md) · Banca, seguros, gobierno, medios de pago · `cobc -x -free prog.cob`

```cobol
IDENTIFICATION DIVISION.
PROGRAM-ID. MONTON.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  N       PIC 9(4) COMP.
01  I       PIC 9(4) COMP.
01  L       PIC 9(4) COMP.
01  TABLA.
    05  ELEM  PIC 9(9) COMP OCCURS 1 TO 1000 TIMES DEPENDING ON N.
01  SALIDA  PIC X(200) VALUE SPACES.
01  SPOS    PIC 9(4) COMP VALUE 1.
01  ED      PIC Z(8)9.
01  TXT     PIC X(10).

PROCEDURE DIVISION.
    ACCEPT LINEA
    COMPUTE N = FUNCTION NUMVAL(LINEA)

    PERFORM VARYING I FROM 1 BY 1 UNTIL I > N
        COMPUTE ELEM(I) = N - I + 1
    END-PERFORM

    PERFORM VARYING I FROM 1 BY 1 UNTIL I > N
        MOVE ELEM(I) TO ED
        MOVE FUNCTION TRIM(ED) TO TXT
        MOVE 0 TO L
        INSPECT FUNCTION REVERSE(TXT) TALLYING L FOR LEADING SPACE
        COMPUTE L = 10 - L
        IF I > 1
            MOVE "-" TO SALIDA(SPOS:1)
            ADD 1 TO SPOS
        END-IF
        MOVE TXT(1:L) TO SALIDA(SPOS:L)
        ADD L TO SPOS
    END-PERFORM

    COMPUTE L = SPOS - 1
    DISPLAY "lista=" SALIDA(1:L)
    STOP RUN.
```

**Lo que esta clase enseña en COBOL.** El programa usa `OCCURS DEPENDING ON` (clase 090), y conviene
recordar la distinción que aquella clase establecía: **eso NO reserva memoria**. El compilador reserva
el máximo y `N` dice cuánto cuenta.

**El COBOL clásico no usa el montón**, y eso es una decisión de arquitectura con consecuencias muy
concretas:

- **El consumo de memoria de un programa se conoce al compilar.** No hay sorpresas en producción.
- **No hay fragmentación, ni fugas, ni punteros colgantes.**
- **Y no hay que liberar nada**, porque no hay nada reservado.

En un monitor transaccional con miles de tareas concurrentes, esa previsibilidad **es lo que permite
dimensionar la máquina**. Una fuga de memoria en un programa que se ejecuta un millón de veces al día
sería catastrófica.

COBOL-2002 sí añadió la reserva dinámica, con la sintaxis esperable:

```cobol
01  PTR      USAGE POINTER.
01  TAMANO   PIC 9(9) COMP.
01  BUFFER   PIC X(1000) BASED.

ALLOCATE TAMANO CHARACTERS RETURNING PTR
SET ADDRESS OF BUFFER TO PTR
...
FREE PTR
```

**`BASED`** declara un dato sin memoria propia —el mismo concepto que en PL/I y RPG (clase 090)— y
`SET ADDRESS OF ... TO` lo superpone donde apunte el puntero.

Es completo, y es **poco frecuente en producción** por lo dicho arriba.

Y donde COBOL sí trabaja con memoria dinámica es en la frontera con otros lenguajes: **al llamar a C o
a Java**, y **al usar las áreas de trabajo de CICS**:

```cobol
EXEC CICS GETMAIN SET(PTR) LENGTH(1000) END-EXEC
EXEC CICS FREEMAIN DATAPOINTER(PTR) END-EXEC
```

**`GETMAIN` y `FREEMAIN` son el `malloc`/`free` del monitor**, y tienen una propiedad que el `malloc`
de C no tiene: **si la transacción termina o falla, CICS libera automáticamente todo lo que reservó**.

Es liberación por ámbito de transacción, y es la misma idea que los grupos de activación de IBM i
(clase 103) y que los *arena allocators* modernos.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program monton
   implicit none
   integer, allocatable :: v(:)
   integer :: n, i
   character(len=400) :: salida
   character(len=20)  :: buf

   read(*, *) n

   allocate(v(n))                    ! reserva EN EJECUCIÓN
   do i = 1, n
      v(i) = n - i + 1
   end do

   salida = ''
   do i = 1, n
      write(buf, '(I0)') v(i)
      if (i == 1) then
         salida = trim(buf)
      else
         salida = trim(salida) // '-' // trim(buf)
      end if
   end do

   write(*, '(A)') 'lista=' // trim(salida)
   deallocate(v)                      ! (opcional: se libera al salir)
end program monton
```

**Lo que esta clase enseña en Fortran.** El `deallocate` final es **opcional**, y esa es la propiedad
más importante de `allocatable` (clase 090): **se libera solo al salir del ámbito**.

Y merece repetir la comparación, porque es la guía práctica del lenguaje:

| | `allocatable` | `pointer` |
|---|---|---|
| Puede tener alias | **no** | sí |
| Se libera al salir del ámbito | **sí** | no |
| Puede quedar colgado | **no** | sí |
| El compilador puede optimizar | **más** | menos |
| Sirve para listas enlazadas | no | **sí** |

**La regla de Fortran moderno: `allocatable` siempre, `pointer` solo para estructuras enlazadas
(clase 097) o cuando hagan falta alias.**

Y hay un detalle de rendimiento propio del cálculo científico que esta clase debe contar: **la
reasignación automática**.

```fortran
v = [v, nuevo]          ! Fortran 2003: reasigna v con un elemento más
```

Eso es cómodo y **reserva un arreglo nuevo, copia todo y libera el viejo** en cada vuelta — O(n²) en un
bucle. Es exactamente el problema del `SetLength` de Pascal (clase 090), y en Fortran se resuelve
reservando de más:

```fortran
if (n > size(v)) then
   allocate(tmp(2 * size(v)))
   tmp(1:n-1) = v
   call move_alloc(tmp, v)      ! TRANSFIERE sin copiar (clase 081)
end if
```

**`move_alloc` es la operación de movimiento**, y con ella se implementa el crecimiento amortizado de
un `std::vector` a mano.

Y hay una advertencia de la clase 127 que aquí encaja: **los arreglos automáticos van a la PILA, no al
montón**.

```fortran
subroutine f(n)
   real :: temporal(n, n)      ! PILA: puede desbordar
   real, allocatable :: seguro(:,:)
   allocate(seguro(n, n))       ! MONTÓN: falla con stat=, no revienta
end subroutine
```

```fortran
allocate(v(n), stat=ierr)
if (ierr /= 0) then ... end if     ! comprobar el fallo, en vez de abortar
```

**`stat=` convierte el fallo de reserva en un código de error** en lugar de terminar el programa — que
es lo que hace falta en un cálculo de ocho horas.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;
with Ada.Unchecked_Deallocation;

procedure Monton is
   type Vector is array (Positive range <>) of Integer;
   type Ref is access Vector;

   procedure Liberar is new Ada.Unchecked_Deallocation (Vector, Ref);

   N : Integer;
   V : Ref;
begin
   Get (N);

   V := new Vector (1 .. N);        --  reserva en el montón

   for I in 1 .. N loop
      V (I) := N - I + 1;
   end loop;

   Put ("lista=");
   for I in 1 .. N loop
      Put (V (I), Width => 1);
      if I < N then
         Put ("-");
      end if;
   end loop;
   New_Line;

   Liberar (V);                      --  liberación EXPLÍCITA y "no comprobada"
end Monton;
```

**Lo que esta clase enseña en Ada.** Fíjate en el nombre del procedimiento que libera:
**`Ada.Unchecked_Deallocation`**.

Ada **te obliga a instanciar un genérico cuyo nombre dice "no comprobado"** para liberar memoria. No es
una función suelta: es una declaración explícita de que estás haciendo algo que el lenguaje no puede
garantizar.

Esa elección de nomenclatura —igual que `Unchecked_Conversion`— es doctrina: **lo peligroso se puede
hacer y se ve en el código**.

Y Ada da tres niveles de control sobre el montón que ningún otro lenguaje de esta página reúne:

**Primero, acotar el almacenamiento de un tipo de acceso:**

```ada
type Ref is access Vector;
for Ref'Storage_Size use 1_000_000;      --  ESTE tipo dispone de 1 MB
```

Al agotarse, `new` lanza **`Storage_Error`** — una excepción capturable, no un fallo. Y como el límite
es **por tipo**, se puede acotar cada subsistema por separado.

**Segundo, prohibirlo por completo:**

```ada
pragma Restrictions (No_Implicit_Heap_Allocations);
pragma Restrictions (No_Allocators);
```

**El compilador rechaza cualquier `new`.** En aviónica certificada bajo DO-178C eso es habitual: **si
no hay montón, no hay fragmentación, ni fugas, ni tiempos de reserva impredecibles**.

**Y tercero, los *storage pools*, que son lo más avanzado:**

```ada
type Mi_Pool is new System.Storage_Pools.Root_Storage_Pool with ...;
overriding procedure Allocate (Pool : in out Mi_Pool; ...);
for Ref'Storage_Pool use Mi_Pool_Instancia;
```

**Se puede escribir un gestor de memoria propio y decirle a un tipo de acceso que lo use.** Con eso se
implementan *arenas*, reserva de tamaño fijo sin fragmentación, memoria en una zona concreta del
hardware, o un montón con instrumentación para detectar fugas.

Es exactamente lo que en C++ son los asignadores personalizados y en Rust el `GlobalAlloc`, disponible
en Ada desde 1995 y **por tipo, no global**.

Y Ada tiene además la alternativa que evita todo esto: **los tipos con discriminante** (clases 100 y
113) y los arreglos no restringidos permiten que muchas estructuras de tamaño variable vivan en la
pila, sin tocar el montón.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Monton;
{$MODE OBJFPC}{$H+}
uses SysUtils;

type
  PNodo = ^TNodo;
  TNodo = record
    Valor: Integer;
    Siguiente: PNodo;
  end;

var
  N, I: Integer;
  Cabeza, Nuevo, P: PNodo;
  Salida: string;

begin
  Read(N);

  { construir la lista 1..N por delante: queda N..1 }
  Cabeza := nil;
  for I := 1 to N do
  begin
    New(Nuevo);                  { RESERVA en el montón }
    Nuevo^.Valor := I;
    Nuevo^.Siguiente := Cabeza;
    Cabeza := Nuevo;
  end;

  Salida := '';
  P := Cabeza;
  while P <> nil do
  begin
    if Salida <> '' then Salida := Salida + '-';
    Salida := Salida + IntToStr(P^.Valor);
    P := P^.Siguiente;
  end;

  WriteLn('lista=', Salida);

  while Cabeza <> nil do         { LIBERAR: responsabilidad del programador }
  begin
    P := Cabeza;
    Cabeza := Cabeza^.Siguiente;
    Dispose(P);
  end;
end.
```

**Lo que esta clase enseña en Pascal.** `New` y `Dispose` son de 1970, y su diseño tiene una ventaja
sobre `malloc`/`free` que se comentó en la clase 097 y que aquí es el tema: **`New` conoce el tipo**.

```pascal
New(P);                    { reserva SizeOf(TNodo), calculado por el compilador }
```

```c
p = malloc(sizeof(struct Nodo));    /* hay que acertar el tamaño a mano */
```

**Reservar el tamaño equivocado es imposible en Pascal** y es un error clásico en C — sobre todo al
cambiar el tipo de una variable y olvidar el `sizeof`.

Y Pascal tiene una variante de `New` que casi nadie conoce y que es elegante, para los registros
variantes de la clase 100:

```pascal
New(P, Cuadrado);       { reserva SOLO lo que necesita esa variante }
Dispose(P, Cuadrado);    { y libera esa cantidad }
```

**Reserva el tamaño de la variante concreta**, no el del registro completo. Es una optimización que en
otros lenguajes hay que hacer a mano.

Free Pascal y Delphi tienen además tres capas encima que conviene distinguir:

```pascal
GetMem(P, Tam);  FreeMem(P);          { sin tipo: como malloc }
New(P);  Dispose(P);                    { con tipo }
Obj := TClase.Create;  Obj.Free;         { objetos, con constructor }
Intf := TClase.Create;                    { interfaz: conteo de referencias (clase 103) }
```

Y el gestor de memoria de Free Pascal es sustituible:

```pascal
SetMemoryManager(MiGestor);
```

Con eso se pueden instrumentar todas las reservas —y de ahí salen las herramientas de detección de
fugas del ecosistema, como **FastMM** en Delphi, que es célebre por su calidad: **informa de las fugas
al terminar el programa, con la pila de dónde se reservó cada bloque**.

Esa herramienta hizo por la calidad del código Delphi más que cualquier característica del lenguaje, y
es la respuesta práctica al problema del cierre de esta clase: **si el lenguaje no libera solo, que al
menos te diga qué olvidaste**.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let* ((n (read))
       (lista '()))
  (dotimes (i n)
    (push (1+ i) lista))          ; cada push reserva un CONS en el montón
  (format t "lista=~{~D~^-~}~%" lista))
```

**Lo que esta clase enseña en Common Lisp.** Cada `push` **reserva un *cons* en el montón**, y nadie lo
libera: **Lisp tiene recolección de basura desde 1959**, y fue el primer lenguaje en tenerla.

John McCarthy la inventó para Lisp, y el término *garbage collection* es suyo. Es, probablemente, la
aportación más influyente de este lenguaje después de las funciones de primera clase (clase 107).

Y esta clase permite mirar lo que hay debajo, porque en Lisp **la reserva es constante y minúscula**:
un programa Lisp idiomático crea millones de *conses* pequeños y efímeros.

Eso obligó a desarrollar la tecnología que hoy es estándar:

```text
recolección generacional  → la mayoría de los objetos mueren jóvenes
reserva por puntero de bump → reservar es sumar, como en la pila
espacios de supervivientes  → copiar los que sobreviven
recolección incremental      → hacerlo por trozos, sin parar el mundo
```

**La hipótesis generacional** —la mayoría de los objetos mueren jóvenes— se formuló estudiando
programas Lisp y Smalltalk, y es la base de los recolectores de Java, .NET y Go.

Y en SBCL se puede mirar:

```lisp
(room)                       ; uso de memoria por generación y por tipo
(sb-ext:gc :full t)           ; forzar una recolección completa
(sb-ext:get-bytes-consed)      ; cuánta memoria se ha reservado en total
(time (mi-funcion))             ; incluye BYTES CONSED, no solo tiempo
```

**`time` en SBCL informa de cuánta memoria ha reservado la expresión**, no solo del tiempo. Es una
métrica que en la mayoría de los lenguajes hay que buscar con un perfilador, y en Lisp está en la
salida por defecto.

Y para el código donde la reserva importa, Common Lisp permite evitarla:

```lisp
(declare (dynamic-extent lista))     ; "esto no sobrevive": puede ir a la PILA
(make-array 100 :element-type 'double-float)   ; vector especializado, compacto
```

**`dynamic-extent`** es una promesa del programador: **este objeto no escapa de aquí**, así que el
compilador puede ponerlo en la pila en lugar del montón. Es exactamente el análisis de escape que hace
la JVM automáticamente, declarado a mano.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea
set n [string trim $linea]

set lista {}
for {set i 1} {$i <= $n} {incr i} {
    set lista [linsert $lista 0 $i]     ;# insertar por delante
}

puts "lista=[join $lista -]"
```

**Lo que esta clase enseña en Tcl.** Tcl **gestiona la memoria por conteo de referencias sobre valores
inmutables** (clase 102), y el programador nunca reserva ni libera.

Cada valor —un `Tcl_Obj`— lleva un contador; cuando llega a cero, se libera. Y como los valores son
inmutables desde el punto de vista del programa, **compartirlos es seguro**.

Ese modelo tiene dos propiedades que lo distinguen de un recolector de basura:

1. **La liberación es inmediata y determinista**, como en Perl (clase 103): cuando la última referencia
   desaparece, la memoria se devuelve. No hay pausas de recolección.
2. **Los ciclos no se liberan.** Y aquí Tcl tiene una ventaja estructural: **sus valores no pueden
   formar ciclos**, porque son inmutables y una lista no puede contenerse a sí misma.

**El problema del ciclo, que en Perl obliga a `weaken` y en C++ a `weak_ptr`, en Tcl no existe** — a
cambio de no tener estructuras mutables compartidas.

Y hay una consecuencia de rendimiento que esta clase permite explicar mejor que ninguna otra: **la
copia al escribir** (clase 102).

```tcl
set b $a          ;# O(1): incrementa el contador
lset b 0 99        ;# AQUÍ se copia, porque hay dos referencias
```

Y de ahí la regla práctica de Tcl que ya apareció en la 114: **`lappend v ...` con el nombre de la
variable es O(1) amortizado; `set v [concat $v ...]` copia la lista entera**.

Tcl expone además el estado de la memoria si se compila con instrumentación:

```tcl
memory info                    ;# con --enable-symbols=mem
memory active fichero.txt       ;# volcar los bloques VIVOS y dónde se reservaron
memory validate on
```

**`memory active` escribe cada bloque reservado con el fichero y la línea de C que lo pidió** — es una
herramienta de detección de fugas para quien extiende Tcl en C, que es donde las fugas pueden ocurrir.

Es coherente con el cierre de esta clase: **en Tcl puro no hay que preocuparse; en la frontera con C,
sí**.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $n = <STDIN>;
chomp $n;

my @lista;
for my $i (1 .. $n) {
    unshift @lista, $i;            # cada elemento se reserva en el montón
}

print "lista=", join('-', @lista), "\n";
```

**Lo que esta clase enseña en Perl.** Perl usa **conteo de referencias**, con las mismas propiedades que
Tcl: liberación determinista y **el problema de los ciclos** (clases 097 y 103).

Y esta clase permite mirar lo que cuesta la flexibilidad de Perl: **cada valor escalar es una
estructura `SV`** con tipo, banderas, contador de referencias y punteros a sus representaciones (clase
124).

```perl
use Devel::Size qw(size total_size);
print size(42);            # decenas de bytes para un entero
print total_size(\@lista);  # el arreglo COMPLETO, siguiendo referencias
```

**`Devel::Size`** es la herramienta para medirlo, y los números sorprenden: un arreglo de un millón de
enteros ocupa en Perl un orden de magnitud más que en C.

Ese es el precio del tipado dinámico cómodo, y la respuesta del ecosistema es la de la clase 089:
**PDL**, con arreglos compactos y operaciones vectorizadas.

Y Perl tiene herramientas de diagnóstico de memoria que merecen nombrarse porque son de las mejores de
esta página:

```perl
use Devel::Cycle;      find_cycle($estructura);    # ENCONTRAR ciclos de referencias
use Devel::Leak;                                     # contar SVs vivos
use Devel::Peek;       Dump($x);                      # ver la estructura INTERNA de un SV
```

**`Devel::Peek::Dump`** muestra el `SV` por dentro: su tipo, su contador de referencias, qué
representaciones tiene cacheadas. Es la mejor forma de entender el modelo de datos de Perl y por qué
`$x` puede ser a la vez número y cadena (clase 101).

Y **`Devel::Cycle`** ataca directamente el problema del conteo de referencias: **busca ciclos en una
estructura y dice dónde están**, para poder romperlos con `weaken`.

Es la misma clase de herramienta que FastMM en Delphi de esta página: **cuando el lenguaje no puede
garantizar la liberación, la comunidad construye el detector**.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>
#include <memory>
#include <string>

struct Nodo {
    int valor;
    std::unique_ptr<Nodo> siguiente;
    explicit Nodo(int v) : valor(v) {}
};

int main() {
    int n{};
    if (!(std::cin >> n)) return 1;

    std::unique_ptr<Nodo> cabeza;
    for (int i = 1; i <= n; ++i) {
        auto nuevo = std::make_unique<Nodo>(i);
        nuevo->siguiente = std::move(cabeza);      // clase 081
        cabeza = std::move(nuevo);
    }

    std::string salida;
    for (const Nodo* p = cabeza.get(); p != nullptr; p = p->siguiente.get()) {
        if (!salida.empty()) salida += '-';
        salida += std::to_string(p->valor);
    }

    std::cout << "lista=" << salida << '\n';
    return 0;                                       // se libera TODO solo
}
```

**Lo que esta clase enseña en C++.** Este programa reserva `n` nodos en el montón y **no tiene ni un
`delete`**: `unique_ptr` los destruye en cascada al salir (clase 097).

Y esta clase es el sitio para mirar el coste real del montón en C++, que suele subestimarse:

```cpp
auto p = std::make_unique<Nodo>(1);
```

Eso hace: **buscar un bloque libre del tamaño adecuado, marcarlo, devolver el puntero, construir el
objeto**. Y al liberarlo, devolver el bloque y quizá fusionarlo con vecinos.

**Reservar en el montón es entre diez y cien veces más caro que en la pila**, y en un bucle apretado
domina el tiempo.

De ahí que C++ tenga la maquinaria para evitarlo:

```cpp
Nodo n{1};                          // en la PILA: gratis
std::vector<Nodo> v; v.reserve(n);    // UNA reserva para todos (clase 090)
std::pmr::monotonic_buffer_resource pool;   // C++17: ARENA
std::pmr::vector<int> v{&pool};              // reserva del pool, libera de golpe
```

**`std::pmr`** —*polymorphic memory resources*, C++17— es la respuesta estándar: **un asignador que se
pasa como parámetro**, con implementaciones para arena, pila y tamaños fijos.

`monotonic_buffer_resource` no libera nunca elemento a elemento: **reserva de un búfer y lo suelta todo
al destruirse**. Para una fase de trabajo con muchos objetos efímeros, es órdenes de magnitud más
rápido, y es la misma idea que los grupos de activación de IBM i (clase 103) y los *storage pools* de
Ada de esta misma clase.

Y hay dos herramientas imprescindibles que esta clase debe nombrar:

```bash
valgrind --leak-check=full ./prog        # fugas, con la pila de la reserva
g++ -fsanitize=address                    # fugas, uso tras liberar, doble liberación
```

**AddressSanitizer detecta el uso después de liberar y la doble liberación**, que son los dos errores
que el conteo de referencias y el recolector eliminan por construcción. En C++ hay que buscarlos, y
estas herramientas los encuentran.

---

## 🟡 Contrato adaptado, y declarado

Estos lenguajes **no pueden** leer de `stdin` y escribir en `stdout` sin dejar de ser ellos
mismos. No es una limitación del material: es su naturaleza. El cálculo es el mismo y la forma
de entrar y salir es la de su anfitrión. **No pasan por el verificador**, y se dice.

### RPG

[Ficha completa](../../../atlas/rpg.md) · IBM i: ERP, retail, logística, manufactura · `CRTBNDRPG sobre IBM i`

> En IBM i un programa recibe sus datos por **parámetros**, por un **fichero** o por una **pantalla**, nunca por la entrada estándar.

```rpgle
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi MONTON;
  n int(10) const;
end-pi;

dcl-s p      pointer;
dcl-s v      int(10) dim(1000) based(p);   // sin memoria propia
dcl-s i      int(10);
dcl-s salida varchar(200) inz('');

p = %alloc(n * 4);                 // RESERVAR en el monton

for i = 1 to n;
  v(i) = n - i + 1;
endfor;

for i = 1 to n;
  if salida <> '';
    salida += '-';
  endif;
  salida += %char(v(i));
endfor;

dsply ('lista=' + salida);

dealloc p;                          // LIBERAR, explicito

*inlr = *on;
return;
```

**Lo que esta clase enseña en RPG.** RPG tiene reserva dinámica desde ILE, con la sintaxis de la clase
090:

```rpgle
p = %alloc(tamano);        // reservar
p = %realloc(p : nuevo);    // redimensionar
dealloc p;                   // liberar
dealloc(n) p;                 // liberar aunque el puntero sea nulo, sin error
```

Y `based(p)` declara una estructura **sin memoria propia**, superpuesta a donde apunte el puntero. Es
el `BASED` de PL/I y de COBOL.

Fíjate en lo que **no** hay en ese código: **ninguna comprobación de que `i` esté dentro de `n`**. El
`dim(1000)` de la declaración **no reserva nada** —solo dice cómo calcular desplazamientos— así que
**RPG pierde aquí la comprobación de índices que sí tiene con tablas normales** (clase 089).

Es exactamente el mismo agujero que en C, y es la razón de que la guía de la plataforma sea usar
memoria dinámica solo cuando hace falta de verdad.

Y como en COBOL, **la plataforma da algo mejor para el caso normal: la liberación por ámbito**.

```text
RCLACTGRP ACTGRP(MIAPP)     -- libera TODO lo del grupo de activación
```

**Al terminar un grupo de activación, el sistema libera toda su memoria**, cierra sus ficheros y
deshace sus transacciones (clase 103). Un programa puede reservar sin liberar y **el sistema limpia al
final del grupo**.

Eso convierte al grupo de activación en un *arena allocator* a escala de aplicación, y explica por qué
las fugas de memoria son un problema mucho menor en IBM i que en un servidor de aplicaciones
tradicional: **la unidad de trabajo tiene un final, y ese final limpia**.

Y para la memoria compartida entre trabajos, la plataforma ofrece objetos con nombre:

```rpgle
dcl-pr crearEspacio extpgm('QUSCRTUS');    // crear un *USRSPC
```

**Un espacio de usuario (`*USRSPC`) es un objeto del sistema de hasta 16 MB**, persistente, con nombre y
accesible desde cualquier trabajo. Es memoria compartida gestionada por el sistema operativo, no por
el programa.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 monton: procedure options(main);

    declare n fixed binary(31);
    declare i fixed binary(31);
    declare p pointer;
    declare 1 nodo based(p),
              2 valor fixed binary(31),
              2 siguiente pointer;
    declare (cabeza, actual, nuevo) pointer;
    declare salida char(200) varying initial('');

    get list (n);

    cabeza = null();
    do i = 1 to n;
       allocate nodo set(nuevo);       /* RESERVAR: PL/I, 1964 */
       nuevo -> valor = i;
       nuevo -> siguiente = cabeza;
       cabeza = nuevo;
    end;

    actual = cabeza;
    do while (actual ^= null());
       if salida ^= '' then salida = salida || '-';
       salida = salida || trim(char(actual -> valor));
       actual = actual -> siguiente;
    end;

    put skip list ('lista=' || salida);

 end monton;
```

**Lo que esta clase enseña en PL/I.** Aquí está el dato que abre esta clase: **`allocate`, `pointer` y
`based` son de PL/I y de 1964**, ocho años antes que `malloc` en C y seis antes que `New` en Pascal.

```pli
 declare 1 nodo based(p), 2 valor fixed binary(31), 2 siguiente pointer;
 allocate nodo set(nuevo);
 nuevo -> valor = 1;
 free nuevo -> nodo;
```

**La flecha `->` de C viene de aquí** (clase 097), y `based` es el antepasado del `BASED` de COBOL y de
RPG.

Y PL/I tiene una capacidad que ningún otro lenguaje de esta página ofrece: **las áreas**.

```pli
 declare mi_area area(100000);
 declare p pointer;

 allocate nodo in(mi_area) set(p);        /* reservar DENTRO del área */
 ...
 write file(salida) from(mi_area);         /* ESCRIBIR EL ÁREA ENTERA a disco */
 read file(entrada) into(mi_area);          /* y leerla de vuelta */
```

**Un `area` es un bloque de memoria dentro del cual se reserva**, con su propio gestor. Y lo
extraordinario es la penúltima línea: **un área con estructuras enlazadas dentro se puede escribir en
un fichero y leer después, y los punteros siguen siendo válidos** — porque son desplazamientos
relativos al área, no direcciones absolutas.

**Eso es serializar un grafo de objetos sin serializador**, en 1964. Es exactamente el problema de la
clase 106, resuelto haciendo que los punteros sean relativos.

Y es la misma idea que hay detrás de los ficheros mapeados en memoria con estructuras internas, de las
regiones de Rust y de los formatos de datos binarios modernos como FlatBuffers o Cap'n Proto —donde el
dato en disco **es** la estructura en memoria, sin conversión.

Y las áreas dan además liberación por ámbito: **liberar el área libera todo lo que hay dentro**, que es
un *arena allocator* con nombre propio.

Es una de las mejores ideas de PL/I y una de las menos conocidas.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
MONTON ; El monton y la asignacion dinamica -- clase 128
 read n
 kill lista
 ; en M no se reserva memoria: se asigna y ya existe
 for i=1:1:n set lista(i) = n - i + 1
 set salida = ""
 for i=1:1:n do
 . if salida '= "" set salida = salida _ "-"
 . set salida = salida _ lista(i)
 write "lista=", salida, !
 quit
```

**Lo que esta clase enseña en M.** **En M no existe la reserva de memoria**: no hay `allocate`, no hay
`new` en el sentido del montón y no hay punteros (clase 089).

```mumps
 set lista(1000000) = "x"        ; existe; no se ha reservado nada explícitamente
 kill lista                        ; y desaparece
```

El intérprete gestiona el árbol disperso por debajo, y el programador **solo asigna y borra**. Es el
modelo más simple de esta página, y tiene tres consecuencias:

1. **No hay fugas de memoria posibles en código M puro**: `kill` borra, y al terminar el proceso se
   libera todo.
2. **No hay punteros colgantes**, porque no hay punteros.
3. **Y no hay control**: no se puede decir dónde vive un dato ni cuánto ocupa.

Y hay una propiedad que hace de M un caso especial en esta clase, y es la más importante: **la
distinción entre memoria y disco casi desaparece**.

```mumps
 set v(i) = x        ; en memoria del proceso
 set ^v(i) = x        ; en DISCO, con la misma sintaxis
```

Para el programador, **la única diferencia es un carácter**. Por debajo, el *global* se escribe en
bloques de base de datos, se cachea en memoria compartida entre procesos y se sincroniza con
transacciones (clase 121).

Eso significa que **el "montón" de M es la base de datos**, y sus propiedades son las de una base de
datos: persistente, compartida, transaccional y **más grande que la memoria física**.

Un programa M puede construir una estructura de cien gigabytes sin pensar en la memoria, porque el
sistema la pagina desde disco.

Es la conclusión que esta parte del curso ha repetido con M: **su modelo de datos absorbe problemas que
en otros lenguajes son del lenguaje**. Aquí, el problema absorbido es la gestión de memoria.

Y el precio también es el de siempre: **sin control sobre la disposición, M no puede competir en cálculo
numérico denso** — y para eso están los enlaces con C, Python y Go de YottaDB.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| n lista |

n := stdin nextLine trimBoth asNumber.

lista := OrderedCollection new.
1 to: n do: [ :i | lista addFirst: i ].     "cada objeto va al montón"

Transcript
    show: 'lista=', ((lista collect: [ :cada | cada printString ])
        inject: '' into: [ :acc :cada |
            acc isEmpty ifTrue: [ cada ] ifFalse: [ acc, '-', cada ] ]);
    cr.
```

**Lo que esta clase enseña en Smalltalk.** **En Smalltalk todo está en el montón**: no hay tipos valor,
no hay pila para los datos y **todo objeto se reserva y lo recoge el recolector**.

`3 + 4` crea... bueno, no: los enteros pequeños son la excepción. **`SmallInteger` se representa
etiquetando el puntero** —usando un bit para distinguir un puntero de un entero inmediato— así que no
se reserva nada.

Esa técnica, **los punteros etiquetados**, es de Smalltalk y de Lisp, y hoy la usan V8, la JVM con
compresión de punteros y casi todos los tiempos de ejecución dinámicos.

Y el resto de la clase es sobre el recolector, que en Smalltalk es de los mejor documentados de la
historia: **la investigación sobre recolección generacional se hizo en Smalltalk y en Lisp**, y de ahí
salieron los recolectores de Java y .NET.

En Pharo se puede consultar todo:

```smalltalk
Smalltalk garbageCollect.
Smalltalk vmParameterAt: 7.                "tamaño del espacio de supervivientes"
Smalltalk garbageCollectMost.               "solo la generación joven: SCAVENGE"
SystemNavigation default allObjects size.    "cuántos objetos hay en la imagen"
```

**`allObjects` recorre la imagen entera y devuelve todos los objetos vivos.** Que eso sea una operación
disponible dice mucho del sistema: **el montón es inspeccionable desde el propio lenguaje**.

Y de ahí salen herramientas que en otros entornos exigen un perfilador externo:

```smalltalk
Persona allInstances size.              "cuántas instancias de esta clase hay"
Persona allInstances first inspect.       "abrir una en el inspector"
objeto chasePointers.                      "QUIÉN apunta a este objeto"
```

**`chasePointers` responde a la pregunta clave de una fuga de memoria: ¿quién sigue reteniendo esto?**
En Java eso exige un volcado del montón y una herramienta de análisis; aquí es un mensaje.

Y hay una consecuencia del modelo de imagen (clase 041) que esta clase debe cerrar: **como la imagen
persiste, una fuga de memoria en Smalltalk también persiste**. Un objeto olvidado sigue ahí mañana, y
la imagen crece sesión a sesión.

Es un problema real del ecosistema, y la razón de que `allObjects` y `chasePointers` existan y se usen.

---

## Y de vuelta a la clase

Lo transferible: **pila y montón no compiten, se reparten según cuánto vive el dato**. Lo que muere con
la función va a la pila y es gratis; lo que sobrevive a quien lo creó, o cuyo tamaño no se sabe, va al
montón y cuesta. El error caro no es elegir mal una vez, es **no saber cuál estás usando**: un arreglo
local enorme desborda la pila (clase 127) y un millón de objetos pequeños fragmentan el montón. La
pregunta que lo decide siempre es la misma: **¿cuánto tiene que vivir esto y quién lo va a soltar?**

⏮️ [Volver a la clase 128](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
