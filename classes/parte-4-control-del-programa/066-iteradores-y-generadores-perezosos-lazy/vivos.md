# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 066

> [⬅️ Volver a la clase 066](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Producir los *n* primeros números pares. El programa es trivial; lo interesante es **quién decide
cuándo se calcula cada valor**. Un generador perezoso no construye la lista entera: fabrica un valor,
lo entrega, **se queda parado a mitad de su bucle** y espera a que le pidan el siguiente. Es control
de flujo suspendido y reanudado, y muy pocos lenguajes de esta página lo tienen.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es la **evaluación perezosa y la suspensión de la ejecución**, y estos lenguajes
> aportan tres cosas que el núcleo no muestra. La primera: **Tcl tiene corrutinas de verdad** desde
> 2012 —`yield` y reanudación—, y este programa las usa. La segunda: **la clausura como generador**, que
> es lo que hace Perl y lo que hacía Lisp antes de que existiera `yield` en ningún sitio.
>
> Y la tercera, la más interesante: en **M** el recorrido perezoso no es una construcción del lenguaje,
> es **`$order` sobre un árbol de disco**, y en **RPG** es el ciclo del programa empujándote los
> registros. Dos modelos de pereza —tirar y empujar— que preceden en décadas a los generadores.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: un entero `n` (n >= 1) → stdout: `pares=<2-4-...-2n>`
- **Regla:** `pares_i = 2·i para i de 1 a n`

| stdin | esperado |
|---|---|
| `3` | `pares=2-4-6` |
| `1` | `pares=2` |
| `5` | `pares=2-4-6-8-10` |

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
PROGRAM-ID. PARES.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  N       PIC 9(4)  COMP-3.
01  I       PIC 9(4)  COMP-3.
01  V       PIC 9(9)  COMP-3.
01  ED-V    PIC Z(8)9.
01  TROZO   PIC X(20).
01  TLEN    PIC 9(4)  COMP-3.
01  SEC     PIC X(400).
01  PTR     PIC 9(4)  COMP-3.

PROCEDURE DIVISION.
    ACCEPT LINEA
    MOVE FUNCTION NUMVAL(LINEA) TO N
    MOVE SPACES TO SEC
    MOVE 1 TO PTR

    PERFORM VARYING I FROM 1 BY 1 UNTIL I > N
        COMPUTE V = 2 * I
        MOVE V TO ED-V
        MOVE FUNCTION TRIM(ED-V) TO TROZO
        COMPUTE TLEN = FUNCTION LENGTH(FUNCTION TRIM(TROZO))
        IF PTR > 1
            MOVE "-" TO SEC(PTR:1)
            ADD 1 TO PTR
        END-IF
        MOVE TROZO(1:TLEN) TO SEC(PTR:TLEN)
        ADD TLEN TO PTR
    END-PERFORM

    DISPLAY "pares=" FUNCTION TRIM(SEC)
    STOP RUN.
```

**Lo que esta clase enseña en COBOL.** **COBOL no tiene generadores, ni corrutinas, ni evaluación
perezosa.** Un `PERFORM` se ejecuta entero; no hay forma de suspenderlo a mitad y reanudarlo después.

Y sin embargo, el modelo *pull* que esta clase describe es **exactamente cómo COBOL lee ficheros**:

```cobol
PERFORM UNTIL FIN-FICHERO
    READ CLIENTES
        AT END SET FIN-FICHERO TO TRUE
        NOT AT END PERFORM PROCESAR-CLIENTE
    END-READ
END-PERFORM
```

`READ` entrega **un registro cada vez**, sin cargar el fichero en memoria, y el bucle pide el
siguiente cuando ha terminado con el anterior. Es un iterador perezoso sobre diez millones de
registros — con la diferencia de que el productor no es código de usuario suspendido, sino el
subsistema de acceso a ficheros del sistema operativo.

Esa es la observación de fondo de esta clase: **la pereza no llegó con los generadores; llegó con la
E/S**. Todo el proceso por lotes desde los años 60 está construido sobre "lee un registro, procésalo,
olvídalo", porque **la cinta no cabía en memoria**. Los generadores de los lenguajes modernos
generalizan a cualquier cálculo lo que la E/S secuencial hacía desde el principio.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program pares
   implicit none
   integer :: n, i
   character(len=:), allocatable :: sec
   character(len=16) :: buf

   read(*, *) n

   sec = ''
   do i = 1, n
      write(buf, '(I0)') 2 * i
      if (i > 1) sec = sec // '-'
      sec = sec // trim(buf)
   end do

   write(*, '(A,A)') 'pares=', sec
end program pares
```

**Lo que esta clase enseña en Fortran.** Fortran **no tiene generadores ni corrutinas**, y es
coherente con su propósito: en cálculo numérico se opera sobre **arrays completos que ya están en
memoria**, no sobre secuencias potencialmente infinitas.

Su forma de generar una secuencia es construir el array de una vez, y para eso tiene una construcción
que sí conviene conocer, el **constructor de array con bucle implícito**:

```fortran
integer :: pares(n)
pares = [(2 * i, i = 1, n)]                 ! el array ENTERO, en una expresión
impares = [(i, i = 1, 100, 2)]
matriz = reshape([(i, i = 1, 12)], [3, 4])  ! y se le da forma
```

`[(expresión, variable = inicio, fin, paso)]` es una **comprensión de lista** —tema de la clase 067—
con sintaxis de 1990. Se evalúa entera, no perezosamente.

Y donde Fortran sí tiene algo parecido a la pereza es en un sitio inesperado: **la evaluación de
expresiones de array**. Cuando escribes `c = a + b * 2`, un compilador optimizador **no** construye el
array intermedio `b * 2`: fusiona las dos operaciones en un solo recorrido. Es *fusión de bucles*, y
tiene el mismo efecto que la pereza —evitar materializar resultados intermedios— pero obtenido por el
compilador en lugar de por el programador.

Es lo mismo que buscan los *ranges* de C++20 y los iteradores encadenados de Rust: **componer sin
materializar**.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;           use Ada.Text_IO;
with Ada.Integer_Text_IO;   use Ada.Integer_Text_IO;
with Ada.Strings;           use Ada.Strings;
with Ada.Strings.Fixed;
with Ada.Strings.Unbounded; use Ada.Strings.Unbounded;

procedure Pares is
   N   : Integer;
   Sec : Unbounded_String := Null_Unbounded_String;
begin
   Get (N);

   for I in 1 .. N loop
      if I > 1 then
         Append (Sec, "-");
      end if;
      Append (Sec, Ada.Strings.Fixed.Trim (Integer'Image (2 * I), Both));
   end loop;

   Put_Line ("pares=" & To_String (Sec));
end Pares;
```

**Lo que esta clase enseña en Ada.** Ada no tiene `yield`, pero tiene algo que ningún otro lenguaje de
esta página ofrece y que resuelve el mismo problema desde otro ángulo: **las tareas y las citas**.

```ada
task Generador is
   entry Siguiente (V : out Integer);
end Generador;

task body Generador is
begin
   for I in 1 .. 1000 loop
      accept Siguiente (V : out Integer) do    --  se BLOQUEA hasta que alguien pida
         V := 2 * I;
      end Siguiente;
   end loop;
end Generador;

--  Y en el consumidor:
Generador.Siguiente (Valor);
```

La tarea se queda **detenida en el `accept`** hasta que alguien llama a `Siguiente`, entrega el valor
y continúa su bucle hasta el siguiente `accept`. **Es exactamente la semántica de un generador**:
producción suspendida y reanudada bajo demanda.

La diferencia con `yield` es que aquí hay un **hilo de verdad** y una sincronización real, con su
coste. Un generador de Python o una corrutina de Tcl se suspenden dentro del mismo hilo. Ada eligió
resolverlo con concurrencia porque la concurrencia estaba en el lenguaje desde 1983, y en un sistema
de tiempo real la cita tiene garantías temporales analizables que un generador no da.

Ada 2012 añadió además las **interfaces de iterador**, que permiten `for X of Coleccion loop` sobre
tipos propios, y con ellas se puede construir un iterador perezoso sin tareas.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Pares;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  N, I: Integer;
  Sec: string;

begin
  Read(N);

  Sec := '';
  for I := 1 to N do
  begin
    if I > 1 then Sec := Sec + '-';
    Sec := Sec + IntToStr(2 * I);
  end;

  WriteLn('pares=', Sec);
end.
```

**Lo que esta clase enseña en Pascal.** Pascal **no tiene generadores**, y su respuesta a esta clase
es el patrón **enumerador**: un objeto con estado que sabe avanzar y entregar el actual.

```pascal
type
  TParesEnumerador = class
  private
    FActual, FLimite: Integer;
  public
    constructor Create(Limite: Integer);
    function MoveNext: Boolean;
    property Current: Integer read FActual;
  end;

function TParesEnumerador.MoveNext: Boolean;
begin
  Inc(FActual, 2);
  Result := FActual <= FLimite * 2;
end;
```

Con `MoveNext` y `Current`, y una función `GetEnumerator` en la clase contenedora, **`for..in`
funciona sobre tu tipo**. Es el mismo contrato de C#, de Java y de Ada 2012.

La diferencia con un generador de verdad está en quién guarda el estado: aquí, **campos de un objeto
que tú declaras**; con `yield`, la **posición dentro del bucle**, que el compilador guarda por ti.
Cuando la lógica de producción es un bucle anidado con condiciones, escribir el enumerador a mano es
considerablemente más difícil que poner `yield` en medio.

Free Pascal tiene además **hilos ligeros y corrutinas** en bibliotecas de la comunidad, pero no en el
lenguaje. Delphi introdujo `TEnumerator<T>` genérico, que es el mismo patrón con tipos.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let ((n (read)))
  (format t "pares=~{~D~^-~}~%" (loop for i from 1 to n collect (* 2 i))))
```

**Lo que esta clase enseña en Common Lisp.** El estándar **no tiene generadores**, y la comunidad
resolvió la pereza de tres maneras distintas, todas **sin cambiar el lenguaje**:

**1) La clausura con estado**, que es el generador manual y funciona en cualquier Lisp:

```lisp
(defun generador-pares (n)
  (let ((i 0))
    (lambda ()
      (when (< i n)
        (incf i)
        (* 2 i)))))

(let ((sig (generador-pares 5)))
  (loop for v = (funcall sig) while v collect v))   ; (2 4 6 8 10)
```

**2) Las listas perezosas** al estilo de Scheme, con `delay` y `force` implementados como macros. La
biblioteca `SERIES` llega a compilar expresiones sobre secuencias perezosas **a bucles sin estructuras
intermedias**, que es la fusión de bucles de Fortran obtenida en tiempo de macroexpansión.

**3) Las corrutinas**, disponibles en bibliotecas como `cl-cont` mediante **transformación a estilo de
paso de continuaciones** — otra vez, macros reescribiendo el código.

Que las tres sean bibliotecas y no características del lenguaje es la tesis de la clase 041 llevada
hasta el final: **cuando el lenguaje permite extender su propia sintaxis, la frontera entre "lo que
trae el lenguaje" y "lo que trae una biblioteca" deja de ser interesante**.

Y `~{~D~^-~}` resuelve el separador: itera sobre la lista y `~^` corta antes del último guion.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea
set n [string trim $linea]

coroutine pares apply {{n} {
    yield
    for {set i 1} {$i <= $n} {incr i} {
        yield [expr {2 * $i}]
    }
    return ""
}} $n

set salida {}
for {set k 1} {$k <= $n} {incr k} {
    lappend salida [pares]
}

puts "pares=[join $salida -]"
```

**Lo que esta clase enseña en Tcl.** **Esta es la única implementación de esta página con un generador
de verdad, y funciona: se ejecuta en CI.**

`coroutine pares apply {...} $n` crea una corrutina: el cuerpo empieza a ejecutarse **hasta el primer
`yield`**, que lo suspende y devuelve el control. A partir de ahí, cada vez que se invoca `pares`
—como si fuera un comando— la corrutina **se reanuda exactamente donde estaba**, dentro del `for`,
produce el siguiente valor con `yield` y vuelve a suspenderse.

Es la misma semántica que `yield` en Python, `yield return` en C# o las corrutinas de Kotlin. Tcl las
tiene desde la **versión 8.6, de 2012**.

Y lo notable es cómo están implementadas: **una corrutina de Tcl es una pila de ejecución
independiente** gestionada por el intérprete, no un hilo del sistema operativo. Crear una cuesta
microsegundos y hay quien mantiene decenas de miles vivas a la vez.

De ahí sale el uso real: combinadas con `fileevent` y la E/S no bloqueante de la clase 056, permiten
escribir código **asíncrono con forma secuencial** —sin el infierno de retrollamadas— quince años
antes de que `async`/`await` llegara a JavaScript, C# o Python:

```tcl
coroutine cliente apply {{sock} {
    set linea [yieldto gets $sock]   ;# parece bloqueante, no lo es
    ...
}} $canal
```

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $n = <STDIN>;
chomp $n;

#  Un generador: una clausura que guarda su estado entre llamadas.
my $i = 0;
my $siguiente = sub { return ++$i <= $n ? 2 * $i : undef };

my @salida;
while (defined(my $v = $siguiente->())) {
    push @salida, $v;
}

print "pares=", join('-', @salida), "\n";
```

**Lo que esta clase enseña en Perl.** Perl no tiene `yield`, y su respuesta es la **clausura con
estado**: una función anónima que **captura** las variables de su entorno y las conserva entre
llamadas.

`$i` está declarada fuera de `sub { }`, pero la subrutina la **captura por referencia**, así que
sobrevive mientras la clausura exista y mantiene su valor de una invocación a otra. Es un generador
con todas las letras: estado privado, producción bajo demanda, sin construir la lista completa.

La forma canónica encapsula el estado dentro:

```perl
sub generador_pares {
    my ($n) = @_;
    my $i = 0;
    return sub { return ++$i <= $n ? 2 * $i : undef };   # $i queda ATRAPADA aquí
}

my $sig = generador_pares(5);
while (defined(my $v = $sig->())) { ... }
```

Cada llamada a `generador_pares` crea **un `$i` nuevo**, así que dos generadores no se pisan. Ese es
el mecanismo con el que se construyen iteradores, contadores, cachés y objetos sin clases en
cualquier lenguaje con clausuras — JavaScript vive de esto.

Y Perl tiene pereza integrada en un sitio muy usado: **el operador de rango en un `foreach` no
materializa la lista**. `for (1 .. 1_000_000_000)` no reserva mil millones de elementos; itera. Es la
misma optimización que `range` de Python 3.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>
#include <string>

//  Un generador escrito a mano: un objeto que guarda su estado.
struct Pares {
    int i = 0;
    int n;
    explicit Pares(int limite) : n(limite) {}

    bool siguiente(int& v) {
        if (i >= n) return false;
        ++i;
        v = 2 * i;
        return true;
    }
};

int main() {
    int n{};
    if (!(std::cin >> n)) return 1;

    Pares gen(n);
    std::string salida;
    int v{};
    while (gen.siguiente(v)) {
        if (!salida.empty()) salida += '-';
        salida += std::to_string(v);
    }

    std::cout << "pares=" << salida << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** Hasta C++20, la única forma era la de este programa: **un objeto
que guarda su estado a mano**, con un método para avanzar. Es el patrón enumerador de Pascal y de C#,
escrito explícitamente.

C++20 añadió las **corrutinas** de verdad, con `co_yield`, y el resultado es mucho más directo:

```cpp
std::generator<int> pares(int n) {          // std::generator es de C++23
    for (int i = 1; i <= n; ++i) {
        co_yield 2 * i;                     // suspende aquí y devuelve el valor
    }
}

for (int v : pares(5)) { ... }
```

Y los **rangos** de C++20 dan pereza componible sin escribir ninguna corrutina:

```cpp
#include <ranges>
auto pares = std::views::iota(1, n + 1)
           | std::views::transform([](int i) { return 2 * i; });
```

Ese `|` encadena **vistas perezosas**: nada se calcula hasta que alguien recorre el resultado, y **no
se construye ningún vector intermedio**. Es la fusión de bucles de la que hablaba la ficha de Fortran,
obtenida en la biblioteca mediante plantillas.

Compilar este programa con `-std=c++17` obliga a la versión manual, y esa es justamente la lección:
**la diferencia entre las dos formas es enteramente de expresividad**. Las dos hacen lo mismo y una se
lee.

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

dcl-pi PARES;
  n int(10) const;
end-pi;

dcl-s i      int(10);
dcl-s sec    varchar(500) inz('');
dcl-s salida char(520);

for i = 1 to n;
  if i > 1;
    sec += '-';
  endif;
  sec += %char(2 * i);
endfor;

salida = 'pares=' + sec;
dsply salida;

*inlr = *on;
return;
```

**Lo que esta clase enseña en RPG.** RPG no tiene generadores ni corrutinas. Pero es el lenguaje de
esta página que mejor ilustra **el otro modelo de pereza**, el de *empujar*.

Con un fichero declarado como **entrada primaria**, el **ciclo del programa** hace el bucle: lee un
registro, ejecuta tu lógica, comprueba los cambios de nivel de control, imprime totales y vuelve a
empezar. **Tú no pides el siguiente registro: el runtime te lo entrega.**

```text
     FVENTAS    IP   E             DISK
     FINFORME   O    E             PRINTER
```

Eso es **inversión de control**, y la diferencia con un iterador es dónde vive el bucle:

| | Quién tiene el bucle | Ejemplos |
|---|---|---|
| **Tirar** (*pull*) | El **consumidor** | Iteradores, generadores, `$order` de M, `READ` de COBOL |
| **Empujar** (*push*) | El **productor** | Ciclo de RPG, eventos, `Observer`, flujos reactivos |

El modelo *push* es el de todos los marcos de trabajo modernos —tú escribes el manejador y el
framework llama— y el de la programación reactiva. Que RPG lo tuviera en 1959, con el nombre de
"ciclo del programa", es de las cosas más sorprendentes de toda esta sección.

Su inconveniente es el mismo que hoy: **si el bucle no es tuyo, salirte de él es difícil**. De ahí los
indicadores `*INLR` y `*INRT`, que existen precisamente para decirle al ciclo qué hacer, y de ahí que
el RPG moderno con `main()` prescinda de él.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 pares: procedure options(main);

    declare n   fixed binary(31);
    declare i   fixed binary(31);
    declare sec character(500) varying initial('');

    get list (n);

    do i = 1 to n;
       if i > 1 then sec = sec || '-';
       sec = sec || trim(char(2 * i));
    end;

    put skip list ('pares=' || sec);

 end pares;
```

**Lo que esta clase enseña en PL/I.** PL/I no tiene generadores, pero tiene **multitarea desde 1964**,
y con ella se puede construir el mismo esquema productor-consumidor que Ada resuelve con tareas y
citas:

```pli
declare productor entry;

call productor task(t1) event(listo);   /* arranca una TAREA */
wait(listo);                            /* espera al suceso */
```

`task`, `event` y `wait` son parte del lenguaje. Es concurrencia con sincronización por sucesos,
veinte años antes que Ada y treinta antes que Java.

Y hay una construcción de PL/I que se acerca todavía más a la suspensión y reanudación de un
generador: **las condiciones `ON` con reanudación**, que ya aparecieron en la clase 049.

```pli
on conversion begin;
   onsource() = '0';   /* CORRIGE el dato... */
end;                    /* ...y la operación CONTINÚA donde estaba */
```

El manejador se ejecuta **encima de la pila del punto que falló**, arregla la situación y devuelve el
control ahí mismo. Eso es exactamente lo que hace un `yield` visto al revés: el control salta a otro
sitio y **vuelve al punto exacto**.

Es la misma capacidad que el sistema de condiciones y reinicios de Common Lisp, y la razón de que
ambos aparezcan citados cuando se habla de que el `try/catch` moderno perdió algo por el camino: al
desenrollar la pila antes de manejar el error, se pierde la posibilidad de reanudar.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
PARES ; Pares -- clase 066
 read n
 set sec = ""
 for i = 1:1:n do
 . set:sec'="" sec = sec _ "-"
 . set sec = sec _ (2 * i)
 write "pares=", sec, !
 quit
```

**Lo que esta clase enseña en M.** M no tiene generadores como construcción, pero **`$order` es un
iterador perezoso de verdad** y merece verse en esta clase, porque su comportamiento es idéntico al de
un generador:

```mumps
 set clave = ""
 for  set clave = $order(^PACIENTE(clave))  quit:clave = ""  do
 . ; procesar UN paciente
```

Cada llamada a `$order` **devuelve la siguiente clave existente** y nada más. No hay lista, no hay
cursor que abrir, no hay conjunto de resultados en memoria. Sobre un *global* de diez millones de
nodos, el consumo de memoria es constante y el coste de cada paso es una búsqueda en el índice.

Y tiene una propiedad que los generadores de los lenguajes modernos **no** tienen: **es reanudable
entre procesos y entre ejecuciones**. La "posición" del iterador es simplemente el valor de `clave`,
un dato normal. Se puede guardar en disco, apagar el programa, y continuar el recorrido tres días
después desde otro proceso:

```mumps
 set ^ESTADO("ultimo") = clave      ; guardar por dónde iba
 ; ... y en otra ejecución:
 set clave = $get(^ESTADO("ultimo"))
```

Eso es imposible con un generador de Python o una corrutina de Tcl, cuyo estado es una pila viva en
memoria. Aquí el estado del recorrido es **un valor**, no una continuación — y por eso los procesos
por lotes de un sistema clínico pueden reanudarse tras una caída sin perder el sitio.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| n sec |

n := stdin nextLine trimBoth asNumber.

sec := String streamContents: [ :flujo |
    (1 to: n)
        do:          [ :i | flujo print: 2 * i ]
        separatedBy: [ flujo nextPut: $- ] ].

Transcript show: 'pares=', sec; cr.
```

**Lo que esta clase enseña en Smalltalk.** Pharo **sí tiene generadores**, y su implementación es una
de las cosas más elegantes de esta página. La clase `Generator` permite escribir:

```smalltalk
| gen |
gen := Generator on: [ :productor |
    1 to: n do: [ :i | productor yield: 2 * i ] ].

gen next.        "2"
gen next.        "4"
gen upToEnd.     "el resto"
```

`yield:` suspende el bloque y devuelve el valor; `next` lo reanuda donde estaba. Es la misma
semántica que la corrutina de Tcl o el `yield` de Python.

Y lo notable es **cómo está implementado**: usando **continuaciones**, que en Smalltalk se obtienen
manipulando el objeto `thisContext` —la pila de ejecución, que **es un objeto normal e
inspeccionable**—. `Generator` no es una característica del compilador ni una palabra clave: es una
clase de biblioteca de unas cien líneas que reifica la pila.

Ese es el techo de lo que permite un lenguaje donde todo es un objeto, **incluida la propia
ejecución**. Con `thisContext` se pueden construir generadores, corrutinas, continuaciones,
depuradores que reanudan y —el caso famoso— el framework web **Seaside**, que usa continuaciones para
que un flujo de varias páginas se escriba como una función secuencial, sin máquina de estados.

Y `String streamContents:` de este programa es el `WriteStream` de la clase 054: un flujo de
escritura, la contrapartida del de lectura.

---

## Y de vuelta a la clase

La distinción que deja esta clase es entre **tirar** (*pull*) y **empujar** (*push*). Un iterador o un
generador es *pull*: tú pides el siguiente y el productor se despierta. El ciclo de RPG, un manejador
de eventos o un `Observer` son *push*: el productor manda y tú reaccionas. Las dos formas recorren lo
mismo y ponen el bucle en sitios opuestos, y reconocer cuál tienes delante explica por qué unas APIs
se componen con facilidad y otras te obligan a llevar el estado a mano.

⏮️ [Volver a la clase 066](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
