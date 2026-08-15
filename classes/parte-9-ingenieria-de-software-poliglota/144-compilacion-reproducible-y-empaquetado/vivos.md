# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 144

> [⬅️ Volver a la clase 144](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Una suma de comprobación: sumar los enteros de una línea. Es el ejemplo mínimo de la idea que sostiene
esta clase — **reducir algo grande a un número que permite decir "esto es exactamente lo mismo"**. Y la
pregunta que la clase persigue es incómoda: **si compilas el mismo código dos veces, ¿sale el mismo
binario?** La respuesta por defecto, en casi todos los lenguajes de esta página, es **no** — y las
razones son sorprendentes.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es la **reproducibilidad de la construcción**, y estos lenguajes lo enseñan porque
> cubren todas las respuestas posibles. **COBOL y PL/I en z/OS producen módulos de carga con marcas de
> tiempo dentro.** **Fortran y Pascal generan ficheros intermedios atados al compilador.** **Tcl y Lisp
> empaquetan el intérprete entero.** **Y Smalltalk lleva la idea al extremo: el artefacto es la imagen.**
>
> Y el motivo por el que esto importa hoy tiene nombre: **la cadena de suministro**. Si dos personas
> compilan el mismo fuente y obtienen binarios distintos, **no hay forma de verificar que el binario
> publicado viene del fuente publicado**.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: una línea con enteros separados por espacio → stdout: `checksum=<suma de los valores>`
- **Regla:** `checksum = suma de los valores`

| stdin | esperado |
|---|---|
| `1 2 3` | `checksum=6` |
| `5` | `checksum=5` |
| `10 20 30` | `checksum=60` |

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
PROGRAM-ID. SUMA.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(200).
01  I       PIC 9(4) COMP.
01  C       PIC X.
01  NUM     PIC S9(9) COMP VALUE 0.
01  TOTAL   PIC S9(9) COMP VALUE 0.
01  ENNUM   PIC 9      VALUE 0.
01  ED      PIC -(8)9.

PROCEDURE DIVISION.
    ACCEPT LINEA

    PERFORM VARYING I FROM 1 BY 1 UNTIL I > 200
        MOVE LINEA(I:1) TO C
        IF C IS NUMERIC
            COMPUTE NUM = NUM * 10 + FUNCTION NUMVAL(C)
            MOVE 1 TO ENNUM
        ELSE
            IF ENNUM = 1
                COMPUTE TOTAL = TOTAL + NUM
                MOVE 0 TO NUM
                MOVE 0 TO ENNUM
            END-IF
        END-IF
    END-PERFORM

    MOVE TOTAL TO ED
    DISPLAY "checksum=" FUNCTION TRIM(ED)
    STOP RUN.
```

**Lo que esta clase enseña en COBOL.** El programa recorre la línea carácter a carácter con
`LINEA(I:1)` —**modificación de referencia**, la forma de COBOL de tomar una subcadena— y usa la
condición de clase `IS NUMERIC`, que es una comprobación integrada en el lenguaje.

Y sobre reproducibilidad, el mundo mainframe tiene una respuesta que merece explicarse porque llegó por
un camino distinto al de la industria libre: **la auditoría**.

En un banco, **hay que poder demostrar qué versión del fuente produjo el módulo que está en
producción**, y eso es un requisito regulatorio, no técnico.

La solución no fue hacer la compilación determinista, sino **registrar la construcción**:

```text
Endevor / ChangeMan guardan, por cada módulo desplegado:
  - el fuente exacto, con su número de versión
  - las opciones de compilación usadas
  - las versiones de todos los copybooks incluidos
  - quién lo compiló, cuándo y con qué autorización
  - y el listado de compilación completo
```

**Eso es una lista de materiales del software** —lo que hoy se llama SBOM— **de los años ochenta**, y
resuelve el mismo problema por otra vía: **si no puedes reproducir el binario, conserva la prueba de
cómo se hizo**.

Y el módulo de carga de z/OS ayuda, porque **lleva metadatos dentro**:

```text
IDENTIFY  MIPGM('COMPILADO 2024-03-15 POR JSMITH V2.4')
```

**El enlazador puede grabar identificadores en el módulo**, y `AMBLIST` los muestra después. Es
información de procedencia embebida en el artefacto.

Y en el lado libre, GnuCOBOL sí permite la construcción determinista con las mismas técnicas que C:

```bash
export SOURCE_DATE_EPOCH=1700000000
cobc -x -free -ffile-prefix-map=$PWD=. prog.cob
sha256sum prog
```

Y merece señalar la fuente de irreproducibilidad más específica de COBOL, porque es la de esta página:
**el copybook**. Dos compilaciones del mismo programa **con distintas versiones de un copybook producen
binarios distintos**, y el fuente del programa no cambió.

Es la razón por la que la lista de materiales de un módulo COBOL tiene que incluir **todos los
copybooks con su versión** — que es exactamente lo que Endevor registra.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program suma
   implicit none
   character(len=200) :: linea
   integer :: total, valor, ios, pos

   read(*, '(A)') linea
   total = 0
   pos = 1

   do
      read(linea(pos:), *, iostat=ios) valor
      if (ios /= 0) exit
      total = total + valor
      pos = pos + index(linea(pos:), ' ')
      if (pos > len_trim(linea)) exit
   end do

   write(*, '(A,I0)') 'checksum=', total
end program suma
```

**Lo que esta clase enseña en Fortran.** El programa usa **lectura interna** —`read` desde una cadena— y
avanza con `index`, que es la forma clásica de tokenizar en Fortran sin bibliotecas.

Y sobre reproducibilidad, Fortran tiene el caso más difícil de esta página, y por dos motivos distintos
que conviene separar.

**El primero es el de todos: el binario.** Fuentes de irreproducibilidad conocidas:

```bash
gfortran -ffile-prefix-map=$PWD=.      # rutas absolutas dentro del binario
export SOURCE_DATE_EPOCH=1700000000     # marcas de tiempo
gfortran -frandom-seed=0                 # ¡el generador de símbolos internos!
```

**`-frandom-seed` es específico de Fortran y sorprende**: gfortran genera nombres internos con un
componente aleatorio, así que **dos compilaciones producen símbolos distintos** salvo que se fije la
semilla.

**Y el segundo es propio del dominio y más profundo: la reproducibilidad del RESULTADO.**

Como la clase 140 explicó, **el mismo programa da números distintos según el compilador, las
optimizaciones, el número de hilos y hasta el modelo de procesador**.

```bash
gfortran -O2 -march=native      # ¡usa las instrucciones de ESTA máquina!
```

**`-march=native` es la trampa clásica**: produce un binario que **no funciona en otra máquina** y que
**da otros números en la que sí funciona**. Es cómodo para un cálculo propio y desastroso para
distribuir.

Y de ahí las herramientas del ecosistema:

| Herramienta | Qué aporta |
|---|---|
| **Spack** | compila con un identificador que incluye compilador, versión, opciones y arquitectura |
| **EasyBuild** | recetas reproducibles para clústeres |
| **`environment modules`** | fijar la versión de compilador y bibliotecas por sesión |
| **contenedores** | Singularity/Apptainer: la imagen entera, para HPC |

**Spack merece la explicación** porque su modelo es el correcto para el problema de esta página: **el
identificador de un paquete instalado es un valor calculado sobre toda su configuración**.

```text
zlib@1.3.1%gcc@13.2.0+optimize+pic+shared arch=linux-ubuntu22.04-zen3
     ^^^^^^^^^^^^ hash: 5rk3nlv...
```

**Dos configuraciones distintas son dos instalaciones distintas, coexistiendo.** Es la respuesta al
problema del `.mod` de la clase 143, y es lo mismo que hace Nix.

Y la conclusión de esta clase para el cálculo científico es una que la comunidad tardó en aceptar: **un
artículo que publica resultados numéricos sin publicar el contenedor o el `spack.lock` no es
reproducible**, aunque publique el código.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Suma is
   Total, Valor : Integer := 0;
begin
   Total := 0;
   loop
      begin
         Get (Valor);
         Total := Total + Valor;
      exception
         when others => exit;
      end;
   end loop;

   Put ("checksum=");
   Put (Total, Width => 1);
   New_Line;
end Suma;
```

**Lo que esta clase enseña en Ada.** El programa lee enteros hasta que falla, capturando la excepción de
fin de fichero — que es el idioma de Ada para "leer hasta que se acabe" (clase 116).

Y sobre reproducibilidad, Ada parte de una ventaja estructural sobre C++ y Fortran, y es la de la clase
143: **el compilador conoce el grafo completo de dependencias**, así que **la construcción es determinista
en su orden**.

Y `gprbuild` lo formaliza:

```ada
project Mi_Proyecto is
   for Source_Dirs use ("src");
   for Object_Dir use "obj";
   package Compiler is
      for Default_Switches ("Ada") use ("-O2", "-gnatwa", "-gnat2022");
   end Compiler;
end Mi_Proyecto;
```

**El fichero de proyecto declara las opciones exactas**, así que **no dependen de quién teclea el
comando** — que es una de las tres fuentes de irreproducibilidad del cierre de esta clase.

Y hay una capacidad de Ada que es directamente el tema de esta página y que ningún otro lenguaje de la
lista tiene igual: **la certificación de la cadena de herramientas**.

En aviación y ferrocarril, **el compilador mismo tiene que estar cualificado**:

```text
DO-330 / DO-178C: Tool Qualification
  - se demuestra que el compilador traduce correctamente
  - se congela su versión EXACTA para todo el proyecto
  - y cualquier cambio obliga a repetir la cualificación
```

**Congelar la versión del compilador durante los diez o veinte años de vida del programa** es la norma
en estos sectores, y es la aplicación más estricta de la regla del cierre de esta clase: **la
reproducibilidad es una propiedad del entorno**.

Y de ahí una práctica que merece conocerse: **se archiva la máquina de construcción entera**, a veces
como imagen de disco, a veces como hardware físico guardado.

Y AdaCore da las herramientas para verificar el resultado:

```bash
gnatcheck        # reglas de codificación
gnatmetric        # métricas del fuente
gnatstub / gnattest
gnatcoverage       # cobertura sin instrumentar, sobre el binario FINAL
```

**`gnatcoverage` sin instrumentar es lo relevante para esta clase**: mide la cobertura **del binario que
se va a desplegar**, no de una versión modificada.

Es una diferencia que importa cuando hay que certificar, porque **lo que se prueba y lo que se despliega
tienen que ser el mismo objeto** — y en la mayoría de los ecosistemas no lo son.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Suma;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  Linea, Tok: string;
  I, Total: Integer;

begin
  ReadLn(Linea);
  Linea := Trim(Linea) + ' ';
  Total := 0;
  Tok := '';

  for I := 1 to Length(Linea) do
    if Linea[I] = ' ' then
    begin
      if Tok <> '' then Total := Total + StrToInt(Tok);
      Tok := '';
    end
    else
      Tok := Tok + Linea[I];

  WriteLn('checksum=', IntToStr(Total));
end.
```

**Lo que esta clase enseña en Pascal.** El programa acumula el número en `Tok` y lo convierte al llegar
al separador — el tokenizador manual de toda la vida, sin depender de bibliotecas.

Y sobre empaquetado, Pascal tiene una virtud que define su ecosistema y que merece destacarse: **el
ejecutable de Pascal es autocontenido y pequeño**.

```bash
fpc -O2 -XX -Xs prog.pas       # -XX: enlace inteligente; -Xs: quitar símbolos
ls -l prog                      # unos pocos cientos de KB, sin dependencias
```

**`-XX` es el enlace inteligente**: el compilador coloca cada función en una sección propia y **el
enlazador descarta las que no se usan**. El resultado es un binario que incluye **solo lo que hace
falta** de la biblioteca estándar.

Eso, más el hecho de que la biblioteca de tiempo de ejecución de Pascal sea pequeña, da lo que Turbo
Pascal hizo famoso: **un `.exe` de 30 KB que funciona en cualquier máquina, sin instalar nada**.

Es exactamente lo que hoy se busca con los binarios estáticos de Go y Rust, y era la norma en 1987.

Y sobre reproducibilidad:

```bash
fpc -B prog.pas            # -B: reconstruir TODO, sin usar .ppu previos
```

**`-B` es importante para esta clase**: sin él, el compilador reutiliza los `.ppu` existentes, y **una
construcción incremental puede mezclar objetos de estados distintos del código**.

Es el mismo problema del `make` sin dependencias correctas, y es la razón por la que las construcciones
de publicación se hacen siempre **desde cero, en un directorio limpio**.

Y hay una fuente de irreproducibilidad específica de Pascal que conviene conocer:

```pascal
{$I %DATE%}     { la fecha de compilación, INSERTADA en el binario }
{$I %TIME%}
{$I %FPCVERSION%}
```

**Esas directivas insertan la fecha y la hora en el ejecutable**, y son de uso muy extendido para
mostrar la versión en el "Acerca de". Y hacen imposible la reproducibilidad bit a bit.

La solución es la de toda esta clase: **sustituirlas por un valor derivado del control de versiones** —el
identificador del *commit*, que es determinista— en lugar del reloj.

Es un ejemplo pequeño y muy representativo del tipo de decisión que hay que revisar: **cualquier cosa
que lea el reloj durante la construcción rompe la reproducibilidad**.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let ((total 0))
  (with-input-from-string (s (read-line))
    (loop for valor = (read s nil nil)
          while valor
          do (incf total valor)))
  (format t "checksum=~D~%" total))
