# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 062

> [⬅️ Volver a la clase 062](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Positivo, negativo o cero. Un problema de tres casos elegido porque en un lenguaje moderno se
resuelve con **coincidencia de patrones** —`match` de Rust, `when` de Kotlin, `match` de Python
3.10—, la construcción de moda de la última década. Y la pregunta de esta página es: **¿qué usaban
estos lenguajes antes de que existiera?** Las respuestas son más interesantes de lo esperable.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es la **coincidencia de patrones**, y estos lenguajes lo enseñan porque muestran
> **tres caminos distintos hacia la misma necesidad**. Uno es el de los rangos en la selección: el
> `case (:-1)` de Fortran y el `when Integer'First .. -1` de Ada permiten casar tramos, no valores. Otro
> es el de los **predicados con nombre**: las condiciones de signo y de clase de COBOL —`IF N IS
> POSITIVE`, `IF C IS ALPHABETIC`— son patrones incorporados al lenguaje.
>
> Y el tercero es el más sorprendente: **M tiene un operador de patrones, `?`, desde 1966**, con su
> propia sintaxis para "uno o más dígitos" o "tres letras seguidas de dos números". Un mini-lenguaje de
> validación anterior a las expresiones regulares de Perl.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: un entero `n` → stdout: `signo=<positivo|negativo|cero>`
- **Regla:** `n>0→positivo; n<0→negativo; n==0→cero`

| stdin | esperado |
|---|---|
| `5` | `signo=positivo` |
| `-3` | `signo=negativo` |
| `0` | `signo=cero` |

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
PROGRAM-ID. SIGNO.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  N       PIC S9(9) COMP-3.
01  SIGNO-T PIC X(10).

PROCEDURE DIVISION.
    ACCEPT LINEA
    MOVE FUNCTION NUMVAL(LINEA) TO N

    EVALUATE TRUE
        WHEN N IS POSITIVE   MOVE "positivo" TO SIGNO-T
        WHEN N IS NEGATIVE   MOVE "negativo" TO SIGNO-T
        WHEN OTHER           MOVE "cero"     TO SIGNO-T
    END-EVALUATE

    DISPLAY "signo=" FUNCTION TRIM(SIGNO-T)
    STOP RUN.
```

**Lo que esta clase enseña en COBOL.** `N IS POSITIVE` no es una comparación abreviada: es una
**condición de signo**, una construcción del lenguaje. Y junto a ella COBOL tiene una familia entera
de **predicados incorporados** que son, en la práctica, patrones con nombre:

```cobol
IF N IS POSITIVE / NEGATIVE / ZERO           *> condiciones de SIGNO
IF CAMPO IS NUMERIC                          *> condiciones de CLASE
IF CAMPO IS ALPHABETIC / ALPHABETIC-UPPER
IF CAMPO IS NOT NUMERIC
IF TABLA(I) IS DBCS                          *> juego de caracteres de doble byte
```

`IF CAMPO IS NUMERIC` responde a "¿el contenido de este campo alfanumérico son todo dígitos?", que es
exactamente lo que en Perl se escribiría con `/^\d+$/` y en Tcl con `string is integer`. Es
validación de forma, integrada en el lenguaje, sin biblioteca y sin expresiones regulares — porque en
1959 no existían.

Y COBOL permite **definir tus propias clases**, que es lo que más se acerca a un patrón con nombre:

```cobol
ENVIRONMENT DIVISION.
CONFIGURATION SECTION.
SPECIAL-NAMES.
    CLASS HEXADECIMAL IS "0" THRU "9", "A" THRU "F".

*> y después, en cualquier sitio:
IF CODIGO IS HEXADECIMAL ...
```

Declaras un conjunto de caracteres, le pones nombre, y se convierte en un predicado del lenguaje. No
es descomposición estructural, pero sí es **reconocimiento de forma con nombre reutilizable**, que es
la mitad de lo que hace un `match` moderno.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program signo
   implicit none
   integer :: n
   character(len=10) :: s

   read(*, *) n

   select case (n)
   case (:-1)
      s = 'negativo'
   case (0)
      s = 'cero'
   case (1:)
      s = 'positivo'
   end select

   write(*, '(A,A)') 'signo=', trim(s)
end program signo
```

**Lo que esta clase enseña en Fortran.** `case (:-1)` y `case (1:)` son **rangos abiertos**: "todo lo
menor o igual que −1" y "todo lo mayor o igual que 1". Es la forma que tiene Fortran de casar
**tramos** en lugar de valores, y con ella los tres casos de esta clase quedan cubiertos sin ningún
`if` y sin `case default`.

Esa capacidad —seleccionar por rango— es la primera de las tres piezas que la coincidencia de
patrones moderna reúne, y Fortran la tiene desde 1990.

Fortran añade además la función `sign`, que resuelve esta clase de otra manera muy suya:

```fortran
sign(1, n)        ! el valor absoluto del primero, con el SIGNO del segundo: 1 o -1
sign(1.0, -0.0)   ! -1.0 -- distingue el cero negativo del IEEE 754
```

`sign(a, b)` transfiere el signo de un número a otro. Parece una función extraña hasta que se ve para
qué existe: en cálculo numérico, aplicar el signo de una magnitud a otra sin escribir una rama es
frecuente, y **una expresión sin ramas se vectoriza y una con `if` no**. La misma motivación que
`merge` en la clase 060.

Lo que Fortran **no** tiene, como ninguno de esta página, es la tercera pieza: **descomponer una
estructura** casando su forma. Para eso hay que esperar a ML y a sus descendientes.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Signo is
   N : Integer;
begin
   Get (N);

   --  Los tres rangos cubren TODO Integer: no hace falta `when others`,
   --  y el compilador lo comprueba.
   case N is
      when Integer'First .. -1 => Put_Line ("signo=negativo");
      when 0                   => Put_Line ("signo=cero");
      when 1 .. Integer'Last   => Put_Line ("signo=positivo");
   end case;
end Signo;
```

**Lo que esta clase enseña en Ada.** Este programa **no lleva `when others`**, y eso es lo importante:
los tres rangos cubren todos los valores de `Integer`, **y el compilador lo verifica**. Si borraras
el caso del cero, no compilaría.

Esa comprobación de exhaustividad es la característica que hace valiosa la coincidencia de patrones
moderna, y Ada la tiene desde 1983 aplicada a rangos y enumerados.

Donde Ada se acerca de verdad a un `match` es en los **registros con discriminante**, que son tipos
suma comprobados:

```ada
type Figura (Clase : Tipo_Figura) is record
   case Clase is
      when Circulo    => Radio : Float;
      when Rectangulo => Ancho, Alto : Float;
      when Triangulo  => A, B, C : Float;
   end case;
end record;

case F.Clase is
   when Circulo    => Area := Pi * F.Radio ** 2;      --  solo aquí existe Radio
   when Rectangulo => Area := F.Ancho * F.Alto;
   when Triangulo  => ...
end case;
```

Acceder a `F.Radio` cuando `F.Clase` no es `Circulo` levanta `Constraint_Error`. **El tipo lleva la
etiqueta, los campos dependen de ella, y el compilador exige tratar todas las variantes.** Es
exactamente un `enum` de Rust con sus `match`, escrito con la sintaxis de 1983.

Lo único que falta frente a un `match` moderno es la **ligadura en el patrón**: aquí hay que escribir
`F.Radio`, mientras que Rust permite `Circulo { radio }` y te da la variable ya extraída.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Signo;
{$MODE OBJFPC}{$H+}
uses Math;

var
  N: Integer;
  S: string;

begin
  Read(N);

  case Sign(N) of
     1: S := 'positivo';
    -1: S := 'negativo';
  else
     S := 'cero';
  end;

  WriteLn('signo=', S);
end.
```

**Lo que esta clase enseña en Pascal.** `Sign(N)` de la unidad `Math` devuelve `-1`, `0` o `1`, y
convierte un problema de tres tramos en un `case` de tres valores. Es una técnica general que vale la
pena reconocer: **normalizar el valor a un dominio pequeño y luego seleccionar**, en vez de comparar
tramos.

Pascal tiene además **conjuntos** como tipo del lenguaje, y son la pieza de esta clase que más se
acerca a un patrón:

```pascal
type
  TDigito = set of '0'..'9';
  TVocal  = set of Char;

const
  VOCALES: TVocal = ['a','e','i','o','u','A','E','I','O','U'];

if C in VOCALES then ...
if C in ['a'..'z', 'A'..'Z', '0'..'9'] then ...    { conjunto literal }
if Dia in [Sabado, Domingo] then ...
```

El operador **`in`** comprueba pertenencia a un conjunto, y el conjunto se escribe entre corchetes con
rangos y listas mezclados. Se implementa como una **máscara de bits**, así que la comprobación es una
sola instrucción con independencia de cuántos elementos tenga.

Es más legible que una cadena de `or`, es más rápido, y es una idea que casi ningún lenguaje posterior
copió —Delphi la mantiene, Modula-2 y Ada tienen variantes, y C, Java, Python y JavaScript no tienen
nada equivalente a nivel de lenguaje—. Para reconocer que un valor pertenece a un grupo, sigue siendo
la construcción más limpia de esta página.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let ((n (read)))
  (format t "signo=~A~%"
          (cond ((plusp n)  "positivo")
                ((minusp n) "negativo")
                (t          "cero"))))
