# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 119

> [⬅️ Volver a la clase 119](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Registrar manejadores y dejar que algo los invoque en orden. Aquí hay dos lenguajes de esta página que
**definieron cómo se programan las interfaces gráficas**: **Tcl/Tk, cuyo bucle de eventos es de 1990 y
es el modelo de JavaScript**, y **Delphi, que en 1995 popularizó el diseño visual con manejadores de
evento**. Y hay un tercero cuyo modelo de eventos mueve el dinero del mundo: **COBOL bajo CICS**.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es la **inversión del control**: tu código no llama, **es llamado**. Y estos
> lenguajes lo enseñan porque tienen las tres arquitecturas. **El bucle de eventos de un solo hilo**:
> Tcl desde 1990, con `after` y `fileevent`, cinco años antes que JavaScript. **Los eventos como campos
> del objeto**: Delphi con `of object` (clase 085), que es de donde salieron los *delegates* de .NET. Y
> **la cola de mensajes del sistema**: COBOL con CICS y RPG con las colas de datos, donde el
> "manejador" es un programa entero que el monitor arranca cuando llega trabajo.
>
> Y los que **no** pueden tenerlo —Fortran, Ada sin tareas, PL/I— enseñan por qué: **sin funciones que
> se puedan guardar, no hay a quién llamar de vuelta**.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: un entero `n` (número de eventos, n >= 1) → stdout: `eventos=<1-2-...-n>` (orden en que llegaron)
- **Regla:** `por cada i en 1..n, emitir evento i; el callback lo recolecta`

| stdin | esperado |
|---|---|
| `3` | `eventos=1-2-3` |
| `1` | `eventos=1` |
| `4` | `eventos=1-2-3-4` |

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
PROGRAM-ID. EVENTOS.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  N       PIC 9(4) COMP.
01  I       PIC 9(4) COMP.
01  L       PIC 9(4) COMP.
01  SALIDA  PIC X(200) VALUE SPACES.
01  SPOS    PIC 9(4) COMP VALUE 1.
01  ED      PIC Z(3)9.
01  TXT     PIC X(5).

PROCEDURE DIVISION.
    ACCEPT LINEA
    COMPUTE N = FUNCTION NUMVAL(LINEA)

    *> COBOL no tiene retrollamadas: los "eventos" se procesan en orden
    PERFORM VARYING I FROM 1 BY 1 UNTIL I > N
        PERFORM MANEJAR-EVENTO
    END-PERFORM

    COMPUTE L = SPOS - 1
    DISPLAY "eventos=" SALIDA(1:L)
    STOP RUN.

MANEJAR-EVENTO.
    MOVE I TO ED
    MOVE FUNCTION TRIM(ED) TO TXT
    MOVE 0 TO L
    INSPECT FUNCTION REVERSE(TXT) TALLYING L FOR LEADING SPACE
    COMPUTE L = 5 - L
    IF I > 1
        MOVE "-" TO SALIDA(SPOS:1)
        ADD 1 TO SPOS
    END-IF
    MOVE TXT(1:L) TO SALIDA(SPOS:L)
    ADD L TO SPOS.
```

**Lo que esta clase enseña en COBOL.** COBOL **no tiene retrollamadas** —no hay funciones de primera
clase (clase 085)— y sin embargo **casi todo el COBOL en producción se ejecuta como manejador de
eventos**. La diferencia está en dónde ocurre la inversión de control.

En un sistema transaccional, **el programa entero es el manejador**:

```text
Terminal → CICS → arranca el programa COBOL → responde → el programa TERMINA
```

Un programa CICS **no tiene bucle principal ni estado entre llamadas**: se arranca, procesa **un**
mensaje y termina. El monitor decide cuándo, con cuántas copias simultáneas y en qué orden.

```cobol
EXEC CICS RECEIVE MAP('PANTALLA') MAPSET('MENU') END-EXEC
...
EXEC CICS SEND MAP('RESULTADO') MAPSET('MENU') END-EXEC
EXEC CICS RETURN TRANSID('MENU') COMMAREA(ESTADO) END-EXEC
```

**`RETURN TRANSID(...) COMMAREA(...)`** es la clave y merece mirarse: el programa **devuelve el control
al monitor diciendo qué transacción atenderá la respuesta del usuario y qué estado hay que
conservar**.

Eso es exactamente **el modelo sin estado de la web**: cada interacción es una petición independiente,
el estado viaja en un área que va y vuelve —la `COMMAREA` es la *cookie* de sesión— y el servidor
decide qué código atiende cada una.

**CICS es de 1969 y HTTP es de 1991**, y la arquitectura es la misma. La razón también: **con miles de
terminales y una máquina, no se puede tener un proceso esperando por cada usuario**.

COBOL tiene además dos mecanismos de evento más:

- **Las `DECLARATIVES`** (clase 103), manejadores declarativos que el sistema invoca al fallar una
  operación de fichero.
- **Los disparadores de cola de CICS**: una cola transitoria puede **arrancar automáticamente una
  transacción** cuando acumula N elementos. Es un consumidor de cola con disparo automático, de los
  setenta.

Es programación por eventos completa, con la unidad de trabajo puesta en el programa en lugar de en la
función.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program eventos
   implicit none

   abstract interface
      subroutine manejador_i(id)
         integer, intent(in) :: id
      end subroutine manejador_i
   end interface

   procedure(manejador_i), pointer :: manejador
   integer :: n, i
   character(len=400) :: salida
   character(len=20)  :: buf

   read(*, *) n

   manejador => registrar          ! "suscribirse": un puntero a procedimiento

   salida = ''
   do i = 1, n
      call manejador(i)             ! "disparar" el evento
   end do

   write(*, '(A)') 'eventos=' // trim(salida)

contains

   subroutine registrar(id)
      integer, intent(in) :: id
      write(buf, '(I0)') id
      if (len_trim(salida) == 0) then
         salida = trim(buf)
      else
         salida = trim(salida) // '-' // trim(buf)
      end if
   end subroutine registrar

end program eventos
```

**Lo que esta clase enseña en Fortran.** Fortran **no tiene programación por eventos**, y este programa
usa lo único que se le parece: **un puntero a procedimiento** invocado en un bucle (clase 085).

Fíjate en que `registrar` **modifica `salida`, que es una variable del programa anfitrión**. Eso
funciona por el anidamiento léxico de `contains`, y es lo más cerca que llega Fortran de una clausura
(clase 083): **el procedimiento interno ve el entorno mientras el anfitrión esté vivo**.

Un puntero a un procedimiento interno **no se puede guardar más allá de la vida del anfitrión**, así
que el patrón "registrar un manejador y volver" no es viable.

Y no es una carencia relevante para su dominio: **un programa Fortran no espera a nadie**. Lee datos,
calcula durante horas y escribe resultados. No hay interfaz, no hay red y no hay usuario que pulse
botones.

Donde sí aparecen las retrollamadas en Fortran es en la frontera con C, y es un caso técnico
interesante:

```fortran
subroutine mi_manejador(x) bind(c)
   real(c_double), value :: x
end subroutine

call registrar_callback(c_funloc(mi_manejador))
```

**`c_funloc`** —de `iso_c_binding`, Fortran 2003— obtiene un puntero a función **compatible con C**, y
`bind(c)` hace que el procedimiento use la convención de llamada de C. Con eso, una biblioteca escrita
en C puede llamar a código Fortran.

Es lo que hace falta para integrarse con GTK, con MPI, con bibliotecas de gráficos o con cualquier
API que use retrollamadas. Y tiene una restricción reveladora: **solo funciona con procedimientos de
módulo o externos, no con internos**, precisamente porque los internos necesitan el entorno del
anfitrión.

Es la misma frontera de la clase 115: **sin clausuras, la retrollamada no puede llevar estado**, y el
apaño es un módulo con variables globales o un argumento de contexto `void*`.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Eventos is
   package Manejo is
      type Manejador is access procedure (Id : Integer);
      procedure Registrar (Id : Integer);
   end Manejo;

   package body Manejo is
      Primero : Boolean := True;

      procedure Registrar (Id : Integer) is
      begin
         if not Primero then
            Put ("-");
         end if;
         Put (Id, Width => 1);
         Primero := False;
      end Registrar;
   end Manejo;

   use Manejo;

   M : constant Manejador := Registrar'Access;
   N : Integer;
begin
   Get (N);

   Put ("eventos=");
   for I in 1 .. N loop
      M (I);                      --  disparar el evento
   end loop;
   New_Line;
end Eventos;
```

**Lo que esta clase enseña en Ada.** Ada puede registrar manejadores con **accesos a subprograma**, y
tiene un modelo de eventos mucho más ambicioso que eso: **las tareas y las citas** de la clase 107.

```ada
task Servidor is
   entry Evento (Id : Integer);
end Servidor;

task body Servidor is
begin
   loop
      select
         accept Evento (Id : Integer) do
            Procesar (Id);
         end Evento;
      or
         accept Parar;
         exit;
      or
         delay 5.0;                    --  TIEMPO DE ESPERA
         Put_Line ("sin eventos");
      end select;
   end loop;
end Servidor;
```

**El `select` con varias alternativas** es lo que hace de esto un modelo de eventos completo: la tarea
**espera a que ocurra cualquiera de varias cosas** —una llamada a `Evento`, una a `Parar`, o que pasen
cinco segundos— y atiende la primera que llegue.

Eso es exactamente lo que hacen `select()` en Unix, `epoll` en Linux y el bucle de eventos de
JavaScript, **y Ada lo tiene como sintaxis del lenguaje desde 1983**.

Y hay más formas del `select` que cubren todo el espacio:

```ada
select
   Servidor.Evento (5);
or
   delay 1.0;                     --  llamada con TIEMPO LÍMITE
end select;

select
   Servidor.Evento (5);
else
   Put_Line ("ocupado");           --  llamada CONDICIONAL: no bloquea
end select;
```

**Llamada con tiempo límite y llamada que no bloquea**, en la gramática. En casi todos los lenguajes
eso son parámetros de una función de biblioteca.

Y para el hardware, Ada tiene lo que ningún otro lenguaje de esta página: **manejadores de interrupción
como construcción del lenguaje**.

```ada
protected Controlador is
   procedure Manejar_Interrupcion;
   pragma Attach_Handler (Manejar_Interrupcion, Reloj_IRQ);
end Controlador;
```

`Attach_Handler` **asocia un procedimiento de un objeto protegido a una interrupción de hardware**, con
la exclusión mutua garantizada por el runtime. Es programación por eventos en el nivel más bajo
posible, escrita con las mismas construcciones que el resto del programa.

Es la razón de que Ada se siga eligiendo para sistemas empotrados críticos: **el manejador de
interrupción no es una excepción al modelo, es parte de él**.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Eventos;
{$MODE OBJFPC}{$H+}
uses SysUtils;

type
  TManejador = procedure(Id: Integer);

var
  Salida: string;

procedure Registrar(Id: Integer);
begin
  if Salida <> '' then Salida := Salida + '-';
  Salida := Salida + IntToStr(Id);
end;

var
  M: TManejador;
  N, I: Integer;

begin
  Read(N);

  Salida := '';
  M := @Registrar;             { "suscribirse" }

  for I := 1 to N do
    M(I);                       { disparar el evento }

  WriteLn('eventos=', Salida);
end.
```

**Lo que esta clase enseña en Pascal.** Aquí está una de las aportaciones más influyentes de esta
página, y ya se apuntó en las clases 085 y 107: **Delphi popularizó la programación dirigida por
eventos con diseño visual, y su mecanismo es el tipo `of object`**.

```pascal
type
  TNotifyEvent = procedure(Sender: TObject) of object;

  TBoton = class(TControl)
  private
    FOnClick: TNotifyEvent;
  published
    property OnClick: TNotifyEvent read FOnClick write FOnClick;
  end;
```

Tres piezas que juntas hacen todo el modelo:

1. **`of object`** guarda **el método y la instancia** (clase 085), así que el manejador lleva su
   contexto — es un *delegate*.
2. **`property`** (clase 110) hace que asignarlo se escriba como un campo.
3. **`published`** (clase 087) genera la RTTI que permite al **inspector de objetos** mostrarlo y al
   `.dfm` guardarlo (clase 117).

Con eso, el flujo de trabajo que Delphi inventó en 1995 —**arrastrar un botón, hacer doble clic,
escribir el manejador**— funciona sin que el programador escriba una línea de infraestructura.

Y de ahí salió, literalmente, **el modelo de eventos de .NET**: `EventHandler`, `+=` para suscribirse,
las propiedades con `get`/`set`. **Anders Hejlsberg**, arquitecto jefe de Delphi, se fue a Microsoft en
1996 y diseñó C# y .NET (clase 073).

Delphi añadió después el patrón que faltaba para varios suscriptores:

```pascal
FOnChange: TNotifyEvent;              { UN manejador }
FListeners: TList<TNotifyEvent>;       { varios, a mano }
```

**Un evento de Delphi admite un solo manejador**, al contrario que los `event` de C#, que son
multidifusión con `+=` y `-=`. Es una diferencia real, y el patrón Observador con una lista es lo que
se escribe cuando hacen falta varios.

Y en el sistema, el modelo de mensajes de Windows aparece en el lenguaje (clase 110):

```pascal
procedure WMPaint(var Msg: TWMPaint); message WM_PAINT;
```

Un método asociado a un número de mensaje, despachado por el runtime al recibirlo. Es la cola de
mensajes de Win32 integrada en la sintaxis de un lenguaje de propósito general.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let* ((n (read))
       (salida '())
       ;; el "manejador" es una clausura que acumula
       (manejador (lambda (id) (push id salida))))
  (dotimes (i n)
    (funcall manejador (1+ i)))          ; disparar el evento
  (format t "eventos=~{~D~^-~}~%" (nreverse salida)))
```

**Lo que esta clase enseña en Common Lisp.** El manejador de este programa es **una clausura que
acumula estado**, y esa es la pieza que a Fortran, Ada y PL/I les falta: **una retrollamada que lleva
su contexto dentro**.

Lisp tiene además dos mecanismos propios que van más allá de las retrollamadas y que merecen esta
clase.

**El primero: `defmethod` como suscripción.** Como los métodos no pertenecen a las clases (clase 110),
**añadir un comportamiento a un evento es escribir un método en otro fichero**:

```lisp
(defgeneric al-guardar (objeto))
(defmethod al-guardar :after ((o documento)) (indexar o))
(defmethod al-guardar :after ((o documento)) (notificar o))
```

Los `:after` **se acumulan**: varios métodos `:after` sobre la misma función genérica se ejecutan
todos. Eso es multidifusión de eventos conseguida con el sistema de objetos, sin lista de suscriptores
y sin registro.

**El segundo: el sistema de condiciones** (clase 103), que es programación por eventos aplicada a los
errores.

```lisp
(handler-bind ((warning (lambda (c) (registrar c) (muffle-warning c))))
  (procesar))
```

**`handler-bind` registra un manejador que se ejecuta EN EL PUNTO DE LA SEÑAL**, sin desenrollar la
pila. El manejador puede mirar el estado, decidir y **continuar la ejecución**. Es una retrollamada
invocada desde dentro del código que falló.

Comparado con `try/catch`, la diferencia es enorme: un `catch` recibe el control **después** de que la
pila se haya deshecho, cuando el contexto ya no existe. Un manejador de Lisp **está ahí, en el
momento**.

Y con **`restart-case`**, quien señala ofrece opciones y quien maneja elige:

```lisp
(restart-case (error "fichero corrupto")
  (usar-copia () (leer-copia))
  (omitir () nil)
  (reintentar () (volver-a-leer)))
```

Eso es exactamente un menú de eventos: **el código de bajo nivel declara qué se puede hacer, y el de
alto nivel decide cuál**. Es el mecanismo que la clase 116 mencionaba y que ni Java, ni Python, ni
Rust tienen.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
proc manejar {i} {
    global salida
    lappend salida $i
}

gets stdin linea
set n [string trim $linea]

set salida {}
for {set i 1} {$i <= $n} {incr i} {
    after 0 [list manejar $i]      ;# ENCOLAR el evento
}

update                              ;# procesar la cola de eventos

puts "eventos=[join $salida -]"
```

**Lo que esta clase enseña en Tcl.** Este programa **usa un bucle de eventos de verdad**: `after 0`
encola un guion y `update` procesa la cola. No es una simulación.

Y aquí está el dato de esta clase, ya apuntado en la clase 096: **el bucle de eventos de Tcl es de
1990, y es el modelo de JavaScript** — un solo hilo, una cola de tareas pendientes, sin bloqueo y sin
sincronización.

```tcl
after 1000 { ... }                          ;# temporizador
after idle { ... }                            ;# cuando no haya nada más que hacer
fileevent $canal readable { procesar }          ;# E/S: datos disponibles
fileevent $canal writable { enviar }
bind .boton <Button-1> { pulsado }               ;# Tk: eventos de interfaz
vwait bandera                                     ;# procesar hasta que cambie
```

**Un solo mecanismo para temporizadores, entrada/salida e interfaz gráfica.** Y las tres cosas
compiten por la misma cola, así que **un manejador que tarde bloquea todo** — el mismo problema y la
misma disciplina que en JavaScript.

`after idle` merece una nota: encola algo **para cuando no quede trabajo pendiente**, y es lo que Tk
usa internamente para agrupar redibujados. Es el `requestIdleCallback` del navegador, treinta años
antes.

Y **Tk** es la otra mitad de la historia. En 1991, John Ousterhout publicó un conjunto de widgets sobre
Tcl que permitía escribir una interfaz gráfica en veinte líneas:

```tcl
pack [button .b -text "Pulsa" -command { incr n }]
```

**Ese `-command` es la retrollamada**, y es un guion normal. En 1991, escribir una interfaz en X11
significaba cientos de líneas de C con Xlib o Motif. Tk lo redujo a un guion, y por eso se convirtió
en el juego de widgets por defecto de Python, Perl, Ruby y Common Lisp durante años.

Tcl 8.6 añadió las **corrutinas**, que resuelven el problema del cierre de esta clase:

```tcl
coroutine cliente apply {{} {
    set datos [yieldto leer]        ;# se SUSPENDE sin bloquear el bucle
    procesar $datos
}}
```

Es `async`/`await` sin sintaxis nueva (clase 122), sobre el mismo bucle de eventos de 1990.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $n = <STDIN>;
chomp $n;

my @salida;
my @manejadores;

#  suscribir: guardar referencias a subrutina (clase 085)
for my $i (1 .. $n) {
    push @manejadores, sub { push @salida, $i };
}

#  disparar los eventos en orden
$_->() for @manejadores;

print "eventos=", join('-', @salida), "\n";
```

**Lo que esta clase enseña en Perl.** Las **referencias a subrutina** (clase 085) hacen que registrar
manejadores sea trivial, y `my $i` dentro del bucle **crea una variable nueva por vuelta**, así que
cada clausura captura su propio valor.

Ese detalle es importante y es donde muchos lenguajes fallan: en JavaScript con `var` —antes de
`let`— todas las clausuras capturaban **la misma** variable y todas veían el valor final. Perl con
`my` dentro del bucle **no tiene ese problema**, porque cada iteración crea un ámbito nuevo.

Perl tiene además dos mecanismos de evento en el propio lenguaje que merecen esta clase:

**Los manejadores de señal**, que son un hash mágico:

```perl
$SIG{INT}  = sub { print "interrumpido\n"; exit };
$SIG{ALRM} = sub { die "tiempo agotado" };
$SIG{__DIE__} = sub { registrar(@_) };
$SIG{__WARN__} = sub { ... };
alarm(5);
```

**`%SIG` es una tabla de retrollamadas del sistema operativo**, y asignarle una referencia a subrutina
la registra. `__DIE__` y `__WARN__` son *pseudoseñales* que interceptan los errores del propio Perl —
un gancho global sobre el manejo de errores.

**Y las variables ligadas (`tie`)**, que son eventos sobre el acceso a datos:

```perl
tie my %cache, 'MiClase', @args;
#  MiClase::FETCH se llama al LEER, STORE al ESCRIBIR, DELETE al borrar
```

**`tie` convierte cada lectura y escritura de una variable en una llamada a un método.** Es
interceptación total del acceso a datos, y es lo que usan los módulos de caché, las bases de datos
persistentes como `DB_File` y los objetos con propiedades calculadas.

Es exactamente lo que en JavaScript hacen los `Proxy` (2015) y en Python los descriptores, y en Perl
está desde 1994.

Para el bucle de eventos, el ecosistema tiene **AnyEvent**, **IO::Async** y **Mojo::IOLoop**, con la
misma arquitectura que Tcl y Node: un hilo, una cola, sin bloqueo.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <functional>
#include <iostream>
#include <string>
#include <vector>

int main() {
    int n{};
    if (!(std::cin >> n)) return 1;

    std::string salida;
    std::vector<std::function<void()>> manejadores;

    for (int i = 1; i <= n; ++i) {
        manejadores.emplace_back([i, &salida] {
            if (!salida.empty()) salida += '-';
            salida += std::to_string(i);
        });
    }

    for (const auto& m : manejadores) {
        m();                                  // disparar
    }

    std::cout << "eventos=" << salida << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** `std::vector<std::function<void()>>` es **la lista de
suscriptores**, y este es uno de los pocos sitios donde `std::function` es la elección correcta: **hay
que guardar retrollamadas de tipos distintos en el mismo contenedor**, y para eso el borrado de tipo
es exactamente lo que hace falta (clase 085).

Fíjate en la captura de la lambda: **`[i, &salida]`** captura `i` **por valor** y `salida` **por
referencia**. Y ahí está el peligro central de esta clase en C++:

```cpp
std::function<void()> f;
{
    std::string local = "hola";
    f = [&local] { std::cout << local; };    // captura una REFERENCIA
}
f();                                          // ¡`local` ya no existe!
```

**Una lambda que captura por referencia y sobrevive a lo capturado deja referencias colgantes.** Es el
mismo problema que Ada previene con la comprobación de accesibilidad (clase 115) y que Rust previene
con los tiempos de vida. En C++ **no hay nada que lo detecte**, y es una de las causas más frecuentes
de fallos en código asíncrono.

La regla práctica: **si la retrollamada se guarda, captura por valor**; y si necesita un objeto, un
`shared_ptr` con `weak_ptr` para no impedir su destrucción.

C++ tiene además dos mecanismos de eventos en el ecosistema que merecen nombrarse:

- **Los signals/slots de Qt**, que son el sistema de eventos más usado en C++ de escritorio. Su primera
  versión exigía un preprocesador propio —`moc`— porque el lenguaje no daba lo necesario; hoy
  `connect` acepta lambdas directamente.
- **Boost.Asio**, el modelo de entrada/salida asíncrona que se convirtió en la base de la propuesta
  de red del estándar y que introdujo en C++ el vocabulario de los manejadores de finalización.

Y C++20 trajo las **corrutinas** (clase 122), que resuelven el problema del cierre de esta clase:
escribir código asíncrono con forma secuencial. Con `co_await`, la cadena de retrollamadas desaparece
y el compilador genera la máquina de estados.

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

dcl-pi EVENTOS;
  n int(10) const;
end-pi;

dcl-s i      int(10);
dcl-s salida varchar(200) inz('');

// RPG no tiene retrollamadas: los eventos se procesan en orden
for i = 1 to n;
  if salida <> '';
    salida += '-';
  endif;
  salida += %char(i);
endfor;

dsply ('eventos=' + salida);

*inlr = *on;
return;
```

**Lo que esta clase enseña en RPG.** RPG no tiene retrollamadas idiomáticas, y **IBM i tiene uno de los
modelos de eventos más completos de cualquier plataforma** — en el sistema operativo, no en el
lenguaje.

**Las colas de datos** de la clase 096, ahora en su papel de mecanismo de eventos:

```rpgle
// un trabajo SERVIDOR que espera indefinidamente:
callp recibirDatos('MICOLA' : 'MIBIB' : longitud : datos : -1);
// -1 = esperar sin límite. El trabajo NO consume CPU mientras espera.
```

Un trabajo se bloquea en la cola sin consumir nada, y **el sistema lo despierta cuando llega un
mensaje**. Con varios trabajos esperando en la misma cola, se reparte el trabajo — es un grupo de
consumidores, de los años ochenta.

**Los programas de salida** de la clase 113, que son retrollamadas del sistema operativo:

```text
ADDEXITPGM EXITPNT(QIBM_QZDA_INIT) PGM(MIBIB/MIVALIDA)
```

**Más de cien puntos donde registrar un programa propio**: al conectarse por FTP, al abrir una sesión
ODBC, al validar una contraseña, al arrancar un trabajo. El sistema invoca ese programa y respeta su
respuesta.

**Los disparadores de base de datos**, que son eventos sobre los datos:

```text
ADDPFTRG FILE(CLIENTES) TRGTIME(*AFTER) TRGEVENT(*INSERT) PGM(MIBIB/MITRG)
```

Un programa RPG que el sistema ejecuta **cada vez que alguien inserta una fila**, sea desde RPG, desde
SQL, desde Java o desde una conexión ODBC.

**Y las colas de mensajes**, donde cada trabajo, usuario y dispositivo tiene la suya, y un programa
puede esperar mensajes en ella.

La lección de esta página es la que se repite en toda la Parte 7 con las plataformas de gestión:
**cuando el lenguaje no lo tiene, mira el sistema operativo**. Y a menudo lo que hay ahí es más
robusto —persistente, transaccional, con reparto entre trabajos— que una retrollamada en memoria.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 eventos: procedure options(main);

    declare n fixed binary(31);
    declare i fixed binary(31);
    declare salida char(200) varying initial('');

    get list (n);

    do i = 1 to n;
       if salida ^= '' then salida = salida || '-';
       salida = salida || trim(char(i));
    end;

    put skip list ('eventos=' || salida);

 end eventos;
```

**Lo que esta clase enseña en PL/I.** PL/I **sí puede registrar retrollamadas** con las variables
`entry` de la clase 085, y **no tiene bucle de eventos**: el programa manda.

Lo que sí tiene, y es notable para 1964, es un mecanismo de eventos de otro tipo: **el manejo de
condiciones con `on`** (clase 103), que ya se ha ido nombrando y que aquí encaja de lleno.

```pli
 on endfile(entrada)   eof = '1'b;
 on key(clientes)      call no_encontrado();
 on conversion         call dato_malo();
 on overflow           call desbordamiento();
 on finish             call cerrar_todo();
```

**Cada `on` registra un manejador para un tipo de suceso**, y el sistema lo invoca cuando ocurre. Es
suscripción a eventos con sintaxis declarativa, y con la propiedad de la clase 103: **alcance
dinámico**, así que un manejador establecido arriba cubre todo lo que se llame desde ahí.

Y PL/I tiene además una construcción que casi nadie recuerda y que es programación concurrente por
eventos: **las variables `event` y `wait`**.

```pli
 declare terminado event;
 declare (e(10)) event;

 call procesar(datos) task(t) event(terminado);   /* lanzar en PARALELO */
 wait(terminado);                                  /* esperar a que acabe */
 wait(e) (3);                                       /* esperar a 3 de los 10 */
```

**`call ... task(...) event(...)`** lanza un procedimiento como tarea concurrente y asocia un evento a
su finalización. **`wait`** se bloquea hasta que se complete — y admite esperar a **varios eventos, o a
solo N de ellos**.

Eso es exactamente `Promise.all` y `Promise.race` de JavaScript, y `WaitForMultipleObjects` de Win32.
**En PL/I, en 1964.**

Es una de las capacidades que más justifican la reputación técnica de PL/I: multitarea con eventos y
espera selectiva, en el lenguaje, cuando Fortran no tenía ni `while` y COBOL no tenía `END-IF`.

Su problema fue el de siempre: **casi ningún compilador la implementó por completo**, y la mayoría del
código PL/I en producción nunca la usó.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
EVENTOS ; Orientado a eventos -- clase 119
 read n
 set salida = ""
 for i=1:1:n do manejar(i)
 write "eventos=", salida, !
 quit
 ;
manejar(id) ; el "manejador": M no tiene retrollamadas de primera clase
 if salida '= "" set salida = salida _ "-"
 set salida = salida _ id
 quit
```

**Lo que esta clase enseña en M.** M **no tiene retrollamadas de primera clase**, y lo que hace en su
lugar es lo de siempre: **guardar el nombre de la rutina y llamarla por indirección** (clase 085).

```mumps
 set ^EVENTOS("al_guardar", 1) = "indexar^BUSCA"
 set ^EVENTOS("al_guardar", 2) = "notificar^AVISOS"

 set k = ""
 for  set k = $order(^EVENTOS("al_guardar", k))  quit:k=""  do @^EVENTOS("al_guardar", k)
```

Y aquí está lo característico, que ya apareció en la clase 115: **la lista de suscriptores está en un
*global***. Es decir, **es persistente, compartida entre procesos y modificable sin recompilar**.

Registrar un manejador nuevo es un `set`. Y sobrevive al reinicio.

Eso es exactamente lo que hace **FileMan con los `TRIGGER`** (clase 118): la relación
"cuando cambie este campo, ejecuta esto" **está guardada en el diccionario de datos**, no en el código.

Y M tiene además dos mecanismos de evento propios del lenguaje:

**`job`**, que lanza un proceso en segundo plano:

```mumps
 job procesar^INFORME(id)
```

**Y los eventos asíncronos** del estándar de 1995, poco implementados y notables:

```mumps
 estart                      ; habilitar la atención de eventos
 etrigger "SIGTERM":"cerrar^LIMPIEZA"
```

Con `etrigger` se asocia una rutina a un evento externo —una señal, un mensaje de otro proceso— y el
intérprete la ejecuta entre comandos.

Y las implementaciones modernas van mucho más allá: **InterSystems IRIS tiene *Interoperability***, un
motor de integración con productores, procesos de negocio y operaciones conectados por mensajes, con
reintentos, colas persistentes y trazabilidad completa.

Es un bus de eventos empresarial construido sobre *globals*, y es lo que hace que IRIS se venda hoy
como plataforma de integración sanitaria: **los mensajes HL7 y FHIR entran por ahí**.

Otra vez el patrón de esta parte: **el lenguaje se quedó donde estaba y la plataforma construyó
encima**.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| n salida manejadores |

n := stdin nextLine trimBoth asNumber.

salida := OrderedCollection new.
manejadores := OrderedCollection new.

"suscribir: cada bloque captura su propio i"
1 to: n do: [ :i | manejadores add: [ salida add: i ] ].

"disparar"
manejadores do: [ :cada | cada value ].

Transcript
    show: 'eventos=', ((salida collect: [ :cada | cada printString ])
        inject: '' into: [ :acc :cada |
            acc isEmpty ifTrue: [ cada ] ifFalse: [ acc, '-', cada ] ]);
    cr.
```

**Lo que esta clase enseña en Smalltalk.** Un bloque es un objeto que captura su entorno (clase 083),
así que una lista de bloques **es** una lista de suscriptores. Y `1 to: n do: [ :i | ... ]` **crea una
variable `i` nueva por vuelta**, así que cada bloque captura la suya.

Lo que hace importante a Smalltalk en esta clase es otra cosa: **el patrón Observador y el MVC salieron
de aquí**.

**Modelo-Vista-Controlador** lo formuló **Trygve Reenskaug en Xerox PARC en 1979**, trabajando en
Smalltalk-76, y su implementación se basaba en el mecanismo de dependencias que el sistema traía de
serie:

```smalltalk
modelo addDependent: vista.
modelo changed: #saldo.               "notifica a TODOS los dependientes"
vista update: unAspecto.               "cada dependiente responde"
```

**`addDependent:`, `changed:` y `update:` están en `Object`**, así que **cualquier objeto del sistema
puede ser observado**. No hace falta heredar de nada ni implementar una interfaz.

De ahí salió el patrón Observador del libro de la *Banda de los Cuatro*, y de ahí sale el modelo de
eventos de casi todas las interfaces gráficas posteriores.

Pharo modernizó el mecanismo con **Announcements**, que corrige el problema del original:

```smalltalk
modelo announcer when: SaldoCambiado do: [ :anuncio | vista actualizar: anuncio ].
modelo announcer announce: (SaldoCambiado nuevo: 100).
```

**El evento es un objeto de una clase propia**, no un símbolo, así que **lleva datos y se puede
tipar**. Con `changed:`/`update:`, el receptor tenía que descifrar qué había cambiado a partir de un
símbolo; con `Announcements`, el anuncio trae la información.

Es la misma evolución que en .NET va de `EventHandler` a `EventArgs` tipados, y en JavaScript de los
eventos con cadenas a los `CustomEvent`.

Y hay un detalle que merece cerrar: **el bucle de eventos de Smalltalk está escrito en Smalltalk**. El
proceso de interfaz es un objeto `Process` con su prioridad, la cola de eventos es una
`SharedQueue`, y todo se puede inspeccionar y modificar en marcha. En un sistema donde todo es un
objeto, **el propio bucle de eventos también lo es**.

---

## Y de vuelta a la clase

Lo transferible: **la programación por eventos cambia legibilidad por capacidad de respuesta, y el
precio se paga en el flujo**. Con retrollamadas, la secuencia de lo que ocurre **no está escrita en
ningún sitio**: hay que reconstruirla leyendo quién registra qué. Ese es el *infierno de las
retrollamadas*, y las soluciones —promesas, `async`/`await` (clase 122), corrutinas— existen todas
para lo mismo: **devolver al código la forma secuencial sin perder la asincronía**.

⏮️ [Volver a la clase 119](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