```

**Lo que esta clase enseña en Common Lisp.** El programa usa `with-input-from-string` para leer números
de una cadena con el propio lector del lenguaje — que es lo natural en Lisp: **el analizador ya existe**
(clase 123).

Y sobre empaquetado, Lisp tiene la respuesta más peculiar de esta página, y es directamente la del
modelo de la Parte 8:

```lisp
(sb-ext:save-lisp-and-die "miapp"
                          :executable t
                          :toplevel #'main
                          :compression t)
```

**`save-lisp-and-die` vuelca el estado completo del sistema a un fichero ejecutable.** Dentro va **el
compilador, el depurador, el recolector, todas las bibliotecas cargadas y todos los objetos que
existían en ese momento**.

Y eso tiene consecuencias que definen el compromiso de esta clase:

**A favor:**

- **Arranque instantáneo**: no hay que cargar ni compilar nada; el estado ya está construido.
- **Cero dependencias en el destino**: es un fichero.
- **Y se pueden precalcular tablas, cachés e índices** antes de guardar, y **estarán ahí al arrancar**.

**En contra:**

- **Decenas de megabytes**, aunque la compresión ayuda.
- **Y es opaco**: lo que hay dentro es lo que había en la imagen, incluida cualquier cosa que se cargara
  por accidente.

Ese último punto es la advertencia práctica de esta explicación: **una imagen guardada desde una sesión
interactiva puede contener variables sueltas, credenciales tecleadas en el REPL o estado de pruebas**.

De ahí la regla del ecosistema: **la imagen de publicación se construye desde un proceso limpio y con un
guion**, nunca desde la sesión donde se estuvo trabajando.

```bash
sbcl --non-interactive --load construir.lisp
```

Y sobre reproducibilidad, Lisp tiene una ventaja y una desventaja concretas:

**A favor**, Quicklisp con `dist-version` fija (clase 143) da un conjunto de dependencias determinista, y
existe `qlot` para bloquear versiones por proyecto.

**En contra**, **las tablas de dispersión y los conjuntos no tienen orden garantizado**, así que
cualquier código que genere salida recorriendo una tabla **puede producir órdenes distintos entre
ejecuciones**.

Es la tercera fuente de irreproducibilidad del cierre de esta clase —**el orden**— y aparece en todos los
lenguajes con tablas de dispersión. La solución es siempre la misma: **ordenar explícitamente antes de
emitir**.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea

set total 0
foreach v [split [string trim $linea]] {
    if {$v ne ""} { incr total $v }
}

puts "checksum=$total"
```

