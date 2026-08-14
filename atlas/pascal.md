# 📘 Pascal — 1970

> [⬅️ Atlas](README.md) · [🧟 Lenguajes que siguen vivos](vivos.md) · [📚 Índice de clases](../classes/README.md)

**El lenguaje diseñado para enseñar a programar bien.** Niklaus Wirth lo escribió como una tesis
sobre cómo debía ser un lenguaje: pequeño, ordenado, con tipos fuertes y sin trampas. Millones de
programadores aprendieron con él, y su influencia está en la sintaxis de media docena de lenguajes
posteriores que probablemente sí usas.

> **🎯 Por qué está en este programa**
>
> **Criterio de inclusión: Pascal se ejecuta hoy**, principalmente a través de sus dos descendientes
> vivos: **Free Pascal** (compilador libre y multiplataforma, con el IDE **Lazarus**) y
> **[Delphi](delphi.md)** (comercial y en desarrollo activo). El Pascal ISO clásico es minoritario;
> la línea Object Pascal es un negocio en marcha.
>
> Entra porque **es el origen documentado de ideas que el núcleo da por sentadas y ya no explica**:
> el tipado fuerte con conversiones explícitas, los **tipos definidos por el usuario** (enumerados,
> subrangos, registros), y la separación limpia entre declaración y ejecución. Cuando en la
> [Parte 3](../classes/parte-3-valores-tipos-y-variables/README.md) se estudia por qué `:=` no es
> `=`, o por qué un `enum` de Rust es distinto de un entero, se está estudiando una decisión que Wirth
> tomó en 1970 y argumentó por escrito. Leer Pascal es leer el razonamiento original.

| | |
|---|---|
| **Año** | 1970; estándar **ISO 7185** en 1983; **Extended Pascal** ISO 10206 en 1990 |
| **Autoría** | **Niklaus Wirth**, ETH de Zúrich |
| **Familia** | ALGOL — descendiente directo de **ALGOL W**, también de Wirth |
| **Paradigma** | Imperativo, procedimental y **estructurado** |
| **Tipado** | **Estático y fuerte**, con subrangos y enumerados comprobados |
| **Memoria** | Pila y montículo explícito (`New` / `Dispose`) |
| **Ejecución** | Compilado a nativo; históricamente a **P-code** para portabilidad |
| **Estado** | 🟡 **El Pascal clásico es minoritario; su rama Object Pascal está muy viva** |

---

## 📜 Historia

**Niklaus Wirth** participó en el comité de ALGOL 68 y se marchó en desacuerdo: consideraba que el
lenguaje se estaba volviendo demasiado grande y complejo para lo que aportaba. Su propuesta rechazada,
**ALGOL W**, se convirtió en la semilla de lo que en 1970 publicó como **Pascal**, en honor a Blaise
Pascal.

El objetivo era doble y explícito: **enseñar programación estructurada** y demostrar que un lenguaje
podía ser potente siendo pequeño. Wirth dedicó su carrera a esa tesis y la resumió en una frase que
sigue citándose: *"hacer las cosas lo más simples posible, pero no más simples"*. Escribió también la
**Ley de Wirth** —"el software se vuelve más lento más deprisa de lo que el hardware se vuelve más
rápido"— que ha envejecido de forma incómodamente buena.

Pascal introdujo o consolidó cosas que hoy son evidentes y entonces no lo eran:

- **Tipos definidos por el usuario**: enumerados (`type Color = (Rojo, Verde, Azul)`), **subrangos**
  (`type Nota = 1..7`) y registros. Un enumerado de Pascal **no es un entero**: no se le puede sumar,
  y esa restricción es el punto.
- **Punteros con tipo**, en lugar de direcciones sin más.
- **Sintaxis de declaración separada** de la ejecución, con `var`, `const` y `type` en secciones
  propias.
- **`:=` para asignar y `=` para comparar**, distinción que Ada, Go (`:=`) y muchos otros heredaron
  precisamente para evitar el clásico `if (x = 5)` de C.

