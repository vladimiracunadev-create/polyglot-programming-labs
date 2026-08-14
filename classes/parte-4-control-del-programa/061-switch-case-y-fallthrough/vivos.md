# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 061

> [⬅️ Volver a la clase 061](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Traducir un número del 1 al 7 al nombre de un día. El `switch` de toda la vida, y con él la pregunta
que ha costado más errores en la historia de C: **¿qué pasa si olvidas el `break`?** Los lenguajes de
esta página responden casi todos lo mismo —**no pasa nada, porque el paso a la siguiente rama no
existe**— y saber que C es la excepción, y no la regla, cambia cómo se lee.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es la **selección múltiple**, y estos lenguajes lo enseñan porque **ninguno tiene
> *fallthrough*** y varios ofrecen bastante más que un `switch`. El `EVALUATE` de COBOL admite rangos
> `THRU`, comodines `ANY` y **varios sujetos a la vez**. El `case` de Ada **obliga a cubrir todos los
> valores del tipo** y no compila si falta uno. El `select case` de Fortran y el `case` de Pascal
> aceptan rangos.
>
> Y **Smalltalk no tiene `switch` en absoluto**, deliberadamente: su respuesta es un diccionario o
> polimorfismo, que es la refactorización que hoy recomienda cualquier guía de diseño.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: un entero `d` (día) → stdout: `dia=<nombre>` o `dia=invalido`
- **Regla:** `1→lunes … 7→domingo; otro→invalido`

| stdin | esperado |
|---|---|
| `1` | `dia=lunes` |
| `6` | `dia=sabado` |
| `8` | `dia=invalido` |

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
PROGRAM-ID. DIAS.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA    PIC X(80).
01  D        PIC S9(9) COMP-3.
01  NOMBRE   PIC X(10).

PROCEDURE DIVISION.
    ACCEPT LINEA
    MOVE FUNCTION NUMVAL(LINEA) TO D

    EVALUATE D
        WHEN 1      MOVE "lunes"     TO NOMBRE
        WHEN 2      MOVE "martes"    TO NOMBRE
        WHEN 3      MOVE "miercoles" TO NOMBRE
        WHEN 4      MOVE "jueves"    TO NOMBRE
        WHEN 5      MOVE "viernes"   TO NOMBRE
        WHEN 6      MOVE "sabado"    TO NOMBRE
        WHEN 7      MOVE "domingo"   TO NOMBRE
        WHEN OTHER  MOVE "invalido"  TO NOMBRE
    END-EVALUATE

    DISPLAY "dia=" FUNCTION TRIM(NOMBRE)
    STOP RUN.
```

**Lo que esta clase enseña en COBOL.** **`EVALUATE` no tiene *fallthrough*.** Ejecuta la rama que
casa y sale; no hace falta `break` y no se puede olvidar. Ese solo hecho elimina una familia entera de
errores que en C hay que vigilar con avisos del compilador.

Y `EVALUATE` es considerablemente más potente que un `switch`. Además del `EVALUATE TRUE` de la clase
058, admite:

```cobol
EVALUATE D
    WHEN 1 THRU 5              MOVE "laborable" TO TIPO    *> RANGOS
    WHEN 6 ALSO 7              ...                          *> varios valores
END-EVALUATE

EVALUATE TIPO ALSO IMPORTE ALSO TRUE
    WHEN "VIP" ALSO 1000 THRU 9999 ALSO URGENTE  PERFORM EXPRES
    WHEN "VIP" ALSO ANY            ALSO ANY      PERFORM NORMAL
    WHEN ANY   ALSO 0 THRU 99      ALSO ANY      PERFORM RECOGIDA
    WHEN OTHER                                   PERFORM REVISAR
END-EVALUATE
```

Ese segundo bloque es una **tabla de decisión** con tres dimensiones: rangos con `THRU`, comodines con
`ANY` y sujetos combinados con `ALSO`. Es lo más cercano a la coincidencia de patrones moderna que
existía en 1985, y sigue sin tener equivalente directo en Java o C#.

Su origen es revelador: las **tablas de decisión** eran una técnica formal de análisis de negocio de
los años 60 —filas de condiciones, columnas de casos— y `EVALUATE` se diseñó para poder escribirlas
tal cual en el programa. El lenguaje copió la herramienta que ya usaban los analistas.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program dias
   implicit none
   integer :: d
   character(len=10) :: nombre

   read(*, *) d

   select case (d)
   case (1)
      nombre = 'lunes'
   case (2)
      nombre = 'martes'
   case (3)
      nombre = 'miercoles'
   case (4)
      nombre = 'jueves'
   case (5)
      nombre = 'viernes'
   case (6)
      nombre = 'sabado'
   case (7)
      nombre = 'domingo'
   case default
      nombre = 'invalido'
   end select

   write(*, '(A,A)') 'dia=', trim(nombre)
end program dias
```

**Lo que esta clase enseña en Fortran.** `select case` llegó con **Fortran 90** y sustituyó a algo
mucho peor: el **`GO TO` calculado**, que era la forma de hacer una selección múltiple en el Fortran
clásico.

```fortran
      GO TO (10, 20, 30, 40, 50, 60, 70), D     ! salta a la etiqueta D-ésima
   10 NOMBRE = 'lunes'
      GO TO 99
   20 NOMBRE = 'martes'
      GO TO 99
```

Una lista de etiquetas y un índice. Es literalmente una **tabla de saltos** escrita a mano — que es
exactamente lo que el compilador de C genera para un `switch`, y de donde viene el *fallthrough*: si
olvidabas el `GO TO 99`, caías en la etiqueta siguiente. **El paso a la siguiente rama no es una
característica de diseño, es el comportamiento por defecto de una tabla de saltos.** C lo conservó;
Fortran lo eliminó al pasar a `select case`.

Y `select case` de Fortran acepta **rangos y listas**, cosa que el de C nunca ha tenido:

```fortran
case (1:5)          ! del 1 al 5
case (6, 7)         ! lista de valores
case (:0)           ! todo lo menor o igual que 0
case (100:)         ! todo lo mayor o igual que 100
```

Sin *fallthrough* y con rangos, el `select case` cubre los casos por los que en C se abusaba de la
caída entre ramas.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Dias is
   D : Integer;
begin
   Get (D);

   case D is
      when 1      => Put_Line ("dia=lunes");
      when 2      => Put_Line ("dia=martes");
      when 3      => Put_Line ("dia=miercoles");
      when 4      => Put_Line ("dia=jueves");
      when 5      => Put_Line ("dia=viernes");
      when 6      => Put_Line ("dia=sabado");
      when 7      => Put_Line ("dia=domingo");
      when others => Put_Line ("dia=invalido");
   end case;
end Dias;
```

**Lo que esta clase enseña en Ada.** **El `case` de Ada obliga a cubrir todos los valores posibles del
tipo, y si falta alguno no compila.** Aquí el `when others` es obligatorio porque `D` es un `Integer`
y sus valores son millones. Pero con un enumerado, la garantía se vuelve muy valiosa:

```ada
type Dia is (Lunes, Martes, Miercoles, Jueves, Viernes, Sabado, Domingo);

case Hoy is
   when Lunes .. Viernes => Put_Line ("laborable");
   when Sabado           => Put_Line ("sábado");
   --  falta Domingo:  ERROR DE COMPILACIÓN
end case;
```

Y esto es lo importante: **el día que añadas `Festivo` al enumerado, el compilador te llevará a todos
los `case` del sistema donde falte tratarlo**. No hay que buscarlos; salen solos. Es la mejor
herramienta de refactorización que da un sistema de tipos, y es la razón de que las guías de Ada
desaconsejen `when others` con enumerados: al ponerlo, renuncias a la comprobación.

Es exactamente lo que hoy ofrecen `match` de Rust, `when` de Kotlin y los `sealed` de Java, y Ada lo
tenía en 1983.

El `case` de Ada admite además rangos (`when 1 .. 5`), listas alternativas (`when Sabado | Domingo`)
y —desde Ada 2012— existe también como **expresión**, con `(case X is when ... => valor)`, que enlaza
con la clase 060. Y no tiene *fallthrough*: cada rama termina donde empieza la siguiente.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Dias;
{$MODE OBJFPC}{$H+}

var
  D: Integer;
  Nombre: string;

begin
  Read(D);

  case D of
    1: Nombre := 'lunes';
    2: Nombre := 'martes';
    3: Nombre := 'miercoles';
    4: Nombre := 'jueves';
    5: Nombre := 'viernes';
    6: Nombre := 'sabado';
    7: Nombre := 'domingo';
  else
    Nombre := 'invalido';
  end;

  WriteLn('dia=', Nombre);
end.
```

**Lo que esta clase enseña en Pascal.** El `case` de Pascal **no tiene *fallthrough*** y acepta
**rangos y listas** desde 1970, treinta años antes de que C# los incorporara:

```pascal
case C of
  'a'..'z', 'A'..'Z': Tipo := 'letra';      { rangos Y lista, juntos }
  '0'..'9':           Tipo := 'digito';
  ' ', #9, #10, #13:  Tipo := 'espacio';
else
  Tipo := 'otro';
end;
```

La restricción es que **el selector tiene que ser un tipo ordinal** —entero, carácter, booleano,
enumerado o subrango— y las etiquetas, **constantes conocidas al compilar**. No se puede hacer `case`
sobre una cadena ni sobre expresiones. Esa limitación viene de la implementación: un `case` sobre
ordinales compila a una tabla de saltos directa, sin comparaciones.

Free Pascal y Delphi levantaron parte de esa restricción y admiten `case` sobre `string`, aunque
entonces el compilador genera comparaciones o una búsqueda binaria.

Fíjate también en el `else` sin `;` delante y en el `end` que cierra el `case`: es la misma regla de
separador de la clase 059, aplicada aquí. Y en Pascal el `case` **no exige exhaustividad**: si ningún
caso encaja y no hay `else`, el comportamiento en el ISO es indefinido, mientras que Free Pascal
simplemente no hace nada. Es la diferencia con Ada, y la razón de poner siempre el `else`.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let ((d (read)))
  (format t "dia=~A~%"
          (case d
            (1 "lunes")
            (2 "martes")
            (3 "miercoles")
            (4 "jueves")
            (5 "viernes")
            (6 "sabado")
            (7 "domingo")
            (otherwise "invalido"))))
