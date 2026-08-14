# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 065

> [⬅️ Volver a la clase 065](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Sumar una lista de enteros cuya longitud **no se sabe de antemano**. Ahí está la diferencia con la
clase anterior: un bucle de rango necesita saber cuántas vueltas dará; recorrer una colección
necesita otra cosa — **preguntarle a la propia colección si queda algo**. Esa inversión es el
concepto del iterador.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es el **recorrido de una colección**, y estos lenguajes lo enseñan porque muestran
> lo que había **antes de que existiera el iterador como abstracción**. En COBOL y Fortran clásico hay
> que llevar el contador a mano, y por eso el idioma es "una tabla y una variable con cuántos elementos
> tiene ocupados". En RPG, el bucle ni siquiera se escribe: **lo pone el ciclo del programa**.
>
> Y M enseña la versión más potente y menos conocida: **`$order` recorre un árbol persistente de un
> millón de nodos sin cargarlo en memoria**, que es exactamente lo que hoy llamamos un iterador
> perezoso sobre una base de datos.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: una línea con enteros separados por espacio → stdout: `suma=<suma de todos>`
- **Regla:** `suma = Σ elementos`

| stdin | esperado |
|---|---|
| `3 1 4` | `suma=8` |
| `10 20 30` | `suma=60` |
| `5` | `suma=5` |

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
PROGRAM-ID. SUMALISTA.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(200).
01  I       PIC 9(4)  COMP-3.
01  LARGO   PIC 9(4)  COMP-3.
01  TOKEN   PIC X(20).
01  TLEN    PIC 9(4)  COMP-3.
01  C       PIC X.
01  TOTAL   PIC S9(18) COMP-3.
01  ED-T    PIC -(17)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    MOVE 0 TO TOTAL
    MOVE SPACES TO TOKEN
    MOVE 0 TO TLEN
    COMPUTE LARGO = FUNCTION LENGTH(FUNCTION TRIM(LINEA)) + 1

    PERFORM VARYING I FROM 1 BY 1 UNTIL I > LARGO
        MOVE LINEA(I:1) TO C
        IF C = SPACE
            IF TLEN > 0
                COMPUTE TOTAL = TOTAL + FUNCTION NUMVAL(TOKEN(1:TLEN))
                MOVE SPACES TO TOKEN
                MOVE 0 TO TLEN
            END-IF
        ELSE
            ADD 1 TO TLEN
            MOVE C TO TOKEN(TLEN:1)
        END-IF
    END-PERFORM

    MOVE TOTAL TO ED-T
    DISPLAY "suma=" FUNCTION TRIM(ED-T)
    STOP RUN.
```

**Lo que esta clase enseña en COBOL.** **COBOL no tiene iteradores ni colecciones de tamaño
variable.** Tiene **tablas** con `OCCURS`, que son arrays de tamaño fijo declarado, y el número de
elementos ocupados lo lleva el programador en una variable aparte:

```cobol
01  TABLA-VENTAS.
    05  NUM-VENTAS  PIC 9(4) COMP-3.
    05  VENTA       OCCURS 1 TO 1000 TIMES
                    DEPENDING ON NUM-VENTAS
                    PIC S9(9)V99 COMP-3.

PERFORM VARYING I FROM 1 BY 1 UNTIL I > NUM-VENTAS
    ADD VENTA(I) TO TOTAL
END-PERFORM
```

`OCCURS DEPENDING ON` es lo más cerca que llega COBOL de una colección de tamaño variable: la tabla
declara un máximo y **una variable dice cuántos elementos son válidos ahora**. Es exactamente el
patrón "array más contador" que C usa, con la ventaja de que aquí la relación está **declarada** y el
compilador puede comprobar los límites con `SSRANGE`.

Y COBOL tiene una operación sobre tablas que sí es de alto nivel y conviene conocer:

```cobol
SEARCH VENTA VARYING I
    AT END DISPLAY "no encontrado"
    WHEN VENTA(I) > LIMITE DISPLAY "encontrado en " I
END-SEARCH

SEARCH ALL VENTA                    *> búsqueda BINARIA, si la tabla está ordenada
    WHEN CLAVE(I) = BUSCADA ...
```

`SEARCH ALL` hace una búsqueda binaria sobre una tabla declarada con `ASCENDING KEY`. Es un algoritmo
completo dentro del lenguaje, en 1968.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program suma_lista
   implicit none
   character(len=1000) :: linea
   integer :: valores(200), n, i, total, ios

   read(*, '(A)') linea

   !  Cuántos valores hay en la línea: se prueba a leer 1, 2, 3... hasta fallar.
   n = 0
   do i = 1, 200
      read(linea, *, iostat=ios) valores(1:i)
      if (ios /= 0) exit
      n = i
   end do

   total = 0
   do i = 1, n
      total = total + valores(i)
   end do

   write(*, '(A,I0)') 'suma=', total
end program suma_lista
```

**Lo que esta clase enseña en Fortran.** El bucle que cuenta los valores es el **idioma clásico de
Fortran para "no sé cuántos hay en esta línea"**, y merece explicación porque es raro visto desde
fuera: se intenta leer 1 valor, luego 2, luego 3, y se para cuando la lectura falla. `iostat=ios`
captura el error en lugar de abortar.

Es O(n²) y nadie lo defendería hoy, y sin embargo aparece en código científico real, porque el
sistema de E/S de Fortran está diseñado para **registros de forma conocida**, no para líneas de
longitud arbitraria. Cuando el fichero tiene una cabecera que dice cuántos valores vienen —que es lo
normal en los formatos científicos— el problema no existe.

Lo que Fortran sí tiene, y es su gran aportación a esta clase, es que **el bucle sobre la colección
casi nunca hace falta**:

```fortran
total = sum(valores(1:n))              ! sin bucle
media = sum(v) / size(v)
mayor = maxval(v)
donde = maxloc(v)                      ! la POSICIÓN del máximo
cuantos = count(v > 0)                 ! cuántos cumplen
todos = all(v > 0)                     ! ¿todos?
alguno = any(v < 0)                    ! ¿alguno?
```

`sum`, `product`, `maxval`, `minval`, `maxloc`, `count`, `all`, `any`, `dot_product`, `matmul` —
todas operan sobre arrays completos y todas se vectorizan. En Fortran, **recorrer un array a mano es
casi siempre un síntoma de que no conoces la intrínseca que hace eso**.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Suma_Lista is
   Linea  : String (1 .. 500);
   Ultimo : Natural;
   Pos    : Positive := 1;
   Fin    : Positive;
   Valor  : Integer;
   Total  : Integer := 0;
begin
   Get_Line (Linea, Ultimo);

   while Pos <= Ultimo loop
      --  Get sobre una PORCIÓN de cadena: devuelve el valor y hasta dónde leyó.
      Get (Linea (Pos .. Ultimo), Valor, Fin);
      Total := Total + Valor;
      Pos := Fin + 1;
   end loop;

   Put ("suma="); Put (Total, Width => 1); New_Line;
end Suma_Lista;
```

**Lo que esta clase enseña en Ada.** `Get (From : String; Item : out Integer; Last : out Positive)`
es una forma de lectura que casi ningún lenguaje ofrece: **analiza un valor a partir de una cadena y
devuelve hasta dónde ha llegado**. Con eso, recorrer una línea de valores es avanzar `Pos` hasta el
final, sin partir la cadena ni reservar memoria.

Es el mismo mecanismo que `std::from_chars` de C++17, disponible desde 1983.

Pero la aportación de Ada a esta clase llegó con **Ada 2012** y sus **interfaces de iterador**, que
permiten que **cualquier tipo tuyo** se recorra con `for ... of`:

```ada
for Elemento of Mi_Coleccion loop ... end loop;
```

Para que eso funcione, el tipo declara el aspecto `Iterable` o implementa `Ada.Iterator_Interfaces`,
con `First`, `Next` y `Has_Element`. Es exactamente el mismo contrato que `IEnumerable` en C#,
`Iterator` en Java o `begin`/`end` en C++.

Y Ada 2022 fue más lejos con las **expresiones de agregado iteradas**, que son comprensiones de
listas:

```ada
Cuadrados : constant Vector := [for I in 1 .. 10 => I * I];
```

Un lenguaje de 1983 incorporando comprensiones en 2022 es, otra vez, el argumento de esta sección
entera: **no son fotos fijas**.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program SumaLista;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  Linea, Token: string;
  I, Total: Integer;

begin
  ReadLn(Linea);
  Linea := Trim(Linea) + ' ';

  Total := 0;
  Token := '';
  for I := 1 to Length(Linea) do
  begin
    if Linea[I] = ' ' then
    begin
      if Token <> '' then
      begin
        Total := Total + StrToInt(Token);
        Token := '';
      end;
    end
    else
      Token := Token + Linea[I];
  end;

  WriteLn('suma=', IntToStr(Total));
end.
```

**Lo que esta clase enseña en Pascal.** El Pascal ISO **no tiene función de partir cadenas**, así que
el tokenizador se escribe a mano. Es una carencia real y muy visible en cuanto se procesa texto.

Free Pascal y Delphi lo resolvieron por dos vías distintas, y conviene conocer las dos porque
aparecen en código de épocas diferentes:

```pascal
{ 1) TStringList con delimitador: la forma clásica de Delphi }
Lista := TStringList.Create;
try
  Lista.Delimiter := ' ';
  Lista.DelimitedText := Linea;
  for I := 0 to Lista.Count - 1 do
    Total := Total + StrToInt(Lista[I]);
finally
  Lista.Free;
end;

{ 2) Ayudantes de tipo, en Delphi moderno }
for S in Linea.Split([' ']) do ...
```

Fíjate en el `try..finally` de la primera: **`TStringList` es un objeto y hay que liberarlo**, con la
disciplina de la clase 042. Ese bloque es el idioma más repetido del código Delphi del mundo.

Y `for..in` sobre colecciones llegó a Free Pascal y Delphi en 2005, con el mismo contrato que los
demás: el tipo implementa `GetEnumerator` y devuelve un objeto con `MoveNext` y `Current`. Es el
patrón que C# había estrenado poco antes, y que Ada, C++ y Java tienen con otros nombres. **Los cinco
llegaron a la misma solución.**

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let ((total 0))
  (loop for valor = (read *standard-input* nil :fin)
        until (eq valor :fin)
        do (incf total valor))
  (format t "suma=~D~%" total))
