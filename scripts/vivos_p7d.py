# -*- coding: utf-8 -*-
"""Parte 7, lote D — clase 110. Ver `vivos_parte7.py` y `gen_vivos.py`."""

SPECS: dict[str, dict] = {}

# ---------------------------------------------------------------------------
# 110 — Orientado a objetos: clases, objetos y estado
# ---------------------------------------------------------------------------
SPECS["110"] = dict(
    gancho="""
Un contador que se incrementa. El objeto más pequeño posible, y el sitio donde estos doce lenguajes se
parten en dos mitades limpias: **siete tienen orientación a objetos y cinco de esos siete la
añadieron después de nacer**. Y el que la inventó está aquí: **Smalltalk no la añadió, la definió**,
y con ella el vocabulario —clase, instancia, método, mensaje, herencia— que usan todos los demás.
""",
    porque="""
Aquí el concepto es el **objeto: estado más comportamiento, con identidad**, y estos lenguajes lo
enseñan porque documentan las tres formas de llegar a él. **Smalltalk (1972)** lo tomó como axioma
único. **Ada 95, Fortran 2003, COBOL 2002, Pascal 1989 y Perl 1994** lo injertaron sobre un lenguaje
existente, y **cómo lo injertaron dice mucho de cada uno**: Ada con tipos etiquetados y operaciones
primitivas, Fortran con `contains` dentro del tipo, Perl con una referencia y una etiqueta.

Y **RPG, PL/I y M no lo tienen**, lo que no les ha impedido sostener sistemas de millones de líneas —
un dato incómodo que merece mirarse de frente.
""",
    cierre="""
Lo transferible: **lo que la orientación a objetos resuelve es añadir casos sin tocar el código
existente**, y todo lo demás —clases, herencia, encapsulación— es maquinaria para eso. Si tu problema
es añadir *operaciones* sobre un conjunto de casos cerrado, los objetos te estorban y un tipo suma con
emparejamiento exhaustivo (clase 100) es más simple. Elegir mal cuesta caro en las dos direcciones, y
la pregunta que lo decide es una sola: **¿qué va a crecer, los casos o las operaciones?**
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. OOCONT.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA  PIC X(80).
01  N      PIC S9(9) COMP-3.
01  I      PIC S9(9) COMP-3.
01  CONTADOR-OBJ.
    05  CUENTA  PIC 9(9) COMP VALUE 0.
01  ED-C   PIC Z(8)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    COMPUTE N = FUNCTION NUMVAL(LINEA)

    PERFORM VARYING I FROM 1 BY 1 UNTIL I > N
        PERFORM INCREMENTAR
    END-PERFORM

    MOVE CUENTA TO ED-C
    DISPLAY "cuenta=" FUNCTION TRIM(ED-C)
    STOP RUN.

INCREMENTAR.
    ADD 1 TO CUENTA.
""", """
**Lo que esta clase enseña en COBOL.** Este programa es COBOL procedimental porque es lo que se
encuentra en producción, y sirve para señalar lo que sí tiene el lenguaje: **el grupo `01` con sus
párrafos es un objeto sin clase** — estado agrupado y operaciones que lo manipulan, unidos solo por
convención.

**Y COBOL orientado a objetos existe desde el estándar de 2002**, completo:

```cobol
CLASS-ID. Contador INHERITS FROM Base.
ENVIRONMENT DIVISION.
CONFIGURATION SECTION.
REPOSITORY.
    CLASS Base INTRINSIC.

OBJECT.
DATA DIVISION.
WORKING-STORAGE SECTION.
01  CUENTA  PIC 9(9) COMP VALUE 0.

PROCEDURE DIVISION.

METHOD-ID. Incrementar.
PROCEDURE DIVISION.
    ADD 1 TO CUENTA.
END METHOD Incrementar.

METHOD-ID. Valor.
DATA DIVISION.
LINKAGE SECTION.
01  RESULTADO PIC 9(9) COMP.
PROCEDURE DIVISION RETURNING RESULTADO.
    MOVE CUENTA TO RESULTADO.
END METHOD Valor.

END OBJECT.
END CLASS Contador.
```

Y el uso:

```cobol
01  C  USAGE OBJECT REFERENCE Contador.
INVOKE Contador "New" RETURNING C
INVOKE C "Incrementar"
```

Está todo: clases, herencia simple, interfaces, métodos de instancia y de clase, polimorfismo,
`SELF`, `SUPER` y referencias a objeto tipadas. Existe en IBM Enterprise COBOL, Micro Focus y
parcialmente en GnuCOBOL.

**Y casi nadie lo usa.** La razón no es la sintaxis, aunque sea verbosa: es la de la clase 099. **El
trabajo del código COBOL es transformar registros**, y para eso el `01` de 1959 es la herramienta
adecuada. La orientación a objetos resuelve "añadir casos sin tocar lo existente", y un programa de
nóminas no añade tipos de nómina: **procesa los mismos registros con reglas que cambian**.

Donde sí encaja es en la frontera: la interoperabilidad con Java. IBM Enterprise COBOL permite que una
clase COBOL **herede de una clase Java** y viceversa, con lo que un programa COBOL puede implementar
una interfaz Java y participar en un marco de aplicaciones moderno.

Es otra vez la modernización por los bordes de la clase 105.
"""),
        "fortran": ("""
module contadorm
   implicit none

   type :: contador
      integer, private :: cuenta = 0        ! estado PRIVADO (clase 087)
   contains
      procedure :: incrementar               ! MÉTODOS, dentro del tipo
      procedure :: valor
   end type contador

contains

   subroutine incrementar(self)
      class(contador), intent(inout) :: self
      self%cuenta = self%cuenta + 1
   end subroutine incrementar

   function valor(self) result(r)
      class(contador), intent(in) :: self
      integer :: r
      r = self%cuenta
   end function valor

end module contadorm


program oo
   use contadorm
   implicit none

   type(contador) :: c
   integer :: n, i

   read(*, *) n

   do i = 1, n
      call c%incrementar()
   end do

   write(*, '(A,I0)') 'cuenta=', c%valor()
end program oo
""", """
**Lo que esta clase enseña en Fortran.** `c%incrementar()` es un **procedimiento ligado al tipo**, y
llegó con **Fortran 2003**: cuarenta y seis años después de la primera versión del lenguaje.

Las piezas del modelo de objetos de Fortran, con sus nombres propios:

```fortran
type, extends(base) :: derivado          ! HERENCIA (simple)
type, abstract :: figura                  ! tipo ABSTRACTO
   procedure(iface), deferred :: area      ! método abstracto
class(figura), allocatable :: f            ! variable POLIMÓRFICA
select type (f)                             ! despacho explícito (clase 100)
   type is (circulo) ...
   class is (poligono) ...
end select
procedure(iface), pointer, nopass :: cb     ! puntero a procedimiento como campo
generic :: operator(+) => sumar             ! sobrecarga de operadores
final :: limpiar                             ! destructor (clase 103)
```

Y la distinción entre `type(t)` y `class(t)` es la clave, ya apuntada en la clase 099: **`type` es
exactamente ese tipo; `class` es ese tipo o cualquier descendiente**, y solo `class` despacha
dinámicamente.

Lo que hace interesante esta clase en Fortran es **por qué** se añadió todo eso, porque no fue por
moda. Los códigos de simulación grandes tenían un problema concreto: **un solver que debe funcionar
con varios modelos físicos**.

```fortran
class(modelo), allocatable :: fisica
select case (config)
case ('newtoniano');  allocate(modelo_newton :: fisica)
case ('viscoelastico'); allocate(modelo_visco :: fisica)
end select

call resolver(fisica)         ! el solver no sabe cuál es
```

Antes de 2003, eso se hacía con **un entero de tipo y un `select case` en cada punto del código** —
exactamente el problema que la orientación a objetos resuelve. Añadir un modelo obligaba a tocar
veinte sitios.

Con `class`, añadir un modelo es escribir un tipo nuevo. Es el argumento del cierre de esta clase, en
su caso de uso más legítimo: **lo que crece son los casos**, no las operaciones.

Y `private` en un componente del tipo da encapsulación real (clase 087), algo que el Fortran de los
`COMMON` no podía ni plantearse.
"""),
        "ada": ("""
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Oo is
   type Contador is tagged record        --  TAGGED: lleva su tipo en ejecución
      Cuenta : Natural := 0;
   end record;

   --  Operaciones PRIMITIVAS: subprogramas cuyo primer parámetro es del tipo
   procedure Incrementar (C : in out Contador) is
   begin
      C.Cuenta := C.Cuenta + 1;
   end Incrementar;

   function Valor (C : Contador) return Natural is (C.Cuenta);

   C : Contador;
   N : Integer;
begin
   Get (N);

   for I in 1 .. N loop
      Incrementar (C);
   end loop;

   Put ("cuenta=");
   Put (Valor (C), Width => 1);
   New_Line;
end Oo;
""", """
**Lo que esta clase enseña en Ada.** Ada 95 añadió la orientación a objetos con una decisión de diseño
que la separa de todas las demás de esta página: **los métodos no van dentro del tipo**.

```ada
type Contador is tagged record ... end record;

procedure Incrementar (C : in out Contador);     --  operación PRIMITIVA
function Valor (C : Contador) return Natural;     --  también
```

Una **operación primitiva** es un subprograma declarado en el mismo ámbito que el tipo y con un
parámetro de ese tipo. No hay bloque `class { ... }` que las contenga.

Eso tiene tres consecuencias buenas:

1. **Se pueden añadir operaciones sin tocar la declaración del tipo** — el otro lado del *expression
   problem* de la clase 100, que las jerarquías cerradas no permiten.
2. **No hay asimetría entre método y función libre.** En C++ hay que decidir si algo es `a.f(b)` o
   `f(a, b)`, y esa decisión afecta a quién puede extenderlo. En Ada no existe la disyuntiva.
3. **El despacho múltiple es natural**: una operación con dos parámetros del tipo etiquetado despacha
   por los dos.

Ada 2005 añadió la **notación de prefijo** para quien la eche de menos:

```ada
C.Incrementar;          --  exactamente lo mismo que Incrementar (C)
```

Es azúcar sintáctico puro, y su llegada tardía dice que la comunidad no lo consideraba necesario.

El resto del modelo se completó en 2005 con lo que faltaba:

```ada
type Dibujable is interface;                       --  INTERFACES, 2005
procedure Dibujar (D : Dibujable) is abstract;

type Figura is new Objeto and Dibujable with ...   --  herencia simple + interfaces
overriding procedure Dibujar (F : Figura);          --  OVERRIDING explícito
```

**`overriding` es obligatorio declararlo si se quiere**, y `not overriding` para lo contrario. Si
crees que estás redefiniendo un método y te equivocas en la firma, **no compila** — el error que en
Java necesitó la anotación `@Override` y que en C++ esperó a `override` en C++11.

Ada lo tuvo en 2005, y es coherente con todo lo demás del lenguaje: **decir la intención y dejar que
el compilador la compruebe**.
"""),
        "pascal": ("""
program Oo;
{$MODE OBJFPC}{$H+}
uses SysUtils;

type
  TContador = class
  private
    FCuenta: Integer;
  public
    procedure Incrementar;
    property Cuenta: Integer read FCuenta;    { propiedad de SOLO LECTURA }
  end;

procedure TContador.Incrementar;
begin
  Inc(FCuenta);
end;

var
  C: TContador;
  N, I: Integer;

begin
  Read(N);

  C := TContador.Create;
  try
    for I := 1 to N do
      C.Incrementar;
    WriteLn('cuenta=', IntToStr(C.Cuenta));
  finally
    C.Free;
  end;
end.
""", """
**Lo que esta clase enseña en Pascal.** Object Pascal tiene **tres modelos de objeto conviviendo**, y
esa acumulación es su historia:

```pascal
type
  TVieja = object ... end;        { Turbo Pascal 5.5, 1989: VALOR con herencia }
  TNueva = class ... end;          { Delphi 1, 1995: REFERENCIA, con Create/Free }
  INueva = interface ... end;       { Delphi 3: contadas por referencia (clase 103) }
```

La de 1989 está obsoleta, la de 1995 es la normal y las interfaces son el mecanismo de gestión
automática.

Y **la aportación de Delphi al modelo de objetos es la `property`**, que este programa usa:

```pascal
property Cuenta: Integer read FCuenta;                      { solo lectura }
property Nombre: string read FNombre write SetNombre;        { con SETTER }
property Items[I: Integer]: TItem read GetItem; default;      { INDEXADA }
```

Una propiedad **se usa como un campo y se implementa como métodos**. `C.Cuenta` parece acceso directo
y puede ser una llamada a un `getter` con validación, notificación de cambios o carga perezosa. Y se
puede cambiar de campo a método **sin tocar el código que la usa**.

Eso es exactamente lo que en Java exige escribir `getCuenta()` y `setCuenta()` a mano, y lo que C#
copió con su misma sintaxis —y con el mismo autor detrás, Anders Hejlsberg (clase 073)—.

Object Pascal tiene además otras dos piezas propias:

**`class of`**, las referencias de clase:

```pascal
type TClaseContador = class of TContador;
var K: TClaseContador;
begin
  K := TContadorEspecial;
  C := K.Create;              { instanciar una clase decidida en EJECUCIÓN }
end;
```

Con eso se construyen fábricas y sistemas de registro de clases sin reflexión, y es la base del
mecanismo de carga de formularios de Delphi.

**Y los mensajes**, que son puro Windows:

```pascal
procedure WMPaint(var Msg: TWMPaint); message WM_PAINT;
```

Un método asociado a un número de mensaje, despachado en ejecución. Es un vestigio de la programación
Win32 integrado en el lenguaje, y muestra hasta qué punto Delphi se diseñó para una plataforma
concreta.
"""),
        "lisp": ("""
(defclass contador ()
  ((cuenta :initform 0 :accessor cuenta)))

(defmethod incrementar ((c contador))
  (incf (cuenta c)))

(let ((c (make-instance 'contador))
      (n (read)))
  (dotimes (i n)
    (incrementar c))
  (format t "cuenta=~D~%" (cuenta c)))
""", """
**Lo que esta clase enseña en Common Lisp.** **CLOS es el sistema de objetos más potente de esta
página**, y su diferencia central con todos los demás cabe en una frase: **los métodos no pertenecen a
las clases**.

```lisp
(defgeneric colisiona (a b))
(defmethod colisiona ((a nave) (b asteroide)) ...)
(defmethod colisiona ((a nave) (b nave)) ...)
(defmethod colisiona ((a asteroide) (b asteroide)) ...)
```

Eso es **despacho múltiple**: el método se elige por los tipos de **todos** los argumentos. En Java,
C++ o Smalltalk, `a.colisiona(b)` solo despacha por `a`, y resolver el otro tipo exige el patrón
Visitante o una cadena de comprobaciones.

Y CLOS tiene una segunda idea igual de importante: **la combinación de métodos**.

```lisp
(defmethod guardar :before ((c cuenta)) (validar c))
(defmethod guardar ((c cuenta)) (escribir c))
(defmethod guardar :after ((c cuenta)) (registrar c))
(defmethod guardar :around ((c cuenta)) (con-transaccion (call-next-method)))
```

`:before`, `:after` y `:around` **envuelven** el método principal, y `call-next-method` invoca al
siguiente. **La clase base no tiene que prever nada**: cualquiera puede añadir un `:around` desde
otro fichero.

Eso es programación orientada a aspectos —registro de trazas, transacciones, seguridad, cachés
añadidos sin tocar el código— y CLOS lo tenía en 1988, trece años antes de que AspectJ le pusiera
nombre.

Y hay una tercera capa que casi ningún lenguaje ofrece: **el protocolo de metaobjetos (MOP)**.

```lisp
(defclass mi-metaclase (standard-class) ())
(defmethod compute-slots ((c mi-metaclase)) ...)
```

**El propio sistema de objetos está implementado con objetos, y se puede modificar.** Cambiar cómo se
calculan los campos, cómo se despachan los métodos o cómo se heredan las clases es escribir métodos
sobre las metaclases. Con eso se han construido sistemas de persistencia, comprobación de tipos y
objetos remotos **sin tocar el compilador**.

*The Art of the Metaobject Protocol* (Kiczales, 1991) es el libro que lo explica, y su autor fundó
después el proyecto AspectJ. La línea es directa.
"""),
        "tcl": ("""
oo::class create Contador {
    variable cuenta
    constructor {} { set cuenta 0 }
    method incrementar {} { incr cuenta }
    method valor {} { return $cuenta }
}

gets stdin linea
set n [string trim $linea]

set c [Contador new]
for {set i 0} {$i < $n} {incr i} {
    $c incrementar
}

puts "cuenta=[$c valor]"
""", """
**Lo que esta clase enseña en Tcl.** **TclOO entró en el núcleo en Tcl 8.6 (2012)**, veinticuatro años
después del lenguaje, y su diseño refleja esa espera: recogió lo mejor de las bibliotecas que la
comunidad llevaba usando —incr Tcl, XOTcl, Snit— y del modelo de CLOS.

Lo primero que hay que entender ya se dijo en la clase 099: **un objeto es un comando**, así que
`$c incrementar` es invocar el comando `$c` con el argumento `incrementar`. No hay sintaxis nueva.

Y de ahí sale lo característico de TclOO: **todo se puede cambiar en ejecución**.

```tcl
oo::define Contador method reiniciar {} { set cuenta 0 }   ;# añadir un método AHORA
oo::define Contador superclass Base                          ;# CAMBIAR la superclase
oo::objdefine $c method especial {} { ... }                   ;# método para ESTE objeto
oo::define Contador mixin Registrable                          ;# mezclar comportamiento
oo::define Contador filter trazar                               ;# interceptar TODAS las llamadas
```

Los objetos existentes **ven los cambios inmediatamente**. Es el modelo de Smalltalk, y no es
casualidad: la propuesta de TclOO cita a Smalltalk y a CLOS explícitamente.

Tres de esas líneas merecen destacarse:

- **`objdefine`** da métodos por objeto, que es programación **basada en prototipos** (clase 113)
  dentro de un sistema de clases. Muy pocos lenguajes ofrecen los dos modelos.
- **`mixin`** compone comportamiento sin herencia, y se puede añadir y quitar en caliente.
- **`filter`** intercepta cualquier envío de mensaje al objeto, que es el `:around` de CLOS y la base
  de proxies, auditoría y objetos remotos.

Y hay una decisión de diseño deliberada y poco común: **TclOO no impone un modelo de clases
concreto**. Es un **marco para construir sistemas de objetos**, y sobre él se han reimplementado incr
Tcl y otros. La biblioteca no dice cómo debe ser tu orientación a objetos: da las piezas.

Es la misma filosofía que el MOP de CLOS, en un lenguaje de guion.
"""),
        "perl": ("""
use strict;
use warnings;

package Contador;
sub new         { my $clase = shift; return bless { cuenta => 0 }, $clase }
sub incrementar { $_[0]{cuenta}++ }
sub valor       { return $_[0]{cuenta} }

package main;

my $n = <STDIN>;
chomp $n;

my $c = Contador->new;
$c->incrementar for 1 .. $n;

print "cuenta=", $c->valor, "\\n";
""", """
**Lo que esta clase enseña en Perl.** El modelo de objetos de Perl 5 es **el más minimalista que se ha
puesto en producción**, y consiste en tres reglas:

1. **Un objeto es una referencia** —normalmente a un hash— **con una etiqueta de paquete**, puesta
   con `bless`.
2. **Un método es una subrutina del paquete**, que recibe el objeto como primer argumento.
3. **`->` busca el método** en el paquete y, si no está, en `@ISA` recursivamente.

Eso es todo. **No hay palabra clave `class`, ni `method`, ni declaración de campos, ni constructor
predefinido.** `new` es una subrutina normal, llamada así por convención.

Larry Wall lo diseñó así en 1994 con un objetivo explícito: **añadir objetos sin cambiar el
lenguaje**, reutilizando paquetes, referencias y la tabla de símbolos que ya existían. Y funcionó: la
orientación a objetos llegó a Perl **sin romper nada**.

El precio es el que se vio en la clase 087: **sin campos declarados, sin privacidad y sin
comprobación**. `$obj->{cuenta}` funciona desde cualquier sitio, y escribir mal el nombre de un campo
lo crea en silencio.

De ahí las tres generaciones de respuestas:

```perl
use Moose;     # 2006: roles, tipos, modificadores before/after/around de CLOS
use Moo;        # ligero, compatible
use Object::Pad; # el prototipo de la sintaxis nativa

use v5.38; use experimental 'class';
class Contador {
    field $cuenta = 0;                 # campo LÉXICO: privado de verdad
    method incrementar { $cuenta++ }
    method valor { return $cuenta }
}
```

**Moose** merece la mención: trajo a Perl los **roles** —composición horizontal sin herencia, lo que
en Rust son los *traits* y en Scala los *traits*— y los modificadores `before`/`after`/`around`
tomados directamente de CLOS. Su documentación cita a CLOS y a Perl 6 como fuentes.

Y la palabra clave `class` nativa, experimental desde 5.38 (2023), es el cierre de un círculo de
treinta años. Su rasgo decisivo es que **los `field` son variables léxicas**, así que la
encapsulación por fin es real y no una convención.
"""),
        "cpp": ("""
#include <iostream>

class Contador {
    int cuenta_ = 0;                 // privado por defecto en una class
public:
    void incrementar() { ++cuenta_; }
    int  valor() const { return cuenta_; }
};

int main() {
    int n{};
    if (!(std::cin >> n)) return 1;

    Contador c;
    for (int i = 0; i < n; ++i) {
        c.incrementar();
    }

    std::cout << "cuenta=" << c.valor() << '\\n';
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** C++ nació en 1979 como *C with Classes*, y su modelo de objetos
está construido sobre una restricción que lo explica todo: **no pagar por lo que no usas**.

De ahí la decisión que lo separa de Java, Smalltalk y casi todos: **el despacho dinámico es
opcional**.

```cpp
class A { void f(); };            // llamada DIRECTA: sin coste, se puede integrar en línea
class B { virtual void f(); };     // llamada INDIRECTA por la vtable
```

Un objeto sin métodos virtuales **ocupa exactamente lo que sus campos** y sus llamadas son directas.
Añadir un `virtual` mete un puntero a la tabla de métodos en cada instancia y una indirección en cada
llamada.

Esa elección es la razón de que `std::vector<Punto>` sea tan compacto como un arreglo de C, y es lo
que hace a C++ viable en sistemas empotrados y en núcleos de sistema operativo.

El precio es el que ya apareció en la clase 099: **el *slicing***.

```cpp
Derivada d;
Base b = d;          // ¡TRUNCA los campos de Derivada!
Base& r = d;          // correcto: referencia, sin cortar
```

Copiar un derivado en una variable del tipo base **descarta lo añadido**, en silencio. Es la
consecuencia directa de tener objetos con semántica de valor y herencia a la vez, y es lo que llevó a
Pascal, C#, Swift y Rust a separar los dos modelos.

C++ añade además dos cosas que casi ningún lenguaje de esta página tiene:

**Herencia múltiple**, con el problema del diamante y su solución:

```cpp
class D : public virtual B { };       // herencia VIRTUAL: una sola copia de B
```

**Y polimorfismo estático con plantillas**, que da despacho sin coste:

```cpp
template <typename T> void usar(T& x) { x.incrementar(); }   // se resuelve al COMPILAR
```

Ese segundo camino —**duck typing comprobado en compilación**— es a menudo mejor que la herencia en
C++ moderno, y con los **conceptos** de C++20 los requisitos por fin se pueden escribir y comprobar:

```cpp
template <typename T>
concept Contable = requires(T x) { x.incrementar(); { x.valor() } -> std::integral; };
```
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi OOCONT;
  n int(10) const;
end-pi;

// RPG no tiene objetos: una estructura de datos y procedimientos que la usan
dcl-ds contador qualified;
  cuenta int(10) inz(0);
end-ds;

dcl-s i int(10);

for i = 1 to n;
  incrementar(contador);
endfor;

dsply ('cuenta=' + %char(contador.cuenta));

*inlr = *on;
return;

dcl-proc incrementar;
  dcl-pi *n;
    c likeds(contador);         // recibe la estructura POR REFERENCIA
  end-pi;
  c.cuenta += 1;
end-proc;
""", """
**Lo que esta clase enseña en RPG.** **RPG no tiene orientación a objetos**, y es uno de los tres
lenguajes de esta página —con PL/I y M— de los que se puede decir sin matices.

Lo que tiene es el patrón de este programa: **una estructura de datos más procedimientos que la
reciben**, con **`likeds`** para declarar un parámetro con la forma de otra estructura.

```rpgle
dcl-pi *n;
  c likeds(contador);        // "de la misma forma que `contador`"
end-pi;
```

Es exactamente el `self` explícito de C, de Go y de Rust: **el objeto es un parámetro, no un
receptor**. Y con los procedimientos exportables o privados de un módulo (clase 087), se consigue
encapsulación real: **el estado en variables globales del módulo, y solo los procedimientos
exportados lo tocan**.

Ese patrón —módulo con estado privado y procedimientos de acceso— es, como se dijo en la clase 083,
**un objeto con un solo ejemplar**. Para varios ejemplares, se pasa la estructura.

Y cuando de verdad hacen falta objetos, IBM dio la salida en 2001 y es la que se usa: **llamar a Java
directamente desde RPG**.

```rpgle
dcl-pr crearLista object(*java : 'java.util.ArrayList')
       extproc(*java : 'java.util.ArrayList' : *constructor);
end-pr;

dcl-pr anadir ind
       extproc(*java : 'java.util.ArrayList' : 'add');
  elemento object(*java : 'java.lang.Object') const;
end-pr;

dcl-s lista object(*java : 'java.util.ArrayList');
lista = crearLista();
```

**`object(*java : ...)`** es un tipo de dato de RPG que contiene una referencia a un objeto Java, y
`extproc(*java : ...)` declara un método. La JVM corre en el mismo trabajo, y RPG instancia clases,
llama a métodos y recibe objetos.

Un lenguaje de 1959 haciendo `new ArrayList()` es la imagen que mejor resume esta sección del curso:
**no hizo falta que RPG tuviera objetos, hizo falta que pudiera hablar con quien los tiene**.
"""),
        "pli": ("""
 oo: procedure options(main);

    /*  PL/I no tiene objetos: una estructura y procedimientos que la usan.  */
    declare 1 contador,
              2 cuenta fixed binary(31) initial(0);

    declare (n, i) fixed binary(31);

    get list (n);

    do i = 1 to n;
       call incrementar;
    end;

    put skip list ('cuenta=' || trim(char(contador.cuenta)));

 incrementar: procedure;
    contador.cuenta = contador.cuenta + 1;    /* ve `contador` por anidamiento */
 end incrementar;

 end oo;
""", """
**Lo que esta clase enseña en PL/I.** **PL/I nunca añadió orientación a objetos**, y ya se explicó por
qué en la clase 099: es una cuestión de calendario. El lenguaje dejó de evolucionar en los años
ochenta, justo cuando la orientación a objetos se generalizaba, y no hubo comité que lo llevara a los
noventa.

Lo que sí tiene es todo lo necesario para construirla a mano, y merece verse porque es exactamente lo
que hacía la gente en C antes de C++:

```pli
 declare 1 objeto based(p),
           2 datos,
             3 cuenta fixed binary(31),
           2 metodos,
             3 incrementar entry variable,     /* PUNTEROS a procedimiento */
             3 valor entry variable returns (fixed binary(31));

 allocate objeto set(p);
 p -> incrementar = inc_contador;               /* rellenar la "vtable" */
 call p -> incrementar;                          /* despacho DINÁMICO */
```

Eso es una tabla de métodos virtuales escrita a mano, con las **variables `entry`** de la clase 085 y
las estructuras `based` de la clase 090. Es exactamente lo que hace el compilador de C++ por debajo, y
lo que hacen los desarrolladores del núcleo de Linux con estructuras de punteros a función.

**PL/I tenía todas las piezas en 1964 y le faltó la sintaxis que las juntara.**

Y esta clase es buen sitio para una observación que evita la caricatura: **no tener objetos no es una
condena**. El código PL/I que sigue en producción —sistemas de reservas aéreas, banca, seguros— es
código de transformación de datos, igual que el COBOL, y para eso los objetos aportan poco.

La modernización de PL/I ha ido, como se dijo en la clase 105, por el camino de la interoperabilidad:
soporte de XML, llamadas a Java y a C, Unicode con `widechar`, y **z/OS Connect** para exponerse como
API REST sin tocar el código.

Es la modernización mínima de esta página, y también es la que su público pedía: **que siga
compilando lo de 1975**.
"""),
        "mumps": ("""
OOCONT ; Orientado a objetos -- clase 110
 read n
 new contador
 set contador("cuenta") = 0
 for i=1:1:n do incrementar(.contador)
 write "cuenta=", contador("cuenta"), !
 quit
 ;
incrementar(c) ; recibe el "objeto" POR REFERENCIA (el punto en la llamada)
 set c("cuenta") = c("cuenta") + 1
 quit
""", """
**Lo que esta clase enseña en M.** **M no tiene objetos**, y lo que hace este programa es lo idiomático
del lenguaje: **un array local con subíndices de texto como campos**, pasado por referencia con el
punto de la clase 109.

```mumps
 set contador("cuenta") = 0
 do incrementar(.contador)
```

Eso es un objeto sin clase: estado con nombres de campo, y rutinas que lo manipulan. Sin
encapsulación, sin tipos y sin comprobación — pero con una ventaja que ningún otro objeto de esta
página tiene: **poniéndole `^` delante, el objeto está en disco**.

```mumps
 set ^CONTADOR(id, "cuenta") = 0
```

Ese "objeto" es persistente, transaccional y compartido entre procesos, sin serializar y sin capa de
persistencia (clases 095 y 106).

Y aquí está la modernización más ambiciosa de esta página, ya apuntada en las clases 099 y 105:
**InterSystems ObjectScript**, descendiente directo de M, **sí tiene orientación a objetos completa**:

```objectscript
Class Ejemplo.Contador Extends %Persistent
{
Property Cuenta As %Integer [ InitialExpression = 0 ];

Method Incrementar()
{
    Set ..Cuenta = ..Cuenta + 1
}
}
```

Clases, herencia múltiple, propiedades con `getter` y `setter`, métodos, `try/catch`, colecciones,
`%JSON.Adaptor`... y **`%Persistent`**, que es lo decisivo: una clase que hereda de `%Persistent`
**se guarda automáticamente en *globals***, y **los mismos datos se consultan a la vez como objetos,
como tablas SQL y como *globals***.

```objectscript
Set obj = ##class(Ejemplo.Contador).%New()
Do obj.%Save()
// y en SQL:  SELECT Cuenta FROM Ejemplo.Contador
// y en M:    write ^Ejemplo.ContadorD(1)
```

**Tres vistas del mismo dato, sin conversión y sin mapeo.** El problema de la impedancia
objeto-relacional —la brecha entre el modelo de objetos y el de tablas, que generó ORMs enteros— aquí
simplemente **no existe**, porque no hay dos almacenamientos.

Es, con diferencia, el ejemplo más fuerte de esta sección sobre lo que significa "actualizado para
resolver problemas actuales".
"""),
        "smalltalk": ("""
| n c |

n := stdin nextLine trimBoth asNumber.

"Contador es una clase del sistema; aquí basta con un objeto con estado"
c := 0.
n timesRepeat: [ c := c + 1 ].

Transcript show: 'cuenta=', c printString; cr.
""", """
**Lo que esta clase enseña en Smalltalk.** Esta es la clase de Smalltalk, y merece decirlo sin rodeos:
**Smalltalk no implementa la orientación a objetos, la DEFINE**.

La versión con clase se escribe así:

```smalltalk
Object subclass: #Contador
    instanceVariableNames: 'cuenta'
    classVariableNames: ''
    package: 'Ejemplo'.

Contador >> initialize   cuenta := 0
Contador >> incrementar  cuenta := cuenta + 1
Contador >> cuenta       ^cuenta

c := Contador new.
n timesRepeat: [ c incrementar ].
```

Y lo que hay debajo son **cinco propiedades que ningún otro lenguaje de esta página reúne**:

1. **Todo es un objeto.** Los números, los booleanos, `nil`, los bloques, **las clases** y las
   metaclases.
2. **Lo único que ocurre es el envío de mensajes.** No hay operadores, no hay sentencias de control y
   no hay declaraciones (clase 108).
3. **Las clases son objetos.** `Contador class` es la metaclase, que también es un objeto con su
   clase. La torre termina en `Metaclass`, que es instancia de sí misma.
4. **El sistema es reflexivo por completo.** Se puede preguntar a cualquier objeto por su clase, sus
   variables, sus métodos y su código fuente, y modificarlo todo en marcha (clase 098).
5. **No hay compilación separada del entorno.** Se programa **dentro** del sistema vivo.

`Object subclass: #Contador ...` es un **mensaje enviado a la clase `Object`** que devuelve una clase
nueva. Crear una clase es una operación normal de ejecución, y por eso se pueden generar clases
mediante programa.

Y esta clase cierra con la observación de Alan Kay que ya apareció en la 107, porque aquí es donde
tiene todo su sentido: dijo que lamentaba el término *orientado a objetos*, porque **lo importante
nunca fueron los objetos sino el paso de mensajes y el ocultamiento total del estado**.

Su modelo mental eran **células biológicas y ordenadores en red**: entidades autónomas que solo se
comunican por mensajes y de las que nadie puede ver el interior. Lo que la industria copió fue
"clases con campos y métodos" — que es la parte fácil y la menos importante.

Los sistemas que sí heredaron la idea completa no son los lenguajes: son **Erlang con sus procesos** y
**los microservicios**.
"""),
    },
)
