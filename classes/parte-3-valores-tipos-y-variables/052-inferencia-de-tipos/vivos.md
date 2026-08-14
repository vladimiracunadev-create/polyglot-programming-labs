# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 052

> [⬅️ Volver a la clase 052](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Multiplicar dos enteros. El programa más corto de la Parte 3, elegido a propósito: lo único que hay
que mirar aquí es **cuánto hay que escribir antes de poder multiplicar**. Y la respuesta separa a
estos doce lenguajes en tres grupos — los que exigen declararlo todo, los que no exigen nada, y los
que deducen el tipo sin que lo digas.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es **la inferencia de tipos**, y estos lenguajes son valiosos porque muestran el
> mundo **anterior** a ella y por qué se inventó. COBOL, Fortran, Ada y Pascal obligan a declarar cada
> variable con su tipo completo: la inferencia moderna existe como reacción a esa verbosidad.
>
> Pero hay dos sorpresas. La primera: **Fortran tuvo inferencia en 1957 y la comunidad se pasó
> cuarenta años apagándola**, porque adivinar el tipo por la inicial del nombre resultó ser inferencia
> hecha mal. La segunda: **SBCL infiere tipos en Common Lisp**, un lenguaje dinámico, y avisa en
> compilación de incompatibilidades que puede demostrar. Inferir y declarar no son opuestos.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: una línea `a b` (dos enteros) → stdout: `producto=<a*b>`
- **Regla:** `producto = a * b`

| stdin | esperado |
|---|---|
| `3 4` | `producto=12` |
| `0 9` | `producto=0` |
| `-2 5` | `producto=-10` |

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
PROGRAM-ID. INFERENCIA.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA     PIC X(80).
01  TXT-A     PIC X(20).
01  TXT-B     PIC X(20).
01  A         PIC S9(9)  COMP-3.
01  B         PIC S9(9)  COMP-3.
01  PRODUCTO  PIC S9(18) COMP-3.
01  ED-P      PIC -(17)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    UNSTRING LINEA DELIMITED BY ALL SPACES INTO TXT-A TXT-B
    MOVE FUNCTION NUMVAL(TXT-A) TO A
    MOVE FUNCTION NUMVAL(TXT-B) TO B

    COMPUTE PRODUCTO = A * B

    MOVE PRODUCTO TO ED-P
    DISPLAY "producto=" FUNCTION TRIM(ED-P)
    STOP RUN.
```

**Lo que esta clase enseña en COBOL.** **Inferencia cero.** Cada dato lleva su `PIC` completo, y el
programa dedica más líneas a describir la forma de los datos que a calcular. Es la verbosidad contra
la que reaccionó todo lo que vino después.

Pero COBOL resolvió el problema real que hay detrás —**repetir la misma declaración en veinte
programas**— con un mecanismo que se adelantó a su tiempo: el **copybook**.

```cobol
*> En un miembro llamado CLIENTE:
01  REG-CLIENTE.
    05  CLI-CODIGO   PIC 9(8).
    05  CLI-NOMBRE   PIC X(40).
    05  CLI-SALDO    PIC S9(11)V99 COMP-3.

*> En cualquier programa que lo necesite:
COPY CLIENTE.
```

`COPY` inserta el texto en tiempo de compilación, y con `REPLACING` permite renombrar los campos al
insertarlos. Todos los programas que tocan el fichero de clientes comparten **una sola definición**,
y cambiar un campo es cambiar un fichero. Es el antepasado directo de los ficheros de cabecera, de
los esquemas compartidos y de los tipos generados a partir de un contrato — el mismo problema, con
una solución de 1968.

Y fíjate en `PIC S9(18)` para el producto: al no haber inferencia, **el programador tiene que
calcular a mano cuántos dígitos puede necesitar el resultado**. Si se queda corto, la clase 049 ya
avisó de lo que pasa.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program inferencia
   implicit none
   integer :: a, b

   read(*, *) a, b

   write(*, '(A,I0)') 'producto=', a * b
end program inferencia
```

**Lo que esta clase enseña en Fortran.** La historia más instructiva de toda la página: **Fortran
tuvo inferencia de tipos desde 1957, y su comunidad se pasó cuarenta años desactivándola**.

La regla era tipográfica: una variable no declarada cuyo nombre empieza por `I`, `J`, `K`, `L`, `M`
o `N` es un **entero**; cualquier otra inicial, un **real**. De ahí el chiste clásico —*God is real,
unless declared integer*— y de ahí también que los bucles de todo el código Fortran del mundo usen
`i`, `j`, `k`: no era estilo, era la única forma de que el contador fuera entero sin declararlo.

Y de ahí, sobre todo, el defecto característico:

```fortran
program mal
   velocidad = 100.0
   velocidda = velocidad * 2.0   ! erratas: crea una variable NUEVA
   print *, velocidad            ! imprime 100.0, y nadie sabe por qué
end program
```

Sin declaraciones, una errata **no es un error**: es una variable nueva. Se dice que un error de este
tipo contribuyó a la pérdida de la sonda Mariner 1 en 1962 —la anécdota exacta se cuenta de varias
maneras y conviene tomarla con cuidado— pero el mecanismo es real y costó incontables horas de
depuración.

`implicit none` apaga la regla y convierte cada errata en un error de compilación. Es la lección de
esta clase: **inferir el tipo a partir del nombre no es inferencia, es adivinación**. La inferencia de
verdad, la de C++ o Rust, deduce del **valor**, y por eso una errata sigue siendo un error.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Inferencia is
   A, B : Integer;
begin
   Get (A);
   Get (B);

   Put ("producto=");
   Put (A * B, Width => 1);
   New_Line;
end Inferencia;
```

**Lo que esta clase enseña en Ada.** Ada **no tiene inferencia general** y es deliberado: si el tipo
es la herramienta principal para expresar la intención, escribirlo no es ruido, es documentación
comprobada.

Pero sí tiene inferencia en tres sitios muy concretos, y elegirlos dice mucho:

```ada
--  1) Números con nombre: sin tipo, valor exacto (ya vistos en la clase 041)
Maximo : constant := 1_000_000;

