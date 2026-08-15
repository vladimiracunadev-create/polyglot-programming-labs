# 🌙 Lua — 1993

> [⬅️ Atlas](README.md) · [🗂️ Todas las fichas](lenguajes.md) · [📚 Índice de clases](../classes/README.md)

Lua nació en Brasil para que unos ingenieros de Petrobras pudieran configurar simulaciones sin
recompilarlas, y hoy es **el lenguaje incrustado más usado del mundo**: está en World of Warcraft, en
Roblox, en Redis, en Nginx y en las plantillas de Wikipedia. Su intérprete completo **cabe en unos 200
kilobytes**.

> **🎯 Por qué está en este programa**
>
> Lua es un **primo de la familia de scripting dinámico** ([Atlas](README.md#scripting-dinamico)) y
> **uno de los tres primos verificados en CI**, junto a [Ruby](ruby.md) y [Perl](perl.md).
>
> Aporta al programa el caso central de una clase entera: **incrustar un lenguaje en otro**
> ([clase 163](../classes/parte-10-interoperabilidad-y-fronteras-entre-lenguajes/163-incrustar-un-lenguaje-en-otro-lua-python-embebido/README.md)),
> con las cuatro decisiones que eso obliga a tomar. Y aporta **la tabla como estructura única**
> (clase 099) y **las corrutinas** (clase 134) en su forma más simple.

| | |
|---|---|
| **Año** | 1993; **5.1** (2006) es la base de LuaJIT; **5.4** la actual |
| **Autoría** | **Roberto Ierusalimschy, Luiz Henrique de Figueiredo, Waldemar Celes** — PUC-Rio, Brasil |
| **Familia** | Scripting dinámico; con influencia de Scheme y de lenguajes de configuración |
| **Paradigma** | Multiparadigma; OO **por prototipos**, con metatablas |
| **Tipado** | **Dinámico**, con ocho tipos en total |
| **Memoria** | Recolector incremental o generacional |
| **Ejecución** | Bytecode sobre una VM de registros; **LuaJIT** compila a nativo |
| **Estado** | 🟢 **Dominante** como lenguaje incrustado; licencia MIT |

---

## 📜 Historia

En **1993**, el grupo Tecgraf de la **Pontificia Universidad Católica de Río de Janeiro** trabajaba
para **Petrobras**. Los ingenieros necesitaban configurar programas de simulación y visualización de
datos geológicos, y los ficheros de configuración se les habían quedado cortos: querían condicionales,
cálculos y variables (clase 163).

Y había una restricción de contexto que resultó decisiva: **Brasil tenía una política de reserva de
mercado para la informática**, así que comprar software extranjero era difícil. **Tuvieron que hacerlo
ellos.**

Diseñaron Lua —"luna" en portugués— con unos objetivos muy concretos que explican todo lo demás:

1. **Que se pueda incrustar en un programa de C** con una API pequeña.
2. **Que sea diminuto y portable**: C89 puro, sin dependencias.
3. **Que sea rápido**.
4. **Y que un ingeniero que no es programador pueda escribirlo.**

**LuaJIT** (Mike Pall, 2005) llevó el rendimiento a otro nivel: **es uno de los compiladores JIT más
rápidos que existen para un lenguaje dinámico**, y sigue basado en Lua 5.1 — lo que ha partido el
ecosistema en dos ramas que conviven.

Y el momento en que el mundo lo conoció fue **World of Warcraft (2004)**, que expuso toda su interfaz
como guiones Lua y creó un ecosistema de miles de complementos escritos por jugadores.

## 🏭 Dónde vive hoy

- **Videojuegos**: World of Warcraft, **Roblox** (con Luau, su variante tipada), Garry's Mod, Angry
  Birds, Love2D, y como lenguaje de guion en decenas de motores.
- **Infraestructura de red**: **OpenResty/Nginx** —lógica de peticiones en Lua—, HAProxy, Kong.
- **Bases de datos**: **Redis** ejecuta guiones Lua de forma atómica, lo que resuelve operaciones
  compuestas sin condiciones de carrera (clase 161).
- **Wikipedia**: el módulo Scribunto ejecuta Lua para las plantillas, en los servidores de Wikimedia.
- **Editores y herramientas**: **Neovim** lo adoptó como lenguaje de configuración y extensión.
- **Sistemas embebidos**: routers (OpenWrt), televisores, dispositivos industriales.

## 🧠 Lo que enseña: hacer mucho con muy poco

**Uno, la tabla es la única estructura de datos** (clase 099):

```lua
local t = {}
t[1] = "primero"          -- array
t.nombre = "Ana"           -- registro
t["clave"] = valor          -- diccionario
```

**Arreglo, registro, diccionario, objeto, espacio de nombres y módulo son la misma cosa.** Es
minimalismo llevado al extremo, y funciona: la biblioteca estándar entera se construye con tablas.

**Dos, las metatablas dan orientación a objetos sin tenerla:**

```lua
local Cuenta = {}
Cuenta.__index = Cuenta        -- ← si no encuentras el campo, búscalo aquí

function Cuenta.new(saldo)
  return setmetatable({saldo = saldo}, Cuenta)
end
function Cuenta:depositar(x) self.saldo = self.saldo + x end
```

**`__index` es la herencia por prototipos** (clase 112), la misma idea que
[JavaScript](javascript.md) y [Self](smalltalk.md) — construida con el mecanismo general de metatablas,
que también permite sobrecargar operadores y controlar el acceso.

**Y tres, las corrutinas** (clase 134), que Lua tiene desde 1993:

```lua
local co = coroutine.create(function()
  for i = 1, 3 do coroutine.yield(i) end
end)
print(coroutine.resume(co))   -- true 1
```

**Multitarea cooperativa con una pila propia**, que es la base de los generadores y de `async`/`await`
de casi todos los lenguajes modernos.

Y para la clase 163, lo importante es **cómo se incrusta**:

```c
lua_State *L = luaL_newstate();
luaL_openlibs(L);                     /* ← o NO abrirlas: se elige QUÉ existe */
lua_register(L, "dibujar", c_dibujar);
luaL_dofile(L, "config.lua");
lua_close(L);
```

> **La línea comentada es la clave y es la razón de su éxito**: **un estado de Lua recién creado no
> tiene `io`, ni `os`, ni nada**. El anfitrión abre las bibliotecas que quiera y registra las funciones
> que quiera. **Es el modelo de capacidades de la clase 153**, integrado en el diseño — y por eso
> Wikipedia puede ejecutar plantillas escritas por cualquiera sin que tumben el servidor.

## 🔄 Lo que se ha modernizado

- **Lua 5.4**: recolector generacional, enteros de 64 bits separados de los reales (5.3), y variables
  `<close>` para liberación determinista (clase 132).
- **LuaJIT**: JIT de trazas y una interfaz con C (`ffi`) que llama a bibliotecas nativas **sin escribir
  envoltorios** (clase 156).
- **Luau** (Roblox): Lua con **tipado gradual**, comprobación estática y aislamiento reforzado — con
  millones de personas escribiéndolo.
- **LuaRocks** como gestor de paquetes (clase 143).
- **Y ganchos de límite de instrucciones** (`lua_sethook`), que permiten cortar un guion que no
  termina — la segunda decisión del cierre de la clase 163.

## ⚙️ Cómo se ejecuta hoy

```bash
lua main.lua < entrada.txt        # el comando de la clase 041
luajit main.lua                    # el JIT, muy superior en cálculo

luarocks install <paquete>
```

## 🧪 El programa de la clase 041 en Lua

Esta versión **se ejecuta y se verifica en CI**.

```lua
local precio, cantidad, descuento = io.read("n", "n", "n")
local total = precio * cantidad * (1 - descuento)
print(string.format("Total: %.2f", total))
```

**Lo que hay que ver.**

- **`io.read("n", "n", "n")` lee tres números directamente**, sin partir la línea ni convertir. Es la
  lectura más limpia de las veinte versiones de la clase 041 — el intérprete hace el análisis.
- **`local` no es opcional en la práctica**: sin él, la variable sería **global**, que es el mismo
  problema que [M](mumps.md) tiene por defecto (clase 146). La regla del ecosistema es tajante:
  **`local` siempre**.
- **`string.format` con `%.2f`** es, otra vez, la herencia de [C](c.md) — Lua está escrito en C y su
  biblioteca lo refleja.
- **Y el detalle que no se ve**: hasta Lua 5.3, **todos los números eran reales de 64 bits**, como en
  [JavaScript](javascript.md). Desde 5.3 hay enteros separados, y esa distinción importa en índices y
  en identificadores grandes (clase 045).

## 📚 Fuentes y bibliografía

- [lua.org/manual](https://www.lua.org/manual/5.4/) — el manual completo cabe en unas cien páginas;
  es de lo más corto y preciso de esta lista.
- **Roberto Ierusalimschy**, *Programming in Lua*, 4.ª ed. — escrito por el autor del lenguaje; la
  primera edición está libre en línea.
- [Lua PIL y la wiki de usuarios](http://lua-users.org/wiki/) — patrones e idiomas de la comunidad.
- **Roberto Ierusalimschy et al.**, *The Evolution of Lua* (HOPL III, 2007) — el artículo que cuenta
  la historia y las decisiones de diseño; excelente lectura para la clase 163.
- [LuaJIT.org](https://luajit.org/) — y la documentación de su `ffi`, que es un caso de estudio de la
  clase 156.

---

⏮️ [Volver al Atlas](README.md) · 🗂️ [Todas las fichas](lenguajes.md) ·
🔗 Relacionadas: [Tcl](tcl.md) · [JavaScript](javascript.md) · [Python](python.md) · [C](c.md)
