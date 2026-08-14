# -*- coding: utf-8 -*-
"""Parte 7, lote E — clase 111. Ver `vivos_parte7.py` y `gen_vivos.py`."""

SPECS: dict[str, dict] = {}

# ---------------------------------------------------------------------------
# 111 — Herencia, composición y polimorfismo
# ---------------------------------------------------------------------------
SPECS["111"] = dict(
    gancho="""
Tres animales y un sonido cada uno. Es el ejemplo canónico del polimorfismo, y aquí sirve para algo
más: **seis de estos doce lenguajes lo resuelven con despacho dinámico de verdad** —Fortran 2003, Ada
95, Pascal, Lisp, Tcl, C++ y Smalltalk— y los otros lo resuelven con un `EVALUATE` sobre una etiqueta.
Ver los dos lado a lado deja claro qué se gana exactamente, que no es elegancia.
""",
    porque="""
Aquí el concepto es el **despacho según el tipo en ejecución**, y estos lenguajes lo enseñan porque
enseñan su coste. **C++** lo hace opcional con `virtual` y cobra una indirección; **Ada** lo hace solo
sobre tipos etiquetados y con `overriding` comprobado; **Fortran** lo hace con `class` y `deferred`, y
lo añadió en 2003 porque los solvers lo necesitaban (clase 110); **Lisp** lo hace por **todos** los
argumentos a la vez.

Y **COBOL, RPG, PL/I y M** enseñan lo otro: qué pasa cuando no lo tienes. La respuesta es un `select`
que hay que actualizar en cada sitio donde aparezca, y en un sistema de un millón de líneas eso tiene
un nombre — **deuda**.
""",
    cierre="""
Lo transferible: **la herencia es la peor de las tres herramientas del título y la que más se usa**. La
composición —tener un objeto en lugar de heredar de él— da lo mismo con menos acoplamiento; las
interfaces (clase 112) dan el polimorfismo sin la herencia. La herencia de implementación solo se
justifica cuando el descendiente **es** realmente un caso del ancestro y **puede sustituirlo en
cualquier sitio** — el principio de sustitución de Liskov. Cuando dudes, compón: es reversible, y la
herencia no.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. POLI.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  TIPO    PIC X(10).
01  SONIDO  PIC X(10).

PROCEDURE DIVISION.
    ACCEPT LINEA
    MOVE FUNCTION TRIM(LINEA) TO TIPO

    EVALUATE TIPO
        WHEN "perro"  MOVE "guau" TO SONIDO
        WHEN "gato"   MOVE "miau" TO SONIDO
        WHEN "vaca"   MOVE "muu"  TO SONIDO
        WHEN OTHER    MOVE "?"    TO SONIDO
    END-EVALUATE

    DISPLAY "sonido=" FUNCTION TRIM(SONIDO)
    STOP RUN.
""", """
**Lo que esta clase enseña en COBOL.** Este `EVALUATE` es exactamente lo que el cierre de la clase 110
llamaba el otro lado del problema: **funciona, y hay que repetirlo en cada sitio donde el
comportamiento dependa del tipo**.

En un sistema real, ese mismo `EVALUATE` sobre `TIPO-CLIENTE` o `CODIGO-PRODUCTO` aparece en cuarenta
programas distintos. Añadir un tipo nuevo obliga a **encontrarlos todos**, y no hay compilador que
avise de los que faltan.

La solución que la práctica COBOL desarrolló para esto no es la orientación a objetos: es la **tabla
de despacho** de la clase 085, con `CALL` dinámico.

```cobol
01  NOMBRE-PROGRAMA  PIC X(8).
...
MOVE TABLA-PROGRAMA(INDICE) TO NOMBRE-PROGRAMA
CALL NOMBRE-PROGRAMA USING DATOS
    ON EXCEPTION DISPLAY "sin implementación para " TIPO
END-CALL
```

Con una tabla en base de datos que asocia cada código a un nombre de programa, **añadir un tipo es
insertar una fila y compilar un programa nuevo**. No hay que tocar ni recompilar nada existente.

Eso es exactamente lo que resuelve el polimorfismo, conseguido con las herramientas de 1968. Y tiene
las mismas ventajas y los mismos riesgos: máxima flexibilidad, **y nadie comprueba que el programa
exista ni que su firma encaje** hasta que se ejecuta.

Y sobre la herencia, COBOL orientado a objetos (clase 110) la tiene con una decisión notable:
**herencia simple, con interfaces múltiples**, igual que Java.

```cobol
CLASS-ID. Perro INHERITS FROM Animal IMPLEMENTS Sonoro.
METHOD-ID. Sonido OVERRIDE.
```

La palabra **`OVERRIDE`** es obligatoria y comprobada, como en Ada 2005 y C++11. Es un acierto de
diseño en un estándar de 2002, cuando Java todavía lo resolvía con una anotación opcional.
"""),
        "fortran": ("""
module animales
   implicit none

   type, abstract :: animal
   contains
      procedure(sonido_i), deferred :: sonido      ! método ABSTRACTO
   end type animal

   abstract interface
      function sonido_i(self) result(s)
         import :: animal
         class(animal), intent(in) :: self
         character(len=10) :: s
      end function sonido_i
   end interface

   type, extends(animal) :: perro
   contains
      procedure :: sonido => sonido_perro
   end type perro

   type, extends(animal) :: gato
   contains
      procedure :: sonido => sonido_gato
   end type gato

   type, extends(animal) :: vaca
   contains
      procedure :: sonido => sonido_vaca
   end type vaca

contains

   function sonido_perro(self) result(s)
      class(perro), intent(in) :: self
      character(len=10) :: s
      s = 'guau'
   end function sonido_perro

   function sonido_gato(self) result(s)
      class(gato), intent(in) :: self
      character(len=10) :: s
      s = 'miau'
   end function sonido_gato

   function sonido_vaca(self) result(s)
      class(vaca), intent(in) :: self
      character(len=10) :: s
      s = 'muu'
   end function sonido_vaca

end module animales


program poli
   use animales
   implicit none

   class(animal), allocatable :: a          ! variable POLIMÓRFICA
   character(len=20) :: tipo

   read(*, *) tipo

   select case (trim(tipo))
   case ('perro');  allocate(perro :: a)
   case ('gato');   allocate(gato  :: a)
   case default;    allocate(vaca  :: a)
   end select

   write(*, '(A)') 'sonido=' // trim(a%sonido())   ! despacho DINÁMICO
end program poli
""", """
**Lo que esta clase enseña en Fortran.** Este programa usa las cuatro piezas del modelo de objetos de
Fortran 2003, y cada una tiene su nombre:

```fortran
type, abstract :: animal                  ! no se puede instanciar
   procedure(iface), deferred :: sonido    ! método sin implementación
type, extends(animal) :: perro             ! HERENCIA
class(animal), allocatable :: a             ! variable polimórfica
allocate(perro :: a)                         ! reservar CON UN TIPO CONCRETO
```

`allocate(perro :: a)` merece atención: **reserva una variable polimórfica con un tipo dinámico
concreto**. Es la construcción de Fortran para "crear un objeto de esta clase" y su sintaxis con `::`
es propia del lenguaje.

Y `import :: animal` dentro de la interfaz abstracta es una peculiaridad que conviene explicar: **una
`interface` en Fortran es un ámbito cerrado**, que por defecto no ve los tipos del módulo que la
contiene. `import` los trae. Es el tipo de detalle que hace que el Fortran moderno tenga fama de
verboso.

Fortran tiene **herencia simple** —un solo `extends`— y **no tiene interfaces** en el sentido de Java.
Lo que hay es la composición manual:

```fortran
type :: coche
   type(motor) :: m               ! COMPOSICIÓN: un motor DENTRO
end type
```

Y una peculiaridad que la clase 087 anticipó: **cuando se hereda, el componente heredado es accesible
por su nombre de tipo padre**:

```fortran
type, extends(animal) :: perro
   integer :: raza
end type

p%animal      ! el "subobjeto padre", accesible como un componente
```

Ese acceso al ancestro como si fuera un campo es coherente con el hecho de que en Fortran **la
herencia es literalmente la inclusión del padre al principio del registro** — el mismo modelo de
memoria que usa C++ para la herencia simple.

Y `select type` (clase 100) es el complemento para cuando el despacho dinámico no basta y hay que
saber el tipo concreto — con la advertencia de siempre: **si aparece mucho `select type`, la jerarquía
está mal repartida**.
"""),
        "ada": ("""
with Ada.Text_IO; use Ada.Text_IO;

procedure Poli is

   --  La jerarquía va en un PAQUETE: solo así las operaciones despachan.
   package Animales is
      type Animal is abstract tagged null record;
      function Sonido (A : Animal) return String is abstract;

      type Perro is new Animal with null record;
      overriding function Sonido (A : Perro) return String;

      type Gato is new Animal with null record;
      overriding function Sonido (A : Gato) return String;

      type Vaca is new Animal with null record;
      overriding function Sonido (A : Vaca) return String;
   end Animales;

   package body Animales is
      overriding function Sonido (A : Perro) return String is ("guau");
      overriding function Sonido (A : Gato)  return String is ("miau");
      overriding function Sonido (A : Vaca)  return String is ("muu");
   end Animales;

   use Animales;

   type Ref is access all Animal'Class;      --  acceso a la CLASE ENTERA

   A      : Ref;
   Linea  : String (1 .. 100);
   Ultimo : Natural;
begin
   Get_Line (Linea, Ultimo);

   if Linea (1 .. Ultimo) = "perro" then
      A := new Perro;
   elsif Linea (1 .. Ultimo) = "gato" then
      A := new Gato;
   else
      A := new Vaca;
   end if;

   Put_Line ("sonido=" & Sonido (A.all));     --  llamada DESPACHADA
end Poli;
""", """
**Lo que esta clase enseña en Ada.** La pieza central es **`Animal'Class`**, y es una idea que ningún
otro lenguaje de esta página expresa igual de bien.

```ada
A : Animal;              --  EXACTAMENTE un Animal
B : Animal'Class;         --  Animal o CUALQUIER descendiente
C : access Animal'Class;   --  un acceso a cualquiera de ellos
```

**El tipo `T'Class` es un tipo real**, no una convención: se puede declarar, pasar como parámetro y
poner en un contenedor. Y la regla es tajante:

- Una llamada con un argumento de tipo `Animal` es **estática**: se sabe al compilar.
- Una llamada con un argumento de tipo `Animal'Class` es **despachada**: se decide en ejecución.

**El programador ve en el tipo si hay despacho dinámico**, sin buscar si el método es virtual. En C++
hay que ir a la declaración de la clase para saberlo; en Ada está en el sitio de la llamada.

Ada tiene **herencia simple** y añadió **interfaces** en 2005:

```ada
type Sonoro is interface;
function Sonido (S : Sonoro) return String is abstract;

type Perro is new Animal and Sonoro with null record;
```

Es el mismo modelo que Java y COBOL 2002: una implementación, muchas interfaces. La decisión de
evitar la herencia múltiple de implementación está documentada en la justificación del estándar, y el
motivo es el previsible: **la complejidad del diamante no compensa en un lenguaje pensado para
sistemas certificables**.

Y `overriding` explícito, ya mencionado en la clase 110, aquí se ve en acción: si el descendiente
escribe `Sonido` con otra firma, **`overriding` hace que no compile**. Sin esa palabra, sería una
sobrecarga nueva y el polimorfismo fallaría en silencio — que es exactamente lo que pasa en C++ sin
`override` y en Java sin `@Override`.

Ada 2012 añade además que **los contratos se heredan**: la precondición de un método redefinido **no
puede ser más fuerte** que la del padre, y la postcondición no puede ser más débil. Es el principio de
sustitución de Liskov **comprobado por el compilador**, y no lo hace ningún otro lenguaje de esta
página.

**Un tropiezo real de este programa.** La primera versión declaraba la jerarquía directamente en la
parte declarativa del procedimiento, y GNAT respondió:

```text
poli.adb:5:13: warning: not dispatching (must be defined in a package spec)
```

**Una operación primitiva solo despacha si se declara en la ESPECIFICACIÓN de un paquete.** Declarada
en el cuerpo de un subprograma, es una función normal con un parámetro de tipo etiquetado: el
compilador la resuelve estáticamente, y la llamada sobre `Animal'Class` no compila.

De ahí el `package Animales is ... end Animales;` anidado que lleva el programa.

La regla parece burocrática y tiene un motivo de fondo: **la tabla de despacho de un tipo se congela
al terminar la especificación donde se declara**. Si se pudieran añadir primitivas después, en
cualquier ámbito, esa tabla tendría que ser dinámica — y Ada garantiza que el despacho tiene coste
constante y acotado, que es lo que exige un sistema de tiempo real.

Es un buen ejemplo de una decisión que molesta al escribir un programa de veinte líneas y que existe
por lo que Ada promete en programas de un millón.
"""),
        "pascal": ("""
program Poli;
{$MODE OBJFPC}{$H+}
uses SysUtils;

type
  TAnimal = class
    function Sonido: string; virtual; abstract;
  end;

  TPerro = class(TAnimal)
    function Sonido: string; override;
  end;

  TGato = class(TAnimal)
    function Sonido: string; override;
  end;

  TVaca = class(TAnimal)
    function Sonido: string; override;
  end;

function TPerro.Sonido: string; begin Result := 'guau'; end;
function TGato.Sonido:  string; begin Result := 'miau'; end;
function TVaca.Sonido:  string; begin Result := 'muu';  end;

var
  A: TAnimal;
  Tipo: string;

begin
  ReadLn(Tipo);
  Tipo := Trim(Tipo);

  if Tipo = 'perro' then
    A := TPerro.Create
  else if Tipo = 'gato' then
    A := TGato.Create
  else
    A := TVaca.Create;

  try
    WriteLn('sonido=', A.Sonido);      { despacho dinámico }
  finally
    A.Free;
  end;
end.
""", """
**Lo que esta clase enseña en Pascal.** Object Pascal tiene **cuatro modificadores de método**, y la
distinción entre ellos es más fina que en la mayoría de los lenguajes:

```pascal
procedure P;                     { ESTÁTICO: sin despacho, se resuelve al compilar }
procedure P; virtual;             { virtual: entra en la VMT }
procedure P; dynamic;              { dinámico: tabla más compacta, llamada más lenta }
procedure P; override;              { redefine uno virtual o dinámico del ancestro }
procedure P; abstract;               { sin cuerpo: obliga al descendiente }
procedure P; reintroduce;             { OCULTA el del ancestro a propósito }
```

**`dynamic` frente a `virtual`** es una distinción propia de Delphi, pensada para las jerarquías
profundas de la biblioteca visual: una tabla de métodos virtuales completa por clase ocupa memoria, y
`dynamic` guarda solo los redefinidos, buscando en la cadena de ancestros al llamar. Es cambiar
velocidad por espacio, y en 1995, con 8 MB de RAM, importaba.

**`reintroduce`** es la más interesante: declara **a propósito** que un método oculta al del ancestro
sin redefinirlo. Sin ella, el compilador avisa. Es Pascal obligando a decir la intención, igual que
`override`.

Y aquí conviene subrayar algo que la clase 110 ya insinuó: **Pascal permite escribir `override` y el
compilador lo comprueba desde 1995**, mientras que C++ esperó a 2011 y Java lo resolvió con una
anotación opcional. Los lenguajes de la familia Wirth han sido consistentemente más estrictos en esto.

Sobre composición frente a herencia, Delphi tiene una construcción propia que merece nombrarse: la
**delegación de interfaces**.

```pascal
type
  TCoche = class(TInterfacedObject, IMotor)
  private
    FMotor: TMotor;
    property Motor: TMotor read FMotor implements IMotor;   { DELEGA la interfaz }
  end;
```

**`implements`** hace que la clase cumpla `IMotor` **reenviando automáticamente todas sus llamadas al
objeto interno**, sin escribir ni un método de reenvío. Es composición con la comodidad sintáctica de
la herencia, y es exactamente lo que el cierre de esta clase recomienda — disponible desde 1997 y muy
poco conocida fuera del ecosistema Delphi.
"""),
        "lisp": ("""
(defclass animal () ())
(defclass perro (animal) ())
(defclass gato  (animal) ())
(defclass vaca  (animal) ())

(defgeneric sonido (a))
(defmethod sonido ((a perro)) "guau")
(defmethod sonido ((a gato))  "miau")
(defmethod sonido ((a vaca))  "muu")

(let* ((tipo (string-trim '(#\\Space #\\Return) (read-line)))
       (a (make-instance (cond ((string= tipo "perro") 'perro)
                               ((string= tipo "gato")  'gato)
                               (t                      'vaca)))))
  (format t "sonido=~A~%" (sonido a)))
""", """
**Lo que esta clase enseña en Common Lisp.** CLOS tiene **herencia múltiple de verdad**, y resolvió el
problema del diamante de una forma que después copiaron Python y Dylan: **la linealización C3**.

```lisp
(defclass anfibio (terrestre acuatico) ())
```

Cuando `anfibio` hereda de dos clases que definen el mismo método, CLOS calcula un **orden de
precedencia de clases** determinista y **monótono**: una lista lineal de todas las superclases. El
método que se ejecuta es el primero de esa lista que lo defina, y `call-next-method` avanza al
siguiente.

```lisp
(class-precedence-list (find-class 'anfibio))
```

Esa función existe y devuelve la lista. **El programador puede inspeccionar exactamente qué se va a
ejecutar**, que es más de lo que ofrece C++ con la herencia virtual.

Y esa linealización es literalmente el algoritmo **MRO de Python** —Python 2.3 adoptó C3 citando a
Dylan, que a su vez venía de CLOS—.

CLOS añade además dos cosas que ningún otro lenguaje de esta página tiene y que cambian el diseño:

**Despacho múltiple** (clase 110), que hace innecesario el patrón Visitante:

```lisp
(defmethod colisiona ((a nave) (b asteroide)) ...)
```

**Y `change-class`**, que cambia la clase de un objeto **existente**:

```lisp
(change-class instancia 'otra-clase)
```

El objeto conserva su identidad —las referencias que lo apuntaban siguen apuntándolo— y cambia de
clase, con `update-instance-for-different-class` para migrar los campos. Es imposible de imaginar en
C++ o Java, y en un sistema vivo que se actualiza sin parar tiene todo el sentido.

Lo mismo pasa al **redefinir una clase** con instancias ya creadas: CLOS las migra llamando a
`update-instance-for-redefined-class`. Es el mismo problema que resuelven las migraciones de esquema
de una base de datos, resuelto en el lenguaje.
"""),
        "tcl": ("""
oo::class create Animal {
    method sonido {} { return "?" }
}

oo::class create Perro {
    superclass Animal
    method sonido {} { return "guau" }
}

oo::class create Gato {
    superclass Animal
    method sonido {} { return "miau" }
}

oo::class create Vaca {
    superclass Animal
    method sonido {} { return "muu" }
}

gets stdin linea
set tipo [string trim $linea]

switch -exact -- $tipo {
    perro   { set a [Perro new] }
    gato    { set a [Gato new] }
    default { set a [Vaca new] }
}

puts "sonido=[$a sonido]"
""", """
**Lo que esta clase enseña en Tcl.** TclOO tiene **herencia múltiple** —`superclass` acepta varias
clases— y usa **la misma linealización C3** que CLOS y Python. La documentación lo dice
explícitamente.

Pero lo característico de TclOO en esta clase son los **mixins**, que son la respuesta al dilema del
cierre:

```tcl
oo::class create Registrable {
    method registrar {msg} { puts "[clock seconds]: $msg" }
}

oo::define Perro mixin Registrable          ;# añadir a la CLASE
oo::objdefine $a mixin Registrable           ;# o solo a ESTE objeto
oo::objdefine $a mixin -clear                 ;# y quitarlo
```

Un **mixin** aporta métodos sin ser superclase: se coloca **delante** de la clase en la cadena de
resolución, así que puede interceptar y llamar a `next`. Y se puede añadir y quitar **en caliente,
sobre objetos que ya existen**.

Eso es composición con despacho, y resuelve el problema que la herencia múltiple crea: **no hay
jerarquía que reorganizar, hay comportamiento que se acopla y se desacopla**.

TclOO tiene además dos mecanismos más en la cadena de resolución, y el orden completo es este:

```text
filtros → mixins del objeto → clase del objeto → mixins de clase → superclases (C3)
```

**Los filtros** interceptan **todos** los métodos:

```tcl
oo::define Perro filter trazar
oo::define Perro method trazar {args} {
    puts "llamando a [self target]"
    return [next {*}$args]
}
```

`self target` dice qué método se estaba invocando y `next` continúa la cadena. Es el `:around` de CLOS
y la base de proxies, auditoría y objetos remotos.

Que un lenguaje cuyo sistema de objetos llegó en 2012 tenga linealización C3, mixins dinámicos y
filtros no es casualidad: **llegó tarde y aprendió de todos los anteriores**, y su propuesta cita a
CLOS, a Smalltalk y a las bibliotecas que la comunidad Tcl había usado durante veinte años.
"""),
        "perl": ("""
use strict;
use warnings;

package Animal;
sub new    { my $clase = shift; return bless {}, $clase }
sub sonido { return '?' }

package Perro; our @ISA = ('Animal');
sub sonido { return 'guau' }

package Gato;  our @ISA = ('Animal');
sub sonido { return 'miau' }

package Vaca;  our @ISA = ('Animal');
sub sonido { return 'muu' }

package main;

my $tipo = <STDIN>;
chomp $tipo;

my %clase = (perro => 'Perro', gato => 'Gato', vaca => 'Vaca');
my $a = ($clase{$tipo} // 'Vaca')->new;

print "sonido=", $a->sonido, "\\n";
""", """
**Lo que esta clase enseña en Perl.** La herencia de Perl es **una variable**: `@ISA`.

```perl
our @ISA = ('Animal');           # la forma cruda
use parent 'Animal';              # el módulo moderno, del núcleo
use base 'Animal';                 # el anterior, todavía en mucho código
```

Y como es una variable normal, **se puede modificar en ejecución**:

```perl
push @Perro::ISA, 'Mascota';      # añadir una superclase AHORA
```

Eso es herencia múltiple dinámica, y Perl la tiene desde 1994. El recorrido por defecto es **en
profundidad y de izquierda a derecha**, que es lo que hacía Python 2 antes de C3 y que tiene el mismo
problema del diamante.

Perl ofrece la alternativa desde 5.10:

```perl
use mro 'c3';                     # linealización C3, como CLOS y Python 3
```

Y hay una parte de la búsqueda de métodos que es característica de Perl: **`AUTOLOAD`**.

```perl
sub AUTOLOAD {
    my $self = shift;
    our $AUTOLOAD;
    my $metodo = $AUTOLOAD;
    $metodo =~ s/.*:://;
    # ... hacer algo con un método que NO EXISTE
}
```

Si la búsqueda por `@ISA` no encuentra el método, Perl llama a `AUTOLOAD` con el nombre en una
variable. Es exactamente el `doesNotUnderstand:` de Smalltalk (clase 051) y el `__getattr__` de
Python, y sirve para lo mismo: generar accesores al vuelo, construir proxies y objetos remotos.

Sobre composición, la respuesta moderna de Perl son los **roles** de `Moose` y `Moo`:

```perl
package Sonoro;
use Moose::Role;
requires 'sonido';                 # el que lo use DEBE implementarlo

package Perro;
use Moose;
with 'Sonoro';                      # componer, no heredar
```

Un **rol** aporta métodos y **exige** otros, y se compone en plano: si dos roles aportan el mismo
método, **es un error en tiempo de composición**, no una resolución silenciosa. Es la diferencia
esencial con la herencia múltiple, y es la idea de los *traits* de Rust, Scala y PHP.
"""),
        "cpp": ("""
#include <iostream>
#include <memory>
#include <string>

struct Animal {
    virtual ~Animal() = default;                  // destructor VIRTUAL: imprescindible
    virtual std::string sonido() const = 0;        // método puro: abstracto
};

struct Perro : Animal { std::string sonido() const override { return "guau"; } };
struct Gato  : Animal { std::string sonido() const override { return "miau"; } };
struct Vaca  : Animal { std::string sonido() const override { return "muu";  } };

int main() {
    std::string tipo;
    if (!(std::cin >> tipo)) return 1;

    std::unique_ptr<Animal> a;
    if (tipo == "perro")     a = std::make_unique<Perro>();
    else if (tipo == "gato") a = std::make_unique<Gato>();
    else                     a = std::make_unique<Vaca>();

    std::cout << "sonido=" << a->sonido() << '\\n';
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** La primera línea de `Animal` es la más importante del programa, y
es el error más caro de C++ en esta clase:

```cpp
virtual ~Animal() = default;
```

**Sin destructor virtual, borrar un `Perro` a través de un puntero a `Animal` es comportamiento
indefinido**: se ejecuta el destructor de `Animal` y no el de `Perro`, así que sus recursos no se
liberan. Con `unique_ptr<Animal>`, ese `delete` ocurre automáticamente al salir del ámbito.

La regla es sencilla y se olvida constantemente: **si una clase tiene algún método virtual, su
destructor debe ser virtual** — o la clase debe declararse `final` y no usarse polimórficamente.

Y `= 0` en `sonido()` la hace **pura**: `Animal` es abstracta y no se puede instanciar.

C++ es el único de esta página con **herencia múltiple de implementación completa**, con el problema
del diamante y su solución explícita:

```cpp
class B { int x; };
class D1 : public virtual B { };      // herencia VIRTUAL
class D2 : public virtual B { };
class E  : public D1, public D2 { };   // UNA sola copia de B
```

Sin `virtual`, `E` tendría **dos copias de `B`** y `e.x` sería ambiguo. Con ella, una sola, a costa de
una indirección extra para llegar a la parte compartida.

Es potente y es la característica que Java, C#, Ada y COBOL decidieron no copiar. C++ la mantiene
porque hace falta para casos concretos —los flujos de la biblioteca estándar la usan— y las guías
recomiendan limitarla a heredar de clases **sin estado**, es decir, interfaces.

Y esta clase es el sitio para la alternativa moderna, que el cierre recomienda: **el polimorfismo sin
herencia**.

```cpp
template <typename T> void hacer_sonar(const T& a) { std::cout << a.sonido(); }
// o con std::variant + std::visit (clase 100), sin jerarquía ninguna
```

Con plantillas y conceptos, el despacho se resuelve al compilar, sin `vtable` y sin puntero. Es más
rápido y menos flexible, y en C++ moderno **es la opción por defecto** salvo que se necesite una
colección heterogénea.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi POLI;
  tipo char(10) const;
end-pi;

dcl-s sonido varchar(10);

// RPG no tiene herencia ni polimorfismo: un select sobre la etiqueta
select;
  when %trim(tipo) = 'perro';  sonido = 'guau';
  when %trim(tipo) = 'gato';   sonido = 'miau';
  when %trim(tipo) = 'vaca';   sonido = 'muu';
  other;                       sonido = '?';
endsl;

dsply ('sonido=' + sonido);

*inlr = *on;
return;
""", """
**Lo que esta clase enseña en RPG.** RPG no tiene herencia ni polimorfismo, y su respuesta es la misma
que la de COBOL: un `select` sobre una etiqueta, con el mismo problema de mantenimiento.

Lo que sí tiene es la vía de escape de la clase 085: **`%paddr` con un puntero a procedimiento**.

```rpgle
dcl-pr obtenerSonido varchar(10) extproc(puntero);
end-pr;

dcl-s puntero pointer;
dcl-ds tabla qualified dim(10);
  tipo   char(10);
  metodo pointer;
end-ds;

// rellenar la tabla al arrancar:
tabla(1).tipo = 'perro';
tabla(1).metodo = %paddr('SONIDO_PERRO');
...
puntero = tabla(%lookup(tipo : tabla(*).tipo)).metodo;
sonido = obtenerSonido();
```

Eso es **una tabla de métodos virtuales construida a mano**, exactamente como la que se describió en
PL/I en la clase 110 y como la que usa el núcleo de Linux con estructuras de punteros a función.

Es la demostración de que **el polimorfismo no necesita orientación a objetos**: necesita una tabla
que asocie un tipo con un comportamiento, y una llamada indirecta. Los objetos son una forma cómoda y
comprobada de tener eso, no la única.

En la práctica, un programa RPG moderno resuelve este problema de dos maneras que reflejan bien la
plataforma:

- **Con `CALL` a un programa cuyo nombre está en una tabla de la base de datos**, como en COBOL: la
  "jerarquía" vive en una tabla Db2 y añadir un tipo es insertar una fila.
- **Llamando a Java** con `extproc(*java)` (clase 110), donde el polimorfismo lo pone la JVM.

Y merece cerrar con lo mismo que la clase 110: **la ausencia de herencia no ha impedido que se
construyan sistemas de millones de líneas en RPG**. Lo que enseña esta clase no es que falte algo, sino
**cuál es el coste concreto de que falte** — y ese coste se paga en cada `select` que hay que
actualizar.
"""),
        "pli": ("""
 poli: procedure options(main);

    declare linea char(80) varying;
    declare sonido char(10) varying;

    get edit (linea) (a(80));
    linea = trim(linea);

    select (linea);
       when ('perro') sonido = 'guau';
       when ('gato')  sonido = 'miau';
       when ('vaca')  sonido = 'muu';
       otherwise      sonido = '?';
    end;

    put skip list ('sonido=' || sonido);

 end poli;
""", """
**Lo que esta clase enseña en PL/I.** Como en COBOL y RPG, la respuesta es un `select` — con la
ventaja de que el `select` de PL/I es de 1964 y no tiene caída entre casos (clase 100).

Lo que PL/I aporta a esta clase, y es lo interesante, es que **tenía las piezas del polimorfismo antes
que nadie y nunca las juntó**:

```pli
 declare 1 objeto based(p),
           2 tipo fixed binary(15),
           2 sonido entry variable returns (char(10) varying);

 p -> sonido = sonido_perro;      /* rellenar la vtable */
 texto = p -> sonido();            /* llamada INDIRECTA: despacho dinámico */
```

**Variables `entry` que apuntan a procedimientos** (clase 085), **estructuras `based`** que se
superponen a memoria (clase 090) y **reserva dinámica** (clase 103). Con esas tres cosas, el
despacho dinámico se escribe a mano, y era un patrón conocido en los años setenta.

Lo que faltó fue la sintaxis y —más importante— **la garantía**: nada comprueba que el puntero apunte
al procedimiento correcto, que la firma encaje ni que la estructura sea del tipo que se cree. El
compilador de C++ hace exactamente eso mismo por debajo, **y lo comprueba**.

Esa es la diferencia real entre "tener las piezas" y "tener la característica", y es una idea que
merece la pena llevarse de esta clase entera.

Y sobre la herencia, PL/I tiene un mecanismo que se le parece de lejos y que conviene no confundir:
**`like`**.

```pli
 declare 1 empleado like persona,     /* copia la ESTRUCTURA de persona */
           2 salario fixed decimal(9,2);
```

`like` copia la declaración de otra estructura y permite añadir campos. **Es herencia de datos sin
herencia de comportamiento y sin polimorfismo**: un ahorro de escritura, no una relación de tipos. Si
cambia `persona`, `empleado` cambia **al recompilar**, y nada más.

Es exactamente el `likeds` de RPG (clase 110), y los dos ilustran lo mismo: **compartir la forma de
los datos es fácil; compartir el comportamiento con garantías es lo que costó veinte años**.
"""),
        "mumps": ("""
POLI ; Herencia y polimorfismo -- clase 111
 read tipo
 set tipo = $zconvert($piece(tipo, " ", 1), "L")
 set sonido = "?"
 ; despacho por INDIRECCION: la etiqueta se construye como texto
 if $text(@(tipo_"^POLI"))'="" set sonido = $$@(tipo_"^POLI")
 write "sonido=", sonido, !
 quit
 ;
perro() quit "guau"
gato()  quit "miau"
vaca()  quit "muu"
""", """
**Lo que esta clase enseña en M.** M no tiene clases, herencia ni polimorfismo, y su respuesta es la
más extrema de esta página: **la indirección** de la clase 085.

```mumps
 set sonido = $$@(tipo_"^POLI")
```

Esa línea llama a **la etiqueta cuyo nombre es el valor de la variable `tipo`**. Añadir un animal es
escribir una etiqueta más en la rutina; **el despachador no se toca**.

Es polimorfismo conseguido con texto, y tiene todas las propiedades del despacho dinámico —añadir
casos sin modificar el código existente— y ninguna de sus garantías: **nada comprueba que la etiqueta
exista ni que devuelva lo que se espera**.

Por eso el programa usa **`$text`** antes de llamar:

```mumps
 if $text(@(tipo_"^POLI"))'=""
```

**`$text` devuelve el código fuente de una línea de programa**, y si la etiqueta no existe devuelve la
cadena vacía. Es la forma de M de preguntar "¿existe este método?", y es el equivalente de
`respond_to?` en Ruby y de `respondsTo:` en Smalltalk.

Que la función que consulta **el texto fuente de una rutina** sea parte del estándar dice mucho del
lenguaje: en M, **el código es un dato accesible en ejecución**, guardado en el mismo tipo de
estructura que los datos.

Con `$text` se construyen, y se construyen de verdad en VistA: comprobación de existencia antes de
llamar, listados de rutinas, herramientas de análisis y **el propio sistema de parcheo**, que compara
versiones de rutinas leyendo su código con `$text`.

Y para cerrar con lo mismo que las clases 109 y 110: la orientación a objetos completa la aportan las
implementaciones modernas —**IRIS con clases, herencia múltiple y polimorfismo**— sobre el mismo modelo
de datos. El lenguaje base se quedó donde estaba; la plataforma siguió.
"""),
        "smalltalk": ("""
| tipo sonido |

tipo := stdin nextLine trimBoth.

"En Smalltalk el polimorfismo es el mecanismo BÁSICO: un diccionario
 de tipo a bloque hace de jerarquía mínima."
sonido := (Dictionary newFrom: {
    'perro' -> 'guau'.
    'gato'  -> 'miau'.
    'vaca'  -> 'muu' })
        at: tipo ifAbsent: [ '?' ].

Transcript show: 'sonido=', sonido; cr.
""", """
**Lo que esta clase enseña en Smalltalk.** La versión con clases es la canónica y se escribe así:

```smalltalk
Object subclass: #Animal.
Animal >> sonido    ^self subclassResponsibility

Animal subclass: #Perro.
Perro >> sonido     ^'guau'

Animal subclass: #Gato.
Gato >> sonido      ^'miau'
```

**`subclassResponsibility`** es cómo Smalltalk declara un método abstracto: **no es una palabra clave,
es un mensaje** heredado de `Object` que lanza un error si alguien lo invoca. Otra vez, lo que en otros
lenguajes es sintaxis, aquí es una llamada.

Y en Smalltalk el polimorfismo **no es una característica: es el único mecanismo que hay**. Un mensaje
se envía a un objeto y ese objeto decide qué hacer. **No existe la llamada estática**, así que no hay
`virtual` que declarar ni `override` que marcar.

De ahí sale el **duck typing**, que aquí no es un apaño sino la consecuencia natural:

```smalltalk
coleccion do: [ :cada | cada sonido ]
```

Eso funciona con cualquier objeto que responda a `sonido`, **tenga o no una superclase común**. La
herencia sirve para **compartir implementación**, no para habilitar el polimorfismo — que es
exactamente lo que separa la herencia de las interfaces (clase 112) y lo que el cierre de esta clase
recomienda tener presente.

Smalltalk tiene **herencia simple**, sin excepciones y sin interfaces, y la comunidad lo compensa con
dos cosas:

- **Los *traits*** (Pharo, 2003): unidades de comportamiento componibles, con resolución explícita de
  conflictos. Son la investigación de la que salieron los *traits* de Rust, PHP y Scala — el artículo
  original es de Schärli, Ducasse, Nierstrasz y Black, en Smalltalk.
- **La convención**: si dos clases sin relación responden a los mismos mensajes, son intercambiables.
  No hace falta declararlo.

Y `subclassResponsibility` tiene un pariente que resume la filosofía: **`doesNotUnderstand:`** (clase
051). Cuando un objeto recibe un mensaje que no entiende, **no es un error del sistema: es un mensaje
más**, que se le envía al propio objeto y que puede interceptar. Con eso se construyen proxies,
objetos remotos y APIs dinámicas.

En Smalltalk, incluso el fallo del polimorfismo es polimórfico.
"""),
    },
)
