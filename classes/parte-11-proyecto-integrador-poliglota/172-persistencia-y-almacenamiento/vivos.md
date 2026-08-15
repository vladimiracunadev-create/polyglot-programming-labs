# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 172

> [⬅️ Volver a la clase 172](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Guardar un par nombre-valor: `guardado=x=5`. Es la operación más simple de persistir, y esta clase trata
de lo que hay detrás de esa palabra: **que el dato siga ahí después**. Y "después" incluye un corte de
luz a mitad de la escritura, que es donde casi todos los sistemas descubren que no habían pensado en
ello. Y aquí hay una respuesta que merece el titular: **el diario, la técnica que hace posible sobrevivir
a eso, es de los años setenta y viene de estos sistemas**.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es la **durabilidad**, y estos lenguajes la enseñan porque **operan sistemas donde
> perder datos no es una opción**: bancos, hospitales, seguros. Y de ahí salieron las técnicas que hoy usan
> todas las bases de datos: **el registro de escritura anticipada, los puntos de control, la confirmación
> en dos fases y el diario de imágenes anterior y posterior** (clase 140).
>
> Y aparece la pregunta que casi nadie se hace hasta que es tarde: **¿qué pasa si el proceso muere entre
> estas dos líneas?**
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: una línea `clave valor` → stdout: `guardado=<clave>=<valor>`
- **Regla:** `almacenar el par y confirmar`

| stdin | esperado |
|---|---|
| `x 5` | `guardado=x=5` |
| `nombre ada` | `guardado=nombre=ada` |
| `n 100` | `guardado=n=100` |

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
PROGRAM-ID. GUARDAR.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(60).
01  C-NOM   PIC X(20).
01  C-VAL   PIC X(20).

PROCEDURE DIVISION.
    ACCEPT LINEA
    UNSTRING LINEA DELIMITED BY ALL SPACES
        INTO C-NOM C-VAL
    END-UNSTRING

    DISPLAY "guardado=" FUNCTION TRIM(C-NOM)
            "=" FUNCTION TRIM(C-VAL)
    STOP RUN.
```

**COBOL y la persistencia.** COBOL tiene el catálogo de organizaciones de fichero más completo del
lenguaje, y merece verlo porque cada una responde a un patrón de acceso (clase 170):

```cobol
       SELECT CLIENTES ASSIGN TO "CLIENTES"
           ORGANIZATION IS INDEXED           *> VSAM KSDS: acceso por clave
           ACCESS MODE IS DYNAMIC             *> secuencial Y aleatorio
           RECORD KEY IS CLI-ID
           ALTERNATE RECORD KEY IS CLI-NIF WITH DUPLICATES
           FILE STATUS IS WS-ESTADO.
```

| Organización | Acceso | Uso |
|---|---|---|
| **SEQUENTIAL** | de principio a fin | lote (clase 152) |
| **RELATIVE** | por número de registro | acceso directo por posición |
| **INDEXED** (VSAM KSDS) | **por clave, con índices alternativos** | maestro de datos |
| **LINE SEQUENTIAL** | texto con saltos de línea | intercambio |

**`ALTERNATE RECORD KEY` merece la mención**: **VSAM mantiene índices secundarios automáticamente** —lo
que M tiene que hacer a mano (clase 170)— y es de 1973.

Y la durabilidad, que es el tema del cierre:

```cobol
           EXEC CICS SYNCPOINT END-EXEC          *> confirmar
           EXEC CICS SYNCPOINT ROLLBACK END-EXEC  *> o deshacer
```

**Y debajo está la técnica del gancho**: **el registro de escritura anticipada**.

```text
Antes de modificar un dato, el sistema escribe en un REGISTRO SECUENCIAL
lo que va a hacer, y se asegura de que ESE registro está en disco.
Solo entonces modifica el dato.

Si el sistema cae, al arrancar recorre el registro:
  - lo confirmado y no aplicado, se aplica
  - lo no confirmado, se deshace
```

**Ese algoritmo —conocido como ARIES, formalizado por IBM en 1992— es la base de la recuperación de
prácticamente todas las bases de datos actuales**: DB2, Oracle, SQL Server, PostgreSQL y SQLite.

Y su idea central es la primera regla del cierre generalizada: **escribir la intención antes que el
cambio**, porque **un registro secuencial se puede escribir de forma atómica y una modificación en su
sitio, no**.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program guardar
   implicit none
   character(len=60) :: linea
   character(len=20) :: nombre, valor
   integer :: p1

   read(*, '(A)') linea
   linea = adjustl(linea)

   p1 = index(linea, ' ')
   nombre = linea(1:p1-1)
   valor  = adjustl(linea(p1+1:))

   write(*, '(A)') 'guardado=' // trim(nombre) // '=' // trim(valor)
end program guardar
```

**Fortran y la persistencia.** El cálculo científico tiene un problema de durabilidad propio y muy
concreto: **escribir terabytes desde miles de procesos a la vez**.

```fortran
! Cada proceso escribe su trozo del mismo fichero, en paralelo
call MPI_File_open(MPI_COMM_WORLD, 'salida.dat', MPI_MODE_CREATE + MPI_MODE_WRONLY, &
                   MPI_INFO_NULL, fh)
call MPI_File_write_at_all(fh, desplazamiento, datos, n, MPI_DOUBLE_PRECISION, estado)
call MPI_File_close(fh)
```

**MPI-IO coordina la escritura de miles de procesos sobre un sistema de ficheros paralelo** —Lustre,
GPFS— y **agrupa las escrituras pequeñas en grandes**, que es lo único que hace viable ese caudal.

Y la técnica de durabilidad de este dominio es la de la clase 171: **los puntos de control**.

```fortran
! Cada N pasos: escribir el estado completo, y hacerlo BIEN
write(nombre, '(A,I6.6,A)') 'ckpt_', paso, '.h5.tmp'
call escribir_estado(nombre)
call flush_y_sincronizar(nombre)
call rename(nombre, 'ckpt_ultimo.h5')     ! ← temporal y renombrado (cierre, regla 1)
```

**Y el renombrado al final es lo que evita el desastre clásico**: **caer mientras se escribe el punto de
control y quedarse sin el nuevo y sin el viejo**.

Y merece nombrar la técnica que este dominio ha desarrollado para el mismo problema a otra escala: **los
puntos de control multinivel**.

```text
Nivel 1: en memoria local o en el nodo vecino    → rapidísimo, sobrevive a fallo de proceso
Nivel 2: en el disco local del nodo                → sobrevive a fallo de nodo
Nivel 3: en el sistema de ficheros paralelo         → sobrevive a todo, y es lento
```

**Se escribe el nivel 1 a menudo y el nivel 3 pocas veces**, porque **la mayoría de los fallos son
locales**.

Es la misma jerarquía que las réplicas de una base de datos —memoria, disco local, otro centro— y la misma
lógica: **la durabilidad se paga en latencia, y conviene comprar solo la que hace falta**.

Es la regla del cierre matizada con datos: **`fsync` cuesta, y saber cuánta durabilidad se necesita en
cada punto es una decisión de ingeniería, no un absoluto**.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO; use Ada.Text_IO;
with Ada.Strings;
with Ada.Strings.Fixed;

procedure Guardar is
   Linea  : String (1 .. 60);
   Ultimo : Natural;
   Sep    : Natural;
begin
   Get_Line (Linea, Ultimo);
   Sep := Ada.Strings.Fixed.Index (Linea (1 .. Ultimo), " ");

   Put_Line ("guardado=" & Linea (1 .. Sep - 1) & "=" &
             Ada.Strings.Fixed.Trim (Linea (Sep + 1 .. Ultimo), Ada.Strings.Both));
end Guardar;
```

**Ada y la persistencia.** Ada tiene entrada y salida con tipos en el estándar, y su diseño merece
señalarse porque es distinto del habitual:

```ada
with Ada.Sequential_IO;
with Ada.Direct_IO;
with Ada.Streams.Stream_IO;

package Registro_IO is new Ada.Direct_IO (Registro);   --  ¡genérico sobre EL TIPO!

F : Registro_IO.File_Type;
Registro_IO.Open (F, Registro_IO.Inout_File, "datos.bin");
Registro_IO.Read (F, R, Positive_Count (Indice));       --  acceso directo por índice
```

**`Direct_IO` se instancia con el tipo del registro**, así que **el fichero es de registros de ese tipo y
solo de ese tipo** — el compilador impide leer una cosa donde se guardó otra.

Es una comprobación que casi ningún lenguaje de esta página hace sobre ficheros binarios, y evita el fallo
de la clase 106.

Y el dominio de Ada trae un requisito de persistencia que merece contarse porque es extremo: **la memoria
no volátil en sistemas embarcados**.

```ada
type Parametros is record ... end record;
for Parametros'Alignment use 4;

--  Escritura en EEPROM o FRAM, con verificación
procedure Guardar_Parametros (P : Parametros) is
   Copia : Parametros := P;
begin
   Copia.Suma := Calcular_Suma (P);       --  ← suma de comprobación EN el registro
   Escribir_Fisico (Copia);
   if Leer_Fisico /= Copia then           --  ← releer y comparar
      raise Error_Escritura;
   end if;
end Guardar_Parametros;
```

**Y las dos técnicas de ahí son la respuesta de este dominio al gancho de esta clase**:

**La suma de comprobación dentro del registro** permite detectar una escritura interrumpida al leerlo.

**Y releer y comparar** confirma que el medio aceptó el dato — porque **en una memoria con celdas
desgastadas, la escritura puede fallar en silencio**.

Y la variante completa, para cuando no se puede perder nada: **dos copias alternadas**.

```text
Se escribe siempre en la copia que NO está en uso, con su contador y su suma.
Al arrancar, se leen las dos y se usa la más reciente que sea VÁLIDA.
```

**Y así, un corte de luz a mitad de escritura deja intacta la copia anterior** — que es la primera regla
del cierre de esta clase, implementada sin sistema de ficheros.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Guardar;
{$MODE OBJFPC}{$H+}
uses SysUtils, StrUtils;

var
  Linea, Nombre, Valor: string;
  P: Integer;

begin
  ReadLn(Linea);
  Linea := Trim(Linea);

  P := Pos(' ', Linea);
  Nombre := Copy(Linea, 1, P - 1);
  Valor  := Trim(Copy(Linea, P + 1, Length(Linea)));

  WriteLn('guardado=', Nombre, '=', Valor);
end.
```

**Pascal y la persistencia.** Pascal tiene un tipo que merece destacarse porque es una idea de 1970 muy
buena y poco imitada: **el fichero tipado**.

```pascal
type
  TRegistro = record
    Id: Integer;
    Nombre: string[50];        { cadena corta: tamaño FIJO, apta para fichero }
    Saldo: Currency;
  end;

var
  F: file of TRegistro;         { ← un fichero DE ESE TIPO }
  R: TRegistro;

begin
  Assign(F, 'datos.dat');
  Reset(F);
  Seek(F, 10);                  { al registro 10 }
  Read(F, R);
  R.Saldo := R.Saldo + 100;
  Seek(F, 10);
  Write(F, R);
  Close(F);
end;
```

**`file of TRegistro` es acceso directo por número de registro, con el tipo comprobado** —lo mismo que
`Direct_IO` de Ada en esta página— y **es de Pascal original**.

Y la advertencia que hay que dar y que la clase 157 explica: **`file of` guarda la representación en
memoria del registro**, así que **el fichero depende de la alineación, del tamaño de los tipos y del orden
de bytes**.

```pascal
{$PACKRECORDS 1}     { sin relleno: el fichero es portable... si todos usan esto }
```

**Un fichero escrito por la versión de 32 bits puede no leerse con la de 64** — que es exactamente el
problema de la migración de la clase 150.

Y sobre durabilidad, el ecosistema Pascal da lo necesario y merece verlo junto porque es la receta
completa del cierre:

```pascal
{ 1. escribir a un temporal }
AssignFile(F, Destino + '.tmp');
Rewrite(F);
...
{ 2. vaciar y sincronizar }
Flush(F);
FileFlush(TFileRec(F).Handle);        { fsync }
CloseFile(F);
{ 3. y renombrar, que es atómico }
RenameFile(Destino + '.tmp', Destino);
```

**Los tres pasos, en ese orden**, y merece subrayar el segundo porque es el que casi siempre falta:
**`Flush` vacía el búfer de la biblioteca al sistema operativo; `FileFlush` obliga al sistema operativo a
llevarlo al disco**.

**Son dos búferes distintos, y solo el segundo sobrevive a un corte de luz.**

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let* ((linea (read-line))
       (sep (position #\Space linea))
       (nombre (subseq linea 0 sep))
       (valor (string-trim '(#\Space #\Return) (subseq linea (1+ sep)))))
  (format t "guardado=~A=~A~%" nombre valor))
```

**Lisp y la persistencia.** Lisp tiene la persistencia más cómoda de esta página y una de las más
peligrosas, y merece ver las dos caras.

**La cómoda, que la clase 159 explicó:**

```lisp
(with-open-file (f "estado.lisp" :direction :output :if-exists :supersede)
  (let ((*print-readably* t) (*print-circle* t))
    (print *estado* f)))

(with-open-file (f "estado.lisp") (read f))
```

**Guardar y cargar una estructura arbitraria son dos líneas** — y `*print-circle*` maneja las referencias
compartidas y los ciclos.

**Y la peligrosa es la del cierre de esta clase**, porque ese código tiene un fallo que casi nadie ve:

```lisp
:if-exists :supersede
```

**`:supersede` trunca el fichero al abrirlo.** Así que **si el proceso muere a mitad de la escritura, el
fichero anterior ya no existe y el nuevo está incompleto** — se pierden las dos versiones.

Y la forma correcta es la primera regla del cierre:

```lisp
(let ((temp (merge-pathnames "estado.tmp" destino)))
  (with-open-file (f temp :direction :output :if-exists :supersede)
    (print *estado* f)
    (finish-output f))                       ; ← vaciar
  (rename-file temp destino))                 ; ← atómico
```

**`finish-output` antes de renombrar** es imprescindible: **sin él, el renombrado puede ocurrir antes de
que los datos lleguen al fichero**.

Y Lisp tiene una forma de persistencia que ningún otro de esta página comparte y que la clase 144
explicó: **la imagen**.

```lisp
(sb-ext:save-lisp-and-die "estado.core")
```

**Guardar el sistema entero, con todos sus objetos vivos** — que es persistencia total y sin código de
serialización.

**Y su límite hay que decirlo**: **no es incremental ni transaccional**. Guardar una imagen de 200 MB para
persistir un cambio pequeño no es una opción, y **si el proceso muere entre dos guardados, se pierde
todo lo intermedio**.

Es un buen ejemplo de la tercera regla del cierre: **para persistencia con garantías, una base de datos**.
La imagen es excelente para arrancar rápido y para congelar un estado conocido, no para ser el almacén.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea
lassign [string trim $linea] nombre valor

puts "guardado=$nombre=$valor"
```

**Tcl y la persistencia.** Tcl tiene la escritura de ficheros integrada en su modelo de canales (clase
161), y esta clase es el sitio para las opciones que deciden la durabilidad:

```tcl
set f [open "datos.txt.tmp" w]
fconfigure $f -encoding utf-8 -translation lf -buffering full
puts $f $contenido
flush $f                      ;# ← vacía el búfer de Tcl al sistema operativo
close $f
file rename -force "datos.txt.tmp" "datos.txt"    ;# ← atómico
```

**Y merece explicar la diferencia entre `flush` y `close`**, porque es la que produce corrupciones:
**`close` vacía y cierra, pero ninguno de los dos garantiza que el dato esté en el disco físico** — para
eso hace falta `fsync`, que Tcl expone en versiones recientes o vía TclX.

Es la segunda regla del cierre, y **Tcl la deja explícita** en lugar de esconderla.

Y merece señalar `-translation lf`, porque es la trampa de la clase 145: **por defecto, Tcl traduce los
fines de línea según la plataforma**, así que **un fichero escrito en Windows y leído en Linux puede
diferir** — y para datos binarios hay que poner `-translation binary`.

Y Tcl trae dos almacenes en la distribución que merecen conocerse:

| Almacén | Notas |
|---|---|
| **`array set` / `array get`** | serializar un arreglo asociativo a una lista y volver |
| **Metakit / VFS** | el sistema de ficheros virtual de los Starkits (clase 144) |
| **`tdbc::sqlite3`** | **SQLite, con transacciones de verdad** |

**Y la tercera es la aplicación directa de la tercera regla del cierre**: cuando hace falta que un
conjunto de cambios sea todo o nada, **la respuesta es SQLite y no un fichero propio**.

```tcl
db transaction {
    db allrows {UPDATE cuentas SET saldo = saldo - :importe WHERE id = :origen}
    db allrows {UPDATE cuentas SET saldo = saldo + :importe WHERE id = :destino}
}
```

**Esas dos actualizaciones ocurren las dos o ninguna**, y sobrevive a un corte de luz — porque SQLite
implementa el registro de escritura anticipada de la explicación de COBOL en esta página.

**Reimplementar eso a mano es la forma más eficaz de perder datos**, y es lo que la tercera regla del
cierre quiere evitar.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;
my ($nombre, $valor) = split ' ', $linea;

print "guardado=$nombre=$valor\n";
```

**Perl y la persistencia.** Perl tiene todo el arsenal de esta clase, y esta es la ocasión para la receta
completa, que es la del cierre:

```perl
use Path::Tiny;
use Fcntl qw(:flock O_WRONLY O_CREAT O_EXCL);

# 1. temporal + fsync + renombrado, en una llamada
path("datos.json")->spew_utf8($json);        # Path::Tiny ya hace temporal y renombrado

# 2. o a mano, con control:
open(my $fh, '>', "$destino.tmp") or die $!;
print $fh $contenido;
$fh->flush;                                   # búfer de Perl → sistema operativo
$fh->sync;                                     # → disco   (IO::Handle)
close $fh;
rename("$destino.tmp", $destino) or die $!;    # atómico
```

**Y la línea `$fh->sync` es la del cierre**: sin ella, **el renombrado puede completarse y el contenido
no estar**, lo que deja un fichero de tamaño cero — un fallo real y muy desconcertante.

Y Perl aporta a esta clase el mecanismo de exclusión que una automatización necesita (clase 171):

```perl
open(my $lock, '>', "/var/run/miapp.lock") or die;
flock($lock, LOCK_EX | LOCK_NB) or die "ya hay otra instancia\n";
```

**`flock` con `LOCK_NB` es la forma correcta de impedir dos ejecuciones simultáneas** — y merece la
advertencia: **es consultivo** (clase 161), y **no funciona bien en sistemas de ficheros de red**.

Y los almacenes del ecosistema, ordenados por lo que garantizan:

| Almacén | Durabilidad |
|---|---|
| **Fichero de texto o JSON** | lo que el programa haga |
| **`Storable`** | binario propio de Perl (clase 159) |
| **`DB_File` / `BerkeleyDB`** | clave-valor con transacciones opcionales |
| **`DBD::SQLite`** | **ACID completo** |
| **PostgreSQL, MySQL** | ACID, con réplicas |

**Y la lección del cierre está en el salto entre la primera y la cuarta**: **entre "escribir un fichero" y
"garantizar que un conjunto de cambios es atómico y durable" hay cuarenta años de ingeniería**, y no se
recorren en una tarde.

Es la razón por la que SQLite está en todos los teléfonos: **es la forma más barata de tener esa
garantía**.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>
#include <string>

int main() {
    std::string nombre, valor;
    if (!(std::cin >> nombre >> valor)) return 1;

    std::cout << "guardado=" << nombre << '=' << valor << '\n';
    return 0;
}
```

**C++ y la persistencia.** C++ es donde se implementan los almacenes de esta página, y esta clase es el
sitio para los detalles que hay que acertar y que casi nadie conoce.

**Los tres búferes del cierre, con sus llamadas:**

```cpp
std::ofstream f("datos.tmp");
f << contenido;
f.flush();                              // 1. búfer de la biblioteca → sistema operativo
// pero eso NO basta:
int fd = ::open("datos.tmp", O_WRONLY);
::fsync(fd);                             // 2. sistema operativo → disco
::close(fd);
::rename("datos.tmp", "datos");           // 3. renombrado atómico
// ¡y falta uno!
int dir = ::open(".", O_RDONLY);
::fsync(dir);                              // 4. ← ¡sincronizar el DIRECTORIO!
::close(dir);
```

**El cuarto paso merece la explicación porque es el que casi todo el mundo olvida**: **el renombrado
modifica el directorio, y esa modificación también está en un búfer**.

Sin `fsync` del directorio, **puede ocurrir que el fichero exista con su contenido y que la entrada de
directorio se pierda** — el fichero desaparece.

**Es un fallo real, documentado, y es la razón por la que las bases de datos serias sincronizan el
directorio.**

Y hay más detalles que merecen conocerse porque han causado pérdidas de datos famosas:

| Detalle | Consecuencia |
|---|---|
| **`fsync` puede fallar y no se puede reintentar** | en Linux, un `fsync` fallido marca las páginas como limpias: **el dato se pierde y el segundo `fsync` dice que todo bien** |
| **`write` puede escribir menos bytes de los pedidos** | hay que comprobar el valor devuelto y repetir |
| **La caché del disco puede mentir** | discos baratos que confirman antes de escribir |
| **`O_DIRECT` salta la caché del sistema** | lo usan las bases de datos, con alineación estricta |

**La primera fila es el llamado "fsyncgate" de 2018**, que obligó a PostgreSQL a cambiar su estrategia de
recuperación: **si `fsync` falla, la única respuesta segura es abortar el proceso**.

Y todo esto es exactamente la tercera regla del cierre de esta clase: **la lista de cosas que hay que
acertar para tener durabilidad es larga, poco conocida y llena de detalles del sistema operativo**.

**Y por eso la recomendación no es aprenderlos todos: es usar una base de datos que ya los haya
acertado.**

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

dcl-pi GUARDAR;
  linea char(60) const;
end-pi;

dcl-s texto  varchar(60);
dcl-s pos    int(10);
dcl-s nombre varchar(20);
dcl-s valor  varchar(20);

texto = %trim(linea);
pos = %scan(' ' : texto);

nombre = %subst(texto : 1 : pos - 1);
valor  = %trim(%subst(texto : pos + 1));

dsply ('guardado=' + nombre + '=' + valor);

*inlr = *on;
return;
```

**RPG y la persistencia.** IBM i tiene la persistencia integrada en el sistema, y esta clase es el sitio
para la pieza que la hace segura y que la clase 140 ya nombró: **el diario**.

```text
STRJRNPF FILE(CLIENTES) JRN(MIJRN) IMAGES(*BOTH)
```

**Y con eso, cada cambio de cada fila queda registrado** con la imagen anterior y la posterior, el
trabajo, el usuario, el programa y la marca de tiempo.

Y merece enumerar lo que eso da, porque es más de lo que parece:

| Capacidad | Cómo |
|---|---|
| **Recuperación tras caída** | se aplican los cambios confirmados del diario |
| **Control de compromiso** | transacciones sobre varios ficheros |
| **`RMVJRNCHG`** | **deshacer los cambios hasta un instante** (clase 148) |
| **Replicación** | el diario se envía a otra máquina: alta disponibilidad |
| **Auditoría** | quién cambió qué y cuándo (clase 142) |
| **Y captura de cambios** | alimentar un almacén analítico |

**La cuarta fila merece destacarse** porque es la base de las soluciones de alta disponibilidad de esta
plataforma: **enviar el diario a un sistema de respaldo que lo aplica** — que es exactamente la
replicación por registro de escritura anticipada de PostgreSQL y de MySQL, y es de los años noventa.

Y el control de compromiso, que es la parte de transacciones:

```rpgle
exec sql SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
...
exec sql COMMIT;      // o ROLLBACK
```

**O con el acceso nativo, `COMMIT` y `ROLLBACK` como operaciones de RPG** sobre ficheros con diario.

Y merece cerrar con la observación que esta plataforma permite y que conecta con el cierre de esta clase:
**aquí la durabilidad no es una decisión del programa, es una propiedad del objeto**.

**Se activa el diario sobre una tabla con un comando, y a partir de ahí todos los programas que la usen
están cubiertos** — sin cambiar ni una línea.

Es la diferencia entre una garantía que hay que implementar en cada sitio y una que se configura una vez,
y explica por qué en esta plataforma la pérdida de datos por un fallo de programación es rara.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 guardar: procedure options(main);

    declare linea  char(60) varying;
    declare nombre char(20) varying;
    declare valor  char(20) varying;
    declare p      fixed binary(31);

    get edit (linea) (a(60));
    linea = trim(linea);

    p = index(linea, ' ');
    nombre = substr(linea, 1, p - 1);
    valor = trim(substr(linea, p + 1));

    put skip list ('guardado=' || nombre || '=' || valor);

 end guardar;
```

**PL/I y la persistencia.** PL/I tiene el catálogo de organizaciones de fichero de COBOL y añade un
concepto propio que merece explicarse porque es de los pocos de esta página: **el área**.

```pli
 declare zona area(100000);
 declare p pointer;
 declare nodo based(p),
           2 valor fixed binary(31),
           2 siguiente pointer;

 allocate nodo in (zona) set (p);      /* reservar DENTRO del área */
 ...
 write file(f) from (zona);             /* ¡y GUARDAR EL ÁREA ENTERA! */
```

**Un `AREA` es un montón autocontenido con punteros relativos a su base**, así que **una estructura
enlazada construida dentro de un área se puede escribir a disco y volver a leer** — con los punteros
intactos.

Es **persistencia de estructuras con punteros**, resuelta en 1964, y merece señalar por qué es difícil:
**los punteros normales son direcciones absolutas y no sirven al recargar en otra dirección** (clase
161).

**Y la solución de PL/I —punteros relativos a un área— es la misma que hoy usan los formatos de
serialización sin copia** como FlatBuffers y Cap'n Proto (clase 159), y la misma que la memoria compartida
entre procesos necesita.

Y merece la comparación con el resto de esta página:

```text
La mayoría:  serializar → escribir → leer → deserializar
Con AREA:     escribir el bloque → leerlo → usarlo directamente
```

**Sin coste de conversión**, que es exactamente el argumento de FlatBuffers.

Y sobre durabilidad, PL/I vive en el mismo mundo de COBOL de esta página: **el registro de escritura
anticipada de DB2 e IMS, el control de compromiso y la confirmación en dos fases** (clase 161).

Y merece cerrar con la observación general que estas columnas permiten y que el cierre de esta clase
defiende: **las garantías de durabilidad que hoy se dan por supuestas en cualquier base de datos son el
resultado de cuarenta años de acertar detalles**, muchos de ellos aprendidos perdiendo datos de verdad —
y esa es la razón para no reimplementarlas.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
GUARDAR ; Persistencia -- clase 172
 read linea
 new nombre, valor
 set nombre = $piece(linea, " ", 1)
 set valor = $piece(linea, " ", 2)
 write "guardado=", nombre, "=", valor, !
 quit
```

**M y la persistencia.** M tiene la persistencia más simple de esta página, y merece verla con la lista
del cierre delante:

```mumps
 set ^CONFIG("x") = 5
```

**Esa línea está en disco, es transaccional, sobrevive al reinicio y es visible para todos los procesos**
(clase 161).

**Y no hay que abrir, ni cerrar, ni vaciar, ni sincronizar, ni serializar.**

Y merece explicar cómo se consigue, porque debajo está exactamente la técnica del gancho: **el diario**.

```text
Una escritura en una global:
  1. se escribe en el DIARIO (secuencial, rápido)
  2. y se modifica la base de datos en memoria
  3. los bloques modificados se llevan a disco después, en bloque

Si el sistema cae, al arrancar se recorre el diario y se recupera.
```

**Es el registro de escritura anticipada de COBOL en esta página**, y M lo tiene desde sus primeras
implementaciones porque su público —hospitales— no podía perder datos.

Y las transacciones:

```mumps
 tstart
 set ^CUENTA(origen) = ^CUENTA(origen) - importe
 set ^CUENTA(destino) = ^CUENTA(destino) + importe
 tcommit
```

**Todo o nada**, y **junto con cualquier otra cosa que la transacción haga** — incluida encolar un mensaje
(clase 161), que es lo que resuelve el problema de la doble escritura.

Y merece cerrar con la comparación que hace M valiosa en esta clase y que la clase 170 anticipó:

```text
En casi todos los lenguajes de esta página:
   variable en memoria  ≠  dato persistente
   y entre las dos hay una capa: ficheros, SQL, mapeador, serialización.

En M:
   ^dato  es  dato persistente
   y la única diferencia con una variable local es un carácter.
```

**Esa ausencia de capa es la propiedad más valiosa del lenguaje**, y es la razón por la que sistemas
escritos en él llevan cuarenta años sin perder datos: **hay muchísimo menos código entre el programa y el
disco, y por tanto muchos menos sitios donde equivocarse**.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| linea partes |

linea := stdin nextLine trimBoth.
partes := linea substrings: ' '.

Transcript
    show: 'guardado=', (partes at: 1), '=', (partes at: 2);
    cr.
```

**Smalltalk y la persistencia.** Smalltalk tiene tres formas de persistir, y compararlas cierra bien esta
clase porque cubren todo el espectro.

**Una, la imagen** (clase 144):

```smalltalk
Smalltalk snapshot: true andQuit: false.
```

**Guarda todos los objetos vivos.** Total, y ni incremental ni transaccional — el mismo límite que la
imagen de Lisp en esta página.

**Dos, la serialización** (clase 159):

```smalltalk
FLSerializer serialize: unGrafo toFileNamed: 'estado.fuel'.
```

**Rápida y completa**, y con la receta del cierre por delante: **temporal, sincronizar y renombrar**.

**Y tres, GemStone**, que es la que merece el espacio porque resuelve lo que las otras dos no:

```smalltalk
System beginTransaction.
cuenta saldo: cuenta saldo - importe.
otra saldo: otra saldo + importe.
System commitTransaction.        "ACID sobre el grafo de objetos"
```

**Los objetos viven en un repositorio transaccional compartido**, y **modificar un objeto es modificar la
base de datos**.

Y merece explicar lo que eso implica, porque es lo mismo que M en esta página conseguido con objetos:

```text
Sin: mapeo objeto-relacional, serialización, consultas, ni "guardar".
Con: transacciones, detección de conflictos, y objetos compartidos entre máquinas.
```

**Y la detección de conflictos merece la mención** porque es la parte difícil: **si dos procesos modifican
el mismo objeto, la confirmación del segundo falla y hay que reintentar** — que es control de concurrencia
optimista, y es lo que permite escalar sin bloqueos largos.

Y esta clase debe cerrar con la observación que las tres formas dejan clara: **el eje real de la
persistencia no es el formato, es la granularidad de la garantía**.

```text
Imagen:     todo o nada, y solo cuando alguien la guarda.
Serializar: un grafo, con la durabilidad que el programa implemente.
GemStone / base de datos: una transacción, garantizada por el sistema.
```

**Y elegir es decidir qué se puede perder**: en un editor, el trabajo desde el último guardado; en un
sistema de pagos, nada.

Es la pregunta que el gancho de esta clase planteaba —**¿qué pasa si el proceso muere entre estas dos
líneas?**— y la respuesta correcta es siempre la misma: **depende de qué haya entre ellas**.

---

## Y de vuelta a la clase

Lo transferible: **escribir no es persistir**. Entre `write` y el plato del disco hay al menos tres
búferes —el de la biblioteca, el del sistema operativo y el del propio disco— y **solo `fsync` cierra el
trato**. De ahí las tres reglas: **escribir a un temporal y renombrar**, porque el renombrado es atómico
y evita ficheros a medias; **`fsync` antes de dar algo por confirmado**, y saber que cuesta; y **no
inventar formatos de almacenamiento transaccional** — si hacen falta transacciones, se usa una base de
datos, porque los detalles que hay que acertar son muchos y llevan cuarenta años acertados.

⏮️ [Volver a la clase 172](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
