# -*- coding: utf-8 -*-
"""Parte 10, lote A — clases 155 a 157. Ver `vivos_parte10.py` y `gen_vivos.py`."""

SPECS: dict[str, dict] = {}

# ---------------------------------------------------------------------------
# 155 — Por qué los sistemas reales son poliglotas
# ---------------------------------------------------------------------------
SPECS["155"] = dict(
    gancho="""
Contar componentes. El programa es una excusa para la pregunta de la parte entera: **¿por qué ningún
sistema serio está escrito en un solo lenguaje?** Y esta página tiene la respuesta más antigua que
existe: **un programa CICS de 1975 ya mezclaba cuatro lenguajes** —COBOL para la lógica, JCL para
orquestar, SQL embebido para los datos y macros de ensamblador para lo que ninguno de los tres podía
hacer—. **El sistema poliglota no es una moda: es el estado natural del software desde el principio.**
""",
    porque="""
Aquí el concepto es la **frontera entre lenguajes como decisión de diseño**, y estos lenguajes la
enseñan porque **casi ninguno pretendió nunca ser el único**. COBOL nació para la lógica de negocio y
delegó todo lo demás. Fortran calcula y deja la interfaz a otros. Tcl se diseñó explícitamente **para
ser la mitad de un sistema de dos lenguajes**. Y RPG convive con Java, Node y SQL en la misma máquina y
en el mismo trabajo.

Y aparece la pregunta que ordena toda la Parte 10: **cuando dos lenguajes se tocan, ¿qué cruza la
frontera y con qué garantías?**
""",
    cierre="""
Lo transferible: **cada frontera entre lenguajes tiene un coste, y ese coste es lo que decide si merece
la pena**. Hay tres tipos, de menor a mayor precio: **el proceso separado** —simple, aislado, y con
serialización en medio—; **la biblioteca compartida** —rápida, y con un ABI que hay que respetar (clase
157)—; y **la máquina virtual compartida** —lo más integrado y lo más frágil—. La regla que evita casi
todos los problemas: **cuantas menos fronteras y más gruesas, mejor**. Diez llamadas al día entre dos
lenguajes no son un problema; diez millones, sí.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. COMPON.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(200).
01  I       PIC 9(4) COMP.
01  CNT     PIC 9(4) COMP VALUE 0.
01  ENPAL   PIC 9      VALUE 0.
01  ED      PIC -(3)9.

PROCEDURE DIVISION.
    ACCEPT LINEA

    PERFORM VARYING I FROM 1 BY 1 UNTIL I > 200
        IF LINEA(I:1) = SPACE
            MOVE 0 TO ENPAL
        ELSE
            IF ENPAL = 0
                MOVE 1 TO ENPAL
                ADD 1 TO CNT
            END-IF
        END-IF
    END-PERFORM

    MOVE CNT TO ED
    DISPLAY "componentes=" FUNCTION TRIM(ED)
    STOP RUN.
""", """
**Lo que esta clase enseña en COBOL.** Aquí está el ejemplo del gancho, y merece verlo en detalle porque
es el sistema poliglota original:

```cobol
       IDENTIFICATION DIVISION.          *> 1. COBOL: la lógica de negocio
       ...
           EXEC CICS RECEIVE MAP('PANT1') END-EXEC     *> 2. CICS: la transacción
           EXEC SQL SELECT SALDO INTO :WS-SALDO         *> 3. SQL embebido: los datos
                    FROM CUENTAS WHERE ID = :WS-ID
           END-EXEC
           CALL 'ASMRUT' USING WS-BLOQUE                 *> 4. Ensamblador: lo demás
```

**Cuatro lenguajes en un fichero**, y ninguno es opcional:

- **CICS** gestiona la transacción, la pantalla y el bloqueo. COBOL no sabe hacer eso.
- **SQL** consulta la base. COBOL sabría recorrer un fichero, pero no optimizar una unión.
- **El ensamblador** hace lo que ninguno puede: llamadas al sistema, manipulación de bits, acceso a
  estructuras de control.

Y por encima está **el JCL** (clase 077), que orquesta los pasos, asigna los ficheros y decide qué se
ejecuta según los códigos de retorno — que es **un quinto lenguaje**, y uno declarativo.

Y la mecánica de la frontera merece explicarse porque es de las más simples de esta página: **el
precompilador**.

```text
fuente.cbl  →  precompilador DB2   →  fuente con CALLs a la interfaz de DB2
            →  traductor CICS       →  fuente con CALLs a la interfaz de CICS
            →  compilador COBOL      →  objeto
            →  enlazador              →  módulo de carga
```

**Los `EXEC SQL` y `EXEC CICS` no son sintaxis de COBOL: son marcas que un programa anterior sustituye
por llamadas normales** (clase 123).

Es exactamente la técnica de los lenguajes embebidos modernos —las consultas comprobadas en compilación,
los generadores de clientes de API— y es de los años setenta.

Y merece extraer lo que este modelo hizo bien y que sigue siendo válido: **cada lenguaje se ocupa de lo
que sabe hacer, y las fronteras están en sitios naturales** —la transacción, la consulta, la
orquestación—, no repartidas por todas partes.

Es la aplicación de la regla del cierre de esta clase: **pocas fronteras y gruesas**.
"""),
        "fortran": ("""
program compon
   implicit none
   character(len=200) :: linea
   integer :: i, cnt
   logical :: en_palabra

   read(*, '(A)') linea
   cnt = 0
   en_palabra = .false.

   do i = 1, len_trim(linea)
      if (linea(i:i) == ' ') then
         en_palabra = .false.
      else if (.not. en_palabra) then
         en_palabra = .true.
         cnt = cnt + 1
      end if
   end do

   write(*, '(A,I0)') 'componentes=', cnt
end program compon
""", """
**Lo que esta clase enseña en Fortran.** El cálculo científico es **el ejemplo más claro de sistema
poliglota bien diseñado que existe hoy**, y merece verlo entero porque casi nadie lo reconoce como tal:

```text
Jupyter / línea de órdenes        ←  el usuario
       ↓
Python                             ←  guiones, preparación de datos, gráficas
       ↓  (NumPy, SciPy, f2py, ctypes)
C / C++                             ←  la capa de pegamento y las estructuras
       ↓
Fortran                              ←  BLAS, LAPACK, los núcleos numéricos
       ↓
ensamblador optimizado a mano         ←  las rutinas críticas de cada fabricante
       ↓
CUDA / OpenMP / MPI                    ←  paralelismo
```

**Cuando alguien escribe `numpy.linalg.solve(A, b)` en Python, está ejecutando Fortran** — LAPACK, con
una BLAS del fabricante debajo, escrita en parte en ensamblador.

Y la razón por la que ese reparto funciona es exactamente la del cierre de esta clase: **la frontera es
gruesa**.

**Una sola llamada cruza la frontera y hace millones de operaciones dentro.** Si el reparto fuera al
revés —Fortran llamando a Python en un bucle— el coste de cruzar se comería todo.

Es la regla práctica que hay que llevarse de esta parte: **la frontera se pone donde el trabajo por
llamada es grande**.

Y los mecanismos concretos de Fortran, que la clase 156 detalla:

| Mecanismo | Qué hace |
|---|---|
| **`iso_c_binding`** | interoperabilidad con C **en el estándar**, desde Fortran 2003 |
| **`f2py`** | genera un módulo de Python desde el fuente Fortran, automáticamente |
| **`ctypes` / `cffi`** | llamar a una biblioteca compartida desde Python |
| **Cython** | escribir el pegamento en algo parecido a Python |

**`f2py` merece la mención** porque es lo que hizo posible el ecosistema científico de Python: **lee el
fuente Fortran, deduce las interfaces y genera el envoltorio**, incluida la conversión de arreglos.

Y merece cerrar con una observación honesta sobre por qué Fortran sigue ahí: **no es inercia**. Es que
**para bucles anidados sobre arreglos, el compilador de Fortran genera código excelente** —los arreglos
no pueden solaparse por defecto, la forma es conocida, y la vectorización es directa— y **cincuenta años
de bibliotecas numéricas validadas no se reescriben porque sí**.
"""),
        "ada": ("""
with Ada.Text_IO; use Ada.Text_IO;
with Ada.Strings;
with Ada.Strings.Fixed;

procedure Compon is
   Linea      : String (1 .. 200);
   Ultimo     : Natural;
   Cnt        : Natural := 0;
   En_Palabra : Boolean := False;
begin
   Get_Line (Linea, Ultimo);

   for I in 1 .. Ultimo loop
      if Linea (I) = ' ' then
         En_Palabra := False;
      elsif not En_Palabra then
         En_Palabra := True;
         Cnt := Cnt + 1;
      end if;
   end loop;

   Put_Line ("componentes=" &
             Ada.Strings.Fixed.Trim (Cnt'Image, Ada.Strings.Both));
end Compon;
""", """
**Lo que esta clase enseña en Ada.** Ada tiene una particularidad que merece destacarse en esta clase:
**la interoperabilidad está en el estándar del lenguaje, con nombre y con reglas**.

```ada
pragma Convention (C, Mi_Tipo);
pragma Convention (Fortran, Mi_Matriz);      --  ¡Fortran, explícitamente!
pragma Convention (COBOL, Mi_Registro);       --  ¡y COBOL!
```

**El estándar de Ada define anexos completos de interfaz con C, con COBOL y con Fortran** —los anexos B.3,
B.4 y B.5—, con paquetes estándar:

```ada
with Interfaces.C;
with Interfaces.C.Strings;
with Interfaces.COBOL;
with Interfaces.Fortran;
```

**`Interfaces.Fortran` incluye el tipo `Fortran_Integer`, los complejos y —lo importante— la convención
de matrices por columnas** (clase 089). **`Interfaces.COBOL` incluye tipos decimales empaquetados y
cadenas con formato de imagen** (clase 072).

Es la única de esta página que trata la interoperabilidad como parte del lenguaje y no como una
biblioteca añadida, y viene de su origen: **Ada se diseñó para sistemas de defensa donde había que
integrar código existente de todo tipo**.

Y el dominio de Ada es un sistema poliglota típico, con un reparto que merece verse:

```text
Ada       ←  la lógica de control, las tareas, lo que se certifica
C          ←  los controladores de dispositivo y las bibliotecas del fabricante
ensamblador ←  el arranque, los vectores de interrupción, lo específico del chip
Simulink/SCADE ←  ¡el modelo del que se GENERA código Ada!
Python      ←  las herramientas de análisis y las pruebas en tierra
```

**La cuarta fila merece explicarse**, porque es un lenguaje que no lo parece: en aviación y automoción,
**buena parte del código de control no se escribe: se genera desde un modelo gráfico** —Simulink, SCADE—
que a su vez está certificado.

Y ahí la frontera entre lenguajes es de otro tipo: **el generador es parte de la cadena de herramientas
cualificada** (clase 144), y lo que se revisa es el modelo, no el Ada resultante.

Es un caso extremo de la observación de esta parte: **cuando un sistema tiene varias capas de
lenguajes, la pregunta importante es cuál de ellas es la fuente de verdad** — y no siempre es la que se
compila.
"""),
        "pascal": ("""
program Compon;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  Linea: string;
  I, Cnt: Integer;
  EnPalabra: Boolean;

begin
  ReadLn(Linea);
  Cnt := 0;
  EnPalabra := False;

  for I := 1 to Length(Linea) do
    if Linea[I] = ' ' then
      EnPalabra := False
    else if not EnPalabra then
    begin
      EnPalabra := True;
      Inc(Cnt);
    end;

  WriteLn('componentes=', IntToStr(Cnt));
end.
""", """
**Lo que esta clase enseña en Pascal.** El mundo Delphi es un caso de estudio interesante de esta clase,
porque **su propuesta era precisamente NO ser poliglota** — y aun así lo fue.

La promesa de Delphi era: **la interfaz, la lógica y el acceso a datos, todo en Object Pascal, en un
solo entorno**. Y funcionaba: es la razón de su éxito en los noventa.

**Y aun así, cualquier aplicación Delphi real tocaba al menos tres lenguajes más:**

```pascal
{ 1. La API de Windows: C }
function MessageBoxW(hWnd: HWND; lpText, lpCaption: PWideChar;
                     uType: UINT): Integer; stdcall;
                     external 'user32.dll' name 'MessageBoxW';

{ 2. SQL, en cualquier consulta }
Query.SQL.Text := 'SELECT ...';

{ 3. Ensamblador en línea, para lo crítico }
function Rapida(X: Integer): Integer; assembler;
asm
  MOV EAX, X
  SHL EAX, 1
end;
```

**Y `external 'user32.dll'` es la FFI de Pascal**, que la clase 156 detalla: una declaración normal con
la biblioteca y el nombre, y el compilador genera la llamada.

Y merece destacar lo bien resuelto que está: **`stdcall`, `cdecl`, `safecall` y `register` son
modificadores de la declaración** (clase 157), así que **la convención de llamada se declara donde se
usa** en lugar de configurarse globalmente.

Es de las interoperabilidades más cómodas de esta página, y explica por qué Delphi fue tan usado para
hacer interfaces gráficas sobre bibliotecas escritas en C.

Y la lección general que este caso enseña y que conviene extraer: **ningún lenguaje evita ser
poliglota, porque el sistema operativo ya es un lenguaje ajeno**.

Todo programa que dibuja una ventana, abre un fichero o usa la red **está llamando a una API escrita en
C**, con la convención de C y con los tipos de C. La única diferencia entre lenguajes es **cuánto de eso
se ve**.

Y esa es la observación que abre la clase 156: **C no es el lenguaje más usado — es el idioma común**.
"""),
        "lisp": ("""
(let ((linea (read-line))
      (cnt 0)
      (en-palabra nil))
  (loop for c across linea
        do (if (char= c #\\Space)
               (setf en-palabra nil)
               (unless en-palabra
                 (setf en-palabra t)
                 (incf cnt))))
  (format t "componentes=~D~%" cnt))
""", """
**Lo que esta clase enseña en Common Lisp.** Lisp tiene una historia con esta clase que merece contarse,
porque **intentó lo contrario y perdió**.

En los años ochenta existieron **las máquinas Lisp** —Symbolics, LMI, Xerox— **ordenadores cuyo sistema
operativo entero estaba escrito en Lisp**: el editor, el compilador, la red, los controladores de disco,
la interfaz gráfica. **Un solo lenguaje, de arriba abajo.**

Y era, por lo que cuentan quienes las usaron, un entorno extraordinario: **todo el sistema era
inspeccionable, modificable y depurable en marcha** — la Parte 8 de este curso llevada al sistema
operativo entero.

**Y desapareció**, por una razón que esta clase debe recoger: **el hardware genérico mejoró más rápido**.
Las estaciones Unix con procesadores estándar acabaron siendo más rápidas y mucho más baratas que las
máquinas especializadas, y **un ecosistema entero de un solo lenguaje no puede competir con uno donde
cada capa la hace quien mejor la hace**.

Es la lección más grande de esta clase: **el sistema poliglota no ganó por elegancia, ganó por
economía**.

Y el Lisp de hoy es plenamente poliglota, con una FFI excelente que la clase 156 detalla:

```lisp
(cffi:define-foreign-library libm (t (:default "libm")))
(cffi:use-foreign-library libm)

(cffi:defcfun ("sqrt" c-sqrt) :double (x :double))
(c-sqrt 2.0d0)     ; → 1.4142135623730951d0
```

**CFFI funciona en todas las implementaciones de Common Lisp**, y es un buen ejemplo de una biblioteca
que unificó lo que antes era distinto en cada una.

Y merece cerrar con la observación que conecta con la clase 163: **el papel que Lisp ocupa hoy en
sistemas poliglotas es el de lenguaje embebido de configuración y extensión**.

**Emacs Lisp** es el ejemplo mayor: un editor con un núcleo en C y **todo lo demás en Lisp**, extensible
en marcha. Y **AutoLISP** hace lo mismo en AutoCAD, y **GNU Guile** es el lenguaje de extensión oficial
del proyecto GNU.

Es exactamente la arquitectura de dos lenguajes de Ousterhout (clase 149), con Lisp en el papel del
lenguaje de guion.
"""),
        "tcl": ("""
gets stdin linea

puts "componentes=[llength [split [string trim $linea]]]"
""", """
**Lo que esta clase enseña en Tcl.** Tcl es el único lenguaje de esta página **diseñado explícitamente
para ser la mitad de un sistema poliglota**, y merece contarlo con las palabras de su autor.

**John Ousterhout creó Tcl en 1988 con un objetivo concreto**: sus estudiantes escribían herramientas de
diseño de circuitos, y **cada una inventaba su propio lenguaje de comandos, malo y distinto**.

Su idea fue: **una biblioteca de intérprete que cualquier programa en C pueda incorporar**, para que
todos compartan el mismo lenguaje de guion.

De ahí el nombre: **Tcl, *Tool Command Language***.

```c
/* Cualquier programa en C se convierte en programable en cuatro líneas */
Tcl_Interp *interp = Tcl_CreateInterp();
Tcl_CreateObjCommand(interp, "simular", SimularCmd, NULL, NULL);
Tcl_Eval(interp, "simular -pasos 1000");
Tcl_DeleteInterp(interp);
```

**Y funcionó**: hoy, **las herramientas de diseño de circuitos de Synopsys, Cadence y Xilinx exponen su
funcionalidad como comandos de Tcl** (clase 149), y los flujos de diseño de los chips que hay en
cualquier dispositivo están escritos en él.

Y la arquitectura que Ousterhout defendió en su artículo de 1998 —**dos lenguajes: uno de sistemas y uno
de guion**— es la observación central de esta clase:

| Capa | Lenguaje | Por qué |
|---|---|---|
| **Componentes** | C, C++, Rust | rendimiento, acceso al sistema, tipos estrictos |
| **Pegamento** | Tcl, Python, Lua | 5-10 veces menos código; **el 90 % de los cambios ocurre aquí** |

Y merece señalar cómo ha envejecido esa tesis, con honestidad: **el eje se ha desplazado**. Hoy hay
lenguajes que pretenden servir para las dos capas —Go, Rust con macros, Julia— y los lenguajes de guion
se han vuelto rápidos.

**Pero la observación de fondo sigue siendo cierta**: en casi todo sistema real hay una capa que cambia
todos los días y una que cambia cada año, **y no conviene que sean el mismo material**.

Y las herramientas de la frontera en Tcl, que la clase 156 detalla:

| Herramienta | Qué hace |
|---|---|
| **La API de C de Tcl** | crear comandos, manipular objetos, gestionar el intérprete |
| **SWIG** | **genera envoltorios automáticamente** desde cabeceras de C |
| **critcl** | **escribir C dentro de un guion Tcl**, compilado al vuelo |
| **TclOO + Tcl_Obj** | objetos de Tcl con representación dual (clase 152) |
"""),
        "perl": ("""
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;

my @componentes = split ' ', $linea;

print "componentes=", scalar(@componentes), "\\n";
""", """
**Lo que esta clase enseña en Perl.** Perl fue durante veinte años **el pegamento por excelencia de los
sistemas Unix**, y merece explicar qué significaba eso en la práctica.

```perl
# Un guion de administración típico de 1998 tocaba, en veinte líneas:
my @procesos = `ps aux`;                          # el shell
open(my $fh, '-|', 'ldapsearch', '-x', $filtro);   # LDAP
$dbh->do('UPDATE usuarios SET ...');                # SQL
system('/usr/sbin/sendmail', '-t');                  # el sistema de correo
print $socket "GET /estado HTTP/1.0\\r\\n\\r\\n";       # HTTP a mano
```

**Perl no reemplazaba nada: unía lo que ya había**, y eso es exactamente el papel de esta clase.

Y su ventaja concreta era que **manejaba bien la salida de todo lo demás**: la mayoría de los programas
de Unix hablan texto, y **Perl era el mejor procesando texto** (clase 093).

Es una observación que merece extraerse porque explica muchas decisiones de arquitectura: **el formato de
la frontera decide qué lenguaje es bueno en ella**. Cuando la frontera es texto de líneas, gana Perl;
cuando es JSON, gana cualquiera con un buen analizador; cuando es memoria compartida, gana quien hable
el ABI (clase 157).

Y Perl tiene la FFI más veterana y una de las más potentes de esta página, con dos generaciones que
conviene distinguir:

```perl
# XS (1994): un lenguaje INTERMEDIO que se compila a C
MODULE = Mi::Modulo   PACKAGE = Mi::Modulo
int
doblar(x)
    int x
  CODE:
    RETVAL = x * 2;
  OUTPUT:
    RETVAL
```

```perl
# FFI::Platypus (2015): sin compilar nada
use FFI::Platypus;
my $ffi = FFI::Platypus->new(api => 2);
$ffi->lib('libm.so.6');
$ffi->attach(sqrt => ['double'] => 'double');
print sqrt(2.0);
```

**XS da el máximo rendimiento y exige compilador; Platypus no compila nada y cuesta una indirección
más.**

Es exactamente el compromiso que la clase 156 desarrolla, y aparece en todos los ecosistemas: **enlazar
en compilación o descubrir en ejecución**.
"""),
        "cpp": ("""
#include <iostream>
#include <string>

int main() {
    std::string componente;
    int cnt = 0;
    while (std::cin >> componente) ++cnt;

    std::cout << "componentes=" << cnt << '\\n';
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** C++ ocupa en esta clase una posición que ningún otro lenguaje de la
página tiene: **es el sustrato sobre el que corren casi todos los demás**.

```text
CPython          ← escrito en C
V8 (JavaScript)   ← escrito en C++
JVM (HotSpot)      ← escrito en C++
SBCL               ← escrito en C y Lisp
Tcl, Perl, Ruby, PHP, Lua  ← escritos en C
SQLite, PostgreSQL, Redis   ← C
Los navegadores, los sistemas operativos, los compiladores  ← C y C++
```

**Cuando alguien escribe Python, está ejecutando C.** Y esa es la razón por la que **C es el idioma común
de la interoperabilidad**, que es la tesis de la clase 156.

Y merece precisar por qué, porque no es porque C sea especial: **es porque el ABI de C es el que todos
los sistemas operativos exponen** (clase 157). Las llamadas al sistema, las bibliotecas compartidas y los
formatos de objeto están definidos en términos de C.

Así que **para que dos lenguajes cualesquiera se entiendan, lo más fácil es que los dos hablen C** —
aunque ninguno de los dos sea C.

Y C++ añade a esta clase el problema que la clase 157 desarrolla y que merece anticipar aquí: **C++
mismo no sirve como idioma común**.

```cpp
extern "C" {                      // ← esto desactiva el decorado de nombres
    int doblar(int x);
}
```

**Sin `extern "C"`, el nombre de una función C++ se decora con su firma completa** —para permitir la
sobrecarga—, y el resultado **depende del compilador**:

```text
GCC:   _Z6doblari
MSVC:  ?doblar@@YAHH@Z
```

Y encima, **las clases, las plantillas, las excepciones y la biblioteca estándar no tienen ABI
estable** (clase 143).

De ahí la práctica universal en bibliotecas C++ pensadas para ser usadas desde fuera: **exponer una
interfaz en C** —punteros opacos y funciones libres— **aunque por dentro sea C++ moderno**.

Es la aplicación más literal de la regla del cierre de esta clase: **la frontera se diseña, y se diseña
estrecha y estable** — porque todo lo que cruce será difícil de cambiar después.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi COMPON;
  linea char(200) const;
end-pi;

dcl-s i     int(10);
dcl-s cnt   int(10);
dcl-s enpal ind;

cnt = 0;
enpal = *off;

for i = 1 to %len(%trimr(linea));
  if %subst(linea : i : 1) = ' ';
    enpal = *off;
  elseif not enpal;
    enpal = *on;
    cnt += 1;
  endif;
endfor;

dsply ('componentes=' + %char(cnt));

*inlr = *on;
return;
""", """
**Lo que esta clase enseña en RPG.** IBM i es, probablemente, **la plataforma más poliglota de esta
página**, y su forma de serlo merece explicarse porque es distinta de todas las demás: **los lenguajes
comparten el proceso, no solo la máquina**.

```text
En un mismo TRABAJO de IBM i pueden convivir:
  RPG          ← la lógica de negocio de 1992
  COBOL         ← otro módulo, del mismo sistema
  C y C++        ← utilidades y APIs
  CL             ← el lenguaje de control: orquestación
  SQL             ← acceso a datos, embebido o dinámico
  Java            ← una JVM dentro del mismo trabajo
  Node.js, Python, PHP  ← en PASE, el entorno AIX integrado
```

**Y se llaman entre sí directamente**, con paso de parámetros, sin serializar y sin salir del proceso:

```rpgle
// RPG llamando a una función de C
dcl-pr strlen int(10) extproc('strlen');
  cadena pointer value options(*string);
end-pr;

// RPG llamando a un método Java
dcl-pr crear object(*JAVA : 'java.math.BigDecimal') extproc(*JAVA : ...);
```

**`extproc` en un prototipo es toda la FFI que hace falta** (clase 156): se declara la función externa
con su convención, y se llama como cualquier otra.

Y el mecanismo que hace esto posible merece destacarse: **el modelo de ILE, *Integrated Language
Environment***.

```text
Fuentes de varios lenguajes  →  MÓDULOS (*MODULE)
Módulos de varios lenguajes   →  un PROGRAMA (*PGM) o un programa de servicio
```

**Los módulos de RPG, COBOL, C y CL se enlazan juntos en el mismo objeto**, comparten grupo de
activación, comparten el manejo de condiciones y comparten la pila.

Es una interoperabilidad más profunda que la de la mayoría de las plataformas, y viene de una decisión
deliberada de 1993: **definir un modelo común de llamada, de almacenamiento y de excepciones, y hacer que
todos los compiladores lo respeten**.

Es exactamente el problema que la clase 157 llama ABI, resuelto a nivel de plataforma **para varios
lenguajes a la vez**, en lugar de que cada uno se adapte al de C.
"""),
        "pli": ("""
 compon: procedure options(main);

    declare linea  char(200) varying;
    declare i      fixed binary(31);
    declare cnt    fixed binary(31) initial(0);
    declare enpal  bit(1) initial('0'b);

    get edit (linea) (a(200));

    do i = 1 to length(linea);
       if substr(linea, i, 1) = ' ' then
          enpal = '0'b;
       else if ^enpal then
          do;
             enpal = '1'b;
             cnt = cnt + 1;
          end;
    end;

    put skip list ('componentes=' || trim(char(cnt)));

 end compon;
""", """
**Lo que esta clase enseña en PL/I.** PL/I es el intento más ambicioso de la historia de **evitar** el
sistema poliglota, y merece contarlo porque su fracaso es instructivo.

**El objetivo declarado de IBM en 1964 era sustituir a Fortran y a COBOL con un solo lenguaje**, y
además cubrir la programación de sistemas para no necesitar ensamblador:

| Necesidad | Lo que PL/I incorporó |
|---|---|
| Cálculo científico | coma flotante, complejos, arreglos, `FIXED BINARY` |
| Gestión comercial | decimal empaquetado, imágenes de edición, ficheros de registros |
| Programación de sistemas | punteros, `BASED`, `AREA`, control de almacenamiento |
| Concurrencia | `TASK`, `EVENT`, `WAIT` |
| Manejo de errores | las condiciones `ON` (clase 103) |

**Y funcionó lo suficiente como para escribir Multics en él** —el sistema operativo precursor de Unix
(clase 149)—, que era la prueba más dura posible.

**Y aun así no sustituyó a nadie.** Fortran siguió en cálculo, COBOL siguió en gestión, y el ensamblador
siguió donde hacía falta.

Y las razones merecen enunciarse porque se repiten cada vez que alguien intenta lo mismo:

**Uno, el coste de cambiar.** Las organizaciones ya tenían millones de líneas y personas formadas.
Migrar no daba beneficio inmediato.

**Dos, el tamaño** (clase 154). Un lenguaje que sirve para todo es un lenguaje que nadie domina entero, y
eso tiene un coste diario.

**Y tres, y es la más importante: los especialistas ganan.** El compilador de Fortran optimizaba mejor
los bucles numéricos porque **su lenguaje le daba más garantías** —arreglos que no se solapan, sin
punteros—. PL/I, al permitirlo todo, **podía suponer menos**.

Es una constante del diseño de lenguajes que esta clase debe dejar clara: **la potencia de un lenguaje y
lo que su compilador puede garantizar están en tensión**, y un lenguaje que lo permite todo no puede
prometer casi nada.

Y por eso el sistema poliglota gana: **cada frontera es también una frontera de suposiciones**, y dentro
de cada una se puede optimizar y verificar con reglas más fuertes.
"""),
        "mumps": ("""
COMPON ; Contar componentes -- clase 155
 read linea
 new i, cnt, p
 set cnt = 0
 for i = 1:1:$length(linea, " ") do
 . set p = $piece(linea, " ", i)
 . if p '= "" set cnt = cnt + 1
 write "componentes=", cnt, !
 quit
""", """
**Lo que esta clase enseña en M.** VistA es un sistema poliglota de una forma peculiar y que merece
describirse, porque el reparto no es por capas técnicas sino **por épocas**:

```text
M                ← el núcleo clínico: 1980-hoy, millones de líneas
FileMan            ← el "lenguaje" de definición de datos, encima de M (clase 149)
Delphi              ← CPRS, la interfaz gráfica clínica, de los años 2000
Java / JavaScript    ← las capas web modernas
Python               ← análisis de datos y aprendizaje automático
C                     ← las extensiones de la implementación de M
```

**Y la frontera entre M y todo lo demás tiene nombre propio en este mundo: *RPC Broker***.

```text
El cliente Delphi o web se conecta por TCP a un proceso M,
envía el nombre de una "llamada a procedimiento remoto" registrada y sus parámetros,
y recibe el resultado como texto.
```

**Es una frontera de proceso, con serialización de texto**, que es la primera de las tres del cierre de
esta clase: **la más simple, la más aislada y la más lenta**.

Y la decisión fue correcta, y merece explicar por qué: **permitió poner una interfaz gráfica moderna
sobre un núcleo de veinte años sin tocarlo**, y **cambiar la interfaz tres veces sin que el núcleo se
enterara**.

Es el patrón del estrangulador de la clase 150, aplicado a la capa de presentación, y la frontera está
exactamente donde el cierre de esta clase la pondría: **pocas llamadas, con mucho trabajo cada una**.

Y las implementaciones modernas de M añaden las otras dos fronteras:

| Mecanismo | Nota |
|---|---|
| **`$ZCALL` / *Call-In / Call-Out*** | llamar a C desde M y a M desde C, en el mismo proceso |
| **YottaDB con envoltorios** | APIs para Go, Rust, Python, Node y Perl |
| **InterSystems IRIS** | Java, .NET, Python **dentro** de la máquina virtual |

**La segunda fila es el cambio de la última década**: YottaDB expuso las globals a otros lenguajes, así
que **un programa en Go o en Python puede leer y escribir la misma base de datos que las rutinas M**, con
las mismas transacciones.

Es la frontera de biblioteca compartida, y convierte a M de lenguaje aislado en **motor de base de datos
usable desde cualquier sitio** — que es, probablemente, su futuro más probable.
"""),
        "smalltalk": ("""
| linea |

linea := stdin nextLine trimBoth.

Transcript show: 'componentes=', (linea substrings: ' ') size printString; cr.
""", """
**Lo que esta clase enseña en Smalltalk.** Smalltalk comparte con Lisp la historia de esta página —**se
intentó hacer un sistema entero en un solo lenguaje**— y merece ver dónde acabó la frontera.

**El Smalltalk-80 original era casi todo Smalltalk**, incluidos el compilador, el depurador, el editor y
la interfaz gráfica (Parte 8). Debajo había solo **una máquina virtual pequeña**, y **una lista de
primitivas**:

```smalltalk
SmallInteger >> + aNumber
    <primitive: 1>                    "← la VM lo hace; si falla, sigue el código Smalltalk"
    ^ super + aNumber
```

**`<primitive: N>` es la frontera**: si la máquina virtual sabe hacerlo rápido, lo hace; **si no
—desbordamiento, tipo inesperado—, ejecuta el código Smalltalk que hay debajo**.

Es un diseño elegante y merece destacarlo: **la frontera tiene una vía de respaldo escrita en el lenguaje
de arriba**, así que el sistema es completo aunque la primitiva no cubra todos los casos.

Y la FFI moderna, que la clase 156 detalla:

```smalltalk
"Pharo: UFFI"
LibC >> ticksNow
    ^ self ffiCall: #( uint clock() )

"Declarar una llamada a una biblioteca C es un MÉTODO"
```

**`ffiCall:` con la firma de C escrita como un literal** es una de las FFI más limpias de esta página: no
hay fichero de definiciones aparte ni generación de envoltorios; **la declaración vive en el método que
la usa**.

Y merece cerrar con dónde está Smalltalk en los sistemas poliglotas de hoy, porque hay un caso que vale
la pena conocer:

**GemStone/S** (clase 148) se usa como **capa de objetos transaccional** dentro de sistemas cuyo resto
está en Java o en Python — el papel de base de datos de objetos, no de lenguaje de aplicación.

Y **Pharo** se usa mucho como **herramienta de análisis de otros lenguajes**: el proyecto **Moose**
importa código Java, C++, COBOL o Python **como objetos Smalltalk** y permite explorarlo, medirlo y
visualizarlo con toda la potencia del entorno vivo.

Es un giro curioso y muy propio de esta clase: **el lenguaje que quiso ser un mundo cerrado acabó siendo
bueno en analizar los mundos de los demás** — porque lo que mejor hace, desde 1980, es **representar
cosas como objetos y dejar preguntarles**.
"""),
    },
)

