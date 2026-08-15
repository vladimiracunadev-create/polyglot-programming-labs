# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 160

> [⬅️ Volver a la clase 160](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Componer un contrato: `GET /users`. Dos palabras y una barra, y ahí está el acuerdo entre dos sistemas
que quizá no comparten lenguaje, empresa ni continente. Y esta clase existe porque **ese acuerdo es lo
único que impide que un cambio en un lado rompa el otro**. Y aquí hay una genealogía que conviene
conocer: **el contrato de interfaz descrito en un lenguaje aparte, del que se generan los clientes y los
servidores, no lo inventó gRPC — lo inventó CORBA en 1991, y antes ASN.1 en 1984**.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es el **contrato como artefacto independiente**, y estos lenguajes lo enseñan porque
> **llevan décadas conviviendo con contratos que no pueden romperse**: la COMMAREA de una transacción
> CICS, la firma de un programa de servicio de IBM i, la especificación de un paquete Ada, el registro de
> una RPC de VistA. Y todos aportan la misma lección desde ángulos distintos: **un contrato sirve si está
> declarado en un sitio, si se puede comprobar y si tiene una regla de evolución**.
>
> Y aparece la pregunta que decide la arquitectura: **¿el contrato se escribe primero, o se deduce del
> código?**
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: una línea `metodo recurso` → stdout: `contrato=<METODO> /<recurso>`
- **Regla:** `combinar método y recurso en un endpoint`

| stdin | esperado |
|---|---|
| `GET users` | `contrato=GET /users` |
| `POST items` | `contrato=POST /items` |
| `PUT data` | `contrato=PUT /data` |

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
PROGRAM-ID. CONTRATO.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(60).
01  C-VERBO PIC X(10).
01  C-REC   PIC X(30).

PROCEDURE DIVISION.
    ACCEPT LINEA
    UNSTRING LINEA DELIMITED BY ALL SPACES
        INTO C-VERBO C-REC
    END-UNSTRING

    DISPLAY "contrato=" FUNCTION TRIM(C-VERBO)
            " /" FUNCTION TRIM(C-REC)
    STOP RUN.
```

**Lo que esta clase enseña en COBOL.** El mundo CICS tiene un contrato con nombre propio, y merece
explicarlo porque es uno de los más antiguos en producción continua: **la COMMAREA**.

```cobol
       01  COMMAREA-PEDIDO.
           05  CA-VERSION      PIC 9(2).        *> ¡la VERSIÓN, en el contrato!
           05  CA-OPERACION    PIC X(10).
           05  CA-CLIENTE      PIC X(10).
           05  CA-IMPORTE      PIC S9(9)V99 COMP-3.
           05  CA-COD-RETORNO  PIC 9(4).
           05  CA-MENSAJE      PIC X(80).
           05  FILLER          PIC X(200).      *> reservado para el futuro
```

**Ese copybook es el contrato entre el programa que llama y el que responde**, y las dos partes lo
comparten como fichero.

Y merece destacar las dos decisiones que aparecen ahí y que son el cierre de esta clase:

**`CA-VERSION` en el propio mensaje.** El receptor lee la versión y decide cómo interpretar el resto —lo
que permite que convivan clientes viejos y nuevos.

**Y el `FILLER` reservado**, que es la primera regla del cierre: **espacio para añadir sin mover nada**.

Y la limitación histórica de la COMMAREA merece contarse porque provocó un cambio de diseño: **está
limitada a 32 KB**. Cuando eso se quedó corto, CICS introdujo **los *channels* y *containers***:

```cobol
           EXEC CICS PUT CONTAINER('PETICION') FROM(DATOS)
                     CHANNEL('CANAL-PEDIDO') END-EXEC
           EXEC CICS LINK PROGRAM('PGMPED') CHANNEL('CANAL-PEDIDO') END-EXEC
           EXEC CICS GET CONTAINER('RESPUESTA') INTO(RESULTADO) END-EXEC
```

**Los contenedores tienen nombre, tamaño ilimitado y se pueden añadir sin romper nada** — porque **el
receptor pide los que conoce e ignora los demás**.

Es exactamente la tercera regla del cierre de esta clase, y es la misma solución que los campos con
identificador de Protobuf (clase 159): **pasar de posiciones fijas a elementos con nombre**.

Y hoy, la capa que expone todo eso como API moderna:

```text
z/OS Connect lee el copybook y genera OpenAPI 3.0
El contrato REST se deriva del contrato COBOL, y se publica.
```

**Y ahí aparece la pregunta del "por qué" de esta clase**: ese contrato **se deduce del código**, así que
**un cambio en el copybook cambia la API publicada**.

La práctica correcta —y la que la disciplina de estos sistemas ya aplicaba— es la contraria: **el
copybook de la interfaz es un artefacto propio, distinto de las estructuras internas del programa**, y se
gestiona con su propio ciclo de aprobación.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program contrato
   implicit none
   character(len=60) :: linea
   character(len=10) :: verbo
   character(len=30) :: recurso
   integer :: p1

   read(*, '(A)') linea
   linea = adjustl(linea)

   p1 = index(linea, ' ')
   verbo = linea(1:p1-1)
   recurso = adjustl(linea(p1+1:))

   write(*, '(A)') 'contrato=' // trim(verbo) // ' /' // trim(recurso)
end program contrato
```

**Lo que esta clase enseña en Fortran.** El mundo científico tiene contratos de interfaz muy serios, y
merecen conocerse porque **no son APIs de red: son especificaciones de bibliotecas y de formatos de
datos**.

**El caso mayor es el de la clase 149: BLAS y LAPACK.**

```text
La especificación de BLAS define, para cada rutina:
  - el nombre exacto y el orden de los argumentos
  - qué hace cada uno y en qué dirección
  - qué valores son válidos y qué pasa si no lo son
  - y la semántica matemática exacta
```

**Y esa especificación es el contrato**: Intel, AMD, NVIDIA y OpenBLAS escriben implementaciones
independientes **que son intercambiables** porque todas cumplen el mismo documento.

Es exactamente lo que un contrato de API busca, con una diferencia notable: **lleva cuarenta años sin
romperse**.

Y merece preguntarse por qué funcionó tan bien, porque las razones son las del cierre de esta clase:

**Uno, el contrato es un artefacto propio** —un documento y unas cabeceras de referencia—, no la
implementación de nadie.

**Dos, existe una implementación de referencia** contra la que comparar (clase 140).

**Y tres, se evoluciona solo añadiendo**: BLAS ha crecido con niveles y con variantes nuevas, **sin
cambiar nunca la firma de una rutina existente**.

Y el segundo contrato de este mundo es de datos, y ya apareció en la clase 159: **las convenciones CF**.

```text
CF Conventions define, para ficheros NetCDF de datos climáticos:
  - los nombres estándar de las variables (air_temperature, sea_surface_height...)
  - las unidades, con una sintaxis formal
  - cómo se declaran las coordenadas, las mallas y el tiempo
  - y cómo se marca lo que falta
```

**Con eso, un programa puede leer un fichero de un centro que no conoce y saber qué contiene**, porque el
vocabulario está acordado.

Es un contrato **semántico**, no solo estructural, y merece destacarlo porque es lo que le falta a la
mayoría de las APIs: **JSON Schema dice que un campo es un número; CF dice que es una temperatura del
aire en kelvin a dos metros del suelo**.

Y esa diferencia —**estructura frente a significado**— es la que separa una interfaz que se puede
consumir de una que además se puede entender.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO; use Ada.Text_IO;
with Ada.Strings;
with Ada.Strings.Fixed;

procedure Contrato is
   Linea  : String (1 .. 60);
   Ultimo : Natural;
   Sep    : Natural;
begin
   Get_Line (Linea, Ultimo);
   Sep := Ada.Strings.Fixed.Index (Linea (1 .. Ultimo), " ");

   Put_Line ("contrato=" & Linea (1 .. Sep - 1) & " /" &
             Ada.Strings.Fixed.Trim (Linea (Sep + 1 .. Ultimo), Ada.Strings.Both));
end Contrato;
```

**Lo que esta clase enseña en Ada.** Ada tiene el contrato dentro del lenguaje, y esta clase es el sitio
para verlo como lo que es: **una especificación de paquete es un contrato de API completo** (clase 154).

```ada
package Cuentas is

   type Cuenta is private;
   type Importe is delta 0.01 range 0.00 .. 1_000_000.00;

   Saldo_Insuficiente : exception;

   function Saldo (C : Cuenta) return Importe
     with Post => Saldo'Result >= 0.00;

   procedure Retirar (C : in out Cuenta; Cantidad : Importe)
     with Pre  => Cantidad > 0.00,
          Post => Saldo (C) = Saldo (C'Old) - Cantidad;

private
   ...
end Cuentas;
```

**Ahí está todo lo que un contrato de API necesita**, y merece enumerarlo porque la correspondencia es
exacta:

| Elemento de Ada | Equivalente en una API |
|---|---|
| Los subprogramas públicos | los puntos de acceso |
| Los tipos y subtipos con rango | **el esquema, con validación** |
| Las excepciones declaradas | los códigos de error documentados |
| **`Pre`** | qué peticiones son válidas |
| **`Post`** | qué garantiza la respuesta |
| La parte `private` | lo que no es contrato y puede cambiar |

**Y la diferencia con un contrato de API típico es que este se comprueba** (clase 118): las
precondiciones fallan en ejecución, y con SPARK se demuestran.

Es la primera práctica del cierre —**un artefacto propio y versionado**— con la ventaja de que **el
compilador se niega a compilar si la implementación no lo cumple**.

Y merece contar el contrato más famoso del mundo de Ada, porque es una lección de esta clase: **el
estándar mismo**.

```text
El Ada Reference Manual es un documento normativo, numerado párrafo a párrafo,
con Ada Issues (AI) que registran cada aclaración y cada cambio,
y un conjunto de PRUEBAS DE CONFORMIDAD -la ACATS- que un compilador debe pasar.
```

**La ACATS es un contrato ejecutable para implementadores de compiladores**: miles de programas de
prueba que verifican que el compilador cumple el estándar.

Es, exactamente, lo que la segunda práctica del cierre pide —**comprobar el contrato automáticamente**—
aplicado al lenguaje entero, y explica por qué el código Ada es tan portable entre compiladores comparado
con C++ (clase 147).

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Contrato;
{$MODE OBJFPC}{$H+}
uses SysUtils, StrUtils;

var
  Linea, Verbo, Recurso: string;
  P: Integer;

begin
  ReadLn(Linea);
  Linea := Trim(Linea);

  P := Pos(' ', Linea);
  Verbo := Copy(Linea, 1, P - 1);
  Recurso := Trim(Copy(Linea, P + 1, Length(Linea)));

  WriteLn('contrato=', Verbo, ' /', Recurso);
end.
```

**Lo que esta clase enseña en Pascal.** El mundo Delphi vivió de cerca la generación de contratos más
ambiciosa de los años noventa, y merece contarla porque es la abuela de gRPC: **COM y su biblioteca de
tipos**.

```pascal
{ Una interfaz COM en Object Pascal }
type
  ICalculadora = interface(IUnknown)
    ['{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}']    { ← el GUID: la IDENTIDAD }
    function Sumar(A, B: Integer): Integer; safecall;
  end;
```

Y las tres decisiones de COM que merecen destacarse porque resuelven el cierre de esta clase:

**Una, el GUID como identidad de la interfaz.** Un identificador único global, no un nombre.

**Y la regla que va con él es tajante y es la mejor formulación de la tercera práctica del cierre**:

> **Una interfaz COM publicada NUNCA se modifica. Si hace falta cambiarla, se crea `IFoo2`.**

**Nada de añadir un método, nada de cambiar un parámetro.** Y por eso existen `IShellFolder`,
`IShellFolder2`, `IPersistStream`, `IPersistStreamInit`… **con nombres feos y compatibilidad de
treinta años**.

Es una disciplina extrema y funciona: **binarios de 1997 siguen funcionando en Windows actual**.

**Dos, la biblioteca de tipos** —la *type library*—, que es el contrato legible por máquina: **describe
las interfaces, los métodos, los tipos y las constantes**, y **de ella se generan los enlaces
automáticamente** en Delphi, en C++, en Visual Basic y en .NET (clase 158).

**Y tres, `safecall`**, que ya apareció en la clase 157: **la convención de llamada convierte las
excepciones en códigos de error**, así que **el contrato incluye la semántica de fallo** y funciona entre
lenguajes con modelos de excepciones distintos.

Y el ecosistema Pascal actual está en el mundo REST:

| Herramienta | Qué hace |
|---|---|
| **mORMot** | servicios con interfaces de Pascal, y OpenAPI generado |
| **DataSnap / RAD Server** | servicios REST integrados |
| **`OpenAPI` generators** | generan cliente Delphi desde una especificación |

Y merece cerrar con la comparación que esta página permite: **COM exigía disciplina y daba compatibilidad
binaria de décadas; REST no exige nada y por eso casi todas las APIs REST rompen a sus clientes al menos
una vez**.

La diferencia no está en la tecnología: está en **si hay una regla escrita sobre qué se puede cambiar**.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let* ((linea (read-line))
       (sep (position #\Space linea))
       (verbo (subseq linea 0 sep))
       (recurso (string-trim '(#\Space #\Return) (subseq linea (1+ sep)))))
  (format t "contrato=~A /~A~%" verbo recurso))
```

**Lo que esta clase enseña en Common Lisp.** Lisp aporta a esta clase una capacidad que su naturaleza
hace natural y que merece destacarse: **el contrato puede ser un dato del que se genere todo**.

```lisp
(define-api pedidos
  (:get "/pedidos/:id"
   :respuesta (:id integer :cliente string :total decimal)
   :errores ((404 "no encontrado")))
  (:post "/pedidos"
   :cuerpo (:cliente string :items (list-of item))
   :respuesta (:id integer)))
```

**Y de esa única declaración se puede generar, con macros** (clase 122):

- **Las rutas del servidor y la validación de la entrada.**
- **El cliente**, con funciones tipadas.
- **La documentación** en OpenAPI.
- **Y las pruebas de contrato.**

Es la primera práctica del cierre —**el contrato como artefacto propio**— con la particularidad de que
**el artefacto vive en el mismo lenguaje**, así que no hay un paso de generación separado ni un fichero
que se olvide de regenerar.

Es la misma idea que la clase 158 mostraba con los enlaces, aplicada a las APIs.

Y merece señalar el compromiso, porque es el de siempre: **ese contrato solo lo entiende Lisp**. Para que
lo entienda el resto del mundo hay que **emitir OpenAPI o un `.proto`** desde ahí — lo que devuelve el
problema al terreno común.

Y el ecosistema:

| Biblioteca | Notas |
|---|---|
| **Hunchentoot / Clack / Woo** | servidores HTTP |
| **Snooze / cl-rest-server** | rutas declarativas |
| **cl-protobufs** | Protobuf con compilador de `.proto` |
| **cl-json-schema** | validación contra JSON Schema |

Y Lisp permite cerrar esta clase con una observación que la atraviesa: **un contrato es una gramática, y
las gramáticas se pueden ejecutar en las dos direcciones**.

De una misma descripción se puede **generar** un mensaje válido y **validar** uno recibido — y las
herramientas que hacen las dos cosas desde la misma fuente son las que de verdad garantizan que no
divergen.

Es la razón por la que los formatos con esquema obligatorio —Protobuf, ASN.1— tienen menos incidentes de
incompatibilidad que los que lo tienen opcional: **cuando la validación y la generación salen del mismo
sitio, no pueden discrepar**.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea
lassign [string trim $linea] verbo recurso

puts "contrato=$verbo /$recurso"
```

**Lo que esta clase enseña en Tcl.** Tcl aporta a esta clase la perspectiva del lenguaje que **consume**
contratos ajenos, que es el papel de un lenguaje de pegamento (clase 155).

```tcl
package require http
package require json

set tok [http::geturl "https://api.ejemplo.com/pedidos/4711" \
             -headers {Accept application/json}]
set datos [json::json2dict [http::data $tok]]
http::cleanup $tok

dict get $datos cliente
```

**Y ahí aparece el problema central de esta clase desde el lado del consumidor**: `dict get $datos
cliente` **falla si el campo no está**, y **nada avisó de que podía no estar**.

Y las tres defensas que un consumidor debería aplicar y que casi nadie aplica merecen enumerarse:

```tcl
# 1. valor por defecto en vez de fallo
set cliente [expr {[dict exists $datos cliente] ? [dict get $datos cliente] : ""}]

# 2. validar contra el esquema publicado, no confiar
package require json::write
# (o validar con una biblioteca de JSON Schema)

# 3. y NO fallar por campos desconocidos: ignorarlos
```

**La tercera es la que hace posible que el emisor evolucione** (clase 159), y es la tercera regla del
cierre de esta clase vista desde el otro lado: **el consumidor tolerante es lo que permite al proveedor
añadir**.

Y Tcl aporta un caso de contrato muy distinto y muy real, que merece contarse porque es el suyo: **los
flujos de diseño de circuitos**.

```tcl
# El "contrato" entre el diseñador y la herramienta:
read_verilog diseno.v
set_clock_period 2.5
compile_ultra
write_verilog netlist.v
```

**Los comandos de Tcl que una herramienta de Synopsys o Cadence expone son su API**, y **cambiarlos entre
versiones rompe flujos de diseño de decenas de miles de líneas** que las empresas han afinado durante
años.

Y por eso esas herramientas mantienen **compatibilidad de comandos durante décadas**, con la misma
disciplina que COM en esta página: **los comandos viejos siguen, marcados como obsoletos, y los nuevos se
añaden**.

Es la misma conclusión, en un dominio inesperado: **cuando el coste de romper es alto y visible, la
disciplina de contrato aparece sola**.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;
my ($verbo, $recurso) = split ' ', $linea;

print "contrato=$verbo /$recurso\n";
```

**Lo que esta clase enseña en Perl.** Perl aporta a esta clase la práctica que el cierre nombra en segundo
lugar y que es la más útil de todas: **comprobar el contrato automáticamente en los dos lados**.

Y el ecosistema tiene la herramienta que la implementa:

```perl
use Test::More;
use JSON::Schema::Modern;

my $esquema = decode_json(path('contratos/pedido.schema.json')->slurp);
my $validador = JSON::Schema::Modern->new(schema => $esquema);

my $respuesta = $cliente->get('/pedidos/4711');
ok($validador->evaluate(decode_json($respuesta->content))->valid,
   'la respuesta cumple el contrato publicado');
```

**Esa prueba se ejecuta en el lado del proveedor y en el del consumidor, con el mismo fichero de
esquema**, y falla en la integración continua si alguien lo rompe (clase 147).

Y merece explicar la técnica que va un paso más allá y que resuelve el problema real, porque es una de
las mejores ideas de la última década: **las pruebas de contrato dirigidas por el consumidor**.

```text
1. Cada CONSUMIDOR escribe qué necesita de la API, como un "pacto":
     "cuando pido GET /pedidos/4711, espero un objeto con id y total"
2. Ese pacto se publica en un repositorio compartido.
3. El PROVEEDOR ejecuta TODOS los pactos de todos sus consumidores en su CI.
4. Si un cambio rompe a alguien, el proveedor se entera ANTES de desplegar.
```

**Eso invierte la responsabilidad**, y es lo que lo hace funcionar: **el proveedor no tiene que adivinar
qué usan sus consumidores — se lo dicen, en forma ejecutable**.

Y resuelve el problema práctico que la clase 148 planteaba: **cómo desplegar sin coordinar a todo el
mundo a la vez**.

El ecosistema:

| Herramienta | Notas |
|---|---|
| **`Pact::Perl` / Pact en general** | pruebas de contrato dirigidas por el consumidor |
| **`JSON::Schema::Modern`** | validación de JSON Schema |
| **`OpenAPI::Client`** | cliente generado desde una especificación OpenAPI |
| **`Mojolicious::Plugin::OpenAPI`** | **servidor que valida entrada y salida contra la especificación** |

**El último merece la mención final** porque aplica la primera práctica del cierre de la forma más
estricta: **la especificación OpenAPI es la fuente, y el marco valida cada petición y cada respuesta
contra ella en ejecución**.

**Si el código devuelve algo que no cumple lo publicado, falla en desarrollo** — con lo que la
documentación no puede mentir, que es el fallo más común de las APIs escritas a mano.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>
#include <string>

int main() {
    std::string verbo, recurso;
    if (!(std::cin >> verbo >> recurso)) return 1;

    std::cout << "contrato=" << verbo << " /" << recurso << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** C++ es donde vive **gRPC**, y esta clase es el sitio para ver por
qué su diseño es el que es — y de dónde viene, que es el dato del gancho.

```protobuf
syntax = "proto3";

service Pedidos {
  rpc Obtener(ObtenerReq) returns (Pedido);
  rpc Listar(ListarReq) returns (stream Pedido);      // flujo de salida
  rpc Cargar(stream Linea) returns (Resumen);          // flujo de entrada
  rpc Chat(stream Msg) returns (stream Msg);            // bidireccional
}

message ObtenerReq { int32 id = 1; }
```

```bash
protoc --cpp_out=. --grpc_out=. --python_out=. --go_out=. pedidos.proto
```

**Un fichero, muchos lenguajes, cliente y servidor generados.**

Y **la genealogía merece contarse**, porque casi nadie la conoce:

| Año | Sistema | Qué aportó |
|---|---|---|
| **1984** | **ASN.1** | esquema formal + codificaciones binarias (BER, DER, PER) |
| **1988** | **Sun RPC / XDR** | IDL + generación de cliente y servidor (NFS lo usa) |
| **1991** | **CORBA IDL** | IDL independiente del lenguaje, con objetos remotos |
| **1996** | **DCOM** | lo mismo, en el mundo de Microsoft |
| **1998** | **SOAP / WSDL** | lo mismo, en XML y sobre HTTP |
| **2008** | **Protobuf** (interno desde 2001) | esquema compacto y **evolución bien pensada** |
| **2015** | **gRPC** | Protobuf + HTTP/2 + flujos |

**ASN.1 sigue en uso masivo hoy** —los certificados TLS, la telefonía móvil y el correo seguro están
codificados en ASN.1 DER— y es de hace cuarenta años.

Y merece preguntarse qué hizo Protobuf mejor que CORBA, porque la respuesta es la lección de esta clase:

**CORBA intentó hacer que un objeto remoto se pareciera a uno local** —con herencia, referencias, ciclo
de vida y transacciones distribuidas— **y esa abstracción se rompía**: la red falla, y un método remoto
que parece local esconde eso.

**Protobuf y gRPC hicieron lo contrario**: **mensajes explícitos, sin objetos remotos, sin estado
compartido, y con el fallo visible**.

Es la aplicación de una regla que atraviesa toda la Parte 10: **una frontera debe verse como frontera**.
Ocultarla hace el código más bonito y el sistema más frágil.

Y las herramientas de comprobación, que es la segunda práctica del cierre:

```bash
buf lint                  # comprueba estilo del .proto
buf breaking --against '.git#branch=main'    # ¿este cambio ROMPE el contrato?
```

**`buf breaking` compara dos versiones del esquema y falla si el cambio es incompatible** —quitar un
campo, reutilizar un identificador, cambiar un tipo—.

Es exactamente `abi-compliance-checker` de la clase 157, aplicado al contrato de datos en lugar de al
binario, y merece estar en la integración continua por la misma razón.

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

dcl-pi CONTRATO;
  verbo   char(10) const;
  recurso char(30) const;
end-pi;

dsply ('contrato=' + %trim(verbo) + ' /' + %trim(recurso));

*inlr = *on;
return;
```

**Lo que esta clase enseña en RPG.** IBM i tiene, en esta clase, el contrato mejor comprobado de toda la
página, y ya apareció dos veces: **la firma de un programa de servicio** (clases 143 y 157).

Y merece verlo aquí como lo que es —**un contrato de API con verificación automática**— y compararlo con
lo que hace la industria:

| Aspecto | Programa de servicio de IBM i | API REST típica |
|---|---|---|
| El contrato | **la lista ordenada de exportaciones** | OpenAPI, si alguien lo mantiene |
| Verificación | **el sistema, al activar el programa** | esperanza, o pruebas de contrato |
| Al romperse | **el programa no arranca, con mensaje claro** | error en producción |
| Evolución | **firmas múltiples**: la nueva y las anteriores | versionado en la URL, si acaso |
| Coste | cero: está en el objeto | herramientas y disciplina |

**La fila de la evolución merece subrayarse**, porque es la tercera práctica del cierre implementada:

```text
STRPGMEXP PGMLVL(*CURRENT) SIGNATURE('PEDIDOS V3')
  EXPORT SYMBOL('CREAR')
  EXPORT SYMBOL('CONSULTAR')
  EXPORT SYMBOL('ANULAR')        /* nuevo */
ENDPGMEXP
STRPGMEXP PGMLVL(*PRV) SIGNATURE('PEDIDOS V2')
  EXPORT SYMBOL('CREAR')
  EXPORT SYMBOL('CONSULTAR')
ENDPGMEXP
```

**El proveedor declara explícitamente qué versiones del contrato sigue soportando**, y el sistema
comprueba cuál usa cada cliente.

Es lo que en el mundo REST se intenta con `/v1/` y `/v2/` en la URL, con la diferencia de que **aquí la
comprobación es automática y el fallo es al arrancar, no en la primera petición rara**.

Y la capa moderna, que la clase 158 ya nombró:

```text
IWS lee el prototipo y publica el servicio con su OpenAPI.
El contrato REST se DERIVA del contrato RPG.
```

**Y ahí aparece la advertencia de esta clase**: derivar el contrato del código significa que **cualquier
cambio en el prototipo cambia la API publicada**.

La práctica correcta, y es la primera del cierre: **el prototipo que se expone es un artefacto propio**
—un procedimiento de fachada, escrito para eso— **distinto de los procedimientos internos que pueden
evolucionar libremente**.

Es la misma separación que la clase 158 pedía entre la capa literal y la idiomática, aplicada aquí a lo
que se publica y lo que se reserva.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 contrato: procedure options(main);

    declare linea   char(60) varying;
    declare verbo   char(10) varying;
    declare recurso char(30) varying;
    declare p       fixed binary(31);

    get edit (linea) (a(60));
    linea = trim(linea);

    p = index(linea, ' ');
    verbo = substr(linea, 1, p - 1);
    recurso = trim(substr(linea, p + 1));

    put skip list ('contrato=' || verbo || ' /' || recurso);

 end contrato;
```

**Lo que esta clase enseña en PL/I.** PL/I vive en el sistema que inventó buena parte del vocabulario de
esta clase, y merece recogerlo porque explica de dónde salieron las ideas.

**El mainframe tiene contratos de interfaz muy formales, y varios tipos:**

| Contrato | Entre qué |
|---|---|
| **La COMMAREA / los contenedores** | programas de una transacción CICS (COBOL en esta página) |
| **El *program interface block*** | programa y gestor de base de datos IMS |
| **La lista de parámetros de LE** | módulos de lenguajes distintos (clase 157) |
| **El *copybook* / la declaración compartida** | cualquier par de programas |
| **La definición de MQ** | sistemas separados, por cola de mensajes |

**Y el último merece el detalle**, porque es la arquitectura de integración más influyente que salió de
este mundo: **IBM MQ, de 1993**.

```text
Un programa PONE un mensaje en una cola con un formato acordado.
Otro programa, quizá en otra máquina, otro sistema operativo y otro lenguaje,
lo SACA cuando puede.
```

Y las propiedades que eso da son las que hicieron carrera:

- **Desacoplamiento temporal**: el receptor no tiene que estar vivo cuando el emisor envía.
- **Entrega garantizada y transaccional**: el mensaje participa en la transacción.
- **Y el contrato es el formato del mensaje**, no una firma de función.

**Es la arquitectura orientada a mensajes**, y de ahí salió directamente todo el vocabulario de los
*Enterprise Integration Patterns* (clase 151) y, en buena medida, la arquitectura de eventos actual.

Y merece señalar la ventaja concreta que tiene sobre una llamada síncrona y que esta clase debe
recoger: **el contrato de una cola es más fácil de evolucionar**.

```text
Con una llamada:  si el receptor cambia, el emisor falla AHORA.
Con una cola:     los mensajes viejos y nuevos conviven en la cola,
                  y el receptor puede manejar las dos versiones a su ritmo.
```

Es la tercera práctica del cierre de esta clase —**no se puede desplegar todo a la vez**— convertida en
propiedad de la arquitectura en lugar de en disciplina de las personas.

Y es la razón por la que, treinta años después, la respuesta habitual a "¿cómo desacoplo estos dos
sistemas?" sigue siendo la misma: **poner una cola en medio**.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
CONTRATO ; Contrato de API -- clase 160
 read linea
 new verbo, recurso
 set verbo = $piece(linea, " ", 1)
 set recurso = $piece(linea, " ", 2)
 write "contrato=", verbo, " /", recurso, !
 quit
```

**Lo que esta clase enseña en M.** El mundo sanitario tiene los contratos de interoperabilidad más
desarrollados de cualquier sector, y merece contarlos porque **es el mejor caso de estudio de esta clase
que existe**.

**HL7 v2 (1987): el contrato de posiciones.**

```text
MSH|^~\&|LAB|HOSP|EMR|HOSP|20240315103000||ORU^R01|MSG001|P|2.5
PID|1||123456^^^HOSP^MR||GARCIA^ANA||19800101|F
OBX|1|NM|GLU^Glucosa^LN||95|mg/dL|70-110|N|||F
```

**Segmentos con nombre, campos separados por barras, posiciones fijas**, y un diccionario aparte que dice
qué es cada una.

Es exactamente el modelo de las globals de M (clase 159), y sus problemas son los mismos: **compacto,
universal y con el significado fuera del mensaje**.

Y hay algo más grave que merece decirse, porque es la lección: **HL7 v2 tiene tantos campos opcionales y
tanta variabilidad permitida que en la práctica cada hospital lo implementa distinto**.

**Un contrato que permite demasiado no es un contrato.** Y por eso la integración de dos sistemas
sanitarios sigue costando meses: **hay que negociar qué subconjunto usa cada uno**.

**FHIR (2014): el contrato con esquema.**

```json
{
  "resourceType": "Patient",
  "id": "123456",
  "identifier": [{"system": "http://hosp/mrn", "value": "123456"}],
  "name": [{"family": "García", "given": ["Ana"]}],
  "birthDate": "1980-01-01"
}
```

Y lo que FHIR hace distinto merece enumerarse, porque es el cierre de esta clase aplicado con rigor:

- **Recursos definidos formalmente**, con esquemas en JSON Schema, XML Schema y `StructureDefinition`.
- **Vocabularios controlados**: LOINC para pruebas, SNOMED para diagnósticos — **contrato semántico**,
  como las convenciones CF de Fortran en esta página.
- **Perfiles**: un país o una organización **restringe** el estándar para su uso, y **esa restricción es
  también un artefacto formal y validable**.
- **Y extensiones con URL**, para añadir lo propio **sin romper a quien no las conoce** — la tercera regla
  del cierre, con nombre.

**Los perfiles son la idea más valiosa y la más transferible**: reconocen que **un estándar global tiene
que permitir mucho**, y que **la interoperabilidad real ocurre cuando alguien publica formalmente qué
subconjunto usa**.

Es la respuesta al problema de HL7 v2, y es aplicable a cualquier API grande: **publicar no solo lo que se
puede enviar, sino lo que de verdad se envía**.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| linea partes |

linea := stdin nextLine trimBoth.
partes := linea substrings: ' '.

Transcript
    show: 'contrato=', (partes at: 1), ' /', (partes at: 2);
    cr.
```

**Lo que esta clase enseña en Smalltalk.** Smalltalk aporta a esta clase una perspectiva incómoda y útil:
**su noción de contrato es el protocolo, y el protocolo no está declarado en ninguna parte** (clase 149).

```smalltalk
"Un 'protocolo' es un conjunto de mensajes que un objeto entiende.
 No hay declaración: si responde, sirve."
```

**Eso es tipado por comportamiento**, y hace el código extraordinariamente flexible **y el contrato
implícito**.

Y la comunidad lo reconoció y construyó respuestas parciales que merecen conocerse:

**Las categorías de método** —los *protocols* del navegador— agrupan los mensajes por propósito
(`accessing`, `printing`, `private`), y **funcionan como documentación de qué forma parte de la interfaz
pública**.

```smalltalk
"Por convención, la categoría 'private' marca lo que NO es contrato"
```

**Los *traits* y los tipos explícitos** de algunos dialectos —Strongtalk, Pharo con `Typer`— intentaron
declararlo formalmente.

**Y las pruebas** —SUnit, inventado aquí (clase 139)— **son el contrato ejecutable**: en un lenguaje sin
declaraciones de tipo, **la prueba es lo que dice qué se espera de un objeto**.

Es la conclusión práctica que la comunidad dinámica alcanzó y merece extraerse: **cuando el lenguaje no
declara el contrato, las pruebas tienen que hacerlo** — y por eso la cultura de pruebas nació en los
lenguajes dinámicos y no en los tipados.

Y para las APIs de red, el ecosistema es moderno y competente:

| Herramienta | Notas |
|---|---|
| **Zinc HTTP** | cliente y servidor HTTP |
| **Teapot / Seaside REST** | rutas declarativas |
| **NeoJSON / STON** | serialización (clase 159) |
| **OpenAPI para Pharo** | generar cliente y documentación |

Y merece cerrar la clase, y con ella el bloque de contratos, con la observación que la página entera
sostiene:

**Todos los mecanismos de esta página** —la COMMAREA, la firma de programa de servicio, la especificación
de Ada, el GUID de COM, el `.proto`, el perfil FHIR, la prueba de SUnit— **hacen lo mismo: escribir en un
sitio lo que dos partes tienen que creer**.

Y todos fracasan por el mismo motivo cuando fracasan: **porque alguien cambió una de las partes sin mirar
el papel**. La tecnología solo decide **si eso se detecta antes o después de que llegue a producción** —
y esa es, al final, toda la diferencia que la ingeniería puede aportar aquí.

---

## Y de vuelta a la clase

Lo transferible: **el contrato es más duradero que cualquiera de sus dos lados, así que merece más
cuidado que ninguno de los dos**. De ahí las tres prácticas que aparecen en toda la página: **escribirlo
en un artefacto propio y versionado** —no deducirlo del código, porque entonces cualquier refactorización
lo cambia—; **comprobarlo automáticamente en los dos lados**, con pruebas de contrato que fallen en la
integración continua cuando alguien lo rompa; y **evolucionarlo solo añadiendo**, porque en cuanto hay
más de un consumidor **ya no se puede desplegar todo a la vez** — que es exactamente el problema que la
clase 148 planteaba con los datos.

⏮️ [Volver a la clase 160](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
