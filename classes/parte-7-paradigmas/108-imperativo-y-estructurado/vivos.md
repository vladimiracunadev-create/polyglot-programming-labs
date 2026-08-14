# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 108

> [⬅️ Volver a la clase 108](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Un acumulador y un bucle. El paradigma imperativo en su forma más pura, y el sitio exacto donde estos
lenguajes tienen algo que contar que ninguno moderno puede: **la programación estructurada no fue un
descubrimiento académico, fue una guerra de veinte años**, y se libró en COBOL, en Fortran y en PL/I.
Los tres tuvieron que **añadir el `while`** a un lenguaje que ya llevaba décadas en producción.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es la **secuencia, la selección y la iteración** —las tres estructuras del teorema de
> Böhm-Jacopini (1966)—, y estos lenguajes lo enseñan porque son los que estaban ahí cuando se
> demostró. **FORTRAN no tuvo `IF/THEN/ELSE` hasta 1977 ni `DO WHILE` hasta 1990. COBOL no tuvo
> `END-IF` hasta 1985.** Antes de eso, la estructura se construía con `GO TO` y etiquetas.
>
> Y **RPG y M** aportan las dos rarezas: RPG tuvo un **bucle principal implícito** hasta que dejó de
> tenerlo, y M **no tiene bloques**: la condición va pegada al comando.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: una línea con enteros separados por espacio → stdout: `suma=<suma de todos>`
- **Regla:** `acumular la suma recorriendo la lista`

| stdin | esperado |
|---|---|
| `1 2 3` | `suma=6` |
| `5` | `suma=5` |
| `10 20` | `suma=30` |

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
PROGRAM-ID. IMPER.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA  PIC X(200).
01  TOKEN  PIC X(20).
01  TLEN   PIC 9(2)  COMP VALUE 0.
01  I      PIC 9(4)  COMP.
01  SUMA   PIC S9(18) COMP-3 VALUE 0.
01  ED-S   PIC -(17)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    MOVE SPACES TO TOKEN

    PERFORM VARYING I FROM 1 BY 1 UNTIL I > 200
        IF LINEA(I:1) = SPACE
            PERFORM ACUMULAR
        ELSE
            ADD 1 TO TLEN
            MOVE LINEA(I:1) TO TOKEN(TLEN:1)
        END-IF
    END-PERFORM
    PERFORM ACUMULAR

    MOVE SUMA TO ED-S
    DISPLAY "suma=" FUNCTION TRIM(ED-S)
    STOP RUN.

ACUMULAR.
    IF TLEN > 0
        COMPUTE SUMA = SUMA + FUNCTION NUMVAL(TOKEN)
        MOVE SPACES TO TOKEN
        MOVE 0 TO TLEN
    END-IF.
```

**Lo que esta clase enseña en COBOL.** COBOL es el caso mejor documentado de un lenguaje que **tuvo
que aprender a ser estructurado**, y las fechas lo cuentan:

| Año | Qué llegó |
|---|---|
| 1959 | `IF`, `GO TO`, `PERFORM`, `ALTER` |
| 1968 | `PERFORM VARYING` |
| 1974 | poco: el debate estaba en marcha |
| **1985** | **`END-IF`, `END-PERFORM`, `EVALUATE`, `PERFORM UNTIL` en línea** |
| 2002 | `EXIT PARAGRAPH`, `EXIT PERFORM`, `CONTINUE` |

**El punto de inflexión es 1985**, y el problema que resolvió era grave. Antes, un `IF` se cerraba con
un punto:

```cobol
    IF SALDO > 0
        DISPLAY "positivo"
        MOVE 1 TO X.
    DISPLAY "siempre"
```

Ese punto después de `MOVE 1 TO X` cierra el `IF`. Un punto de más, y la mitad del cuerpo se sale del
condicional; uno de menos, y el resto del párrafo entra dentro. **Y el compilador no se queja**,
porque las dos formas son legales.

Con `END-IF`, el problema desaparece: el bloque tiene un delimitador explícito, y hoy la práctica
universal es no usar puntos salvo al final del párrafo.

Y hay una sentencia que merece nombrarse porque es célebre por lo dañina: **`ALTER`**.

```cobol
    ALTER PARRAFO-X TO PROCEED TO PARRAFO-Z.
```

`ALTER` **cambia en ejecución el destino de un `GO TO`**. Es decir: leyendo el código no se puede
saber a dónde salta, porque depende de qué `ALTER` se haya ejecutado antes. Es el `GO TO` calculado
elevado a su peor forma, y produjo código literalmente imposible de seguir.

Está **obsoleta desde COBOL-85 y eliminada del estándar de 2002**, y sigue apareciendo en programas
antiguos que nadie se atreve a tocar. Cuando se habla del "código COBOL heredado ininteligible", una
parte concreta de esa reputación tiene nombre, y es este.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program imper
   implicit none
   integer :: v(100), n, ios, i
   integer :: suma
   character(len=400) :: linea

   read(*, '(A)') linea

   n = 0
   do i = 1, 100
      read(linea, *, iostat=ios) v(1:i)
      if (ios /= 0) exit
      n = i
   end do

   !  Estilo IMPERATIVO: acumulador y bucle explícito
   suma = 0
   do i = 1, n
      suma = suma + v(i)
   end do

   write(*, '(A,I0)') 'suma=', suma
end program imper
```

**Lo que esta clase enseña en Fortran.** Fortran es el otro gran caso de esta clase, y su historia es
aún más llamativa que la de COBOL: **el FORTRAN de 1957 no tenía `IF/THEN/ELSE`**.

Lo que tenía era el **`IF` aritmético**, una de las construcciones más extrañas que han existido:

```fortran
      IF (X - Y) 10, 20, 30
```

**Tres etiquetas: salta a la primera si la expresión es negativa, a la segunda si es cero y a la
tercera si es positiva.** Es una bifurcación a tres bandas, pensada para el hardware del IBM 704, y
era la única forma de decidir.

La cronología de la estructuración de Fortran:

| Versión | Qué añadió | Qué faltaba |
|---|---|---|
| 1957 | `IF` aritmético, `DO`, `GO TO` | todo lo demás |
| 1966 | `IF` lógico de una sentencia | bloques |
| **1977** | **`IF/THEN/ELSE/END IF`** | **no hay `WHILE`** |
| **1990** | **`DO WHILE`, `EXIT`, `CYCLE`, `SELECT CASE`** | — |
| 1995 | se **borran** del estándar `ASSIGN` y el `GO TO` asignado | — |

**Fortran no tuvo `while` hasta 1990.** Treinta y tres años escribiendo bucles condicionales así:

```fortran
   10 IF (.NOT. COND) GO TO 20
         ...
      GO TO 10
   20 CONTINUE
```

Ese idioma está en todo el código Fortran clásico, y explica por qué las bibliotecas numéricas
históricas —LINPACK, EISPACK, las rutinas de Numerical Recipes— se leen como se leen. **No es mala
programación: es que no había otra forma.**

Y hay un fósil que merece verse porque hoy sería inconcebible: **el `DO` original ejecutaba el cuerpo
al menos una vez**, aunque el límite fuera menor que el inicio. `DO 10 I = 1, 0` daba una vuelta. Se
corrigió en Fortran 77, y hubo que revisar código.

Fortran 90 completó la estructuración con nombres de bucle, que son mejores que el `break` con
etiqueta de otros lenguajes:

```fortran
externo: do i = 1, n
   interno: do j = 1, m
      if (...) exit externo         ! salir del bucle EXTERNO por su nombre
      if (...) cycle interno
   end do interno
end do externo
```

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Imper is
   Linea  : String (1 .. 400);
   Ultimo : Natural;
   Pos    : Integer := 1;
   Valor  : Integer;
   Fin    : Positive;
   Suma   : Integer := 0;
begin
   Get_Line (Linea, Ultimo);

   loop
      while Pos <= Ultimo and then Linea (Pos) = ' ' loop
         Pos := Pos + 1;
      end loop;
      exit when Pos > Ultimo;

      Get (Linea (Pos .. Ultimo), Valor, Fin);
      Suma := Suma + Valor;
      Pos := Fin + 1;
   end loop;

   Put ("suma=");
   Put (Suma, Width => 1);
   New_Line;
end Imper;
```

**Lo que esta clase enseña en Ada.** Ada nació **después** de que la batalla estructurada terminara, y
se nota: es de los pocos lenguajes de esta página donde el `goto` casi no se usa, y donde el diseño de
los bucles está pensado con cuidado.

Ada tiene **una sola construcción de bucle** con tres formas:

```ada
loop ... end loop;                       --  infinito
while Cond loop ... end loop;             --  con condición al principio
for I in 1 .. N loop ... end loop;         --  contado
for I in reverse 1 .. N loop ... end loop; --  descendente
for E of Coleccion loop ... end loop;       --  Ada 2012: sobre los ELEMENTOS
```

Y **`exit when`**, que es la aportación de diseño:

```ada
loop
   Leer (X);
   exit when X = 0;
   Procesar (X);
end loop;
```

Eso resuelve el **bucle "y medio"** —el que necesita salir por el medio— que Dijkstra señaló como el
caso que las tres estructuras clásicas no cubren bien. En C hay que escribir `while (true)` con un
`break`; en Ada, `exit when` es la forma normal.

Y `exit` acepta el nombre del bucle, como en Fortran:

```ada
Externo:
for I in 1 .. N loop
   for J in 1 .. M loop
      exit Externo when Encontrado;
   end loop;
end loop Externo;
```

Fíjate en que **`end loop Externo` repite el nombre**. Ada lo permite —y lo exige si el bucle está
nombrado— para todos los bloques: `end if`, `end loop Nombre`, `end Procedimiento`. En un
procedimiento de trescientas líneas, saber qué se está cerrando sin contar sangrías es más útil de lo
que parece.

Ada **sí tiene `goto`**, con la sintaxis `goto <<Etiqueta>>`, y las guías lo permiten para un caso
concreto: salir de bucles anidados profundos en código generado. Que exista, esté acotado y casi no se
use es la señal de que el debate ya estaba resuelto cuando el lenguaje se diseñó.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Imper;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  Linea, Tok: string;
  I, Suma: Integer;
  C: Char;

begin
  ReadLn(Linea);

  Suma := 0;
  Tok := '';

  for I := 1 to Length(Linea) + 1 do
  begin
    if I <= Length(Linea) then C := Linea[I] else C := ' ';
    if C = ' ' then
    begin
      if Tok <> '' then
      begin
        Suma := Suma + StrToInt(Tok);
        Tok := '';
      end;
    end
    else
      Tok := Tok + C;
  end;

  WriteLn('suma=', IntToStr(Suma));
end.
```

**Lo que esta clase enseña en Pascal.** Pascal **es** esta clase: se diseñó en 1970 para enseñar
exactamente esto, y su sintaxis es la programación estructurada convertida en gramática.

Las tres estructuras están completas y sin excepciones desde el primer día:

```pascal
begin ... end                 { secuencia }
if ... then ... else          { selección }
case ... of ... end            { selección múltiple, CON rangos (clase 092) }
while ... do                    { iteración con condición al principio }
repeat ... until                 { con condición al final }
for ... to / downto ... do        { iteración contada }
```

Y lo que **deliberadamente NO tiene** es lo más instructivo:

- **Sin `break` ni `continue`** en el Pascal original. Wirth los consideraba `goto` disfrazados.
- **Sin `return` anticipado**: el valor se asigna al nombre de la función y el procedimiento termina
  donde termina.
- **Sin caída entre casos** en el `case`, al contrario que el `switch` de C.
- **El `for` no permite modificar la variable de control dentro del bucle** — el estándar lo prohíbe,
  y la variable **queda indefinida al salir**.

Esa última regla suele sorprender y tiene un motivo técnico: permite al compilador guardar el índice
en un registro y no escribirlo en memoria.

Pascal **sí tiene `goto`**, y Wirth lo incluyó a regañadientes con una restricción severa: **solo
puede saltar a una etiqueta del mismo bloque o de uno que lo contenga**, nunca hacia dentro de otro
bloque. Es `goto` que no puede romper la estructura.

Y hay un detalle histórico que cierra el argumento de esta clase: **Pascal apareció en 1970, dos años
después de la carta de Dijkstra sobre el `GO TO`**. No es una coincidencia — Wirth y Dijkstra
trabajaron juntos en el comité de Algol 68 y compartían el diagnóstico. Pascal es la respuesta de
Wirth escrita en forma de compilador, después de que la propuesta conjunta que firmaron contra Algol
68 fuera rechazada.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let ((suma 0))
  (loop for x = (read *standard-input* nil nil)
        while x
        do (incf suma x))                  ; imperativo: mutar un acumulador
  (format t "suma=~D~%" suma))
