# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 137

> [⬅️ Volver a la clase 137](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Clasificar un error por su fase. La clase 123 dio el mapa de las fases; esta lo usa para lo que
importa: **saber en qué fase falló ahorra la mitad del trabajo**. Y aquí hay dos casos extremos:
**Ada detecta en la fase de *bind* lo que C++ descubre en ejecución** (clase 123), y **M no detecta
casi nada hasta que la línea se ejecuta** — porque su código es texto que se construye en marcha.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es la **taxonomía del fallo**, y estos lenguajes la enseñan porque en ellos las fases
> están separadas y **cada una tiene su vocabulario**. Un `syntax error, unexpected AREA` de GnuCOBOL es
> del analizador (clase 100); un `not dispatching (must be defined in a package spec)` de GNAT es del
> semántico (clase 111); un `undefined reference` es del enlazador; y un `Constraint_Error` es de
> ejecución.
>
> Y muestran el eje que de verdad importa: **cuánto se detecta antes**. Ada y Fortran con módulos
> comprueban entre unidades; C y PL/I emparejan por nombre y no comprueban nada (clase 088).
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: un entero `codigo` (1 a 4) → stdout: `error=<sintaxis|tipos|enlace|ejecucion>`
- **Regla:** `1→sintaxis, 2→tipos, 3→enlace, 4→ejecucion`

| stdin | esperado |
|---|---|
| `1` | `error=sintaxis` |
| `3` | `error=enlace` |
| `4` | `error=ejecucion` |

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
PROGRAM-ID. ERRORES.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  CODIGO  PIC 9(2) COMP.
01  TIPO    PIC X(12).

PROCEDURE DIVISION.
    ACCEPT LINEA
    COMPUTE CODIGO = FUNCTION NUMVAL(LINEA)

    EVALUATE CODIGO
        WHEN 1  MOVE "sintaxis"  TO TIPO
        WHEN 2  MOVE "tipos"     TO TIPO
        WHEN 3  MOVE "enlace"    TO TIPO
        WHEN 4  MOVE "ejecucion" TO TIPO
        WHEN OTHER MOVE "?"      TO TIPO
    END-EVALUATE

    DISPLAY "error=" FUNCTION TRIM(TIPO)
    STOP RUN.
```

**Lo que esta clase enseña en COBOL.** La cadena de COBOL (clase 123) tiene **más fases que ninguna otra
de esta página**, y cada una falla con su propio vocabulario:

| Fase | Ejemplo de error | Cuándo |
|---|---|---|
| Librarian | `COPY member not found` | expansión |
| Precompilador DB2 | `DSNH104I ILLEGAL SYMBOL` | antes de compilar |
| Traductor CICS | `DFH7011I` | antes de compilar |
| **Compilador** | `IGYPS0037-S Syntax error` | análisis |
| **Enlazador** | `IEW2456E UNRESOLVED EXTERNAL` | enlace |
| **BIND de DB2** | `DSNT408I SQLCODE = -204, TABLE NOT FOUND` | **después de compilar** |
| **Ejecución** | `S0C7 data exception` | producción |

**El `BIND` es una fase que casi ningún lenguaje tiene**: el plan de acceso a la base de datos se
valida por separado, así que **una tabla que falta se detecta al hacer `BIND`, no al compilar ni al
ejecutar**.

Y **`S0C7`** merece una explicación porque es el error de ejecución más famoso del mainframe: **excepción
de datos**, y ocurre cuando una instrucción decimal recibe algo que no es un decimal empaquetado
válido.

En la práctica significa **un campo numérico con basura**, casi siempre porque el registro leído no
tenía el formato esperado (clase 106) o porque un campo no se inicializó.

Es la razón de la disciplina de `INITIALIZE` y de comprobar `FILE STATUS` tras cada operación (clase
104): **en un lenguaje sin tipos comprobados en la frontera de los datos, el error aparece al usarlos**.

Y COBOL tiene un mecanismo de diagnóstico que esta clase debe destacar y que es de los mejores de esta
página: **el listado de compilación**.

```text
OPTIONS: XREF, MAP, LIST, OFFSET, SOURCE
```

**El listado incluye el fuente expandido, una tabla de referencias cruzadas de cada nombre, el mapa de
almacenamiento con el desplazamiento de cada campo, y el ensamblador generado.** Es un documento de
decenas de páginas y responde a casi cualquier pregunta sobre qué entendió el compilador.

En una época sin depuradores interactivos, ese listado **era la herramienta de diagnóstico**, y sigue
siendo la forma de resolver un `S0C7`: buscar el desplazamiento en el mapa y ver qué campo hay ahí.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program errores
   implicit none
   integer :: codigo
   character(len=12) :: tipo

   read(*, *) codigo

   select case (codigo)
   case (1);     tipo = 'sintaxis'
   case (2);     tipo = 'tipos'
   case (3);     tipo = 'enlace'
   case (4);     tipo = 'ejecucion'
   case default; tipo = '?'
   end select

   write(*, '(A)') 'error=' // trim(tipo)
end program errores
```

**Lo que esta clase enseña en Fortran.** Fortran tiene una historia con esta clase que explica muchas
de sus decisiones modernas: **durante décadas, casi nada se comprobaba**.

El **`implicit none`** que abre todos los programas de esta serie es la prueba. Sin él, Fortran aplica
la regla implícita:

```fortran
      X = 3.14        ! X es REAL: empieza por A-H o O-Z
      I = 42           ! I es INTEGER: empieza por I-N
      LONGITUD = 10     ! ¡INTEGER! empieza por L
```

**Cualquier nombre no declarado se convierte en una variable nueva**, con el tipo según su primera
letra. Y de ahí el error más famoso de la historia de Fortran:

```fortran
      DO 10 I = 1.10        ! un PUNTO en vez de una coma
```

Eso **no es un bucle**: es una asignación a una variable llamada `DO10I` con el valor 1.10. Compilaba
sin avisar, y la leyenda —probablemente apócrifa— lo culpa de la pérdida de la sonda Mariner 1.

**`implicit none` cierra ese agujero**, y es la primera línea obligatoria de cualquier Fortran moderno.

Y las fases de Fortran fallan así:

| Fase | Ejemplo |
|---|---|
| Sintaxis | `Error: Expecting END PROGRAM statement` |
| **Semántica con módulos** | `Error: Type mismatch in argument 'x' at (1)` |
| **Semántica SIN módulos** | *silencio*: el procedimiento externo no se comprueba |
| Enlace | `undefined reference to 'calcular_'` |
| Ejecución | `Fortran runtime error: Index '11' of dimension 1 above upper bound of 10` |

**La tercera fila es la clave y ya apareció en la clase 109**: un procedimiento externo suelto **no
tiene interfaz explícita**, así que **llamarlo con argumentos de otro tipo compila y enlaza**.

Ese es el motivo real de que la recomendación número uno para modernizar Fortran sea **meter todo en
módulos**: no es organización, **es activar la comprobación**.

Y el subrayado del nombre —`calcular_`— es el *name mangling* de Fortran, que la clase 157 detallará: el
compilador añade un guion bajo, y por eso los errores de enlace con C aparecen con ese sufijo.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO; use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Errores is
   Codigo : Integer;
begin
   Get (Codigo);

   case Codigo is
      when 1      => Put_Line ("error=sintaxis");
      when 2      => Put_Line ("error=tipos");
      when 3      => Put_Line ("error=enlace");
      when 4      => Put_Line ("error=ejecucion");
      when others => Put_Line ("error=?");
   end case;
end Errores;
```

**Lo que esta clase enseña en Ada.** Ada está diseñado para que **la mayor parte de los errores caigan
en las fases tempranas**, y esta clase permite ver cuántas categorías traslada hacia arriba:

| Error | Dónde falla en C | **Dónde falla en Ada** |
|---|---|---|
| Tipo incompatible | compilación (a veces) | **compilación, siempre** |
| Unidad no recompilada | enlace o ejecución | **bind** (clase 123) |
| Orden de inicialización | ejecución | **bind** |
| Índice fuera de rango | ejecución (o nada) | **ejecución, con excepción clara** |
| Valor fuera de rango | nada | **ejecución, `Constraint_Error`** |
| Método mal redefinido | ejecución | **compilación, con `overriding`** |
| Contrato incumplido | nada | **ejecución, o DEMOSTRADO con SPARK** |

**Cada fila que sube una fila ahorra órdenes de magnitud**, que es el argumento del cierre de esta
clase.

Y los errores de ejecución de Ada tienen nombres que dicen qué pasó, no dónde:

```text
raised CONSTRAINT_ERROR : prog.adb:15 index check failed
raised STORAGE_ERROR : stack overflow
raised PROGRAM_ERROR : access before elaboration
raised TASKING_ERROR : dependent task terminated
```

**`PROGRAM_ERROR: access before elaboration`** es el que ilustra mejor esta clase: **se usó algo antes
de que su paquete se inicializara** (clase 123). En C++, ese mismo fallo es el fiasco del orden de
inicialización estática y **produce basura sin mensaje**.

Y GNAT tiene un conjunto de comprobaciones que conviene conocer porque suben más errores de fase:

```bash
gnatmake -gnatwa -gnatVa -gnato -gnata prog.adb
```

`-gnatwa` activa todos los avisos, `-gnatVa` todas las comprobaciones de validez, `-gnato` la
comprobación de desbordamiento y `-gnata` las aserciones y los contratos.

Y **`gnatprove`** cierra el cuadro (clase 118): **lo que no se puede comprobar al compilar, se
demuestra** — y lo demostrado se puede dejar de comprobar en ejecución, sin perder la garantía.

Es la única vía de esta página que permite **quitar comprobaciones sin quitar seguridad**.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Errores;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  Codigo: Integer;

begin
  Read(Codigo);

  case Codigo of
    1: WriteLn('error=sintaxis');
    2: WriteLn('error=tipos');
    3: WriteLn('error=enlace');
    4: WriteLn('error=ejecucion');
  else
    WriteLn('error=?');
  end;
end.
```

**Lo que esta clase enseña en Pascal.** Pascal fue diseñado para que **el compilador de una pasada
cazara mucho** (clase 123), y su fama entre generaciones de estudiantes viene precisamente de eso:
**avisaba de todo, a veces con exceso de celo**.

Sus errores clásicos son didácticos:

```text
Error: Identifier not found "Contador"          { declara antes de usar }
Error: Incompatible types: got "Real" expected "Integer"
Error: Illegal expression                        { falta un ; o sobra }
Fatal: Syntax error, ";" expected but "identifier" found
Warning: Variable "X" does not seem to be initialized
Note: Local variable "Y" is assigned but never used
```

**Los avisos y las notas de Free Pascal son de los más útiles de esta página**, y `-Sew` los convierte
en errores — que es la disciplina recomendada en un proyecto serio.

Y los errores de ejecución de Pascal tienen números que la comunidad conoce de memoria:

```text
Runtime error 201: Range check error       { con {$R+} }
Runtime error 215: Arithmetic overflow      { con {$Q+} }
Runtime error 216: General protection fault  { puntero inválido }
Runtime error 202: Stack overflow
Runtime error 203: Heap overflow
```

**`RTE 201` y `RTE 215` solo aparecen si las comprobaciones están activadas**, y ahí está la trampa que
esta clase debe señalar: **Free Pascal las trae DESACTIVADAS en la configuración de publicación**.

```pascal
{$R+}      { comprobación de rango }
{$Q+}       { comprobación de desbordamiento }
{$S+}        { comprobación de pila }
```

Un programa compilado sin ellas **no avisa de un índice fuera de rango: escribe donde no debe**, que es
el comportamiento de C.

Es exactamente el compromiso de las clases 089 y 124, y la recomendación práctica es la misma que en
todos los ecosistemas: **comprobaciones activadas en desarrollo y en pruebas, y decidir
conscientemente en producción**.

Y hay un detalle de Delphi que merece nombrarse: **`Assert` se elimina con `{$C-}`**, así que las
aserciones son gratis en producción — el mismo modelo que `assert` en C y `pragma Assertion_Policy` en
Ada.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let* ((codigo (read))
       (tipo (case codigo
               (1 "sintaxis")
               (2 "tipos")
               (3 "enlace")
               (4 "ejecucion")
               (t "?"))))
  (format t "error=~A~%" tipo))
