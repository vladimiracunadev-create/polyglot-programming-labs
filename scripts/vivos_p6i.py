# -*- coding: utf-8 -*-
"""Parte 6, lote I — clase 099. Ver `vivos_parte6.py` y `gen_vivos.py`."""

SPECS: dict[str, dict] = {}

# ---------------------------------------------------------------------------
# 099 — Registros, structs y clases
# ---------------------------------------------------------------------------
SPECS["099"] = dict(
    gancho="""
Una persona con nombre y edad, mostrada con formato. La estructura más antigua del procesamiento de
datos —**COBOL la llamó registro en 1959 y la puso en el centro del lenguaje**— y la pregunta que
separa a estos doce lenguajes: **¿un registro es solo datos, o también comportamiento?** Siete de
ellos tienen las dos cosas hoy, y **cinco de esos siete lo añadieron después de nacer**.
""",
    porque="""
Aquí el concepto es el **agregado con campos con nombre**, y estos lenguajes lo enseñan porque
documentan la transición de "registro" a "objeto". **COBOL añadió clases en 2002; Fortran, en 2003;
Ada, en 1995; RPG y Pascal, en los noventa; PL/I, nunca**. Ver la misma estructura antes y después de
esa frontera enseña qué añadió realmente la orientación a objetos: **no los campos, que ya estaban,
sino ligar el comportamiento al dato y poder extenderlo**.

Y **Smalltalk** está en el otro extremo: **no tiene registros**, porque un objeto lo cubre todo.
""",
    cierre="""
Lo transferible: **un registro de datos y una clase resuelven problemas distintos, y confundirlos
cuesta caro**. Un registro es una forma de memoria: se copia, se escribe en disco y se envía por la
red, y su compatibilidad la define su disposición binaria. Una clase es un contrato de comportamiento:
se sustituye por un descendiente y su compatibilidad la define su interfaz. Cuando veas un lenguaje
que distingue `struct` de `class` —C#, Swift, Rust con `dyn`— está separando exactamente eso. Y cuando
veas un objeto serializado a JSON, estás convirtiéndolo de vuelta en un registro.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. PERSONA.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(200).
01  TXT-E   PIC X(20).
01  REG-PERSONA.
    05  NOMBRE  PIC X(20).
    05  EDAD    PIC 9(3).
01  ED-E    PIC Z(2)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    UNSTRING LINEA DELIMITED BY ALL SPACES INTO NOMBRE TXT-E
    COMPUTE EDAD = FUNCTION NUMVAL(TXT-E)

    MOVE EDAD TO ED-E
    DISPLAY "Persona(nombre=" FUNCTION TRIM(NOMBRE)
            ", edad=" FUNCTION TRIM(ED-E) ")"
    STOP RUN.
""", """
**Lo que esta clase enseña en COBOL.** El registro **es** COBOL. Toda la `DATA DIVISION` está
organizada en niveles jerárquicos, y esa jerarquía no es una elección de estilo: **es el formato del
fichero**.

```cobol
01  REG-CLIENTE.
    05  CLI-ID         PIC 9(9).
    05  CLI-NOMBRE.
        10  CLI-PILA   PIC X(20).
        10  CLI-APE1   PIC X(25).
    05  CLI-SALDO      PIC S9(11)V99 COMP-3.
```

Ese `01` describe **exactamente los bytes** de un registro en disco: dónde empieza cada campo, cuántos
ocupa y cómo se codifica. Leerlo es `READ` y ya está: no hay analizador, no hay deserialización y no
hay coste. Es la razón de que COBOL siga procesando volúmenes que asombran — **el fichero y la
estructura del programa son la misma disposición de bytes**.

Y de ahí salen tres cosas propias:

- **`REDEFINES`** (clase 091): los mismos bytes con otra forma.
- **`RENAMES`** (nivel 66): agrupar campos no contiguos bajo un nombre.
- **`COPY`** (clase 088): compartir la definición entre programas, que es lo que garantiza que el que
  escribe y el que lee usen el mismo formato.

**COBOL orientado a objetos existe desde el estándar de 2002**, y es completo:

```cobol
CLASS-ID. Persona INHERITS FROM Base.
OBJECT.
    DATA DIVISION.
    WORKING-STORAGE SECTION.
    01  NOMBRE PIC X(20).
    PROCEDURE DIVISION.
    METHOD-ID. SET-NOMBRE.
    ...
    END METHOD.
END OBJECT.
END CLASS Persona.
```

Clases, herencia, interfaces, métodos y polimorfismo, con la verbosidad esperable. Existe en IBM
Enterprise COBOL, en Micro Focus y en GnuCOBOL parcialmente, y **casi nadie lo usa**.

La razón no es desconocimiento: **el problema que resuelve la orientación a objetos —extender
comportamiento sin tocar el código existente— no es el problema del código COBOL**, cuyo trabajo es
transformar registros de un formato a otro. Y sobre eso, el `01` de 1959 sigue siendo la herramienta
adecuada.
"""),
        "fortran": ("""
program persona
   implicit none

   type :: registro
      character(len=20) :: nombre
      integer           :: edad
   end type registro

   type(registro) :: p
   character(len=200) :: linea
   integer :: pos

   read(*, '(A)') linea
   pos = index(trim(linea), ' ')

   p%nombre = linea(1:pos-1)
   read(linea(pos+1:), *) p%edad

   write(*, '(A,I0,A)') 'Persona(nombre=' // trim(p%nombre) // &
                        ', edad=', p%edad, ')'
end program persona
""", """
**Lo que esta clase enseña en Fortran.** Los tipos derivados de Fortran 90 empezaron siendo puros
agregados —campos y nada más— y **Fortran 2003 los convirtió en clases completas**, con una sintaxis
que merece verse:

```fortran
type :: persona
   character(len=20) :: nombre
   integer :: edad
contains
   procedure :: saludar                 ! un MÉTODO, dentro del tipo
   procedure :: imprimir
   generic :: write(formatted) => imprimir   ! sobrecargar la ESCRITURA
end type persona

type, extends(persona) :: empleado      ! HERENCIA
   real :: salario
end type empleado
```

Cuatro piezas de una vez: **`contains` dentro del tipo** para los métodos, **`extends`** para heredar,
**`class(persona)`** en lugar de `type(persona)` para el polimorfismo, y **`select type`** para el
despacho explícito.

La palabra `class` es la clave y confunde al principio:

```fortran
type(persona)  :: a      ! EXACTAMENTE persona
class(persona) :: b      ! persona o cualquier descendiente -- POLIMÓRFICO
```

Y hay dos añadidos de 2003 que son particularmente útiles y poco conocidos:

**La sobrecarga de la entrada y salida definida por el usuario.** `generic :: write(formatted)`
permite que `print *, p` invoque un método propio, así que un tipo puede decidir cómo se imprime. Es
`operator<<` de C++ y `printOn:` de Smalltalk.

**Los constructores y destructores.** `final :: limpiar` declara un procedimiento que se ejecuta al
destruirse el objeto — el destructor de C++, en un lenguaje de 1957.

El motivo de todo esto no fue seguir la moda: **los códigos científicos grandes necesitaban
polimorfismo** para escribir un solver que funcionara con distintos modelos físicos sin duplicar el
código. Es el mismo problema que resuelven las interfaces en cualquier otro sitio, llegado a Fortran
por la puerta del cálculo.
"""),
        "ada": ("""
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Persona is
   type Registro is record
      Nombre : String (1 .. 20) := (others => ' ');
      Largo  : Natural := 0;
      Edad   : Natural := 0;
   end record;

   P      : Registro;
   Linea  : String (1 .. 200);
   Ultimo : Natural;
   Corte  : Natural := 0;
begin
   Get_Line (Linea, Ultimo);

   for I in 1 .. Ultimo loop
      if Linea (I) = ' ' then
         Corte := I;
         exit;
      end if;
   end loop;

   P.Largo := Corte - 1;
   P.Nombre (1 .. P.Largo) := Linea (1 .. P.Largo);
   P.Edad := Natural'Value (Linea (Corte + 1 .. Ultimo));

   Put ("Persona(nombre=" & P.Nombre (1 .. P.Largo) & ", edad=");
   Put (P.Edad, Width => 1);
   Put_Line (")");
end Persona;
""", """
**Lo que esta clase enseña en Ada.** Fíjate en la declaración del registro: **los campos tienen valor
por defecto**.

```ada
type Registro is record
   Nombre : String (1 .. 20) := (others => ' ');
   Edad   : Natural := 0;
end record;
```

Esa **inicialización por defecto de componentes** está en Ada desde 1983, y significa que `P : Registro;`
crea un valor **completamente definido**. En C y C++ hasta C++11, una `struct` sin inicializar contiene
basura, y leerla es comportamiento indefinido.

Y Ada añade el mecanismo que hace de esto una garantía real y no una costumbre: **los tipos
controlados**.

```ada
type Recurso is new Ada.Finalization.Controlled with record ... end record;

overriding procedure Initialize (R : in out Recurso);   --  al crear
overriding procedure Adjust     (R : in out Recurso);   --  al COPIAR
overriding procedure Finalize   (R : in out Recurso);   --  al destruir
```

`Initialize`, `Adjust` y `Finalize` son el constructor, el constructor de copia y el destructor de
C++, con una diferencia de nombre reveladora: **`Adjust` se llama DESPUÉS de la copia bit a bit**,
para arreglar lo que haga falta —duplicar un búfer, incrementar un contador—. Es un modelo distinto
del de C++, donde el constructor de copia construye desde cero, y para muchos casos es más simple.

Y sobre objetos: **Ada 95 añadió la orientación a objetos con `tagged`**, no con una palabra `class`.

```ada
type Persona is tagged record ... end record;
type Empleado is new Persona with record Salario : Float; end record;
```

`tagged` significa "este tipo lleva una etiqueta de su tipo real en ejecución", que es lo que permite
el despacho dinámico. Y el detalle de diseño: **los métodos no van dentro del tipo**, son
subprogramas normales cuyo primer parámetro es del tipo etiquetado. Eso permite **añadir operaciones
primitivas sin tocar la declaración**, y evita la asimetría de `a.f(b)` frente a `f(a, b)` que en C++
obliga a decidir entre método y función libre.
"""),
        "pascal": ("""
program Persona;
{$MODE OBJFPC}{$H+}
uses SysUtils;

type
  TPersona = record
    Nombre: string;
    Edad: Integer;
  end;

var
  P: TPersona;
  Linea: string;
  Corte: Integer;

begin
  ReadLn(Linea);
  Linea := Trim(Linea);

  Corte := Pos(' ', Linea);
  P.Nombre := Copy(Linea, 1, Corte - 1);
  P.Edad := StrToInt(Trim(Copy(Linea, Corte + 1, Length(Linea))));

  WriteLn('Persona(nombre=', P.Nombre, ', edad=', IntToStr(P.Edad), ')');
end.
""", """
**Lo que esta clase enseña en Pascal.** Pascal es de los pocos lenguajes de esta página donde
**`record` y `class` conviven con semánticas claramente distintas**, y la distinción es exactamente la
del cierre de esta clase:

```pascal
type
  TPunto = record          { VALOR: se copia al asignar, vive en la pila }
    X, Y: Integer;
  end;

  TFigura = class          { REFERENCIA: se comparte, vive en el montón }
    X, Y: Integer;
    constructor Create;
    destructor Destroy; override;
  end;

var
  A, B: TPunto;
  F, G: TFigura;
begin
  B := A;        { COPIA los campos }
  G := F;        { comparte el MISMO objeto }
end;
```

Esa dualidad es la que después copiaron C# —`struct` frente a `class`— y Swift, con las mismas
consecuencias y las mismas confusiones.

Y hay una tercera opción, propia de Delphi y de Free Pascal, que se sitúa en medio:

```pascal
TVieja = object          { OBJETO al estilo Turbo Pascal 5.5: valor CON métodos y herencia }
```

`object` fue la primera orientación a objetos de Pascal (1989) y tiene semántica de valor con
herencia y métodos virtuales. Está obsoleto y sigue apareciendo en código antiguo.

Object Pascal moderno añade a los `record` casi todo lo que tiene una clase salvo la herencia:
métodos, propiedades, constructores, operadores sobrecargados y campos con visibilidad. Es
deliberado: **la herencia con semántica de valor lleva al problema del *slicing*** —copiar un
descendiente en una variable del ancestro trunca los campos añadidos—, y evitarlo es la misma decisión
que tomaron C# y Swift.

Y una última pieza propia: **el `class` de Delphi tiene métodos y variables de CLASE**, más
`class constructor`, con lo que la clase es a la vez un objeto — algo que en Java se resuelve con
`static` y en Smalltalk, mucho mejor, con metaclases de verdad.
"""),
        "lisp": ("""
(defstruct persona nombre edad)

(let* ((linea (string-trim '(#\\Space #\\Return) (read-line)))
       (corte (position #\\Space linea))
       (p (make-persona :nombre (subseq linea 0 corte)
                        :edad   (parse-integer (subseq linea (1+ corte))))))
  (format t "Persona(nombre=~A, edad=~D)~%"
          (persona-nombre p) (persona-edad p)))
""", """
**Lo que esta clase enseña en Common Lisp.** `(defstruct persona nombre edad)` es una línea, y genera
**siete cosas**:

```lisp
(make-persona :nombre "Ada" :edad 36)    ; constructor con argumentos por nombre
(persona-nombre p)                        ; accesor
(setf (persona-nombre p) "Ada")           ; y es un LUGAR asignable
(persona-p x)                             ; predicado de tipo
(copy-persona p)                          ; copia superficial
#S(PERSONA :NOMBRE "Ada" :EDAD 36)        ; impresión LEGIBLE...
                                           ; ...y que `read` puede volver a leer
```

Esa última propiedad es la interesante: **la impresión de una estructura se puede leer de vuelta** con
`read`, así que guardar un objeto en un fichero es `print` y recuperarlo es `read`. Serialización sin
biblioteca, otra vez, como el árbol de la clase 097.

`defstruct` acepta además opciones que cubren casi todo:

```lisp
(defstruct (persona (:include entidad)      ; HERENCIA simple
                    (:constructor crear (nombre edad))   ; constructor posicional
                    (:print-function mostrar))
  (nombre "" :type string)                   ; con TIPO declarado
  (edad 0 :type (integer 0 150)))            ; y con RANGO
```

Y cuando hace falta más, está **CLOS**, el sistema de objetos de Common Lisp, que es el más potente de
esta página y con diferencia:

```lisp
(defclass persona () ((nombre :accessor persona-nombre :initarg :nombre)))
(defmethod saludar ((p persona)) ...)
(defmethod saludar ((p empleado)) ...)
```

Tres diferencias con la orientación a objetos habitual, y las tres importan:

1. **Los métodos no pertenecen a las clases.** Una **función genérica** tiene métodos, y cada método
   se especializa en los tipos de **todos** sus parámetros — despacho múltiple.
2. **Herencia múltiple** con un orden de linealización definido y predecible.
3. **Combinación de métodos**: `:before`, `:after`, `:around` y `call-next-method` permiten componer
   comportamiento sin que la clase base lo prevea.

CLOS es de 1988 y sigue siendo más expresivo que los sistemas de objetos de la mayoría de los
lenguajes actuales. Y está escrito **en el propio lenguaje**, con el protocolo de metaobjetos (MOP)
como interfaz para modificarlo.
"""),
        "tcl": ("""
gets stdin linea
lassign [split [string trim $linea]] nombre edad

set p [dict create nombre $nombre edad $edad]

puts "Persona(nombre=[dict get $p nombre], edad=[dict get $p edad])"
""", """
**Lo que esta clase enseña en Tcl.** El registro de Tcl es un **`dict`**, y esa es la respuesta
idiomática para datos: un valor, con claves con nombre, que se pasa, se anida y se serializa
imprimiéndolo.

```tcl
set p [dict create nombre Ada edad 36]
dict get $p nombre
dict with p { puts "$nombre tiene $edad" }     ;# expone las claves como variables
```

Para datos con comportamiento, Tcl tiene **TclOO** en el núcleo desde 8.6 (2012), y su diseño es
llamativo por lo dinámico:

```tcl
oo::class create Persona {
    variable nombre edad
    constructor {n e} { set nombre $n; set edad $e }
    method mostrar {} { return "Persona(nombre=$nombre, edad=$edad)" }
}

set p [Persona new "Ada" 36]
puts [$p mostrar]
```

Fíjate en `[$p mostrar]`: **un objeto ES un comando**, y enviarle un mensaje es invocarlo con el
nombre del método como primer argumento. No hay sintaxis nueva — es la regla básica del lenguaje otra
vez.

Y TclOO tiene tres capacidades que muy pocos sistemas de objetos ofrecen:

```tcl
oo::objdefine $p method extra {} { ... }      ;# un método SOLO para ESTE objeto
oo::define Persona mixin Registrable           ;# mezclar comportamiento, sin herencia
oo::define Persona filter trazar                ;# INTERCEPTAR todas las llamadas
```

**`oo::objdefine`** da métodos por objeto —programación basada en prototipos, como JavaScript—;
**`mixin`** compone sin herencia; y **`filter`** intercepta cualquier envío de mensaje, que es lo que
permite construir *proxies*, registros de auditoría y objetos remotos.

Todo eso **en ejecución, sobre objetos que ya existen**. Es el modelo de Smalltalk y de CLOS, y no es
casualidad: la propuesta de TclOO cita explícitamente a los dos, más Snit e incr Tcl, las dos
bibliotecas de objetos que la comunidad usó durante veinte años antes de que hubiera una oficial.
"""),
        "perl": ("""
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;
my ($nombre, $edad) = split ' ', $linea;

my $p = { nombre => $nombre, edad => $edad };

print "Persona(nombre=$p->{nombre}, edad=$p->{edad})\\n";
""", """
**Lo que esta clase enseña en Perl.** El registro de Perl es **una referencia a hash**, y el objeto de
Perl es **exactamente lo mismo, con una etiqueta pegada**:

```perl
package Persona;
sub new {
    my ($clase, %args) = @_;
    my $yo = { nombre => $args{nombre}, edad => $args{edad} };
    return bless $yo, $clase;          # ETIQUETAR la referencia con la clase
}
sub nombre { $_[0]->{nombre} }
```

**`bless` es todo el sistema de objetos de Perl 5.** Marca una referencia con el nombre de un paquete;
a partir de ahí, `$obj->metodo` busca `metodo` en ese paquete y en `@ISA`. No hay clases como
entidades, no hay campos declarados y no hay privacidad (clase 087).

Larry Wall lo diseñó así por una razón explícita: **añadir objetos a Perl 5 sin cambiar el lenguaje**,
reutilizando paquetes, referencias y tablas de símbolos que ya existían. Es minimalista y funcionó — y
tiene el coste de que cada proyecto define los objetos a su manera.

De ahí que el ecosistema haya producido tres generaciones de soluciones:

```perl
use Moose;                    # 2006: completo, con roles, tipos y modificadores
use Moo;                       # ligero, compatible con Moose
has nombre => (is => 'ro', isa => 'Str', required => 1);
```

**Moose** trajo a Perl los roles —composición horizontal, como los *traits*—, la validación de tipos,
los modificadores `before`/`after`/`around` de CLOS y la introspección completa. Está inspirado
declaradamente en CLOS y en el sistema de objetos de Perl 6.

Y la tercera generación es del lenguaje mismo: **la palabra clave `class`, experimental desde Perl
5.38 (2023)**:

```perl
use v5.38;
use experimental 'class';

class Persona {
    field $nombre :param;      # campos LÉXICOS: privados de verdad
    field $edad   :param;
    method mostrar { "Persona(nombre=$nombre, edad=$edad)" }
}
```

Los `field` son variables léxicas, así que **son realmente privados** (clase 087). Es el cambio más
importante en el modelo de objetos de Perl desde 1994, y llegó treinta años después de `bless`.
"""),
        "cpp": ("""
#include <iostream>
#include <string>

struct Persona {
    std::string nombre;
    int edad{};
};

int main() {
    Persona p;
    if (!(std::cin >> p.nombre >> p.edad)) return 1;

    std::cout << "Persona(nombre=" << p.nombre
              << ", edad=" << p.edad << ")\\n";
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** `struct` y `class` en C++ **son la misma construcción** y solo se
diferencian en el defecto de visibilidad (clase 087). Eso no significa que la distinción del cierre de
esta clase no exista en C++: existe, y es una **convención muy asentada**.

- **`struct`** para agregados de datos: todo público, sin invariantes que mantener, copiable.
- **`class`** cuando hay invariantes que proteger, con constructores que los establecen.

El compilador no la impone, y todas las guías de estilo serias la recogen.

Y hay un concepto del lenguaje que la formaliza: **el agregado**. Una `struct` sin constructores, sin
miembros privados, sin virtuales y sin bases es un *aggregate*, y eso desbloquea la inicialización con
llaves:

```cpp
Persona p{"Ada", 36};
Persona q{.nombre = "Ada", .edad = 36};    // C++20: designadores, en orden
```

El `int edad{}` de este programa es la **inicialización de valor por defecto de miembro** (C++11), y
resuelve el problema que Ada tenía resuelto desde 1983: sin ella, `edad` contendría basura.

Y aquí conviene señalar lo que C++ **no** genera automáticamente, en contraste con las líneas únicas
de Lisp, Rust o Python:

```cpp
p == q             // NO existe salvo que lo escribas
std::cout << p     // tampoco
std::hash<Persona> // tampoco
```

C++20 alivió la primera con el **operador de comparación por defecto**:

```cpp
struct Persona {
    std::string nombre;
    int edad{};
    auto operator<=>(const Persona&) const = default;   // == , < , > , <= , >=
};
```

`<=>` —el *operador nave espacial*— genera **las seis comparaciones** a partir de una declaración, y
lo hace campo a campo en orden de declaración. Es lo que Rust hace con `#[derive(PartialOrd)]` y Lisp
con `defstruct`, llegado en 2020.

La impresión sigue exigiendo escribir `operator<<` o una especialización de `std::formatter` — y esa
sigue siendo una de las asperezas más visibles del lenguaje frente a sus contemporáneos.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi PERSONA;
  entrada char(200) const;
end-pi;

dcl-ds persona qualified;
  nombre varchar(20);
  edad   int(10);
end-ds;

dcl-s corte int(10);
dcl-s texto varchar(200);

texto = %trimr(entrada);
corte = %scan(' ' : texto);

persona.nombre = %subst(texto : 1 : corte - 1);
persona.edad   = %int(%subst(texto : corte + 1 : %len(texto) - corte));

dsply ('Persona(nombre=' + persona.nombre +
       ', edad=' + %char(persona.edad) + ')');

*inlr = *on;
return;
""", """
**Lo que esta clase enseña en RPG.** La **estructura de datos** de RPG comparte con COBOL la
propiedad decisiva: **es a la vez una estructura con campos y un bloque de bytes**, así que describe
directamente el formato de un registro de fichero.

Y RPG añade una capacidad que ya se mencionó en la clase 091 y que aquí se ve en su papel principal:

```rpgle
dcl-ds cliente likerec(CLIREG : *input);      // la forma EXACTA de la tabla
dcl-ds cliente extname('CLIENTES') qualified end-ds;   // desde el catálogo
```

**`extname` construye la estructura leyendo la definición de la tabla en el catálogo del sistema al
compilar.** Si alguien añade una columna, la estructura la tiene al recompilar. No hay generador de
código, no hay fichero intermedio y no hay desincronización posible entre el esquema y el programa.

Eso es posible porque en IBM i **la base de datos es parte del sistema operativo** y su catálogo está
disponible para el compilador. Es una integración que en otras plataformas se persigue con
herramientas —generadores desde el esquema, migraciones tipadas— y aquí es una palabra clave.

Sobre objetos: **RPG no tiene orientación a objetos**, y es el único de los lenguajes generales de
esta página junto con PL/I y M que no la añadió.

La razón es la misma que en COBOL: el trabajo de RPG es transformar registros, y para eso la
estructura de datos con procedimientos en un módulo (clase 087) es suficiente. IBM sí dio la salida
para cuando hace falta: **RPG llama a Java directamente**, con `extproc(*java)`, y ese es el camino
oficial cuando un programa necesita objetos de verdad.

```rpgle
dcl-pr crearLista object(*java : 'java.util.ArrayList')
       extproc(*java : 'java.util.ArrayList' : *constructor);
end-pr;
```

Un lenguaje de 1959 instanciando objetos Java desde su sintaxis. Es una de las imágenes que mejor
resumen esta sección del curso.
"""),
        "pli": ("""
 persona: procedure options(main);

    declare 1 reg,
              2 nombre char(20) varying,
              2 edad   fixed binary(31);

    declare linea char(200) varying;
    declare corte fixed binary(31);

    get edit (linea) (a(200));
    linea = trim(linea);

    corte = index(linea, ' ');
    reg.nombre = substr(linea, 1, corte - 1);
    reg.edad   = substr(linea, corte + 1);

    put skip list ('Persona(nombre=' || reg.nombre ||
                   ', edad=' || trim(char(reg.edad)) || ')');

 end persona;
""", """
**Lo que esta clase enseña en PL/I.** La estructura de PL/I es la de COBOL con más potencia (clases
091 y 095): niveles numerados, asignación `by name`, operaciones sobre estructuras completas y
combinación libre con arreglos.

Y **PL/I nunca añadió orientación a objetos**. Es el único lenguaje de propósito general de esta
página del que se puede decir eso sin matices —COBOL la añadió en 2002, Fortran en 2003, Ada en 1995,
Pascal y RPG en los noventa—.

La razón es de calendario: **PL/I dejó de evolucionar en los años ochenta**, justo cuando la
orientación a objetos se generalizaba. El último estándar ANSI es de 1987 —con el subconjunto de 1981
antes—, y a partir de ahí los compiladores de IBM añadieron extensiones propias pero ninguna revisión
del lenguaje. No hubo un comité que lo llevara a los noventa.

Lo que sí ofrece IBM Enterprise PL/I moderno son extensiones muy prácticas, y conviene conocerlas
porque cambian la impresión de que es un lenguaje congelado:

```pli
%include <fichero>;              /* inclusión */
define alias entero fixed bin(31);          /* alias de tipo */
define structure 1 punto, 2 x float, 2 y float;   /* TIPO estructura reutilizable */
declare p type(punto);                       /* declarar por su tipo */
```

**`define structure` y `type`** son de verdad importantes: hasta ellas, cada declaración repetía la
estructura entera —el equivalente de no tener `typedef`—. Con ellas, PL/I tiene tipos de registro con
nombre, lo que Ada tenía en 1983.

Y hay soporte moderno para XML, para llamar a Java y a C, y para Unicode con `widechar`. El lenguaje
sigue mantenido y sigue compilando código de 1970 sin tocarlo, que es exactamente lo que su público
pide.

Es un caso claro de lo que documenta esta sección: **no todos los lenguajes vivos se han modernizado
igual**, y decirlo es parte del rigor.
"""),
        "mumps": ("""
PERSONA ; Registros -- clase 099
 read linea
 set p("nombre") = $piece(linea, " ", 1)
 set p("edad") = $piece(linea, " ", 2)
 write "Persona(nombre=", p("nombre"), ", edad=", p("edad"), ")", !
 quit
""", """
**Lo que esta clase enseña en M.** El registro de M es **un array con subíndices de texto**, y no hay
que declarar nada:

```mumps
 set p("nombre") = "Ada"
 set p("edad") = 36
 set p("direccion", "calle") = "..."      ; anidado, sin declarar
```

Es un diccionario, es un registro y es un árbol, a la vez (clase 095). Y con `^` delante, es una fila
persistente:

```mumps
 set ^PAC(id, "nombre") = "Ada"
```

Lo que M no tiene es **esquema**: nada dice qué campos existen, de qué tipo son ni cuáles son
obligatorios. Y en un sistema de millones de líneas eso sería insostenible, así que VistA construyó la
capa que falta: **FileMan**, que ya apareció en la clase 087.

FileMan es un **diccionario de datos escrito en M**, de 1982, y hace lo que hoy hace un ORM más un
esquema más un validador:

```text
Fichero 2 (PATIENT)
  Campo .01  NAME       tipo FREE TEXT, obligatorio, 3-30 caracteres
  Campo .03  DOB        tipo DATE
  Campo .02  SEX        tipo SET OF CODES ("M:MALE;F:FEMALE")
```

Con esa definición, FileMan **genera la validación, los índices, las pantallas de entrada de datos,
los informes y la auditoría**. Y el código de aplicación accede con sus APIs, no tocando los *globals*
directamente.

Hay dos cosas notables aquí. La primera es que **el diccionario de datos está guardado en globals**,
así que FileMan se describe a sí mismo — un catálogo de sistema escrito en la misma estructura que los
datos.

La segunda es que **eso es exactamente lo que hoy se llama base de datos documental sin esquema con
validación en la capa de aplicación**, y funciona en cientos de hospitales desde hace cuarenta años.

Objetos, M no tiene. **InterSystems IRIS sí**: su lenguaje ObjectScript, descendiente directo de M,
añadió clases, herencia y persistencia de objetos, y **un objeto se puede consultar a la vez como
objeto, como tabla SQL y como global**. Es la modernización más ambiciosa de esta página.
"""),
        "smalltalk": ("""
| partes p |

partes := stdin nextLine substrings.

"En Smalltalk no hay registros: hay objetos. Un Dictionary hace de registro anónimo."
p := Dictionary new.
p at: #nombre put: (partes at: 1).
p at: #edad   put: (partes at: 2).

Transcript
    show: 'Persona(nombre=', (p at: #nombre),
          ', edad=', (p at: #edad), ')';
    cr.
""", """
**Lo que esta clase enseña en Smalltalk.** **Smalltalk no tiene registros.** No hay `record`, no hay
`struct` y no hay agregado sin comportamiento: si algo tiene campos, es un objeto, y si es un objeto,
tiene una clase.

```smalltalk
Object subclass: #Persona
    instanceVariableNames: 'nombre edad'
    classVariableNames: ''
    package: 'Ejemplo'.

Persona >> nombre        ^nombre
Persona >> nombre: unV   nombre := unV
Persona >> printOn: unFlujo
    unFlujo nextPutAll: 'Persona(nombre=', nombre, ', edad=', edad printString, ')'
```

Y ahí está la aportación que hay que subrayar: **`printOn:`**.

Todo objeto de Smalltalk hereda `printString`, que llama a `printOn:`. Redefiniéndolo, **el objeto
decide cómo se muestra en el depurador, en el inspector, en el Transcript y al imprimirlo** — en
todos los sitios a la vez, con un método.

Eso es lo que en Java es `toString`, en Python `__repr__`, en Rust `Display` y en C++ `operator<<`, y
**los cuatro descienden de aquí**.

Y hay un detalle de diseño que lo distingue de `toString`: `printOn:` recibe **un flujo**, no devuelve
una cadena. Así, imprimir un objeto que contiene otros mil no construye mil cadenas intermedias:
todos escriben en el mismo flujo. Es una decisión de eficiencia tomada en 1980 que Java no tomó, y de
ahí que exista `StringBuilder` como parche.

Fíjate también en cómo se declara una clase: **`Object subclass: #Persona instanceVariableNames: ...`
es un MENSAJE enviado a la clase `Object`**. No hay sintaxis de declaración de clases: crear una clase
es enviar un mensaje, en ejecución, y por eso se pueden crear clases mediante programa.

Ese es el fondo del asunto y el punto en el que Smalltalk sigue siendo distinto de casi todo: **no hay
nada en el lenguaje que no sea un objeto recibiendo un mensaje**. Ni siquiera declarar una clase.
"""),
    },
)
