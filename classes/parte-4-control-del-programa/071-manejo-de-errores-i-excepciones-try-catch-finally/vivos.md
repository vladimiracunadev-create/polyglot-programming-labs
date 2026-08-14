# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 071

> [⬅️ Volver a la clase 071](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Dividir dos enteros, y que dividir por cero no reviente el programa. El caso más simple de manejo de
errores, y el que separa a estos lenguajes de forma más nítida de toda la Parte 4: **cuatro de ellos
tienen excepciones, cuatro no tienen ninguna forma de excepción, y tres tienen algo MEJOR que las
excepciones** — condiciones que se pueden manejar **sin destruir el contexto en que ocurrió el
error**.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es la **señalización y el manejo de errores**, y estos lenguajes lo enseñan porque
> contienen tanto el origen como el camino no tomado. **PL/I inventó el manejo estructurado de errores
> en 1964** con las condiciones `ON`, y su modelo permitía **reparar y continuar**, no solo capturar y
> abortar. **Common Lisp** llevó esa idea a su forma más completa con el sistema de condiciones y
> reinicios. Y **Smalltalk** tiene excepciones **reanudables**.
>
> Enfrente, **Fortran no tiene excepciones en absoluto**, y COBOL tiene manejo por sentencia —`ON SIZE
> ERROR`— en lugar de por bloque.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: una línea `a b` (dos enteros) → stdout: `resultado=<a/b entera>` o `error=division por cero` si b es 0
- **Regla:** `si b != 0 → a/b (entera); si b == 0 → mensaje de error`

| stdin | esperado |
|---|---|
| `10 2` | `resultado=5` |
| `7 0` | `error=division por cero` |
| `9 3` | `resultado=3` |

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
PROGRAM-ID. DIVSEG.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  TXT-A   PIC X(20).
01  TXT-B   PIC X(20).
01  A       PIC S9(9) COMP-3.
01  B       PIC S9(9) COMP-3.
01  R       PIC S9(9) COMP-3.
01  ED-R    PIC -(8)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    UNSTRING LINEA DELIMITED BY ALL SPACES INTO TXT-A TXT-B
    MOVE FUNCTION NUMVAL(TXT-A) TO A
    MOVE FUNCTION NUMVAL(TXT-B) TO B

    DIVIDE A BY B GIVING R
        ON SIZE ERROR
            DISPLAY "error=division por cero"
        NOT ON SIZE ERROR
            MOVE R TO ED-R
            DISPLAY "resultado=" FUNCTION TRIM(ED-R)
    END-DIVIDE

    STOP RUN.
```

**Lo que esta clase enseña en COBOL.** **COBOL no tiene `try`/`catch`. Tiene manejo de condiciones
por SENTENCIA**, y esa es una diferencia de diseño con consecuencias.

`ON SIZE ERROR` es una cláusula del propio `DIVIDE`, no un bloque que envuelva código. La rama de
error está **pegada a la operación que puede fallar**, y `NOT ON SIZE ERROR` es la rama de éxito. No
hay forma de "envolver veinte líneas" y capturar lo que sea que falle dentro.

La familia completa sigue el mismo patrón, y cubre lo que puede fallar en cada verbo:

```cobol
DIVIDE ... ON SIZE ERROR ...          *> desbordamiento o división por cero
READ ... AT END ...                   *> fin de fichero
READ ... INVALID KEY ...              *> clave no encontrada
STRING ... ON OVERFLOW ...            *> no cabe
CALL ... ON EXCEPTION ...             *> el programa no existe
```

La ventaja es que **es imposible olvidar dónde puede fallar algo**: la posibilidad está escrita en la
sentencia. La desventaja es la verbosidad, y que no hay propagación: cada nivel maneja lo suyo.

Para los errores que no pertenecen a una sentencia concreta, COBOL tiene las **DECLARATIVES**, que sí
son un manejador global:

```cobol
PROCEDURE DIVISION.
DECLARATIVES.
ERROR-FICHERO SECTION.
    USE AFTER STANDARD ERROR PROCEDURE ON CLIENTES.
MANEJAR.
    DISPLAY "fallo de E/S: " FILE-STATUS-CLIENTES.
END DECLARATIVES.
```

`USE AFTER ERROR` instala un manejador para un fichero, que se ejecuta automáticamente ante cualquier
fallo de E/S sobre él. Es exactamente el `ON` de PL/I, con otro nombre.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program divseg
   implicit none
   integer :: a, b

   read(*, *) a, b

   !  Fortran NO tiene excepciones: la comprobación es explícita, y punto.
   if (b == 0) then
      write(*, '(A)') 'error=division por cero'
   else
      write(*, '(A,I0)') 'resultado=', a / b
   end if
end program divseg
```

**Lo que esta clase enseña en Fortran.** **Fortran no tiene excepciones. Ninguna.** Ni `try`, ni
`catch`, ni `raise`, ni condiciones. En 2026, con el estándar de 2023, sigue sin tenerlas.

No es un olvido: es coherente con su dominio. Un manejador de excepciones implica un salto no local y
un desenrollado de pila, y las dos cosas **impiden vectorizar y reordenar**. En un bucle que se
ejecuta mil millones de veces, la mera posibilidad de que algo salte fuera limita al optimizador.

Lo que Fortran tiene son **códigos de estado**, que es el modelo de la clase siguiente:

```fortran
read(unidad, *, iostat=ios, iomsg=mensaje) valor
if (ios /= 0) then ...

allocate(v(n), stat=err, errmsg=mensaje)
if (err /= 0) then ...
```

`iostat`, `stat`, `iomsg` y `errmsg` son **argumentos opcionales**: si los pones, el error se te
devuelve; si no los pones, **el programa aborta**. Esa elección por llamada es muy característica.

Y para la aritmética, Fortran 2003 añadió el módulo **`ieee_arithmetic`**, que da acceso a las
banderas del procesador definidas por IEEE 754:

```fortran
use ieee_arithmetic
if (ieee_support_flag(ieee_divide_by_zero, x)) then
   call ieee_set_halting_mode(ieee_divide_by_zero, .false.)   ! no abortar
   ...
   call ieee_get_flag(ieee_divide_by_zero, ocurrio)           ! ¿pasó?
end if
```

Es manejo de errores **consultando banderas después**, no interrumpiendo el flujo. Encaja perfectamente
con el cálculo vectorizado: se procesan mil millones de elementos y al final se pregunta si alguno dio
problemas.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Divseg is
   A, B, R : Integer;
begin
   Get (A);
   Get (B);

   begin
      R := A / B;               --  B = 0 levanta Constraint_Error
      Put ("resultado="); Put (R, Width => 1); New_Line;
   exception
      when Constraint_Error =>
         Put_Line ("error=division por cero");
   end;
end Divseg;
```

**Lo que esta clase enseña en Ada.** Ada tiene excepciones desde 1983, con una diferencia importante
frente a Java o C++: **las excepciones de Ada no son objetos, son nombres**. No llevan datos ni
jerarquía de clases; son etiquetas de una situación.

```ada
Saldo_Insuficiente : exception;        --  se DECLARA como una constante
raise Saldo_Insuficiente with "faltan 20 euros";   --  Ada 2005: con mensaje
```

Eso las hace baratísimas y analizables. Y las cuatro predefinidas cubren la mayoría de los casos:
`Constraint_Error` (rango, índice, división por cero, nulo), `Program_Error`, `Storage_Error`
(memoria o pila agotada) y `Tasking_Error`.

Fíjate en que este programa **no comprueba `B = 0`**: la división levanta `Constraint_Error` por sí
sola. Es la misma filosofía de los subtipos de la clase 041 — el error se detecta en la operación, no
en una comprobación previa que alguien podría olvidar.

Y hay algo de fondo que conviene saber: **en aviónica y sistemas críticos, las excepciones suelen
prohibirse**. El perfil Ravenscar y las guías de certificación las restringen porque **el tiempo de
propagación de una excepción es difícil de acotar**, y en un sistema de tiempo real duro todo tiene
que tener un límite superior demostrable.

Ahí se usa el modelo de la clase siguiente: parámetros de estado, contratos que garantizan que el
error no puede ocurrir, y SPARK demostrándolo estáticamente. **La mejor excepción es la que se
demuestra imposible.**

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Divseg;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  A, B, R: Integer;

begin
  Read(A, B);

  try
    R := A div B;
    WriteLn('resultado=', IntToStr(R));
  except
    on E: EDivByZero do
      WriteLn('error=division por cero');
  end;
end.
```

**Lo que esta clase enseña en Pascal.** **El Pascal ISO no tiene excepciones.** `try`/`except` y
`try`/`finally` son de Delphi, incorporados en 1995 junto con la jerarquía de clases `Exception`, y
Free Pascal los adoptó.

Y hay una particularidad sintáctica que distingue a Object Pascal de casi todos los demás: **son dos
construcciones separadas que no se combinan**.

```pascal
try
  try
    ...
  except
    on E: EDivByZero do ...;
  end;
finally
  Recurso.Free;        { hay que ANIDAR: no existe try..except..finally }
end;
```

En Java, C# y Python se escribe `try/catch/finally` en un solo bloque. En Object Pascal hay que
anidar uno dentro de otro. Es más verboso y tiene una lógica: separa **manejar un error** de
**garantizar una limpieza**, que son dos preocupaciones distintas.

Y `try..finally` es, en la práctica, **la construcción más usada del lenguaje**, mucho más que
`try..except`. La razón es la clase 042: sin recolector de basura, cada objeto creado necesita su
`Free` garantizado.

```pascal
Lista := TStringList.Create;
try
  ...
finally
  Lista.Free;      { el idioma más repetido de todo el código Delphi }
end;
```

Es el mismo problema que C++ resuelve con RAII y Go con `defer`. Object Pascal eligió la
construcción explícita, con la ventaja de que se ve y el inconveniente de que se puede olvidar.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let* ((a (read))
       (b (read)))
  (handler-case
      (format t "resultado=~D~%" (truncate a b))
    (division-by-zero ()
      (format t "error=division por cero~%"))))