```

**Lo que esta clase enseña en Common Lisp.** `case` compara con `eql` —identidad para números,
caracteres y símbolos— y **devuelve un valor**, así que se puede usar directamente como argumento,
como en este programa. Sin *fallthrough*, sin `break` y sin variable temporal.

Lisp tiene además **una familia entera** de construcciones de selección, cada una comparando de una
forma distinta, y elegir la correcta es parte del oficio:

| Construcción | Compara con | Para qué |
|---|---|---|
| `case` | `eql` | Números, caracteres, símbolos |
| `ccase` / `ecase` | `eql` | Igual, pero **error si no encaja** (`e` = *error*) |
| `typecase` | El **tipo** del valor | Despacho por tipo |
| `cond` | Condiciones arbitrarias | Cadena de guardas |

`ecase` es la que merece atención: es idéntica a `case` pero **señala un error si ningún caso
encaja**, en vez de devolver `nil` en silencio. Es la exhaustividad de Ada trasladada al tiempo de
ejecución, y la comunidad recomienda usarla siempre que los casos deban ser exhaustivos — porque un
`nil` silencioso se propaga y el error aparece lejos del sitio donde estaba.

`typecase` no tiene equivalente en la mayoría del núcleo: selecciona según el **tipo** del valor, y
como el sistema de tipos de Lisp incluye rangos (`(integer 0 100)`) y uniones (`(or null string)`),
resulta ser una coincidencia de patrones sobre tipos bastante expresiva.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea
set d [string trim $linea]

switch -- $d {
    1 { set nombre lunes }
    2 { set nombre martes }
    3 { set nombre miercoles }
    4 { set nombre jueves }
    5 { set nombre viernes }
    6 { set nombre sabado }
    7 { set nombre domingo }
    default { set nombre invalido }
}

puts "dia=$nombre"
```

