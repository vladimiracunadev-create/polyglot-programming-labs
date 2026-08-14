# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 113

> [⬅️ Volver a la clase 113](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Un objeto con un método propio, sin clase que lo defina. Es el modelo de JavaScript, y viene de un
sitio que este curso ya ha nombrado: **Self, un descendiente directo de Smalltalk creado en Xerox PARC
y Sun en 1987**. De estos doce lenguajes, **tres lo soportan de verdad** —Tcl con `oo::objdefine`,
Perl con clausuras y Lisp con listas de asociación— y los demás no pueden ni acercarse.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es el **objeto sin clase: comportamiento por objeto y delegación en lugar de
> herencia**, y estos lenguajes lo enseñan por contraste. **Los compilados con tipos estáticos —COBOL,
> Fortran, Ada, Pascal, C++, RPG, PL/I— no pueden tenerlo**, y no por falta de ganas: si el conjunto de
> métodos de un objeto puede cambiar en ejecución, **la disposición de memoria y la tabla de despacho
> dejan de ser conocidas al compilar**, que es justo lo que esos lenguajes garantizan.
>
> Y los dinámicos lo tienen casi gratis: **en Tcl, Perl, Lisp y Smalltalk un objeto ya es una tabla, y
> añadirle una entrada es añadirle un método**.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: un entero `n` → stdout: `resultado=<2n>`
- **Regla:** `objeto.doble() = valor·2`

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
PROGRAM-ID. PROTO.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  OBJETO.
    05  VALOR  PIC S9(9)  COMP-3 VALUE 0.
01  RESULT  PIC S9(18) COMP-3.
01  ED-R    PIC -(17)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    COMPUTE VALOR = FUNCTION NUMVAL(LINEA)

    PERFORM DOBLE

    MOVE RESULT TO ED-R
    DISPLAY "resultado=" FUNCTION TRIM(ED-R)
    STOP RUN.

DOBLE.
    COMPUTE RESULT = VALOR * 2.
```

**Lo que esta clase enseña en COBOL.** **COBOL no puede tener prototipos**, y la razón es
arquitectónica, no una omisión: **la disposición de un `01` se fija al compilar**, y todo el modelo del
lenguaje —el `MOVE` de grupo que copia bytes, el `REDEFINES`, el registro que es el formato del
fichero— depende de que esa forma sea conocida y estable.

Un objeto al que se le pueden añadir campos y métodos en ejecución es incompatible con eso.

Y merece decir que esa rigidez es exactamente lo que se le pide: **un registro COBOL escrito hoy tiene
que ser leído dentro de veinte años por un programa distinto**, y su forma es un contrato entre
sistemas (clase 106).

Lo más cerca que llega COBOL de la idea de delegación es el **`CALL` dinámico** de la clase 085: el
comportamiento se decide en ejecución buscando un programa por nombre.

```cobol
MOVE TABLA-METODO(INDICE) TO NOMBRE-PROGRAMA
CALL NOMBRE-PROGRAMA USING OBJETO
```

Con una tabla en base de datos que asocia cada objeto a sus programas, se consigue **comportamiento
por instancia decidido en ejecución** — que es la definición funcional de un prototipo. Y como
siempre en COBOL, **con toda la flexibilidad y ninguna comprobación**.

Y hay un mecanismo del entorno que da a esta clase una vuelta interesante: **los objetos programables
de CICS y las salidas de usuario**. Un sistema transaccional permite **registrar un programa que se
invocará en un punto concreto** —antes de grabar, al validar, al abrir— sin recompilar el sistema.

```text
CEDA DEFINE PROGRAM(VALIDA01) GROUP(MIAPP)
```

Eso es delegación configurada en tiempo de instalación: **el comportamiento de un punto del sistema se
cambia registrando otro programa**. No es un prototipo, y resuelve el mismo problema práctico —
adaptar el comportamiento sin tocar el código— que es para lo que los prototipos se usan de verdad.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program proto
   implicit none

   type :: objeto
      integer :: valor = 0
   contains
      procedure :: doble
   end type objeto

   type(objeto) :: o
   integer :: n

   read(*, *) n
   o%valor = n

   write(*, '(A,I0)') 'resultado=', o%doble()

contains

   function doble(self) result(r)
      class(objeto), intent(in) :: self
      integer :: r
      r = self%valor * 2
   end function doble

end program proto
```

**Lo que esta clase enseña en Fortran.** Fortran es el lenguaje de esta página **más lejos posible de
los prototipos**, y la razón se entiende mirando para qué existe: **el compilador debe conocer la
disposición exacta de cada dato para vectorizar, para paralelizar y para colocar arreglos en memoria
contigua**.

Un objeto cuya forma cambia en ejecución destruye todo eso.

Lo más cercano que ofrece es lo que ya apareció en la clase 112: **campos que son punteros a
procedimiento**, asignados al construir el objeto.

```fortran
type :: modelo
   integer :: valor = 0
   procedure(op_i), pointer, nopass :: doble => null()
end type

m%doble => version_rapida        ! el "método" se decide en EJECUCIÓN
```

Eso es comportamiento por instancia, y es lo más parecido a un prototipo que Fortran puede tener: **la
forma del objeto sigue siendo fija —un entero y un puntero— pero a qué apunta ese puntero se decide en
marcha**.

Y tiene un uso real en códigos científicos: **seleccionar el algoritmo según el tamaño del problema o
el hardware disponible**, sin un `if` en el bucle interior.

```fortran
if (n < 1000) then
   m%resolver => directo
else
   m%resolver => iterativo
end if
```

La diferencia con un prototipo de verdad es que **el conjunto de "métodos" está declarado en el tipo**:
se puede cambiar a qué apuntan, no cuántos hay ni cómo se llaman.

Y aquí conviene decir algo que esta parte del curso ha ido mostrando: **la rigidez de Fortran no es
antigüedad, es el precio de su ventaja**. Es el lenguaje más rápido de esta página en cálculo numérico
precisamente porque no permite nada que impida al compilador saberlo todo de antemano.

Cambiar eso para tener prototipos sería cambiar Fortran por otro lenguaje.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Proto is
   --  Ada no tiene prototipos: lo más cercano es un campo que es un
   --  ACCESO A SUBPROGRAMA, decidido en ejecución (clase 085).
   type Operacion is access function (X : Integer) return Integer;

   type Objeto is record
      Valor : Integer := 0;
      Doble : Operacion := null;
   end record;

   function Por_Dos (X : Integer) return Integer is (X * 2);

   O : Objeto;
   N : Integer;
begin
   Get (N);

   O.Valor := N;
   O.Doble := Por_Dos'Access;      --  el "método" se asigna al objeto

   Put ("resultado=");
   Put (O.Doble (O.Valor), Width => 1);
   New_Line;
end Proto;
```

**Lo que esta clase enseña en Ada.** Ada **no tiene prototipos y no puede tenerlos**, por la misma
razón que se explicó en la clase 111: **la tabla de despacho de un tipo etiquetado se congela al
terminar la especificación del paquete donde se declara**.

Esa decisión es lo que permite garantizar que **una llamada despachada tiene coste constante y
acotado**, que es un requisito de los sistemas de tiempo real donde Ada vive.

Lo que sí ofrece es lo que hace este programa: **un campo que es un acceso a subprograma**, con lo que
cada instancia puede tener un comportamiento distinto.

```ada
type Operacion is access function (X : Integer) return Integer;
O.Doble := Por_Dos'Access;
```

Y con la comprobación de accesibilidad de la clase 083: **no se puede asignar un subprograma que viva
menos que el tipo del acceso**, lo que impide guardar un puntero a algo que va a desaparecer.

Ada tiene además dos mecanismos que cubren, con garantías, los usos legítimos de un prototipo:

**Los tipos con discriminante** (clase 100), que permiten que una instancia tenga forma distinta según
un valor conocido al crearla:

```ada
type Buffer (Tamano : Natural) is record
   Datos : String (1 .. Tamano);
end record;
```

**Y los genéricos con parámetros formales de subprograma** (clase 078):

```ada
generic
   with function Transformar (X : Integer) return Integer;
package Procesador is ... end Procesador;
```

Cada instanciación es un paquete distinto con un comportamiento distinto, **resuelto en compilación y
sin coste en ejecución**.

Esa es la respuesta característica de Ada a todo lo que en un lenguaje dinámico se resuelve en marcha:
**mover la decisión a la compilación y conservar la comprobación**. Es más rígido, es más verboso, y
es lo que permite certificar el software que vuela.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Proto;
{$MODE OBJFPC}{$H+}
uses SysUtils;

type
  TOperacion = function(X: Integer): Integer;

  TObjeto = record
    Valor: Integer;
    Doble: TOperacion;         { el "método" es un CAMPO }
  end;

function PorDos(X: Integer): Integer;
begin
  Result := X * 2;
end;

var
  O: TObjeto;
  N: Integer;

begin
  Read(N);

  O.Valor := N;
  O.Doble := @PorDos;           { se asigna al objeto, no a la clase }

  WriteLn('resultado=', IntToStr(O.Doble(O.Valor)));
end.
```

**Lo que esta clase enseña en Pascal.** Object Pascal no tiene prototipos, y tiene la pieza que más se
les acerca de todos los lenguajes compilados de esta página: **el tipo `of object`** de la clase 085.

```pascal
type
  TMetodo = function(X: Integer): Integer of object;   { método + INSTANCIA }
  TAnonima = reference to function(X: Integer): Integer; { CLAUSURA }

var
  O: TObjeto;
begin
  O.Doble := Otro.Calcular;       { un método de OTRO objeto, con su estado }
  O.Doble := function(X: Integer): Integer
             begin Result := X * 3 end;   { una lambda, Delphi 2009 }
end;
```

Un campo `of object` guarda **el método y el objeto al que pertenece**, así que asignarle el método de
otra instancia es **delegación de verdad**: el comportamiento y su estado viajan juntos.

Ese es el mecanismo sobre el que está construido todo el modelo de eventos de Delphi (clase 107), y es
literalmente delegación por objeto:

```pascal
Boton1.OnClick := Formulario.GuardarClick;
Boton2.OnClick := Formulario.GuardarClick;    { el MISMO comportamiento }
Boton3.OnClick := OtroModulo.CancelarClick;    { otro, en otro objeto }
```

Cada botón tiene su propio comportamiento, asignado en ejecución, sin heredar de nada. **Es
programación basada en prototipos con otro nombre**, limitada a los campos declarados en el tipo.

Y con las **funciones anónimas** de Delphi 2009 y Free Pascal 3.2, se puede asignar una clausura
construida al vuelo, con lo que el comportamiento ni siquiera tiene que existir como método:

```pascal
O.Doble := function(X: Integer): Integer
           begin Result := X * Factor end;    { captura Factor }
```

La diferencia con un prototipo real sigue siendo la del cierre: **el conjunto de campos está fijado en
el tipo**. Se puede cambiar el comportamiento de cada uno, no añadir uno nuevo.

Y para eso, Free Pascal ofrece la reflexión con RTTI extendida (clase 105), que permite descubrir y
llamar métodos por nombre en ejecución — lento, y disponible.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let* ((n (read))
       ;; Un "prototipo": una lista de asociación con datos Y funciones
       (proto (list (cons :doble (lambda (o) (* 2 (cdr (assoc :valor o)))))))
       ;; Un objeto: sus propios datos, delegando el método al prototipo
       (obj (cons (cons :valor n) proto)))
  (format t "resultado=~D~%"
          (funcall (cdr (assoc :doble obj)) obj)))
