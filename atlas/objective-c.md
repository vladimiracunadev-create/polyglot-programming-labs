# 📱 Objective-C — 1984

> [⬅️ Atlas](README.md) · [🗂️ Todas las fichas](lenguajes.md) · [📚 Índice de clases](../classes/README.md)

Objective-C es **[C](c.md) más [Smalltalk](smalltalk.md)**, literalmente: la sintaxis de mensajes de
uno pegada sobre el otro, sin mezclarlos. Durante treinta años fue el lenguaje del Mac y del iPhone, y
aunque [Swift](swift.md) lo ha sustituido para lo nuevo, **hay demasiado código y demasiadas APIs
escritas en él como para que desaparezca**.

> **🎯 Por qué está en este programa**
>
> Objective-C es un **primo de la familia C / llaves** ([Atlas](README.md#c-llaves)), cuyo
> representante en el núcleo es [C](c.md).
>
> Aporta al programa algo que ningún otro lenguaje de la lista enseña con tanta claridad: **el
> despacho dinámico de mensajes en un lenguaje compilado**
> ([clases 111 y 112](../classes/parte-7-paradigmas/README.md)). En Objective-C
> **cualquier objeto puede recibir cualquier mensaje**, y eso se decide en ejecución — el modelo de
> Smalltalk, sobre memoria y punteros de C.

| | |
|---|---|
| **Año** | 1984; **Objective-C 2.0** en 2006; **ARC** en 2011 |
| **Autoría** | **Brad Cox** y **Tom Love**, Stepstone; adoptado por **NeXT** y luego Apple |
| **Familia** | C / llaves — con el modelo de objetos de [Smalltalk](smalltalk.md) |
| **Paradigma** | Imperativo + orientado a objetos por **paso de mensajes** |
| **Tipado** | **Estático para C, dinámico para los objetos**; `id` es "cualquier objeto" |
| **Memoria** | Conteo de referencias; manual hasta 2011, **automático (ARC)** desde entonces |
| **Ejecución** | Compilado a nativo (Clang), con un tiempo de ejecución que resuelve los mensajes |
| **Estado** | 🟡 **Mantenimiento**: no se elige para lo nuevo, y hay muchísimo escrito |

---

## 📜 Historia

A principios de los ochenta, **Brad Cox** quería la reutilización de componentes que
[Smalltalk](smalltalk.md) prometía, pero con el rendimiento y la portabilidad de C. Su solución fue
**no mezclar los dos lenguajes**: añadir a C **una sintaxis nueva y separada** —los corchetes— para el
envío de mensajes, dejando C intacto por debajo.

**Steve Jobs lo eligió para NeXTSTEP** en 1988, y ahí se construyeron las bibliotecas que hoy siguen
vivas: las clases con prefijo `NS` —de **NeXTSTEP**— que cualquiera que haya tocado macOS o iOS
reconoce.

Cuando Apple compró NeXT en 1996, NeXTSTEP se convirtió en **Mac OS X**, y Objective-C pasó a ser el
lenguaje de Apple. Con el **iPhone SDK (2008)** se volvió, de golpe, uno de los lenguajes más
demandados del mundo.

**Objective-C 2.0 (2006)** trajo propiedades, enumeración rápida y recolección de basura —después
descartada—; y **ARC (2011)** automatizó el conteo de referencias, que hasta entonces se escribía a
mano con `retain` y `release`.

En **2014** Apple presentó [Swift](swift.md) y Objective-C entró en mantenimiento. No ha desaparecido:
**buena parte de los marcos de Apple sigue siendo Objective-C por dentro**, y la interoperabilidad
entre los dos es diaria.

## 🏭 Dónde vive hoy

- **Aplicaciones de iOS y macOS anteriores a 2015**, que son muchísimas y siguen mantenidas.
- **Los marcos de Apple**: Foundation, AppKit y buena parte de UIKit tienen implementación
  Objective-C, aunque se usen desde Swift.
- **Bibliotecas y SDK de terceros** que aún no se han migrado.
- **GNUstep**: la reimplementación libre de los marcos de NeXT, que sigue viva.

## 🧠 Lo que enseña: el mensaje no es una llamada

Esta es la idea que hay que llevarse:

```objc
[objeto hacerAlgoCon:valor y:otro];       // NO es objeto.hacerAlgo(valor, otro)
```

**Enviar un mensaje no es llamar a un método**: es pedirle al tiempo de ejecución que busque qué
método corresponde, **en ejecución**, por el nombre del selector.

Y de ahí salen tres consecuencias que la clase 111 desarrolla:

- **Se puede enviar un mensaje a `nil` y no pasa nada** — devuelve cero y sigue. Es una decisión
  deliberada que elimina montañas de comprobaciones y que a la vez esconde errores.
- **Se puede preguntar en ejecución** si un objeto responde a un mensaje (`respondsToSelector:`), y
  **añadir métodos a una clase existente** con las *categorías* — lo que en Ruby se llama clase
  abierta y en C# métodos de extensión.
- **Y existe `forwardInvocation:`**, el equivalente de `doesNotUnderstand:` de
  [Smalltalk](smalltalk.md) (clase 158): un objeto puede **interceptar los mensajes que no entiende** y
  reenviarlos. Es la base de los objetos proxy y de la simulación en pruebas, sin biblioteca.

> **Y el precio es el de siempre en este curso** (clase 164): esa flexibilidad **impide comprobar en
> compilación** que el mensaje existe. Enviar un selector mal escrito compila con un aviso y falla al
> ejecutarse. Swift eligió lo contrario, y esa es la diferencia principal entre los dos.

## 🔄 Lo que se ha modernizado

- **ARC** (2011): el compilador inserta `retain`/`release`, con lo que la gestión manual desapareció
  — sin recolector y sin pausas (clase 131).
- **Literales y suscripción** (`@[]`, `@{}`, `array[0]`), que hicieron el lenguaje mucho menos
  verboso.
- **Anotaciones de nulabilidad** (`nullable`, `nonnull`) y **genéricos ligeros**, añadidos sobre todo
  **para que Swift pueda importar las APIs con tipos precisos** — la interoperabilidad guiando el
  diseño.
- **Módulos** (`@import`) en lugar de `#import` textual, con compilación mucho más rápida
  (clase 149).

## ⚙️ Cómo se ejecuta hoy

```bash
clang -framework Foundation main.m -o venta        # macOS
gcc `gnustep-config --objc-flags` main.m -o venta   # GNUstep, en Linux
```

## 🧪 El programa de la clase 041 en Objective-C

Es la versión que aparece en el
[`primos.md` de la clase 041](../classes/parte-3-valores-tipos-y-variables/041-literales-valores-variables-y-constantes/primos.md).

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        double precio, cantidad, descuento;
        scanf("%lf %lf %lf", &precio, &cantidad, &descuento);
        double total = precio * cantidad * (1 - descuento);
        printf("Total: %.2f\n", total);
    }
    return 0;
}
```

**Lo que hay que ver.**

- **Es C tal cual.** `scanf`, `printf`, `double`, `&precio`: **el programa de la ficha de [C](c.md)
  compila aquí sin tocar nada**. Esa es la tesis del lenguaje — la capa de objetos **se añade**, no
  sustituye.
- **`@autoreleasepool` es lo único que no es C**, y marca el ámbito donde se liberan los objetos
  aplazados. Con ARC ya casi no hace falta, y aparece por costumbre.
- **Lo que este ejemplo no enseña son los corchetes**, porque no crea ningún objeto. La versión
  idiomática usaría `NSString` y `NSScanner`, y ahí aparecería `[cadena doubleValue]` — el paso de
  mensajes.
- **Y esa mezcla es exactamente la seña de identidad**: en un mismo fichero conviven la aritmética de
  C y el modelo de objetos de Smalltalk, **sin fundirse**.

## 📚 Fuentes y bibliografía

- [Documentación de Apple para Objective-C](https://developer.apple.com/documentation/objectivec) y la
  guía *Programming with Objective-C*.
- [Objective-C Runtime Reference](https://developer.apple.com/documentation/objectivec/objective-c_runtime)
  — la API del tiempo de ejecución; leerla explica cómo funciona el despacho (clase 111).
- [GNUstep](https://www.gnustep.org/) — para ejecutarlo fuera de Apple.
- **Aaron Hillegass, Mikey Ward**, *Objective-C Programming: The Big Nerd Ranch Guide* — la
  introducción de referencia.
- **Matt Galloway**, *Effective Objective-C 2.0*, Addison-Wesley — 52 elementos sobre el lenguaje y su
  tiempo de ejecución.

---

⏮️ [Volver al Atlas](README.md) · 🗂️ [Todas las fichas](lenguajes.md) ·
🔗 Relacionadas: [C](c.md) · [Smalltalk](smalltalk.md) · [Swift](swift.md) · [C++](cpp.md)