```

**Lo que esta clase enseña en Common Lisp.** Que un programa Lisp aparezca en la clase de programación
imperativa no es una contradicción: **Common Lisp es tan imperativo como funcional**, y esa es una de
sus diferencias más importantes con Scheme y con Haskell.

El lenguaje tiene, sin ningún reparo:

```lisp
(setf x 10)                       ; asignación
(incf x)  (decf x)                 ; incremento y decremento
(push x lista)  (pop lista)         ; mutación de estructuras
(setf (aref v 3) 99)                 ; escribir en un vector
(setf (gethash k tabla) v)            ; y en una tabla hash
(dotimes (i 10) ...)  (dolist (x l) ...)  (loop ...)
(prog1 ...)  (progn ...)  (tagbody ... (go etiqueta))
```

**Y sí, Lisp tiene `go`.** `tagbody` con etiquetas y `go` es una construcción del estándar, y es la
primitiva sobre la que se implementan los bucles: `loop`, `do` y `dotimes` **se expanden a `tagbody`
con `go`**.

Eso es exactamente lo que Lisp hace distinto: **las estructuras de control son macros sobre
primitivas de salto**, así que el lenguaje ofrece las estructuras civilizadas y **deja la primitiva
accesible** para quien construya nuevas.

Y hay una razón histórica que conviene decir, porque desmonta una idea muy extendida: **Lisp no era un
lenguaje funcional puro en 1958**. Tenía `setq`, `rplaca` y `rplacd` —mutación destructiva de
*conses*— desde el principio. La pureza funcional llegó como **estilo recomendado** mucho después, y
principalmente desde la comunidad de Scheme y de ML.

El estilo dominante en Common Lisp real es mixto: **funcional donde ayuda, imperativo donde es más
claro**, y con `loop` como caballo de batalla. La razón la dan las clases 084 y 090: acumular con
`push` e invertir, o usar `loop ... collect`, es más rápido y más legible que la recursión pura, y la
comunidad lo asumió sin complejos.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea

set suma 0
foreach x [split [string trim $linea]] {
    incr suma $x
}

puts "suma=$suma"
```