```

**Lo que esta clase enseña en Common Lisp.** Este programa muestra el modelo de prototipos en su forma
mínima, y en Lisp sale casi solo por lo que se vio en la clase 095: **una lista de asociación con un
prototipo delante es delegación**.

```lisp
(cons (cons :valor n) proto)
```

Buscar `:doble` en `obj` **no lo encuentra en la primera celda y sigue por el resto, que es el
prototipo**. Esa es exactamente la cadena de prototipos de JavaScript, implementada con `assoc` y sin
ninguna maquinaria.

Y añadir una propiedad propia que **oculte** la del prototipo es poner otra celda delante:

```lisp
(acons :doble (lambda (o) 0) obj)     ; este objeto ahora tiene SU doble
```

Es *shadowing* por construcción, y era el idioma habitual de Lisp para entornos y ámbitos décadas
antes de que JavaScript existiera.

Common Lisp tiene además dos formas más de conseguir comportamiento por objeto:

**Las clausuras como objetos** (clase 087):

```lisp
(defun crear-contador ()
  (let ((n 0))
    (lambda (msg)
      (case msg
        (:incrementar (incf n))
        (:valor n)))))
```

Un objeto con estado **verdaderamente privado** y su propio despacho, sin clases. Es el patrón que
Abelson y Sussman enseñan en *Structure and Interpretation of Computer Programs*, y es prototípico
puro.

**Y el MOP** (clase 110), que permite lo que ningún lenguaje de clases ofrece:

```lisp
(defclass prototipo (standard-class) ())
(defmethod validate-superclass ((c prototipo) (s standard-class)) t)
```

**Con una metaclase propia se puede implementar un sistema de prototipos completo dentro de CLOS**, y
se ha hecho — hay bibliotecas que lo ofrecen. El sistema de objetos de Lisp es lo bastante abierto
como para albergar otro sistema de objetos distinto.

Es la conclusión que esta parte del curso repite: **en Lisp, un paradigma es una biblioteca**.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea
set n [string trim $linea]

#  Un objeto SIN clase, con métodos propios: prototipos en TclOO
set obj [oo::object new]
oo::objdefine $obj {
    variable valor
    method fijar {v} { set valor $v }
    method doble {}  { return [expr {$valor * 2}] }
}

$obj fijar $n
puts "resultado=[$obj doble]"
```

