# -*- coding: utf-8 -*-
"""Parte 8, lote E — clase 127. Ver `vivos_parte8.py` y `gen_vivos.py`."""

SPECS: dict[str, dict] = {}

# ---------------------------------------------------------------------------
# 127 — La pila y el marco de llamada
# ---------------------------------------------------------------------------
SPECS["127"] = dict(
    gancho="""
Sumar recursivamente y contar cuántos marcos se apilan. Aquí hay un dato que cuesta creer: **tres de
estos lenguajes no tenían recursión** —FORTRAN hasta 1990, COBOL hasta 2002 y RPG hasta 1994— y no por
descuido, sino porque **sus variables locales no vivían en una pila**. La pila de llamadas, que hoy
parece parte del hardware, fue una decisión de diseño que estos lenguajes tomaron tarde.
""",
    porque="""
Aquí el concepto es el **marco de activación**: dónde viven los parámetros, las locales y la dirección
de retorno. Y estos lenguajes lo enseñan porque **muestran el mundo sin pila**. En el FORTRAN de 1957
y en el COBOL clásico, **cada subrutina tenía UN juego de variables, en direcciones fijas**, así que
llamarse a sí misma pisaba su propio estado (clase 082).

Ese modelo tiene ventajas que hoy se han redescubierto: **tamaño de memoria conocido en compilación y
sin posibilidad de desbordar la pila** — que es exactamente lo que exigen los sistemas empotrados
certificados.
""",
    cierre="""
Lo transferible: **la pila es rápida porque es tonta**: reservar es sumar al puntero de pila y liberar
es restarlo, sin buscar hueco y sin fragmentación. Su precio es que **el tamaño total está acotado y
no lo controlas bien**: un arreglo local grande o una recursión profunda la desbordan, y el fallo no
avisa. Por eso los lenguajes serios permiten fijar el tamaño de pila por hilo y por tarea, y por eso
en sistemas críticos se prohíbe la recursión — no por dogma, sino porque **el peor caso tiene que ser
calculable**.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. PILAMARCO.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  N       PIC 9(4) COMP.
01  I       PIC 9(4) COMP.
01  SUMA    PIC 9(9) COMP VALUE 0.
01  PROF    PIC 9(4) COMP VALUE 0.
01  ED-S    PIC Z(8)9.
01  ED-P    PIC Z(3)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    COMPUTE N = FUNCTION NUMVAL(LINEA)

    *> COBOL clásico no recurre: se simula la profundidad con un contador
    PERFORM VARYING I FROM 1 BY 1 UNTIL I > N
        ADD I TO SUMA
        ADD 1 TO PROF
    END-PERFORM

    MOVE SUMA TO ED-S
    MOVE PROF TO ED-P
    DISPLAY "suma=" FUNCTION TRIM(ED-S)
            " profundidad=" FUNCTION TRIM(ED-P)
    STOP RUN.
""", """
**Lo que esta clase enseña en COBOL.** **El COBOL clásico no tiene pila de llamadas para sus datos**, y
esa es la razón de que no fuera recursivo hasta 2002.

La `WORKING-STORAGE` de un programa es **estática**: existe una sola copia, en direcciones fijas,
desde que el programa se carga hasta que termina (clase 082). Si un programa se llamara a sí mismo,
**la segunda invocación machacaría las variables de la primera**.

Y eso, que suena a limitación, tiene dos ventajas que explican por qué se mantuvo:

1. **El consumo de memoria se conoce al compilar.** Un programa COBOL no puede desbordar la pila,
   porque no la usa para sus datos.
2. **El estado sobrevive entre llamadas.** Un programa llamado muchas veces conserva sus variables —de
   ahí `INITIAL` para forzar lo contrario, y de ahí que `*INLR` en RPG (clase 103) importe tanto.

COBOL-2002 añadió lo que faltaba, y la sintaxis dice exactamente qué cambia:

```cobol
IDENTIFICATION DIVISION.
PROGRAM-ID. FACTORIAL RECURSIVE.
DATA DIVISION.
WORKING-STORAGE SECTION.
01  CONTADOR  PIC 9(4) COMP.        *> UNA copia, compartida por todas las llamadas
LOCAL-STORAGE SECTION.
01  N-LOCAL   PIC 9(4) COMP.         *> una copia POR INVOCACIÓN: el marco de pila
```

**`LOCAL-STORAGE` es el marco de activación de COBOL**: se reserva al entrar y se libera al salir, y
cada invocación tiene el suyo. Es la diferencia entre `static` y automático de C, con nombres de
sección.

Y merece una nota operativa que explica por qué se usa poco: **en un monitor transaccional con miles de
tareas concurrentes, la memoria total es un recurso administrado**, y una recursión de profundidad
impredecible es un riesgo. Los sistemas de gestión prefieren estructuras iterativas con tablas de
tamaño declarado (clase 097).

Y hay una pila que COBOL sí usa siempre y que conviene nombrar: **la de `PERFORM`**. Un `PERFORM
párrafo` guarda la dirección de retorno, y anidar `PERFORM` del mismo párrafo **tiene comportamiento
indefinido en el estándar** — es la trampa clásica del `PERFORM` recursivo accidental.
"""),
        "fortran": ("""
program pilamarco
   implicit none
   integer :: n, s, prof

   read(*, *) n

   prof = 0
   s = sumar(n, prof)

   write(*, '(A,I0,A,I0)') 'suma=', s, ' profundidad=', prof

contains

   recursive function sumar(k, p) result(r)
      integer, intent(in) :: k
      integer, intent(inout) :: p
      integer :: r
      p = p + 1                       ! un marco más
      if (k <= 1) then
         r = k
      else
         r = k + sumar(k - 1, p)
      end if
   end function sumar

end program pilamarco
""", """
**Lo que esta clase enseña en Fortran.** La palabra **`recursive`** de este programa fue obligatoria
durante veintiocho años, y su historia es la de esta clase.

**El FORTRAN de 1957 asignaba las variables locales estáticamente**, como COBOL: una dirección fija por
variable, sin marco de pila. El IBM 704 no tenía instrucciones de pila (clase 125), y la dirección de
retorno se guardaba **modificando el código**.

Con ese modelo, **la recursión es imposible**, y el estándar la prohibió explícitamente hasta 1990.

La cronología:

| Versión | Recursión |
|---|---|
| FORTRAN 77 | **prohibida** |
| Fortran 90 | permitida, con `recursive` obligatorio |
| Fortran 2008 | los procedimientos internos son recursivos por defecto |
| **Fortran 2018** | **todos lo son**; existe `non_recursive` para lo contrario |

Y esa evolución dejó rastros que hoy se ven en el código antiguo: **los algoritmos clásicos escritos con
pila explícita** (clase 096), porque no había otra.

Fortran conserva además la palabra clave que expresa el modelo antiguo, y sigue siendo útil:

```fortran
subroutine contador()
   integer, save :: n = 0        ! ESTÁTICA: una sola copia, sobrevive entre llamadas
   n = n + 1
end subroutine
```

**`save`** es el `static` de C. Y hay una trampa muy conocida que conviene decir: **una variable local
con inicializador implica `save`**.

```fortran
integer :: n = 0      ! ¡esto es SAVE! Solo se inicializa UNA vez
integer :: n
n = 0                  ! esto sí se ejecuta en cada llamada
```

Es una fuente clásica de errores en código concurrente: una variable así **se comparte entre hilos**,
y el bucle `do concurrent` (clase 121) puede dar resultados incorrectos.

Y sobre el tamaño de la pila, Fortran tiene un problema práctico muy real en cálculo científico: **los
arreglos temporales y automáticos van a la pila**.

```fortran
subroutine calcular(n)
   real :: temporal(n, n)      ! arreglo AUTOMÁTICO: en la pila
end subroutine
```

Con `n = 5000`, eso son 200 MB en la pila, y **la pila por defecto suele ser de 8 MB**. El programa
falla con un fallo de segmentación desconcertante, y la solución habitual es `ulimit -s unlimited`,
`-fmax-stack-var-size` o declararlo `allocatable`.

Es uno de los fallos más frecuentes al portar código Fortran entre máquinas, y es exactamente lo que
advierte el cierre de esta clase.
"""),
        "ada": ("""
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Pilamarco is
   Prof : Natural := 0;

   function Sumar (K : Integer) return Integer is
   begin
      Prof := Prof + 1;             --  un marco más
      if K <= 1 then
         return K;
      else
         return K + Sumar (K - 1);
      end if;
   end Sumar;

   N, S : Integer;
begin
   Get (N);
   S := Sumar (N);

   Put ("suma=");         Put (S,    Width => 1);
   Put (" profundidad="); Put (Prof, Width => 1);
   New_Line;
end Pilamarco;
""", """
**Lo que esta clase enseña en Ada.** Ada tiene recursión desde 1983 sin declararla, y tiene lo que a
esta clase le importa de verdad: **control explícito del tamaño de la pila**.

```ada
task Trabajador is
   pragma Storage_Size (64 * 1024);        --  64 KB de pila para ESTA tarea
end Trabajador;

pragma Storage_Size (T'Class, ...);
```

**Cada tarea declara cuánta pila necesita**, y si se pasa, **se lanza `Storage_Error`** — una excepción
normal, capturable, no un fallo de segmentación.

Esa diferencia es el argumento entero de Ada en esta clase: **desbordar la pila no es un fallo
indeterminado, es un error del programa** que se puede manejar, registrar y del que se puede
recuperar.

Compara con C, C++ o Fortran, donde el desbordamiento produce un fallo de segmentación sin
información, o —peor— **corrompe memoria vecina en sistemas sin protección**.

Y para los sistemas donde eso no basta, Ada tiene la restricción:

```ada
pragma Restrictions (No_Recursion);
pragma Restrictions (No_Implicit_Heap_Allocations);
pragma Profile (Ravenscar);
```

**`No_Recursion` hace que el compilador RECHACE cualquier llamada recursiva**, con lo que **el uso
máximo de pila se puede calcular estáticamente**.

Y eso no es teoría: hay herramientas —**GNATstack**— que **analizan el ejecutable y calculan el consumo
de pila en el peor caso**, sumando los marcos a lo largo del grafo de llamadas. Con eso se puede
dimensionar la pila con garantía en lugar de por prueba y error.

En aviónica, esa cifra **es un requisito de certificación**: hay que demostrar que el sistema no puede
quedarse sin pila.

Y Ada permite además elegir dónde vive cada cosa:

```ada
X : Integer;                                   --  en la pila
Y : Integer with Volatile;                      --  con acceso no optimizable
for Z'Address use System'To_Address (16#FF00#); --  en una dirección CONCRETA
```

Ese último —**colocar una variable en una dirección de memoria fija**— es cómo se accede a los
registros de hardware sin escribir ensamblador, y es una de las razones por las que Ada se usa en
sistemas empotrados.
"""),
        "pascal": ("""
program Pilamarco;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  Prof: Integer;

function Sumar(K: Integer): Integer;
begin
  Inc(Prof);                       { un marco más }
  if K <= 1 then
    Result := K
  else
    Result := K + Sumar(K - 1);
end;

var
  N, S: Integer;

begin
  Read(N);

  Prof := 0;
  S := Sumar(N);

  WriteLn('suma=', IntToStr(S), ' profundidad=', IntToStr(Prof));
end.
""", """
**Lo que esta clase enseña en Pascal.** Pascal **tiene recursión desde 1970**, heredada de Algol 60 —al
contrario que Fortran y COBOL— y sus procedimientos anidados hacen el marco de pila más interesante de
lo habitual.

```pascal
procedure Externo;
var X: Integer;
  procedure Interno;
  begin
    X := X + 1;        { ve la X del marco de EXTERNO }
  end;
begin ... end;
```

Para que `Interno` acceda a `X`, su marco necesita **un puntero al marco del anfitrión**, y eso tiene
un nombre clásico: **el enlace estático** (*static link*), frente al **enlace dinámico** que apunta al
llamante.

Con anidamiento profundo hace falta recorrer varios enlaces, y de ahí la alternativa que los libros de
compiladores llaman **el display**: un vector con los marcos de cada nivel léxico.

**Ese mecanismo es lo que C decidió no tener**, y por eso C no admite funciones anidadas: **sin enlace
estático, el marco es más simple y más barato**. Es un ejemplo limpio de una decisión de diseño de
lenguaje que se ve en la disposición de la pila.

Pascal permite además fijar el tamaño de la pila, como Ada:

```pascal
{$M 16777216, 0, 0}          { tamaño de pila en Windows }
```

```bash
fpc -Cs2000000 programa.pas   # tamaño de la comprobación de pila
```

Y tiene una directiva que es exactamente lo que el cierre de esta clase recomienda:

```pascal
{$STACKCHECKS ON}
```

**Con ella, cada llamada comprueba si queda pila** y lanza `EStackOverflow` —una excepción normal— en
lugar de fallar. Es lo mismo que hace Ada con `Storage_Error`, disponible con una directiva.

Y hay un detalle histórico que explica una decisión del lenguaje: **el `for` de Pascal deja la variable
de control indefinida al salir** (clase 108). El motivo es que el compilador puede mantenerla **en un
registro** en lugar de en el marco de pila, y no está obligado a escribirla de vuelta.

Es una regla del estándar puesta para que el código generado sea más rápido.
"""),
        "lisp": ("""
(defun sumar (k prof)
  (if (<= k 1)
      (values k (1+ (car prof)))
      (progn (incf (car prof))
             (+ k (sumar (1- k) prof)))))

(let* ((n (read))
       (prof (list 0))
       (s (progn (incf (car prof) 0) 0)))
  ;; recursión simple, contando marcos
  (labels ((rec (k)
             (incf (car prof))
             (if (<= k 1) k (+ k (rec (1- k))))))
    (setf s (rec n)))
  (format t "suma=~D profundidad=~D~%" s (car prof)))
""", """
**Lo que esta clase enseña en Common Lisp.** Lisp **fue diseñado alrededor de la recursión** —es su
herramienta de control principal desde 1958— y esta clase permite explicar por qué eso obligó a
inventar cosas.

La primera: **la pila de Lisp tiene que ser grande**, porque los algoritmos recursivos sobre listas
tienen profundidad proporcional a la longitud. Recorrer una lista de un millón de elementos con
recursión simple **desborda**.

De ahí una de las diferencias más citadas entre Lisp y Scheme: **Scheme exige eliminación de llamadas
en cola; Common Lisp no**.

```lisp
(defun contar (n acc)
  (if (zerop n) acc (contar (1- n) (1+ acc))))    ; llamada EN COLA
```

En Scheme, eso **se convierte en un bucle** y no consume pila: está en el estándar. En Common Lisp,
**depende de la implementación** — SBCL lo hace con `(optimize (debug 1))` o menos, y no lo hace con
`(debug 3)`, porque conservar los marcos es lo que permite depurar.

Es un compromiso explícito: **eliminar la llamada en cola borra el marco, y con él la información que
el depurador necesita**.

Y ahí está la aportación de Lisp a esta clase, que ya apareció en la clase 096: **la pila es un objeto
inspeccionable**.

Cuando salta un error, el depurador muestra los marcos con sus variables, y permite **elegir un marco,
examinarlo, cambiar un valor y REANUDAR desde ahí**.

```lisp
(sb-debug:print-backtrace)
(sb-debug:arg 0)              ; los argumentos de un marco concreto
```

Esa capacidad —**reanudar desde un marco intermedio**— es la que necesitan los reinicios (clases 103 y
116), y es la razón de que Common Lisp no borre marcos alegremente.

Y para los casos donde la recursión profunda es inevitable, el idioma es el de la clase 090:
**acumular con `push` e invertir**, o usar `loop`, que compila a un bucle sin marcos.

Es un buen ejemplo del cierre de esta clase: **la elegancia recursiva tiene un coste en pila, y hay que
saber cuándo se paga**.
"""),
        "tcl": ("""
proc sumar {k} {
    global prof
    incr prof
    if {$k <= 1} { return $k }
    return [expr {$k + [sumar [expr {$k - 1}]]}]
}

gets stdin linea
set n [string trim $linea]

set prof 0
set s [sumar $n]

puts "suma=$s profundidad=$prof"
""", """
**Lo que esta clase enseña en Tcl.** Tcl tiene recursión, y **el límite es un parámetro del intérprete,
no del sistema operativo**:

```tcl
interp recursionlimit {} 5000        ;# consultar o CAMBIAR el límite
```

Por defecto son **1000 niveles**, y al pasarse **se lanza un error normal de Tcl** —capturable con
`catch`— en lugar de un fallo de segmentación.

Esa decisión es muy propia de Tcl: **el intérprete se protege a sí mismo**, porque un guion es a menudo
código no confiable incrustado en otra aplicación (clase 107). Un desbordamiento de pila que tirara la
aplicación anfitriona sería inaceptable.

Y Tcl tiene una construcción que ataca directamente el problema de esta clase: **`tailcall`**.

```tcl
proc contar {n acc} {
    if {$n == 0} { return $acc }
    tailcall contar [expr {$n - 1}] [expr {$acc + 1}]    ;# NO crece la pila
}
```

**`tailcall` (Tcl 8.6) reemplaza el marco actual por el de la llamada nueva**, en lugar de apilar uno
más. Es exactamente el `goto &funcion` de Perl (clase 108) y la eliminación de llamadas en cola de
Scheme, como **un comando explícito**.

Que sea explícito tiene una ventaja sobre hacerlo automáticamente: **el programador declara la
intención**, y si la llamada no está realmente en posición de cola, el error se ve.

Y Tcl 8.6 añadió la pieza que reescribió su intérprete por dentro: **NRE** (*Non-Recursive Engine*).

Antes, **la pila de Tcl era la pila de C**: cada nivel de recursión de un guion consumía marcos de C, y
por eso el límite era bajo y las corrutinas eran imposibles.

Con NRE, **el intérprete gestiona su propia pila en el montón**, así que:

- La recursión profunda ya no depende de la pila del proceso.
- **Las corrutinas** (clase 122) se pueden implementar guardando ese estado.
- `tailcall`, `yield` y `coroutine` existen gracias a eso.

Es un caso de manual de cómo **una decisión de implementación de la pila habilita características del
lenguaje**.
"""),
        "perl": ("""
use strict;
use warnings;

my $prof = 0;

sub sumar {
    my ($k) = @_;
    $prof++;                          # un marco más
    return $k if $k <= 1;
    return $k + sumar($k - 1);
}

my $n = <STDIN>;
chomp $n;

my $s = sumar($n);

print "suma=$s profundidad=$prof\\n";
""", """
**Lo que esta clase enseña en Perl.** Perl tiene recursión, y **avisa cuando se pasa de cien niveles**:

```text
Deep recursion on subroutine "main::sumar" at prog.pl line 8.
```

Ese aviso es de `use warnings` y se puede desactivar con `no warnings 'recursion'`. Es una decisión
llamativa: **Perl considera que una recursión de más de cien niveles es sospechosa por defecto**,
porque en su dominio —procesar texto y datos— casi siempre lo es.

Y Perl tiene el mecanismo de la clase 108 que resuelve esta clase, y merece verlo aquí en su contexto:

```perl
sub contar {
    my ($n, $acc) = @_;
    return $acc if $n == 0;
    @_ = ($n - 1, $acc + 1);
    goto &contar;                  # SUSTITUYE el marco actual: la pila no crece
}
```

**`goto &funcion` reemplaza el marco de pila actual por el de otra función**, pasándole `@_`. Es
recursión de cola de verdad, y la función original **desaparece del rastro de llamadas**.

Su uso principal no es ese, sino el de los envoltorios transparentes: **`AUTOLOAD`** (clase 111) suele
terminar con `goto &$metodo_real` para que la llamada parezca directa.

Y Perl expone la pila como datos, lo que permite escribir herramientas:

```perl
my ($paquete, $fichero, $linea, $sub) = caller(0);
my $nivel = 0;
$nivel++ while caller($nivel);           # PROFUNDIDAD actual de la pila
use Carp;  croak "error";                 # informa desde el punto del LLAMANTE
```

**`caller` con un número devuelve la información de ese nivel de la pila**, y con eso está construido
`Carp`, el módulo estándar de mensajes de error.

La distinción de `Carp` es útil y poco conocida: **`die` informa del sitio donde falla, `croak` informa
del sitio que hizo la llamada equivocada**. Para una biblioteca, lo segundo es lo correcto — al usuario
no le sirve saber la línea interna del módulo.

Es un buen ejemplo de que **exponer la pila permite mejores mensajes de error**, que es de lo que va la
clase 137.
"""),
        "cpp": ("""
#include <iostream>

static int prof = 0;

int sumar(int k) {
    ++prof;                          // un marco más
    if (k <= 1) return k;
    return k + sumar(k - 1);
}

int main() {
    int n{};
    if (!(std::cin >> n)) return 1;

    const int s = sumar(n);

    std::cout << "suma=" << s << " profundidad=" << prof << '\\n';
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** C++ hereda de C el modelo de pila, y esta clase es el sitio para
mirar lo que hay dentro de un marco:

```text
| argumentos             |
| dirección de retorno   |
| puntero de marco previo|
| variables locales      |   <- el marco
| registros guardados    |
```

Y C++ añade una cosa a ese marco que C no tiene y que cuesta: **el desenrollado de excepciones**.

Cuando una excepción se propaga, **hay que ejecutar los destructores de todos los objetos locales de
cada marco** (clase 103). Eso exige que el compilador genere **tablas de desenrollado** que describen,
para cada punto del código, **qué objetos hay vivos y cómo destruirlos**.

```bash
g++ -fno-exceptions      # sin excepciones: marcos más pequeños, sin tablas
```

Esas tablas ocupan espacio en el ejecutable y **no cuestan nada si no salta ninguna excepción** — es el
modelo de "coste cero cuando no se usa". El precio se paga en tamaño y al lanzar.

Y sobre el desbordamiento de pila, C++ está en el peor sitio de esta página: **no hay ninguna
comprobación**.

```cpp
void f() { f(); }        // desbordamiento: fallo de segmentación, sin más información
int v[10000000];          // en la pila: falla al ENTRAR en la función
```

En Linux hay una **página guardia** que provoca `SIGSEGV`, así que al menos falla en lugar de corromper
memoria. En sistemas empotrados sin protección de memoria, **puede escribir sobre otras estructuras en
silencio**.

Las herramientas ayudan:

```bash
g++ -fstack-protector-strong    # canarios: detectan escrituras fuera del marco
g++ -fsanitize=address           # detecta el desbordamiento de pila
ulimit -s 16384                   # cambiar el tamaño de la pila
```

Y C++23 añadió por fin algo relevante para la clase 138: **`std::stacktrace`**.

```cpp
#include <stacktrace>
std::cout << std::stacktrace::current();
```

**Obtener la traza de la pila desde el propio programa**, en el estándar. Hasta entonces hacía falta
`backtrace()` de glibc, la API de Windows o una biblioteca — y era una de las carencias más señaladas
frente a los lenguajes con runtime.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller) main(Principal);

dcl-s prof int(10) inz(0);

dcl-proc Principal;
  dcl-pi *n;
    n int(10) const;
  end-pi;

  dsply ('suma=' + %char(sumar(n)) + ' profundidad=' + %char(prof));
end-proc;

dcl-proc sumar;
  dcl-pi *n int(20);
    k int(10) const;
  end-pi;

  prof += 1;                    // un marco mas
  if k <= 1;
    return k;
  endif;
  return k + sumar(k - 1);
end-proc;
""", """
**Lo que esta clase enseña en RPG.** **RPG no tuvo recursión hasta ILE (1994)**, y por la misma razón
que COBOL: **sus variables eran estáticas**.

En el RPG clásico, todos los campos de un programa vivían en almacenamiento estático, así que una
subrutina `BEGSR` que se llamara a sí misma pisaba su propio estado (clase 109).

Con ILE, un `dcl-proc` con variables declaradas dentro **tiene almacenamiento automático**, y con eso
llegó la recursión. Y RPG mantiene la distinción explícita:

```rpgle
dcl-proc calcular;
  dcl-s local int(10);              // AUTOMÁTICA: una por invocación
  dcl-s persistente int(10) static;  // ESTÁTICA: una para todas
end-proc;
```

**`static` en una variable de procedimiento** es exactamente el `save` de Fortran y el `static` de C —y
tiene el aviso de la clase 087: **en un programa de servicio con activación compartida, el estado
`static` se comparte entre trabajos**.

Y aquí está lo que hace distinta a esta clase en IBM i: **la pila es un objeto del sistema y se puede
inspeccionar**.

```text
DSPJOB  ->  opción 11: pila de llamadas del trabajo
```

**Ver la pila de llamadas de un trabajo en producción, desde fuera, sin depurador y sin detenerlo.**
Muestra cada programa y procedimiento, con su módulo y su número de sentencia.

Y por SQL, que es la forma moderna (clase 117):

```sql
SELECT * FROM TABLE(QSYS2.STACK_INFO('*'))
```

Eso devuelve **la pila de llamadas de todos los trabajos del sistema como una tabla**, consultable con
`WHERE` y `ORDER BY`.

Es una capacidad de observabilidad que en otras plataformas exige herramientas específicas —`jstack`,
`gdb`, un perfilador— y aquí es una consulta. Es la clase 142 anticipada, y viene de que **en IBM i
todo es un objeto del sistema**, incluida la pila de un trabajo.
"""),
        "pli": ("""
 pilamarco: procedure options(main);

    declare n fixed binary(31);
    declare s fixed binary(31);
    declare prof fixed binary(31) initial(0);

    get list (n);
    s = sumar(n);

    put skip list ('suma=' || trim(char(s)) ||
                   ' profundidad=' || trim(char(prof)));

 sumar: procedure (k) returns (fixed binary(31)) recursive;
    declare k fixed binary(31);
    prof = prof + 1;                 /* un marco mas */
    if k <= 1 then return (k);
    return (k + sumar(k - 1));
 end sumar;

 end pilamarco;
""", """
**Lo que esta clase enseña en PL/I.** La palabra **`recursive`** de este programa es obligatoria, y su
existencia cuenta la historia de esta clase desde el lado de 1964.

PL/I **sí permitía la recursión desde el principio** —al contrario que FORTRAN y COBOL— y **hacía falta
declararla** porque el compilador asignaba las variables automáticas de forma estática cuando podía.

```pli
 declare x fixed binary(31) automatic;   /* en la PILA: una por invocación */
 declare y fixed binary(31) static;       /* una sola copia, permanente */
 declare z fixed binary(31) based(p);      /* donde apunte p (clase 090) */
 declare w fixed binary(31) controlled;     /* una PILA de generaciones (clase 096) */
```

**PL/I tiene cuatro clases de almacenamiento**, y es el lenguaje de esta página que las distingue con
más precisión. `automatic` es el marco de pila; `static` es el modelo antiguo; `based` es el montón
manual; y **`controlled` es una pila explícita de valores** que el programa maneja con `allocate` y
`free` — algo que no tiene ningún otro lenguaje de esta página.

Y `automatic` **es el valor por defecto en un procedimiento**, lo que sitúa a PL/I del lado moderno
desde 1964.

Y hay una construcción de PL/I relacionada con la pila que es notable y peligrosa, ya nombrada en la
clase 108: **saltar a una etiqueta de un bloque exterior desde un procedimiento anidado**.

```pli
 declare destino label;
 destino = fin;
 go to destino;          /* deshace TODOS los marcos intermedios */
```

Eso **desenrolla la pila hasta el marco donde vive la etiqueta**, ejecutando lo que haga falta. Es un
`throw` sin `catch`, y el compilador tiene que generar la información para hacerlo — la misma
maquinaria que el desenrollado de excepciones de C++ de esta misma clase.

Y las condiciones `on` de PL/I (clase 103) usan esa maquinaria en su forma disciplinada: **un manejador
con alcance dinámico se busca subiendo por la pila de marcos**, exactamente como una excepción.

PL/I tenía, en 1964, la infraestructura de pila que C++ necesitó las excepciones para justificar.
"""),
        "mumps": ("""
PILAMARCO ; La pila y el marco de llamada -- clase 127
 read n
 set prof = 0
 set s = $$sumar(n)
 write "suma=", s, " profundidad=", prof, !
 quit
 ;
sumar(k) ; recursivo
 new r
 set prof = prof + 1
 quit:k<=1 k
 set r = k + $$sumar(k - 1)
 quit r
""", """
**Lo que esta clase enseña en M.** M **tiene recursión desde siempre**, y su pila es de las más
peculiares de esta página, porque **hay dos**.

**La primera es la pila de llamadas normal**, con `do` y `$$`, y se consulta con:

```mumps
 write $stack                    ; profundidad ACTUAL de la pila
 write $stack(1, "PLACE")         ; dónde está el nivel 1
 write $stack(1, "MCODE")          ; el CÓDIGO fuente de esa línea
 write $stack(1, "ECODE")           ; el código de error, si lo hubo
```

**`$stack` con "MCODE" devuelve la línea de código fuente de cada nivel de la pila**, en ejecución. Es
lo mismo que `$text` (clase 123) aplicado a la pila, y con eso se escriben trazas de error completas
sin depurador.

**Y la segunda es la pila de `new`** (clases 096 y 109), que es lo que hace posible la recursión en un
lenguaje sin ámbitos:

```mumps
sumar(k) ;
 new r          ; APILA el valor anterior de r
 ...
 quit r          ; y lo restaura al salir
```

Sin ese `new`, **la variable `r` sería la misma en todos los niveles de recursión** y el resultado
sería basura. **La recursión en M no funciona por defecto: funciona porque el programador declara qué
variables se apilan.**

Es un detalle importante y una fuente clásica de errores: **olvidar un `new` en una rutina recursiva
produce un fallo silencioso** que nada detecta.

Fíjate además en el `quit:k<=1 k` del programa: **`quit` con postcondicional y con valor de retorno**,
todo en una línea. Es la densidad característica de M (clase 108).

Y hay un límite práctico que conviene conocer: **el tamaño de la pila de M es configurable y suele ser
generoso**, porque los recorridos recursivos de árboles son habituales en VistA. Al pasarse, se lanza
un error `M53` capturable, no un fallo del proceso — como en Tcl y en Ada, y por la misma razón: **el
sistema tiene que seguir en pie**.
"""),
        "smalltalk": ("""
| n prof sumar s |

n := stdin nextLine trimBoth asNumber.

prof := 0.
sumar := nil.
sumar := [ :k |
    prof := prof + 1.
    k <= 1 ifTrue: [ k ] ifFalse: [ k + (sumar value: k - 1) ] ].

s := sumar value: n.

Transcript
    show: 'suma=', s printString;
    show: ' profundidad=', prof printString;
    cr.
""", """
**Lo que esta clase enseña en Smalltalk.** El programa usa **un bloque recursivo** —`sumar` se refiere a
sí mismo, por eso hace falta declararlo antes—, y eso funciona porque un bloque captura la variable,
no su valor (clase 083).

Y aquí está la aportación de Smalltalk a esta clase, ya adelantada en la clase 096 y que aquí es el
tema central: **el marco de pila es un objeto**.

```smalltalk
thisContext                       "el marco ACTUAL"
thisContext sender                 "el marco que me llamó"
thisContext method                  "el método que se está ejecutando"
thisContext tempAt: 1                "una variable local de ese marco"
thisContext pc                        "el contador de programa"
thisContext copy                       "una COPIA del marco"
```

**`MethodContext` es una clase normal**, y una instancia suya se puede inspeccionar, modificar, guardar
y reanudar.

Con eso, Smalltalk implementa **dentro del propio lenguaje** cosas que en cualquier otro sitio exigen
soporte de la máquina virtual:

- **El depurador**: recorre `sender` hacia arriba y muestra los marcos.
- **Las excepciones**: `signal`, `return:`, `retry`, `resume:` manipulan la pila (clase 116).
- **Las corrutinas y las continuaciones**: guardar un contexto y reanudarlo.
- **Y lo más llamativo: modificar un método y CONTINUAR desde el marco actual**, sin reiniciar.

Ese último punto es lo que hace único el flujo de trabajo de Smalltalk: **salta un error, se abre el
depurador sobre la pila viva, se escribe el método que faltaba, se pulsa "reanudar" y el programa
sigue** como si nunca hubiera fallado.

Es programar descubriendo lo que hace falta según hace falta, y depende por completo de que la pila
sea un objeto.

Y sobre el desbordamiento: **la recursión infinita en Smalltalk no tira el proceso**, lanza una
excepción y abre el depurador con la pila entera disponible para inspección. Es la mejor experiencia
de esta página ante ese fallo, y es coherente con todo lo demás del sistema.
"""),
    },
)