```

**Lo que esta clase enseña en Common Lisp.** `(read stream nil :fin)` es la lectura con **valor
centinela**: en lugar de señalar un error al llegar al final, devuelve el objeto que le indiques.
Aquí, la palabra clave `:fin`, que no puede confundirse con ningún número.

Es el mismo patrón que `iostat` en Fortran y que comprobar el flujo en C++, y es la primera pieza de
esta clase: **cómo sabe el bucle que ya no hay más**.

La segunda pieza es que Lisp tiene **funciones de secuencia genéricas** que funcionan igual sobre
listas, vectores y cadenas —lo que ya se vio en la clase 048—:

```lisp
(reduce #'+ lista)                    ; suma
(count-if #'evenp lista)              ; cuántos pares
(find-if (lambda (x) (> x 100)) lista)
(position 42 lista)
(some #'minusp lista)                 ; ¿alguno negativo?  cortocircuita
(every #'plusp lista)
(map 'vector #'1+ lista)              ; el TIPO del resultado como argumento
```

`some` y `every` **cortocircuitan**, al contrario que `any`/`all` de PL/I sobre cadenas de bits.

Y `loop` tiene cláusulas de acumulación que hacen innecesaria la variable manual de este programa:

```lisp
(loop for x in lista sum x)
(loop for x in lista when (evenp x) collect x)
(loop for x in lista maximize x)
(loop for x in lista count (plusp x))
```

`sum`, `collect`, `maximize`, `minimize`, `count`, `append` y `nconc` son parte del mini-lenguaje de
`loop`, y cubren casi todo lo que en otros lenguajes exige `map`/`filter`/`reduce`.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea

set total 0
foreach v [split [string trim $linea]] {
    incr total $v
}

puts "suma=$total"
```

**Lo que esta clase enseña en Tcl.** `foreach` es el recorrido de colección de Tcl, y tiene dos
formas que casi ningún lenguaje ofrece:

```tcl
foreach {clave valor} $lista { ... }        ;# de DOS en dos
foreach a $lista1 b $lista2 { ... }         ;# dos listas EN PARALELO
foreach a $l1 {b c} $l2 { ... }             ;# ¡y con tamaños de grupo distintos!
```

Recorrer una lista de pares clave-valor de dos en dos, o dos listas a la vez, son operaciones que en
C++ exigen iteradores manuales y en Python el `zip`. Aquí son argumentos adicionales del mismo
comando.

Y `split` es la contrapartida de `join`: convierte una cadena en lista partiendo por los caracteres
que indiques. **Sin argumento, parte por espacios en blanco**, que es lo que hace este programa.

Un aviso que conviene tener presente: `split` **con** un delimitador explícito produce elementos
vacíos si hay separadores consecutivos:

```tcl
split "a,,b" ","          ;# -> {a {} b}   -- tres elementos, uno vacío
split "a  b"              ;# -> {a {} b}   -- ¡también!
split [string trim "a  b"] " "  ;# sigue dando el vacío
```

Por eso este programa usa `split` **sin argumento** sobre la cadena recortada, que colapsa las rachas
de espacios. Es la misma diferencia que en COBOL entre `DELIMITED BY SPACE` y `DELIMITED BY ALL
SPACES`, y en Perl entre `split /,/` y `split ' '`.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;
use List::Util qw(sum0);

my $linea = <STDIN>;
chomp $linea;

my $total = sum0(split ' ', $linea);

print "suma=$total\n";
```

**Lo que esta clase enseña en Perl.** `sum0(split ' ', $linea)` es toda la solución: partir y sumar,
sin bucle y sin variable acumuladora.

`List::Util` está en el núcleo desde 2001 y sus funciones están escritas en C:

```perl
use List::Util qw(sum sum0 max min first any all none reduce shuffle uniq);

sum @v            # undef si la lista está vacía
sum0 @v           # 0 si está vacía  <- casi siempre lo que quieres
first { $_ > 100 } @v      # cortocircuita
reduce { $a + $b } @v      # el plegado general
```

La distinción entre `sum` y `sum0` es la clase 053 aplicada aquí: **"no hay elementos" y "la suma es
cero" son cosas distintas**, y Perl te deja elegir cuál devuelve.

Y el recorrido idiomático es `foreach`, con la propiedad que ya apareció en la clase 064 y que
conviene recordar porque es peligrosa y útil a partes iguales:

```perl
for my $x (@lista) { $x *= 2 }      # MODIFICA @lista: $x es un ALIAS
for my $x (@lista) { my $y = $x * 2 }   # sin tocar el original
```

La variable del bucle **no es una copia**, es una referencia al elemento real. En Python o Java eso
no ocurre. Ada lo hace igual con `for E of` cuando el elemento no es constante, y C++ solo si escribes
`auto&`.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>
#include <iterator>
#include <numeric>
#include <sstream>
#include <string>
#include <vector>

int main() {
    std::string linea;
    if (!std::getline(std::cin, linea)) return 1;

    std::istringstream iss(linea);
    const std::vector<int> valores{std::istream_iterator<int>(iss),
                                   std::istream_iterator<int>()};

    const int total = std::accumulate(valores.begin(), valores.end(), 0);

    std::cout << "suma=" << total << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** Este programa construye el vector **directamente desde un par de
iteradores de flujo**, sin bucle de lectura. `std::istream_iterator<int>(iss)` es un iterador que, al
avanzar, lee el siguiente entero; el construido sin argumentos representa el final.

Ese es el diseño de la **STL** de Alexander Stepanov, y es la aportación conceptual de C++ a esta
clase: **los algoritmos no conocen los contenedores, conocen iteradores**.

```cpp
std::accumulate(v.begin(), v.end(), 0);        // sobre un vector
std::accumulate(l.begin(), l.end(), 0);        // sobre una lista enlazada
std::accumulate(s.begin(), s.end(), 0);        // sobre un conjunto
std::accumulate(it_flujo, it_fin, 0);          // ¡sobre un FLUJO de entrada!
```

**El mismo algoritmo, sin recompilar nada distinto, sobre cuatro estructuras que no se parecen en
nada.** Un contenedor solo tiene que ofrecer iteradores; un algoritmo solo tiene que pedirlos. Esa
separación en tres piezas —contenedores, iteradores, algoritmos— es la idea que después copiaron los
`Stream` de Java, los `IEnumerable` de C# y los `Iterator` de Rust.

C++20 la refinó con los **rangos**, que evitan tener que escribir `begin()` y `end()`:

```cpp
#include <ranges>
const int total = std::ranges::fold_left(valores, 0, std::plus{});
```

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

dcl-pi SUMALIS;
  linea varchar(200) const;
end-pi;

dcl-s trozos varchar(20) dim(50);
dcl-s cuantos int(10);
dcl-s i       int(10);
dcl-s total   int(20) inz(0);
dcl-s salida  char(40);

trozos = %split(linea : ' ');
cuantos = %elem(trozos);

for i = 1 to cuantos;
  total += %int(trozos(i));
endfor;

salida = 'suma=' + %char(total);
dsply salida;

*inlr = *on;
return;
```

**Lo que esta clase enseña en RPG.** `%split` —que parte una cadena y devuelve una **matriz**— se
añadió en **IBM i 7.4, en 2019**. Durante cincuenta años, partir una cadena en RPG se hacía con un
bucle y `%scan`. Es otro recordatorio de que estos lenguajes siguen recibiendo funcionalidad.

Pero el recorrido de colecciones **de verdad** en RPG no es sobre matrices: es sobre **ficheros de
base de datos**, y ahí está la aportación de esta clase.

```rpgle
dcl-f CLIENTES usage(*input) keyed;

setll *loval CLIENTES;        // posicionarse al principio
read CLIENTES;
dow not %eof(CLIENTES);
  total += CLI_SALDO;         // los campos son VARIABLES del programa
  read CLIENTES;
enddo;
```

`setll` (*set lower limit*), `read`, `reade` (leer mientras la clave coincida), `chain` (búsqueda
directa) y `%eof` son el vocabulario de recorrido, y operan sobre **millones de registros sin
cargarlos en memoria**. Es un iterador perezoso sobre una base de datos, integrado en el lenguaje.

Y en el RPG clásico ni siquiera eso se escribía: con un fichero declarado como **entrada primaria**,
el **ciclo del programa** hacía el `read` y el `dow` por ti. Tú solo escribías qué hacer con cada
registro. Es exactamente la inversión de control de la clase 063.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 suma_lista: procedure options(main);

    declare linea  character(200) varying;
    declare trozo  character(20)  varying;
    declare total  fixed binary(31) initial(0);
    declare (i, p) fixed binary(31);

    get edit (linea) (a(200));
    linea = trim(linea) || ' ';

    p = 1;
    do i = 1 to length(linea);
       if substr(linea, i, 1) = ' ' then do;
          if i > p then do;
             trozo = substr(linea, p, i - p);
             total = total + trozo;      /* conversión implícita texto->número */
          end;
          p = i + 1;
       end;
    end;

    put skip list ('suma=' || trim(char(total)));

 end suma_lista;
```

**Lo que esta clase enseña en PL/I.** Fíjate en `total = total + trozo`: **`trozo` es una cadena de
caracteres y se suma a un entero sin ninguna conversión escrita**. Es la conversión implícita de la
clase 050, aquí en su versión más cómoda y más peligrosa: funciona perfectamente hasta que el texto
no es un número, y entonces levanta la condición `CONVERSION`.

Sobre el recorrido de colecciones, PL/I tiene arrays de primera clase con operaciones sobre el
conjunto, igual que Fortran:

```pli
declare v(100) fixed binary(31);

total = sum(v);              /* sin bucle */
mayor = max(v);
v = v * 2;                   /* opera sobre TODO el array */
v(10:20) = 0;                /* una PORCIÓN */
if any(v > 100) then ...
```

Que un lenguaje de negocio de 1964 tuviera aritmética de arrays completos es notable, y es la
influencia directa de FORTRAN en su diseño — recuerda que PL/I nació para unir los dos mundos.

Lo que no tiene es un iterador abstracto: no hay forma de recorrer una estructura definida por el
usuario con una construcción genérica. Para eso hay que esperar a los lenguajes con tipos abstractos
de datos, que es lo que trajo Ada en 1983 y CLU un poco antes.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
SUMA ; Suma de una lista -- clase 065
 read linea
 set total = 0
 for i = 1:1:$length(linea, " ") do
 . set total = total + $piece(linea, " ", i)
 write "suma=", total, !
 quit
```

**Lo que esta clase enseña en M.** `$length(linea, " ")` cuenta **cuántos trozos** hay, y `$piece`
extrae el *i*-ésimo. Es el recorrido de la "colección ligera" de M: una cadena con delimitadores.

Pero la aportación real de M a esta clase es **`$order`**, que recorre un árbol de la base de datos
**sin cargarlo en memoria**:

```mumps
 set clave = ""
 for  set clave = $order(^VENTAS(clave))  quit:clave = ""  do
 . set total = total + ^VENTAS(clave)
```

`$order(^VENTAS(clave))` devuelve **la siguiente clave existente en orden**, y la cadena vacía cuando
no queda ninguna. Con eso se recorre un *global* de **diez millones de nodos** consumiendo memoria
constante, porque cada llamada es una búsqueda en el índice del árbol B en disco.

Eso es un **iterador perezoso sobre una base de datos**, con una sola función y sin cursor que abrir
ni cerrar. Y funciona en cualquier nivel de subíndice y en cualquier dirección:

```mumps
 set fecha = $order(^CITAS(pac, fecha), -1)     ; la ANTERIOR: recorrido inverso
 set sig = $query(^CITAS(pac))                  ; el siguiente nodo con VALOR, a cualquier profundidad
```

`$query` recorre el árbol entero en profundidad, saltando de nodo a nodo con independencia del número
de subíndices. Es el recorrido completo de una estructura jerárquica en una llamada — y es la razón
de que un sistema clínico en M pueda listar el historial de un paciente sin ningún ORM.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| total |

total := (stdin nextLine substrings collect: [ :cada | cada asNumber ])
    inject: 0 into: [ :acc :cada | acc + cada ].

Transcript show: 'suma=', total printString; cr.
```

**Lo que esta clase enseña en Smalltalk.** `inject:into:` es el **plegado** —el `reduce` de la clase
068— y aquí resuelve la suma sin bucle ni acumulador visible: `0` es el valor inicial y el bloque
recibe el acumulado y el elemento.

Pero lo que hay que ver en esta clase es de dónde sale: **`inject:into:` está implementado en
`Collection`, en términos de `do:`**, y `do:` es lo único que una colección tiene que saber hacer:

```smalltalk
Collection >> inject: valorInicial into: unBloque
    | acumulado |
    acumulado := valorInicial.
    self do: [ :cada | acumulado := unBloque value: acumulado value: cada ].
    ^ acumulado
```

Y con `do:` implementado, una subclase hereda **gratis** todo el protocolo: `collect:`, `select:`,
`reject:`, `detect:`, `inject:into:`, `anySatisfy:`, `allSatisfy:`, `sum`, `max`, `sorted`,
`asOrderedCollection`, `groupedBy:`, `count:`… más de cien métodos.

Ese es el patrón del **método plantilla** en su forma más pura: define una operación primitiva y
recibe el resto. Es la misma economía que la STL de C++ obtiene con iteradores y que Rust obtiene con
el *trait* `Iterator` y sus métodos por defecto — tres soluciones distintas al mismo problema de
diseño, y esta es la más antigua.

Para colecciones grandes o infinitas, Pharo tiene además `ReadStream` y `Generator`, que se ven en la
clase siguiente.

---

## Y de vuelta a la clase

Lo transferible es la pregunta **"¿quién sabe cuándo termina el recorrido?"**. Si la respuesta es "una
variable contador que llevo yo", el código es frágil: basta con que alguien inserte un elemento sin
actualizarla. Si la respuesta es "la colección", el recorrido es correcto por construcción. Toda la
evolución que va del `DO 100 I = 1, N` de Fortran al `for x of coleccion` de Ada 2012 y al
`for (auto& x : v)` de C++11 es el traslado de esa responsabilidad del programador a la estructura.

⏮️ [Volver a la clase 065](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