**El truco de la portabilidad.** El compilador de Zúrich no generaba código máquina: generaba
**P-code**, un bytecode para una máquina virtual imaginaria. Para llevar Pascal a un ordenador nuevo
bastaba con escribir un intérprete de P-code. **UCSD Pascal** llevó esa idea al mercado en los 70 y
consiguió que el mismo software corriera en máquinas incompatibles. Es exactamente el modelo que
Java popularizó veinte años después con la JVM y el bytecode.

En 1983 **Borland** lanzó **Turbo Pascal**: un compilador y un editor en un solo programa, que cabía
en un disquete, compilaba en segundos y costaba 49,95 dólares cuando la competencia pedía cientos. Fue
un fenómeno, y su descendiente directo es [Delphi](delphi.md).

Wirth siguió adelante con **Modula-2** (1978, con módulos de verdad) y **Oberon** (1986, aún más
pequeño). Ninguno alcanzó la difusión de Pascal, pero Modula-2 influyó en el sistema de módulos de
casi todo lo que vino después. Wirth murió en enero de 2024.

## 🏭 Dónde sobrevive hoy

- **A través de [Delphi](delphi.md) y Free Pascal/Lazarus**: aplicaciones de escritorio, ERP, TPV,
  software industrial. Ahí está el grueso del Pascal en producción.
- **Educación**: sigue usándose en enseñanza secundaria y primeros cursos universitarios en varios
  países, precisamente porque fue diseñado para eso.
- **Competición de programación**: fue durante décadas uno de los lenguajes admitidos en olimpiadas
  de informática, y aún hay comunidades que lo usan por la velocidad de compilación.
- **Aplicaciones heredadas** de los 80 y 90 en administración, laboratorios e industria.

## 🧠 Por qué no ha muerto

**1. Su descendiente es un producto comercial vivo.** El Pascal ISO puro es una pieza de museo, pero
Object Pascal no. Ver [Delphi](delphi.md).

**2. Compila absurdamente rápido.** El diseño del lenguaje —una sola pasada, declaraciones antes del
uso, sin preprocesador— permite compiladores que procesan cientos de miles de líneas por segundo. Free
Pascal y Delphi siguen siendo de los compiladores más rápidos que existen, y quien viene de esperar
minutos con C++ o Rust lo nota de inmediato.

**3. Es genuinamente bueno para enseñar.** Fuerza a declarar antes de usar, distingue asignación de
comparación, no permite conversiones silenciosas y su sintaxis se lee en voz alta. Los errores que
un principiante comete en C —confundir `=` con `==`, desbordar un array, olvidar un tipo— en Pascal
son errores de compilación.

**4. Free Pascal es un compilador serio.** Multiplataforma real (Windows, Linux, macOS, Android,
Raspberry Pi, incluso microcontroladores), compatible con la sintaxis de Delphi, libre y mantenido.

## 🔄 Lo que se ha modernizado

El Pascal ISO de 1983 sí está congelado. **Free Pascal, que es donde vive el lenguaje, no**:

- **Genéricos, sobrecarga de operadores, métodos anónimos (*closures*), interfaces, ayudantes de tipo
  y `for..in`** — todo lo que se espera de un lenguaje actual.
- **Multiplataforma real**: x86, x86-64, ARM, **AArch64**, **RISC-V**, MIPS, PowerPC; Windows, Linux,
  macOS (incluida Apple Silicon), FreeBSD, **Android**, y hasta microcontroladores AVR y ARM
  Cortex-M sin sistema operativo.
- **WebAssembly**: FPC tiene un generador de código para **wasm**, así que el mismo Pascal puede
  ejecutarse en el navegador.
- **Compatibilidad con el dialecto de Delphi** (`-Mdelphi`), suficiente para compilar proyectos
  comerciales completos con un compilador libre.
- **Lazarus** ofrece el diseñador visual, depurador integrado y un gestor de paquetes en línea.
- **Velocidad de compilación** que sigue siendo de las mejores del mercado — un rasgo del diseño
  original de Wirth que hoy vuelve a valorarse.

## ⚙️ Cómo se ejecuta hoy