**Lo que esta clase enseña en Tcl.** Tcl inventó, en 2002, la solución al empaquetado que hoy se
considera moderna: **el Starkit**.

```bash
sdx wrap miapp.kit              # empaqueta la aplicación
sdx wrap miapp.exe -runtime tclkit-win32.exe    # ...con el intérprete dentro
```

Y lo que hay dentro merece explicarse, porque la idea es elegante:

**Un Starkit es un fichero que contiene un sistema de ficheros virtual completo** —**Metakit** o
**VFS**— con el código, los paquetes, las imágenes, la documentación y los datos.

Y el intérprete **lo monta como un directorio** al arrancar:

```tcl
source [file join $starkit::topdir lib app-miapp miapp.tcl]
```

**El programa cree que está leyendo ficheros normales**, y en realidad están dentro del ejecutable.

Un **Starpack** añade el intérprete al principio del fichero, y el resultado es **un único ejecutable
sin dependencias**, para Windows, Linux o macOS.

Eso es, exactamente, lo que hoy hacen AppImage, los ejecutables de PyInstaller, los binarios únicos de
Node y Deno, y en buena medida los contenedores. **En Tcl es de hace más de veinte años.**

Y hay una propiedad del Starkit que sigue siendo poco común y que merece señalarse: **el sistema de
ficheros virtual es de lectura y escritura**.

