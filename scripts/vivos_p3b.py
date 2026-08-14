# -*- coding: utf-8 -*-
"""Parte 3, lote B — clases 047 a 051. Ver `vivos_parte3.py` y `gen_vivos.py`.

El código de los ocho lenguajes de la sección 🟢 se ejecuta en CI contra el
`casos.json` de la clase (`scripts/verificar_vivos.py`).
"""

SPECS: dict[str, dict] = {}

# ---------------------------------------------------------------------------
# 047 — Caracteres, texto y Unicode
# ---------------------------------------------------------------------------
SPECS["047"] = dict(
    gancho="""
Leer un carácter y decir qué número lo representa. Es la clase que obliga a mirar debajo del texto,
y allí no hay letras: hay números. La pregunta interesante no es *cuál* es el número, sino **quién
decide la tabla**: porque en el mainframe de IBM la letra `A` no vale 65, vale **193**, y ese
desacuerdo de 1964 sigue costando dinero hoy en cada integración entre un banco y el resto del mundo.
""",
    porque="""
Aquí el concepto es **la codificación: la correspondencia entre un carácter y su número**, y estos
lenguajes lo enseñan porque **no comparten tabla**. COBOL, PL/I y RPG viven en **EBCDIC**, el juego
de caracteres de IBM, donde las letras no son contiguas —entre la `I` y la `J` hay un hueco— y las
minúsculas van *antes* que las mayúsculas. Todo lo demás vive en ASCII y sus descendientes.

Esa es una diferencia que el núcleo no puede mostrar, porque sus diez lenguajes están todos del
mismo lado. Y explica por qué Fortran tiene **dos parejas de funciones** para lo mismo, y por qué en
COBOL ordenar alfabéticamente no da el mismo resultado según la máquina.
""",
    cierre="""
La lección transferible es que **el orden alfabético no existe: existe el orden de la tabla**. En
ASCII, `'Z' < 'a'`. En EBCDIC, `'a' < 'A'`. En Unicode con reglas de idioma, la `ñ` va entre la `n`
y la `o` en español y al final del alfabeto en otros. Cualquier programa que ordene texto y no
declare qué colación usa está tomando una decisión sin saberlo — y en un lenguaje de 1959 esa
decisión estaba tan a la vista que había una `SPECIAL-NAMES` para cambiarla.
""",
    langs={
        "cobol": ("""
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
""", """
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
"""),
        "fortran": ("""
program caracteres
   implicit none
   character(len=1) :: c

   read(*, '(A)') c

   write(*, '(A,A,A,I0)') 'char=', c, ' codigo=', iachar(c)
end program caracteres
""", """
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
"""),
        "ada": ("""
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
""", """
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
"""),
        "pascal": ("""
program Caracteres;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  C: Char;

begin
  Read(C);
  WriteLn('char=', C, ' codigo=', IntToStr(Ord(C)));
end.
""", """
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
"""),
        "lisp": ("""
(let ((c (read-char)))
  (format t "char=~C codigo=~D~%" c (char-code c)))
""", """
**Lo que esta clase enseña en Common Lisp.** Los caracteres son **objetos de primera clase con
sintaxis propia**: se escriben `#\\a`, `#\\A`, `#\\Space`, `#\\Newline`, `#\\Tab`. Esa notación `#\\`
existe precisamente porque un carácter **no es una cadena de longitud uno** —distinción que Python
no hace y que causa más confusión de la que parece.

`char-code` y su inversa `code-char` dan el punto de código. En las implementaciones modernas —SBCL
entre ellas— es **Unicode completo**, así que `(char-code #\\ñ)` da 241 y `(char-code #\\€)` da 8364.

Y hay dos familias de comparadores, que es la parte interesante para esta clase:

```lisp
(char= #\\a #\\A)        ; => NIL   distingue mayúsculas
(char-equal #\\a #\\A)   ; => T     no las distingue
(char< #\\a #\\b)        ; => T
(string< "casa" "caso") ; => 3     devuelve el índice donde difieren, no un booleano
```

Que `string<` devuelva **la posición del primer carácter distinto** en lugar de `T` es muy propio de
Lisp: el dato útil es más informativo que el booleano, y `nil` sigue sirviendo como falso. Es la
misma filosofía que hace que `and` devuelva el último valor en vez de `T`.
"""),
        "tcl": ("""
gets stdin linea
set c [string index $linea 0]
scan $c %c codigo

puts "char=$c codigo=$codigo"
""", """
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
"""),
        "perl": ("""
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;
my $c = substr($linea, 0, 1);

printf "char=%s codigo=%d\\n", $c, ord($c);
""", """
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

Perl añade además la pregunta que casi nadie se hace: `"\\N{LATIN SMALL LETTER N WITH TILDE}"`
permite escribir un carácter **por su nombre Unicode**, y `\\p{Letter}` en una expresión regular
casa cualquier letra de cualquier alfabeto.
"""),
        "cpp": ("""
#include <iostream>

int main() {
    char c{};
    if (!(std::cin >> c)) return 1;

    std::cout << "char=" << c
              << " codigo=" << static_cast<int>(static_cast<unsigned char>(c))
              << '\\n';
    return 0;
}
""", """
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
"""),
        "rpg": ("""
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
""", """
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
"""),
        "pli": ("""
 caracteres: procedure options(main);

    declare linea character(80) varying;
    declare c     character(1);

    get edit (linea) (a(80));
    c = substr(linea, 1, 1);

    put skip list ('char=' || c || ' codigo=' || trim(char(rank(c))));

 end caracteres;
""", """
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
"""),
        "mumps": ("""
CARACT ; Caracteres -- clase 047
 read linea
 set c = $extract(linea, 1)
 write "char=", c, " codigo=", $ascii(c), !
 quit
""", """
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
"""),
        "smalltalk": ("""
| c |

c := stdin nextLine first.

Transcript
    show: 'char=', c asString;
    show: ' codigo=', c asInteger printString;
    cr.
""", """
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
"""),
    },
)

