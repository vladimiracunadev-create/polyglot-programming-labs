# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 170

> [⬅️ Volver a la clase 170](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Sumar una lista: `total=60`. Es lo que hace un `SUM()` en SQL, y esta clase trata de la decisión que hay
detrás: **quién hace el trabajo con los datos, el lenguaje o la base**. Y aquí hay dos de esta página que
no tienen el problema que todos los demás sufren: **M y Smalltalk con GemStone no tienen desajuste entre
el modelo del lenguaje y el de la base**, porque **su base de datos guarda lo mismo que su lenguaje
manipula**.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es el **acceso a datos como componente**, y estos lenguajes lo enseñan porque **cubren
> los tres modelos que existen**: el **navegacional** —moverse registro a registro por índices— que
> COBOL, RPG y M practican; el **relacional** con SQL embebido, que todos adoptaron; y el **de objetos
> persistentes**, que M y GemStone tienen de fábrica.
>
> Y aparece la tensión que ordena la clase: **el desajuste de impedancia** — que las tablas y las
> estructuras del lenguaje no encajan, y que treinta años de mapeadores objeto-relacionales han intentado
> tapar.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: una línea con enteros separados por espacio (valores a agregar) → stdout: `total=<suma de los valores>`
- **Regla:** `total = suma de los valores`

| stdin | esperado |
|---|---|
| `10 20 30` | `total=60` |
| `5` | `total=5` |
| `1 2 3 4` | `total=10` |

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
PROGRAM-ID. DATOS.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(200).
01  I       PIC 9(4) COMP.
01  C       PIC X.
01  NUM     PIC S9(9) COMP VALUE 0.
01  TOTAL   PIC S9(9) COMP VALUE 0.
01  ENNUM   PIC 9      VALUE 0.
01  ED      PIC -(8)9.

PROCEDURE DIVISION.
    ACCEPT LINEA

    PERFORM VARYING I FROM 1 BY 1 UNTIL I > 200
        MOVE LINEA(I:1) TO C
        IF C IS NUMERIC
            COMPUTE NUM = NUM * 10 + FUNCTION NUMVAL(C)
            MOVE 1 TO ENNUM
        ELSE
            IF ENNUM = 1
                COMPUTE TOTAL = TOTAL + NUM
                MOVE 0 TO NUM
                MOVE 0 TO ENNUM
            END-IF
        END-IF
    END-PERFORM

    MOVE TOTAL TO ED
    DISPLAY "total=" FUNCTION TRIM(ED)
    STOP RUN.
```

**COBOL y el componente de datos.** COBOL vivió los dos modelos del "por qué" de esta clase, y merece
verlos juntos porque la comparación es el contenido de la clase.

**El navegacional, con VSAM:**

```cobol
           START CLIENTES KEY >= WS-ID
           PERFORM UNTIL FIN
               READ CLIENTES NEXT
                   AT END SET FIN TO TRUE
               END-READ
               ADD CLI-IMPORTE TO WS-TOTAL
           END-PERFORM
```

**Y el relacional, con SQL embebido:**

```cobol
           EXEC SQL
               SELECT SUM(IMPORTE) INTO :WS-TOTAL
                 FROM CLIENTES
                WHERE ZONA = :WS-ZONA
           END-EXEC
```

**Y la diferencia es la del cierre de esta clase**: el primero trae **todas las filas al programa** y suma
una a una; el segundo **suma en la base y trae un número**.

Con un millón de filas, **la diferencia es de dos órdenes de magnitud** — y no por el lenguaje, sino por
cuántas veces se cruza la frontera (clase 155).

Y merece decir cuándo el navegacional sigue siendo correcto, porque no es nunca: **cuando hay que hacer
algo con cada fila**.

```text
Un proceso de cierre que recorre 20 millones de pólizas
y aplica una regla distinta a cada una NO se puede expresar en SQL,
y el acceso secuencial por bloques es lo más rápido que existe (clase 152).
```

**Y ahí la técnica de la clase 152 es la que manda**: **ordenar los ficheros por la misma clave y
recorrerlos en paralelo**, en lugar de consultar por cada fila.

Y esta clase debe recoger la propiedad de COBOL que más importa en el componente de datos y que la clase
072 explicó: **el tipo decimal**.

```cobol
       01  IMPORTE PIC S9(13)V99 COMP-3.
```

```sql
CREATE TABLE ... (importe DECIMAL(15,2))
```

**Los dos son decimales exactos, y encajan sin pérdida.** Es una de las pocas correspondencias perfectas
entre un lenguaje y una base de datos de esta página, y es la razón por la que **migrar esa aritmética a
un lenguaje con `double` es un problema** (clase 140).

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program datos
   implicit none
   character(len=200) :: linea
   integer :: total, valor, ios, pos

   read(*, '(A)') linea
   total = 0
   pos = 1

   do
      read(linea(pos:), *, iostat=ios) valor
      if (ios /= 0) exit
      total = total + valor
      pos = pos + index(linea(pos:), ' ')
      if (pos > len_trim(linea)) exit
   end do

   write(*, '(A,I0)') 'total=', total
end program datos
```

**Fortran y el componente de datos.** El cálculo científico casi no usa bases de datos relacionales, y
merece explicar por qué, porque la razón es técnica y buena: **sus datos no son filas**.

```text
Un resultado de simulación es un ARREGLO de 1.000 × 1.000 × 500 valores,
con coordenadas, tiempo y metadatos.

Guardarlo como 500 millones de filas en una tabla sería absurdo:
  - el tamaño se multiplicaría por diez
  - y leer un corte sería lentísimo
```

**Y por eso este dominio usa formatos de arreglos** (clase 159): **NetCDF, HDF5 y hoy Zarr**.

Y sus capacidades merecen enumerarse, porque son las de una base de datos para este tipo de dato:

| Capacidad | Cómo |
|---|---|
| **Consulta por rebanada** | leer solo `datos(100:200, :, 5)` sin cargar el resto |
| **Compresión por trozos** | cada bloque comprimido por separado |
| **Metadatos** | unidades, coordenadas, procedencia (clase 160) |
| **Acceso paralelo** | HDF5 sobre MPI-IO: mil procesos escribiendo a la vez |
| **Y en la nube** | Zarr: cada trozo es un objeto, leíble por rango HTTP |

**La primera es la clave y es exactamente la regla del cierre de esta clase**: **pedir solo lo que hace
falta, y que el sistema de almacenamiento haga el trabajo de localizarlo**.

Es lo mismo que un índice en SQL, con otro nombre y sobre otra forma de dato.

Y donde Fortran sí toca bases de datos relacionales es en los metadatos, y merece nombrarlo: **el
catálogo de ejecuciones**.

```sql
-- qué se ejecutó, con qué parámetros, cuándo, y dónde está el resultado
CREATE TABLE ejecuciones (id, fecha, version_codigo, hash_config, ruta_salida, ...)
```

**Y eso resuelve el problema de la clase 154** —la deuda de reproducibilidad— **mejor que cualquier otra
cosa**: si cada ejecución queda registrada con su versión de código y su configuración, **un resultado de
hace cinco años se puede rastrear**.

Es una práctica barata, poco extendida, y de las que más valor dan en este dominio.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;
with Ada.Strings;
with Ada.Strings.Fixed;

procedure Datos is
   Total, Valor : Integer := 0;
begin
   Total := 0;
   loop
      begin
         Get (Valor);
         Total := Total + Valor;
      exception
         when others => exit;
      end;
   end loop;

   Put_Line ("total=" & Ada.Strings.Fixed.Trim (Total'Image, Ada.Strings.Both));
end Datos;
```

**Ada y el componente de datos.** Ada tiene acceso a bases de datos —GNATCOLL.SQL, APQ— y esta clase es el
sitio para una capacidad suya que resuelve el desajuste del "por qué" mejor que un mapeador:
**GNATCOLL.SQL genera código Ada desde el esquema**.

```bash
gnatcoll_db2ada -dbmodel=esquema.txt -api=Base
```

```ada
--  Y a partir de ahí, las consultas se escriben con TIPOS COMPROBADOS:
Q : constant SQL_Query :=
      SQL_Select (Fields  => Clientes.Nombre & Clientes.Saldo,
                  From    => Clientes,
                  Where   => Clientes.Zona = Text_Param (1));
```

**Y lo que eso da es lo que esta clase busca**: **un error de nombre de columna o de tipo es un error de
compilación**, no un fallo en producción.

Es la misma idea que jOOQ en Java, sqlc en Go y Diesel en Rust — **generar el acceso desde el esquema en
lugar de escribir cadenas** — y es la respuesta correcta al desajuste de impedancia: **no tapar la
diferencia, sino comprobarla**.

Y merece añadir la aportación de Ada al componente de datos que su sistema de tipos permite y que la
clase 124 explicó: **el dominio en el tipo**.

```ada
subtype Codigo_Postal is String (1 .. 5)
   with Dynamic_Predicate => (for all C of Codigo_Postal => C in '0' .. '9');
type Saldo is delta 0.01 range -1_000_000.00 .. 1_000_000.00;
```

**Y ahí está la propiedad valiosa**: **la restricción que la base de datos tiene en un `CHECK` está
también en el programa**, con el mismo significado.

En la mayoría de los sistemas, **la validación está escrita dos veces —en la base y en el código— y
diverge** (clase 140). Aquí, **al menos, las dos son explícitas y revisables**.

Y merece cerrar con la observación práctica que este dominio impone y que casi nadie más se plantea: **en
un sistema de tiempo real, una consulta a base de datos no es aceptable en el camino crítico**, porque
**su tiempo no está acotado**.

Así que el reparto es: **el control trabaja con datos en memoria, y la persistencia ocurre fuera del
lazo** — que es otra vez la separación por plazos de la clase 165.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Datos;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  Linea, Tok: string;
  I, Total: Integer;

begin
  ReadLn(Linea);
  Linea := Trim(Linea) + ' ';
  Total := 0;
  Tok := '';

  for I := 1 to Length(Linea) do
    if Linea[I] = ' ' then
    begin
      if Tok <> '' then Total := Total + StrToInt(Tok);
      Tok := '';
    end
    else
      Tok := Tok + Linea[I];

  WriteLn('total=', IntToStr(Total));
end.
```

**Pascal y el componente de datos.** El ecosistema Delphi tiene una abstracción de datos muy influyente y
merece explicarla porque su modelo se copió mucho: **el `TDataSet`**.

```pascal
Query.SQL.Text := 'SELECT nombre, saldo FROM clientes WHERE zona = :zona';
Query.ParamByName('zona').AsString := Zona;      { ← parametrizado (clase 153) }
Query.Open;

while not Query.Eof do
begin
  Total := Total + Query.FieldByName('saldo').AsCurrency;
  Query.Next;
end;
```

**`TDataSet` es un cursor navegable con una API común**, y de ahí sale la propiedad que hizo famoso a
Delphi: **cualquier control visual se conecta a él** (clase 169).

Y merece señalar dos cosas de ese fragmento, porque son las reglas del cierre de esta clase:

**Una, `ParamByName` en lugar de concatenar** — la defensa contra la inyección, y además **permite que la
base reutilice el plan de ejecución** (clase 152).

**Y dos, ese bucle es exactamente lo que el cierre desaconseja.**

```pascal
{ ✓ que sume la base }
Query.SQL.Text := 'SELECT SUM(saldo) FROM clientes WHERE zona = :zona';
```

Y `Currency` merece la mención porque es una decisión acertada del lenguaje: **es un entero de 64 bits
escalado por 10.000**, así que **es decimal exacto con cuatro decimales** — el tipo correcto para dinero
(clase 072), y encaja con `DECIMAL` de SQL sin pérdida.

Y el ecosistema moderno:

| Herramienta | Notas |
|---|---|
| **FireDAC** | el acceso a datos actual de Delphi, con muchos motores |
| **SQLdb / ZeosLib** | los de Free Pascal |
| **mORMot ORM** | mapeo objeto-relacional rápido (clase 168) |
| **`TFDMemTable`** | conjuntos de datos en memoria, para pruebas |

**El último merece la mención** porque resuelve un problema de la clase 139: **probar el código de datos
sin base de datos**, cargando un conjunto en memoria con la misma API.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let ((total 0))
  (with-input-from-string (s (read-line))
    (loop for valor = (read s nil nil)
          while valor
          do (incf total valor)))
  (format t "total=~D~%" total))
```

**Lisp y el componente de datos.** Lisp tiene una relación con SQL que merece contarse porque su enfoque
es distinto: **generar la consulta como estructura, no como texto**.

```lisp
(select (:sum :saldo)
  (from :clientes)
  (where (:= :zona zona)))
;; → "SELECT SUM(saldo) FROM clientes WHERE zona = ?"  con el parámetro aparte
```

**La consulta se construye como listas anidadas** —que es como Lisp representa todo (clase 123)— y **la
biblioteca la traduce a SQL con parámetros**.

Y las ventajas son exactamente las dos reglas del cierre de esta clase:

**Una, es imposible la inyección**: los valores **nunca se concatenan**, van como parámetros por
construcción.

**Y dos, la consulta se puede componer con funciones**:

```lisp
(defun con-filtro-zona (consulta zona)
  (if zona (append consulta `((where (:= :zona ,zona)))) consulta))
```

**Construir consultas dinámicas concatenando cadenas es la fuente número uno de inyecciones**; hacerlo
con estructuras **es seguro por construcción**.

Es la misma idea que las consultas como árbol de jOOQ, de SQLAlchemy y de Ecto, y en Lisp sale del propio
lenguaje.

Y el ecosistema:

| Biblioteca | Notas |
|---|---|
| **Postmodern** | PostgreSQL, con S-SQL: consultas como formas Lisp |
| **CLSQL** | veterana, varios motores |
| **Mito** | mapeador objeto-relacional |
| **cl-dbi** | interfaz común, al estilo de DBI (clase 158) |

Y merece cerrar con una idea que Lisp permite y que este componente agradece: **la base de datos también
puede ejecutar Lisp**.

```sql
CREATE FUNCTION calcular(...) RETURNS numeric AS $$ ... $$ LANGUAGE plpgsql;
```

**PostgreSQL admite funciones en varios lenguajes**, y existe `pl/lisp` entre ellos.

Y el criterio para usarlo es el del cierre: **la lógica que necesita muchos datos debe ejecutarse donde
están los datos**. Mover un cálculo a la base es la misma optimización que mover un cálculo al núcleo
numérico (clase 155): **acercar el código al dato en lugar del dato al código**.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea

set total 0
foreach v [split [string trim $linea]] {
    if {$v ne ""} { incr total $v }
}

puts "total=$total"
```

**Tcl y el componente de datos.** Tcl tiene una interfaz de bases de datos con un diseño limpio y merece
verla: **TDBC**, del propio núcleo desde Tcl 8.6.

```tcl
package require tdbc::postgres

tdbc::postgres::connection create db -host localhost -db midb

set stmt [db prepare {SELECT SUM(saldo) AS total FROM clientes WHERE zona = :zona}]
$stmt foreach fila {
    puts [dict get $fila total]
} -as dicts
```

**Y tres detalles merecen destacarse porque son buenas decisiones:**

**`:zona` con dos puntos toma el valor de la variable Tcl del mismo nombre** — parametrizado por defecto,
y sin escribir la vinculación.

**`foreach` sobre la sentencia recorre las filas sin cargarlas todas**, que es lo correcto con conjuntos
grandes.

**Y `-as dicts` devuelve cada fila como diccionario**, con los nombres de columna — lo que hace el código
legible sin mapeador.

Y Tcl aporta a esta clase una capacidad que su modelo de datos hace natural y que la clase 152 explicó:
**la representación dual**.

```tcl
# Una fila de la base llega como diccionario; y es a la vez una cadena
set fila [dict create id 1 nombre "Ana" saldo 100.50]
puts $fila         ;# id 1 nombre Ana saldo 100.50
```

**Así que serializar el resultado para pasarlo a otro proceso** (clase 161) **es imprimirlo**, y volver a
interpretarlo es leerlo.

Y merece cerrar con el papel real de Tcl en este componente y que es el de la clase 165: **el pegamento de
datos**.

```tcl
# Extraer de un sistema, transformar, cargar en otro: en veinte líneas
$origen foreach fila {
    set transformada [transformar $fila]
    $destino allrows -- $insert $transformada
}
```

**Es el ETL de Perl en esta página** (clase 165), con la ventaja de que **TDBC da la misma API para todos
los motores**, así que el guion no cambia al cambiar de base.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;
use List::Util qw(sum0);

my $linea = <STDIN>;
chomp $linea;

print "total=", sum0(split ' ', $linea), "\n";
```

**Perl y el componente de datos.** Perl tiene **DBI**, que la clase 158 ya presentó como el modelo que
copiaron JDBC y DB-API, y esta clase es el sitio para ver sus decisiones de uso:

```perl
my $dbh = DBI->connect($dsn, $usuario, $clave, {
    RaiseError  => 1,        # ← los errores LANZAN, no devuelven undef
    AutoCommit  => 0,        # ← transacciones explícitas
    PrintError  => 0,
});

my $total = $dbh->selectrow_array(
    'SELECT SUM(saldo) FROM clientes WHERE zona = ?', undef, $zona);

$dbh->commit;
```

**`RaiseError => 1` es la primera línea que hay que escribir**, y merece explicarlo: **sin él, DBI
devuelve `undef` en caso de error y el programa sigue** — con lo que un fallo de base de datos se
convierte en un cálculo con datos incompletos.

Es el mismo argumento que los avisos como errores de la clase 147: **hacer que el fallo sea imposible de
ignorar**.

Y `selectrow_array` con una consulta agregada es la regla del cierre en una línea: **la base suma, el
programa recibe un número**.

Y merece contrastar con el antipatrón que esta clase quiere señalar y que tiene nombre: **el problema
N+1**.

```perl
# ✗ N+1: una consulta para los pedidos, y UNA MÁS por cada uno
my $pedidos = $dbh->selectall_arrayref('SELECT id FROM pedidos');
for my $p (@$pedidos) {
    my $lineas = $dbh->selectall_arrayref(
        'SELECT * FROM lineas WHERE pedido = ?', undef, $p->[0]);   # ← ¡mil viajes!
}

# ✓ una consulta con unión, o dos consultas y agrupar en memoria
my $todo = $dbh->selectall_arrayref(
    'SELECT p.id, l.* FROM pedidos p JOIN lineas l ON l.pedido = p.id',
    { Slice => {} });
```

**El problema N+1 es el fallo de rendimiento más común de cualquier aplicación con base de datos**, y lo
producen sobre todo los mapeadores objeto-relacionales, porque **hacen que cada acceso a una relación
parezca un atributo**.

Es la consecuencia directa del desajuste del "por qué" de esta clase: **la abstracción que oculta la
frontera hace fácil cruzarla mil veces sin darse cuenta** (clase 155).

Y la defensa práctica es la de la clase 152: **medir**. Un registro de consultas por petición, con el
número y el tiempo total, **hace visible el N+1 el día que aparece** en lugar de seis meses después.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>

int main() {
    long long total = 0, valor = 0;
    while (std::cin >> valor) total += valor;

    std::cout << "total=" << total << '\n';
    return 0;
}
```

**C++ y el componente de datos.** C++ es, otra vez, **el suelo**: PostgreSQL, MySQL, SQLite, MongoDB,
ClickHouse y RocksDB están escritos en C o C++.

Y para usarlas desde C++, el ecosistema:

| Biblioteca | Notas |
|---|---|
| **libpq / libmysqlclient** | las de C, oficiales |
| **SOCI** | interfaz común, al estilo de DBI |
| **sqlpp11** | **consultas comprobadas en compilación**, con el esquema en C++ |
| **ODB** | mapeador objeto-relacional con generador de código |
| **SQLite embebido** | la base de datos **dentro** del proceso |

**`sqlpp11` merece la mención** porque hace en C++ lo que GNATCOLL en Ada de esta página: **la consulta se
escribe con tipos, y una columna mal escrita no compila**.

Y **SQLite embebido merece un apartado propio**, porque cambia el reparto de esta clase:

```cpp
sqlite3_open("datos.db", &db);
```

**No hay servidor, ni conexión, ni red**: la base de datos es **una biblioteca dentro del proceso** y los
datos, **un fichero**.

Y sus consecuencias merecen enumerarse porque son las que la han hecho la base de datos más desplegada del
mundo —está en todos los teléfonos, todos los navegadores y casi todas las aplicaciones de escritorio—:

| Propiedad | Consecuencia |
|---|---|
| **Sin proceso servidor** | cero administración, cero configuración |
| **Un fichero** | copiar la base es copiar un fichero |
| **Transacciones ACID reales** | con confirmación en dos fases sobre el sistema de ficheros |
| **Y una consulta no cruza ninguna frontera** | microsegundos, no milisegundos |

**La última es la que conecta con el cierre de esta clase**: **con SQLite, el problema N+1 casi
desaparece**, porque cada consulta cuesta microsegundos y no hay viaje de red.

**Y eso cambia el diseño**: lo que en una base cliente-servidor sería un antipatrón, aquí puede ser
razonable.

Es un buen recordatorio de que **las reglas de rendimiento dependen de la frontera** (clase 155), y de
que conviene saber cuál se tiene delante antes de aplicar una receta.

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

dcl-pi DATOS;
  linea char(200) const;
end-pi;

dcl-s texto varchar(200);
dcl-s pos   int(10);
dcl-s total int(20);

texto = %trim(linea) + ' ';
total = 0;

dow %len(%trim(texto)) > 0;
  pos = %scan(' ' : texto);
  if pos = 0;
    leave;
  endif;
  if pos > 1;
    total += %int(%subst(texto : 1 : pos - 1));
  endif;
  texto = %trim(%subst(texto : pos + 1));
enddo;

dsply ('total=' + %char(total));

*inlr = *on;
return;
```

**RPG y el componente de datos.** IBM i tiene la integración más estrecha de esta página entre lenguaje y
base de datos, y esta clase es el sitio para el detalle que la explica: **Db2 for i y el sistema son la
misma cosa** (clase 139).

```rpgle
// El acceso NATIVO: los ficheros son parte del programa
dcl-f clientes keyed;
chain (idCliente) clientes;
if %found(clientes);
  total += saldo;
endif;

// Y el SQL, embebido y comprobado en compilación (clase 163)
exec sql SELECT SUM(saldo) INTO :total
           FROM clientes WHERE zona = :zona;
```

**Y las dos formas acceden a los MISMOS datos** — no hay dos motores ni sincronización: **una tabla SQL y
un fichero físico son el mismo objeto visto de dos maneras**.

Es una propiedad poco común y merece destacarla: **el mismo dato se puede leer registro a registro con
acceso nativo y por conjuntos con SQL, indistintamente**.

Y por eso la transición de esta plataforma —**de navegacional a SQL** (clase 152)— pudo hacerse **fila a
fila y programa a programa**, sin migrar nada.

Y las razones para preferir SQL, que son las del cierre de esta clase, merecen enumerarse porque en esta
plataforma son medibles:

| SQL gana en | Por qué |
|---|---|
| **Agregar y filtrar** | el optimizador elige el plan (clase 152) |
| **Uniones** | imposibles de expresar bien con acceso nativo |
| **Paralelismo** | Db2 puede repartir la consulta |
| **Índices nuevos sin tocar el programa** | el Index Advisor los sugiere |

**Y el acceso nativo gana en un caso**: **procesar cada fila de un fichero enorme en orden de clave**, que
es el proceso de lote de la clase 152.

Y merece cerrar con la capacidad de esta plataforma que la clase 142 ya nombró y que aquí es el
complemento del componente de datos: **todo el catálogo es consultable con SQL**.

```sql
SELECT * FROM QSYS2.SYSTABLES WHERE TABLE_SCHEMA = 'MIBIB';
SELECT * FROM QSYS2.SYSIXADV ORDER BY TIMES_ADVISED DESC;
```

**Preguntar al sistema qué tablas hay, qué índices faltan y qué consultas van lentas es SQL** — lo que
convierte el mantenimiento del componente de datos en algo que cualquiera con SQL puede hacer.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 datos: procedure options(main);

    declare valor fixed binary(31);
    declare total fixed binary(31) initial(0);

    on endfile(sysin) goto fin;

    do while ('1'b);
       get list (valor);
       total = total + valor;
    end;

 fin:
    put skip list ('total=' || trim(char(total)));

 end datos;
```

**PL/I y el componente de datos.** PL/I vivió una generación de bases de datos que merece conocerse porque
precede a lo relacional y sigue en producción: **IMS DB, jerárquica, de 1966**.

```pli
 call plitdli(cuatro, 'GU      ', pcb, area, ssa1);   /* Get Unique */
 call plitdli(cuatro, 'GNP     ', pcb, area, ssa2);    /* Get Next in Parent */
```

**IMS organiza los datos en árboles**: un cliente tiene pedidos, un pedido tiene líneas — **y se navega
por la jerarquía**.

Y merece la comparación, porque explica por qué lo relacional ganó y también qué se perdió:

| | IMS jerárquica | Relacional |
|---|---|---|
| Consultas previstas | **rapidísimas** | rápidas |
| Consultas **no** previstas | **muy difíciles** | naturales |
| Modelo de datos | fijo, decidido al diseñar | flexible |
| Uniones arbitrarias | no | sí |
| **Rendimiento máximo** | **el más alto que existe** | muy bueno |

**La última fila merece la mención porque es real**: **IMS sigue procesando algunas de las cargas
transaccionales más altas del mundo** —miles de millones de transacciones al día en bancos grandes—
porque **cuando el patrón de acceso se conoce de antemano, una jerarquía optimizada es imbatible**.

Y lo relacional ganó por lo que la clase 164 llamaría la razón correcta: **no por rendimiento, sino
porque permite preguntar cosas que nadie previó** — y eso resultó valer más.

Y merece señalar el paralelismo con hoy, porque es exacto: **las bases de datos de clave y valor y las
documentales son jerárquicas**, y su compromiso es el mismo — **rapidísimas para el acceso previsto,
incómodas para lo demás** (clase 099).

Es la misma decisión, redescubierta cuarenta años después, y con las mismas consecuencias: **el modelo de
datos se elige por los patrones de acceso, y cambiarlo después cuesta**.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
DATOS ; Componente de datos -- clase 170
 read linea
 new i, total, n
 set total = 0
 for i = 1:1:$length(linea, " ") do
 . set n = $piece(linea, " ", i)
 . if n '= "" set total = total + n
 write "total=", total, !
 quit
```

**M y el componente de datos.** Aquí está la primera mitad del gancho, y merece desarrollarla porque es la
propiedad más valiosa de M: **no hay desajuste de impedancia, porque no hay dos modelos**.

```mumps
 set ^PEDIDO(4711, "CLIENTE") = "ACME"
 set total = 0
 set art = ""
 for  set art = $order(^PEDIDO(4711, "LINEA", art)) quit:art=""  do
 . set total = total + $piece(^PEDIDO(4711, "LINEA", art), "^", 2)
```

**Ahí no hay consulta, ni conexión, ni conversión de tipos, ni mapeador**: **la variable persistente es la
estructura de datos** (clase 099).

Y merece enumerar lo que eso ahorra, porque es todo lo que las demás columnas de esta página gestionan:

```text
Sin: cadena de conexión, conjunto de conexiones, SQL, parámetros,
     conversión de tipos, mapeo objeto-relacional, problema N+1,
     ni diferencia entre "el objeto" y "la fila".
```

**Y el coste es el que la clase 099 explicó**: **no hay consultas ad hoc**. Para responder "cuántos
pedidos hay por zona" **hay que tener un índice que lo permita, o recorrerlo todo**.

Es exactamente el compromiso de IMS en esta página, y el mismo de las bases de clave y valor modernas.

Y por eso los sistemas M serios tienen **una capa de índices explícita**, mantenida por el programa:

```mumps
 ; al guardar, se actualizan los índices
 set ^PEDIDO(id, "ZONA") = zona
 set ^PEDIDOX("ZONA", zona, id) = ""      ; índice secundario
```

**Y ahí está el riesgo del cierre de esta clase**: **si alguien escribe sin actualizar el índice, el
índice miente** — y no hay motor que lo impida.

**FileMan resuelve eso** (clase 149): **escribir por su API mantiene los índices automáticamente**, y por
eso el estándar de VistA prohíbe escribir directamente en las globals de otro paquete (clase 166).

Y merece cerrar con lo que las implementaciones modernas han añadido y que cambia el cuadro: **SQL sobre
las mismas globals**.

```sql
-- InterSystems IRIS y YottaDB Octo: SQL sobre datos M
SELECT SUM(importe) FROM Pedidos WHERE zona = 'NORTE'
```

**Y con eso se tienen las dos cosas**: el acceso directo sin impedancia para lo que el programa hace todos
los días, y SQL para las preguntas que nadie previó — que es, exactamente, lo que este componente
necesita.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| linea total |

linea := stdin nextLine trimBoth.
total := 0.

(linea substrings: ' ') do: [ :p | total := total + p asNumber ].

Transcript show: 'total=', total printString; cr.
```

**Smalltalk y el componente de datos.** Y aquí está la segunda mitad del gancho, y merece contarla porque
es una tecnología notable y poco conocida: **GemStone/S**.

```smalltalk
"Un objeto persistente NO se guarda: simplemente se referencia desde el árbol raíz"
System myUserProfile symbolList at: #Pedidos put: (Set new).
Pedidos add: unPedido.
System commitTransaction.
```

**No hay mapeo, ni consultas, ni serialización**: **los objetos viven en un repositorio compartido y
transaccional**, y **varias máquinas virtuales trabajan sobre él a la vez** (clase 161).

Y las propiedades merecen enumerarse porque son las de una base de datos de verdad:

| Propiedad | Detalle |
|---|---|
| **Transacciones ACID** | con detección de conflictos y reintento |
| **Objetos compartidos entre procesos y máquinas** | el repositorio es el estado |
| **Índices sobre colecciones** | consultas rápidas sin SQL |
| **Y el mismo lenguaje** | el código de negocio corre **dentro** del repositorio |

**La última es la más interesante y conecta con Lisp en esta página**: **la lógica se ejecuta donde están
los datos**, sin viaje de red — que es la regla del cierre de esta clase llevada al extremo.

Y GemStone lleva en producción desde los años noventa en sistemas financieros, con volúmenes serios.

Y merece añadir la observación general que este componente permite hacer al cerrar la clase: **el
desajuste de impedancia no es una ley de la naturaleza — es la consecuencia de que el lenguaje y la base
de datos evolucionaran por separado**.

```text
Los que NO lo tienen:
  M          → la variable es la base de datos
  GemStone    → el objeto es persistente
  SQLite en proceso  → la frontera casi no existe
  Y los lenguajes con consultas integradas y comprobadas (LINQ, sqlpp11, GNATCOLL)
     → el desajuste sigue, pero al menos el compilador lo vigila
```

**Y el resto del mundo lo tapa con mapeadores objeto-relacionales**, que funcionan bien hasta que
esconden un problema N+1 o generan una consulta que nadie entiende.

Es la lección práctica de esta clase, y la más útil para el proyecto de esta parte: **el mapeador es una
comodidad, no una abstracción**. Conviene saber siempre qué SQL se está ejecutando — y las herramientas
que lo enseñan valen más que las que lo esconden.

---

## Y de vuelta a la clase

Lo transferible: **la regla que más rendimiento gana en un sistema con base de datos es pedir por
conjuntos, no por filas**. Un bucle que hace mil consultas cuesta mil viajes; una consulta que devuelve
mil filas cuesta uno — y es la misma diferencia dos órdenes de magnitud (clase 152). De ahí las dos
prácticas: **dejar que la base haga lo que sabe hacer** —filtrar, agregar, ordenar, unir— **en lugar de
traérselo todo y hacerlo en el lenguaje**; y **nunca construir SQL concatenando** (clase 153), que es la
misma regla vista desde la seguridad.

⏮️ [Volver a la clase 170](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
