# 🎯 Dart — 2011

> [⬅️ Atlas](README.md) · [🗂️ Todas las fichas](lenguajes.md) · [📚 Índice de clases](../classes/README.md)

Dart nació para sustituir a [JavaScript](javascript.md) en el navegador, fracasó en ese objetivo, y
**encontró después su razón de ser en Flutter** — donde hoy mueve aplicaciones móviles, de escritorio y
web con un solo código. Es un buen recordatorio de que un lenguaje puede acertar por un camino que no
era el previsto.

> **🎯 Por qué está en este programa**
>
> Dart es un **primo de la familia JavaScript / web** ([Atlas](README.md#javascript-web)), cuyos
> representantes en el núcleo son [JavaScript](javascript.md) y [TypeScript](typescript.md).
>
> Aporta al programa algo muy concreto y poco común: **el mismo lenguaje se compila de dos maneras
> distintas según el momento** — JIT con recarga en caliente mientras se desarrolla, y **AOT a código
> nativo** al publicar
> ([clases 126 y 174](../classes/parte-8-como-funcionan-los-lenguajes/README.md)). Es la
> demostración más clara de que **JIT y AOT no son propiedades del lenguaje, sino decisiones del
> despliegue**.

| | |
|---|---|
| **Año** | 2011; **2.0** con tipado sano (2018); **3.0** (2023) con seguridad frente a nulos completa |
| **Autoría** | **Lars Bak** y **Kasper Lund**, Google — los autores de la máquina virtual V8 |
| **Familia** | JavaScript / web; sintaxis de C, con influencia de [Java](java.md) y Smalltalk |
| **Paradigma** | Orientado a objetos con clases; con cierres y programación asíncrona |
| **Tipado** | **Estático, sano y con nulabilidad comprobada**; inferencia amplia |
| **Memoria** | Recolección de basura generacional, optimizada para objetos de vida corta |
| **Ejecución** | **JIT** en desarrollo, **AOT nativo** al publicar, y **a JavaScript o WebAssembly** |
| **Estado** | 🟢 **Muy vivo** gracias a Flutter |

---

## 📜 Historia

En **2011**, Google presentó Dart con una ambición explícita: **sustituir a JavaScript**. El plan
incluía una máquina virtual de Dart dentro de Chrome. Los demás navegadores no lo aceptaron —con
razón: nadie quería un segundo lenguaje web controlado por una empresa— y en **2015 Google retiró el
plan**.

Dart quedó como un lenguaje que compilaba a JavaScript y que casi nadie usaba. Y entonces, en
**2017**, apareció **Flutter**, y con él la razón de existir: un kit de interfaz que **dibuja cada
píxel él mismo** —sin usar los controles nativos— y que necesitaba un lenguaje con **recarga en
caliente** para desarrollar y **compilación nativa** para publicar.

**Dart 2.0 (2018)** hizo el tipado **sano** —hasta entonces era opcional y no garantizaba nada— y
**Dart 3.0 (2023)** completó la **seguridad frente a nulos**, además de añadir registros,
emparejamiento de patrones y clases selladas.

## 🏭 Dónde vive hoy

- **Flutter**: aplicaciones móviles (Android e iOS), de escritorio y web con un solo código. Es, con
  diferencia, el uso principal.
- **Google**: partes de Google Ads, Google Pay y varias herramientas internas.
- **Servidores**: con `dart:io` y marcos como Serverpod, aunque es un nicho pequeño.
- **Herramientas de línea de comandos**: por la compilación AOT y el binario autocontenido
  (clase 167).

## 🧠 Lo que enseña: dos compiladores para un lenguaje

Esta es la idea que hay que llevarse de la ficha:

```text
Durante el DESARROLLO:
  JIT + recarga en caliente → se cambia una línea y la aplicación se actualiza
  en menos de un segundo, CONSERVANDO su estado.

Al PUBLICAR:
  AOT a código nativo ARM o x86 → arranque instantáneo, sin JIT y sin sobresaltos
  de rendimiento en la primera ejecución de cada función.
```

**La recarga en caliente con conservación de estado** es lo que hace productivo a Flutter, y es
exactamente lo que la clase 124 describe en [Smalltalk](smalltalk.md) y [Lisp](common-lisp.md) —**el
ciclo corto como capacidad, no como comodidad**— llegando al desarrollo móvil.

**Y la compilación AOT resuelve el problema contrario**: en un móvil no se puede pagar el calentamiento
del JIT ni las pausas del recolector durante una animación (clase 152).

Y hay una segunda cosa que Dart hace bien y merece señalarse: **la seguridad frente a nulos aplicada a
un lenguaje ya existente**.

```dart
String nombre = null;      // ✗ no compila
String? apodo = null;       // ✓ el ? declara que puede faltar
print(apodo!.length);        // ! afirma que no es nulo, y falla si lo es
```

**La migración se hizo gradual**, mezclando código migrado y sin migrar durante la transición — el
mismo problema que [TypeScript](typescript.md) resolvió con el tipado gradual (clase 143).

## 🔄 Lo que se ha modernizado

- **Registros y emparejamiento de patrones** (3.0): tipos de datos algebraicos y desestructuración
  (clase 100).
- **Clases selladas** y `switch` exhaustivo comprobado por el compilador.
- **Compilación a WebAssembly** (`dart2wasm`) usando **WasmGC**, además del clásico `dart2js`
  (clase 162).
- **`dart format` sin opciones**, como `gofmt` (clase 146), y `dart analyze` integrado.
- **Interoperabilidad** con Java/Kotlin, Swift/Objective-C y C mediante `dart:ffi` (clase 156).

## ⚙️ Cómo se ejecuta hoy

```bash
dart run main.dart < entrada.txt       # el comando de la clase 041
dart compile exe main.dart -o venta     # ← binario nativo AOT (clase 174)
dart compile js main.dart                # a JavaScript

dart format . && dart analyze            # calidad (clase 146)
dart test                                 # pruebas (clase 139)
flutter run                                # con recarga en caliente
```

## 🧪 El programa de la clase 041 en Dart

```dart
import 'dart:io';

void main() {
  final v = stdin.readLineSync()!.split(' ').map(double.parse).toList();
  final total = v[0] * v[1] * (1 - v[2]);
  print('Total: ${total.toStringAsFixed(2)}');
}
```

**Lo que hay que ver.**

- **El `!` después de `readLineSync()`** es la seguridad frente a nulos en acción: el método devuelve
  `String?` —puede no haber línea— y `!` **afirma** que la hay. **En [JavaScript](javascript.md) esa
  posibilidad no aparece en ningún sitio**, y ahí está la diferencia.
- **`toStringAsFixed(2)` es el `toFixed` de JavaScript** con otro nombre: la herencia de familia se ve
  en la biblioteca, no solo en la sintaxis.
- **`final` fija el nombre, no el contenido** (clase 102), igual que `const` de JavaScript. Para
  inmutabilidad real en tiempo de compilación, Dart tiene `const`.
- **`double.parse` como función de primera clase** pasada a `map` — el estilo funcional que comparte
  con toda la familia.

## 📚 Fuentes y bibliografía

- [dart.dev](https://dart.dev/guides) — el tour del lenguaje y la guía de estilo, muy bien escritos.
- [Effective Dart](https://dart.dev/effective-dart) — la guía oficial de estilo, diseño y
  documentación (clases 146 y 154).
- [docs.flutter.dev](https://docs.flutter.dev/) — para el contexto en el que se usa de verdad.
- **Randal Schwartz, Kathy Walrath et al.**, *Dart: Up and Running*, O'Reilly — histórico pero útil
  para el porqué del diseño.
- [Blog de Dart en Medium](https://medium.com/dartlang) — las notas de cada versión, con la motivación
  de cada característica.

---

⏮️ [Volver al Atlas](README.md) · 🗂️ [Todas las fichas](lenguajes.md) ·
🔗 Relacionadas: [JavaScript](javascript.md) · [TypeScript](typescript.md) · [Swift](swift.md) ·
[Kotlin](kotlin.md) · [Java](java.md)
