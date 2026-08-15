# -*- coding: utf-8 -*-
"""Parte 10, lote D — clases 163 y 164. Ver `vivos_parte10.py` y `gen_vivos.py`."""

SPECS: dict[str, dict] = {}

# ---------------------------------------------------------------------------
# 163 — Incrustar un lenguaje en otro
# ---------------------------------------------------------------------------
SPECS["163"] = dict(
    gancho="""
Sumar dos números como si un guion los hubiera pedido. Es el papel del lenguaje incrustado: **dejar que
el usuario de un programa escriba lógica sin recompilarlo**. Y esta página tiene el caso más grande de
la historia y casi nadie lo reconoce como tal: **el SQL embebido en COBOL es un lenguaje incrustado en
otro**, con su precompilador, sus variables compartidas y su manejo de errores — y lleva funcionando
desde 1981.
""",
    porque="""
Aquí el concepto es el **lenguaje de extensión**, y estos lenguajes lo enseñan desde los dos lados.
**Como anfitriones**: COBOL y PL/I con SQL y CICS, C++ con Lua y Python, Delphi con Pascal Script.
**Y como incrustados**: Tcl fue diseñado exactamente para eso (clase 155), y Lisp es el lenguaje de
extensión de Emacs, de AutoCAD y del proyecto GNU.

Y aparece la pregunta que decide el diseño: **¿qué puede tocar el código incrustado?** Porque un
lenguaje de extensión sin límites es una puerta trasera con sintaxis agradable.
""",
    cierre="""
Lo transferible: **incrustar un lenguaje es dar poder a quien no puede recompilar, y eso hay que
acotarlo desde el principio**. Las cuatro decisiones son siempre las mismas: **qué API se expone** —
poco y concreto, no "todo"—; **qué límites de recursos hay** —tiempo y memoria, porque un bucle infinito
del usuario no puede colgar el programa—; **qué pasa con los errores** —tienen que llegar como errores
del anfitrión, no tumbar el proceso—; y **quién puede escribir esos guiones**, porque en la práctica es
ejecución de código con los permisos del programa.
""",
    langs={
        "cobol": ("""
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
""", """
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
"""),
        "fortran": ("""
program incrust
   implicit none
   integer :: a, b

   read(*, *) a, b

   write(*, '(A,I0)') 'resultado=', a + b
end program incrust
""", """
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
"""),
        "ada": ("""
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
""", """
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
"""),
        "pascal": ("""
program Incrust;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  A, B: Integer;

begin
  Read(A, B);
  WriteLn('resultado=', IntToStr(A + B));
end.
""", """
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
"""),
        "lisp": ("""
(let ((a (read))
      (b (read)))
  (format t "resultado=~D~%" (+ a b)))
""", """
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
"""),
        "tcl": ("""
gets stdin linea
lassign [string trim $linea] a b

puts "resultado=[expr {$a + $b}]"
""", """
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
    fprintf(stderr, "%s\\n", Tcl_GetStringResult(interp));
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
"""),
        "perl": ("""
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;
my ($a1, $b1) = split ' ', $linea;

print "resultado=", $a1 + $b1, "\\n";
""", """
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
"""),
        "cpp": ("""
#include <iostream>

int main() {
    long long a{}, b{};
    if (!(std::cin >> a >> b)) return 1;

    std::cout << "resultado=" << a + b << '\\n';
    return 0;
}
""", """
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
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi INCRUST;
  a int(10) const;
  b int(10) const;
end-pi;

dsply ('resultado=' + %char(a + b));

*inlr = *on;
return;
""", """
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
"""),
        "pli": ("""
 incrust: procedure options(main);

    declare (a, b) fixed binary(31);

    get list (a, b);

    put skip list ('resultado=' || trim(char(a + b)));

 end incrust;
""", """
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

Es exactamente lo que la clase 122 llamaba metaprogramación, y **es de 1964**: mucho antes que las
plantillas de C++ y las macros de Rust, y con la misma tensión que la clase 122 señalaba — **potentísimo
y capaz de hacer el programa ilegible**.

Y por eso los estándares de instalación (clase 146) solían restringirlo severamente: **un programa cuyo
significado depende de un preprocesador programable es un programa que no se puede leer**.
"""),
        "mumps": ("""
INCRUST ; Suma pedida por un guion -- clase 163
 read linea
 new a, b
 set a = $piece(linea, " ", 1)
 set b = $piece(linea, " ", 2)
 write "resultado=", a + b, !
 quit
""", """
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
   Expresión MUMPS:   $$FMDIFF^XLFDT(DT, FECHA_NACIMIENTO)\\365.25

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
"""),
        "smalltalk": ("""
| linea partes a b |

linea := stdin nextLine trimBoth.
partes := linea substrings: ' '.

a := (partes at: 1) asNumber.
b := (partes at: 2) asNumber.

Transcript show: 'resultado=', (a + b) printString; cr.
""", """
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
"""),
    },
)

