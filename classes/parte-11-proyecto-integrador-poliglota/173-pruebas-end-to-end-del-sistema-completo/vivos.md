# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 173

> [⬅️ Volver a la clase 173](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Comprobar el sistema entero con una entrada y una salida esperada: `e2e=pasa`. Es lo que hace el
verificador de este curso desde la clase 040, y lo que hacen las pruebas de extremo a extremo de
cualquier sistema. Y estos lenguajes aportan aquí la técnica más antigua y más eficaz que existe para
esto: **preparar unos ficheros de entrada, ejecutar el sistema y comparar la salida con una guardada** —
que es de los años sesenta y sigue siendo insuperable.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es la **prueba del sistema completo**, y estos lenguajes la enseñan porque **sus
> sistemas no se pueden probar de otra manera**: un lote de veinte pasos, una transacción que toca cuatro
> programas y dos bases de datos, o un cálculo que corre en mil procesos. Y de ahí salieron las técnicas
> que esta parte del curso ha ido nombrando: **la comparación de salidas** (clase 140), **la ejecución en
> paralelo** y **Expect** para lo que no tiene API (clase 147).
>
> Y aparece la tensión que define esta clase: **estas pruebas son las más valiosas y las más frágiles**.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: una línea `a b esperado` → stdout: `e2e=<pasa|falla>`
- **Regla:** `pasa si el sistema (a + b) da el esperado`

| stdin | esperado |
|---|---|
| `3 4 7` | `e2e=pasa` |
| `2 2 5` | `e2e=falla` |
| `10 5 15` | `e2e=pasa` |

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
PROGRAM-ID. E2E.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(60).
01  C-A     PIC X(15).
01  C-B     PIC X(15).
01  C-E     PIC X(15).
01  A       PIC S9(9) COMP.
01  B       PIC S9(9) COMP.
01  ESPER   PIC S9(9) COMP.

PROCEDURE DIVISION.
    ACCEPT LINEA
    UNSTRING LINEA DELIMITED BY ALL SPACES
        INTO C-A C-B C-E
    END-UNSTRING

    COMPUTE A     = FUNCTION NUMVAL(C-A)
    COMPUTE B     = FUNCTION NUMVAL(C-B)
    COMPUTE ESPER = FUNCTION NUMVAL(C-E)

    IF A + B = ESPER
        DISPLAY "e2e=pasa"
    ELSE
        DISPLAY "e2e=falla"
    END-IF
    STOP RUN.
```

**COBOL y las pruebas de extremo a extremo.** El mundo del lote inventó la técnica del gancho, y merece
verla completa porque es más elaborada de lo que parece:

```jcl
//PRUEBA JOB
//COPIAR  EXEC PGM=IEBGENER          <-- preparar los datos de entrada conocidos
//SISUT1   DD DSN=PRUEBA.ENTRADA.CASO01,DISP=SHR
//SISUT2   DD DSN=&&ENTRADA,DISP=(NEW,PASS)
//EJECUTA EXEC PROC=MIPROCESO         <-- ejecutar el sistema completo
//COMPARA EXEC PGM=ISRSUPC            <-- comparar la salida con la esperada
//NEWDD    DD DSN=&&SALIDA,DISP=SHR
//OLDDD    DD DSN=PRUEBA.ESPERADA.CASO01,DISP=SHR
//OUTDD    DD SYSOUT=*
```

**`ISRSUPC` —SuperC— es el comparador de IBM**, y es lo que hace esta técnica práctica, porque tiene una
capacidad que un `diff` normal no tiene:

```text
CMPCOLM 1:60,80:100      <-- comparar SOLO estas columnas
DPLINE '2026-'            <-- IGNORAR las líneas que contengan una fecha
```

**Poder excluir columnas y líneas es lo que hace usable la comparación de salidas**, porque **toda salida
real contiene cosas que cambian en cada ejecución**: fechas, horas, números de trabajo, contadores.

Es exactamente lo que `Test::Deep` con `ignore()` hace en Perl (clase 140), con cuarenta años de
adelanto.

Y merece señalar la segunda regla del cierre aplicada a este mundo, porque es donde falla: **los datos de
prueba**.

```text
✗ Ejecutar la prueba contra la base de datos de desarrollo compartida.
   → otro equipo cambia un cliente y la prueba falla mañana.

✓ Cada caso restaura sus propias tablas antes de ejecutarse,
   desde un juego de datos versionado.
```

**Y esa restauración es lo que hace que las pruebas de lote sean reproducibles**, y es la práctica
estándar en los sistemas serios: **juegos de datos de prueba tratados como código** (clase 145),
versionados y con dueño.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program e2e
   implicit none
   integer :: a, b, esperado

   read(*, *) a, b, esperado

   if (a + b == esperado) then
      write(*, '(A)') 'e2e=pasa'
   else
      write(*, '(A)') 'e2e=falla'
   end if
end program e2e
```

**Fortran y las pruebas de extremo a extremo.** El cálculo científico tiene la versión más difícil de esta
clase, y ya apareció en la clase 140: **la salida nunca es idéntica**.

```text
Comparar dos ejecuciones de una simulación:
  - con distinto compilador → el último dígito cambia
  - con distinto número de procesos → el orden de las sumas cambia
  - con la misma máquina y la misma versión → normalmente sí coincide
```

**Así que la comparación byte a byte no sirve**, y la técnica de este dominio es de tres niveles y merece
verla porque es un buen modelo:

**Nivel 1 — pruebas de regresión con tolerancia:**

```text
Caso pequeño, resultado guardado, y comparación con tolerancia RELATIVA
justificada por el análisis del error (clase 140), no por lo que hizo falta.
```

**Nivel 2 — magnitudes conservadas:**

```fortran
! La masa total, la energía y el momento DEBEN conservarse
if (abs(masa_final - masa_inicial) / masa_inicial > 1e-12_dp) error stop
```

**Esas comprobaciones no dependen del valor exacto**, así que **son robustas frente al compilador y al
paralelismo** — y detectan la mayoría de los errores reales.

**Nivel 3 — soluciones analíticas:**

```text
Para unos pocos casos existe la solución exacta (una onda plana, un flujo laminar).
Comparar contra ella verifica el MÉTODO, no solo la ausencia de cambios.
```

**Y la diferencia entre el nivel 1 y el nivel 3 es la de esta clase**: **el nivel 1 detecta que algo
cambió; el nivel 3 detecta que algo está mal**.

Y merece cerrar con la práctica que este dominio ha adoptado y que es la primera regla del cierre: **la
pirámide de casos**.

```text
En cada cambio:      casos de segundos, con 2 procesos
Cada noche:           casos de minutos, con varias combinaciones
Antes de publicar:     el caso de producción, en el clúster (clase 147)
```

**Y lo importante es que el nivel de arriba exista y se ejecute alguna vez**, porque **es el único que
prueba lo que de verdad se usa** — y muchos proyectos se quedan solo en el primero.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure E2e is
   A, B, Esperado : Integer;
begin
   Get (A);
   Get (B);
   Get (Esperado);

   if A + B = Esperado then
      Put_Line ("e2e=pasa");
   else
      Put_Line ("e2e=falla");
   end if;
end E2e;
```

**Ada y las pruebas de extremo a extremo.** En los dominios de Ada, esta clase tiene un nombre formal y un
peso enorme: **la verificación del sistema integrado**.

```text
Niveles de prueba en un proyecto certificado:
  1. Unitaria         → cada subprograma, con cobertura MC/DC (clase 139)
  2. Integración      → los componentes entre sí
  3. Hardware-software → el software sobre el hardware REAL
  4. Sistema          → el equipo completo, en banco de pruebas
  5. Y vuelo o campo   → el sistema en su entorno
```

**Y cada nivel tiene sus requisitos trazados** (clase 166): **cada requisito de alto nivel se verifica en
el nivel que le corresponde**, y una herramienta comprueba que no falte ninguno.

Y este dominio aporta a esta clase la técnica que hace posible probar lo que no se puede ejecutar de
verdad, y merece explicarla: **la prueba con hardware simulado en el bucle**.

```text
El sistema real ejecuta su software, y en lugar de sensores y actuadores
tiene conectado un SIMULADOR que:
  - le da lecturas de sensor como si volara
  - recibe sus órdenes de actuador
  - y simula la física del vehículo en tiempo real
```

**Y así se prueban situaciones que no se pueden provocar de verdad**: un fallo de motor, una ráfaga
extrema, un sensor que miente.

Es la versión física de los objetos simulados de la clase 139, y su valor es el mismo: **poder ejercitar
los caminos de error**.

Y merece señalar la propiedad que la tercera regla del cierre pide y que este mundo consigue mejor que
nadie: **el determinismo**.

```text
Con Ravenscar (clase 146) y sin reserva dinámica,
el sistema es determinista: la misma entrada da la misma secuencia de ejecución.

Y eso hace que una prueba que falla se pueda REPRODUCIR.
```

**Una prueba de extremo a extremo reproducible es una herramienta; una intermitente es un impuesto** — y
la diferencia, en gran parte, viene de las decisiones de diseño de la clase 135, no de la prueba.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program E2e;
{$MODE OBJFPC}{$H+}

var
  A, B, Esperado: Integer;

begin
  Read(A, B, Esperado);

  if A + B = Esperado then
    WriteLn('e2e=pasa')
  else
    WriteLn('e2e=falla');
end.
```

**Pascal y las pruebas de extremo a extremo.** El ecosistema Delphi tiene el problema de esta clase en su
forma clásica: **probar una aplicación de escritorio con interfaz gráfica**.

```pascal
{ Automatización de la interfaz: TestComplete, Ranorex, o la API de Windows }
FindWindow('TForm1', 'Mi aplicación');
SendMessage(Handle, WM_COMMAND, ...);
```

**Y merece decir con franqueza que esas pruebas son las más frágiles que existen**: dependen de
posiciones, de nombres de control, de la velocidad de la máquina y del tema visual.

Y la lección de esta clase, que vale para cualquier interfaz gráfica o web, es la primera regla del
cierre: **pocas y bien elegidas**.

```text
✗ Probar cada formulario y cada validación por la interfaz.
   → miles de pruebas lentas y frágiles.

✓ Probar la LÓGICA por debajo (clase 139),
   y por la interfaz solo unos pocos caminos completos:
   "entrar, crear un pedido, cobrarlo, imprimir el ticket".
```

**Y para que eso sea posible, la lógica tiene que estar separada de la interfaz** (clase 149) — que es,
otra vez, buena arquitectura y comprobabilidad siendo lo mismo.

Y el ecosistema tiene una técnica que merece nombrarse y que resuelve la segunda regla del cierre: **la
base de datos en memoria o en fichero temporal**.

```pascal
{ Cada prueba arranca con su propia base, creada desde un guion }
FDConnection.Params.Database := TempDir + 'prueba_' + GUID + '.fdb';
EjecutarGuion('esquema.sql');
EjecutarGuion('datos_de_prueba.sql');
```

**Una base por prueba, creada y destruida**, elimina de golpe las pruebas intermitentes por estado
compartido — y con SQLite o Firebird embebido cuesta milisegundos.

Es la aplicación más directa de "datos propios y desechables", y merece señalar que **la mayoría de los
equipos que sufren pruebas intermitentes no han probado esto**.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let ((a (read))
      (b (read))
      (esperado (read)))
  (format t "e2e=~A~%" (if (= (+ a b) esperado) "pasa" "falla")))