# ---------------------------------------------------------------------------
# 048 — Cadenas: representación, inmutabilidad e interpolación
# ---------------------------------------------------------------------------
SPECS["048"] = dict(
    gancho="""
Leer una palabra y decir cuánto mide. Dos operaciones triviales que esconden la pregunta que separa
a estos doce lenguajes: **¿dónde está escrita la longitud de una cadena?** ¿En un contador delante
del texto, en un byte cero al final, en el tipo, o en ninguna parte porque el campo siempre mide lo
mismo y se rellena con espacios?
""",
    porque="""
Aquí el concepto es **la representación física de una cadena**, y estos lenguajes cubren las cuatro
respuestas posibles, cosa que el núcleo no hace. COBOL y Fortran usan **campos de longitud fija
rellenos de espacios**, así que la longitud "real" es una convención y `TRIM` aparece por todas
partes. PL/I y RPG tienen cadenas **con contador** (`varying`, `varchar`). C++ arrastra las cadenas
**terminadas en cero** de C junto a `std::string`. Y Smalltalk y Lisp las tratan como **colecciones
de objetos**, con toda la maquinaria de colecciones aplicable.

Cada respuesta arrastra sus propios errores característicos, y reconocerlos es lo transferible.
""",
    cierre="""
Si algo deja claro esta página es que **"longitud de una cadena" no es una pregunta única**. Puede
ser el tamaño del campo, la posición del último carácter no blanco, el contador guardado delante, la
distancia hasta el byte cero, o el número de caracteres Unicode — que ya vimos en la clase 047 que
tampoco es el número de bytes. Cuando un programa mezcla dos de esas definiciones sin darse cuenta,
aparece el defecto más difícil de encontrar de todos: el que solo se manifiesta con ciertos datos.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. CADENAS.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA     PIC X(80).
01  PALABRA   PIC X(80).
01  LONGITUD  PIC 9(4) COMP-3.
01  ED-LON    PIC Z(3)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    MOVE FUNCTION TRIM(LINEA) TO PALABRA
    COMPUTE LONGITUD = FUNCTION LENGTH(FUNCTION TRIM(PALABRA))
    MOVE LONGITUD TO ED-LON
    DISPLAY "hola=" FUNCTION TRIM(PALABRA)
            " longitud=" FUNCTION TRIM(ED-LON)
    STOP RUN.
""", """
**Lo que esta clase enseña en COBOL.** En COBOL una cadena **no tiene longitud**: tiene **tamaño**.
`PIC X(80)` mide siempre ochenta caracteres, contengan lo que contengan. Si guardas `"Ada"`, los
otros 77 son espacios. `FUNCTION LENGTH(PALABRA)` devolvería **80**, no 3.

De ahí que `FUNCTION TRIM` aparezca en casi todas las líneas de esta página, y de ahí también el
error más frecuente al integrar un sistema COBOL con cualquier otro: **los campos llegan rellenos de
espacios** y el receptor los toma como parte del dato. Un `"MADRID   "` que no casa con `"MADRID"`.

Esa decisión no es un descuido, es coherencia con el modelo: un registro de un fichero tiene
posiciones fijas, así que un campo también. Toda la `DATA DIVISION` describe posiciones exactas
dentro de un registro, y una longitud variable rompería esa correspondencia.

COBOL 2002 añadió la alternativa —`PIC X(80) VARYING`, con contador— pero el grueso del código en
producción es de longitud fija, y conviene contar con ello al leerlo.

Y las operaciones tienen verbo propio, no operadores: `STRING` para concatenar, `UNSTRING` para
partir, `INSPECT` para contar o reemplazar. Concatenar dos campos es una sentencia completa, no un
`+`.
"""),
        "fortran": ("""
program cadenas
   implicit none
   character(len=100) :: palabra

   read(*, '(A)') palabra

   write(*, '(A,A,A,I0)') 'hola=', trim(palabra), &
                          ' longitud=', len_trim(palabra)
end program cadenas
""", """
**Lo que esta clase enseña en Fortran.** El mismo modelo que COBOL, y con la misma consecuencia:
`character(len=100)` mide siempre 100. Por eso Fortran tiene **dos funciones distintas** donde otros
lenguajes tienen una:

| Función | Devuelve |
|---|---|
| `len(s)` | El **tamaño declarado** — aquí, 100 |
| `len_trim(s)` | La posición del **último carácter no blanco** — aquí, 3 |

Confundirlas es el error clásico. `len` es una propiedad del **tipo** y se conoce en tiempo de
compilación; `len_trim` mira el **contenido** y hay que ejecutarla.

Fortran 2003 añadió por fin la longitud diferida, que es lo que se usa hoy en código nuevo:

```fortran
character(len=:), allocatable :: nombre
nombre = 'Ada'          ! se dimensiona sola: len(nombre) == 3
nombre = 'Fortran'      ! se redimensiona: len(nombre) == 7
```

Con `allocatable`, la asignación **reasigna** el tamaño y `len` sí devuelve lo esperado. Es la
diferencia entre el Fortran de 1977 y el de hoy, y explica por qué el código antiguo está lleno de
`trim()` y el moderno mucho menos.

Y `//` es la concatenación —no un comentario— con la trampa de que `'a' // 'b'` sobre campos de
longitud fija concatena **incluidos los espacios de relleno**. De ahí `trim(a) // trim(b)`.
"""),
        "ada": ("""
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Cadenas is
   Palabra : String (1 .. 100);
   Ultimo  : Natural;
begin
   Get_Line (Palabra, Ultimo);

   Put ("hola=" & Palabra (1 .. Ultimo));
   Put (" longitud=");
   Put (Ultimo, Width => 1);
   New_Line;
end Cadenas;
""", """
**Lo que esta clase enseña en Ada.** `String` en Ada es **un array de caracteres con límites fijos**,
declarado como `array (Positive range <>) of Character`. Su longitud forma parte del **tipo del
objeto** y no puede cambiar después de crearlo. Por eso `Get_Line` recibe **dos** cosas: el búfer y
una variable de salida `Ultimo` que dice hasta dónde se llenó.

Y `Palabra (1 .. Ultimo)` no es una función de subcadena: es una **porción de array**, la misma
sintaxis que se usaría con un array de enteros. Las cadenas no son un caso especial del lenguaje; son
arrays, y todo lo que vale para arrays vale para ellas.

Cuando la longitud fija estorba, Ada ofrece dos alternativas en la biblioteca estándar, y la elección
entre ellas es una decisión de ingeniería que el lenguaje deja explícita:

```ada
with Ada.Strings.Bounded;    --  longitud variable con MÁXIMO declarado
with Ada.Strings.Unbounded;  --  longitud libre, con memoria dinámica
```

`Bounded` se usa en sistemas críticos porque **no reserva memoria dinámica**: el tamaño máximo se
conoce al compilar, así que no hay fragmentación ni fallos de asignación imprevisibles. `Unbounded` es
cómodo y usa el montículo. En aviónica se elige `Bounded`, y esa preferencia dice mucho sobre para qué
se diseñó el lenguaje.
"""),
        "pascal": ("""
program Cadenas;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  Palabra: string;

begin
  ReadLn(Palabra);
  Palabra := Trim(Palabra);

  WriteLn('hola=', Palabra, ' longitud=', IntToStr(Length(Palabra)));
end.
""", """
**Lo que esta clase enseña en Pascal.** Pascal inventó la **cadena con contador**, y esa decisión de
1970 sigue siendo relevante. El `ShortString` clásico guarda la longitud en el **byte 0** del propio
dato: por eso mide como máximo 255 caracteres, y por eso `Length(s)` es **una lectura de un byte**,
no un recorrido.

Compara con C, donde la cadena termina en un byte cero y `strlen` tiene que **recorrer** el texto
entero para contarlo. Un bucle que llame a `strlen` en cada vuelta es cuadrático; en Pascal es
constante. Ese detalle de representación tiene consecuencias de rendimiento medibles, y es la razón
de que casi todos los lenguajes posteriores —Java, C#, Go, Rust, Python— hayan elegido el contador y
no el terminador.

La directiva `{$H+}` de este programa cambia el significado de `string`: sin ella es `ShortString`
(255 caracteres, en la pila); con ella es `AnsiString`, de longitud ilimitada, con **conteo de
referencias** y **copia al escribir**. Es decir, asignar una cadena a otra no copia el texto: copia
un puntero e incrementa un contador; solo se copia de verdad si alguien la modifica.

Esa combinación —conteo de referencias más copia perezosa— es la misma que usan Delphi, PHP y Swift,
y es lo que permite pasar cadenas grandes por valor sin coste.
"""),
        "lisp": ("""
(let ((palabra (string-trim '(#\\Space #\\Tab #\\Return) (read-line))))
  (format t "hola=~A longitud=~D~%" palabra (length palabra)))
""", """
**Lo que esta clase enseña en Common Lisp.** Una cadena de Lisp **es un array de caracteres**, sin
metáfora: su tipo real es `(vector character)`. Y esa no es una curiosidad, es la clave de todo,
porque significa que **las funciones de secuencia funcionan sobre ella**:

```lisp
(length  "polyglot")               ; => 8
(reverse "polyglot")               ; => "tolgylop"
(subseq  "polyglot" 4)             ; => "glot"
(position #\\g "polyglot")          ; => 4
(remove-if #'(lambda (c) (find c "aeiou")) "polyglot")  ; => "plyglt"
(sort (copy-seq "polyglot") #'char<)                    ; => "gglloopty"
```

`length`, `reverse`, `subseq`, `position`, `remove-if`, `sort`, `map`, `reduce`: **las mismas
funciones que se usan con listas y con vectores**. No hay una biblioteca de cadenas separada, porque
una cadena no es una cosa aparte. Ese es el rendimiento del diseño uniforme: aprendes las funciones
de secuencia una vez y sirven para los tres tipos.

Y `string-trim` recibe **el conjunto de caracteres a recortar** como argumento, en lugar de asumir
"los espacios en blanco". Es más verboso y es más honesto: ¿el tabulador cuenta?, ¿el retorno de
carro?, ¿el espacio de no separación? En Lisp lo dices tú.
"""),
        "tcl": ("""
gets stdin linea
set palabra [string trim $linea]

puts "hola=$palabra longitud=[string length $palabra]"
""", """
**Lo que esta clase enseña en Tcl.** Es el lenguaje donde esta clase es **todo el lenguaje**: si todo
valor es una cadena, entonces las operaciones sobre cadenas son las operaciones fundamentales. Por
eso `string` es un comando con más de treinta subcomandos: `length`, `index`, `range`, `first`,
`last`, `map`, `match`, `trim`, `tolower`, `repeat`, `compare`, `is`…

`string is` merece atención porque resuelve, sin tipos, el problema que los tipos resolverían:

```tcl
string is integer -strict $x     ;# ¿esta cadena es un entero?
string is double -strict $x
string is alnum -strict $x
```

En un lenguaje sin tipos, **la validación sustituye a la declaración**. Es la misma función que
cumple `PIC 9(9)` en COBOL, movida del momento de declarar al momento de comprobar.

Y sobre la interpolación, que es el otro tema de esta clase: Tcl la tiene desde 1988 con la sintaxis
que después copió medio mundo. `"hola $nombre"` sustituye la variable; `{hola $nombre}` no sustituye
nada. **Las comillas y las llaves no son dos formas de citar lo mismo**: son "con sustitución" y "sin
sustitución", y elegir mal es el error más común del lenguaje.
"""),
        "perl": ("""
use strict;
use warnings;

my $palabra = <STDIN>;
chomp $palabra;

printf "hola=%s longitud=%d\\n", $palabra, length($palabra);
""", """
**Lo que esta clase enseña en Perl.** La interpolación de Perl es la más completa de esta página y
es el rasgo que definió al lenguaje: dentro de comillas dobles se sustituyen variables escalares,
elementos de array, elementos de hash, listas enteras y hasta expresiones:

```perl
print "Hola $nombre, tienes $edad años\\n";
print "El primero es $lista[0] y la clave es $h{color}\\n";
print "Toda la lista: @lista\\n";           # los une con espacios
print "Resultado: @{[ $a * $b ]}\\n";       # el idioma para interpolar una expresión
```

Las comillas **simples** no interpolan nada, exactamente como las llaves de Tcl. Y `qq{}` y `q{}` son
las formas alternativas cuando el texto ya lleva comillas.

Sobre la representación: un escalar de Perl guarda la longitud junto al texto —no hay terminador
nulo—, así que `length` es constante y las cadenas **pueden contener bytes nulos** sin problema. Eso
importa al procesar datos binarios, donde C se rompe.

Y las cadenas de Perl son **mutables**: `substr` no solo lee, también **escribe**, e incluso puede
usarse como destino de una asignación —`substr($s, 0, 3) = "XYZ"`—. Es la diferencia con Python y
Java, donde toda operación sobre una cadena crea otra. Ninguna postura es mejor: la inmutabilidad
permite compartir sin copiar, y la mutabilidad evita copias al modificar en sitio.
"""),
        "cpp": ("""
#include <iostream>
#include <string>

int main() {
    std::string palabra;
    if (!(std::cin >> palabra)) return 1;

    std::cout << "hola=" << palabra
              << " longitud=" << palabra.size() << '\\n';
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** C++ arrastra **las dos representaciones a la vez**, y esa
convivencia es la fuente de una parte enorme de sus problemas históricos:

| | `const char*` (de C) | `std::string` |
|---|---|---|
| Longitud | Hasta el byte `\\0` — `strlen` **recorre** | Guardada — `size()` es constante |
| Memoria | Tú la gestionas | La gestiona el objeto |
| Nulos dentro | Imposible | Permitidos |
| Coste de `length` | O(n) | O(1) |

Las cadenas terminadas en cero son la causa directa de desbordamientos de búfer que llevan cincuenta
años apareciendo en boletines de seguridad, porque **la longitud no está en el dato**: hay que
confiar en que alguien puso el cero.

`std::string` lo resuelve, y añade la **optimización de cadena corta** (*SSO*): las cadenas de hasta
unos 15 caracteres se guardan **dentro del propio objeto**, sin tocar el montículo. Por eso manejar
millones de palabras cortas en C++ es tan rápido — un detalle de implementación que no está en el
estándar pero que tienen todas las bibliotecas serias.

Y C++17 añadió `std::string_view`: una **vista** —puntero más longitud— sobre una cadena que ya
existe, sin copiarla. Pasar un `string_view` a una función que solo lee evita una copia completa. Su
peligro es simétrico a su virtud: la vista **no es dueña** de los datos, así que si la cadena original
muere, la vista queda colgando.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi CADENAS;
  palabra varchar(100) const;
end-pi;

dcl-s limpia varchar(100);
dcl-s salida char(150);

limpia = %trim(palabra);

salida = 'hola=' + limpia + ' longitud=' + %char(%len(limpia));
dsply salida;

*inlr = *on;
return;
""", """
**Lo que esta clase enseña en RPG.** RPG tiene **las dos representaciones con nombres distintos**, y
la diferencia es visible en la declaración:

```rpgle
dcl-s fijo    char(100);      // siempre 100, relleno de blancos, como COBOL
dcl-s variable varchar(100);  // longitud guardada delante, hasta 100
```

`%len(campo)` sobre un `char` devuelve **100**; sobre un `varchar`, la longitud real. Es exactamente
la distinción `len`/`len_trim` de Fortran, pero movida al tipo en vez de a la función: en RPG el tipo
te dice qué significa la longitud.

`%trim`, `%triml` y `%trimr` recortan por los dos lados, por la izquierda o por la derecha, y en
código real aparecen constantemente porque la base de datos histórica de IBM i está llena de campos
`char` de longitud fija.

Y hay una función que conviene conocer porque no tiene equivalente directo en el núcleo: **`%scanrpl`**,
que busca y reemplaza en una sola pasada, y **`%split`**, añadida en versiones recientes, que parte
una cadena por un delimitador y devuelve una **matriz**. Que `%split` sea reciente dice mucho: durante
treinta años, partir una cadena en RPG se hacía con un bucle y `%scan`.
"""),
        "pli": ("""
 cadenas: procedure options(main);

    declare linea   character(80) varying;
    declare palabra character(80) varying;

    get edit (linea) (a(80));
    palabra = trim(linea);

    put skip list ('hola=' || palabra ||
                   ' longitud=' || trim(char(length(palabra))));

 end cadenas;
""", """
**Lo que esta clase enseña en PL/I.** PL/I tuvo **cadenas de longitud variable en 1964**, veinte años
antes que casi nadie, con el atributo `varying`: la longitud se guarda en una media palabra delante
del texto, exactamente el modelo que después adoptaron Pascal, Java y Go.

Y tiene un catálogo de operaciones sobre texto que en su momento no tenía rival y que sigue siendo
sorprendente:

```pli
index(cadena, patron)          /* posición de la primera aparición */
verify(cadena, conjunto)       /* primera posición que NO está en el conjunto */
translate(cadena, nuevo, viejo)/* sustitución carácter a carácter */
repeat(cadena, n)              /* replicación */
substr(cadena, i, n)           /* subcadena — también como DESTINO de asignación */
```

`verify` es la que casi nadie tiene: devuelve la posición del primer carácter que **no** pertenece a
un conjunto dado, lo que valida un campo entero en una llamada. `verify(codigo, '0123456789') = 0`
significa "son todo dígitos". Es la validación sin expresiones regulares, y es rapidísima.

Y `substr` como **pseudovariable** —a la izquierda del igual— permite modificar en el sitio:
`substr(nombre, 1, 1) = 'X'`. Es la misma capacidad que tiene Perl y que Java y Python no tienen.
"""),
        "mumps": ("""
CADENAS ; Cadenas -- clase 048
 read palabra
 write "hola=", palabra, " longitud=", $length(palabra), !
 quit
""", """
**Lo que esta clase enseña en M.** En M **todo es una cadena**, así que este programa no convierte
nada: `palabra` ya es lo que hay que imprimir y `$length` lo cuenta. Es el programa más corto de la
página, y no por casualidad.

Lo interesante es `$length` con **dos** argumentos, que hace algo completamente distinto:

```mumps
set fila = "Pérez^María^1978-04-12^O+"
write $length(fila)            ; 25 -- caracteres
write $length(fila, "^")       ; 4  -- CAMPOS separados por ^
write $piece(fila, "^", 2)     ; María
```

`$length(cadena, delimitador)` cuenta **trozos**, no caracteres. Junto a `$piece`, que extrae el
trozo *n*, forma el modelo de datos ligero de M: **un registro entero es una cadena con delimitadores**,
y se guarda así en el *global*. Nada de estructuras, nada de serialización, nada de esquema.

Ese es el motivo de que los sistemas clínicos en M sean tan compactos y tan difíciles de leer sin
documentación: `$P(^PAC(id,0),U,3)` es el tercer campo del nodo cero del paciente, y qué sea ese
tercer campo solo lo sabe el diccionario de datos. VistA lo resuelve con **FileMan**, un diccionario
que describe cada global y que es, en la práctica, el esquema que el lenguaje no tiene.
"""),
        "smalltalk": ("""
| palabra |

palabra := stdin nextLine trimBoth.

Transcript
    show: 'hola=', palabra;
    show: ' longitud=', palabra size printString;
    cr.
""", """
**Lo que esta clase enseña en Smalltalk.** Una cadena es **una colección de caracteres**, y por eso
el mensaje para su longitud es `size` — el mismo que para un array, un diccionario o un conjunto. No
existe `length` como concepto aparte.

Y de ahí se sigue lo importante: **todo el protocolo de colecciones funciona sobre texto**.

```smalltalk
'polyglot' size                                  "8"
'polyglot' reversed                              "'tolgylop'"
'polyglot' asUppercase                           "'POLYGLOT'"
'polyglot' select: [ :c | c isVowel ]            "'ooo'"
'polyglot' collect: [ :c | c asUppercase ]       "'POLYGLOT'"
'polyglot' detect: [ :c | c isVowel ]            "$o"
'polyglot' inject: 0 into: [ :a :c | a + 1 ]     "8"
'uno dos tres' substrings                        "#('uno' 'dos' 'tres')"
```

`select:`, `collect:`, `detect:`, `inject:into:` son los mismos mensajes que se envían a cualquier
colección. Es la misma uniformidad que Lisp consigue con las funciones de secuencia, obtenida por
herencia en vez de por polimorfismo de funciones.

Sobre la mutabilidad, Smalltalk hace una distinción precisa que conviene conocer: **los literales de
cadena son objetos concretos del método compilado**, así que modificarlos altera el propio código
—en Pharo están marcados como de solo lectura para evitarlo—. Para una cadena que vas a modificar se
usa `String new: 10` o `copy`. Y para texto que se construye por trozos, `WriteStream`, que es el
equivalente de `StringBuilder`.
"""),
    },
)

