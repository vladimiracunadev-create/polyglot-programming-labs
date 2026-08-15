# -*- coding: utf-8 -*-
"""Parte 9, lote A — clases 139 a 142. Ver `vivos_parte9.py` y `gen_vivos.py`."""

SPECS: dict[str, dict] = {}

# ---------------------------------------------------------------------------
# 139 — Pruebas unitarias por lenguaje
# ---------------------------------------------------------------------------
SPECS["139"] = dict(
    gancho="""
Una prueba: `a + b` debería dar `esperado`. El programa es minúsculo a propósito, porque lo que esta
clase compara no es el código: es **qué significa "prueba unitaria" en cada ecosistema**. Y hay
sorpresas de fecha: **el primer marco de pruebas unitarias de la historia se escribió en Smalltalk en
1994**, y de él descienden JUnit, PyTest, RSpec y todos los demás. El resto de esta página lo adoptó
después.
""",
    porque="""
Aquí el concepto es la **prueba automatizada como parte del código fuente**, y estos lenguajes lo
enseñan porque llegaron a ella por caminos opuestos. **Smalltalk la inventó** —SUnit, de Kent Beck—.
**Ada la lleva en el lenguaje** con contratos que se comprueban solos (clase 118). **Fortran y COBOL
vivieron cincuenta años sin marcos de pruebas**, con la comparación de ficheros de salida como método.
Y **Perl trajo TAP**, el formato de salida de pruebas que hoy usan lenguajes que nunca han visto Perl.

Y el eje que las ordena es **qué se considera la unidad**: un método, un procedimiento, un programa
entero o un fichero de salida.
""",
    cierre="""
Lo transferible: **una prueba unitaria es una afirmación ejecutable sobre una unidad de código, y su
valor no está en encontrar fallos nuevos sino en detectar los que se reintroducen**. Por eso la
pregunta útil al escribir una no es "¿qué puede fallar?" sino **"¿qué quiero que siga siendo verdad
dentro de cinco años, cuando otro cambie esto?"**. Y por eso el ecosistema importa menos que la
disciplina: un `if` que compara y grita es ya una prueba; lo demás es comodidad.
""",
    langs={
        "cobol": ("""
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
""", """
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
"""),
        "fortran": ("""
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
""", """
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
"""),
        "ada": ("""
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
""", """
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
"""),
        "pascal": ("""
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
""", """
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
"""),
        "lisp": ("""
(let ((a (read))
      (b (read))
      (esperado (read)))
  (format t "test=~A~%" (if (= (+ a b) esperado) "pasa" "falla")))
""", """
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
"""),
        "tcl": ("""
gets stdin linea
lassign [string trim $linea] a b esperado

puts "test=[expr {$a + $b == $esperado ? {pasa} : {falla}}]"
""", """
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
"""),
        "perl": ("""
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;
my ($a1, $b1, $esperado) = split ' ', $linea;

print "test=", ($a1 + $b1 == $esperado ? 'pasa' : 'falla'), "\\n";
""", """
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
"""),
        "cpp": ("""
#include <iostream>

int main() {
    long long a{}, b{}, esperado{};
    if (!(std::cin >> a >> b >> esperado)) return 1;

    std::cout << "test=" << (a + b == esperado ? "pasa" : "falla") << '\\n';
    return 0;
}
""", """
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
"""),
        "rpg": ("""
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
""", """
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
"""),
        "pli": ("""
 prueba: procedure options(main);

    declare (a, b, esperado) fixed binary(31);

    get list (a, b, esperado);

    if a + b = esperado then
       put skip list ('test=pasa');
    else
       put skip list ('test=falla');

 end prueba;
""", """
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
"""),
        "mumps": ("""
PRUEBA ; Prueba unitaria -- clase 139
 read linea
 set a = $piece(linea, " ", 1)
 set b = $piece(linea, " ", 2)
 set esperado = $piece(linea, " ", 3)
 write "test=", $select(a + b = esperado : "pasa", 1 : "falla"), !
 quit
""", """
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
"""),
        "smalltalk": ("""
| linea partes a b esperado |

linea := stdin nextLine trimBoth.
partes := linea substrings: ' '.

a := (partes at: 1) asNumber.
b := (partes at: 2) asNumber.
esperado := (partes at: 3) asNumber.

Transcript show: 'test=', (a + b = esperado ifTrue: [ 'pasa' ] ifFalse: [ 'falla' ]); cr.
""", """
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
"""),
    },
)