```

**Lisp y las pruebas de extremo a extremo.** Lisp aporta a esta clase una técnica que su modelo hace fácil
y que merece destacarse porque ataca la fragilidad del cierre: **grabar y reproducir**.

```lisp
;; Envolver una función para GRABAR sus llamadas y sus resultados en producción
(defun grabar (nombre fn)
  (lambda (&rest args)
    (let ((r (apply fn args)))
      (push (list nombre args r) *grabacion*)
      r)))

;; Y luego reproducir: la misma secuencia, sin el sistema externo
```

**Grabar las interacciones reales con los sistemas externos y reproducirlas** convierte una prueba de
extremo a extremo —lenta, dependiente de la red y frágil— **en una prueba rápida y determinista**.

Es la técnica que en otros ecosistemas se llama *VCR* o *cassettes*, y que Lisp permite montar en veinte
líneas porque **redefinir una función es una operación normal** (clase 139).

Y la advertencia que va con ella y merece decirse: **una prueba con grabación deja de detectar cambios en
el sistema externo**.

**Así que hacen falta las dos**: la mayoría con grabación —rápidas y estables— y **unas pocas contra el
sistema real**, ejecutadas menos veces (clase 147).

Y el ecosistema para esta clase:

```lisp
(asdf:test-system "mi-sistema")
(uiop:run-program (list "./servicio" "--puerto" "8080") :wait nil)
(dex:get "http://localhost:8080/pedidos/1")
```

**`uiop:run-program` con `:wait nil` lanza el sistema en segundo plano**, y el guion de prueba puede
esperar, ejercitar y parar — que es el patrón de la clase 165.

Y merece cerrar con la aportación de Lisp que la Parte 8 hace posible y que en esta clase es muy valiosa:
**cuando una prueba de extremo a extremo falla, se puede entrar**.

```lisp
;; La prueba falla → el depurador se abre CON el estado vivo (clase 141)
;; y se puede inspeccionar el sistema entero en el punto del fallo
```

**Diagnosticar un fallo de una prueba de sistema sin reproducirlo a mano** es lo que más tiempo ahorra en
esta clase, y es exactamente lo que un depurador sobre el proceso vivo permite.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea
lassign [string trim $linea] a b esperado

puts "e2e=[expr {$a + $b == $esperado ? {pasa} : {falla}}]"
```