**Lo que esta clase enseña en Tcl.** El `--` de `switch -- $d` no es decoración: **marca el final de
las opciones**. Sin él, si `$d` empezara por guion, `switch` lo interpretaría como una opción y
fallaría. Es una convención que recorre todo Tcl y todo Unix, y omitirla es una vulnerabilidad
clásica cuando el valor viene de fuera.

Y `switch` en Tcl es **cuatro construcciones en una**, según la opción que se le pase:

```tcl
switch -exact -- $x { ... }     ;# comparación literal (por defecto)
switch -glob  -- $x {
    "*.txt"  { ... }            ;# patrones de nombre de fichero
    "img_*"  { ... }
}
switch -regexp -- $x {
    {^[0-9]+$}     { ... }      ;# EXPRESIONES REGULARES
    {^[a-z]+@}     { ... }
}
```

Con `-regexp`, `switch` se convierte en **coincidencia de patrones de verdad** —tema de la clase
062—, con captura de grupos incluida mediante `-matchvar`. Es bastante más de lo que ofrece un
`switch` de C.

Y sí tiene una forma de *fallthrough*, pero **explícita**: un cuerpo que consista únicamente en un
guion `-` significa "usa el del siguiente caso".

```tcl
switch -- $d {
    6 -
    7 { set tipo finde }        ;# 6 y 7 comparten cuerpo
    default { set tipo laborable }
}
```