```

**Lo que esta clase enseña en Common Lisp.** Lisp **desdibuja las fases de esta clase**, y de una forma
que merece explicarse: **la compilación es incremental y ocurre en cualquier momento** (clase 124).

Un error de sintaxis en Lisp **es un error del lector**, y se detecta al leer:

```text
end of file on #<STREAM> inside read     ; un paréntesis sin cerrar
```

**Ese es el error de sintaxis más común de Lisp**, y es notablemente pobre: dice que se acabó el
fichero, no dónde faltaba el paréntesis. Los editores lo compensan con el emparejamiento automático y
con la edición estructural —Paredit—, que es la razón de que la comunidad Lisp use editores tan
específicos.

Y de tipos, Lisp comprueba **en ejecución** por defecto:

```text
The value 3 is not of type STRING when binding X
```

Con una diferencia importante: **SBCL hace inferencia de tipos y avisa en compilación** cuando puede
demostrar un error:

```text
caught WARNING: Constant 3 conflicts with its asserted type STRING.
caught STYLE-WARNING: The variable X is defined but never used.
note: doing signed word to integer coercion, can't open code
```

**Esa tercera es la más útil y la más peculiar** (clase 124): **SBCL avisa de que no puede optimizar y
por qué**. Es un diálogo con el compilador que ningún otro lenguaje de esta página ofrece.

Y "enlace" en Lisp no existe como fase, y su equivalente sí:

```text
The function FOO is undefined.
```

**Una función no definida se detecta al LLAMARLA**, no al cargar. Es la máxima flexibilidad —se puede
definir después— y la mínima detección temprana.

Con la contrapartida que ya se contó en la clase 103: **ese error abre el depurador con reinicios**.

```text
Restarts:
  0: [CONTINUE] Retry calling FOO.
  1: [USE-VALUE] Call specified function.
  2: [RETURN-VALUE] Return specified values.
  3: [ABORT] Exit debugger.
