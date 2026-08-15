# 💎 Ruby — 1995

> [⬅️ Atlas](README.md) · [🗂️ Todas las fichas](lenguajes.md) · [📚 Índice de clases](../classes/README.md)

Ruby se diseñó con un criterio poco frecuente y declarado por su autor: **la felicidad de quien
programa**. De esa decisión salieron un lenguaje extraordinariamente expresivo, un marco web que
cambió la industria, y buena parte de las prácticas ágiles que hoy se dan por supuestas.

> **🎯 Por qué está en este programa**
>
> Ruby es un **primo de la familia de scripting dinámico** ([Atlas](README.md#scripting-dinamico)),
> cuyos representantes en el núcleo son [Python](python.md) y [PHP](php.md). **Es uno de los tres
> primos que se verifican en CI** en cada clase, junto a [Perl](perl.md) y [Lua](lua.md).
>
> Aporta al programa el modelo de objetos más puro de todos los lenguajes de uso masivo —**todo es un
> objeto, incluidos los números y `nil`**, como en [Smalltalk](smalltalk.md) (clase 111)— y **los
> bloques**, que son la forma más elegante de la clase 121 en un lenguaje mayoritario.

| | |
|---|---|
| **Año** | 1995; **1.9** con la máquina virtual YARV (2007); **3.0** en 2020 |
| **Autoría** | **Yukihiro Matsumoto ("Matz")**, Japón |
| **Familia** | Scripting dinámico; con [Smalltalk](smalltalk.md), [Perl](perl.md), Lisp y Eiffel dentro |
| **Paradigma** | Orientado a objetos puro, con fuerte componente funcional |
| **Tipado** | **Dinámico y fuerte**, con tipos gradual y opcionalmente comprobados (RBS) |
| **Memoria** | Recolección de basura generacional e incremental |
| **Ejecución** | Bytecode sobre YARV, con **JIT (YJIT)** desde 3.1 |
| **Estado** | 🟢 **Muy vivo** en web y automatización; Rails sigue siendo referencia |

---

## 📜 Historia

**Yukihiro Matsumoto** quería, en 1993, un lenguaje de guion verdaderamente orientado a objetos.
[Perl](perl.md) era potente y no era OO; [Python](python.md) era OO y —en su opinión— no lo bastante.
Su frase resume el criterio de diseño:

> **"Ruby está diseñado para hacer felices a los programadores."**

Eso no es marketing: es una decisión de ingeniería con consecuencias. **Cuando hay varias formas de
escribir algo, Ruby suele permitir todas**, y elige como idiomática la que se lee mejor en voz alta.
Es lo contrario del "solo una forma obvia" de Python, y la comparación entre los dos es uno de los
contrastes más instructivos de este Atlas.

Ruby fue popular en Japón durante años y desconocido fuera. **En 2004, David Heinemeier Hansson
publicó Ruby on Rails**, y eso lo cambió todo: Rails llevó al mundo entero **la convención sobre la
configuración**, los **generadores de código**, las **migraciones de base de datos** y una forma de
trabajar que hoy está en Django, Laravel, Phoenix y media docena más.

Y con Rails llegó también una **cultura de pruebas** —RSpec, Cucumber, el desarrollo dirigido por
pruebas como norma— que salió del ecosistema Ruby hacia todos los demás (clase 139).

Después vino la corrección del talón de Aquiles: **YARV** (1.9) sustituyó al intérprete de árbol,
**Ruby 3.0 (2020)** cumplió el objetivo *"Ruby 3x3"* —tres veces más rápido que 2.0— y **YJIT**,
escrito en [Rust](rust.md) por Shopify, ha dado saltos grandes de rendimiento en producción real.

## 🏭 Dónde vive hoy

- **Aplicaciones web**: Rails mueve GitHub, Shopify, Basecamp, Airbnb y decenas de miles de productos.
- **Automatización e infraestructura**: **Chef**, **Puppet**, **Vagrant**, **Fastlane** — la
  generación anterior de herramientas de configuración (clase 171).
- **Herramientas de desarrollo**: **Homebrew**, el gestor de paquetes de macOS, está escrito en Ruby.
- **Guiones de administración**, como sucesor natural de [Perl](perl.md).
- **Y como lenguaje de DSL**: Rakefile, Gemfile, Podfile y Vagrantfile son **programas Ruby que
  parecen ficheros de configuración** (clase 163).

## 🧠 Lo que enseña: todo es un objeto, y los bloques

**Uno, la pureza del modelo de objetos** (clase 111):

```ruby
5.class          # Integer
5.times { |i| puts i }
nil.to_a          # []      ← hasta nil es un objeto con métodos
Integer.ancestors # [Integer, Numeric, Comparable, Object, Kernel, BasicObject]
```

**No hay tipos primitivos.** En [Java](java.md) `int` no es un objeto y hay que envolverlo; en Ruby,
como en [Smalltalk](smalltalk.md), **no existe esa distinción** — y eso hace el lenguaje uniforme a
costa de rendimiento, que es lo que YJIT recupera con las cachés de envío de la clase 152.

**Dos, los bloques**, que son la aportación más reconocible:

```ruby
[1, 2, 3].map { |x| x * 2 }
File.open("datos.txt") do |f|      # ← el fichero se cierra SOLO al salir del bloque
  f.each_line { |l| puts l }
end
```

**Un bloque es un trozo de código que se pasa a un método**, y el método decide cuándo y cuántas veces
ejecutarlo. Eso da a la vez **iteración** (clase 115) y **gestión de recursos** (clase 132) — el
`File.open` con bloque es RAII sin destructores, y el `with` de Python y el `try-with-resources` de
Java persiguen lo mismo con más ceremonia.

**Y tres, las clases abiertas**, que son su característica más potente y más peligrosa:

```ruby
class String
  def gritar = upcase + "!"
end
"hola".gritar        # "HOLA!"
```

**Se puede añadir un método a cualquier clase, incluidas las del sistema.** Es lo que hace posible la
expresividad de Rails —`2.days.ago`, `"texto".pluralize`— y también lo que produce el problema que la
comunidad llama *monkey patching*: **dos bibliotecas que parchean lo mismo, y un fallo que nadie sabe
de dónde viene** (clase 150).

> **Ruby lo reconoció y dio una solución** (clase 146): los **refinamientos** (`refine`/`using`)
> limitan el parche al ámbito donde se activa. Es un buen ejemplo de un lenguaje corrigiendo su propio
> exceso sin quitar la característica.

## 🔄 Lo que se ha modernizado

- **YJIT** (Rust, desde 3.1): mejoras de rendimiento de dos dígitos en aplicaciones Rails reales.
- **RBS y Sorbet**: tipos **en ficheros aparte** o en anotaciones, comprobados por herramientas — el
  tipado gradual de la clase 146 llegando a Ruby.
- **Ractor** (3.0): actores con memoria aislada para paralelismo real, porque **Ruby también tiene un
  bloqueo global del intérprete** (clase 135). Y **fibras** para concurrencia asíncrona (clase 134).
- **Emparejamiento de patrones** (`case/in`, 2.7) con desestructuración de arreglos y `hash`.
- **`Bundler` con `Gemfile.lock`**: es de 2010 y fue **uno de los primeros ficheros de bloqueo
  populares** (clase 143), un modelo que copiaron después npm, Cargo y Composer.

## ⚙️ Cómo se ejecuta hoy

```bash
ruby main.rb < entrada.txt        # el comando de la clase 041

bundle install                     # dependencias, con Gemfile.lock (clase 143)
rubocop && rspec                    # estilo y pruebas (clases 139 y 146)
ruby --yjit main.rb                  # con el JIT activado
```

## 🧪 El programa de la clase 041 en Ruby

Esta versión **se ejecuta y se verifica en CI** contra el mismo `casos.json` que el núcleo.

```ruby
precio, cantidad, descuento = STDIN.gets.split.map(&:to_f)
total = precio * cantidad * (1 - descuento)
puts format("Total: %.2f", total)
```

**Lo que hay que ver.**

- **Tres líneas, y ninguna sobra.** Es la versión más corta de las veinte de la clase 041, y esa
  densidad legible es exactamente lo que el lenguaje persigue.
- **`&:to_f` es un símbolo convertido en bloque**: el idioma más característico de Ruby. Equivale a
  `{ |x| x.to_f }`, y aprovecha que **`to_f` es un método del objeto** — otra vez la pureza del modelo.
- **`split` sin argumentos** parte por espacios en blanco, como `strings.Fields` en [Go](go.md) y
  `split ' '` en [Perl](perl.md).
- **La asignación múltiple** desestructura los tres valores, como [Python](python.md).
- **`format` con `%.2f`** viene de [C](c.md), vía Perl: la herencia se ve.

## 📚 Fuentes y bibliografía

- [ruby-lang.org](https://www.ruby-lang.org/es/) — en español; y la
  [documentación de la biblioteca](https://docs.ruby-lang.org/en/master/).
- [Ruby Style Guide](https://rubystyle.guide/) — la guía comunitaria que RuboCop hace cumplir
  (clase 146).
- **Dave Thomas, Andy Hunt, Chad Fowler**, *Programming Ruby* — "el libro del pico"; la referencia
  clásica.
- **Sandi Metz**, *Practical Object-Oriented Design in Ruby* — uno de los mejores libros de diseño
  orientado a objetos que existen, en cualquier lenguaje (clases 149 y 166).
- **Paolo Perrotta**, *Metaprogramming Ruby*, Pragmatic — el modelo de objetos y las clases abiertas,
  explicados de verdad (clase 122).

---

⏮️ [Volver al Atlas](README.md) · 🗂️ [Todas las fichas](lenguajes.md) ·
🔗 Relacionadas: [Python](python.md) · [Perl](perl.md) · [Smalltalk](smalltalk.md) ·
[Elixir](elixir.md) · [Lua](lua.md)
