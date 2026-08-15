# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 139

> [⬅️ Volver a la clase 139](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Una prueba: `a + b` debería dar `esperado`. El programa es minúsculo a propósito, porque lo que esta
clase compara no es el código: es **qué significa "prueba unitaria" en cada ecosistema**. Y hay
sorpresas de fecha: **el primer marco de pruebas unitarias de la historia se escribió en Smalltalk en
1994**, y de él descienden JUnit, PyTest, RSpec y todos los demás. El resto de esta página lo adoptó
después.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es la **prueba automatizada como parte del código fuente**, y estos lenguajes lo
> enseñan porque llegaron a ella por caminos opuestos. **Smalltalk la inventó** —SUnit, de Kent Beck—.
> **Ada la lleva en el lenguaje** con contratos que se comprueban solos (clase 118). **Fortran y COBOL
> vivieron cincuenta años sin marcos de pruebas**, con la comparación de ficheros de salida como método.
> Y **Perl trajo TAP**, el formato de salida de pruebas que hoy usan lenguajes que nunca han visto Perl.
>
> Y el eje que las ordena es **qué se considera la unidad**: un método, un procedimiento, un programa
> entero o un fichero de salida.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: una línea `a b esperado` → stdout: `test=<pasa|falla>`
- **Regla:** `pasa si a + b == esperado`

| stdin | esperado |
|---|---|
| `3 4 7` | `test=pasa` |
| `2 2 5` | `test=falla` |
| `10 5 15` | `test=pasa` |

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
PROGRAM-ID. PRUEBA.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  C-A     PIC X(20).
01  C-B     PIC X(20).
01  C-E     PIC X(20).
01  A       PIC S9(9) COMP.
01  B       PIC S9(9) COMP.
01  ESPER   PIC S9(9) COMP.

PROCEDURE DIVISION.
    ACCEPT LINEA
    UNSTRING LINEA DELIMITED BY ALL SPACES
        INTO C-A C-B C-E
    END-UNSTRING

    COMPUTE A     = FUNCTION NUMVAL(C-A)
    COMPUTE B     = FUNCTION NUMVAL(C-B)
    COMPUTE ESPER = FUNCTION NUMVAL(C-E)

    IF A + B = ESPER
        DISPLAY "test=pasa"
    ELSE
        DISPLAY "test=falla"
    END-IF
    STOP RUN.
```

**Lo que esta clase enseña en COBOL.** COBOL pasó **casi cincuenta años sin marcos de pruebas
unitarias**, y entender por qué explica muchísimo sobre la cultura de estos sistemas.

La razón es de granularidad: **la unidad no era un procedimiento, era un programa entero**. Un programa
COBOL de lote lee ficheros, calcula y escribe ficheros, así que **la prueba consistía en preparar
ficheros de entrada conocidos, ejecutar el programa y comparar la salida con una salida esperada
guardada**.

```jcl
//PASO1  EXEC PGM=MIPGM
//ENTRADA  DD DSN=PRUEBA.ENTRADA.CASO01,DISP=SHR
//SALIDA   DD DSN=&&TEMP,DISP=(NEW,PASS)
//PASO2  EXEC PGM=IDCAMS       <-- comparar con la salida esperada
```

**Eso es una prueba de regresión, y funciona.** No es una prueba unitaria: es lo que hoy se llamaría
una prueba de caracterización, o *golden file testing* — y sigue siendo la técnica de referencia para
sistemas que uno no se atreve a tocar.

Y hoy sí hay marcos:

```cobol
      *> GnuCOBOL: cobol-unit-test / cobol-check
       TESTSUITE "calculos"
           TESTCASE "suma basica"
               PERFORM CALCULAR
               EXPECT WS-RESULTADO TO BE 7
```

**`cobol-check`** es el marco moderno, y funciona **insertando código de prueba en una copia del
programa** antes de compilarlo — porque COBOL no tiene reflexión ni forma de invocar un párrafo desde
fuera.

Y `PERFORM` es lo que hace posible probar por partes: **un párrafo se puede ejecutar aisladamente**
(clase 084), que es la unidad más pequeña que COBOL ofrece.

La lección para esta clase es incómoda y real: **el legado sin pruebas no se prueba escribiendo
pruebas unitarias**. Se prueba **capturando el comportamiento actual** con ficheros de entrada y
salida, y solo después se refactoriza — que es exactamente lo que la clase 150 desarrollará.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program prueba
   implicit none
   integer :: a, b, esperado

   read(*, *) a, b, esperado

   if (a + b == esperado) then
      write(*, '(A)') 'test=pasa'
   else
      write(*, '(A)') 'test=falla'
   end if
end program prueba
```

**Lo que esta clase enseña en Fortran.** Fortran tiene un problema propio con las pruebas unitarias que
ningún otro lenguaje de esta página comparte con la misma intensidad: **¿qué significa "igual" cuando
el resultado es un número en coma flotante?**

```fortran
if (resultado == 3.14159) then      ! CASI SIEMPRE FALSO
if (abs(resultado - esperado) < 1.0e-10) then    ! tolerancia absoluta
if (abs(resultado - esperado) <= tol * abs(esperado)) then   ! RELATIVA
```

**La comparación exacta es casi siempre un error**, porque el mismo cálculo con distinto compilador,
distinta optimización o distinto orden de sumas **da un último dígito diferente** (clase 073).

De ahí que los marcos de Fortran tengan aserciones con tolerancia como primitiva de primera clase:

```fortran
call assert_equal(esperado, obtenido, tolerance=1.0e-12_dp)
call assert_relative_equal(esperado, obtenido, 1.0e-8_dp)
```

Los marcos del ecosistema actual:

| Marco | Notas |
|---|---|
| **pFUnit** | de la NASA; **soporta MPI**: pruebas en paralelo con N procesos |
| **test-drive** | del *Fortran Standard Library*; ligero, sin preprocesador |
| **FRUIT** | veterano, genera el corredor con Ruby |
| **Vegetables** | moderno, con descubrimiento automático |

**pFUnit merece destacarse por lo de MPI**: una prueba puede declarar `@test(npes=[1,2,4])` y el marco
**la ejecuta con 1, 2 y 4 procesos**, comprobando que el resultado no depende del reparto.

Ese es el fallo característico del cálculo paralelo —**un resultado que cambia según el número de
procesos**— y es la clase de cosa que solo se caza con una prueba diseñada para ello.

Y el `@test` revela algo del ecosistema: **la mayoría de los marcos de Fortran usan un preprocesador**,
porque el lenguaje no tiene reflexión y **hay que generar el programa que llama a cada prueba**. Es el
mismo problema que COBOL en esta página, resuelto con generación de código.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Prueba is
   A, B, Esperado : Integer;
begin
   Get (A);
   Get (B);
   Get (Esperado);

   if A + B = Esperado then
      Put_Line ("test=pasa");
   else
      Put_Line ("test=falla");
   end if;
end Prueba;
```

**Lo que esta clase enseña en Ada.** Ada tiene una posición peculiar en esta clase: **buena parte de lo
que en otros lenguajes se escribe como prueba unitaria, en Ada está en el lenguaje**.

```ada
function Dividir (A, B : Integer) return Integer
   with Pre  => B /= 0,
        Post => Dividir'Result * B <= A;

subtype Porcentaje is Integer range 0 .. 100;
type Grados is delta 0.01 range -90.0 .. 90.0;
```

**Cada uno de esos ejemplos elimina una familia entera de pruebas**: no hace falta probar que la
función rechaza un divisor cero, ni que el porcentaje no se sale de rango — **el compilador o el
sistema de ejecución lo garantizan** (clases 118 y 124).

Y con SPARK, **se demuestra**, con lo que la prueba deja de ser una muestra y pasa a ser una prueba en
el sentido matemático.

Lo que queda por probar es la lógica de negocio, y para eso el ecosistema tiene:

```ada
--  AUnit: descendiente directo de JUnit, y por tanto de SUnit (1994)
overriding procedure Run_Test (T : in out Test_Suma) is
begin
   Assert (Sumar (3, 4) = 7, "3+4 debería ser 7");
end Run_Test;
```

| Herramienta | Qué hace |
|---|---|
| **AUnit** | pruebas unitarias al estilo xUnit |
| **GNATtest** | **genera el esqueleto de pruebas leyendo las especificaciones** |
| **GNATcoverage** | cobertura **sin instrumentar**, con MC/DC para certificación |
| **gnatprove** | demuestra, en lugar de probar |

**GNATtest merece la explicación**: recorre los ficheros `.ads` —las especificaciones— y **genera un
esqueleto de prueba para cada subprograma público**, incluida la comprobación de los contratos.

Eso responde a la pregunta "¿qué pruebo?" con la respuesta "todo lo que expones", y **detecta cuando
alguien añade una operación pública sin prueba**.

Y **GNATcoverage con MC/DC** es un requisito de la certificación aeronáutica DO-178C nivel A: **no
basta con ejecutar cada rama; hay que demostrar que cada condición individual de cada decisión ha
influido por sí sola en el resultado**.

Es el estándar de cobertura más exigente que existe, y explica por qué Ada tiene herramientas que otros
ecosistemas no necesitan.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Prueba;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  A, B, Esperado: Integer;

begin
  Read(A, B, Esperado);

  if A + B = Esperado then
    WriteLn('test=pasa')
  else
    WriteLn('test=falla');
end.
```

**Lo que esta clase enseña en Pascal.** El ecosistema Pascal adoptó xUnit pronto y con nombres
reconocibles:

```pascal
type
  TPruebaSuma = class(TTestCase)
  published                       { published: ¡la clave! }
    procedure PruebaBasica;
  end;

procedure TPruebaSuma.PruebaBasica;
begin
  CheckEquals(7, Sumar(3, 4), 'la suma de 3 y 4');
end;
```

**La palabra `published` es lo interesante de esta página**, y conecta con la clase 108.

En Object Pascal, **los miembros `published` generan información de tipo en tiempo de ejecución
(RTTI)**, mientras que los `public` no. Y el marco de pruebas **recorre esa RTTI para descubrir los
métodos de prueba** sin que haya que registrarlos uno a uno.

```pascal
RegisterTest(TPruebaSuma);      { basta con registrar la CLASE }
```

Eso es lo que Fortran y COBOL de esta página resuelven con un preprocesador: **Pascal lo resuelve con
reflexión**, y `published` es exactamente el mecanismo que Delphi inventó para el inspector de
propiedades del diseñador visual (clase 108).

**La misma característica que hacía funcionar el diseñador de formularios en 1995 es la que hace
funcionar el descubrimiento de pruebas.** Es un buen ejemplo de una decisión de diseño que rinde en un
sitio inesperado.

Los marcos del ecosistema:

| Marco | Notas |
|---|---|
| **FPCUnit** | en la distribución de Free Pascal; integrado en Lazarus |
| **DUnit** | el clásico de Delphi |
| **DUnitX** | moderno: atributos, casos con datos, `[Test]` |
| **Delphi-Mocks** | objetos simulados con interfaces |

Y **DUnitX** usa atributos en lugar de `published`:

```pascal
[Test]
[TestCase('basica', '3,4,7')]
[TestCase('ceros', '0,0,0')]
procedure PruebaSuma(A, B, Esperado: Integer);
```

**Un caso con datos**: la misma prueba con varios juegos de valores, declarados como atributos. Es la
misma idea que `@pytest.mark.parametrize`, y llegó a Delphi por el mismo camino que a todos: **desde
Smalltalk, vía JUnit**.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let ((a (read))
      (b (read))
      (esperado (read)))
  (format t "test=~A~%" (if (= (+ a b) esperado) "pasa" "falla")))
