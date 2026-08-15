# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 140

> [⬅️ Volver a la clase 140](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Comparar dos resultados y decir si son equivalentes. Es literalmente lo que hace el verificador de este
curso (clase 040) y lo que este programa reproduce en doce lenguajes. Y no es un ejercicio académico:
**la migración de sistemas COBOL a Java lleva treinta años haciendo exactamente esto** — ejecutar los
dos sistemas con los mismos datos durante meses y comparar cada salida, byte a byte, antes de apagar el
viejo.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es la **equivalencia observable**: dos implementaciones distintas son intercambiables
> si producen la misma salida para las mismas entradas. Y estos lenguajes lo enseñan porque **es su
> problema profesional real**. COBOL y PL/I viven en migraciones. RPG convive con Java en la misma
> máquina. Fortran valida modelos nuevos contra modelos viejos. Y todos ellos aportan la parte incómoda:
> **la equivalencia no es igualdad**, porque hay redondeo, orden y precisión de por medio.
>
> Y aparece la pregunta que atraviesa la clase: **¿qué tolerancia hace falta para que "igual" siga
> significando algo?**
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: una línea `x y` (dos resultados a comparar) → stdout: `equivalente=<true|false>`
- **Regla:** `equivalente si x == y`

| stdin | esperado |
|---|---|
| `6 6` | `equivalente=true` |
| `5 7` | `equivalente=false` |
| `0 0` | `equivalente=true` |

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
```

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

Y COBOL aporta a esta clase el motivo técnico más frecuente de discrepancia, que es de la clase 045:
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

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
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
```

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

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
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
```

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

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
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
```

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

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let ((x (read))
      (y (read)))
  (format t "equivalente=~A~%" (if (equal x y) "true" "false")))
```

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

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea
lassign [string trim $linea] x y

puts "equivalente=[expr {$x eq $y ? {true} : {false}}]"
```

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

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;
my ($x, $y) = split ' ', $linea;

print "equivalente=", ($x eq $y ? 'true' : 'false'), "\n";
```

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
    creado_en => re(qr/^\d{4}-\d{2}/),      # una fecha, no importa cuál
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

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>
#include <string>

int main() {
    std::string x, y;
    if (!(std::cin >> x >> y)) return 1;

    std::cout << "equivalente=" << (x == y ? "true" : "false") << '\n';
    return 0;
}
```

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
```

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

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 equival: procedure options(main);

    declare (x, y) fixed binary(31);

    get list (x, y);

    if x = y then
       put skip list ('equivalente=true');
    else
       put skip list ('equivalente=false');

 end equival;
```

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

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
EQUIVAL ; Verificador de equivalencia -- clase 140
 read linea
 set x = $piece(linea, " ", 1)
 set y = $piece(linea, " ", 2)
 write "equivalente=", $select(x = y : "true", 1 : "false"), !
 quit
```

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

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| linea partes x y |

linea := stdin nextLine trimBoth.
partes := linea substrings: ' '.

x := partes at: 1.
y := partes at: 2.

Transcript show: 'equivalente=', (x = y ifTrue: [ 'true' ] ifFalse: [ 'false' ]); cr.
```

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

---

## Y de vuelta a la clase

Lo transferible: **una prueba de integración comprueba una frontera; el verificador de equivalencia
comprueba una sustitución**. Y el segundo es la herramienta más valiosa que existe para cambiar algo
grande sin miedo, porque convierte una migración en una operación con red: si el nuevo produce lo mismo
que el viejo para todo lo que ha pasado por el sistema, se puede cambiar. La disciplina que hay que
aprender es **guardar entradas y salidas reales**, porque sin ellas no hay red — y esa decisión hay que
tomarla antes de necesitarla.

⏮️ [Volver a la clase 140](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
