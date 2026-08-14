# -*- coding: utf-8 -*-
"""Parte 6, lote O — clase 105. Ver `vivos_parte6.py` y `gen_vivos.py`."""

SPECS: dict[str, dict] = {}

# ---------------------------------------------------------------------------
# 105 — JSON: serialización y deserialización
# ---------------------------------------------------------------------------
SPECS["105"] = dict(
    gancho="""
Producir un objeto JSON. Es la clase donde mejor se ve lo que esta sección quiere demostrar: **JSON es
de 2001 y estos lenguajes son de 1959, y casi todos lo hablan hoy de forma nativa**. COBOL tiene
`JSON GENERATE` en el estándar desde 2014; RPG tiene `DATA-INTO` y `DATA-GEN`; Fortran tiene
`json-fortran`; Ada, `GNATCOLL.JSON`. **No es adaptación: es sintaxis del lenguaje o biblioteca
oficial.**
""",
    porque="""
Aquí el concepto es la **serialización a un formato de intercambio**, y estos lenguajes lo enseñan
porque su respuesta demuestra por qué siguen vivos: **cuando el mundo pasó a hablar JSON, ellos
aprendieron JSON**. La alternativa —reescribir cuarenta años de lógica de negocio— no era viable, así
que la modernización vino por donde tenía que venir: **por los bordes**.

Y muestran algo más: **Lisp, Tcl y Smalltalk ya tenían este problema resuelto antes de que existiera
JSON**, porque en los tres el formato de impresión de una estructura es legible por el propio
lenguaje.
""",
    cierre="""
Lo transferible: **generar JSON a mano es fácil y equivocado**. Los programas de esta página lo
construyen concatenando, y ninguno escapa las comillas, las barras invertidas ni los caracteres de
control del nombre. Con una entrada controlada funciona; con una entrada de usuario produce JSON
inválido en el mejor caso y una inyección en el peor. **Usa siempre un generador**: `JSON GENERATE`,
`DATA-GEN`, `json-fortran`, `GNATCOLL.JSON`, `JSON::PP`, `nlohmann/json`. Lo mismo vale para SQL, para
HTML y para CSV — y es la misma lección que la clase 106 repetirá con las comas.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. AJSON.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(200).
01  TXT-E   PIC X(20).
01  PERSONA-REG.
    05  NOMBRE  PIC X(20).
    05  EDAD    PIC 9(3).
01  ED-E    PIC Z(2)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    UNSTRING LINEA DELIMITED BY ALL SPACES INTO NOMBRE TXT-E
    COMPUTE EDAD = FUNCTION NUMVAL(TXT-E)
    MOVE EDAD TO ED-E

    DISPLAY '{"nombre": "' FUNCTION TRIM(NOMBRE)
            '", "edad": '  FUNCTION TRIM(ED-E) '}'
    STOP RUN.
""", """
**Lo que esta clase enseña en COBOL.** Este programa construye el JSON a mano —y el cierre de esta
clase explica por qué eso está mal—, así que lo importante es lo otro: **COBOL tiene JSON en el
lenguaje**.

**`JSON GENERATE`** y **`JSON PARSE`** entraron en el estándar con la enmienda de 2014 y están en IBM
Enterprise COBOL desde la versión 6.1:

```cobol
01  PERSONA-REG.
    05  NOMBRE  PIC X(20).
    05  EDAD    PIC 9(3).
01  SALIDA-JSON  PIC X(500).
01  LON  PIC 9(4) COMP.

JSON GENERATE SALIDA-JSON FROM PERSONA-REG
    COUNT IN LON
    NAME NOMBRE IS 'nombre' EDAD IS 'edad'
    SUPPRESS EDAD WHEN ZERO
    ON EXCEPTION DISPLAY "error al generar"
END-JSON
```

Lee eso con atención, porque es más de lo que parece:

- **Toma un grupo COBOL y produce JSON** con los campos como claves, **sin escribir el recorrido**.
- **`NAME ... IS`** renombra las claves, porque los nombres COBOL van en mayúsculas y con guiones y el
  JSON del mundo real no.
- **`SUPPRESS`** omite campos vacíos o cero.
- Y `JSON PARSE`, en el otro sentido, **rellena el grupo a partir de un JSON**, emparejando por
  nombre.

Eso significa que un programa COBOL de 1985 puede exponerse como servicio REST **añadiendo dos
sentencias**: `JSON PARSE` a la entrada y `JSON GENERATE` a la salida. Y esa es exactamente la
estrategia con la que IBM ha mantenido vivo el mainframe.

El cuadro se completa con **z/OS Connect**, que expone un programa CICS o IMS como API REST con JSON
sin tocar el código, y con `XML GENERATE`/`XML PARSE`, que llegaron antes por el mismo camino.

Y merece decirse con claridad: **un lenguaje de 1959 hablando el formato de intercambio de la web sin
capas intermedias** es el argumento más fuerte de toda esta sección del curso.

GnuCOBOL 3.x implementa `JSON GENERATE` sobre cJSON, con soporte parcial de las cláusulas.
"""),
        "fortran": ("""
program ajson
   implicit none
   character(len=200) :: linea
   character(len=20)  :: nombre
   integer :: edad, pos

   read(*, '(A)') linea
   pos = index(trim(linea), ' ')

   nombre = linea(1:pos-1)
   read(linea(pos+1:), *) edad

   write(*, '(A,I0,A)') '{"nombre": "' // trim(nombre) // '", "edad": ', &
                        edad, '}'
end program ajson
""", """
**Lo que esta clase enseña en Fortran.** El estándar de Fortran **no tiene JSON** y probablemente
nunca lo tendrá: no es su dominio. Lo que tiene es un ecosistema que lo resolvió.

**`json-fortran`** es la biblioteca de referencia, y su interfaz aprovecha los tipos derivados de
Fortran 2003:

```fortran
use json_module

type(json_file)   :: json
type(json_core)   :: core
type(json_value), pointer :: p

call json%initialize()
call json%load(filename='config.json')
call json%get('malla.nx', nx, encontrado)
call json%get('nombres', lista)

call core%create_object(p, '')
call core%add(p, 'nombre', 'Ada')
call core%add(p, 'edad', 36)
call core%print(p)
```

Y su existencia responde a una necesidad muy concreta: **los códigos científicos modernos necesitan
ficheros de configuración legibles**. Durante décadas, un código Fortran se configuraba con un
**fichero de entrada posicional** —línea 3, columnas 11 a 20, el paso de tiempo— o con las
**`namelist`**, que sí están en el estándar:

```fortran
namelist /parametros/ nx, ny, dt, metodo
read(10, nml=parametros)
```

Un fichero `namelist` se parece bastante a un `.ini`:

```text
&parametros
  nx = 100,
  dt = 0.01,
  metodo = 'implicito'
/
```

**Las `namelist` son de FORTRAN 77 como extensión y del estándar desde Fortran 90**, y siguen usándose
masivamente en modelos climáticos y de fluidos. Su ventaja es que **no hay que escribir el analizador
ni el escritor**: el lenguaje empareja los nombres con las variables.

Su límite es que son planas y propias de Fortran: nadie más las lee. De ahí el paso a JSON, YAML
(`fortran-yaml`) y TOML (`toml-f`) en los proyectos que tienen que hablar con Python, que hoy es la
mayoría.

Es un ejemplo limpio de modernización por necesidad de interoperar, no por moda.
"""),
        "ada": ("""
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Ajson is
   Comilla : constant Character := '"';

   Linea  : String (1 .. 200);
   Ultimo : Natural;
   Corte  : Natural := 0;
   Edad   : Integer;
begin
   Get_Line (Linea, Ultimo);

   for I in 1 .. Ultimo loop
      if Linea (I) = ' ' then
         Corte := I;
         exit;
      end if;
   end loop;

   Edad := Integer'Value (Linea (Corte + 1 .. Ultimo));

   Put ("{" & Comilla & "nombre" & Comilla & ": "
        & Comilla & Linea (1 .. Corte - 1) & Comilla & ", "
        & Comilla & "edad" & Comilla & ": ");
   Put (Edad, Width => 1);
   Put_Line ("}");
end Ajson;
""", """
**Lo que esta clase enseña en Ada.** Fíjate primero en un detalle de sintaxis: el programa declara
`Comilla : constant Character := '"';` porque **en Ada, para poner comillas dentro de una cadena hay
que duplicarlas**: el texto `él dijo "hola"` se escribe abriendo la cadena y poniendo dos comillas
seguidas por cada una que se quiera. Es la misma regla que en Pascal con los apóstrofos, y con muchas
comillas seguidas —como en este JSON— la constante se lee bastante mejor.

Y sobre JSON, Ada lo tiene resuelto por biblioteca oficial de AdaCore: **`GNATCOLL.JSON`**.

```ada
with GNATCOLL.JSON; use GNATCOLL.JSON;

declare
   Obj : JSON_Value := Create_Object;
begin
   Obj.Set_Field ("nombre", "Ada");
   Obj.Set_Field ("edad", 36);
   Put_Line (Obj.Write);              --  serializar

   declare
      Leido : JSON_Value := Read (Texto);
      N : String := Leido.Get ("nombre");
   begin
      null;
   end;
end;
```

`Set_Field` está sobrecargado para cada tipo, y `Get` devuelve el tipo que se le pida — con
`Constraint_Error` si no coincide, que es el comportamiento correcto en Ada.

Y esta clase es buen sitio para señalar dónde se usa Ada hoy con JSON, porque explica la necesidad:
**Ada está en la aviónica y en el control ferroviario, y esos sistemas se integran cada vez más con
servicios web**. Un sistema de gestión de tráfico aéreo escrito en Ada tiene que hablar con servicios
de meteorología que devuelven JSON.

El ecosistema moderno lo cubre bien: **GNATCOLL** trae además SQL, sockets, expresiones regulares,
registro de trazas y traducción; y **Alire** (clase 088) da acceso a bibliotecas de la comunidad —
`AWS` para servicios web, `VSS` para cadenas Unicode.

Y hay un dato que redondea la modernización de Ada: **GNAT compila a WebAssembly**, y hay proyectos
que ejecutan código Ada verificado con SPARK dentro de un navegador. Un lenguaje de 1983 en un destino
de 2017.
"""),
        "pascal": ("""
program Ajson;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  Linea, Nombre: string;
  Corte, Edad: Integer;

begin
  ReadLn(Linea);
  Linea := Trim(Linea);

  Corte := Pos(' ', Linea);
  Nombre := Copy(Linea, 1, Corte - 1);
  Edad := StrToInt(Trim(Copy(Linea, Corte + 1, Length(Linea))));

  WriteLn('{"nombre": "', Nombre, '", "edad": ', IntToStr(Edad), '}');
end.
""", """
**Lo que esta clase enseña en Pascal.** Free Pascal trae **`fpjson`** en su biblioteca estándar, y
Delphi trae `System.JSON`. Los dos son completos, y el de Free Pascal se usa así:

```pascal
uses fpjson, jsonparser;

var
  Obj: TJSONObject;
begin
  Obj := TJSONObject.Create;
  try
    Obj.Add('nombre', 'Ada');
    Obj.Add('edad', 36);
    WriteLn(Obj.AsJSON);                    { serializar }
  finally
    Obj.Free;                                { clase 103 }
  end;

  Obj := GetJSON(Texto) as TJSONObject;      { deserializar }
  WriteLn(Obj.Get('nombre', ''));
end;
```

Y Free Pascal tiene además algo que muy pocos lenguajes de esta página ofrecen: **serialización
automática por reflexión**, usando el `published` de la clase 087.

```pascal
uses fpjsonrtti;

type
  TPersona = class(TPersistent)
  private
    FNombre: string;
    FEdad: Integer;
  published                            { published -> genera RTTI }
    property Nombre: string read FNombre write FNombre;
    property Edad: Integer read FEdad write FEdad;
  end;

var S: TJSONStreamer;
begin
  WriteLn(S.ObjectToJSONString(Persona));    { sin escribir el mapeo }
end;
```

**`TJSONStreamer` recorre las propiedades `published` en tiempo de ejecución** y produce el JSON solo.
`TJSONDeStreamer` hace lo inverso.

Eso es posible porque `published` genera **información de tipos en tiempo de ejecución (RTTI)**, y esa
información existía desde 1995 para que el inspector de objetos del IDE pudiera editar los formularios
(clase 087). Es decir: **una característica creada para el diseñador visual acabó dando serialización
automática veinte años después**.

Es un ejemplo elegante de una capacidad que se construyó para una cosa y sirvió para otra, y explica
por qué el ecosistema Delphi adoptó JSON con tanta facilidad.
"""),
        "lisp": ("""
(let* ((linea (string-trim '(#\\Space #\\Return) (read-line)))
       (corte (position #\\Space linea))
       (nombre (subseq linea 0 corte))
       (edad (parse-integer (subseq linea (1+ corte)))))
  ;;  ~S imprime una cadena CON sus comillas: evita escaparlas a mano
  (format t "{~S: ~S, ~S: ~D}~%" "nombre" nombre "edad" edad))
""", """
**Lo que esta clase enseña en Common Lisp.** La directiva **`~S`** de `format` imprime un objeto **de
forma legible por `read`**, y para una cadena eso significa con sus comillas. Por eso este programa no
escapa nada: `~S` sobre `"nombre"` produce `"nombre"`.

Esa distinción entre `~A` y `~S` es una de las mejores ideas de la biblioteca:

```lisp
(format t "~A" "hola")     ; hola      -- para HUMANOS
(format t "~S" "hola")     ; "hola"    -- para READ
```

Es la misma que en Python separa `str()` de `repr()`, y viene de aquí.

Y lo que Lisp enseña de fondo en esta clase es que **ya tenía el problema resuelto antes de JSON**. La
propiedad de las clases 097 y 104 —imprimir una estructura y volver a leerla— es exactamente lo que
hace JSON, con treinta y cinco años de ventaja:

```lisp
'(:nombre "Ada" :edad 36)          ; una lista de propiedades
#S(PERSONA :NOMBRE "Ada" :EDAD 36) ; una estructura
```

Cualquiera de las dos se escribe en un fichero con `print` y se recupera con `read`. Es serialización
sin biblioteca, sin esquema y sin generador.

Con el aviso serio de la clase 104: **`read` ejecuta macros de lectura**, así que **nunca se debe usar
sobre datos no fiables**. JSON es deliberadamente un formato **sin poder de cómputo**, y esa es su
principal virtud frente a los formatos autoevaluables — una lección que se aprendió por las malas con
la deserialización de objetos en Java, Python y Ruby.

Para JSON de verdad, el ecosistema tiene varias opciones maduras:

```lisp
(ql:quickload :jonathan)
(jonathan:to-json '(:|nombre| "Ada" :|edad| 36))
(jonathan:parse "{\\"a\\": 1}")
```

`jzon`, `cl-json`, `shasht` y `jonathan` cubren el terreno, y la elección típica hoy es `jzon` por su
corrección con Unicode y números grandes.
"""),
        "tcl": ("""
gets stdin linea
lassign [split [string trim $linea]] nombre edad

puts [format {{"nombre": "%s", "edad": %d}} $nombre $edad]
""", """
**Lo que esta clase enseña en Tcl.** El truco sintáctico del programa merece explicación: **las llaves
de Tcl agrupan sin sustituir**, así que `{{"nombre": "%s", "edad": %d}}` pasa a `format` la cadena
literal `{"nombre": "%s", "edad": %d}` **sin escapar ninguna comilla**.

Es un ejemplo perfecto de la regla básica del lenguaje (clase 041): **las llaves protegen de todas las
sustituciones**, así que son la forma natural de escribir literales con caracteres especiales.

Y Tcl aporta a esta clase una observación que casi nadie hace: **el formato nativo de Tcl —la lista—
es más simple que JSON y hace casi lo mismo**.

```tcl
set datos {nombre Ada edad 36}
dict get $datos nombre
```

Esa cadena es a la vez el dato, su representación textual y algo que se puede escribir en un fichero y
volver a leer. Como Lisp, como Smalltalk, **Tcl ya tenía serialización antes de que hiciera falta un
formato para intercambiarla**.

La diferencia con JSON es la que importa: **la lista de Tcl no distingue tipos**. `36` es una cadena
que parece un número, y `{}` es a la vez lista vacía, cadena vacía y falso. Eso está bien dentro de
Tcl y es inaceptable al hablar con otro sistema — de ahí que JSON haga falta.

Para JSON real, Tcllib trae el paquete oficial:

```tcl
package require json
package require json::write

set d [json::json2dict $texto]
puts [json::write object nombre [json::write string "Ada"] edad 36]
```

Fíjate en que **hay que decir explícitamente que "Ada" es una cadena** con `json::write string`, y que
`36` sin envolver sale como número. Es la forma que tiene Tcl de recuperar la distinción de tipos que
su modelo no guarda, y es exactamente el trabajo que un lenguaje tipado hace solo.

Es el precio de "todo es una cadena", cobrado justo en la frontera con el exterior.
"""),
        "perl": ("""
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;
my ($nombre, $edad) = split ' ', $linea;

print '{"nombre": "', $nombre, '", "edad": ', $edad, "}\\n";
""", """
**Lo que esta clase enseña en Perl.** El programa usa **comillas simples** para el literal, porque en
Perl —como en el shell— las comillas simples no interpolan, así que las dobles de dentro son
literales. Es el mismo recurso que las llaves de Tcl.

Y Perl tiene JSON resuelto desde hace veinte años, con una lección de ecosistema que merece contarse:

```perl
use JSON::PP;                         # EN EL NÚCLEO desde Perl 5.14

my $texto = encode_json({ nombre => 'Ada', edad => 36 });
my $datos = decode_json($texto);
```

**`JSON::PP` está en el núcleo de Perl**, así que no hay que instalar nada. Y hay una variante en C,
`JSON::XS`, entre diez y cien veces más rápida — con el mismo interfaz, de modo que se puede cambiar
sin tocar el código. `JSON::MaybeXS` elige automáticamente la mejor disponible.

Ese patrón —**una implementación pura en Perl en el núcleo, una acelerada en C opcional, y un selector
que decide**— se repite por todo CPAN, y es una solución elegante al dilema entre portabilidad y
velocidad.

Perl tiene además una peculiaridad en esta clase que conviene conocer, porque muerde: **Perl no
distingue números de cadenas** (clase 101), así que el codificador tiene que adivinar.

```perl
my $x = "36";
encode_json({ n => $x });      # {"n":"36"}   -- CADENA
my $y = 36;
encode_json({ n => $y });      # {"n":36}     -- número
my $z = "36"; $z + 0;           # usarlo como número CAMBIA la representación interna
```

El codificador mira la representación interna del escalar, así que **el mismo valor puede salir como
número o como cadena según lo que se haya hecho antes con él**. Es una fuente conocida de sorpresas al
hablar con APIs estrictas, y la defensa es forzar el tipo explícitamente: `$x + 0` o `"$x"`.

Es exactamente el mismo problema que en Tcl, y por la misma causa.
"""),
        "cpp": ("""
#include <iostream>
#include <string>

int main() {
    std::string nombre;
    int edad{};
    if (!(std::cin >> nombre >> edad)) return 1;

    std::cout << "{\\"nombre\\": \\"" << nombre
              << "\\", \\"edad\\": " << edad << "}\\n";
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** Las barras invertidas del programa —`\\"`— son el escape de C
para meter una comilla en una cadena, y son la razón de que construir JSON a mano en C++ sea tan
incómodo de leer.

C++11 añadió las **cadenas crudas**, que lo resuelven y son poco conocidas:

```cpp
std::cout << R"({"nombre": ")" << nombre << R"(", "edad": )" << edad << "}\\n";
R"(cualquier cosa "con comillas" y \\barras)"
R"delim(incluso con )" dentro)delim"
```

`R"(...)"` no interpreta ningún escape, y el delimitador opcional permite incluir la secuencia de
cierre. Es lo que hace legibles las expresiones regulares y el JSON incrustado en C++.

Y **la biblioteca estándar no tiene JSON**, ni parece que vaya a tenerlo pronto. El ecosistema lo
cubre, y la opción dominante es **`nlohmann/json`**, cuya interfaz es célebre por parecer Python:

```cpp
#include <nlohmann/json.hpp>
using json = nlohmann::json;

json j;
j["nombre"] = "Ada";
j["edad"] = 36;
std::cout << j.dump() << '\\n';

json leido = json::parse(texto);
std::string n = leido["nombre"];
```

Y tiene una capacidad que aprovecha las plantillas de forma elegante: **la conversión automática a
tipos propios**.

```cpp
struct Persona { std::string nombre; int edad; };
NLOHMANN_DEFINE_TYPE_INTRUSIVE(Persona, nombre, edad)

json j = persona;              // serializa
Persona p = j.get<Persona>();  // y deserializa
```

Esa macro genera las funciones de conversión **en tiempo de compilación**, sin reflexión y sin coste
en ejecución. Es lo mismo que `#[derive(Serialize)]` en Rust.

Las alternativas cubren los extremos: `simdjson` analiza gigabytes por segundo usando instrucciones
vectoriales, y `RapidJSON` prioriza el uso de memoria. La elección depende de si el cuello de botella
es la comodidad o el rendimiento — que es la pregunta habitual en C++.

**Y C++26 traerá reflexión estática**, con lo que la serialización automática podrá escribirse sin
macros. Es probablemente el cambio más esperado del lenguaje.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi AJSON;
  entrada char(200) const;
end-pi;

dcl-s texto  varchar(200);
dcl-s nombre varchar(20);
dcl-s edad   int(10);
dcl-s corte  int(10);

texto  = %trimr(entrada);
corte  = %scan(' ' : texto);
nombre = %subst(texto : 1 : corte - 1);
edad   = %int(%subst(texto : corte + 1 : %len(texto) - corte));

dsply ('{"nombre": "' + nombre + '", "edad": ' + %char(edad) + '}');

*inlr = *on;
return;
""", """
**Lo que esta clase enseña en RPG.** Como COBOL, RPG **tiene JSON en el lenguaje**, y su solución es
de las más elegantes de esta página.

**`DATA-INTO`** (RPG 7.2, 2018) analiza un documento y **rellena una estructura de datos**:

```rpgle
dcl-ds persona qualified;
  nombre varchar(20);
  edad   int(10);
end-ds;

data-into persona %data(documentoJson) %parser('YAJLINTO');
```

**`DATA-GEN`** (RPG 7.4, 2019) hace lo inverso: **genera el documento desde la estructura**.

```rpgle
data-gen persona %data(salida : 'countprefix=len') %gen('YAJLDTAGEN');
```

Y aquí está el detalle de diseño que las hace especiales: **el analizador es un parámetro**.

`%parser('YAJLINTO')` nombra un **programa externo** que hace el análisis. IBM suministra uno para
JSON y otro para XML, y **cualquiera puede escribir el suyo** —los hay para CSV, para YAML y para
formatos propietarios—. La sentencia del lenguaje se ocupa de **emparejar el resultado con la
estructura de datos**, que es la parte difícil y repetitiva; el formato concreto es intercambiable.

Es una separación de responsabilidades muy limpia, y no la tiene ningún otro lenguaje de esta página:
en todos los demás, el analizador y el mapeo van juntos en la misma biblioteca.

Y como en COBOL, esto no es un adorno: es lo que permite que un programa RPG de los años noventa
**exponga y consuma APIs REST** sin reescribirse. Con `HTTPAPI` o las funciones SQL `HTTP_GET` de Db2
for i, un programa RPG llama a un servicio web, recibe JSON, lo mete en una estructura de datos con
`DATA-INTO` y sigue con su lógica de siempre.

Es la modernización por los bordes en su forma más directa.
"""),
        "pli": ("""
 ajson: procedure options(main);

    declare linea  char(200) varying;
    declare nombre char(20)  varying;
    declare corte  fixed binary(31);
    declare edad   fixed binary(31);

    get edit (linea) (a(200));
    linea = trim(linea);

    corte  = index(linea, ' ');
    nombre = substr(linea, 1, corte - 1);
    edad   = substr(linea, corte + 1);

    put skip list ('{"nombre": "' || nombre ||
                   '", "edad": ' || trim(char(edad)) || '}');

 end ajson;
""", """
**Lo que esta clase enseña en PL/I.** PL/I es, en esta clase, el lenguaje que peor ha envejecido de
los cuatro grandes del mainframe, y conviene decirlo sin adornos: **el estándar no tiene JSON, y no
hay una biblioteca estándar que lo dé**.

Lo que sí hay son tres caminos, y los tres se usan en producción:

**El primero es lo que hace este programa**: construir el texto con `||`. Con `varying` y `trim` sale
razonablemente limpio, y sirve para generar. Para **analizar** JSON a mano en PL/I —contando llaves,
corchetes y comillas— el resultado es un programa largo y frágil.

**El segundo es delegar en otro lenguaje del mismo sistema.** En z/OS conviven PL/I, COBOL, C y Java
en el mismo espacio de direcciones, así que un programa PL/I puede **llamar a un módulo COBOL que use
`JSON PARSE`** y recibir la estructura ya rellena. Es feo de explicar y funciona perfectamente, y es
la solución habitual.

**El tercero es z/OS Connect**, que expone el programa PL/I como API REST **sin tocarlo**: la
plataforma traduce el JSON entrante a la estructura de parámetros que el programa espera, y la salida
de vuelta.

Ese tercer camino es el importante y es el que conviene subrayar, porque relativiza la carencia: **si
la traducción la hace la plataforma, el lenguaje no necesita saber JSON**. El programa PL/I sigue
recibiendo una estructura con campos, que es lo que siempre supo manejar.

Lo que sí tiene Enterprise PL/I moderno son las piezas que hacen esto posible: soporte de XML,
llamadas a Java y a C, tipos `widechar` para Unicode, y `define structure` para declarar tipos con
nombre (clase 099).

Es la modernización mínima de esta página, y es honesto reconocerlo: **PL/I se mantiene compilando,
no evolucionando**.
"""),
        "mumps": ("""
AJSON ; JSON -- clase 105
 read linea
 set nombre = $piece(linea, " ", 1)
 set edad = $piece(linea, " ", 2)
 set q = $char(34)                       ; la comilla doble
 write "{", q, "nombre", q, ": ", q, nombre, q
 write ", ", q, "edad", q, ": ", edad, "}", !
 quit
""", """
**Lo que esta clase enseña en M.** El programa construye la comilla con **`$char(34)`** porque en M
las cadenas van entre comillas dobles y meter una dentro exige duplicarla —`""`—, lo que con muchas
seguidas se vuelve ilegible. Es el mismo problema que en Ada y en Pascal.

Y aquí M tiene la historia de modernización más interesante de toda esta parte, porque es la más
necesaria: **los historiales clínicos tenían que hablar el idioma del resto del mundo o quedarse
fuera**.

El resultado es **FHIR** —*Fast Healthcare Interoperability Resources*—, el estándar de intercambio
sanitario actual, que **es JSON**. Y las plataformas M lo implementan de forma nativa:

- **InterSystems IRIS for Health** tiene un servidor FHIR completo, con `%JSON.Adaptor` para convertir
  clases a JSON y de vuelta, y objetos `%DynamicObject` que se manipulan con sintaxis parecida a
  JavaScript.
- **YottaDB** tiene enlaces con Node.js, Python y Go, así que la capa REST se escribe en el lenguaje
  que convenga sobre los mismos *globals*.
- **VistA** expone sus datos por FHIR a través de pasarelas que traducen entre FileMan (clase 099) y
  los recursos del estándar.

En IRIS, el código se parece a esto:

```objectscript
set obj = {"nombre": "Ada", "edad": 36}        // literal JSON en el LENGUAJE
write obj.nombre
set texto = obj.%ToJSON()
set otro = {}.%FromJSON(texto)
```

**Literales JSON en la sintaxis del lenguaje**, en un descendiente directo de un lenguaje de 1966. Es
probablemente la modernización más agresiva de esta página.

Y hay una razón de fondo por la que encajó tan bien, y merece cerrar con ella: **el modelo de datos de
M ya era jerárquico y sin esquema**. Un *global* con subíndices anidados y un documento JSON son la
misma forma de pensar los datos. M no tuvo que cambiar su modelo para hablar JSON — **solo tuvo que
aprender a escribirlo**.
"""),
        "smalltalk": ("""
| partes nombre edad |

partes := stdin nextLine substrings.
nombre := partes first.
edad := (partes at: 2) asNumber.

Transcript
    show: '{"nombre": "', nombre, '", "edad": ', edad printString, '}';
    cr.
""", """
**Lo que esta clase enseña en Smalltalk.** El literal del programa va entre **comillas simples**,
porque en Smalltalk **las comillas dobles delimitan comentarios**:

```smalltalk
'una cadena'          "un comentario"
```

Es al revés que en casi todos los lenguajes, y por eso las comillas dobles del JSON no necesitan
escaparse dentro de una cadena.

Y como Lisp y Tcl, Smalltalk **ya tenía este problema resuelto**: `storeString` produce una
representación **que el propio sistema puede volver a evaluar**.

```smalltalk
#(1 2 3) storeString              "((Array new: 3) at: 1 put: 1; ...; yourself)"
'hola' storeString                 "'hola'"
36 storeString                      "36"
```

Es la distinción `printString` / `storeString`, que es la misma que `~A` / `~S` en Lisp y `str` /
`repr` en Python — y otra vez, **el original está aquí**.

Para JSON de verdad, Pharo trae varias opciones en la imagen base:

```smalltalk
| json |
json := STONJSON toString: (Dictionary newFrom: { #nombre -> 'Ada'. #edad -> 36 }).
STONJSON fromString: json.

NeoJSONWriter toString: unObjeto.
NeoJSONReader fromString: texto.
```

**STON** es especialmente interesante: es el formato nativo de Pharo —*Smalltalk Object Notation*— y
es **un superconjunto de JSON**. Todo JSON es STON válido, y STON añade lo que a JSON le falta para
serializar objetos de verdad: **nombres de clase, referencias compartidas y ciclos**.

```text
Persona { #nombre: 'Ada', #edad: 36 }
```

Esa última capacidad —**referencias y ciclos**— es la que hace que STON pueda guardar un grafo de
objetos y JSON no, y conecta con la clase 102: **serializar un grafo requiere lo mismo que copiarlo en
profundidad, un registro de lo ya visto**.

Es un buen final para esta clase: JSON es simple porque **renunció a representar identidad**, y esa
renuncia es a la vez su mayor virtud y su límite.
"""),
    },
)
