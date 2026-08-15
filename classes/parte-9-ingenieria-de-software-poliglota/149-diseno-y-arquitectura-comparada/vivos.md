# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 149

> [⬅️ Volver a la clase 149](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Contar capas: `web api datos` son tres. Es la abstracción más repetida de la industria, y esta clase la
pone frente a las alternativas que estos lenguajes practican. Y hay un dato que conviene tener presente
al hablar de arquitectura: **el patrón Modelo-Vista-Controlador se inventó en Smalltalk-80**, lo
describió Trygve Reenskaug en Xerox PARC en 1979, y **todo lo que hoy se llama arquitectura de
aplicaciones interactivas desciende de ahí**.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es la **arquitectura como reparto de responsabilidades**, y estos lenguajes lo enseñan
> porque **practican arquitecturas distintas de la de tres capas**, y todas siguen funcionando. **COBOL y
> JCL: la canalización de lotes**, donde cada paso es un programa y el acoplamiento es un fichero.
> **Fortran: capas numéricas**, con BLAS y LAPACK como ejemplo canónico de biblioteca en niveles. **M:
> arquitectura centrada en los datos**, donde el esquema es el sistema. **Y Smalltalk: MVC y objetos**.
>
> Y aparece la pregunta de fondo: **¿qué decide dónde va cada cosa?** Porque toda arquitectura es una
> respuesta a esa pregunta, y las respuestas difieren mucho más de lo que el vocabulario común sugiere.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: una línea con nombres de capas (palabras separadas por espacio) → stdout: `capas=<cantidad>`
- **Regla:** `contar los nombres de capa`

| stdin | esperado |
|---|---|
| `web api datos` | `capas=3` |
| `cli` | `capas=1` |
| `web api datos cache` | `capas=4` |

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
PROGRAM-ID. CAPAS.

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
    DISPLAY "capas=" FUNCTION TRIM(ED)
    STOP RUN.
```

**Lo que esta clase enseña en COBOL.** El mundo del lote practica una arquitectura que merece conocerse
porque es excelente y porque la industria la reinventó dos veces: **la canalización de pasos**.

```jcl
//PASO1 EXEC PGM=EXTRAER      <-- lee la base, escribe un fichero
//PASO2 EXEC PGM=SORT           <-- ordena
//PASO3 EXEC PGM=VALIDAR         <-- lee, valida, escribe válidos y rechazos
//PASO4 EXEC PGM=CALCULAR         <-- lee válidos, calcula, escribe resultados
//PASO5 EXEC PGM=INFORMAR          <-- lee resultados, imprime
```

Y sus propiedades son las que hoy se buscan en cualquier sistema de procesamiento de datos:

- **Cada paso es un programa independiente**, con una entrada y una salida.
- **El acoplamiento es un fichero con formato declarado**, no una llamada.
- **Cada paso se puede reejecutar solo**, si falla, sin repetir los anteriores.
- **Se puede insertar un paso nuevo en medio** sin tocar los demás.
- **Y cada paso se prueba dando un fichero de entrada y comparando la salida** (clase 139).

**Eso es la arquitectura de tuberías y filtros**, y es la misma que Unix adoptó con `|`, la que
MapReduce popularizó, y la que hoy tienen Airflow, Spark y cualquier orquestador de datos.

Y merece señalar la diferencia con la arquitectura de tres capas que el gancho nombra: **aquí no hay
capas, hay etapas**. El eje no es "presentación / lógica / datos" sino "paso 1 / paso 2 / paso 3".

Es una arquitectura orientada al flujo, no a la responsabilidad, y para procesamiento por lotes es
mejor.

Y el mismo mundo tiene la otra arquitectura, la transaccional, que sí es en capas:

```text
Terminal 3270  →  CICS (control de transacción)  →  Programa COBOL  →  DB2
                        ↑                              ↑
                  presentación (BMS)            lógica de negocio
```

Y el problema arquitectónico clásico de estos sistemas es exactamente el de la segunda regla del cierre:
**los programas COBOL de los años ochenta mezclaban las tres capas**, con `EXEC CICS SEND MAP` —
presentación— y `EXEC SQL` —datos— en el mismo párrafo que el cálculo.

Y de ahí que la modernización de estos sistemas consista, casi siempre, en **separar la lógica de
negocio de la presentación** para poder exponerla como servicio.

Es la misma operación que la clase 150 llamará refactorización, hecha a escala de millones de líneas, y
es la razón por la que "extraer la lógica a un programa llamable" es la tarea número uno de cualquier
proyecto de modernización de COBOL.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program capas
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

   write(*, '(A,I0)') 'capas=', cnt
end program capas
```

**Lo que esta clase enseña en Fortran.** El cálculo científico tiene una arquitectura en capas propia, y
es probablemente **el ejemplo más exitoso de arquitectura por niveles de toda la historia del
software**: **BLAS y LAPACK**.

```text
Aplicación del usuario
      ↓
LAPACK      -- resolución de sistemas, valores propios, descomposiciones
      ↓
BLAS nivel 3 -- operaciones MATRIZ-matriz  (gemm)
BLAS nivel 2  -- matriz-VECTOR             (gemv)
BLAS nivel 1   -- vector-vector            (axpy, dot)
      ↓
la implementación optimizada de CADA fabricante
```

Y el motivo por el que esto funcionó tan extraordinariamente bien merece explicarse, porque es una
lección de arquitectura de primer orden:

**BLAS es una especificación de interfaz, no una implementación.** Define exactamente qué hace `dgemm`
—multiplicar matrices de dobles— y con qué argumentos, **y nada más**.

Y entonces:

- **Intel, AMD, NVIDIA, IBM y ARM escriben su propia implementación**, optimizada hasta el último ciclo
  para su hardware.
- **LAPACK se escribió encima**, expresando todos sus algoritmos **en términos de BLAS nivel 3**.
- **Y cualquier programa que use LAPACK se acelera automáticamente** al enlazar con la BLAS del
  fabricante.

**La decisión clave fue expresarlo todo en operaciones matriz-matriz**, porque son las que permiten
aprovechar la caché (clase 128): una multiplicación de matrices hace muchas operaciones por cada dato
leído de memoria, y una operación vector-vector hace una.

**Esa reescritura de LINPACK a LAPACK, en los años ochenta, multiplicó por diez el rendimiento sin
cambiar ningún algoritmo** — solo reorganizando el código para que usara la capa correcta.

Es la mejor demostración de la primera regla del cierre: **la arquitectura correcta hizo fácil un cambio
que de otro modo habría sido imposible**, porque nadie va a reescribir sesenta años de código numérico
para cada procesador nuevo.

Y el ecosistema moderno sigue el patrón:

| Capa | Ejemplos |
|---|---|
| Aplicación | modelos climáticos, CFD, dinámica molecular |
| **Marcos** | PETSc, Trilinos, deal.II |
| **Solvers** | LAPACK, ScaLAPACK, MUMPS, SuperLU |
| **Núcleo** | BLAS (OpenBLAS, MKL, BLIS), FFTW |
| **Comunicación** | MPI |

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO; use Ada.Text_IO;
with Ada.Strings;
with Ada.Strings.Fixed;

procedure Capas is
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

   Put_Line ("capas=" & Ada.Strings.Fixed.Trim (Cnt'Image, Ada.Strings.Both));
end Capas;
```

**Lo que esta clase enseña en Ada.** Ada tiene una construcción que es **arquitectura expresada en el
lenguaje**, y merece ser el centro de esta explicación: **las unidades hijas**.

```ada
package Banco is ...                    --  el paquete raíz
package Banco.Cuentas is ...             --  hijo público
package Banco.Cuentas.Interes is ...      --  nieto
private package Banco.Interno is ...       --  hijo PRIVADO
```

Y las reglas de visibilidad son exactamente las de una arquitectura en capas, **y las comprueba el
compilador**:

**Un hijo ve la parte privada de su padre.** Es decir: `Banco.Cuentas` puede acceder a los detalles
internos de `Banco`, pero **nadie de fuera puede**.

**Y un paquete hijo privado solo es visible dentro del árbol del padre.** `Banco.Interno` **no se puede
usar desde fuera de `Banco`**, y el compilador rechaza el `with`.

**Eso es control de dependencias arquitectónicas impuesto por el compilador**, y es lo que en otros
lenguajes hay que conseguir con herramientas externas —ArchUnit en Java, reglas de `import` en
analizadores— o con disciplina y esperanza.

Y Ada tiene una segunda construcción que resuelve la segunda regla del cierre de forma directa: **las
restricciones de dependencia en el fichero de proyecto**.

```ada
project Dominio is
   for Source_Dirs use ("src/dominio");
   --  y NO depende de nada de infraestructura
end Dominio;

project Infraestructura is
   for Source_Dirs use ("src/infra");
   --  este SÍ depende de Dominio
end Infraestructura;
```

**Un proyecto declara de qué otros proyectos depende, y `gprbuild` se niega a compilar si alguien
importa hacia el lado equivocado.**

Es la arquitectura hexagonal —o de puertos y adaptadores— **verificada por la construcción**, que es la
única forma de que sobreviva a dos años de prisas.

Y merece cerrar con la arquitectura que Ada practica en su dominio y que es distinta de las tres capas:
**el sistema de tiempo real como conjunto de tareas periódicas**.

```ada
task Sensor with Priority => 20;      --  cada 10 ms
task Control with Priority => 15;      --  cada 50 ms
task Registro with Priority => 5;       --  cuando sobre tiempo
```

**El eje de descomposición aquí no es la responsabilidad funcional: es el plazo temporal** (clase 135).
Y con el perfil Ravenscar (clase 146), **se puede demostrar que el conjunto cumple sus plazos**.

Es una arquitectura donde la propiedad que se garantiza no es la mantenibilidad: es el tiempo.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Capas;
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

  WriteLn('capas=', IntToStr(Cnt));
end.
```

**Lo que esta clase enseña en Pascal.** El ecosistema Delphi aporta a esta clase un caso de estudio muy
valioso, porque **su arquitectura por defecto era mala y la comunidad tardó años en salir de ella**.

El modelo original de Delphi era la **programación orientada a eventos con doble clic**: se dibujaba el
formulario, se hacía doble clic en un botón y **se escribía ahí la lógica**.

```pascal
procedure TForm1.Button1Click(Sender: TObject);
begin
  Query1.SQL.Text := 'SELECT * FROM clientes WHERE id = ' + Edit1.Text;
  Query1.Open;
  Label1.Caption := Query1.FieldByName('nombre').AsString;
end;
```

**Ahí están las tres capas en cinco líneas**: presentación, lógica y acceso a datos, con inyección SQL
de regalo (clase 153).

Y eso no era un accidente: **era el modelo que el producto promovía**, porque hacía espectacular la
demostración de dos minutos.

Y la salida de ahí es la historia de esta clase en el ecosistema:

**Primero, los módulos de datos** —`TDataModule`—: un contenedor **sin interfaz visual** donde poner los
componentes de acceso a datos, compartido entre formularios. **Es la primera separación real**, y es de
Delphi 2.

**Después, la separación en unidades por responsabilidad**, con la regla que hoy es evidente: **la
unidad del formulario no debe contener lógica de negocio**.

**Y hoy, el ecosistema moderno**: contenedores de inversión de control (Spring4D), interfaces para las
dependencias, y arquitectura por capas verificada.

Y merece extraer la lección general, porque es la más útil de esta página: **la arquitectura por defecto
de una herramienta es la que tendrá el 90 % del código**.

Si la forma más fácil de hacer algo mezcla las capas, **la mayoría del código las mezclará** — por
mucho que el documento de arquitectura diga otra cosa.

De ahí que la decisión arquitectónica más eficaz no sea escribir un diagrama, sino **hacer que el camino
correcto sea el más fácil**: una plantilla de proyecto, un generador, una comprobación en la integración
continua.

Es la aplicación práctica de la segunda regla del cierre: **una capa que no está impuesta por algo no
es una capa, es una intención**.

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
  (format t "capas=~D~%" cnt))
```

**Lo que esta clase enseña en Common Lisp.** Lisp practica una arquitectura que no aparece en ningún
diagrama de tres capas y que merece explicarse, porque es la más característica del lenguaje:
**construir un lenguaje hasta el problema**.

La idea, formulada por Paul Graham y practicada desde los años setenta:

> En lugar de escribir el programa en el lenguaje, **se extiende el lenguaje hacia el problema** hasta
> que el programa se pueda escribir en una página.

```lisp
;; capa 4: el problema, escrito en el vocabulario del dominio
(definir-flujo procesar-pedido
  (validar :contra esquema-pedido)
  (calcular-impuestos :segun pais)
  (reservar-stock :con-reintentos 3)
  (emitir-evento :pedido-confirmado))

;; capa 3: las macros que hacen que eso sea código válido
;; capa 2: las funciones de dominio
;; capa 1: Common Lisp
```

**`definir-flujo` no existe en Lisp: se define con `defmacro`** (clase 123), y a partir de ahí es
sintaxis del lenguaje.

Y las consecuencias arquitectónicas son reales, en los dos sentidos:

**A favor**, la capa superior es **legible por alguien del dominio** y muy densa: cada línea significa
mucho. Y los cambios habituales —añadir un paso, cambiar una regla— se hacen ahí, sin tocar nada más.

**En contra**, y hay que decirlo: **cada proyecto acaba con su propio lenguaje**, que nadie más conoce.
La curva de entrada de un desarrollador nuevo es alta, y **las herramientas genéricas no entienden ese
código**.

Es exactamente el compromiso que la clase 122 planteaba, aquí a escala de sistema.

Y Lisp tiene una segunda aportación arquitectónica de primer orden que merece nombrarse: **CLOS y el
protocolo de metaobjetos** (clase 111).

```lisp
(defgeneric calcular-precio (producto cliente))
(defmethod calcular-precio ((p Libro) (c ClienteVIP)) ...)
(defmethod calcular-precio ((p Digital) (c Cualquiera)) ...)
```

**El despacho múltiple cambia la arquitectura**: no hay que decidir si el método "pertenece" al producto
o al cliente, porque **pertenece a la relación entre ambos**.

En un lenguaje con despacho simple, esa decisión fuerza patrones —visitante, doble despacho— que existen
**solo para compensar la limitación**. Es un buen recordatorio de que **muchos patrones de diseño son
parches a carencias del lenguaje**, que es lo que la clase 151 desarrolla.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea

set capas [llength [split [string trim $linea]]]

puts "capas=$capas"
```

**Lo que esta clase enseña en Tcl.** `llength [split ...]` cuenta en un comando lo que las demás columnas
construyen a mano, y ese contraste es la arquitectura de Tcl en miniatura: **es un lenguaje de
pegamento, y su papel arquitectónico es unir cosas escritas en otros**.

Y esa arquitectura tiene nombre y una justificación explícita de su autor. **John Ousterhout la
formuló en 1998**:

> Los sistemas se construyen mejor con **dos lenguajes**: uno de sistemas —C, C++— para los componentes
> que necesitan rendimiento, y uno de guion —Tcl, Python— para **unirlos y configurarlos**.

**Y la métrica que daba es la clave del argumento**: el código de pegamento es **de cinco a diez veces
más corto** en un lenguaje de guion, y **el 90 % de los cambios de un sistema ocurren en el pegamento,
no en los componentes**.

Es la primera regla del cierre de esta clase con datos: **la arquitectura correcta es la que hace fácil
lo que se cambia a menudo**.

Y Tcl se diseñó para ese papel desde el primer día:

```c
/* Un componente en C expone comandos a Tcl */
Tcl_CreateObjCommand(interp, "simular", SimularCmd, NULL, NULL);
```

```tcl
# y el sistema se compone, se configura y se prueba en Tcl
simular -pasos 1000 -modelo $modelo -salida resultados.dat
```

**El componente pesado en C; la composición, los parámetros y el flujo en Tcl.**

Y esa arquitectura es la que domina en un sector entero que merece nombrarse, porque es el mayor éxito
del lenguaje: **el diseño de circuitos integrados**.

```tcl
# el flujo de síntesis de un chip, en Tcl
read_verilog diseno.v
set_clock_period 2.5
compile_ultra
report_timing
write_verilog netlist.v
```

**Synopsys, Cadence, Xilinx y Mentor exponen sus herramientas como comandos de Tcl**, y los flujos de
diseño —que son programas de decenas de miles de líneas— están escritos en él.

Es la arquitectura de aplicación embebible en su forma más pura: **el programa principal no es el
guion, es la herramienta; el guion es el que decide qué hace**.

Y la clase 163 volverá sobre esto — **el lenguaje embebido como decisión de arquitectura** — porque es
la razón por la que Lua está en los videojuegos y Tcl en el diseño de circuitos.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;

my @capas = split ' ', $linea;

print "capas=", scalar(@capas), "\n";
```

**Lo que esta clase enseña en Perl.** Perl es el caso de estudio de esta página sobre **qué pasa cuando
un lenguaje no impone ninguna arquitectura**, y su historia merece contarse porque tiene las dos mitades.

**La primera mitad: el guion que creció.**

Perl fue diseñado para guiones de una página, y su lema —"hay más de una forma de hacerlo"— es lo
contrario de una arquitectura. El resultado, en los años noventa, fueron sistemas enteros escritos como
guiones CGI de tres mil líneas, sin módulos, con variables globales y HTML mezclado con SQL.

**Ese código es el origen de la mala fama del lenguaje**, y es justo reconocer que la culpa no era del
lenguaje sino de que **nada empujaba hacia otra cosa** — el mismo diagnóstico que Pascal en esta página.

**Y la segunda mitad: la comunidad construyó la arquitectura por encima.**

| Pieza | Qué aportó |
|---|---|
| **Moose** (2006) | **un sistema de objetos completo**: roles, atributos, tipos, modificadores |
| **Plack / PSGI** | la interfaz común servidor-aplicación (como WSGI y Rack) |
| **DBIx::Class** | mapeo objeto-relacional |
| **Catalyst / Dancer / Mojolicious** | marcos MVC |
| **Try::Tiny** | manejo de excepciones sano |

**Moose merece el detalle**, porque es de las mejores implementaciones de un concepto arquitectónico que
esta clase debe nombrar: **los roles**.

```perl
package Nadador;
use Moose::Role;
requires 'mover';                    # quien tome este rol DEBE tener 'mover'
sub nadar { ... }

package Pato;
use Moose;
with 'Nadador', 'Volador';            # COMPONER comportamientos
```

**Un rol es un conjunto de métodos que se compone en una clase, con requisitos declarados** — y a
diferencia de la herencia múltiple, **los conflictos son errores en tiempo de composición**, no
resoluciones silenciosas por orden (clase 111).

Es la solución al problema que la herencia múltiple plantea, la misma que adoptaron los *traits* de
Scala y de Rust, y viene de la investigación en Smalltalk de 2003.

Y la lección de esta página es la que el ecosistema Perl demostró: **la arquitectura se puede añadir
después**, con bibliotecas y disciplina, incluso a un lenguaje que no la fomenta. Cuesta más, y funciona.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>
#include <string>

int main() {
    std::string capa;
    int cnt = 0;
    while (std::cin >> capa) ++cnt;

    std::cout << "capas=" << cnt << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** C++ tiene una restricción arquitectónica que ningún otro lenguaje de
esta página comparte con la misma fuerza, y es la que de verdad decide la estructura de un proyecto
grande: **las dependencias de compilación son físicas, no lógicas**.

```cpp
// cliente.hpp
#include "pedido.hpp"      // ← quien incluya cliente.hpp compila TAMBIÉN pedido.hpp
class Cliente { Pedido ultimo_; };
```

**Incluir una cabecera es depender de ella en tiempo de compilación**, y eso se propaga: un proyecto mal
estructurado acaba con **cada fichero compilando medio sistema**, y **una construcción de una hora**.

De ahí que la arquitectura de C++ tenga un vocabulario propio, y merece conocerlo porque es real:

**Declaración adelantada** en lugar de inclusión, cuando basta con un puntero o una referencia:

```cpp
class Pedido;                    // no hace falta la definición completa
class Cliente { Pedido* ultimo_; };
```

**El patrón *pimpl***, que oculta la implementación entera:

```cpp
class Cliente {
public:
    Cliente(); ~Cliente();
    void procesar();
private:
    struct Impl;
    std::unique_ptr<Impl> p_;    // los detalles están en el .cpp
};
```

**Con `pimpl`, cambiar los miembros privados no obliga a recompilar a los clientes** — y además **no
cambia el ABI** (clase 143), lo que permite actualizar una biblioteca compartida sin recompilar lo que
la usa.

Es la única forma en C++ de conseguir lo que Ada tiene de serie con la separación de especificación y
cuerpo (clase 143).

Y el vocabulario arquitectónico de la comunidad, que John Lakos formalizó en *Large-Scale C++ Software
Design* (1996):

| Concepto | Qué significa |
|---|---|
| **Niveles** | el grafo de dependencias debe ser **acíclico**, y cada componente tiene un nivel |
| **Componente** | un par `.hpp` / `.cpp`: **la unidad física de diseño** |
| **Insulation** | ocultar la implementación para romper dependencias de compilación |
| **Escalable** | una jerarquía en la que se puede probar de abajo arriba |

**"El grafo debe ser acíclico" es la segunda regla del cierre de esta clase**, y en C++ tiene una
consecuencia física inmediata: **un ciclo de dependencias entre componentes hace imposible probarlos por
separado y multiplica el tiempo de compilación**.

Y las herramientas modernas lo comprueban:

```bash
include-what-you-use *.cpp        # cada fichero incluye lo que usa, y nada más
cpp-dependencies --graph          # el grafo de dependencias, para ver los ciclos
```

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

dcl-pi CAPAS;
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

dsply ('capas=' + %char(cnt));

*inlr = *on;
return;
```

**Lo que esta clase enseña en RPG.** El mundo IBM i tiene una evolución arquitectónica en tres etapas que
es la historia de esta clase contada en una plataforma, y merece verla completa.

**Etapa 1 — el programa monolítico (1988-2000):**

```text
Un programa RPG que:
  - dibuja la pantalla 5250   (especificaciones O y ficheros de pantalla)
  - lee y escribe la base      (acceso registro a registro)
  - y calcula                   (en medio de todo lo anterior)
```

**Las tres capas en un objeto**, exactamente como Delphi y COBOL en esta página.

**Etapa 2 — el programa de servicio (2000-2015):**

```rpgle
// La lógica sale a procedimientos exportados
dcl-proc calcularDescuento export;
  dcl-pi *n packed(9:2);
    cliente char(10) const;
    importe packed(9:2) const;
  end-pi;
  ...
end-proc;
```

**Y con eso llegó todo lo demás**: pruebas unitarias (clase 139), reutilización entre programas,
versionado por firma (clase 143) y la posibilidad de que un programa Java llamara a la misma lógica.

**Es la separación que hizo posible modernizar sin reescribir**, y sigue siendo la recomendación número
uno de la plataforma.

**Etapa 3 — la API (2015-hoy):**

```rpgle
// El mismo procedimiento, expuesto como servicio web con IWS
// o consumido desde una aplicación web moderna
exec sql SELECT ... ;                    // acceso por conjuntos, no por registro
```

| Pieza | Qué permite |
|---|---|
| **IWS** (*Integrated Web Services*) | **convertir un programa RPG en un servicio REST**, sin código |
| **`YAJL` / `DATA-INTO` / `DATA-GEN`** | JSON nativo en RPG (clase 105) |
| **Db2 for i con SQL** | conjuntos en vez de bucles registro a registro |
| **Node.js / Python en PASE** | la capa web moderna, en la misma máquina |

**`DATA-INTO` merece la mención** porque es la pieza que faltaba: **analiza JSON o XML directamente a
una estructura de datos RPG**, con una sola instrucción.

Y la arquitectura resultante es la que la plataforma recomienda hoy y que responde a la primera regla
del cierre: **la lógica de negocio en programas de servicio, estable y probada; la presentación en
cualquier tecnología, sustituible**.

Es la arquitectura hexagonal, alcanzada por evolución en una plataforma de 1988, y con una ventaja
concreta sobre las reescrituras: **la lógica de negocio de treinta años, que funciona y está validada,
no se toca**.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 capas: procedure options(main);

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

    put skip list ('capas=' || trim(char(cnt)));

 end capas;
```

**Lo que esta clase enseña en PL/I.** PL/I tiene una construcción que es directamente una decisión
arquitectónica del lenguaje y que merece explicarse, porque casi ningún lenguaje moderno la tiene: **los
procedimientos anidados con alcance léxico**.

```pli
 sistema: procedure options(main);
    declare estado fixed binary(31);        /* visible en TODO lo de dentro */

    contabilidad: procedure;
       declare saldo fixed decimal(11,2);    /* visible solo aquí y en sus hijos */

       calcular: procedure;
          saldo = saldo + estado;             /* ve las dos */
       end calcular;

    end contabilidad;
 end sistema;
```

**El anidamiento define la arquitectura**: lo que está dentro ve lo de fuera, y lo de fuera **no ve lo de
dentro**.

Es encapsulación por estructura léxica, y tiene una propiedad interesante para esta clase: **la
arquitectura está en la forma del fichero, no en un documento aparte**.

Y sus límites también merecen decirse, porque explican por qué el modelo no ganó: **el anidamiento es un
árbol**, y **las arquitecturas reales son grafos**. Cuando dos ramas del árbol necesitan compartir algo,
hay que subirlo al tronco — y el tronco crece hasta contenerlo todo.

Es exactamente el problema que los módulos con importación explícita resuelven, y por eso Ada, Modula-2
y todos los posteriores fueron por ahí.

Y PL/I aporta la arquitectura que su mundo practica, y que es la de COBOL en esta página: **la
canalización de pasos de lote y el sistema transaccional en capas**.

Con una particularidad propia que conviene conocer: **PL/I se usó mucho para programación de sistemas**
—Multics, el precursor de Unix, está escrito casi entero en PL/I— y ahí practicó una arquitectura que
merece nombrarse: **los anillos de protección**.

```text
Anillo 0: núcleo
Anillo 1-3: servicios del sistema
Anillo 4-7: aplicaciones de usuario
```

**Un anillo interior puede llamar al exterior, pero no al revés sin una puerta controlada.** Es la
segunda regla del cierre de esta clase —**la dependencia en un solo sentido**— implementada en el
hardware, en 1969.

Y de Multics salieron, además de Unix, la idea de sistema de ficheros jerárquico, la memoria virtual
segmentada y buena parte del vocabulario de la seguridad informática. **PL/I fue el lenguaje en que se
escribió todo eso**, y es una parte de su historia que suele olvidarse.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
CAPAS ; Contar capas -- clase 149
 read linea
 new i, cnt, p
 set cnt = 0
 for i = 1:1:$length(linea, " ") do
 . set p = $piece(linea, " ", i)
 . if p '= "" set cnt = cnt + 1
 write "capas=", cnt, !
 quit
```

**Lo que esta clase enseña en M.** M practica una arquitectura que casi no aparece en los libros y que es
la que sostiene VistA: **la arquitectura centrada en los datos**, donde **el esquema es el sistema**.

Y la pieza que la implementa merece explicarse en detalle, porque es una de las construcciones más
interesantes de esta página: **FileMan**.

**FileMan es una base de datos y un generador de aplicaciones escrito en M**, de 1979, y su idea central
es esta:

```text
El "diccionario de datos" describe cada fichero:
  - los campos, su tipo, su validación y su ayuda
  - los índices
  - las relaciones con otros ficheros
  - los permisos de lectura y escritura POR CAMPO
  - y las reglas de negocio, como código M asociado al campo
```

Y a partir de ese diccionario, **FileMan genera las pantallas de entrada, los informes, las búsquedas y
las validaciones** — sin escribir código para cada una.

```mumps
 do ^DIC       ; buscar en cualquier fichero: la interfaz sale del diccionario
 do ^DIE        ; editar: los campos, las validaciones y la ayuda salen del diccionario
 do ^DIP         ; imprimir: el informe se define, no se programa
```

**Eso es una arquitectura dirigida por metadatos**, y sus propiedades son las que hoy se buscan en
cualquier plataforma de bajo código:

- **Añadir un campo a una ficha de paciente actualiza las pantallas, los informes y las búsquedas**, sin
  tocar programas.
- **Las reglas de validación viven junto al dato**, no repartidas por la aplicación.
- **Y los permisos son por campo**, que en sanidad no es un lujo.

Y el coste hay que decirlo con la misma claridad: **el sistema entero depende del diccionario**, y un
cambio mal hecho ahí afecta a todo. Además, **la lógica escrita como código M dentro de los metadatos es
difícil de versionar y de revisar** (clase 145).

Es el mismo compromiso que cualquier plataforma dirigida por metadatos —Salesforce, SAP, los ERP en
general— y merece reconocerlo: **la flexibilidad de configurar en lugar de programar se paga con
opacidad**.

Y la lección para el cierre de esta clase: **la arquitectura de VistA hace facilísimo el cambio que su
dominio necesita todos los días** —añadir un campo, un informe, una validación clínica— **y difícil casi
todo lo demás**. Que es, exactamente, lo que se espera de una buena decisión arquitectónica.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| linea |

linea := stdin nextLine trimBoth.

Transcript show: 'capas=', (linea substrings: ' ') size printString; cr.
```

**Lo que esta clase enseña en Smalltalk.** Aquí está el dato del gancho, y merece desarrollarse porque es
el origen de casi todo el vocabulario de esta clase: **MVC se inventó en Smalltalk-80**.

**Trygve Reenskaug lo describió en Xerox PARC en 1979**, y el reparto original era este:

```text
Modelo       -- los datos y las reglas del dominio. NO sabe que existen las vistas.
Vista         -- cómo se presenta. Observa al modelo.
Controlador   -- interpreta la entrada del usuario (ratón, teclado) y actúa sobre el modelo.
```

Y **la pieza que lo hace funcionar es el mecanismo de dependencias**, que en Smalltalk-80 estaba en la
clase `Object`:

```smalltalk
modelo addDependent: unaVista.       "la vista se suscribe"
...
modelo changed: #saldo.               "y el modelo AVISA sin saber a quién"
```

**El modelo no conoce a las vistas: publica que algo cambió.** Eso es el patrón Observador (clase 120), y
está en la raíz de la jerarquía de clases desde 1980.

Y merece señalar una precisión histórica, porque el término se ha desdibujado: **el MVC original no es
el MVC de los marcos web**.

| Smalltalk-80 (1979) | Marcos web actuales |
|---|---|
| El controlador maneja **la entrada física** (ratón, teclado) | El controlador maneja **la petición HTTP** |
| La vista **observa** al modelo y se actualiza sola | La vista se **renderiza** una vez por petición |
| Hay **un trío por cada widget** de la pantalla | Hay un trío por **página** |

**En el MVC original, cada botón y cada campo tenía su propio trío**, y la composición de la interfaz era
la composición de esos tríos.

Lo que hoy más se parece al MVC original no son los marcos web clásicos: **son los marcos reactivos de
componentes** —donde cada componente observa su estado y se actualiza solo— que redescubrieron el modelo
treinta años después.

Y Smalltalk aporta a esta clase una segunda idea arquitectónica que merece nombrarse: **la arquitectura
es la jerarquía de clases y sus protocolos**.

```smalltalk
"Un 'protocolo' es un conjunto de mensajes que un objeto entiende.
 No hay declaración: si responde a los mensajes, sirve."
```

**El tipado por comportamiento** (clase 112) hace que la arquitectura se defina por **qué mensajes se
envían entre partes**, no por qué clases hay.

Y eso tiene una consecuencia práctica que conecta con el cierre de esta clase: **la frontera entre capas
es un conjunto de mensajes**, y se puede sustituir cualquier objeto por otro que responda a los mismos.

Es inyección de dependencias sin marco, objetos simulados sin biblioteca, y arquitectura hexagonal sin
interfaces declaradas — **porque el acoplamiento nunca fue al tipo, sino al comportamiento**.

---

## Y de vuelta a la clase

Lo transferible: **una arquitectura es un conjunto de decisiones difíciles de cambiar, y su valor está
en qué cambios hace fáciles**. De ahí la prueba que conviene aplicar a cualquier propuesta: **nombrar los
tres cambios más probables del próximo año y ver si la estructura los facilita o los estorba**. Y la
segunda regla, que es la que más se incumple: **las capas solo sirven si la dependencia va en un solo
sentido**; en cuanto la capa de datos conoce a la de presentación, hay tres capas en el diagrama y una
sola en la práctica.

⏮️ [Volver a la clase 149](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