# ---------------------------------------------------------------------------
# 049 — Conversión de tipos: casting explícito vs. coerción implícita
# ---------------------------------------------------------------------------
SPECS["049"] = dict(
    gancho="""
Tomar `3.7` y quedarse con `3`. Todo el mundo sabe hacerlo; casi nadie sabe qué hace su lenguaje
cuando **no** se lo pides. Esta clase separa la **conversión explícita** —la que escribes— de la
**coerción implícita** —la que el lenguaje hace por su cuenta—, y de paso descubre una trampa que
sorprende incluso a programadores veteranos: **no todos los lenguajes truncan al convertir a entero.
Ada redondea.**
""",
    porque="""
Aquí el concepto es **quién decide una conversión y cuándo**, y estos lenguajes ocupan todo el
espectro. En un extremo, **Ada**: no hay ninguna conversión implícita entre tipos numéricos, todas se
escriben, y aun así `Integer(3.7)` da **4** y no 3 — porque la conversión *escrita* también tiene una
semántica que hay que conocer. En el otro extremo, **M** y **Tcl**, donde no hay conversión porque no
hay tipos, y el resultado depende del operador que toques.

Y en medio, COBOL con algo que ningún lenguaje moderno tiene: **la conversión ocurre en el `MOVE`**,
gobernada por la forma del destino, y trunca por la izquierda sin avisar si el destino es más corto.
""",
    cierre="""
Dos reglas transferibles. La primera: **truncar y redondear no son lo mismo, y tu lenguaje ha elegido
uno por ti**. C, C++, Perl, Tcl y Pascal truncan hacia cero; Ada redondea; RPG redondea con `/` pero
trunca con `%int`. Comprueba cuál antes de escribir un cálculo con dinero.

La segunda: **una conversión implícita es una decisión que nadie revisó**. Ada la prohíbe entera y
paga verbosidad a cambio; COBOL la esconde en el `MOVE`; Perl y M ni siquiera la consideran una
conversión. Saber en qué punto del espectro está tu lenguaje es lo que evita el defecto silencioso.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. CONVERSION.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  R       PIC S9(9)V99 COMP-3.
01  E       PIC S9(9)    COMP-3.
01  ED-E    PIC -(9)9.
01  ED-R    PIC -(9)9.99.

PROCEDURE DIVISION.
    ACCEPT LINEA
    MOVE FUNCTION NUMVAL(LINEA) TO R
    MOVE R TO E
    MOVE E TO ED-E
    MOVE R TO ED-R
    DISPLAY "entero=" FUNCTION TRIM(ED-E)
            " real=" FUNCTION TRIM(ED-R)
    STOP RUN.
""", """
**Lo que esta clase enseña en COBOL.** `MOVE R TO E` es **la conversión implícita de COBOL**, y es la
razón de que `MOVE` no sea un simple `=`. El destino manda: `E` es `PIC S9(9)` sin decimales, así que
los decimales de `R` **se descartan** —truncados, no redondeados— y nadie avisa.

Y hay una segunda parte, mucho más peligrosa, que es el motivo de que esta clase importe en COBOL:
**la truncación también ocurre por la izquierda**.

```cobol
01  GRANDE  PIC 9(9)  VALUE 123456789.
01  CHICO   PIC 9(3).

MOVE GRANDE TO CHICO      *> CHICO vale 789.  Sin error. Sin aviso.
```

Se pierden los seis dígitos más significativos y el programa continúa. Es el fallo silencioso
característico del lenguaje, y la razón de que las revisiones de código COBOL se centren tanto en
comprobar que los `PIC` de origen y destino cuadran.

La forma de no sufrirlo es pedir el aviso explícitamente, que existe pero hay que escribirlo:

```cobol
COMPUTE CHICO = GRANDE
    ON SIZE ERROR DISPLAY "no cabe"
END-COMPUTE
```

`ON SIZE ERROR` funciona en `COMPUTE`, `ADD`, `SUBTRACT`, `MULTIPLY` y `DIVIDE` — pero **no en
`MOVE`**. Mover nunca avisa. Ese detalle explica muchos incidentes.
"""),
        "fortran": ("""
program conversion
   implicit none
   real(kind=8) :: r
   integer :: e
   character(len=32) :: buf

   read(*, *) r
   e = int(r)                    ! int() trunca HACIA CERO

   write(buf, '(F20.2)') r
   write(*, '(A,I0,A,A)') 'entero=', e, ' real=', trim(adjustl(buf))
end program conversion
""", """
**Lo que esta clase enseña en Fortran.** Fortran tiene **cuatro funciones distintas** para pasar de
real a entero, y esa es toda la lección: la conversión no es una operación, son cuatro decisiones
diferentes con nombre propio.

| Función | `3.7` | `-3.7` | Qué hace |
|---|---|---|---|
| `int(x)` | 3 | -3 | Trunca **hacia cero** |
| `nint(x)` | 4 | -4 | Redondea al **más cercano** |
| `floor(x)` | 3 | **-4** | Al entero **inferior** |
| `ceiling(x)` | 4 | -3 | Al entero **superior** |

Fíjate en la columna de los negativos, que es donde se ven las diferencias reales: `int(-3.7)` da
`-3` y `floor(-3.7)` da `-4`. Confundirlas produce errores que solo aparecen con datos negativos,
que suelen ser los que no están en las pruebas.

En cambio, la conversión **en el otro sentido sí es implícita**: `r = 5` promociona el entero a real
sin decir nada, porque no se pierde información. Fortran aplica la misma regla que Pascal — la
promoción segura es automática, la que pierde datos hay que escribirla.

Y hay una trampa clásica de la que esta clase debe advertir: **`1/2` en Fortran da `0`**. Si los dos
operandos son enteros, la división es entera, aunque el destino sea real. `r = 1/2` deja `r` a cero;
hay que escribir `r = 1.0/2.0`. El mismo error existe en C, Java y Go.
"""),
        "ada": ("""
with Ada.Text_IO;            use Ada.Text_IO;
with Ada.Integer_Text_IO;    use Ada.Integer_Text_IO;
with Ada.Long_Float_Text_IO; use Ada.Long_Float_Text_IO;

procedure Conversion is
   R : Long_Float;
   E : Integer;
begin
   Get (R);

   --  ¡Integer (R) REDONDEA en Ada!  Para truncar hace falta el atributo.
   E := Integer (Long_Float'Truncation (R));

   Put ("entero="); Put (E, Width => 1);
   Put (" real=");  Put (R, Fore => 1, Aft => 2, Exp => 0);
   New_Line;
end Conversion;
""", """
**Lo que esta clase enseña en Ada.** Esta es la sorpresa más útil de toda la Parte 3: **en Ada,
`Integer (3.7)` da `4`, no `3`.** La conversión de real a entero **redondea al más cercano**, al
contrario que en C, C++, Java, Go, Rust, Python, Perl, Tcl y Pascal, donde trunca.

No es un capricho. Ada considera que convertir es *representar el mismo valor en otro tipo*, y la
representación más fiel de 3.7 como entero es 4. Truncar es una operación **distinta**, y por eso
tiene un nombre distinto: el atributo `'Truncation`. Junto a él están `'Rounding`, `'Floor` y
`'Ceiling`, la misma familia que las cuatro funciones de Fortran.

Es exactamente la clase de detalle que hace que portar un algoritmo entre lenguajes sin leer el
manual produzca resultados que difieren en uno. Y el motivo de que Ada obligue a escribir **todas**
las conversiones: si tienes que escribirla, tienes que pensar cuál.

```ada
E := Integer (R);                       --  redondea: 4
E := Integer (Long_Float'Truncation(R));--  trunca:   3
E := Integer (Long_Float'Floor (R));    --  hacia abajo
```

Y aún hay una segunda capa: si `E` fuera de un subtipo con rango —`subtype Nota is Integer range
1 .. 7`— la conversión además **comprobaría el rango** y levantaría `Constraint_Error`. La conversión
en Ada convierte, redondea y valida, todo en el mismo sitio visible.
"""),
        "pascal": ("""
program Conversion;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  R: Double;
  E: Integer;

begin
  Read(R);
  E := Trunc(R);          { Trunc corta hacia cero; Round redondearía }

  WriteLn('entero=', IntToStr(E), ' real=', R:0:2);
end.
""", """
**Lo que esta clase enseña en Pascal.** Pascal fue de los primeros en separar las dos operaciones con
nombres distintos y obligatorios: **`Trunc`** corta hacia cero y **`Round`** redondea. No existe una
conversión implícita de real a entero — `E := R` **no compila**—, así que el programador tiene que
elegir una de las dos en cada sitio.

Esa obligación es la política que Ada heredaría después, y el contraste con C es claro: en C,
`int e = r;` compila, trunca, y nadie se entera de que hubo una decisión.

Hay un detalle de `Round` que conviene conocer porque contradice la intuición: en Delphi y Free
Pascal, `Round` usa **redondeo bancario** —al par más cercano— porque sigue el estándar IEEE 754. Así
que `Round(2.5)` da **2** y `Round(3.5)` da **4**. Quien espera 3 y 4 se lleva una sorpresa, y en un
cálculo de importes esa sorpresa es un descuadre. Para el redondeo "de toda la vida" hay que usar
`SimpleRoundTo` de `Math`.

La promoción en la dirección segura sí es automática: `R := E` funciona. Y la conversión desde texto
es explícita y con su propia familia de funciones —`StrToInt`, `StrToFloat`, `StrToIntDef`, `TryStrToInt`—
donde las dos últimas son las importantes: una devuelve un valor por defecto y la otra un booleano,
en lugar de lanzar una excepción con datos sucios.
"""),
        "lisp": ("""
(setf *read-default-float-format* 'double-float)

(let* ((r (read))
       (e (truncate r)))
  (format t "entero=~D real=~,2F~%" e r))
""", """
**Lo que esta clase enseña en Common Lisp.** Lisp tiene las cuatro operaciones con nombres claros
—`truncate`, `round`, `floor`, `ceiling`— y una peculiaridad que las hace mejores que sus
equivalentes en otros lenguajes: **devuelven dos valores**.

```lisp
(truncate 3.7)     ; => 3  y  0.7
(floor -3.7)       ; => -4 y  0.3
(round 2.5)        ; => 2  y  0.5    ¡redondeo bancario, como Pascal!
(multiple-value-bind (cociente resto) (truncate 17 5)
  (format t "~D con resto ~D" cociente resto))   ; 3 con resto 2
```

El segundo valor es **el resto**, es decir, lo que se perdió al convertir. Casi siempre se ignora
—`format` solo usa el primero—, pero está ahí sin coste si lo necesitas. Los valores múltiples de
Lisp son un mecanismo del lenguaje, no una tupla: no se construye ningún objeto, así que ignorarlos es
gratis. Muy pocos lenguajes lo tienen; Go lo aproxima con retornos múltiples, pero allí hay que
declarar que los ignoras.

Y `round` en Lisp también usa **redondeo bancario** —`(round 2.5)` es 2 y `(round 3.5)` es 4—, la
misma regla que Pascal y que el estándar IEEE. Que dos lenguajes tan distintos coincidan aquí y
difieran de C es un buen recordatorio de que "redondear" tampoco significa lo mismo en todas partes.
"""),
        "tcl": ("""
gets stdin linea
set r [string trim $linea]

set e [expr {int($r)}]

puts "entero=$e real=[format %.2f $r]"
""", """
**Lo que esta clase enseña en Tcl.** En un lenguaje sin tipos, la conversión **no existe como
concepto**: lo que existe es la interpretación que hace cada operación. `$r` contiene la cadena
`"3.7"` todo el tiempo; `int()` la lee como número y devuelve la parte entera, `format %.2f` la lee
como real, y `string length` la contaría como texto de tres caracteres.

Dentro de `expr`, Tcl ofrece las cuatro funciones habituales —`int()`, `round()`, `floor()`,
`ceil()`— con la semántica de C: `int()` trunca hacia cero.

Pero hay una trampa muy específica de Tcl que conviene conocer, porque contradice lo que la intuición
sugiere en un lenguaje de tipado débil: **la división de dos enteros es entera**.

```tcl
expr {7 / 2}        ;# 3     -- ¡ambos son enteros!
expr {7 / 2.0}      ;# 3.5
expr {double(7)/2}  ;# 3.5
```

Que un lenguaje sin tipos preserve la distinción entero/real en la división sorprende, y es
deliberado: Tcl mira el **texto** de los operandos para decidir. `"7"` parece entero, `"7.0"` parece
real. La forma en que escribes el literal cambia el resultado — que es, exactamente, lo que significa
que el tipo lo aporte la operación y no el dato.

Y desde Tcl 8.5 `int()` está limitado a la palabra de máquina; para valores grandes hay que usar
`entier()`, que respeta la precisión arbitraria.
"""),
        "perl": ("""
use strict;
use warnings;

my $r = <STDIN>;
chomp $r;

my $e = int($r);          # int() trunca hacia cero, NO redondea

printf "entero=%d real=%.2f\\n", $e, $r;
""", """
**Lo que esta clase enseña en Perl.** Perl es el extremo opuesto de Ada: **no hay conversión porque
no hay tipos que convertir**. Un escalar guarda a la vez su forma numérica y su forma textual, y cada
operador usa la que necesita. `"3.7" + 0` es 3.7 y `3.7 . ""` es `"3.7"`, sin que ocurra nada
especial.

`int()` trunca hacia cero, como en C. Para redondear no hay función incorporada, y el idioma clásico
es `int($x + 0.5)` —que falla con negativos— o `sprintf("%.0f", $x)`, que usa redondeo bancario.
Que Perl no traiga `round` es una de sus rarezas más comentadas; `POSIX::floor` y `POSIX::ceil` sí
están, importando el módulo.

Lo específico de esta clase en Perl es lo que ocurre cuando el texto **no** es un número:

```perl
my $x = "12abc" + 0;    # 12   -- lee el prefijo y descarta el resto
my $y = "abc" + 0;      # 0
```

Sin `use warnings`, eso pasa en silencio. **Con** `use warnings`, Perl emite
`Argument "12abc" isn't numeric in addition`, que es exactamente el aviso que M **no** da y que
convierte un tipado débil manejable en uno peligroso. Es el mejor argumento de esta página a favor
de activar los avisos: no cambian la semántica, hacen visible la coerción.

Y `looks_like_number` de `Scalar::Util` es la comprobación explícita, el equivalente de
`string is double` en Tcl.
"""),
        "cpp": ("""
#include <iomanip>
#include <iostream>

int main() {
    double r{};
    if (!(std::cin >> r)) return 1;

    const int e = static_cast<int>(r);   // trunca hacia cero

    std::cout << "entero=" << e
              << " real=" << std::fixed << std::setprecision(2) << r << '\\n';
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** `static_cast<int>(r)` es deliberadamente **verboso**, y esa
verbosidad es la característica. En C bastaba `(int)r`, un molde que servía para todo: convertir
tipos numéricos, quitar `const`, reinterpretar punteros. C++ lo partió en cuatro operadores con
nombres largos y significados distintos:

| Operador | Para qué |
|---|---|
| `static_cast<T>` | Conversiones con sentido comprobadas al compilar |
| `dynamic_cast<T>` | Bajar en una jerarquía de clases, con comprobación en ejecución |
| `const_cast<T>` | Quitar o poner `const` — casi siempre una señal de alarma |
| `reinterpret_cast<T>` | Reinterpretar los bits; peligroso y a veces indefinido |

El motivo del nombre largo es explícito: **son fáciles de buscar**. `grep reinterpret_cast` encuentra
todos los sitios sospechosos de una base de código; `grep '(int)'` no encuentra nada útil. Es diseño
de lenguaje pensando en la revisión de código.

Y esta clase toca además la parte más oscura de C++: las **conversiones implícitas** que sí quedan.
`int` a `double` es segura; `double` a `int` trunca y **avisa solo con `-Wconversion`**; `int` a
`unsigned` convierte un negativo en un número enorme; y una comparación entre `signed` y `unsigned`
convierte el con signo, con el resultado clásico de que `-1 < 1u` es **falso**. Compilar con
`-Wall -Wextra -Wconversion` es lo que convierte esas trampas en avisos.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi CONVERS;
  r packed(15:2) const;
end-pi;

dcl-s e      int(10);
dcl-s salida char(60);

e = %int(r);          // %int trunca; %inth redondea (half adjust)

salida = 'entero=' + %char(e) + ' real=' + %char(r);
dsply salida;

*inlr = *on;
return;
""", """
**Lo que esta clase enseña en RPG.** RPG tiene la distinción **en el nombre de la función**, con una
convención que recorre todo el lenguaje: la **`h` final significa *half adjust***, es decir,
redondeo.

| Función | Qué hace |
|---|---|
| `%int(x)` | Convierte a entero **truncando** |
| `%inth(x)` | Convierte a entero **redondeando** |
| `%dec(x : d : p)` | Convierte a decimal truncando |
| `%dech(x : d : p)` | Convierte a decimal redondeando |

Esa pareja sistemática es más honesta que tener una sola función y una nota en el manual. Y en un
lenguaje de facturación, la diferencia entre truncar y redondear un importe **es una decisión de
negocio**, así que exigir que se elija en cada llamada es lo correcto.

Hay además una trampa propia de RPG que ya apareció en la clase 044 y que aquí es central: **el
operador `/` redondea**, no trunca, según los decimales del destino. `e = 7 / 2` con `e` entero da
**4**, no 3. Quien llega de C o de Java escribe esa línea esperando 3 y obtiene otra cosa, sin ningún
aviso.

La forma correcta de la división entera es `%div(7 : 2)`, que da 3, con `%rem(7 : 2)` para el resto.
"""),
        "pli": ("""
 conversion: procedure options(main);

    declare r    fixed decimal(15,2);
    declare e    fixed binary(31);
    declare pres picture 'ZZZZZZZZZ9V.99';

    get list (r);
    e = trunc(r);

    pres = r;
    put skip list ('entero=' || trim(char(e)) || ' real=' || trim(pres));

 end conversion;
""", """
**Lo que esta clase enseña en PL/I.** PL/I es, con diferencia, **el lenguaje con más conversiones
implícitas de esta página**, y esta clase es donde eso se vuelve un problema. Casi cualquier
asignación entre tipos distintos compila y hace algo:

```pli
declare n fixed decimal(5,2);
declare c character(10) varying;

n = '123.45';    /* texto a decimal: funciona */
c = n;           /* decimal a texto: funciona, con formato implícito */
n = '12abc';     /* ERROR EN EJECUCIÓN: condición CONVERSION */
```

Esa última línea es la clave: cuando la conversión implícita **no puede** hacerse, PL/I no devuelve
un valor degradado como M ni avisa como Perl: levanta la condición **`CONVERSION`**, que se puede
capturar con el mecanismo `ON` de la clase 041.

```pli
on conversion begin;
   put skip list ('dato no numérico: ' || onsource());
   onsource() = '0';       /* CORRIGE el dato y REANUDA */
end;
```

`onsource()` como pseudovariable permite **reemplazar el dato que falló y continuar la operación**.
No es capturar una excepción y abortar: es reparar y seguir. Es el mismo poder que los reinicios de
[Common Lisp](../../../atlas/common-lisp.md), y una capacidad que el `try/catch` moderno perdió por
el camino.

Y `trunc` frente a `round`: PL/I tiene las dos, y además `divide(a, b, p, q)` para controlar la
precisión exacta del resultado de una división.
"""),
        "mumps": ("""
CONVER ; Conversion -- clase 049
 read r
 set e = r\\1
 write "entero=", e, " real=", $justify(r, 0, 2), !
 quit
""", """
**Lo que esta clase enseña en M.** `r\\1` es la conversión a entero, y merece explicación: `\\` es la
**división entera** de M, así que dividir por uno y quedarse con la parte entera **es** truncar. No
hay función `int` porque no hace falta: el operador ya trunca.

Es un ejemplo perfecto de la economía del lenguaje —una operación que en otros sitios necesita una
función aquí es un efecto colateral de un operador— y también de por qué M es difícil de leer sin
conocerlo: `r\\1` no dice "truncar" en ninguna parte.

Y esta clase es donde el tipado débil de M muestra su lado más peligroso, que ya se apuntó en la 043:
**la conversión de texto a número nunca falla**.

```mumps
write "12abc" + 0     ; 12   -- lee el prefijo
write "abc" + 0       ; 0    -- sin error, sin aviso
write "1.5e3" + 0     ; 1500 -- entiende notación científica
write "" + 0          ; 0
```

Perl hace lo mismo pero **avisa** con `use warnings`. PL/I hace lo mismo pero **levanta una
condición** capturable. M no hace ninguna de las dos cosas: devuelve 0 y sigue. En un sistema clínico
de 1966 eso se consideró preferible a detener el proceso, y sigue siendo el comportamiento hoy.

La consecuencia práctica es que **la validación en M es responsabilidad del programador, siempre**.
De ahí que VistA tenga FileMan, un diccionario de datos que valida cada campo antes de escribirlo: el
esquema y la validación que el lenguaje no da, construidos encima.
"""),
        "smalltalk": ("""
| r e |

r := stdin nextLine trimBoth asNumber.
e := r truncated.

Transcript
    show: 'entero=', e printString;
    show: ' real=', (r asFloat printShowingDecimalPlaces: 2);
    cr.
""", """
**Lo que esta clase enseña en Smalltalk.** La conversión es **un mensaje enviado al objeto**, y por
eso el catálogo está en la clase `Number` y se puede leer:

```smalltalk
3.7 truncated     "3   -- hacia cero"
3.7 rounded       "4"
3.7 floor         "3"
-3.7 floor        "-4"
3.7 ceiling       "4"
3.7 asInteger     "3   -- sinónimo de truncated"
'3.7' asNumber    "3.7 -- del texto al número"
3.7 printString   "'3.7' -- del número al texto"
```

Fíjate en la dirección de los mensajes: `asNumber` se envía a la **cadena** y `printString` al
**número**. Cada objeto sabe convertirse a lo demás, en lugar de existir una función externa que los
conozca a los dos. Añadir un tipo nuevo al sistema no obliga a modificar ninguna función de
conversión: basta con que implemente los mensajes.

Y hay una consecuencia de esta clase que solo se ve aquí y en Lisp: como los enteros no tienen
límite, `truncated` **nunca desborda**. `1e100 truncated` devuelve el entero de 101 dígitos completo.
En C++ eso sería comportamiento indefinido; en Java daría `Long.MAX_VALUE`; aquí simplemente
funciona.

`asNumber` sobre texto no numérico devuelve `nil` en lugar de cero, lo que obliga a comprobarlo —la
postura contraria a la de M— y enlaza con la clase 053.
"""),
    },
)

