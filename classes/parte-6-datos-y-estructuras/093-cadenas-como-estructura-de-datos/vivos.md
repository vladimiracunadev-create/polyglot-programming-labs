# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 093

> [⬅️ Volver a la clase 093](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Invertir una palabra. La operación más trivial de la parte, y la que destapa la diferencia más grande
entre estos lenguajes: **para COBOL, Fortran, RPG y PL/I una cadena es un campo de longitud fija
rellenado con espacios**, y esa decisión —tomada cuando los datos vivían en tarjetas de ochenta
columnas— sigue condicionando cómo se escribe el código sesenta años después.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es **qué es una cadena realmente**, y estos lenguajes lo enseñan porque cubren las
> tres respuestas posibles. **Longitud fija con relleno**: COBOL, Fortran, PL/I con `char(n)`, RPG con
> `char`. **Longitud variable con prefijo**: PL/I `varying`, RPG `varchar`, Pascal `ShortString`.
> **Puntero a bloque contado**: C++, Perl, Tcl, Lisp, Pascal moderno.
>
> Y de ahí sale el detalle que más código ha generado en la historia: **si una cadena es de longitud
> fija, comparar "ADA" con "ADA   " requiere decidir qué hacer con los espacios**, y cada lenguaje
> decidió distinto.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: una palabra (ASCII, sin espacios) → stdout: `invertido=<la palabra al revés>`
- **Regla:** `invertir la secuencia de caracteres`

| stdin | esperado |
|---|---|
| `hola` | `invertido=aloh` |
| `Ada` | `invertido=adA` |
| `abc` | `invertido=cba` |

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
PROGRAM-ID. CADENA.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(200).
01  N       PIC 9(4) COMP.
01  INVER   PIC X(200).

PROCEDURE DIVISION.
    ACCEPT LINEA

    MOVE 0 TO N
    INSPECT FUNCTION REVERSE(LINEA) TALLYING N FOR LEADING SPACE
    COMPUTE N = 200 - N

    MOVE FUNCTION REVERSE(LINEA(1:N)) TO INVER

    DISPLAY "invertido=" INVER(1:N)
    STOP RUN.
```

**Lo que esta clase enseña en COBOL.** `PIC X(200)` es **siempre** doscientos caracteres. Al mover
`"hola"` a ese campo, COBOL guarda `hola` seguido de **196 espacios**, y no hay ninguna forma de que
el campo "sepa" que solo cuatro son significativos.

De ahí la línea más rara de este programa:

```cobol
INSPECT FUNCTION REVERSE(LINEA) TALLYING N FOR LEADING SPACE
COMPUTE N = 200 - N
```

Se invierte la cadena, se cuentan los espacios que quedan **delante**, y se restan del total. Ese es
el idioma canónico para averiguar la longitud útil de un campo COBOL, y aparece en millones de líneas
de código. COBOL 2002 añadió `FUNCTION LENGTH` con `TRAILING`, y muchos compiladores ofrecen
`FUNCTION STORED-CHAR-LENGTH`, pero el truco del `REVERSE` es lo que se encuentra en el código
existente.

El manejo de cadenas de COBOL es sorprendentemente completo para su fama, y todo gira alrededor de
posiciones fijas:

```cobol
MOVE LINEA(5:10) TO TROZO           *> "referencia modificada": desde 5, 10 chars
STRING A DELIMITED SIZE B DELIMITED SPACE INTO C
UNSTRING C DELIMITED BY "," INTO P1 P2 P3
INSPECT T REPLACING ALL "a" BY "A"
INSPECT T TALLYING N FOR ALL ","
FUNCTION UPPER-CASE(T)   FUNCTION TRIM(T)   FUNCTION REVERSE(T)
```

`STRING` y `UNSTRING` son concatenación y división con delimitadores, y llevan cláusulas
`POINTER` y `OVERFLOW` para controlar dónde escriben y qué pasa si no cabe. Es verboso y es
**explícito sobre el desbordamiento**, que es más de lo que ofrecía C durante treinta años.

Y la comparación ignora los espacios finales: `IF NOMBRE = "ADA"` es cierto para `"ADA      "`, porque
COBOL rellena el operando corto antes de comparar. Es una decisión sensata para su modelo de datos, y
sorprende a todo el que llega de otro lenguaje.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program cadena
   implicit none
   character(len=200) :: linea
   integer :: n, i

   read(*, '(A)') linea
   n = len_trim(linea)              ! longitud SIN los espacios finales

   write(*, '(A)', advance='no') 'invertido='
   do i = n, 1, -1
      write(*, '(A)', advance='no') linea(i:i)
   end do
   write(*, '(A)') ''
end program cadena
```

**Lo que esta clase enseña en Fortran.** Como en COBOL, `character(len=200)` es **siempre** doscientos
caracteres rellenos de espacios, y de ahí que `len_trim` —la longitud sin los espacios finales— sea
una de las funciones más usadas del lenguaje.

```fortran
len(s)              ! la longitud DECLARADA: siempre 200
len_trim(s)         ! la longitud ÚTIL
trim(s)             ! la cadena sin espacios finales
adjustl(s)          ! desplaza a la izquierda
s(3:7)              ! subcadena: los caracteres 3 a 7
s(i:i)              ! UN carácter -- Fortran no tiene tipo carácter suelto
```

Fíjate en `s(i:i)`: en Fortran **no existe el "carácter" como tipo distinto de la cadena**. Un
carácter es una cadena de longitud 1, y por eso el índice se escribe dos veces. Es coherente y
desconcierta la primera vez.

El operador de concatenación es **`//`**, elegido porque `+` estaba reservado para la aritmética y el
lenguaje no tiene sobrecarga en su versión original.

Fortran 2003 trajo la mejora que faltaba: **las cadenas de longitud diferida**.

```fortran
character(len=:), allocatable :: s
s = 'hola'                    ! toma la longitud exacta: 4
s = s // ' mundo'             ! se REASIGNA a 10
```

Con `len=:` y `allocatable`, la cadena se ajusta sola al asignarla, y por fin se puede escribir código
de manipulación de texto sin declarar tamaños máximos. Es la diferencia entre el Fortran que se ve en
los códigos científicos antiguos —lleno de `character(len=256)`— y el moderno.

Y la lectura con `read(*, '(A)')` sobre un `character(len=200)` rellena con espacios lo que sobra:
otra vez el modelo de la tarjeta perforada, funcionando en 2026.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO; use Ada.Text_IO;

procedure Cadena is
   Linea  : String (1 .. 200);
   Ultimo : Natural;
begin
   Get_Line (Linea, Ultimo);

   Put ("invertido=");
   for I in reverse 1 .. Ultimo loop
      Put (Linea (I));
   end loop;
   New_Line;
end Cadena;
```

**Lo que esta clase enseña en Ada.** El `String` de Ada **es un arreglo de caracteres**, literalmente:
`type String is array (Positive range <>) of Character`. No es un tipo especial, y por eso hereda todo
lo de la clase 089 — `S'Length`, `S'First`, `S'Last`, secciones, comparación, concatenación con `&`.

Y trae la consecuencia incómoda del arreglo no restringido: **la longitud forma parte del valor**, así
que una variable `String` tiene un tamaño fijo desde que se crea. `Get_Line` devuelve por eso **dos**
cosas: el búfer y hasta dónde llenó.

Ada resuelve el resto con **tres tipos de cadena**, y elegir entre ellos es una decisión de diseño
real:

| Tipo | Paquete | Cuándo |
|---|---|---|
| `String` | integrado | longitud conocida y fija |
| `Bounded_String` | `Ada.Strings.Bounded` | **máximo conocido, sin memoria dinámica** |
| `Unbounded_String` | `Ada.Strings.Unbounded` | longitud arbitraria |

`Bounded_String` es el que no tiene equivalente en el núcleo, y existe por la misma razón que los
contenedores llegaron tarde (clase 090): **en sistemas empotrados certificados no se puede reservar
memoria**. Una cadena acotada guarda un búfer de tamaño máximo y una longitud, todo en la pila, y
ofrece el mismo interfaz que la ilimitada.

```ada
package Nombres is new Ada.Strings.Bounded.Generic_Bounded_Length (Max => 80);
```

Ada tiene además `Ada.Strings.Fixed` con `Index`, `Trim`, `Replace_Slice` y `Head`/`Tail`, y desde
Ada 2012 el soporte completo de Unicode con `Wide_Wide_String` (UTF-32) y `Ada.Strings.UTF_Encoding`.

Tres tipos donde otros lenguajes tienen uno es más trabajo, y es exactamente el tipo de decisión que
Ada obliga a tomar explícitamente en lugar de esconderla.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Cadena;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  S, R: string;
  I: Integer;

begin
  ReadLn(S);
  S := Trim(S);

  R := '';
  for I := Length(S) downto 1 do
    R := R + S[I];

  WriteLn('invertido=', R);
end.
```

**Lo que esta clase enseña en Pascal.** Pascal tiene la historia de cadenas más accidentada de esta
página, y merece contarse porque explica la directiva `{$H+}` que aparece en todos los programas de
este curso.

**El Pascal original de Wirth no tenía cadenas.** Solo `packed array[1..n] of Char`, con las mismas
limitaciones que Fortran y COBOL.

**Turbo Pascal inventó la `ShortString`**: un arreglo de 256 bytes donde **el byte 0 guarda la
longitud**. De ahí el límite de 255 caracteres, y de ahí que `Length(S)` sea instantáneo — es leer un
byte. Fue una solución brillante para 1983 y una restricción severa después.

**Delphi 2 (1996) trajo la `AnsiString`**, que es lo que hoy se llama `string`: puntero a un bloque
con longitud y **contador de referencias**, gestionada automáticamente, sin límite práctico.

```pascal
{$H+}      { string = AnsiString, larga }
{$H-}      { string = ShortString, 255 caracteres }
```

Esa directiva sigue existiendo por compatibilidad, y es la razón de que todo código Free Pascal
moderno empiece con `{$H+}`.

Y hay un detalle que sorprende a quien viene de C: **las cadenas de Pascal empiezan en el índice 1**.
`S[1]` es el primer carácter. Es coherente con los arreglos del lenguaje, y es una de las
incompatibilidades más molestas al portar código.

Las cadenas modernas son **contadas por referencia y con copia al escribir**: asignar no copia, y la
copia solo ocurre al modificar una cadena compartida. Concatenar en un bucle —como hace este
programa— es por tanto O(n²), y para volúmenes grandes lo idiomático es `TStringBuilder`.

Hoy conviven además `UnicodeString` (UTF-16) y `UTF8String`, con conversión automática entre ellas —
cómodo, y una fuente conocida de conversiones invisibles que cuestan rendimiento.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let ((s (string-trim '(#\Space #\Return #\Tab) (read-line))))
  (format t "invertido=~A~%" (reverse s)))
```

**Lo que esta clase enseña en Common Lisp.** En Common Lisp, **una cadena es un vector de
caracteres**, igual que en Ada: `string` es un subtipo de `vector`, que a su vez lo es de `array` y
de `sequence`.

Y de ahí sale lo que hace elegante a esta implementación: **`reverse` no es una función de cadenas**.
Es la función de secuencias, y funciona igual sobre una lista, un vector o una cadena. Lo mismo vale
para `length`, `subseq`, `position`, `find`, `remove`, `sort`, `count` y `map`.

```lisp
(reverse "hola")          ; "aloh"
(reverse '(1 2 3))        ; (3 2 1)
(subseq "hola mundo" 5)   ; "mundo"
(position #\a "hola")     ; 3
(count #\a "banana")      ; 3
(map 'string #'char-upcase "hola")   ; "HOLA"
```

Un solo juego de funciones para todas las secuencias: eso es lo que consiguió Common Lisp al unificar
la biblioteca en 1984, y es más de lo que tienen la mayoría de los lenguajes de esta página.

El carácter **sí es un tipo propio** —`#\a`, `#\Space`, `#\Newline`— al contrario que en Fortran.

Y las cadenas son **mutables** si se crean como tales, lo que sorprende a quien viene de Java o
Python:

```lisp
(let ((s (copy-seq "hola")))
  (setf (aref s 0) #\H)
  s)                             ; "Hola"
```

Modificar un literal de cadena, en cambio, es comportamiento indefinido: el compilador puede
colocarlo en memoria de solo lectura o compartir literales iguales. Es la misma trampa que en C.

Para construir texto por trozos, el idioma eficiente es `with-output-to-string`, que evita el
`concatenate` cuadrático:

```lisp
(with-output-to-string (s) (dolist (x lista) (format s "~A-" x)))
```

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea
puts "invertido=[string reverse [string trim $linea]]"
```

**Lo que esta clase enseña en Tcl.** Tcl es **el lenguaje de esta página cuya cadena es el tipo
fundamental**: su lema fundacional es *everything is a string*, y de ahí viene todo lo demás.

`string` es un comando con más de treinta subcomandos, que cubren esta clase entera:

```tcl
string reverse $s        string length $s       string index $s 0
string range $s 2 5      string toupper $s      string trim $s
string map {a A b B} $s  string first "x" $s    string repeat "ab" 3
string match "*.txt" $s  string is integer $s   string cat $a $b
```

`string map` es especialmente potente: sustituye **varios pares a la vez, en una pasada**, sin
solaparse. `string is` es el validador de tipos del lenguaje —`string is integer`, `is double`, `is
alnum`, `is boolean`— y es la forma idiomática de comprobar un dato de entrada.

Debajo, la realidad es mucho más elaborada que "todo es una cadena": desde Tcl 8.1 **las cadenas son
UTF-8 internamente y se indexan por carácter**, no por byte. `string length "ñandú"` devuelve 5. Tcl
tuvo soporte Unicode correcto **en 1999**, antes que casi todos los lenguajes de esta página.

Y desde Tcl 9.0 (2024), el soporte se completó con cadenas de longitud arbitraria por encima de 2 GB y
manejo pleno de los caracteres fuera del plano básico —emoji incluidos—, que era la última laguna.

La contrapartida del modelo es la de la clase 090: **si todo puede ser una cadena, cualquier valor
puede convertirse a texto y volver**, y esas conversiones cuestan. El *shimmering* aparece aquí
también, y `string is` sobre un valor que ya es un entero es más barato que sobre uno textual.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $s = <STDIN>;
chomp $s;

print "invertido=", scalar reverse($s), "\n";
```

**Lo que esta clase enseña en Perl.** `scalar reverse($s)` necesita el `scalar` por lo que ya se vio
en la clase 090: **`reverse` invierte la lista en contexto de lista y la cadena en contexto escalar**.
Sin él, se invertiría una lista de un solo elemento y saldría la cadena original.

Perl es el lenguaje de esta página construido **alrededor** del texto, y su aportación no son las
funciones de cadena —que las tiene todas— sino **las expresiones regulares integradas en la
sintaxis**:

```perl
$s =~ s/viejo/nuevo/g;             # sustituir
$s =~ tr/a-z/A-Z/;                  # transliterar, carácter a carácter
my @campos = split /\s*,\s*/, $s;   # dividir con un patrón
if ($s =~ /^(\d{4})-(\d{2})$/) { ... }   # capturar en $1, $2
```

Que `=~`, `s///` y `//` sean **operadores del lenguaje** y no llamadas a una biblioteca es lo que hizo
a Perl dominar el procesamiento de texto durante veinte años, y es lo que copió después todo el mundo:
la sintaxis de expresiones regulares de Python, Java, JavaScript, PHP, Ruby y .NET es **PCRE**, es
decir, *Perl Compatible Regular Expressions*.

Es probablemente la contribución más duradera de Perl a la informática, y sobrevive en lenguajes cuyos
usuarios no han escrito una línea de Perl.

Sobre Unicode, Perl tiene el modelo más explícito y también el más confuso: hay que declarar la
intención con `use utf8` para el código fuente y capas de entrada/salida para los datos.

```perl
use utf8;                              # el FUENTE está en UTF-8
binmode(STDOUT, ':encoding(UTF-8)');   # la SALIDA se codifica en UTF-8
```

Sin eso, Perl trata los datos como bytes. Es riguroso —distingue cadena de caracteres de cadena de
bytes, que es la distinción correcta— y exige entenderlo, a diferencia de Tcl, donde es automático.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <algorithm>
#include <iostream>
#include <string>

int main() {
    std::string s;
    if (!(std::cin >> s)) return 1;

    std::reverse(s.begin(), s.end());

    std::cout << "invertido=" << s << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** `std::reverse` no es una función de cadenas: es **un algoritmo
genérico que funciona sobre cualquier par de iteradores bidireccionales**. Sirve igual para un
`vector`, un `array`, un `deque` o una `string`, porque `std::string` es, a efectos de la STL, un
contenedor de caracteres.

Esa unificación es la misma idea que en Lisp y en Ada, con otra tecnología: en Lisp la da el tipo
`sequence`, en Ada el arreglo, en C++ el concepto de iterador.

`std::string` arregló el problema histórico de C —cadenas terminadas en `\0`, sin longitud, con
`strcpy` como fuente inagotable de desbordamientos— y sus operaciones son las esperables:
`size()`, `substr()`, `find()`, `+`, `==`, `starts_with()` desde C++20.

Tres cosas que conviene saber y que no son evidentes:

**La optimización de cadena corta.** Casi todas las implementaciones guardan las cadenas de hasta 15
o 22 caracteres **dentro del propio objeto**, sin reservar memoria. Por eso `std::string` ocupa 32
bytes y no 8, y por eso las cadenas cortas son mucho más rápidas de lo que su interfaz sugiere.

**`std::string_view` (C++17)** es la pieza que faltaba: una **vista no propietaria** —puntero y
longitud— que evita copiar al pasar subcadenas.

```cpp
void procesar(std::string_view s);      // acepta string, const char*, literal: sin copiar
```

Con la trampa que le corresponde: **no prolonga la vida de lo que apunta**. Una `string_view` sobre
una `string` temporal queda colgando, y es un error frecuente.

**Y Unicode: `std::string` es una secuencia de bytes, no de caracteres.** `s.size()` sobre `"ñ"` en
UTF-8 devuelve 2, y `std::reverse` sobre texto no ASCII **rompe la codificación**. C++ sigue sin
soporte Unicode real en la biblioteca estándar en 2026, y la respuesta práctica es ICU o utf8cpp. Es
la carencia más señalada del lenguaje en este terreno, y la razón de que este programa se limite a
ASCII.

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

dcl-pi CADENA;
  entrada char(200) const;
end-pi;

dcl-s s varchar(200);
dcl-s r varchar(200) inz('');
dcl-s i int(10);

s = %trimr(entrada);

for i = %len(s) downto 1;
  r += %subst(s : i : 1);
endfor;

dsply ('invertido=' + r);

*inlr = *on;
return;
```

**Lo que esta clase enseña en RPG.** RPG comparte el modelo de COBOL —`char(n)` es siempre `n`
posiciones rellenas de espacios— y por eso `%trim`, `%trimr` y `%triml` aparecen por todas partes en
el código real.

La familia de funciones integradas cubre lo esperable, con el prefijo `%` que caracteriza al RPG
libre:

```rpgle
%subst(s : inicio : longitud)      // subcadena; TAMBIÉN a la izquierda del =
%scan('abc' : s)                    // buscar, devuelve posición o 0
%scanrpl('a' : 'A' : s)             // buscar y reemplazar (RPG 7.1)
%replace('X' : s : 3 : 1)           // sustituir en una posición
%len(s)  %trim(s)  %char(n)  %int(s)  %upper(s)  %lower(s)
%split(s : ' ')                     // dividir en una lista (RPG 7.5, 2022)
```

Dos de esas merecen atención.

**`%subst` funciona como destino de asignación**, no solo como fuente:

```rpgle
%subst(fecha : 5 : 2) = '12';       // escribir EN una posición concreta
```

Es la reference modification de COBOL y el `set $piece` de M: modificar una porción de la cadena en el
sitio, sin reconstruirla.

**Y `%split`, de 2022**, es un ejemplo perfecto de lo que documenta esta sección: un lenguaje de 1959
que en 2022 incorpora la división de cadenas en una lista porque el trabajo real —consumir APIs,
procesar JSON— lo pide.

En la misma línea, RPG 7.2+ añadió `DATA-INTO` y `DATA-GEN`, que **analizan y generan JSON y XML
directamente hacia una estructura de datos**, sin escribir el analizador. Eso, en un lenguaje cuyo
tipo de cadena sigue siendo de longitud fija por defecto, dice bastante de cómo se están modernizando
estas plataformas.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 cadena: procedure options(main);

    declare s char(200) varying;
    declare r char(200) varying initial('');
    declare i fixed binary(31);

    get edit (s) (a(200));
    s = trim(s);

    do i = length(s) to 1 by -1;
       r = r || substr(s, i, 1);
    end;

    put skip list ('invertido=' || r);

 end cadena;
```

**Lo que esta clase enseña en PL/I.** PL/I fue **el primer lenguaje mayoritario con cadenas de
longitud variable**, con el atributo **`varying`**, en 1964.

```pli
declare fijo   char(20);           /* siempre 20, rellenado con espacios */
declare varia  char(20) varying;    /* hasta 20, con longitud REAL guardada */
declare libre  char(20) varyingz;   /* variante terminada en nulo, para C */
```

Una `varying` guarda un prefijo de dos bytes con la longitud actual — exactamente el mismo diseño que
la `ShortString` de Turbo Pascal veinte años después, y que el `varchar` de RPG y de SQL. El `VARCHAR`
de todas las bases de datos del mundo desciende de aquí.

Y PL/I trae una batería de funciones de cadena que en 1964 no tenía nadie:

```pli
substr(s, i, n)      index(s, 'abc')     length(s)     trim(s)
translate(s, 'ABC', 'abc')               verify(s, '0123456789')
repeat('ab', 3)      reverse(s)          string(estructura)
```

**`verify`** es la joya olvidada: devuelve la posición del primer carácter **que NO está** en el
conjunto dado, y con eso se valida un campo entero sin bucle.

```pli
 if verify(codigo, '0123456789') ^= 0 then ...   /* hay algo que no es dígito */
```

Es una operación de conjuntos sobre caracteres, resuelta por el compilador, y sigue sin tener
equivalente directo en la mayoría de los lenguajes del núcleo.

**Y `substr` funciona como pseudovariable**, es decir, a la izquierda del signo igual:

```pli
 substr(fecha, 5, 2) = '12';
```

Ese patrón —modificar un trozo de cadena en el sitio— lo comparten PL/I, COBOL, RPG y M, y es
consecuencia directa del modelo de datos posicional que los cuatro comparten.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
CADENA ; Cadenas -- clase 093
 read s
 set r = ""
 for i=$length(s):-1:1 set r = r _ $extract(s, i)
 write "invertido=", r, !
 quit
```

**Lo que esta clase enseña en M.** En M **todo es una cadena**, como en Tcl, y por la misma razón
histórica: el lenguaje se diseñó para manipular texto médico en máquinas pequeñas.

No hay tipos, así que `1 + "2"` vale 3 y `"abc" + 1` vale 1 —M convierte el prefijo numérico, o 0 si
no hay— sin ningún error. Es la conversión más permisiva de esta página.

Las funciones de cadena de M son pocas y están extraordinariamente bien elegidas:

```mumps
 $extract(s, i, j)         ; subcadena por POSICIÓN
 $length(s)                 ; longitud
 $length(s, ",")            ; número de PIEZAS con ese delimitador
 $piece(s, ",", n)          ; la pieza n
 $find(s, "abc")            ; buscar
 $translate(s, "abc", "ABC"); traducir carácter a carácter
 $justify(s, 10)            ; alinear
 $reverse(s)                 ; invertir
```

Las dos que definen el lenguaje son **`$piece` y `$extract`**, y **las dos funcionan como
pseudovariables**:

```mumps
 set $extract(s, 3) = "x"          ; cambiar el tercer carácter
 set $piece(s, "^", 4) = "nuevo"   ; cambiar la cuarta pieza
```

Poder asignar a `$piece` es lo que hace viable el modelo de datos de VistA (clase 090): un registro es
una cadena con piezas, y actualizar un campo es una sola sentencia sobre el *global*, sin leer,
descomponer, modificar y recomponer.

```mumps
 set $piece(^PAC(id, 0), "^", 3) = "M"
```

Esa línea actualiza un campo de un registro en disco, dentro de una transacción, sin SQL y sin capa de
persistencia. Es fea, es frágil ante cambios de esquema y es **muy rápida** — y es exactamente por lo
que M sigue moviendo los historiales clínicos de decenas de millones de personas.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| s |

s := stdin nextLine trimBoth.

Transcript show: 'invertido=', s reversed; cr.
```

**Lo que esta clase enseña en Smalltalk.** `String` es una subclase de `ArrayedCollection`, así que
—como en Lisp, Ada y C++— **una cadena es una colección**, y responde a todo el protocolo de la clase
089.

```smalltalk
'hola' reversed                        "aloh"
'hola' size                             "4"
'hola' asUppercase
'hola mundo' substrings: ' '
'hola' , ' mundo'                       "la coma es CONCATENAR"
('hola' collect: [ :c | c asUppercase ])   "map sobre caracteres"
('hola' select: [ :c | c isVowel ])         "filter: 'oa'"
```

Que `select:` y `collect:` funcionen sobre una cadena y devuelvan una cadena es la regla *species* de
la clase 090 en acción.

Y Smalltalk tiene una distinción que ningún otro lenguaje de esta página hace de forma tan explícita:
**`String` frente a `Symbol`**.

```smalltalk
'hola' == 'hola'      "false: son DOS objetos distintos con el mismo contenido"
#hola  == #hola       "true: un símbolo es ÚNICO en el sistema"
```

Un `Symbol` está **internado**: solo existe uno por cada texto, así que comparar dos símbolos es
comparar punteros, en tiempo constante. Por eso los nombres de mensaje son símbolos (clase 085), y por
eso las claves de un diccionario suelen serlo.

Es la misma idea que los símbolos de Lisp, los átomos de Erlang y los `Symbol` de Ruby, y viene del
mismo sitio.

Las cadenas de Smalltalk son **mutables** —`s at: 1 put: $H`— lo que las diferencia de Java y Python,
y para construir texto por trozos lo idiomático es `WriteStream`:

```smalltalk
String streamContents: [ :flujo |
    coleccion do: [ :cada | flujo print: cada ] separatedBy: [ flujo nextPut: $- ] ]
```

`do:separatedBy:` resuelve en un mensaje el problema del separador que no va al final — el mismo que
en Lisp resuelve `~^` y en el resto de lenguajes obliga a un `if` dentro del bucle.

---

## Y de vuelta a la clase

Lo transferible: **el relleno con espacios no es una torpeza antigua, es lo que exige un fichero de
registros de longitud fija**, y ese formato sigue moviendo la mayor parte de los datos bancarios del
mundo. Cuando veas `TRIM` en cada línea de un programa COBOL o RPG, no estás viendo código
descuidado: estás viendo la frontera entre un modelo de datos posicional y uno de longitud variable.
La misma frontera aparece hoy al leer un fichero de ancho fijo con Pandas.

⏮️ [Volver a la clase 093](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
