# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 166

> [⬅️ Volver a la clase 166](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Comprobar que dos versiones de contrato encajan. Es lo primero que hace cualquier sistema distribuido al
arrancar, y esta clase trata de la decisión que lo precede: **qué hace cada componente y qué se promete
a los demás**. Y aquí estos lenguajes aportan algo que ningún diagrama de arquitectura da: **la
evidencia de qué contratos aguantan treinta años** — y la respuesta es siempre la misma clase de
contrato: **el pequeño, el explícito y el que solo crece**.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es el **reparto de responsabilidades**, y estos lenguajes lo enseñan porque **tienen
> contratos con décadas de historia**: la COMMAREA de CICS, la firma de un programa de servicio, la
> especificación de un paquete Ada, el formato de un registro, el diccionario de FileMan. Y todos
> demuestran lo mismo que la clase 160 concluía: **lo que decide si un contrato sobrevive no es la
> tecnología, sino si hay una regla escrita sobre qué se puede cambiar**.
>
> Y aparece la pregunta de diseño: **¿dónde se pone la frontera?** Porque una mal puesta obliga a cambiar
> dos componentes cada vez.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: una línea `a b` (los valores de contrato de cada componente) → stdout: `contrato=<compatible|incompatible>`
- **Regla:** `compatible si a == b`

| stdin | esperado |
|---|---|
| `5 5` | `contrato=compatible` |
| `5 6` | `contrato=incompatible` |
| `0 0` | `contrato=compatible` |

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
PROGRAM-ID. CONTRAT.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(40).
01  C-A     PIC X(10).
01  C-B     PIC X(10).
01  A       PIC 9(4) COMP.
01  B       PIC 9(4) COMP.

PROCEDURE DIVISION.
    ACCEPT LINEA
    UNSTRING LINEA DELIMITED BY ALL SPACES
        INTO C-A C-B
    END-UNSTRING

    COMPUTE A = FUNCTION NUMVAL(C-A)
    COMPUTE B = FUNCTION NUMVAL(C-B)

    IF A = B
        DISPLAY "contrato=compatible"
    ELSE
        DISPLAY "contrato=incompatible"
    END-IF
    STOP RUN.
```

**Cómo se diseñan las responsabilidades en COBOL.** El mundo del lote tiene un principio de diseño que
merece nombrarse porque es el cierre de esta clase aplicado con rigor: **un paso, una responsabilidad**
(clase 149).

```jcl
//PASO1 EXEC PGM=EXTRAER     <-- solo extrae
//PASO2 EXEC PGM=SORT         <-- solo ordena
//PASO3 EXEC PGM=VALIDAR       <-- solo valida
//PASO4 EXEC PGM=CALCULAR       <-- solo calcula
//PASO5 EXEC PGM=INFORMAR        <-- solo informa
```

**Y el contrato entre pasos es el formato del fichero intermedio**, declarado en un copybook (clase 159).

Y merece señalar lo que ese diseño consigue y que es el criterio del cierre: **la mayoría de los cambios
tocan un solo paso**.

```text
Cambia una regla de validación   →  solo PASO3
Cambia el formato del informe     →  solo PASO5
Cambia el origen de los datos      →  solo PASO1
```

**Y cuando un cambio toca dos pasos, casi siempre es porque cambió el contrato** — y eso se ve, se
declara y se revisa.

Y el diseño interno del programa sigue el mismo principio, con la separación que la clase 149
recomendaba:

```cobol
      *> ✗ un párrafo que hace de todo
       PROCESAR.
           EXEC CICS RECEIVE MAP(...) END-EXEC
           EXEC SQL SELECT ... END-EXEC
           COMPUTE ...
           EXEC CICS SEND MAP(...) END-EXEC

      *> ✓ separado, y el cálculo es un programa llamable y PROBABLE
       PROCESAR.
           PERFORM LEER-PANTALLA
           PERFORM LEER-DATOS
           CALL 'CALCULO' USING WS-ENTRADA WS-SALIDA
           PERFORM ESCRIBIR-PANTALLA
```

**Y la diferencia práctica es la de la clase 139**: la segunda versión **se puede probar sin CICS y sin
base de datos**.

Es el criterio del cierre visto desde dentro: **la frontera correcta es también la que permite probar
cada parte por separado** — y las dos propiedades suelen coincidir, porque las dos miden lo mismo: **si
las responsabilidades están de verdad separadas**.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program contrat
   implicit none
   integer :: a, b

   read(*, *) a, b

   if (a == b) then
      write(*, '(A)') 'contrato=compatible'
   else
      write(*, '(A)') 'contrato=incompatible'
   end if
end program contrat
```

**Cómo se diseñan las responsabilidades en Fortran.** El cálculo científico tiene un reparto de
responsabilidades con nombre propio y muy bien pensado, y merece verlo porque es un ejemplo de manual
(clase 149):

```text
Aplicación         →  qué problema físico se resuelve
Discretización      →  cómo se convierte en un sistema de ecuaciones
Solver               →  cómo se resuelve el sistema
Álgebra lineal        →  BLAS/LAPACK
Comunicación           →  MPI
```

**Y el contrato entre capas es una interfaz de subrutina con argumentos declarados**, con `intent`
(clase 146) y con la semántica documentada (clase 160).

Y merece señalar el criterio del cierre aplicado aquí: **cambiar de solver no debería obligar a cambiar
la física**.

```fortran
! ✓ el solver es un argumento, no una dependencia fija
call resolver(matriz, rhs, solucion, metodo=gmres, precond=ilu)
```

**Y ese diseño es la razón de que PETSc y Trilinos existan**: son marcos que permiten **cambiar el
método numérico sin tocar el modelo**, lo que en investigación es exactamente el cambio más frecuente.

Y hay un contrato específico de este dominio que esta clase debe nombrar porque casi nunca se declara y
casi siempre se incumple: **las unidades**.

```fortran
! ✗ ¿en metros o en kilómetros? ¿kelvin o celsius? ¿pascales o bares?
call calcular(presion, temperatura, altura)
```

**El fracaso del Mars Climate Orbiter en 1999 fue exactamente eso**: **un componente entregaba impulso en
libras-fuerza por segundo y el otro lo esperaba en newtons por segundo**. Se perdió la sonda.

Y las defensas que este dominio ha desarrollado merecen conocerse porque son transferibles:

| Defensa | Cómo |
|---|---|
| **Tipos con unidad** | módulos que definen `type(metros)` y prohíben mezclar |
| **Convenciones CF** | las unidades **en los metadatos del fichero** (clase 160) |
| **Documentar en la interfaz** | el comentario de cabecera de LAPACK como modelo |
| **Y comprobar en las fronteras** | validar rangos al entrar |

**La primera es la única que lo hace imposible**, y es lo que Ada consigue con sus tipos derivados
(clase 124) — un caso claro de que **el contrato más fuerte es el que el compilador comprueba**.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Contrat is
   A, B : Integer;
begin
   Get (A);
   Get (B);

   if A = B then
      Put_Line ("contrato=compatible");
   else
      Put_Line ("contrato=incompatible");
   end if;
end Contrat;
```

**Cómo se diseñan las responsabilidades en Ada.** Ada permite expresar el diseño de esta clase **en el
lenguaje**, y con una precisión que ningún otro de esta página iguala (clases 149 y 160).

```ada
package Motor is                          --  QUÉ hace este componente
   type Estado is (Parado, Arrancando, En_Marcha, Fallo);

   procedure Arrancar
     with Pre  => Leer_Estado = Parado,           --  QUÉ exige
          Post => Leer_Estado = Arrancando;        --  QUÉ garantiza

   function Leer_Estado return Estado;

private
   ...                                     --  lo que NO es contrato
end Motor;
```

**Y las cuatro piezas del diseño están ahí**: la responsabilidad, la interfaz, el contrato comprobable y
lo que queda oculto.

Y Ada añade la comprobación de la segunda regla del cierre —**interfaces estrechas**— con un mecanismo
del lenguaje que la clase 149 nombró y que aquí es central: **los paquetes hijos privados**.

```ada
private package Motor.Interno is ...      --  invisible fuera del árbol Motor
```

**El compilador impide que otro componente dependa de lo interno**, así que **la frontera no es una
convención: es una regla**.

Y merece explicar el patrón de diseño que estos sistemas usan y que responde al criterio del cierre:
**la arquitectura por capas con dependencias en un solo sentido**.

```text
Aplicación   →  depende de  →  Servicios  →  depende de  →  Dominio
                                                              ↑
Infraestructura (controladores, red, disco)  →  depende de ──┘
```

**Y el dominio no depende de nada.** Es la arquitectura hexagonal, y en Ada se puede **verificar con los
ficheros de proyecto** (clase 149): `gprbuild` se niega a compilar si alguien importa hacia el lado
equivocado.

Y merece cerrar con lo que la industria crítica añade y que esta parte del curso debería recoger: **la
trazabilidad del diseño**.

```text
Requisito de alto nivel  →  requisito de bajo nivel  →  paquete  →  prueba
```

**Cada componente responde a requisitos identificados**, y una herramienta comprueba que no falte ninguno
(clase 147).

Es pesado, y resuelve el problema que casi ningún sistema resuelve: **saber por qué existe cada
componente** — que es la primera pregunta que se hace quien llega dentro de diez años.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Contrat;
{$MODE OBJFPC}{$H+}

var
  A, B: Integer;

begin
  Read(A, B);

  if A = B then
    WriteLn('contrato=compatible')
  else
    WriteLn('contrato=incompatible');
end.
```

**Cómo se diseñan las responsabilidades en Pascal.** El ecosistema Delphi tiene una unidad de diseño muy
clara —**la `unit`, con su `interface` y su `implementation`** (clase 143)— y esta clase es el sitio para
señalar el error de diseño más común de ese mundo y su solución.

**El error: la dependencia circular entre unidades.**

```pascal
unit Cliente;
interface
uses Pedido;        { Cliente necesita Pedido }

unit Pedido;
interface
uses Cliente;       { ...y Pedido necesita Cliente. ERROR }
```

**Free Pascal y Delphi lo rechazan en la sección `interface`** —hay que moverlo a `implementation`, donde
sí se permite—.

Y esa restricción, que parece una molestia, **es exactamente la primera regla del cierre de esta clase
impuesta por el compilador**: **obliga a pensar la dirección de las dependencias**.

Y las soluciones son las de siempre y merecen enumerarse porque son transferibles:

| Solución | Cómo |
|---|---|
| **Extraer lo común a una tercera unidad** | `Tipos`, de la que dependen las dos |
| **Invertir la dependencia con una interfaz** | `IRepositorioCliente` en la unidad del dominio |
| **Mover el `uses` a `implementation`** | funciona, y **esconde el problema** |
| **Eventos en lugar de llamadas** | el modelo de Delphi (clase 120) |

**La segunda es la correcta y merece el ejemplo**, porque es la inversión de dependencias en su forma más
simple:

```pascal
unit Dominio;
interface
type
  IRepositorio = interface
    function Buscar(Id: Integer): TCliente;
  end;
  TServicio = class
    constructor Create(ARepo: IRepositorio);    { recibe la dependencia }
  end;

unit Infraestructura;         { ← esta depende de Dominio, no al revés }
interface
uses Dominio;
type
  TRepositorioSQL = class(TInterfacedObject, IRepositorio) ... end;
```

**Y el resultado es el criterio del cierre**: cambiar de base de datos **toca una unidad**; cambiar una
regla de negocio, **toca otra**.

Y merece señalar el beneficio secundario que esta parte del curso ya conoce: **con la interfaz, el
servicio se puede probar con un repositorio simulado** (clase 139) — otra vez, **buena separación y
comprobabilidad son la misma propiedad**.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let ((a (read))
      (b (read)))
  (format t "contrato=~A~%" (if (= a b) "compatible" "incompatible")))
