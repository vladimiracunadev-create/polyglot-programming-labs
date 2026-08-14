# 🐪 Perl — 1987

> [⬅️ Atlas](README.md) · [🧟 Lenguajes que siguen vivos](vivos.md) · [📚 Índice de clases](../classes/README.md)

**La cinta adhesiva de Internet.** Durante los años 90, buena parte de la web dinámica del planeta
funcionaba con guiones CGI en Perl. Esa época pasó, pero Perl no: sigue procesando texto,
administrando sistemas y secuenciando genomas, con una nueva versión estable cada año.

> **🎯 Por qué está en este programa**
>
> **Criterio de inclusión: Perl 5 se mantiene activamente y publica una versión estable anual**; la
> documentación vigente corresponde a la serie 5.44. Viene instalado en prácticamente cualquier
> sistema Unix o Linux, sostiene herramientas que se usan a diario (`git send-email`, Bugzilla,
> cPanel, buena parte de la infraestructura de Debian) y sigue siendo dominante en bioinformática.
>
> Entra porque **muestra dos conceptos que el núcleo no expresa bien**. El primero: las **expresiones
> regulares como parte de la sintaxis del lenguaje**, no como una biblioteca. Perl las integró tan a
> fondo que definió el estándar de facto —**PCRE**, *Perl Compatible Regular Expressions*— que hoy
> usan Python, JavaScript, PHP, Java, Go y casi todos los demás. Cuando escribes una regex en
> cualquier lenguaje, estás escribiendo Perl. El segundo: el **contexto**, un concepto que casi no
> existe fuera de aquí: en Perl **la misma expresión devuelve cosas distintas según dónde se use**,
> y entenderlo enseña a mirar con otros ojos la evaluación de expresiones.
>
> Perl ya aparece resuelto en cada [`primos.md`](../classes/parte-3-valores-tipos-y-variables/041-literales-valores-variables-y-constantes/primos.md)
> del programa y **se ejecuta en CI**; esta ficha es su historia y su porqué.

| | |
|---|---|
| **Año** | 18 de diciembre de 1987 (Perl 1.0); **Perl 5** desde 1994 |
| **Autoría** | **Larry Wall** — lingüista de formación, y se nota en el diseño |
| **Familia** | Scripting dinámico; influencias de C, `sed`, `awk`, shell y Lisp |
| **Paradigma** | Multiparadigma: procedimental, funcional y OO |
| **Tipado** | **Dinámico**, con *sigilos* que marcan la forma del dato (`$`, `@`, `%`) |
| **Memoria** | Conteo de referencias |
| **Ejecución** | Compilado a un árbol interno en cada arranque y ejecutado |
| **Estado** | 🟡 **Mantenido y en uso** — administración, texto, bioinformática, sistemas heredados |

---

## 📜 Historia

En 1987 **Larry Wall** trabajaba como administrador de sistemas y programador en un proyecto que
necesitaba generar informes a partir de árboles de ficheros de texto. Las herramientas disponibles no
le servían: `awk` no manejaba bien ficheros ni estructuras complejas, `sed` era demasiado limitado, el
shell era frágil y C era demasiado ceremonioso para un guion. Escribió **Perl** para cubrir ese hueco
concreto, y lo publicó en el grupo de noticias `comp.sources.unix` el 18 de diciembre de 1987.

Wall es **lingüista** de formación, y eso explica la filosofía del lenguaje mejor que cualquier
decisión técnica. Sus dos lemas son deliberadamente contrarios a la corriente:

- **TMTOWTDI** — *There's More Than One Way To Do It*. Frente al "debería haber una forma obvia" de
  Python, Perl asume que los lenguajes naturales tienen sinónimos y registros, y que quien escribe
  elige el que mejor comunica su intención.
- **"Perl facilita lo fácil y hace posible lo difícil."**

**Perl 5**, en 1994, fue la reescritura que lo convirtió en un lenguaje serio: referencias (y con
ellas estructuras de datos anidadas), módulos, paquetes y orientación a objetos mediante `bless`. Un
año después nació **CPAN**, el *Comprehensive Perl Archive Network*, que fue **el primer gran
repositorio de módulos de la historia** — el antepasado directo de PyPI, npm, RubyGems y crates.io.

