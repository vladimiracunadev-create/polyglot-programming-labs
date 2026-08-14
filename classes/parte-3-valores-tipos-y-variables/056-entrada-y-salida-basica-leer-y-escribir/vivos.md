# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 056

> [⬅️ Volver a la clase 056](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Leer una línea y devolverla. El programa más simple posible, y el que cierra la Parte 3 con la
pregunta que la atraviesa entera: **¿de dónde vienen los datos y quién decide de dónde?** Porque en
la mitad de estos lenguajes el programa **no sabe** si lee de un teclado, de un fichero o de una
cinta — y esa ignorancia deliberada es una de las mejores ideas de la informática.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es **la abstracción del canal de entrada y salida**, y estos lenguajes lo enseñan
> mejor que el núcleo por un motivo histórico: **inventaron la idea**. Fortran habla con **unidades
> numeradas**, no con ficheros. COBOL declara nombres lógicos que alguien conecta fuera. M escribe al
> **dispositivo actual**, sea el que sea. Y [JCL](../../../atlas/jcl.md) —que por eso aparece en esta
> clase y no en otras— es literalmente el lenguaje de **conectar los nombres lógicos de un programa a
> ficheros reales en el momento de ejecutar**.
>
> Eso que hoy llamamos inyección de dependencias, configuración por entorno o volúmenes montados es
> esto, y estaba resuelto en 1964.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: una línea de texto → stdout: `eco: <la línea leída>`
- **Regla:** `salida = 'eco: ' + entrada`

| stdin | esperado |
|---|---|
| `hola` | `eco: hola` |
| `Polyglot` | `eco: Polyglot` |
| `123` | `eco: 123` |

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
PROGRAM-ID. ECO.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(200).

PROCEDURE DIVISION.
    ACCEPT LINEA
    DISPLAY "eco: " FUNCTION TRIM(LINEA)
    STOP RUN.
```

**Lo que esta clase enseña en COBOL.** `ACCEPT` y `DISPLAY` son la E/S **de conversación**: rápida de
escribir y pensada para mensajes al operador, no para datos. La E/S de verdad en COBOL es la de
ficheros, y es donde aparece la idea que importa:

```cobol
ENVIRONMENT DIVISION.
INPUT-OUTPUT SECTION.
FILE-CONTROL.
    SELECT CLIENTES ASSIGN TO ENTRADA
        ORGANIZATION IS SEQUENTIAL.

DATA DIVISION.
FILE SECTION.
FD  CLIENTES.
01  REG-CLIENTE   PIC X(200).
```

**`ASSIGN TO ENTRADA` no nombra ningún fichero.** `ENTRADA` es un **nombre lógico** —un *ddname*—, y
quién sea de verdad lo decide el [JCL](../../../atlas/jcl.md) en el momento de ejecutar. El mismo
programa, sin recompilar, lee hoy un fichero de pruebas de cien registros y mañana el de producción
de diez millones.

Eso es **independencia del dispositivo**, y en 1959 era revolucionario: el programa deja de saber
dónde están sus datos. Es la misma idea que hoy se implementa con variables de entorno, con
inyección de dependencias o montando un volumen en un contenedor.

Y `ORGANIZATION` declara la estructura —`SEQUENTIAL`, `INDEXED`, `RELATIVE`—, así que un fichero
indexado se lee por clave (`READ ... KEY IS`) con la misma sintaxis con la que se recorre uno
secuencial. COBOL tenía acceso por clave en el lenguaje décadas antes de que existieran las bases de
datos relacionales.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program eco
   implicit none
   character(len=200) :: linea

   read(*, '(A)') linea

   write(*, '(A,A)') 'eco: ', trim(linea)
end program eco
```

**Lo que esta clase enseña en Fortran.** El asterisco de `read(*, ...)` y `write(*, ...)` no significa
"la consola": significa **la unidad por defecto**. Y ahí está la idea de Fortran para esta clase — la
E/S va contra **unidades numeradas**, no contra ficheros.

```fortran
open(unit=10, file='datos.txt', status='old', action='read')
read(10, '(A)') linea
close(10)

write(6, *) 'a la salida estándar'    ! 6 y 5 son las unidades históricas
```

Un número entero identifica un canal abierto. Cambiar de dónde lee un procedimiento es pasarle otro
número, sin tocar su código:

```fortran
subroutine procesar(unidad)
   integer, intent(in) :: unidad
   read(unidad, '(A)') linea      ! le da igual si es un fichero o el teclado
end subroutine
```

Es exactamente la misma abstracción que el *ddname* de COBOL y el descriptor de fichero de Unix,
expresada como un número que se pasa por parámetro. Fortran moderno añadió `newunit=` para que el
sistema asigne un número libre y no haya colisiones —el problema clásico de los números fijos—, y las
constantes con nombre `input_unit`, `output_unit` y `error_unit` en `iso_fortran_env`.

Y `read(*, '(A)')` con formato `A` lee la línea **tal cual**; con formato `*` —lista— la interpretaría
buscando valores separados, que es lo que hacen el resto de programas de este curso.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO; use Ada.Text_IO;

procedure Eco is
   Linea  : String (1 .. 200);
   Ultimo : Natural;
begin
   Get_Line (Linea, Ultimo);

   Put_Line ("eco: " & Linea (1 .. Ultimo));
end Eco;
```

**Lo que esta clase enseña en Ada.** `Ada.Text_IO` opera sobre un **fichero actual** implícito, y las
versiones sin argumento de `Get_Line` y `Put_Line` lo usan. Cambiar el destino de un programa entero
es una línea:

```ada
Set_Output (Mi_Fichero);      --  a partir de aquí, todo Put_Line va ahí
Put_Line ("esto va al fichero");
Set_Output (Standard_Output); --  y de vuelta
```

Es el mismo mecanismo que el dispositivo actual de M y que la redirección del shell, dentro del
lenguaje.

Lo que Ada aporta de propio es que **la E/S está fuertemente tipada y es genérica**. No hay un `Put`
que sirva para todo: hay un paquete por tipo, y los de los tipos numéricos son **instancias de un
genérico**:

```ada
package Ada.Integer_Text_IO is new Ada.Text_IO.Integer_IO (Integer);
package Mi_IO is new Ada.Text_IO.Integer_IO (Mi_Tipo_Entero);   --  para TU tipo
```

Por eso los programas de este curso importan `Ada.Integer_Text_IO` y `Ada.Long_Float_Text_IO` por
separado. Es más verboso que un `print` universal y a cambio **la lectura valida el tipo**: leer un
`Descuento_T` con rango `0.0 .. 1.0` —como en la clase 041— rechaza un 1.5 en el propio `Get`, sin
ninguna comprobación escrita.

Y `Get_Line` devuelve la longitud en `Ultimo` porque `String` es de tamaño fijo, como se vio en la
clase 048.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Eco;
{$MODE OBJFPC}{$H+}

var
  Linea: string;

begin
  ReadLn(Linea);

  WriteLn('eco: ', Linea);
end.
```

**Lo que esta clase enseña en Pascal.** `Read`, `ReadLn`, `Write` y `WriteLn` no son funciones
normales: son **construcciones del compilador**. Aceptan cualquier número de argumentos, de tipos
distintos, y con los especificadores `:ancho:decimales` que se vieron en la clase 041. Ninguna función
de Pascal escrita por un usuario puede hacer eso.

Esa es una decisión de diseño interesante: Wirth prefirió **incorporar la E/S al lenguaje** en vez de
darle a los usuarios variadicidad y polimorfismo. Es coherente con su idea de mantener el lenguaje
pequeño, y es la razón de que Pascal no tenga sobrecarga de funciones en su forma original.

El fichero es un **tipo del lenguaje**, no un objeto de biblioteca:

```pascal
var
  F: TextFile;              { fichero de texto }
  D: file of TRegistro;     { fichero TIPADO: registros de TRegistro }
begin
  AssignFile(F, 'datos.txt');
  Reset(F);                 { abrir para leer }
  ReadLn(F, Linea);         { la misma ReadLn, con el fichero delante }
  CloseFile(F);
```

`file of TRegistro` es un fichero **con tipo**: cada `Read` devuelve un registro completo, y el
compilador conoce su tamaño. Es el equivalente del `FD` de COBOL, y no existe en C ni en Java, donde
un fichero es una secuencia de bytes y la estructura la pone el programador.

Y `ReadLn(F, X)` es la misma `ReadLn` con un argumento más: el canal por defecto es `Input` y se puede
sustituir. La misma idea que `Set_Output` en Ada.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let ((linea (read-line)))
  (format t "eco: ~A~%" linea))
