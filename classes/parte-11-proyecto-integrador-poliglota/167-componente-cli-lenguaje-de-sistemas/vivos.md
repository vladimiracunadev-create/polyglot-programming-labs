# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 167

> [⬅️ Volver a la clase 167](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Un comando y sus argumentos: `comando=run args=2`. Es la interfaz de usuario más antigua que sigue viva,
y la que estos doce lenguajes conocen mejor. Y merece empezar con una observación: **la línea de comandos
no ha sobrevivido por nostalgia, sino porque es la única interfaz que se puede automatizar, versionar,
componer y ejecutar sin persona delante** — que son exactamente los requisitos de todo lo que esta parte
del curso está construyendo.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es la **herramienta de línea de comandos como componente**, y estos lenguajes la
> enseñan porque **cubren los dos extremos**: los que producen un ejecutable nativo sin dependencias
> —Pascal, Ada, C++, COBOL, Fortran— y los que necesitan su intérprete —Perl, Tcl, Lisp—. Y esa diferencia
> decide algo muy práctico: **si la herramienta se puede copiar y ejecutar, o hay que instalar un
> entorno**.
>
> Y aparecen las convenciones que hacen que una herramienta encaje con las demás: **códigos de salida,
> salida estándar frente a error, y comportarse bien en una tubería**.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: una línea `comando arg1 arg2 ...` (al menos el comando) → stdout: `comando=<comando> args=<número de argumentos>`
- **Regla:** `primer token = comando; resto = argumentos`

| stdin | esperado |
|---|---|
| `run a b` | `comando=run args=2` |
| `build` | `comando=build args=0` |
| `deploy x y z` | `comando=deploy args=3` |

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
PROGRAM-ID. CLI.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(200).
01  I       PIC 9(4) COMP.
01  CNT     PIC 9(4) COMP VALUE 0.
01  ENPAL   PIC 9      VALUE 0.
01  COMANDO PIC X(30) VALUE SPACES.
01  POSIC   PIC 9(4) COMP VALUE 1.
01  ED      PIC -(3)9.

PROCEDURE DIVISION.
    ACCEPT LINEA

    PERFORM VARYING I FROM 1 BY 1 UNTIL I > 200
        IF LINEA(I:1) = SPACE
            MOVE 0 TO ENPAL
        ELSE
            IF ENPAL = 0
                MOVE 1 TO ENPAL
                ADD 1 TO CNT
            END-IF
            IF CNT = 1
                MOVE LINEA(I:1) TO COMANDO(POSIC:1)
                COMPUTE POSIC = POSIC + 1
            END-IF
        END-IF
    END-PERFORM

    COMPUTE CNT = CNT - 1
    MOVE CNT TO ED
    DISPLAY "comando=" FUNCTION TRIM(COMANDO)
            " args=" FUNCTION TRIM(ED)
    STOP RUN.
```

**COBOL como herramienta de línea de comandos.** COBOL sabe hacerlo, y merece conocer cómo, porque el
mundo GnuCOBOL lo usa de verdad:

```cobol
       PROCEDURE DIVISION.
           ACCEPT WS-ARGS FROM COMMAND-LINE          *> toda la línea
           ACCEPT WS-N    FROM ARGUMENT-NUMBER        *> cuántos hay
           PERFORM VARYING I FROM 1 BY 1 UNTIL I > WS-N
               ACCEPT WS-ARG FROM ARGUMENT-VALUE      *> uno a uno
           END-PERFORM

           ACCEPT WS-VAR FROM ENVIRONMENT "MI_VARIABLE"
           ...
           MOVE 2 TO RETURN-CODE                       *> ← el código de salida
           STOP RUN.
```

**`RETURN-CODE` es la tercera propiedad del cierre de esta clase**, y en COBOL es una variable especial:
**asignarle un valor antes de `STOP RUN` es el código de salida del proceso**.

Y merece explicar de dónde viene esa convención, porque es del mundo del lote y sigue viva: **el código
de retorno gobierna el JCL** (clase 077).

```jcl
//PASO2 EXEC PGM=SIGUIENTE,COND=(4,LT,PASO1)
//*    ejecutar PASO2 solo si el código de PASO1 NO es mayor que 4
```

**Los valores tienen significado convenido en el mainframe**:

```text
0   todo bien
4   avisos: continuar
8   error: normalmente parar
12  error grave
16  error fatal
```

**Es exactamente la idea de los códigos de salida de Unix, con más granularidad y con un lenguaje —el
JCL— para decidir en función de ellos.**

Y merece señalar la diferencia con la práctica actual: **en Unix, 0 es bien y cualquier otro es mal**;
en el mainframe, **hay una escala** y los guiones la usan.

Es una idea que merece rescatarse para la primera regla del cierre: **distinguir "falló" de "terminó con
avisos" permite automatizar decisiones que con un booleano no se pueden tomar** — y es lo que hacen hoy
las herramientas serias con códigos de salida específicos documentados.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program cli
   implicit none
   character(len=200) :: linea
   character(len=30)  :: comando
   integer :: i, cnt, p1
   logical :: en_palabra

   read(*, '(A)') linea
   linea = adjustl(linea)

   p1 = index(linea, ' ')
   comando = linea(1:p1-1)

   cnt = 0
   en_palabra = .false.
   do i = 1, len_trim(linea)
      if (linea(i:i) == ' ') then
         en_palabra = .false.
      else if (.not. en_palabra) then
         en_palabra = .true.
         cnt = cnt + 1
      end if
   end do

   write(*, '(A,I0)') 'comando=' // trim(comando) // ' args=', cnt - 1
end program cli
```

**Fortran como herramienta de línea de comandos.** Fortran tardó en tener acceso a los argumentos de
forma estándar, y merece contarlo porque ilustra bien la evolución del lenguaje:

```fortran
! Antes de 2003: extensiones distintas en cada compilador
call getarg(1, arg)          ! ¡no estándar!

! Fortran 2003, en el estándar:
integer :: n, largo, estado
character(len=:), allocatable :: arg

n = command_argument_count()
call get_command_argument(1, length=largo)
allocate(character(len=largo) :: arg)
call get_command_argument(1, arg)

call get_environment_variable('MI_VAR', valor)
call execute_command_line('ls -l', wait=.true., exitstat=codigo)   ! 2008
```

**`get_command_argument` con `length=` primero y luego el valor** es el idioma correcto: **se pregunta la
longitud, se reserva, y se lee** — porque las cadenas de Fortran son de longitud fija (clase 093).

Y **`execute_command_line`, de Fortran 2008**, merece la mención porque cierra un hueco importante: **hasta
entonces, ejecutar otro programa desde Fortran requería extensiones del compilador**.

Y esta clase es el sitio para señalar la costumbre de este dominio que choca con el cierre de esta clase,
porque merece revisarse: **los programas científicos no suelen tener interfaz de línea de comandos: leen
un fichero de configuración** (clase 163).

```bash
./simulacion < entrada.nml       # o incluso con el fichero con un nombre fijo
```

**Y eso los hace difíciles de automatizar**: para lanzar mil variantes hay que generar mil ficheros.

Y la recomendación de esta parte del curso es concreta y barata: **aceptar los parámetros también por la
línea de comandos**, con los valores del fichero como valores por defecto.

```bash
./simulacion --config base.nml --set dt=0.0005 --set modelo=laminar
```

**Con eso, un barrido de parámetros es un bucle de shell** en lugar de un generador de ficheros — y la
herramienta pasa a componerse con todo lo demás, que es la definición del cierre de esta clase.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Strings;
with Ada.Strings.Fixed;

procedure Cli is
   Linea      : String (1 .. 200);
   Ultimo     : Natural;
   Sep        : Natural;
   Cnt        : Natural := 0;
   En_Palabra : Boolean := False;
begin
   Get_Line (Linea, Ultimo);
   Sep := Ada.Strings.Fixed.Index (Linea (1 .. Ultimo), " ");

   if Sep = 0 then
      Sep := Ultimo + 1;
   end if;

   for I in 1 .. Ultimo loop
      if Linea (I) = ' ' then
         En_Palabra := False;
      elsif not En_Palabra then
         En_Palabra := True;
         Cnt := Cnt + 1;
      end if;
   end loop;

   Put_Line ("comando=" & Linea (1 .. Sep - 1) & " args=" &
             Ada.Strings.Fixed.Trim (Natural'Image (Cnt - 1), Ada.Strings.Both));
end Cli;
```

**Ada como herramienta de línea de comandos.** Ada tiene los argumentos en el estándar desde 1995, con una
API pequeña y clara:

```ada
with Ada.Command_Line; use Ada.Command_Line;

for I in 1 .. Argument_Count loop
   Put_Line (Argument (I));
end loop;

Put_Line (Command_Name);
Set_Exit_Status (Failure);      --  o Success, o un valor concreto
```

**`Set_Exit_Status` con `Success` y `Failure` como constantes con nombre** es un detalle pequeño y
representativo: **el código de salida no es un número mágico, es un valor de un tipo**.

Y las herramientas de línea de comandos escritas en Ada tienen una ventaja concreta para el proyecto de
esta parte, y merece decirla: **son ejecutables nativos, estáticos y sin dependencias**.

```bash
gnatmake -O2 herramienta.adb
ldd herramienta        # apenas libc: se copia y funciona
```

**Y con `pragma Restrictions` y el perfil reducido** (clase 162), **el binario puede ser muy pequeño y de
consumo acotado** — lo que la hace apta para arrancar en un contenedor mínimo (clase 174).

Y Ada aporta a esta clase una técnica de diseño que encaja con el cierre y que la clase 124 hace posible:
**validar los argumentos con tipos**.

```ada
subtype Puerto is Integer range 1 .. 65_535;

declare
   P : constant Puerto := Puerto'Value (Argument (1));   --  lanza si no encaja
begin
   ...
exception
   when Constraint_Error =>
      Put_Line (Standard_Error, "El puerto debe estar entre 1 y 65535");
      Set_Exit_Status (Failure);
end;
```

**El rango del tipo es la validación**, y el mensaje de error se escribe una vez.

Y merece señalar el `Standard_Error` de ese fragmento, porque es la primera propiedad del cierre de esta
clase y la que más se incumple: **los mensajes van al error estándar, no a la salida**.

Si el mensaje de ayuda o el aviso salen por la salida estándar, **se cuelan en la tubería** y estropean lo
que el siguiente programa recibe. Es un fallo pequeño, muy frecuente, y hace que una herramienta no se
pueda componer.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Cli;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  Linea, Comando: string;
  I, Cnt, P: Integer;
  EnPalabra: Boolean;

begin
  ReadLn(Linea);
  Linea := Trim(Linea);

  P := Pos(' ', Linea);
  if P = 0 then P := Length(Linea) + 1;
  Comando := Copy(Linea, 1, P - 1);

  Cnt := 0;
  EnPalabra := False;
  for I := 1 to Length(Linea) do
    if Linea[I] = ' ' then
      EnPalabra := False
    else if not EnPalabra then
    begin
      EnPalabra := True;
      Inc(Cnt);
    end;

  WriteLn('comando=', Comando, ' args=', IntToStr(Cnt - 1));
end.
```

**Pascal como herramienta de línea de comandos.** Free Pascal es de las mejores opciones de esta página
para el componente de esta clase, y merece justificarlo:

```pascal
uses SysUtils, CustApp;

type
  TMiApp = class(TCustomApplication)
  protected
    procedure DoRun; override;
  end;

procedure TMiApp.DoRun;
begin
  if HasOption('h', 'help') then begin MostrarAyuda; Terminate; Exit end;
  if not CheckOptions('hv:', 'help verbose:') = '' then ...
  WriteLn(GetOptionValue('v', 'verbose'));
  ExitCode := 0;
  Terminate;
end;
```

**`TCustomApplication` viene en la distribución** y trae análisis de opciones cortas y largas, ayuda y
manejo de excepciones — sin instalar nada.

Y las razones por las que Pascal encaja bien aquí son las de la clase 164:

| Ventaja | Detalle |
|---|---|
| **Binario pequeño y autocontenido** | se copia y funciona (clase 144) |
| **Arranque instantáneo** | sin cargar intérprete ni máquina virtual |
| **Compilación cruzada** | un solo corredor produce Windows, Linux y macOS (clase 147) |
| **Compila en segundos** | el ciclo de desarrollo es rapidísimo |

**Y la tercera es la que más vale para el proyecto de esta parte**: **`fpc -Twin64` y `fpc -Tlinux` desde
la misma máquina** producen las dos herramientas, sin contenedores ni cadenas cruzadas.

Y merece añadir la propiedad del cierre que a menudo se olvida y que Pascal facilita: **detectar si hay
terminal**.

```pascal
uses Unix;
if IsATTY(StdOutputHandle) = 1 then
  { hay persona: se puede usar color y barra de progreso }
else
  { está en una tubería: salida limpia, sin adornos }
```

**Una herramienta que detecta si su salida va a un terminal o a una tubería puede ser bonita y
automatizable a la vez** — y es lo que hacen `git`, `ls` y todas las herramientas modernas bien hechas.

Es la cuarta propiedad del cierre resuelta con una llamada.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let* ((linea (read-line))
       (piezas (let ((lista '()) (actual '()))
                 (loop for c across linea
                       do (if (char= c #\Space)
                              (when actual
                                (push (coerce (nreverse actual) 'string) lista)
                                (setf actual nil))
                              (push c actual)))
                 (when actual (push (coerce (nreverse actual) 'string) lista))
                 (nreverse lista))))
  (format t "comando=~A args=~D~%" (first piezas) (1- (length piezas))))
```

**Lisp como herramienta de línea de comandos.** Lisp puede hacerlo, y tiene una limitación práctica que
merece enunciarse con claridad: **el arranque**.

```lisp
;; Acceso a los argumentos: NO está en el estándar; cada implementación tiene el suyo
sb-ext:*posix-argv*        ; SBCL
(uiop:command-line-arguments)   ; portable, con UIOP
(uiop:quit 1)                    ; código de salida
```

**Y la solución al arranque es la de la clase 144: guardar una imagen ejecutable.**

```lisp
(sb-ext:save-lisp-and-die "miherramienta"
                          :executable t
                          :toplevel #'main
                          :compression t)
```

**Con eso el arranque es de milisegundos** —el estado ya está construido— **a costa de un binario de
decenas de megabytes**.

Y merece la comparación honesta para el proyecto de esta parte:

| Aspecto | Lisp con imagen | Pascal/Ada/C++ |
|---|---|---|
| Arranque | **rápido** (ya construido) | rápido |
| Tamaño | **20-60 MB** | **0,2-5 MB** |
| Dependencias | ninguna | ninguna |
| Desarrollo | **el más rápido de esta página** | ciclo de compilación |

**Y esa tabla es la decisión**: si la herramienta se ejecuta mil veces al día en una canalización, el
tamaño importa; si es una herramienta interna que se usa a mano, no.

Y Lisp tiene, para esta clase, dos ecosistemas que merecen nombrarse:

| Herramienta | Notas |
|---|---|
| **Roswell** | gestor de implementaciones y **guiones ejecutables** con `#!/usr/bin/env ros` |
| **UIOP** | portabilidad: argumentos, procesos, rutas, salida |
| **clingon / unix-opts** | análisis de opciones, con subcomandos |
| **`--script`** | ejecutar un fichero sin construir imagen, pagando el arranque |

Y merece cerrar con la propiedad del cierre que Lisp cumple especialmente bien y que conviene aprovechar:
**la salida legible por máquina**.

```lisp
(if (uiop:getenvp "SALIDA_JSON")
    (yason:encode resultado)
    (format t "~{~A~%~}" resultado))
```

**Un `--json` opcional convierte la herramienta en un componente**, y en Lisp la estructura de datos ya
está ahí — solo hay que elegir el formateador.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea
set args [split [string trim $linea]]

puts "comando=[lindex $args 0] args=[expr {[llength $args] - 1}]"
```

**Tcl como herramienta de línea de comandos.** Tcl tiene los argumentos en variables globales, y su
manejo es directo:

```tcl
puts $argv0            ;# el nombre del guion
puts $argc              ;# cuántos argumentos
puts $argv               ;# la LISTA de argumentos
exit 1                    ;# código de salida
```

**`$argv` es una lista de verdad**, no una cadena que hay que partir — que es una comodidad real
comparada con varios de esta página.

Y Tcl es especialmente adecuado para el componente de esta clase por lo que la clase 165 señalaba: **es el
pegamento**, y la mayoría de las herramientas internas de un proyecto son pegamento.

```tcl
#!/usr/bin/env tclsh
package require cmdline

set opciones {
    {verbose        "salida detallada"}
    {config.arg  "" "fichero de configuración"}
    {jobs.arg     4 "trabajos en paralelo"}
}
array set params [::cmdline::getoptions argv $opciones "uso: $argv0 [opciones] comando"]
```

**`cmdline` está en tcllib** y da opciones, valores por defecto y el mensaje de uso.

Y merece señalar la propiedad del cierre de esta clase que Tcl facilita mejor que casi todos, porque es
su especialidad (clase 161): **encadenar procesos**.

```tcl
set salida [exec ./extraer $fichero | sort -n | uniq -c]
```

**`exec` con tuberías, en una línea** — y con la citación correcta, sin pasar por un intérprete de órdenes
(clase 153).

Y la advertencia práctica de esta clase para Tcl, que la clase 164 anticipó: **el guion necesita
`tclsh`**.

Y las respuestas son las de la clase 144:

```bash
sdx wrap miherramienta.exe -runtime tclkit    # Starpack: un ejecutable, sin dependencias
```

**Un Starpack convierte el guion en un binario autocontenido**, con lo que la herramienta se copia y
funciona — que es lo que el proyecto de esta parte necesita para distribuir sus utilidades sin exigir un
entorno.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;

my @args = split ' ', $linea;
my $comando = shift @args;

print "comando=$comando args=", scalar(@args), "\n";
```

**Perl como herramienta de línea de comandos.** Perl es, probablemente, **el lenguaje con el que más
herramientas de línea de comandos se han escrito**, y su ergonomía para esto es excelente:

```perl
use Getopt::Long;

GetOptions(
    'verbose!'   => \my $verbose,        # --verbose / --no-verbose
    'jobs=i'     => \(my $jobs = 4),      # --jobs 8
    'config=s'   => \my $config,          # --config fichero
    'help'       => sub { pod2usage(0) },  # ← la ayuda sale del POD (clase 154)
) or pod2usage(2);

exit(2) if $error;
```

**`pod2usage` merece la mención** porque resuelve un problema real: **el mensaje de ayuda se genera desde
la documentación POD del propio guion**, así que **no puede desincronizarse**.

Es la aplicación de la clase 154 a esta clase: **la documentación y la ayuda son la misma fuente**.

Y Perl tiene los idiomas de una línea que definieron el género y que merecen conocerse porque siguen
siendo insuperables:

```bash
perl -pe 's/viejo/nuevo/g' fichero          # sustituir e imprimir
perl -ne 'print if /error/' registro.log     # filtrar
perl -lane 'print $F[2]' datos.txt            # ¡la tercera columna!
perl -i.bak -pe 's/a/b/' *.conf                # editar EN SITIO, con copia
perl -MJSON::PP -e '...'                        # con un módulo cargado
```

**`-lane` es el más denso**: `-l` maneja los saltos de línea, `-a` **parte cada línea en `@F`
automáticamente**, `-n` hace el bucle y `-e` da el código.

**Es `awk` con todo Perl detrás**, y sigue siendo la forma más rápida de resolver una transformación de
texto puntual.

Y merece cerrar con las propiedades del cierre de esta clase, que Perl cumple si se escriben:

```perl
print STDERR "aviso: ...\n";        # mensajes al ERROR estándar
print STDOUT $resultado;              # el resultado, a la salida
exit 0;                                # explícito
$| = 1;                                 # sin búfer, si va a una tubería (clase 141)
```

**`$| = 1` merece la advertencia**: sin él, **la salida de Perl se guarda en un búfer cuando no va a un
terminal**, y una herramienta que escribe progreso en una tubería **parece colgada** hasta que termina.

Es la misma lección que `flush` en Fortran (clase 141), y una de las causas más frecuentes de "esto no
funciona en el servidor".

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>
#include <string>
#include <vector>

int main() {
    std::vector<std::string> args;
    std::string a;
    while (std::cin >> a) args.push_back(a);

    if (args.empty()) return 1;

    std::cout << "comando=" << args.front()
              << " args=" << args.size() - 1 << '\n';
    return 0;
}
```

**C++ como herramienta de línea de comandos.** C++ produce el binario más rápido y más pequeño de esta
página, y su ecosistema para esta clase es bueno:

```cpp
#include <CLI/CLI.hpp>          // CLI11: solo cabeceras

int main(int argc, char** argv) {
    CLI::App app{"Mi herramienta"};
    int jobs = 4;
    std::string config;
    bool verbose = false;

    app.add_option("-j,--jobs", jobs, "Trabajos en paralelo")->check(CLI::Range(1, 64));
    app.add_option("-c,--config", config, "Fichero de configuración")
       ->check(CLI::ExistingFile);
    app.add_flag("-v,--verbose", verbose);

    auto* sub = app.add_subcommand("build", "Construir el proyecto");

    CLI11_PARSE(app, argc, argv);
    return 0;
}
```

**`->check(CLI::Range(1, 64))` y `->check(CLI::ExistingFile)`** merecen destacarse: **la validación se
declara junto a la opción**, y el mensaje de error lo genera la biblioteca.

Es lo mismo que Ada consigue con los subtipos con rango en esta página, con una biblioteca en lugar de
con el sistema de tipos.

Y las alternativas del ecosistema:

| Biblioteca | Notas |
|---|---|
| **CLI11** | solo cabeceras, subcomandos, validación, configuración |
| **argparse** | ligera, al estilo de Python |
| **Boost.Program_options** | veterana, potente, pesada |
| **getopt / getopt_long** | de C, sin dependencias, y tediosa |

Y merece señalar, para el proyecto de esta parte, la propiedad de C++ que decide su uso aquí: **el
tiempo de arranque**.

```text
Un binario en C++ arranca en ~1 ms.
Python arranca en ~30-50 ms; Node en ~40 ms; una JVM en ~100-300 ms.
```

**Y eso importa cuando la herramienta se invoca miles de veces**, que es exactamente lo que pasa en un
sistema de construcción o en un gancho de git (clase 145).

Es la razón por la que las herramientas que se ejecutan en bucle —compiladores, formateadores,
analizadores, `ripgrep`, `fd`— **están escritas en lenguajes compilados**, y no por casualidad.

Y la advertencia final del cierre, que en C++ hay que escribir a mano: **cerrar bien la salida**.

```cpp
std::cout << resultado << std::flush;
return std::cout.good() ? 0 : 1;       // ¿falló la escritura? (disco lleno, tubería rota)
```

**Ignorar un error de escritura en la salida es un fallo silencioso clásico**, y una herramienta seria lo
comprueba.

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

dcl-pi CLI;
  linea char(200) const;
end-pi;

dcl-s texto   varchar(200);
dcl-s comando varchar(30);
dcl-s pos     int(10);
dcl-s cnt     int(10);
dcl-s enpal   ind;
dcl-s i       int(10);

texto = %trim(linea);
pos = %scan(' ' : texto);
if pos = 0;
  comando = texto;
else;
  comando = %subst(texto : 1 : pos - 1);
endif;

cnt = 0;
enpal = *off;
for i = 1 to %len(texto);
  if %subst(texto : i : 1) = ' ';
    enpal = *off;
  elseif not enpal;
    enpal = *on;
    cnt += 1;
  endif;
endfor;

dsply ('comando=' + comando + ' args=' + %char(cnt - 1));

*inlr = *on;
return;
```

**RPG como herramienta de línea de comandos.** IBM i tiene una noción de "línea de comandos" propia y muy
elaborada, y merece conocerla porque resuelve cosas que las demás de esta página dejan a la biblioteca:
**el comando CL definido por el usuario**.

```text
CMD PROMPT('Procesar pedidos')
PARM KWD(CLIENTE) TYPE(*CHAR) LEN(10) MIN(1) PROMPT('Cliente')
PARM KWD(DESDE)   TYPE(*DATE) PROMPT('Fecha desde')
PARM KWD(MODO)    TYPE(*CHAR) LEN(10) DFT(*NORMAL) +
                  SPCVAL((*NORMAL) (*SIMULA)) PROMPT('Modo')
```

**Ese fichero define un comando del sistema**, y con él se obtiene:

| Se obtiene | Sin escribir código |
|---|---|
| **Validación de tipos y longitudes** | el sistema la hace |
| **Valores especiales y por defecto** | declarados |
| **Ayuda contextual** | con `F1` sobre cada parámetro |
| **Petición interactiva de parámetros** | con `F4`: **un formulario generado** |
| **Y comprobación de autorización** | por comando |

**La cuarta fila es la que sorprende**: **pulsar F4 sobre un comando genera una pantalla con un campo por
parámetro, con su descripción y su ayuda** — automáticamente, desde la definición.

Es la interfaz de línea de comandos y la interfaz interactiva **generadas del mismo contrato**, que es
exactamente lo que la clase 160 pedía y lo que casi ninguna herramienta moderna consigue.

Y merece la comparación con el mundo Unix, porque las dos filosofías son coherentes:

```text
Unix:    el programa recibe una lista de cadenas y se apaña.
         Máxima flexibilidad, cero ayuda, cada herramienta a su manera.

IBM i:   el comando declara sus parámetros y el sistema hace lo demás.
         Consistencia total, y menos libertad.
```

**Y la consistencia tiene un valor que se nota**: en IBM i, **todos los comandos se comportan igual**
—`F1` ayuda, `F4` pide, los valores especiales empiezan por asterisco— y eso hace que aprender uno sea
aprender todos.

Es una idea que las herramientas modernas persiguen con especificaciones de línea de comandos declarativas
y con generadores de autocompletado — llegando al mismo sitio cuarenta años después.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 cli: procedure options(main);

    declare linea   char(200) varying;
    declare comando char(30) varying;
    declare i       fixed binary(31);
    declare cnt     fixed binary(31) initial(0);
    declare enpal   bit(1) initial('0'b);
    declare p       fixed binary(31);

    get edit (linea) (a(200));
    linea = trim(linea);

    p = index(linea, ' ');
    if p = 0 then
       comando = linea;
    else
       comando = substr(linea, 1, p - 1);

    do i = 1 to length(linea);
       if substr(linea, i, 1) = ' ' then
          enpal = '0'b;
       else if ^enpal then
          do;
             enpal = '1'b;
             cnt = cnt + 1;
          end;
    end;

    put skip list ('comando=' || comando || ' args=' || trim(char(cnt - 1)));

 end cli;
```

**PL/I como herramienta de línea de comandos.** PL/I recibe los parámetros de una forma que merece
explicarse porque es la del mainframe y es distinta de todo lo demás de esta página:

```pli
 miprog: procedure (parametros) options(main);
    declare parametros char(100) varying;
    ...
 end miprog;
```

```jcl
//PASO1 EXEC PGM=MIPROG,PARM='CLIENTE=4711,MODO=SIMULA'
```

**El `PARM` del JCL llega como una única cadena**, y **el programa la analiza**.

Y merece señalar la limitación histórica, porque explica una costumbre: **el `PARM` clásico está limitado
a 100 caracteres**.

Por eso, cuando hace falta más, **la configuración va por un fichero declarado en el JCL**:

```jcl
//PARAMS DD *
CLIENTE=4711
MODO=SIMULA
FECHA=2026-08-15
/*
```

**`DD *` mete los datos en el propio JCL**, así que **el trabajo y su configuración viajan juntos y se
versionan juntos** (clase 145).

Es una propiedad que merece destacarse porque el mundo moderno la ha redescubierto: **la configuración
junto a la definición del trabajo** es lo que hacen hoy los ficheros de las canalizaciones de integración
continua y los manifiestos de despliegue.

Y el código de retorno, que es la tercera propiedad del cierre de esta clase:

```pli
 declare plirest entry (fixed binary(31)) options(assembler);
 call plirest(8);       /* código de retorno 8 */
```

**O, más simple, con `return` desde el procedimiento principal** según el compilador.

Y merece cerrar con la observación que esta página permite hacer sobre la primera propiedad del cierre:
**en el mainframe, la salida no es "la salida estándar" — son ficheros declarados**.

```jcl
//SYSPRINT DD SYSOUT=*        <-- el informe
//ERRORES  DD DSN=...          <-- los errores, a otro sitio
//SALIDA   DD DSN=...           <-- los datos, a un tercero
```

**Cada flujo tiene su destino declarado en el JCL**, así que **la separación entre resultado, mensajes y
errores no es una convención: es explícita y se configura al ejecutar**.

Es más rígido que las tuberías de Unix y resuelve el mismo problema con más control — y es, otra vez, la
misma idea con distinta ropa.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
CLI ; Componente de linea de comandos -- clase 167
 read linea
 new i, cnt, comando, p
 set comando = $piece(linea, " ", 1)
 set cnt = 0
 for i = 1:1:$length(linea, " ") do
 . set p = $piece(linea, " ", i)
 . if p '= "" set cnt = cnt + 1
 write "comando=", comando, " args=", cnt - 1, !
 quit
```

**M como herramienta de línea de comandos.** M tiene acceso a los argumentos en las implementaciones
modernas, aunque no en el estándar:

```mumps
 ; YottaDB / GT.M
 write $zcmdline                  ; la línea de comandos completa
 set arg1 = $piece($zcmdline, " ", 1)
 zhalt 1                           ; código de salida
```

```bash
yottadb -run MIRUT arg1 arg2
mumps -run %XCMD 'do ^MIRUT'
```

**`$zcmdline` es una extensión `$Z`** (clase 146), así que **el código que la use no es portable entre
implementaciones**.

Y esta clase es el sitio para señalar que **el equivalente de la línea de comandos en este mundo es otra
cosa: el menú**.

```text
En VistA, el usuario no escribe comandos: navega por MENÚS,
definidos como datos en el fichero OPTION, con:
  - el nombre de la opción y su texto
  - la rutina o el menú al que lleva
  - las CLAVES DE SEGURIDAD que hacen falta (clase 153)
  - y la ayuda
```

**Y eso es, otra vez, una interfaz generada desde metadatos** (clase 149) — igual que los comandos de CL
en RPG en esta página.

Y merece la observación general, porque esta página la hace evidente: **las plataformas integradas
generan sus interfaces desde declaraciones; el mundo Unix las escribe a mano en cada programa**.

```text
Generada:  consistente, con ayuda, con permisos, y limitada a lo previsto.
A mano:    libre, inconsistente, y cada herramienta reinventa lo mismo.
```

Y la industria ha ido, lentamente, hacia la primera: **las especificaciones de línea de comandos en
ficheros, los generadores de autocompletado, y las herramientas que publican su interfaz en JSON** están
persiguiendo lo mismo.

Y para el proyecto de esta parte, la recomendación que se deriva es concreta: **declarar la interfaz de
la herramienta en un sitio** —una estructura, un fichero, una definición— **y generar de ahí el análisis,
la ayuda y la documentación**, en lugar de escribir las tres por separado y verlas divergir (clase 154).

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| linea args |

linea := stdin nextLine trimBoth.
args := linea substrings: ' '.

Transcript
    show: 'comando=', args first;
    show: ' args=', (args size - 1) printString;
    cr.
```

**Smalltalk como herramienta de línea de comandos.** Smalltalk puede hacerlo, y merece decir con
honestidad que **es de sus usos menos naturales**.

```smalltalk
"Pharo: acceso a los argumentos"
Smalltalk arguments.
Smalltalk os environment at: 'HOME'.
Smalltalk exitSuccess.
Smalltalk exit: 1.
```

```bash
./pharo miapp.image eval "Smalltalk arguments"
./pharo miapp.image miComando --opcion valor      # con Clap
```

Y el motivo de la fricción es el de la clase 144: **el artefacto es una imagen**, así que una herramienta
de línea de comandos escrita en Smalltalk **arrastra una imagen de decenas de megabytes** y **su arranque
tiene que cargarla**.

Y el ecosistema ha construido lo que faltaba:

| Herramienta | Notas |
|---|---|
| **Clap** | análisis de opciones y subcomandos, con documentación integrada |
| **`pharo eval`** | ejecutar una expresión desde el sistema operativo |
| **Reducción de imagen** | quitar lo que no se usa (clase 144) |

Y merece señalar el uso donde Smalltalk **sí** es la elección correcta para esta clase y que es real:
**la herramienta que analiza el propio sistema** (clase 165).

```bash
./pharo moose.image analizar --proyecto ../miapp --formato json
```

**Moose importa código de cualquier lenguaje y responde preguntas sobre él**, y ahí el coste de arranque
es irrelevante porque el análisis tarda minutos.

Es la regla general que esta clase deja: **el coste de arranque importa en proporción a lo que la
herramienta hace**. Para algo que se invoca mil veces en un bucle, C++ o Pascal; para algo que se lanza
una vez y trabaja diez minutos, da igual.

Y merece cerrar con la propiedad del cierre que Smalltalk cumple de forma natural y que conviene
aprovechar: **la salida estructurada**.

```smalltalk
STON toStringPretty: resultado.
NeoJSONWriter toString: resultado.
```

**Serializar el resultado es una línea** (clase 159), así que **añadir `--json` a una herramienta escrita
en Smalltalk es trivial** — y con eso cumple la cuarta propiedad del cierre y se convierte en un
componente que otros pueden consumir.

---

## Y de vuelta a la clase

Lo transferible: **una buena herramienta de línea de comandos es la que se deja usar por otro programa**.
Eso significa cuatro cosas concretas: **el resultado por la salida estándar y los mensajes por la de
error**, para que se pueda encauzar; **un código de salida que distinga bien de mal**, para que un guion
decida; **no preguntar nada si no hay terminal**, para que funcione desatendida; y **un formato de salida
estable o elegible** —`--json` cuando lo consuma una máquina—. Con esas cuatro, la herramienta se compone
con todo lo demás; sin ellas, es un callejón sin salida por muy bonita que sea.

⏮️ [Volver a la clase 167](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