# ---------------------------------------------------------------------------
# 140 — Pruebas de integración y el verificador de equivalencia
# ---------------------------------------------------------------------------
SPECS["140"] = dict(
    gancho="""
Comparar dos resultados y decir si son equivalentes. Es literalmente lo que hace el verificador de este
curso (clase 040) y lo que este programa reproduce en doce lenguajes. Y no es un ejercicio académico:
**la migración de sistemas COBOL a Java lleva treinta años haciendo exactamente esto** — ejecutar los
dos sistemas con los mismos datos durante meses y comparar cada salida, byte a byte, antes de apagar el
viejo.
""",
    porque="""
Aquí el concepto es la **equivalencia observable**: dos implementaciones distintas son intercambiables
si producen la misma salida para las mismas entradas. Y estos lenguajes lo enseñan porque **es su
problema profesional real**. COBOL y PL/I viven en migraciones. RPG convive con Java en la misma
máquina. Fortran valida modelos nuevos contra modelos viejos. Y todos ellos aportan la parte incómoda:
**la equivalencia no es igualdad**, porque hay redondeo, orden y precisión de por medio.

Y aparece la pregunta que atraviesa la clase: **¿qué tolerancia hace falta para que "igual" siga
significando algo?**
""",
    cierre="""
Lo transferible: **una prueba de integración comprueba una frontera; el verificador de equivalencia
comprueba una sustitución**. Y el segundo es la herramienta más valiosa que existe para cambiar algo
grande sin miedo, porque convierte una migración en una operación con red: si el nuevo produce lo mismo
que el viejo para todo lo que ha pasado por el sistema, se puede cambiar. La disciplina que hay que
aprender es **guardar entradas y salidas reales**, porque sin ellas no hay red — y esa decisión hay que
tomarla antes de necesitarla.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. EQUIVAL.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  C-X     PIC X(20).
01  C-Y     PIC X(20).
01  VX      PIC S9(9) COMP.
01  VY      PIC S9(9) COMP.

PROCEDURE DIVISION.
    ACCEPT LINEA
    UNSTRING LINEA DELIMITED BY ALL SPACES
        INTO C-X C-Y
    END-UNSTRING

    COMPUTE VX = FUNCTION NUMVAL(C-X)
    COMPUTE VY = FUNCTION NUMVAL(C-Y)

    IF VX = VY
        DISPLAY "equivalente=true"
    ELSE
        DISPLAY "equivalente=false"
    END-IF
    STOP RUN.
""", """
**Lo que esta clase enseña en COBOL.** Esta es, probablemente, la clase de todo el curso donde COBOL
tiene más que enseñar, porque **la comparación de equivalencia es la técnica central de la modernización
de sistemas**, y COBOL lleva treinta años en el centro de ese problema.

El procedimiento estándar de una migración se llama ***parallel run***, y es este:

1. **Se instrumenta el sistema viejo** para guardar cada entrada y cada salida.
2. **El sistema nuevo se ejecuta con las mismas entradas**, normalmente en paralelo y sin efectos.
3. **Se comparan las salidas**, campo a campo, durante semanas o meses.
4. **Cada diferencia se investiga**: o es un fallo del nuevo, o es un fallo del viejo que llevaba
   veinte años en producción.

**El punto 4 es el que sorprende a quien no ha hecho una migración**: aparecen discrepancias que
resultan ser errores históricos del sistema original **de los que dependen los clientes**. Y entonces
hay que decidir si el sistema nuevo debe **reproducir el error**.

La respuesta, casi siempre, es que sí. Es lo que se llama *bug-for-bug compatibility*.

Y COBOL aporta a esta clase el motivo técnico más frecuente de discrepancia, que es de la clase 072:
**la aritmética decimal**.

```cobol
COMPUTE RESULTADO ROUNDED = A * B / C
```

**COBOL calcula en decimal con `COMP-3` y redondea a la mitad hacia arriba.** Un Java que use `double`
**dará otro resultado en los céntimos**, y en un sistema bancario eso son millones de discrepancias.

La solución conocida es usar `BigDecimal` con el modo de redondeo exacto:

```java
resultado.setScale(2, RoundingMode.HALF_UP)     // el de COBOL por defecto
```

Y la letra pequeña que arruina migraciones: **`ROUNDED` de COBOL admite varios modos** —`ROUNDED MODE
IS NEAREST-EVEN`, `TRUNCATION`, `PROHIBITED`—, y **el que no se declara depende del compilador y de las
opciones de compilación**.

La lección para esta clase, y es dura: **la equivalencia se define, no se supone**. Antes de comparar
hay que decidir **qué campos, con qué tolerancia y con qué regla de redondeo** — y esa decisión es la
mitad del trabajo de una migración.
"""),
        "fortran": ("""
program equival
   implicit none
   integer :: x, y

   read(*, *) x, y

   if (x == y) then
      write(*, '(A)') 'equivalente=true'
   else
      write(*, '(A)') 'equivalente=false'
   end if
end program equival
""", """
**Lo que esta clase enseña en Fortran.** Fortran vive la versión más difícil de esta clase: **comparar
dos programas numéricos que nunca darán exactamente el mismo resultado**.

El motivo es de la clase 073: **la suma en coma flotante no es asociativa**.

```fortran
! Estas tres sumas dan resultados DISTINTOS en el último bit:
s = ((a + b) + c) + d
s = (a + b) + (c + d)
s = a + (b + (c + d))
```

Y eso importa porque **cualquier cambio de compilador, de nivel de optimización, de número de procesos
MPI o de hilos OpenMP cambia el orden de las sumas** — y por tanto el último dígito.

De ahí las técnicas que la comunidad de cálculo científico ha desarrollado y que esta clase debe
recoger:

**Primera, comparar con tolerancia relativa, no absoluta:**

```fortran
error = abs(nuevo - viejo) / max(abs(viejo), tiny(1.0_dp))
if (error > 1.0e-10_dp) then ...
```

**Segunda, comparar magnitudes agregadas y no valores puntuales**: la energía total, la masa
conservada, la norma de la diferencia — porque **una diferencia local puede ser ruido y una diferencia
global es un error**.

**Tercera, forzar la reproducibilidad cuando hace falta:**

```bash
gfortran -ffp-contract=off        # sin fundir multiplicación y suma (FMA)
ifort -fp-model precise            # sin reasociar
export MKL_CBWR=COMPATIBLE          # resultados reproducibles entre CPUs
export OMP_NUM_THREADS=1             # sin reparto variable
```

**`-ffp-contract=off` merece la explicación**: la instrucción FMA calcula `a*b + c` **con un solo
redondeo en vez de dos**, y por tanto **es más precisa y da otro resultado**. El compilador la usa por
defecto si el procesador la tiene, y **por eso el mismo código da distintos números en distintas
máquinas**.

Y **`MKL_CBWR`** —*conditional bitwise reproducibility*— es la respuesta de Intel a este problema:
obliga a la biblioteca a usar el mismo camino de código en cualquier CPU, **a costa de rendimiento**.

Esa es la lección general y transferible: **la reproducibilidad bit a bit es alcanzable y se paga**. Y
la pregunta de ingeniería no es si conseguirla, sino **si el dominio la necesita** — en un modelo
climático probablemente no, en un cálculo de certificación probablemente sí.
"""),
        "ada": ("""
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Equival is
   X, Y : Integer;
begin
   Get (X);
   Get (Y);

   if X = Y then
      Put_Line ("equivalente=true");
   else
      Put_Line ("equivalente=false");
   end if;
end Equival;
""", """
**Lo que esta clase enseña en Ada.** Ada aporta a esta clase una idea que cambia el planteamiento: **si
la equivalencia se puede expresar como un contrato, se puede comprobar en cada llamada real, no solo
en las pruebas**.

```ada
function Nuevo_Calculo (X : Entrada) return Salida
   with Post => Nuevo_Calculo'Result = Viejo_Calculo (X);
```

**Esa postcondición dice literalmente "el nuevo debe dar lo mismo que el viejo"**, y con
`Assertion_Policy (Check)` **se comprueba en producción, en cada llamada, con datos reales** (clase
118).

Es el *parallel run* de COBOL de esta página **expresado en el lenguaje** y ejecutado por el sistema,
en lugar de por un proceso externo que compara ficheros.

Y con SPARK, se puede ir más lejos:

```ada
--  gnatprove intenta DEMOSTRAR que son equivalentes para TODA entrada
```

**Lo que la comparación de salidas hace por muestreo, la demostración lo hace para el dominio
completo.** No siempre es posible —depende de la complejidad de las funciones— pero cuando lo es,
sustituye meses de ejecución en paralelo.

Y Ada tiene un mecanismo que encaja exactamente con esta clase y que merece conocerse: **la
redundancia con votación**, usada en sistemas críticos.

```ada
--  Tres implementaciones independientes del mismo cálculo; se vota
Resultado := Votar (Impl_A (X), Impl_B (X), Impl_C (X));
```

**Programación en N versiones**: se escriben tres implementaciones, idealmente por equipos distintos, y
**el sistema toma el valor en el que coincidan al menos dos**.

Se usó en el Boeing 777 y en el Airbus A320 —con procesadores y compiladores distintos—, y su premisa
es la de esta clase llevada al extremo: **si dos implementaciones independientes coinciden, es muy
improbable que ambas estén mal de la misma manera**.

Su límite también es conocido y merece decirse: **los errores de especificación afectan a las tres
versiones por igual**. Si el requisito estaba mal, las tres implementaciones lo cumplirán mal y votarán
lo mismo.

Es la razón por la que la industria crítica invierte tanto en la especificación y tan poco en el
código: **el verificador de equivalencia no protege de una idea equivocada**.
"""),
        "pascal": ("""
program Equival;
{$MODE OBJFPC}{$H+}

var
  X, Y: Integer;

begin
  Read(X, Y);

  if X = Y then
    WriteLn('equivalente=true')
  else
    WriteLn('equivalente=false');
end.
""", """
**Lo que esta clase enseña en Pascal.** El ecosistema Pascal se encuentra con esta clase por una vía muy
concreta y muy frecuente: **migrar una aplicación Delphi de 32 bits a 64 bits, o de Delphi a Free
Pascal, o de Windows a Linux**.

Y ahí aparece un catálogo de diferencias que ilustra bien lo que la equivalencia tiene de traicionera:

| Diferencia | Consecuencia |
|---|---|
| **`Integer` sigue siendo 32 bits, pero el puntero pasa a 64** | `Integer(punteroCasteado)` trunca |
| **`NativeInt` cambia de tamaño** | los cálculos de desplazamiento cambian |
| **`string` es UTF-16 en Delphi y puede ser UTF-8 en FPC** | `Length` da otro número |
| **`Extended` es de 80 bits en x86 y de 64 en x64** | **el último dígito cambia** |
| **El fin de línea es `#13#10` o `#10`** | la comparación de ficheros falla |

**La cuarta fila es la más insidiosa** y conecta con Fortran de esta página: **Delphi para Windows de
64 bits redefinió `Extended` como `Double`**, así que **un cálculo financiero acumulado da otro
resultado tras migrar**, sin ningún cambio en el código.

Y `string` como UTF-16 frente a UTF-8 (clase 093) es la otra fuente clásica: **`Length(s)` cuenta
unidades de código, no caracteres**, así que un texto con acentos da longitudes distintas en cada
plataforma.

La técnica que el ecosistema usa es la de esta clase, y es sana:

```pascal
{ 1. capturar la salida del sistema actual }
GuardarResultado('caso_' + IntToStr(I) + '.esperado', Calcular(Entrada[I]));

{ 2. tras migrar, comparar }
CheckEquals(CargarEsperado(I), Calcular(Entrada[I]), 'caso ' + IntToStr(I));
```

Y hay una herramienta del mundo Delphi que merece nombrarse porque automatiza justo esto: **el
comparador de bases de datos**, que ejecuta la aplicación vieja y la nueva contra copias de la misma
base y **compara las tablas al terminar**.

Es el *parallel run* de COBOL, aplicado a aplicaciones de escritorio con base de datos — el mismo
patrón, otra escala.
"""),
        "lisp": ("""
(let ((x (read))
      (y (read)))
  (format t "equivalente=~A~%" (if (equal x y) "true" "false")))
""", """
**Lo que esta clase enseña en Common Lisp.** Lisp obliga a hacerse la pregunta que esta clase esconde:
**"equivalente" ¿en qué sentido?** Y lo hace porque **tiene cuatro predicados de igualdad distintos**
(clase 101):

```lisp
(eq   x y)     ; el MISMO objeto: identidad
(eql  x y)      ; eq, o números del mismo tipo y valor, o caracteres iguales
(equal x y)      ; eql, o listas/cadenas iguales elemento a elemento
(equalp x y)      ; equal, ignorando mayúsculas y mezclando tipos numéricos
```

```lisp
(equal  "Hola" "hola")   ; NIL
(equalp "Hola" "hola")    ; T
(equalp 1 1.0)             ; T   ¡un entero y un real!
(equal  1 1.0)              ; NIL
```

**Esas cuatro respuestas distintas a la misma pregunta son el contenido de esta clase**: el verificador
de equivalencia tiene que elegir una, y la elección **es una decisión de diseño con consecuencias**.

¿Es `1` equivalente a `1.0`? En un verificador de resultados numéricos, probablemente sí. En uno de
tipos, desde luego que no.

Y Lisp aporta una técnica que esta clase debe recoger y que la comunidad usa mucho: **la comparación
generativa**.

```lisp
(check-it:check-that
  (check-it:generator (integer))
  (lambda (n) (= (implementacion-vieja n) (implementacion-nueva n))))
```

**Pruebas basadas en propiedades**: en lugar de escribir casos, **se declara la propiedad —"las dos
implementaciones coinciden"— y la biblioteca genera cientos de entradas aleatorias**, incluidos los
casos extremos que nadie escribiría.

Y cuando encuentra un fallo, hace lo más valioso: **reduce la entrada al caso mínimo que lo
reproduce**.

Esa técnica nació en Haskell con QuickCheck (1999) y hoy está en todos los ecosistemas —Hypothesis,
proptest, jqwik—, y **encaja con esta clase mejor que con ninguna otra**: cuando lo que se quiere
comprobar es que dos implementaciones coinciden, **la propiedad se escribe sola**.

Es, con diferencia, la forma más eficiente de verificar una reescritura: no hay que inventar casos,
solo hay que decir qué debe cumplirse.
"""),
        "tcl": ("""
gets stdin linea
lassign [string trim $linea] x y

puts "equivalente=[expr {$x eq $y ? {true} : {false}}]"
""", """
**Lo que esta clase enseña en Tcl.** Tcl expone en una línea la trampa de esta clase, y es la de la
clase 101: **`==` y `eq` no son lo mismo**.

```tcl
expr {"10" == "10.0"}      ;# 1  -- compara como NÚMEROS
expr {"10" eq "10.0"}       ;# 0  -- compara como CADENAS
expr {"1e3" == "1000"}        ;# 1
expr {" 5" == "5"}             ;# 1  -- ¡con espacio!
```

**Un verificador de equivalencia escrito con `==` daría por buena una salida `10.0` donde se esperaba
`10`.** Y a veces eso es lo correcto, y a veces es un fallo grave.

Por eso el ejemplo de esta página usa `eq`: **el contrato del curso es sobre texto exacto** (clase
040), y ahí la comparación de cadenas es la definición correcta.

Y Tcl es especialmente adecuado para el papel de esta clase por una razón práctica: **es el lenguaje de
pegamento por excelencia**, y un verificador de equivalencia es exactamente eso.

```tcl
set esperado [exec ./version_vieja < $entrada]
set obtenido  [exec ./version_nueva < $entrada]

if {$esperado ne $obtenido} {
    puts "DIFIERE en $entrada"
    exec diff [makeTemp $esperado] [makeTemp $obtenido] >@ stdout
}
```

**Cinco líneas y ya hay un verificador de equivalencia entre dos binarios cualesquiera.** Es
literalmente lo que hace el verificador de este curso, y es la razón por la que Tcl se usó durante
décadas en la industria de diseño de circuitos: **automatizar la comparación de salidas de herramientas
distintas**.

Y `tcltest` tiene un mecanismo pensado para esto:

```tcl
customMatch equivalenteNumerico {apply {{esperado obtenido} {
    expr {abs($esperado - $obtenido) < 1e-9}
}}}

test calculo-1.1 {...} -body { calcular } -match equivalenteNumerico -result 3.14159265
```

**`-match` con un comparador propio** permite declarar qué significa "igual" **por prueba**, que es
justo la decisión que Fortran y COBOL de esta página obligan a tomar.
"""),
        "perl": ("""
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;
my ($x, $y) = split ' ', $linea;

print "equivalente=", ($x eq $y ? 'true' : 'false'), "\\n";
""", """
**Lo que esta clase enseña en Perl.** Perl es, históricamente, **la herramienta con la que se han hecho
la mayoría de los verificadores de equivalencia del mundo real**, y por un motivo que esta clase debe
explicar: **es lo que había instalado en todas partes y sabía manejar texto**.

Un verificador completo cabe en muy poco:

```perl
use strict; use warnings;
use Test::More;

for my $caso (glob 'casos/*.in') {
    my $viejo = `./sistema_viejo < $caso`;
    my $nuevo = `./sistema_nuevo < $caso`;
    is($nuevo, $viejo, "equivalencia en $caso");
}
done_testing();
```

**Y con TAP** (clase 139), la salida ya es consumible por cualquier integración continua.

Y Perl distingue —como Tcl de esta página— entre comparar como número y como cadena:

```perl
"10" == "10.0"      # verdadero: numérico
"10" eq "10.0"       # falso: textual
```

Y el ecosistema tiene módulos que resuelven las variantes difíciles de esta clase:

| Módulo | Para qué |
|---|---|
| **Test::Deep** | estructuras con comodines: `num(3.14, 0.01)`, `ignore()` |
| **Text::Diff** | la diferencia legible entre dos salidas |
| **Test::Differences** | `eq_or_diff`: falla mostrando un diff en columnas |
| **Test::Files** | comparar ficheros y árboles completos |

**`Test::Deep` merece el detalle**, porque resuelve el problema real de comparar respuestas que
contienen partes que **deben** cambiar:

```perl
cmp_deeply($respuesta, {
    id        => ignore(),                 # cambia en cada ejecución
    creado_en => re(qr/^\\d{4}-\\d{2}/),      # una fecha, no importa cuál
    total     => num(120.50, 0.01),          # con tolerancia
    items     => bag(@esperados),             # el mismo conjunto, otro orden
});
```

**`ignore()`, `re()`, `num()` con tolerancia y `bag()` para orden indiferente** son exactamente las
cuatro excepciones que aparecen en toda comparación de sistemas reales: identificadores, marcas de
tiempo, redondeo y orden.

Declararlas explícitamente es mejor que filtrarlas con expresiones regulares antes de comparar, porque
**queda escrito qué se está ignorando y por qué** — que es la disciplina que el cierre de esta clase
pide.
"""),
        "cpp": ("""
#include <iostream>
#include <string>

int main() {
    std::string x, y;
    if (!(std::cin >> x >> y)) return 1;

    std::cout << "equivalente=" << (x == y ? "true" : "false") << '\\n';
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** C++ aporta a esta clase el problema más incómodo, y es el de la
Parte 8: **el comportamiento indefinido hace que "equivalente" pueda dejar de tener sentido** (clase
136).

Dos compilaciones del mismo código pueden dar resultados distintos si hay comportamiento indefinido de
por medio, **y ninguna de las dos es "la correcta"**. Un verificador que compara dos versiones puede
estar comparando dos comportamientos igualmente inválidos.

De ahí que en C++ el verificador de equivalencia se combine siempre con los desinfectantes:

```bash
g++ -O0 -fsanitize=address,undefined -o viejo_dbg viejo.cpp
g++ -O2 -o viejo_opt viejo.cpp
# si viejo_dbg y viejo_opt discrepan, el problema NO es la comparación
```

**Comparar el mismo programa consigo mismo con y sin optimización** es el primer paso, y detecta el
comportamiento indefinido antes de que contamine la comparación real.

Y C++ tiene una herramienta específica para esta clase que merece conocerse:

```bash
csmith | tee prog.c        # genera programas C aleatorios SIN comportamiento indefinido
gcc prog.c -o a1; clang prog.c -o a2
./a1; ./a2                  # si difieren, uno de los DOS COMPILADORES tiene un fallo
```

**Csmith** genera programas aleatorios garantizadamente bien definidos y **compara compiladores entre
sí**. Encontró cientos de errores reales en GCC, Clang y otros.

Es el verificador de equivalencia aplicado un nivel más abajo —**a las implementaciones del lenguaje,
no a los programas**— y es la misma idea de esta clase.

Y sobre la comparación numérica, C++20 añadió lo que faltaba:

```cpp
#include <compare>
auto r = a <=> b;                          // orden de tres vías
std::is_eq(r); std::is_lt(r);
// y para coma flotante, lo de siempre:
std::abs(a - b) <= tol * std::max(std::abs(a), std::abs(b));
```

Y la letra pequeña que arruina comparaciones y merece decirse: **`std::partial_ordering::unordered`**.
Con `NaN` de por medio, **`a <=> b` no devuelve ni menor, ni igual, ni mayor**: devuelve "no
comparable" — porque `NaN != NaN`.

Es la formalización, en el sistema de tipos, de algo que Fortran de esta página lleva sufriendo desde
1985: **en coma flotante, la igualdad no es una relación de equivalencia**.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi EQUIVAL;
  x char(20) const;
  y char(20) const;
end-pi;

dcl-s res varchar(5);

if %trim(x) = %trim(y);
  res = 'true';
else;
  res = 'false';
endif;

dsply ('equivalente=' + res);

*inlr = *on;
return;
""", """
**Lo que esta clase enseña en RPG.** IBM i vive esta clase de una forma particular y muy instructiva:
**el sistema viejo y el nuevo conviven en la misma máquina**, y esa convivencia es el modelo de
modernización de la plataforma.

Un mismo trabajo puede llamar a un programa RPG y a una clase Java. Una tabla DB2 la leen los dos. Y
**la lista de bibliotecas decide cuál se ejecuta** (clase 139):

```text
CHGLIBL LIBL(NUEVO VIEJO COMUN)      <-- el nuevo tiene prioridad
CHGLIBL LIBL(VIEJO COMUN)             <-- vuelta atrás inmediata
```

**Ese es el mecanismo de despliegue y de reversión más simple de esta página** (clase 148): cambiar el
orden de una lista.

Y para la comparación, la plataforma da una capacidad que casi ningún sistema tiene de serie: **el
diario de la base de datos**.

```text
STRJRNPF FILE(CLIENTES) JRN(MIJRN) IMAGES(*BOTH)
```

**`IMAGES(*BOTH)` registra la imagen anterior y la posterior de cada cambio de cada fila**, con el
trabajo, el usuario, el programa y la marca de tiempo.

Y eso se consulta con SQL:

```sql
SELECT * FROM TABLE(QSYS2.DISPLAY_JOURNAL('MIBIB', 'MIJRN'))
WHERE JOURNAL_ENTRY_TYPE IN ('UP','PT','DL')
```

**Con el diario, el verificador de equivalencia no compara salidas: compara los cambios que cada
sistema hizo en la base de datos.** Se ejecuta el viejo, se anota el diario; se restaura, se ejecuta el
nuevo, se anota; y se comparan las secuencias de cambios.

Es una forma de equivalencia **más fuerte que comparar salidas**, porque captura los efectos
secundarios además del resultado — que es justo lo que se escapa en una prueba de caja negra.

Y es una idea transferible a cualquier ecosistema con una base de datos que soporte captura de cambios:
**si dos sistemas producen la misma secuencia de cambios, son equivalentes en lo que importa**.
"""),
        "pli": ("""
 equival: procedure options(main);

    declare (x, y) fixed binary(31);

    get list (x, y);

    if x = y then
       put skip list ('equivalente=true');
    else
       put skip list ('equivalente=false');

 end equival;
""", """
**Lo que esta clase enseña en PL/I.** PL/I es el lenguaje donde la palabra *equivalencia* tiene un
significado técnico extra que merece explicarse, porque es una trampa histórica de esta clase.

```pli
 declare 1 registro,
           2 codigo   char(4),
           2 importe  fixed decimal(9,2);

 declare texto char(10) based(addr(registro));   /* la MISMA memoria, otro tipo */
```

**`based` y `defined` permiten que dos declaraciones distintas se refieran a la misma memoria** —lo que
en Fortran es `EQUIVALENCE` y en C es una unión.

Y eso es exactamente lo contrario de lo que esta clase busca: **dos vistas del mismo dato, no dos
implementaciones del mismo cálculo**. Conviene tener clara la diferencia porque el vocabulario colisiona.

Lo que PL/I sí aporta a la clase, y es de peso, es **la razón por la que las migraciones desde PL/I son
tan delicadas: el sistema de conversiones**.

```pli
 declare a fixed decimal(5,2);
 declare b fixed binary(31);
 declare c char(10);

 a = b;        /* binario -> decimal: puede truncar */
 c = a;         /* decimal -> texto: con un formato IMPLÍCITO */
 a = c;          /* texto -> decimal: condición CONVERSION si no es numérico */
```

**Cada una de esas asignaciones tiene reglas de conversión definidas en el estándar, con decenas de
páginas de detalle** — y **un reescritor en otro lenguaje tiene que reproducirlas exactamente**.

Y la más traicionera es la de la primera línea de esta explicación: **`fixed decimal(5,2)` tiene
precisión y escala declaradas**, y **cada operación aritmética calcula la precisión del resultado según
reglas del estándar**:

```text
fixed decimal(5,2) * fixed decimal(3,1)  ->  fixed decimal(9,3)
```

**El tipo del resultado se deduce, y si excede la precisión máxima, se trunca por la izquierda con la
condición `SIZE`.**

Reproducir eso en un lenguaje con `double` es imposible; reproducirlo con `BigDecimal` requiere
**implementar las reglas de precisión de PL/I a mano**.

Es la misma lección que COBOL en esta página, subida de nivel: **la aritmética decimal con precisión
declarada no se migra sola**, y es la razón número uno de discrepancias en las migraciones de sistemas
financieros.
"""),
        "mumps": ("""
EQUIVAL ; Verificador de equivalencia -- clase 140
 read linea
 set x = $piece(linea, " ", 1)
 set y = $piece(linea, " ", 2)
 write "equivalente=", $select(x = y : "true", 1 : "false"), !
 quit
""", """
**Lo que esta clase enseña en M.** M expone la misma trampa que Tcl en esta página, y de forma más
brusca: **`=` en M compara según el contexto, y M convierte agresivamente**.

```mumps
 write ("10" = "10.0")     ; 0  -- comparación de CADENAS, distintas
 write (10 = "10.0")        ; 0  -- también cadenas: M compara texto con =
 write (+"10" = +"10.0")     ; 1  -- el + fuerza interpretación NUMÉRICA
 write ("10abc" + 0)          ; 10 -- ¡convierte el prefijo numérico y descarta el resto!
```

**La cuarta línea es la característica más peligrosa de M para esta clase**: `"10abc" + 0` **da 10 sin
error ninguno**, porque M interpreta el prefijo numérico y descarta lo demás.

Un verificador de equivalencia que compare numéricamente en M **daría por iguales `"10"` y `"10abc"`**.

Por eso el operador correcto para comparar salidas textualmente es `=` sobre cadenas, y el numérico se
fuerza con `+` explícito. Es la misma distinción `eq`/`==` de Tcl y Perl, resuelta con un prefijo en
lugar de con dos operadores.

Y M aporta a esta clase una técnica que su modelo de datos hace natural y que es genuinamente útil:
**comparar dos globals enteras recorriéndolas en orden**.

```mumps
comparar(g1, g2) ;
 new s1, s2, dif
 set (s1, s2) = "", dif = 0
 for  do  quit:(s1 = "") & (s2 = "")
 . set s1 = $order(@g1@(s1))
 . set s2 = $order(@g2@(s2))
 . if s1 '= s2 set dif = dif + 1 quit
 . if s1 '= "", @g1@(s1) '= @g2@(s2) set dif = dif + 1
 quit dif
```

**`$order` recorre los subíndices en orden colativo** (clase 095), así que **dos globals se comparan en
un solo recorrido simultáneo**, sin cargar nada en memoria y sin ordenar.

Es exactamente el algoritmo de `diff` sobre ficheros ordenados, aplicado a la base de datos, y en los
sistemas VistA es la forma habitual de verificar una migración de datos: **recorrer las dos globals a la
vez y contar diferencias**.

Y encaja con la conclusión de RPG en esta página: **cuando el estado vive en la base de datos, la
equivalencia se comprueba sobre el estado, que es más fuerte que comprobarla sobre la salida**.
"""),
        "smalltalk": ("""
| linea partes x y |

linea := stdin nextLine trimBoth.
partes := linea substrings: ' '.

x := partes at: 1.
y := partes at: 2.

Transcript show: 'equivalente=', (x = y ifTrue: [ 'true' ] ifFalse: [ 'false' ]); cr.
""", """
**Lo que esta clase enseña en Smalltalk.** Smalltalk plantea la pregunta de esta clase con la máxima
claridad, porque **la igualdad es un mensaje y por tanto es negociable**:

```smalltalk
a == b       "identidad: ¿el MISMO objeto? -- no se puede redefinir"
a = b         "igualdad: la define CADA CLASE"
```

**`=` es un método ordinario**, y una clase puede definir lo que quiera:

```smalltalk
Medida >> = otra
    ^ (self valorEnMetros - otra valorEnMetros) abs < 0.001

Medida >> hash
    ^ (self valorEnMetros roundTo: 0.001) hash
```

**La tolerancia de equivalencia se declara en el objeto**, y desde ese momento **todo el sistema la
usa**: los conjuntos, los diccionarios, `includes:`, y por supuesto las pruebas.

Es la respuesta más limpia de esta página a la pregunta "¿qué significa igual?", porque **la respuesta
vive junto al dato al que se refiere** en lugar de repetirse en cada comparación.

Y el aviso que va con ella, y que es la regla más citada de la programación orientada a objetos: **si
redefines `=`, tienes que redefinir `hash`**, o los conjuntos y diccionarios se romperán en silencio
(clase 094).

Y Smalltalk aporta a esta clase dos herramientas propias de su modelo:

**Primera, `storeString` como base de la comparación** (clase 105):

```smalltalk
objetoA storeString = objetoB storeString
```

**Compara la representación serializada completa**, incluidos los objetos anidados — que es la
comparación estructural profunda de `is_deeply` de Perl, obtenida gratis.

**Y segunda, la comparación de imágenes**: como el estado del sistema entero es un objeto, se puede
**guardar la imagen antes de una operación, ejecutar las dos implementaciones y comparar el estado
resultante**.

Es el equivalente al diario de IBM i de esta página, conseguido por la vía del modelo de objetos: **si
el estado es inspeccionable, la equivalencia se puede comprobar sobre el estado**.

Y cierra donde empezó esta clase: **el verificador de equivalencia no compara programas, compara lo que
se puede observar de ellos**. Definir qué es observable es la decisión de ingeniería; lo demás es
recorrer y comparar.
"""),
    },
)