```

**Lo que esta clase enseña en Common Lisp.** Lisp tiene una relación con las pruebas que se deriva de
su modelo de la Parte 8: **el ciclo de prueba es más corto que en ningún otro lenguaje de esta
página**, porque **la función se recompila sola y se vuelve a llamar sin reiniciar nada** (clase 124).

En la práctica, un desarrollador de Lisp **prueba constantemente en el REPL** mientras escribe, y la
prueba automatizada formaliza lo que ya se estaba haciendo a mano.

Los marcos del ecosistema:

| Marco | Notas |
|---|---|
| **FiveAM** | el más usado; `is`, `signals`, `finishes`, suites anidadas |
| **Parachute** | moderno, con dependencias entre pruebas |
| **Rove** | sucesor de Prove |
| **1AM / lisp-unit** | mínimos, sin dependencias |

```lisp
(def-suite aritmetica)
(in-suite aritmetica)

(test suma-basica
  (is (= 7 (sumar 3 4)))
  (is (= 0 (sumar 0 0)))
  (signals division-by-zero (dividir 1 0)))

(run! 'aritmetica)
```

**`signals` comprueba que se señala una condición concreta**, y encaja con el sistema de condiciones de
la clase 116.

Y Lisp tiene dos capacidades en esta clase que no tienen equivalente directo:

**Primera, las macros permiten inventar la sintaxis de las pruebas.** `test`, `is` y `signals` no son
palabras del lenguaje: son macros, y cualquiera puede escribir las suyas. Por eso hay tantos marcos de
pruebas en Lisp: **escribir uno básico son cincuenta líneas**.

**Y segunda, `trace` y la redefinición permiten simular sin marco de simulación**:

```lisp
(defun consultar-bd (id) (error "no llamar en pruebas"))    ; redefinir y ya está
```

**Sustituir una función por otra en marcha es una operación normal**, así que los objetos simulados
—los *mocks*— no necesitan biblioteca. Es lo mismo que Smalltalk y Perl de esta página, y lo contrario
de Ada y C++, donde hay que haber previsto el punto de sustitución en el diseño.

Es un patrón general que la clase 151 retomará: **cuanto más dinámico el lenguaje, menos ceremonia
necesita la prueba — y menos garantías da el compilador**.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea
lassign [string trim $linea] a b esperado

puts "test=[expr {$a + $b == $esperado ? {pasa} : {falla}}]"
```

**Lo que esta clase enseña en Tcl.** Tcl trae **su marco de pruebas en la distribución**, y con una
propiedad que lo distingue: **es el mismo que se usa para probar el propio Tcl**.

```tcl
package require tcltest
namespace import ::tcltest::*

test suma-1.1 {suma basica} -body {
    sumar 3 4
} -result 7

test suma-1.2 {division por cero} -body {
    dividir 1 0
} -returnCodes error -result "divide by zero"

cleanupTests
```

La estructura de `tcltest` tiene detalles que merecen comentarse:

**El nombre `suma-1.1` es una convención**, no un requisito: `nombre-grupo.caso`, y permite ejecutar
subconjuntos con patrones: `-match suma-1.*`.

**`-setup` y `-cleanup`** dan preparación y limpieza por prueba, y **`-constraints`** condiciona la
ejecución:

```tcl
test archivo-2.1 {...} -constraints {unix root} -body { ... }
::tcltest::testConstraint tieneBaseDatos [expr {[catch {package require tdbc}] == 0}]
```

**Las restricciones son la característica más práctica**: una prueba que necesita Windows, o permisos
de administrador, o una biblioteca opcional, **se declara y se omite limpiamente** en lugar de fallar.

Es la respuesta al problema de las pruebas que solo pasan en la máquina de alguien, y es un mecanismo
que muchos marcos modernos han acabado añadiendo (`@pytest.mark.skipif`, `#[ignore]`).

Y Tcl tiene una capacidad de simulación que se deriva de la clase 138: **`rename` intercepta cualquier
comando**.

```tcl
rename ::consultarBD ::consultarBD_real
proc ::consultarBD {id} { return {simulado} }
...
rename ::consultarBD {}                       ;# borrar el simulado
rename ::consultarBD_real ::consultarBD        ;# restaurar
```

**Sustituir un comando del sistema durante una prueba y devolverlo después** es una operación de dos
líneas, y no requiere que el código bajo prueba haya previsto nada.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;
my ($a1, $b1, $esperado) = split ' ', $linea;

print "test=", ($a1 + $b1 == $esperado ? 'pasa' : 'falla'), "\n";
```

**Lo que esta clase enseña en Perl.** Perl aportó a esta clase algo que hoy usan lenguajes que nunca lo
han tocado: **TAP, el *Test Anything Protocol***.

```text
1..3
ok 1 - la suma de 3 y 4
not ok 2 - la resta de 10 y 3
#   Failed test 'la resta de 10 y 3'
#          got: 8
#     expected: 7
ok 3 - el producto
```

**Ese formato de texto plano es el protocolo**, y su idea es de una simplicidad que explica su éxito:
**la prueba imprime líneas `ok` o `not ok`, y un programa aparte las cuenta e informa**.

Eso desacopla completamente la prueba del corredor:

- **La prueba puede estar escrita en cualquier lenguaje.**
- **El corredor no necesita saber nada del lenguaje probado.**
- **Y la salida es legible por una persona sin herramientas.**

TAP nació en 1987 con el propio Perl —para probar el intérprete— y hoy tiene implementaciones en C,
Python, JavaScript, PHP, Java, Go y varias decenas más. **Es probablemente la contribución más
duradera de Perl a la ingeniería de software**, por delante de las expresiones regulares.

El ecosistema de Perl:

```perl
use Test::More tests => 3;
is(sumar(3, 4), 7, 'la suma de 3 y 4');
is_deeply($estructura, $esperado, 'la estructura completa');
like($texto, qr/^error:/, 'el mensaje de error');
done_testing();
```

| Módulo | Qué añade |
|---|---|
| **Test::More** | el estándar: `is`, `ok`, `like`, `is_deeply` |
| **Test2::V0** | la generación moderna, más estricta |
| **Test::Deep** | comparaciones de estructuras con comodines |
| **Test::MockModule** | sustituir funciones de otro módulo |
| **Devel::Cover** | cobertura de sentencias, ramas y condiciones |
| **prove** | el corredor: `prove -lr t/` |

Y **`is_deeply` merece la mención** porque resuelve el problema de la clase 100: **comparar dos
estructuras anidadas y decir en qué punto exacto difieren**.

```text
#   Failed test 'la estructura'
#     Structures begin differing at:
#          $got->{usuarios}[2]{edad} = 30
#     $expected->{usuarios}[2]{edad} = 31
```

**Esa ruta —`{usuarios}[2]{edad}`— es lo que convierte un fallo en un diagnóstico**, y es lo que un
`assert a == b` sobre estructuras grandes nunca da.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>

int main() {
    long long a{}, b{}, esperado{};
    if (!(std::cin >> a >> b >> esperado)) return 1;

    std::cout << "test=" << (a + b == esperado ? "pasa" : "falla") << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** C++ tiene el problema de esta clase en su forma más aguda: **el
lenguaje no tiene reflexión**, así que **no hay forma automática de descubrir las pruebas**.

Y la solución que todo el ecosistema adoptó es la misma, y es instructiva: **macros que registran en el
arranque**.

```cpp
TEST(Aritmetica, SumaBasica) {
    EXPECT_EQ(7, sumar(3, 4));
}
```

Esa macro se expande, aproximadamente, a **una clase con un método y un objeto global cuyo constructor
la registra en una lista**. Y como los objetos globales se construyen antes de `main` (clase 123),
**para cuando el corredor arranca, la lista ya está llena**.

Es un uso deliberado de la inicialización estática —la misma que causa el fiasco del orden de la clase
123— y es el patrón de registro más extendido de C++.

El ecosistema:

| Marco | Notas |
|---|---|
| **GoogleTest** | el más usado; `EXPECT_*` (sigue) y `ASSERT_*` (aborta) |
| **Catch2** | solo cabeceras; `REQUIRE(a + b == c)` |
| **doctest** | como Catch2, pero compila mucho más rápido |
| **Boost.Test** | veterano y completo |
| **GoogleMock** | objetos simulados sobre interfaces virtuales |

**Catch2 tiene un truco que merece explicarse**, porque parece magia:

```cpp
REQUIRE(sumar(3, 4) == 8);
// FAILED: REQUIRE( sumar(3, 4) == 8 )
// with expansion: 7 == 8
```

**Una sola macro, y el mensaje muestra los dos valores.** Lo consigue con *expression decomposition*:
la macro envuelve la expresión en un objeto cuyo `operator<` de baja precedencia **captura el lado
izquierdo antes de que se evalúe la comparación**, y luego sobrecarga `==` para guardar los dos
operandos.

Es un abuso brillante de la precedencia de operadores, y ahorra tener que escribir `EXPECT_EQ`,
`EXPECT_LT`, `EXPECT_GT` y compañía.

Y sobre la simulación, C++ está en el lado difícil de esta página: **`GoogleMock` solo puede simular
métodos virtuales**, porque no hay forma de interceptar una llamada resuelta en compilación.

De ahí que el diseño para pruebas en C++ obligue a **introducir interfaces donde no harían falta**, con
el coste de despacho dinámico de la clase 112 — o a usar plantillas y **inyectar la dependencia como
parámetro de tipo**, que es gratis en ejecución pero contagia el tipo a todo lo que lo use.

Es un compromiso real y sin solución limpia, y merece conocerlo antes de diseñar.

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

dcl-pi PRUEBA;
  a        int(10) const;
  b        int(10) const;
  esperado int(10) const;
end-pi;

dcl-s res varchar(5);

if a + b = esperado;
  res = 'pasa';
else;
  res = 'falla';
endif;

dsply ('test=' + res);

*inlr = *on;
return;
```

**Lo que esta clase enseña en RPG.** El mundo IBM i comparte con COBOL el punto de partida de esta
página —**la unidad histórica era el programa entero**— y llegó a las pruebas unitarias por una vía
concreta: **los programas de servicio** (clase 086).

Cuando la lógica de negocio pasó de estar dentro de programas monolíticos a estar en **procedimientos
exportados desde un programa de servicio**, se pudo llamar a cada procedimiento por separado. **Y ahí
apareció la unidad.**

```rpgle
// RPGUnit: el marco de referencia
dcl-proc test_suma export;
  dcl-pi *n end-pi;
  aEqual(7 : suma(3 : 4) : 'la suma de 3 y 4');
end-proc;
```

**RPGUnit** descubre las pruebas por convención de nombre —los procedimientos exportados que empiezan
por `test`— leyendo **el objeto programa de servicio**, no el fuente.

Eso es posible porque IBM i guarda metadatos ricos dentro de los objetos (clase 138), y es la misma
razón por la que se puede depurar sin fuente.

Y el ecosistema moderno:

| Herramienta | Qué hace |
|---|---|
| **RPGUnit** | xUnit para RPG y COBOL de IBM i |
| **iRPGUnit** | mantenimiento actual, integrado con RDi |
| **ibmi-bob** | construcción reproducible desde fuentes en el IFS |
| **Code4i** | extensión de VS Code: compilar y probar desde el editor |

Y hay una peculiaridad de las pruebas en esta plataforma que conviene conocer y que la clase 140
retomará: **la base de datos está siempre ahí**.

En IBM i, DB2 es parte del sistema operativo, así que **una prueba puede crear una biblioteca temporal,
copiar tablas, ejecutar y borrar la biblioteca**:

```text
CRTLIB PRUEBA01
CRTDUPOBJ OBJ(CLIENTES) FROMLIB(PROD) OBJTYPE(*FILE) TOLIB(PRUEBA01) DATA(*YES)
CHGLIBL LIBL(PRUEBA01 PROD)        <-- la lista de bibliotecas decide QUÉ tabla se usa
```

**La *lista de bibliotecas* redirige a qué tabla accede el programa sin tocar el programa.** Es
inyección de dependencias a nivel de sistema operativo, y resuelve sin código el problema que en otros
ecosistemas requiere abstracciones de repositorio.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 prueba: procedure options(main);

    declare (a, b, esperado) fixed binary(31);

    get list (a, b, esperado);

    if a + b = esperado then
       put skip list ('test=pasa');
    else
       put skip list ('test=falla');

 end prueba;
```

**Lo que esta clase enseña en PL/I.** PL/I es, con COBOL, el caso donde esta clase tiene que hablar de
lo que hay en lugar de lo que debería haber: **no hay un marco de pruebas unitarias de referencia**.

Y el motivo no es descuido. Es que el software escrito en PL/I es **software de misión crítica de hace
treinta o cuarenta años**, y su régimen de verificación es otro:

- **Revisión formal de código**, por varias personas, documentada.
- **Juegos de datos de prueba** enormes, versionados, con salidas esperadas.
- **Ejecución en paralelo**: el sistema nuevo y el viejo, con los mismos datos, comparando salidas
  durante meses.
- **Y ventanas de cambio muy controladas.**

**La tercera es la más interesante para esta clase** y tiene nombre propio en la industria: *parallel
run*. Es exactamente lo que la clase 140 llamará **verificador de equivalencia**, aplicado a sistemas
enteros y durante meses.

Lo que PL/I sí tiene, y es sustancial, es lo que la Parte 8 mostró: **el lenguaje detecta y diagnostica
mucho por sí solo**.

```pli
 (subscriptrange, stringrange, size, stringsize):
 procesar: procedure;
    ...
 end procesar;
```

**Ese prefijo activa las comprobaciones para todo el procedimiento**, y son las que en otros lenguajes
hay que escribir como pruebas: índices, subcadenas, desbordamiento y truncamiento.

Y con `on` (clase 137), el programa puede **registrar el fallo con todo el contexto y continuar**, lo
que en un lote de horas es la diferencia entre perder el trabajo entero y perder un registro.

Y para probar por partes, PL/I ofrece lo que su modularidad permite:

```pli
 declare calcular entry (fixed binary(31)) returns (fixed binary(31)) external;
```

**Un procedimiento externo se puede compilar y enlazar por separado**, así que se puede escribir un
programa principal de prueba que lo llame — que es exactamente lo que hace el ejemplo de esta página.

Es xUnit sin marco: **un programa que llama, compara y grita**. Y como decía el cierre de la clase, eso
ya es una prueba.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
PRUEBA ; Prueba unitaria -- clase 139
 read linea
 set a = $piece(linea, " ", 1)
 set b = $piece(linea, " ", 2)
 set esperado = $piece(linea, " ", 3)
 write "test=", $select(a + b = esperado : "pasa", 1 : "falla"), !
 quit
```

**Lo que esta clase enseña en M.** M tiene el mismo problema que el resto de esta columna —**pocas
comprobaciones del lenguaje, así que las pruebas cargan con todo**— y una comunidad que construyó su
propia solución alrededor de VistA, el sistema sanitario del Departamento de Veteranos de EE. UU.

El marco de referencia es **MUnit**, y tiene una particularidad que merece explicarse:

```mumps
ZTMSUM ; pruebas de la rutina SUMA
 quit
test1 ; suma basica
 do CHKEQ^%ut(7, $$suma^MIRUT(3, 4), "3+4")
 quit
test2 ; con ceros
 do CHKEQ^%ut(0, $$suma^MIRUT(0, 0), "0+0")
 quit
```

**MUnit descubre las pruebas leyendo el propio fuente con `$text`** (clases 123 y 138): recorre las
líneas de la rutina, encuentra las etiquetas que empiezan por `test`, y las invoca por indirección.

```mumps
 set etiqueta = "test1"
 do @(etiqueta_"^ZTMSUM")        ; llamada indirecta
```

**Eso es reflexión sin sistema de reflexión**, conseguida porque el código es texto en la base de datos
y hay una operación para leerlo y otra para ejecutarlo.

Es la misma solución que Pascal consigue con `published` y RTTI en esta página, y que C++ tiene que
simular con macros y registro estático — obtenida en M **gratis, por el modelo del lenguaje**.

Y hay un aspecto de las pruebas en M que es característico del dominio y merece nombrarse: **los datos
de prueba son *globals*, y por tanto persistentes**.

```mumps
 new $etrap
 set ^||TMP("PACIENTE", 1) = "prueba"     ; ^|| : global TEMPORAL, por proceso
 kill ^||TMP
```

**El prefijo `^||`** declara una global temporal privada del proceso, que desaparece al terminar. Es la
forma idiomática de aislar una prueba en un sistema donde todo lo demás es persistente y compartido, y
resuelve el problema que en otros ecosistemas se resuelve con una base de datos en memoria.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| linea partes a b esperado |

linea := stdin nextLine trimBoth.
partes := linea substrings: ' '.

a := (partes at: 1) asNumber.
b := (partes at: 2) asNumber.
esperado := (partes at: 3) asNumber.

Transcript show: 'test=', (a + b = esperado ifTrue: [ 'pasa' ] ifFalse: [ 'falla' ]); cr.
```

**Lo que esta clase enseña en Smalltalk.** Aquí está el origen: **SUnit, escrito por Kent Beck en
Smalltalk en 1994, es el primer marco de pruebas unitarias de la historia**, y todo lo demás de esta
página desciende de él.

La genealogía es literal: **Kent Beck y Erich Gamma escribieron JUnit en un vuelo de Zúrich a
Washington en 1997, portando SUnit a Java**. De JUnit salieron NUnit, CppUnit, PyUnit, AUnit,
FPCUnit, RPGUnit y prácticamente todos los marcos con "Unit" en el nombre.

Y el diseño original ya tenía las piezas que hoy se dan por supuestas:

```smalltalk
TestCase subclass: #PruebaSuma
    instanceVariableNames: ''

PruebaSuma >> setUp
    calculadora := Calculadora new.

PruebaSuma >> testSumaBasica
    self assert: (calculadora sumar: 3 con: 4) equals: 7.

PruebaSuma >> testDivisionPorCero
    self should: [ calculadora dividir: 1 con: 0 ] raise: ZeroDivide.
```

**`setUp`, `tearDown`, el descubrimiento por prefijo `test`, y la suite** — todo eso es de 1994.

Y el descubrimiento funciona por la vía natural de Smalltalk (clase 108): **`TestCase` pregunta a la
clase por sus selectores y se queda con los que empiezan por `test`**.

```smalltalk
self class selectors select: [ :s | s beginsWith: 'test' ]
```

**Una línea**, sin macros, sin preprocesador y sin atributos — porque **la clase es un objeto al que se
le puede preguntar**.

Y hay dos aportaciones del ecosistema Smalltalk que esta clase debe cerrar:

**Primera, el desarrollo dirigido por pruebas**: TDD se formuló en este entorno, y la razón es
material —**el ciclo rojo-verde-refactor requiere que ejecutar la prueba cueste menos de un segundo**,
y en una imagen viva con compilación incremental (clase 124), cuesta milisegundos.

**Y segunda, el depurador como parte del ciclo** (clase 138): en Smalltalk se puede **escribir la
prueba de un método que aún no existe, ejecutarla, y cuando el depurador se abre en el
`doesNotUnderstand:`, escribir el método ahí mismo y continuar**.

Eso no es una anécdota: **es TDD sin cambiar de ventana**, y es la razón de que la práctica naciera
aquí y no en un lenguaje compilado.

---

## Y de vuelta a la clase

Lo transferible: **una prueba unitaria es una afirmación ejecutable sobre una unidad de código, y su
valor no está en encontrar fallos nuevos sino en detectar los que se reintroducen**. Por eso la
pregunta útil al escribir una no es "¿qué puede fallar?" sino **"¿qué quiero que siga siendo verdad
dentro de cinco años, cuando otro cambie esto?"**. Y por eso el ecosistema importa menos que la
disciplina: un `if` que compara y grita es ya una prueba; lo demás es comodidad.

⏮️ [Volver a la clase 139](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