**Lo que esta clase enseña en Tcl.** Tcl es imperativo y sus estructuras de control son **comandos**,
no sintaxis — lo que ya se vio en la clase 107 y que aquí tiene una consecuencia práctica muy
concreta.

```tcl
if {$x > 0} { ... } elseif { ... } else { ... }
while {$x > 0} { ... }
for {set i 0} {$i < 10} {incr i} { ... }
foreach x $lista { ... }
foreach {a b} $lista { ... }          ;# de DOS en dos
foreach a $l1 b $l2 { ... }            ;# DOS listas a la vez
switch -exact -- $x { ... }
break    continue    return
```

Dos de esas formas de `foreach` no las tiene casi nadie: **recorrer de n en n** y **recorrer varias
listas en paralelo**. Son cómodas y son consecuencia de que `foreach` sea un comando que recibe pares
de argumentos, no una construcción con gramática fija.

Y **Tcl no tiene `goto`**. Nunca lo tuvo, y su ausencia no se echa de menos porque `break`,
`continue`, `return` y las excepciones cubren los casos.

Lo que sí tiene, y es lo característico, es que **el flujo de control se puede extender**. `uplevel` y
`upvar` permiten escribir comandos que ejecutan código en el ámbito del llamante:

```tcl
proc mientras_haya {var lista cuerpo} {
    upvar 1 $var v
    foreach v $lista {
        uplevel 1 $cuerpo
    }
}
```

