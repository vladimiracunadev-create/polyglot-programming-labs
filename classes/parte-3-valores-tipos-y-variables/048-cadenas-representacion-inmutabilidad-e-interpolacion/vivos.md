# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 048

> [⬅️ Volver a la clase 048](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Leer una palabra y decir cuánto mide. Dos operaciones triviales que esconden la pregunta que separa
a estos doce lenguajes: **¿dónde está escrita la longitud de una cadena?** ¿En un contador delante
del texto, en un byte cero al final, en el tipo, o en ninguna parte porque el campo siempre mide lo
mismo y se rellena con espacios?

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es **la representación física de una cadena**, y estos lenguajes cubren las cuatro
> respuestas posibles, cosa que el núcleo no hace. COBOL y Fortran usan **campos de longitud fija
> rellenos de espacios**, así que la longitud "real" es una convención y `TRIM` aparece por todas
> partes. PL/I y RPG tienen cadenas **con contador** (`varying`, `varchar`). C++ arrastra las cadenas
> **terminadas en cero** de C junto a `std::string`. Y Smalltalk y Lisp las tratan como **colecciones
> de objetos**, con toda la maquinaria de colecciones aplicable.
>
> Cada respuesta arrastra sus propios errores característicos, y reconocerlos es lo transferible.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: una palabra (ASCII, sin espacios) → stdout: `hola=<palabra> longitud=<número de caracteres>`
- **Regla:** `longitud = |palabra|`

| stdin | esperado |
|---|---|
| `Ada` | `hola=Ada longitud=3` |
| `Bo` | `hola=Bo longitud=2` |
| `polyglot` | `hola=polyglot longitud=8` |

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
```

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

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program cadenas
   implicit none
   character(len=100) :: palabra

   read(*, '(A)') palabra

   write(*, '(A,A,A,I0)') 'hola=', trim(palabra), &
                          ' longitud=', len_trim(palabra)
end program cadenas
```

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

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
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
```

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

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
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
```

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

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let ((palabra (string-trim '(#\Space #\Tab #\Return) (read-line))))
  (format t "hola=~A longitud=~D~%" palabra (length palabra)))
```

**Lo que esta clase enseña en Common Lisp.** Una cadena de Lisp **es un array de caracteres**, sin
metáfora: su tipo real es `(vector character)`. Y esa no es una curiosidad, es la clave de todo,
porque significa que **las funciones de secuencia funcionan sobre ella**:

```lisp
(length  "polyglot")               ; => 8
(reverse "polyglot")               ; => "tolgylop"
(subseq  "polyglot" 4)             ; => "glot"
(position #\g "polyglot")          ; => 4
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

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea
set palabra [string trim $linea]

puts "hola=$palabra longitud=[string length $palabra]"
```

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

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $palabra = <STDIN>;
chomp $palabra;

printf "hola=%s longitud=%d\n", $palabra, length($palabra);
```

**Lo que esta clase enseña en Perl.** La interpolación de Perl es la más completa de esta página y
es el rasgo que definió al lenguaje: dentro de comillas dobles se sustituyen variables escalares,
elementos de array, elementos de hash, listas enteras y hasta expresiones:

```perl
print "Hola $nombre, tienes $edad años\n";
print "El primero es $lista[0] y la clave es $h{color}\n";
print "Toda la lista: @lista\n";           # los une con espacios
print "Resultado: @{[ $a * $b ]}\n";       # el idioma para interpolar una expresión
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

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>
#include <string>

int main() {
    std::string palabra;
    if (!(std::cin >> palabra)) return 1;

    std::cout << "hola=" << palabra
              << " longitud=" << palabra.size() << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** C++ arrastra **las dos representaciones a la vez**, y esa
convivencia es la fuente de una parte enorme de sus problemas históricos:

| | `const char*` (de C) | `std::string` |
|---|---|---|
| Longitud | Hasta el byte `\0` — `strlen` **recorre** | Guardada — `size()` es constante |
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
```

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

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 cadenas: procedure options(main);

    declare linea   character(80) varying;
    declare palabra character(80) varying;

    get edit (linea) (a(80));
    palabra = trim(linea);

    put skip list ('hola=' || palabra ||
                   ' longitud=' || trim(char(length(palabra))));

 end cadenas;
```

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

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
CADENAS ; Cadenas -- clase 048
 read palabra
 write "hola=", palabra, " longitud=", $length(palabra), !
 quit
```

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

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| palabra |

palabra := stdin nextLine trimBoth.

Transcript
    show: 'hola=', palabra;
    show: ' longitud=', palabra size printString;
    cr.
```

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

---

## Y de vuelta a la clase

Si algo deja claro esta página es que **"longitud de una cadena" no es una pregunta única**. Puede
ser el tamaño del campo, la posición del último carácter no blanco, el contador guardado delante, la
distancia hasta el byte cero, o el número de caracteres Unicode — que ya vimos en la clase 047 que
tampoco es el número de bytes. Cuando un programa mezcla dos de esas definiciones sin darse cuenta,
aparece el defecto más difícil de encontrar de todos: el que solo se manifiesta con ciertos datos.

⏮️ [Volver a la clase 048](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