```

**Lo que esta clase enseña en Common Lisp.** Lisp tiene **flujos** (*streams*) como objetos de primera
clase, y las funciones de E/S aceptan uno como argumento opcional. Sin él usan `*standard-input*` y
`*standard-output*`, que son **variables especiales** — y ahí está lo interesante.

Al ser variables, se pueden **reenlazar dinámicamente** para un fragmento de código:

```lisp
(with-open-file (f "salida.txt" :direction :output)
  (let ((*standard-output* f))
    (imprimir-informe)))     ; TODO lo que imprima esta función va al fichero
```

`imprimir-informe` no sabe nada de ficheros: escribe con `format t`, y el `t` significa
"`*standard-output*`". Al reenlazar la variable, **todo el árbol de llamadas** cambia de destino sin
que ninguna función lo sepa. Es la redirección del shell, dentro del lenguaje y con ámbito dinámico.

Ese mismo mecanismo da uno de los idiomas más útiles de Lisp:

```lisp
(with-output-to-string (s)
  (dotimes (i 5) (format s "~D-" i)))    ; => "0-1-2-3-4-"
```

Capturar en una cadena la salida de un código que cree estar imprimiendo. Es el `StringBuilder` de la
clase 054 y a la vez la forma de probar código que imprime, sin tocarlo.

Y `read-line` devuelve además **un segundo valor** que indica si la línea terminó por fin de fichero
en vez de por salto de línea — otra vez el patrón de los valores múltiples.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea

puts "eco: $linea"
```