**Lo que esta clase enseña en Tcl.** Tcl es de los pocos lenguajes de esta página que soporta **los dos
modelos a la vez**, y este programa usa el prototípico: **`oo::object new` crea un objeto sin clase
propia y `oo::objdefine` le añade métodos que solo tiene él**.

```tcl
set obj [oo::object new]
oo::objdefine $obj {
    method doble {} { ... }
}
```

Ese objeto **no pertenece a ninguna clase que declare `doble`**. El método vive en el objeto.

Y la maquinaria que lo hace posible es elegante: **por debajo, TclOO crea una clase anónima para ese
objeto** —su *clase por objeto*— y mete ahí los métodos. Es exactamente lo que hace Ruby con las
*singleton classes* y lo que Smalltalk hace con las metaclases.

El repertorio completo de manipulación por objeto es amplio:

```tcl
oo::objdefine $obj method nuevo {} { ... }     ;# añadir un método
oo::objdefine $obj mixin Registrable            ;# mezclar comportamiento
oo::objdefine $obj forward abrir $otro abrir     ;# DELEGAR a otro objeto
oo::objdefine $obj class OtraClase                ;# CAMBIAR su clase
```

**`forward`** merece atención porque es delegación explícita: `$obj abrir ...` se reenvía tal cual a
`$otro abrir ...`. Es lo que en Delphi hace `implements` (clase 111) y en Ruby `delegate`.