# ---------------------------------------------------------------------------
# 141 — Depuradores
# ---------------------------------------------------------------------------
SPECS["141"] = dict(
    gancho="""
Una traza: las sumas acumuladas de 1 a n, unidas por guiones. Es un programa que **se explica a sí
mismo mientras corre**, que es la técnica de depuración más antigua y más usada del mundo. Y esta clase
la pone en su sitio: **`print` no es la alternativa pobre al depurador — es la alternativa correcta
cuando el fallo no se reproduce**, y todos los lenguajes de esta página tienen algo mejor que `print`
para hacerlo.
""",
    porque="""
Aquí el concepto es el **depurador como herramienta y sus límites**, y estos lenguajes lo enseñan
porque cubren los dos extremos. **Ada, C++ y Fortran usan GDB**, el depurador externo que lee símbolos
y controla el proceso. **Lisp, Smalltalk, Tcl y M llevan el depurador dentro**, escrito en el propio
lenguaje. **Perl trae el suyo en el intérprete.** Y **COBOL y RPG tienen depuradores del sistema
operativo**, capaces de entrar en un trabajo ajeno que ya está corriendo.

Y el eje que los separa es el de la clase 138: **si el programa sigue vivo, se dialoga; si no, se hace
arqueología**.
""",
    cierre="""
Lo transferible: **el depurador responde "¿qué está pasando ahora?", y esa no siempre es la pregunta**.
Para un fallo que ocurre una vez de cada mil, o de madrugada, o en la máquina de un cliente, la
pregunta es "¿qué pasó?", y para esa sirven los registros, las trazas y la grabación reversible. La
habilidad que hay que desarrollar no es manejar un depurador: es **decidir rápido de qué tipo es el
fallo**, porque eso determina la herramienta y el 90 % del tiempo que costará.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. TRAZA.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  N       PIC S9(9) COMP.
01  I       PIC S9(9) COMP.
01  ACUM    PIC S9(9) COMP.
01  ED      PIC -(8)9.
01  SALIDA  PIC X(200).
01  POSIC   PIC 9(4) COMP VALUE 1.

PROCEDURE DIVISION.
    ACCEPT LINEA
    COMPUTE N = FUNCTION NUMVAL(LINEA)

    MOVE "traza=" TO SALIDA
    MOVE 7 TO POSIC
    MOVE 0 TO ACUM

    PERFORM VARYING I FROM 1 BY 1 UNTIL I > N
        COMPUTE ACUM = ACUM + I
        MOVE ACUM TO ED
        IF I > 1
            MOVE "-" TO SALIDA(POSIC:1)
            COMPUTE POSIC = POSIC + 1
        END-IF
        STRING FUNCTION TRIM(ED) DELIMITED BY SIZE
            INTO SALIDA WITH POINTER POSIC
        END-STRING
    END-PERFORM

    DISPLAY FUNCTION TRIM(SALIDA)
    STOP RUN.
""", """
**Lo que esta clase enseña en COBOL.** El programa usa `STRING ... WITH POINTER`, que es la forma
idiomática de COBOL de ir concatenando: **`POSIC` avanza sola** conforme se escribe, y es un puntero de
escritura dentro del campo.

Y sobre depuradores, el mundo COBOL tiene dos que merecen conocerse por lo distintos que son de lo
habitual.

**IBM Debug Tool / z/OS Debugger**, el interactivo, con una capacidad que sorprende:

```text
AT ENTRY MIPGM PERFORM
   LIST WS-CLIENTE;
   IF WS-IMPORTE > 10000 THEN GO TO ETIQUETA;
END-PERFORM;
```

**Los puntos de ruptura ejecutan comandos**, incluidos condicionales, listados y **cambios de flujo**.
Es un lenguaje de guion dentro del depurador, y permite instrumentar sin recompilar.

Y hay dos capacidades específicas del mainframe que no tienen equivalente:

**`AT CHANGE`**, que detiene el programa **cuando un campo cambia de valor** — el punto de vigilancia
de datos, resuelto por el sistema:

```text
AT CHANGE WS-SALDO PERFORM LIST WS-SALDO; LIST %LINE; END-PERFORM;
```

**Y CEDF para CICS** (clase 138), que intercepta cada comando de una transacción viva en producción y
**permite modificar los datos antes de que se ejecute**.

Y GnuCOBOL, en el lado libre:

```bash
cobc -x -g -fsource-location prog.cob     # -g: símbolos; y el fuente en el ejecutable
gdb ./prog
```

**`-fsource-location` hace que el ejecutable conserve fichero y línea**, para que un aborto informe de
dónde ocurrió — que es lo que la clase 137 señalaba como la diferencia entre un diagnóstico y un
volcado.

Y merece cerrar con la técnica que sigue siendo la más usada en producción, y que este programa
ilustra: **la traza escrita**. En un lote nocturno **no hay nadie para pulsar "continuar"**, así que lo
que sirve es que el programa deje escrito por dónde pasó.
"""),
        "fortran": ("""
program traza
   implicit none
   integer :: n, i, acum
   character(len=400) :: salida
   character(len=20)  :: pieza

   read(*, *) n

   salida = 'traza='
   acum = 0

   do i = 1, n
      acum = acum + i
      write(pieza, '(I0)') acum
      if (i > 1) salida = trim(salida) // '-'
      salida = trim(salida) // trim(pieza)
   end do

   write(*, '(A)') trim(salida)
end program traza
""", """
**Lo que esta clase enseña en Fortran.** El `write(pieza, '(I0)')` del programa es **escritura interna**
(clase 093): escribir a una cadena en lugar de a un fichero, que es el `sprintf` de Fortran y la forma
idiomática de convertir números a texto.

Y sobre depuración, Fortran tiene una particularidad que define su relación con las herramientas: **el
depurador tiene que entender los arreglos**.

```text
(gdb) print matriz
$1 = (( 1, 2, 3) ( 4, 5, 6))
(gdb) print vector(3:7)          # una SECCIÓN
(gdb) print vector(3)@5           # 5 elementos desde el 3
(gdb) ptype matriz                 # tipo, forma y límites
```

**Un depurador que no sabe imprimir un arreglo multidimensional con sus límites es inútil en Fortran**,
y esa es la razón de que el soporte de GDB para Fortran haya recibido tanto trabajo.

Y hay dos problemas de depuración que son específicos de este lenguaje y que merecen conocerse:

**Primero, los arreglos asumidos y los descriptores.** Un arreglo `dimension(:,:)` pasado a un
procedimiento **no es un puntero: es un descriptor** con la dirección, los límites y los saltos. Si el
depurador no lo interpreta, muestra basura. Es lo mismo que la clase 129 explicaba sobre punteros
gordos.

**Y segundo, la depuración de código paralelo**, que en Fortran es la norma:

```bash
mpirun -np 4 xterm -e gdb ./prog          # cuatro depuradores, uno por proceso
mpirun -np 4 ./prog --wait-for-debugger    # y engancharse con gdb -p
```

**Lanzar un depurador por proceso deja de funcionar pasados unos pocos**, y por eso existen TotalView y
Arm DDT (clase 138), que **agrupan los procesos por comportamiento**.

Y hay una técnica de bajo coste que la comunidad usa mucho y que este programa ilustra:

```fortran
if (mi_rango == 0) write(*, *) 'paso', i, 'residuo', residuo
flush(6)                                     ! ¡IMPORTANTE!
```

**`flush` es la parte crítica**: sin él, la salida está en el búfer y **si el programa aborta, se
pierde justo lo que interesa** — el último mensaje antes del fallo.

Es una lección transferible a cualquier lenguaje: **una traza sin vaciado no sirve para diagnosticar un
aborto**.
"""),
        "ada": ("""
with Ada.Text_IO;           use Ada.Text_IO;
with Ada.Integer_Text_IO;   use Ada.Integer_Text_IO;
with Ada.Strings;
with Ada.Strings.Fixed;
with Ada.Strings.Unbounded; use Ada.Strings.Unbounded;

procedure Traza is
   N, Acum : Integer;
   Salida  : Unbounded_String := To_Unbounded_String ("traza=");
begin
   Get (N);
   Acum := 0;

   for I in 1 .. N loop
      Acum := Acum + I;
      if I > 1 then
         Append (Salida, "-");
      end if;
      Append (Salida,
              Ada.Strings.Fixed.Trim (Integer'Image (Acum), Ada.Strings.Both));
   end loop;

   Put_Line (To_String (Salida));
end Traza;
""", """
**Lo que esta clase enseña en Ada.** El programa usa `Unbounded_String` (clase 093) y `'Image` con
`Trim`, que es la conversión de número a texto idiomática de Ada: **`'Image` de un entero positivo
lleva un espacio delante** —reservado para el signo—, y por eso hay que recortarlo.

Y sobre depuración, Ada tiene la posición coherente con toda su filosofía: **cuando el lenguaje detecta
tanto, el depurador se usa menos** — pero cuando se usa, GDB habla el vocabulario de Ada.

```text
(gdb) print Mi_Registro
$1 = (nombre => "Ana       ", edad => 30, activo => true)
(gdb) print Vector
$2 = (1 => 10, 2 => 20, 3 => 30)
(gdb) print Mi_Enum
$3 = Rojo
(gdb) catch exception Constraint_Error      <-- ¡detener AL LANZARSE!
(gdb) info tasks
(gdb) task 2                                  <-- cambiar de tarea
```

**`catch exception` merece destacarse**: detiene el programa **en el punto donde se lanza la excepción,
antes de que se propague** — con la pila todavía intacta.

Es la diferencia entre ver dónde se capturó y ver dónde se produjo, y en un lenguaje con propagación de
excepciones eso lo es todo.

**Y `info tasks` con `task N`** (clase 138) permite cambiar de tarea y mirar su pila, con el estado en
vocabulario de Ada: *Runnable*, *Waiting on entry call*, *Accept*, *Delay*.

Y la aportación propia de Ada a esta clase es la instrumentación integrada:

```ada
pragma Debug (Poner_Traza ("acum = " & Acum'Image));
```

**`pragma Debug` ejecuta una llamada solo si la compilación tiene `-gnata`.** Es una traza que **no
cuesta nada en producción** y que **el compilador comprueba igualmente** —tipos incluidos— aunque no la
genere.

Es superior a un `#ifdef` de C por eso mismo: **el código de depuración no se pudre**, porque siempre
se compila aunque no se ejecute.

Y `'Image` sobre cualquier tipo (Ada 2022 lo extendió a todos, incluidos registros y arreglos) da una
representación legible sin escribir el formateador:

```ada
Put_Line (Mi_Registro'Image);      --  (NOMBRE => "Ana", EDAD => 30)
```

Es lo que Lisp tiene con `print` y Smalltalk con `printString`, llegado a Ada por la vía de los
atributos.
"""),
        "pascal": ("""
program Traza;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  N, I, Acum: Integer;
  Salida: string;

begin
  Read(N);

  Salida := 'traza=';
  Acum := 0;

  for I := 1 to N do
  begin
    Acum := Acum + I;
    if I > 1 then Salida := Salida + '-';
    Salida := Salida + IntToStr(Acum);
  end;

  WriteLn(Salida);
end.
""", """
**Lo que esta clase enseña en Pascal.** Pascal tiene el mérito histórico de esta clase, ya adelantado en
la clase 138: **Turbo Pascal integró el depurador en el editor en 1987**.

Antes de eso, depurar era **compilar, ejecutar un depurador aparte, y traducir a mano las direcciones
de memoria a nombres de variable**. Turbo Pascal puso F7, F8 y una ventana de vigilancia **en el mismo
programa donde se escribía el código**, en un ordenador de 640 KB.

Ese modelo —editor, compilador y depurador en uno— es el de todos los IDE actuales, y su influencia es
mayor que la del lenguaje.

Hoy, el ecosistema:

```bash
fpc -g -gl -gw3 prog.pas       # símbolos + números de línea + DWARF 3
gdb ./prog
```

Y en Lazarus, todo eso está integrado con puntos de ruptura condicionales, vigilancia y evaluación de
expresiones.

Y hay dos herramientas del ecosistema que resuelven bien el problema de la clase:

**El registro de excepciones con pila**, que es la solución para el fallo que ocurre en la máquina del
cliente:

```pascal
uses SysUtils;

try
  Procesar;
except
  on E: Exception do
    WriteLn(E.ClassName, ': ', E.Message, LineEnding, BackTraceStrFunc(...));
end;
```

**Y `heaptrc`** (clase 138), con `-gh`, que informa al terminar de cada bloque no liberado **con la
pila de dónde se reservó**.

Y una técnica propia del mundo Delphi que merece nombrarse porque anticipa la telemetría moderna:
**madExcept** y **EurekaLog** capturan cualquier excepción no manejada y **componen un informe con la
pila simbolizada, las variables, la versión, el sistema y una captura de pantalla**, listo para
enviar.

Eso resuelve el caso más difícil del cierre de esta clase —**el fallo que ocurre donde no puedes
mirar**— y lo hace por la vía correcta: **no intentando depurar en remoto, sino recogiendo suficiente
contexto para no tener que hacerlo**.
"""),
        "lisp": ("""
(let ((n (read))
      (acum 0)
      (piezas '()))
  (dotimes (i n)
    (incf acum (1+ i))
    (push (format nil "~D" acum) piezas))
  (format t "traza=~{~A~^-~}~%" (nreverse piezas)))
""", """
**Lo que esta clase enseña en Common Lisp.** El programa usa **`~{~A~^-~}`**, una directiva de `format`
que merece explicarse porque es de las más útiles del lenguaje:

- **`~{ ... ~}`** itera sobre una lista.
- **`~A`** imprime el elemento.
- **`~^`** significa **"si no quedan más elementos, sal aquí"**.

**El resultado es "unir con guiones sin guion final"** — el `join` de otros lenguajes, expresado como
directiva de formato. `format` de Common Lisp es un lenguaje completo dentro del lenguaje, con
iteración, condicionales y recursión.

Y sobre depuración, Lisp tiene lo que la clase 138 detalló, y aquí conviene añadir la herramienta más
característica para el problema concreto de esta clase —**seguir la ejecución**:

```lisp
(trace factorial)
(factorial 4)
  0: (FACTORIAL 4)
    1: (FACTORIAL 3)
      2: (FACTORIAL 2)
        3: (FACTORIAL 1)
        3: FACTORIAL returned 1
      2: FACTORIAL returned 2
    1: FACTORIAL returned 6
  0: FACTORIAL returned 24
```

**`trace` da exactamente lo que este programa construye a mano**, y sin tocar el código: **la traza
completa de llamadas con indentación por profundidad y el valor de retorno de cada una**.

Y admite condiciones:

```lisp
(trace factorial :break t)                    ; entrar al depurador en cada llamada
(trace foo :condition (> (car args) 100))      ; solo si el argumento pasa de 100
(trace foo :report :graph)
```

**Poder activar la traza sobre una función ya cargada, con una condición, sin recompilar y sin haberlo
previsto** es la ventaja concreta del modelo de la Parte 8.

Y merece cerrar con `step` y `inspect`:

```lisp
(step (factorial 4))       ; ejecución paso a paso por FORMAS, no por líneas
(inspect *objeto*)          ; inspector interactivo y navegable
(describe 'factorial)        ; su definición, argumentos, documentación y tipo
```

**`step` avanza por formas**, no por líneas de texto, que es lo coherente en un lenguaje donde el
programa es un árbol (clase 123) — y es más preciso que una línea, porque una línea puede contener
varias formas anidadas.
"""),
        "tcl": ("""
gets stdin linea
set n [string trim $linea]

set acum 0
set piezas {}
for {set i 1} {$i <= $n} {incr i} {
    incr acum $i
    lappend piezas $acum
}

puts "traza=[join $piezas -]"
""", """
**Lo que esta clase enseña en Tcl.** `join $piezas -` resuelve en un comando lo que otros lenguajes de
esta página construyen a mano, y es coherente con la clase 090: **en Tcl toda lista sabe unirse**.

Y sobre depuración, Tcl tiene el mecanismo más elegante de esta página para el problema concreto de la
clase, y ya apareció en la clase 138: **`trace add execution`**.

```tcl
proc calcular {n} { ... }

trace add execution calcular enter {apply {{cmd op} {
    puts "-> $cmd"
}}}
trace add execution calcular leave {apply {{cmd code res op} {
    puts "<- $res"
}}}
```

**Eso produce la traza de llamadas de `trace` de Lisp**, con dos comandos y sin tocar el procedimiento.

Y **`enterstep`** va más allá que cualquier otro lenguaje de esta página:

```tcl
trace add execution calcular enterstep {apply {{cmd op} { puts "  $cmd" }}}
```

**Imprime CADA comando que se ejecuta dentro del procedimiento**, con sus argumentos ya sustituidos. Es
un `set -x` de shell aplicado a un procedimiento concreto, activable en marcha.

Y para el problema clásico —**"¿quién cambió esta variable?"**—:

```tcl
trace add variable ::config write {apply {{n1 n2 op} {
    puts "config cambió a $::config desde [info level -1]"
}}}
```

**`info level -1` da la llamada del llamante**, así que el mensaje dice **quién** hizo el cambio, no
solo que se hizo.

Eso responde en tres líneas a lo que en C++ requiere un punto de vigilancia de hardware (clase 138) y
en la mayoría de los lenguajes no tiene respuesta directa.

Y el ecosistema completa el cuadro:

| Herramienta | Qué hace |
|---|---|
| **TclDebugger** | depurador gráfico con puntos de ruptura |
| **tclsh + `-errorinfo`** | la pila con el texto de cada comando (clase 137) |
| **nagelfar** | análisis estático |
| **`coroprobe`** (8.7) | inspeccionar una corrutina suspendida |
| **tkcon** | consola interactiva sobre una aplicación en marcha |

**tkcon** merece la mención final: **se puede inyectar en una aplicación Tk en ejecución** y da una
consola sobre ella, con acceso a todas sus variables y procedimientos.

Es el `swank` de Lisp de la clase 138: **una puerta al programa vivo**.
"""),
        "perl": ("""
use strict;
use warnings;

my $n = <STDIN>;
chomp $n;

my ($acum, @piezas) = (0);
for my $i (1 .. $n) {
    $acum += $i;
    push @piezas, $acum;
}

print "traza=", join('-', @piezas), "\\n";
""", """
**Lo que esta clase enseña en Perl.** Perl trae **un depurador completo en el intérprete**, sin instalar
nada y en cualquier máquina donde haya Perl — que durante veinte años fue todas.

```bash
perl -d prog.pl
```

Los comandos que conviene conocer:

```text
n / s          siguiente línea / entrar en la función
c 42            continuar hasta la línea 42
b 15 $x > 100    punto de ruptura CONDICIONAL
w $variable       vigilar: parar cuando cambie
x $estructura      volcar una estructura anidada
T                   la pila
r                    ejecutar hasta salir de la función
R                     reiniciar
|m $objeto             los métodos disponibles, paginados
```

**`x` es el comando central**, y hace lo que `Data::Dumper` pero interactivamente y con profundidad
controlable: `x 2 $estructura` limita a dos niveles.

Y el depurador de Perl tiene una propiedad poco conocida que ilustra bien la filosofía del lenguaje:
**está escrito en Perl**, en el fichero `perl5db.pl`, y **se puede sustituir por otro**.

De ahí toda la familia `Devel::`:

```bash
perl -d:NYTProf prog.pl      # el perfilador de referencia
perl -d:Trace prog.pl         # traza de cada línea ejecutada
perl -d:ptkdb prog.pl          # depurador gráfico en Tk
```

**Todos usan el mismo gancho**: `-d:Foo` carga `Devel::Foo` como depurador, y el intérprete le entrega
el control en cada sentencia.

Es una arquitectura de complementos para la depuración, y es la razón de que Perl tenga un perfilador
tan bueno sin que el intérprete tenga que soportarlo específicamente.

Y para el caso del cierre de esta clase —**el fallo que no se puede depurar en vivo**—:

```perl
use Carp;
$SIG{__DIE__} = sub { Carp::confess(@_) };     # cualquier muerte, CON pila
$SIG{ALRM}   = sub { Carp::cluck("colgado") }; # y un aviso con pila si se cuelga
alarm 30;
```

**Convertir toda muerte en una muerte con pila completa** es una línea, y es lo primero que conviene
poner en un programa que va a correr sin supervisión.
"""),
        "cpp": ("""
#include <iostream>
#include <string>

int main() {
    long long n{};
    if (!(std::cin >> n)) return 1;

    std::string salida = "traza=";
    long long acum = 0;

    for (long long i = 1; i <= n; ++i) {
        acum += i;
        if (i > 1) salida += '-';
        salida += std::to_string(acum);
    }

    std::cout << salida << '\\n';
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** C++ tiene el depurador más potente de esta página y el más
laborioso de usar, y esta clase es el sitio para las técnicas que de verdad rinden.

**Puntos de ruptura condicionales y con acción**, para no parar mil veces:

```text
(gdb) break procesar if id == 4711
(gdb) break archivo.cpp:42
(gdb) commands
> print estado
> continue
> end
```

**Ese `commands` con `continue` es un `printf` sin recompilar**: imprime y sigue, tantas veces como
haga falta, sobre un binario que ya existe.

**Puntos de vigilancia de hardware**, para "¿quién escribió aquí?":

```text
(gdb) watch *ptr
(gdb) rwatch variable       # cuando se LEE
(gdb) awatch variable        # lectura o escritura
```

El procesador tiene registros de depuración —cuatro en x86— que **detienen la ejecución en el acceso**,
sin coste. Es la respuesta a la corrupción de memoria, y es lo que Tcl hace con `trace add variable`
por software.

**La pila y los marcos**:

```text
(gdb) bt              # la pila
(gdb) frame 3          # subir al marco 3
(gdb) info locals       # sus variables (clase 127)
(gdb) finish             # ejecutar hasta volver
```

**Impresión bonita de la biblioteca estándar**, que hay que activar y que cambia la experiencia:

```text
(gdb) print v
$1 = std::vector of length 3, capacity 4 = {10, 20, 30}
```

Sin los *pretty printers* de GCC, eso se ve como tres punteros. **Es lo primero que hay que comprobar
al montar un entorno de C++.**

Y **rr**, que merece cerrar porque cambia lo que se puede preguntar:

```bash
rr record ./prog
rr replay
(gdb) watch -l saldo
(gdb) reverse-continue      # hacia ATRÁS hasta la última escritura
```

**Grabar una ejecución y recorrerla hacia atrás desde el fallo hasta la causa.** Con carreras
incluidas, porque `rr` serializa los hilos y **reproduce exactamente la misma intercalación**.

Es la respuesta más directa al cierre de esta clase: **convierte un fallo intermitente en un fallo
determinista**, y a partir de ahí es un problema normal.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi TRAZA;
  n int(10) const;
end-pi;

dcl-s i     int(10);
dcl-s acum  int(10);
dcl-s salida varchar(200);

salida = 'traza=';
acum = 0;

for i = 1 to n;
  acum += i;
  if i > 1;
    salida += '-';
  endif;
  salida += %char(acum);
endfor;

dsply salida;

*inlr = *on;
return;
""", """
**Lo que esta clase enseña en RPG.** IBM i tiene, para esta clase, una capacidad que ningún otro sistema
de esta página iguala: **se puede depurar un trabajo ajeno que ya está corriendo, sin haberlo previsto**
(clase 138).

```text
STRSRVJOB JOB(123456/USUARIO/OTROTRABAJO)     <-- "servir" otro trabajo
STRDBG PGM(MIBIB/MIPGM) UPDPROD(*YES)
BREAK 42                                        <-- punto de ruptura
```

**Ese trabajo puede ser una sesión de un usuario que está reportando un problema en ese momento, o un
lote nocturno a mitad de proceso.** No hay que reiniciarlo, ni configurarlo, ni compilarlo distinto.

Y funciona sin tener el fuente en la máquina, porque **la vista de depuración se guarda dentro del
objeto programa**:

```text
CRTBNDRPG PGM(MIPGM) DBGVIEW(*ALL)
```

`DBGVIEW(*SOURCE)` guarda el fuente original; `*LIST` guarda el listado con las copias expandidas;
`*ALL`, todo. **El objeto lleva su propio código dentro**, y por eso se puede depurar un programa de
hace quince años cuyo fuente se perdió.

Es una decisión de diseño de plataforma que resuelve el problema más frecuente del mantenimiento de
legado, y merece pensarse: **el ejecutable como contenedor de su propia información de depuración** es
lo que hoy hacen los formatos con símbolos embebidos, y aquí es de 1988.

Y el resto del arsenal:

| Herramienta | Qué hace |
|---|---|
| **`STRDBG` / `STRISDB`** | depurador de sistema, con `EVAL`, `WATCH` y `STEP` |
| **`WATCH`** | punto de vigilancia sobre una variable o dirección |
| **`DSPJOBLOG`** | el registro completo con pila (clase 138) |
| **`QSYS2.STACK_INFO`** | la pila de cualquier trabajo, **por SQL** |
| **RDi / Code4i** | depuración gráfica desde Eclipse o VS Code |
| **`dsply`** | el `print` de RPG, que este programa usa |

Y merece cerrar señalando lo que esto significa para el cierre de la clase: **en IBM i la distinción
entre "depurar en vivo" y "hacer arqueología" casi desaparece**, porque el trabajo sigue vivo y el
registro conserva la historia.

Es la excepción de esta página, y viene de una decisión de plataforma, no de lenguaje.
"""),
        "pli": ("""
 traza: procedure options(main);

    declare n         fixed binary(31);
    declare i         fixed binary(31);
    declare acum      fixed binary(31) initial(0);
    declare salida    char(200) varying initial('traza=');

    get list (n);

    do i = 1 to n;
       acum = acum + i;
       if i > 1 then
          salida = salida || '-';
       salida = salida || trim(char(acum));
    end;

    put skip list (salida);

 end traza;
""", """
**Lo que esta clase enseña en PL/I.** PL/I trae la instrumentación **en el lenguaje**, con un mecanismo
que ningún otro de esta página tiene igual: **las condiciones de depuración `CHECK` y `SUBSCRIPTRANGE`
activadas por prefijo**.

```pli
 (check(acum, i)):
 calcular: procedure;
    ...
 end calcular;

 on check(acum) put skip list ('acum ahora vale', acum);
```

**`CHECK` dispara un manejador cada vez que una variable cambia de valor.** Es el punto de vigilancia de
datos —el `watch` de GDB, el `AT CHANGE` de COBOL, el `trace add variable` de Tcl— **integrado en el
lenguaje y activable por ámbito con un prefijo**.

Y como es una condición normal, el manejador es código PL/I: puede imprimir, contar, comparar o abortar.

Es de 1964, y es una idea que la mayoría de los lenguajes modernos delegan por completo en herramientas
externas.

El resto del repertorio de esta clase:

```pli
 put data;                        /* volcar TODAS las variables (clase 138) */
 on error snap put data;           /* al fallar: pila + volcado */
 put skip list ('en ' || onloc()); /* dónde estamos */
```

**`snap` imprime la traza de la pila**, y `onloc()` da el nombre del procedimiento donde ocurrió la
condición.

Y para depuración interactiva, el mundo z/OS usa el mismo **z/OS Debugger** que COBOL en esta página,
con las mismas capacidades: puntos de ruptura con guion, `AT CHANGE` y depuración de programas en
ejecución.

Y merece cerrar con la observación que atraviesa la columna de la izquierda de esta página: **COBOL,
PL/I y Fortran resolvieron la depuración con instrumentación declarada en el propio programa**, porque
en su época **no había una consola donde sentarse a mirar**.

La consecuencia es que su instrumentación **sobrevive al despliegue**: está en el código, se activa con
una opción de compilación, y funciona igual en producción que en desarrollo.

Es exactamente lo que la observabilidad moderna redescubrió cincuenta años después, y que la clase 142
desarrolla.
"""),
        "mumps": ("""
TRAZA ; Traza acumulada -- clase 141
 read n
 new i, acum, salida
 set acum = 0, salida = "traza="
 for i = 1:1:n do
 . set acum = acum + i
 . if i > 1 set salida = salida _ "-"
 . set salida = salida _ acum
 write salida, !
 quit
""", """
**Lo que esta clase enseña en M.** El programa usa `_` para concatenar —el operador de concatenación de
M— y el bucle `for i = 1:1:n` con el punto de anidamiento, que son los idiomas del lenguaje (clases 083
y 090).

Y sobre depuración, M tiene la propiedad que la clase 138 detalló y que aquí conviene aplicar al
problema concreto de esta clase: **el código es texto accesible en ejecución**, así que **una traza
puede imprimir el propio código**.

```mumps
 set $etrap = "do TRAZA^ERRLOG"
 ...
TRAZA ;
 new i
 for i = $stack(-1):-1:1 do
 . write $stack(i, "PLACE"), "  ", $stack(i, "MCODE"), !
 quit
```

**Ese bucle imprime la pila con el código fuente de cada nivel**, sin depurador, sin símbolos y sin
haber compilado de forma especial.

Y el depurador interactivo del entorno, con las extensiones `$Z`:

```mumps
 zbreak procesar^MIRUT             ; punto de ruptura
 zbreak procesar^MIRUT:"n>100"      ; condicional
 zstep into / zstep over / zstep outof
 zshow "V"                            ; todas las variables locales
 zshow "S"                             ; la pila
 zwrite                                  ; volcado del espacio de variables
```

**`zwrite` sin argumentos vuelca todas las variables locales con todos sus subíndices**, que en M —donde
una variable local puede ser un árbol entero (clase 099)— es mucha información en un comando.

Y merece cerrar con la capacidad que se deriva del modelo de datos y que resuelve el caso difícil del
cierre de la clase:

```mumps
 set ^LOG($job, $horolog, $increment(^LOG("N"))) = "paso " _ i _ " acum " _ acum
```

**Escribir la traza a una global es escribirla a la base de datos**: es persistente, transaccional,
indexada por trabajo y por tiempo, **y consultable desde otro proceso mientras el programa sigue
corriendo**.

Eso es exactamente lo que un sistema de registro estructurado moderno hace con mucha más maquinaria, y
en M **es una asignación**.

Es la ventaja de tener la base de datos dentro del lenguaje, y la clase 142 la retoma.
"""),
        "smalltalk": ("""
| n acum piezas |

n := stdin nextLine trimBoth asNumber.

acum := 0.
piezas := OrderedCollection new.

1 to: n do: [ :i |
    acum := acum + i.
    piezas add: acum printString ].

Transcript show: 'traza=', (piezas inject: '' into: [ :a :b |
    a isEmpty ifTrue: [ b ] ifFalse: [ a, '-', b ] ]); cr.
""", """
**Lo que esta clase enseña en Smalltalk.** El programa une con `inject:into:` —el pliegue de la clase
115— porque en Smalltalk incluso unir cadenas es un mensaje sobre una colección.

Y sobre depuración, aquí está el extremo de esta página y lo que la clase 138 ya adelantó: **el
depurador de Smalltalk no controla un proceso desde fuera; ES parte del sistema, escrito en Smalltalk,
y opera sobre objetos vivos**.

Las consecuencias que importan para esta clase:

**Primera, `halt` en cualquier sitio, sin recompilar el mundo:**

```smalltalk
Calculadora >> sumar: a con: b
    self halt.               "abre el depurador AQUÍ"
    ^ a + b
```

Aceptar ese método recompila solo ese método (clase 124), en milisegundos, con el sistema corriendo.

**Segunda, el depurador se puede abrir sin que haya error:**

```smalltalk
[ self calcular ] fork.                       "en otro proceso"
Processor activeProcess suspend.               "y mirarlo"
thisContext                                     "el marco actual como OBJETO"
```

**Tercera, y es la que no tiene equivalente: se puede modificar el programa y continuar.** Escribir el
método que falta, corregir el que está mal, cambiar el valor de una variable, **volver a un marco
anterior de la pila y reejecutar desde ahí**.

```text
[Proceed] [Restart] [Into] [Over] [Through] [Full Stack] [Where is?]
```

**`Restart` reinicia el marco seleccionado** — no el programa: **ese marco**, con el método ya
corregido.

Y cuarta, para el caso difícil del cierre de esta clase: **la depuración remota**. Como el depurador es
un objeto y la pila es un objeto, **se pueden serializar y enviar**:

```smalltalk
"En producción: capturar el contexto del error y mandarlo"
[ self procesar ] on: Error do: [ :e |
    self enviarInforme: e signalerContext copy ]
```

**Lo que viaja no es un texto con la pila: es la pila**, con sus objetos, y se puede **abrir en el
depurador en la máquina del desarrollador**.

Es la conclusión de esta clase llevada al límite: **cuando todo es un objeto, el estado de un fallo es
un dato que se puede guardar, enviar y volver a examinar** — y la distinción entre depurar en vivo y
hacer arqueología deja de existir.
"""),
    },
)