--  2) La variable de un bucle for: su tipo se DEDUCE del rango
for I in 1 .. 10 loop ... end loop;              --  I es Integer, y es constante
for Dia in Lunes .. Viernes loop ... end loop;   --  Dia es del tipo enumerado

--  3) Agregados y literales, que toman el tipo del contexto
V : Vector := (others => 0.0);
```

Los tres tienen algo en común: **el tipo se deduce de algo que ya está escrito al lado**. No hay que
buscarlo lejos.

Y el caso del bucle merece subrayarse porque resuelve un error clásico: en Ada, la variable de un
`for` **es una constante local al bucle**. No se puede modificar dentro, no existe fuera, y no hace
falta declararla. En C se declara, se puede modificar dentro del cuerpo y sobrevive si la declaraste
fuera — tres oportunidades de error que Ada simplemente elimina.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Inferencia;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  A, B: Integer;

begin
  Read(A, B);

  WriteLn('producto=', IntToStr(A * B));
end.
```

**Lo que esta clase enseña en Pascal.** Pascal exige declararlo todo en la sección `var`, con la
misma lógica de una sola pasada que ya apareció en la clase 042. Pero tiene un caso de inferencia
desde el principio, y es el mismo que Ada: **las constantes sin tipo**.

```pascal
const
  MAXIMO = 1000;        { el compilador deduce el tipo en cada uso }
  PI     = 3.14159;
  SALUDO = 'hola';
```

Una constante sin tipo se adapta al contexto: `MAXIMO` puede usarse donde se espera un `Byte`, un
`Integer` o un `Int64`, y solo se comprueba el rango en el punto de uso. Es exactamente el concepto
del **número con nombre** de Ada, y también el de las constantes sin tipo de Go.

Y la rama moderna sí llegó: **Delphi 10.3, en 2019**, añadió la declaración de variables en línea con
inferencia, y Free Pascal tiene su equivalente:

```pascal
var Total := A * B;            { Delphi 10.3+: el tipo se deduce }
for var I := 1 to 10 do ...    { y también en el bucle }
```

