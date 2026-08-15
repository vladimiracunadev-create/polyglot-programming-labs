# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 146

> [⬅️ Volver a la clase 146](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Un identificador es válido si está todo en minúsculas. Es una regla de estilo arbitraria, y ahí está el
punto de esta clase: **casi todas lo son**. Lo que no es arbitrario es **quién la comprueba**. Y esta
página tiene los dos extremos del mundo: **MISRA y las normas de certificación de Ada**, donde cada
desviación se documenta y se justifica ante un auditor, y **M**, donde la convención más importante
nació de un límite físico: **los nombres no podían pasar de ocho caracteres**.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es el **estándar de codificación y la revisión como proceso**, y estos lenguajes lo
> enseñan porque **inventaron la disciplina**. La revisión formal de código —con roles, actas y métricas—
> se formalizó en IBM en 1976, sobre programas COBOL y PL/I. Los estándares de codificación restrictivos
> —MISRA, JSF, SPARK— nacieron en C y Ada para sistemas donde un fallo mata. Y **Perl aportó la idea
> opuesta**: un analizador que aplica un libro de estilo, configurable y con severidades.
>
> Y aparece la pregunta que decide el valor de una revisión: **¿qué debe mirar una persona, y qué debe
> mirar una máquina?**
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: una palabra (identificador, solo letras) → stdout: `valido=<true|false>` (true si está todo en minúsculas)
- **Regla:** `valido si todos los caracteres son minúsculas`

| stdin | esperado |
|---|---|
| `total` | `valido=true` |
| `Total` | `valido=false` |
| `abc` | `valido=true` |

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
PROGRAM-ID. ESTILO.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(60).
01  I       PIC 9(4) COMP.
01  LG      PIC 9(4) COMP.
01  VALIDO  PIC X(5) VALUE "true".

PROCEDURE DIVISION.
    ACCEPT LINEA
    MOVE FUNCTION LENGTH(FUNCTION TRIM(LINEA)) TO LG

    PERFORM VARYING I FROM 1 BY 1 UNTIL I > LG
        IF LINEA(I:1) IS NOT ALPHABETIC-LOWER
            MOVE "false" TO VALIDO
        END-IF
    END-PERFORM

    DISPLAY "valido=" FUNCTION TRIM(VALIDO)
    STOP RUN.
```

**Lo que esta clase enseña en COBOL.** El programa usa **`ALPHABETIC-LOWER`**, una condición de clase
integrada en el lenguaje: COBOL tiene `NUMERIC`, `ALPHABETIC`, `ALPHABETIC-UPPER` y `ALPHABETIC-LOWER`
como comprobaciones nativas, más las clases definidas por el usuario con `CLASS`.

Y sobre revisión, aquí está el origen histórico que el "por qué" de esta clase anunciaba: **la
inspección de código formal, inventada por Michael Fagan en IBM en 1976**.

Y merece detallarse porque casi todo lo que hoy se hace en una revisión viene de ahí:

**Los roles están separados:**

- **Moderador**: dirige, no revisa el código; su papel es que la reunión no derive.
- **Autor**: presenta, **y no defiende** — explica.
- **Lector**: parafrasea el código en voz alta, línea a línea. **No es el autor.**
- **Inspectores**: buscan defectos contra una **lista de comprobación**.
- **Escriba**: registra cada defecto encontrado.

**Las reglas duras:**

- **Se buscan defectos, no soluciones.** Discutir cómo arreglarlo está prohibido en la reunión.
- **No se evalúa a la persona.** Los datos de la inspección **no pueden usarse para evaluar al autor**,
  o el proceso se corrompe de inmediato.
- **Hay preparación previa obligatoria**, con tiempo medido.
- **Y un ritmo máximo**: unas **150 líneas por hora**. Más rápido, y la eficacia se desploma.

**Los datos de IBM fueron contundentes**: las inspecciones encontraban entre el 60 % y el 90 % de los
defectos, y **detectarlos ahí costaba entre 10 y 100 veces menos que en producción**.

Y el dato del ritmo sigue siendo la crítica más útil a la revisión moderna: **una petición de cambios de
800 líneas revisada en veinte minutos no es una revisión**. Los estudios de Cisco y SmartBear de los
años 2000 confirmaron el mismo límite, con el mismo número.

Y las herramientas actuales del mundo COBOL:

| Herramienta | Qué comprueba |
|---|---|
| **SonarQube (plugin COBOL)** | complejidad, duplicación, reglas de mantenibilidad |
| **cobolint / GnuCOBOL `-Wall`** | avisos del compilador como norma |
| **CAST / Micro Focus Enterprise Analyzer** | análisis de sistemas enteros y grafo de impacto |
| **`GO TO` prohibido salvo `GO TO ... EXIT`** | la regla de estilo más extendida en COBOL |

**La última merece explicarse**: COBOL permite `ALTER` y saltos arbitrarios, y el estándar de facto de
la industria desde los años ochenta es **prohibirlos** — dejando solo `GO TO` hacia la etiqueta de
salida de un párrafo.

Es la aplicación práctica de la programación estructurada, impuesta por norma de equipo, en un lenguaje
que nunca la impuso.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program estilo
   implicit none
   character(len=60) :: linea
   integer :: i, n, c
   logical :: valido

   read(*, '(A)') linea
   n = len_trim(linea)
   valido = n > 0

   do i = 1, n
      c = iachar(linea(i:i))
      if (c < iachar('a') .or. c > iachar('z')) valido = .false.
   end do

   if (valido) then
      write(*, '(A)') 'valido=true'
   else
      write(*, '(A)') 'valido=false'
   end if
end program estilo
```

**Lo que esta clase enseña en Fortran.** El programa compara con `iachar`, que da el código **ASCII**
del carácter — frente a `ichar`, que da el del juego de caracteres del procesador. En una máquina
EBCDIC eso importa, y usar `iachar` hace el programa portable.

Y sobre estándares, Fortran tiene el suyo escrito en la primera línea de todos los programas de este
curso: **`implicit none`**.

La clase 137 contó por qué. Aquí importa la otra mitad: **es una regla de estilo que el compilador puede
imponer**.

```bash
gfortran -fimplicit-none -Wall -Wextra -std=f2018 -pedantic
```

**`-std=f2018 -pedantic` rechaza las extensiones no estándar**, que es la regla más valiosa en un
lenguaje con sesenta años de extensiones específicas de cada fabricante.

Y las reglas que la comunidad científica ha consolidado, y que merecen conocerse porque son sustanciales:

| Regla | Motivo |
|---|---|
| **`implicit none` siempre** | los nombres mal escritos crean variables (clase 137) |
| **Todo en `module`** | activa la comprobación de interfaces (clase 109) |
| **`intent(in/out/inout)` en cada argumento** | documenta y hace comprobar la dirección |
| **`private` por defecto en los módulos** | `public :: solo_lo_que_exporto` |
| **Nada de `common`, `equivalence` ni `goto` calculado** | de la era de las tarjetas |
| **`real(dp)` con `dp` de `iso_fortran_env`** | y nunca `real*8`, que no es estándar |
| **`pure` y `elemental` donde se pueda** | permite optimizar y documenta que no hay efectos |

**`intent` merece el detalle**, porque es una regla de estilo con consecuencias reales: declarar
`intent(in)` **hace que el compilador rechace cualquier modificación del argumento**, y **permite pasar
por referencia sin copia con seguridad**.

Es documentación que el compilador comprueba, que es lo mejor que puede ser una convención.

Y las herramientas:

```bash
fprettify --indent 3 --strict-indent      # formateo determinista
fortran-linter prog.f90
findent -ofree                              # convertir formato fijo a libre
```

Y merece cerrar con la observación cultural que esta clase permite: **el código científico se revisa
poco**, porque históricamente lo escribía **una persona sola, para su propia tesis**, y nadie más lo
leía.

La consecuencia se ve en el legado: programas de cien mil líneas sin pruebas, sin módulos y con
variables de tres letras. Y la respuesta de la comunidad en la última década —revistas que exigen el
código, revisión de software científico, iniciativas como el *Journal of Open Source Software*— es
exactamente esta clase aplicada a un campo que la necesitaba.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO; use Ada.Text_IO;

procedure Estilo is
   Linea  : String (1 .. 60);
   Ultimo : Natural;
   Valido : Boolean;
begin
   Get_Line (Linea, Ultimo);
   Valido := Ultimo > 0;

   for I in 1 .. Ultimo loop
      if Linea (I) not in 'a' .. 'z' then
         Valido := False;
      end if;
   end loop;

   if Valido then
      Put_Line ("valido=true");
   else
      Put_Line ("valido=false");
   end if;
end Estilo;
```

**Lo que esta clase enseña en Ada.** `Linea (I) not in 'a' .. 'z'` usa la pertenencia a un rango de un
tipo enumerado —`Character` lo es— que es una construcción del lenguaje, no una comparación numérica.

Y sobre estándares, Ada tiene los más estrictos de esta página, y merece ver cómo funcionan de verdad.

**Primero, el lenguaje impone restricciones por declaración:**

```ada
pragma Restrictions (No_Allocators);              --  prohibido reservar en el montón
pragma Restrictions (No_Recursion);                --  prohibida la recursión
pragma Restrictions (No_Secondary_Stack);           --  sin pila secundaria
pragma Restrictions (No_Exception_Propagation);      --  las excepciones no suben
pragma Restrictions (Max_Tasks => 8);                 --  como mucho ocho tareas
pragma Profile (Ravenscar);                            --  el perfil de tiempo real
```

**Esas restricciones las comprueba el compilador y se niega a compilar si se violan.** No son
recomendaciones: son parte del programa.

**Y el perfil Ravenscar** es un conjunto de restricciones sobre la concurrencia (clase 135) que hace el
sistema **analizable**: sin creación dinámica de tareas, sin entradas con guardas complejas, con
prioridades fijas — de modo que **se puede demostrar que se cumplen los plazos**.

Es una decisión de ingeniería que merece entenderse: **se renuncia deliberadamente a la mitad del
lenguaje para poder demostrar propiedades**. Y funciona: Ravenscar se usa en satélites y en control de
vuelo.

**Segundo, las normas del sector:**

| Norma | Ámbito |
|---|---|
| **DO-178C** | aviónica; niveles A a E, con MC/DC en el nivel A |
| **EN 50128** | ferrocarril |
| **IEC 61508** | seguridad funcional industrial |
| **JSF++ / MISRA** | los equivalentes en C++ y C |
| **AdaCore Coding Standard** | el estándar de estilo con `gnatcheck` |

**Y la propiedad que las define todas**: cada desviación **se documenta, se justifica técnicamente y la
aprueba un auditor**. No hay "lo dejo así porque tengo prisa".

**Y tercero, las herramientas:**

```bash
gnatcheck -rules -from=proyecto.rules      # reglas de codificación
gnatmetric                                  # complejidad ciclomática, anidamiento
gnatpp                                       # formateo determinista
gnatprove                                     # DEMOSTRACIÓN de ausencia de errores
```

Y merece cerrar con lo que esto significa para la revisión humana, porque es la respuesta a la pregunta
del "por qué" de esta clase: **cuando las reglas mecánicas las aplica el compilador y las propiedades
las demuestra una herramienta, la revisión humana se dedica íntegramente a si el requisito es el
correcto**.

Y en estos sistemas ese es, de hecho, el sitio donde están los fallos que matan: **no en el código, en la
especificación**.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Estilo;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  Linea: string;
  I: Integer;
  Valido: Boolean;

begin
  ReadLn(Linea);
  Linea := Trim(Linea);
  Valido := Length(Linea) > 0;

  for I := 1 to Length(Linea) do
    if not (Linea[I] in ['a'..'z']) then
      Valido := False;

  if Valido then
    WriteLn('valido=true')
  else
    WriteLn('valido=false');
end.
```

**Lo que esta clase enseña en Pascal.** `Linea[I] in ['a'..'z']` usa **el operador de conjuntos** de
Pascal (clase 094): `['a'..'z']` es un conjunto literal, y `in` comprueba la pertenencia en una sola
instrucción de máquina, con máscaras de bits.

Es una construcción de 1970 que sigue siendo más legible que la comparación doble de casi todos los
lenguajes de esta página.

Y sobre estilo, Pascal tiene una historia particular: **fue diseñado como lenguaje de enseñanza**, y eso
le dio una cultura de estilo explícita desde el principio.

Las convenciones del ecosistema, muy estables desde los años noventa:

| Convención | Ejemplo |
|---|---|
| Tipos con `T` | `TCliente`, `TFormaPago` |
| Interfaces con `I` | `IRepositorio` |
| Campos privados con `F` | `FNombre` |
| Argumentos con `A` | `ANombre` |
| **PascalCase** para todo lo público | `CalcularTotal` |
| Constantes con prefijo del grupo | `clRojo`, `mrOk` |

**El prefijo `F` para campos merece la explicación**, porque no es capricho: en Delphi, **una propiedad
y su campo de respaldo tienen el mismo nombre conceptual**:

```pascal
private
  FNombre: string;
published
  property Nombre: string read FNombre write SetNombre;
```

**Sin el prefijo, habría colisión**, así que la convención resuelve una restricción real del lenguaje. Y
esa es la clase de regla de estilo que sobrevive: **la que resuelve algo**.

Y las herramientas del ecosistema:

```bash
ptop -c ptop.cfg entrada.pas salida.pas    # el formateador de Free Pascal
```

| Herramienta | Qué hace |
|---|---|
| **`ptop`** | formateador incluido en Free Pascal |
| **Jedi Code Format** | el formateador de referencia en Delphi |
| **Pascal Analyzer (Peganza)** | análisis estático profundo: variables no usadas, ámbitos |
| **`{$WARN ... ERROR}`** | convertir avisos concretos en errores |

**`{$WARN SYMBOL_DEPRECATED ERROR}` merece la mención**, porque es la forma limpia de aplicar una regla
de equipo: **marcar lo obsoleto y hacer que su uso no compile**.

```pascal
procedure MetodoViejo; deprecated 'usa MetodoNuevo';
```

Es documentación, aviso y regla de estilo en una declaración, y el compilador la hace cumplir — que es
lo que el cierre de esta clase pide.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let ((palabra (string-trim '(#\Space #\Return) (read-line))))
  (format t "valido=~A~%"
          (if (and (plusp (length palabra))
                   (every #'lower-case-p palabra))
              "true" "false")))
```

**Lo que esta clase enseña en Common Lisp.** `every` con `#'lower-case-p` es la forma idiomática de
comprobar una propiedad sobre toda una secuencia (clase 115), y `plusp` comprueba que sea positiva —Lisp
tiene predicados con nombre para casi todo.

Y sobre estilo, Lisp tiene convenciones muy consolidadas y **muy informativas**, porque **el nombre dice
el tipo de cosa**:

| Convención | Significado |
|---|---|
| `nombre-p` / `nombrep` | **predicado**: devuelve verdadero o falso |
| `*variable-global*` | *earmuffs*: **variable especial** (clase 088) |
| `+constante+` | constante definida con `defconstant` |
| `%interno%` o `%funcion` | **de bajo nivel**, no usar desde fuera |
| `nombre!` (raro en CL) | destructivo — en Scheme es la norma |
| `n` de prefijo: `nreverse` | **destructivo**: reutiliza la estructura |
| `with-...` | macro que establece un contexto y lo deshace |
| `do-...` | macro de iteración |
| `define-...` / `def...` | definición |

**Los asteriscos de `*variable*` merecen destacarse** porque no son decorativos: marcan que la variable
tiene **alcance dinámico** (clase 088), y **enlazarla con `let` afecta a todo lo que se llame desde
ahí**.

Confundir una variable especial con una léxica produce fallos muy difíciles de encontrar, y **la
convención de nombres es la única defensa**, porque el lenguaje no lo distingue sintácticamente.

Es un ejemplo perfecto de la regla del cierre: **una convención que codifica información que el
compilador no da**.

Y el prefijo `n` de los destructivos —`nreverse`, `nconc`, `nsubst`— es igual de sustancial: avisa de
que **la estructura de entrada puede quedar destrozada**, que es la diferencia entre un programa
correcto y uno con corrupción silenciosa (clase 102).

Las herramientas:

```bash
sbcl --eval '(compile-file "prog.lisp")'    # los avisos del compilador SON el analizador
```

| Herramienta | Notas |
|---|---|
| **Los avisos de SBCL** | inferencia de tipos, variables sin usar, notas de optimización |
| **`lisp-critic`** | sugiere idiomas más limpios; nació para enseñar |
| **`sblint` / `sbcl-lint`** | los avisos en formato consumible |
| **`(declaim (optimize (safety 3) (debug 3)))`** | la política de compilación como norma |

**`lisp-critic` es curioso y merece la mención**: es un sistema experto con reglas del estilo *"esto es
un `(if x t nil)`, escribe `x` a secas"*, escrito para enseñar buen estilo Lisp a estudiantes.

Es el antepasado directo de los analizadores que sugieren idiomas, y es de los años noventa.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea
set p [string trim $linea]

if {$p ne "" && [string is lower -strict $p]} {
    puts "valido=true"
} else {
    puts "valido=false"
}
```

**Lo que esta clase enseña en Tcl.** **`string is lower -strict`** hace el trabajo entero: Tcl tiene una
familia de comprobaciones de clase —`alpha`, `digit`, `integer`, `double`, `boolean`, `space`, `xdigit`,
`wordchar`— y **`-strict` es la parte importante**: sin él, **la cadena vacía devuelve verdadero**.

Es una decisión de diseño discutible que ha causado muchos fallos, y por eso `-strict` es prácticamente
obligatorio en código serio. Es un buen ejemplo de regla de estilo con motivo.

Y Tcl tiene un estándar de estilo con nombre y con autoridad: **las *Tcl Style Guidelines* de John
Ousterhout**, el creador del lenguaje, publicadas en 1997.

Y sus reglas principales siguen siendo el estándar de facto:

| Regla | Motivo |
|---|---|
| **Llaves siempre en `expr` y en `if`**: `if {$x > 5}` | **sin llaves, hay doble sustitución: es un riesgo de inyección** |
| **`{*}` en lugar de `eval`** | `eval` sobre datos ajenos es ejecución de código |
| Espacios de nombres para todo paquete | evita colisiones globales (clase 086) |
| `::` explícito para las globales | deja claro el alcance |
| Comentarios con `#` **al principio de comando** | `#` a mitad de línea **no es un comentario** |

**La primera es la más importante y merece explicarse**, porque es a la vez estilo, rendimiento y
seguridad:

```tcl
if {$x > 5} { ... }        ;# CORRECTO: la expresión se compila una vez
if "$x > 5" { ... }         ;# MAL: se sustituye y se reanaliza CADA VEZ
```

**Sin llaves, el valor de `$x` se pega al texto y luego se analiza como expresión.** Si `$x` contiene
`1] ; exec rm -rf /  ; expr [1`, **eso se ejecuta**.

Es una inyección de código idéntica en naturaleza a la inyección SQL (clase 153), y la regla de estilo
—**pon llaves siempre**— es la defensa completa.

Y de paso es más rápido: **con llaves, el compilador de bytecode de Tcl compila la expresión una sola
vez** (clase 125).

Es el mejor ejemplo de esta página de una regla de estilo que **no es cosmética**: protege de una
vulnerabilidad y multiplica el rendimiento.

Y las herramientas:

```bash
nagelfar prog.tcl        # análisis estático: aridades, comandos, citación
frink -w prog.tcl         # formateo y comprobación de estilo
tclchecker                 # el de ActiveState
```

**Nagelfar detecta precisamente los `expr` sin llaves**, entre otras cosas, y es la herramienta que
convierte estas reglas en algo comprobable — que es lo que el cierre de esta clase exige.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $palabra = <STDIN>;
chomp $palabra;

print "valido=", ($palabra =~ /^[a-z]+$/ ? 'true' : 'false'), "\n";
```

**Lo que esta clase enseña en Perl.** La expresión regular `^[a-z]+$` resuelve el problema en una línea,
y es el argumento de Perl entero: **para trabajar con texto, la herramienta correcta es una expresión
regular** (clase 093).

Y sobre estándares, Perl aportó a esta clase algo que merece contarse, porque **cambió cómo la industria
piensa los estándares de estilo**.

En 2005, Damian Conway publicó **Perl Best Practices**: 256 reglas de estilo, **cada una con su
justificación**. Y al año siguiente, Jeffrey Ryan Thalhammer escribió **`Perl::Critic`**, un analizador
que **aplica esas reglas** — con dos características que hoy son estándar en todos los analizadores y
que entonces no lo eran:

**Primera, severidades:**

```bash
perlcritic --brutal prog.pl      # nivel 1: TODO, incluso lo discutible
perlcritic --cruel prog.pl        # nivel 2
perlcritic --harsh prog.pl         # nivel 3
perlcritic --stern prog.pl          # nivel 4
perlcritic --gentle prog.pl          # nivel 5: solo lo grave (por defecto)
```

**Que las reglas tengan severidad graduable es lo que permite adoptarlas en un proyecto existente**: se
empieza por lo grave y se sube el listón con el tiempo.

**Y segunda, la configuración por proyecto y las excepciones justificadas:**

```perl
# .perlcriticrc
severity = 3
[-Subroutines::ProhibitExplicitReturnUndef]
[Variables::ProhibitPunctuationVars]
allow = $@ $! $0
```

```perl
## no critic (ProhibitStringyEval)
my $r = eval $codigo;   # justificado: el código viene de la configuración firmada
## use critic
```

**La anotación en línea con el nombre de la regla concreta** obliga a decir **qué** se está saltando, y
deja constancia en el código.

Es el modelo que hoy tienen `eslint-disable`, `# noqa`, `#[allow(...)]` y `// NOLINT`, y **viene de
aquí**.

Y hay una regla de Perl Best Practices que merece citarse porque es la más contraintuitiva y la más
útil:

> **Escribe las expresiones regulares con `/x`**, que permite espacios y comentarios dentro.

```perl
if ($fecha =~ m{
        ^(\d{4})    # año
        -(\d{2})     # mes
        -(\d{2})$     # día
    }x) { ... }
```

**Una expresión regular comentada es legible; una de sesenta caracteres no lo es.** Y en un lenguaje
famoso por producir código ilegible, la respuesta de su comunidad no fue prohibir la característica: fue
**dar una forma legible de usarla**.

Es el mejor resumen de la filosofía de esta clase: **los estándares no están para limitar el lenguaje,
están para que el código siga siendo legible dentro de dos años**.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <algorithm>
#include <cctype>
#include <iostream>
#include <string>

int main() {
    std::string palabra;
    if (!(std::cin >> palabra)) return 1;

    const bool valido = !palabra.empty() &&
        std::all_of(palabra.begin(), palabra.end(),
                    [](unsigned char c) { return std::islower(c) != 0; });

    std::cout << "valido=" << (valido ? "true" : "false") << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** El `unsigned char` en el parámetro de la lambda **no es
decorativo**: pasar un `char` con signo negativo a `std::islower` es **comportamiento indefinido**, y es
uno de los errores más frecuentes y menos conocidos de la biblioteca estándar de C.

Es exactamente el tipo de regla que un estándar de codificación debe recoger y una herramienta debe
comprobar, porque **nadie lo recuerda**.

Y C++ tiene los estándares más elaborados de esta página, cada uno con su motivo:

| Estándar | Ámbito | Carácter |
|---|---|---|
| **C++ Core Guidelines** | general; Stroustrup y Sutter | recomendaciones, con herramienta |
| **MISRA C++** | automoción | restrictivo; se prohíbe mucho |
| **AUTOSAR C++14** | automoción moderna | fusionado hoy con MISRA |
| **JSF++** | aviónica militar (F-35) | el más estricto: 221 reglas |
| **CERT C++** | seguridad | centrado en vulnerabilidades |
| **Google / LLVM style** | industria | sobre todo formato y nombres |

**Y el patrón común de los restrictivos merece verse**, porque enseña qué se considera peligroso:

```text
Prohibido: reserva dinámica después del arranque
Prohibido: excepciones (¡en JSF++ y en muchos sistemas embarcados!)
Prohibido: herencia múltiple de clases con implementación
Prohibido: sobrecarga de operadores salvo casos listados
Prohibido: recursión
Prohibido: goto, salvo salida de bucles anidados
Obligatorio: llaves en TODO if, incluso de una línea
```

**"Prohibidas las excepciones" sorprende y tiene un motivo concreto**: el tiempo de propagación de una
excepción **no está acotado**, porque depende de cuántos destructores haya que ejecutar. En un sistema
con plazos duros, eso es inaceptable.

Es la misma lógica que las restricciones de Ada en esta página: **se renuncia a características para
poder demostrar propiedades temporales**.

Y las herramientas, que en C++ son de las mejores que existen:

```bash
clang-tidy --checks='cppcoreguidelines-*,modernize-*,bugprone-*' prog.cpp
clang-format -i prog.cpp
cppcheck --enable=all prog.cpp
g++ -Wall -Wextra -Wpedantic -Wshadow -Wconversion -Werror
include-what-you-use prog.cpp
```

**`clang-tidy` con `modernize-*` merece la mención final**, porque hace algo poco común: **reescribe el
código**.

```bash
clang-tidy --fix --checks='modernize-use-nullptr,modernize-loop-convert' *.cpp
```

Convierte `NULL` en `nullptr`, bucles con índice en bucles por rango, `typedef` en `using`. **Es
migración automatizada de estilo a escala de millones de líneas**, y es la respuesta a la objeción de
que un estándar nuevo no se puede aplicar a código existente.

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

dcl-pi ESTILO;
  palabra char(60) const;
end-pi;

dcl-s texto  varchar(60);
dcl-s i      int(10);
dcl-s valido ind;

texto = %trim(palabra);
valido = %len(texto) > 0;

for i = 1 to %len(texto);
  if %subst(texto : i : 1) < 'a' or %subst(texto : i : 1) > 'z';
    valido = *off;
  endif;
endfor;

if valido;
  dsply 'valido=true';
else;
  dsply 'valido=false';
endif;

*inlr = *on;
return;
```

**Lo que esta clase enseña en RPG.** RPG es el caso más dramático de esta página en materia de estándares
de codificación, porque **el estándar cambió el lenguaje entero**.

Comparar las dos formas explica por sí solo lo que es un estándar de estilo:

```text
     C                   EVAL      TOTAL = PRECIO * CANTIDAD
     C                   IF        TOTAL > 1000
     C                   EVAL      DESCUENTO = TOTAL * 0.1
     C                   ENDIF
```

```rpgle
total = precio * cantidad;
if total > 1000;
  descuento = total * 0.1;
endif;
```

**Lo primero es RPG de formato fijo por columnas** —herencia de la tarjeta perforada, igual que COBOL y
Fortran en esta página—: la columna 6 es el tipo de especificación, la 7-11 el nivel, la 12-25 el factor
1, la 26-35 la operación...

**Y lo segundo es el mismo lenguaje en formato totalmente libre**, disponible desde 2013.

Y el estándar de la comunidad hoy es inequívoco:

| Regla | Motivo |
|---|---|
| **Formato totalmente libre para todo lo nuevo** | legibilidad, herramientas, git (clase 145) |
| **Nada de indicadores numéricos** (`*IN03`) | usar nombres: `dcl-s salir ind` |
| **Procedimientos, no subrutinas** | ámbito local y parámetros, en vez de globales |
| **Programas de servicio para la lógica** | permite pruebas unitarias (clase 139) |
| **`dcl-s`, `dcl-ds`, `dcl-pr` explícitos** | frente a las especificaciones D |
| **SQL embebido en lugar de acceso registro a registro** | conjuntos en vez de bucles (clase 117) |
| **Sin `goto`, sin `cabxx`** | de la era de los operadores de comparación con salto |

**"Nada de indicadores" merece la explicación**, porque es la seña de identidad del RPG antiguo: el
lenguaje tenía **99 indicadores numéricos globales** —`*IN01` a `*IN99`— que servían para todo:
condiciones, teclas de función, control de errores.

```text
     C                   IF        *IN03
```

**Nadie sabe qué es `*IN03` sin buscar en la pantalla o en la documentación.** Es el ejemplo perfecto de
una convención que el hardware impuso y que se mantuvo cuarenta años por inercia.

Y la modernización real de RPG consistió en **darle nombre a las cosas** — que es, reducido a lo
esencial, de lo que trata esta clase entera.

Las herramientas:

| Herramienta | Qué hace |
|---|---|
| **RDi / Code4i** | verificador de sintaxis, formateo, navegación |
| **ARCAD Observer / Transformer** | **conversión automática de fijo a libre** |
| **SonarQube (plugin RPG)** | métricas y reglas |
| **`OPTION(*SRCSTMT)`** | números de sentencia del fuente en los errores |

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 estilo: procedure options(main);

    declare palabra char(60) varying;
    declare i       fixed binary(31);
    declare valido  bit(1) initial('1'b);
    declare c       char(1);

    get edit (palabra) (a(60));
    palabra = trim(palabra);

    if length(palabra) = 0 then valido = '0'b;

    do i = 1 to length(palabra);
       c = substr(palabra, i, 1);
       if c < 'a' | c > 'z' then valido = '0'b;
    end;

    if valido then
       put skip list ('valido=true');
    else
       put skip list ('valido=false');

 end estilo;
```

**Lo que esta clase enseña en PL/I.** PL/I es el lenguaje que mejor ilustra **por qué existen los
estándares de codificación restrictivos**, porque es el caso de estudio del problema opuesto: **un
lenguaje que lo permite todo**.

PL/I se diseñó en 1964 para unificar el mundo científico de Fortran y el comercial de COBOL, **y añadió
además concurrencia, procesamiento de listas, manejo de excepciones y programación de sistemas**.

El resultado fue enorme, y la reacción de la comunidad académica fue igual de célebre: **Edsger
Dijkstra escribió que era un lenguaje "demasiado barroco para ser dominado"** y **Niklaus Wirth diseñó
Pascal en gran medida como respuesta** — un lenguaje pequeño, con una sola forma de hacer cada cosa.

**Pascal y PL/I son las dos filosofías de esta clase en estado puro**, y las dos siguen vivas: los
lenguajes que dan un camino y los que dan veinte.

Y la solución práctica en PL/I fue la de esta clase: **subconjuntos de uso obligatorio**.

```text
Estándares típicos de una instalación PL/I:
  - Prohibido DEFAULT: declarar TODO explícitamente
  - Prohibido el alias por DEFINED y BASED salvo casos aprobados
  - Prohibidas las conversiones implícitas: conversión explícita siempre
  - Un solo punto de retorno por procedimiento
  - Prefijos de condición obligatorios: (SUBSCRIPTRANGE, STRINGRANGE, SIZE)
  - Nada de GOTO fuera del bloque
```

**"Prohibido `DEFAULT`" merece la explicación**, porque es la característica más peligrosa del lenguaje:

```pli
 default range(a:z) fixed binary(31);   /* TODO lo no declarado es entero */
```

**`DEFAULT` permite redefinir las reglas de tipos implícitos para todo un programa.** Es potentísimo y
convierte el código en ilegible para quien no vio esa línea — el mismo problema que el `implicit` de
Fortran en esta página, elevado a norma configurable.

Y las opciones del compilador que aplican el estándar:

```text
PP(MACRO) FLAG(W) RULES(NOLAXDCL, NOLAXCTL, NOLAXIF, NOLAXQUAL)
```

**`RULES(NOLAXDCL)` exige que todo esté declarado**, `NOLAXIF` prohíbe las comparaciones laxas y
`NOLAXQUAL` obliga a cualificar los nombres de estructura.

Es `implicit none` y `use strict` de esta página, en un compilador de IBM, aplicable por opción de
compilación — y es la forma correcta de imponer un estándar: **que no compile**.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
ESTILO ; Validar identificador -- clase 146
 read palabra
 new i, c, valido
 set valido = $select($length(palabra) > 0 : 1, 1 : 0)
 for i = 1:1:$length(palabra) do
 . set c = $extract(palabra, i)
 . if (c < "a") ! (c > "z") set valido = 0
 write "valido=", $select(valido : "true", 1 : "false"), !
 quit
```

**Lo que esta clase enseña en M.** Aquí está el caso que el gancho de la clase anunciaba: **la convención
más importante de M nació de una limitación física**.

**El estándar de M limitaba los nombres a ocho caracteres** —y en la práctica, muchas implementaciones
solo distinguían los primeros ocho—. Además, **el espacio de rutinas era plano y global**: no hay
espacios de nombres.

Y de ahí salió la convención que define el código VistA y que merece explicarse, porque es una solución
ingeniosa a un problema real:

```text
DPT      -- fichero de pacientes
XU       -- Kernel (utilidades del sistema)
XUS      -- Kernel, seguridad
DI       -- FileMan
LR       -- laboratorio
PS       -- farmacia
RA       -- radiología
```

**Cada paquete tiene un prefijo de dos o tres letras asignado formalmente**, y **todas sus rutinas,
globals y variables empiezan por él**.

```mumps
 do EN^PSOORDER          ; punto de entrada EN de la rutina PSOORDER (farmacia)
 set ^PSDRUG(ien, 0)      ; la global de medicamentos
```

**Eso es un espacio de nombres implementado con una convención de nombres**, administrado por un
registro central, y funcionando en un sistema de decenas de miles de rutinas.

Es la respuesta más pura de esta página a la pregunta de qué es un estándar de codificación: **una
convención que sustituye a una característica que el lenguaje no tiene**.

Y VistA tiene el documento que lo formaliza, y merece nombrarse: **el SAC, *VistA Programming Standards
and Conventions***, que además de los prefijos regula:

| Regla | Motivo |
|---|---|
| **`new` obligatorio para toda variable local** | el ámbito es global por defecto (clase 088) |
| **Nada de `$zx` específico del fabricante** en código portable | funciona en varias implementaciones |
| **Puntos de entrada documentados**, con `;;` | la línea de doble comentario es la interfaz |
| **Nada de `kill` sin argumentos** | borraría todas las variables del proceso |
| **`$$` para funciones extrínsecas** | distingue función de procedimiento |
| **Nada de indirección ni `xecute` sin justificar** | imposible de analizar (clase 123) |

**La primera es la más importante y la más peligrosa de olvidar**: en M, **una variable no declarada es
global al proceso**, así que **una rutina que usa `I` como contador sin hacer `new I` destruye el
contador de quien la llamó**.

Es el mismo fallo que las variables globales de cualquier lenguaje, agravado porque **aquí es el
comportamiento por defecto**.

Y por eso la regla del SAC es tajante y la revisión de código de VistA la comprueba siempre: **`new`
todo lo que uses**. Es la convención que hace posible que miles de rutinas de decenas de paquetes
convivan en un espacio de variables compartido.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| palabra valido |

palabra := stdin nextLine trimBoth.

valido := palabra notEmpty and: [
    palabra allSatisfy: [ :c | c isLowercase ] ].

Transcript show: 'valido=', (valido ifTrue: [ 'true' ] ifFalse: [ 'false' ]); cr.
```

**Lo que esta clase enseña en Smalltalk.** `allSatisfy:` con un bloque es el `every` de Lisp y el
`all_of` de C++ de esta página, y `and:` con un bloque es la conjunción **perezosa**: el segundo
argumento **solo se evalúa si el primero es verdadero** (clase 084).

Y sobre estilo, Smalltalk tiene las convenciones más peculiares de esta página, porque **la sintaxis de
mensajes con palabras clave convierte los nombres en frases**:

```smalltalk
cuenta transferir: 100 desde: origen a: destino.
coleccion detect: [ :x | x > 5 ] ifNone: [ nil ].
```

**El selector completo es `transferir:desde:a:`**, y las convenciones giran alrededor de eso:

| Convención | Ejemplo |
|---|---|
| **El selector debe leerse como una frase** | `at:put:`, no `set:with:` |
| Predicados con `is` o adjetivo | `isEmpty`, `notNil`, `includes:` |
| Devolver `self` en los que modifican | permite encadenar con `;` |
| **Los métodos, cortos** | tres a siete líneas es lo habitual |
| Categorías (protocolos) para agrupar | `accessing`, `printing`, `private` |
| Comentario de clase obligatorio | explica el **propósito**, no la implementación |

**"Los métodos cortos" no es una recomendación blanda en Smalltalk: es cultural y muy estricta.** Un
método de treinta líneas se considera un defecto, y la razón es concreta: **el navegador muestra un
método a la vez**, así que **un método que no cabe en la ventana es un método que no se puede leer de
una vez**.

Es un caso claro de una convención de estilo formada por la herramienta, igual que el ancho de 80
columnas viene del terminal y las ocho letras de M vienen del estándar.

Y las herramientas del ecosistema, que aquí son especiales por la razón de siempre —**el sistema se
analiza a sí mismo**:

| Herramienta | Qué hace |
|---|---|
| **SmallLint / Code Critics** | reglas de estilo y defectos, integradas en el navegador |
| **`allCallsOn:`** | quién llama a un selector (clase 138) |
| **Refactoring Browser** | **renombrar, extraer método, mover, con seguridad** |
| **Metrics / Moose** | métricas y análisis de arquitectura sobre el sistema vivo |

**SmallLint merece la mención final**, porque hace algo que muy pocos analizadores hacen: **avisa
mientras escribes, dentro del navegador de clases, y ofrece la corrección aplicable con un clic**.

Y la razón por la que puede hacerlo es la de la Parte 8: **el código es un objeto, así que el analizador
es un programa que recorre objetos** — no un analizador de texto que reimplementa el lenguaje.

Es la conclusión de esta clase en su forma más limpia: **cuando el entorno entiende el código, la
comprobación mecánica es barata y automática, y la revisión humana queda libre para lo que solo una
persona puede juzgar**.

---

## Y de vuelta a la clase

Lo transferible: **todo lo que una máquina pueda comprobar, debe comprobarlo la máquina** — formato,
nombres, complejidad, patrones peligrosos, cobertura. Lo que queda para la revisión humana es lo único
que una herramienta no puede juzgar: **si el código resuelve el problema correcto, si el diseño
aguantará el próximo cambio, y si alguien que llegue dentro de dos años lo entenderá**. Una revisión que
discute sangrados está desperdiciando lo más caro del proceso, que es la atención de otra persona. Y una
regla que no se puede automatizar y nadie recuerda, **no es un estándar: es una aspiración**.

⏮️ [Volver a la clase 146](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
