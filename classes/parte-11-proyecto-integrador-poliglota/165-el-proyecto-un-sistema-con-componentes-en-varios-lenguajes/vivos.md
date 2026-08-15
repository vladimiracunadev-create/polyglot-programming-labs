# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 165

> [⬅️ Volver a la clase 165](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Contar los componentes y nombrarlos: `componentes=3 nombres=cli-api-web`. Es el inventario de un
sistema, y con él abre la parte final del curso. Y estos doce lenguajes tienen algo que decir aquí que
ningún lenguaje moderno puede decir: **saben cómo se ve un sistema poliglota a los treinta años**,
porque llevan ahí. La pregunta de esta parte no es qué componentes tendría el proyecto, sino **cuál
sería el papel de cada uno de estos lenguajes en él**.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es el **sistema como conjunto de componentes con dueño**, y estos lenguajes lo enseñan
> porque **no son candidatos hipotéticos: son los que ocupan esos papeles hoy en los sistemas grandes del
> mundo**. El componente de lote es COBOL. El núcleo numérico es Fortran. El control crítico es Ada. El
> motor es C++. El pegamento es Tcl o Perl. Y la lógica de gestión, RPG.
>
> Y aparece la pregunta que esta parte va a responder clase a clase: **¿por qué ese reparto y no otro?**
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: una línea con nombres de componentes (palabras) → stdout: `componentes=<N> nombres=<unidos por ->`
- **Regla:** `contar y listar los componentes`

| stdin | esperado |
|---|---|
| `cli api web` | `componentes=3 nombres=cli-api-web` |
| `app` | `componentes=1 nombres=app` |
| `web api datos cache` | `componentes=4 nombres=web-api-datos-cache` |

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
PROGRAM-ID. INVENT.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(200).
01  I       PIC 9(4) COMP.
01  CNT     PIC 9(4) COMP VALUE 0.
01  ENPAL   PIC 9      VALUE 0.
01  SALIDA  PIC X(200).
01  POSIC   PIC 9(4) COMP VALUE 1.
01  ED      PIC -(3)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    MOVE SPACES TO SALIDA

    PERFORM VARYING I FROM 1 BY 1 UNTIL I > 200
        IF LINEA(I:1) = SPACE
            IF ENPAL = 1
                MOVE 0 TO ENPAL
            END-IF
        ELSE
            IF ENPAL = 0
                MOVE 1 TO ENPAL
                ADD 1 TO CNT
                IF CNT > 1
                    MOVE "-" TO SALIDA(POSIC:1)
                    COMPUTE POSIC = POSIC + 1
                END-IF
            END-IF
            MOVE LINEA(I:1) TO SALIDA(POSIC:1)
            COMPUTE POSIC = POSIC + 1
        END-IF
    END-PERFORM

    MOVE CNT TO ED
    DISPLAY "componentes=" FUNCTION TRIM(ED)
            " nombres=" FUNCTION TRIM(SALIDA)
    STOP RUN.
```

**El papel de COBOL en el sistema.** En un sistema real, COBOL es **el componente de lote y el de la
lógica de negocio validada**.

```text
┌──────────────────────────────────────────────────────┐
│  Web / móvil            (TypeScript, Swift, Kotlin)  │
├──────────────────────────────────────────────────────┤
│  API                     (Java, Node, Go...)          │
├──────────────────────────────────────────────────────┤
│  ►  Lógica de negocio y lote   (COBOL)                │
├──────────────────────────────────────────────────────┤
│  Base de datos           (DB2, Oracle)                │
└──────────────────────────────────────────────────────┘
```

**Y merece precisar qué hace exactamente**, porque la caricatura del "sistema COBOL" no ayuda:

| Responsabilidad | Por qué COBOL |
|---|---|
| **Cierre diario, mensual y anual** | procesa millones de registros en una ventana fija (clase 152) |
| **Cálculo de intereses, comisiones y saldos** | decimal exacto (clase 045) |
| **Aplicación de las reglas normativas** | están implementadas y auditadas ahí |
| **Conciliación y contabilidad** | idem, con treinta años de casos particulares |

**Lo que COBOL NO hace en un sistema moderno**: la interfaz, la API, la autenticación, la mensajería, la
observabilidad. **Todo eso está fuera y habla con él** por una frontera declarada (clase 160).

Y el dato del inventario que el cierre de esta clase pide y que en estos sistemas suele estar peor: **el
dueño**.

En muchos sistemas COBOL de banca, **el componente lo mantienen dos o tres personas cercanas a la
jubilación** (clase 154), y **eso es un riesgo de continuidad de negocio**, no un problema técnico.

**Y por eso la primera tarea de un proyecto sobre un sistema así no es tecnológica: es documentar quién
sabe qué, y por qué las reglas son como son.**

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program invent
   implicit none
   character(len=200) :: linea, salida
   integer :: i, cnt
   logical :: en_palabra

   read(*, '(A)') linea
   cnt = 0
   salida = ''
   en_palabra = .false.

   do i = 1, len_trim(linea)
      if (linea(i:i) == ' ') then
         en_palabra = .false.
      else
         if (.not. en_palabra) then
            en_palabra = .true.
            cnt = cnt + 1
            if (cnt > 1) salida = trim(salida) // '-'
         end if
         salida = trim(salida) // linea(i:i)
      end if
   end do

   write(*, '(A,I0,A)') 'componentes=', cnt, ' nombres=' // trim(salida)
end program invent
```

**El papel de Fortran en el sistema.** Fortran es **el núcleo de cálculo**, y su frontera está bien
definida desde hace décadas (clase 155).

```text
Interfaz / cuaderno       →  Python, JavaScript
Orquestación y datos       →  Python
►  Núcleo numérico          →  FORTRAN
Bibliotecas de álgebra       →  Fortran y ensamblador (BLAS, LAPACK)
Comunicación                  →  MPI
Almacenamiento                 →  NetCDF, HDF5 (clase 159)
```

**Y la frontera es gruesa a propósito**: una llamada cruza y dentro se hacen millones de operaciones.

Y merece señalar el dato del inventario que este dominio hace visible mejor que ninguno y que el cierre
de esta clase pide: **quién lo mantiene**.

```text
Un modelo de simulación típico tiene:
  - un autor original, que hizo su tesis con él, y que ya no está
  - dos o tres personas que han añadido módulos
  - y ningún ingeniero de software
```

Y de ahí que el componente de cálculo sea, casi siempre, **el mejor validado científicamente y el peor
mantenido como software**: sin pruebas (clase 139), sin construcción reproducible (clase 144) y con el
conocimiento en personas.

**Y esa es la aportación de esta parte del curso a este dominio**: no reescribir el cálculo —está bien y
está validado— sino **ponerle alrededor lo que le falta**: pruebas de caracterización, un contenedor con
el entorno, un contrato de datos y un dueño identificado.

Es la misma receta que COBOL en esta página, con otro vocabulario: **el componente que funciona se
respeta; lo que se añade es la ingeniería alrededor**.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;           use Ada.Text_IO;
with Ada.Strings;
with Ada.Strings.Fixed;
with Ada.Strings.Unbounded; use Ada.Strings.Unbounded;

procedure Invent is
   Linea      : String (1 .. 200);
   Ultimo     : Natural;
   Cnt        : Natural := 0;
   En_Palabra : Boolean := False;
   Salida     : Unbounded_String;
begin
   Get_Line (Linea, Ultimo);

   for I in 1 .. Ultimo loop
      if Linea (I) = ' ' then
         En_Palabra := False;
      else
         if not En_Palabra then
            En_Palabra := True;
            Cnt := Cnt + 1;
            if Cnt > 1 then
               Append (Salida, "-");
            end if;
         end if;
         Append (Salida, Linea (I));
      end if;
   end loop;

   Put_Line ("componentes=" &
             Ada.Strings.Fixed.Trim (Cnt'Image, Ada.Strings.Both) &
             " nombres=" & To_String (Salida));
end Invent;
```

**El papel de Ada en el sistema.** Ada es **el componente crítico**, y en un sistema real ocupa una zona
pequeña, muy delimitada y rodeada de otras cosas.

```text
Interfaz de operador / análisis en tierra  →  Python, C#, web
Registro, telemetría, simulación             →  C++, Python
►  Control, seguridad y tiempo real          →  ADA / SPARK
Controladores de dispositivo                   →  C
Arranque y vectores de interrupción              →  ensamblador
```

**Y la frontera está donde está el requisito de certificación**: lo que hay que demostrar está en Ada; lo
que no, en lo que sea más productivo.

Y merece explicar la propiedad que hace ese reparto posible y que es específica de este dominio: **la
separación por criticidad**.

```text
DAL A (un fallo es catastrófico)   →  Ada/SPARK, con MC/DC y demostración
DAL C (un fallo es mayor)           →  Ada o C con MISRA
DAL E (sin efecto en la seguridad)   →  cualquier cosa
```

**Y la separación tiene que estar garantizada por la arquitectura**, no por buena voluntad: **particiones
de memoria y de tiempo** —ARINC 653 en aviónica— **para que un componente no crítico no pueda afectar a
uno crítico**.

Es la versión más estricta de lo que el cierre de esta clase llama frontera: **no basta con que los
componentes estén separados en el diagrama; el sistema tiene que impedir que se toquen**.

Y es una idea que merece transferirse fuera de la aviónica, porque casi ningún sistema la aplica y varios
la necesitan: **si un componente puede agotar la memoria, la CPU o el disco que otro necesita, no están
realmente separados** — y ahí es donde los contenedores con límites y WebAssembly (clase 162) están
llegando por otro camino.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Invent;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  Linea, Salida: string;
  I, Cnt: Integer;
  EnPalabra: Boolean;

begin
  ReadLn(Linea);
  Cnt := 0;
  Salida := '';
  EnPalabra := False;

  for I := 1 to Length(Linea) do
    if Linea[I] = ' ' then
      EnPalabra := False
    else
    begin
      if not EnPalabra then
      begin
        EnPalabra := True;
        Inc(Cnt);
        if Cnt > 1 then Salida := Salida + '-';
      end;
      Salida := Salida + Linea[I];
    end;

  WriteLn('componentes=', IntToStr(Cnt), ' nombres=', Salida);
end.
```

**El papel de Object Pascal en el sistema.** Pascal es **el componente de escritorio**, y merece
describirlo porque es una zona que muchos sistemas modernos han descuidado y que sigue existiendo.

```text
Servidores y API           →  lo que sea
►  Aplicación de escritorio →  DELPHI / LAZARUS
Punto de venta, laboratorio, taller, control de planta
Integración local           →  puertos serie, dispositivos, impresoras fiscales
```

**Y ese componente tiene requisitos que la web no cubre bien**, y merece enumerarlos porque explican por
qué sigue habiendo aplicaciones de escritorio:

| Requisito | Por qué la web no basta |
|---|---|
| **Hardware local** | balanzas, lectores, impresoras fiscales, tornos, PLC |
| **Funcionar sin red** | una caja de supermercado no puede parar |
| **Arranque instantáneo** | y sin instalar un navegador entero |
| **Impresión precisa** | etiquetas, cheques, formularios con posiciones |

Y el dato del inventario que este componente suele tener bien y que merece señalar: **el dueño está
claro**, porque **la aplicación de escritorio es visible para el usuario final**, así que cuando falla se
sabe a quién llamar.

Es lo contrario del componente de lote o del núcleo numérico de esta página, que fallan de madrugada y en
silencio.

Y hay una decisión de arquitectura que este componente obliga a tomar y que el resto de la parte
retomará: **cuánta lógica vive en el cliente**.

```text
Cliente "tonto":  toda la lógica en el servidor. Fácil de actualizar (clase 148).
                  Inútil sin red.
Cliente "gordo":  lógica en el escritorio. Funciona sin red.
                  Y hay que desplegar en 4.000 puestos.
```

**Y la respuesta habitual es la intermedia y la más difícil**: **la lógica crítica duplicada en los dos
sitios**, con el riesgo de la clase 140 —que las dos versiones divergan— que solo se controla con un
verificador de equivalencia.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let ((linea (read-line))
      (cnt 0)
      (piezas '())
      (actual '()))
  (loop for c across linea
        do (if (char= c #\Space)
               (when actual
                 (push (coerce (nreverse actual) 'string) piezas)
                 (setf actual nil))
               (push c actual)))
  (when actual (push (coerce (nreverse actual) 'string) piezas))
  (setf piezas (nreverse piezas)
        cnt (length piezas))
  (format t "componentes=~D nombres=~{~A~^-~}~%" cnt piezas))
```

**El papel de Common Lisp en el sistema.** Lisp ocupa, cuando está, **el componente de lógica compleja o
de exploración**, y su reparto merece explicarse porque no es el que se supone.

```text
Interfaz, API, persistencia   →  lo convencional del equipo
►  Motor de reglas, planificador, optimizador, analizador  →  LISP
```

**Y la razón es la de la clase 149**: cuando el problema tiene **muchas reglas que cambian y que las
escribe gente del dominio**, un lenguaje donde se puede construir el vocabulario del problema gana.

Y los casos reales lo confirman: **planificación, configuración de productos complejos, motores de
tarificación, análisis de lenguaje natural clásico y sistemas de demostración**.

Y merece señalar el riesgo del inventario en este caso, porque es el mayor de esta página: **el
componente Lisp suele tener un solo dueño**.

```text
Lo escribió alguien muy bueno, con macros a medida y un vocabulario propio.
Funciona extraordinariamente bien.
Y cuando esa persona se va, nadie más lo entiende.
```

**Es el escenario clásico**, y la responsabilidad no es del lenguaje: **es de haber permitido que un
componente crítico tuviera un único dueño** (clase 154).

Y las mitigaciones que funcionan y que esta parte del curso ya ha ido nombrando:

| Práctica | Clase |
|---|---|
| **Documentar el porqué**, no el qué | 154 |
| **Macros solo cuando una función no basta** | 122, 150 |
| **Pruebas que sirvan de especificación** | 139 |
| **Y una frontera clara**: el resto del sistema no ve Lisp | 160 |

**La última es la que de verdad protege**: si el componente se comunica por una API bien definida,
**puede reescribirse en otra cosa el día que haga falta** sin tocar el resto — que es exactamente el
argumento del cierre de esta clase sobre las fronteras.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea
set comps [split [string trim $linea]]

puts "componentes=[llength $comps] nombres=[join $comps -]"
```

**El papel de Tcl en el sistema.** Tcl es **el pegamento**, y en el proyecto de esta parte ocuparía un
sitio muy concreto (clases 155 y 163).

```text
►  Guiones de construcción, despliegue y automatización  →  TCL
►  Lenguaje de configuración de las herramientas propias   →  TCL incrustado
►  Pruebas de sistema que orquestan varios procesos         →  TCL
```

**Y merece justificar por qué ese papel y no otro**, con el argumento que la clase 155 desarrolló: **el
90 % de los cambios de un sistema ocurren en el pegamento**, así que conviene que esa capa esté en algo
donde un cambio cueste minutos.

Y hay una capacidad de Tcl que lo hace especialmente bueno para el componente de pruebas de sistema
(clase 173), y merece destacarla:

```tcl
# Arrancar tres componentes, esperar a que estén listos, probar, y parar
set apiPid [exec ./api --puerto 8080 &]
set webPid [exec ./web --api http://localhost:8080 &]

# Esperar a que respondan, sin dormir a ciegas
esperarPuerto 8080 -timeout 30

# Ejecutar la prueba
set r [exec curl -s http://localhost:8080/pedidos/1]
if {[dict get [json::json2dict $r] total] != 100} { error "mal" }

# Y limpiar SIEMPRE
exec kill $apiPid $webPid
```

**Ese guion es exactamente el componente de automatización del proyecto**, y en Tcl cabe en una página.

Y el dato del inventario que este componente tiene peor y que merece la advertencia: **el pegamento suele
no tener dueño**.

**Los guiones de construcción, despliegue y pruebas se escriben deprisa, no se revisan** (clase 146) **y
nadie los mantiene** — hasta que uno falla en el peor momento.

Y la recomendación de esta parte es incómoda y correcta: **el pegamento es código de producción**. Tiene
que estar en el repositorio, revisado, con dueño y —cuando es crítico— con pruebas.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;

my @comps = split ' ', $linea;

print "componentes=", scalar(@comps), " nombres=", join('-', @comps), "\n";
```

**El papel de Perl en el sistema.** Perl ocupa, en los sistemas reales donde está, **el componente de
transformación de datos y de integración**.

```text
Sistema A (formato propio)  →  ►  PERL  →  Sistema B (otro formato)
Registros y ficheros            →  ►  PERL  →  métricas y avisos
Datos de laboratorio             →  ►  PERL  →  base de datos
```

**Y es un papel real y muy extendido**, aunque casi nunca aparezca en el diagrama de arquitectura: **el
proceso que a las tres de la mañana convierte un fichero que llega de un proveedor en filas de una
tabla**.

Y merece nombrar el patrón porque tiene nombre y es el 80 % de la integración empresarial: **ETL**
—extraer, transformar y cargar—.

| Fase | Lo que hace Perl bien |
|---|---|
| **Extraer** | leer cualquier formato de texto, por raro que sea (clase 093) |
| **Transformar** | expresiones regulares, estructuras anidadas, decisiones por fila |
| **Cargar** | DBI, con transacciones (clase 158) |

Y este componente tiene un problema de inventario específico que merece la advertencia, porque es la
forma de deuda de la clase 154 en su versión más común:

```text
Empieza como un guion de 50 líneas para "convertir este fichero".
Se le añaden casos particulares: este proveedor, aquel formato, esa excepción.
Diez años después: 6.000 líneas, sin pruebas, y es crítico.
```

**Y la señal de alarma es la de siempre: "no toques eso".**

Y la receta de esta parte del curso para un componente así es concreta y funciona:

**Uno, pruebas de caracterización** con ficheros reales y sus salidas (clase 150). **Dos, ponerle una
frontera**: que la entrada y la salida sean contratos declarados (clase 160). **Y tres, un dueño**,
aunque sea a regañadientes.

Con esas tres cosas, el componente **se puede refactorizar o reescribir cuando convenga**; sin ellas, **no
se puede tocar y nadie se atreve**.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>
#include <string>
#include <vector>

int main() {
    std::vector<std::string> comps;
    std::string c;
    while (std::cin >> c) comps.push_back(c);

    std::cout << "componentes=" << comps.size() << " nombres=";
    for (std::size_t i = 0; i < comps.size(); ++i) {
        if (i) std::cout << '-';
        std::cout << comps[i];
    }
    std::cout << '\n';
    return 0;
}
```

**El papel de C++ en el sistema.** C++ es **el motor**: el componente donde el rendimiento o el control
son el requisito, y **es también el suelo sobre el que corren varios de los demás** (clase 155).

```text
Interfaz              →  TypeScript, Qt/QML
API y orquestación     →  Go, Java, Python
►  Motor                →  C++  (procesado, renderizado, simulación, indexado)
Aceleración              →  CUDA, SIMD, ensamblador
```

**Y la frontera de C++ en un sistema poliglota tiene una forma característica** que la Parte 10 explicó:
**una interfaz en C con punteros opacos** (clase 156), o **un proceso separado con un protocolo**.

Y merece plantear la decisión concreta, porque es la que un proyecto tiene que tomar:

| Opción | A favor | En contra |
|---|---|---|
| **Biblioteca cargada en el proceso** | rápido: sin serializar | **un fallo tumba todo** (clase 153) |
| **Proceso separado con socket o tubería** | **aislado**: si cae, se reinicia | serialización y latencia |
| **Módulo WebAssembly** | aislado **y** en proceso (clase 162) | rendimiento algo menor |

**La segunda fila es la que gana casi siempre en sistemas de negocio**, y merece explicar por qué: **un
error de memoria en C++ no es un error, es un comportamiento indefinido** (clase 136), y **dentro del
proceso puede corromper cualquier cosa**.

**Aislarlo en un proceso convierte un fallo catastrófico en un reinicio.**

Es una decisión de arquitectura que compra fiabilidad con latencia, y es exactamente el tipo de
compromiso que esta parte del curso pide razonar en lugar de heredar.

Y el dato del inventario que este componente suele tener mejor que los demás de esta página: **hay más
gente que sabe C++**, así que el riesgo de dueño único es menor.

**Y a cambio tiene el peor riesgo de complejidad acumulada** (clase 154): C++ permite tantos estilos que
un motor de quince años **contiene cuatro generaciones del lenguaje a la vez**, y entenderlo requiere
conocerlas todas.

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

dcl-pi INVENT;
  linea char(200) const;
end-pi;

dcl-s i      int(10);
dcl-s cnt    int(10);
dcl-s enpal  ind;
dcl-s salida varchar(200);
dcl-s c      char(1);

cnt = 0;
enpal = *off;
salida = '';

for i = 1 to %len(%trimr(linea));
  c = %subst(linea : i : 1);
  if c = ' ';
    enpal = *off;
  else;
    if not enpal;
      enpal = *on;
      cnt += 1;
      if cnt > 1;
        salida += '-';
      endif;
    endif;
    salida += c;
  endif;
endfor;

dsply ('componentes=' + %char(cnt) + ' nombres=' + salida);

*inlr = *on;
return;
```

**El papel de RPG en el sistema.** RPG es **el componente de gestión**: pedidos, inventario, facturación,
nóminas — la lógica que mueve una empresa.

```text
Web y móvil            →  React, Angular, aplicaciones nativas
API REST                →  IWS o Node, sobre la misma máquina (clase 160)
►  Lógica de gestión     →  RPG, en programas de servicio (clase 149)
Base de datos             →  Db2 for i, integrada en el sistema
Lote y orquestación        →  CL, planificado por el sistema
```

**Y la particularidad de este componente frente a los demás de esta página es que su plataforma le da
gratis lo que otros montan**: base de datos, seguridad, registro, colas, planificación y despliegue
(clases 142, 148 y 161).

Y por eso el inventario de un sistema IBM i tiene una forma peculiar y merece señalarla: **muchos
componentes que en otros sistemas son piezas separadas, aquí no existen como tales**.

```text
En un sistema típico:        En IBM i:
  base de datos                 el sistema operativo
  gestor de colas                el sistema operativo
  planificador                    el sistema operativo
  sistema de registro              el sistema operativo
  gestor de identidades             el sistema operativo
```

**Eso reduce drásticamente el número de piezas que hay que integrar, versionar y vigilar** — que es la
ventaja operativa real de las plataformas integradas (clase 164).

**Y el coste es la dependencia de un proveedor único**, que es una decisión estratégica y no técnica.

Y el dato del inventario que aquí es crítico y que la clase 154 ya nombró: **el dueño**.

**Este componente suele tener treinta años, funcionar perfectamente y mantenerlo dos personas.** Y la
tarea urgente no es modernizar el código: **es capturar por qué las reglas son como son**, antes de que
se vayan quienes lo saben.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 invent: procedure options(main);

    declare linea  char(200) varying;
    declare salida char(200) varying initial('');
    declare i      fixed binary(31);
    declare cnt    fixed binary(31) initial(0);
    declare enpal  bit(1) initial('0'b);
    declare c      char(1);

    get edit (linea) (a(200));

    do i = 1 to length(linea);
       c = substr(linea, i, 1);
       if c = ' ' then
          enpal = '0'b;
       else
          do;
             if ^enpal then
                do;
                   enpal = '1'b;
                   cnt = cnt + 1;
                   if cnt > 1 then salida = salida || '-';
                end;
             salida = salida || c;
          end;
    end;

    put skip list ('componentes=' || trim(char(cnt)) || ' nombres=' || salida);

 end invent;
```

**El papel de PL/I en el sistema.** PL/I ocupa, donde está, **el mismo sitio que COBOL** —lógica de
negocio y lote— con un matiz que merece explicarse: **suele estar en los sistemas con más cálculo**.

```text
Donde hay PL/I en producción hoy:
  - seguros: cálculo actuarial, reservas técnicas, siniestros
  - banca: tesorería, riesgo, valoración de instrumentos
  - logística y transporte: optimización de rutas y de carga
  - administraciones públicas: liquidaciones y padrones
```

**Y el motivo histórico es el de la clase 155**: cuando había que elegir, **COBOL se llevó lo comercial y
Fortran lo científico; PL/I se quedó con lo que era las dos cosas** — cálculo intensivo sobre datos
comerciales.

Y merece señalar la decisión que un proyecto sobre un sistema PL/I tiene que tomar y que es distinta de
la de COBOL, por la razón de la clase 162: **no hay implementación libre**.

```text
COBOL:  hay GnuCOBOL, así que la lógica se puede compilar y probar fuera del mainframe.
PL/I:   no. Probar exige el compilador propietario y la plataforma.
```

**Eso cambia la estrategia de modernización**: donde con COBOL se puede montar una integración continua
barata (clase 147), con PL/I hay que hacerlo contra el sistema real.

Y por eso, en la práctica, **los proyectos sobre sistemas PL/I tienden a la traducción** —a Java, a C# o
a COBOL— más que los de COBOL, que tienden a la encapsulación.

Y esta parte del curso tiene una recomendación concreta para ese caso, que es la de la clase 150: **el
patrón del estrangulador con verificador de equivalencia** (clase 140).

**No traducir el sistema entero: traducir un programa, ejecutarlo en paralelo comparando salidas durante
meses, y solo entonces apagar el viejo** — y repetir. Es lento, y es lo que funciona.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
INVENT ; Inventario de componentes -- clase 165
 read linea
 new i, cnt, p, salida
 set cnt = 0, salida = ""
 for i = 1:1:$length(linea, " ") do
 . set p = $piece(linea, " ", i)
 . if p '= "" do
 . . set cnt = cnt + 1
 . . set salida = $select(salida = "" : p, 1 : salida _ "-" _ p)
 write "componentes=", cnt, " nombres=", salida, !
 quit
```

**El papel de M en el sistema.** M es **el componente de datos clínicos y su lógica**, y su reparto en un
sistema sanitario real merece verse porque es peculiar (clase 155):

```text
Aplicación clínica (web o escritorio)  →  JavaScript, Delphi, .NET
Interoperabilidad                        →  FHIR, HL7 (clase 160)
Analítica y aprendizaje automático        →  Python, R
►  Núcleo clínico y datos                  →  M + FileMan
Integración                                 →  motores de interfaces (Mirth, Rhapsody)
```

**Y lo que distingue este reparto es que el componente M es a la vez la base de datos y la lógica**
(clase 149): no hay separación entre uno y otro, y esa es su fuerza y su límite.

Y merece nombrar el riesgo de inventario que este dominio tiene y que no es técnico: **la criticidad**.

```text
Un fallo en el componente de facturación es un problema.
Un fallo en el módulo de prescripción es una dosis equivocada.
```

**Y por eso las prácticas de este ecosistema son conservadoras hasta un punto que desde fuera parece
excesivo** —parches numerados, sumas de comprobación por rutina, entornos de prueba obligatorios (clases
144 y 148)— **y no lo es**.

Y la aportación de esta parte del curso a un sistema así es la misma de siempre y merece decirla: **poner
fronteras y contratos donde hoy hay acoplamiento**.

**FHIR es exactamente eso** (clase 160): un contrato estándar que permite que la analítica, la aplicación
móvil y el sistema del hospital vecino hablen con el núcleo **sin conocer sus globals**.

Y eso, además de interoperabilidad, compra lo que el cierre de esta clase pide: **la posibilidad de
cambiar un componente sin tocar el resto** — que en un sistema de cuarenta años es la única forma de
evolucionar sin reescribir.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| linea comps |

linea := stdin nextLine trimBoth.
comps := linea substrings: ' '.

Transcript
    show: 'componentes=', comps size printString;
    show: ' nombres=', (comps inject: '' into: [ :a :b |
        a isEmpty ifTrue: [ b ] ifFalse: [ a, '-', b ] ]);
    cr.
```

**El papel de Smalltalk en el sistema.** Smalltalk ocupa, cuando está, **el componente de modelo de
dominio complejo** — y merece explicar por qué ese y no otro.

```text
Interfaz              →  web
API                    →  Zinc o Teapot, o un servidor delante
►  Modelo de dominio    →  SMALLTALK
Persistencia             →  GemStone, o una base relacional con mapeo
```

**Y la razón es la de la clase 149**: cuando el dominio es complejo y cambia —seguros, logística,
finanzas—, **modelarlo con objetos vivos que se pueden inspeccionar y modificar en marcha es
extraordinariamente productivo**.

Y esta parte del curso permite añadir el papel que Smalltalk ocupa hoy con más frecuencia y que es
distinto: **la herramienta de análisis del sistema, no el sistema**.

```text
Moose importa el código de TODOS los demás componentes
  —Java, C++, COBOL, Python—
como objetos Smalltalk, y permite:
  - medir, visualizar y navegar el sistema entero
  - encontrar dependencias cíclicas y código muerto (clase 154)
  - y hacer preguntas que ninguna herramienta estándar responde
```

**Es un uso poco conocido y muy potente**: el lenguaje que mejor representa cosas como objetos, aplicado
a representar **el propio sistema**.

Y merece cerrar esta clase señalando la aportación de Smalltalk al inventario que el cierre pide, porque
es una capacidad literal:

```smalltalk
SystemNavigation default allClasses size.
SystemNavigation default allUnsentMessages.
(RPackageOrganizer default packages) collect: [ :p | p name -> p classes size ].
```

**El sistema puede responder a "¿qué componentes tengo, cuánto ocupan y qué no usa nadie?"** — sin
herramientas externas y sin analizar texto.

Es la mejor ilustración de la idea que abre esta parte: **un sistema que se puede inspeccionar es un
sistema que se puede gobernar**, y todo lo que esta parte va a construir —contratos, pruebas, despliegue,
documentación— existe para conseguir eso en sistemas que no lo traen de fábrica.

---

## Y de vuelta a la clase

Lo transferible: **un sistema se entiende por sus componentes y por sus fronteras, no por su lenguaje**.
El inventario útil de un sistema poliglota tiene, por cada componente, cuatro datos: **qué hace, en qué
está escrito, con quién habla y quién lo mantiene**. Y el cuarto es el que más veces falta y el que más
caro sale: **un componente sin dueño identificable es deuda técnica esperando a manifestarse** (clase
154). Lo demás —el lenguaje, el marco, el estilo— se puede cambiar; **el reparto de responsabilidades y
la persona que responde, no**.

⏮️ [Volver a la clase 165](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