**Tcl y las pruebas de extremo a extremo.** Este es **el componente de Tcl por excelencia** en esta parte
(clase 165), y merece juntar aquí la receta completa con las tres reglas del cierre.

```tcl
package require tcltest
namespace import ::tcltest::*

# 1. Datos propios y desechables (regla 2)
proc arrancarSistema {} {
    set ::dir [file tempdir]
    exec sqlite3 $::dir/prueba.db < esquema.sql
    set ::api [exec ./api --db $::dir/prueba.db --puerto 0 --puertofile $::dir/p &]
    esperarFichero $::dir/p -timeout 10          ;# 2. esperar EVENTOS (regla 3)
    set ::puerto [leerFichero $::dir/p]
}

proc pararSistema {} {
    exec kill $::api
    file delete -force $::dir
}

test flujo-completo-1.1 {crear un pedido y cobrarlo} -setup {
    arrancarSistema
} -body {
    set id [crearPedido $::puerto {items {A1 2}}]
    cobrar $::puerto $id
    dict get [consultar $::puerto $id] estado
} -cleanup {
    pararSistema
} -result {cobrado}

cleanupTests
```

**Y tres detalles de ese guion merecen destacarse porque son las decisiones que hacen la prueba
sostenible:**

**`--puerto 0` y un fichero con el puerto real.** **Pedir un puerto fijo es la causa clásica de pruebas
que fallan al ejecutarse en paralelo** (clase 147): **que el sistema elija y lo publique** permite
ejecutar veinte a la vez.

