# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 095

> [⬅️ Volver a la clase 095](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Contar cuántas veces aparece un valor. Es la estructura de datos que define la programación moderna
—diccionario, mapa, tabla *hash*, array asociativo— y el reparto entre estos doce lenguajes es
brutal: **cinco la tienen integrada en la sintaxis, tres la tienen en biblioteca y cuatro no la tienen
en absoluto**. Y el que mejor la resuelve es el más viejo de todos: **en M, el diccionario es la única
estructura que existe, y además está en disco**.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es la **asociación clave-valor**, y estos lenguajes lo enseñan porque muestran cuándo
> dejó de ser exótica. **Lisp** tuvo listas de asociación desde 1958 y tablas *hash* en el estándar de
> 1984; **M** las tiene desde 1966 como estructura única; **Perl** (1987) y **Tcl** (1988) las pusieron
> en la sintaxis del lenguaje y con eso definieron el estilo de los lenguajes de guion.
>
> Enfrente, **COBOL, Fortran, RPG y PL/I no tienen diccionarios**, y su respuesta —tabla ordenada con
> búsqueda binaria, o delegar en la base de datos— sigue siendo perfectamente razonable en su contexto.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: una línea con enteros separados por espacio → stdout: `cuenta=<veces que aparece el primer elemento>`
- **Regla:** `cuenta = frecuencia[lista[0]]`

| stdin | esperado |
|---|---|
| `3 1 3 3` | `cuenta=3` |
| `5 5` | `cuenta=2` |
| `7 1 2` | `cuenta=1` |

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
PROGRAM-ID. MAPA.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(200).
01  TOKEN   PIC X(20).
01  TLEN    PIC 9(2) COMP VALUE 0.
01  I       PIC 9(4) COMP.
01  J       PIC 9(4) COMP.
01  N       PIC 9(4) COMP VALUE 0.
01  VALOR   PIC S9(9) COMP-3.
01  PRIMERO PIC S9(9) COMP-3.
01  HAY-PRIMERO PIC X VALUE "N".
01  POSICION    PIC 9(4) COMP.
01  TABLA.
    05  ENTRADA OCCURS 100 TIMES.
        10  CLAVE  PIC S9(9) COMP-3.
        10  CUENTA PIC 9(4)  COMP.
01  ED-C    PIC Z(3)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    MOVE SPACES TO TOKEN
    PERFORM VARYING I FROM 1 BY 1 UNTIL I > 200
        IF LINEA(I:1) = SPACE
            PERFORM CERRAR-TOKEN
        ELSE
            ADD 1 TO TLEN
            MOVE LINEA(I:1) TO TOKEN(TLEN:1)
        END-IF
    END-PERFORM
    PERFORM CERRAR-TOKEN

    MOVE 0 TO POSICION
    PERFORM VARYING J FROM 1 BY 1 UNTIL J > N
        IF CLAVE(J) = PRIMERO
            MOVE J TO POSICION
        END-IF
    END-PERFORM

    MOVE CUENTA(POSICION) TO ED-C
    DISPLAY "cuenta=" FUNCTION TRIM(ED-C)
    STOP RUN.

CERRAR-TOKEN.
    IF TLEN > 0
        COMPUTE VALOR = FUNCTION NUMVAL(TOKEN)
        IF HAY-PRIMERO = "N"
            MOVE VALOR TO PRIMERO
            MOVE "S" TO HAY-PRIMERO
        END-IF
        MOVE 0 TO POSICION
        PERFORM VARYING J FROM 1 BY 1 UNTIL J > N
            IF CLAVE(J) = VALOR
                MOVE J TO POSICION
            END-IF
        END-PERFORM
        IF POSICION = 0
            ADD 1 TO N
            MOVE VALOR TO CLAVE(N)
            MOVE 1 TO CUENTA(N)
        ELSE
            ADD 1 TO CUENTA(POSICION)
        END-IF
        MOVE SPACES TO TOKEN
        MOVE 0 TO TLEN
    END-IF.
```

**Lo que esta clase enseña en COBOL.** **COBOL no tiene diccionarios**, y lo que se escribe en su
lugar es exactamente este programa: **una tabla de pares clave-valor y una búsqueda**.

Es un patrón tan común que tiene nombre en el mundo COBOL —*tabla de trabajo* o *tabla interna*— y
sostiene una parte enorme del código de negocio: cargar los códigos de país, las tarifas o los tipos
de IVA en una tabla al arrancar y consultarlos millones de veces sin volver a la base de datos.

Con `SEARCH ALL` y `ASCENDING KEY` (clase 094) la consulta es **binaria**, así que una tabla de diez
mil entradas se consulta en catorce comparaciones. No es O(1), y para el volumen de una tabla de
referencia es indistinguible.

Cuando la tabla es grande o compartida, la respuesta de la plataforma es otra, y merece conocerse:

**VSAM KSDS** —un fichero indexado por clave, con árbol B en disco— es literalmente un diccionario
persistente, y `READ ... KEY IS` es su operación de consulta:

```cobol
MOVE "ES" TO PAIS-CLAVE
READ TABLA-PAISES KEY IS PAIS-CLAVE
    INVALID KEY DISPLAY "no existe"
END-READ
```

VSAM es de 1973 y sigue moviendo datos hoy. Es la misma idea que los *globals* de M: **una estructura
de datos del programa que vive en disco**, sin capa de persistencia.

Y en CICS existe además la *tabla temporal de almacenamiento* (TSQ), que es un diccionario compartido
entre transacciones — el equivalente de un Redis, integrado en el monitor transaccional desde los años
setenta.

La conclusión se repite: **COBOL no tiene la estructura, la plataforma sí**.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program mapa
   implicit none
   integer :: v(100), n, ios, i, j, primero, cuenta

   character(len=400) :: linea

   read(*, '(A)') linea

   n = 0
   do i = 1, 100
      read(linea, *, iostat=ios) v(1:i)
      if (ios /= 0) exit
      n = i
   end do

   primero = v(1)
   cuenta = count(v(1:n) == primero)     ! sin bucle: máscara lógica

   write(*, '(A,I0)') 'cuenta=', cuenta
end program mapa
```

**Lo que esta clase enseña en Fortran.** **Fortran no tiene tablas asociativas** en el estándar, y
esta clase concreta se resuelve sin ninguna: `count(v(1:n) == primero)` cuenta las apariciones con la
máscara lógica de la clase 094.

Que la operación completa quepa en una expresión es la fuerza del lenguaje; que no haya diccionario
es su límite, y es un límite real. Cuando un código Fortran necesita asociar nombres a valores —leer
un fichero de configuración, indexar especies químicas, mapear identificadores de malla— hay tres
salidas históricas:

1. **Arreglos paralelos ordenados** con búsqueda binaria escrita a mano.
2. **Un arreglo indexado por un entero denso**, cuando las claves se pueden numerar. Es el idioma
   dominante en códigos científicos: convertir la clave en un índice y usar un arreglo.
3. **Llamar a C**, con `iso_c_binding`, para usar una tabla *hash* de verdad.

La tercera dejó de ser necesaria con **`stdlib`** (2020), que incluye `stdlib_hashmaps` con dos
implementaciones —encadenamiento abierto y direccionamiento abierto— y varias funciones *hash*
seleccionables.

```fortran
use stdlib_hashmaps, only: chaining_hashmap_type
type(chaining_hashmap_type) :: mapa
call mapa%init(fnv_1_hasher)
call mapa%map_entry(clave, valor)
```

Merece subrayarse lo que significa: **el lenguaje del cálculo numérico tuvo su primera tabla hash
estándar en 2020**, sesenta y tres años después de nacer. No por incapacidad, sino porque durante
sesenta años **no la necesitó**: sus datos son mallas y matrices, indexadas por posición.

Es un recordatorio útil de que "le falta X" solo significa algo si X hace falta para el problema.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;
with Ada.Containers.Ordered_Maps;

procedure Mapa is
   package Mapas is new Ada.Containers.Ordered_Maps
     (Key_Type => Integer, Element_Type => Integer);
   use Mapas;

   M          : Map;
   Linea      : String (1 .. 400);
   Ultimo     : Natural;
   Pos        : Integer := 1;
   Valor      : Integer;
   Fin        : Positive;
   Primero    : Integer := 0;
   Es_Primero : Boolean := True;
   C          : Cursor;
begin
   Get_Line (Linea, Ultimo);

   loop
      while Pos <= Ultimo and then Linea (Pos) = ' ' loop
         Pos := Pos + 1;
      end loop;
      exit when Pos > Ultimo;

      Get (Linea (Pos .. Ultimo), Valor, Fin);
      if Es_Primero then
         Primero := Valor;
         Es_Primero := False;
      end if;

      C := M.Find (Valor);
      if C = No_Element then
         M.Insert (Valor, 1);
      else
         M.Replace_Element (C, Element (C) + 1);
      end if;

      Pos := Fin + 1;
   end loop;

   Put ("cuenta=");
   Put (M.Element (Primero), Width => 1);
   New_Line;
end Mapa;
```

**Lo que esta clase enseña en Ada.** Como con los conjuntos, Ada obliga a elegir entre **el árbol y la
tabla**, y lo dice en el nombre del paquete:

```ada
Ada.Containers.Ordered_Maps      --  árbol equilibrado: O(log n), ORDENADO
Ada.Containers.Hashed_Maps        --  tabla hash: O(1), sin orden
Ada.Containers.Indefinite_*       --  cuando la clave o el valor no tienen tamaño fijo
```

Los `Indefinite_` son una peculiaridad de Ada que hay que entender: un `Ordered_Maps` normal exige que
el tipo tenga **tamaño conocido**, porque guarda los elementos por valor. Para un `String`, cuya
longitud es parte del tipo, hace falta `Indefinite_Ordered_Maps`, que reserva cada elemento por
separado.

Es más trabajo mental que en un lenguaje donde todo es un puntero, y es información real: **la
versión definida no hace ninguna reserva por elemento**, lo que importa en sistemas donde eso está
prohibido.

Y el **cursor** merece atención, porque es el iterador de Ada con una garantía extra:

```ada
C := M.Find (Valor);
if C /= No_Element then
   M.Replace_Element (C, Element (C) + 1);      --  sin volver a buscar
end if;
```

Buscar una vez y reutilizar la posición evita la doble búsqueda que hace el idioma ingenuo
—`if M.Contains (K) then M.Update (K, ...)`—. Es lo mismo que el `find`/`emplace_hint` de C++ y la
`entry` API de Rust.

Ada añade además **comprobación de manipulación (*tampering*)**: modificar un contenedor mientras se
recorre **lanza una excepción** en lugar de producir comportamiento indefinido. En C++, invalidar un
iterador así es un fallo silencioso; en Ada, es un error detectado.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Mapa;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  Claves, Cuentas: array of Integer;
  Linea, Tok: string;
  I, J, Valor, Primero, Posicion: Integer;
  C: Char;
  HayPrimero: Boolean;

begin
  ReadLn(Linea);

  SetLength(Claves, 0);
  SetLength(Cuentas, 0);
  HayPrimero := False;
  Primero := 0;
  Tok := '';

  for I := 1 to Length(Linea) + 1 do
  begin
    if I <= Length(Linea) then C := Linea[I] else C := ' ';
    if C = ' ' then
    begin
      if Tok <> '' then
      begin
        Valor := StrToInt(Tok);
        if not HayPrimero then
        begin
          Primero := Valor;
          HayPrimero := True;
        end;

        Posicion := -1;
        for J := 0 to High(Claves) do
          if Claves[J] = Valor then Posicion := J;

        if Posicion = -1 then
        begin
          SetLength(Claves, Length(Claves) + 1);
          SetLength(Cuentas, Length(Cuentas) + 1);
          Claves[High(Claves)] := Valor;
          Cuentas[High(Cuentas)] := 1;
        end
        else
          Inc(Cuentas[Posicion]);

        Tok := '';
      end;
    end
    else
      Tok := Tok + C;
  end;

  Posicion := -1;
  for J := 0 to High(Claves) do
    if Claves[J] = Primero then Posicion := J;

  WriteLn('cuenta=', IntToStr(Cuentas[Posicion]));
end.
```

**Lo que esta clase enseña en Pascal.** **El Pascal original no tiene diccionarios**, y este programa
escribe el que hace falta: dos arreglos paralelos y una búsqueda lineal. Es lo que se enseñaba en el
libro de Wirth, y es lo que hay en el código Pascal antiguo.

Free Pascal y Delphi modernos lo resolvieron con **genéricos**, y hoy lo idiomático es:

```pascal
uses Generics.Collections;

var
  Cuentas: TDictionary<Integer, Integer>;
begin
  Cuentas := TDictionary<Integer, Integer>.Create;
  try
    if not Cuentas.ContainsKey(V) then
      Cuentas.Add(V, 1)
    else
      Cuentas[V] := Cuentas[V] + 1;
  finally
    Cuentas.Free;
  end;
end;
```

`Generics.Collections` trae `TDictionary`, `TList<T>`, `TQueue<T>`, `TStack<T>` y `TObjectDictionary`,
que además **destruye los objetos que contiene** al liberarse — una respuesta a la gestión manual de
memoria que Pascal nunca automatizó del todo.

Y hay una estructura anterior, de los tiempos de Delphi 1, que sigue usándose por todas partes:

```pascal
uses Classes;

var L: TStringList;
begin
  L := TStringList.Create;
  L.Values['nombre'] := 'Ada';        { pares clave=valor }
  L.Sorted := True;                    { búsqueda BINARIA a partir de aquí }
  L.AddObject('clave', UnObjeto);      { una cadena y un objeto asociado }
end;
```

`TStringList` es una lista de cadenas con un puntero opcional por elemento, con carga y guardado a
fichero, ordenación y búsqueda. Es el "todo en uno" del ecosistema Delphi, y se usa como diccionario,
como lista, como parser de configuración y como almacén de objetos. Es poco elegante y es
extraordinariamente práctico — la clase de herramienta que solo aparece en lenguajes con treinta años
de código detrás.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let ((v '())
      (tabla (make-hash-table :test #'eql)))
  (loop for x = (read *standard-input* nil nil)
        while x
        do (push x v)
           (incf (gethash x tabla 0)))          ; 0 es el valor POR DEFECTO
  (format t "cuenta=~D~%" (gethash (car (last v)) tabla)))
```

**Lo que esta clase enseña en Common Lisp.** Lisp tiene **dos** estructuras clave-valor, y la más
antigua es la más característica.

**La lista de asociación (*alist*)**, de 1958:

```lisp
(defparameter *config* '((:host . "local") (:puerto . 8080)))
(cdr (assoc :puerto *config*))          ; 8080
(acons :nuevo 1 *config*)                ; añadir POR DELANTE, sin modificar
```

Es una lista de *conses*, con búsqueda lineal. Parece primitiva y tiene dos propiedades que la
mantienen viva: **es un dato literal** —se escribe, se imprime y se lee tal cual— y **es inmutable de
forma barata**, porque añadir por delante **oculta** la entrada anterior sin copiar nada. Eso la
convierte en la estructura natural para entornos y ámbitos anidados, que es exactamente para lo que la
usó Lisp desde el principio.

**La tabla hash**, estandarizada en 1984:

```lisp
(make-hash-table :test #'equal)          ; el TEST decide qué es "la misma clave"
(gethash clave tabla valor-por-defecto)
(setf (gethash clave tabla) valor)
(incf (gethash clave tabla 0))            ; contar: si no existe, empieza en 0
(remhash clave tabla)
(maphash (lambda (k v) ...) tabla)
(hash-table-count tabla)
```

La línea `(incf (gethash x tabla 0))` merece un momento: `gethash` con valor por defecto devuelve 0 si
la clave no está, e `incf` **funciona sobre `gethash` como lugar asignable**. Contar frecuencias cabe
en una expresión sin comprobar si la clave existe.

Eso es posible por **`setf` y el concepto de *lugar***: en Lisp, cualquier forma que "designe un
sitio" —`car`, `aref`, `gethash`, `slot-value`, un campo de `defstruct`— puede ir a la izquierda de
una asignación, y `incf`, `push` y `rotatef` funcionan sobre todas ellas.

Es la misma idea que las pseudovariables de PL/I y `$piece` de M, generalizada a todo el lenguaje y
extensible por el usuario con `define-setf-expander`.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea
set v [split [string trim $linea]]

set cuentas [dict create]
foreach x $v {
    dict incr cuentas $x            ;# incrementa, creando la clave si falta
}

puts "cuenta=[dict get $cuentas [lindex $v 0]]"
```

**Lo que esta clase enseña en Tcl.** Tcl tiene **dos** estructuras clave-valor, y la diferencia entre
ellas es una de las cosas que más confunde del lenguaje.

**El `array`**, desde 1988, que —como ya se dijo en la clase 089— **no es un arreglo**:

```tcl
set edad(ada) 36
set edad(alan) 41
array names edad
array size edad
info exists edad(ada)
array unset edad ada
```

Es una tabla *hash* y es **una variable especial, no un valor**: no se puede pasar a un procedimiento
ni guardar dentro de una lista. Hay que pasarlo **por nombre** y usar `upvar` (clase 080).

**El `dict`**, desde Tcl 8.5 (2007), que sí es un valor:

```tcl
set d [dict create a 1 b 2]
dict get $d a
dict set d c 3
dict incr d a
dict exists $d a
dict for {k v} $d { ... }
dict get $d usuarios ada correo      ;# ANIDADO, en una sola llamada
```

El `dict` llegó veinte años tarde y arregló todo lo que le faltaba al `array`: es un valor de primera
clase, se pasa y se devuelve, se anida y **conserva el orden de inserción**.

`dict incr` es el equivalente exacto del `(incf (gethash ...))` de Lisp: incrementa creando la clave
si no existe.

Y hay un detalle de implementación elegante: **un `dict` es un valor inmutable con copia al escribir**,
así que `dict set d c 3` conceptualmente crea un diccionario nuevo, pero si solo hay una referencia lo
modifica en el sitio. Se obtiene la semántica de valor con el rendimiento de la mutación.

La recomendación práctica hoy es clara: **`dict` para todo lo nuevo**, `array` solo cuando hace falta
la variable global compartida o al mantener código anterior a 2007.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;
my @v = split ' ', $linea;

my %cuentas;
$cuentas{$_}++ for @v;              # autovivificación: la clave se crea sola

print "cuenta=", $cuentas{$v[0]}, "\n";
```

**Lo que esta clase enseña en Perl.** El hash **está en la sintaxis del lenguaje**, con su propio
sigilo `%`, y esa decisión de 1987 es una de las razones por las que Perl dominó el procesamiento de
datos durante veinte años.

`$cuentas{$_}++` funciona sin comprobar si la clave existe por la **autovivificación**: al usar una
clave inexistente en un contexto que la necesita, Perl **la crea**. Con `undef` como valor, `++` lo
trata como 0.

Eso se extiende a las estructuras anidadas, y ahí es donde resulta espectacular:

```perl
$datos{ventas}{2026}{enero} += 100;      # crea los TRES niveles si no existen
push @{ $indice{$letra} }, $palabra;      # crea el arreglo si no existe
```

Ninguna de esas líneas necesita inicialización previa. Es comodísimo y tiene el peligro
correspondiente: **basta con leer una clave anidada para crear los niveles intermedios**, así que un
`if ($datos{a}{b})` inocente deja `$datos{a}` creado. `exists` sí evita crear el último nivel, pero no
los intermedios.

El resto del vocabulario de hashes de Perl es el que después copiaron muchos:

```perl
keys %h        values %h      each %h
exists $h{k}   delete $h{k}
my %copia = (%a, %b);                  # fusionar: gana el segundo
my @vals = @h{qw(a b c)};              # rebanada de hash (clase 094)
```

Y un detalle de seguridad que dejó huella: desde Perl 5.18, **el orden de las claves se aleatoriza en
cada ejecución**. Se hizo para evitar ataques de colisión de *hash* —enviar claves diseñadas para
degradar la tabla a lista enlazada— y rompió código que asumía un orden estable. Python hizo lo mismo
en 3.3 por la misma razón.

Es la lección del cierre de esta clase, aprendida a base de romper programas: **si el orden importa,
hay que pedirlo explícitamente** con `sort keys %h`.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>
#include <iterator>
#include <unordered_map>
#include <vector>

int main() {
    std::vector<int> v{std::istream_iterator<int>(std::cin),
                       std::istream_iterator<int>()};
    if (v.empty()) return 1;

    std::unordered_map<int, int> cuentas;
    for (int x : v) {
        ++cuentas[x];               // operator[] CREA la entrada con valor 0
    }

    std::cout << "cuenta=" << cuentas[v.front()] << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** `++cuentas[x]` funciona porque **`operator[]` de un mapa inserta
la clave con el valor por defecto si no existe** —0 para un `int`— y devuelve una referencia. Es la
autovivificación de Perl, con tipos.

Y esa comodidad esconde la trampa más conocida de los mapas de C++: **`operator[]` sobre un mapa
constante no compila, y sobre uno mutable MODIFICA el mapa aunque solo quisieras consultar**.

```cpp
if (m[clave] == 0) { ... }        // ¡acaba de INSERTAR clave con valor 0!
if (m.count(clave)) { ... }        // consulta sin insertar
if (m.contains(clave)) { ... }     // C++20, más legible
auto it = m.find(clave);           // consulta y deja la posición para reutilizar
```

Los dos mapas de C++ repiten la división de la clase 094:

| | `std::map` | `std::unordered_map` |
|---|---|---|
| Estructura | árbol rojo-negro | tabla *hash* |
| Complejidad | O(log n) | O(1) promedio |
| Orden | **por clave** | arbitrario |
| Desde | C++98 | C++11 |

Y hay una crítica bien fundada a `std::unordered_map` que conviene conocer: **el estándar exige
encadenamiento con cubetas**, es decir, listas enlazadas por cubeta y estabilidad de las referencias.
Eso impide implementaciones de direccionamiento abierto, que son considerablemente más rápidas por
localidad de caché. Por eso las alternativas —`absl::flat_hash_map` de Google, `robin_hood`,
`ankerl::unordered_dense`— superan a la estándar por factores de dos a cinco, y son la elección
habitual en código donde el rendimiento importa.

Es un caso ejemplar de cómo **especificar demasiado en un estándar limita las implementaciones para
siempre**, porque cambiarlo rompería la compatibilidad binaria.

C++17 añadió `try_emplace` e `insert_or_assign`, que resuelven la inserción condicional sin construir
el valor dos veces.

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

dcl-pi MAPA;
  entrada char(200) const;
end-pi;

dcl-ds tabla qualified dim(100);
  clave  int(10);
  cuenta int(10);
end-ds;

dcl-s n       int(10) inz(0);
dcl-s i       int(10);
dcl-s j       int(10);
dcl-s pos     int(10);
dcl-s valor   int(10);
dcl-s primero int(10) inz(0);
dcl-s hay     ind inz(*off);
dcl-s tok     varchar(20) inz('');
dcl-s c       char(1);

for i = 1 to %len(%trimr(entrada)) + 1;
  if i <= %len(%trimr(entrada));
    c = %subst(entrada : i : 1);
  else;
    c = ' ';
  endif;

  if c = ' ';
    if tok <> '';
      valor = %int(tok);
      if not hay;
        primero = valor;
        hay = *on;
      endif;
      pos = 0;
      for j = 1 to n;
        if tabla(j).clave = valor;
          pos = j;
        endif;
      endfor;
      if pos = 0;
        n += 1;
        tabla(n).clave = valor;
        tabla(n).cuenta = 1;
      else;
        tabla(pos).cuenta += 1;
      endif;
      tok = '';
    endif;
  else;
    tok += c;
  endif;
endfor;

pos = 0;
for j = 1 to n;
  if tabla(j).clave = primero;
    pos = j;
  endif;
endfor;

dsply ('cuenta=' + %char(tabla(pos).cuenta));

*inlr = *on;
return;
```

**Lo que esta clase enseña en RPG.** **RPG no tiene diccionarios**, y la respuesta idiomática es la de
este programa: una **estructura de datos con `dim`** (clase 091) que funciona como tabla de pares, más
`%lookup` para consultarla.

Con `sorta` y `%lookup` sobre una tabla ordenada, la consulta es binaria — el mismo nivel que el
`SEARCH ALL` de COBOL.

Donde RPG se separa de COBOL es en lo que hay **encima**: en IBM i, la respuesta natural a esta clase
no es una tabla en memoria sino **SQL incrustado**, y es idiomático desde hace veinte años.

```rpgle
exec sql
  select count(*) into :cuenta
  from movimientos
  where codigo = :buscado;
```

O, para una tabla de referencia que se consulta muchas veces, un **fichero indexado por clave** leído
con `chain`:

```rpgle
chain (codigo) TARIFAS;
if %found(TARIFAS);
  importe = precio * cantidad;
endif;
```

**`chain` es una consulta a un índice de base de datos escrita como una operación del lenguaje**, y
`%found` dice si acertó. Es la misma idea que el `READ ... KEY IS` de COBOL sobre VSAM y que los
*globals* de M: **el diccionario está en disco y el lenguaje lo consulta directamente**.

Que tres de los lenguajes más viejos de esta página —COBOL, RPG y M— resuelvan el diccionario en la
capa de datos y no en memoria no es casualidad: **son lenguajes de sistemas de gestión, donde los
datos siempre fueron más grandes que la memoria**. La estructura tenía que estar en disco desde el
primer día.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 mapa: procedure options(main);

    declare linea char(200) varying;
    declare 1 tabla(100),
              2 clave  fixed binary(31),
              2 cuenta fixed binary(31);
    declare (n, i, j, pos, valor, primero) fixed binary(31);
    declare hay bit(1) initial('0'b);
    declare tok char(20) varying initial('');
    declare c char(1);

    get edit (linea) (a(200));
    n = 0;

    do i = 1 to length(linea) + 1;
       if i <= length(linea) then c = substr(linea, i, 1); else c = ' ';
       if c = ' ' then do;
          if tok ^= '' then do;
             valor = tok;
             if ^hay then do; primero = valor; hay = '1'b; end;
             pos = 0;
             do j = 1 to n;
                if clave(j) = valor then pos = j;
             end;
             if pos = 0 then do;
                n = n + 1;
                clave(n) = valor;
                cuenta(n) = 1;
             end;
             else cuenta(pos) = cuenta(pos) + 1;
             tok = '';
          end;
       end;
       else tok = tok || c;
    end;

    pos = 0;
    do j = 1 to n;
       if clave(j) = primero then pos = j;
    end;

    put skip list ('cuenta=' || trim(char(cuenta(pos))));

 end mapa;
```

**Lo que esta clase enseña en PL/I.** **PL/I no tiene tablas asociativas**, y este programa usa lo que
sí tiene: un **arreglo de estructuras** (clase 089), que en PL/I se declara con la elegancia de poder
tratar los campos como columnas.

```pli
declare 1 tabla(100),
          2 clave  fixed binary(31),
          2 cuenta fixed binary(31);

cuenta = 0;                    /* pone a cero LAS CIEN cuentas */
```

Esa segunda línea —una asignación que recorre un campo de cien registros— vuelve a aparecer aquí, y
sigue sin tener equivalente en el núcleo.

Para diccionarios de verdad, un programa PL/I hace una de tres cosas, y todas se ven en código real:

1. **Tabla ordenada con búsqueda binaria**, escrita a mano.
2. **Una estructura enlazada** con `based` y punteros (clase 090), típicamente un árbol o una tabla
   *hash* con encadenamiento — PL/I tiene todo lo necesario y era habitual escribirlo.
3. **Delegar en la plataforma**: DB2, VSAM o un fichero indexado.

La segunda merece una nota, porque PL/I fue **el primer lenguaje de alto nivel con punteros y
reserva dinámica listos para construir estructuras enlazadas** (1964), antes que C. La razón de que
esas estructuras no acabaran en una biblioteca estándar es de época: **en 1964 no existía la idea de
biblioteca estándar de estructuras de datos**. El lenguaje daba las piezas y cada instalación
construía las suyas.

Ese es, probablemente, el mayor cambio entre aquella época y la actual, y explica media docena de
"carencias" de los lenguajes de esta página: no es que no supieran hacer un diccionario, es que **la
noción de que el lenguaje debía traerlo hecho no se generalizó hasta los años noventa**.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
MAPA ; Mapas y diccionarios -- clase 095
 read linea
 kill cuenta
 set n = $length(linea, " ")
 for i=1:1:n do
 . set x = $piece(linea, " ", i)
 . set cuenta(x) = $get(cuenta(x), 0) + 1
 set primero = $piece(linea, " ", 1)
 write "cuenta=", cuenta(primero), !
 quit
```

**Lo que esta clase enseña en M.** Aquí M gana, y merece decirse sin rodeos: **el array de M es un
diccionario, y lleva siéndolo desde 1966**, cuando ningún lenguaje mayoritario tenía uno.

```mumps
 set cuenta("ada") = 1        ; clave de texto
 set cuenta(36) = 1            ; clave numérica
 set cuenta(1, "x") = 1        ; clave COMPUESTA, sin declarar nada
```

`$get(cuenta(x), 0)` devuelve el valor o **0 si no existe**, que es el mismo idioma que
`(gethash x tabla 0)` en Lisp y `dict incr` en Tcl, veinte años antes que los dos.

Y hay tres propiedades que lo separan de cualquier tabla *hash*:

**Está ordenado.** Las claves se mantienen en orden —numérico primero, después por texto— y `$order`
las recorre así. Un diccionario ordenado, siempre, sin pedirlo.

**Es multinivel sin límite.** `cuenta(a, b, c, d)` es legal y no hay que crear los niveles
intermedios. Es un árbol, un diccionario anidado y una tabla multidimensional a la vez.

**Y con `^` delante, está en disco.**

```mumps
 set ^CUENTA(codigo) = $get(^CUENTA(codigo), 0) + 1
```

Esa línea incrementa un contador **persistente, transaccional y compartido entre todos los procesos
del sistema**, con la misma sintaxis que la variable local. No hay conexión, no hay consulta, no hay
serialización y no hay caché que invalidar.

Es, en una línea, la razón por la que M sigue existiendo: **la distancia entre la estructura de datos
del programa y la de la base de datos es un carácter**. Los lenguajes modernos han dedicado décadas a
reducir esa distancia con ORMs, y M la eliminó no cerrando la brecha sino no abriéndola nunca.

El precio es todo lo demás: sin tipos, sin espacios de nombres, sin encapsulación y con una sintaxis
de los años sesenta.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| v cuentas |

v := stdin nextLine substrings collect: [ :cada | cada asNumber ].

cuentas := Bag new.
v do: [ :cada | cuentas add: cada ].

Transcript
    show: 'cuenta=', (cuentas occurrencesOf: v first) printString;
    cr.
```

**Lo que esta clase enseña en Smalltalk.** El programa usa **`Bag`** en lugar de `Dictionary`, porque
`Bag` **es** el contador de frecuencias: una colección que admite repetidos y sabe cuántas veces está
cada elemento.

```smalltalk
| b |
b := Bag new.
b add: 'ada'; add: 'ada'; add: 'alan'.
b occurrencesOf: 'ada'.      "2"
b size.                       "3 -- el TOTAL, no los distintos"
b asSet size.                 "2 -- los distintos"
b sortedCounts.               "los elementos ordenados por frecuencia"
```

Que exista una clase dedicada a esto desde 1980, cuando en la mayoría de los lenguajes sigue siendo un
diccionario a mano, es representativo del cuidado con que se diseñó esa jerarquía de colecciones.

`Dictionary` es lo esperable, con el protocolo de mensajes que caracteriza al lenguaje:

```smalltalk
d at: #clave put: 1.
d at: #clave.
d at: #clave ifAbsent: [ 0 ].              "valor por defecto, PEREZOSO"
d at: #clave ifAbsentPut: [ 0 ].            "y lo inserta si falta"
d at: #clave ifPresent: [ :v | ... ] ifAbsent: [ ... ]
d keysAndValuesDo: [ :k :v | ... ]
d associationsDo: [ :a | ... ]              "clase 091"
```

Fíjate en que el valor por defecto se pasa **como bloque**, no como valor: `ifAbsent: [ 0 ]` **solo se
evalúa si hace falta**. Con un valor directo, calcular un defecto caro costaría siempre. Es evaluación
perezosa conseguida sin ninguna característica especial del lenguaje — solo bloques, otra vez.

Y hay tres variantes que distinguen por igualdad, que es la clase 101 anticipada:
`IdentityDictionary` compara con `==`, `Dictionary` con `=`, y `WeakKeyDictionary` **no impide que el
recolector de basura se lleve la clave** — un diccionario que no retiene lo que guarda, útil para
cachés.

---

## Y de vuelta a la clase

Lo transferible: **un diccionario es un compromiso entre velocidad y orden, y hay que elegir**. La
tabla *hash* da O(1) y devuelve las claves en un orden arbitrario que **puede cambiar entre
ejecuciones**; el árbol da O(log n) y las devuelve ordenadas. Perl y Python aleatorizan
deliberadamente el orden de un hash por seguridad, y de ahí salen errores intermitentes en programas
que asumían un orden estable. Si el orden importa, dilo en el tipo: `std::map`, `Ordered_Maps`,
`SortedDictionary`.

⏮️ [Volver a la clase 095](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
