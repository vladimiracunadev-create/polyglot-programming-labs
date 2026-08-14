# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 045

> [⬅️ Volver a la clase 045](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Sumar `0.1` y `0.2`. El caso de prueba más famoso de la informática, y el que separa a los lenguajes
en dos familias: los que calculan en **binario** —donde `0.1` no existe exactamente y la suma da
`0.30000000000000004`— y los que calculan en **decimal**, donde da `0.30` y punto. Esta página tiene
representantes de las dos, y la diferencia no es académica: es la razón de que la banca no use
`double`.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es **la representación de los reales y su error acumulado**, y estos lenguajes lo
> enseñan porque **algunos eligieron no tener el problema**. COBOL, RPG y PL/I usan aritmética decimal
> de coma fija: `0.1 + 0.2` da exactamente `0.30` porque nunca pasan por binario. Fortran y Ada
> eligieron lo contrario —binario IEEE— porque su dominio es el cálculo científico, donde el error
> relativo importa más que el céntimo exacto.
>
> Que dos familias de lenguajes tomaran decisiones opuestas **por buenas razones** es la lección de
> esta clase. No hay una representación correcta: hay una correcta *para tu dominio*.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: una línea `a b` (dos reales) → stdout: `suma=<a+b con 2 decimales> producto=<a*b con 2 decimales>`
- **Regla:** `suma = a + b ; producto = a * b (ambos a 2 decimales)`

| stdin | esperado |
|---|---|
| `1.5 2.5` | `suma=4.00 producto=3.75` |
| `0.1 0.2` | `suma=0.30 producto=0.02` |
| `10 3` | `suma=13.00 producto=30.00` |

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
PROGRAM-ID. REALES.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA     PIC X(80).
01  TXT-A     PIC X(20).
01  TXT-B     PIC X(20).
01  A         PIC S9(9)V9(4) COMP-3.
01  B         PIC S9(9)V9(4) COMP-3.
01  SUMA      PIC S9(9)V99   COMP-3.
01  PRODUCTO  PIC S9(9)V99   COMP-3.
01  ED-S      PIC -(9)9.99.
01  ED-P      PIC -(9)9.99.

PROCEDURE DIVISION.
    ACCEPT LINEA
    UNSTRING LINEA DELIMITED BY ALL SPACES INTO TXT-A TXT-B
    MOVE FUNCTION NUMVAL(TXT-A) TO A
    MOVE FUNCTION NUMVAL(TXT-B) TO B

    COMPUTE SUMA     ROUNDED = A + B
    COMPUTE PRODUCTO ROUNDED = A * B

    MOVE SUMA     TO ED-S
    MOVE PRODUCTO TO ED-P
    DISPLAY "suma=" FUNCTION TRIM(ED-S)
            " producto=" FUNCTION TRIM(ED-P)
    STOP RUN.
```

**Lo que esta clase enseña en COBOL.** **En COBOL, `0.1 + 0.2` da `0.30`. Exactamente.** No por
suerte ni por redondeo al imprimir: porque `PIC S9(9)V9(4) COMP-3` **no es punto flotante**. Es
decimal empaquetado —cada dígito decimal en medio byte— y la aritmética es decimal de principio a
fin. El número `0.1` se guarda como el dígito 1 en la primera posición decimal, no como la
aproximación binaria más cercana.

Esa es la respuesta de COBOL a esta clase, y explica su supervivencia mejor que ningún argumento
sobre coste de migración.

COBOL **sí** tiene punto flotante binario si lo quieres —`COMP-1` es de 32 bits y `COMP-2` de 64—,
y son los tipos correctos para cálculo científico. Lo que COBOL hace bien es **obligarte a elegir**:
el tipo se declara, así que la decisión "esto es dinero, esto es una magnitud" queda escrita.

Y `ROUNDED` no es opcional por descuido: sin él, `COMPUTE` **trunca** al guardar. En dinero, decidir
entre truncar y redondear es una decisión de negocio, y COBOL la pone en la sentencia. Además admite
la política: `ROUNDED MODE IS NEAREST-EVEN`, `TOWARD-GREATER`, `PROHIBITED`…

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program reales
   implicit none
   real(kind=8) :: a, b
   character(len=32) :: bs, bp

   read(*, *) a, b

   write(bs, '(F20.2)') a + b
   write(bp, '(F20.2)') a * b

   write(*, '(A,A,A,A)') 'suma=', trim(adjustl(bs)), &
                         ' producto=', trim(adjustl(bp))
end program reales
```

**Lo que esta clase enseña en Fortran.** Fortran es el lado opuesto de COBOL, y con la misma buena
razón: en simulación climática o en dinámica de fluidos **no existe el valor exacto**. Los datos
vienen de sensores con error, el modelo es una aproximación, y lo que importa es el **error relativo
acumulado a lo largo de mil millones de operaciones**. El punto flotante binario IEEE 754 es la
herramienta correcta para eso, y aquí `0.1 + 0.2` da `0.30000000000000004`, como debe ser.

Por eso Fortran trae herramientas para **preguntar por la precisión** que casi ningún lenguaje ofrece:

```fortran
epsilon(1.0d0)   ! el menor x tal que 1+x /= 1  -> ~2.2e-16
huge(1.0d0)      ! el mayor representable
tiny(1.0d0)      ! el menor positivo normalizado
precision(1.0d0) ! dígitos decimales significativos -> 15
nearest(x, 1.0)  ! el siguiente representable hacia arriba
```

Estas funciones son la razón de que el código numérico serio se escriba en Fortran: permiten
comparar con tolerancia de forma disciplinada —`abs(a - b) < epsilon(a) * abs(a)`— en vez del `==`
que nunca hay que usar con reales.

Y el detalle del programa: `F20.2` en un buffer y luego `trim(adjustl(...))`, en lugar de `F0.2`
directo. `F0.2` pide ancho mínimo, pero **su comportamiento con el cero varía entre compiladores**
—algunos escriben `.00` sin el cero inicial—, y el contrato de la clase exige la misma salida en
todas partes.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;            use Ada.Text_IO;
with Ada.Long_Float_Text_IO; use Ada.Long_Float_Text_IO;

procedure Reales is
   A, B : Long_Float;
begin
   Get (A);
   Get (B);

   Put ("suma=");      Put (A + B, Fore => 1, Aft => 2, Exp => 0);
   Put (" producto="); Put (A * B, Fore => 1, Aft => 2, Exp => 0);
   New_Line;
end Reales;
```

**Lo que esta clase enseña en Ada.** Ada es el único lenguaje de esta página que te deja **declarar
la precisión que necesitas y hacer que el compilador la garantice**, en lugar de elegir entre `float`
y `double` y esperar que baste:

```ada
type Temperatura is digits 6  range -273.15 .. 1000.0;   --  coma flotante
type Euros       is delta 0.01 range 0.0 .. 1.0e9;       --  COMA FIJA
```

`digits 6` pide **al menos** seis dígitos significativos: si la máquina no puede, **no compila**.
Nada de descubrir en producción que `float` no daba para tanto.

Y `delta 0.01` es lo importante para esta clase: declara un **tipo de coma fija**, con incrementos
exactos de un céntimo. Ada tiene aritmética decimal exacta **en el sistema de tipos**, igual que
COBOL, pero expresada como una propiedad del tipo en lugar de como una plantilla de dígitos. Existe
además `type Dinero is delta 0.01 digits 12` —coma fija **decimal**— pensada explícitamente para
interoperar con COBOL en sistemas mixtos.

Así que Ada no elige bando en el debate de esta clase: te da las dos representaciones y te obliga a
decir cuál usas y con qué garantías.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Reales;
{$MODE OBJFPC}{$H+}

var
  A, B: Double;

begin
  Read(A, B);

  WriteLn('suma=', (A + B):0:2, ' producto=', (A * B):0:2);
end.
```

**Lo que esta clase enseña en Pascal.** El formateo `valor:ancho:decimales` está **en la sintaxis del
`Write`**, no en una cadena de plantilla, y eso tiene una consecuencia que se agradece: **no depende
de la configuración regional**. En un equipo configurado en español, `Format('%.2f', [x])` de Delphi
produce `0,30` con coma; `x:0:2` produce siempre `0.30` con punto.

Ese detalle ha roto más integraciones de las que parece: un fichero CSV generado en un servidor
español que el sistema receptor no puede leer. Cuando el destino es una máquina y no una persona,
el formateo independiente de la configuración regional no es una preferencia estética.

Sobre la representación, Free Pascal y Delphi ofrecen la escala completa —`Single` (32 bits), `Double`
(64), `Extended` (80 en x86)— y, para esta clase, lo importante: **`Currency`**, un entero de 64 bits
escalado con **cuatro decimales fijos**, es decir, decimal exacto para dinero. Es el mismo tipo que
tiene [VBA](../../../atlas/vba.md), y por el mismo motivo: los dos vienen del mundo de las
aplicaciones de gestión.

`Extended` de 80 bits merece una nota: es un tipo real del x87 que ya casi nadie usa y que **no
existe en x86-64 con SSE ni en ARM**. Código antiguo que dependía de esos bits de más da resultados
distintos al recompilarlo hoy.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(setf *read-default-float-format* 'double-float)

(let* ((a (read))
       (b (read)))
  (format t "suma=~,2F producto=~,2F~%" (+ a b) (* a b)))
```

**Lo que esta clase enseña en Common Lisp.** Lisp tiene una tercera respuesta, distinta de la de
COBOL y de la de Fortran: **los racionales exactos**.

```lisp
(+ 1/10 2/10)     ; => 3/10     exacto, sin error
(+ 0.1d0 0.2d0)   ; => 0.30000000000000004d0
(rationalize 0.1) ; => 1/10     la fracción "que el humano quería decir"
(rational 0.1)    ; => 3602879701896397/36028797018963968  el valor REAL del double
```

Esas dos últimas líneas son la mejor demostración pedagógica que existe del problema de esta clase.
`rational` te enseña **qué número guarda de verdad un `double` cuando escribiste `0.1`**: no es una
décima, es una fracción de denominador 2⁵⁵. `rationalize` devuelve la fracción simple más probable.
Ver los dos resultados juntos explica el punto flotante mejor que cualquier párrafo.

Y la aritmética se comporta en consecuencia: mientras trabajas con racionales, todo es exacto; en
cuanto entra un `float`, el resultado se **contagia** y pasa a ser aproximado. La regla de contagio
está en el estándar y es predecible.

`*read-default-float-format*` en la primera línea es necesario porque, sin ella, `0.1` se leería como
precisión simple y los errores serían mucho mayores.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea
lassign [split [string trim $linea]] a b

set suma     [expr {$a + $b}]
set producto [expr {$a * $b}]

puts "suma=[format %.2f $suma] producto=[format %.2f $producto]"
```

**Lo que esta clase enseña en Tcl.** Tcl usa `double` IEEE para todo lo que no sea entero, así que
hereda el problema entero de esta clase. Pero tiene una peculiaridad interesante: como **el valor
canónico es la cadena**, la representación textual de un real importa mucho más que en otros
lenguajes.

Por eso Tcl 8.5 cambió a un algoritmo que garantiza el **viaje de ida y vuelta**: la cadena que
produce Tcl para un `double` es la más corta que, al volver a leerse, da **exactamente el mismo
double**. `expr {0.1 + 0.2}` muestra `0.30000000000000004` — no redondea para que quede bonito,
porque hacerlo rompería la identidad entre el valor y su texto.

Es la misma decisión que tomaron después JavaScript, Python 3 y Go, y en Tcl era obligatoria en vez
de deseable.

Para dinero, la comunidad recomienda dos caminos: trabajar en **enteros de céntimos** —posible
porque los enteros de Tcl son de precisión arbitraria— o usar el paquete `math::bignum` de Tcllib.
Nunca `double`.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;
my ($x, $y) = split ' ', $linea;

printf "suma=%.2f producto=%.2f\n", $x + $y, $x * $y;
```

**Lo que esta clase enseña en Perl.** Perl guarda los reales como `double` de C, con el mismo
comportamiento, y añade un matiz propio: como su escalar mantiene a la vez la representación
numérica y la textual, **`0.1 + 0.2` impreso con `print` da `0.3`**, no `0.30000000000000004`.

Eso no es que Perl calcule mejor: es que su conversión a texto por defecto usa **15 dígitos
significativos** en vez de los 17 necesarios para el viaje de ida y vuelta, y el error queda escondido
justo debajo del corte. El bug sigue ahí:

```perl
printf "%.17g\n", 0.1 + 0.2;   # 0.30000000000000004
print 0.1 + 0.2 == 0.3 ? "sí" : "no";   # no
```

Es un buen recordatorio de que **"se imprime bien" no significa "es exacto"**, y de que la
comparación de reales con `==` es un error en cualquier lenguaje.

Para dinero, CPAN ofrece las dos soluciones clásicas: `Math::BigFloat` para precisión arbitraria y
`bignum` como pragma que cambia el comportamiento de todo el ámbito. Y para saber qué está pasando
de verdad, `Data::Float` expone las piezas del IEEE 754.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iomanip>
#include <iostream>

int main() {
    double a{}, b{};
    if (!(std::cin >> a >> b)) return 1;

    std::cout << std::fixed << std::setprecision(2)
              << "suma=" << (a + b)
              << " producto=" << (a * b) << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** C++ hereda el punto flotante de C y expone sus propiedades a
través de `std::numeric_limits`, que es la versión con tipos de las funciones `epsilon`, `huge` y
`tiny` de Fortran:

```cpp
#include <limits>
std::numeric_limits<double>::epsilon();        // 2.22045e-16
std::numeric_limits<double>::max();
std::numeric_limits<double>::infinity();
std::numeric_limits<double>::quiet_NaN();
std::numeric_limits<double>::is_iec559;        // ¿cumple IEEE 754?
```

Esa última línea es la que importa en código serio: **el estándar de C++ no obliga a que `double` sea
IEEE 754**. Casi siempre lo es, y `is_iec559` lo dice.

Y hay dos trampas de esta clase que C++ enseña bien. La primera: `std::setprecision` **cambia de
significado** según haya o no `std::fixed`. Con `std::fixed` son decimales después del punto; sin él,
son **dígitos significativos totales**. La segunda: las dos son **pegajosas** —afectan a todo lo que
se escriba después en ese flujo—, igual que `std::hex`.

Para dinero, C++ no trae decimal en la biblioteca estándar. Se usa `boost::multiprecision`, una clase
propia sobre enteros de céntimos, o el tipo decimal de la propuesta ISO TR 24733, que sigue sin
adoptarse. Es una carencia real frente a COBOL, RPG y PL/I.

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

dcl-pi REALES;
  a packed(15:4) const;
  b packed(15:4) const;
end-pi;

dcl-s suma     packed(15:2);
dcl-s producto packed(15:2);
dcl-s salida   char(80);

suma     = a + b;
producto = a * b;

salida = 'suma=' + %char(suma) + ' producto=' + %char(producto);
dsply salida;

*inlr = *on;
return;
```

**Lo que esta clase enseña en RPG.** Como COBOL: `packed(15:4)` es **decimal exacto**, así que
`0.1 + 0.2` da `0.30` sin discusión. RPG tiene `float(4)` y `float(8)` para punto flotante binario,
y la guía de estilo de la plataforma es tajante — **no se usan para importes**.

Lo específico de RPG en esta clase es cómo trata el **redondeo**, que es lo que más sorprende al
llegar desde otro lenguaje. En RPG, `/` sobre decimales **redondea a la mitad hacia arriba** según los
decimales del destino, en lugar de truncar. `10 / 3` guardado en un `packed(5:2)` da `3.33`, y
guardado en un entero da **3**, pero `10 / 4` en un entero da **3**, no 2. Es aritmética de contable,
no de máquina.

Y cuando eso no basta, RPG tiene un operador propio: **`%dech`**, `%decp`, `%dec` con modo de
redondeo, y la palabra clave `half adjust` (`h` en formato fijo) que fuerza el redondeo comercial en
una operación concreta. Como el `ROUNDED` de COBOL: la política de redondeo es una decisión que se
escribe al lado de la operación, no un ajuste global.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 reales: procedure options(main);

    declare (a, b)   fixed decimal(15,4);
    declare suma     fixed decimal(15,2);
    declare producto fixed decimal(15,2);
    declare (ps, pp) picture 'ZZZZZZZZZ9V.99';

    get list (a, b);

    suma     = a + b;
    producto = a * b;

    ps = suma;
    pp = producto;
    put skip list ('suma=' || trim(ps) || ' producto=' || trim(pp));

 end reales;
```

**Lo que esta clase enseña en PL/I.** PL/I es donde esta clase se ve con más claridad, porque el
lenguaje **te obliga a decir en qué base calculas**. `fixed decimal(15,4)` es decimal exacto;
`float binary(53)` es el `double` de siempre. La misma expresión da resultados distintos según cómo
declaraste los operandos, y eso está a la vista en la declaración.

El precio de esa potencia son las **reglas de precisión del resultado**, que son famosas por lo poco
intuitivas. Al multiplicar `fixed decimal(15,4)` por `fixed decimal(15,4)`, el estándar define
exactamente cuántos dígitos y decimales tiene el resultado intermedio, y ese cálculo puede exceder la
precisión máxima del compilador y **truncar en silencio**. La condición `FIXEDOVERFLOW` existe
precisamente para atrapar eso:

```pli
on fixedoverflow put skip list ('desbordamiento decimal');
```

Es el mismo mecanismo `ON` de la clase 041: se instala un manejador para la condición y queda activo.
Un programa PL/I bien escrito para banca instala `FIXEDOVERFLOW`, `ZERODIVIDE` y `SIZE` al principio y
no vuelve a preocuparse.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
REALES ; Reales -- clase 045
 read linea
 set a = $piece(linea, " ", 1)
 set b = $piece(linea, " ", 2)
 set suma = a + b
 set producto = a * b
 write "suma=", $justify(suma, 0, 2)
 write " producto=", $justify(producto, 0, 2), !
 quit
```

**Lo que esta clase enseña en M.** M no tiene tipos, pero **sí tiene una decisión tomada sobre los
reales**, y es poco conocida: el estándar exige **al menos 15 dígitos decimales significativos** y la
aritmética de las implementaciones principales es **decimal**, no binaria. En YottaDB y en IRIS,
`0.1 + 0.2` da `0.3`.

No es casualidad: M nació en un hospital para manejar dosis, resultados de laboratorio y facturación
sanitaria. Un error de representación en una dosis no es un redondeo desafortunado.

`$justify(x, ancho, decimales)` es la función de formateo: con `ancho` 0 no rellena, y con el tercer
argumento **redondea** al número de decimales indicado. Con dos argumentos solo justifica a la
derecha. Es la misma función haciendo dos trabajos distintos según cuántos argumentos reciba, algo
muy propio de la economía de M.

Y una advertencia al leer código M antiguo: como todo es cadena, es habitual encontrar importes
guardados como texto con formato ya aplicado. Comparar `"10.50"` con `"10.5"` da falso como cadenas y
verdadero como números, y en M **el operador decide**: `=` compara como cadena, así que hay que
forzar el contexto numérico con `+` delante.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| partes a b |

partes := stdin nextLine substrings collect: [ :cada | cada asNumber ].
a := partes first.
b := partes second.

Transcript
    show: 'suma=', ((a + b) asFloat printShowingDecimalPlaces: 2);
    show: ' producto=', ((a * b) asFloat printShowingDecimalPlaces: 2);
    cr.
```

**Lo que esta clase enseña en Smalltalk.** Smalltalk tiene **tres respuestas** a esta clase, todas en
el mismo sistema de clases y todas con literal propio:

```smalltalk
0.1 + 0.2            "Float:         0.30000000000000004  — IEEE 754"
(1/10) + (2/10)      "Fraction:      3/10                 — exacto"
0.1s2 + 0.2s2        "ScaledDecimal: 0.30s2               — decimal exacto"
```

`ScaledDecimal` es el equivalente del `COMP-3` de COBOL: **decimal exacto, con el número de decimales
en el propio literal** (`s2` = dos decimales). Guarda internamente una fracción, así que las
operaciones intermedias no pierden precisión y solo se redondea al presentar.

Y `Fraction` aparece **sola**, sin pedirla: `1/3` en Smalltalk **no** es `0.333…`, es el objeto
`Fraction` con numerador 1 y denominador 3. `(1/3) * 3` da exactamente `1`. La división de dos
enteros que no dividen exactamente produce una fracción, no un real truncado ni un real aproximado —
una decisión que solo comparte con Lisp en esta página.

`printShowingDecimalPlaces:` es un mensaje al número. Como todo lo demás.

---

## Y de vuelta a la clase

Si te llevas una sola cosa de esta página, que sea esta: **`double` no es el tipo de los números con
decimales, es el tipo de las magnitudes físicas**. Para dinero, para porcentajes contractuales y para
cualquier cifra que alguien vaya a cuadrar a mano, el tipo correcto es el decimal exacto — y esos
lenguajes de sesenta años lo tienen de serie, mientras que Java, C# y Python tuvieron que añadirlo
después con `BigDecimal`, `decimal` y `Decimal`.

⏮️ [Volver a la clase 045](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
