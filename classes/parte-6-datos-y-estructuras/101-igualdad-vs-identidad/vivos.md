# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 101

> [⬅️ Volver a la clase 101](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Dos enteros y una pregunta de una palabra. El programa es trivial en los doce lenguajes, y la
pregunta que hay debajo es de las más profundas del curso: **¿son el mismo valor, o son el mismo
objeto?** Y aquí hay un caso extremo: **Common Lisp tiene CUATRO predicados de igualdad**, y elegir
mal es una fuente clásica de errores. **Smalltalk tiene dos y los distingue con un carácter.**

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es la **distinción entre valor e identidad**, y estos lenguajes la enseñan porque
> cada uno la resolvió en su momento y a su manera. **COBOL** tiene una regla que sorprende a todos:
> compara cadenas **rellenando la más corta con espacios**, así que `"ADA"` y `"ADA   "` son iguales.
> **Pascal** no permite comparar registros con `=` en absoluto. **Ada** distingue igualdad de valor,
> igualdad de acceso e identidad de objeto, y permite redefinir la primera.
>
> Y **Fortran** aporta una trampa que ha costado precisión numérica durante sesenta años: **comparar
> reales con `==` casi nunca es lo que quieres**.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: una línea `a b` (dos enteros) → stdout: `iguales=<true|false>`
- **Regla:** `iguales = (a == b)`

| stdin | esperado |
|---|---|
| `5 5` | `iguales=true` |
| `3 7` | `iguales=false` |
| `0 0` | `iguales=true` |

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
PROGRAM-ID. IGUALES.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA  PIC X(80).
01  T1     PIC X(20).
01  T2     PIC X(20).
01  A      PIC S9(9) COMP-3.
01  B      PIC S9(9) COMP-3.
01  RES    PIC X(5).

PROCEDURE DIVISION.
    ACCEPT LINEA
    UNSTRING LINEA DELIMITED BY ALL SPACES INTO T1 T2
    COMPUTE A = FUNCTION NUMVAL(T1)
    COMPUTE B = FUNCTION NUMVAL(T2)

    IF A = B
        MOVE "true"  TO RES
    ELSE
        MOVE "false" TO RES
    END-IF

    DISPLAY "iguales=" FUNCTION TRIM(RES)
    STOP RUN.
```

**Lo que esta clase enseña en COBOL.** **En COBOL no existe la identidad**: no hay punteros
idiomáticos, no hay referencias y no hay objetos que comparar. Solo hay valores, y `=` compara
valores.

Lo interesante es **cómo** los compara, porque las reglas son propias y sorprenden.

**Comparación numérica: por valor algebraico, ignorando el formato.**

```cobol
01  A  PIC 9(3)V99        VALUE 12.50.
01  B  PIC S9(5)V9 COMP-3 VALUE 12.5.

IF A = B      *> CIERTO: se comparan los valores, no las representaciones
```

Un `DISPLAY` decimal, un `COMP-3` empaquetado y un `COMP` binario con el mismo valor **son iguales**.
COBOL alinea las comas decimales, extiende con ceros y compara. Es lo correcto para un lenguaje de
cálculo con decimales exactos, y no es gratis: la comparación puede requerir conversión.

**Comparación alfanumérica: se rellena con espacios el operando corto.**

```cobol
IF NOMBRE = "ADA"     *> CIERTO aunque NOMBRE sea PIC X(20)
```

Esa regla es la que hace utilizable el modelo de campos de longitud fija de la clase 093: sin ella,
comparar un campo con un literal exigiría escribir el relleno a mano. Y tiene un efecto que hay que
conocer: **`"ADA"` y `"ADA   "` son iguales, pero `"ADA"` y `" ADA"` no**, porque el relleno es solo
por la derecha.

**Y la comparación de grupos es de bytes.** Un `01` con subcampos se compara como una cadena, sin
mirar los tipos:

```cobol
IF REG-CLIENTE = REG-COPIA      *> compara los BYTES de todo el registro
```

Eso es rapidísimo y tiene una trampa clásica: **si el registro tiene campos numéricos binarios con
relleno sin inicializar, dos registros lógicamente iguales pueden diferir en bytes**. De ahí la norma
de inicializar los registros con `INITIALIZE` antes de usarlos.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program iguales
   implicit none
   integer :: a, b

   read(*, *) a, b

   if (a == b) then
      write(*, '(A)') 'iguales=true'
   else
      write(*, '(A)') 'iguales=false'
   end if
end program iguales
```

**Lo que esta clase enseña en Fortran.** Fortran no tiene identidad —no hay referencias comparables— y
tiene una lección que ha costado dinero de verdad: **nunca compares reales con `==`**.

```fortran
if (0.1 + 0.2 == 0.3) ...        ! FALSO en aritmética de coma flotante
if (abs(x - y) < 1.0e-10) ...     ! comparación por TOLERANCIA
if (abs(x - y) <= epsilon(x) * max(abs(x), abs(y))) ...   ! tolerancia RELATIVA
```

`epsilon(x)` es una función intrínseca que devuelve la precisión de la máquina para ese tipo, y su
existencia desde Fortran 90 —junto con `tiny`, `huge`, `spacing` y `nearest`— dice mucho sobre para
qué se diseñó el lenguaje. **Fortran es el lenguaje que más en serio se toma la aritmética de coma
flotante**, y esas funciones son el vocabulario para razonar sobre ella.

Fortran tiene además una peculiaridad sintáctica heredada de las tarjetas: **dos juegos de operadores
de comparación**.

```fortran
if (a .eq. b)     ! FORTRAN 77 y anterior: no había símbolos = < > en el juego de caracteres
if (a == b)       ! Fortran 90 en adelante
```

Los dos siguen siendo válidos, y el código antiguo está lleno de `.eq.`, `.ne.`, `.lt.`, `.ge.`. Es
la misma razón por la que el acceso a campos usa `%` en lugar de `.` (clase 091).

Y hay una distinción que Fortran hace y casi ningún lenguaje: **la comparación de lógicos tiene su
propio operador**.

```fortran
if (bandera .eqv. otra)      ! equivalencia LÓGICA
if (bandera .neqv. otra)     ! o exclusivo
```

`==` no funciona sobre `logical`: hay que usar `.eqv.`. Es más estricto que C, donde comparar
booleanos con `==` funciona porque son enteros.

Para tipos derivados, `==` **no se genera automáticamente**: hay que sobrecargar el operador con
`interface operator(==)`. Es la misma situación que en C++ antes de C++20 (clase 099).

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Iguales is
   A, B : Integer;
begin
   Get (A);
   Get (B);

   if A = B then
      Put_Line ("iguales=true");
   else
      Put_Line ("iguales=false");
   end if;
end Iguales;
```

**Lo que esta clase enseña en Ada.** Ada distingue **tres** comparaciones distintas, y las escribe de
formas distintas:

```ada
A = B                     --  igualdad de VALOR
P = Q                     --  para punteros: ¿apuntan al MISMO objeto?  (identidad)
P.all = Q.all             --  ¿los objetos apuntados son iguales?        (valor)
```

Y hay una regla que la diferencia de casi todos: **la igualdad predefinida de los registros compara
campo a campo, no bytes**. En C, `memcmp` sobre dos `struct` puede fallar por el relleno entre
campos; en Ada, `=` sobre un registro compara sus componentes uno a uno, así que el relleno no
interviene. Es correcto por construcción.

Para los tipos limitados, Ada va más lejos:

```ada
type Recurso is limited private;      --  sin = y sin asignación
```

**`limited`** significa que el tipo **no tiene igualdad ni asignación**, y hay que declararlas si se
quieren. Es la forma de decir "este objeto es único y no tiene sentido copiarlo ni compararlo" — un
fichero abierto, un semáforo, una tarea. En C++ se consigue borrando el constructor de copia; en Ada
es una palabra en la declaración.

Y redefinir la igualdad es sobrecargar el operador, con una regla importante:

```ada
function "=" (A, B : Cliente) return Boolean is (A.Nif = B.Nif);
```

**Ada 2012 aclaró que redefinir `"="` afecta también a los contenedores** —conjuntos, mapas, `Find`,
`Contains`— y a la comparación de arreglos de ese tipo. Antes había casos en que la igualdad
redefinida no se propagaba, lo que producía sorpresas; hoy la propagación está especificada.

Para la identidad de objetos en la orientación a objetos, Ada usa la comparación de accesos o el
atributo `'Address`, y para las tareas hay `Ada.Task_Identification`, que da un identificador único
comparable — la identidad convertida en un valor.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Iguales;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  A, B: Integer;

begin
  Read(A, B);

  if A = B then
    WriteLn('iguales=true')
  else
    WriteLn('iguales=false');
end.
```

**Lo que esta clase enseña en Pascal.** Pascal tiene una carencia en esta clase que sorprende y que
explica bastante código: **dos `record` NO se pueden comparar con `=`**.

```pascal
type TPunto = record X, Y: Integer; end;
var A, B: TPunto;
begin
  if A = B then ...        { NO COMPILA en Pascal estándar ni en Delphi }
end;
```

Wirth lo dejó fuera deliberadamente: **con registros variantes (clase 100) y relleno entre campos, no
hay una definición obvia de igualdad**, y comparar bytes daría resultados erróneos. Así que la
decisión fue no ofrecer ninguna.

La consecuencia es que en Pascal hay que escribir la comparación a mano, campo a campo, o recurrir a
`CompareMem`, con el riesgo del relleno.

Free Pascal moderno lo alivió con la **sobrecarga de operadores en registros**:

```pascal
type
  TPunto = record
    X, Y: Integer;
    class operator = (const A, B: TPunto): Boolean;
  end;
```

Y para los otros tipos, las reglas de Pascal son claras y distinguen bien valor de identidad:

| Comparación | Qué compara |
|---|---|
| `A = B` con enteros, reales, enumeraciones | valor |
| `S1 = S2` con `string` | **el CONTENIDO**, carácter a carácter |
| `O1 = O2` con objetos `class` | **la REFERENCIA**: ¿son el mismo objeto? |
| `P1 = P2` con punteros | la dirección |
| `C1 = C2` con conjuntos | los mismos elementos |

La segunda y la tercera son la distinción central: **las cadenas comparan valor, los objetos comparan
identidad**. Para comparar objetos por contenido hay que redefinir un método —`Equals`, heredado de
`TObject` en Delphi, siguiendo el modelo de Java.

Y hay una trampa clásica con las cadenas: **`=` sobre cadenas distingue mayúsculas**. Para no
distinguirlas hay `SameText` y `CompareText`, y usar `UpperCase` en la comparación es un error con
caracteres no ingleses.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let ((a (read))
      (b (read)))
  (format t "iguales=~A~%" (if (eql a b) "true" "false")))
```

**Lo que esta clase enseña en Common Lisp.** Aquí está el caso extremo de toda la página: **Common
Lisp tiene cuatro predicados de igualdad**, más varios especializados, y elegir el correcto es una
habilidad que se aprende a base de errores.

| Predicado | Compara | Ejemplo que da `T` | Ejemplo que da `NIL` |
|---|---|---|---|
| `eq` | **identidad de puntero** | `(eq 'a 'a)` | `(eq "a" "a")` |
| `eql` | identidad, más números y caracteres **del mismo tipo** por valor | `(eql 3 3)` | `(eql 3 3.0)` |
| `equal` | estructura: listas y cadenas elemento a elemento | `(equal "ab" "ab")` | `(equal "AB" "ab")` |
| `equalp` | como `equal`, ignorando mayúsculas y tipo numérico | `(equalp 3 3.0)` | `(equalp 3 4)` |

Y hay dos avisos que merecen destacarse.

**`eq` sobre números no es fiable.** `(eq 3 3)` puede devolver `T` o `NIL` según la implementación,
porque depende de si los enteros pequeños están internados. **Nunca uses `eq` con números**; usa
`eql`, que es el defecto de casi todo el lenguaje.

**`equalp` es sorprendentemente laxo.** Ignora mayúsculas en cadenas y compara enteros con flotantes,
así que `(equalp "Hola" "HOLA")` y `(equalp 1 1.0)` son ciertos. Es cómodo y es una fuente de fallos
sutiles cuando se usa por costumbre.

La razón de que existan los cuatro es histórica y de rendimiento: `eq` es **una comparación de
punteros**, la más barata posible; `equalp` puede recorrer estructuras enteras. Common Lisp expone el
coste en el nombre en lugar de esconderlo.

Y esto tiene consecuencias directas en las estructuras de datos (clase 095):

```lisp
(make-hash-table :test #'eql)     ; el defecto
(make-hash-table :test #'equal)   ; para claves que son CADENAS o listas
```

Una tabla con `:test #'eql` y claves de cadena **no encuentra nada**, porque dos cadenas iguales son
objetos distintos. Es probablemente el error más común de quien empieza con Lisp, y la corrección es
una palabra.

Para los objetos CLOS, la igualdad se define escribiendo un método sobre una función genérica propia
— el estándar no impone ninguna, lo que evita el problema de las jerarquías con `equals` heredado.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea
lassign [split [string trim $linea]] a b

if {$a == $b} {
    set r true
} else {
    set r false
}

puts "iguales=$r"
```

**Lo que esta clase enseña en Tcl.** Tcl tiene una peculiaridad que se explica sola una vez que se
entiende su modelo: **hay dos familias de comparación, y hay que elegir la correcta**.

```tcl
expr {$a == $b}      ;# comparación NUMÉRICA si ambos parecen números
expr {$a eq $b}      ;# comparación de CADENAS, siempre
expr {$a != $b}      ;#  y sus negaciones
expr {$a ne $b}
```

`==` intenta convertir a número; `eq` compara texto. La diferencia se ve en un ejemplo clásico:

```tcl
expr {"10" == "10.0"}     ;# 1 -- son el mismo NÚMERO
expr {"10" eq "10.0"}     ;# 0 -- son cadenas distintas
expr {"0x10" == 16}       ;# 1 -- se interpreta como hexadecimal
```

`eq` y `ne` llegaron en **Tcl 8.4 (2002)**, y son un buen ejemplo de corrección de diseño: durante
catorce años, comparar cadenas exigía `string compare` o arriesgarse a que `==` las convirtiera a
número. Ese riesgo era real: un identificador como `"007"` comparado con `"7"` daba igual.

Y **la identidad prácticamente no existe en Tcl**, porque todos los valores son inmutables desde el
punto de vista del programa: no hay forma de preguntar si dos variables comparten el mismo objeto
interno. La implementación sí los comparte —por eso funciona la copia al escribir de la clase 090—
pero el lenguaje no lo expone.

La excepción son los objetos TclOO, que **son comandos**, así que su identidad es su nombre:

```tcl
set a [Persona new]
set b $a
expr {$a eq $b}          ;# 1: el mismo comando, el mismo objeto
```

Ese diseño —**la identidad de un objeto es el nombre de su comando**— es coherente con el resto del
lenguaje y tiene un efecto práctico: un objeto se puede pasar como cadena, guardar en un fichero de
configuración y recuperar, siempre que siga existiendo.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;
my ($a, $b) = split ' ', $linea;

print "iguales=", ($a == $b ? 'true' : 'false'), "\n";
```

**Lo que esta clase enseña en Perl.** Perl tiene **dos juegos completos de operadores de
comparación**, uno numérico y otro de cadenas, y confundirlos es el error clásico del lenguaje:

| | Numérico | Cadena |
|---|---|---|
| igual | `==` | `eq` |
| distinto | `!=` | `ne` |
| menor | `<` | `lt` |
| ordenar | `<=>` | `cmp` |

La razón es la misma que en Tcl: **un escalar de Perl no tiene tipo**, así que el operador es quien
decide cómo interpretarlo.

```perl
"10" == "10.0"      # cierto: mismo número
"10" eq "10.0"      # falso: cadenas distintas
"abc" == "def"      # ¡CIERTO! ambos valen 0 como números
```

Esa última línea es el error que `use warnings` existe para avisar —"Argument isn't numeric"— y es la
razón de que esa directiva sea obligatoria en cualquier código serio.

`<=>` y `cmp` devuelven −1, 0 o 1, y son lo que se pasa a `sort`:

```perl
sort { $a <=> $b } @numeros;      # ORDEN NUMÉRICO
sort @numeros;                     # orden de CADENA: 10 antes que 9
```

Ese `sort` sin bloque, que ordena como texto, es otro clásico de las listas de errores frecuentes.

Y para la identidad, Perl compara **referencias**:

```perl
$ref1 == $ref2                              # ¿la misma estructura? -- las referencias
                                             #  se numerizan a su dirección
Scalar::Util::refaddr($ref)                  # la dirección, explícitamente
$obj1->isa('Persona')                        # el tipo
```

Comparar dos referencias con `==` funciona porque una referencia en contexto numérico da su
dirección. Es un detalle de implementación que se convirtió en idioma, y `refaddr` de `Scalar::Util`
es la forma limpia de escribirlo.

Para igualdad estructural profunda, CPAN tiene `Data::Compare` y, en pruebas, `Test::Deep` —que
además explica **en qué difieren** dos estructuras, algo que un simple booleano no da.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>

int main() {
    int a{}, b{};
    if (!(std::cin >> a >> b)) return 1;

    std::cout << "iguales=" << (a == b ? "true" : "false") << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** C++ distingue valor e identidad de la forma más explícita posible,
porque **la referencia y el puntero son visibles en el tipo**:

```cpp
a == b            // VALOR
&a == &b          // IDENTIDAD: la misma dirección
p == q            // punteros: ¿apuntan al mismo sitio?
*p == *q          // ¿los objetos apuntados son iguales?
```

Y hay una trampa que ha causado incontables errores, y que se hereda de C:

```cpp
const char* s = "hola";
if (s == "hola") { ... }      // compara PUNTEROS, no texto -- puede ser cierto por azar
std::string t = "hola";
if (t == "hola") { ... }      // compara CONTENIDO -- correcto
```

Con `const char*`, `==` compara direcciones. Que a veces funcione —porque el compilador une los
literales iguales— lo hace peor: el error aparece cuando una de las cadenas viene de otro sitio.

C++20 reformó la comparación con el **operador de tres vías**:

```cpp
struct Punto {
    int x, y;
    auto operator<=>(const Punto&) const = default;    // genera <, >, <=, >=
    bool operator==(const Punto&) const = default;      // y == , != aparte
};
```

Tres cosas cambiaron y las tres son mejoras reales:

1. **`= default`** genera la comparación campo a campo, sin escribirla.
2. **El compilador sintetiza `!=` a partir de `==`**, y `>`, `<=`, `>=` a partir de `<=>`. Antes había
   que escribir los seis, y era habitual que alguno fuera incoherente.
3. **La comparación es simétrica**: `a == b` y `b == a` usan el mismo operador, lo que antes exigía
   declararlo como función libre.

`<=>` devuelve además una categoría —`strong_ordering`, `weak_ordering`, `partial_ordering`— que
**documenta en el tipo qué clase de orden es**. `partial_ordering` es la de los flotantes, porque
`NaN` no es comparable con nada: ni menor, ni mayor, ni igual. Es la única biblioteca estándar de esta
página que hace explícita esa distinción matemática.

Y para los conjuntos y mapas, la regla del cierre: **si redefines `==`, especializa `std::hash`**.

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

dcl-pi IGUALES;
  a int(10) const;
  b int(10) const;
end-pi;

dcl-s r varchar(5);

if a = b;
  r = 'true';
else;
  r = 'false';
endif;

dsply ('iguales=' + r);

*inlr = *on;
return;
```

**Lo que esta clase enseña en RPG.** RPG usa **`=` para todo** —no tiene `==`— y comparte con COBOL la
regla que define a los lenguajes de campos fijos: **la comparación de caracteres rellena con espacios
por la derecha**.

```rpgle
dcl-s nombre char(20) inz('ADA');
if nombre = 'ADA';           // CIERTO: se rellena el literal
```

Y con `varchar`, la comparación es por longitud real, así que **un `char(20)` con 'ADA' y un
`varchar(20)` con 'ADA' son iguales** — RPG rellena el corto para comparar. Es coherente y hay que
saberlo al mezclar los dos tipos.

Hay una peculiaridad de RPG que conviene conocer, porque es la única de esta página: **el orden de
comparación de caracteres es el de EBCDIC**, no el de ASCII.

```text
ASCII:  0-9  <  A-Z  <  a-z
EBCDIC: a-z  <  A-Z  <  0-9
```

**Los dígitos van DESPUÉS de las letras en EBCDIC**, al revés que en ASCII. Un fichero de códigos
ordenado en IBM i y otro ordenado en Linux salen en órdenes distintos, y eso es una fuente real de
problemas al integrar sistemas: los informes no cuadran, las comparaciones de rango fallan y las
uniones de ficheros ordenados producen basura.

Es un detalle que parece anecdótico y que ha costado muchas horas de depuración en proyectos de
migración. La solución habitual es ordenar siempre en el mismo lado, o usar una tabla de traducción
explícita.

RPG añade también las **funciones de comparación de fechas**, que son mejores que las de la mayoría de
los lenguajes de esta página:

```rpgle
if fecha1 = fecha2;                      // los tipos date se comparan directamente
dias = %diff(fecha1 : fecha2 : *days);   // diferencia con unidad explícita
```

`date`, `time` y `timestamp` son **tipos del lenguaje** desde los años noventa, con aritmética y
comparación propias. Es más de lo que tiene C++ sin `<chrono>` y más de lo que tuvo Java hasta 2014.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 iguales: procedure options(main);

    declare (a, b) fixed binary(31);
    declare r char(5) varying;

    get list (a, b);

    if a = b then r = 'true';
    else r = 'false';

    put skip list ('iguales=' || r);

 end iguales;
```

**Lo que esta clase enseña en PL/I.** PL/I usa **`=` tanto para comparar como para asignar**, y
distingue por posición:

```pli
 a = b;              /* ASIGNACIÓN */
 if a = b then ...   /* COMPARACIÓN */
 c = a = b;          /* asigna a c el RESULTADO BOOLEANO de comparar a con b */
```

Esa tercera línea es legal y es célebre por lo confusa que resulta. C resolvió lo mismo separando `=`
de `==`, a costa de crear el error más frecuente de su historia —`if (a = b)`—, que PL/I no puede
cometer porque `if` exige una expresión booleana... salvo que la asignación produzca una.

La comparación de PL/I tiene una propiedad que viene de su ambición de unificar Fortran y COBOL:
**convierte los operandos a un tipo común antes de comparar**, con reglas detalladas.

```pli
 declare a fixed decimal(5,2) initial(12.50);
 declare b float binary(21)   initial(12.5);
 if a = b then ...      /* CIERTO: se convierten a un tipo común */

 declare c char(5) initial('12');
 if c = 12 then ...      /* CIERTO: la cadena se convierte a número */
```

Esa última conversión automática de cadena a número es exactamente lo que hacen Perl y Tcl, y por la
misma razón —comodidad— con el mismo riesgo. La diferencia es que PL/I lo hace con **reglas de
conversión especificadas hasta el último detalle** en el estándar, ocupando decenas de páginas.

Esa exhaustividad es marca de la casa y es parte de por qué escribir un compilador de PL/I completo
llevaba años.

Y para cadenas, PL/I comparte la regla de COBOL: **el operando corto se rellena con espacios**. Con
`varying` (clase 093), en cambio, la longitud cuenta:

```pli
 declare v char(10) varying initial('ADA');
 if v = 'ADA' then ...      /* CIERTO */
 if length(v) = 3 then ...  /* CIERTO: la longitud REAL es 3 */
```

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
IGUALES ; Igualdad e identidad -- clase 101
 read linea
 set a = $piece(linea, " ", 1)
 set b = $piece(linea, " ", 2)
 set r = "false"
 if a = b set r = "true"
 write "iguales=", r, !
 quit
```

**Lo que esta clase enseña en M.** M tiene **dos operadores de igualdad y ninguna identidad**, y las
reglas son de las más peculiares de esta página.

```mumps
 if a = b        ; comparación de CADENAS -- siempre
 if a '= b       ; distinto (la comilla simple es la NEGACIÓN)
```

**`=` en M compara SIEMPRE como cadena**, y eso produce el resultado que sorprende a todo el mundo:

```mumps
 if 1 = 1.0        ; FALSO -- "1" y "1.0" son cadenas distintas
 if 1 + 0 = 1.0 + 0 ; CIERTO -- la suma canoniza los dos a "1"
 if 007 = 7        ; FALSO
 if +007 = +7      ; CIERTO -- el + unario fuerza interpretación numérica
```

El idioma **`+x`** —un más unario delante— es la forma canónica de forzar comparación numérica en M, y
aparece constantemente en código real. Es lo contrario de Perl y Tcl, que comparan como número por
defecto y necesitan un operador aparte para el texto.

Y M tiene un operador de comparación que no tiene ningún otro lenguaje de esta página: **el operador
de contención**.

```mumps
 if "abcdef" [ "cde"     ; ¿CONTIENE la subcadena?
 if "abc" ] "abd"        ; ¿SIGUE en orden alfabético?
 if "abc" ]] "abd"       ; comparación de ordenación estándar de M