**Y `class`** cambia la clase de un objeto existente, como el `change-class` de CLOS (clase 111).

La combinación —clases para lo estructural, comportamiento por objeto para las excepciones— es
exactamente lo que el cierre de esta clase recomienda, y Tcl es de los pocos que la ofrece sin
esfuerzo.

Hay que señalar el coste: **cada objeto con métodos propios lleva una clase anónima**, con su memoria
y su entrada en la caché de resolución de métodos. Para unos pocos objetos especiales es
insignificante; para un millón, no.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $n = <STDIN>;
chomp $n;

#  Un prototipo: un hash con datos Y funciones
my $proto = {
    doble => sub { my $self = shift; return $self->{valor} * 2 },
};

#  Un objeto: se CLONA el prototipo y se le pone su propio estado
my $obj = { %$proto, valor => $n + 0 };

print "resultado=", $obj->{doble}->($obj), "\n";
```

**Lo que esta clase enseña en Perl.** El objeto de este programa **es un hash con funciones dentro**, y
`{ %$proto, valor => ... }` lo **clona** copiando las entradas del prototipo y añadiendo estado propio.

Es programación basada en prototipos hecha con las estructuras normales del lenguaje, y funciona
porque en Perl **una función es un valor** (clase 085) y **un hash acepta cualquier cosa como valor**.

Y Perl tiene además el mecanismo que lo convierte en delegación de verdad, ya nombrado en la clase
111: **`AUTOLOAD`**.

```perl
sub AUTOLOAD {
    my $self = shift;
    our $AUTOLOAD;
    (my $m = $AUTOLOAD) =~ s/.*:://;
    return $self->{$m}->($self, @_) if ref $self->{$m} eq 'CODE';
    return $self->{padre}->$m(@_) if $self->{padre};   # DELEGAR al prototipo
    die "no entiendo $m";
}
```

Con eso, `$obj->doble` busca el método **primero en el propio hash y después en el objeto padre**, que
es literalmente la cadena de prototipos de JavaScript.

`AUTOLOAD` es el `doesNotUnderstand:` de Smalltalk (clase 051), y esta clase es donde su uso es más
natural.

Y Perl tiene una tercera vía que es la más elegante y la más privada, la de la clase 087: **objetos
hechos con clausuras**.

```perl
sub crear {
    my $valor = shift;
    my %self;
    %self = (
        doble => sub { $valor * 2 },
        fijar => sub { $valor = shift },
    );
    return \%self;
}
```

`$valor` **no está en el hash**: es una variable léxica capturada por las clausuras, así que **no hay
forma de acceder a ella desde fuera**. Es más privado que cualquier campo de un objeto bendecido, y es
el mismo patrón que en Lisp (clase 087) y en JavaScript antes de los campos privados.

Y a esta clase le corresponde una advertencia de rendimiento: **cada objeto lleva su propia copia de
todas las funciones**, así que un millón de objetos son un millón de clausuras. Con `bless` y una
clase, las subrutinas se comparten. Es el mismo compromiso que en Tcl.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <functional>
#include <iostream>
#include <map>
#include <string>

int main() {
    int n{};
    if (!(std::cin >> n)) return 1;

    //  Lo más cerca de un objeto-prototipo en C++: un mapa de nombre a función
    std::map<std::string, std::function<int()>> obj;
    obj["doble"] = [n] { return n * 2; };

    std::cout << "resultado=" << obj["doble"]() << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** **C++ no tiene prototipos y no puede tenerlos**, y merece
entenderse el porqué con precisión, porque no es dogma.

En C++, **el tipo de un objeto determina su tamaño, la disposición de sus campos y su tabla de métodos
virtuales, todo en compilación**. Un `sizeof(T)` es una constante. Añadir un método a una instancia en
ejecución obligaría a que la tabla fuera dinámica y a que el objeto llevara información de sus métodos
— exactamente lo que el modelo de C++ evita para que un objeto sin virtuales cueste cero.

Lo que sí se puede es lo de este programa: **guardar funciones en el objeto**.

```cpp
struct Objeto {
    int valor = 0;
    std::function<int(int)> doble;          // comportamiento por INSTANCIA
};