# ---------------------------------------------------------------------------
# 156 — La FFI: llamar a C desde todos
# ---------------------------------------------------------------------------
SPECS["156"] = dict(
    gancho="""
Doblar un número llamando a una función externa. Es el "hola mundo" de la interoperabilidad, y la
pregunta que hay detrás es **por qué siempre es C**. La respuesta no es que C sea mejor: es que **el ABI
de C es el que los sistemas operativos exponen** (clase 157), así que **hablar C es hablar con el
sistema**. Y esta página tiene los dos extremos: **Ada declara la interfaz con un `pragma` del
estándar**, y **RPG llama a una función de C con la misma sintaxis con que llama a un procedimiento
propio**.
""",
    porque="""
Aquí el concepto es la **interfaz de función externa**, y estos lenguajes la enseñan porque **todos
tuvieron que resolverla y llegaron a soluciones muy distintas**: en el estándar del lenguaje (Ada,
Fortran 2003, RPG), con un lenguaje intermedio que se compila (Perl con XS, Tcl con SWIG), con
descubrimiento en ejecución (CFFI en Lisp, FFI::Platypus en Perl, UFFI en Smalltalk) o simplemente
declarando la biblioteca (Pascal).

Y aparecen los cuatro problemas que toda FFI tiene que resolver: **los nombres, los tipos, la memoria y
los errores**.
""",
    cierre="""
Lo transferible: **una llamada a través de una FFI parece una llamada normal y no lo es**. Cruza cuatro
fronteras a la vez —**el nombre**, que puede estar decorado; **los tipos**, que hay que traducir;
**la memoria**, donde hay que decidir quién reserva y quién libera; y **los errores**, porque las
excepciones no cruzan—. De ahí la práctica que evita casi todos los fallos: **envolver la FFI en una
capa fina propia**, que traduzca los tipos, gestione la memoria y convierta los códigos de error en la
forma nativa del lenguaje — y no dejar que el resto del programa vea nunca la interfaz cruda.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. LLAMAR.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(40).
01  N       PIC S9(9) COMP-5.
01  R       PIC S9(9) COMP-5.
01  ED      PIC -(8)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    COMPUTE N = FUNCTION NUMVAL(LINEA)

    CALL "DOBLAR" USING N R

    MOVE R TO ED
    DISPLAY "resultado=" FUNCTION TRIM(ED)
    STOP RUN.

IDENTIFICATION DIVISION.
PROGRAM-ID. DOBLAR.
DATA DIVISION.
LINKAGE SECTION.
01  X       PIC S9(9) COMP-5.
01  Y       PIC S9(9) COMP-5.
PROCEDURE DIVISION USING X Y.
    COMPUTE Y = X * 2.
    GOBACK.
END PROGRAM DOBLAR.
END PROGRAM LLAMAR.
""", """
**Lo que esta clase enseña en COBOL.** El programa define **un programa anidado** y lo llama con `CALL
... USING`, sin más — y **ahí está la primera lección**: eso es **paso por referencia**, el modo por
defecto de COBOL, y **no es lo que C espera**.

Y hay tres detalles que merecen explicarse, porque son los cuatro problemas del cierre de esta clase:

**Primero, `COMP-5`.** COBOL tiene varios formatos numéricos binarios:

```cobol
       01  A PIC S9(9) COMP.      *> binario, pero LIMITADO al rango decimal declarado
       01  B PIC S9(9) COMP-5.     *> binario NATIVO de la máquina: el int de C
```

**`COMP-5` es el tipo que corresponde a un `int` de C**; `COMP` puede truncar al rango de nueve dígitos
decimales. **Usar el tipo equivocado es el error de FFI más frecuente en COBOL.**

**Segundo, `BY VALUE` frente a `BY REFERENCE`.** Y aquí está la trampa que la clase 157 desarrolla:

```cobol
           CALL "func" USING BY REFERENCE N      *> el DEFECTO de COBOL: pasa la DIRECCIÓN
           CALL "func" USING BY VALUE N           *> lo que C espera para un int
```

**COBOL pasa por referencia por defecto y C espera por valor.** Una llamada sin `BY VALUE` **pasa un
puntero donde la función espera un número**, y el resultado es un valor absurdo o una caída.

**Y tercero, las cadenas.** C termina las cadenas con un byte cero; **COBOL usa longitud fija con
espacios de relleno** (clase 093):

```cobol
       01  NOMBRE-C PIC X(51).
           ...
           STRING FUNCTION TRIM(WS-NOMBRE) X"00" DELIMITED BY SIZE
               INTO NOMBRE-C
           END-STRING
           CALL "puts" USING BY REFERENCE NOMBRE-C
```

**Hay que añadir el cero explícitamente**, y reservar sitio para él.

Es la traducción de tipos del cierre de esta clase en su forma más concreta, y es la razón por la que la
recomendación —**envolver la FFI en una capa propia**— vale tanto aquí: **un programa COBOL que añada el
cero en veinte sitios lo hará mal en alguno**.
"""),
        "fortran": ("""
module enlace_c
   use iso_c_binding
   implicit none
contains

   ! bind(C) fija el nombre del símbolo; value, el paso por valor de C.
   pure function doblar(x) bind(C, name='doblar') result(r)
      integer(c_int), value :: x
      integer(c_int) :: r
      r = 2 * x
   end function doblar

end module enlace_c

program llamar
   use iso_c_binding
   use enlace_c
   implicit none
   integer :: n

   read(*, *) n
   write(*, '(A,I0)') 'resultado=', doblar(int(n, c_int))
end program llamar
""", """
**Lo que esta clase enseña en Fortran.** El programa muestra **`iso_c_binding`**, que es la
interoperabilidad con C **en el estándar de Fortran desde 2003**, y merece explicar cada pieza porque
resuelve los cuatro problemas del cierre.

**`bind(C, name='doblar')`** resuelve **los nombres**: sin él, gfortran decoraría el símbolo como
`doblar_` con un guion bajo (clase 137), y el enlazador no lo encontraría.

**`integer(c_int)`** resuelve **los tipos**: `iso_c_binding` define `c_int`, `c_double`, `c_char`,
`c_ptr`, `c_size_t` y compañía, **con el tamaño exacto que tienen en C en esa plataforma**.

**`value`** resuelve la convención de paso, y es el punto crítico: **Fortran pasa TODO por referencia
por defecto**.

```fortran
integer(c_int), value :: x        ! por VALOR: lo que C espera
integer(c_int) :: y                ! por REFERENCIA: C recibiría un puntero
```

Es exactamente la misma trampa que COBOL en esta página, y **la causa número uno de fallos al llamar a C
desde Fortran**.

Y las cadenas merecen su apartado, porque son el caso más laborioso:

```fortran
character(kind=c_char, len=1), dimension(*) :: cadena     ! un arreglo, no una cadena
! y hay que añadir c_null_char al final
nombre_c = trim(nombre) // c_null_char
```

**Una cadena de Fortran no lleva terminador y sí lleva longitud implícita** —que se pasa como un
**argumento oculto** (clase 157)—, así que **hay que construir un arreglo de caracteres terminado en
cero a mano**.

Y en el otro sentido, **`c_f_pointer` convierte un puntero de C en un arreglo de Fortran con forma**:

```fortran
type(c_ptr) :: p
real(c_double), pointer :: v(:)
call c_f_pointer(p, v, [n])       ! ahora v es un arreglo de Fortran normal
```

**Eso es lo que hace posible que NumPy y Fortran compartan memoria sin copiar** (clase 155), y es la
pieza que convierte una llamada cara en una barata.

Y merece señalar el antes y el después: **hasta 2003, todo esto se hacía adivinando** —el guion bajo, el
tamaño de los enteros, el orden de los argumentos ocultos— **y dependía del compilador**. `iso_c_binding`
lo convirtió en estándar y portable, y es una de las mejoras más importantes del Fortran moderno.
"""),
        "ada": ("""
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;
with Interfaces.C;

procedure Llamar is
   use type Interfaces.C.int;

   function Doblar (X : Interfaces.C.int) return Interfaces.C.int is (2 * X);

   N : Integer;
begin
   Get (N);

   Put ("resultado=");
   Put (Integer (Doblar (Interfaces.C.int (N))), Width => 1);
   New_Line;
end Llamar;
""", """
**Lo que esta clase enseña en Ada.** Ada tiene **la interfaz con C mejor integrada de esta página**, y
merece ver por qué: **está en el estándar, con tipos propios y con comprobación**.

```ada
with Interfaces.C; use Interfaces.C;

--  Importar una función de C
function C_Sqrt (X : double) return double
  with Import => True, Convention => C, External_Name => "sqrt";

--  Exportar una función de Ada para que la llame C
procedure Mi_Callback (V : int)
  with Export => True, Convention => C, External_Name => "mi_callback";
```

**`Import`, `Convention` y `External_Name` son aspectos del estándar**, y con ellos:

- **`Convention => C`** hace que el compilador use la convención de llamada y el paso por valor de C.
- **`External_Name`** resuelve el problema de los nombres, sin ambigüedad.
- **Y `Export` funciona en la otra dirección**, para que C llame a Ada.

Y `Interfaces.C` define los tipos con los nombres de C —`int`, `long`, `unsigned`, `double`, `char`,
`size_t`— **con el tamaño correcto de la plataforma**, más los paquetes hijos:

```ada
with Interfaces.C.Strings;    --  chars_ptr: cadenas terminadas en cero
with Interfaces.C.Pointers;    --  aritmética de punteros al estilo de C
```

**`Interfaces.C.Strings` merece la mención** porque resuelve el tercer problema del cierre —**la
memoria**— de forma explícita:

```ada
declare
   P : chars_ptr := New_String ("hola");     --  RESERVA con malloc
begin
   Llamar_A_C (P);
   Free (P);                                  --  y hay que LIBERAR
end;
```

**El tipo obliga a decidir quién libera**, en lugar de dejarlo implícito.

Y Ada tiene una capacidad de esta clase que ningún otro lenguaje de la página ofrece igual: **generar los
enlaces automáticamente desde las cabeceras de C**.

```bash
g++ -fdump-ada-spec -C /usr/include/sqlite3.h
```

**El compilador de GNAT lee un `.h` de C y produce la especificación Ada equivalente**, con los tipos,
las constantes y los `pragma` correctos.

Es lo que en otros ecosistemas hacen herramientas externas —SWIG, bindgen, cgo—, y aquí lo hace el
propio compilador porque **ya tiene que entender C para la interoperabilidad del estándar**.
"""),
        "pascal": ("""
program Llamar;
{$MODE OBJFPC}{$H+}
uses SysUtils;

{ Una función con la convención de llamada de C: así se declara y así se exporta }
function Doblar(X: LongInt): LongInt; cdecl;
begin
  Result := 2 * X;
end;

var
  N: LongInt;

begin
  Read(N);
  WriteLn('resultado=', IntToStr(Doblar(N)));
end.
""", """
**Lo que esta clase enseña en Pascal.** El modificador **`cdecl`** de la declaración es toda la FFI de
Pascal: **la convención de llamada es parte de la firma** (clase 157).

Y llamar a una biblioteca externa es igual de directo:

```pascal
function sqrt(X: Double): Double; cdecl; external 'm' name 'sqrt';
function MessageBoxW(hWnd: HWND; lpText, lpCaption: PWideChar;
                     uType: UINT): Integer; stdcall; external 'user32.dll';

{ o cargando en ejecución }
var H: TLibHandle;
begin
  H := LoadLibrary('milib.so');
  @MiFuncion := GetProcedureAddress(H, 'mi_funcion');
```

**`external 'lib' name 'símbolo'` en la propia declaración** es de las formas más limpias de esta
página: no hay fichero aparte, ni generación, ni configuración.

Y Pascal resuelve los cuatro problemas del cierre con tipos del lenguaje:

| Problema | Solución en Pascal |
|---|---|
| **Nombres** | `name 'símbolo'` en la declaración |
| **Convención** | `cdecl`, `stdcall`, `safecall`, `register`, `varargs` |
| **Tipos** | `LongInt`, `Int64`, `PChar`, `PWideChar`, `Pointer`, `PtrInt` |
| **Cadenas** | `PChar` es la cadena de C; conversión explícita desde `string` |
| **Memoria** | `GetMem`/`FreeMem` frente a las del sistema; hay que saber cuál usar |

**La fila de las cadenas merece el detalle**, porque es donde se cometen los errores:

```pascal
var S: string;
    P: PChar;
begin
  S := 'hola';
  P := PChar(S);         { válido MIENTRAS S exista y no se modifique }
  LlamarA_C(P);
```

**`PChar(S)` no copia: apunta dentro de la cadena de Pascal**, que tiene conteo de referencias (clase
131). **Si `S` se libera o se modifica mientras C usa el puntero, es un uso después de liberar.**

Es exactamente el tercer problema del cierre —**quién es dueño de la memoria y hasta cuándo**— y es la
fuente de fallos más común de cualquier FFI, en cualquier lenguaje.

Y la buena noticia es que Free Pascal facilita ir en la otra dirección: **compilar una biblioteca
compartida que C pueda usar**.

```pascal
library milib;
function doblar(x: LongInt): LongInt; cdecl;
begin Result := 2 * x; end;
exports doblar;
begin end.
```
"""),
        "lisp": ("""
(defun doblar (x) (* 2 x))

(let ((n (read)))
  (format t "resultado=~D~%" (doblar n)))
""", """
**Lo que esta clase enseña en Common Lisp.** El programa es puro Lisp porque en el verificador no hay
biblioteca externa que enlazar, pero **la FFI de Lisp es una de las más cómodas de esta página**, y
merece verla.

```lisp
(ql:quickload :cffi)

(cffi:define-foreign-library libm
  (:unix (:or "libm.so.6" "libm.so"))
  (t (:default "libm")))
(cffi:use-foreign-library libm)

(cffi:defcfun ("sqrt" c-sqrt) :double
  (x :double))

(c-sqrt 2.0d0)      ; → 1.4142135623730951d0
```

**Y la propiedad que la distingue de todas las compiladas de esta página: no compila nada.**

CFFI **carga la biblioteca en ejecución y construye la llamada al vuelo**, así que:

- **No hace falta compilador de C** en la máquina del usuario.
- **Se puede probar y ajustar en el REPL**, sin ciclo de compilación (clase 124).
- **Y una firma equivocada se corrige y se reevalúa al instante.**

Y esa última es también el peligro, y merece decirlo: **una firma equivocada no da error de
compilación**. Declarar `:int` donde el C real usa `:long` **compila, ejecuta y corrompe la pila**.

Es el segundo problema del cierre —**los tipos**— sin la red que un enlazador da.

Y CFFI resuelve el tercero, la memoria, con construcciones explícitas:

```lisp
(cffi:with-foreign-object (buf :char 256)      ; reservado y LIBERADO al salir
  (c-gets buf 256)
  (cffi:foreign-string-to-lisp buf))

(cffi:with-foreign-string (s "hola")            ; convierte y libera
  (c-puts s))
```

**Las macros `with-...` garantizan la liberación aunque haya una excepción** — que es el mismo patrón que
`unwind-protect` y RAII (clase 132), aplicado a la memoria de la otra parte.

Y el cuarto problema, **los errores**, merece la advertencia porque es específico de los lenguajes con
recolector: **una función de C que llame de vuelta a Lisp y ese Lisp señale una condición no puede
desenrollar la pila de C con seguridad**.

```lisp
(cffi:defcallback mi-callback :int ((x :int))
  (handler-case (procesar x)
    (error () -1)))       ; ← capturar SIEMPRE dentro de una retrollamada
```

**Toda retrollamada debe capturar sus propios errores y devolver un código**, nunca dejar que una
condición cruce la frontera. Es una regla universal de las FFI y una de las que más veces se olvida.
"""),
        "tcl": ("""
gets stdin linea
set n [string trim $linea]

proc doblar {x} { expr {2 * $x} }

puts "resultado=[doblar $n]"
""", """
**Lo que esta clase enseña en Tcl.** Tcl fue diseñado para esta clase (clase 155), así que su
interoperabilidad con C no es una FFI añadida: **es el mecanismo principal del lenguaje**.

```c
/* Un comando de Tcl escrito en C */
static int DoblarCmd(ClientData cd, Tcl_Interp *interp,
                     int objc, Tcl_Obj *const objv[]) {
    int x;
    if (objc != 2) { Tcl_WrongNumArgs(interp, 1, objv, "x"); return TCL_ERROR; }
    if (Tcl_GetIntFromObj(interp, objv[1], &x) != TCL_OK) return TCL_ERROR;
    Tcl_SetObjResult(interp, Tcl_NewIntObj(2 * x));
    return TCL_OK;
}
```

Y merece señalar las tres cosas que ese fragmento hace bien y que son los problemas del cierre de esta
clase:

**`Tcl_GetIntFromObj` convierte y valida a la vez**, dejando el mensaje de error en el intérprete: **la
conversión de tipos y el manejo de errores son la misma llamada**.

**`Tcl_NewIntObj` crea un objeto de Tcl con conteo de referencias**, así que **la memoria la gestiona
Tcl**: no hay duda de quién libera.

**Y devolver `TCL_ERROR` convierte el fallo en una excepción de Tcl**, con su traza (clase 137). **Los
errores cruzan la frontera correctamente**, que es lo que casi ninguna FFI de esta página consigue.

Y el ecosistema tiene tres formas de llegar ahí, cada una con su punto en el compromiso:

| Herramienta | Notas |
|---|---|
| **La API de C directa** | control total; hay que escribir el envoltorio a mano |
| **SWIG** | **lee las cabeceras de C++ y genera el envoltorio**, para Tcl, Python, Perl, Ruby... |
| **critcl** | **escribir C dentro del guion Tcl**, compilado y cacheado al vuelo |
| **Ffidl / cffi** | llamar a bibliotecas sin compilar nada, como CFFI en Lisp |

**critcl merece el detalle** porque es una idea poco común:

```tcl
package require critcl
critcl::cproc doblar {int x} int { return 2 * x; }
```

**Ese C se compila la primera vez que se ejecuta el guion y se guarda en caché.** El resultado es un
guion Tcl que **contiene su propio código C**, sin proyecto ni sistema de construcción.

Es la respuesta más práctica al problema de la clase 155 —**la capa de guion y la de sistemas en el mismo
sitio**— y anticipa lo que hoy hacen Cython, Numba y las extensiones en línea de varios lenguajes.
"""),
        "perl": ("""
use strict;
use warnings;

sub doblar { return 2 * $_[0] }

my $n = <STDIN>;
chomp $n;

print "resultado=", doblar($n), "\\n";
""", """
**Lo que esta clase enseña en Perl.** Perl tiene **dos FFI de generaciones distintas**, y compararlas es
la mejor forma de ver el compromiso central de esta clase.

**XS (1994): un lenguaje intermedio que se compila a C.**

```c
MODULE = Mi::Modulo    PACKAGE = Mi::Modulo

int
doblar(x)
    int x
  CODE:
    RETVAL = x * 2;
  OUTPUT:
    RETVAL
```

**`xsubpp` traduce eso a C**, se compila y se enlaza como un módulo binario.

- **A favor**: la llamada es **casi tan rápida como una llamada de C**, y se tiene acceso completo a las
  estructuras internas de Perl.
- **En contra**: hace falta **un compilador de C en la máquina que instala**, y XS es un lenguaje más que
  aprender —con `SV*`, `AV*`, `HV*`, las macros de la pila y el conteo de referencias a mano—.

**FFI::Platypus (2015): descubrimiento en ejecución.**

```perl
use FFI::Platypus 2.00;
my $ffi = FFI::Platypus->new(api => 2, lib => ['libm.so.6']);
$ffi->attach(sqrt => ['double'] => 'double');
print sqrt(2.0);
```

- **A favor**: **no compila nada**, se prueba al instante, y funciona con cualquier biblioteca
  compartida.
- **En contra**: cuesta una indirección por llamada, y **un tipo mal declarado corrompe memoria sin
  aviso**.

**Y esa comparación es la de toda esta clase**: **enlazar en compilación** —rápido, comprobado, exige
herramientas— **frente a descubrir en ejecución** —flexible, inmediato, sin red—.

Aparece igual en Lisp (CFFI frente a extensiones compiladas), en Python (extensiones C frente a
`ctypes`), en Tcl (la API de C frente a Ffidl) y en Java (JNI frente al Panamá moderno).

Y Perl aporta a esta clase una advertencia sobre el cuarto problema del cierre —**los errores**— que es
suya y merece conocerse: **`die` dentro de una retrollamada llamada desde C**.

```perl
# ✗ el die intenta desenrollar la pila de Perl... a través de marcos de C
$ffi->closure(sub { die "error" });

# ✓ capturar dentro y devolver un código
$ffi->closure(sub { eval { procesar(@_); 1 } or return -1; return 0 });
```

**Dejar que una excepción cruce marcos de C produce fugas o caídas**, porque C no sabe deshacer lo que
tenía a medias. Es la misma regla que en Lisp en esta página, y vale para cualquier lenguaje con
excepciones.
"""),
        "cpp": ("""
#include <iostream>

// Con enlace de C: nombre sin decorar, para que cualquier lenguaje lo llame.
extern "C" long long doblar(long long x) {
    return 2 * x;
}

int main() {
    long long n{};
    if (!(std::cin >> n)) return 1;

    std::cout << "resultado=" << doblar(n) << '\\n';
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** El `extern "C"` del programa es **la pieza central de toda esta
página**, y merece explicar exactamente qué hace: **desactiva el decorado de nombres y usa la convención
de llamada de C**.

```cpp
long long doblar(long long);                 // símbolo: _Z6doblarx  (GCC)
extern "C" long long doblar(long long);       // símbolo: doblar
```

**Sin él, ningún otro lenguaje encuentra la función**, porque el nombre decorado incluye los tipos de los
argumentos y **el esquema de decorado es distinto en cada compilador** (clase 157).

Y la forma habitual en una cabecera que sirva para C y para C++:

```cpp
#ifdef __cplusplus
extern "C" {
#endif

int doblar(int x);

#ifdef __cplusplus
}
#endif
```

Y merece enunciar con claridad **qué se puede y qué no se puede exponer** por esa frontera, porque es la
regla práctica de esta clase:

| Se puede exponer | No se puede |
|---|---|
| Funciones libres con tipos de C | **clases, métodos, plantillas** |
| Punteros opacos (`typedef struct T T;`) | **`std::string`, `std::vector`** en la firma |
| `struct` con disposición simple | **excepciones**: no cruzan |
| Enteros, reales, punteros | **sobrecargas**: C no las tiene |

**Y la técnica estándar para exponer una clase C++ es el puntero opaco**:

```cpp
extern "C" {
    typedef struct Motor Motor;             // tipo incompleto: opaco
    Motor* motor_crear(void);
    int    motor_procesar(Motor* m, int x);
    void   motor_destruir(Motor* m);
}
```

```cpp
struct Motor { MiClaseCpp impl; };          // por dentro, C++ moderno
extern "C" Motor* motor_crear() { return new Motor{}; }
extern "C" void motor_destruir(Motor* m) { delete m; }
```

**Ese patrón —crear, operar, destruir, con un puntero opaco— es la forma canónica de exponer C++ a
cualquier lenguaje**, y resuelve los cuatro problemas del cierre: los nombres con `extern "C"`, los tipos
con enteros y punteros, la memoria con una pareja explícita crear/destruir, y los errores con códigos de
retorno.

Y la última regla, que hay que aplicar sin excepción: **ninguna excepción de C++ puede salir de una
función `extern "C"`**.

```cpp
extern "C" int motor_procesar(Motor* m, int x) {
    try { return m->impl.procesar(x); }
    catch (...) { return -1; }              // capturar TODO en la frontera
}
```

**Dejar escapar una excepción por una función con enlace de C es comportamiento indefinido**, y en la
práctica es una terminación abrupta del proceso.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi LLAMAR;
  n int(10) const;
end-pi;

// Prototipo con la convencion de C: extproc y value
dcl-pr doblar int(10) extproc('doblar');
  x int(10) value;
end-pr;

dcl-proc doblar export;
  dcl-pi *n int(10);
    x int(10) value;
  end-pi;
  return 2 * x;
end-proc;

dsply ('resultado=' + %char(doblar(n)));

*inlr = *on;
return;
""", """
**Lo que esta clase enseña en RPG.** Aquí está el caso del gancho: **en RPG, llamar a una función de C es
declarar un prototipo**.

```rpgle
// La biblioteca estándar de C, desde RPG
dcl-pr strlen uns(10) extproc('strlen');
  cadena pointer value options(*string);
end-pr;

dcl-pr malloc pointer extproc('malloc');
  tamano uns(10) value;
end-pr;

dcl-pr sqrt float(8) extproc('sqrt');
  x float(8) value;
end-pr;

longitud = strlen('hola');       // y se llama como cualquier procedimiento
```

**No hay generación de envoltorios, ni fichero de definiciones, ni biblioteca de FFI**: el prototipo *es*
la interfaz.

Y las palabras clave resuelven los cuatro problemas del cierre de forma explícita:

| Palabra clave | Qué resuelve |
|---|---|
| **`extproc('nombre')`** | el nombre externo, **sensible a mayúsculas** |
| **`value`** | paso por valor, frente al **paso por referencia por defecto de RPG** |
| **`options(*string)`** | **convierte la cadena de RPG en una cadena terminada en cero, automáticamente** |
| **`const`** | permite pasar expresiones y promete no modificar |
| **`pointer`** | el puntero de C, con `%addr` y `%str` para manejarlo |

**`options(*string)` merece destacarse** porque hace, en una palabra clave, lo que COBOL y Fortran en esta
página tienen que hacer a mano: **añadir el terminador nulo y gestionar el búfer temporal**.

Es la mejor ergonomía de FFI de esta página para el caso más común.

Y la interoperabilidad va mucho más allá de C (clase 155):

```rpgle
// Java, con la misma sintaxis de prototipo
dcl-pr crearBigDecimal object(*JAVA : 'java.math.BigDecimal')
       extproc(*JAVA : 'java.math.BigDecimal' : *CONSTRUCTOR);
  valor object(*JAVA : 'java.lang.String') const;
end-pr;
```

**`extproc(*JAVA : ...)` llama a Java desde RPG**, con la JVM dentro del mismo trabajo.

Y hay un detalle que merece la advertencia práctica, porque es el error más común: **en IBM i, los
nombres de las funciones de C distinguen mayúsculas y minúsculas y los de RPG no**.

```rpgle
dcl-pr doblar int(10) extproc('doblar');     // ✓ el nombre exacto del símbolo
dcl-pr doblar int(10) extproc('DOBLAR');      // ✗ no lo encuentra
```

Es el primero de los cuatro problemas del cierre —**los nombres**— apareciendo donde menos se espera.
"""),
        "pli": ("""
 llamar: procedure options(main);

    declare n fixed binary(31);

    doblar: procedure (x) returns (fixed binary(31)) options(byvalue);
       declare x fixed binary(31) byvalue;
       return (2 * x);
    end doblar;

    get list (n);

    put skip list ('resultado=' || trim(char(doblar(n))));

 end llamar;
""", """
**Lo que esta clase enseña en PL/I.** PL/I tiene la interoperabilidad más veterana de esta página, porque
**siempre convivió con el ensamblador**, y su vocabulario merece conocerse:

```pli
 declare c_sqrt entry (float binary(53) byvalue)
                returns (float binary(53) byvalue)
                options(linkage(optlink)) external('sqrt');
```

Y las tres opciones que resuelven los problemas del cierre:

**`OPTIONS(BYVALUE)`** resuelve la convención de paso. Y aquí está la trampa de esta página, por tercera
vez: **PL/I pasa por referencia por defecto**, igual que COBOL, Fortran y RPG.

```text
Los cuatro lenguajes de gestión y cálculo de esta página pasan por REFERENCIA.
C pasa por VALOR.
Y esa diferencia es el fallo de interoperabilidad número uno.
```

**Merece pararse en ello**, porque el motivo es histórico y explica mucho: **cuando estos lenguajes se
diseñaron, copiar un valor era caro y las estructuras eran grandes**, así que pasar la dirección era lo
sensato. C, que nació para escribir un sistema operativo con estructuras pequeñas, eligió lo contrario.

**`OPTIONS(LINKAGE(...))`** resuelve la convención de llamada (clase 157): `OPTLINK`, `SYSTEM`,
`STDCALL`, `CDECL` — porque en z/OS y en los sistemas de IBM han convivido varias.

**Y `EXTERNAL('nombre')`** resuelve los nombres, con el mismo problema de mayúsculas que RPG en esta
página: **PL/I pone los nombres en mayúsculas por defecto** y C los distingue.

Y PL/I tiene un tipo pensado exactamente para esta clase:

```pli
 declare cadena char(100) varyingz;      /* VARYINGZ: terminada en cero, como C */
```

**`VARYINGZ` es una cadena de longitud variable con terminador nulo** — el tipo que hace falta para
hablar con C, disponible como tipo del lenguaje en vez de como convención.

Y merece cerrar con el caso de interoperabilidad más masivo de este mundo, que no es con C: **la llamada
entre PL/I y COBOL**.

```pli
 declare pgm_cobol entry external;
 call pgm_cobol(registro);
```

**En un sistema z/OS típico conviven programas COBOL, PL/I, ensamblador y a veces C, llamándose entre
sí**, y funcionan porque **IBM definió una convención de llamada común para el sistema** —Language
Environment— con una pila, un manejo de condiciones y una gestión de almacenamiento compartidos.

Es exactamente lo mismo que ILE en IBM i (clase 155): **la plataforma define el ABI, y todos los
compiladores lo respetan** — que es una solución mejor que la de que todos imiten a C.
"""),
        "mumps": ("""
LLAMAR ; Llamada a funcion externa -- clase 156
 read n
 write "resultado=", $$doblar(n), !
 quit
 ;
doblar(x) ; devuelve el doble
 quit x * 2
""", """
**Lo que esta clase enseña en M.** M tiene una FFI que en el estándar apenas existe y que **cada
implementación resolvió a su manera**, y merece verlas porque las diferencias son instructivas.

**GT.M y YottaDB: *Call-Out* y *Call-In*.**

```text
# fichero de tabla de llamadas: declara la interfaz
doblar: xc_long_t doblar^(I:xc_long_t)
```

```mumps
 set $zroutines = ...
 set resultado = $&milib.doblar(5)      ; $& es la llamada externa
```

**`$&biblioteca.funcion(...)` llama a una función de C**, con la firma declarada en una **tabla de
llamadas externa** — un fichero de texto aparte.

Y esa decisión merece comentarse: **la firma no está en el programa, está en un fichero de
configuración**. Es lo contrario de RPG y Pascal en esta página, y tiene una ventaja concreta: **se puede
cambiar sin tocar el código M**; y una desventaja evidente: **el programa no documenta lo que llama**.

**Y en la otra dirección, *Call-In*:**

```c
ci_name_descriptor fn;
ydb_ci("procesar", &resultado, entrada);    /* C llamando a una rutina M */
```

**Un programa en C puede invocar una etiqueta de una rutina M**, con la base de datos y las transacciones
funcionando.

**InterSystems IRIS** va más lejos y es el caso más integrado de esta página:

```objectscript
Set obj = ##class(%Net.HttpRequest).%New()      // clases nativas
Do ##class(%SYS.Python).Import("numpy")          // ¡Python DENTRO de la VM!
```

**IRIS incorpora Java, .NET y Python en el mismo proceso**, con conversión automática de tipos.

Y **YottaDB** eligió el camino opuesto y más abierto: **exponer las globals a otros lenguajes**.

```go
// Go leyendo la misma base de datos que las rutinas M
var v yottadb.BufferT
yottadb.ValST(yottadb.NOTTP, nil, &v, "^PACIENTE", []string{"123"})
```

**Hay envoltorios oficiales para Go, Rust, Python, Node, Perl y C**, todos sobre la misma API.

Y esa es la evolución que merece destacar como conclusión: **M dejó de intentar ser el lenguaje y pasó a
ser el motor**.

La lógica clínica sigue en M porque son millones de líneas validadas; **lo nuevo se escribe en otros
lenguajes contra la misma base de datos, con las mismas transacciones** — que es exactamente el patrón
del estrangulador de la clase 150 aplicado a un ecosistema entero.
"""),
        "smalltalk": ("""
| n |

n := stdin nextLine trimBoth asNumber.

Transcript show: 'resultado=', (n * 2) printString; cr.
""", """
**Lo que esta clase enseña en Smalltalk.** Smalltalk tuvo durante décadas la FFI más incómoda de esta
página, y hoy tiene una de las más limpias. Merece ver el cambio.

**Antes: los *plugins* de la máquina virtual.**

```text
Para llamar a una función de C había que:
  1. escribir un módulo en C para la VM
  2. compilar la VM entera, o el plugin
  3. registrarlo con un nombre
  4. y llamarlo con <primitive: 'nombre' module: 'MiPlugin'>
```

**Eso significaba que añadir una llamada a C exigía recompilar la máquina virtual**, lo que en un sistema
que presume de modificarse en marcha (Parte 8) era una contradicción incómoda.

**Hoy: UFFI.**

```smalltalk
LibM >> sqrtOf: aDouble
    ^ self ffiCall: #( double sqrt (double aDouble) )

LibC >> getpid
    ^ self ffiCall: #( int getpid () )
```

**La firma de C se escribe como un literal dentro del método**, y UFFI construye la llamada en ejecución.

Y merece destacar tres propiedades que lo hacen notable:

**Primera, la declaración vive en el método que la usa.** No hay fichero de interfaz separado, así que
**la documentación de qué se llama está donde se llama** — lo contrario de la tabla externa de M en esta
página.

**Segunda, se puede probar y corregir en el REPL**, sin compilar nada (clase 124). Ajustar una firma
equivocada es reescribir el método y aceptarlo.

**Y tercera, encaja con el sistema de objetos**: una biblioteca externa se representa como **una subclase
de `FFILibrary`**, y sus funciones como métodos — así que **se navega, se documenta y se refactoriza como
cualquier otro código** (clase 150).

Y la gestión de memoria, que es el tercer problema del cierre:

```smalltalk
| buffer |
buffer := ExternalAddress allocate: 256.
[ self llamarConBuffer: buffer ]
    ensure: [ buffer free ].            "ensure: garantiza la liberación (clase 132)"
```

**`ExternalAddress` es memoria fuera del montón de Smalltalk**, así que **el recolector no la toca y hay
que liberarla a mano** — con `ensure:` para que ocurra incluso si hay una excepción.

Y merece cerrar con la observación que esta clase deja clara mirando la página entera: **todas las FFI se
parecen en lo que tienen que resolver y difieren en cuánto obligan a escribir**.

El eje va desde RPG y Pascal —**una declaración**— hasta XS de Perl y los plugins de la VM —**un
proyecto**—, y el precio de la comodidad es siempre el mismo: **menos comprobación en compilación**.
"""),
    },
)

