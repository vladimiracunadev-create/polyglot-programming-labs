# -*- coding: utf-8 -*-
"""Parte 9, lote E — clases 153 y 154. Ver `vivos_parte9.py` y `gen_vivos.py`."""

SPECS: dict[str, dict] = {}

# ---------------------------------------------------------------------------
# 153 — Seguridad: entradas, memoria y dependencias
# ---------------------------------------------------------------------------
SPECS["153"] = dict(
    gancho="""
Aceptar una entrada solo si es alfanumérica. Es la validación más básica que existe y **la que habría
evitado la mayoría de las vulnerabilidades de la historia**. Y esta página tiene los dos casos que mejor
enseñan el problema: **Perl inventó en 1989 un mecanismo que marca los datos que vienen de fuera y se
niega a usarlos en operaciones peligrosas**; y **C++ sigue siendo responsable de alrededor del 70 % de
las vulnerabilidades graves de Chrome y de Windows**, todas de la misma familia.
""",
    porque="""
Aquí el concepto es la **superficie de ataque**, y estos lenguajes la enseñan porque **cada uno tiene la
suya y son muy distintas**. C++ y Fortran: **la memoria**. Tcl, M, Lisp y Perl: **la ejecución de código
que llega como dato**. COBOL y RPG: **los datos y los permisos**, porque el ataque a un sistema bancario
no es un desbordamiento, es una autorización mal puesta. Y Ada: **el caso honesto**, donde el lenguaje
detectó el problema correctamente y el sistema se perdió igual.

Y aparece la clasificación que ordena la clase: **lo que entra, lo que se ejecuta, lo que se recuerda y
lo que se confía**.
""",
    cierre="""
Lo transferible: **toda entrada es hostil hasta que se demuestre lo contrario, y "demostrar" significa
validar contra una lista de lo permitido, no filtrar lo prohibido** — porque la lista de lo prohibido
siempre está incompleta. De ahí las cuatro reglas que atraviesan la página: **nunca construir código o
consultas concatenando datos**; **nunca confiar en la longitud de nada**; **actualizar las dependencias,
porque la mayoría de las vulnerabilidades explotadas hoy son de bibliotecas con parche disponible**; y
la que más veces se olvida, **no registrar datos sensibles** (clase 142), porque los registros se copian
a sitios donde nadie los protege.
""",
    langs={
        "cobol": ("""
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
""", """
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
"""),
        "fortran": ("""
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
""", """
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
gfortran -fcheck=all -fstack-protector-strong -D_FORTIFY_SOURCE=2 \\
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
"""),
        "ada": ("""
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
""", """
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
"""),
        "pascal": ("""
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
""", """
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
"""),
        "lisp": ("""
(let ((palabra (string-trim '(#\\Space #\\Return) (read-line))))
  (format t "seguro=~A~%"
          (if (and (plusp (length palabra))
                   (every #'alphanumericp palabra))
              "true" "false")))
""", """
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
"""),
        "tcl": ("""
gets stdin linea
set p [string trim $linea]

if {$p ne "" && [string is alnum -strict $p]} {
    puts "seguro=true"
} else {
    puts "seguro=false"
}
""", """
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
"""),
        "perl": ("""
use strict;
use warnings;

my $palabra = <STDIN>;
chomp $palabra;

print "seguro=", ($palabra =~ /^[A-Za-z0-9]+$/ ? 'true' : 'false'), "\\n";
""", """
**Lo que esta clase enseña en Perl.** El anclaje `^...$` de la expresión regular no es decorativo: **sin
él, la comprobación pasaría con `abc; rm -rf /`** porque encontraría una coincidencia en cualquier parte.

Y hay una trampa poco conocida que merece decirse: **`$` en Perl también casa antes de un salto de línea
final**, así que `"abc\\n"` pasaría un `/^\\w+$/`. **La forma estricta es `\\z`**:

```perl
$palabra =~ /^[A-Za-z0-9]+\\z/     # \\z: fin absoluto de la cadena
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
if ($fichero =~ /^([A-Za-z0-9_.\\-]+)\\z/) {
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
"""),
        "cpp": ("""
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

    std::cout << "seguro=" << (seguro ? "true" : "false") << '\\n';
    return 0;
}
""", """
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
g++ -fsanitize=address,undefined -fstack-protector-strong \\
    -D_FORTIFY_SOURCE=3 -Wformat-security -fPIE -Wl,-z,relro,-z,now
clang-tidy --checks='bugprone-*,cert-*,cppcoreguidelines-*'
```

**Y el consenso actual, que conviene conocer porque es una recomendación oficial de varias agencias de
seguridad**: para código nuevo en dominios críticos, **usar un lenguaje con seguridad de memoria**; para
el existente, **desinfectantes en las pruebas, análisis estático, y sustituir por partes**.

No es un juicio sobre el lenguaje: es la constatación de que **cincuenta años de disciplina no han
bastado**, y de que la propiedad que falta —que el compilador conozca el tamaño y la vida de las
cosas— es la que COBOL y Ada tienen en esta misma página.
"""),
        "rpg": ("""
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
""", """
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
"""),
        "pli": ("""
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
""", """
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
"""),
        "mumps": ("""
VALIDAR ; Validar entrada -- clase 153
 read palabra
 new i, c, seguro
 set seguro = $select($length(palabra) > 0 : 1, 1 : 0)
 for i = 1:1:$length(palabra) do
 . set c = $extract(palabra, i)
 . if "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789" '[ c set seguro = 0
 write "seguro=", $select(seguro : "true", 1 : "false"), !
 quit
""", """
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
"""),
        "smalltalk": ("""
| palabra seguro |

palabra := stdin nextLine trimBoth.

seguro := palabra notEmpty and: [
    palabra allSatisfy: [ :c | c isAlphaNumeric ] ].

Transcript show: 'seguro=', (seguro ifTrue: [ 'true' ] ifFalse: [ 'false' ]); cr.
""", """
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
"""),
    },
)

