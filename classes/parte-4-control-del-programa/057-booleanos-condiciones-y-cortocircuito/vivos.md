# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 057

> [⬅️ Volver a la clase 057](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Dos preguntas sobre un número y la conjunción de ambas. Lo que parece trivial esconde la pregunta
que abre toda la Parte 4: **cuando escribes `A y B`, ¿se evalúa siempre `B`?** Si `B` es una simple
comparación da igual; si `B` accede a una posición de un array, llama a una función o lee un fichero,
la respuesta decide entre un programa correcto y una excepción.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es el **cortocircuito**, y estos lenguajes lo enseñan porque **no lo dan por
> supuesto**. En C, Java o Python, `&&` cortocircuita y no hay elección; en **Ada** hay cuatro
> operadores —`and`, `or`, `and then`, `or else`— y hay que decidir en cada uso. En **Fortran** el
> estándar **no garantiza** el cortocircuito y el compilador puede evaluar los dos lados. En **PL/I**
> `&` es una operación sobre bits que siempre evalúa ambos.
>
> Y en **Smalltalk** el cortocircuito no es una regla del lenguaje: es la consecuencia de que `and:`
> reciba **un bloque** en lugar de un valor. Ver esa diferencia es entender de dónde sale el
> comportamiento que en los demás lenguajes viene dado.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: un entero `n` → stdout: `positivo=<true|false> par=<true|false> ambos=<true|false>`
- **Regla:** `positivo = n>0 ; par = n%2==0 ; ambos = positivo && par`

| stdin | esperado |
|---|---|
| `4` | `positivo=true par=true ambos=true` |
| `-3` | `positivo=false par=false ambos=false` |
| `7` | `positivo=true par=false ambos=false` |

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
PROGRAM-ID. CONDICIONES.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  N       PIC S9(9) COMP-3.
01  R-POS   PIC X(5).
01  R-PAR   PIC X(5).
01  R-AMB   PIC X(5).

PROCEDURE DIVISION.
    ACCEPT LINEA
    MOVE FUNCTION NUMVAL(LINEA) TO N

    IF N > 0
        MOVE "true"  TO R-POS
    ELSE
        MOVE "false" TO R-POS
    END-IF

    IF FUNCTION MOD(N, 2) = 0
        MOVE "true"  TO R-PAR
    ELSE
        MOVE "false" TO R-PAR
    END-IF

    IF N > 0 AND FUNCTION MOD(N, 2) = 0
        MOVE "true"  TO R-AMB
    ELSE
        MOVE "false" TO R-AMB
    END-IF

    DISPLAY "positivo=" FUNCTION TRIM(R-POS)
            " par=" FUNCTION TRIM(R-PAR)
            " ambos=" FUNCTION TRIM(R-AMB)
    STOP RUN.
```

**Lo que esta clase enseña en COBOL.** El estándar **no obliga** al cortocircuito: el compilador
puede evaluar las dos partes de un `AND`. En la práctica los compiladores modernos cortocircuitan,
pero **no se puede depender de ello** en código portable, así que la comprobación de índice se escribe
anidada:

```cobol
IF I <= MAXIMO
    IF TABLA(I) = BUSCADO
        ...
    END-IF
END-IF
```

Lo que COBOL sí tiene, y no tiene casi nadie, son las **condiciones abreviadas**, que permiten
escribir una comparación una vez y encadenar varios valores:

```cobol
IF ESTADO = "A" OR "B" OR "C"          *> implícito: ESTADO = "A" OR ESTADO = "B"...
IF N > 0 AND < 100                     *> implícito: N > 0 AND N < 100
IF SALDO NOT = ZERO AND NOT = SPACES
```

Se lee casi como se diría en voz alta, que era el objetivo del lenguaje. Y también es una fuente de
confusión: `IF A = 1 OR 2` no pregunta "¿A es 1 o 2 es cierto?", pregunta "¿A es 1 o A es 2?". En un
lenguaje donde el `OR` fuera sobre booleanos, la primera lectura sería la correcta.

Fíjate también en que COBOL admite **comparar rangos con `THRU` en `EVALUATE`** y las clases del
lenguaje —`IF N IS NUMERIC`, `IF C IS ALPHABETIC`, `IF X IS POSITIVE`—, que son predicados
incorporados y ahorran la comparación explícita.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program condiciones
   implicit none
   integer :: n
   logical :: positivo, par

   read(*, *) n
   positivo = n > 0
   par = mod(n, 2) == 0

   write(*, '(A,A,A,A,A,A)') 'positivo=', trim(tf(positivo)), &
                             ' par=', trim(tf(par)), &
                             ' ambos=', trim(tf(positivo .and. par))
contains

   function tf(v) result(s)
      logical, intent(in) :: v
      character(len=5) :: s
      s = merge('true ', 'false', v)
   end function tf

end program condiciones
```

**Lo que esta clase enseña en Fortran.** Es el caso más claro de toda la página: **el estándar de
Fortran no garantiza el cortocircuito, y además permite evaluar los operandos en cualquier orden.**
El compilador puede evaluar el segundo primero, o los dos a la vez si eso vectoriza mejor.

Esa libertad es deliberada y tiene sentido en su dominio: en un bucle que se ejecuta mil millones de
veces, obligar a un orden impide reordenar y vectorizar. Fortran prefiere el rendimiento y traslada
la responsabilidad al programador.

La consecuencia práctica es directa: **este patrón está mal en Fortran**.

```fortran
if (i <= n .and. v(i) == buscado) then     ! MAL: v(i) puede evaluarse con i fuera de rango
```

Y la forma correcta es anidar, exactamente como en COBOL:

```fortran
if (i <= n) then
   if (v(i) == buscado) then
      ...
```

Es más verboso y es lo único seguro. Quien llega desde C y da por hecho el cortocircuito escribe
código que funciona en un compilador y falla en otro — o peor, funciona con `-O0` y falla con `-O2`.

Fortran compensa con operadores que otros no tienen: `.eqv.` (equivalencia) y `.neqv.` (o exclusivo),
y `merge`, que sobre arrays aplica la condición **elemento a elemento** sin ningún bucle.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Condiciones is

   function Tf (V : Boolean) return String is
     (if V then "true" else "false");

   N             : Integer;
   Positivo, Par : Boolean;
begin
   Get (N);
   Positivo := N > 0;
   Par      := N mod 2 = 0;

   Put_Line ("positivo=" & Tf (Positivo) &
             " par=" & Tf (Par) &
             " ambos=" & Tf (Positivo and then Par));
end Condiciones;
```

**Lo que esta clase enseña en Ada.** Ada es el único lenguaje de esta página que **obliga a elegir**,
con cuatro operadores en lugar de dos:

| Operador | Evalúa el segundo operando |
|---|---|
| `and` | **Siempre** |
| `or` | **Siempre** |
| `and then` | Solo si el primero es cierto |
| `or else` | Solo si el primero es falso |

Y esa elección es **parte de la corrección**, no una preferencia de estilo:

```ada
if I <= Ultimo and then Tabla (I) = Buscado then   --  correcto
if I <= Ultimo and      Tabla (I) = Buscado then   --  Constraint_Error si I se pasa
```

En C escribes `&&` sin pensarlo y funciona. En Ada tienes que escribir `and then`, y al escribirlo
declaras que **el segundo operando depende del primero**. Es información que en C queda implícita en
la elección entre `&&` y `&`, y que aquí está en el texto.

Ada añade además una tercera forma que casi ningún lenguaje tiene y que resuelve esta clase de una
manera distinta: los **cuantificadores** sobre rangos y contenedores.

```ada
if (for all I in Tabla'Range => Tabla (I) > 0) then ...
if (for some I in Tabla'Range => Tabla (I) = Buscado) then ...
```

Son expresiones booleanas del lenguaje, no bucles, y —lo importante— **se pueden usar dentro de un
contrato `Pre`/`Post`**, donde SPARK las demuestra estáticamente. La condición deja de ser algo que se
comprueba y pasa a ser algo que se prueba.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Condiciones;
{$MODE OBJFPC}{$H+}

function Tf(V: Boolean): string;
begin
  if V then Result := 'true' else Result := 'false';
end;

var
  N: Integer;
  Positivo, Par: Boolean;

begin
  Read(N);
  Positivo := N > 0;
  Par := (N mod 2) = 0;

  WriteLn('positivo=', Tf(Positivo),
          ' par=', Tf(Par),
          ' ambos=', Tf(Positivo and Par));
end.
```

**Lo que esta clase enseña en Pascal.** El Pascal ISO **no garantiza** el cortocircuito, igual que
Fortran y COBOL. Pero Free Pascal y Delphi lo controlan con una **directiva de compilador**, que es
una solución propia y muy explícita:

```pascal
{$B-}   { evaluación PEREZOSA: cortocircuita. Es el valor por defecto }
{$B+}   { evaluación COMPLETA: evalúa siempre los dos operandos }
```

Que sea una directiva y no dos operadores tiene una consecuencia incómoda: **el significado de `and`
depende de una línea que puede estar en otro fichero**, incluida por una unidad. Un mismo código
fuente se comporta distinto según cómo se compile. Ada resolvió el mismo problema poniendo la
decisión en el operador, donde se lee.

En la práctica, `{$B-}` es lo universal y el cortocircuito funciona. Pero código antiguo portado de
Turbo Pascal puede depender de lo contrario.

Y esta clase vuelve a tropezar con la trampa de precedencia de la clase 046: **`and` tiene más
precedencia que las comparaciones**, así que los paréntesis de `(N mod 2) = 0` y de
`(A > 0) and (B > 0)` son obligatorios. Es la herencia de haber unificado los operadores lógicos con
los de bits, y la razón de que el código Pascal esté lleno de paréntesis que en C sobrarían.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(flet ((tf (v) (if v "true" "false")))
  (let* ((n (read))
         (positivo (> n 0))
         (par (evenp n)))
    (format t "positivo=~A par=~A ambos=~A~%"
            (tf positivo) (tf par) (tf (and positivo par)))))
```

**Lo que esta clase enseña en Common Lisp.** `and` y `or` **son macros, no funciones**, y toda la
clase cabe en esa frase. Una función recibe sus argumentos ya evaluados; una macro recibe **el
código sin evaluar** y decide qué hacer con él. Por eso `and` puede parar en el primer `nil`: no le
llegaron valores, le llegaron expresiones.

La expansión es literalmente una cadena de `if`:

```lisp
(and a b c)   ; se expande a:  (if a (if b c nil) nil)
(or a b c)    ; se expande a:  (let ((x a)) (if x x (or b c)))
```

Puedes comprobarlo con `(macroexpand-1 '(and a b))`. **El cortocircuito no es una regla del
lenguaje: es lo que hace esa expansión**, y está escrita en código que se puede leer.

De ahí se sigue algo que los lenguajes con cortocircuito integrado no permiten: **puedes escribir tus
propios operadores de control**.

```lisp
(defmacro si-todo (&rest formas)
  (if (null (cdr formas))
      (car formas)
      `(if ,(car formas) (si-todo ,@(cdr formas)) nil)))
```

Y ojo con `and` devolviendo un **valor** en vez de un booleano: `(and 1 2 3)` da `3`, y
`(or nil "x")` da `"x"`. Es lo que permite el idioma
`(or (buscar-cache) (buscar-disco) "por-defecto")`, que JavaScript y Python copiaron después.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
proc tf {v} { return [expr {$v ? "true" : "false"}] }

gets stdin linea
set n [string trim $linea]

set positivo [expr {$n > 0}]
set par [expr {$n % 2 == 0}]

puts "positivo=[tf $positivo] par=[tf $par] ambos=[tf [expr {$positivo && $par}]]"
```

**Lo que esta clase enseña en Tcl.** `&&` y `||` **sí cortocircuitan** dentro de `expr`, con la
semántica de C. Pero hay un detalle propio de Tcl que esta clase es el sitio para explicar: **el
cortocircuito solo funciona si la expresión va entre llaves**.

```tcl
expr {$a && [funcion_cara]}     ;# cortocircuita: funcion_cara solo se llama si $a es cierto
expr "$a && [funcion_cara]"     ;# NO: la sustitución ocurre ANTES, la función se llama SIEMPRE
```

Sin llaves, Tcl sustituye los corchetes —ejecutando el comando— antes de que `expr` vea la
expresión. Cuando `expr` recibe el texto, la llamada ya ocurrió. El cortocircuito se pierde no por la
semántica del operador, sino por **el orden de las sustituciones**.

Es la tercera razón para la regla de "`expr` siempre con llaves", después del rendimiento y de la
inyección que aparecieron en las clases 041 y 055. Tres motivos distintos, una sola regla.

Y como `expr` **devuelve `1` o `0`**, no `true`/`false`, este programa necesita `tf` para traducir —
igual que en las clases 043 y 046.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

sub tf { return $_[0] ? 'true' : 'false' }

my $n = <STDIN>;
chomp $n;

my $positivo = $n > 0;
my $par = ($n % 2 == 0);

printf "positivo=%s par=%s ambos=%s\n",
       tf($positivo), tf($par), tf($positivo && $par);
```

**Lo que esta clase enseña en Perl.** `&&` y `||` cortocircuitan, y **devuelven el último valor
evaluado**, no un booleano — lo mismo que en Lisp. Eso convierte el cortocircuito en una herramienta
de expresión, no solo de control:

```perl
my $nombre = $usuario->{nombre} || 'anónimo';
my $puerto = $config{puerto} // 8080;          # // mira DEFINIDO, no verdadero
abrir($f) or die "no puedo abrir: $!";         # `or`, con precedencia baja
```

La tercera línea es el idioma más característico de Perl y usa `or` en lugar de `||` **a propósito**:
`or` tiene precedencia más baja que la asignación, así que funciona como control de flujo al final de
una sentencia. Con `||` habría que poner paréntesis. Son los dos juegos de operadores lógicos de la
clase 046, aplicados aquí a su uso real.

Y hay un detalle de esta clase que Perl hace de forma única: **el operador de comparación
encadenada no existe, pero `..` sí tiene un comportamiento con estado**. En contexto escalar, `..` es
el *operador de rango biestable*: recuerda si ya se activó, y sirve para procesar "desde la línea que
casa esto hasta la que casa aquello":

```perl
while (<>) {
    print if /^INICIO/ .. /^FIN/;    # imprime el bloque entre ambas marcas
}
```

Es un operador con memoria entre iteraciones, heredado de `sed` y `awk`, y no tiene equivalente en
ningún otro lenguaje de esta página.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>

int main() {
    int n{};
    if (!(std::cin >> n)) return 1;

    const bool positivo = n > 0;
    const bool par = (n % 2 == 0);

    std::cout << std::boolalpha
              << "positivo=" << positivo
              << " par=" << par
              << " ambos=" << (positivo && par) << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** `&&` y `||` cortocircuitan y —esto es lo importante—
**establecen un punto de secuencia**: el estándar garantiza que el primer operando se evalúa
completamente, con todos sus efectos laterales, **antes** de decidir si evalúa el segundo. Es una de
las pocas garantías fuertes de orden que da el lenguaje, y por eso `if (p && p->campo)` es correcto.

Compara con la coma o con los argumentos de una función, donde el orden **no** estaba especificado
hasta C++17 y todavía hoy es un terreno resbaladizo.

Y hay una trampa específica de C++ que esta clase debe nombrar: **`&&` y `||` se pueden
sobrecargar**, y si una clase lo hace, **el cortocircuito desaparece**.

```cpp
struct Cond { bool v; };
bool operator&&(Cond a, Cond b);   // legal... y desastroso
```

Al convertirse en una llamada a función normal, los dos argumentos se evalúan siempre. Por eso las
guías —incluidas las *Core Guidelines*— dicen sin matices: **nunca sobrecargues `&&`, `||` ni la
coma**, porque cambias una garantía del lenguaje que todo el mundo da por supuesta.

C++17 añadió además `if constexpr`, que es cortocircuito **en tiempo de compilación**: la rama no
tomada ni siquiera se compila, lo que permite escribir código genérico que solo es válido para
algunos tipos.

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

dcl-pi CONDIC;
  n int(10) const;
end-pi;

dcl-s positivo ind;
dcl-s par      ind;
dcl-s salida   char(70);

positivo = (n > 0);
par = (%rem(n : 2) = 0);

salida = 'positivo=' + tf(positivo)
       + ' par=' + tf(par)
       + ' ambos=' + tf(positivo and par);
dsply salida;

*inlr = *on;
return;

dcl-proc tf;
  dcl-pi *n varchar(5);
    v ind const;
  end-pi;
  if v = *on;
    return 'true';
  endif;
  return 'false';
end-proc;
```

**Lo que esta clase enseña en RPG.** RPG **sí cortocircuita** `and` y `or`, con la semántica
habitual. Lo interesante de esta clase en RPG es histórico: **antes de que existieran los booleanos
con nombre, todo el control de flujo iba por los indicadores del ciclo**.

```rpgle
     C     CANTIDAD      COMP      LIMITE                        101112
```

Esa línea de RPG en formato fijo compara y enciende **tres indicadores a la vez** según el resultado
—`*IN10` si es mayor, `*IN11` si es menor, `*IN12` si es igual—, y el resto del programa consultaba
esos números. La condición no tenía nombre; tenía un número, y saber qué significaba `*IN11` exigía
leer todo el programa.

El RPG libre de hoy —`if cantidad > limite;`— es el mismo movimiento que hizo COBOL con los niveles
88: **dar nombre a la condición**. Y la razón de que `dcl-s x ind` se llame *indicator* y valga
`*on`/`*off` en vez de `true`/`false` es exactamente esa herencia.

Es la mejor ilustración de un patrón que se repite en toda esta sección: los lenguajes viejos no son
peores porque les falte algo, son **capas geológicas** donde conviven la forma de 1959 y la de 2013,
y el código real mezcla las dos.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 condiciones: procedure options(main);

    declare n             fixed binary(31);
    declare (positivo, par) bit(1);

    get list (n);
    positivo = (n > 0);
    par      = (mod(n, 2) = 0);

    put skip list ('positivo=' || tf(positivo) ||
                   ' par='     || tf(par)      ||
                   ' ambos='   || tf(positivo & par));

 tf: procedure (v) returns (character(5) varying);
    declare v bit(1);
    if v then return ('true');
    return ('false');
 end tf;

 end condiciones;
```

**Lo que esta clase enseña en PL/I.** **`&` y `|` en PL/I no cortocircuitan, y no pueden hacerlo**,
porque no son operadores de control: son **operaciones sobre cadenas de bits**. `'1100'b & '1010'b`
da `'1000'b`, operando bit a bit. Sobre `bit(1)` eso resulta ser la lógica booleana, pero la
naturaleza de la operación es otra.

La consecuencia es la de siempre, y aquí es inevitable:

```pli
if i <= n & tabla(i) = buscado then    /* MAL: tabla(i) se evalúa SIEMPRE */

if i <= n then                          /* la única forma correcta */
   if tabla(i) = buscado then
      ...
```

Es exactamente el mismo problema de Fortran y COBOL, y explica **por qué C separó `&` de `&&`**.
Dennis Ritchie venía de este mundo: había visto que unificar la lógica con los bits obliga a anidar
`if` en todas partes, y decidió tener las dos familias. Es una de las decisiones de diseño de C mejor
justificadas, y solo se entiende mirando lo que había antes.

PL/I compensa con algo que casi nadie tiene: las operaciones de bits funcionan sobre **cadenas de
cualquier longitud**, así que se pueden evaluar 32 condiciones a la vez, y `bool(a, b, '0110'b)`
aplica una **función booleana arbitraria** especificada por su tabla de verdad. Es potente, es
oscuro, y es muy PL/I.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
COND ; Condiciones -- clase 057
 read n
 set positivo = (n > 0)
 set par = (n#2 = 0)
 write "positivo=", $$tf(positivo)
 write " par=", $$tf(par)
 write " ambos=", $$tf(positivo & par), !
 quit
 ;
tf(v) ; booleano a texto
 quit $select(v : "true", 1 : "false")
```

**Lo que esta clase enseña en M.** `&` es el *y* lógico y **`!` es el *o***, no la negación —la
negación es el apóstrofo `'`—. Esa asignación de símbolos es la primera trampa de M para cualquiera
que venga de C, y ya apareció en la clase 046.

Sobre el cortocircuito, el estándar de M **no lo garantiza**: los operadores lógicos son operaciones
sobre valores y evalúan ambos lados. La forma segura, y la idiomática, es el **postcondicional**:

```mumps
 set:i'>n valor = tabla(i)      ; el SET solo se ejecuta si la condición se cumple
 quit:$data(x)=0 "sin datos"    ; guarda de salida temprana
 do:edad<18 MENOR               ; llamada condicional
```

`comando:condición` es la construcción más característica del lenguaje. No es azúcar sobre `if`: es
un modificador que admite **casi cualquier comando**, y permite escribir guardas y control de flujo
sin abrir bloques. Es, en la práctica, el cortocircuito de M — la condición decide si el comando
llega a ejecutarse.

Y `$select(cond1 : val1, cond2 : val2, 1 : porDefecto)` **sí evalúa perezosamente**: recorre los pares
de izquierda a derecha y devuelve el primer valor cuya condición se cumple, **sin evaluar los
demás**. Es el `cond` de Lisp en forma de función incorporada, y es la herramienta correcta cuando lo
que quieres es un valor y no una acción.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| n positivo par tf |

n := stdin nextLine trimBoth asNumber.
positivo := n > 0.
par := n even.

tf := [ :v | v ifTrue: [ 'true' ] ifFalse: [ 'false' ] ].

Transcript
    show: 'positivo=', (tf value: positivo);
    show: ' par=', (tf value: par);
    show: ' ambos=', (tf value: (positivo and: [ par ]));
    cr.
```

**Lo que esta clase enseña en Smalltalk.** Los corchetes de `and: [ par ]` **no son estilo: son el
cortocircuito**. `and:` recibe un **bloque** —un trozo de código sin evaluar— y la implementación
decide si lo evalúa:

```smalltalk
True  >> and: unBloque    ^ unBloque value
False >> and: unBloque    ^ false          "ni siquiera lo mira"
```

Y al lado existe `&`, que recibe **un valor ya evaluado**:

```smalltalk
True  >> & unBooleano     ^ unBooleano
False >> & unBooleano     ^ false
```

Dos mensajes, dos comportamientos, y la diferencia está enteramente en **si el argumento llega
evaluado o sin evaluar**. Es exactamente la distinción `&&` frente a `&` de C, obtenida sin ninguna
sintaxis especial y sin ninguna regla del compilador: solo pasando código en lugar de datos.

Esa es, probablemente, la demostración más elegante de toda esta sección. En Ada hay que añadir dos
operadores al lenguaje; en C hay que añadir una regla de evaluación; en Lisp hace falta una macro. En
Smalltalk basta con que el argumento sea un objeto que sabe ejecutarse cuando se lo pidan.

Y por eso `and:`, `or:`, `ifTrue:`, `whileTrue:` y `to:do:` se escriben todos con corchetes: **son la
misma idea aplicada a distintas estructuras de control**.

---

## Y de vuelta a la clase

La regla práctica: **si el segundo operando solo es válido cuando el primero es cierto, el orden y el
cortocircuito son parte de la corrección del programa, no una optimización**. `i < n and then v(i) =
x` es correcto; con `and` a secas es un fallo. Cuando cambies de lenguaje, esa es la primera pregunta
que hay que hacerle a su tabla de operadores — y en Fortran, la respuesta obliga a anidar los `if`.

⏮️ [Volver a la clase 057](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