**`esperarFichero` en lugar de dormir** (clase 171). **Nunca `after 3000`**.

**Y `-cleanup` que se ejecuta siempre**, incluso si el cuerpo falla — que es la propiedad que evita que
una prueba rota deje procesos y directorios por todas partes.

Y Tcl aporta lo que la clase 147 ya señaló y que aquí es la herramienta para lo que no tiene API:
**Expect**.

**Probar de extremo a extremo una aplicación de terminal, un instalador o un equipo de red** es algo que
solo Expect hace bien, y sigue siendo la respuesta treinta y cinco años después.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;
my ($a1, $b1, $esperado) = split ' ', $linea;

print "e2e=", ($a1 + $b1 == $esperado ? 'pasa' : 'falla'), "\n";
```

**Perl y las pruebas de extremo a extremo.** Perl tiene el ecosistema más completo de esta página para
esta clase, y merece verlo porque cubre las tres reglas del cierre:

```perl
use Test::More;
use Test::TCP;              # ← puerto libre y arranque de servidor
use Test::PostgreSQL;        # ← ¡una base de datos temporal por prueba!
use Test::Deep;               # comparación con comodines (clase 140)

my $pg = Test::PostgreSQL->new;               # arranca su propio PostgreSQL
test_tcp(
    server => sub {
        my $puerto = shift;
        exec './api', '--dsn', $pg->dsn, '--puerto', $puerto;
    },
    client => sub {
        my $puerto = shift;
        my $r = pedir("http://127.0.0.1:$puerto/pedidos", {items => 2});
        cmp_deeply($r, {
            id     => ignore(),                # cambia en cada ejecución
            creado => re(qr/^\d{4}-/),
            total  => num(24.20, 0.01),
        }, 'el pedido creado cumple el contrato');
    },
);
done_testing();
```

**`Test::PostgreSQL` merece destacarse** porque resuelve la segunda regla del cierre de la forma más
limpia: **arranca una instancia de PostgreSQL propia, en un directorio temporal, y la destruye al
terminar**.

**Cada prueba tiene su base de datos entera, aislada**, y **se pueden ejecutar en paralelo sin
coordinación**.

Es una idea excelente y sorprendentemente poco usada: **el coste de arrancar una base vacía es de
segundos, y el de depurar pruebas que se pisan es de días**.

**Y `Test::TCP`** resuelve el problema del puerto igual que Tcl en esta página: **busca uno libre y se lo
pasa al servidor**.

Y merece cerrar con la observación que la clase 147 anticipó y que en esta clase es la regla que sostiene
todo: **una prueba intermitente hay que arreglarla o borrarla**.

```perl
# ✗ lo que NO hay que hacer, y todo el mundo acaba haciendo
$ENV{REINTENTOS} = 3;
```

**Reintentar hasta que pase convierte la suite en un generador de ruido**, y a partir de ahí **nadie mira
el rojo** — que es exactamente lo que la integración continua existía para evitar.

Y la causa suele ser una de tres: **espera por tiempo, estado compartido, o dependencia del orden**. Las
tres tienen solución conocida, y ninguna es el reintento.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>

int main() {
    long long a{}, b{}, esperado{};
    if (!(std::cin >> a >> b >> esperado)) return 1;

    std::cout << "e2e=" << (a + b == esperado ? "pasa" : "falla") << '\n';
    return 0;
}
```

