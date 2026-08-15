# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 145

> [⬅️ Volver a la clase 145](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Contar cuántos mensajes de *commit* hay en una línea. El programa es trivial; lo que no lo es, es que
**tres de los lenguajes de esta página no guardan su código en ficheros de texto**: RPG lo tuvo durante
décadas en ficheros de base de datos con números de secuencia, M lo tiene dentro de la propia base de
datos, y Smalltalk lo tiene dentro de una imagen binaria. **Git supone que el código son ficheros de
texto separados por saltos de línea**, y esa suposición es la clase entera.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es el **control de versiones y sus supuestos**, y estos lenguajes lo enseñan porque
> **cada uno rompe uno de ellos**. COBOL y Fortran tienen **formato por columnas**, así que un cambio de
> sangrado produce un diff enorme. RPG guardaba el fuente en **ficheros físicos con números de
> secuencia**. M vive en la base de datos. Smalltalk versiona **métodos, no líneas**. Y todos ellos han
> tenido que encajar en una herramienta que se diseñó para el núcleo de Linux.
>
> Y aparece la fricción concreta que cualquier proyecto poliglota sufre: **finales de línea,
> codificaciones, ficheros generados y binarios**.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: una línea con mensajes de commit (palabras separadas por espacio) → stdout: `commits=<cantidad>`
- **Regla:** `contar los mensajes`

| stdin | esperado |
|---|---|
| `fix add refactor` | `commits=3` |
| `init` | `commits=1` |
| `a b c d` | `commits=4` |

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
PROGRAM-ID. COMMITS.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(200).
01  I       PIC 9(4) COMP.
01  CNT     PIC 9(4) COMP VALUE 0.
01  ENPAL   PIC 9      VALUE 0.
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
        END-IF
    END-PERFORM

    MOVE CNT TO ED
    DISPLAY "commits=" FUNCTION TRIM(ED)
    STOP RUN.
```

**Lo que esta clase enseña en COBOL.** COBOL tiene el conflicto más directo con las herramientas
modernas de esta página, y es de formato: **el formato fijo por columnas**.

```text
Columnas 1-6:   número de secuencia (histórico: el número de la TARJETA)
Columna 7:      indicador: * comentario, - continuación, / salto de página
Columnas 8-11:  área A: divisiones, secciones, nombres de nivel 01 y 77
Columnas 12-72: área B: el resto del código
Columnas 73-80: identificación del programa (histórico)
```

**Ese formato viene de la tarjeta perforada de 80 columnas**, y las columnas 1-6 se usaban para
**reordenar la baraja si se caía al suelo**.

Y su consecuencia para esta clase es doble y muy práctica:

**Primera, muchos fuentes heredados llevan números de secuencia**, y hay herramientas que los
renumeran. **Renumerar cambia todas las líneas**, así que el diff resultante es del 100 % del fichero y
la revisión es imposible.

La regla es la del cierre de esta clase: **normalizar de una vez, en un *commit* que no haga otra cosa,
y no volver a tocarlo**.

**Y segunda, el área A y el área B importan**: mover una línea dos espacios **puede cambiar el
significado**. Así que **no se puede aplicar un formateador genérico** ni confiar en la sangría
automática de un editor que no conozca COBOL.

Y el formato libre —`>>SOURCE FORMAT FREE`, que este curso usa con `cobc -free`— es el estándar desde
COBOL 2002, y es la recomendación para código nuevo por exactamente esta razón.

Y hay una fricción específica del mundo mainframe que merece explicarse: **la codificación**.

**El fuente en z/OS está en EBCDIC**, no en ASCII ni en UTF-8. Así que llevarlo a git implica
**transcodificar**, y ahí aparecen problemas reales: **los caracteres que no existen en ambas
codificaciones** —el signo `¬`, la barra vertical, los corchetes— **cambian según la página de códigos
nacional**.

```text
En la página 037 (EE. UU.), el corchete izquierdo es x'BA'
En la 297 (Francia), esa posición es otra cosa
```

**Un fuente COBOL transcodificado con la página de códigos equivocada compila mal o no compila.**

Y por eso `.gitattributes` es imprescindible en un repositorio mainframe:

```text
*.cbl  working-tree-encoding=IBM-1047 text eol=lf
*.cpy  working-tree-encoding=IBM-1047 text eol=lf
```

**Git puede guardar en UTF-8 y presentar en EBCDIC**, con esa configuración. Es una capacidad poco
conocida y es justo lo que este caso necesita.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program commits
   implicit none
   character(len=200) :: linea
   integer :: i, cnt
   logical :: en_palabra

   read(*, '(A)') linea
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

   write(*, '(A,I0)') 'commits=', cnt
end program commits
```

**Lo que esta clase enseña en Fortran.** Fortran comparte el problema de COBOL en esta página —**el
formato fijo**— y con una historia igual de concreta:

```text
Columnas 1-5:   etiqueta numérica
Columna 6:      continuación (cualquier carácter distinto de espacio o 0)
Columnas 7-72:  el código
Columnas 73-80: ignoradas (números de secuencia)
```

**Y la columna 73 en adelante se IGNORA.** Esa es la trampa clásica: una línea de más de 72 caracteres
**se trunca en silencio**, y el compilador no avisa.

```fortran
      IF (X .GT. 0) CALL PROCESAR(A, B, C, D, E, F, G, H, VALOR_LARGO)
!                                                          ^ columna 73: TODO ESTO SE PIERDE
```

Y para esta clase, la consecuencia es la misma que en COBOL: **cualquier herramienta que reformatee o
reindente puede romper el código en silencio**, y un diff de reformateo es ilegible.

El formato libre —desde Fortran 90, con extensión `.f90`— es la recomendación evidente. Pero hay millones
de líneas en formato fijo, y de ahí las herramientas del ecosistema:

| Herramienta | Qué hace |
|---|---|
| **fprettify** | formateador para Fortran libre; sangrado y espaciado consistentes |
| **findent** | **convierte formato fijo a libre** y viceversa |
| **`.editorconfig`** | tabuladores frente a espacios, ancho de línea |

**`findent` merece la mención** porque hace la conversión que casi todo proyecto heredado acaba
necesitando, y la conversión es exactamente el tipo de cambio que **debe ir en su propio *commit***.

Y Fortran aporta a esta clase una fricción propia y muy común, que es la de la clase 143: **los ficheros
generados**.

```gitignore
*.mod        # generados por el compilador, atados a su versión
*.o
*.smod       # submódulos
build/
```

**Versionar un `.mod` es garantizarse conflictos sin significado**, porque es un binario que cambia con
cada compilación.

Y merece extraer la regla general, porque es la primera del cierre de esta clase y se viola
constantemente: **si un fichero se puede regenerar desde otro que está versionado, no se versiona**.

La excepción que sí conviene conocer: **cuando regenerarlo requiere una herramienta que no todo el
mundo tiene** —un generador de analizadores, un compilador de esquemas—, a veces se versiona el
resultado a propósito. Es una decisión legítima **si se toma conscientemente y se documenta**, y un
desastre si ocurre por descuido.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO; use Ada.Text_IO;
with Ada.Strings;
with Ada.Strings.Fixed;

procedure Commits is
   Linea      : String (1 .. 200);
   Ultimo     : Natural;
   Cnt        : Natural := 0;
   En_Palabra : Boolean := False;
begin
   Get_Line (Linea, Ultimo);

   for I in 1 .. Ultimo loop
      if Linea (I) = ' ' then
         En_Palabra := False;
      elsif not En_Palabra then
         En_Palabra := True;
         Cnt := Cnt + 1;
      end if;
   end loop;

   Put_Line ("commits=" &
             Ada.Strings.Fixed.Trim (Cnt'Image, Ada.Strings.Both));
end Commits;
```

**Lo que esta clase enseña en Ada.** El programa usa `'Image` con `Trim` para quitar el espacio inicial
del signo, y `Get_Line` con un parámetro `Ultimo` que devuelve cuántos caracteres se leyeron de verdad
— porque la cadena es de longitud fija (clase 093).

Y sobre control de versiones, Ada tiene una propiedad estructural que ayuda mucho y que merece
señalarse: **la separación de especificación y cuerpo en ficheros distintos** (clase 143).

```text
cliente.ads     <-- el contrato: cambia POCAS veces
cliente.adb      <-- la implementación: cambia MUCHO
```

**Un cambio en `.ads` es un cambio de interfaz, y un cambio en `.adb` no lo es.** Y eso se ve
directamente en el historial: **`git log -- '*.ads'` muestra la evolución de las interfaces del
sistema**, separada del ruido de la implementación.

Es una propiedad muy útil para revisar y para entender un sistema ajeno, y en lenguajes donde todo está
en un fichero no se puede obtener.

Y Ada tiene una convención de nombres que interactúa con los sistemas de ficheros y que conviene
conocer, porque produce conflictos reales en equipos mixtos:

```text
Mi_Paquete.Sub_Unidad   →   mi_paquete-sub_unidad.ads
```

**GNAT usa nombres de fichero en minúsculas derivados del nombre de la unidad**, con `-` para los
hijos. Y en macOS y Windows, **el sistema de ficheros no distingue mayúsculas de minúsculas**, así que
un fichero renombrado solo de mayúsculas **git no lo detecta como cambio** en esas plataformas.

Es una fricción de proyecto poliglota clásica, y la configuración que la evita:

```bash
git config core.ignorecase false
```

Y el ecosistema de Ada añade herramientas de formato que encajan con la segunda regla del cierre:

```bash
gnatpp -rnb *.adb          # formateador oficial, en su sitio
gnatcheck -rules -from=reglas.rules
```

**`gnatpp` es un formateador determinista**, así que **ponerlo en un gancho de pre-commit elimina para
siempre los diffs de estilo** — que es la práctica que esta clase recomienda y que en Ada tiene el
respaldo de una herramienta oficial.

Y merece nombrarse la práctica de los proyectos críticos que va más allá de lo habitual: **cada *commit*
enlaza con un requisito o un informe de problema**, y hay herramientas que **verifican la trazabilidad
completa** entre requisitos, código, pruebas y cambios.

Es una obligación de las normas de certificación, y es la versión estricta de "un *commit* cuenta una
cosa".

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Commits;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  Linea: string;
  I, Cnt: Integer;
  EnPalabra: Boolean;

begin
  ReadLn(Linea);
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

  WriteLn('commits=', IntToStr(Cnt));
end.
```

**Lo que esta clase enseña en Pascal.** El ecosistema Pascal aporta a esta clase el ejemplo canónico de
lo que **no** hay que versionar, y es una historia con mucha sangre: **los ficheros del diseñador
visual**.

```text
Unit1.pas    <-- el código: texto, se revisa bien
Unit1.dfm     <-- el FORMULARIO: posiciones, tamaños, propiedades de cada control
Unit1.lfm      <-- lo mismo en Lazarus
Project1.dproj  <-- XML del proyecto, reescrito por el IDE en cada guardado
```

**El `.dfm` es donde está el problema.** Es un fichero que el diseñador reescribe entero cada vez que
alguien mueve un control dos píxeles, y contiene la posición y el tamaño de todos ellos.

Consecuencias, todas reales:

- **Dos personas tocando el mismo formulario producen un conflicto casi seguro**, aunque hayan cambiado
  cosas distintas.
- **El conflicto es imposible de resolver a mano** con sensatez, porque el orden de las propiedades no
  es estable.
- **Y el `.dproj` cambia por sí solo** al abrir el proyecto, generando *commits* sin contenido.

Las prácticas que el ecosistema desarrolló:

```text
# guardar el formulario en TEXTO, no en binario (opción del IDE)
# y en .gitattributes:
*.dfm  text eol=crlf
*.pas  text eol=crlf
*.lfm  text eol=lf
*.dproj merge=ours          <-- no intentar fusionar; quedarse con el propio
```

**Y la regla de organización que de verdad funciona: un formulario, una persona.** Es una restricción
social impuesta por una limitación técnica, y es honesta reconocerla.

Y Pascal aporta la otra fricción clásica de esta página, y esta afecta a cualquier proyecto poliglota:
**los finales de línea**.

El mundo Delphi es de Windows y usa CRLF; Free Pascal en Linux usa LF. **Y un fichero que cambia de
final de línea aparece en git como modificado entero.**

```text
# .gitattributes: la solución correcta
*        text=auto              # normalizar a LF en el repositorio
*.pas    text eol=crlf           # ...y entregar CRLF a Windows
*.sh     text eol=lf              # los guiones SIEMPRE con LF
*.bat    text eol=crlf
*.png    binary
```

**`text=auto` guarda LF en el repositorio y entrega lo que cada plataforma espera.** Es la
configuración que todo repositorio poliglota debería tener desde el primer *commit*, y añadirla después
produce un cambio masivo que hay que aislar en su propio *commit*.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let ((linea (read-line))
      (cnt 0)
      (en-palabra nil))
  (loop for c across linea
        do (if (char= c #\Space)
               (setf en-palabra nil)
               (unless en-palabra
                 (setf en-palabra t)
                 (incf cnt))))
  (format t "commits=~D~%" cnt))
```

**Lo que esta clase enseña en Common Lisp.** `loop for c across linea` recorre una cadena carácter a
carácter — `across` es para vectores y `in` para listas, una distinción que `loop` mantiene explícita.

Y sobre control de versiones, Lisp tiene una fricción propia que merece explicarse, porque es directamente
el supuesto que esta clase cuestiona: **git compara por líneas, y el código Lisp es un árbol**.

```lisp
(defun procesar (datos)
  (let ((resultado '()))
    (dolist (d datos)
      (push (transformar d) resultado))
    (nreverse resultado)))
```

**Envolver ese cuerpo en un `handler-case` cambia la sangría de todas las líneas de dentro**, y el diff
muestra el bloque entero como modificado — cuando lo que pasó es que se añadió un nivel.

Es el mismo problema que cualquier lenguaje con bloques anidados, agravado porque **en Lisp la sangría
es muy significativa para la lectura** y la comunidad la respeta estrictamente.

Y las herramientas que lo mitigan:

```bash
git diff -w                    # ignorar cambios de espacio en blanco
git diff --word-diff            # comparar por PALABRAS, no por líneas
```

**`--word-diff` es especialmente útil en Lisp** por la densidad de las expresiones: una línea con seis
formas anidadas cambia entera aunque solo se toque una.

Y el ecosistema:

| Herramienta | Notas |
|---|---|
| **`cl-format` / `lisp-format`** | formateo automático, para ganchos de pre-commit |
| **SLIME + Paredit** | edición estructural: nunca se desequilibran los paréntesis |
| **`.dir-locals.el`** | reglas de sangría por proyecto, en Emacs |

Y Lisp aporta a esta clase una advertencia específica y muy suya, que viene de la Parte 8: **el estado
de la imagen no está en git**.

En un flujo de trabajo interactivo, es normal **redefinir funciones en el REPL** mientras se prueba. Y
entonces:

- **La imagen tiene una definición y el fichero tiene otra.**
- **Las pruebas pasan en la imagen y fallan en una construcción limpia.**
- **Y el cambio que hacía funcionar todo puede no haberse guardado nunca.**

Es el equivalente Lisp de "funciona en mi máquina", y la disciplina que lo evita es la que el ecosistema
recomienda: **recargar el sistema desde cero antes de dar nada por bueno**.

```lisp
(asdf:load-system "mi-proyecto" :force t)
```

Es la misma lección que Smalltalk en esta página, y viene del mismo sitio: **cuando el entorno de
desarrollo tiene estado, ese estado puede mentir**.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea

set n 0
foreach p [split [string trim $linea]] {
    if {$p ne ""} { incr n }
}

puts "commits=$n"
```

**Lo que esta clase enseña en Tcl.** Tcl está en el lado cómodo de esta clase —**el código es texto plano
sin formato obligatorio**— y aporta algo distinto: **es el lenguaje con el que se han automatizado
muchísimos flujos de control de versiones**.

Pero hay una fricción propia que merece explicarse, y es de las más frecuentes en proyectos poliglotas:
**los ganchos de git son guiones, y los guiones necesitan finales de línea LF**.

```bash
#!/usr/bin/env tclsh
# .git/hooks/pre-commit
```

**Si ese fichero se guarda con CRLF en Windows, falla con un mensaje incomprensible**:

```text
/usr/bin/env: 'tclsh': No such file or directory
```

**El `\r` acaba formando parte del nombre del intérprete.** Es uno de los errores más desconcertantes
que produce un repositorio mal configurado, y la solución está en `.gitattributes`:

```text
*.sh        text eol=lf
*.tcl       text eol=lf
hooks/*     text eol=lf
```

Y Tcl es especialmente adecuado para escribir esos ganchos, por lo mismo que la clase 140 señalaba:
**ejecutar programas y comparar salidas es su especialidad**.

```tcl
#!/usr/bin/env tclsh
# pre-commit: rechazar si algún fichero tiene tabuladores mezclados
set ficheros [exec git diff --cached --name-only --diff-filter=ACM]
foreach f [split $ficheros \n] {
    if {[file extension $f] ne ".tcl"} continue
    set fh [open $f]; set contenido [read $fh]; close $fh
    if {[string match "*\t*" $contenido]} {
        puts stderr "ERROR: $f contiene tabuladores"
        exit 1
    }
}
exit 0
```

Y merece señalar el principio general que hay detrás y que es la segunda regla del cierre: **lo que se
puede comprobar automáticamente no debe comprobarse en la revisión**.

Un revisor humano que dedica atención a los tabuladores **no la está dedicando a la lógica**. Los ganchos
y el formateador automático existen para liberar esa atención, y la clase 146 lo desarrolla.

Y una advertencia práctica sobre los ganchos que conviene conocer: **los ganchos locales no se
versionan** —viven en `.git/hooks`, que no está en el repositorio— así que **no se puede confiar en que
todo el mundo los tenga**.

La solución habitual es tenerlos en un directorio versionado y **apuntar `core.hooksPath` ahí**, o
—mejor— **hacer la misma comprobación también en la integración continua** (clase 147), que es el único
sitio donde no se puede saltar.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;

my @commits = split ' ', $linea;

print "commits=", scalar(@commits), "\n";
```

**Lo que esta clase enseña en Perl.** `scalar(@commits)` fuerza el contexto escalar de un arreglo, que es
su número de elementos — uno de los idiomas más característicos del lenguaje (clase 090).

Y sobre control de versiones, Perl tiene una conexión histórica directa que merece contarse: **git se
escribió inicialmente con una parte importante en Perl**.

`git-svn`, `git-send-email`, `git-cvsimport`, `git-request-pull` y varios más eran guiones de Perl, y
algunos lo siguen siendo. **La fontanería en C y la porcelana en guiones** fue la arquitectura original
de git, y Perl era el lenguaje de la porcelana.

Y Perl es todavía la herramienta natural para el trabajo que esta clase implica:

```perl
# reescribir el historial, analizar registros, migrar de un sistema a otro
git filter-branch --tree-filter 'perl -pi -e "s/viejo/nuevo/g" *.pl' HEAD
git log --format='%h %ae %s' | perl -ane '$c{$F[1]}++; END { ... }'
```

Y aporta a esta clase la advertencia más importante sobre la reescritura del historial, que merece
decirse con claridad:

**Reescribir el historial de un repositorio compartido rompe el de todos los demás.** `filter-branch`,
`filter-repo` y `rebase` sobre ramas publicadas **cambian los identificadores de todos los *commits*
posteriores**, y quien tenga el historial anterior se encontrará con dos versiones divergentes de la
misma historia.

Es una operación legítima —para quitar un fichero enorme, o unas credenciales filtradas— pero **exige
coordinar con todo el equipo**, y no se deshace.

Y hay un caso donde sí es obligatoria y esta clase debe nombrarlo, porque conecta con la clase 153: **si
se han filtrado credenciales al repositorio, borrarlas en un *commit* nuevo NO basta**.

```bash
git filter-repo --path secretos.env --invert-paths
```

**El *commit* antiguo sigue ahí y el secreto sigue siendo accesible** para cualquiera que clone. Hay que
reescribir el historial **y, en cualquier caso, rotar la credencial** — porque si estuvo publicada, hay
que darla por comprometida.

Y las herramientas para prevenirlo, que es lo que de verdad funciona:

```bash
git-secrets --install          # gancho que rechaza patrones de credenciales
gitleaks detect                 # escaneo del historial completo
trufflehog git file://.          # busca entropía alta: claves y tokens
```

**Ejecutarlas sobre el historial existente** es una de esas tareas que casi ningún proyecto hace y casi
todos deberían.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>
#include <string>

int main() {
    std::string palabra;
    int cnt = 0;
    while (std::cin >> palabra) ++cnt;

    std::cout << "commits=" << cnt << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** C++ aporta a esta clase el problema del proyecto grande, y es el
que justifica media herramienta moderna: **la fragmentación del código en dos ficheros por unidad**.

```text
geometria.hpp    <-- la declaración
geometria.cpp     <-- la definición
```

**Un cambio de firma toca los dos**, así que **el diff de un cambio simple aparece repartido**, y es
fácil actualizar uno y olvidar el otro — con el resultado de la clase 137: un error de enlace.

Y hay dos fricciones más que aparecen en cualquier proyecto C++ mediano:

**Primera, los ficheros generados y los submódulos.**

```gitignore
build/
*.o
*.so
compile_commands.json      # generado por CMake; útil pero NO se versiona
```

Y los submódulos de git, que el ecosistema C++ usa mucho por falta de gestor de paquetes (clase 143),
tienen fama merecida de problemáticos: **un submódulo apunta a un *commit* concreto, y quien clona sin
`--recursive` obtiene un directorio vacío** y un error de compilación desconcertante.

**Y segunda, el formato.** C++ permite tantos estilos que un equipo sin acuerdo produce diffs
inservibles. La solución es la que hoy se considera obligatoria:

```yaml
# .clang-format
BasedOnStyle: LLVM
IndentWidth: 4
ColumnLimit: 100
```

```bash
git clang-format          # formatear SOLO lo que se ha cambiado
```

**`git clang-format` es la pieza que hace esto práctico**: reformatea únicamente las líneas del cambio
actual, así que **no produce un diff masivo** al introducir el formateador en un proyecto existente.

Y sobre la introducción del formateador en un proyecto viejo, git tiene una característica poco conocida
que resuelve el problema del cierre de esta clase:

```bash
# 1. reformatear TODO en un commit que no hace nada más
git commit -am "Formateo con clang-format (sin cambios funcionales)"
git rev-parse HEAD >> .git-blame-ignore-revs

# 2. y decirle a git que lo ignore al atribuir líneas
git config blame.ignoreRevsFile .git-blame-ignore-revs
```

**`.git-blame-ignore-revs` hace que `git blame` salte esos *commits***, así que **la atribución sigue
apuntando a quien escribió la lógica**, no a quien pasó el formateador.

Es la respuesta al argumento más usado contra reformatear un proyecto antiguo, y GitHub y GitLab
respetan ese fichero.

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

dcl-pi COMMITS;
  linea char(200) const;
end-pi;

dcl-s i     int(10);
dcl-s cnt   int(10);
dcl-s enpal ind;

cnt = 0;
enpal = *off;

for i = 1 to %len(%trimr(linea));
  if %subst(linea : i : 1) = ' ';
    enpal = *off;
  elseif not enpal;
    enpal = *on;
    cnt += 1;
  endif;
endfor;

dsply ('commits=' + %char(cnt));

*inlr = *on;
return;
```

**Lo que esta clase enseña en RPG.** Aquí está el caso que el gancho de la clase anunciaba, y es el más
llamativo de esta página: **durante casi cuarenta años, el fuente de RPG no estuvo en ficheros de
texto**.

```text
MIBIB/QRPGLESRC        <-- un FICHERO FÍSICO de base de datos
   Miembro: MIPGM       <-- cada programa es un MIEMBRO
      Registro 1: SEQNBR=0001.00  DATE=880115  "     H DFTACTGRP(*NO)"
      Registro 2: SEQNBR=0002.00  DATE=920304  "     D cliente  S ..."
```

**Cada línea de código es una fila de una tabla**, con **su número de secuencia y su fecha de última
modificación**.

Y eso tiene implicaciones fascinantes para esta clase:

**A favor**: **cada línea sabe cuándo se cambió por última vez.** Es un `git blame` de granularidad de
línea, integrado en el almacenamiento, desde 1988. El editor SEU lo mostraba, y sigue ahí.

**En contra**: **es incompatible con todo lo demás.** No hay diff, no hay ramas, no hay fusión, no hay
historial de versiones —solo la última fecha— y desde luego no hay git.

Y de ahí que la modernización de la plataforma en la última década haya consistido, en buena parte, en
**sacar el fuente de los ficheros físicos y ponerlo en el IFS**, el sistema de ficheros de flujo:

```text
/home/proyecto/qrpglesrc/mipgm.rpgle     <-- un fichero de texto normal
```

Y con eso llegó todo lo demás:

| Herramienta | Qué permite |
|---|---|
| **Git en el IFS** | ramas, fusiones, revisión, historial completo |
| **ibmi-bob** | construir desde el IFS con `Makefile` (clase 144) |
| **Code4i / RDi** | editar en VS Code o Eclipse, compilar en el sistema |
| **`CPYFRMSTMF` / `CPYTOSTMF`** | mover entre IFS y ficheros físicos, con transcodificación |

Y hay dos fricciones que la migración destapó y que merecen conocerse:

**La codificación**, igual que en COBOL de esta página: **los fuentes en ficheros físicos están en
EBCDIC** —CCSID 37, 273, 297 según el país— y el IFS puede estar en UTF-8. La conversión es explícita y
la página de códigos hay que declararla.

**Y la longitud de línea**: los ficheros físicos de fuente tienen **ancho fijo** —92 o 112 caracteres—,
así que **el código nunca superó ese ancho**. Al pasar a ficheros de texto, esa restricción desaparece,
y conviene decidir un límite deliberadamente en lugar de heredarlo por accidente.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 commits: procedure options(main);

    declare linea  char(200) varying;
    declare i      fixed binary(31);
    declare cnt    fixed binary(31) initial(0);
    declare enpal  bit(1) initial('0'b);

    get edit (linea) (a(200));

    do i = 1 to length(linea);
       if substr(linea, i, 1) = ' ' then
          enpal = '0'b;
       else if ^enpal then
          do;
             enpal = '1'b;
             cnt = cnt + 1;
          end;
    end;

    put skip list ('commits=' || trim(char(cnt)));

 end commits;
```

**Lo que esta clase enseña en PL/I.** PL/I comparte con COBOL el mundo de esta página —**EBCDIC,
bibliotecas particionadas y gestores de configuración**— y aporta una perspectiva histórica que merece
recogerse, porque el control de versiones no empezó con git.

**La genealogía de la disciplina en el mainframe:**

| Época | Sistema | Qué aportó |
|---|---|---|
| Años 70 | **SCCS** (Unix, 1972) | el primer control de versiones: *deltas* |
| Años 70-80 | **Librarian**, **Panvalet** | versiones de miembros de PDS, con auditoría |
| Años 80-90 | **Endevor**, **ChangeMan** | promoción por entornos, aprobaciones, impacto |
| Hoy | **Git + Zowe / IDz** | el mainframe conectado al flujo moderno |

**SCCS es de 1972 y ya tenía la idea central**: guardar los cambios, no las copias.

Y los gestores de mainframe añadieron algo que git no tiene y que conviene conocer, porque no es una
carencia sino un enfoque distinto: **el flujo de aprobación como parte del sistema**.

```text
DEV → UNIT → QA → PRE → PROD
Cada promoción requiere:
  - la aprobación de un rol distinto al que hizo el cambio
  - que las pruebas de ese entorno hayan pasado
  - una ventana de cambio autorizada
  - y queda registrado quién aprobó qué y cuándo
```

**Eso es una obligación regulatoria en banca**, y es la razón de que estos sistemas parezcan pesados: **no
son un control de versiones, son un control de cambios**.

En el mundo moderno, ese papel lo cumplen las reglas de protección de ramas, las revisiones obligatorias
y los entornos con aprobación de las plataformas de integración continua — pero **la separación de
funciones** —quien escribe no aprueba, quien aprueba no despliega— **es un concepto que viene de aquí** y
que muchos equipos redescubren cuando les llega la primera auditoría.

Y merece cerrar con la razón por la que hoy el mainframe se conecta a git en lugar de sustituirlo:
**Zowe** —un proyecto abierto de la Open Mainframe Project— **expone z/OS por API REST**, así que **el
fuente puede vivir en git, la construcción se lanza desde una integración continua normal, y el resultado
se despliega en el mainframe**.

Es la reconciliación de los dos mundos de esta página, y es de la última década.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
COMMITS ; Contar mensajes -- clase 145
 read linea
 new i, cnt, p
 set cnt = 0
 for i = 1:1:$length(linea, " ") do
 . set p = $piece(linea, " ", i)
 . if p '= "" set cnt = cnt + 1
 write "commits=", cnt, !
 quit
```

**Lo que esta clase enseña en M.** M rompe el supuesto de esta clase de la forma más profunda: **el
código no está en ficheros, está en la base de datos** (clase 123).

Una rutina M vive como una entrada del sistema, y **no hay un fichero `MIRUT.m` en ningún directorio**
—salvo que alguien lo exporte a propósito.

Y de ahí que el control de versiones en M haya seguido dos caminos, y los dos merecen conocerse:

**El primero es el histórico, y es el de la clase 144: el sistema de parches de VistA.**

```text
Parche XU*8.0*655
  - descripción del problema y de la solución
  - rutinas afectadas, con su SUMA DE COMPROBACIÓN antes y después
  - requisitos previos: qué parches deben estar instalados
  - y todo el paquete distribuido como una global
```

**La suma de comprobación por rutina hace de identificador de versión**, y el sistema puede comprobar
si una rutina está en el estado que el parche espera **antes de tocarla**.

Es control de versiones basado en el contenido, no en el historial, y funciona sorprendentemente bien
para el problema que resuelve: **coordinar actualizaciones en cientos de instalaciones independientes
que pueden haber divergido**.

**Y el segundo es el moderno: exportar a ficheros y usar git.**

```mumps
 do ^%RO          ; exportar rutinas a un fichero de texto
 do ^%RI           ; importarlas
```

Y las implementaciones actuales lo han integrado:

| Sistema | Qué ofrece |
|---|---|
| **YottaDB** | rutinas como ficheros `.m` en disco, con `$ZROUTINES` |
| **GT.M** | igual: el fuente está en el sistema de ficheros |
| **InterSystems IRIS** | **exportación automática a ficheros al guardar**, para git |
| **VistA moderno** | repositorios git con las rutinas exportadas |

**La exportación automática al guardar es la solución práctica**: el desarrollador edita en el entorno
nativo, y **un gancho escribe el fichero de texto correspondiente**, que git ve.

Es exactamente lo mismo que Smalltalk resolvió con Tonel en esta página, y por la misma razón: **cuando
el entorno de desarrollo no usa ficheros, hay que fabricar una proyección a ficheros para que las
herramientas del mundo funcionen**.

Y merece extraer la observación general, porque explica por qué esta clase existe: **git ganó tan
completamente que hoy todo entorno de desarrollo tiene que proyectarse a ficheros de texto, aunque su
modelo interno sea otro**.

Los que no pueden —o no quieren— quedan fuera del ecosistema de revisión, integración continua y
automatización, y esa presión es la que ha modernizado estas plataformas en la última década.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| linea partes |

linea := stdin nextLine trimBoth.
partes := linea substrings: ' '.

Transcript show: 'commits=', partes size printString; cr.
```

**Lo que esta clase enseña en Smalltalk.** Smalltalk rompe el supuesto de esta clase de la manera más
interesante: **su unidad de cambio no es la línea ni el fichero — es el método**.

Y eso da un control de versiones **mejor** que el de ficheros para lo que esta clase busca, y **peor**
para todo lo demás.

**Monticello** (clase 143) compara así:

```text
Comparando MiPaquete-v12 con MiPaquete-v13:
  + Cliente >> #calcularDescuento:      (método AÑADIDO)
  - Cliente >> #metodoViejo              (ELIMINADO)
  ~ Pedido >> #total                      (MODIFICADO)
  + Clase: DescuentoEspecial
```

**Eso es un diff semántico**: dice qué métodos cambiaron, no qué líneas. Y con eso:

- **Mover un método de sitio en el fichero no aparece como cambio** —porque no hay fichero.
- **Reordenar métodos no genera conflicto.**
- **Y dos personas que tocan métodos distintos de la misma clase NO tienen conflicto**, aunque en un
  fichero estarían a diez líneas de distancia.

Ese último punto es una ventaja real y considerable: **la mayoría de los conflictos de fusión en
lenguajes de ficheros son artefactos de la representación**, no desacuerdos de verdad.

**Y la desventaja es la que la clase 144 anticipó: el mundo funciona con ficheros y con git.**

De ahí **Tonel** (2016), la solución que reconcilió Smalltalk con el ecosistema:

```text
src/
  MiPaquete/
    Cliente.class.st           <-- una clase, un fichero, en texto
    Cliente.extension.st
    package.st
```

**Tonel escribe cada clase en un fichero de texto legible**, con los métodos en orden estable, **para
que git pueda versionarlo, GitHub pueda mostrarlo y las herramientas de revisión funcionen**.

Y **Iceberg** es la herramienta que integra git dentro de Pharo: **hacer *commit*, cambiar de rama y
fusionar, desde el entorno**, con la imagen sincronizándose con el árbol de trabajo.

Y hay una fricción que merece nombrarse porque es la misma que Lisp señalaba en esta página y es
característica de los entornos con imagen: **la imagen y el repositorio pueden divergir**.

Se puede cambiar un método en la imagen y olvidar confirmarlo; o cambiar de rama y **quedarse con una
imagen que tiene métodos de las dos**. Iceberg avisa, pero la disciplina la pone la persona.

Y cierra esta clase con la observación que la atraviesa: **git ganó, y ganar significa que todo lo demás
se adapta a él**. Smalltalk tenía un modelo de versionado más fino y más adecuado a su lenguaje, y aun
así **construyó Tonel para poder hablar el idioma de todos** — porque el valor de estar en el ecosistema
común superó al de tener la mejor herramienta propia.

---

## Y de vuelta a la clase

Lo transferible: **el control de versiones no versiona código, versiona ficheros — y esa diferencia
tiene consecuencias**. De ahí las tres reglas que aparecen en toda esta página: **no versionar lo que se
genera**, porque produce conflictos que no significan nada; **normalizar el formato antes de que llegue
al repositorio**, con `.gitattributes` y un formateador automático, porque un cambio de estilo mezclado
con un cambio de lógica hace ilegible la revisión; y **hacer *commits* que cuenten una cosa**, porque el
historial es documentación y es lo único que quedará explicando por qué.

⏮️ [Volver a la clase 145](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
