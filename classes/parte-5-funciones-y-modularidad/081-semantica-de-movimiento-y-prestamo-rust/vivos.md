# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 081

> [⬅️ Volver a la clase 081](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Una palabra, su longitud, y la pregunta que Rust puso en el centro de la conversación en la última
década: **¿quién es el dueño de este dato y cuándo se libera?** La respuesta de Rust —propiedad,
movimiento y préstamo comprobados por el compilador— parece nueva. Y sin embargo **Fortran tiene una
operación de movimiento desde 2003** y **C++ construyó la suya en 2011**.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es la **propiedad de un recurso**, y estos lenguajes lo enseñan porque muestran las
> tres estrategias históricas. **Gestión manual**: C++ antes de 2011, donde copiar era la única forma
> segura y el rendimiento se pagaba en copias. **Recolección de basura**: Lisp, Smalltalk, Tcl, Perl y
> M, donde la pregunta desaparece a cambio de pausas impredecibles. Y **conteo de referencias con copia
> al escribir**: Pascal, Tcl y Perl, donde el dato se comparte hasta que alguien lo toca.
>
> Y hay dos hallazgos concretos: **`move_alloc` de Fortran 2003 es literalmente un movimiento**, y
> **Ada tiene tipos controlados** con `Adjust` y `Finalize`, que son los constructores de copia y
> destructores de C++ con otro nombre.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: una palabra (ASCII) → stdout: `movido=<palabra> longitud=<len>`
- **Regla:** `longitud por préstamo; el texto se muestra tras moverse`

| stdin | esperado |
|---|---|
| `Ada` | `movido=Ada longitud=3` |
| `Bo` | `movido=Bo longitud=2` |
| `hola` | `movido=hola longitud=4` |

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
PROGRAM-ID. MOVIDO.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA     PIC X(80).
01  PALABRA   PIC X(80).
01  LARGO     PIC 9(4) COMP-3.
01  ED-L      PIC Z(3)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    MOVE FUNCTION TRIM(LINEA) TO PALABRA
    COMPUTE LARGO = FUNCTION LENGTH(FUNCTION TRIM(PALABRA))

    MOVE LARGO TO ED-L
    DISPLAY "movido=" FUNCTION TRIM(PALABRA)
            " longitud=" FUNCTION TRIM(ED-L)
    STOP RUN.
```

**Lo que esta clase enseña en COBOL.** **En COBOL clásico la pregunta de esta clase no existe, porque
no hay memoria dinámica.** Todo el `WORKING-STORAGE` se reserva al cargar el programa y se libera al
terminar. No hay `new`, no hay `free`, no hay punteros colgantes y **no hay fugas**.

Esa es una propiedad notable de la que se habla poco: **un programa COBOL de 1980 no puede tener una
fuga de memoria**. Tampoco puede tener corrupción del montículo, ni doble liberación, ni referencia a
memoria liberada. La clase entera de errores que Rust vino a eliminar **es imposible por
construcción**.

El precio es la rigidez: el tamaño máximo de cada tabla se decide al compilar, y si mañana hay más
clientes de los previstos hay que recompilar.

COBOL sí añadió memoria dinámica cuando hizo falta, y su vocabulario delata la época:

```cobol
ALLOCATE 1000 CHARACTERS RETURNING PUNTERO
SET DIRECCION OF REGISTRO TO PUNTERO
FREE PUNTERO
```

`ALLOCATE` y `FREE` (COBOL 2002) son `malloc` y `free`, con los mismos riesgos. Se usan sobre todo
para hablar con servicios del sistema y con programas C, no en la lógica de negocio.

Y `MOVE`, a pesar de su nombre, **no es un movimiento en el sentido de esta clase**: es una copia. El
origen queda intacto. Es una coincidencia de vocabulario que conviene no confundir.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program movido
   implicit none
   character(len=:), allocatable :: palabra, destino
   character(len=200) :: buf

   read(*, '(A)') buf
   palabra = trim(buf)

   !  move_alloc: TRANSFIERE la asignación. `palabra` queda DESASIGNADA.
   call move_alloc(palabra, destino)

   write(*, '(A,A,A,I0)') 'movido=', destino, ' longitud=', len(destino)
end program movido
```

**Lo que esta clase enseña en Fortran.** **`move_alloc` es una operación de movimiento de verdad**, y
está en el estándar desde **Fortran 2003** — ocho años antes que la de C++ y doce antes de Rust.

```fortran
call move_alloc(origen, destino)
!  destino pasa a ser dueño de la memoria de origen
!  origen queda DESASIGNADO (allocated(origen) es .false.)
!  NO se copia ni un byte
```

Es exactamente `std::move` seguido de dejar el origen vacío: **transferencia de propiedad, coste
constante, y el origen queda inutilizable**.

Y no se inventó por elegancia: se inventó porque en cálculo científico **los arrays son enormes**.
Redimensionar un array de diez gigabytes copiando sería imposible; con `move_alloc` se reserva el
nuevo, se copia lo necesario y se transfiere la propiedad en una operación de coste cero:

```fortran
allocate(temporal(2 * n))
temporal(1:n) = v
call move_alloc(temporal, v)      ! v ahora es el grande; temporal, nada
```

Ese es el idioma para hacer crecer un array en Fortran, y es literalmente cómo está implementado
`std::vector` por dentro.

La diferencia con Rust es que **Fortran no lo comprueba**: usar `palabra` después del `move_alloc` es
un error en ejecución, no de compilación. El compilador puede avisar con `-fcheck=all`, pero la
garantía la pone el programador. Rust puso esa misma operación en el sistema de tipos, y esa es toda
la diferencia.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;           use Ada.Text_IO;
with Ada.Integer_Text_IO;   use Ada.Integer_Text_IO;
with Ada.Strings.Unbounded; use Ada.Strings.Unbounded;

procedure Movido is
   Buf      : String (1 .. 200);
   Ultimo   : Natural;
   Palabra  : Unbounded_String;
begin
   Get_Line (Buf, Ultimo);
   Palabra := To_Unbounded_String (Buf (1 .. Ultimo));

   Put ("movido=" & To_String (Palabra) & " longitud=");
   Put (Length (Palabra), Width => 1);
   New_Line;
end Movido;
```

**Lo que esta clase enseña en Ada.** `Unbounded_String` gestiona su propia memoria, y lo hace con un
mecanismo que Ada 95 introdujo y que es **el equivalente exacto de los constructores y destructores
de C++**: los **tipos controlados**.

```ada
type Recurso is new Ada.Finalization.Controlled with record
   Datos : Acceso_Array;
end record;

overriding procedure Initialize (R : in out Recurso);   --  constructor
overriding procedure Adjust     (R : in out Recurso);   --  tras COPIAR
overriding procedure Finalize   (R : in out Recurso);   --  destructor
```

Un tipo que hereda de `Controlled` recibe esas tres llamadas **automáticamente**: al crearse, después
de cada asignación, y al salir del ámbito. Con ellas se implementa RAII completo, conteo de
referencias, copia profunda o lo que haga falta.

`Finalize` **se ejecuta siempre**, incluso si una excepción desenrolla la pila — la garantía que en
C++ dan los destructores y que Java tuvo que suplir con `try-with-resources`.

Lo que Ada **no** tiene en el estándar es la semántica de movimiento: `Adjust` siempre copia. Para
transferir sin copiar hay que implementarlo a mano con punteros y una bandera de propiedad.

Y para el mundo crítico hay una respuesta más radical, la de la ficha de COBOL: **en aviónica la
memoria dinámica se prohíbe**. Sin `new`, no hay propiedad que gestionar, y el consumo de memoria del
programa es analizable antes de volar. SPARK va más lejos y tiene un sistema de **propiedad y préstamo
comprobado estáticamente**, muy parecido al de Rust, añadido en 2019.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Movido;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  Palabra, Destino: string;

begin
  ReadLn(Palabra);
  Palabra := Trim(Palabra);

  Destino := Palabra;      { NO copia el texto: comparte y suma 1 al contador }

  WriteLn('movido=', Destino, ' longitud=', IntToStr(Length(Destino)));
end.
```

**Lo que esta clase enseña en Pascal.** `Destino := Palabra` **no copia el texto**. Copia un puntero e
incrementa un contador de referencias. La copia real solo ocurre si alguno de los dos se modifica —la
**copia al escribir** de la clase 048.

Ese modelo, que Delphi introdujo en 1996 con `AnsiString`, resuelve el problema de esta clase de una
tercera manera: **ni gestión manual ni recolector, sino conteo de referencias con copia diferida**.

```pascal
A := 'texto largo';
B := A;              { contador = 2, un solo texto en memoria }
B := B + '!';        { AHORA se copia, porque hay dos dueños }
```

Las propiedades son buenas: liberación **determinista** (cuando el contador llega a cero, se libera al
instante, sin esperar a un recolector), semántica de valor, y coste de copia solo cuando hace falta.

Y las limitaciones también son conocidas: **los ciclos no se liberan nunca** —dos objetos que se
apuntan mutuamente mantienen el contador en 1— y el conteo tiene un coste en cada asignación, que en
código multihilo exige operaciones atómicas.

Es el mismo modelo que usan PHP, Swift y los `shared_ptr` de C++, con los mismos compromisos. Swift
resolvió el problema de los ciclos obligando a declarar referencias `weak`; Delphi no, y las fugas por
ciclos entre interfaces son un problema real de sus aplicaciones grandes.

Para los **objetos** (`TObject`), Object Pascal no cuenta referencias: hay que llamar a `Free`, con el
`try..finally` de la clase 071.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let ((palabra (string-trim '(#\Space #\Tab #\Return) (read-line))))
  (format t "movido=~A longitud=~D~%" palabra (length palabra)))
```

**Lo que esta clase enseña en Common Lisp.** **En Lisp la pregunta de esta clase no se plantea: hay un
recolector de basura**, y de hecho **Lisp es donde se inventó**, en 1959, para este mismo problema.

McCarthy necesitaba manipular estructuras de listas que se creaban y descartaban continuamente, y
llevar la cuenta a mano era inviable. La solución —recorrer periódicamente lo alcanzable y liberar el
resto— es el primer recolector de la historia, y de ahí viene el nombre *garbage collection*.

Los recolectores modernos de Lisp son generacionales y con compactación: SBCL usa uno que separa los
objetos jóvenes de los viejos, porque la observación empírica es que **la mayoría de los objetos
mueren jóvenes**. Es el mismo diseño que la JVM y el CLR.

Y hay un matiz de esta clase que Lisp sí hace explícito: **la diferencia entre compartir y copiar**.

```lisp
(setf b a)              ; b y a apuntan al MISMO objeto
(setf b (copy-seq a))   ; una copia SUPERFICIAL
(setf b (copy-tree a))  ; una copia PROFUNDA, recursiva
```

Tener las tres con nombres distintos evita la ambigüedad de "¿esto copia?" que en otros lenguajes hay
que averiguar leyendo la documentación.

Lo que un recolector no elimina son las **fugas lógicas**: una estructura global que sigue apuntando a
datos que ya no se necesitan. El recolector no puede saber que ya no te interesan. Es la fuga que sí
existe en Java, Lisp y Smalltalk, y la más difícil de encontrar.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea
set palabra [string trim $linea]
set destino $palabra          ;# comparte la representación; NO copia

puts "movido=$destino longitud=[string length $destino]"
```

**Lo que esta clase enseña en Tcl.** Tcl usa **conteo de referencias con copia al escribir**, como
Pascal, y lo aplica a **todos los valores**, no solo a las cadenas.

Cada valor de Tcl es un objeto interno (`Tcl_Obj`) con un contador. `set destino $palabra` incrementa
el contador; nada se copia. Y cuando alguien modifica uno de los dos, Tcl comprueba el contador: si es
1, **modifica en el sitio**; si es mayor, copia primero.

Ese mecanismo es lo que hace correctas las optimizaciones de la clase 054:

```tcl
append sec "-$i"       ;# contador 1: modifica en el sitio, LINEAL
lappend lista $x       ;# igual
set b $a               ;# ahora el contador es 2...
append a "x"           ;# ...y ESTO sí copia
```

El programador ve siempre **semántica de valor pura** —nadie te cambia un dato por detrás— con el
rendimiento de la referencia mientras nadie escriba.

Y Tcl tiene el mismo problema de ciclos que Pascal, con una diferencia: **como los valores son
inmutables desde fuera, no se pueden formar ciclos entre ellos**. Un valor no puede contenerse a sí
mismo. Los ciclos solo aparecen entre estructuras de C registradas por extensiones, y por eso Tcl no
necesita un recolector de ciclos.

Es un ejemplo interesante de cómo una decisión de diseño —valores inmutables— elimina de raíz el
problema que obligó a Swift a inventar `weak`.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;
my $palabra = $linea;

print "movido=$palabra longitud=", length($palabra), "\n";
```

**Lo que esta clase enseña en Perl.** Perl usa **conteo de referencias puro**, sin recolector de
ciclos, y esa decisión tiene una consecuencia que hay que conocer: **las estructuras circulares no se
liberan nunca**.

```perl
my $a = {};
my $b = { otro => $a };
$a->{otro} = $b;        # ciclo: NUNCA se liberan, ni al salir del ámbito
```

La solución de Perl son las **referencias débiles** de `Scalar::Util`:

```perl
use Scalar::Util qw(weaken);
$a->{padre} = $b;
weaken($a->{padre});    # no cuenta para el contador
```

Es el mismo `weak` de Swift y el mismo `weak_ptr` de C++, y por el mismo motivo.

A cambio, el conteo de referencias da algo que un recolector no da: **destrucción determinista**. Un
objeto se destruye **en el instante** en que su última referencia desaparece, así que el método
`DESTROY` se ejecuta cuando toca:

```perl
{
    my $f = Fichero->new('datos.txt');
    ...
}   # aquí, exactamente aquí, se cierra el fichero
```

Ese es el RAII de C++ obtenido con conteo de referencias, y es la razón de que Perl no necesite un
`finally` para cerrar recursos — igual que Python, que usa el mismo modelo.

Java y Lisp, con recolector generacional, **no** lo tienen: el finalizador se ejecuta cuando el
recolector pasa, que puede ser nunca. De ahí `try-with-resources` y `with`.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>
#include <string>
#include <utility>

int main() {
    std::string linea;
    if (!std::getline(std::cin, linea)) return 1;

    //  std::move NO mueve nada: convierte a referencia rvalue, y eso permite
    //  al constructor de destino ROBAR el búfer en vez de copiarlo.
    std::string destino = std::move(linea);

    std::cout << "movido=" << destino
              << " longitud=" << destino.size() << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** **`std::move` no mueve nada.** Es una conversión de tipo: convierte
su argumento en una **referencia rvalue** (`T&&`), y eso hace que la sobrecarga elegida sea el
constructor de movimiento en lugar del de copia.

```cpp
std::string b = a;              // COPIA: reserva memoria y copia los bytes
std::string b = std::move(a);   // MUEVE: roba el puntero interno de a
```

Tras el movimiento, `a` queda en un estado **válido pero no especificado**: se puede asignar y
destruir, y no se debe leer su valor. Es exactamente lo que hace `move_alloc` en Fortran, con dos
diferencias: aquí lo implementa cada clase, y **el compilador no impide usar el origen después**.

Ahí está la diferencia con Rust, y es toda la diferencia: Rust puso esta operación en el **sistema de
tipos**, así que usar el origen después **no compila**. C++ la puso en la biblioteca, y usarlo es un
error en ejecución que nadie detecta.

La semántica de movimiento (C++11) fue el cambio más importante del lenguaje moderno, porque resolvió
un problema que tenía treinta años: **devolver un objeto grande de una función**. Antes había que
devolver punteros o pasar parámetros de salida; desde C++11, `return v;` no copia nada.

Y `std::unique_ptr` es la propiedad hecha tipo: **no se puede copiar, solo mover**, así que el
compilador garantiza que hay exactamente un dueño. Es lo más cerca que llega C++ al modelo de Rust, y
llegó cuatro años antes.

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

dcl-pi MOVIDO;
  palabra varchar(100) const;
end-pi;

dcl-s destino varchar(100);
dcl-s salida  char(150);

destino = palabra;      // copia: RPG no tiene movimiento ni referencias

salida = 'movido=' + destino + ' longitud=' + %char(%len(destino));
dsply salida;

*inlr = *on;
return;
```

**Lo que esta clase enseña en RPG.** Como COBOL, **RPG evita el problema no teniendo memoria dinámica**
en el código de negocio: las variables se dimensionan al compilar y viven en el almacenamiento
automático o estático de la clase 069.

Un programa RPG típico **no puede tener fugas**, y esa propiedad es parte de por qué las aplicaciones
de IBM i llevan décadas ejecutándose sin reiniciar.

RPG sí tiene memoria dinámica cuando hace falta, con el vocabulario de C:

```rpgle
dcl-s p pointer;
dcl-s buffer char(65535) based(p);

p = %alloc(1000);          // malloc
...
dealloc p;                 // free
p = *null;
```

`%alloc`, `%realloc` y `dealloc` son literalmente `malloc`, `realloc` y `free`, con los mismos
riesgos: fugas, doble liberación y punteros colgantes. Se usan para hablar con las APIs del sistema y
para manejar datos de tamaño imprevisible, no en la lógica de negocio.

Y hay una propiedad de la plataforma que cambia el panorama: en IBM i, **la memoria dinámica de un
programa se libera automáticamente al terminar su grupo de activación**. Aunque un programa tenga
fugas, al cerrar el trabajo desaparecen. Es una red de seguridad a nivel de sistema operativo que
pocos entornos ofrecen, y que explica que el asunto se vigile menos que en C.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 movido: procedure options(main);

    declare palabra character(200) varying;
    declare destino character(200) varying;

    get edit (palabra) (a(200));
    palabra = trim(palabra);

    destino = palabra;      /* copia: PL/I no tiene semántica de movimiento */

    put skip list ('movido=' || destino ||
                   ' longitud=' || trim(char(length(destino))));

 end movido;
```

**Lo que esta clase enseña en PL/I.** PL/I **sí tiene memoria dinámica**, y con más formas que casi
cualquier lenguaje de esta página, gracias a las cuatro clases de almacenamiento de la clase 042:

```pli
declare v(1000) fixed binary(31) controlled;

allocate v;        /* APILA una instancia nueva */
allocate v;        /* otra encima: la anterior sigue viva, oculta */
free v;            /* desapila la última */
```

`controlled` mantiene **una pila de asignaciones** de la misma variable, y `allocation(v)` dice
cuántas hay. Es un mecanismo que no tiene equivalente en ningún lenguaje moderno, y que se usaba para
implementar recursión antes de que fuera barata, y para guardar contexto en manejadores de error.

Y `based` con `allocate ... set(p)` es el `malloc` clásico, con todos los riesgos.

Lo que PL/I **no** tiene es ninguna forma de gestión automática: ni recolector, ni conteo de
referencias, ni destructores. **Cada `allocate` necesita su `free`**, y no hay nada que lo compruebe.

Es coherente con su época —1964, antes de que el recolector de Lisp se considerara viable para
lenguajes de propósito general— y es una de las razones de que los programas PL/I grandes tuvieran
fama de fugar memoria.

La comparación con COBOL es instructiva: COBOL evitó el problema **no dando la herramienta**, y PL/I lo
creó **dándola sin barandillas**. Las dos decisiones se pueden defender, y la segunda es la que la
industria repitió con C.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
MOVIDO ; Movimiento y prestamo -- clase 081
 read palabra
 set destino = palabra
 write "movido=", destino, " longitud=", $length(destino), !
 quit
```

**Lo que esta clase enseña en M.** M gestiona la memoria automáticamente y la pregunta de esta clase
no aparece — pero por un motivo distinto del de Lisp, y es el más interesante de la página: **en M el
dato importante no está en memoria, está en disco**.

Una variable local vive lo que viva la rutina. Un ***global*** —`^PACIENTE`— **es persistente por
definición**, y su gestión no es un problema de memoria sino de base de datos: bloques, índices,
transacciones y recuperación ante fallos.

```mumps
 set ^PACIENTE(id) = datos      ; esto es una ESCRITURA EN DISCO
 kill ^PACIENTE(id)             ; y esto un BORRADO
```

`kill` sobre un global borra el nodo **y todos sus descendientes**, transaccionalmente. No hay
"liberar memoria": hay borrar datos.

Esa inversión —que el almacenamiento principal sea el disco y la memoria un detalle— es lo que hace
que M no tenga las categorías de esta clase. No hay propiedad que transferir porque el dato no es de
nadie: **está en la base de datos**.

Para las variables locales, `kill` las elimina y `new` de la clase 069 las restaura al salir. El
consumo de memoria de un proceso M está acotado por el tamaño de su tabla de símbolos locales, que las
implementaciones limitan explícitamente.

Es el mismo razonamiento que hace que un programa COBOL no tenga fugas, llevado un paso más allá: **si
todo lo que importa está en disco, la gestión de memoria deja de ser un problema de diseño del
lenguaje**.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| palabra destino |

palabra := stdin nextLine trimBoth.
destino := palabra.        "comparten el mismo objeto: no hay copia"

Transcript
    show: 'movido=', destino;
    show: ' longitud=', destino size printString;
    cr.
```

**Lo que esta clase enseña en Smalltalk.** `destino := palabra` **no copia nada**: las dos variables
apuntan al mismo objeto. En Smalltalk **toda variable es una referencia**, siempre, y el recolector se
encarga del resto.

Y Smalltalk tiene un mecanismo que casi ningún lenguaje ofrece y que encaja exactamente en esta
clase: **el objeto puede enterarse de que va a ser recolectado**.

```smalltalk
unObjeto finalizationRegistry add: unObjeto executor: unBloque
```

Los **finalizadores** de Pharo permiten ejecutar código cuando un objeto se vuelve inalcanzable —
cerrar un fichero, liberar un recurso del sistema operativo—. Es lo mismo que los `PhantomReference`
de Java y con la misma advertencia: **no está garantizado cuándo ocurre**, así que no sirve para
recursos escasos. Para eso está `ensure:` de la clase 071.

Y hay dos capacidades que solo tienen sentido en un sistema donde la memoria es un objeto más:

```smalltalk
unObjeto becomeForward: otro     "TODAS las referencias a unObjeto pasan a otro"
Smalltalk garbageCollect          "forzar una recolección"
unObjeto pointersTo               "¿QUIÉN me está apuntando?"
```

**`become:` intercambia la identidad de dos objetos en todo el sistema**, en una operación. Se usa
para migrar instancias cuando cambia una clase —el sistema está vivo y hay objetos existentes— y no
tiene equivalente en ningún otro lenguaje.

Y `pointersTo` responde a la pregunta más difícil de depurar en cualquier lenguaje con recolector:
**"¿por qué este objeto sigue vivo?"**. En Java hace falta un analizador de volcados de memoria; aquí
es un mensaje.

---

## Y de vuelta a la clase

Lo transferible: **"quién libera esto" es una pregunta que todo programa responde, explícita o
implícitamente**. Rust la puso en el sistema de tipos; C++ la puso en los destructores y la semántica
de movimiento; los lenguajes con recolector la delegaron en el runtime; y COBOL, RPG y Fortran clásico
la evitaron **no teniendo memoria dinámica**. Esa última opción, que parece primitiva, es la razón de
que un programa COBOL de 1980 no tenga fugas: **no hay nada que liberar**.

⏮️ [Volver a la clase 081](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