**C++ y las pruebas de extremo a extremo.** C++ aporta a esta clase una técnica que la clase 141 nombró y
que aquí es la respuesta al problema más difícil: **el fallo que solo ocurre a veces**.

```bash
rr record ./sistema_completo --caso 42
# ...falla una vez de cada cincuenta...
rr replay                       # ← la MISMA ejecución, exactamente
```

**`rr` graba una ejecución completa y la reproduce de forma determinista**, incluidas las condiciones de
carrera.

**Y eso convierte una prueba intermitente en un fallo reproducible** — que es la diferencia entre poder
arreglarlo y no poder.

Es la mejor herramienta que existe para la tensión del "por qué" de esta clase, y merece conocerse aunque
solo se use dos veces al año.

Y las otras técnicas de C++ para esta clase, ordenadas por lo que cazan:

| Técnica | Qué caza |
|---|---|
| **ThreadSanitizer en la prueba de sistema** | carreras que se manifiestan una vez de cada mil (clase 136) |
| **AddressSanitizer** | corrupción de memoria bajo carga real |
| **Fuzzing con `libFuzzer`** | entradas que nadie pensó |
| **Pruebas basadas en propiedades** | invariantes, con casos generados (clase 140) |
| **`rr`** | reproducir lo irreproducible |

**El fuzzing merece la mención** porque en un sistema que procesa entradas externas es la prueba de
extremo a extremo más rentable que existe:

```bash
./api_fuzzer corpus/ -max_total_time=3600
```

**Se generan millones de entradas aleatorias y mutadas, guiadas por cobertura**, y **cada caída se guarda
como caso de prueba reproducible**.

**Y encuentra cosas que ninguna persona escribiría**: cadenas vacías, números en los límites, secuencias
UTF-8 inválidas, anidamientos de mil niveles.

Y para el proyecto de esta parte, la recomendación concreta es la primera regla del cierre aplicada con
criterio: **pocas pruebas de extremo a extremo, y en cambio fuzzing continuo sobre las fronteras** —
porque es donde llegan los datos hostiles (clase 153) y donde una persona escribiendo casos nunca va a
competir con una máquina.

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

dcl-pi E2E;
  a        int(10) const;
  b        int(10) const;
  esperado int(10) const;
end-pi;

if a + b = esperado;
  dsply 'e2e=pasa';
else;
  dsply 'e2e=falla';
endif;

*inlr = *on;
return;
```

**RPG y las pruebas de extremo a extremo.** IBM i tiene un mecanismo que resuelve la segunda regla del
cierre mejor que cualquier otra plataforma de esta página, y ya apareció en la clase 139: **la lista de
bibliotecas**.

```text
CRTLIB PRUEBA$$$
CRTDUPOBJ OBJ(*ALL) FROMLIB(PRODDATOS) OBJTYPE(*FILE) TOLIB(PRUEBA$$$) DATA(*YES)
CHGLIBL LIBL(PRUEBA$$$ MIAPP QGPL)
   ... ejecutar las pruebas ...
DLTLIB PRUEBA$$$
```

**Copiar el esquema y los datos a una biblioteca temporal y redirigir el trabajo hacia ella** da a cada
ejecución de pruebas **su propia copia completa de la base de datos**, sin tocar nada.

**Y es una operación del sistema, no de la aplicación**: los programas **no saben** que están usando otras
tablas.

Es inyección de dependencias a nivel de sistema operativo (clase 139), y resuelve de raíz la fuente número
uno de pruebas intermitentes.

Y las otras dos reglas del cierre tienen respuesta en la plataforma:

**Los datos deterministas**: `CRTDUPOBJ` desde un juego de datos versionado, y **el diario** (clase 172)
permite volver al estado inicial con `RMVJRNCHG` en lugar de recrear.

**Y el diagnóstico**: **si una prueba falla, el registro del trabajo tiene todo** (clase 142) — cada
mensaje, con su programa y su número de sentencia.

Y merece cerrar con la práctica de este mundo que la primera regla del cierre recomienda y que aquí es
natural: **probar por la interfaz de programa, no por la pantalla**.

```rpgle
// La prueba llama al procedimiento del programa de servicio,
// no simula pulsaciones en una pantalla 5250
aEqual(120.50 : calcularTotal(pedidoDePrueba) : 'total con IVA');
```

**Y para el flujo completo, un guion CL que encadena los programas** (clase 171) y compara los ficheros
resultantes con los esperados — que es, otra vez, la técnica de COBOL de esta página.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 e2e: procedure options(main);

    declare (a, b, esperado) fixed binary(31);

    get list (a, b, esperado);

    if a + b = esperado then
       put skip list ('e2e=pasa');
    else
       put skip list ('e2e=falla');

 end e2e;
```

