# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 162

> [⬅️ Volver a la clase 162](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Elevar al cuadrado. El programa da igual: lo que esta clase pregunta es **dónde se ejecuta**. Y la
respuesta nueva es **un formato binario portátil que corre en el navegador, en el servidor y en el borde
de la red, con aislamiento por diseño**. Y aquí hay una sorpresa que merece el titular: **de los doce
lenguajes de esta página, al menos siete tienen hoy alguna forma de ejecutarse en WebAssembly** — y
entre ellos están Perl, Pascal y Smalltalk.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es el **objetivo de compilación común**, y estos lenguajes lo enseñan porque **ya
> vivieron esta historia**: la máquina virtual de Smalltalk (1980), el bytecode de Tcl y de Perl, la
> máquina virtual de Java (1995), la de .NET (2002). **WebAssembly es el enésimo intento de un formato
> intermedio universal**, y el primero que ha conseguido que casi todos lo apunten.
>
> Y aparece la pregunta que decide cuánto sirve para cada uno: **¿el lenguaje necesita un recolector de
> basura, hilos o llamadas al sistema?** Porque WebAssembly, por diseño, **no tenía nada de eso**.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: un entero `n` → stdout: `resultado=<n²>`
- **Regla:** `calcular n al cuadrado (como en un módulo Wasm)`

| stdin | esperado |
|---|---|
| `5` | `resultado=25` |
| `0` | `resultado=0` |
| `7` | `resultado=49` |

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
PROGRAM-ID. CUADRADO.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(40).
01  N       PIC S9(9) COMP.
01  R       PIC S9(18) COMP.
01  ED      PIC -(17)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    COMPUTE N = FUNCTION NUMVAL(LINEA)
    COMPUTE R = N * N

    MOVE R TO ED
    DISPLAY "resultado=" FUNCTION TRIM(ED)
    STOP RUN.
```

**Lo que esta clase enseña en COBOL.** COBOL en el navegador suena a broma y no lo es, y merece contarlo
porque el camino es instructivo.

**GnuCOBOL traduce COBOL a C** (clase 123), y **C compila a WebAssembly con Emscripten**. Así que:

```bash
cobc -x -free -C prog.cob             # → prog.c
emcc prog.c libcob.a -o prog.html      # → WebAssembly
```

**Y funciona**: hay demostraciones públicas de GnuCOBOL ejecutándose en el navegador, y proyectos que lo
usan para enseñar COBOL sin instalar nada.

Y merece preguntarse para qué sirve de verdad, porque la respuesta es más interesante que la anécdota:

**Primero, para formación y para pruebas.** Un entorno donde escribir y ejecutar COBOL sin acceso a un
mainframe **resuelve un problema real de una industria con un problema de relevo generacional** (clase
154).

**Segundo, para llevar la lógica de negocio al cliente.** Hay reglas —el cálculo de un interés, la
validación de un IBAN, una tarifa— **que están implementadas en COBOL y validadas durante décadas**, y
que hoy se reimplementan en JavaScript para el navegador, **con el riesgo de que las dos versiones
diverjan** (clase 140).

**Compilar la original a WebAssembly elimina esa duplicación.**

Y ahí está el argumento más serio de esta clase para los lenguajes de esta columna: **WebAssembly permite
reutilizar código validado en sitios donde ese lenguaje no llegaba**.

Y las limitaciones hay que decirlas, y son las del cierre:

| Necesita | ¿Está en WebAssembly? |
|---|---|
| Ficheros indexados VSAM | **no**: hay que emular o llevar los datos a memoria |
| CICS, DB2 | **no**: son el entorno, no el lenguaje |
| Decimal empaquetado | **sí**: es aritmética; GnuCOBOL lo implementa en software |
| Ficheros secuenciales | **sí, con WASI** o con el sistema de ficheros virtual de Emscripten |

**La tercera fila merece destacarse** y conecta con la clase 045: **el decimal exacto de COBOL no
depende del hardware**, así que **se conserva perfectamente** — que es justo lo que hace que valga la
pena portar cálculos financieros y no reescribirlos con `double`.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program cuadrado
   implicit none
   integer(kind=8) :: n

   read(*, *) n

   write(*, '(A,I0)') 'resultado=', n * n
end program cuadrado
```

**Lo que esta clase enseña en Fortran.** Fortran llega a WebAssembly por el camino que la clase 123
describía: **LLVM**.

```bash
flang-new --target=wasm32-wasi -o prog.wasm prog.f90     # con LLVM Flang
# o el camino histórico:
f2c prog.f && emcc prog.c -lf2c -o prog.js
```

**Flang, el compilador Fortran de LLVM, genera la misma representación intermedia que Clang**, y de ahí
sale WebAssembly.

Y merece explicar por qué esto importa en este dominio, porque el caso de uso es concreto y bueno: **los
modelos de simulación en el navegador**.

```text
Un modelo de dinámica de fluidos, de clima o de estructuras
está escrito en Fortran y validado durante veinte años.

Antes: para enseñarlo o demostrarlo había que instalarlo, o montar un servidor.
Ahora: compila a WebAssembly y se ejecuta en la página, en el cliente.
```

Y hay proyectos reales haciéndolo: **modelos climáticos simplificados, simuladores educativos y
herramientas de ingeniería** que ejecutan el código original en el navegador.

Y las limitaciones de esta columna son las que el cierre de esta clase anuncia, y en Fortran son
específicas:

| Necesidad | Estado en WebAssembly |
|---|---|
| **Aritmética de coma flotante** | **sí, y con IEEE 754 estricto** |
| **Arreglos grandes** | sí, con memoria de 64 bits en propuestas recientes |
| **OpenMP (hilos)** | **parcial**: requiere hilos de WebAssembly y aislamiento cruzado |
| **MPI** | **no**: no hay procesos ni red directa |
| **SIMD y vectorización** | **sí**: WebAssembly tiene SIMD de 128 bits |
| **Entrada y salida de ficheros** | con WASI o con el sistema virtual de Emscripten |

**La cuarta fila es la que limita el uso real**: el cálculo de producción es paralelo y distribuido, y
**eso no cabe en el modelo**.

Así que el papel de WebAssembly en este dominio no es sustituir al clúster: **es llevar el mismo código a
la demostración, a la docencia y al preprocesado en el cliente**.

Y merece señalar una ventaja de esta clase que se pasa por alto y que a Fortran le viene bien: **la
reproducibilidad**.

**WebAssembly especifica la aritmética de coma flotante de forma estricta y determinista** —sin FMA
implícito, sin registros de 80 bits, sin reasociación—, así que **el mismo módulo da exactamente los
mismos bits en cualquier máquina**.

Es lo que la clase 140 buscaba con `-ffp-contract=off` y `MKL_CBWR`, **garantizado por el formato**.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;
with Ada.Strings;
with Ada.Strings.Fixed;

procedure Cuadrado is
   N : Integer;
   R : Long_Long_Integer;
begin
   Get (N);
   R := Long_Long_Integer (N) * Long_Long_Integer (N);

   Put_Line ("resultado=" &
             Ada.Strings.Fixed.Trim (R'Image, Ada.Strings.Both));
end Cuadrado;
```

**Lo que esta clase enseña en Ada.** Ada llega a WebAssembly por dos caminos, y merece distinguirlos
porque representan dos filosofías:

**GNAT-LLVM**, que compila Ada a la representación intermedia de LLVM y de ahí a `wasm32-wasi`.

**Y GNAT con la biblioteca de ejecución reducida** —`Light` o `Light-Tasking`, antes llamada ZFP, *zero
footprint*—, que es la que hace esto viable.

Y ahí está el contenido de esta clase para Ada, y merece explicarlo porque es exactamente la pregunta del
"por qué":

```text
La biblioteca de ejecución de Ada incluye:
  - el planificador de tareas
  - el manejo de excepciones con propagación
  - las comprobaciones de restricción
  - la finalización controlada
  - y la entrada y salida

WebAssembly (sin extensiones) no tiene hilos, ni pila secundaria, ni sistema operativo.
```

**Así que Ada completo no cabe; Ada reducido sí.**

Y el perfil reducido es exactamente el que Ada ya usa en sistemas embarcados (clase 146):

```ada
pragma Restrictions (No_Exception_Propagation);
pragma Restrictions (No_Tasking);
pragma Restrictions (No_Allocators);
```

**Y esa es la observación interesante: el subconjunto que hace falta para WebAssembly es el mismo que
Ada lleva cuarenta años usando en satélites.**

No es coincidencia: **un microcontrolador sin sistema operativo y un módulo WebAssembly aislado tienen
las mismas carencias** —sin hilos del sistema, sin sistema de ficheros, sin memoria dinámica ilimitada—
y por eso **los lenguajes que ya sabían funcionar sin sistema operativo llegaron antes**.

Es la razón por la que Rust y C fueron los primeros destinos serios de WebAssembly, y por la que los
lenguajes con recolector tardaron hasta que llegó la propuesta de recolección de basura en 2023.

Y merece cerrar con lo que Ada aporta al modelo de esta clase y que encaja sorprendentemente bien: **el
aislamiento de WebAssembly y las restricciones de Ada persiguen lo mismo por caminos distintos** — que un
componente **no pueda** hacer más de lo que se le permitió.

Uno lo consigue con el sistema de tipos y las restricciones del compilador; el otro, con el formato y el
entorno de ejecución. **Y combinados, dan un componente cuyo comportamiento está acotado por dos vías
independientes**, que es justo lo que un sistema crítico quiere.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Cuadrado;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  N: Int64;

begin
  Read(N);
  WriteLn('resultado=', IntToStr(N * N));
end.
```

**Lo que esta clase enseña en Pascal.** Free Pascal tiene una sorpresa para esta clase que merece el
titular del gancho: **soporta WebAssembly como destino nativo del compilador**.

```bash
fpc -Twasi -Pwasm32 prog.pas       # ← ¡un destino más, como Win64 o ARM!
```

**No hay Emscripten, ni LLVM, ni traducción a C**: **el generador de código de WebAssembly está dentro de
Free Pascal**, junto a los de x86, ARM, PowerPC, SPARC y los demás.

Y eso encaja con lo que la clase 147 destacaba del compilador: **Free Pascal está escrito en Pascal y
tiene generadores de código propios para cada arquitectura**, así que **añadir WebAssembly fue añadir un
generador más**.

Es una posición poco común: **la mayoría de los lenguajes de esta página llegan a WebAssembly a través de
LLVM o de C**, y Free Pascal llega directamente.

Y las dos variantes que soporta merecen distinguirse porque son las dos formas de usar WebAssembly:

```bash
fpc -Twasi -Pwasm32 prog.pas         # WASI: consola, ficheros, argumentos
fpc -Tembedded -Pwasm32 lib.pas       # módulo puro, para llamar desde JavaScript
```

**El primero produce un programa que se ejecuta con `wasmtime` o `wasmer`**, con entrada y salida
estándar — que es lo que este curso usa.

**Y el segundo produce un módulo sin sistema operativo**, para importar desde una página web y llamar
desde JavaScript.

Y el ecosistema ha construido encima lo que faltaba:

| Pieza | Qué aporta |
|---|---|
| **`wasmtime` / `wasmer`** | ejecutar módulos WASI fuera del navegador |
| **Enlace con JavaScript de FPC** | declarar funciones de JS y exportar las de Pascal |
| **`pas2js`** | **el otro camino: Pascal a JavaScript**, para interfaces |
| **Lazarus + `pas2js`** | aplicaciones web con el mismo código de escritorio |

**`pas2js` merece la mención** porque representa la alternativa histórica: **compilar a JavaScript en vez
de a WebAssembly**.

Y la comparación es la que esta clase debe dejar clara: **a JavaScript se llega antes y se integra mejor
con el navegador; a WebAssembly se llega con más rendimiento y con la semántica exacta del lenguaje
original** —enteros de 64 bits, punteros, aritmética predecible—.

Es el mismo compromiso que la clase 156 planteaba con las FFI: **traducir al idioma del anfitrión o
hablar el propio y pagar la frontera**.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let ((n (read)))
  (format t "resultado=~D~%" (* n n)))
```

**Lo que esta clase enseña en Common Lisp.** Lisp es el caso donde la pregunta del "por qué" de esta clase
muerde con más fuerza, y merece explicarlo porque es el argumento central: **Lisp necesita un recolector
de basura, y WebAssembly no tenía uno**.

```text
El modelo original de WebAssembly (2017):
  - memoria lineal: un gran arreglo de bytes
  - sin recolector
  - sin punteros gestionados
  - sin objetos ni estructuras
```

**Así que un lenguaje con recolección tenía que llevar el suyo dentro del módulo**, compilado a
WebAssembly, gestionando su propio montón dentro de la memoria lineal.

Y eso funciona —es lo que hacen las implementaciones de Lisp que llegaron por Emscripten— con dos
costes que merecen enunciarse:

**Uno, el tamaño**: el módulo incluye el recolector, el compilador y toda la biblioteca. Un "hola mundo"
de Lisp en WebAssembly puede ocupar megabytes.

**Y dos, la cooperación**: **el recolector del módulo no ve los objetos de JavaScript y viceversa**, así
que **un ciclo de referencias entre los dos mundos no se recoge nunca** — una fuga estructural.

Y las implementaciones que hoy funcionan:

| Implementación | Camino |
|---|---|
| **ECL** | compila a C, y de ahí con Emscripten |
| **JSCL** | Common Lisp **compilado a JavaScript**, en el navegador |
| **Clasp** | sobre LLVM, con camino a WebAssembly |
| **Hoot (Guile)** | **Scheme a WebAssembly, usando la propuesta de recolección** |

**Hoot merece el detalle** porque es la novedad que cambia esta clase: **la propuesta WasmGC**, aceptada
en 2023 y ya en los navegadores, **añade tipos gestionados y recolección de basura al propio
WebAssembly**.

```text
Con WasmGC, el lenguaje NO lleva su recolector:
  - usa el del entorno, que ya está ahí
  - los objetos son visibles para el recolector del navegador
  - y los ciclos entre módulos y JavaScript SÍ se recogen
```

**Y el resultado es drástico: los módulos pasan de megabytes a decenas de kilobytes.**

Es lo que ha permitido que Java, Kotlin, Dart, Scheme y OCaml lleguen a WebAssembly de forma práctica en
los últimos dos años, y es la respuesta a la pregunta del cierre de esta clase: **lo que el lenguaje
necesitaba y no estaba, acabó añadiéndose al formato**.

Es la historia de todas las máquinas virtuales universales: **empiezan mínimas y crecen hacia los
lenguajes que quieren atraer**.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea
set n [string trim $linea]

puts "resultado=[expr {$n * $n}]"
```

**Lo que esta clase enseña en Tcl.** Tcl llega a WebAssembly por el camino de Emscripten, y su caso
merece contarse porque **el resultado es especialmente útil**: **un intérprete completo dentro del
navegador**.

```bash
emconfigure ./configure --host=wasm32
emmake make
# → tcl.wasm: el intérprete entero
```

Y la diferencia con los lenguajes compilados de esta página es importante y merece subrayarse:

```text
Fortran o Pascal a WebAssembly:  se compila EL PROGRAMA.
Tcl a WebAssembly:                se compila EL INTÉRPRETE,
                                  y luego ejecuta cualquier guion.
```

**Eso significa que el módulo puede ejecutar código que no existía cuando se compiló** — lo que en el
navegador tiene un uso claro: **entornos interactivos, consolas y demostraciones**.

Es exactamente lo mismo que hacen Pyodide con Python y WebR con R, y es una de las aplicaciones más
exitosas de WebAssembly: **llevar un lenguaje entero, con su ecosistema, a una página web**.

Y esta clase es el sitio para señalar una coincidencia que Tcl ilumina bien: **WebAssembly redescubrió la
arquitectura de Tcl**.

| Idea | Tcl (1988) | WebAssembly (2017) |
|---|---|---|
| Un motor pequeño, incrustable | **el intérprete como biblioteca** (clase 155) | el módulo, con su tiempo de ejecución |
| **Aislamiento por defecto** | **Safe-Tcl** (clase 153) | el módulo no puede hacer nada sin permiso |
| Capacidades concedidas una a una | **los *alias*** de Safe-Tcl | **las importaciones** del módulo |
| Extensible por el anfitrión | comandos nuevos en C | funciones importadas |

**La tercera fila es la coincidencia notable**: **un módulo WebAssembly declara qué funciones importa, y
el anfitrión decide cuáles le da** — que es literalmente el mecanismo de los alias de Safe-Tcl, treinta
años después.

Es la mejor ilustración de la tesis del cierre de esta clase: **lo importante de WebAssembly no es el
rendimiento, es el modelo de seguridad** — y ese modelo es el de capacidades que la clase 153 describía,
adoptado por fin como norma de la industria.

Y **WASI**, la interfaz de sistema de WebAssembly, lo lleva al extremo:

```bash
wasmtime --dir=./datos prog.wasm      # ← solo ve ESE directorio. Nada más.
```

**El módulo recibe un descriptor del directorio permitido y no puede nombrar rutas fuera de él.** Es
seguridad por capacidades aplicada al sistema de ficheros, y es de las pocas veces que un modelo
académicamente correcto ha llegado a la práctica masiva.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $n = <STDIN>;
chomp $n;

print "resultado=", $n * $n, "\n";
```

**Lo que esta clase enseña en Perl.** Aquí está una de las sorpresas del gancho, y merece contarla porque
es un proyecto notable de una sola persona: **WebPerl**.

**Hauke Dämpfling compiló el intérprete de Perl completo a WebAssembly con Emscripten**, y el resultado
es que **se puede escribir Perl en una página web**:

```html
<script src="webperl.js"></script>
<script type="text/perl">
    use strict; use warnings;
    my @datos = map { $_ * 2 } (1 .. 10);
    js('document')->getElementById('salida')->{innerHTML} = "@datos";
</script>
```

**`<script type="text/perl">` funciona como `type="text/javascript"`**, y **`js(...)` da acceso al DOM
desde Perl**.

Y merece señalar lo que eso implica técnicamente, porque es más de lo que parece: **Perl completo**
—expresiones regulares, referencias, el recolector por conteo, `eval`, los módulos puros de CPAN— **corre
en el navegador**.

Y las limitaciones son exactamente las del cierre de esta clase:

| Necesita Perl | Estado |
|---|---|
| Recolección por conteo de referencias | **sí**: es suya, va dentro del módulo |
| **Módulos XS** (compilados en C) | **no**: habría que compilarlos también |
| `fork`, procesos, señales | **no** |
| Sockets | solo a través de JavaScript |
| Sistema de ficheros | el virtual de Emscripten, en memoria |

**La segunda fila es la que más limita**, y es la misma que afecta a Pyodide con las extensiones de
Python: **el ecosistema de un lenguaje maduro incluye mucho código compilado**, y llevarlo entero
requiere recompilarlo todo.

Y merece extraer la observación general que este caso ilustra mejor que ninguno de esta página:
**WebAssembly no porta lenguajes, porta implementaciones**.

Lo que llega al navegador **no es "Perl": es el intérprete de Perl compilado**, con sus decisiones, sus
dependencias y sus limitaciones.

Y por eso el trabajo real de portar un lenguaje a WebAssembly **no está en el generador de código: está
en la biblioteca de ejecución** —qué hace cuando pide memoria, cuando abre un fichero, cuando crea un
hilo— y en decidir qué se emula, qué se delega al anfitrión y qué simplemente no estará.

Es la misma conclusión que Ada y Lisp en esta página, dicha desde el otro extremo del espectro.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>

int main() {
    long long n{};
    if (!(std::cin >> n)) return 1;

    std::cout << "resultado=" << n * n << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** C++ es **el lenguaje con el que nació WebAssembly**, y merece contar
la historia porque explica el diseño del formato.

```text
2011: Alon Zakai escribe EMSCRIPTEN: compila LLVM a JavaScript.
      Funciona, y es lento.
2013: asm.js — un SUBCONJUNTO de JavaScript con anotaciones de tipo,
      que los motores pueden compilar a código nativo directamente.
      El navegador lo ejecuta como JavaScript normal si no lo reconoce.
2015: los cuatro fabricantes de navegadores acuerdan WebAssembly.
2017: soporte en todos los navegadores.
2019: WASI — WebAssembly fuera del navegador.
2023: WasmGC y componentes.
```

**El paso de 2013 es el ingenioso**: asm.js era **JavaScript válido**, así que funcionaba en todas
partes, y **los motores que lo reconocían lo compilaban a nativo**.

Es una técnica de compatibilidad que merece admirarse: **desplegar algo nuevo que degrada limpiamente en
lo viejo**.

Y compilar C++ es directo:

```bash
emcc prog.cpp -O2 -o prog.html                  # navegador, con HTML y JS
emcc prog.cpp -O2 -s WASM=1 -o prog.js           # solo el módulo
clang --target=wasm32-wasi prog.cpp -o prog.wasm  # WASI, sin Emscripten
```

Y los casos de uso reales de C++ en WebAssembly son de los más visibles del ecosistema:

| Aplicación | Qué es |
|---|---|
| **Figma** | editor de diseño; el motor de renderizado en C++ |
| **AutoCAD web** | décadas de C++ llevadas al navegador |
| **Google Earth** | idem |
| **FFmpeg.wasm** | codificación de vídeo en el cliente |
| **SQLite wasm** | base de datos completa en la página |
| **Unity / Unreal** | juegos, con el motor compilado |

**Ese es el argumento económico de esta clase**: **millones de líneas de C++ validado que antes solo
funcionaban instaladas, funcionan ahora en una pestaña**.

Y las limitaciones que C++ encuentra merecen decirse porque son las del cierre:

```text
- Las excepciones costaban mucho; ahora hay una propuesta nativa
- Los hilos requieren SharedArrayBuffer y cabeceras de aislamiento cruzado
- No hay JIT dentro del módulo: nada de generar código en marcha
- El tamaño del módulo importa: hay que descargarlo
```

**La segunda merece la advertencia práctica**: **`std::thread` funciona en WebAssembly solo si el
servidor envía las cabeceras COOP y COEP**, y muchos no las envían — con lo que un programa que compila
falla al arrancar en producción.

Es un buen recordatorio de que **el destino de compilación trae su propio contrato con el entorno**, y de
que conviene leerlo antes de prometer nada.

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

dcl-pi CUADRADO;
  n int(10) const;
end-pi;

dcl-s r int(20);

r = n * n;

dsply ('resultado=' + %char(r));

*inlr = *on;
return;
```

**Lo que esta clase enseña en RPG.** RPG **no compila a WebAssembly**, y merece explicar por qué, porque
la razón es exactamente la del cierre de esta clase y es más interesante que la lista de los que sí.

```text
RPG no es solo un lenguaje: es un lenguaje ATADO a una plataforma.

Un programa RPG usa:
  - ficheros de la base de datos integrada, con acceso por clave
  - la lista de bibliotecas para resolver nombres (clase 148)
  - grupos de activación y el manejo de condiciones de ILE (clase 157)
  - punteros de 16 bytes con etiqueta por hardware (clase 153)
  - y ficheros de pantalla 5250
```

**Nada de eso existe fuera de IBM i.** Un "RPG a WebAssembly" tendría que llevar consigo medio sistema
operativo.

Y esa es la observación que merece extraerse y que vale para muchos lenguajes: **la portabilidad de un
lenguaje no depende de su sintaxis, sino de cuánto de su semántica está en la plataforma**.

C es portable porque supone muy poco. RPG no lo es porque supone mucho — **y eso mismo es lo que lo hace
productivo en su plataforma** (clases 142 y 148).

Y aun así, la plataforma sí participa del mundo de WebAssembly por otra vía, y merece nombrarla:

```text
En PASE (el entorno AIX dentro de IBM i) se pueden ejecutar:
   - Node.js, y por tanto módulos WebAssembly
   - Python, con wasmtime
   - y runtimes de WebAssembly compilados para POWER
```

**Así que IBM i puede EJECUTAR WebAssembly aunque RPG no compile a él** — y ese reparto tiene sentido con
la arquitectura de la clase 149: **la lógica de negocio en RPG, y los componentes portables de terceros
como módulos aislados**.

Y merece cerrar con lo que sí se está haciendo en esta plataforma y que persigue el mismo objetivo que
esta clase: **exponer la lógica como API** (clase 160) **y consumirla desde donde sea**.

Es la alternativa a portar el código: **no mover la lógica, mover la frontera**. Y para un sistema que
funciona, está validado y no se puede parar, suele ser la decisión correcta — que es la misma conclusión
que la clase 150 alcanzaba sobre las reescrituras.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 cuadrado: procedure options(main);

    declare n fixed binary(31);
    declare r fixed binary(63);

    get list (n);
    r = n * n;

    put skip list ('resultado=' || trim(char(r)));

 end cuadrado;
```

**Lo que esta clase enseña en PL/I.** PL/I comparte el diagnóstico de RPG en esta página —**no hay un
compilador a WebAssembly**— y por razones que merecen distinguirse, porque no son las mismas.

**RPG no llega porque su semántica está en la plataforma. PL/I no llega porque no hay quien lo lleve.**

```text
Los compiladores de PL/I en producción son:
  - IBM Enterprise PL/I para z/OS      (propietario)
  - IBM PL/I para AIX / Windows         (propietario)
  - Iron Spring PL/I                     (subconjunto, para OS/2 y Linux)

No hay ningún compilador de PL/I sobre LLVM ni sobre GCC con soporte activo.
```

**Y sin una interfaz con LLVM, no hay camino a WebAssembly** — porque casi todos los destinos nuevos
llegan por ahí (clase 123).

Y merece extraer la lección, porque es de las más importantes de este curso y aparece aquí con claridad:
**la supervivencia de un lenguaje depende de que alguien mantenga una implementación libre**.

Compárese con los demás de esta página:

| Lenguaje | Implementación libre | ¿Llega a destinos nuevos? |
|---|---|---|
| COBOL | **GnuCOBOL** | sí, vía C |
| Fortran | **gfortran, LLVM Flang** | sí |
| Ada | **GNAT (FSF)** | sí, vía GCC y LLVM |
| Pascal | **Free Pascal** | **sí, con generador propio** |
| Lisp | **SBCL, ECL, Clasp** | sí |
| Tcl, Perl, C++ | libres | sí |
| **PL/I** | **no** | **no** |
| **RPG** | no | no |

**Las dos últimas filas son las únicas de esta página sin implementación libre**, y son las dos que se
quedan fuera de cada plataforma nueva.

Es una observación de fondo sobre el ecosistema del software: **un lenguaje sin implementación libre
depende, para cada plataforma nueva, de que su propietario decida invertir** — y esa decisión se toma
mirando el mercado, no la técnica.

Y por eso el destino de PL/I está donde está: **millones de líneas en producción, funcionando
perfectamente, en una plataforma concreta y sin camino de salida más allá de la traducción a otro
lenguaje** — que es lo que la clase 150 llamaba el patrón del estrangulador, aplicado a un lenguaje
entero.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
CUADRADO ; Elevar al cuadrado -- clase 162
 read n
 write "resultado=", n * n, !
 quit
```

**Lo que esta clase enseña en M.** M sí llega a WebAssembly, y por el camino que su implementación libre
permite: **YottaDB está escrito en C, y C compila a WebAssembly**.

**Y hay algo más interesante que merece contarse**: existen **intérpretes de M escritos para el
navegador**, y **Mumps.js** y proyectos similares permiten ejecutar rutinas M en una página.

Pero la parte sustancial de esta clase para M es otra, y merece explicarla porque toca el problema real
de este ecosistema: **el motor de base de datos no cabe en el modelo**.

```text
Un sistema M no es un intérprete: es un intérprete MÁS una base de datos
con transacciones, bloqueos, diario y memoria compartida entre procesos.

WebAssembly (sin extensiones) no tiene:
  - memoria compartida entre módulos
  - ficheros mapeados
  - bloqueos entre procesos
  - ni procesos
```

**Así que lo que puede llegar al navegador es un M de un solo proceso, con la base en memoria** — útil
para docencia y para demostraciones, no para un hospital.

Y esta clase es el sitio para señalar dónde WebAssembly sí encaja bien con este mundo, y es una idea que
merece destacarse: **como formato de extensión segura**.

```text
Un sistema clínico necesita ejecutar reglas escritas por el hospital:
  cálculos de dosis, alertas, validaciones locales.

Hoy eso se hace con código M dentro del diccionario de datos (clase 151),
que es ejecución de código arbitrario con todos los permisos (clase 153).

Un módulo WebAssembly haría lo mismo con AISLAMIENTO:
  - solo puede llamar a las funciones que se le den
  - no puede tocar globals que no se le pasen
  - y el consumo de CPU y memoria se puede acotar
```

**Eso es el modelo de capacidades del cierre de esta clase aplicado exactamente donde hace falta**, y es
lo que ya hacen sistemas modernos con complementos: **Envoy, Istio y varias bases de datos ejecutan
extensiones de usuario como módulos WebAssembly precisamente por eso**.

Y merece cerrar con la observación general que este caso ilustra: **el uso más valioso de WebAssembly no
es portar lenguajes viejos a la web — es ejecutar código de terceros con garantías**.

La portabilidad es lo llamativo; **el aislamiento es lo que resuelve un problema que no tenía solución
buena**.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| n |

n := stdin nextLine trimBoth asNumber.

Transcript show: 'resultado=', (n * n) printString; cr.
```

**Lo que esta clase enseña en Smalltalk.** Smalltalk tiene, para esta clase, la observación más
irónica de toda la página, y merece decirla claramente: **Smalltalk lleva haciendo esto desde 1980**.

```text
Smalltalk-80 ya tenía:
  - un formato de BYTECODE portátil (clase 125)
  - una máquina virtual pequeña, portable a cualquier hardware
  - una IMAGEN que se ejecuta igual en cualquier plataforma
  - y aislamiento: el código no puede tocar memoria arbitraria (clase 129)
```

**Es, punto por punto, la lista de propiedades de WebAssembly** — cuarenta años antes.

Y esta clase permite ver la genealogía completa de la idea, que merece ordenarse:

| Año | Sistema | Qué aportó |
|---|---|---|
| 1966 | **O-code** (BCPL) | bytecode portátil |
| 1970 | **P-code** (Pascal) | **el compilador se portaba escribiendo un intérprete** |
| **1980** | **Smalltalk-80** | bytecode + imagen + VM portable |
| 1995 | **JVM** | bytecode con verificación y **seguridad** |
| 2002 | **CLR (.NET)** | bytecode **multi-lenguaje** desde el diseño |
| 2013 | **asm.js** | subconjunto de JavaScript compilable |
| **2017** | **WebAssembly** | binario, verificado, aislado, multi-lenguaje |

**El P-code de Pascal merece destacarse** porque su idea era la misma de esta clase y funcionó: **para
llevar Pascal a una máquina nueva bastaba con escribir un intérprete de P-code**, y así se extendió el
lenguaje por decenas de arquitecturas en los años setenta.

Y Smalltalk llega hoy a WebAssembly por varios caminos:

| Proyecto | Qué es |
|---|---|
| **SqueakJS** | **la máquina virtual de Squeak en JavaScript**: ejecuta imágenes reales de 1998 |
| **Squeak/Pharo con Emscripten** | la VM compilada a WebAssembly |
| **PharoJS** | traduce código Pharo a JavaScript |

**SqueakJS merece el cierre**, porque demuestra algo de esta clase de forma contundente: **puede cargar y
ejecutar en el navegador una imagen de Smalltalk-80 de 1978**, restaurada, **con su interfaz original
funcionando**.

**Cuarenta y ocho años de compatibilidad binaria, en una pestaña.**

Y esa es la mejor conclusión de esta clase y de la Parte 10 entera: **el bytecode portátil no es una idea
nueva, y lo que WebAssembly ha aportado no es la técnica sino el acuerdo**.

Lo difícil nunca fue definir un formato intermedio —hay decenas— sino **conseguir que todos los
fabricantes implementaran el mismo**. Y eso, que es un problema de coordinación y no de ingeniería, es lo
que había impedido durante cuarenta años que la idea de Smalltalk se convirtiera en la infraestructura de
todos.

---

## Y de vuelta a la clase

Lo transferible: **WebAssembly no es un lenguaje ni un sustituto de nada — es un objetivo de compilación
con aislamiento por defecto**. Y esa última parte es lo importante: **un módulo no puede hacer nada que
no se le haya dado explícitamente**, ni leer ficheros, ni abrir sockets, ni ver la memoria de nadie. Es
el modelo de capacidades de la clase 153 aplicado al despliegue. La regla práctica al considerarlo:
**preguntar qué necesita el lenguaje que no está en el modelo** —recolector, hilos, sistema de
ficheros— porque de eso depende si la portabilidad sale casi gratis o cuesta un año.

⏮️ [Volver a la clase 162](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
