# 🎬 ActionScript — 1998

> [⬅️ Atlas](README.md) · [🗂️ Todas las fichas](lenguajes.md) · [📚 Índice de clases](../classes/README.md)

ActionScript es el único lenguaje de este Atlas que **está muerto de verdad**, y por eso merece una
ficha: **su historia es la mejor lección sobre dependencia de plataforma que este curso puede ofrecer**.
Durante una década movió la mitad de la web interactiva; el 31 de diciembre de 2020 dejó de
ejecutarse en cualquier navegador del mundo, en un mismo día.

> **🎯 Por qué está en este programa**
>
> ActionScript es un **primo de la familia JavaScript / web** ([Atlas](README.md#javascript-web)) —de
> hecho, **es un dialecto de ECMAScript**, hermano directo de [JavaScript](javascript.md)—.
>
> Está aquí por una razón que no es técnica: **es el caso de estudio de qué pasa cuando el lenguaje
> depende de un tiempo de ejecución propietario** (clases 162 y 164). [PL/I](pl-i.md) y [RPG](rpg.md)
> enseñan lo mismo en su versión lenta; ActionScript lo enseña en su versión brusca. Y ActionScript 3
> es, además, **la implementación más completa que existió del abandonado ECMAScript 4**.

| | |
|---|---|
| **Año** | 1998 (AS1); **AS2** en 2003; **AS3** en 2006; **fin del Flash Player** el 31-12-2020 |
| **Autoría** | **Gary Grossman**, Macromedia; después Adobe |
| **Familia** | JavaScript / web — implementación de **ECMAScript 4**, que nunca se aprobó |
| **Paradigma** | Orientado a objetos con clases, dirigido por eventos |
| **Tipado** | AS1/AS2: dinámico. **AS3: estático opcional**, con comprobación en compilación |
| **Memoria** | Recolección de basura, con conteo de referencias y marcado |
| **Ejecución** | Bytecode sobre la **AVM2** del Flash Player, con JIT |
| **Estado** | 🔴 **Extinto en la web**; sobrevive en Adobe AIR y en emuladores |

---

## 📜 Historia

**Flash** empezó en 1996 como una herramienta de animación vectorial. En **1998**, Macromedia le añadió
un lenguaje de guion —**ActionScript**— para que los botones hicieran algo.

Y entonces pasó lo que nadie previó: **Flash se convirtió en la plataforma de aplicaciones de la web**.
Entre 2000 y 2010, **cuando el navegador no podía hacer casi nada** —sin `canvas`, sin vídeo nativo,
sin audio, con un JavaScript lento y con diferencias enormes entre navegadores—, Flash sí podía. Y
por eso llevaba dentro:

- **El vídeo de YouTube**, en sus primeros años.
- **Los juegos web**: Newgrounds, Kongregate, Miniclip, FarmVille — un ecosistema enorme.
- **Aplicaciones de empresa** con Flex, que competían con las de escritorio.
- **Y la publicidad y las animaciones** de media Internet.

**ActionScript 3 (2006)** fue un salto técnico serio: **tipado estático opcional, clases de verdad,
paquetes, excepciones y una máquina virtual nueva con JIT** que multiplicó el rendimiento por diez.
Estaba basado en la propuesta **ECMAScript 4**, la modernización de JavaScript que se estaba
negociando entonces.

**Y ES4 se abandonó en 2008.** JavaScript siguió por otro camino —el que llevó a ES5 y a ES6—, así que
**ActionScript 3 quedó como la única implementación completa de un estándar que nunca existió**: un
lenguaje huérfano, primo de JavaScript pero incompatible.

El final tiene fecha y carta: en **abril de 2010, Steve Jobs publicó *Thoughts on Flash***, explicando
por qué el iPhone nunca lo admitiría —batería, rendimiento, seguridad y, sobre todo, **no depender de
una capa propietaria de terceros**—. La web abierta alcanzó a Flash con HTML5, `canvas`, vídeo nativo
y WebGL. Adobe anunció el fin en 2017, y **el 31 de diciembre de 2020 el reproductor dejó de
funcionar**, con un bloqueo programado en el propio software.

## 🏭 Dónde vive hoy

- **Adobe AIR**, hoy mantenido por HARMAN: aplicaciones de escritorio y móviles heredadas siguen
  ejecutándose.
- **Apache Royale**: el sucesor libre de Flex, que **compila ActionScript a JavaScript**.
- **Ruffle**: un emulador de Flash **escrito en [Rust](rust.md) y compilado a
  [WebAssembly](../classes/parte-10-interoperabilidad-y-fronteras-entre-lenguajes/162-webassembly-como-objetivo-comun/README.md)**,
  que permite volver a ejecutar juegos y animaciones antiguos en el navegador.
- **Proyectos de preservación**: Flashpoint ha archivado más de 100.000 juegos y animaciones.

> **Ruffle merece la mención como cierre de la historia**: **la tecnología que sustituyó a Flash es
> la que hoy lo resucita**. Y esa es una lección de la clase 162 — **un objetivo de compilación
> abierto y estándar sobrevive a las plataformas propietarias**.

## 🧠 Lo que enseña: la dependencia de plataforma

**El día que Flash murió, murió todo lo escrito en ActionScript.** No hubo migración, ni capa de
compatibilidad, ni versión de mantenimiento: **el intérprete se apagó**.

Y merece contrastarlo con los demás lenguajes de este Atlas:

| Situación | Qué pasó |
|---|---|
| **[COBOL](cobol.md), 66 años** | sigue ejecutándose; hay compiladores libres y comerciales |
| **[Pascal](pascal.md), 55 años** | Free Pascal es libre y llega a plataformas nuevas (clase 162) |
| **[Smalltalk](smalltalk.md), 46 años** | SqueakJS ejecuta imágenes de 1978 en el navegador |
| **[PL/I](pl-i.md), 62 años** | vivo, y **sin implementación libre**: no llega a plataformas nuevas |
| **ActionScript, 22 años** | **extinto**: dependía de un reproductor de una sola empresa |

**Y el patrón es el de la clase 164**: **la supervivencia depende de que exista una implementación
libre y de que el formato sea abierto**. ActionScript no tenía ninguna de las dos.

Y la segunda lección, más fina, es sobre estándares: **AS3 implementó una propuesta que no llegó a
ser estándar**. Apostar a una especificación en discusión es un riesgo real, y aquí costó la
compatibilidad con el lenguaje del que venía.

## 🔄 Lo que quedó

- **La AVM2 y su bytecode** influyeron en el diseño de máquinas virtuales posteriores.
- **El modelo de eventos con burbujeo y captura** de Flash está en el DOM actual (clase 120).
- **Las corrutinas y la línea de tiempo** de Flash anticiparon patrones de animación que hoy están en
  CSS y en los marcos declarativos.
- **Y la lección de gobernanza**, que es lo que esta ficha aporta al curso.

## ⚙️ Cómo se ejecuta hoy

```bash
# Apache Royale: ActionScript compilado a JavaScript
mxmlc Venta.as -output venta.swf         # el compilador clásico (Flex SDK)
asjsc Venta.as                            # Royale: a JavaScript

# Y para ver contenido antiguo:
#   Ruffle (WebAssembly), en el navegador o como aplicación de escritorio
```

## 🧪 El programa de la clase 041 en ActionScript

Como en [SQL](sql.md) y en [Elm](elm.md), aquí el contrato **está adaptado** (clase 040): **el
reproductor Flash no tiene entrada estándar**, así que se ilustra el cálculo.

```actionscript
// ActionScript corre en el reproductor Flash, sin stdin: se ilustra el cálculo.
package {
    public class Venta {
        public static function total(precio:Number, cantidad:Number, descuento:Number):String {
            var t:Number = precio * cantidad * (1 - descuento);
            return "Total: " + t.toFixed(2);
        }
    }
}
```

**Lo que hay que ver.**

- **`precio:Number` es la anotación de tipo**, con **dos puntos**, igual que
  [TypeScript](typescript.md) — que llegó **catorce años después**. No es coincidencia: los dos
  descienden de la misma propuesta ES4.
- **`Number` es el mismo tipo único de coma flotante** de [JavaScript](javascript.md), y `toFixed(2)`
  es literalmente la misma función. **La familia se reconoce sin esfuerzo**, que es la tesis del
  Atlas.
- **`package` y `public class`** vienen de [Java](java.md), y son lo que ES4 quería añadir a
  JavaScript y no se aprobó.
- **Y la ausencia de entrada estándar no es un detalle del ejemplo**: es la marca de un lenguaje
  atado a un entorno concreto, que es exactamente lo que esta ficha cuenta.

## 📚 Fuentes y bibliografía

- [Apache Royale](https://royale.apache.org/) — el sucesor libre; documentación de migración desde
  Flex.
- [Ruffle](https://ruffle.rs/) — el emulador en Rust y WebAssembly; su código es interesante como
  caso de la clase 162.
- **Steve Jobs**, *Thoughts on Flash* (2010) — archivado; una página que conviene leer como documento
  de decisión tecnológica (clase 175).
- **Colin Moock**, *Essential ActionScript 3.0*, O'Reilly — la referencia del lenguaje en su momento.
- [Flashpoint Archive](https://flashpointarchive.org/) — el proyecto de preservación; un ejemplo de
  qué hace falta para que el software sobreviva a su plataforma (clase 154).

---

⏮️ [Volver al Atlas](README.md) · 🗂️ [Todas las fichas](lenguajes.md) ·
🔗 Relacionadas: [JavaScript](javascript.md) · [TypeScript](typescript.md) · [Dart](dart.md) ·
[Delphi](delphi.md)