**Una aplicación puede escribir dentro de su propio Starkit** —configuración, complementos, datos—, y el
fichero se actualiza solo. Es una aplicación que se autocontiene por completo, incluidos sus datos.

Y sobre reproducibilidad, Tcl está en el lado fácil de esta página por la razón de la clase 143:
**distribuye fuente, no binarios**. El único binario es el intérprete, que se descarga precompilado y
verificable.

La irreproducibilidad que sí aparece es la del orden:

```tcl
foreach k [array names datos] { ... }         ;# ORDEN ARBITRARIO
foreach k [lsort [array names datos]] { ... }  ;# determinista
```

**`array names` no garantiza orden**, porque es una tabla de dispersión. Es la misma advertencia que en
Lisp en esta página, y la misma solución: **ordenar antes de emitir**.

Y el detalle que lo hace crítico aquí: **un Starkit construido recorriendo un directorio sin ordenar
produce ficheros distintos en cada construcción**, aunque el contenido sea idéntico.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;
use List::Util qw(sum0);

my $linea = <STDIN>;
chomp $linea;

print "checksum=", sum0(split ' ', $linea), "\n";
```

**Lo que esta clase enseña en Perl.** `sum0` de `List::Util` suma una lista devolviendo 0 si está vacía
—el `sum` a secas devuelve `undef`—, y es un detalle representativo de una biblioteca estándar pensada
por gente que se había quemado.

Y sobre empaquetado, Perl tiene tres soluciones que cubren tres escenarios distintos y que merecen
conocerse:

**Primera, `App::FatPacker`**, para guiones:

```bash
fatpack pack script.pl > script-empaquetado.pl
```

**Mete todos los módulos puros de Perl dentro del propio guion**, en una sección de datos, y el guion
los carga desde ahí. El resultado es **un solo fichero `.pl` que funciona en cualquier Perl**, sin
instalar nada.

**Segunda, `PAR::Packer`**, para aplicaciones:

```bash
pp -o miapp.exe script.pl
```

**Empaqueta el intérprete, los módulos —incluidos los compilados en C— y los datos en un ejecutable**.
Es el equivalente exacto del Starpack de Tcl en esta página.

**Y tercera, `Carton` con `cpanfile.snapshot`** (clase 143), para servidores: **se despliega el árbol de
dependencias exacto**, verificado por suma de comprobación.

Y Perl aporta a esta clase una advertencia sobre reproducibilidad que es más importante de lo que
parece, y es la tercera fuente del cierre: **el orden de las claves de una tabla de dispersión es
deliberadamente aleatorio**.

```perl
for my $k (keys %datos) { ... }            # ORDEN DISTINTO EN CADA EJECUCIÓN
for my $k (sort keys %datos) { ... }        # determinista
```

**Desde Perl 5.18 (2013), el orden cambia entre ejecuciones del mismo programa**, y no por descuido: es
una medida de seguridad contra **los ataques de colisión de dispersión**, en los que un atacante envía
claves elegidas para degradar la tabla a una lista y consumir la CPU del servidor.

Perl añadió una semilla aleatoria por proceso, y **eso rompió muchísimo código que dependía sin saberlo
del orden**.

Es una lección doble y muy transferible:

**Una, sobre reproducibilidad**: **nunca dependas de un orden que no está garantizado**, porque el día
que cambie no habrá aviso.

**Y otra, sobre seguridad** (clase 153): **una estructura de datos puede ser un vector de ataque**, y la
defensa —aleatorizar— puede romper suposiciones que nadie escribió.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>

int main() {
    long long total = 0, valor = 0;
    while (std::cin >> valor) total += valor;

    std::cout << "checksum=" << total << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** C++ es el lenguaje donde el movimiento de las construcciones
reproducibles nació y donde más trabajo ha costado, y merece contar por qué.

**El problema, en concreto**: compilar dos veces el mismo fuente producía binarios distintos por
razones tontas pero reales.

| Causa | Solución |
|---|---|
| `__DATE__` y `__TIME__` en el binario | `SOURCE_DATE_EPOCH` |
| **Rutas absolutas** en la información de depuración | `-ffile-prefix-map=$PWD=.` |
| **Orden de los ficheros** al enlazar | ordenar la lista explícitamente |
| **Orden de lectura del directorio** | ordenar; no confiar en `readdir` |
| Marcas de tiempo en los `.a` | `ar D` (determinista), por defecto hoy |
| **Rutas en `__FILE__`** (assert, logs) | `-fmacro-prefix-map` |
| Símbolos de plantillas en orden variable | fijar el orden de las unidades |
| **Paralelismo del enlazador** | `--sort-section=name`, LTO determinista |

**El proyecto *Reproducible Builds*** (2013, nacido en Debian) recorrió esa lista para **decenas de miles
de paquetes**, y hoy **más del 90 % de Debian se compila de forma reproducible**.

Y la razón por la que ese esfuerzo importa merece explicarse, porque es el argumento central de esta
clase:

**Ken Thompson lo planteó en 1984, en "Reflections on Trusting Trust"**: se puede modificar un
compilador para que **inserte una puerta trasera al compilar un programa concreto**, y para que
**inserte esa misma modificación al compilarse a sí mismo** — de modo que **la puerta trasera no aparece
en ningún código fuente**.

**Las construcciones reproducibles son la defensa práctica contra eso**: si varias personas
independientes compilan el mismo fuente con sus propias herramientas y obtienen **exactamente el mismo
binario**, hay evidencia fuerte de que ese binario viene de ese fuente.

Y el ataque no es teórico: **SolarWinds (2020)** fue exactamente eso —**comprometer la máquina de
construcción, no el repositorio**— y afectó a decenas de miles de organizaciones.

Las herramientas del ecosistema hoy:

```bash
diffoscope binario1 binario2     # QUÉ difiere entre dos binarios, recursivamente
strip-nondeterminism              # limpiar marcas de tiempo de los artefactos
cosign / in-toto / SLSA            # firmar y atestiguar la procedencia
```

**`diffoscope` merece la mención final** porque es una herramienta sorprendentemente buena: **desempaqueta
recursivamente** —archivos dentro de paquetes dentro de imágenes— y **desensambla, descomprime y compara
metadatos** hasta encontrar el byte que cambió y explicar por qué.

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

dcl-pi SUMA;
  linea char(200) const;
end-pi;

dcl-s texto varchar(200);
dcl-s pos   int(10);
dcl-s total int(20);

texto = %trim(linea) + ' ';
total = 0;

dow %len(%trim(texto)) > 0;
  pos = %scan(' ' : texto);
  if pos = 0;
    leave;
  endif;
  if pos > 1;
    total += %int(%subst(texto : 1 : pos - 1));
  endif;
  texto = %trim(%subst(texto : pos + 1));
enddo;

dsply ('checksum=' + %char(total));

*inlr = *on;
return;
```