```bash
sudo apt-get install -y fpc

fpc -Mobjfpc total_venta.pas
echo "15000 2 0.10" | ./total_venta
# Total: 27000.00
```

**Implementaciones:** **Free Pascal (FPC)** es la libre y la más completa; **Lazarus** es su IDE con
diseñador visual de formularios, clon libre del de Delphi. **[Delphi](delphi.md)** de Embarcadero es
la comercial. **GNU Pascal** existe pero lleva años sin desarrollo activo.

**Modos de compilación de FPC**, que hay que conocer porque cambian el lenguaje: `-Mfpc` (dialecto
propio), `-Mobjfpc` (Object Pascal con extensiones propias, el recomendado), `-Mdelphi`
(compatibilidad con Delphi), `-Miso` (ISO 7185 estricto).

## 🧪 El programa de la clase 041 en Pascal

```pascal
program TotalVenta;
{$MODE OBJFPC}{$H+}

var
  Precio, Cantidad, Descuento, Total: Double;

begin
  Read(Precio, Cantidad, Descuento);

  Total := Precio * Cantidad * (1 - Descuento);

  WriteLn('Total: ', Total:0:2);
end.
```

**Recorrido, línea a línea.**

- `program TotalVenta;` nombra el programa. En el Pascal ISO era obligatorio y llevaba además la lista
  de ficheros externos (`program X(input, output);`); FPC lo acepta sin ella.
- `{$MODE OBJFPC}` es una **directiva de compilador** —van entre llaves con `$`, y sí, ocupan el mismo
  espacio sintáctico que los comentarios—. Selecciona el dialecto. `{$H+}` hace que `string` sea de
  longitud dinámica en lugar del `ShortString` de 255 caracteres heredado de Turbo Pascal.
- **La sección `var` va antes del cuerpo, y eso no es negociable.** Pascal exige declarar todo antes de
  usarlo, en su sitio. Es la restricción que más molesta a quien viene de lenguajes modernos y es,
  literalmente, la razón por la que el compilador puede trabajar en una sola pasada y ser tan rápido.
- `begin` … `end.` delimita el bloque principal. El **punto final** tras el último `end` marca el fin
  del programa; los `end` internos llevan punto y coma. Olvidarlo es el error de sintaxis clásico.
- `:=` asigna. `=` compara. La separación es deliberada y es una de las mejores decisiones de diseño
  del lenguaje: en Pascal es **imposible** escribir por accidente el bug de `if (x = 5)` de C.
- `Read(Precio, Cantidad, Descuento)` lee tres reales separados por espacios o saltos de línea. La E/S
  está **en el lenguaje**, no en una biblioteca: `Read`, `ReadLn`, `Write` y `WriteLn` aceptan un
  número variable de argumentos de tipos distintos, algo que ninguna función normal de Pascal puede
  hacer. Son casos especiales del compilador.
- **`Total:0:2` es el detalle que hay que llevarse.** En un `Write`, la sintaxis `valor:ancho:decimales`
  formatea directamente: ancho mínimo 0 (sin relleno), 2 decimales. Es formateo integrado en la
  sintaxis, sin cadena de plantilla, sin `printf` y **sin depender de la configuración regional**.
  Para el caso `0.0` produce `0.00`, que es justo lo que otros lenguajes complican.

**Y ahora el Pascal que merece la pena ver**, el de los tipos:

```pascal
type
  TDia       = (Lunes, Martes, Miercoles, Jueves, Viernes, Sabado, Domingo);
  TLaborable = Lunes..Viernes;              { subrango: un tipo con límites }
  TVenta = record
    Producto : string[40];
    Unidades : 1..9999;                     { el rango es parte del tipo }
    Importe  : Double;
  end;

var
  Hoy   : TDia;
  Venta : TVenta;
begin
  Hoy := Miercoles;
  { Hoy := Hoy + 1;   <-- no compila: un enumerado no es un entero }
  Hoy := Succ(Hoy);   { esta es la forma correcta }

  Venta.Unidades := 0;  { con {$R+} activo, esto es un error en ejecución }
end.
```