**Lo que esta clase enseña en Tcl.** `stdin`, `stdout` y `stderr` son **canales**, y un canal es
simplemente una cadena que identifica un flujo abierto. `open` devuelve otra, y todos los comandos de
E/S aceptan cualquiera:

```tcl
set canal [open "datos.txt" r]
gets $canal linea
close $canal

set canal [open "|comando externo" r]     ;# una TUBERÍA, con el mismo comando
set canal [socket www.ejemplo.com 80]     ;# un SOCKET, con el mismo comando
```

Ficheros, tuberías y sockets son **el mismo tipo de cosa** y se manejan con `gets`, `puts`, `read`,
`flush` y `close` sin distinción. Es la abstracción de Unix llevada al lenguaje de guion, y explica
por qué Tcl fue durante años tan popular para automatizar sistemas.

Y `fconfigure` es donde se ajusta todo lo que en otros lenguajes exige clases distintas:

```tcl
fconfigure $canal -translation binary    ;# sin traducir saltos de línea
fconfigure $canal -encoding utf-8        ;# codificación del canal
fconfigure $canal -blocking 0            ;# lectura no bloqueante
```

Ese último es el que importa: con `-blocking 0` más `fileevent`, Tcl hace **E/S asíncrona dirigida
por eventos** — un bucle de eventos con retrollamadas, en 1990. Es el modelo que Node.js popularizó
quince años después, disponible aquí desde el principio y por la misma razón: un lenguaje de guion
que tiene que atender varias cosas a la vez sin hilos.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;

