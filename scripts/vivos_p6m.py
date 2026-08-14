# -*- coding: utf-8 -*-
"""Parte 6, lote M — clase 103. Ver `vivos_parte6.py` y `gen_vivos.py`."""

SPECS: dict[str, dict] = {}

# ---------------------------------------------------------------------------
# 103 — Propiedad y ciclo de vida de los datos
# ---------------------------------------------------------------------------
SPECS["103"] = dict(
    gancho="""
Un recurso que se crea, se usa y **se libera solo** al salir del ámbito. Es la idea que hizo posible
programar sin recolector de basura y sin fugas, y aquí hay una sorpresa de fechas: **Ada la tenía en
1983** con los tipos controlados, **C++ la bautizó RAII en 1994**, y **Fortran la incorporó en 2003**
con `final`. Los tres llegaron a la misma solución: **atar la liberación a la destrucción de una
variable de pila**.
""",
    porque="""
Aquí el concepto es la **propiedad y la liberación determinista**, y estos lenguajes la enseñan porque
enseñan las tres respuestas históricas. **Liberación automática atada al ámbito**: Ada con
`Finalization`, C++ con destructores, Fortran con `final`, Perl con `DESTROY` por conteo de
referencias. **Bloque de limpieza explícito**: Tcl con `try/finally`, Lisp con `unwind-protect`,
Pascal con `try/finally`. Y **nada**: COBOL, RPG, PL/I y M, donde la liberación es una línea que
alguien tiene que acordarse de escribir.

Y ese "nada" no es descuido: en esos lenguajes **casi no hay nada que liberar**, porque la memoria se
reserva al arrancar y los ficheros los cierra el sistema.
""",
    cierre="""
Lo transferible: **la pregunta correcta no es "¿cuándo se libera?" sino "¿quién es el dueño?"**. Un
recurso con un dueño claro se libera solo, en el punto exacto en que ese dueño muere. Un recurso sin
dueño se libera dos veces o ninguna. Esa es la idea que Ada escribió con `Controlled`, C++ con RAII y
Rust convirtió en el centro de su sistema de tipos con la propiedad y el préstamo de la clase 081. Y
el recolector de basura no la resuelve: gestiona la memoria y **no gestiona ficheros, conexiones ni
bloqueos**, que es por lo que Java necesitó `try-with-resources` y Python los gestores de contexto.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. CICLO.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  N       PIC S9(9) COMP-3.
01  ED-N    PIC -(8)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    COMPUTE N = FUNCTION NUMVAL(LINEA)

    PERFORM USAR-RECURSO
    PERFORM LIBERAR-RECURSO

    STOP RUN.

USAR-RECURSO.
    MOVE N TO ED-N
    DISPLAY "valor=" FUNCTION TRIM(ED-N) WITH NO ADVANCING.

LIBERAR-RECURSO.
    DISPLAY " estado=liberado".
""", """
**Lo que esta clase enseña en COBOL.** **COBOL no tiene destructores, ni ámbitos, ni liberación
automática**, y la limpieza es lo que se ve en este programa: **un párrafo que hay que acordarse de
llamar**.

Y sin embargo los sistemas COBOL casi no tienen fugas. La razón es que **casi no hay nada que
liberar**:

- La memoria se reserva **entera al arrancar** (clase 082): la `WORKING-STORAGE` es estática.
- Los ficheros se abren con `OPEN` y se cierran con `CLOSE`, y **el sistema los cierra igualmente** al
  terminar el programa.
- Los recursos caros —conexiones, bloqueos, transacciones— los gestiona **el monitor transaccional**,
  no el programa.

Ese último punto es el importante y define la arquitectura: **en CICS o IMS, la transacción es la
unidad de propiedad**. Si el programa falla, el monitor **deshace la transacción, libera los bloqueos
y devuelve los recursos**, sin que el programa lo pida. Es limpieza automática, implementada en la
plataforma en lugar del lenguaje.

Lo que COBOL sí tiene, y es lo más cercano a un bloque `finally`, son las **DECLARATIVES**:

```cobol
PROCEDURE DIVISION.
DECLARATIVES.
ERROR-FICHERO SECTION.
    USE AFTER STANDARD ERROR PROCEDURE ON CLIENTES.
MANEJAR.
    DISPLAY "error en CLIENTES: " FILE-STATUS-CLI.
END DECLARATIVES.
```

`USE AFTER STANDARD ERROR PROCEDURE` declara un manejador que el sistema invoca **automáticamente**
cuando falla una operación sobre ese fichero. Es un gancho declarativo de manejo de errores, en COBOL
desde 1968.

Y para la memoria dinámica, COBOL-2002 añadió lo esperable, con la responsabilidad esperable:

```cobol
ALLOCATE 1000 CHARACTERS RETURNING PTR
FREE PTR
```

Sin destructores y sin ámbito, así que **liberar es responsabilidad del programador**, exactamente
como en C. Es poco frecuente en producción, y esa rareza es lo que mantiene el historial de fugas
tan limpio.
"""),
        "fortran": ("""
module recursom
   implicit none

   type :: recurso
      integer :: valor = 0
   contains
      final :: liberar          ! FINALIZADOR: se llama al morir el objeto
   end type recurso

contains

   subroutine liberar(r)
      type(recurso), intent(inout) :: r
      write(*, '(A)') ' estado=liberado'
   end subroutine liberar

end module recursom


program ciclo
   use recursom
   implicit none
   integer :: n

   read(*, *) n

   block                         ! un ÁMBITO (Fortran 2008)
      type(recurso) :: r
      r%valor = n
      write(*, '(A,I0)', advance='no') 'valor=', r%valor
   end block                      ! aquí se ejecuta el finalizador

end program ciclo
""", """
**Lo que esta clase enseña en Fortran.** Este programa usa dos características que el Fortran clásico
no tenía y que juntas dan la liberación determinista.

**`final`** (Fortran 2003) declara un **finalizador**: un procedimiento que el runtime ejecuta cuando
el objeto deja de existir.

```fortran
type :: recurso
   integer :: valor = 0
contains
   final :: liberar
end type
```

Es el destructor de C++ y el `Finalize` de Ada, y se invoca al salir del ámbito, al reasignar sobre el
objeto y al desasignar un `allocatable` que lo contenga.

**`block`** (Fortran 2008) crea un **ámbito interno** con sus propias declaraciones, que era justo lo
que faltaba: antes de 2008, el único ámbito de un programa Fortran era el procedimiento entero, así
que no había forma de decir "este objeto vive solo aquí".

```fortran
block
   type(recurso) :: r
   ...
end block          ! r se finaliza AQUÍ
```

Ahora bien, conviene ser honesto sobre el estado real: **la finalización de Fortran es la
característica peor soportada del estándar de 2003**. Los compiladores tardaron más de una década en
implementarla, hay casos concretos —arreglos de tipos finalizables, finalización de temporales— en los
que sigue habiendo divergencias, y es un tema recurrente en las listas de correo de gfortran.

Por eso el idioma dominante en código Fortran real sigue siendo otro, y funciona:

```fortran
integer, allocatable :: v(:)     ! se libera SOLO al salir del ámbito
```

Un componente `allocatable` **se desasigna automáticamente** cuando su contenedor muere, sin
finalizador y sin código. Cubre el caso mayoritario —memoria— y por eso la ausencia de destructores
maduros duele menos de lo que cabría esperar en un lenguaje de cálculo.
"""),
        "ada": ("""
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;
with Ada.Finalization;

procedure Ciclo is

   type Recurso is new Ada.Finalization.Controlled with record
      Valor : Integer := 0;
   end record;

   overriding procedure Finalize (R : in out Recurso);

   overriding procedure Finalize (R : in out Recurso) is
   begin
      Put_Line (" estado=liberado");
   end Finalize;

   N : Integer;
begin
   Get (N);

   declare
      R : Recurso;             --  vive solo dentro de este bloque
   begin
      R.Valor := N;
      Put ("valor=");
      Put (R.Valor, Width => 1);
   end;                         --  aquí se llama a Finalize

end Ciclo;
""", """
**Lo que esta clase enseña en Ada.** **Ada tenía esto en 1983**, once años antes de que C++ le pusiera
nombre.

`Ada.Finalization.Controlled` es un tipo abstracto del que se hereda, y aporta tres operaciones que
ya aparecieron en las clases 099 y 102:

```ada
procedure Initialize (R : in out Recurso);   --  al crear
procedure Adjust     (R : in out Recurso);   --  al COPIAR
procedure Finalize   (R : in out Recurso);   --  al destruir
```

`Finalize` se ejecuta **al salir del ámbito, siempre**: por el final normal del bloque, por un `return`
anticipado, por un `goto` que salga y **por una excepción que se propague**. Esa última garantía es la
que hace utilizable el mecanismo, y es la misma que da el destructor de C++.

Y Ada tiene una variante que C++ no tiene: **`Limited_Controlled`**, para tipos que **no se pueden
copiar** (clase 101). Un fichero abierto o un bloqueo son `Limited_Controlled`: tienen `Initialize` y
`Finalize` pero no `Adjust`, porque copiarlos no tiene sentido y el lenguaje lo impide.

```ada
type Bloqueo is new Ada.Finalization.Limited_Controlled with ...
```

Eso es exactamente lo que en C++ se consigue borrando el constructor de copia y en Rust no
implementando `Copy` — declarado en el tipo desde el principio, en lugar de conseguido quitando algo.

Y el ecosistema de tiempo real de Ada lleva la idea más lejos con los **objetos protegidos**:

```ada
protected type Contador is
   procedure Incrementar;
   function Valor return Integer;
private
   N : Integer := 0;
end Contador;
```

Un objeto protegido garantiza **exclusión mutua sin escribir ni un `lock`**: el compilador y el
runtime generan la adquisición y la liberación, incluso si el cuerpo lanza una excepción. Es
propiedad de un recurso —el acceso exclusivo— gestionada por el lenguaje, y es una de las razones por
las que Ada se sigue eligiendo para sistemas concurrentes críticos.
"""),
        "pascal": ("""
program Ciclo;
{$MODE OBJFPC}{$H+}
uses SysUtils;

type
  TRecurso = class
    Valor: Integer;
    constructor Create(V: Integer);
    destructor Destroy; override;
  end;

constructor TRecurso.Create(V: Integer);
begin
  inherited Create;
  Valor := V;
end;

destructor TRecurso.Destroy;
begin
  Write(' estado=liberado');
  WriteLn;
  inherited Destroy;
end;

var
  N: Integer;
  R: TRecurso;

begin
  Read(N);

  R := TRecurso.Create(N);
  try
    Write('valor=', IntToStr(R.Valor));
  finally
    R.Free;               { liberación EXPLÍCITA, garantizada por finally }
  end;
end.
""", """
**Lo que esta clase enseña en Pascal.** Object Pascal tiene destructor y **no tiene liberación
automática de objetos**: `TRecurso.Create` reserva en el montón, y **alguien tiene que llamar a
`Free`**.

De ahí que el patrón `try...finally` sea **omnipresente** en el código Delphi y Lazarus, hasta el
punto de ser lo primero que se enseña:

```pascal
R := TRecurso.Create;
try
  ...
finally
  R.Free;
end;
```

`Free` es un método de `TObject` que comprueba si la referencia es `nil` antes de destruir, así que es
seguro llamarlo sobre algo no creado — una comodidad pequeña que evita muchos fallos.

Pascal ofrece **tres** mecanismos de gestión de vida, y elegir bien es la decisión de diseño típica
del lenguaje:

| Mecanismo | Vida |
|---|---|
| `record` | **valor**: muere con el ámbito, sin código |
| `class` + `Free` | manual, con `try/finally` |
| `interface` | **automática, por conteo de referencias** |

Las **interfaces** son la parte interesante: en Delphi y Free Pascal, una variable de tipo interfaz
lleva conteo de referencias, y el objeto **se destruye solo** cuando la última referencia desaparece.

```pascal
type IRecurso = interface
  procedure Usar;
end;

var R: IRecurso;
begin
  R := TRecurso.Create;      { a partir de aquí, se libera SOLA }
end;
```

Por eso mucho código Delphi declara interfaces **solo para no escribir `try/finally`**, un uso que
sorprende a quien las conoce únicamente como contrato de tipos.

Y hay una trampa muy conocida: **mezclar referencias de objeto y de interfaz al mismo objeto** produce
doble liberación, porque el conteo de referencias no ve la referencia de objeto. Es de los errores más
difíciles de diagnosticar del ecosistema.

`ARC` —conteo de referencias también para objetos— existió en Delphi para móviles entre 2013 y 2019,
y se retiró por las incompatibilidades que generaba. Es un caso instructivo de que **cambiar el modelo
de memoria de un lenguaje maduro es casi imposible**.
"""),
        "lisp": ("""
(let ((n (read)))
  (unwind-protect
       (format t "valor=~D" n)
    (format t " estado=liberado~%")))     ; la parte de LIMPIEZA
""", """
**Lo que esta clase enseña en Common Lisp.** Common Lisp **tiene recolector de basura**, así que la
memoria no es problema. Lo que sí lo es —ficheros, conexiones, bloqueos— se resuelve con
**`unwind-protect`**, que es el `try/finally` del lenguaje:

```lisp
(unwind-protect
     (forma-protegida)
  (limpieza-1)
  (limpieza-2))
```

La limpieza se ejecuta **pase lo que pase**: retorno normal, `return-from`, `go`, `throw` o una
condición que se propague.

Y sobre `unwind-protect` está construida la familia de macros `with-`, que es el idioma dominante:

```lisp
(with-open-file (f "datos.txt" :direction :output)
  (write-line "hola" f))          ; el fichero se cierra SOLO

(with-lock-held (mutex) ...)
(with-output-to-string (s) ...)
```

Y aquí está lo que hace distinto a Lisp: **`with-open-file` no es una característica del lenguaje, es
una macro** que expande a `unwind-protect`. Cualquiera puede escribir la suya:

```lisp
(defmacro with-recurso ((var valor) &body cuerpo)
  `(let ((,var (crear-recurso ,valor)))
     (unwind-protect (progn ,@cuerpo)
       (liberar-recurso ,var))))
```

Eso es lo que en Python son los gestores de contexto —una característica del lenguaje con protocolo
propio— y en Lisp es una macro de diez líneas. Es el argumento habitual a favor de las macros: **lo
que otros lenguajes añaden al núcleo, Lisp lo añade como biblioteca**.

Common Lisp tiene además **finalizadores** en las implementaciones —`sb-ext:finalize` en SBCL— con el
aviso de rigor: **se ejecutan cuando el recolector lo decide, o nunca**. Es la misma lección que los
finalizadores de Java, deprecados en Java 9 y eliminados en Java 18: **el recolector gestiona memoria,
no recursos**, y confiar en él para cerrar ficheros lleva a agotar los descriptores.
"""),
        "tcl": ("""
gets stdin linea
set n [string trim $linea]

try {
    puts -nonewline "valor=$n"
} finally {
    puts " estado=liberado"
}
""", """
**Lo que esta clase enseña en Tcl.** `try`/`finally` llegó en **Tcl 8.6 (2012)**, y antes de eso el
idioma era `catch` con limpieza a mano:

```tcl
set err [catch { ... } resultado opciones]
# limpieza
if {$err} { return -options $opciones $resultado }
```

`try` con `on error`, `trap` y `finally` sustituyó a ese patrón, y `finally` **se ejecuta siempre** —
incluida la salida por `return`, `break` o `error`.

Tcl gestiona la memoria por **conteo de referencias** sobre valores inmutables (clase 102), así que
las estructuras de datos se liberan solas. Lo que necesita gestión son los **recursos con nombre**:
canales, ventanas de Tk, comandos de objeto, imágenes.

Y ahí Tcl tiene un mecanismo propio y muy potente: **`trace`**.

```tcl
trace add variable v unset { apply {{args} { puts "liberado" }} }
trace add command $obj delete { ... }
trace add execution $cmd enter { ... }
```

**`trace` engancha código a un evento sobre una variable, un comando o una ejecución**, y `unset` es
el evento que dispara cuando la variable desaparece —incluido al salir del procedimiento—. Con eso se
construye un destructor sin que el lenguaje tenga destructores.

TclOO añade el destructor de verdad:

```tcl
oo::class create Recurso {
    constructor {v} { ... }
    destructor { puts " estado=liberado" }
}
```

Y se invoca al hacer `$obj destroy` o al destruirse el intérprete. **No al salir del ámbito**, porque
un objeto TclOO es un comando global (clase 101) y no pertenece a ningún ámbito.

Esa es la diferencia de fondo con C++ y Ada: en Tcl, la vida de un objeto **no está atada a una
variable de pila**, así que el idioma es `try/finally` con `destroy` explícito. Es el mismo modelo que
Java antes de `try-with-resources`.
"""),
        "perl": ("""
use strict;
use warnings;

package Recurso;
sub new { my ($clase, $v) = @_; return bless { valor => $v }, $clase }
sub DESTROY { print " estado=liberado\\n" }

package main;

my $linea = <STDIN>;
chomp $linea;

{
    my $r = Recurso->new($linea + 0);      # nace aquí
    print "valor=", $r->{valor};
}                                            # muere aquí: DESTROY
""", """
**Lo que esta clase enseña en Perl.** Perl gestiona la memoria por **conteo de referencias**, y eso le
da algo que un recolector generacional no puede dar: **destrucción determinista**.

`DESTROY` se llama **en el momento exacto** en que la última referencia desaparece —al salir del
bloque, en este programa— no "en algún momento futuro". Por eso los objetos de Perl pueden cerrar
ficheros y soltar bloqueos con fiabilidad, cosa que en Java o en C# sería un error de diseño.

El precio ya se vio en la clase 097: **los ciclos no se liberan nunca**, y hay que romperlos con
`Scalar::Util::weaken`.

Sobre esa base, Perl tiene tres idiomas para esta clase:

**El objeto guardián**, que es el equivalente exacto de RAII:

```perl
{
    my $guardia = Guard->new(sub { limpiar() });
    ...
}   # al salir, DESTROY llama a la función
```

`Guard` y `Scope::Guard` de CPAN empaquetan justo eso, y `Try::Tiny` da `try/catch/finally` con
semántica correcta —el `try/catch` nativo llegó a Perl en 5.34 (2021) y se estabilizó en 5.40—.

**`local`**, que restaura el valor anterior al salir del ámbito (clases 082 y 096):

```perl
{
    local $/ = undef;       # cambia el separador de registro...
    $contenido = <$fh>;
}                            # ...y se restaura solo
```

**Y los descriptores léxicos**, que es la mejora más agradecida:

```perl
open(my $fh, '<', 'datos.txt') or die $!;
# $fh se cierra SOLO al salir del ámbito
```

Antes de Perl 5.6, los descriptores eran símbolos globales —`open(FH, ...)`— que había que cerrar a
mano y que colisionaban entre módulos. Pasar a descriptores léxicos hizo que la mayor parte del código
Perl dejara de necesitar `close` explícito, y es un buen ejemplo de una mejora pequeña con efecto
grande.
"""),
        "cpp": ("""
#include <iostream>

class Recurso {
    int valor_;
public:
    explicit Recurso(int v) : valor_(v) {}
    ~Recurso() { std::cout << " estado=liberado\\n"; }   // se llama SOLO

    int valor() const { return valor_; }
};

int main() {
    int n{};
    if (!(std::cin >> n)) return 1;

    {
        Recurso r{n};                       // nace aquí
        std::cout << "valor=" << r.valor();
    }                                        // muere aquí: destructor

    return 0;
}
""", """
**Lo que esta clase enseña en C++.** Esto es **RAII** —*Resource Acquisition Is Initialization*—, el
nombre que Bjarne Stroustrup dio en 1994 a la idea de **atar la vida de un recurso a la vida de un
objeto de pila**.

El nombre es malo y él mismo lo ha reconocido: lo importante no es la adquisición sino **la liberación
en el destructor**. Pero la idea es probablemente la aportación más influyente de C++ al diseño de
lenguajes.

Tres garantías la sostienen, y las tres importan:

1. **El destructor se ejecuta siempre** al salir del ámbito: por el final, por un `return`, por un
   `break` y **por una excepción que se propague** (desenrollado de pila).
2. **En orden inverso a la construcción** (clase 096), lo que hace correctas las dependencias entre
   recursos.
3. **Determinista**: en el punto exacto, no cuando lo decida un recolector.

Sobre eso está construida toda la biblioteca estándar moderna:

```cpp
std::unique_ptr<T>          // memoria
std::lock_guard<std::mutex> // el bloqueo se suelta al salir
std::ifstream               // el fichero se cierra al salir
std::scoped_lock            // C++17: varios mutex sin interbloqueo
```

`std::lock_guard` es el ejemplo canónico: **no hay forma de olvidar soltar el mutex**, porque no hay
ninguna operación de soltar que escribir.

Y esta idea es exactamente lo que **Rust convirtió en el centro de su sistema de tipos**: la propiedad
y el préstamo de la clase 081 son RAII con comprobación en compilación. Rust añade lo que a C++ le
falta —**el compilador impide usar algo después de moverlo o liberarlo**— pero el modelo mental es el
mismo, y sus autores lo reconocen explícitamente.

C++ tiene además `std::exchange`, `std::swap` y la regla de los cinco (clase 102) como maquinaria
alrededor, y desde C++11 los tipos **solo movibles** —`unique_ptr`, `thread`, `lock_guard`— que
expresan propiedad única sin poder copiarse.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi CICLO;
  n int(10) const;
end-pi;

dcl-s p pointer;

// crear: RPG no tiene destructores; hay que liberar a mano
p = %alloc(4);

dsply ('valor=' + %char(n) + ' estado=liberado');

// liberar: explicito, siempre
dealloc p;

*inlr = *on;
return;
""", """
**Lo que esta clase enseña en RPG.** RPG **no tiene destructores ni ámbitos con liberación
automática**: `%alloc` reserva y `dealloc` libera, y olvidarlo es una fuga.

Y como en COBOL, en la práctica casi no hay fugas, por dos razones muy concretas de la plataforma.

**La primera es `*INLR`.** Esa línea que cierra todos los programas de esta serie:

```rpgle
*inlr = *on;
```

`*INLR` es el **indicador de última vuelta**, y activarlo hace que al terminar el programa el sistema
**cierre todos los ficheros abiertos, libere el almacenamiento estático y descargue el programa**. Es
limpieza automática al salir, integrada en el ciclo del lenguaje desde los años sesenta.

Y su ausencia es un error clásico: **sin `*INLR`, el programa queda cargado con sus ficheros abiertos
y sus variables intactas**, y la siguiente llamada continúa con el estado anterior. Eso a veces se usa
a propósito —para no reabrir ficheros en un bucle de llamadas— y a veces produce errores
desconcertantes.

**La segunda es el grupo de activación.** `actgrp(*caller)` en el `ctl-opt` de estos programas declara
en qué grupo de activación se ejecuta, y ese grupo **es la unidad de propiedad de los recursos**:

```text
RCLACTGRP ACTGRP(MIAPP)      -- reclamar el grupo: libera TODO lo suyo
```

Al terminar un grupo de activación, el sistema **libera toda la memoria reservada, cierra los ficheros
y deshace las transacciones pendientes** de todos los programas que corrían en él. Es un ámbito de
liberación automática **a nivel de sistema operativo**, no de lenguaje.

Es la misma idea que los *arenas* o *region allocators* que hoy se usan en C y en Rust para evitar la
liberación individual: **reservar todo en una región y liberar la región entera de golpe**. IBM i lo
lleva haciendo desde 1993.
"""),
        "pli": ("""
 ciclo: procedure options(main);

    declare n fixed binary(31);
    declare p pointer;
    declare 1 recurso based(p),
              2 valor fixed binary(31);

    get list (n);

    allocate recurso set(p);       /* crear */
    p -> valor = n;

    put skip list ('valor=' || trim(char(p -> valor)) ||
                   ' estado=liberado');

    free p -> recurso;              /* liberar: EXPLÍCITO */

 end ciclo;
""", """
**Lo que esta clase enseña en PL/I.** PL/I **no tiene destructores**, y `free` es responsabilidad del
programador, exactamente como en C.

Lo que sí tiene, y es notable para 1964, es el **manejo de condiciones con `on`**, que permite
enganchar limpieza a eventos:

```pli
 on condition(storage)  begin; put list('sin memoria'); end;
 on error               begin; call limpiar(); end;
 on endfile(entrada)    eof = '1'b;
 on finish              begin; call cerrar_todo(); end;
```

**`on finish`** es lo más cercano a un `finally` global: se ejecuta cuando el programa termina, normal
o anormalmente. Y **`on error`** captura cualquier condición no manejada.

Y hay una propiedad de `on` que lo distingue del `try/catch` moderno y que conviene entender: **los
manejadores de PL/I son de alcance DINÁMICO**, no léxico.

```pli
 procesar: procedure;
    on condition(zerodivide) begin; ... end;   /* activo durante TODA la llamada... */
    call subrutina;                              /* ...incluido dentro de subrutina */
 end procesar;
```

Un `on` establecido en un procedimiento sigue activo en todo lo que ese procedimiento llame, hasta que
retorna. Es exactamente el modelo de las **condiciones y reinicios de Common Lisp**, y ninguno de los
dos se parece al `try/catch` de C++ y Java, que es léxico y solo cubre el bloque.

La diferencia práctica es grande: con alcance dinámico, **una rutina de bajo nivel puede ser manejada
por una decisión tomada arriba**, sin pasar parámetros. Y con `signal condition`, PL/I permite además
definir condiciones propias:

```pli
 on condition(saldo_insuficiente) begin; ... end;
 signal condition(saldo_insuficiente);
```

Excepciones definidas por el usuario con manejadores dinámicos, en 1964. Es una de las
características por las que PL/I sigue apareciendo en las historias de la informática pese a su
declive comercial.
"""),
        "mumps": ("""
CICLO ; Ciclo de vida de los datos -- clase 103
 read n
 new recurso                       ; NEW apila el valor anterior
 set recurso = n
 write "valor=", recurso
 do liberar
 quit                               ; al salir, NEW restaura lo anterior
 ;
liberar ;
 kill recurso
 write " estado=liberado", !
 quit
""", """
**Lo que esta clase enseña en M.** M **no tiene destructores ni ámbitos de objeto**, y tiene dos
comandos que cubren esta clase de forma sorprendentemente directa.

**`kill`** destruye una variable o un subárbol entero:

```mumps
 kill v            ; borra v y TODOS sus subíndices
 kill v(3)         ; borra solo esa rama
 kill (a, b)       ; borra TODO menos a y b  <-- kill EXCLUSIVO
 kill ^DATOS       ; borra un global entero, en disco
```

El **`kill` exclusivo** —`kill (a, b)`— no tiene equivalente en ningún otro lenguaje de esta página:
borra todas las variables locales **excepto las nombradas**. Es la forma canónica de limpiar el
espacio de nombres global de M (clase 082) antes de llamar a algo.

**`new`** es el que resuelve el ciclo de vida, y ya apareció en la clase 096: apila el valor actual de
una variable y **lo restaura automáticamente al salir de la rutina**.

```mumps
 new i, j          ; se restauran solos al hacer quit
```

Es alcance dinámico implementado como pila, igual que `local` de Perl y `controlled` de PL/I, y es
**la única liberación automática que tiene M**.

Y sobre los recursos serios, M tiene lo que más importa en su dominio: **la transacción**.

```mumps
 tstart
 set ^CUENTA(a) = ^CUENTA(a) - importe
 set ^CUENTA(b) = ^CUENTA(b) + importe
 tcommit
```

Si el proceso muere entre `tstart` y `tcommit`, **el sistema deshace todo automáticamente**, incluidos
los bloqueos tomados con `lock`. Es la misma solución que COBOL con CICS y RPG con los grupos de
activación: **la propiedad de los recursos la gestiona la plataforma, no el lenguaje**.

Los tres lenguajes de gestión de esta página llegaron, por caminos independientes, a la misma
conclusión: cuando lo que hay que proteger son datos compartidos y no memoria, **la unidad de limpieza
correcta es la transacción**.
"""),
        "smalltalk": ("""
| n |

n := stdin nextLine trimBoth asNumber.

[ Transcript show: 'valor=', n printString ]
    ensure: [ Transcript show: ' estado=liberado'; cr ].
""", """
**Lo que esta clase enseña en Smalltalk.** `ensure:` es el `finally` de Smalltalk, y —como todo en el
lenguaje— **es un mensaje enviado a un bloque**:

```smalltalk
[ ... ] ensure: [ ... limpieza ... ]
[ ... ] ifCurtailed: [ ... solo si termina ANORMALMENTE ... ]
```

`ensure:` ejecuta la limpieza pase lo que pase; **`ifCurtailed:` solo si el bloque se abandona** por
una excepción o un retorno no local. Esa distinción —limpiar siempre frente a limpiar solo si algo
salió mal— no la hace casi ningún lenguaje, y es útil: deshacer una transacción es `ifCurtailed:`,
cerrar un fichero es `ensure:`.

Sobre `ensure:` está construido el idioma habitual:

```smalltalk
'datos.txt' asFileReference writeStreamDo: [ :flujo | ... ]
```

`writeStreamDo:` abre, ejecuta el bloque y cierra con `ensure:`. Es el mismo patrón que
`with-open-file` de Lisp, y por la misma razón: **con bloques de primera clase, un gestor de recursos
es un método normal**.

Smalltalk tiene **recolector de basura desde 1980** —fue uno de los primeros sistemas con recolector
generacional— así que la memoria no requiere atención. Para lo demás hay dos mecanismos poco
conocidos:

```smalltalk
objeto finalizationRegistry
WeakArray with: objeto             "referencias DÉBILES"
```

Las **referencias débiles** no impiden que el recolector se lleve el objeto, y son la base de
`WeakKeyDictionary` (clase 095) y de los registros de finalización. Smalltalk las tuvo antes que Java
y con la misma advertencia: **la finalización no es determinista**.

Y hay un matiz que solo aparece en un sistema de imagen viva (clase 041): **la imagen persiste entre
sesiones**, así que un objeto mal gestionado no muere al cerrar el programa — **sigue ahí mañana**. La
higiene de recursos en Smalltalk importa por una razón que en un proceso normal no existe: **no hay
final del proceso que lo limpie todo**.
"""),
    },
)