Compartir cuerpo sin poder caer por accidente: el caso legítimo del *fallthrough*, resuelto sin su
peligro.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my @dias = qw(lunes martes miercoles jueves viernes sabado domingo);

my $d = <STDIN>;
chomp $d;

my $nombre = ($d >= 1 && $d <= 7) ? $dias[$d - 1] : 'invalido';

print "dia=$nombre\n";
```

**Lo que esta clase enseña en Perl.** **Perl no tiene `switch`**, y su historia es la mejor
advertencia de esta clase. Perl 5.10 introdujo `given`/`when` como característica experimental; nunca
se estabilizó, sus reglas de *coincidencia inteligente* resultaron impredecibles, y acabó **retirada
del lenguaje**.

La respuesta idiomática es la de este programa: **una estructura de datos en lugar de una
construcción de control**.

```perl
my @dias = qw(lunes martes miercoles jueves viernes sabado domingo);
my $nombre = $dias[$d - 1] // 'invalido';

# O con un hash, cuando las claves no son consecutivas:
my %accion = (
    alta  => \&dar_alta,
    baja  => \&dar_baja,
    mod   => \&modificar,
);
my $f = $accion{$comando} // \&desconocido;
$f->(@args);
```

Ese segundo bloque es una **tabla de despacho**: un hash de nombre a **referencia a función**. Añadir
un comando es añadir una entrada, no tocar un `switch`. Es la misma técnica que en Tcl, en Smalltalk
y en C++ con `std::map`, y escala mucho mejor que cualquier construcción de selección: se puede
construir en ejecución, cargar de un fichero de configuración o extender desde un plugin.

`qw(...)` es la lista de palabras sin comillas ni comas, un atajo muy usado. Y `//` es el operador de
coalescencia de nulos de la clase 053.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>