# ---------------------------------------------------------------------------
# 050 — Tipado estático vs. dinámico
# ---------------------------------------------------------------------------
SPECS["050"] = dict(
    gancho="""
Sumar un entero y un real. La operación más inocente del programa, y la que obliga a cada lenguaje a
declarar su postura: **¿cuándo se decide que esto es una suma de reales?** ¿Al compilar, mirando las
declaraciones? ¿Al ejecutar, mirando los valores? ¿O no se decide nunca, porque no hay tipos que
mirar?
""",
    porque="""
Aquí el concepto es **el momento en que se resuelve el tipo**, y estos lenguajes cubren el espectro
entero con posturas más nítidas que el núcleo. **Ada** representa el extremo estático absoluto: la
suma **no compila** sin una conversión escrita, aunque sea evidente lo que quieres. **COBOL** decide
al compilar, pero la conversión la esconde en el `MOVE`. **Fortran, Pascal y C++** promocionan solos
en la dirección segura. Y **Tcl, M, Perl y Smalltalk** no deciden nada hasta que la operación se
ejecuta.

Lo interesante es que estático y dinámico **no es una escala de rigor**: Smalltalk es dinámico y
fuertemente tipado, Tcl es dinámico y débil, y C++ es estático y permite conversiones que pierden
datos. Son dos ejes distintos, y esta clase junto con la 051 los separa.
""",
    cierre="""
La pregunta que deja esta página no es "¿estático o dinámico?" sino **"¿cuánto sabe el compilador
antes de ejecutar, y qué hace con lo que no sabe?"**. Ada lo sabe todo y se niega a suponer. C++ lo
sabe casi todo y supone en silencio. Smalltalk no sabe nada hasta que llega el objeto, pero cuando
llega comprueba de verdad. Y Tcl y M no comprueban nunca. Las cuatro posturas tienen sistemas en
producción desde hace décadas, así que ninguna es simplemente incorrecta.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. MIXTO.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  TXT-A   PIC X(20).
01  TXT-B   PIC X(20).
01  A       PIC S9(9)    COMP-3.
01  B       PIC S9(9)V99 COMP-3.
01  S       PIC S9(9)V99 COMP-3.
01  ED-S    PIC -(9)9.99.

PROCEDURE DIVISION.
    ACCEPT LINEA
    UNSTRING LINEA DELIMITED BY ALL SPACES INTO TXT-A TXT-B
    MOVE FUNCTION NUMVAL(TXT-A) TO A
    MOVE FUNCTION NUMVAL(TXT-B) TO B

    COMPUTE S = A + B

    MOVE S TO ED-S
    DISPLAY "suma=" FUNCTION TRIM(ED-S)
    STOP RUN.
""", """
**Lo que esta clase enseña en COBOL.** COBOL es **estático hasta el extremo**: el tipo, el número de
dígitos, la posición de la coma decimal y la representación física de cada dato están decididos
**antes de compilar**, y no pueden cambiar. Una variable no puede contener a veces un número y a
veces un texto; ni siquiera puede contener un número con más dígitos de los declarados.

Pero —y esta es la parte interesante— **la conversión entre tipos numéricos es totalmente
implícita**. `COMPUTE S = A + B` con `A` sin decimales y `B` con dos funciona sin decir nada: el
compilador alinea las comas decimales, hace la suma y ajusta al destino. COBOL sabe exactamente qué
está pasando porque todo está declarado, así que no necesita preguntar.

Eso lo sitúa en una casilla que casi ningún lenguaje moderno ocupa: **estático, fuerte en cuanto a la
forma del dato, y permisivo en la aritmética**. La comprobación no está en prohibir la mezcla, está
en que la mezcla se resuelve con reglas deterministas y documentadas.

El precio es el de la clase 049: cuando el destino no da de sí, el resultado se trunca en silencio.
COBOL confía en que declaraste bien.
"""),
        "fortran": ("""
program mixto
   implicit none
   integer :: a
   real(kind=8) :: b, s
   character(len=32) :: buf

   read(*, *) a, b
   s = a + b            ! promoción implícita: a se convierte a real

   write(buf, '(F20.2)') s
   write(*, '(A,A)') 'suma=', trim(adjustl(buf))
end program mixto
""", """
**Lo que esta clase enseña en Fortran.** Fortran es estático y **promociona en la dirección segura**:
en `a + b` con `a` entero y `b` real, el entero se convierte a real y la suma es real. La regla se
llama *conversión aritmética* y está en el estándar; no hay ambigüedad.

Lo que hay que vigilar es que **la promoción ocurre en la expresión, no en la asignación**, y esa
distinción es la fuente del error más clásico del lenguaje:

```fortran
real(kind=8) :: x
x = 1 / 2          ! x vale 0.0  -- la división es ENTERA, y luego se promociona
x = 1.0d0 / 2      ! x vale 0.5  -- ahora la división ya es real
```

El destino no influye en cómo se evalúa la expresión. Es el mismo comportamiento de C, Java y Go, y
el mismo error.

Y `implicit none` vuelve a ser decisivo en esta clase: **sin él, Fortran es estático pero con tipos
adivinados**. Una variable sin declarar recibe tipo según su inicial, así que `total = a + b` podría
estar sumando en entero sin que aparezca ninguna declaración que lo delate. Es tipado estático con la
mitad de las garantías, y es la razón de que esa línea sea obligatoria en cualquier Fortran serio.
"""),
        "ada": ("""
with Ada.Text_IO;            use Ada.Text_IO;
with Ada.Integer_Text_IO;    use Ada.Integer_Text_IO;
with Ada.Long_Float_Text_IO; use Ada.Long_Float_Text_IO;

procedure Mixto is
   A    : Integer;
   B, S : Long_Float;
begin
   Get (A);
   Get (B);

   --  S := A + B;  NO COMPILA. La conversión es obligatoria y visible.
   S := Long_Float (A) + B;

   Put ("suma="); Put (S, Fore => 1, Aft => 2, Exp => 0);
   New_Line;
end Mixto;
""", """
**Lo que esta clase enseña en Ada.** La línea comentada es el contenido entero de la clase: **`A + B`
no compila**. Ada no promociona nada, nunca, entre tipos numéricos distintos. Ni siquiera en la
dirección segura que Fortran, Pascal, C++ y Java permiten sin decir nada.

Y va más lejos de lo que parece, porque en Ada **dos tipos con la misma representación siguen siendo
distintos**:

```ada
type Metros is new Float;
type Pies   is new Float;

M : Metros := 100.0;
P : Pies   := 50.0;
--  X := M + P;          NO COMPILA: son tipos distintos
X : Metros := M + Metros (Float (P) * 0.3048);   --  la conversión declara la intención
```

Eso es **tipado nominal fuerte**: el nombre del tipo importa, no solo su forma. Es la característica
que habría evitado la pérdida de la sonda Mars Climate Orbiter, y la razón de que Ada siga en
aviónica.

El coste es real y conviene reconocerlo: el código es más largo y hay conversiones por todas partes.
La apuesta de Ada es que **escribir la conversión obliga a pensarla**, y que en un sistema donde un
fallo cuesta vidas, ese coste sale barato. En un guion de cinco líneas, no.
"""),
        "pascal": ("""
program Mixto;
{$MODE OBJFPC}{$H+}

var
  A: Integer;
  B, S: Double;

begin
  Read(A, B);
  S := A + B;          { Pascal promociona en la dirección segura }

  WriteLn('suma=', S:0:2);
end.
""", """
**Lo que esta clase enseña en Pascal.** Pascal ocupa la casilla intermedia con una regla explícita y
fácil de recordar: **promociona hacia donde no se pierde información, y prohíbe lo demás**.

```pascal
S := A + B;      { Integer + Double -> Double.  Correcto. }
A := S;          { NO COMPILA: hay que escribir Trunc(S) o Round(S) }
```

Es la misma política que Fortran, con la diferencia de que Pascal la aplica también a los tipos
definidos por el usuario. Un subrango `1..10` se asigna a un `Integer` sin problema, pero al revés
requiere comprobación de rango en ejecución con `{$R+}`.

Y esta clase toca un punto donde Pascal fue **más estricto que casi todos**: los **tipos
incompatibles por nombre**. `type Metros = Integer` crea un alias compatible, pero
`type Metros = type Integer` —con la palabra `type` repetida— crea un tipo **distinto** que no se
mezcla, exactamente como el `new` de Ada. Delphi lo usa mucho para que el compilador distinga
identificadores que son todos enteros pero significan cosas distintas.

Es una capacidad que muy pocos lenguajes tienen y que hoy se pide constantemente con el nombre de
*newtype* o *branded types*: TypeScript la simula con trucos, Rust la tiene con `struct Metros(f64)`,
y Pascal la tenía en 1970.
"""),
        "lisp": ("""
(setf *read-default-float-format* 'double-float)

(let* ((a (read))
       (b (read))
       (s (+ a b)))
  (format t "suma=~,2F~%" s))
""", """
**Lo que esta clase enseña en Common Lisp.** Lisp es **dinámico y fuertemente tipado**, y esta
combinación es la que más cuesta ver desde fuera. Dinámico: el tipo pertenece al **valor**, y `a`
puede contener hoy un entero y mañana una lista. Fuerte: `(+ 1 "dos")` **no** convierte nada, levanta
un error de tipo en ejecución.

Y la aritmética aplica la **regla de contagio** de la torre numérica que apareció en la clase 043: al
mezclar un entero exacto con un real inexacto, el resultado es inexacto. `(+ 2 3.5d0)` da `5.5d0`, y
`(+ 1/2 1/3)` da `5/6` porque los dos son exactos.

Lo que Lisp añade y que casi ningún dinámico tiene es la posibilidad de **declarar tipos cuando
interesa**, sin dejar de ser dinámico:

```lisp
(defun suma (a b)
  (declare (type double-float a b)
           (optimize (speed 3) (safety 0)))
  (+ a b))
```

Con esa declaración, SBCL genera código nativo tan rápido como el de C, sin comprobaciones. Sin ella,
la misma función acepta cualquier número. Es **tipado gradual** —lo que hoy hacen TypeScript, Python
con anotaciones o Sorbet en Ruby— disponible en el estándar de 1994. Y SBCL va más lejos: **infiere y
avisa en tiempo de compilación** de incompatibilidades que puede demostrar, aunque no hayas declarado
nada.
"""),
        "tcl": ("""
gets stdin linea
lassign [split [string trim $linea]] a b

set s [expr {$a + $b}]

puts "suma=[format %.2f $s]"
""", """
**Lo que esta clase enseña en Tcl.** No hay tipos, así que no hay nada que decidir al compilar. La
pregunta "¿esto es una suma de enteros o de reales?" la responde **`expr`, en el momento de
ejecutar**, mirando el aspecto del texto:

```tcl
expr {2 + 3}        ;# 5      -- los dos parecen enteros
expr {2 + 3.5}      ;# 5.5    -- uno parece real, promociona
expr {"2" + "3"}    ;# 5      -- las comillas no cambian nada
expr {2 + "hola"}   ;# ERROR  -- Tcl SÍ falla aquí
```

Esa última línea importa: Tcl es de tipado débil, pero **no es JavaScript**. No inventa un resultado;
lanza un error. La debilidad de Tcl consiste en aceptar que cualquier cadena *que parezca un número*
lo sea, no en convertir cualquier cosa a cualquier cosa.

Y hay un detalle de implementación que explica por qué esto no es lento: Tcl guarda junto a la cadena
una **representación interna** con su tipo real —entero, real, lista, comando compilado—, y solo la
regenera si el valor cambia. Un bucle que sume un millón de veces no reanaliza el texto un millón de
veces. La semántica es "todo es cadena"; la implementación es otra cosa.

Ese truco —conocido como *dual-ported object*— es de 1997 y es el antepasado directo de las clases
ocultas de los motores de JavaScript modernos.
"""),
        "perl": ("""
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;
my ($a_val, $b_val) = split ' ', $linea;

printf "suma=%.2f\\n", $a_val + $b_val;
""", """
**Lo que esta clase enseña en Perl.** Perl es dinámico y **débil**, y aquí ni siquiera hay una
decisión que tomar: `$a_val` y `$b_val` contienen texto leído de la entrada, y el operador `+` los
lee como números porque eso es lo que hace `+`. No hay promoción de entero a real porque **no hay
entero ni real**: hay un escalar que sabe comportarse como ambos.

Internamente, un escalar de Perl (una estructura `SV`) tiene ranuras para el valor entero (`IV`), el
real (`NV`) y la cadena (`PV`), y va rellenando la que haga falta. Por eso `$x = "3.5"; $y = $x + 0;`
no "convierte": simplemente materializa la ranura numérica y la conserva para la próxima vez.

La consecuencia práctica es que **el tipo lo elige el operador, no el dato**, y de ahí que Perl
necesite dos juegos de operadores —tema de la clase 051—. Y también que la única forma de comprobar
algo sea preguntar explícitamente:

```perl
use Scalar::Util qw(looks_like_number);
die "no es un número" unless looks_like_number($b_val);
```

Nota sobre el estilo: las variables se llaman `$a_val` y `$b_val` y no `$a` y `$b` a propósito.
`$a` y `$b` son **variables especiales** que Perl usa internamente en `sort`, y aunque `use strict`
las deja pasar, usarlas para otra cosa es una de esas trampas que solo muerden mucho después.
"""),
        "cpp": ("""
#include <iomanip>
#include <iostream>

int main() {
    int a{};
    double b{};
    if (!(std::cin >> a >> b)) return 1;

    const double s = a + b;      // promoción aritmética implícita

    std::cout << "suma=" << std::fixed << std::setprecision(2) << s << '\\n';
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** C++ es estático y con **conversiones aritméticas implícitas**
definidas por un conjunto de reglas —las *usual arithmetic conversions*— que casi nadie ha leído
entero y que producen sorpresas genuinas:

```cpp
int a = -1;
unsigned int b = 1;
if (a < b) { }          // FALSO: a se convierte a unsigned y vale 4294967295

short x = 30000, y = 30000;
int z = x + y;          // ambos se promocionan a int: 60000, correcto
short w = x + y;        // desbordamiento al volver a short
```

La regla de fondo es que los operandos se promocionan al tipo "más grande" de la expresión, y que
`unsigned` gana a `signed` del mismo rango. Ese último punto es el origen de una familia entera de
errores, y la razón de que las guías modernas recomienden no usar `unsigned` para cantidades que solo
son "no negativas".

Lo que C++ ofrece a cambio es que **todas esas conversiones se pueden hacer visibles**: compilar con
`-Wconversion -Wsign-conversion` convierte cada promoción con pérdida en un aviso. Y desde C++11, la
**inicialización con llaves** las prohíbe donde importa:

```cpp
int  n1 = 3.7;    // compila, n1 vale 3
int  n2 {3.7};    // NO COMPILA: narrowing conversion
```

Es la misma política de Ada, disponible como opción en vez de como norma.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi MIXTO;
  a int(10)      const;
  b packed(15:2) const;
end-pi;

dcl-s s      packed(15:2);
dcl-s salida char(40);

s = a + b;          // entero + decimal: RPG alinea y suma

salida = 'suma=' + %char(s);
dsply salida;

*inlr = *on;
return;
""", """
**Lo que esta clase enseña en RPG.** RPG es estático y, como COBOL, **resuelve la mezcla numérica sin
protestar**: alinea las comas decimales y ajusta al destino. El compilador lo puede hacer porque
conoce exactamente los dígitos y decimales de cada operando.

Lo que RPG añade y que conviene conocer es que **el resultado intermedio también tiene precisión
declarada**, y ahí está el riesgo. Al multiplicar dos `packed(15:2)`, el resultado natural tendría 30
dígitos con 4 decimales, que excede el máximo del tipo (63 dígitos en versiones recientes, 31 en las
antiguas). Si el destino no da de sí, se trunca.

Por eso existe la palabra clave **`eval-corr`** para estructuras y, sobre todo, la posibilidad de
forzar la precisión intermedia:

```rpgle
s = %dech(a * b : 15 : 2);   // decide TÚ los dígitos y el redondeo
```

Y hay una diferencia con COBOL que salta a la vista en el tipado: RPG **sí** distingue `int` de
`packed`, es decir, binario de decimal, mientras que COBOL lo trata como una cláusula de
almacenamiento (`COMP` frente a `COMP-3`) sobre el mismo `PIC`. Dos formas de decir lo mismo, con
consecuencias distintas al leer el código: en RPG el tipo lo dices, en COBOL lo dice la forma.
"""),
        "pli": ("""
 mixto: procedure options(main);

    declare a    fixed binary(31);
    declare b    fixed decimal(15,2);
    declare s    fixed decimal(15,2);
    declare pres picture 'ZZZZZZZZZ9V.99';

    get list (a, b);

    s = a + b;      /* binaria + decimal: PL/I convierte segun sus reglas */

    pres = s;
    put skip list ('suma=' || trim(pres));

 end mixto;
""", """
**Lo que esta clase enseña en PL/I.** PL/I es estático y **el campeón absoluto de la conversión
implícita**. Aquí se suman un `fixed binary` y un `fixed decimal` —bases distintas, no solo tipos
distintos— y el lenguaje lo resuelve sin decir nada: convierte el binario a decimal según una regla
del estándar y opera.

Esa regla existe, está documentada y ocupa varias páginas. Define la precisión del resultado
intermedio a partir de la de los operandos, para cada combinación de base y escala. Es **determinista
y prácticamente imposible de recordar**, y ese es exactamente el problema que Dijkstra señalaba: un
lenguaje puede ser completamente especificado y aun así inmanejable, si nadie puede predecir su
comportamiento sin consultar el manual.

La lección de diseño que deja PL/I para esta clase es la más valiosa del programa: **hay una
diferencia entre "el lenguaje sabe qué hacer" y "el programador sabe qué va a pasar"**. COBOL acierta
porque sus reglas son pocas; Ada acierta porque no tiene ninguna; PL/I falla porque tiene demasiadas.

Cuando en un lenguaje moderno alguien discute si añadir una conversión implícita más, este es el
precedente que hay que citar.
"""),
        "mumps": ("""
MIXTO ; Estatico vs dinamico -- clase 050
 read linea
 set a = $piece(linea, " ", 1)
 set b = $piece(linea, " ", 2)
 set s = a + b
 write "suma=", $justify(s, 0, 2), !
 quit
""", """
**Lo que esta clase enseña en M.** M es el caso más puro de tipado dinámico y débil: **no hay tipos
que resolver ni al compilar ni al ejecutar**. `a` y `b` son cadenas, `+` las lee como números, y el
resultado es una cadena que representa un número.

Y aquí conviene mirar algo que no se ve en ningún otro lenguaje de esta página: **la ausencia de tipos
llega también a la base de datos**. Un *global* de M no tiene esquema, así que el mismo nodo puede
contener hoy un número y mañana un texto, y las claves del árbol se ordenan con una regla mixta —
primero la cadena vacía, luego los números en orden numérico, luego el resto en orden de colación—.

Esa regla de ordenación *numérica antes que alfabética* es una decisión de diseño con cincuenta años
que hoy resulta familiar: es lo que hacen los índices de una base de datos documental. M era NoSQL
sin esquema en 1966, con las mismas ventajas —flexibilidad ante datos irregulares— y los mismos
inconvenientes —ninguna garantía, validación siempre por cuenta del programador—.

Por eso VistA construyó **FileMan** encima: un diccionario que define, para cada campo, su tipo, su
rango, su obligatoriedad y sus reglas. Es literalmente el sistema de tipos que el lenguaje no tiene,
implementado como datos dentro de la propia base de datos.
"""),
        "smalltalk": ("""
| partes a b |

partes := stdin nextLine substrings collect: [ :cada | cada asNumber ].
a := partes first.
b := partes second.

Transcript
    show: 'suma=', ((a + b) asFloat printShowingDecimalPlaces: 2);
    cr.
""", """
**Lo que esta clase enseña en Smalltalk.** Smalltalk es **dinámico y fuertemente tipado**, y es el
mejor ejemplo de que esos dos ejes son independientes. No hay declaraciones de tipo en ninguna parte,
pero `3 + 'hola'` **no** produce un resultado raro: produce un error, porque `SmallInteger` no sabe
sumar una cadena.

Y la forma en que ocurre la suma mixta es lo específico de esta clase. `a + b` con `a` entero y `b`
real no es una regla del lenguaje: es **doble despacho**. `SmallInteger>>+` recibe un argumento que no
sabe manejar y hace lo único sensato — le pregunta al argumento:

```smalltalk
Number >> + aNumber
    ^ self generality < aNumber generality
        ifTrue:  [ (aNumber coerce: self) + aNumber ]
        ifFalse: [ self + (self coerce: aNumber) ]
```

Cada clase numérica declara su **generalidad** —entero < fracción < real < complejo— y la de menor
generalidad se convierte a la de mayor. La torre numérica de Lisp existe aquí también, pero
implementada **como código de biblioteca que puedes leer y extender**, no como una regla del
compilador.

La consecuencia es notable: si defines una clase `Dinero` y le das `generality` y `coerce:`, se
integra en la aritmética existente y `3 + unDinero` funciona. Añadir un tipo numérico al lenguaje no
requiere tocar el lenguaje.
"""),
    },
)

