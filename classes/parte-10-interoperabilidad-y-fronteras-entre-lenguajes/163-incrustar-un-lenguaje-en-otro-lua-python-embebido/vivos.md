# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 163

> [⬅️ Volver a la clase 163](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Sumar dos números como si un guion los hubiera pedido. Es el papel del lenguaje incrustado: **dejar que
el usuario de un programa escriba lógica sin recompilarlo**. Y esta página tiene el caso más grande de
la historia y casi nadie lo reconoce como tal: **el SQL embebido en COBOL es un lenguaje incrustado en
otro**, con su precompilador, sus variables compartidas y su manejo de errores — y lleva funcionando
desde 1981.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es el **lenguaje de extensión**, y estos lenguajes lo enseñan desde los dos lados.
> **Como anfitriones**: COBOL y PL/I con SQL y CICS, C++ con Lua y Python, Delphi con Pascal Script.
> **Y como incrustados**: Tcl fue diseñado exactamente para eso (clase 155), y Lisp es el lenguaje de
> extensión de Emacs, de AutoCAD y del proyecto GNU.
>
> Y aparece la pregunta que decide el diseño: **¿qué puede tocar el código incrustado?** Porque un
> lenguaje de extensión sin límites es una puerta trasera con sintaxis agradable.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: una línea `a b` (los datos que el anfitrión pasa al script) → stdout: `resultado=<a+b>` (lo que el script calcula)
- **Regla:** `el script embebido evalúa a + b`

| stdin | esperado |
|---|---|
| `3 4` | `resultado=7` |
| `10 5` | `resultado=15` |
| `0 0` | `resultado=0` |

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
PROGRAM-ID. INCRUST.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(40).
01  C-A     PIC X(15).
01  C-B     PIC X(15).
01  A       PIC S9(9) COMP.
01  B       PIC S9(9) COMP.
01  ED      PIC -(8)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    UNSTRING LINEA DELIMITED BY ALL SPACES
        INTO C-A C-B
    END-UNSTRING

    COMPUTE A = FUNCTION NUMVAL(C-A)
    COMPUTE B = FUNCTION NUMVAL(C-B)

    COMPUTE A = A + B
    MOVE A TO ED
    DISPLAY "resultado=" FUNCTION TRIM(ED)
    STOP RUN.
```

**Lo que esta clase enseña en COBOL.** Aquí está el caso del gancho, y merece mirarlo con los ojos de
esta clase porque cambia la perspectiva: **`EXEC SQL` es un lenguaje incrustado en otro, con todo lo que
eso implica**.

```cobol
           EXEC SQL
               SELECT NOMBRE, SALDO
                 INTO :WS-NOMBRE, :WS-SALDO
                 FROM CLIENTES
                WHERE ID = :WS-ID
           END-EXEC

           IF SQLCODE NOT = 0
               PERFORM ERROR-BD
           END-IF
```

Y las cuatro decisiones del cierre de esta clase están todas ahí, resueltas hace cuarenta años:

**Qué se comparte: las variables de host.** El `:WS-NOMBRE` es una variable COBOL a la que SQL puede
escribir. **La frontera está declarada campo a campo**, no abierta.

**Cómo llegan los errores: `SQLCA`.**

```cobol
       01  SQLCA.
           05  SQLCODE   PIC S9(9) COMP.
           05  SQLERRM   PIC X(70).
           05  SQLSTATE  PIC X(5).
```

**Una estructura compartida donde el lenguaje incrustado deja el resultado**, que el anfitrión comprueba.
Es códigos de retorno, no excepciones — coherente con COBOL.

**Cómo se ejecuta: el precompilador** (clase 155). El `EXEC SQL` se sustituye por llamadas antes de
compilar, así que **el coste en ejecución es una llamada normal**.

**Y quién puede escribirlo: cualquiera que toque el fuente** — con la salvedad decisiva de que **el SQL
estático se fija en el `BIND`** (clase 137), así que **el plan de acceso y los permisos se comprueban al
desplegar, no al ejecutar**.

Y merece la comparación que esta clase quiere dejar clara:

| Aspecto | SQL **estático** embebido | SQL **dinámico** |
|---|---|---|
| Cuándo se analiza | **al compilar y en el `BIND`** | en ejecución |
| Plan de acceso | **fijo y revisable** | recalculado |
| Permisos | **del plan, no del usuario** | del usuario |
| Inyección | **imposible** | posible (clase 153) |
| Flexibilidad | ninguna | total |

**La fila de la inyección es la que importa**: el SQL estático **no puede sufrir inyección porque la
consulta no se construye** — y ese es el motivo por el que el mundo COBOL, que tiene sesenta años y mala
fama, tiene notablemente pocas vulnerabilidades de este tipo.

Es la mejor ilustración del cierre de esta clase: **acotar lo que el lenguaje incrustado puede hacer no
es una limitación — es la característica**.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program incrust
   implicit none
   integer :: a, b

   read(*, *) a, b

   write(*, '(A,I0)') 'resultado=', a + b
end program incrust
```

**Lo que esta clase enseña en Fortran.** El cálculo científico tiene un problema que esta clase resuelve
y que merece nombrarse porque es universal en el dominio: **el fichero de entrada que quiere ser un
programa**.

```text
&PARAMETROS
  n_celdas   = 1000
  dt         = 0.001
  modelo     = 'turbulento'
  viscosidad = 1.5e-5
/
```

**Eso es un `namelist` de Fortran**, y es el mecanismo estándar del lenguaje para leer configuración
—cómodo y limitado—.

Y el problema aparece en cuanto alguien pide algo así:

```text
"Quiero que la viscosidad dependa de la temperatura."
"Quiero parar cuando el residuo baje de 1e-6 O cuando pasen 1000 pasos."
"Quiero una condición de contorno distinta en la mitad izquierda."
```

**Cada una de esas peticiones, implementada como opción, añade un parámetro al `namelist` y un `if` al
código** — y en veinte años el programa tiene doscientos parámetros y nadie sabe qué combinaciones
funcionan.

**La alternativa es incrustar un lenguaje**, y la comunidad lo hace:

| Solución | Cómo |
|---|---|
| **Lua incrustado** | ligero, rápido, con `iso_c_binding` sobre la API de C (clase 156) |
| **Python incrustado** | `Py_Initialize` desde C; potente y pesado |
| **Fortran + f2py, al revés** | **Python es el anfitrión y Fortran la biblioteca** (clase 155) |
| **YAML/TOML con expresiones** | un lenguaje mínimo propio, evaluado |

**Y la última fila merece la advertencia**, porque es la tentación habitual y casi siempre sale mal:
**inventar un lenguajito propio para las expresiones del fichero de configuración**.

Empieza con `a + b`, sigue con condicionales, luego con variables, y acaba siendo **un lenguaje de
programación mal diseñado, sin documentación, sin depurador y sin nadie que lo mantenga**.

Es exactamente el problema que Ousterhout describió al crear Tcl (clase 155) —**cada herramienta
inventaba su propio lenguaje de comandos, malo y distinto**— y la respuesta sigue siendo la misma:
**incrustar uno que ya existe**.

Y la opción dominante hoy en este dominio es la tercera fila, y merece señalarlo: **invertir la
relación**. En lugar de que Fortran incruste un intérprete, **Python es el programa principal y llama a
Fortran** — con lo que la configuración, la lógica de control y las gráficas están en un lenguaje de
verdad, y el cálculo en el que sabe hacerlo.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;
with Ada.Strings;
with Ada.Strings.Fixed;

procedure Incrust is
   A, B : Integer;
begin
   Get (A);
   Get (B);

   Put_Line ("resultado=" &
             Ada.Strings.Fixed.Trim (Integer'Image (A + B), Ada.Strings.Both));
end Incrust;
```

**Lo que esta clase enseña en Ada.** Ada tiene con esta clase una relación tensa que merece explicarse,
porque ilustra bien el compromiso: **incrustar un lenguaje interpretado destruye las garantías que Ada
existe para dar**.

```text
Ada garantiza:
  - que el consumo de memoria está acotado (sin reserva dinámica)
  - que el peor caso de ejecución se puede calcular (clase 152)
  - que las comprobaciones de tipo y de rango se hacen
  - y que se puede DEMOSTRAR la ausencia de errores (clase 118)

Un intérprete incrustado destruye las cuatro:
  reserva memoria, tarda lo que tarde, y ejecuta lo que le den.
```

**Así que en un sistema certificado, incrustar un lenguaje simplemente no se hace.**

Y merece señalar qué se hace en su lugar, porque es una solución de ingeniería interesante: **tablas de
configuración con dominio acotado**.

```ada
type Modo is (Reposo, Crucero, Aterrizaje);
type Parametros is record
   Ganancia : Float range 0.0 .. 10.0;
   Umbral   : Float range -1.0 .. 1.0;
   Retardo  : Duration range 0.0 .. 1.0;
end record;
```

**La configuración es un dato con tipos y rangos declarados** (clase 153), así que **cualquier valor
inválido se rechaza al cargarlo** y **el conjunto de comportamientos posibles es finito y analizable**.

Es la respuesta correcta a la pregunta del "por qué" de esta clase —**¿qué puede tocar el código
incrustado?**— llevada al extremo: **no hay código incrustado; hay parámetros con dominio**.

Y en el otro lado, **donde Ada sí participa de esta clase es en las herramientas y en el suelo**:

| Caso | Cómo |
|---|---|
| **Ada como anfitrión, fuera de lo crítico** | enlaces a Lua o Python para herramientas de tierra |
| **Ada como el código generado** | de Simulink o SCADE (clase 155): **el modelo es el lenguaje alto** |
| **Ada bajo un intérprete** | escribir la máquina virtual de otro lenguaje en Ada |

**La fila del medio es la importante y merece cerrar con ella**: en aviación y automoción, **el
"lenguaje incrustado" existe y es un modelo gráfico** —bloques, máquinas de estados, ecuaciones— **del
que se genera Ada o C**.

Y eso da lo que esta clase busca —**que alguien que no es programador exprese la lógica**— **sin perder
las garantías**, porque el generador es parte de la cadena cualificada (clase 144) y **el resultado se
analiza como cualquier otro código**.

Es una solución cara y es la única que satisface las dos exigencias a la vez.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Incrust;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  A, B: Integer;

begin
  Read(A, B);
  WriteLn('resultado=', IntToStr(A + B));
end.
```

**Lo que esta clase enseña en Pascal.** El mundo Delphi tiene una tradición de lenguajes incrustados
inusualmente rica, y por una razón de negocio muy concreta: **su público hacía aplicaciones que se
vendían a muchos clientes, y cada cliente quería algo distinto**.

Y la respuesta fue **incrustar un intérprete de Pascal dentro de la aplicación escrita en Pascal**:

```pascal
uses uPSCompiler, uPSRuntime;      { Pascal Script, de RemObjects }

Script.Script.Text :=
  'function Calcular(A, B: Integer): Integer;' + LineEnding +
  'begin' + LineEnding +
  '  Result := A + B;' + LineEnding +
  'end;';

Script.Compile;
Script.Execute;
```

**El cliente escribe sus reglas en el mismo lenguaje que la aplicación**, sin compilador y sin
redesplegar.

Y merece enumerar las opciones del ecosistema porque son varias y buenas:

| Motor | Notas |
|---|---|
| **Pascal Script (RemObjects)** | subconjunto de Object Pascal; libre y muy usado |
| **DWScript** | Delphi Web Script: más completo, con clases y genéricos |
| **FastScript / TMS Scripter** | comerciales; varios lenguajes |
| **Lua para Delphi** | cuando se prefiere un lenguaje distinto |
| **Python4Delphi** | Python completo dentro de la aplicación |

Y **el caso de uso dominante merece nombrarse porque explica la inversión**: **los informes y las reglas
de negocio**.

```text
FastReport, QuickReport y ReportBuilder incrustan un intérprete
para que el usuario final escriba expresiones en los informes:
   [Total] * 1.21
   IIF([Saldo] < 0, 'DEUDOR', 'AL CORRIENTE')
```

**Millones de informes de empresa contienen pequeños trozos de código escritos por gente de
administración**, y funcionan porque el motor está incrustado.

Y las cuatro decisiones del cierre de esta clase aparecen aquí con toda claridad, y Pascal Script las
resuelve bien:

```pascal
{ QUÉ se expone: hay que registrar EXPLÍCITAMENTE cada función y cada clase }
Compiler.AddDelphiFunction('function Redondear(X: Double): Integer');
RegisterClass_TCliente(Runtime);

{ LÍMITES: contador de instrucciones para cortar bucles infinitos }
Exec.OnRunLine := @ComprobarTiempoLimite;

{ ERRORES: el script lanza excepciones que el anfitrión captura }
try Script.Execute except on E: Exception do MostrarError(E) end;
```

**"Hay que registrar explícitamente cada función" es la propiedad clave**: **el guion no ve nada por
defecto** — que es exactamente el modelo de capacidades de la clase 153 y del cierre de esta.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let ((a (read))
      (b (read)))
  (format t "resultado=~D~%" (+ a b)))
```

**Lo que esta clase enseña en Common Lisp.** Lisp es, probablemente, **el lenguaje incrustado con más
usuarios de la historia**, y merece contar por qué: **Emacs**.

```elisp
;; Emacs Lisp: el editor es un intérprete de Lisp con un núcleo en C
(defun mi-comando ()
  (interactive)
  (insert (format "Hoy es %s" (current-time-string))))

(global-set-key (kbd "C-c d") 'mi-comando)
```

**Emacs no es un editor con complementos: es un intérprete de Lisp que resulta que edita texto.** El
90 % de su funcionalidad —los modos, el correo, el cliente de git, el gestor de ficheros— **está escrito
en Emacs Lisp** y es modificable en marcha.

Es la arquitectura de dos lenguajes de la clase 149 llevada al extremo: **un núcleo pequeño en C y todo
lo demás arriba**.

Y hay más casos, y merecen nombrarse porque son enormes:

| Aplicación | Lenguaje incrustado |
|---|---|
| **Emacs** | Emacs Lisp |
| **AutoCAD** | **AutoLISP**, desde 1986 |
| **GIMP** | Script-Fu (Scheme) |
| **GNU Guile** | **el lenguaje de extensión OFICIAL del proyecto GNU** |
| **Sawfish, StumpWM** | Lisp como configuración de escritorio |
| **Nyxt** | navegador web programable en Common Lisp |

**AutoLISP merece la mención** porque es el ejemplo más masivo fuera del software libre: **decenas de
miles de despachos de arquitectura e ingeniería tienen rutinas de AutoLISP escritas a lo largo de treinta
años**, y ese código es un activo real que ata a la herramienta.

Y merece preguntarse por qué Lisp acabó en tantos sitios como lenguaje de extensión, porque las razones
son técnicas y buenas:

**Una, el intérprete es pequeño.** Un evaluador de Lisp básico son unos cientos de líneas (clase 123).

**Dos, no hay que escribir un analizador.** La sintaxis de paréntesis **es el árbol**, así que **leer un
guion es leer datos**.

**Tres, las macros permiten que el anfitrión defina el vocabulario del dominio** (clase 149), así que el
usuario no escribe Lisp genérico: escribe algo que se parece a su problema.

**Y cuatro, se puede modificar en marcha**, que es lo que hace de Emacs lo que es.

Y el cierre de esta clase aplicado a Lisp trae una advertencia real: **`eval` sobre lo que escriba el
usuario es todo el poder del anfitrión** (clase 153). Emacs lo asume —tu configuración eres tú— pero **un
producto que ejecute guiones de terceros necesita un intérprete restringido**, y ahí Lisp no tiene una
respuesta tan buena como Safe-Tcl.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea
lassign [string trim $linea] a b

puts "resultado=[expr {$a + $b}]"
```

**Lo que esta clase enseña en Tcl.** Tcl **es** esta clase: fue diseñado, en 1988, para ser el lenguaje
incrustado que a todo el mundo le faltaba (clase 155).

```c
/* Incrustar Tcl en cualquier programa de C: */
Tcl_Interp *interp = Tcl_CreateInterp();
Tcl_Init(interp);

/* Exponer SOLO lo que este programa quiere ofrecer */
Tcl_CreateObjCommand(interp, "dibujar", DibujarCmd, NULL, NULL);
Tcl_CreateObjCommand(interp, "medir",   MedirCmd,   NULL, NULL);

/* Y ejecutar el guion del usuario */
if (Tcl_EvalFile(interp, "config.tcl") != TCL_OK)
    fprintf(stderr, "%s\n", Tcl_GetStringResult(interp));
```

Y las cuatro decisiones del cierre de esta clase tienen respuesta directa en Tcl, y merece verlas juntas
porque es el conjunto más completo de esta página:

**Qué se expone**: `Tcl_CreateObjCommand`, uno a uno. **Y con un intérprete seguro, ni siquiera hay
`open` ni `exec`** (clase 153).

```tcl
set i [interp create -safe]
$i alias dibujar ::miDibujarControlado      ;# la única puerta
```

**Los límites de recursos**:

```c
Tcl_LimitSetCommands(interp, 100000);       /* máximo de comandos ejecutados */
Tcl_LimitSetTime(interp, &tiempoLimite);     /* y de tiempo de reloj */
```

**Tcl tiene límites de ejecución en la API**, así que **un bucle infinito del usuario se corta** — que es
la segunda decisión del cierre, resuelta por la biblioteca en lugar de a mano.

**Los errores**: un guion que falla devuelve `TCL_ERROR` con el mensaje y la traza (clase 137), y **el
anfitrión decide qué hacer**. No tumba el proceso.

**Y quién escribe**: con intérpretes seguros y alias, **se puede ejecutar código de terceros no
confiables**, que era el caso de uso original de Safe-Tcl —código que llegaba por correo—.

Y merece cerrar con el reconocimiento que esta clase permite hacer: **la lista de programas que
incrustan Tcl es larga y poco conocida**.

```text
Las herramientas de diseño de circuitos de Synopsys, Cadence, Xilinx, Mentor
Cisco IOS (durante años), F5 BIG-IP (con iRules)
AOLserver, Expect, y una parte de la infraestructura de telecomunicaciones
```

**Y en todas, el lenguaje incrustado sobrevivió al programa que lo incrustaba**: los flujos de diseño
escritos en Tcl en los años noventa **siguen ejecutándose hoy** (clase 160).

Es la mejor razón para elegir un lenguaje incrustado que ya existe en lugar de inventar uno: **el código
que los usuarios escriban durará más que el producto**.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;
my ($a1, $b1) = split ' ', $linea;

print "resultado=", $a1 + $b1, "\n";
```

**Lo que esta clase enseña en Perl.** Perl se puede incrustar, y su caso mayor merece contarse porque
sostuvo buena parte de la web durante quince años: **`mod_perl`**.

```apache
<Perl>
  # Configuración de Apache... escrita en Perl
  $Location{'/privado'} = { AuthType => 'Basic', require => 'valid-user' };
</Perl>

PerlResponseHandler MiApp::Manejador
```

**`mod_perl` incrusta el intérprete de Perl DENTRO del proceso de Apache**, y eso da dos cosas:

- **El intérprete no arranca en cada petición** —a diferencia de CGI—, así que es órdenes de magnitud más
  rápido.
- **Y los manejadores de Perl tienen acceso a la API interna de Apache**: pueden intervenir en cualquier
  fase del ciclo de la petición, no solo generar la respuesta.

Y el mecanismo general:

```c
#include <EXTERN.h>
#include <perl.h>

PerlInterpreter *mi_perl = perl_alloc();
perl_construct(mi_perl);
perl_parse(mi_perl, NULL, argc, argv, NULL);
perl_run(mi_perl);
call_pv("MiModulo::procesar", G_DISCARD);
```

Y merece señalar el problema que `mod_perl` sufrió y que es la advertencia de esta clase, porque se
repite en todos los lenguajes incrustados de larga vida: **el estado persistente entre peticiones**.

```perl
# ✗ en CGI esto era inofensivo; en mod_perl, la variable SOBREVIVE
my $usuario;                      # variable de fichero
sub manejar { $usuario ||= autenticar(); ... }   # ¡el del usuario ANTERIOR!
```

**Un intérprete que persiste convierte cualquier estado global en una fuga entre peticiones** —y en
`mod_perl` eso produjo fallos de seguridad reales: sesiones cruzadas entre usuarios.

Es la tercera decisión del cierre de esta clase vista desde otro ángulo: **no solo hay que decidir qué
puede tocar el guion, sino qué queda entre ejecuciones**.

Y la respuesta que la industria adoptó y que merece extraerse: **el intérprete se reutiliza, el estado
no**. Los marcos modernos —PSGI en Perl, WSGI en Python, cualquier servidor de aplicaciones— **crean un
contexto nuevo por petición y lo destruyen al terminar**, precisamente por esto.

Y para el caso contrario —Perl como anfitrión— el ecosistema tiene lo esperable:

```perl
use Inline::Lua;                  # Lua dentro de Perl
use JavaScript::Duktape;           # JavaScript dentro de Perl
my $r = eval $codigo_del_usuario;   # ✗ y esto, nunca con datos ajenos
```

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>

int main() {
    long long a{}, b{};
    if (!(std::cin >> a >> b)) return 1;

    std::cout << "resultado=" << a + b << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** C++ es **el anfitrión por excelencia** de esta clase, y merece
dedicar el espacio al lenguaje que domina el papel de incrustado: **Lua**.

**Lua se creó en 1993 en la Universidad Católica de Río de Janeiro**, y su origen es exactamente el
problema de esta clase: **Petrobras necesitaba que sus ingenieros configuraran programas de simulación
sin recompilarlos**, y los ficheros de configuración se habían quedado cortos.

Y sus decisiones de diseño están todas orientadas a ser incrustado, y merecen enumerarse porque explican
su éxito:

| Decisión | Consecuencia |
|---|---|
| **Escrito en C ANSI puro** | compila en cualquier sitio, incluso en consolas y microcontroladores |
| **El intérprete cabe en ~200 KB** | se puede incluir en cualquier programa |
| **Sin biblioteca estándar impuesta** | el anfitrión decide qué existe |
| **Una sola estructura de datos: la tabla** | simple de aprender y de exponer |
| **Corrutinas** (clase 134) | ideal para lógica de juego y de guiones |
| **Licencia MIT** | sin fricción para uso comercial |

**La tercera fila es la del cierre de esta clase**: **un estado de Lua recién creado no tiene `io`, ni
`os`, ni nada** — el anfitrión abre las bibliotecas que quiera.

```cpp
#include <sol/sol.hpp>          // sol2: enlace moderno de Lua para C++

sol::state lua;
lua.open_libraries(sol::lib::base, sol::lib::math);   // ← SOLO estas

lua.set_function("sumar", [](int a, int b) { return a + b; });
lua.new_usertype<Personaje>("Personaje",
    "vida", &Personaje::vida,
    "mover", &Personaje::mover);

lua.script("p = Personaje.new(); p:mover(10, 0)");
```

**`sol2` merece la mención** porque usa plantillas para generar el enlace en compilación: **exponer una
clase de C++ a Lua son tres líneas y no cuesta nada en ejecución**.

Y la lista de dónde está Lua es la mejor prueba de esta clase:

```text
World of Warcraft (toda la interfaz), Roblox, Angry Birds, Garry's Mod
Redis (scripts atómicos), Nginx (OpenResty), Wireshark, VLC, Neovim
Adobe Lightroom, MediaWiki (las plantillas de Wikipedia)
```

**Los guiones de la interfaz de World of Warcraft** son un ecosistema de miles de complementos escritos
por usuarios, y **las plantillas de Wikipedia** ejecutan Lua en los servidores de Wikimedia.

Y el límite de recursos, que es la segunda decisión del cierre, Lua lo resuelve con un mecanismo elegante:

```c
lua_sethook(L, gancho, LUA_MASKCOUNT, 100000);   /* llama al gancho cada 100k instrucciones */
```

**Un gancho que se dispara cada N instrucciones** permite cortar un bucle infinito — y es lo que hace
Wikipedia para que una plantilla mal escrita no tumbe un servidor.

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

dcl-pi INCRUST;
  a int(10) const;
  b int(10) const;
end-pi;

dsply ('resultado=' + %char(a + b));

*inlr = *on;
return;
```

**Lo que esta clase enseña en RPG.** RPG comparte con COBOL el caso mayor de esta página —**el SQL
embebido**— y merece verlo aquí porque en IBM i tiene una integración especialmente estrecha:

```rpgle
exec sql
  SELECT nombre, saldo
    INTO :nombre, :saldo
    FROM clientes
   WHERE id = :idCliente;

if sqlcode <> 0;
  // manejar
endif;

// Y con cursores, para conjuntos:
exec sql DECLARE c1 CURSOR FOR
  SELECT id, importe FROM pedidos WHERE cliente = :idCliente;
exec sql OPEN c1;
dow sqlcode = 0;
  exec sql FETCH c1 INTO :id, :importe;
  ...
enddo;
```

**Y la ventaja concreta de esta plataforma es que la base de datos está dentro del sistema operativo**
(clase 139), así que **no hay servidor, ni conexión, ni controlador**: el SQL embebido llama directamente
al motor.

Y esta clase es el sitio para señalar la transición más importante que ha vivido RPG en los últimos
veinte años, y que la clase 152 ya rozó: **pasar del acceso registro a registro al SQL embebido**.

```text
El acceso nativo (READ, CHAIN, SETLL) es del lenguaje.
El SQL embebido es un lenguaje INCRUSTADO.

Y el segundo gana casi siempre, porque el optimizador decide el plan
y el bucle no puede (clase 152).
```

**Es un caso poco común: un lenguaje incrustado que sustituye a una característica nativa del
anfitrión**, y por razones de rendimiento y de expresividad.

Y el resto de lenguajes que IBM i incrusta o aloja merecen la lista, porque la plataforma es de las más
poliglotas (clase 155):

| Lenguaje | Papel |
|---|---|
| **SQL** | acceso a datos, embebido en RPG, COBOL, C y CL |
| **CL** | **el lenguaje de control**: orquestación, como el JCL de z/OS |
| **Python, Node, PHP** | en PASE, para la capa web y las herramientas |
| **Java** | dentro del mismo trabajo (clase 156) |
| **`QCMDEXC`** | **ejecutar un comando del sistema desde un programa** |

**`QCMDEXC` merece la advertencia final**, porque es la puerta que el cierre de esta clase señala:

```rpgle
callp qcmdexc('DLTF FILE(' + %trim(entrada) + ')' : 30);   // ✗ inyección de comandos
```

**Es la inyección de la clase 153, con comandos de sistema en lugar de SQL** — y con `USRPRF(*OWNER)`
(clase 153), **con los permisos del propietario del programa**.

Es la misma lección: **un lenguaje incrustado al que se le pasa entrada del usuario sin validar es
ejecución remota de código**.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 incrust: procedure options(main);

    declare (a, b) fixed binary(31);

    get list (a, b);

    put skip list ('resultado=' || trim(char(a + b)));

 end incrust;
```

**Lo que esta clase enseña en PL/I.** PL/I comparte con COBOL el caso del gancho, y merece añadir la
perspectiva histórica: **el mainframe inventó el patrón del lenguaje incrustado con precompilador**, y lo
usó para más de una cosa a la vez.

```pli
 exec sql SELECT saldo INTO :ws_saldo FROM cuentas WHERE id = :ws_id;
 exec cics send map('PANT1') mapset('MAPAS');
 exec dli get unique segment(cliente);        /* IMS: otra base de datos */
```

**Tres lenguajes incrustados en un programa**, cada uno con su precompilador, y todos comparten las
variables del programa anfitrión.

Y esa arquitectura —**marcas en el fuente que un preprocesador convierte en llamadas**— es la que hoy
usan, con otros nombres:

| Hoy | Equivale a |
|---|---|
| **Consultas comprobadas en compilación** (sqlc, jOOQ, Diesel) | el precompilador SQL |
| **JSX y las plantillas compiladas** | el traductor CICS |
| **Las macros procedurales** de Rust | el preprocesador con acceso al árbol |
| **Los generadores de cliente** desde OpenAPI (clase 160) | los generadores de stubs |

**Y la propiedad que todos comparten es la que esta clase quiere destacar: el lenguaje incrustado se
comprueba antes de ejecutar.**

Es la diferencia entre `EXEC SQL` estático —la consulta se valida contra el catálogo en el `BIND`— y una
cadena SQL construida en ejecución.

Y PL/I tiene además su propio lenguaje incrustado, y es del propio lenguaje: **el preprocesador**.

```pli
 %declare depurar character;
 %depurar = 'si';

 %if depurar = 'si' %then
    %do;
       put skip list ('traza: ', x);
    %end;
 %end;
```

**El preprocesador de PL/I es un lenguaje completo** —con variables, condicionales, bucles y
procedimientos— **que se ejecuta en tiempo de compilación y genera código PL/I**.

Es exactamente lo que la clase 123 llamaba metaprogramación, y **es de 1964**: mucho antes que las
plantillas de C++ y las macros de Rust, y con la misma tensión que la clase 123 señalaba — **potentísimo
y capaz de hacer el programa ilegible**.

Y por eso los estándares de instalación (clase 146) solían restringirlo severamente: **un programa cuyo
significado depende de un preprocesador programable es un programa que no se puede leer**.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
INCRUST ; Suma pedida por un guion -- clase 163
 read linea
 new a, b
 set a = $piece(linea, " ", 1)
 set b = $piece(linea, " ", 2)
 write "resultado=", a + b, !
 quit
```

**Lo que esta clase enseña en M.** M es, de todos los de esta página, **el que más lejos lleva la idea de
esta clase — y el que peor la acota**.

Porque en M **el lenguaje incrustado es M mismo** (clase 151):

```mumps
 xecute codigo                    ; ejecutar una cadena
 do @(rutina_"^"_paquete)          ; llamada indirecta
 set valor = @expresion             ; evaluar una expresión guardada
```

Y en VistA eso es una arquitectura, no una anécdota: **el diccionario de datos de FileMan guarda código M
en los campos** (clase 149).

```text
Campo "EDAD" del fichero PACIENTE:
   Tipo:              calculado
   Expresión MUMPS:   $$FMDIFF^XLFDT(DT, FECHA_NACIMIENTO)\365.25

Campo "PESO":
   Verificación de entrada:  I X<0!(X>500) W "!!Peso fuera de rango" K X
```

**Ese código lo escribe el personal técnico del hospital, no el fabricante**, y se ejecuta cuando alguien
edita la ficha.

Y merece reconocer lo que eso resuelve, porque es exactamente lo que esta clase busca: **cada hospital
puede añadir sus validaciones, sus campos calculados y sus alertas sin tocar el sistema**.

**Y las cuatro decisiones del cierre de esta clase no están tomadas:**

| Decisión | En FileMan |
|---|---|
| **Qué se expone** | **todo**: es M completo, con acceso a cualquier global |
| **Límites de recursos** | ninguno: un bucle infinito cuelga el proceso |
| **Errores** | `$etrap` global, si alguien lo puso (clase 137) |
| **Quién puede escribir** | quien tenga permiso sobre el diccionario |

**Y la única defensa real es la cuarta**, con permisos muy restringidos y un proceso de aprobación
formal — un control organizativo donde otros ecosistemas ponen uno técnico (clase 153).

Y merece cerrar con la valoración justa, porque es fácil ser injusto con esto: **la decisión fue
razonable en su contexto**. En 1979, **no existía la noción de intérprete restringido**, y la alternativa
—que cada cambio clínico requiriera un ciclo de desarrollo del fabricante— **habría hecho el sistema
inservible en un hospital**.

Es la misma lección que la clase 154 dejaba: **una decisión correcta cuyo contexto cambió**. Hoy existen
mecanismos —módulos WebAssembly aislados (clase 162), intérpretes restringidos, límites de recursos— que
darían la misma flexibilidad con garantías, y la migración a ellos es una de las deudas técnicas más
grandes de este ecosistema.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| linea partes a b |

linea := stdin nextLine trimBoth.
partes := linea substrings: ' '.

a := (partes at: 1) asNumber.
b := (partes at: 2) asNumber.

Transcript show: 'resultado=', (a + b) printString; cr.
```

**Lo que esta clase enseña en Smalltalk.** Smalltalk tiene con esta clase una relación peculiar y que
merece explicarse: **no necesita incrustar un lenguaje, porque él mismo es el lenguaje de extensión de
sus aplicaciones**.

```smalltalk
"El usuario de una aplicación Smalltalk puede, si se le permite:"
Compiler evaluate: 'pedido total * 1.21'.

"O escribir un método nuevo, en marcha, sobre una clase existente:"
Pedido compile: 'descuentoEspecial ^ self total * 0.15'.
```

**En Smalltalk no hay frontera entre "la aplicación" y "los guiones del usuario"** — es todo el mismo
sistema vivo (Parte 8).

Y eso es a la vez su mayor virtud y el problema del cierre de esta clase: **el poder es total y por
defecto**.

Y merece contar dos casos donde eso se explotó bien:

**Uno, los entornos de fin de usuario.** Smalltalk se diseñó en Xerox PARC **para que personas que no
eran programadores construyeran sus propias herramientas**, y de ahí salió la línea que llega hasta
**Scratch** —el lenguaje visual de bloques del MIT para enseñar a programar a niños— que **está
implementado sobre Squeak**.

**Scratch es un lenguaje incrustado en un entorno Smalltalk**, y es probablemente el lenguaje de
programación con más usuarios nuevos cada año del mundo.

**Y dos, los sistemas de negocio configurables**: aplicaciones financieras y de seguros construidas en
Smalltalk donde **las reglas de tarificación las escriben los actuarios**, en Smalltalk, sobre el sistema
vivo.

Y las defensas para acotar eso, que es lo que esta clase pide, existen:

```smalltalk
"Entornos restringidos: el guion solo ve las clases que se le importan"
| entorno |
entorno := Environment new.
entorno importSelf; import: Kernel; import: MiDominio.
```

```smalltalk
"Límite de tiempo: el proceso se mata si tarda demasiado"
[ self evaluarGuion ] valueWithin: 2 seconds onTimeout: [ self abortar ]
```

**`valueWithin:onTimeout:` merece la mención** porque resuelve la segunda decisión del cierre de forma
idiomática: **cualquier bloque puede ejecutarse con un plazo**, y si lo supera, se interrumpe.

Y merece cerrar la clase, y con ella el bloque de interoperabilidad, con la observación que la página
entera sostiene: **incrustar un lenguaje es siempre la misma operación** —dar al usuario poder de
cómputo— **y siempre plantea las mismas cuatro preguntas**.

Los sistemas que las respondieron —Safe-Tcl con capacidades, Lua con bibliotecas opcionales y ganchos,
Pascal Script con registro explícito— **son los que hoy se pueden usar con código de terceros**. Los que
no —FileMan, `eval` a secas, el diccionario con código— **funcionan porque se confía en quien escribe**,
y esa confianza es una decisión de arquitectura aunque nadie la tomara conscientemente.

---

## Y de vuelta a la clase

Lo transferible: **incrustar un lenguaje es dar poder a quien no puede recompilar, y eso hay que
acotarlo desde el principio**. Las cuatro decisiones son siempre las mismas: **qué API se expone** —
poco y concreto, no "todo"—; **qué límites de recursos hay** —tiempo y memoria, porque un bucle infinito
del usuario no puede colgar el programa—; **qué pasa con los errores** —tienen que llegar como errores
del anfitrión, no tumbar el proceso—; y **quién puede escribir esos guiones**, porque en la práctica es
ejecución de código con los permisos del programa.

⏮️ [Volver a la clase 163](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
