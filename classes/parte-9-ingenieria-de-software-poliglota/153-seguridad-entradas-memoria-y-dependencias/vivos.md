# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 153

> [⬅️ Volver a la clase 153](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Aceptar una entrada solo si es alfanumérica. Es la validación más básica que existe y **la que habría
evitado la mayoría de las vulnerabilidades de la historia**. Y esta página tiene los dos casos que mejor
enseñan el problema: **Perl inventó en 1989 un mecanismo que marca los datos que vienen de fuera y se
niega a usarlos en operaciones peligrosas**; y **C++ sigue siendo responsable de alrededor del 70 % de
las vulnerabilidades graves de Chrome y de Windows**, todas de la misma familia.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es la **superficie de ataque**, y estos lenguajes la enseñan porque **cada uno tiene la
> suya y son muy distintas**. C++ y Fortran: **la memoria**. Tcl, M, Lisp y Perl: **la ejecución de código
> que llega como dato**. COBOL y RPG: **los datos y los permisos**, porque el ataque a un sistema bancario
> no es un desbordamiento, es una autorización mal puesta. Y Ada: **el caso honesto**, donde el lenguaje
> detectó el problema correctamente y el sistema se perdió igual.
>
> Y aparece la clasificación que ordena la clase: **lo que entra, lo que se ejecuta, lo que se recuerda y
> lo que se confía**.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: una palabra (entrada a validar) → stdout: `seguro=<true|false>` (true si es alfanumérica)
- **Regla:** `seguro si todos los caracteres son letras o dígitos`

| stdin | esperado |
|---|---|
| `abc` | `seguro=true` |
| `a;b` | `seguro=false` |
| `hola123` | `seguro=true` |

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
PROGRAM-ID. VALIDAR.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(60).
01  I       PIC 9(4) COMP.
01  LG      PIC 9(4) COMP.
01  C       PIC X.
01  SEGURO  PIC X(5) VALUE "true".

PROCEDURE DIVISION.
    ACCEPT LINEA
    MOVE FUNCTION LENGTH(FUNCTION TRIM(LINEA)) TO LG

    PERFORM VARYING I FROM 1 BY 1 UNTIL I > LG
        MOVE LINEA(I:1) TO C
        IF C IS NOT ALPHABETIC AND C IS NOT NUMERIC
            MOVE "false" TO SEGURO
        END-IF
    END-PERFORM

    DISPLAY "seguro=" FUNCTION TRIM(SEGURO)
    STOP RUN.
```

**Lo que esta clase enseña en COBOL.** COBOL tiene una propiedad de seguridad que merece decirse porque
va en contra de la intuición sobre los lenguajes antiguos: **es prácticamente inmune a los
desbordamientos de búfer**.

```cobol
       01  NOMBRE PIC X(20).
       ...
           MOVE ENTRADA-DE-60-CARACTERES TO NOMBRE    *> TRUNCA a 20. Punto.
```

**`MOVE` a un campo de longitud fija trunca, no desborda.** No hay aritmética de punteros, no hay
`strcpy`, no hay longitud implícita — **el tamaño está en la declaración y el compilador genera el
movimiento con ese tamaño**.

Es exactamente la clase de fallo que produce el 70 % de las vulnerabilidades de C++ en esta página, y en
COBOL **no existe**.

Y esa es una observación general que merece extraerse: **la seguridad de memoria no es una cuestión de
antigüedad del lenguaje, sino de si el lenguaje conoce el tamaño de las cosas**. COBOL, de 1959, lo
conoce; C, de 1972, no.

Y las superficies de ataque que COBOL sí tiene son otras, y hay que conocerlas:

**Primera, el SQL dinámico**, que es la única forma de inyección real en este mundo:

```cobol
      *> ✗ inyección: la entrada se pega a la consulta
           STRING "SELECT * FROM CLI WHERE ID='" WS-ENTRADA "'"
               INTO WS-SQL
           EXEC SQL PREPARE S FROM :WS-SQL END-EXEC

      *> ✓ variable de host: el valor va por separado, NO se analiza como SQL
           EXEC SQL SELECT NOMBRE INTO :WS-NOMBRE
                    FROM CLI WHERE ID = :WS-ENTRADA END-EXEC
```

**El SQL estático con variables de host es parametrizado por definición**, y por eso la inyección es rara
en COBOL: **la forma normal de escribirlo ya es la segura**.

Es la mejor demostración de la primera regla del cierre: **cuando el camino fácil es el correcto, el
problema desaparece**.

**Segunda, la truncación silenciosa como fallo lógico.** Que no haya desbordamiento no significa que no
haya error: **un importe que se trunca al mover a un campo más corto produce datos incorrectos sin
avisar** — y hay fraudes documentados que explotan exactamente eso.

**Y tercera, los permisos**, que en el mainframe son el verdadero perímetro: **RACF, ACF2 y Top Secret**
controlan quién puede ejecutar qué transacción y leer qué fichero, y **la vulnerabilidad típica de un
sistema bancario es una autorización mal concedida**, no un fallo de código.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program validar
   implicit none
   character(len=60) :: linea
   integer :: i, n, c
   logical :: seguro

   read(*, '(A)') linea
   n = len_trim(linea)
   seguro = n > 0

   do i = 1, n
      c = iachar(linea(i:i))
      if (.not. ((c >= iachar('a') .and. c <= iachar('z')) .or.  &
                 (c >= iachar('A') .and. c <= iachar('Z')) .or.  &
                 (c >= iachar('0') .and. c <= iachar('9')))) seguro = .false.
   end do

   if (seguro) then
      write(*, '(A)') 'seguro=true'
   else
      write(*, '(A)') 'seguro=false'
   end if
end program validar
```

**Lo que esta clase enseña en Fortran.** Fortran tiene un perfil de seguridad que merece explicarse
porque es distinto del de todos los demás: **su código casi nunca está expuesto a Internet, y por eso
nadie se ha preocupado**.

Un modelo climático no recibe peticiones HTTP. Y esa premisa, que fue cierta durante cincuenta años,
**ha dejado de serlo**:

- **Los datos de entrada vienen de fuera**: ficheros NetCDF, HDF5 y de observación, descargados de
  repositorios públicos.
- **El código se ejecuta en clústeres compartidos**, con otros usuarios.
- **Y las bibliotecas científicas se instalan desde repositorios** (clase 143).

Y las vulnerabilidades reales de este mundo son de la primera categoría:

```fortran
! ✗ leer una dimensión de un fichero y usarla sin comprobar
read(u) n
allocate(datos(n))          ! si n viene corrupto: reserva absurda o negativa
read(u) (datos(i), i = 1, n)
```

**Un fichero de datos manipulado puede provocar una reserva enorme, un índice fuera de rango o una
lectura de memoria ajena** — y en Fortran, **sin comprobación de límites activada, eso no da error**.

Y las defensas son las de siempre en este lenguaje:

```bash
gfortran -fcheck=all -fstack-protector-strong -D_FORTIFY_SOURCE=2 \
         -Wall -Wextra -std=f2018
```

**`-fcheck=bounds` es la línea de defensa principal**, y la discusión de siempre es que cuesta
rendimiento (clase 124). La postura sensata, y es la de esta clase: **activada siempre en el código que
lee datos externos**, aunque se desactive en los bucles internos del cálculo.

Y hay dos vulnerabilidades históricas de Fortran que merecen conocerse porque enseñan bien:

**La primera es de la clase 137**: sin `implicit none`, **una variable mal escrita crea otra nueva con
valor indefinido**, y una comprobación de seguridad puede quedar sin efecto sin que nadie lo note.

**Y la segunda es de la clase 109**: **un procedimiento externo sin interfaz explícita no comprueba los
argumentos**, así que pasar una cadena donde se espera un arreglo compila, enlaza y corrompe memoria.

Las dos se cierran con la misma disciplina de la clase 150 —**`implicit none` y todo en módulos**— que
resulta ser, además de buena ingeniería, la medida de seguridad más rentable del lenguaje.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO; use Ada.Text_IO;

procedure Validar is
   Linea  : String (1 .. 60);
   Ultimo : Natural;
   Seguro : Boolean;
begin
   Get_Line (Linea, Ultimo);
   Seguro := Ultimo > 0;

   for I in 1 .. Ultimo loop
      if Linea (I) not in 'a' .. 'z'
        and then Linea (I) not in 'A' .. 'Z'
        and then Linea (I) not in '0' .. '9'
      then
         Seguro := False;
      end if;
   end loop;

   if Seguro then
      Put_Line ("seguro=true");
   else
      Put_Line ("seguro=false");
   end if;
end Validar;
```

**Lo que esta clase enseña en Ada.** Ada es el lenguaje diseñado explícitamente para esto, y su respuesta
es la de toda la Parte 8: **hacer que la validación esté en el tipo, no en un `if`**.

```ada
subtype Identificador is String
   with Dynamic_Predicate =>
     (for all C of Identificador => C in 'a' .. 'z' | 'A' .. 'Z' | '0' .. '9');

subtype Puerto is Integer range 1 .. 65_535;
type Importe is delta 0.01 range 0.00 .. 1_000_000.00;
```

**Con eso, un valor fuera del dominio no puede existir**: cualquier conversión o asignación **lanza
`Constraint_Error`** (clase 124).

Es la primera regla del cierre de esta clase —**validar contra lo permitido**— expresada como
declaración, y comprobada en todos los puntos de entrada sin escribirla en ninguno.

Y con SPARK, **se demuestra que no hay desbordamiento, ni índice fuera de rango, ni valor sin
inicializar, para toda entrada posible** (clase 118) — que es la forma más fuerte de garantía que existe
en esta página.

Y esta clase merece contar el caso honesto que el "por qué" anunciaba, porque enseña más que cualquier
éxito: **el vuelo 501 del Ariane 5, en 1996**.

```text
1. Se reutilizó, sin revisar, el código del sistema de referencia inercial del Ariane 4.
2. El Ariane 5 tenía una trayectoria distinta, con velocidades horizontales MAYORES.
3. Una conversión de coma flotante de 64 bits a entero con signo de 16 bits desbordó.
4. Ada detectó el desbordamiento y lanzó la excepción, CORRECTAMENTE.
5. No había manejador: por diseño, el ordenador se apagaba ante un error no previsto.
6. El ordenador de reserva, con el MISMO software, había fallado igual 72 milisegundos antes.
7. El cohete se autodestruyó. 370 millones de dólares.
```

**Y el detalle decisivo**: la comprobación de esa conversión **se había desactivado deliberadamente por
rendimiento**, tras un análisis que demostraba —**para el Ariane 4**— que el valor no podía desbordar.

Las lecciones son cuatro y todas son de esta clase:

- **El lenguaje hizo su trabajo.** La detección fue correcta y a tiempo.
- **La reutilización sin revalidar el contexto es el fallo**: el análisis era válido para otro cohete.
- **La redundancia idéntica no es redundancia**: dos ordenadores con el mismo software fallan igual.
- **Y el código problemático ni siquiera era necesario** tras el despegue: seguía activo por herencia.

Es el mejor recordatorio de que **la seguridad no es una propiedad del lenguaje, sino del sistema
entero** — y de que las suposiciones que se documentan y no se revisan son las que acaban costando caro.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Validar;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  Linea: string;
  I: Integer;
  Seguro: Boolean;

begin
  ReadLn(Linea);
  Linea := Trim(Linea);
  Seguro := Length(Linea) > 0;

  for I := 1 to Length(Linea) do
    if not (Linea[I] in ['a'..'z', 'A'..'Z', '0'..'9']) then
      Seguro := False;

  if Seguro then
    WriteLn('seguro=true')
  else
    WriteLn('seguro=false');
end.
```

**Lo que esta clase enseña en Pascal.** `Linea[I] in ['a'..'z', 'A'..'Z', '0'..'9']` es la validación por
conjunto (clase 094), y es **exactamente la forma correcta**: una lista de lo permitido, en una
expresión legible.

Y Pascal aporta a esta clase el ejemplo más didáctico de una decisión de seguridad que se toma sin
pensarla, y ya apareció en la clase 137: **las comprobaciones desactivadas en la configuración de
publicación**.

```pascal
{$R+}   { comprobación de rango: índices y subrangos }
{$Q+}    { comprobación de desbordamiento aritmético }
{$S+}     { comprobación de desbordamiento de pila }
```

**Free Pascal y Delphi las traen ACTIVADAS en la configuración de depuración y DESACTIVADAS en la de
publicación.**

Y eso significa que **el binario que llega a los usuarios es el que no comprueba nada**:

```pascal
var V: array[1..10] of Integer;
    I: Integer;
begin
  I := LeerDelUsuario;
  V[I] := 42;        { con {$R-}: escribe DONDE SEA. Es C. }
```

**Con `{$R-}`, Pascal es tan inseguro como C en ese punto.** Con `{$R+}`, lanza `ERangeError`.

Y la decisión es exactamente la del Ariane 5 de esta página, tomada por omisión: **se desactivó la
comprobación por rendimiento, en el código que llega al usuario**.

La recomendación de esta clase es concreta: **mantener `{$R+}` y `{$Q+}` en producción**, salvo en los
bucles internos medidos donde se haya demostrado que importa. El coste típico es de un pequeño
porcentaje; el beneficio es que **un fallo se convierte en una excepción con línea en lugar de en una
corrupción silenciosa**.

Y las otras superficies del ecosistema Pascal:

| Riesgo | Defensa |
|---|---|
| **Inyección SQL** en `Query.SQL.Text := '...' + Edit1.Text` | `ParamByName`, siempre |
| **`PChar` y APIs de Windows** | comprobar longitudes; `StrLCopy`, no `StrCopy` |
| **Punteros y `GetMem`** | `heaptrc` (clase 138), y preferir clases o interfaces |
| **Componentes de terceros sin mantenimiento** | el mismo problema de dependencias (clase 143) |

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let ((palabra (string-trim '(#\Space #\Return) (read-line))))
  (format t "seguro=~A~%"
          (if (and (plusp (length palabra))
                   (every #'alphanumericp palabra))
              "true" "false")))
```

**Lo que esta clase enseña en Common Lisp.** El programa usa **`read-line`**, no `read`, y esa distinción
es la lección de seguridad más importante de Lisp:

**`read` no es un analizador de datos: es el analizador del LENGUAJE, y puede ejecutar código.**

```lisp
;; ✗ NUNCA con datos de fuera
(read stream)
```

Y el motivo es una característica del lector que merece conocerse: **la macro de lector `#.`**.

```lisp
;; Si la entrada contiene esto:
#.(uiop:run-program "rm -rf /")
;; ...el LECTOR lo ejecuta, en tiempo de lectura, antes de evaluar nada.
```

**`#.` significa "evalúa esto ahora, al leer"**, y existe para que un fichero fuente pueda calcular
constantes en tiempo de compilación. **Sobre datos externos, es ejecución remota de código.**

La defensa es una variable estándar:

```lisp
(let ((*read-eval* nil))
  (read stream))            ; ahora #. señala un error
```

**Pero eso no basta**, y conviene decirlo: incluso con `*read-eval*` desactivado, `read`
**crea símbolos** —agotando memoria con entradas grandes—, **puede activar macros de lector personalizadas**
y **puede reservar arreglos enormes** con `#(...)`.

La regla correcta es tajante: **para datos externos, un analizador de datos** —`jsonrpc`, `cl-json`,
`yason`— **nunca `read`**.

Es la misma lección que `pickle` en Python, `Marshal` en Ruby y la deserialización de Java: **un formato
que puede reconstruir objetos arbitrarios es un formato que puede ejecutar código**, y las
vulnerabilidades de deserialización llevan quince años en la lista de las más explotadas.

Y las otras superficies de Lisp:

| Riesgo | Nota |
|---|---|
| **`eval` sobre datos** | lo evidente, y menos frecuente que `read` |
| **`intern` sin control** | agota memoria: los símbolos no se recogen |
| **`format` con cadena de control externa** | **`~/foo/` invoca una función arbitraria** |
| **La imagen guardada** | puede contener credenciales tecleadas en el REPL (clase 144) |

**La tercera merece la advertencia** porque es poco conocida: **`(format t entrada-del-usuario)` con la
directiva `~/paquete:funcion/` llama a esa función**. La forma segura es siempre `(format t "~A"
entrada)`.

Es el mismo fallo que las cadenas de formato de C —`printf(entrada)`— con otro mecanismo, y la misma
regla: **la cadena de formato nunca es un dato**.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea
set p [string trim $linea]

if {$p ne "" && [string is alnum -strict $p]} {
    puts "seguro=true"
} else {
    puts "seguro=false"
}
```

**Lo que esta clase enseña en Tcl.** Tcl tiene la superficie de ataque más directa de esta página —**el
texto es código** (clase 081)— y también **uno de los primeros mecanismos de aislamiento reales de la
historia**.

Los riesgos, que la clase 146 ya adelantó:

```tcl
if "$x > 5" { ... }          ;# ✗ doble sustitución: inyección de expresión
eval $comandoDelUsuario        ;# ✗ evidente
exec sh -c $orden               ;# ✗ inyección de comandos
subst $plantilla                 ;# ✗ ejecuta lo que haya en [ ]
[$op $a $b]                       ;# ✗ el comando sale de un dato (clase 151)
```

**Y las defensas idiomáticas:**

```tcl
if {$x > 5} { ... }                        ;# llaves SIEMPRE
exec ls -- $fichero                          ;# separar opciones de datos
{*}$listaDeArgumentos                         ;# expansión segura, en vez de eval
subst -nocommands -novariables $plantilla      ;# subst limitado
```

Y aquí está la aportación notable de Tcl a esta clase: **Safe-Tcl**, de 1993.

```tcl
set interp [interp create -safe]
$interp eval $codigoNoConfiable      ;# en una jaula
```

**Un intérprete seguro es un intérprete completo al que se le han QUITADO los comandos peligrosos**: no
tiene `exec`, ni `open`, ni `socket`, ni `file`, ni `cd`, ni `load`.

Y lo que lo hace realmente interesante es el mecanismo de concesión: **los *alias***.

```tcl
$interp alias leerConfig ::miLeerConfigControlado
```

**El código del interior puede llamar a `leerConfig`, y lo que se ejecuta es una función del exterior que
valida y decide.** El interior no tiene acceso al sistema de ficheros: **tiene acceso a la puerta que se
le ha dado**.

**Eso es seguridad por capacidades**, y Safe-Tcl la implementó en 1993 —**dos años antes de que
apareciera el aislamiento de JavaScript en el navegador**— para el mismo problema: **ejecutar código
ajeno que llega por correo o por red**.

Y el principio merece extraerse porque es el correcto y sigue siendo minoritario: **en lugar de prohibir
lo peligroso, no dar acceso a nada y conceder capacidades concretas**.

Es lo que hoy hacen los permisos de WebAssembly con WASI, los contenedores con `seccomp`, y los sistemas
de capacidades como Capsicum. La lista negra siempre está incompleta; la lista de capacidades concedidas,
no.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $palabra = <STDIN>;
chomp $palabra;

print "seguro=", ($palabra =~ /^[A-Za-z0-9]+$/ ? 'true' : 'false'), "\n";
```

**Lo que esta clase enseña en Perl.** El anclaje `^...$` de la expresión regular no es decorativo: **sin
él, la comprobación pasaría con `abc; rm -rf /`** porque encontraría una coincidencia en cualquier parte.

Y hay una trampa poco conocida que merece decirse: **`$` en Perl también casa antes de un salto de línea
final**, así que `"abc\n"` pasaría un `/^\w+$/`. **La forma estricta es `\z`**:

```perl
$palabra =~ /^[A-Za-z0-9]+\z/     # \z: fin absoluto de la cadena
```

Es exactamente el fallo que ha permitido inyecciones en validadores que parecían correctos.

Y aquí está el mecanismo del gancho, y es una de las contribuciones más originales de Perl a la
seguridad: **el modo *taint***.

```bash
perl -T script.pl
```

**Con `-T`, Perl MARCA todos los datos que vienen de fuera** —argumentos, variables de entorno, entrada
estándar, ficheros, sockets— **y se niega a usarlos en operaciones peligrosas**:

```perl
my $fichero = <STDIN>;
open(my $fh, '<', $fichero);        # muere: "Insecure dependency in open"
system("ls $dir");                   # muere
unlink $ruta;                         # muere
```

**Y la marca se propaga**: si un dato marcado participa en un cálculo, **el resultado también queda
marcado**.

**La única forma de limpiarlo es una captura de expresión regular:**

```perl
if ($fichero =~ /^([A-Za-z0-9_.\-]+)\z/) {
    my $limpio = $1;               # ← esto SÍ está limpio
    open(my $fh, '<', $limpio) or die;
} else {
    die "nombre no permitido";
}
```

**El diseño obliga a escribir explícitamente qué se considera válido**, que es exactamente la primera
regla del cierre de esta clase — **impuesta por el intérprete**.

Es de 1989, y sigue siendo un mecanismo poco imitado: solo Ruby tuvo algo equivalente —`$SAFE`, hoy
retirado—, y los lenguajes modernos lo han sustituido por análisis estático de flujo de datos
—*taint analysis*—, que persigue el mismo objetivo desde fuera del lenguaje.

Y las otras defensas del ecosistema:

```perl
open(my $fh, '<', $f)              # 3 argumentos: el modo NO sale del dato
system('ls', '-l', $dir)            # lista: NO pasa por el intérprete de órdenes
$dbh->do('... WHERE id = ?', undef, $id)   # SQL parametrizado
use re 'strict';
```

**`open` con dos argumentos era la vulnerabilidad clásica de Perl**: `open(FH, $f)` con `$f` valiendo
`"| rm -rf /"` **ejecuta un comando**, porque el modo estaba en la propia cadena.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <algorithm>
#include <cctype>
#include <iostream>
#include <string>

int main() {
    std::string palabra;
    if (!(std::cin >> palabra)) return 1;

    const bool seguro = !palabra.empty() &&
        std::all_of(palabra.begin(), palabra.end(),
                    [](unsigned char c) { return std::isalnum(c) != 0; });

    std::cout << "seguro=" << (seguro ? "true" : "false") << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** Aquí está la otra mitad del gancho, y merece darse con datos porque
la magnitud sorprende:

```text
Microsoft (2019):  ~70 % de sus CVE de los últimos 12 años son de seguridad de memoria.
Chromium (2020):    ~70 % de los fallos graves son de seguridad de memoria.
Android (2022):     los fallos de memoria pasaron del 76 % al 35 % al introducir Rust.
```

**Todas de la misma familia**, y merece enumerarla porque son categorías con nombre:

| Fallo | Qué es |
|---|---|
| **Desbordamiento de búfer** | escribir más allá del final (clase 089) |
| **Uso después de liberar** | usar un puntero a memoria ya devuelta (clase 130) |
| **Doble liberación** | liberar dos veces: corrompe el montón |
| **Lectura sin inicializar** | leer memoria con basura, que puede ser de otro |
| **Desbordamiento de entero** | `n * sizeof(T)` da la vuelta y se reserva de menos |
| **Confusión de tipos** | interpretar un objeto como otro |
| **Carrera de datos** | dos hilos, sin sincronizar (clase 136) |

**La quinta es especialmente traicionera** y merece el ejemplo, porque parece código correcto:

```cpp
size_t n = leer_del_usuario();
char* p = (char*)malloc(n * sizeof(Registro));   // si n es enorme, DA LA VUELTA
for (size_t i = 0; i < n; ++i) p[i] = ...;        // y escribe fuera
```

**El desbordamiento del cálculo del tamaño produce una reserva pequeña y un bucle largo.** Es el origen
de vulnerabilidades muy graves, y por eso `calloc` comprueba la multiplicación y `std::vector` también.

Y las defensas de C++ moderno, que son sustanciales:

```cpp
std::vector<T> v;  v.at(i);          // .at() comprueba; operator[] no
std::span<T> s;                       // puntero + longitud, juntos
std::string_view sv;                   // sin terminador nulo, con longitud
std::unique_ptr / shared_ptr            // sin liberación manual (clase 130)
gsl::not_null<T*>
```

```bash
g++ -fsanitize=address,undefined -fstack-protector-strong \
    -D_FORTIFY_SOURCE=3 -Wformat-security -fPIE -Wl,-z,relro,-z,now
clang-tidy --checks='bugprone-*,cert-*,cppcoreguidelines-*'
```

**Y el consenso actual, que conviene conocer porque es una recomendación oficial de varias agencias de
seguridad**: para código nuevo en dominios críticos, **usar un lenguaje con seguridad de memoria**; para
el existente, **desinfectantes en las pruebas, análisis estático, y sustituir por partes**.

No es un juicio sobre el lenguaje: es la constatación de que **cincuenta años de disciplina no han
bastado**, y de que la propiedad que falta —que el compilador conozca el tamaño y la vida de las
cosas— es la que COBOL y Ada tienen en esta misma página.

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

dcl-pi VALIDAR;
  palabra char(60) const;
end-pi;

dcl-s texto  varchar(60);
dcl-s i      int(10);
dcl-s c      char(1);
dcl-s seguro ind;

texto = %trim(palabra);
seguro = %len(texto) > 0;

for i = 1 to %len(texto);
  c = %subst(texto : i : 1);
  if not ((c >= 'a' and c <= 'z') or
          (c >= 'A' and c <= 'Z') or
          (c >= '0' and c <= '9'));
    seguro = *off;
  endif;
endfor;

if seguro;
  dsply 'seguro=true';
else;
  dsply 'seguro=false';
endif;

*inlr = *on;
return;
```

**Lo que esta clase enseña en RPG.** IBM i tiene fama de plataforma segura, y merece explicar de dónde
viene y también dónde está el riesgo real, que no es donde la gente cree.

**De dónde viene la fama:**

**Primero, los objetos tienen tipo, impuesto por el hardware.** El sistema no permite ejecutar un
fichero de datos ni escribir en un objeto programa: **la arquitectura basada en objetos, con punteros con
etiqueta, hace imposible el desbordamiento de búfer clásico**.

Un puntero en IBM i **lleva un bit de etiqueta que el hardware protege**: si el programa modifica los
bytes del puntero, **la etiqueta se borra y el puntero deja de ser válido**.

**Eso elimina, por hardware, la técnica sobre la que se construyen la mayoría de los exploits de C++ de
esta página.**

**Segundo, la seguridad a nivel de objeto** está en el sistema operativo, no en la aplicación: cada
objeto tiene propietario y autoridades, y **el nivel de seguridad 40 o 50 impide saltarse las
interfaces**.

**Y ahora el riesgo real**, que merece decirse porque es donde ocurren los incidentes:

**Uno, la autoridad adoptada.**

```text
CRTBNDRPG ... USRPRF(*OWNER)
```

**Un programa con `USRPRF(*OWNER)` se ejecuta con los permisos de su propietario**, no del usuario. Es
imprescindible para muchas cosas, y **si ese programa permite ejecutar algo elegido por el usuario, le
está regalando los permisos del propietario**.

**Dos, `QSECOFR` y los perfiles con `*ALLOBJ`.** El equivalente de repartir la cuenta de administrador,
y es el hallazgo número uno de cualquier auditoría de esta plataforma.

**Tres, el SQL dinámico**, exactamente igual que en COBOL de esta página:

```rpgle
// ✗
sentencia = 'SELECT * FROM CLI WHERE ID = ''' + entrada + '''';
exec sql PREPARE s FROM :sentencia;

// ✓
exec sql SELECT nombre INTO :nombre FROM cli WHERE id = :entrada;
```

**Y cuatro, y es el más olvidado: los servicios de red heredados.** FTP, Telnet y las colas de datos
expuestas **saltan por completo los controles de la aplicación** y usan solo la autoridad a nivel de
objeto. **Si los permisos de las tablas son permisivos porque "la aplicación ya controla", un FTP los
lee todos.**

Es la lección general de esta página: **la seguridad de una plataforma sólida se pierde por la
configuración, no por el código** — y por eso las auditorías de IBM i miran autoridades, no
desbordamientos.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 validar: procedure options(main);

    declare palabra char(60) varying;
    declare i       fixed binary(31);
    declare c       char(1);
    declare seguro  bit(1) initial('1'b);

    get edit (palabra) (a(60));
    palabra = trim(palabra);

    if length(palabra) = 0 then seguro = '0'b;

    do i = 1 to length(palabra);
       c = substr(palabra, i, 1);
       if ^((c >= 'a' & c <= 'z') | (c >= 'A' & c <= 'Z') |
            (c >= '0' & c <= '9')) then seguro = '0'b;
    end;

    if seguro then
       put skip list ('seguro=true');
    else
       put skip list ('seguro=false');

 end validar;
```

**Lo que esta clase enseña en PL/I.** PL/I está en una posición intermedia interesante en esta clase:
**tiene las comprobaciones de Ada disponibles y las de C por defecto**.

```pli
 (subscriptrange, stringrange, stringsize, size):
 procesar: procedure;
    ...
 end procesar;
```

**Con ese prefijo, PL/I comprueba índices, subcadenas, truncamiento de cadenas y desbordamiento
aritmético** — es decir, **casi toda la lista de la tabla de C++ en esta página**.

**Y sin él, no comprueba nada**, porque **las comprobaciones están desactivadas por defecto** en la
mayoría de las configuraciones de compilación, por rendimiento.

Es exactamente la situación de Pascal con `{$R-}` en esta página, y la misma recomendación: **activarlas
en todo lo que procese datos externos**.

Y PL/I tiene la construcción que más peligro concentra y que merece explicarse: **`BASED` con punteros**.

```pli
 declare p pointer;
 declare estructura based(p);          /* la forma se decide al desreferenciar */
 declare buffer char(32767) based(p);   /* ¡el MISMO puntero, otra forma! */

 p = addr(datos);
 /* leer 32767 caracteres desde donde apunte p, sea lo que sea */
```

**Eso es aritmética de punteros con reinterpretación de tipos**, y es tan peligroso como en C: **PL/I
puede escribir donde no debe**.

Y la técnica que hace difícil auditar estos programas es la misma que la clase 150 señalaba: **con
`BASED` y `DEFINED`, saber qué memoria toca cada sentencia requiere seguir el flujo de los punteros**.

Y sobre entradas, la superficie característica de PL/I es la **condición `CONVERSION`** (clase 137):

```pli
 declare importe fixed decimal(11,2);
 declare entrada char(20) varying;

 importe = entrada;         /* si entrada no es numérica: CONVERSION */
```

**Sin un manejador `on conversion`, el programa aborta.** Y con uno mal escrito —que use `onsource` para
"arreglar" el dato— **se puede acabar aceptando entradas que deberían rechazarse**.

Es un buen ejemplo de la primera regla del cierre: **la conversión permisiva no es validación**. Validar
es comprobar contra lo permitido **antes** de convertir, no reparar después de fallar.

Y la superficie que de verdad domina en este mundo es la de COBOL en esta página: **los permisos de
RACF, quién puede ejecutar qué transacción y qué fichero puede leer** — porque en un sistema donde el
código lleva treinta años estable, **lo que cambia y se configura mal son las autorizaciones**.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
VALIDAR ; Validar entrada -- clase 153
 read palabra
 new i, c, seguro
 set seguro = $select($length(palabra) > 0 : 1, 1 : 0)
 for i = 1:1:$length(palabra) do
 . set c = $extract(palabra, i)
 . if "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789" '[ c set seguro = 0
 write "seguro=", $select(seguro : "true", 1 : "false"), !
 quit
```

**Lo que esta clase enseña en M.** El programa usa el operador **`[`** —"contiene"— con una cadena de
caracteres permitidos: es la lista blanca del cierre de esta clase, escrita como una constante.

Y M tiene la superficie de ataque más directa de esta página, por lo que la clase 123 explicó: **la
indirección y `xecute` ejecutan texto**.

```mumps
 xecute entrada          ; ✗ ejecución de código arbitrario, sin más
 do @rutina               ; ✗ si "rutina" viene de fuera
 set @nombre = valor       ; ✗ escribir en CUALQUIER variable o global
```

**`set @nombre = valor` merece destacarse**, porque no es evidente: si `nombre` vale
`"^SEGURIDAD(""ADMIN"")"`, **la asignación escribe en la global de seguridad**.

Es la misma clase de fallo que la contaminación de prototipos en JavaScript y la asignación masiva en
los marcos web: **dejar que la entrada decida el destino de la escritura, no solo su valor**.

Y las defensas son las de siempre y hay que aplicarlas explícitamente:

```mumps
 ; ✓ lista blanca de rutinas permitidas
 if '$data(^PERMITIDAS(rutina)) quit "no permitida"
 do @(rutina_"^PAQUETE")

 ; ✓ validar antes de usar como subíndice
 if entrada'?1.30AN quit "entrada no valida"     ; PATRÓN: 1 a 30 alfanuméricos
```

**Y `?1.30AN` merece explicarse**, porque es una característica de M que casi ningún lenguaje tiene: **el
operador de coincidencia de patrones está en el lenguaje**.

```mumps
 if x?1.8AN            ; de 1 a 8 caracteres alfanuméricos
 if x?3N1"-"2N          ; tres dígitos, un guion, dos dígitos
 if x?.E1"@"1.E          ; algo, arroba, algo
```

**`?` con un patrón compacto es la validación idiomática de M**, es de 1977, y es exactamente la primera
regla del cierre de esta clase disponible como operador.

Y esta clase debe cerrar con lo que de verdad importa en el dominio de M, porque es distinto del resto de
la página: **la privacidad**.

M se usa en sanidad, así que **el riesgo principal no es la ejecución de código: es el acceso indebido a
historias clínicas**.

Y VistA construyó para eso mecanismos formales que merecen conocerse:

| Mecanismo | Qué hace |
|---|---|
| **Claves de seguridad** (*security keys*) | qué opciones puede usar cada persona |
| **Auditoría de FileMan** | **quién consultó qué ficha y cuándo** (clase 142) |
| **Pacientes sensibles** | aviso y registro obligatorio al acceder |
| **Ruptura de cristal** | acceso de emergencia, con justificación y revisión posterior |

**"Romper el cristal" es un patrón que merece extraerse**: en una urgencia, **el sistema permite el
acceso pero lo marca, exige una justificación y lo notifica para revisión**.

Es la respuesta correcta a un conflicto real entre seguridad y vida humana, y es aplicable a cualquier
sistema donde negar el acceso pueda ser peor que concederlo.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| palabra seguro |

palabra := stdin nextLine trimBoth.

seguro := palabra notEmpty and: [
    palabra allSatisfy: [ :c | c isAlphaNumeric ] ].

Transcript show: 'seguro=', (seguro ifTrue: [ 'true' ] ifFalse: [ 'false' ]); cr.
```

**Lo que esta clase enseña en Smalltalk.** Smalltalk parte con **seguridad de memoria completa** —no hay
punteros, no hay aritmética de direcciones, los índices se comprueban siempre (clase 129)— así que toda
la tabla de C++ de esta página **no aplica**.

Y su superficie de ataque es la de un lenguaje muy dinámico:

```smalltalk
objeto perform: entradaDelUsuario asSymbol.        "✗ llamar a CUALQUIER método"
Compiler evaluate: textoDelUsuario.                 "✗ compilar y ejecutar"
Smalltalk at: nombre asSymbol.                       "✗ acceder a cualquier global"
(Smalltalk at: #Clase) new.
```

**`perform:` con un selector que viene de fuera permite invocar cualquier método del objeto**, incluidos
los privados por convención — porque en Smalltalk **la privacidad es una convención, no una regla**
(clase 087).

Y hay una operación que merece mención especial por lo poderosa que es: **`become:`**.

```smalltalk
objetoA become: objetoB.
"TODAS las referencias a A pasan a apuntar a B, y viceversa, en TODO el sistema"
```

**Eso intercambia dos objetos en todas las referencias existentes.** Es una primitiva extraordinaria
para migrar estructuras en caliente, y **es una capacidad total sobre el sistema**.

Y Smalltalk aporta a esta clase una línea de investigación de primer orden que merece contarse, porque
es el origen de un modelo de seguridad importante: **la seguridad por capacidades**.

```text
Smalltalk → Self → E (Mark Miller, 1997) → Caja / SES → los "realms" de JavaScript
```

**La idea central es la misma que Safe-Tcl en esta página, formalizada**: **un objeto solo puede hacer
aquello para lo que tiene una referencia**. No hay autoridad ambiental —ni variables globales, ni acceso
al sistema de ficheros por nombre—: **si no te han pasado el objeto "fichero", no puedes tocar
ficheros**.

Y eso encaja de forma natural con la orientación a objetos: **una referencia a un objeto ES un permiso
para usarlo**.

**Mark Miller, que desarrolló E, es hoy uno de los autores de las propuestas de aislamiento de
JavaScript** —los *realms* y los *hardened objects*— y de SES, que es lo que hace posible ejecutar
complementos no confiables en el mismo proceso.

Y el ecosistema Smalltalk lo tiene disponible:

```smalltalk
"Pharo: espejos y entornos restringidos"
Environment new importSelf; import: Kernel; yourself.
```

Y merece cerrar con la observación que conecta con todo lo anterior: **el modelo de capacidades es la
respuesta correcta al problema de esta clase**, y aparece dos veces en esta página —en Tcl en 1993 y en
Smalltalk desde los ochenta— porque **los lenguajes que ejecutan código ajeno tuvieron que resolverlo
antes que nadie**.

---

## Y de vuelta a la clase

Lo transferible: **toda entrada es hostil hasta que se demuestre lo contrario, y "demostrar" significa
validar contra una lista de lo permitido, no filtrar lo prohibido** — porque la lista de lo prohibido
siempre está incompleta. De ahí las cuatro reglas que atraviesan la página: **nunca construir código o
consultas concatenando datos**; **nunca confiar en la longitud de nada**; **actualizar las dependencias,
porque la mayoría de las vulnerabilidades explotadas hoy son de bibliotecas con parche disponible**; y
la que más veces se olvida, **no registrar datos sensibles** (clase 142), porque los registros se copian
a sitios donde nadie los protege.

⏮️ [Volver a la clase 153](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
