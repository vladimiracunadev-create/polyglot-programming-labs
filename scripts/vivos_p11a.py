# -*- coding: utf-8 -*-
"""Parte 11, lote A — clases 165 a 167. Ver `vivos_parte11.py` y `gen_vivos.py`."""

SPECS: dict[str, dict] = {}

# ---------------------------------------------------------------------------
# 165 — El proyecto: un sistema con componentes en varios lenguajes
# ---------------------------------------------------------------------------
SPECS["165"] = dict(
    gancho="""
Contar los componentes y nombrarlos: `componentes=3 nombres=cli-api-web`. Es el inventario de un
sistema, y con él abre la parte final del curso. Y estos doce lenguajes tienen algo que decir aquí que
ningún lenguaje moderno puede decir: **saben cómo se ve un sistema poliglota a los treinta años**,
porque llevan ahí. La pregunta de esta parte no es qué componentes tendría el proyecto, sino **cuál
sería el papel de cada uno de estos lenguajes en él**.
""",
    porque="""
Aquí el concepto es el **sistema como conjunto de componentes con dueño**, y estos lenguajes lo enseñan
porque **no son candidatos hipotéticos: son los que ocupan esos papeles hoy en los sistemas grandes del
mundo**. El componente de lote es COBOL. El núcleo numérico es Fortran. El control crítico es Ada. El
motor es C++. El pegamento es Tcl o Perl. Y la lógica de gestión, RPG.

Y aparece la pregunta que esta parte va a responder clase a clase: **¿por qué ese reparto y no otro?**
""",
    cierre="""
Lo transferible: **un sistema se entiende por sus componentes y por sus fronteras, no por su lenguaje**.
El inventario útil de un sistema poliglota tiene, por cada componente, cuatro datos: **qué hace, en qué
está escrito, con quién habla y quién lo mantiene**. Y el cuarto es el que más veces falta y el que más
caro sale: **un componente sin dueño identificable es deuda técnica esperando a manifestarse** (clase
154). Lo demás —el lenguaje, el marco, el estilo— se puede cambiar; **el reparto de responsabilidades y
la persona que responde, no**.
""",
    langs={
        "cobol": ("""
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
""", """
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
| **Cálculo de intereses, comisiones y saldos** | decimal exacto (clase 072) |
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
"""),
        "fortran": ("""
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
""", """
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
"""),
        "ada": ("""
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
""", """
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
"""),
        "pascal": ("""
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
""", """
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
"""),
        "lisp": ("""
(let ((linea (read-line))
      (cnt 0)
      (piezas '())
      (actual '()))
  (loop for c across linea
        do (if (char= c #\\Space)
               (when actual
                 (push (coerce (nreverse actual) 'string) piezas)
                 (setf actual nil))
               (push c actual)))
  (when actual (push (coerce (nreverse actual) 'string) piezas))
  (setf piezas (nreverse piezas)
        cnt (length piezas))
  (format t "componentes=~D nombres=~{~A~^-~}~%" cnt piezas))
""", """
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
"""),
        "tcl": ("""
gets stdin linea
set comps [split [string trim $linea]]

puts "componentes=[llength $comps] nombres=[join $comps -]"
""", """
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
"""),
        "perl": ("""
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;

my @comps = split ' ', $linea;

print "componentes=", scalar(@comps), " nombres=", join('-', @comps), "\\n";
""", """
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
"""),
        "cpp": ("""
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
    std::cout << '\\n';
    return 0;
}
""", """
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
"""),
        "rpg": ("""
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
""", """
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
"""),
        "pli": ("""
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
""", """
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
"""),
        "mumps": ("""
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
""", """
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
"""),
        "smalltalk": ("""
| linea comps |

linea := stdin nextLine trimBoth.
comps := linea substrings: ' '.

Transcript
    show: 'componentes=', comps size printString;
    show: ' nombres=', (comps inject: '' into: [ :a :b |
        a isEmpty ifTrue: [ b ] ifFalse: [ a, '-', b ] ]);
    cr.
""", """
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
"""),
    },
)

