# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 142

> [⬅️ Volver a la clase 142](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Una línea de registro con su nivel y su dato: `[INFO] procesados=5`. Es el programa más humilde de la
parte y el que más se parece a lo que hay en producción. Y esta clase existe porque **el registro es lo
único que queda cuando el fallo ya pasó**: el depurador de la clase 141 exige que el problema esté
ocurriendo ahora, y **la mayoría no lo está**. Aquí hay además un caso que sorprende: **IBM i registra
todo eso sin que nadie lo pida**.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es la **observabilidad**: dejar suficiente rastro para reconstruir lo que pasó sin
> estar delante. Y estos lenguajes lo enseñan porque **llevan décadas operando sin nadie mirando** —lotes
> nocturnos, sistemas embarcados, hospitales, cajeros—, así que su cultura de registro es anterior al
> término y en algunos casos mejor que la actual.
>
> Y aparece la tensión central de la clase: **cuanto más se registra, más cuesta y más ruido hay**. Cada
> lenguaje de esta página resuelve el equilibrio de una manera distinta, y todas siguen vigentes.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: un entero `n` (elementos procesados) → stdout: `log=[INFO] procesados=<n>`
- **Regla:** `emitir un registro de nivel INFO con el conteo`

| stdin | esperado |
|---|---|
| `5` | `log=[INFO] procesados=5` |
| `0` | `log=[INFO] procesados=0` |
| `3` | `log=[INFO] procesados=3` |

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
PROGRAM-ID. REGISTRO.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA  PIC X(80).
01  N      PIC S9(9) COMP.
01  ED-N   PIC -(8)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    COMPUTE N = FUNCTION NUMVAL(LINEA)

    MOVE N TO ED-N
    DISPLAY "log=[INFO] procesados=" FUNCTION TRIM(ED-N)
    STOP RUN.
```

**Lo que esta clase enseña en COBOL.** El mundo COBOL lleva sesenta años haciendo lo que hoy se llama
observabilidad, con otro nombre y con una diferencia importante: **el registro no era un fichero de
texto, era un fichero con estructura**.

```cobol
       01  REG-LOG.
           05  LOG-TIMESTAMP   PIC X(26).
           05  LOG-NIVEL       PIC X(5).
           05  LOG-PROGRAMA    PIC X(8).
           05  LOG-TRANSACCION PIC X(16).
           05  LOG-USUARIO     PIC X(10).
           05  LOG-CODIGO      PIC 9(4).
           05  LOG-TEXTO       PIC X(120).
```

**Ese registro de longitud fija, con campos declarados, es un registro estructurado** — la idea que la
industria redescubrió con JSON treinta años después.

Y tiene una ventaja que el JSON no tiene: **se puede leer con un programa COBOL, ordenar con `SORT` y
consultar sin analizar nada**, porque cada campo está en una posición conocida.

Y hay una capacidad del mainframe que merece ser el centro de esta explicación, porque es la mejor
respuesta de esta página al problema de correlacionar: **SMF, el *System Management Facility***.

**Cada trabajo, cada transacción CICS, cada llamada a DB2 y cada operación de fichero escribe un
registro SMF automáticamente**, con:

- **CPU consumida**, en milisegundos, por paso y por transacción.
- **Operaciones de entrada y salida**, contadas.
- **Memoria usada.**
- **Tiempo de respuesta**, desglosado.
- **Usuario, terminal, programa y hora.**

Sin instrumentar nada. **Es exactamente lo que hoy se llama telemetría, y lleva funcionando desde
1966.**

Y sobre eso se construyó lo que hoy llamaríamos facturación por uso: **el *chargeback*** — cobrar a cada
departamento por los recursos que consumió, calculado desde los registros SMF.

Y en CICS, la correlación tiene nombre: **la *task number* y el *unit of work ID*** identifican una
transacción a través de todos sus componentes —programa, base de datos, colas—, que es exactamente lo
que un identificador de traza distribuida hace hoy.

La lección de esta clase es incómoda para el discurso de la modernidad: **la observabilidad no se
inventó en la última década; se inventó cuando el tiempo de máquina costaba dinero y había que
justificarlo.**

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program registro
   implicit none
   integer :: n

   read(*, *) n

   write(*, '(A,I0)') 'log=[INFO] procesados=', n
end program registro
```

**Lo que esta clase enseña en Fortran.** El registro en cálculo científico tiene un problema propio que
esta clase debe explicar, y no es el habitual: **hay miles de procesos escribiendo a la vez**.

```fortran
! 10.000 procesos MPI escribiendo a stdout: ilegible y lentísimo
write(*, *) 'paso', paso, 'residuo', residuo
```

Las técnicas que la comunidad usa:

**Primera, escribir solo desde el proceso maestro:**

```fortran
if (mi_rango == 0) write(*, '(A,I0,A,ES12.5)') 'paso ', paso, ' residuo ', residuo
```

**Segunda, un fichero por proceso**, cuando hace falta el detalle:

```fortran
write(nombre, '(A,I5.5,A)') 'log_', mi_rango, '.txt'
open(newunit=u, file=nombre, status='replace')
```

**Y tercera, y es la crítica: `flush`.**

```fortran
write(u, '(A)') mensaje
flush(u)
```

**Sin `flush`, el mensaje se queda en el búfer** y **si el programa aborta se pierde exactamente lo que
interesa** (clase 141). En un cálculo de ocho horas que revienta a la séptima, esa línea es la
diferencia entre saber dónde falló y no saberlo.

Y el coste hay que decirlo: **`flush` en cada línea con 10.000 procesos satura el sistema de ficheros
paralelo**. El compromiso habitual es **vaciar en los mensajes de nivel alto y no en los de traza**.

Y Fortran tiene una particularidad de formato que ayuda mucho y merece nombrarse:

```fortran
write(*, '(A,I0,A,ES12.5,A,F6.2,A)') 'paso=', p, ' residuo=', r, ' t=', t, 's'
```

**`ES12.5` es notación científica normalizada** —una cifra antes del punto— y **`I0` es el ancho
mínimo**. Con eso, **las líneas salen alineadas y son analizables por columnas**, que es lo que
permite graficar la convergencia con un guion de tres líneas.

Y es una observación transferible: **el formato del registro determina si se puede analizar**. Un
registro que hay que leer con expresiones regulares complejas es un registro mal diseñado, y ese es el
argumento a favor del registro estructurado que atraviesa esta clase.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Registro is
   N : Integer;
begin
   Get (N);

   Put ("log=[INFO] procesados=");
   Put (N, Width => 1);
   New_Line;
end Registro;
```

**Lo que esta clase enseña en Ada.** Ada aborda el registro desde su dominio: **sistemas embarcados y
críticos, donde escribir a un fichero puede no ser una opción** — no hay disco, no hay sistema de
ficheros, o el tiempo de escritura no es acotado.

De ahí soluciones que merecen conocerse porque son transferibles a cualquier sistema con restricciones
de tiempo real:

**Un búfer circular en memoria**, que se vuelca solo si hace falta:

```ada
protected Bitacora is
   procedure Anotar (Codigo : Evento; Valor : Integer);
   procedure Volcar;
private
   Buffer : array (0 .. 1023) of Registro;
   Indice : Natural := 0;
end Bitacora;
```

**El objeto protegido garantiza el acceso seguro entre tareas** (clase 135) **con un tiempo máximo
acotado**, que es el requisito duro: un registro que puede bloquear indefinidamente no es aceptable en
un sistema de tiempo real.

**Y códigos numéricos en lugar de texto**:

```ada
type Evento is (Arranque, Lectura_Sensor, Fuera_De_Rango, Parada);
Bitacora.Anotar (Fuera_De_Rango, Valor);
```

**Registrar un enumerado y un número ocupa unos pocos bytes y no requiere formatear nada.** El texto se
compone después, en tierra, con la tabla de códigos.

Es la técnica de las cajas negras de aviación y de las sondas espaciales, y la razón es doble: **espacio
y determinismo**.

Y el ecosistema de Ada añade:

| Herramienta | Qué hace |
|---|---|
| **GNATCOLL.Traces** | registro con canales activables por fichero de configuración |
| **Ada.Exceptions** | nombre, mensaje e información con traza (clase 138) |
| **`'Image`** | representación textual de cualquier tipo, sin escribir formateadores |
| **`pragma Debug`** | instrumentación que desaparece sin `-gnata` (clase 141) |

**GNATCOLL.Traces merece el detalle** porque implementa bien la idea central de la clase:

```text
# fichero de configuración, leído al arrancar
+
SQL=yes
CACHE=no
NETWORK=yes:file:/tmp/red.log
```

**Los canales se activan sin recompilar y sin reiniciar**, y cada uno puede ir a un destino distinto.
Es el mismo modelo que los registradores por categoría de cualquier marco moderno, y encaja con la
regla de esta clase: **la decisión de qué registrar debe poder tomarse después de desplegar**.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Registro;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  N: Integer;

begin
  Read(N);

  WriteLn('log=[INFO] procesados=', IntToStr(N));
end.
```

**Lo que esta clase enseña en Pascal.** El ecosistema Pascal resolvió el registro por la vía de sus
aplicaciones típicas: **software de escritorio instalado en máquinas ajenas**, donde el registro es
literalmente la única información que llegará.

Free Pascal trae la unidad en la distribución:

```pascal
uses EventLog;

var Log: TEventLog;
begin
  Log := TEventLog.Create(nil);
  Log.LogType := ltFile;          { o ltSystem: ¡el registro del SISTEMA! }
  Log.FileName := 'app.log';
  Log.Active := True;

  Log.Info('procesados=%d', [N]);
  Log.Warning('reintento %d', [Intento]);
  Log.Error('fallo: %s', [E.Message]);
end;
```

**`ltSystem` es lo interesante**: escribe **al registro de eventos de Windows o a syslog en Unix**, con
la misma llamada. La unidad abstrae la diferencia, y el mensaje aparece donde los administradores ya
miran.

Es un principio que conviene extraer: **el mejor sitio para un registro suele ser donde ya se está
mirando**, no un fichero nuevo que nadie sabe que existe.

Y el ecosistema añade:

| Herramienta | Qué hace |
|---|---|
| **`EventLog`** | en la distribución; fichero, syslog o registro de Windows |
| **`log4delphi` / `TLoggerPro`** | niveles, destinos múltiples, formato configurable |
| **madExcept / EurekaLog** | informe completo de excepción no manejada (clase 141) |
| **`heaptrc`** | fugas, con la pila de cada reserva (clase 138) |

Y una técnica del mundo Delphi que anticipa la telemetría moderna y merece cerrarse aquí: **el informe
automático de fallos**.

Cuando una aplicación instalada en miles de escritorios falla, **madExcept compone un informe con la
pila simbolizada, el sistema, la versión, las variables y una captura**, y **ofrece al usuario
enviarlo**.

Y el detalle que lo hace funcionar y que conecta con la clase 144: **los símbolos de depuración se
guardan aparte y se distribuyen sin ellos**, así que el informe llega con direcciones y **se simboliza
en el lado del desarrollador**.

Eso es exactamente lo que hoy hacen los ficheros de símbolos y los mapas de fuentes, y por la misma
razón: **el binario que se distribuye no debe llevar la información que hace falta para depurarlo**.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let ((n (read)))
  (format t "log=[INFO] procesados=~D~%" n))
```

**Lo que esta clase enseña en Common Lisp.** Lisp aporta a esta clase algo que su modelo hace natural y
que la mayoría de los lenguajes necesitan mucha maquinaria para conseguir: **el registro puede ser un
objeto, no una cadena**.

```lisp
(log:info "procesados=~D" n)              ; texto, como todos
(log-evento (list :nivel :info :procesados n :duracion-ms 42))   ; DATOS
```

Y la segunda forma tiene una propiedad decisiva: **la salida se puede volver a leer**.

```lisp
(with-open-file (f "app.log" :direction :output :if-exists :append)
  (print (list :ts (get-universal-time) :nivel :info :procesados n) f))
```

**`print` produce una representación legible por `read`** (clase 104), así que **analizar el registro es
llamar a `read`**, sin analizador y sin ambigüedad.

Es el registro estructurado con treinta años de adelanto, y sale gratis por la homoiconicidad del
lenguaje.

Y el sistema de condiciones aporta la otra mitad, y es la más interesante para esta clase (clase 116):

```lisp
(handler-bind ((warning (lambda (c)
                          (log-evento (list :nivel :warn :texto (princ-to-string c)))
                          (muffle-warning c))))     ; registrar Y CONTINUAR
  (procesar-todo))
```

**`handler-bind` observa la condición sin desenrollar la pila**, así que **se puede registrar el aviso
con todo el contexto vivo y luego decidir continuar**.

En un lenguaje con solo `try`/`catch`, registrar una advertencia obliga a lanzar y capturar —perdiendo
la pila— o a devolver códigos. Aquí **el registro es un observador**, que es conceptualmente lo
correcto: **anotar no debería alterar el flujo**.

Y los marcos del ecosistema:

| Marco | Notas |
|---|---|
| **log4cl** | jerárquico por paquete y función; **se configura desde el REPL** |
| **verbose** | asíncrono, con hilos |
| **cl-syslog** | al registro del sistema |

**log4cl merece la mención final** por lo que permite hacer con el modelo de la Parte 8:

```lisp
(log:config :debug)                      ; cambiar el nivel EN MARCHA
(log:config '(mi-paquete mi-funcion) :trace)   ; de UNA función concreta
```

**Subir el nivel de detalle de una sola función en un servidor en producción, sin reiniciar**, es la
capacidad que resuelve el problema práctico de esta clase: **el detalle que hace falta para diagnosticar
es demasiado caro para dejarlo siempre encendido**.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea
set n [string trim $linea]

puts "log=\[INFO\] procesados=$n"
```

**Lo que esta clase enseña en Tcl.** Fíjate en las barras invertidas: **`\[` y `\]`**. En Tcl los
corchetes son **sustitución de comandos**, así que `[INFO]` intentaría ejecutar un comando llamado
`INFO`. Hay que escaparlos, o usar llaves.

Es un recordatorio de la clase 081: **en Tcl el texto y el código comparten sintaxis**, y esa es a la
vez su mayor virtud y su trampa más frecuente.

Y Tcl trae su registro en la distribución, con una arquitectura que merece explicarse:

```tcl
package require logger

set log [logger::init miapp]
${log}::info "procesados=$n"
${log}::debug "detalle interno"
${log}::setlevel warn                 ;# cambiar el nivel en marcha

# y jerárquico:
set log2 [logger::init miapp::red]     ;# hereda de miapp
logger::setlevel miapp::red debug       ;# ...y se ajusta por separado
```

**La jerarquía por espacios de nombres** (clase 086) es lo que hace práctico el registro en un programa
grande: **`miapp::red` hereda la configuración de `miapp`**, y se puede subir el detalle de una rama sin
tocar el resto.

Es el mismo modelo de log4j y de todos sus descendientes, y en Tcl sale de una característica que ya
existía para otra cosa.

Y Tcl tiene una capacidad para esta clase que ya apareció en la clase 141 y que aquí es especialmente
útil: **instrumentar sin tocar el código**.

```tcl
trace add execution procesarPedido enter {apply {{cmd op} {
    ${::log}::info "entrada: $cmd"
}}}
trace add execution procesarPedido leave {apply {{cmd code res op} {
    ${::log}::info "salida: $res"
}}}
```

**Añadir registro a un procedimiento de una biblioteca ajena, en producción, sin recompilar y sin
tenerlo previsto.**

Y con `rename` (clase 139), lo mismo sobre cualquier comando, incluidos los del núcleo.

Es la respuesta más directa al problema real de esta clase: **el registro que hace falta es siempre el
que no se puso**. En Tcl se puede poner después.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $n = <STDIN>;
chomp $n;

print "log=[INFO] procesados=$n\n";
```

**Lo que esta clase enseña en Perl.** Perl fue durante veinte años **el lenguaje con el que se procesaban
los registros del mundo**, así que tiene una perspectiva doble: escribe registros y, sobre todo, los
lee.

Para escribir, el ecosistema:

```perl
use Log::Log4perl qw(:easy);
Log::Log4perl->easy_init($INFO);
INFO  "procesados=$n";
WARN  "reintento";
ERROR "fallo: $@";
```

**`Log::Log4perl` es un puerto fiel de log4j**, con la misma jerarquía de categorías, los mismos
niveles y **la misma configuración por fichero recargable en caliente**.

Y para el registro estructurado, que es donde va la industria:

```perl
use Log::Any qw($log);
$log->info("pedido procesado", { pedido_id => $id, ms => $t, items => $n });
```

**`Log::Any` desacopla la biblioteca del destino**: un módulo registra con `Log::Any` y **la
aplicación decide dónde va**. Es la solución al problema de que una biblioteca no debe imponer el
sistema de registro de quien la usa — el mismo papel que SLF4J en Java.

Y para leer, que es donde Perl fue insustituible:

```perl
while (<$log>) {
    next unless /\[(\w+)\]\s+(\w+)=(\S+)/;
    $conteo{$1}{$2} += $3;
}
```

**Una línea de expresión regular por formato**, y de ahí salieron **Logwatch**, **Swatch**,
**awstats**, **Nagios** y buena parte del ecosistema de monitorización de los años noventa.

Y merece cerrar con la lección que Perl aprendió por el camino difícil, y que justifica el registro
estructurado de toda esta clase:

**Analizar registros con expresiones regulares funciona hasta que el formato cambia.** Y cambia: alguien
añade un campo, o un mensaje lleva un salto de línea, o una ruta contiene un espacio. Cada cambio rompe
silenciosamente un guion que nadie vuelve a mirar.

De ahí la regla del cierre de esta clase: **registrar datos, no prosa**. Un `{"pedido":123,"ms":42}`
sobrevive a los cambios de formato; un `"Pedido 123 procesado en 42ms"` no.

Perl es el lenguaje que mejor demostró que se puede analizar cualquier cosa — y el que mejor demostró
por qué no conviene tener que hacerlo.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>

int main() {
    long long n{};
    if (!(std::cin >> n)) return 1;

    std::cout << "log=[INFO] procesados=" << n << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** C++ plantea esta clase desde el coste: **en un sistema que procesa
un millón de eventos por segundo, el registro puede ser más caro que el trabajo**.

Y de ahí las técnicas que definen el registro de alto rendimiento y que son transferibles a cualquier
lenguaje:

**Primera, comprobar el nivel antes de formatear:**

```cpp
if (logger.should_log(level::debug))
    logger.debug("estado: {}", costoso_de_formatear());
```

Y los marcos lo hacen con macros para que **ni siquiera se evalúen los argumentos**:

```cpp
SPDLOG_DEBUG("estado: {}", costoso());     // desaparece si el nivel es alto
```

**Segunda, registro asíncrono**: el hilo que trabaja **solo escribe a una cola**, y otro hilo formatea y
escribe al disco (clase 135). El coste en el camino crítico baja a unos nanosegundos.

**Y tercera, y es la más interesante: aplazar el formateo por completo.**

```cpp
// se guardan los ARGUMENTOS en binario, no el texto
LOG_BIN(EVENTO_PEDIDO, id, ms);
// y un programa aparte reconstruye el texto con la tabla de formatos
```

**Eso es *deferred formatting*, y es lo que usan las bibliotecas de baja latencia** —el trading de alta
frecuencia, sobre todo—. Registrar cuesta copiar unos bytes; el texto se compone después, fuera del
proceso.

Es exactamente la misma idea que los códigos numéricos de Ada en esta página, llegada por el camino del
rendimiento en lugar del camino del espacio.

El ecosistema:

| Biblioteca | Notas |
|---|---|
| **spdlog** | el más usado; síncrono o asíncrono, sobre `fmt` |
| **fmtlib** | formateo rápido y seguro de tipos; base de `std::format` |
| **Quill / NanoLog** | baja latencia, con formateo aplazado |
| **glog** | el de Google; veterano |
| **OpenTelemetry C++** | trazas y métricas con propagación de contexto |

Y **`std::format` (C++20) y `std::print` (C++23)** llevaron al estándar lo que `fmt` demostró:

```cpp
std::print("log=[{}] procesados={}\n", "INFO", n);
```

**Comprobación del formato en tiempo de compilación**: si los tipos no encajan con la cadena, **no
compila**.

Es el fin de una familia entera de fallos de `printf` que llevaba cincuenta años produciendo caídas y
vulnerabilidades, y llegó al estándar en 2020.

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

dcl-pi REGISTRO;
  n int(10) const;
end-pi;

dsply ('log=[INFO] procesados=' + %char(n));

*inlr = *on;
return;
```

**Lo que esta clase enseña en RPG.** Aquí está el caso que el gancho de la clase anunciaba: **en IBM i,
el registro existe sin que nadie lo pida**.

**El registro del trabajo** (clases 137 y 138) recoge **cada mensaje del sistema, con su código, su
texto, su ayuda de segundo nivel, el programa emisor, el número de sentencia y la pila de llamadas en
ese momento** — para todos los trabajos, siempre.

Y sobre eso, la plataforma tiene tres capas más que merecen conocerse porque cubren lo que en otros
sistemas requiere montar una infraestructura entera:

**Primera, las colas de mensajes como canal de registro:**

```rpgle
dcl-pr enviarMensaje extpgm('QMHSNDPM');
  ...
end-pr;
// o, más simple, con SQL:
exec sql CALL QSYS2.SEND_MESSAGE('procesados=' || :n);
```

**Un mensaje enviado a `QSYSOPR` aparece en la cola del operador**, que es donde alguien está mirando.

**Segunda, el diario de la base de datos** (clase 140), que registra **cada cambio de cada fila con
imagen anterior y posterior**, con el trabajo, el usuario y el programa. Es una auditoría completa sin
escribir código.

**Y tercera, y es la que sorprende: todo se consulta con SQL.**

```sql
SELECT * FROM TABLE(QSYS2.JOBLOG_INFO('123456/USUARIO/MIAPP'))
SELECT * FROM TABLE(QSYS2.STACK_INFO('*'))
SELECT * FROM QSYS2.ACTIVE_JOB_INFO(SUBSYSTEM_LIST_FILTER => 'QINTER')
SELECT * FROM TABLE(QSYS2.DISPLAY_JOURNAL('MIBIB', 'MIJRN'))
SELECT * FROM QSYS2.SYSTEM_STATUS_INFO
```

**Los registros, las pilas, los trabajos activos, el consumo de CPU y el diario son tablas.** Con
`WHERE`, `GROUP BY` y `JOIN`.

Es, literalmente, lo que un sistema de observabilidad moderno intenta ofrecer con una interfaz web
propia — disponible aquí con la herramienta de consulta que todo el mundo ya sabe usar.

Y merece extraer la lección general, porque es la del cierre de esta clase: **la observabilidad no es un
producto que se instala, es una propiedad del diseño del sistema**. IBM i la tiene porque decidió en
1988 que **cada objeto y cada trabajo llevarían su propia metainformación**; los sistemas que no lo
decidieron la reconstruyen después, a mucho mayor coste y peor.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 registro: procedure options(main);

    declare n fixed binary(31);

    get list (n);

    put skip list ('log=[INFO] procesados=' || trim(char(n)));

 end registro;
```

**Lo que esta clase enseña en PL/I.** PL/I comparte la infraestructura de COBOL en esta página —SMF, las
colas de mensajes, los ficheros de registro estructurados— y aporta un mecanismo del lenguaje que
encaja exactamente con lo que la observabilidad moderna busca: **instrumentación declarada y activable
por ámbito**.

```pli
 (check(saldo, contador)):
 procesar: procedure;
    ...
 end procesar;

 on check(saldo)
    put skip list ('[TRACE] saldo=', saldo, ' en ', onloc());
```

**`CHECK` dispara el manejador cada vez que la variable cambia** (clase 141), y el manejador es código
normal: puede filtrar, contar o escribir a un fichero.

Y lo que lo hace relevante para esta clase es lo que ya se dijo de `pragma Debug` en Ada: **el prefijo
se puede quitar recompilando, sin tocar el código**, así que **la instrumentación no se pudre**.

Y PL/I tiene la infraestructura de condiciones que permite registrar el contexto completo de un fallo
(clases 137 y 138):

```pli
 on error snap begin;
    put skip list ('[ERROR] codigo=', oncode(), ' en=', onloc());
    put data;                              /* TODAS las variables */
    call escribir_bitacora();
 end;
```

**`snap` añade la traza de la pila y `put data` vuelca el estado completo** — que es, exactamente, lo
que un informe de excepción moderno contiene.

Y merece cerrar con la observación sobre el formato, porque conecta con la regla del cierre de la clase:

```pli
 put file(bitacora) edit
    (fecha, hora, nivel, programa, codigo, valor)
    (a(10), a(8), a(5), a(8), f(4), f(15,2));
```

**`put edit` con formato declarado produce columnas de posición fija**, igual que COBOL en esta página.

Y esa decisión —**posiciones fijas en lugar de separadores**— tiene una virtud que se aprecia después de
años: **un registro de longitud fija se lee igual dentro de veinte años**, sin depender de que nadie
haya cambiado un delimitador ni de que un valor contenga una coma.

Es la razón por la que los archivos históricos de estos sistemas siguen siendo legibles, y es un
argumento a favor de la disciplina que esta clase defiende: **el formato del registro es una decisión a
largo plazo, y el largo plazo llega**.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
REGISTRO ; Registro con nivel -- clase 142
 read n
 write "log=[INFO] procesados=", n, !
 quit
```

**Lo que esta clase enseña en M.** M tiene, para esta clase, la respuesta más simple y una de las más
potentes de toda la página: **el registro es una escritura en la base de datos**.

```mumps
 set ^LOG($job, $horolog, $increment(^LOG("SEQ"))) = "INFO^procesados="_n
```

Y esa única línea da, sin nada más:

- **Persistencia**: es una global, está en disco.
- **Transaccionalidad**: participa en `tstart`/`tcommit` como cualquier otro dato.
- **Índice por trabajo y por tiempo**: los subíndices están ordenados (clase 095).
- **Consulta desde otro proceso, mientras el programa sigue corriendo.**
- **Y purga trivial**: `kill ^LOG(trabajoViejo)`.

**Consultarlo es recorrer con `$order`:**

```mumps
 set fecha = ""
 for  set fecha = $order(^LOG(trabajo, fecha)) quit:fecha=""  do
 . write fecha, " ", ^LOG(trabajo, fecha), !
```

Y con un índice adicional, se busca por nivel:

```mumps
 set ^LOGX("ERROR", $horolog, seq) = ""      ; índice secundario
```

**Eso es un sistema de registro indexado y consultable en unas pocas líneas**, y explica por qué los
sistemas VistA nunca necesitaron una infraestructura de registro aparte.

Y esta clase es el sitio para la advertencia más importante del cierre, porque en el dominio de M es
crítica: **M se usa en sanidad, y un registro con datos de pacientes es una historia clínica sin
control de acceso**.

```mumps
 ; ✗ NUNCA
 set ^LOG(...) = "consultado paciente "_nombre_" dni "_dni
 ; ✓ el identificador interno, y el resto por auditoría formal
 set ^LOG(...) = "consulta DFN="_dfn
```

Y VistA tiene precisamente para eso un mecanismo formal que merece nombrarse: **la auditoría de acceso
de FileMan**, que registra **quién** consultó **qué ficha** y **cuándo**, con control de acceso propio y
retención definida — separada del registro técnico.

Es la distinción que esta clase quiere dejar clara y que se aplica a cualquier sistema con datos
sensibles: **el registro técnico y la auditoría de acceso son dos cosas distintas, con dos públicos,
dos retenciones y dos niveles de protección**. Mezclarlas es el error que convierte un fichero de
diagnóstico en una brecha de datos.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| n |

n := stdin nextLine trimBoth asNumber.

Transcript show: 'log=[INFO] procesados=', n printString; cr.
```

**Lo que esta clase enseña en Smalltalk.** `Transcript` **es** el registro de Smalltalk, y es un objeto
como cualquier otro — lo que tiene una consecuencia directa: **se puede sustituir**.

```smalltalk
Transcript := MiRegistrador new.       "y todo el sistema registra donde yo diga"
```

Y el ecosistema tiene un marco moderno construido sobre esa idea, que merece explicarse porque es
distinto de todo lo demás de esta página: **Beacon**.

```smalltalk
"Emitir una SEÑAL: un OBJETO, no una cadena"
PedidoProcesadoSignal new
    pedido: unPedido;
    duracion: tiempo;
    emit.
```

**Lo que se emite es un objeto con sus campos**, no un texto. Y luego:

```smalltalk
"Los 'runners' deciden qué hacer con las señales"
logger := MemoryLogger new.       "guardar en memoria"
logger := FileLogger new.          "a un fichero"
logger := TranscriptLogger new.     "a la consola"
logger runFor: PedidoProcesadoSignal.
```

**La separación es limpia y es la que la industria acabó adoptando**: el código **emite eventos
tipados**, y la configuración decide **qué se conserva y dónde**.

Y las ventajas se ven al usarlo:

- **Se puede filtrar por clase de señal**, no por una cadena de nivel.
- **El objeto conserva sus referencias**: se puede inspeccionar el pedido, no solo su identificador.
- **Y el formateo se aplaza** al momento de escribir, o no ocurre nunca.

Eso último es lo mismo que el formateo aplazado de C++ en esta página, obtenido aquí **por ser objetos
desde el principio**.

Y Smalltalk añade lo que su modelo permite y que cierra esta clase con el mismo argumento que la 141:
**un error puede capturarse con su contexto entero**.

```smalltalk
[ self procesar ] on: Error do: [ :e |
    ErrorSignal new
        exception: e;
        context: e signalerContext copy;      "LA PILA, como objeto"
        emit ]
```

**Guardar la pila viva en el registro**, no su representación textual — y poder **abrirla en el
depurador** más tarde (clase 141).

Es el límite superior de lo que esta clase persigue: **el registro deja de ser un mensaje al futuro y
pasa a ser el estado mismo, conservado**. Y es coherente con las decisiones que Smalltalk tomó en toda
la Parte 8: **si todo es un objeto, todo se puede guardar, enviar y volver a mirar**.

---

## Y de vuelta a la clase

Lo transferible: **un registro es un mensaje al futuro, y el futuro no tendrá tu contexto**. De ahí las
tres reglas que atraviesan toda la página: registrar **datos, no prosa** —para poder buscar y agregar—;
incluir siempre **un identificador que permita unir las líneas de una misma operación**; y elegir el
nivel pensando en **quién lee y qué decidirá**. Y la regla que más caro sale ignorar: **nunca registrar
datos personales o credenciales**, porque un registro se copia, se envía y se conserva mucho más tiempo
que la base de datos que sí está protegida.

⏮️ [Volver a la clase 142](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