**Lo que esta clase enseña en RPG.** IBM i tiene, para el empaquetado, un formato propio que resuelve el
problema de esta clase de una forma que merece conocerse: **el fichero de salvado**.

```text
CRTSAVF FILE(QGPL/ENTREGA)
SAVOBJ OBJ(*ALL) LIB(MIAPP) DEV(*SAVF) SAVF(QGPL/ENTREGA)
```

**Un fichero de salvado contiene objetos completos** —programas, tablas, áreas de datos, colas— **con
todos sus metadatos**: propietario, autoridades, descripción, fecha de creación, **la vista de
depuración** (clase 141) y **la información de qué fuente lo creó**.

Y esa última parte es directamente el tema de esta clase:

```text
DSPOBJD OBJ(MIAPP/MIPGM) OBJTYPE(*PGM) DETAIL(*SERVICE)
   Fuente ......... : MIAPP/QRPGLESRC(MIPGM)
   Fecha del fuente : 2024-03-15 09:22:41
   Compilador ...... : IBM RPG 7.4
   Nivel de destino  : V7R3M0
```

**El objeto sabe de qué fuente salió, cuándo y con qué compilador.** Es procedencia embebida, sin
herramienta externa — lo que Endevor tiene que registrar aparte en COBOL, aquí está en el objeto.

