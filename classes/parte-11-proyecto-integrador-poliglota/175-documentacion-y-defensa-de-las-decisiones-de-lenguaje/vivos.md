# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 175

> [⬅️ Volver a la clase 175](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Contar las secciones de un documento: `documentado=5 secciones`. Es lo más aburrido de esta parte y lo
que más se agradece dentro de tres años. Y estos lenguajes son la mejor prueba de por qué: **todos ellos
fueron, en su momento, una decisión razonable** — y hoy, quien se encuentra ese código sin explicación
suele concluir que alguien se equivocó. **Lo que falta casi nunca es el código: es el porqué** (clase
154).

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es la **decisión documentada**, y estos lenguajes lo enseñan porque **son decisiones que
> han sobrevivido a sus autores**. Un sistema COBOL de 1985, un modelo Fortran de 1978 o un paquete VistA
> de 1990 llevan décadas ejecutándose, y **la pregunta que todo el mundo hace al llegar es la misma: ¿por
> qué está esto así?**
>
> Y aparece el formato que la industria ha encontrado para responderla: **el registro de decisión de
> arquitectura**, corto, con contexto, alternativas y consecuencias.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: un entero `n` (número de secciones documentadas) → stdout: `documentado=<n> secciones`
- **Regla:** `informar el número de secciones`

| stdin | esperado |
|---|---|
| `5` | `documentado=5 secciones` |
| `1` | `documentado=1 secciones` |
| `8` | `documentado=8 secciones` |

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
PROGRAM-ID. DOCUMEN.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(40).
01  N       PIC S9(9) COMP.
01  ED      PIC -(8)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    COMPUTE N = FUNCTION NUMVAL(LINEA)

    MOVE N TO ED
    DISPLAY "documentado=" FUNCTION TRIM(ED) " secciones"
    STOP RUN.
```

**La decisión, escrita: COBOL.** Así se vería el registro de decisión que casi nunca se escribió y que hoy
haría falta:

```text
DECISIÓN 001 — Mantener el motor de cálculo de intereses en COBOL
Estado: aceptada (2024), revisada desde la original de 1987

CONTEXTO
  - 240.000 líneas de COBOL implementan las reglas de cálculo,
    incluidas 30 años de normativa acumulada y sus excepciones.
  - No existe especificación escrita: el código ES la especificación (clase 154).
  - El sistema procesa el cierre diario en una ventana de 4 horas.
  - La aritmética es decimal exacta y auditada por el regulador (clase 072).

DECISIÓN
  Mantener el motor en COBOL y exponerlo como servicio (clases 149 y 160).
  Todo lo nuevo se escribe fuera.

ALTERNATIVAS CONSIDERADAS
  - Reescritura completa a Java: descartada. Las reescrituras de sistemas
    sin especificación fracasan con frecuencia documentada (clase 150),
    y el coste de reproducir el redondeo decimal exacto es alto (clase 140).
  - Traducción automática: descartada. Produce código que nadie entiende
    y hereda la deuda sin las personas que la conocen.
  - Estrangulamiento por partes: ACEPTADA para las funciones que cambien.

CONSECUENCIAS
  + La lógica validada no se toca; el riesgo regulatorio no aumenta.
  + Lo nuevo se escribe con tecnología actual.
  - Dependencia de un perfil escaso, con relevo generacional urgente (clase 154).
  - Y hay que mantener la capa de fachada.

REVISAR SI
  - se pierde el conocimiento del equipo actual
  - o cambia la normativa de forma que obligue a tocar el núcleo
```

**Y el apartado "revisar si" merece destacarse**, porque es el que convierte un documento en una
herramienta: **una decisión correcta depende de un contexto, y decir cuál permite saber cuándo dejó de
serlo** (clase 154).

Sin él, la decisión se hereda como dogma — y es exactamente lo que le pasó al estilo abreviado de M
(clase 154) y a tantas otras.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program documen
   implicit none
   integer :: n

   read(*, *) n

   write(*, '(A,I0,A)') 'documentado=', n, ' secciones'
end program documen
```

**La decisión, escrita: Fortran.**

```text
DECISIÓN 007 — El núcleo numérico se mantiene en Fortran moderno

CONTEXTO
  - El solver tiene 80.000 líneas, validado contra datos experimentales
    y contra soluciones analíticas durante 20 años (clase 173).
  - Se ejecuta en clústeres con MPI, hasta 4.000 procesos.
  - Depende de LAPACK y de FFTW, y su rendimiento está optimizado
    para el orden de acceso por columnas (clases 149 y 152).
  - El equipo son físicos, no ingenieros de software.

DECISIÓN
  Mantener Fortran para el núcleo, y Python para todo lo demás:
  preparación de datos, orquestación, análisis y gráficas (clase 155).

ALTERNATIVAS CONSIDERADAS
  - C++ con Eigen: rendimiento equivalente. Descartada porque el equipo
    no lo domina y porque reescribir invalidaría 20 años de validación.
  - Julia: atractiva; descartada por madurez del ecosistema MPI
    y por el coste de migrar. REVISAR en 3 años.
  - Todo en Python con NumPy: descartada. Los bucles anidados con
    dependencias no se vectorizan bien.

CONSECUENCIAS
  + Se conserva la validación y el rendimiento.
  + La capa de Python permite trabajar a quien no sabe Fortran.
  - Hay que mantener la frontera con f2py (clase 158).
  - Y hay que invertir en lo que al código le falta:
    pruebas (clase 139), construcción reproducible (clase 144) y un dueño.

REVISAR SI
  - Julia o Rust alcanzan paridad de ecosistema en HPC
  - o si el equipo cambia lo bastante como para no poder mantenerlo
```

**Y la línea de las consecuencias sobre lo que "hay que invertir" es la más útil de este documento**,
porque nombra la deuda de forma explícita (clase 154).

**Una decisión que reconoce lo que deja pendiente es una decisión honesta**; una que solo lista ventajas
es publicidad.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;
with Ada.Strings;
with Ada.Strings.Fixed;

procedure Documen is
   N : Integer;
begin
   Get (N);

   Put_Line ("documentado=" &
             Ada.Strings.Fixed.Trim (N'Image, Ada.Strings.Both) & " secciones");
end Documen;
```

**La decisión, escrita: Ada.** En el dominio de Ada, este documento **no es opcional**: forma parte del
expediente de certificación, y merece verlo con ese peso.

```text
DECISIÓN 002 — Ada/SPARK para el software de control de vuelo

CONTEXTO
  - Requisito DO-178C nivel A: un fallo es catastrófico.
  - Hay que demostrar cobertura MC/DC (clase 139) y ausencia de
    errores de ejecución.
  - Vida operativa prevista: 30 años.
  - Restricciones: memoria acotada, plazos duros, sin sistema operativo.

DECISIÓN
  Ada 2012 con perfil Ravenscar y subconjunto SPARK para los módulos
  de nivel A (clases 135 y 146).

ALTERNATIVAS CONSIDERADAS
  - C con MISRA-C: viable y usado en el sector. Descartada porque
    exige herramientas externas para lo que Ada da en el lenguaje,
    y la evidencia de análisis es más costosa de producir.
  - Rust: seguridad de memoria comparable. Descartada HOY por falta de
    cadena de herramientas cualificada y de precedente ante el regulador
    (clase 164). REVISAR en cada nuevo programa.
  - Generación desde modelo (SCADE): ACEPTADA para las leyes de control;
    el código generado es Ada.

CONSECUENCIAS
  + gnatprove demuestra la ausencia de errores de ejecución (clase 118).
  + El perfil Ravenscar permite demostrar los plazos (clase 152).
  - Contratación difícil: hay que formar internamente (clase 154).
  - Ecosistema pequeño: casi todo se escribe en casa.
  - Y la cadena de herramientas queda CONGELADA durante el programa (clase 174).

REVISAR SI
  - la certificación de una cadena Rust madura
  - o si el coste de contratación se vuelve prohibitivo
```

**Y merece señalar lo que este dominio hace y que el resto debería copiar**: **las alternativas se
documentan aunque se descarten**, y **se dice qué las haría ganar**.

Es la diferencia entre "elegimos Ada" y "elegimos Ada, y esto es lo que tendría que pasar para elegir otra
cosa" — la segunda es una decisión de ingeniería; la primera, una preferencia.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Documen;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  N: Integer;

begin
  Read(N);
  WriteLn('documentado=', IntToStr(N), ' secciones');
end.
```

**La decisión, escrita: Object Pascal.**

```text
DECISIÓN 015 — Mantener el terminal de punto de venta en Delphi

CONTEXTO
  - 4.200 terminales instalados en tiendas, con hardware específico:
    balanza, cajón, impresora fiscal, lector (clase 165).
  - Deben funcionar SIN RED: una caída de línea no puede parar la caja.
  - Aplicación de 350.000 líneas, 18 años de evolución.
  - Actualización remota, sin técnico en tienda (clase 148).

DECISIÓN
  Mantener Delphi para el terminal. La lógica de negocio ya está
  separada en unidades sin interfaz (clase 149) y se prueba con DUnitX.

ALTERNATIVAS CONSIDERADAS
  - Aplicación web: descartada. No funciona sin red y el acceso al
    hardware local exige un agente nativo igualmente.
  - Electron o similar: descartada. Arranque lento y consumo alto
    para el hardware instalado, que tiene 8 años.
  - .NET o Java: viable técnicamente. Descartada por el coste de
    reescribir la integración con hardware, que es la parte cara.

CONSECUENCIAS
  + Binario autocontenido, arranque instantáneo, sin dependencias (clase 174).
  + La inversión en integración de hardware se conserva.
  - Licencias de Delphi y contratación difícil (clase 164).
  - Y el ecosistema encoge: hay que asumir mantener más cosas en casa.

REVISAR SI
  - se renueva el parque de terminales
  - o si aparece una necesidad de movilidad que el escritorio no cubra
```

**Y la fila de "no funciona sin red" merece destacarse** porque es el tipo de restricción que suele
faltar en estas discusiones y que decide el resultado.

**Las decisiones de tecnología casi nunca las gana el lenguaje mejor**: las gana **la restricción que
elimina más opciones** — y escribirla es lo que hace que la discusión sea corta y la decisión, defendible.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let ((n (read)))
  (format t "documentado=~D secciones~%" n))
```

**La decisión, escrita: Common Lisp.**

```text
DECISIÓN 021 — El motor de reglas de tarificación en Common Lisp

CONTEXTO
  - Las reglas de precio las definen los actuarios, cambian cada mes
    y tienen interacciones complejas entre sí.
  - Intentos previos con tablas de configuración se quedaron cortos:
    acabaron necesitando condicionales, y luego variables (clase 163).
  - El equipo son 3 personas, con experiencia en Lisp.

DECISIÓN
  Motor en Common Lisp, con un lenguaje de dominio definido con macros
  (clase 149), aislado tras una API (clase 160).

ALTERNATIVAS CONSIDERADAS
  - Motor de reglas comercial: descartado por coste y por rigidez
    del modelo de reglas frente a lo que el dominio necesita.
  - Python con un DSL: viable. Descartada porque las macros permiten
    que la regla se lea como la escribe el actuario, y eso reduce
    los errores de traducción.
  - Reglas en la base de datos: descartada por lo que enseña VistA
    (clase 151): la lógica deja de ser revisable y versionable.

CONSECUENCIAS
  + Las reglas se escriben en el vocabulario del dominio.
  + El ciclo de prueba es de segundos (clase 124).
  - RIESGO PRINCIPAL: un solo dueño. Mitigación obligatoria:
    documentar el porqué (clase 154), macros solo cuando una función
    no baste (clase 150), y pruebas que sirvan de especificación (clase 139).
  - Contratación muy difícil.
  - Y la API es la frontera: si hay que reescribirlo, se reescribe
    solo este componente (clase 165).

REVISAR SI
  - el equipo baja de dos personas que lo dominen
  - o si el ritmo de cambio de las reglas se estabiliza
```

**Y la línea del riesgo principal es la que hace útil este documento**: **nombra el peligro y escribe la
mitigación**.

**Una decisión que no dice cómo puede salir mal no está terminada** — y en tecnologías minoritarias, el
riesgo casi siempre es el mismo y casi nunca se escribe.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea
set n [string trim $linea]

puts "documentado=$n secciones"
```

**La decisión, escrita: Tcl.**

```text
DECISIÓN 009 — Tcl como lenguaje de guion de la herramienta

CONTEXTO
  - La herramienta es un motor de simulación en C++ (clase 165).
  - Los usuarios son ingenieros que necesitan automatizar flujos
    y componer análisis, no programar el motor.
  - El sector ya usa Tcl en las herramientas equivalentes (clase 149):
    los usuarios lo conocen.
  - Los flujos que escriban durarán más que varias versiones del producto.

DECISIÓN
  Incrustar Tcl como lenguaje de comandos, con una API de comandos
  registrados explícitamente (clase 163).

ALTERNATIVAS CONSIDERADAS
  - Lua: más pequeño y más rápido. Descartada porque los usuarios
    del sector ya escriben Tcl y sus flujos existentes se podrían reusar.
  - Python incrustado: más popular en general. Descartada por el peso
    del intérprete y por la fragmentación de versiones del entorno.
  - Un lenguaje propio: DESCARTADA explícitamente. Es el error que
    Ousterhout describió al crear Tcl (clase 155) y siempre acaba
    siendo un lenguaje mal diseñado sin herramientas.

CONSECUENCIAS
  + Los usuarios son productivos desde el primer día.
  + Safe-Tcl permite ejecutar guiones de terceros con capacidades
    acotadas y límites de recursos (clases 153 y 163).
  - Compromiso de compatibilidad: los guiones de los clientes
    NO se pueden romper entre versiones (clase 160).
  - Y la comunidad de Tcl es pequeña: menos bibliotecas de terceros.

REVISAR SI
  - el perfil de usuario cambia hacia gente que espera Python
```

**Y la alternativa descartada explícitamente —inventar un lenguaje propio— merece estar escrita**, porque
es la que siempre vuelve.

**Documentar por qué NO se hizo algo evita repetir la discusión cada dos años** — y es, probablemente, el
valor más subestimado de este tipo de documento.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $n = <STDIN>;
chomp $n;

print "documentado=$n secciones\n";
```

**La decisión, escrita: Perl.**

```text
DECISIÓN 033 — El proceso de integración de ficheros sigue en Perl

CONTEXTO
  - 47 proveedores envían ficheros en 31 formatos distintos, algunos
    definidos hace 20 años y ninguno negociable a corto plazo.
  - El proceso tiene 6.000 líneas y 12 años (clase 165).
  - Se ejecuta cada noche y es crítico: si falla, no hay facturación.
  - Tiene 0 % de cobertura de pruebas.

DECISIÓN
  Mantenerlo en Perl, y ANTES de cualquier cambio:
    1. pruebas de caracterización con ficheros reales (clase 150)
    2. un contrato declarado para la entrada y la salida (clase 160)
    3. un dueño identificado

ALTERNATIVAS CONSIDERADAS
  - Reescribir en Python: descartada de momento. Sin pruebas,
    una reescritura no se puede verificar (clase 140).
  - Herramienta ETL comercial: descartada. Los formatos irregulares
    exigen lógica que las herramientas gráficas expresan mal.
  - Dejarlo como está: DESCARTADA. Es el estado actual y ya ha
    provocado dos incidentes.

CONSECUENCIAS
  + El proceso sigue funcionando mientras se estabiliza.
  + Con pruebas y contrato, la reescritura futura será verificable.
  - Perl es hoy una elección minoritaria: la contratación cuesta.
  - Y hay que invertir en lo que debió hacerse hace años.

REVISAR SI
  - los pasos 1 a 3 están completos: entonces la reescritura
    pasa a ser una decisión de coste, no de riesgo
```

**Y ese último apartado es lo mejor que puede tener un documento de este tipo**: **convierte "algún día
habrá que hacer algo" en una condición concreta**.

Es la diferencia entre una deuda que se arrastra y una que tiene un plan (clase 154) — y la condición
escrita es lo que permite volver a la conversación con datos en lugar de con opiniones.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>

int main() {
    long long n{};
    if (!(std::cin >> n)) return 1;

    std::cout << "documentado=" << n << " secciones" << '\n';
    return 0;
}
```

**La decisión, escrita: C++.**

```text
DECISIÓN 004 — C++ para el motor de procesado, con frontera en C

CONTEXTO
  - El motor procesa 2 millones de eventos por segundo con un
    presupuesto de 50 µs en el percentil 99 (clase 152).
  - Depende de bibliotecas de terceros que solo existen en C++.
  - Lo consumen componentes en Python y en Go (clase 155).

DECISIÓN
  Motor en C++20, expuesto con una interfaz en C y punteros opacos
  (clase 156). Aislado en su propio proceso (clase 165).

ALTERNATIVAS CONSIDERADAS
  - Rust: rendimiento equivalente y seguridad de memoria (clase 164).
    Descartada HOY por las bibliotecas de terceros. Se ha ACEPTADO
    escribir los componentes NUEVOS en Rust, con frontera en C.
  - Go: descartada por las pausas del recolector frente al presupuesto
    de latencia del percentil 99.
  - Java: ídem.

CONSECUENCIAS
  + Se cumple el presupuesto de latencia.
  + La interfaz en C sirve para cualquier lenguaje cliente (clase 157).
  - RIESGO: seguridad de memoria. Mitigaciones OBLIGATORIAS:
    desinfectantes en toda la suite (clase 147), fuzzing continuo
    de las fronteras (clase 173), y proceso aislado para que un
    fallo no comprometa el resto (clase 153).
  - Y el proyecto acumulará varias generaciones del lenguaje: hay
    que fijar el estándar y un formateador desde el día uno (clase 146).

REVISAR SI
  - las bibliotecas críticas tienen equivalente en Rust
  - o si el análisis de incidentes muestra que las mitigaciones no bastan
```

**Y las mitigaciones marcadas como obligatorias son lo que distingue una decisión responsable de una
imprudente.**

Elegir C++ sabiendo el riesgo y poniendo las defensas es ingeniería; elegirlo sin nombrarlo es lo que
produce el 70 % de las vulnerabilidades de la clase 153.

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

dcl-pi DOCUMEN;
  n int(10) const;
end-pi;

dsply ('documentado=' + %char(n) + ' secciones');

*inlr = *on;
return;
```

**La decisión, escrita: RPG e IBM i.**

```text
DECISIÓN 012 — Permanecer en IBM i, con RPG modernizado

CONTEXTO
  - ERP propio de 1,2 millones de líneas, 28 años, en producción
    con 900 usuarios y disponibilidad del 99,98 %.
  - La plataforma aporta base de datos, seguridad, colas,
    planificación y observabilidad integradas (clases 142 y 164).
  - Coste operativo actual: 2 personas de sistemas.
  - Edad media del equipo de desarrollo: 54 años (clase 154).

DECISIÓN
  Permanecer. Y ejecutar un plan de modernización EN la plataforma:
    - conversión a formato totalmente libre (clase 150)
    - extracción de lógica a programas de servicio (clase 149)
    - SQL en lugar de acceso registro a registro (clase 152)
    - fuentes en git, en el IFS (clase 145) y CI con ibmi-bob (clase 147)
    - y APIs REST con IWS para lo nuevo (clase 160)

ALTERNATIVAS CONSIDERADAS
  - Migrar a un ERP de mercado: descartada. El ajuste funcional
    cubre el 60 %; el resto habría que reimplementarlo igualmente.
  - Reescribir en Java sobre Linux: descartada por coste y riesgo
    (clase 150), y porque habría que reconstruir lo que la plataforma
    da de fábrica: 2 personas de sistemas pasarían a ser un equipo.
  - No hacer nada: DESCARTADA. El riesgo de relevo es inmediato.

CONSECUENCIAS
  + Se conserva la lógica validada y el coste operativo bajo.
  + Lo nuevo se escribe con tecnología actual, sobre la misma máquina.
  - Dependencia de un único proveedor.
  - Y hay que resolver el relevo: contratación, formación y captura
    del conocimiento de las reglas, con urgencia (clase 154).

REVISAR SI
  - el relevo generacional no se resuelve en 3 años
  - o si el coste de licencias cambia significativamente
```

**Y la última consecuencia con la palabra "urgencia" es la más importante del documento**, porque es la
única con plazo.

**Una decisión que identifica un riesgo sin fecha es una decisión que lo aplaza** — y este es el caso
donde eso sale más caro.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 documen: procedure options(main);

    declare n fixed binary(31);

    get list (n);

    put skip list ('documentado=' || trim(char(n)) || ' secciones');

 end documen;
```

**La decisión, escrita: PL/I.**

```text
DECISIÓN 018 — Migrar el sistema actuarial de PL/I, por fases

CONTEXTO
  - 600.000 líneas de PL/I, cálculo de reservas técnicas, 35 años.
  - NO hay implementación libre del lenguaje (clase 162): no se puede
    compilar ni probar fuera del mainframe (clase 147).
  - El equipo que lo conoce son 3 personas; 2 se jubilan en 4 años.
  - La normativa de solvencia obliga a cambios frecuentes.

DECISIÓN
  Migración por estrangulamiento (clase 150), no reescritura completa:
    1. fachada de servicios sobre el sistema actual (clase 160)
    2. verificador de equivalencia con datos reales, en paralelo (clase 140)
    3. traducción función a función, verificada contra el original
    4. y apagado del componente viejo solo cuando el nuevo lleve
       6 meses coincidiendo

ALTERNATIVAS CONSIDERADAS
  - Reescritura completa: descartada. 600.000 líneas sin especificación
    y con un plazo de 4 años es el escenario clásico de fracaso.
  - Traducción automática PL/I → Java: descartada como solución única.
    Produce código sintácticamente correcto e ilegible, y hereda
    la deuda sin las personas. Se usará como PUNTO DE PARTIDA de cada
    función, con refactorización posterior.
  - Permanecer: descartada por el riesgo de relevo y por la
    imposibilidad de montar una CI moderna.

CONSECUENCIAS
  + Cada paso es reversible y el sistema funciona todo el tiempo.
  + El verificador de equivalencia da evidencia ante el regulador.
  - Es lento: 4 a 6 años.
  - Y exige mantener los dos sistemas durante la transición.

REVISAR SI
  - el ritmo de traducción se desvía más de un 30 % del plan
```

**Y la decisión de usar la traducción automática como punto de partida y no como resultado merece
destacarse**, porque es el matiz que suele faltar: **la herramienta ahorra la parte mecánica y no sustituye
al criterio**.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
DOCUMEN ; Documentar decisiones -- clase 175
 read n
 write "documentado=", n, " secciones", !
 quit
```

**La decisión, escrita: M.**

```text
DECISIÓN 026 — Conservar el núcleo clínico en M, sobre YottaDB

CONTEXTO
  - Historia clínica de 40 años, con lógica clínica validada
    y usada por 12.000 profesionales.
  - El modelo de datos —árboles ordenados, transaccionales,
    sin impedancia (clase 170)— encaja con el dominio.
  - El lenguaje es indefendible con criterios actuales: sin
    declaraciones, con ámbito global por defecto, con indirección
    imposible de analizar (clases 146 y 150).
  - Un error clínico puede causar daño a un paciente.

DECISIÓN
  Separar las dos cosas:
    - CONSERVAR el motor de datos (YottaDB) y la lógica clínica en M
    - ESCRIBIR todo lo nuevo en otros lenguajes, contra las mismas
      globals con los envoltorios oficiales (clase 156)
    - EXPONER el sistema con FHIR, no con estructuras internas (clase 160)

ALTERNATIVAS CONSIDERADAS
  - Migrar a un sistema comercial: descartada por coste y porque
    la lógica local acumulada se perdería.
  - Migrar los datos a PostgreSQL: descartada. El modelo jerárquico
    encaja mejor con la historia clínica que el relacional, y la
    migración pondría en riesgo 40 años de datos.
  - Reescribir la lógica clínica: descartada por riesgo asistencial.

CONSECUENCIAS
  + El dato y su lógica validada no se tocan.
  + Lo nuevo se escribe con tecnología actual y personal contratable.
  + FHIR permite integrar aplicaciones de terceros (clase 169).
  - Sigue habiendo código M que mantener, con relevo difícil.
  - Y hay una deuda pendiente: el código dentro del diccionario de
    datos es ejecución sin límites (clases 151 y 163). Plan: sustituirlo
    por extensiones acotadas.

REVISAR SI
  - la deuda del código en el diccionario provoca un incidente
  - o si aparece un motor con el mismo modelo y mejor ecosistema
```

**Y la separación entre "el lenguaje" y "el motor" es lo que hace defendible esta decisión** (clase 164).

**Sin ese matiz, la discusión se reduce a "M es antiguo" y se pierde lo único que importa: que el modelo
de datos es bueno y los datos son irremplazables.**

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| n |

n := stdin nextLine trimBoth asNumber.

Transcript show: 'documentado=', n printString, ' secciones'; cr.
```

**La decisión, escrita: Smalltalk.**

```text
DECISIÓN 030 — Smalltalk para el modelo de dominio del sistema de seguros

CONTEXTO
  - El dominio tiene 400 tipos de cobertura con interacciones,
    y cambia varias veces al año.
  - El equipo trabaja con los actuarios en sesiones de modelado.
  - Requisito: poder explorar reglas nuevas en horas, no en semanas.
  - El resto del sistema —web, integración— usa tecnología convencional.

DECISIÓN
  Modelo de dominio en Pharo, con persistencia en GemStone (clase 172),
  expuesto por API REST (clase 160). Todo lo demás, fuera.

ALTERNATIVAS CONSIDERADAS
  - Java o C# con un ORM: viable y descartada por el ciclo de
    exploración: el modelado con objetos vivos es mucho más rápido
    para este dominio (clase 124).
  - Motor de reglas comercial: descartado por rigidez.
  - Python: buen ciclo, y descartada por la persistencia de objetos:
    GemStone elimina el mapeo objeto-relacional por completo.

CONSECUENCIAS
  + Ciclo de modelado de minutos; los actuarios participan directamente.
  + Sin impedancia entre el modelo y el almacenamiento (clase 170).
  - Comunidad pequeña; contratación muy difícil (clase 164).
  - El modelo de imagen exige disciplina con git (clase 145) y con
    la construcción reproducible (clase 174). Mitigación: Tonel,
    Metacello con versiones fijas, e imagen construida desde cero en CI.
  - Y GemStone es comercial: dependencia de proveedor.

REVISAR SI
  - el equipo que lo domina baja de tres personas
  - o si el ritmo de cambio del dominio se estabiliza y el ciclo
    rápido deja de compensar sus costes
```

**Y merece cerrar esta clase con la observación que las doce decisiones de esta página comparten**: **en
ninguna gana el lenguaje "mejor"**.

Gana **el que encaja con el contexto**: la validación acumulada, el modelo de datos, el equipo, la
restricción dura, el horizonte temporal.

**Y todas las decisiones dicen bajo qué condición habría que revisarlas** — que es lo único que impide que
una decisión razonable de hoy se convierta en el "¿por qué está esto así?" de dentro de veinte años, que
es exactamente lo que estos doce lenguajes llevan escuchando toda su vida.

---

## Y de vuelta a la clase

Lo transferible: **documenta las decisiones, no el código**. El código dice qué hace; lo que se pierde es
**qué se consideró, qué se descartó y por qué** — y sin eso, quien llegue después solo puede suponer que
fue un error. De ahí el formato que funciona y que cabe en una página: **contexto** (qué problema había y
qué restricciones), **decisión** (qué se eligió), **alternativas** (qué más se miró y por qué no), y
**consecuencias** (qué se gana, qué se pierde y qué habría que revisar si cambia el contexto). Y la regla
que lo hace sostenible: **las decisiones se escriben cuando se toman**, porque reconstruirlas después es
imposible.

⏮️ [Volver a la clase 175](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
