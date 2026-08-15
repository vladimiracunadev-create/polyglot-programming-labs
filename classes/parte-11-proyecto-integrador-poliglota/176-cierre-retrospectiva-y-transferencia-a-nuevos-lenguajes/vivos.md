# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 176

> [⬅️ Volver a la clase 176](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

La última clase: contar las lecciones y afirmar que son transferibles. Y esta página cierra 136 clases de
lenguajes vivos con la pregunta que las justifica todas: **¿para qué sirve haber mirado COBOL, Fortran,
Ada, Pascal, Lisp, Tcl, Perl, C++, RPG, PL/I, M y Smalltalk?** La respuesta no es para usarlos —aunque
varios se sigan usando— sino porque **en ellos están las decisiones originales, con sus razones
intactas**, y reconocerlas en cualquier lenguaje nuevo es lo que convierte aprender en reconocer.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es la **transferencia**, y estos doce lenguajes son el mejor material posible porque
> **cada uno lleva una decisión al extremo**: la aritmética exacta, los arreglos, la seguridad demostrada,
> la legibilidad, el código como dato, el texto como código, la expresividad, el control total, la
> plataforma integrada, la ambición, el dato persistente, y todo como objeto.
>
> Y las decisiones extremas se ven; las moderadas se confunden con lo natural. **Por eso se aprende más de
> un lenguaje raro que de uno cómodo.**
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: un entero `n` (número de lecciones que te llevas) → stdout: `lecciones=<n> transferible=si`
- **Regla:** `informar las lecciones y confirmar la transferibilidad`

| stdin | esperado |
|---|---|
| `5` | `lecciones=5 transferible=si` |
| `12` | `lecciones=12 transferible=si` |
| `1` | `lecciones=1 transferible=si` |

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
PROGRAM-ID. CIERRE.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(40).
01  N       PIC S9(9) COMP.
01  ED      PIC -(8)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    COMPUTE N = FUNCTION NUMVAL(LINEA)

    MOVE N TO ED
    DISPLAY "lecciones=" FUNCTION TRIM(ED) " transferible=si"
    STOP RUN.
```

**Lo que se lleva de COBOL.** Tres cosas, y ninguna es sintaxis.

**Una, que los números decimales no son coma flotante** (clase 072). COBOL lo tuvo claro en 1959 porque
su dominio era el dinero, y **cualquier lenguaje moderno tiene un tipo decimal** —`BigDecimal`,
`decimal`, `Decimal`— **que casi nadie usa hasta que llega el primer céntimo descuadrado**.

**Reconocerlo**: en cuanto un programa maneje dinero, cantidades exactas o porcentajes que se suman, la
pregunta es cuál es el tipo decimal del lenguaje y por qué no se está usando.

**Dos, que la legibilidad es una decisión de diseño con coste** (clase 146). COBOL se diseñó para que lo
leyera gente de negocio, y **por eso es verboso**. Hoy nadie diseñaría así, y **la intención sigue siendo
correcta**: **el código se lee muchas más veces de las que se escribe** (clase 154).

**Y tres, que un sistema puede sobrevivir a todos sus autores** (clase 175). COBOL es la prueba de que el
software dura mucho más de lo que su autor imagina, y de que **lo que se pierde no es el código: es el
porqué**.

**Reconocerlo**: cada vez que alguien pregunte "¿por qué está esto así?" y nadie sepa la respuesta, ahí
hay una decisión que no se documentó (clase 154).

Y merece cerrar con la lección incómoda que COBOL enseña mejor que ningún otro de esta página: **el
software que funciona vale más que el software elegante**.

Doscientos mil millones de líneas ejecutando el sistema financiero mundial son un argumento — y quien
trabaje alguna vez en un sistema así descubrirá que **la pregunta no es cómo reescribirlo, sino cómo
respetarlo mientras se construye lo siguiente al lado** (clase 150).

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program cierre
   implicit none
   integer :: n

   read(*, *) n

   write(*, '(A,I0,A)') 'lecciones=', n, ' transferible=si'
end program cierre
```

**Lo que se lleva de Fortran.** Tres cosas que se aplican en cualquier lenguaje.

**Una, que el rendimiento moderno es un problema de memoria, no de aritmética** (clases 128 y 152). La
lección de LAPACK —**diez veces más rápido sin cambiar el algoritmo, solo el orden de acceso**— es la más
transferible de este curso.

**Reconocerlo**: ante un bucle lento, la primera pregunta no es cuántas operaciones hace, sino **cuántos
datos trae de memoria y si los aprovecha**. El orden de los bucles, la disposición de los datos y la
localidad importan más que el número de instrucciones.

**Dos, que la coma flotante no es igualdad** (clases 073 y 140). Comparar reales con `==`, esperar que dos
ejecuciones den lo mismo, o suponer que la suma es asociativa: los tres son errores, y **están en todos
los lenguajes**.

**Y tres, que declarar más permite optimizar más.** `intent`, `pure`, los arreglos que no se solapan: cada
declaración es información que el compilador usa (clase 164).

**Reconocerlo**: `const`, `final`, `readonly`, `noexcept`, los tipos inmutables — **todo lo que restringe
lo que el programa puede hacer permite que la herramienta razone mejor**. La ceremonia que parece
burocracia suele ser información.

Y merece cerrar con lo que Fortran enseña sobre la vida del software y que la clase 154 desarrolló: **el
código científico está mejor validado y peor mantenido que casi ningún otro**.

Y la conclusión no es que los científicos escriban mal: es que **la validación del resultado y la calidad
del software son cosas distintas**, y **un programa puede ser correcto y a la vez imposible de
modificar**.

Es una distinción útil en cualquier dominio.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;
with Ada.Strings;
with Ada.Strings.Fixed;

procedure Cierre is
   N : Integer;
begin
   Get (N);

   Put_Line ("lecciones=" & Ada.Strings.Fixed.Trim (N'Image, Ada.Strings.Both) &
             " transferible=si");
end Cierre;
```

**Lo que se lleva de Ada.** Es, probablemente, el lenguaje de esta página con más lecciones
transferibles, y merece elegir tres.

**Una, que un tipo puede llevar el dominio dentro** (clase 124).

```ada
subtype Porcentaje is Integer range 0 .. 100;
type Metros is new Float;      --  y NO se puede sumar a Pies
```

**Reconocerlo**: en cualquier lenguaje, **cada vez que se escribe una comprobación de rango en varios
sitios, ahí falta un tipo**. Los tipos envoltorio, los enumerados y los tipos con validación en el
constructor hacen lo mismo — y **convierten una comprobación repetida en una garantía**.

**Dos, que un contrato escrito puede comprobarse** (clase 118). Precondiciones, postcondiciones e
invariantes existen en Ada, y **su equivalente existe en todos los lenguajes**: aserciones, `assert`,
tipos refinados, o simplemente una prueba que documenta la expectativa (clase 139).

**Reconocerlo**: cuando un comentario dice "este parámetro no puede ser nulo", **eso es una precondición
que no se comprueba** — y hay una forma de escribirla para que sí.

**Y tres, que renunciar a características compra propiedades** (clases 146 y 152). Ravenscar, `pragma
Restrictions` y SPARK son eso: **quitar la mitad del lenguaje para poder demostrar cosas sobre la otra
mitad**.

**Reconocerlo**: es lo mismo que hacen `strict mode`, los subconjuntos de un lenguaje, las reglas de
estilo que prohíben construcciones (clase 146), y **la programación funcional al renunciar al estado
mutable**.

**Lo que un lenguaje prohíbe es lo que permite a sus herramientas prometer.**

Y esa es, quizá, la idea más importante de todo este curso, y por eso Ada la lleva al extremo: **la
libertad y las garantías son el mismo recurso, repartido de otra manera**.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Cierre;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  N: Integer;

begin
  Read(N);
  WriteLn('lecciones=', IntToStr(N), ' transferible=si');
end.
```

**Lo que se lleva de Pascal.** Tres lecciones, y las tres son de diseño.

**Una, que un lenguaje pequeño es una decisión, no una carencia** (clase 164). Wirth hizo Pascal, luego
Modula-2 y luego Oberon, **cada uno más pequeño que el anterior**, con un criterio explícito: **una
característica solo entra si su beneficio supera el coste de que todos tengan que aprenderla y leerla**.

**Reconocerlo**: ante cualquier lenguaje o biblioteca que crece, la pregunta es si cada adición se paga —
y **PL/I en esta misma página es el experimento contrario, con su resultado** (clase 155).

**Dos, que la herramienta forma el estilo** (clase 149). El diseñador visual de Delphi hacía facilísimo
poner la lógica en el manejador del botón, **y por eso millones de líneas la tienen ahí**.

**Reconocerlo**: **la arquitectura por defecto de una herramienta será la del 90 % del código**, por mucho
que el documento diga otra cosa. Si se quiere otra estructura, **hay que hacer que el camino correcto sea
el más fácil**: plantillas, generadores, comprobaciones automáticas (clase 147).

**Y tres, que la compilación rápida cambia cómo se trabaja** (clase 123). Turbo Pascal compilaba en
segundos cuando lo normal eran minutos, y eso **no fue una mejora de comodidad: cambió el ciclo**.

**Reconocerlo**: cualquier cosa que acorte el ciclo —compilación incremental, recarga en caliente,
pruebas rápidas (clase 147)— **rinde mucho más de lo que su descripción sugiere**, porque **cambia cuántas
veces al día se experimenta**.

Y merece cerrar con lo que Pascal enseña sobre este curso entero: **fue diseñado para enseñar**, y sigue
haciéndolo bien porque **hace visible lo que otros lenguajes esconden** — la diferencia entre asignar y
comparar, entre declarar y usar, entre valor y referencia.

**Y ver esas diferencias es exactamente lo que permite reconocerlas en cualquier otro sitio.**

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let ((n (read)))
  (format t "lecciones=~D transferible=si~%" n))
```

**Lo que se lleva de Common Lisp.** Lisp es el lenguaje del que más cosas han salido, y la lista de la
clase 164 lo resume: **la recolección de basura, los cierres, el REPL, las excepciones, las macros, el
tipado dinámico y buena parte de los IDE**.

Y tres lecciones para llevarse:

**Una, que el código puede ser un dato** (clases 122 y 123). Es la idea más radical de esta página, y su
consecuencia práctica es que **un lenguaje puede extenderse hacia el problema** (clase 149).

**Reconocerlo**: las macros de Rust, los decoradores de Python, los constructores de consultas (clase
170), JSX, y **cualquier cosa que genere código a partir de una declaración** — todos son la misma idea,
más limitada.

**Y su coste también es transferible**: **lo que se genera es difícil de analizar y de depurar** (clase
150), así que la regla de Lisp vale en todas partes: **si una función basta, no uses una macro**.

**Dos, que el ciclo corto es una capacidad, no una comodidad** (clase 124). El REPL de Lisp permite probar
una idea en segundos, y eso **cambia qué problemas se pueden atacar**: los mal definidos, donde hay que
explorar.

**Reconocerlo**: los cuadernos, la recarga en caliente y las pruebas rápidas persiguen lo mismo — y
**merece invertir en el ciclo antes que en casi cualquier otra cosa**.

**Y tres, que el manejo de errores puede ofrecer más que abortar** (clase 116). Los reinicios de Lisp
—**decidir cómo continuar desde donde se sabe qué hacer**— siguen siendo superiores a `try`/`catch`, y
casi ningún lenguaje los tiene.

**Reconocerlo**: cada vez que un manejador de errores tenga que reconstruir el contexto que se perdió al
propagar, **ahí falta lo que Lisp tenía**.

Y merece cerrar con lo que Lisp enseña sobre este curso: **es un lenguaje de 1958 del que la industria
sigue extrayendo ideas**, y eso debería bastar para desconfiar de la palabra "moderno".

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea
set n [string trim $linea]

puts "lecciones=$n transferible=si"
```

**Lo que se lleva de Tcl.** Tres lecciones, y la primera es de arquitectura.

**Una, la tesis de los dos lenguajes** (clase 155): **un sistema se construye mejor con uno de sistemas
para los componentes y uno de guion para unirlos**, porque **el 90 % de los cambios ocurre en el
pegamento**.

**Reconocerlo**: está en todas partes —los complementos de un editor, los guiones de un motor de juego, la
configuración programable de una herramienta (clase 163)— y **la pregunta útil en cualquier sistema es
qué capa cambia todos los días y si está hecha del material adecuado**.

**Dos, que la uniformidad es una propiedad valiosa** (clases 081 y 161). En Tcl **todo es una cadena y
todo es un canal**, y eso hace que **el mismo código sirva para un fichero, una tubería y un socket**.

**Reconocerlo**: cada vez que una API trata de forma distinta cosas que son conceptualmente iguales,
**está pidiendo que su usuario aprenda una distinción que no aporta nada** — y `everything is a file` de
Unix es la misma idea con el mismo beneficio.

**Y tres, que ejecutar código ajeno es un problema de capacidades, no de listas negras** (clase 153).
Safe-Tcl, de 1993, **quitó todo y concedió puertas concretas** — y ese modelo es hoy el de WebAssembly,
el de los contenedores y el de los permisos móviles (clase 162).

**Reconocerlo**: ante cualquier complemento, guion de usuario o dependencia de terceros, la pregunta
correcta no es qué prohibir, sino **qué necesita de verdad y cómo dárselo solo a eso**.

Y merece cerrar con lo que Tcl enseña sobre el éxito: **su idea principal ganó tan completamente que hoy
es invisible**, y casi nadie sabe que hubo que defenderla.

**Es la mejor forma de éxito que puede tener una idea**, y también la razón por la que conviene conocer
de dónde vienen las cosas: **lo que hoy parece obvio fue una decisión, y tuvo alternativas**.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $n = <STDIN>;
chomp $n;

print "lecciones=$n transferible=si\n";
```

**Lo que se lleva de Perl.** Perl es el lenguaje del que la industria copió más infraestructura sin
citarlo, y la lista de la clase 164 lo resume: **CPAN, TAP, CPAN Testers, el modo taint, POD, las
severidades de perlcritic y las expresiones regulares tal como todos las usan**.

Y tres lecciones:

**Una, que el ecosistema vale más que el lenguaje** (clase 164). CPAN, en 1995, **inventó el archivo de
paquetes** y con él la forma de trabajar de todos los ecosistemas posteriores.

**Reconocerlo**: al evaluar cualquier tecnología, **la pregunta que más pesa no es cómo es el lenguaje,
sino qué hay ya escrito para tu problema** — y las clases 143 y 164 lo repiten desde varios ángulos.

**Dos, que "hay más de una forma de hacerlo" tiene un precio** (clases 146 y 154). Perl es libertad total,
y **su fama de ilegible es la factura**.

**Reconocerlo**: cualquier lenguaje o biblioteca con muchas formas de hacer lo mismo **acaba con un
dialecto por persona**, y la respuesta es la de la clase 146: **un estándar de estilo comprobado
automáticamente**, no la disciplina individual.

**Y tres, que marcar el dato que viene de fuera es una idea excelente** (clase 153). El modo taint de
1989 —**los datos externos están marcados y no se pueden usar en operaciones peligrosas hasta validarlos
explícitamente**— sigue siendo poco imitado y muy sensato.

**Reconocerlo**: es lo que persiguen el análisis de flujo de datos, los tipos "validado" frente a "sin
validar" y **la disciplina de validar en la frontera**. Y la regla que queda es simple: **toda entrada es
hostil hasta que se demuestre lo contrario, y demostrarlo es comprobar contra una lista de lo permitido**.

Y merece cerrar con lo que Perl enseña sobre las modas: **su declive no fue técnico**. Perl 5 siguió
mejorando todo el tiempo; lo que cambió fue la percepción, y quince años de espera por una versión que
acabó siendo otro lenguaje.

**La suerte de una tecnología depende de cosas que no son su calidad** — y saberlo ayuda a juzgar las de
hoy.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>

int main() {
    long long n{};
    if (!(std::cin >> n)) return 1;

    std::cout << "lecciones=" << n << " transferible=si" << '\n';
    return 0;
}
```

**Lo que se lleva de C++.** Tres lecciones, y las tres se aplican a lenguajes que no se parecen en nada a
él.

**Una, que la gestión de recursos es un patrón, no una característica** (clase 132). RAII —**atar la vida
de un recurso a la de un objeto**— es la mejor solución que existe al problema de liberar lo que se
reserva, y **su equivalente está en todos los lenguajes**: `with` en Python, `try-with-resources` en Java,
`defer` en Go, `using` en C#, `unwind-protect` en Lisp (clase 171).

**Reconocerlo**: cada vez que haya un `abrir` sin un `cerrar` garantizado, **falta el mecanismo del
lenguaje que lo garantiza** — y todos lo tienen.

**Dos, que el comportamiento indefinido es una categoría distinta de "error"** (clase 136). Un programa
con comportamiento indefinido **no hace algo incorrecto: deja de tener significado**, y puede funcionar
durante años y romperse al cambiar de compilador.

**Reconocerlo**: las carreras de datos en cualquier lenguaje, el orden de evaluación no especificado, y
todo lo que la documentación llame "no especificado" o "depende de la implementación" — **son promesas que
nadie hizo, y apoyarse en ellas es deuda invisible**.

**Y tres, que la seguridad de memoria no se consigue con disciplina** (clases 153 y 164). El 70 % de las
vulnerabilidades graves de los sistemas grandes son de esa familia, **escritas por equipos excelentes con
revisión y herramientas**.

**Reconocerlo**: es el argumento más fuerte que existe a favor de que **la garantía la dé la herramienta y
no la persona** — y se aplica más allá de la memoria: **a los tipos, a la concurrencia, a los contratos y
al formato del código** (clase 146).

Y merece cerrar con lo que C++ enseña sobre la evolución: **es un lenguaje que ha cambiado
profundamente cuatro veces sin romper nada**, y esa compatibilidad —que es su gran virtud— **es también
por qué un proyecto real contiene cuatro generaciones a la vez** (clase 154).

**Todo lo que se promete mantener, hay que mantenerlo.**

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

dcl-pi CIERRE;
  n int(10) const;
end-pi;

dsply ('lecciones=' + %char(n) + ' transferible=si');

*inlr = *on;
return;
```

**Lo que se lleva de RPG e IBM i.** Tres lecciones, y ninguna es del lenguaje.

**Una, que la integración de plataforma tiene un valor que no aparece en las comparativas** (clase 164).
Base de datos, seguridad, colas, planificación, registro y observabilidad **en un solo sistema
coherente** dan una productividad operativa que un montaje de veinte piezas no alcanza — y **dos personas
de sistemas mantienen lo que en otra arquitectura serían diez**.

**Reconocerlo**: al comparar arquitecturas, **contar las piezas que hay que integrar, versionar, vigilar y
parchear** es tan importante como comparar las capacidades.

**Dos, que la compatibilidad comprobada es mejor que la prometida** (clases 143 y 160). La firma de un
programa de servicio —**calculada sobre las exportaciones y verificada al arrancar**— hace lo que el
versionado semántico intenta expresar con un número.

**Reconocerlo**: `abi-compliance-checker`, `buf breaking`, las pruebas de contrato (clase 160) — **todo lo
que convierte una promesa en una comprobación automática** merece el esfuerzo, porque **las promesas se
rompen sin querer**.

**Y tres, que la observabilidad puede ser una propiedad del sistema y no un producto** (clase 142). En
IBM i, **cada trabajo lleva su registro con la pila y el número de sentencia, sin instrumentar nada**.

**Reconocerlo**: la pregunta correcta ante cualquier sistema es **"¿qué puedo saber de lo que pasó sin
haberlo previsto?"** — y la respuesta suele ser "poco", porque la observabilidad se añade después y solo
donde alguien se acordó.

Y merece cerrar con lo que esta plataforma enseña sobre el software y las personas, que es la lección más
seria de esta parte: **un sistema puede ser técnicamente sólido y estar en riesgo por completo**.

**El relevo generacional de estos sistemas no es un problema de tecnología** (clase 154), y **no se
resuelve modernizando el código**: se resuelve capturando el porqué de las reglas antes de que se vaya
quien lo sabe.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 cierre: procedure options(main);

    declare n fixed binary(31);

    get list (n);

    put skip list ('lecciones=' || trim(char(n)) || ' transferible=si');

 end cierre;
```

**Lo que se lleva de PL/I.** PL/I es el lenguaje de esta página que menos se usa y del que más se aprende
sobre diseño, y merece tres lecciones.

**Una, que un lenguaje que lo permite todo no puede prometer casi nada** (clase 155). PL/I quiso sustituir
a Fortran y a COBOL a la vez, **y perdió contra los dos** — porque **el compilador de un lenguaje
especializado puede suponer más**, y suponer es lo que permite optimizar y verificar.

**Reconocerlo**: es la misma idea que Ada lleva al extremo en esta página, vista desde el otro lado. **Cada
característica que un lenguaje añade le quita garantías**, y la ambición tiene un precio que se paga
siempre.

**Dos, que el tamaño es un coste de mantenimiento** (clase 154). Un lenguaje que nadie domina entero
**produce un dialecto por persona**, y un sistema con cinco dialectos internos es cinco veces más caro de
entender.

**Reconocerlo**: se aplica a los lenguajes, a los marcos y a las bibliotecas internas — y la defensa es la
de la clase 146: **un subconjunto acordado y comprobado**.

**Y tres, la más práctica y la más dura: sin implementación libre, un lenguaje no llega a las plataformas
nuevas** (clase 162).

**Reconocerlo**: al elegir cualquier tecnología con horizonte largo, **la pregunta sobre quién la mantiene
y bajo qué licencia pesa más que casi cualquier característica** — porque decide si dentro de quince años
seguirá habiendo un camino hacia adelante.

Y merece cerrar con lo que PL/I aporta a la memoria de la disciplina: **tenía en 1964 el manejo de
excepciones con reanudación, la concurrencia en el lenguaje, el decimal exacto y un preprocesador
programable** (clases 116 y 163).

**Muchas de las ideas que hoy parecen recientes tienen sesenta años y ya se probaron.**

Y saberlo cambia cómo se leen las novedades: **no todas lo son, y las que no lo son vienen con su
historia de por qué no funcionaron la primera vez**.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
CIERRE ; Retrospectiva -- clase 176
 read n
 write "lecciones=", n, " transferible=si", !
 quit
```

**Lo que se lleva de M.** M es el lenguaje de esta página que más rechazo produce a primera vista y el
que más ideas valiosas esconde, y merece tres.

**Una, que el desajuste entre el lenguaje y la base de datos no es inevitable** (clase 170). En M **la
variable persistente y la variable local se diferencian en un carácter**, y con eso desaparecen el
mapeo objeto-relacional, la serialización y media capa de infraestructura.

**Reconocerlo**: cada vez que un sistema tenga tres representaciones del mismo dato —el objeto, la fila y
el JSON—, **ahí hay una traducción que cuesta código y produce fallos** (clases 159 y 170). No siempre se
puede evitar, y saber que es una decisión y no una ley ayuda a elegir.

**Dos, que un modelo de datos jerárquico y ordenado es una buena idea que se abandonó y volvió** (clases
099 y 170). Las globals de M son árboles ordenados, persistentes y transaccionales — **y las bases de
clave y valor las redescubrieron cuarenta años después, casi siempre sin las transacciones**.

**Reconocerlo**: el modelo de datos se elige por los patrones de acceso, y **lo jerárquico gana cuando el
acceso se conoce de antemano** — igual que IMS en la clase 170.

**Y tres, la más incómoda de este curso: una tecnología se juzga por su arquitectura, no por su
sintaxis** (clase 164).

**M tiene una sintaxis indefendible con criterios actuales y un modelo de datos excelente.** Y quien se
quede en lo primero **no verá lo segundo**, y concluirá que los sistemas construidos sobre él son un error
— cuando llevan cuarenta años sin perder datos de pacientes.

**Reconocerlo**: es un sesgo constante en las discusiones de tecnología, y **la pregunta que lo corrige es
la del cierre de esta clase**: **¿qué decidió esto, contra qué, y por qué?**

Y merece cerrar con lo que M enseña sobre las decisiones heredadas: **su estilo abreviado fue una decisión
correcta cuando la memoria era cara, y sobrevivió a su motivo** (clase 154).

**Y ese es el patrón general**: **casi ninguna decisión antigua fue estúpida cuando se tomó**. Lo que
suele fallar no es la decisión: **es que nadie escribió su contexto** — que es exactamente el argumento de
la clase 175 y de este curso entero.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| n |

n := stdin nextLine trimBoth asNumber.

Transcript show: 'lecciones=', n printString, ' transferible=si'; cr.
```

**Lo que se lleva de Smalltalk.** Y con esto cierran las 136 clases de esta serie.

Smalltalk es el lenguaje de esta página con menos usuarios y más descendencia, y la clase 164 hizo la
lista: **la interfaz gráfica, MVC, el Observador, las pruebas unitarias, TDD, la refactorización
automática, la deuda técnica, las cachés de envío que hacen posible todo JIT moderno, y buena parte de lo
ágil**.

Y tres lecciones para llevarse:

**Una, que la uniformidad conceptual tiene poder.** En Smalltalk **todo es un objeto y todo es un envío de
mensaje** —incluidos el `if`, el bucle y la clase (clase 151)—, y de esa única decisión salen la
reflexión, el depurador vivo, la refactorización automática y el navegador.

**Reconocerlo**: cuando un lenguaje o un sistema tiene pocos conceptos aplicados con consistencia,
**aprende más rápido y compone mejor** — y cuando tiene muchos casos especiales, cada uno hay que
recordarlo.

**Dos, que un sistema que se puede preguntar es un sistema que se puede gobernar** (clases 138, 150 y
165). Smalltalk puede responder qué clases tiene, quién llama a qué, qué no usa nadie y dónde está parado
un proceso.

**Reconocerlo**: **cada pregunta que un sistema no puede responder sobre sí mismo se acaba respondiendo
con arqueología** — y las herramientas de análisis, los registros estructurados y las trazas existen para
recuperar parte de esa capacidad.

**Y tres, que las mejores ideas no vienen de la tecnología más usada.** Una comunidad pequeña, trabajando
en un lenguaje minoritario, produjo la forma en que hoy trabaja todo el sector.

**Y esa es la razón de haber recorrido estos doce lenguajes.**

No para usarlos —aunque varios se sigan usando, y con buenas razones (clase 164)— sino porque **cada uno
llevó una decisión al extremo y por eso se ve**: la aritmética exacta, la memoria, la demostración, la
legibilidad, el código como dato, el texto como código, el texto como especialidad, el control, la
plataforma, la ambición, el dato persistente, y el objeto.

**Y todas esas decisiones están, más discretas, en el lenguaje que uses mañana.**

Reconocerlas es lo que convierte aprender un lenguaje nuevo en **reconocer un reparto conocido de
compromisos** — y esa es la única habilidad de este curso que no caduca.

---

## Y de vuelta a la clase

Lo transferible —y es lo último de esta serie—: **un lenguaje es un conjunto de decisiones, y todas se
pagan**. Lo que un lenguaje te da, se lo quita a otra cosa: la seguridad cuesta ceremonia, la
flexibilidad cuesta análisis, el rendimiento cuesta control manual, la abstracción cuesta previsibilidad.
Y por eso la pregunta útil ante cualquier lenguaje nuevo no es si es bueno, sino **qué decidió, contra
qué, y si eso encaja con lo que tienes delante**. Quien sabe hacer esa pregunta aprende un lenguaje nuevo
en semanas; quien no, lleva veinte años aprendiendo el primero.

⏮️ [Volver a la clase 176](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
