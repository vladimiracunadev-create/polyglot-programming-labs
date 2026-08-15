# 🐘 PHP — 1995

> [⬅️ Atlas](README.md) · [🗂️ Todas las fichas](lenguajes.md) · [📚 Índice de clases](../classes/README.md)

PHP no se diseñó: **creció**. Empezó como unos guiones en C para contar visitas a una página personal
y acabó ejecutando la mayor parte de la web. Esa historia explica sus rarezas — y también por qué,
después de una década de mala fama merecida, **PHP 8 es un lenguaje razonable que casi nadie ha vuelto
a mirar**.

> **🎯 Por qué está en este programa**
>
> **PHP es uno de los diez lenguajes del núcleo**, y comparte con [Python](python.md) la
> representación del **scripting dinámico** ([Atlas](README.md#scripting-dinamico)).
>
> Está en el núcleo por una razón que no es sentimental: **es el lenguaje del que depende una parte
> desproporcionada de la web pública**, y quien vaya a mantener software real se lo encontrará. Y
> aporta al programa el caso de estudio más claro de **coerción débil de tipos** y de **cómo un
> ecosistema entero corrige un lenguaje desde fuera** (clases 100, 143 y 146).

| | |
|---|---|
| **Año** | 1995; **PHP 5** con OO real (2004); **PHP 7** (2015); **PHP 8** (2020), anual |
| **Autoría** | **Rasmus Lerdorf**; el motor Zend, de **Andi Gutmans** y **Zeev Suraski** |
| **Familia** | Scripting dinámico; sintaxis de C y Perl |
| **Paradigma** | Imperativo y orientado a objetos; con rasgos y funciones de primera clase |
| **Tipado** | **Dinámico y débil**; con **declaraciones de tipo comprobadas** desde PHP 7 |
| **Memoria** | Conteo de referencias + recolector de ciclos; **liberación al final de la petición** |
| **Ejecución** | Bytecode con caché (OPcache); **JIT** desde PHP 8 |
| **Estado** | 🟢 **Enorme cuota de la web**; muy mejorado y poco reconocido |

---

## 📜 Historia

En **1994**, Rasmus Lerdorf escribió unos guiones en C para contar quién visitaba su currículum en
línea. Los llamó **Personal Home Page Tools**. No pretendían ser un lenguaje.

La gente empezó a pedírselos, y en **1995** los publicó. En **1997**, dos estudiantes israelíes
—**Andi Gutmans** y **Zeev Suraski**— reescribieron el analizador entero: nació el **motor Zend** y el
nombre pasó a ser el acrónimo recursivo **PHP: Hypertext Preprocessor**.

Y ahí está el origen de casi todo lo que se le critica: **la biblioteca estándar creció por
acumulación**, sin plan. De ahí la inconsistencia famosa —`strlen` pero `str_replace`,
`in_array($aguja, $pajar)` pero `strpos($pajar, $aguja)`— que es real y que hoy no se puede arreglar
sin romper media web.

Lo que sí se arregló:

- **PHP 5 (2004)**: un modelo de objetos de verdad, con excepciones e interfaces.
- **PHP 5.3 (2009)**: espacios de nombres y cierres — lo que hizo posible **Composer** (2012) y con él
  un ecosistema moderno de dependencias (clase 143).
- **PHP 7 (2015)**: el motor reescrito. **Duplicó el rendimiento y redujo a la mitad la memoria**, un
  salto que muy pocos lenguajes han dado. Y llegaron las **declaraciones de tipo escalares**.
- **PHP 8 (2020)**: **JIT**, atributos, `match`, promoción de propiedades del constructor, tipos unión,
  argumentos con nombre, `nullsafe`.
- **PHP 8.1-8.4**: enumerados, `readonly`, fibras (clase 134), propiedades con captadores.

## 🏭 Dónde vive hoy

- **WordPress**: mueve por sí solo una fracción enorme de todos los sitios web del mundo.
- **Comercio electrónico**: Magento, PrestaShop, WooCommerce.
- **Aplicaciones de empresa a medida**: **Laravel** y **Symfony** son marcos de primer nivel, con una
  calidad que sorprende a quien juzga PHP por su reputación de 2005.
- **Wikipedia**: MediaWiki está escrito en PHP (y sus plantillas ejecutan [Lua](lua.md), clase 163).
- **Sistemas de gestión de contenidos y foros**: Drupal, Joomla, Nextcloud.

## 🧠 Lo que enseña: el modelo de ejecución sin estado

PHP tiene un modelo que ningún otro del núcleo comparte y que explica la mitad de sus decisiones:
**"nada compartido"**.

```text
Llega una petición HTTP
  → se arranca un intérprete (o se reutiliza uno limpio)
  → se ejecuta el guion
  → se envía la respuesta
  → y SE DESTRUYE TODO el estado
```

**Y esa propiedad, que parece un derroche, es exactamente la primera regla del cierre de la clase
168**: **un servicio que no guarda estado en el proceso escala, se reinicia sin que nadie lo note y no
filtra datos de una petición a la siguiente**.

Es lo contrario de `mod_perl` (clase 163) y de un servidor Java de larga vida — y es la razón por la
que **PHP casi nunca sufre las fugas de estado entre usuarios** que aquellos tuvieron.

**El coste** es que no hay caché en proceso ni conexiones persistentes fáciles, y por eso el ecosistema
depende de OPcache, Redis y agrupadores de conexiones.

Y el otro tema que PHP enseña mejor que nadie es **la coerción débil** (clase 100):

```php
0 == "abc"        // false en PHP 8; TRUE hasta PHP 7  ← ¡lo arreglaron!
"1" == "01"        // true
"10" == "1e1"       // true
100 == "1e2"         // true
```

> **La línea corregida merece destacarse**, porque es un ejemplo excelente de la clase 175: **PHP 8
> cambió la comparación entre número y cadena no numérica**, rompiendo compatibilidad
> deliberadamente, porque **el comportamiento anterior causaba fallos de seguridad reales** —una
> comparación de contraseñas con `==` podía dar verdadero—. Fue una decisión difícil, documentada y
> correcta. Y la regla práctica sigue siendo la de la clase 146: **usar siempre `===`**.

## 🔄 Lo que se ha modernizado

- **Tipos por todas partes**: parámetros, retornos, propiedades, uniones, intersecciones, `never`.
  Con `declare(strict_types=1)`, PHP se comporta como un lenguaje de tipado fuerte.
- **Enumerados** (8.1) con métodos, y **`readonly`** (8.1/8.2) para inmutabilidad (clase 102).
- **Fibras** (8.1): corrutinas en el lenguaje, base de los tiempos de ejecución asíncronos
  (clase 134).
- **JIT** (8.0) — decisivo en cálculo, poco relevante en web, donde el cuello es la base de datos.
- **Composer y PSR**: gestor de dependencias con fichero de bloqueo (clase 143) y estándares de
  interoperabilidad entre marcos — el ecosistema puso el orden que el lenguaje no tenía.
- **Herramientas de análisis excelentes**: **PHPStan** y **Psalm** hacen análisis estático por niveles
  y detectan lo que el tipado dinámico deja pasar (clase 146).

## ⚙️ Cómo se ejecuta hoy

```bash
php main.php < entrada.txt        # el comando de la clase 041
php -S localhost:8000              # servidor de desarrollo, integrado

composer install                    # dependencias, con composer.lock (clase 143)
vendor/bin/phpstan analyse -l 9      # análisis estático estricto (clase 146)
vendor/bin/phpunit                    # pruebas (clase 139)
```

## 🧪 El programa de la clase 041 en PHP

```php
<?php
// PHP: dinámico y débilmente tipado; las variables llevan el prefijo $.
$linea = trim(fgets(STDIN));
[$precio, $cantidad, $descuento] = preg_split('/\s+/', $linea);

$precioUnitario = (float) $precio;
$cantidadInt = (int) $cantidad;
$descuentoFloat = (float) $descuento;

$subtotal = $precioUnitario * $cantidadInt;
$total = $subtotal * (1 - $descuentoFloat);

printf("Total: %.2f\n", $total);
```

**Lo que hay que ver.**

- **El `$` delante de cada variable** viene de [Perl](perl.md), y con él la sintaxis general del
  lenguaje. Es la marca visual de la familia.
- **Las conversiones explícitas `(float)` y `(int)` no son necesarias** —PHP convertiría solo— y están
  ahí a propósito: **hacen visible lo que el lenguaje haría en silencio**, que es exactamente la
  disciplina que la clase 146 recomienda en un lenguaje con coerción débil.
- **La desestructuración `[$a, $b, $c] = ...`** es de PHP 7.1; antes se escribía `list(...)`.
- **`printf` con `%.2f`** es la misma familia que [C](c.md) y [Perl](perl.md): PHP heredó la función
  y su formato.
- **Y con `declare(strict_types=1)` al principio**, este programa **fallaría** si algún argumento no
  fuera del tipo declarado — que es la forma moderna de escribirlo.

## 📚 Fuentes y bibliografía

- [Manual de PHP](https://www.php.net/manual/es/) — está en español y es sorprendentemente bueno; los
  comentarios de usuario, con precaución.
- [PHP: The Right Way](https://phptherightway.com/) — la guía comunitaria de buenas prácticas, y el
  antídoto contra los tutoriales de 2008 que siguen circulando.
- [PHP-FIG y los PSR](https://www.php-fig.org/psr/) — los estándares de interoperabilidad del
  ecosistema (clase 160).
- **Josh Lockhart**, *Modern PHP*, O'Reilly — el libro que separa el PHP actual del de su reputación.
- **Matthias Noback**, *Object Design Style Guide* y *Advanced Web Application Architecture* —
  arquitectura seria en PHP, aplicable a la Parte 9 del curso.

---

⏮️ [Volver al Atlas](README.md) · 🗂️ [Todas las fichas](lenguajes.md) ·
🔗 Relacionadas: [Python](python.md) · [Perl](perl.md) · [Ruby](ruby.md) · [JavaScript](javascript.md)
