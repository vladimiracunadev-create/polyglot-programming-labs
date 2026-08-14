# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 044

> [⬅️ Volver a la clase 044](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Escribir el mismo número en base 10, 16, 8 y 2 parece un ejercicio de formato. No lo es: es la
prueba más rápida para descubrir **qué considera cada lenguaje que es un entero**. Si un lenguaje
piensa en el entero como un patrón de bits, la conversión a hexadecimal viene de fábrica. Si piensa
en él como una cantidad decimal de negocio, no viene — y hay que escribirla.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Esta es la clase donde la lista se parte en dos mitades limpias. **Fortran, Lisp, Perl y C++ te dan
> las bases hechas**, porque su entero es una palabra de máquina o un objeto matemático. **COBOL, Ada,
> Pascal, RPG y PL/I no**, y hay que escribir la conversión a mano — no por descuido de sus
> diseñadores, sino porque en banca, seguros y aviónica *no existe* la necesidad de imprimir un saldo
> en octal. La herramienta refleja el dominio.
>
> Y en medio queda Tcl, que tiene `%x` y `%o` pero **no `%b`**: un recordatorio de que estas
> capacidades se añaden una a una, cuando alguien las necesita, y no en bloque.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: una línea `n` (entero no negativo) → stdout: `dec=<n> hex=<hex minúscula> oct=<octal> bin=<binario>`
- **Regla:** `misma n en base 10, 16, 8 y 2 (sin prefijos ni ceros a la izquierda)`

| stdin | esperado |
|---|---|
| `255` | `dec=255 hex=ff oct=377 bin=11111111` |
| `10` | `dec=10 hex=a oct=12 bin=1010` |
| `1` | `dec=1 hex=1 oct=1 bin=1` |

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
PROGRAM-ID. BASES.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA     PIC X(80).
01  N         PIC 9(9) COMP-3.
01  ED-N      PIC Z(8)9.
01  DIGITOS   PIC X(16) VALUE "0123456789abcdef".
01  VALOR     PIC 9(9) COMP-3.
01  BASE      PIC 9(2) COMP-3.
01  RESTO     PIC 9(2) COMP-3.
01  IDX       PIC 9(2) COMP-3.
01  POS       PIC 9(2) COMP-3.
01  BUFFER    PIC X(40).
01  HEX-TXT   PIC X(40).
01  OCT-TXT   PIC X(40).
01  BIN-TXT   PIC X(40).

PROCEDURE DIVISION.
    ACCEPT LINEA
    MOVE FUNCTION NUMVAL(LINEA) TO N

    MOVE 16 TO BASE
    PERFORM CONVERTIR
    MOVE BUFFER TO HEX-TXT

    MOVE 8 TO BASE
    PERFORM CONVERTIR
    MOVE BUFFER TO OCT-TXT

    MOVE 2 TO BASE
    PERFORM CONVERTIR
    MOVE BUFFER TO BIN-TXT

    MOVE N TO ED-N
    DISPLAY "dec=" FUNCTION TRIM(ED-N)
            " hex=" FUNCTION TRIM(HEX-TXT)
            " oct=" FUNCTION TRIM(OCT-TXT)
            " bin=" FUNCTION TRIM(BIN-TXT)
    STOP RUN.

CONVERTIR.
    MOVE SPACES TO BUFFER
    MOVE N TO VALOR
    MOVE 40 TO POS
    IF VALOR = 0
        MOVE "0" TO BUFFER(40:1)
    ELSE
        PERFORM UNTIL VALOR = 0
            COMPUTE RESTO = FUNCTION MOD(VALOR, BASE)
            COMPUTE IDX = RESTO + 1
            MOVE DIGITOS(IDX:1) TO BUFFER(POS:1)
            SUBTRACT 1 FROM POS
            COMPUTE VALOR = VALOR / BASE
        END-PERFORM
    END-IF.
```

**Lo que esta clase enseña en COBOL.** **COBOL no sabe imprimir en hexadecimal**, y la razón es
coherente con todo lo demás: su entero no es un patrón de bits, es **una cantidad decimal con un
número de dígitos declarado**. `PIC 9(9)` no significa "32 bits", significa "nueve dígitos". La
pregunta "¿cómo se ve esto en base 16?" simplemente no se plantea cuando el dato es el saldo de una
cuenta.

Así que el algoritmo hay que escribirlo, y al escribirlo se ve lo que `%x` esconde: **divisiones
sucesivas quedándose con el resto**, llenando el resultado de derecha a izquierda. `BUFFER(POS:1)` es
**modificación de referencia**, la forma de COBOL de indexar dentro de un campo: `campo(inicio:largo)`.

Y hay un detalle de esta clase que COBOL trata mejor que casi nadie: **el desbordamiento**. Un
`PIC 9(9)` que recibe mil millones **trunca por la izquierda en silencio** —igual que C—, salvo que
lo pidas explícitamente:

```cobol
COMPUTE TOTAL = A * B
    ON SIZE ERROR DISPLAY "desbordamiento"
END-COMPUTE
```

`ON SIZE ERROR` es una cláusula del propio verbo aritmético. No es una excepción global ni un flag
del compilador: es una rama del `COMPUTE`, escrita al lado de la operación que puede desbordar.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program bases
   implicit none
   integer :: n, i
   character(len=40) :: hex, oct, bin

   read(*, *) n

   write(hex, '(Z0)') n
   write(oct, '(O0)') n
   write(bin, '(B0)') n

   do i = 1, len_trim(hex)
      if (iachar(hex(i:i)) >= iachar('A') .and. &
          iachar(hex(i:i)) <= iachar('F')) then
         hex(i:i) = achar(iachar(hex(i:i)) + 32)
      end if
   end do

   write(*, '(A,I0,A,A,A,A,A,A)') 'dec=', n, ' hex=', trim(hex), &
        ' oct=', trim(oct), ' bin=', trim(bin)
end program bases
```

**Lo que esta clase enseña en Fortran.** Fortran **sí** trae las bases, y de una forma que no tiene
ningún otro lenguaje de esta página: como **descriptores de edición** dentro del formato, junto a `I`
para decimal y `F` para real.

| Descriptor | Base |
|---|---|
| `I` | 10 |
| `Z` | 16 |
| `O` | 8 |
| `B` | 2 |

El `0` de `'(Z0)'` pide **ancho mínimo**: sin él habría que decir cuántas columnas ocupa. Que las
cuatro bases sean descriptores del sistema de formato, y no funciones de biblioteca, es muy propio
de Fortran: el formato es un mini-lenguaje con entidad propia, igual que el `format` de Lisp.

Lo único que falta es minúsculas —`Z` produce `FF`, no `ff`—, y por eso el bucle de conversión.
`achar` e `iachar` son las funciones que van de código ASCII a carácter y al revés; existen también
`char` e `ichar`, que usan el juego de caracteres del procesador. Que haya dos parejas es una
concesión a las máquinas que no eran ASCII, un rastro más de 1957.

Sobre el desbordamiento: un `integer` por defecto son 32 bits y **desborda en silencio**. Con
`gfortran -fcheck=all` se detecta en ejecución, y con `integer(int64)` se pospone.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Bases is

   Digitos : constant String := "0123456789abcdef";

   --  Recursiva: divisiones sucesivas, de la más significativa a la última.
   function En_Base (N : Natural; B : Positive) return String is
   begin
      if N < B then
         return (1 => Digitos (N + 1));
      else
         return En_Base (N / B, B) & Digitos (N rem B + 1);
      end if;
   end En_Base;

   N : Integer;
begin
   Get (N);

   Put ("dec=");  Put (N, Width => 1);
   Put (" hex=" & En_Base (N, 16));
   Put (" oct=" & En_Base (N, 8));
   Put (" bin=" & En_Base (N, 2));
   New_Line;
end Bases;
```

**Lo que esta clase enseña en Ada.** Ada **sí** tiene salida en otras bases —`Put (N, Base => 16)`—
pero produce `16#FF#`, que es el **literal basado** del propio lenguaje, con la base delante y el
número entre almohadillas. Es coherente y es inutilizable aquí, así que el programa escribe la
conversión.

Y esa notación es lo que hay que llevarse de esta clase: en Ada puedes **escribir** literales en
cualquier base de 2 a 16, en el código fuente:

```ada
Mascara  : constant := 2#1111_0000#;   --  binario, con subrayados
Color    : constant := 16#FF_A0_20#;   --  hexadecimal
Permisos : constant := 8#755#;         --  octal
```

Compara con C y sus prefijos `0x`, `0` y `0b`: en Ada la base es un número explícito delante, así que
funciona para **cualquier** base, no solo para tres privilegiadas. Es un caso claro de generalidad
por diseño.

Sobre el desbordamiento, aquí Ada se separa de casi todos: **no desborda en silencio**. Superar
`Integer'Last` levanta `Constraint_Error` en el punto exacto. Y los atributos `Integer'First`,
`Integer'Last`, `Integer'Size` permiten preguntar los límites al propio tipo en vez de consultarlos
en un manual.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Bases;
{$MODE OBJFPC}{$H+}
uses SysUtils;

function EnBase(N, B: Integer): string;
const
  DIGITOS = '0123456789abcdef';
begin
  if N < B then
    Result := DIGITOS[N + 1]
  else
    Result := EnBase(N div B, B) + DIGITOS[N mod B + 1];
end;

var
  N: Integer;

begin
  Read(N);
  WriteLn('dec=', IntToStr(N),
          ' hex=', EnBase(N, 16),
          ' oct=', EnBase(N, 8),
          ' bin=', EnBase(N, 2));
end.
```

**Lo que esta clase enseña en Pascal.** Pascal distingue **dos operadores de división**, y esta clase
es donde se nota: `div` es división entera y `/` **siempre** da un `Real`, incluso entre enteros.
`7 div 2` es `3`; `7 / 2` es `3.5` y no puede asignarse a un `Integer`. En C, en Java y en Go, `7/2`
da `3` y hay que recordar que el tipo decide; en Pascal el operador lo dice.

Sobre las bases: el Pascal ISO no tiene conversión, y Free Pascal añade `IntToHex` y `BinStr`/`OctStr`
—que rellenan con ceros a la izquierda hasta el ancho que pidas—. Escribir `EnBase` a mano evita esa
asimetría y muestra el algoritmo.

Los literales sí traen notación de base, heredada de Turbo Pascal, con un símbolo distinto por base:

```pascal
const
  Mascara = %11110000;   { binario }
  Color   = $FFA020;     { hexadecimal }
  Permiso = &755;        { octal }
```

Y sobre el desbordamiento, Free Pascal tiene una directiva que casi nadie activa y debería:
`{$Q+}` comprueba el desbordamiento aritmético en ejecución y `{$R+}` comprueba los rangos de índices
y subrangos. Con ellas, Pascal se comporta como Ada; sin ellas, como C.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let ((n (read)))
  (format t "dec=~D hex=~(~X~) oct=~O bin=~B~%" n n n n))
```

**Lo que esta clase enseña en Common Lisp.** Una línea. `format` trae las cuatro bases como
directivas —`~D`, `~X`, `~O`, `~B`— y además `~R`, que imprime en **cualquier** base:
`(format nil "~3R" 255)` da `"100110"` en base 3. Y `~R` sin argumento numérico escribe el número
**en palabras**: `(format nil "~R" 255)` da `"two hundred fifty-five"`.

El `~(` … `~)` que envuelve al `~X` es una **directiva de conversión de mayúsculas y minúsculas**:
todo lo que se produzca dentro sale en minúsculas. `format` no es una función de formateo: es un
lenguaje completo empotrado, con condicionales (`~[`), iteración sobre listas (`~{`), pluralización
(`~P`) y recursión (`~?`).

Los literales también admiten cualquier base con `#<base>r`:

```lisp
#b1111        ; binario   -> 15
#o755         ; octal     -> 493
#xFF          ; hexa      -> 255
#3r210        ; base 3    -> 21
```

Y la parte que hace único a Lisp en esta clase: **sus enteros no desbordan**. `(expt 2 200)` devuelve
el número completo, de 61 dígitos. No hay tamaño, no hay signo que se voltee, no hay
comportamiento indefinido. El desbordamiento —el tema central de esta clase en casi todos los demás
lenguajes— sencillamente no existe aquí.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
proc enBase {n b} {
    set digitos "0123456789abcdef"
    if {$n < $b} { return [string index $digitos $n] }
    return "[enBase [expr {$n / $b}] $b][string index $digitos [expr {$n % $b}]]"
}

gets stdin linea
set n [string trim $linea]

puts "dec=$n hex=[format %x $n] oct=[format %o $n] bin=[enBase $n 2]"
```

**Lo que esta clase enseña en Tcl.** Un ejemplo perfecto de que estas capacidades **se añaden de una
en una**: `format` de Tcl tiene `%x` y `%o`, heredados de `printf` de C, pero **no tiene `%b`**,
porque `printf` de C tampoco lo tiene. Nadie lo echó de menos lo suficiente durante décadas. Así que
el binario hay que escribirlo, mientras que hexadecimal y octal vienen hechos — una asimetría que no
responde a ninguna lógica del lenguaje, solo a su historia.

Para la dirección contraria, Tcl tiene `scan`, que es el `sscanf` de C: `scan ff %x valor` deja 255
en `valor`. Y desde Tcl 8.5 los literales aceptan `0x`, `0o` y `0b`.

Fíjate también en cómo se construye el resultado recursivo: `"[enBase ...][string index ...]"` —dos
sustituciones de comando **pegadas dentro de una cadena entre comillas**. En Tcl no hace falta
operador de concatenación porque la interpolación de cadenas ya concatena. Es el mismo principio de
siempre: todo es texto, así que juntar dos cosas es escribirlas seguidas.

Y sobre el desbordamiento: desde Tcl 8.5, **los enteros son de precisión arbitraria**, como en Lisp.
`expr {2**200}` funciona.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $n = <STDIN>;
chomp $n;

printf "dec=%d hex=%x oct=%o bin=%b\n", $n, $n, $n, $n;
```

**Lo que esta clase enseña en Perl.** Perl es el único de esta página que trae las **cuatro** bases
en `printf` sin excepciones: `%d`, `%x`, `%o` y `%b`. El `%b` que le falta a C y a Tcl aquí sí está,
porque Perl añadió lo que la gente pedía en vez de limitarse a envolver la biblioteca de C.

La dirección contraria también es de una línea, con `oct`, que a pesar del nombre entiende los tres
prefijos:

```perl
my $x = hex("ff");      # 255
my $y = oct("0xff");    # 255  — oct reconoce 0x, 0b y 0
my $z = oct("0b1010");  # 10
```

Y los literales admiten **subrayados como separadores**, en cualquier base:
`0xFF_A0_20`, `0b1111_0000`, `1_000_000`.

Sobre el desbordamiento, Perl hace algo característico suyo y discutible: cuando un entero no cabe
en la palabra de máquina, **lo convierte a real en silencio** y sigue. No falla y no avisa; empiezas
a perder precisión sin enterarte. Si necesitas exactitud sin límite, el módulo `bigint` de la
biblioteca estándar cambia el comportamiento del programa entero con una sola línea `use bigint;`.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>
#include <string>

std::string en_base(unsigned long n, unsigned base) {
    static const char* digitos = "0123456789abcdef";
    if (n < base) return std::string(1, digitos[n]);
    return en_base(n / base, base) + digitos[n % base];
}

int main() {
    unsigned long n{};
    if (!(std::cin >> n)) return 1;

    std::cout << "dec=" << n
              << " hex=" << en_base(n, 16)
              << " oct=" << en_base(n, 8)
              << " bin=" << en_base(n, 2) << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** C++ tiene `std::hex` y `std::oct` como manipuladores de flujo,
pero **no tiene `std::bin`**: la misma laguna que Tcl y por el mismo motivo, la herencia de `printf`.
Para binario está `std::bitset`, que rellena con ceros hasta un ancho fijo, o —desde C++20—
`std::format("{:b}", n)`, que por fin lo resuelve bien.

Y hay una trampa clásica que conviene conocer: **`std::hex` es pegajoso**. Cambia el estado del flujo
y **sigue activo** para todo lo que se escriba después, hasta que alguien ponga `std::dec`. Más de un
número decimal ha salido en hexadecimal por esto. Es el mismo defecto de diseño que `std::fixed` y
`std::setprecision`, y es la razón por la que `std::format` y `std::print` los sustituyen.

Fíjate en que este programa usa `unsigned long`, no `int`. Es deliberado: **el desplazamiento y el
desbordamiento de un entero con signo son comportamiento indefinido en C++**, no un valor
sorprendente sino una licencia para que el compilador asuma que nunca ocurre y optimice en
consecuencia. Con `unsigned`, el estándar sí define la aritmética modular. Cuando se manipulan
patrones de bits, `unsigned` no es una preferencia: es lo correcto.

Los literales llevan las tres bases —`0xFF`, `0755`, `0b1111` (C++14)— y desde C++14 la comilla
simple separa: `0b1111'0000`.

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
ctl-opt dftactgrp(*no) actgrp(*caller) main(Bases);

dcl-c DIGITOS '0123456789abcdef';

dcl-proc Bases;
  dcl-pi *n;
    n int(10) const;
  end-pi;

  dcl-s salida char(80);

  salida = 'dec=' + %char(n)
         + ' hex=' + enBase(n : 16)
         + ' oct=' + enBase(n : 8)
         + ' bin=' + enBase(n : 2);
  dsply salida;
end-proc;

dcl-proc enBase;
  dcl-pi *n varchar(64);
    v int(10) const;
    b int(10) const;
  end-pi;

  if v < b;
    return %subst(DIGITOS : v + 1 : 1);
  endif;
  return enBase(%div(v : b) : b) + %subst(DIGITOS : %rem(v : b) + 1 : 1);
end-proc;
```

**Lo que esta clase enseña en RPG.** Igual que COBOL: **no hay conversión de base**, porque el dato
de un ERP es una cantidad, no un patrón de bits. Lo más cercano son las APIs del sistema `CVTHC` y
`CVTCH` (*convert hex to char* y viceversa), que se llaman como programas del sistema operativo, no
como funciones del lenguaje.

Lo interesante de esta versión es otra cosa: **`main()` en `ctl-opt`**. Al declarar un procedimiento
principal, el programa deja de usar el **ciclo de RPG** y se comporta como un `main` de C — sin
indicadores, sin `*inlr`, con variables locales de verdad en cada `dcl-proc`. Es el RPG moderno, y
convive en la misma plataforma con programas que siguen usando el ciclo de 1959.

`%div` y `%rem` son las funciones de división entera y resto. Existen aparte porque el operador `/`
en RPG **redondea** al número de decimales del destino: `7 / 2` guardado en un entero da **4**, no 3.
Es una de las diferencias más peligrosas al portar código desde C o Java, y la razón de que RPG
obligue a pedir la división entera por su nombre.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 bases: procedure options(main);

    declare n       fixed binary(31);
    declare digitos character(16) initial('0123456789abcdef');

    declare en_base entry (fixed binary(31), fixed binary(31))
                    returns (character(64) varying) recursive;

    get list (n);

    put skip list ('dec='  || trim(char(n))     ||
                   ' hex=' || en_base(n, 16)    ||
                   ' oct=' || en_base(n, 8)     ||
                   ' bin=' || en_base(n, 2));

 en_base: procedure (v, b) returns (character(64) varying) recursive;
    declare (v, b) fixed binary(31);
    if v < b then
       return (substr(digitos, v + 1, 1));
    return (en_base(divide(v, b, 31), b) || substr(digitos, mod(v, b) + 1, 1));
 end en_base;

 end bases;
```

**Lo que esta clase enseña en PL/I.** Tampoco tiene conversión de base para presentación, pero sí
tiene algo que ningún otro lenguaje de esta página ofrece: **`unspec`**, que devuelve la
representación **en bits** de cualquier variable, del tipo que sea.

```pli
declare patron bit(32);
patron = unspec(n);        /* los bits crudos del entero */
```

Y funciona al revés: `unspec(x) = patron` reinterpreta los bits como el tipo de `x`. Es el
antepasado de `reinterpret_cast` de C++ y de `std::bit_cast`, disponible en 1964 y aplicable a
cualquier tipo, incluidas estructuras completas.

Fíjate también en `divide(v, b, 31)`: la división en PL/I es una **función con la precisión del
resultado como argumento**. `divide(a, b, 15, 2)` significa "divide y dame el resultado con 15
dígitos, 2 de ellos decimales". En un lenguaje que distingue base y escala, el resultado de una
división no se puede deducir de los operandos: hay que decirlo. Es verboso y es exacto.

Y `recursive` es una palabra que hay que escribir: en PL/I, como en el COBOL clásico, un
procedimiento **no es recursivo por defecto**, porque su almacenamiento es estático salvo que se
diga otra cosa.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
BASES ; Bases numericas -- clase 044
 read n
 write "dec=", n
 write " hex=", $$base(n, 16)
 write " oct=", $$base(n, 8)
 write " bin=", $$base(n, 2), !
 quit
 ;
base(v, b) ; v escrito en base b
 new d
 set d = "0123456789abcdef"
 quit:v<b $extract(d, v + 1)
 quit $$base(v\b, b) _ $extract(d, (v#b) + 1)
```

**Lo que esta clase enseña en M.** M no tiene bases —previsible, en un lenguaje sin tipos
numéricos—, pero la implementación muestra tres rasgos que definen el lenguaje.

El primero es **`$$etiqueta(args)`**, la llamada a una *función extrínseca*: una etiqueta normal que
devuelve un valor con `quit <valor>`. El doble dólar la distingue de las funciones incorporadas, que
llevan uno solo (`$piece`, `$extract`, `$select`).

El segundo son los **operadores de una sola letra o símbolo**: `\` es división entera —no una barra
invertida de escape—, `#` es módulo y `_` es concatenación. Que la concatenación sea el subrayado
sorprende siempre, y es la razón de que en M los nombres de variable no lleven subrayados.

El tercero es **`quit:v<b <valor>`**, el postcondicional. Casi cualquier comando admite `:condición`
pegada detrás para ejecutarse solo si se cumple. `quit:v<b ...` es el caso base de la recursión
escrito en once caracteres, sin `if` y sin bloque. Es a la vez la mayor virtud y el mayor obstáculo
del lenguaje: densidad extrema, legible solo cuando ya lo conoces.

Y `new d` da **ámbito dinámico** a `d` durante la llamada, que es la única forma de variable local
que existe en M.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| n |

n := stdin nextLine trimBoth asInteger.

Transcript
    show: 'dec=', n printString;
    show: ' hex=', (n printStringBase: 16) asLowercase;
    show: ' oct=', (n printStringBase: 8);
    show: ' bin=', (n printStringBase: 2);
    cr.
```

**Lo que esta clase enseña en Smalltalk.** `printStringBase:` es un **mensaje enviado al número**, y
acepta cualquier base entre 2 y 36. No es una función de biblioteca ni una directiva de formato: es
un método de la clase `Integer`, que puedes abrir, leer y —si quisieras— redefinir.

Los literales usan la misma idea, con la base delante y una `r` de *radix*:

```smalltalk
16rFF        "255"
2r1111_0000  "240, con subrayados desde Pharo 8"
36rZZ        "1295 — base 36, dígitos 0-9 y A-Z"
```

Que funcione hasta base 36 no es un adorno: es consecuencia de que la conversión sea código normal en
vez de una tabla privilegiada del compilador.

Y aquí, como en Lisp, **el desbordamiento no existe**. `SmallInteger` se convierte en
`LargePositiveInteger` de forma automática e invisible cuando el valor no cabe, y
`(2 raisedTo: 1000) printStringBase: 16` devuelve la cadena completa. En un lenguaje donde el entero
es un objeto y no una palabra de máquina, el tamaño deja de ser una propiedad del tipo y pasa a ser
un detalle de implementación.

---

## Y de vuelta a la clase

La lección es que **"pasar a hexadecimal" no es una operación universal**: es una facilidad que un
lenguaje ofrece si su idea de entero es el patrón de bits. Cuando la escribes a mano —en COBOL, en
Ada, en Pascal— redescubres el algoritmo de división sucesiva que hay debajo de `%x`, y esa es
precisamente la parte transferible. La otra lección, la incómoda, es que el desbordamiento sigue
esperando: `PIC 9(9)` desborda a los mil millones, un `int` de C++ a los 2147483647, y solo Lisp y
Smalltalk se niegan a desbordar.

⏮️ [Volver a la clase 044](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