# ---------------------------------------------------------------------------
# 166 — Diseño: responsabilidades y contratos entre componentes
# ---------------------------------------------------------------------------
SPECS["166"] = dict(
    gancho="""
Comprobar que dos versiones de contrato encajan. Es lo primero que hace cualquier sistema distribuido al
arrancar, y esta clase trata de la decisión que lo precede: **qué hace cada componente y qué se promete
a los demás**. Y aquí estos lenguajes aportan algo que ningún diagrama de arquitectura da: **la
evidencia de qué contratos aguantan treinta años** — y la respuesta es siempre la misma clase de
contrato: **el pequeño, el explícito y el que solo crece**.
""",
    porque="""
Aquí el concepto es el **reparto de responsabilidades**, y estos lenguajes lo enseñan porque **tienen
contratos con décadas de historia**: la COMMAREA de CICS, la firma de un programa de servicio, la
especificación de un paquete Ada, el formato de un registro, el diccionario de FileMan. Y todos
demuestran lo mismo que la clase 160 concluía: **lo que decide si un contrato sobrevive no es la
tecnología, sino si hay una regla escrita sobre qué se puede cambiar**.

Y aparece la pregunta de diseño: **¿dónde se pone la frontera?** Porque una mal puesta obliga a cambiar
dos componentes cada vez.
""",
    cierre="""
Lo transferible: **la frontera correcta es la que hace que la mayoría de los cambios queden dentro de un
solo componente**. Ese es el criterio, y es medible: si cada funcionalidad nueva toca tres componentes,
la separación está mal hecha, por muy bonito que sea el diagrama. De ahí las dos reglas: **agrupar lo
que cambia junto y separar lo que cambia por razones distintas**; y **hacer las interfaces estrechas**,
porque **todo lo que se expone hay que mantenerlo** — y lo que no se expone se puede cambiar el martes
sin avisar a nadie.
""",
    langs={
        "cobol": ("""
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
""", """
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
"""),
        "fortran": ("""
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
""", """
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
"""),
        "ada": ("""
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
""", """
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
"""),
        "pascal": ("""
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
""", """
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
"""),
        "lisp": ("""
(let ((a (read))
      (b (read)))
  (format t "contrato=~A~%" (if (= a b) "compatible" "incompatible")))
""", """
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
"""),
        "tcl": ("""
gets stdin linea
lassign [string trim $linea] a b

puts "contrato=[expr {$a == $b ? {compatible} : {incompatible}}]"
""", """
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
"""),
        "perl": ("""
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;
my ($a1, $b1) = split ' ', $linea;

print "contrato=", ($a1 == $b1 ? 'compatible' : 'incompatible'), "\\n";
""", """
**Cómo se diseñan las responsabilidades en Perl.** Perl tiene el módulo como unidad, y **el contrato es
lo que se exporta**:

```perl
package MiSistema::Pedidos;
use strict; use warnings;
use Exporter 'import';

our @EXPORT_OK = qw(crear consultar anular);       # el contrato
our %EXPORT_TAGS = (todo => \\@EXPORT_OK);

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
"""),
        "cpp": ("""
#include <iostream>

int main() {
    int a{}, b{};
    if (!(std::cin >> a >> b)) return 1;

    std::cout << "contrato=" << (a == b ? "compatible" : "incompatible") << '\\n';
    return 0;
}
""", """
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
"""),
        "rpg": ("""
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
""", """
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
"""),
        "pli": ("""
 contrat: procedure options(main);

    declare (a, b) fixed binary(31);

    get list (a, b);

    if a = b then
       put skip list ('contrato=compatible');
    else
       put skip list ('contrato=incompatible');

 end contrat;
""", """
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
"""),
        "mumps": ("""
CONTRAT ; Compatibilidad de contrato -- clase 166
 read linea
 new a, b
 set a = $piece(linea, " ", 1)
 set b = $piece(linea, " ", 2)
 write "contrato=", $select(a = b : "compatible", 1 : "incompatible"), !
 quit
""", """
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
"""),
        "smalltalk": ("""
| linea partes a b |

linea := stdin nextLine trimBoth.
partes := linea substrings: ' '.

a := (partes at: 1) asNumber.
b := (partes at: 2) asNumber.

Transcript
    show: 'contrato=', (a = b ifTrue: [ 'compatible' ] ifFalse: [ 'incompatible' ]);
    cr.
""", """
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
"""),
    },
)