```

**`[`** es "contiene", **`]`** es "sigue a" y **`]]`** es la comparación por el orden de recorrido de
`$order` — numéricos primero, después alfabéticos. Que la contención de subcadenas sea un **operador
del lenguaje** y no una función es único de M, y refleja otra vez su origen: manipular texto médico
con la mínima cantidad de caracteres posible.

De identidad no hay nada que decir, porque **no hay objetos ni referencias**: `set a = b` copia el
valor, y no existe forma de que dos nombres designen la misma cosa. Es el modelo más simple posible, y
es la otra cara de no tener estructuras compartidas: **en M nunca hay que preguntarse si una
modificación afectará a otra variable**, que es exactamente el problema de la clase 102.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| partes a b r |

partes := stdin nextLine substrings collect: [ :cada | cada asNumber ].
a := partes first.
b := partes second.

r := a = b ifTrue: [ 'true' ] ifFalse: [ 'false' ].

Transcript show: 'iguales=', r; cr.
```

**Lo que esta clase enseña en Smalltalk.** Smalltalk resuelve esta clase con la distinción más limpia
de toda la página, y la escribe con **un solo carácter de diferencia**:

```smalltalk
a = b        "IGUALDAD: ¿tienen el mismo valor?"
a == b       "IDENTIDAD: ¿son el MISMO objeto?"
a ~= b       "no iguales"
a ~~ b       "no idénticos"
```

