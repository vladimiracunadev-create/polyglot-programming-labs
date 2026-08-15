# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 155

> [⬅️ Volver a la clase 155](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Contar componentes. El programa es una excusa para la pregunta de la parte entera: **¿por qué ningún
sistema serio está escrito en un solo lenguaje?** Y esta página tiene la respuesta más antigua que
existe: **un programa CICS de 1975 ya mezclaba cuatro lenguajes** —COBOL para la lógica, JCL para
orquestar, SQL embebido para los datos y macros de ensamblador para lo que ninguno de los tres podía
hacer—. **El sistema poliglota no es una moda: es el estado natural del software desde el principio.**

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es la **frontera entre lenguajes como decisión de diseño**, y estos lenguajes la
> enseñan porque **casi ninguno pretendió nunca ser el único**. COBOL nació para la lógica de negocio y
> delegó todo lo demás. Fortran calcula y deja la interfaz a otros. Tcl se diseñó explícitamente **para
> ser la mitad de un sistema de dos lenguajes**. Y RPG convive con Java, Node y SQL en la misma máquina y
> en el mismo trabajo.
>
> Y aparece la pregunta que ordena toda la Parte 10: **cuando dos lenguajes se tocan, ¿qué cruza la
> frontera y con qué garantías?**
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: una línea con nombres de componentes (palabras) → stdout: `componentes=<cantidad>`
- **Regla:** `contar los componentes`

| stdin | esperado |
|---|---|
| `cli api web` | `componentes=3` |
| `app` | `componentes=1` |
| `web api datos cache` | `componentes=4` |

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
```

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

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
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
```

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

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
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
```

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

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
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
```

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

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let ((linea (read-line))
      (cnt 0)
      (en-palabra nil))
  (loop for c across linea
        do (if (char= c #\Space)
               (setf en-palabra nil)
               (unless en-palabra
                 (setf en-palabra t)
                 (incf cnt))))
  (format t "componentes=~D~%" cnt))
```

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

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea

puts "componentes=[llength [split [string trim $linea]]]"
```

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

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;

my @componentes = split ' ', $linea;

print "componentes=", scalar(@componentes), "\n";
```

**Lo que esta clase enseña en Perl.** Perl fue durante veinte años **el pegamento por excelencia de los
sistemas Unix**, y merece explicar qué significaba eso en la práctica.

```perl
# Un guion de administración típico de 1998 tocaba, en veinte líneas:
my @procesos = `ps aux`;                          # el shell
open(my $fh, '-|', 'ldapsearch', '-x', $filtro);   # LDAP
$dbh->do('UPDATE usuarios SET ...');                # SQL
system('/usr/sbin/sendmail', '-t');                  # el sistema de correo
print $socket "GET /estado HTTP/1.0\r\n\r\n";       # HTTP a mano
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

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>
#include <string>

int main() {
    std::string componente;
    int cnt = 0;
    while (std::cin >> componente) ++cnt;

    std::cout << "componentes=" << cnt << '\n';
    return 0;
}
```

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
```

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

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
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
```

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

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
COMPON ; Contar componentes -- clase 155
 read linea
 new i, cnt, p
 set cnt = 0
 for i = 1:1:$length(linea, " ") do
 . set p = $piece(linea, " ", i)
 . if p '= "" set cnt = cnt + 1
 write "componentes=", cnt, !
 quit
```

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

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| linea |

linea := stdin nextLine trimBoth.

Transcript show: 'componentes=', (linea substrings: ' ') size printString; cr.
```

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

---

## Y de vuelta a la clase

Lo transferible: **cada frontera entre lenguajes tiene un coste, y ese coste es lo que decide si merece
la pena**. Hay tres tipos, de menor a mayor precio: **el proceso separado** —simple, aislado, y con
serialización en medio—; **la biblioteca compartida** —rápida, y con un ABI que hay que respetar (clase
157)—; y **la máquina virtual compartida** —lo más integrado y lo más frágil—. La regla que evita casi
todos los problemas: **cuantas menos fronteras y más gruesas, mejor**. Diez llamadas al día entre dos
lenguajes no son un problema; diez millones, sí.

⏮️ [Volver a la clase 155](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
