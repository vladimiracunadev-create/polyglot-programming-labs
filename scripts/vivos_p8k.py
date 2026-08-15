# -*- coding: utf-8 -*-
"""Parte 8, lote K — clases 137 y 138. Ver `vivos_parte8.py` y `gen_vivos.py`."""

SPECS: dict[str, dict] = {}

# ---------------------------------------------------------------------------
# 137 — Errores de sintaxis, de tipos, de enlace y de ejecución
# ---------------------------------------------------------------------------
SPECS["137"] = dict(
    gancho="""
Clasificar un error por su fase. La clase 123 dio el mapa de las fases; esta lo usa para lo que
importa: **saber en qué fase falló ahorra la mitad del trabajo**. Y aquí hay dos casos extremos:
**Ada detecta en la fase de *bind* lo que C++ descubre en ejecución** (clase 123), y **M no detecta
casi nada hasta que la línea se ejecuta** — porque su código es texto que se construye en marcha.
""",
    porque="""
Aquí el concepto es la **taxonomía del fallo**, y estos lenguajes la enseñan porque en ellos las fases
están separadas y **cada una tiene su vocabulario**. Un `syntax error, unexpected AREA` de GnuCOBOL es
del analizador (clase 100); un `not dispatching (must be defined in a package spec)` de GNAT es del
semántico (clase 111); un `undefined reference` es del enlazador; y un `Constraint_Error` es de
ejecución.

Y muestran el eje que de verdad importa: **cuánto se detecta antes**. Ada y Fortran con módulos
comprueban entre unidades; C y PL/I emparejan por nombre y no comprueban nada (clase 088).
""",
    cierre="""
Lo transferible: **cada fase que detecta un error ahorra órdenes de magnitud respecto a la
siguiente**. Un error de sintaxis cuesta segundos; uno de tipos, minutos; uno de enlace, una tarde; y
uno de ejecución en producción, una llamada de madrugada. Por eso los lenguajes con comprobación
fuerte piden ceremonia: **están comprando detección temprana**. Y por eso la pregunta útil ante un
fallo nuevo no es "¿cómo lo arreglo?" sino **"¿qué fase debería haberlo cazado?"**.
""",
    langs={
        "cobol": ("""
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
""", """
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
"""),
        "fortran": ("""
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
""", """
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
"""),
        "ada": ("""
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
""", """
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
"""),
        "pascal": ("""
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
""", """
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
"""),
        "lisp": ("""
(let* ((codigo (read))
       (tipo (case codigo
               (1 "sintaxis")
               (2 "tipos")
               (3 "enlace")
               (4 "ejecucion")
               (t "?"))))
  (format t "error=~A~%" tipo))
""", """
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
"""),
        "tcl": ("""
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
""", """
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
"""),
        "perl": ("""
use strict;
use warnings;

my $codigo = <STDIN>;
chomp $codigo;

my %tipos = (1 => 'sintaxis', 2 => 'tipos', 3 => 'enlace', 4 => 'ejecucion');

print "error=", ($tipos{$codigo} // '?'), "\\n";
""", """
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
"""),
        "cpp": ("""
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

    std::cout << "error=" << tipo << '\\n';
    return 0;
}
""", """
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
"""),
        "rpg": ("""
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
""", """
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
"""),
        "pli": ("""
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
""", """
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
"""),
        "mumps": ("""
ERRORES ; Tipos de error -- clase 137
 read codigo
 set tipo = $select(codigo=1:"sintaxis", codigo=2:"tipos", codigo=3:"enlace", codigo=4:"ejecucion", 1:"?")
 write "error=", tipo, !
 quit
""", """
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
"""),
        "smalltalk": ("""
| codigo tipo |

codigo := stdin nextLine trimBoth asNumber.

tipo := codigo = 1 ifTrue: [ 'sintaxis' ] ifFalse: [
        codigo = 2 ifTrue: [ 'tipos' ] ifFalse: [
        codigo = 3 ifTrue: [ 'enlace' ] ifFalse: [
        codigo = 4 ifTrue: [ 'ejecucion' ] ifFalse: [ '?' ] ] ] ].

Transcript show: 'error=', tipo; cr.
""", """
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
"""),
    },
)