```

**Cómo se diseñan las responsabilidades en Common Lisp.** Lisp tiene una unidad de diseño que esta clase
debe destacar porque su semántica es distinta de la de casi todos: **el paquete** (clase 087).

```lisp
(defpackage :mi-sistema.dominio
  (:use :cl)
  (:export #:pedido                 ; ← LO QUE SE EXPORTA es el contrato
           #:total
           #:añadir-linea))

(defpackage :mi-sistema.persistencia
  (:use :cl :mi-sistema.dominio)     ; ← depende del dominio
  (:export #:guardar #:cargar))
```

**Un paquete de Lisp exporta símbolos**, y **lo no exportado se puede seguir usando con `::`** — así que
la frontera es **una convención muy fuerte, no una barrera**.

Y merece decirlo con claridad porque define el estilo de este ecosistema: **`paquete::simbolo-interno`
funciona**, y la comunidad lo trata como **una señal de alarma explícita en el código**.

Es lo mismo que el `_privado` de Python: **una convención visible en el punto de uso**, que hace que
saltarse la frontera **quede escrito**.

Y Lisp aporta a esta clase una capacidad de diseño que ningún otro de esta página tiene igual y que la
clase 149 nombró: **las funciones genéricas separan el contrato de la implementación sin jerarquía**.

```lisp
(defgeneric calcular-precio (producto cliente)
  (:documentation "El precio final, ya con descuentos e impuestos."))

;; Y cualquier componente puede añadir métodos DESPUÉS,
;; sin tocar ni el genérico ni las clases existentes
(defmethod calcular-precio ((p producto-digital) (c cliente-ue)) ...)
```

**Eso es extensión sin modificación en su forma más pura** —el principio de abierto/cerrado— y **no
requiere haberlo previsto**.

Y el coste, que es la contrapartida constante de este curso: **cualquier componente puede añadir un
método a cualquier genérico**, así que **el comportamiento del sistema depende de qué se haya cargado**
(clase 150).

Es el mismo compromiso que la clase 164 resumía: **flexibilidad frente a poder razonar sobre el
conjunto** — y en un sistema con varios equipos, la segunda suele valer más.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea
lassign [string trim $linea] a b

puts "contrato=[expr {$a == $b ? {compatible} : {incompatible}}]"
```

**Cómo se diseñan las responsabilidades en Tcl.** Tcl tiene el espacio de nombres como unidad de diseño
(clase 086), y esta clase es el sitio para señalar cómo se define un contrato en un lenguaje donde **no
hay nada que lo imponga**.

```tcl
namespace eval ::pedidos {
    namespace export crear consultar anular      ;# ← el contrato
    variable cache                                 ;# interno, sin exportar

    proc crear {cliente items} { ... }
    proc _validar {items} { ... }                   ;# el guion bajo: convención
}

namespace import ::pedidos::*                      ;# solo lo exportado
```

**`namespace export` declara el contrato y `namespace import` lo respeta** — pero **nada impide llamar a
`::pedidos::_validar` directamente**.

Y esa es la situación de la mayoría de los lenguajes dinámicos, y merece plantear la pregunta de diseño
que trae: **si la frontera no se puede imponer, ¿cómo se sostiene?**

Y las tres respuestas que funcionan en la práctica y que esta parte del curso ya ha ido dando:

**Una, la revisión** (clase 146): una llamada a un símbolo interno de otro componente **es un hallazgo de
revisión**, y se rechaza.

**Dos, la comprobación automática**: un analizador que busque `::otro::_` en el código de un componente
**convierte la convención en una regla de la integración continua** (clase 147).

**Y tres, las pruebas**: si el contrato tiene pruebas y lo interno no, **cambiar lo interno no rompe
nada** — y quien dependía de ello se entera cuando falla.

Y Tcl aporta una capacidad de diseño propia que merece destacarse y que la clase 153 ya rozó: **el
intérprete seguro como frontera real**.

```tcl
set componente [interp create -safe]
$componente alias consultar ::pedidos::consultar    ;# SOLO esto
```

**Ahí la frontera sí es una barrera**: el componente de dentro **no puede llamar a nada que no se le haya
dado**.

Es el modelo de capacidades (clases 153 y 162) aplicado al diseño interno de un sistema, y es una idea que
merece considerarse cuando un componente ejecuta código de terceros o de menor confianza.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;
my ($a1, $b1) = split ' ', $linea;

print "contrato=", ($a1 == $b1 ? 'compatible' : 'incompatible'), "\n";
```

**Cómo se diseñan las responsabilidades en Perl.** Perl tiene el módulo como unidad, y **el contrato es
lo que se exporta**:

```perl
package MiSistema::Pedidos;
use strict; use warnings;
use Exporter 'import';

our @EXPORT_OK = qw(crear consultar anular);       # el contrato
our %EXPORT_TAGS = (todo => \@EXPORT_OK);

sub crear { ... }
sub _validar { ... }                                # convención: interno
```

**`@EXPORT_OK` en lugar de `@EXPORT`** es la práctica recomendada, y merece explicar por qué, porque es un
principio de diseño de esta clase: **`@EXPORT` mete símbolos en el espacio de quien usa el módulo sin que
lo pida**.

```perl
use MiSistema::Pedidos;              # con @EXPORT: llegan cosas sin pedirlas
use MiSistema::Pedidos qw(crear);     # con @EXPORT_OK: llega lo que se pide
```

**Y la segunda forma hace visible en el punto de uso qué se está importando** — que es exactamente la
segunda regla del cierre: **interfaces estrechas, y explícitas**.

Y Perl aporta a esta clase el mecanismo de diseño que la clase 149 destacó y que merece verse aquí como
herramienta de reparto de responsabilidades: **los roles de Moose**.

```perl
package Auditable;
use Moose::Role;
requires 'identificador';           # quien tome el rol DEBE tener esto
has historial => (is => 'ro', default => sub { [] });
sub registrar { ... }

package Pedido;
use Moose;
with 'Auditable', 'Serializable';    # componer capacidades
```

**Un rol es una responsabilidad que se compone**, y **`requires` declara qué necesita del anfitrión**.

Y su ventaja sobre la herencia para el diseño de esta clase merece subrayarse: **la herencia obliga a
elegir una jerarquía** —un pedido es *una cosa*— **y los roles permiten decir qué sabe hacer** —es
auditable, es serializable, es facturable—.

**Y eso encaja mejor con la primera regla del cierre**: **agrupar lo que cambia junto**. Las
capacidades cambian por razones distintas entre sí, así que **estar en piezas separadas y componibles es
exactamente lo que se quiere**.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>

int main() {
    int a{}, b{};
    if (!(std::cin >> a >> b)) return 1;

    std::cout << "contrato=" << (a == b ? "compatible" : "incompatible") << '\n';
    return 0;
}
```

**Cómo se diseñan las responsabilidades en C++.** C++ tiene una restricción de diseño que la clase 149
explicó y que en esta clase es decisiva: **las dependencias son físicas**.

```cpp
// El contrato: una cabecera con lo mínimo
// motor.hpp
class Configuracion;                     // declaración adelantada: NO incluye
class Motor {
public:
    explicit Motor(const Configuracion& c);
    ~Motor();
    Resultado procesar(std::span<const std::byte> datos);
private:
    struct Impl;
    std::unique_ptr<Impl> p_;            // pimpl: los detalles NO están aquí
};
```

**Y esa cabecera es el contrato completo del componente**: quien lo use **no compila nada de su
implementación**, y **cambiar lo privado no obliga a recompilar a nadie** (clase 149).

Y merece señalar el criterio del cierre de esta clase medido en C++, porque aquí es literal y visible:

```bash
# ¿Cuántos ficheros hay que recompilar al tocar esta cabecera?
grep -rl '#include "motor.hpp"' src/ | wc -l
```

**Si ese número es grande, la frontera está mal puesta.** Es una métrica objetiva del diseño, y no
existe en lenguajes con compilación por módulos.

Y C++20 añade la herramienta que ataca la raíz:

```cpp
export module motor;
export class Motor { ... };
```

**Un módulo declara explícitamente qué exporta**, y **lo no exportado es invisible incluso para el
enlazador**.

Es la segunda regla del cierre —**interfaces estrechas**— llevada al sistema de compilación, y su
adopción lenta (clase 143) es un buen recordatorio de que **cambiar el modelo de dependencias de un
ecosistema cuesta décadas**.

Y merece cerrar con la técnica de diseño que este lenguaje ha popularizado y que responde a la primera
regla: **la inyección de dependencias por plantilla**.

```cpp
template <class Reloj, class Registro>
class Servicio { ... };                  // sin coste en ejecución
```

**El componente no depende de un reloj ni de un registrador concretos**, lo que lo hace probable (clase
139) **sin pagar despacho dinámico** — a costa de que el tipo se propague, que es el compromiso que la
clase 151 señalaba.

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

dcl-pi CONTRAT;
  a int(10) const;
  b int(10) const;
end-pi;

if a = b;
  dsply 'contrato=compatible';
else;
  dsply 'contrato=incompatible';
endif;

*inlr = *on;
return;
```

**Cómo se diseñan las responsabilidades en RPG.** IBM i tiene la unidad de diseño más comprobada de esta
página, y esta clase es el sitio para verla como herramienta de arquitectura: **el programa de servicio**
(clases 143 y 160).

```text
Un programa de servicio agrupa procedimientos relacionados:
   PEDIDOS   →  crear, consultar, anular, listar
   CLIENTES   →  alta, baja, buscar, validarCredito
   FISCAL      →  calcularIVA, validarNIF
```

**Y el contrato es la lista de exportaciones, verificada por firma al activar** — la única de esta página
que el sistema comprueba solo.

Y merece explicar el criterio de agrupación que la primera regla del cierre pide, porque en esta
plataforma tiene una consecuencia técnica directa:

```text
Un cambio en CUALQUIER procedimiento exportado obliga a:
  - recompilar ese módulo
  - y volver a crear el programa de servicio

Y si cambia la LISTA de exportaciones, cambia la firma,
y todos los clientes dejan de arrancar (clase 143).
```

**Así que agrupar mal tiene coste inmediato y visible**: **un programa de servicio con cincuenta
procedimientos de tres dominios distintos cambia constantemente**, y cada cambio arrastra a todos sus
clientes.

Y la regla práctica que la plataforma enseña y que es transferible: **agrupar por razón de cambio, no por
similitud técnica**.

```text
✗ UTILIDADES  → todo lo que no sabemos dónde poner. Cambia siempre.
✓ FISCAL       → cambia cuando cambia la normativa fiscal. Una o dos veces al año.
✓ PEDIDOS       → cambia cuando cambia el proceso de pedidos.
```

**Ese es exactamente el principio de responsabilidad única bien enunciado**: no "hace una cosa" sino
**"tiene una única razón para cambiar"**.

Y esta plataforma lo hace evidente porque **el coste de equivocarse se paga en cada despliegue** — que es
la mejor forma de aprender un principio de diseño.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 contrat: procedure options(main);

    declare (a, b) fixed binary(31);

    get list (a, b);

    if a = b then
       put skip list ('contrato=compatible');
    else
       put skip list ('contrato=incompatible');

 end contrat;
```

**Cómo se diseñan las responsabilidades en PL/I.** PL/I tiene el procedimiento externo como unidad, y su
contrato es la declaración de entrada:

```pli
 declare calcular_prima entry (fixed decimal(11,2),   /* capital */
                               fixed binary(15),       /* edad */
                               char(2))                 /* tipo de póliza */
                        returns (fixed decimal(11,2))
                        external;
```

**Y ahí está una lección de diseño que merece destacarse y que la clase 166 quiere dejar clara: esa firma
no dice nada del significado.**

```text
¿El capital en euros o en céntimos?
¿La edad en años cumplidos o en años del seguro?
¿Qué valores admite el tipo de póliza?
¿Qué pasa si la edad es 0? ¿Y si es 200?
```

**Los tipos declaran la forma, no el contrato.**

Y las respuestas que esta página ha ido dando merecen ponerse juntas, porque son la escala completa:

| Nivel | Ejemplo |
|---|---|
| **Solo forma** | `fixed binary(15)` — PL/I, C, COBOL |
| **Forma + dominio** | `subtype Edad is Integer range 0 .. 130` — Ada (clase 124) |
| **+ precondiciones** | `with Pre => Capital > 0.0` — Ada (clase 118) |
| **+ demostración** | SPARK: se prueba para toda entrada |
| **+ pruebas de contrato** | el consumidor declara qué espera (clase 160) |
| **+ documentación del porqué** | lo que sobrevive al equipo (clase 154) |

**Y la mayoría de los sistemas se quedan en el primer nivel**, y compensan con documentación externa que
se desincroniza y con conocimiento en las personas.

Y merece señalar la práctica que el mundo del mainframe sí desarrolló para eso y que funciona: **el
copybook compartido con comentarios normativos**.

```pli
 /* TIPO DE PÓLIZA. Valores admitidos:                     */
 /*   'VI' vida individual   'VC' vida colectiva            */
 /*   'AC' accidentes        'SA' salud                     */
 /* Cualquier otro valor: condición ERROR. Ver norma 12/97. */
 declare tipo_poliza char(2);
```

**El contrato y su documentación, en el mismo fichero que las dos partes comparten** — que es la
propiedad que la clase 154 pedía y que casi ningún sistema moderno consigue mejor.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
CONTRAT ; Compatibilidad de contrato -- clase 166
 read linea
 new a, b
 set a = $piece(linea, " ", 1)
 set b = $piece(linea, " ", 2)
 write "contrato=", $select(a = b : "compatible", 1 : "incompatible"), !
 quit
```

**Cómo se diseñan las responsabilidades en M.** M tiene la unidad más pequeña y el contrato más débil de
esta página —**la rutina, sin declaración de interfaz**— y VistA lo compensó con las convenciones de la
clase 146:

```mumps
 do EN^PSOORDER            ; el punto de entrada estándar del paquete de farmacia
 set x = $$CALC^PSOUTIL(a, b)
```

**El prefijo de dos o tres letras es el componente, y las etiquetas convenidas son el contrato.**

Y esta clase es el sitio para señalar el problema de diseño de fondo de este ecosistema, porque es
instructivo y muy común fuera de M: **el acoplamiento por datos compartidos**.

```mumps
 ; El paquete A escribe:
 set ^PACIENTE(dfn, "TRATAMIENTO", n) = ...

 ; Y el paquete B lo lee DIRECTAMENTE:
 set t = $get(^PACIENTE(dfn, "TRATAMIENTO", n))
```

**Ahí no hay contrato: hay dos componentes acoplados a la estructura física de una global** (clase 159).

Y la consecuencia es la que el cierre de esta clase mide: **cualquier cambio en esa estructura toca los
dos** — y en VistA, con decenas de paquetes, puede tocar veinte.

Y la solución que este ecosistema construyó merece conocerse porque es la correcta: **el acceso por la
API de FileMan, nunca directamente a la global**.

```mumps
 do GETS^DIQ(2, dfn_",", ".01;.03", "", .resultado)   ; por NOMBRE de campo
```

**FileMan traduce del nombre lógico del campo a su posición física**, así que **el componente que lee no
depende de dónde está el dato**.

Es exactamente la separación entre interfaz e implementación de esta clase, conseguida con una capa de
metadatos (clase 149).

Y la disciplina del SAC (clase 146) lo formaliza: **acceder directamente a las globals de otro paquete
está prohibido**, y es uno de los puntos que la revisión comprueba.

Es una regla que funciona **porque hay una alternativa cómoda**. Cuando la alternativa correcta es más
molesta que saltarse la frontera, la frontera se salta — y esa es una lección de diseño más general que
M ilustra bien.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| linea partes a b |

linea := stdin nextLine trimBoth.
partes := linea substrings: ' '.

a := (partes at: 1) asNumber.
b := (partes at: 2) asNumber.

Transcript
    show: 'contrato=', (a = b ifTrue: [ 'compatible' ] ifFalse: [ 'incompatible' ]);
    cr.
```

**Cómo se diseñan las responsabilidades en Smalltalk.** Smalltalk lleva el diseño de esta clase a su forma
más pura, porque **la unidad es el objeto y el contrato es el conjunto de mensajes que entiende** (clase
160).

Y de esa comunidad salieron dos de las herramientas de diseño más usadas del mundo, y merece nombrarlas:

**Las tarjetas CRC** —*Class, Responsibility, Collaborator*—, inventadas por **Kent Beck y Ward
Cunningham en 1989** para enseñar diseño orientado a objetos:

```text
┌─────────────────────────────────────────┐
│ Pedido                                   │
├──────────────────────┬──────────────────┤
│ Responsabilidades     │ Colaboradores    │
│ - conocer sus líneas  │ Linea            │
│ - calcular su total   │ Cliente          │
│ - validarse            │ Tarifa           │
└──────────────────────┴──────────────────┘
```

**Una tarjeta de cartulina por clase**, con lo que hace y con quién habla — y **el tamaño de la tarjeta
es el límite**: si no cabe, la clase hace demasiado.

Es una restricción física convertida en criterio de diseño, y sigue siendo una de las mejores formas de
repartir responsabilidades en una pizarra con un equipo.

**Y los patrones de diseño** (clase 151), que salieron de la misma comunidad y en la misma década.

Y Smalltalk aporta a esta clase una técnica de diseño que su modelo hace natural: **descubrir el diseño
programando**.

```smalltalk
"Se escribe el código que se QUERRÍA poder escribir:"
pedido total.
"Y el depurador se abre en doesNotUnderstand: (clase 141),
 donde se implementa el método que falta, y se continúa."
```

**Diseñar escribiendo el código del cliente antes que el del servidor** es una práctica que este entorno
hace trivial, y que responde a la segunda regla del cierre de esta clase: **la interfaz sale de lo que se
necesita, no de lo que se puede ofrecer**.

Y es la diferencia entre una API diseñada desde fuera —pequeña, porque solo tiene lo que se pidió— y una
diseñada desde dentro —grande, porque expone lo que había—.

Es, probablemente, el consejo de diseño más rentable de esta clase: **escribir primero la llamada, y
después lo que la atiende**.

---

## Y de vuelta a la clase

Lo transferible: **la frontera correcta es la que hace que la mayoría de los cambios queden dentro de un
solo componente**. Ese es el criterio, y es medible: si cada funcionalidad nueva toca tres componentes,
la separación está mal hecha, por muy bonito que sea el diagrama. De ahí las dos reglas: **agrupar lo
que cambia junto y separar lo que cambia por razones distintas**; y **hacer las interfaces estrechas**,
porque **todo lo que se expone hay que mantenerlo** — y lo que no se expone se puede cambiar el martes
sin avisar a nadie.

⏮️ [Volver a la clase 166](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