A finales de los 90, Perl era el lenguaje de la web: los guiones CGI en `cgi-bin` eran Perl casi por
definición. Ese dominio se perdió frente a PHP, y luego frente a Python y Ruby.

**El episodio Perl 6.** Anunciado en el año 2000 como el rediseño total del lenguaje, se convirtió en
uno de los desarrollos más largos de la historia del software. Durante quince años la comunidad
quedó dividida entre un Perl 5 que "iba a ser sustituido" y un Perl 6 que no llegaba. Cuando por fin
se estabilizó, era tan distinto que en **2019 se renombró como [Raku](https://raku.org/)** y se
declaró un lenguaje aparte. Perl 5 recuperó su nombre y su cadencia anual de versiones. La lección
—el coste de anunciar un sucesor que no llega— es de las más citadas en gestión de proyectos de
lenguajes, y conviene tenerla presente al estudiar cualquier migración mayor.

## 🏭 Dónde sobrevive hoy

- **Administración de sistemas Unix/Linux**: viene preinstalado, siempre está ahí, y procesa registros
  y configuraciones sin instalar nada.
- **Bioinformática**: **BioPerl** fue durante años la biblioteca de referencia para manipular
  secuencias genómicas, y sigue habiendo mucha canalización de datos científica en Perl.
- **Infraestructura conocida**: **`git send-email`** y varias utilidades de Git son guiones Perl;
  **Bugzilla**, **cPanel/WHM** (el panel de hosting más extendido) y el sistema de gestión de paquetes
  de Debian dependen de él.
- **Empresas de gran escala** con base histórica en Perl, siendo **Booking.com** el caso más
  documentado públicamente.
- **Procesamiento de texto y ETL** en general: sigue siendo excepcionalmente bueno en ello.

## 🧠 Por qué no ha muerto

**1. Las regex son parte del lenguaje.** `if ($linea =~ /^(\w+)\s+(\d+)$/)` no llama a una función:
`=~` es un operador, `/.../` es literal de patrón, y `$1`, `$2` aparecen automáticamente. En Python
o Java hay que importar un módulo, compilar el patrón y consultar un objeto de coincidencia. Para
trabajo de texto intenso, la diferencia de densidad es enorme.

**2. CPAN sigue siendo excepcional.** Decenas de miles de distribuciones, con una cultura de pruebas
inusualmente rigurosa: **CPAN Testers** ejecuta automáticamente la batería de pruebas de cada módulo
en decenas de combinaciones de sistema operativo y versión de Perl, y publica los resultados. Pocos
ecosistemas tienen algo comparable.

**3. Compatibilidad hacia atrás casi obsesiva.** Un guion de 1998 sigue funcionando. Cuando el
lenguaje ha querido cambiar algo, lo ha hecho tras `use feature` o `use v5.36`, sin romper lo
existente. Perl no tuvo su ruptura 2→3.

**4. Ubicuidad.** Está en cualquier sistema tipo Unix. Para un administrador que no puede instalar
nada en una máquina ajena, eso lo convierte en la única opción.

## 🔄 Lo que se ha modernizado

El Perl que se escribe hoy no es el de los guiones CGI de 1998:

- **Firmas de subrutina** estables desde 5.36: `sub total ($precio, $cantidad, $descuento) { ... }`,
  en lugar del clásico `my (...) = @_;`.
- **`try`/`catch`/`finally`** como sintaxis del lenguaje (5.34–5.40), en vez del idioma
  `eval { }; if ($@)` que era fácil de escribir mal.
- **Clases nativas.** La palabra clave `class` con `field` y `method` (el proyecto *Corinna*) está
  entrando en el lenguaje desde 5.38 como característica experimental: orientación a objetos de
  verdad, en lugar del `bless` sobre un hash.
- **`use v5.40`** activa de golpe el conjunto de características modernas —`say`, firmas,
  `try/catch`, `strict`, `warnings`— con una sola línea.
- **Una versión estable al año**, con la serie 5.44 como documentación vigente, y compatibilidad hacia
  atrás mantenida a rajatabla.
- **Ecosistema actual**: **Carton** y **cpanfile** para dependencias fijadas por proyecto,
  **Perl::Critic** para análisis estático, **Mojolicious** y **Dancer2** como marcos web modernos con
  soporte asíncrono y WebSockets, y **PDL** para cálculo numérico vectorizado.

## ⚙️ Cómo se ejecuta hoy

```bash
perl --version          # ya está instalado en Linux y macOS

perl total.pl < entrada.txt
echo "15000 2 0.10" | perl total.pl
# Total: 27000.00

# Como una sola línea, que es donde Perl brilla:
perl -ne 'print if /ERROR/' registro.log
perl -pi -e 's/viejo/nuevo/g' *.conf
```

**Ecosistema:** **`cpanm`** (`cpanminus`) para instalar módulos, **Carton** para fijar versiones por
proyecto (equivalente a un *lockfile*), **perlbrew** o **plenv** para gestionar varias versiones del
intérprete, y **Perl::Critic** y **perltidy** para estilo y análisis estático. La documentación
completa está en la propia máquina: `perldoc perlre`, `perldoc -f split`.

## 🧪 El programa de la clase 041 en Perl

```perl
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;

my ($precio, $cantidad, $descuento) = split ' ', $linea;
my $total = $precio * $cantidad * (1 - $descuento);

printf "Total: %.2f\n", $total;
```

**Recorrido, línea a línea.**

- `use strict; use warnings;` son las **dos primeras líneas de cualquier Perl escrito después de
  1995**, y su ausencia es la mejor señal de que estás ante código antiguo o descuidado. `strict`
  obliga a declarar las variables (sin él, un nombre mal tecleado crea una variable global nueva en
  silencio) y `warnings` avisa de usos sospechosos.
- `my` declara una variable **de ámbito léxico**, el equivalente a `let` de JavaScript.
- **Los *sigilos*** son la marca de la casa: `$` para un **escalar** (un valor), `@` para una
  **lista**, `%` para un **hash**. El sigilo no describe el tipo del dato sino la **forma en que lo
  estás usando**, que es una idea distinta y desconcertante al principio: `$lista[0]` lleva `$` —no
  `@`— porque un elemento suelto de la lista *es* un escalar.
- `<STDIN>` lee del canal de entrada. Y aquí aparece **el contexto**, el concepto más específicamente
  perlero: en **contexto escalar** (`my $linea = <STDIN>`) devuelve **una línea**; en **contexto de
  lista** (`my @todo = <STDIN>`) devuelve **todas las líneas**. La misma expresión, dos resultados,
  según lo que espere el lado izquierdo. Lo mismo ocurre con un array: `my $n = @lista` da el número
  de elementos, porque un array en contexto escalar es su longitud.
- `chomp` elimina el salto de línea final. **Es obligatorio y se olvida siempre.** En este programa
  el resultado saldría bien igualmente porque el `\n` desaparece al convertir a número, pero en
  cuanto se compara texto —`if ($palabra eq "Ada")`— la cadena mide un carácter de más y la
  comparación falla sin dar ningún error. Es exactamente el defecto que se encontró al ejecutar por
  primera vez los primos de este repositorio en CI.
- `split ' ', $linea` usa el **patrón mágico de un solo espacio**: no significa "parte por el carácter
  espacio", significa "parte por rachas de espacios en blanco e ignora los iniciales". Es un caso
  especial documentado, heredado de `awk`, y es lo que hace que funcione con entradas mal alineadas.
- La asignación a `my ($a, $b, $c) = ...` es **desestructuración**, treinta años antes de que
  JavaScript la incorporara.
- `printf "%.2f"` es el mismo formato de C, porque Perl viene de ahí.

**Y ahora lo que hace de Perl lo que es.** El procesamiento de texto:

```perl
while (my $linea = <STDIN>) {
    next unless $linea =~ /^(\d{4})-(\d{2})-(\d{2})\s+(\w+)\s+(\d+)$/;
    my ($anio, $mes, $dia, $producto, $unidades) = ($1, $2, $3, $4, $5);
    $ventas{$producto} += $unidades;
}
printf "%-15s %6d\n", $_, $ventas{$_} for sort keys %ventas;
```

Ocho líneas que analizan un registro con formato, validan cada fila contra un patrón, agregan por
clave y emiten un informe ordenado. `next unless` es un modificador de sentencia —la condición va
detrás, porque así se lee mejor en voz alta, decisión típicamente lingüística de Wall—, `$1..$5` son
las capturas del patrón, `%ventas` es un hash que se crea solo al usarlo, y `for sort keys %ventas`
al final es otro modificador. Reproducir esto en cualquier lenguaje del núcleo cuesta el doble de
líneas. **Ese es el nicho donde Perl sigue siendo la mejor herramienta.**

## 🔍 Qué reconocer si vienes de otro lenguaje

| Si conoces… | En Perl es… |
|---|---|
| `x = 5` | `my $x = 5;` |
| Lista / array | `my @a = (1, 2, 3);` y el elemento es `$a[0]` |
| Diccionario | `my %h = (clave => 'valor');` y el elemento es `$h{clave}` |
| `len(a)` | `scalar @a` — o simplemente `@a` en contexto escalar |
| `re.match(p, s)` | `$s =~ /p/` — operador, no función |
| `s.replace(a, b)` | `$s =~ s/a/b/g;` |
| `a.split(",")` | `split /,/, $a` |
| `"".join(a)` | `join '', @a` |
| `def f(a, b):` | `sub f { my ($a, $b) = @_; ... }` — los argumentos llegan en `@_` |
| `try / except` | `eval { ... }; if ($@) { ... }` — o `Try::Tiny` de CPAN |
| `import modulo` | `use Modulo;` |
| Referencia / puntero | `\@lista`, `\%hash`, y se accede con `->` |

## ⚠️ Errores comunes al leerlo

- **Olvidar `chomp`.** El defecto silencioso número uno.
- **No poner `use strict; use warnings;`.** Sin ellos, `$totl` es una variable global nueva y válida.
- **Confundir los comparadores.** `==` compara **números**, `eq` compara **cadenas**. `"10" == "10.0"`
  es cierto; `"10" eq "10.0"` es falso. Usar el equivocado es un error clásico y difícil de ver.
- **Ignorar el contexto.** `my $n = @lista;` da la longitud, no el primer elemento. Es correcto y
  desconcertante hasta que se interioriza.
- **Leer los sigilos como tipos.** `$a[0]` con `$` es correcto: describe la forma del **acceso**, no
  la del contenedor.
- **Creer que todo Perl es ilegible.** El Perl de golf y las líneas sueltas crípticas dieron fama al
  lenguaje, pero un Perl moderno con `use v5.36`, funciones con firma y módulos de CPAN es perfectamente
  ordenado.

## 📚 Fuentes y bibliografía

- [perl.org](https://www.perl.org/) y [perldoc.perl.org](https://perldoc.perl.org/) — sitio oficial y
  documentación completa, también disponible sin conexión con `perldoc`.
- [MetaCPAN](https://metacpan.org/) — el buscador moderno de CPAN.
- [CPAN Testers](http://www.cpantesters.org/) — los resultados de ejecutar las pruebas de cada módulo
  en decenas de plataformas; vale la pena verlo aunque no uses Perl.
- **Larry Wall, Tom Christiansen, Jon Orwant**, *Programming Perl*, O'Reilly — "el libro del camello",
  escrito por el autor del lenguaje; la referencia canónica.
- **chromatic**, *Modern Perl* — [gratis en línea](http://modernperlbooks.com/); cómo escribir Perl
  hoy y no como en 1998. Es el libro por el que empezar.
- **Mark Jason Dominus**, *Higher-Order Perl* — [gratis del autor](https://hop.perl.plover.com/);
  programación funcional avanzada, y uno de los mejores libros de programación de su década.
- **Jeffrey Friedl**, *Mastering Regular Expressions*, O'Reilly — la obra definitiva sobre expresiones
  regulares; útil sea cual sea tu lenguaje.

---

⏮️ [Volver al Atlas](README.md) · 🧟 [Los lenguajes que siguen vivos](vivos.md) ·
🔗 Relacionadas: [Tcl/Tk](tcl.md) · [Common Lisp](common-lisp.md) · [C](c.md)
