# -*- coding: utf-8 -*-
"""Parte 4, lote A — clases 057 a 062. Ver `vivos_parte4.py` y `gen_vivos.py`.

El código de los ocho lenguajes de la sección 🟢 se ejecuta en CI contra el
`casos.json` de la clase (`scripts/verificar_vivos.py`).
"""

SPECS: dict[str, dict] = {}

# ---------------------------------------------------------------------------
# 057 — Booleanos, condiciones y cortocircuito
# ---------------------------------------------------------------------------
SPECS["057"] = dict(
    gancho="""
Dos preguntas sobre un número y la conjunción de ambas. Lo que parece trivial esconde la pregunta
que abre toda la Parte 4: **cuando escribes `A y B`, ¿se evalúa siempre `B`?** Si `B` es una simple
comparación da igual; si `B` accede a una posición de un array, llama a una función o lee un fichero,
la respuesta decide entre un programa correcto y una excepción.
""",
    porque="""
Aquí el concepto es el **cortocircuito**, y estos lenguajes lo enseñan porque **no lo dan por
supuesto**. En C, Java o Python, `&&` cortocircuita y no hay elección; en **Ada** hay cuatro
operadores —`and`, `or`, `and then`, `or else`— y hay que decidir en cada uso. En **Fortran** el
estándar **no garantiza** el cortocircuito y el compilador puede evaluar los dos lados. En **PL/I**
`&` es una operación sobre bits que siempre evalúa ambos.

Y en **Smalltalk** el cortocircuito no es una regla del lenguaje: es la consecuencia de que `and:`
reciba **un bloque** en lugar de un valor. Ver esa diferencia es entender de dónde sale el
comportamiento que en los demás lenguajes viene dado.
""",
    cierre="""
La regla práctica: **si el segundo operando solo es válido cuando el primero es cierto, el orden y el
cortocircuito son parte de la corrección del programa, no una optimización**. `i < n and then v(i) =
x` es correcto; con `and` a secas es un fallo. Cuando cambies de lenguaje, esa es la primera pregunta
que hay que hacerle a su tabla de operadores — y en Fortran, la respuesta obliga a anidar los `if`.
""",
    langs={
        "cobol": ("""
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
""", """
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
"""),
        "fortran": ("""
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
""", """
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
"""),
        "ada": ("""
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
""", """
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
"""),
        "pascal": ("""
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
""", """
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
"""),
        "lisp": ("""
(flet ((tf (v) (if v "true" "false")))
  (let* ((n (read))
         (positivo (> n 0))
         (par (evenp n)))
    (format t "positivo=~A par=~A ambos=~A~%"
            (tf positivo) (tf par) (tf (and positivo par)))))
""", """
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
"""),
        "tcl": ("""
proc tf {v} { return [expr {$v ? "true" : "false"}] }

gets stdin linea
set n [string trim $linea]

set positivo [expr {$n > 0}]
set par [expr {$n % 2 == 0}]

puts "positivo=[tf $positivo] par=[tf $par] ambos=[tf [expr {$positivo && $par}]]"
""", """
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
"""),
        "perl": ("""
use strict;
use warnings;

sub tf { return $_[0] ? 'true' : 'false' }

my $n = <STDIN>;
chomp $n;

my $positivo = $n > 0;
my $par = ($n % 2 == 0);

printf "positivo=%s par=%s ambos=%s\\n",
       tf($positivo), tf($par), tf($positivo && $par);
""", """
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
"""),
        "cpp": ("""
#include <iostream>

int main() {
    int n{};
    if (!(std::cin >> n)) return 1;

    const bool positivo = n > 0;
    const bool par = (n % 2 == 0);

    std::cout << std::boolalpha
              << "positivo=" << positivo
              << " par=" << par
              << " ambos=" << (positivo && par) << '\\n';
    return 0;
}
""", """
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
"""),
        "rpg": ("""
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
""", """
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
"""),
        "pli": ("""
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
""", """
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
"""),
        "mumps": ("""
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
""", """
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
"""),
        "smalltalk": ("""
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
""", """
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
"""),
    },
)

# ---------------------------------------------------------------------------
# 058 — Guardas y validación temprana
# ---------------------------------------------------------------------------
SPECS["058"] = dict(
    gancho="""
Tres casos y una salida por cada uno. El patrón que se estudia aquí —**comprobar lo excepcional
primero y salir**— es el que evita la pirámide de `if` anidados, y su nombre técnico es *cláusula de
guarda*. La pregunta que separa a estos lenguajes es sencilla: **¿se puede salir de un procedimiento
por la mitad?**
""",
    porque="""
Aquí el concepto es la **salida temprana**, y estos lenguajes lo enseñan porque **la mitad de ellos
nació cuando eso se consideraba mala práctica**. El COBOL estructurado desaconsejaba salir de un
párrafo por el medio; Fortran tenía `RETURN` desde el principio pero su cultura era de un único punto
de salida; y Pascal, en su forma original, **no tenía `return` en absoluto**.

Enfrente, M tiene la forma más compacta que existe —`quit:condición`, la guarda en once
caracteres— y COBOL tiene `EVALUATE TRUE`, que convierte una cadena de guardas en una tabla legible.
""",
    cierre="""
Lo transferible es que **la guarda no es un truco de estilo: reduce la profundidad de anidamiento y
pone lo excepcional al principio**, donde se revisa. La discusión sobre el "único punto de salida"
viene de una época sin `finally` ni destructores, en la que salir por el medio se llevaba por delante
la liberación de recursos. Hoy que existen RAII, `finally` y `defer`, ese argumento ha desaparecido —
pero el estilo sobrevive en el código de esa época, y conviene saber por qué está escrito así.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. GUARDAS.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  EDAD    PIC S9(9) COMP-3.

PROCEDURE DIVISION.
    ACCEPT LINEA
    MOVE FUNCTION NUMVAL(LINEA) TO EDAD

    EVALUATE TRUE
        WHEN EDAD < 0    DISPLAY "invalido"
        WHEN EDAD < 18   DISPLAY "menor"
        WHEN OTHER       DISPLAY "adulto"
    END-EVALUATE

    STOP RUN.
""", """
**Lo que esta clase enseña en COBOL.** **`EVALUATE TRUE` es la construcción que hay que llevarse de
esta clase.** No es un `switch` sobre un valor: es un `switch` sobre **condiciones**, donde cada
`WHEN` lleva una expresión booleana completa y gana la primera que se cumple.

```cobol
EVALUATE TRUE
    WHEN SALDO < 0                DISPLAY "descubierto"
    WHEN SALDO = 0                DISPLAY "a cero"
    WHEN SALDO < LIMITE-AVISO     DISPLAY "saldo bajo"
    WHEN OTHER                    DISPLAY "correcto"
END-EVALUATE
```

Es una cadena de guardas escrita como una tabla, y se lee de arriba abajo sin anidamiento. En C, Java
o Python hay que encadenar `else if`; aquí la estructura declara que **es una decisión entre casos
excluyentes**, no una serie de comprobaciones independientes.

Y `EVALUATE` va mucho más lejos, con **varios sujetos a la vez**:

```cobol
EVALUATE TIPO-CLIENTE ALSO IMPORTE ALSO TRUE
    WHEN "VIP"  ALSO 1000 THRU 9999 ALSO URGENTE   PERFORM ENVIO-EXPRES
    WHEN "VIP"  ALSO ANY            ALSO ANY       PERFORM ENVIO-NORMAL
    WHEN ANY    ALSO 0 THRU 99      ALSO ANY       PERFORM RECOGIDA
END-EVALUATE
```

Eso es una **tabla de decisión** —con rangos `THRU`, comodines `ANY` y combinación de sujetos— dentro
del lenguaje. Es lo más parecido a la coincidencia de patrones moderna que existía en 1985, y sigue
sin tener equivalente directo en la mayoría del núcleo.
"""),
        "fortran": ("""
program guardas
   implicit none
   integer :: edad

   read(*, *) edad

   if (edad < 0) then
      write(*, '(A)') 'invalido'
   else if (edad < 18) then
      write(*, '(A)') 'menor'
   else
      write(*, '(A)') 'adulto'
   end if
end program guardas
""", """
**Lo que esta clase enseña en Fortran.** El `if / else if / end if` de este programa es Fortran
**moderno**. El del 66 no lo tenía, y esta clase es un buen sitio para ver de dónde venimos:

```fortran
      IF (EDAD) 10, 20, 30        ! IF ARITMÉTICO: salta a una etiqueta u otra
                                  ! según el valor sea <0, =0 o >0
   10 WRITE(6,*) 'invalido'
      GO TO 40
   20 ...
```

El **`IF` aritmético de tres ramas** era la forma original, y es un salto a etiquetas. Está declarado
obsolescente desde Fortran 90 y eliminado en Fortran 2018, pero aparece en código heredado. Junto al
`GO TO` calculado y al `GO TO` asignado, formaba un modelo de control que la programación estructurada
vino a sustituir — y la reacción contra él es literalmente el origen de la carta de Dijkstra
*"Go To Statement Considered Harmful"*, de 1968.

Fortran moderno tiene además una pieza que da nombre a los bloques y que resulta muy útil para las
guardas:

```fortran
validacion: block
   if (edad < 0) exit validacion       ! sale del BLOQUE, no del programa
   ...
end block validacion
```

`block` (Fortran 2008) crea un ámbito con nombre del que se puede salir con `exit`. Es la guarda sin
`return` y sin `goto`, y sin abandonar el procedimiento.
"""),
        "ada": ("""
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Guardas is
   Edad : Integer;
begin
   Get (Edad);

   if Edad < 0 then
      Put_Line ("invalido");
   elsif Edad < 18 then
      Put_Line ("menor");
   else
      Put_Line ("adulto");
   end if;
end Guardas;
""", """
**Lo que esta clase enseña en Ada.** `elsif` —sin la `e`— es una palabra clave propia y no un `else`
seguido de un `if`. La diferencia importa: **cada `if` necesita su `end if`**, así que una cadena
escrita con `else if` obligaría a cerrar tantos `end if` como ramas hubiera. Con `elsif`, la cadena
tiene **un solo `end if`** y la estructura queda plana, que es exactamente lo que una cadena de
guardas debe parecer.

Es una decisión sintáctica pequeña con un efecto grande sobre la legibilidad, y la copiaron después
Python (`elif`), PL/SQL, Ruby (`elsif`) y el shell (`elif`).

Pero la respuesta de Ada a esta clase no está en el `if`: está en **los contratos**, que suben la
guarda de la implementación a la especificación.

```ada
function Clasificar (Edad : Integer) return String
  with Pre => Edad >= 0;              --  la validación es parte de la FIRMA
```

Con `Pre`, la condición se comprueba en cada llamada —o, con SPARK, **se demuestra estáticamente que
ninguna llamada la viola**, y entonces la comprobación se elimina—. La guarda deja de estar dentro de
la función repetida en cada implementación y pasa a ser una obligación del que llama, verificable.

Es la diferencia entre "compruebo por si acaso" y "el compilador sabe que no puede pasar".
"""),
        "pascal": ("""
program Guardas;
{$MODE OBJFPC}{$H+}

var
  Edad: Integer;

begin
  Read(Edad);

  if Edad < 0 then
    WriteLn('invalido')
  else if Edad < 18 then
    WriteLn('menor')
  else
    WriteLn('adulto');
end.
""", """
**Lo que esta clase enseña en Pascal.** El **Pascal ISO no tiene `return`**. Ninguna forma de salir
de un procedimiento antes del final. Wirth lo consideró incompatible con la programación estructurada:
un procedimiento tenía **una entrada y una salida**, y punto.

La consecuencia es que el código Pascal clásico usa banderas y anidamiento donde otros lenguajes usan
guardas, y de ahí viene la fama de "pirámide de `if`" que arrastra el estilo de la época.

Free Pascal y Delphi añadieron después dos formas de salir:

```pascal
Exit;               { sale del procedimiento }
Exit(valor);        { sale de una función devolviendo un valor (Delphi 2009+) }
Break; Continue;    { para bucles }
```

Y fíjate en la trampa sintáctica de este programa, que es la más famosa del lenguaje: **no hay punto
y coma antes de `else`**. `WriteLn('invalido')` va sin `;` porque el `;` **termina** la sentencia
`if`, y entonces el `else` queda huérfano y no compila. Es la primera piedra con la que tropieza todo
el mundo, y la razón es que en Pascal el `;` es un **separador** entre sentencias, no un terminador
como en C.

La misma regla explica por qué el `end` final tampoco lleva `;` delante y por qué `end.` cierra el
programa con punto.
"""),
        "lisp": ("""
(let ((edad (read)))
  (format t "~A~%"
          (cond ((< edad 0)  "invalido")
                ((< edad 18) "menor")
                (t           "adulto"))))
""", """
**Lo que esta clase enseña en Common Lisp.** `cond` **es** la cadena de guardas, y es la forma
original: apareció en el Lisp de McCarthy en 1958 y es el antepasado directo del `else if` de todos
los lenguajes posteriores.

Su forma es una lista de pares `(condición resultado)`, evaluados de arriba abajo, y el `t` final
—que siempre es cierto— hace de `else`. No hay `else`, no hay `elsif` y no hay `end`: hay una lista.

Y lo decisivo para esta clase: **`cond` es una expresión, no una sentencia**. Devuelve un valor, así
que se puede usar donde se espere uno —aquí, como argumento de `format`—. No hace falta una variable
temporal ni asignar en cada rama, que es lo que obliga a hacer un `if` que no devuelve nada.

Lisp tiene además una guarda de salida real, y su nombre delata que la salida temprana era un tema
delicado:

```lisp
(defun clasificar (edad)
  (when (< edad 0)
    (return-from clasificar "invalido"))    ; sale de la función POR SU NOMBRE
  (if (< edad 18) "menor" "adulto"))
```

`return-from` exige **nombrar el bloque del que sale**, y eso permite salir de un bloque interior
concreto, no solo del más cercano. Con `block` puedes crear bloques con nombre propio y saltar a
cualquiera de ellos — un `goto` estructurado y comprobado en compilación.
"""),
        "tcl": ("""
gets stdin linea
set edad [string trim $linea]

if {$edad < 0} {
    puts "invalido"
} elseif {$edad < 18} {
    puts "menor"
} else {
    puts "adulto"
}
""", """
**Lo que esta clase enseña en Tcl.** `if` es un **comando**, y su firma es
`if condición cuerpo ?elseif condición cuerpo? ?else cuerpo?`. Es decir, `elseif` y `else` no son
palabras clave: son **argumentos** con un valor concreto, y por eso hay que escribirlos exactamente
así.

Eso explica dos reglas que sorprenden:

```tcl
if {$a > 0} {puts "sí"}      ;# correcto
if {$a > 0}
{puts "sí"}                  ;# ERROR: el comando if TERMINA al final de la línea
```

La llave de apertura **debe ir en la misma línea**, porque el salto de línea termina el comando y el
bloque quedaría suelto. Es la única regla de formato obligatoria de Tcl, y es consecuencia directa de
que no haya sintaxis: si `if` es un comando, sus argumentos van en la misma línea.

Para las guardas de verdad, Tcl usa `return` —que en un procedimiento sale de inmediato— y tiene una
forma que casi ningún lenguaje ofrece: **`return -code`**, que permite devolver un código de control.

```tcl
proc validar {edad} {
    if {$edad < 0} { return -code error "edad negativa" }
    return $edad
}
```

`return -code error` lanza un error desde una función corriente, y existen también `-code break` y
`-code continue`, que permiten que un procedimiento **afecte al bucle de quien lo llama**. Es potente
y es peligroso, y es la clase de cosa que solo cabe en un lenguaje donde el control de flujo son
comandos.
"""),
        "perl": ("""
use strict;
use warnings;

my $edad = <STDIN>;
chomp $edad;

if    ($edad < 0)  { print "invalido\\n" }
elsif ($edad < 18) { print "menor\\n" }
else               { print "adulto\\n" }
""", """
**Lo que esta clase enseña en Perl.** Perl es el lenguaje de esta página **diseñado explícitamente
para escribir guardas**, porque sus modificadores de sentencia ponen la condición al final:

```perl
return          if $edad < 0;
die "negativa"  unless $edad >= 0;
next            if $linea =~ /^#/;      # saltar comentarios
last            if $encontrado;
```

La condición va detrás porque **así se lee en voz alta**: *"vuelve si la edad es negativa"*. Larry
Wall es lingüista, y esa decisión es deliberada: en una guarda, lo importante es la acción, y la
condición es la subordinada.

`unless` es la negación con nombre propio, y evita el `if (!(...))` con doble negación que cuesta
leer. La convención de la comunidad es usar `unless` solo con condiciones simples y nunca con `else`,
porque `unless ... else` obliga a negar mentalmente dos veces.

Y hay algo más que hace de Perl el lenguaje de las guardas: **la asignación dentro de la condición es
idiomática y segura**.

```perl
while (my $linea = <$fh>) { ... }
if (my ($a, $b) = $texto =~ /(\\d+)-(\\d+)/) { ... }
```

`my` dentro de la condición declara la variable con ámbito en el bloque. Es el mismo patrón que C++17
añadió con `if (auto x = f(); x > 0)` treinta años después.
"""),
        "cpp": ("""
#include <iostream>

int main() {
    int edad{};
    if (!(std::cin >> edad)) return 1;

    if (edad < 0) {
        std::cout << "invalido\\n";
    } else if (edad < 18) {
        std::cout << "menor\\n";
    } else {
        std::cout << "adulto\\n";
    }
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** La primera línea del programa **ya es una guarda**:
`if (!(std::cin >> edad)) return 1;` valida la entrada y sale, antes de tocar nada. Es el patrón que
esta clase enseña, aplicado al caso más real que existe.

Y C++ es donde el debate del "único punto de salida" tuvo su desenlace, porque el lenguaje lo
resolvió por otra vía. El argumento clásico contra las salidas múltiples era la **liberación de
recursos**: si sales por el medio, ¿quién cierra el fichero?

**RAII responde a eso**: el destructor se ejecuta al salir del ámbito, **por cualquier camino** —
`return`, excepción o final normal—.

```cpp
{
    std::ifstream f("datos.txt");        // se abre
    if (!f) return 1;                    // se cierra solo
    if (algo_mal()) throw std::runtime_error("...");  // también se cierra
}                                        // y aquí también
```

Con eso, la razón histórica para prohibir la salida temprana desaparece, y las guías modernas de C++
la recomiendan sin reservas.

C++17 añadió además la forma de inicializar dentro de la condición, que es la versión C++ del `my`
de Perl:

```cpp
if (auto it = mapa.find(clave); it != mapa.end()) {
    usar(it->second);
}   // it deja de existir aquí
```

Y `[[nodiscard]]` y `[[maybe_unused]]` completan la idea: convertir en errores los descuidos que
antes eran convenciones.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi GUARDAS;
  edad int(10) const;
end-pi;

dcl-s salida char(20);

select;
  when edad < 0;
    salida = 'invalido';
  when edad < 18;
    salida = 'menor';
  other;
    salida = 'adulto';
endsl;

dsply salida;

*inlr = *on;
return;
""", """
**Lo que esta clase enseña en RPG.** `select` / `when` / `other` / `endsl` es el equivalente exacto
del `EVALUATE TRUE` de COBOL: **un `switch` sobre condiciones**, no sobre un valor. Cada `when` lleva
una expresión booleana completa y gana el primero que se cumple.

Que los dos lenguajes de negocio de esta página tengan esta construcción —y que los lenguajes de
sistemas no la tengan— no es casualidad. Las reglas de negocio son **tablas de decisión**: "si el
cliente es de este tipo y el importe está en este rango y es urgente, entonces…". Un `switch` sobre
un solo valor no sirve para eso; una cadena de `else if` lo expresa mal. `SELECT`/`EVALUATE` sí.

RPG tiene además una guarda muy usada que conviene reconocer, porque enlaza con la clase 072:

```rpgle
chain (clave) CLIENTES;
if not %found(CLIENTES);
  return;                    // guarda: no está, salimos
endif;
```

`%found` y `%error` son **funciones que consultan el resultado de la última operación**, en lugar de
que la operación devuelva un valor. Es el modelo de los indicadores de la clase 057, modernizado: la
condición sigue siendo un estado global de la operación anterior, pero al menos tiene nombre.
"""),
        "pli": ("""
 guardas: procedure options(main);

    declare edad fixed binary(31);

    get list (edad);

    select;
       when (edad < 0)  put skip list ('invalido');
       when (edad < 18) put skip list ('menor');
       otherwise        put skip list ('adulto');
    end;

 end guardas;
""", """
**Lo que esta clase enseña en PL/I.** `select` sin expresión —solo `select;`— evalúa las condiciones
de cada `when` en orden y ejecuta la primera que sea cierta. Es la misma construcción que el
`EVALUATE TRUE` de COBOL y el `select` de RPG, y PL/I la tenía antes que los dos.

Con expresión, `select (dia);` compara contra valores concretos, así que **una sola construcción
cubre los dos usos** —el `switch` clásico y la cadena de guardas—. Es una unificación elegante, y es
lo que después hicieron Ada con `case`, Rust con `match` y Kotlin con `when`.

PL/I tiene además la salida temprana con `return`, y algo más raro: `leave`, que sale de un bucle con
nombre.

```pli
bucle_ext: do i = 1 to n;
   do j = 1 to m;
      if encontrado then leave bucle_ext;   /* sale de los DOS bucles */
   end;
end bucle_ext;
```

Salir de un bucle exterior por su nombre resuelve el caso que en C obliga a usar `goto` o una bandera.
Java lo añadió con etiquetas, Rust con `'label: loop`, y PL/I lo tenía en los 60. Es un buen ejemplo
de que la crítica a PL/I no era por falta de buenas ideas: era por tener demasiadas a la vez.
"""),
        "mumps": ("""
GUARDA ; Guardas -- clase 058
 read edad
 write:edad<0 "invalido",!
 quit:edad<0
 write:edad<18 "menor",!
 quit:edad<18
 write "adulto",!
 quit
""", """
**Lo que esta clase enseña en M.** **`quit:condición` es la cláusula de guarda más compacta que
existe en ningún lenguaje.** Once caracteres, sin bloque, sin `if` y sin anidamiento.

El **postcondicional** —el `:condición` pegado detrás de un comando— es la construcción central de M
y ya apareció en la 057. Aquí se ve para qué sirve de verdad: escribir una cadena de guardas como una
secuencia plana de líneas, cada una con su condición.

```mumps
validar(x) ;
 quit:x="" "vacio"
 quit:x'?1.N "no numerico"       ; ?1.N es un PATRÓN: uno o más dígitos
 quit:x<0 "negativo"
 quit "ok"
```

Fíjate en `x'?1.N`: M tiene **coincidencia de patrones en el propio operador `?`**, con una sintaxis
propia —`1.N` significa "uno o más numéricos", `.A` "cero o más alfabéticos", `1"ABC"` un literal—.
Es un mini-lenguaje de validación incorporado, anterior a las expresiones regulares de Perl y mucho
más limitado, pero disponible en 1966 y suficiente para validar campos de un formulario.

Esta clase es, junto a la 072, donde M se ve mejor: un lenguaje diseñado para escribir **muchas
comprobaciones cortas seguidas**, que es exactamente lo que hace un sistema clínico al validar una
entrada.
"""),
        "smalltalk": ("""
| edad |

edad := stdin nextLine trimBoth asNumber.

Transcript
    show: (edad < 0
        ifTrue:  [ 'invalido' ]
        ifFalse: [ edad < 18 ifTrue: [ 'menor' ] ifFalse: [ 'adulto' ] ]);
    cr.
""", """
**Lo que esta clase enseña en Smalltalk.** **No hay `elsif`, y no puede haberlo.** Como `ifTrue:` es
un mensaje enviado a un booleano, una cadena de guardas se escribe **anidando** el segundo
condicional dentro del bloque `ifFalse:` del primero. No hay forma de aplanarla con sintaxis, porque
no hay sintaxis.

Eso podría parecer una carencia, y la comunidad la convirtió en un principio de diseño: **si tu
método tiene una cadena de condiciones anidadas, probablemente te falta polimorfismo**. La solución
idiomática no es aplanar el `if`, es **eliminarlo**:

```smalltalk
"En vez de preguntar por el tipo, se le pregunta al objeto."
Menor  >> clasificacion    ^ 'menor'
Adulto >> clasificacion    ^ 'adulto'
```

Ese es el consejo más citado del mundo Smalltalk —*"reemplaza el condicional por polimorfismo"*— y
está en el catálogo de refactorizaciones de Martin Fowler, que trabajó en esta comunidad. La
incomodidad sintáctica del `else if` empuja hacia el diseño que el lenguaje considera correcto.

Para las guardas de salida sí hay una forma directa: **`^` devuelve del método inmediatamente**, y
funciona **desde dentro de un bloque**, saliendo del método que lo contiene:

```smalltalk
clasificar: edad
    edad < 0 ifTrue: [ ^'invalido' ].     "sale del método, no del bloque"
    ^edad < 18 ifTrue: [ 'menor' ] ifFalse: [ 'adulto' ]
```

Ese `^` dentro de un bloque es un **retorno no local**, y es una capacidad potente: un bloque pasado
a otro método puede terminar el método que lo creó.
"""),
    },
)