print "eco: $linea\n";
```

**Lo que esta clase enseña en Perl.** `<STDIN>` es el **operador de diamante** aplicado a un manejador
de fichero, y su comportamiento depende del contexto: en contexto escalar da una línea, en contexto de
lista da todas. Es la misma dualidad de la clase 041.

Pero lo que hay que llevarse de Perl en esta clase es `<>` **a secas**, el diamante mágico:

```perl
while (my $linea = <>) {
    print "eco: $linea";
}
```

`<>` lee de **los ficheros nombrados en la línea de comandos**, uno tras otro, y si no hay ninguno lee
de la entrada estándar. Con esas cinco líneas el programa se comporta exactamente como `cat`, `grep`
o `sort`: `programa.pl a.txt b.txt` o `cat a.txt | programa.pl` funcionan igual, sin escribir una sola
línea de gestión de argumentos.

Ese comportamiento es **la convención de las herramientas de Unix**, incorporada al lenguaje. Es la
razón de que Perl desplazara a `awk` y `sed` en los 90: escribir un filtro correcto costaba una línea.

Y las opciones de línea de comandos llevan la idea al extremo:

```bash
perl -ne 'print if /ERROR/' registro.log       # -n envuelve en el bucle <>
perl -pe 's/viejo/nuevo/' fichero              # -p además imprime cada línea
perl -i.bak -pe 's/a/b/g' *.conf               # -i edita EN EL SITIO con copia
```

`-n` y `-p` generan el bucle de lectura por ti. Es E/S como parte de la invocación del programa, no
del programa.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>
#include <string>

int main() {
    std::string linea;
    if (!std::getline(std::cin, linea)) return 1;

    std::cout << "eco: " << linea << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** `std::cin` y `std::cout` son **flujos**, y `>>` y `<<` son
operadores sobrecargados sobre ellos. Que la E/S se escriba con los operadores de desplazamiento de
bits fue una decisión discutida en su día y hoy es la marca de la casa.

La ventaja real es la **seguridad de tipos**: `std::cout << x` elige la sobrecarga correcta según el
tipo de `x`, mientras que `printf("%d", x)` con `x` de otro tipo compila y lee la pila mal. Y funciona
con tipos propios sin tocar nada del sistema:

```cpp
std::ostream& operator<<(std::ostream& os, const Punto& p) {
    return os << '(' << p.x << ", " << p.y << ')';
}
std::cout << mi_punto << '\n';     // ya funciona
```

Y como todos los flujos comparten interfaz, una función que reciba `std::ostream&` escribe
indistintamente en la consola, en un fichero (`std::ofstream`) o en una cadena
(`std::ostringstream`) — que es el `with-output-to-string` de Lisp y la clave para poder **probar**
código que imprime.

Dos avisos prácticos de esta clase. Primero: `std::getline` lee la línea entera **incluidos los
espacios**, mientras que `std::cin >> s` se detiene en el primer espacio; mezclarlos deja el salto de
línea pendiente en el búfer y produce una lectura vacía inesperada. Segundo: para E/S masiva,
`std::ios::sync_with_stdio(false)` desactiva la sincronización con `printf` y multiplica la velocidad
— el detalle que todo el mundo descubre en su primer problema de programación competitiva.

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

dcl-pi ECO;
  linea varchar(200) const;
end-pi;

dcl-s salida char(220);

salida = 'eco: ' + %trim(linea);
dsply salida;

*inlr = *on;
return;
```

**Lo que esta clase enseña en RPG.** `dsply` es el equivalente de `ACCEPT`/`DISPLAY` de COBOL: una
línea de conversación, útil para depurar y nada más. La E/S real de RPG es la que define la
plataforma, y tiene tres formas que conviene distinguir:

```rpgle
dcl-f CLIENTES  usage(*input);              // fichero de base de datos
dcl-f PANTALLA  workstn;                    // fichero de PANTALLA (display file)
dcl-f INFORME   printer oflind(*in90);      // fichero de IMPRESORA
```

Las tres se declaran igual y se leen y escriben con los mismos verbos —`read`, `chain`, `write`,
`exfmt`—. Un fichero de pantalla se describe **fuera del programa**, en DDS o en un diseñador visual,
y `exfmt` (*execute format*) escribe la pantalla y lee la respuesta del usuario en una sola operación.

Ese es el rasgo distintivo: **en IBM i la pantalla es un fichero**. La misma abstracción que COBOL
aplica a las cintas y Unix a los dispositivos, llevada a la interfaz de usuario. Un programa RPG no
"pinta" una pantalla: escribe un registro en un fichero que resulta ser un terminal.

Y el fichero de base de datos aparece como **variables del programa**: al declarar `dcl-f CLIENTES`,
los campos de la tabla son nombres directamente utilizables. Sin ORM, sin mapeo y sin serialización —
la distancia entre el registro en disco y la variable en memoria es cero, como en
[M](../../../atlas/mumps.md).

