# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 164

> [⬅️ Volver a la clase 164](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Un dominio, un lenguaje: `sistemas → Rust`, `web → TypeScript`, `datos → SQL`. Es una simplificación
deliberada, porque esta clase cierra la Parte 10 con la pregunta más incómoda de todo el curso: **¿y
estos doce, cuándo se elegirían hoy?** Y la respuesta honesta —que cada apartado de esta página da— es
más interesante que un ranking: **varios se siguen eligiendo, con razones sólidas; otros no se eligen y
se heredan; y saber la diferencia es lo que separa una decisión de una inercia.**

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es la **decisión tecnológica**, y estos lenguajes la enseñan mejor que ninguno porque
> **llevan décadas siendo elegidos o no elegidos**, y las razones están documentadas por los hechos. Y
> aportan lo que a esta discusión le suele faltar: **el largo plazo**. Un lenguaje elegido hoy tendrá que
> mantenerse en 2045, con otro equipo, otro hardware y otras herramientas — y varios de esta página son la
> única evidencia empírica que existe sobre qué pasa entonces.
>
> Y aparece el criterio que casi nunca está en las comparativas: **¿quién va a mantener esto, y estará?**
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: una palabra: `sistemas`, `web` o `datos` → stdout: `lenguaje=<Rust|TypeScript|SQL>`
- **Regla:** `sistemas→Rust, web→TypeScript, datos→SQL`

| stdin | esperado |
|---|---|
| `sistemas` | `lenguaje=Rust` |
| `web` | `lenguaje=TypeScript` |
| `datos` | `lenguaje=SQL` |

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
PROGRAM-ID. ELEGIR.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  DOMINIO PIC X(20).
01  LENG    PIC X(20).

PROCEDURE DIVISION.
    ACCEPT DOMINIO

    EVALUATE FUNCTION TRIM(DOMINIO)
        WHEN "sistemas" MOVE "Rust"       TO LENG
        WHEN "web"      MOVE "TypeScript" TO LENG
        WHEN "datos"    MOVE "SQL"        TO LENG
        WHEN OTHER      MOVE "?"          TO LENG
    END-EVALUATE

    DISPLAY "lenguaje=" FUNCTION TRIM(LENG)
    STOP RUN.
```

**¿Cuándo se elige COBOL hoy?** La respuesta honesta: **casi nunca para un sistema nuevo, y con muy buenas
razones para no reescribir el existente.**

**Por qué no para lo nuevo:**

- **El ecosistema no está**: no hay bibliotecas para JSON moderno, criptografía, HTTP o nube sin recurrir
  a otros lenguajes.
- **La contratación es un problema real** (clase 154), y empeora cada año.
- **Y las herramientas** —editores, análisis, dependencias— están décadas por detrás.

**Y por qué sí para lo que ya existe, que es el argumento que casi nadie escucha:**

```text
- 200.000-800.000 millones de líneas en producción
- Ejecutando el 43 % de los sistemas bancarios
- Con una fiabilidad medida en décadas
- Y una lógica de negocio que NO ESTÁ DOCUMENTADA en ninguna otra parte (clase 154)
```

**Las reescrituras de sistemas COBOL fracasan con una frecuencia bien documentada** (clase 150), y el
motivo no es técnico: **es que el comportamiento real del sistema viejo, con sus treinta años de casos
particulares, no está escrito en ningún sitio salvo en su código**.

Y donde COBOL sigue siendo **objetivamente bueno** merece decirse, porque suele omitirse:

| Fortaleza | Por qué |
|---|---|
| **Aritmética decimal exacta** | `COMP-3` y `PIC S9(9)V99` (clase 045): sin sorpresas de redondeo |
| **Procesamiento de lotes enormes** | el modelo de fichero y el `SORT` son insuperables (clase 152) |
| **Legibilidad para no programadores** | un analista de negocio puede leer la regla |
| **Estabilidad** | código de 1985 compila hoy |

**La primera es una ventaja real sobre la mayoría de los lenguajes modernos**, donde el decimal exacto
requiere una biblioteca y disciplina.

Y la estrategia sensata para un sistema COBOL, que es la de toda esta parte: **no reescribir, exponer**
(clases 149 y 160). La lógica se queda donde funciona; lo nuevo se escribe fuera y habla con ella por una
frontera bien definida.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program elegir
   implicit none
   character(len=20) :: dominio, lenguaje

   read(*, '(A)') dominio
   dominio = adjustl(dominio)

   select case (trim(dominio))
   case ('sistemas'); lenguaje = 'Rust'
   case ('web');      lenguaje = 'TypeScript'
   case ('datos');    lenguaje = 'SQL'
   case default;      lenguaje = '?'
   end select

   write(*, '(A)') 'lenguaje=' // trim(lenguaje)
end program elegir
```

**¿Cuándo se elige Fortran hoy?** Esta es de las respuestas más claras de la página: **para cálculo
numérico intensivo sobre arreglos, sigue siendo una elección defendible — y a veces la mejor.**

**Las razones son técnicas y concretas:**

**Una, los arreglos son ciudadanos de primera clase.** Operaciones de arreglo completo, secciones,
`reshape`, `matmul`, reducciones — **con una sintaxis que expresa la intención y que el compilador
vectoriza bien** (clase 089).

**Dos, la ausencia de solapamiento por defecto.** En C, dos punteros pueden apuntar al mismo sitio, así
que el compilador no puede reordenar; **en Fortran, los argumentos no se solapan salvo que se declare**,
y eso permite optimizaciones que en C requieren `restrict` y esperanza.

**Tres, sesenta años de bibliotecas validadas** (clase 149): BLAS, LAPACK, FFTW, PETSc, ARPACK. **Nadie va
a reescribir eso, y su corrección está probada por un uso masivo.**

**Y cuatro, es el lenguaje del paralelismo científico**: MPI y OpenMP tienen soporte de primera en
Fortran, y las herramientas de los superordenadores lo esperan.

**Y las razones en contra, que también son reales:**

| Debilidad | Consecuencia |
|---|---|
| Manejo de texto pobre | cualquier cosa con cadenas es tedioso (clase 093) |
| Sin gestor de paquetes maduro | `fpm` es de 2020 (clase 143) |
| Ecosistema pequeño fuera del cálculo | nada de web, ni de nube, ni de interfaces |
| Legado difícil | `COMMON`, formato fijo, `GOTO` (clase 150) |

**Y la arquitectura que la comunidad ha convergido es la de la clase 155**: **Python arriba, Fortran
abajo**.

Es una elección poliglota deliberada, y es un buen ejemplo del cierre de esta clase: **el lenguaje
aburrido y productivo para el 90 %, y el especializado para el núcleo que lo justifica**.

Y si el proyecto es nuevo y numérico, hoy la decisión real es **Fortran moderno frente a C++ con Eigen
frente a Julia** — y la respuesta depende sobre todo del equipo y de las bibliotecas que ya se vayan a
usar.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO; use Ada.Text_IO;

procedure Elegir is
   Linea  : String (1 .. 20);
   Ultimo : Natural;
begin
   Get_Line (Linea, Ultimo);

   if Linea (1 .. Ultimo) = "sistemas" then
      Put_Line ("lenguaje=Rust");
   elsif Linea (1 .. Ultimo) = "web" then
      Put_Line ("lenguaje=TypeScript");
   elsif Linea (1 .. Ultimo) = "datos" then
      Put_Line ("lenguaje=SQL");
   else
      Put_Line ("lenguaje=?");
   end if;
end Elegir;
```

**¿Cuándo se elige Ada hoy?** Y aquí hay una respuesta que sorprende a mucha gente: **se sigue eligiendo,
para sistemas nuevos, y no solo por inercia.**

**Dónde se elige de verdad:**

```text
Aviónica civil y militar, control ferroviario (ERTMS), satélites y lanzadores,
sistemas de defensa, dispositivos médicos, control industrial crítico.
```

**Y las razones son las que este curso ha ido mostrando:**

| Razón | Clase |
|---|---|
| **Tipos con rango y unidades**: los errores se vuelven imposibles de escribir | 124 |
| **Contratos comprobados o demostrados** con SPARK | 118 |
| **Concurrencia analizable** con Ravenscar: se demuestran los plazos | 135, 146 |
| **Sin sorpresas**: nada de comportamiento indefinido | 136 |
| **Legibilidad**: el código lo revisa gente que no lo escribió | 146 |
| **Estabilidad**: código de 1995 compila hoy, y lo hará en 2045 | 154 |

**Y la fila de SPARK es la que hace la diferencia hoy**: **demostrar matemáticamente la ausencia de
errores de ejecución** es una capacidad que, en producción industrial, tienen muy pocos lenguajes.

Y merece la comparación honesta con Rust, porque es la que se plantea en 2026:

| | Ada/SPARK | Rust |
|---|---|---|
| Seguridad de memoria | sí, y **demostrable** | sí, por el sistema de tipos |
| Ecosistema | **pequeño** | grande y creciente |
| Contratación | **muy difícil** | difícil, mejorando |
| Certificación | **madura**: DO-178C, EN 50128 | **en construcción** |
| Herramientas de demostración | **gnatprove, maduro** | Kani, Creusot: jóvenes |
| Concurrencia | tareas y Ravenscar, analizable | sin carreras, con `Send`/`Sync` |

**La fila de la certificación es la decisiva en estos sectores**: hay cadenas de herramientas Ada
cualificadas y décadas de evidencia ante los reguladores. **Rust está llegando, y todavía no está.**

Y la conclusión práctica del cierre de esta clase: **Ada se elige cuando el coste de un fallo es mucho
mayor que el coste del desarrollo**. Fuera de esos dominios, el ecosistema y la contratación pesan más —
y eso es una decisión racional, no un desprecio.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Elegir;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  Dominio: string;

begin
  ReadLn(Dominio);
  Dominio := Trim(Dominio);

  if Dominio = 'sistemas' then WriteLn('lenguaje=Rust')
  else if Dominio = 'web' then WriteLn('lenguaje=TypeScript')
  else if Dominio = 'datos' then WriteLn('lenguaje=SQL')
  else WriteLn('lenguaje=?');
end.
```

**¿Cuándo se elige Object Pascal hoy?** La respuesta honesta: **rara vez para algo nuevo desde cero, y
con argumentos reales para un nicho concreto — aplicaciones de escritorio nativas.**

**Lo que sigue siendo bueno:**

| Fortaleza | Detalle |
|---|---|
| **Compilación rapidísima** | un proyecto grande compila en segundos (clase 123) |
| **Binario autocontenido y pequeño** | sin instalar nada en el destino (clase 144) |
| **Interfaces nativas de verdad** | no un navegador empaquetado |
| **Compilación cruzada trivial** | Free Pascal, a casi cualquier destino (clase 147) |
| **Legibilidad** | fue diseñado para eso (clase 152) |
| **Estabilidad** | código de 1997 sigue compilando |

**Y lo que pesa en contra, que es mucho:**

- **La comunidad se ha reducido**, y con ella las bibliotecas para lo nuevo.
- **Delphi es comercial y caro**; Free Pascal y Lazarus son libres pero con menos pulido.
- **La contratación es difícil**, y el perfil medio es de más edad (clase 154).
- **Y el mundo se movió a la web y al móvil**, donde su presencia es marginal.

Y merece decir dónde sigue vivo de verdad, porque no es poco: **decenas de miles de aplicaciones de
gestión, de punto de venta, de laboratorio y de control industrial en Europa y Latinoamérica**, muchas
con veinte años y en mantenimiento activo.

**Es un ecosistema real, con clientes que pagan, y su problema no es técnico: es demográfico.**

Y hay un uso de Pascal que sí es indiscutible hoy y merece cerrar con él: **enseñar**.

**Pascal se diseñó para eso** (clase 152), y sigue siendo excelente: **sintaxis explícita, sin trampas,
con un compilador rápido y mensajes de error claros** (clase 137).

Y hay un argumento adicional que este curso hace evidente: **quien aprende Pascal entiende después
cualquier lenguaje imperativo con tipos**, porque **Pascal hace visible lo que otros esconden** —la
diferencia entre asignar y comparar, entre valor y referencia, entre declarar y usar—.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let ((dominio (string-trim '(#\Space #\Return) (read-line))))
  (format t "lenguaje=~A~%"
          (cond ((string= dominio "sistemas") "Rust")
                ((string= dominio "web") "TypeScript")
                ((string= dominio "datos") "SQL")
                (t "?"))))
```

**¿Cuándo se elige Common Lisp hoy?** Es de las respuestas más matizadas de la página: **se elige poco, y
quienes lo eligen tienen razones muy concretas y bastante buenas.**

**Dónde brilla de verdad:**

| Caso | Por qué |
|---|---|
| **Problemas mal definidos** | el ciclo de exploración es el más corto que existe (clase 124) |
| **Dominios con lógica compleja** | las macros permiten construir el vocabulario (clase 149) |
| **Sistemas que no pueden pararse** | redefinición en caliente (clase 148) |
| **Manipulación simbólica** | álgebra, demostradores, compiladores, planificación |
| **Prototipos que acaban en producción** | el prototipo **es** el sistema |

**Y los casos reales que merece conocer**: **Maxima** (álgebra simbólica), **ITA Software** —el motor de
búsqueda de vuelos que compró Google y que sigue moviendo reservas aéreas—, **Grammarly** en sus
comienzos, y buena parte de la investigación en planificación y en demostración automática.

**Y las razones en contra son igual de reales:**

- **El ecosistema es pequeño**: para casi cualquier problema moderno hay más y mejores bibliotecas en
  otros lenguajes.
- **La contratación es muy difícil.**
- **Y la sintaxis de paréntesis, aunque no es realmente un problema para quien la usa, sí lo es para
  convencer a un equipo.**

Y merece señalar la influencia, porque es la parte de Lisp que más se subestima y que este curso ha ido
mostrando:

```text
De Lisp salieron: la recolección de basura, las funciones de primera clase, los cierres,
la evaluación perezosa, el REPL, las excepciones con reinicios, las macros higiénicas,
el tipado dinámico moderno, la programación funcional aplicada,
y buena parte del diseño de los IDE.
```

**Prácticamente todo lo que hoy se considera moderno en un lenguaje de alto nivel apareció primero en
Lisp**, entre 1958 y 1985.

Y la conclusión para el cierre de esta clase: **si el problema es explorar algo que nadie ha resuelto y
el equipo es pequeño y bueno, Lisp sigue siendo una elección defendible**. Si el problema es conocido y
el equipo va a crecer, casi con seguridad no.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin dominio
set d [string trim $dominio]

switch -exact -- $d {
    sistemas { set l "Rust" }
    web      { set l "TypeScript" }
    datos    { set l "SQL" }
    default  { set l "?" }
}

puts "lenguaje=$l"
```

**¿Cuándo se elige Tcl hoy?** La respuesta es la más específica de esta página: **para incrustar, y para
las plataformas donde ya está.**

**Donde sigue siendo la elección correcta:**

| Caso | Por qué |
|---|---|
| **Lenguaje de extensión de una aplicación en C** | para eso se diseñó (clases 155 y 163) |
| **Automatizar herramientas interactivas** | Expect no tiene sustituto real (clase 147) |
| **Diseño de circuitos** | es el lenguaje de todas las herramientas del sector |
| **Interfaces rápidas y multiplataforma** | Tk sigue siendo la forma más corta de hacer una ventana |
| **Guiones que deben durar décadas** | compatibilidad hacia atrás extrema (clase 154) |

**La primera fila es la que aguanta el argumento**: comparado con Lua —su competidor natural—, Tcl es más
grande y más lento, pero trae **más batería incluida**: sockets, bucle de eventos, expresiones regulares,
Tk, y un modelo de seguridad maduro (clase 153).

**Y la tercera es la que garantiza su supervivencia**: **el sector del diseño de circuitos no va a
cambiar de lenguaje de guion**, porque sus flujos tienen décadas y un valor enorme.

**Y las razones para no elegirlo en un proyecto nuevo genérico:**

- **La comunidad es pequeña** y las bibliotecas modernas escasean.
- **El modelo "todo es una cadena"** produce un rendimiento peculiar (clase 152) y sorpresas de citación
  (clase 146).
- **Y Python y Lua ocupan hoy sus dos nichos naturales** con ecosistemas mucho mayores.

Y merece cerrar con lo que Tcl aportó y que sí sobrevive en todas partes, porque es la parte importante de
su legado:

**La tesis de los dos lenguajes** (clase 155): que un sistema se construye mejor con un lenguaje de
sistemas para los componentes y uno de guion para unirlos.

**Esa idea ganó tan completamente que hoy es invisible**: cada aplicación con complementos, cada
herramienta con configuración programable y cada motor de juego con guiones **está aplicando el argumento
de Ousterhout de 1998**, aunque use Lua, Python o JavaScript.

Es la mejor forma de éxito que puede tener una idea: **que nadie recuerde que hubo que defenderla**.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $dominio = <STDIN>;
chomp $dominio;

my %mapa = (sistemas => 'Rust', web => 'TypeScript', datos => 'SQL');

print "lenguaje=", ($mapa{$dominio} // '?'), "\n";
```

**¿Cuándo se elige Perl hoy?** La respuesta honesta y sin adornos: **para texto, y para mantener lo que
ya existe.**

**Donde sigue siendo objetivamente bueno:**

| Caso | Por qué |
|---|---|
| **Transformar texto a gran escala** | las expresiones regulares siguen siendo las mejores (clase 093) |
| **Guiones de una línea** | `perl -ne` es imbatible para lo desechable |
| **Bioinformática** | BioPerl y décadas de canalizaciones |
| **Sistemas heredados** | hay mucho, funcionando |
| **Está instalado en todas partes** | en cualquier Unix, sin instalar nada |

**Y merece reconocer que su motor de expresiones regulares definió el estándar**: **PCRE —*Perl
Compatible Regular Expressions*— es la biblioteca que usan PHP, Nginx, Apache, R y decenas más**.

**El nombre lo dice todo: el estándar de facto de las expresiones regulares se llama "compatible con
Perl".**

**Y las razones para no elegirlo hoy en un proyecto nuevo:**

- **Python ocupó su nicho** —guiones, administración, ciencia de datos, texto— con una comunidad mucho
  mayor y un código más legible por defecto.
- **La saga de Perl 6** —anunciado en 2000, publicado en 2015 y finalmente renombrado a Raku en 2019—
  **paralizó la percepción del lenguaje durante quince años**, aunque Perl 5 siguió mejorando todo ese
  tiempo.
- **Y su fama de ilegible**, merecida a medias: **Perl permite escribir código horrible**, y muchos lo
  hicieron; **también permite escribirlo bien** (clase 146), y menos gente lo hizo.

Y merece cerrar con lo que Perl dejó y que este curso ha ido señalando, porque es una lista notable:

```text
CPAN, el primer archivo de paquetes de un lenguaje (clase 143)
TAP, el protocolo de pruebas (clase 139)
CPAN Testers, integración continua distribuida (clase 147)
El modo taint (clase 153)
POD, documentación embebida (clase 154)
Perl Best Practices y perlcritic, con severidades (clase 146)
Y las expresiones regulares tal como hoy las usa todo el mundo
```

**Casi todo lo que un ecosistema de lenguaje moderno da por supuesto lo inventó o lo popularizó Perl**, y
esa es una forma de vigencia que no aparece en los índices de popularidad.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>
#include <string>

int main() {
    std::string dominio;
    if (!std::getline(std::cin, dominio)) return 1;

    const std::string leng =
        dominio == "sistemas" ? "Rust" :
        dominio == "web"      ? "TypeScript" :
        dominio == "datos"    ? "SQL" : "?";

    std::cout << "lenguaje=" << leng << '\n';
    return 0;
}
```

**¿Cuándo se elige C++ hoy?** Es de los pocos de esta página que **se elige constantemente para proyectos
nuevos**, y merece decir con precisión cuándo y cuándo no.

**Donde es la elección correcta:**

| Caso | Por qué |
|---|---|
| **Rendimiento con abstracción** | plantillas y `constexpr`: cero coste en ejecución (clase 123) |
| **Motores de juego y gráficos** | Unreal, y todo el ecosistema de renderizado |
| **Sistemas embebidos potentes** | automoción, robótica, imagen médica |
| **Alta frecuencia y baja latencia** | control total sobre memoria y disposición (clase 152) |
| **Bibliotecas para otros lenguajes** | es el sustrato de casi todos (clase 155) |
| **Bases de datos y compiladores** | LLVM, ClickHouse, MongoDB, MySQL |

**Y donde ya no es la elección obvia, que es la novedad de la última década:**

```text
Para sistemas NUEVOS donde la seguridad de memoria importa,
Rust ofrece un rendimiento comparable con garantías que C++ no puede dar (clase 153).

Y varias agencias de seguridad lo recomiendan explícitamente para código nuevo.
```

**Merece la comparación honesta**, porque es la decisión real de 2026:

| | C++ | Rust |
|---|---|---|
| Rendimiento | equivalente | equivalente |
| **Seguridad de memoria** | **no**, sin disciplina y herramientas | **sí, por el compilador** |
| Ecosistema | **inmenso y maduro** | grande y creciente |
| Interoperabilidad con C | **nativa** | buena, con `unsafe` |
| Curva de aprendizaje | larga, con trampas | **empinada al principio** |
| Tiempo de compilación | malo | malo |
| Código existente | **miles de millones de líneas** | poco, comparativamente |

**Y la fila del código existente es la que decide en la práctica**: **nadie reescribe un motor de juego de
tres millones de líneas**, así que la estrategia real es **la que Android y Chromium aplican: código nuevo
en Rust, el existente en C++, con la frontera bien definida** (clases 156 y 157).

Es, exactamente, el cierre de esta clase: **poliglota por decisión, no por accidente**.

Y merece señalar que C++ no se ha quedado quieto: **C++11, 17, 20 y 23 cambiaron el lenguaje
profundamente** —lambdas, punteros inteligentes, `constexpr`, conceptos, rangos, corrutinas— y **el C++
moderno bien escrito es un lenguaje muy distinto del de 1998**.

El problema, que este curso ha señalado varias veces, es que **el lenguaje viejo sigue siendo válido**, así
que **un proyecto real contiene las cuatro décadas a la vez** (clase 154).

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

dcl-pi ELEGIR;
  dominio char(20) const;
end-pi;

dcl-s leng varchar(20);

select;
  when %trim(dominio) = 'sistemas'; leng = 'Rust';
  when %trim(dominio) = 'web';      leng = 'TypeScript';
  when %trim(dominio) = 'datos';    leng = 'SQL';
  other;                            leng = '?';
endsl;

dsply ('lenguaje=' + leng);

*inlr = *on;
return;
```

**¿Cuándo se elige RPG hoy?** La respuesta es la más condicionada de esta página: **si ya tienes un IBM i,
es una elección excelente; si no lo tienes, la pregunta no es sobre el lenguaje.**

**Y merece explicar por qué la primera mitad es verdad**, porque suele darse por supuesto que no:

| En IBM i, RPG da | Detalle |
|---|---|
| **Acceso a datos sin fricción** | la base de datos es el sistema operativo (clase 139) |
| **SQL embebido de primera** | comprobado en compilación (clase 163) |
| **Rendimiento excelente en gestión** | compilado, nativo, sin capas |
| **Observabilidad por defecto** | registro, pilas y auditoría sin configurar (clase 142) |
| **Despliegue y reversión triviales** | la lista de bibliotecas (clase 148) |
| **Compatibilidad de décadas** | objetos de 1990 siguen funcionando |

**Y el RPG moderno —formato totalmente libre, procedimientos, programas de servicio, SQL, JSON con
`DATA-INTO`— es un lenguaje razonable** (clases 146 y 158), muy lejos del RPG de columnas que le dio la
fama.

**La decisión real, entonces, no es "¿RPG o Python?" sino "¿seguimos en IBM i?"** — y eso es una decisión
de plataforma con implicaciones enormes: hardware, licencias, personal y treinta años de aplicaciones.

**Y los argumentos en contra son de plataforma, no de lenguaje:**

- **Coste**: hardware POWER y licencias frente a máquinas genéricas y software libre.
- **Contratación**: el problema demográfico de la clase 154, agudo.
- **Ecosistema**: todo lo moderno llega, pero tarde y por PASE.
- **Y la dependencia de un único proveedor.**

Y merece cerrar con lo que esta plataforma enseña y que el resto de la industria está redescubriendo,
porque aparece una y otra vez en este curso: **integrar la base de datos, el sistema operativo, la
seguridad y la observabilidad en un solo sistema coherente da una productividad operativa que un montaje
de veinte piezas no alcanza**.

Es el argumento de fondo de las plataformas integradas, y explica por qué quien tiene un IBM i funcionando
rara vez se va — y por qué quien no lo tiene rara vez entra.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 elegir: procedure options(main);

    declare dominio char(20) varying;

    get edit (dominio) (a(20));
    dominio = trim(dominio);

    select (dominio);
       when ('sistemas') put skip list ('lenguaje=Rust');
       when ('web')      put skip list ('lenguaje=TypeScript');
       when ('datos')    put skip list ('lenguaje=SQL');
       otherwise         put skip list ('lenguaje=?');
    end;

 end elegir;
```

**¿Cuándo se elige PL/I hoy?** La respuesta más corta de esta página: **nunca para algo nuevo.**

Y merece explicar por qué con precisión, porque las razones son instructivas y ninguna es "el lenguaje es
malo":

**Una, no hay implementación libre** (clase 162). Es la razón estructural: **sin un compilador libre, el
lenguaje no llega a ninguna plataforma nueva** y depende por completo de que su propietario invierta.

**Dos, no hay comunidad ni ecosistema.** No hay gestor de paquetes, ni bibliotecas modernas, ni foros
activos, ni cursos.

**Tres, la contratación es prácticamente imposible** para nuevos proyectos.

**Y cuatro, lo que PL/I hacía bien lo hacen otros**: el decimal exacto lo tiene COBOL y lo tienen los tipos
decimales modernos; el cálculo lo hace Fortran; la programación de sistemas la hacen C, C++ y Rust.

**Y aun así, merece defender lo que fue**, porque este curso lo ha ido mostrando y es notable:

```text
PL/I tenía, en 1964, cosas que otros lenguajes tardaron décadas en tener:
  - manejo de excepciones con reanudación (clase 116)
  - concurrencia en el lenguaje
  - decimal exacto con precisión declarada (clase 045)
  - punteros y gestión de almacenamiento explícita
  - un preprocesador programable (clase 163)
  - y una biblioteca de funciones de arreglos y cadenas muy rica
```

**Fue el lenguaje más ambicioso de su época, y su ambición fue su problema** (clases 146 y 155): **un
lenguaje que sirve para todo es un lenguaje que nadie domina entero y que su compilador no puede
optimizar bien**.

Y la lección que deja para el cierre de esta clase es de las más útiles del curso, y no es sobre PL/I:

**El diseño de un lenguaje es un ejercicio de renuncia.** Lo que un lenguaje **prohíbe** es lo que
permite a su compilador optimizar, a sus herramientas analizar y a sus usuarios entenderlo.

Es la misma observación que Wirth aplicó con Pascal, Modula-2 y Oberon —**cada uno más pequeño que el
anterior**— y la que explica por qué los lenguajes que sobreviven suelen ser los que dijeron que no a
tiempo.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
ELEGIR ; Elegir lenguaje por dominio -- clase 164
 read dominio
 write "lenguaje=", $select(dominio="sistemas" : "Rust", dominio="web" : "TypeScript", dominio="datos" : "SQL", 1 : "?"), !
 quit
```

**¿Cuándo se elige M hoy?** La respuesta tiene dos mitades muy distintas, y merece separarlas porque casi
siempre se confunden: **el lenguaje, casi nunca; el motor de base de datos, más de lo que parece.**

**El lenguaje M no se elige para nada nuevo**, y las razones son claras: sin declaraciones, con ámbito
global por defecto (clase 146), con indirección imposible de analizar (clase 150) y con una sintaxis
que rechaza a cualquiera que llegue nuevo.

**Y el motor sí se elige, y merece explicar por qué**, porque es una tecnología genuinamente buena:

| Propiedad | Detalle |
|---|---|
| **Árboles jerárquicos ordenados y persistentes** | las globals (clase 099): esquema libre, con orden |
| **Transacciones ACID reales** | `tstart`/`tcommit`, con el código y los datos juntos (clase 161) |
| **Rendimiento en escrituras pequeñas** | miles de operaciones por segundo por núcleo |
| **Cero impedancia** | no hay traducción entre el lenguaje y la base (clase 099) |
| **Fiabilidad demostrada** | décadas en hospitales y en bancos, sin perder datos |

**Y ahí está la elección real de hoy: YottaDB como motor, con la aplicación en Go, Python, Rust o
Node** (clase 156).

Eso da lo bueno de M —**el modelo de datos y la transaccionalidad**— sin lo malo —**el lenguaje**—, y es
la dirección en la que este ecosistema se está moviendo.

**Y merece nombrar dónde M está hoy, porque es más de lo que se supone:**

```text
Sanidad:  VistA (Veteranos de EE. UU.), Epic (el mayor proveedor de historia
          clínica del mundo, sobre InterSystems), y sistemas nacionales en varios países
Finanzas: Ameritrade y varios sistemas de negociación
Y decenas de sistemas nacionales de identidad y de registro
```

**Epic merece la mención**: mueve la historia clínica de cientos de millones de pacientes, **y su núcleo
funciona sobre una base de datos M** — un dato que sorprende a casi todo el mundo.

Y la conclusión para el cierre de esta clase: **M es el mejor ejemplo del curso de una tecnología juzgada
por su sintaxis en lugar de por su arquitectura**.

El lenguaje es indefendible con criterios de 2026. **El modelo de datos —árboles ordenados,
persistentes, transaccionales, sin impedancia— es una idea excelente** que las bases de datos de clave y
valor redescubrieron cuarenta años después, casi siempre sin las transacciones.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| dominio |

dominio := stdin nextLine trimBoth.

Transcript
    show: 'lenguaje=', (dominio = 'sistemas'
        ifTrue: [ 'Rust' ]
        ifFalse: [ dominio = 'web'
            ifTrue: [ 'TypeScript' ]
            ifFalse: [ dominio = 'datos'
                ifTrue: [ 'SQL' ]
                ifFalse: [ '?' ] ] ]);
    cr.
```

**¿Cuándo se elige Smalltalk hoy?** Y con esta respuesta cierra la Parte 10, así que merece hacerla bien:
**rara vez, y su influencia está en todas partes.**

**Dónde se sigue eligiendo:**

| Caso | Por qué |
|---|---|
| **Dominios complejos y cambiantes** | modelar con objetos vivos es insuperable (clase 149) |
| **Sistemas que no pueden pararse** | actualización en caliente (clase 148) |
| **Análisis de software** | **Moose**: importar código ajeno como objetos (clase 155) |
| **Investigación y enseñanza** | Pharo y Squeak; Scratch está encima (clase 163) |
| **Finanzas con GemStone** | objetos transaccionales, en producción desde los noventa |

**Y las razones en contra, que son las de siempre**: comunidad pequeña, contratación muy difícil, y el
modelo de imagen (clase 144) que choca con todo el instrumental moderno —git, contenedores, integración
continua— hasta que se adapta (clase 145).

**Y ahora lo que merece decirse al cerrar la parte, porque es lo importante:**

```text
De Smalltalk salieron, y este curso las ha ido nombrando una por una:

  la interfaz gráfica con ventanas, iconos y ratón   (Xerox PARC → Apple → todos)
  MVC                                                  (clase 149)
  el patrón Observador en la raíz del sistema           (clase 149)
  las pruebas unitarias: SUnit → JUnit → todo lo demás   (clase 139)
  el desarrollo dirigido por pruebas                      (clase 139)
  la refactorización automática: el Refactoring Browser    (clase 150)
  la deuda técnica, como metáfora                           (clase 154)
  las cachés de envío en línea, base de todos los JIT        (clase 152)
  la programación extrema y buena parte de lo ágil
  y el propio término "orientado a objetos"
```

**Prácticamente todo lo que un equipo de software hace hoy por costumbre —escribir la prueba antes,
refactorizar con el IDE, hablar de deuda técnica, separar el modelo de la vista— salió de una comunidad
pequeña que trabajaba en un lenguaje que casi nadie usa.**

Y esa es la mejor conclusión posible para esta parte y para estas doce columnas: **el valor de un lenguaje
no se mide solo por cuánta gente lo usa, sino por cuánto de él acabó dentro de los demás**.

Y por eso este curso los ha recorrido: **no para que se usen —aunque varios se sigan usando— sino porque
en ellos están las decisiones originales, con sus razones intactas**, y entenderlas es lo que permite
tomar las propias con criterio en lugar de por costumbre.

---

## Y de vuelta a la clase

Lo transferible: **la elección de lenguaje casi nunca la decide el lenguaje**. La deciden el ecosistema
—las bibliotecas que ya existen para tu problema—, el equipo —lo que sabe y lo que puede contratar—, la
integración —con qué tiene que hablar— y el horizonte —cuántos años vivirá esto—. El rendimiento y la
elegancia importan mucho menos de lo que las discusiones sugieren, salvo en los pocos casos en que son el
requisito. Y la regla que más disgustos evita: **elegir el lenguaje aburrido para el 90 % del sistema y
reservar el interesante para el 10 % que lo justifica** — que es, exactamente, la arquitectura poliglota
de toda esta parte.

⏮️ [Volver a la clase 164](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