# ---------------------------------------------------------------------------
# 138 — Depuración
# ---------------------------------------------------------------------------
SPECS["138"] = dict(
    gancho="""
Un valor, su cuadrado y su cubo. El programa es una excusa para la pregunta de esta clase: **cuando
algo va mal, ¿qué puedes mirar?** Y aquí hay dos extremos que definen el espectro: **Smalltalk, donde
el error abre un depurador sobre el sistema vivo y puedes escribir el método que falta y continuar**,
y **COBOL en un lote nocturno, donde lo único que hay es un volcado de memoria y un listado de
compilación**.
""",
    porque="""
Aquí el concepto es la **observabilidad de un programa en marcha**, y estos lenguajes lo enseñan porque
tienen las herramientas más distintas de esta página. **El volcado y el listado**: COBOL y PL/I, donde
la depuración es forense. **El registro del trabajo**: IBM i, donde cada mensaje queda con su pila.
**El código como dato**: M con `$text` y `$stack` (clases 123 y 127). **Y el sistema vivo**: Smalltalk
y Lisp, donde el depurador es parte del programa.

Y el eje que las ordena no es la antigüedad: **es si el programa sigue vivo cuando lo miras**.
""",
    cierre="""
Lo transferible: **depurar es reducir el espacio de estados posibles, y las herramientas solo ayudan a
mirar**. Un depurador da el estado actual; un registro, la historia; un volcado, la foto final; y una
prueba que reproduce el fallo, el control. La más valiosa es la última, y por eso la depuración
empieza casi siempre por **conseguir reproducirlo**. Cuando un fallo no se reproduce, lo que hay que
mejorar no es la técnica de depuración: es lo que el programa registra.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. DEPURA.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  N       PIC S9(9)  COMP-3.
01  CUAD    PIC S9(18) COMP-3.
01  CUBO    PIC S9(18) COMP-3.
01  ED-N    PIC -(8)9.
01  ED-C    PIC -(17)9.
01  ED-K    PIC -(17)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    COMPUTE N = FUNCTION NUMVAL(LINEA)

    COMPUTE CUAD = N * N
    COMPUTE CUBO = N * N * N

    MOVE N    TO ED-N
    MOVE CUAD TO ED-C
    MOVE CUBO TO ED-K
    DISPLAY "valor=" FUNCTION TRIM(ED-N)
            " cuadrado=" FUNCTION TRIM(ED-C)
            " cubo=" FUNCTION TRIM(ED-K)
    STOP RUN.
""", """
**Lo que esta clase enseña en COBOL.** La depuración en el mundo COBOL tiene dos modos muy distintos, y
merece conocer los dos.

**El interactivo**, con IBM Debug Tool o Micro Focus, que hace lo esperable: puntos de ruptura,
inspección de variables, ejecución paso a paso y **modificación de datos en marcha**.

**Y el forense**, que es el que define la cultura: **el volcado**.

```text
ABEND S0C7 → volcado de memoria + listado de compilación
```

Cuando un lote nocturno falla a las 3:40, **no hay nadie mirando y no se puede reproducir**. Lo que
queda es:

- **El volcado**: la memoria del programa en el instante del fallo.
- **El listado con `MAP` y `OFFSET`** (clase 137): **qué campo hay en cada desplazamiento**.
- **Y el desplazamiento del error**, que el sistema informa.

Con esas tres cosas se localiza **qué instrucción falló y qué contenía cada campo**, sin ejecutar
nada. Es arqueología, y funciona.

Y COBOL tiene ayudas del lenguaje que esta clase debe nombrar:

```cobol
DISPLAY "traza: " CAMPO UPON SYSOUT       *> el printf de siempre
DECLARATIVES ... USE FOR DEBUGGING ON ...  *> secciones de depuración
```

**`USE FOR DEBUGGING`** es una construcción del estándar que declara código que **solo se ejecuta si la
compilación tiene `WITH DEBUGGING MODE`**, y que puede dispararse **cada vez que cambia un dato o se
ejecuta un párrafo**.

```cobol
DEBUG-ITEM       *> variable especial: qué párrafo, qué línea, qué valor
```

Es un mecanismo de traza integrado en el lenguaje, de 1974, y hoy se considera obsoleto — pero la idea
—**instrumentación activable al compilar**— es la de cualquier marco de registro moderno.

Y hay una técnica del mainframe que conviene mencionar porque no tiene equivalente: **CEDF**, el
facilitador de depuración interactiva de CICS, que **intercepta cada comando `EXEC CICS` de una
transacción en producción y lo muestra**, permitiendo modificar los datos antes de continuar.

Es depuración de una transacción viva en un sistema en producción, con miles de usuarios conectados.
"""),
        "fortran": ("""
program depura
   implicit none
   integer :: n

   read(*, *) n

   write(*, '(A,I0,A,I0,A,I0)') 'valor=', n, ' cuadrado=', n * n, &
                                ' cubo=', n * n * n
end program depura
""", """
**Lo que esta clase enseña en Fortran.** La depuración en Fortran tiene una peculiaridad que la
distingue: **el problema no suele ser un fallo, es un número equivocado**.

Un programa numérico que produce resultados sutilmente incorrectos —por un índice mal puesto, por una
condición de contorno o por pérdida de precisión— **no falla**: da un resultado plausible y erróneo.

De ahí que las herramientas de Fortran se centren en las comprobaciones:

```bash
gfortran -g -fcheck=all -ffpe-trap=invalid,zero,overflow \\
         -fbacktrace -Wall -Wextra prog.f90
```

- **`-fcheck=all`**: índices, punteros no asociados, conformidad de arreglos.
- **`-ffpe-trap`**: **convierte NaN, infinito y división por cero en una excepción**, en lugar de
  propagar un NaN silenciosamente por todo el cálculo.
- **`-fbacktrace`**: traza de la pila al abortar.
- **`-finit-real=snan`**: inicializar los reales con NaN señalizador, para **detectar el uso de
  variables sin inicializar**.

**`-ffpe-trap` es la más importante** y merece la explicación: en coma flotante, `0.0/0.0` da `NaN`, y
`NaN` se propaga por cualquier operación. Un cálculo de ocho horas puede terminar con todo a `NaN` y
**sin saber dónde empezó**. Con la trampa activada, **el programa se detiene en la operación culpable**.

Y para la depuración interactiva, Fortran usa **gdb** con soporte específico:

```text
(gdb) print v(3)@10        # imprimir 10 elementos desde v(3)
(gdb) print matriz
(gdb) info locals
```

Y para el paralelismo, hay herramientas especializadas que esta clase debe nombrar porque el problema
es real: **depurar 10.000 procesos MPI**.

```text
TotalView, Arm DDT   -- depuradores paralelos: agrupan procesos por comportamiento
Intel Inspector       -- carreras en OpenMP
Valgrind, MAP          -- perfilado
```

**Agrupar procesos por comportamiento** es la técnica clave: en lugar de mirar 10.000 pilas, la
herramienta muestra "9.997 procesos están aquí, 3 están allí" — y esos 3 son el problema.

Es una idea que la observabilidad moderna ha redescubierto con el agrupamiento de trazas.
"""),
        "ada": ("""
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Depura is
   N : Integer;
begin
   Get (N);

   Put ("valor=");      Put (N,         Width => 1);
   Put (" cuadrado=");  Put (N * N,     Width => 1);
   Put (" cubo=");      Put (N * N * N, Width => 1);
   New_Line;
end Depura;
""", """
**Lo que esta clase enseña en Ada.** La filosofía de Ada en esta clase es coherente con toda su página
en la Parte 8: **el mejor depurador es el que no hace falta**.

Con las comprobaciones activadas por defecto (clase 124), **un error de ejecución en Ada llega con
información**:

```text
raised CONSTRAINT_ERROR : prog.adb:15 index check failed
```

**Fichero, línea y qué comprobación falló**, sin depurador y sin símbolos. Compara con
`Segmentation fault` de C++ (clase 137).

Y GNAT añade la traza:

```bash
gnatmake -g -gnata -bargs -E prog.adb     # -E: guardar la traza en las excepciones
```

```ada
with GNAT.Traceback.Symbolic;
Put_Line (GNAT.Traceback.Symbolic.Symbolic_Traceback (E));
```

**Obtener la pila de una excepción desde el propio programa**, para registrarla.

Y Ada tiene tres mecanismos de depuración que son propios y que esta clase debe destacar:

**Primero, los contratos como aserciones activables** (clase 118):

```ada
pragma Assertion_Policy (Check);      --  o Ignore, en producción
function F (X : Integer) return Integer with Pre => X > 0;
```

**Las precondiciones se comprueban en desarrollo y se desactivan en producción**, con la misma
declaración. Y con SPARK, **lo que se demuestra ya no hace falta comprobarlo**.

**Segundo, `Ada.Exceptions` con información estructurada**:

```ada
exception
   when E : others =>
      Put_Line (Exception_Name (E));       --  qué excepción
      Put_Line (Exception_Message (E));      --  el mensaje
      Put_Line (Exception_Information (E));   --  todo, incluida la traza
```

**Y tercero, la depuración de tareas**: GDB con soporte de Ada muestra **las tareas, su estado, en qué
entrada están esperando y quién tiene cada objeto protegido**.

```text
(gdb) info tasks
   ID   TID       P-ID  Pri  State           Name
   1    ...       0     15   Runnable        main_task
   2    ...       1     15   Waiting on entry call  sensor
```

**Ver que una tarea está esperando en una entrada concreta** es la información que hace falta para
diagnosticar un interbloqueo, y en la mayoría de los lenguajes hay que deducirla de las pilas.

Es depuración con el vocabulario del modelo de concurrencia del lenguaje, no con el del sistema
operativo.
"""),
        "pascal": ("""
program Depura;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  N: Integer;

begin
  Read(N);

  WriteLn('valor=', IntToStr(N),
          ' cuadrado=', IntToStr(N * N),
          ' cubo=', IntToStr(N * N * N));
end.
""", """
**Lo que esta clase enseña en Pascal.** El mundo Pascal tiene una tradición de depuración muy marcada, y
viene de la clase 123: **Turbo Pascal integró el depurador en el editor en 1987**, cuando eso no
existía.

Poner un punto de ruptura con F5, ejecutar paso a paso con F7 e inspeccionar variables con Ctrl+F4
**en el mismo entorno donde se escribía el código** era revolucionario. Es el modelo de todos los IDE
modernos.

Hoy, Free Pascal usa **GDB** y Lazarus lo integra, y el ecosistema tiene tres herramientas que merecen
nombrarse:

**El registro de errores con pila**:

```pascal
uses SysUtils;
{$IFDEF DEBUG}
  SetHeapTraceOutput('fugas.txt');    { del unit heaptrc }
{$ENDIF}
```

**`heaptrc`** es la unidad de detección de fugas de Free Pascal (clase 130): con `-gh`, **al terminar el
programa informa de cada bloque no liberado con la pila de dónde se reservó**.

```bash
fpc -gh -gl prog.pas       # -gh: rastreo de montón; -gl: números de línea
```

**Y `-gl` es el complemento**: hace que las trazas incluyan fichero y línea, con lo que un error de
ejecución da:

```text
Runtime error 216 at $0000000000401234
  $0000000000401234  PROCESAR,  line 42 of prog.pas
```

Y en Delphi, la herramienta de referencia es **madExcept** o **EurekaLog**, que capturan cualquier
excepción no manejada y producen **un informe con la pila, las variables, la versión y una captura de
pantalla** — pensado para recibir informes de fallos de usuarios finales.

Es una capacidad que el ecosistema desarrolló porque su público es el software de escritorio
distribuido: **el fallo ocurre en la máquina del cliente**, y hay que diagnosticarlo sin acceso.

Es exactamente el problema que hoy resuelven Sentry y los sistemas de telemetría de fallos, y en el
mundo Delphi está resuelto desde hace veinte años.
"""),
        "lisp": ("""
(let ((n (read)))
  (format t "valor=~D cuadrado=~D cubo=~D~%" n (* n n) (* n n n)))
""", """
**Lo que esta clase enseña en Common Lisp.** Lisp tiene, junto con Smalltalk, **la mejor experiencia de
depuración de esta página**, y por la misma razón: **el programa está vivo mientras lo miras**.

Cuando salta un error, se entra en el depurador **con la pila intacta y el sistema funcionando**:

```text
The value 3 is not of type STRING.
   [Condition of type TYPE-ERROR]

Restarts:
  0: [USE-VALUE] Specify a value to use instead.
  1: [RETRY] Retry SLIME REPL evaluation request.
  2: [ABORT] Return to SLIME's top level.

Backtrace:
  0: (MI-FUNCION 3)
  1: (OTRA-FUNCION)
```

Y **los reinicios** son lo que distingue a Lisp de todo lo demás (clases 103 y 116): **no solo se ve el
error, se ofrecen formas de continuar**.

`USE-VALUE` permite **dar el valor correcto y seguir desde ahí**, sin reiniciar el programa.

Y el arsenal del depurador:

```lisp
(trace mi-funcion)                 ; registrar cada llamada y su resultado
(untrace)
(break)                             ; punto de ruptura explícito
(inspect objeto)                     ; inspector interactivo
(describe objeto)
(step (mi-funcion 3))                 ; ejecución paso a paso
(sb-debug:print-backtrace)
(disassemble 'mi-funcion)              ; ver el código máquina (clase 123)
(time (mi-funcion 3))                   ; tiempo Y memoria reservada (clase 128)
```

**`trace` funciona sobre cualquier función, incluidas las del sistema**, sin recompilar y sin
instrumentar el código: envuelve la función en marcha.

Y con **SLIME** —el entorno de Emacs para Lisp— todo eso está integrado: **la pila navegable, el
inspector, la recompilación de una función y la reanudación**, todo sobre la imagen viva.

Y hay una capacidad que esta clase debe cerrar y que ilustra lo que significa "programa vivo": **se
puede depurar un servidor en producción conectándose por red**.

```lisp
(swank:create-server :port 4005)
```

**Abrir un servidor SLIME dentro de la aplicación en marcha** y conectarse desde el editor, para
inspeccionar, redefinir funciones y arreglar el problema **sin detener el servicio**.

Es una práctica real en despliegues de Common Lisp, y suena imprudente hasta que se compara con la
alternativa: reiniciar y perder el estado que provocó el fallo.
"""),
        "tcl": ("""
gets stdin linea
set n [string trim $linea]

puts "valor=$n cuadrado=[expr {$n * $n}] cubo=[expr {$n * $n * $n}]"
""", """
**Lo que esta clase enseña en Tcl.** Tcl tiene un mecanismo de depuración que ningún otro lenguaje de
esta página iguala en potencia y en simplicidad: **`trace`**.

```tcl
trace add variable x write { apply {{n1 n2 op} { puts "x cambió a $::x" }} }
trace add variable x read  { ... }
trace add variable x unset { ... }
trace add execution miProc enter { ... }
trace add execution miProc leave { ... }
trace add execution miProc enterstep { ... }     ;# ¡CADA COMANDO de dentro!
```

**`trace add execution ... enterstep` ejecuta código antes de CADA comando dentro de un
procedimiento**, sin modificar el código y sin recompilar.

Eso es un depurador paso a paso construido con un comando, y es lo que hace el depurador de Tcl.

Y `trace add variable ... write` responde a la pregunta más difícil de la depuración: **"¿quién cambió
esto?"**. En la mayoría de los entornos hace falta un punto de ruptura de datos del hardware; en Tcl es
una línea.

El resto del arsenal:

```tcl
info level 0                 ;# la llamada actual, con sus argumentos
info level -1                 ;# la del llamante
info frame                     ;# fichero y línea
catch { ... } r opts            ;# con -errorinfo: la pila completa (clase 137)
rename puts puts_orig            ;# INTERCEPTAR cualquier comando (clase 109)
```

**`rename` más un procedimiento envoltorio permite interceptar cualquier comando del sistema**, y es
como se instrumentan bibliotecas ajenas sin tocarlas.

Y el ecosistema tiene:

```bash
tclsh -encoding utf-8 ...
package require TclDebugger      # el depurador de ActiveState
nagelfar prog.tcl                 # análisis estático (clase 137)
```

Y en Tcl 8.7, la depuración de corrutinas (clase 134):

```tcl
coroprobe $nombre { info level }    ;# mirar DENTRO de una corrutina suspendida
```

**Inspeccionar una corrutina suspendida** es un problema abierto en la mayoría de los entornos
asíncronos —¿dónde está la pila de una tarea que no se está ejecutando?— y Tcl lo resolvió con un
comando.
"""),
        "perl": ("""
use strict;
use warnings;

my $n = <STDIN>;
chomp $n;

printf "valor=%d cuadrado=%d cubo=%d\\n", $n, $n * $n, $n * $n * $n;
""", """
**Lo que esta clase enseña en Perl.** Perl trae **un depurador completo en el intérprete**, sin instalar
nada:

```bash
perl -d programa.pl
```

```text
  DB<1> n              # siguiente línea
  DB<2> s               # entrar en la función
  DB<3> c 42             # continuar hasta la línea 42
  DB<4> x $estructura     # volcar una estructura de datos, RECURSIVAMENTE
  DB<5> T                  # la pila
  DB<6> b 15 $x > 100       # punto de ruptura CONDICIONAL
  DB<7> w $variable          # vigilar una variable
```

**`x` es el comando estrella**: vuelca una estructura anidada con indentación y tipos, y es lo que
hace utilizable la depuración de estructuras complejas de Perl (clase 097).

Y `perl -d` tiene una propiedad poco conocida: **el depurador está escrito en Perl** —`perl5db.pl`— y
se puede sustituir:

```bash
PERL5DB='BEGIN { require "mi_depurador.pl" }' perl -d prog.pl
perl -d:Trace prog.pl          # módulos Devel::*
perl -d:NYTProf prog.pl         # el PERFILADOR de referencia
```

**`Devel::NYTProf`** merece la mención: es uno de los mejores perfiladores de cualquier lenguaje de
guion, con informes HTML línea a línea y desglose por llamada.

Y el arsenal de diagnóstico de Perl es de los más ricos de esta página:

```perl
use Data::Dumper;   print Dumper($estructura);      # volcar
use Devel::Peek;     Dump($x);                       # la estructura INTERNA (clase 128)
use Carp;            confess "error";                 # morir CON la pila
use Devel::Cycle;    find_cycle($x);                   # ciclos (clase 131)
$SIG{__DIE__} = sub { ... };                            # gancho global (clase 119)
```

**`Carp::confess`** es `die` con la pila completa, y `cluck` es `warn` con pila. Son la forma
idiomática de que un error de una biblioteca diga desde dónde se la llamó (clase 127).

Y `Data::Dumper` tiene una propiedad que encaja con esta parte del curso: **su salida es código Perl
válido**, así que una estructura volcada **se puede volver a leer con `eval`**.

Es la misma idea que `print`/`read` en Lisp (clase 104) y `storeString` en Smalltalk: **el volcado de
depuración y el formato de serialización son el mismo**.
"""),
        "cpp": ("""
#include <iostream>

int main() {
    long long n{};
    if (!(std::cin >> n)) return 1;

    std::cout << "valor=" << n
              << " cuadrado=" << n * n
              << " cubo=" << n * n * n << '\\n';
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** C++ tiene **las herramientas de depuración más potentes y las
menos integradas** de esta página, y esa combinación define su cultura.

```bash
g++ -g -O0 prog.cpp        # -g: símbolos de depuración; -O0: sin optimizar
gdb ./prog
lldb ./prog
```

Y la primera lección es la del compromiso: **`-g` con `-O2` produce información de depuración
engañosa**. El compilador reordena, elimina variables y funde funciones, así que **el depurador muestra
valores optimizados o "value optimized out"**.

De ahí la práctica universal: **compilar dos veces**, una para depurar y otra para producción — con el
riesgo conocido de que **el fallo solo aparezca con optimización**, que suele significar comportamiento
indefinido (clase 137).

El arsenal de C++ es enorme, y merece organizarlo por lo que responde:

| Pregunta | Herramienta |
|---|---|
| ¿Qué estado hay ahora? | **gdb**, **lldb**, puntos de ruptura condicionales |
| ¿Quién tocó esta memoria? | **watchpoints** de hardware: `watch *ptr` |
| ¿Hay fugas o accesos inválidos? | **AddressSanitizer**, **Valgrind** |
| ¿Hay carreras? | **ThreadSanitizer** (clase 136) |
| ¿Hay comportamiento indefinido? | **UBSan** |
| ¿Dónde se va el tiempo? | **perf**, **VTune**, **Callgrind** |
| ¿Y en producción? | **eBPF**, volcados de núcleo, `std::stacktrace` (C++23) |

**Los `watchpoints` de hardware** merecen destacarse: `watch *0x7fff1234` hace que el procesador
detenga el programa **cuando algo escriba en esa dirección**, y responde a la pregunta "¿quién está
corrompiendo esto?" — que es la más difícil de C++.

Es lo mismo que `trace add variable ... write` en Tcl de esta página, con el hardware haciendo el
trabajo en lugar del intérprete.

Y **rr** merece la mención final porque cambia el tipo de pregunta que se puede hacer:

```bash
rr record ./prog       # graba la ejecución
rr replay              # y la reproduce, con GDB, hacia ATRÁS
(gdb) reverse-continue  # ejecutar hacia atrás hasta el punto de ruptura
```

**Depuración reversible**: reproducir exactamente la misma ejecución —incluidas las condiciones de
carrera— y **retroceder desde el fallo hasta la causa**.

Es la respuesta más directa al cierre de esta clase: **cuando puedes reproducir el fallo
determinísticamente, el problema está medio resuelto**.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi DEPURA;
  n int(10) const;
end-pi;

dcl-s cuad int(20);
dcl-s cubo int(20);

cuad = n * n;
cubo = n * n * n;

dsply ('valor=' + %char(n) + ' cuadrado=' + %char(cuad) + ' cubo=' + %char(cubo));

*inlr = *on;
return;
""", """
**Lo que esta clase enseña en RPG.** IBM i tiene, en depuración, la propiedad que más lo distingue de
todas las plataformas de esta página: **todo queda registrado sin configurar nada**.

**El registro del trabajo** (clase 137):

```text
DSPJOBLOG JOB(123456/USUARIO/MIAPP)
```

Cada mensaje lleva **el código, el texto, la ayuda de segundo nivel, el programa, el número de
sentencia y la pila de llamadas en ese momento**. Sin instrumentar el código y sin activar nada.

**El depurador del sistema**:

```text
STRDBG PGM(MIBIB/MIAPP) UPDPROD(*YES)
```

Y con `DBGVIEW(*SOURCE)` al compilar, **el depurador muestra el fuente**, aunque el objeto esté en otra
máquina — porque **la vista de depuración se guarda dentro del objeto programa**.

Eso resuelve un problema clásico: **no hace falta tener el fuente para depurar**. Está en el objeto.

**El depurador de servicio**, que es la capacidad que sorprende:

```text
STRSRVJOB JOB(123456/USUARIO/OTROTRABAJO)
STRDBG PGM(...)
```

**Depurar un trabajo AJENO que ya está en ejecución**, incluido uno de un usuario conectado o un
trabajo por lotes en marcha, desde otra sesión.

Y por SQL, la forma moderna (clase 117):

```sql
SELECT * FROM TABLE(QSYS2.STACK_INFO('*'))          -- pilas de TODOS los trabajos
SELECT * FROM TABLE(QSYS2.JOBLOG_INFO('123456/USUARIO/MIAPP'))
SELECT * FROM QSYS2.ACTIVE_JOB_INFO(...)
```

**Consultar la pila de llamadas y el registro de cualquier trabajo del sistema con `WHERE` y
`ORDER BY`.**

Es observabilidad por defecto, y es una diferencia cultural profunda: **en IBM i la pregunta "¿qué
estaba haciendo el programa?" tiene respuesta siempre**, mientras que en un servidor moderno depende
de si alguien puso el registro adecuado antes de que pasara.

Es exactamente lo que el cierre de esta clase señala: **lo que hay que mejorar cuando un fallo no se
diagnostica no es la técnica, es lo que el sistema registra** — y aquí lo registra la plataforma.
"""),
        "pli": ("""
 depura: procedure options(main);

    declare n fixed binary(31);

    get list (n);

    put skip list ('valor=' || trim(char(n)) ||
                   ' cuadrado=' || trim(char(n * n)) ||
                   ' cubo=' || trim(char(n * n * n)));

 end depura;
""", """
**Lo que esta clase enseña en PL/I.** PL/I comparte con COBOL la cultura forense del volcado (clase
138, apartado COBOL) y tiene dos capacidades de diagnóstico propias que merecen conocerse.

**La primera es `put data`**, ya nombrada en la clase 106:

```pli
 put data;                    /* vuelca TODAS las variables del ámbito */
 put data (x, y, estructura);  /* o las indicadas */
```

**`put data` sin argumentos imprime cada variable con su nombre y su valor**, con formato
`NOMBRE=VALOR`. Es un volcado de depuración integrado en el lenguaje, y su salida **se puede volver a
leer con `get data`**.

Es la misma propiedad que `Data::Dumper` en Perl y `print`/`read` en Lisp de esta página: **el volcado
de depuración y el formato de intercambio son el mismo**.

**Y la segunda es el manejo de condiciones como instrumentación** (clases 103 y 137):

```pli
 on error snap begin;
    put data;                 /* volcar el estado */
    put skip list ('en ' || onloc());     /* dónde ocurrió */
 end;
```

**`snap`** es la palabra clave que lo hace especial: **hace que el sistema imprima la traza de la pila**
antes de ejecutar el manejador.

Y las funciones de contexto de las condiciones dan información estructurada:

```pli
 onloc()      /* el nombre del procedimiento donde ocurrió */
 oncode()     /* el código numérico de la condición */
 onchar()     /* el carácter que causó un error de conversión */
 onsource()   /* la CADENA que lo causó, y se puede MODIFICAR (clase 116) */
 onfile()     /* el fichero implicado */
```

**`onsource` es la que no tiene equivalente**: da el dato que causó el error de conversión **y permite
cambiarlo y reanudar** — lo que en la clase 116 se comparaba con los reinicios de Lisp.

Y el listado de compilación de PL/I (clase 137), con `XREF`, `MAP`, `ATTRIBUTES` y `LIST`, completa el
cuadro: **un documento que dice dónde está cada variable, quién la usa y qué código se generó**.

Es depuración sin depurador, diseñada para una época en que la máquina estaba en otro edificio.
"""),
        "mumps": ("""
DEPURA ; Depuracion -- clase 138
 read n
 write "valor=", n, " cuadrado=", n * n, " cubo=", n * n * n, !
 quit
""", """
**Lo que esta clase enseña en M.** M tiene una propiedad que lo hace singular en esta clase y que viene
de las clases 123 y 127: **el código fuente es un dato accesible en ejecución**.

```mumps
 write $text(+3^MIRUT)                 ; la línea 3 del fuente
 write $stack($stack, "MCODE")          ; el CÓDIGO de la línea actual de la pila
 write $stack(-1)                        ; cuántos niveles hay
 write $stack(2, "PLACE")                 ; dónde está el nivel 2
 write $zstatus                            ; el error completo (extensión)
```

**`$stack(nivel, "MCODE")` devuelve el texto del código de ese nivel de la pila.** Es una traza que
muestra **el código, no solo los nombres de función**, y sin depurador ni símbolos.

Y el manejo de errores con `$etrap` (clase 137) permite construir un registro completo:

```mumps
 set $etrap = "do ^ERRLOG"
 ...
errlog ;
 new i
 for i=$stack(-1):-1:1 write $stack(i,"PLACE")," ",$stack(i,"MCODE"),!
 quit
```

**Ese bucle imprime la pila entera con el código de cada línea**, y es un patrón real en los sistemas
VistA.

Y M tiene además el depurador interactivo del entorno:

```mumps
 zbreak procesar^RUTINA           ; punto de ruptura (extensión $Z)
 zstep into
 zshow "V"                          ; mostrar todas las variables
 zwrite                              ; volcar el espacio de variables
```

**`zwrite` sin argumentos vuelca todas las variables locales con sus subíndices**, y es el `put data`
de PL/I de esta página.

Y hay una capacidad que se deriva del modelo de M y que esta clase debe cerrar: **el estado se puede
inspeccionar desde otro proceso**.

```mumps
 write ^PACIENTE(123)              ; desde CUALQUIER proceso, en cualquier momento
```

**Como los datos están en *globals*, un proceso puede examinar lo que otro está haciendo**, sin
depurador y sin detenerlo — siempre que el programa haya escrito su estado ahí.

Es lo mismo que la observabilidad de IBM i de esta página, conseguido por la vía del modelo de datos:
**si el estado importante vive en la base de datos, siempre se puede mirar**.

Y es la conclusión práctica del cierre de esta clase: **lo que se registra es lo que se puede
diagnosticar**, y en M el registro es el modelo de datos.
"""),
        "smalltalk": ("""
| n |

n := stdin nextLine trimBoth asNumber.

Transcript
    show: 'valor=', n printString;
    show: ' cuadrado=', (n * n) printString;
    show: ' cubo=', (n * n * n) printString;
    cr.
""", """
**Lo que esta clase enseña en Smalltalk.** Aquí está el extremo del espectro que abre esta clase, y
cierra la Parte 8 entera: **en Smalltalk, el depurador no es una herramienta externa — es parte del
sistema, escrito en Smalltalk, y opera sobre el programa vivo**.

Cuando salta un error:

1. **Se abre el depurador sobre el proceso**, que sigue suspendido y con todo su estado.
2. **La pila es navegable**, y cada marco muestra sus variables, su receptor y su código (clase 127).
3. **Se puede inspeccionar y modificar cualquier objeto** de cualquier marco.
4. **Se puede editar el método ahí mismo**, aceptarlo y **pulsar "reintentar"**.
5. **Y el programa continúa** desde ese punto, con el método nuevo.

**El paso 4 es el que no tiene equivalente en ninguna otra fila de esta página.**

Y el arsenal está todo en el lenguaje:

```smalltalk
self halt.                          "punto de ruptura en el código"
self inspect.                        "abrir el inspector sobre este objeto"
thisContext.                          "el marco actual (clase 127)"
objeto browse.                         "abrir el navegador en su clase"
objeto chasePointers.                   "quién lo retiene (clase 131)"
MessageTally spyOn: [ ... ].             "PERFILADOR: dónde se va el tiempo"
Object subclass: ... instanceVariableNames: ...    "crear una clase, en marcha"
```

**`MessageTally spyOn:`** es el perfilador, escrito en Smalltalk, que muestrea la pila del proceso y
produce un árbol de llamadas con porcentajes.

Y hay dos capacidades que resumen la diferencia de modelo:

**El navegador de mensajes** (clase 098):

```smalltalk
SystemNavigation default allCallsOn: #imprimir
SystemNavigation default browseAllImplementorsOf: #imprimir
```

**"¿Quién llama a esto?" y "¿quién lo implementa?" se responden recorriendo la imagen**, en un segundo
y sin herramientas externas.

**Y la depuración remota sobre la imagen en producción**, igual que el `swank` de Lisp de esta página:
conectarse a un sistema en marcha, inspeccionar, corregir y continuar.

Y con eso cierra la Parte 8, con la observación que la recorre entera: **Smalltalk tomó en cada una de
las dieciséis clases la decisión que maximiza la observabilidad** —bytecode con JIT, todo en el montón,
sin punteros, la pila como objeto, recolector, compilador en el sistema— **y el resultado es un entorno
donde casi cualquier pregunta sobre el programa tiene respuesta inmediata**.

El precio está en la otra columna: menos control, menos predecibilidad y menos rendimiento en el peor
caso. **Es el mismo compromiso de siempre, tomado con coherencia absoluta durante cuarenta y seis
años.**
"""),
    },
)