# ---------------------------------------------------------------------------
# 059 — if / else y anidamiento
# ---------------------------------------------------------------------------
SPECS["059"] = dict(
    gancho="""
Cuatro tramos de nota a partir de una puntuación. Una cadena de comparaciones ordenadas, que es la
estructura de decisión más común de todo el software de negocio. Y es también la que más se escribe
mal: **si los tramos se comprueban en el orden equivocado, el programa compila, se ejecuta y da un
resultado incorrecto sin ninguna señal**.
""",
    porque="""
Aquí el concepto es el **anidamiento y el orden de las condiciones**, y estos lenguajes lo enseñan
porque cargan con la cicatriz más famosa de la historia de la sintaxis: **el `else` colgante**.

En COBOL, el `.` de más dentro de un `IF` cambia el flujo del programa sin dar error —de ahí que
COBOL-85 tuviera que inventar `END-IF`—. En Fortran clásico, un `IF` sin `THEN` solo abarca una
sentencia. Y en Pascal, el punto y coma antes del `else` no compila. Tres lenguajes, tres formas
distintas de que el anidamiento se rompa en silencio o casi.
""",
    cierre="""
La lección: **el terminador explícito no es burocracia**. `END-IF`, `end if`, `endif`, `fi`,
`END-EVALUATE` existen porque los lenguajes que no los tenían acumularon defectos reales — el más
caro documentado es el fallo de `goto fail` de Apple en 2014, donde una línea duplicada bajo un `if`
sin llaves desactivó la validación de certificados TLS. Poner siempre las llaves, o el terminador, no
es estilo: es la mitigación de un error que ya ha ocurrido.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. NOTAS.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  SCORE   PIC S9(9) COMP-3.
01  NOTA    PIC X.

PROCEDURE DIVISION.
    ACCEPT LINEA
    MOVE FUNCTION NUMVAL(LINEA) TO SCORE

    EVALUATE TRUE
        WHEN SCORE >= 90   MOVE "A" TO NOTA
        WHEN SCORE >= 80   MOVE "B" TO NOTA
        WHEN SCORE >= 70   MOVE "C" TO NOTA
        WHEN OTHER         MOVE "F" TO NOTA
    END-EVALUATE

    DISPLAY "nota=" NOTA
    STOP RUN.
""", """
**Lo que esta clase enseña en COBOL.** Aquí está **el defecto sintáctico más caro de COBOL**: hasta
COBOL-85 no existía `END-IF`, y el alcance de un `IF` lo delimitaba **el punto**.

```cobol
IF SALDO > 0
    DISPLAY "positivo".
    DISPLAY "siempre se ejecuta".      *> el punto anterior CERRÓ el IF
```

Esa segunda línea parece estar dentro del `IF` —está indentada— y **no lo está**. El punto de la
línea anterior cerró la sentencia. El programa compila, se ejecuta y hace algo distinto de lo que
aparenta, sin un solo aviso. Con `IF` anidados, un punto de más colapsa varios niveles a la vez.

COBOL-85 introdujo los **terminadores de ámbito** —`END-IF`, `END-PERFORM`, `END-EVALUATE`,
`END-READ`, `END-COMPUTE`— precisamente para eliminar esa dependencia del punto. La regla de estilo
moderna es tajante: **un punto por párrafo, al final, y terminadores explícitos en todo lo demás**.

Y para el caso de esta clase, `EVALUATE TRUE` evita el anidamiento por completo, con una ventaja
sobre el `else if` que conviene ver: los tramos quedan **alineados en columna**, así que revisar que
el orden es correcto —de mayor a menor— es una lectura vertical. En una cadena de `if` anidados, esa
misma comprobación exige seguir la indentación.
"""),
        "fortran": ("""
program notas
   implicit none
   integer :: score
   character(len=1) :: nota

   read(*, *) score

   if (score >= 90) then
      nota = 'A'
   else if (score >= 80) then
      nota = 'B'
   else if (score >= 70) then
      nota = 'C'
   else
      nota = 'F'
   end if

   write(*, '(A,A)') 'nota=', nota
end program notas
""", """
**Lo que esta clase enseña en Fortran.** El `if` de Fortran tiene **dos formas**, y confundirlas es
un error clásico:

```fortran
if (x > 0) y = 1                 ! IF LÓGICO: una sola sentencia, sin then ni end if
if (x > 0) then                  ! IF de BLOQUE: varias sentencias
   y = 1
   z = 2
end if
```

La primera forma no lleva `then` y **solo abarca la sentencia que va en la misma línea**. Escribir
una segunda línea debajo, indentada, no la mete dentro del `if`. Es exactamente el mismo problema que
el punto de COBOL y que el `if` sin llaves de C, con la diferencia de que en Fortran la ausencia de
`then` lo hace algo más visible.

Fortran moderno añadió además **nombres de construcción**, que ayudan mucho con el anidamiento
profundo:

```fortran
clasificar: if (score >= 90) then
   nota = 'A'
else if (score >= 80) then clasificar
   nota = 'B'
end if clasificar
```

Poder nombrar un `if`, un `do` o un `select case` y repetir el nombre al cerrarlo hace que un bloque
de doscientas líneas siga siendo legible, y que el compilador detecte un cierre mal emparejado. Ada
hace lo mismo con `end Nombre_Del_Procedimiento`, y por la misma razón: **el código de larga vida lo
lee alguien que no lo escribió**.
"""),
        "ada": ("""
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Notas is
   Score : Integer;
   Nota  : Character;
begin
   Get (Score);

   if Score >= 90 then
      Nota := 'A';
   elsif Score >= 80 then
      Nota := 'B';
   elsif Score >= 70 then
      Nota := 'C';
   else
      Nota := 'F';
   end if;

   Put_Line ("nota=" & Nota);
end Notas;
""", """
**Lo que esta clase enseña en Ada.** En Ada **el `else` colgante no existe**, y no por convención:
porque la gramática lo impide. Cada `if` termina obligatoriamente en `end if;`, así que no hay
ninguna ambigüedad posible sobre a qué `if` pertenece un `else`.

```ada
if A then
   if B then
      X := 1;
   end if;        --  este end if cierra el interior...
else
   X := 2;        --  ...y por tanto ESTE else es del exterior. Sin duda.
end if;
```

En C, en Java y en JavaScript esa misma estructura sin llaves es ambigua para el lector —el
compilador la resuelve asociando el `else` al `if` más cercano— y ha producido errores reales.

Y `elsif` en lugar de `else if` es lo que evita la cascada de `end if`: con `else if` harían falta
tres cierres para tres tramos.

Ada añade a esta clase algo que resuelve el problema de fondo —**el orden equivocado de los
tramos**— mediante los subtipos:

```ada
subtype Puntuacion is Integer range 0 .. 100;
Score : Puntuacion;                      --  leer 150 levanta Constraint_Error
```

Los tramos mal ordenados siguen siendo posibles, pero **el rango de entrada queda garantizado por el
tipo**, así que desaparece toda una familia de casos límite que en otros lenguajes hay que comprobar
a mano al principio de la cadena.
"""),
        "pascal": ("""
program Notas;
{$MODE OBJFPC}{$H+}

var
  Score: Integer;
  Nota: Char;

begin
  Read(Score);

  if Score >= 90 then
    Nota := 'A'
  else if Score >= 80 then
    Nota := 'B'
  else if Score >= 70 then
    Nota := 'C'
  else
    Nota := 'F';

  WriteLn('nota=', Nota);
end.
""", """
**Lo que esta clase enseña en Pascal.** Fíjate en los punto y coma de este programa: **no hay ninguno
antes de un `else`**, y solo aparece uno al final de toda la cadena. Es la regla que más tropiezos
causa en Pascal, y tiene una explicación precisa.

En Pascal, **el `;` es un separador entre sentencias, no un terminador**. `if ... then A else B` es
**una sola sentencia**, así que poner `;` después de `A` la daría por terminada y dejaría el `else`
sin dueño: error de compilación.

```pascal
if C then A;  else B;      { NO COMPILA }
if C then A   else B;      { correcto }
```

En C ocurre lo contrario —el `;` termina, y `if (c) a; else b;` es correcto— y por eso quien viene de
C escribe mal el primer `if` de Pascal que le toca.

La ventaja es que **el error se detecta al compilar**. Compara con el punto de COBOL, que no da
error y cambia el significado; o con el `if` sin llaves de C, que compila y hace otra cosa. De las
tres formas de equivocarse con el anidamiento que aparecen en esta página, la de Pascal es la única
que el compilador atrapa siempre.

Y a Pascal, al no tener terminador de `if`, le pasa lo mismo que a C con el anidamiento: la solución
es usar `begin`/`end` incluso cuando hay una sola sentencia, que es la versión Pascal de "pon siempre
las llaves".
"""),
        "lisp": ("""
(let ((score (read)))
  (format t "nota=~A~%"
          (cond ((>= score 90) "A")
                ((>= score 80) "B")
                ((>= score 70) "C")
                (t             "F"))))
""", """
**Lo que esta clase enseña en Common Lisp.** **En Lisp el anidamiento no puede ser ambiguo, porque
los paréntesis lo delimitan todo.** No hay `else` colgante, no hay punto que cierre de más, no hay
`;` que termine antes de tiempo. La estructura del código **es** la estructura del árbol sintáctico,
literalmente.

Ese es el argumento que la comunidad Lisp lleva sesenta años haciendo: los paréntesis que tanto
critican desde fuera son lo que elimina una familia entera de errores de sintaxis. Y como el editor
los empareja y los reindenta solo, la molestia práctica es mucho menor de lo que parece.

Para esta clase concreta, Lisp ofrece además una variante de `cond` que casi nadie conoce y que viene
justo al caso:

```lisp
(cond ((< score 0) :invalido)
      ((find score '(90 100)) ...))

;; Y la forma "=>" que pasa el VALOR de la condición al resultado:
(cond ((assoc score tabla) => cdr)     ; si la búsqueda encuentra algo, aplica cdr
      (t "F"))                          ; sin repetir la búsqueda
```

La forma `=>` —estándar en Scheme y disponible en varias bibliotecas de Common Lisp— evita el patrón
de "comprobar y volver a calcular" que en otros lenguajes obliga a una variable temporal. Es el mismo
problema que C++17 resolvió con `if (auto x = f(); x)`.
"""),
        "tcl": ("""
gets stdin linea
set score [string trim $linea]

if {$score >= 90} {
    set nota A
} elseif {$score >= 80} {
    set nota B
} elseif {$score >= 70} {
    set nota C
} else {
    set nota F
}

puts "nota=$nota"
""", """
**Lo que esta clase enseña en Tcl.** Las llaves son **obligatorias** en Tcl, y no por estilo: el
comando `if` recibe el cuerpo como **un argumento**, así que tiene que ser una sola palabra —y en Tcl
una "palabra" con espacios se escribe entre llaves—. No existe la forma sin llaves que causa
problemas en C.

Esa obligación elimina de raíz el problema del anidamiento: **cada rama está delimitada porque tiene
que estarlo para poder pasarse como argumento**.

Y hay una consecuencia menos obvia que esta clase es el sitio para ver. Como `if` es un comando y
`elseif` es literalmente el texto `"elseif"` en la posición correcta, escribir `elsif` o `else if`
(separado) **no es un error de sintaxis**: es pasarle a `if` un argumento que no espera, y el error
sale en ejecución.

```tcl
if {$a} { ... } else if {$b} { ... }    ;# ERROR: "else if" no es "elseif"
```

Para una cadena larga de tramos, la forma idiomática de Tcl no es `if`/`elseif` sino `switch` con el
patrón `-` para condiciones, o directamente una estructura de datos:

```tcl
foreach {umbral letra} {90 A 80 B 70 C 0 F} {
    if {$score >= $umbral} { set nota $letra ; break }
}
```

Convertir la cadena de condiciones en **datos recorridos por un bucle** es una técnica que funciona en
cualquier lenguaje y que en Tcl resulta especialmente natural, porque la lista y el código son la
misma cosa.
"""),
        "perl": ("""
use strict;
use warnings;

my $score = <STDIN>;
chomp $score;

my $nota = $score >= 90 ? 'A'
         : $score >= 80 ? 'B'
         : $score >= 70 ? 'C'
         :                'F';

print "nota=$nota\\n";
""", """
**Lo que esta clase enseña en Perl.** Este programa usa la **cadena de ternarios**, alineada en
columna, que es un idioma muy extendido en Perl y que merece explicación porque parece más raro de lo
que es.

`?:` es **asociativo por la derecha**, así que `a ? b : c ? d : e` se agrupa como
`a ? b : (c ? d : e)`. Encadenados y alineados con los `:` en la misma columna, se leen como una
tabla de tramos — que es exactamente lo que son.

La ventaja sobre `if`/`elsif` no es la brevedad: es que **es una expresión**. `my $nota = ...` asigna
una sola vez, en una sola sentencia. Con `if`/`elsif` habría que declarar `$nota` antes y asignarla
en cada rama, y el compilador no puede comprobar que todas las ramas asignan. Es el mismo argumento
que hace que Rust y Kotlin conviertan `if` en expresión.

Perl tiene además los `if` y `unless` como **modificadores** al final, que ya aparecieron en la 058, y
un detalle de esta clase: **las llaves son obligatorias**.

```perl
if ($a) print "x";        # NO COMPILA en Perl
if ($a) { print "x" }     # correcto
print "x" if $a;          # o el modificador
```

Perl, igual que Tcl, eliminó el `if` sin llaves. Es una decisión de 1987 que C nunca tomó y que le
habría ahorrado a la industria unos cuantos incidentes.
"""),
        "cpp": ("""
#include <iostream>

int main() {
    int score{};
    if (!(std::cin >> score)) return 1;

    char nota{};
    if (score >= 90) {
        nota = 'A';
    } else if (score >= 80) {
        nota = 'B';
    } else if (score >= 70) {
        nota = 'C';
    } else {
        nota = 'F';
    }

    std::cout << "nota=" << nota << '\\n';
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** C++ **permite omitir las llaves** cuando la rama tiene una sola
sentencia, y esa permisividad tiene el historial de fallos más caro de esta página.

El caso documentado es **`goto fail`**, de Apple, en 2014:

```c
if (algo)
    goto fail;
    goto fail;          // línea duplicada; NO está dentro del if
...
fail:
    return err;
```

La segunda línea está indentada como si perteneciera al `if`, y no pertenece: se ejecuta siempre. El
resultado fue que la validación de la firma en el intercambio TLS **se saltaba por completo**, en
iOS y macOS, durante meses. Una llave habría hecho imposible el error.

Por eso todas las guías modernas —*Core Guidelines* incluidas— dicen: **llaves siempre, aunque haya
una sola sentencia**. Y los compiladores ayudan: `-Wmisleading-indentation` en GCC y Clang avisa
exactamente de este patrón.

Para el caso concreto de esta clase, C++ ofrece además dos alternativas que evitan la cadena:

```cpp
const char nota = score >= 90 ? 'A' : score >= 80 ? 'B' : score >= 70 ? 'C' : 'F';

// O, con un contenedor ordenado, buscando el tramo:
static const std::map<int, char> tramos{{90,'A'},{80,'B'},{70,'C'},{0,'F'}};
auto it = tramos.lower_bound(score);   // la estructura de datos hace la decisión
```

Convertir la cadena de condiciones en datos es la misma técnica que en Tcl, y escala mucho mejor
cuando los tramos son quince y no cuatro.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi NOTAS;
  score int(10) const;
end-pi;

dcl-s nota   char(1);
dcl-s salida char(20);

select;
  when score >= 90;
    nota = 'A';
  when score >= 80;
    nota = 'B';
  when score >= 70;
    nota = 'C';
  other;
    nota = 'F';
endsl;

salida = 'nota=' + nota;
dsply salida;

*inlr = *on;
return;
""", """
**Lo que esta clase enseña en RPG.** `select`/`when`/`other`/`endsl` mantiene los cuatro tramos
**alineados en columna**, sin anidar. Es el mismo argumento que el `EVALUATE TRUE` de COBOL: una
decisión entre casos excluyentes se lee mejor como una tabla que como una escalera.

RPG tiene también `if`/`elseif`/`else`/`endif`, y la elección entre las dos formas es una convención
de estilo con criterio: `if` para una o dos ramas, `select` a partir de tres.

Lo que hace peculiar a RPG en esta clase es lo que había antes del formato libre. En el RPG de
columnas, el anidamiento se marcaba con **niveles de indicadores**, y un `IF` se cerraba con `END`
sin ninguna pista de cuál cerraba:

```text
     C                   IF        SCORE >= 90
     C                   MOVE      'A'           NOTA
     C                   ELSE
     C                   IF        SCORE >= 80
     C                   MOVE      'B'           NOTA
     C                   END
     C                   END
```

Dos `END` seguidos, sin nombre y sin indentación obligatoria. En un programa de mil líneas, emparejar
esos `END` a mano era una tarea real. Los terminadores con nombre —`endif`, `endsl`, `endfor`,
`enddo`— del formato libre resolvieron exactamente ese problema, igual que `END-IF` lo resolvió en
COBOL-85.
"""),
        "pli": ("""
 notas: procedure options(main);

    declare score fixed binary(31);
    declare nota  character(1);

    get list (score);

    select;
       when (score >= 90) nota = 'A';
       when (score >= 80) nota = 'B';
       when (score >= 70) nota = 'C';
       otherwise          nota = 'F';
    end;

    put skip list ('nota=' || nota);

 end notas;
""", """
**Lo que esta clase enseña en PL/I.** `select` sin expresión evalúa las condiciones en orden, igual
que el `EVALUATE TRUE` de COBOL y el `select` de RPG. PL/I la tuvo primero, y de aquí la tomaron los
otros dos.

Sobre el anidamiento, PL/I resolvió el problema del `else` colgante con **`do`/`end` como bloque
genérico**:

```pli
if a then do;
   x = 1;
   y = 2;
end;
else do;
   x = 3;
end;
```

`do; ... end;` agrupa sentencias sin ser un bucle, que es exactamente lo que hacen `begin`/`end` en
Pascal y las llaves en C. Que la misma palabra sirva para el bucle y para el bloque es económico y
confunde al principio.

Y PL/I tiene una construcción propia que conviene conocer al leer código antiguo: **`begin` block**,
que además de agrupar **crea un ámbito nuevo** con su propio almacenamiento automático, y puede
llevar sus propias declaraciones y manejadores `ON`. Es el `declare` block de Ada y el bloque de C++,
con la diferencia de que en PL/I es más pesado —implica activar un marco de pila— y por eso se
prefería `do; end;` para el agrupamiento simple.
"""),
        "mumps": ("""
NOTAS ; Notas -- clase 059
 read score
 set nota = $select(score>=90 : "A", score>=80 : "B", score>=70 : "C", 1 : "F")
 write "nota=", nota, !
 quit
""", """
**Lo que esta clase enseña en M.** `$select` resuelve la cadena entera **en una expresión**, sin
`if`, sin bloques y sin anidamiento. Recorre los pares `condición : valor` de izquierda a derecha,
devuelve el primero cuya condición sea cierta, y el `1 :` final hace de `else` porque `1` siempre es
verdadero.

Y —esto es lo importante— **evalúa perezosamente**: no calcula los valores de las ramas que no gana.
Es `cond` de Lisp con forma de función, y cubre el 90 % de los usos del `if` en código M real.

Si ninguna condición se cumple y no hay rama final, `$select` **levanta un error**, no devuelve vacío.
Es una de las pocas cosas en M que fallan ruidosamente, y es deliberado: un `$select` sin caso por
defecto significa que el programador afirmaba que uno de los casos siempre se daría.

Para el anidamiento con bloques, M usa el **nivel de puntos**, que es único entre los lenguajes de
esta página:

```mumps
 if score>0 do
 . write "positivo",!
 . if score>100 do
 . . write "fuera de rango",!
 . write "fin del bloque",!
```

Un punto por nivel, al principio de la línea. No hay llaves ni `end`: la profundidad **es** la
indentación, hecha obligatoria y contada por el intérprete. Es la misma idea que Python adoptaría
treinta años después, con una notación mucho más difícil de leer.
"""),
        "smalltalk": ("""
| score nota |

score := stdin nextLine trimBoth asNumber.

nota := score >= 90
    ifTrue:  [ 'A' ]
    ifFalse: [ score >= 80
        ifTrue:  [ 'B' ]
        ifFalse: [ score >= 70 ifTrue: [ 'C' ] ifFalse: [ 'F' ] ] ].

Transcript show: 'nota=', nota; cr.
""", """
**Lo que esta clase enseña en Smalltalk.** El anidamiento de tres niveles de este programa es
**incómodo a propósito**, y la comunidad lo lee como una señal. Cuando un método acumula
condicionales anidados, la respuesta idiomática no es aplanarlos: es **quitarlos**.

Y para una tabla de tramos, la forma que un programador Smalltalk escribiría de verdad convierte las
condiciones en **datos**:

```smalltalk
| tramos |
tramos := { 90 -> 'A'. 80 -> 'B'. 70 -> 'C'. 0 -> 'F' }.
nota := (tramos detect: [ :par | score >= par key ]) value.
```

`{ ... }` es un array construido en ejecución, `->` crea una **asociación** clave-valor, y `detect:`
devuelve el primer elemento que cumple el bloque. La cadena de condiciones desaparece: queda una
tabla y una búsqueda.

Es exactamente la misma técnica que aparece en las versiones de Tcl y C++ de esta clase, y aquí es
especialmente natural porque los bloques y las colecciones son el vocabulario básico del lenguaje.

Y `detect:` tiene un pariente que conviene conocer: `detect:ifNone:`, que recibe un bloque para el
caso de que ninguno cumpla. Sin él, `detect:` **levanta una excepción** si no encuentra nada — la
misma decisión que `$select` en M: la ausencia de caso por defecto se considera un error del
programador, no un resultado.
"""),
    },
)