int main() {
    int d{};
    if (!(std::cin >> d)) return 1;

    const char* nombre = nullptr;
    switch (d) {
        case 1: nombre = "lunes";     break;
        case 2: nombre = "martes";    break;
        case 3: nombre = "miercoles"; break;
        case 4: nombre = "jueves";    break;
        case 5: nombre = "viernes";   break;
        case 6: nombre = "sabado";    break;
        case 7: nombre = "domingo";   break;
        default: nombre = "invalido"; break;
    }

    std::cout << "dia=" << nombre << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** C++ es **el único lenguaje de esta página con *fallthrough***, y
esta clase es el sitio para entender por qué. El `switch` de C no es una selección: es una **tabla de
saltos con etiquetas**. `case 3:` es literalmente una etiqueta, el `switch` salta a ella, y a partir
de ahí **la ejecución continúa hacia abajo** hasta encontrar un `break`. La caída no es una
característica que alguien diseñara: es lo que ocurre si no saltas fuera.

De ahí vienen dos cosas. La primera, el error de olvidar un `break`, que los compiladores detectan
hoy con `-Wimplicit-fallthrough`. La segunda, el **Duff's device**, esa pieza legendaria en la que un
`switch` y un `while` se entrelazan aprovechando la caída — legal, ingeniosa y absolutamente
ilegible.

C++17 añadió el atributo que separa la caída intencionada del descuido:

```cpp
switch (x) {
    case 1:
        preparar();
        [[fallthrough]];      // "esto es a propósito", y el compilador calla
    case 2:
        ejecutar();
        break;
}
```

También añadió el inicializador en el `switch` —`switch (auto v = f(); v)`— y, sobre todo, hay que
recordar la restricción de fondo: **el selector debe ser un tipo entero o enumerado**. No se puede
hacer `switch` sobre `std::string`. Para eso, la solución es la de Perl y Tcl: un `std::map` de
cadena a función, es decir, una tabla de despacho.

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

dcl-pi DIAS;
  d int(10) const;
end-pi;

dcl-s nombres varchar(10) dim(7);
dcl-s nombre  varchar(10);
dcl-s salida  char(30);

nombres(1) = 'lunes';
nombres(2) = 'martes';
nombres(3) = 'miercoles';
nombres(4) = 'jueves';
nombres(5) = 'viernes';
nombres(6) = 'sabado';
nombres(7) = 'domingo';

if d >= 1 and d <= 7;
  nombre = nombres(d);
else;
  nombre = 'invalido';
endif;

salida = 'dia=' + nombre;
dsply salida;

*inlr = *on;
return;
```

**Lo que esta clase enseña en RPG.** RPG tiene `select`/`when`, sin *fallthrough*, pero para una
correspondencia número→nombre lo idiomático es una **matriz**, como en este programa. Y RPG tiene una
forma de rellenarla que no existe en ningún otro lenguaje de esta página: los **datos en tiempo de
compilación**.

```rpgle
dcl-s nombres char(10) dim(7) ctdata perrcd(1);
...
**CTDATA nombres
lunes
martes
miercoles
jueves
viernes
sabado
domingo
```

`ctdata` indica que la matriz se rellena con datos escritos **al final del propio fuente**, tras la
marca `**CTDATA`. El compilador los incrusta en el programa. Es una tabla de datos que vive en el
código, versionada con él, sin fichero externo ni código de inicialización.

Existe también `altseq` y `ftrans` para tablas de traducción de caracteres, y `dcl-s ... extfmt` para
leerlas de un fichero. Toda esa maquinaria responde a una necesidad muy concreta del dominio:
**catálogos pequeños y estables** —códigos de país, tipos de movimiento, literales por idioma— que
cambian una vez al año y no merecen una tabla en la base de datos.

Es una solución de 1969 al problema que hoy se resuelve con un fichero de recursos o un JSON
incrustado.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 dias: procedure options(main);

    declare d      fixed binary(31);
    declare nombre character(10) varying;

    get list (d);

    select (d);
       when (1) nombre = 'lunes';
       when (2) nombre = 'martes';
       when (3) nombre = 'miercoles';
       when (4) nombre = 'jueves';
       when (5) nombre = 'viernes';
       when (6) nombre = 'sabado';
       when (7) nombre = 'domingo';
       otherwise nombre = 'invalido';
    end;

    put skip list ('dia=' || nombre);

 end dias;
```

**Lo que esta clase enseña en PL/I.** `select (expresión)` compara contra los valores de cada `when`
y **no tiene *fallthrough***. Es la misma construcción que ya vimos sin expresión en la clase 058:
**una sola forma sintáctica cubre el `switch` clásico y la cadena de guardas**, según lleve o no
expresión.

Esa unificación es elegante y es exactamente lo que después hicieron Ada con `case`, Rust con `match`
y Kotlin con `when`. PL/I llegó primero.

Y `when` admite **varios valores separados por comas**, lo que cubre el caso legítimo del
*fallthrough* sin su peligro:

```pli
select (d);
   when (6, 7)         tipo = 'finde';
   when (1, 2, 3, 4, 5) tipo = 'laborable';
   otherwise            tipo = 'invalido';
end;
```

Lo que PL/I **no** tiene son rangos en el `when` —nada de `1 THRU 5` como COBOL ni `1:5` como
Fortran—, así que para tramos hay que volver al `select;` sin expresión con condiciones completas.

Y si ningún `when` casa y no hay `otherwise`, PL/I levanta la condición **`ERROR`**. Como el
`$select` de M y el `ecase` de Lisp: la ausencia de caso por defecto se trata como un fallo del
programador, no como un resultado válido.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
DIAS ; Dias de la semana -- clase 061
 read d
 set nombres = "lunes^martes^miercoles^jueves^viernes^sabado^domingo"
 set nombre = $select(d<1 : "invalido", d>7 : "invalido", 1 : $piece(nombres, "^", d))
 write "dia=", nombre, !
 quit
```

**Lo que esta clase enseña en M.** **M no tiene `switch`**, y su respuesta es la más característica
del lenguaje: **la tabla es una cadena con delimitadores, y `$piece` es la selección**.

`$piece("lunes^martes^...", "^", d)` devuelve el trozo *d*-ésimo. Una tabla de siete entradas cabe en
una línea, no ocupa memoria como estructura, se puede guardar en un *global* y se puede cambiar sin
tocar el código:

```mumps
 set ^CFG("dias") = "lunes^martes^miercoles^jueves^viernes^sabado^domingo"
 set nombre = $piece(^CFG("dias"), "^", d)     ; la tabla vive en la BASE DE DATOS
```

Esa segunda versión es cómo se hace de verdad en un sistema M: **la tabla de traducción está en la
base de datos**, así que cambiar los literales o añadir un idioma no requiere recompilar nada. Es la
misma idea que un fichero de recursos, con la ventaja de que en M la base de datos está siempre ahí.

Y para selecciones que no son consecutivas, el idioma es un array indexado por la clave:

```mumps
 set ^ACCION("alta")="DARALTA", ^ACCION("baja")="DARBAJA"
 do @$get(^ACCION(comando), "DESCONOCIDO")     ; @ = INDIRECCIÓN: ejecuta por nombre
```

El operador `@` es la **indirección**: toma una cadena y la usa como si fuera código. Es la tabla de
despacho de Perl, con el nombre de la rutina guardado como dato. Potentísimo, y la razón de que el
código M sea difícil de analizar estáticamente: **qué se ejecuta puede decidirse en ejecución**.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| d nombres nombre |

d := stdin nextLine trimBoth asNumber.
nombres := #('lunes' 'martes' 'miercoles' 'jueves' 'viernes' 'sabado' 'domingo').

nombre := (d between: 1 and: 7)
    ifTrue:  [ nombres at: d ]
    ifFalse: [ 'invalido' ].

Transcript show: 'dia=', nombre; cr.
```

**Lo que esta clase enseña en Smalltalk.** **Smalltalk no tiene `switch`, y la ausencia es
deliberada.** No es que se les olvidara: es que la comunidad considera que una selección múltiple
sobre un valor es casi siempre un síntoma de que falta polimorfismo.

Las dos respuestas idiomáticas son las de este programa y la del diccionario:

```smalltalk
"1) Indexar una colección, cuando las claves son consecutivas"
nombres at: d ifAbsent: [ 'invalido' ]

"2) Un diccionario, cuando no lo son"
acciones := Dictionary newFrom: {
    #alta -> [ self darAlta ].
    #baja -> [ self darBaja ] }.
(acciones at: comando ifAbsent: [ [ self desconocido ] ]) value.
```

El diccionario guarda **bloques**, así que es una tabla de despacho igual que el hash de referencias
a función de Perl. Se construye en ejecución, se puede modificar y se puede extender desde otro
paquete sin tocar el original.

Y la tercera respuesta, la que la comunidad considera correcta cuando el `switch` es sobre un tipo,
es **no escribir ninguna selección**:

```smalltalk
Lunes >> nombre    ^'lunes'
Sabado >> nombre   ^'sabado'
Sabado >> esFinde  ^true
Lunes >> esFinde   ^false
```

Cada clase responde por sí misma. Añadir un día nuevo es añadir una clase, no editar siete `switch`
repartidos por el sistema. Es *"reemplaza el condicional por polimorfismo"*, la refactorización que
Martin Fowler catalogó trabajando precisamente en esta comunidad.

---

## Y de vuelta a la clase

Dos ideas que llevarse. La primera: **el *fallthrough* de C es un accidente histórico**, no un
requisito de los lenguajes de selección; heredado de la implementación como tabla de saltos, ha
sobrevivido por compatibilidad, y C++17 tuvo que añadir `[[fallthrough]]` para distinguir el
intencionado del olvidado. La segunda: **la exhaustividad comprobada por el compilador —el `case` de
Ada— es una garantía enorme**, porque al añadir un valor nuevo al enumerado, el compilador te lleva a
todos los sitios donde falta tratarlo. Es lo que hoy dan `match` de Rust y `when` de Kotlin.

⏮️ [Volver a la clase 061](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