# ---------------------------------------------------------------------------
# 142 — Registro (logging) y observabilidad
# ---------------------------------------------------------------------------
SPECS["142"] = dict(
    gancho="""
Una línea de registro con su nivel y su dato: `[INFO] procesados=5`. Es el programa más humilde de la
parte y el que más se parece a lo que hay en producción. Y esta clase existe porque **el registro es lo
único que queda cuando el fallo ya pasó**: el depurador de la clase 141 exige que el problema esté
ocurriendo ahora, y **la mayoría no lo está**. Aquí hay además un caso que sorprende: **IBM i registra
todo eso sin que nadie lo pida**.
""",
    porque="""
Aquí el concepto es la **observabilidad**: dejar suficiente rastro para reconstruir lo que pasó sin
estar delante. Y estos lenguajes lo enseñan porque **llevan décadas operando sin nadie mirando** —lotes
nocturnos, sistemas embarcados, hospitales, cajeros—, así que su cultura de registro es anterior al
término y en algunos casos mejor que la actual.

Y aparece la tensión central de la clase: **cuanto más se registra, más cuesta y más ruido hay**. Cada
lenguaje de esta página resuelve el equilibrio de una manera distinta, y todas siguen vigentes.
""",
    cierre="""
Lo transferible: **un registro es un mensaje al futuro, y el futuro no tendrá tu contexto**. De ahí las
tres reglas que atraviesan toda la página: registrar **datos, no prosa** —para poder buscar y agregar—;
incluir siempre **un identificador que permita unir las líneas de una misma operación**; y elegir el
nivel pensando en **quién lee y qué decidirá**. Y la regla que más caro sale ignorar: **nunca registrar
datos personales o credenciales**, porque un registro se copia, se envía y se conserva mucho más tiempo
que la base de datos que sí está protegida.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. REGISTRO.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA  PIC X(80).
01  N      PIC S9(9) COMP.
01  ED-N   PIC -(8)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    COMPUTE N = FUNCTION NUMVAL(LINEA)

    MOVE N TO ED-N
    DISPLAY "log=[INFO] procesados=" FUNCTION TRIM(ED-N)
    STOP RUN.
""", """
**Lo que esta clase enseña en COBOL.** El mundo COBOL lleva sesenta años haciendo lo que hoy se llama
observabilidad, con otro nombre y con una diferencia importante: **el registro no era un fichero de
texto, era un fichero con estructura**.

```cobol
       01  REG-LOG.
           05  LOG-TIMESTAMP   PIC X(26).
           05  LOG-NIVEL       PIC X(5).
           05  LOG-PROGRAMA    PIC X(8).
           05  LOG-TRANSACCION PIC X(16).
           05  LOG-USUARIO     PIC X(10).
           05  LOG-CODIGO      PIC 9(4).
           05  LOG-TEXTO       PIC X(120).
```

**Ese registro de longitud fija, con campos declarados, es un registro estructurado** — la idea que la
industria redescubrió con JSON treinta años después.

Y tiene una ventaja que el JSON no tiene: **se puede leer con un programa COBOL, ordenar con `SORT` y
consultar sin analizar nada**, porque cada campo está en una posición conocida.

Y hay una capacidad del mainframe que merece ser el centro de esta explicación, porque es la mejor
respuesta de esta página al problema de correlacionar: **SMF, el *System Management Facility***.

**Cada trabajo, cada transacción CICS, cada llamada a DB2 y cada operación de fichero escribe un
registro SMF automáticamente**, con:

- **CPU consumida**, en milisegundos, por paso y por transacción.
- **Operaciones de entrada y salida**, contadas.
- **Memoria usada.**
- **Tiempo de respuesta**, desglosado.
- **Usuario, terminal, programa y hora.**

Sin instrumentar nada. **Es exactamente lo que hoy se llama telemetría, y lleva funcionando desde
1966.**

Y sobre eso se construyó lo que hoy llamaríamos facturación por uso: **el *chargeback*** — cobrar a cada
departamento por los recursos que consumió, calculado desde los registros SMF.

Y en CICS, la correlación tiene nombre: **la *task number* y el *unit of work ID*** identifican una
transacción a través de todos sus componentes —programa, base de datos, colas—, que es exactamente lo
que un identificador de traza distribuida hace hoy.

La lección de esta clase es incómoda para el discurso de la modernidad: **la observabilidad no se
inventó en la última década; se inventó cuando el tiempo de máquina costaba dinero y había que
justificarlo.**
"""),
        "fortran": ("""
program registro
   implicit none
   integer :: n

   read(*, *) n

   write(*, '(A,I0)') 'log=[INFO] procesados=', n
end program registro
""", """
**Lo que esta clase enseña en Fortran.** El registro en cálculo científico tiene un problema propio que
esta clase debe explicar, y no es el habitual: **hay miles de procesos escribiendo a la vez**.

```fortran
! 10.000 procesos MPI escribiendo a stdout: ilegible y lentísimo
write(*, *) 'paso', paso, 'residuo', residuo
```

Las técnicas que la comunidad usa:

**Primera, escribir solo desde el proceso maestro:**

```fortran
if (mi_rango == 0) write(*, '(A,I0,A,ES12.5)') 'paso ', paso, ' residuo ', residuo
```

**Segunda, un fichero por proceso**, cuando hace falta el detalle:

```fortran
write(nombre, '(A,I5.5,A)') 'log_', mi_rango, '.txt'
open(newunit=u, file=nombre, status='replace')
```

**Y tercera, y es la crítica: `flush`.**

```fortran
write(u, '(A)') mensaje
flush(u)
```

**Sin `flush`, el mensaje se queda en el búfer** y **si el programa aborta se pierde exactamente lo que
interesa** (clase 141). En un cálculo de ocho horas que revienta a la séptima, esa línea es la
diferencia entre saber dónde falló y no saberlo.

Y el coste hay que decirlo: **`flush` en cada línea con 10.000 procesos satura el sistema de ficheros
paralelo**. El compromiso habitual es **vaciar en los mensajes de nivel alto y no en los de traza**.

Y Fortran tiene una particularidad de formato que ayuda mucho y merece nombrarse:

```fortran
write(*, '(A,I0,A,ES12.5,A,F6.2,A)') 'paso=', p, ' residuo=', r, ' t=', t, 's'
```

**`ES12.5` es notación científica normalizada** —una cifra antes del punto— y **`I0` es el ancho
mínimo**. Con eso, **las líneas salen alineadas y son analizables por columnas**, que es lo que
permite graficar la convergencia con un guion de tres líneas.

Y es una observación transferible: **el formato del registro determina si se puede analizar**. Un
registro que hay que leer con expresiones regulares complejas es un registro mal diseñado, y ese es el
argumento a favor del registro estructurado que atraviesa esta clase.
"""),
        "ada": ("""
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Registro is
   N : Integer;
begin
   Get (N);

   Put ("log=[INFO] procesados=");
   Put (N, Width => 1);
   New_Line;
end Registro;
""", """
**Lo que esta clase enseña en Ada.** Ada aborda el registro desde su dominio: **sistemas embarcados y
críticos, donde escribir a un fichero puede no ser una opción** — no hay disco, no hay sistema de
ficheros, o el tiempo de escritura no es acotado.

De ahí soluciones que merecen conocerse porque son transferibles a cualquier sistema con restricciones
de tiempo real:

**Un búfer circular en memoria**, que se vuelca solo si hace falta:

```ada
protected Bitacora is
   procedure Anotar (Codigo : Evento; Valor : Integer);
   procedure Volcar;
private
   Buffer : array (0 .. 1023) of Registro;
   Indice : Natural := 0;
end Bitacora;
```

**El objeto protegido garantiza el acceso seguro entre tareas** (clase 135) **con un tiempo máximo
acotado**, que es el requisito duro: un registro que puede bloquear indefinidamente no es aceptable en
un sistema de tiempo real.

**Y códigos numéricos en lugar de texto**:

```ada
type Evento is (Arranque, Lectura_Sensor, Fuera_De_Rango, Parada);
Bitacora.Anotar (Fuera_De_Rango, Valor);
```

**Registrar un enumerado y un número ocupa unos pocos bytes y no requiere formatear nada.** El texto se
compone después, en tierra, con la tabla de códigos.

Es la técnica de las cajas negras de aviación y de las sondas espaciales, y la razón es doble: **espacio
y determinismo**.

Y el ecosistema de Ada añade:

| Herramienta | Qué hace |
|---|---|
| **GNATCOLL.Traces** | registro con canales activables por fichero de configuración |
| **Ada.Exceptions** | nombre, mensaje e información con traza (clase 138) |
| **`'Image`** | representación textual de cualquier tipo, sin escribir formateadores |
| **`pragma Debug`** | instrumentación que desaparece sin `-gnata` (clase 141) |

**GNATCOLL.Traces merece el detalle** porque implementa bien la idea central de la clase:

```text
# fichero de configuración, leído al arrancar
+
SQL=yes
CACHE=no
NETWORK=yes:file:/tmp/red.log
```

**Los canales se activan sin recompilar y sin reiniciar**, y cada uno puede ir a un destino distinto.
Es el mismo modelo que los registradores por categoría de cualquier marco moderno, y encaja con la
regla de esta clase: **la decisión de qué registrar debe poder tomarse después de desplegar**.
"""),
        "pascal": ("""
program Registro;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  N: Integer;

begin
  Read(N);

  WriteLn('log=[INFO] procesados=', IntToStr(N));
end.
""", """
**Lo que esta clase enseña en Pascal.** El ecosistema Pascal resolvió el registro por la vía de sus
aplicaciones típicas: **software de escritorio instalado en máquinas ajenas**, donde el registro es
literalmente la única información que llegará.

Free Pascal trae la unidad en la distribución:

```pascal
uses EventLog;

var Log: TEventLog;
begin
  Log := TEventLog.Create(nil);
  Log.LogType := ltFile;          { o ltSystem: ¡el registro del SISTEMA! }
  Log.FileName := 'app.log';
  Log.Active := True;

  Log.Info('procesados=%d', [N]);
  Log.Warning('reintento %d', [Intento]);
  Log.Error('fallo: %s', [E.Message]);
end;
```

**`ltSystem` es lo interesante**: escribe **al registro de eventos de Windows o a syslog en Unix**, con
la misma llamada. La unidad abstrae la diferencia, y el mensaje aparece donde los administradores ya
miran.

Es un principio que conviene extraer: **el mejor sitio para un registro suele ser donde ya se está
mirando**, no un fichero nuevo que nadie sabe que existe.

Y el ecosistema añade:

| Herramienta | Qué hace |
|---|---|
| **`EventLog`** | en la distribución; fichero, syslog o registro de Windows |
| **`log4delphi` / `TLoggerPro`** | niveles, destinos múltiples, formato configurable |
| **madExcept / EurekaLog** | informe completo de excepción no manejada (clase 141) |
| **`heaptrc`** | fugas, con la pila de cada reserva (clase 138) |

Y una técnica del mundo Delphi que anticipa la telemetría moderna y merece cerrarse aquí: **el informe
automático de fallos**.

Cuando una aplicación instalada en miles de escritorios falla, **madExcept compone un informe con la
pila simbolizada, el sistema, la versión, las variables y una captura**, y **ofrece al usuario
enviarlo**.

Y el detalle que lo hace funcionar y que conecta con la clase 144: **los símbolos de depuración se
guardan aparte y se distribuyen sin ellos**, así que el informe llega con direcciones y **se simboliza
en el lado del desarrollador**.

Eso es exactamente lo que hoy hacen los ficheros de símbolos y los mapas de fuentes, y por la misma
razón: **el binario que se distribuye no debe llevar la información que hace falta para depurarlo**.
"""),
        "lisp": ("""
(let ((n (read)))
  (format t "log=[INFO] procesados=~D~%" n))
""", """
**Lo que esta clase enseña en Common Lisp.** Lisp aporta a esta clase algo que su modelo hace natural y
que la mayoría de los lenguajes necesitan mucha maquinaria para conseguir: **el registro puede ser un
objeto, no una cadena**.

```lisp
(log:info "procesados=~D" n)              ; texto, como todos
(log-evento (list :nivel :info :procesados n :duracion-ms 42))   ; DATOS
```

Y la segunda forma tiene una propiedad decisiva: **la salida se puede volver a leer**.

```lisp
(with-open-file (f "app.log" :direction :output :if-exists :append)
  (print (list :ts (get-universal-time) :nivel :info :procesados n) f))
```

**`print` produce una representación legible por `read`** (clase 104), así que **analizar el registro es
llamar a `read`**, sin analizador y sin ambigüedad.

Es el registro estructurado con treinta años de adelanto, y sale gratis por la homoiconicidad del
lenguaje.

Y el sistema de condiciones aporta la otra mitad, y es la más interesante para esta clase (clase 116):

```lisp
(handler-bind ((warning (lambda (c)
                          (log-evento (list :nivel :warn :texto (princ-to-string c)))
                          (muffle-warning c))))     ; registrar Y CONTINUAR
  (procesar-todo))
```

**`handler-bind` observa la condición sin desenrollar la pila**, así que **se puede registrar el aviso
con todo el contexto vivo y luego decidir continuar**.

En un lenguaje con solo `try`/`catch`, registrar una advertencia obliga a lanzar y capturar —perdiendo
la pila— o a devolver códigos. Aquí **el registro es un observador**, que es conceptualmente lo
correcto: **anotar no debería alterar el flujo**.

Y los marcos del ecosistema:

| Marco | Notas |
|---|---|
| **log4cl** | jerárquico por paquete y función; **se configura desde el REPL** |
| **verbose** | asíncrono, con hilos |
| **cl-syslog** | al registro del sistema |

**log4cl merece la mención final** por lo que permite hacer con el modelo de la Parte 8:

```lisp
(log:config :debug)                      ; cambiar el nivel EN MARCHA
(log:config '(mi-paquete mi-funcion) :trace)   ; de UNA función concreta
```

**Subir el nivel de detalle de una sola función en un servidor en producción, sin reiniciar**, es la
capacidad que resuelve el problema práctico de esta clase: **el detalle que hace falta para diagnosticar
es demasiado caro para dejarlo siempre encendido**.
"""),
        "tcl": ("""
gets stdin linea
set n [string trim $linea]

puts "log=\\[INFO\\] procesados=$n"
""", """
**Lo que esta clase enseña en Tcl.** Fíjate en las barras invertidas: **`\\[` y `\\]`**. En Tcl los
corchetes son **sustitución de comandos**, así que `[INFO]` intentaría ejecutar un comando llamado
`INFO`. Hay que escaparlos, o usar llaves.

Es un recordatorio de la clase 081: **en Tcl el texto y el código comparten sintaxis**, y esa es a la
vez su mayor virtud y su trampa más frecuente.

Y Tcl trae su registro en la distribución, con una arquitectura que merece explicarse:

```tcl
package require logger

set log [logger::init miapp]
${log}::info "procesados=$n"
${log}::debug "detalle interno"
${log}::setlevel warn                 ;# cambiar el nivel en marcha

# y jerárquico:
set log2 [logger::init miapp::red]     ;# hereda de miapp
logger::setlevel miapp::red debug       ;# ...y se ajusta por separado
```

**La jerarquía por espacios de nombres** (clase 086) es lo que hace práctico el registro en un programa
grande: **`miapp::red` hereda la configuración de `miapp`**, y se puede subir el detalle de una rama sin
tocar el resto.

Es el mismo modelo de log4j y de todos sus descendientes, y en Tcl sale de una característica que ya
existía para otra cosa.

Y Tcl tiene una capacidad para esta clase que ya apareció en la clase 141 y que aquí es especialmente
útil: **instrumentar sin tocar el código**.

```tcl
trace add execution procesarPedido enter {apply {{cmd op} {
    ${::log}::info "entrada: $cmd"
}}}
trace add execution procesarPedido leave {apply {{cmd code res op} {
    ${::log}::info "salida: $res"
}}}
```

**Añadir registro a un procedimiento de una biblioteca ajena, en producción, sin recompilar y sin
tenerlo previsto.**

Y con `rename` (clase 139), lo mismo sobre cualquier comando, incluidos los del núcleo.

Es la respuesta más directa al problema real de esta clase: **el registro que hace falta es siempre el
que no se puso**. En Tcl se puede poner después.
"""),
        "perl": ("""
use strict;
use warnings;

my $n = <STDIN>;
chomp $n;

print "log=[INFO] procesados=$n\\n";
""", """
**Lo que esta clase enseña en Perl.** Perl fue durante veinte años **el lenguaje con el que se procesaban
los registros del mundo**, así que tiene una perspectiva doble: escribe registros y, sobre todo, los
lee.

Para escribir, el ecosistema:

```perl
use Log::Log4perl qw(:easy);
Log::Log4perl->easy_init($INFO);
INFO  "procesados=$n";
WARN  "reintento";
ERROR "fallo: $@";
```

**`Log::Log4perl` es un puerto fiel de log4j**, con la misma jerarquía de categorías, los mismos
niveles y **la misma configuración por fichero recargable en caliente**.

Y para el registro estructurado, que es donde va la industria:

```perl
use Log::Any qw($log);
$log->info("pedido procesado", { pedido_id => $id, ms => $t, items => $n });
```

**`Log::Any` desacopla la biblioteca del destino**: un módulo registra con `Log::Any` y **la
aplicación decide dónde va**. Es la solución al problema de que una biblioteca no debe imponer el
sistema de registro de quien la usa — el mismo papel que SLF4J en Java.

Y para leer, que es donde Perl fue insustituible:

```perl
while (<$log>) {
    next unless /\\[(\\w+)\\]\\s+(\\w+)=(\\S+)/;
    $conteo{$1}{$2} += $3;
}
```

**Una línea de expresión regular por formato**, y de ahí salieron **Logwatch**, **Swatch**,
**awstats**, **Nagios** y buena parte del ecosistema de monitorización de los años noventa.

Y merece cerrar con la lección que Perl aprendió por el camino difícil, y que justifica el registro
estructurado de toda esta clase:

**Analizar registros con expresiones regulares funciona hasta que el formato cambia.** Y cambia: alguien
añade un campo, o un mensaje lleva un salto de línea, o una ruta contiene un espacio. Cada cambio rompe
silenciosamente un guion que nadie vuelve a mirar.

De ahí la regla del cierre de esta clase: **registrar datos, no prosa**. Un `{"pedido":123,"ms":42}`
sobrevive a los cambios de formato; un `"Pedido 123 procesado en 42ms"` no.

Perl es el lenguaje que mejor demostró que se puede analizar cualquier cosa — y el que mejor demostró
por qué no conviene tener que hacerlo.
"""),
        "cpp": ("""
#include <iostream>

int main() {
    long long n{};
    if (!(std::cin >> n)) return 1;

    std::cout << "log=[INFO] procesados=" << n << '\\n';
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** C++ plantea esta clase desde el coste: **en un sistema que procesa
un millón de eventos por segundo, el registro puede ser más caro que el trabajo**.

Y de ahí las técnicas que definen el registro de alto rendimiento y que son transferibles a cualquier
lenguaje:

**Primera, comprobar el nivel antes de formatear:**

```cpp
if (logger.should_log(level::debug))
    logger.debug("estado: {}", costoso_de_formatear());
```

Y los marcos lo hacen con macros para que **ni siquiera se evalúen los argumentos**:

```cpp
SPDLOG_DEBUG("estado: {}", costoso());     // desaparece si el nivel es alto
```

**Segunda, registro asíncrono**: el hilo que trabaja **solo escribe a una cola**, y otro hilo formatea y
escribe al disco (clase 135). El coste en el camino crítico baja a unos nanosegundos.

**Y tercera, y es la más interesante: aplazar el formateo por completo.**

```cpp
// se guardan los ARGUMENTOS en binario, no el texto
LOG_BIN(EVENTO_PEDIDO, id, ms);
// y un programa aparte reconstruye el texto con la tabla de formatos
```

**Eso es *deferred formatting*, y es lo que usan las bibliotecas de baja latencia** —el trading de alta
frecuencia, sobre todo—. Registrar cuesta copiar unos bytes; el texto se compone después, fuera del
proceso.

Es exactamente la misma idea que los códigos numéricos de Ada en esta página, llegada por el camino del
rendimiento en lugar del camino del espacio.

El ecosistema:

| Biblioteca | Notas |
|---|---|
| **spdlog** | el más usado; síncrono o asíncrono, sobre `fmt` |
| **fmtlib** | formateo rápido y seguro de tipos; base de `std::format` |
| **Quill / NanoLog** | baja latencia, con formateo aplazado |
| **glog** | el de Google; veterano |
| **OpenTelemetry C++** | trazas y métricas con propagación de contexto |

Y **`std::format` (C++20) y `std::print` (C++23)** llevaron al estándar lo que `fmt` demostró:

```cpp
std::print("log=[{}] procesados={}\\n", "INFO", n);
```

**Comprobación del formato en tiempo de compilación**: si los tipos no encajan con la cadena, **no
compila**.

Es el fin de una familia entera de fallos de `printf` que llevaba cincuenta años produciendo caídas y
vulnerabilidades, y llegó al estándar en 2020.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi REGISTRO;
  n int(10) const;
end-pi;

dsply ('log=[INFO] procesados=' + %char(n));

*inlr = *on;
return;
""", """
**Lo que esta clase enseña en RPG.** Aquí está el caso que el gancho de la clase anunciaba: **en IBM i,
el registro existe sin que nadie lo pida**.

**El registro del trabajo** (clases 137 y 138) recoge **cada mensaje del sistema, con su código, su
texto, su ayuda de segundo nivel, el programa emisor, el número de sentencia y la pila de llamadas en
ese momento** — para todos los trabajos, siempre.

Y sobre eso, la plataforma tiene tres capas más que merecen conocerse porque cubren lo que en otros
sistemas requiere montar una infraestructura entera:

**Primera, las colas de mensajes como canal de registro:**

```rpgle
dcl-pr enviarMensaje extpgm('QMHSNDPM');
  ...
end-pr;
// o, más simple, con SQL:
exec sql CALL QSYS2.SEND_MESSAGE('procesados=' || :n);
```

**Un mensaje enviado a `QSYSOPR` aparece en la cola del operador**, que es donde alguien está mirando.

**Segunda, el diario de la base de datos** (clase 140), que registra **cada cambio de cada fila con
imagen anterior y posterior**, con el trabajo, el usuario y el programa. Es una auditoría completa sin
escribir código.

**Y tercera, y es la que sorprende: todo se consulta con SQL.**

```sql
SELECT * FROM TABLE(QSYS2.JOBLOG_INFO('123456/USUARIO/MIAPP'))
SELECT * FROM TABLE(QSYS2.STACK_INFO('*'))
SELECT * FROM QSYS2.ACTIVE_JOB_INFO(SUBSYSTEM_LIST_FILTER => 'QINTER')
SELECT * FROM TABLE(QSYS2.DISPLAY_JOURNAL('MIBIB', 'MIJRN'))
SELECT * FROM QSYS2.SYSTEM_STATUS_INFO
```

**Los registros, las pilas, los trabajos activos, el consumo de CPU y el diario son tablas.** Con
`WHERE`, `GROUP BY` y `JOIN`.

Es, literalmente, lo que un sistema de observabilidad moderno intenta ofrecer con una interfaz web
propia — disponible aquí con la herramienta de consulta que todo el mundo ya sabe usar.

Y merece extraer la lección general, porque es la del cierre de esta clase: **la observabilidad no es un
producto que se instala, es una propiedad del diseño del sistema**. IBM i la tiene porque decidió en
1988 que **cada objeto y cada trabajo llevarían su propia metainformación**; los sistemas que no lo
decidieron la reconstruyen después, a mucho mayor coste y peor.
"""),
        "pli": ("""
 registro: procedure options(main);

    declare n fixed binary(31);

    get list (n);

    put skip list ('log=[INFO] procesados=' || trim(char(n)));

 end registro;
""", """
**Lo que esta clase enseña en PL/I.** PL/I comparte la infraestructura de COBOL en esta página —SMF, las
colas de mensajes, los ficheros de registro estructurados— y aporta un mecanismo del lenguaje que
encaja exactamente con lo que la observabilidad moderna busca: **instrumentación declarada y activable
por ámbito**.

```pli
 (check(saldo, contador)):
 procesar: procedure;
    ...
 end procesar;

 on check(saldo)
    put skip list ('[TRACE] saldo=', saldo, ' en ', onloc());
```

**`CHECK` dispara el manejador cada vez que la variable cambia** (clase 141), y el manejador es código
normal: puede filtrar, contar o escribir a un fichero.

Y lo que lo hace relevante para esta clase es lo que ya se dijo de `pragma Debug` en Ada: **el prefijo
se puede quitar recompilando, sin tocar el código**, así que **la instrumentación no se pudre**.

Y PL/I tiene la infraestructura de condiciones que permite registrar el contexto completo de un fallo
(clases 137 y 138):

```pli
 on error snap begin;
    put skip list ('[ERROR] codigo=', oncode(), ' en=', onloc());
    put data;                              /* TODAS las variables */
    call escribir_bitacora();
 end;
```

**`snap` añade la traza de la pila y `put data` vuelca el estado completo** — que es, exactamente, lo
que un informe de excepción moderno contiene.

Y merece cerrar con la observación sobre el formato, porque conecta con la regla del cierre de la clase:

```pli
 put file(bitacora) edit
    (fecha, hora, nivel, programa, codigo, valor)
    (a(10), a(8), a(5), a(8), f(4), f(15,2));
```

**`put edit` con formato declarado produce columnas de posición fija**, igual que COBOL en esta página.

Y esa decisión —**posiciones fijas en lugar de separadores**— tiene una virtud que se aprecia después de
años: **un registro de longitud fija se lee igual dentro de veinte años**, sin depender de que nadie
haya cambiado un delimitador ni de que un valor contenga una coma.

Es la razón por la que los archivos históricos de estos sistemas siguen siendo legibles, y es un
argumento a favor de la disciplina que esta clase defiende: **el formato del registro es una decisión a
largo plazo, y el largo plazo llega**.
"""),
        "mumps": ("""
REGISTRO ; Registro con nivel -- clase 142
 read n
 write "log=[INFO] procesados=", n, !
 quit
""", """
**Lo que esta clase enseña en M.** M tiene, para esta clase, la respuesta más simple y una de las más
potentes de toda la página: **el registro es una escritura en la base de datos**.

```mumps
 set ^LOG($job, $horolog, $increment(^LOG("SEQ"))) = "INFO^procesados="_n
```

Y esa única línea da, sin nada más:

- **Persistencia**: es una global, está en disco.
- **Transaccionalidad**: participa en `tstart`/`tcommit` como cualquier otro dato.
- **Índice por trabajo y por tiempo**: los subíndices están ordenados (clase 095).
- **Consulta desde otro proceso, mientras el programa sigue corriendo.**
- **Y purga trivial**: `kill ^LOG(trabajoViejo)`.

**Consultarlo es recorrer con `$order`:**

```mumps
 set fecha = ""
 for  set fecha = $order(^LOG(trabajo, fecha)) quit:fecha=""  do
 . write fecha, " ", ^LOG(trabajo, fecha), !
```

Y con un índice adicional, se busca por nivel:

```mumps
 set ^LOGX("ERROR", $horolog, seq) = ""      ; índice secundario
```

**Eso es un sistema de registro indexado y consultable en unas pocas líneas**, y explica por qué los
sistemas VistA nunca necesitaron una infraestructura de registro aparte.

Y esta clase es el sitio para la advertencia más importante del cierre, porque en el dominio de M es
crítica: **M se usa en sanidad, y un registro con datos de pacientes es una historia clínica sin
control de acceso**.

```mumps
 ; ✗ NUNCA
 set ^LOG(...) = "consultado paciente "_nombre_" dni "_dni
 ; ✓ el identificador interno, y el resto por auditoría formal
 set ^LOG(...) = "consulta DFN="_dfn
```

Y VistA tiene precisamente para eso un mecanismo formal que merece nombrarse: **la auditoría de acceso
de FileMan**, que registra **quién** consultó **qué ficha** y **cuándo**, con control de acceso propio y
retención definida — separada del registro técnico.

Es la distinción que esta clase quiere dejar clara y que se aplica a cualquier sistema con datos
sensibles: **el registro técnico y la auditoría de acceso son dos cosas distintas, con dos públicos,
dos retenciones y dos niveles de protección**. Mezclarlas es el error que convierte un fichero de
diagnóstico en una brecha de datos.
"""),
        "smalltalk": ("""
| n |

n := stdin nextLine trimBoth asNumber.

Transcript show: 'log=[INFO] procesados=', n printString; cr.
""", """
**Lo que esta clase enseña en Smalltalk.** `Transcript` **es** el registro de Smalltalk, y es un objeto
como cualquier otro — lo que tiene una consecuencia directa: **se puede sustituir**.

```smalltalk
Transcript := MiRegistrador new.       "y todo el sistema registra donde yo diga"
```

Y el ecosistema tiene un marco moderno construido sobre esa idea, que merece explicarse porque es
distinto de todo lo demás de esta página: **Beacon**.

```smalltalk
"Emitir una SEÑAL: un OBJETO, no una cadena"
PedidoProcesadoSignal new
    pedido: unPedido;
    duracion: tiempo;
    emit.
```

**Lo que se emite es un objeto con sus campos**, no un texto. Y luego:

```smalltalk
"Los 'runners' deciden qué hacer con las señales"
logger := MemoryLogger new.       "guardar en memoria"
logger := FileLogger new.          "a un fichero"
logger := TranscriptLogger new.     "a la consola"
logger runFor: PedidoProcesadoSignal.
```

**La separación es limpia y es la que la industria acabó adoptando**: el código **emite eventos
tipados**, y la configuración decide **qué se conserva y dónde**.

Y las ventajas se ven al usarlo:

- **Se puede filtrar por clase de señal**, no por una cadena de nivel.
- **El objeto conserva sus referencias**: se puede inspeccionar el pedido, no solo su identificador.
- **Y el formateo se aplaza** al momento de escribir, o no ocurre nunca.

Eso último es lo mismo que el formateo aplazado de C++ en esta página, obtenido aquí **por ser objetos
desde el principio**.

Y Smalltalk añade lo que su modelo permite y que cierra esta clase con el mismo argumento que la 141:
**un error puede capturarse con su contexto entero**.

```smalltalk
[ self procesar ] on: Error do: [ :e |
    ErrorSignal new
        exception: e;
        context: e signalerContext copy;      "LA PILA, como objeto"
        emit ]
```

**Guardar la pila viva en el registro**, no su representación textual — y poder **abrirla en el
depurador** más tarde (clase 141).

Es el límite superior de lo que esta clase persigue: **el registro deja de ser un mensaje al futuro y
pasa a ser el estado mismo, conservado**. Y es coherente con las decisiones que Smalltalk tomó en toda
la Parte 8: **si todo es un objeto, todo se puede guardar, enviar y volver a mirar**.
"""),
    },
)