# ---------------------------------------------------------------------------
# 060 — Expresiones condicionales: ternario e `if` como expresión
# ---------------------------------------------------------------------------
SPECS["060"] = dict(
    gancho="""
El mayor de dos números. El ejercicio elegido porque la diferencia entre resolverlo con una
**sentencia** y resolverlo con una **expresión** se ve en una línea: `if` decide *qué se ejecuta*,
mientras que una expresión condicional decide *qué valor tiene esto*. Y de esa distinción depende que
puedas escribir `const` en la variable que recibe el resultado.
""",
    porque="""
Aquí el concepto es **la diferencia entre sentencia y expresión**, y estos lenguajes lo enseñan
porque están en los dos bandos. En **Lisp** y **Smalltalk** la distinción **no existe**: todo es una
expresión y todo devuelve un valor, así que el condicional siempre ha sido asignable. En **COBOL**,
**PL/I** y **RPG** no hay ternario en absoluto: hay que declarar la variable y asignarla dentro de
cada rama.

Y en medio, **Ada** y **Fortran** ilustran la vía alternativa: en vez de un operador ternario,
**funciones y atributos** —`Integer'Max`, `max()`, `merge()`— que resuelven el caso concreto sin
necesidad de sintaxis condicional.
""",
    cierre="""
Lo transferible es que **una expresión condicional permite inicializar y sellar en una sola
sentencia**. `const int m = a > b ? a : b;` declara, calcula y prohíbe futuras modificaciones a la
vez; la versión con `if` obliga a declarar sin valor y confiar en que todas las ramas asignen. Por
eso Rust, Kotlin y Scala convirtieron `if` en expresión, y por eso Python añadió `a if c else b`. Los
lenguajes de esta página muestran de dónde venía la necesidad.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. MAXIMO.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  TXT-A   PIC X(20).
01  TXT-B   PIC X(20).
01  A       PIC S9(9) COMP-3.
01  B       PIC S9(9) COMP-3.
01  MAYOR   PIC S9(9) COMP-3.
01  ED-M    PIC -(9)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    UNSTRING LINEA DELIMITED BY ALL SPACES INTO TXT-A TXT-B
    MOVE FUNCTION NUMVAL(TXT-A) TO A
    MOVE FUNCTION NUMVAL(TXT-B) TO B

    COMPUTE MAYOR = FUNCTION MAX(A, B)

    MOVE MAYOR TO ED-M
    DISPLAY "max=" FUNCTION TRIM(ED-M)
    STOP RUN.
""", """
**Lo que esta clase enseña en COBOL.** **COBOL no tiene operador ternario ni `if` como expresión.**
Un `IF` es una sentencia que ejecuta cosas; no devuelve nada. Sin las funciones intrínsecas habría
que escribir:

```cobol
IF A > B
    MOVE A TO MAYOR
ELSE
    MOVE B TO MAYOR
END-IF
```

Cuatro líneas, una variable declarada antes sin valor, y ninguna garantía de que todas las ramas la
asignen.

Lo que COBOL ofrece en su lugar son las **funciones intrínsecas**, incorporadas en COBOL-85, y son
más de las que la gente recuerda:

```cobol
FUNCTION MAX(A, B, C)          *> acepta CUALQUIER número de argumentos
FUNCTION MIN(TABLA(ALL))       *> ¡y una tabla entera con ALL!
FUNCTION SUM(VENTAS(ALL))
FUNCTION MEAN(NOTAS(ALL))
FUNCTION ORD-MAX(A, B, C)      *> la POSICIÓN del mayor, no su valor
```

`FUNCTION MAX(TABLA(ALL))` sobre un array completo es notable: es una operación sobre una colección
entera, sin bucle, en un lenguaje de 1985. Es la misma idea que `max()` de Fortran sobre arrays y que
`inject:into:` de Smalltalk, y la razón es la misma — el dominio del lenguaje está lleno de
totalizar, promediar y buscar máximos sobre tablas.
"""),
        "fortran": ("""
program maximo
   implicit none
   integer :: a, b

   read(*, *) a, b

   write(*, '(A,I0)') 'max=', max(a, b)
end program maximo
""", """
**Lo que esta clase enseña en Fortran.** Fortran **tampoco tiene ternario**, y su respuesta es la más
característica del lenguaje: **funciones elementales**.

`max(a, b)` no es una función normal. Es **elemental**, lo que significa que se aplica igual a
escalares y a arrays, elemento a elemento:

```fortran
max(3, 7)                 ! 7
max(a, b, c, d)           ! cualquier número de argumentos
max(vector1, vector2)     ! un ARRAY con el mayor de cada posición
max(matriz, 0.0)          ! pone a cero todos los negativos de una matriz
```

Esa última línea es el idioma que hace innecesario el condicional: en vez de recorrer y comparar,
aplicas la operación a la estructura entera. Es la mentalidad vectorizada de la clase 043, aplicada
al control de flujo.

Y para el caso general, Fortran tiene **`merge`**, que es lo más parecido a un ternario que ofrece:

```fortran
merge(a, b, a > b)              ! el ternario de Fortran
merge(v, 0.0, v > 0.0)          ! sobre un array: pone a cero los no positivos
```

`merge` es también elemental, así que la condición puede ser **un array de lógicos** y la selección se
hace posición a posición. Es una operación sin ramas, que el compilador puede vectorizar — que es
exactamente por lo que existe. En un bucle de mil millones de vueltas, un `if` rompe la
segmentación del procesador y `merge` no.
"""),
        "ada": ("""
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Maximo is
   A, B : Integer;
begin
   Get (A);
   Get (B);

   --  Integer'Max es un ATRIBUTO del tipo. También valdría la expresión
   --  condicional de Ada 2012:  (if A > B then A else B)
   Put ("max=");
   Put (Integer'Max (A, B), Width => 1);
   New_Line;
end Maximo;
""", """
**Lo que esta clase enseña en Ada.** Ada tiene **las dos** respuestas, y compararlas es instructivo.

La primera es `Integer'Max (A, B)`: un **atributo del tipo**, no una función de biblioteca. Cada tipo
escalar trae `'Max`, `'Min`, `'Succ`, `'Pred`, `'First`, `'Last`, `'Image`, `'Value`, `'Range`… Si
defines `type Metros is new Float`, `Metros'Max` existe automáticamente y **devuelve un `Metros`**, no
un `Float`. Los atributos se heredan con el tipo, cosa que una función genérica tendría que
instanciar.

La segunda llegó con **Ada 2012**: las **expresiones condicionales**, que exigen paréntesis
obligatorios.

```ada
M : constant Integer := (if A > B then A else B);
X : constant String  := (case Dia is when Sabado | Domingo => "finde",
                                     when others           => "laborable");
```

Los paréntesis no son opcionales, y esa exigencia es muy propia de Ada: **hacen imposible confundir
la expresión con la sentencia** al leer, y evitan cualquier ambigüedad de precedencia.

Lo importante es lo que habilitó esa incorporación: **poder declarar `constant`**. Antes de 2012, una
variable cuyo valor dependía de una condición tenía que declararse sin valor y asignarse en un `if`,
así que no podía ser constante. La expresión condicional no se añadió por brevedad — se añadió para
que más cosas pudieran ser inmutables.
"""),
        "pascal": ("""
program Maximo;
{$MODE OBJFPC}{$H+}
uses SysUtils, Math;

var
  A, B: Integer;

begin
  Read(A, B);

  WriteLn('max=', IntToStr(Max(A, B)));
end.
""", """
**Lo que esta clase enseña en Pascal.** El Pascal ISO **no tiene ternario**, y Free Pascal y Delphi
añadieron `Max` y `Min` en la unidad `Math`, además de una función `IfThen` que parece un ternario y
**no lo es**:

```pascal
uses Math, StrUtils;

X := IfThen(A > B, A, B);              { versión de Math, para enteros }
S := IfThen(Cond, 'sí', 'no');         { versión de StrUtils, para cadenas }
```

Y aquí está la trampa que esta clase debe señalar: **`IfThen` es una función normal, así que evalúa
sus tres argumentos siempre**. Un ternario de verdad no evalúa la rama que no se toma.

```pascal
X := IfThen(Divisor <> 0, Dividendo div Divisor, 0);   { ¡DIVISIÓN POR CERO! }
```

Esa línea **falla** cuando `Divisor` es cero, porque la división se evalúa antes de llamar a
`IfThen`. En C, `d != 0 ? n / d : 0` es correcto. Es exactamente la diferencia entre una función y
una construcción de control, y es la misma razón por la que `and:` de Smalltalk necesita un bloque y
por la que `and` de Lisp es una macro.

Delphi 10.4 añadió por fin la expresión condicional real —`var m := if a > b then a else b`—, y Free
Pascal la ofrece con el modificador de modo correspondiente. Pero el `IfThen` de la biblioteca sigue
ahí, y sigue siendo una trampa para quien lo confunde con un ternario.
"""),
        "lisp": ("""
(let* ((a (read))
       (b (read)))
  (format t "max=~D~%" (max a b)))
""", """
**Lo que esta clase enseña en Common Lisp.** En Lisp **la distinción entre sentencia y expresión no
existe**. Todo es una expresión, todo devuelve un valor, y por tanto `if` **siempre** ha sido
asignable:

```lisp
(let ((m (if (> a b) a b))) ...)          ; el if devuelve un valor
(setf x (cond (c1 v1) (c2 v2) (t v3)))    ; cond también
(setf y (case k (1 'uno) (t 'otro)))      ; y case
(setf z (progn (log "hola") 42))          ; incluso un bloque: vale su última forma
```

No hay un `if` que ejecute y otro que devuelva: hay uno solo. Y `when` y `unless`, que son `if` sin
la rama contraria, devuelven `nil` cuando no se cumplen — así que también son expresiones.

Esa uniformidad es lo que Rust, Kotlin, Scala y Ruby adoptaron después, y viene de aquí. La razón por
la que casi todos los lenguajes de los 70 y 80 separaron sentencia de expresión es la máquina: una
sentencia se compilaba a un salto y una expresión a un valor en un registro, y unificarlas costaba.
Lisp lo hizo desde el principio porque su modelo era el cálculo lambda, no la máquina.

`max` en Lisp acepta cualquier número de argumentos y **funciona sobre toda la torre numérica** de la
clase 043: `(max 1/2 0.3 7)` compara una fracción, un real y un entero y devuelve el 7.
"""),
        "tcl": ("""
gets stdin linea
lassign [split [string trim $linea]] a b

puts "max=[expr {max($a, $b)}]"
""", """
**Lo que esta clase enseña en Tcl.** Dentro de `expr`, Tcl **sí tiene el ternario de C** —`c ? a : b`—
y desde la versión 8.5 también las funciones `max()` y `min()` con cualquier número de argumentos.

Fuera de `expr` no hay ninguna de las dos cosas, porque fuera de `expr` no hay operadores. Y eso
produce una asimetría que conviene tener clara:

```tcl
set m [expr {$a > $b ? $a : $b}]     ;# ternario: dentro de expr
set m [expr {max($a, $b)}]           ;# función: dentro de expr
if {$a > $b} { set m $a } else { set m $b }   ;# comando: fuera
```

Las tres formas hacen lo mismo. La primera y la segunda son **expresiones** y se pueden usar donde se
espera un valor; la tercera es un comando que además **devuelve un valor** —el de la última sentencia
del cuerpo ejecutado—, así que en Tcl incluso el `if` es asignable:

```tcl
set m [if {$a > $b} { set _ $a } else { set _ $b }]
```

Funciona, aunque nadie lo escribe así. La razón de que funcione es la misma de siempre: **en Tcl todo
comando devuelve una cadena**, incluido `if`, `while` y `proc`. La distinción sentencia/expresión no
existe porque no hay más que comandos, cada uno con su resultado.
"""),
        "perl": ("""
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;
my ($x, $y) = split ' ', $linea;

my $mayor = $x > $y ? $x : $y;

print "max=$mayor\\n";
""", """
**Lo que esta clase enseña en Perl.** Perl tiene el ternario de C y, además, algo que casi ningún
lenguaje de esta página ofrece: **el ternario es asignable**.

```perl
($x > $y ? $x : $y) = 0;      # pone a cero la MAYOR de las dos variables
```

Eso funciona porque en Perl el ternario devuelve un **lvalue** —una referencia al sitio, no una
copia— cuando ambas ramas lo son. Es la misma capacidad que tiene `substr` en la clase 048, y muestra
una idea de fondo de Perl: las construcciones devuelven *lugares*, no solo valores.

Perl también tiene una versión de esta clase que es más idiomática para más de dos elementos, y viene
de la biblioteca estándar:

```perl
use List::Util qw(max min sum first reduce any all none);

my $mayor = max @numeros;
my $total = sum @numeros;
my $primero = first { $_ > 100 } @numeros;
my $hay = any { $_ < 0 } @numeros;
```

`List::Util` está en el núcleo desde 2001 y sus funciones están escritas en C, así que son rápidas.
`first`, `any`, `all` y `none` **cortocircuitan**: paran en cuanto tienen la respuesta. Es la
biblioteca de orden superior que la clase 068 estudiará a fondo, disponible aquí para resolver el
caso concreto sin escribir un condicional.
"""),
        "cpp": ("""
#include <algorithm>
#include <iostream>

int main() {
    int a{}, b{};
    if (!(std::cin >> a >> b)) return 1;

    const int mayor = std::max(a, b);

    std::cout << "max=" << mayor << '\\n';
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** La palabra clave de este programa es **`const`**. `const int
mayor = std::max(a, b);` declara, calcula y **sella** en una sola línea. Con un `if` habría que
escribir `int mayor;` sin valor y asignarlo en las ramas, perdiendo la constancia y abriendo la
posibilidad de que alguna rama no asigne.

Esa es la razón práctica por la que las expresiones condicionales importan, y explica por qué el C++
moderno prefiere el ternario o una lambda inmediatamente invocada cuando la lógica es más compleja:

```cpp
const int mayor = a > b ? a : b;

const auto categoria = [&] {          // lambda invocada al vuelo
    if (score >= 90) return "A";
    if (score >= 80) return "B";
    return "F";
}();                                   // <- se llama aquí mismo
```

Ese patrón —conocido como *IIFE*— convierte una cadena de `if` en una expresión, permitiendo
`const`. Es el sustituto del `if` como expresión en un lenguaje que no lo tiene.

Y un aviso sobre `std::max`: **devuelve una referencia constante**, así que
`const auto& m = std::max(f(), g());` deja una referencia colgante si los argumentos son temporales.
Con `auto` a secas —copiando— no hay problema. Es un caso clásico y sutil que aparece en cuanto se
mezcla `auto&` con funciones que devuelven referencias.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi MAXIMO;
  a int(10) const;
  b int(10) const;
end-pi;

dcl-s mayor  int(10);
dcl-s salida char(30);

if a > b;
  mayor = a;
else;
  mayor = b;
endif;

salida = 'max=' + %char(mayor);
dsply salida;

*inlr = *on;
return;
""", """
**Lo que esta clase enseña en RPG.** **RPG no tiene ternario ni `if` como expresión**, así que hay
que declarar la variable y asignarla en las ramas. Es la misma situación que COBOL y PL/I, y por el
mismo motivo: los tres nacieron cuando la sentencia y la expresión eran cosas distintas también en la
máquina.

Lo que RPG sí tiene, y viene al caso, son funciones incorporadas sobre **matrices**:

```rpgle
dcl-s ventas packed(11:2) dim(12);

total = %sum(ventas);            // suma de todos los elementos
mayor = %max(ventas);            // el mayor
posicion = %lookup(buscado : ventas);   // búsqueda, devuelve el índice
```

`%sum`, `%max`, `%min` y `%lookup` sobre matrices completas son la misma idea que
`FUNCTION SUM(TABLA(ALL))` de COBOL y `max(array)` de Fortran: **operar sobre la colección entera sin
escribir el bucle**. Los tres lenguajes de negocio y cálculo de esta página llegaron a la misma
solución, porque totalizar tablas es lo que hacen todo el día.

Y para elegir entre dos valores, el idioma de RPG es `%max(a : b)` con la forma de dos argumentos,
que evita el `if` de este programa — aunque sigue sin ser una expresión condicional general.
"""),
        "pli": ("""
 maximo: procedure options(main);

    declare (a, b) fixed binary(31);

    get list (a, b);

    put skip list ('max=' || trim(char(max(a, b))));

 end maximo;
""", """
**Lo que esta clase enseña en PL/I.** PL/I **no tiene ternario**, pero su catálogo de funciones
incorporadas es enorme y cubre este caso y muchos más: `max`, `min`, `abs`, `sign`, `sum`, `prod`,
`any`, `all`, `poly`…

Dos de ellas merecen atención en esta clase porque operan sobre **cadenas de bits**, que es la forma
que PL/I tiene de trabajar con varias condiciones a la vez:

```pli
declare condiciones bit(8);

if any(condiciones) then ...     /* ¿alguno de los 8 bits está a 1? */
if all(condiciones) then ...     /* ¿todos? */
```

`any` y `all` sobre una cadena de bits son el equivalente de los cuantificadores `for all` y
`for some` de Ada de la clase 057, y de `any`/`all` de List::Util en Perl. Con 32 condiciones
empaquetadas en un `bit(32)`, comprobarlas todas es una sola instrucción.

Es un ejemplo del patrón que recorre toda esta sección: **PL/I no tenía la construcción de control,
tenía la operación sobre datos**. Y en muchos casos la operación sobre datos es mejor, porque
paraleliza; en otros, obliga a evaluarlo todo cuando bastaría con lo primero. Esa es exactamente la
frontera entre `any` de PL/I y `first` de Perl, que cortocircuita.
"""),
        "mumps": ("""
MAXIMO ; Maximo -- clase 060
 read linea
 set a = $piece(linea, " ", 1)
 set b = $piece(linea, " ", 2)
 set mayor = $select(a > b : a, 1 : b)
 write "max=", mayor, !
 quit
""", """
**Lo que esta clase enseña en M.** **`$select` es el ternario de M**, y es más general que el `?:` de
C porque admite cualquier número de pares:

```mumps
set nivel = $select(x>90 : "alto", x>50 : "medio", x>0 : "bajo", 1 : "nulo")
```

Es una expresión, devuelve un valor, evalúa perezosamente y encadena tantos casos como quieras. En un
lenguaje sin ternario ni `if` asignable, `$select` cubre las dos necesidades.

Y M tiene una segunda pieza que resuelve esta clase de otra manera, y que es muy suya: **`$order` y
la ordenación de las claves**. Como los subíndices de un array se guardan en orden, el máximo de un
conjunto no se calcula, **se consulta**:

```mumps
 set ^TMP(3)="", ^TMP(7)="", ^TMP(5)=""
 write $order(^TMP(""), -1)      ; 7 -- el ÚLTIMO subíndice: el máximo
 write $order(^TMP(""))          ; 3 -- el PRIMERO: el mínimo
```

El `-1` recorre en orden inverso. En una base de datos con un millón de nodos, obtener el máximo es
una operación de índice, no un recorrido. Es la misma ventaja que da un índice B-tree en SQL, con la
diferencia de que aquí no hay que declararlo: **el orden es una propiedad del almacenamiento**.
"""),
        "smalltalk": ("""
| partes a b |

partes := stdin nextLine substrings collect: [ :cada | cada asNumber ].
a := partes first.
b := partes second.

Transcript show: 'max=', (a max: b) printString; cr.
""", """
**Lo que esta clase enseña en Smalltalk.** `a max: b` es **un mensaje enviado al número**, y como todo
mensaje devuelve un valor, la distinción de esta clase sencillamente no se plantea: en Smalltalk
**todo es una expresión**.

`ifTrue:ifFalse:` devuelve el valor del bloque que se evaluó, así que es asignable sin ninguna
sintaxis especial:

```smalltalk
mayor := a > b ifTrue: [ a ] ifFalse: [ b ].
etiqueta := score > 50 ifTrue: [ 'apto' ] ifFalse: [ 'no apto' ].
```

Y lo mismo vale para el resto de estructuras de control: `whileTrue:` devuelve `nil`, `to:do:`
devuelve el receptor, `detect:ifNone:` devuelve el elemento encontrado. **No hay ninguna construcción
del lenguaje que no devuelva algo**, porque todas son envíos de mensajes y un mensaje siempre
responde.

La implementación de `max:` es, como cabe esperar, una línea que puedes abrir y leer:

```smalltalk
Magnitude >> max: unaMagnitud
    ^ self > unaMagnitud ifTrue: [ self ] ifFalse: [ unaMagnitud ]
```

Está en `Magnitude`, la superclase abstracta de todo lo que se puede comparar —números, caracteres,
fechas, cadenas—. Basta con implementar `<` en una clase nueva para heredar `max:`, `min:`,
`between:and:` y el resto del protocolo de comparación. Es la misma economía que el `Comparable` de
Java, veinte años antes.
"""),
    },
)

