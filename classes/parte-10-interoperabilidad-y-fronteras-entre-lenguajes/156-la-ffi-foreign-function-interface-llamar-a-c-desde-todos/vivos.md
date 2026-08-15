# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 156

> [⬅️ Volver a la clase 156](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Doblar un número llamando a una función externa. Es el "hola mundo" de la interoperabilidad, y la
pregunta que hay detrás es **por qué siempre es C**. La respuesta no es que C sea mejor: es que **el ABI
de C es el que los sistemas operativos exponen** (clase 157), así que **hablar C es hablar con el
sistema**. Y esta página tiene los dos extremos: **Ada declara la interfaz con un `pragma` del
estándar**, y **RPG llama a una función de C con la misma sintaxis con que llama a un procedimiento
propio**.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es la **interfaz de función externa**, y estos lenguajes la enseñan porque **todos
> tuvieron que resolverla y llegaron a soluciones muy distintas**: en el estándar del lenguaje (Ada,
> Fortran 2003, RPG), con un lenguaje intermedio que se compila (Perl con XS, Tcl con SWIG), con
> descubrimiento en ejecución (CFFI en Lisp, FFI::Platypus en Perl, UFFI en Smalltalk) o simplemente
> declarando la biblioteca (Pascal).
>
> Y aparecen los cuatro problemas que toda FFI tiene que resolver: **los nombres, los tipos, la memoria y
> los errores**.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: un entero `n` → stdout: `resultado=<2n>`
- **Regla:** `llamar a doble(n) 'externo'`

| stdin | esperado |
|---|---|
| `5` | `resultado=10` |
| `0` | `resultado=0` |
| `7` | `resultado=14` |

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
```

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

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
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
```

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

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
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
```

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

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
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
```

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

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(defun doblar (x) (* 2 x))

(let ((n (read)))
  (format t "resultado=~D~%" (doblar n)))
```

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

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea
set n [string trim $linea]

proc doblar {x} { expr {2 * $x} }

puts "resultado=[doblar $n]"
```

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

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

sub doblar { return 2 * $_[0] }

my $n = <STDIN>;
chomp $n;

print "resultado=", doblar($n), "\n";
```

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

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>

// Con enlace de C: nombre sin decorar, para que cualquier lenguaje lo llame.
extern "C" long long doblar(long long x) {
    return 2 * x;
}

int main() {
    long long n{};
    if (!(std::cin >> n)) return 1;

    std::cout << "resultado=" << doblar(n) << '\n';
    return 0;
}
```

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
```

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

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 llamar: procedure options(main);

    declare n fixed binary(31);

    doblar: procedure (x) returns (fixed binary(31)) options(byvalue);
       declare x fixed binary(31) byvalue;
       return (2 * x);
    end doblar;

    get list (n);

    put skip list ('resultado=' || trim(char(doblar(n))));

 end llamar;
```

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

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
LLAMAR ; Llamada a funcion externa -- clase 156
 read n
 write "resultado=", $$doblar(n), !
 quit
 ;
doblar(x) ; devuelve el doble
 quit x * 2
```

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

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| n |

n := stdin nextLine trimBoth asNumber.

Transcript show: 'resultado=', (n * 2) printString; cr.
```

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

---

## Y de vuelta a la clase

Lo transferible: **una llamada a través de una FFI parece una llamada normal y no lo es**. Cruza cuatro
fronteras a la vez —**el nombre**, que puede estar decorado; **los tipos**, que hay que traducir;
**la memoria**, donde hay que decidir quién reserva y quién libera; y **los errores**, porque las
excepciones no cruzan—. De ahí la práctica que evita casi todos los fallos: **envolver la FFI en una
capa fina propia**, que traduzca los tipos, gestione la memoria y convierta los códigos de error en la
forma nativa del lenguaje — y no dejar que el resto del programa vea nunca la interfaz cruda.

⏮️ [Volver a la clase 156](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
