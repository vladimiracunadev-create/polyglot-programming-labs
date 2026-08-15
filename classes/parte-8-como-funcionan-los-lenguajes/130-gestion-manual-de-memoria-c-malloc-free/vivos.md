# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 130

> [⬅️ Volver a la clase 130](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Reservar `n` enteros, usarlos y liberarlos. **Cinco de estos lenguajes te hacen escribir la
liberación** —COBOL, RPG, PL/I, C++ con punteros crudos y Fortran con `pointer`— y sus ecosistemas
llevan décadas conviviendo con las consecuencias. Y aquí hay una lección que la industria tardó
cuarenta años en aceptar: **la mayoría de esos lenguajes NO tienen fugas en producción, y no es por
disciplina — es porque casi no reservan**.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es **quién libera y cuándo**, y estos lenguajes lo enseñan porque muestran las cuatro
> estrategias que funcionan. **No reservar**: COBOL y RPG clásicos, con memoria estática (clase 128).
> **Liberar por ámbito**: `allocatable` de Fortran, los tipos controlados de Ada, RAII en C++. **Liberar
> por región**: los grupos de activación de IBM i, las áreas de PL/I, `GETMAIN` de CICS. **Y liberar a
> mano**: lo que queda, y donde están los errores.
>
> La cuarta es la que produce **fuga, doble liberación y uso tras liberar** — tres fallos que las otras
> tres estrategias eliminan por construcción.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: un entero `n` (n >= 1) → stdout: `reservado=<n> suma=<1+...+n>`
- **Regla:** `reservar n enteros, llenarlos 1..n, sumar, liberar`

| stdin | esperado |
|---|---|
| `5` | `reservado=5 suma=15` |
| `1` | `reservado=1 suma=1` |
| `3` | `reservado=3 suma=6` |

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
PROGRAM-ID. MANUAL.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  N       PIC 9(4) COMP.
01  I       PIC 9(4) COMP.
01  SUMA    PIC 9(9) COMP VALUE 0.
01  TABLA.
    05  ELEM  PIC 9(9) COMP OCCURS 1 TO 1000 TIMES DEPENDING ON N.
01  ED-N    PIC Z(3)9.
01  ED-S    PIC Z(8)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    COMPUTE N = FUNCTION NUMVAL(LINEA)

    PERFORM VARYING I FROM 1 BY 1 UNTIL I > N
        MOVE I TO ELEM(I)
        ADD I TO SUMA
    END-PERFORM

    MOVE N    TO ED-N
    MOVE SUMA TO ED-S
    DISPLAY "reservado=" FUNCTION TRIM(ED-N)
            " suma=" FUNCTION TRIM(ED-S)
    STOP RUN.
```

**Lo que esta clase enseña en COBOL.** Este programa **no reserva nada**, y esa es la respuesta de COBOL
a esta clase: **la mejor gestión manual de memoria es la que no hace falta**.

Como se dijo en la clase 128, la `WORKING-STORAGE` es estática y su tamaño se conoce al compilar. **No
hay `free` que olvidar porque no hay `malloc` que escribir.**

Y ese modelo, que parece una limitación, es lo que permite garantizar el comportamiento de un sistema
con miles de transacciones por segundo: **el consumo de memoria de cada tarea es una constante
conocida**.

Cuando sí hace falta reservar, COBOL usa lo de la clase 128:

```cobol
ALLOCATE 1000 CHARACTERS RETURNING PTR
FREE PTR
EXEC CICS GETMAIN SET(PTR) LENGTH(1000) END-EXEC
EXEC CICS FREEMAIN DATAPOINTER(PTR) END-EXEC
```

Y ahí está lo que hace distinto al mundo COBOL, y es la tercera estrategia del cierre de esta clase:
**la liberación por región**.

**Todo lo que reserva una transacción CICS se libera al terminar la transacción**, con o sin `FREEMAIN`,
haya fallado o no. La unidad de trabajo tiene un final, y ese final limpia.

Con transacciones que duran milisegundos, **una fuga dentro de una transacción es irrelevante**: se
recoge sola en cuanto termina.

Eso explica una observación que sorprende a quien viene de otros entornos: **los sistemas COBOL no
tienen problemas de fugas de memoria**, pese a estar escritos en un lenguaje sin recolector y con
liberación manual.

No es disciplina: **es que la arquitectura hace que la fuga no tenga tiempo de acumularse**.

Y es exactamente el mismo argumento que hoy se usa a favor de los procesos efímeros, los contenedores
que se reinician y las funciones sin servidor: **si el proceso vive poco, la gestión de memoria importa
menos**.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program manual
   implicit none
   integer, pointer :: v(:)         ! puntero: hay que liberar A MANO
   integer :: n, i, suma, ierr

   read(*, *) n

   allocate(v(n), stat=ierr)
   if (ierr /= 0) then
      write(*, '(A)') 'sin memoria'
      stop 1
   end if

   suma = 0
   do i = 1, n
      v(i) = i
      suma = suma + i
   end do

   write(*, '(A,I0,A,I0)') 'reservado=', n, ' suma=', suma

   deallocate(v)                    ! obligatorio con `pointer`
   nullify(v)
end program manual
```

**Lo que esta clase enseña en Fortran.** Este programa usa **`pointer` en vez de `allocatable`** para
que la liberación sea obligatoria, y así se ve la diferencia que la clase 128 explicaba:

```fortran
integer, pointer     :: p(:)    ! hay que deallocate: si no, FUGA
integer, allocatable :: a(:)     ! se libera SOLO al salir del ámbito
```

**Esa es toda la diferencia**, y es la razón de la guía moderna de Fortran: **usa `allocatable` salvo
que necesites alias o estructuras enlazadas**.

Y `stat=ierr` es la otra pieza que esta clase debe destacar:

```fortran
allocate(v(n), stat=ierr)
if (ierr /= 0) ...
deallocate(v, stat=ierr)
```

**Sin `stat=`, un fallo de reserva termina el programa.** En un cálculo de ocho horas eso es
inaceptable, y `stat=` permite reducir el tamaño del problema y seguir, o guardar el estado antes de
morir.

Y Fortran tiene una construcción propia y muy útil para el problema del cierre de esta clase —**los
caminos que no pasan por el `deallocate`**—:

```fortran
block
   integer, allocatable :: temporal(:)
   allocate(temporal(1000000))
   ...
end block                       ! se libera AQUÍ, salga por donde salga
```

**El `block`** de Fortran 2008 (clase 103) da un ámbito interno, y **los `allocatable` declarados en él
se liberan al salir**, incluido por `exit`, `return` o `error stop`.

Es liberación por ámbito con la sintaxis de un bloque, y es la respuesta idiomática al problema de esta
clase.

Y para diagnosticar fugas cuando se usan punteros, el ecosistema tiene lo esperable:

```bash
valgrind --leak-check=full ./programa
gfortran -fsanitize=address
gfortran -fcheck=pointer          # detecta punteros no asociados
```

**`-fcheck=pointer`** comprueba en ejecución que un puntero esté asociado antes de usarlo, que es
exactamente el fallo que `allocatable` hace imposible.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;
with Ada.Unchecked_Deallocation;

procedure Manual is
   type Vector is array (Positive range <>) of Integer;
   type Ref is access Vector;

   procedure Liberar is new Ada.Unchecked_Deallocation (Vector, Ref);

   N    : Integer;
   V    : Ref;
   Suma : Integer := 0;
begin
   Get (N);

   V := new Vector (1 .. N);

   for I in 1 .. N loop
      V (I) := I;
      Suma := Suma + I;
   end loop;

   Put ("reservado=");  Put (N,    Width => 1);
   Put (" suma=");      Put (Suma, Width => 1);
   New_Line;

   Liberar (V);          --  V queda en null automáticamente
end Manual;
```

**Lo que esta clase enseña en Ada.** `Ada.Unchecked_Deallocation` tiene dos detalles que lo hacen más
seguro que un `free`, y merece verlos:

**Primero: pone el puntero a `null`.**

```ada
Liberar (V);        --  V pasa a ser null, NO queda colgado
```

**El parámetro es `in out`**, así que después de liberar, el puntero no apunta a memoria muerta. En C,
`free(p)` deja `p` apuntando a memoria liberada, y usarlo es el clásico *use after free*.

**Y segundo: está tipado.** El genérico se instancia con el tipo del objeto y el del acceso, así que
**no se puede liberar un puntero de otro tipo**.

Y Ada ofrece las tres estrategias del cierre de esta clase, y su cultura prefiere las tres primeras:

**No reservar** — con `pragma Restrictions (No_Allocators)` en sistemas certificados (clase 128).

**Liberar por ámbito** — con los **tipos controlados** (clase 103):

```ada
type Recurso is new Ada.Finalization.Controlled with ...;
overriding procedure Finalize (R : in out Recurso);
```

`Finalize` se ejecuta **al salir del ámbito, incluso si se propaga una excepción**. Es RAII, y llegó a
Ada en 1983 — once años antes de que C++ le pusiera nombre.

**Liberar por región** — con los ***storage pools*** (clase 128):

```ada
for Ref'Storage_Pool use Mi_Arena;
```

Un gestor propio por tipo de acceso, con el que se implementa una arena que suelta todo de golpe.

Y hay una comprobación que Ada hace y que casi nadie más: **al terminar un ámbito con un
`Storage_Pool` propio, se puede liberar el pool entero**, con lo que las fugas dentro de él dejan de
importar.

Es la misma idea que las transacciones de CICS de esta clase y que los grupos de activación de IBM i:
**si la región tiene un final, la fuga tiene fecha de caducidad**.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Manual;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  V: PInteger;
  N, I, Suma: Integer;
  Q: PInteger;

begin
  Read(N);

  GetMem(V, N * SizeOf(Integer));      { reservar a mano }

  Suma := 0;
  Q := V;
  for I := 1 to N do
  begin
    Q^ := I;
    Suma := Suma + I;
    Inc(Q);                              { requiere {$POINTERMATH} o PInteger }
  end;

  WriteLn('reservado=', IntToStr(N), ' suma=', IntToStr(Suma));

  FreeMem(V);                            { liberar a mano }
end.
```

**Lo que esta clase enseña en Pascal.** Pascal tiene tres pares de reserva y liberación, y usarlos
cruzados es un error clásico:

```pascal
New(P);      Dispose(P);         { tipado: reserva SizeOf del tipo (clase 128) }
GetMem(P, T); FreeMem(P);          { sin tipo: como malloc }
Obj := TC.Create;  Obj.Free;        { objetos, con constructor y destructor }
```

**Mezclarlos —`New` con `FreeMem`, o `Create` con `Dispose`— produce corrupción del montón**, y es de
los errores más difíciles de diagnosticar del ecosistema.

Y el problema del cierre de esta clase —**los caminos que no pasan por la liberación**— tiene en Pascal
la solución canónica, que es la que se enseña desde el primer día:

```pascal
Obj := TClase.Create;
try
  ...                    { salga por donde salga }
finally
  Obj.Free;               { esto SIEMPRE se ejecuta }
end;
```

**`try...finally` es tan omnipresente en el código Delphi que se escribe sin pensar**, y es lo que
compensa la ausencia de destructores automáticos (clase 103).

Y hay dos alternativas que eliminan el problema:

```pascal
var I: IInterfaz;                { conteo de referencias: se libera SOLA }
var R: TRegistro;                 { valor: muere con el ámbito }
```

Free Pascal añadió además **los registros gestionados** en la versión 3.2, que son lo más cercano a
RAII que tiene el lenguaje:

```pascal
type
  TRecurso = record
    class operator Initialize(var R: TRecurso);   { constructor }
    class operator Finalize(var R: TRecurso);      { DESTRUCTOR automático }
  end;
```

**Con `Initialize` y `Finalize`, un registro se construye y se destruye solo al entrar y salir del
ámbito.** Es exactamente RAII de C++ y los tipos controlados de Ada, llegado a Pascal en 2020.

Y la herramienta que hizo por la calidad del código Delphi más que ninguna característica del lenguaje
es la de la clase 128: **FastMM**, que al terminar el programa **informa de cada fuga con la pila de
llamadas de dónde se reservó**.

Es la respuesta pragmática del cierre de esta clase: **si el lenguaje no libera solo, que al menos te
diga exactamente qué olvidaste**.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let* ((n (read))
       (v (make-array n))
       (suma 0))
  (dotimes (i n)
    (setf (aref v i) (1+ i))
    (incf suma (1+ i)))
  ;; no hay que liberar: hay recolector de basura (clase 131)
  (format t "reservado=~D suma=~D~%" n suma))
