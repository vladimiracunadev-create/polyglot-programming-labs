# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 047

> [⬅️ Volver a la clase 047](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Leer un carácter y decir qué número lo representa. Es la clase que obliga a mirar debajo del texto,
y allí no hay letras: hay números. La pregunta interesante no es *cuál* es el número, sino **quién
decide la tabla**: porque en el mainframe de IBM la letra `A` no vale 65, vale **193**, y ese
desacuerdo de 1964 sigue costando dinero hoy en cada integración entre un banco y el resto del mundo.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es **la codificación: la correspondencia entre un carácter y su número**, y estos
> lenguajes lo enseñan porque **no comparten tabla**. COBOL, PL/I y RPG viven en **EBCDIC**, el juego
> de caracteres de IBM, donde las letras no son contiguas —entre la `I` y la `J` hay un hueco— y las
> minúsculas van *antes* que las mayúsculas. Todo lo demás vive en ASCII y sus descendientes.
>
> Esa es una diferencia que el núcleo no puede mostrar, porque sus diez lenguajes están todos del
> mismo lado. Y explica por qué Fortran tiene **dos parejas de funciones** para lo mismo, y por qué en
> COBOL ordenar alfabéticamente no da el mismo resultado según la máquina.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: un único carácter (ASCII) → stdout: `char=<c> codigo=<punto de código>`
- **Regla:** `codigo = punto_de_codigo(c)`

| stdin | esperado |
|---|---|
| `A` | `char=A codigo=65` |
| `z` | `char=z codigo=122` |
| `0` | `char=0 codigo=48` |

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
PROGRAM-ID. CARACTERES.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA    PIC X(80).
01  C        PIC X.
01  CODIGO   PIC 9(4) COMP-3.
01  ED-COD   PIC Z(3)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    MOVE LINEA(1:1) TO C
    COMPUTE CODIGO = FUNCTION ORD(C) - 1
    MOVE CODIGO TO ED-COD
    DISPLAY "char=" C " codigo=" FUNCTION TRIM(ED-COD)
    STOP RUN.
```

**Lo que esta clase enseña en COBOL.** El `- 1` de `FUNCTION ORD(C) - 1` no es un ajuste
caprichoso: **`ORD` devuelve la posición en la secuencia de colación empezando por 1**, no el valor
del byte. En COBOL el primer carácter de la tabla ocupa la posición 1, así que hay que restar uno
para obtener el punto de código. Su inversa es `FUNCTION CHAR(n)`, con la misma base 1.

Y detrás está lo importante: **en un mainframe IBM esta tabla es EBCDIC, no ASCII**. Ahí `A` vale
**193**, `B` vale 194… pero `I` vale 201 y `J` vale **209**: hay un hueco de siete posiciones. Las
letras no son contiguas.

Esa sola frase invalida un idioma que todo el mundo escribe sin pensar:

```cobol
IF C >= "A" AND C <= "Z"        *> en EBCDIC NO significa "es una mayúscula"
```

En EBCDIC ese rango incluye caracteres que no son letras. La comprobación correcta es enumerar los
tres tramos, o usar las clases del propio lenguaje: `IF C IS ALPHABETIC`.

Y COBOL, consciente del problema desde el principio, permite **cambiar la tabla** en la
`ENVIRONMENT DIVISION`:

```cobol
SPECIAL-NAMES.
    ALPHABET ASCII-TABLA IS STANDARD-1.
```

La colación es configurable porque en 1959 ya se sabía que iba a haber más de una.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program caracteres
   implicit none
   character(len=1) :: c

   read(*, '(A)') c

   write(*, '(A,A,A,I0)') 'char=', c, ' codigo=', iachar(c)
end program caracteres
```

**Lo que esta clase enseña en Fortran.** Fortran tiene **dos parejas de funciones que parecen la
misma**, y la diferencia entre ellas es exactamente el tema de esta clase:

| Función | Tabla que usa |
|---|---|
| `iachar(c)` / `achar(n)` | **ASCII**, siempre, en cualquier máquina |
| `ichar(c)` / `char(n)` | La del **procesador** — EBCDIC si estás en un mainframe |

La `a` de `iachar` es de *ASCII*. Existen las dos porque Fortran se ejecutaba en máquinas de IBM y
de CDC con tablas distintas, y el estándar quiso ofrecer a la vez "dame el código de esta máquina"
y "dame el código ASCII pase lo que pase". Este programa usa `iachar` porque el contrato de la clase
pide el punto de código ASCII, y esa elección debe ser deliberada.

Y hay una consecuencia más profunda: **las comparaciones de caracteres con `<` y `>` usan la tabla
del procesador**, pero Fortran ofrece además `LLT`, `LLE`, `LGT` y `LGE` —*lexically less than*, etc.—
que comparan **siempre en ASCII**. Cuatro funciones que existen solo para que ordenar texto dé el
mismo resultado en todas las máquinas. Es la clase de detalle que revela para qué se diseñó de verdad
un lenguaje portable.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Caracteres is
   C : Character;
begin
   Get (C);

   Put ("char=" & C);
   Put (" codigo=");
   Put (Character'Pos (C), Width => 1);
   New_Line;
end Caracteres;
```

**Lo que esta clase enseña en Ada.** `Character'Pos (C)` no es una función: es un **atributo del
tipo**. Y eso importa porque `Character` en Ada **es un tipo enumerado**, exactamente igual que
`Boolean` o que cualquiera que declares tú:

```ada
type Character is (NUL, SOH, ..., 'A', 'B', ..., 'z', ...);   --  simplificado
```

Por eso funcionan sobre él **todos** los atributos de los enumerados: `'Pos` da la posición, `'Val`
es la inversa, `'Succ` y `'Pred` dan el siguiente y el anterior, `'First` y `'Last` dan los
extremos, y `'Image` da su nombre. No hay funciones especiales para caracteres porque no hacen
falta: son las de los enumerados.

Ada distingue además **tres tipos de carácter**, con su tipo de cadena correspondiente:

| Tipo | Tamaño | Cadena |
|---|---|---|
| `Character` | 8 bits (Latin-1) | `String` |
| `Wide_Character` | 16 bits (BMP de Unicode) | `Wide_String` |
| `Wide_Wide_Character` | 32 bits (Unicode completo) | `Wide_Wide_String` |

Son **tipos distintos e incompatibles**: no se mezclan sin conversión explícita. En un sistema donde
hay que certificar el comportamiento, que el ancho del carácter esté en el tipo y no en una
suposición es exactamente lo que se busca.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Caracteres;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  C: Char;

begin
  Read(C);
  WriteLn('char=', C, ' codigo=', IntToStr(Ord(C)));
end.
```

**Lo que esta clase enseña en Pascal.** `Ord` es la misma función que se usa con los enumerados y con
los subrangos, porque **`Char` es un tipo ordinal más**. Su inversa es `Chr`. Esa uniformidad —una
sola pareja de funciones para todos los tipos ordinales— es muy propia de Wirth: menos conceptos,
aplicados a más sitios.

Y de ahí sale una capacidad que casi ningún lenguaje moderno tiene: **`Char` puede ser el índice de
un array**.

```pascal
var
  Frecuencia: array['a'..'z'] of Integer;
begin
  Frecuencia['e'] := Frecuencia['e'] + 1;
```

El array va literalmente de la `a` a la `z`, sin restar `Ord('a')` a mano como habría que hacer en C
o en Java. También se pueden usar en un `case` con rangos —`case C of 'a'..'z': ...`— y en conjuntos:
`if C in ['a'..'z', 'A'..'Z'] then`. Ese operador `in` sobre conjuntos de tipos ordinales es una idea
de Pascal que se perdió por el camino y que sigue siendo más legible que cualquier alternativa.

Free Pascal añadió después `WideChar` (UTF-16) y `UnicodeString`, y `{$codepage UTF8}` para que los
literales del fuente se interpreten como UTF-8.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let ((c (read-char)))
  (format t "char=~C codigo=~D~%" c (char-code c)))
```

**Lo que esta clase enseña en Common Lisp.** Los caracteres son **objetos de primera clase con
sintaxis propia**: se escriben `#\a`, `#\A`, `#\Space`, `#\Newline`, `#\Tab`. Esa notación `#\`
existe precisamente porque un carácter **no es una cadena de longitud uno** —distinción que Python
no hace y que causa más confusión de la que parece.

`char-code` y su inversa `code-char` dan el punto de código. En las implementaciones modernas —SBCL
entre ellas— es **Unicode completo**, así que `(char-code #\ñ)` da 241 y `(char-code #\€)` da 8364.

Y hay dos familias de comparadores, que es la parte interesante para esta clase:

```lisp
(char= #\a #\A)        ; => NIL   distingue mayúsculas
(char-equal #\a #\A)   ; => T     no las distingue
(char< #\a #\b)        ; => T
(string< "casa" "caso") ; => 3     devuelve el índice donde difieren, no un booleano
```

Que `string<` devuelva **la posición del primer carácter distinto** en lugar de `T` es muy propio de
Lisp: el dato útil es más informativo que el booleano, y `nil` sigue sirviendo como falso. Es la
misma filosofía que hace que `and` devuelva el último valor en vez de `T`.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea
set c [string index $linea 0]
scan $c %c codigo

puts "char=$c codigo=$codigo"
```

**Lo que esta clase enseña en Tcl.** `scan` es el `sscanf` de C: lee de una cadena según un formato y
**deja los resultados en variables**, en lugar de devolverlos. `scan $c %c codigo` interpreta el
carácter y guarda su punto de código en `codigo`. Su pareja es `format`, que es `sprintf`.

Que la operación se llame `scan` y no `ord` delata el origen del lenguaje: Tcl no piensa en
caracteres, piensa en **cadenas**, porque no tiene tipo carácter. `string index $linea 0` devuelve
una cadena de longitud uno, no un carácter — la misma decisión que Python.

Sobre Unicode, Tcl fue **muy** temprano: desde la versión 8.1, en 1999, todas las cadenas son
internamente Unicode, mucho antes que la mayoría. Pero durante décadas se quedó limitado al plano
básico (16 bits), y **Tcl 9.0, en 2024, es la versión que por fin soporta el rango completo** de
Unicode, incluidos los emoji y los planos suplementarios.

Ese retraso no es anecdótico: es el mismo problema que arrastran Java, C# y JavaScript por haber
adoptado Unicode cuando "16 bits bastarán para todo". Tcl 9 lo resolvió; los otros conviven con
pares subrogados hasta hoy.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;
my $c = substr($linea, 0, 1);

printf "char=%s codigo=%d\n", $c, ord($c);
```

**Lo que esta clase enseña en Perl.** `ord` y `chr` son la pareja de siempre, y `substr` extrae — no
hay tipo carácter, igual que en Tcl y Python.

Lo específico de Perl en esta clase es su **modelo de Unicode**, que es a la vez el más potente y el
más incomprendido de la lista. Perl distingue con precisión entre una **cadena de caracteres** y una
**cadena de bytes**, y el paso de una a otra es explícito:

```perl
use utf8;                    # el FUENTE está en UTF-8
binmode(STDOUT, ':utf8');    # la SALIDA se codifica en UTF-8
use open ':std', ':encoding(UTF-8)';   # ambas cosas, para todos los canales

my $s = "ñandú";
length($s);                  # 5 con `use utf8`; 7 sin él (¡bytes!)
```

Ese `length` que devuelve 5 o 7 según una línea de arriba del fichero es la fuente inagotable de
confusión. Y la regla que Perl enseña, y que vale para cualquier lenguaje, es el llamado **sándwich
de Unicode**: *decodifica al entrar, trabaja siempre en caracteres, codifica al salir*. Los idiomas
que fallan son los que trabajan con bytes en medio.

Perl añade además la pregunta que casi nadie se hace: `"\N{LATIN SMALL LETTER N WITH TILDE}"`
permite escribir un carácter **por su nombre Unicode**, y `\p{Letter}` en una expresión regular
casa cualquier letra de cualquier alfabeto.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>

int main() {
    char c{};
    if (!(std::cin >> c)) return 1;

    std::cout << "char=" << c
              << " codigo=" << static_cast<int>(static_cast<unsigned char>(c))
              << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** La doble conversión `static_cast<int>(static_cast<unsigned
char>(c))` parece paranoia y no lo es: **el estándar no dice si `char` tiene signo**. En x86 con GCC
lo tiene; en ARM, tradicionalmente no. Y si lo tiene, un byte por encima de 127 —una `ñ` en Latin-1,
o cualquier byte de una secuencia UTF-8— se convierte a un **entero negativo**.

Ese es un error real y clásico: pasar un `char` con signo a `std::isalpha` o a `std::toupper` es
**comportamiento indefinido** cuando el valor es negativo, porque esas funciones esperan un valor
representable en `unsigned char`. La regla es convertir siempre a `unsigned char` primero.

C++ arrastra además el mayor zoo de tipos de carácter de toda la página:

| Tipo | Para qué |
|---|---|
| `char` | Un byte; con o sin signo según la plataforma |
| `signed char` / `unsigned char` | Cuando el signo importa; **tres tipos distintos** |
| `wchar_t` | Ancho, pero de tamaño no especificado (16 bits en Windows, 32 en Linux) |
| `char8_t` (C++20) | Una unidad de UTF-8 |
| `char16_t` / `char32_t` (C++11) | UTF-16 y UTF-32 |

Seis tipos para representar texto es el resultado de treinta años de intentos sucesivos, cada uno
resolviendo el problema del anterior sin poder retirarlo. Es el precio exacto de la compatibilidad
hacia atrás que hace posible que C++ siga en producción.

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

dcl-pi CARACTER;
  c char(1) const;
end-pi;

// En IBM i el juego nativo es EBCDIC: 'A' vale 193, no 65. Se convierte a
// UCS-2 y se lee el valor de los dos bytes para obtener el punto Unicode.
dcl-ds punto qualified;
  texto ucs2(1);
  valor uns(5) overlay(punto : 1);
end-ds;

dcl-s salida char(50);

punto.texto = %ucs2(c);

salida = 'char=' + c + ' codigo=' + %char(punto.valor);
dsply salida;

*inlr = *on;
return;
```

**Lo que esta clase enseña en RPG.** Este programa es la demostración más literal de todo el
material sobre por qué esta clase importa: **en IBM i no se puede pedir "el código de este
carácter"**, porque la respuesta nativa sería EBCDIC. Para obtener el punto de código que espera el
resto del mundo hay que **convertir a Unicode primero**.

`%ucs2(c)` hace esa conversión, y la **estructura de datos con `overlay`** es la forma de RPG de
mirar los mismos bytes con otro tipo: `texto` los ve como dos bytes de UCS-2 y `valor` los ve como un
entero sin signo de 16 bits. Es lo mismo que una `union` de C, y en RPG se usa constantemente —para
descomponer un campo de fecha, para leer una cabecera, para reinterpretar un registro—.

Ese `overlay` es, además, la respuesta de RPG a lo que PL/I resuelve con `unspec` y C++ con
`reinterpret_cast`: **acceso a la representación**, sin abandonar el lenguaje.

Y la conversión entre juegos de caracteres no es un caso raro en IBM i: es el pan de cada día. Cada
campo de la base de datos tiene un **CCSID** —un identificador de juego de caracteres— y el sistema
convierte automáticamente al leer y escribir. Cuando alguien se queja de que "los acentos salen mal"
en una integración con un mainframe, casi siempre es un CCSID mal declarado.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 caracteres: procedure options(main);

    declare linea character(80) varying;
    declare c     character(1);

    get edit (linea) (a(80));
    c = substr(linea, 1, 1);

    put skip list ('char=' || c || ' codigo=' || trim(char(rank(c))));

 end caracteres;
```

**Lo que esta clase enseña en PL/I.** `rank(c)` devuelve la posición del carácter en el juego de la
máquina —**base 0**, al contrario que el `ORD` de COBOL— y `byte(n)` es su inversa. En z/OS eso
significa EBCDIC, con todas las consecuencias de la ficha de COBOL: letras no contiguas y minúsculas
antes que mayúsculas.

Lo que PL/I aporta de propio en esta clase es su tratamiento del texto como **cadena de longitud
variable de primera clase**, algo que en 1964 no era normal:

```pli
declare nombre character(50) varying;    /* longitud variable, hasta 50 */
declare fijo   character(50);            /* siempre 50, rellena con blancos */
declare bits   bit(32) aligned;          /* cadena de BITS, no de bytes */
```

Que `character varying` existiera desde el principio es la razón de que PL/I se sintiera más cómodo
que COBOL con el procesamiento de texto. Y las **cadenas de bits** como tipo con operadores propios
—`&`, `|`, `substr` sobre bits— no tienen equivalente en ningún lenguaje del núcleo.

Enterprise PL/I añadió después `widechar` para UTF-16 y las funciones `charg`/`wcharg` para convertir
entre juegos, que es la misma necesidad que resuelve `%ucs2` en RPG.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
CARACT ; Caracteres -- clase 047
 read linea
 set c = $extract(linea, 1)
 write "char=", c, " codigo=", $ascii(c), !
 quit
```

**Lo que esta clase enseña en M.** `$ascii(c)` da el código y `$char(n)` es la inversa. El nombre
delata la época: la función se llama *ascii* porque en 1966 no había otra tabla que nombrar.

`$extract(cadena, n)` es el acceso por posición, y admite un rango: `$extract(cadena, 3, 7)` devuelve
del tercer al séptimo carácter. Es el `substr` de M, y junto a `$piece` —que parte por delimitador—
forma todo el arsenal de manipulación de texto del lenguaje. Con esos dos y la concatenación `_` se
escribe cualquier cosa.

Lo interesante de M en esta clase es lo que hace con **Unicode**: como todo valor es una cadena y las
claves de los *globals* también, la codificación afecta directamente al **orden de la base de datos**.
Recorrer un global con `$order` devuelve las claves en orden de colación, así que cambiar la
codificación cambiaría el orden de los pacientes en un listado.

Por eso las implementaciones modernas separan explícitamente los dos modos: YottaDB distingue **`M`**
(bytes) de **`UTF-8`** (caracteres), y la elección se hace al arrancar el entorno, no por programa.
`$length` cuenta bytes en un modo y caracteres en el otro — el mismo dilema que el `length` de Perl,
resuelto a nivel de instalación en vez de a nivel de fichero.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| c |

c := stdin nextLine first.

Transcript
    show: 'char=', c asString;
    show: ' codigo=', c asInteger printString;
    cr.
```

**Lo que esta clase enseña en Smalltalk.** `Character` es una clase, y sus instancias son **únicas**:
`$a == $a` es verdadero por **identidad**, no solo por igualdad. Los caracteres están internados en
una tabla, así que hay exactamente un objeto por punto de código. Es la misma idea que los símbolos.

La sintaxis literal es `$a` o `$A` —y el espacio se escribe con un `$` seguido de un espacio—, y
para los no imprimibles hay mensajes de clase: `Character cr`, `Character tab`, `Character space`,
`Character value: 241`.

Y aquí aparece de nuevo la lección de fondo de Smalltalk: **`asUppercase` es un mensaje al carácter**,
no una función de biblioteca. Puedes abrir `Character` en el navegador, leer cómo está implementado y
ver que consulta la tabla Unicode. Lo mismo con `isVowel`, `isLetter`, `isDigit`, `isSeparator` — el
catálogo de predicados vive en la clase, junto al dato.

Pharo trabaja con **Unicode completo** y distingue con claridad `String` (bytes, para texto latino
compacto) de `WideString` (32 bits por carácter), promocionando de una a otra de forma automática
cuando aparece un carácter que no cabe. Es la misma estrategia que `SmallInteger` con
`LargePositiveInteger` en la clase 044: **el tipo concreto es un detalle de implementación que el
sistema gestiona solo**, y el programador ve un único concepto.

---

## Y de vuelta a la clase

La lección transferible es que **el orden alfabético no existe: existe el orden de la tabla**. En
ASCII, `'Z' < 'a'`. En EBCDIC, `'a' < 'A'`. En Unicode con reglas de idioma, la `ñ` va entre la `n`
y la `o` en español y al final del alfabeto en otros. Cualquier programa que ordene texto y no
declare qué colación usa está tomando una decisión sin saberlo — y en un lenguaje de 1959 esa
decisión estaba tan a la vista que había una `SPECIAL-NAMES` para cambiarla.

⏮️ [Volver a la clase 047](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