# ---------------------------------------------------------------------------
# 061 — switch / case y fallthrough
# ---------------------------------------------------------------------------
SPECS["061"] = dict(
    gancho="""
Traducir un número del 1 al 7 al nombre de un día. El `switch` de toda la vida, y con él la pregunta
que ha costado más errores en la historia de C: **¿qué pasa si olvidas el `break`?** Los lenguajes de
esta página responden casi todos lo mismo —**no pasa nada, porque el paso a la siguiente rama no
existe**— y saber que C es la excepción, y no la regla, cambia cómo se lee.
""",
    porque="""
Aquí el concepto es la **selección múltiple**, y estos lenguajes lo enseñan porque **ninguno tiene
*fallthrough*** y varios ofrecen bastante más que un `switch`. El `EVALUATE` de COBOL admite rangos
`THRU`, comodines `ANY` y **varios sujetos a la vez**. El `case` de Ada **obliga a cubrir todos los
valores del tipo** y no compila si falta uno. El `select case` de Fortran y el `case` de Pascal
aceptan rangos.

Y **Smalltalk no tiene `switch` en absoluto**, deliberadamente: su respuesta es un diccionario o
polimorfismo, que es la refactorización que hoy recomienda cualquier guía de diseño.
""",
    cierre="""
Dos ideas que llevarse. La primera: **el *fallthrough* de C es un accidente histórico**, no un
requisito de los lenguajes de selección; heredado de la implementación como tabla de saltos, ha
sobrevivido por compatibilidad, y C++17 tuvo que añadir `[[fallthrough]]` para distinguir el
intencionado del olvidado. La segunda: **la exhaustividad comprobada por el compilador —el `case` de
Ada— es una garantía enorme**, porque al añadir un valor nuevo al enumerado, el compilador te lleva a
todos los sitios donde falta tratarlo. Es lo que hoy dan `match` de Rust y `when` de Kotlin.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. DIAS.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA    PIC X(80).
01  D        PIC S9(9) COMP-3.
01  NOMBRE   PIC X(10).

PROCEDURE DIVISION.
    ACCEPT LINEA
    MOVE FUNCTION NUMVAL(LINEA) TO D

    EVALUATE D
        WHEN 1      MOVE "lunes"     TO NOMBRE
        WHEN 2      MOVE "martes"    TO NOMBRE
        WHEN 3      MOVE "miercoles" TO NOMBRE
        WHEN 4      MOVE "jueves"    TO NOMBRE
        WHEN 5      MOVE "viernes"   TO NOMBRE
        WHEN 6      MOVE "sabado"    TO NOMBRE
        WHEN 7      MOVE "domingo"   TO NOMBRE
        WHEN OTHER  MOVE "invalido"  TO NOMBRE
    END-EVALUATE

    DISPLAY "dia=" FUNCTION TRIM(NOMBRE)
    STOP RUN.
""", """
**Lo que esta clase enseña en COBOL.** **`EVALUATE` no tiene *fallthrough*.** Ejecuta la rama que
casa y sale; no hace falta `break` y no se puede olvidar. Ese solo hecho elimina una familia entera de
errores que en C hay que vigilar con avisos del compilador.

Y `EVALUATE` es considerablemente más potente que un `switch`. Además del `EVALUATE TRUE` de la clase
058, admite:

```cobol
EVALUATE D
    WHEN 1 THRU 5              MOVE "laborable" TO TIPO    *> RANGOS
    WHEN 6 ALSO 7              ...                          *> varios valores
END-EVALUATE

EVALUATE TIPO ALSO IMPORTE ALSO TRUE
    WHEN "VIP" ALSO 1000 THRU 9999 ALSO URGENTE  PERFORM EXPRES
    WHEN "VIP" ALSO ANY            ALSO ANY      PERFORM NORMAL
    WHEN ANY   ALSO 0 THRU 99      ALSO ANY      PERFORM RECOGIDA
    WHEN OTHER                                   PERFORM REVISAR
END-EVALUATE
```

Ese segundo bloque es una **tabla de decisión** con tres dimensiones: rangos con `THRU`, comodines con
`ANY` y sujetos combinados con `ALSO`. Es lo más cercano a la coincidencia de patrones moderna que
existía en 1985, y sigue sin tener equivalente directo en Java o C#.

Su origen es revelador: las **tablas de decisión** eran una técnica formal de análisis de negocio de
los años 60 —filas de condiciones, columnas de casos— y `EVALUATE` se diseñó para poder escribirlas
tal cual en el programa. El lenguaje copió la herramienta que ya usaban los analistas.
"""),
        "fortran": ("""
program dias
   implicit none
   integer :: d
   character(len=10) :: nombre

   read(*, *) d

   select case (d)
   case (1)
      nombre = 'lunes'
   case (2)
      nombre = 'martes'
   case (3)
      nombre = 'miercoles'
   case (4)
      nombre = 'jueves'
   case (5)
      nombre = 'viernes'
   case (6)
      nombre = 'sabado'
   case (7)
      nombre = 'domingo'
   case default
      nombre = 'invalido'
   end select

   write(*, '(A,A)') 'dia=', trim(nombre)
end program dias
""", """
**Lo que esta clase enseña en Fortran.** `select case` llegó con **Fortran 90** y sustituyó a algo
mucho peor: el **`GO TO` calculado**, que era la forma de hacer una selección múltiple en el Fortran
clásico.

```fortran
      GO TO (10, 20, 30, 40, 50, 60, 70), D     ! salta a la etiqueta D-ésima
   10 NOMBRE = 'lunes'
      GO TO 99
   20 NOMBRE = 'martes'
      GO TO 99
```

Una lista de etiquetas y un índice. Es literalmente una **tabla de saltos** escrita a mano — que es
exactamente lo que el compilador de C genera para un `switch`, y de donde viene el *fallthrough*: si
olvidabas el `GO TO 99`, caías en la etiqueta siguiente. **El paso a la siguiente rama no es una
característica de diseño, es el comportamiento por defecto de una tabla de saltos.** C lo conservó;
Fortran lo eliminó al pasar a `select case`.

Y `select case` de Fortran acepta **rangos y listas**, cosa que el de C nunca ha tenido:

```fortran
case (1:5)          ! del 1 al 5
case (6, 7)         ! lista de valores
case (:0)           ! todo lo menor o igual que 0
case (100:)         ! todo lo mayor o igual que 100
```

Sin *fallthrough* y con rangos, el `select case` cubre los casos por los que en C se abusaba de la
caída entre ramas.
"""),
        "ada": ("""
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Dias is
   D : Integer;
begin
   Get (D);

   case D is
      when 1      => Put_Line ("dia=lunes");
      when 2      => Put_Line ("dia=martes");
      when 3      => Put_Line ("dia=miercoles");
      when 4      => Put_Line ("dia=jueves");
      when 5      => Put_Line ("dia=viernes");
      when 6      => Put_Line ("dia=sabado");
      when 7      => Put_Line ("dia=domingo");
      when others => Put_Line ("dia=invalido");
   end case;
end Dias;
""", """
**Lo que esta clase enseña en Ada.** **El `case` de Ada obliga a cubrir todos los valores posibles del
tipo, y si falta alguno no compila.** Aquí el `when others` es obligatorio porque `D` es un `Integer`
y sus valores son millones. Pero con un enumerado, la garantía se vuelve muy valiosa:

```ada
type Dia is (Lunes, Martes, Miercoles, Jueves, Viernes, Sabado, Domingo);

case Hoy is
   when Lunes .. Viernes => Put_Line ("laborable");
   when Sabado           => Put_Line ("sábado");
   --  falta Domingo:  ERROR DE COMPILACIÓN
end case;
```

Y esto es lo importante: **el día que añadas `Festivo` al enumerado, el compilador te llevará a todos
los `case` del sistema donde falte tratarlo**. No hay que buscarlos; salen solos. Es la mejor
herramienta de refactorización que da un sistema de tipos, y es la razón de que las guías de Ada
desaconsejen `when others` con enumerados: al ponerlo, renuncias a la comprobación.

Es exactamente lo que hoy ofrecen `match` de Rust, `when` de Kotlin y los `sealed` de Java, y Ada lo
tenía en 1983.

El `case` de Ada admite además rangos (`when 1 .. 5`), listas alternativas (`when Sabado | Domingo`)
y —desde Ada 2012— existe también como **expresión**, con `(case X is when ... => valor)`, que enlaza
con la clase 060. Y no tiene *fallthrough*: cada rama termina donde empieza la siguiente.
"""),
        "pascal": ("""
program Dias;
{$MODE OBJFPC}{$H+}

var
  D: Integer;
  Nombre: string;

begin
  Read(D);

  case D of
    1: Nombre := 'lunes';
    2: Nombre := 'martes';
    3: Nombre := 'miercoles';
    4: Nombre := 'jueves';
    5: Nombre := 'viernes';
    6: Nombre := 'sabado';
    7: Nombre := 'domingo';
  else
    Nombre := 'invalido';
  end;

  WriteLn('dia=', Nombre);
end.
""", """
**Lo que esta clase enseña en Pascal.** El `case` de Pascal **no tiene *fallthrough*** y acepta
**rangos y listas** desde 1970, treinta años antes de que C# los incorporara:

```pascal
case C of
  'a'..'z', 'A'..'Z': Tipo := 'letra';      { rangos Y lista, juntos }
  '0'..'9':           Tipo := 'digito';
  ' ', #9, #10, #13:  Tipo := 'espacio';
else
  Tipo := 'otro';
end;
```

La restricción es que **el selector tiene que ser un tipo ordinal** —entero, carácter, booleano,
enumerado o subrango— y las etiquetas, **constantes conocidas al compilar**. No se puede hacer `case`
sobre una cadena ni sobre expresiones. Esa limitación viene de la implementación: un `case` sobre
ordinales compila a una tabla de saltos directa, sin comparaciones.

Free Pascal y Delphi levantaron parte de esa restricción y admiten `case` sobre `string`, aunque
entonces el compilador genera comparaciones o una búsqueda binaria.

Fíjate también en el `else` sin `;` delante y en el `end` que cierra el `case`: es la misma regla de
separador de la clase 059, aplicada aquí. Y en Pascal el `case` **no exige exhaustividad**: si ningún
caso encaja y no hay `else`, el comportamiento en el ISO es indefinido, mientras que Free Pascal
simplemente no hace nada. Es la diferencia con Ada, y la razón de poner siempre el `else`.
"""),
        "lisp": ("""
(let ((d (read)))
  (format t "dia=~A~%"
          (case d
            (1 "lunes")
            (2 "martes")
            (3 "miercoles")
            (4 "jueves")
            (5 "viernes")
            (6 "sabado")
            (7 "domingo")
            (otherwise "invalido"))))
""", """
**Lo que esta clase enseña en Common Lisp.** `case` compara con `eql` —identidad para números,
caracteres y símbolos— y **devuelve un valor**, así que se puede usar directamente como argumento,
como en este programa. Sin *fallthrough*, sin `break` y sin variable temporal.

Lisp tiene además **una familia entera** de construcciones de selección, cada una comparando de una
forma distinta, y elegir la correcta es parte del oficio:

| Construcción | Compara con | Para qué |
|---|---|---|
| `case` | `eql` | Números, caracteres, símbolos |
| `ccase` / `ecase` | `eql` | Igual, pero **error si no encaja** (`e` = *error*) |
| `typecase` | El **tipo** del valor | Despacho por tipo |
| `cond` | Condiciones arbitrarias | Cadena de guardas |

`ecase` es la que merece atención: es idéntica a `case` pero **señala un error si ningún caso
encaja**, en vez de devolver `nil` en silencio. Es la exhaustividad de Ada trasladada al tiempo de
ejecución, y la comunidad recomienda usarla siempre que los casos deban ser exhaustivos — porque un
`nil` silencioso se propaga y el error aparece lejos del sitio donde estaba.

`typecase` no tiene equivalente en la mayoría del núcleo: selecciona según el **tipo** del valor, y
como el sistema de tipos de Lisp incluye rangos (`(integer 0 100)`) y uniones (`(or null string)`),
resulta ser una coincidencia de patrones sobre tipos bastante expresiva.
"""),
        "tcl": ("""
gets stdin linea
set d [string trim $linea]

switch -- $d {
    1 { set nombre lunes }
    2 { set nombre martes }
    3 { set nombre miercoles }
    4 { set nombre jueves }
    5 { set nombre viernes }
    6 { set nombre sabado }
    7 { set nombre domingo }
    default { set nombre invalido }
}

puts "dia=$nombre"
""", """
**Lo que esta clase enseña en Tcl.** El `--` de `switch -- $d` no es decoración: **marca el final de
las opciones**. Sin él, si `$d` empezara por guion, `switch` lo interpretaría como una opción y
fallaría. Es una convención que recorre todo Tcl y todo Unix, y omitirla es una vulnerabilidad
clásica cuando el valor viene de fuera.

Y `switch` en Tcl es **cuatro construcciones en una**, según la opción que se le pase:

```tcl
switch -exact -- $x { ... }     ;# comparación literal (por defecto)
switch -glob  -- $x {
    "*.txt"  { ... }            ;# patrones de nombre de fichero
    "img_*"  { ... }
}
switch -regexp -- $x {
    {^[0-9]+$}     { ... }      ;# EXPRESIONES REGULARES
    {^[a-z]+@}     { ... }
}
```

Con `-regexp`, `switch` se convierte en **coincidencia de patrones de verdad** —tema de la clase
062—, con captura de grupos incluida mediante `-matchvar`. Es bastante más de lo que ofrece un
`switch` de C.

Y sí tiene una forma de *fallthrough*, pero **explícita**: un cuerpo que consista únicamente en un
guion `-` significa "usa el del siguiente caso".

```tcl
switch -- $d {
    6 -
    7 { set tipo finde }        ;# 6 y 7 comparten cuerpo
    default { set tipo laborable }
}
```

Compartir cuerpo sin poder caer por accidente: el caso legítimo del *fallthrough*, resuelto sin su
peligro.
"""),
        "perl": ("""
use strict;
use warnings;

my @dias = qw(lunes martes miercoles jueves viernes sabado domingo);

my $d = <STDIN>;
chomp $d;

my $nombre = ($d >= 1 && $d <= 7) ? $dias[$d - 1] : 'invalido';

print "dia=$nombre\\n";
""", """
**Lo que esta clase enseña en Perl.** **Perl no tiene `switch`**, y su historia es la mejor
advertencia de esta clase. Perl 5.10 introdujo `given`/`when` como característica experimental; nunca
se estabilizó, sus reglas de *coincidencia inteligente* resultaron impredecibles, y acabó **retirada
del lenguaje**.

La respuesta idiomática es la de este programa: **una estructura de datos en lugar de una
construcción de control**.

```perl
my @dias = qw(lunes martes miercoles jueves viernes sabado domingo);
my $nombre = $dias[$d - 1] // 'invalido';

# O con un hash, cuando las claves no son consecutivas:
my %accion = (
    alta  => \\&dar_alta,
    baja  => \\&dar_baja,
    mod   => \\&modificar,
);
my $f = $accion{$comando} // \\&desconocido;
$f->(@args);
```

Ese segundo bloque es una **tabla de despacho**: un hash de nombre a **referencia a función**. Añadir
un comando es añadir una entrada, no tocar un `switch`. Es la misma técnica que en Tcl, en Smalltalk
y en C++ con `std::map`, y escala mucho mejor que cualquier construcción de selección: se puede
construir en ejecución, cargar de un fichero de configuración o extender desde un plugin.

`qw(...)` es la lista de palabras sin comillas ni comas, un atajo muy usado. Y `//` es el operador de
coalescencia de nulos de la clase 053.
"""),
        "cpp": ("""
#include <iostream>

int main() {
    int d{};
    if (!(std::cin >> d)) return 1;

    const char* nombre = nullptr;
    switch (d) {
        case 1: nombre = "lunes";     break;
        case 2: nombre = "martes";    break;
        case 3: nombre = "miercoles"; break;
        case 4: nombre = "jueves";    break;
        case 5: nombre = "viernes";   break;
        case 6: nombre = "sabado";    break;
        case 7: nombre = "domingo";   break;
        default: nombre = "invalido"; break;
    }

    std::cout << "dia=" << nombre << '\\n';
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** C++ es **el único lenguaje de esta página con *fallthrough***, y
esta clase es el sitio para entender por qué. El `switch` de C no es una selección: es una **tabla de
saltos con etiquetas**. `case 3:` es literalmente una etiqueta, el `switch` salta a ella, y a partir
de ahí **la ejecución continúa hacia abajo** hasta encontrar un `break`. La caída no es una
característica que alguien diseñara: es lo que ocurre si no saltas fuera.

De ahí vienen dos cosas. La primera, el error de olvidar un `break`, que los compiladores detectan
hoy con `-Wimplicit-fallthrough`. La segunda, el **Duff's device**, esa pieza legendaria en la que un
`switch` y un `while` se entrelazan aprovechando la caída — legal, ingeniosa y absolutamente
ilegible.

C++17 añadió el atributo que separa la caída intencionada del descuido:

```cpp
switch (x) {
    case 1:
        preparar();
        [[fallthrough]];      // "esto es a propósito", y el compilador calla
    case 2:
        ejecutar();
        break;
}
```

También añadió el inicializador en el `switch` —`switch (auto v = f(); v)`— y, sobre todo, hay que
recordar la restricción de fondo: **el selector debe ser un tipo entero o enumerado**. No se puede
hacer `switch` sobre `std::string`. Para eso, la solución es la de Perl y Tcl: un `std::map` de
cadena a función, es decir, una tabla de despacho.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi DIAS;
  d int(10) const;
end-pi;

dcl-s nombres varchar(10) dim(7);
dcl-s nombre  varchar(10);
dcl-s salida  char(30);

nombres(1) = 'lunes';
nombres(2) = 'martes';
nombres(3) = 'miercoles';
nombres(4) = 'jueves';
nombres(5) = 'viernes';
nombres(6) = 'sabado';
nombres(7) = 'domingo';

if d >= 1 and d <= 7;
  nombre = nombres(d);
else;
  nombre = 'invalido';
endif;

salida = 'dia=' + nombre;
dsply salida;

*inlr = *on;
return;
""", """
**Lo que esta clase enseña en RPG.** RPG tiene `select`/`when`, sin *fallthrough*, pero para una
correspondencia número→nombre lo idiomático es una **matriz**, como en este programa. Y RPG tiene una
forma de rellenarla que no existe en ningún otro lenguaje de esta página: los **datos en tiempo de
compilación**.

```rpgle
dcl-s nombres char(10) dim(7) ctdata perrcd(1);
...
**CTDATA nombres
lunes
martes
miercoles
jueves
viernes
sabado
domingo
```

`ctdata` indica que la matriz se rellena con datos escritos **al final del propio fuente**, tras la
marca `**CTDATA`. El compilador los incrusta en el programa. Es una tabla de datos que vive en el
código, versionada con él, sin fichero externo ni código de inicialización.

Existe también `altseq` y `ftrans` para tablas de traducción de caracteres, y `dcl-s ... extfmt` para
leerlas de un fichero. Toda esa maquinaria responde a una necesidad muy concreta del dominio:
**catálogos pequeños y estables** —códigos de país, tipos de movimiento, literales por idioma— que
cambian una vez al año y no merecen una tabla en la base de datos.

Es una solución de 1969 al problema que hoy se resuelve con un fichero de recursos o un JSON
incrustado.
"""),
        "pli": ("""
 dias: procedure options(main);

    declare d      fixed binary(31);
    declare nombre character(10) varying;

    get list (d);

    select (d);
       when (1) nombre = 'lunes';
       when (2) nombre = 'martes';
       when (3) nombre = 'miercoles';
       when (4) nombre = 'jueves';
       when (5) nombre = 'viernes';
       when (6) nombre = 'sabado';
       when (7) nombre = 'domingo';
       otherwise nombre = 'invalido';
    end;

    put skip list ('dia=' || nombre);

 end dias;
""", """
**Lo que esta clase enseña en PL/I.** `select (expresión)` compara contra los valores de cada `when`
y **no tiene *fallthrough***. Es la misma construcción que ya vimos sin expresión en la clase 058:
**una sola forma sintáctica cubre el `switch` clásico y la cadena de guardas**, según lleve o no
expresión.

Esa unificación es elegante y es exactamente lo que después hicieron Ada con `case`, Rust con `match`
y Kotlin con `when`. PL/I llegó primero.

Y `when` admite **varios valores separados por comas**, lo que cubre el caso legítimo del
*fallthrough* sin su peligro:

```pli
select (d);
   when (6, 7)         tipo = 'finde';
   when (1, 2, 3, 4, 5) tipo = 'laborable';
   otherwise            tipo = 'invalido';
end;
```

Lo que PL/I **no** tiene son rangos en el `when` —nada de `1 THRU 5` como COBOL ni `1:5` como
Fortran—, así que para tramos hay que volver al `select;` sin expresión con condiciones completas.

Y si ningún `when` casa y no hay `otherwise`, PL/I levanta la condición **`ERROR`**. Como el
`$select` de M y el `ecase` de Lisp: la ausencia de caso por defecto se trata como un fallo del
programador, no como un resultado válido.
"""),
        "mumps": ("""
DIAS ; Dias de la semana -- clase 061
 read d
 set nombres = "lunes^martes^miercoles^jueves^viernes^sabado^domingo"
 set nombre = $select(d<1 : "invalido", d>7 : "invalido", 1 : $piece(nombres, "^", d))
 write "dia=", nombre, !
 quit
""", """
**Lo que esta clase enseña en M.** **M no tiene `switch`**, y su respuesta es la más característica
del lenguaje: **la tabla es una cadena con delimitadores, y `$piece` es la selección**.

`$piece("lunes^martes^...", "^", d)` devuelve el trozo *d*-ésimo. Una tabla de siete entradas cabe en
una línea, no ocupa memoria como estructura, se puede guardar en un *global* y se puede cambiar sin
tocar el código:

```mumps
 set ^CFG("dias") = "lunes^martes^miercoles^jueves^viernes^sabado^domingo"
 set nombre = $piece(^CFG("dias"), "^", d)     ; la tabla vive en la BASE DE DATOS
```

Esa segunda versión es cómo se hace de verdad en un sistema M: **la tabla de traducción está en la
base de datos**, así que cambiar los literales o añadir un idioma no requiere recompilar nada. Es la
misma idea que un fichero de recursos, con la ventaja de que en M la base de datos está siempre ahí.

Y para selecciones que no son consecutivas, el idioma es un array indexado por la clave:

```mumps
 set ^ACCION("alta")="DARALTA", ^ACCION("baja")="DARBAJA"
 do @$get(^ACCION(comando), "DESCONOCIDO")     ; @ = INDIRECCIÓN: ejecuta por nombre
```

El operador `@` es la **indirección**: toma una cadena y la usa como si fuera código. Es la tabla de
despacho de Perl, con el nombre de la rutina guardado como dato. Potentísimo, y la razón de que el
código M sea difícil de analizar estáticamente: **qué se ejecuta puede decidirse en ejecución**.
"""),
        "smalltalk": ("""
| d nombres nombre |

d := stdin nextLine trimBoth asNumber.
nombres := #('lunes' 'martes' 'miercoles' 'jueves' 'viernes' 'sabado' 'domingo').

nombre := (d between: 1 and: 7)
    ifTrue:  [ nombres at: d ]
    ifFalse: [ 'invalido' ].

Transcript show: 'dia=', nombre; cr.
""", """
**Lo que esta clase enseña en Smalltalk.** **Smalltalk no tiene `switch`, y la ausencia es
deliberada.** No es que se les olvidara: es que la comunidad considera que una selección múltiple
sobre un valor es casi siempre un síntoma de que falta polimorfismo.

Las dos respuestas idiomáticas son las de este programa y la del diccionario:

```smalltalk
"1) Indexar una colección, cuando las claves son consecutivas"
nombres at: d ifAbsent: [ 'invalido' ]

"2) Un diccionario, cuando no lo son"
acciones := Dictionary newFrom: {
    #alta -> [ self darAlta ].
    #baja -> [ self darBaja ] }.
(acciones at: comando ifAbsent: [ [ self desconocido ] ]) value.
```

El diccionario guarda **bloques**, así que es una tabla de despacho igual que el hash de referencias
a función de Perl. Se construye en ejecución, se puede modificar y se puede extender desde otro
paquete sin tocar el original.

Y la tercera respuesta, la que la comunidad considera correcta cuando el `switch` es sobre un tipo,
es **no escribir ninguna selección**:

```smalltalk
Lunes >> nombre    ^'lunes'
Sabado >> nombre   ^'sabado'
Sabado >> esFinde  ^true
Lunes >> esFinde   ^false
```

Cada clase responde por sí misma. Añadir un día nuevo es añadir una clase, no editar siete `switch`
repartidos por el sistema. Es *"reemplaza el condicional por polimorfismo"*, la refactorización que
Martin Fowler catalogó trabajando precisamente en esta comunidad.
"""),
    },
)