Ese `mientras_haya` es una estructura de control nueva, y **se usa exactamente igual que `foreach`**.

Hay una consecuencia de rendimiento que conviene conocer: como `if` y `while` son comandos que
reciben cadenas, **es crucial usar llaves y no comillas**:

```tcl
while {$i < 10} { ... }      ;# la condición se COMPILA una vez
while "$i < 10" { ... }       ;# se sustituye ANTES: bucle infinito, y lento
```

Con llaves, el compilador de bytecode de Tcl 8.0+ compila la expresión una sola vez. Sin ellas, se
reanaliza en cada vuelta. Es la diferencia entre Tcl rápido y Tcl lento, y está en un par de llaves.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;

my $suma = 0;
$suma += $_ for split ' ', $linea;      # modificador de sentencia

print "suma=$suma\n";
```

**Lo que esta clase enseña en Perl.** La línea `$suma += $_ for split ' ', $linea;` usa un
**modificador de sentencia**, que es una de las señas de identidad del lenguaje:

```perl
print "hola" if $x > 0;
$total += $_ for @lista;
print while <$fh>;
$i++ until $i >= 10;
do { ... } while $cond;        # la ÚNICA forma de do-while
```

Escribir la condición **detrás** de la acción viene de la sensibilidad lingüística de Larry Wall: en
lenguaje natural se dice "cierra la puerta si hace frío", no "si hace frío, cierra la puerta". Para
una sola acción, el modificador se lee mejor y evita las llaves.

Y Perl tiene el juego completo de estructuras, con detalles propios:

```perl
if / elsif / else / unless        # unless = if not
while / until / for / foreach
last / next / redo                 # break / continue / REPETIR sin reevaluar
LOOP: foreach (...) { last LOOP; } # etiquetas de bucle
```

**`redo`** no lo tiene casi ningún lenguaje: repite el cuerpo del bucle **sin reevaluar la condición
ni avanzar el iterador**. Es útil para reintentos.

Y **Perl tiene `goto`**, en tres formas, y la tercera es una rareza que merece nombrarse:

```perl
goto ETIQUETA;              # el goto clásico, prácticamente sin uso
goto &otra_funcion;         # SUSTITUIR la llamada actual por otra
```

**`goto &funcion`** reemplaza el marco de pila actual por el de otra función, **pasándole `@_` tal
cual**. La función original desaparece del rastro de llamadas, como si nunca hubiera estado.

Se usa para dos cosas reales: **llamadas en cola sin crecer la pila** —recursión de cola de verdad— y
**funciones envolventes transparentes**, que es como funcionan `AUTOLOAD` y varios módulos de CPAN
que interceptan llamadas.

Es una primitiva de bajo nivel expuesta en un lenguaje de alto nivel, muy en la línea de Perl:
**dejarte hacer lo que quieras y confiar en que sabes lo que haces**.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>
#include <iterator>
#include <vector>

int main() {
    std::vector<int> v{std::istream_iterator<int>(std::cin),
                       std::istream_iterator<int>()};

    int suma = 0;
    for (int x : v) {          // bucle basado en rango (C++11)
        suma += x;
    }

    std::cout << "suma=" << suma << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** C++ hereda de C todas las estructuras y **también el `goto`**, y
su historia en esta clase es la de un lenguaje que **añadió abstracción sin quitar nada**.

El bucle de este programa es la forma moderna:

```cpp
for (int x : v) { ... }              // C++11: sobre los ELEMENTOS
for (const auto& [k, val] : mapa) { ... }   // C++17, con enlace estructurado
for (auto x : v | std::views::filter(par)) { ... }   // C++20
```

Frente al de C, que sigue siendo legal:

```cpp
for (std::size_t i = 0; i < v.size(); ++i) { ... }
```

La diferencia no es estética: **el bucle basado en rango no puede tener un error de índice**, porque
no hay índice. Elimina de un plumazo la familia entera de errores de "uno de más" y de acceso fuera de
rango, que son la causa de una parte enorme de los fallos de seguridad de C y C++.

Y esta clase es el sitio para el `switch`, porque C tomó una decisión que se considera un error de
diseño y C++ la heredó:

```cpp
switch (x) {
    case 1:
        hacer_algo();
        // ¡sin break! CAE al caso siguiente
    case 2:
        hacer_otra();
        break;
}
```

**La caída entre casos es el comportamiento por defecto**, y olvidar un `break` es un error silencioso
tan común que los compiladores llevan décadas avisando con `-Wimplicit-fallthrough`. C++17 añadió
`[[fallthrough]]` para declarar que la caída es intencionada.

Pascal (1970), Ada (1983) y PL/I (1964) **no tienen ese problema**: en los tres, cada caso termina
solo. C lo introdujo en 1972, después de que los tres lo hubieran resuelto, y todos sus descendientes
—C++, Java, C#, JavaScript, PHP— lo arrastran.

Es probablemente el ejemplo más citado de que **una decisión de diseño mala sobrevive a base de
compatibilidad**, y por eso Go, Rust, Swift y Kotlin rompieron con ella explícitamente.

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

dcl-pi IMPER;
  entrada char(200) const;
end-pi;

dcl-s texto varchar(200);
dcl-s tok   varchar(20) inz('');
dcl-s c     char(1);
dcl-s i     int(10);
dcl-s suma  int(20) inz(0);

texto = %trimr(entrada);

for i = 1 to %len(texto) + 1;
  if i <= %len(texto);
    c = %subst(texto : i : 1);
  else;
    c = ' ';
  endif;
  if c = ' ';
    if tok <> '';
      suma += %int(tok);
      tok = '';
    endif;
  else;
    tok += c;
  endif;
endfor;

dsply ('suma=' + %char(suma));

*inlr = *on;
return;
```