```

**Se puede definir la función que falta y elegir "reintentar"**, y el programa continúa como si nada.
Es el mejor manejo de errores de ejecución de esta página, y compensa buena parte de la detección
tardía.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea
set codigo [string trim $linea]

switch -exact -- $codigo {
    1       { set tipo "sintaxis" }
    2       { set tipo "tipos" }
    3       { set tipo "enlace" }
    4       { set tipo "ejecucion" }
    default { set tipo "?" }
}

puts "error=$tipo"
```

**Lo que esta clase enseña en Tcl.** En Tcl **casi todo es un error de ejecución**, y esa es la
consecuencia directa de su modelo: **el código es texto que se analiza al ejecutarse** (clase 123).

```text
invalid command name "foo"                    ; el comando no existe: al LLAMARLO
can't read "x": no such variable               ; la variable no existe: al LEERLA
wrong # args: should be "proc a b"              ; aridad: al llamar
expected integer but got "hola"                  ; tipo: al operar
```

**No hay fase de tipos ni de enlace**, y un error de sintaxis solo se detecta **cuando se va a ejecutar
ese trozo**:

```tcl
proc nunca {} { esto { es } basura sin cerrar    ;# no falla hasta llamarla
```

Y de ahí la importancia de dos herramientas del ecosistema que esta clase debe nombrar:

**`info complete`** (clase 123), que comprueba si un texto es sintácticamente completo:

```tcl
if {[info complete $codigo]} { eval $codigo }
```

**Y los analizadores estáticos**, que en Tcl son especialmente valiosos por lo tardío de la detección:

```bash
nagelfar prog.tcl        # el analizador estático de referencia
frink prog.tcl            # formateo y comprobación
```

**Nagelfar** comprueba aridades, nombres de comando, tipos aproximados y errores de citación, y es lo
más parecido a una fase de comprobación que tiene Tcl.

Y lo que Tcl sí da, y muy bien, es la información del error de ejecución:

```tcl
catch { ... } resultado opciones
puts [dict get $opciones -errorinfo]      ;# la pila COMPLETA
puts [dict get $opciones -errorcode]       ;# un código estructurado
```

**`-errorinfo` da la traza con el texto de cada comando de la pila**, no solo nombres de función. Es
más informativo que una traza normal, porque **muestra el comando que se estaba ejecutando**.

Es el mismo principio que `$stack("MCODE")` en M (clase 127): **cuando el código es texto accesible, el
diagnóstico puede mostrarlo**.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $codigo = <STDIN>;
chomp $codigo;

my %tipos = (1 => 'sintaxis', 2 => 'tipos', 3 => 'enlace', 4 => 'ejecucion');

