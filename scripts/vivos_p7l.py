# -*- coding: utf-8 -*-
"""Parte 7, lote L — clase 118. Ver `vivos_parte7.py` y `gen_vivos.py`."""

SPECS: dict[str, dict] = {}

# ---------------------------------------------------------------------------
# 118 — Lógico: reglas, hechos y unificación
# ---------------------------------------------------------------------------
SPECS["118"] = dict(
    gancho="""
¿Divide `a` a `b`? En Prolog eso se escribe como **una regla**, y el motor la usa en las dos
direcciones: puede comprobarla y puede **buscar todos los divisores**. Ninguno de estos doce lenguajes
es lógico, y tres tienen una conexión histórica directa con Prolog: **Lisp, donde se inventaron sus
antecesores; C++, cuyas plantillas resultaron ser un motor lógico por accidente; y COBOL, que en 1965
tuvo tablas de decisión**.
""",
    porque="""
Aquí el concepto es la **relación en lugar de la función**: declarar hechos y reglas, y dejar que un
motor busque. Estos lenguajes lo enseñan por dos vías. La histórica: **Prolog (Colmerauer y Kowalski,
1972) salió de la tradición de Lisp** —Planner y Conniver, escritos en Lisp— y los primeros
intérpretes de Prolog **se escribieron en Lisp**.

Y la práctica: **el paradigma lógico sí está en producción, con otro nombre**. Los motores de reglas
de negocio, las restricciones de integridad de una base de datos, los sistemas de tipos con inferencia
y `SELECT` con varios `JOIN` son todos programación lógica.
""",
    cierre="""
Lo transferible: **la programación lógica sirve cuando la relación importa más que la dirección**. Una
función va de entradas a salidas; una regla dice **qué es cierto**, y el motor la recorre hacia donde
haga falta. Por eso los sistemas de tipos, los planificadores y los verificadores son lógicos: no
calculan un resultado, **buscan una asignación que satisfaga las restricciones**. Cuando te descubras
escribiendo el mismo `if` en cuatro sitios distintos, la pregunta útil es si eso es una regla que
debería estar declarada una vez.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. LOGICO.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  T1      PIC X(20).
01  T2      PIC X(20).
01  A       PIC S9(9) COMP-3.
01  B       PIC S9(9) COMP-3.
01  RESULT  PIC X(5).

PROCEDURE DIVISION.
    ACCEPT LINEA
    UNSTRING LINEA DELIMITED BY ALL SPACES INTO T1 T2
    COMPUTE A = FUNCTION NUMVAL(T1)
    COMPUTE B = FUNCTION NUMVAL(T2)

    IF FUNCTION MOD(B, A) = 0
        MOVE "true"  TO RESULT
    ELSE
        MOVE "false" TO RESULT
    END-IF

    DISPLAY "divisor=" FUNCTION TRIM(RESULT)
    STOP RUN.
""", """
**Lo que esta clase enseña en COBOL.** COBOL no es lógico, y tiene una conexión histórica con este
paradigma que casi nadie recuerda: **las tablas de decisión**.

A mediados de los sesenta, el mismo comité que estandarizaba COBOL —CODASYL— trabajó en **DETAB/65**,
una extensión que permitía escribir la lógica de negocio como **una tabla de condiciones y acciones**:

```text
              R1   R2   R3   R4
CONDICIONES
  Saldo > 0    S    S    N    N
  Cliente VIP  S    N    S    N
ACCIONES
  Aprobar      X    X    -    -
  Revisar      -    -    X    -
  Rechazar     -    -    -    X
```

Eso **no es un programa: es una especificación**. Cada columna es una regla, y un preprocesador
generaba el COBOL correspondiente. La ventaja que se buscaba era concreta: **una tabla se puede
comprobar por completitud y por contradicción** —¿hay alguna combinación de condiciones sin acción?
¿alguna con dos?— cosa que una cadena de `IF` anidados no permite.

DETAB no llegó al estándar y la idea sobrevivió: los generadores de tablas de decisión fueron
herramientas comerciales durante décadas, y **el concepto es exactamente el de un motor de reglas de
negocio moderno** — Drools, la lógica de decisión de un ERP, las tablas de un sistema de tarificación
de seguros.

Y ahí es donde COBOL se encuentra hoy con la programación lógica: **los sistemas de reglas escritos
encima**. Un núcleo de pólizas o de tarifas rara vez tiene las reglas en el código COBOL; las tiene en
tablas de base de datos que un intérprete recorre, precisamente para poder cambiarlas sin recompilar.

Y dentro del lenguaje, la construcción más cercana a declarar una regla es el **nivel 88** de la clase
092:

```cobol
88  APROBABLE  VALUE "A" THRU "C".
88  CLIENTE-VIP VALUE "V".
IF APROBABLE AND CLIENTE-VIP ...
```

Un nombre para una condición, declarado junto al dato y usado en muchos sitios. Es un hecho, no una
regla con variables — y es lo que más se le parece.
"""),
        "fortran": ("""
program logico
   implicit none
   integer :: a, b

   read(*, *) a, b

   if (mod(b, a) == 0) then
      write(*, '(A)') 'divisor=true'
   else
      write(*, '(A)') 'divisor=false'
   end if
end program logico
""", """
**Lo que esta clase enseña en Fortran.** Fortran no tiene nada lógico, y merece decirlo sin adornos:
**es el lenguaje de esta página más lejos del paradigma**. Su modelo es calcular, no buscar.

Lo que sí tiene, y conecta de lejos, son los **operadores lógicos como valores** y las máscaras de la
clase 117:

```fortran
logical :: divisores(100)
divisores = mod(b, [(i, i = 1, 100)]) == 0     ! TODOS los divisores, de golpe
count(divisores)                                 ! cuántos hay
pack([(i, i = 1, 100)], divisores)                ! cuáles son
```

Esa última línea **devuelve la lista de todos los divisores de `b`**, que es justo lo que un Prolog
haría con retroceso. La diferencia es fundamental y merece verse: **Fortran lo calcula todo y luego
filtra; Prolog busca y se detiene cuando encuentra**.

Para el caso de "¿existe alguno?", `any(...)` cortocircuita conceptualmente y en la práctica el
compilador evalúa el arreglo entero. Para cien elementos da igual; para un espacio de búsqueda
combinatorio, la diferencia es entre terminar y no terminar.

Y donde Fortran sí se cruza con la programación lógica es en un sitio inesperado: **la programación
con restricciones aplicada al cálculo numérico**.

Los problemas de optimización con restricciones —programación lineal, entera, no lineal— son
formalmente lo mismo que un problema lógico: **encontrar valores que satisfagan un conjunto de
condiciones**. Y las bibliotecas que los resuelven, las que están detrás de la planificación de
producción y las rutas de reparto, **están escritas en Fortran y en C**: MINOS, SNOPT, IPOPT, las
rutinas de HSL.

```fortran
call snopta(..., f, g, ...)      ! minimizar f sujeto a restricciones
```

Es programación declarativa por restricciones con un motor de búsqueda muy sofisticado detrás —el
método símplex, puntos interiores, ramificación y acotación— y es el mismo tipo de motor que hay bajo
un solucionador SAT o un Prolog con restricciones.

**El paradigma lógico y la optimización numérica son primos**, y Fortran está en el segundo desde
siempre.
"""),
        "ada": ("""
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Logico is
   A, B : Integer;
begin
   Get (A);
   Get (B);

   if B mod A = 0 then
      Put_Line ("divisor=true");
   else
      Put_Line ("divisor=false");
   end if;
end Logico;
""", """
**Lo que esta clase enseña en Ada.** Ada no es lógico, y **es el lenguaje de esta página con la
conexión más fuerte con la programación lógica en su uso real** — por SPARK.

Cuando se escribe un contrato:

```ada
function Es_Divisor (A, B : Positive) return Boolean
   with Post => Es_Divisor'Result = (B mod A = 0);

procedure Ordenar (V : in out Vector)
   with Post => (for all I in V'First .. V'Last - 1 => V (I) <= V (I + 1));
```

...y se ejecuta `gnatprove`, lo que ocurre por debajo **es programación lógica pura**:

1. La herramienta traduce el programa y sus contratos a **fórmulas lógicas** —obligaciones de prueba—.
2. Se las pasa a **demostradores automáticos**: Z3, CVC5, Alt-Ergo.
3. Esos demostradores son **solucionadores SMT**, que buscan una asignación de valores que haga falsa
   la fórmula. **Si no existe, el contrato está demostrado.**

Ese "buscar una asignación que satisfaga las restricciones" es exactamente lo que dice el cierre de
esta clase, y es lo que hace un motor Prolog.

Y las expresiones cuantificadas de Ada 2012 (clase 117) son literalmente sintaxis de lógica de primer
orden dentro del lenguaje:

```ada
(for all I in V'Range => P (V (I)))
(for some I in V'Range => P (V (I)))
```

Con esas dos, más `Pre`, `Post`, `Type_Invariant` y `Subtype_Predicate`, **Ada permite escribir la
especificación lógica de un programa en el propio programa**, y demostrarla.

Merece subrayar la diferencia con las pruebas: un conjunto de casos de prueba comprueba **algunas**
entradas; una demostración cubre **todas**. Por eso SPARK se usa donde se usa —aviónica, ferrocarril,
criptografía—, y por eso el proyecto **seL4**, un microkernel verificado formalmente, es noticia: es
software del que se ha demostrado que hace lo que dice.

Y hay una anécdota que cierra bien: **Prolog y Ada son casi contemporáneos** —1972 y 1983— y los dos
salieron de proyectos europeos con financiación pública. La programación lógica prometía que se
programaría declarando; Ada prometía que se programaría con garantías. **Cuarenta años después, la
segunda promesa se cumplió usando la maquinaria de la primera.**
"""),
        "pascal": ("""
program Logico;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  Linea: string;
  Corte, A, B: Integer;

begin
  ReadLn(Linea);
  Linea := Trim(Linea);

  Corte := Pos(' ', Linea);
  A := StrToInt(Copy(Linea, 1, Corte - 1));
  B := StrToInt(Trim(Copy(Linea, Corte + 1, Length(Linea))));

  if B mod A = 0 then
    WriteLn('divisor=true')
  else
    WriteLn('divisor=false');
end.
""", """
**Lo que esta clase enseña en Pascal.** Pascal no es lógico y tiene un vínculo histórico con este
paradigma que merece contarse, porque es de los datos más curiosos de esta sección: **el primer
compilador de Prolog ampliamente distribuido se escribió en Pascal**.

**DEC-10 Prolog** (Warren, Pereira y Pereira, Edimburgo, 1977) fue el que convirtió a Prolog de
curiosidad académica en herramienta usable, y de él salió la **Máquina Abstracta de Warren (WAM)**, el
modelo de ejecución que **siguen usando casi todas las implementaciones de Prolog hoy**.

Y hay más: **Turbo Prolog** (Borland, 1986) llevó Prolog al PC con el mismo entorno integrado que
Turbo Pascal, y fue para mucha gente el primer contacto con el paradigma. Borland vendía los dos, con
la misma filosofía —compilador rápido, entorno integrado, precio bajo— y eso hizo por la difusión de
la programación lógica más que cualquier artículo.

Turbo Prolog era además **tipado y compilado**, al contrario que el Prolog de Edimburgo, lo que le
valió críticas de los puristas y lo hizo mucho más rápido.

Dentro de Pascal, lo más cercano a una regla declarada son los **conjuntos** de la clase 094 y el
`case` con rangos:

```pascal
if (C in ['a'..'z', 'A'..'Z']) then ...
case Estado of
  Nuevo, Pendiente: ...;
  Aprobado..Cerrado: ...;
end;
```

Un conjunto **es un predicado sobre un dominio finito**, y `in` es la comprobación de pertenencia con
sintaxis matemática. Es lo más declarativo que ofrece el lenguaje, y se lee bastante bien.

Y como en COBOL, el paradigma lógico llega al mundo Delphi por la puerta de las reglas de negocio: los
sistemas grandes guardan las reglas en tablas y las interpretan, precisamente para no recompilar. Es
la misma conclusión que la clase 117 saca sobre lo declarativo: **cuando las reglas cambian más rápido
que el código, se mueven a los datos**.
"""),
        "lisp": ("""
(let ((a (read))
      (b (read)))
  (format t "divisor=~A~%" (if (zerop (mod b a)) "true" "false")))
""", """
**Lo que esta clase enseña en Common Lisp.** Aquí está la conexión más importante de esta clase:
**Prolog salió de la tradición de Lisp**.

La línea histórica es directa y está documentada:

- **Planner** (Carl Hewitt, MIT, 1969): un lenguaje de reglas con encadenamiento hacia atrás,
  escrito en Lisp. **Su implementación parcial, Micro-Planner, es la influencia declarada de Prolog.**
- **Conniver** (1972): la respuesta del MIT a Planner, con control explícito de la búsqueda.
- **Alain Colmerauer**, en Marsella, tomó esas ideas y **Robert Kowalski** aportó la interpretación
  procedimental de la lógica de Horn. De ahí sale **Prolog, en 1972**.
- Y **los primeros Prolog se escribieron en Lisp**.

Esa relación no terminó ahí. En Lisp, **implementar un Prolog es un ejercicio de libro**: *Paradigms
of Artificial Intelligence Programming* (Norvig, 1992) dedica tres capítulos a construir uno completo,
con unificación, retroceso y compilación a Lisp.

Y hay bibliotecas que lo traen hecho:

```lisp
(ql:quickload :screamer)
(screamer:all-values
  (let ((x (screamer:an-integer-between 1 12)))
    (unless (zerop (mod 12 x)) (screamer:fail))
    x))                            ; (1 2 3 4 6 12) -- TODOS los divisores
```

**Eso es exactamente el ejercicio de esta clase resuelto al estilo Prolog**: se declara el dominio, se
descarta lo que no cumple, y el motor devuelve todas las soluciones. Con retroceso de verdad, no
generando y filtrando.

**Screamer** consigue eso sobre Common Lisp sin tocar el compilador, usando macros que transforman el
código a estilo de paso de continuaciones. Y su versión con restricciones, `screamer+`, añade
propagación — la base de la programación con restricciones.

Y merece nombrarse la otra mitad de la historia: **el algoritmo RETE** de Charles Forgy (1979), el
motor de encadenamiento hacia delante que está detrás de **OPS5**, **CLIPS**, **Jess** y **Drools**.
Se desarrolló en Lisp, y es la tecnología que hoy mueve los motores de reglas de negocio de medio
mundo.

Es el argumento de la clase 107 otra vez: **Lisp no adoptó el paradigma lógico — lo incubó**.
"""),
        "tcl": ("""
gets stdin linea
lassign [split [string trim $linea]] a b

if {$b % $a == 0} {
    puts "divisor=true"
} else {
    puts "divisor=false"
}
""", """
**Lo que esta clase enseña en Tcl.** Tcl no es lógico, y su parentesco con este paradigma está en algo
que sí tiene y que es media programación lógica: **el emparejamiento de patrones**.

```tcl
switch -glob -- $ruta {
    *.txt  { ... }
    *.log  { ... }
}
switch -regexp -- $linea {
    {^ERROR (\\d+): (.*)$} { ... }
}
string match {[a-z]*} $x
regexp {(\\d+)-(\\d+)} $texto -> desde hasta
```

**`regexp` con variables de captura es unificación en miniatura**: se da un patrón con huecos, y si el
dato encaja, **los huecos quedan ligados a valores**. Eso es exactamente lo que hace Prolog al unificar
`divide(3, X)` con un hecho.

La diferencia es la que marca el cierre de esta clase: **las expresiones regulares van en una sola
dirección** —comprueban y extraen— mientras que la unificación de Prolog funciona en las dos: el mismo
término sirve para comprobar y para generar.

Y Tcl es el anfitrión de un caso de programación lógica muy conocido y poco identificado como tal:
**Expect**.

```tcl
spawn ssh servidor
expect {
    "password:"       { send "$clave\\r"; exp_continue }
    "Permission denied" { error "clave incorrecta" }
    "$ "               { send "uptime\\r" }
    timeout            { error "sin respuesta" }
}
```

**`expect` con varios patrones es un conjunto de reglas**: "si aparece esto, haz aquello". El programa
no dice el orden en que ocurrirán las cosas — **declara qué hacer ante cada situación posible** y el
motor reacciona a lo que llegue.

Es programación dirigida por reglas aplicada al control de procesos interactivos, y Expect (Don Libes,
1990) es una de las herramientas que hicieron famoso a Tcl. Sigue usándose para automatizar
dispositivos de red, instaladores y cualquier cosa que pida contraseñas.

Y para lógica de verdad, Tcllib no trae nada; existen enlaces con SWI-Prolog y `struct::graph` para
recorridos. La conclusión honesta es que **Tcl no compite en este paradigma: lo automatiza desde
fuera**.
"""),
        "perl": ("""
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;
my ($a, $b) = split ' ', $linea;

print "divisor=", ($b % $a == 0 ? 'true' : 'false'), "\\n";
""", """
**Lo que esta clase enseña en Perl.** Perl no es lógico, y **tiene el motor de emparejamiento de
patrones más potente de esta página**, que es lo más cerca que llega un lenguaje imperativo de la
unificación.

```perl
if ($texto =~ /^(\\w+)-(\\d+)$/) {
    my ($nombre, $numero) = ($1, $2);      # los huecos quedan LIGADOS
}
```

Y las expresiones regulares de Perl fueron mucho más allá de las clásicas, hasta tener capacidades que
son propiamente lógicas:

```perl
(?<nombre>\\w+)                  # capturas con NOMBRE
(?=...)   (?!...)                # anticipación positiva y negativa
(?<=...)  (?<!...)                # retrospección
(?R)  (?1)                         # RECURSIÓN: patrones recursivos
(??{ codigo })                      # ejecutar código y usar el resultado como patrón
(?{ codigo })                        # ejecutar código durante el emparejamiento
```

**Los patrones recursivos** hacen de las expresiones regulares de Perl algo que ya no es un lenguaje
regular: **pueden reconocer paréntesis anidados**, que es formalmente imposible para un autómata
finito.

```perl
my $balanceado = qr/\\( (?: [^()]++ | (?R) )* \\)/x;
```

Eso es una gramática, y con `(??{ ... })` **el patrón se puede construir en ejecución**. Es un motor de
reconocimiento con retroceso —**exactamente el mecanismo de Prolog**— aplicado a texto.

Y esa es la conexión de fondo: **el retroceso del motor de expresiones regulares y el de Prolog son el
mismo algoritmo**. Cuando una alternativa falla, se deshace y se prueba la siguiente. De ahí que las
expresiones regulares mal escritas puedan tener explosión combinatoria —el llamado *ReDoS*— que es el
mismo problema que un Prolog que no termina.

Perl 6 —hoy **Raku**— llevó la idea al final con las **gramáticas**:

```raku
grammar Fecha {
    token TOP  { <anio> '-' <mes> }
    token anio { \\d ** 4 }
    token mes  { \\d ** 2 }
}
```

Una gramática de verdad, con reglas nombradas y acciones, **como parte del lenguaje**. Es el
reconocimiento declarativo llevado a su forma natural, y es una de las mejores ideas de Raku.
"""),
        "cpp": ("""
#include <iostream>

int main() {
    int a{}, b{};
    if (!(std::cin >> a >> b)) return 1;

    std::cout << "divisor=" << (b % a == 0 ? "true" : "false") << '\\n';
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** C++ no es lógico, y tiene el hallazgo más divertido de esta clase:
**su sistema de plantillas es un lenguaje lógico, y nadie lo diseñó así**.

Las plantillas con especialización parcial funcionan **exactamente como Prolog**: se declaran reglas
—especializaciones— y el compilador **busca cuál encaja** con los argumentos dados. Eso es unificación
y resolución.

```cpp
template <int N> struct Factorial {
    static constexpr int valor = N * Factorial<N - 1>::valor;   // la REGLA
};
template <> struct Factorial<0> {
    static constexpr int valor = 1;                              // el HECHO base
};

static_assert(Factorial<5>::valor == 120);
```

**Eso es un programa lógico**: un caso base y una regla recursiva, resueltos por búsqueda de patrones
en tiempo de compilación. Y como se dijo en la clase 107, **se descubrió en 1994** cuando Erwin Unruh
demostró que el sistema era Turing-completo — no estaba previsto.

De ahí salió toda la metaprogramación con plantillas, con su vocabulario propio:

```cpp
std::conditional_t<cond, A, B>        // el if
std::enable_if_t<cond, T>              // guardas: SFINAE
std::is_integral_v<T>                   // predicados sobre tipos
```

**SFINAE** —*Substitution Failure Is Not An Error*— es el mecanismo que hace de esto un motor lógico:
si al sustituir una plantilla el resultado no es válido, **no es un error: esa regla simplemente no
aplica y se prueba la siguiente**. Es literalmente el retroceso de Prolog.

Y su parecido con la programación lógica se nota en lo malo también: **los mensajes de error son
ilegibles**, porque el compilador cuenta por qué falló la búsqueda entre docenas de candidatos.

C++20 lo civilizó con **conceptos** y `if constexpr` (clases 107 y 112), que expresan lo mismo de forma
legible y con errores útiles.

Y hay una conexión más seria que merece nombrarse: **los solucionadores SAT y SMT más usados del mundo
—Z3, MiniSat, CVC5— están escritos en C++**. Son los motores que hay detrás de SPARK (la página de Ada
de esta misma clase), de la verificación de hardware y de los planificadores.

**C++ no es un lenguaje lógico y es el lenguaje en el que se implementa la lógica.**
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi LOGICO;
  a int(10) const;
  b int(10) const;
end-pi;

dcl-s r varchar(5);

if %rem(b : a) = 0;
  r = 'true';
else;
  r = 'false';
endif;

dsply ('divisor=' + r);

*inlr = *on;
return;
""", """
**Lo que esta clase enseña en RPG.** RPG no es lógico, y su historia con este paradigma es la más
peculiar de la página, porque **su forma original era declarativa por reglas** (clase 107).

En el RPG de columnas, la lógica se escribía con **indicadores**: banderas que se encendían al cumplirse
una condición y que condicionaban las líneas siguientes.

```text
C           SALDO     COMP 0                        10 11 12
C   10      TIPO      COMP 'V'                         20
C   1020                MOVE  'APROBAR'   ACCION
```

Léelo como una tabla: **"si el indicador 10 está encendido y el 20 también, entonces esta acción"**.
Eso es **una tabla de decisión**, y es exactamente el DETAB de COBOL de esta misma clase, integrado en
el lenguaje.

Y el ciclo de RPG lo completaba: **el programador no escribía cuándo se ejecutaba cada cosa**;
declaraba en qué condiciones y en qué nivel de ruptura, y el ciclo generado decidía el orden.

Es programación por reglas, en 1959, y su desaparición —el RPG libre de 2013 no la usa— es el
movimiento inverso al de la mayoría de los lenguajes.

Donde IBM i hace hoy programación lógica de verdad es en la base de datos:

```sql
ALTER TABLE clientes ADD CONSTRAINT saldo_valido CHECK (saldo >= 0);
ALTER TABLE pedidos ADD FOREIGN KEY (cliente) REFERENCES clientes;
CREATE TRIGGER validar BEFORE INSERT ON pedidos ...
```

**Las restricciones de integridad son reglas declaradas**, y el sistema las impone a todos los
programas, en cualquier lenguaje, para siempre. Es la observación que ya apareció en la clase 100: **la
validación pertenece al dato**.

Y con **`WITH RECURSIVE`** (clase 098), Db2 for i hace recorridos que en Prolog serían reglas
recursivas:

```sql
with recursive subordinados (id, nivel) as (
    select id, 0 from empleados where jefe is null
  union all
    select e.id, s.nivel + 1 from empleados e join subordinados s on e.jefe = s.id
)
select * from subordinados;
```

Eso es **una regla recursiva con caso base**, escrita en SQL. Es la misma forma que un predicado
Prolog, y el motor hace la búsqueda con punto fijo.
"""),
        "pli": ("""
 logico: procedure options(main);

    declare (a, b) fixed binary(31);

    get list (a, b);

    if mod(b, a) = 0 then
       put skip list ('divisor=true');
    else
       put skip list ('divisor=false');

 end logico;
""", """
**Lo que esta clase enseña en PL/I.** PL/I no es lógico, y su conexión con este paradigma es de época:
**PL/I y Prolog pertenecen a mundos que se ignoraron**.

PL/I salió de IBM en 1964 con la ambición de unificar la programación comercial y la científica. Prolog
salió de Marsella en 1972 desde la lógica matemática y el procesamiento del lenguaje natural. Los dos
proyectos eran grandes, ambiciosos y europeos-o-corporativos, y **no se cruzaron**.

Lo que PL/I sí tiene, y merece nombrarse en esta clase, es el tipo **`bit(n)`** de la clase 094, que
permite hacer álgebra de Boole de verdad:

```pli
 declare (condiciones, reglas(20)) bit(16);
 declare i fixed binary(31);

 do i = 1 to 20;
    if (condiciones & reglas(i)) = reglas(i) then
       call aplicar(i);         /* la regla i se cumple */
 end;
```

Eso es **un motor de reglas con máscaras de bits**: cada regla es un patrón de condiciones, y una
operación `&` comprueba si el estado actual lo satisface. Es rapidísimo —una instrucción por regla— y
era la forma habitual de implementar tablas de decisión en los sistemas de la época.

Y el preprocesador de PL/I (clases 088 y 115), con sus condicionales y bucles en tiempo de compilación,
permitía **generar el código de las reglas a partir de una tabla**, que es lo que hacían los
generadores de tablas de decisión.

Hay además una conexión indirecta que redondea la clase: **el SQL incrustado de PL/I** (clase 117) es
programación lógica en el sentido estricto. Un `SELECT` con varios `JOIN` y un `WHERE` **es una
consulta a una base de datos relacional, que es formalmente equivalente a un programa Datalog** —el
subconjunto de Prolog sin funciones—.

Esa equivalencia entre el álgebra relacional y la lógica de primer orden es un resultado de Codd de
1970, y es la razón de que las bases de datos deductivas y las relacionales sean parientes.

**El programador de PL/I lleva escribiendo lógica desde 1981 sin llamarla así.**
"""),
        "mumps": ("""
LOGICO ; Logico -- clase 118
 read linea
 set a = $piece(linea, " ", 1)
 set b = $piece(linea, " ", 2)
 write "divisor=", $select(b#a=0 : "true", 1 : "false"), !
 quit
""", """
**Lo que esta clase enseña en M.** M no es lógico, y el programa usa **`$select`**, que es la
expresión condicional del lenguaje y se lee sorprendentemente como una tabla de reglas:

```mumps
 set nivel = $select(edad<18 : "menor", edad<65 : "adulto", 1 : "jubilado")
```

**Pares condición-valor, evaluados en orden, con `1` como caso final.** Es un `cond` de Lisp, y es una
de las construcciones más usadas de M porque cabe en una línea.

Y aquí, como en toda esta parte, lo interesante está en la capa que la comunidad construyó encima:
**FileMan es un motor de reglas**.

Cada campo de cada fichero puede llevar código M asociado que el sistema ejecuta automáticamente
(clase 113):

```text
Campo .01  NAME
  INPUT TRANSFORM:  K:$L(X)>30!($L(X)<3) X
  EXECUTABLE HELP:  D HELP^DPTNAME
Campo 15   ESTADO
  TRIGGER:          S ^DPT(DA,"FECHA")=DT
  CROSS-REFERENCE:  S ^DPT("AEST",X,DA)=""
```

- **`INPUT TRANSFORM`** es una **regla de validación**: se ejecuta al introducir el dato y lo rechaza
  si no cumple.
- **`TRIGGER`** es una **regla de propagación**: al cambiar este campo, actualiza aquel.
- **`CROSS-REFERENCE`** mantiene **índices automáticamente**.

Eso es exactamente lo que hace un motor de reglas de negocio: **hechos, condiciones y acciones
declaradas fuera del código, aplicadas por un intérprete**. Y lleva funcionando desde 1982 en cientos
de hospitales.

La diferencia con Prolog es la del cierre de esta clase: **FileMan encadena hacia delante** —cuando
cambia un dato, dispara lo que dependa— mientras que Prolog encadena hacia atrás — para probar algo,
busca qué lo justifica. Son los dos modos clásicos de un sistema de reglas, y los motores modernos
implementan los dos.

Y hay una conexión histórica que merece cerrar la clase: **los sistemas expertos médicos de los
setenta y ochenta —MYCIN, INTERNIST-I, CADUCEUS— eran programación lógica aplicada a la medicina**, y
se desarrollaron en Lisp mientras los historiales clínicos se guardaban en M.

Las dos mitades del problema, en dos lenguajes de esta página, sin llegar a juntarse.
"""),
        "smalltalk": ("""
| partes a b |

partes := stdin nextLine substrings collect: [ :cada | cada asNumber ].
a := partes first.
b := partes second.

Transcript
    show: 'divisor=', ((b \\\\ a = 0) ifTrue: [ 'true' ] ifFalse: [ 'false' ]);
    cr.
""", """
**Lo que esta clase enseña en Smalltalk.** El `\\\\` del programa es el operador módulo de Smalltalk —un
mensaje binario, como todo—, y `b \\\\ a = 0` se lee de izquierda a derecha sin precedencias: **primero
el módulo, después la igualdad**.

Smalltalk no es lógico, y su relación con este paradigma tiene un episodio histórico que merece
contarse, porque explica una parte de por qué el lenguaje no se generalizó.

En los años ochenta, **la inteligencia artificial simbólica y la programación orientada a objetos
compitieron por el mismo espacio**: las estaciones Lisp de Symbolics y LMI, los sistemas expertos, y
Smalltalk como entorno de desarrollo interactivo. Cuando llegó el **invierno de la IA** a finales de
los ochenta, el mercado de máquinas y entornos especializados se hundió, y **Smalltalk arrastró parte
de esa caída** pese a no ser un lenguaje de IA.

Lo que sí hay en Smalltalk, y es propio, son **implementaciones de motores de reglas en el propio
sistema**. La más notable es que **el patrón Visitante y la reflexión permiten construir motores de
inferencia con muy poco código**, y hubo productos comerciales —Humble, KnowledgeWorks— que lo
explotaron.

Y hay una conexión directa que sí prosperó: **la unificación aplicada a la refactorización**.

```smalltalk
RBParser parseExpression: 'foo bar: `@arg'
```

El **Refactoring Browser** (clase 098) usa **patrones de código con metavariables** —los backtick de
ahí— para buscar y transformar código:

```text
`@receptor foo: `@arg     "encaja con CUALQUIER envío de foo: "
```

Eso **es unificación sobre árboles de sintaxis**: un patrón con huecos que se liga con el código real.
Es el mismo mecanismo que Prolog, aplicado a la manipulación de programas, y es lo que hace posible
que un IDE ofrezca "reemplaza todas las apariciones de este patrón" con seguridad.

Esa técnica —**la reescritura de términos**— es la base de las herramientas de refactorización
modernas, de los *linters* con reglas configurables y de las transformaciones de código automáticas. Y
está aquí, en un lenguaje de objetos de 1980, porque **cuando el programa es un objeto inspeccionable,
razonar sobre él es programación lógica**.
"""),
    },
)