# ---------------------------------------------------------------------------
# 062 — Coincidencia de patrones (match / when)
# ---------------------------------------------------------------------------
SPECS["062"] = dict(
    gancho="""
Positivo, negativo o cero. Un problema de tres casos elegido porque en un lenguaje moderno se
resuelve con **coincidencia de patrones** —`match` de Rust, `when` de Kotlin, `match` de Python
3.10—, la construcción de moda de la última década. Y la pregunta de esta página es: **¿qué usaban
estos lenguajes antes de que existiera?** Las respuestas son más interesantes de lo esperable.
""",
    porque="""
Aquí el concepto es la **coincidencia de patrones**, y estos lenguajes lo enseñan porque muestran
**tres caminos distintos hacia la misma necesidad**. Uno es el de los rangos en la selección: el
`case (:-1)` de Fortran y el `when Integer'First .. -1` de Ada permiten casar tramos, no valores. Otro
es el de los **predicados con nombre**: las condiciones de signo y de clase de COBOL —`IF N IS
POSITIVE`, `IF C IS ALPHABETIC`— son patrones incorporados al lenguaje.

Y el tercero es el más sorprendente: **M tiene un operador de patrones, `?`, desde 1966**, con su
propia sintaxis para "uno o más dígitos" o "tres letras seguidas de dos números". Un mini-lenguaje de
validación anterior a las expresiones regulares de Perl.
""",
    cierre="""
Lo que se ve aquí es que la coincidencia de patrones moderna **une tres cosas que antes estaban
separadas**: seleccionar por valor (el `switch`), comprobar una forma (las expresiones regulares o el
`?` de M) y **descomponer la estructura** extrayendo sus partes. Esa tercera es la genuinamente
nueva, y viene de los lenguajes funcionales tipados —ML y Haskell—, no de esta tradición. Los
lenguajes de esta página tienen las dos primeras repartidas en construcciones distintas; verlo
explica por qué `match` se sintió como un avance real y no como azúcar sintáctico.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. SIGNO.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  N       PIC S9(9) COMP-3.
01  SIGNO-T PIC X(10).

PROCEDURE DIVISION.
    ACCEPT LINEA
    MOVE FUNCTION NUMVAL(LINEA) TO N

    EVALUATE TRUE
        WHEN N IS POSITIVE   MOVE "positivo" TO SIGNO-T
        WHEN N IS NEGATIVE   MOVE "negativo" TO SIGNO-T
        WHEN OTHER           MOVE "cero"     TO SIGNO-T
    END-EVALUATE

    DISPLAY "signo=" FUNCTION TRIM(SIGNO-T)
    STOP RUN.
""", """
**Lo que esta clase enseña en COBOL.** `N IS POSITIVE` no es una comparación abreviada: es una
**condición de signo**, una construcción del lenguaje. Y junto a ella COBOL tiene una familia entera
de **predicados incorporados** que son, en la práctica, patrones con nombre:

```cobol
IF N IS POSITIVE / NEGATIVE / ZERO           *> condiciones de SIGNO
IF CAMPO IS NUMERIC                          *> condiciones de CLASE
IF CAMPO IS ALPHABETIC / ALPHABETIC-UPPER
IF CAMPO IS NOT NUMERIC
IF TABLA(I) IS DBCS                          *> juego de caracteres de doble byte
```

`IF CAMPO IS NUMERIC` responde a "¿el contenido de este campo alfanumérico son todo dígitos?", que es
exactamente lo que en Perl se escribiría con `/^\\d+$/` y en Tcl con `string is integer`. Es
validación de forma, integrada en el lenguaje, sin biblioteca y sin expresiones regulares — porque en
1959 no existían.

Y COBOL permite **definir tus propias clases**, que es lo que más se acerca a un patrón con nombre:

```cobol
ENVIRONMENT DIVISION.
CONFIGURATION SECTION.
SPECIAL-NAMES.
    CLASS HEXADECIMAL IS "0" THRU "9", "A" THRU "F".

*> y después, en cualquier sitio:
IF CODIGO IS HEXADECIMAL ...
```

Declaras un conjunto de caracteres, le pones nombre, y se convierte en un predicado del lenguaje. No
es descomposición estructural, pero sí es **reconocimiento de forma con nombre reutilizable**, que es
la mitad de lo que hace un `match` moderno.
"""),
        "fortran": ("""
program signo
   implicit none
   integer :: n
   character(len=10) :: s

   read(*, *) n

   select case (n)
   case (:-1)
      s = 'negativo'
   case (0)
      s = 'cero'
   case (1:)
      s = 'positivo'
   end select

   write(*, '(A,A)') 'signo=', trim(s)
end program signo
""", """
**Lo que esta clase enseña en Fortran.** `case (:-1)` y `case (1:)` son **rangos abiertos**: "todo lo
menor o igual que −1" y "todo lo mayor o igual que 1". Es la forma que tiene Fortran de casar
**tramos** en lugar de valores, y con ella los tres casos de esta clase quedan cubiertos sin ningún
`if` y sin `case default`.

Esa capacidad —seleccionar por rango— es la primera de las tres piezas que la coincidencia de
patrones moderna reúne, y Fortran la tiene desde 1990.

Fortran añade además la función `sign`, que resuelve esta clase de otra manera muy suya:

```fortran
sign(1, n)        ! el valor absoluto del primero, con el SIGNO del segundo: 1 o -1
sign(1.0, -0.0)   ! -1.0 -- distingue el cero negativo del IEEE 754
```

`sign(a, b)` transfiere el signo de un número a otro. Parece una función extraña hasta que se ve para
qué existe: en cálculo numérico, aplicar el signo de una magnitud a otra sin escribir una rama es
frecuente, y **una expresión sin ramas se vectoriza y una con `if` no**. La misma motivación que
`merge` en la clase 060.

Lo que Fortran **no** tiene, como ninguno de esta página, es la tercera pieza: **descomponer una
estructura** casando su forma. Para eso hay que esperar a ML y a sus descendientes.
"""),
        "ada": ("""
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Signo is
   N : Integer;
begin
   Get (N);

   --  Los tres rangos cubren TODO Integer: no hace falta `when others`,
   --  y el compilador lo comprueba.
   case N is
      when Integer'First .. -1 => Put_Line ("signo=negativo");
      when 0                   => Put_Line ("signo=cero");
      when 1 .. Integer'Last   => Put_Line ("signo=positivo");
   end case;
end Signo;
""", """
**Lo que esta clase enseña en Ada.** Este programa **no lleva `when others`**, y eso es lo importante:
los tres rangos cubren todos los valores de `Integer`, **y el compilador lo verifica**. Si borraras
el caso del cero, no compilaría.

Esa comprobación de exhaustividad es la característica que hace valiosa la coincidencia de patrones
moderna, y Ada la tiene desde 1983 aplicada a rangos y enumerados.

Donde Ada se acerca de verdad a un `match` es en los **registros con discriminante**, que son tipos
suma comprobados:

```ada
type Figura (Clase : Tipo_Figura) is record
   case Clase is
      when Circulo    => Radio : Float;
      when Rectangulo => Ancho, Alto : Float;
      when Triangulo  => A, B, C : Float;
   end case;
end record;

case F.Clase is
   when Circulo    => Area := Pi * F.Radio ** 2;      --  solo aquí existe Radio
   when Rectangulo => Area := F.Ancho * F.Alto;
   when Triangulo  => ...
end case;
```

Acceder a `F.Radio` cuando `F.Clase` no es `Circulo` levanta `Constraint_Error`. **El tipo lleva la
etiqueta, los campos dependen de ella, y el compilador exige tratar todas las variantes.** Es
exactamente un `enum` de Rust con sus `match`, escrito con la sintaxis de 1983.

Lo único que falta frente a un `match` moderno es la **ligadura en el patrón**: aquí hay que escribir
`F.Radio`, mientras que Rust permite `Circulo { radio }` y te da la variable ya extraída.
"""),
        "pascal": ("""
program Signo;
{$MODE OBJFPC}{$H+}
uses Math;

var
  N: Integer;
  S: string;

begin
  Read(N);

  case Sign(N) of
     1: S := 'positivo';
    -1: S := 'negativo';
  else
     S := 'cero';
  end;

  WriteLn('signo=', S);
end.
""", """
**Lo que esta clase enseña en Pascal.** `Sign(N)` de la unidad `Math` devuelve `-1`, `0` o `1`, y
convierte un problema de tres tramos en un `case` de tres valores. Es una técnica general que vale la
pena reconocer: **normalizar el valor a un dominio pequeño y luego seleccionar**, en vez de comparar
tramos.

Pascal tiene además **conjuntos** como tipo del lenguaje, y son la pieza de esta clase que más se
acerca a un patrón:

```pascal
type
  TDigito = set of '0'..'9';
  TVocal  = set of Char;

const
  VOCALES: TVocal = ['a','e','i','o','u','A','E','I','O','U'];

if C in VOCALES then ...
if C in ['a'..'z', 'A'..'Z', '0'..'9'] then ...    { conjunto literal }
if Dia in [Sabado, Domingo] then ...
```

El operador **`in`** comprueba pertenencia a un conjunto, y el conjunto se escribe entre corchetes con
rangos y listas mezclados. Se implementa como una **máscara de bits**, así que la comprobación es una
sola instrucción con independencia de cuántos elementos tenga.

Es más legible que una cadena de `or`, es más rápido, y es una idea que casi ningún lenguaje posterior
copió —Delphi la mantiene, Modula-2 y Ada tienen variantes, y C, Java, Python y JavaScript no tienen
nada equivalente a nivel de lenguaje—. Para reconocer que un valor pertenece a un grupo, sigue siendo
la construcción más limpia de esta página.
"""),
        "lisp": ("""
(let ((n (read)))
  (format t "signo=~A~%"
          (cond ((plusp n)  "positivo")
                ((minusp n) "negativo")
                (t          "cero"))))
""", """
**Lo que esta clase enseña en Common Lisp.** `plusp`, `minusp` y `zerop` son **predicados con
nombre**, y la convención `-p` final —de *predicate*— recorre toda la biblioteca: `evenp`, `oddp`,
`null`, `listp`, `stringp`, `numberp`. Es la misma idea que las condiciones de clase de COBOL: dar
nombre a una comprobación de forma.

Pero donde Lisp llega más lejos que nadie en esta clase es en la **descomposición estructural**, que
es la pieza que le falta a todos los demás lenguajes de esta página:

```lisp
(destructuring-bind (nombre (calle numero) &optional (pais "ES")) datos
  ...)   ; extrae de una lista anidada, con opcionales y valores por defecto

(defun f (&key (color :rojo) tamano &rest resto) ...)   ; en la propia lambda-lista
```

`destructuring-bind` casa la **forma** de una lista y liga las partes a variables. Es exactamente lo
que hace `let (a, b) = tupla` en Rust o el desempaquetado de Python, disponible desde los años 80.

Y como Lisp permite añadir sintaxis, la coincidencia de patrones completa existe **como biblioteca**:

```lisp
(match figura
  ((list 'circulo r)        (* pi r r))
  ((list 'rect ancho alto)  (* ancho alto))
  ((guard n (numberp n))    n))
```

Eso es `trivia` u `optima`, dos bibliotecas de CPAN… perdón, de Quicklisp. **Lo notable es que
`match` no necesitó cambiar el lenguaje**: es una macro. Es la demostración práctica de para qué
sirve la homoiconicidad de la clase 041 — cuando aparece una idea nueva de diseño de lenguajes, en
Lisp se implementa como biblioteca.
"""),
        "tcl": ("""
gets stdin linea
set n [string trim $linea]

set signo [expr {$n > 0 ? "positivo" : $n < 0 ? "negativo" : "cero"}]

puts "signo=$signo"
""", """
**Lo que esta clase enseña en Tcl.** Para este caso concreto basta un ternario encadenado, pero Tcl
tiene coincidencia de patrones de verdad en dos sitios, y son de los más completos de esta página.

El primero es `switch` con `-regexp` y `-matchvar`, que **captura los grupos**:

```tcl
switch -regexp -matchvar m -- $linea {
    {^(\\d{4})-(\\d{2})-(\\d{2})$} {
        lassign $m todo anio mes dia          ;# los grupos, ya extraídos
        puts "fecha: $dia/$mes/$anio"
    }
    {^[a-z]+@[a-z.]+$} { puts "correo" }
    default            { puts "desconocido" }
}
```

Eso **sí** es reconocer una forma y descomponerla — las dos piezas que un `match` moderno reúne.

El segundo es `string match`, con patrones de estilo *glob*, mucho más baratos que una expresión
regular:

```tcl
string match "*.txt" $fichero
string match -nocase "IMG_*" $nombre
```

Y hay una tercera pieza muy propia de Tcl: **`regexp` y `regsub` asignan directamente a variables**.

```tcl
if {[regexp {(\\w+)=(\\w+)} $texto todo clave valor]} {
    ...    ;# clave y valor ya están puestas
}
```

`regexp` devuelve 1 o 0 **y** deja las capturas en las variables que le nombres. Es la combinación de
comprobar y extraer en una sola operación, que es justo el patrón que `if let` de Rust y el operador
morsa de Python vinieron a resolver décadas después.
"""),
        "perl": ("""
use strict;
use warnings;

my $n = <STDIN>;
chomp $n;

my $signo = $n > 0 ? 'positivo'
          : $n < 0 ? 'negativo'
          :          'cero';

print "signo=$signo\\n";
""", """
**Lo que esta clase enseña en Perl.** **Perl es el lenguaje que popularizó la coincidencia de patrones
sobre texto**, y su influencia es tan grande que el estándar de facto lleva su nombre: **PCRE**,
*Perl Compatible Regular Expressions*. Cuando escribes una expresión regular en Python, JavaScript,
Java, PHP, Go o C#, estás escribiendo Perl.

Lo que hizo distinta a su integración no fue tener regex —`grep` y `sed` ya las tenían—, sino que
fueran **parte de la sintaxis**:

```perl
if ($linea =~ /^(\\d{4})-(\\d{2})-(\\d{2})$/) {
    my ($anio, $mes, $dia) = ($1, $2, $3);      # capturas
}

if ($linea =~ /^(?<anio>\\d{4})-(?<mes>\\d{2})/) {
    print $+{anio};                              # capturas CON NOMBRE
}

my @todas = $texto =~ /(\\w+)=(\\w+)/g;           # todas las coincidencias
(my $limpio = $sucio) =~ s/\\s+//g;               # sustitución sobre una copia
```

`=~` es un operador, `/.../` es un literal, y `$1`, `$2` y `%+` aparecen solos. No hay que importar
nada, compilar el patrón ni consultar un objeto de coincidencia.

Perl fue además muy lejos en potencia: **recursión en los patrones** (`(?R)`) para casar estructuras
anidadas, **código incrustado** con `(?{ ... })`, y `/x` para escribir patrones en varias líneas con
comentarios. Con la recursión, una expresión regular de Perl deja de reconocer solo lenguajes
regulares —puede casar paréntesis balanceados—, lo que técnicamente ya no es una expresión regular en
el sentido de la teoría, y es una fuente inagotable de discusiones.
"""),
        "cpp": ("""
#include <iostream>

int main() {
    int n{};
    if (!(std::cin >> n)) return 1;

    const char* signo = (n > 0) ? "positivo"
                      : (n < 0) ? "negativo"
                      :           "cero";

    std::cout << "signo=" << signo << '\\n';
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** **C++ no tiene coincidencia de patrones**, y es una de las
carencias más señaladas del lenguaje. Hay una propuesta de `inspect` que lleva años en el comité y
que no ha entrado todavía.

Lo que sí llegó es la pieza de la **descomposición**, con C++17:

```cpp
auto [minimo, maximo] = std::minmax(a, b);           // descomposición estructurada
for (const auto& [clave, valor] : mapa) { ... }      // sobre un map
auto [it, insertado] = conjunto.insert(x);           // sobre un par de retorno
```

`auto [a, b] = ...` funciona sobre `std::pair`, `std::tuple`, arrays y cualquier estructura de campos
públicos. Es exactamente el `destructuring-bind` de Lisp y el `let (a, b)` de Rust.

Y para tipos suma, C++17 trajo `std::variant` con `std::visit`, que es lo más cerca que se puede
estar hoy de un `match` sin sintaxis:

```cpp
std::variant<Circulo, Rectangulo> figura = Circulo{2.0};

const double area = std::visit(overloaded{
    [](const Circulo& c)    { return 3.14159 * c.r * c.r; },
    [](const Rectangulo& r) { return r.ancho * r.alto; }
}, figura);
```

`std::visit` **comprueba la exhaustividad en tiempo de compilación**: si falta una alternativa, no
compila. Es la garantía de Ada y de Rust, obtenida mediante plantillas en lugar de sintaxis — verboso,
pero con la misma propiedad. El truco `overloaded` es una plantilla de tres líneas que hay que
escribir a mano, y su presencia en tantos proyectos es la mejor prueba de que la sintaxis hace falta.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi SIGNO;
  n int(10) const;
end-pi;

dcl-s s      varchar(10);
dcl-s salida char(30);

select;
  when n > 0;
    s = 'positivo';
  when n < 0;
    s = 'negativo';
  other;
    s = 'cero';
endsl;

salida = 'signo=' + s;
dsply salida;

*inlr = *on;
return;
""", """
**Lo que esta clase enseña en RPG.** RPG no tiene coincidencia de patrones ni expresiones regulares en
el lenguaje, y su respuesta a esta clase es `select` con condiciones. Pero tiene algo que conviene
conocer porque resuelve el mismo problema por otra vía: **el SQL embebido**.

```rpgle
exec sql
  select case when :n > 0 then 'positivo'
              when :n < 0 then 'negativo'
              else 'cero' end
    into :s
    from sysibm.sysdummy1;
```

Puede parecer un rodeo, y en este caso lo es. Pero para reconocer formas de verdad, en IBM i lo
idiomático es delegar en Db2, que sí tiene expresiones regulares:

```rpgle
exec sql
  select count(*) into :n
    from clientes
   where regexp_like(email, '^[a-z]+@[a-z.]+$');
```

`REGEXP_LIKE`, `REGEXP_SUBSTR` y `REGEXP_REPLACE` están en Db2 for i, así que **el motor de patrones
del sistema está en la base de datos, no en el lenguaje**. Es una división del trabajo muy propia de
la plataforma: RPG lleva la lógica de negocio y SQL lleva todo lo que tenga que ver con conjuntos de
datos y con texto.

Y para validación simple, RPG tiene `%check` y `%checkr`, que devuelven la primera posición cuyo
carácter **no** está en un conjunto dado — el mismo `verify` de PL/I de la clase 048, y la versión
mínima de "¿esta cadena tiene la forma esperada?".
"""),
        "pli": ("""
 signo: procedure options(main);

    declare n fixed binary(31);
    declare s character(10) varying;

    get list (n);

    select;
       when (n > 0) s = 'positivo';
       when (n < 0) s = 'negativo';
       otherwise    s = 'cero';
    end;

    put skip list ('signo=' || s);

 end signo;
""", """
**Lo que esta clase enseña en PL/I.** PL/I no tiene coincidencia de patrones, y para esta clase usa
`select;` con condiciones. Lo que sí tiene, y encaja aquí, es la función **`verify`** de la clase 048
y su compañera `search`, que son reconocimiento de forma sin expresiones regulares:

```pli
if verify(codigo, '0123456789') = 0 then       /* son TODO dígitos */
if search(texto, 'aeiou') > 0 then             /* contiene alguna vocal */
if index(texto, patron) > 0 then               /* contiene esta subcadena */
```

`verify` devuelve la posición del primer carácter que **no** pertenece al conjunto, y cero si todos
pertenecen. Con una llamada valida un campo entero, y es rapidísimo porque se compila a una
instrucción de traducción del hardware de IBM.

Esa familia —`verify`, `search`, `index`, `translate`— es la caja de herramientas de reconocimiento
de texto anterior a las expresiones regulares, y aparece en COBOL (`INSPECT`), en PL/I y en las
instrucciones del propio System/360. Cubre bien el 80 % de los casos reales de validación de campos,
que es lo que hacía falta.

Lo que no cubre es la estructura: no hay forma de decir "cuatro dígitos, un guion, dos dígitos" en
una sola expresión. Para eso hubo que esperar a que Ken Thompson llevara las expresiones regulares de
la teoría de autómatas al editor `ed`, en 1968, y a que Perl las hiciera cómodas veinte años después.
"""),
        "mumps": ("""
SIGNO ; Signo -- clase 062
 read n
 set s = $select(n > 0 : "positivo", n < 0 : "negativo", 1 : "cero")
 write "signo=", s, !
 quit
""", """
**Lo que esta clase enseña en M.** La sorpresa de esta página: **M tiene un operador de coincidencia
de patrones desde 1966**, y se escribe con una sola interrogación.

```mumps
 if x?1.N          write "uno o más dígitos",!
 if x?3N1"-"2N     write "tres dígitos, un guion, dos dígitos",!
 if x?1U.A         write "una mayúscula seguida de letras",!
 if x?.E1"@".E     write "contiene una arroba",!
 if dni?8N1U       write "DNI español: 8 números y una letra",!
```

La sintaxis es un mini-lenguaje propio: un **contador** seguido de un **código de clase**.

| Código | Significa | | Contador | Significa |
|---|---|---|---|---|
| `N` | Numérico | | `1` | Exactamente uno |
| `A` | Alfabético | | `3` | Exactamente tres |
| `U` / `L` | Mayúscula / minúscula | | `.` | Cero o más |
| `P` | Puntuación | | `1.` | Uno o más |
| `C` | Control | | `2.5` | De dos a cinco |
| `E` | Cualquiera | | | |

`8N1U` se lee "ocho numéricos y una mayúscula". Es notablemente compacto y **mucho más legible que la
expresión regular equivalente** para este tipo de validación de campos.

Es menos potente que una regex —no hay alternancia general ni capturas— y llegó **dos años antes** de
que Ken Thompson implementara las expresiones regulares en `ed`. Dos comunidades resolviendo el mismo
problema a la vez, sin conocerse, con soluciones distintas: la de la teoría de autómatas ganó, y la de
los hospitales sigue en producción.
"""),
        "smalltalk": ("""
| n signo |

n := stdin nextLine trimBoth asNumber.

signo := n > 0
    ifTrue:  [ 'positivo' ]
    ifFalse: [ n < 0 ifTrue: [ 'negativo' ] ifFalse: [ 'cero' ] ].

Transcript show: 'signo=', signo; cr.
""", """
**Lo que esta clase enseña en Smalltalk.** Smalltalk no tiene coincidencia de patrones y **su
posición es que no la necesita**, porque el problema que resuelve —despachar según la forma de un
valor— ya lo resuelve el envío de mensajes.

```smalltalk
"En vez de casar el tipo, se le pregunta al objeto"
Circulo    >> area    ^ Float pi * radio squared
Rectangulo >> area    ^ ancho * alto
```

Un `match` sobre un tipo suma y una jerarquía de clases con un método polimórfico resuelven el mismo
problema **con la extensibilidad al revés**, y esa diferencia es el fondo del asunto:

- Con **`match`**, añadir una **operación** nueva es fácil (una función más) y añadir un **caso**
  nuevo obliga a tocar todos los `match` existentes.
- Con **polimorfismo**, añadir un **caso** nuevo es fácil (una clase más) y añadir una **operación**
  nueva obliga a tocar todas las clases.

Eso se conoce como el **problema de la expresión**, y no tiene una solución que gane siempre: depende
de qué eje vaya a crecer más en tu sistema. Los lenguajes funcionales eligieron un lado, los
orientados a objetos el otro, y los modernos —Scala, Rust con *traits*, Kotlin— intentan ofrecer los
dos.

Para el caso concreto de esta clase, Smalltalk sí tiene el predicado: `n sign` devuelve `-1`, `0` o
`1`, y `n positive`, `n negative`, `n isZero`, `n even`, `n between:and:` están todos en `Number`.
Como siempre, **son mensajes que puedes leer** en el navegador de clases.

Y para texto, Pharo tiene `RxParser` y `matchesRegex:` como biblioteca — no en el lenguaje, porque en
Smalltalk casi nada está en el lenguaje.
"""),
    },
)
