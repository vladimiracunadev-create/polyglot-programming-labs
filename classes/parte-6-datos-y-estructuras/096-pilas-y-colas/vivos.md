# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 096

> [⬅️ Volver a la clase 096](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Los mismos datos, salidos por los dos extremos. LIFO y FIFO son las dos disciplinas de acceso más
antiguas de la informática, y ninguno de estos doce lenguajes tiene una sintaxis dedicada para ellas
— porque no hace falta: **se construyen con lo que ya hay**. Lo interesante es dónde aparecen sin que
las escribas: **la pila de llamadas está en todos**, y **PL/I tiene una pila de VARIABLES**, que no
tiene nadie más.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es la **disciplina de acceso**, no la estructura, y estos lenguajes lo enseñan porque
> enseñan las dos caras. Por un lado, la construcción explícita: un arreglo con un índice —lo que hacen
> COBOL, Fortran, RPG y PL/I— o un contenedor de biblioteca. Por otro, **dónde la usa el sistema**:
> **Ada tiene colas en el lenguaje** —las entradas de una tarea son una cola con disciplina
> seleccionable—, **RPG tiene las colas de datos del sistema operativo**, y **COBOL vive dentro de un
> monitor transaccional que es, en esencia, una cola**.
>
> Y **PL/I** aporta la rareza de la página: `controlled` hace que una **variable** sea una pila.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: una línea con enteros separados por espacio → stdout: `pila=<orden LIFO> cola=<orden FIFO>`
- **Regla:** `pila = inverso(lista); cola = lista`

| stdin | esperado |
|---|---|
| `1 2 3` | `pila=3-2-1 cola=1-2-3` |
| `5` | `pila=5 cola=5` |
| `1 2 3 4` | `pila=4-3-2-1 cola=1-2-3-4` |

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
PROGRAM-ID. PILACOLA.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(200).
01  TOKEN   PIC X(20).
01  TLEN    PIC 9(2) COMP VALUE 0.
01  I       PIC 9(4) COMP.
01  L       PIC 9(4) COMP.
01  N       PIC 9(4) COMP VALUE 0.
01  TABLA.
    05  ELEM  PIC S9(9) COMP-3 OCCURS 100 TIMES.
01  PILA    PIC X(200) VALUE SPACES.
01  COLA    PIC X(200) VALUE SPACES.
01  PPOS    PIC 9(4) COMP VALUE 1.
01  CPOS    PIC 9(4) COMP VALUE 1.
01  LP      PIC 9(4) COMP.
01  LC      PIC 9(4) COMP.
01  ED      PIC -(8)9.
01  TXT     PIC X(10).

PROCEDURE DIVISION.
    ACCEPT LINEA
    MOVE SPACES TO TOKEN
    PERFORM VARYING I FROM 1 BY 1 UNTIL I > 200
        IF LINEA(I:1) = SPACE
            PERFORM CERRAR-TOKEN
        ELSE
            ADD 1 TO TLEN
            MOVE LINEA(I:1) TO TOKEN(TLEN:1)
        END-IF
    END-PERFORM
    PERFORM CERRAR-TOKEN

    *> LIFO: se saca por el mismo extremo por el que se metió
    PERFORM VARYING I FROM N BY -1 UNTIL I < 1
        MOVE ELEM(I) TO ED
        MOVE FUNCTION TRIM(ED) TO TXT
        PERFORM MEDIR
        MOVE TXT(1:L) TO PILA(PPOS:L)
        ADD L TO PPOS
        IF I > 1
            MOVE "-" TO PILA(PPOS:1)
            ADD 1 TO PPOS
        END-IF
    END-PERFORM

    *> FIFO: se saca por el extremo contrario
    PERFORM VARYING I FROM 1 BY 1 UNTIL I > N
        MOVE ELEM(I) TO ED
        MOVE FUNCTION TRIM(ED) TO TXT
        PERFORM MEDIR
        MOVE TXT(1:L) TO COLA(CPOS:L)
        ADD L TO CPOS
        IF I < N
            MOVE "-" TO COLA(CPOS:1)
            ADD 1 TO CPOS
        END-IF
    END-PERFORM

    COMPUTE LP = PPOS - 1
    COMPUTE LC = CPOS - 1
    DISPLAY "pila=" PILA(1:LP) " cola=" COLA(1:LC)
    STOP RUN.

MEDIR.
    MOVE 0 TO L
    INSPECT FUNCTION REVERSE(TXT) TALLYING L FOR LEADING SPACE
    COMPUTE L = 10 - L.

CERRAR-TOKEN.
    IF TLEN > 0
        ADD 1 TO N
        COMPUTE ELEM(N) = FUNCTION NUMVAL(TOKEN)
        MOVE SPACES TO TOKEN
        MOVE 0 TO TLEN
    END-IF.
```

**Lo que esta clase enseña en COBOL.** COBOL **no tiene pilas ni colas**, y construirlas es lo de este
programa: una tabla y un índice. Con `ADD 1 TO TOPE` y `SUBTRACT 1 FROM TOPE` se tiene una pila; con
dos índices, una cola circular.

Lo que hace interesante esta clase en COBOL es dónde **sí** hay colas, y es en un sitio que define la
arquitectura de los sistemas de misión crítica: **el monitor transaccional**.

Un programa COBOL de banca no se ejecuta suelto. Vive dentro de **CICS** o **IMS**, y esos sistemas
son, en el fondo, gestores de colas:

```text
Terminal → [cola de entrada] → CICS → programa COBOL → [cola de salida] → Terminal
```

Y COBOL habla con esas colas mediante llamadas del monitor:

```cobol
EXEC CICS WRITEQ TS QUEUE('MICOLA') FROM(DATOS) LENGTH(100) END-EXEC
EXEC CICS READQ  TS QUEUE('MICOLA') INTO(DATOS) LENGTH(LON)  END-EXEC
```

Las **colas temporales (TSQ)** y las **colas transitorias (TDQ)** de CICS son colas de verdad, con
persistencia, recuperación tras caída y participación en la transacción. Una TDQ puede además
**disparar automáticamente un programa** cuando acumula N elementos — es una cola con consumidor
automático, de los años setenta.

En IMS, el modelo es todavía más explícito: **un programa lee mensajes de una cola, los procesa y
escribe respuestas en otra**. Es exactamente la arquitectura que hoy se llama *microservicios con
mensajería*, y lleva funcionando cincuenta años sobre las mismas ideas.

Cuando alguien describe Kafka o RabbitMQ a un programador de mainframe, la respuesta suele ser que eso
ya existía y se llamaba gestor de colas. No le falta razón.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program pilacola
   implicit none
   integer :: v(100), n, ios, i
   character(len=400) :: linea, pila, cola
   character(len=20)  :: buf

   read(*, '(A)') linea

   n = 0
   do i = 1, 100
      read(linea, *, iostat=ios) v(1:i)
      if (ios /= 0) exit
      n = i
   end do

   pila = ''
   do i = n, 1, -1                    ! LIFO
      write(buf, '(I0)') v(i)
      if (i == n) then
         pila = trim(buf)
      else
         pila = trim(pila) // '-' // trim(buf)
      end if
   end do

   cola = ''
   do i = 1, n                        ! FIFO
      write(buf, '(I0)') v(i)
      if (i == 1) then
         cola = trim(buf)
      else
         cola = trim(cola) // '-' // trim(buf)
      end if
   end do

   write(*, '(A)') 'pila=' // trim(pila) // ' cola=' // trim(cola)
end program pilacola
```

**Lo que esta clase enseña en Fortran.** Fortran **no tiene pilas ni colas**, y hay una razón
histórica que va más allá de la biblioteca: **el Fortran hasta 1990 no tenía recursión**.

```fortran
      SUBROUTINE F(N)
      CALL F(N-1)      ! ILEGAL en FORTRAN 77
      END
```

Sin recursión, las variables locales se podían asignar **estáticamente**, una sola copia por
subrutina, sin pila de activación. Eso permitía compilar para máquinas sin hardware de pila y generar
código muy rápido, y era la norma en el Fortran clásico.

Fortran 90 introdujo `recursive` como palabra clave explícita, y **Fortran 2018 hizo la recursión el
comportamiento por defecto**, con `non_recursive` para pedir lo contrario. Sesenta años para dar por
supuesto lo que casi todos los lenguajes daban por supuesto desde Algol 60.

Esa historia explica por qué muchos algoritmos clásicos en Fortran están escritos **con una pila
explícita** en lugar de recursión: recorridos de árboles, ordenación rápida, resolución de mallas.

```fortran
integer :: pila(1000), tope
tope = 0
tope = tope + 1;  pila(tope) = nodo      ! apilar
nodo = pila(tope); tope = tope - 1        ! desapilar
```

Ese idioma sigue apareciendo en código numérico moderno, y no siempre por herencia: **una pila
explícita tiene tamaño acotado y predecible**, mientras que la recursión puede desbordar la pila del
sistema. En cálculo con mallas de millones de elementos, eso importa.

Hoy `stdlib` no incluye pilas ni colas —se consideran triviales sobre `allocatable`— y el idioma
recomendado es un arreglo con un contador, exactamente como en este programa.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;
with Ada.Containers.Vectors;

procedure Pilacola is
   package Vectores is new Ada.Containers.Vectors (Positive, Integer);
   use Vectores;

   V      : Vector;
   Linea  : String (1 .. 400);
   Ultimo : Natural;
   Pos    : Integer := 1;
   Valor  : Integer;
   Fin    : Positive;
   N      : Integer;
begin
   Get_Line (Linea, Ultimo);

   loop
      while Pos <= Ultimo and then Linea (Pos) = ' ' loop
         Pos := Pos + 1;
      end loop;
      exit when Pos > Ultimo;

      Get (Linea (Pos .. Ultimo), Valor, Fin);
      V.Append (Valor);
      Pos := Fin + 1;
   end loop;

   N := Integer (V.Length);

   Put ("pila=");
   for I in reverse 1 .. N loop
      Put (V.Element (I), Width => 1);
      if I > 1 then Put ("-"); end if;
   end loop;

   Put (" cola=");
   for I in 1 .. N loop
      Put (V.Element (I), Width => 1);
      if I < N then Put ("-"); end if;
   end loop;

   New_Line;
end Pilacola;
```

**Lo que esta clase enseña en Ada.** Ada construye pilas y colas con `Vectors` o con
`Doubly_Linked_Lists`, y además tiene un paquete dedicado —`Ada.Containers.Synchronized_Queue_
Interfaces` y sus implementaciones `Unbounded_Synchronized_Queues` y
`Bounded_Priority_Queues`— que son **colas seguras para concurrencia**, con bloqueo cuando están
vacías o llenas.

Pero lo importante de esta clase en Ada está en otro sitio: **la cola es una construcción del
lenguaje, dentro del modelo de tareas**.

```ada
task Servidor is
   entry Atender (Peticion : in Datos);     --  una ENTRADA es una COLA
end Servidor;

task body Servidor is
begin
   loop
      accept Atender (Peticion : in Datos) do
         ...
      end Atender;
   end loop;
end Servidor;
```

Cada `entry` de una tarea **tiene su propia cola de llamadas en espera**, gestionada por el
*runtime*. Quien llama a `Servidor.Atender (X)` se bloquea hasta que la tarea acepta. No hay que
escribir la cola: **es parte del mecanismo de comunicación**.

Y la disciplina de esa cola se puede elegir, lo que en un sistema de tiempo real es crítico:

```ada
pragma Queuing_Policy (Priority_Queuing);    --  por prioridad, no por llegada
pragma Locking_Policy (Ceiling_Locality);     --  techo de prioridad
```

`Queuing_Policy` decide si las llamadas se atienden por orden de llegada (`FIFO_Queuing`, el defecto)
o por prioridad del llamante. Y `Ceiling_Locality` implementa el **protocolo de techo de prioridad**,
que resuelve la inversión de prioridades — el fallo que casi acaba con la misión Mars Pathfinder en
1997.

Que la política de encolado sea una directiva del lenguaje, y no una decisión escondida en una
biblioteca, es exactamente lo que se espera de un lenguaje diseñado para sistemas donde una cola mal
disciplinada mata gente.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Pilacola;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  V: array of Integer;
  Linea, Tok, Pila, Cola: string;
  I: Integer;
  C: Char;

begin
  ReadLn(Linea);

  SetLength(V, 0);
  Tok := '';
  for I := 1 to Length(Linea) + 1 do
  begin
    if I <= Length(Linea) then C := Linea[I] else C := ' ';
    if C = ' ' then
    begin
      if Tok <> '' then
      begin
        SetLength(V, Length(V) + 1);
        V[High(V)] := StrToInt(Tok);
        Tok := '';
      end;
    end
    else
      Tok := Tok + C;
  end;

  Pila := '';
  for I := High(V) downto 0 do            { LIFO }
  begin
    if Pila <> '' then Pila := Pila + '-';
    Pila := Pila + IntToStr(V[I]);
  end;

  Cola := '';
  for I := 0 to High(V) do                { FIFO }
  begin
    if Cola <> '' then Cola := Cola + '-';
    Cola := Cola + IntToStr(V[I]);
  end;

  WriteLn('pila=', Pila, ' cola=', Cola);
end.
```

**Lo que esta clase enseña en Pascal.** Pascal es **el lenguaje en el que se enseñaron pilas y colas a
una generación entera**, en el libro que Wirth publicó en 1976: *Algorithms + Data Structures =
Programs*.

La versión canónica del libro usa punteros y registros:

```pascal
type
  PNodo = ^TNodo;
  TNodo = record
    Valor: Integer;
    Siguiente: PNodo;
  end;

procedure Apilar(var Tope: PNodo; X: Integer);
var N: PNodo;
begin
  New(N);
  N^.Valor := X;
  N^.Siguiente := Tope;      { el nuevo apunta al antiguo tope }
  Tope := N;                  { y pasa a ser el tope }
end;
```

Cuatro líneas que millones de personas copiaron a mano en un cuaderno. La notación `^` —`PNodo` es
"puntero a nodo", `N^.Valor` es "el campo Valor de lo que apunta N"— sigue siendo la más clara para
explicar la indirección, más que el `*` y el `->` de C.

Hoy Free Pascal y Delphi traen las estructuras hechas:

```pascal
uses Generics.Collections;
var
  P: TStack<Integer>;
  C: TQueue<Integer>;
begin
  P := TStack<Integer>.Create;
  P.Push(1); P.Pop; P.Peek;
  C := TQueue<Integer>.Create;
  C.Enqueue(1); C.Dequeue;
end;
```

Y hay una pila que Pascal usa sin que se vea, y que conviene mencionar porque es una decisión de
diseño del lenguaje: **el `record` se pasa por valor y se copia en la pila**, salvo que se declare
`var` o `const`. Pasar un registro grande sin `const` copia todos sus bytes en cada llamada, y es una
de las causas más frecuentes de código Pascal lento — el equivalente de pasar por valor en C++ sin
referencia constante.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let ((v '()))
  (loop for x = (read *standard-input* nil nil)
        while x
        do (push x v))                  ; push construye una PILA
  (format t "pila=~{~D~^-~} cola=~{~D~^-~}~%" v (reverse v)))
```

**Lo que esta clase enseña en Common Lisp.** En Lisp, **una lista ya es una pila**, y la sintaxis lo
reconoce: `push` y `pop` son macros del estándar que operan sobre cualquier **lugar** (clase 095).

```lisp
(push x lista)          ; añadir por delante -- O(1)
(pop lista)             ; sacar por delante -- O(1)
(push x (gethash k tabla))       ; sobre una entrada de tabla hash
(push x (cdr registro))           ; sobre cualquier lugar asignable
```

Por eso este programa construye la pila **sin querer**: leer con `push` deja la lista en orden
inverso, que es exactamente el orden LIFO. La cola se obtiene con `reverse`.

Y ese es el idioma más característico de Lisp para acumular resultados: **construir al revés con
`push` e invertir al final**, que es O(n), en lugar de añadir al final, que sería O(n²).

Para una cola de verdad —añadir por un extremo y sacar por el otro, ambas en O(1)— la lista simple no
basta, y Common Lisp ofrece dos respuestas:

**La lista con puntero a la cola**, que es el idioma clásico:

```lisp
(defstruct cola (cabeza nil) (final nil))
```

**Y `nconc` sobre una lista con celda de guarda**, que es lo que hace `loop ... collect` internamente:
`collect` mantiene un puntero al último cons y añade ahí, así que **acumula en orden y en O(1) por
elemento**.

```lisp
(loop for x in lista collect (* x 2))     ; en ORDEN, sin reverse, sin coste cuadrático
```

Saber eso cambia cómo se escribe: si `loop ... collect` sirve, no hace falta el idioma de
`push` + `reverse`.

Lisp tiene además la pila más visible de todos estos lenguajes: **la pila de llamadas es un objeto
inspeccionable**. Cuando salta un error, el depurador muestra los marcos, permite examinar sus
variables, **reanudar desde cualquiera de ellos** y reintentar con un valor distinto. Es el sistema de
condiciones y reinicios, y no tiene equivalente en el núcleo.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea
set v [split [string trim $linea]]

puts "pila=[join [lreverse $v] -] cola=[join $v -]"
```

**Lo que esta clase enseña en Tcl.** En Tcl, una lista **es** una pila y una cola a la vez, con los
comandos de siempre:

```tcl
lappend pila $x                  ;# apilar -- O(1) amortizado
set x [lindex $pila end]         ;# cima
set pila [lrange $pila 0 end-1]  ;# desapilar -- copia la lista
```

Ese `lrange` para desapilar es lo que estuvo mal durante veinte años: **es O(n)**, porque construye
una lista nueva. Tcl 8.7 lo arregló con dos comandos nuevos:

```tcl
lpop pila                        ;# saca el último -- O(1)
lpop cola 0                      ;# saca el primero
lremove lista 2                  ;# quita por índice
```

La notación **`end`, `end-1`, `end-3`** para indexar desde el final es de Tcl y es de las cosas que
otros lenguajes copiaron con otra sintaxis —el `-1` de Python, el `^1` de C#—.

Donde Tcl tiene colas de verdad es en su modelo de eventos, y ahí está lo característico del lenguaje:
**el bucle de eventos es una cola de guiones pendientes**.

```tcl
after 1000 { puts "un segundo después" }     ;# encolar para más tarde
after idle { ... }                            ;# cuando no haya nada más que hacer
fileevent $canal readable { ... }             ;# cuando lleguen datos
vwait bandera                                  ;# procesar eventos hasta que cambie
```

`after` **encola un guion** para ejecutarlo cuando corresponda; `after idle` lo pone al final de la
cola de trabajo pendiente. Es exactamente el modelo del bucle de eventos de JavaScript —cola de
tareas, tareas de microcola, sin hilos— y **Tcl lo tenía en 1990**, cinco años antes de que existiera
JavaScript.

Tk, la interfaz gráfica, está construida sobre esa cola, y es la razón de que programar una interfaz
en Tcl sea tan directo: no hay hilos que sincronizar, hay guiones encolados.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;
my @v = split ' ', $linea;

print "pila=", join('-', reverse @v),
      " cola=", join('-', @v), "\n";
```

**Lo que esta clase enseña en Perl.** Perl es el lenguaje de esta página donde pila y cola están más
cerca de la superficie, porque **las cuatro operaciones tienen nombre propio** desde 1987:

```perl
push @a, $x;      pop @a;        # PILA: por el final
unshift @a, $x;   shift @a;      # COLA: entrar por el final, salir por delante
```

Los nombres vienen del shell de Unix —`shift` desplaza los argumentos posicionales— y son tan
idiomáticos que se usan sin pensar. Una cola es `push` + `shift`; una pila es `push` + `pop`.

Y como se vio en la clase 090, **`shift` es O(1)** por una optimización deliberada, así que la cola es
eficiente sin trucos.

Perl añade además `splice`, que generaliza las cuatro:

```perl
splice(@a, $i, 1);            # quitar el elemento i
splice(@a, $i, 0, $x);        # insertar en la posición i
splice(@a, 0, 0, @otros);     # unshift múltiple
```

Y hay dos pilas invisibles en Perl que merecen mención porque explican cómo funciona el lenguaje.

**`@_`, la pila de argumentos.** No es una copia: es un **alias** a los argumentos del llamante
(clase 079), y `shift` sobre ella es la forma canónica de leer parámetros.

**`local`, la pila de valores globales.** `local $/ = undef;` guarda el valor anterior de la variable
global **en una pila interna** y lo restaura automáticamente al salir del ámbito (clase 082). Es
alcance dinámico implementado como una pila, y es el mismo mecanismo que las variables especiales de
Lisp y las `controlled` de PL/I — tres lenguajes muy distintos con la misma idea.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>
#include <iterator>
#include <queue>
#include <stack>
#include <vector>

int main() {
    std::vector<int> v{std::istream_iterator<int>(std::cin),
                       std::istream_iterator<int>()};

    std::stack<int> p;
    std::queue<int> c;
    for (int x : v) { p.push(x); c.push(x); }

    std::cout << "pila=";
    for (bool primero = true; !p.empty(); p.pop(), primero = false) {
        if (!primero) std::cout << '-';
        std::cout << p.top();
    }

    std::cout << " cola=";
    for (bool primero = true; !c.empty(); c.pop(), primero = false) {
        if (!primero) std::cout << '-';
        std::cout << c.front();
    }

    std::cout << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** `std::stack` y `std::queue` **no son contenedores**: son
**adaptadores de contenedor**, y esa distinción es una de las ideas más limpias de la STL.

```cpp
std::stack<int>                              // por debajo, un std::deque
std::stack<int, std::vector<int>>            // o un vector, si se prefiere
std::queue<int, std::list<int>>              // la cola, sobre una lista
```

Un adaptador **no implementa nada**: envuelve otro contenedor y **restringe su interfaz** a las
operaciones permitidas. `std::stack` sobre un `vector` no añade código; quita `operator[]`, `begin()`
y todo lo que rompería la disciplina LIFO.

Eso es encapsulación en su forma más pura —**la estructura de datos no cambia, cambia el contrato**— y
es exactamente el punto del cierre de esta clase.

Detalles que conviene conocer:

- **`pop()` no devuelve nada.** Hay que hacer `top()` y luego `pop()`. La razón es la **seguridad ante
  excepciones**: si `pop()` devolviera por valor y el constructor de copia lanzara, el elemento ya
  habría salido de la pila y se perdería. Separar las dos operaciones lo evita. Es la decisión de
  diseño más explicada y más criticada de la STL.
- **El contenedor por defecto es `std::deque`**, no `vector`, porque `deque` no reubica al crecer.
- **`std::priority_queue`** es el tercer adaptador: una cola que saca siempre el mayor, implementada
  como montículo binario sobre un `vector`. Es lo que hace falta para Dijkstra y para cualquier
  planificador.

Y la pila que C++ usa sin decirlo es la del propio programa: **los destructores se ejecutan en orden
inverso al de construcción**, que es LIFO. Todo el modelo RAII —adquirir en el constructor, liberar en
el destructor— depende de esa disciplina, y es la razón de que C++ pueda gestionar recursos sin
recolector de basura.

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

dcl-pi PILACOLA;
  entrada char(200) const;
end-pi;

dcl-s elem int(10) dim(100);
dcl-s n    int(10) inz(0);
dcl-s i    int(10);
dcl-s tok  varchar(20) inz('');
dcl-s c    char(1);
dcl-s pila varchar(200) inz('');
dcl-s cola varchar(200) inz('');

for i = 1 to %len(%trimr(entrada)) + 1;
  if i <= %len(%trimr(entrada));
    c = %subst(entrada : i : 1);
  else;
    c = ' ';
  endif;
  if c = ' ';
    if tok <> '';
      n += 1;
      elem(n) = %int(tok);
      tok = '';
    endif;
  else;
    tok += c;
  endif;
endfor;

for i = n downto 1;              // LIFO
  if pila <> '';
    pila += '-';
  endif;
  pila += %char(elem(i));
endfor;

for i = 1 to n;                  // FIFO
  if cola <> '';
    cola += '-';
  endif;
  cola += %char(elem(i));
endfor;

dsply ('pila=' + pila + ' cola=' + cola);

*inlr = *on;
return;
```

**Lo que esta clase enseña en RPG.** RPG construye pilas y colas con una tabla y un índice, como
COBOL. Lo interesante es que **IBM i tiene colas en el sistema operativo**, y RPG las usa como si
fueran parte del lenguaje.

**Las colas de datos** (`*DTAQ`) son objetos del sistema, persistentes y compartidos entre trabajos:

```rpgle
dcl-pr enviarDatos extpgm('QSNDDTAQ');
  cola  char(10) const;
  bib   char(10) const;
  lon   packed(5) const;
  datos char(1000) const;
end-pr;

// y para recibir, QRCVDTAQ con un TIEMPO DE ESPERA:
//   espera = -1  -> bloquear indefinidamente hasta que llegue algo
//   espera = 30  -> esperar 30 segundos
```

Una cola de datos tiene tres propiedades que la convierten en infraestructura de verdad:

1. **Bloqueo con espera**: un trabajo puede quedarse esperando sin consumir CPU.
2. **Disciplina seleccionable**: FIFO, **LIFO** o **por clave** —una cola con clave permite recibir
   solo los mensajes que coincidan con un patrón—.
3. **Persistencia opcional**: sobrevive al reinicio del sistema.

Con eso se construyen desde los años ochenta las arquitecturas asíncronas de IBM i: un trabajo
servidor que espera en una cola, varios clientes que encolan peticiones. Es lo que hoy se monta con
RabbitMQ, resuelto por el sistema operativo.

Y **las colas de mensajes** (`*MSGQ`) son la otra mitad: cada trabajo, cada usuario y cada dispositivo
tiene la suya, y los programas se comunican con el operador enviando mensajes a ellas.

El tema se repite en toda esta parte del curso: **en las plataformas de gestión, lo que en otros
lenguajes es una biblioteca aquí es un objeto del sistema operativo**.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 pilacola: procedure options(main);

    declare linea char(200) varying;
    declare v(100) fixed binary(31);
    declare (n, i) fixed binary(31);
    declare pila char(200) varying initial('');
    declare cola char(200) varying initial('');
    declare tok char(20) varying initial('');
    declare c char(1);

    get edit (linea) (a(200));
    n = 0;

    do i = 1 to length(linea) + 1;
       if i <= length(linea) then c = substr(linea, i, 1); else c = ' ';
       if c = ' ' then do;
          if tok ^= '' then do;
             n = n + 1;
             v(n) = tok;
             tok = '';
          end;
       end;
       else tok = tok || c;
    end;

    do i = n to 1 by -1;
       if pila ^= '' then pila = pila || '-';
       pila = pila || trim(char(v(i)));
    end;

    do i = 1 to n;
       if cola ^= '' then cola = cola || '-';
       cola = cola || trim(char(v(i)));
    end;

    put skip list ('pila=' || pila || ' cola=' || cola);

 end pilacola;
```

**Lo que esta clase enseña en PL/I.** PL/I tiene la rareza más llamativa de esta clase: **una variable
puede SER una pila**, gracias al atributo `controlled` que ya apareció en la clase 090.

```pli
declare x fixed binary(31) controlled;

allocate x;  x = 1;      /* x vale 1 */
allocate x;  x = 2;      /* x vale 2; el 1 sigue ahí, DEBAJO */
put list (x);            /* 2 */
free x;                  /* desapila */
put list (x);            /* 1  -- ha VUELTO */
```

Cada `allocate` **apila una generación** de la variable y oculta la anterior; cada `free` desapila y
la anterior reaparece. `allocation(x)` dice cuántas generaciones hay.

Es alcance dinámico implementado como estructura de datos, y sirve exactamente para lo mismo que
`local` en Perl y las variables especiales en Lisp: **guardar y restaurar un valor global alrededor de
una llamada**, sin pasarlo como parámetro.

También sirve para escribir algoritmos recursivos sin parámetros de estado, y es una fuente notable de
confusión al leer código ajeno — porque el valor de una variable depende de cuántos `allocate` haya
pendientes en la pila de llamadas.

Para pilas de datos, PL/I tiene todo lo necesario desde 1964: `based`, punteros y `allocate ... set`,
con los que la lista enlazada se escribe igual que en Pascal.

```pli
 declare 1 nodo based(p), 2 valor fixed binary(31), 2 siguiente pointer;
 allocate nodo set(q);
 q -> siguiente = tope;
 tope = q;
```

`q -> siguiente` es la notación de acceso a través de puntero, **anterior al `->` de C** y con el
mismo significado. Es uno de los muchos sitios donde se ve que C heredó más de PL/I de lo que suele
reconocerse.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
PILACOLA ; Pilas y colas -- clase 096
 read linea
 set n = $length(linea, " ")
 set pila = "", cola = ""
 for i=n:-1:1 do
 . if pila '= "" set pila = pila _ "-"
 . set pila = pila _ $piece(linea, " ", i)
 for i=1:1:n do
 . if cola '= "" set cola = cola _ "-"
 . set cola = cola _ $piece(linea, " ", i)
 write "pila=", pila, " cola=", cola, !
 quit
```

**Lo que esta clase enseña en M.** M no tiene pilas ni colas, y las construye con lo de siempre: un
array con subíndices numéricos y un contador, o —más idiomático— **`$order` para recorrer en los dos
sentidos**.

```mumps
 set $order(v(i), -1)     ; el subíndice ANTERIOR: recorrer hacia atrás
 set $order(v(i), 1)      ; el siguiente (por defecto)
```

Ese segundo argumento de `$order` convierte cualquier array en una estructura recorrible en ambos
sentidos, lo que sirve tanto para LIFO como para FIFO sin escribir nada más.

Y M tiene una pila propia del lenguaje que conviene conocer, porque es la respuesta al problema del
alcance global de la clase 082: **`new`**.

```mumps
procesar(x) ;
 new i, temporal          ; APILA los valores actuales de i y temporal
 set i = 1                 ; ... y trabaja con copias nuevas
 quit                       ; al salir, se DESAPILAN los valores anteriores
```

`new` guarda el valor actual de una variable en una pila interna y lo restaura al salir del bloque. Es
exactamente `local` de Perl, `controlled` de PL/I y las variables especiales de Lisp — **cuatro
lenguajes independientes que llegaron a la misma solución**: alcance dinámico implementado como pila.

Sin `new`, cualquier variable que una rutina use pisa la de su llamante, con consecuencias que en un
sistema de un millón de líneas serían intratables. Con `new`, cada rutina declara qué nombres se
reserva.

M tiene además una operación que sí es una cola de verdad y que forma parte del estándar: **`job`**,
que lanza un proceso en segundo plano.

```mumps
 job procesar^INFORME(id)
```

Y en las implementaciones modernas, colas persistentes construidas sobre *globals* con `lock` y
transacciones — que, otra vez, es la estructura de datos del lenguaje haciendo de infraestructura.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| v pila cola unir |

v := stdin nextLine substrings collect: [ :cada | cada asNumber ].

unir := [ :col |
    (col collect: [ :cada | cada printString ])
        inject: '' into: [ :acc :cada |
            acc isEmpty ifTrue: [ cada ] ifFalse: [ acc, '-', cada ] ] ].

pila := unir value: v reverse.
cola := unir value: v.

Transcript show: 'pila=', pila, ' cola=', cola; cr.
```

**Lo que esta clase enseña en Smalltalk.** `OrderedCollection` es a la vez pila y cola, con mensajes
que dicen por qué extremo se opera:

```smalltalk
c addLast: x.     c removeLast.      "PILA"
c addLast: x.     c removeFirst.     "COLA"
c addFirst: x.
c removeFirst: 3.                     "quitar tres de golpe"
```

Y como se vio en la clase 090, **las dos son O(1) amortizado** porque hay hueco por ambos extremos.

Lo que hace distinta a esta clase en Smalltalk es que **la pila de llamadas es un objeto normal del
sistema**, y esa es una de las ideas más radicales del lenguaje.

```smalltalk
thisContext                          "el marco de pila ACTUAL, como objeto"
thisContext sender                    "quién me llamó"
thisContext receiver                  "sobre qué objeto"
thisContext tempAt: 1                 "sus variables locales"
```

`thisContext` es un objeto de la clase `MethodContext`, y se puede inspeccionar, **modificar** y
**guardar**. Con eso, Smalltalk implementa **dentro del propio lenguaje** cosas que en otros
requieren soporte de la máquina virtual:

- **El depurador**: es un programa Smalltalk que recorre contextos.
- **Las excepciones**: `signal`, `return:`, `retry` y `resume:` manipulan la pila.
- **Las continuaciones y las corrutinas** (clase 066): guardar un contexto y reanudarlo después.
- **Modificar un método y seguir ejecutando desde el marco actual**, sin reiniciar.

Esa última es la que sorprende a quien viene de fuera: al saltar un error, el depurador permite
**escribir el método que faltaba y continuar la ejecución desde donde estaba**. Programar
descubriendo lo que hace falta según hace falta.

Y para colas concurrentes, la biblioteca trae `SharedQueue`, con `next` bloqueante — el mismo diseño
que las colas de datos de IBM i y las colas sincronizadas de Ada.

---

## Y de vuelta a la clase

Lo transferible: **pila y cola no son estructuras, son contratos sobre por dónde entran y salen los
datos**, y elegir el contrato correcto decide el comportamiento del sistema entero. Una pila procesa
lo más reciente primero: bien para deshacer, para recorrer en profundidad y para el intérprete; mal
para atender peticiones, porque las viejas se quedan al fondo para siempre. Una cola es justa y
predecible. Cuando veas un sistema donde algunas tareas nunca se atienden, la primera pregunta es si
alguien puso una pila donde debía haber una cola.

⏮️ [Volver a la clase 096](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