Y lo importante: **`=` es un mensaje**, no un operador del lenguaje. Su implementación por defecto en
`Object` es `^self == anObject` —identidad—, y **cada clase decide si redefinirla**.

```smalltalk
'hola' = 'hola'      "true:  String redefine = para comparar contenido"
'hola' == 'hola'     "false: son dos objetos distintos"
#hola == #hola       "true:  los símbolos están internados (clase 093)"
3 = 3.0              "true:  Number compara valor numérico"
3 == 3.0             "false"
```

De ahí sale el contrato que hoy se enseña en Java, C++, Python y Rust, y que **empezó aquí**:

> Si redefines `=`, **debes** redefinir `hash`, de modo que `a = b` implique `a hash = b hash`.

Sin eso, el objeto se pierde dentro de un `Set` o un `Dictionary` (clase 094): se busca en la cubeta
equivocada y no aparece, unas veces sí y otras no. Es el mismo error que en Java con
`equals`/`hashCode`, y viene del mismo sitio.

Smalltalk ofrece además las colecciones que usan una u otra:

```smalltalk
Set new                  "usa ="
IdentitySet new           "usa =="
Dictionary new            "usa ="
IdentityDictionary new    "usa =="
```

Que la elección esté **en el nombre de la clase** es más honesto que un parámetro escondido, y evita
el problema de Lisp de tener que recordar el `:test` correcto.

Y `a = b ifTrue: [...] ifFalse: [...]` recuerda la lección de la clase 062: **el condicional también
es un mensaje**, enviado al booleano resultante. No hay `if` en el lenguaje.

---

## Y de vuelta a la clase

Lo transferible: **la igualdad no es una propiedad del lenguaje, es una decisión de diseño de cada
tipo**, y hay que tomarla explícitamente. Dos fechas con la misma marca temporal en zonas distintas,
¿son iguales? Dos clientes con el mismo NIF pero distinto nombre, ¿son el mismo? Cuando redefinas la
igualdad, respeta el contrato —reflexiva, simétrica, transitiva— y **redefine también la función
hash**, porque los conjuntos y diccionarios dependen de que ambas coincidan. Ese contrato es el mismo
en Smalltalk, Java, C++, Python y Rust, y viene del primero.

⏮️ [Volver a la clase 101](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
