# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 097

> [⬅️ Volver a la clase 097](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Un árbol binario de búsqueda y su recorrido en orden. Aquí se separan de golpe dos mundos: los
lenguajes que **construyen el árbol con punteros** —Pascal, Ada, C++, Fortran moderno, PL/I— y los que
**no tienen punteros y lo simulan con una tabla de índices**, que es lo que hace COBOL desde 1959. Y
en medio queda M, donde **el árbol no se construye: es lo que hay**.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es la **estructura recursiva enlazada**, y estos lenguajes lo enseñan porque marcan
> cuándo se volvió escribible. **PL/I (1964) fue el primer lenguaje de alto nivel con punteros y reserva
> dinámica** listos para esto, antes que C. **Pascal (1970) lo convirtió en material didáctico** con la
> notación `^`, y el libro de Wirth enseñó árboles a una generación entera.
>
> **COBOL y RPG no tienen punteros idiomáticos**, y su respuesta —índices dentro de una tabla— no es una
> carencia: es la representación correcta cuando la estructura tiene que **caber en un registro de
> fichero**.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: una línea con enteros distintos separados por espacio → stdout: `inorden=<los valores ordenados ascendente unidos por ->`
- **Regla:** `in-order de un BST = orden ascendente`

| stdin | esperado |
|---|---|
| `3 1 4` | `inorden=1-3-4` |
| `5 2 8 1` | `inorden=1-2-5-8` |
| `9 7` | `inorden=7-9` |

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
PROGRAM-ID. ARBOL.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(200).
01  TOKEN   PIC X(20).
01  TLEN    PIC 9(2) COMP VALUE 0.
01  I       PIC 9(4) COMP.
01  L       PIC 9(4) COMP.
01  VALOR   PIC S9(9) COMP-3.
01  RAIZ    PIC 9(4) COMP VALUE 0.
01  NN      PIC 9(4) COMP VALUE 0.
01  ACT     PIC 9(4) COMP.
01  TOPE    PIC 9(4) COMP VALUE 0.
01  COLOCADO PIC 9 COMP VALUE 0.
01  ARBOL.
    05  NODO OCCURS 100 TIMES.
        10  VAL  PIC S9(9) COMP-3.
        10  IZQ  PIC 9(4) COMP.
        10  DER  PIC 9(4) COMP.
01  PILA.
    05  MARCO PIC 9(4) COMP OCCURS 100 TIMES.
01  SALIDA  PIC X(200) VALUE SPACES.
01  SPOS    PIC 9(4) COMP VALUE 1.
01  ED      PIC -(8)9.
01  TXT     PIC X(10).

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

    *> Recorrido EN ORDEN con pila explícita: COBOL no recurre por defecto
    MOVE RAIZ TO ACT
    MOVE 0 TO TOPE
    PERFORM UNTIL ACT = 0 AND TOPE = 0
        PERFORM UNTIL ACT = 0
            ADD 1 TO TOPE
            MOVE ACT TO MARCO(TOPE)
            MOVE IZQ(ACT) TO ACT
        END-PERFORM
        MOVE MARCO(TOPE) TO ACT
        SUBTRACT 1 FROM TOPE
        PERFORM EMITIR
        MOVE DER(ACT) TO ACT
    END-PERFORM

    COMPUTE L = SPOS - 1
    DISPLAY "inorden=" SALIDA(1:L)
    STOP RUN.

EMITIR.
    IF SPOS > 1
        MOVE "-" TO SALIDA(SPOS:1)
        ADD 1 TO SPOS
    END-IF
    MOVE VAL(ACT) TO ED
    MOVE FUNCTION TRIM(ED) TO TXT
    MOVE 0 TO L
    INSPECT FUNCTION REVERSE(TXT) TALLYING L FOR LEADING SPACE
    COMPUTE L = 10 - L
    MOVE TXT(1:L) TO SALIDA(SPOS:L)
    ADD L TO SPOS.

NUEVO-NODO.
    ADD 1 TO NN
    MOVE VALOR TO VAL(NN)
    MOVE 0 TO IZQ(NN)
    MOVE 0 TO DER(NN).

CERRAR-TOKEN.
    IF TLEN > 0
        COMPUTE VALOR = FUNCTION NUMVAL(TOKEN)
        IF RAIZ = 0
            PERFORM NUEVO-NODO
            MOVE NN TO RAIZ
        ELSE
            MOVE RAIZ TO ACT
            MOVE 0 TO COLOCADO
            PERFORM UNTIL COLOCADO = 1
                IF VALOR < VAL(ACT)
                    IF IZQ(ACT) = 0
                        PERFORM NUEVO-NODO
                        MOVE NN TO IZQ(ACT)
                        MOVE 1 TO COLOCADO
                    ELSE
                        MOVE IZQ(ACT) TO ACT
                    END-IF
                ELSE
                    IF DER(ACT) = 0
                        PERFORM NUEVO-NODO
                        MOVE NN TO DER(ACT)
                        MOVE 1 TO COLOCADO
                    ELSE
                        MOVE DER(ACT) TO ACT
                    END-IF
                END-IF
            END-PERFORM
        END-IF
        MOVE SPACES TO TOKEN
        MOVE 0 TO TLEN
    END-IF.
```

**Lo que esta clase enseña en COBOL.** Este programa es el más largo de la parte, y lo es por dos
motivos que definen a COBOL.

**Primero: no hay punteros.** Los "enlaces" son **números de fila dentro de una tabla**, con el 0
como marca de nulo:

```cobol
05  NODO OCCURS 100 TIMES.
    10  VAL  PIC S9(9) COMP-3.
    10  IZQ  PIC 9(4) COMP.      *> índice, no dirección
    10  DER  PIC 9(4) COMP.
```

Y esto, que parece un apaño, **es la representación correcta en su contexto**: la tabla entera es un
bloque contiguo de bytes, así que se puede escribir en un fichero de un solo golpe, leer de vuelta y
seguir funcionando. Con punteros, no. Es la idea del cierre de esta clase, y COBOL la aplica desde el
principio porque no tenía otra opción.

**Segundo: el recorrido usa una pila explícita** porque un programa COBOL **no es recursivo por
defecto**. Sus variables son estáticas —una sola copia por programa (clase 082)— así que una llamada
recursiva pisaría su propio estado.

COBOL-2002 lo permite declarándolo:

```cobol
IDENTIFICATION DIVISION.
PROGRAM-ID. RECORRE RECURSIVE.
LOCAL-STORAGE SECTION.        *> una copia POR LLAMADA
01  ACTUAL  PIC 9(4) COMP.
```

`RECURSIVE` en el `PROGRAM-ID` y **`LOCAL-STORAGE`** en lugar de `WORKING-STORAGE`: esa sección se
reserva en cada entrada y se libera al salir, que es exactamente el marco de pila de los demás
lenguajes. Existe desde 2002 y sigue siendo poco frecuente en producción.

Y hay una razón práctica para no usarla en muchos entornos: en sistemas transaccionales con miles de
tareas concurrentes, **una pila de tamaño impredecible es un riesgo operativo**. Es el mismo argumento
que en aviónica (clase 090), en otro sector.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
module arbolm
   implicit none

   type :: nodo
      integer :: valor
      type(nodo), pointer :: izq => null()
      type(nodo), pointer :: der => null()
   end type nodo

contains

   recursive subroutine insertar(p, x)
      type(nodo), pointer :: p
      integer, intent(in) :: x
      if (.not. associated(p)) then
         allocate(p)
         p%valor = x
         p%izq => null()
         p%der => null()
      else if (x < p%valor) then
         call insertar(p%izq, x)
      else
         call insertar(p%der, x)
      end if
   end subroutine insertar

   recursive subroutine inorden(p, salida)
      type(nodo), pointer :: p
      character(len=*), intent(inout) :: salida
      character(len=20) :: buf
      if (.not. associated(p)) return
      call inorden(p%izq, salida)
      write(buf, '(I0)') p%valor
      if (len_trim(salida) == 0) then
         salida = trim(buf)
      else
         salida = trim(salida) // '-' // trim(buf)
      end if
      call inorden(p%der, salida)
   end subroutine inorden

end module arbolm


program arbol
   use arbolm
   implicit none

   type(nodo), pointer :: raiz => null()
   integer :: v(100), n, ios, i
   character(len=400) :: linea, salida

   read(*, '(A)') linea

   n = 0
   do i = 1, 100
      read(linea, *, iostat=ios) v(1:i)
      if (ios /= 0) exit
      n = i
   end do

   do i = 1, n
      call insertar(raiz, v(i))
   end do

   salida = ''
   call inorden(raiz, salida)

   write(*, '(A)') 'inorden=' // trim(salida)
end program arbol
```

**Lo que esta clase enseña en Fortran.** Este programa **habría sido imposible antes de 1990**, y por
partida doble: **no había tipos derivados, no había punteros y no había recursión**. El Fortran de
mallas y matrices no tenía nada de esto.

Los **punteros de Fortran 90** son distintos de los de C, y la diferencia importa:

```fortran
type(nodo), pointer :: p
p => otro          !  ASOCIACIÓN de puntero: la flecha
p = otro           !  ASIGNACIÓN de valor: copia lo apuntado
associated(p)      !  ¿apunta a algo?
nullify(p)         !  desasociar
```

**`=>` asocia y `=` copia**, y confundirlos es el error más común de quien viene de C. Además, un
puntero de Fortran **no es una dirección con aritmética**: no se puede sumar, no se puede convertir a
entero y no puede apuntar a cualquier cosa — solo a objetos declarados con el atributo `target` o
reservados con `allocate`.

Esa restricción es deliberada y es lo que permite al compilador seguir optimizando agresivamente. La
aritmética de punteros de C es justamente lo que impide muchas optimizaciones de aliasing.

La palabra **`recursive`** era obligatoria hasta Fortran 2018, que invirtió el defecto. Y con ella
llegó una limitación que sorprende: **una función recursiva no podía devolver un arreglo de tamaño
variable** hasta que las funciones con resultado `allocatable` de Fortran 2003 lo resolvieron.

En la práctica, los árboles son raros en código Fortran, y no por dificultad: **los datos de la
física son densos y regulares**, y una malla se representa mejor con arreglos de índices que con
nodos enlazados. Cuando aparecen —árboles de octantes para simulación de N cuerpos, árboles k-d para
búsqueda espacial— es habitual verlos implementados **con arreglos de índices**, exactamente como en
COBOL, y por la misma razón: localidad de caché y facilidad para volcarlos a disco.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Arbol is
   type Nodo;
   type Enlace is access Nodo;

   type Nodo is record
      Valor    : Integer;
      Izq, Der : Enlace;
   end record;

   Raiz    : Enlace  := null;
   Primero : Boolean := True;

   procedure Insertar (P : in out Enlace; X : Integer) is
   begin
      if P = null then
         P := new Nodo'(Valor => X, Izq => null, Der => null);
      elsif X < P.Valor then
         Insertar (P.Izq, X);
      else
         Insertar (P.Der, X);
      end if;
   end Insertar;

   procedure Inorden (P : Enlace) is
   begin
      if P = null then
         return;
      end if;
      Inorden (P.Izq);
      if not Primero then
         Put ("-");
      end if;
      Put (P.Valor, Width => 1);
      Primero := False;
      Inorden (P.Der);
   end Inorden;

   Linea  : String (1 .. 400);
   Ultimo : Natural;
   Pos    : Integer := 1;
   Valor  : Integer;
   Fin    : Positive;
begin
   Get_Line (Linea, Ultimo);

   loop
      while Pos <= Ultimo and then Linea (Pos) = ' ' loop
         Pos := Pos + 1;
      end loop;
      exit when Pos > Ultimo;

      Get (Linea (Pos .. Ultimo), Valor, Fin);
      Insertar (Raiz, Valor);
      Pos := Fin + 1;
   end loop;

   Put ("inorden=");
   Inorden (Raiz);
   New_Line;
end Arbol;
```

**Lo que esta clase enseña en Ada.** Tres detalles de este programa son característicos del lenguaje.

**La declaración incompleta.** `type Nodo;` declara que el tipo existe antes de definirlo, para poder
declarar `Enlace` que lo referencia. Es lo mismo que la declaración adelantada de C, con sintaxis
propia.

**El agregado en el `new`.** `new Nodo'(Valor => X, Izq => null, Der => null)` reserva **e
inicializa completamente** en una expresión, con el agregado con nombres de la clase 091. **No puede
quedar un campo sin inicializar**, porque el agregado obliga a cubrirlos todos. En C++ y en C, un
campo olvidado en el constructor es basura.

**El `.` sin desreferenciar.** `P.Valor` funciona directamente sobre un acceso — Ada no tiene `->`.
La forma explícita `P.all.Valor` existe y casi nunca se escribe.

Y ahora lo importante, que es lo que Ada hace distinto: **los tipos de acceso llevan un
almacenamiento asociado**, y se puede acotar.

```ada
type Enlace is access Nodo;
for Enlace'Storage_Size use 10_000;      --  ESTE tipo tiene 10 KB y no más
```

Cuando se agota, `new` lanza `Storage_Error` — **una excepción, no un fallo indeterminado**. Y con
`pragma Restrictions (No_Implicit_Heap_Allocations)` se prohíbe la reserva no declarada en todo el
programa.

Ada no tiene recolector de basura obligatorio —el estándar lo permite y ninguna implementación seria
lo hace—, así que liberar es responsabilidad del programador, con un genérico que hay que instanciar
a propósito:

```ada
procedure Liberar is new Ada.Unchecked_Deallocation (Nodo, Enlace);
```

Fíjate en el nombre: **`Unchecked_`**. Ada obliga a escribir la palabra "no comprobada" para hacer
algo peligroso, y ese detalle de nomenclatura —igual que `Unchecked_Conversion`— es una de las
señales más claras de su filosofía: **lo inseguro se puede hacer, y se ve en el código**.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Arbol;
{$MODE OBJFPC}{$H+}
uses SysUtils;

type
  PNodo = ^TNodo;
  TNodo = record
    Valor: Integer;
    Izq, Der: PNodo;
  end;

var
  Raiz: PNodo;
  Salida, Linea, Tok: string;
  I: Integer;
  C: Char;

procedure Insertar(var P: PNodo; X: Integer);
begin
  if P = nil then
  begin
    New(P);
    P^.Valor := X;
    P^.Izq := nil;
    P^.Der := nil;
  end
  else if X < P^.Valor then
    Insertar(P^.Izq, X)
  else
    Insertar(P^.Der, X);
end;

procedure Inorden(P: PNodo);
begin
  if P = nil then Exit;
  Inorden(P^.Izq);
  if Salida <> '' then Salida := Salida + '-';
  Salida := Salida + IntToStr(P^.Valor);
  Inorden(P^.Der);
end;

begin
  ReadLn(Linea);
  Raiz := nil;
  Salida := '';
  Tok := '';

  for I := 1 to Length(Linea) + 1 do
  begin
    if I <= Length(Linea) then C := Linea[I] else C := ' ';
    if C = ' ' then
    begin
      if Tok <> '' then
      begin
        Insertar(Raiz, StrToInt(Tok));
        Tok := '';
      end;
    end
    else
      Tok := Tok + C;
  end;

  Inorden(Raiz);
  WriteLn('inorden=', Salida);
end.
```

**Lo que esta clase enseña en Pascal.** Este programa es, casi línea por línea, **el ejemplo canónico
del libro que enseñó estructuras de datos a la informática**: *Algorithms + Data Structures =
Programs*, Niklaus Wirth, 1976.

El árbol binario de búsqueda con `PNodo = ^TNodo` aparece en el capítulo 4, y de ahí pasó a los planes
de estudio de medio mundo durante veinte años. Si has aprendido árboles con dibujos de cajas y
flechas, el origen probable es ese libro.

La notación merece defenderse, porque es mejor que la de C:

```pascal
type PNodo = ^TNodo;      { "puntero a TNodo" -- se lee de izquierda a derecha }
P^.Valor                   { "el campo Valor de LO QUE APUNTA P" }
New(P);   Dispose(P);      { reservar y liberar }
```

`^` a la derecha del puntero para desreferenciar, `^` a la izquierda del tipo para declararlo. En C,
`*` hace las dos cosas y la declaración `TNodo *p` se lee al revés que su uso.

Wirth eligió `New`/`Dispose` en lugar de `malloc`/`free` porque **`New` conoce el tipo**: reserva
exactamente el tamaño de `TNodo`. En C hay que escribir `malloc(sizeof(TNodo))` y confiar en no
equivocarse — el error de reservar el tamaño equivocado es clásico.

Object Pascal moderno añade tres alternativas al puntero crudo:

```pascal
type
  TNodo = class                    { objetos: referencia + Create/Free }
    Valor: Integer;
    Izq, Der: TNodo;
  end;

  INodo = interface ... end;        { interfaces: CONTADAS por referencia, se liberan solas }

  TArbol = specialize TFPGMap<Integer, string>;   { genéricos de biblioteca }
```

Las interfaces de Delphi son el único mecanismo del lenguaje con gestión automática de memoria, y por
eso se usan a veces solo por eso — un uso que sorprende a quien las conoce solo como contrato de tipos.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(defun insertar (arbol x)
  (cond ((null arbol) (list x nil nil))
        ((< x (first arbol))
         (list (first arbol) (insertar (second arbol) x) (third arbol)))
        (t
         (list (first arbol) (second arbol) (insertar (third arbol) x)))))

(defun inorden (arbol)
  (if (null arbol)
      '()
      (append (inorden (second arbol))
              (list (first arbol))
              (inorden (third arbol)))))

(let ((arbol nil))
  (loop for x = (read *standard-input* nil nil)
        while x
        do (setf arbol (insertar arbol x)))
  (format t "inorden=~{~D~^-~}~%" (inorden arbol)))
```

**Lo que esta clase enseña en Common Lisp.** Aquí hay algo que ningún otro lenguaje de esta página
puede decir: **el árbol no necesita estructura de datos, porque la lista de Lisp YA es un árbol**.

`(3 (1 nil nil) (4 nil nil))` es a la vez el valor, su representación textual y su forma escrita en el
código fuente. Se puede imprimir, guardar en un fichero, leer de vuelta con `read` y seguir siendo el
mismo árbol — sin serializador, sin esquema y sin biblioteca.

Esa propiedad —**homoiconicidad**— es la razón de ser de Lisp: **el código es un árbol, y los datos
también**, así que un programa puede construir y transformar programas con las mismas funciones que
usa para los datos. Es de donde salen las macros (clase 092).

Y fíjate en que este `insertar` **no modifica nada**: devuelve un árbol nuevo. Es una estructura
**persistente**, en el sentido funcional del término: las versiones anteriores siguen siendo válidas.

Lo notable es el coste: **el árbol nuevo comparte con el viejo todas las ramas que no cambiaron**.
Insertar en un árbol equilibrado de un millón de nodos copia unos veinte nodos, no un millón. Es
*structural sharing*, y es la base de las estructuras inmutables de Clojure, Scala, Immutable.js y
Rust con `im`.

Que se consiga sin ninguna maquinaria —solo `cons` y recursión— es lo que hace que Lisp siga
apareciendo en cualquier discusión seria sobre estructuras persistentes.

Para árboles con rendimiento, Common Lisp usa `defstruct` (clase 091), que da acceso por
desplazamiento en lugar de recorrer *conses*:

```lisp
(defstruct nodo valor izq der)
(setf (nodo-izq n) hijo)
```

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
proc insertar {arbol x} {
    if {[llength $arbol] == 0} {
        return [list $x {} {}]
    }
    lassign $arbol v izq der
    if {$x < $v} {
        return [list $v [insertar $izq $x] $der]
    }
    return [list $v $izq [insertar $der $x]]
}

proc inorden {arbol} {
    if {[llength $arbol] == 0} { return {} }
    lassign $arbol v izq der
    return [concat [inorden $izq] [list $v] [inorden $der]]
}

gets stdin linea
set arbol {}
foreach x [split [string trim $linea]] {
    set arbol [insertar $arbol $x]
}

puts "inorden=[join [inorden $arbol] -]"
```

**Lo que esta clase enseña en Tcl.** La representación es la misma que en Lisp —**una lista de tres
elementos: valor, izquierda y derecha**— y por la misma razón: en Tcl, una lista puede contener
listas, así que **una lista anidada es un árbol**.

Y como en Lisp, es un valor: se imprime, se guarda en un fichero y se lee de vuelta.

```tcl
set arbol {3 {1 {} {}} {4 {} {}}}
```

Esa cadena es el árbol. No hay serialización porque no hay nada que serializar.

Para árboles grandes, esta representación tiene un coste real: **cada `insertar` reconstruye el camino
desde la raíz**, y `concat` en el recorrido copia listas. Tcl tiene dos alternativas idiomáticas.

**La primera es el `array` con claves compuestas**, que es lo que se usa en código de producción:

```tcl
set nodo(1,valor) 3
set nodo(1,izq) 2
set nodo(1,der) 3
array names nodo *,valor          ;# todos los nodos
```

Esa notación de "clave compuesta separada por comas" es el idioma clásico de Tcl para estructuras
multidimensionales, y funciona porque **la clave de un array es una cadena cualquiera** — igual que
los subíndices de M.

**La segunda es el paquete `struct::tree` de Tcllib**, que es sorprendentemente completo: nodos con
atributos, recorridos en preorden, postorden y en anchura, serialización, corte y pegado de subárboles.

Y hay un uso de árboles que en Tcl es cotidiano y no se ve como tal: **el widget `ttk::treeview` de
Tk**, que muestra un árbol con columnas y es lo que se usa para tablas, listas jerárquicas y
exploradores de ficheros. Cualquiera que haya usado una interfaz Tk ha usado un árbol de Tcl sin
saberlo.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

sub insertar {
    my ($nodo, $x) = @_;
    return { valor => $x, izq => undef, der => undef } unless defined $nodo;
    if ($x < $nodo->{valor}) {
        $nodo->{izq} = insertar($nodo->{izq}, $x);
    } else {
        $nodo->{der} = insertar($nodo->{der}, $x);
    }
    return $nodo;
}

sub inorden {
    my ($nodo) = @_;
    return () unless defined $nodo;
    return (inorden($nodo->{izq}), $nodo->{valor}, inorden($nodo->{der}));
}

my $linea = <STDIN>;
chomp $linea;

my $raiz;
$raiz = insertar($raiz, $_) for split ' ', $linea;

print "inorden=", join('-', inorden($raiz)), "\n";
```

**Lo que esta clase enseña en Perl.** Las estructuras anidadas de Perl se construyen con
**referencias**, y esta clase es donde eso se vuelve imprescindible.

La razón es la de la clase 089: **los arreglos y los hashes se aplanan**. `(@a, @b)` es una sola
lista, así que no se puede meter un hash dentro de otro directamente. La solución de Perl 5 fue añadir
**referencias**, que son escalares que apuntan a una estructura:

```perl
my $ref = { valor => 1 };        # referencia a HASH anónimo
my $lst = [ 1, 2, 3 ];            # referencia a ARREGLO anónimo
$ref->{valor}                      # acceso con flecha
$$ref{valor}                       # la misma cosa, sintaxis antigua
${$ref}{valor}                     # y otra vez, explícita
@{$lst}                            # desreferenciar el arreglo entero
```

Que haya tres sintaxis para lo mismo es una de las cosas que hacen difícil leer Perl ajeno. La
recomendación moderna es usar siempre `->`.

Perl 5 no tenía referencias en su versión original: **llegaron en Perl 5.0 (1994)**, y fueron el
cambio que convirtió a Perl de lenguaje de guion en lenguaje de propósito general. Sin ellas no hay
estructuras anidadas, no hay objetos —un objeto es una referencia bendecida— y no hay clausuras
útiles.

La documentación oficial dedica dos capítulos enteros al tema, `perlref` y `perldsc` (*Data Structures
Cookbook*), y ese segundo nombre es revelador: **hizo falta un recetario** para explicar cómo se
construye un hash de arreglos de hashes.

Y aquí conviene señalar el peligro que acompaña a esta clase: **las referencias circulares no se
liberan**. Perl usa conteo de referencias, así que un árbol con punteros al padre **nunca se libera**
salvo que se usen referencias débiles:

```perl
use Scalar::Util qw(weaken);
$hijo->{padre} = $nodo;
weaken($hijo->{padre});       # no cuenta para el conteo de referencias
```

Es el mismo problema que `std::shared_ptr` resuelve con `std::weak_ptr`, y una de las razones por las
que los árboles con enlace al padre son una fuente conocida de fugas.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>
#include <memory>
#include <string>

struct Nodo {
    int valor;
    std::unique_ptr<Nodo> izq, der;
    explicit Nodo(int v) : valor(v) {}
};

void insertar(std::unique_ptr<Nodo>& p, int x) {
    if (!p) {
        p = std::make_unique<Nodo>(x);
    } else if (x < p->valor) {
        insertar(p->izq, x);
    } else {
        insertar(p->der, x);
    }
}

void inorden(const std::unique_ptr<Nodo>& p, std::string& salida) {
    if (!p) return;
    inorden(p->izq, salida);
    if (!salida.empty()) salida += '-';
    salida += std::to_string(p->valor);
    inorden(p->der, salida);
}

int main() {
    std::unique_ptr<Nodo> raiz;
    int x{};
    while (std::cin >> x) {
        insertar(raiz, x);
    }

    std::string salida;
    inorden(raiz, salida);

    std::cout << "inorden=" << salida << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** El programa no tiene ni un `delete`, y **no hay ninguna fuga de
memoria**. Esa es la lección.

`std::unique_ptr` (C++11) es un puntero que **posee** lo que apunta y lo destruye al salir del ámbito.
Cuando `raiz` muere al final de `main`, su destructor destruye su nodo, cuyo destructor destruye sus
hijos, y así hasta las hojas. **El árbol entero se libera solo**, en cascada.

Eso es **RAII** —*Resource Acquisition Is Initialization*— y es la respuesta de C++ a la gestión de
memoria: en lugar de un recolector de basura, **destructores deterministas** que se ejecutan en un
momento conocido, en orden inverso a la construcción (clase 096).

Tres detalles del código:

- **`std::make_unique<Nodo>(x)`** en lugar de `new Nodo(x)`: reserva y envuelve en una operación, sin
  que quede un puntero crudo en ningún momento. Es lo recomendado desde C++14.
- **`std::unique_ptr<Nodo>&`** como parámetro: se pasa **por referencia** porque `unique_ptr` no se
  puede copiar —solo tiene un dueño— y hay que poder modificarlo.
- **`explicit`** en el constructor evita conversiones implícitas de `int` a `Nodo`.

Y hay una trampa real que conviene conocer, porque afecta a este mismo programa: **la destrucción en
cascada es recursiva**. Un árbol degenerado en lista de un millón de nodos **desborda la pila al
destruirse**, no al construirse. La solución es un destructor iterativo, y es un ejercicio clásico de
entrevista.

Para los otros dos casos, C++ tiene:

```cpp
std::shared_ptr<Nodo>     // propiedad COMPARTIDA, con conteo de referencias
std::weak_ptr<Nodo>       // observador que NO cuenta: para el enlace al padre
```

El par `shared_ptr`/`weak_ptr` resuelve exactamente el problema de los ciclos que en Perl requiere
`weaken`, y por la misma razón: los dos usan conteo de referencias.

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

dcl-pi ARBOL;
  entrada char(200) const;
end-pi;

dcl-ds nodo qualified dim(100);
  valor int(10);
  izq   int(10);
  der   int(10);
end-ds;

dcl-s raiz int(10) inz(0);
dcl-s nn   int(10) inz(0);
dcl-s act  int(10);
dcl-s i    int(10);
dcl-s tok  varchar(20) inz('');
dcl-s c    char(1);
dcl-s x    int(10);
dcl-s salida varchar(200) inz('');
dcl-s pila int(10) dim(100);
dcl-s tope int(10) inz(0);

for i = 1 to %len(%trimr(entrada)) + 1;
  if i <= %len(%trimr(entrada));
    c = %subst(entrada : i : 1);
  else;
    c = ' ';
  endif;
  if c = ' ';
    if tok <> '';
      x = %int(tok);
      nn += 1;
      nodo(nn).valor = x;
      nodo(nn).izq = 0;
      nodo(nn).der = 0;
      if raiz = 0;
        raiz = nn;
      else;
        act = raiz;
        dow '1' = '1';
          if x < nodo(act).valor;
            if nodo(act).izq = 0;
              nodo(act).izq = nn;
              leave;
            endif;
            act = nodo(act).izq;
          else;
            if nodo(act).der = 0;
              nodo(act).der = nn;
              leave;
            endif;
            act = nodo(act).der;
          endif;
        enddo;
      endif;
      tok = '';
    endif;
  else;
    tok += c;
  endif;
endfor;

// recorrido en orden, con pila explicita
act = raiz;
dow act <> 0 or tope > 0;
  dow act <> 0;
    tope += 1;
    pila(tope) = act;
    act = nodo(act).izq;
  enddo;
  act = pila(tope);
  tope -= 1;
  if salida <> '';
    salida += '-';
  endif;
  salida += %char(nodo(act).valor);
  act = nodo(act).der;
enddo;

dsply ('inorden=' + salida);

*inlr = *on;
return;
```

**Lo que esta clase enseña en RPG.** RPG usa la misma representación que COBOL —**índices dentro de
una tabla de estructuras**— y por la misma razón: es lo que encaja con el modelo de datos de la
plataforma.

RPG **sí tiene punteros** desde ILE (clase 090), con `based(p)` y `%alloc`, así que un árbol con
punteros es escribible:

```rpgle
dcl-ds nodo qualified based(p);
  valor int(10);
  izq   pointer;
  der   pointer;
end-ds;

p = %alloc(%size(nodo));
```

Y **RPG sí tiene recursión** desde ILE: un `dcl-proc` con `dcl-pi` es recursivo si sus variables se
declaran dentro del procedimiento, porque entonces son automáticas.

```rpgle
dcl-proc inorden;
  dcl-pi *n;
    p pointer value;
  end-pi;
  dcl-s local int(10);        // automática: una copia POR LLAMADA
  ...
end-proc;
```

Que este programa use igualmente índices y una pila explícita refleja lo que se encuentra en código
real, y no es inercia: en IBM i, **una estructura de datos que se pueda escribir en un fichero es más
útil que una que solo viva en memoria**.

Pero la respuesta idiomática de la plataforma a esta clase es otra, y conviene decirla: **un árbol de
búsqueda ordenado en IBM i es un índice de base de datos**.

```rpgle
setll (*loval) MOVIMIENTOS;      // posicionarse al principio del índice
dow *on;
  reade MOVIMIENTOS;              // leer en ORDEN DE CLAVE
  if %eof(MOVIMIENTOS);
    leave;
  endif;
  // ... procesar en orden ascendente
enddo;
```

`setll` + `reade` recorre un índice —un árbol B mantenido por el sistema— **en orden**, que es
exactamente lo que hace el recorrido en orden de este programa. El sistema operativo mantiene el
árbol, lo equilibra, lo persiste y lo comparte entre trabajos.

Es el mismo argumento que en COBOL con VSAM y en M con los *globals*: **el árbol serio está en disco y
lo mantiene la plataforma**.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 arbol: procedure options(main) reorder;

    declare 1 nodo based(p),
              2 valor fixed binary(31),
              2 izq   pointer,
              2 der   pointer;

    declare (p, q, raiz, act) pointer;
    declare linea char(200) varying;
    declare tok char(20) varying initial('');
    declare c char(1);
    declare i fixed binary(31);
    declare x fixed binary(31);
    declare salida char(200) varying initial('');
    declare colocado bit(1);

    raiz = null();
    get edit (linea) (a(200));

    do i = 1 to length(linea) + 1;
       if i <= length(linea) then c = substr(linea, i, 1); else c = ' ';
       if c = ' ' then do;
          if tok ^= '' then do;
             x = tok;
             allocate nodo set(q);
             q -> valor = x;
             q -> izq = null();
             q -> der = null();
             if raiz = null() then raiz = q;
             else do;
                act = raiz;
                colocado = '0'b;
                do while (^colocado);
                   if x < act -> valor then do;
                      if act -> izq = null() then do;
                         act -> izq = q; colocado = '1'b;
                      end;
                      else act = act -> izq;
                   end;
                   else do;
                      if act -> der = null() then do;
                         act -> der = q; colocado = '1'b;
                      end;
                      else act = act -> der;
                   end;
                end;
             end;
             tok = '';
          end;
       end;
       else tok = tok || c;
    end;

    call inorden(raiz);
    put skip list ('inorden=' || salida);

 inorden: procedure (n) recursive;
    declare n pointer;
    if n = null() then return;
    call inorden(n -> izq);
    if salida ^= '' then salida = salida || '-';
    salida = salida || trim(char(n -> valor));
    call inorden(n -> der);
 end inorden;

 end arbol;
```

**Lo que esta clase enseña en PL/I.** **PL/I fue el primer lenguaje de alto nivel con todo lo
necesario para escribir esto**, en 1964: estructuras, punteros, reserva dinámica y recursión. C llegó
ocho años después; Pascal, seis; Fortran, veintiséis.

Las tres piezas están en este programa:

```pli
declare 1 nodo based(p), 2 valor fixed binary(31), 2 izq pointer, 2 der pointer;
allocate nodo set(q);        /* reservar y dejar el puntero en q */
q -> valor = x;               /* acceso a través de puntero */
free q -> nodo;               /* liberar */
```

**La flecha `->` de C viene de aquí.** Y `based` —"esta estructura describe lo que haya donde apunte
el puntero, sin memoria propia"— es el antepasado directo del `BASED` de COBOL, del `based` de RPG y,
en espíritu, del `struct` + `malloc` de C.

La palabra **`recursive`** en el procedimiento es necesaria por la misma razón que en COBOL y Fortran:
**por defecto, las variables automáticas de un procedimiento PL/I podían asignarse estáticamente**, y
declarar la recursión avisa al compilador de que necesita marcos de pila.

Es notable la coincidencia: **COBOL, Fortran y PL/I —los tres lenguajes mayoritarios de los sesenta—
tenían la recursión desactivada por defecto**, y los tres la añadieron como declaración explícita.
Algol 60 la tenía desde el principio, y esa diferencia fue uno de los grandes debates de la época: la
recursión se consideraba un lujo académico caro.

Sobre la memoria, PL/I no tiene recolector de basura y `free` es responsabilidad del programador,
igual que en C. Lo que sí tiene, y es raro para su época, es la condición **`STORAGE`** que se puede
capturar cuando la reserva falla:

```pli
 on condition(storage) begin; put list('sin memoria'); end;
```

Un manejador de "sin memoria" declarativo, en 1964. Es la misma idea que el `Storage_Error` de Ada y
que `std::bad_alloc` de C++.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
ARBOL ; Arboles -- clase 097
 read linea
 kill arbol
 set n = $length(linea, " ")
 ; el array de M YA es un arbol ordenado: basta con usar el valor como subindice
 for i=1:1:n set arbol($piece(linea, " ", i)) = ""
 set salida = "", k = ""
 for  set k = $order(arbol(k))  quit:k=""  do
 . if salida '= "" set salida = salida _ "-"
 . set salida = salida _ k
 write "inorden=", salida, !
 quit
```

**Lo que esta clase enseña en M.** Aquí M no construye un árbol: **usa el que ya tiene**.

Un array de M **es un árbol ordenado**, y sus subíndices se mantienen en orden sin que nadie lo pida.
Así que "insertar en un árbol binario de búsqueda y recorrerlo en orden" se reduce a:

```mumps
 set arbol(x) = ""                                  ; insertar
 for  set k = $order(arbol(k))  quit:k=""  ...      ; recorrer EN ORDEN
```

Dos líneas frente a las ochenta de COBOL. Y no es un truco: **`$order` sobre un array es literalmente
un recorrido en orden de un árbol**, y la implementación por debajo es un **árbol B**, no un árbol
binario — mejor equilibrado y mucho mejor para disco.

Lo que hace M diferente es que esa estructura es **la única que tiene**, y que sirve para todo: array,
diccionario, conjunto, lista ordenada y árbol multinivel.

```mumps
 set ^ORG("ventas", "europa", "españa", "madrid") = 100
```

Cuatro niveles de jerarquía, sin declarar nada, ordenados en cada nivel, y **en disco**. Recorrer un
subárbol es `$order` sobre el nivel que interese; contar sus hijos es un bucle; borrar la rama entera
es `kill ^ORG("ventas","europa")`.

Y `$query` recorre **el árbol completo en profundidad**, saltando entre niveles:

```mumps
 set ref = "^ORG"
 for  set ref = $query(@ref)  quit:ref=""  write ref, "=", @ref, !
```

Es un recorrido en preorden de una estructura arbitrariamente profunda, en una línea, sobre datos
persistentes.

Esa es la baza de M y la razón de que las bases de datos que lo implementan —InterSystems IRIS,
YottaDB— compitan en rendimiento con motores mucho más modernos en cargas jerárquicas: **el árbol no
es una estructura que el programa construye sobre la base de datos, es la base de datos**.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| v ordenado |

v := stdin nextLine substrings collect: [ :cada | cada asNumber ].

"SortedCollection mantiene el orden en la inserción, como un BST"
ordenado := SortedCollection sortBlock: [ :a :b | a <= b ].
v do: [ :cada | ordenado add: cada ].

Transcript
    show: 'inorden=', ((ordenado collect: [ :cada | cada printString ])
        inject: '' into: [ :acc :cada |
            acc isEmpty ifTrue: [ cada ] ifFalse: [ acc, '-', cada ] ]);
    cr.
```

**Lo que esta clase enseña en Smalltalk.** El programa usa `SortedCollection` en lugar de construir un
árbol, y eso es deliberado: **la propiedad que esta clase quiere mostrar —insertar y obtener en orden—
la ofrece la biblioteca directamente**.

```smalltalk
| c |
c := SortedCollection sortBlock: [ :a :b | a valor <= b valor ].
c add: x.          "inserta EN SU SITIO"
c first.            "el menor"
c last.             "el mayor"
```

El **bloque de ordenación** se pasa al crear la colección, así que el criterio es un parámetro, no una
propiedad del tipo. Cambiar el orden es cambiar un bloque, sin tocar la clase de los elementos y sin
`Comparator` ni `operator<`.

Para un árbol de verdad, en Smalltalk se escribe como una clase, y el resultado es notablemente
legible:

```smalltalk
Object subclass: #Nodo
    instanceVariableNames: 'valor izq der'.

Nodo >> insertar: x
    x < valor
        ifTrue: [ izq isNil ifTrue: [ izq := Nodo nuevo: x ] ifFalse: [ izq insertar: x ] ]
        ifFalse: [ der isNil ifTrue: [ der := Nodo nuevo: x ] ifFalse: [ der insertar: x ] ]

Nodo >> inordenHacer: unBloque
    izq ifNotNil: [ izq inordenHacer: unBloque ].
    unBloque value: valor.
    der ifNotNil: [ der inordenHacer: unBloque ]
```

Fíjate en `inordenHacer:`, que **recibe un bloque en lugar de devolver una lista**. Es el patrón de
iteración interna de Smalltalk: en lugar de construir la colección de resultados, el árbol **llama al
bloque una vez por nodo**. No reserva memoria y es lo que hacen `do:`, `collect:` y toda la jerarquía
de colecciones.

Ese detalle es una diferencia real con los iteradores externos de C++, Ada y Rust: aquí **la
estructura controla el recorrido y el cliente aporta el qué hacer**, mientras que un iterador externo
deja el control al cliente. La iteración interna es más simple y no permite recorrer dos estructuras a
la vez, que es justo lo que resuelve el iterador externo.

Y no hay memoria que liberar: **Smalltalk tiene recolector de basura desde 1980**, y fue uno de los
primeros sistemas en tenerlo generacional.

---

## Y de vuelta a la clase

Lo transferible: **un puntero y un índice de tabla son la misma cosa con distinto alcance**. El
puntero apunta a memoria y muere con el proceso; el índice apunta dentro de un bloque y **se puede
escribir en disco, enviar por la red y volver a leer**. Por eso los formatos binarios, las bases de
datos y los sistemas de ficheros usan índices y desplazamientos, no punteros. Cuando serialices una
estructura enlazada, lo primero que harás será convertir sus punteros en índices — que es donde COBOL
llevaba desde el principio.

⏮️ [Volver a la clase 097](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