Objeto o;
o.doble = [](int x) { return x * 2; };
o.doble = [factor](int x) { return x * factor; };   // con estado capturado
```

Es delegación por objeto, con las advertencias de la clase 085: **`std::function` borra el tipo, lo
que implica indirección y posiblemente una reserva de memoria**. Para un caso puntual es correcto;
en un bucle caliente no.

Y esta clase es buen sitio para mencionar el idioma de C++ que resuelve el problema real que los
prototipos suelen resolver —**adaptar un objeto sin tocar su clase**— con coste cero: el **borrado de
tipos hecho a mano**.

```cpp
class Dibujable {
    struct Concepto { virtual void dibujar() const = 0; virtual ~Concepto() = default; };
    template <typename T> struct Modelo : Concepto {
        T obj;
        void dibujar() const override { obj.dibujar(); }   // duck typing
    };
    std::unique_ptr<Concepto> p;
public:
    template <typename T> Dibujable(T x) : p(std::make_unique<Modelo<T>>(std::move(x))) {}
    void dibujar() const { p->dibujar(); }
};
```

Ese patrón permite meter en un mismo contenedor **cualquier tipo que sepa dibujarse, sin que herede de
nada ni sepa que `Dibujable` existe**. Es lo que hace `std::function` internamente, y lo que en Rust
son los objetos de *trait*.

Sean Parent lo popularizó con una charla célebre cuyo argumento resume esta clase: **la herencia es la
clase base de todo mal**, y la alternativa es composición con borrado de tipos.

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

dcl-pi PROTO;
  n int(10) const;
end-pi;

// RPG no tiene objetos ni prototipos. Lo mas cercano: una estructura
// con un PUNTERO a procedimiento, asignado en ejecucion (clase 085).
dcl-pr aplicar int(20) extproc(metodo);
  x int(10) const;
end-pr;

dcl-ds objeto qualified;
  valor  int(10);
  metodo pointer;
end-ds;

dcl-s metodo pointer;

objeto.valor = n;
objeto.metodo = %paddr('POR_DOS');
metodo = objeto.metodo;

dsply ('resultado=' + %char(aplicar(objeto.valor)));

*inlr = *on;
return;

dcl-proc POR_DOS export;
  dcl-pi *n int(20);
    x int(10) const;
  end-pi;
  return x * 2;
end-proc;
```