print "error=", ($tipos{$codigo} // '?'), "\n";
```

**Lo que esta clase enseña en Perl.** Perl **compila el programa entero antes de ejecutarlo** (clase
123), así que **sí tiene una fase de sintaxis** que caza mucho:

```bash
perl -c programa.pl        # comprobar sin ejecutar
```

Y sus errores de compilación son famosos por una razón concreta: **el mensaje suele apuntar a la línea
siguiente**.

```text
syntax error at prog.pl line 15, near "foo"
Global symbol "$x" requires explicit package name at prog.pl line 12.
Missing right curly or square bracket at prog.pl line 40, at end of line
```

**Ese último es el error más temido de Perl**: una llave sin cerrar en la línea 5 se detecta en la 40,
porque el analizador sigue leyendo hasta que se acaba el fichero. Es el mismo problema del paréntesis
de Lisp de esta página.

Y las dos directivas que convierten a Perl en un lenguaje comprobado son las de esta clase:

```perl
use strict;        # sin declarar, sin referencias simbólicas, sin barewords
use warnings;       # avisos de todo lo sospechoso
```

**`use strict` mueve una familia entera de errores de la fase de ejecución a la de compilación**: sin
él, una variable mal escrita **crea una variable nueva** (como el `implicit` de Fortran de esta
página), y el fallo aparece mucho después con un valor vacío.

Es probablemente la línea más importante de cualquier programa Perl, y su historia es instructiva:
**`strict` existe desde Perl 5.0 (1994) y no se activa por defecto por compatibilidad**. Solo desde
Perl 5.36, escribir `use v5.36;` lo activa automáticamente.

**Treinta años entre saber la solución y poder aplicarla por defecto.**

Y `use warnings` avisa de lo que el cierre de esta clase quiere cazar antes:

```text
Use of uninitialized value $x in addition
Argument "hola" isn't numeric in numeric eq (==)      # clase 101
Deep recursion on subroutine "main::f"                 # clase 127
Odd number of elements in hash assignment
```

Y el ecosistema añade la capa de análisis estático:

```bash
perlcritic --brutal prog.pl        # las reglas del libro "Perl Best Practices"
```

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>
#include <string>

int main() {
    int codigo{};
    if (!(std::cin >> codigo)) return 1;

    std::string tipo;
    switch (codigo) {
        case 1:  tipo = "sintaxis";  break;
        case 2:  tipo = "tipos";      break;
        case 3:  tipo = "enlace";      break;
        case 4:  tipo = "ejecucion";    break;
        default: tipo = "?";             break;
    }

    std::cout << "error=" << tipo << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** C++ tiene las cuatro fases muy marcadas, y **sus errores son
célebres por lo difíciles de leer**:

```text
error: expected ';' before '}' token                    # sintaxis
error: no matching function for call to 'f(int)'         # tipos, con 200 candidatos
undefined reference to `Clase::metodo()'                  # ENLACE
Segmentation fault (core dumped)                           # ejecución, sin información
```

**El error de enlace más frecuente de C++** —`undefined reference`— tiene tres causas típicas que
conviene reconocer:

1. **Se declaró un método y no se definió.**
2. **Se olvidó enlazar la biblioteca** (`-lm`, `-lpthread`).
3. **Discrepancia de nombres decorados**: el `.h` es de C y no lleva `extern "C"` (clase 157).

Y esta clase es el sitio para el problema de los mensajes de plantillas, ya mencionado en la clase 118:
**un error dentro de una plantilla produce páginas de texto** porque el compilador cuenta toda la
cadena de instanciación.

**C++20 lo alivió con los conceptos** (clase 112):

```cpp
template <std::integral T> void f(T x);
// error: constraints not satisfied: 'std::string' does not satisfy 'integral'
```

**Un error de concepto dice qué requisito falla, no dónde reventó la instanciación.** Es una de las
mejoras de usabilidad más importantes de la historia del lenguaje.

Y sobre los errores de ejecución, C++ está en el peor sitio de esta página: **el comportamiento
indefinido no produce un error, produce un programa sin significado** (clase 136).

Las herramientas son imprescindibles, y esta clase debe listarlas:

```bash
g++ -Wall -Wextra -Wpedantic -Werror     # avisos como errores
g++ -fsanitize=address,undefined          # memoria y comportamiento indefinido
g++ -fsanitize=thread                      # carreras (clase 136)
valgrind ./prog
clang-tidy prog.cpp                          # análisis estático
```

**`-fsanitize=undefined` convierte comportamiento indefinido en un mensaje con fichero y línea**, y es
lo que más se acerca a subir esos errores de fase.

Es la conclusión de esta clase en C++: **el lenguaje no detecta, y el ecosistema ha construido las
herramientas que detectan** — y usarlas no es opcional.

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

dcl-pi ERRORES;
  codigo int(10) const;
end-pi;

dcl-s tipo varchar(12);

select;
  when codigo = 1;  tipo = 'sintaxis';
  when codigo = 2;  tipo = 'tipos';
  when codigo = 3;  tipo = 'enlace';
  when codigo = 4;  tipo = 'ejecucion';
  other;            tipo = '?';
endsl;

dsply ('error=' + tipo);

*inlr = *on;
return;
```

**Lo que esta clase enseña en RPG.** Los errores de RPG llevan **códigos con prefijo que identifican la
fase**, y esa nomenclatura es sistemática en toda la plataforma:

| Prefijo | Fase |
|---|---|
| `RNF` | **compilación** de RPG (*RPG No Free*, histórico) |
| `RNS` | compilación, formato libre |
| `CPF` | **sistema operativo**: objeto no encontrado, sin autoridad |
| `MCH` | **máquina**: puntero inválido, división por cero |
| `RNQ` | **ejecución de RPG**: índice fuera de rango, error de conversión |
| `SQL` | precompilador o ejecución de SQL |

**`RNQ0121` es índice fuera de rango y `MCH3601` es puntero inválido**, y quien trabaja en la
plataforma los reconoce de memoria.

Y hay una particularidad del enlace en IBM i que ya apareció en la clase 086 y que aquí es un error de
fase propio: **la firma del programa de servicio**.

```text
CPF3EE1 - La firma del programa de servicio UTILES no coincide
```

**Eso se detecta al CARGAR el programa, no al enlazarlo ni al ejecutar la llamada.** Si alguien cambió
el orden de las exportaciones de un programa de servicio, **todos sus clientes fallan al arrancar con
un mensaje claro** — en lugar de llamar a la función equivocada.

Es una fase de comprobación que casi ningún sistema tiene, y es lo que hace segura la actualización de
bibliotecas compartidas en esa plataforma.

Y el diagnóstico de los errores de ejecución tiene una propiedad que esta clase debe destacar y que la
clase 138 desarrollará: **el registro del trabajo lo conserva todo**.

```text
DSPJOBLOG JOB(123456/USUARIO/MIAPP)
```

**Cada mensaje, con su código, su texto, su ayuda de segundo nivel, el programa y el número de
sentencia que lo provocó, y la pila de llamadas en ese momento.** Sin configurar nada y sin
instrumentar el código.

Es observabilidad por defecto, y es la razón de que diagnosticar un fallo en IBM i sea a menudo más
rápido que en un servidor moderno con registros dispersos.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 errores: procedure options(main);

    declare codigo fixed binary(31);
    declare tipo char(12) varying;

    get list (codigo);

    select (codigo);
       when (1) tipo = 'sintaxis';
       when (2) tipo = 'tipos';
       when (3) tipo = 'enlace';
       when (4) tipo = 'ejecucion';
       otherwise tipo = '?';
    end;

    put skip list ('error=' || tipo);

 end errores;
```

**Lo que esta clase enseña en PL/I.** PL/I tiene un sistema de diagnóstico de compilación que era
excepcional para su época y que sigue siendo instructivo: **los mensajes se clasifican por severidad**.

```text
I  - Informational   (nota)
W  - Warning          (aviso)
E  - Error             (error, pero compila)
S  - Severe            (grave)
U  - Unrecoverable      (no se puede continuar)
```

**Y `E` significa "hay un error y he generado código igualmente"**, con una suposición documentada. Eso
suena temerario y tenía un motivo: **en la época de las tarjetas perforadas, una compilación tardaba
horas**, así que el compilador intentaba **seguir para encontrar todos los errores de una vez** en
lugar de parar en el primero.

Esa filosofía —**recuperación de errores para diagnosticar todo en una pasada**— es la misma que hoy
tienen los compiladores modernos, y en PL/I estaba llevada al extremo de generar código.

Y PL/I tiene la característica que más se le reprocha en esta clase, ya nombrada en la clase 107: **las
conversiones implícitas**.

```pli
 declare x fixed decimal(5,2);
 declare c char(10);
 x = c;          /* convierte la cadena a número: si no lo es, CONVERSION */
```

**Casi cualquier cosa se convierte a cualquier otra**, y el error aparece en ejecución como la condición
`CONVERSION` — que, eso sí, es capturable y **permite corregir el dato y reanudar** con `onsource`
(clase 116).

Es el compromiso de PL/I entero: **máxima flexibilidad, comprobación tardía y un mecanismo de
recuperación excelente**.

Y las condiciones de PL/I son la taxonomía de errores de ejecución más detallada de esta página:

```pli
 on conversion       ...     /* dato no convertible */
 on zerodivide        ...     /* división por cero */
 on overflow           ...     /* desbordamiento */
 on subscriptrange      ...     /* índice fuera de rango (clase 089) */
 on stringrange          ...     /* subcadena fuera de rango */
 on endfile(f)            ...     /* fin de fichero */
 on key(f)                 ...     /* clave no encontrada */
 on undefinedfile(f)        ...     /* no se pudo abrir */
 on storage                  ...     /* sin memoria */
 on error                     ...     /* cualquier otra */
```

**Diez condiciones distintas para diez fallos distintos**, cada una con su manejador. Es más fino que
el `catch` de la mayoría de los lenguajes modernos, y es de 1964.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
ERRORES ; Tipos de error -- clase 137
 read codigo
 set tipo = $select(codigo=1:"sintaxis", codigo=2:"tipos", codigo=3:"enlace", codigo=4:"ejecucion", 1:"?")
 write "error=", tipo, !
 quit
```

**Lo que esta clase enseña en M.** **En M, casi todo es un error de ejecución**, y su modelo es el más
tardío de esta página, por la razón de la clase 123: **el código se puede construir con texto y
ejecutar con `xecute` o indirección**.

Los códigos de error de M están estandarizados y empiezan por `M`:

```text
M6   - Variable indefinida
M7   - Nodo de global indefinido
M9   - División por cero
M26  - Etiqueta no encontrada
M56  - Identificador demasiado largo
M57  - Etiqueta duplicada
M53  - Demasiados niveles de anidamiento
ZLINKFILE, ZSRCHSTRINCL... (extensiones $Z de cada implementación)
```

**`M6` —variable indefinida— es el error más común de M**, y es la consecuencia directa de no tener
declaraciones (clase 082): **escribir mal un nombre no es un error de compilación, es una variable que
no existe**.

Es exactamente el problema que `use strict` resuelve en Perl y `implicit none` en Fortran, y **M no
tiene equivalente**. La defensa es `$get` con valor por defecto (clase 116) y la disciplina.

Y M tiene un mecanismo de manejo de errores propio y peculiar: **`$etrap` y `$ecode`**.

```mumps
 set $etrap = "do error^UTIL quit"        ; código a ejecutar SI HAY ERROR
 set $ecode = ",M6,"                        ; el código de error actual
 write $stack($stack, "ECODE")               ; el error de un nivel de la pila
 write $zstatus                               ; texto completo (extensión)
```

**`$etrap` es una cadena de código M que se ejecuta cuando salta un error**, y su alcance es la pila:
si el nivel actual no lo maneja, sube.

Es un manejador de errores **guardado como texto en una variable especial**, coherente con todo lo
demás del lenguaje — y con la misma consecuencia: **flexible e imposible de analizar**.

Y merece cerrar con lo que M sí da y que la clase 138 desarrollará: **`$stack` con `MCODE` devuelve el
código fuente de cada nivel de la pila** (clase 127).

**Un error en M puede informar de la línea exacta de código de cada nivel**, sin depurador y sin
símbolos, porque el fuente vive en la base de datos.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| codigo tipo |

codigo := stdin nextLine trimBoth asNumber.

tipo := codigo = 1 ifTrue: [ 'sintaxis' ] ifFalse: [
        codigo = 2 ifTrue: [ 'tipos' ] ifFalse: [
        codigo = 3 ifTrue: [ 'enlace' ] ifFalse: [
        codigo = 4 ifTrue: [ 'ejecucion' ] ifFalse: [ '?' ] ] ] ].

Transcript show: 'error=', tipo; cr.
```

**Lo que esta clase enseña en Smalltalk.** Smalltalk **casi no tiene fases** (clase 123): se compila un
método cada vez, al aceptarlo, y no hay enlace.

Y eso reparte los errores así:

| Tipo | Cuándo |
|---|---|
| Sintaxis | **al aceptar el método**, en el editor, inmediatamente |
| Nombre desconocido | **al aceptar**: el editor pregunta si es una variable nueva |
| Tipos | **al enviar el mensaje**, en ejecución |
| Enlace | **no existe** |
| Método inexistente | al enviarlo: `doesNotUnderstand:` |

**La segunda fila es característica y muy buena**: al aceptar un método que usa un nombre desconocido,
**el entorno pregunta** —"¿es una variable de instancia, una temporal, una global, o lo has escrito
mal?"— y ofrece corregirlo.

Es detección temprana con diálogo, y resuelve el problema de `M6` en M y del `implicit` en Fortran de
esta misma página **preguntando en lugar de suponiendo**.

Y los errores de ejecución de Smalltalk son, con diferencia, **los mejores de esta página**, por lo que
la clase 127 explicaba: **la pila es un objeto**.

```text
MessageNotUnderstood: Persona>>#nombreCompleto
```

Y al saltar, **se abre el depurador sobre el proceso vivo**, con:

- **La pila completa**, navegable, con las variables de cada marco.
- **La posibilidad de inspeccionar y MODIFICAR cualquier valor.**
- **La opción de escribir el método que falta ahí mismo** y pulsar "reintentar".
- **Y de reanudar desde cualquier marco**, no solo desde el último.

**Ese flujo —el error abre el editor en el punto exacto, escribes lo que falta y continúas— es la
experiencia de depuración que la mayoría de los entornos no ha alcanzado en cuarenta años.**

Y merece cerrar esta clase con lo que eso implica sobre su taxonomía: **en Smalltalk, un error de
ejecución no es el final de nada**. Es una interrupción con toda la información disponible y la
posibilidad de arreglar el programa sin perder el estado.

Es exactamente lo contrario del `Segmentation fault` de C++ de esta misma página, y las dos son
consecuencias coherentes de las decisiones de la Parte 8 entera.

---

## Y de vuelta a la clase

Lo transferible: **cada fase que detecta un error ahorra órdenes de magnitud respecto a la
siguiente**. Un error de sintaxis cuesta segundos; uno de tipos, minutos; uno de enlace, una tarde; y
uno de ejecución en producción, una llamada de madrugada. Por eso los lenguajes con comprobación
fuerte piden ceremonia: **están comprando detección temprana**. Y por eso la pregunta útil ante un
fallo nuevo no es "¿cómo lo arreglo?" sino **"¿qué fase debería haberlo cazado?"**.

⏮️ [Volver a la clase 137](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
