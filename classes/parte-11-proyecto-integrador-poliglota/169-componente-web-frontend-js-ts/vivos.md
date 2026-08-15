# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 169

> [⬅️ Volver a la clase 169](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Un contador de elementos y un `render=ok`. Es lo que hace un frontal: **coger datos y pintarlos**. Y esta
clase tiene una premisa que conviene decir de entrada: **ninguno de estos doce lenguajes es hoy la
elección para el componente web, y todos han pintado interfaces**. Unos generando HTML desde el servidor,
otros con bibliotecas gráficas propias, y varios —de forma sorprendente— **ejecutándose dentro del
navegador** (clase 162).

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es la **capa de presentación como componente**, y estos lenguajes la enseñan porque
> **vivieron todas las generaciones**: pantallas de bloques (3270, 5250), interfaces de escritorio (Tk,
> VCL), HTML generado en el servidor (CGI, mod_perl), y hoy WebAssembly. Y esa historia deja una lección
> que la moda oculta: **cada generación resolvió los mismos problemas** —estado, validación, navegación,
> rendimiento— **y las soluciones se parecen mucho más de lo que su vocabulario sugiere**.
>
> Y aparece la decisión de siempre: **cuánta lógica vive en el cliente**.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: un entero `n` (número de elementos a renderizar) → stdout: `items=<n> render=ok`
- **Regla:** `renderizar n elementos y confirmar`

| stdin | esperado |
|---|---|
| `3` | `items=3 render=ok` |
| `0` | `items=0 render=ok` |
| `10` | `items=10 render=ok` |

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
PROGRAM-ID. FRONTAL.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(40).
01  N       PIC S9(9) COMP.
01  ED      PIC -(8)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    COMPUTE N = FUNCTION NUMVAL(LINEA)

    MOVE N TO ED
    DISPLAY "items=" FUNCTION TRIM(ED) " render=ok"
    STOP RUN.
```

**COBOL y la capa de presentación.** COBOL tiene una historia con las interfaces que merece contarse
porque **inventó el formulario y la validación declarativa**: **las pantallas BMS de CICS**.

```text
MAPA    DFHMSD TYPE=MAP,MODE=INOUT,LANG=COBOL,TIOAPFX=YES
PANT1   DFHMDI SIZE=(24,80)
NOMBRE  DFHMDF POS=(3,10),LENGTH=20,ATTRB=(UNPROT,IC),
               INITIAL='                    '
IMPORTE DFHMDF POS=(5,10),LENGTH=9,ATTRB=(UNPROT,NUM),PICIN='9(7)V99'
MENSAJE DFHMDF POS=(23,1),LENGTH=79,ATTRB=(PROT,BRT)
```

**Ese fichero define la pantalla**, y de él se genera **una estructura COBOL con un campo por control**.

Y merece enumerar lo que ya hacía, porque es exactamente lo que un formulario web necesita:

| Atributo | Qué hace |
|---|---|
| **`UNPROT` / `PROT`** | editable o solo lectura |
| **`NUM`** | **el terminal solo acepta dígitos**: validación en el cliente |
| **`IC`** | dónde va el cursor al abrir |
| **`BRT` / `DRK`** | resaltado, y **campos ocultos para contraseñas** |
| **`PICIN` / `PICOUT`** | formato de entrada y de salida |
| **`MDT`** | **marca de campo modificado**: solo se transmite lo que cambió |

**La última merece destacarse** porque es una optimización que la web redescubrió: **el terminal 3270
envía solo los campos modificados**, no la pantalla entera.

**Es exactamente la idea del DOM virtual y de las actualizaciones parciales**, en un protocolo de 1972 y
por la misma razón: **el ancho de banda era caro**.

Y la arquitectura de aquello es la del cierre de esta clase, y conviene verla:

```text
El terminal valida el TIPO (NUM impide letras).
El programa valida TODO lo demás en el servidor.
El estado de la conversación va en la COMMAREA, no en el terminal (clase 168).
```

**Validación doble, estado en el servidor, y el terminal sin lógica de negocio** — las tres reglas del
cierre, cincuenta años antes de que hubiera navegadores.

Y hoy, el frontal de un sistema COBOL es web o móvil, y habla con él por una API (clase 160). **La
lección que queda es que la pantalla vieja hacía bien lo que muchas aplicaciones nuevas hacen mal**:
tenía un contrato declarado, generado y comprobado.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program frontal
   implicit none
   integer :: n

   read(*, *) n

   write(*, '(A,I0,A)') 'items=', n, ' render=ok'
end program frontal
```

**Fortran y la capa de presentación.** Fortran no pinta interfaces, y merece decirlo sin rodeos — y a
cambio, esta clase es el sitio para hablar de lo que sí produce: **visualización científica**.

```text
El "frontal" de un cálculo Fortran no es una interfaz de usuario:
  es una visualización de campos escalares y vectoriales en tres dimensiones,
  con millones de celdas y con evolución temporal.
```

Y la arquitectura habitual es la de la clase 155, con la frontera en el fichero:

```text
Fortran  →  NetCDF / HDF5 (clase 159)  →  ParaView / VisIt / VTK  →  imagen
                                        →  Python + matplotlib
                                        →  y hoy: navegador con WebGL
```

**Y esa separación es un buen ejemplo de la segunda regla del cierre**: **el visualizador no conoce el
programa que generó los datos** — solo el formato, que es autodescriptivo (clase 159).

Y por eso **el mismo ParaView visualiza salidas de decenas de códigos distintos**, y por eso un resultado
de hace quince años se puede volver a mirar.

Y hay una técnica de este dominio que merece nombrarse porque resuelve un problema que la web también
tiene: **la visualización *in situ***.

```text
Problema: una simulación genera 10 TB de datos por ejecución.
          Escribirlos y luego visualizarlos es inviable.

Solución: el visualizador se ENLAZA con el código de simulación
          y genera las imágenes MIENTRAS se calcula (Catalyst, Ascent).
```

**Es mover el cálculo hacia el dato en lugar del dato hacia el cálculo**, y es la misma idea que el
renderizado en el servidor y que los cálculos en el borde.

Y para el proyecto de esta parte, la aportación de esta columna es una recomendación concreta: **el
componente de cálculo no debe generar la presentación**.

Debe **emitir datos con un formato declarado**, y que el frontal —web, cuaderno o herramienta de
visualización— decida cómo se ven. Es la separación de la clase 149, y aquí tiene una consecuencia
práctica inmediata: **la misma salida sirve para la gráfica, para el informe y para el análisis
posterior**.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;
with Ada.Strings;
with Ada.Strings.Fixed;

procedure Frontal is
   N : Integer;
begin
   Get (N);

   Put_Line ("items=" & Ada.Strings.Fixed.Trim (N'Image, Ada.Strings.Both) &
             " render=ok");
end Frontal;
```

**Ada y la capa de presentación.** Ada tiene interfaces gráficas —GtkAda, Gnoga, AWS con web— y merece
plantear la pregunta que su dominio hace inevitable y que esta clase debe recoger: **¿qué pasa cuando la
interfaz es crítica?**

```text
Una pantalla de cabina de avión, un panel de control de una central
o el display de un desfibrilador NO son "frontales":
  son componentes con requisitos de seguridad.
```

Y las reglas que esos sistemas aplican merecen conocerse, porque son la versión extrema del cierre de
esta clase:

| Regla | Motivo |
|---|---|
| **La interfaz no decide nada** | solo muestra y transmite; la lógica está detrás |
| **Todo dato mostrado tiene una marca de frescura** | un valor congelado es peor que ninguno |
| **Los estados se pintan de forma inequívoca** | nada de depender solo del color |
| **La entrada se confirma en el sistema, no en la pantalla** | la validación real está detrás |
| **Y la interfaz no puede bloquear al control** | particiones de tiempo (clase 165) |

**La segunda merece el detalle**, porque es un fallo real y de los peores: **una pantalla que sigue
mostrando el último valor recibido cuando el sensor ha dejado de enviar** hace creer que todo va bien.

**La defensa es que el dato lleve su instante y que la pantalla lo marque como obsoleto** — y es
transferible a cualquier panel de control, incluidos los de un sistema informático normal.

Y hay una norma que este mundo tiene y que el resto no: **ARINC 661**, que **separa la definición de la
interfaz de la aplicación**.

```text
Un fichero de definición describe los widgets de la pantalla.
Un "servidor de cabina" certificado los pinta.
Y la aplicación solo ENVÍA DATOS y RECIBE EVENTOS.
```

**Es la separación de la primera regla del cierre llevada al extremo**: la aplicación **no puede** pintar
nada que no esté en la definición, y esa definición se certifica por separado.

Y merece la observación general: **es lo mismo que un contrato de API entre frontal y servicio** (clase
160), con la diferencia de que aquí **el sistema lo hace cumplir** — y en una aplicación normal lo hace
cumplir la disciplina.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Frontal;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  N: Integer;

begin
  Read(N);
  WriteLn('items=', IntToStr(N), ' render=ok');
end.
```

**Pascal y la capa de presentación.** Aquí Pascal tiene mucho que decir, porque **Delphi definió cómo se
construyen las interfaces de escritorio** y su modelo sigue vivo en varias herramientas.

```pascal
{ El diseñador visual, el inspector de objetos y los eventos }
procedure TForm1.Button1Click(Sender: TObject);
begin
  Label1.Caption := IntToStr(ListBox1.Items.Count) + ' items';
end;
```

**Y las tres ideas que Delphi popularizó merecen nombrarse** porque están en todas partes:

**Una, el componente visual con propiedades editables** en un inspector —y persistidas en el `.dfm`
(clase 159)—.

**Dos, la programación dirigida por eventos con métodos de objeto** (clase 151), gracias a `of object`
que hace que el manejador lleve su formulario consigo.

**Y tres, el enlace de datos**: un control conectado a un origen de datos que **se actualiza solo**.

```pascal
DBGrid1.DataSource := DataSource1;
DataSource1.DataSet := Query1;
```

**Ese enlace bidireccional entre datos e interfaz es lo que hoy hacen Vue, Angular y todos los marcos
reactivos** (clase 120) — y en Delphi es de 1995.

Y el ecosistema Pascal llega hoy a la web por los dos caminos de la clase 162:

| Camino | Notas |
|---|---|
| **`pas2js`** | Pascal **a JavaScript**, con acceso al DOM |
| **WebAssembly** | `fpc -Twasi -Pwasm32`, con generador propio |
| **TMS Web Core** | marco comercial: diseñador visual que produce web |
| **Lazarus + LCL** | escritorio nativo, multiplataforma |

**TMS Web Core merece la mención** porque persigue lo mismo que Delphi en 1995: **arrastrar controles y
que salga una aplicación**, ahora en el navegador.

Y esta clase debe recoger la advertencia que ese modelo trae y que la clase 149 ya señaló: **el diseñador
visual empuja a poner la lógica en el manejador del botón**.

**Y en un frontal eso choca con la segunda regla del cierre**: la lógica de negocio en el cliente **se
duplica, se desincroniza y se puede saltar** (clase 153). El manejador debe llamar a un servicio, no
calcular.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let ((n (read)))
  (format t "items=~D render=ok~%" n))
```

**Lisp y la capa de presentación.** Lisp llega al navegador por varios caminos, y esta clase es el sitio
para una idea suya que la industria adoptó sin saberlo: **generar el marcado con el propio lenguaje**.

```lisp
(cl-who:with-html-output-to-string (s)
  (:div :class "pedidos"
    (:h1 "Pedidos")
    (:ul
      (dolist (p pedidos)
        (:li (str (pedido-nombre p)))))))
```

**El HTML se escribe como estructuras de Lisp**, así que:

- **No hay lenguaje de plantillas que aprender**: es el mismo lenguaje.
- **Se puede componer con funciones**: un fragmento es un valor.
- **Y es imposible generar marcado mal formado**, porque la estructura es un árbol.

**Y esa última propiedad merece destacarse porque resuelve un fallo de seguridad real**: **la inyección de
HTML** (clase 153). Si el marcado se construye concatenando cadenas, **un dato con `<script>` se ejecuta**;
si se construye como árbol, **la biblioteca escapa el texto**.

Es el mismo argumento que las consultas parametrizadas frente al SQL concatenado (clase 163), aplicado a
la presentación — y es la razón por la que JSX, Hiccup y los constructores de elementos ganaron a las
plantillas de texto.

Y los caminos de Lisp al navegador:

| Vía | Notas |
|---|---|
| **cl-who / Spinneret** | generación de HTML desde el servidor |
| **Parenscript** | **escribe JavaScript con sintaxis de Lisp** |
| **JSCL / Clasp** | Common Lisp en el navegador (clase 162) |
| **ClojureScript** | el caso de éxito real: Lisp compilado a JavaScript |
| **Hoot (Guile)** | Scheme a WebAssembly con WasmGC |

**ClojureScript merece la mención** porque es el único de esta lista con adopción industrial, y **de él
salió una idea que el resto del mundo web adoptó**: **el estado de la aplicación como un único valor
inmutable**, del que la interfaz es una función.

```text
interfaz = f(estado)
```

**Esa formulación —que Re-frame y Redux popularizaron— es la tercera regla del cierre de esta clase**:
**separar el estado del pintado** hace que la interfaz sea predecible y depurable, porque **se puede
reconstruir a partir del estado**.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea
set n [string trim $linea]

puts "items=$n render=ok"
```

**Tcl y la capa de presentación.** Tcl tiene aquí un mérito histórico que merece contarse: **Tk, de 1991,
fue el primer kit de interfaces gráficas verdaderamente multiplataforma y fácil**.

```tcl
package require Tk

label .titulo -text "Pedidos"
listbox .lista
button .cerrar -text "Cerrar" -command exit

pack .titulo .lista .cerrar -fill both -expand 1
```

**Cuatro líneas y hay una ventana funcionando en Linux, Windows y macOS.**

Y merece explicar por qué eso fue tan influyente en su momento: **en 1991, hacer una interfaz gráfica
significaba escribir cientos de líneas de C con Xlib o con la API de Windows**, distintas en cada
plataforma.

**Tk lo redujo a un lenguaje declarativo con gestores de disposición**, y su influencia fue enorme:

```text
Tkinter (Python), Perl/Tk, Ruby/Tk, Tcl/Tk en R...
Tk se convirtió en el kit gráfico "por defecto" de media docena de lenguajes.
```

**Y sigue siéndolo**: `tkinter` viene con Python, y es con lo que se hacen decenas de miles de
herramientas internas.

Y las dos ideas de Tk que merecen destacarse porque son de diseño y siguen vigentes:

**Los gestores de disposición**: `pack`, `grid` y `place` — **la posición no se fija en píxeles, se
declara una relación** —"esto se expande, aquello se pega arriba"—.

**Es exactamente lo que hacen Flexbox y Grid en CSS**, treinta años después, y por la misma razón: **las
ventanas cambian de tamaño y las pantallas son distintas**.

**Y la variable enlazada**:

```tcl
entry .campo -textvariable ::nombre
# cambiar ::nombre actualiza el campo, y escribir en el campo actualiza ::nombre
```

**Enlace bidireccional entre una variable y un control**, igual que Delphi en esta página y que los
marcos reactivos actuales.

Y merece cerrar con lo que esta clase debería concluir: **los problemas de las interfaces no han cambiado**
—disposición adaptable, enlace de datos, eventos, validación— y **cada generación los ha resuelto con el
mismo puñado de ideas**, redescubiertas con vocabulario nuevo.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $n = <STDIN>;
chomp $n;

print "items=$n render=ok\n";
```

**Perl y la capa de presentación.** Perl fue **el lenguaje con el que se construyó la primera web
dinámica**, y esta clase debe contarlo porque de ahí salen varias cosas que seguimos usando.

```perl
#!/usr/bin/perl
use CGI;
my $q = CGI->new;
print $q->header('text/html'),
      $q->start_html('Pedidos'),
      $q->h1('Pedidos'),
      $q->ul(map { $q->li($_) } @pedidos),
      $q->end_html;
```

**CGI.pm, de Lincoln Stein (1995), fue durante una década el módulo más usado de CPAN**, y con él se
hicieron los primeros formularios, buscadores, foros y tiendas de la web.

Y merece nombrar lo que aquella generación estableció y que sigue vigente:

| Idea | Sigue |
|---|---|
| **Formularios HTML con `POST`** | igual |
| **Cookies de sesión** | igual |
| **Parámetros con codificación de URL** | igual |
| **Cabeceras de tipo de contenido** | igual |
| **Y la validación en el servidor, siempre** | **la primera regla del cierre** |

Y también lo que se hizo mal y que costó años corregir, porque es la lección de esta clase:

```perl
# ✗ el fallo de seguridad más común de aquella web
print "<p>Hola, $nombre</p>";       # si $nombre contiene <script>, se EJECUTA
```

**Eso es *cross-site scripting***, y fue —y sigue siendo— una de las vulnerabilidades más extendidas.

**Y la defensa es la que la explicación de Lisp de esta página describe**: **escapar por defecto**, que es
lo que hacen las plantillas modernas.

```perl
use Template;                       # Template Toolkit
# [% nombre | html %]  ← el filtro de escape, explícito

# Y los marcos modernos:
use Mojolicious::Lite;
get '/pedidos' => sub { $_[0]->render(json => \@pedidos) };
```

**Mojolicious escapa por defecto** y hay que pedir explícitamente lo contrario — que es la forma correcta
de una API insegura: **que lo peligroso sea lo que hay que escribir**.

Y merece cerrar con la observación sobre la evolución del papel de este componente, que Perl vivió entera:

```text
1995: el servidor genera TODO el HTML. El navegador solo pinta.
2005: AJAX. El navegador pide trozos y actualiza partes.
2015: el navegador tiene la aplicación; el servidor solo da JSON.
2020: y vuelta parcial al servidor, por rendimiento y por accesibilidad.
```

**El péndulo ha ido y vuelto**, y lo que no ha cambiado en treinta años es la primera regla del cierre:
**la validación del servidor es la única que cuenta**.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>

int main() {
    long long n{};
    if (!(std::cin >> n)) return 1;

    std::cout << "items=" << n << " render=ok" << '\n';
    return 0;
}
```

**C++ y la capa de presentación.** C++ es, otra vez, **el suelo**: los navegadores, los motores de
renderizado y los kits gráficos están escritos en él.

```text
Chromium / Blink   →  C++
WebKit              →  C++
Gecko                →  C++ y Rust
Skia (el renderizador de Chrome y Android)  →  C++
Qt, wxWidgets, GTK (C)  →  los kits de escritorio
```

**Así que cuando esta clase habla del componente web, C++ está debajo aunque no aparezca.**

Y C++ sí llega al navegador directamente por la vía de la clase 162, con casos que merecen recordarse:
**Figma, AutoCAD web, Google Earth y los motores de juego**.

Y hay un modelo de interfaz que merece explicarse porque viene de los juegos y ha influido mucho: **la
interfaz de modo inmediato**.

```cpp
// Dear ImGui: la interfaz se DECLARA cada fotograma
if (ImGui::Begin("Pedidos")) {
    ImGui::Text("items=%d", (int)pedidos.size());
    if (ImGui::Button("Recargar")) recargar();
    ImGui::End();
}
```

**No hay objetos de widget que crear, guardar y destruir**: **cada fotograma se dice qué debe haber en
pantalla**, y la biblioteca lo pinta y devuelve los eventos.

Y merece señalar el parecido con la web moderna, porque es exactamente el mismo modelo:

```text
Modo inmediato (ImGui):  interfaz = f(estado), redibujada cada fotograma
React:                     interfaz = f(estado), reconciliada cada cambio
```

**Los dos parten de la misma observación: mantener sincronizados un árbol de objetos de interfaz y un
estado es la fuente de la mayoría de los fallos**, y es más simple **volver a declarar la interfaz
entera** y dejar que algo optimice la diferencia.

Es la tercera regla del cierre de esta clase —**separar el estado del pintado**— convertida en modelo de
programación, y aparece de forma independiente en dos mundos que apenas se hablan.

Y la contrapartida es la misma en los dos: **hay que redibujar o reconciliar**, y eso cuesta — que es la
razón de que existan el DOM virtual, los memos y los `shouldComponentUpdate`.

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

dcl-pi FRONTAL;
  n int(10) const;
end-pi;

dsply ('items=' + %char(n) + ' render=ok');

*inlr = *on;
return;
```

**RPG y la capa de presentación.** IBM i tiene su propia generación de pantallas —**los ficheros de
pantalla 5250**, hermanos de los mapas BMS de COBOL en esta página— y su modernización es un caso de
estudio de esta clase.

```text
     A          R PANTALLA1
     A                                  1  30'Pedidos'
     A            CLIENTE       10A  B  5 10CHECK(ME)
     A            IMPORTE        9Y 2B  7 10EDTCDE(J)
     A                                     ERRMSG('Cliente no válido' 51)
```

**Y de nuevo, la validación básica la hace el terminal** —`CHECK(ME)` obliga a rellenar, `EDTCDE` da el
formato— **y la de negocio, el programa**.

Y la modernización de esas pantallas ha pasado por tres fases que merecen conocerse porque el patrón se
repite en cualquier sistema heredado:

| Fase | Qué hace | Valoración |
|---|---|---|
| **1. Refaceado automático** | traduce la pantalla 5250 a HTML al vuelo | rápido, y **es la misma aplicación con otra piel** |
| **2. Reescribir la interfaz** | una web nueva que llama al programa por API | correcto, y **exige separar la lógica** (clase 149) |
| **3. Web nativa desde el principio** | lo nuevo se escribe web | lo ideal para lo que no existe |

**Y la fase 1 merece la advertencia**, porque es la tentación: **el refaceado no moderniza nada**. La
navegación sigue siendo por pantallas, el flujo sigue siendo el del terminal, y **el resultado suele
gustar menos que la pantalla verde** a quien ya sabía usarla.

**Y su único valor real es de transición**: permite enseñar algo mientras se hace la fase 2.

Y la fase 2 es la que esta parte del curso defiende, y su requisito previo es el de la clase 149:
**separar la lógica de la presentación** para poder llamarla desde otro sitio.

```rpgle
// La lógica, en un procedimiento exportado: la usan la pantalla 5250 Y la web
dcl-proc crearPedido export;
```

**Y con eso, las dos interfaces coexisten** durante los años que dure la transición — que es la propiedad
que hace la migración posible sin apagar nada, y es la segunda regla del cierre de esta clase: **el
frontal no conoce el sistema, conoce un contrato**.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 frontal: procedure options(main);

    declare n fixed binary(31);

    get list (n);

    put skip list ('items=' || trim(char(n)) || ' render=ok');

 end frontal;
```

**PL/I y la capa de presentación.** PL/I comparte el mundo de las pantallas de bloques con COBOL en esta
página, y esta clase es el sitio para explicar una propiedad de aquella arquitectura que merece
rescatarse, porque hoy se echa de menos: **la interacción por bloques**.

```text
Terminal 3270:
  - el usuario rellena TODA la pantalla
  - pulsa ENTER
  - y se transmite UNA vez, solo los campos modificados
  - el servidor procesa y devuelve la pantalla siguiente
```

**Y eso hacía que la aplicación fuera utilizable con 300 milisegundos de latencia** — porque **no había
comunicación mientras se teclea**.

Y merece comparar con lo que ocurre hoy:

```text
Un formulario web moderno puede hacer:
  - una petición por pulsación (autocompletado)
  - una validación por campo al salir de él
  - una comprobación de disponibilidad en tiempo real
  - y varias más para telemetría
```

**Y cada una es un viaje de ida y vuelta que puede fallar.**

Es una observación honesta: **la interfaz por bloques era menos agradable y mucho más robusta**, y la
gente que trabajaba con ella todo el día **era rapidísima**, porque **no había esperas intermedias ni
elementos que se movían**.

Y la lección transferible, que es una de las más útiles de esta clase: **la interactividad tiene un
coste, y conviene decidirlo en lugar de heredarlo**.

Un formulario que valida al enviar es más simple, más rápido de rellenar con teclado y **no deja al
usuario a medias si se cae la red**. Uno que valida campo a campo es más amable para quien no conoce el
dominio.

**Las dos son decisiones legítimas, y depende de quién lo use y cuántas veces al día.**

Y merece cerrar con el dato que lo confirma y que este mundo conoce bien: **en aplicaciones de uso
intensivo** —un centro de atención telefónica, una mesa de contratación, una consulta médica— **los
usuarios expertos prefieren teclado y pantallas densas**, y las modernizaciones que las sustituyen por
interfaces amables con muchos clics **suelen empeorar la productividad**.

Es la primera pregunta que un componente de frontal debería hacerse: **¿quién lo va a usar, y cuántas
horas al día?**

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
FRONTAL ; Componente web -- clase 169
 read n
 write "items=", n, " render=ok", !
 quit
```

**M y la capa de presentación.** El mundo VistA vivió la transición de esta clase de forma muy visible, y
merece contarla porque las tres generaciones conviven hoy en los mismos hospitales.

```text
1980s  Terminal de texto, con menús de FileMan  ← todavía en uso
2000s  CPRS: cliente Delphi, hablando por el RPC Broker (clase 168)
2010s+ Web y móvil, sobre FHIR (clase 160)
```

**Y la observación que merece hacerse es la de la columna de PL/I en esta página, y aquí es un hecho
documentado**: **muchos clínicos veteranos prefieren la interfaz de texto**.

```text
La razón no es nostalgia: es que en la pantalla de texto
  - todo está en un sitio fijo, siempre
  - se navega con teclado, sin ratón
  - y una orden de diez pasos se teclea en cinco segundos
```

**Y las interfaces gráficas que las sustituyeron a menudo requerían más clics para lo mismo.**

Es un caso real y bien estudiado, y la lección es la del cierre de esta clase aplicada al diseño: **la
interfaz se diseña para quien la usa, no para quien la compra**.

Y esta clase debe recoger la aportación técnica que este dominio ha hecho y que resuelve la segunda regla
del cierre mejor que la mayoría: **SMART on FHIR**.

```text
Una aplicación clínica de terceros:
  - se autentica con OAuth2 contra el sistema del hospital
  - pide los datos del paciente por FHIR, con permisos acotados
  - y se muestra DENTRO de la historia clínica, como un componente
```

**Es un modelo de complementos con contrato estándar y permisos explícitos** (clase 153), y funciona entre
fabricantes distintos.

**Y eso es exactamente lo que la segunda regla del cierre pide**: el frontal —aquí, una aplicación
entera— **no conoce el sistema, conoce un contrato**, así que **la misma aplicación funciona sobre VistA,
sobre Epic o sobre Cerner**.

Es uno de los pocos ecosistemas donde la interoperabilidad de componentes de interfaz entre fabricantes
funciona de verdad, y merece conocerse como modelo.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| n |

n := stdin nextLine trimBoth asNumber.

Transcript show: 'items=', n printString, ' render=ok'; cr.
```

**Smalltalk y la capa de presentación.** Y aquí conviene decir lo que esta parte del curso ha ido
repitiendo, porque en esta clase es el origen directo: **la interfaz gráfica con ventanas, iconos, menús
y ratón se inventó en Smalltalk**.

```text
Xerox PARC, Smalltalk-76 y Smalltalk-80:
  - ventanas solapadas y redimensionables
  - menús emergentes
  - el ratón como dispositivo principal
  - copiar y pegar entre aplicaciones
  - el portapapeles
  - y MVC para organizarlo todo (clase 149)
```

**Steve Jobs visitó PARC en 1979, vio Smalltalk funcionando, y de ahí salieron el Lisa y el Macintosh** —
y de ahí, Windows y todo lo demás.

**Cada ventana que se abre hoy en cualquier sistema desciende de eso.**

Y merece señalar la idea de aquel diseño que esta clase debe destacar y que sigue siendo la mejor
respuesta a la tercera regla del cierre: **el modelo no sabe que existe la vista**.

```smalltalk
modelo addDependent: vista.
modelo changed: #total.        "el modelo AVISA; no sabe a quién"
```

**Separar el estado de negocio del estado de la interfaz** es lo que permite tener dos vistas del mismo
dato, deshacer, probar el modelo sin interfaz y cambiar la presentación sin tocar la lógica.

Y Smalltalk llega hoy al navegador por caminos reales:

| Proyecto | Qué es |
|---|---|
| **Seaside** | el marco de continuaciones (clase 168) |
| **Amber / PharoJS** | Smalltalk **compilado a JavaScript** |
| **SqueakJS** | la máquina virtual en el navegador (clase 162) |
| **Scratch** | **construido sobre Squeak**: el lenguaje visual del MIT |

**Y Scratch merece cerrar esta clase**, porque es el descendiente más directo del propósito original de
PARC: **que personas que no son programadores construyan cosas**.

Decenas de millones de niños han escrito su primer programa en un entorno **que nació como una aplicación
Smalltalk**, arrastrando bloques en una interfaz que desciende, en línea recta, de las mismas ideas de
1979.

Es la mejor forma de terminar una clase sobre la capa de presentación: **la interfaz gráfica no se
inventó para hacer bonito el software — se inventó para que más gente pudiera usarlo y modificarlo**, y
ese sigue siendo el criterio con el que conviene juzgarla.

---

## Y de vuelta a la clase

Lo transferible: **la validación del cliente es comodidad; la del servidor es la única real** (clase 153).
Todo lo que se comprueba en el navegador se puede saltar, así que **se comprueba dos veces o no se
comprueba**. Y las otras dos reglas que atraviesan la página: **el frontal no debe conocer la estructura
interna del sistema**, sino un contrato (clase 160), porque es el componente que más cambia y no puede
arrastrar a los demás; y **el estado de la interfaz es del cliente y el de negocio es del servidor** —
mezclarlos es el origen de la mayoría de los fallos difíciles de una aplicación web.

⏮️ [Volver a la clase 169](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