**Lo que esta clase enseña en RPG.** RPG no tiene objetos, así que tampoco prototipos, y lo que hace
este programa es lo único posible: **una estructura con un puntero a procedimiento**, asignado con
`%paddr` en ejecución (clase 085).

Es comportamiento por instancia, con la misma advertencia de siempre: **`%paddr` resuelve por nombre y
nadie comprueba que la firma encaje**.

Lo que sí tiene la plataforma IBM i, y es el mecanismo que en la práctica cubre lo que los prototipos
resuelven, son los **programas de salida** (*exit programs*).

```text
ADDEXITPGM EXITPNT(QIBM_QZDA_INIT) FORMAT(ZDAI0100) PGM(MIBIB/MIVALIDA)
```

Un **punto de salida** es un lugar del sistema operativo donde se puede **registrar un programa
propio** que se invocará automáticamente: al conectarse por FTP, al abrir una sesión ODBC, al validar
una contraseña, al arrancar un trabajo.

Hay más de un centenar de puntos de salida documentados, y con ellos **se cambia el comportamiento del
sistema operativo sin modificarlo**. Es delegación configurada, exactamente como las salidas de CICS
que se mencionaron en la página de COBOL.

Y hay una segunda vía, más moderna: **los disparadores de base de datos**.

```sql
CREATE TRIGGER validar BEFORE INSERT ON clientes
  FOR EACH ROW MODE DB2ROW
  BEGIN ... END
```

O un disparador escrito en RPG, registrado con `ADDPFTRG`. **El comportamiento se asocia al dato, no
al programa**, y se aplica a todos los programas que toquen esa tabla — incluidos los que se escriban
dentro de diez años.