# ---------------------------------------------------------------------------
# 164 — Elegir el lenguaje correcto para cada componente
# ---------------------------------------------------------------------------
SPECS["164"] = dict(
    gancho="""
Un dominio, un lenguaje: `sistemas → Rust`, `web → TypeScript`, `datos → SQL`. Es una simplificación
deliberada, porque esta clase cierra la Parte 10 con la pregunta más incómoda de todo el curso: **¿y
estos doce, cuándo se elegirían hoy?** Y la respuesta honesta —que cada apartado de esta página da— es
más interesante que un ranking: **varios se siguen eligiendo, con razones sólidas; otros no se eligen y
se heredan; y saber la diferencia es lo que separa una decisión de una inercia.**
""",
    porque="""
Aquí el concepto es la **decisión tecnológica**, y estos lenguajes la enseñan mejor que ninguno porque
**llevan décadas siendo elegidos o no elegidos**, y las razones están documentadas por los hechos. Y
aportan lo que a esta discusión le suele faltar: **el largo plazo**. Un lenguaje elegido hoy tendrá que
mantenerse en 2045, con otro equipo, otro hardware y otras herramientas — y varios de esta página son la
única evidencia empírica que existe sobre qué pasa entonces.

Y aparece el criterio que casi nunca está en las comparativas: **¿quién va a mantener esto, y estará?**
""",
    cierre="""
Lo transferible: **la elección de lenguaje casi nunca la decide el lenguaje**. La deciden el ecosistema
—las bibliotecas que ya existen para tu problema—, el equipo —lo que sabe y lo que puede contratar—, la
integración —con qué tiene que hablar— y el horizonte —cuántos años vivirá esto—. El rendimiento y la
elegancia importan mucho menos de lo que las discusiones sugieren, salvo en los pocos casos en que son el
requisito. Y la regla que más disgustos evita: **elegir el lenguaje aburrido para el 90 % del sistema y
reservar el interesante para el 10 % que lo justifica** — que es, exactamente, la arquitectura poliglota
de toda esta parte.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. ELEGIR.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  DOMINIO PIC X(20).
01  LENG    PIC X(20).

PROCEDURE DIVISION.
    ACCEPT DOMINIO

    EVALUATE FUNCTION TRIM(DOMINIO)
        WHEN "sistemas" MOVE "Rust"       TO LENG
        WHEN "web"      MOVE "TypeScript" TO LENG
        WHEN "datos"    MOVE "SQL"        TO LENG
        WHEN OTHER      MOVE "?"          TO LENG
    END-EVALUATE

    DISPLAY "lenguaje=" FUNCTION TRIM(LENG)
    STOP RUN.
""", """
**¿Cuándo se elige COBOL hoy?** La respuesta honesta: **casi nunca para un sistema nuevo, y con muy buenas
razones para no reescribir el existente.**

**Por qué no para lo nuevo:**

- **El ecosistema no está**: no hay bibliotecas para JSON moderno, criptografía, HTTP o nube sin recurrir
  a otros lenguajes.
- **La contratación es un problema real** (clase 154), y empeora cada año.
- **Y las herramientas** —editores, análisis, dependencias— están décadas por detrás.

**Y por qué sí para lo que ya existe, que es el argumento que casi nadie escucha:**

```text
- 200.000-800.000 millones de líneas en producción
- Ejecutando el 43 % de los sistemas bancarios
- Con una fiabilidad medida en décadas
- Y una lógica de negocio que NO ESTÁ DOCUMENTADA en ninguna otra parte (clase 154)
```

**Las reescrituras de sistemas COBOL fracasan con una frecuencia bien documentada** (clase 150), y el
motivo no es técnico: **es que el comportamiento real del sistema viejo, con sus treinta años de casos
particulares, no está escrito en ningún sitio salvo en su código**.

Y donde COBOL sigue siendo **objetivamente bueno** merece decirse, porque suele omitirse:

| Fortaleza | Por qué |
|---|---|
| **Aritmética decimal exacta** | `COMP-3` y `PIC S9(9)V99` (clase 072): sin sorpresas de redondeo |
| **Procesamiento de lotes enormes** | el modelo de fichero y el `SORT` son insuperables (clase 152) |
| **Legibilidad para no programadores** | un analista de negocio puede leer la regla |
| **Estabilidad** | código de 1985 compila hoy |

**La primera es una ventaja real sobre la mayoría de los lenguajes modernos**, donde el decimal exacto
requiere una biblioteca y disciplina.

Y la estrategia sensata para un sistema COBOL, que es la de toda esta parte: **no reescribir, exponer**
(clases 149 y 160). La lógica se queda donde funciona; lo nuevo se escribe fuera y habla con ella por una
frontera bien definida.
"""),
        "fortran": ("""
program elegir
   implicit none
   character(len=20) :: dominio, lenguaje

   read(*, '(A)') dominio
   dominio = adjustl(dominio)

   select case (trim(dominio))
   case ('sistemas'); lenguaje = 'Rust'
   case ('web');      lenguaje = 'TypeScript'
   case ('datos');    lenguaje = 'SQL'
   case default;      lenguaje = '?'
   end select

   write(*, '(A)') 'lenguaje=' // trim(lenguaje)
end program elegir
""", """
**¿Cuándo se elige Fortran hoy?** Esta es de las respuestas más claras de la página: **para cálculo
numérico intensivo sobre arreglos, sigue siendo una elección defendible — y a veces la mejor.**

**Las razones son técnicas y concretas:**

**Una, los arreglos son ciudadanos de primera clase.** Operaciones de arreglo completo, secciones,
`reshape`, `matmul`, reducciones — **con una sintaxis que expresa la intención y que el compilador
vectoriza bien** (clase 089).

**Dos, la ausencia de solapamiento por defecto.** En C, dos punteros pueden apuntar al mismo sitio, así
que el compilador no puede reordenar; **en Fortran, los argumentos no se solapan salvo que se declare**,
y eso permite optimizaciones que en C requieren `restrict` y esperanza.

**Tres, sesenta años de bibliotecas validadas** (clase 149): BLAS, LAPACK, FFTW, PETSc, ARPACK. **Nadie va
a reescribir eso, y su corrección está probada por un uso masivo.**

**Y cuatro, es el lenguaje del paralelismo científico**: MPI y OpenMP tienen soporte de primera en
Fortran, y las herramientas de los superordenadores lo esperan.

**Y las razones en contra, que también son reales:**

| Debilidad | Consecuencia |
|---|---|
| Manejo de texto pobre | cualquier cosa con cadenas es tedioso (clase 093) |
| Sin gestor de paquetes maduro | `fpm` es de 2020 (clase 143) |
| Ecosistema pequeño fuera del cálculo | nada de web, ni de nube, ni de interfaces |
| Legado difícil | `COMMON`, formato fijo, `GOTO` (clase 150) |

**Y la arquitectura que la comunidad ha convergido es la de la clase 155**: **Python arriba, Fortran
abajo**.

Es una elección poliglota deliberada, y es un buen ejemplo del cierre de esta clase: **el lenguaje
aburrido y productivo para el 90 %, y el especializado para el núcleo que lo justifica**.

Y si el proyecto es nuevo y numérico, hoy la decisión real es **Fortran moderno frente a C++ con Eigen
frente a Julia** — y la respuesta depende sobre todo del equipo y de las bibliotecas que ya se vayan a
usar.
"""),
        "ada": ("""
with Ada.Text_IO; use Ada.Text_IO;

procedure Elegir is
   Linea  : String (1 .. 20);
   Ultimo : Natural;
begin
   Get_Line (Linea, Ultimo);

   if Linea (1 .. Ultimo) = "sistemas" then
      Put_Line ("lenguaje=Rust");
   elsif Linea (1 .. Ultimo) = "web" then
      Put_Line ("lenguaje=TypeScript");
   elsif Linea (1 .. Ultimo) = "datos" then
      Put_Line ("lenguaje=SQL");
   else
      Put_Line ("lenguaje=?");
   end if;
end Elegir;
""", """
**¿Cuándo se elige Ada hoy?** Y aquí hay una respuesta que sorprende a mucha gente: **se sigue eligiendo,
para sistemas nuevos, y no solo por inercia.**

**Dónde se elige de verdad:**

```text
Aviónica civil y militar, control ferroviario (ERTMS), satélites y lanzadores,
sistemas de defensa, dispositivos médicos, control industrial crítico.
```

**Y las razones son las que este curso ha ido mostrando:**

| Razón | Clase |
|---|---|
| **Tipos con rango y unidades**: los errores se vuelven imposibles de escribir | 124 |
| **Contratos comprobados o demostrados** con SPARK | 118 |
| **Concurrencia analizable** con Ravenscar: se demuestran los plazos | 135, 146 |
| **Sin sorpresas**: nada de comportamiento indefinido | 136 |
| **Legibilidad**: el código lo revisa gente que no lo escribió | 146 |
| **Estabilidad**: código de 1995 compila hoy, y lo hará en 2045 | 154 |

**Y la fila de SPARK es la que hace la diferencia hoy**: **demostrar matemáticamente la ausencia de
errores de ejecución** es una capacidad que, en producción industrial, tienen muy pocos lenguajes.

Y merece la comparación honesta con Rust, porque es la que se plantea en 2026:

| | Ada/SPARK | Rust |
|---|---|---|
| Seguridad de memoria | sí, y **demostrable** | sí, por el sistema de tipos |
| Ecosistema | **pequeño** | grande y creciente |
| Contratación | **muy difícil** | difícil, mejorando |
| Certificación | **madura**: DO-178C, EN 50128 | **en construcción** |
| Herramientas de demostración | **gnatprove, maduro** | Kani, Creusot: jóvenes |
| Concurrencia | tareas y Ravenscar, analizable | sin carreras, con `Send`/`Sync` |

**La fila de la certificación es la decisiva en estos sectores**: hay cadenas de herramientas Ada
cualificadas y décadas de evidencia ante los reguladores. **Rust está llegando, y todavía no está.**

Y la conclusión práctica del cierre de esta clase: **Ada se elige cuando el coste de un fallo es mucho
mayor que el coste del desarrollo**. Fuera de esos dominios, el ecosistema y la contratación pesan más —
y eso es una decisión racional, no un desprecio.
"""),
        "pascal": ("""
program Elegir;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  Dominio: string;

begin
  ReadLn(Dominio);
  Dominio := Trim(Dominio);

  if Dominio = 'sistemas' then WriteLn('lenguaje=Rust')
  else if Dominio = 'web' then WriteLn('lenguaje=TypeScript')
  else if Dominio = 'datos' then WriteLn('lenguaje=SQL')
  else WriteLn('lenguaje=?');
end.
""", """
**¿Cuándo se elige Object Pascal hoy?** La respuesta honesta: **rara vez para algo nuevo desde cero, y
con argumentos reales para un nicho concreto — aplicaciones de escritorio nativas.**

**Lo que sigue siendo bueno:**

| Fortaleza | Detalle |
|---|---|
| **Compilación rapidísima** | un proyecto grande compila en segundos (clase 123) |
| **Binario autocontenido y pequeño** | sin instalar nada en el destino (clase 144) |
| **Interfaces nativas de verdad** | no un navegador empaquetado |
| **Compilación cruzada trivial** | Free Pascal, a casi cualquier destino (clase 147) |
| **Legibilidad** | fue diseñado para eso (clase 152) |
| **Estabilidad** | código de 1997 sigue compilando |

**Y lo que pesa en contra, que es mucho:**

- **La comunidad se ha reducido**, y con ella las bibliotecas para lo nuevo.
- **Delphi es comercial y caro**; Free Pascal y Lazarus son libres pero con menos pulido.
- **La contratación es difícil**, y el perfil medio es de más edad (clase 154).
- **Y el mundo se movió a la web y al móvil**, donde su presencia es marginal.

Y merece decir dónde sigue vivo de verdad, porque no es poco: **decenas de miles de aplicaciones de
gestión, de punto de venta, de laboratorio y de control industrial en Europa y Latinoamérica**, muchas
con veinte años y en mantenimiento activo.

**Es un ecosistema real, con clientes que pagan, y su problema no es técnico: es demográfico.**

Y hay un uso de Pascal que sí es indiscutible hoy y merece cerrar con él: **enseñar**.

**Pascal se diseñó para eso** (clase 152), y sigue siendo excelente: **sintaxis explícita, sin trampas,
con un compilador rápido y mensajes de error claros** (clase 137).

Y hay un argumento adicional que este curso hace evidente: **quien aprende Pascal entiende después
cualquier lenguaje imperativo con tipos**, porque **Pascal hace visible lo que otros esconden** —la
diferencia entre asignar y comparar, entre valor y referencia, entre declarar y usar—.
"""),
        "lisp": ("""
(let ((dominio (string-trim '(#\\Space #\\Return) (read-line))))
  (format t "lenguaje=~A~%"
          (cond ((string= dominio "sistemas") "Rust")
                ((string= dominio "web") "TypeScript")
                ((string= dominio "datos") "SQL")
                (t "?"))))
""", """
**¿Cuándo se elige Common Lisp hoy?** Es de las respuestas más matizadas de la página: **se elige poco, y
quienes lo eligen tienen razones muy concretas y bastante buenas.**

**Dónde brilla de verdad:**

| Caso | Por qué |
|---|---|
| **Problemas mal definidos** | el ciclo de exploración es el más corto que existe (clase 124) |
| **Dominios con lógica compleja** | las macros permiten construir el vocabulario (clase 149) |
| **Sistemas que no pueden pararse** | redefinición en caliente (clase 148) |
| **Manipulación simbólica** | álgebra, demostradores, compiladores, planificación |
| **Prototipos que acaban en producción** | el prototipo **es** el sistema |

**Y los casos reales que merece conocer**: **Maxima** (álgebra simbólica), **ITA Software** —el motor de
búsqueda de vuelos que compró Google y que sigue moviendo reservas aéreas—, **Grammarly** en sus
comienzos, y buena parte de la investigación en planificación y en demostración automática.

**Y las razones en contra son igual de reales:**

- **El ecosistema es pequeño**: para casi cualquier problema moderno hay más y mejores bibliotecas en
  otros lenguajes.
- **La contratación es muy difícil.**
- **Y la sintaxis de paréntesis, aunque no es realmente un problema para quien la usa, sí lo es para
  convencer a un equipo.**

Y merece señalar la influencia, porque es la parte de Lisp que más se subestima y que este curso ha ido
mostrando:

```text
De Lisp salieron: la recolección de basura, las funciones de primera clase, los cierres,
la evaluación perezosa, el REPL, las excepciones con reinicios, las macros higiénicas,
el tipado dinámico moderno, la programación funcional aplicada,
y buena parte del diseño de los IDE.
```

**Prácticamente todo lo que hoy se considera moderno en un lenguaje de alto nivel apareció primero en
Lisp**, entre 1958 y 1985.

Y la conclusión para el cierre de esta clase: **si el problema es explorar algo que nadie ha resuelto y
el equipo es pequeño y bueno, Lisp sigue siendo una elección defendible**. Si el problema es conocido y
el equipo va a crecer, casi con seguridad no.
"""),
        "tcl": ("""
gets stdin dominio
set d [string trim $dominio]

switch -exact -- $d {
    sistemas { set l "Rust" }
    web      { set l "TypeScript" }
    datos    { set l "SQL" }
    default  { set l "?" }
}

puts "lenguaje=$l"
""", """
**¿Cuándo se elige Tcl hoy?** La respuesta es la más específica de esta página: **para incrustar, y para
las plataformas donde ya está.**

**Donde sigue siendo la elección correcta:**

| Caso | Por qué |
|---|---|
| **Lenguaje de extensión de una aplicación en C** | para eso se diseñó (clases 155 y 163) |
| **Automatizar herramientas interactivas** | Expect no tiene sustituto real (clase 147) |
| **Diseño de circuitos** | es el lenguaje de todas las herramientas del sector |
| **Interfaces rápidas y multiplataforma** | Tk sigue siendo la forma más corta de hacer una ventana |
| **Guiones que deben durar décadas** | compatibilidad hacia atrás extrema (clase 154) |

**La primera fila es la que aguanta el argumento**: comparado con Lua —su competidor natural—, Tcl es más
grande y más lento, pero trae **más batería incluida**: sockets, bucle de eventos, expresiones regulares,
Tk, y un modelo de seguridad maduro (clase 153).

**Y la tercera es la que garantiza su supervivencia**: **el sector del diseño de circuitos no va a
cambiar de lenguaje de guion**, porque sus flujos tienen décadas y un valor enorme.

**Y las razones para no elegirlo en un proyecto nuevo genérico:**

- **La comunidad es pequeña** y las bibliotecas modernas escasean.
- **El modelo "todo es una cadena"** produce un rendimiento peculiar (clase 152) y sorpresas de citación
  (clase 146).
- **Y Python y Lua ocupan hoy sus dos nichos naturales** con ecosistemas mucho mayores.

Y merece cerrar con lo que Tcl aportó y que sí sobrevive en todas partes, porque es la parte importante de
su legado:

**La tesis de los dos lenguajes** (clase 155): que un sistema se construye mejor con un lenguaje de
sistemas para los componentes y uno de guion para unirlos.

**Esa idea ganó tan completamente que hoy es invisible**: cada aplicación con complementos, cada
herramienta con configuración programable y cada motor de juego con guiones **está aplicando el argumento
de Ousterhout de 1998**, aunque use Lua, Python o JavaScript.

Es la mejor forma de éxito que puede tener una idea: **que nadie recuerde que hubo que defenderla**.
"""),
        "perl": ("""
use strict;
use warnings;

my $dominio = <STDIN>;
chomp $dominio;

my %mapa = (sistemas => 'Rust', web => 'TypeScript', datos => 'SQL');

print "lenguaje=", ($mapa{$dominio} // '?'), "\\n";
""", """
**¿Cuándo se elige Perl hoy?** La respuesta honesta y sin adornos: **para texto, y para mantener lo que
ya existe.**

**Donde sigue siendo objetivamente bueno:**

| Caso | Por qué |
|---|---|
| **Transformar texto a gran escala** | las expresiones regulares siguen siendo las mejores (clase 093) |
| **Guiones de una línea** | `perl -ne` es imbatible para lo desechable |
| **Bioinformática** | BioPerl y décadas de canalizaciones |
| **Sistemas heredados** | hay mucho, funcionando |
| **Está instalado en todas partes** | en cualquier Unix, sin instalar nada |

**Y merece reconocer que su motor de expresiones regulares definió el estándar**: **PCRE —*Perl
Compatible Regular Expressions*— es la biblioteca que usan PHP, Nginx, Apache, R y decenas más**.

**El nombre lo dice todo: el estándar de facto de las expresiones regulares se llama "compatible con
Perl".**

**Y las razones para no elegirlo hoy en un proyecto nuevo:**

- **Python ocupó su nicho** —guiones, administración, ciencia de datos, texto— con una comunidad mucho
  mayor y un código más legible por defecto.
- **La saga de Perl 6** —anunciado en 2000, publicado en 2015 y finalmente renombrado a Raku en 2019—
  **paralizó la percepción del lenguaje durante quince años**, aunque Perl 5 siguió mejorando todo ese
  tiempo.
- **Y su fama de ilegible**, merecida a medias: **Perl permite escribir código horrible**, y muchos lo
  hicieron; **también permite escribirlo bien** (clase 146), y menos gente lo hizo.

Y merece cerrar con lo que Perl dejó y que este curso ha ido señalando, porque es una lista notable:

```text
CPAN, el primer archivo de paquetes de un lenguaje (clase 143)
TAP, el protocolo de pruebas (clase 139)
CPAN Testers, integración continua distribuida (clase 147)
El modo taint (clase 153)
POD, documentación embebida (clase 154)
Perl Best Practices y perlcritic, con severidades (clase 146)
Y las expresiones regulares tal como hoy las usa todo el mundo
```

**Casi todo lo que un ecosistema de lenguaje moderno da por supuesto lo inventó o lo popularizó Perl**, y
esa es una forma de vigencia que no aparece en los índices de popularidad.
"""),
        "cpp": ("""
#include <iostream>
#include <string>

int main() {
    std::string dominio;
    if (!std::getline(std::cin, dominio)) return 1;

    const std::string leng =
        dominio == "sistemas" ? "Rust" :
        dominio == "web"      ? "TypeScript" :
        dominio == "datos"    ? "SQL" : "?";

    std::cout << "lenguaje=" << leng << '\\n';
    return 0;
}
""", """
**¿Cuándo se elige C++ hoy?** Es de los pocos de esta página que **se elige constantemente para proyectos
nuevos**, y merece decir con precisión cuándo y cuándo no.

**Donde es la elección correcta:**

| Caso | Por qué |
|---|---|
| **Rendimiento con abstracción** | plantillas y `constexpr`: cero coste en ejecución (clase 122) |
| **Motores de juego y gráficos** | Unreal, y todo el ecosistema de renderizado |
| **Sistemas embebidos potentes** | automoción, robótica, imagen médica |
| **Alta frecuencia y baja latencia** | control total sobre memoria y disposición (clase 152) |
| **Bibliotecas para otros lenguajes** | es el sustrato de casi todos (clase 155) |
| **Bases de datos y compiladores** | LLVM, ClickHouse, MongoDB, MySQL |

**Y donde ya no es la elección obvia, que es la novedad de la última década:**

```text
Para sistemas NUEVOS donde la seguridad de memoria importa,
Rust ofrece un rendimiento comparable con garantías que C++ no puede dar (clase 153).

Y varias agencias de seguridad lo recomiendan explícitamente para código nuevo.
```

**Merece la comparación honesta**, porque es la decisión real de 2026:

| | C++ | Rust |
|---|---|---|
| Rendimiento | equivalente | equivalente |
| **Seguridad de memoria** | **no**, sin disciplina y herramientas | **sí, por el compilador** |
| Ecosistema | **inmenso y maduro** | grande y creciente |
| Interoperabilidad con C | **nativa** | buena, con `unsafe` |
| Curva de aprendizaje | larga, con trampas | **empinada al principio** |
| Tiempo de compilación | malo | malo |
| Código existente | **miles de millones de líneas** | poco, comparativamente |

**Y la fila del código existente es la que decide en la práctica**: **nadie reescribe un motor de juego de
tres millones de líneas**, así que la estrategia real es **la que Android y Chromium aplican: código nuevo
en Rust, el existente en C++, con la frontera bien definida** (clases 156 y 157).

Es, exactamente, el cierre de esta clase: **poliglota por decisión, no por accidente**.

Y merece señalar que C++ no se ha quedado quieto: **C++11, 17, 20 y 23 cambiaron el lenguaje
profundamente** —lambdas, punteros inteligentes, `constexpr`, conceptos, rangos, corrutinas— y **el C++
moderno bien escrito es un lenguaje muy distinto del de 1998**.

El problema, que este curso ha señalado varias veces, es que **el lenguaje viejo sigue siendo válido**, así
que **un proyecto real contiene las cuatro décadas a la vez** (clase 154).
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi ELEGIR;
  dominio char(20) const;
end-pi;

dcl-s leng varchar(20);

select;
  when %trim(dominio) = 'sistemas'; leng = 'Rust';
  when %trim(dominio) = 'web';      leng = 'TypeScript';
  when %trim(dominio) = 'datos';    leng = 'SQL';
  other;                            leng = '?';
endsl;

dsply ('lenguaje=' + leng);

*inlr = *on;
return;
""", """
**¿Cuándo se elige RPG hoy?** La respuesta es la más condicionada de esta página: **si ya tienes un IBM i,
es una elección excelente; si no lo tienes, la pregunta no es sobre el lenguaje.**

**Y merece explicar por qué la primera mitad es verdad**, porque suele darse por supuesto que no:

| En IBM i, RPG da | Detalle |
|---|---|
| **Acceso a datos sin fricción** | la base de datos es el sistema operativo (clase 139) |
| **SQL embebido de primera** | comprobado en compilación (clase 163) |
| **Rendimiento excelente en gestión** | compilado, nativo, sin capas |
| **Observabilidad por defecto** | registro, pilas y auditoría sin configurar (clase 142) |
| **Despliegue y reversión triviales** | la lista de bibliotecas (clase 148) |
| **Compatibilidad de décadas** | objetos de 1990 siguen funcionando |

**Y el RPG moderno —formato totalmente libre, procedimientos, programas de servicio, SQL, JSON con
`DATA-INTO`— es un lenguaje razonable** (clases 146 y 158), muy lejos del RPG de columnas que le dio la
fama.

**La decisión real, entonces, no es "¿RPG o Python?" sino "¿seguimos en IBM i?"** — y eso es una decisión
de plataforma con implicaciones enormes: hardware, licencias, personal y treinta años de aplicaciones.

**Y los argumentos en contra son de plataforma, no de lenguaje:**

- **Coste**: hardware POWER y licencias frente a máquinas genéricas y software libre.
- **Contratación**: el problema demográfico de la clase 154, agudo.
- **Ecosistema**: todo lo moderno llega, pero tarde y por PASE.
- **Y la dependencia de un único proveedor.**

Y merece cerrar con lo que esta plataforma enseña y que el resto de la industria está redescubriendo,
porque aparece una y otra vez en este curso: **integrar la base de datos, el sistema operativo, la
seguridad y la observabilidad en un solo sistema coherente da una productividad operativa que un montaje
de veinte piezas no alcanza**.

Es el argumento de fondo de las plataformas integradas, y explica por qué quien tiene un IBM i funcionando
rara vez se va — y por qué quien no lo tiene rara vez entra.
"""),
        "pli": ("""
 elegir: procedure options(main);

    declare dominio char(20) varying;

    get edit (dominio) (a(20));
    dominio = trim(dominio);

    select (dominio);
       when ('sistemas') put skip list ('lenguaje=Rust');
       when ('web')      put skip list ('lenguaje=TypeScript');
       when ('datos')    put skip list ('lenguaje=SQL');
       otherwise         put skip list ('lenguaje=?');
    end;

 end elegir;
""", """
**¿Cuándo se elige PL/I hoy?** La respuesta más corta de esta página: **nunca para algo nuevo.**

Y merece explicar por qué con precisión, porque las razones son instructivas y ninguna es "el lenguaje es
malo":

**Una, no hay implementación libre** (clase 162). Es la razón estructural: **sin un compilador libre, el
lenguaje no llega a ninguna plataforma nueva** y depende por completo de que su propietario invierta.

**Dos, no hay comunidad ni ecosistema.** No hay gestor de paquetes, ni bibliotecas modernas, ni foros
activos, ni cursos.

**Tres, la contratación es prácticamente imposible** para nuevos proyectos.

**Y cuatro, lo que PL/I hacía bien lo hacen otros**: el decimal exacto lo tiene COBOL y lo tienen los tipos
decimales modernos; el cálculo lo hace Fortran; la programación de sistemas la hacen C, C++ y Rust.

**Y aun así, merece defender lo que fue**, porque este curso lo ha ido mostrando y es notable:

```text
PL/I tenía, en 1964, cosas que otros lenguajes tardaron décadas en tener:
  - manejo de excepciones con reanudación (clase 116)
  - concurrencia en el lenguaje
  - decimal exacto con precisión declarada (clase 072)
  - punteros y gestión de almacenamiento explícita
  - un preprocesador programable (clase 163)
  - y una biblioteca de funciones de arreglos y cadenas muy rica
```

**Fue el lenguaje más ambicioso de su época, y su ambición fue su problema** (clases 146 y 155): **un
lenguaje que sirve para todo es un lenguaje que nadie domina entero y que su compilador no puede
optimizar bien**.

Y la lección que deja para el cierre de esta clase es de las más útiles del curso, y no es sobre PL/I:

**El diseño de un lenguaje es un ejercicio de renuncia.** Lo que un lenguaje **prohíbe** es lo que
permite a su compilador optimizar, a sus herramientas analizar y a sus usuarios entenderlo.

Es la misma observación que Wirth aplicó con Pascal, Modula-2 y Oberon —**cada uno más pequeño que el
anterior**— y la que explica por qué los lenguajes que sobreviven suelen ser los que dijeron que no a
tiempo.
"""),
        "mumps": ("""
ELEGIR ; Elegir lenguaje por dominio -- clase 164
 read dominio
 write "lenguaje=", $select(dominio="sistemas" : "Rust", dominio="web" : "TypeScript", dominio="datos" : "SQL", 1 : "?"), !
 quit
""", """
**¿Cuándo se elige M hoy?** La respuesta tiene dos mitades muy distintas, y merece separarlas porque casi
siempre se confunden: **el lenguaje, casi nunca; el motor de base de datos, más de lo que parece.**

**El lenguaje M no se elige para nada nuevo**, y las razones son claras: sin declaraciones, con ámbito
global por defecto (clase 146), con indirección imposible de analizar (clase 150) y con una sintaxis
que rechaza a cualquiera que llegue nuevo.

**Y el motor sí se elige, y merece explicar por qué**, porque es una tecnología genuinamente buena:

| Propiedad | Detalle |
|---|---|
| **Árboles jerárquicos ordenados y persistentes** | las globals (clase 099): esquema libre, con orden |
| **Transacciones ACID reales** | `tstart`/`tcommit`, con el código y los datos juntos (clase 161) |
| **Rendimiento en escrituras pequeñas** | miles de operaciones por segundo por núcleo |
| **Cero impedancia** | no hay traducción entre el lenguaje y la base (clase 099) |
| **Fiabilidad demostrada** | décadas en hospitales y en bancos, sin perder datos |

**Y ahí está la elección real de hoy: YottaDB como motor, con la aplicación en Go, Python, Rust o
Node** (clase 156).

Eso da lo bueno de M —**el modelo de datos y la transaccionalidad**— sin lo malo —**el lenguaje**—, y es
la dirección en la que este ecosistema se está moviendo.

**Y merece nombrar dónde M está hoy, porque es más de lo que se supone:**

```text
Sanidad:  VistA (Veteranos de EE. UU.), Epic (el mayor proveedor de historia
          clínica del mundo, sobre InterSystems), y sistemas nacionales en varios países
Finanzas: Ameritrade y varios sistemas de negociación
Y decenas de sistemas nacionales de identidad y de registro
```

**Epic merece la mención**: mueve la historia clínica de cientos de millones de pacientes, **y su núcleo
funciona sobre una base de datos M** — un dato que sorprende a casi todo el mundo.

Y la conclusión para el cierre de esta clase: **M es el mejor ejemplo del curso de una tecnología juzgada
por su sintaxis en lugar de por su arquitectura**.

El lenguaje es indefendible con criterios de 2026. **El modelo de datos —árboles ordenados,
persistentes, transaccionales, sin impedancia— es una idea excelente** que las bases de datos de clave y
valor redescubrieron cuarenta años después, casi siempre sin las transacciones.
"""),
        "smalltalk": ("""
| dominio |

dominio := stdin nextLine trimBoth.

Transcript
    show: 'lenguaje=', (dominio = 'sistemas'
        ifTrue: [ 'Rust' ]
        ifFalse: [ dominio = 'web'
            ifTrue: [ 'TypeScript' ]
            ifFalse: [ dominio = 'datos'
                ifTrue: [ 'SQL' ]
                ifFalse: [ '?' ] ] ]);
    cr.
""", """
**¿Cuándo se elige Smalltalk hoy?** Y con esta respuesta cierra la Parte 10, así que merece hacerla bien:
**rara vez, y su influencia está en todas partes.**

**Dónde se sigue eligiendo:**

| Caso | Por qué |
|---|---|
| **Dominios complejos y cambiantes** | modelar con objetos vivos es insuperable (clase 149) |
| **Sistemas que no pueden pararse** | actualización en caliente (clase 148) |
| **Análisis de software** | **Moose**: importar código ajeno como objetos (clase 155) |
| **Investigación y enseñanza** | Pharo y Squeak; Scratch está encima (clase 163) |
| **Finanzas con GemStone** | objetos transaccionales, en producción desde los noventa |

**Y las razones en contra, que son las de siempre**: comunidad pequeña, contratación muy difícil, y el
modelo de imagen (clase 144) que choca con todo el instrumental moderno —git, contenedores, integración
continua— hasta que se adapta (clase 145).

**Y ahora lo que merece decirse al cerrar la parte, porque es lo importante:**

```text
De Smalltalk salieron, y este curso las ha ido nombrando una por una:

  la interfaz gráfica con ventanas, iconos y ratón   (Xerox PARC → Apple → todos)
  MVC                                                  (clase 149)
  el patrón Observador en la raíz del sistema           (clase 149)
  las pruebas unitarias: SUnit → JUnit → todo lo demás   (clase 139)
  el desarrollo dirigido por pruebas                      (clase 139)
  la refactorización automática: el Refactoring Browser    (clase 150)
  la deuda técnica, como metáfora                           (clase 154)
  las cachés de envío en línea, base de todos los JIT        (clase 152)
  la programación extrema y buena parte de lo ágil
  y el propio término "orientado a objetos"
```

**Prácticamente todo lo que un equipo de software hace hoy por costumbre —escribir la prueba antes,
refactorizar con el IDE, hablar de deuda técnica, separar el modelo de la vista— salió de una comunidad
pequeña que trabajaba en un lenguaje que casi nadie usa.**

Y esa es la mejor conclusión posible para esta parte y para estas doce columnas: **el valor de un lenguaje
no se mide solo por cuánta gente lo usa, sino por cuánto de él acabó dentro de los demás**.

Y por eso este curso los ha recorrido: **no para que se usen —aunque varios se sigan usando— sino porque
en ellos están las decisiones originales, con sus razones intactas**, y entenderlas es lo que permite
tomar las propias con criterio en lugar de por costumbre.
"""),
    },
)