# ---------------------------------------------------------------------------
# 157 — ABI, enlace y convenciones de llamada
# ---------------------------------------------------------------------------
SPECS["157"] = dict(
    gancho="""
Comparar dos anchos de palabra y decir si son compatibles. Es la comprobación más tosca posible de un
ABI, y detrás está la razón por la que la clase 156 funciona o no: **cuando dos lenguajes se llaman, hay
un acuerdo no escrito sobre dónde van los argumentos, quién limpia la pila y cómo se llama de verdad la
función**. Y esta página tiene el ejemplo que mejor lo enseña: **Fortran pasa un argumento oculto que no
aparece en ninguna firma** —la longitud de cada cadena— y **durante cuarenta años nadie se puso de
acuerdo en dónde ponerlo**.
""",
    porque="""
Aquí el concepto es la **interfaz binaria de aplicación**, y estos lenguajes la enseñan porque **cada uno
tiene una convención distinta y todos tuvieron que encajar**. Fortran y COBOL pasan por referencia; C
pasa por valor. C++ decora los nombres y cada compilador de forma distinta. Ada declara la convención por
tipo. Y **IBM resolvió el problema dos veces a nivel de plataforma** —Language Environment en z/OS e ILE
en IBM i— definiendo un ABI común para todos los lenguajes en lugar de que todos imitaran a C.

Y aparecen las cuatro capas del acuerdo: **los nombres, el paso de argumentos, la disposición de los
datos y quién limpia**.
""",
    cierre="""
Lo transferible: **un ABI es un contrato binario, y romperlo no da un error de compilación: da un
programa que funciona hasta que no**. De ahí las tres reglas que evitan casi todos los problemas:
**usar los tipos de tamaño garantizado en las fronteras** —`int32_t`, `c_int`, `COMP-5`, `Interfaces.C`,
nunca los tipos cuyo tamaño depende de la plataforma—; **pasar estructuras por puntero, no por valor**,
porque el relleno y la alineación varían; y **versionar la interfaz explícitamente**, porque cuando algo
cambie hará falta detectarlo — que es exactamente lo que la firma de programa de servicio de IBM i hace
por sistema (clase 143).
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. ABI.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(40).
01  C-A     PIC X(10).
01  C-B     PIC X(10).
01  A       PIC 9(4) COMP.
01  B       PIC 9(4) COMP.

PROCEDURE DIVISION.
    ACCEPT LINEA
    UNSTRING LINEA DELIMITED BY ALL SPACES
        INTO C-A C-B
    END-UNSTRING

    COMPUTE A = FUNCTION NUMVAL(C-A)
    COMPUTE B = FUNCTION NUMVAL(C-B)

    IF A = B
        DISPLAY "abi=compatible"
    ELSE
        DISPLAY "abi=incompatible"
    END-IF
    STOP RUN.
""", """
**Lo que esta clase enseña en COBOL.** COBOL tiene una convención de llamada muy simple y muy distinta de
la de C, y merece enunciarla porque es la fuente de fallos de la clase 156:

**COBOL pasa todo por referencia, y la lista de argumentos es una lista de direcciones.**

```cobol
           CALL "SUBPGM" USING A B C
```

**Lo que se pasa son tres punteros**, y el programa llamado los recibe en su `LINKAGE SECTION`:

```cobol
       LINKAGE SECTION.
       01  P1 PIC S9(9) COMP.
       PROCEDURE DIVISION USING P1.
```

Y hay tres detalles que definen el ABI de COBOL y que conviene conocer:

**Primero, no hay comprobación.** El programa llamado **cree** que el primer parámetro es un entero
binario de cuatro bytes. Si el llamador pasó un `PIC X(20)`, **nadie avisa**: se interpreta la memoria
como si fuera un número.

Es la misma situación que los procedimientos externos de Fortran sin interfaz (clase 109), y por el
mismo motivo: **el enlace es por nombre y por posición, sin tipos**.

**Segundo, la disposición de las estructuras**, que es la tercera capa del acuerdo:

```cobol
       01  REGISTRO.
           05  CODIGO PIC X(4).
           05  IMPORTE PIC S9(7)V99 COMP-3.
           05  FECHA   PIC 9(8).
```

**COBOL empaqueta los campos sin relleno**, y **`COMP-3` es decimal empaquetado** (clase 072): dos
dígitos por byte, con el signo en el último medio byte.

**Un `struct` de C con esos campos tendría relleno y otros tipos**, así que **la traducción de registros
entre COBOL y C hay que hacerla campo a campo**, y es un trabajo delicado.

**Y tercero, `SYNCHRONIZED`**, que es la palabra clave de la alineación:

```cobol
           05  N PIC S9(9) COMP SYNCHRONIZED.     *> alineado a 4 bytes
```

**Sin `SYNCHRONIZED`, COBOL no alinea**, y en arquitecturas que lo exigen —o donde cuesta rendimiento—
eso importa.

Es exactamente la segunda regla del cierre de esta clase: **la disposición de una estructura no es
obvia**, y por eso conviene pasarla por puntero y traducirla explícitamente en lugar de suponer que
coincide.
"""),
        "fortran": ("""
program abi
   implicit none
   integer :: a, b

   read(*, *) a, b

   if (a == b) then
      write(*, '(A)') 'abi=compatible'
   else
      write(*, '(A)') 'abi=incompatible'
   end if
end program abi
""", """
**Lo que esta clase enseña en Fortran.** Aquí está el ejemplo del gancho, y es de los casos más
instructivos de toda la interoperabilidad: **el argumento oculto de longitud de cadena**.

```fortran
subroutine procesar(texto, n)
   character(len=*) :: texto
   integer :: n
end subroutine
```

**Esa subrutina, vista desde C, no tiene dos argumentos: tiene TRES.**

```c
void procesar_(char *texto, int *n, size_t texto_len);
                                    /* ↑ el compilador AÑADE la longitud */
```

**La longitud de la cadena viaja como un argumento extra que no aparece en el fuente**, porque en Fortran
`len=*` significa "la longitud la sabe el llamador".

Y el problema histórico es que **nadie se puso de acuerdo en dónde ponerlo**:

| Compilador | Dónde va la longitud oculta | Tipo |
|---|---|---|
| **gfortran, ifort (Unix)** | **al final**, tras todos los argumentos | `size_t` o `int` |
| **Compiladores de Cray clásicos** | **inmediatamente después de la cadena** | descriptor |
| **IBM XL, algunos de Windows** | varía según opciones | varía |

**Y ese desacuerdo hizo imposible durante décadas escribir código portable que pasara cadenas entre C y
Fortran.**

Fortran 2018 lo estandarizó por fin, con `ISO_Fortran_binding.h`, pero **la solución práctica sigue
siendo la misma: no pasar cadenas de Fortran a C** — usar arreglos de `character(kind=c_char)` terminados
en cero (clase 156).

Y el segundo elemento del ABI de Fortran es el que ya apareció en la clase 137: **el decorado de
nombres**.

```text
gfortran:  subroutine calcular  →  calcular_
ifort:     subroutine calcular   →  calcular_
Módulo:    module m, sub calcular →  __m_MOD_calcular   (gfortran)
                                    m_mp_calcular_       (ifort)
```

**El símbolo de un procedimiento dentro de un módulo es completamente distinto entre compiladores**, y
por eso **`bind(C, name=...)` es obligatorio** para cualquier cosa que se vaya a llamar desde fuera.

**Y el tercero: Fortran pasa todo por referencia.** Un `integer` sin `value` se pasa como puntero, igual
que COBOL, PL/I y RPG en esta página.

Y el cuarto, que merece la advertencia porque afecta al rendimiento y a la corrección: **los arreglos con
forma asumida se pasan como descriptor**, no como puntero (clase 129). Un `real(:,:)` pasado a C **no es
una dirección: es una estructura con la dirección, los límites y los saltos** — y su formato lo define
el compilador.
"""),
        "ada": ("""
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Abi is
   A, B : Integer;
begin
   Get (A);
   Get (B);

   if A = B then
      Put_Line ("abi=compatible");
   else
      Put_Line ("abi=incompatible");
   end if;
end Abi;
""", """
**Lo que esta clase enseña en Ada.** Ada es el único lenguaje de esta página donde **la convención de
llamada es un atributo declarado del tipo y del subprograma**, y eso resuelve la mayoría de los
problemas de esta clase de forma explícita.

```ada
type Callback is access procedure (X : Interfaces.C.int)
  with Convention => C;            --  ¡la convención es parte del TIPO!

procedure Registrar (F : Callback)
  with Import => True, Convention => C, External_Name => "registrar";
```

**Que la convención forme parte del tipo del puntero a función significa que el compilador comprueba que
no se pase un subprograma con convención de Ada donde se espera uno de C** — un error que en C++ y en
Pascal se descubre al fallar.

Y Ada da control explícito sobre la tercera capa del acuerdo —**la disposición de los datos**— con una
precisión que ningún otro de esta página iguala:

```ada
type Registro is record
   Codigo  : Interfaces.C.int;
   Activo  : Boolean;
   Valor   : Interfaces.C.double;
end record
  with Convention => C_Pass_By_Copy;

--  Y si hace falta el control total, la cláusula de representación:
type Estado is record
   Listo   : Boolean;
   Error   : Boolean;
   Codigo  : Integer range 0 .. 63;
end record;

for Estado use record
   Listo  at 0 range 0 .. 0;        --  byte 0, bit 0
   Error  at 0 range 1 .. 1;         --  byte 0, bit 1
   Codigo at 0 range 2 .. 7;          --  byte 0, bits 2 a 7
end record;

for Estado'Size use 8;
for Estado'Bit_Order use System.Low_Order_First;
```

**Las cláusulas de representación permiten decir exactamente en qué bit va cada campo**, y el compilador
**se niega a compilar si lo declarado no cabe o es inconsistente**.

Es la respuesta más completa de esta página al problema de la disposición, y su origen es el dominio:
**en un sistema embarcado hay que leer un registro de hardware o una trama de un protocolo donde cada bit
tiene un significado fijado por una norma**.

Y merece señalar la diferencia con la alternativa habitual: en C eso se hace con **campos de bits**, cuyo
orden **depende de la implementación**, o con **máscaras y desplazamientos a mano**. En Ada, **se declara
y se comprueba**.

Y para el caso general, `Ada.Unchecked_Conversion` da la reinterpretación explícita:

```ada
function A_Bytes is new Ada.Unchecked_Conversion (Estado, Interfaces.Unsigned_8);
```

**El nombre lleva la advertencia**: `Unchecked` deja claro en el punto de uso que ahí se está saltando el
sistema de tipos, que es exactamente lo que un `reinterpret_cast` debería comunicar y no comunica.
"""),
        "pascal": ("""
program Abi;
{$MODE OBJFPC}{$H+}

var
  A, B: Integer;

begin
  Read(A, B);

  if A = B then
    WriteLn('abi=compatible')
  else
    WriteLn('abi=incompatible');
end.
""", """
**Lo que esta clase enseña en Pascal.** El mundo Pascal, por vivir en Windows, es donde mejor se ve la
segunda capa del acuerdo de esta clase: **las convenciones de llamada, en plural**.

```pascal
function F(A, B: Integer): Integer; cdecl;      { C: el LLAMADOR limpia la pila }
function G(A, B: Integer): Integer; stdcall;     { Win32 API: el LLAMADO limpia }
function H(A, B: Integer): Integer; register;     { Delphi: los 3 primeros en EAX, EDX, ECX }
function I(A, B: Integer): Integer; safecall;      { COM: convierte excepciones en HRESULT }
function J(A: Integer): Integer; pascal;            { obsoleta: argumentos al REVÉS }
```

Y merece explicar la diferencia que más caídas ha producido: **quién limpia la pila**.

```text
cdecl:   el llamador quita los argumentos de la pila después de la llamada.
         → permite número VARIABLE de argumentos (printf)
stdcall: la función llamada los quita al volver, con "ret N".
         → más compacto; imposible con argumentos variables
```

**Si el llamador cree que es `cdecl` y la función es `stdcall`, la pila se limpia dos veces** —o
ninguna—, y el programa se corrompe **unas cuantas llamadas después**, en un sitio que no tiene nada que
ver.

Es el ejemplo perfecto del cierre de esta clase: **no hay error de compilación; hay un fallo diferido e
incomprensible**.

Y hay dos detalles que merecen la mención porque son propios de este ecosistema:

**`safecall` es una convención con semántica añadida**: la función devuelve un `HRESULT`, y el compilador
**genera automáticamente el código que convierte una excepción de Pascal en un código de error y viceversa
en el llamador**.

Es la única de esta página que resuelve el cuarto problema de la clase 156 —**los errores no cruzan la
frontera**— **en la propia convención de llamada**, y viene de COM, la tecnología de componentes de
Microsoft.

**Y `register` es la convención por defecto de Delphi**, no `cdecl`, así que **una función Delphi
declarada sin modificador no la puede llamar C** — un error muy frecuente al exportar una biblioteca.

Y en 64 bits, buena parte de este lío desapareció y merece decirlo: **x86-64 tiene una sola convención
por sistema operativo** —System V AMD64 en Linux y macOS, Microsoft x64 en Windows—, así que `cdecl`,
`stdcall` y `register` **se ignoran y son sinónimos**.

Es un caso poco común de un problema que se resolvió porque la arquitectura nueva impuso un estándar.
"""),
        "lisp": ("""
(let ((a (read))
      (b (read)))
  (format t "abi=~A~%" (if (= a b) "compatible" "incompatible")))
""", """
**Lo que esta clase enseña en Common Lisp.** Lisp tiene una posición interesante en esta clase: **su
propia representación de datos no se parece en nada a la de C**, así que **toda la frontera es
traducción**.

```lisp
;; Un entero de Lisp NO es un int de C
(cffi:foreign-type-size :int)        ; 4
;; un fixnum de SBCL lleva bits de etiqueta (clase 128)
```

Y por eso CFFI define **una tabla de tipos explícita**, y usarla mal es el fallo del cierre de esta
clase:

```lisp
(cffi:defcfun ("procesar" c-procesar) :int
  (n :long)                  ; ← si el C real usa "int", esto CORROMPE la pila en algunas ABI
  (buf :pointer)
  (tam :size))
```

**`:long` es 8 bytes en Linux de 64 bits y 4 en Windows de 64 bits.** Es la primera regla del cierre de
esta clase en su forma más pura: **usar tipos de tamaño garantizado**.

```lisp
(cffi:defcfun ("procesar" c-procesar) :int32
  (n :int32)                 ; ✓ sin ambigüedad
  (buf :pointer)
  (tam :size))
```

Y CFFI da acceso a la tercera capa —**la disposición**— con estructuras declaradas:

```lisp
(cffi:defcstruct punto
  (x :double)
  (y :double)
  (etiqueta :char :count 32))

(cffi:foreign-slot-value p '(:struct punto) 'x)
(cffi:foreign-type-size '(:struct punto))     ; ¡comprobar que coincide con sizeof en C!
```

**Y esa última línea es una práctica recomendable**: comprobar en las pruebas que el tamaño calculado por
CFFI coincide con el `sizeof` real, porque **el relleno y la alineación los infiere CFFI de las reglas
habituales**, y una estructura con `#pragma pack` o con un tipo inesperado no coincidirá.

Y hay un problema de esta clase que es específico de los lenguajes con recolector de basura y que merece
destacarse, porque no aparece en las columnas compiladas: **el recolector mueve los objetos**.

```lisp
;; ✗ pasar un puntero a un vector de Lisp y guardarlo en C
;;   el recolector puede MOVER ese vector, y el puntero de C queda apuntando a basura

;; ✓ copiar a memoria externa, o fijar el objeto mientras dure la llamada
(cffi:with-pointer-to-vector-data (ptr vector)
  (c-procesar ptr (length vector)))
```

**Un puntero a memoria gestionada solo es válido mientras el recolector no actúe**, y esa es una regla que
Java (JNI), C# (`fixed`), Go (`cgo`) y Python tienen igual, con nombres distintos.

Es la quinta capa del acuerdo, la que no aparece en la lista del "por qué" porque C no la tiene: **la
vida de los objetos a través de la frontera**.
"""),
        "tcl": ("""
gets stdin linea
lassign [string trim $linea] a b

puts "abi=[expr {$a == $b ? {compatible} : {incompatible}}]"
""", """
**Lo que esta clase enseña en Tcl.** Tcl resuelve esta clase de una forma que merece destacarse porque es
una decisión de diseño deliberada: **la extensión no se enlaza con símbolos del intérprete — se le pasa
una tabla**.

```c
int Milib_Init(Tcl_Interp *interp) {
    if (Tcl_InitStubs(interp, "8.6", 0) == NULL) return TCL_ERROR;
    Tcl_CreateObjCommand(interp, "doblar", DoblarCmd, NULL, NULL);
    Tcl_PkgProvide(interp, "milib", "1.0");
    return TCL_OK;
}
```

**`Tcl_InitStubs` es la pieza clave**, y merece explicarse porque resuelve un problema real de esta
clase: **el mecanismo de *stubs***.

```text
Sin stubs:  la extensión se enlaza con libtcl8.6.so
            → funciona SOLO con esa versión exacta
            → y en Windows, solo con esa DLL concreta

Con stubs:  la extensión NO enlaza con nada del intérprete
            → recibe una TABLA DE PUNTEROS A FUNCIÓN al inicializarse
            → funciona con cualquier Tcl 8.6 o posterior, y con cualquier build
```

**Una extensión compilada con stubs funciona en cualquier intérprete de Tcl compatible**, incluido uno
empotrado dentro de otra aplicación (clase 155) que ni siquiera exporte sus símbolos.

Y esa es exactamente la tercera regla del cierre de esta clase —**versionar la interfaz
explícitamente**— resuelta con un mecanismo: **la tabla tiene un orden fijo y solo crece, así que una
extensión vieja sigue funcionando con un intérprete nuevo**.

Es el mismo principio que la firma de programa de servicio de IBM i (clase 143) y que las tablas de
métodos virtuales: **añadir al final, nunca reordenar**.

Y merece señalar por qué esto importa tanto en Tcl y menos en otros: **Tcl se empotra**. Una extensión
puede acabar cargada en un intérprete que vive dentro de una herramienta de diseño de circuitos, dentro
de un servidor o dentro de un router — y **en ninguno de esos casos hay una `libtcl.so` con la que
enlazar**.

Y para la otra dirección, Tcl tiene el tipo que resuelve la primera capa:

```c
Tcl_Obj *obj;                       /* con conteo de referencias */
Tcl_IncrRefCount(obj);
Tcl_DecrRefCount(obj);
```

**La memoria de la frontera la gestiona Tcl con conteo de referencias**, así que la pregunta "¿quién
libera?" tiene una respuesta única y documentada — que es más de lo que ofrecen la mayoría de las FFI de
la clase 156.
"""),
        "perl": ("""
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;
my ($a1, $b1) = split ' ', $linea;

print "abi=", ($a1 == $b1 ? 'compatible' : 'incompatible'), "\\n";
""", """
**Lo que esta clase enseña en Perl.** Perl aporta a esta clase el ejemplo más claro de una consecuencia
del ABI que casi nadie anticipa: **un módulo binario está atado a la construcción exacta del
intérprete**.

```bash
$ perl -V:archname
archname='x86_64-linux-gnu-thread-multi'
```

**Esa cadena es la identidad del ABI de ese Perl**, y los módulos compilados se instalan en un
directorio con ese nombre:

```text
/usr/lib/perl5/5.36/x86_64-linux-gnu-thread-multi/auto/Mi/Modulo/Modulo.so
```

Y las cosas que forman parte de esa identidad son más de las que parece:

| Elemento | Por qué cambia el ABI |
|---|---|
| **Versión de Perl** | las estructuras internas cambian entre versiones |
| **`useithreads`** | **con hilos, cada función lleva un argumento oculto `pTHX`** |
| **`use64bitint`** | el tamaño de los enteros internos |
| **`uselongdouble`** | el tamaño de los reales |
| **Arquitectura y sistema** | lo evidente |

**La segunda fila merece el detalle**, porque es el mismo fenómeno que el argumento oculto de Fortran en
esta página: **un Perl compilado con hilos pasa un puntero al intérprete como primer argumento oculto de
cada función interna**.

```c
/* sin hilos */   void Perl_sv_setiv(SV *sv, IV num);
/* con hilos */    void Perl_sv_setiv(pTHX_ SV *sv, IV num);
```

**Un módulo compilado para uno no funciona con el otro**, y el fallo es una caída, no un mensaje claro.

De ahí que XS use macros —`dTHX`, `aTHX_`— **que se expanden a nada o al argumento según la
configuración**, y que todo el código de extensiones esté escrito con ellas.

Es la solución de esta clase al problema de tener dos ABI: **hacer que el fuente sea el mismo y que la
diferencia la ponga el preprocesador**.

Y la consecuencia práctica es la que todo el ecosistema conoce: **al actualizar Perl hay que recompilar
todos los módulos binarios**, y por eso `cpanm`, los gestores de paquetes del sistema y `perlbrew`
mantienen árboles separados por versión.

Es la misma lección que los `.mod` de Fortran y los `.bpl` de Delphi en la clase 143: **distribuir
binarios ata al entorno**, y el ABI es la forma concreta de esa atadura.
"""),
        "cpp": ("""
#include <cstdint>
#include <iostream>

int main() {
    std::int64_t a{}, b{};
    if (!(std::cin >> a >> b)) return 1;

    std::cout << "abi=" << (a == b ? "compatible" : "incompatible") << '\\n';
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** El programa usa **`std::int64_t`**, que es la primera regla del
cierre de esta clase: **en una frontera, el tipo debe tener tamaño garantizado**.

```cpp
int          // 4 bytes casi siempre... pero no está garantizado
long         // 8 en Linux de 64 bits, 4 en Windows de 64 bits  ← ¡la trampa!
size_t        // depende de la arquitectura
std::int32_t   // exactamente 32 bits, o no compila
```

**La diferencia de `long` entre Linux y Windows en 64 bits** —el modelo LP64 frente a LLP64— **es la
incompatibilidad de ABI más común del mundo**, y afecta a cualquier código portable.

Y C++ tiene, además del ABI de C, **un ABI propio que no está estandarizado**, y merece enumerar qué
incluye porque explica por qué la clase 156 recomienda exponer C:

| Elemento del ABI de C++ | Por qué no es portable |
|---|---|
| **Decorado de nombres** | GCC/Clang usan Itanium; MSVC usa el suyo |
| **Tablas de métodos virtuales** | posición y contenido definidos por el compilador |
| **Disposición con herencia múltiple** | ajustes de puntero (*thunks*) distintos |
| **Excepciones** | tablas de desenrollado con formatos distintos |
| **La biblioteca estándar** | `std::string` cambió en GCC 5 (clase 143) |
| **Información de tipo en ejecución** | la comparación de `type_info` varía |

Y las convenciones de llamada de x86-64, que merecen conocerse porque explican mucho:

```text
System V AMD64 (Linux, macOS, BSD):
  enteros:  RDI, RSI, RDX, RCX, R8, R9, y luego pila
  reales:   XMM0-XMM7
  retorno:  RAX (y RDX para 128 bits), XMM0 para reales

Microsoft x64 (Windows):
  enteros:  RCX, RDX, R8, R9, y luego pila
  reales:   XMM0-XMM3
  ¡y 32 bytes de "espacio sombra" reservados por el LLAMADOR!
```

**El "espacio sombra" merece la mención**: Windows exige que el llamador reserve 32 bytes en la pila
**aunque la función no los use**, para que la función llamada pueda volcar ahí sus argumentos de registro
si le conviene.

**Un código que llama con la convención de Linux en Windows corrompe la pila**, y ese es el tipo de fallo
que esta clase enseña a reconocer.

Y merece cerrar con la herramienta que hace comprobable todo esto:

```bash
abi-compliance-checker -l milib -old v1.dump -new v2.dump
nm -C libmilib.so | grep ' T '        # los símbolos exportados, sin decorar
c++filt _Z6doblari                     # traducir un nombre decorado
```

**`abi-compliance-checker` compara dos versiones de una biblioteca y dice si el cambio rompe el ABI** —
que es la tercera regla del cierre puesta en práctica, y una comprobación que merece estar en la
integración continua de cualquier biblioteca con usuarios (clase 147).
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi ABICMP;
  a int(10) const;
  b int(10) const;
end-pi;

if a = b;
  dsply 'abi=compatible';
else;
  dsply 'abi=incompatible';
endif;

*inlr = *on;
return;
""", """
**Lo que esta clase enseña en RPG.** IBM i resolvió el problema de esta clase de una forma que merece
destacarse porque es distinta de la de todos los demás: **definió un ABI de plataforma y obligó a todos
los compiladores a respetarlo**.

**ILE, el *Integrated Language Environment*** (clase 155), especifica:

```text
- la convención de llamada de procedimientos, común a RPG, COBOL, C, C++ y CL
- el modelo de almacenamiento: grupos de activación, montón y pila compartidos
- el manejo de CONDICIONES común: un error de C lo puede capturar RPG
- la resolución de símbolos: por firma de programa de servicio (clase 143)
- y la depuración: una sola vista para todos los lenguajes (clase 141)
```

**Que el manejo de excepciones sea común es lo más notable**, y merece subrayarlo: en el mundo C++ /
Python / Rust, **las excepciones no cruzan la frontera** (clase 156). **En ILE, sí**: una condición
señalada en un módulo C **la puede manejar un `monitor` de RPG** en el mismo trabajo.

Es la respuesta a uno de los cuatro problemas de la clase 156 que casi nadie resuelve, y solo es posible
porque **el ABI lo definió la plataforma en vez de heredarlo de C**.

Y la segunda pieza es la que la clase 143 detalló y que aquí conviene ver como lo que es —**una solución
al problema del cierre de esta clase**:

```text
CPF3EE1 - La firma del programa de servicio no coincide
```

**La firma se calcula sobre la lista ordenada de exportaciones y se comprueba al activar el programa.**

Compárese con lo que hace un sistema Unix ante el mismo escenario: **el enlazador dinámico resuelve por
nombre**, y si la función cambió de firma sin cambiar de nombre, **enlaza y falla en ejecución de forma
impredecible**.

**Es literalmente la tercera regla del cierre de esta clase —versionar la interfaz explícitamente—
implementada por el sistema operativo.**

Y hay una particularidad de esta plataforma que merece nombrarse porque es de las pocas de esta página:
**los punteros son de 16 bytes**.

```rpgle
dcl-s p pointer;      // 16 bytes: espacio de direcciones de 128 bits, con etiqueta
```

**IBM i usa un espacio de direcciones único y persistente de 128 bits**, con punteros etiquetados por
hardware (clase 153). Así que **un puntero de IBM i no cabe en un `void*` de 8 bytes**, y la
interoperabilidad con C en PASE —que sí usa punteros normales de AIX— **requiere conversión explícita**.

Es un recordatorio útil de que **"puntero" no significa lo mismo en todas partes**, y de que suponer que
un puntero cabe en un entero es una de las suposiciones más caras de la programación de sistemas.
"""),
        "pli": ("""
 abicmp: procedure options(main);

    declare (a, b) fixed binary(31);

    get list (a, b);

    if a = b then
       put skip list ('abi=compatible');
    else
       put skip list ('abi=incompatible');

 end abicmp;
""", """
**Lo que esta clase enseña en PL/I.** PL/I vive en la plataforma donde el problema de esta clase se
resolvió por primera vez a nivel de sistema: **Language Environment, de IBM, en z/OS**.

Y merece describir qué hizo, porque es el mismo enfoque que ILE en RPG de esta página, diez años antes:

```text
Language Environment (1991) define, para COBOL, PL/I, C, C++ y Fortran:
  - una convención de llamada común
  - una PILA común y un gestor de almacenamiento común
  - un manejo de CONDICIONES común, con propagación entre lenguajes
  - las rutinas de la biblioteca de ejecución compartidas
  - y un conjunto de mensajes y de códigos de error unificado
```

**Antes de LE, cada compilador de IBM traía su propia biblioteca de ejecución**, con su propia gestión de
almacenamiento y su propio manejo de errores. **Mezclar COBOL y PL/I en un mismo programa era posible y
delicado**: cada uno inicializaba su entorno y se pisaban.

Y el manejo de condiciones común merece el mismo comentario que en RPG: **una condición señalada en un
módulo PL/I la puede manejar un `USE` de COBOL**, y una división por cero en C activa el manejo de
condiciones de LE que los tres entienden.

Es una capacidad que la mayoría de los ecosistemas poliglotas modernos **no tiene**.

Y PL/I aporta a esta clase el vocabulario de las convenciones de enlace, que en z/OS son varias por
razones históricas:

```pli
 options(linkage(system))    /* la convención estándar de z/OS: R1 apunta a una lista */
 options(linkage(optlink))    /* la de los compiladores C de IBM */
 options(linkage(cdecl))       /* la de C en otras plataformas */
 options(assembler)             /* llamar a una rutina de ensamblador clásica */
```

**`LINKAGE(SYSTEM)` es la convención clásica del mainframe**, y merece describirse porque es distinta de
todo lo de esta página:

```text
R1 apunta a una LISTA DE DIRECCIONES de los argumentos.
El último elemento tiene el bit de signo activado para marcar el final.
R13 apunta al área de guardado; R14 es la dirección de retorno; R15, el punto de entrada.
```

**El bit alto del último puntero como marca de fin de lista** es una convención de 1964 que sigue viva, y
es un buen ejemplo de lo que esta clase quiere transmitir: **un ABI es un montón de acuerdos concretos
sobre bits y registros**, y funcionan porque todo el mundo los respeta — no porque sean elegantes.
"""),
        "mumps": ("""
ABICMP ; Comparar anchos de ABI -- clase 157
 read linea
 new a, b
 set a = $piece(linea, " ", 1)
 set b = $piece(linea, " ", 2)
 write "abi=", $select(a = b : "compatible", 1 : "incompatible"), !
 quit
""", """
**Lo que esta clase enseña en M.** M es el caso donde esta clase casi no aplica, y merece explicar por
qué, porque la razón es interesante: **en M no hay tipos, así que no hay disposición de datos que
acordar**.

```mumps
 set x = 42          ; ¿entero? ¿cadena "42"? LAS DOS (clase 081)
 set x = "hola"       ; y ahora otra cosa
```

**Todo valor de M es, conceptualmente, una cadena de caracteres**, así que **la frontera con cualquier
otro lenguaje es una frontera de texto**.

Y eso tiene dos consecuencias opuestas que merecen verse juntas:

**A favor: la interoperabilidad es trivial de especificar.** No hay alineación, ni relleno, ni orden de
bytes, ni tamaños de entero. **Una cadena es una cadena en todas partes.**

**En contra: todo se convierte, y convertir cuesta.** Un número que cruza la frontera **se formatea a
texto y se vuelve a analizar**, y en un bucle de millones de llamadas eso es carísimo (clase 152).

Es exactamente el compromiso de la primera frontera del cierre de la clase 155 —**el proceso separado con
serialización**— aplicado dentro del mismo proceso.

Y las tablas de llamadas de GT.M y YottaDB (clase 156) son donde esta clase sí aparece, porque **ahí sí
hay que declarar tipos de C**:

```text
doblar: xc_long_t doblar^(I:xc_long_t)
sumar:  xc_double_t sumar^(I:xc_double_t, I:xc_double_t)
texto:  xc_status_t procesar^(I:xc_char_t*, O:xc_char_t*[512])
```

**`xc_long_t`, `xc_double_t`, `xc_char_t` son los tipos de la interfaz**, y `I:` y `O:` declaran la
dirección —entrada, salida o ambas—.

**Y la declaración `[512]` de la tercera línea merece destacarse**, porque resuelve el problema de la
memoria de la clase 156 de forma explícita: **dice cuánto espacio reserva el sistema de ejecución de M
para el resultado**, así que **no hay duda de quién reserva ni de cuánto**.

Es una decisión de diseño sensata: **cuando el tamaño no se puede negociar en ejecución, se declara por
adelantado**.

Y merece cerrar con la observación general que M ilustra bien: **cuanto más dinámico es un lenguaje,
menos ABI tiene y más traducción hace**.

Es el mismo eje que recorre toda esta parte del curso: **las garantías estáticas y la flexibilidad son
la misma palanca**, y en la frontera entre lenguajes esa palanca se llama coste de conversión.
"""),
        "smalltalk": ("""
| linea partes a b |

linea := stdin nextLine trimBoth.
partes := linea substrings: ' '.

a := (partes at: 1) asNumber.
b := (partes at: 2) asNumber.

Transcript
    show: 'abi=', (a = b ifTrue: [ 'compatible' ] ifFalse: [ 'incompatible' ]);
    cr.
""", """
**Lo que esta clase enseña en Smalltalk.** Smalltalk tiene el mismo punto de partida que M en esta página
—**su representación interna no se parece a la de C**— y una dificultad añadida que merece explicarse:
**el recolector mueve los objetos**.

```text
Un objeto de Smalltalk tiene:
  - una cabecera con su clase, su tamaño y bits del recolector
  - los campos, que son referencias a otros objetos (o enteros pequeños etiquetados)
  - y una DIRECCIÓN QUE PUEDE CAMBIAR en cualquier recolección
```

**Así que no se puede pasar la dirección de un objeto a C y esperar que siga siendo válida.**

Y UFFI lo resuelve con una distinción explícita entre dos memorias:

```smalltalk
"Memoria de Smalltalk: la mueve el recolector"
| coleccion | coleccion := ByteArray new: 256.

"Memoria EXTERNA: malloc, no la toca el recolector, hay que liberarla"
| externa | externa := ExternalAddress allocate: 256.
[ self llamarC: externa ] ensure: [ externa free ].
```

**Y para el caso frecuente —pasar datos de Smalltalk a C durante una llamada— se copia**:

```smalltalk
self ffiCall: #( void procesar (ByteArray datos, int tam) )
"UFFI copia el ByteArray a memoria externa, llama, y libera"
```

**La copia es el precio de la seguridad**, y es la misma decisión que toman Java con `GetByteArrayElements`
y Go con `cgo`: **copiar, o fijar el objeto durante la llamada**.

Es la quinta capa del acuerdo que la explicación de Lisp en esta página nombraba —**la vida de los
objetos**— y es la que separa a los lenguajes con recolector de los que no.

Y Smalltalk aporta a esta clase una capacidad de introspección poco común, que encaja con toda su
Parte 8:

```smalltalk
(ExternalType int) byteSize.              "el tamaño de un int en ESTA plataforma"
FFIBackend current calloutAPIClass.
Smalltalk vm wordSize.                     "4 u 8"
Smalltalk os isWindows.
```

**Se puede preguntar al sistema en marcha por los tamaños de los tipos externos**, y ajustar la
declaración en consecuencia — que es lo que hace posible que una misma imagen funcione en plataformas
distintas.

Y merece cerrar la clase con la observación que la página entera sostiene: **el ABI es la capa donde
todas las abstracciones se acaban**.

Por muy alto que sea el nivel de un lenguaje —objetos vivos, recolección, mensajes— **en la frontera hay
registros, bytes y alineaciones**, y la única forma de cruzarla bien es **conocer el contrato y
declararlo explícitamente**, en lugar de suponer que los dos lados entienden lo mismo.
"""),
    },
)