**PL/I y las pruebas de extremo a extremo.** PL/I aporta a esta clase la versión más ambiciosa que existe,
y la clase 140 ya la nombró: **la ejecución en paralelo**.

```text
Durante SEIS MESES:
  - el sistema viejo y el nuevo procesan las MISMAS entradas reales
  - solo el viejo tiene efectos
  - y un proceso compara TODAS las salidas, todos los días
  - cada discrepancia se investiga y se documenta
```

**Es una prueba de extremo a extremo con datos de producción reales, ejecutada millones de veces.**

Y merece explicar por qué se hace así y no con casos escritos, porque el argumento es fuerte: **nadie
puede escribir los casos que un sistema de treinta años ha visto**.

```text
Las discrepancias que aparecen son casi siempre:
  - clientes con configuraciones que ya no se dan de alta
  - contratos con excepciones aprobadas hace veinte años
  - casos que el sistema viejo maneja mal y de los que alguien depende
```

**Y ninguno de esos estaría en un juego de casos de prueba**, porque nadie sabe que existen.

Es la lección más importante de esta clase para cualquier reescritura: **los datos de producción son la
única especificación completa del sistema actual**.

Y la técnica que lo hace posible y que merece nombrarse: **la captura y reproducción de entradas**.

```text
Se instrumenta el sistema viejo para guardar cada entrada
—cada mensaje, cada fichero, cada petición—
y se reproduce contra el nuevo, fuera de línea.
```

**Y eso permite ejecutar seis meses de tráfico real en unas horas**, cuantas veces haga falta.

Y es la aportación de esta columna a la primera regla del cierre, con un matiz: **aquí las pruebas no son
pocas y bien elegidas — son todas las que ocurrieron**.

Y la razón es que **el objetivo no es comprobar que el sistema funciona, sino que es equivalente** (clase
140), y para eso **la cobertura de casos reales vale más que cualquier diseño de pruebas**.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
E2E ; Prueba de extremo a extremo -- clase 173
 read linea
 new a, b, esperado
 set a = $piece(linea, " ", 1)
 set b = $piece(linea, " ", 2)
 set esperado = $piece(linea, " ", 3)
 write "e2e=", $select(a + b = esperado : "pasa", 1 : "falla"), !
 quit
```

**M y las pruebas de extremo a extremo.** M tiene, para esta clase, una capacidad que su modelo de datos
hace posible y que es más fuerte que comparar salidas: **comparar el estado de la base**.

```mumps
 ; 1. copiar el estado inicial a un espacio temporal
 merge ^||INICIAL = ^PACIENTE(dfn)

 ; 2. ejecutar el flujo completo
 do procesarAlta^ADT(dfn, datos)

 ; 3. y comparar el resultado con el esperado
 write $$comparar^UTIL($name(^PACIENTE(dfn)), $name(^ESPERADO(caso)))
```

**`merge` copia un subárbol entero de una global a otra en una operación** — que es la forma de M de
capturar un estado.

Y merece explicar por qué comparar el estado es mejor que comparar la salida, porque es la lección de esta
explicación y ya apareció en la clase 140:

```text
Comparar la SALIDA detecta lo que el sistema dijo.
Comparar el ESTADO detecta lo que el sistema HIZO.

Y un fallo típico —actualizar mal un índice, dejar un registro huérfano,
no borrar algo temporal— no se ve en la salida y sí en el estado.
```

**Y esa es la clase de fallo que aparece meses después**, cuando alguien consulta por ese índice.

Y las dos reglas del cierre que este dominio resuelve bien:

**Los datos propios**: `^||` da globals temporales privadas del proceso (clase 139), y **las
implementaciones modernas permiten regiones de base de datos desechables**.

**Y el determinismo**: la trampa clásica de este mundo es **la fecha**.

```mumps
 ; ✗ una prueba que usa DT (la fecha de hoy) falla el 1 de enero
 if $$edad^UTIL(fechaNac, DT) > 65 ...

 ; ✓ la fecha se INYECTA
 if $$edad^UTIL(fechaNac, fechaReferencia) > 65 ...
