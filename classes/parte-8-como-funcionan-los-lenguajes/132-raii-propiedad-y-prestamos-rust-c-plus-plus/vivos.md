# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 132

> [⬅️ Volver a la clase 132](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Un recurso que se adquiere, se usa y se libera solo. Es RAII, y esta clase cierra el arco de la Parte
8 con la conclusión que las clases 128 a 131 han ido preparando: **la gestión automática de memoria no
la inventó el recolector, la inventó el ÁMBITO**. Y aquí hay dos lenguajes que llegaron antes que C++:
**Ada con los tipos controlados en 1983** y **Pascal con `try/finally`**, que resuelve el mismo
problema desde el otro lado.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es la **propiedad: quién es responsable de liberar y cuándo**, y estos lenguajes lo
> enseñan porque tienen todas las piezas de las que Rust hizo un sistema de tipos. **`Finalize` de Ada
> es el destructor**; **`allocatable` de Fortran es propiedad única sin alias**; **`limited` de Ada es
> un tipo que no se puede copiar**; **`unique_ptr` de C++ es propiedad única con movimiento** (clase
> 081).
>
> Rust no inventó esas ideas: **las juntó y las hizo comprobables en compilación**. Ver las piezas
> sueltas en los lenguajes donde nacieron explica de dónde viene el préstamo mejor que cualquier
> introducción.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: un entero `n` → stdout: `resultado=<2n>`
- **Regla:** `prestar n a una función que devuelve 2n`

| stdin | esperado |
|---|---|
| `5` | `resultado=10` |
| `0` | `resultado=0` |
| `7` | `resultado=14` |

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
PROGRAM-ID. PROPIED.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  N       PIC S9(9)  COMP-3.
01  R       PIC S9(18) COMP-3.
01  ED-R    PIC -(17)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    COMPUTE N = FUNCTION NUMVAL(LINEA)

    PERFORM ADQUIRIR
    PERFORM USAR
    PERFORM LIBERAR

    MOVE R TO ED-R
    DISPLAY "resultado=" FUNCTION TRIM(ED-R)
    STOP RUN.

ADQUIRIR.
    CONTINUE.

USAR.
    COMPUTE R = N * 2.

LIBERAR.
    CONTINUE.
```

**Lo que esta clase enseña en COBOL.** **COBOL no tiene RAII, ni destructores, ni propiedad**, y sus
sistemas gestionan recursos con una fiabilidad que muchos lenguajes modernos envidiarían.

La razón es la que esta parte del curso ha repetido: **la propiedad está en la transacción, no en el
objeto**.

```cobol
EXEC CICS READ FILE('CLIENTES') RIDFLD(ID) UPDATE END-EXEC
*> el registro queda BLOQUEADO
EXEC CICS SYNCPOINT END-EXEC
*> se confirma y se sueltan TODOS los bloqueos y recursos
```

**El monitor es el dueño de todo**: bloqueos de registro, memoria de `GETMAIN`, colas, conexiones. Y
cuando la transacción termina —bien o mal— **libera todo lo suyo**.

Eso es RAII con la unidad puesta en la transacción en lugar del ámbito léxico, y tiene una propiedad
que RAII no tiene: **funciona aunque el programa se caiga**. Un destructor de C++ no se ejecuta si el
proceso muere; un `SYNCPOINT` deshecho por el monitor, sí.

Dentro del programa, COBOL tiene lo que la clase 103 describía:

```cobol
DECLARATIVES.
ERROR-FICHERO SECTION.
    USE AFTER STANDARD ERROR PROCEDURE ON CLIENTES.
```

**Un manejador declarativo que el sistema invoca al fallar una operación** — y que se usa para cerrar y
registrar.

Y hay una construcción de COBOL-2002 que se parece más a lo de esta clase de lo que suele reconocerse:
**los programas anidados con `LOCAL-STORAGE`** (clase 127).

```cobol
PROGRAM-ID. SUB RECURSIVE.
LOCAL-STORAGE SECTION.
01  BUFFER  PIC X(1000).      *> se reserva al entrar, se libera al salir
```

**`LOCAL-STORAGE` es un recurso atado al ámbito de la invocación**, y eso es exactamente la idea de
RAII aplicada a la memoria.

Lo que falta es el gancho: **no hay forma de ejecutar código al salir**. Es la mitad del mecanismo, y
la otra mitad la pone el monitor.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program propied
   implicit none
   integer :: n, r

   read(*, *) n

   block
      integer, allocatable :: recurso(:)
      allocate(recurso(100))          ! adquirir
      recurso = n
      r = recurso(1) * 2               ! usar
   end block                            ! LIBERAR: automático, salga por donde salga

   write(*, '(A,I0)') 'resultado=', r
end program propied
```

**Lo que esta clase enseña en Fortran.** **`allocatable` es propiedad única con liberación por ámbito**,
y esa frase describe exactamente lo que Rust llama *ownership*.

Y las tres propiedades que lo hacen equivalente son las de la clase 128:

1. **No puede tener alias.** Solo un nombre posee el arreglo.
2. **Se libera al salir del ámbito**, siempre.
3. **`move_alloc` transfiere la propiedad** sin copiar (clase 081) — que es el `std::move` de C++ y el
   movimiento de Rust.

```fortran
call move_alloc(origen, destino)      ! origen queda SIN ASIGNAR
```

**Después de `move_alloc`, `origen` está desasignado** — igual que una variable movida en Rust queda
inutilizable. Es la misma semántica, expresada con una subrutina en lugar de con el sistema de tipos.

Y Fortran 2003 completó el modelo con **componentes `allocatable` en tipos derivados**:

```fortran
type :: matriz
   real, allocatable :: datos(:,:)      ! el tipo POSEE sus datos
end type
```

**Al morir una `matriz`, sus datos se liberan automáticamente**, en cascada — que es exactamente lo que
hace `unique_ptr` dentro de una clase en C++ (clase 128).

Lo que a Fortran le falta para ser RAII completo es el gancho de la clase 103: **`final`**, que existe
desde 2003 y es la característica peor soportada del estándar.

```fortran
type :: fichero
   integer :: unidad
contains
   final :: cerrar          ! DEBERÍA ejecutarse al morir el objeto
end type
```

**Con `final` funcionando bien, Fortran tendría RAII para cualquier recurso.** Sin él, la memoria se
libera sola y los ficheros hay que cerrarlos a mano.

Es un caso claro de lo que esta clase quiere mostrar: **las piezas de RAII estaban repartidas por
varios lenguajes, y hacía falta juntarlas**.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;
with Ada.Finalization;

procedure Propied is
   package Recursos is
      type Recurso is new Ada.Finalization.Limited_Controlled with record
         Valor : Integer := 0;
      end record;

      overriding procedure Initialize (R : in out Recurso);
      overriding procedure Finalize   (R : in out Recurso);
   end Recursos;

   package body Recursos is
      overriding procedure Initialize (R : in out Recurso) is
      begin
         null;                    --  adquirir
      end Initialize;

      overriding procedure Finalize (R : in out Recurso) is
      begin
         null;                    --  LIBERAR: automático al salir del ámbito
      end Finalize;
   end Recursos;

   use Recursos;

   N, R : Integer;
begin
   Get (N);

   declare
      Rec : Recurso;              --  Initialize aquí
   begin
      Rec.Valor := N;
      R := Rec.Valor * 2;
   end;                            --  Finalize aquí, pase lo que pase

   Put ("resultado=");
   Put (R, Width => 1);
   New_Line;
end Propied;
```

**Lo que esta clase enseña en Ada.** **Ada tenía RAII completo en 1983**, once años antes de que
Stroustrup le pusiera nombre, y este programa lo demuestra con las tres piezas juntas.

**Primera: `Limited_Controlled`.** El tipo es a la vez:

- **`Controlled`**: tiene `Initialize` y `Finalize`, que el runtime ejecuta al crear y al destruir.
- **`Limited`**: **no se puede copiar ni asignar** (clase 101).

Esa segunda mitad es lo que Rust expresa no implementando `Copy` y C++ borrando el constructor de
copia. **En Ada es una palabra en la declaración del tipo.**

**Segunda: `Finalize` se ejecuta siempre.** Al salir del bloque, por `return`, por `goto` y **por una
excepción que se propague**. Es la garantía que hace utilizable el mecanismo.

**Y tercera: la comprobación de accesibilidad** (clase 083), que impide guardar una referencia a algo
que vive menos. **Eso es el préstamo con comprobación en compilación**, y Ada lo tiene desde el
principio para los tipos de acceso.

Y Ada 2012 añadió lo que faltaba para acercarse todavía más a Rust: **los aspectos de propiedad**.

```ada
type Puntero is not null access Recurso
   with Ownership;                        --  SPARK: propiedad comprobada
```

**En SPARK, `Ownership` hace que el análisis siga quién posee cada recurso** y rechace usar algo tras
moverlo o liberarlo — **con comprobación estática, como Rust**.

Es la conclusión de esta clase: **las piezas del sistema de propiedad de Rust existían repartidas —
destructores en Ada y C++, propiedad única en Fortran, tipos no copiables en Ada— y lo que hizo Rust
fue hacerlas comprobables por el compilador en un solo modelo coherente**.

Y merece decir lo que Ada hace mejor incluso hoy: **`Finalize` se ejecuta también al abortar una
tarea** (clase 121), y la combinación de tipos controlados con objetos protegidos garantiza la
liberación en escenarios concurrentes que en otros lenguajes exigen cuidado manual.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Propied;
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
  Valor := V;                    { adquirir }
end;

destructor TRecurso.Destroy;
begin
  inherited Destroy;              { liberar }
end;

var
  N, R: Integer;
  Rec: TRecurso;

begin
  Read(N);

  Rec := TRecurso.Create(N);
  try
    R := Rec.Valor * 2;
  finally
    Rec.Free;                     { SIEMPRE se ejecuta }
  end;

  WriteLn('resultado=', IntToStr(R));
end.
```

**Lo que esta clase enseña en Pascal.** Pascal resuelve esta clase **desde el otro lado**: no con
destructores automáticos, sino con **`try...finally`**, que garantiza la ejecución de la limpieza.

Y esa diferencia merece explicarse, porque es la elección que hicieron Java, C# y Python:

| | RAII (C++, Ada, Rust) | `try/finally` (Pascal, Java) |
|---|---|---|
| Quién libera | **el destructor del objeto** | **el bloque de código** |
| Se escribe | una vez, en el tipo | **en cada uso** |
| Se puede olvidar | no | **sí** |
| Funciona con excepciones | sí | sí |

**La ventaja de RAII es que se escribe una vez y no se puede olvidar**; la de `try/finally` es que no
exige destructores automáticos ni semántica de valor.

Y el mundo Pascal ha ido convergiendo hacia RAII por tres vías:

**Las interfaces con conteo de referencias** (clases 103 y 131), que liberan solas y que se usan a
menudo **solo por eso**.

**Los registros gestionados** de Free Pascal 3.2 (clase 130), que sí son RAII completo:

```pascal
type
  TRecurso = record
    class operator Initialize(var R: TRecurso);   { constructor automático }
    class operator Finalize(var R: TRecurso);      { DESTRUCTOR automático }
  end;

procedure P;
var R: TRecurso;        { Initialize aquí }
begin
  ...
end;                     { Finalize aquí, pase lo que pase }
```

**Eso es exactamente RAII**, llegado a Pascal en 2020.

**Y los helpers y las clausuras**, con los que se construye el patrón de "recurso con bloque":

```pascal
ConRecurso(procedure(const R: TRecurso)
           begin ... end);          { la función adquiere, llama y libera }
```

Es el `with-open-file` de Lisp (clase 103) escrito con métodos anónimos, y es lo que hacen hoy muchas
bibliotecas de Delphi.

Merece cerrar señalando que **el `try/finally` de Delphi es de 1995 y precede a `try-with-resources`
de Java (2011) en dieciséis años** — y que la crítica que se le hace hoy —que hay que acordarse de
escribirlo— es exactamente la que motivó RAII.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let* ((n (read))
       (r 0))
  ;; unwind-protect: la limpieza se ejecuta pase lo que pase (clase 103)
  (unwind-protect
       (setf r (* n 2))
    nil)                              ; aquí iría la liberación
  (format t "resultado=~D~%" r))