Sesenta años después de ALGOL W, el lenguaje que definió "declara todo arriba" adoptó lo contrario.
Es una buena muestra de que estas decisiones no son permanentes: la restricción de la pasada única
dejó de importar cuando los compiladores dejaron de estar limitados por la memoria.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let* ((a (read))
       (b (read)))
  (format t "producto=~D~%" (* a b)))
```

**Lo que esta clase enseña en Common Lisp.** La sorpresa de esta clase: **SBCL infiere tipos, y
avisa en tiempo de compilación**, en un lenguaje que todo el mundo clasifica como dinámico.

```lisp
(defun mal (x)
  (declare (type integer x))
  (concatenate 'string x "hola"))

; SBCL al compilar:
;   caught WARNING: Derived type of X is (INTEGER), conflicting with its asserted type SEQUENCE.
```

SBCL propaga los tipos por el flujo de datos, deduce el tipo de cada expresión y **señala las
contradicciones que puede demostrar**, sin ejecutar nada. Es la misma técnica que usan los
compiladores estáticos, aplicada a un lenguaje sin declaraciones obligatorias.

Y el sistema de tipos que infiere es más expresivo que el de la mayoría de los estáticos, porque
incluye **rangos y uniones**:

```lisp
(declare (type (integer 0 100) porcentaje))     ; un entero ENTRE 0 y 100
(declare (type (or null string) nombre))        ; nulable, explícito
(declare (type (simple-array double-float (*)) datos))
```

`(integer 0 100)` es exactamente el subrango de Ada y Pascal, aquí como tipo de primera clase. Con
`(safety 0)` SBCL confía y genera código sin comprobaciones; con `(safety 3)` las comprueba todas en
ejecución. **El mismo código, con o sin red, según una declaración.** Eso es tipado gradual, y estaba
en el estándar de 1994.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea
lassign [split [string trim $linea]] a b

puts "producto=[expr {$a * $b}]"
```

**Lo que esta clase enseña en Tcl.** No hay nada que inferir: no hay declaraciones y no hay tipos.
`lassign` crea `a` y `b` en el acto, y `expr` decide qué son en el momento de multiplicar.

Lo interesante es que **el compilador de bytecode de Tcl sí infiere**, aunque el lenguaje no lo
exponga. Cuando `expr` recibe una expresión entre llaves —y por eso siempre se escribe entre
llaves—, Tcl la compila **una sola vez** a bytecode y, si detecta que los operandos han sido enteros
en las últimas vueltas, genera una ruta rápida que opera directamente sobre la representación
numérica en caché, sin volver a analizar el texto.

Si en alguna iteración el valor deja de ser un entero, la ruta rápida se abandona y se vuelve a la
genérica. Ese patrón —especular sobre el tipo, comprobarlo barato y desespecializar si falla— es
**exactamente** lo que hacen hoy V8, JavaScriptCore y PyPy con sus clases ocultas y su compilación
por trazas. Tcl lo hacía en 1997.

La lección: en los lenguajes dinámicos rápidos, la inferencia no desapareció, **se movió del
programador al motor y del compilado al tiempo de ejecución**.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;
my ($x, $y) = split ' ', $linea;

printf "producto=%d\n", $x * $y;
```

**Lo que esta clase enseña en Perl.** `my` declara la **existencia** y el **ámbito** de una variable,
pero no su tipo — porque no hay tipo que declarar. Lo único que el sigilo indica es la **forma del
acceso**: escalar, lista o hash.

Y aquí hay una distinción que esta clase deja clara y que se confunde a menudo: `use strict` **no
añade tipos**. Lo que hace es obligar a **declarar el nombre**, que es un problema distinto —el de
la errata de Fortran— y se resuelve por separado del tipado.

Perl moderno ha ido añadiendo declaración donde importa. Las **firmas de subrutina**, estables desde
5.36, declaran cuántos parámetros hay y con qué nombre, aunque no de qué tipo:

```perl
use v5.36;

sub producto ($a_val, $b_val) {    # firma: nombre y aridad declarados
    return $a_val * $b_val;
}
```

Antes de eso, los argumentos llegaban en el array `@_` y una llamada con el número equivocado de
argumentos **no daba error**. La firma convierte eso en un fallo en tiempo de compilación. Es la
misma dirección que ha tomado Python con las anotaciones y Ruby con RBS: **añadir declaración
opcional a un lenguaje dinámico, empezando por lo que más errores causa**.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>

int main() {
    int a{}, b{};
    if (!(std::cin >> a >> b)) return 1;

    const auto producto = a * b;      // auto: el tipo lo deduce el compilador

    std::cout << "producto=" << producto << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** `auto` es la inferencia de verdad: el tipo **existe**, es
`int`, es estricto, y lo deduce el compilador a partir del valor. No se pierde ninguna comprobación
— es exactamente lo mismo que escribir `int`, con menos teclas.

Y hay tres motivos por los que se usa que van más allá de la comodidad:

```cpp
auto it = mapa.begin();     // en vez de std::map<std::string, std::vector<int>>::iterator
auto lambda = [](int x) { return x * 2; };   // el tipo de una lambda NO SE PUEDE escribir
for (const auto& [clave, valor] : mapa) { }  // C++17: descomposición estructurada
```

El segundo es el decisivo: **el tipo de una lambda es único, generado por el compilador y sin
nombre**. Sin `auto` no habría forma de declarar la variable. Cuando un lenguaje introduce valores
cuyo tipo no se puede escribir, la inferencia deja de ser azúcar y pasa a ser necesaria.

C++ tiene además `decltype` —"el tipo de esta expresión, sin evaluarla"— y, desde C++17, la
**deducción de argumentos de plantilla en el constructor**: `std::pair p{1, "a"};` en lugar de
`std::pair<int, const char*>`.

Y el aviso habitual: `auto` **descarta las referencias y los `const`** salvo que los pidas.
`auto x = vec[0];` copia; `auto& x = vec[0];` no. Esa distinción de un carácter es la causa de
copias silenciosas en bucles sobre contenedores grandes.

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

dcl-pi INFEREN;
  a int(10) const;
  b int(10) const;
end-pi;

dcl-s producto like(a);       // LIKE: hereda el tipo de otra variable
dcl-s salida   char(40);

producto = a * b;

salida = 'producto=' + %char(producto);
dsply salida;

*inlr = *on;
return;
```

**Lo que esta clase enseña en RPG.** `like(a)` es la inferencia de RPG, y resuelve un problema muy
concreto del mundo empresarial: **que el tipo de una variable siga al del campo de la base de datos
sin repetirlo**.

```rpgle
dcl-s importe   like(FACTURA.TOTAL);   // el tipo del campo, sea cual sea
dcl-s copia     likeds(cabecera);      // la misma estructura de datos
dcl-s texto     like(nombre) inz('');
```

Si mañana el campo `TOTAL` pasa de `packed(11:2)` a `packed(13:2)`, **todos los programas que usan
`like` se ajustan al recompilar**. Sin él habría que buscar y cambiar cada declaración, con el riesgo
de olvidar una y truncar importes en silencio —el fallo de la clase 049—.

Es inferencia con un propósito distinto de la de C++: no ahorra teclas, **elimina una duplicación
que se desincroniza**. El mismo motivo por el que en TypeScript se escribe `typeof config` o en Rust
se derivan tipos de un esquema.

RPG añadió después **`likefile`** para prototipos de ficheros y las **plantillas** (`template`), que
permiten declarar un tipo que solo existe para ser copiado con `like` y que nunca ocupa memoria. Es
el equivalente de un `typedef` en un lenguaje que no tenía ninguno.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 inferencia: procedure options(main);

    declare (a, b)   fixed binary(31);
    declare producto fixed binary(31);

    get list (a, b);
    producto = a * b;

    put skip list ('producto=' || trim(char(producto)));

 end inferencia;
```

**Lo que esta clase enseña en PL/I.** PL/I tenía **declaración implícita**, como Fortran: una
variable sin declarar recibía atributos según su inicial —`I` a `N` binaria fija, el resto flotante
decimal—. Con los mismos problemas y por los mismos motivos.

Pero PL/I hizo algo que ningún otro lenguaje de esta página: dejó que **el programador redefiniera
las reglas de inferencia**, con la sentencia `DEFAULT`:

```pli
default range(*) fixed binary(31);        /* todo lo no declarado es entero */
default range(a:h) character(20) varying; /* salvo a..h, que son texto */
default (constant) value(fixed binary(31));
```

Es decir: la convención de nombres deja de ser una regla del lenguaje y pasa a ser **configuración
del programa**. Visto hoy suena a mala idea —dos ficheros del mismo sistema podrían tener reglas
distintas— y probablemente lo era. Pero es un ejemplo notable de la filosofía de PL/I: si hay una
regla, que sea parametrizable.

La práctica moderna en PL/I es la contraria, y se parece a `implicit none`:

```pli
default range(*) ;    /* sin atributos: obliga a declararlo TODO */
```

Otra vez el mismo arco que en Fortran — el lenguaje ofrece la adivinación y la comunidad acaba
apagándola.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
INFER ; Inferencia -- clase 052
 read linea
 set a = $piece(linea, " ", 1)
 set b = $piece(linea, " ", 2)
 write "producto=", a * b, !
 quit
```

**Lo que esta clase enseña en M.** No hay tipos, no hay declaraciones y no hay inferencia: **hay
`set`**. Una variable existe desde que se le asigna y su contenido es siempre una cadena.

Lo que sí tiene M, y conviene no confundir con una declaración, es **`new`**:

```mumps
rutina ;
 new a, b, temporal      ; NO declara: guarda el valor anterior y lo restaura al salir
 set a = 1
 quit                    ; aquí a, b y temporal recuperan lo que valieran antes
```

`new` no crea variables locales en el sentido léxico de casi todos los lenguajes: **intercepta las
globales durante la llamada**. Es ámbito **dinámico**, el mismo mecanismo que `local` en Perl y que
las variables especiales de Common Lisp. Si una rutina llamada desde aquí lee `a`, ve la de este
ámbito, no la del llamante — cosa que con ámbito léxico sería imposible.

Ese modelo es más frágil y más flexible a la vez, y explica un idioma muy visto en código M
heredado: rutinas que se comunican por variables acordadas en vez de por parámetros. Funciona, es
rapidísimo, y hace que entender un programa exija leer toda la cadena de llamadas.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| partes a b |

partes := stdin nextLine substrings collect: [ :cada | cada asNumber ].
a := partes first.
b := partes second.

Transcript show: 'producto=', (a * b) printString; cr.
```

**Lo que esta clase enseña en Smalltalk.** Las temporales se declaran entre barras y **nunca llevan
tipo**, porque el tipo pertenece al objeto. `a` puede referirse hoy a un entero y mañana a una
ventana; lo único que decide qué se le puede hacer es **a qué mensajes responde**.

Y aquí está la aportación de Smalltalk a esta clase, que no es sobre el lenguaje sino sobre las
**herramientas**: como no hay tipos escritos, el entorno los **descubre en ejecución**. El navegador
de Pharo puede responder a preguntas que un compilador estático respondería en compilación:

- *¿quién envía este mensaje?* — buscando en todos los métodos de la imagen;
- *¿qué clases lo implementan?* — el conjunto real de receptores posibles;
- *¿qué valores ha tomado esta variable?* — instrumentando y observando.

Es **inferencia por observación** en lugar de por deducción. Y llevada al extremo produce algo que
ningún lenguaje estático puede: el depurador de Smalltalk, ante un método que no existe, te ofrece
crearlo **en el momento**, con los argumentos reales delante y la pila viva, y continuar.

La contrapartida es honesta y hay que decirla: sin tipos declarados, **el compilador no puede
demostrar nada antes de ejecutar**. Un error de tipo aparece cuando se recorre esa rama, no antes.
Por eso los proyectos Smalltalk grandes se apoyan tanto en pruebas — no es casualidad que SUnit,
el antepasado de JUnit, naciera aquí.

---

## Y de vuelta a la clase

La lección es que **inferencia no significa "sin tipos"**. En C++ y en Rust el tipo existe, es
estricto y lo deduce el compilador; en Fortran del 57 el tipo se adivinaba por una regla tipográfica,
que es otra cosa muy distinta; y en Tcl o M no hay nada que inferir. Cuando alguien dice "mi lenguaje
tiene inferencia", la pregunta útil es **qué pasa cuando la deducción sale mal** — si es un error de
compilación o un valor basura.

⏮️ [Volver a la clase 052](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