**Lo que esta clase enseña en RPG.** RPG es el lenguaje de esta página cuya historia con la
programación estructurada es más rara, porque **su punto de partida no era el `GO TO`: era no tener
flujo de control en absoluto**.

En el RPG original (clase 107), el programador **no escribía el bucle principal**: lo generaba el
ciclo. Y para decidir, no había `IF`: había **indicadores**.

```text
C           SALDO     COMP 0                        10 11 12
C   10                MOVE  'DEUDOR'    ESTADO
```

Esa línea compara `SALDO` con 0 y **enciende los indicadores 10, 11 o 12** según sea mayor, menor o
igual. La siguiente línea, condicionada por el indicador 10, hace algo. Son los **indicadores `*IN01`
a `*IN99`**, banderas globales numeradas que gobernaban todo el programa.

Es exactamente el `IF` aritmético de Fortran (clase 108, apartado de Fortran) llevado a su forma más
extrema: **el estado del programa está en cien banderas globales con nombres de número**, y para saber
qué hace una línea hay que saber qué indicadores están encendidos, que depende de todo lo anterior.

De ahí la mala fama del RPG clásico, y merece decirse que estaba justificada.

La estructuración llegó por etapas:

| Versión | Qué llegó |
|---|---|
| 1978 (RPG III) | `DO`, `DOW`, `DOU`, `IF`, `ELSE`, `END`, subrutinas |
| 1994 (RPG IV) | procedimientos con parámetros y valor de retorno |
| 2001 | **formato libre en el cálculo**: `if x > 0;` en lugar de columnas |
| 2013 | formato totalmente libre, sin columnas en ninguna parte |