```

**Lo que esta clase enseña en Common Lisp.** Lisp resuelve esta clase con **`unwind-protect`** y con las
macros `with-` que se construyen sobre él (clase 103), y esa solución tiene una propiedad que la
distingue de RAII: **la limpieza está en el sitio de uso, no en el tipo**.

```lisp
(with-open-file (f "datos.txt")       ; adquirir
  (leer f))                            ; usar; y al salir, cerrar
```

Y como se dijo en la clase 103, **eso no es una característica del lenguaje: es una macro**, y
cualquiera puede escribir la suya:

```lisp
(defmacro with-recurso ((var arg) &body cuerpo)
  `(let ((,var (adquirir ,arg)))
     (unwind-protect (progn ,@cuerpo)
       (liberar ,var))))
```

**Diez líneas y el patrón queda disponible para todo el proyecto**, con la limpieza garantizada y
escrita una sola vez — que es la ventaja de RAII conseguida con macros.

Es la diferencia entre los dos enfoques: **RAII lo ata al tipo; las macros lo atan a la forma de
uso**. Y para recursos que no son objetos —una transacción, un bloqueo global, un cambio temporal de
configuración— **la macro encaja mejor**.

Y Lisp tiene un tercer mecanismo que ningún otro lenguaje de esta página tiene y que resuelve casos que
RAII no cubre: **el enlace dinámico** (clase 082).

```lisp
(let ((*print-base* 16))
  (print 255))              ; FF -- y al salir, *print-base* vuelve a 10
```

**Cambiar una variable especial dentro de un `let` la restaura al salir**, automáticamente y
respetando las excepciones. Es RAII aplicado a la configuración, sin objetos y sin macros.

Es el mismo mecanismo que `local` en Perl (clase 096), `new` en M y `controlled` en PL/I — cuatro
lenguajes que llegaron a lo mismo.

Y la conclusión de esta clase en Lisp es la de la clase 107: **el problema de la propiedad se resuelve
con las herramientas que el lenguaje ya tiene**, y en Lisp esas herramientas son la macro y el ámbito.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea
set n [string trim $linea]

try {
    set recurso [expr {$n * 2}]       ;# adquirir y usar
    puts "resultado=$recurso"
} finally {
    # liberar: se ejecuta pase lo que pase
}
```

**Lo que esta clase enseña en Tcl.** Tcl resuelve esta clase con `try...finally` (Tcl 8.6) y con los
mecanismos de la clase 103, y su modelo de memoria hace que la propiedad casi no sea un problema:
**los valores son inmutables y se liberan solos** (clase 131).

Lo que sí tiene dueño en Tcl son **los recursos con nombre**: canales, objetos, ventanas, temporizadores
e intérpretes. Y para ellos hay tres patrones:

```tcl
try { ... } finally { close $canal }              ;# explícito
trace add variable v unset { close $canal }        ;# atado a una VARIABLE
oo::class create R { destructor { close $canal } }  ;# atado a un objeto
```

**El segundo es el más parecido a RAII y el menos conocido**: `trace ... unset` engancha código a la
desaparición de una variable, **incluida la salida del procedimiento**.

```tcl
proc procesar {} {
    set canal [open datos.txt]
    trace add variable canal unset [list apply {{c args} { close $c }} $canal]
    ...
}                                     ;# al salir, `canal` desaparece y se cierra
```

Eso es **un destructor construido con las piezas del lenguaje**, y funciona aunque haya `return` o
error.

Y Tcl tiene la liberación por región de la clase 130, que es la respuesta más contundente:

```tcl
set i [interp create]
$i eval $codigo_no_confiable
interp delete $i                ;# TODO lo suyo desaparece
```

**Un intérprete secundario es una arena**: sus variables, sus procedimientos, sus canales y sus objetos
mueren con él.

Y eso conecta con la clase 153, porque es también el mecanismo de aislamiento de Tcl: **un intérprete
seguro (*safe interp*) tiene comandos restringidos y se destruye entero**, con lo que ejecutar código
ajeno no puede dejar residuos.

Es una idea que hoy reaparece en los aislamientos de WebAssembly y en los espacios de nombres de los
contenedores: **dar un mundo pequeño y borrarlo entero**.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

package Guardia;
sub new { my ($c, $cb) = @_; return bless { cb => $cb }, $c }
sub DESTROY { $_[0]{cb}->() }          # se ejecuta al morir el objeto

package main;

my $n = <STDIN>;
chomp $n;

my $r;
{
    my $g = Guardia->new(sub { });     # "adquirir": la limpieza va en el guardia
    $r = $n * 2;
}                                        # aquí muere $g y se ejecuta DESTROY

print "resultado=$r\n";
```

**Lo que esta clase enseña en Perl.** Este programa implementa **RAII en Perl**, y funciona por la
propiedad de la clase 131: **el conteo de referencias da destrucción determinista**.

`$g` muere al salir del bloque, `DESTROY` se ejecuta **en ese instante**, y la limpieza ocurre.

Ese patrón tiene nombre en la comunidad —**el objeto guardián**— y CPAN lo empaqueta:

```perl
use Scope::Guard;
my $g = Scope::Guard->new(sub { close $fh });

use Guard;
scope_guard { limpiar() };            # sintaxis más limpia
```

Y esta clase permite señalar por qué Perl puede hacer esto y Java no: **la diferencia entre conteo de
referencias y recolector de trazado**.

| | Conteo (Perl, Tcl, Delphi) | Trazado (Java, Lisp, Smalltalk) |
|---|---|---|
| Cuándo se destruye | **en el instante exacto** | **cuando el recolector quiera** |
| Sirve para RAII | **sí** | no |
| Ciclos | problema | resueltos |
| Coste | en cada copia | en las pausas |

**Esa primera fila es la que decide**: RAII necesita saber **cuándo** muere el objeto, y un recolector
de trazado no lo garantiza. Por eso Java necesitó `try-with-resources` y Python, pese a tener conteo de
referencias en CPython, documenta que no hay que depender de él.

Y Perl tiene además `local` (clases 082 y 096), que es RAII para variables globales:

```perl
{
    local $/ = undef;        # cambia el separador de registro
    $todo = <$fh>;
}                             # y se RESTAURA al salir, pase lo que pase
```

**`local` guarda el valor anterior en una pila interna y lo restaura al salir del ámbito**, incluidas
las salidas por excepción. Es exactamente el enlace dinámico de Lisp de esta misma clase.

Cuatro lenguajes de esta página —Perl, Lisp, PL/I y M— tienen ese mecanismo, y ninguno de los cuatro lo
llamó RAII.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>

class Recurso {
    int valor_;
public:
    explicit Recurso(int v) : valor_(v) {}      // adquirir
    ~Recurso() = default;                        // liberar: automático
    Recurso(const Recurso&) = delete;             // NO copiable: propiedad única
    Recurso& operator=(const Recurso&) = delete;
    int valor() const { return valor_; }
};

int main() {
    int n{};
    if (!(std::cin >> n)) return 1;

    int r = 0;
    {
        const Recurso rec{n};        // nace
        r = rec.valor() * 2;
    }                                 // muere: destructor, pase lo que pase

    std::cout << "resultado=" << r << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** Este programa tiene las tres piezas de la propiedad, y merece
verlas por separado:

```cpp
explicit Recurso(int v) : valor_(v) {}         // 1. ADQUIRIR en el constructor
~Recurso() = default;                           // 2. LIBERAR en el destructor
Recurso(const Recurso&) = delete;                // 3. NO COPIABLE: dueño único
```

**La tercera es la que convierte RAII en propiedad.** Sin ella, dos objetos podrían creerse dueños del
mismo recurso y liberarlo dos veces. `= delete` (C++11) es la forma moderna de expresarlo; antes se
declaraba privado y sin definir.

Y con el movimiento (clase 081), la propiedad se puede **transferir**:

```cpp
Recurso(Recurso&&) noexcept;                    // constructor de MOVIMIENTO
Recurso& operator=(Recurso&&) noexcept;
```

**Eso es exactamente el modelo de Rust**: un dueño, transferible, no copiable.

Y aquí está la comparación que cierra esta clase y esta parte del curso:

| | C++ | Rust |
|---|---|---|
| Propiedad única | por convención (`unique_ptr`) | **en el sistema de tipos** |
| Usar tras mover | compila; el objeto queda "válido pero indeterminado" | **no compila** |
| Referencia colgante | compila; comportamiento indefinido | **no compila** |
| Dos referencias mutables | compila | **no compila** |
| Coste en ejecución | ninguno | ninguno |

**Las ideas son las mismas; la diferencia es quién las comprueba.** Los autores de Rust lo dicen
explícitamente: **RAII de C++ es el antepasado directo de la propiedad de Rust**, y el préstamo es la
formalización de lo que las guías de C++ recomiendan de palabra.

Y C++ ha ido en esa dirección con las herramientas:

```cpp
[[nodiscard]] Recurso crear();          // avisa si se ignora el resultado
gsl::owner<T*>                            // marcar quién posee, en las Core Guidelines
clang-tidy --checks=cppcoreguidelines-*   // comprobación estática de las reglas
```

**Las C++ Core Guidelines de Stroustrup y Sutter son, en buena medida, el modelo de Rust escrito como
recomendaciones** — con analizadores que comprueban parte de ellas.

Es un buen final para la Parte 8: **el problema de "quién limpia" recorre sesenta años de diseño de
lenguajes, y la respuesta ha ido pasando del programador a la biblioteca y de la biblioteca al
compilador**.

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

dcl-pi PROPIED;
  n int(10) const;
end-pi;

dcl-s p pointer;
dcl-s r int(20);

monitor;
  p = %alloc(100);           // adquirir
  r = n * 2;                  // usar
on-error;
  // manejar el error
endmon;

dealloc(n) p;                 // liberar: tambien si hubo error

dsply ('resultado=' + %char(r));

*inlr = *on;
return;
```

**Lo que esta clase enseña en RPG.** RPG no tiene destructores ni propiedad, y tiene las dos piezas que
la plataforma pone en su lugar y que ya han aparecido en las clases 103, 130 y 131.

**Primera: `monitor`/`on-error`/`endmon`**, el manejo de errores de RPG, con el que se construye el
patrón de esta clase.

```rpgle
monitor;
  p = %alloc(1000);
  procesar(p);
on-error;
  // limpiar y relanzar
endmon;
dealloc(n) p;
```

Con la advertencia del cierre de esta clase: **eso hay que escribirlo bien en cada uso**, y `on-error`
no cubre todos los caminos si hay `return` dentro.

**Y segunda, la que de verdad resuelve el problema: el grupo de activación** (clase 130).

```text
CRTPGM ... ACTGRP(MIAPP)
RCLACTGRP ACTGRP(MIAPP)      -- libera TODO: memoria, ficheros, transacciones
```

**El dueño de los recursos es el grupo de activación**, no el objeto ni el ámbito. Y su final libera
todo lo suyo, aunque el programa haya fallado.

Es la misma arquitectura que CICS en COBOL de esta clase: **la propiedad está en la unidad de trabajo**.

Y RPG tiene además el `*INLR` de la clase 103, que es propiedad a nivel de programa:

```rpgle
*inlr = *on;      // al terminar: cerrar ficheros, liberar estático, descargar
```

Merece cerrar esta página con la observación que la Parte 8 ha ido construyendo: **las plataformas de
gestión resolvieron el problema de "quién limpia" antes que los lenguajes, y lo resolvieron a una
escala mayor**.

RAII ata la limpieza a un ámbito léxico; CICS y los grupos de activación la atan a **una unidad de
trabajo que puede abarcar varios programas y sobrevivir a un fallo**. Son soluciones al mismo problema
en niveles distintos, y las dos siguen siendo necesarias.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 propied: procedure options(main);

    declare n fixed binary(31);
    declare r fixed binary(31);
    declare p pointer;
    declare recurso(100) fixed binary(31) based(p);

    get list (n);

    on error begin;                  /* manejador con alcance dinamico */
       put skip list ('error');
    end;

    allocate recurso set(p);          /* adquirir */
    r = n * 2;                         /* usar */
    free recurso;                       /* liberar */

    put skip list ('resultado=' || trim(char(r)));

 end propied;
```

**Lo que esta clase enseña en PL/I.** PL/I **no tiene RAII**, y tiene las tres piezas sueltas repartidas
por el lenguaje, que es exactamente el punto de esta clase.

**El almacenamiento `automatic`** (clase 127) es propiedad por ámbito para la memoria de pila: se
reserva al entrar y se libera al salir.

**Las áreas** (clases 128 y 130) son propiedad por región: liberar el área libera todo lo de dentro.

**Y `controlled`** (clase 096) es una pila de generaciones donde el emparejamiento es estructural.

Lo que falta es **el gancho**: no hay forma de ejecutar código al salir de un ámbito. Un procedimiento
PL/I no tiene destructor.

Y sin embargo PL/I tiene la construcción que más se le acerca de esta página, y que ya se ha mencionado
varias veces: **`on finish`**.

```pli
 on finish begin;
    call cerrar_todo();      /* se ejecuta al TERMINAR el programa, normal o no */
 end;
```

Y con manejadores de alcance dinámico (clase 103), un procedimiento puede establecer un manejador que
cubra **todo lo que llame**, y limpiar desde ahí.

Merece cerrar la página de PL/I en esta parte con el balance que se ha ido acumulando: **PL/I tuvo
punteros, reserva dinámica, áreas, multitarea, promesas, excepciones reanudables y aritmética de
arreglos antes que nadie**.

Lo que no tuvo fue **el destructor automático**, que es la pieza que convierte todas las demás en un
sistema. C++ la añadió en 1985, Ada en 1983, y esa pieza es la que hizo posible RAII.

Es una lección de diseño que esta clase deja clara: **un lenguaje no es la suma de sus
características, sino cómo encajan**. PL/I tenía más piezas que casi nadie y le faltó la que las unía.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
PROPIED ; RAII, propiedad y prestamos -- clase 132
 read n
 new recurso                        ; "adquirir": apila el valor anterior
 set recurso = n * 2
 write "resultado=", recurso, !
 quit                                ; al salir, `new` restaura: liberacion automatica
```

**Lo que esta clase enseña en M.** M no tiene destructores ni propiedad, y tiene **`new`**, que es lo
más parecido a RAII que ofrece el lenguaje y que ya ha aparecido en las clases 096, 127 y 131.

```mumps
 new recurso          ; guarda el valor anterior en una pila
 ...
 quit                  ; y lo RESTAURA al salir, pase lo que pase
```

**`new` ata la restauración al final de la rutina**, incluida la salida por error. Es exactamente
`local` de Perl y el enlace dinámico de Lisp de esta misma clase.

Y para los recursos de verdad —bloqueos y transacciones—, M tiene la propiedad atada al **proceso** y a
la **transacción**:

```mumps
 lock +^PACIENTE(id)
 ...
 lock -^PACIENTE(id)
```

Con una garantía que ningún destructor da: **si el proceso muere, el sistema suelta sus bloqueos**. Es
la misma propiedad que la clase 121 destacaba de las transacciones frente a los mutex.

```mumps
 tstart
 ...
 tcommit               ; o si el proceso muere: TROLLBACK automático
```

**El dueño de la transacción es el proceso, y su muerte la deshace.**

Y merece cerrar la Parte 8 desde M con la observación que la recorre entera: **M no tiene ninguna de
las construcciones de esta parte** —ni pila de marcos con destructores, ni montón explícito, ni
recolector, ni propiedad— **y sostiene sistemas con miles de usuarios concurrentes sobre datos
compartidos**.

Lo hace porque **movió el problema de sitio**: la gestión de memoria es del intérprete, la
persistencia es del modelo de datos, la concurrencia es de las transacciones y la limpieza es del
proceso.

No es que M resolviera estos problemas mejor. Es que **eligió un modelo donde la mayoría no aparecen**,
y pagó el precio en todo lo demás — sin tipos, sin ámbitos, sin módulos y sin objetos.

Es, probablemente, la lección más útil de esta parte del curso: **la mitad de los problemas de un
lenguaje vienen de decisiones que podrían no haberse tomado**.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| n r |

n := stdin nextLine trimBoth asNumber.

r := [ n * 2 ]                    "usar"
    ensure: [ nil ].               "liberar: se ejecuta pase lo que pase"

Transcript show: 'resultado=', r printString; cr.
```

**Lo que esta clase enseña en Smalltalk.** Smalltalk resuelve esta clase con **`ensure:`** y
**`ifCurtailed:`** (clase 103), y no con destructores: **tiene recolector de basura**, así que la
memoria no necesita propiedad, y para los demás recursos usa bloques.

```smalltalk
[ ... ] ensure: [ ... ]              "limpiar SIEMPRE"
[ ... ] ifCurtailed: [ ... ]          "limpiar solo si termina ANORMALMENTE"
'f.txt' asFileReference readStreamDo: [ :s | ... ]   "el patrón with-"
```

Y esa distinción entre `ensure:` e `ifCurtailed:` —limpiar siempre frente a limpiar solo si algo falló—
es más fina que la de casi todos los lenguajes de esta página, y es útil: **deshacer una transacción es
`ifCurtailed:`; cerrar un fichero es `ensure:`**.

Lo que Smalltalk no tiene es propiedad, y no la necesita: **el recolector se ocupa, y las referencias
débiles cubren las cachés** (clase 131).

Y merece cerrar la Parte 8 con la observación que la recorre desde el lado de Smalltalk: **este sistema
tomó la decisión contraria a la de C++ en cada una de las dieciséis clases de esta parte**.

| | C++ | Smalltalk |
|---|---|---|
| Compilación | AOT a nativo | bytecode con JIT |
| Memoria | manual y RAII | **recolector** |
| Referencias | punteros crudos | **solo referencias, sin direcciones** |
| Pila | estructura interna | **objetos inspeccionables** |
| Tipos | estáticos | dinámicos |
| Errores | excepciones que desenrollan | **excepciones REANUDABLES** |

**Y los dos funcionan.** C++ mueve los sistemas donde el rendimiento y el control mandan; Smalltalk
influyó en cómo se programa todo lo demás — y sus técnicas de máquina virtual son las que hacen rápido
a JavaScript y a Java hoy.

Es la conclusión honesta de esta parte del curso: **no hay un conjunto correcto de decisiones sobre
cómo funciona un lenguaje**. Hay compromisos, y cada uno abre unas puertas y cierra otras.

---

## Y de vuelta a la clase

Lo transferible: **RAII es una respuesta a una pregunta más general que la memoria — ¿quién limpia?**.
Ficheros, bloqueos, conexiones, transacciones y bloques de memoria comparten el problema, y todos se
resuelven igual: **atar la liberación a la muerte de algo que muere seguro**. Cuando escribas código
con recursos, la pregunta útil no es "¿dónde libero?" sino **"¿de quién es esto y qué lo va a
enterrar?"** — y si la respuesta es "de nadie en concreto", ahí está el fallo futuro.

⏮️ [Volver a la clase 132](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