Un enumerado de Pascal **no** es un entero disfrazado: no se le puede sumar, y `Succ`/`Pred` son las
operaciones legítimas. Un subrango `1..9999` es un tipo cuyo dominio comprueba el compilador cuando
puede y el runtime cuando no (con `{$R+}`). Compara con `enum` de C, que sí es un entero y admite
cualquier valor. Esa diferencia —el tipo como afirmación sobre los valores posibles, no solo sobre
el tamaño en bytes— es la línea recta que va de Pascal a [Ada](ada.md), y de ahí a los tipos suma de
Rust y a los tipos literales de TypeScript.

## 🔍 Qué reconocer si vienes de otro lenguaje

| Si conoces… | En Pascal es… |
|---|---|
| `int x = 5;` | `var x: Integer;` … `x := 5;` |
| `==` | `=`; y la asignación es `:=` |
| `!=` | `<>` |
| `&&` / `\|\|` / `!` | `and` / `or` / `not` |
| `{ ... }` | `begin ... end` |
| `// comentario` | `{ comentario }` o `(* comentario *)`; FPC acepta `//` |
| `struct` | `record` |
| `enum` | `type T = (A, B, C);` — y **no** es un entero |
| `typedef unsigned char` | `type TNota = 1..7;` — subrango comprobado |
| `void f()` / `int f()` | `procedure f;` / `function f: Integer;` |
| `return x` | `Result := x;` (Object Pascal) o `NombreFuncion := x;` (clásico) |
| `malloc` / `free` | `New(p)` / `Dispose(p)` |
| `printf("%.2f", x)` | `Write(x:0:2)` |

## ⚠️ Errores comunes al leerlo

- **El punto final.** `end.` cierra el programa; `end;` cierra un bloque. Confundirlos es el primer
  error de todo el mundo.
- **Punto y coma antes de `else`.** `if c then a; else b;` no compila: el `;` **termina** la sentencia
  `if` y deja el `else` huérfano. Es la trampa sintáctica más famosa del lenguaje.
- **Declarar en medio del código.** No se puede. Toda variable va en la sección `var` del bloque.
- **Suponer evaluación en cortocircuito.** Depende del modo del compilador (`{$B-}` la activa, que es
  lo habitual, pero el ISO no la garantiza). Conviene no depender de ella al leer código antiguo.
- **Confundir `ShortString` con `string`.** Sin `{$H+}`, `string` es de 255 caracteres como máximo,
  herencia de Turbo Pascal. Con `{$H+}`, es dinámico con conteo de referencias.
- **Índices arbitrarios.** `array[1..10]` empieza en 1, pero `array[-5..5]` y `array['a'..'z']` son
  perfectamente legales. El array lleva sus límites en el tipo.

## 📚 Fuentes y bibliografía

- [Free Pascal](https://www.freepascal.org/) — compilador libre, con la referencia del lenguaje y de
  la biblioteca en línea.
- [Lazarus IDE](https://www.lazarus-ide.org/) — el entorno visual libre.
- [Free Pascal — Reference Guide](https://www.freepascal.org/docs.html) — la documentación que
  usarás a diario.
- **Niklaus Wirth**, *Algorithms + Data Structures = Programs*, Prentice Hall, 1976 — uno de los
  libros fundacionales de la disciplina; el título es una tesis y el lenguaje de los ejemplos es
  Pascal. Sigue siendo excelente.
- **Niklaus Wirth**, *The Programming Language Pascal*, Acta Informatica, 1971 — el artículo original;
  merece la pena leer el razonamiento de diseño de primera mano.
- **Kathleen Jensen, Niklaus Wirth**, *Pascal User Manual and Report* — el documento de referencia
  clásico.
- **Marco Cantù**, *Object Pascal Handbook* — para el salto al Pascal moderno; ver
  [Delphi](delphi.md).

---

⏮️ [Volver al Atlas](README.md) · 🧟 [Los lenguajes que siguen vivos](vivos.md) ·
🔗 Relacionadas: [Delphi / Object Pascal](delphi.md) · [Ada](ada.md) · [C](c.md)