Y el RPG moderno de este programa —`for`, `if`, `endif`, funciones `%`— se lee como cualquier lenguaje
imperativo actual. **Los indicadores siguen existiendo** y siguen usándose para la comunicación con
las pantallas, pero la lógica ya no depende de ellos.

Es probablemente la transformación más completa de esta página: de un generador de informes con
banderas globales a un lenguaje estructurado con procedimientos, sin romper la compatibilidad en
sesenta años.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 imper: procedure options(main);

    declare linea char(200) varying;
    declare tok   char(20)  varying initial('');
    declare c     char(1);
    declare (i, suma) fixed binary(31);

    get edit (linea) (a(200));
    linea = trim(linea);
    suma = 0;

    do i = 1 to length(linea) + 1;
       if i <= length(linea) then c = substr(linea, i, 1); else c = ' ';
       if c = ' ' then do;
          if tok ^= '' then do;
             suma = suma + tok;
             tok = '';
          end;
       end;
       else tok = tok || c;
    end;

    put skip list ('suma=' || trim(char(suma)));

 end imper;
```

**Lo que esta clase enseña en PL/I.** PL/I es el lenguaje de esta página que **nació estructurado**, y
es un dato que suele pasarse por alto: **en 1964, PL/I ya tenía todo lo que a Fortran le faltaría
hasta 1990 y a COBOL hasta 1985**.

```pli
 if ... then do; ... end; else do; ... end;
 do while (cond);  ...  end;
 do until (cond);  ...  end;
 do i = 1 to 10 by 2;  ...  end;
 select (x); when (1) ...; otherwise ...; end;
 leave;      /* break */
 iterate;    /* continue */
