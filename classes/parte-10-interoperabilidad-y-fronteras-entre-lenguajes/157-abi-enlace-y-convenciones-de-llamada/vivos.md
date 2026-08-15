# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 157

> [⬅️ Volver a la clase 157](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Comparar dos anchos de palabra y decir si son compatibles. Es la comprobación más tosca posible de un
ABI, y detrás está la razón por la que la clase 156 funciona o no: **cuando dos lenguajes se llaman, hay
un acuerdo no escrito sobre dónde van los argumentos, quién limpia la pila y cómo se llama de verdad la
función**. Y esta página tiene el ejemplo que mejor lo enseña: **Fortran pasa un argumento oculto que no
aparece en ninguna firma** —la longitud de cada cadena— y **durante cuarenta años nadie se puso de
acuerdo en dónde ponerlo**.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es la **interfaz binaria de aplicación**, y estos lenguajes la enseñan porque **cada uno
> tiene una convención distinta y todos tuvieron que encajar**. Fortran y COBOL pasan por referencia; C
> pasa por valor. C++ decora los nombres y cada compilador de forma distinta. Ada declara la convención por
> tipo. Y **IBM resolvió el problema dos veces a nivel de plataforma** —Language Environment en z/OS e ILE
> en IBM i— definiendo un ABI común para todos los lenguajes en lugar de que todos imitaran a C.
>
> Y aparecen las cuatro capas del acuerdo: **los nombres, el paso de argumentos, la disposición de los
> datos y quién limpia**.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: una línea `a b` (ancho de bits de cada componente) → stdout: `abi=<compatible|incompatible>`
- **Regla:** `compatible si los anchos coinciden`

| stdin | esperado |
|---|---|
| `64 64` | `abi=compatible` |
| `64 32` | `abi=incompatible` |
| `32 32` | `abi=compatible` |

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
```

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

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
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
```

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

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
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
```

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

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
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
```

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

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let ((a (read))
      (b (read)))
  (format t "abi=~A~%" (if (= a b) "compatible" "incompatible")))
```

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

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea
lassign [string trim $linea] a b

puts "abi=[expr {$a == $b ? {compatible} : {incompatible}}]"
```

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

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;
my ($a1, $b1) = split ' ', $linea;

print "abi=", ($a1 == $b1 ? 'compatible' : 'incompatible'), "\n";
```

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

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <cstdint>
#include <iostream>

int main() {
    std::int64_t a{}, b{};
    if (!(std::cin >> a >> b)) return 1;

    std::cout << "abi=" << (a == b ? "compatible" : "incompatible") << '\n';
    return 0;
}
```

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
```

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

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 abicmp: procedure options(main);

    declare (a, b) fixed binary(31);

    get list (a, b);

    if a = b then
       put skip list ('abi=compatible');
    else
       put skip list ('abi=incompatible');

 end abicmp;
```

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

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
ABICMP ; Comparar anchos de ABI -- clase 157
 read linea
 new a, b
 set a = $piece(linea, " ", 1)
 set b = $piece(linea, " ", 2)
 write "abi=", $select(a = b : "compatible", 1 : "incompatible"), !
 quit
```

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

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| linea partes a b |

linea := stdin nextLine trimBoth.
partes := linea substrings: ' '.

a := (partes at: 1) asNumber.
b := (partes at: 2) asNumber.

Transcript
    show: 'abi=', (a = b ifTrue: [ 'compatible' ] ifFalse: [ 'incompatible' ]);
    cr.
```

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

---

## Y de vuelta a la clase

Lo transferible: **un ABI es un contrato binario, y romperlo no da un error de compilación: da un
programa que funciona hasta que no**. De ahí las tres reglas que evitan casi todos los problemas:
**usar los tipos de tamaño garantizado en las fronteras** —`int32_t`, `c_int`, `COMP-5`, `Interfaces.C`,
nunca los tipos cuyo tamaño depende de la plataforma—; **pasar estructuras por puntero, no por valor**,
porque el relleno y la alineación varían; y **versionar la interfaz explícitamente**, porque cuando algo
cambie hará falta detectarlo — que es exactamente lo que la firma de programa de servicio de IBM i hace
por sistema (clase 143).

⏮️ [Volver a la clase 157](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