Y el ecosistema moderno cerró el resto del círculo:

| Herramienta | Qué aporta |
|---|---|
| **ibmi-bob** | construcción desde fuentes **en el IFS**, con `Makefile` y dependencias |
| **Git en el IFS** | los fuentes en ficheros de flujo, no en ficheros físicos (clase 145) |
| **Code4i / RDi** | compilar y desplegar desde VS Code o Eclipse |
| **`SAVRSTOBJ`** | salvar y restaurar entre sistemas en una operación |

**ibmi-bob es el cambio importante de la última década**: llevó la construcción de IBM i al modelo
normal —**fuentes en git, construcción declarada, dependencias resueltas, salida verificable**— cuando
antes cada tienda tenía su propio programa CL de compilación.

Y hay un detalle sobre reproducibilidad específico de esta plataforma que merece señalarse: **el nivel
de destino**.

```text
CRTBNDRPG ... TGTRLS(V7R3M0)
```

**`TGTRLS` fija para qué versión del sistema operativo se genera el objeto**, y con eso **el objeto
funciona en cualquier sistema de esa versión o posterior**.

Es compatibilidad hacia adelante declarada explícitamente, y es coherente con la firma de programa de
servicio de la clase 143: **en esta plataforma, la compatibilidad se declara y el sistema la comprueba**,
en lugar de suponerse.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 suma: procedure options(main);

    declare valor fixed binary(31);
    declare total fixed binary(31) initial(0);

    on endfile(sysin) goto fin;

    do while ('1'b);
       get list (valor);
       total = total + valor;
    end;

 fin:
    put skip list ('checksum=' || trim(char(total)));

 end suma;