```

`do while` en 1964. `select` sin caída entre casos en 1964. `leave` e `iterate` con **nombre de bloque
opcional** para salir de bucles anidados:

```pli
 externo: do i = 1 to n;
    do j = 1 to m;
       leave externo;
    end;
 end externo;
```

Todo eso estaba en el lenguaje **cuatro años antes de la carta de Dijkstra sobre el `GO TO`**, y esa
coincidencia no es casual: PL/I se diseñó con la influencia directa de **Algol 60**, que ya tenía
bloques y estructuras, y su comité incluía a gente que venía de ahí.

Es una de las mejores respuestas a la idea de que "los lenguajes antiguos eran primitivos": **el
problema no era que no se supiera cómo hacerlo, era que Fortran y COBOL ya tenían demasiado código
escrito para cambiar**.

PL/I **sí tiene `go to`**, y con una capacidad peligrosa que ya apareció en la clase 085: **las
variables de etiqueta**.

```pli
 declare destino label;
 destino = fin;
 go to destino;              /* salto INDIRECTO */
```

Y algo más raro todavía: **se puede saltar a una etiqueta de un bloque exterior desde dentro de un
procedimiento anidado**, deshaciendo los marcos de pila intermedios. Es un `throw` sin `catch`, y es
la construcción que hacía que el código PL/I de los setenta pudiera ser tan difícil de seguir pese a
tener todas las estructuras a mano.

La moraleja encaja con el cierre de esta clase: **tener las estructuras no basta si el lenguaje deja
abierta la puerta de atrás**.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
IMPER ; Imperativo y estructurado -- clase 108
 read linea
 set suma = 0
 for i=1:1:$length(linea, " ") set suma = suma + $piece(linea, " ", i)
 write "suma=", suma, !
 quit
```

**Lo que esta clase enseña en M.** M es el lenguaje **menos estructurado** de esta página, y no por
antigüedad —PL/I es dos años anterior y estaba mucho mejor estructurado— sino por una decisión de
diseño: **M no tiene bloques**.

No hay `begin`/`end`, no hay llaves y no hay `endif`. Lo que hay es:

**El postcondicional**, que pega la condición al comando:

```mumps
 set:x>0 y=1              ; ejecuta el set SOLO si x>0
 quit:x=""                 ; salir si está vacío
 do:valido procesar
 write:n>10 "muchos",!
```

**El `if` sin `else` real**, cuyo alcance es **hasta el final de la línea**:

```mumps
 if x>0 write "positivo" set y=1        ; las DOS cosas si x>0
```

Y **`else`** no es un bloque: es un comando que se ejecuta si el último `if` fue falso, apoyándose en
una variable del sistema, **`$test`**.

```mumps
 if x>0 write "positivo"
 else  write "no positivo"
```