Ese es el patrón que recorre toda esta parte del curso en las plataformas de gestión: **cuando el
lenguaje no ofrece la extensibilidad, la ofrece el sistema**, y a menudo en un sitio más útil.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 proto: procedure options(main);

    /*  PL/I no tiene objetos. Lo mas cercano: una estructura con una
        variable ENTRY, es decir, un procedimiento guardado en un campo. */
    declare 1 objeto,
              2 valor fixed binary(31),
              2 doble entry (fixed binary(31))
                      returns (fixed binary(31)) variable;

    declare n fixed binary(31);

    get list (n);

    objeto.valor = n;
    objeto.doble = por_dos;         /* el "metodo" se asigna al objeto */

    put skip list ('resultado=' || trim(char(objeto.doble(objeto.valor))));

 por_dos: procedure (x) returns (fixed binary(31));
    declare x fixed binary(31);
    return (x * 2);
 end por_dos;

 end proto;
```

**Lo que esta clase enseña en PL/I.** Este programa hace algo que sorprende viniendo de un lenguaje de
1964: **guarda un procedimiento dentro de una estructura**.

```pli
 declare 1 objeto,
           2 valor fixed binary(31),
           2 doble entry (...) returns (...) variable;

 objeto.doble = por_dos;
 resultado = objeto.doble(objeto.valor);
```

Es la **variable `entry`** de la clase 085 usada como campo, y con eso cada instancia puede tener su
propio comportamiento. Comportamiento por objeto, en PL/I, sesenta años antes de esta clase.

Y con `based` y punteros (clase 090), la estructura se puede reservar dinámicamente y encadenar:

```pli
 declare 1 objeto based(p),
           2 padre pointer,                 /* la CADENA de prototipos */
           2 doble entry (...) variable;
```

Un campo `padre` que apunta a otro objeto, y una búsqueda que sube por la cadena si el campo está
vacío. **Eso es exactamente el modelo de JavaScript**, escrito a mano y sin ninguna comprobación.

Lo que falta, como en las clases 110 y 111, es lo mismo: **la sintaxis que lo haga cómodo y el
compilador que lo compruebe**. Nadie garantiza que `doble` esté asignado antes de llamarlo, y llamar a
una variable `entry` no inicializada es un salto a una dirección arbitraria.

PL/I ilustra bien la idea de fondo de esta clase entera: **los prototipos no requieren nada exótico —
requieren que un objeto sea una tabla y que las funciones sean valores**. Cualquier lenguaje con esas
dos cosas los puede tener.

Lo que separa a JavaScript y a Self de PL/I no es la capacidad: es que **allí es el modelo del
lenguaje y aquí es una técnica de programador**, sin comprobación, sin herramientas y sin comunidad
que la reconozca.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
PROTO ; Prototipos -- clase 113
 read n
 ; un "objeto": un array con datos, y metodos como NOMBRES DE ETIQUETA
 new obj
 set obj("valor") = n
 set obj("doble") = "pordos^PROTO"
 ; despacho: la etiqueta guardada en el objeto se invoca por indireccion
 write "resultado=", $$@(obj("doble"))(obj("valor")), !
 quit
 ;
pordos(x) quit x * 2
```

**Lo que esta clase enseña en M.** M no tiene objetos, y sin embargo este programa hace algo muy
parecido a un prototipo, con las dos piezas que ya conocemos: **un array como tabla de propiedades** y
**la indirección** (clase 085).

```mumps
 set obj("valor") = n
 set obj("doble") = "pordos^PROTO"
 set r = $$@(obj("doble"))(obj("valor"))
```

**El método es un dato**: una cadena con el nombre de la etiqueta, guardada en el propio objeto. Y
como los arrays de M son multinivel y sin esquema (clase 089), añadir una propiedad o un método es una
asignación más.

La delegación se escribe con la misma naturalidad:

```mumps
 set obj("padre") = "^PROTOTIPOS(""animal"")"
 if '$data(obj("doble")) set metodo = @obj("padre")@("doble")
```

Y aquí está lo que hace único a M en esta clase: **con `^` delante, el prototipo está en disco y lo
comparten todos los procesos**.

```mumps
 set ^PROTO("animal", "sonido") = "generico^SONIDOS"
 set ^PROTO("perro", "padre") = "animal"
 set ^PROTO("perro", "sonido") = "guau^SONIDOS"
```