### JCL

[Ficha completa](../../../atlas/jcl.md) · z/OS: proceso por lotes de banca, seguros y administración · `SUBMIT desde ISPF, o zowe jobs submit`

> JCL **no calcula**: describe qué programa se ejecuta y a qué ficheros reales se conectan sus nombres lógicos. Aparece en las clases donde ese reparto de responsabilidades es justamente lo que se estudia.

```text
//ECO      JOB (CONTAB),'ECO DE UNA LINEA',CLASS=A,MSGCLASS=X,
//             NOTIFY=&SYSUID
//*
//* El programa COBOL de esta clase lee de SYSIN y escribe en SYSOUT.
//* NO SABE que hay al otro lado: lo decide este JCL, al ejecutar.
//*
//EJECUTA  EXEC PGM=ECO
//STEPLIB  DD DSN=VLAD.LOADLIB,DISP=SHR
//SYSOUT   DD SYSOUT=*
//SYSIN    DD *
hola
/*
//
```

**Lo que esta clase enseña en JCL.** Esta es la clase para la que JCL existe, y por eso aparece aquí
y no en las anteriores.

El programa COBOL de más arriba dice `ACCEPT` y `DISPLAY`, o —en un programa de verdad— declara
`SELECT ENTRADA ASSIGN TO SYSIN`. **En ningún sitio nombra un fichero.** Las sentencias `DD` de este
JCL son las que conectan esos nombres lógicos con algo real, **en el momento de ejecutar**:

```text
//SYSIN    DD *                                   <- los datos van aquí mismo
//SYSIN    DD DSN=VLAD.PRUEBAS.PEQUENO,DISP=SHR   <- un fichero de pruebas
//SYSIN    DD DSN=PROD.CLIENTES.DIARIO,DISP=SHR   <- diez millones de registros
//SYSIN    DD DUMMY                               <- nada, fichero vacío
```

**Cuatro orígenes distintos, cero cambios en el programa y cero recompilaciones.** Ese es el concepto
completo de esta clase, y está resuelto desde 1964.

Es exactamente lo que hoy se consigue con una variable de entorno, con un volumen montado en un
contenedor o con inyección de dependencias, y el vocabulario ha cambiado más que la idea. Cuando el
manifiesto de los doce factores dice *"guarda la configuración en el entorno"*, está redescubriendo
la sentencia `DD`.

`DD SYSOUT=*` envía la salida al *spool*, de donde se recoge después; `DD DUMMY` conecta el nombre a
la nada, que es el `/dev/null` del mainframe. Y `//SYSIN DD *` con los datos en línea es lo que hace
que este trabajo sea autocontenido — el equivalente exacto del *here-document* de un shell.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 eco: procedure options(main);

    declare linea character(200) varying;

    on endfile(sysin) stop;

    get edit (linea) (a(200));

    put skip list ('eco: ' || trim(linea));

 end eco;
```

**Lo que esta clase enseña en PL/I.** PL/I distingue **tres modos de E/S**, y tener los tres con
sintaxis propia es muy característico del lenguaje:

| Modo | Sintaxis | Para qué |
|---|---|---|
| **Dirigida por lista** | `get list (a, b);` | Valores separados; lo más cómodo |
| **Dirigida por edición** | `get edit (x) (a(20));` | Posiciones y formatos exactos |
| **Dirigida por datos** | `get data;` | El **dato trae su propio nombre** |

La tercera es la que no tiene equivalente. Con `get data`, la entrada es `A=5, B=7;` y PL/I **asigna
a las variables `A` y `B` del programa por su nombre**. Es autodescriptiva: el fichero de entrada
lleva las claves, como un JSON o un `.ini`, en 1964. Y `put data;` hace lo inverso, volcando el valor
de las variables con su nombre — que es exactamente lo que se necesita para depurar.

Y `on endfile(sysin) stop;` es el manejo del fin de fichero mediante el mecanismo `ON` de la clase
041: se **instala** un manejador y queda activo, en vez de comprobar el resultado de cada lectura.
Comparado con el `if (!getline(...))` de C++ o el `while (my $l = <>)` de Perl, es un modelo
distinto: **el fin de fichero es una condición, no un valor de retorno**.

Ese enfoque —condiciones instaladas en lugar de códigos comprobados— es el antepasado directo de las
excepciones, y la razón de que PL/I aparezca en cualquier historia del manejo de errores.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
ECO ; Eco de una linea -- clase 056
 read linea
 write "eco: ", linea, !
 quit
```