```

**Lo que esta clase enseña en PL/I.** El programa usa `on endfile` con un salto —el idioma clásico de
PL/I para leer hasta el final (clase 103)— y `do while ('1'b)`, que es el bucle infinito con una
constante de bit.

Y sobre empaquetado, z/OS tiene un modelo que merece conocerse porque su unidad es distinta de todo lo
demás de esta página: **el módulo de carga en una biblioteca particionada**.

```text
PDS/PDSE: un fichero que contiene MIEMBROS con nombre
   MI.PROD.LOADLIB(MIPGM)     <-- el módulo ejecutable
   MI.PROD.SOURCE(MIPGM)       <-- el fuente
   MI.PROD.COPYLIB(CLIENTE)     <-- el copybook
```

**Una biblioteca particionada es a la vez un directorio y un fichero**, y se copia, se salva y se
transporta como una unidad.

Y de ahí la forma clásica de desplegar en el mainframe, que es asombrosamente simple:

```jcl
//COPIA  EXEC PGM=IEBCOPY
//SYSUT1  DD DSN=MI.QA.LOADLIB,DISP=SHR
//SYSUT2  DD DSN=MI.PROD.LOADLIB,DISP=SHR
//SYSIN   DD *
  COPY OUTDD=SYSUT2,INDD=SYSUT1
  SELECT MEMBER=(MIPGM)
```

**Copiar un miembro de una biblioteca a otra ES el despliegue** (clase 148), y la vuelta atrás es
copiar el anterior de vuelta — que se conserva porque **las bibliotecas se versionan por generaciones**:

```text
MI.PROD.LOADLIB.G0042V00     <-- grupo de datos generacional
MI.PROD.LOADLIB.G0041V00      <-- la anterior, automáticamente conservada
```

**Los *generation data groups*** mantienen las últimas N versiones automáticamente, y se referencian con
`(0)` para la actual, `(-1)` para la anterior.

Es control de versiones de artefactos integrado en el sistema de ficheros, y es de los años sesenta.

Y sobre reproducibilidad, PL/I comparte la solución de COBOL de esta página —**registrar la construcción
en lugar de reproducirla**— con una particularidad propia que conviene nombrar: **el listado de
compilación con `AGGREGATE` y `ATTRIBUTES`** documenta **la disposición exacta en memoria de cada
estructura**.

Y eso importa aquí porque **en PL/I la disposición depende de opciones de compilación** —`ALIGNED`,
`UNALIGNED`, el modelo de direccionamiento—, así que **el mismo fuente puede producir estructuras con
distinto tamaño**.

Es la misma clase de dependencia oculta que el ABI de C++ en esta página: **el binario depende de cosas
que no están en el fuente**, y por eso la lista de materiales tiene que incluir las opciones.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
SUMA ; Suma de comprobacion -- clase 144
 read linea
 new i, total, n
 set total = 0
 for i = 1:1:$length(linea, " ") do
 . set n = $piece(linea, " ", i)
 . if n '= "" set total = total + n
 write "checksum=", total, !
 quit
```

**Lo que esta clase enseña en M.** `$length(linea, " ")` devuelve **cuántos trozos hay** al partir por
espacios, y `$piece` extrae cada uno: es el par de funciones que hace el reparto de texto en M sin
crear listas (clase 093).

Y sobre empaquetado, M tiene el modelo más ajeno de esta página y ya apareció en la clase 143: **el
artefacto es una global**.

Un paquete KIDS **es una estructura de datos en la base**, no un fichero, y contiene el código como
texto junto con las definiciones de datos y los guiones de instalación.

Y eso tiene una consecuencia que merece destacarse para esta clase: **la instalación es una transacción
de base de datos**.

```mumps
 tstart
 ; cargar rutinas, migrar datos, actualizar definiciones
 tcommit
```

**Si algo falla a mitad, se deshace todo** — incluidas las rutinas ya sustituidas, porque las rutinas
son datos.

En un despliegue de ficheros, "deshacer a mitad" significa restaurar una copia de seguridad y esperar. En
M es un `trollback`.

Y sobre reproducibilidad y verificación, la comunidad M construyó una técnica que merece conocerse
porque resuelve el problema de esta clase con los medios del lenguaje: **la suma de comprobación de
rutina**.

