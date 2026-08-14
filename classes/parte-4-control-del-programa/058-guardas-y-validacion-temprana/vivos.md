# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 058

> [⬅️ Volver a la clase 058](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Tres casos y una salida por cada uno. El patrón que se estudia aquí —**comprobar lo excepcional
primero y salir**— es el que evita la pirámide de `if` anidados, y su nombre técnico es *cláusula de
guarda*. La pregunta que separa a estos lenguajes es sencilla: **¿se puede salir de un procedimiento
por la mitad?**

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es la **salida temprana**, y estos lenguajes lo enseñan porque **la mitad de ellos
> nació cuando eso se consideraba mala práctica**. El COBOL estructurado desaconsejaba salir de un
> párrafo por el medio; Fortran tenía `RETURN` desde el principio pero su cultura era de un único punto
> de salida; y Pascal, en su forma original, **no tenía `return` en absoluto**.
>
> Enfrente, M tiene la forma más compacta que existe —`quit:condición`, la guarda en once
> caracteres— y COBOL tiene `EVALUATE TRUE`, que convierte una cadena de guardas en una tabla legible.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: un entero `edad` → stdout: `invalido` si edad<0, `menor` si edad<18, `adulto` en otro caso
- **Regla:** `guardas: edad<0 → invalido; edad<18 → menor; si no → adulto`

| stdin | esperado |
|---|---|
| `-5` | `invalido` |
| `10` | `menor` |
| `20` | `adulto` |

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
```

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

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
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
```

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

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
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
```

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

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
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
```

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

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let ((edad (read)))
  (format t "~A~%"
          (cond ((< edad 0)  "invalido")
                ((< edad 18) "menor")
                (t           "adulto"))))
```

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

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea
set edad [string trim $linea]

if {$edad < 0} {
    puts "invalido"
} elseif {$edad < 18} {
    puts "menor"
} else {
    puts "adulto"
}
```

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

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $edad = <STDIN>;
chomp $edad;

if    ($edad < 0)  { print "invalido\n" }
elsif ($edad < 18) { print "menor\n" }
else               { print "adulto\n" }
```

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
if (my ($a, $b) = $texto =~ /(\d+)-(\d+)/) { ... }
```

`my` dentro de la condición declara la variable con ámbito en el bloque. Es el mismo patrón que C++17
añadió con `if (auto x = f(); x > 0)` treinta años después.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>

int main() {
    int edad{};
    if (!(std::cin >> edad)) return 1;

    if (edad < 0) {
        std::cout << "invalido\n";
    } else if (edad < 18) {
        std::cout << "menor\n";
    } else {
        std::cout << "adulto\n";
    }
    return 0;
}
```

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
```

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

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 guardas: procedure options(main);

    declare edad fixed binary(31);

    get list (edad);

    select;
       when (edad < 0)  put skip list ('invalido');
       when (edad < 18) put skip list ('menor');
       otherwise        put skip list ('adulto');
    end;

 end guardas;
```

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

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
GUARDA ; Guardas -- clase 058
 read edad
 write:edad<0 "invalido",!
 quit:edad<0
 write:edad<18 "menor",!
 quit:edad<18
 write "adulto",!
 quit
```

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

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| edad |

edad := stdin nextLine trimBoth asNumber.

Transcript
    show: (edad < 0
        ifTrue:  [ 'invalido' ]
        ifFalse: [ edad < 18 ifTrue: [ 'menor' ] ifFalse: [ 'adulto' ] ]);
    cr.
```

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

---

## Y de vuelta a la clase

Lo transferible es que **la guarda no es un truco de estilo: reduce la profundidad de anidamiento y
pone lo excepcional al principio**, donde se revisa. La discusión sobre el "único punto de salida"
viene de una época sin `finally` ni destructores, en la que salir por el medio se llevaba por delante
la liberación de recursos. Hoy que existen RAII, `finally` y `defer`, ese argumento ha desaparecido —
pero el estilo sobrevive en el código de esa época, y conviene saber por qué está escrito así.

⏮️ [Volver a la clase 058](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