```

**Lo que esta clase enseña en Common Lisp.** `plusp`, `minusp` y `zerop` son **predicados con
nombre**, y la convención `-p` final —de *predicate*— recorre toda la biblioteca: `evenp`, `oddp`,
`null`, `listp`, `stringp`, `numberp`. Es la misma idea que las condiciones de clase de COBOL: dar
nombre a una comprobación de forma.

Pero donde Lisp llega más lejos que nadie en esta clase es en la **descomposición estructural**, que
es la pieza que le falta a todos los demás lenguajes de esta página:

```lisp
(destructuring-bind (nombre (calle numero) &optional (pais "ES")) datos
  ...)   ; extrae de una lista anidada, con opcionales y valores por defecto

(defun f (&key (color :rojo) tamano &rest resto) ...)   ; en la propia lambda-lista
```

`destructuring-bind` casa la **forma** de una lista y liga las partes a variables. Es exactamente lo
que hace `let (a, b) = tupla` en Rust o el desempaquetado de Python, disponible desde los años 80.

Y como Lisp permite añadir sintaxis, la coincidencia de patrones completa existe **como biblioteca**:

```lisp
(match figura
  ((list 'circulo r)        (* pi r r))
  ((list 'rect ancho alto)  (* ancho alto))
  ((guard n (numberp n))    n))
```

Eso es `trivia` u `optima`, dos bibliotecas de CPAN… perdón, de Quicklisp. **Lo notable es que
`match` no necesitó cambiar el lenguaje**: es una macro. Es la demostración práctica de para qué
sirve la homoiconicidad de la clase 041 — cuando aparece una idea nueva de diseño de lenguajes, en
Lisp se implementa como biblioteca.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea
set n [string trim $linea]

set signo [expr {$n > 0 ? "positivo" : $n < 0 ? "negativo" : "cero"}]

puts "signo=$signo"
```

**Lo que esta clase enseña en Tcl.** Para este caso concreto basta un ternario encadenado, pero Tcl
tiene coincidencia de patrones de verdad en dos sitios, y son de los más completos de esta página.

El primero es `switch` con `-regexp` y `-matchvar`, que **captura los grupos**:

```tcl
switch -regexp -matchvar m -- $linea {
    {^(\d{4})-(\d{2})-(\d{2})$} {
        lassign $m todo anio mes dia          ;# los grupos, ya extraídos
        puts "fecha: $dia/$mes/$anio"
    }
    {^[a-z]+@[a-z.]+$} { puts "correo" }
    default            { puts "desconocido" }
}
```

Eso **sí** es reconocer una forma y descomponerla — las dos piezas que un `match` moderno reúne.

El segundo es `string match`, con patrones de estilo *glob*, mucho más baratos que una expresión
regular:

```tcl
string match "*.txt" $fichero
string match -nocase "IMG_*" $nombre
```

Y hay una tercera pieza muy propia de Tcl: **`regexp` y `regsub` asignan directamente a variables**.

```tcl
if {[regexp {(\w+)=(\w+)} $texto todo clave valor]} {
    ...    ;# clave y valor ya están puestas
}
```

`regexp` devuelve 1 o 0 **y** deja las capturas en las variables que le nombres. Es la combinación de
comprobar y extraer en una sola operación, que es justo el patrón que `if let` de Rust y el operador
morsa de Python vinieron a resolver décadas después.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $n = <STDIN>;
chomp $n;

my $signo = $n > 0 ? 'positivo'
          : $n < 0 ? 'negativo'
          :          'cero';

print "signo=$signo\n";
```

**Lo que esta clase enseña en Perl.** **Perl es el lenguaje que popularizó la coincidencia de patrones
sobre texto**, y su influencia es tan grande que el estándar de facto lleva su nombre: **PCRE**,
*Perl Compatible Regular Expressions*. Cuando escribes una expresión regular en Python, JavaScript,
Java, PHP, Go o C#, estás escribiendo Perl.

Lo que hizo distinta a su integración no fue tener regex —`grep` y `sed` ya las tenían—, sino que
fueran **parte de la sintaxis**:

```perl
if ($linea =~ /^(\d{4})-(\d{2})-(\d{2})$/) {
    my ($anio, $mes, $dia) = ($1, $2, $3);      # capturas
}

if ($linea =~ /^(?<anio>\d{4})-(?<mes>\d{2})/) {
    print $+{anio};                              # capturas CON NOMBRE
}

my @todas = $texto =~ /(\w+)=(\w+)/g;           # todas las coincidencias
(my $limpio = $sucio) =~ s/\s+//g;               # sustitución sobre una copia
```

`=~` es un operador, `/.../` es un literal, y `$1`, `$2` y `%+` aparecen solos. No hay que importar
nada, compilar el patrón ni consultar un objeto de coincidencia.

Perl fue además muy lejos en potencia: **recursión en los patrones** (`(?R)`) para casar estructuras
anidadas, **código incrustado** con `(?{ ... })`, y `/x` para escribir patrones en varias líneas con
comentarios. Con la recursión, una expresión regular de Perl deja de reconocer solo lenguajes
regulares —puede casar paréntesis balanceados—, lo que técnicamente ya no es una expresión regular en
el sentido de la teoría, y es una fuente inagotable de discusiones.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>

int main() {
    int n{};
    if (!(std::cin >> n)) return 1;

    const char* signo = (n > 0) ? "positivo"
                      : (n < 0) ? "negativo"
                      :           "cero";

    std::cout << "signo=" << signo << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** **C++ no tiene coincidencia de patrones**, y es una de las
carencias más señaladas del lenguaje. Hay una propuesta de `inspect` que lleva años en el comité y
que no ha entrado todavía.

Lo que sí llegó es la pieza de la **descomposición**, con C++17:

```cpp
auto [minimo, maximo] = std::minmax(a, b);           // descomposición estructurada
for (const auto& [clave, valor] : mapa) { ... }      // sobre un map
auto [it, insertado] = conjunto.insert(x);           // sobre un par de retorno
```

`auto [a, b] = ...` funciona sobre `std::pair`, `std::tuple`, arrays y cualquier estructura de campos
públicos. Es exactamente el `destructuring-bind` de Lisp y el `let (a, b)` de Rust.

Y para tipos suma, C++17 trajo `std::variant` con `std::visit`, que es lo más cerca que se puede
estar hoy de un `match` sin sintaxis:

```cpp
std::variant<Circulo, Rectangulo> figura = Circulo{2.0};

const double area = std::visit(overloaded{
    [](const Circulo& c)    { return 3.14159 * c.r * c.r; },
    [](const Rectangulo& r) { return r.ancho * r.alto; }
}, figura);
```

`std::visit` **comprueba la exhaustividad en tiempo de compilación**: si falta una alternativa, no
compila. Es la garantía de Ada y de Rust, obtenida mediante plantillas en lugar de sintaxis — verboso,
pero con la misma propiedad. El truco `overloaded` es una plantilla de tres líneas que hay que
escribir a mano, y su presencia en tantos proyectos es la mejor prueba de que la sintaxis hace falta.

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

dcl-pi SIGNO;
  n int(10) const;
end-pi;

dcl-s s      varchar(10);
dcl-s salida char(30);

select;
  when n > 0;
    s = 'positivo';
  when n < 0;
    s = 'negativo';
  other;
    s = 'cero';
endsl;

salida = 'signo=' + s;
dsply salida;

*inlr = *on;
return;
```

**Lo que esta clase enseña en RPG.** RPG no tiene coincidencia de patrones ni expresiones regulares en
el lenguaje, y su respuesta a esta clase es `select` con condiciones. Pero tiene algo que conviene
conocer porque resuelve el mismo problema por otra vía: **el SQL embebido**.

```rpgle
exec sql
  select case when :n > 0 then 'positivo'
              when :n < 0 then 'negativo'
              else 'cero' end
    into :s
    from sysibm.sysdummy1;
```

Puede parecer un rodeo, y en este caso lo es. Pero para reconocer formas de verdad, en IBM i lo
idiomático es delegar en Db2, que sí tiene expresiones regulares:

```rpgle
exec sql
  select count(*) into :n
    from clientes
   where regexp_like(email, '^[a-z]+@[a-z.]+$');
```

`REGEXP_LIKE`, `REGEXP_SUBSTR` y `REGEXP_REPLACE` están en Db2 for i, así que **el motor de patrones
del sistema está en la base de datos, no en el lenguaje**. Es una división del trabajo muy propia de
la plataforma: RPG lleva la lógica de negocio y SQL lleva todo lo que tenga que ver con conjuntos de
datos y con texto.

Y para validación simple, RPG tiene `%check` y `%checkr`, que devuelven la primera posición cuyo
carácter **no** está en un conjunto dado — el mismo `verify` de PL/I de la clase 048, y la versión
mínima de "¿esta cadena tiene la forma esperada?".

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 signo: procedure options(main);

    declare n fixed binary(31);
    declare s character(10) varying;

    get list (n);

    select;
       when (n > 0) s = 'positivo';
       when (n < 0) s = 'negativo';
       otherwise    s = 'cero';
    end;

    put skip list ('signo=' || s);

 end signo;
```

**Lo que esta clase enseña en PL/I.** PL/I no tiene coincidencia de patrones, y para esta clase usa
`select;` con condiciones. Lo que sí tiene, y encaja aquí, es la función **`verify`** de la clase 048
y su compañera `search`, que son reconocimiento de forma sin expresiones regulares:

```pli
if verify(codigo, '0123456789') = 0 then       /* son TODO dígitos */
if search(texto, 'aeiou') > 0 then             /* contiene alguna vocal */
if index(texto, patron) > 0 then               /* contiene esta subcadena */
```

`verify` devuelve la posición del primer carácter que **no** pertenece al conjunto, y cero si todos
pertenecen. Con una llamada valida un campo entero, y es rapidísimo porque se compila a una
instrucción de traducción del hardware de IBM.

Esa familia —`verify`, `search`, `index`, `translate`— es la caja de herramientas de reconocimiento
de texto anterior a las expresiones regulares, y aparece en COBOL (`INSPECT`), en PL/I y en las
instrucciones del propio System/360. Cubre bien el 80 % de los casos reales de validación de campos,
que es lo que hacía falta.

Lo que no cubre es la estructura: no hay forma de decir "cuatro dígitos, un guion, dos dígitos" en
una sola expresión. Para eso hubo que esperar a que Ken Thompson llevara las expresiones regulares de
la teoría de autómatas al editor `ed`, en 1968, y a que Perl las hiciera cómodas veinte años después.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
SIGNO ; Signo -- clase 062
 read n
 set s = $select(n > 0 : "positivo", n < 0 : "negativo", 1 : "cero")
 write "signo=", s, !
 quit
```

**Lo que esta clase enseña en M.** La sorpresa de esta página: **M tiene un operador de coincidencia
de patrones desde 1966**, y se escribe con una sola interrogación.

```mumps
 if x?1.N          write "uno o más dígitos",!
 if x?3N1"-"2N     write "tres dígitos, un guion, dos dígitos",!
 if x?1U.A         write "una mayúscula seguida de letras",!
 if x?.E1"@".E     write "contiene una arroba",!
 if dni?8N1U       write "DNI español: 8 números y una letra",!
```

La sintaxis es un mini-lenguaje propio: un **contador** seguido de un **código de clase**.

| Código | Significa | | Contador | Significa |
|---|---|---|---|---|
| `N` | Numérico | | `1` | Exactamente uno |
| `A` | Alfabético | | `3` | Exactamente tres |
| `U` / `L` | Mayúscula / minúscula | | `.` | Cero o más |
| `P` | Puntuación | | `1.` | Uno o más |
| `C` | Control | | `2.5` | De dos a cinco |
| `E` | Cualquiera | | | |

`8N1U` se lee "ocho numéricos y una mayúscula". Es notablemente compacto y **mucho más legible que la
expresión regular equivalente** para este tipo de validación de campos.

Es menos potente que una regex —no hay alternancia general ni capturas— y llegó **dos años antes** de
que Ken Thompson implementara las expresiones regulares en `ed`. Dos comunidades resolviendo el mismo
problema a la vez, sin conocerse, con soluciones distintas: la de la teoría de autómatas ganó, y la de
los hospitales sigue en producción.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| n signo |

n := stdin nextLine trimBoth asNumber.

signo := n > 0
    ifTrue:  [ 'positivo' ]
    ifFalse: [ n < 0 ifTrue: [ 'negativo' ] ifFalse: [ 'cero' ] ].

Transcript show: 'signo=', signo; cr.
```

**Lo que esta clase enseña en Smalltalk.** Smalltalk no tiene coincidencia de patrones y **su
posición es que no la necesita**, porque el problema que resuelve —despachar según la forma de un
valor— ya lo resuelve el envío de mensajes.

```smalltalk
"En vez de casar el tipo, se le pregunta al objeto"
Circulo    >> area    ^ Float pi * radio squared
Rectangulo >> area    ^ ancho * alto
```

Un `match` sobre un tipo suma y una jerarquía de clases con un método polimórfico resuelven el mismo
problema **con la extensibilidad al revés**, y esa diferencia es el fondo del asunto:

- Con **`match`**, añadir una **operación** nueva es fácil (una función más) y añadir un **caso**
  nuevo obliga a tocar todos los `match` existentes.
- Con **polimorfismo**, añadir un **caso** nuevo es fácil (una clase más) y añadir una **operación**
  nueva obliga a tocar todas las clases.

Eso se conoce como el **problema de la expresión**, y no tiene una solución que gane siempre: depende
de qué eje vaya a crecer más en tu sistema. Los lenguajes funcionales eligieron un lado, los
orientados a objetos el otro, y los modernos —Scala, Rust con *traits*, Kotlin— intentan ofrecer los
dos.

Para el caso concreto de esta clase, Smalltalk sí tiene el predicado: `n sign` devuelve `-1`, `0` o
`1`, y `n positive`, `n negative`, `n isZero`, `n even`, `n between:and:` están todos en `Number`.
Como siempre, **son mensajes que puedes leer** en el navegador de clases.

Y para texto, Pharo tiene `RxParser` y `matchesRegex:` como biblioteca — no en el lenguaje, porque en
Smalltalk casi nada está en el lenguaje.

---

## Y de vuelta a la clase

Lo que se ve aquí es que la coincidencia de patrones moderna **une tres cosas que antes estaban
separadas**: seleccionar por valor (el `switch`), comprobar una forma (las expresiones regulares o el
`?` de M) y **descomponer la estructura** extrayendo sus partes. Esa tercera es la genuinamente
nueva, y viene de los lenguajes funcionales tipados —ML y Haskell—, no de esta tradición. Los
lenguajes de esta página tienen las dos primeras repartidas en construcciones distintas; verlo
explica por qué `match` se sintió como un avance real y no como azúcar sintáctico.

⏮️ [Volver a la clase 062](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