```

**Lo que esta clase enseña en Common Lisp.** `handler-case` **es** el `try/catch`, y funciona como se
espera. Pero es la parte aburrida: Lisp tiene además un **sistema de condiciones y reinicios** que es
estrictamente más potente y que casi ningún lenguaje copió.

La diferencia clave: **`handler-bind` ejecuta el manejador ANTES de desenrollar la pila**.

```lisp
(defun leer-registro (linea)
  (restart-case (parsear linea)
    (usar-valor (v) :report "Usar otro valor" v)      ; REINICIOS ofrecidos
    (saltar ()     :report "Ignorar esta línea" nil)))

(handler-bind ((error (lambda (c)
                        (invoke-restart 'saltar))))   ; el manejador ELIGE
  (dolist (l lineas) (leer-registro l)))
```

`parsear` no sabe qué hacer con un error, así que **ofrece opciones** con `restart-case`. Quien llama
—que sí conoce el contexto— elige una con `invoke-restart`. Y el manejador se ejecuta **encima del
punto que falló**, con toda la pila viva, así que puede reparar y continuar **en el sitio exacto**.

Con `try/catch` eso es imposible: para cuando el `catch` se ejecuta, los marcos entre medias ya se
destruyeron y solo queda reintentar todo desde fuera.

Ese diseño tiene una consecuencia práctica que se ve a diario: **cuando un programa Lisp falla en el
REPL, el depurador te ofrece una lista de reinicios** —reintentar, usar otro valor, definir la función
que faltaba, abortar— y puedes arreglar el problema y **continuar la ejecución** sin reiniciar.

Es la misma idea que las condiciones `ON` de PL/I de 1964, llevada a su forma completa. Dylan la
heredó; el resto de la industria eligió `try/catch`.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea
lassign [split [string trim $linea]] a b

if {[catch {expr {$a / $b}} r]} {
    puts "error=division por cero"
} else {
    puts "resultado=$r"
}
```

**Lo que esta clase enseña en Tcl.** **`catch` no es una construcción de excepciones: es un comando
que devuelve un número.** Ejecuta el cuerpo y devuelve el código de resultado —0 si todo fue bien, 1
si hubo error— dejando el valor o el mensaje en la variable que le des.

Eso lo convierte, literalmente, en el modelo de "errores como valores" de la clase siguiente, con
sintaxis de excepción. Y encaja con lo que se vio en la clase 070: **en Tcl todo comando devuelve uno
de cinco códigos**, y `catch` simplemente los expone en lugar de propagarlos.

Tcl 8.6 añadió `try`, que es azúcar sobre `catch` con mejor legibilidad:

```tcl
try {
    expr {$a / $b}
} trap {ARITH DIVZERO} {msg opciones} {
    puts "error=division por cero"
} on error {msg opciones} {
    puts "otro error: $msg"
} finally {
    puts "esto se ejecuta siempre"
}
```

`trap` casa contra el **código de error**, que en Tcl es una **lista** —`ARITH DIVZERO {divide by
zero}`— y no una clase. Casar por prefijo de lista da una jerarquía sin necesidad de herencia:
`trap {POSIX ENOENT}` o `trap {POSIX}` para cualquier error POSIX.

Y `error` lanza, con tres argumentos: mensaje, información de pila y **código estructurado**.

```tcl
error "saldo insuficiente" "" {BANCO SALDO 42}
```

Que el código de error sea un dato estructurado y no un tipo es muy propio de Tcl, y resulta
sorprendentemente práctico: se puede construir, comparar y serializar sin definir ninguna clase.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;
my ($x, $y) = split ' ', $linea;

my $r = eval { int($x / $y) };

if ($@) {
    print "error=division por cero\n";
} else {
    print "resultado=$r\n";
}
```

**Lo que esta clase enseña en Perl.** El manejo de errores clásico de Perl es **`eval` con bloque**, y
es de las partes del lenguaje que peor han envejecido:

```perl
eval { ... };          # ejecuta y captura lo que muera
if ($@) { ... }        # $@ contiene el error, o cadena vacía
```

Funciona y tiene **tres trampas** conocidas, que conviene conocer porque explican por qué existe
`Try::Tiny`:

1. **`$@` es global** y cualquier cosa puede pisarlo — incluido un destructor que se ejecute al salir
   del `eval`.
2. **Hay que comprobar `$@` inmediatamente**, antes de cualquier otra operación.
3. **`$@` puede quedar vacío aunque haya habido error**, en casos límite documentados.

Por eso el módulo `Try::Tiny` fue durante quince años prácticamente obligatorio:

```perl
use Try::Tiny;
try   { ... }
catch { warn "error: $_" }
finally { ... };
```

Y **Perl 5.34 incorporó `try`/`catch` al lenguaje**, estabilizado en 5.40:

```perl
use v5.36;
use feature 'try';

try {
    my $r = $x / $y;
} catch ($e) {
    say "error: $e";
}
```

Que un lenguaje de 1987 añadiera manejo de errores con sintaxis moderna en 2021 es, otra vez, el
argumento de esta sección. Y `die` puede lanzar **cualquier referencia**, no solo cadenas, así que las
excepciones como objetos existen desde siempre: `die Mi::Error->new(...)`.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>
#include <stdexcept>

int main() {
    int a{}, b{};
    if (!(std::cin >> a >> b)) return 1;

    try {
        //  OJO: en C++ la división entera por cero NO lanza: es comportamiento
        //  indefinido. Hay que comprobarlo y lanzar explícitamente.
        if (b == 0) {
            throw std::domain_error("division por cero");
        }
        std::cout << "resultado=" << (a / b) << '\n';
    } catch (const std::domain_error&) {
        std::cout << "error=division por cero\n";
    }
    return 0;
}
```

**Lo que esta clase enseña en C++.** El comentario del código es el contenido de la clase: **la
división entera por cero en C++ NO lanza una excepción. Es comportamiento indefinido.** El programa
puede abortar, dar basura o —lo peor— hacer que el compilador asuma que nunca ocurre y elimine el
código que lo comprueba.

Es una diferencia real con Ada, Pascal, Lisp, Perl y Smalltalk, donde sí es un error definido. En C++
hay que comprobarlo a mano.

Y lo que C++ aporta de verdad a esta clase no es `try/catch`: es **RAII**, que resuelve el problema
del `finally` sin necesidad de `finally`.

```cpp
{
    std::lock_guard<std::mutex> cierre(m);     // se bloquea
    std::ifstream f("datos.txt");              // se abre
    procesar(f);                               // si esto lanza...
}   // ...el mutex se libera y el fichero se cierra IGUAL
```

**C++ es el único lenguaje mayoritario sin `finally`, y es a propósito.** Stroustrup ha argumentado
repetidamente que `finally` es la solución equivocada: obliga a escribir la limpieza en cada sitio
donde se usa el recurso, mientras que el destructor la escribe **una vez, en la clase del recurso**.

La contrapartida es una regla estricta: **un destructor no debe lanzar nunca**. Si lanza durante el
desenrollado de otra excepción, el programa llama a `std::terminate`. Por eso los destructores se
marcan `noexcept` por defecto desde C++11.

Y `noexcept` en una función es una promesa comprobada: si algo escapa, `terminate`. Permite al
compilador generar código mejor —sin tablas de desenrollado— y es la base de que `std::vector` pueda
mover elementos en lugar de copiarlos al crecer.

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

dcl-pi DIVSEG;
  a int(10) const;
  b int(10) const;
end-pi;

dcl-s r      int(10);
dcl-s salida char(40);

monitor;
  r = %div(a : b);
  salida = 'resultado=' + %char(r);
on-error;
  salida = 'error=division por cero';
endmon;

dsply salida;

*inlr = *on;
return;
```

**Lo que esta clase enseña en RPG.** **`monitor` / `on-error` / `endmon` es el `try`/`catch` de RPG**,
y llegó con la versión 5 en 2001. Antes de eso, el manejo de errores era… los indicadores.

En el RPG clásico, cada operación que podía fallar llevaba un indicador en una columna concreta:

```text
     C     CLAVE         CHAIN     CLIENTES                           50
```

Ese `50` significa: "si la operación falla, enciende `*IN50`". El código de después consultaba
`*IN50` para saber si había ido bien. **El manejo de errores eran variables globales numeradas**, con
todos los problemas que eso implica: nadie recuerda qué indicador es cuál, y olvidar comprobarlo no
da ningún aviso.

`monitor` también acepta filtrar por **rango de códigos de error**, lo que da una jerarquía sin
clases:

```rpgle
monitor;
  ...
on-error 00121;          // índice de matriz fuera de rango
  ...
on-error *file;          // cualquier error de fichero
on-error *all;           // cualquiera
endmon;
```

Y RPG tiene además el manejador global heredado del ciclo: el subprocedimiento **`*PSSR`**, que se
ejecuta ante cualquier error no capturado y puede decidir si continuar o terminar. Es el equivalente
de las DECLARATIVES de COBOL y del `ON ERROR` de PL/I.

Lo que no tiene RPG es `finally`. La limpieza se escribe en `*PSSR` o se repite.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 divseg: procedure options(main);

    declare (a, b, r) fixed binary(31);

    on zerodivide begin;
       put skip list ('error=division por cero');
       stop;
    end;

    get list (a, b);

    r = divide(a, b, 31);
    put skip list ('resultado=' || trim(char(r)));

 end divseg;
```

**Lo que esta clase enseña en PL/I.** **Aquí nació el manejo estructurado de errores.** En 1964, cuando
FORTRAN comprobaba códigos y COBOL tenía cláusulas por sentencia, PL/I introdujo las **condiciones
`ON`**: un manejador que se **instala** y queda activo, y al que el sistema salta cuando ocurre la
condición.

```pli
on zerodivide   ...      /* división por cero */
on overflow     ...      /* desbordamiento en punto flotante */
on fixedoverflow ...     /* desbordamiento decimal */
on conversion   ...      /* texto no numérico */
on endfile(f)   ...      /* fin de fichero */
on subscriptrange ...    /* índice fuera de rango */
on error        ...      /* cualquier cosa */
```

Fíjate en la diferencia con `try/catch`: **no hay bloque**. `on` no envuelve código; declara que a
partir de ahí, y hasta que se salga del ámbito, esa condición tiene ese manejador. Es **ámbito
dinámico** aplicado al manejo de errores — el mismo mecanismo que `handler-bind` de Common Lisp y que
las variables `new` de M.

Y esa es la clave de por qué el modelo de PL/I es más potente que el `try/catch` que heredamos: **el
manejador se ejecuta encima del punto que falló, sin desenrollar la pila**. Si no hace `goto` ni
`stop`, la ejecución **continúa donde estaba**.

```pli
on conversion begin;
   onsource() = '0';     /* CORRIGE el dato que falló... */
end;                      /* ...y la conversión se REINTENTA con el valor nuevo */
```

`onsource()` es una **pseudovariable**: representa el dato que provocó el error y se le puede
asignar. Junto a `oncode()`, `onchar()` y `onloc()`, forman un conjunto de introspección del error que
ningún lenguaje moderno tiene.

Dijkstra criticó a PL/I por su tamaño. Esta parte, sin embargo, era mejor que lo que vino después.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
DIVSEG ; Excepciones -- clase 071
 read linea
 set a = $piece(linea, " ", 1)
 set b = $piece(linea, " ", 2)
 if b = 0 write "error=division por cero",! quit
 write "resultado=", a\b, !
 quit
```

**Lo que esta clase enseña en M.** El M estándar de 1977 **no tenía manejo de errores**: un error
abortaba la rutina y devolvía el control al nivel superior, y punto. La comprobación previa —como en
este programa— era la única forma.

Las implementaciones añadieron cada una la suya, y eso produjo la fragmentación más visible del
lenguaje:

```mumps
 set $ztrap = "MANEJADOR^RUTINA"     ; GT.M, YottaDB, Caché: manejador global
 set $etrap = "do ERROR^UTIL"        ; el estándar posterior
```

`$ztrap` y `$etrap` son **variables especiales que contienen código**: cuando ocurre un error, M
ejecuta lo que haya en esa cadena. Es la indirección de la clase 068 aplicada al manejo de errores, con
la misma potencia y la misma imposibilidad de análisis estático.

El estándar **M95** incorporó por fin una estructura moderna, y las implementaciones actuales la
tienen:

```mumps
 try {
   set r = a/b
 } catch e {
   write "error: ", e.Name, !
 }
```

Esa sintaxis con llaves es de **InterSystems ObjectScript**, el descendiente de M de la clase 043, y
convive con el M clásico en el mismo sistema.

Y hay una variable que conviene conocer: **`$ecode`**, que contiene la lista de errores activos según
el estándar, y **`$stack`**, que da acceso a la pila de llamadas. Con ellas se puede escribir un
manejador portable — aunque en la práctica casi todo el código M usa las extensiones de su
implementación.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| partes a b |

partes := stdin nextLine substrings collect: [ :cada | cada asNumber ].
a := partes first.
b := partes second.

[ Transcript show: 'resultado=', (a // b) printString; cr ]
    on: ZeroDivide
    do: [ :e | Transcript show: 'error=division por cero'; cr ].
```

**Lo que esta clase enseña en Smalltalk.** **`on:do:` es un mensaje enviado a un bloque.** No hay
`try`, no hay `catch` y no hay sintaxis: el bloque protegido es el receptor, la clase de excepción y
el manejador son los argumentos.

```smalltalk
BlockClosure >> on: unaClaseDeExcepcion do: unManejador
```

Y las excepciones son **objetos con protocolo propio**, lo que da al manejador opciones que el
`catch` de Java o C++ no tienen:

```smalltalk
[ ... ] on: Error do: [ :e |
    e return: 0.       "termina el bloque protegido devolviendo 0"
    e retry.           "vuelve a EJECUTAR el bloque protegido desde el principio"
    e resume: 42.      "CONTINÚA donde saltó, como si la expresión valiera 42"
    e pass.            "delega en el manejador de más afuera"
    e signal.          "vuelve a lanzarla"
].
```

**`resume:` es la que importa.** Reanuda la ejecución **en el punto exacto donde se señaló el error**,
sustituyendo el valor de la expresión que falló. Eso solo es posible porque, igual que en PL/I y en
CommonLisp, **el manejador se ejecuta antes de desenrollar la pila**.

No todas las excepciones son reanudables: `Error` no lo es, `Warning` sí. La clase declara si lo es
con `isResumable`, y el sistema lo comprueba.

Y `ensure:` es el `finally`, también como mensaje:

```smalltalk
[ ... ] ensure: [ recurso close ].         "pase lo que pase"
[ ... ] ifCurtailed: [ registrar ].        "SOLO si termina anormalmente"
```

`ifCurtailed:` no tiene equivalente en el núcleo: distingue "termina" de "termina mal", que son
cosas distintas y en Java hay que averiguar con una bandera.

---

## Y de vuelta a la clase

La idea que hay que llevarse: **el `try/catch` moderno desenrolla la pila ANTES de ejecutar el
manejador**, y con ella se destruye el contexto donde ocurrió el error. Cuando el manejador decide
que se puede continuar, ya es tarde: hay que reintentar la operación entera desde fuera.

PL/I, Common Lisp y Smalltalk hacen lo contrario: **el manejador se ejecuta encima del punto que
falló**, con todo vivo, y puede decidir reparar y reanudar. Es estrictamente más potente, casi nadie
lo copió, y saber que existe cambia cómo se leen las limitaciones del `catch` que usas a diario.

⏮️ [Volver a la clase 071](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