`$test` es global al proceso, así que **cualquier cosa que se ejecute entre el `if` y el `else` puede
cambiarlo**, incluida una llamada a otra rutina. Es una de las construcciones más frágiles que existen
en un lenguaje en producción.

La estructuración llegó a medias con los **niveles de punto**:

```mumps
 for i=1:1:10 do
 . set x = i * 2
 . if x > 10 do
 . . write x,!
```

Un punto por nivel de anidamiento, al principio de la línea. **Es sangría con significado
sintáctico**, veinticinco años antes que Python, y con la fragilidad que cabe esperar: un punto de más
o de menos cambia la estructura en silencio.

Y M **sí tiene `goto`**, con indirección (clase 085): `goto @etiqueta`, donde el destino se construye
como cadena en ejecución.

Es la única entrada de esta página donde hay que decirlo sin matices: **M se quedó fuera de la
revolución estructurada**, y lo que lo mantiene vivo no es su modelo de programación sino su modelo de
datos (clase 107).

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| suma |

suma := 0.
stdin nextLine substrings do: [ :cada |
    suma := suma + cada asNumber ].

Transcript show: 'suma=', suma printString; cr.
```

**Lo que esta clase enseña en Smalltalk.** Smalltalk resuelve esta clase de una forma que la
trasciende: **no tiene estructuras de control, y por eso no tuvo que estructurarse**.

Como se dijo en la clase 107, `ifTrue:`, `whileTrue:` y `to:do:` son **mensajes**, no sintaxis. Y esa
decisión tiene una consecuencia directa sobre el tema de esta clase: **no hay `goto` que prohibir,
porque no hay sitio donde ponerlo**.

```smalltalk
x > 0 ifTrue: [ ... ] ifFalse: [ ... ]
[ x > 0 ] whileTrue: [ ... ]
[ x = 0 ] whileFalse: [ ... ]
1 to: 10 do: [ :i | ... ]
10 timesRepeat: [ ... ]
coleccion do: [ :cada | ... ]
```

Y `ifTrue:ifFalse:` está implementado **en el propio lenguaje**, con polimorfismo:

```smalltalk
True  >> ifTrue: b1 ifFalse: b2    ^b1 value
False >> ifTrue: b1 ifFalse: b2    ^b2 value
```

**El condicional es despacho dinámico sobre dos clases con un objeto cada una.** No hay salto
condicional en el modelo: hay un mensaje que dos clases responden distinto. Es de las ideas más
elegantes que se han puesto en un lenguaje de programación.

En la práctica, el compilador reconoce esos mensajes cuando el receptor es un booleano y los **integra
en línea** generando saltos reales — pero el modelo sigue siendo válido, y si envías `ifTrue:` a un
objeto propio que lo implemente, funciona.

Lo único que se parece a un salto no local es el **retorno desde un bloque**:

```smalltalk
coleccion do: [ :cada | cada = objetivo ifTrue: [ ^cada ] ].
^nil
```

Ese **`^` dentro de un bloque no sale del bloque: sale del MÉTODO que lo creó** (clase 083). Es un
retorno no local, y está implementado desenrollando la pila hasta el contexto del método — con la
posibilidad de que ese contexto ya haya terminado, en cuyo caso se lanza `BlockCannotReturn`.

Es lo más parecido a un `goto` que tiene Smalltalk, y su nombre lo dice todo: **no es un salto, es un
retorno que ocurre desde otro sitio**.

---

## Y de vuelta a la clase

Lo transferible: **el `GO TO` no se prohibió por dogma, se abandonó porque impide razonar
localmente**. Con saltos arbitrarios, para saber qué vale una variable en una línea hay que examinar
el programa entero; con bloques anidados, basta con lo que hay encima. Esa propiedad —**poder razonar
sobre un trozo sin leer el resto**— es lo que buscan también las funciones puras, la inmutabilidad y
los tipos. La programación estructurada fue la primera victoria de esa idea, y las demás clases de
esta parte son continuaciones de la misma batalla.

⏮️ [Volver a la clase 108](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