```mumps
 ; ^%RCMP y CHKSUM^XTSUMBLD en VistA
 do CHKSUM^XTSUMBLD("MIRUT")
 ; devuelve un valor calculado sobre el CÓDIGO de la rutina
```

**Cada rutina de VistA tiene una suma de comprobación publicada**, y el sistema puede recorrer todas las
rutinas instaladas y **comprobar que ninguna ha sido modificada localmente**.

Eso responde a una pregunta muy concreta y muy real en estos sistemas: **"¿este hospital ha parcheado
algo a mano?"** — y la respuesta importa, porque un parche local puede romper una actualización o puede
ser la razón por la que un fallo no se reproduce en otro sitio.

Es exactamente la función de un `sha256sum` sobre los binarios instalados, adaptada a un sistema donde el
código vive en la base de datos.

Y la lección transferible es la del cierre de esta clase: **un artefacto verificable requiere una
identidad calculada sobre su contenido**, y da igual si ese contenido es un binario, un fichero de texto
o una entrada de base de datos.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| linea total |

linea := stdin nextLine trimBoth.
total := 0.

(linea substrings: ' ') do: [ :p | total := total + p asNumber ].

Transcript show: 'checksum=', total printString; cr.
```

**Lo que esta clase enseña en Smalltalk.** Aquí está el extremo de esta clase, y es coherente con toda
la Parte 8: **el artefacto de despliegue es la imagen**.

```smalltalk
Smalltalk snapshot: true andQuit: true.
```

Y eso significa que **lo que se despliega es el estado completo del sistema**: todas las clases, todos
los métodos compilados, todos los objetos vivos, las conexiones abiertas, las cachés calentadas y las
ventanas que estuvieran abiertas.

**A favor**, es la reproducibilidad más fuerte que hay: **no hay nada que instalar, resolver, compilar
ni configurar**. La aplicación arranca exactamente en el estado en que se guardó, en milisegundos.

**En contra**, es opaca. **¿Qué hay dentro de una imagen de 80 MB?** Todo lo que alguien cargó alguna
vez, incluidos experimentos, versiones antiguas de métodos y objetos huérfanos.

Y de ahí las dos prácticas que la comunidad desarrolló y que merecen conocerse porque son la respuesta a
esta clase:

**Primera, la construcción de imagen desde cero, con guion:**

```bash
# Pharo: descargar una imagen limpia y cargar el proyecto encima
curl get.pharo.org/64/110 | bash
./pharo Pharo.image eval "Metacello new baseline: 'MiApp';
    repository: 'github://org/miapp:v1.2.3/src'; load."
./pharo Pharo.image save miapp
```

**La imagen se construye desde una imagen base conocida más una lista de paquetes con versión** — que es
exactamente el modelo de un contenedor con su fichero de construcción.

**Y segunda, la reducción de imagen**:

```smalltalk
Smalltalk garbageCollect.
Smalltalk cleanUp: true.
SystemNavigation default obsoleteBehaviors.     "clases zombis"
```

**Limpiar el sistema antes de guardar** quita las clases obsoletas, las referencias de las herramientas
de desarrollo y los objetos inalcanzables.

Y hay una versión extrema de esto que merece nombrarse: **el reductor de imagen** de algunos Smalltalk
comerciales **elimina las clases y métodos que la aplicación no usa**, analizando el grafo de envíos —lo
que produce imágenes de pocos megabytes.

Es el mismo enlace inteligente que Pascal tiene con `-XX` en esta página, aplicado a un sistema de
objetos vivos, y con la misma dificultad que en cualquier lenguaje dinámico: **`perform:` con un
selector construido en marcha hace imposible saber qué se usa** (clase 111).

Y ahí está la observación que cierra esta clase para Smalltalk: **la flexibilidad que hace tan buena la
depuración es la misma que impide reducir el sistema con garantías** — el compromiso que la Parte 8
mostró clase tras clase, apareciendo una vez más en el empaquetado.

---

## Y de vuelta a la clase

Lo transferible: **una construcción reproducible convierte un binario en algo verificable**. Cualquiera
puede recompilar y comprobar que le sale lo mismo, y eso cierra la puerta al ataque más difícil de
detectar de todos: **modificar el compilador o la máquina de construcción en lugar del código**. Las
tres fuentes de irreproducibilidad son siempre las mismas —**tiempo, rutas y orden**— y las tres tienen
solución conocida. La disciplina que hay que llevarse: **fijar la versión de todo lo que participa en la
construcción**, porque la reproducibilidad no es una propiedad del código, es una propiedad del
entorno.

⏮️ [Volver a la clase 144](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