# ---------------------------------------------------------------------------
# 051 — Tipado fuerte vs. débil
# ---------------------------------------------------------------------------
SPECS["051"] = dict(
    gancho="""
El mismo valor, dos operaciones: **sumarlo consigo mismo** y **pegarlo consigo mismo**. Con `5` da
`10` y `55`. Es el experimento mínimo del tipado débil, y separa a los lenguajes en dos grupos
tajantes: los que necesitan **dos operadores distintos** porque el dato no dice qué es, y los que
necesitan **una conversión explícita** porque el dato sí lo dice.
""",
    porque="""
Aquí el concepto es **la fuerza del tipado**, que es cosa distinta de si es estático o dinámico
—tema de la clase 050—. Y estos lenguajes lo enseñan porque contienen los dos casos extremos.

En **M** y en **Perl**, el mismo valor se suma con `+` y se concatena con `_` o con `.`: **el
operador decide el tipo**, y por eso hacen falta dos. En **Tcl** ni siquiera hace falta operador de
concatenación, porque pegar dos cosas es escribirlas juntas. En el otro extremo, **Ada** y **C++**
exigen convertir a texto con una llamada visible antes de poder concatenar.

Y entre medias está COBOL, que necesita **un verbo entero** —`STRING`— para hacer lo que en Perl es
un punto.
""",
    cierre="""
La regla transferible es simple y vale para cualquier lenguaje que aprendas: **cuenta los operadores
de comparación**. Si el lenguaje tiene dos juegos —`==` y `eq` en Perl, `=` y `==` en M según el
contexto, `==` y `===` en JavaScript y PHP— es porque el dato no lleva su tipo encima y hay que
decírselo al operador. Si tiene uno solo, el tipo está en el valor. Esa cuenta te dice más sobre un
lenguaje en diez segundos que su documentación en una hora.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. TIPADO.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  LIMPIO  PIC X(20).
01  LARGO   PIC 9(2) COMP-3.
01  N       PIC S9(9) COMP-3.
01  SUMA    PIC S9(9) COMP-3.
01  TEXTO   PIC X(40).
01  ED-S    PIC -(9)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    MOVE FUNCTION TRIM(LINEA) TO LIMPIO
    COMPUTE LARGO = FUNCTION LENGTH(FUNCTION TRIM(LIMPIO))
    MOVE FUNCTION NUMVAL(LIMPIO) TO N

    COMPUTE SUMA = N + N

    MOVE SPACES TO TEXTO
    STRING LIMPIO(1:LARGO) DELIMITED BY SIZE
           LIMPIO(1:LARGO) DELIMITED BY SIZE
      INTO TEXTO
    END-STRING

    MOVE SUMA TO ED-S
    DISPLAY "suma=" FUNCTION TRIM(ED-S) " texto=" FUNCTION TRIM(TEXTO)
    STOP RUN.
""", """
**Lo que esta clase enseña en COBOL.** COBOL es **fuertemente tipado en la forma del dato**: `N` es
numérico y `LIMPIO` es alfanumérico, y no se mezclan. Para sumar hace falta `COMPUTE`; para
concatenar hace falta **`STRING`**, que es un **verbo completo**, no un operador.

Que la concatenación necesite una sentencia entera —con `DELIMITED BY`, `INTO` y `END-STRING`— dice
mucho sobre las prioridades del lenguaje: manipular texto era una tarea secundaria frente a mover
registros de longitud fija. En Perl es un punto; aquí son cinco líneas.

Y `LIMPIO(1:LARGO)` es la **modificación de referencia** que ya apareció en la clase 044, aquí
usada para no arrastrar los espacios de relleno del campo. Sin ella, `STRING` copiaría los veinte
caracteres, blancos incluidos, y el resultado sería `"5                   5"`.

Pero la comprobación tiene un agujero notable, y conviene conocerlo: **COBOL no comprueba que un
campo alfanumérico contenga de verdad un número**. `MOVE "hola" TO N` con `N` numérico compila, y el
resultado es basura interpretada como dígitos. Por eso existe la comprobación explícita, que en
código de producción aparece constantemente:

```cobol
IF LIMPIO IS NUMERIC
    MOVE FUNCTION NUMVAL(LIMPIO) TO N
END-IF
```
"""),
        "fortran": ("""
program tipado
   implicit none
   integer :: n
   character(len=32) :: txt

   read(*, *) n
   write(txt, '(I0)') n           ! número -> texto: hay que ESCRIBIRLO

   write(*, '(A,I0,A,A)') 'suma=', n + n, ' texto=', trim(txt) // trim(txt)
end program tipado
""", """
**Lo que esta clase enseña en Fortran.** Fortran es **fuertemente tipado**: `n` es un `integer` y
nunca será un texto. Para obtener su representación textual hay que hacer una **escritura interna**
—`write(txt, formato) n`—, que es la conversión número a texto del lenguaje.

Esa construcción merece atención porque es peculiar y muy útil: `write` a una **variable de carácter**
en lugar de a un fichero. Todo el sistema de formatos —los descriptores `I`, `F`, `E`, `Z` de la clase
044— queda disponible para construir cadenas. Y existe la operación inversa, la **lectura interna**:

```fortran
character(len=20) :: entrada
integer :: valor
entrada = '  42  '
read(entrada, *) valor      ! del texto al número, con el mismo mecanismo
```

Es el `parse` de Fortran, y no hay otro. Ni `atoi`, ni `StrToInt`, ni `asNumber`: se lee de una
cadena como si fuera un fichero.

Y `//` es la concatenación, con la trampa de la clase 048: sobre campos de longitud fija concatena
**incluidos los blancos de relleno**, de ahí `trim(txt) // trim(txt)`. Es la asimetría característica
de un lenguaje donde las cadenas son arrays de tamaño fijo.
"""),
        "ada": ("""
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;
with Ada.Strings;
with Ada.Strings.Fixed;

procedure Tipado is
   N : Integer;
begin
   Get (N);

   declare
      --  'Image da " 5" con un espacio delante para el signo. Hay que quitarlo.
      Txt : constant String :=
        Ada.Strings.Fixed.Trim (Integer'Image (N), Ada.Strings.Both);
   begin
      Put ("suma="); Put (N + N, Width => 1);
      Put (" texto=" & Txt & Txt);
      New_Line;
   end;
end Tipado;
""", """
**Lo que esta clase enseña en Ada.** Ada tiene el tipado **más fuerte de toda la página**, y aquí se
ve en dos sitios.

El primero: la conversión de número a texto es el atributo **`'Image`**, disponible en cualquier
tipo escalar —`Integer'Image`, `Float'Image`, `Boolean'Image`, y también en los enumerados que
definas tú—. Su inversa es `'Value`: `Integer'Value ("42")` devuelve 42 y levanta `Constraint_Error`
si el texto no es válido. Un par de atributos uniforme para todos los tipos, en lugar de una función
distinta por cada uno.

El segundo, y es la trampa más conocida del lenguaje: **`Integer'Image (5)` devuelve `" 5"`, con un
espacio delante**. El estándar reserva esa posición para el signo, de modo que los negativos den
`"-5"` con la misma anchura. Es coherente y sorprende a todo el mundo la primera vez, y por eso
prácticamente todo el código Ada del mundo envuelve `'Image` en un `Trim`.

Y el operador `&` es la concatenación, que en Ada no es un caso especial: está definido para **todos
los tipos array**, porque `String` es un array. Concatenar dos vectores de enteros usa el mismo `&`.
Otra vez la misma idea — no hay operaciones de cadena, hay operaciones de array.
"""),
        "pascal": ("""
program Tipado;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  N: Integer;
  Txt: string;

begin
  Read(N);
  Txt := IntToStr(N);          { conversión explícita }

  WriteLn('suma=', IntToStr(N + N), ' texto=', Txt + Txt);
end.
""", """
**Lo que esta clase enseña en Pascal.** Pascal es fuertemente tipado y **reutiliza `+` para
concatenar**, que es una decisión discutible y muy extendida: `2 + 2` es 4 y `'2' + '2'` es `'22'`.
Funciona porque el tipado es fuerte y estático, así que el compilador sabe cuál de las dos
operaciones aplica y **no hay ambigüedad posible**.

Compara con JavaScript, donde `+` también hace las dos cosas pero el tipado es débil y dinámico:
`2 + '2'` da `'22'` y `2 - '2'` da `0`. La misma sobrecarga del operador es segura en Pascal y
peligrosa en JavaScript, y la diferencia no está en el operador: está en si el lenguaje puede saber
qué tiene delante.

La conversión es explícita y con una familia de funciones que conviene conocer entera, porque el
manejo de errores las distingue:

```pascal
IntToStr(42)                  { entero -> texto }
StrToInt('42')                { texto -> entero; EXCEPCIÓN si no vale }
StrToIntDef('x', 0)           { devuelve 0 si no vale }
TryStrToInt('x', N)           { devuelve False y no toca N }
```

Las dos últimas son las que se usan con datos que vienen de fuera. Elegir `StrToInt` para procesar un
fichero de entrada es garantizar una excepción el día que llegue una línea mal formada.
"""),
        "lisp": ("""
(let* ((n (read))
       (txt (princ-to-string n)))
  (format t "suma=~D texto=~A~%" (+ n n) (concatenate 'string txt txt)))
""", """
**Lo que esta clase enseña en Common Lisp.** Lisp es **fuertemente tipado y dinámico**: `(+ 5 "5")`
no concatena ni convierte, señala un error de tipo. La conversión hay que pedirla, y hay varias
formas según qué representación quieras:

```lisp
(princ-to-string 42)     ; "42"    -- como lo imprimiría PRINC (para humanos)
(prin1-to-string 42)     ; "42"    -- como lo leería READ (con comillas si es cadena)
(format nil "~D" 42)     ; "42"    -- con todo el control de FORMAT
(write-to-string 42 :base 16)  ; "2A"
(parse-integer "42")     ; 42      -- la inversa, estricta
(read-from-string "42")  ; 42      -- la inversa, usando el LECTOR del lenguaje
```

La distinción entre `princ` y `prin1` es propia de Lisp y vale la pena: `princ` produce la forma
**legible por humanos** y `prin1` la forma **legible por la máquina**, es decir, la que `read`
volvería a convertir en el mismo objeto. Para la cadena `"hola"`, `princ` da `hola` y `prin1` da
`"hola"` con las comillas. Es la misma distinción que `__str__` y `__repr__` en Python, que viene
directamente de aquí.

Y `concatenate` recibe **el tipo del resultado como primer argumento** —`'string`, `'list`,
`'vector`—, porque es la función genérica de secuencias de la clase 048. No hay concatenación de
cadenas: hay concatenación de secuencias, y una cadena es una.
"""),
        "tcl": ("""
gets stdin linea
set n [string trim $linea]

set suma  [expr {$n + $n}]
set texto "$n$n"

puts "suma=$suma texto=$texto"
""", """
**Lo que esta clase enseña en Tcl.** Estas dos líneas son la definición operativa del tipado débil:
**la misma variable `$n`, dos resultados distintos según lo que se haga con ella.** `expr` la lee
como número y da 10; la interpolación la pega consigo misma y da 55. No hubo conversión en ninguna
dirección, porque no había nada que convertir.

Y fíjate en que **no hay operador de concatenación**. En Perl es `.`, en Pascal `+`, en Ada `&`, en
Fortran `//`. En Tcl es *escribir las cosas juntas*: `"$n$n"`. Es la consecuencia lógica de que todo
sea texto — pegar dos textos no necesita una operación, necesita ponerlos seguidos.

La comparación es donde esto se vuelve delicado, y Tcl lo resuelve con comandos separados en lugar de
con operadores duplicados:

```tcl
expr {"10" == "10.0"}          ;# 1  -- compara como NÚMEROS
expr {"10" eq "10.0"}          ;# 0  -- compara como CADENAS
string compare "10" "10.0"     ;# -1 -- comparación textual explícita
string equal "abc" "abc"       ;# 1
```

`eq` y `ne` se añadieron en Tcl 8.4, en 2002, **precisamente porque `==` daba sorpresas**. Es el mismo
problema que llevó a JavaScript a añadir `===` y a PHP a añadir `==='`. Tres lenguajes distintos, la
misma cicatriz.
"""),
        "perl": ("""
use strict;
use warnings;

my $n = <STDIN>;
chomp $n;

printf "suma=%d texto=%s\\n", $n + $n, $n . $n;
""", """
**Lo que esta clase enseña en Perl.** `$n + $n` y `$n . $n`. Un solo dato, dos operadores, dos
resultados. Perl es el ejemplo canónico de tipado débil **bien diseñado**, y la razón es que separó
los operadores en lugar de sobrecargarlos:

| Operación | Números | Cadenas |
|---|---|---|
| Combinar | `+` | `.` |
| Repetir | `*` | `x` |
| Igualdad | `==` | `eq` |
| Distinto | `!=` | `ne` |
| Orden | `<` `>` `<=` `>=` | `lt` `gt` `le` `ge` |
| Comparar | `<=>` | `cmp` |

Esa tabla es toda la clase. En JavaScript, `+` hace las dos cosas y `2 + '2'` da `'22'` mientras que
`2 - '2'` da `0`; en Perl esa ambigüedad **no puede existir**, porque el operador declara la
intención. Larry Wall eligió duplicar los operadores en vez de duplicar las sorpresas, y en
retrospectiva acertó.

El precio es que hay que elegir bien: `if ($a == $b)` sobre dos cadenas de texto compara ambas como
números —las dos valen 0— y **da verdadero siempre**. Es el error clásico, y `use warnings` lo avisa
con `isn't numeric`.

Y `x` es el operador de repetición de cadenas, que casi ningún lenguaje tiene como operador:
`'-' x 40` produce una línea de cuarenta guiones. Aquí, `$n x 2` habría sido otra forma de resolver
la clase.
"""),
        "cpp": ("""
#include <iostream>
#include <string>

int main() {
    std::string txt;
    if (!(std::cin >> txt)) return 1;

    const int n = std::stoi(txt);        // texto -> número, explícito

    std::cout << "suma=" << (n + n)
              << " texto=" << (txt + txt) << '\\n';
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** Tipado fuerte y estático: `n` es un `int` y `txt` es un
`std::string`, y son cosas distintas para siempre. `n + n` suma porque `int` tiene `operator+`;
`txt + txt` concatena porque `std::string` tiene el suyo. **Es el mismo símbolo resolviendo dos
funciones distintas en tiempo de compilación**, que es exactamente lo que la sobrecarga de operadores
significa.

Y `n + txt` **no compila**, que es la diferencia con JavaScript y la razón de que la sobrecarga sea
segura aquí: no hay conversión implícita entre `int` y `std::string`, así que no hay ninguna
sobrecarga aplicable.

Las conversiones son explícitas y su historia es instructiva:

```cpp
std::stoi("42");                 // C++11: lanza excepción si falla
std::to_string(42);              // C++11: número -> texto
std::atoi("42");                 // heredado de C: devuelve 0 si falla, SIN avisar
std::from_chars(b, e, valor);    // C++17: sin excepciones, sin locale, el más rápido
```

`atoi` es el ejemplo perfecto de por qué las funciones de C envejecen mal: **no distingue `"0"` de
`"hola"`**, las dos dan cero. `stoi` lanza `std::invalid_argument`, y `from_chars` devuelve un código
de error sin excepciones. Tres generaciones de la misma operación, y las tres siguen disponibles
porque C++ no rompe lo que ya funcionaba.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi TIPADO;
  n int(10) const;
end-pi;

dcl-s txt    varchar(20);
dcl-s salida char(60);

txt = %char(n);              // numero -> texto, explicito

salida = 'suma=' + %char(n + n) + ' texto=' + txt + txt;
dsply salida;

*inlr = *on;
return;
""", """
**Lo que esta clase enseña en RPG.** RPG es fuertemente tipado y usa **`+` para las dos cosas**, como
Pascal: sobre numéricos suma, sobre caracteres concatena. Y funciona por la misma razón —el
compilador conoce los tipos— con una diferencia importante frente al Pascal moderno: **RPG no
convierte números a texto automáticamente**, así que `'suma=' + n` **no compila**. Hay que escribir
`%char(n)`.

La familia de conversiones de RPG es amplia y muy explícita, cosa esperable en un lenguaje de
negocio:

```rpgle
%char(valor)              // a texto (numérico, fecha, hora, timestamp...)
%int(texto)               // a entero
%dec(texto : 15 : 2)      // a decimal con dígitos y decimales declarados
%date(texto : *iso)       // a fecha, con el formato declarado
%editc(valor : 'A')       // a texto con edición: separadores de miles, signo...
%editw(valor : '  0.  ')  // a texto con una máscara de edición propia
```

`%editc` y `%editw` son las que no tienen equivalente en el núcleo: aplican **códigos y máscaras de
edición** —los mismos de los campos editados de COBOL— para producir `1.234.567,89` o
`$   1,234.56` sin construir la cadena a mano. Es formateo de importes como operación del lenguaje,
que es justo lo que se necesita al imprimir una factura.
"""),
        "pli": ("""
 tipado: procedure options(main);

    declare n   fixed binary(31);
    declare txt character(20) varying;

    get list (n);
    txt = trim(char(n));      /* char() convierte; en PL/I tambien seria implicito */

    put skip list ('suma=' || trim(char(n + n)) || ' texto=' || txt || txt);

 end tipado;
""", """
**Lo que esta clase enseña en PL/I.** PL/I es **estático y débil a la vez**, una combinación que casi
nadie más tiene, y esta clase la expone perfectamente. La conversión de número a texto se puede
escribir con `char(n)`… o se puede omitir:

```pli
declare n   fixed binary(31) initial(5);
declare txt character(20) varying;

txt = n;              /* FUNCIONA. Conversión implícita a texto. */
txt = txt || n;       /* TAMBIÉN funciona: convierte y concatena. */
n = '42';             /* Y esto también, en la dirección contraria. */
```

Todo eso compila y hace algo razonable. El operador `||` es la concatenación —el mismo de SQL, que lo
heredó de aquí— y convierte sus operandos a cadena si hace falta.

Es cómodo, y es exactamente lo que hace que un `if` mal escrito compile y falle en producción. La
diferencia con Perl es reveladora: Perl es débil pero **duplicó los operadores** para que la
intención sea explícita; PL/I es débil y **sobrecargó las conversiones** para que nada estorbe. La
primera decisión envejeció bien y la segunda no.

Cuando en la [Parte 1](../../../classes/parte-1-atlas-y-genealogia-de-los-lenguajes/README.md) se
habla de que un lenguaje puede tener demasiadas reglas, este es el caso concreto al que apuntar.
"""),
        "mumps": ("""
FUERTE ; Tipado debil -- clase 051
 read n
 write "suma=", n + n
 write " texto=", n _ n, !
 quit
""", """
**Lo que esta clase enseña en M.** El programa más corto de toda la Parte 3, y el más elocuente:
**`n + n` y `n _ n`**. La misma variable, dos operadores, dos resultados. `+` la lee como número, `_`
la concatena como texto. No hay conversión, no hay declaración, no hay comprobación.

Es el mismo diseño que Perl —operadores separados para números y para texto— pero llevado al extremo
y **sin la red de seguridad de `use warnings`**. En M, `"hola" + 1` da `1` en silencio; en Perl da un
aviso.

La comparación arrastra la misma dualidad, y aquí está la trampa que más código M ha roto:

```mumps
write 10 = 10.0        ; 0   -- ¡FALSO! "=" compara como CADENAS
write +10 = +10.0      ; 1   -- el + fuerza contexto numérico
write "10" < "9"       ; 1   -- comparación numérica: 10 < 9 es falso... ¿o no?
```

En M, `=` compara **cadenas** y `<`, `>` comparan **números**. Dos operadores de comparación con
contextos distintos, en el mismo lenguaje, sin nada que lo señale. El idioma para forzar el contexto
numérico es anteponer `+`, igual que `+$x` en JavaScript.

Ese es el motivo de que M tenga fama de ilegible: no es la brevedad, es que **el contexto no está
escrito en ninguna parte** y hay que reconstruirlo mentalmente operador a operador.
"""),
        "smalltalk": ("""
| n txt |

n := stdin nextLine trimBoth asNumber.
txt := n printString.

Transcript
    show: 'suma=', (n + n) printString;
    show: ' texto=', txt , txt;
    cr.
""", """
**Lo que esta clase enseña en Smalltalk.** Tipado **fuerte y dinámico**: `3 + '3'` no concatena ni
convierte, levanta un `MessageNotUnderstood` porque `SmallInteger` no sabe qué hacer con una cadena.
La conversión es explícita y va en las dos direcciones con mensajes simétricos: `printString` del
objeto al texto, `asNumber` del texto al objeto.

Fíjate en que la concatenación es la **coma**: `txt , txt`. Y no es un operador de cadenas — es el
mensaje `,` definido en **`Collection`**, así que concatena arrays, conjuntos ordenados y cualquier
otra colección con la misma sintaxis. Otra vez la uniformidad de la clase 048.

Lo que hace único a Smalltalk en esta clase es qué ocurre **cuando el tipo no encaja**. En C++ es un
error de compilación; en Perl, una coerción; en M, un cero silencioso. En Smalltalk se envía a la
imagen un mensaje `doesNotUnderstand:` que, por defecto, **abre el depurador con la pila viva** — y
ahí puedes inspeccionar el objeto, implementar el método que faltaba y **continuar la ejecución desde
el punto exacto**, sin reiniciar.

Y `doesNotUnderstand:` se puede **redefinir**, lo que permite construir objetos que responden a
mensajes que nadie implementó: es el mecanismo con el que se hacen los *proxies*, los objetos remotos
y los envoltorios dinámicos. El fallo de tipado es, en Smalltalk, un punto de extensión.
"""),
    },
)
