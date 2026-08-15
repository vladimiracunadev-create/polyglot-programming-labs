# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 154

> [⬅️ Volver a la clase 154](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Contar módulos y llamarlo complejidad. Es una métrica tosca a propósito, porque esta clase trata de algo
que se mide mal y se paga siempre. Y estos lenguajes son el mejor sitio para hablar de ello, por una
razón sencilla: **son los que llevan más tiempo en mantenimiento**. Hay COBOL de 1968 en producción, y
**el término "deuda técnica" lo acuñó Ward Cunningham en 1992, en una conferencia sobre Smalltalk**,
describiendo exactamente lo que estos sistemas viven.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es el **coste de vivir con el código**, y estos lenguajes lo enseñan porque **han vivido
> con él más que nadie**. Y aportan las tres respuestas que existen a la pregunta de dónde va la
> documentación: **fuera del código** —los manuales del mainframe—, **dentro del código como comentario
> estructurado** —POD en Perl, Doxygen en C++, `;;` en M—, y **como parte del propio programa** —las
> cadenas de documentación de Lisp, el comentario de clase de Smalltalk, la especificación de Ada—.
>
> Y aparece la observación que más incomoda: **el código se lee muchas más veces de las que se escribe**,
> y casi todas las decisiones de estilo y estructura se toman pensando en escribirlo.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: una línea con nombres de módulos (palabras separadas por espacio) → stdout: `complejidad=<número de módulos>`
- **Regla:** `contar los módulos`

| stdin | esperado |
|---|---|
| `a b c` | `complejidad=3` |
| `x` | `complejidad=1` |
| `a b c d e` | `complejidad=5` |

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
PROGRAM-ID. COMPLEJ.
AUTHOR. CURSO-POLIGLOTA.

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
    DISPLAY "complejidad=" FUNCTION TRIM(ED)
    STOP RUN.
```

**Lo que esta clase enseña en COBOL.** Fíjate en `AUTHOR.` — es una entrada de la `IDENTIFICATION
DIVISION`, junto con `INSTALLATION`, `DATE-WRITTEN`, `DATE-COMPILED` y `SECURITY`.

**COBOL tiene una división entera dedicada a documentar quién, cuándo y para qué**, y es de 1959. Hoy se
consideran obsoletas —el control de versiones lo dice mejor (clase 145)— pero la intención merece
reconocerse: **el lenguaje reservó un sitio para el contexto**.

Y COBOL es el caso de estudio de esta clase, porque **es el código en mantenimiento más antiguo del
mundo**:

```text
Estimaciones publicadas (2020-2024):
  - entre 200.000 y 800.000 millones de líneas de COBOL en producción
  - el 43 % de los sistemas bancarios
  - el 95 % de las transacciones de cajero
  - y una edad media del código superior a los 30 años
```

**Y la deuda de estos sistemas tiene una forma muy concreta que merece describirse**, porque no es la que
la gente imagina:

**No es que el código sea malo.** Buena parte está bien escrito y funciona con una fiabilidad que pocos
sistemas modernos alcanzan.

**Es que el conocimiento se perdió.** Nadie sabe por qué ese campo se comprueba, ni qué regla de negocio
implementa ese `IF` de 1987, ni si esa excepción para el cliente 4711 sigue haciendo falta.

Y de ahí que la disciplina que esta clase defiende —**escribir por qué, no qué**— sea la más rentable de
todas:

```cobol
      *> Los pedidos anteriores a 1998 usan la tarifa antigua porque la
      *> migración de la circular 12/97 dejó fuera los contratos vitalicios.
      *> Ver expediente ARCH-4471. NO quitar sin consultar con Legal.
           IF FECHA-PEDIDO < 19980101
```

**Ese comentario vale más que el código que acompaña**, porque el código ya se ve y la razón no.

Y las herramientas modernas atacan exactamente ese problema:

| Herramienta | Qué hace |
|---|---|
| **IBM ADDI / watsonx Code Assistant** | extrae **reglas de negocio** del código, con IA |
| **CAST Imaging** | grafo completo del sistema: qué toca qué |
| **Micro Focus Enterprise Analyzer** | análisis de impacto y de código muerto |
| **SonarQube COBOL** | complejidad, duplicación, reglas |

**Y la métrica que estos sistemas usan y que merece conocerse es el código muerto**: en un sistema de
treinta años, **entre el 20 % y el 40 % del código no se ejecuta nunca** — párrafos de casos que ya no
existen, programas que nadie llama, campos que nadie lee.

Localizarlo y borrarlo es la devolución de deuda con mejor relación entre esfuerzo y beneficio que
existe, porque **cada línea que se borra es una línea que nadie tendrá que entender nunca más**.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program complej
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

   write(*, '(A,I0)') 'complejidad=', cnt
end program complej
```

**Lo que esta clase enseña en Fortran.** El código científico tiene un problema de mantenibilidad muy
característico, y merece nombrarlo sin rodeos: **casi todo lo escribió una persona sola, para un
artículo, sin intención de que nadie más lo leyera**.

Y las consecuencias se ven en el legado:

```fortran
      SUBROUTINE DGEMM(TRANSA,TRANSB,M,N,K,ALPHA,A,LDA,B,LDB,BETA,C,LDC)
```

**Trece argumentos posicionales con nombres de una letra.** Y sin embargo esa rutina es de las mejor
documentadas del mundo, porque **la comunidad numérica sí desarrolló una cultura de documentación**:

```fortran
!> @brief Multiplica matrices: C := alpha*op(A)*op(B) + beta*C
!!
!! @param[in]     transa  'N' sin transponer, 'T' transpuesta
!! @param[in]     m       filas de op(A) y de C. m >= 0.
!! @param[in,out] c       matriz de dimensión (ldc, n)
```

**El comentario de cabecera de las rutinas de LAPACK es tan detallado que hace de especificación**, y es
lo que ha permitido que decenas de implementaciones distintas sean intercambiables durante cuarenta años
(clase 149).

Y las herramientas del ecosistema:

| Herramienta | Notas |
|---|---|
| **FORD** | generador de documentación específico de Fortran moderno |
| **Doxygen** | con soporte de Fortran |
| **`!>` y `!!`** | las marcas de comentario de documentación |
| **fpm** | `fpm.toml` con metadatos del proyecto |

Y la deuda característica de este mundo merece describirse porque es de una forma que no aparece en
otros dominios: **la deuda de reproducibilidad**.

```text
Un artículo de 2004 cita resultados producidos con:
  - una versión del código que no está publicada
  - un compilador que ya no existe
  - unas bibliotecas de las que no se anotó la versión
  - y en una máquina que se desguazó
```

**Ese resultado no se puede reproducir**, y por tanto no se puede verificar ni construir encima con
confianza (clase 144).

Y la respuesta de la comunidad en la última década es exactamente devolución de deuda: **revistas que
exigen publicar el código, revisión de software científico, identificadores permanentes para el
software, y contenedores que congelan el entorno**.

Es la aplicación del cierre de esta clase a un campo entero: **se contrajo deuda durante cincuenta años
—entregar el resultado sin el andamiaje— y ahora se está devolviendo**, con esfuerzo y a destiempo, que
es como siempre se devuelve.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO; use Ada.Text_IO;
with Ada.Strings;
with Ada.Strings.Fixed;

--  Cuenta las palabras de una línea. La complejidad declarada del sistema
--  es, por convención de este ejercicio, el número de módulos.
procedure Complej is
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

   Put_Line ("complejidad=" &
             Ada.Strings.Fixed.Trim (Cnt'Image, Ada.Strings.Both));
end Complej;
```

**Lo que esta clase enseña en Ada.** Ada tiene la mejor respuesta estructural de esta página a la
pregunta de dónde va la documentación: **en la especificación**.

```ada
package Cuentas is

   --  Una cuenta corriente con saldo no negativo.
   --  El saldo se expresa en céntimos para evitar el redondeo binario.

   type Cuenta is private;

   function Saldo (C : Cuenta) return Importe
     with Post => Saldo'Result >= 0.00;

   procedure Retirar (C : in out Cuenta; Cantidad : Importe)
     with Pre  => Cantidad > 0.00 and then Cantidad <= Saldo (C),
          Post => Saldo (C) = Saldo (C'Old) - Cantidad;

private
   ...
end Cuentas;
```

**El fichero `.ads` es a la vez la interfaz, la documentación y el contrato comprobable** (clase 118).

Y las tres propiedades que eso da merecen destacarse, porque resuelven el problema clásico de la
documentación:

**Una, no se puede desincronizar.** Un contrato que deja de ser cierto **falla en ejecución o no
compila**. Un comentario que deja de ser cierto **no hace nada**, y por eso la mitad de los comentarios
de cualquier sistema viejo mienten.

**Dos, se lee sin el cuerpo.** Para usar el paquete no hace falta leer la implementación —**y no se
debe**—, lo que reduce el acoplamiento cognitivo.

**Y tres, es lo que se revisa** (clase 145): `git log -- '*.ads'` es la historia de las interfaces del
sistema.

Y las herramientas:

```bash
gnatdoc                    # documentación desde las especificaciones y sus comentarios
gnatmetric                  # complejidad ciclomática, anidamiento, líneas por unidad
gnatcheck                    # reglas de estilo (clase 146)
```

**`gnatmetric` merece la mención** porque da la métrica que esta clase nombra:

```text
Cyclomatic complexity   : 12
Essential complexity     :  3
Maximum loop nesting      :  2
```

**La complejidad esencial mide cuánto queda tras reducir las estructuras bien anidadas** — es decir,
**cuánto flujo de control no estructurado hay**. Un valor de 1 significa código perfectamente
estructurado; un valor alto significa marañas de saltos.

Y en el dominio de Ada hay una obligación que merece nombrarse y que casi ningún otro sector tiene: **la
documentación es un entregable contractual, con trazabilidad verificada** (clase 147).

Cada requisito enlaza con código y con pruebas, **y una herramienta comprueba que no falte ninguno**. Es
la versión más estricta de "escribir por qué", y funciona porque **está en el mismo sistema que impide
entregar sin ella**.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Complej;
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

  WriteLn('complejidad=', IntToStr(Cnt));
end.
```

**Lo que esta clase enseña en Pascal.** Pascal fue **diseñado para ser legible**, y merece reconocerlo
porque es una decisión de diseño explícita de Niklaus Wirth y no un accidente.

```pascal
begin ... end        { en vez de llaves }
:=  para asignar      { distinto de = para comparar }
procedure / function   { la diferencia se declara }
```

**La verbosidad de Pascal es deliberada**, y su objetivo era exactamente el del cierre de esta clase:
**que el código se leyera bien**, porque se lee muchas más veces de las que se escribe.

Y Wirth llevó ese principio más lejos que nadie, con una regla que merece conocerse porque es célebre en
el diseño de lenguajes: **cada lenguaje que diseñó era más pequeño que el anterior** —Pascal, Modula-2,
Oberon—, y sobre Oberon escribió que quitó **todo lo que no fuera imprescindible**.

**Su criterio: una característica solo entra si su beneficio supera el coste de que todo el mundo tenga
que aprenderla y leerla.** Es un criterio de mantenibilidad aplicado al lenguaje mismo, y es lo contrario
de lo que hizo PL/I (clase 146).

Y las herramientas del ecosistema:

| Herramienta | Qué hace |
|---|---|
| **PasDoc** | genera documentación desde comentarios `{** ... }` |
| **fpdoc** | el de Free Pascal, con descripciones en XML **separadas del código** |
| **Pascal Analyzer** | métricas, código muerto, variables no usadas, ámbitos |
| **`deprecated` / `experimental` / `platform`** | **marcas del lenguaje** |

**Las marcas del lenguaje merecen destacarse** porque son documentación que el compilador hace cumplir:

```pascal
procedure MetodoViejo; deprecated 'usa MetodoNuevo desde la versión 3.2';
function Experimental: Integer; experimental;
procedure SoloWindows; platform;
```

**Usar algo marcado como obsoleto produce un aviso con el texto**, y con `{$WARN SYMBOL_DEPRECATED
ERROR}` se convierte en error (clase 146).

Es la mejor forma de gestionar la deuda de una interfaz: **no borrar de golpe, sino marcar, avisar y dar
una fecha** — que es el ciclo de retirada que cualquier biblioteca con usuarios necesita.

Y **fpdoc merece la mención por su decisión contraria a la moda**: la documentación va en **ficheros XML
separados**, no en comentarios. La ventaja es que **se puede traducir y editar sin tocar el código**; la
desventaja, la de siempre: **lo que está separado se desincroniza**.

Es el compromiso central de esta clase, y las dos posturas siguen vivas.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(defun contar-palabras (linea)
  "Devuelve cuántas palabras separadas por espacios contiene LINEA."
  (let ((cnt 0) (en-palabra nil))
    (loop for c across linea
          do (if (char= c #\Space)
                 (setf en-palabra nil)
                 (unless en-palabra (setf en-palabra t) (incf cnt))))
    cnt))

(format t "complejidad=~D~%" (contar-palabras (read-line)))
```

**Lo que esta clase enseña en Common Lisp.** Fíjate en la cadena que hay justo debajo del nombre de la
función: **eso no es un comentario. Es una *docstring*, y forma parte del objeto función**.

```lisp
(documentation 'contar-palabras 'function)
;; → "Devuelve cuántas palabras separadas por espacios contiene LINEA."

(describe 'contar-palabras)
```

**Lisp inventó la cadena de documentación**, y merece reconocerse la importancia: es la idea que después
adoptaron Python, Elixir, Julia, Clojure y Rust, y que convierte la documentación **de un comentario que
el compilador descarta en un dato que el sistema conserva**.

Y las consecuencias son grandes:

- **`C-c C-d d` en el editor muestra la documentación de cualquier función**, incluida la de las
  bibliotecas cargadas, sin salir del entorno.
- **`apropos` busca por texto** en toda la documentación del sistema.
- **Y se puede escribir un generador de documentación en veinte líneas**, porque los datos ya están ahí.

Es la tercera respuesta del "por qué" de esta clase —**la documentación como parte del programa**— y es
la que menos se desincroniza, porque **está en el mismo sitio que la definición**.

Y el ecosistema:

| Herramienta | Notas |
|---|---|
| **`documentation` / `describe` / `apropos`** | en el estándar |
| **Declt, Coo, Staple** | generadores de documentación |
| **SLIME** | documentación, argumentos y ejemplos en el editor |
| **`sb-cover`** | cobertura, como indicador de qué está probado |

Y Lisp aporta a esta clase una forma de deuda técnica muy propia y que merece explicarse: **la deuda de
macros**.

Una macro bien elegida hace el código más claro (clase 122). **Y una macro innecesaria crea un lenguaje
privado que solo su autor entiende** — y que las herramientas no entienden en absoluto (clase 150).

La regla que la comunidad consolidó, y que es un buen ejemplo de la primera práctica del cierre: **si se
puede hacer con una función, hazlo con una función**. Las macros son para lo que requiere controlar la
evaluación —crear enlaces, retrasar, envolver— y nada más.

Y hay una forma de deuda que solo tienen los lenguajes con imagen (clase 145) y que conviene nombrar:
**el conocimiento que vive en la imagen y no en el repositorio** — funciones redefinidas al vuelo,
configuraciones probadas en el REPL, estado que nadie sabe cómo se construyó.

Se paga el día que hay que arrancar de cero, y entonces se paga entera.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea

set n [llength [split [string trim $linea]]]

puts "complejidad=$n"
```

**Lo que esta clase enseña en Tcl.** Tcl tiene una cultura de documentación notablemente fuerte para su
tamaño, y merece explicar por qué: **el lenguaje se define por sus páginas de manual**.

**Cada comando de Tcl tiene una página de manual**, escrita con un rigor poco común, y **esa página es la
especificación**. No hay un documento estándar aparte: **las páginas de manual son el estándar**.

Y el ecosistema construyó su propio formato:

```tcl
[manpage_begin miPaquete n 1.2]
[titledesc {Utilidades de proceso}]
[require Tcl 8.6]
[description]
[list_begin definitions]
[call [cmd ::mipkg::procesar] [arg datos] [opt [arg opciones]]]
Procesa [arg datos] y devuelve el resultado.
[list_end]
[manpage_end]
```

**`doctools` genera desde ahí páginas de manual, HTML, texto y wiki**, y es lo que usan tcllib y tklib
para documentar cientos de módulos.

Y Tcl aporta a esta clase una lección sobre deuda que su propia historia ilustra bien y que merece
contarse con honestidad: **el coste de no romper la compatibilidad**.

Tcl mantiene compatibilidad hacia atrás con una disciplina extrema: **código de 1993 sigue funcionando**.
Y eso tiene las dos caras:

**A favor**: los sistemas escritos en Tcl —flujos de diseño de circuitos de decenas de miles de líneas
(clase 149)— **han sobrevivido treinta años sin reescrituras**. En una industria donde cada migración de
versión de un lenguaje cuesta meses, eso tiene un valor enorme.

**En contra**: **las decisiones antiguas se quedan**. `string is lower` sin `-strict` devuelve verdadero
para la cadena vacía (clase 153); `expr` sin llaves sigue permitido; el modelo de codificación de texto
arrastró limitaciones durante años.

Y la forma en que Tcl gestiona esa deuda es la que merece extraerse, porque es la práctica correcta:
**añadir lo nuevo sin quitar lo viejo, y marcar la diferencia**.

```tcl
package require Tcl 8.6      ;# el código declara qué necesita
```

Y en Tcl 9 —la primera ruptura importante en décadas— **la comunidad publicó una guía de migración
detallada y mantuvo 8.6 en soporte**, que es lo que separa una transición de un abandono.

Es la aplicación del cierre de esta clase a escala de lenguaje: **la deuda se lleva en cuenta, se anuncia
y se devuelve por partes** — y treinta años de compatibilidad son, ellos mismos, el interés que se
decidió pagar a cambio de que nadie tuviera que reescribir nada.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

=head1 NAME

complej - cuenta los módulos de una línea

=head1 DESCRIPTION

Lee una línea de nombres separados por espacios y devuelve cuántos hay.

=cut

my $linea = <STDIN>;
chomp $linea;

my @modulos = split ' ', $linea;

print "complejidad=", scalar(@modulos), "\n";
```

**Lo que esta clase enseña en Perl.** Ese bloque entre `=head1` y `=cut` es **POD, *Plain Old
Documentation***, y es una de las contribuciones de Perl que más se ha imitado sin citar.

**POD es documentación embebida en el fuente, con marcado propio, que el intérprete IGNORA por
completo.**

```bash
perldoc script.pl        # leerla como página de manual
pod2html script.pl        # a HTML
pod2man script.pl          # a página de manual de Unix
podchecker script.pl        # comprobar que el marcado es válido
```

Y las propiedades que lo hacen bueno merecen destacarse:

**Primera, está junto al código que documenta**, así que se actualiza en el mismo cambio — que es el
argumento central de esta clase.

**Segunda, es legible en el fuente**: no es HTML ni XML, es texto con unas pocas marcas.

**Y tercera, y es la que lo hace único: se puede poner en cualquier parte del fichero**, incluso
intercalada entre funciones, y **el intérprete la salta**.

Y encima de POD, la comunidad construyó una convención de estructura que hoy se da por supuesta en
cualquier ecosistema:

```text
=head1 NAME / SYNOPSIS / DESCRIPTION / METHODS / DIAGNOSTICS
       / CONFIGURATION / DEPENDENCIES / BUGS AND LIMITATIONS
       / AUTHOR / LICENSE AND COPYRIGHT
```

**Y `Test::Pod` y `Test::Pod::Coverage` lo comprueban en la integración continua**:

```perl
all_pod_files_ok();                # ¿el POD es válido?
all_pod_coverage_ok();              # ¿está TODA función pública documentada?
```

**La segunda es la que convierte una buena intención en una regla**: una función pública sin
documentación **hace fallar las pruebas**.

Es la aplicación exacta de lo que la clase 146 defendía: **lo que una máquina puede comprobar, lo
comprueba la máquina**.

Y Perl aporta a esta clase una forma de deuda muy reconocible y que merece nombrar sin adornos: **el
guion que se convirtió en sistema**.

Un fichero de 200 líneas que nadie pensó mantener, y que diez años después tiene 8.000, ninguna prueba y
es crítico para la empresa. **Es la deuda técnica en su forma más pura**: se contrajo sin saber que se
estaba contrayendo.

Y la señal de alarma que conviene reconocer es simple y sirve en cualquier lenguaje: **el momento en que
alguien dice "no toques eso, nadie sabe cómo funciona"** — ahí ya no es un guion: es un sistema sin
dueño, y el interés lleva años acumulándose.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>
#include <string>

/// Cuenta los módulos (palabras) de una línea de entrada.
/// @param entrada flujo del que se leen las palabras
/// @return número de palabras encontradas
int contar(std::istream& entrada) {
    std::string palabra;
    int cnt = 0;
    while (entrada >> palabra) ++cnt;
    return cnt;
}

int main() {
    std::cout << "complejidad=" << contar(std::cin) << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** Los comentarios `///` con `@param` son **el formato de Doxygen**, que
merece una mención histórica: **Dimitri van Heesch lo publicó en 1997**, inspirado por Javadoc, y **se
convirtió en el estándar de facto para C, C++, y de ahí para media docena de lenguajes más**.

Su aportación fue combinar dos cosas: **comentarios estructurados junto al código** y **generación de
grafos**:

```text
Doxygen genera automáticamente:
  - el grafo de llamadas y de llamadores de cada función
  - el diagrama de herencia de cada clase
  - el grafo de dependencias entre ficheros de cabecera
  - y referencias cruzadas con el código fuente
```

**Los grafos de inclusión son lo que más valor tiene en un proyecto C++ grande**, porque hacen visible el
problema que la clase 149 describía: **las dependencias físicas de compilación**.

Y la deuda técnica en C++ tiene formas propias que merecen catalogarse, porque son caras:

| Forma de deuda | Coste |
|---|---|
| **Cabeceras que incluyen de más** | tiempo de compilación creciente (clase 147) |
| **Ciclos de dependencias** | imposible probar por partes |
| **Punteros desnudos heredados** | fugas y usos después de liberar (clase 153) |
| **Macros del preprocesador** | no se pueden depurar ni analizar |
| **Estándares antiguos** | no se puede usar lo que hace el código más simple |
| **Comportamiento indefinido latente** | funciona hasta que el compilador mejora |

**La última merece la advertencia**, porque es la más traicionera de esta página: **un programa con
comportamiento indefinido puede funcionar durante años y romperse al actualizar el compilador** — no
porque el compilador tenga un fallo, sino porque **una optimización nueva aprovechó una suposición que el
código violaba**.

Es deuda que no da señales hasta que vence, y por eso `-fsanitize=undefined` en la integración continua
(clase 147) es la forma de irla detectando.

Y las herramientas de medición de deuda:

```bash
lizard src/                       # complejidad ciclomática y funciones largas
cppcheck --enable=all              # análisis estático
include-what-you-use                # inclusiones innecesarias
sonar-scanner                        # deuda estimada en tiempo
```

**SonarQube expresa la deuda en horas**, con una fórmula discutible pero útil para una cosa concreta que
esta clase quiere subrayar: **hace la deuda visible en una unidad que un responsable de proyecto
entiende**.

Y ese es su valor real. La cifra exacta importa poco; **que exista una cifra que sube cuando se toman
atajos y baja cuando se limpian** es lo que convierte una discusión sobre calidad en una decisión de
planificación.

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

// Cuenta los modulos (palabras) de una linea.
// Autor: curso poliglota. Ver clase 154.

dcl-pi COMPLEJ;
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

dsply ('complejidad=' + %char(cnt));

*inlr = *on;
return;
```

**Lo que esta clase enseña en RPG.** IBM i tiene una forma de documentación que casi ningún sistema tiene
y que merece explicarse: **la descripción está en el objeto**.

```text
CHGOBJD OBJ(MIBIB/MIPGM) OBJTYPE(*PGM) TEXT('Calculo de intereses - circular 12/97')
DSPOBJD OBJ(MIBIB/*ALL) OBJTYPE(*ALL)
```

**Cada objeto del sistema —programa, tabla, cola, área de datos— lleva un texto descriptivo**, y
`DSPOBJD` lista una biblioteca entera con sus descripciones.

Y lo mismo con las columnas de la base de datos:

```sql
LABEL ON COLUMN clientes (nif IS 'Número de identificación fiscal');
COMMENT ON TABLE clientes IS 'Maestro de clientes. Origen: migración 2003.';
```

**Esas etiquetas aparecen en las consultas, en los informes y en las herramientas**, así que **la
documentación viaja con el dato**.

Es la misma idea que las cadenas de documentación de Lisp en esta página, aplicada al catálogo del
sistema, y merece reconocerse como buena: **el sitio correcto para describir algo es el sitio donde
alguien se lo va a encontrar**.

Y la deuda característica de esta plataforma merece describirse porque es muy reconocible:

**Uno, el código en formato fijo** (clase 146). Legible solo para quien creció con él, y con una plantilla
de columnas al lado.

**Dos, los indicadores numéricos.** `*IN03`, `*IN12`, `*IN99` repartidos por miles de líneas, cada uno
significando algo distinto según el contexto.

**Tres, los programas monolíticos** que mezclan pantalla, base de datos y cálculo (clase 149).

**Y cuatro, y es el que de verdad duele: la generación que lo escribió se está jubilando.**

Ese último punto merece tratarse con seriedad porque es un problema real y medible: **la edad media de
los desarrolladores de RPG y COBOL supera con claridad la del sector**, y el conocimiento de estos
sistemas **no está documentado en ninguna parte más que en las personas**.

Y las respuestas que funcionan son las de esta clase, aplicadas con urgencia:

| Práctica | Por qué |
|---|---|
| **Convertir a formato libre** | que alguien nuevo pueda leerlo (clase 150) |
| **Extraer a programas de servicio** | que se pueda probar y entender por partes |
| **Documentar el porqué de las reglas** | es lo que se va con las personas |
| **Y grabar las entrevistas** | literalmente: antes de que se jubilen |

**La última no es una broma**: varias organizaciones grandes tienen programas formales de captura de
conocimiento con las personas que se van, porque **el coste de perder el porqué es mucho mayor que el de
perder el código**.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 /* Cuenta los modulos de una linea. Clase 154 del curso poliglota. */
 complej: procedure options(main);

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

    put skip list ('complejidad=' || trim(char(cnt)));

 end complej;
```

**Lo que esta clase enseña en PL/I.** PL/I ilustra la forma de deuda técnica que menos se discute y que
más cara sale: **la deuda del tamaño**.

El lenguaje se diseñó para unirlo todo (clase 149), y el resultado fue **un lenguaje que casi nadie
dominaba entero**. Y eso tiene un coste de mantenimiento directo: **cada programador usa el subconjunto
que conoce, y todos usan subconjuntos distintos**.

**Un sistema PL/I grande acaba escrito en cinco dialectos internos**, según quién escribiera cada
módulo — uno lleno de `BASED` y punteros, otro de estructuras y `LIKE`, otro de condiciones y `ON`.

Es la razón de que los estándares de instalación de la clase 146 fueran tan restrictivos: **no eran
pedantería, eran la única forma de que el sistema siguiera siendo legible por un equipo**.

Y la lección general merece extraerse porque se aplica a cualquier lenguaje grande de hoy: **la
variabilidad de estilo es deuda técnica**, y el coste no es estético — es que **cada persona nueva tiene
que aprender varios dialectos en lugar de uno**.

Y la documentación en el mundo del mainframe sigue el modelo que el "por qué" de esta clase nombraba
primero: **fuera del código**.

```text
- Manual de diseño funcional
- Manual de diseño técnico
- Diagrama de flujo del sistema
- Descripción de ficheros y de registros
- Manual de operación: qué hacer si el paso 4 aborta
- Y el LISTADO DE COMPILACIÓN, archivado (clases 137 y 144)
```

**Y ese modelo tiene una virtud que merece reconocerse**: la documentación de operación —qué hacer
cuando algo falla a las 3:40 de la madrugada— **existe, está escrita y la usa gente que no programa**.

Es algo que muchos sistemas modernos no tienen, y que se echa en falta exactamente cuando hace falta.

**Y tiene el defecto conocido**: está separada, así que **se desincroniza**. Un sistema de treinta años
tiene manuales que describen una versión que ya no existe, y nadie sabe cuál de las dos miente.

Es el compromiso de esta clase en su forma más pura, y la conclusión razonable es la que la práctica ha
ido adoptando: **la documentación de interfaces y de comportamiento, junto al código; la de operación y
de contexto, donde la va a buscar quien la necesita** — y las dos con fecha y con dueño.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
COMPLEJ ; Contar modulos -- clase 154
 ;;1.0;CURSO POLIGLOTA;;Aug 15, 2026
 ; Lee una linea y devuelve cuantos nombres separados por espacios contiene.
 read linea
 new i, cnt, p
 set cnt = 0
 for i = 1:1:$length(linea, " ") do
 . set p = $piece(linea, " ", i)
 . if p '= "" set cnt = cnt + 1
 write "complejidad=", cnt, !
 quit
```

**Lo que esta clase enseña en M.** Fíjate en la segunda línea: **`;;1.0;CURSO POLIGLOTA;;Aug 15, 2026`**.

**El doble punto y coma no es un comentario cualquiera: es la línea de versión de VistA**, y su formato
está fijado por el estándar:

```text
 ;;<versión>;<nombre del paquete>;**<lista de parches>**;<fecha>
 ;;8.0;KERNEL;**10,49,110,275**;Jul 10, 1995
```

**Ahí está la versión del paquete, todos los parches aplicados y la fecha de la versión base** — y el
sistema puede leerlo con `$text` (clase 123) para comprobar qué hay instalado.

Es **metadatos de versión dentro del código, legibles por el programa**, y es la pieza que hace posible
el sistema de parches de la clase 143.

Y M aporta a esta clase el ejemplo más extremo de una tensión que la atraviesa: **el código breve frente
al código legible**.

```mumps
 S %=$O(^A(""))  Q:%=""  D  Q
 . S %1=$G(^A(%,0)) I $P(%1,U,3)="Y" D EN^B(%)
```

**Eso es M idiomático de los años ochenta**, y era así por un motivo real: **la memoria y el espacio de
disco eran caros, y las rutinas tenían un tamaño máximo**. Los nombres de una letra y los comandos
abreviados **no eran pereza: eran una restricción**.

Y hoy esa restricción no existe, así que el mismo código se escribe:

```mumps
 new dfn
 set dfn = $order(^PACIENTE(""))
 for  quit:dfn=""  do
 . if $piece($get(^PACIENTE(dfn, 0)), "^", 3) = "Y" do procesar^ALTAS(dfn)
 . set dfn = $order(^PACIENTE(dfn))
```

**Y ahí está la lección de esta clase**: la deuda de aquel código no es que esté mal — **funcionaba y era
la decisión correcta en 1985**. La deuda es que **las razones desaparecieron y el estilo se quedó**.

Es la forma más común de deuda técnica y la más difícil de ver: **una decisión correcta cuyo contexto
cambió**.

Y por eso la práctica del cierre de esta clase —**escribir por qué**— es la defensa: un comentario que
diga "abreviado por el límite de tamaño de rutina de la versión 3" permite a quien lo lea treinta años
después **saber que la razón ya no aplica**.

Sin ese comentario, lo que queda es una convención que nadie entiende y que todos copian por respeto.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
"Cuenta los modulos (palabras) de una linea de entrada.
 Ver la clase 154 del curso poliglota."

| linea |

linea := stdin nextLine trimBoth.

Transcript show: 'complejidad=', (linea substrings: ' ') size printString; cr.
```

**Lo que esta clase enseña en Smalltalk.** Aquí está el dato del gancho, y merece contarse completo:
**Ward Cunningham acuñó la metáfora de la deuda técnica en 1992, en un informe de experiencia presentado
en OOPSLA** —la conferencia de programación orientada a objetos— **sobre un sistema financiero escrito en
Smalltalk**.

Y su formulación original es más matizada que como suele citarse, y merece leerse con cuidado:

> Entregar código por primera vez es como endeudarse. Una pequeña deuda acelera el desarrollo **siempre
> que se pague de inmediato con una reescritura**. El peligro aparece cuando la deuda no se devuelve.

**Dos precisiones que se pierden en el uso habitual:**

**Primera, Cunningham no hablaba de código malo.** Hablaba de **código que refleja un entendimiento
incompleto del problema** — se escribe lo que se entiende, se entrega, se aprende, y **entonces se
reescribe con el entendimiento nuevo**.

**Y segunda, la deuda es una herramienta legítima.** Contraerla a conciencia para aprender antes es
**buena ingeniería**. Lo que no lo es, es no devolverla.

Y Smalltalk aporta la infraestructura que hace eso practicable, y es toda de esta parte del curso: **el
Refactoring Browser** (clase 150), **SUnit** (clase 139) y **un ciclo de segundos** (clase 124).

**No es casualidad que la metáfora, la disciplina del refactorizado, las pruebas unitarias, TDD y los
patrones salieran de la misma comunidad en la misma década**: eran las herramientas y el vocabulario del
mismo problema.

Y sobre documentación, Smalltalk tiene la respuesta más radical de esta página:

```smalltalk
Cuenta class comment: 'Represento una cuenta corriente.
El saldo se guarda en céntimos para evitar el redondeo binario.
Ver la clase Transaccion para el registro de movimientos.'
```

**El comentario de clase es un objeto**, accesible con `Cuenta comment`, editable en el navegador y
**obligatorio por convención**: las herramientas de calidad avisan de las clases sin comentario.

Y a eso se suma lo que la clase 146 explicaba: **los métodos son cortos y los nombres son frases**, así
que **el código se lee como documentación**.

```smalltalk
coleccion detect: [ :cada | cada estaVencida ] ifNone: [ nil ]
```

Y merece cerrar esta clase, y con ella la Parte 9, con la métrica que Smalltalk permite y casi nadie
más:

```smalltalk
SystemNavigation default allUnsentMessages.     "métodos que nadie llama: CÓDIGO MUERTO"
```

**Preguntar al sistema entero qué código no usa nadie**, y borrarlo. Es la devolución de deuda con mejor
relación entre esfuerzo y beneficio, y coincide exactamente con lo que COBOL señalaba al principio de
esta página: **en un sistema viejo, entre el 20 % y el 40 % del código está muerto**.

**Cada línea borrada es una línea que nadie tendrá que entender nunca más** — y ese, al final, es el
único indicador de mantenibilidad que no engaña.

---

## Y de vuelta a la clase

Lo transferible: **la deuda técnica es una metáfora financiera y hay que tomarla en serio como tal** —se
contrae a propósito para entregar antes, y **paga intereses en forma de cada cambio futuro más lento**—.
Lo que la convierte en un problema no es contraerla: es **no llevar la cuenta y no devolverla nunca**. De
ahí las dos prácticas que funcionan: **escribir por qué, no qué** —el código ya dice qué hace; lo que se
pierde es la razón—, y **dejar constancia de la deuda donde se contrae**, con una nota que diga qué se
sacrificó y a cambio de qué. Un sistema de veinte años es legible o ilegible según se haya hecho eso,
no según el lenguaje.

⏮️ [Volver a la clase 154](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