# ---------------------------------------------------------------------------
# 167 — Componente CLI: lenguaje de sistemas
# ---------------------------------------------------------------------------
SPECS["167"] = dict(
    gancho="""
Un comando y sus argumentos: `comando=run args=2`. Es la interfaz de usuario más antigua que sigue viva,
y la que estos doce lenguajes conocen mejor. Y merece empezar con una observación: **la línea de comandos
no ha sobrevivido por nostalgia, sino porque es la única interfaz que se puede automatizar, versionar,
componer y ejecutar sin persona delante** — que son exactamente los requisitos de todo lo que esta parte
del curso está construyendo.
""",
    porque="""
Aquí el concepto es la **herramienta de línea de comandos como componente**, y estos lenguajes la
enseñan porque **cubren los dos extremos**: los que producen un ejecutable nativo sin dependencias
—Pascal, Ada, C++, COBOL, Fortran— y los que necesitan su intérprete —Perl, Tcl, Lisp—. Y esa diferencia
decide algo muy práctico: **si la herramienta se puede copiar y ejecutar, o hay que instalar un
entorno**.

Y aparecen las convenciones que hacen que una herramienta encaje con las demás: **códigos de salida,
salida estándar frente a error, y comportarse bien en una tubería**.
""",
    cierre="""
Lo transferible: **una buena herramienta de línea de comandos es la que se deja usar por otro programa**.
Eso significa cuatro cosas concretas: **el resultado por la salida estándar y los mensajes por la de
error**, para que se pueda encauzar; **un código de salida que distinga bien de mal**, para que un guion
decida; **no preguntar nada si no hay terminal**, para que funcione desatendida; y **un formato de salida
estable o elegible** —`--json` cuando lo consuma una máquina—. Con esas cuatro, la herramienta se compone
con todo lo demás; sin ellas, es un callejón sin salida por muy bonita que sea.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. CLI.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(200).
01  I       PIC 9(4) COMP.
01  CNT     PIC 9(4) COMP VALUE 0.
01  ENPAL   PIC 9      VALUE 0.
01  COMANDO PIC X(30) VALUE SPACES.
01  POSIC   PIC 9(4) COMP VALUE 1.
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
            IF CNT = 1
                MOVE LINEA(I:1) TO COMANDO(POSIC:1)
                COMPUTE POSIC = POSIC + 1
            END-IF
        END-IF
    END-PERFORM

    COMPUTE CNT = CNT - 1
    MOVE CNT TO ED
    DISPLAY "comando=" FUNCTION TRIM(COMANDO)
            " args=" FUNCTION TRIM(ED)
    STOP RUN.
""", """
**COBOL como herramienta de línea de comandos.** COBOL sabe hacerlo, y merece conocer cómo, porque el
mundo GnuCOBOL lo usa de verdad:

```cobol
       PROCEDURE DIVISION.
           ACCEPT WS-ARGS FROM COMMAND-LINE          *> toda la línea
           ACCEPT WS-N    FROM ARGUMENT-NUMBER        *> cuántos hay
           PERFORM VARYING I FROM 1 BY 1 UNTIL I > WS-N
               ACCEPT WS-ARG FROM ARGUMENT-VALUE      *> uno a uno
           END-PERFORM

           ACCEPT WS-VAR FROM ENVIRONMENT "MI_VARIABLE"
           ...
           MOVE 2 TO RETURN-CODE                       *> ← el código de salida
           STOP RUN.
```

**`RETURN-CODE` es la tercera propiedad del cierre de esta clase**, y en COBOL es una variable especial:
**asignarle un valor antes de `STOP RUN` es el código de salida del proceso**.

Y merece explicar de dónde viene esa convención, porque es del mundo del lote y sigue viva: **el código
de retorno gobierna el JCL** (clase 077).

```jcl
//PASO2 EXEC PGM=SIGUIENTE,COND=(4,LT,PASO1)
//*    ejecutar PASO2 solo si el código de PASO1 NO es mayor que 4
```

**Los valores tienen significado convenido en el mainframe**:

```text
0   todo bien
4   avisos: continuar
8   error: normalmente parar
12  error grave
16  error fatal
```

**Es exactamente la idea de los códigos de salida de Unix, con más granularidad y con un lenguaje —el
JCL— para decidir en función de ellos.**

Y merece señalar la diferencia con la práctica actual: **en Unix, 0 es bien y cualquier otro es mal**;
en el mainframe, **hay una escala** y los guiones la usan.

Es una idea que merece rescatarse para la primera regla del cierre: **distinguir "falló" de "terminó con
avisos" permite automatizar decisiones que con un booleano no se pueden tomar** — y es lo que hacen hoy
las herramientas serias con códigos de salida específicos documentados.
"""),
        "fortran": ("""
program cli
   implicit none
   character(len=200) :: linea
   character(len=30)  :: comando
   integer :: i, cnt, p1
   logical :: en_palabra

   read(*, '(A)') linea
   linea = adjustl(linea)

   p1 = index(linea, ' ')
   comando = linea(1:p1-1)

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

   write(*, '(A,I0)') 'comando=' // trim(comando) // ' args=', cnt - 1
end program cli
""", """
**Fortran como herramienta de línea de comandos.** Fortran tardó en tener acceso a los argumentos de
forma estándar, y merece contarlo porque ilustra bien la evolución del lenguaje:

```fortran
! Antes de 2003: extensiones distintas en cada compilador
call getarg(1, arg)          ! ¡no estándar!

! Fortran 2003, en el estándar:
integer :: n, largo, estado
character(len=:), allocatable :: arg

n = command_argument_count()
call get_command_argument(1, length=largo)
allocate(character(len=largo) :: arg)
call get_command_argument(1, arg)

call get_environment_variable('MI_VAR', valor)
call execute_command_line('ls -l', wait=.true., exitstat=codigo)   ! 2008
```

**`get_command_argument` con `length=` primero y luego el valor** es el idioma correcto: **se pregunta la
longitud, se reserva, y se lee** — porque las cadenas de Fortran son de longitud fija (clase 093).

Y **`execute_command_line`, de Fortran 2008**, merece la mención porque cierra un hueco importante: **hasta
entonces, ejecutar otro programa desde Fortran requería extensiones del compilador**.

Y esta clase es el sitio para señalar la costumbre de este dominio que choca con el cierre de esta clase,
porque merece revisarse: **los programas científicos no suelen tener interfaz de línea de comandos: leen
un fichero de configuración** (clase 163).

```bash
./simulacion < entrada.nml       # o incluso con el fichero con un nombre fijo
```

**Y eso los hace difíciles de automatizar**: para lanzar mil variantes hay que generar mil ficheros.

Y la recomendación de esta parte del curso es concreta y barata: **aceptar los parámetros también por la
línea de comandos**, con los valores del fichero como valores por defecto.

```bash
./simulacion --config base.nml --set dt=0.0005 --set modelo=laminar
```

**Con eso, un barrido de parámetros es un bucle de shell** en lugar de un generador de ficheros — y la
herramienta pasa a componerse con todo lo demás, que es la definición del cierre de esta clase.
"""),
        "ada": ("""
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Strings;
with Ada.Strings.Fixed;

procedure Cli is
   Linea      : String (1 .. 200);
   Ultimo     : Natural;
   Sep        : Natural;
   Cnt        : Natural := 0;
   En_Palabra : Boolean := False;
begin
   Get_Line (Linea, Ultimo);
   Sep := Ada.Strings.Fixed.Index (Linea (1 .. Ultimo), " ");

   if Sep = 0 then
      Sep := Ultimo + 1;
   end if;

   for I in 1 .. Ultimo loop
      if Linea (I) = ' ' then
         En_Palabra := False;
      elsif not En_Palabra then
         En_Palabra := True;
         Cnt := Cnt + 1;
      end if;
   end loop;

   Put_Line ("comando=" & Linea (1 .. Sep - 1) & " args=" &
             Ada.Strings.Fixed.Trim (Natural'Image (Cnt - 1), Ada.Strings.Both));
end Cli;
""", """
**Ada como herramienta de línea de comandos.** Ada tiene los argumentos en el estándar desde 1995, con una
API pequeña y clara:

```ada
with Ada.Command_Line; use Ada.Command_Line;

for I in 1 .. Argument_Count loop
   Put_Line (Argument (I));
end loop;

Put_Line (Command_Name);
Set_Exit_Status (Failure);      --  o Success, o un valor concreto
```

**`Set_Exit_Status` con `Success` y `Failure` como constantes con nombre** es un detalle pequeño y
representativo: **el código de salida no es un número mágico, es un valor de un tipo**.

Y las herramientas de línea de comandos escritas en Ada tienen una ventaja concreta para el proyecto de
esta parte, y merece decirla: **son ejecutables nativos, estáticos y sin dependencias**.

```bash
gnatmake -O2 herramienta.adb
ldd herramienta        # apenas libc: se copia y funciona
```

**Y con `pragma Restrictions` y el perfil reducido** (clase 162), **el binario puede ser muy pequeño y de
consumo acotado** — lo que la hace apta para arrancar en un contenedor mínimo (clase 174).

Y Ada aporta a esta clase una técnica de diseño que encaja con el cierre y que la clase 124 hace posible:
**validar los argumentos con tipos**.

```ada
subtype Puerto is Integer range 1 .. 65_535;

declare
   P : constant Puerto := Puerto'Value (Argument (1));   --  lanza si no encaja
begin
   ...
exception
   when Constraint_Error =>
      Put_Line (Standard_Error, "El puerto debe estar entre 1 y 65535");
      Set_Exit_Status (Failure);
end;
```

**El rango del tipo es la validación**, y el mensaje de error se escribe una vez.

Y merece señalar el `Standard_Error` de ese fragmento, porque es la primera propiedad del cierre de esta
clase y la que más se incumple: **los mensajes van al error estándar, no a la salida**.

Si el mensaje de ayuda o el aviso salen por la salida estándar, **se cuelan en la tubería** y estropean lo
que el siguiente programa recibe. Es un fallo pequeño, muy frecuente, y hace que una herramienta no se
pueda componer.
"""),
        "pascal": ("""
program Cli;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  Linea, Comando: string;
  I, Cnt, P: Integer;
  EnPalabra: Boolean;

begin
  ReadLn(Linea);
  Linea := Trim(Linea);

  P := Pos(' ', Linea);
  if P = 0 then P := Length(Linea) + 1;
  Comando := Copy(Linea, 1, P - 1);

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

  WriteLn('comando=', Comando, ' args=', IntToStr(Cnt - 1));
end.
""", """
**Pascal como herramienta de línea de comandos.** Free Pascal es de las mejores opciones de esta página
para el componente de esta clase, y merece justificarlo:

```pascal
uses SysUtils, CustApp;

type
  TMiApp = class(TCustomApplication)
  protected
    procedure DoRun; override;
  end;

procedure TMiApp.DoRun;
begin
  if HasOption('h', 'help') then begin MostrarAyuda; Terminate; Exit end;
  if not CheckOptions('hv:', 'help verbose:') = '' then ...
  WriteLn(GetOptionValue('v', 'verbose'));
  ExitCode := 0;
  Terminate;
end;
```

**`TCustomApplication` viene en la distribución** y trae análisis de opciones cortas y largas, ayuda y
manejo de excepciones — sin instalar nada.

Y las razones por las que Pascal encaja bien aquí son las de la clase 164:

| Ventaja | Detalle |
|---|---|
| **Binario pequeño y autocontenido** | se copia y funciona (clase 144) |
| **Arranque instantáneo** | sin cargar intérprete ni máquina virtual |
| **Compilación cruzada** | un solo corredor produce Windows, Linux y macOS (clase 147) |
| **Compila en segundos** | el ciclo de desarrollo es rapidísimo |

**Y la tercera es la que más vale para el proyecto de esta parte**: **`fpc -Twin64` y `fpc -Tlinux` desde
la misma máquina** producen las dos herramientas, sin contenedores ni cadenas cruzadas.

Y merece añadir la propiedad del cierre que a menudo se olvida y que Pascal facilita: **detectar si hay
terminal**.

```pascal
uses Unix;
if IsATTY(StdOutputHandle) = 1 then
  { hay persona: se puede usar color y barra de progreso }
else
  { está en una tubería: salida limpia, sin adornos }
```

**Una herramienta que detecta si su salida va a un terminal o a una tubería puede ser bonita y
automatizable a la vez** — y es lo que hacen `git`, `ls` y todas las herramientas modernas bien hechas.

Es la cuarta propiedad del cierre resuelta con una llamada.
"""),
        "lisp": ("""
(let* ((linea (read-line))
       (piezas (let ((lista '()) (actual '()))
                 (loop for c across linea
                       do (if (char= c #\\Space)
                              (when actual
                                (push (coerce (nreverse actual) 'string) lista)
                                (setf actual nil))
                              (push c actual)))
                 (when actual (push (coerce (nreverse actual) 'string) lista))
                 (nreverse lista))))
  (format t "comando=~A args=~D~%" (first piezas) (1- (length piezas))))
""", """
**Lisp como herramienta de línea de comandos.** Lisp puede hacerlo, y tiene una limitación práctica que
merece enunciarse con claridad: **el arranque**.

```lisp
;; Acceso a los argumentos: NO está en el estándar; cada implementación tiene el suyo
sb-ext:*posix-argv*        ; SBCL
(uiop:command-line-arguments)   ; portable, con UIOP
(uiop:quit 1)                    ; código de salida
```

**Y la solución al arranque es la de la clase 144: guardar una imagen ejecutable.**

```lisp
(sb-ext:save-lisp-and-die "miherramienta"
                          :executable t
                          :toplevel #'main
                          :compression t)
```

**Con eso el arranque es de milisegundos** —el estado ya está construido— **a costa de un binario de
decenas de megabytes**.

Y merece la comparación honesta para el proyecto de esta parte:

| Aspecto | Lisp con imagen | Pascal/Ada/C++ |
|---|---|---|
| Arranque | **rápido** (ya construido) | rápido |
| Tamaño | **20-60 MB** | **0,2-5 MB** |
| Dependencias | ninguna | ninguna |
| Desarrollo | **el más rápido de esta página** | ciclo de compilación |

**Y esa tabla es la decisión**: si la herramienta se ejecuta mil veces al día en una canalización, el
tamaño importa; si es una herramienta interna que se usa a mano, no.

Y Lisp tiene, para esta clase, dos ecosistemas que merecen nombrarse:

| Herramienta | Notas |
|---|---|
| **Roswell** | gestor de implementaciones y **guiones ejecutables** con `#!/usr/bin/env ros` |
| **UIOP** | portabilidad: argumentos, procesos, rutas, salida |
| **clingon / unix-opts** | análisis de opciones, con subcomandos |
| **`--script`** | ejecutar un fichero sin construir imagen, pagando el arranque |

Y merece cerrar con la propiedad del cierre que Lisp cumple especialmente bien y que conviene aprovechar:
**la salida legible por máquina**.

```lisp
(if (uiop:getenvp "SALIDA_JSON")
    (yason:encode resultado)
    (format t "~{~A~%~}" resultado))
```

**Un `--json` opcional convierte la herramienta en un componente**, y en Lisp la estructura de datos ya
está ahí — solo hay que elegir el formateador.
"""),
        "tcl": ("""
gets stdin linea
set args [split [string trim $linea]]

puts "comando=[lindex $args 0] args=[expr {[llength $args] - 1}]"
""", """
**Tcl como herramienta de línea de comandos.** Tcl tiene los argumentos en variables globales, y su
manejo es directo:

```tcl
puts $argv0            ;# el nombre del guion
puts $argc              ;# cuántos argumentos
puts $argv               ;# la LISTA de argumentos
exit 1                    ;# código de salida
```

**`$argv` es una lista de verdad**, no una cadena que hay que partir — que es una comodidad real
comparada con varios de esta página.

Y Tcl es especialmente adecuado para el componente de esta clase por lo que la clase 165 señalaba: **es el
pegamento**, y la mayoría de las herramientas internas de un proyecto son pegamento.

```tcl
#!/usr/bin/env tclsh
package require cmdline

set opciones {
    {verbose        "salida detallada"}
    {config.arg  "" "fichero de configuración"}
    {jobs.arg     4 "trabajos en paralelo"}
}
array set params [::cmdline::getoptions argv $opciones "uso: $argv0 [opciones] comando"]
```

**`cmdline` está en tcllib** y da opciones, valores por defecto y el mensaje de uso.

Y merece señalar la propiedad del cierre de esta clase que Tcl facilita mejor que casi todos, porque es
su especialidad (clase 161): **encadenar procesos**.

```tcl
set salida [exec ./extraer $fichero | sort -n | uniq -c]
```

**`exec` con tuberías, en una línea** — y con la citación correcta, sin pasar por un intérprete de órdenes
(clase 153).

Y la advertencia práctica de esta clase para Tcl, que la clase 164 anticipó: **el guion necesita
`tclsh`**.

Y las respuestas son las de la clase 144:

```bash
sdx wrap miherramienta.exe -runtime tclkit    # Starpack: un ejecutable, sin dependencias
```

**Un Starpack convierte el guion en un binario autocontenido**, con lo que la herramienta se copia y
funciona — que es lo que el proyecto de esta parte necesita para distribuir sus utilidades sin exigir un
entorno.
"""),
        "perl": ("""
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;

my @args = split ' ', $linea;
my $comando = shift @args;

print "comando=$comando args=", scalar(@args), "\\n";
""", """
**Perl como herramienta de línea de comandos.** Perl es, probablemente, **el lenguaje con el que más
herramientas de línea de comandos se han escrito**, y su ergonomía para esto es excelente:

```perl
use Getopt::Long;

GetOptions(
    'verbose!'   => \\my $verbose,        # --verbose / --no-verbose
    'jobs=i'     => \\(my $jobs = 4),      # --jobs 8
    'config=s'   => \\my $config,          # --config fichero
    'help'       => sub { pod2usage(0) },  # ← la ayuda sale del POD (clase 154)
) or pod2usage(2);

exit(2) if $error;
```

**`pod2usage` merece la mención** porque resuelve un problema real: **el mensaje de ayuda se genera desde
la documentación POD del propio guion**, así que **no puede desincronizarse**.

Es la aplicación de la clase 154 a esta clase: **la documentación y la ayuda son la misma fuente**.

Y Perl tiene los idiomas de una línea que definieron el género y que merecen conocerse porque siguen
siendo insuperables:

```bash
perl -pe 's/viejo/nuevo/g' fichero          # sustituir e imprimir
perl -ne 'print if /error/' registro.log     # filtrar
perl -lane 'print $F[2]' datos.txt            # ¡la tercera columna!
perl -i.bak -pe 's/a/b/' *.conf                # editar EN SITIO, con copia
perl -MJSON::PP -e '...'                        # con un módulo cargado
```

**`-lane` es el más denso**: `-l` maneja los saltos de línea, `-a` **parte cada línea en `@F`
automáticamente**, `-n` hace el bucle y `-e` da el código.

**Es `awk` con todo Perl detrás**, y sigue siendo la forma más rápida de resolver una transformación de
texto puntual.

Y merece cerrar con las propiedades del cierre de esta clase, que Perl cumple si se escriben:

```perl
print STDERR "aviso: ...\\n";        # mensajes al ERROR estándar
print STDOUT $resultado;              # el resultado, a la salida
exit 0;                                # explícito
$| = 1;                                 # sin búfer, si va a una tubería (clase 141)
```

**`$| = 1` merece la advertencia**: sin él, **la salida de Perl se guarda en un búfer cuando no va a un
terminal**, y una herramienta que escribe progreso en una tubería **parece colgada** hasta que termina.

Es la misma lección que `flush` en Fortran (clase 141), y una de las causas más frecuentes de "esto no
funciona en el servidor".
"""),
        "cpp": ("""
#include <iostream>
#include <string>
#include <vector>

int main() {
    std::vector<std::string> args;
    std::string a;
    while (std::cin >> a) args.push_back(a);

    if (args.empty()) return 1;

    std::cout << "comando=" << args.front()
              << " args=" << args.size() - 1 << '\\n';
    return 0;
}
""", """
**C++ como herramienta de línea de comandos.** C++ produce el binario más rápido y más pequeño de esta
página, y su ecosistema para esta clase es bueno:

```cpp
#include <CLI/CLI.hpp>          // CLI11: solo cabeceras

int main(int argc, char** argv) {
    CLI::App app{"Mi herramienta"};
    int jobs = 4;
    std::string config;
    bool verbose = false;

    app.add_option("-j,--jobs", jobs, "Trabajos en paralelo")->check(CLI::Range(1, 64));
    app.add_option("-c,--config", config, "Fichero de configuración")
       ->check(CLI::ExistingFile);
    app.add_flag("-v,--verbose", verbose);

    auto* sub = app.add_subcommand("build", "Construir el proyecto");

    CLI11_PARSE(app, argc, argv);
    return 0;
}
```

**`->check(CLI::Range(1, 64))` y `->check(CLI::ExistingFile)`** merecen destacarse: **la validación se
declara junto a la opción**, y el mensaje de error lo genera la biblioteca.

Es lo mismo que Ada consigue con los subtipos con rango en esta página, con una biblioteca en lugar de
con el sistema de tipos.

Y las alternativas del ecosistema:

| Biblioteca | Notas |
|---|---|
| **CLI11** | solo cabeceras, subcomandos, validación, configuración |
| **argparse** | ligera, al estilo de Python |
| **Boost.Program_options** | veterana, potente, pesada |
| **getopt / getopt_long** | de C, sin dependencias, y tediosa |

Y merece señalar, para el proyecto de esta parte, la propiedad de C++ que decide su uso aquí: **el
tiempo de arranque**.

```text
Un binario en C++ arranca en ~1 ms.
Python arranca en ~30-50 ms; Node en ~40 ms; una JVM en ~100-300 ms.
```

**Y eso importa cuando la herramienta se invoca miles de veces**, que es exactamente lo que pasa en un
sistema de construcción o en un gancho de git (clase 145).

Es la razón por la que las herramientas que se ejecutan en bucle —compiladores, formateadores,
analizadores, `ripgrep`, `fd`— **están escritas en lenguajes compilados**, y no por casualidad.

Y la advertencia final del cierre, que en C++ hay que escribir a mano: **cerrar bien la salida**.

```cpp
std::cout << resultado << std::flush;
return std::cout.good() ? 0 : 1;       // ¿falló la escritura? (disco lleno, tubería rota)
```

**Ignorar un error de escritura en la salida es un fallo silencioso clásico**, y una herramienta seria lo
comprueba.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi CLI;
  linea char(200) const;
end-pi;

dcl-s texto   varchar(200);
dcl-s comando varchar(30);
dcl-s pos     int(10);
dcl-s cnt     int(10);
dcl-s enpal   ind;
dcl-s i       int(10);

texto = %trim(linea);
pos = %scan(' ' : texto);
if pos = 0;
  comando = texto;
else;
  comando = %subst(texto : 1 : pos - 1);
endif;

cnt = 0;
enpal = *off;
for i = 1 to %len(texto);
  if %subst(texto : i : 1) = ' ';
    enpal = *off;
  elseif not enpal;
    enpal = *on;
    cnt += 1;
  endif;
endfor;

dsply ('comando=' + comando + ' args=' + %char(cnt - 1));

*inlr = *on;
return;
""", """
**RPG como herramienta de línea de comandos.** IBM i tiene una noción de "línea de comandos" propia y muy
elaborada, y merece conocerla porque resuelve cosas que las demás de esta página dejan a la biblioteca:
**el comando CL definido por el usuario**.

```text
CMD PROMPT('Procesar pedidos')
PARM KWD(CLIENTE) TYPE(*CHAR) LEN(10) MIN(1) PROMPT('Cliente')
PARM KWD(DESDE)   TYPE(*DATE) PROMPT('Fecha desde')
PARM KWD(MODO)    TYPE(*CHAR) LEN(10) DFT(*NORMAL) +
                  SPCVAL((*NORMAL) (*SIMULA)) PROMPT('Modo')
```

**Ese fichero define un comando del sistema**, y con él se obtiene:

| Se obtiene | Sin escribir código |
|---|---|
| **Validación de tipos y longitudes** | el sistema la hace |
| **Valores especiales y por defecto** | declarados |
| **Ayuda contextual** | con `F1` sobre cada parámetro |
| **Petición interactiva de parámetros** | con `F4`: **un formulario generado** |
| **Y comprobación de autorización** | por comando |

**La cuarta fila es la que sorprende**: **pulsar F4 sobre un comando genera una pantalla con un campo por
parámetro, con su descripción y su ayuda** — automáticamente, desde la definición.

Es la interfaz de línea de comandos y la interfaz interactiva **generadas del mismo contrato**, que es
exactamente lo que la clase 160 pedía y lo que casi ninguna herramienta moderna consigue.

Y merece la comparación con el mundo Unix, porque las dos filosofías son coherentes:

```text
Unix:    el programa recibe una lista de cadenas y se apaña.
         Máxima flexibilidad, cero ayuda, cada herramienta a su manera.

IBM i:   el comando declara sus parámetros y el sistema hace lo demás.
         Consistencia total, y menos libertad.
```

**Y la consistencia tiene un valor que se nota**: en IBM i, **todos los comandos se comportan igual**
—`F1` ayuda, `F4` pide, los valores especiales empiezan por asterisco— y eso hace que aprender uno sea
aprender todos.

Es una idea que las herramientas modernas persiguen con especificaciones de línea de comandos declarativas
y con generadores de autocompletado — llegando al mismo sitio cuarenta años después.
"""),
        "pli": ("""
 cli: procedure options(main);

    declare linea   char(200) varying;
    declare comando char(30) varying;
    declare i       fixed binary(31);
    declare cnt     fixed binary(31) initial(0);
    declare enpal   bit(1) initial('0'b);
    declare p       fixed binary(31);

    get edit (linea) (a(200));
    linea = trim(linea);

    p = index(linea, ' ');
    if p = 0 then
       comando = linea;
    else
       comando = substr(linea, 1, p - 1);

    do i = 1 to length(linea);
       if substr(linea, i, 1) = ' ' then
          enpal = '0'b;
       else if ^enpal then
          do;
             enpal = '1'b;
             cnt = cnt + 1;
          end;
    end;

    put skip list ('comando=' || comando || ' args=' || trim(char(cnt - 1)));

 end cli;
""", """
**PL/I como herramienta de línea de comandos.** PL/I recibe los parámetros de una forma que merece
explicarse porque es la del mainframe y es distinta de todo lo demás de esta página:

```pli
 miprog: procedure (parametros) options(main);
    declare parametros char(100) varying;
    ...
 end miprog;
```

```jcl
//PASO1 EXEC PGM=MIPROG,PARM='CLIENTE=4711,MODO=SIMULA'
```

**El `PARM` del JCL llega como una única cadena**, y **el programa la analiza**.

Y merece señalar la limitación histórica, porque explica una costumbre: **el `PARM` clásico está limitado
a 100 caracteres**.

Por eso, cuando hace falta más, **la configuración va por un fichero declarado en el JCL**:

```jcl
//PARAMS DD *
CLIENTE=4711
MODO=SIMULA
FECHA=2026-08-15
/*
```

**`DD *` mete los datos en el propio JCL**, así que **el trabajo y su configuración viajan juntos y se
versionan juntos** (clase 145).

Es una propiedad que merece destacarse porque el mundo moderno la ha redescubierto: **la configuración
junto a la definición del trabajo** es lo que hacen hoy los ficheros de las canalizaciones de integración
continua y los manifiestos de despliegue.

Y el código de retorno, que es la tercera propiedad del cierre de esta clase:

```pli
 declare plirest entry (fixed binary(31)) options(assembler);
 call plirest(8);       /* código de retorno 8 */
```

**O, más simple, con `return` desde el procedimiento principal** según el compilador.

Y merece cerrar con la observación que esta página permite hacer sobre la primera propiedad del cierre:
**en el mainframe, la salida no es "la salida estándar" — son ficheros declarados**.

```jcl
//SYSPRINT DD SYSOUT=*        <-- el informe
//ERRORES  DD DSN=...          <-- los errores, a otro sitio
//SALIDA   DD DSN=...           <-- los datos, a un tercero
```

**Cada flujo tiene su destino declarado en el JCL**, así que **la separación entre resultado, mensajes y
errores no es una convención: es explícita y se configura al ejecutar**.

Es más rígido que las tuberías de Unix y resuelve el mismo problema con más control — y es, otra vez, la
misma idea con distinta ropa.
"""),
        "mumps": ("""
CLI ; Componente de linea de comandos -- clase 167
 read linea
 new i, cnt, comando, p
 set comando = $piece(linea, " ", 1)
 set cnt = 0
 for i = 1:1:$length(linea, " ") do
 . set p = $piece(linea, " ", i)
 . if p '= "" set cnt = cnt + 1
 write "comando=", comando, " args=", cnt - 1, !
 quit
""", """
**M como herramienta de línea de comandos.** M tiene acceso a los argumentos en las implementaciones
modernas, aunque no en el estándar:

```mumps
 ; YottaDB / GT.M
 write $zcmdline                  ; la línea de comandos completa
 set arg1 = $piece($zcmdline, " ", 1)
 zhalt 1                           ; código de salida
```

```bash
yottadb -run MIRUT arg1 arg2
mumps -run %XCMD 'do ^MIRUT'
```

**`$zcmdline` es una extensión `$Z`** (clase 146), así que **el código que la use no es portable entre
implementaciones**.

Y esta clase es el sitio para señalar que **el equivalente de la línea de comandos en este mundo es otra
cosa: el menú**.

```text
En VistA, el usuario no escribe comandos: navega por MENÚS,
definidos como datos en el fichero OPTION, con:
  - el nombre de la opción y su texto
  - la rutina o el menú al que lleva
  - las CLAVES DE SEGURIDAD que hacen falta (clase 153)
  - y la ayuda
```

**Y eso es, otra vez, una interfaz generada desde metadatos** (clase 149) — igual que los comandos de CL
en RPG en esta página.

Y merece la observación general, porque esta página la hace evidente: **las plataformas integradas
generan sus interfaces desde declaraciones; el mundo Unix las escribe a mano en cada programa**.

```text
Generada:  consistente, con ayuda, con permisos, y limitada a lo previsto.
A mano:    libre, inconsistente, y cada herramienta reinventa lo mismo.
```

Y la industria ha ido, lentamente, hacia la primera: **las especificaciones de línea de comandos en
ficheros, los generadores de autocompletado, y las herramientas que publican su interfaz en JSON** están
persiguiendo lo mismo.

Y para el proyecto de esta parte, la recomendación que se deriva es concreta: **declarar la interfaz de
la herramienta en un sitio** —una estructura, un fichero, una definición— **y generar de ahí el análisis,
la ayuda y la documentación**, en lugar de escribir las tres por separado y verlas divergir (clase 154).
"""),
        "smalltalk": ("""
| linea args |

linea := stdin nextLine trimBoth.
args := linea substrings: ' '.

Transcript
    show: 'comando=', args first;
    show: ' args=', (args size - 1) printString;
    cr.
""", """
**Smalltalk como herramienta de línea de comandos.** Smalltalk puede hacerlo, y merece decir con
honestidad que **es de sus usos menos naturales**.

```smalltalk
"Pharo: acceso a los argumentos"
Smalltalk arguments.
Smalltalk os environment at: 'HOME'.
Smalltalk exitSuccess.
Smalltalk exit: 1.
```

```bash
./pharo miapp.image eval "Smalltalk arguments"
./pharo miapp.image miComando --opcion valor      # con Clap
```

Y el motivo de la fricción es el de la clase 144: **el artefacto es una imagen**, así que una herramienta
de línea de comandos escrita en Smalltalk **arrastra una imagen de decenas de megabytes** y **su arranque
tiene que cargarla**.

Y el ecosistema ha construido lo que faltaba:

| Herramienta | Notas |
|---|---|
| **Clap** | análisis de opciones y subcomandos, con documentación integrada |
| **`pharo eval`** | ejecutar una expresión desde el sistema operativo |
| **Reducción de imagen** | quitar lo que no se usa (clase 144) |

Y merece señalar el uso donde Smalltalk **sí** es la elección correcta para esta clase y que es real:
**la herramienta que analiza el propio sistema** (clase 165).

```bash
./pharo moose.image analizar --proyecto ../miapp --formato json
```

**Moose importa código de cualquier lenguaje y responde preguntas sobre él**, y ahí el coste de arranque
es irrelevante porque el análisis tarda minutos.

Es la regla general que esta clase deja: **el coste de arranque importa en proporción a lo que la
herramienta hace**. Para algo que se invoca mil veces en un bucle, C++ o Pascal; para algo que se lanza
una vez y trabaja diez minutos, da igual.

Y merece cerrar con la propiedad del cierre que Smalltalk cumple de forma natural y que conviene
aprovechar: **la salida estructurada**.

```smalltalk
STON toStringPretty: resultado.
NeoJSONWriter toString: resultado.
```

**Serializar el resultado es una línea** (clase 159), así que **añadir `--json` a una herramienta escrita
en Smalltalk es trivial** — y con eso cumple la cuarta propiedad del cierre y se convierte en un
componente que otros pueden consumir.
"""),
    },
)