Eso es una **jerarquía de prototipos persistente**, modificable en caliente y visible para todo el
sistema. Cambiar el comportamiento de todos los "perros" del hospital es una asignación.

Es exactamente lo que hace FileMan (clase 099) para las validaciones y los cálculos: **el diccionario
de datos guarda código M como cadenas**, y lo ejecuta por indirección cuando toca.

```text
Campo .01 NAME
   INPUT TRANSFORM: K:$L(X)>30!($L(X)<3) X
```

Ese `INPUT TRANSFORM` es **código M guardado como dato**, ejecutado al validar el campo. Es
comportamiento asociado al dato y modificable sin recompilar nada.

Con todas las virtudes y todos los peligros que cabe esperar — y funcionando en cientos de hospitales
desde 1982.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| n obj |

n := stdin nextLine trimBoth asNumber.

"Smalltalk es de clases, pero un bloque hace de objeto-prototipo mínimo:
 estado capturado y comportamiento propio."
obj := Dictionary new.
obj at: #valor put: n.
obj at: #doble put: [ :o | (o at: #valor) * 2 ].

Transcript show: 'resultado=', ((obj at: #doble) value: obj) printString; cr.
```

**Lo que esta clase enseña en Smalltalk.** Smalltalk es **el abuelo de los prototipos**, y la historia
merece contarse porque cierra el círculo de esta clase.

En 1986, en Xerox PARC, **David Ungar y Randall Smith crearon Self**: un lenguaje que tomaba Smalltalk
y **le quitaba las clases**. La tesis era que las clases son una complicación innecesaria — basta con
objetos que se clonan y delegan.

```text
"En Self:"
punto = ( | x <- 0. y <- 0. suma = ( x + y ) | )
copia = punto copy
copia x: 3
```

Self no triunfó comercialmente y su influencia fue enorme por dos vías:

1. **Sus técnicas de compilación.** Para hacer rápido un lenguaje sin clases y con despacho totalmente
   dinámico, el equipo de Self inventó las **cachés de línea polimórficas** y la **compilación
   adaptativa con reoptimización** — es decir, el **JIT moderno**. Esa tecnología pasó directamente a
   **HotSpot**, la máquina virtual de Java, porque **fue el mismo equipo el que la construyó**. Cada
   programa Java que corre hoy usa ideas de Self.

2. **Su modelo de objetos.** Brendan Eich cita a Self y a Scheme como las dos influencias declaradas de
   JavaScript, escrito en diez días en 1995. **Los prototipos de JavaScript son los de Self.**

Y en el propio Smalltalk, el comportamiento por objeto **existe** aunque no sea idiomático: Pharo tiene
**clases anónimas**.

```smalltalk
obj := Object new.
obj class instanceVariableNames: ''.
"o, con las herramientas de Pharo:"
obj adoptInstance: (Object subclass) new
```

Y como se dijo en la clase 110, **las clases de Smalltalk ya son objetos con su propia metaclase**, así
que el sistema tiene una clase por clase — la maquinaria de los prototipos está ahí, solo que
reservada al sistema.

Es un buen final para esta clase: **Smalltalk tenía dentro lo que hacía falta para quitarse las
clases**, y alguien lo hizo. De ahí salieron el JIT de Java y el modelo de objetos de JavaScript, que
son dos de las tres o cuatro cosas más ejecutadas del planeta.

---

## Y de vuelta a la clase

Lo transferible: **clases y prototipos no son dos filosofías rivales, son dos puntos de un mismo eje —
cuánto se decide al compilar**. Las clases fijan la forma pronto y a cambio dan comprobación,
velocidad y herramientas; los prototipos la dejan abierta y a cambio dan flexibilidad y adaptación en
caliente. JavaScript, que empezó puramente prototípico, **añadió `class` en 2015** porque los
programas grandes necesitan la estructura; y Tcl, Lisp y Smalltalk, que empezaron con clases,
**añadieron el comportamiento por objeto** porque a veces hace falta la excepción.

⏮️ [Volver a la clase 113](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