**Lo que esta clase enseña en M.** M no tiene `stdin` ni `stdout`: tiene **el dispositivo actual**.
`read` y `write` operan sobre él, sea el que sea, y `use` lo cambia:

```mumps
 open "/tmp/salida.txt":("NEW"):10       ; abrir con tiempo de espera
 use "/tmp/salida.txt"                   ; a partir de aquí, write va ahí
 write "esto va al fichero",!
 use $principal                          ; de vuelta al dispositivo original
 close "/tmp/salida.txt"
```

`$principal` es la variable del sistema que guarda el dispositivo con el que arrancó el proceso. La
idea es la misma que `Set_Output` en Ada y que reenlazar `*standard-output*` en Lisp: **el destino es
estado del proceso, no un argumento de cada escritura**.

Y `write` tiene un mini-lenguaje de control propio que conviene reconocer al leer código M:

```mumps
 write "hola",!          ; ! = nueva línea
 write "hola",#          ; # = nueva página (form feed)
 write ?20,"columna 20"  ; ?n = tabular a la columna n
 write *65               ; *n = escribe el carácter con ese código
```

`?20` para tabular a una columna concreta delata para qué se diseñó esto: **informes impresos en
terminales de ancho fijo**. Es el mismo problema que resuelven los campos editados de COBOL y los
descriptores de formato de Fortran, con una tercera sintaxis distinta — tres respuestas de la misma
época a la misma necesidad.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| linea |

linea := stdin nextLine.

Transcript show: 'eco: ', linea; cr.
```

**Lo que esta clase enseña en Smalltalk.** La E/S es **un objeto más**, y por eso apenas hay sintaxis
que aprender: `stdin` responde a `nextLine`, `Transcript` responde a `show:`. Los dos son flujos, y
los flujos son colecciones que se recorren.

Lo que hace distinto a Smalltalk en esta clase es que **el concepto de "salida estándar" apenas
existe**, porque el entorno no es una terminal: es una imagen viva con ventanas. `Transcript` es la
ventana de registro del propio sistema, no un descriptor de fichero. Un programa Smalltalk típico no
imprime — **inspecciona**.

```smalltalk
unObjeto inspect.        "abre un inspector sobre el objeto, navegable"
unaColeccion explore.    "abre un explorador del árbol de referencias"
self halt.               "detiene y abre el depurador AQUÍ"
```

Esa es la diferencia cultural que esta clase deja ver. En un lenguaje de terminal, la forma de saber
qué pasa es imprimir; en Smalltalk, es **abrir el objeto y mirarlo**, con su estado real delante y la
posibilidad de modificarlo y continuar. La depuración por `printf` —que el resto de esta página da por
supuesta— es aquí el último recurso, no el primero.

Y para leer y escribir de verdad están `ReadStream`, `WriteStream` y `ReadWriteStream`, que funcionan
igual sobre un fichero, sobre un socket o sobre una colección en memoria. El mismo protocolo, el
mismo código: la abstracción de canal de esta clase, obtenida por polimorfismo en lugar de por
descriptores numerados.

---

## Y de vuelta a la clase

La idea que cierra la Parte 3 es la **independencia del dispositivo**: un programa bien escrito no
nombra ficheros, nombra **canales**, y alguien de fuera decide qué hay al otro lado. Unix lo llamó
después *entrada estándar* y lo convirtió en cultura con las tuberías; el mainframe lo llamó *ddname*
veinte años antes. Cuando escribes un programa que lee de `stdin` en lugar de abrir `datos.txt`,
estás heredando esta decisión — y por eso todas las implementaciones de este curso pueden verificarse
con el mismo `casos.json`.

⏮️ [Volver a la clase 056](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