```

**Depender del reloj es la segunda causa de pruebas intermitentes**, después del estado compartido — y en
un dominio donde casi todo se calcula respecto a hoy, es un problema constante.

**Y la defensa es de diseño**: **el tiempo es un parámetro, no una variable global** — que es una de las
recomendaciones más rentables de toda esta parte del curso.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| linea partes a b esperado |

linea := stdin nextLine trimBoth.
partes := linea substrings: ' '.

a := (partes at: 1) asNumber.
b := (partes at: 2) asNumber.
esperado := (partes at: 3) asNumber.

Transcript
    show: 'e2e=', (a + b = esperado ifTrue: [ 'pasa' ] ifFalse: [ 'falla' ]);
    cr.
```

**Smalltalk y las pruebas de extremo a extremo.** Smalltalk, que inventó las pruebas unitarias (clase
139), aporta a esta clase dos capacidades que vienen de su modelo.

**La primera: la imagen como estado de prueba.**

```smalltalk
"Preparar el sistema en un estado concreto y GUARDARLO"
self cargarDatosDePrueba.
Smalltalk snapshot: true andQuit: true.
```

**Una imagen con los datos ya cargados arranca en el estado exacto que la prueba necesita** — lo que
resuelve la segunda regla del cierre sin base de datos temporal ni guiones de carga.

Es la misma idea que una instantánea de contenedor (clase 174), disponible desde 1980.

**Y la segunda: el fallo se puede examinar entero.**

```smalltalk
[ self ejecutarFlujoCompleto ] on: Error do: [ :e |
    "Guardar el CONTEXTO del error para abrirlo después (clase 141)"
    FLSerializer serialize: e signalerContext toFileNamed: 'fallo.fuel' ]
```

**Y ese fichero se abre en el depurador en otra máquina**, con la pila viva y los objetos.

**Es la respuesta al problema más caro de esta clase**: una prueba de sistema que falla en la integración
continua y no se reproduce en local. Aquí **el fallo viaja**.

Y merece cerrar esta clase con la observación que Smalltalk permite hacer y que resume la parte: **las
pruebas de extremo a extremo son caras porque el sistema no se deja preguntar**.

```text
Si el sistema puede decir en qué estado está,
si el fallo se puede capturar entero,
y si el entorno se puede recrear exactamente,
entonces la prueba de extremo a extremo es barata y estable.

Y si no, se compensa con esperas, reintentos y capturas de pantalla.
```

**La fragilidad de estas pruebas es, casi siempre, un síntoma del sistema y no de la prueba** — y las
propiedades que las abaratan son las mismas que esta parte del curso viene defendiendo: **fronteras
claras, estado inspeccionable, entorno reproducible y tiempo inyectado**.

---

## Y de vuelta a la clase

Lo transferible: **una prueba de extremo a extremo comprueba lo que de verdad importa y falla por lo que
no**. De ahí las tres reglas que la hacen sostenible: **pocas y bien elegidas** —cubrir los caminos
críticos, no todos los casos, que ya están cubiertos abajo (clase 139)—; **con datos propios y
desechables**, porque una prueba que depende del estado que dejó otra falla de forma intermitente; y
**esperando por eventos, no por tiempos** (clase 171), que es la causa número uno de pruebas
intermitentes. Y la regla que sostiene todo: **una prueba que falla a veces y se reintenta hasta que pasa
ya no prueba nada** — y enseña al equipo a ignorar el rojo.

⏮️ [Volver a la clase 173](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
