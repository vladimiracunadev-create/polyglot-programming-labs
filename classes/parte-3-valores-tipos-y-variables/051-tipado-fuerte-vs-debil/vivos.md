# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 051

> [⬅️ Volver a la clase 051](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

El mismo valor, dos operaciones: **sumarlo consigo mismo** y **pegarlo consigo mismo**. Con `5` da
`10` y `55`. Es el experimento mínimo del tipado débil, y separa a los lenguajes en dos grupos
tajantes: los que necesitan **dos operadores distintos** porque el dato no dice qué es, y los que
necesitan **una conversión explícita** porque el dato sí lo dice.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es **la fuerza del tipado**, que es cosa distinta de si es estático o dinámico
> —tema de la clase 050—. Y estos lenguajes lo enseñan porque contienen los dos casos extremos.
>
> En **M** y en **Perl**, el mismo valor se suma con `+` y se concatena con `_` o con `.`: **el
> operador decide el tipo**, y por eso hacen falta dos. En **Tcl** ni siquiera hace falta operador de
> concatenación, porque pegar dos cosas es escribirlas juntas. En el otro extremo, **Ada** y **C++**
> exigen convertir a texto con una llamada visible antes de poder concatenar.
>
> Y entre medias está COBOL, que necesita **un verbo entero** —`STRING`— para hacer lo que en Perl es
> un punto.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: un entero `n` → stdout: `suma=<n+n> texto=<n concatenado consigo mismo>`
- **Regla:** `suma = n + n ; texto = str(n) ++ str(n)`

| stdin | esperado |
|---|---|
| `5` | `suma=10 texto=55` |
| `3` | `suma=6 texto=33` |
| `12` | `suma=24 texto=1212` |

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
```

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

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program tipado
   implicit none
   integer :: n
   character(len=32) :: txt

   read(*, *) n
   write(txt, '(I0)') n           ! número -> texto: hay que ESCRIBIRLO

   write(*, '(A,I0,A,A)') 'suma=', n + n, ' texto=', trim(txt) // trim(txt)
end program tipado
```

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

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
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
```

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

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
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
```

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

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let* ((n (read))
       (txt (princ-to-string n)))
  (format t "suma=~D texto=~A~%" (+ n n) (concatenate 'string txt txt)))
```

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

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea
set n [string trim $linea]

set suma  [expr {$n + $n}]
set texto "$n$n"

puts "suma=$suma texto=$texto"
```

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

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $n = <STDIN>;
chomp $n;

printf "suma=%d texto=%s\n", $n + $n, $n . $n;
```

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

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>
#include <string>

int main() {
    std::string txt;
    if (!(std::cin >> txt)) return 1;

    const int n = std::stoi(txt);        // texto -> número, explícito

    std::cout << "suma=" << (n + n)
              << " texto=" << (txt + txt) << '\n';
    return 0;
}
```

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
```

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

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 tipado: procedure options(main);

    declare n   fixed binary(31);
    declare txt character(20) varying;

    get list (n);
    txt = trim(char(n));      /* char() convierte; en PL/I tambien seria implicito */

    put skip list ('suma=' || trim(char(n + n)) || ' texto=' || txt || txt);

 end tipado;
```

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

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
FUERTE ; Tipado debil -- clase 051
 read n
 write "suma=", n + n
 write " texto=", n _ n, !
 quit
```

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

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| n txt |

n := stdin nextLine trimBoth asNumber.
txt := n printString.

Transcript
    show: 'suma=', (n + n) printString;
    show: ' texto=', txt , txt;
    cr.
```

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

---

## Y de vuelta a la clase

La regla transferible es simple y vale para cualquier lenguaje que aprendas: **cuenta los operadores
de comparación**. Si el lenguaje tiene dos juegos —`==` y `eq` en Perl, `=` y `==` en M según el
contexto, `==` y `===` en JavaScript y PHP— es porque el dato no lleva su tipo encima y hay que
decírselo al operador. Si tiene uno solo, el tipo está en el valor. Esa cuenta te dice más sobre un
lenguaje en diez segundos que su documentación en una hora.

⏮️ [Volver a la clase 051](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
