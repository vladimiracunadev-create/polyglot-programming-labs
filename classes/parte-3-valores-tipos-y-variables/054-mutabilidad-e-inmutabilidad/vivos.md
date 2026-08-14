# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 054

> [⬅️ Volver a la clase 054](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Construir `1-2-3-4-5` juntando trozos. Es el ejercicio que convierte la mutabilidad en algo
observable: **¿cada `+=` crea una cadena nueva y tira la anterior, o modifica la que ya había?** La
respuesta no cambia el resultado, cambia el rendimiento — y en un bucle de cien mil vueltas la
diferencia entre las dos es la diferencia entre un segundo y un minuto.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es **quién puede cambiar un valor y qué cuesta**, y estos lenguajes lo enseñan
> porque cubren el arco entero. En COBOL una cadena es un **campo de posiciones fijas** que se modifica
> en el sitio: no hay asignación que copie, hay escritura sobre bytes concretos. En Fortran hasta 2003
> **no se podía** hacer crecer una cadena, así que este programa era imposible de escribir tal cual.
> Y en Smalltalk y Lisp la respuesta es un **flujo de escritura**, que es la misma solución que hoy
> llamamos `StringBuilder`.
>
> Además aparece un concepto que casi ningún lenguaje moderno tiene explícito: la **copia al escribir**
> de Pascal y Delphi, donde asignar una cadena no copia nada hasta que alguien la modifica.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: un entero `n` (n >= 1) → stdout: `sec=1-2-...-n` (números de 1 a n separados por guiones)
- **Regla:** `sec = unir([1..n], separador='-')`

| stdin | esperado |
|---|---|
| `3` | `sec=1-2-3` |
| `1` | `sec=1` |
| `5` | `sec=1-2-3-4-5` |

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
PROGRAM-ID. SECUENCIA.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  N       PIC 9(4) COMP-3.
01  I       PIC 9(4) COMP-3.
01  ED-I    PIC Z(3)9.
01  TROZO   PIC X(10).
01  LON-T   PIC 9(4) COMP-3.
01  SEC     PIC X(200).
01  LARGO   PIC 9(4) COMP-3.

PROCEDURE DIVISION.
    ACCEPT LINEA
    MOVE FUNCTION NUMVAL(LINEA) TO N
    MOVE SPACES TO SEC
    MOVE 1 TO LARGO

    PERFORM VARYING I FROM 1 BY 1 UNTIL I > N
        MOVE I TO ED-I
        MOVE FUNCTION TRIM(ED-I) TO TROZO
        COMPUTE LON-T = FUNCTION LENGTH(FUNCTION TRIM(TROZO))
        IF I > 1
            MOVE "-" TO SEC(LARGO:1)
            ADD 1 TO LARGO
        END-IF
        MOVE TROZO(1:LON-T) TO SEC(LARGO:LON-T)
        ADD LON-T TO LARGO
    END-PERFORM

    DISPLAY "sec=" FUNCTION TRIM(SEC)
    STOP RUN.
```

**Lo que esta clase enseña en COBOL.** En COBOL **todo es mutable y nada se copia de más**. `SEC` es
un bloque de 200 bytes que existe desde que arranca el programa, y `MOVE ... TO SEC(LARGO:LON-T)`
escribe **directamente sobre las posiciones indicadas**. No hay asignación que construya una cadena
nueva, no hay memoria que reservar, no hay recolector que despertar.

Por eso este bucle es lineal por construcción: cada vuelta escribe sus dos o tres bytes y avanza el
puntero `LARGO`. El problema del acumulador cuadrático —el que sufren Java, Python y C# al concatenar
en un bucle— **no puede ocurrir aquí**, porque no hay una operación de concatenación que copie.

El precio está en la otra columna: `SEC` mide 200 bytes tanto si guarda `"1"` como si guarda la
secuencia completa, hay que **calcular a mano si cabe**, y escribir más allá del final es
comportamiento indefinido —COBOL no comprueba los límites de la modificación de referencia salvo que
se compile con `-fec=bound-ref-mod` en GnuCOBOL o con `SSRANGE` en el compilador de IBM—.

Es exactamente el mismo intercambio que hace C: control total y coste predecible, a cambio de que la
seguridad la ponga el programador. Y la lección de esta clase es que **la inmutabilidad no es
gratuita ni obviamente superior**: es una decisión que cambia dónde se paga.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program secuencia
   implicit none
   integer :: n, i
   character(len=:), allocatable :: sec
   character(len=16) :: buf

   read(*, *) n

   sec = ''
   do i = 1, n
      write(buf, '(I0)') i
      if (i > 1) sec = sec // '-'
      sec = sec // trim(buf)
   end do

   write(*, '(A,A)') 'sec=', sec
end program secuencia
```

**Lo que esta clase enseña en Fortran.** **Este programa no se podía escribir en Fortran antes de
2003.** Una cadena tenía longitud fija decidida al declararla, y no había forma de hacerla crecer: la
única salida era declarar un búfer enorme y llevar un contador a mano, exactamente como hace COBOL.

Lo que lo hace posible es `character(len=:), allocatable`, la **longitud diferida**: al asignar,
Fortran **reasigna** la variable con el tamaño exacto del valor nuevo. `sec = sec // '-'` libera la
anterior, reserva una mayor y copia.

Y eso es justo lo que hay que ver en esta clase: **es cómodo y es cuadrático**. Cada vuelta copia
todo lo acumulado. Con `n` de cinco no importa; con un millón, sí. La versión rápida vuelve a
parecerse a COBOL:

```fortran
character(len=8*n) :: buffer      ! reserva de una vez
integer :: pos
pos = 1
do i = 1, n
   write(buffer(pos:), '(I0)') i
   pos = pos + len_trim(...)
end do
```

Fortran ofrece las dos y no oculta la diferencia, que es lo mejor que puede hacer un lenguaje
orientado al rendimiento. La comodidad de 2003 no borró la herramienta de 1977: la puso al lado.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;           use Ada.Text_IO;
with Ada.Integer_Text_IO;   use Ada.Integer_Text_IO;
with Ada.Strings;           use Ada.Strings;
with Ada.Strings.Fixed;
with Ada.Strings.Unbounded; use Ada.Strings.Unbounded;

procedure Secuencia is
   N   : Integer;
   Sec : Unbounded_String := Null_Unbounded_String;
begin
   Get (N);

   for I in 1 .. N loop
      if I > 1 then
         Append (Sec, "-");
      end if;
      Append (Sec, Ada.Strings.Fixed.Trim (Integer'Image (I), Both));
   end loop;

   Put_Line ("sec=" & To_String (Sec));
end Secuencia;
```

**Lo que esta clase enseña en Ada.** Ada obliga a **elegir el modelo de cadena en la declaración**, y
esa elección es una decisión de ingeniería con consecuencias que el lenguaje deja a la vista:

| Tipo | Longitud | Memoria dinámica | Dónde se usa |
|---|---|---|---|
| `String` | Fija al crear | No | Lo normal; porciones y arrays |
| `Bounded_String` | Variable, con **máximo declarado** | **No** | Sistemas críticos |
| `Unbounded_String` | Libre | Sí | Aplicaciones normales |

`Unbounded_String` es lo que este programa usa, y `Append` **modifica en el sitio** en lugar de
construir una cadena nueva, así que el bucle es amortizadamente lineal — no cuadrático como la
versión de Fortran.

Lo interesante es la fila del medio. En aviónica y ferrocarril se usa `Bounded_String` precisamente
**porque no toca el montículo**: el tamaño máximo se conoce al compilar, así que no hay fragmentación,
no hay fallos de asignación imprevisibles y el consumo de memoria del programa entero es analizable
antes de ejecutarlo. Si el texto no cabe, se levanta una excepción o se trunca según la política que
elijas — pero **nunca se pide memoria en vuelo**.

Es la mejor ilustración de esta clase: la mutabilidad y la asignación dinámica no son un detalle de
estilo, son una propiedad certificable del sistema.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Secuencia;
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
    Sec := Sec + IntToStr(I);
  end;

  WriteLn('sec=', Sec);
end.
```

**Lo que esta clase enseña en Pascal.** Con `{$H+}`, `string` es un `AnsiString`: longitud variable,
**conteo de referencias** y **copia al escribir** (*copy-on-write*). Y eso hace de Pascal el mejor
ejemplo de esta clase, porque su modelo no es "mutable" ni "inmutable": es **las dos cosas según el
momento**.

```pascal
A := 'hola';
B := A;          { NO copia el texto: copia un puntero y suma 1 al contador }
B := B + '!';    { AHORA sí copia, porque el contador era 2 y hay que separar }
```

Asignar es O(1). Modificar cuando alguien más comparte el dato provoca la copia; modificar cuando
eres el único dueño se hace **en el sitio**. El programador no ve nada de esto: obtiene la semántica
de valor —nadie te cambia tu cadena por detrás— con el coste de la referencia mientras no haga falta
copiar.

Es el mismo mecanismo que usan PHP, Swift y las cadenas de Delphi, y explica por qué en Pascal se
pueden pasar cadenas grandes por valor sin pensárselo.

El bucle de este programa **sigue siendo cuadrático**, porque `Sec + IntToStr(I)` crea un resultado
nuevo cada vuelta. La versión lineal usa `SetLength` para reservar y escribir por índice, o
`TStringBuilder` en Delphi — el mismo patrón del acumulador que aparece en todos los lenguajes de
cadenas con semántica de valor.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let ((n (read)))
  (format t "sec=~{~D~^-~}~%" (loop for i from 1 to n collect i)))
```

**Lo que esta clase enseña en Common Lisp.** La solución no construye ninguna cadena: construye
**una lista** y deja que `format` la recorra. `~{` … `~}` itera sobre los elementos, `~D` imprime
cada uno, y **`~^` corta la iteración si no quedan más**, lo que hace que el guion aparezca *entre*
los elementos y no al final. Es el problema del separador resuelto en cuatro caracteres.

Y esta clase toca el corazón de la distinción de Lisp entre **funciones destructivas y no
destructivas**, que el lenguaje marca por convención en el nombre:

| No destructiva | Destructiva | Qué hace la destructiva |
|---|---|---|
| `append` | `nconc` | Reutiliza las celdas en vez de copiar |
| `remove` | `delete` | Modifica la lista original |
| `reverse` | `nreverse` | Invierte los punteros en el sitio |
| `sort` (copia) | `sort` sobre la propia lista | Puede destruir el original |

Las destructivas empiezan por `n` —de *non-consing*, "sin reservar memoria"— y son mucho más
rápidas. También son la fuente de los errores más difíciles del lenguaje, porque **el argumento
original queda en un estado indeterminado** y seguir usándolo produce comportamientos imposibles de
reproducir.

La regla de la comunidad es clara y vale para cualquier lenguaje: **usa la versión no destructiva
hasta que midas que importa**, y cuando uses la destructiva, no vuelvas a tocar el original.
Para acumular texto, el idioma es `with-output-to-string`, que es un `StringBuilder` con otra cara.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea
set n [string trim $linea]

set sec {}
for {set i 1} {$i <= $n} {incr i} {
    lappend sec $i
}

puts "sec=[join $sec -]"
```

**Lo que esta clase enseña en Tcl.** `lappend` y `join` en lugar de concatenar en el bucle, y esa
elección es exactamente el tema de la clase.

En Tcl todo valor es **inmutable a nivel semántico**: `set b $a` no copia, comparte la representación
interna y sube un contador de referencias —igual que el `AnsiString` de Pascal—. Y aquí está la
optimización que hay que conocer, porque es la razón de escribir `lappend` y no `set sec "$sec $i"`:

**`lappend` está especializado para modificar en el sitio cuando el contador de referencias es 1.**
Si nadie más comparte la lista, la amplía sin copiar. `set sec "$sec-$i"` construiría una cadena
nueva cada vuelta, y el bucle sería cuadrático.

La misma optimización existe en `append` para cadenas:

```tcl
append sec "-$i"      ;# modifica en el sitio si es posible: LINEAL
set sec "$sec-$i"     ;# construye una cadena nueva: CUADRÁTICO
```

Dos líneas que hacen lo mismo con complejidades distintas. Es el detalle de rendimiento más citado en
la comunidad Tcl, y es la versión de este lenguaje del `StringBuilder` de Java: el mecanismo está
ahí, pero hay que usar el comando correcto para activarlo.

`join $sec -` une la lista con el separador, resolviendo el problema del guion sin ningún `if`.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $n = <STDIN>;
chomp $n;

print "sec=", join('-', 1 .. $n), "\n";
```

**Lo que esta clase enseña en Perl.** Una línea, y sin bucle. `1 .. $n` es el **operador de rango**,
que en contexto de lista genera todos los enteros, y `join` los une con el separador. El problema del
guion intercalado desaparece porque nunca se construye la cadena a mano.

Sobre la mutabilidad, Perl es el más permisivo de esta página: **las cadenas son mutables y se pueden
modificar en el sitio de formas que en Java o Python no existen**.

```perl
my $s = "hola mundo";
substr($s, 0, 4) = "HOLA";     # substr como DESTINO de una asignación
substr($s, 0, 4, "adio");      # o con cuatro argumentos, misma idea
$s =~ tr/a-z/A-Z/;             # transliteración EN EL SITIO
$s =~ s/mundo/planeta/;        # sustitución EN EL SITIO
chop $s;  chomp $s;            # recortan la variable, no devuelven copia
```

Y el acumulador es lineal sin trucos: `$sec .= "-$i"` en un bucle **modifica el escalar**, ampliando
su búfer cuando hace falta. No hay `StringBuilder` en Perl porque no hace falta — la cadena ya es un
búfer que crece.

Ese es el intercambio de Perl en esta clase: máxima eficiencia al modificar y **ninguna garantía de
que nadie te cambie una cadena por debajo**. Si pasas un escalar a una función, esa función puede
modificarlo, porque `@_` contiene **alias** de los argumentos originales, no copias. Es un detalle que
sorprende y que conviene conocer antes de leer código ajeno.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>
#include <string>

int main() {
    int n{};
    if (!(std::cin >> n)) return 1;

    std::string sec;
    sec.reserve(static_cast<std::size_t>(n) * 4);   // reserva: evita realojos

    for (int i = 1; i <= n; ++i) {
        if (i > 1) sec += '-';
        sec += std::to_string(i);
    }

    std::cout << "sec=" << sec << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** `std::string` es **mutable** y `+=` modifica en el sitio: amplía
el búfer interno cuando se queda corto, duplicando su capacidad. Por eso este bucle es amortizadamente
lineal y no cuadrático, al contrario que el equivalente en Java con `String`.

Y `reserve()` es la línea que hay que entender. Sin ella, la cadena crece a saltos y cada salto
**copia todo lo acumulado** a un búfer nuevo; con ella, se reserva una vez y no hay ningún realojo.
Es el mismo concepto que `ArrayList.ensureCapacity` en Java o `Vec::with_capacity` en Rust, y es la
optimización más rentable que existe cuando se conoce el tamaño aproximado de antemano.

C++ separa además **capacidad** de **tamaño**, y las expone las dos: `size()` es cuánto hay,
`capacity()` es cuánto cabe sin volver a reservar. Casi ningún lenguaje de esta página deja ver esa
diferencia; en C++ es parte de la interfaz porque el control de la memoria es el punto.

Y el contrapunto: la mutabilidad tiene un coste de corrección que C++ gestiona con `const`.

```cpp
void mostrar(const std::string& s);   // promete no modificar: se pasa sin copiar
void modificar(std::string& s);       // puede modificar: el llamante lo ve en la firma
void copiar(std::string s);           // copia entera
```

Esas tres firmas son tres contratos distintos, visibles en el punto de llamada. Es la respuesta de
C++ al problema que Perl deja abierto con los alias de `@_`.

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

dcl-pi SECUENC;
  n int(10) const;
end-pi;

dcl-s sec    varchar(500) inz('');
dcl-s i      int(10);
dcl-s salida char(520);

for i = 1 to n;
  if i > 1;
    sec += '-';
  endif;
  sec += %char(i);
endfor;

salida = 'sec=' + sec;
dsply salida;

*inlr = *on;
return;
```

**Lo que esta clase enseña en RPG.** `varchar(500)` es un búfer de 500 bytes con un contador de
longitud delante, y `+=` **escribe sobre él y actualiza el contador**. No hay reserva, no hay realojo
y no hay recolector: el bucle es lineal y el consumo de memoria está decidido en la declaración.

Es el mismo modelo de COBOL —memoria estática, escritura en el sitio— pero con la longitud
gestionada por el lenguaje en vez de por un contador a mano. Ese es el salto que RPG dio con
`varchar` y que COBOL solo ofrece desde 2002.

El límite es real y hay que dimensionarlo: si la secuencia pasa de 500 caracteres, **se trunca**.
En RPG moderno el máximo de un `varchar` es de 16 MB, así que sobra margen, pero la decisión sigue
siendo del programador. Y para tamaños de verdad grandes existen los campos `CLOB`.

Fíjate en el operador `+=`, que RPG incorporó en la versión 7.1 junto a `-=`, `*=` y `/=`. Antes se
escribía `sec = sec + '-'`, con el mismo efecto: el compilador ya reconocía el patrón y escribía en
el sitio. La novedad fue sintáctica, no semántica — pero cambió cómo se lee el código, que en un
lenguaje que se mantiene durante treinta años no es poco.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 secuencia: procedure options(main);

    declare n   fixed binary(31);
    declare i   fixed binary(31);
    declare sec character(500) varying initial('');

    get list (n);

    do i = 1 to n;
       if i > 1 then sec = sec || '-';
       sec = sec || trim(char(i));
    end;

    put skip list ('sec=' || sec);

 end secuencia;
```

**Lo que esta clase enseña en PL/I.** `character(500) varying` es el mismo modelo que el `varchar` de
RPG: un búfer de tamaño máximo declarado, con la longitud actual guardada delante. La asignación
`sec = sec || '-'` **escribe sobre el mismo almacenamiento**, así que el bucle es lineal.

Lo que PL/I añade a esta clase es un concepto que no tiene ningún otro lenguaje de la página: la
**variable `DEFINED`**, que da un nombre alternativo a un almacenamiento que ya existe.

```pli
declare buffer  character(500);
declare cabecera character(10) defined(buffer);              /* los 10 primeros */
declare cuerpo   character(490) defined(buffer) position(11);/* del 11 en adelante */
```

`cabecera` y `cuerpo` **no son copias**: son ventanas sobre `buffer`. Modificar una modifica el otro,
porque son la misma memoria vista con otro nombre y otro tipo. Es una `union` de C con sintaxis de
declaración, y en su día era la forma de descomponer un registro leído de un fichero sin copiarlo.

Visto hoy es exactamente lo que hace `std::string_view` en C++ o un *slice* en Go y Rust: **una vista
sobre memoria ajena**. Con el mismo peligro, que en PL/I no está mitigado por nada: si `buffer` se
reasigna, las ventanas siguen apuntando ahí.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
SECUEN ; Secuencia -- clase 054
 read n
 set sec = ""
 for i = 1:1:n do
 . set:i>1 sec = sec _ "-"
 . set sec = sec _ i
 write "sec=", sec, !
 quit
```

**Lo que esta clase enseña en M.** Tres cosas de sintaxis y una de fondo.

De sintaxis: **`for i = 1:1:n`** es "desde 1, de 1 en 1, hasta n" —los dos puntos separan inicio,
incremento y final—. El **punto al principio de línea** marca el nivel de anidamiento del bloque que
abre `do`. Y **`set:i>1`** es el postcondicional: el comando se ejecuta solo si la condición se
cumple, sin necesidad de un `if`.

De fondo: en M las cadenas son mutables y `_` concatena sobre el mismo valor, así que el bucle es
eficiente. Pero **la verdadera lección de mutabilidad en M está en los *globals***.

```mumps
set ^LISTA(1) = "uno"      ; esto YA está en disco
set ^LISTA(1) = "UNO"      ; y esto lo ha modificado, para todos los procesos
```

No hay una operación de guardado. **La asignación es la escritura.** Y es visible inmediatamente para
cualquier otro proceso que lea ese nodo, sin caché que invalidar ni sesión que sincronizar.

Eso convierte la mutabilidad en un asunto de **concurrencia**, no de rendimiento, y por eso M tiene
`lock` —bloqueos por nodo, cooperativos— y `tstart`/`tcommit` para transacciones. En un lenguaje donde
asignar una variable puede modificar el historial clínico que otro terminal está leyendo, la pregunta
"¿esto es mutable?" tiene una respuesta con consecuencias muy distintas de las de un `String` en Java.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| n sec |

n := stdin nextLine trimBoth asNumber.

sec := String streamContents: [ :flujo |
    (1 to: n)
        do:           [ :i | flujo print: i ]
        separatedBy:  [ flujo nextPut: $- ] ].

Transcript show: 'sec=', sec; cr.
```

**Lo que esta clase enseña en Smalltalk.** `String streamContents:` es el `StringBuilder` de
Smalltalk, y existe desde mucho antes de que Java lo necesitara. Crea un `WriteStream` sobre un búfer
que crece, ejecuta el bloque escribiendo en él, y devuelve la cadena final. **Una sola reserva
amortizada, en vez de una cadena nueva por vuelta.**

Si el bucle usara `sec := sec , i printString`, cada `,` construiría una colección nueva copiando
todo lo anterior: cuadrático. La distinción entre las dos formas es exactamente el contenido de esta
clase.

Y **`do:separatedBy:`** merece atención propia: es un mensaje de `Collection` que ejecuta el primer
bloque por cada elemento y el segundo **solo entre elementos**. El problema del separador —que en
COBOL, C++ y RPG exige un `if i > 1`— aquí es un método de la biblioteca. Es la misma solución que el
`~^` de Lisp y el `join` de Perl y Tcl, obtenida sin sintaxis especial: solo un método más en
`Collection` que alguien escribió una vez.

Sobre la mutabilidad en general, Smalltalk es mutable por defecto y ofrece la inmutabilidad como
propiedad del objeto: `unObjeto beReadOnlyObject` marca cualquier instancia como de solo lectura, y
cualquier intento de modificarla dispara una excepción capturable. Los literales de cadena de los
métodos compilados están marcados así en Pharo — porque, como se vio en la clase 048, son parte del
propio código.

---

## Y de vuelta a la clase

La regla transferible es la del **acumulador**: concatenar dentro de un bucle con el operador normal
es cuadrático en los lenguajes de cadenas inmutables —Java, C#, Python, y también Lisp y Smalltalk si
usas `,`— porque cada vuelta copia todo lo acumulado. La solución tiene el mismo nombre en todas
partes aunque se escriba distinto: **un búfer que crece** — `WriteStream`, `with-output-to-string`,
`StringBuilder`, `std::string::reserve`, `Unbounded_String`. Reconocer ese patrón es lo que se lleva
uno de esta clase.

⏮️ [Volver a la clase 054](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