# ---------------------------------------------------------------------------
# 154 — Mantenibilidad, documentación y deuda técnica
# ---------------------------------------------------------------------------
SPECS["154"] = dict(
    gancho="""
Contar módulos y llamarlo complejidad. Es una métrica tosca a propósito, porque esta clase trata de algo
que se mide mal y se paga siempre. Y estos lenguajes son el mejor sitio para hablar de ello, por una
razón sencilla: **son los que llevan más tiempo en mantenimiento**. Hay COBOL de 1968 en producción, y
**el término "deuda técnica" lo acuñó Ward Cunningham en 1992, en una conferencia sobre Smalltalk**,
describiendo exactamente lo que estos sistemas viven.
""",
    porque="""
Aquí el concepto es el **coste de vivir con el código**, y estos lenguajes lo enseñan porque **han vivido
con él más que nadie**. Y aportan las tres respuestas que existen a la pregunta de dónde va la
documentación: **fuera del código** —los manuales del mainframe—, **dentro del código como comentario
estructurado** —POD en Perl, Doxygen en C++, `;;` en M—, y **como parte del propio programa** —las
cadenas de documentación de Lisp, el comentario de clase de Smalltalk, la especificación de Ada—.

Y aparece la observación que más incomoda: **el código se lee muchas más veces de las que se escribe**,
y casi todas las decisiones de estilo y estructura se toman pensando en escribirlo.
""",
    cierre="""
Lo transferible: **la deuda técnica es una metáfora financiera y hay que tomarla en serio como tal** —se
contrae a propósito para entregar antes, y **paga intereses en forma de cada cambio futuro más lento**—.
Lo que la convierte en un problema no es contraerla: es **no llevar la cuenta y no devolverla nunca**. De
ahí las dos prácticas que funcionan: **escribir por qué, no qué** —el código ya dice qué hace; lo que se
pierde es la razón—, y **dejar constancia de la deuda donde se contrae**, con una nota que diga qué se
sacrificó y a cambio de qué. Un sistema de veinte años es legible o ilegible según se haya hecho eso,
no según el lenguaje.
""",
    langs={
        "cobol": ("""
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
""", """
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
"""),
        "fortran": ("""
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
""", """
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
"""),
        "ada": ("""
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
""", """
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
"""),
        "pascal": ("""
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
""", """
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
"""),
        "lisp": ("""
(defun contar-palabras (linea)
  "Devuelve cuántas palabras separadas por espacios contiene LINEA."
  (let ((cnt 0) (en-palabra nil))
    (loop for c across linea
          do (if (char= c #\\Space)
                 (setf en-palabra nil)
                 (unless en-palabra (setf en-palabra t) (incf cnt))))
    cnt))

(format t "complejidad=~D~%" (contar-palabras (read-line)))
""", """
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
"""),
        "tcl": ("""
gets stdin linea

set n [llength [split [string trim $linea]]]

puts "complejidad=$n"
""", """
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
"""),
        "perl": ("""
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

print "complejidad=", scalar(@modulos), "\\n";
""", """
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
"""),
        "cpp": ("""
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
    std::cout << "complejidad=" << contar(std::cin) << '\\n';
    return 0;
}
""", """
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
"""),
        "rpg": ("""
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
""", """
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
"""),
        "pli": ("""
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
""", """
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
"""),
        "mumps": ("""
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
""", """
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
"""),
        "smalltalk": ("""
"Cuenta los modulos (palabras) de una linea de entrada.
 Ver la clase 154 del curso poliglota."

| linea |

linea := stdin nextLine trimBoth.

Transcript show: 'complejidad=', (linea substrings: ' ') size printString; cr.
""", """
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
"""),
    },
)