```

**Lo que esta clase enseña en Common Lisp.** **En Lisp no hay gestión manual de memoria**, y esta clase
es el sitio para explicar por qué esa decisión, de 1959, fue tan influyente.

McCarthy inventó la recolección de basura porque **Lisp la necesitaba para existir**: un lenguaje que
construye y descarta listas constantemente no puede pedir al programador que libere cada *cons*.

Y esa decisión tuvo un coste que la industria tardó décadas en aceptar: **pausas impredecibles**. Es la
razón por la que Lisp no se usó en sistemas de tiempo real, y por la que los primeros recolectores
—que paraban el mundo— dieron mala fama al concepto.

Lo que Lisp sí ofrece es control sobre cuánto se reserva, que es la otra mitad del problema:

```lisp
(declare (dynamic-extent lista))          ; "no escapa": puede ir a la PILA (clase 128)
(make-array n :element-type 'double-float) ; vector compacto, sin punteros
(let ((*gc-inhibit* t)) ...)                ; en algunas implementaciones
(sb-ext:gc :gen 2)                           ; forzar la recolección de una generación
```

Y para la frontera con C, donde **sí hay que liberar a mano**, el ecosistema tiene CFFI (clase 129):

```lisp
(cffi:with-foreign-object (p :int 100)     ; se libera al salir del bloque
  ...)
(cffi:foreign-alloc :int :count 100)         ; y esto hay que foreign-free
```

**`with-foreign-object` es la macro que ata la liberación al ámbito** — la misma forma que
`with-open-file` (clase 103) y que todas las soluciones del cierre de esta clase.

Y es un ejemplo de lo que se dijo en la clase 107: **en Lisp, la solución a un problema del lenguaje es
una macro**. `unwind-protect` más una macro `with-` cubre cualquier recurso, y escribirla son diez
líneas.

Merece cerrar con una observación histórica: **las máquinas Lisp de los ochenta tenían recolección de
basura asistida por hardware**, con barreras de escritura implementadas en silicio. Cuando esas
máquinas desaparecieron, las técnicas pasaron al software — y hoy están en la JVM, en .NET y en Go.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea
set n [string trim $linea]

set v {}
set suma 0
for {set i 1} {$i <= $n} {incr i} {
    lappend v $i
    incr suma $i
}

# no hay que liberar: conteo de referencias sobre valores inmutables
puts "reservado=$n suma=$suma"
```

**Lo que esta clase enseña en Tcl.** **En Tcl puro no existe la gestión manual de memoria**: el conteo
de referencias sobre valores inmutables (clase 128) libera todo automáticamente y sin ciclos posibles.

Donde sí existe —y es donde Tcl tiene sus fugas reales— es **en las extensiones escritas en C**:

```c
Tcl_Obj *obj = Tcl_NewIntObj(42);
Tcl_IncrRefCount(obj);     /* incrementar el contador */
...
Tcl_DecrRefCount(obj);      /* y decrementarlo: si llega a 0, se libera */
```

**Toda la API de C de Tcl gira alrededor de `Tcl_IncrRefCount` y `Tcl_DecrRefCount`**, y equivocarse
produce las dos caras del problema: **decrementar de más libera algo que todavía se usa; decrementar de
menos es una fuga**.

Y Tcl tiene reglas explícitas sobre quién posee qué —los objetos con contador cero son "frescos" y los
puede tomar quien los reciba— que están documentadas precisamente porque son la fuente de errores más
común al extender el lenguaje.

Para diagnosticarlo, Tcl se puede compilar con instrumentación (clase 128):

```tcl
memory info
memory active fugas.txt      ;# los bloques VIVOS, con fichero y línea de C
memory trace on
```

Y para los recursos que no son memoria —canales, ventanas, objetos— Tcl usa lo del cierre de esta
clase: **atar la liberación a algo que ocurre siempre**.

```tcl
try { ... } finally { close $canal }            ;# Tcl 8.6
trace add variable v unset { ... }               ;# al desaparecer la variable
oo::class create R { destructor { ... } }         ;# destructor de objeto
interp alias / interp delete                       ;# al morir el intérprete
```

**`trace add variable ... unset`** es la más peculiar: **engancha código a la desaparición de una
variable**, incluida la salida del procedimiento. Con eso se construye un destructor sin que el
lenguaje tenga destructores (clase 103).

Y hay un mecanismo de región muy propio de Tcl: **crear un intérprete secundario y destruirlo**.

```tcl
set i [interp create]
$i eval { ... }              ;# todo lo que cree vive AHÍ
interp delete $i              ;# y desaparece de golpe
```

Es un *arena allocator* a escala de intérprete, y se usa para ejecutar código no confiable con límites
(clase 153).

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;
use List::Util qw(sum0);

my $n = <STDIN>;
chomp $n;

my @v = (1 .. $n);
my $suma = sum0(@v);

# no hay que liberar: conteo de referencias
print "reservado=$n suma=$suma\n";
```

**Lo que esta clase enseña en Perl.** Perl libera por **conteo de referencias**, y eso da la propiedad
que las clases 103 y 128 destacaban: **liberación determinista**, en el momento exacto en que la
última referencia desaparece.

Por eso `DESTROY` en Perl sirve para cerrar ficheros y soltar bloqueos, cosa que con un recolector de
basura sería un error de diseño.

Y por eso Perl **sí tiene un problema de gestión manual**: **los ciclos**.

```perl
my $a = {};
$a->{yo} = $a;          # ciclo: NUNCA se libera
```

La solución es explícita y hay que acordarse de ella:

```perl
use Scalar::Util qw(weaken);
$hijo->{padre} = $nodo;
weaken($hijo->{padre});      # no cuenta para el contador
```

**Cualquier estructura con enlaces al padre —árboles, grafos, observadores— necesita `weaken`**, y
olvidarlo es la fuga clásica de Perl.

Y las herramientas para encontrarla son de las mejores de esta página (clase 128):

```perl
use Devel::Cycle;  find_cycle($estructura);     # ENCONTRAR el ciclo
use Devel::Leak;                                  # contar SVs vivos
use Test::Memory::Cycle;  memory_cycle_ok($obj);   # como PRUEBA automática
```

**`Test::Memory::Cycle` convierte la ausencia de ciclos en una prueba unitaria** — es la forma correcta
de atacar el problema: **no confiar en la disciplina, comprobarlo en CI**.

Y para la frontera con C, donde Perl sí gestiona a mano, están `XS` y `Inline::C` (clase 126), con las
macros de gestión de referencias `SvREFCNT_inc` y `SvREFCNT_dec` — el mismo modelo que Tcl de esta
clase, y con los mismos errores posibles.

Es un patrón que esta clase deja claro: **los lenguajes con conteo de referencias tienen dos zonas —el
código propio, donde no hay que hacer nada, y la extensión en C, donde hay que hacerlo todo**.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>
#include <memory>

int main() {
    int n{};
    if (!(std::cin >> n)) return 1;

    //  reserva dinámica SIN delete: unique_ptr libera al salir
    auto v = std::make_unique<int[]>(n);

    long long suma = 0;
    for (int i = 0; i < n; ++i) {
        v[i] = i + 1;
        suma += i + 1;
    }

    std::cout << "reservado=" << n << " suma=" << suma << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** El programa reserva en el montón y **no tiene `delete`**, y esa es
toda la lección: **en C++ moderno, escribir `delete` a mano es la señal de que algo está mal**.

La progresión histórica es la de esta clase entera:

```cpp
int* v = new int[n];  ...  delete[] v;      // 1985: a mano, con todos los riesgos
std::vector<int> v(n);                        // 1998: el contenedor libera
auto v = std::make_unique<int[]>(n);           // 2014: propiedad única explícita
```

Y el problema del cierre —**los caminos que no pasan por el `delete`**— es especialmente grave en C++
por una razón concreta: **las excepciones**.

```cpp
int* v = new int[n];
procesar(v);              // si esto LANZA...
delete[] v;                // ...esto no se ejecuta: FUGA
```

**Ese fue el problema que motivó RAII** (clase 103): con excepciones, cualquier línea puede ser una
salida, y un `delete` al final no basta.

Los tres errores clásicos de la gestión manual, y qué los elimina:

| Error | Qué pasa | Qué lo elimina |
|---|---|---|
| Fuga | la memoria no se devuelve | RAII, contenedores |
| Doble liberación | corrupción del montón | propiedad única |
| Uso tras liberar | lectura de basura o peor | propiedad y tiempos de vida |

Y las herramientas que los detectan son las de la clase 128, con una nota sobre cuál usar:

```bash
valgrind --leak-check=full        # completo y LENTO (10-50x)
g++ -fsanitize=address             # rápido (2x), detecta también use-after-free
g++ -fsanitize=leak                 # solo fugas, muy barato
```

**AddressSanitizer es hoy la herramienta por defecto**, y debería estar activada en la compilación de
las pruebas de cualquier proyecto en C++.

Y hay una advertencia sobre `new[]` y `delete[]` que esta clase debe dejar: **hay que emparejarlos
correctamente**.

```cpp
int* p = new int[10];
delete p;              // ¡MAL! comportamiento indefinido: falta []
```

Es un error que no da síntomas inmediatos y que corrompe el montón. Con `make_unique<int[]>` no puede
ocurrir, porque el tipo lleva la información.

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

dcl-pi MANUAL;
  n int(10) const;
end-pi;

dcl-s p     pointer;
dcl-s v     int(10) dim(1000) based(p);
dcl-s i     int(10);
dcl-s suma  int(20) inz(0);

p = %alloc(n * 4);                 // RESERVAR

for i = 1 to n;
  v(i) = i;
  suma += i;
endfor;

dsply ('reservado=' + %char(n) + ' suma=' + %char(suma));

dealloc p;                          // LIBERAR
p = *null;

*inlr = *on;
return;
```

**Lo que esta clase enseña en RPG.** RPG tiene `%alloc` y `dealloc`, y la plataforma tiene la respuesta
de la clase 128 que hace que las fugas importen poco: **los grupos de activación**.

```text
RCLACTGRP ACTGRP(MIAPP)      -- libera TODO lo del grupo
```

Y ahí está el punto que conecta con COBOL y CICS de esta misma clase: **la unidad de trabajo tiene un
final, y ese final limpia**.

Además, RPG tiene una construcción específica para el problema del cierre —los caminos que no pasan por
la liberación—:

```rpgle
monitor;
  p = %alloc(1000);
  procesar(p);
on-error;
  // manejar el error
endmon;
dealloc(n) p;        // el (n) permite liberar aunque p sea nulo
```

**`monitor`/`on-error`/`endmon` es el `try`/`catch` de RPG** (llegó con V5R1), y `dealloc(n)` con el
operando extendido **no falla si el puntero es nulo** — es el `Free` de Delphi de esta misma clase.

Y hay tres capacidades de la plataforma que conviene nombrar porque cubren lo que el lenguaje no:

**Primera: `%realloc` conserva el contenido.**

```rpgle
p = %realloc(p : nuevo_tamano);
```

Con la trampa clásica de C: **si falla, el puntero original se pierde**. La forma segura es usar una
variable temporal.

**Segunda: la memoria de un grupo de activación se puede consultar.**

```text
DSPJOB -> opción 16: almacenamiento asignado por grupo de activación
```

**Ver cuánta memoria ha reservado cada grupo, desde fuera y sin detener el trabajo.** Es la
observabilidad de la clase 142, aplicada a la memoria.

**Y tercera: los espacios de usuario** (clase 128), que son objetos del sistema con nombre, persistentes
y de hasta 16 MB — memoria que **sobrevive al trabajo que la creó** y que hay que borrar con
`DLTUSRSPC`.

Ahí sí hay una fuga posible de verdad, y es de las pocas que un sistema IBM i puede acumular: **objetos
temporales que nadie borra**. La herramienta para encontrarlos es una consulta SQL sobre
`QSYS2.OBJECT_STATISTICS` (clase 117).

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 manual: procedure options(main);

    declare n fixed binary(31);
    declare i fixed binary(31);
    declare suma fixed binary(31) initial(0);
    declare p pointer;
    declare v(1000) fixed binary(31) based(p);

    get list (n);

    allocate v set(p);                  /* RESERVAR */

    do i = 1 to n;
       v(i) = i;
       suma = suma + i;
    end;

    put skip list ('reservado=' || trim(char(n)) ||
                   ' suma=' || trim(char(suma)));

    free v;                              /* LIBERAR */

 end manual;
```

**Lo que esta clase enseña en PL/I.** PL/I inventó `allocate` y `free` en 1964 (clases 128 y 129), y con
ellos **inventó también los problemas**: la fuga, la doble liberación y el uso tras liberar existen
desde entonces.

Y PL/I tiene **cuatro clases de almacenamiento** (clase 127), que son cuatro respuestas distintas a
esta clase:

| Clase | Quién libera |
|---|---|
| `static` | nadie: existe siempre |
| `automatic` | **el ámbito**, al salir |
| `controlled` | el programador, con `free` — y es una **pila** |
| `based` | el programador, con `free` |

**`controlled` es el caso interesante**, ya visto en la clase 090: cada `allocate` apila una generación
y cada `free` desapila. Eso hace que la liberación sea **más fácil de emparejar** —es una pila, no un
grafo— y `allocation(x)` dice cuántas generaciones quedan.

Y PL/I tiene la mejor respuesta de esta página al problema del cierre, ya nombrada en la clase 128:
**las áreas**.

```pli
 declare mi_area area(100000);
 allocate nodo in(mi_area) set(p);
 ...
 free mi_area;              /* libera TODO lo de dentro, de golpe */
```

**Liberar el área libera todo lo reservado dentro**, sin recorrer ni emparejar nada. Es un *arena
allocator* con sintaxis del lenguaje, en 1964, y es exactamente lo que hoy se recomienda para
estructuras con muchos objetos pequeños de vida común.

Y PL/I añade el manejo de condiciones para los fallos de reserva (clases 103 y 116):

```pli
 on condition(storage) begin;
    put list('sin memoria: liberando cachés');
    call liberar_caches();
    /* y se puede REANUDAR, reintentando la reserva */
 end;
```

**Un manejador de "sin memoria" que puede liberar cachés y reanudar** es algo que ni C, ni C++, ni Java
ofrecen de forma directa — en Java, `OutOfMemoryError` llega cuando ya casi no se puede hacer nada.

Es una capacidad que viene de que las condiciones de PL/I **no desenrollan la pila** (clase 116), y es
otro caso de una buena idea que no se difundió.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
MANUAL ; Gestion manual de memoria -- clase 130
 read n
 kill v
 set suma = 0
 for i=1:1:n set v(i) = i, suma = suma + i
 write "reservado=", n, " suma=", suma, !
 kill v                              ; liberar: borrar el arbol
 quit
```

**Lo que esta clase enseña en M.** **En M no hay gestión manual de memoria en el sentido de esta
clase**: no hay reserva, así que no hay `free` que olvidar (clase 128).

Lo que hay es `kill`, que **borra un nombre y todo su subárbol**:

```mumps
 kill v              ; borra v y TODOS sus subíndices
 kill v(3)            ; solo esa rama
 kill (a, b)           ; TODO menos a y b -- el kill exclusivo
 kill ^DATOS            ; un global entero, en DISCO
```

Y ahí está la particularidad de M en esta clase: **`kill` sobre un *global* no libera memoria, libera
espacio de base de datos**, y eso tiene consecuencias que la memoria no tiene:

- **Es transaccional**: dentro de `tstart`/`tcommit`, se puede deshacer.
- **Es persistente**: lo borrado sigue borrado mañana.
- **Y el espacio no siempre vuelve al sistema operativo**: los bloques quedan libres dentro del fichero
  de base de datos, que **no encoge**.

Ese último punto es el equivalente de la fragmentación del montón, a escala de disco, y las
implementaciones tienen herramientas para ello —la reorganización de la base de datos en YottaDB e
IRIS— que son el equivalente de un compactador.

Y hay una fuga que sí existe en M y que es específica de su modelo: **las variables locales que nadie
mata**.

```mumps
 set temporal(i) = ...       ; sin `new` y sin `kill`
```

Como las variables locales son globales al proceso (clase 082), **una rutina que crea un array temporal
grande y no lo borra lo deja en memoria durante toda la sesión**. En un proceso de servidor que atiende
peticiones sin reiniciarse, eso se acumula.

De ahí que el idioma disciplinado de M sea **`new` al entrar o `kill` al salir**, y que el `kill`
exclusivo —`kill (a, b)`— exista precisamente para limpiar el espacio de nombres de golpe.

Es la misma forma que todas las soluciones del cierre de esta clase: **atar la limpieza a algo que
ocurre siempre**, y en M ese algo es el `quit` de la rutina con su `new`.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| n v suma |

n := stdin nextLine trimBoth asNumber.

v := OrderedCollection new.
suma := 0.
1 to: n do: [ :i | v add: i. suma := suma + i ].

"no hay que liberar: recolector de basura desde 1980"
Transcript
    show: 'reservado=', n printString;
    show: ' suma=', suma printString;
    cr.
```

**Lo que esta clase enseña en Smalltalk.** **En Smalltalk no hay gestión manual de memoria en
absoluto**: no existe `free`, no existe `delete` y no hay forma de liberar un objeto a mano.

Y esa ausencia es más radical que en Lisp o en Java, por lo que se explicó en la clase 129: **el sistema
puede mover los objetos** porque nadie guarda direcciones. Un recolector que compacta y `become:` solo
son posibles con esa garantía.

Lo que sí existe, y es la fuga que Smalltalk puede tener, es **la referencia olvidada**:

```smalltalk
| cache |
cache := Dictionary new.
cache at: clave put: objetoEnorme.        "y nadie lo quita"
```

Mientras algo lo referencie, el objeto vive. Y aquí está la particularidad del modelo de imagen (clase
041) que la clase 128 ya adelantaba: **la fuga sobrevive a la sesión**. Un objeto olvidado sigue en la
imagen mañana, y la imagen crece.

Por eso Smalltalk tiene las herramientas de diagnóstico más directas de esta página:

```smalltalk
MiClase allInstances size.            "¿cuántas hay vivas?"
objeto chasePointers.                  "¿QUIÉN me está reteniendo?"
Smalltalk garbageCollect.
SystemNavigation default allObjects size.
```

**`chasePointers` responde exactamente a la pregunta que se hace ante una fuga**, y en un mensaje. En
Java eso exige un volcado del montón y una herramienta de análisis; aquí abre un inspector.

Y para las cachés, Smalltalk tiene lo que hace falta:

```smalltalk
WeakArray with: objeto.               "referencia DÉBIL: no impide la recolección"
WeakKeyDictionary new.                 "cachés que no retienen (clase 095)"
objeto finalizationRegistry.
```

**`WeakKeyDictionary`** es la solución idiomática al problema de la caché que crece para siempre: **si
nadie más usa la clave, la entrada desaparece sola**.

Y hay un detalle histórico que cierra esta clase: **Smalltalk y Lisp fueron los dos sistemas donde se
desarrolló la recolección generacional**, y la razón fue la misma: **crean muchísimos objetos pequeños
y efímeros**.

La hipótesis de que "la mayoría de los objetos mueren jóvenes" se midió en programas Smalltalk, y de
ahí salieron los recolectores de Java, .NET y Go.

---

## Y de vuelta a la clase

Lo transferible: **liberar a mano no falla por descuido, falla por caminos**. El `free` está escrito, y
hay un `return` anticipado, una excepción o una rama de error que no pasa por ahí. Por eso todas las
soluciones que funcionan —RAII, `defer`, `with`, ámbitos, regiones— tienen la misma forma: **atar la
liberación a algo que ocurre siempre**. Si te descubres escribiendo `free` en tres sitios distintos de
la misma función, ese es el síntoma.

⏮️ [Volver a la clase 130](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
